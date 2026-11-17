---
tag: 46M4XT
kind: algorithm
slug: sweep-and-prune
name: Sweep and prune
aliases:
- sort and sweep
area: graphics-and-signals/rigid-body-simulation
level: core
summary: Find overlapping bounding boxes by keeping their interval endpoints sorted per axis and updating the sort incrementally between time steps.
solves: [collision-detection]
model: real-ram
complexity:
  vars: {n: the number of boxes, r: the number of endpoint swaps in one update, q: the number of pairs whose intervals overlap on the sweep axis, m: the number of pairs that overlap on at least one axis}
  time: {update: O(n + r), sort_and_sweep: O(n log n + q), worst_update: O(n^2)}
  space: {total: O(n + m)}
properties: {deterministic: true, online: true, recursive: false, in_place: true}
history:
  year: 1992
  people: [David Baraff, Jonathan D. Cohen, Ming C. Lin, Dinesh Manocha, Madhav K. Ponamgi]
  note: Baraff used sorted interval lists and coherence between steps in his 1992 thesis. The I-COLLIDE system of Cohen, Lin, Manocha and Ponamgi (1995) made the incremental sort of box endpoints the standard broad phase.
prereqs: [axis-aligned-bounding-box, insertion-sort]
see_also: [collision-detection, bounding-volume-hierarchy, spatial-hashing, uniform-grid, rectangle-intersection-reporting, interval-tree, lin-canny-closest-features, radix-sort]
sources:
  - paper: doi:10.1145/199404.199437
    title: Jonathan D. Cohen, Ming C. Lin, Dinesh Manocha and Madhav K. Ponamgi, I-COLLIDE, an interactive and exact collision detection system for large-scale environments, Proceedings of the 1995 Symposium on Interactive 3D Graphics, 189 to 196
    locator: the sweep and prune of bounding boxes with sorted endpoint lists, insertion sort between frames, and the use of coherence
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 7, Spatial Partitioning (the sort and sweep methods)
---

Sweep and prune is a broad phase for collision detection. It finds all pairs of overlapping [axis-aligned bounding boxes](/axis-aligned-bounding-box/) among $n$ boxes. For each axis it keeps a list of the $2n$ interval endpoints in sorted order, and for each pair of boxes it keeps the number of axes on which their intervals overlap. Between time steps the boxes move only a little, so [insertion sort](/insertion-sort/) repairs each list with few swaps, and each swap changes one counter. The pairs with a full count go to the narrow phase.

## In plain words

Think of a set of boxes on a table. Look at them from the front, so that each box is a line segment on the floor line. Two boxes can touch only if their segments overlap. Do the same from the side. Two boxes overlap only if their segments overlap in both views.

To find overlapping segments fast, write all the segment ends in order along the line. When you pass the start of a segment, it is open, and it overlaps every segment that is open at that moment.

The boxes move only a little from one frame to the next. So the list of ends is almost in order already. Fix it with a few neighbor swaps. Each time the start of one segment passes the end of another, the two segments start or stop overlapping, and you update one count.

## The problem

The input is $n$ closed boxes $B_i = [x^{lo}_i, x^{hi}_i] \times [y^{lo}_i, y^{hi}_i]$ in the plane, given again at each time step with new values. The output at each step is the set of pairs $\{i, j\}$ with $B_i \cap B_j \ne \emptyset$. Two closed boxes intersect exactly when their intervals intersect on each axis, so the problem splits into one interval problem per axis. This page uses 2D boxes. In 3D the method is the same with three lists.

This is the broad phase of [collision detection](/collision-detection/). The boxes bound the objects, so a pair that is not reported cannot collide, and each reported pair goes to an exact test, for example [GJK](/gjk-algorithm/) for convex shapes.

## The algorithm

Each endpoint is a triple (value, kind, box), with kind 0 for a lower endpoint and 1 for an upper endpoint. Triples compare in lexicographic order. So at equal values a lower endpoint comes first, and boxes that only touch count as overlapping. The state is the sorted list $E[a]$ for each axis $a$, a counter $c[i, j]$ for each pair that overlaps on at least one axis, and the set $P$ of pairs with $c = 2$.

