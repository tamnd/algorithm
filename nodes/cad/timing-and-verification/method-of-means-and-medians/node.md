---
tag: JBVF6M
kind: algorithm
slug: method-of-means-and-medians
name: Method of means and medians
aliases:
- MMM clock routing
- MMM
area: cad/timing-and-verification
level: core
summary: Jackson, Srinivasan and Kuh's clock router that splits the sinks at the median again and again and connects the centre of mass of each half to that of the whole.
solves: [clock-tree-synthesis]
model: real-ram
complexity:
  vars: {n: the number of clock sinks}
  time: {worst: O(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true, exact: false}
history:
  year: 1990
  people: [Mike A. B. Jackson, Arvind Srinivasan, Ernest S. Kuh]
  note: Jackson, Srinivasan and Kuh gave the method at the 1990 Design Automation Conference as a clock router for sinks that are not on a regular grid.
prereqs: [median, binary-tree]
see_also: [clock-tree-synthesis, h-tree-clock, tsay-zero-skew, deferred-merge-embedding, geometric-median, weighted-median, rectilinear-steiner-tree-problem, elmore-delay]
sources:
  - paper: doi:10.1145/123186.123406
    title: Mike A. B. Jackson, Arvind Srinivasan and Ernest S. Kuh, Clock routing for high-performance ICs, Proceedings of the 27th Design Automation Conference, 573 to 579, 1990
    locator: the method of means and medians, the recursive median split in alternating directions and the connection of the centres of mass
  - book: isbn:9789048195909
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, Springer, 2011
    locator: Chapter 7, Specialized Routing, Section 7.5.1, Constructing Trees with Zero Global Skew (method of means and medians)
---

The method of means and medians (MMM) is a clock routing algorithm: it builds a wire tree from the clock source to a set of sinks by splitting the sinks at the median into two halves, alternately by $x$ and by $y$, and joining the centre of mass (the mean) of each set to the centres of mass of its two halves. It generalizes the [H-tree](/h-tree-clock/) to sinks at arbitrary places, and on a full square grid it gives exactly the H-tree. The paths have roughly balanced lengths, but the skew is not zero in general. Jackson, Srinivasan and Kuh published it in 1990.

## In plain words

The registers that need the clock are scattered over the chip. Draw a vertical line that puts half of them on each side. Join the middle of all the registers, their average position, to the average position of each side.

Now do the same inside each side, but with a horizontal line. Then use a vertical line again, and so on, until each group holds one register.

Because each cut halves the group, the tree has few levels, and each wire points from a group to the middle of its own half, so no branch goes far out of its way. On a perfect grid of registers every path has the same length. On an uneven placement the paths are only roughly equal, and some registers can get the clock later than others.

## The problem

The input is a set of $n$ sinks with points $p_s$ in the plane. The output is a rooted tree whose leaves are the sinks, with a point for each internal node and rectilinear wires along the edges, such that the root-to-sink path lengths are close to each other. MMM does not solve a stated optimization problem: it is a construction for the topology and the embedding of [clock tree synthesis](/clock-tree-synthesis/) with no guarantee on skew or wire length, except on a full grid. Its delay model is the path length; the [Elmore delay](/elmore-delay/) of the result is not balanced either.

## The algorithm

```pseudo id=main
MMM(S, axis)
L1  c ← the centre of mass of the points of S
L2  if |S| = 1 then return a leaf at c
L3  order S by the coordinate of axis, ties by the other coordinate;  h ← ⌊|S| / 2⌋
L4  S₁ ← the first h sinks of S;  S₂ ← the other |S| − h sinks
L5  T₁ ← MMM(S₁, the other axis);  T₂ ← MMM(S₂, the other axis)
L6  return a node at c, with wires from c to the roots of T₁ and T₂
L7  run MMM(all sinks, x) and connect the clock source to its root
```

Lines L3 and L4 split $S$ at its median in the current direction. The implementation sorts the sinks once by $x$ and once by $y$ and splits both lists in linear time at each node, which keeps both orders. A final tie break by the sink index makes the order total, so equal points are also split.

## Example

Take the sinks $s_1 = (0, 6)$, $s_2 = (0, 7)$, $s_3 = (2, 3)$ and $s_4 = (8, 6)$.

| set | split | centre of mass | edge to parent |
| --- | --- | --- | --- |
| $s_1, s_2, s_3, s_4$ | by $x$ | $(5/2, 11/2)$ | |
| $s_1, s_2$ | by $y$ | $(0, 13/2)$ | $5/2 + 1 = 7/2$ |
| $s_3, s_4$ | by $y$ | $(5, 9/2)$ | $5/2 + 1 = 7/2$ |
| $s_1$ and $s_2$ | | $(0, 6)$, $(0, 7)$ | $1/2$ each |
| $s_3$ and $s_4$ | | $(2, 3)$, $(8, 6)$ | $3 + 3/2 = 9/2$ each |

The paths to $s_1$ and $s_2$ have length $7/2 + 1/2 = 4$, and the paths to $s_3$ and $s_4$ have length $7/2 + 9/2 = 8$. The skew under linear delay is 4, and the total wire is 17. The far apart pair $s_3, s_4$ pulls its centre of mass to the middle, and both of its sinks are far from it.

On four sinks $(\pm 1, \pm 1)$ the root is $(0, 0)$, the halves have centres $(\pm 1, 0)$, and every path has length 2, the H-tree on these sinks.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The tree is a valid routing tree: each split gives two nonempty halves that partition the set, and the leaves are the sinks at their own points. The depth is exactly $\lceil \log_2 n \rceil$, since the larger half has $\lceil n/2 \rceil$ sinks. On $4^k$ sinks at the centres of a $2^k \times 2^k$ grid on a square of side $D$, two levels of splitting reach the centres of the four quarter squares, each at distance $D/4 + D/4$ from the centre, and leave four copies of the same problem with half the side. So every path has length $D (1 - 2^{-k})$ and the wire is $\frac{3}{2} D (2^k - 1)$, the values of the H-tree. For other inputs no bound on the skew is proved, and the example above shows a skew of half the longest path.

## Complexity

The two sorts take $O(n \log n)$ time. At a set $S$ the centre of mass and the split of both sorted lists take $O(|S|)$ time, the sets at one depth are disjoint, and there are $\lceil \log_2 n \rceil + 1$ depths, so the total is $O(n \log n)$. A version that sorts each set again takes $O(n \log^2 n)$; one that finds each median by linear-time selection also takes $O(n \log n)$. The tree has $2n - 1$ nodes, so the space is $\Theta(n)$.

## Properties

- The tree is a full binary tree of depth $\lceil \log_2 n \rceil$ (proved), so the number of branch points on every path is the same up to one.
- On a full $2^k \times 2^k$ grid of sinks it is the H-tree, with zero skew (proved).
- In general the skew is not zero, and no bound on it or on the wire length is proved.
- It is a top-down method: the topology and the embedding come from the same splits, and nothing is computed bottom up from delays.
- The result depends on the first split direction and on the tie break; a rotation of the input can change the tree.

## Variants and improvements

- **Topology for exact zero skew.** The most common use is as a topology generator. [Tsay's method](/tsay-zero-skew/) or [deferred-merge embedding](/deferred-merge-embedding/) on the MMM topology then gives exact zero skew, with the points of the nodes chosen bottom up instead of at the centres of mass.
- **Choice of direction.** Instead of alternating, each set can be split along the direction in which it is wider, or along the direction that gives the shorter wires.
- **Weighted sinks.** With load capacitances, the centre of mass can be weighted by the loads, and the split can balance the load instead of the count.
- **Recursive geometric matching.** A bottom-up alternative pairs the sinks by a minimum matching, joins each pair at a balance point, and repeats on the merged points.

## When to use it

Use it to get a balanced topology quickly for an irregular placement of sinks, especially as the first step of an exact zero-skew router. Use it on its own only when an approximately balanced tree is enough. For sinks on a regular array, the H-tree is the same tree with no computation. When the skew must be zero, embed the topology with deferred-merge embedding.

## Pitfalls

- MMM does not give zero skew, even under linear delay, except on special inputs such as a full grid. A claim of zero skew for general sinks is false.
- The centre of mass of a half can be far from all of its sinks when they are spread out, which gives long wires and large skew, as in the example.
- The tie break matters when many sinks share a coordinate. Without the second key and the index, a split can put equal points on both sides in an arbitrary way.
- The length of a path ignores the loads. Two paths of equal length can have very different Elmore delays.

## Implementations

## History

Jackson, Srinivasan and Kuh introduced the method of means and medians at the Design Automation Conference in 1990, to route clock nets in high-performance chips whose sinks are not on a regular grid, where the H-tree of earlier designs does not fit. The following methods kept its recursive topology but replaced the centres of mass with exactly balanced points: Tsay's exact zero skew in 1991, and deferred-merge embedding in 1992.

## References
