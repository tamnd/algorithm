---
tag: 8Y4Y9J
kind: problem
slug: minimum-width-annulus
name: Minimum width annulus
aliases:
- minimum-width ring
- minimum zone circle
- roundness problem
area: geometry/geometric-optimization
level: advanced
summary: Find the thinnest annulus, the region between two concentric circles, that contains a point set. It measures roundness; exact algorithms are near n^(3/2).
prereqs: [voronoi-diagram, farthest-point-voronoi-diagram, minimum-enclosing-circle]
see_also: [polygon-width, minimum-enclosing-circle, parametric-search, megiddo-fixed-dimension-lp, lp-type-problem, coreset, chans-randomized-optimization, minimum-area-enclosing-triangle]
sources:
  - paper: "Hiroshi Ebara, Noriyuki Fukuyama, Hiroshi Nakano and Yasuhiro Nakanishi, Roundness algorithms using the Voronoi diagrams, 1st Canadian Conference on Computational Geometry, 1989"
    locator: the characterization of optimal centers by the nearest and farthest point Voronoi diagrams, and the O(n^2) algorithm by their overlay
  - paper: "Pankaj K. Agarwal, Micha Sharir and Sivan Toledo, Applications of parametric searching in geometric optimization, Journal of Algorithms 17(3), 1994"
    locator: the minimum width annulus in O(n^(8/5+ε)) time by parametric search
  - paper: "Pankaj K. Agarwal and Micha Sharir, Efficient randomized algorithms for some geometric optimization problems, Discrete and Computational Geometry 16(4), 1996"
    locator: the minimum width annulus in O(n^(3/2+ε)) expected time
  - paper: doi:10.1145/1008731.1008736
    title: "Approximating extent measures of points"
    locator: the (1+ε)-approximation of the minimum width spherical shell by linearization and ε-kernels
  - book: isbn:9783540779735
    title: "Computational Geometry: Algorithms and Applications, 3rd edition"
    locator: Chapter 7, nearest and farthest point Voronoi diagrams
---

The minimum width annulus problem asks for two concentric circles, with radii $r \le R$, such that every input point lies between them and the width $R - r$ is as small as possible. It is the standard measure of *roundness* in metrology: a machined part is round to within $R - r$ if its probed boundary points fit in such an annulus, the *minimum zone circle*. The optimal center is a vertex of the [Voronoi diagram](/voronoi-diagram/), a vertex of the [farthest point Voronoi diagram](/farthest-point-voronoi-diagram/), or a crossing of an edge of each, which gives an $O(n^2)$ algorithm (Ebara et al. 1989). [Parametric search](/parametric-search/) and randomization lowered the time to $O(n^{8/5+\varepsilon})$ and then $O(n^{3/2+\varepsilon})$ expected (Agarwal, Sharir and Toledo 1994; Agarwal and Sharir 1996). Unlike the [minimum enclosing circle](/minimum-enclosing-circle/), the problem is not convex.

## In plain words

You have measured many points on the rim of a part that should be a perfect circle. You want to know how far from round it is.

Draw two circles with the same center, one inside the other, so that every point lies in the ring between them. The narrower the ring, the rounder the part. The task is to find the narrowest such ring.

The center is not simply the middle of the points. Moving the center can make the outer circle shrink faster than the inner one, and the best place is where the two circles each touch enough points that no move helps. That happens at special points found from two maps: one of nearest points and one of farthest points.

## Definition

Notation: $P$ is a set of $n$ points in the plane. For a center $c$, let $r(c) = \min_{p \in P} |p - c|$ and $R(c) = \max_{p \in P} |p - c|$. The annulus with center $c$ and radii $r \le R$ is $\{x : r \le |x - c| \le R\}$, and its width is $R - r$.

**Input.** $P$, with $n \ge 1$.

**Output.** A center $c^*$ that minimizes $w(c) = R(c) - r(c)$, and the width $w^* = w(c^*)$.

**Characterization.** In general position, at an optimal finite center at least four points lie on the two circles, in one of three patterns:

1. three on the outer circle and one on the inner; then $c^*$ is a vertex of the farthest point Voronoi diagram;
2. one on the outer circle and three on the inner; then $c^*$ is a vertex of the nearest point Voronoi diagram;
3. two on each; then $c^*$ is a crossing of an edge of the nearest point diagram with an edge of the farthest point diagram.

So the optimum is among $O(n^2)$ candidate centers, and on each face of the overlay of the two diagrams the nearest and the farthest point are fixed.

**Degeneracies.** The infimum need not be attained. As the center moves to infinity in a direction $u$, the annulus tends to a strip perpendicular to $u$, and $w(c)$ tends to the extent of $P$ in direction $u$. So $\inf w \le$ the [width](/polygon-width/) of $P$. For three collinear points $(-1,0), (0,0), (1,0)$, the center $(0, y)$ gives width $\sqrt{1 + y^2} - |y|$, which tends to 0 but is never 0. Implementations must report this case, the best strip, as a limit. If all points lie on one circle, $w^* = 0$. Degenerate inputs can put more than four points on the two circles, as in the second example below.

The problem is not convex: $R$ is convex in $c$, but $r$ is not concave, and $w$ can have several local minima.

## Variants

