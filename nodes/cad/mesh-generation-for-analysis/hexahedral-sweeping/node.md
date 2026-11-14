---
tag: AETFHW
kind: algorithm
slug: hexahedral-sweeping
name: Sweeping for hexahedral meshes
aliases:
- swept meshing
- one-to-one sweep
- many-to-one sweep
area: cad/mesh-generation-for-analysis
level: core
summary: Meshes a two-and-a-half dimensional solid by sweeping the quad mesh of a source face to a target face through layers, the most used hex method in practice.
solves: [hexahedral-mesh-generation]
model: real-ram
complexity:
  vars: {K: the number of layers of hexes, n: the number of vertices of the source quad mesh}
  time: {worst: O(K n)}
  space: {extra: O(K n)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1996
  people: [B. Shih, H. Sakurai, Patrick M. Knupp]
  note: Extrusion of a 2D mesh is older. Shih and Sakurai in 1996 split a solid into swept volumes, and Knupp in 1998 placed the inner nodes of each layer by an affine map fitted to its boundary loop.
prereqs: [hexahedral-mesh-generation, scaled-jacobian, bilinear-interpolation, normal-equations]
see_also: [transfinite-interpolation-grid, structured-grid-generation, mesh-untangling, plastering, polycube-hex-meshing, medial-axis-decomposition-meshing, whisker-weaving, volumetric-spline-parameterization]
sources:
  - paper: "B. Shih and H. Sakurai, Automated hexahedral mesh generation by swept volume decomposition and recomposition, Proceedings of the 5th International Meshing Roundtable, 1996"
    locator: the split of a solid into swept volumes and the one-to-one sweep of each part (general locator)
  - paper: "Patrick M. Knupp, Next-generation sweep tool, a method for generating all-hex meshes on two-and-a-half dimensional geometries, Proceedings of the 7th International Meshing Roundtable, 1998, 505 to 513"
    locator: the placement of the inner nodes of each layer by a least squares affine map of the boundary loop (general locator)
  - paper: "Matthew L. Staten, Scott A. Canann and Steven J. Owen, BMSweep, locating interior nodes during sweeping, Engineering with Computers 15, 1999, 212 to 218"
    locator: the placement of the inner nodes by a blend of boundary maps (general locator)
  - paper: "David R. White, Sunil Saigal and Steven J. Owen, CCSweep, automatic decomposition of multi-sweep volumes, Engineering with Computers 20(3), 2004, 222 to 236"
    locator: the many-to-one sweep and the split of a volume with several source faces (general locator)
---

Sweeping makes an all-hex mesh of a solid that is a quad face moved along a path, such as an extruded or revolved part. The user gives a source face with a quad mesh, a target face, and linking sides that join them and are already meshed in layers. Each layer of the sweep is a copy of the source mesh: the boundary nodes of the copy are on the linking sides, and the inner nodes are placed by a map from the source face. Corresponding quads of two neighbouring layers are joined into a hex. This page is one method for [hexahedral mesh generation](/hexahedral-mesh-generation/), and it meshes only solids that have a sweep direction, while that page states the general problem and its limits. Sweeping is the main hex method in commercial meshers, where the user first cuts the part into sweepable volumes.

## In plain words

Think of a cookie cutter pushed through dough. On the face of the cutter we draw a grid of four-sided cells. We push copies of this grid along the part, one layer at a time, to the far end. Two copies in a row, with their matching cells joined, make a layer of bricks.

The edge of each copy must follow the side walls of the part, so it is known. The inner points are not known. A simple rule is to find the stretch, turn and shift that best moves the source edge onto the new edge, and to apply the same move to the inner points.

The bricks are good when each step from one layer to the next is a gentle move. If one layer turns too far against the last one, the bricks between them collapse, even if their corners look correct.

## The problem

The source face is a polygon $S$ in the plane with a conforming mesh of strictly convex counterclockwise quads. Its vertices are $p_v$, and its boundary loop is the cycle of vertices $\ell_1, \ldots, \ell_m$, not all on one line. The linking sides are meshed already, so the input also gives the position $B_k[\ell_i] \in \mathbb{R}^3$ of each loop vertex on each layer $k = 0, \ldots, K$, with $K \ge 1$. Layer $0$ is the source face and layer $K$ is the target face.

The output is a node $x_{k,v}$ for every layer and every source vertex, and the $K$ times $Q$ hexes that join quad $(a, b, c, d)$ of layer $k$ to the same quad of layer $k + 1$. Here $Q$ is the number of source quads. A hex is valid if its trilinear map from the unit cube has $\det J > 0$ at every point, as on the [scaled Jacobian](/scaled-jacobian/) page. A mesh is valid if every hex is valid and two hexes meet only in a common face, edge or vertex.

## The algorithm

For layer $k$, line L2 finds the affine map $\varphi_k(p) = L_k p + t_k$, with $L_k$ a $3 \times 2$ matrix, that minimizes $\sum_i \lVert \varphi_k(p_{\ell_i}) - B_k[\ell_i] \rVert^2$. This is a least squares problem with one $3 \times 3$ system of [normal equations](/normal-equations/) per coordinate. CERTIFY tests the slab map between two layers. Its coefficients $b_0, b_1, b_2$ are given below.

```pseudo id=main
SWEEP(p, quads, loop, B)
L1  for k ← 0 to K do
L2      φ_k ← the least squares affine map with φ_k(p_ℓ) ≈ B_k[ℓ] for the loop vertices ℓ
L3      for each source vertex v do
L4          x_{k,v} ← B_k[v] if v is on the loop, else φ_k(p_v)
L5  H ← empty list
L6  for k ← 0 to K − 1 do
L7      for each source quad (a, b, c, d) do
L8          append the hex (x_{k,a}, x_{k,b}, x_{k,c}, x_{k,d}, x_{k+1,a}, x_{k+1,b}, x_{k+1,c}, x_{k+1,d}) to H
L9  ok ← every hex of H has 8 positive corner Jacobians
L10 return H, x, φ, ok

CERTIFY(p, loop, x, φ)
L11 for k ← 0 to K do
L12     if x_{k,v} ≠ φ_k(p_v) for some vertex v then return false
L13 for k ← 0 to K − 1 do
L14     for each loop vertex ℓ do
L15         (b_0, b_1, b_2) ← the slab coefficients of φ_k and φ_{k+1} at p_ℓ
L16         if not (b_0 > 0 and b_2 > 0 and (b_1 ≥ 0 or b_1² < b_0 b_2)) then return false
L17 return true
```

Lines L1 to L4 build the layers. A loop vertex keeps its given position, so the mesh follows the linking sides exactly. The inner nodes copy the source mesh through the fitted map. Lines L5 to L8 join the layers. The hex has the standard vertex order, so its bottom face is the source quad and its top face is the same quad one layer up. Line L9 is the usual check of the corner Jacobians. It is necessary for validity but not sufficient.

CERTIFY is the stronger test. When every layer is affine, the hexes of slab $k$ are pieces of the slab map

$$F_k(p, w) = (1 - w)\,\varphi_k(p) + w\,\varphi_{k+1}(p), \qquad p \in S,\ w \in [0, 1].$$

With $L_k = [\,l_{k,1}\ l_{k,2}\,]$ and $d(p) = \varphi_{k+1}(p) - \varphi_k(p)$, its Jacobian determinant is a quadratic in $w$:

$$\det DF_k = b_0 (1 - w)^2 + 2 b_1 w (1 - w) + b_2 w^2,$$

$$b_0 = \det[l_{k,1}, l_{k,2}, d], \quad b_2 = \det[l_{k+1,1}, l_{k+1,2}, d], \quad 2 b_1 = \det[l_{k,1}, l_{k+1,2}, d] + \det[l_{k+1,1}, l_{k,2}, d].$$

Line L16 is an exact test that this quadratic is positive on $[0, 1]$. The coefficients are affine in $p$, so a test at the loop vertices covers the whole face.

## Example

The source face is the square $[0, 2]^2$ with the $2 \times 2$ grid of unit quads. There are three layers, all about the center $(1, 1)$. Layer $0$ is the source at height $0$. Layer $1$ at height $1$ applies the matrix $A_1 = \begin{pmatrix} 1 & -1/2 \\ 1/2 & 1 \end{pmatrix}$, which turns and stretches the square, with $\det A_1 = 5/4$. Layer $2$ at height $2$ is the target face, the square turned by $90$ degrees. Each loop is an exact affine image of the source loop, so L2 recovers the map exactly, and the inner node $(1, 1)$ stays at $(1, 1)$ on every layer. The corner $(0, 0)$ goes to $(1/2, -1/2, 1)$ and then to $(2, 0, 2)$.

| slab | $(b_0, b_1, b_2)$ at every loop vertex | corner Jacobians of each hex | volume of each hex |
|---|---|---|---|
| 0 | $(1, 1, 5/4)$ | $1, 1, 1, 1, 5/4, 5/4, 5/4, 5/4$ | $13/12$ |
| 1 | $(5/4, 1/2, 1)$ | $5/4, 5/4, 5/4, 5/4, 1, 1, 1, 1$ | $11/12$ |

All coefficients are positive, so CERTIFY returns true and every hex is valid at every point. The eight volumes add up to $8$, the volume of the swept solid. Every node of layer $2$ is the source node $(x, y)$ moved to $(2 - y, x, 2)$, so the target face gets the source mesh turned by $90$ degrees.

**A twist that looks valid.** Now use two layers only, and let layer $1$ be the source turned by $180$ degrees about $(1, 1)$, at height $1$. Every hex has all eight corner Jacobians equal to $1$, so L9 sets ok to true. But the coefficients are $(1, -1, 1)$, so $\det DF_0 = (1 - 2w)^2$, which is $0$ at $w = 1/2$. All four hexes pass through the axis point $(1, 1, 1/2)$, and each has the volume $1/3$ in place of $1$. CERTIFY returns false. With the stretched turn $\operatorname{diag}(-1, -2)$ in place of the half turn, the corners are still positive, but $\det J < 0$ inside every hex at $w = 2/5$.

## Correctness

L4 keeps every loop vertex, and when a loop is the image of an affine map, the fit is exact and the whole layer is that image, so the target mesh is the expected one. For validity, an affine layer pair makes each hex the slab map $F_k$ applied to (source quad) times $[0, 1]$. The chain rule then gives $\det J_{\text{hex}} = \det DF_k \cdot \det DP$, where $P$ is the bilinear map of the source quad. For a strictly convex quad, $\det DP$ is affine and positive at the corners, so it is positive. So the hexes are valid when every slab map is orientation preserving. If the slab maps are also one to one, the hexes fill the solid without overlap. For planar layers at increasing heights, CERTIFY implies this. The full proof is below.

What is proved and what is measured are different here. The proof covers only affine layers and convex source quads. For curved linking sides, real sweepers fit or blend non-affine maps, and then validity is measured by the corner check of L9 or by a [scaled Jacobian](/scaled-jacobian/) sample, not proved. The tests of the implementation check the example, the half turn, the target mesh, and 500 random sweeps. In each random sweep, CERTIFY agrees with an exact minimization of $\det((1 - w) A_k + w A_{k+1})$, and the hex volumes add up to the exact integral of the slab determinant.

## Complexity

L2 builds and solves a $3 \times 3$ system in $O(m)$ time for a loop of $m$ vertices. L3 and L4 take $O(n)$ per layer. A planar quad mesh has fewer quads than vertices, so L5 to L8 take $O(Kn)$, and L9 takes constant time per hex. The total time and space are $O(Kn)$. CERTIFY also takes $O(Kn)$. Sweeping has no iteration, so it is one of the cheapest ways to make a large hex mesh.

## Properties

- **Structured in the sweep direction.** Every inner vertex has degree 6 away from the source and target faces, and the mesh is a stack of copies of the source mesh.
- **Fixed count.** The mesh has exactly $KQ$ hexes, set by the source mesh and the number of layers.
- **Exact on the linking sides.** The loop nodes are the given ones.
- **Exact for affine layers.** If every loop is an affine image of the source loop, every layer is that image.
- **Twist per slab.** For layers that are turns by an angle $\theta$ about one axis, the coefficients are $(1, \cos\theta, 1)$, so each slab can turn by any angle below $180$ degrees and the hexes stay valid.
- **No general guarantee.** For curved or warped sides, the inner nodes can leave the solid or fold, and the corner check can miss an inverted hex.

## Variants and improvements

- **Other node placement.** In place of one affine map per layer, the inner nodes can come from a blend of the maps from the source and from the target, as in BMSweep, from weighted residuals, or from a [transfinite interpolation](/transfinite-interpolation-grid/) of the linking sides. These follow curved sides better but have no validity proof.
- **Projection to the target.** The target face is often curved. The inner nodes of the last layer are then projected onto it, and the quads of the target mesh are checked.
- **Many-to-one sweep.** Several source faces sweep to one target face. Their meshes must be merged in the layer where they meet, and the volume is first split into parts with one source each (CCSweep).
- **Multi-axis sweeps.** The volume is split into parts that sweep in different directions, and their interface meshes are matched.
- **Smoothing and untangling.** A last pass of [mesh untangling](/mesh-untangling/) or [optimization based smoothing](/optimization-based-mesh-smoothing/) repairs the few hexes that fail the check.

## When to use it

Use sweeping for extruded, revolved and other two-and-a-half dimensional parts, which are very common in mechanical design. It gives hexes aligned with the sweep direction, which is good for boundary layers and thin walls. Use it inside a decomposition: cut the part into sweepable volumes, by hand or by a method such as [medial axis decomposition](/medial-axis-decomposition-meshing/), and sweep each part. Do not use it for a solid with no sweep direction. For such a solid, use [polycube](/polycube-hex-meshing/) or [frame field](/frame-field-hex-meshing/) methods, or accept a mixed mesh.

## Pitfalls

- **Corner checks are not proofs.** The half turn of the example has eight positive corner Jacobians and a zero Jacobian inside. Test each slab with a certificate such as CERTIFY or with the Bernstein coefficients of the hex.
- **Source and target meshes that do not match.** A one-to-one sweep needs the same quad mesh on the source and the target, up to the map. If the target face is already meshed by a neighbour volume, the two meshes must agree, or the sweep fails.
- **Linking sides with a different layer count.** Every linking side must have the same number of layers, so the interval counts of the sides must be matched before sweeping.
- **Floating point fits.** The least squares fit and the sign tests round. Near a degenerate slab, use exact arithmetic, as the implementation does, or a tolerance.
- **Concave source quads.** The proof needs strictly convex quads. A concave quad already has a negative $\det DP$, and no sweep can repair it.

## Implementations

## History

Moving a 2D mesh along a third direction is one of the oldest ways to make hexes, and early structured grid codes extruded blocks in this way. Shih and Sakurai in 1996 proposed to split a solid into swept volumes and to sweep each part. Knupp in 1998 gave an affine method to place the inner nodes of each layer from its boundary loop, and Staten, Canann and Owen in 1999 gave BMSweep, which blends maps from both ends. Miyoshi and Blacker in 2000 swept along several axes, and White, Saigal and Owen in 2004 split many-to-one volumes automatically. The Pietroni et al. survey of 2022 reports that sweeping of a user decomposition is still the main hex method in commercial software.

## References
