---
tag: AECSN6
kind: problem
slug: distributed-dominating-set
name: Distributed dominating set
aliases:
- distributed minimum dominating set
- distributed domination
area: distributed/distributed-graph-algorithms
level: advanced
summary: Approximate a minimum dominating set by local communication. LP rounding gives O(log Delta) in O(log n / eps) rounds; KMW shows polylog ratios need Omega(log Delta / log log Delta) rounds.
prereqs: [local-model, dominating-set, lp-relaxation]
see_also: [kmw-lower-bound, dominating-set-inapproximability, greedy-set-cover, lp-rounding-set-cover, distributed-minimum-vertex-cover, distributed-mis, set-cover, network-decomposition]
sources:
  - paper: doi:10.1007/s00446-002-0078-0
    title: Lujun Jia, Rajmohan Rajaraman and Torsten Suel, An efficient distributed algorithm for constructing small dominating sets, Distributed Computing 15(4), 2002
    locator: pp. 193 to 205 (a randomized distributed version of the greedy algorithm with expected ratio O(log Delta) in O(log n log Delta) rounds; also PODC 2001)
  - paper: doi:10.1007/s00446-004-0112-5
    title: Fabian Kuhn and Roger Wattenhofer, Constant-time distributed dominating set approximation, Distributed Computing 17(4), 2005
    locator: pp. 303 to 310 (expected ratio O(k Delta^(2/k) log Delta) in O(k^2) rounds, by LP relaxation and rounding; also PODC 2003, doi:10.1145/872035.872040, pp. 25 to 32)
  - paper: doi:10.1145/2742012
    title: Fabian Kuhn, Thomas Moscibroda and Roger Wattenhofer, Local computation, lower and upper bounds, Journal of the ACM 63(2), 2016
    locator: Section 4.1 (the lower bound for dominating set by the line graph reduction, Theorem 15 and Corollary 16 in arXiv 1011.5470v2) and Section 5 (covering LPs within 1 + eps in O(log n / eps) rounds, randomized rounding, and a (1 + eps) ln Delta ratio for dominating set)
  - paper: doi:10.1007/978-3-642-15763-9_48
    title: Christoph Lenzen and Roger Wattenhofer, Minimum dominating set approximation in graphs of bounded arboricity, DISC 2010
    locator: pp. 510 to 524 (better ratios on sparse graph classes)
---

In the distributed dominating set problem, the nodes of a network must choose a set $D$ such that every node is in $D$ or has a neighbour in $D$, and $D$ should be close to the smallest possible. Finding the minimum is NP-hard and also needs global information, so distributed algorithms aim for a good approximation in few rounds. The best ratio is $O(\log \Delta)$, achieved by Jia, Rajaraman and Suel (2002) with a greedy-like method and by Kuhn, Moscibroda and Wattenhofer with LP rounding, and the [KMW lower bound](/kmw-lower-bound/) shows that any polylogarithmic ratio needs $\Omega(\log \Delta / \log \log \Delta)$ rounds.

Notation on this page: $G = (V, E)$ has $n$ nodes and maximum degree $\Delta$. $N[v]$ is the closed neighbourhood of $v$, that is $v$ and its neighbours, so $|N[v]| \le \Delta + 1$. $\mathrm{OPT}$ is the size of a minimum dominating set, and $\mathrm{OPT}_{\mathrm{LP}}$ the optimum of the LP relaxation below. The model is [LOCAL](/local-model/) unless stated; most algorithms here also run in [CONGEST](/congest-model/).

## In plain words

A company wants to place help desks in some of its offices so that every office either has a desk or is next door to one. It wants as few desks as possible.

If each office only talks with its neighbours, nobody knows the best plan. A simple rule is that an office takes a desk when it can serve many offices that are not yet served, which is the classic greedy idea. Offices that serve about the same number act together, using random choices so that not too many of them take a desk at once.

Another way is to first agree on fractional desks, a number between 0 and 1 per office, which is easier to do locally. Then each office takes a real desk with a chance that grows with its fraction. Both ways use at most a logarithmic factor more desks than the best plan.

## Definition

**Input.** A graph $G$ in the LOCAL or CONGEST model, with unique identifiers.

**Output.** Each node outputs one bit; $D$ is the set of nodes with bit 1.

**Condition.** $D$ is a [dominating set](/dominating-set/): $D \cap N[v] \ne \emptyset$ for every $v$.

**Goal.** Make $|D|$ small. An algorithm has ratio $\alpha$ if $|D| \le \alpha \cdot \mathrm{OPT}$ always, or in expectation for randomized algorithms.

