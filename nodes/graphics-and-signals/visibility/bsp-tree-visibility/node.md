---
tag: Q78XXG
kind: algorithm
slug: bsp-tree-visibility
name: BSP tree visibility
aliases:
- BSP painter's algorithm
- BSP tree hidden surface removal
- BSP back-to-front traversal
area: graphics-and-signals/visibility
level: advanced
summary: Build a BSP tree of the polygons once. For each viewpoint, a traversal that visits the far side of each node first gives a correct back-to-front painting order.
solves: [hidden-surface-removal]
model: real-ram
complexity:
  vars: {n: the number of polygons, m: the number of fragments in the tree, P: "the number of covered pixels, summed over all fragments"}
  time: {worst: Θ(m + P), average: Θ(m + P), best: Θ(m + P)}
  space: {extra: O(m)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1980
  people: [Henry Fuchs, Zvi M. Kedem, Bruce F. Naylor]
  note: Fuchs, Kedem and Naylor gave the BSP tree and its back-to-front traversal for visible surface generation at SIGGRAPH 1980. Gordon and Chen gave a front-to-back display of BSP trees in 1991.
prereqs: [bsp-tree, painters-algorithm, hidden-surface-removal]
see_also: [newell-newell-sancha-algorithm, z-buffer, occlusion-culling, portal-culling, back-face-culling, potentially-visible-set, object-space-vs-image-space, ray-casting]
sources:
  - paper: doi:10.1145/800250.807481
    title: Henry Fuchs, Zvi M. Kedem and Bruce F. Naylor, On visible surface generation by a priori tree structures, Proceedings of SIGGRAPH 1980, Computer Graphics 14(3)
    locator: the tree of the polygons of a scene and the back-to-front traversal from any viewpoint
  - paper: doi:10.1109/38.90569
    title: Dan Gordon and Shuhong Chen, Front-to-back display of BSP trees, IEEE Computer Graphics and Applications 11(5), 1991, pages 79 to 85
    locator: the whole paper
  - paper: doi:10.1007/BF02187806
    title: Michael S. Paterson and F. Frances Yao, Efficient binary space partitions for hidden-surface removal and solid modeling, Discrete and Computational Geometry 5, 1990
    locator: the O(n^2) bound for the size of a BSP of n triangles in space
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 12, Binary Space Partitions (the painter's algorithm with a BSP tree, and BSPs in three dimensions)
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, 1990
    locator: Chapter 15, Section 15.5 (list-priority algorithms, binary space-partitioning trees)
---

BSP tree visibility solves [hidden surface removal](/hidden-surface-removal/) with a [BSP tree](/bsp-tree/) of the polygons of a scene. The tree is built once, and the splits that it makes remove each cycle of overlap. For each viewpoint, a traversal visits at each node first the side of the plane that does not hold the viewer, then the polygons on the plane, then the side of the viewer. This gives a valid back-to-front order for the [painter's algorithm](/painters-algorithm/) in time linear in the size of the tree. The reverse traversal gives a front-to-back order, which can stop when the image is full. Fuchs, Kedem and Naylor introduced the method in 1980.

## In plain words

Think of a wall in a room. If you stand on one side of the wall, nothing on the other side can be in front of something on your side. So you may draw the far side of the wall first, then the wall, then your side.

A BSP tree stores the scene as walls inside walls. Each node is a plane, with the polygons that lie on it, and its two children hold the parts of the scene on the two sides. To draw the scene, start at the top node. Find the side of the plane where the viewer stands. Draw the other side first, by the same rule, then the polygons on the plane, then the side of the viewer. The tree does not depend on the viewer, so the same tree works when the viewer moves. Only the choice of side at each node changes.

## The problem

The input is a BSP tree of planar [convex polygons](/convex-polygon/) in space, built as on the [BSP tree](/bsp-tree/) page with planes instead of lines, a viewer at a point $E$, and an image of $W \times H$ [pixels](/pixel/). Pixel $(i, j)$ is the point sample $S = (i + \tfrac12, j + \tfrac12, 0)$ on the image plane $z = 0$, and it shows the polygon that the ray $E + t(S - E)$, $t > 0$, meets first. This is a perspective view with the center $E$; an orthographic view is the limit of a viewer at infinity. A polygon whose plane holds $E$ is seen edge on and covers no pixel.

Each node $t$ has a plane with the side function $\sigma_t(X) = n_t \cdot X - d_t$, a list $t.on$ of fragments in the plane, a subtree $t.front$ of fragments in $\sigma_t \ge 0$ and a subtree $t.back$ of fragments in $\sigma_t \le 0$. An order of the fragments is *valid* for $E$ when no fragment is in front of a later fragment along a pixel ray.

## The algorithm

Both traversals use an explicit stack of pairs (node, action), so the depth of the tree does not limit them.

```pseudo id=main
BSP-PAINT(T, E, W, H)                       ▷ back to front
L1  stack ← [(root of T, visit)]
L2  while stack is not empty do
L3      pop (t, a) from stack
L4      if t = nil then continue
L5      if a = draw then paint each fragment of t.on over the image; continue
L6      if σt(E) ≥ 0 then (near, far) ← (t.front, t.back) else (near, far) ← (t.back, t.front)
L7      push (near, visit), (t, draw), (far, visit)          ▷ far is popped first

BSP-FRONT-TO-BACK(T, E, W, H)               ▷ write only empty pixels
L8  stack ← [(root of T, visit)]; filled ← 0
L9  while stack is not empty and filled < W·H do
L10     pop (t, a) from stack; if t = nil then continue
L11     if a = draw then for each fragment f of t.on, write f to each empty pixel that f covers, and count it in filled; continue
L12     choose near and far as in L6; push (far, visit), (t, draw), (near, visit)    ▷ near is popped first
```

To paint a fragment at line L5 means to write it to each pixel whose ray meets it. In a renderer this is a [scan conversion](/triangle-rasterization/) after the projection; the implementation tests each pixel ray exactly. When the viewer is on the plane, $\sigma_t(E) = 0$, the fragments of $t.on$ are edge on, and each order of the two sides is valid; line L6 then takes the front side as near.

BSP-FRONT-TO-BACK draws the nearest fragments first, so a pixel that is written is final. It keeps a mask of the written pixels and stops when all are full. Gordon and Chen used a structure of free spans per scanline in place of the mask, so that a covered span costs no work.

## Example

Take the three strips of the [painter's algorithm](/painters-algorithm/) page, which overlap in a cycle, moved to $z < 0$: $S_1$ has the corners $(0,1,-7), (8,1,-5), (8,2,-5), (0,2,-7)$, $S_2$ has $(5,0,-8), (6,0,-8), (2,6,-4), (1,6,-4)$ and $S_3$ has $(1,0,-4), (2,0,-4), (7,6,-10), (6,6,-10)$. No depth order of the three is correct. The build takes the strips in this order and makes 6 fragments.

| node | plane | fragments on it | children |
|---|---|---|---|
| root | of $S_1$ | $S_1$ | front: $S_{2a}$, back: $S_{2b}$ |
| $S_{2a}$ | of $S_2$ | the part of $S_2$ in front of the plane of $S_1$ | front: $S_{3a}$ |
| $S_{2b}$ | of $S_2$ | the part of $S_2$ behind the plane of $S_1$ | front: $S_{3b}$, back: $S_{3c}$ |
| $S_{3a}$ | of $S_3$ | the part of $S_3$ in front of the plane of $S_1$ | none |
| $S_{3b}$ | of $S_3$ | the middle part of $S_3$ | none |
| $S_{3c}$ | of $S_3$ | the part of $S_3$ with $y \ge 12/5$ | none |

The plane of $S_1$ cuts $S_2$ along the segment from $(16/5, 27/10, -31/5)$ to $(4, 3, -6)$, and it also cuts $S_3$. The plane of $S_2$ cuts the back part of $S_3$ again, along the line $y = 12/5$, $z = -32/5$.

From the viewer $E = (4, 3, 40)$, the root has $\sigma(E) = 368 > 0$, so the back subtree comes first. At $S_{2b}$ the viewer is again in front, so the order there is $S_{3c}, S_{2b}, S_{3b}$. Then comes $S_1$, then the front subtree: $S_{2a}$, then $S_{3a}$. The full order is $S_{3c}, S_{2b}, S_{3b}, S_1, S_{2a}, S_{3a}$. From the viewer $(4, 3, -60)$, below the scene, each sign changes, and the order is the exact reverse. In both cases the painted image of $8 \times 6$ pixels is equal to a nearest-hit test of each pixel ray against all polygons, and BSP-FRONT-TO-BACK gives the same image.

The image from $E = (4, 3, 40)$, with the top row $j = 5$ first and the digit $k$ for $S_k$:

```
.2......
..2..3..
...23...
...2....
.1311111
.3...2..
```

The perspective makes the strips smaller than in the orthographic view of the painter's page, because the image plane is between the viewer and the scene.

## Correctness

Take a node $t$ with $\sigma_t(E) > 0$. A segment from $E$ to a point $y$ with $\sigma_t(y) \ge 0$ has $\sigma_t > 0$ at each point before $y$, because $\sigma_t$ is affine along the segment. So it does not meet a fragment of the back subtree, which lies in $\sigma_t \le 0$, before it reaches $y$. Hence no fragment of the back subtree hides a part of a fragment in $t.on$ or in the front subtree, and the fragments in $t.on$ are in one plane and do not hide each other. The case $\sigma_t(E) < 0$ is symmetric, and for $\sigma_t(E) = 0$ a ray with $t > 0$ meets the plane at most at its start, so each order is valid. By induction on the tree, BSP-PAINT outputs a valid order, so the last fragment painted at a pixel is the nearest one. BSP-FRONT-TO-BACK uses the reverse order, so the first fragment written at a pixel is the nearest one. The full proof is below.

## Complexity

Each node is pushed once for a visit and once for a draw, so the traversal takes $\Theta(m)$ time for $m$ fragments, besides the painting. The painting takes time proportional to $P$, the number of pixels that the fragments cover, with scan conversion. So BSP-PAINT takes $\Theta(m + P)$ time for each viewpoint, and the extra space is $O(m)$ for the stack. The tree is built once, before the frames: with a random order of the polygons, Paterson and Yao showed that an autopartition of $n$ triangles in space has $O(n^2)$ expected fragments, and some sets of $n$ triangles need $\Omega(n^2)$ fragments in any BSP. See the [BSP tree](/bsp-tree/) page for the build and the bounds. In practice $m$ is a small multiple of $n$ for a good choice of planes.

BSP-FRONT-TO-BACK can stop after the first fragments if they fill the image. In the worst case it still visits all $m$ nodes. Its time on covered pixels is the cost of the test "is this pixel empty", which a span structure makes small.

The implementation tests all $WH$ pixel rays for each fragment, so its painting costs $\Theta(mWH)$ ray tests.

## Properties

- **Exact for each viewpoint.** The order is valid for each $E$, with no tests between polygons at run time. Only one side test per node depends on $E$.
- **View independent build.** The tree does not depend on $E$, so it suits a static scene and a moving viewer. A moving object must be inserted at each frame, or drawn by another method such as the [z-buffer](/z-buffer/).
- **No depth buffer.** The back-to-front paint needs only the image. The front-to-back form needs a mask of one bit per pixel.
- **Back to front for blending.** The order is correct for translucent polygons that are blended with the *over* operator.
- **Overdraw.** BSP-PAINT writes each covered pixel once per fragment. The front-to-back form writes each pixel once.

## Variants and improvements

- **Front to back with spans.** Gordon and Chen keep, for each scanline, the spans that are still empty, and clip each fragment to them. Each pixel is written once, and the traversal can stop early.
- **Culling during the traversal.** Store a bounding box at each node. Skip a subtree whose box is outside the view frustum ([frustum culling](/frustum-culling/)) or hidden by the pixels already written ([occlusion culling](/occlusion-culling/)). Skip a fragment that faces away from $E$ ([back-face culling](/back-face-culling/)).
- **Leaf BSP trees and cells.** Store the convex cells of space at the leaves. The cells and the openings between them give the [potentially visible sets](/potentially-visible-set/) and [portal culling](/portal-culling/) of indoor scenes.
- **Ray casting.** A walk of the tree from front to back along one ray finds the first hit, as in [ray casting](/ray-casting/).

## When to use it

Use a BSP tree for a static scene with a moving viewer when you need a correct order with no depth buffer, for example on hardware with no z-buffer, for blended translucent geometry, or for vector output. Early 3D games drew their static maps front to back with a BSP tree. On current hardware, the [z-buffer](/z-buffer/) handles opaque geometry, and BSP trees are used mainly for the order of translucent faces, for collision tests and for the cells of portal systems.

## Pitfalls

- **Swapping near and far.** If line L7 pushes the far side last, the near side is painted first, and far fragments overwrite near ones. In BSP-PAINT, far must be popped first; in BSP-FRONT-TO-BACK, near must be popped first.
- **Using the view direction instead of the viewer position.** The side test of line L6 uses the point $E$, not the direction of view. Under perspective, a plane can face the view direction while $E$ is on its back side.
- **Overwrites in the front-to-back order.** BSP-FRONT-TO-BACK must not overwrite a written pixel. With overwrites it shows the farthest fragment.
- **A changed scene.** The order is valid only for the fragments in the tree. A polygon added outside the tree, or a moved polygon, can make the image wrong.
- **Rounding in the build.** In floating point, a fragment near a plane can go to the wrong side. Use a tolerance band in the build and put fragments in the band on the plane list, or use exact arithmetic as in the implementation.

## Implementations

## History

Schumacker and others used fixed priority orders for clusters of faces in flight simulators at General Electric in 1969. Fuchs, Kedem and Naylor generalized the idea in 1980 to the BSP tree, which splits the polygons once so that an order exists for each viewpoint. Fuchs, Abram and Grant gave faster ways to build and use the trees in 1983. Paterson and Yao proved bounds on the size of the tree in 1990. Gordon and Chen showed in 1991 how to draw the tree front to back, so that each pixel is written once. Front-to-back BSP rendering of static maps was common in 3D computer games in the 1990s.

## References
