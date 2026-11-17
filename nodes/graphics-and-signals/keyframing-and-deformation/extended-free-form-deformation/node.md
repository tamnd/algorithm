---
tag: 7CMXN6
kind: algorithm
slug: extended-free-form-deformation
name: Extended free-form deformation
aliases:
- EFFD
area: graphics-and-signals/keyframing-and-deformation
level: advanced
summary: Free-form deformation with lattices of non-parallelepiped shape, such as cylinders, glued into one, so that the deformation follows the object.
solves: [shape-deformation]
model: real-ram
complexity:
  vars: {N: "the number of points to deform", c: "the number of chunks of the lattice", q: "the number of control points of one chunk", K: "the largest number of Newton steps per chunk"}
  time: {embed: "O(N c K q)", deform: "Θ(N q)"}
  space: {extra: "Θ(c q + N)"}
properties: {deterministic: true, exact: false, online: true, recursive: false}
prereqs: [free-form-deformation, newton-method-for-systems]
see_also: [free-form-deformation, cage-based-deformation, shape-deformation, newton-point-inversion, point-projection-onto-a-surface, bezier-patch, tensor-product-surface, barr-global-deformations]
sources:
  - paper: doi:10.1145/97879.97900
    title: "Sabine Coquillart, Extended free-form deformation: a sculpturing tool for 3D geometric modeling, SIGGRAPH 90, Computer Graphics 24(4), 187-196, 1990"
    locator: the whole paper (lattices built from joined elementary lattices such as cylinders, the embedding of a point by a numerical solve, and the deformation of the object with the lattice)
  - paper: doi:10.1145/15886.15903
    title: "Thomas W. Sederberg and Scott R. Parry, Free-form deformation of solid geometric models, SIGGRAPH 86, Computer Graphics 20(4), 151-160, 1986"
    locator: the whole paper (the parallelepiped lattice that EFFD generalizes)
---

Extended free-form deformation (EFFD) is [free-form deformation](/free-form-deformation/) with a lattice of any shape.
The lattice is made of several Bezier volumes, the chunks, glued along shared faces, so it can be a ring, a cylinder or a bent tube that hugs the object.
Because the undeformed lattice is no longer a box, the local coordinates of a point have no closed form, and EFFD finds them by Newton iteration.
After that, the deformation is the same as in FFD: each point follows its chunk.
Sabine Coquillart (1990) introduced the method as a sculpting tool, for example to dig a groove that runs around a cylinder.

## In plain words

In plain free-form deformation the object sits in a box of jelly with a grid of handles.
Many objects do not fit a box well: a bottle, a ring, a bent pipe.
EFFD lets you build the jelly from several pieces, each shaped like part of the object, glued side by side.
The catch is that a point of the object no longer knows at once where it sits inside its piece.
So, before the edit, each point searches for its place, by guessing and correcting the guess a few times.
When the search fails, the point lies outside every piece and is left alone.
Then the handles move, and each point follows its own piece as in plain FFD.

## The problem

The input is a lattice of $c$ chunks and a set of points.
Chunk $b$ is a Bezier volume $B_b(w; P) = \sum_{ijk} B_i^l(w_1)B_j^m(w_2)B_k^n(w_3)P_{g_b(i,j,k)}$ over $w = (w_1, w_2, w_3) \in [0, 1]^3$, where $g_b$ maps the local index of a control point to an index in one global list $P$.
Two chunks that share a face use the same global indices for its control points.
$P$ is the rest lattice and $P'$ the edited lattice.
The output is, for each point $X$, the point $X' = B_b(w; P')$, where $B_b(w; P) = X$, or NOT FOUND if no chunk holds $X$.

## The algorithm

$J_b(w)$ is the 3 by 3 Jacobian matrix of $B_b(\cdot\,; P)$ at $w$, computed from the derivatives of the Bernstein polynomials.

```pseudo id=main
EFFD(X, chunks, P, P')
L1  for each chunk b do
L2      w ← (1/2, 1/2, 1/2)
L3      repeat at most K times
L4          r ← B_b(w; P) - X
L5          if |r| < tol then leave the loop
L6          w ← w - J_b(w)^(-1) r
L7      if |r| < tol and w ∈ [0, 1]^3 then
L8          return B_b(w; P')
L9  return NOT FOUND
```

Lines L2 to L6 are Newton's method for the system $B_b(w; P) = X$ of three equations in three unknowns.
Line L7 accepts the result only if it converged and lies in the parameter cube; a solution outside the cube belongs to the extension of the polynomial, not to the chunk.
The embedding, lines L1 to L7, depends only on $P$, so it runs once; line L8 runs again each time the user edits $P'$.
The implementation also stops a chunk when $J_b$ is singular or the iterate runs away.

## Example

