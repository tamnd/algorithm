---
tag: YBB4K3
kind: algorithm
slug: metro-mesh-comparison
name: Metro mesh comparison
aliases:
- Metro tool
- mesh Hausdorff error
area: cad/mesh-processing
level: core
summary: Cignoni, Rocchini and Scopigno's estimate of the one-sided and symmetric Hausdorff and mean distances between two meshes by sampling one surface.
model: real-ram
complexity:
  vars: {S: the number of samples, F: the number of triangles of the other mesh, C: the number of grid cells}
  time: {brute_force: O(S F), grid_worst: O(S F)}
  space: {grid: O(F + C)}
properties: {deterministic: false, recursive: false, exact: false}
history:
  year: 1998
  people: [Paolo Cignoni, Claudio Rocchini, Roberto Scopigno]
  note: Cignoni, Rocchini and Scopigno released Metro in 1998 to measure the error of simplified meshes by sampling one surface and querying distances to the other with a uniform grid.
prereqs: [hausdorff-distance, uniform-grid]
see_also: [mesh-simplification, quadric-error-metrics, chamfer-distance, monte-carlo-integration, stratified-sampling, isotropic-remeshing, catastrophic-cancellation, geometric-robustness-problem]
sources:
  - paper: doi:10.1111/1467-8659.00236
    title: Paolo Cignoni, Claudio Rocchini and Roberto Scopigno, Metro, measuring error on simplified surfaces, Computer Graphics Forum 17(2), 1998, 167 to 174
    locator: the one-sided and symmetric Hausdorff distance, the mean error, the sampling of the first surface (similar-triangle subdivision, Monte Carlo, scan conversion), and the uniform grid for distance queries
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 7, Simplification and Approximation (the error metrics of simplification; general locator)
---

Metro is the standard way to say how far apart two triangle meshes are, for example a mesh and its simplified copy. It samples the surface of one mesh, finds for each sample the nearest point of the other mesh, and reports the largest of these distances, an estimate of the one-sided [Hausdorff distance](/hausdorff-distance/), with their mean and root mean square. It does the same in the other direction, and the larger of the two maxima estimates the symmetric Hausdorff distance. Paolo Cignoni, Claudio Rocchini and Roberto Scopigno released it in 1998 as a tool to compare [mesh simplification](/mesh-simplification/) methods. The estimate is never too large, and it is too small by at most the spacing of the samples.

## In plain words

Two meshes describe nearly the same shape, and you want to know how much they differ. Put many points on the first surface. For each point, measure how far it is to the second surface. The largest of these distances tells you the worst place, and the average tells you the typical error.

The worst place can be missed if no point lands on it. More points make the miss smaller. A point that is far from the second surface can only be found from the first surface, so the measurement is done in both directions.

## The problem

The input is two triangle meshes $A$ and $B$. The distance of a point $p$ to $B$ is $d(p, B) = \min_{q \in B} |p - q|$. The one-sided Hausdorff distance is $h(A, B) = \max_{p \in A} d(p, B)$, and the symmetric one is $H(A, B) = \max(h(A, B), h(B, A))$. The mean distance is $\frac{1}{|A|}\int_A d(p, B)\, dp$, where $|A|$ is the area of $A$. Metro estimates these numbers. The distance does not depend on the orientation of the faces; the code of the page keeps the usual convention that faces are oriented so that the outward normal follows the right-hand rule, but it does not use it.

## The algorithm

The core step is the exact distance from a point to a triangle. The plane around a triangle splits into seven regions, the three corner regions, the three edge regions and the inside, and the nearest point is the corner, the foot of the perpendicular on the edge, or the projection onto the plane. Six dot products of edge vectors with $p$ minus a corner decide the region, as in the [orientation test](/orientation-test/), and only ring operations and one division follow, so the result is exact for rational input.

For speed, the triangles of $B$ are put into a [uniform grid](/uniform-grid/) of cubic cells: each triangle goes into every cell that meets its bounding box. A query visits rings of cells around the cell of $p$, of growing radius $r$, and stops as soon as the nearest triangle found is at most $r h$ away, where $h$ is the cell size, because every triangle not yet seen is at least that far.