- **Minimum area annulus.** Minimize $\pi(R^2 - r^2)$ instead. This is a linear program in four variables, so it takes $O(n)$ time; see Reductions.
- **Fixed center.** With $c$ given, $w(c)$ is computed in $O(n)$ time.
- **Fixed inner or outer radius.** Fit a ring of given width, or test if one exists: the decision version used by parametric search.
- **Spherical shells.** The same problem in $\mathbb{R}^d$, with two concentric spheres.
- **Approximation.** A $(1+\varepsilon)$-approximation of the width via [coresets](/coreset/) for extent measures (Agarwal, Har-Peled and Varadarajan 2004).
- **Least squares circle.** Metrology also uses the circle that minimizes the sum of squared radial errors, and the minimum circumscribed and maximum inscribed circles. These give different centers and are not the minimum zone.

## Examples

| points | optimal center | $r$ | $R$ | $w^*$ |
|---|---|---|---|---|
| $(\pm 1, 0), (0, \pm 2)$ | $(0, 0)$ | 1 | 2 | 1 |
| $(\pm 5, 0), (0, \pm 5), (3, 0), (0, 3)$ | $(-1, -1)$ | $\sqrt{17}$ | $\sqrt{37}$ | $\sqrt{37} - \sqrt{17} \approx 1.960$ |
| $(-1, 0), (0, 0), (1, 0)$ | none | | | infimum 0 |

**Four points, pattern 3.** For $(\pm 1, 0), (0, \pm 2)$ and a center $c = (x, y)$: $R^2 \ge |c|^2 + 4 + 4|y|$ and $r^2 \le |c|^2 + 1 - 2|x|$. Also $R + r \le 2|c| + 3 \le 3 + 2|x| + 2|y|$. Hence $R - r = (R^2 - r^2)/(R + r) \ge (3 + 2|x| + 4|y|)/(3 + 2|x| + 2|y|) \ge 1$, with equality only at $c = 0$. The two points $(\pm 1, 0)$ lie on the inner circle and $(0, \pm 2)$ on the outer.

**The obvious center is not optimal.** The six points $(\pm 5, 0), (0, \pm 5), (3, 0), (0, 3)$ fit in the annulus centered at the origin with radii 3 and 5, of width 2. The center $(-1, -1)$ is at distance $\sqrt{37}$ from $(5, 0)$ and $(0, 5)$ and at distance $\sqrt{17}$ from the other four points, so it gives width $\sqrt{37} - \sqrt{17} \approx 1.960 < 2$. This is a degenerate case: two points lie on the outer circle and four on the inner circle. An exhaustive check of all $O(n^2)$ candidate centers confirms it is optimal.

## Known algorithms

| algorithm | time | idea |
|---|---|---|
| candidates, each evaluated directly | $O(n^3)$ | all circumcenters of triples and all crossings of two bisectors |
| Ebara, Fukuyama, Nakano and Nakanishi (1989) | $O(n^2)$ | overlay of the nearest and farthest point Voronoi diagrams; each candidate costs $O(1)$ |
| Agarwal, Sharir and Toledo (1994) | $O(n^{8/5+\varepsilon})$ | parametric search over the decision problem |
| Agarwal and Sharir (1996) | $O(n^{3/2+\varepsilon})$ expected | randomized divide and conquer over the decision problem |
| Agarwal, Har-Peled and Varadarajan (2004) | $O(n + 1/\varepsilon^{O(1)})$ | $(1+\varepsilon)$-approximation by linearization and a coreset |

The $O(n^2)$ algorithm builds both Voronoi diagrams in $O(n \log n)$ time, then walks the overlay. Each overlay face has a fixed nearest point $q$ and farthest point $p$, so $w(c) = |c - p| - |c - q|$ there. The overlay can have quadratic size, so subquadratic algorithms avoid building it.

## Bounds

- **Upper.** $O(n^{3/2+\varepsilon})$ expected time for any fixed $\varepsilon > 0$. No near linear exact algorithm is known.
- **Lower.** $\Omega(n)$ trivially, since every point must be read. No better lower bound is stated in the sources above.
- **Candidates.** The nearest and farthest point Voronoi diagrams have $O(n)$ edges each, and two straight edges cross at most once, so there are $O(n^2)$ candidate centers.
- **Against the strip.** $w^* \le$ the width of $P$, the limit of annuli with far centers.

## Reductions

- **Minimum area annulus to linear programming.** Write $u = r^2 - |c|^2$ and $v = R^2 - |c|^2$. The condition $r^2 \le |p - c|^2 \le R^2$ becomes $u \le |p|^2 - 2 p \cdot c \le v$, which is linear in $(c, u, v)$, and the area is $\pi(v - u)$. So the minimum area annulus is a linear program in four variables with $2n$ constraints, solved in $O(n)$ time by [Megiddo's algorithm](/megiddo-fixed-dimension-lp/) or [Seidel's algorithm](/seidel-linear-programming/). At the optimum $u = \min_p (|p|^2 - 2p \cdot c)$, so $r^2 = \min_p |p - c|^2 \ge 0$ holds by itself.
- **Width to area.** For the width this trick fails: $R - r = (R^2 - r^2)/(R + r)$, and the denominator depends on the center. That is why the width version is harder.
- **To the decision problem.** Deciding if $w^* \le \delta$ is the core of [parametric search](/parametric-search/) and of [Chan's randomized optimization](/chans-randomized-optimization/).
- **To extent measures.** Lifting $p \mapsto (p, |p|^2)$ turns circles into planes, so the annulus width becomes a function of a few linear functions, which is what the coreset method approximates.

## Applications

- **Roundness in metrology.** The ANSI and ISO definition of roundness error uses the minimum zone annulus of the measured profile.
- **Circle fitting.** The minimax fit of a circle to noisy points, robust to the worst point.
- **Quality control.** Testing shafts, bearings and holes produced by machine tools.
- **Shape matching.** A measure of how well a curve or point cloud fits a circular arc.

## References
