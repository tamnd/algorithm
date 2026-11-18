---
tag: 5KAMME
kind: algorithm
slug: roam-terrain
name: ROAM
aliases:
- real-time optimally adapting meshes
area: graphics-and-signals/real-time-rendering
level: advanced
summary: Keep a terrain triangulation as a binary triangle tree and split and merge triangles with two priority queues to meet an error bound each frame.
model: real-ram
complexity:
  vars: {M: the grid size in cells along each side, L: the number of leaves at the start and at the end of the frame, s: the number of splits and merges in the frame}
  time: {worst: O((L + s) log(L + s))}
  space: {extra: Θ(M^2)}
properties: {stable: false, in_place: true, adaptive: false, online: true, deterministic: true, comparison: false, recursive: false}
history:
  year: 1997
  people: [Mark Duchaineau, Murray Wolinsky, David E. Sigeti, Mark C. Miller, Charles Aldrich, Mark B. Mineev-Weinstein]
  note: ROAM was presented at IEEE Visualization 97. It uses a triangle bintree with forced splits, nested wedgie bounds, and a split queue and a merge queue that carry the mesh of one frame to the next.
prereqs: [level-of-detail, priority-queue, binary-tree]
see_also: [view-dependent-refinement, geometry-clipmaps, geomorphing, binary-heap, quadtree, frustum-culling, triangulation]
sources:
  - paper: doi:10.1109/VISUAL.1997.663860
    title: Mark Duchaineau, Murray Wolinsky, David E. Sigeti, Mark C. Miller, Charles Aldrich and Mark B. Mineev-Weinstein, ROAMing terrain, real-time optimally adapting meshes, Proceedings of IEEE Visualization 97, 81 to 88
    locator: Section 4.1 (the triangle bintree), Section 4.2 (forced splits, Figure 5), Section 5.1 (the split queue and the optimality), Section 5.2 (the merge queue), Section 6.1 (the wedgie thickness, Equation 1), Section 6.2 (the screen distortion, Equations 2 and 3) and Section 7.1 (frustum culling)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: the part on terrain level of detail in the chapter on acceleration algorithms (general locator)
---

ROAM keeps a terrain as the leaves of a binary tree of right triangles, and each frame it splits the leaves with the largest error and merges the pairs with the smallest error, with one priority queue for each. A split that would leave a crack first splits the coarser neighbor across the base, so the mesh has no T-junctions at any time. [View-dependent refinement](/view-dependent-refinement/) does the same kind of local work on any progressive mesh with stored records, and [geometry clipmaps](/geometry-clipmaps/) use fixed nested grids in place of a tree. ROAM needs only the height grid and a bound per triangle, which it computes once.

## In plain words

Cut a square of terrain along a diagonal into two triangles. Any triangle of this kind can be cut again, from its right angle to the middle of its long side, into two smaller triangles of the same shape. Repeating this gives finer and finer meshes.

ROAM keeps a mesh made of such triangles. For each one it knows, from a table made at the start, how far the flat triangle can be from the true ground below it. Each frame it cuts the triangles whose error looks large from where the viewer is, and joins pairs of triangles whose error looks small. If a cut would make a gap with a larger neighbor, it cuts that neighbor first. The mesh of one frame is the start for the next, so a small move of the viewer gives few changes.

## The problem

The input is a height grid $h$ on the points $(x, y)$ with $0 \le x, y \le M$ and $M = 2^k$, the position of the eye, a priority $p(T)$ for each triangle and an error bound $\varepsilon$. A *bintree triangle* $T = (a, v_0, v_1)$ has its right angle at the apex $a$ and the base $v_0 v_1$. Its children are $(c, a, v_0)$ and $(c, v_1, a)$ with $c$ the midpoint of the base. The two roots split the square along a diagonal. The *partner* of $T$ is the triangle of the same level across its base; together they form a *diamond*. A mesh is the set of leaves of a cut of the tree. It is *conforming* when no vertex of a leaf lies inside an edge of another leaf. The output, each frame, is a conforming mesh in which every leaf has $p(T) \le \varepsilon^2$, with as few triangles as possible. The paper writes the height as $z$; this page uses $h$.

## The algorithm

