---
tag: F7AXBD
kind: technique
slug: curvature-comb
name: Curvature comb
aliases:
- porcupine plot
- curvature plot
area: cad/surface-interrogation-and-design
level: intro
summary: Draws the curvature of a curve as spikes along its normal, so inflections, curvature jumps and unfair regions show at a glance.
prereqs: [frenet-frame, parametric-curve]
see_also: [frenet-frame, bezier-curve, parametric-continuity, isophote, reflection-lines, curve-offsetting]
sources:
  - book: isbn:9783540424543
    title: Nicholas M. Patrikalakis and Takashi Maekawa, Shape Interrogation for Computer Aided Design and Manufacturing, Springer, 2002
    locator: Chapter 8, Curve and Surface Interrogation (interrogation of curves by curvature plots)
  - paper: "Gerald Farin and Nickolas Sapidis, Curvature and the fairness of curves and surfaces, IEEE Computer Graphics and Applications 9(2), 52 to 57, 1989"
    title: Farin and Sapidis 1989
    locator: curvature plots as a test of the fairness of curves, and fair curves as curves whose curvature plot has few monotone pieces
  - book: isbn:9780132125895
    title: Manfredo P. do Carmo, Differential Geometry of Curves and Surfaces, Prentice-Hall, 1976
    locator: Section 1-5 (signed curvature of plane curves and the Frenet formulas)
---

A curvature comb is a drawing of a plane curve with a short segment, a tooth, at each of many sample points, perpendicular to the curve and with length proportional to the curvature there. The free ends of the teeth form a second curve, and its shape shows how the curvature varies: where it changes sign, where it jumps, and where it wobbles. The comb is a diagnostic, not an algorithm. It shows the curvature function of a curve to a designer, who reads it to judge whether the curve is fair.

## In plain words

Drive along a road and watch the steering wheel. On a straight part it is centered, in a long bend it is turned and held, and at an S-bend it swings from one side to the other. A curvature comb draws this. At many points along the curve it puts a little spike, sideways, as long as the steering wheel is turned. A gentle bend gets short spikes, a tight bend long ones, and a straight part none. The spikes switch sides where the curve switches from turning left to turning right. If you join the tips of the spikes, a well shaped curve gives a smooth, calm outline. A sudden step in that outline means the steering wheel jumped, which a driver or a machine tool would feel.

## When it applies

- The input is a plane curve with at least two continuous derivatives on each piece: a [Bézier curve](/bezier-curve/), a B-spline or a NURBS curve, a curve of a sketch, or a section of a surface.
- The question is about smoothness and fairness: is a join $G^2$, where are the inflections, and does the curvature vary in a few monotone pieces?
- For a surface, combs are drawn on chosen curves of it, such as isoparametric curves or plane sections. For whole surfaces, [isophotes](/isophote/) and [reflection lines](/reflection-lines/) do the same job.

## The template

Let $c(t) = (x(t), y(t))$ be a regular plane curve. Use the unit tangent $T = c'/|c'|$, the left unit normal $N = (-y', x')/|c'|$, and the signed curvature

