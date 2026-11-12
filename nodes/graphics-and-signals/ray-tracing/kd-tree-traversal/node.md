---
tag: AK1SG3
kind: algorithm
slug: kd-tree-traversal
name: kd-tree ray traversal
aliases: [kd-tree ray tracing]
area: graphics-and-signals/ray-tracing
level: advanced
summary: Walk a spatial kd-tree along a ray from front to back, cutting the interval of the ray at each splitting plane, and stop at the first leaf with a hit that lies inside the cell of that leaf.
model: real-ram
complexity:
  vars: {n: the number of triangles, N: the number of nodes and leaf entries of the tree, h: the height of the tree}
  time: {best: O(1), worst: O(N)}
  space: {extra: O(h)}
properties: {deterministic: true, recursive: false}
history:
  year: 1992
  people: [Kelvin Sung, Peter Shirley, Vlastimil Havran]
  note: Space subdivision with axis-aligned planes was used for ray tracing from the middle of the 1980s; Sung and Shirley (1992) gave the recursive front-to-back walk with the split distance, and Havran (2000) made it the standard.
prereqs: [kd-tree, slab-method]
see_also: [bvh-traversal, bounding-interval-hierarchy, spatial-splits, surface-area-heuristic, amanatides-woo-traversal, bsp-tree, octree, ray-packet-tracing]
sources:
  - paper: doi:10.1111/j.1467-8659.2010.01844.x
    title: Michal Hapala and Vlastimil Havran, Review, Kd-tree traversal algorithms for ray tracing, Computer Graphics Forum 30(1), 2011, 199 to 213
    locator: the recursive front-to-back traversal with a stack, and the variants without a stack (kd-restart, short stack, ropes)
  - paper: doi:10.1109/RT.2006.280216
    title: Ingo Wald and Vlastimil Havran, On building fast kd-trees for ray tracing, and on doing that in O(N log N), IEEE Symposium on Interactive Ray Tracing 2006, 61 to 69
    locator: the SAH kd-tree for ray tracing, its build in O(N log N) by sorting the events once, and the clipping of triangles to the cells
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Chapter 4, Section 4.4 Kd-Tree Accelerator (the node layout, the SAH build, and the traversal with a stack of far children and the early stop)
---

**kd-tree ray traversal** finds the first object along a ray in a spatial kd-tree. This tree is not the [kd-tree](/kd-tree/) of points of Bentley: it cuts space, not a set of points. Each node has a box called its cell; an inner node cuts its cell with an axis-aligned plane into two closed cells, and each leaf holds every primitive that meets its cell, so a primitive that crosses a plane is in both children. The walk keeps the interval $[t_n, t_f]$ of the ray inside the current cell. At an inner node it computes where the ray meets the plane, $t_s$, and goes to the near child with $[t_n, t_s]$ and later to the far child with $[t_s, t_f]$, or to one of them only. So it visits the leaves in the order in which the ray passes through their cells, and it stops at the first leaf that has a hit with $t \le t_f$. The cells do not overlap, so such a hit is the closest one. Before BVHs took over around 2010, SAH kd-trees with this walk were the fastest structures for ray tracing static scenes.

## In plain words

Cut the scene in two with a wall, then each half with another wall, and so on, until each small room holds only a few objects. An object that crosses a wall is listed in the rooms on both sides.

To find what a ray hits first, follow the ray through the rooms in the order it enters them. At each wall, first go into the room the ray is in now, and remember the room on the other side for later. In each small room, test its objects. If an object is hit inside this room, stop: every room after this one is farther away. But an object listed in this room can be hit at a point in a later room; that hit does not count yet, because some other object in between may be hit first.

## The problem

The input is a spatial kd-tree over $n$ primitives, a ray $o + t d$ with $d \ne 0$, and a bound $t_{max}$. The [closest-hit query](/closest-hit-query/) asks for the least $t \in [0, t_{max}]$ at which the ray meets a primitive, and the primitive. The [any-hit query](/any-hit-query/) asks only whether such a $t$ exists. The tree is given: how to build it is a separate problem, solved well by the SAH build of Wald and Havran (2006).

## The algorithm

The walk uses a stack of far children with their intervals. Each inner node has an axis $a$, a plane position $p$, a left child with the cell $x_a \le p$ and a right child with the cell $x_a \ge p$.