The LP relaxation and its dual are
$$\min \sum_{v} x_v \ \text{ s.t. } \sum_{u \in N[v]} x_u \ge 1 \ \forall v, \ x \ge 0; \qquad \max \sum_v y_v \ \text{ s.t. } \sum_{v \in N[u]} y_v \le 1 \ \forall u, \ y \ge 0.$$
Each constraint involves only one closed neighbourhood, so a node can check its own constraint after one round. Dominating set is the [set cover](/set-cover/) instance with ground set $V$ and the sets $N[v]$.

The condition is locally checkable, but the goal is not: a node cannot tell from its neighbourhood whether $|D|$ is within a factor $\alpha$ of the optimum. So this is an optimization problem, not a [locally checkable labeling](/locally-checkable-labeling/) problem.

## Variants

- **Weighted.** Each node has a cost, and the goal is the least total cost; the LP methods extend with the same ratio.
- **Connected dominating set.** $D$ must also induce a connected subgraph, as a backbone for routing. KMW show that a polylogarithmic ratio needs $\Omega(\log n / \log \log n)$ rounds, because connectivity is a global condition. A dominating set can be connected with at most three times as many nodes (see Reductions), but the connecting step needs non-local information.
- **$k$-fold and distance-$r$ domination.** Every node must be dominated $k$ times, or by a node within distance $r$; the second is domination in the power graph $G^r$.
- **Edge dominating set.** A set of edges that touches every edge; it is dominating set on the [line graph](/line-graph/), and within a factor 2 it is the same as vertex cover.
- **Restricted graph classes.** On planar graphs and graphs of bounded arboricity, constant or near-constant ratios are possible in few rounds (Lenzen and Wattenhofer, 2010, and later work).

## Examples

- **A star.** The centre alone dominates, so $\mathrm{OPT} = 1$. Every node can decide in one round: a node of largest degree in its neighbourhood joins. An [MIS](/distributed-mis/) is also a dominating set, but the MIS made of the $n - 1$ leaves has ratio $n - 1$; an MIS is a valid answer, not a good one.
- **A path.** A path of $n$ nodes has $\mathrm{OPT} = \lceil n / 3 \rceil$: take every third node. All nodes with degree 2 in the path look the same up to large distances, so a fast algorithm needs identifiers or randomness to pick a pattern, and with constant rounds it pays a constant factor.
- **Disjoint cliques.** On a union of cliques $K_{\Delta + 1}$, $\mathrm{OPT}$ is the number of cliques. If every node joins with probability $p$, a clique is left empty with probability $(1 - p)^{\Delta + 1}$; with $p = \ln(\Delta + 1) / (\Delta + 1)$ this is at most $1 / (\Delta + 1)$, and the expected size is about $\ln(\Delta + 1)$ per clique. This is the LP rounding below with $x_v = 1/(\Delta + 1)$.

## Known algorithms

**LP rounding.** Given a feasible fractional solution $x$, every node $v$ joins with probability $\min(1, x_v \ln(\Delta + 1))$, independently; then every node that is not dominated joins. This takes two rounds after the LP.

*Claim.* $\mathbb{E}|D| \le (\ln(\Delta + 1) + 1) \sum_v x_v$.

*Proof.* The first step adds at most $\ln(\Delta + 1) \sum_v x_v$ nodes in expectation. A node $v$ stays undominated with probability at most $\prod_{u \in N[v]} (1 - x_u \ln(\Delta + 1)) \le \exp(-\ln(\Delta + 1) \sum_{u \in N[v]} x_u) \le \frac{1}{\Delta + 1}$, using $1 - z \le e^{-z}$ and the LP constraint; if some $x_u \ln(\Delta + 1) \ge 1$, then $u$ joins surely and the bound holds trivially. So the second step adds at most $n / (\Delta + 1)$ nodes in expectation. Summing the constraints over all $v$ gives $n \le \sum_v \sum_{u \in N[v]} x_u \le (\Delta + 1) \sum_u x_u$, so $n / (\Delta + 1) \le \sum_u x_u$. $\blacksquare$

With $x$ within $1 + \varepsilon$ of $\mathrm{OPT}_{\mathrm{LP}} \le \mathrm{OPT}$, the expected ratio is $(1 + \varepsilon)(\ln(\Delta + 1) + 1)$. KMW compute such an $x$ in $O(\log n / \varepsilon)$ rounds with a distributed algorithm for covering and packing LPs, and with a finer rounding they get ratio $(1 + \varepsilon) \ln \Delta$. This is the same rounding as for [set cover](/lp-rounding-set-cover/), and centrally a ratio much better than $\ln \Delta$ is NP-hard ([inapproximability](/dominating-set-inapproximability/)); in LOCAL, local computation is free, but the round bound still limits the ratio.

