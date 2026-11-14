---
tag: VGPKYE
kind: technique
slug: riser-design-modulus-method
name: Modulus method for riser design
aliases:
- Wlodawer modulus method
- riser sizing
area: cad/manufacturing-process-planning
level: core
summary: Sizes each riser so its modulus V/A exceeds that of the section it feeds by about 20 percent, so it freezes last and feeds the shrinkage.
prereqs: [chvorinov-rule]
see_also: [casting-hot-spot-detection, fixed-point-iteration, heat-equation, finite-element-method, medial-axis]
sources:
  - title: R. Wlodawer, Directional Solidification of Steel Castings, Pergamon Press, Oxford, 1966, translated by L. D. Hewitt and edited by R. V. Riley
    locator: the modulus of the casting sections, the feeder modulus about 1.2 times the modulus of the section it feeds, the modulus of the neck between them, and the check of the feed volume (general locator)
  - book: isbn:9780444635099
    title: John Campbell, Complete Casting Handbook, 2nd edition, Butterworth-Heinemann, 2015
    locator: the chapter on feeding and its feeding rules, among them the rule that the feeder modulus is at least about 1.2 times the casting modulus (general locator)
  - title: J. B. Caine, A theoretical approach to the problem of dimensioning risers, Transactions of the American Foundrymen's Society 56, 1948, 492 and following
    locator: the hyperbola that relates the freezing ratio of casting and riser to their volume ratio, with constants fitted to sound and unsound test castings
---

