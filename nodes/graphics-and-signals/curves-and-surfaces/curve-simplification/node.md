---
tag: T2CZX3
kind: problem
slug: curve-simplification
name: Curve simplification
aliases:
- line generalization
- curve flattening
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Replace a curve or a dense polyline in the plane or in space by a polyline with fewer points that stays within a distance or area tolerance.
prereqs: [polygon, point-to-segment-distance, parametric-curve]
see_also: [polygon-simplification, ramer-douglas-peucker, visvalingam-whyatt, hausdorff-distance, frechet-distance, de-casteljau-algorithm, mesh-simplification, segmented-least-squares]
sources:
  - paper: doi:10.1016/S0146-664X(72)80017-0
    title: Urs Ramer, An iterative procedure for the polygonal approximation of plane curves, Computer Graphics and Image Processing 1(3), 244-256 (1972)
    locator: polygonal approximation of a plane curve by repeated splitting at the point farthest from the chord
  - paper: doi:10.3138/FM57-6770-U75U-7727
    title: David H. Douglas and Thomas K. Peucker, Algorithms for the reduction of the number of points required to represent a digitized line or its caricature, The Canadian Cartographer 10(2), 112-122 (1973)
    locator: the reduction of digitized map lines with a distance tolerance
  - paper: doi:10.1179/000870493786962263
    title: M. Visvalingam and J. D. Whyatt, Line generalisation by repeated elimination of points, The Cartographic Journal 30(1), 46-51 (1993)
    locator: the effective area tolerance and the ranking of all points by one run
---

Curve simplification replaces a curve by a polyline with fewer points that stays close to it. The input is a dense polyline in the plane or in $\mathbb{R}^d$, such as a GPS track or a digitized map line, or a smooth [parametric curve](/parametric-curve/) that must be drawn with straight segments. The tolerance can be a distance, which bounds how far the output moves from the input, or an area, which bounds the size of the features that are removed. This page covers the curve view: the dimension, the flattening of smooth curves, the hierarchies of levels of detail, and the two kinds of tolerance. The optimal forms for a polyline in the plane, with the shortcut graph and its bounds, are on the [polygon simplification](/polygon-simplification/) page.

## In plain words

A curve on a screen or in a file is a row of points joined by straight pieces. Often there are far more points than you need. A track from a phone can have a point every second, and a smooth curve can be cut into thousands of tiny pieces. You want fewer points, and the line must still look the same.

There are two ways to say "the same". One says that no part of the line may move more than a set distance. The other says that the small bumps you remove must be smaller than a set size. The first is safe for measurement, and the second often looks better. A good method also gives you all levels at once, so that you can show more points when the user zooms in.

## Definition

**Input.** One of these:

- a polyline $P_0, \dots, P_{n-1}$ with points in $\mathbb{R}^d$, open or closed;
- a parametric curve $C : [a, b] \to \mathbb{R}^d$ that you can evaluate, for example a [Bézier curve](/bezier-curve/) of degree $p$ with $p + 1$ control points.

Also a tolerance: a distance $\varepsilon \ge 0$, an area $A \ge 0$, or a budget of $k$ points.

**Output.** A polyline $Q_0, \dots, Q_m$ with the same end points. In the *vertex-restricted* form the $Q_j$ are a subsequence of the $P_i$. For a parametric curve, $Q_j = C(t_j)$ for parameters $a = t_0 < t_1 < \dots < t_m = b$, and the task is called *flattening*.

**Error.** For a distance tolerance, the common measures are:

- *segment error*: each removed point $P_i$ is within $\varepsilon$ of the output segment that replaces it; for a curve, each arc $C([t_j, t_{j+1}])$ is within $\varepsilon$ of the chord $Q_j Q_{j+1}$;
- [Hausdorff distance](/hausdorff-distance/) between the input and the output as point sets;
- [Fréchet distance](/frechet-distance/), which also respects the order along the curve.

The segment error bounds the Hausdorff distance by the same $\varepsilon$, as the [Ramer-Douglas-Peucker](/ramer-douglas-peucker/) proof shows. For an area tolerance, the measure is the *effective area* of a removed point: the area of the triangle that it makes with its neighbors when it is removed. An area has no fixed relation to a distance, so this form has no distance guarantee.

**Goal.** Meet the tolerance with few points. The *min-#* form asks for the fewest points, and the *min-ε* form asks for the least error with $k$ points. The practical methods meet the tolerance but do not minimize the count.

