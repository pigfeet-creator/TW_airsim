#!/usr/bin/env python3
"""
Air campaign over the Taiwan Strait — consolidated parametric model.

Reproduces every figure in air-campaign-model-report.md.

Model logic
-----------
The controlling quantity is f, the fraction of a based force airborne over the
target area at any moment:

    f = (sorties per day) * (loiter hours per sortie) / 24

loiter is governed by the LAST REFUELLING POINT, not by the base: from the
tanker orbit inward the fighter is on internal fuel, so

    loiter_hours = 2 * (combat_radius - tanker_to_target) / cruise * LOITER_EFF

sorties/day is capped by cycle time, and either crew duty hours (no rotation)
or the maintenance ceiling (with 24h crew rotation).

Attrition uses a mechanistic BVR engagement model (finite magazines,
simultaneous fire, explicit target assignment) rather than assuming a
Lanchester exponent. The empirical exponent that emerges is alpha ~ 0.56,
midway between the linear and square laws.

Usage:  python3 taiwan_air_model.py [section]
        sections: geometry onstation engagement basing y2030 all
"""
import sys
import numpy as np

# ----------------------------------------------------------------------
# CONSTANTS AND ASSUMPTIONS  (see report's "soft parameters" section)
# ----------------------------------------------------------------------
R_EARTH_NM   = 3440.065
CRUISE_KT    = 450.0
LOITER_EFF   = 1.4     # loiter hours per cruise-hour-equivalent of fuel
MAINT_CEIL   = 4.0     # max sorties/aircraft/day (maintenance) - SOFT, key param
CREW_HOURS   = 12.0    # flight hours/crew/day when no rotation
TURN_US_H    = 2.0
TURN_CN_H    = 1.25
OFFLOAD_LB   = 90000.0 # usable offload per tanker sortie
FUEL_BURN    = 10.0    # lb/nm, fighter cruise - SOFT
TANKER_SPOTS = 3.0     # fighter ramp spots per tanker - SOFT, sets force ceiling
TKR_SORTIES  = 2.0

# Geography
STRAIT       = (24.50, 119.30)   # centre of the Taiwan Strait
TANKER_ORBIT = (22.00, 124.50)   # optimal under a 350nm coast-standoff constraint
D_PEN_CN     = 84.0              # Chinese tanker orbit to Strait (over own territory)

CHINA_COAST = [(30.0,121.6),(28.5,121.5),(27.0,120.6),(26.0,119.6),(25.0,119.0),
               (24.0,118.0),(23.4,116.7),(22.8,115.4),(22.5,114.0),(21.9,112.5)]

# combat radius, nm (unrefuelled, includes reserves)
RADIUS = {"F/A-18E":400, "F-35C":620, "F-35A":670, "F-15E":790, "F-15EX":790,
          "F-22A":590, "CCA":700, "J-10C":450, "J-16":800, "J-20":1100}

US_BASES = [  # (name, coords, ramp capacity in fighter spots)
    ("Kyushu",       (32.80,131.00), 120),
    ("W Honshu",     (34.40,132.50), 130),
    ("C Honshu",     (35.30,137.00), 140),
    ("Kanto",        (35.75,139.35),  60),
    ("Guam",         (13.58,144.92),  90),
    ("Misawa",       (40.70,141.37),  80),
]
PHIL_BASES = [
    ("N Luzon (EDCA)",  (18.20,121.60), 100),
    ("C Luzon (Basa)",  (15.00,120.50), 100),
]
CN_BANDS = [(90,0.50),(270,0.35),(540,0.15)]  # (distance to Strait, weight)


# ----------------------------------------------------------------------
def haversine(a, b):
    la1,lo1,la2,lo2 = map(np.radians,[a[0],a[1],b[0],b[1]])
    return R_EARTH_NM*2*np.arcsin(np.sqrt(
        np.sin((la2-la1)/2)**2 + np.cos(la1)*np.cos(la2)*np.sin((lo2-lo1)/2)**2))

def dist_to_coast(p):
    return min(haversine(p,c) for c in CHINA_COAST)

def loiter_hours(radius_nm, pen_nm):
    """Hours on station, given the penetration leg is flown on internal fuel."""
    return max((2*(radius_nm-pen_nm)/CRUISE_KT)*LOITER_EFF, 0.0)

