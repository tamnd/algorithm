---
title: The engagement angle has closed forms for straight and circular cuts, and each step of the generator keeps the pixel stock exact and picks a heading at which the engagement crosses the target
proves: [correctness]
status: full
---

**Setting.** The tool is a disk of radius $R$ with center $c$, moving in the unit direction $u$. Let $u^\perp$ be $u$ turned by $+90°$. The front half circle is $\{c + R(\cos t\, u + \sin t\, u^\perp) : |t| \le 90°\}$. The engagement angle $\theta(c, u)$ is the measure of the set of $t \in [-90°, 90°]$ whose point is in material. The code samples $n$ values of $t$, at the centers of $n$ equal arcs, so it returns the measure of the sampled set, $180°$ times the fraction of samples in material.

**Claim 1 (straight cut).** Let the material be the half-plane above a line parallel to $u$, at the distance $a \in [0, 2R]$ inside the tool, measured from the side of the tool farthest into the material: in coordinates with $u = (1, 0)$ and $c = (0, a - R)$, the material is $\{y \ge 0\}$. Then $\theta = \arccos(1 - a/R)$.

*Proof.* The point at $t$ has height $a - R + R\sin t$. It is in material when $\sin t \ge 1 - a/R$. On $[-90°, 90°]$, $\sin$ is increasing, so the set is $[\arcsin(1 - a/R), 90°]$, of measure $90° - \arcsin(1 - a/R) = \arccos(1 - a/R)$. $\square$

**Claim 2 (circular cut).** Let the tool center move on the circle of radius $\rho$ about $O$, counterclockwise, so $u$ is the tangent, and let $n$ be the outward unit normal at $c$. Let the material ahead of the tool be the set of points at distance more than $R_b$ from $O$, with $\rho - R < R_b < \rho + R$. Then
$$
\cos\theta = \frac{R_b^2 - \rho^2 - R^2}{2\rho R}.
$$

*Proof.* Write a point of the tool circle as $c + R(\cos\varphi\, n + \sin\varphi\, u)$, with $\varphi$ measured from $n$ toward $u$. Its squared distance from $O$ is $\rho^2 + R^2 + 2\rho R\cos\varphi$, since $c = \rho n$ and $n \perp u$. So it lies beyond $R_b$ exactly when $\cos\varphi > \cos\alpha_0$, with $\cos\alpha_0$ the right side above, that is when $|\varphi| < \alpha_0$. The front half is $u$-side: $\sin\varphi \ge 0$, that is $\varphi \in [0°, 180°]$. On it, the material set is $[0, \alpha_0)$, of measure $\alpha_0$. Points with $\varphi < 0$ lie behind the tool; in a steady pass they were already removed by earlier positions of the same pass, and in any case they are not in the front half. $\square$

**Claim 3 (constant engagement stepover on a circle).** If the previous pass left the boundary at $R_b = \rho - s + R$, the engagement equals $\theta^*$ exactly when
$$
s = \rho + R - \sqrt{\rho^2 + R^2 + 2\rho R\cos\theta^*}.
$$

*Proof.* Claim 2 with $\theta = \theta^*$ gives $R_b^2 = \rho^2 + R^2 + 2\rho R\cos\theta^*$, and $R_b > 0$, so $R_b$ is the positive root. Solve $R_b = \rho - s + R$ for $s$. $\square$

As $\rho \to \infty$ this tends to $R(1 - \cos\theta^*)$, the stepover of Claim 1, and for finite $\rho$ it is smaller, because $\rho^2 + R^2 + 2\rho R\cos\theta^* > (\rho + R\cos\theta^*)^2$ when $\sin\theta^* \ne 0$.

**Claim 4 (one step of the generator).** Assume that before a step the stock holds exactly the pixels whose centers are in the initial material and at distance more than $R$ from every segment cut so far. Then:

(a) after line L7 the same holds with the new segment added;

(b) the new heading $\varphi$ lies within the allowed turn of the old heading $\psi$;

(c) let $E(\varphi)$ be the sampled engagement at $c + \sigma(\cos\varphi, \sin\varphi)$ with heading $\varphi$. If $E(\text{away}) < \theta^* < E(\text{toward})$, the bisection of line L6 ends with two headings $\ell$ and $h$, $|\ell - h| = 2\Delta / 2^{12}$, with $E(\ell) > \theta^* \ge E(h)$, and returns their midpoint. In the other cases it returns the end of the allowed range that is nearest to the target, as lines L4 and L5 say.

*Proof.* (a) The function `cut_capsule` visits every pixel whose center can be within $R$ of the segment (a box around it), computes the exact nearest point of the segment to the center by clamping the projection parameter to $[0, 1]$, and clears the pixel when the distance is at most $R$. No other pixel changes. (b) Lines L3 to L6 only return `toward`, `away`, or a point between them, which are $\psi \pm \Delta$. (c) The bisection keeps the invariant $E(\ell) > \theta^* \ge E(h)$: it holds at the start by the case condition, and each step replaces $\ell$ or $h$ by the midpoint according to the side of $\theta^*$ on which $E(\text{mid})$ falls. After 12 halvings the interval has length $2\Delta/2^{12}$. $\square$

**Termination.** Each step evaluates $E$ at most 15 times, each evaluation looks at $n$ samples, and each cut visits a finite box of pixels. So the generator stops after its given number of steps.

**What is proved and what is measured.** Claims 1 to 3 are exact statements about the engagement of a disk. Claim 4 says what one step does: the stock stays exact for the pixel model, and the heading is a point where the sampled engagement crosses the target. If the engagement grows as the heading turns toward the material, which holds for the smooth boundaries met in the tests, this crossing is where the engagement equals the target up to the sample step of $180°/n$. Nothing here proves that a whole path keeps the engagement near the target, avoids leaving islands of material, or finishes the region. Those are measured: in the tests the path holds $60°$ to $63°$ after a warm-up, the pixel engagement agrees with an exact stock (Fractions, union of capsules) to within two samples, and it matches Claims 1 and 2 to within one sample plus $2°$.