## Variants

- **Distance against area.** A distance tolerance $\varepsilon$ is a length, so it scales by $s$ when the drawing scales by $s$. An area tolerance $A$ scales by $s^2$. A triangle with base $w$ and height $h$ has area $wh/2$, so an area test removes a narrow spike with a small $w$ even when $h$ is large, and keeps a wide flat bump with a small $h$. A distance test does the opposite. Pick the distance form when the error must be bounded, and the area form when small features must go first.
- **Levels of detail.** Instead of one tolerance, rank all points once, and keep the points whose rank is above a threshold. The results for two thresholds are then nested, and one ranking serves every zoom level. See the section on known algorithms for how to rank exactly.
- **Free output points.** The output points can be anywhere, not only input points. This can use fewer points. The problem is then close to the [minimum link path](/minimum-link-path/) through a tube around the curve.
- **Dimension.** Distances to segments and triangle areas exist in every $\mathbb{R}^d$, so the greedy methods work for curves in space and for tracks with time or height as a coordinate. The fast planar methods for the optimal forms use planar geometry and do not carry over as they are.
- **Vertical error.** For a time series, the error is often the vertical distance at each sample, and the problem becomes [segmented least squares](/segmented-least-squares/) or a piecewise linear fit.
- **Several curves.** Map lines that share end points, or that must not cross, need the same simplification of each shared part and a test for crossings.

## Examples

**One polyline, three answers.** Take the 8 points $(0, 0), (2, 1), (4, 0), (6, 3), (8, 1), (10, 6), (12, 5), (14, 7)$. With the segment error and $\varepsilon = 2$, Ramer-Douglas-Peucker keeps 5 points, the indices $0, 3, 4, 5, 7$. The 3 points with indices $0, 2, 7$ also meet the same tolerance, so the greedy answer is not the smallest. If 5 points must stay, the [Visvalingam-Whyatt algorithm](/visvalingam-whyatt/) keeps the indices $0, 2, 4, 5, 7$, so a distance ranking and an area ranking keep different points.

**Area against distance.** The 3 points $(0, 0), (1, 100), (2, 0)$ make a spike of height 100 and area 100. The 3 points $(0, 0), (500, 1), (1000, 0)$ make a bump of height 1 and area 500. A distance tolerance of 10 keeps the spike and removes the bump. An area tolerance of 200 removes the spike and keeps the bump.

**Flattening a quadratic.** The Bézier curve with control points $(0, 0), (1, 2), (2, 0)$ has degree $p = 2$ and 3 control points. Its point at $t = 1/2$ is $(1, 1)$, which is 1 from the chord. The bound below gives $1$ for one piece and $1/m^2$ for $m$ equal pieces in $t$, so $m = 10$ pieces meet $\varepsilon = 0.01$.

## Known algorithms

| Method | Tolerance | Output | Time | Note |
|---|---|---|---|---|
| [Ramer-Douglas-Peucker](/ramer-douglas-peucker/) | distance | subsequence | $\Theta(n^2 d)$ worst, $O(n \log n)$ in the plane with path hulls | Hausdorff bound, not minimal |
| [Visvalingam-Whyatt](/visvalingam-whyatt/) | area | subsequence | $O(n \log n)$ worst | ranks all points, no distance bound |
| Shortcut graph and shortest path | distance | fewest points of a subsequence | $O(n^2)$ in the plane, see [polygon simplification](/polygon-simplification/) | optimal for the segment error |
| Uniform flattening | distance | points $C(t_j)$ | $O(m)$ evaluations | needs a bound on the second derivative |
| Adaptive flattening | distance | points $C(t_j)$ | $m - 1$ splits for $m$ output pieces | uses the [de Casteljau algorithm](/de-casteljau-algorithm/) and a flatness test |

**Exact rankings for levels of detail.** One full run of a greedy method gives a value for each point, and the threshold is then a filter.

- For Ramer-Douglas-Peucker, run with tolerance 0, so that every pair with a point off its segment splits, and give each kept point the least split distance on its path from the first pair. Then the points with value above $\varepsilon$, plus the two ends, are exactly the output for $\varepsilon$. The reason is that the split point of a pair does not depend on $\varepsilon$, and a pair is split for $\varepsilon$ only when all splits above it exceed $\varepsilon$. A random test of 500 integer polylines against direct runs agrees for every tolerance.
- For Visvalingam-Whyatt, run to the end and give each point the running maximum of the removal areas up to its step. The run for $A$ stops at the first area that is not below $A$, so it removes exactly the points with value below $A$.