```pseudo id=main
METRO(A, B, k, n)
L1  S ← the vertices of a k × k similar subdivision of each triangle of A, and n random points of A
L2  for each p ∈ S do δ(p)² ← min over triangles T of B near p of |p − CLOSEST-POINT(p, T)|²
L3  h_AB ← max over p ∈ S of δ(p)
L4  mean_AB ← average of δ(p); rms_AB ← square root of the average of δ(p)²
L5  compute h_BA, mean_BA and rms_BA by L1 to L4 with A and B exchanged
L6  return h_AB, h_BA and max(h_AB, h_BA)
```

The random points of L1 are uniform by area: a triangle is chosen with probability proportional to its area, and two uniform numbers $u, v$ in $[0, 1]$ give the point $a + u(b - a) + v(c - a)$, with $(u, v)$ replaced by $(1 - u, 1 - v)$ when $u + v > 1$. This reflection maps the unit square onto the triangle twice, evenly.

**Degenerate cases.** A triangle of zero area has no inside region and the formula divides by zero; the code requires positive area. A sample that lies on $B$ has distance 0. If $A$ and $B$ are the same mesh, all distances are 0. A mesh with no triangles has no defined distance. The grid needs a cell size $h > 0$; a very small $h$ makes many cells and a very large $h$ puts all triangles in one cell, which is the brute-force loop.

## Example

Let $A$ be the unit square in the plane $z = 0$, as two triangles, and $B$ the triangle $(0,0,0)$, $(1,0,0)$, $(0,1,0)$, the lower left half of the square. With $k = 2$, L1 gives the 9 points with coordinates in $\{0, \frac12, 1\}$.

| step | value |
|---|---|
| L2 | the 6 points with $x + y \le 1$ lie on $B$: $\delta = 0$ |
| L2 | $(1, \frac12)$ and $(\frac12, 1)$ are $\frac{1/2}{\sqrt2} \approx 0.354$ from the edge $x + y = 1$ |
| L2 | $(1, 1)$ is $\frac{1}{\sqrt2} \approx 0.707$ from that edge |
| L3 | $h_{AB} = 1/\sqrt2 \approx 0.7071$, the true value, because the farthest corner is a sample |
| L4 | mean $= (2 \cdot 0.354 + 0.707)/9 \approx 0.1571$, rms $\approx 0.2887$ |
| L5 | $B$ lies on $A$, so $h_{BA} = 0$ |
| L6 | the symmetric estimate is $0.7071$ |

The true mean is $\int_0^1 \frac{s}{\sqrt2}(1 - s)\, ds = \frac{1}{6\sqrt2} \approx 0.1179$ and the true rms is $\sqrt{1/24} \approx 0.2041$. The grid points overweight the corner of the square, so their mean is too large. The table compares the two kinds of samples in the code of the page.

| samples | max | mean | rms |
|---|---|---|---|
| subdivision, $k = 2$ (9 points) | 0.7071 | 0.1571 | 0.2887 |
| subdivision, $k = 8$ (81 points) | 0.7071 | 0.1309 | 0.2282 |
| subdivision, $k = 32$ (1089 points) | 0.7071 | 0.1214 | 0.2104 |
| Monte Carlo, 100 points | 0.6555 | 0.1180 | 0.2053 |
| Monte Carlo, 10000 points | 0.7015 | 0.1173 | 0.2033 |
| true value | 0.7071 | 0.1179 | 0.2041 |

The subdivision vertices find the maximum when it is at a vertex, and Monte Carlo points estimate the mean without bias but miss the maximum. Metro uses both kinds for this reason.

**When the arithmetic is floating point.** The code of the page computes every squared distance exactly in rational arithmetic and takes square roots only for the reported numbers. In doubles, the region tests are signs of dot products and the last step divides by a sum that is proportional to the squared area of the triangle. For a sliver of length 2 and width $10^{-15}$, the float distance from a point at distance 0.41 was off by 0.025, a case of [catastrophic cancellation](/catastrophic-cancellation/); for widths down to $10^{-12}$ the float error stayed below $10^{-15}$ in 3000 random queries. Simplified meshes often contain slivers, so a tool that compares them should guard the division, use [exact predicates](/shewchuk-expansion-sum/) for the region tests, or fall back to the three edge distances when the area is tiny. This is the [robustness problem](/geometric-robustness-problem/) of geometry in a mild form: the answer is a measured number, and a wrong region gives a point of the triangle whose distance is close to the true one unless the triangle is nearly degenerate.

## Correctness