```pseudo id=main
FORCE-SPLIT(mesh, t)                               ▷ t is a leaf with children
L1  stack ← [t]
L2  while the stack is not empty do u ← the top; if u is not a leaf then pop u and go on
L3      b ← the leaf with the base of u as an edge, or nil on the border
L4      if b ≠ nil and the base of b is not the base of u then push b and go on
L5      split u, and split b if b ≠ nil; pop u

UPDATE(mesh, p, ε)                                 ▷ one frame
L6  Qs ← a max-heap of the leaves by p
L7  while p(top of Qs) > ε^2 do pop T; if T is a leaf then FORCE-SPLIT(mesh, T) and push the new leaves
L8  Qm ← a min-heap of the mergeable diamonds by the larger p of the two; while p(top of Qm) ≤ ε^2 do merge it and push the parent diamonds that become mergeable
L9  return mesh

WEDGIES(tree)                                      ▷ once, before the first frame
L10 for each triangle T of the full tree, finest first do
L11     e_T ← 0 for a leaf, else max(e_T0, e_T1) + |h(c) - (h(v0) + h(v1))/2|

L12 p(T) = e_T^2 / max(dist(eye, T)^2, d0^2)       ▷ the priority
```

Line L4 is the forced split of Section 4.2 of the paper. In a conforming mesh, the leaf across the base of $u$ is either the partner of $u$, or a triangle one level coarser whose leg is the base of $u$. In the second case $b$ must be split first; the split of $b$ makes the partner of $u$, and the next pass splits the diamond.

Lines L10 and L11 compute the *wedgie thickness* of Section 6.1, Equation 1: the true surface lies within $e_T$ of the plane of $T$ above or below each point of $T$. A *mergeable* diamond is a split triangle and its partner whose four children are all leaves.

Line L12 is the priority of the code: the squared wedgie over the squared distance in the domain from the eye to the triangle, with a floor $d_0$ against a division by zero. It is a heuristic in place of the screen distortion of Section 6.2, which projects the wedgie with the camera. It is squared so that it stays rational, and it is *monotone*: a child never has a larger priority than its parent. The value of $d_0$ is a tuning.

## Example

**A forced split.** Take $M = 4$, all heights 0 except $h(3, 3) = 4$. The five triangles with a nonzero wedgie have $e_T = 4$. Asking for the leaf that holds the point $(3.5, 3.25)$ at each step gives these calls of FORCE-SPLIT.

| step | the leaf that is asked for | triangles split | leaves after |
|---|---|---|---|
| 1 | the root $((4, 4), (0, 4), (4, 0))$ | 2, a diamond of the two roots | 4 |
| 2 | $((2, 2), (4, 0), (4, 4))$ | 1, its base is on the border | 5 |
| 3 | $((4, 2), (4, 4), (2, 2))$ | 3 | 8 |
| 4 | $((3, 3), (4, 2), (4, 4))$ | 1, its base is on the border | 9 |

At step 3 the base of the leaf goes from $(4, 4)$ to $(2, 2)$, and the leaf across it is the coarser $((2, 2), (4, 4), (0, 4))$, for which this base is a leg. Line L4 pushes it, line L5 splits it, which makes the partner $((2, 4), (2, 2), (4, 4))$, and the next pass splits the diamond. So 3 triangles are split, and the point $(3, 3)$ enters the mesh without a T-junction. Step 4 is not needed for accuracy: its triangle has $e_T = 0$. UPDATE with $\varepsilon = 0$ from any eye gives the 8 leaves after step 3, the smallest conforming mesh that shows the surface exactly.

**Error bounds.** On an $8 \times 8$ grid with random heights from 0 to 10 (the seed 1), the full tree has 254 triangles, and 126 of them have children. The two roots have the wedgies $55/2$ and 33. With the eye over the point $(1, 1)$ and $d_0 = 1$, UPDATE from the two roots gives these meshes.

| $\varepsilon$ | 1/4 | 1/2 | 1 | 2 |
|---|---|---|---|---|
| leaves | 116 | 110 | 88 | 56 |

With $\varepsilon = 1/2$, moving the eye from $(1, 1)$ to $(2, 1)$ and running UPDATE on the old mesh splits 2 triangles and merges none, so the mesh goes from 110 to 112 leaves. The result equals the mesh that a fresh run from the two roots gives for the new eye.

## Correctness

The proof file gives the full arguments, and the tests check them on random grids.

- **The wedgies.** For every triangle $T$ and point $q$ in it, the surface of the full grid differs from the plane of $T$ by at most $e_T$, and $e_{T_0}, e_{T_1} \le e_T$ (a proved property, by induction from the finest level).
- **Forced splits.** From a conforming mesh, FORCE-SPLIT ends, splits $t$, keeps the mesh conforming after each split, and splits at most $2(\ell + 1)$ triangles for a leaf of level $\ell$ (a proved property).
- **One frame.** With the monotone priority of line L12, UPDATE from any conforming mesh ends with the split set equal to the smallest set that holds every triangle with $p > \varepsilon^2$ and is closed under parents and partners. So the result does not depend on the mesh of the last frame (a proved property).
- **Optimality.** That mesh has the fewest leaves among all conforming meshes whose leaves have $p \le \varepsilon^2$, and it is the only one with that number. This is the optimality claim of Section 5.1 in a precise form (a proved property). The test checks it by enumerating all 5489 conforming meshes of the $4 \times 4$ grid.

