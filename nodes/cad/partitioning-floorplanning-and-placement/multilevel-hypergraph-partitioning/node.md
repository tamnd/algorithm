---
tag: FYFXXW
kind: algorithm
slug: multilevel-hypergraph-partitioning
name: Multilevel hypergraph partitioning
aliases:
- hMETIS algorithm
area: cad/partitioning-floorplanning-and-placement
level: advanced
summary: Karypis, Aggarwal, Kumar and Shekhar's multilevel scheme for hypergraphs with hyperedge coarsening and V-cycles of FM refinement, the base of netlist partitioners.
solves: [hypergraph-partitioning]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of nets, P: the number of pins, l: the number of levels, p: the largest number of FM passes on one level}
  time: {worst: "O(l (P log P + p (n + P)))", average: "O(l (P log P + p (n + P)))", best: "O(n + P log P)"}
  space: {extra: "O(n + l P)"}
properties: {deterministic: false, recursive: false, exact: false}
history:
  year: 1997
  people: [George Karypis, Rajat Aggarwal, Vipin Kumar, Shashi Shekhar]
  note: The method was presented at the Design Automation Conference in 1997 and published in IEEE Transactions on VLSI Systems in 1999 as hMETIS.
prereqs: [hypergraph-partitioning, multilevel-graph-partitioning, fiduccia-mattheyses]
see_also: [hypergraph-partitioning, multilevel-graph-partitioning, fiduccia-mattheyses, kernighan-lin, clique-net-model, spectral-partitioning, min-cut-placement, graph-partitioning-problem]
sources:
  - paper: doi:10.1109/92.748202
    title: George Karypis, Rajat Aggarwal, Vipin Kumar and Shashi Shekhar, Multilevel hypergraph partitioning, applications in VLSI domain, IEEE Transactions on VLSI Systems 7(1), 69 to 79, 1999
    locator: the coarsening schemes (edge, hyperedge and modified hyperedge coarsening), the initial partitioning, the FM and hyperedge refinement, and the V-cycle refinement with restricted coarsening
  - paper: "George Karypis, Rajat Aggarwal, Vipin Kumar and Shashi Shekhar, Multilevel hypergraph partitioning, application in VLSI domain, Proceedings of the 34th Design Automation Conference, 1997"
    locator: the conference version of the method
  - paper: doi:10.1137/S1064827595287997
    title: George Karypis and Vipin Kumar, A fast and high quality multilevel scheme for partitioning irregular graphs, SIAM Journal on Scientific Computing 20(1), 359 to 392, 1998
    locator: the multilevel scheme for graphs (METIS), with heavy edge matching and boundary refinement, which hMETIS carries over to hypergraphs
  - paper: doi:10.1109/DAC.1982.1585498
    title: C. M. Fiduccia and R. M. Mattheyses, A linear-time heuristic for improving network partitions, 19th Design Automation Conference, 175 to 181, 1982
    locator: the refinement used at each level, with gain buckets and the balance condition with vertex weights
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 2, Netlist and System Partitioning (the multilevel framework; general locator)
---

Multilevel hypergraph partitioning bisects a netlist in three phases. It merges groups of vertices again and again to get a small hypergraph, it partitions the small hypergraph, and it carries the partition back level by level with [Fiduccia-Mattheyses](/fiduccia-mattheyses/) (FM) refinement at each level. Karypis, Aggarwal, Kumar and Shekhar built it for circuits as hMETIS (1997, 1999), with *hyperedge coarsening*, which merges all pins of a net at once, and *V-cycles*, which coarsen and refine an existing partition again. It works on nets directly, so it minimizes the true cut of [hypergraph partitioning](/hypergraph-partitioning/), not a [clique model](/clique-net-model/) of it. It is a heuristic: it has no approximation guarantee, and its quality is known from benchmarks.

## In plain words

FM improves a split by moving one cell at a time. On a big netlist this is short-sighted: a whole cluster of cells may belong on the other side, but moving any one cell of it makes the cut worse, so FM never starts the move.

So first glue cells together. Cells that share a small net almost surely belong on the same side, so glue each such net into one heavy cell. Do this again on the glued netlist, until only a few heavy cells are left. Split those carefully. Then undo the gluing one level at a time, and at each level let FM move the cells of that level. A move of a heavy cell at a coarse level is the move of a whole cluster.

## The problem

