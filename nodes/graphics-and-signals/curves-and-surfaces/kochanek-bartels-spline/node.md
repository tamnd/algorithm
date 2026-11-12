---
tag: 9M4696
kind: definition
slug: kochanek-bartels-spline
name: Kochanek-Bartels spline
aliases:
- TCB spline
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: An interpolating cubic Hermite spline whose tangents at each key come from three parameters, tension, continuity and bias. It generalizes the Catmull-Rom spline for keyframe animation.
prereqs: [hermite-spline, catmull-rom-spline]
see_also: [parametric-continuity, curve-interpolation, natural-cubic-spline, arc-length-parametrization]
sources:
  - paper: doi:10.1145/964965.808575
    title: Doris H. U. Kochanek and Richard H. Bartels, Interpolating splines with local tension, continuity, and bias control, Computer Graphics 18(3), 33-41 (SIGGRAPH 1984)
    locator: the three parameters, the incoming and outgoing tangents, and the adjustment for keys at unequal time intervals
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 9, Constructing Spline Curves (C1 piecewise cubic interpolation and the choice of tangents)
  - book: isbn:9780201848403
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition in C, Addison-Wesley, 1996
    locator: Chapter 11, Representing Curves and Surfaces (Hermite curves, Catmull-Rom splines and the Kochanek-Bartels parameters)
---

A Kochanek-Bartels spline, or TCB spline, is an interpolating [Hermite spline](/hermite-spline/) for keyframe animation. At each key the animator sets three numbers: the tension $t$, the continuity $c$ and the bias $b$. They fix the tangents from the two chords next to the key. With $t = c = b = 0$ the curve is the uniform [Catmull-Rom spline](/catmull-rom-spline/). The tension changes the length of the tangents, the bias turns them towards one chord, and the continuity gives each key two different tangents, so the curve can have a corner. Doris Kochanek and Richard Bartels published the method at SIGGRAPH 1984. It is the key interpolation of many animation systems, because the three parameters act only on the two segments next to a key and have a visible meaning.

## Definition

Let $P_0, \dots, P_n$ be keys in $\mathbb{R}^d$, $n \ge 3$. Each inner key $P_k$ has parameters $t_k, c_k, b_k$, usually in $[-1, 1]$. Write

$$\Delta^{in}_k = P_k - P_{k-1}, \qquad \Delta^{out}_k = P_{k+1} - P_k$$

for the chords before and after the key. The key has an *incoming tangent* $T^{in}_k$, used at the end of the segment that arrives at $P_k$, and an *outgoing tangent* $T^{out}_k$, used at the start of the segment that leaves it:

$$T^{in}_k = \frac{(1 - t)(1 - c)(1 + b)}{2}\, \Delta^{in}_k + \frac{(1 - t)(1 + c)(1 - b)}{2}\, \Delta^{out}_k,$$

$$T^{out}_k = \frac{(1 - t)(1 + c)(1 + b)}{2}\, \Delta^{in}_k + \frac{(1 - t)(1 - c)(1 - b)}{2}\, \Delta^{out}_k,$$

with $t = t_k$, $c = c_k$, $b = b_k$. Segment $k$, from $P_k$ to $P_{k+1}$, is the cubic Hermite segment

$$C_k(u) = H_0(u) P_k + H_1(u)\, T^{out}_k + H_2(u)\, T^{in}_{k+1} + H_3(u) P_{k+1}, \qquad u \in [0, 1],$$

with the basis of the [Hermite spline](/hermite-spline/) page. As for the Catmull-Rom spline, $P_0$ and $P_n$ only shape the first and the last tangent, and the curve runs from $P_1$ to $P_{n-1}$.

**What each parameter does.** The formulas give the following, at one key.

- *Tension.* Both tangents have the factor $1 - t$. The value $t = 1$ makes them zero: the curve is the chord polygon, and the point stops at each key ($C_k(u) = P_k + H_3(u)(P_{k+1} - P_k)$). Negative tension makes the tangents longer and the curve rounder. With $c = b = 0$ the tangent is $(1 - t)\frac12 (P_{k+1} - P_{k-1})$, the tangent of a cardinal spline.
- *Continuity.* The difference of the two tangents is

$$T^{out}_k - T^{in}_k = (1 - t)\, c \left( (1 + b)\, \Delta^{in}_k - (1 - b)\, \Delta^{out}_k \right).$$

So $c = 0$ gives one tangent per key and a $C^1$ curve in the uniform parameter (each segment on a unit interval). For $c \ne 0$ the two tangents differ, the velocity jumps at the key, and the curve has a corner unless the chords are parallel. The value $c = -1$ with $t = b = 0$ gives $T^{in}_k = \Delta^{in}_k$ and $T^{out}_k = \Delta^{out}_k$. Then segment $k$ has both end tangents equal to its own chord, so it is the straight line from $P_k$ to $P_{k+1}$ at constant speed, and the keys are sharp corners. Positive $c$ turns each tangent towards the chord on the far side, which gives a boxy corner that points the other way.
- *Bias.* With $c = 0$ the tangent is $(1 - t)\left(\frac{1 + b}{2} \Delta^{in}_k + \frac{1 - b}{2} \Delta^{out}_k\right)$. The value $b = 1$ gives the incoming chord: the motion keeps its direction past the key and overshoots. The value $b = -1$ gives the outgoing chord: the motion turns early and anticipates the next key.