The claim needs a monotone priority. A priority that can grow from a parent to a child can hide a child with a large error below a parent with a small one, and the split phase then stops before the child is reached. Any other priority, such as the screen distortion of the paper, must be checked for this property before the optimality claim is used.

## Complexity

Lines L10 and L11 visit each of the $4M^2 - 2$ triangles of the full tree once, so the wedgies take $\Theta(M^2)$ time and space. For a frame that starts and ends with at most $L$ leaves and makes $s$ splits and merges, the code puts $O(L + s)$ entries in the two heaps, each at $O(\log(L + s))$, so a frame costs $O((L + s) \log(L + s))$ in the worst case. The paper keeps both queues from frame to frame and recomputes only the priorities that change, so the work of a frame is about proportional to the number of changes (Section 5.2). In the code the split heap is built from all leaves each frame, which is simpler and shows the result, not the speed.

## Properties

- **Conforming at every step.** No split or merge makes a crack or a T-junction (a proved property).
- **Independent of history.** With a monotone priority and a fixed $\varepsilon$, the mesh of a frame depends only on the view, not on the mesh before it (a proved property).
- **Smallest.** No conforming mesh with fewer triangles meets the bound at every leaf (a proved property).
- **Coherent.** A small move of the eye gives few splits and merges; the example moves the eye by one cell and splits 2 triangles (a measurement).
- **Pops.** A split changes the surface at once. The change is at most the wedgie of the triangle, so a small $\varepsilon$ keeps it small on the screen, but it is still a jump.

## Variants and improvements

- **Screen distortion.** The paper projects the wedgie with the camera, so the error is in pixels and a wedgie seen along the line of sight counts little (Section 6.2, Equations 2 and 3).
- **Frustum culling.** Each triangle keeps a label for each plane of the view frustum: inside, outside or across. The children of a triangle that is inside a plane are inside it too, so only the labels across a plane need a new test (Section 7.1). See [frustum culling](/frustum-culling/).
- **A triangle budget.** The queues can stop at a target number of triangles in place of an error bound, so that the cost of a frame stays about fixed (a tuning).
- **Morphs.** Each split and merge can blend the new vertex from the midpoint of the base to its height over a few frames, as in [geomorphing](/geomorphing/).
- **Patches.** Later systems refine patches of many triangles in place of single triangles, so that the GPU gets large batches. [Geometry clipmaps](/geometry-clipmaps/) take this further with fixed grids.

## When to use it

ROAM fits a height field on a regular grid that is seen from near and far at the same time, as in a flight simulator, when the CPU builds the mesh each frame and a fixed error bound or a fixed triangle count is wanted. On current GPUs, the work per triangle and the many small changes make it slower than methods that draw large fixed grids, such as [geometry clipmaps](/geometry-clipmaps/). For meshes that are not height fields, use [view-dependent refinement](/view-dependent-refinement/).

## Pitfalls

- **Splitting one side of a diamond.** If line L5 splits $u$ and not its partner $b$, the midpoint of the shared base is a vertex of $u$'s children inside an edge of $b$, and the mesh has a T-junction that can show a crack.
- **No forced split.** If line L4 is left out and line L5 splits $u$ when $b$ is coarser, the new vertex $c$ lies inside a leg of $b$, and the mesh has a T-junction there.
- **A wedgie that is not nested.** If line L11 uses only the gap $|h(c) - (h(v_0) + h(v_1))/2|$ without the children, the value is not a bound: a parent with a gap of 0 hides children with a large error, and the split phase stops too early.
- **The wrong order.** Line L10 must visit the finest triangles first; from coarse to fine, line L11 reads wedgies of the children that are not yet computed.
- **No floor in the priority.** Line L12 with $d_0 = 0$ divides by zero when the eye is above the triangle.
- **A distance to one point.** If line L12 uses the distance to the center of $T$ in place of the nearest point of $T$, a child can be nearer to the eye than its parent's center, the priority is not monotone, and the result of a frame is no longer the smallest accurate mesh.
- **Merging a half diamond.** If line L8 merges a triangle without its partner, the result has a T-junction at the midpoint of their base.

## Implementations

## History

Lindstrom and others had shown continuous terrain level of detail on regular grids at SIGGRAPH 96. Duchaineau, Wolinsky, Sigeti, Miller, Aldrich and Mineev-Weinstein presented ROAM at IEEE Visualization 97. The paper put the forced splits of the triangle bintree, the nested wedgie bounds and the two queues together, and it gave the optimality of the split queue for monotone priorities. Many terrain engines of the following years used ROAM or variants of it. As GPUs grew, methods that send large fixed blocks of triangles, such as [geometry clipmaps](/geometry-clipmaps/) in 2004, took its place in many systems.

## References