```pseudo id=main
UPDATE(E, c, P, box)                     ▷ box: the new boxes, same indices
L1  r ← 0
L2  for each axis a do
L3      set the value of each endpoint in E[a] from box
L4      for i ← 1 to |E[a]| - 1 do
L5          j ← i
L6          while j > 0 and E[a][j - 1] > E[a][j] do
L7              x ← E[a][j]; y ← E[a][j - 1]; p ← the pair of the boxes of x and y
L8              if x is lower and y is upper then c[p] ← c[p] + 1; if c[p] = 2 then add p to P
L9              if x is upper and y is lower then if c[p] = 2 then remove p from P; c[p] ← c[p] - 1
L10             swap E[a][j - 1] and E[a][j]; j ← j - 1; r ← r + 1
L11 return P, r
```

Lines L4 to L10 are insertion sort. Line L8 is the case where the lower endpoint of one box passes to the left of the upper endpoint of another box: their intervals start to overlap on this axis. Line L9 is the opposite case: they stop overlapping. A swap of two lower endpoints or of two upper endpoints changes nothing.

The first frame has no sorted lists to repair. Sort each list once and set the counters with one sweep per axis: at each lower endpoint, add 1 to the counter of the new box and each box that is open. The same sweep on one axis, with a test of the other axis for each open box, is the one-shot method that is also called sort and sweep.

```pseudo id=sweep
SORT-AND-SWEEP(box, a)                   ▷ a: the sweep axis
L12 sort the boxes by their lower value on axis a; active ← empty; out ← empty
L13 for each box i in this order do
L14     remove from active each j with hi_a(j) < lo_a(i)
L15     for each j in active do if B_i and B_j overlap on the other axis then add {i, j} to out
L16     add i to active
L17 return out
```

## Example

Take four boxes: $B_0 = [0, 4] \times [0, 2]$, $B_1 = [3, 6] \times [1, 5]$, $B_2 = [5, 8] \times [4, 6]$ and $B_3 = [9, 10] \times [0, 3]$. Write $\ell_i$ and $h_i$ for the lower and upper endpoints of box $i$. After the first sort and sweep:

| axis | sorted list | overlaps on this axis |
|---|---|---|
| x | $\ell_0{:}0,\ \ell_1{:}3,\ h_0{:}4,\ \ell_2{:}5,\ h_1{:}6,\ h_2{:}8,\ \ell_3{:}9,\ h_3{:}10$ | {0, 1}, {1, 2} |
| y | $\ell_0{:}0,\ \ell_3{:}0,\ \ell_1{:}1,\ h_0{:}2,\ h_3{:}3,\ \ell_2{:}4,\ h_1{:}5,\ h_2{:}6$ | {0, 1}, {0, 3}, {1, 3}, {1, 2} |

So $c[0, 1] = c[1, 2] = 2$, $c[0, 3] = c[1, 3] = 1$, and $P = \{\{0, 1\}, \{1, 2\}\}$.

Now box 3 moves 4 units to the left and 2 units up, to $[5, 6] \times [2, 5]$. Line L3 writes the new values into the old lists, and insertion sort makes these swaps:

| axis | swap at line L10 | rule | counter | P |
|---|---|---|---|---|
| x | $\ell_3{:}5$ passes $h_2{:}8$ | L8 | $c[2, 3] = 1$ | no change |
| x | $\ell_3{:}5$ passes $h_1{:}6$ | L8 | $c[1, 3] = 2$ | add {1, 3} |
| x | $h_3{:}6$ passes $h_2{:}8$ | none | | |
| y | $\ell_1{:}1$ passes $\ell_3{:}2$ | none | | |
| y | $\ell_2{:}4$ passes $h_3{:}5$ | L8 | $c[2, 3] = 2$ | add {2, 3} |
| y | $h_1{:}5$ passes $h_3{:}5$ | none | | |

The update makes $r = 6$ swaps and returns $P = \{\{0, 1\}, \{1, 2\}, \{1, 3\}, \{2, 3\}\}$, which is the brute force answer. The pair {0, 3} keeps $c = 1$: the boxes touch on y at the value 2, but on x the interval [5, 6] does not meet [0, 4]. In the last swap the two upper endpoints have the same value 5, and the box index breaks the tie, which changes no counter.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The main fact is that the relation "the lower endpoint of $i$ is before the upper endpoint of $j$, and the lower endpoint of $j$ is before the upper endpoint of $i$" is the overlap of the two closed intervals when the list is sorted. A swap of two neighbors changes this relation for the pair of their owners only, and only when one is a lower endpoint and the other an upper endpoint. Lines L8 and L9 follow these changes exactly, so after the sort each counter is the number of axes on which the pair overlaps. The two endpoints of one box are never swapped, because the lower endpoint is never larger than the upper one.

