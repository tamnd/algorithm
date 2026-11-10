---
tag: 45V5QV
kind: problem
slug: streaming-maximal-matching-problem
name: Maximal matching in streams problem
aliases:
- matching in a graph stream
area: online-and-streaming/streaming-sketches
level: advanced
summary: Find a matching close to maximum in size from a stream of edges in semi-streaming space. One pass gives 1/2 by greedy, and no one-pass method can beat about 0.558.
prereqs: [maximal-matching, maximum-matching, streaming-model, approximation-ratio]
see_also: [greedy-streaming-matching, maximum-weight-matching, stream-connectivity-problem, agm-graph-sketch, streaming-triangle-counting-problem, index-problem, greedy-online-matching, augmenting-path]
sources:
  - paper: doi:10.1016/j.tcs.2005.09.013
    title: Joan Feigenbaum, Sampath Kannan, Andrew McGregor, Siddharth Suri and Jian Zhang, On graph problems in a semi-streaming model, Theoretical Computer Science 348(2-3), 2005
    locator: pp. 207 to 216; the definition of the semi-streaming model and the section on unweighted and weighted matching
  - paper: doi:10.1145/2627692.2627694
    title: Andrew McGregor, Graph stream algorithms, a survey, SIGMOD Record 43(1), 2014
    locator: the section on matchings (single-pass and multi-pass algorithms, weighted matching, lower bounds)
  - url: https://theory.epfl.ch/kapralov/papers/slb-full.pdf
    title: Michael Kapralov, Better bounds for matchings in the streaming model, SODA 2013
    locator: the main lower bound (no 1 − 1/e + ε approximation in one pass with n polylog n space, even for vertex arrivals)
  - url: https://dl.acm.org/doi/10.5555/3458064.3458176
    title: Michael Kapralov, Space lower bounds for approximating maximum matching in the edge arrival model, SODA 2021
    locator: pp. 1874 to 1893; the main theorem (the threshold 1/(1 + ln 2) ≈ 0.59 for one pass)
  - url: https://arxiv.org/abs/2607.14644
    title: Sepehr Assadi, Max Jiang and Mars Xiang, Semi-streaming matching in a single pass I, a new framework for lower bounds via blueprints, 2026
    locator: the main theorem (the threshold (8 − 2√10)/3 ≈ 0.558 for one pass)
---

The maximal matching in streams problem gives the edges of a graph one at a time and asks for a matching whose size is close to the size of a maximum matching, using memory near linear in the number of vertices, which is far less than the number of edges. A maximal matching, one to which no edge can be added, is the classical answer: the [greedy streaming matching](/greedy-streaming-matching/) builds one in a single pass, and it has at least half the size of a maximum matching. The main questions are how close to the maximum one pass can get, how many passes reach $1 - \varepsilon$, and what changes with weights, deletions, or a random order. On this page $n$ is the number of vertices, $m$ the number of edges, and $\nu(G)$ the size of a maximum matching.

## In plain words

A company receives a long list of possible pairs of workers who could share a task. Each worker can be in only one pair. The list is too long to store, so the company reads it once and decides at each line. The best possible plan, made with the whole list in hand, would form some number of pairs. The question is how many of those pairs a single reading can guarantee with little memory. The simple rule "pair them if both are still free" always gets at least half. Clever rules might do better, but researchers have proved that no rule can get more than about 56 percent in the worst case.

## Definition

**Stream.** The input is a sequence of the edges of a graph $G = (V, E)$ with $V = [n]$ known in advance. In the *insertion-only* model edges only arrive. In the *dynamic* model edges arrive and are deleted. In the *random-order* model the edges arrive in a uniformly random order instead of an order chosen by an adversary.

**Semi-streaming model.** Feigenbaum, Kannan, McGregor, Suri and Zhang (2005) allowed $O(n\,\mathrm{polylog}\,n)$ bits of memory. This is enough to store a matching or a spanning forest, but in general not the whole graph, since $m$ can be $\Theta(n^2)$.

**The problem.** Output a matching $M \subseteq E$ with $|M| \ge \alpha\,\nu(G)$, where $0 < \alpha \le 1$ is the approximation ratio. The algorithm makes $p$ passes over the stream, $p = 1$ unless stated. A randomized algorithm must succeed with constant probability for each fixed stream.

**Weighted version.** Edges have weights $w(e) > 0$, and the goal is a matching of total weight at least $\alpha$ times the [maximum weight matching](/maximum-weight-matching/).

**Size only.** A related problem asks only for an estimate of $\nu(G)$, not for the edges. This can be done in much less space for some graph classes and stream orders.

## Variants

- **One pass or several passes**, and the trade-off between passes and $\alpha$.
- **Bipartite or general graphs.** Some multi-pass bounds are better for bipartite graphs.
- **Weighted matching** and **b-matching**, where each vertex may be in up to $b$ edges.
- **Vertex arrivals.** The vertices of one side arrive with all their edges at once. Kapralov's 2013 bound holds even here.
- **Dynamic streams** with deletions, where the space needed for a good approximation grows close to $n^2$.
- **Random-order streams**, where one pass can beat $1/2$.

## Examples

**A 6-cycle.** On the cycle $1, 2, 3, 4, 5, 6$, $\nu = 3$. The stream order $\{2,3\}$, $\{1,2\}$, $\{3,4\}$, $\{5,6\}$, $\{4,5\}$, $\{1,6\}$ makes greedy take $\{2,3\}$ and $\{5,6\}$, a maximal matching of size 2. The greedy page traces it.