The raw values do not work in either case: a later split can be farther than its parent, and a later removal can have a smaller area.

**Flattening by a bound.** Let $C$ be a Bézier curve of degree $p$ on $[0, 1]$ with control points $b_0, \dots, b_p$, and let $D = \max_i |b_i - 2 b_{i+1} + b_{i+2}|$. The difference $f(t) = C(t) - ((1 - t) b_0 + t b_p)$ is zero at both ends, and $|f''(t)| \le p (p - 1) D$, because $f''$ is $p(p-1)$ times a convex combination of the second differences. A function that is zero at both ends of $[0, 1]$ satisfies $|f(t)| \le \max |f''| / 8$. So the curve is within $p (p - 1) D / 8$ of its chord. On $m$ equal pieces in $t$, the second differences of each piece are $1/m^2$ times as large, so

$$m = \left\lceil \sqrt{\frac{p (p - 1) D}{8 \varepsilon}} \right\rceil$$

equal pieces meet the segment error $\varepsilon$. The bound is exact for the quadratic example above. A random test on 2000 curves of degree 2 to 5 in $\mathbb{R}^3$ found no deviation above it.

**Adaptive flattening.** If all control points of a piece are within $\varepsilon$ of its chord, the [convex hull property](/convex-hull-property/) puts the whole piece within $\varepsilon$ of that chord. Otherwise split the piece at $t = 1/2$ with the de Casteljau algorithm and test both halves. This uses fewer pieces where the curve is flat, and it works for any curve with a subdivision rule and a convex hull property, such as B-splines.

## Bounds

- **Reading the input.** Every method that guarantees the tolerance for a polyline must read all $n$ points, so $\Omega(n)$ time.
- **Greedy methods.** Ramer-Douglas-Peucker is $\Theta(n^2 d)$ in the worst case, and Hershberger and Snoeyink gave $O(n \log n)$ in the plane. Visvalingam-Whyatt is $O(n \log n)$ with a heap. Both bounds are worst case.
- **Optimal subsequences.** For the segment error in the plane, the fewest points come from a shortest path in the shortcut graph in $O(n^2)$ time. The details and the hardness results for related forms are on the [polygon simplification](/polygon-simplification/) page. In $\mathbb{R}^d$ the direct test of each of the $O(n^2)$ shortcuts costs $O(n d)$, which gives $O(n^3 d)$.
- **Flattening.** The bound above needs $O(\varepsilon^{-1/2})$ pieces in the worst case for a fixed curve. This order is tight for curves that bend: a circle arc of radius $R$ and angle $\theta$ cut into pieces of angle $\varphi$ has the gap $R (1 - \cos(\varphi / 2)) \approx R \varphi^2 / 8$, so it needs about $\theta \sqrt{R / (8 \varepsilon)}$ pieces. For $R = 1$, $\theta = \pi / 2$ and $\varepsilon = 10^{-4}$, the exact count is 56 and the estimate is 55.5.

## Reductions

- **Curve to polyline.** Sample the curve densely, then simplify the polyline. This is simple but can lose thin features between samples. Flattening by a bound avoids the sampling step.
- **Polyline to shortest path.** The min-# form with the segment error reduces to a shortest path in a graph with one vertex per point and one edge per allowed shortcut. See [polygon simplification](/polygon-simplification/).
- **Surfaces.** [Mesh simplification](/mesh-simplification/) is the same problem one dimension up: remove vertices or collapse edges while an error stays small. The Visvalingam-Whyatt pattern, a heap of local costs with updates only near each change, is the same as in edge collapse with quadric errors.
- **Time series.** With the vertical error and a cost per segment, the problem is [segmented least squares](/segmented-least-squares/).

## Applications

- **Maps.** Line generalization of coastlines, rivers and borders for each zoom level, with a ranking computed once and filtered when drawing.
- **Tracks.** Compression of GPS and motion tracks, where a distance bound keeps the track usable for measurement.
- **Vector graphics and fonts.** Renderers flatten Bézier paths into line segments before they fill or stroke them, with a tolerance below one pixel.
- **Machining and plotting.** Tool paths and pen paths need line segments, and a distance bound gives the accuracy of the part.
- **Pen input.** Simplifying a stroke before fitting a smooth curve to it.

## References
