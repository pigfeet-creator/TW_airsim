# Air Campaign Over the Taiwan Strait — Modelling Report

Open-source parametric model of air-to-air attrition over the Strait, assuming the US elects to force a decisive air engagement rather than fight a protracted one.

**In scope:** fighter presence and attrition over the Strait; fuel and tanker geometry; basing capacity; sortie generation.

**Out of scope, and each omitted mechanism favours the US:** mainland SAM coverage reaching over the Strait, attrition of AEW and tankers, ballistic and cruise missile attack on the basing itself, and Chinese production replacement during the campaign. The model also assumes the US fights to annihilation; a real commander withdraws at some attrition threshold, having killed proportionally fewer.

**Two things that look like pro-China omissions but are not.** Taiwanese aircraft are out of action in the opening phase and are not a factor in the decisive engagement modelled here. Allied JASDF aircraft are subject to the identical ceiling — the constraint derived in B1 is on airframes in theatre rather than on US airframes, since allied fighters fly the same distances with the same tanker dependence. Two hundred of them would require roughly 37 additional tankers costing ~111 ramp spots, against a system already saturated at 607 of 620. Allied participation changes the composition of the 390, not the total.

**The pro-China assumptions are confined to two estimated parameters:** the maintenance ceiling of 4 sorties per aircraft per day, which likely overstates Chinese sortie generation, and the 900–1,100 in-range figure, which is an estimated theatre allocation.

**Two different ratios appear throughout, and they are not the same number:**

- **Force ratio** (e.g. "4.3:1") — Chinese aircraft airborne over the Strait divided by US aircraft airborne over the Strait, at any given moment. This is the primary output of the model.
- **Loss exchange ratio, LER** (e.g. "1:2.9") — US aircraft lost per Chinese aircraft lost. Derived from the engagement model, not from the force ratio directly.

They are linked by the empirical exponent α ≈ 0.557 derived in D1: **LER ≈ force_ratio^0.557**. A 4.3:1 force ratio therefore implies roughly a 1:2.2 loss exchange. A force ratio is always the larger, more dramatic-looking number — do not read it as losses.

Every table reporting a force ratio also reports the implied LER. These implied figures are *converted* from the force ratio using α, not independently simulated. The directly-modelled LERs from the engagement runs appear in D1 and range 1:2.3 to 1:4.0, which brackets the converted values.

**Configuration labels** are given for each finding, because several were established under earlier parameter sets and are directional rather than final.

---

## Headline result

**At capability parity, the US cannot generate competitive airborne presence over the Strait. The shortfall is structural — geometry, basing and fuel — not qualitative.**

*Final configuration: land-based US airpower only, Chinese tanking modelled, 24h crew rotation both sides, basing capacity and tanker ramp competition enforced.*

| | US | China |
|---|---|---|
| Committed / based | 390 fighters + 72 tankers | 750 fighters |
| Ramp spots used | 607 of 620 available | not binding |
| Airborne over the Strait | **88.6** | **380.1** |
| **Force ratio (airborne)** | | **4.3 : 1 against** |
| Implied loss exchange | | ~1 : 2.2 |

The build-up to that figure, showing what each correction contributed:

| Configuration | US airborne | China airborne | Force ratio | Implied LER |
|---|---|---|---|---|
| 620 based, no Chinese tanking, no crew rotation | 82.9 | 167.2 | 2.0 : 1 | 1 : 1.5 |
| + Chinese tanking | 82.9 | 267.2 | 3.2 : 1 | 1 : 1.9 |
| + 24h crew rotation, both sides | 132.6 | 380.1 | 2.9 : 1 | 1 : 1.8 |
| **+ basing capacity and tanker ramp competition** | **88.6** | **380.1** | **4.3 : 1** | **1 : 2.3** |

The first three rows assume 620 fighters can be based forward with tankers occupying no ramp space. They cannot. Enforcing capacity gives a self-consistent ceiling of 390 fighters plus the 72 tankers required to fly them — beyond which additional fighters displace the tankers that make them useful.