Every sample lies on $A$, so its distance to $B$ is at most $h(A, B)$, and the sampled maximum is a lower bound. The distance to $B$ is 1-Lipschitz: moving the point by $\delta$ changes it by at most $\delta$. The worst point of $A$ is within $\delta$ of a sample, where $\delta$ is the largest distance from a point of $A$ to its nearest sample, so the sampled maximum is at least $h(A, B) - \delta$. For the subdivision of each triangle into $k^2$ similar copies, $\delta$ is at most the longest edge of $A$ divided by $k$. The closest-point routine finds the nearest point of a triangle by its Voronoi regions, and the grid search stops only when no unseen triangle can be closer. The full proof is below.

## Complexity

With $S$ samples and $F$ triangles in $B$, the brute-force query costs $O(F)$ per sample and $O(S F)$ in total. The grid takes $O(F + C)$ space for $C$ cells, counting a triangle once per cell it meets. A query on a mesh with evenly sized triangles and a cell size near the triangle size touches $O(1)$ cells and triangles, but in the worst case, for example one long triangle in every cell, it touches all $F$. The subdivision gives about $k^2/2$ samples per triangle, so the sampling error $\delta$ falls like $1/k$ while the cost grows like $k^2$. The Monte Carlo mean has an error that falls like $1/\sqrt n$.

## Properties

- **One-sided lower bound.** The sampled maximum never exceeds the true Hausdorff distance, and it grows when samples are added.
- **Two-sided error bound.** The true value is at most the sampled maximum plus the sample spacing.
- **Not symmetric.** $h(A, B)$ and $h(B, A)$ can be very different, as in the example, where they are 0.707 and 0.
- **Randomized.** The Monte Carlo samples depend on the seed; the subdivision samples do not.
- **Unsigned.** The distance does not say on which side of $B$ the sample lies.

## Variants and improvements

- **Sampling schemes.** The original tool offers similar-triangle subdivision, Monte Carlo sampling and a sampling by scan conversion of each triangle, a form of [stratified sampling](/stratified-sampling/), with a sampling density per unit area.
- **Vertex-only error.** Measuring only at the vertices of $A$ is cheap but misses the error in the middle of large triangles, which is where a simplified mesh is far from the original.
- **MESH.** Aspert, Santa-Cruz and Ebrahimi (2002) gave a similar tool with a different sampling and a grid query.
- **Chamfer distance.** Averaging the nearest distances both ways, instead of taking the maximum, gives the [chamfer distance](/chamfer-distance/), which is common in learning on point sets.
- **Error during simplification.** [Quadric error metrics](/quadric-error-metrics/) bound a different quantity, the sum of squared distances to planes, during the simplification itself; Metro checks the result afterwards.

## When to use it

Use Metro to report the approximation error of a simplified, remeshed or compressed mesh against the original, and to compare methods such as [mesh simplification](/mesh-simplification/) or [isotropic remeshing](/isotropic-remeshing/) fairly. Report both one-sided maxima, the mean and the sampling density. When a guarantee is needed rather than an estimate, add the spacing bound to the maximum, or use an exact algorithm for the Hausdorff distance between triangle meshes.

## Pitfalls

- **Only one direction.** The distance from the simplified mesh to the original is often small while the other direction is large, for example when a thin part has been removed. Always measure both.
- **Too few samples.** The maximum can be missed by up to the sample spacing. State the density.
- **Mean over vertices.** A mean over subdivision vertices is not area-weighted, as the example shows: 0.157 against 0.118.
- **Units.** The values are absolute lengths. Divide by the diagonal of the bounding box to compare meshes of different size, and say so.
- **Slivers in floating point.** Nearly degenerate triangles give wrong distances with doubles, as shown above.

## Implementations

## History

The Hausdorff distance goes back to Felix Hausdorff's 1914 book on set theory. Mesh simplification grew fast in the 1990s, and papers measured their error in different ways, often only at the vertices. Cignoni, Rocchini and Scopigno released Metro in 1998 at the CNR in Pisa as a free tool that made the comparison uniform, with sampling of the first surface, a uniform grid for the distance queries, and a coloured map of the error on the surface. It became the usual way to report the error of simplified meshes. Aspert, Santa-Cruz and Ebrahimi described the similar tool MESH in 2002, and the Metro code later became part of the VCG library and of MeshLab.

## References
