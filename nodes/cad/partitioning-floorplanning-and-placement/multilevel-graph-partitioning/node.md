---
tag: M115PE
kind: technique
slug: multilevel-graph-partitioning
name: Multilevel graph partitioning
aliases:
- multilevel partitioning
area: cad/partitioning-floorplanning-and-placement
level: core
summary: Coarsens the graph by matching heavy edges, partitions the coarsest graph, then uncoarsens with Kernighan-Lin or FM refinement at each level.
prereqs: [graph-partitioning-problem, kernighan-lin, fiduccia-mattheyses, maximal-matching]
see_also: [multilevel-hypergraph-partitioning, spectral-partitioning, graph-partitioning-problem, hypergraph-partitioning, multigrid-method, algebraic-multigrid, nested-dissection, graph-contraction]
sources:
  - paper: doi:10.1137/S1064827595287997
    title: George Karypis and Vipin Kumar, A fast and high quality multilevel scheme for partitioning irregular graphs, SIAM Journal on Scientific Computing 20(1), 359 to 392, 1998
    locator: the three phases, the matching schemes (random, heavy edge, light edge and heavy clique), greedy graph growing for the coarsest graph, and boundary Kernighan-Lin refinement
  - paper: doi:10.1145/224170.224228
    title: Bruce Hendrickson and Robert Leland, A multilevel algorithm for partitioning graphs, Proceedings of the 1995 ACM/IEEE Conference on Supercomputing, article 28, 1995
    locator: coarsening by contraction of a matching, and periodic Kernighan-Lin refinement on the way back (the Chaco code)
  - paper: "Thang Nguyen Bui and Curt Jones, A heuristic for reducing fill-in in sparse matrix factorization, Proceedings of the 6th SIAM Conference on Parallel Processing for Scientific Computing, 445 to 452, 1993"
    locator: an early use of contraction before Kernighan-Lin bisection, for separators in sparse matrix ordering
  - paper: doi:10.1002/cpe.4330060203
    title: Stephen T. Barnard and Horst D. Simon, Fast multilevel implementation of recursive spectral bisection for partitioning unstructured problems, Concurrency, Practice and Experience 6(2), 101 to 117, 1994
    locator: a coarse to fine computation of the Fiedler vector
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 2, Netlist and System Partitioning (multilevel methods; general locator)
---

Multilevel graph partitioning is a technique for the [graph partitioning problem](/graph-partitioning-problem/), most of all for balanced bisection of large sparse graphs. It has three phases. *Coarsening* contracts a [matching](/maximal-matching/) of the graph again and again, which gives a sequence of smaller graphs $G_0, G_1, \ldots, G_\ell$ with vertex and edge weights. *Initial partitioning* bisects the small graph $G_\ell$. *Uncoarsening* projects the bisection back one level at a time and improves it at each level with [Kernighan-Lin](/kernighan-lin/) or [Fiduccia-Mattheyses](/fiduccia-mattheyses/) refinement. The weights make the cut and the balance of a coarse partition equal to those of the fine partition it stands for, so nothing is lost on the way back, and the local search at each level moves whole clusters of the original graph at once. The method was developed by Bui and Jones (1993), Hendrickson and Leland (1995) and Karypis and Kumar (1998), whose METIS uses heavy edge matching. It is a heuristic and has no approximation guarantee. The hypergraph version, hMETIS, has its own page, [multilevel hypergraph partitioning](/multilevel-hypergraph-partitioning/).

## In plain words

You must split a big group of people into two equal teams, with as few friendships across the teams as possible. Looking at single people is slow, and a local swap of one person rarely helps.

So first pair each person with a close friend and treat each pair as one unit. Pair the units again, and go on until only a few units are left. Split these few units well, by hand. Then open the units again, one round at a time. After each round, try to move some of the smaller units to the other team if that removes friendships across. The early rounds move big blocks, the late rounds fix single people.

## When it applies

- **Large sparse graphs.** The graph has many vertices and few edges per vertex, as in finite element meshes, circuit graphs and sparse matrices. Each level costs time about linear in its size, so the method scales to millions of vertices.
- **Local structure.** The graph has clusters or a geometric shape, so that contracting heavy edges keeps the good cuts. Contraction cannot create a cut that did not exist, and a good partition must keep most heavy edges inside a part.
- **A local search is at hand.** The refinement is a move based method such as KL or FM. It works on weighted vertices and weighted edges.
- **Balance with some slack.** Coarse vertices have weights, so exact balance can be impossible on a coarse level. The method fits a balance window, for example each part within a few percent of half the weight.
- **Not useful** when the graph has no small cut, as for expanders, or when contraction stalls, as on a star, where each matching has one edge. For small graphs an exact method or plain FM is enough.

