---
tag: 5JYM67
kind: problem
slug: distributed-vertex-coloring
name: Distributed vertex coloring
aliases:
- distributed graph coloring
- distributed (Delta+1)-coloring
area: distributed/distributed-graph-algorithms
level: core
summary: Properly colour a network with Delta + 1 colours by local communication. Random trials take O(log n) rounds; deterministic algorithms take O~(log^2 n) rounds.
prereqs: [local-model, graph-coloring, delta-plus-one-bound, round-complexity]
see_also: [linial-algorithm, cole-vishkin, ring-coloring, linial-coloring-lower-bound, distributed-mis, distributed-edge-coloring, network-decomposition, jones-plassmann]
sources:
  - paper: doi:10.1137/0221015
    title: Nathan Linial, Locality in distributed graph algorithms, SIAM Journal on Computing 21(1), 1992
    locator: pp. 193 to 201 (O(Delta^2) colours in O(log* n) rounds, and the Omega(log* n) lower bound)
  - paper: doi:10.1016/S0020-0190(99)00064-2
    title: Öjvind Johansson, Simple distributed Delta+1-coloring of graphs, Information Processing Letters 70(5), 1999
    locator: pp. 229 to 232 (randomized colour trials, O(log n) rounds with high probability)
  - paper: doi:10.1137/12088848X
    title: Leonid Barenboim, Michael Elkin and Fabian Kuhn, Distributed (Delta+1)-coloring in linear (in Delta) time, SIAM Journal on Computing 43(1), 2014
    locator: pp. 72 to 95 (deterministic, O(Delta) + log* n rounds)
  - paper: doi:10.1109/FOCS52979.2021.00101
    title: Mohsen Ghaffari and Fabian Kuhn, Deterministic distributed vertex coloring, simpler, faster, and without network decomposition, FOCS 2021
    locator: pp. 1009 to 1020 (deterministic (degree+1)-list colouring in O(log^2 Delta log n) rounds in CONGEST)
  - paper: doi:10.1145/3357713.3384298
    title: Václav Rozhoň and Mohsen Ghaffari, Polylogarithmic-time deterministic network decomposition and distributed derandomization, STOC 2020
    locator: pp. 350 to 363 (the first deterministic polylog n algorithm for (Delta+1)-colouring and MIS)
  - paper: doi:10.1006/jagm.1996.0017
    title: Alessandro Panconesi and Aravind Srinivasan, On the complexity of distributed network decomposition, Journal of Algorithms 20(2), 1996
    locator: pp. 356 to 374 (deterministic 2^O(sqrt(log n)) rounds via network decomposition)
  - paper: doi:10.1145/2903137
    title: Leonid Barenboim, Michael Elkin, Seth Pettie and Johannes Schneider, The locality of distributed symmetry breaking, Journal of the ACM 63(3), 2016
    locator: the randomized O(log Delta) + 2^O(sqrt(log log n)) colouring and the shattering method (FOCS 2012 version, pp. 321 to 330)
  - paper: doi:10.1145/3178120
    title: David G. Harris, Johannes Schneider and Hsin-Hao Su, Distributed (Delta+1)-coloring in sublogarithmic rounds, Journal of the ACM 65(4), 2018
    locator: the randomized O(sqrt(log Delta)) + 2^O(sqrt(log log n)) algorithm (STOC 2016 version, pp. 465 to 478)
  - paper: doi:10.1137/19M1249527
    title: Yi-Jun Chang, Wenzheng Li and Seth Pettie, Distributed (Delta+1)-coloring via ultrafast graph shattering, SIAM Journal on Computing 49(3), 2020
    locator: pp. 497 to 539 (randomized colouring in the deterministic complexity of (degree+1)-list colouring on poly(log n) nodes)
  - paper: doi:10.1145/3564246.3585243
    title: Mohsen Ghaffari and Christoph Grunau, Faster deterministic distributed MIS and approximate matching, STOC 2023
    locator: pp. 1777 to 1790 (deterministic O~(log^2 n) for MIS and, by reductions, (Delta+1)-colouring; randomized colouring in O~(log^2 log n))
  - book: doi:10.1007/978-3-031-02009-4
    title: Leonid Barenboim and Michael Elkin, Distributed Graph Coloring, Fundamentals and Recent Developments, Morgan and Claypool, 2013
    locator: Chapter 3 (basic distributed colouring algorithms)
