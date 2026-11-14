---
tag: MJFVD0
kind: algorithm
slug: offset-trimming
name: Offset trimming
aliases:
- offset self-intersection removal
area: cad/surface-interrogation-and-design
level: advanced
summary: Removes the loops of an offset curve, where the distance exceeds the radius of curvature or distant parts come close, by cutting it at its self-intersections and keeping the parts at full distance.
solves: [curve-offsetting]
model: real-ram
complexity:
  vars: {m: the number of samples of the offset, n: the number of control points, K: the number of segment pairs whose x ranges overlap, I: the number of crossings}
  time: {worst: Θ(m log m + K + (I + 1) n), best: Θ(m log m + n)}
  space: {extra: Θ(m + I)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1996
  people: [In-Kwon Lee, Myung-Soo Kim, Gershon Elber]
  note: Lee, Kim and Elber approximated planar offsets by polygons and removed their self-intersections with a plane sweep, the scheme of this page. Distance tests to classify the pieces are older and common to many offset methods.
prereqs: [offset-curve, b-spline, orientation-test]
see_also: [curve-offsetting, bentley-ottmann-algorithm, all-segment-intersections, catastrophic-cancellation, de-boor-algorithm, medial-axis, pocket-machining, offset-surface]
sources:
  - paper: "In-Kwon Lee, Myung-Soo Kim and Gershon Elber, Planar curve offset based on circle approximation, Computer-Aided Design 28(8), 617 to 630, 1996"
    title: Lee, Kim and Elber 1996
    locator: the polygonal approximation of the offset and the removal of its self-intersections by a plane sweep
  - paper: "Joon-Kyung Seong, Gershon Elber and Myung-Soo Kim, Trimming local and global self-intersections in offset curves/surfaces using distance maps, Computer-Aided Design 38(3), 183 to 193, 2006"
    title: Seong, Elber and Kim 2006
    locator: the distinction of local and global self-intersections, and the trimming of the parts that are closer than the offset distance
  - paper: "Takashi Maekawa, An overview of offset curves and surfaces, Computer-Aided Design 31(3), 165 to 173, 1999"
    title: Maekawa 1999
    locator: the survey of offset methods, including the detection and removal of local and global self-intersections
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 2, Line Segment Intersection (the plane sweep and its O((n + I) log n) bound)
  - book: isbn:9780132125895
    title: Manfredo P. do Carmo, Differential Geometry of Curves and Surfaces, Prentice-Hall, 1976
    locator: Section 1-7, global properties of plane curves (simple closed curves, positive orientation and the interior on the left)
---

Offset trimming turns the raw offset of a curve, the point set $C + dN$, into the curve that is really at distance $|d|$ from $C$. Where $d$ is larger than the radius of curvature on the concave side, the raw offset has cusps and small loops, the swallowtails, and where two distant parts of $C$ come closer than $2|d|$, the two offsets cross. In both cases some parts of the raw offset are closer to $C$ than $|d|$. The algorithm samples the raw offset as a polyline, finds all its self-crossings with a sweep and exact orientation tests, cuts it at the crossings, and keeps the pieces whose middle point is at distance $|d|$ from $C$. It is the trimming step of [curve offsetting](/curve-offsetting/), and the core of tool path computation for pockets.

The model is the [real RAM](/real-ram/) for the geometry. The crossing tests are decided exactly on the floating point samples, in rational arithmetic; the distances are computed in floating point and compared with a tolerance.

## In plain words

Roll a coin of radius $|d|$ along the inside of a closed wire, always touching it, and mark where its center goes. Most of the time the center draws a clean curve parallel to the wire. But where the wire bends more sharply than the coin, the coin cannot fit into the corner, and the naive rule "go a distance $|d|$ straight in from the wire" makes the mark run backwards in a little loop. Where the wire pinches into a narrow neck, the marks from the two sides pass each other. In both places, the marks that went too far are closer to the wire than the coin's radius, so the coin could never have been there. The algorithm draws all the naive marks, finds where the drawing crosses itself, cuts it there, and throws away every piece whose middle is too close to the wire.

## The problem

The input is a closed planar curve $C$, here a closed uniform cubic [B-spline](/b-spline/) with control points $P_0, \dots, P_{n-1}$ and parameter $t \in [0, n)$, a signed distance $d \ne 0$, a number of samples $m$ and a tolerance. This page uses the left unit normal $N$, which points into the interior of a counterclockwise curve, and the signed curvature $\kappa$, positive where the curve turns left. So $d > 0$ offsets a counterclockwise curve inward. The mean curvature $H$ of surfaces does not appear.

The raw offset is $\gamma(t) = C(t) + d N(t)$; see [offset curve](/offset-curve/). It satisfies $\gamma' = (1 - d\kappa) C'$, so it has a cusp where $d \kappa = 1$ and runs backwards where $d \kappa > 1$. The *trimmed offset* is the set of points of $\gamma$ at distance exactly $|d|$ from $C$:

$$O_d = \{\gamma(t) : \operatorname{dist}(\gamma(t), C) = |d|\}.$$

The output is the pieces of the sampled offset, each marked kept or removed, such that the kept pieces approximate $O_d$. For a closed curve, $O_d$ is the boundary of the region shrunk or grown by $|d|$, the boundary of a [Minkowski sum](/minkowski-sum/) or difference with a disc.

## The algorithm

```pseudo id=main
OFFSET-TRIM(P_0, ..., P_(n−1), d, m, tol)
L1  q_k ← C(t_k) + d N(t_k) for t_k = k n / m, k = 0, ..., m − 1        ▷ de Boor for C and C'
L2  X ← the pairs of non-adjacent segments of the closed polyline q that meet   ▷ sweep in x, exact tests
L3  for each pair (i, j) in X do
L4      add the meeting point as a cut on segment i and as a cut on segment j
L5  sort the cuts along the polyline
L6  for each piece between two consecutive cuts, cyclically, do
L7      u ← the middle parameter of the piece;  δ ← dist(γ(u), C)
L8      keep ← (δ ≥ |d| − tol)
L9      output the piece and keep
L10 return the pieces
```

**Sampling (line L1).** The [de Boor algorithm](/de-boor-algorithm/) gives $C(t)$, and $C'(t)$ is the quadratic B-spline with control points $P_j - P_{j-1}$ on the same knots. The normal is $N = (-y', x')/|C'|$.

**Crossings (line L2).** Sort the $m$ segments by their least $x$ coordinate and sweep from left to right. Keep an active list of the segments whose $x$ range reaches the current one, drop the ones that end before it, and test the new segment against the rest. The test is the [orientation test](/orientation-test/): segments $ab$ and $ce$ meet if and only if $\operatorname{orient}(a, b, c)\operatorname{orient}(a, b, e) \le 0$ and $\operatorname{orient}(c, e, a)\operatorname{orient}(c, e, b) \le 0$. Each sign is computed in exact rational arithmetic from the floating point coordinates, because near a crossing of almost parallel branches the cross product is a difference of nearly equal numbers, and a floating point sign can be wrong by [catastrophic cancellation](/catastrophic-cancellation/). A wrong sign here loses a crossing, and a lost crossing merges a kept piece with a removed one. Two collinear overlapping segments, or two adjacent segments that fold back on each other, are reported as degenerate input; another $m$ avoids them.

**Cutting (lines L3 to L5).** For a crossing of segments $i$ and $j$, the exact ratios $\lambda$ and $\mu$ of the meeting point along both segments are rationals, and the point is computed once and used for both cuts, so the pieces that meet there share the same end point. Sorting the cuts by (segment, ratio) orders them along the polyline.

**Classifying (lines L6 to L8).** For each piece, line L7 evaluates the exact offset $\gamma$ at the middle parameter, not the polyline, and computes its distance to $C$ by dense sampling of $C$ and Newton steps on $(C(s) - p) \cdot C'(s) = 0$ at the local minima. The piece is kept when this distance is $|d|$ up to the tolerance; removed pieces are at a distance clearly less than $|d|$.

## Example

Take the closed uniform cubic B-spline with the eight control points

$$(-3, -1.5),\ (-1, -0.4),\ (1, -0.4),\ (3, -1.5),\ (3, 1.5),\ (1, 0.4),\ (-1, 0.4),\ (-3, 1.5),$$

a counterclockwise dumbbell with two lobes and a neck. At the middle of the neck, $x = 0$, the curve is at $y = \pm 107/240 \approx \pm 0.4458$, so the neck is $0.8917$ wide. The curvature is largest, about $2.3975$, at the four corners of the lobes, where the radius of curvature is about $0.4171$. Offset inward by $d = 0.5$ with $m = 400$ samples.

Since $0.5 > 0.4171$, the raw offset has a swallowtail at each of the four corners, with its crossing at $(\pm 2.3308, \pm 0.4404)$. Since $0.5$ is more than half the neck, the offsets of the top and the bottom cross at $(\pm 0.6688, 0)$. The sweep finds these $6$ crossings, the same $6$ that the brute force test of all pairs finds, and the cuts give $12$ pieces:

| pieces | length each | distance of the middle point to $C$ | decision |
|---|---|---|---|
| 4 swallowtail loops | $0.0698$ | $0.4938$ | removed |
| 2 pieces across the neck | $1.3435$ | $0.3917$ | removed |
| 2 end pieces, at $(\pm 2.4167, 0)$ | $0.9055$ | $0.5000$ | kept |
| 4 side pieces | $1.7238$ | $0.5000$ | kept |

The piece across the neck has its middle at $(0, 0.0542)$: it is the bottom offset, $0.5$ above the bottom at $y = -0.4458$, and it is only $0.4458 - 0.0542 = 0.3917$ below the top. The six kept pieces close up into two loops, one in each lobe, with total length $8.7062$. So the inward offset of the dumbbell at this distance has two components, as the region shrunk by a disc of radius $0.5$ falls apart at the neck.

## Correctness

The proof file below has two parts.

Part A is exact and about the polyline. The orientation test with exact signs decides whether two segments meet. The sweep reports exactly the pairs of non-adjacent segments that meet: if two segments meet, their $x$ ranges overlap, so the earlier one is still active when the later one starts. After cutting at all reported points, two pieces share a point only at a cut.

Part B is about the exact offset $\gamma$ of a simple closed $C^3$ curve, and it is the reason a single test point per piece is enough. Let $f(t) = \operatorname{dist}(\gamma(t), C) - |d| \le 0$. Assume that $|d|$ is not the radius of curvature at a vertex of $C$. Then every point where $f$ changes from $0$ to negative is a self-intersection of $\gamma$. The proof looks at the disc of radius $|d|$ about the point: if it touches $C$ twice, both contacts are on the offset side by the Jordan curve theorem, which makes the point a double point of $\gamma$; if it touches once, the second and third derivatives of the squared distance show that $f$ stays $0$ nearby. So on each arc between consecutive self-intersections, $f$ is identically $0$ or negative throughout.

The two parts meet in the sampling: the crossings of the polyline approximate the self-intersections of $\gamma$, and the decision is taken on $\gamma$ itself. How fine $m$ must be is measured, not proved.

## Complexity

Sampling costs $\Theta(m)$, since each de Boor evaluation of a cubic costs $O(1)$. Sorting costs $\Theta(m \log m)$. The sweep tests each pair of segments whose $x$ ranges overlap once, $K$ pairs, at $O(1)$ each, since the rationals come from floats of bounded size. So line L2 costs $\Theta(m \log m + K)$. For a curve that is long in $x$, $K$ is close to $m$, but for a curve with many segments over the same $x$ range, $K$ can be close to $m^2/2$. With $I$ crossings there are $2I$ pieces, or one, and each distance costs $\Theta(n)$ for the dense sampling of $C$ with a fixed number of samples per span. The total is $\Theta(m \log m + K + (I + 1) n)$, with extra space $\Theta(m + I)$.

The [Bentley-Ottmann algorithm](/bentley-ottmann-algorithm/) finds the $I$ crossings in $O((m + I) \log m)$ time, independent of $K$, and is the better choice for long polylines with many overlapping $x$ ranges. The $x$ sweep of this page is simpler and robust with exact tests, and it is fast for the typical offset, which is made of a few monotone runs.

## Properties

- **Exact topology of the polyline.** All crossing decisions are exact for the sampled points, so the cut set is exactly that of the polyline, with no missed or doubled crossings.
- **Closed output.** For a closed curve, in the generic case two kept and two removed piece ends meet at each crossing, and the kept pieces close up into loops. The number of loops can change with $d$, as in the example.
- **Local and global loops alike.** The algorithm does not need to know whether a crossing comes from a swallowtail or from two distant parts of $C$.
- **Accuracy is the sampling's.** The kept pieces are polylines with vertices on $\gamma$, with the chord error of the sampling. A tangential crossing of two branches, or a swallowtail smaller than the sample spacing, can be missed by the polyline.

## Variants and improvements

- **Exact curve intersection.** Instead of a polyline, approximate the offset by Bézier or B-spline pieces and find their self-intersections by [curve intersection](/curve-intersection/), for example by subdivision. The cut points are then accurate to the tolerance of that method.
- **Local loops first.** The swallowtails lie between pairs of cusps, the parameters where $d\kappa = 1$. Finding these zeros first and cutting each swallowtail directly removes the local loops cheaply, and only global loops need a sweep.
- **Distance maps.** Seong, Elber and Kim compute, for the offset, the squared distance to $C$ as a function of two parameters and trim the parameter ranges where it is less than $d^2$. This avoids the sampling of the self-intersections.
- **Voronoi diagrams and the medial axis.** For lines and arcs, all trimmed offsets of a region can be read off the [medial axis](/medial-axis/), and no trimming is needed.
- **Surfaces.** The [offset surface](/offset-surface/) has self-intersection curves instead of points, and trimming removes regions of the parameter domain; the classification by a distance test is the same.
- **Bentley-Ottmann.** Replace the $x$ sweep by the [Bentley-Ottmann algorithm](/bentley-ottmann-algorithm/) for an output sensitive bound.

## When to use it

Use it whenever an offset is computed by moving points along the normal and the distance can exceed a radius of curvature, or the curve has narrow regions: tool paths for [pocket machining](/pocket-machining/) and contour milling, the shelling of a profile, and the outlines of wide strokes. For an open curve, the same scheme works, but more cuts are needed, because a point of the offset can also come close to the end points of $C$ or to the offset on the other side; add the circles around the end points and the opposite offset to the crossing search.

## Pitfalls

- **Floating point signs.** At a nearly tangential crossing, a floating point orientation test can report no crossing, and then a kept and a removed part become one piece, and the test point decides both. Use exact or adaptive signs.
- **Classifying by the polyline.** The middle point of a chord is not on $\gamma$, and its distance to $C$ differs from $|d|$ by the chord error, which can exceed a small tolerance. Evaluate $\gamma$ at the middle parameter.
- **A local distance search.** A Newton step from the foot point of the same parameter always finds the distance $|d|$, because $C(u)$ is at distance $|d|$ from $\gamma(u)$. The distance must be global, over all of $C$.
- **Tolerance.** With a tolerance that is too large, the end parts of a swallowtail, which are only slightly closer than $|d|$, are kept. With one that is too small, rounding removes valid pieces.
- **Too few samples.** A swallowtail or a neck crossing smaller than the sample spacing is invisible. Sample more densely where $d\kappa$ is near $1$.
- **Degenerate sampling.** Collinear overlapping segments, which can occur with straight parts of $C$, have no single crossing point. The implementation rejects them; perturbing $m$ resolves them.

## Implementations

The Python file in this folder has `offset_trimming(points, d, m)`, which returns the sampled offset, the crossing pairs and the pieces with their marks, together with the de Boor evaluation of the curve and its derivative, the exact segment test and the distance to the curve. The tests compare the sweep with a brute force test of all pairs of segments, which solves the two line equations in exact fractions, on random polylines, on integer grids with touching and collinear cases, and on offsets. They check the de Boor evaluation against the basis functions, the worked example, that sampled points of kept pieces are at distance $|d|$ and points of removed pieces closer by a dense brute force distance, that kept pieces do not cross and close up into loops, and two cases where nothing or everything is removed.

## History

Offsets with loops appeared as soon as offsets were computed for numerically controlled machining. Lee, Kim and Elber approximated planar offsets by polygons and removed their self-intersections with a plane sweep in 1996. Maekawa surveyed offset curves and surfaces, including their self-intersections, in 1999. Seong, Elber and Kim treated local and global self-intersections of curves and surfaces together with distance maps in 2006.

## References
