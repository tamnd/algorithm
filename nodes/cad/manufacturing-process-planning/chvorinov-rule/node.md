---
tag: P8JFDM
kind: model
slug: chvorinov-rule
name: Chvorinov's rule
aliases:
- Chvorinov's law
area: cad/manufacturing-process-planning
level: intro
summary: The solidification time of a casting section is proportional to (V/A)^n with n about 2, so sections are ranked by their modulus V/A in feeding design.
prereqs: [heat-equation]
see_also: [riser-design-modulus-method, casting-hot-spot-detection, taylor-tool-life-equation, finite-difference-method, finite-element-method, distance-transform]
sources:
  - paper: "N. Chvorinov, Theorie der Erstarrung von Gussstücken, Die Giesserei 27, 1940, 177 to 186, 201 to 208 and 222 to 225"
    locator: the solidification time of a casting in a sand mold as a function of the ratio of its volume to its cooling surface, from heat conduction into the mold
  - book: isbn:9780133128741
    title: Serope Kalpakjian and Steven R. Schmid, Manufacturing Engineering and Technology, 7th edition, Pearson, 2014
    locator: the chapter on the fundamentals of metal casting, the solidification time t = C (V/A)^n with n between 1.5 and 2 and usually taken as 2 (general locator)
  - title: Merton C. Flemings, Solidification Processing, McGraw-Hill, 1974
    locator: the solidification of a pure metal against a semi-infinite insulating mold, with the heat flux that falls as one over the square root of time, and the correction for a curved surface (general locator)
  - book: isbn:9780444635099
    title: John Campbell, Complete Casting Handbook, 2nd edition, Butterworth-Heinemann, 2015
    locator: the chapter on feeding, the modulus V/A as the measure of the freezing time of a section in feeding design (general locator)
---

Chvorinov's rule says that the time $t$ for a casting, or a section of a casting, to solidify in its mold is

$$t = B \left(\frac{V}{A}\right)^{n},$$

where $V$ is the volume of the casting, $A$ is the area of its surface that gives heat to the mold, $B$ is a constant for the metal, the mold and the pouring temperature, and $n$ is close to 2. The ratio $M = V/A$, a length, is the *modulus* of the casting. N. Chvorinov published the rule in 1940 from the theory of heat conduction into a sand mold. Its main use is to rank the sections of a casting by the order in which they freeze, which is the base of [riser design by the modulus method](/riser-design-modulus-method/) and of [hot spot detection](/casting-hot-spot-detection/).

## The machine

### The law

**Variables.** $t$ is the time from the end of pouring to the end of solidification. $V$ and $A$ are the volume and the cooling area of the section. A face where the section joins another section of the same casting gives no heat to the mold, so it is not counted in $A$. A face against a core counts as a cooling face.

**Form.** The rule says that two sections with the same modulus freeze in the same time, whatever their shape, and that a section with twice the modulus takes about four times as long. On a log-log plot of $t$ against $M$, the measured points lie near a line of slope $n$.

**Constants.** Kalpakjian and Schmid give $n$ between 1.5 and 2 and say that it is usually taken as 2. The constant $B$ depends on the metal (its density, its latent heat and its freezing temperature), on the mold material (its ability to absorb heat) and on the superheat. A foundry fits $B$ from a test casting of its own metal and mold. The model below gives a formula for $B$, and also explains why $n$ can be less than 2.

### Where the square comes from

Take the simplest case: a pure metal poured at its melting temperature $T_m$, with no superheat, into a sand mold at the temperature $T_0$. Sand conducts heat much less well than the metal, so all the resistance to the flow of heat is in the mold. The metal side of the interface stays at $T_m$ while metal is still liquid, and there is no resistance at the interface.

**The mold is a semi-infinite solid.** Near the interface, the heat flows into the mold in one direction $x$, normal to the surface. The temperature in the mold obeys the one-dimensional [heat equation](/heat-equation/) $\partial T / \partial t = \alpha\, \partial^2 T / \partial x^2$, with the diffusivity $\alpha = k / (\rho c)$ of the mold, the boundary value $T(0, t) = T_m$ and the initial value $T(x, 0) = T_0$. Its solution is

