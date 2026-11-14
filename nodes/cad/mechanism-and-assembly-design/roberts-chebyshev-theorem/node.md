---
tag: 4ZKXP9
kind: theorem
slug: roberts-chebyshev-theorem
name: Roberts-Chebyshev cognate theorem
aliases:
- cognate linkages theorem
- Roberts-Chebyshev theorem
area: cad/mechanism-and-assembly-design
level: core
summary: Every four-bar coupler curve is traced by two other four-bars, its cognates, so a designer can pick the one with better pivots or transmission.
prereqs: [coupler-curve, four-bar-linkage]
see_also: [grashof-condition, path-generation, transmission-angle, nine-point-path-synthesis, kinematic-synthesis, watt-and-stephenson-six-bar, instant-center-of-velocity]
sources:
  - paper: "Samuel Roberts, On three-bar motion in plane space, Proceedings of the London Mathematical Society, s1-7 (1875), 14 to 23"
  - book: "P. L. Chebyshev, Oeuvres, Volume 2, St. Petersburg, 1907"
    locator: pp. 273 to 281, the 1878 paper on the three linkages that trace one curve (first place of publication not confirmed)
  - book: isbn:9780198561248
    title: Kenneth H. Hunt, Kinematic Geometry of Mechanisms, Oxford University Press, 1978
    locator: Chapter 7, the coupler curves of the four-bar and their cognates (general locator; no page number confirmed)
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Section 3.7 (p. 134, cognates; the Roberts-Chebychev theorem on p. 134, parallel motion on p. 137, geared fivebar cognates on p. 140)
  - book: doi:10.1007/978-1-4419-7892-9
    title: J. Michael McCarthy and Gim Song Soh, Geometric Design of Linkages, 2nd edition, Springer, 2011
    locator: Chapter 2 (pp. 15 to 53), the planar 4R linkage and its coupler curve
---

The Roberts-Chebyshev theorem says that the [coupler curve](/coupler-curve/) of a four-bar is also traced by two other four-bars, its cognates. The three linkages have different ground pivots and different link lengths, but their coupler points move on the same curve, and one of the cognates even moves with the same timing when it is driven by the right link. The three pairs of ground pivots form a triangle similar to the coupler triangle. A designer who has found a good path with a bad linkage, for example with a poor [transmission angle](/transmission-angle/) or a pivot in the wrong place, can switch to a cognate.

This page is about the other linkages that trace a given curve. The [coupler curve](/coupler-curve/) page is about the curve of one linkage, its degree 6 and its triple circular points.

## Statement

Use the notation of the [four-bar linkage](/four-bar-linkage/) page in complex numbers, with ground pivots $O_A$ and $O_B$, input $a$ from $O_A$ to $A$, coupler $b$ from $A$ to $B$, output $c$ from $O_B$ to $B$, and $d = |O_B - O_A|$. Let the coupler point be $P = A + z(B - A)$ for a fixed complex number $z \ne 0, 1$, so $P \ne A$ and $P \ne B$. Put

$$u = A - O_A, \qquad w = B - A, \qquad v = B - O_B, \qquad O_C = O_A + z(O_B - O_A).$$

The triangle $O_A O_B O_C$ is similar to the coupler triangle $A B P$, with the same $z$.

**Theorem (Roberts 1875, Chebyshev 1878).**

1. *Cognate 2.* The four-bar with ground pivots $O_A$ and $O_C$, the link $O_A A_2$ with $A_2 = O_A + z w$, the coupler $A_2 B_2$ with $B_2 = A_2 + z u$, the link $O_C B_2$, and the coupler point $P_2 = A_2 + u$, has the lengths $|z|b$, $|z|a$, $|z|c$ and ground $|z|d$, and its coupler point traces the same curve as $P$.
2. *Cognate 3.* The four-bar with ground pivots $O_B$ and $O_C$, the link $O_B B_3$ with $B_3 = O_B + (z - 1) w$, the coupler $B_3 C_3$ with $C_3 = B_3 + (1 - z) v$, the link $O_C C_3$, and the coupler point $P_3 = B_3 + v$, has the lengths $|1 - z|b$, $|1 - z|c$, $|1 - z|a$ and ground $|1 - z|d$, and its coupler point traces the same curve.
3. *Bijection.* The maps $(u, w, v) \mapsto$ cognate 2 and $(u, w, v) \mapsto$ cognate 3 are bijections between the configuration spaces, and $P = P_2 = P_3$ in corresponding configurations.
4. *Timing.* In corresponding configurations the link $O_C C_3$ of cognate 3 is parallel to the input $O_A A$, so it turns with the same angular velocity. Driving cognate 3 at $O_C$ reproduces the motion of $P$ with the same timing as the original.