The input is a [hypergraph](/hypergraph/) $H = (V, N)$ with $n$ vertices (cells) of integer weights $c(v) \ge 1$, $m$ nets of integer weights $w(e) \ge 1$ and $P = \sum_e |e|$ pins, and a balance window $lo \le hi$. The output is a bisection $V = V_0 \cup V_1$ with $lo \le c(V_0) \le hi$. The objective is a small cut, the total weight of the nets with pins on both sides. Finding the minimum is NP-hard; see [hypergraph partitioning](/hypergraph-partitioning/) for the variants and the hardness.

## The algorithm

A level is a hypergraph $H_j$. A *coarsening* of $H_j$ is a map $\pi_j$ from its vertices onto the vertices of $H_{j+1}$. A coarse vertex weighs the sum of the weights of its preimage. Each net $e$ becomes the net $\pi_j(e)$; nets with a single coarse pin are dropped, and equal coarse nets are merged with their weights added.

*Hyperedge coarsening* (HEC) visits the nets by non-increasing weight, then by non-decreasing size, in random order among ties. If no pin of the net is merged yet, it merges all its pins into one coarse vertex. Pins that no net merges stay as single vertices. Heavy nets come first because cutting them costs most; small nets come first because their pins are most tightly bound. The implementation also offers *edge coarsening* (EC), which visits the vertices in random order and matches each with the unmatched vertex that maximizes $\sum w(e)/(|e| - 1)$ over their shared nets.

The implementation caps the weight of a coarse vertex at $\mathit{cap}$, with $\max_v c(v) \le \mathit{cap} \le hi - lo + 1$ (by default $\max(1, hi - lo)$). This cap is a choice of this page, made so that a balanced start always exists at the coarsest level.

```pseudo id=main
MULTILEVEL-BISECT(H, lo, hi, c0, t, v)
L1  H_0 ← H; ℓ ← 0
L2  while H_ℓ has more than c0 vertices
L3      H_{ℓ+1} ← HEC(H_ℓ, cap); if no vertices merged then stop the loop
L4      ℓ ← ℓ + 1; if H_ℓ has more than 9/10 of the vertices of H_{ℓ−1} then stop the loop
L5  repeat t times
L6      s′ ← FM(H_ℓ, GREEDY-FILL(H_ℓ, lo, hi), lo, hi)
L7      if s′ has the least cut so far then s ← s′
L8  for j ← ℓ − 1 down to 0
L9      s ← the projection of s: each vertex of H_j takes the side of its coarse vertex
L10     s ← FM(H_j, s, lo, hi)
L11 repeat v times                                        ▷ V-cycles
L12     run lines L1 to L10 again, with HEC restricted to vertices on the same side of s, and with s projected down in place of lines L5 to L7
L13 return s
```

GREEDY-FILL puts the vertices on side 0 in random order, while $c(V_0) < lo$. FM is the Fiduccia-Mattheyses pass with vertex weights: each free vertex moves at most once, always the one of largest gain whose move keeps $c(V_0)$ in $[lo, hi]$, the best prefix of the pass is kept, and passes repeat while the best prefix has a positive gain. The implementation finds the vertex of largest gain by a scan instead of gain buckets, which is simpler but slower.

*Restricted coarsening* (line L12) merges only vertices on the same side of the current partition $s$. Then $s$ is a partition of every coarse level, with the same cut, and FM at the coarse levels can move whole clusters of $s$ across the cut.

## Example

Take $n = 10$ unit cells, unit nets and the window $[4, 6]$, so $\mathit{cap} = 2$:

$$ \{0,1,2\}, \{1,2,3\}, \{0,3,4\}, \{2,4\}, \{0,1\}, \;\; \{5,6,7\}, \{6,7,8\}, \{5,8,9\}, \{7,9\}, \{5,6\}, \;\; \{4,5\}, \{2,3,7\}. $$

The first five nets live on $\{0, \ldots, 4\}$, the next five on $\{5, \ldots, 9\}$, and the last two join the groups. The trace below is the run of the implementation with `random.Random(7)` and $c_0 = 8$.

**Coarsening.** All weights are 1, so HEC visits the five nets of size 2 first. It merges $\{2, 4\}$, $\{7, 9\}$, $\{0, 1\}$ and $\{5, 6\}$, then skips $\{4, 5\}$ because 4 and 5 are already merged. Every net of size 3 then has a merged pin. The cells 3 and 8 stay single. So $H_1$ has 6 vertices:

| coarse vertex | A | B | C | D | E | F |
| --- | --- | --- | --- | --- | --- | --- |
| cells | 2, 4 | 7, 9 | 0, 1 | 5, 6 | 3 | 8 |
| weight | 2 | 2 | 2 | 2 | 1 | 1 |

The nets of $H_1$ are $\{A, C\}$ of weight 1 (from $\{0,1,2\}$), $\{A, C, E\}$ of weight 2 (from $\{1,2,3\}$ and $\{0,3,4\}$, merged), $\{B, D\}$ of weight 1, $\{B, D, F\}$ of weight 2, $\{A, D\}$ of weight 1 (from $\{4,5\}$) and $\{A, B, E\}$ of weight 1 (from $\{2,3,7\}$). The nets $\{2,4\}$, $\{0,1\}$, $\{7,9\}$ and $\{5,6\}$ are inside coarse vertices and are dropped. $H_1$ has $6 \le c_0$ vertices, so coarsening stops.

**Initial partitioning.** The first greedy fill puts $\{C, D, F\}$ on side 0, weight 5. Its cut is 7: the nets $\{A, C\}$, $\{A, C, E\}$ (weight 2), $\{B, D\}$, $\{B, D, F\}$ (weight 2) and $\{A, D\}$ are cut. FM turns it into $\{A, C, E\} \mid \{B, D, F\}$, with weight 5 on side 0 and cut 2 (the nets $\{A, D\}$ and $\{A, B, E\}$). The other three trials, from starts with cuts 6, 7 and 7, end at the same partition.

**Uncoarsening.** Line L9 gives the cells $\{0, 1, 2, 3, 4\} \mid \{5, \ldots, 9\}$, with cut 2, the same as at level 1. FM finds no improving prefix.

**V-cycle.** Restricted coarsening merges $\{2,4\}$, $\{5,6\}$, $\{0,1\}$ and $\{7,9\}$ again (here the same pairs), each inside one side. FM at both levels keeps the partition. The result is $\{0, \ldots, 4\} \mid \{5, \ldots, 9\}$ with cut 2, the nets $\{4, 5\}$ and $\{2, 3, 7\}$. A brute force over all $2^{10}$ splits with 4 to 6 cells on side 0 confirms that 2 is the least cut for this window.

## Correctness

The [proof](proofs/correctness.md) shows the following for every input with $\max_v c(v) \le \mathit{cap} \le hi - lo + 1$ and $lo \le c(V)$.

- **Projection keeps the cut and the balance.** For every partition $s$ of $H_{j+1}$, its projection to $H_j$ has the same cut and the same weight on side 0.
- **A balanced start.** GREEDY-FILL always ends with $lo \le c(V_0) \le hi$, because while $c(V_0) < lo$ every vertex fits.
- **FM never worsens.** Each FM pass keeps the balance at every step and lowers the cut by its best prefix gain, which is at least 0. So FM ends, and its output is balanced and has a cut no larger than its input.
- **Balanced output.** By the three items, the output satisfies $lo \le c(V_0) \le hi$.
- **V-cycles never worsen.** Under restricted coarsening the current partition is a partition of every coarse level with the same cut, so a V-cycle returns a cut no larger than the one it started from.
- **Termination.** Each coarsening level that is kept removes at least one vertex, so there are at most $n$ levels; with the 9/10 rule there are $O(\log n)$.

## Complexity

Let $\ell$ be the number of levels and $P_j \le P$ the number of pins of $H_j$.

- **Coarsening.** One HEC level sorts the nets, scans the pins and builds the coarse nets with sorted pin lists, in $O(P_j \log P_j)$. EC costs $O(\sum_e |e|^2)$ per level, because each vertex scans the pins of its nets.
- **Levels.** Every kept level except the last has at most $9/10$ of the vertices of the one before, so $\ell \le 1 + \log_{10/9}(n / c_0) = O(\log n)$, and the vertex counts of all levels add up to at most $10 n$.
- **Refinement.** With gain buckets, one FM pass on $H_j$ costs $O(n_j + P_j)$. With $p$ passes per level and $t$ trials at the coarsest level, the total is $O(\ell (P \log P + p (n + P)))$ for a constant number of V-cycles. The implementation picks the vertex of largest gain by a scan and scans the pins of each net of a moved vertex, so its pass costs $O(n_j^2 + \sum_e |e|^2)$.
- **Space.** All levels are kept for the way back, $O(n + \ell P)$.