**Attrition consequence.** Across engagement runs the US committed force was annihilated under every parameter set tested, at loss-exchange ratios of 1:2.3 to 1:4.0 against, with China retaining 56–94% of its in-range fleet depending on force size and Pk. The exchange ratio proved insensitive to absolute force size — it is set by the on-station ratio and by Pk.

---

## Force structure derivation

The airframe counts drive everything downstream, so each is set out here with its basis. **Sourced** figures come from published assessments; **estimated** figures are my inference and are the weaker half of the model.

### China

| Quantity | Value | Basis |
|---|---|---|
| Total fighters | ~1,900 | **Sourced** — DoD China Military Power Report 2024, drawing on classified intelligence: ~3,150 total active aircraft excluding trainers and UAVs, ~2,400 combat aircraft, of which roughly 1,900 fighters. |
| 4th-generation or better | **1,300+** | **Sourced** — same report. Includes J-10, J-11, J-16 variants; J-7/J-8 being phased out. |
| Annual production | 240+ | **Sourced** — combined J-10/J-16/J-20 output. Other assessments put AVIC capacity at 300–400 4th/5th-gen annually and ~250/yr to the PLAAF by 2027. |
| J-20 fleet | 300 (mid-2025), possibly ~500 (mid-2026) | **Sourced** — analyst estimates from unit dispositions across 14 frontline units plus test/training bases. |
| Tanker fleet | 16 Y-20U (2024), ~40 assumed 2026 | Partly sourced; the 2026 figure is interpolated. |
| **Bringable within range** | **900–1,100 (central 1,000)** | **ESTIMATED.** CSIS notes a large share of PLA air assets is concentrated in the Eastern and Southern Theater Commands, and internal lines permit reinforcement from other commands. 70–85% of the modern fleet is defensible but is an inference, not a published figure. |
| Readiness | 75% | **ESTIMATED.** Standard planning assumption, not China-specific data. |
| **Committed to the air battle** | **750** | Derived: 1,000 × 0.75. |
| 2030 modern fleet | ~2,300 | **Projected** from production rates plus RUSI's estimate of ~1,000 J-20 and ~900 J-16 by 2030. In-range × readiness → ~1,400. |

Note the 2023 reorganisation transferred roughly 300 shore-based fixed-wing combat aircraft from PLAN aviation to the PLAAF, so PLAAF and PLANAF counts should not be added naively.

### United States

| Quantity | Value | Basis |
|---|---|---|
| Carrier air wing | ~44 strike fighters (34 Super Hornet, 10 F-35C) | **Sourced** — typical wing composition; F-35C transition incomplete across wings. |
| Carriers available | 8 of 11; 4 deployed mid-2026 | **Sourced** — three simultaneously unavailable in 2026 (Ford fire repair, Truman entering RCOH, Stennis in maintenance). Fleet Response Plan doctrine claims 6 surge-capable within 30 days, but readiness has run near 50%. |
| Fighter combat radii | 400nm F/A-18E, 620 F-35C, 670 F-35A, 790 F-15E/EX | **Sourced**, though published figures vary by profile and loadout. |
| **Total forward ramp capacity** | **620 fighter spots** | **ESTIMATED — the weakest number in the model.** Sum of the band estimates below. |
| Kyushu | 120 | **ESTIMATED.** Tsuiki, Nyutabaru, Ashiya, Kanoya plus civil fields — roughly 5 squadrons' worth of US aircraft *on top of* resident JASDF. |
| W Honshu | 130 | **ESTIMATED.** Iwakuni, Komatsu, Hofu, Miho. |
| C Honshu | 140 | **ESTIMATED.** Hamamatsu, Gifu, Komaki, Atsugi. |
| Kanto | 60 | **ESTIMATED.** Yokota, Hyakuri. |
| Guam | 90 | **ESTIMATED.** Andersen. |
| Misawa | 80 | **ESTIMATED.** |
| Philippines (2030 case) | 200 | **ESTIMATED.** EDCA sites, N and C Luzon. |
| Tanker ramp cost | 3 fighter spots each | **ESTIMATED.** Sets the force ceiling directly — see soft parameters. |

