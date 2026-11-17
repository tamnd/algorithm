---
tag: 4CA5PS
kind: algorithm
slug: consistent-normal-orientation
name: Consistent normal orientation
aliases:
- Hoppe normal orientation
area: computer-vision/point-clouds-and-registration
level: advanced
summary: Orient the normals of a point cloud consistently by propagating along a minimum spanning tree of a neighbor graph weighted by how parallel the normals are.
model: real-ram
complexity:
  vars: {n: the number of points, k: the number of neighbors per point}
  time: {worst: O(n^2 log n), average: O(n k log n), best: Ω(n k)}
  space: {extra: Θ(n k)}
properties: {deterministic: true, exact: false, heuristic: true, online: false, recursive: false, input_sign_invariant: true}
history:
  year: 1992
  people: [Hugues Hoppe, Tony DeRose, Tom Duchamp, John McDonald, Werner Stuetzle]
  note: "Hoppe and his coauthors oriented the tangent planes of an unorganized point cloud by propagation along a minimum spanning tree of a graph of near points, with the cost 1 - |n_i . n_j| on each edge, as a step of their surface reconstruction method."
prereqs: [point-cloud-normal-estimation, minimum-spanning-tree]
see_also: [prim, kruskal, euclidean-minimum-spanning-tree, depth-first-search, k-nearest-neighbors, surface-reconstruction, poisson-surface-reconstruction, signed-distance-function]
sources:
  - paper: doi:10.1145/142920.134011
    title: "Hugues Hoppe, Tony DeRose, Tom Duchamp, John McDonald and Werner Stuetzle, Surface reconstruction from unorganized points, Computer Graphics (Proceedings of SIGGRAPH 92) 26(2), 1992, 71-78"
    locator: "The consistent orientation of the tangent planes: the Riemannian graph of the Euclidean minimum spanning tree and the k nearest neighbor edges, the cost 1 - |n_i . n_j|, and the traversal of its minimum spanning tree from the point of largest z"
---

Consistent normal orientation chooses the sign of each normal of a point cloud so that neighboring normals point to the same side of the surface. [Normal estimation](/point-cloud-normal-estimation/) by local plane fitting gives each normal only up to its sign, and a cloud with signs chosen at random is useless for shading, for [surface reconstruction](/surface-reconstruction/) and for any method that needs an inside and an outside. The method of Hoppe and his coauthors (1992) builds a graph of near points, gives each edge a cost that is small when the two normals are close to parallel, and takes a [minimum spanning tree](/minimum-spanning-tree/) of this graph. It fixes the sign at the highest point so that its normal points up, then walks the tree and flips each child normal that points against its parent. The tree prefers flat, smooth paths, where the sign decision is easy. The method is a heuristic: it can fail at thin parts and sharp edges.

## In plain words

Each point has a normal, a short arrow that sticks out of the surface, but some arrows point out and some point in. You want them all to point out.

Start at the highest point of the cloud. Its arrow must point up to be on the outside, so turn it up if it points down. Then go to a near point. If its arrow points against the arrow you just fixed, turn it around. Keep going, from fixed points to near points, until every point is done.

The order of the walk matters. A step between two points on a flat part is safe, because their arrows are almost the same. A step across a sharp edge or between the two sides of a thin sheet is risky. So the walk goes along a tree that uses the safest steps first.

## The problem

The input is a list of $n$ points $p_1, \ldots, p_n$ in $\mathbb{R}^3$ sampled from a surface, unit normals $\mathbf{n}_1, \ldots, \mathbf{n}_n$ with arbitrary signs, and a neighborhood size $k$. The output is a sign $s_i \in \{+1, -1\}$ for each point, and the oriented normals $s_i \mathbf{n}_i$.

The wanted output is the orientation of the true surface, for example the outward normals of a closed object. The surface is unknown, so this goal has no exact form. The method replaces it with a local rule: the normals of neighboring points should have a positive dot product. On a smooth, well-sampled surface the true orientation obeys this rule, but at a sharp edge or across a thin part it does not.

## The algorithm

```pseudo id=main
ORIENT-NORMALS(P, N, k)
L1  G ← the graph with the edges of the Euclidean MST of P and the edges to the k nearest neighbors
L2  give each edge (i, j) of G the cost 1 - |n_i · n_j|
L3  r ← the point of P with the largest z coordinate
L4  T ← a minimum spanning tree of G, grown by Prim's algorithm from r
L5  if n_r · e_z < 0 then n_r ← -n_r
L6  S ← a stack that holds r
L7  while S is not empty do
L8      i ← POP(S)
L9      for each child j of i in T do
L10         if n_i · n_j < 0 then n_j ← -n_j
L11         PUSH(S, j)
L12 return N
```