**Keys at unequal times.** In animation the key $P_k$ is reached at time $s_k$, and the segment parameter is $u = (s - s_k)/h_k$ with $h_k = s_{k+1} - s_k$. The velocity in time is $dC/ds = (1/h_k)\, dC/du$ (the chain rule, as in the [Hermite spline](/hermite-spline/) definition). If the same tangent $T$ is used at the end of segment $k - 1$ and at the start of segment $k$, the velocity jumps from $T/h_{k-1}$ to $T/h_k$, even for $c = 0$. The paper adjusts the two tangents of a key with factors built from the two interval lengths next to it. One choice that the chain rule justifies is: read $T^{in}_k$ and $T^{out}_k$ as the velocities $V^{in}_k = 2T^{in}_k/(h_{k-1} + h_k)$ and $V^{out}_k = 2T^{out}_k/(h_{k-1} + h_k)$, and use the tangents $h_{k-1} V^{in}_k$ at the end of segment $k - 1$ and $h_k V^{out}_k$ at the start of segment $k$. Then $c = 0$ gives $V^{in}_k = V^{out}_k$, a $C^1$ motion in time. Uniform times give back the plain formulas. The velocity along the curve is still not constant: for constant speed, reparametrize by [arc length](/arc-length-parametrization/).

**Properties.** The curve interpolates the inner keys. It is local: the data of $P_k$ change at most four segments. It is affine invariant, because the tangents are linear in the chords. It is $C^1$ where $c_k = 0$ (with the time adjustment when the keys are not evenly spaced), and in general not $C^2$. It has no convex hull property, as for the Catmull-Rom spline.

## Examples and non-examples

**The three parameters at one corner.** Take the keys $P_0 = (0, 0)$, $P_1 = (1, 0)$, $P_2 = (1, 1)$, $P_3 = (2, 1)$, the same parameters at every key, and look at the middle segment from $P_1$ to $P_2$. At $P_1$, $\Delta^{in} = (1, 0)$ and $\Delta^{out} = (0, 1)$.

| $(t, c, b)$ | $T^{in}_1$ | $T^{out}_1$ |
|---|---|---|
| $(0, 0, 0)$ | $(0.5, 0.5)$ | $(0.5, 0.5)$ |
| $(0, -0.5, 0)$ | $(0.75, 0.25)$ | $(0.25, 0.75)$ |
| $(0, 0, 0.5)$ | $(0.75, 0.25)$ | $(0.75, 0.25)$ |
| $(0.5, 0, 0)$ | $(0.25, 0.25)$ | $(0.25, 0.25)$ |

With $b = 0$ the $x$ part of the middle segment is $x(u) = 1 + \frac{(1 - t)(1 + c)}{2}\,(2u^3 - 3u^2 + u)$. The cubic $2u^3 - 3u^2 + u$ has the largest absolute value $\sqrt3/18 \approx 0.0962$ on $[0, 1]$, so the segment bulges sideways by $\frac{(1 - t)(1 + c)}{2} \cdot 0.0962$ on each side of the line $x = 1$. The bulge is $0.0481$ for Catmull-Rom ($t = c = 0$), $0.0241$ for $c = -0.5$ or for $t = 0.5$, $0.0722$ for $c = 0.5$ or for $t = -0.5$, and $0$ for $c = -1$, where the segment is the straight edge. The bias $b = 0.5$ moves the midpoint $C_1(1/2)$ from $(1, 0.5)$ to $(1.0625, 0.4375)$: the motion carries on to the right past $P_1$ before it turns up.

**A corner with $c \ne 0$.** For $(t, c, b) = (0, -0.5, 0)$ the curve arrives at $P_1$ with the velocity $(0.75, 0.25)$ and leaves with $(0.25, 0.75)$. The position is continuous and the direction turns by $\arccos 0.6 \approx 53.1°$ at the key, so the curve is $C^0$ and not $G^1$ there (see [parametric continuity](/parametric-continuity/)).

**Non-example: tension does not change the path direction at a key.** With $c = b = 0$ any tension gives tangents parallel to $P_{k+1} - P_{k-1}$. The tension changes how far the curve swings, not the direction in which it passes the key. Only $b$ and $c$ turn the tangent.

**Non-example: unequal key times without the adjustment.** Take five keys at times $0, 1, 2, 4, 5$ and use the plain tangents with $c = 0$. At the key at time 2 the curve arrives with velocity $T$ (interval length 1) and leaves with $T/2$ (interval length 2). The path is smooth, but the motion halves its speed in one frame. This is the defect that the time adjustment removes.

## Related definitions

- [Hermite spline](/hermite-spline/): the segment form. A TCB spline is a rule that sets its tangents.
- [Catmull-Rom spline](/catmull-rom-spline/): the case $t = c = b = 0$.
- Cardinal spline: the case $c = b = 0$, with tension only.
- [Natural cubic spline](/natural-cubic-spline/): a global $C^2$ alternative with no shape parameters.
- [Parametric continuity](/parametric-continuity/): $c = 0$ gives $C^1$, other values give corners.
- [Arc-length parametrization](/arc-length-parametrization/): the step that makes the speed along a TCB path constant.

## References
