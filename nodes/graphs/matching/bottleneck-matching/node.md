---
tag: B4XQPW
kind: problem
slug: bottleneck-matching
name: Bottleneck matching
aliases:
- bottleneck assignment problem
area: graphs/matching
level: advanced
summary: Find a perfect matching that minimizes the largest edge weight.
prereqs: [assignment-problem, binary-search-on-answer]
see_also: [hopcroft-karp, perfect-matching, konig-theorem, hall-theorem, minimum-bottleneck-spanning-tree, bottleneck-tsp, widest-path, parametric-search]
sources:
  - paper: doi:10.1016/0196-6774(88)90031-4
    title: Harold N. Gabow and Robert E. Tarjan, Algorithms for two bottleneck optimization problems, Journal of Algorithms 9(3), 411 to 417 (1988)
    locator: the whole paper (bottleneck bipartite matching in O(m (n log n)^(1/2)) time)
  - book: isbn:9780898716634
    title: Rainer Burkard, Mauro Dell'Amico and Silvano Martello, Assignment Problems, SIAM (2009)
    locator: Chapter 6, Other types of linear assignment problems (Section 6.2, the linear bottleneck assignment problem, with threshold algorithms, dual method and the min-max theorem)
  - paper: "Oliver Gross, The bottleneck assignment problem, RAND Corporation paper P-1630 (1959)"
    locator: the whole paper (the problem and the min-max theorem)
---

The bottleneck matching problem asks for a [perfect matching](/perfect-matching/) whose largest edge weight is as small as possible. In its classic form, the bottleneck assignment problem, it assigns $n$ workers to $n$ jobs so that the slowest assignment is as fast as possible, the min-max cousin of the min-sum [assignment problem](/assignment-problem/). Only the order of the weights matters, so the problem reduces to a [binary search](/binary-search-on-answer/) over thresholds with one perfect-matching test per step. It is defined on weighted graphs, bipartite in the classic case and general in the broader one.

## In plain words

A team of workers must take a set of jobs, one each, and all jobs run at the same time. The work is done when the slowest worker finishes. So the total time does not matter; only the worst single assignment does.

The trick is to guess a time limit. Keep only the worker-job pairs that finish within it, and check whether everyone can still get a job. If yes, try a smaller limit; if no, a larger one. Because only the order of the times matters, the search runs over the distinct times in the input, and a handful of checks finds the best limit.

## Definition

**Input.** A graph $G = (V, E)$ with edge weights $w: E \to \mathbb{R}$. In the bipartite form, $G = (X \cup Y, E)$ with $|X| = |Y| = n$; in the assignment form, $G = K_{n,n}$ given by a cost matrix $C = (c_{ij})$.

**Output.** A perfect matching $M$ minimizing $\max_{e \in M} w(e)$, called the *bottleneck value* $b^*(G)$, or the answer that $G$ has no perfect matching. For $V = \emptyset$ the empty matching is perfect, with bottleneck value $-\infty$ by convention.

**Threshold view.** For a real $t$, let $G_t = (V, \{ e : w(e) \le t \})$. Then

$$b^*(G) = \min \{ t \in \{ w(e) : e \in E \} : G_t \text{ has a perfect matching} \},$$

since a perfect matching of $G_t$ has bottleneck at most $t$, and the bottleneck of any perfect matching is one of the weights. The property "$G_t$ has a perfect matching" is monotone in $t$, which makes binary search valid.

**Min-max theorem (bipartite).** For an $n \times n$ cost matrix,

$$\min_{\sigma} \max_i c_{i\sigma(i)} = \max \Bigl\{ \min_{i \in S,\, j \in T} c_{ij} : S, T \subseteq \{1, \ldots, n\},\; |S| + |T| = n + 1 \Bigr\}.$$

