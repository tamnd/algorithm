---
tag: H3T7WW
kind: algorithm
slug: boundary-layer-mesh-generation
name: Boundary layer mesh generation
aliases:
- advancing layers method
- prismatic layer meshing
area: cad/mesh-generation-for-analysis
level: advanced
summary: Grows thin layers of prisms or stretched tetrahedra out from walls along normals with geometric growth, to resolve boundary layers in flow simulation.
solves: [mesh-generation]
model: real-ram
complexity:
  vars: {n: the number of wall vertices, k: the number of layers}
  time: {worst: O(k n^2)}
  space: {extra: O(k n)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1996
  people: [Shahyar Pirzadeh, Rao V. Garimella, Mark S. Shephard]
  note: Pirzadeh described the advancing layers method for viscous tetrahedral grids in 1996, and Garimella and Shephard described layers of prisms and stretched tetrahedra on curved walls in 2000.
prereqs: [offset-curve, advancing-front-mesh-generation, shoelace-formula]
see_also: [anisotropic-mesh-adaptation, structured-grid-generation, straight-skeleton, finite-volume-method, mesh-quality-measures, mesh-sizing-function, paving, constrained-delaunay-tetrahedralization]
sources:
  - paper: doi:10.2514/3.13019
    title: Shahyar Pirzadeh, Three-dimensional unstructured viscous grids by the advancing-layers method, AIAA Journal 34(1), 1996, 43 to 49
    locator: the march of layers along wall normals, the growth of the layer thickness, normal smoothing and the local stop of layers where fronts approach each other (general locator)
---

Boundary layer mesh generation makes thin, stretched elements next to the walls of a body, for flow simulations. In a viscous flow the velocity changes very fast across a thin layer near the wall, and slowly along it, so the first cells must be very thin in the wall normal direction and can be long along the wall. The method moves the wall vertices outward along normal directions in steps, one layer at a time, with heights that grow by a fixed ratio, and joins each layer to the one before it. In 2D the cells are quads, in 3D prisms, which can be split into tetrahedra. Each layer is accepted only if its cells are valid, so the growth stops where layers would invert or collide. The rest of the domain is then filled by an isotropic mesher.

## In plain words

Draw the outline of a wing. Draw a second outline a tiny step outside it, then a third one a slightly bigger step outside the second, and so on, each step a fixed factor bigger than the one before. Join each corner to the matching corner of the next outline. The strips between the outlines are thin cells that hug the wall.

On a round shape this always works, because the outlines get longer as they move out. In a dent the outlines get shorter, and at some point a strip has no length left, or two sides of the dent meet. Before that, the method stops adding layers. The space that is left is filled with ordinary triangles.

## The problem

The input is a wall polygon in counterclockwise order, with the flow outside it, a first height $h_1$, a growth ratio $r > 1$ and a number of layers $k$. The output is a mesh of quads in up to $k$ layers. Layer $j$ has the thickness $h_1 r^{j-1}$, so the total height after $j$ layers is $d_j = h_1 (r^j - 1)/(r - 1)$. Every quad must be strictly convex, the layers must not overlap, and the outer front must be a simple polygon, so that a triangle mesher can fill the rest. The first height comes from the flow: for a turbulent flow it is chosen so that the first cell centre is inside the viscous sublayer.

## The algorithm

Each wall vertex moves along its miter vector $m_i$, which is the sum of the unit outward normals of its two edges, divided by one plus their dot product. The point $x_i + d\,m_i$ is at the distance $d$ from both edge lines, so every layer is a true offset of the wall.

```pseudo id=main
GROW-LAYERS(wall x_0..x_{n−1}, h1, r, k)
L1  n_i ← the unit outward normal of the edge x_i x_{i+1}
L2  m_i ← (n_{i−1} + n_i) / (1 + n_{i−1} · n_i)
L3  d_0 ← 0; d_j ← d_{j−1} + h1 · r^(j−1) for j = 1..k
L4  for j ← 1 to k do
L5      x_i^j ← x_i + d_j · m_i for every i
L6      Q_i^j ← (x_{i+1}^{j−1}, x_i^{j−1}, x_i^j, x_{i+1}^j) for every i
L7      if some Q_i^j is not strictly convex and counterclockwise then stop
L8      if the polygon x_0^j..x_{n−1}^j is not simple then stop
L9      accept layer j
L10 return the accepted quads and the number of layers
```

L7 uses exact [orientation tests](/orientation-test/) on the float coordinates, which convert to fractions without rounding. L8 tests every pair of front edges for a common point, which costs $O(n^2)$.

## Example

Take the unit square as the wall, with $h_1 = 0.01$ and $r = 1.2$. All corners turn by $90°$, and the miter of each corner is $(\pm 1, \pm 1)$, so layer $j$ is the square $[-d_j, 1 + d_j]^2$. After 10 layers, $d_{10} = 0.2596$, all 40 quads are valid, and their total area $1.3079$ equals $(1 + 2 d_{10})^2 - 1$, as Theorem 5 of the proof says.

Now take the U-shaped wall $(0,0)$, $(3,0)$, $(3,2)$, $(2,2)$, $(2,1)$, $(1,1)$, $(1,2)$, $(0,2)$, with a slot of width 1 and depth 1, and $h_1 = 0.05$, $r = 1.2$.

| layer $j$ | $d_j$ | length of the slot bottom, $1 - 2 d_j$ | result |
|---|---|---|---|
| 1 | 0.0500 | 0.9000 | accepted |
| 3 | 0.1820 | 0.6360 | accepted |
| 5 | 0.3721 | 0.2558 | accepted |
| 6 | 0.4965 | 0.0070 | accepted |
| 7 | 0.6458 | $-0.2916$ | stop: the quad inverts |

Both ends of the slot bottom are reflex corners that turn by $-90°$, so the offset of the bottom loses $2d$ of length, and it collapses at $d = 0.5$. The method keeps 6 layers, 48 quads. On a horseshoe shaped wall whose two tips face each other across a gap of 0.4, the same parameters stop at layer 4, where $d_4 = 0.2684 > 0.2$: the quads are still valid, but the two fronts cross.

## Correctness

The proof file has the details. The heights are a geometric series, so the thickness ratio is exactly $r$. The miter vector puts every layer vertex at the distance $d$ from both edge lines, so each offset edge is parallel to its wall edge, and its length is $L + d(\tan(\alpha_a/2) + \tan(\alpha_b/2))$, where $\alpha_a$ and $\alpha_b$ are the signed turning angles at its ends. Each quad is a trapezoid, and it is strictly convex exactly while that length is positive, which gives an exact collapse height at reflex corners.

For a whole layer, the boundaries of the quads add up to the outer front minus the inner front, because each radial edge cancels with its neighbour. So the winding numbers add up the same way. If every quad is valid and the new front is simple, every point between the fronts is in exactly one quad, every point inside the inner front is inside the outer front, and the area of the layer is the difference of the two front areas. On a strictly convex wall the lengths only grow, so every layer is accepted.

What is not proved: the stop rule is safe but crude, nothing bounds the stretch of the quads, which is high on purpose, and the miter length is unbounded at sharp convex corners.

## Complexity

One layer costs $O(n)$ for the new points and the quad tests and $O(n^2)$ for the simplicity test of the front, so $k$ layers cost $O(k n^2)$. A sweep line or a grid of buckets makes the front test $O(n \log n)$ for most inputs, and production codes test only nearby fronts with a search tree. The space is $O(k n)$ for the points and quads.

## Properties

- **Exact heights.** The distance of each layer vertex from both of its wall edges is exactly the planned height in exact arithmetic.
- **Valid by test.** No inverted or overlapping cell is ever accepted.
- **Convex walls always work.** On a strictly convex wall, every requested layer is accepted.
- **Anisotropic by design.** The cells are long along the wall and thin across it, with aspect ratios of 100 or more in practice.
- **Structured in the normal direction.** The layers form a structured grid in the wall normal direction, which flow solvers like.

## Variants and improvements

- **Local stop.** Instead of stopping the whole layer, real codes freeze single vertices where a quad would invert or fronts come close, and close the gap with triangles or pyramids. This keeps more layers where the wall is smooth.
- **Normal smoothing.** Pirzadeh's advancing layers method smooths the march directions over many layers, so that the layers open up in concave regions instead of collapsing.
- **Fans at sharp corners.** At a sharp convex corner, such as a trailing edge, several directions spread out from one wall vertex, which avoids the long miter.
- **3D prisms and tetrahedra.** In 3D the wall is a triangle mesh, each layer gives prisms, and each prism can be split into three tetrahedra. Garimella and Shephard handle curved walls and the transition to the isotropic mesh.
- **Metric view.** A boundary layer mesh is an [anisotropic mesh](/anisotropic-mesh-adaptation/) whose metric is stretched in the normal direction near the wall.

## When to use it

Use it for viscous flow simulations with the [finite volume method](/finite-volume-method/) or a finite element method, where the solver needs thin, wall aligned cells to resolve the velocity gradient at the wall. Use it before the isotropic mesher, which then meshes the region outside the last front, for example by [advancing front mesh generation](/advancing-front-mesh-generation/) or Delaunay methods. For inviscid flow or for structures, there is no thin layer to resolve, and an isotropic mesh is enough.

## Pitfalls

- **Reflex corners.** The offset edges next to a reflex corner shrink and invert at the collapse height. Test each layer, and stop or smooth the directions there.
- **Narrow gaps.** Two parts of the wall that face each other across a gap smaller than twice the total height make the fronts cross, even when every quad is valid. Test the front for self intersection.
- **Sharp convex corners.** The miter length is $1/\cos(\alpha/2)$ and is unbounded as the turning angle $\alpha$ approaches $180°$. Use a fan of directions there.
- **Bad transition.** If the last layer is much thinner than the size of the outer mesh, the jump in size spoils the solution. Choose $r$ and $k$ so that the last thickness is close to the outer size.
- **Float tests.** A float orientation test can accept a quad that is slightly inverted, which a solver later rejects. Use exact tests.

## Implementations

## History

Meshes for viscous flows were first made with structured grids. With the move to unstructured tetrahedral meshes for complex shapes in the 1990s, several groups made layers of thin cells next to the walls before filling the rest. Shahyar Pirzadeh described the advancing layers method in the AIAA Journal in 1996: it marches the wall triangles outward layer by layer along smoothed normals and stops locally where layers would collide. Rao Garimella and Mark Shephard described the generation of layers of prisms and stretched tetrahedra on curved walls in 2000.

## References