The lattice is a quarter of a thick ring and the next quarter, two chunks of degree $(2, 1, 1)$.
In the first chunk, $w_1$ runs along a quadratic arc with the control points $(r, 0)$, $(r, r)$, $(0, r)$, $w_2$ runs from the radius $r = 1$ to $r = 2$, and $w_3$ runs from the height $z = 0$ to $z = 1$.
The second chunk uses the arc $(0, r)$, $(-r, r)$, $(-r, 0)$, and the two chunks share the 4 control points of the face at 90 degrees.
The point $X = (1.125, 1.125, 0.5)$ is $B_1((1/2, 1/2, 1/2); P)$, and Newton's method from $(1/2, 1/2, 1/2)$ finds it in the first chunk at once.
Now move the two outer middle control points $(2, 2, 0)$ and $(2, 2, 1)$ to $(2.5, 2.5, 0)$ and $(2.5, 2.5, 1)$.
Each has the weight $B_1^2(1/2)B_1^1(1/2)B_k^1(1/2) = 1/8$ at $X$, so $X$ moves by $2 \cdot \frac18 \cdot (0.5, 0.5, 0) = (0.125, 0.125, 0)$ to $(1.25, 1.25, 0.5)$.
The point $(0.2, 0.2, 0.5)$ lies in the hole of the ring; Newton's method converges in neither chunk to a parameter in the cube, so it is NOT FOUND.
The tests check these values, the recovery of random parameters, and the continuity across the shared face.

## Correctness

If line L7 accepts $w$ for chunk $b$, then $B_b(w; P) = X$ within the tolerance, so $X$ lies in chunk $b$ and line L8 is the FFD of that chunk.
With $P' = P$, line L8 returns $B_b(w; P) \approx X$, so the rest lattice gives the identity; an affine map applied to all of $P$ gives the same map on the points, by the Bernstein identities of [free-form deformation](/free-form-deformation/).
On a shared face, both chunks reduce to the same Bezier patch of the shared control points, so the deformation is continuous across the face for every $P'$.
Newton's method converges quadratically from a start close enough to a solution where $J_b$ is invertible; this is a local result, and from $(1/2, 1/2, 1/2)$ it can fail or find a solution outside the cube.
The [proof](proofs/correctness.md) gives the details and the cases where the embedding can miss a point.

## Complexity

One Newton step evaluates $B_b$ and $J_b$ in $\Theta(q)$ time for a chunk with $q$ control points, plus $O(1)$ for the 3 by 3 solve.
Embedding a point costs $O(cKq)$ in the worst case, when it tries every chunk; a bounding box per chunk usually rejects most chunks at once.
After the embedding, each edit costs $\Theta(q)$ per point.
The lattice takes $\Theta(cq)$ memory, and each point stores its chunk and its $w$.

## Properties

- **Identity at rest (proved).** If the embedding converged, the rest lattice gives back the point, within the Newton tolerance.
- **Affine invariance (proved).** An affine map of the whole lattice gives the same map of the embedded points.
- **C0 across shared faces (proved).** Chunks that share control points on a face meet continuously for every edit.
- **Not C1 in general.** The derivatives across a shared face agree only if the neighbouring layers of control points satisfy the usual Bezier conditions; an edit that ignores them makes a crease.
- **Embedding is numerical.** Newton's method has only local convergence. The start, the iteration limit and the tolerance are tuning, not part of a proof.
- **Points outside do not move.** As in FFD, points with no chunk are left in place.

## Variants and improvements

- **Better starts.** Start Newton's method from the nearest sample of a precomputed grid of parameters, or subdivide the chunk until the point is close, to make the embedding robust.
- **Bounding boxes.** The convex hull property of Bezier volumes bounds each chunk by its control points, so a chunk whose box misses the point can be skipped.
- **Smooth junctions.** Keep the layers on both sides of a shared face collinear when editing, to get $C^1$ junctions.
- **Cages.** [Cage-based deformation](/cage-based-deformation/) uses a coarse mesh of any shape and closed-form coordinates, so it needs no Newton iteration at all.

## When to use it

Use EFFD when the deformation should follow a curved or ring-shaped part of an object, such as a groove around a cylinder or a bulge along a bent pipe, and a box lattice would put control points far from the surface.
If the lattice can be a box, plain [FFD](/free-form-deformation/) is simpler and has exact local coordinates.
If the shape is better framed by a coarse mesh than by Bezier chunks, use [cage-based deformation](/cage-based-deformation/).

## Pitfalls

- **Failed embedding.** A point near a chunk boundary or a fold of the rest lattice can be NOT FOUND or land in the wrong chunk. Check the residual, and try all chunks before giving up.
- **Folded rest lattice.** If $\det J_b$ changes sign inside a chunk, a point can have two parameters, and the deformation is not well defined there.
- **Tolerance.** A loose tolerance gives points that jump a little even at rest. The tests use $10^{-12}$ and accept parameters within $10^{-9}$ of the cube.
- **Shared indices.** Chunks that store their own copies of the shared face points instead of shared indices drift apart when only one copy moves.

## Implementations

## History

Coquillart presented EFFD at SIGGRAPH 1990 as a way to sculpt shapes that the box lattice of Sederberg and Parry could not follow.
She built lattices from elementary ones, such as cylindrical lattices, joined them, and then embedded the object numerically.
The cost and the fragility of the numerical embedding later pushed work toward cages with closed-form coordinates, such as mean value, harmonic and Green coordinates.

## References