## Properties

Multilevel hypergraph partitioning is a heuristic. What is proved and what is measured are kept apart.

**What is proved.** The items of the correctness section: the output is balanced; projection keeps the cut; each FM pass and each V-cycle never increase the cut; and the output is a local optimum of FM at the finest level, that is, no balanced prefix of one more FM pass lowers the cut. No approximation ratio is known. The method is randomized, through the order of the nets in HEC and the greedy fills.

**What is measured.** Karypis and coauthors (1999) compared hMETIS with the netlist partitioners of the time on benchmark circuits and reported smaller cuts and shorter run times; the numbers are in their paper. The numbers below are from the implementation of this page, on toy inputs, and are not benchmark results. On 200 random hypergraphs with $n = 14$ unit cells and $m = 20$ unit nets of sizes 2 to 5 (generator `random.Random(2026)`, run $t$ seeded with `random.Random(t)`), with 6 to 8 cells on side 0 and $c_0 = 4$, compared with exhaustive bisection:

| method | optimal | mean of cut / optimum | worst |
| --- | --- | --- | --- |
| multilevel, 4 trials, 1 V-cycle | 191 of 200 | 1.007 | 1.333 |
| multilevel, 1 trial, no V-cycle | 175 of 200 | 1.018 | |
| flat FM from a random bisection | 164 of 200 | 1.031 | 1.667 |

At $n = 14$ flat FM already sees the whole netlist, so a small gap is expected. These numbers say nothing about large netlists, where the multilevel scheme was designed to help.

## Variants and improvements

- **Modified hyperedge coarsening (MHEC).** After HEC, the pins of each net that are still unmerged are merged with each other, so fewer single vertices remain.
- **Edge coarsening.** The EC scheme of the implementation, a heavy edge matching under the [clique net model](/clique-net-model/) with weight $1/(|e| - 1)$.
- **Hyperedge refinement.** Besides FM, hMETIS can move all pins of a cut net to one side at once (HER), which FM moves of single vertices cannot do in one step.
- **Many trials and the best of them.** Run the whole scheme with several seeds and keep the best result; cheap because each run is fast.
- **k-way partitioning.** Recursive bisection, or direct $k$-way refinement at each level, for the cut-net or the connectivity metric.
- **Later tools.** PaToH for sparse matrices and KaHyPar, with $n$-level coarsening that removes one vertex per level, follow the same multilevel idea.

## When to use it

Use a multilevel hypergraph partitioner for any netlist of more than a few thousand cells, and for hypergraph models of sparse matrices and parallel computations. It is the standard partitioner inside [min-cut placement](/min-cut-placement/). For a graph, the graph version, [multilevel graph partitioning](/multilevel-graph-partitioning/), is simpler and as good. For tiny instances, exhaustive search or an exact solver gives a proof of optimality, which this method never gives.

## Pitfalls

- **Coarse vertices that are too heavy.** If one coarse vertex weighs more than $hi - lo + 1$, a balanced partition of the coarse level may not exist, and the greedy start fails. Cap the weight, or allow a looser balance at coarse levels.
- **Large nets in HEC.** A net with many pins would merge many cells into one vertex. The order by size and the weight cap prevent this; tools also skip nets above a size limit.
- **Counting clique edges.** The cut is the weight of the cut nets. EC uses clique weights only to choose pairs, never as the objective.
- **Dropping merged nets wrongly.** Two fine nets with the same coarse image must become one coarse net with the sum of the weights. Dropping one of them makes the coarse cut wrong.
- **Stalled coarsening.** If a level merges almost nothing, the next level is the same size, and the loop would run forever. Stop when a level removes too few vertices.
- **Restricted coarsening forgotten.** A V-cycle that merges vertices across the cut destroys the current partition at the coarse levels.

## Implementations

## History

Multilevel partitioning of graphs grew from Bui and Jones (1993) and Hendrickson and Leland (1995), and Karypis and Kumar made it fast and robust in METIS (1995 to 1998). Karypis, Aggarwal, Kumar and Shekhar carried the scheme to hypergraphs as hMETIS, presented at DAC 1997 and published in 1999, with hyperedge coarsening and V-cycles. The authors reported smaller cuts than earlier netlist partitioners on the benchmarks of the time, and hMETIS became a common reference partitioner for placement and for later tools.

## References