def on_station(radius_nm, base_to_tanker_nm, pen_nm, turn_h, rotation=True):
    """Returns (f, loiter_h, sorties_per_day, sortie_h)."""
    l = loiter_hours(radius_nm, pen_nm)
    if l <= 0:
        return 0.0, 0.0, 0.0, 0.0
    sortie = 2*base_to_tanker_nm/CRUISE_KT + 2*pen_nm/CRUISE_KT + l
    cycle_cap = 24/(sortie+turn_h)
    n = min(cycle_cap, MAINT_CEIL) if rotation else min(cycle_cap, CREW_HOURS/sortie, MAINT_CEIL)
    return n*l/24, l, n, sortie


# ----------------------------------------------------------------------
def china_airborne(total_committed, tanking=True, rotation=True):
    pen = D_PEN_CN if tanking else 0.0
    f_tot = 0.0
    for d, w in CN_BANDS:
        # unrefuelled case: the "penetration" leg is the whole base-to-Strait run
        if tanking:
            fa,_,_,_ = on_station(RADIUS["J-16"], d, pen, TURN_CN_H, rotation)
            fb,_,_,_ = on_station(RADIUS["J-10C"], d, pen, TURN_CN_H, rotation)
        else:
            fa,_,_,_ = on_station(RADIUS["J-16"], 0.0, d, TURN_CN_H, rotation)
            fb,_,_,_ = on_station(RADIUS["J-10C"], 0.0, d, TURN_CN_H, rotation)
        f_tot += w*(0.5*fa + 0.5*fb)
    return total_committed*f_tot, f_tot


def us_max_force(bases, mix, total_spots, rotation=True):
    """
    Self-consistent solution: fighters + the tankers needed to fly them must
    fit inside the available ramp. Returns (airborne, n_aircraft, n_tankers, spots).
    mix: list of (label, radius, share, ramp_spots_each)
    """
    d_pen = haversine(TANKER_ORBIT, STRAIT)
    rows = []
    for nm, c, cap in bases:
        d = haversine(c, TANKER_ORBIT)
        f_w = n_w = 0.0
        for _, R, share, _ in mix:
            f, l, n, s = on_station(R, d, d_pen, TURN_US_H, rotation)
            f_w += share*f; n_w += share*n
        rows.append((nm, d, cap, f_w, n_w))
    spots_each = sum(share*sp for _, _, share, sp in mix)

    best = None
    for N in range(20, 4001, 10):
        rem, dist, ab = N, 0.0, 0.0
        for nm, d, cap, f_w, n_w in rows:
            take = min(rem, cap/spots_each)
            ab += take*f_w
            dist += take*n_w*2*(d + d_pen)
            rem -= take
        if rem > 0:
            continue
        tankers = dist*FUEL_BURN*0.55/(OFFLOAD_LB*TKR_SORTIES)
        used = N*spots_each + tankers*TANKER_SPOTS
        if used <= total_spots and (best is None or ab > best[0]):
            best = (ab, N, tankers, used)
    return best, rows


# ----------------------------------------------------------------------
def engagement(nB, nR, pk=0.25, mag=6, rng=None, coordinated=True):
    """One BVR engagement, identical aircraft. Returns (blue_lost, red_lost)."""
    rng = rng or np.random.default_rng()
    nB, nR = int(nB), int(nR)
    if nB == 0 or nR == 0:
        return 0, 0
    Bm, Rm = np.full(nB, mag), np.full(nR, mag)
    Ba, Ra = np.ones(nB, bool), np.ones(nR, bool)
    while Ba.any() and Ra.any():
        bs = np.flatnonzero(Ba & (Bm > 0)); rs = np.flatnonzero(Ra & (Rm > 0))
        if len(bs) == 0 and len(rs) == 0:
            break
        ra, ba = np.flatnonzero(Ra), np.flatnonzero(Ba)
        if coordinated:
            bt = np.resize(rng.permutation(ra), len(bs)) if len(bs) else np.array([], int)
            rt = np.resize(rng.permutation(ba), len(rs)) if len(rs) else np.array([], int)
        else:
            bt = rng.choice(ra, len(bs)) if len(bs) else np.array([], int)
            rt = rng.choice(ba, len(rs)) if len(rs) else np.array([], int)
        Bm[bs] -= 1; Rm[rs] -= 1
        rk = np.unique(bt[rng.random(len(bt)) < pk]) if len(bt) else np.array([], int)
        bk = np.unique(rt[rng.random(len(rt)) < pk]) if len(rt) else np.array([], int)
        Ra[rk] = False; Ba[bk] = False
    return nB - Ba.sum(), nR - Ra.sum()