## The template

```pseudo id=main
MULTILEVEL-BISECT(G0, lo, hi)
L1  j ← 0
L2  while G_j has more than c vertices and the last step shrank it enough
L3      M ← a matching of G_j, for example heavy edge matching
L4      G_{j+1} ← G_j with each edge of M contracted; add vertex weights, add the weights of parallel edges, drop loops
L5      j ← j + 1
L6  s ← a bisection of G_j with weight of side 0 in [lo, hi]        ▷ greedy graph growing, spectral or exhaustive
L7  s ← REFINE(G_j, s, lo, hi)                                    ▷ KL or FM passes
L8  for i ← j − 1 down to 0
L9      s ← the projection of s to G_i: each vertex takes the side of the vertex it was merged into
L10     s ← REFINE(G_i, s, lo, hi)
L11 return s
```

Heavy edge matching visits the vertices in random order and matches each unmatched vertex with the unmatched neighbor joined by the heaviest edge. If $M$ is contracted, the total edge weight of $G_{j+1}$ is the total edge weight of $G_j$ less the weight of $M$. So the heavier the matching, the smaller the total weight of the coarse graph, and every cut of $G_{j+1}$ is at most that total. This is the reason for heavy edges in METIS.

The method rests on two facts, which hold for every matching.

- **Projection keeps the cut and the balance.** A bisection $s'$ of $G_{j+1}$ defines the bisection $s = s' \circ \pi$ of $G_j$, where $\pi$ maps each vertex to the vertex it was merged into. A coarse vertex weighs the sum of its preimage, so the side weights agree. A fine edge inside a merged pair is never cut, and the coarse edge $xy$ weighs the sum of the fine edges between the preimages of $x$ and $y$, so the cut weights agree.
- **Refinement never increases the cut.** A KL or FM pass keeps the best prefix of its tentative moves, and the empty prefix is allowed, so the cut after line L7 or line L10 is at most the cut before it.

So the output cut is at most the cut of the bisection of line L6, and it lies in $[lo, hi]$ if line L6 does. The converse does not hold: the coarse graph only has the bisections that keep every merged pair together, so the minimum bisection of $G_{j+1}$ can be larger than that of $G_j$. That is why the refinement at the fine levels is needed.

**Cost.** One step of matching and contraction costs $O(n_j + m_j)$ on a graph with $n_j$ vertices and $m_j$ edges, with a hash or a mark array to merge parallel edges. With gain buckets and small integer weights, an FM pass costs $O(n_j + m_j)$. If both counts shrink by a constant factor per level, the sums are geometric and the whole method costs $O(p (n + m))$ for at most $p$ passes per level. The shrink factor is not guaranteed: a maximal matching can be very small, as on a star, so line L2 stops when a step shrinks the graph too little.

### Example

Take the weighted ladder on 8 vertices: the rails $0\text{-}1\text{-}2\text{-}3$ and $4\text{-}5\text{-}6\text{-}7$ with edge weights $2, 1, 2$, and the four rungs $\{i, i + 4\}$ with weight 3. All vertices weigh 1, the total edge weight is 22, and the window is exactly 4 and 4.

| level | vertices (weights) | edges (weights) | total edge weight |
| --- | --- | --- | --- |
| $G_0$ | $0, \ldots, 7$ (1 each) | rails $2, 1, 2$; rungs 3 | 22 |
| $G_1$ | $A = \{0, 4\}$, $B = \{1, 5\}$, $C = \{2, 6\}$, $D = \{3, 7\}$ (2 each) | $AB$ 4, $BC$ 2, $CD$ 4 | 10 |
| $G_2$ | $\{A, B\}$, $\{C, D\}$ (4 each) | one edge, 2 | 2 |

In $G_0$ the heaviest edge at every vertex is its rung, so heavy edge matching picks the four rungs in every visiting order and removes weight 12. In $G_1$, a path with weights $4, 2, 4$, the heaviest edge at $B$ is $AB$ and at $C$ is $CD$, so every order matches $AB$ and $CD$ and removes weight 8. The coarsest graph has two vertices of weight 4, and its only balanced bisection has cut 2. Projected to $G_0$, it is $\{0, 1, 4, 5\} \mid \{2, 3, 6, 7\}$, with cut $1 + 1 = 2$, the same value, and no FM move improves it. A brute force over all 70 bisections of $G_0$ confirms that 2 is the minimum and that this split and its mirror are the only ones that reach it. The bound $n \lambda_2 / 4$ from the [graph partitioning problem](/graph-partitioning-problem/) page gives the same conclusion: here $\lambda_2 = 3 - \sqrt5 \approx 0.764$, so every bisection cuts at least $1.53$, and with integer weights at least 2.