Line L1 builds what Hoppe and his coauthors call the Riemannian graph. The $k$ nearest neighbor edges connect points on the same part of the surface. The [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) edges make sure the graph is connected even when the cloud has gaps. Line L2 uses the absolute value, so the cost does not depend on the current signs: it is 0 for parallel or antiparallel normals and 1 for perpendicular ones. Line L3 picks a point whose outward normal is known: on a closed surface, the highest point has the normal $+e_z$. Line L4 is [Prim's algorithm](/prim/) on the costs of line L2. Any minimum spanning tree method works, for example [Kruskal's algorithm](/kruskal/) followed by a traversal. Lines L6 to L11 are a [depth-first traversal](/depth-first-search/) of the tree. A child is handled after its parent is final, so line L10 compares it with a normal that will not change again.

## Example

Take five points on the unit circle in the $xz$ plane, at the angles 90°, 60°, 30°, 120° and 150°, numbered 0 to 4. The true outward normal of each point is the point itself. The input normals have the signs $+, -, +, +, -$, and $k = 2$.

Neighbors on the arc are 30° apart, so their normals have $|n_i \cdot n_j| = \cos 30° \approx 0.866$ and the cost $0.134$. Points 60° apart have the cost $0.5$. The graph has the edges 0-1, 1-2, 0-3 and 3-4 of cost $0.134$, and 0-2 and 0-4 of cost $0.5$. The tree takes the four cheap edges. The root is point 0, the highest.

| point | angle | input normal | parent | dot with parent | action | output |
|---|---|---|---|---|---|---|
| 0 | 90° | $(0, 0, 1)$ | root | $n_z = 1 \ge 0$ | keep | $(0, 0, 1)$ |
| 1 | 60° | $(-0.5, 0, -0.866)$ | 0 | $-0.866$ | flip | $(0.5, 0, 0.866)$ |
| 2 | 30° | $(0.866, 0, 0.5)$ | 1 | $0.866$ | keep | $(0.866, 0, 0.5)$ |
| 3 | 120° | $(-0.5, 0, 0.866)$ | 0 | $0.866$ | keep | $(-0.5, 0, 0.866)$ |
| 4 | 150° | $(0.866, 0, -0.5)$ | 3 | $-0.866$ | flip | $(-0.866, 0, 0.5)$ |

The four tree edges have the same cost up to rounding, so the order in which the stack handles the two branches depends on the last bits of the costs. The result does not: each branch only reads its own parents. Every output normal points away from the center of the circle. Point 4 is compared with the new normal of point 3, and point 2 with the new normal of point 1, never with an input normal.

## Correctness

After the traversal, the root normal has $n_z \ge 0$ and every child has a nonnegative dot product with its parent. Each point is pushed once, as a child of its parent, after the parent is final, so this holds on every tree edge. When no tree edge has a zero dot product, these conditions fix every sign, so the output does not depend on the input signs. If a true orientation agrees along every tree edge, the output equals it up to one global sign, and the sign is right when the true normal at the highest point points up. The tree is a minimum spanning tree for the cost $1 - |n_i \cdot n_j|$, so it avoids edges where the normals turn fast. The full proof is below.

Nothing makes a true orientation agree along the tree. The guarantee is conditional, and the method is a heuristic.

## Complexity

The model is the [real RAM](/real-ram/), with $n$ points and $k$ neighbors per point. The graph has $O(n k)$ edges, because the minimum spanning tree adds only $n - 1$.

- **Brute force.** A dense Prim on all pairs gives the Euclidean MST in $O(n^2)$ time. A scan of all points with a heap of size $k$ gives the $k$ nearest neighbors of one point in $O(n \log k)$, so $O(n^2 \log k)$ in total. Prim's algorithm with a binary heap on the graph costs $O(n k \log n)$. The traversal costs $O(n)$. The total is $O(n^2 \log n)$.
- **With spatial search.** A [k-d tree](/kd-tree/) finds the neighbors in $O(n (\log n + k \log k))$ on well-spread points. For such points the Euclidean MST can be taken from the Delaunay triangulation, or the MST edges can be left out when the $k$ nearest neighbor graph is already connected. Prim's algorithm then dominates, with $O(n k \log n)$.
- **Space.** $\Theta(n k)$ for the graph, and $\Theta(n)$ for the tree and the stack.

