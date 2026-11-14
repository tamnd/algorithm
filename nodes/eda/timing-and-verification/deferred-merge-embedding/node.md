---
tag: RDEGA7
kind: algorithm
slug: deferred-merge-embedding
name: Deferred-merge embedding
aliases:
- DME
- deferred merge embedding
area: eda/timing-and-verification
level: core
summary: Builds a zero-skew tree of least wire length for a given topology by computing merging segments bottom up, then embedding the tapping points top down.
solves: [clock-tree-synthesis]
model: real-ram
complexity:
  vars: {n: the number of clock sinks}
  time: {given_topology: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true, exact: true}
history:
  year: 1992
  people: [Ting-Hai Chao, Yu-Chin Hsu, Jan-Ming Ho, Kenneth D. Boese, Andrew B. Kahng]
  note: Chao, Hsu, Ho, Boese and Kahng gave the method in 1992, and Boese and Kahng presented it at the ASIC Conference the same year.
prereqs: [binary-tree, tsay-zero-skew]
see_also: [clock-tree-synthesis, tsay-zero-skew, method-of-means-and-medians, h-tree-clock, rectilinear-steiner-arborescence, elmore-delay, tree-dynamic-programming, clock-skew-scheduling]
sources:
  - paper: "Ting-Hai Chao, Yu-Chin Hsu, Jan-Ming Ho, Kenneth D. Boese and Andrew B. Kahng, Zero skew clock routing with minimum wirelength, IEEE Transactions on Circuits and Systems II 39(11), 799 to 814, 1992"
    locator: the merging segments as Manhattan arcs, the bottom-up and top-down phases, and the proof of least wire length for a fixed topology under linear delay
  - paper: "Kenneth D. Boese and Andrew B. Kahng, Zero-skew clock routing trees with minimum wirelength, Proceedings of the IEEE International ASIC Conference 1992"
    locator: the conference presentation of the method
  - book: isbn:9789048195909
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, Springer, 2011
    locator: Chapter 7, Specialized Routing, Section 7.5.1, Constructing Trees with Zero Global Skew (deferred-merge embedding)
  - paper: doi:10.1145/157485.165066
    title: Masato Edahiro, A clustering-based optimization algorithm in zero-skew routings, Proceedings of the 30th Design Automation Conference, 612 to 616, 1993
    locator: the greedy clustering that builds the topology on which the merging segments are computed
---

Deferred-merge embedding (DME) is a clock routing algorithm: for a given binary topology over the clock sinks, it builds a wire tree in which every source-to-sink path has the same delay and the total wire length is the least possible. It does not fix the root of a subtree when the subtree is built. It keeps the whole set of points where the root could go, a segment called the *merging segment*, and picks a point from it only in a second, top-down pass. Under linear delay the result is proved optimal for the topology; under the [Elmore delay](/elmore-delay/) it keeps zero skew but is a heuristic for wire length.

## In plain words

Tsay's method joins two subtrees at one point on the wire between their roots. But a subtree often has many good roots, all with the same delay to its sinks, and the choice matters later.

DME first goes up the tree and only records where each root may go. For a single sink, that is the sink itself. For two joined subtrees, it is the set of points at the right distances from the two child sets, and on a Manhattan grid this set is always a straight piece of a diagonal line, or one point.

Then DME goes down. It puts the root anywhere on its segment, and puts each child at the point of its own segment nearest to its parent. Each wire is then as short as it can be, and all paths keep the same length.

## The problem

The input is a set of $n$ sinks with points $p_s$ in the plane and a full binary tree (the *topology*) whose leaves are the sinks. Wires run horizontally and vertically, so distances are L1 distances $d$. Under *linear delay* the delay of a path is its wire length. The output is a point $p_v$ for each internal node and a wire length $e_c \ge d(p_c, p_{\text{parent}(c)})$ for each non-root node $c$ (a longer wire is a detour), such that all root-to-sink paths have the same length and the total $\sum_c e_c$ is least. This is the zero-skew case of [clock tree synthesis](/clock-tree-synthesis/) with the topology fixed.