**What this means for confidence.** The Chinese airframe counts rest on published DoD assessment; the theatre allocation does not. The US ramp capacities are entirely my estimates, and since they set the force ceiling, they are where the headline figure is most exposed. A reader who rejects the 620-spot total should recompute rather than adjust — the ceiling is `620 = fighters + 3 × tankers`, with tankers scaling from sortie count.

---

## The controlling mechanism: on-station fraction

Sortie counts are the wrong metric. What matters is **f**, the fraction of a based force airborne over the target area at any moment. It is the product of:

- **loiter per sortie** — unrefuelled radius minus the distance from the last refuelling point to the target
- **sorties per day** — sortie duration, turnaround, and either crew hours or the maintenance ceiling

*Final config, F-35A, tanker orbit 324nm from the Strait, 24h crew rotation:*

| Base | To tanker | Sortie | Sorties/day | f |
|---|---|---|---|---|
| Kyushu | 735nm | 6.86h | 2.71 | 0.243 |
| W Honshu | 856nm | 7.40h | 2.55 | 0.229 |
| C Honshu | 1,033nm | 8.19h | 2.36 | 0.212 |
| Kanto | 1,133nm | 8.63h | 2.26 | 0.203 |
| Guam | 1,270nm | 9.24h | 2.14 | 0.192 |
| Misawa | 1,412nm | 9.87h | 2.02 | 0.182 |

Chinese equivalents run **0.44–0.53** — roughly double the best US figure, from bases 90–540nm from the Strait with tankers orbiting over their own territory.

---

# A. Geometry and fuel

## A1. The tanker line caps the mission *(final config)*

US fighters cannot loiter over the Strait on internal fuel from any survivable base, so tanking is mandatory. But from the last top-off inward the fighter is on internal fuel, which means **the tanker orbit position, not the base, sets the loiter budget.**

| Tanker line from Strait | F/A-18E | F-35C | F-35A | F-15E |
|---|---|---|---|---|
| 200nm | 1.24h | 2.61h | 2.92h | 3.67h |
| 300nm | 0.62h | 1.99h | 2.30h | 2.96h |
| 400nm | **cannot reach** | 1.37h | 1.68h | 2.43h |
| 500nm | cannot reach | 0.75h | 1.06h | 1.86h |
| 600nm+ | cannot reach | 0.12h | 0.44h | 1.18h |

**There is no safe line.** A J-20 at ~1,100nm combat radius carrying PL-17 at ~215nm can threaten a tanker essentially anywhere it could usefully orbit. The line cannot be chosen for safety, only for whether the mission is possible.

## A2. The Strait is 34nm from the Chinese mainland

Standoff from the target and standoff from the threat are the **same quantity**:

| Tanker distance from Strait | Distance from mainland |
|---|---|
| 301nm | 295nm |
| 351nm | 344nm |
| 475nm | 468nm |
| 649nm | 641nm |

No orbit geometry is close to the target and far from the threat. Every mile of tanker safety is a mile of lost loiter, with no favourable trade available anywhere on the map. This is a fact about the coastline rather than a modelling output, and it does not depend on any soft parameter.

## A3. The route is a dogleg, and it costs offload rather than time

Constrained to 350nm from the coast, the optimal tanker orbit sits southeast of Taiwan near (22.0N, 124.5E). From Kyushu the path is two near-perpendicular legs:

- Kyushu → tanker: 782nm, bearing 208°
- tanker → Strait: 324nm, bearing 299°
- turn at the tanker: **90.7°**
- total 1,106nm against 825nm direct — **+34%**

This does not reduce on-station time, because sortie rate is capped by maintenance or crew before cycle time binds. It raises offload demand by roughly **23%**, so the tanker fleet must grow proportionally — which is what makes A3 feed directly into B1.

