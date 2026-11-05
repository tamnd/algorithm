---
tag: W63QYJ
kind: problem
slug: maximum-weight-matching
name: Maximum-weight matching
aliases:
- weighted matching
area: graphs/matching
level: advanced
summary: Find a matching of largest total edge weight in a general graph.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, N: the largest absolute value of an integer edge weight}
  time: {worst: O(n m + n^2 log n)}
prereqs: [maximum-matching, linear-programming-problem]
see_also: [minimum-weight-perfect-matching, matching-polytope, hungarian-algorithm, assignment-problem, edmonds-blossom, maximal-matching, min-cost-flow-problem, jonker-volgenant-algorithm]
sources:
  - paper: doi:10.6028/jres.069B.013
    title: Jack Edmonds, Maximum matching and a polyhedron with 0,1-vertices, Journal of Research of the National Bureau of Standards 69B, 125 to 130 (1965)
    locator: the whole paper (the primal-dual algorithm for weighted matching in general graphs)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency, Springer
    locator: Chapter 26, Weighted nonbipartite matching algorithmically (with the survey of running times), and Chapter 17, Weighted bipartite matching and the assignment problem
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer
    locator: Chapter 11, Weighted Matching
  - paper: "Harold N. Gabow, Data structures for weighted matching and nearest common ancestors with linking, Proceedings of the First Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 1990), 434 to 443 (1990)"
    locator: the whole paper (the O(nm + n^2 log n) implementation of Edmonds' algorithm)
  - paper: doi:10.1145/2529989
    title: Ran Duan and Seth Pettie, Linear-time approximation for maximum weight matching, Journal of the ACM 61(1), article 1 (2014)
    locator: the whole paper (a (1 - ε)-approximation in O(m ε^(-1) log ε^(-1)) time)
---

The maximum-weight matching problem asks for a matching of a graph whose edges have the largest total weight. It is the weighted form of [maximum matching](/maximum-matching/). On a [bipartite graph](/bipartite-graph/) it is a form of the [assignment problem](/assignment-problem/) and is solved by the [Hungarian algorithm](/hungarian-algorithm/). On a general graph, odd cycles make it harder, and Edmonds solved it in 1965 with a primal-dual algorithm over the [matching polytope](/matching-polytope/). The best strongly polynomial bound is $O(nm + n^2 \log n)$, by Gabow.

## In plain words

People must be put into pairs, and each possible pair has a score that says how good it is. Some people may stay alone. You want the pairs, with nobody in two pairs, that give the largest total score.

This is not the same as making as many pairs as possible. One very good pair can be worth more than two weak pairs that it blocks. With two separate groups, such as workers and jobs, the classical assignment methods work. When anyone may pair with anyone, a group of three people who all fit each other causes trouble, and the algorithm must treat such odd groups as single units for a while.

## Definition

Let $G = (V, E)$ be a finite undirected graph, general (odd cycles allowed) and weighted, with $n = |V|$, $m = |E|$, and a weight $w(e) \in \mathbb{R}$ for each edge. For integer weights, $N$ is the largest $|w(e)|$. A matching $M$ has weight $w(M) = \sum_{e \in M} w(e)$.

- **Input:** $G$ and $w$.
- **Output:** a matching $M$ with the largest $w(M)$.

An edge with $w(e) \le 0$ never needs to be used, so we may delete these edges. The empty matching, with weight 0, is a matching of every graph, so the answer always exists, and it is 0 for the graph with no edges.

**Linear programming form.** By Edmonds' theorem on the [matching polytope](/matching-polytope/), the optimum is the value of the linear program
$$\max\; w^{\mathsf T} x \quad \text{subject to} \quad x \ge 0, \;\; x(\delta(v)) \le 1 \;(v \in V), \;\; x(E[U]) \le \tfrac{|U| - 1}{2} \;(U \subseteq V, |U| \text{ odd}).$$
The dual has a variable $y_v \ge 0$ for each vertex and $z_U \ge 0$ for each odd set. It minimizes $\sum_v y_v + \sum_U \frac{|U| - 1}{2} z_U$ subject to $y_u + y_v + \sum_{U \ni u, v} z_U \ge w(uv)$ for each edge. A matching is optimal if and only if a dual solution with the same value exists, and Edmonds' algorithm always constructs one.

## Variants

- **Bipartite graphs.** Only the vertex constraints are needed. This is the weighted [bipartite matching](/bipartite-matching/) problem, solved by the [Hungarian algorithm](/hungarian-algorithm/), by [min-cost flow](/min-cost-flow-problem/), by the [auction algorithm](/auction-algorithm/) or by the [Jonker-Volgenant algorithm](/jonker-volgenant-algorithm/).
- **Perfect matching.** The matching must cover every vertex: [minimum-weight perfect matching](/minimum-weight-perfect-matching/), after negating the weights. The two problems reduce to each other, as shown below.
- **Maximum cardinality first.** Among the [maximum matchings](/maximum-matching/), find one of largest weight. Add a constant larger than the sum of all absolute weights to every weight.
- **Approximation.** A matching with weight at least $(1 - \varepsilon)$ times the optimum. Greedy by weight gives $\frac12$; Duan and Pettie give $1 - \varepsilon$ in $O(m \varepsilon^{-1} \log \varepsilon^{-1})$ time.
- **Online, streaming and dynamic models.** Each restricts how the input arrives; see [online bipartite matching](/online-bipartite-matching/), [greedy streaming matching](/greedy-streaming-matching/) and [dynamic matching](/dynamic-matching/).
- **Capacities.** Each vertex $v$ may have up to $b(v)$ matching edges: the weighted [b-matching](/b-matching/) problem.

## Examples

**Weight is not cardinality.** On the path $a - b - c - d$ with $w(ab) = 1$, $w(bc) = 3$ and $w(cd) = 1$, the maximum matching $\{ab, cd\}$ has weight 2, but $\{bc\}$ has weight 3, which is optimal.

**An odd cycle where greedy fails.** Take the 5-cycle $v_1 v_2 v_3 v_4 v_5$ with weight 5 on each edge, and a pendant vertex $t$ with $w(t v_1) = 2$. Greedy by weight takes $v_1 v_2$ and then $v_3 v_4$, with weight 10, and no edge can be added. The optimum is $\{t v_1, v_2 v_3, v_4 v_5\}$, with weight 12. So the best matching uses the lightest edge. This graph is not bipartite, so only an algorithm that handles the odd cycle as a blossom finds the optimum by local improvements.

**Negative and zero weights.** In a triangle with weights $-1$, $0$ and $-2$, the empty matching, of weight 0, is optimal.

**No perfect matching.** In the star $K_{1,3}$ with weights 1, 2, 3, the optimum is the single edge of weight 3, and no perfect matching exists. The maximum-weight matching is defined for every graph.

**The empty graph.** With no vertices, or no edges, the answer is the empty matching, of weight 0.

## Known algorithms

| algorithm | graphs | time |
|---|---|---|
| [Hungarian algorithm](/hungarian-algorithm/) with Fibonacci heaps | bipartite | $O(nm + n^2 \log n)$ |
| Gabow-Tarjan scaling | bipartite, integer weights | $O(m \sqrt n \log(nN))$ |
| Edmonds' primal-dual algorithm, as implemented by Gabow and by Lawler in the 1970s | general | $O(n^3)$ |
| Gabow's implementation of Edmonds' algorithm | general | $O(nm + n^2 \log n)$ |
| Duan, Pettie and Su scaling | general, integer weights | $O(m \sqrt n \log(nN))$ |
| greedy by weight | general | $O(m \log n)$, a $\frac12$-approximation |
| Duan-Pettie | general | $O(m \varepsilon^{-1} \log \varepsilon^{-1})$, a $(1 - \varepsilon)$-approximation |

The algorithm of Edmonds keeps a dual solution $(y, z)$ that satisfies the dual constraints, with $z_U > 0$ only on the sets $U$ that form nested [blossoms](/blossom/). It grows alternating trees using only *tight* edges, those whose dual constraint holds with equality, shrinks odd cycles of tight edges into blossoms, augments when it can, and otherwise changes the duals by the largest amount that keeps them feasible. It stops when the matching and the dual satisfy [complementary slackness](/complementary-slackness/). Kolmogorov's Blossom V is a widely used implementation of the perfect matching form.

**The greedy $\frac12$-approximation.** Sort the edges by weight, largest first, and add each edge whose ends are both free. Let $M$ be the result and $M^*$ an optimum. Each edge $e \in M^*$ either is in $M$ or shares an end with an edge $f \in M$ that was chosen before $e$ was considered, so $w(f) \ge w(e)$. Each $f \in M$ is charged in this way by at most two edges of $M^*$, one at each end. So $w(M^*) \le 2 w(M)$.

## Bounds

- **Upper bounds.** $O(nm + n^2 \log n)$ strongly polynomial on the [word RAM](/word-ram/); $O(m \sqrt n \log(nN))$ for integer weights.
- **Lower bound.** $\Omega(n + m)$, the size of the input.
- **Bipartite graphs.** Recent almost-linear-time [min-cost flow](/min-cost-flow-problem/) algorithms give $m^{1 + o(1)} \log N$ time for integer weights. No almost-linear bound is known for general graphs.
- **Approximation.** A $(1 - \varepsilon)$-approximation takes linear time for fixed $\varepsilon$, so exact computation is the hard part.

## Reductions

- **To minimum-weight perfect matching.** Make a copy $G'$ of $G$ with the same weights, and join each vertex $v$ to its copy $v'$ by an edge of weight 0. A matching $M$ of $G$ gives a perfect matching of $G \cup G'$: $M$, its copy, and the edges $vv'$ for the vertices that $M$ leaves exposed. Its weight is $2 w(M)$. Conversely, a perfect matching of $G \cup G'$ splits into a matching of $G$ and one of $G'$, so its weight is at most $2$ times the optimum. So the optimum of $G$ is half the maximum-weight perfect matching of $G \cup G'$, and negating weights turns that into a minimum-weight perfect matching problem.
- **From minimum-weight perfect matching.** Replace $w(e)$ by $C - w(e)$ with $C$ larger than $\sum_e |w(e)|$. Then every maximum-weight matching has the largest possible number of edges, so it is a perfect matching when one exists, and among perfect matchings it minimizes $w$.
- **Bipartite case to min-cost flow.** Direct the edges from $L$ to $R$ with unit capacities and cost $-w(e)$, and add a source and a sink; a [min-cost flow](/min-cost-flow-problem/) of any value, with the best value chosen, gives the optimum.

## Applications

- **Pairing with scores.** Pairing players, students or kidney donors and patients by compatibility scores.
- **Routing and tours.** With the reduction above, [Christofides' algorithm](/christofides-algorithm/) and the [Chinese postman problem](/chinese-postman-problem/) need weighted matchings.
- **Computer vision and physics.** Matching features between images, and decoding surface codes in quantum error correction, where a minimum-weight perfect matching of the error syndromes gives the most likely correction.
- **Scheduling.** Pairing jobs that can share a machine, with a benefit for each pair.

## References