---

Distributed vertex colouring is the problem of [colouring](/graph-coloring/) the nodes of a network so that adjacent nodes get different colours, when each node is a processor that talks only with its neighbours in synchronous rounds. The standard target is $\Delta + 1$ colours, where $\Delta$ is the maximum degree: a [greedy argument](/delta-plus-one-bound/) shows they always suffice, and every partial colouring extends. The cost is the number of rounds in the [LOCAL](/local-model/) or [CONGEST](/congest-model/) model. Random colour trials take $O(\log n)$ rounds with high probability; deterministic algorithms take $O(\log^2 \Delta \cdot \log n)$ rounds (Ghaffari and Kuhn 2021), $\tilde{O}(\log^2 n)$ rounds (Ghaffari and Grunau 2023) or $O(\Delta) + \log^* n$ rounds (Barenboim, Elkin and Kuhn 2014), and $\Omega(\log^* n)$ rounds are needed.

Notation on this page: $G = (V, E)$ has $n$ nodes and maximum degree $\Delta$, and $N(v)$ and $\deg(v)$ are the neighbours and the degree of $v$. Nodes have distinct identifiers of $O(\log n)$ bits and know $n$ and $\Delta$ (or polynomial upper bounds on them). "With high probability" (w.h.p.) means with probability at least $1 - n^{-c}$ for a constant $c$ that can be chosen. $\tilde{O}$ hides factors polynomial in $\log \log n$.

## In plain words

Radio stations that are close to each other must use different channels, and there are only a few channels. No central office plans the channels: each station can only talk with its near neighbours, in rounds.

If a station has at most some number of neighbours, one channel more than that number is always enough, because the neighbours can block at most that many channels. The question is how many rounds of talk the stations need to agree.

A random method works well. In each round, every station without a channel flips a coin, and on heads it picks a random free channel and announces it. If no neighbour announced the same channel, it keeps it. Each station succeeds with a fair chance in every round, so after a number of rounds that grows with the logarithm of the network size, all stations are done. Methods without coins are slower.

## Definition

**Input.** A graph $G$, given as a network: each node knows its identifier and its neighbours, and nodes communicate in synchronous rounds.

**Output.** A colour $c(v) \in \{0, \dots, \Delta\}$ at every node, with $c(u) \ne c(v)$ for every edge $\{u, v\} \in E$.

**Cost.** The number of rounds until all nodes have fixed their colours. For a deterministic algorithm, in the worst case; for a randomized one, a bound that holds w.h.p. In the LOCAL model messages are unbounded; in the CONGEST model each message has $O(\log n)$ bits.

## Variants