---

# B. Basing

## B1. Capacity binds before force size does — and tankers eat the ramp *(final config)*

| Base | f | Capacity | Cumulative aircraft | Cumulative airborne |
|---|---|---|---|---|
| Kyushu | 0.243 | 120 | 120 | 29.2 |
| W Honshu | 0.229 | 130 | 250 | 59.0 |
| C Honshu | 0.212 | 140 | 390 | 88.6 |
| Kanto | 0.203 | 60 | 450 | 100.8 |
| Guam | 0.192 | 90 | 540 | 118.0 |
| Misawa | 0.182 | 80 | 620 | 132.6 |

Each additional aircraft goes to a worse base, so marginal presence falls as the force grows. Tanker requirement scales with the force, and a KC-135 footprint is roughly 3 fighter spots:

| Fighters | Tankers required | Ramp spots | Feasible |
|---|---|---|---|
| 250 | 45 | 385 | yes |
| **390** | **72** | **607** | **at the limit** |
| 450 | 84 | 702 | no |
| 620 | 120 | 980 | no |

| Tankers based forward | Spots displaced | Fighters that fit | Airborne | Force ratio | Implied LER |
|---|---|---|---|---|---|
| 0 | 0 | 620 | 132.6 | 2.9 : 1 | 1 : 1.8 |
| 60 | 180 | 440 | 98.7 | 3.8 : 1 | 1 : 2.1 |
| 100 | 300 | 320 | 73.8 | 5.2 : 1 | 1 : 2.5 |
| 140 | 420 | 200 | 47.5 | 8.0 : 1 | 1 : 3.2 |
| 180 | 540 | 80 | 19.5 | 19.5 : 1 | 1 : 5.2 |

**The tanker fleet needed to make the fighters useful displaces the fighters it exists to support.** The system saturates at ~390 fighters regardless of how many airframes the US could otherwise deploy. Sending more does not help; there is nowhere to put them.

---

# C. Force employment

## C1. The escort barrier cannot be separated from the melee *(earlier config — directional)*

To protect tankers you must kill the J-20 *before* PL-17 launch, so the barrier sits ~275nm forward of the tanker orbit. At tanker lines under 350nm the barrier lands inside the contested zone — not a barrier, just more fighters in the main engagement.

Two constructs, compared under the pre-capacity configuration:

| Construct | Escort tax | Airborne over Strait | Force ratio | Implied LER |
|---|---|---|---|---|
| Dedicated escort, 475nm line | 110 airframes | 23.7 | 6.4 : 1 | 1 : 2.8 |
| Main mass as screen, 350nm line | none | 63.5 | 2.4 : 1 | 1 : 1.6 |

Mass-as-screen is unambiguously better. Paying for a separate barrier *and* standing the tankers off was strictly worse on both terms. The final configuration uses mass-as-screen.

## C2. Crew rotation is the only variable favouring the US *(pre-capacity config)*

24h crew rotation lifts US airborne presence **+60%** against China's **+42%**, improving that configuration's ratio from 3.22:1 to 2.87:1. The reason is structural rather than incidental: long US sorties were crew-hour-limited, while short Chinese sorties were already near the maintenance ceiling with less headroom to unlock. Distance is what created the US headroom in the first place.

## C3. Chinese J-20 allocation is nearly free *(pre-capacity config)*

Withholding a quarter of the J-20 fleet for tanker-busting versus committing everything changes Chinese losses by 1–18 aircraft and retention by 1–3 points. The threat that forces the US tanker line back therefore **costs China almost nothing in the CAP fight** — the posture pays for itself through the geometry it imposes, not through kills. A tanker-busting force that never fires still sets the US loiter budget.

---

# D. Attrition and quality

## D1. Quality cannot close the gap *(engagement model, 400 v 975)*

Square-law breakeven requires the outnumbered side's per-airframe effectiveness to exceed the **square** of the numerical deficit — 9× at 3:1, 16× at 4:1.