$$\kappa = \frac{x' y'' - y' x''}{|c'|^3},$$

which is positive where the curve turns to the left, toward $N$. The center of curvature is $c + N/\kappa$. Choose a scale $s > 0$.

1. Sample parameters $t_0 < t_1 < \dots < t_m$, densely enough that consecutive tips are close, and preferably equally spaced in arc length.
2. At each $t_i$, compute $\kappa_i$ and $N_i$, and draw the tooth from $c(t_i)$ to the tip $c(t_i) - s \kappa_i N_i$.
3. Join the tips in order by a polyline, the *tip curve*.

With the minus sign, each tooth points away from the center of curvature, to the convex side of the curve. Some systems draw the teeth to the concave side; the picture is then mirrored, and the readings below do not change. A tooth has length $s |\kappa|$. The scale is chosen so that the longest tooth is a fixed fraction of the size of the drawing.

**What the tip curve shows.** Parametrize by arc length, so that the Frenet formulas are $T' = \kappa N$ and $N' = -\kappa T$ (see [Frenet frame](/frenet-frame/)). The tip curve is $\tau = c - s \kappa N$, and

$$\tau' = (1 + s \kappa^2)\, T - s \kappa' N.$$

- If the curve is $G^2$, then $\kappa$ and $N$ are continuous, so $\tau$ is continuous. If it is $G^1$ but the curvature jumps from $\kappa^-$ to $\kappa^+$, the tip jumps by $s |\kappa^+ - \kappa^-|$ along $N$.
- Since $1 + s \kappa^2 > 0$, the tip curve is always regular, and its direction makes the angle $\arctan(s \kappa' / (1 + s \kappa^2))$ with $T$, measured toward $-N$. So if $\kappa'$ jumps, as at a $G^2$ join that is not $G^3$, the tip curve has a corner.
- At an inflection, $\kappa$ changes sign, the teeth change sides, and the tip curve crosses the curve.
- A fair curve has a tip curve with few wiggles, because its curvature has few monotone pieces (Farin and Sapidis 1989).

## Classic examples

### Worked example: a cubic Bézier curve with an inflection

Take the cubic Bézier curve with control points $(0, 0)$, $(1, 1)$, $(2, -1)$, $(3, 0)$, and the scale $s = 0.5$. Then $c'(t) = (3,\ 18t^2 - 18t + 3)$ and $c''(t) = (0,\ 36t - 18)$, so $x' = 3$ is constant and

$$\kappa(t) = \frac{3 (36 t - 18)}{\left(9 + (18 t^2 - 18 t + 3)^2\right)^{3/2}}.$$

| $t$ | $c(t)$ | $c'(t)$ | $\kappa$ | $N$ | tip $c - s \kappa N$ |
|---|---|---|---|---|---|
| $0$ | $(0, 0)$ | $(3, 3)$ | $-1/\sqrt 2 \approx -0.70711$ | $(-0.70711, 0.70711)$ | $(-0.25, 0.25)$ |
| $1/4$ | $(0.75, 0.28125)$ | $(3, -0.375)$ | $-0.97701$ | $(0.12403, 0.99228)$ | $(0.81059, 0.76598)$ |
| $1/2$ | $(1.5, 0)$ | $(3, -1.5)$ | $0$ | $(0.44721, 0.89443)$ | $(1.5, 0)$ |
| $3/4$ | $(2.25, -0.28125)$ | $(3, -0.375)$ | $0.97701$ | $(0.12403, 0.99228)$ | $(2.18941, -0.76598)$ |
| $1$ | $(3, 0)$ | $(3, 3)$ | $1/\sqrt 2 \approx 0.70711$ | $(-0.70711, 0.70711)$ | $(3.25, -0.25)$ |

The comb reads as follows. On the first half the curve turns right ($\kappa < 0$), and the teeth stand above it, on its convex side. At $t = 1/2$ the tooth has length zero: this is the only inflection, since $36t - 18$ has its only zero there. On the second half the teeth stand below. The curve is symmetric about the point $(1.5, 0)$, and so is the comb. The longest teeth are at $t \approx 0.1492$ and $t \approx 0.8508$, where $|\kappa| \approx 1.2916$ and the tooth length is about $0.6458$. The tip curve is continuous and smooth, as it must be for a polynomial curve.

### A line joined to a circular arc

Join the segment from $(-2, 0)$ to $(0, 0)$ to the quarter circle of radius $2$ with center $(0, 2)$, from $(0, 0)$ to $(2, 2)$. The join is $G^1$: both pieces have the tangent $(1, 0)$ at $(0, 0)$. The curvature is $0$ on the segment and $1/2$ on the arc. With $s = 0.5$ the teeth on the segment have length $0$, so the tip curve is the segment itself, and the teeth on the arc have length $0.25$ and point away from the center, so the tip curve is the circle of radius $2.25$ about $(0, 2)$. At the join the tip curve jumps from $(0, 0)$ to $(0, -0.25)$. This step is the reason road and rail designers put a transition curve with linearly growing curvature between a straight and an arc.

## Variations

- **Curvature graph.** Plot $\kappa$ against arc length in a separate chart. It shows the same data, without the geometry of the curve.
- **Radius of curvature comb.** Teeth of length $1/|\kappa|$ toward the center of curvature, so that the tips trace the evolute. It is unbounded near inflections and is used less.
- **Space curves.** Teeth along the principal normal with length $s \kappa$, $\kappa \ge 0$. There are no signed inflections, so a second comb of the torsion is sometimes added.
- **Surfaces.** Combs on a net of isoparametric curves or of plane sections give a coarse picture of the surface curvature.

## Pitfalls

- **Scale.** With a scale that is too small, real jumps are invisible. With one that is too large, the tip curve crosses itself and is hard to read.
- **Sampling.** The comb shows only the samples. A curvature spike between two samples, for example near a short knot interval of a B-spline, can be missed. Equal steps in the parameter put few teeth where the curve moves fast.
- **Points with zero speed.** Where $c' = 0$, for example when two end control points coincide, the formula for $\kappa$ divides by zero, and the curve can have a cusp there.
- **Tessellated curves.** A comb computed from a polyline, by fitting circles through consecutive vertices, shows noise of the tessellation and not the curvature of the design curve.
- **Parametric smoothness.** A comb shows geometric smoothness. A curve can be $C^2$ in its parameter and still have a corner where its speed is zero, for example $(t^3, \max(t, 0)^3)$ at $t = 0$, and a curve can be $G^2$ without being $C^2$.

## Exercises

1. Draw the comb of a circle of radius $R$ traversed counterclockwise. Show that the tip curve is the circle of radius $R + s/R$ with the same center.
2. For the parabola $c(t) = (t, t^2)$, show that $\kappa(t) = 2/(1 + 4t^2)^{3/2}$, and find the tip of the tooth at $t = 0$ for $s = 1$. (Answer: $(0, -2)$.)
3. Show that a $G^2$ join of two curves gives a continuous tip curve, and that the tip curve of the line and arc example jumps by $s/R$.
4. Show that the tip curve $\tau = c - s \kappa N$ of a curve parametrized by arc length is regular for every $s > 0$.

## References
