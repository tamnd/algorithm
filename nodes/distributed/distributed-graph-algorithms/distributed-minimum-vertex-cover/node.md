---
tag: 511N17
kind: problem
slug: distributed-minimum-vertex-cover
name: Distributed minimum vertex cover
aliases:
- distributed vertex cover approximation
area: distributed/distributed-graph-algorithms
level: advanced
summary: Approximate a minimum vertex cover by local communication. A maximal matching gives factor 2; primal-dual gives 2 + eps in O(log Delta / log log Delta) rounds, which KMW shows is tight.
prereqs: [local-model, vertex-cover, distributed-maximal-matching, dual-linear-program]
see_also: [vertex-cover-2-approximation, primal-dual-weighted-vertex-cover, bar-yehuda-even-vertex-cover, kmw-lower-bound, distributed-dominating-set, distributed-weighted-matching, fractional-matching, weighted-vertex-cover]
sources:
  - paper: doi:10.1145/3060294
    title: Reuven Bar-Yehuda, Keren Censor-Hillel and Gregory Schwartzman, A distributed (2 + epsilon)-approximation for vertex cover in O(log Delta / epsilon log log Delta) rounds, Journal of the ACM 64(3), 2017
    locator: Article 23 (the deterministic primal-dual algorithm for weighted vertex cover; PODC 2016 version pp. 3 to 8)
  - paper: doi:10.1145/2742012
    title: Fabian Kuhn, Thomas Moscibroda and Roger Wattenhofer, Local computation, lower and upper bounds, Journal of the ACM 63(2), 2016
    locator: Article 17 (Omega(min(log Delta / log log Delta, sqrt(log n / log log n))) rounds for a constant-factor approximation)
  - paper: doi:10.1006/jagm.1994.1036
    title: Samir Khuller, Uzi Vishkin and Neal Young, A primal-dual parallel approximation technique applied to weighted set and vertex covers, Journal of Algorithms 17(2), 1994
    locator: pp. 280 to 289 (the parallel (2 + epsilon)-approximation for weighted vertex cover by edge packing)
  - paper: doi:10.1145/1435375.1435381
    title: Fabrizio Grandoni, Jochen Könemann and Alessandro Panconesi, Distributed weighted vertex cover via maximal matchings, ACM Transactions on Algorithms 5(1), 2008
    locator: Article 6 (a 2-approximation for weighted vertex cover by maximal matchings in an auxiliary graph)
  - paper: doi:10.1145/1810479.1810533
    title: Matti Åstrand and Jukka Suomela, Fast distributed approximation algorithms for vertex cover and set cover in anonymous networks, SPAA 2010
    locator: pp. 294 to 302 (a maximal edge packing, and so a 2-approximate weighted vertex cover, in O(Delta + log* W) rounds without identifiers)
  - paper: doi:10.1007/s00446-013-0194-z
    title: Mika Göös and Jukka Suomela, No sublogarithmic-time approximation scheme for bipartite vertex cover, Distributed Computing 27(6), 2014
    locator: pp. 435 to 443 (a (1 + delta)-approximation needs Omega(log n) rounds for some constant delta > 0)
  - paper: doi:10.1016/0020-0190(86)90144-4
    title: Amos Israeli and Alon Itai, A fast and simple randomized parallel algorithm for maximal matching, Information Processing Letters 22(2), 1986
    locator: pp. 77 to 80 (the maximal matching behind the unweighted 2-approximation)
---

The distributed minimum vertex cover problem asks the nodes of a network to choose a set of nodes that touches every edge and is as small, or as light, as possible, when nodes exchange messages with their neighbours in synchronous rounds. Finding a minimum [vertex cover](/vertex-cover/) is NP-hard, and in the [LOCAL model](/local-model/) the obstacle is locality, not computation, so the goal is an approximation in few rounds. The ends of a [maximal matching](/distributed-maximal-matching/) give a 2-approximation, and the primal-dual algorithm of Bar-Yehuda, Censor-Hillel and Schwartzman gives a $(2 + \varepsilon)$-approximation of the weighted problem in $O(\log \Delta / (\varepsilon \log \log \Delta))$ rounds, which the [KMW lower bound](/kmw-lower-bound/) shows is optimal in $\Delta$ for constant $\varepsilon$.