Mechanistic engagement modelling (identical aircraft, finite magazines, simultaneous fire, target assignment, 6,000 Monte Carlo trials) yields an empirical exponent of **α ≈ 0.56**, roughly midway between the linear and square laws. That is much gentler than square law, and still:

| US quality edge | China retains | LER |
|---|---|---|
| parity | 88% | 1 : 3.5 |
| 1.2× | 86% | 1 : 2.9 |
| 1.5× | 82% | 1 : 2.3 |
| 2.0× | 76% | 1 : 1.7 |

The US committed force is annihilated in every case. Plausible actual US quality across a mixed force — largely Super Hornets and 4.5-gen types, against a Chinese fleet fielding 300–500 J-20s plus the J-35A — is **1.0–1.2×**.

## D2. Model behaviour

- **Pk is the dominant unknown**, and higher lethality *helps* the outnumbered side — everyone dies before numbers accumulate advantage. At Pk 0.15 China retains 83%; at 0.40, 67%.
- **Magazine depth is irrelevant above 4 BVR rounds.** The fight resolves before anyone runs dry.
- **Targeting coordination and first-shot advantage are negligible** at these ratios (0.37 vs 0.38, and 0.37 vs 0.39 respectively).
- **The exchange ratio is insensitive to absolute force size** — 3.55 to 3.87 across the full plausible range.
- **China's absolute losses fall as it commits more** (132 at 600 committed, 108 at 1,300). No restraint incentive exists at any point.
- **Attrition has no plateau.** The last 10% of the US force dies at roughly 10× the rate of the first 10%.

---

# E. 2030 projection

Same model, projected force structures. Vulnerability of the basing is still excluded — though note that on distance alone Kyushu (529nm from the nearest Chinese coast), Central Luzon (548nm) and Northern Luzon (402nm) sit in the same exposure band, so opening the Philippines buys capacity without buying survivability.

**Force projections.** China: modern fleet ~1,300 → ~2,300, driven by AVIC capacity of 300–400 fourth- and fifth-generation fighters annually, with RUSI projecting roughly 1,000 J-20s and 900 J-16s in service by 2030 plus the J-35A entering the force. In-range × readiness therefore goes 750 → ~1,400, and Chinese airborne presence **380 → 710**. Tanker fleet ~40 → ~120, so the 84nm penetration leg is sustainable at scale. US: ramp capacity unchanged at 620 spots absent new access; mix shifts to F-35A, F-15EX and CCA.

| Scenario | Max sustainable | US airborne | China airborne | Force ratio | Implied LER |
|---|---|---|---|---|---|
| 2026 baseline | 390 + 72 tankers | 88.6 | 380 | 4.3 : 1 | 1 : 2.3 |
| 2030, same mix and basing | 390 + 72 | 88.6 | 710 | **8.0 : 1** | **1 : 3.2** |
| 2030, F-35A/F-15EX/CCA mix | 430 + 78 | 104.4 | 710 | 6.8 : 1 | 1 : 2.9 |
| 2030 + Philippine access | 570 + 106 | 134.2 | 710 | 5.3 : 1 | 1 : 2.5 |
| 2030 + Philippines + 30% more ramp | 740 + 139 | 172.1 | 710 | 4.1 : 1 | 1 : 2.2 |

**No modelled US measure recovers the 2026 position.** The best case — opening Philippine basing *and* expanding ramp capacity by 30% — returns the ratio to 4.1:1, which is roughly where it stood in 2026, four years later and against a doubled adversary force.

**Airframe leverage at Kyushu, 2030 mix:**

| Type | Radius | Loiter | Sorties/day | f | Ramp cost |
|---|---|---|---|---|---|
| F-35A | 670nm | 2.15h | 2.71 | 0.243 | 1.0 spot |
| F-15EX | 790nm | 2.90h | 2.50 | 0.302 | 1.0 spot |
| CCA | 700nm | 2.34h | 2.65 | 0.259 | 0.5 spot |