## Complexity

The update does $O(n)$ work per axis outside the swaps, and $O(1)$ work per swap with a hash table for the counters. So it costs $O(n + r)$ in the real RAM with hashing, where $r$ is the number of inversions that the motion makes in the lists. This bound is exact in terms of $r$, but $r$ itself has no useful worst case bound: one step can reverse a list, and then $r = \Theta(n^2)$. That $r$ is close to $O(n)$ in a simulation is an observation about coherent motion, not a theorem.

The one-shot sort and sweep costs $O(n \log n + q)$, where $q$ is the number of pairs whose intervals overlap on the sweep axis. The output size $k$ can be much smaller than $q$. If all boxes are in a thin column along the sweep axis, every pair overlaps on that axis, so $q = \Theta(n^2)$ even when $k = 0$. Choosing the sweep axis with the largest spread of box centers helps, but it does not remove this case.

The space is $O(n + m)$ for the lists and the counters of the $m$ pairs that overlap on at least one axis. Like $q$, $m$ can be $\Theta(n^2)$ for clustered scenes.

## Properties

- The output is exact for the boxes: no pair is lost and no pair is reported twice.
- The method is deterministic and in place on the lists.
- It is output sensitive only through $r$ and $q$, not through the output size $k$.
- It handles boxes that change size, not only boxes that move.

## Variants and improvements

- **Sort and sweep from scratch.** Sort once per frame, for example with [radix sort](/radix-sort/) on the float keys, and sweep one axis. It does not keep counters between frames, so it has no cost for teleports and no memory for pairs.
- **Three axes or one axis.** I-COLLIDE keeps sorted lists on all three axes of 3D. Many engines keep one sorted axis and test the other axes directly for the open boxes, which uses less memory.
- **Insertions and deletions.** A new box can be put at the end of each list with the value $+\infty$ and then moved into place with the update. A deleted box is moved to the end in the same way, and its counters are dropped.
- **Several sweep and prune regions.** A large world is cut into regions with one structure each, so that a cluster in one place does not make all lists long.
- **Other broad phases.** A [uniform grid](/uniform-grid/) or [spatial hashing](/spatial-hashing/) is better when objects are of similar size and spread in all directions. A dynamic [bounding volume hierarchy](/bounding-volume-hierarchy/) is better for many static objects and for ray queries. The offline problem of reporting all intersecting rectangles has an $O(n \log n + k)$ solution with an [interval tree](/interval-tree/); see [rectangle intersection reporting](/rectangle-intersection-reporting/).

## When to use it

Use sweep and prune as the broad phase of a simulation with many moving objects and small motion per step, which is the usual case in games and physics engines. Use sort and sweep from scratch when objects jump, appear and disappear often. Do not use it when many objects line up along an axis (a stack of boxes, a long road of cars), unless you choose the axis with care; a grid or a BVH is not sensitive to this.

## Pitfalls

- **Ties.** Line L6 must use the same total order as the first sort. With lower endpoints before upper endpoints at equal values, touching boxes overlap. With the other order they do not. A mix of the two orders makes the counters wrong.
- **Updating counters without the swap rules.** Do not recompute a pair from its boxes at a swap and then add or subtract 1. A swap of two lower endpoints, or of two upper endpoints, must change nothing, and two equal values must not toggle anything.
- **A counter of 0.** Remove a pair from the table when its counter drops to 0, or the table grows with every pair that ever overlapped on one axis.
- **Teleports.** A box that jumps across the scene makes up to $2n$ swaps on each axis. If this happens often, rebuild with a full sort.
- **Clustering.** A scene that is spread along one axis only, for example objects in a line on a floor, gives many overlaps on the other axis and makes $m$ and $q$ large.
- **Float noise.** Boxes that are computed from rotating objects change size every frame, so their endpoints swap back and forth around equal values. Grow the boxes by a small margin and update them only when an object leaves its grown box.

## Implementations

## History

Baraff (1992) used sorted lists of interval endpoints and the coherence between time steps for the box tests in his thesis on rigid body simulation. Cohen, Lin, Manocha and Ponamgi (1995) described sweep and prune in the I-COLLIDE system: they kept the endpoints of the boxes on each axis sorted, repaired the lists by insertion sort, and passed the pairs that overlap on all axes to the [Lin-Canny](/lin-canny-closest-features/) closest feature test. Since then it is the broad phase of many physics engines, often with one sorted axis and a full sort per frame.

## References