## Classic examples

- **METIS** (Karypis and Kumar 1998). Heavy edge matching, coarsening until the graph has fewer than 100 vertices, greedy graph growing for the coarsest graph, and a boundary Kernighan-Lin refinement that looks only at the vertices on the cut. The paper also compares random, light edge and heavy clique matching. On its test graphs, which include finite element meshes, the authors report cuts better than those of [spectral partitioning](/spectral-partitioning/) in much less time. This is a measured result, not a theorem.
- **Chaco** (Hendrickson and Leland 1995). Contraction of matchings and Kernighan-Lin refinement applied on the way back.
- **Sparse matrix ordering.** Bui and Jones (1993) used contraction to improve KL bisection for separators. METIS uses the same multilevel bisection to find vertex separators for [nested dissection](/nested-dissection/).
- **Multilevel spectral bisection** (Barnard and Simon 1994). Here the levels serve only to compute the Fiedler vector fast, from coarse to fine; the split is still spectral.
- **Hypergraphs and circuits.** hMETIS coarsens hypergraphs with heavy edge or edge coarsening, and adds V-cycles; see [multilevel hypergraph partitioning](/multilevel-hypergraph-partitioning/). Min-cut placers use it at each cut; see [min-cut placement](/min-cut-placement/).

## Variations

- **Matching schemes.** Random matching, heavy edge, light edge and heavy clique matching; the last prefers pairs whose merge gives a dense coarse vertex.
- **Clustering instead of matching.** Merge more than two vertices at a time, which shrinks the graph faster and helps when matchings are small. Cap the weight of a coarse vertex, so that balance stays possible.
- **Initial partitioning.** Greedy graph growing from a random vertex (repeated a few times), a spectral split, or an exhaustive search when the coarsest graph is tiny.
- **Boundary refinement.** Move only the vertices that have a neighbor on the other side, kept in a hash table, so a pass costs time in the size of the boundary.
- **k-way partitions.** Bisect recursively, or coarsen once, split the coarsest graph into $k$ parts, and refine all $k$ parts together on the way back.
- **V-cycles.** Coarsen again with matchings inside each side, so the current partition is a partition of every coarse graph, and refine once more. The cut never increases.
- **The multigrid link.** The scheme is the same as in [multigrid](/multigrid-method/) and [algebraic multigrid](/algebraic-multigrid/) methods: coarsen, solve on the coarsest level, interpolate, and smooth. Here the smoother is a local search, not a relaxation of a linear system.

## Pitfalls

- **Forgetting the weights.** If the coarse graph counts parallel edges once, or ignores vertex weights, the cut and the balance on coarse levels are no longer those of the fine partition, and refinement optimizes the wrong value.
- **Heavy coarse vertices.** A coarse vertex that weighs more than the slack of the window can make every bisection of the coarsest graph unbalanced. Cap the merged weight.
- **Stalled coarsening.** On a star or on graphs with many leaves, a matching has few edges, so the levels shrink slowly. Stop when the shrink factor is too small, or merge leaves that share a neighbor.
- **Trusting the coarse optimum.** The minimum bisection of a coarse graph is at least the minimum of the fine graph, and can be larger. The fine refinements are needed, and even then the result is a local optimum.
- **Calling the result optimal.** The method has no approximation guarantee. Results on benchmarks are measurements on those graphs only.

## Exercises

1. Prove that projection keeps the cut and the side weights for every matching $M$, and that the total edge weight of $G_{j+1}$ is that of $G_j$ less the weight of $M$.
2. Show that every matching of the star $K_{1, k}$ has one edge. How many levels does heavy edge matching need to reach 2 vertices, and how would you change the coarsening?
3. In the unit weight $2 \times 4$ ladder (all 10 edges of weight 1), contract the matching $\{0, 4\}, \{1, 2\}, \{5, 6\}, \{3, 7\}$. Show that every balanced bisection of the coarse graph has cut 4, while the minimum bisection of the ladder has cut 2. Which FM moves at level 0 reach 2?
4. Without a cap on the merged weight, give a graph and a window $[lo, hi]$ for which the coarsest graph has no bisection inside the window. Then show that if every coarse vertex weighs at most $hi - lo + 1$ and the total weight is at least $lo$, a greedy fill always reaches the window.

## References
