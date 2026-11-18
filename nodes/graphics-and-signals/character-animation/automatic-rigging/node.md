---
tag: FM8DXC
kind: algorithm
slug: automatic-rigging
name: Automatic rigging by heat diffusion
aliases:
- Pinocchio rigging
- bone heat weights
area: graphics-and-signals/character-animation
level: advanced
summary: Embed a template skeleton into a character mesh and compute skinning weights by heat diffusion from each bone over the surface.
solves: [character-skinning]
model: real-ram
complexity:
  vars: {n: "the number of surface vertices", B: "the number of bones", J: "the number of joints", C: "the number of candidate joint positions"}
  time: {embedding: "O(B C^2 n + J C^J log C)", weights: "O(n^2 B + n^3)"}
  space: {extra: "O(B C^2 + J C^J + n^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
prereqs: [linear-blend-skinning, a-star-search, cotangent-laplacian]
see_also: [bounded-biharmonic-weights, skinning-decomposition, character-skeleton, medial-axis, cholesky-decomposition, poisson-equation, harmonic-coordinates, bind-pose]
sources:
  - paper: doi:10.1145/1276377.1276467
    title: "Ilya Baran and Jovan Popović, Automatic rigging and animation of 3D characters, ACM Transactions on Graphics 26(3), SIGGRAPH 2007, article 72"
    locator: the skeleton embedding by a discrete search over the centers of medial spheres followed by a continuous refinement, and the attachment by the heat equation with one weight function per bone (general locator)
---

Automatic rigging takes a character mesh and a template skeleton, and returns the skeleton fitted inside the mesh together with skinning weights for [linear blend skinning](/linear-blend-skinning/).
Baran and Popović (2007) built it in two parts, in a system that they called Pinocchio.
The first part places the joints: it searches over a discrete set of points inside the mesh for the placement with the smallest sum of penalties, and then refines the result.
The second part computes the weights: each bone acts as a heat source, the heat spreads over the surface, and the steady state temperature of the bone at a vertex is its weight.
The weights are smooth, nonnegative and sum to 1, and they stay low on parts of the body that the bone cannot see.

## In plain words

To animate a character, you need a skeleton inside it and a rule that tells each vertex how much it follows each bone.
This method does both from a template, such as a generic human skeleton.
It first tries many ways to put the template joints inside the shape and scores each one: are the bones as long as they should be, do they point the right way, do they stay inside?
A best-first search finds the placement with the best score without trying all of them.
Then it heats each bone and lets the heat flow over the skin.
A vertex near the upper arm gets hot from the upper arm bone and stays cold for the leg bones.
Heat flows along the surface, not through the air, so a hand that rests on a leg does not get weight from the leg.

## The problem

The input is a closed surface mesh with vertices $x_j$, $j = 1, \ldots, n$, and a template skeleton: a tree of $J$ joints with a rest offset $o_j$ for the bone from the parent of $j$ to $j$.
The output is a position for every joint inside the mesh and a weight $w^i_j \ge 0$ per bone $i$ and vertex $j$, with $\sum_i w^i_j = 1$.

For the embedding, fix a set of $C$ candidate points inside the mesh.
An embedding assigns a candidate $a(j)$ to each joint, and its cost is $\sum_j \pi_j(a(\text{parent}(j)), a(j))$, a sum of nonnegative bone penalties.
The best embedding has the smallest cost.

For the weights, let $\Delta$ be the discrete Laplacian of the surface, $d(j)$ the distance from $x_j$ to the nearest bone that is visible from $x_j$ (the segment between them stays inside the mesh), and $H$ the diagonal matrix with $H_{jj} = c / d(j)^2$, or $H_{jj} = 0$ if no bone is visible.
Let $p^i_j = 1/k$ if bone $i$ is one of the $k$ nearest visible bones of $x_j$, else $p^i_j = 0$.
The weights of bone $i$ solve

$$-\Delta w^i + H w^i = H p^i.$$

## The algorithm

```pseudo id=main
RIG(mesh, template skeleton, candidates, c)
L1  embed the skeleton (lines L2 to L6), then make one bone per joint and its parent
L2      precompute the penalty of every bone for every pair of candidates, and its minimum low_j
L3      push the empty assignment with the priority low_1 + … + low_J
L4      pop the partial assignment with the smallest g + h, where h = the sum of low_j over the joints not placed yet
L5      if every joint is placed, return it
L6      else for each candidate c: place the next joint at c and push the result with g increased by its bone penalty
L7  build the Laplacian of the surface: the stiffness matrix K and the masses M
L8  for each vertex j: find its nearest visible bones; set H_jj and p^i_j
L9  factor K + M H by Cholesky, once
L10 for each bone i: solve (K + M H) w^i = M H p^i with the factor; return the weights
```

Lines L2 to L6 are [A* search](/a-star-search/) over partial assignments, with joints placed in an order where each parent comes before its children.
The heuristic $h$ adds the smallest possible penalty of every bone not placed yet, so it never overestimates the remaining cost.
The paper builds its candidates from the centers of spheres packed along the [medial axis](/medial-axis/) of the mesh and uses a branch and bound search that is close to A*.
It then refines the joint positions by a continuous optimization; the code does not.

Lines L7 to L10 are the equation of the problem in the weak form: $K$ is the stiffness matrix, so $-\Delta \approx M^{-1} K$, and multiplying by $M$ gives a symmetric system.
On a triangle mesh, $K$ is the [cotangent Laplacian](/cotangent-laplacian/).
The matrix does not depend on the bone, so one [Cholesky factorization](/cholesky-decomposition/) serves all bones.

The code in `impl/python` works in 2D.
The character is a simple polygon and its surface is the closed boundary, so $K$ has the entry $1/\ell_e$ for each edge of length $\ell_e$, and the mass of a vertex is half the length of its two edges.
The bone penalties are three terms of the same kind as the paper's: the relative length error squared, one minus the cosine of the angle to the template direction, and a fixed penalty when the bone leaves the shape.
The paper uses a larger set of nine penalties.

## Example

Take the square with the corners $(-1, -1)$, $(1, -1)$, $(1, 1)$, $(-1, 1)$ as the surface, with four vertices and four edges of length 2.
Bone A is the segment from $(-0.5, -0.5)$ to $(0.5, -0.5)$, and bone B is the segment from $(-0.5, 0.5)$ to $(0.5, 0.5)$.
The two lower corners have bone A as the nearest visible bone, at the distance $\sqrt{0.5}$, so with $c = 1$, $H_{jj} = 2$; the upper corners have bone B at the same distance.

Each vertex has the mass $2$ and the stiffness entries $K_{jj} = 1$ and $-1/2$ for its two neighbors.
By symmetry, $w^A = (a, a, 1 - a, 1 - a)$.
The row of vertex 1 reads $a - \frac{1}{2} a - \frac{1}{2} (1 - a) + 4 a = 4$, so $5 a = 4.5$ and $a = 0.9$.

| vertex | $(-1, -1)$ | $(1, -1)$ | $(1, 1)$ | $(-1, 1)$ |
|---|---|---|---|---|
| $w^A$ | 0.9 | 0.9 | 0.1 | 0.1 |
| $w^B$ | 0.1 | 0.1 | 0.9 | 0.9 |

The weights sum to 1 at every vertex, and the heat leaks a little to the far side along the surface.
The tests check these numbers.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).
- **The embedding is optimal.** The heuristic is consistent: along an edge of the search tree, $g$ grows by a bone penalty, which is at least the $\text{low}_j$ that $h$ loses. So the first complete assignment that line L4 pops has the smallest cost.
- **The system has one solution.** If at least one vertex sees a bone, $K + M H$ is symmetric positive definite, so line L9 succeeds.
- **The weights sum to 1.** $K \mathbf{1} = 0$ and $\sum_i p^i_j = 1$ at every vertex with $H_{jj} > 0$, so $\sum_i w^i$ solves the system with the right side $M H \mathbf{1}$, whose solution is $\mathbf{1}$.
- **The weights are nonnegative.** $K + M H$ has nonpositive entries off the diagonal and is positive definite, so its inverse has no negative entries, and the right side has none.

