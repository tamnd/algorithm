---
tag: N10GPS
kind: problem
slug: maximum-area-inscribed-triangle
name: Maximum-area inscribed triangle
aliases:
- largest triangle in a convex polygon
- largest-area triangle of a point set
- maximum-area triangle in a convex polygon
area: geometry/geometric-optimization
level: core
summary: Find the triangle of largest area inside a convex polygon. Its corners are polygon vertices; O(n) time is possible, and a published O(n) method was shown wrong in 2017.
prereqs: [convex-polygon, oriented-triangle-area, antipodal-pairs, two-pointers]
see_also: [minimum-area-enclosing-triangle, polygon-diameter, rotating-calipers, heilbronn-triangle-problem, convex-hull-problem, minimum-area-enclosing-rectangle, polygon-width, shoelace-formula]
sources:
  - paper: doi:10.1137/0214011
    title: James E. Boyce, David P. Dobkin, Robert L. (Scot) Drysdale III and Leonidas J. Guibas, Finding extremal polygons, SIAM Journal on Computing 14(1), 1985
    locator: the whole paper (the largest-area and largest-perimeter k-gon with vertices in a point set, in O(kn log n + n log n) time)
  - paper: "David P. Dobkin and Lawrence Snyder, On a general method for maximizing and minimizing among certain geometric problems, Proceedings of the 20th IEEE Symposium on Foundations of Computer Science, 1979"
    locator: the claimed linear-time algorithm for the largest inscribed triangle
  - paper: "Vahideh Keikha, Maarten Löffler, Ali Mohades, Jérôme Urhausen and Ivor van der Hoog, Maximum-area triangle in a convex polygon, revisited, arXiv:1705.11035, 2017"
    locator: the counterexample to the Dobkin and Snyder algorithm, a quadratic repair, and an O(n log n) algorithm
  - paper: "Sharat Chandran and David M. Mount, A parallel algorithm for enclosed and enclosing triangles, International Journal of Computational Geometry and Applications 2, 1992"
    locator: the linear-time sequential algorithm for the largest enclosed and the smallest enclosing triangle
  - paper: "Kai Jin, Maximal area triangles in a convex polygon, arXiv:1707.04071, 2017"
    locator: the Rotate-and-Kill method, a linear-time algorithm, and the comparison with Chandran and Mount and with Kallus
---

The maximum-area inscribed triangle problem asks for the triangle of largest area contained in a [convex polygon](/convex-polygon/) with $n$ vertices; for a point set it asks for the largest triangle with corners in the set. The corners of an optimal triangle are vertices of the polygon, so the brute force tries $\binom{n}{3}$ triples, and a two-pointer walk needs only $O(n^2)$ time. Linear-time algorithms exist (Chandran and Mount 1992, Kallus 2017, Jin 2017), but the classical "linear" algorithm of Dobkin and Snyder from 1979 was shown to be wrong in 2017, which makes the problem a lesson in how easy it is to trust a plausible walk.

## In plain words

You have a convex shape with straight sides, and you want to cut the biggest possible triangle out of it. The corners of the best triangle always sit on corners of the shape, because moving a corner of the triangle toward the far side only makes it bigger.

Trying every three corners is slow. A better way picks the first corner, then slides the other two forward around the shape, and each of them moves only forward. This tries every useful triangle with that first corner in one pass. Faster methods move all three corners together, but some of these methods look right and still miss the best triangle on certain shapes.

## Definition

Notation: $P$ is a convex polygon with vertices $p_0, \ldots, p_{n-1}$ in counterclockwise order, no three collinear, $n \ge 3$; a point is $p = (x, y)$; $\mathrm{orient}(p, q, r)$ is the sign of $(q - p) \times (r - p)$, and the [oriented area](/oriented-triangle-area/) of the triangle $pqr$ is $\frac{1}{2}(q - p) \times (r - p)$.

**Input.** The vertices of $P$ in counterclockwise order.

**Output.** Indices $i, j, k$ that maximize the area $\frac{1}{2}|(p_j - p_i) \times (p_k - p_i)|$ over all triangles contained in $P$, and the area.

**Theorem 1 (vertices suffice).** Some largest triangle in $P$ has its corners at vertices of $P$. *Proof.* Fix two corners $a, b$. The area of $abc$ is $\frac{1}{2}|(b - a) \times (c - a)|$, the absolute value of an affine function of $c$, hence convex in $c$. A convex function on the polygon $P = \operatorname{conv}\{p_k\}$ attains its maximum at a vertex. Replace each corner in turn by such a vertex; the area never decreases. $\square$

So for a finite point set the answer is a triangle on its [convex hull](/convex-hull/) vertices, and with integer coordinates twice the area is an integer.

