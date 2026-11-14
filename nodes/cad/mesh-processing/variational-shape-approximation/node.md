---
tag: J5DY1Y
kind: algorithm
slug: variational-shape-approximation
name: Variational shape approximation
aliases:
- VSA
- Cohen-Steiner-Alliez-Desbrun approximation
area: cad/mesh-processing
level: advanced
summary: Cohen-Steiner, Alliez and Desbrun's Lloyd-like partition of a mesh into connected regions, each fit by a plane under a normal error, then a coarse polygon mesh from them.
model: real-ram
complexity:
  vars: {n: the number of faces, k: the number of proxies, s: the largest number of rounds for each number of proxies}
  time: {worst: O(k s n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2004
  people: [David Cohen-Steiner, Pierre Alliez, Mathieu Desbrun]
  note: They cast the approximation of a surface by k planes as a clustering of its faces, and solved it with Lloyd's two steps, a flood that keeps the regions connected, and a normal-based error.
prereqs: [mesh-segmentation, lloyds-algorithm, polygon-mesh]
see_also: [k-means, region-growing, mesh-simplification, quadric-error-metrics, isotropic-remeshing, curvature-tensor-estimation, shape-diameter-function]
sources:
  - paper: doi:10.1145/1015706.1015817
    title: David Cohen-Steiner, Pierre Alliez and Mathieu Desbrun, Variational shape approximation, ACM Transactions on Graphics 23(3), 2004, 905 to 914
    locator: the L^2 and L^(2,1) error metrics, the fit of the proxies, the partition by flooding with a priority queue, the insertion of proxies, and the extraction of the coarse mesh from the anchor vertices
  - paper: doi:10.1109/TIT.1982.1056489
    title: S. P. Lloyd, Least squares quantization in PCM, IEEE Transactions on Information Theory 28(2), 1982, 129 to 137
    locator: the alternation between the best representative of each cell and the best cell of each point, and the fact that neither step increases the error
---

Variational shape approximation (VSA) cuts a triangle mesh into $k$ connected regions and fits a plane, the proxy, to each region, so that the faces of each region are nearly parallel to their plane. From the regions it then builds a coarse polygon mesh, with one polygon for each region. Cohen-Steiner, Alliez and Desbrun (2004) cast this as a clustering of the faces and solved it in the style of [Lloyd's algorithm](/lloyds-algorithm/): fit the best proxy to each region, then grow the regions again from the proxies, and repeat. The error of a face $T$ against a proxy with unit normal $N$ is $a_T|n_T - N|^2$, with $a_T$ the area and $n_T$ the unit normal of $T$, and the total over all faces is called the $L^{2,1}$ energy. It depends on the normals and not on the positions, so it follows the shape of the surface and ignores where the plane is. The fit step is optimal, and with one guard on the growth step the energy never increases.

## In plain words

Think of a model made of many tiny triangles, and the job is to describe it with a few large flat pieces. Each flat piece covers a group of triangles that face almost the same way.

Start with one group and one direction. Find the triangle that disagrees most with its group, and start a new group there. Then improve the groups. For each group, find the direction that fits its triangles best. Then let the groups grow again, like ink spreading from one triangle of each group, where each triangle goes to the group whose ink reaches it first. Keep the new groups only if they fit at least as well. Repeat until there are as many groups as you want.

At the end, the corners where three or more groups meet become the corners of the flat pieces.

## The problem

The input is a connected triangle mesh in which each face $T$ has area $a_T > 0$ and unit normal $n_T$, and an integer $k \ge 1$, at most the number of faces. The output is a partition of the faces into at most $k$ connected regions $R_1, \ldots, R_k$ with unit proxy normals $N_1, \ldots, N_k$ of small energy

$$E(R, N) = \sum_{i}\sum_{T \in R_i} a_T\,|n_T - N_i|^2,$$

and a coarse polygon mesh with one polygon for each region. The exact minimum of $E$ over connected partitions is not the target. Like [k-means](/k-means/), the method returns a local optimum.

## The algorithm

```pseudo id=main
VSA(faces with areas a_T and unit normals n_T, k, s)
L1  R ← one region that holds all faces;  N_1 ← the normal of the first face
L2  repeat
L3      for up to s rounds do
L4          for each region i do m ← Σ over T in R_i of a_T n_T;  if m ≠ 0 then N_i ← m / |m|
L5          seed_i ← the face T of R_i with the least error a_T |n_T − N_i|²
L6          R′ ← grow the regions from the seeds, always giving the free face of least error to the region that reached it
L7          if R′ ≠ R and E(R′, N) ≤ E(R, N) then R ← R′ else stop the rounds
L8      fit N again as in L4;  if there are k proxies or E(R, N) = 0 then return R, N
L9      i ← the region with the largest total error;  T ← the face of R_i with the largest error
L10     move T to a new region, with the proxy normal n_T
```

Line L4 is the fit step. The best unit normal of a set of faces is the unit vector along $m = \sum a_T n_T$, because $\sum a_T|n_T - N|^2 = 2A - 2\,m \cdot N$ for unit $N$. On a closed surface the sum $m$ over all faces is 0, so line L4 keeps the old normal when $m = 0$. Lines L5 and L6 are the flood. A priority queue holds entries (error, face, region). Each seed pushes its neighbours with their error to the proxy of its region. The flood pops the entry of least error, and if its face is still free, gives the face that region and pushes the free neighbours of the face. So each region grows through shared edges and stays connected. Line L7 is the guard: the flood is not proved to decrease the energy, and it sometimes increases it, so the new partition is kept only when its energy is not larger. Lines L9 and L10 add proxies one at a time where the error is worst.

**The coarse mesh.** An anchor is a vertex where three or more regions meet. It moves to the mean of its projections to the proxy planes of those regions, where the plane of region $i$ has the normal $N_i$ and passes through the area-weighted centroid of $R_i$. The polygon of a region is the list of the anchors on its border, in order. The code does only this step. The paper also adds anchors on a border between two regions that has too few of them, and splits long polygon edges where the border is far from the straight edge.

## Example

**A box.** Take the surface of the box $2 \times 3 \times 5$, each side cut into a $2 \times 2$ grid of squares and each square into two triangles, 48 faces in total. The area is $A = 62$. With one proxy the energy is $2A = 124$, because the area-weighted normals of a closed surface sum to 0 and so every normal fits equally badly. As proxies are added, the energy goes down:

| $k$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| energy | $124$ | $64$ | $37.94$ | $24$ | $9.69$ | $0$ |

At $k = 6$ the regions are the six sides and the proxy normals are the six axis directions. The anchors are the 8 corners, at their exact positions, and the coarse mesh is the box itself, as 6 rectangles. With a $3 \times 4 \times 5$ grid on the sides the result is the same.

**A sphere.** On the icosphere of radius 1 with 1280 faces, the energy at $k = 6$, $12$ and $24$ is $4.22$, $2.17$ and $1.07$. It halves each time $k$ doubles. At $k = 6$ the coarse mesh has 8 anchors and 6 quadrilaterals, connected like the faces of a cube. At $k = 12$ there are 19 anchors and at $k = 24$ there are 44.

## Correctness

The proof file shows these facts.

- **The fit is optimal.** For a set of faces with total area $A$ and $m = \sum a_T n_T$, the error of a unit normal $N$ is $2A - 2\,m \cdot N \ge 2A - 2|m|$, with equality exactly at $N = m/|m|$, by the Cauchy-Schwarz inequality. So line L4 does not increase the energy.
- **The classic assignment is optimal, the flood is not.** With the proxies fixed, giving each face to its proxy of least error minimizes the energy over all partitions. That is the second step of Lloyd's algorithm, and it can make regions that are not connected. The flood of line L6 keeps the regions connected but is not proved to decrease the energy. In 30 runs from random seeds on perturbed icospheres with 320 faces, 119 of 337 flood steps increased it, by up to 16%.
- **The energy never increases.** The fit does not increase it, the guard of line L7 rejects a flood that would, and an insertion sets the error of the moved face to 0 and changes nothing else.
- **It stops with $k$ connected regions.** On a connected mesh every face gets a region, each region is connected and holds its seed, and an insertion never empties a region. The rounds are bounded by $s$ and there are at most $k - 1$ insertions. If the energy reaches 0 first, the algorithm stops with fewer regions.
- **The box.** A partition of a box into 6 regions has energy 0 exactly when the regions are the 6 sides. From the 6 side normals with one seed on each side, the flood returns the 6 sides, and the anchors are the 8 corners.

The method returns a local optimum, not the partition of least energy. That the full algorithm reaches the six sides on every subdivision of every box is not proved. The tests check it on two subdivisions.

## Complexity

One fit costs $\Theta(n)$ for $n$ faces. One flood pushes each face at most once from each neighbour, so at most $3n$ entries, and costs $O(n \log n)$ with a binary heap. Each insertion costs $\Theta(n)$. With at most $s$ rounds for each of the $k$ numbers of proxies, the time is $O(k s n \log n)$ on the [real RAM](/real-ram/). The extra space is $\Theta(n)$ for the labels, the queue and the face data. On the sphere of the example with $k = 24$, the run made 330 floods, about 14 for each number of proxies.

## Properties

- **Monotone with the guard.** The energy never increases, and the run stops.
- **Connected regions.** Each region is connected through shared edges, unlike plain clustering of the normals.
- **Local optimum.** The result depends on the first face and on the order of the insertions, like any Lloyd-style method.
- **Normal-based.** The $L^{2,1}$ energy does not change when a region moves along its plane or the whole mesh is translated, and it does not change under scaling except by the factor of the areas. It captures how the surface bends, not how far it is from the planes.
- **Deterministic.** With the same mesh, $k$ and tie-breaking, the output is the same.

## Variants and improvements

- **The $L^2$ error.** The squared distance of the surface to the proxy plane, integrated over each face. The best plane of a region passes through its centroid with the normal of least variance, the eigenvector of the smallest eigenvalue of the covariance matrix of the region. It controls the distance but follows the normals less well.
- **Other proxies.** Spheres, cylinders and general quadrics as proxies give coarse models of mechanical parts with curved faces.
- **Proxy deletion and teleportation.** Cohen-Steiner, Alliez and Desbrun also merge two adjacent regions whose union costs little and move a proxy from a region of low error to one of high error, to escape poor local optima.
- **A target error instead of $k$.** Insert proxies until the energy falls below a threshold.
- **Interactive control.** The user can add, remove or move proxies between rounds and see the regions change, because each round is fast.

## When to use it

Use VSA to turn a dense scan or a tessellated model of a mostly flat object, such as a building or a mechanical part, into a few large polygons, for simplification, for reverse engineering, or as a [segmentation](/mesh-segmentation/) into nearly flat patches. For a coarse triangle mesh that stays close in distance, edge collapse with [quadric error metrics](/quadric-error-metrics/) is simpler and faster. For curved organic shapes, where no small number of planes fits well, a segmentation into meaningful parts, for example by the [shape diameter function](/shape-diameter-function/), is the better tool.

## Pitfalls

- **No guard.** Without line L7 the energy can go up between rounds, and the loop can cycle between partitions.
- **The zero sum.** On a closed surface, or on any region whose area-weighted normals cancel, $m = 0$ and $m/|m|$ is undefined. Keep the old normal.
- **A poor start.** Random seeds can leave two proxies on one flat side and none on another. Insert proxies at the worst face, or teleport them.
- **Too few anchors.** A border between two regions that meets no third region, such as the circle between two halves of a cylinder, has no anchor, and its region gives no polygon. Add anchors on such borders.
- **Disconnected meshes.** The flood does not cross between components. Run the method on each component.
- **Units.** The $L^{2,1}$ energy is an area, so a threshold on it must scale with the model.

## Implementations

## History

Lloyd described in 1957, and published in 1982, the alternation between the best representative of each cell and the best cell of each point, for quantization. It became the standard heuristic for [k-means](/k-means/) and for centroidal Voronoi tessellations. In 2004 Cohen-Steiner, Alliez and Desbrun applied it to shape approximation. They clustered the faces of a mesh with planar proxies, introduced the $L^{2,1}$ error on the normals, replaced the assignment step by a flood that keeps each region connected, and built a coarse polygon mesh from the regions. Later work used other proxies, such as spheres, cylinders and quadrics.

## References