def campaign(us_force, cn_force, f_us, f_cn, pk=0.25, trials=250, seed=9):
    """Repeated engagements; each side commits its on-station fraction."""
    rng = np.random.default_rng(seed)
    ue, ce = [], []
    for _ in range(trials):
        U, C = float(us_force), float(cn_force)
        while U >= 1 and C >= 1:
            au = max(int(round(f_us*U)), 1)
            ac = max(int(round(f_cn*C)), 1)
            bl, rl = engagement(au, ac, pk, 6, rng)
            if bl == 0 and rl == 0:
                break
            U -= bl; C -= rl
        ue.append(max(U, 0)); ce.append(max(C, 0))
    return np.mean(ue), np.mean(ce)


# ----------------------------------------------------------------------
def sec_geometry():
    print("="*74); print("GEOMETRY"); print("="*74)
    d_pen = haversine(TANKER_ORBIT, STRAIT)
    print(f"  Strait to nearest Chinese coast : {dist_to_coast(STRAIT):5.0f} nm")
    print(f"  tanker orbit to Strait          : {d_pen:5.0f} nm")
    print(f"  tanker orbit to Chinese coast   : {dist_to_coast(TANKER_ORBIT):5.0f} nm")
    print("\n  Standoff from the target and from the threat are the same number:")
    for t in [301,351,475,649]:
        best=None
        for x in np.linspace(0,1,500):
            p=(STRAIT[0]+x*(33.68-STRAIT[0]), STRAIT[1]+x*(131.04-STRAIT[1]))
            d=haversine(p,STRAIT)
            if best is None or abs(d-t)<abs(best[0]-t): best=(d,dist_to_coast(p))
        print(f"    {best[0]:4.0f}nm from Strait -> {best[1]:4.0f}nm from mainland")

    print("\n  Dogleg (Kyushu -> tanker -> Strait):")
    ky=(33.68,131.04)
    l1,l2=haversine(ky,TANKER_ORBIT), d_pen
    gc=haversine(ky,STRAIT)
    print(f"    legs {l1:.0f}nm + {l2:.0f}nm = {l1+l2:.0f}nm vs {gc:.0f}nm direct "
          f"({100*(l1+l2)/gc-100:+.0f}%)")
    print(f"    extra offload demand: +{100*2*(l1+l2-gc)*FUEL_BURN/24000:.0f}%")

    print("\n  Base exposure (distance from nearest Chinese coast):")
    for nm,c in [("Kyushu",(33.68,131.04)),("C Luzon",(15.0,120.5)),
                 ("N Luzon",(18.2,121.6)),("Kadena",(26.35,127.77))]:
        print(f"    {nm:<10} {dist_to_coast(c):5.0f} nm")


def sec_onstation():
    print("="*74); print("ON-STATION FRACTIONS"); print("="*74)
    d_pen = haversine(TANKER_ORBIT, STRAIT)
    print(f"\n  Tanker line sensitivity (loiter hours), penetration = line distance:")
    print(f"  {'line':>6}" + "".join(f"{k:>10}" for k in
          ["F/A-18E","F-35C","F-35A","F-15E"]))
    for T in [200,300,400,500,600]:
        row=f"  {T:6}"
        for k in ["F/A-18E","F-35C","F-35A","F-15E"]:
            l=loiter_hours(RADIUS[k],T)
            row += f"{('  --  ' if l<=0 else f'{l:.2f}h'):>10}"
        print(row)

    print(f"\n  US bases (F-35A, penetration {d_pen:.0f}nm, 24h crew rotation):")
    print(f"  {'base':<12}{'to tanker':>10}{'sortie':>8}{'sort/day':>10}{'f':>8}")
    for nm,c,cap in US_BASES:
        d=haversine(c,TANKER_ORBIT)
        f,l,n,s=on_station(RADIUS["F-35A"],d,d_pen,TURN_US_H,True)
        print(f"  {nm:<12}{d:9.0f}nm{s:7.2f}h{n:10.2f}{f:8.3f}")

    print("\n  Chinese blended f:")
    for tank in [False,True]:
        for rot in [False,True]:
            _,f=china_airborne(1,tank,rot)
            print(f"    tanking={str(tank):<5} rotation={str(rot):<5} f={f:.3f}")