Every edge of the graph is looked at once, so the time is at least $\Omega(n k)$.

## Properties

- **Input sign invariant.** The costs, the tree and the root do not depend on the input signs, so the output is the same whatever signs come in, except when a tree edge has a zero dot product.
- **Locally consistent.** Neighbors along the tree have normals with a nonnegative dot product.
- **Global sign from one point.** The outward side comes from the highest point only. If that point lies on a sharp tip or on a noisy part, the whole result can come out inward.
- **Error propagation.** One wrong decision flips the whole subtree below it, often a large connected patch.
- **Deterministic.** With a fixed tie rule, the same input gives the same output.

## Variants and improvements

- **Viewpoint orientation.** When the cloud comes from one sensor at a known position $o$, flip each normal to face $o$. This needs no graph, and it is right for every point the sensor saw. Clouds merged from many scans keep the sensor position of each point for this test.
- **Graph without the EMST.** Most libraries use only the $k$ nearest neighbor graph, or a radius graph, and orient each connected component on its own. This is faster, but a component can get a sign that disagrees with the rest.
- **Other edge costs.** The cost can also grow with the distance between the points or with the curvature, which keeps the tree away from edges and thin parts.
- **Multiple roots.** Start the traversal at several points whose orientation is known, such as the extreme points along each axis, and grow the trees together.
- **Global methods.** Other methods choose all signs together, for example by an energy over all graph edges or by making a signed distance field or a winding number field consistent. They cost more and handle thin parts and noise better.
- **Orientation inside reconstruction.** Some reconstruction methods take unoriented normals or none and find the inside and outside as part of the fit, which removes this step.

## When to use it

Use propagation along a minimum spanning tree when the cloud has no sensor positions, the surface is smooth at the scale of the sampling, and the sampling is dense compared with the thickness of the thinnest part. This holds for many scans of single objects, and it is the usual step before [Poisson surface reconstruction](/poisson-surface-reconstruction/) or a [signed distance function](/signed-distance-function/) fit. When the sensor positions are known, orient by the viewpoint. For thin sheets, sharp CAD models and very noisy clouds, use a global method or check the result.

## Pitfalls

- **Thin parts.** At line L1 the $k$ nearest neighbors of a point on one side of a thin plate include points of the other side. Their normals are parallel, so line L2 gives the cost 0, the tree crosses the plate, and line L10 makes both sides point the same way. Choose $k$ small compared with the thickness, or downsample less.
- **Sharp edges.** Across a 90° edge the dot product at line L10 is near 0, and noise decides its sign. The cost of line L2 makes such edges expensive, but the tree must still cross the edge once to reach the other face.
- **A bad root.** Line L5 assumes that the highest point has a normal near $+e_z$. On a cloud with the highest point at a sharp tip, an open boundary or an outlier, the guess can be wrong and every normal comes out inward. Remove outliers first, or test the global sign afterwards.
- **Comparing with the input normal.** Line L10 must compare the child with the parent's final normal, not with the parent's input normal. A breadth-first or depth-first order over the tree does this. Flipping by a loop over the tree edges in an arbitrary order does not.
- **A disconnected graph.** Without the EMST edges of line L1, the $k$ nearest neighbor graph of a cloud with gaps has several components, and line L4 reaches only the component of the root. The other points keep their input signs.
- **Signed costs.** Using the cost $1 - n_i \cdot n_j$ at line L2, without the absolute value, makes the tree depend on the input signs and steers it toward edges whose input signs happen to agree.

## Implementations

## History

Hoppe, DeRose, Duchamp, McDonald and Stuetzle (1992) reconstructed surfaces from unorganized points by a signed distance function to a set of tangent planes. The sign of the distance needs oriented planes, so they oriented the plane normals by propagation. They first used the Euclidean minimum spanning tree as the order of propagation, saw that it failed where the surface has thin or curved parts, and then added the $k$ nearest neighbor edges to form the Riemannian graph with the cost $1 - |n_i \cdot n_j|$, rooting the tree at the point of largest $z$. The method became the standard first step for orienting normals of unorganized clouds. Later work changed the graph and the costs, used the sensor positions when they are known, and replaced the local propagation with global optimization.

## References