$$T(x, t) = T_0 + (T_m - T_0)\, \operatorname{erfc}\!\left(\frac{x}{2\sqrt{\alpha t}}\right).$$

**The heat flux falls as $1/\sqrt{t}$.** The flux into the mold at $x = 0$ is $q = -k\, \partial T / \partial x$. Since the derivative of $\operatorname{erfc}(u)$ is $-2 e^{-u^2} / \sqrt{\pi}$,

$$q(t) = \frac{k\,(T_m - T_0)}{\sqrt{\pi \alpha t}} = (T_m - T_0)\sqrt{\frac{k \rho c}{\pi t}}.$$

The heat that has entered one unit of area of the mold by the time $t$ is the integral of $q$:

$$\int_0^t q(s)\, ds = 2\,(T_m - T_0)\sqrt{\frac{k \rho c\, t}{\pi}}.$$

**The heat balance.** To freeze, the casting must give up its latent heat, $\rho_s L V$, where $\rho_s$ is the density of the metal and $L$ its latent heat per unit mass. If the flux is the same over all of $A$, which is the one-dimensional assumption, the casting is solid at the time $t$ when

$$\rho_s L V = 2 A\,(T_m - T_0)\sqrt{\frac{k \rho c\, t}{\pi}}.$$

Solve for $t$:

$$t = \frac{\pi}{4} \left(\frac{\rho_s L}{T_m - T_0}\right)^{2} \frac{1}{k \rho c} \left(\frac{V}{A}\right)^{2}.$$

This is the rule with $n = 2$ and an explicit $B$. The volume enters once, through the heat that must be removed, and the time enters as $\sqrt{t}$, through the heat that the mold can take. So the time grows with the square of the modulus. The product $k \rho c$ of the mold, its *heat diffusivity*, is the only mold property in $B$: a mold that absorbs heat faster gives a smaller $B$.

**A second limit gives $n = 1$.** Now let the resistance be at the interface instead, as for a metal mold with a coating or an air gap, with a heat transfer coefficient $h$ and both sides at nearly constant temperatures. Then the flux is constant, $q = h (T_m - T_0)$, and the balance $\rho_s L V = h (T_m - T_0) A t$ gives

$$t = \frac{\rho_s L}{h\,(T_m - T_0)} \cdot \frac{V}{A},$$

which is the rule with $n = 1$. Real molds lie between the two limits, which is one reason why fitted exponents are less than 2.

## What it counts

The model counts the time to remove the latent heat of the casting through its cooling surface. It does not count the time to remove the superheat before freezing starts, or the time for the solid to cool to the temperature of shakeout. With superheat $\Delta T_s$, the heat to remove per unit mass becomes $L + c_s \Delta T_s$ for the specific heat $c_s$ of the liquid, so $L$ in $B$ is replaced by this sum, and the rule keeps its form.

The quantity that planners use is not $t$ but the order of the times. For that only the modulus matters, since $B$ and $n$ are the same for all sections of one casting.

## Relation to other models

### Where it comes from

Chvorinov worked on steel castings in sand molds and published the rule in the German journal Die Giesserei in 1940, in three parts. The form $t \propto (V/A)^2$ follows from the conduction model above, which Flemings gives in his book on solidification. Wlodawer built the modulus method of feeder design on it, see [riser design by the modulus method](/riser-design-modulus-method/). The rule is an empirical law in the same sense as the [Taylor tool life equation](/taylor-tool-life-equation/) of machining: a short formula with fitted constants that a planner can use without a simulation.

A full solution of the heat equation over the casting and the mold, by the [finite difference method](/finite-difference-method/) or the [finite element method](/finite-element-method/), with latent heat, gives the freezing time at every point and replaces the rule when the geometry or the alloy is far from its assumptions.

### Range of validity

The derivation makes these assumptions, so the rule ignores what they leave out.

