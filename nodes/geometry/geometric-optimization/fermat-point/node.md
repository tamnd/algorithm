---
tag: 5JH6XC
kind: concept
slug: fermat-point
name: Fermat point
aliases:
- Fermat-Torricelli point
- Torricelli point
- first isogonic center
area: geometry/geometric-optimization
level: core
summary: The point with the smallest sum of distances to the corners of a triangle. If all angles are below 120 degrees, it sees each side at 120 degrees; otherwise it is the obtuse corner.
prereqs: [euclidean-distance, convex-function, dot-product]
see_also: [geometric-median, weiszfelds-algorithm, euclidean-steiner-tree-problem, steiner-ratio, facility-location-problem, subgradient, minimum-enclosing-circle]
sources:
  - book: isbn:9780195105193
    title: Richard Courant and Herbert Robbins, What Is Mathematics?, 2nd edition revised by Ian Stewart, Oxford University Press, 1996
    locator: Chapter VII, Steiner's problem (the 120 degree condition, the case of an angle of 120 degrees or more, and the generalization to n points)
  - paper: doi:10.1007/BF01584648
    title: Harold W. Kuhn, A note on Fermat's problem, Mathematical Programming 4, 1973
    locator: the whole paper (the n-point problem with weights, the optimality condition at a data point, and the convergence of Weiszfeld's iteration)
  - paper: "Edgar N. Gilbert and Henry O. Pollak, Steiner minimal trees, SIAM Journal on Applied Mathematics 16(1), 1968"
    locator: the three-point case and the 120 degree angles at Steiner points
---

The Fermat point of a triangle $ABC$ is the point $F$ that minimizes $|FA| + |FB| + |FC|$. If every angle of the triangle is less than 120 degrees, $F$ is the unique point inside the triangle from which each side is seen at an angle of 120 degrees, and the three lines that join each corner to the apex of the equilateral triangle erected outward on the opposite side all pass through $F$. If one angle is 120 degrees or more, $F$ is the corner with that angle. Fermat posed the problem and Torricelli solved it in the seventeenth century. The Fermat point is the [geometric median](/geometric-median/) of three points and the Steiner point of a three-terminal [Euclidean Steiner tree](/euclidean-steiner-tree-problem/).

## In plain words

Three towns want to share one well, and they will dig a straight pipe from the well to each town. Where should the well go so that the total pipe is as short as possible?

In most triangles the best place is inside, at the one spot where the three pipes meet at equal angles, so that each pair of pipes makes a third of a full turn. There, a pull of equal strength along each pipe toward its town would leave the well at rest.

If one corner of the triangle is very wide, the best place is that corner itself. Then one town has the well, and the other two run pipes to it. A pull toward the two far towns is then too weak to move the well away from the wide corner.

## The idea

Notation: $A, B, C$ are points in the plane, with $a = |BC|$, $b = |CA|$, $c = |AB|$ and $K$ the area of the triangle; a point is $p = (x, y)$; $f(p) = |pA| + |pB| + |pC|$ with the [Euclidean distance](/euclidean-distance/); for $p \ne q$, $u_q(p) = (p - q)/|p - q|$ is the unit vector from $q$ toward $p$.

**Theorem.** Let $A, B, C$ not lie on one line.

1. $f$ has exactly one minimizer $F$.
2. If every angle of $ABC$ is less than 120 degrees, $F$ lies inside the triangle and $\angle AFB = \angle BFC = \angle CFA = 120°$. Then $f(F) = |CC'|$, where $C'$ is the apex of the equilateral triangle on $AB$ on the side away from $C$, and $f(F)^2 = \frac{1}{2}(a^2 + b^2 + c^2) + 2\sqrt{3}\,K$.
3. If the angle at $A$ is at least 120 degrees, then $F = A$ and $f(F) = b + c$.

*Proof.* Each term $|p - q|$ is a [convex function](/convex-function/) of $p$, and it is strictly convex along every line that does not pass through $q$. No line passes through all three points, so $f$ is strictly convex along every line, and it tends to infinity as $|p|$ grows. So a minimizer exists and is unique.

At a point $p$ that is not a corner, $f$ is differentiable with gradient $u_A(p) + u_B(p) + u_C(p)$. Three unit vectors sum to zero exactly when they are the sides of an equilateral triangle placed head to tail, that is, when each pair makes an angle of 120 degrees.

At the corner $A$, the one-sided derivative of $f$ in a unit direction $v$ is $1 + \langle u_B(A) + u_C(A), v \rangle$, from the term $|pA|$ and the two smooth terms. The smallest value over all $v$ is $1 - |u_B(A) + u_C(A)|$, so $A$ is a minimizer exactly when $|u_B(A) + u_C(A)| \le 1$. The angle between $u_B(A)$ and $u_C(A)$ is the angle $\alpha$ of the triangle at $A$, so this is $2 + 2\cos \alpha \le 1$, or $\cos \alpha \le -\frac{1}{2}$, or $\alpha \ge 120°$. This gives part 3. In part 2 no corner meets this condition, so $F$ is not a corner and the three 120 degree angles hold at $F$. The gradient condition also writes $F$ as a weighted average of $A, B, C$ with positive weights $1/|FA|, 1/|FB|, 1/|FC|$, so $F$ is inside the triangle.

For the length, let $R$ be the rotation by 60 degrees about $A$ that takes $B$ to $C'$. For any $p$, the triangle $A\,p\,R(p)$ is equilateral, so $|p\,R(p)| = |pA|$, and $|R(p)\,C'| = |pB|$. Hence $f(p) = |Cp| + |p\,R(p)| + |R(p)\,C'| \ge |CC'|$. At $F$, the angles of 120 degrees at $F$ and of 60 degrees in the equilateral triangle put $C, F, R(F), C'$ on one line in this order, so equality holds. The law of cosines in the triangle $A C C'$, with the angle $\alpha + 60°$ at $A$, gives $|CC'|^2 = b^2 + c^2 - 2bc \cos(\alpha + 60°) = b^2 + c^2 - bc\cos\alpha + \sqrt{3}\,bc \sin \alpha$, and $2bc\cos \alpha = b^2 + c^2 - a^2$, $bc \sin \alpha = 2K$. $\square$

The proof of part 2 gives the construction usually credited to Thomas Simpson (1750): erect equilateral triangles outward on two sides and join each apex to the opposite corner. The two lines meet at $F$, and each has length $f(F)$.

**Degenerate input.** If the three points lie on a line, $f$ is minimized at the middle point, which agrees with part 3 since the angle there is 180 degrees. If two points coincide, that point is the minimizer.

**Weights.** For positive weights $w_A, w_B, w_C$ and $f(p) = \sum w_q |pq|$, the same argument shows that an interior minimizer satisfies $w_A u_A + w_B u_B + w_C u_C = 0$, a triangle of forces, and that the corner $A$ is optimal exactly when $|w_B u_B(A) + w_C u_C(A)| \le w_A$. The mechanical model is the Varignon frame: three strings through holes in a table, with the weights hanging below and the strings knotted at the minimizer.

## Examples

**Equilateral triangle** $(0, 0), (2, 0), (1, \sqrt{3})$: $F$ is the center $(1, 1/\sqrt{3})$, and $f(F) = 3 \cdot 2/\sqrt{3} = 2\sqrt{3} \approx 3.4641$. The formula gives $f(F)^2 = \frac{1}{2}(4 + 4 + 4) + 2\sqrt{3} \cdot \sqrt{3} = 12$.

**Right isosceles triangle** $(0, 0), (1, 0), (0, 1)$: the angles are 90, 45 and 45 degrees. By symmetry $F = (t, t)$, and the 120 degree condition gives $t = (3 - \sqrt{3})/6 \approx 0.2113$. The formula gives $f(F)^2 = \frac{1}{2}(1 + 1 + 2) + 2\sqrt{3} \cdot \frac{1}{2} = 2 + \sqrt{3}$, so $f(F) = (\sqrt{6} + \sqrt{2})/2 \approx 1.9319$.

**Scalene triangle** $(0, 0), (4, 0), (1, 3)$: the angles are about 71.57, 45 and 63.43 degrees. Here $a^2 = 18$, $b^2 = 10$, $c^2 = 16$ and $K = 6$, so $f(F) = \sqrt{22 + 12\sqrt{3}} \approx 6.5410$, at $F \approx (1.3022, 1.0467)$. The apex on $AB$ is $C' = (2, -2\sqrt{3})$, and $|CC'|^2 = 1 + (3 + 2\sqrt{3})^2 = 22 + 12\sqrt{3}$, the same value.

**The wide-angle trap** $A = (0, 0), B = (4, 0), C = (-1, 1)$: the angle at $A$ is 135 degrees, so $F = A$ and $f(F) = 4 + \sqrt{2} \approx 5.4142$. The construction still produces lines that meet, at about $(-0.1383, -0.2823)$, outside the triangle, where $f \approx 6.0071$. The formula gives $\sqrt{22 + 4\sqrt{3}} \approx 5.3785$, a value below the true minimum that no point attains. Code that uses the construction without the angle test returns a wrong point and a wrong length.

## Where it is used

- **Geometric median.** The Fermat point is the [geometric median](/geometric-median/) of three points. For more points there is no construction by ruler and compass in general, and [Weiszfeld's algorithm](/weiszfelds-algorithm/) computes the median by iteration; its fixed point equation is the weighted average that appears in the proof above.
- **Steiner trees.** The shortest network that joins three points is the star at the Fermat point when all angles are below 120 degrees, and the two shorter sides otherwise. In every [Euclidean Steiner tree](/euclidean-steiner-tree-problem/), each added Steiner point has three edges at 120 degrees, so it is the Fermat point of its three neighbors. The equilateral triangles of the construction are the basis of Melzak's algorithm.
- **Steiner ratio.** For the equilateral triangle with side 1, the star at $F$ has length $\sqrt{3}$ and a spanning tree has length 2. The ratio $\sqrt{3}/2$ is the value in the [Gilbert-Pollak conjecture](/steiner-ratio/).
- **Facility location.** The Fermat point is the one-facility, three-client case of the Weber problem in [facility location](/facility-location-problem/).
- **Optimality conditions.** The corner test is a worked case of the [subgradient](/subgradient/) condition for a nonsmooth convex function: zero must lie in the set of subgradients at the minimizer.

## References