The search is exact for the discrete problem, but the result is only as good as the penalties and the candidates.
The heat weights are a model, not the solution of a problem about the best deformation.

## Complexity

The costs are in the real RAM model.
The penalty tables take $O(B C^2)$ evaluations, and each tests the bone against the $n$ edges of the boundary, so $O(B C^2 n)$.
The search can visit up to $O(C^J)$ partial assignments, each with a heap operation of cost $O(\log C^J) = O(J \log C)$, which gives the exponential worst case $O(J C^J \log C)$.
A good heuristic and good penalties make the search visit far fewer nodes in practice; in an L-shaped example with 48 candidates and three joints, A* expands 55 nodes instead of the $48^3$ assignments of a brute force search.
For the weights, the visibility tests cost $O(n^2 B)$, the dense Cholesky factorization $O(n^3)$, and each solve $O(n^2)$.
The matrix is sparse, so a sparse Cholesky factorization costs much less on real meshes.

## Properties

- Automatic: the only inputs are the mesh and a template skeleton.
- Smooth weights: the weights are harmonic away from the vertices with $H_{jj} > 0$.
- Convex weights: the weights are nonnegative and sum to 1 at every vertex.
- Aware of the surface: heat flows along the surface, and visibility keeps a bone from attaching to a vertex that it cannot see.
- Not local by construction: every weight is positive on the connected part of the surface that holds its heat source, even if it is very small.