Every permutation meets every $S \times T$ with $|S| + |T| > n$, which gives $\ge$. For $\le$, let $b^*$ be the minimum; the graph of entries below $b^*$ has no perfect matching, so by the Frobenius and [Kőnig](/konig-theorem/) theorem, or [Hall's theorem](/hall-theorem/), its biadjacency matrix has an all-blank $S \times T$ with $|S| + |T| = n + 1$, and every entry there is at least $b^*$.

## Variants

- **Maximin.** Maximize the smallest weight of a perfect matching: negate the weights, or search for the largest threshold that keeps a perfect matching among the edges of weight at least $t$.
- **General graphs.** The same threshold search, with a perfect-matching test for general graphs such as [Edmonds' blossom algorithm](/edmonds-blossom/) or the [Micali-Vazirani algorithm](/micali-vazirani-algorithm/) in place of [Hopcroft-Karp](/hopcroft-karp/).
- **Bottleneck maximum matching.** When no perfect matching exists, minimize the largest weight among matchings of maximum size $\nu(G)$; the threshold test becomes $\nu(G_t) = \nu(G)$.
- **Lexicographic bottleneck.** Minimize the largest weight, then the second largest, and so on; it can be solved by a sequence of bottleneck and sum problems with rescaled weights.
- **Balanced assignment.** Minimize $\max - \min$ of the weights in the matching, solved by sliding a window over the sorted weights with incremental matching tests.
- **Geometric bottleneck matching.** Match two sets of $n$ points so that the longest segment is shortest; the threshold test uses geometric data structures to avoid building all $n^2$ edges.
- **Related bottleneck problems.** The [minimum bottleneck spanning tree](/minimum-bottleneck-spanning-tree/), the [widest path](/widest-path/) and the [bottleneck travelling salesman problem](/bottleneck-tsp/) apply the same min-max objective to other structures.

## Examples

**A 4 by 4 matrix.** The cost matrix of the [assignment problem](/assignment-problem/) page,

$$C = \begin{pmatrix} 9 & 2 & 7 & 8 \\ 6 & 4 & 3 & 7 \\ 5 & 8 & 1 & 8 \\ 7 & 6 & 9 & 4 \end{pmatrix},$$

has the min-sum optimum $\sigma = (2, 1, 3, 4)$ with cost 13 and largest entry 6. The bottleneck optimum is $\sigma = (2, 3, 1, 4)$: entries 2, 3, 5, 4, largest 5, sum 14. The threshold search: the distinct values are $1, \ldots, 9$; at $t = 4$ the allowed entries are $c_{12}, c_{22}, c_{23}, c_{33}, c_{44}$, and column 1 has none, so no perfect matching; at $t = 5$ the entry $c_{31}$ is added, and $\{12, 23, 31, 44\}$ is perfect. The min-max certificate is $S = \{1, 2, 3, 4\}$, $T = \{1\}$: $|S| + |T| = 5$ and the smallest entry of column 1 is 5.

**Sum and bottleneck disagree.** With $C = \begin{pmatrix} 1 & 4 \\ 4 & 5 \end{pmatrix}$ the min-sum assignment is the diagonal, sum 6 and largest entry 5, while the bottleneck assignment is the anti-diagonal, sum 8 and largest entry 4.

**No perfect matching.** The bipartite graph with $X = \{x_1, x_2\}$, $Y = \{y_1, y_2\}$ and only the edges $x_1 y_1$, $x_2 y_1$ has no perfect matching at any threshold, and the answer is "none". So does the triangle, a general graph with an odd number of vertices.

**General graph.** In the 4-cycle $a\,b\,c\,d$ with weights $ab = 1$, $bc = 5$, $cd = 2$, $da = 3$, together with the chord $ac$ of weight 1, the perfect matchings are $\{ab, cd\}$ with bottleneck 2 and $\{bc, da\}$ with bottleneck 5; the chord is in no perfect matching. So $b^* = 2$.

**Edge cases.** For $n = 1$ the answer is the only edge. If all weights are equal, every perfect matching is optimal. Ties do not matter: only the set of distinct weights is searched.

## Known algorithms

- **Threshold binary search.** Sort the $m$ weights and binary search over them, testing each threshold with [Hopcroft-Karp](/hopcroft-karp/): $O(m \log m)$ for sorting plus $O(\log m)$ tests of $O(m\sqrt n)$ each, $O(m\sqrt n \log n)$ in total. In general graphs the test is a maximum matching in a general graph.
- **Incremental augmentation.** Add edges in increasing order of weight and keep a maximum matching, keeping the alternating search from the free vertices alive and extending it as each edge arrives; between two augmentations the search scans each edge once, so the $n$ augmentations cost $O(nm)$ in total, and the weight that completes a perfect matching is the answer. Mixing the two, a binary search to a good starting matching and then augmentations, works well in practice.
- **Gabow and Tarjan (1988).** A refined threshold search that reuses the matching between thresholds and balances the search against the augmentation work: $O(m\sqrt{n \log n})$ time for bipartite graphs.
- **Dual and shortest-path methods.** Burkard and coauthors describe threshold methods with a good starting threshold, such as the largest of the row and column minima, and augmenting-path methods that work directly on the bottleneck objective; their Chapter 6 compares the methods on dense matrices.
- **Through the assignment problem.** Replacing each cost by a rapidly growing function of its rank, such as $(n + 1)^{\text{rank}}$, makes any min-sum optimum a bottleneck optimum, but the numbers grow to $\Theta(m \log n)$ bits; useful in theory, slow in practice.

## Bounds

- **Upper bounds.** $O(m\sqrt{n \log n})$ for bipartite graphs, by Gabow and Tarjan; $O(m\sqrt n \log n)$ by the plain threshold search; any improvement in bipartite perfect-matching time carries over with an $O(\log n)$ factor, so [almost-linear max flow](/almost-linear-max-flow/) gives $m^{1 + o(1)}$.
- **Lower bound.** $\Omega(m)$, since every edge weight can matter: lowering one unread weight can change the answer.
- **Comparison model.** Only comparisons between weights are needed, so the problem is solved exactly for any totally ordered weights, without arithmetic.

## Reductions

- **To perfect matching.** $O(\log m)$ perfect-matching tests on threshold graphs, as above; this is the [binary search on the answer](/binary-search-on-answer/) pattern.
- **To the assignment problem,** by exponential rescaling of ranks, as above.
- **From perfect matching.** Give every edge weight 0: a bottleneck matching exists if and only if a perfect matching does, so bottleneck matching is at least as hard as deciding perfect matching.
- **Maximin and minimax** reduce to each other by negating the weights.

## Applications

- Assigning parallel jobs to machines when the makespan is set by the slowest pair, as in production lines where all stations work at the pace of the slowest one.
- Matching sensors to targets or robots to goals so that the longest travel distance is small, for example to bound the time for a fleet to reach a formation.
- Comparing two point sets by the bottleneck distance, a measure used for persistence diagrams in topological data analysis.
- Scheduling with deadlines, where every assignment must fit under a common time limit, and the smallest feasible limit is wanted.

## References