- **$(\deg + 1)$-list colouring.** Each node $v$ has its own list of at least $\deg(v) + 1$ allowed colours. It contains $(\Delta + 1)$-colouring, and it is the form needed when a colouring is built in parts, because a node with coloured neighbours has a shorter free list. See [list colouring](/list-coloring/).
- **More colours, fewer rounds.** $O(\Delta^2)$ colours take $\log^* n + O(1)$ rounds by [Linial's algorithm](/linial-algorithm/), with no dependence on $\Delta$ in the round count.
- **$\Delta$ colours.** By [Brooks' theorem](/brooks-theorem/), a connected graph that is neither a complete graph nor an odd cycle has a $\Delta$-colouring. Finding one is harder in the distributed setting: Brandt et al. (2016) show a randomized lower bound of $\Omega(\log \log n)$ rounds even on trees; see [sinkless orientation](/sinkless-orientation/).
- **Rings and trees.** With $\Delta = 2$ this is [ring colouring](/ring-coloring/), which takes $\Theta(\log^* n)$ rounds; rooted trees take 3 colours in $\log^* n + O(1)$ rounds by [Cole-Vishkin](/cole-vishkin/).
- **Edge colouring.** Colouring the edges so that edges at a node differ is vertex colouring of the [line graph](/line-graph/); see [distributed edge colouring](/distributed-edge-coloring/).
- **Parallel colouring.** In shared-memory parallel computing the cost is work and span, not rounds. [Jones-Plassmann](/jones-plassmann/) computes the greedy colouring of a random order; run as a distributed algorithm, its number of rounds is the length of the longest path of decreasing priority.

## Examples

**The complete graph $K_{\Delta+1}$** needs all $\Delta + 1$ colours, so the target cannot be lowered in general. Every node sees all others in one round, so one round suffices: colour by the rank of the identifier.

**One phase of random trials** on the path $a - b - c$ with $\Delta = 2$ and colours $\{0, 1, 2\}$. Suppose $a$ and $b$ try and both draw colour 1, and $c$ tries colour 0. Then $a$ and $b$ conflict and both stay uncoloured, while $c$ keeps 0. In the next phase the palette of $b$ is $\{1, 2\}$, since its neighbour $c$ holds 0, and the palette of $a$ is still $\{0, 1, 2\}$.

**A non-example.** Letting every node pick a random colour once and keep it gives a proper colouring only by chance: on a graph with $m$ edges and $\Delta + 1$ colours, the expected number of edges with equal colours is $m / (\Delta + 1)$.

## Known algorithms

**Random colour trials (proved here).** In each phase, every uncoloured node $v$ does the following. With probability $\frac{1}{2}$ it tries: it draws a colour $x$ uniformly from its palette $P(v)$, the colours of $\{0, \dots, \Delta\}$ that no coloured neighbour holds, and sends $x$ to its neighbours. It keeps $x$ if no neighbour tried $x$ in this phase. A phase takes two rounds, and each message is one colour, so the algorithm runs in CONGEST. Johansson (1999) analyzes this kind of algorithm.

*Claim.* In every phase, each uncoloured node keeps a colour with probability at least $\frac{1}{4}$, conditioned on everything that happened before the phase.

*Proof.* Fix the state at the start of the phase. Let $d'$ be the number of uncoloured neighbours of $v$. The coloured neighbours block at most $\deg(v) - d'$ colours, so $|P(v)| \ge \Delta + 1 - (\deg(v) - d') \ge d' + 1$. Let $X$ be the number of uncoloured neighbours that try; $E[X] = d'/2$. The choice of $v$ is uniform on $P(v)$ and independent of the neighbours' choices, which block at most $X$ colours of $P(v)$. So, given that $v$ tries, $v$ keeps its colour with probability at least $E[1 - X/(d' + 1)] \ge 1 - \frac{d'/2}{d' + 1} \ge \frac{1}{2}$. With the coin, the probability is at least $\frac{1}{4}$. $\square$

*Theorem.* After $R = \lceil (c + 1) \log_{4/3} n \rceil$ phases, that is $2R$ rounds, all nodes are coloured with probability at least $1 - n^{-c}$, and the colouring is always proper.

*Proof.* By the claim, a fixed node is still uncoloured after $R$ phases with probability at most $(3/4)^R \le n^{-(c+1)}$. A [union bound](/union-bound/) over the $n$ nodes gives the bound. A node keeps a colour only if no neighbour tried it in the same phase, and later nodes avoid colours of coloured neighbours, so no edge gets two equal colours. $\blacksquare$

**The landscape.** All rows are for $(\Delta + 1)$-colouring; most of them also solve $(\deg + 1)$-list colouring.

| Result | Type | Rounds | Model |
|---|---|---|---|
| Linial (1992), then one colour class per round | deterministic | $O(\Delta^2) + \log^* n$ | CONGEST |
| Barenboim, Elkin and Kuhn (2014) | deterministic | $O(\Delta) + \log^* n$ | LOCAL |
| Panconesi and Srinivasan (1996), by network decomposition | deterministic | $2^{O(\sqrt{\log n})}$ | LOCAL |
| Rozhoň and Ghaffari (2020), by network decomposition | deterministic | $\mathrm{poly}(\log n)$ | LOCAL |
| Ghaffari and Kuhn (2021) | deterministic | $O(\log^2 \Delta \cdot \log n)$ | CONGEST |
| Ghaffari and Grunau (2023), by the MIS reduction | deterministic | $\tilde{O}(\log^2 n)$ | LOCAL |
| Random colour trials (Johansson 1999) | randomized | $O(\log n)$ w.h.p. | CONGEST |
| Barenboim, Elkin, Pettie and Schneider (2012, 2016) | randomized | $O(\log \Delta) + 2^{O(\sqrt{\log \log n})}$ w.h.p. | LOCAL |
| Harris, Schneider and Su (2016, 2018) | randomized | $O(\sqrt{\log \Delta}) + 2^{O(\sqrt{\log \log n})}$ w.h.p. | LOCAL |
| Chang, Li and Pettie (2018, 2020), with Ghaffari and Kuhn (2021) | randomized | $O(\log^3 \log n)$ w.h.p. | LOCAL |
| Chang, Li and Pettie, with Ghaffari and Grunau (2023) | randomized | $\tilde{O}(\log^2 \log n)$ w.h.p. | LOCAL |

The randomized algorithms after 2012 use **shattering**: a randomized phase colours most nodes, and the uncoloured nodes form components of $\mathrm{poly}(\log n)$ size w.h.p., which a deterministic algorithm then finishes. So the randomized complexity depends on the deterministic complexity on graphs of $\mathrm{poly}(\log n)$ nodes: the $O(\log^3 \log n)$ bound is the $O(\log^2 \Delta \cdot \log n)$ bound of Ghaffari and Kuhn applied to such graphs, and the $\tilde{O}(\log^2 \log n)$ bound comes from the $\tilde{O}(\log^2 n)$ bound of Ghaffari and Grunau in the same way.

## Bounds

- **Lower bound.** $\Omega(\log^* n)$ rounds, for deterministic algorithms by [Linial](/linial-coloring-lower-bound/) and for randomized ones by Naor (1991), already on rings with $\Delta = 2$. No larger lower bound is known for $(\Delta + 1)$-colouring in general graphs.
- **Upper bounds.** Deterministic: the smallest of $O(\log^2 \Delta \cdot \log n)$, $\tilde{O}(\log^2 n)$ and $O(\Delta) + \log^* n$. Randomized: $\tilde{O}(\log^2 \log n)$ w.h.p.
- **The gap.** Between $\Omega(\log^* n)$ and these upper bounds there is a gap; whether deterministic $(\Delta + 1)$-colouring takes $O(\log n)$ rounds, or even $\mathrm{poly}(\log \log n)$, is open.

## Reductions

- **Colouring to MIS.** A proper colouring with $k$ colours gives a [maximal independent set](/distributed-mis/) in $k$ rounds: for each colour class in turn, every node of that class with no neighbour in the set joins it.
- **MIS to colouring.** Let $G'$ have the nodes $(v, i)$ for $v \in V$ and $i \in \{0, \dots, \Delta\}$, with the nodes of one $v$ forming a clique and $(u, i)$ adjacent to $(v, i)$ for every edge $\{u, v\}$. Each node of $G$ simulates its $\Delta + 1$ copies, so a round on $G'$ is a round on $G$ in LOCAL. An MIS $I$ of $G'$ holds at most one copy of each $v$, and at least one: if no copy of $v$ were in $I$, each $(v, i)$ would have a neighbour $(u, i)$ in $I$ with $u \in N(v)$, which needs $\Delta + 1$ distinct neighbours of $v$. So $c(v) = i$ for $(v, i) \in I$ is a proper $(\Delta + 1)$-colouring. This is Luby's reduction, and it carries every MIS algorithm over to colouring.
- **Network decomposition.** A [network decomposition](/network-decomposition/) with $C$ colours and cluster diameter $D'$ gives a $(\Delta + 1)$-colouring in $O(C \cdot D')$ rounds: the cluster colours are processed in turn, and each cluster gathers its topology and colours its nodes as a list colouring problem.

## Applications

- **Channel and slot assignment.** Frequency assignment in radio networks and TDMA schedules, where nodes of one colour transmit at the same time without interference.
- **Symmetry breaking.** A colouring with few colours turns into an MIS, a [maximal matching](/distributed-maximal-matching/) or a [ruling set](/ruling-set/) in as many rounds as there are colours.
- **Scheduling local work.** Nodes of one colour class can update shared state in their neighbourhoods at the same time without conflicts, as in the class removal rounds of [Cole-Vishkin](/cole-vishkin/) and [Linial's algorithm](/linial-algorithm/).

## References