## Variants and improvements

- **Bounded biharmonic weights.** [Bounded biharmonic weights](/bounded-biharmonic-weights/) minimize a biharmonic energy with explicit bounds, which gives smoother weights and supports points and cages as handles.
- **Weights from examples.** [Skinning decomposition](/skinning-decomposition/) fits weights and bones to a sequence of example meshes instead of a template.
- **Volumetric weights.** Solving the heat equation in the volume instead of on the surface avoids the visibility test, at the price of a volume mesh.
- **Other skinning models.** The weights also work with [dual quaternion skinning](/dual-quaternion-skinning/).

## When to use it

Use automatic rigging when you need a working rig quickly for many characters of the same kind, such as humanoids, and an artist can fix the result afterwards.
It works best on closed meshes with a clear shape, where the limbs are separated.
Use [bounded biharmonic weights](/bounded-biharmonic-weights/) if you need smoother weights or other kinds of handles.

## Pitfalls

- **Bones on the surface.** If a bone touches the surface, $d(j) = 0$ and $H_{jj}$ is infinite. The code rejects such bones.
- **Broken meshes.** Holes and parts that are not connected stop the heat from spreading, and a part without a visible bone gets weights only from the parts that it is connected to.
- **Visibility near contacts.** A hand that touches the hip can see the hip bone, and the weights near the contact need a manual fix.
- **Penalties that do not match the shape.** A creature with an unusual body plan needs other penalties or another template. In the paper, the search found a correct embedding for most but not all of the test characters.
- **The choice of c.** A larger $c$ makes the weights closer to the nearest bone weights $p^i$ and the joints sharper; a smaller $c$ makes the weights smoother. The test with $c = 10^7$ shows that the weights tend to $p^i$.

## Implementations

## History

Before Pinocchio, an artist placed the skeleton by hand and painted the weights, which took hours per character.
Baran and Popović (2007) automated both steps with a template skeleton: a discrete embedding scored by penalties, followed by heat diffusion for the weights.
In their tests, the embedding was correct for 13 of 16 characters.
The heat weights, often called bone heat weights, became the default automatic weights in common animation tools, and later work such as [bounded biharmonic weights](/bounded-biharmonic-weights/) built on the same idea of weights as the solution of a partial differential equation.

## References
