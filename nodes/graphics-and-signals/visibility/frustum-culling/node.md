---
tag: F4J7C6
kind: algorithm
slug: frustum-culling
name: Frustum culling
aliases:
- view-frustum culling
- view-volume culling
area: graphics-and-signals/visibility
level: intro
summary: Skip each object whose bounding box is wholly outside one plane of the view frustum. A conservative test that never drops an object that meets the view.
solves: [visibility-culling]
model: real-ram
complexity:
  vars: {n: the number of objects}
  time: {worst: Θ(n), average: O(n), best: Θ(1)}
  space: {extra: O(log n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1976
  people: [James H. Clark]
  note: Clark proposed a hierarchy of bounding volumes so that a renderer can reject a whole subtree of the scene that is outside the view volume with one test.
prereqs: [axis-aligned-bounding-box, bounding-volume-hierarchy, dot-product]
see_also: [back-face-culling, occlusion-culling, portal-culling, separating-axis-theorem, bounding-volume, hidden-surface-removal, potentially-visible-set, bvh-traversal]
sources:
  - paper: doi:10.1145/360349.360354
    title: James H. Clark, Hierarchical geometric models for visible surface algorithms, Communications of the ACM 19(10), 1976, pages 547 to 554
    locator: the whole paper
  - paper: doi:10.1080/10867651.2000.10487517
    title: Ulf Assarsson and Tomas Möller, Optimized view frustum culling algorithms for bounding boxes, Journal of Graphics Tools 5(1), 2000, pages 9 to 22
    locator: the whole paper
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, 2005
    locator: Chapter 5, Section 5.2.3 (testing box against plane), pages 161 to 164, and Section 5.2.2 (sphere against plane), page 160
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, 2018
    locator: Chapter 19, Section 19.4 (View Frustum Culling), page 835
---

Frustum culling skips each object that is wholly outside the *view frustum*, the truncated pyramid of space that the camera can see. The test uses a [bounding volume](/bounding-volume/) of each object, here an [axis-aligned box](/axis-aligned-bounding-box/), and the six planes of the frustum. If the box is wholly on the outer side of one plane, the object cannot appear in the image. The test is *conservative*: it never drops an object that meets the frustum, but it can keep a box that is near a corner of the frustum and does not meet it. Over a [bounding volume hierarchy](/bounding-volume-hierarchy/), one test can drop a whole group of objects. It is a common case of [visibility culling](/visibility-culling/).

## In plain words

A camera sees only what is in front of it, inside a cone with four flat sides, cut off near the lens and far away. Things behind the camera or off to the side are not in the picture.

So before it draws an object, the renderer asks: is the object surely outside? It puts a box around the object and checks the box against each of the six walls of the view. If the whole box is on the outer side of one wall, the object is skipped.

The check is quick and never wrong in the bad direction: it never skips a thing that is in view. Sometimes it keeps a box that is just outside a corner, because no single wall shuts the box out. That costs a little time but gives no wrong pixels.

## The problem

The *frustum* $V$ is the intersection of six closed half-spaces $\{x : n_j \cdot x + d_j \ge 0\}$, $j = 1, \ldots, 6$, with each normal $n_j$ pointing into the frustum. For a camera at $E$ that looks down the $-z$ axis, with the window $[l, r] \times [b, t]$ at the distance $z_n$ and the far plane at the distance $z_f$, the planes are the left, right, bottom, top, near and far planes. An object is drawn only where it meets $V$, so an object that does not meet $V$ adds nothing to the image.

The input is $V$ and $n$ objects, each with a box $[lo, hi] = \prod_k [lo_k, hi_k]$ that contains it. The output is a set of objects that contains each object whose box meets $V$. A smaller output is better, but the requirement is only that no object that meets $V$ is missing. The coordinates are real numbers; the implementation uses integers or exact fractions.

## The algorithm

For a plane with normal $n$, the *p-vertex* of a box is its corner farthest in the direction $n$: $p_k = hi_k$ if $n_k \ge 0$, else $lo_k$. The *n-vertex* is the opposite corner. The box is wholly outside the plane if its p-vertex is outside, and wholly inside if its n-vertex is inside. The traversal keeps, for each node, the set of planes that the node box still straddles. A plane that wholly contains a node box contains each box below it, so it is not tested again in that subtree.

```pseudo id=main
FRUSTUM-CULL(hierarchy with root R, boxes of the objects, planes π[1 .. 6])
L1  kept ← an empty list
L2  stack ← [(R, {1, …, 6})]; while stack is not empty do
L3      pop (v, active) from stack; left ← an empty set
L4      for each j in active do
L5          if n_j · pvertex(box(v), n_j) + d_j < 0 then
L6              skip v and continue at L2                       ▷ wholly outside plane j
L7          if n_j · nvertex(box(v), n_j) + d_j < 0 then add j to left   ▷ straddles plane j
L8      if left is empty then add each object below v to kept; continue   ▷ wholly inside V
L9      if v is a leaf then
L10         for each object i of v do test box(i) on the planes of left as in L4 to L7, and add i to kept unless it is outside
L11     else for each child c of v do push (c, left)
L12 return kept
```

Lines L4 to L7 classify a box against the active planes with two corners per plane. Line L8 is the *plane masking* step: a node that is inside all active planes is inside $V$, and its whole subtree is accepted with no more tests. Line L10 tests the objects of a leaf one by one, so the output is the same as the flat test of each object box against all six planes. The stack is explicit; the implementation builds the hierarchy by a median split on the longest axis.

## Example

The camera is at the origin and looks down $-z$, with $l = b = -1$, $r = t = 1$, near distance 1 and far distance 10. The planes, in order, are left $x - z \ge 0$, right $-x - z \ge 0$, bottom $y - z \ge 0$, top $-y - z \ge 0$, near $-z - 1 \ge 0$ and far $z + 10 \ge 0$. Five boxes:

| box | $lo$ | $hi$ | result of L4 to L7 | meets $V$ |
|---|---|---|---|---|
| A | $(-1, -1, -6)$ | $(1, 1, -4)$ | inside all six planes | yes |
| B | $(5, -1, -4)$ | $(7, 1, -2)$ | outside the right plane | no |
| C | $(3, 3, -4)$ | $(5, 5, -3)$ | straddles right and top | yes |
| D | $(11, -1, -13)$ | $(12, 1, -9)$ | straddles right and far | no |
| E | $(-4, -1, -3)$ | $(-2, 1, -2)$ | straddles left | yes |

For B and the right plane, the p-vertex is $(5, \cdot, -4)$ and $-5 + 4 = -1 < 0$, so B is dropped. For C, the point $(3, 3, -4)$ is inside each plane, so C meets $V$. For D, the right plane gives $-11 + 13 = 2 \ge 0$ at its p-vertex $(11, \cdot, -13)$, and the far plane gives $-9 + 10 = 1 \ge 0$ at its p-vertex $(\cdot, \cdot, -9)$, so no plane drops it. But each point of $V$ has $z \ge -10$ and $x \le -z \le 10 < 11$, so D does not meet $V$. The output is A, C, D and E: one box too many, and none missing.

## Correctness

For a linear function $x \mapsto n \cdot x + d$ on a box, the largest value is at the p-vertex, because each coordinate can be chosen alone. So if the p-vertex is outside a plane, each point of the box is outside that plane and so outside $V$. A box below $v$ is inside the box of $v$, so a plane that holds all of $v$'s box holds it too; this justifies the masking of lines L7 and L8. Hence each object that the algorithm drops has a box with no point in $V$, and each object whose box meets $V$ is kept. The full proofs are below. The tests check this against an exact test of box against frustum, by a search for a vertex of the polyhedron $\text{box} \cap V$ with integer arithmetic.

## Complexity

One plane test costs two dot products, so a box test costs $O(1)$. The traversal visits only the nodes whose parents straddle $V$. In the worst case, for example when many small boxes lie along the boundary of $V$, it visits each of the $O(n)$ nodes, so the time is $\Theta(n)$. If the root box is outside a plane or inside $V$, the time is $O(1)$ plus the output. The stack holds $O(\text{depth})$ entries, which is $O(\log n)$ for the median split hierarchy. Building that hierarchy is a preprocessing step of $O(n \log^2 n)$ time with a sort at each level, or $O(n \log n)$ with a linear-time median.

## Properties

- **Conservative.** No object that meets $V$ is dropped. The proof uses only the p-vertex bound.
- **Not exact.** A box near an edge or a corner of $V$ can be outside $V$ but inside each of the six half-spaces, as box D shows. The random tests find such boxes.
- **Independent of occlusion.** An object inside $V$ but behind a wall is kept. [Occlusion culling](/occlusion-culling/) handles that case.
- **Hierarchical.** With a hierarchy and plane masking, a group of objects that is wholly outside or wholly inside costs one box test.
- **Exact arithmetic.** With integer or fraction input each sign is exact. With floating point, add a small tolerance on the side of keeping the box.

## Variants and improvements

- **Spheres.** For a bounding sphere with center $c$ and radius $\rho$ and a plane with unit normal, the sphere is outside when $n \cdot c + d < -\rho$. The test is cheaper but the volume is looser.
- **Oriented boxes.** For an oriented box with center $c$ and half axes $a_1, a_2, a_3$, the radius of the box in the direction $n$ is $\sum_k |n \cdot a_k|$, and the box is outside when $n \cdot c + d$ is less than minus this radius.
- **Exact test.** To remove the false positives such as D, use the [separating axis theorem](/separating-axis-theorem/): the box and $V$ are disjoint exactly when the projections are disjoint on a face normal of one of them or on a cross product of an edge direction of each. This costs more and is rarely worth it for culling.
- **Plane coherence.** Remember, for each node, the plane that dropped it in the last frame, and test that plane first in the next frame. Assarsson and Möller studied this and other optimizations.
- **Clip-space tests.** After the projection, $V$ becomes the cube $-w \le x, y, z \le w$ (or $0 \le z \le w$), and the plane tests become comparisons of coordinates.

## When to use it

Use frustum culling in each real-time renderer with more than a few objects, before the more costly steps. Put the objects in a [bounding volume hierarchy](/bounding-volume-hierarchy/), a grid or a scene tree, so that the test runs on groups. Combine it with [back-face culling](/back-face-culling/), which works on faces, and with [occlusion culling](/occlusion-culling/) or [portal culling](/portal-culling/), which remove objects hidden behind others.

## Pitfalls

- **Testing only the corners.** The test "drop the box if none of its corners is in $V$" is wrong. A large box around the whole frustum has all eight corners outside $V$ and still meets it. The tests check such a box. Test against one plane at a time.
- **Planes with outward normals.** If the normals point out of $V$, the test drops the visible objects and keeps the others. Check the sign convention of $n \cdot x + d \ge 0$ with a point that is surely inside.
- **Masking with a loose child.** The masking of line L8 needs each child box to be inside its parent box. In a hierarchy where child boxes are refit after a move but parent boxes are not, the masking can drop a visible object.
- **Strict and loose comparisons.** A box that touches $V$ at one point meets $V$. To be conservative, drop a box only when the p-vertex value is strictly negative.
- **Objects that move.** The box must contain the object at the time when it is drawn, including the animation and the deformation of that frame.

## Implementations

## History

Clark in 1976 proposed hierarchical geometric models for visible surface algorithms. A bounding volume around each subtree of the scene lets the renderer reject the whole subtree when the volume is outside the view volume. Real-time graphics systems made this test a standard step. The box against plane test with the corner farthest in the direction of the normal became the common form of the test. Assarsson and Möller in 2000 compared optimized tests for boxes against the frustum, including plane masking and plane coherence between frames.

## References