**F-15EX is the strongest single airframe lever** — 25% more on-station time per aircraft than the F-35A, purely from radius. **CCA's contribution is ramp footprint rather than loiter**: at half a spot it fits more airframes onto fixed concrete, which is precisely the binding constraint identified in B1. That is a stronger argument for CCA in this scenario than the usual cost-per-airframe case.

**The structural asymmetry.** Chinese growth is a production problem solved on existing lines. The US response is a real-estate problem: presence cannot be added without new concrete, and the concrete is in allied territory inside the missile envelope. Two of the three US improvements modelled — Philippine access and ramp expansion — have lead times measured in years and depend on host-nation politics rather than procurement.

*Additional soft parameters in this section:* CCA radius (700nm) and ramp footprint (0.5 spot) are estimates, as is Philippine capacity (200 spots).

---

## What would change the answer

Ranked by leverage:

1. **Kadena surviving.** At 472nm from the Strait against 825nm from Kyushu, Okinawa is the only basing that makes the fuel geometry tractable. Its loss changes the arithmetic category rather than degrading it.
2. **A tanker line inside 300nm holding.** Worth more than any quantity of additional tankers — Super Hornet loiter roughly doubles. Requires the J-20/PL-17 threat to be manageable, which is the load-bearing assumption of the whole analysis.
3. **Ramp capacity in Japan.** The force ceiling is a concrete-and-fuel problem. Dispersal to civilian fields raises capacity only if munitions, fuel and maintenance follow.
4. **Longer-ranged US fighters.** The F-15E at 790nm radius is the only type retaining useful loiter past a 400nm tanker line.
5. **Chinese maintenance limits.** The 4 sorties/day ceiling is what prevents the Chinese figures running away entirely.

---

## Soft parameters, ranked by influence

1. **The 3:1 tanker-to-fighter ramp displacement ratio.** Load-bearing for the headline: at 2:1 the ceiling rises to ~470 fighters, at 4:1 it falls to ~330. My estimate, not sourced.
2. **Maintenance ceiling of 4 sorties/aircraft/day.** The J-16 figures under rotation imply ~15 flight hours per airframe per day, above sustained real-world rates — so Chinese f may be overstated.
3. **Chinese modern fighters in range (900–1,100 assumed).** Estimated. Drives retention percentage; barely affects the exchange ratio.
4. **Pk = 0.25 baseline.** Swings retention by ±10 points.
5. **Fuel burn of 10 lb/nm.** Sets tanker demand, hence the ramp ceiling; ±30% moves it proportionally.
6. **LO detection range of 40nm** (hence 80nm frontage). Sets the escort bill in C1; unpublished figure, and the requirement scales inversely.
7. **Base capacities** (120 Kyushu, 130 W Honshu, and so on). Estimates.

---

## Corrections made during the run

- Sortie arithmetic initially overstated the US disadvantage at 5–10:1; correcting against design and historical rates gave 3–4:1.
- On-station fractions were first guessed at 25%/37%; derived from cycle times they are 13.7%/26.6%.
- Tanking was modelled as a simple range extender for the US and omitted entirely for China. Both wrong; correcting the second roughly doubled Chinese airborne presence.
- Tanker attrition mechanics were introduced with invented parameters and then removed. Results did not depend on them.
- "Total transit is fixed regardless of tanker position" was wrong — it holds only when the tanker sits on the direct route, which the coast-standoff constraint prevents.
- US carrier surge of 6–7 CVNs was too generous: 8 of 11 are available and 4 were deployed as of mid-2026.
- Kadena and mainland Japan aircraft were double-counted in early runs while simultaneously being treated as cratered.
- The J-20/PL-17 pairing was described as a single airframe; the PL-17 is too long for the J-20's bay and flies externally on the J-16, making the shot cooperative.
- The headline initially reported 2.9:1 from an unconstrained 620-fighter force. Enforcing capacity and tanker ramp competition gives 4.3:1.
