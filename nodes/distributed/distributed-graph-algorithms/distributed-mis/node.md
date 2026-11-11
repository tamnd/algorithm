---
tag: CESMCY
kind: problem
slug: distributed-mis
name: Distributed maximal independent set
aliases:
- distributed MIS
- maximal independent set in distributed networks
area: distributed/distributed-graph-algorithms
level: advanced
summary: Find a maximal independent set when each node talks only with its neighbours. Luby takes O(log n) rounds; Ghaffari takes O(log Delta) plus a small term; KMW gives a lower bound.
prereqs: [local-model, maximal-independent-set, luby-mis, round-complexity]
see_also: [kmw-lower-bound, distributed-vertex-coloring, distributed-maximal-matching, ruling-set, network-decomposition, ring-coloring, israeli-itai, jones-plassmann]
sources:
  - paper: doi:10.1137/0215074
    title: Michael Luby, A simple parallel algorithm for the maximal independent set problem, SIAM Journal on Computing 15(4), 1986
    locator: pp. 1036 to 1053 (the randomized algorithm with O(log n) rounds, and the reduction from (Delta+1)-colouring to MIS)
  - paper: doi:10.1016/0196-6774(86)90019-2
    title: Noga Alon, László Babai and Alon Itai, A fast and simple randomized parallel algorithm for the maximal independent set problem, Journal of Algorithms 7(4), 1986
    locator: pp. 567 to 583 (the same O(log n) bound, found independently)
  - paper: doi:10.1137/1.9781611974331.ch20
    title: Mohsen Ghaffari, An improved distributed algorithm for maximal independent set, SODA 2016
    locator: pp. 270 to 277 (O(log Delta) + 2^O(sqrt(log log n)) rounds, and the local guarantee O(log Delta + log 1/epsilon))
  - paper: doi:10.1145/2742012
    title: Fabian Kuhn, Thomas Moscibroda and Roger Wattenhofer, Local computation, lower and upper bounds, Journal of the ACM 63(2), 2016
    locator: Article 17 (the lower bound Omega(min(log Delta / log log Delta, sqrt(log n / log log n))) for MIS)
  - paper: doi:10.1145/3461458
    title: Alkida Balliu, Sebastian Brandt, Juho Hirvonen, Dennis Olivetti, Mikaël Rabie and Jukka Suomela, Lower bounds for maximal matchings and maximal independent sets, Journal of the ACM 68(5), 2021
    locator: Article 39 (Omega(min(Delta, log n / log log n)) deterministic and Omega(min(Delta, log log n / log log log n)) randomized; FOCS 2019 version pp. 481 to 497)
  - paper: doi:10.1145/3357713.3384298
    title: Václav Rozhoň and Mohsen Ghaffari, Polylogarithmic-time deterministic network decomposition and distributed derandomization, STOC 2020
    locator: pp. 350 to 363 (the first deterministic poly(log n) MIS)
  - paper: doi:10.1145/3564246.3585243
    title: Mohsen Ghaffari and Christoph Grunau, Faster deterministic distributed MIS and approximate matching, STOC 2023
    locator: pp. 1777 to 1790 (deterministic MIS in O~(log^2 n) rounds)
  - paper: doi:10.1109/FOCS61266.2024.00007
    title: Mohsen Ghaffari and Christoph Grunau, Near-optimal deterministic network decomposition and ruling set, and improved MIS, FOCS 2024
    locator: pp. 2148 to 2179 (deterministic MIS in O~(log^(5/3) n) rounds)
  - paper: doi:10.1145/2903137
    title: Leonid Barenboim, Michael Elkin, Seth Pettie and Johannes Schneider, The locality of distributed symmetry breaking, Journal of the ACM 63(3), 2016
    locator: the randomized MIS in O(log^2 Delta) + 2^O(sqrt(log log n)) rounds by shattering
  - paper: doi:10.1006/jagm.1996.0017
    title: Alessandro Panconesi and Aravind Srinivasan, On the complexity of distributed network decomposition, Journal of Algorithms 20(2), 1996
    locator: pp. 356 to 374 (deterministic MIS in 2^O(sqrt(log n)) rounds)