Notation on this page: $G = (V, E)$ has $n$ nodes, maximum degree $\Delta$, and node weights $w(v) > 0$ (all 1 in the unweighted case). $E(v)$ is the set of edges at $v$, and $\mathrm{OPT}$ is the weight of a minimum weight vertex cover. A vertex cover is a set $C \subseteq V$ with $u \in C$ or $v \in C$ for every edge $\{u, v\}$.

## In plain words

A city puts guards at street corners so that every street has a guard at one of its ends. Guards cost money, so the city wants few of them. Each corner can only talk with the corners next to it.

One quick rule is: pair up corners along streets until no street has two unpaired ends, and put a guard at both corners of every pair. Every street then has a guard. Any plan must put a guard at one end of every pair, so this rule uses at most twice the best number.

When corners have different costs, corners can share the cost of each street step by step, and a corner takes a guard when its streets have paid almost its cost. This gives nearly the same guarantee. A lower bound shows that no method with fewer rounds can be much better.

## Definition

**Input.** A graph $G$ as a network, and at each node its weight $w(v)$.

**Output.** A bit $x_v$ at every node, such that $C = \{v : x_v = 1\}$ is a vertex cover.

**Goal.** For a ratio $\alpha \ge 1$, an $\alpha$-approximation has $w(C) \le \alpha \cdot \mathrm{OPT}$ on every input. The cost is the number of rounds, as a function of $n$, $\Delta$ and $\alpha$.

## Variants

- **Unweighted and weighted.** The unweighted case has a 2-approximation from a maximal matching. Weights need a fractional argument, because a matching does not see them.
- **Port numbering.** Without identifiers, symmetric graphs prevent a maximal matching, but a 2-approximation still exists: Åstrand and Suomela (2010) give one for integer weights at most $W$ in $O(\Delta + \log^* W)$ rounds, through a maximal edge packing.
- **Approximation schemes.** With unbounded local computation, $(1 + \varepsilon)$-approximations take $\mathrm{poly}(\log n)/\varepsilon$ rounds by [network decomposition](/network-decomposition/); Göös and Suomela (2014) show that some constant $\delta > 0$ makes a $(1 + \delta)$-approximation need $\Omega(\log n)$ rounds, even on bipartite graphs.
- **Set cover.** Vertex cover is [set cover](/set-cover/) with sets of size 2 in the dual view, and the [dominating set](/distributed-dominating-set/) problem is a covering problem of the same type with a $\Theta(\log \Delta)$ ratio.

## Examples

**Disjoint edges.** On $k$ disjoint edges, the maximal matching takes all $k$ edges and the cover takes all $2k$ ends, while $\mathrm{OPT} = k$. So the ratio 2 of the matching method is reached.

**A star with $k$ leaves.** A maximal matching has one edge, so the cover is the centre and one leaf, with $\mathrm{OPT} = 1$. On this graph the edge packing of the next section does better: the centre gets the share $1/k$ from each edge, becomes saturated, and alone forms the cover.

**A non-example.** The set of nodes whose identifier is smaller than all neighbours' identifiers is not a vertex cover in general: on the path $1 - 2 - 3 - 4$ it is $\{1\}$, which misses the edge $\{2, 3\}$.

## Known algorithms

**The 2-approximation from a maximal matching.** Compute a maximal matching $M$ and output its $2|M|$ ends. Every edge has a matched end, otherwise $M$ would not be maximal, so the output is a cover. The edges of $M$ share no ends, so every cover holds a different node for each of them, and $\mathrm{OPT} \ge |M|$. So the cover has at most $2 \cdot \mathrm{OPT}$ nodes. The rounds are those of the matching: $O(\log n)$ w.h.p. with [Israeli-Itai](/israeli-itai/), and deterministic $O(\log^2 \Delta \cdot \log n)$ or $O(\Delta + \log^* n)$. In the centralized setting this is the [2-approximation for vertex cover](/vertex-cover-2-approximation/).

**Primal-dual by edge packing.** An edge packing assigns each edge $e$ a value $y_e \ge 0$ with $\sum_{e \in E(v)} y_e \le w(v)$ at every node. It is a feasible solution of the [dual](/dual-linear-program/) of the [LP relaxation](/lp-relaxation/) of vertex cover, so $\sum_e y_e \le \mathrm{OPT}$ by weak duality. Call $v$ saturated when $\sum_{e \in E(v)} y_e \ge (1 - \varepsilon) w(v)$.

*Claim.* If $y$ is an edge packing and the saturated nodes $C$ cover every edge, then $w(C) \le \frac{2}{1 - \varepsilon} \mathrm{OPT}$.