For a general linkage these are the only four-bars that trace the curve, so a four-bar coupler curve has exactly three generating four-bars. That uniqueness part is due to Roberts and is proved in Hunt, Chapter 7. It is cited here, not proved.

## In plain words

Pin a plate to the middle bar of a four-bar loop and mark a point on it. As the loop moves, the point draws a curve. The theorem says that you can build two more four-bar loops, with different bar lengths and different fixed pins, that draw exactly the same curve with their own marked points.

The recipe uses only parallelograms. Each bar of a new loop is a copy of a bar of the old loop, turned by a fixed angle and stretched by a fixed factor. So it turns at the same speed as the bar it copies. The three fixed pins form a triangle with the same shape as the plate. If you drive the right bar of the third loop with the same motor, the point even follows the curve at the same speed.

## Proof

**Step 1, cognate 2 closes and is rigid.** The original linkage satisfies the loop $O_A + u + w = O_B + v$, so $B - O_B = v$ and $B - O_A = u + w$. Hence

$$O_C + z v = O_A + z(O_B - O_A) + z(B - O_B) = O_A + z(B - O_A) = O_A + z(u + w) = B_2.$$

So $B_2$ is at distance $|z v| = |z|c$ from $O_C$, the link $O_A A_2$ has length $|z w| = |z|b$, and the coupler $A_2 B_2$ has length $|z u| = |z|a$. The coupler point is fixed on the coupler: $B_2 - A_2 = z u = z(P_2 - A_2)$, so $P_2 = A_2 + (B_2 - A_2)/z$ for a constant $1/z$. And it is the same point: $P_2 = O_A + z w + u = A + z w = P$.

**Step 2, cognate 3 closes and is rigid.** The vector from $O_C$ to $C_3$ is

$$C_3 - O_C = O_B + (z - 1) w + (1 - z) v - O_A - z(O_B - O_A) = (1 - z)(O_B - O_A - w + v).$$

The loop gives $O_B - O_A = u + w - v$, so the bracket is $u$. Hence $C_3 - O_C = (1 - z) u$, of length $|1 - z|a$. The link $O_B B_3$ is $(z - 1) w$, of length $|1 - z|b$, and the coupler $B_3 C_3$ is $(1 - z) v$, of length $|1 - z|c$. The coupler point is fixed on it: $C_3 - B_3 = (1 - z) v = (1 - z)(P_3 - B_3)$. And $P_3 = O_B + v + (z - 1) w = B + (z - 1) w = A + z w = P$.

**Step 3, the bijection.** Steps 1 and 2 show that every configuration $(u, w, v)$ of the original gives a configuration of each cognate with the same coupler point. Conversely, a configuration of cognate 2 is a triple of vectors $(z w', z u', z v')$ of the right lengths with $O_A + z w' + z u' = O_C + z v'$. Divide by $z$ and use $O_C - O_A = z(O_B - O_A)$: $u' + w' - v' = O_B - O_A$, which is the original loop. So $(u', w', v')$ is a configuration of the original, and the two maps are inverse. The same division by $1 - z$ works for cognate 3. A bijection of configuration spaces that keeps the coupler point gives equal coupler curves, on every circuit.

**Step 4, timing.** In cognate 3 the link at $O_C$ is $(1 - z) u$, a constant complex multiple of the input vector $u$. So its angle is the input angle plus the constant $\arg(1 - z)$, and the two angular velocities are equal. If cognate 3 is driven at $O_C$ with the motion of the original input, step 3 gives the configuration of the original at every instant, and $P_3 = P$ at every instant. $\blacksquare$

The same argument shows more: every link of a cognate is a constant multiple of a link of the original. In cognate 2, the link at $O_A$ turns with the original coupler, the coupler with the original input, and the link at $O_C$ with the original output. In cognate 3, the link at $O_B$ turns with the original coupler, the coupler with the original output, and the link at $O_C$ with the original input.

## Consequences