**Greedy in parallel (Jia, Rajaraman and Suel, 2002).** The sequential [greedy](/greedy-set-cover/) rule picks the node that dominates the most undominated nodes and has ratio $H(\Delta + 1) \le \ln(\Delta + 1) + 1$. JRS run it in parallel: each node computes its span, the number of undominated nodes in $N[v]$, rounded up to a power of 2; a node is a candidate if its rounded span is the largest within distance 2; each undominated node counts the candidates that cover it; and a candidate joins with probability inversely related to the median count over the nodes it covers. The expected ratio is $O(\log \Delta)$, and the rounded spans fall fast enough that $O(\log n \log \Delta)$ rounds suffice w.h.p. Messages are small, so it runs in CONGEST.

**Constant time (Kuhn and Wattenhofer, 2003).** For a parameter $k$, a fractional solution is built in $O(k^2)$ rounds by raising $x_v$ in stages, with thresholds on the number of undominated neighbours that fall by a factor $\Delta^{1/k}$ per stage, and it is then rounded as above. The expected ratio is $O(k \Delta^{2/k} \log \Delta)$. This was the first non-trivial ratio in a constant number of rounds, and $k = \Theta(\log \Delta)$ gives an $O(\log^2 \Delta)$ ratio in $O(\log^2 \Delta)$ rounds.

**Deterministic.** The randomized rounding can be derandomized with a [network decomposition](/network-decomposition/) and conditional expectations inside the clusters, which gives deterministic $\mathrm{poly}(\log n)$-round algorithms with ratio $O(\log \Delta)$.

| Algorithm | Ratio | Rounds | Randomized |
|---|---|---|---|
| Jia, Rajaraman and Suel (2002) | $O(\log \Delta)$ expected | $O(\log n \log \Delta)$ | yes |
| Kuhn and Wattenhofer (2003) | $O(k \Delta^{2/k} \log \Delta)$ expected | $O(k^2)$ | yes |
| KMW, LP plus rounding | $(1 + \varepsilon) \ln \Delta$ expected | $O(\log n / \varepsilon)$ | yes |
| Network decomposition plus derandomized rounding | $O(\log \Delta)$ | $\mathrm{poly}(\log n)$ | no |

## Bounds

- **KMW lower bound.** In $k$ rounds, every algorithm, randomized or not, has ratio at least $\Omega(\Delta^{1/(k+1)} / k)$ and $\Omega(n^{(1 - o(1))/(4k^2)} / k)$ on some graphs. So a constant or polylogarithmic ratio needs $\Omega(\log \Delta / \log \log \Delta)$ and $\Omega(\sqrt{\log n / \log \log n})$ rounds, even for the fractional problem. The proof reduces vertex cover to dominating set on the line graph; see the [KMW lower bound](/kmw-lower-bound/).
- **Upper bounds.** The $O(\log \Delta)$ ratio is reached in $O(\log n)$ rounds for constant $\varepsilon$. With $k = \Theta(\log \Delta / \log \log \Delta)$, the Kuhn and Wattenhofer bound gives a polylogarithmic ratio in $O(\log^2 \Delta / (\log \log \Delta)^2)$ rounds, which is about the square of the lower bound.
- **Central hardness.** In polynomial time, a ratio of $(1 - \varepsilon) \ln n$ is NP-hard; distributed algorithms with polynomial local computation inherit this limit, while the round lower bound holds even with unbounded local computation.

## Reductions

- **To set cover.** Dominating set is set cover with the sets $N[v]$, and set cover with element and set nodes reduces to dominating set in a bipartite network with $O(1)$ overhead per round, so the distributed algorithms for one carry over to the other.
- **From vertex cover, for lower bounds.** On the line graph, an edge dominating set gives a vertex cover at most twice as large, and back; a $k$-round algorithm on the line graph runs in $k$ rounds on $G$. This transfers the KMW bound from [vertex cover](/distributed-minimum-vertex-cover/) to dominating set.
- **From MIS, as a feasibility tool.** Any MIS is a dominating set, so an MIS algorithm gives a valid answer with no ratio guarantee; on graphs where every node has degree at most $\Delta$, it has ratio at most $\Delta$.
- **To connected dominating set.** A dominating set $D$ can be connected by adding at most two nodes per edge of a spanning tree on the clusters of $D$, giving at most $3|D|$ nodes.

## Applications

- **Clustering and backbones in wireless networks.** The dominating nodes act as cluster heads, and a connected dominating set serves as a routing backbone.
- **Facility placement.** Servers, caches or sensors placed so that every node is near one.
- **A test case for local approximation.** Dominating set is the main covering problem of the KMW study, and its fractional version shows that even LPs need many rounds to solve locally.

## References