The modulus method sizes the risers of a casting, also called feeders: reservoirs of liquid metal that feed the casting while it shrinks during solidification. It uses [Chvorinov's rule](/chvorinov-rule/), which ranks the freezing times of sections by their modulus $M = V/A$, the volume over the cooling area. A riser must freeze after the section it feeds, so its modulus must be larger. Wlodawer made this a design method for steel castings, with a riser modulus of about 1.2 times the casting modulus. The factor 1.2 is a safety margin from foundry practice, not a result of the theory. The method also checks that the riser holds enough metal, and that the neck between riser and casting stays open long enough.

## In plain words

Metal takes up less room when it turns from liquid to solid. A casting that freezes in its mold therefore needs extra liquid metal to fill the space, or it gets holes inside. A riser is a thick lump of extra metal on top or on the side of the casting that stays liquid longer and flows in to fill the space.

For this to work, the riser must freeze after the casting. Thick, compact lumps freeze later than thin ones, and the modulus, the volume divided by the cooling surface, measures how thick a lump is. So the riser is made thicker than the casting, by about a fifth more modulus, and big enough to hold all the extra metal the casting needs.

## When it applies

- A sand or investment casting whose freezing order follows [Chvorinov's rule](/chvorinov-rule/), with the same metal and mold for the riser and the casting, so that the constants $B$ and $n$ of the rule are the same for both.
- A metal that shrinks when it freezes, such as steel, aluminium and copper alloys. Grey and ductile iron expand during part of their freezing, and the method needs changes for them.
- The casting can be split into feeding zones, each a group of sections that one riser feeds through a path of growing moduli.

## The template

**Why a larger modulus means a later freeze.** By [Chvorinov's rule](/chvorinov-rule/), the freezing time of a section is $t = B M^n$, with the same $B > 0$ and $n > 0$ for the riser and the casting, since they are the same metal in the same mold. The function $M \mapsto B M^n$ is strictly increasing for $M > 0$. So $M_r > M_c$ gives $t_r > t_c$: the riser is still partly liquid when the casting section is solid. With $M_r = 1.2\, M_c$ and $n = 2$, the riser takes $1.2^2 = 1.44$ times as long to freeze.

**Why a margin.** The rule gives $t_r > t_c$ for any $M_r > M_c$. The margin is there because the riser does not freeze like a separate lump of the rule. It loses metal into the casting, so its volume falls while the casting feeds. The face where it joins the casting is not a cooling face, but heat from the casting reaches the riser through it. The end of freezing in the casting must also come before the riser has frozen too far to flow. The rule itself is a fit, with the errors listed on its page. Wlodawer and Campbell give a riser modulus of about 1.2 times the casting modulus as a rule that works in practice. It is a safety factor from experience, and some foundries use other values.

```pseudo id=main
MODULUS-RISER(casting, β, ε, shape)
L1  split the casting into sections and compute each modulus M = V / A, leaving out of A the faces that join other sections
L2  group the sections into feeding zones, each with moduli that grow towards one riser position
L3  for each zone with the largest section modulus M_c
L4      choose the riser size so that M_r ≥ 1.2 · M_c for the riser shape, leaving the contact face out of its area
L5      recompute M_c with the contact face of the riser left out, and repeat L4 until the size does not change
L6      if a neck joins riser and casting, choose its modulus between M_c and M_r
L7      check the volume: ε · V_r ≥ β · V_zone; if not, enlarge the riser
L8      check the feeding distance from the riser over the zone; if too long, add a riser or a chill
L9  return the risers
```

The holes are the safety factor (1.2 here), the shrinkage $\beta$ of the metal, the fraction $\varepsilon$ of its volume that the riser can give before its own shrinkage cavity reaches the casting, which depends on the riser shape and on sleeves, and the feeding distance rules. All of them come from tables of foundry practice, not from the method.

**Line L4.** For a cylinder of diameter $D$ and height $H$ on top of the casting, with the base as the contact face, $V = \pi D^2 H / 4$ and $A = \pi D H + \pi D^2 / 4$. With $H = D$, $M_r = D / 5$. For a side riser of the same shape, where the contact through a neck is small, all faces cool, and $M_r = D / 6$. So the riser diameter follows from $M_r$ directly.

**Line L5.** The contact face of the riser no longer cools the casting, so the casting modulus grows with the riser size. This makes $D$ the solution of a fixed point equation, which the loop solves by [fixed-point iteration](/fixed-point-iteration/). The map is a contraction when the contact face is small against the cooling area of the casting.

**Line L6.** Wlodawer gives the moduli of casting, neck and riser in the proportion of about $1 : 1.1 : 1.2$, so that the neck freezes after the casting and before the riser. This is again a practice rule.

## Classic examples

**A top riser on a plate.** A steel plate of $300 \times 300 \times 50$ mm has $V = 4.5 \times 10^6$ mm$^3$ and, with all faces cooling, $A = 240{,}000$ mm$^2$, so $M_c = 18.75$ mm. A cylindrical top riser with $H = D$ has $M_r = D/5$, so $M_r = 1.2\, M_c$ needs $D = 6\, M_c$. The riser covers the area $\pi D^2 / 4$ of the top face, which no longer cools. The iteration of line L5 is

$$D_{k+1} = \frac{6V}{240{,}000 - \pi D_k^2 / 4},$$

and from $D_0 = 112.5$ mm it gives 117.36, 117.81, 117.85 and 117.86 mm. So $D = H = 117.9$ mm, with $M_c = 19.64$ mm and $M_r = 23.57$ mm.

The volume check of line L7 needs $\beta$ and $\varepsilon$. With $\beta = 0.03$ and $\varepsilon = 0.15$, values assumed here only to show the step, the riser holds $V_r = \pi D^3 / 4 = 1.29 \times 10^6$ mm$^3$ and can give $0.15 \times 1.29 \times 10^6 = 1.93 \times 10^5$ mm$^3$, and the plate needs $0.03 \times 4.5 \times 10^6 = 1.35 \times 10^5$ mm$^3$. So the modulus decides the size here, not the volume.

**A plate too large for one riser.** A long thin plate has a small modulus, so a riser by the modulus rule is small. The volume check may still pass, but the liquid cannot flow far through a thin plate before it freezes. Line L8 then splits the plate into zones, each with its own riser.

## Variations

- **Caine's method.** Caine (1948) relates the freezing ratio $X$ to the volume ratio $Y = V_r / V_c$ by a hyperbola
  $$X = \frac{a}{Y - b} + c,$$
  where $X$ is the ratio of the moduli, riser over casting, which Caine writes as the ratio of the surface to volume ratios of casting and riser. The constant $b$ is the shrinkage of the metal: no riser smaller than the shrinkage can feed. The constant $c$ is the relative freezing rate of riser and casting, the smallest freezing ratio that can work with a very large riser. The constant $a$ is fitted from test castings. A riser is expected to be sound when the point $(Y, X)$ lies above the curve. For steel, the values $a = 0.10$, $b = 0.03$ and $c = 1.0$ are quoted in teaching notes. They have not been checked against Caine's paper here.

  For the plate above, the riser of the modulus method has $X = 1.20$ and $Y = 0.286$, but the curve with these constants asks for $X \ge 0.10 / (0.286 - 0.03) + 1 = 1.39$. So Caine's curve asks for a larger riser. Solving for the riser with $(Y, X)$ on the curve gives $D = 128.3$ mm, with $X = 1.30$ and $Y = 0.369$. The two methods are fits of different data with different safety margins, and they need not agree.
- **Shape factor methods.** Other methods replace the modulus by a shape factor of the casting, such as the sum of length and width over thickness, and read the riser volume from a curve. They need less computation and fit the castings they were measured on.
- **Sleeves and exothermic material.** An insulating or exothermic sleeve slows the cooling of the riser. Its effect is given as a factor on the riser modulus, so a smaller riser has the same apparent modulus.
- **Simulation.** A thermal simulation by the [finite element method](/finite-element-method/), solving the [heat equation](/heat-equation/) with latent heat, shows the last regions to freeze directly. A modulus design is then a start point that the simulation checks.
- **Geometric hot spots.** The largest section modulus can be replaced by the points that freeze last, found with [hot spot detection](/casting-hot-spot-detection/), which uses the distance to the mold, a function closely related to the [medial axis](/medial-axis/) of the casting.

## Pitfalls

- **Leaving the contact face in.** Counting the joint between riser and casting as a cooling face of the casting gives a casting modulus that is too small, and a riser that is too small. The example above shows the change, from 18.75 to 19.64 mm.
- **The wrong section.** The riser must be sized for the largest modulus in its zone, not for the modulus of the whole casting, and the path from that section to the riser must have growing moduli.
- **A neck that freezes first.** A neck with a smaller modulus than the casting cuts the riser off before the casting is solid. The riser is then useless, however large it is.
- **Expanding metals.** Grey and ductile iron expand during part of their freezing, so the modulus rule overestimates the riser for them unless the method is changed.
- **Treating 1.2 as exact.** The factor is a margin from practice. A design that needs it to be exact, for example one that fails at 1.15, has no margin left.

## References