**Theorem 2 (unimodality for a fixed side).** For fixed $i$ and $j$, the distance of $p_k$ from the line $p_i p_j$, as $k$ runs from $j + 1$ to $i - 1$ around the polygon, increases and then decreases (with at most one tie at the top, when an edge is parallel to $p_i p_j$). *Proof.* The difference of consecutive values has the sign of $(p_j - p_i) \times (p_{k+1} - p_k)$. The edge directions $p_{k+1} - p_k$ turn counterclockwise monotonically through less than a full turn on this chain, so this sign changes at most once, from positive to negative. $\square$

## Variants

- **Largest $k$-gon.** The largest-area convex $k$-gon with vertices in a set of $n$ points. Boyce, Dobkin, Drysdale and Guibas solve it in $O(kn \log n + n \log n)$ time; matrix searching later removed a log factor from the $kn$ term.
- **Largest perimeter.** The same question with perimeter as the measure; Boyce et al. treat it too.
- **Largest triangle of a point set.** Compute the hull, then solve the polygon version.
- **Smallest enclosing triangle.** The dual problem is the [minimum-area enclosing triangle](/minimum-area-enclosing-triangle/); Chandran and Mount, and Jin, compute both with one method.
- **Smallest triangle.** The smallest-area triangle with corners in a point set is a different problem, with links to 3SUM and to the [Heilbronn triangle problem](/heilbronn-triangle-problem/).

## Examples

**The pentagon** $(0, 0), (4, 0), (5, 3), (3, 5), (0, 4)$ has area 20. Its largest triangles have area 10, for example $(0, 0), (4, 0), (3, 5)$ and $(0, 0), (5, 3), (0, 4)$; no triple of vertices does better.

**The hexagon** $(0, 0), (4, 0), (6, 2), (6, 4), (2, 4), (0, 2)$ has area 20, and its largest triangles have area 10: $(0, 0), (6, 2), (2, 4)$ and $(4, 0), (6, 4), (0, 2)$.

**The diameter is not always a side.** For the pentagon $(0, 10), (1, 2), (8, 0), (10, 4), (7, 6)$ of area 54, the farthest pair is $(0, 10)$ and $(8, 0)$, at squared distance 164. The best triangle that uses this pair has area 27, with $(1, 2)$. The largest triangle is $(0, 10), (1, 2), (10, 4)$ with area 37, and it does not use the diameter. A heuristic that starts from the farthest pair misses it.

## Known algorithms

| algorithm | time | status |
|---|---|---|
| all triples | $\Theta(n^3)$ | correct |
| fix $p_i$, walk $j$ and $k$ forward (Theorem 2) | $O(n^2)$ | correct |
| Dobkin and Snyder (1979) | $O(n)$ claimed | wrong: Keikha, Löffler, Mohades, Urhausen and van der Hoog (2017) give a counterexample |
| Boyce, Dobkin, Drysdale and Guibas (1985) | $O(n \log n)$ for $k = 3$ | correct |
| Keikha et al. (2017) | $O(n \log n)$ by divide and conquer | correct |
| Chandran and Mount (1992) | $O(n)$ | correct; it also gives the smallest enclosing triangle |
| Kallus (2017), Jin (2017) | $O(n)$ | correct |

The quadratic walk. For each $i$, let $k$ start at $i + 2$. For $j = i + 1, i + 2, \ldots$, move $k$ forward while the next vertex is farther from the line $p_i p_j$, that is while $(p_j - p_i) \times (p_{k+1} - p_k) > 0$, and record the area of $p_i p_j p_k$. By Theorem 2, $p_k$ is then the farthest vertex from the line, and when $j$ moves forward the farthest vertex can only move forward too, so $k$ makes one pass. Each $i$ costs $O(n)$, and all comparisons use exact integer cross products.

The failure of Dobkin and Snyder. Their walk moves all three corners forward in one pass. Keikha et al. give a convex polygon on which it returns a triangle that is not the largest, and they show that the same method also fails for the largest quadrilateral.

## Bounds

- **Upper bound.** $O(n)$ for a convex polygon (Chandran and Mount; Kallus; Jin), so $O(n \log n)$ for a point set by the hull first.
- **Lower bound.** Every vertex must be read, so $\Omega(n)$ for a convex polygon. The linear algorithms are optimal.
- **Size of the answer.** For a convex polygon, the largest inscribed triangle has at least a fixed fraction of the polygon's area; both examples above reach exactly half.

## Reductions

- **To a point set problem.** Theorem 1 reduces the continuous problem to the vertices.
- **To antipodal walks.** For a fixed side $p_i p_j$, the best third corner is the vertex antipodal to the direction of $p_i p_j$, which is the [antipodal pair](/antipodal-pairs/) and [rotating calipers](/rotating-calipers/) idea.

## Applications

- **Shape approximation.** The largest inscribed triangle or $k$-gon is a simple inner model of a convex shape, used in image analysis and in collision tests.
- **Sampling and statistics.** The largest triangle of a sample is a measure of spread, and its expected size for random points is studied in geometric probability.
- **Algorithm testing.** The failure of the 1979 algorithm is a standard example for testing geometric code against a brute force on random convex polygons.

## References
