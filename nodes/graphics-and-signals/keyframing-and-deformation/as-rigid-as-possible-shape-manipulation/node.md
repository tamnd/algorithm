---
tag: 6TBSNN
kind: algorithm
slug: as-rigid-as-possible-shape-manipulation
name: As-rigid-as-possible shape manipulation
aliases:
- Igarashi shape manipulation
area: graphics-and-signals/keyframing-and-deformation
level: advanced
summary: Deform a 2D triangulated shape in real time from moved handles by two least-squares steps that minimize distortion of each triangle.
solves: [shape-deformation]
model: real-ram
complexity:
  vars: {n: "the number of mesh vertices", m: "the number of triangles"}
  time: {register: "O(n^3 + m)", per_move: "O(n^2 + m)"}
  space: {extra: "Θ(n^2 + m)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
prereqs: [least-squares-problem, cholesky-decomposition]
see_also: [as-rigid-as-possible-shape-interpolation, as-rigid-as-possible-deformation, laplacian-surface-editing, kabsch-algorithm, shape-deformation, cage-based-deformation, green-coordinates, arap-parameterization]
sources:
  - paper: doi:10.1145/1073204.1073323
    title: "Takeo Igarashi, Tomer Moscovich and John F. Hughes, As-rigid-as-possible shape manipulation, SIGGRAPH 2005, ACM Transactions on Graphics 24(3), 1134-1141, 2005"
    locator: the whole paper (the scale-free construction, the scale adjustment by fitted triangles, and the precomputed factorizations that make each handle move a pair of back substitutions)
---

As-rigid-as-possible shape manipulation moves a 2D shape, given as a triangle mesh, by a few handles that the user drags.
The rest of the mesh follows so that each triangle changes as little as possible, apart from a rotation.
Takeo Igarashi, Tomer Moscovich and John Hughes (2005) made it fast enough for real time with two linear least squares steps and no iteration: the first step allows each triangle to rotate and scale, and the second removes the scale.
Both matrices depend only on the mesh and the choice of handles, so they are factored once; each move of a handle costs only back substitutions.
It is the classic tool for puppet-style animation of 2D drawings.

## In plain words

Draw a figure, fill it with small triangles, and pin a few points.
Now drag one pin.
The figure should bend like a sheet of rubber, not stretch like soft cheese.
The method does this in two quick passes.
The first pass asks each triangle to keep its shape but lets it grow or shrink, because that makes the problem easy to solve.
The second pass takes each triangle from the first pass, turns a copy of the original triangle to match it, and then asks the mesh to fit these turned copies, which have the original size.
Each pass is one linear solve, so the figure moves as fast as the mouse.

## The problem

The input is a triangle mesh with the rest positions $v_1, \dots, v_n$ in the plane, a set $H$ of at least two handle vertices, and the target positions $q_k$ of the handles.
The output is new positions $v'$ with $v'_k = q_k$ for $k \in H$, such that each triangle of $v'$ is close to a rotated copy of the same triangle of $v$.
Let $R_{90}$ be the turn by 90 degrees.
For a triangle with the vertices $v_0, v_1, v_2$ in one of its three orders, the third vertex has fixed coordinates $(x, y)$ in the frame of the opposite edge: $v_2 = v_0 + x(v_1 - v_0) + yR_{90}(v_1 - v_0)$.
Step 1 minimizes

$$E_1(v') = \sum_{\text{triangles}}\ \sum_{\text{3 orders}} \big|v'_2 - v'_0 - x(v'_1 - v'_0) - yR_{90}(v'_1 - v'_0)\big|^2,$$

which is 0 exactly when every triangle is similar to its rest triangle.
Step 2 minimizes $E_2(v') = \sum_{\text{triangles}}\sum_{\text{edges } ij}|(v'_i - v'_j) - (w_i - w_j)|^2$, where $w$ is the fitted triangle of rest size.

## The algorithm

```pseudo id=main
REGISTER(v, triangles, H)
L1  for each triangle and each of its 3 vertex orders, compute (x, y) of the third vertex
L2  build the matrix G of E_1 and factor its block of the free vertices by Cholesky
L3  for each triangle, factor the 4 by 4 matrix of the fit; build the matrix of E_2 and factor its free block
MOVE(q)
L4  step 1: solve for the free vertices of v' that minimize E_1, with the handles at q
L5  for each triangle, fit the similar copy of its rest triangle closest to its step 1 position, and rescale it to the rest size about its centroid
L6  step 2: solve for the free vertices that minimize E_2 with the fitted triangles, for x and y separately
L7  return the step 1 and step 2 results
```

$E_1$ and $E_2$ are quadratic in the free vertices, and the handles enter only on the right side, so lines L4 and L6 are linear systems with the matrices of lines L2 and L3.
Line L5 has two unknown vertices $w_0$, $w_1$ for each triangle, with $w_2$ given by the frame relation, and minimizes $\sum_k|w_k - v'_k|^2$ over them, a 6 by 4 least squares problem whose 4 by 4 normal matrix depends only on the rest triangle.
The matrix of $E_2$ is the graph [Laplacian](/laplacian-matrix/) of the mesh edges, counted once per triangle, and its $x$ and $y$ systems are the same.

## Example

The mesh is a bar of $5 \times 1$ unit squares, each cut into 2 triangles: 12 vertices and 10 triangles, with the vertices $(i, j)$ for $i = 0..5$ and $j = 0, 1$.
The handles are the four end vertices.
The two right handles move up by $1.5$, to $(5, 1.5)$ and $(5, 2.5)$, and the left ones stay.
After step 1, the vertex that starts at $(2, 0)$ is at $(2.18, 0.54)$, and the vertex that starts at $(1, 1)$ is at $(0.88, 1.18)$.
After step 2 they are at about $(2.1903, 0.5898)$ and $(0.8972, 1.1624)$.
The bar bends into a smooth S and stays symmetric about its center $(2.5, 1.25)$.
The longest change of an edge length is about 13% after step 1 and about 17% after step 2: the handles are now $\sqrt{27.25} \approx 5.22$ apart instead of 5, and step 2 forbids the uniform growth that step 1 used to absorb this.

To see why step 2 is needed, scale the handles by 2 about the origin.
Step 1 then scales the whole mesh by 2 exactly, because a scaled mesh has $E_1 = 0$, and the free vertical edges have length 2.
After step 2 the free vertical edges have the lengths 1.08 to 1.13: the mesh is stretched between the handles, but its triangles keep close to their rest size.

## Correctness

The [proof](proofs/correctness.md) proves the following.
$E_1$ is 0 for every mesh that is a similarity image of the rest mesh, because the frame coordinates $(x, y)$ do not change under rotation, scale and translation.
With two handles at different positions, the free block of $G$ is positive definite, so step 1 has a unique minimizer, and the Cholesky factorization exists. With one handle it is singular, and the implementation raises an error.
If the handle targets are a rigid motion of the rest handles, the rigid image of the whole mesh has $E_1 = 0$, so step 1 returns it; every fitted triangle then equals its image, so $E_2 = 0$ there, and step 2 returns it too.
The fit of line L5, followed by the rescale, equals the rotation of the rest triangle about the centroids that minimizes the squared distances, the 2D [Kabsch](/kabsch-algorithm/) or Procrustes solution.
Each step is the exact minimizer of its energy, but the two steps together do not minimize a single energy, so the result is a heuristic for "as rigid as possible", not the minimizer of a rigidity energy.

## Complexity

Let $n$ be the number of vertices and $m$ the number of triangles.
Lines L1 and L3, apart from the factorizations, take $O(m)$ time.
The implementation uses dense Cholesky factorizations, which cost $O(n^3)$ time and $\Theta(n^2)$ memory, and each move costs $O(n^2)$ for the triangular solves plus $O(m)$ for line L5.
The matrices are sparse, with $O(1)$ entries per row for meshes of bounded degree, so a sparse Cholesky factorization with a fill-reducing order makes registration and each move much cheaper on large meshes.
Registration repeats only when the user adds or removes a handle.

## Properties

- **Handles met exactly (proved).** The handles are fixed values, not soft constraints.
- **Rigid motions reproduced (proved).** If the handles move rigidly, the whole mesh moves by the same rigid motion.
- **Uniform scale removed (proved for step 1, measured for step 2).** Step 1 reproduces a uniform scale of the handles exactly; step 2 pulls the triangles back toward their rest size.
- **Each step optimal (proved).** Step 1 is the unique minimizer of $E_1$ and step 2 of $E_2$ with the fitted triangles fixed.
- **No iteration.** The result is the same every time for the same handles, and its cost per move is fixed, unlike iterative methods.
- **Not a minimizer of rigidity.** Two steps give no guarantee that the result is the most rigid shape; large rotations within a short distance can still shear triangles.
- **No fold check.** Nothing stops a triangle from flipping under an extreme drag.

## Variants and improvements

- **Iterating the second step.** Fitting rotations to the result of step 2 and solving again is close to the local and global iteration of [as-rigid-as-possible deformation](/as-rigid-as-possible-deformation/) (Sorkine and Alexa 2007), which does decrease one rigidity energy at each step.
- **Surfaces.** On 3D surfaces, [Laplacian surface editing](/laplacian-surface-editing/) and the iterative method above play the same role.
- **Interpolation instead of handles.** [As-rigid-as-possible shape interpolation](/as-rigid-as-possible-shape-interpolation/) solves a different problem: it is given two complete shapes in correspondence and makes the shapes in between, by splitting the map of each triangle into a rotation and a stretch and interpolating them. Shape manipulation is given one shape and some handle targets, and has no second shape.
- **Weights from handles.** Linear methods such as [bounded biharmonic weights](/bounded-biharmonic-weights/) or [cage coordinates](/cage-based-deformation/) blend handle transforms with precomputed weights, which is faster but not adapted to the drag.
- **Parameterization.** The same rotation fitting appears in [ARAP parameterization](/arap-parameterization/), which flattens a surface with little distortion.

## When to use it

Use it to animate a 2D drawing, a character or a logo, by dragging a few points, when the motion should look like bending rather than stretching.
It needs a triangle mesh of the shape, which is easy to make from an outline with a [Delaunay triangulation](/delaunay-triangulation/).
For 3D surfaces, use [as-rigid-as-possible deformation](/as-rigid-as-possible-deformation/); for a 2D shape with a cage around it and no mesh, use [Green coordinates](/green-coordinates/) or another [cage method](/cage-based-deformation/).

## Pitfalls

- **One handle.** With a single handle, step 1 has no unique solution: a rotation and a scale about the handle cost nothing. Use at least two handles.
- **Order of the steps.** Step 2 needs the step 1 result only to fit the triangles; solving step 2 alone, with the rest triangles unrotated, gives a stiff shape that does not turn.
- **Refactoring.** The factorizations depend on which vertices are handles; adding a handle needs a new registration, but moving a handle does not.
- **Coarse meshes.** Few, large triangles cannot bend smoothly; use a fine and well-shaped triangulation.
- **Folding.** A drag past the shape can flip triangles; check the sign of each triangle area if this matters.

## Implementations

## History

Igarashi, Moscovich and Hughes presented the method at SIGGRAPH 2005, with an interface in which the user places and drags handles on a 2D shape.
It followed the as-rigid-as-possible interpolation of Alexa, Cohen-Or and Levin (2000), which used the same idea of rigid triangles for morphing.
Its two-step solution made it fast enough for live puppetry, and Sorkine and Alexa (2007) later used an iteration that minimizes a rigidity energy on surfaces.

## References