**The path that halves greedy.** On the path $1, 2, 3, 4$, $\nu = 2$, but if $\{2,3\}$ comes first, any maximal matching that contains it has size 1. So $1/2$ is the worst case for maximal matchings.

**Why one pass cannot be exact.** See the reduction under Bounds: deciding whether a perfect matching exists needs $\Omega(n^2)$ bits in one pass.

## Known algorithms

| algorithm | model | ratio | space or passes |
|---|---|---|---|
| [greedy streaming matching](/greedy-streaming-matching/) | one pass, any order | $1/2$ | $O(n \log n)$ bits |
| Feigenbaum et al. 2005, weighted | one pass | $1/6$ of the weight | semi-streaming |
| McGregor 2005, weighted | one pass | about $1/5.83$ | semi-streaming |
| Paz and Schwartzman 2017, local ratio | one pass | $1/(2 + \varepsilon)$ of the weight | semi-streaming |
| McGregor 2005, augmenting paths | $(1/\varepsilon)^{O(1/\varepsilon)}$ passes | $1 - \varepsilon$ | semi-streaming |
| Fischer, Mitrović and Uitto 2022 | $\mathrm{poly}(1/\varepsilon)$ passes, general graphs | $1 - \varepsilon$ | semi-streaming |
| Konrad, Magniez and Mathieu 2012 | one pass, random order | above $1/2$ | semi-streaming |
| store the graph and run [Edmonds](/edmonds-blossom/) | one pass | 1 | $O(m \log n)$ bits |

The multi-pass algorithms start from a maximal matching and, in each group of passes, find many short [augmenting paths](/augmenting-path/) at once, which removes the factor 2.

## Bounds

**Greedy is a 1/2-approximation.** A maximal matching $M$ touches every edge, each edge of a maximum matching $M^*$ has its own endpoint in $V(M)$, so $|M^*| \le 2|M|$. The [greedy page](/greedy-streaming-matching/) proves this in full.

**Exact matching needs Ω(n²) bits in one pass.** Use the [INDEX problem](/index-problem/) on $k^2$ bits: Alice holds $x \in \{0, 1\}^{k \times k}$ and Bob holds $(i, j)$. Alice streams a bipartite graph on $L = \{l_1, \ldots, l_k\}$ and $R = \{r_1, \ldots, r_k\}$ with the edge $\{l_a, r_b\}$ when $x_{ab} = 1$, and sends the memory. Bob adds new vertices $p_a$ for $a \ne i$ and $q_b$ for $b \ne j$, with the edges $\{l_a, p_a\}$ and $\{r_b, q_b\}$. A vertex $p_a$ has only one edge, so a perfect matching must use $\{l_a, p_a\}$, and similarly $\{r_b, q_b\}$. Then $l_i$ and $r_j$ are left and must be matched to each other. So the graph has a perfect matching exactly when $x_{ij} = 1$. The graph has $n = 4k - 2$ vertices, and INDEX needs $\Omega(k^2)$ bits, so any one-pass algorithm that decides whether a perfect matching exists, or computes $\nu$ exactly, needs $\Omega(n^2)$ bits.

**One-pass approximation thresholds.** In the semi-streaming model:

- Goel, Kapralov and Khanna (SODA 2012): no ratio above $2/3$.
- Kapralov (SODA 2013): no ratio above $1 - 1/e \approx 0.632$, even with vertex arrivals.
- Kapralov (SODA 2021): no ratio above $1/(1 + \ln 2) \approx 0.590$ with edge arrivals.
- Assadi, Jiang and Xiang (2026): no ratio above $(8 - 2\sqrt{10})/3 \approx 0.558$.

The bounds of Kapralov hold for space $n^{1 + o(1)}$, with the $o(1)$ of order $1/\log\log n$. So the best ratio in one pass is between $1/2$ and about $0.558$, and whether it exceeds $1/2$ is open.

**Dynamic streams.** With deletions, Assadi, Khanna, Li and Yaroslavtsev (SODA 2016) and Konrad (2015) showed that an $n^\varepsilon$-approximation needs about $n^{2 - 3\varepsilon}$ space, and sketches give nearly matching upper bounds. So semi-streaming space cannot give a constant ratio in one pass with deletions.

## Reductions

- **Vertex cover.** The endpoints of a maximal matching form a vertex cover at most twice the minimum, so one greedy pass gives a 2-approximate vertex cover.
- **From INDEX.** Lower bounds for exact matching and for perfect matching come from INDEX, as above; the approximation thresholds come from more complex communication problems built on random graphs.
- **Weighted to unweighted.** Rounding weights to powers of $1 + \varepsilon$ and running unweighted algorithms on the classes is a common step, at a loss of a constant factor.
- **To online matching.** A one-pass algorithm that never removes an edge is an online algorithm for edge arrivals, so bounds for [online matching](/greedy-online-matching/) and for streaming are closely related.

## Applications

- Matching in very large graphs, such as recommendation and assignment problems with many candidate pairs.
- A first step of multi-pass and parallel algorithms for maximum matching.
- An approximate vertex cover from the same pass.
- A test case for lower bound methods in streaming and communication complexity.

## References
