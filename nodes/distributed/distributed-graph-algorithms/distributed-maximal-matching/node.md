---
tag: YK5M1K
kind: problem
slug: distributed-maximal-matching
name: Distributed maximal matching
aliases:
- distributed matching
area: distributed/distributed-graph-algorithms
level: advanced
summary: Find a maximal matching when each node talks only with its neighbours. Randomized O(log n) rounds; deterministic O(log^2 Delta log n); Omega(min(Delta, log n / log log n)) deterministic.
prereqs: [local-model, maximal-matching, distributed-mis, line-graph]
see_also: [israeli-itai, luby-mis, distributed-weighted-matching, distributed-minimum-vertex-cover, kmw-lower-bound, distributed-edge-coloring, ring-coloring, round-elimination]
sources:
  - paper: doi:10.1016/0020-0190(86)90144-4
    title: Amos Israeli and Alon Itai, A fast and simple randomized parallel algorithm for maximal matching, Information Processing Letters 22(2), 1986
    locator: pp. 77 to 80 (randomized maximal matching in O(log n) rounds)
  - paper: doi:10.1137/0215074
    title: Michael Luby, A simple parallel algorithm for the maximal independent set problem, SIAM Journal on Computing 15(4), 1986
    locator: pp. 1036 to 1053 (maximal matching as an MIS of the line graph)
  - paper: doi:10.1007/PL00008932
    title: Alessandro Panconesi and Romeo Rizzi, Some simple distributed algorithms for sparse networks, Distributed Computing 14(2), 2001
    locator: pp. 97 to 100 (deterministic maximal matching in O(Delta + log* n) rounds)
  - paper: doi:10.1137/S0895480100373121
    title: Michał Hańćkowiak, Michał Karoński and Alessandro Panconesi, On the distributed complexity of computing maximal matchings, SIAM Journal on Discrete Mathematics 15(1), 2001
    locator: pp. 41 to 57 (the first deterministic poly(log n) algorithm, O(log^4 n) rounds)
  - paper: doi:10.1007/s00446-018-0344-4
    title: Manuela Fischer, Improved deterministic distributed matching via rounding, Distributed Computing 33(3-4), 2020
    locator: pp. 279 to 291 (deterministic maximal matching in O(log^2 Delta log n) rounds by rounding a fractional matching)
  - paper: doi:10.1145/2903137
    title: Leonid Barenboim, Michael Elkin, Seth Pettie and Johannes Schneider, The locality of distributed symmetry breaking, Journal of the ACM 63(3), 2016
    locator: the randomized maximal matching in O(log Delta) rounds plus a poly(log log n) term, by shattering
  - paper: doi:10.1145/3461458
    title: Alkida Balliu, Sebastian Brandt, Juho Hirvonen, Dennis Olivetti, Mikaël Rabie and Jukka Suomela, Lower bounds for maximal matchings and maximal independent sets, Journal of the ACM 68(5), 2021
    locator: Article 39 (Omega(min(Delta, log n / log log n)) deterministic and Omega(min(Delta, log log n / log log log n)) randomized; FOCS 2019 version pp. 481 to 497)
  - paper: doi:10.1145/2742012
    title: Fabian Kuhn, Thomas Moscibroda and Roger Wattenhofer, Local computation, lower and upper bounds, Journal of the ACM 63(2), 2016
    locator: Article 17 (the lower bound Omega(min(log Delta / log log Delta, sqrt(log n / log log n))) for maximal matching)
  - paper: doi:10.1145/3564246.3585243
    title: Mohsen Ghaffari and Christoph Grunau, Faster deterministic distributed MIS and approximate matching, STOC 2023
    locator: pp. 1777 to 1790 (deterministic O~(log^2 n) for MIS, which carries to maximal matching)
---

The distributed maximal matching problem asks the nodes of a network to choose a set of edges with no two sharing an end, such that every edge of the graph shares an end with a chosen edge, when nodes exchange messages with their neighbours in synchronous rounds. A [maximal matching](/maximal-matching/) is an MIS of the [line graph](/line-graph/), so the problem sits next to [distributed MIS](/distributed-mis/), and the cost is the number of rounds in the [LOCAL](/local-model/) or [CONGEST](/congest-model/) model. Randomized algorithms take $O(\log n)$ rounds ([Israeli-Itai](/israeli-itai/)), deterministic ones $O(\log^2 \Delta \cdot \log n)$ rounds (Fischer) or $O(\Delta + \log^* n)$ rounds (Panconesi and Rizzi), and Balliu et al. (2019) show that $O(\Delta + \log^* n)$ is optimal when $\Delta$ is small.