```pseudo id=main
KD-CLOSEST(T, o, d, t_max)
L1  [t_n, t_f] ← the ray against the root cell on [0, t_max] by the slab method; if it is empty, return none
L2  stack ← [(root, t_n, t_f)]
L3  while the stack is not empty do pop (v, t_n, t_f)
L4      while v is an inner node with axis a and plane p do
L5          (near, far) ← (left, right) if o_a < p or (o_a = p and d_a ≤ 0), else (right, left)
L6          if d_a = 0 then v ← near; continue                        ▷ the ray is parallel to the plane
L7          t_s ← (p − o_a) / d_a
L8          if t_s > t_f or t_s ≤ 0 then v ← near                     ▷ the ray does not cross the plane in the cell
L9          else if t_s < t_n then v ← far                             ▷ it crossed the plane before the cell
L10         else push (far, t_s, t_f); v ← near; t_f ← t_s
L11     best ← the least hit with t ≤ t_max over the primitives of leaf v
L12     if best exists and t(best) ≤ t_f then return best
L13 return none
```

Line L5 picks as near the side that holds the ray just after $t = 0$; a ray that starts on the plane is on the side it moves into. Line L6 avoids a division by zero: a ray parallel to the plane stays in the near cell, and if it lies in the plane it is in both cells, so the near cell is enough. Line L8 covers the rays that cross the plane after leaving the cell, and the rays that move away from it. Line L10 is the case in which the ray crosses the plane inside the cell: the far child waits on the stack. Line L12 is the early stop. The any-hit query is the same walk, and it returns at the first hit with $t \le t_{max}$ in any leaf.

## Example

Two triangles: $P$ with the corners $(0, 0, 0)$, $(16, 2, 0)$, $(16, 0, 2)$ lies in the plane $x = 8(y + z)$ and its box spans $0 \le x \le 16$; $Q$ with the corners $(10, 0, 0)$, $(10, 2, 0)$, $(10, 0, 2)$ lies in the plane $x = 10$. The scene box is $[0, 16] \times [0, 2] \times [0, 2]$. The root splits $x$ at $p = 8$. The left leaf holds $P$, and the right leaf holds $P$ and $Q$, since $P$ crosses the plane. Two rays along the $x$ axis at $y = z = 7/8$ meet $P$ at $x = 14$ and $Q$ at $x = 10$.

| ray | root interval | $t_s$ | case | first leaf | hits there | result |
|---|---|---|---|---|---|---|
| $o = (-1, 7/8, 7/8)$, $d = (1, 0, 0)$ | $[1, 17]$ | 9 | L10: push right with $[9, 17]$, go left with $[1, 9]$ | left, $[1, 9]$ | $P$ at $t = 15 > 9$: no stop | right leaf, $[9, 17]$: $Q$ at 11 and $P$ at 15; return $Q$ at $t = 11$ |
| $o = (20, 7/8, 7/8)$, $d = (-1, 0, 0)$ | $[4, 20]$ | 12 | L10: push left with $[12, 20]$, go right with $[4, 12]$ | right, $[4, 12]$ | $P$ at $t = 6$ and $Q$ at $t = 10$ | return $P$ at $t = 6 \le 12$; the left leaf is never visited |

The first ray shows why line L12 tests $t \le t_f$: the near leaf holds $P$, and the ray hits $P$, but at $x = 14$, in the far cell. Returning it would miss $Q$ at $t = 11$. The tests check both rays, and that the walk without the test of line L12 gives a wrong answer on some random scenes.

## Correctness

Claim: KD-CLOSEST returns the least hit in $[0, t_{max}]$, or none if there is none.

Each leaf holds every primitive that meets its cell, since the build puts a primitive into each child that its box meets. By a case analysis of lines L5 to L10, each step passes on an interval in which the ray lies in the cell of the child, and splits it at $t_s$ into a near part and a far part that follow each other. The stack is last in, first out, so the whole near subtree is walked before the far child. So the leaves are visited in the order of their intervals along the ray, and these intervals cover the part of the ray in the scene box. Let $t^*$ be the closest hit, on a primitive $q$. The point at $t^*$ lies in the cell of some leaf, and $q$ is in that leaf, so that leaf, or an earlier one, returns. An earlier leaf returns a hit $t_b \le t_f$, and its $t_f$ is at most $t^*$, so $t_b = t^*$. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

The model is the [real RAM](/real-ram/). Let $N$ be the size of the tree, its nodes plus its leaf entries; with duplicated primitives, $N$ can be much larger than $n$. Each node is reached at most once and each leaf entry is tested at most once, so the walk costs $O(N)$ per ray in the worst case, and a ray that grazes many cells can come close to it. The extra space is the stack, at most one entry per level, so $O(h)$. A ray that misses the scene box costs $O(1)$.

The time of about $\log N$ steps per ray that SAH kd-trees show on real scenes is an observation, not a bound.

## Properties