---

The distributed maximal independent set (MIS) problem asks the nodes of a network to choose a set of nodes with no two adjacent, such that every node outside the set has a neighbour in it, when each node can only exchange messages with its neighbours in synchronous rounds. It is the same [problem as in the parallel setting](/maximal-independent-set/), but the cost is the number of rounds in the [LOCAL](/local-model/) or [CONGEST](/congest-model/) model, not work and span. [Luby's algorithm](/luby-mis/) takes $O(\log n)$ rounds with high probability, Ghaffari (2016) takes $O(\log \Delta) + 2^{O(\sqrt{\log \log n})}$, and the [KMW lower bound](/kmw-lower-bound/) shows that $\Omega(\min(\log \Delta / \log \log \Delta, \sqrt{\log n / \log \log n}))$ rounds are needed. Deterministic algorithms now take $\tilde{O}(\log^{5/3} n)$ rounds.

Notation on this page: $G = (V, E)$ has $n$ nodes and maximum degree $\Delta$; $N(v)$ is the set of neighbours of $v$. Nodes have distinct $O(\log n)$-bit identifiers and know $n$ and $\Delta$ up to polynomial factors. "With high probability" (w.h.p.) means with probability at least $1 - n^{-c}$ for a constant $c$ that can be chosen. $\tilde{O}$ hides factors polynomial in $\log \log n$.

## In plain words

People stand in a crowd, and some pairs are rivals. We want a team in which no two members are rivals, and in which every person left out has a rival in the team, so that nobody else can join. Each person can only talk to their rivals, in rounds.

The difficulty is that rivals look alike, so someone must step back. Random numbers break the tie: each person draws a number, and the people with the smallest number among their rivals join. Their rivals leave, and the rest try again. About half of the rival pairs disappear in each round, so few rounds are needed.

Without random numbers, the crowd must use the names of the people to break ties, which is slower. There is also a limit: in some crowds, every method needs a certain number of rounds, because nobody can see far enough to decide.

## Definition

**Input.** A graph $G$ as a network. Each node knows its identifier and its neighbours.

**Output.** A bit $x_v \in \{0, 1\}$ at every node, such that $I = \{v : x_v = 1\}$ is independent (no edge of $G$ has both ends in $I$) and maximal (every $v \notin I$ has a neighbour in $I$).

**Cost.** The number of rounds until all nodes have fixed their bits, in the worst case for deterministic algorithms and w.h.p. for randomized ones. MIS is a locally checkable problem: each node can check its part of the condition by looking at its neighbours; see [locally checkable labeling](/locally-checkable-labeling/).

## Variants

- **Ruling sets.** An $(\alpha, \beta)$-[ruling set](/ruling-set/) asks for nodes at distance at least $\alpha$ from each other, with every node within distance $\beta$ of the set. An MIS is a $(2, 1)$-ruling set. Relaxing $\beta$ makes the problem easier: deterministic $(2, O(\log n))$-ruling sets take $O(\log n)$ rounds.
- **Maximal matching.** A [maximal matching](/distributed-maximal-matching/) is an MIS of the [line graph](/line-graph/). One round on the line graph costs $O(1)$ rounds on $G$ in LOCAL, so every MIS algorithm gives a matching algorithm, with $\Delta$ replaced by $2\Delta - 2$.
- **Maximum independent set.** The largest independent set is a different, NP-hard problem; see [maximum independent set](/maximum-independent-set/). An MIS can be far smaller than the maximum: in a star, the centre alone is an MIS.
- **CONGEST.** Luby's algorithm sends $O(\log n)$-bit priorities, so it runs in CONGEST with the same round count. Some fast algorithms gather whole neighbourhoods and need LOCAL.

## Examples

**A ring of $n$ nodes.** With a 3-colouring from [Cole-Vishkin](/cole-vishkin/), three more rounds give an MIS, so an MIS of an oriented ring takes $O(\log^* n)$ rounds. By [Linial's lower bound](/linial-coloring-lower-bound/), $\Omega(\log^* n)$ rounds are needed, because an MIS of a ring gives a 3-colouring in one round.

**A complete graph $K_n$.** Exactly one node is in any MIS. One round suffices: the node with the smallest identifier joins.

**A star with centre $c$ and leaves $\ell_1, \dots, \ell_k$.** The two MISs are $\{c\}$ and $\{\ell_1, \dots, \ell_k\}$. In one phase of Luby's algorithm, the centre joins if its priority is the smallest of all $k + 1$, which has probability $1/(k + 1)$; otherwise every leaf with a smaller priority than the centre joins, the centre leaves, and the remaining leaves join in the next phase.

**A non-example.** The set of nodes whose identifier is smaller than all neighbours' identifiers is independent but not always maximal: on the path $3 - 1 - 2 - 4$, only node 1 qualifies, and node 4 has no neighbour in the set.

## Known algorithms

**Luby's algorithm in rounds.** The algorithm is on the page [Luby's algorithm](/luby-mis/), with its proof that the number of live edges halves in expectation in each phase. As a distributed algorithm, a phase is two rounds: every live node sends a fresh random priority to its neighbours, then every node whose priority is smaller than all live neighbours' priorities joins and tells its neighbours, which leave. So the round count is twice the number of phases, $O(\log n)$ w.h.p., and the messages have $O(\log n)$ bits. The parallel page counts $O(\log^2 n)$ span, because a parallel machine must also pack the live vertices and edges in each phase; in the LOCAL model there is no such cost, since each node keeps its own state.

**MIS from a colouring.** A proper colouring with $k$ colours gives an MIS in $k$ rounds. In round $x$, every node of colour $x$ that has no neighbour in the set joins. Nodes of one colour are not adjacent, so they can decide together. The set stays independent, because a node joins only when no neighbour is in it, and no two nodes join next to each other in the same round. It is maximal, because each node $v$ has a turn: if $v$ does not join, it has a neighbour in the set. With [Linial's algorithm](/linial-algorithm/) this gives a deterministic MIS in $O(\Delta^2) + \log^* n$ rounds, and with the $(\Delta + 1)$-colouring of Barenboim, Elkin and Kuhn in $O(\Delta) + \log^* n$ rounds.

**MIS from a network decomposition.** A [network decomposition](/network-decomposition/) with $C$ cluster colours and cluster diameter $D$ gives an MIS in $O(C \cdot D)$ rounds: process the colours in turn, and let each cluster of the current colour gather its topology and the current set, and choose a maximal set of its free nodes. Clusters of one colour are not adjacent, so their choices do not conflict. This is the route to all deterministic poly-logarithmic algorithms.

**Ghaffari's algorithm.** Each node $v$ keeps a desire level $p_t(v)$, which starts at $\frac{1}{2}$. Let $d_t(v) = \sum_{u \in N(v)} p_t(u)$ be its effective degree. In each round, $v$ marks itself with probability $p_t(v)$ and joins if it is marked and no neighbour is marked. Then $p_{t+1}(v) = p_t(v)/2$ if $d_t(v) \ge 2$, and $p_{t+1}(v) = \min(2 p_t(v), \frac{1}{2})$ otherwise. Ghaffari shows a local guarantee: for each node $v$ and each $\varepsilon > 0$, after $O(\log \Delta + \log(1/\varepsilon))$ rounds, $v$ or a neighbour of $v$ is in the set with probability at least $1 - \varepsilon$, whatever the random choices far from $v$. With $\varepsilon = \Delta^{-c}$, after $O(\log \Delta)$ rounds the remaining nodes form components of $\mathrm{poly}(\Delta) \log n$ nodes w.h.p., and a deterministic algorithm finishes them. This step is called shattering.

| Result | Type | Rounds |
|---|---|---|
| Luby (1986); Alon, Babai and Itai (1986) | randomized | $O(\log n)$ w.h.p. |
| Barenboim, Elkin, Pettie and Schneider (2012, 2016) | randomized | $O(\log^2 \Delta) + 2^{O(\sqrt{\log \log n})}$ w.h.p. |
| Ghaffari (2016) | randomized | $O(\log \Delta) + 2^{O(\sqrt{\log \log n})}$ w.h.p. |
| Ghaffari (2016) with a deterministic poly-logarithmic finish | randomized | $O(\log \Delta) + \mathrm{poly}(\log \log n)$ w.h.p. |
| Linial colouring, then colour classes | deterministic | $O(\Delta^2) + \log^* n$ |
| Barenboim, Elkin and Kuhn colouring, then colour classes | deterministic | $O(\Delta) + \log^* n$ |
| Panconesi and Srinivasan (1996), by network decomposition | deterministic | $2^{O(\sqrt{\log n})}$ |
| Rozhoň and Ghaffari (2020), by network decomposition | deterministic | $\mathrm{poly}(\log n)$ |
| Ghaffari and Grunau (2023) | deterministic | $\tilde{O}(\log^2 n)$ |
| Ghaffari and Grunau (2024) | deterministic | $\tilde{O}(\log^{5/3} n)$ |

## Bounds

- **$\Omega(\log^* n)$** on rings, deterministic and randomized, from [ring colouring](/ring-coloring/): an MIS of a ring gives a 3-colouring in one round.
- **The KMW bound.** Every randomized algorithm needs $\Omega(\min(\log \Delta / \log \log \Delta, \sqrt{\log n / \log \log n}))$ rounds. The hard graphs have high girth, so the bound holds on graphs that look like trees locally. See [KMW lower bound](/kmw-lower-bound/).
- **Balliu et al. (2019, 2021).** Every deterministic algorithm needs $\Omega(\min(\Delta, \log n / \log \log n))$ rounds, and every randomized one $\Omega(\min(\Delta, \log \log n / \log \log \log n))$. So the $O(\Delta) + \log^* n$ algorithm is optimal as a function of $\Delta$ when $\Delta$ is small compared with $\log n / \log \log n$ (deterministic) or $\log \log n / \log \log \log n$ (randomized). The proof uses [round elimination](/round-elimination/).
- **Gaps.** For randomized algorithms, the dependence on $\Delta$ is $O(\log \Delta)$ against $\Omega(\log \Delta / \log \log \Delta)$, which is tight up to the $\log \log \Delta$ factor. The dependence on $n$ is $\mathrm{poly}(\log \log n)$ against $\Omega(\log \log n / \log \log \log n)$, and for deterministic algorithms $\tilde{O}(\log^{5/3} n)$ against $\Omega(\log n / \log \log n)$.

## Reductions

- **Colouring to MIS** in $k$ rounds, for a $k$-colouring (above).
- **MIS to $(\Delta + 1)$-colouring.** An MIS of $G \times K_{\Delta + 1}$ gives a $(\Delta + 1)$-colouring of $G$; each node simulates its $\Delta + 1$ copies. The proof is on the page [distributed vertex colouring](/distributed-vertex-coloring/).
- **MIS to maximal matching.** An MIS of the line graph is a maximal matching, so lower bounds for maximal matching are lower bounds for MIS, and upper bounds for MIS carry to matching.
- **Derandomization.** Ghaffari, Kuhn and Maus (2017) and Ghaffari, Harris and Kuhn (2018) show that a deterministic poly-logarithmic network decomposition gives a deterministic poly-logarithmic algorithm for every locally checkable problem that has a poly-logarithmic randomized algorithm. The Rozhoň-Ghaffari decomposition supplied this, and deterministic MIS in $\mathrm{poly}(\log n)$ rounds followed.

## Applications

- **Clustering.** The nodes of an MIS are cluster centres, and every other node joins a neighbouring centre, which gives clusters of radius 1.
- **Symmetry breaking in larger algorithms.** MIS is a step in colouring, matching, [network decomposition](/network-decomposition/) and [sinkless orientation](/sinkless-orientation/) algorithms, often on a power graph $G^k$, where it gives a ruling set of $G$.
- **Backbones in wireless networks.** An MIS is a dominating set of a special kind, and connecting its nodes gives a small connected dominating set for routing; see [distributed dominating set](/distributed-dominating-set/).

## References