Notation on this page: $G = (V, E)$ has $n$ nodes, $m$ edges and maximum degree $\Delta$. Nodes have distinct $O(\log n)$-bit identifiers. "With high probability" (w.h.p.) means with probability at least $1 - n^{-c}$ for a constant $c$ that can be chosen. $\tilde{O}$ hides factors polynomial in $\log \log n$.

## In plain words

Dancers at a party want to form couples. Some pairs of people know each other, and only such pairs can dance. The rule is that nobody dances with two partners, and when the music starts, no two people who know each other may both be sitting out. Each person can only talk to the people they know, in rounds.

The trouble is the same as in any problem of breaking ties: two people may both want the same partner. Random choices settle most conflicts quickly, and a constant share of the possible couples is decided in each round, so few rounds are needed.

Without random choices it is harder. If each person knows only a few others, people can go through their friends one by one. If each person knows many others, cleverer methods are needed, and some number of rounds cannot be avoided.

## Definition

**Input.** A graph $G$ as a network. Each node knows its identifier and its incident edges.

**Output.** At every node $v$, either a neighbour $\mathrm{mate}(v)$ or "unmatched", such that $\mathrm{mate}(\mathrm{mate}(v)) = v$ for every matched $v$, and no edge has two unmatched ends.

**Cost.** The number of rounds until all nodes have fixed their outputs, in the worst case for deterministic algorithms and w.h.p. for randomized ones. Each node can check its part of the output by looking at its neighbours, so maximal matching is a [locally checkable labeling](/locally-checkable-labeling/) problem.

## Variants

- **Approximate maximum matching.** A maximal matching is a 2-approximation of a [maximum matching](/maximum-matching/). Better ratios $1 + \varepsilon$ need different methods, based on augmenting paths of bounded length.
- **Weighted matching.** With edge weights, the target is an approximation of the [maximum weight matching](/maximum-weight-matching/); see [distributed weighted matching](/distributed-weighted-matching/).
- **$b$-matching and hypergraph matching.** Each node may have up to $b(v)$ partners, or the edges are hyperedges. Fischer, Ghaffari and Kuhn (2017) use deterministic hypergraph maximal matching to get deterministic edge colouring.
- **Bipartite graphs.** With the sides known, proposal schemes in which one side proposes and the other side accepts are simpler; the deterministic algorithm of Hańćkowiak, Karoński and Panconesi starts from this case.

## Examples