*Proof.* $w(C) \le \frac{1}{1 - \varepsilon} \sum_{v \in C} \sum_{e \in E(v)} y_e \le \frac{2}{1 - \varepsilon} \sum_e y_e \le \frac{2}{1 - \varepsilon} \mathrm{OPT}$. The second step holds because each edge has two ends and is counted at most twice. $\blacksquare$

So the task is to raise the $y_e$ in rounds until every edge has a saturated end, without breaking a node's capacity. In the simplest scheme each unsaturated node $v$ offers each of its live edges the share $r(v)/\deg'(v)$ of its remaining capacity $r(v)$, and each edge takes the smaller offer of its two ends; this is the parallel method of Khuller, Vishkin and Young, which needs $O(\log n \cdot \log(1/\varepsilon))$ rounds. Bar-Yehuda, Censor-Hillel and Schwartzman (2016, 2017) raise the values more boldly, by a factor that grows with $\log \Delta / \log \log \Delta$, and show that every node is saturated or loses all its live edges within $O(\log \Delta / (\varepsilon \log \log \Delta))$ rounds. Their algorithm is deterministic and works in CONGEST. The centralized relatives are [primal-dual weighted vertex cover](/primal-dual-weighted-vertex-cover/) and [Bar-Yehuda-Even](/bar-yehuda-even-vertex-cover/).

| Result | Ratio | Type | Rounds |
|---|---|---|---|
| Ends of a maximal matching (Israeli-Itai) | 2, unweighted | randomized | $O(\log n)$ w.h.p. |
| Ends of a maximal matching (Panconesi-Rizzi) | 2, unweighted | deterministic | $O(\Delta + \log^* n)$ |
| Khuller, Vishkin and Young (1994) | $2 + \varepsilon$, weighted | deterministic | $O(\log n \cdot \log(1/\varepsilon))$ |
| Grandoni, Könemann and Panconesi (2005, 2008) | 2, weighted | randomized | as maximal matching on an auxiliary graph |
| Åstrand and Suomela (2010) | 2, integer weights at most $W$ | deterministic, no identifiers | $O(\Delta + \log^* W)$ |
| Bar-Yehuda, Censor-Hillel and Schwartzman (2016, 2017) | $2 + \varepsilon$, weighted | deterministic | $O(\log \Delta / (\varepsilon \log \log \Delta))$ |

## Bounds

- **KMW lower bound.** Every algorithm, randomized or deterministic, with a constant approximation ratio needs $\Omega(\min(\log \Delta / \log \log \Delta, \sqrt{\log n / \log \log n}))$ rounds; see [KMW lower bound](/kmw-lower-bound/). For constant $\varepsilon$, the algorithm of Bar-Yehuda, Censor-Hillel and Schwartzman matches the $\log \Delta / \log \log \Delta$ term exactly.- **Below the ratio 2.** By Göös and Suomela, a $(1 + \delta)$-approximation for some constant $\delta > 0$ needs $\Omega(\log n)$ rounds, even on bipartite graphs, while a $(2 + \varepsilon)$-approximation needs no dependence on $n$ at all.
- **Computation is not the limit.** In LOCAL, nodes may compute anything, so the NP-hardness of vertex cover and the hardness of approximation below 2 for centralized algorithms do not apply; the lower bounds above come from what nodes cannot see.

## Reductions

- **From maximal matching.** As above, the ends of any maximal matching are a 2-approximate cover in no extra rounds.
- **To fractional matching.** The edge packing is a [fractional matching](/fractional-matching/) when all weights are 1, and the claim above shows that its value is within a factor $2/(1 - \varepsilon)$ of the cover, so the same algorithm approximates a maximum fractional matching.
- **Lower bound transfer.** The KMW construction is for fractional vertex cover and fractional matching; integral covers and matchings inherit the bound, and so does a maximal matching, whose ends would be a 2-approximate cover.

## Applications

- **Monitoring links.** In a sensor or router network, the nodes of a vertex cover can watch every link, and the cover is chosen locally.
- **Conflict resolution.** Removing a vertex cover leaves an independent set, so a cheap cover gives a large set of nodes that can act without conflicts.
- **A test case for local LP rounding.** Vertex cover is the simplest covering LP, and its primal-dual algorithms are the model for [distributed dominating set](/distributed-dominating-set/) and set cover algorithms.

## References