def sec_engagement():
    print("="*74); print("ENGAGEMENT MODEL — pure numbers, identical aircraft")
    print("="*74)
    rng=np.random.default_rng(12345)
    print(f"  {'ratio':>6}{'small lost':>12}{'large lost':>12}{'disadvantage':>14}")
    base=40; xs,ys=[],[]
    for ratio in [1.25,1.5,2.0,3.0,4.0,5.0]:
        nB,nR=base,int(base*ratio)
        bl=rl=0
        for _ in range(3000):
            b,r=engagement(nB,nR,rng=rng); bl+=b; rl+=r
        bl/=3000; rl/=3000
        xs.append(ratio); ys.append(bl/rl)
        print(f"  {ratio:6.2f}{bl:12.1f}{rl:12.1f}{bl/rl:13.2f}:1")
    alpha=np.polyfit(np.log(xs),np.log(ys),1)[0]
    print(f"\n  empirical Lanchester exponent alpha = {alpha:.3f}")
    print("  (0 = linear law, 1 = square law)")

    print("\n  Quality sensitivity (400 US v 975 China, f 0.137/0.266):")
    for k in [1.0,1.2,1.5,2.0]:
        u,c=campaign(400,975,0.137*k,0.266,trials=120)
        print(f"    k={k:<4} China retains {100*c/975:3.0f}%  "
              f"LER 1 : {(400-u)/(975-c):.1f}")


def sec_basing():
    print("="*74); print("BASING CEILING (2026)"); print("="*74)
    mix=[("F-35A",RADIUS["F-35A"],1.0,1.0)]
    best,rows=us_max_force(US_BASES,mix,620,True)
    ab,N,tk,used=best
    cn,_=china_airborne(750,True,True)
    print(f"  self-consistent max: {N:.0f} fighters + {tk:.0f} tankers "
          f"({used:.0f}/620 spots)")
    print(f"  US airborne {ab:.1f}  |  China airborne {cn:.1f}  "
          f"|  ratio {cn/ab:.1f}:1")
    print("\n  Tanker ramp displacement:")
    for t in [0,60,100,140,180]:
        fit=max(620-t*TANKER_SPOTS,0); rem=fit; a=0
        for nm,d,cap,f_w,n_w in rows:
            take=min(rem,cap); a+=take*f_w; rem-=take
        r=f"{cn/a:5.1f}:1" if a>0 else "  n/a"
        print(f"    {t:4} tankers -> {fit:4.0f} fighter spots, airborne {a:6.1f}, {r}")


def sec_y2030():
    print("="*74); print("2030 PROJECTION"); print("="*74)
    MIX26=[("F-35A",RADIUS["F-35A"],1.0,1.0)]
    MIX30=[("F-35A",RADIUS["F-35A"],0.55,1.0),
           ("F-15EX",RADIUS["F-15EX"],0.20,1.0),
           ("CCA",RADIUS["CCA"],0.25,0.5)]
    scen=[("2026 baseline",US_BASES,MIX26,620,750),
          ("2030 same mix/basing",US_BASES,MIX26,620,1400),
          ("2030 new mix",US_BASES,MIX30,620,1400),
          ("2030 + Philippines",US_BASES+PHIL_BASES,MIX30,820,1400),
          ("2030 + Phil + 30% ramp",US_BASES+PHIL_BASES,MIX30,1066,1400)]
    for lbl,bases,mix,spots,cn_tot in scen:
        best,_=us_max_force(bases,mix,spots,True)
        cn,_=china_airborne(cn_tot,True,True)
        if best is None:
            print(f"  {lbl:<26} infeasible"); continue
        ab,N,tk,used=best
        print(f"  {lbl:<26} {N:5.0f} ac + {tk:3.0f} tkr  US {ab:6.1f}  "
              f"CN {cn:6.1f}  ratio {cn/ab:5.1f}:1")

    print("\n  Airframe leverage at Kyushu:")
    d=haversine((32.80,131.00),TANKER_ORBIT); d_pen=haversine(TANKER_ORBIT,STRAIT)
    for k,sp in [("F-35A",1.0),("F-15EX",1.0),("CCA",0.5)]:
        f,l,n,s=on_station(RADIUS[k],d,d_pen,TURN_US_H,True)
        print(f"    {k:<7} R={RADIUS[k]:4}nm loiter {l:.2f}h f={f:.3f} ramp {sp}")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    fns = {"geometry":sec_geometry, "onstation":sec_onstation,
           "engagement":sec_engagement, "basing":sec_basing, "y2030":sec_y2030}
    if which == "all":
        for f in fns.values():
            f(); print()
    elif which in fns:
        fns[which]()
    else:
        print(__doc__)