**A directed cycle.** A maximal matching gives a 3-colouring in one round: the tail of a matched edge takes colour 1, its head colour 2, and an unmatched node colour 3. An unmatched node has two matched neighbours, so it conflicts with nobody. So [Linial's bound](/linial-coloring-lower-bound/) gives $\Omega(\log^* n)$ rounds, and a 3-colouring plus three rounds gives a maximal matching, so the cycle takes $\Theta(\log^* n)$ rounds.

**A star with $k$ leaves.** Every maximal matching has exactly one edge. In one phase of the line-graph algorithm below, the edge with the least priority is the least at the centre and at its leaf, so it joins, and the phase ends the algorithm.

**A non-example.** On the path $a - b - c - d$, the set $\{\{b, c\}\}$ is a maximal matching, but $\{\{a, b\}\}$ alone is not, because the edge $\{c, d\}$ has two unmatched ends.

## Known algorithms

**Israeli-Itai.** Each node proposes to a random neighbour, each node keeps one proposal, the kept edges form paths and cycles, and a random choice on them picks a matching. A constant fraction of the edges leaves in each round in expectation, so the number of rounds is $O(\log n)$ w.h.p. The algorithm and its proof are on the page [Israeli-Itai](/israeli-itai/). In the parallel setting it costs $O(\log^2 n)$ span, because each round also packs the remaining graph; in the LOCAL model each node keeps its own state, and the cost is $O(\log n)$ rounds with $O(\log n)$-bit messages, so it runs in CONGEST.

**Luby on the line graph.** [Luby's algorithm](/luby-mis/) on the line graph, simulated on $G$, takes three rounds per phase. In round 1, the end with the smaller identifier of each live edge draws a fresh random priority and sends it to the other end. In round 2, every node sends the least priority of its live edges to its neighbours. An edge joins when its priority is the least at both ends; both ends know this after round 2. In round 3, matched nodes tell their neighbours, and all edges at matched nodes leave. Two edges that share an end $v$ cannot both join, since only one of them has the least priority at $v$. The phases are exactly the phases of Luby's algorithm on the line graph, which has $m \le n^2$ nodes, so $O(\log n)$ phases suffice w.h.p.

**Panconesi and Rizzi, $O(\Delta + \log^* n)$.** Each node gives its edges towards neighbours with larger identifiers distinct labels in $\{1, \dots, \Delta\}$. The edges with label $i$ form a rooted forest $F_i$: each node has at most one parent in $F_i$, and identifiers grow towards the roots. All forests are 3-coloured at the same time by [Cole-Vishkin](/cole-vishkin/) in $O(\log^* n)$ rounds. Then the forests are processed one at a time. In $F_i$, for each colour in turn, every free node of that colour proposes to its parent if the parent is free, and every free parent accepts one proposal. If an edge of $F_i$ had two free ends at the end, the child would have proposed at its colour's turn, and the parent, free at that time, would have accepted a proposal. So each forest takes $O(1)$ rounds, and the total is $O(\Delta + \log^* n)$.

**Deterministic poly-logarithmic algorithms.** Hańćkowiak, Karoński and Panconesi (2001) gave the first deterministic algorithm with $\mathrm{poly}(\log n)$ rounds, $O(\log^4 n)$. Fischer (2020) rounds a fractional matching to an integral one deterministically and gets $O(\log^2 \Delta \cdot \log n)$ rounds.

| Result | Type | Rounds |
|---|---|---|
| Israeli and Itai (1986); Luby (1986) on the line graph | randomized | $O(\log n)$ w.h.p. |
| Barenboim, Elkin, Pettie and Schneider (2012, 2016) | randomized | $O(\log \Delta) + \mathrm{poly}(\log \log n)$ w.h.p. |
| Panconesi and Rizzi (2001) | deterministic | $O(\Delta + \log^* n)$ |
| Hańćkowiak, Karoński and Panconesi (2001) | deterministic | $O(\log^4 n)$ |
| Fischer (2017, 2020) | deterministic | $O(\log^2 \Delta \cdot \log n)$ |
| Ghaffari and Grunau (2023), MIS on the line graph | deterministic | $\tilde{O}(\log^2 n)$ |

## Bounds

- **$\Omega(\log^* n)$** on cycles, from the 3-colouring above.
- **KMW.** Every randomized algorithm needs $\Omega(\min(\log \Delta / \log \log \Delta, \sqrt{\log n / \log \log n}))$ rounds; see [KMW lower bound](/kmw-lower-bound/). The bound holds even for constant-factor approximations of a maximum matching.
- **Balliu, Brandt, Hirvonen, Olivetti, Rabie and Suomela (2019).** Every deterministic algorithm needs $\Omega(\min(\Delta, \log n / \log \log n))$ rounds, and every randomized one $\Omega(\min(\Delta, \log \log n / \log \log \log n))$. The proof is by [round elimination](/round-elimination/) on regular trees, through a family of relaxed matching problems. So $O(\Delta + \log^* n)$ is optimal for $\Delta$ up to about $\log n / \log \log n$ (deterministic) or $\log \log n / \log \log \log n$ (randomized). The same bounds hold for MIS.
- **Gaps.** For large $\Delta$, the deterministic upper bound $O(\log^2 \Delta \cdot \log n)$ and the lower bound $\Omega(\log n / \log \log n)$ differ by about $\log^2 \Delta$.

## Reductions

- **To MIS.** A maximal matching of $G$ is an MIS of the line graph $L(G)$, and one round on $L(G)$ costs $O(1)$ rounds on $G$ in LOCAL. The maximum degree of $L(G)$ is at most $2\Delta - 2$, and $L(G)$ has at most $n^2$ nodes, so every MIS bound in $n$ and $\Delta$ carries over.
- **From edge colouring.** A proper edge colouring with $k$ colours gives a maximal matching in $k$ rounds: in round $x$, an edge of colour $x$ joins if both ends are free. So a $(2\Delta - 1)$-[edge colouring](/distributed-edge-coloring/) gives a maximal matching in $2\Delta - 1$ more rounds.
- **To vertex cover.** The $2|M|$ ends of a maximal matching $M$ form a vertex cover, at most twice the minimum, because any cover holds an end of each edge of $M$, and these edges share no ends. See [distributed minimum vertex cover](/distributed-minimum-vertex-cover/).
- **To approximate maximum matching.** Every edge of a maximum matching $M^*$ has an end matched by a maximal matching $M$, and each edge of $M$ has two ends, so $|M^*| \le 2|M|$.

## Applications

- **2-approximate vertex cover** in the same number of rounds, as above.
- **Building blocks.** Repeated maximal matchings give edge colourings, and maximal matchings in layered graphs give $(1 + \varepsilon)$-approximate matchings through short augmenting paths.
- **Pairing processes.** Load balancing, where nodes pair up to exchange load, and switch scheduling, where inputs and outputs of a switch pair up in each time slot.

## References