The algorithm works in the rotated coordinates $u = x + y$, $v = x - y$, where the L1 distance becomes $\max(|\Delta u|, |\Delta v|)$. A segment of slope $\pm 1$ in the plane is an axis-parallel segment in $(u, v)$. The *tilted rectangular region* $\mathrm{TRR}(S, e)$, the set of points within distance $e$ of a region $S$, is $S$ widened by $e$ on all four sides.

## The algorithm

```pseudo id=main
DME(topology T, sinks, source q₀)
    // bottom-up phase: BUILD(v) sets ms(v), t(v) and the edge lengths below v
    BUILD(v)
L1      if v is a sink s then
L2          ms(v) ← {p_s};  t(v) ← 0;  return
L3      BUILD(a);  BUILD(b)                  // a, b are the children of v
L4      D ← d(ms(a), ms(b))
L5      if |t(a) − t(b)| ≤ D then e_a ← (D + t(b) − t(a)) / 2;  e_b ← D − e_a
L6      else the slower child gets length 0 and the other gets |t(a) − t(b)|
L7      ms(v) ← TRR(ms(a), e_a) ∩ TRR(ms(b), e_b)
L8      t(v) ← t(a) + e_a
    // top-down phase: EMBED(v, q) places v at the point of ms(v) nearest q
L9  BUILD(root of T);  EMBED(root of T, q₀)
    EMBED(v, q)
L10     p_v ← the point of ms(v) nearest to q
L11     for each child c of v do EMBED(c, p_v)
```

In line L6 the delays differ by more than the distance, so the faster child gets a detour wire, and $\mathrm{ms}(v)$ is part of the slower child's segment. In line L10 the nearest point is found by clamping each rotated coordinate of $q$ into the interval of $\mathrm{ms}(v)$; for the root, $q_0$ is the clock source, or any point if the source is free. Since the wire from the source to the root is not part of the tree, the choice of the root point does not change the total length.

## Example

Take four sinks $s_1 = (1, 3)$, $s_2 = (0, 1)$, $s_3 = (2, 0)$ and $s_4 = (3, 2)$ and the topology $((s_1, s_2), (s_3, s_4))$.

| node | children | $D$ | $e_a$, $e_b$ | merging segment | $t$ |
| --- | --- | --- | --- | --- | --- |
| $a$ | $s_1$, $s_2$ | 3 | $3/2$, $3/2$ | from $(0, 5/2)$ to $(1, 3/2)$ | $3/2$ |
| $b$ | $s_3$, $s_4$ | 3 | $3/2$, $3/2$ | from $(2, 3/2)$ to $(3, 1/2)$ | $3/2$ |
| root | $a$, $b$ | 1 | $1/2$, $1/2$ | the point $(3/2, 3/2)$ | 2 |

Every point of the segment of $a$ is at distance $3/2$ from both $s_1$ and $s_2$; for example $(0, 5/2)$ is $1 + 1/2$ from $s_1$ and $0 + 3/2$ from $s_2$. The two segments come closest at $(1, 3/2)$ and $(2, 3/2)$, at distance 1, so the root segment is the single point between them. Top down, the root is at $(3/2, 3/2)$, $a$ goes to $(1, 3/2)$ and $b$ to $(2, 3/2)$. The wire lengths are $1/2 + 1/2$ at the root and $3/2$ to each sink, a total of 7, and every sink is at path length 2 from the root.

A merge that fixes each subtree root when it is built does worse here. With the taps at the ends $(0, 5/2)$ and $(3, 1/2)$ of the two segments, which also give delay $3/2$, the top merge must span distance 5, and the total is $3 + 3 + 5 = 11$. DME saves 4 units of wire by waiting.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows three facts. First, each merging segment is nonempty and is a segment of slope $\pm 1$ or a point, because in each rotated coordinate the two widened intervals meet, and they touch at a single value in a coordinate where the gap equals $D$. Second, the top-down pass is valid: a point of $\mathrm{ms}(v)$ lies within $e_c$ of $\mathrm{ms}(c)$, so the nearest point of $\mathrm{ms}(c)$ can be joined with a wire of length $e_c$, and by induction all paths below $v$ have length $t(v)$. Third, by induction on the height, every zero-skew tree on the same topology with root point $p$ and delay $\tau$ has $\tau \ge t(v) + d(p, \mathrm{ms}(v))$ and a cost minus delay of at least the value of DME. At the root these give a cost of at least the DME cost, so the DME tree has the least wire length for the topology.