- **The Grashof type of the cognates.** Up to a scale, cognate 2 has the lengths $b, a, c, d$ for (link at $O_A$, coupler, link at $O_C$, ground), and cognate 3 has $b, c, a, d$ for (link at $O_B$, coupler, link at $O_C$, ground). They are the same multiset as the original, so by the [Grashof condition](/grashof-condition/) the three are all Grashof or all not. Only the place of the shortest link changes. A crank-rocker with $a$ shortest has the crank-rocker cognate 3, driven at $O_C$, and the Grashof double-rocker cognate 2, whose coupler is the short link. A double-crank, with $d$ shortest, has two double-crank cognates, since the ground stays the ground.
- **The Cayley diagram.** Drawing the original, the two parallelograms $O_A A P A_2$ and $O_B B P B_3$, and the two small copies of the coupler triangle gives a single figure with all three linkages. It is the usual way to draw cognates by hand.
- **Choice in path design.** A [path generation](/path-generation/) or [nine-point path synthesis](/nine-point-path-synthesis/) solution can be replaced by either cognate. The cognates have different [transmission angles](/transmission-angle/), different pivots and different sizes, and the designer picks the best.
- **Parallel motion and six-bars.** Since the link at $O_C$ of cognate 3 is parallel to the original input, a cognate can be joined to the original to build a six-bar whose output link moves parallel to a given link, as in Norton Section 3.7. Such a six-bar is a [Watt or Stephenson six-bar](/watt-and-stephenson-six-bar/) linkage.
- **Instant centers.** The coupler point $P$ is a point of the coupler of all three linkages. So the three instant centers $P_{13}$ of the three couplers all lie on the line through $P$ perpendicular to the tangent of the curve, the normal at $P$. This follows from the definition on the [instant center of velocity](/instant-center-of-velocity/) page.

**A worked example: Hoeken and Chebyshev.** Take the straight-line linkage of the [coupler curve](/coupler-curve/) page: $O_A = (0, 0)$, $O_B = (2, 0)$, $a = 1$, $b = c = 2.5$, and $z = 2$, so $P = A + 2(B - A)$. Then $O_C = (4, 0)$. Cognate 2 has the lengths $2b = 5$ at $O_A$, $2a = 2$ for the coupler, $2c = 5$ at $O_C$, and ground $4$, with $P_2 = A_2 + (B_2 - A_2)/2$ at the middle of the coupler: this is Chebyshev's straight-line linkage, scaled by 2, with crossed rockers. At $\theta_2 = 180°$, $A = (-1, 0)$ and $B = (0.5, 2)$, so $w = (1.5, 2)$, $u = (-1, 0)$, $v = (-1.5, 2)$, and $A_2 = (3, 4)$, $B_2 = (1, 4)$, $P_2 = (2, 4) = P$. Cognate 3 has $|1 - z| = 1$: the link $O_B B_3 = w$ of length $2.5$, the coupler of length $2.5$, a crank of length $1$ at $O_C$, and ground $2$. It is the mirror image of the original. At the same instant $B_3 = (3.5, 2)$, $C_3 = (5, 0)$ and $P_3 = (2, 4)$. All the coordinates above are exact.

## Tightness

- **The cases $z = 0$ and $z = 1$.** If $P = A$, cognate 2 has scale $|z| = 0$ and collapses, and the coupler curve is a circle, traced by many linkages. The same happens for $P = B$ with cognate 3. So the hypothesis $z \ne 0, 1$ is needed for three proper linkages.
- **Coincident cognates.** For special linkages two of the three can be congruent, as for Hoeken's linkage above, whose cognate 3 is its mirror image. Then the curve has fewer than three different generating four-bars up to congruence. The count "exactly three" is for a general linkage.
- **Timing of cognate 2.** The grounded links of cognate 2 turn with the original coupler (at $O_A$) and the original output (at $O_C$). Only its coupler turns with the original input, and a coupler cannot be driven by a motor on the ground. So cognate 2 driven at a grounded link traces the curve with different timing. Geared five-bar cognates, in Norton Section 3.7, are a way to keep the timing.
- **Other linkages.** The theorem is about four-bars. Six-bar linkages can trace the same curve too, for example a cognate joined to the original as in the parallel-motion construction. Linkages with more links trace any bounded part of an algebraic curve by the [Kempe universality theorem](/kempe-universality-theorem/).

## History

Samuel Roberts proved in 1875, in a paper to the London Mathematical Society, that a three-bar curve is traced by three different three-bar linkages, the ground not being counted as a bar. Chebyshev found the result independently and published it in 1878. The figure that holds all three linkages is called the Cayley diagram, after Cayley, who wrote on three-bar motion in 1876. In English texts the result is called the Roberts-Chebyshev theorem, and the three linkages are called cognates.

## References
