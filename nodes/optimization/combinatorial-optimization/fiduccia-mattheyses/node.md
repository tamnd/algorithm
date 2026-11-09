---
tag: K9FVJG
kind: algorithm
slug: fiduccia-mattheyses
name: Fiduccia-Mattheyses algorithm
aliases:
- FM algorithm
- Fiduccia-Mattheyses heuristic
- FM refinement
area: optimization/combinatorial-optimization
level: advanced
summary: Linear-time-per-pass refinement of a partition by moving single vertices with bucket gains.
solves: [graph-partitioning-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, P: the total number of pins (sum of net sizes), p: the number of passes}
  time: {worst: Θ(p (n + P)), average: Θ(p (n + P)), best: Θ(n + P)}
  space: {extra: Θ(n + P)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1982
  people: [Charles M. Fiduccia, Robert M. Mattheyses]
  note: Fiduccia and Mattheyses presented the method at the 19th Design Automation Conference in 1982, as a linear-time version of the Kernighan-Lin idea for circuit netlists.
prereqs: [kernighan-lin, hypergraph, bucket-queue]
see_also: [kernighan-lin, graph-partitioning-problem, hypergraph, bucket-queue, doubly-linked-list, local-search, local-optimum, simulated-annealing]
sources:
  - paper: doi:10.1109/DAC.1982.1585498
    title: C. M. Fiduccia and R. M. Mattheyses, A linear-time heuristic for improving network partitions, 19th Design Automation Conference, 175 to 181, 1982
    locator: the gain buckets, the critical net update rules, the balance condition and the linear time bound per pass
  - paper: doi:10.1002/j.1538-7305.1970.tb01770.x
    title: B. W. Kernighan and S. Lin, An efficient heuristic procedure for partitioning graphs, Bell System Technical Journal 49(2), 291 to 307, 1970
    locator: the pass of tentative moves with locking and the best prefix
  - paper: doi:10.1137/S1064827595287997
    title: George Karypis and Vipin Kumar, A fast and high quality multilevel scheme for partitioning irregular graphs, SIAM Journal on Scientific Computing 20(1), 359 to 392, 1998
    locator: the refinement phase, which uses variants of Kernighan-Lin and Fiduccia-Mattheyses with gain buckets
  - paper: "B. Krishnamurthy, An improved min-cut algorithm for partitioning VLSI networks, IEEE Transactions on Computers C-33(5), 438 to 446, 1984"
    locator: the higher-level gains used to break ties
  - paper: "Charles J. Alpert and Andrew B. Kahng, Recent directions in netlist partitioning, a survey, Integration, the VLSI Journal 19(1 to 2), 1 to 81, 1995"
    locator: the section on iterative improvement and the Fiduccia-Mattheyses family
---

The Fiduccia-Mattheyses (FM) algorithm is a [local search](/local-search/) heuristic that improves a two-way partition of a graph or [hypergraph](/hypergraph/) so that fewer edges or nets cross between the sides. It follows the plan of [Kernighan-Lin](/kernighan-lin/): a pass makes tentative moves, locks each moved vertex, goes on through moves with negative gain, and then keeps only the best prefix. The difference is that FM moves one vertex at a time, under a balance tolerance, and keeps the vertices in *gain buckets* indexed by their gain. With the critical net rules for updating gains, a whole pass takes $O(n + P)$ time, where $P$ is the number of pins, instead of $\Theta(n^3)$ for the direct Kernighan-Lin pass. Like Kernighan-Lin it has no proved approximation ratio. It is the standard refinement step in multilevel partitioners for graphs and circuits.

## In plain words

You have split the parts of a circuit into two groups, and you want fewer wires between the groups. The groups may differ in size a little, but not much.

A pass works like this. Find the part whose move to the other group helps the most, or hurts the least, among the moves that keep the sizes within the limit. Move it on paper and freeze it. Repeat until no part can move. Then look back and keep only the first moves that together helped most.

The trick is in the bookkeeping. Each part sits in a numbered box that says how much its move would help. After each move only a few parts change boxes, and finding the best part is just a look into the highest box that is not empty. So a pass takes time in proportion to the size of the circuit.

## The problem

The input is a hypergraph with vertices $0, \ldots, n-1$ and a list of *nets*, each a set of vertices (its *pins*), together with a partition into sides 0 and 1 and limits $lo \le hi$ on the number of vertices on side 0. A graph is the case where every net has two pins. A net is *cut* if it has pins on both sides. The output is a partition that keeps the size of side 0 in $[lo, hi]$ and has a small cut. Finding the least cut is NP-hard (see the [graph partitioning problem](/graph-partitioning-problem/)), so FM aims at a good cut.

For a vertex $v$ on side $s$, its *gain* $g(v)$ is the number of nets in which $v$ is the only pin on side $s$, minus the number of nets that lie entirely on side $s$. Moving $v$ alone lowers the cut by exactly $g(v)$. If $v$ is on at most $p_{\max}$ nets, then $-p_{\max} \le g(v) \le p_{\max}$, so the gains fit in an array of $2 p_{\max} + 1$ buckets.

## The algorithm

```pseudo id=main
FIDUCCIA-MATTHEYSES(H, side, lo, hi)
L1  repeat
L2      count the pins of each net on each side; compute every gain g(v); put each vertex in bucket g(v) of its side; unlock all
L3      while some free vertex can move with the size of side 0 staying in [lo, hi] do
L4          among the sides allowed to give a vertex, take a free vertex v from the highest non-empty bucket (ties: the larger side)
L5          remove v from its bucket, lock it, and record g_p ← g(v) and v_p ← v
L6          for each net e of v, update the gains of the free pins of e by the critical net rules
L7          move v to the other side
L8      choose the smallest k ≥ 0 that maximizes G_k = g_1 + ⋯ + g_k  (G_0 = 0)
L9      if G_k ≤ 0 then exit the loop
L10     move v_1, …, v_k in the real partition
L11 return side
```

The *critical net rules* of line L6 handle a move of $v$ from side $F$ (from) to side $T$ (to). Let $F(e)$ and $T(e)$ be the numbers of pins of $e$ on the two sides.

- Before the move: if $T(e) = 0$, add 1 to the gain of every free pin of $e$; if $T(e) = 1$, subtract 1 from the gain of the single pin on side $T$, if it is free.
- Then $F(e)$ falls by 1 and $T(e)$ grows by 1.
- After the move: if $F(e) = 0$, subtract 1 from the gain of every free pin of $e$; if $F(e) = 1$, add 1 to the gain of the single pin on side $F$, if it is free.

A net with locked pins on both sides stays cut for the rest of the pass, and the rules never change gains through it. Each bucket is a [doubly linked list](/doubly-linked-list/), as in a [bucket queue](/bucket-queue/), so a vertex changes bucket in $O(1)$ time, and a pointer to the highest non-empty bucket of each side moves only by small steps.

## Example

Take the graph of the [graph partitioning](/graph-partitioning-problem/) page, as nets with 2 pins: two triangles $a, b, c$ and $d, e, f$ joined by the edges $cd$ and $be$. Start from side 0 $= \{a, b, d\}$ and side 1 $= \{c, e, f\}$, with cut 6, and allow 2 to 4 vertices on side 0. For a graph the gain of $v$ is the number of its edges to the other side minus the number to its own side.

| step | free gains before the step (side 0 \| side 1) | allowed to give | moved | $g_p$ | $G_p$ | cut | size of side 0 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | $a\,0, b\,1, d\,3 \mid c\,3, e\,1, f\,0$ | both | $d$ | 3 | 3 | 3 | 2 |
| 2 | $a\,0, b\,1 \mid c\,1, e\,{-1}, f\,{-2}$ | side 1 | $c$ | 1 | 4 | 2 | 3 |
| 3 | $a\,{-2}, b\,{-1} \mid e\,{-1}, f\,{-2}$ | both | $b$ | $-1$ | 3 | 3 | 2 |
| 4 | $a\,0 \mid e\,{-3}, f\,{-2}$ | side 1 | $f$ | $-2$ | 1 | 5 | 3 |
| 5 | $a\,0 \mid e\,{-1}$ | both | $a$ | 0 | 1 | 5 | 2 |
| 6 | $\mid e\,{-1}$ | side 1 | $e$ | $-1$ | 0 | 6 | 3 |

In step 1, $d$ and $c$ both have gain 3, the sides have equal size, and the tie goes to side 0. After step 1, side 0 has only 2 vertices, so in step 2 only side 1 may give a vertex. The best prefix is $k = 2$ with $G_2 = 4$, so line L10 moves $d$ and $c$, and the cut falls from 6 to 2. This is the optimal bisection, reached by two single moves instead of one swap. The second pass has gains $-1, -1, 0, 0, 1, 1$, so no prefix helps and line L9 stops.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **Gain formula.** Moving $v$ alone lowers the cut by exactly $g(v)$, the number of nets where $v$ is alone on its side minus the number of nets entirely on its side.
- **Gain updates.** A case analysis of the counts $F(e)$ and $T(e)$ shows that the critical net rules give exactly the change of each free gain.
- **Selection.** The bucket pointers never fall below the highest non-empty bucket, so line L4 takes a free vertex of largest gain among the moves that keep the balance.
- **Balance and progress.** Every tentative partition is balanced, and the partition after $k$ moves has cut $C - G_k$. So each applied pass lowers the cut by $G_k > 0$.
- **Termination and local optimality.** The cut is a non-negative integer, so there are at most $C + 1$ passes for a start with cut $C$. In the output, no single move that keeps the balance lowers the cut.

## Complexity

Let $P$ be the number of pins.

- **Per pass.** Line L2 takes $O(n + P)$ time. In a pass, each net starts a scan of its pins at most 8 times, because each rule changes the counts or the locked pins of the net in a way that cannot be undone in the same pass. So all scans take $O(P)$ time, and each scan step moves one vertex between buckets in $O(1)$ time. The bucket pointers rise by at most 1 per gain increase, so their total movement is also $O(P)$. A pass takes $\Theta(n + P)$ time, which is $\Theta(n + m)$ for a graph with $m$ edges.
- **Number of passes.** At most $C + 1$ for a start with cut $C$. Fiduccia and Mattheyses reported that few passes are needed in practice. In our measurement below, the mean was 2.3 passes, counting the last pass that changes nothing.
- **Space.** The net lists of the vertices, the pin counts and the buckets take $\Theta(n + P)$ space.

## Properties

- **Heuristic.** FM has no proved approximation ratio. Its output is a local optimum for single balanced moves, and also for every prefix of the last pass.
- **Needs slack.** A single move changes the sizes of the sides. With exact balance, $lo = hi$, no move is allowed at all. A tolerance of at least one vertex, or of the largest vertex weight, is needed.
- **Deterministic.** The tie rules (the larger side first, then the last vertex added to the bucket) fix the result.
- **Measured quality.** On 300 random graphs $G(14, 0.3)$ (Python `random.Random(2026)`), started from a random bisection with 6 to 8 vertices allowed on side 0, FM found on average 1.032 times the best cut over all such partitions, computed by brute force, with median 1.000 and maximum 1.5. It was optimal in 82 percent of the graphs. These are small graphs, so this measures behavior, not a bound.

## Variants and improvements

- **Vertex weights.** Fiduccia and Mattheyses allow cells of different sizes. A move is allowed if the weight of each side stays within the target ratio plus or minus the largest cell weight.
- **Tie breaking.** Krishnamurthy (1984) added higher-level gains that look ahead to break ties among vertices of equal gain. The order inside a bucket also matters: experiments found that last in, first out works better than first in, first out.
- **k-way FM.** Keep gains for moves to each of the other parts, or refine pairs of parts in turn.
- **Multilevel refinement.** Coarsen the graph by matchings, partition the coarsest graph, and run FM passes at each level on the way back. METIS for graphs and hMETIS for hypergraphs follow this scheme. A boundary version only puts vertices next to the cut into the buckets.
- **Early stop.** Stop a pass after a number of moves without improvement. This saves time on large graphs with little loss of quality.

## When to use it

- To refine a partition of a large sparse graph or a circuit netlist, where the $\Theta(n^3)$ pass of [Kernighan-Lin](/kernighan-lin/) is too slow.
- For hypergraphs, where swaps of pairs do not fit the net cut well.
- As the refinement step of a multilevel partitioner.

When the sides must have exactly equal sizes and the graph is small, [Kernighan-Lin](/kernighan-lin/) swaps fit better. For a proof of optimality, use exact methods.

## Pitfalls

- **Wrong order of the rules.** The rules for $T(e)$ use the counts before the move, and the rules for $F(e)$ use the counts after it. Mixing them gives wrong gains without any error message.
- **Updating locked vertices.** Only free pins change buckets. A locked vertex is out of the buckets for the rest of the pass.
- **Stale bucket pointer.** After a gain increase the pointer of the side must rise to the new bucket if needed, and line L4 must skip empty buckets downward.
- **Single-pin nets.** A net with one pin is never cut. The formula gives it a contribution of $1 - 1 = 0$, which is correct, but special code for nets must not count it twice.
- **No tolerance.** With $lo = hi$ the algorithm makes no move and returns the start.

## Implementations

## History

Charles Fiduccia and Robert Mattheyses, at General Electric, presented the method at the Design Automation Conference in 1982. They kept the pass structure of Kernighan and Lin (1970) but moved single cells, added a balance condition with cell sizes, and showed that the bucket structure and the critical net rules make a pass linear in the size of the netlist. Krishnamurthy (1984) refined the gains, and in the 1990s FM became the refinement engine of multilevel tools such as METIS (Karypis and Kumar) and hMETIS. Most partitioners for circuits, meshes and sparse matrices still use a variant of it.

## References