- **Superheat.** The model starts at $T_m$. Superheat can be added to $L$ as above, which changes $B$ but not $n$.
- **Latent heat only.** The heat of the liquid above $T_m$ and the heat of the solid below it are not in the balance. For a metal with a small $L$ relative to $c_s (T_m - T_0)$ this matters more.
- **Resistance in the mold only.** The metal is assumed to conduct heat so well that it has no temperature gradient. This is close for sand and investment molds. For metal molds the resistance is at the interface and in the casting, and $n$ moves towards 1, as the second limit shows.
- **No interface resistance.** A gap that opens when the casting shrinks away from the mold adds a resistance that changes with time.
- **A flat, one-dimensional surface.** At a convex surface of the casting, the heat spreads out into more mold, and the flux is higher than in one dimension. For a sphere of radius $r$ in an infinite mold, Flemings gives $q = k (T_m - T_0) \bigl(1/\sqrt{\pi \alpha t} + 1/r\bigr)$, so small, compact castings freeze faster than the rule says. At a concave corner of the casting, the mold is a thin wedge that heats up quickly and takes less heat, so the metal there freezes later. This is why inside corners make hot spots.
- **An infinite mold.** A thin wall of sand, such as a core inside a casting with metal on both sides, heats up and stops taking heat. Its faces then cool the casting much less than the rule assumes.
- **A pure metal or a eutectic.** An alloy with a freezing range freezes over a range of temperatures and releases its latent heat over it, and a mushy zone grows instead of a sharp front. The rule then predicts the end of freezing less well.
- **No convection.** Flow in the liquid after pouring carries heat and is not in the model.
- **Constant properties.** $k$, $\rho$ and $c$ of the mold change with temperature, and the sand can lose water and binder near the casting.

Inside its range, the rule ranks sections well, which is what feeding design needs. Its absolute times are less reliable, so $B$ is fitted from tests, not computed from handbook properties.

## Known results in the model

### How planners use it

**Moduli of simple shapes.** For a section that loses heat on all its faces:

| shape | $V/A$ |
|---|---|
| plate of thickness $T$, large | $T/2$ |
| square bar of side $a$, long | $a/4$ |
| round bar of radius $r$, long | $r/2$ |
| cube of side $a$ | $a/6$ |
| sphere of radius $r$ | $r/3$ |

For a plate, a long bar and a long cylinder, the ends are ignored. For a section of a larger casting, the faces that join other sections are left out of $A$, which makes its modulus larger.

**Worked example.** A plate of $200 \times 200 \times 20$ mm has $V = 800{,}000$ mm$^3$ and $A = 2 \times 40{,}000 + 4 \times 4{,}000 = 96{,}000$ mm$^2$, so $M = 8.33$ mm. The infinite plate value $T/2 = 10$ mm is larger, since the edges also cool. A cube of side 100 mm has $M = 100/6 = 16.67$ mm. The two moduli differ by a factor of 2, so with $n = 2$ the cube takes $2^2 = 4$ times as long to freeze as the plate.

Suppose a test cube of side 50 mm, $M = 0.833$ cm, freezes in 4.0 min in a given mold. With $n = 2$, $B = 4.0 / 0.833^2 = 5.76$ min/cm$^2$. Then the plate, with the same modulus, also freezes in 4.0 min, and the 100 mm cube in $5.76 \times 1.667^2 = 16.0$ min. This value of $B$ is a made-up test result, used only to show the steps.

**Size of $B$ from the model.** With property values of the size found in handbooks for steel in silica sand, assumed here and not taken from a named table ($\rho_s = 7300$ kg/m$^3$, $L = 272$ kJ/kg, $T_m - T_0 = 1500$ K, and for the sand $k = 0.52$ W/(m K), $\rho = 1600$ kg/m$^3$, $c = 1170$ J/(kg K)), the formula gives $B = 1.41 \times 10^6$ s/m$^2$, or about 2.4 min/cm$^2$. This is the right order, but a real value must come from a test, for the reasons in the range of validity.

**Ranking and feeding.** The section with the largest modulus freezes last, so it is where shrinkage porosity forms if nothing feeds it. A casting is fed well when the moduli of its sections grow along the path to a feeder, so that freezing moves from the thin sections towards the feeder. A feeder must have a larger modulus than the section it feeds. Both rules are the subject of [riser design by the modulus method](/riser-design-modulus-method/). The modulus of a whole section is a coarse measure. [Hot spot detection](/casting-hot-spot-detection/) finds the points inside a casting that freeze last, with a geometric proxy such as the [distance transform](/distance-transform/) or with a simulation.

## References