## Complexity

With the topology given, each of the $n - 1$ internal nodes needs one distance between two rectangles, two widenings and one intersection bottom up, and one clamp top down, each with $O(1)$ arithmetic operations. The time is $\Theta(n)$ and the extra space is $\Theta(n)$ for the segments. Building the topology is a separate step; the greedy and partitioning methods used in practice take $O(n \log n)$ time or more.

## Properties

- Exact zero skew under linear delay, for every topology.
- Least total wire length among all zero-skew trees on the topology under linear delay (proved). It is not the least over all topologies; the topology is an input.
- Each merging segment is a Manhattan arc, so it is stored as four numbers.
- When the source is not fixed, every point of the root segment gives the same total wire length; the root segment is the set of best root points.
- Under the Elmore delay the same two passes work with the balance formula of [Tsay's method](/tsay-zero-skew/) in place of line L5, and the segments are still Manhattan arcs. The tree has exact zero Elmore skew, but the wire length is not proved least, because the split of each wire then depends on its length.

## Variants and improvements

- **Elmore delay.** Chao et al. gave the version for the Elmore delay of the RC interconnect tree, which is the one used in practice. It keeps zero skew and in their measurements uses less wire than Tsay's merge on the same topology.
- **Topology generation.** DME needs a topology. A top-down split of the sinks, as in the [method of means and medians](/method-of-means-and-medians/), or a bottom-up greedy matching of the nearest merging segments both work. Edahiro's clustering method builds the topology and the segments together.
- **Bounded skew.** If a skew bound $B > 0$ is allowed, the merging regions become polygons rather than segments, and the extra freedom saves wire. Cong, Kahng, Koh and Tsao gave this bounded-skew form.
- **Fixed source.** When the source position is given, line L9 starts the top-down pass from it, and the root goes to the point of its segment nearest to the source.

## When to use it

Use it to route a zero-skew clock tree on a placement when the topology is known or built by a separate heuristic, and wire length matters. It replaces Tsay's merge with the same skew and less wire. For a regular array of sinks an [H-tree](/h-tree-clock/) needs no computation. For the plain least-wire tree with no skew constraint, use a [rectilinear Steiner tree](/rectilinear-steiner-tree-problem/) method instead.

## Pitfalls

- The topology decides most of the wire length. DME is optimal for the topology it is given, not over all topologies, and a poor topology forces long wires or detours.
- In line L6 the detour wire has length $|t(a) - t(b)|$, which is longer than the distance. The embedding must route it as a real detour; a straight wire of length $D$ leaves a skew.
- The rotation halves coordinates when it is undone, so integer sinks give half-integer points. Use exact arithmetic or keep the rotated coordinates.
- A choice of the tap that is only nearest in the plane, and not in the merging segment, breaks the bound $d(p_c, p_v) \le e_c$. Clamp in the rotated coordinates.
- Zero skew under linear delay is not zero skew under the Elmore delay, since loads differ between branches. Use the Elmore form for real wires.

## Implementations

## History

Before 1992, clock routers such as the [method of means and medians](/method-of-means-and-medians/) of Jackson, Srinivasan and Kuh (1990) balanced path lengths only roughly, and Tsay's exact zero-skew method (1991) fixed each tapping point as soon as it joined two subtrees. In 1992 Chao, Hsu, Ho, Boese and Kahng showed that the choice can be deferred to a top-down pass, proved that this gives the least wire length for the topology under linear delay, and gave the Elmore form. Masato Edahiro described the same idea independently, and his 1993 paper uses it inside a greedy clustering that also builds the topology.

## References