- **Front to back.** The leaves are visited in the order of $t$, which allows the early stop. A BVH walk has no such order, since the boxes of the children can overlap.
- **Exact cover.** The cells of the leaves partition the scene box, apart from their shared faces.
- **Duplicates.** A primitive can be tested in many leaves. Mailboxing, a record of the last ray tested against each primitive, avoids testing it twice.
- **Cheap nodes.** An inner node is an axis, a plane and a child index; 8 bytes in PBRT.
- **Iterative.** The walk uses an explicit stack of far children, with no recursion.

## Variants and improvements

- **Recursive form.** The same walk as a recursive function: visit near on $[t_n, \min(t_f, t_s)]$, then far on $[\max(t_n, t_s), t_f]$ if the first call found nothing. Sung and Shirley (1992) and Havran (2000) gave the forms used in most renderers.
- **Without a stack.** On GPUs, kd-restart starts again from the root with $t_n \leftarrow t_f$ after each leaf, and the short stack keeps only the last few far children. Ropes link each face of a leaf cell to the neighbor cells, so the walk goes from leaf to leaf without going up the tree.
- **Packets.** A group of coherent rays walks the tree together; the node is visited when any ray of the [packet](/ray-packet-tracing/) needs it. See also [ray coherence](/ray-coherence/).
- **SAH kd-trees.** The planes are chosen by the [surface area heuristic](/surface-area-heuristic/), with empty space cut off early. Wald and Havran (2006) build such a tree in $O(n \log n)$ by sorting the plane events once, and they clip each triangle to the cells to get tight boxes, the same clipping as in [spatial splits](/spatial-splits/).
- **Uniform grids.** The [Amanatides-Woo traversal](/amanatides-woo-traversal/) walks a [uniform grid](/uniform-grid/) cell by cell in the same front-to-back order; an [octree](/octree/) is walked in the same way with eight children per node.
- **Two planes per node.** The [bounding interval hierarchy](/bounding-interval-hierarchy/) stores each object once and cuts with two planes per node, which costs it the early stop.

## When to use it

Use a kd-tree when the scene is static and is traced with many rays, so that a slow SAH build pays off, and when memory for duplicated references is available. For scenes that change, a [BVH](/bvh-traversal/) is easier to update by [refitting](/bvh-refitting/) and is faster to build. Most production renderers now use BVHs, since their size is bounded by $2n - 1$ nodes and their build is simpler; a kd-tree is still a good choice for a static scene and for a [BSP-tree](/bsp-tree/) style of spatial query.

## Pitfalls

- **No cell test in line L12.** A primitive in a leaf can be hit outside the cell of that leaf, as $P$ in the example. Returning such a hit misses a nearer hit in a later cell.
- **The tie in line L5.** When $o_a = p$, near must be the side the ray moves into. Taking the left side for every $o_a = p$ makes a ray with $d_a > 0$ go into the left cell with an interval of the right cell, and its hits are tested in the wrong leaf.
- **A division in line L6.** With $d_a = 0$, $(p - o_a)/d_a$ is $\pm \infty$ in [IEEE 754](/ieee-754/), or NaN when $o_a = p$, and a NaN fails every comparison of lines L8 and L9, so the walk takes the far child in line L10 with a NaN interval. Test $d_a = 0$ first, as line L6 does.
- **$t_s < 0$ in place of $t_s \le 0$ in line L8.** A ray that starts on the plane has $t_s = 0$, and line L10 then visits near with $[0, 0]$ and far with $[0, t_f]$. But for $t > 0$ the ray is in near and not in far, so line L12 can accept a hit in far that lies beyond a nearer hit in near.
- **A missing update in line L10.** After the push, the near child must get $t_f \leftarrow t_s$. With the old $t_f$, line L12 accepts hits in the far cell, the same error as no cell test.
- **Rounding at the plane.** In floating point, a hit exactly on the plane can get $t$ slightly above the $t_f = t_s$ of the near leaf, and be found again in the far leaf. If a leaf also rejects hits with $t < t_n$, the hit is lost in both. Do not test $t \ge t_n$, or widen the interval of the leaf by a few [ulps](/ulp/).

## Implementations

## History

Kaplan (1985) and Fussell and Subramanian (1988) used binary space partitions with axis-aligned planes to speed up ray tracing, after Glassner (1984) did it with octrees. Sung and Shirley (1992) gave the recursive walk with the split distance $t_s$ and the near and far children, and Havran (2000), in his thesis, compared the many forms of it and made the recursive form with a stack the standard. Wald and Havran (2006) showed how to build an SAH kd-tree in $O(n \log n)$, and for some years SAH kd-trees were the fastest acceleration structures for static scenes. GPU variants without a full stack followed (Foley and Sugerman 2005, Horn et al. 2007, Popov et al. 2007). From about 2010, BVHs with the SAH and spatial splits replaced kd-trees in most renderers.

## References
