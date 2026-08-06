# Taiwan Strait Air Campaign Model

A parametric model of air-to-air attrition over the Taiwan Strait, built from
open sources. The question it answers: **if the US elects to force a decisive
air engagement over the Strait, what airborne presence can it actually
generate, and what does the exchange look like?**

## Headline result

**2026, capacity-constrained: 390 fighters + 76 tankers filling 619 of 620
available ramp spots. US 71.9 aircraft airborne over the Strait against
China's 380.1 — a force ratio of 5.3:1 against, implying roughly 1:2.5 in
losses.**

The binding constraints are geometry and ramp space, not aircraft quality.
Across every configuration tested — 2026 and 2030, carriers in and out, escort
constructs both ways, crew rotation on and off, Chinese tanking on and off,
tanker lines 250–475nm, force sizes 176–764, quality parity through 2× — the
force ratio never fell below 1.3:1 and the US committed force was annihilated
in every engagement run.

## Why

Three findings drive it:

1. **There is no safe tanker line.** A J-20 at ~1,100nm combat radius carrying
   PL-17 (~215nm) threatens a tanker anywhere it could usefully orbit. And
   loiter over the target is set by the *last refuelling point*, not the base —
   from the tanker orbit inward the fighter is on internal fuel.
2. **The Strait is 34nm from the Chinese mainland.** Standoff from the target
   and standoff from the threat are the same quantity. There is no orbit
   geometry that is close to the target and far from the threat.
3. **Ramp space binds before force size does, and tankers eat the ramp.** A
   KC-135 footprint is ~3 fighter spots, and tanker demand scales with force
   size, so the tankers required to make the fighters useful displace the
   fighters they support. The system saturates at ~390 airframes.

## Layout

```
src/taiwan_air_model.py   consolidated model, reproduces every reported figure
docs/report.md            full write-up with all findings and sensitivities
docs/summary-post.md      short public summary
```

## Running

```bash
pip install -r requirements.txt
python3 src/taiwan_air_model.py            # everything
python3 src/taiwan_air_model.py geometry    # coastline, tanker line, dogleg, exposure
python3 src/taiwan_air_model.py onstation   # on-station fractions by base and type
python3 src/taiwan_air_model.py engagement  # BVR model, empirical Lanchester exponent
python3 src/taiwan_air_model.py basing      # ramp ceiling, tanker displacement
python3 src/taiwan_air_model.py y2030       # 2030 projection
```

Requires numpy only.

## Model logic

The controlling quantity is `f`, the fraction of a based force airborne over
the target area at any moment:

```
f = sorties_per_day × loiter_hours_per_sortie / 24

loiter = 2 × (combat_radius − tanker_to_target) / cruise × LOITER_EFF
```

Attrition uses a mechanistic BVR engagement model — finite magazines,
simultaneous fire, explicit target assignment, Monte Carlo — rather than
assuming a Lanchester exponent. The exponent that *emerges* is **α ≈ 0.557**,
midway between the linear and square laws. Force ratios convert to loss
exchange ratios as `LER ≈ force_ratio^0.557`.

## Two different ratios

- **Force ratio** — Chinese aircraft airborne over the Strait ÷ US aircraft
  airborne, at any moment. Primary model output.
- **Loss exchange ratio (LER)** — US aircraft lost per Chinese aircraft lost.

A force ratio is always the larger, more dramatic-looking figure. Do not read
it as losses.

## Assumptions and omissions — all favour the US

- **Japanese and Philippine bases treated as safe.** No missile attack, no
  cratering, no repair denial. Kyushu is 529nm from the Chinese coast, Central
  Luzon 548nm, Northern Luzon 402nm — all inside the MRBM/cruise envelope.
- **Full AEW coverage for both sides, free.** In reality US AEW must orbit
  200–300nm from the Strait to detect fighter-sized targets, i.e. *forward* of
  the tanker line — exactly what PL-17 exists to kill. Chinese KJ-500s orbit
  over their own coast under SAM cover.
- **No tanker attrition.**
- **No mainland SAM coverage over the Strait.** HQ-9B and successors reach over
  the water at no sortie cost. Excluded entirely.
- **No Chinese production replacement** during the campaign.
- **The US fights to annihilation** rather than withdrawing at an attrition
  threshold.
- **Capability parity assumed**, despite 300–500 J-20s plus J-35A against a
  mostly Super Hornet and 4.5-gen US force.

**Two things that look like pro-China omissions but aren't.** Taiwanese
aircraft are out of action in the opening phase. Allied JASDF aircraft hit the
*same* ceiling — the constraint is on airframes in theatre, not US airframes.
200 Japanese fighters need ~39 more tankers costing ~117 ramp spots against a
system already at 619/620. Allied participation changes the composition of the
390, not the total.

## Where the airframe numbers come from

**China — sourced.** DoD China Military Power Report 2024: ~1,900 fighters of which
**over 1,300 are fourth-generation or better** (J-10, J-11, J-16 variants), out of
~2,400 combat aircraft and ~3,150 total excluding trainers and UAVs. Combined
J-10/J-16/J-20 production exceeds 240 units a year. J-20 fleet estimated at 300 by
mid-2025. Note the 2023 reorganisation moved ~300 shore-based fixed-wing combat
aircraft from PLAN aviation to the PLAAF, so service counts should not be added
naively.

**China — estimated by me.** That 900–1,100 of the 1,300 can be brought within
range of the Strait (CSIS notes a large share of PLA air assets sits in the Eastern
and Southern Theater Commands, and internal lines permit reinforcement from
others — but 70–85% is an inference, not a published figure), and 75% readiness as
a generic planning assumption. Committed force = 1,000 × 0.75 = **750**.

**US — sourced.** Carrier air wing ~44 strike fighters (34 Super Hornet, 10 F-35C).
8 of 11 carriers available with 4 deployed mid-2026. Combat radii, each type in
its typical air-to-air CAP fit (stealth types internal fuel, F/A-18E with 2
external tanks, F-15E/EX with CFTs): 400nm F/A-18E, 670 F-35C, 590 F-35A,
790 F-15E/EX.

**US — estimated by me, and this is the weakest part of the model.** The 620-spot
forward ramp total is the sum of my band estimates: Kyushu 120, W Honshu 130,
C Honshu 140, Kanto 60, Guam 90, Misawa 80, plus 200 for Philippine EDCA sites in
the 2030 case. Since ramp space sets the force ceiling, this is where the headline
figure is most exposed. The ceiling is `620 = fighters + 3 × tankers`, with tankers
scaling from sortie count — recompute rather than adjust if you reject the total.

Full derivation with per-item basis in `docs/report.md`.

## Parameters to challenge

Ranked by influence. These are the pro-China assumptions and the place to
attack the model:

| Parameter | Value | Why it matters |
|---|---|---|
| `TANKER_SPOTS` | 3.0 | Fighter ramp spots per tanker. Sets the force ceiling directly. At 2.0 the ceiling rises to ~470 fighters; at 4.0 it falls to ~330. |
| `MAINT_CEIL` | 4.0 | Sorties/aircraft/day. Probably overstates Chinese sortie generation — implies ~15 flight hours/airframe/day for the J-16 under crew rotation. |
| China in-range | 750 (2026) | Estimated theatre allocation, not sourced. Drives retention %; barely affects the exchange ratio. |
| `pk` | 0.25 | Swings retention ±10 points. Note higher lethality *helps* the outnumbered side. |
| `FUEL_BURN` | 10.0 lb/nm | Sets tanker demand, hence the ramp ceiling. |
| Base capacities | 120 Kyushu, etc. | Estimates. |

## Licence

MIT.
