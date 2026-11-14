---
tag: S1Z8DM
kind: algorithm
slug: iterated-one-steiner
name: Iterated 1-Steiner heuristic
aliases:
- 1-Steiner heuristic
- Kahng-Robins heuristic
area: cad/routing
level: core
summary: Kahng and Robins's heuristic that repeatedly adds the Hanan grid point that shortens the rectilinear MST most, and stops when no point makes it shorter.
solves: [rectilinear-steiner-tree-problem]
model: real-ram
complexity:
  vars: {n: the number of pins, R: the number of rounds}
  time: {per_iteration: O(n^3 log n), total: O(R n^3 log n)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1990
  people: [Andrew B. Kahng, Gabriel Robins]
  note: Kahng and Robins presented the iterated 1-Steiner heuristic at ICCAD 1990, and the journal version appeared in IEEE Transactions on Computer-Aided Design in 1992.
prereqs: [rectilinear-minimum-spanning-tree, hanan-theorem]
see_also: [rectilinear-steiner-tree-problem, hanan-theorem, rectilinear-minimum-spanning-tree, hwang-rectilinear-steiner-ratio, flute, steiner-tree-problem, greedy-algorithm, local-search]
sources:
  - paper: doi:10.1109/43.144853
    title: Andrew B. Kahng and Gabriel Robins, A new class of iterative Steiner tree heuristics with good performance, IEEE Transactions on Computer-Aided Design 11(7), 893 to 902, 1992
    locator: the 1-Steiner step, its iteration over the Hanan points and the removal of Steiner points of degree at most 2
  - paper: "Andrew B. Kahng and Gabriel Robins, A new family of Steiner tree heuristics with good performance: the iterated 1-Steiner approach, Proceedings of ICCAD 1990, 428 to 431"
    locator: the conference version of the same method
  - paper: doi:10.1137/0114025
    title: M. Hanan, On Steiner's problem with rectilinear distance, SIAM Journal on Applied Mathematics 14(2), 255 to 265, 1966
    locator: the theorem that the candidate points can be taken on the grid of lines through the pins
  - paper: doi:10.1137/0130013
    title: F. K. Hwang, On Steiner minimal trees with rectilinear distance, SIAM Journal on Applied Mathematics 30(1), 104 to 114, 1976
    locator: the bound of 3/2 on the ratio of the rectilinear minimum spanning tree to the Steiner minimal tree
---

The iterated 1-Steiner heuristic of Andrew Kahng and Gabriel Robins builds a short rectilinear Steiner tree for a net in electronic design automation (EDA). It starts from the [rectilinear minimum spanning tree](/rectilinear-minimum-spanning-tree/) of the pins. In each round it tries every point of the Hanan grid, the crossings of the horizontal and vertical lines through the pins, as one extra Steiner point, and keeps the point that makes the minimum spanning tree shortest. It then drops Steiner points that no longer help, and repeats until no point makes the tree shorter. The tree is never longer than the minimum spanning tree, so it is within 3/2 of the optimum by [Hwang's theorem](/hwang-rectilinear-steiner-ratio/). It is exact for three pins, but not for all nets, since the [rectilinear Steiner tree problem](/rectilinear-steiner-tree-problem/) is NP-hard.

## In plain words

You must join some pins with horizontal and vertical wire, as short as possible. Joining the pins directly, pin to pin, is the minimum spanning tree. Often the wire gets shorter if you add a branch point that is not a pin, where three wires meet.

Where should such a point go? Draw a horizontal and a vertical line through every pin. Some best tree has all its branch points on the crossings of these lines, so only these crossings are worth trying.

Try each crossing in turn. Add it as an extra pin, compute the minimum spanning tree again, and see how much wire it saves. Keep the crossing that saves most. Then do it again with the new set of pins. If a branch point you added now joins only one or two wires, throw it away, because it saves nothing. Stop when no crossing saves any wire.

## The problem

The input is a set $P$ of $n$ pins in the plane. A rectilinear Steiner tree is a set $S$ of extra points, the Steiner points, and a tree on $P \cup S$ whose edges are drawn as horizontal and vertical wires, so that each edge $uv$ costs the L1 distance $d(u, v) = |x_u - x_v| + |y_u - y_v|$. The output is a tree of small total length. For a fixed $S$ the best tree is the minimum spanning tree $\mathrm{MST}(P \cup S)$ under L1, so the task is to choose $S$.

The *Hanan grid* of $P$ is the set of the crossings $(x_i, y_j)$ of the vertical lines through the pins and the horizontal lines through the pins, at most $n^2$ points. By [Hanan's theorem](/hanan-theorem/) some optimal tree has all its Steiner points on it. The *gain* of a point $x$ for the set $S$ is

$$\Delta(x, S) = |\mathrm{MST}(P \cup S)| - |\mathrm{MST}(P \cup S \cup \{x\})|.$$

## The algorithm

```pseudo id=main
ITERATED-1-STEINER(P)
L1  H ← the points of the Hanan grid of P that are not pins;  S ← ∅
L2  loop
L3      T ← MST(P ∪ S);  base ← length(T)
L4      for each x in H \ S do gain(x) ← base − length(MST(P ∪ S ∪ {x}))
L5      if no x has gain(x) > 0 then return T
L6      add to S a point x of largest gain
L7      repeat remove from S each point of degree at most 2 in MST(P ∪ S)
L8      until no point is removed
```

Line L4 does not build each tree from nothing. The minimum spanning tree of $P \cup S \cup \{x\}$ uses only edges of $T$ and edges from $x$, so it is the minimum spanning tree of a graph with fewer than $2(|P| + |S|)$ edges, found by [Kruskal's algorithm](/kruskal/) in $O(n \log n)$ time. Ties in line L6 go to the first point in the order of the Hanan grid, by $x$ and then by $y$.

## Example

Take the five pins $(0, 0)$, $(4, 1)$, $(1, 4)$, $(5, 5)$ and $(2, 3)$, the example of the [rectilinear minimum spanning tree](/rectilinear-minimum-spanning-tree/) page. The lines through the pins have $x \in \{0, 1, 2, 4, 5\}$ and $y \in \{0, 1, 3, 4, 5\}$, so the Hanan grid has 25 points, and 20 of them are not pins.

| round | base length | best points and gains | added |
| --- | --- | --- | --- |
| 1 | 16 | $(2, 1)$ and $(4, 3)$ with gain 2, six points with gain 1 | $(2, 1)$ |
| 2 | 14 | $(2, 4)$ with gain 1 | $(2, 4)$ |
| 3 | 13 | none | stop |

In round 1 the two best points tie, and $(2, 1)$ comes first in the order of the grid. Both added points have degree 3 in the tree, so line L7 removes nothing. The final tree has the edges

$(1,4)$ to $(2,4)$ of length 1, $(2,3)$ to $(2,4)$ of 1, $(4,1)$ to $(2,1)$ of 2, $(2,3)$ to $(2,1)$ of 2, $(0,0)$ to $(2,1)$ of 3 and $(5,5)$ to $(2,4)$ of 4,

with total length 13. A brute force over all sets of at most three Hanan points gives 13 as the optimum, so here the heuristic is exact, and it saves 3 of the 16 units of the minimum spanning tree.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **Fast gains.** The minimum spanning tree of $P \cup S \cup \{x\}$ can be taken from the edges of $\mathrm{MST}(P \cup S)$ and the edges from $x$. This is the cycle property: an edge $uv$ outside the old tree has a path in the old tree whose edges are all at most $d(u, v)$.
- **Removal is safe.** A Steiner point of degree 1 or 2 can be removed without making the tree longer, since its one or two edges can be replaced by nothing or by the direct edge between its two neighbors, which is no longer by the triangle inequality.
- **Never worse than the MST.** The length after every round is at most the length before it, so the output is at most $|\mathrm{MST}(P)|$, and so at most 3/2 times the optimum.
- **Termination.** Each round makes the length strictly shorter, so no set $S$ comes back, and there are finitely many subsets of the Hanan grid.
- **At most $n - 2$ Steiner points.** After line L8 every Steiner point has degree at least 3 in a tree with $n$ pins, which allows at most $n - 2$ of them.
- **Exact for three pins.** The point with the median $x$ and the median $y$ is on the Hanan grid, and the star from it has the optimal length, the half perimeter of the bounding box.

## Complexity

- **One round.** The Hanan grid has at most $n^2$ points. After line L8 there are at most $n - 2$ Steiner points, so each tree has fewer than $2n$ points. The gain of one point takes $O(n)$ edges from $x$ and a Kruskal run on $O(n)$ edges, which is $O(n \log n)$. A round is $O(n^3 \log n)$.
- **Rounds.** The proof bounds the number of rounds $R$ only by the finite number of subsets of the grid. Each round adds one point, so $R - 1$ is at least the number of Steiner points in the output. With integer coordinates each round saves at least 1, so $R \le |\mathrm{MST}(P)| + 1$.
- **Space.** The Hanan grid takes $\Theta(n^2)$ space, and the trees take $O(n)$.
- **Faster gains.** The gains of all points in a round can be computed faster than one Kruskal run per point, by data structures over the old tree. The implementation here uses the simple $O(n \log n)$ update per point.

## Properties

- **What is proved.** The output is a rectilinear Steiner tree no longer than the rectilinear minimum spanning tree, so its ratio to the optimum is at most 3/2. The loop ends. The output has at most $n - 2$ Steiner points. The output is optimal for $n \le 3$. The heuristic is not optimal on all inputs.
- **What is measured.** On random nets with integer coordinates from 0 to 99 (Python `random.Random(2026)`), compared with the brute-force optimum over pins plus at most $n - 2$ Hanan points: for 200 nets of 5 pins, the mean ratio to the optimum was 1.0008, the worst 1.0443, and 191 nets were optimal; for 25 nets of 6 pins, the mean was 1.0007, the worst 1.0170, and 24 were optimal. On the same nets the minimum spanning tree had mean ratios 1.1106 and 1.1065. These are toy inputs, not benchmark results.
- **Greedy.** Each round makes the choice with the best immediate gain. It is a [greedy algorithm](/greedy-algorithm/) and a form of [local search](/local-search/) over sets of Steiner points.
- **Deterministic.** With fixed tie rules the output depends only on the input.

## Variants and improvements

- **Batched 1-Steiner.** Instead of one point per round, sort the points by gain and add, in this order, each point whose gain is still positive after the points added before it in the round. This needs fewer rounds, and the length after each round is still never longer than before it.
- **Graphs and other metrics.** The same step works in any metric where a finite set of candidate points is known, and in graphs, where the candidates are the vertices that are not terminals.
- **Lookup tables.** For nets with few pins, [FLUTE](/flute/) finds an optimal tree from precomputed tables much faster, and it is the usual choice inside placement tools.
- **Exact methods.** For exact trees of larger nets, exact Steiner tree solvers use the [Hanan theorem](/hanan-theorem/) and full components. They are much slower than this heuristic.

## When to use it

- When a short rectilinear Steiner tree is needed for nets of up to a few hundred pins, and the time of a few rounds of $O(n^3 \log n)$ is acceptable.
- As a reference heuristic when testing faster Steiner tree methods.

For nets of a few pins inside an inner loop, use [FLUTE](/flute/). For a quick estimate with a proved bound, the [rectilinear minimum spanning tree](/rectilinear-minimum-spanning-tree/) is enough.

## Pitfalls

- **Keeping useless Steiner points.** After later points are added, an earlier Steiner point can end up with degree 2 or 1. If it is not removed, the number of Steiner points can grow past $n - 2$ and each round gets slower. The length is not hurt, but the bound on the round time is.
- **Rebuilding the MST from nothing.** Computing each gain with a fresh minimum spanning tree on all pairs costs $O(n^2)$ per point and $O(n^4)$ per round. Use the update from the old tree.
- **Candidates off the grid.** Points outside the Hanan grid are never needed for one optimal tree, and adding them as candidates only costs time.
- **Expecting optimal trees.** The greedy choice can be wrong: a point with the best gain now can block a better pair of points later. The measured results above show that this is rare on small random nets, but it is not proved to be rare.

## Implementations

## History

M. Hanan showed in 1966 that some optimal rectilinear Steiner tree has its Steiner points on the grid of lines through the pins, which gives a finite set of candidates. F. K. Hwang showed in 1976 that the minimum spanning tree is at most 3/2 times the optimal Steiner tree, so any method that starts from the spanning tree and never makes it longer keeps this bound. Andrew Kahng and Gabriel Robins presented the iterated 1-Steiner heuristic at ICCAD in 1990 and published the journal version in 1992. It became a common reference heuristic for rectilinear Steiner trees in VLSI routing. Later methods such as FLUTE (2005 and 2008) aimed at similar quality in much less time.

## References
