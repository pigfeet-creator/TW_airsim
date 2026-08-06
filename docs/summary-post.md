**I modelled the air war over the Taiwan Strait. Result: the US tops out at ~72 fighters airborne over the Strait against China's 380 — a force ratio of 5.3:1 against. It can't be fixed by buying aircraft.**

 |US|China
---|---|---
Fighters committed|390 (+76 tankers)|750
Airborne over the Strait|**71.9**|**380.1**
**Force ratio**|**5.3 : 1 against**|

**The ceiling isn't airframes — it's ramp space, and tankers eat it.** Tanker demand scales with force size, and a KC-135 footprint is ~3 fighter spots, so the tankers required to make the fighters useful displace the fighters:

Fighters|Tankers needed|Ramp spots|Fits in 620?
---|---|---|---
250|48|393|yes
**390**|**76**|**619**|**at the limit**
450|89|717|no
620|126|999|no

390 + 76 is the self-consistent maximum. Send more airframes and there's nowhere to put them.

*That's a force ratio, not a kill ratio. The engagement model derives a Lanchester exponent of ~0.56, so LER ≈ force_ratio^0.56 — 5.3:1 implies ~1:2.5 in losses. Simulated runs give 1:2.3 to 1:4.0.*

---

**WHY THE US CAN'T GET MORE PRESENCE**

The controlling quantity is *f*, the fraction of a based force airborne over the target at any moment: `f = sorties/day × loiter hours ÷ 24`. Loiter is set by the **last refuelling point**, not the base — from the tanker orbit inward the fighter is on internal fuel.

So tanker standoff caps the mission:

Tanker line|F/A-18E|F-35C|F-35A|F-15E
---|---|---|---|---
200nm|1.24h|2.92h|2.43h|3.67h
300nm|0.62h|2.30h|1.80h|3.05h
400nm|**can't reach**|1.68h|1.18h|2.43h
600nm|can't reach|0.44h|can't reach|1.18h

And tankers can't come forward — a J-20 at ~1,100nm radius with PL-17 (~215nm) threatens them anywhere useful. Worse, **the Strait is 34nm from the Chinese mainland**, so standoff from the target and standoff from the threat are the *same number*. 351nm from the Strait is 344nm from the coast. There's no favourable geometry anywhere on the map.

Then every extra aircraft goes to a worse base:

Base|To tanker|f|Capacity
---|---|---|---
Kyushu|735nm|0.198|~120
W Honshu|856nm|0.186|~130
C Honshu|1,033nm|0.171|~140
Kanto|1,133nm|0.164|~60
Guam|1,270nm|0.154|~90
Misawa|1,412nm|0.146|~80

---

**EVERY OMISSION FAVOURS THE US**

- **Japanese bases treated as safe.** No missile attack, no cratering, no repair denial. Kyushu is 529nm from the Chinese coast, N Luzon 402nm — inside the envelope.
- **Free AEW for both sides.** In reality US AEW must orbit 200–300nm out to detect fighters, i.e. *forward* of the tanker line — exactly what PL-17 exists to kill. KJ-500s orbit over their own coast under SAM cover.
- **No tanker attrition. No mainland SAM coverage over the Strait. No Chinese production replacement** (240+ J-10/J-16/J-20 a year).
- **The US fights to annihilation** rather than withdrawing, so it kills more here than it would.
- **Capability parity** — no Chinese quality edge, despite 300–500 J-20s plus J-35A against a mostly Super Hornet force.

Taiwanese aircraft are gone in the opening phase, as well as Kadena. Allied JASDF fighters hit the *same* ceiling — the constraint is airframes in theatre, not US airframes: 200 of them need ~39 more tankers costing ~117 ramp spots against a system already at 619/620. They change the composition of the 390, not the total.

Chinese counts are DoD's China Military Power Report: ~1,900 fighters, 1,300+ fourth-gen or better. The 620-spot ramp total is my own estimate and it's the weakest number in the model — it sets the ceiling directly, so at 2 spots per tanker it rises to ~470 fighters and at 4 it falls to ~330.

Code and full report in the comments.
