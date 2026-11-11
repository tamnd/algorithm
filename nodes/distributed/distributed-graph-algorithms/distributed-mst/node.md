---
tag: 59V4HH
kind: problem
slug: distributed-mst
name: Distributed minimum spanning tree
aliases:
- distributed MST
- distributed minimum spanning tree problem
area: distributed/distributed-graph-algorithms
level: advanced
summary: Compute the minimum spanning tree of a weighted graph where each node knows only its incident edges.
model: congest-model
complexity:
  vars: {n: the number of nodes, m: the number of edges, D: the hop diameter}
  time: {worst: Ω(D + n^(1/2)/log n)}
  messages: {worst: Ω(m)}
prereqs: [minimum-spanning-tree, cut-property, boruvka, congest-model, round-complexity]
see_also: [gallager-humblet-spira, peleg-rubinovich-lower-bound, low-congestion-shortcuts, distributed-connected-components, distributed-spanning-tree, parallel-minimum-spanning-tree, mst-verification, awerbuch-leader-election]
sources:
  - paper: "Gopal Pandurangan, Peter Robinson and Michele Scquizzato, The distributed minimum spanning tree problem, Bulletin of the EATCS 125, 2018"
    locator: Section 3 (the history up to 2016 and the recent results), Table 1 (the upper bounds), Section 4 (GHS, the Pipeline algorithm and GKP)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Section 4.4 (SynchGHS, the synchronous Borůvka version) and Section 15.5 (the asynchronous GHS algorithm)
  - paper: doi:10.1145/357195.357200
    title: Robert G. Gallager, Pierre A. Humblet and Philip M. Spira, A distributed algorithm for minimum-weight spanning trees, ACM TOPLAS 5(1), 1983
    locator: pages 66 to 77
  - paper: "Juan A. Garay, Shay Kutten and David Peleg, A sublinear time distributed algorithm for minimum-weight spanning trees, SIAM Journal on Computing 27(1), 1998"
    locator: pages 302 to 316, the O(D + n^0.614 log* n) bound
  - paper: "Shay Kutten and David Peleg, Fast distributed construction of small k-dominating sets and applications, Journal of Algorithms 28(1), 1998"
    locator: pages 40 to 66, the O(D + n^(1/2) log* n) bound
  - paper: "Michael Elkin, A faster distributed protocol for constructing a minimum spanning tree, Journal of Computer and System Sciences 72(8), 2006"
    locator: pages 1282 to 1308
  - paper: "Michael Elkin, A simple deterministic distributed MST algorithm, with near-optimal time and message complexities, PODC 2017"
    locator: pages 157 to 163
  - paper: "Gopal Pandurangan, Peter Robinson and Michele Scquizzato, A time- and message-optimal distributed algorithm for minimum spanning trees, STOC 2017"
    locator: pages 743 to 756
  - paper: "Bernhard Haeupler, D. Ellis Hershkowitz and David Wajc, Round- and message-optimal distributed graph algorithms, PODC 2018"
    locator: the MST result, deterministic, Õ(D + n^(1/2)) rounds and Õ(m) messages
  - paper: doi:10.1137/11085178X
    title: Atish Das Sarma, Stephan Holzer, Liah Kor, Amos Korman, Danupon Nanongkai, Gopal Pandurangan, David Peleg and Roger Wattenhofer, Distributed verification and hardness of distributed approximation, SIAM Journal on Computing 41(5), 2012
    locator: pages 1235 to 1265, Theorem 5.1 and the lower bounds for MST and spanning connected subgraph
  - paper: "Shay Kutten, Gopal Pandurangan, David Peleg, Peter Robinson and Amitabh Trehan, On the complexity of universal leader election, Journal of the ACM 62(1), 2015"
    locator: the Ω(m) message lower bound
  - paper: "Tomasz Jurdziński and Krzysztof Nowicki, MST in O(1) rounds of congested clique, SODA 2018"
    locator: pages 2620 to 2632
---

In the distributed minimum spanning tree problem, the nodes of a network compute the [minimum spanning tree](/minimum-spanning-tree/) of the network itself. Each node knows only the weights of its own edges, and at the end each node knows which of its edges are in the tree. The standard setting is the [CONGEST model](/congest-model/): synchronous rounds, and one message of $O(\log n)$ bits on each edge in each round. The first algorithm is [GHS](/gallager-humblet-spira/) (1983). The best algorithms take $\tilde{O}(D + \sqrt{n})$ rounds and $\tilde{O}(m)$ messages, and the [Peleg-Rubinovich lower bound](/peleg-rubinovich-lower-bound/) shows that no algorithm can do much better in rounds. The problem is the model case for "global" problems in distributed computing.

## In plain words

Each computer in a network knows only its own cables and their prices. Together, the computers must choose the cheapest set of cables that still connects all of them. No computer sees the whole network, and messages are small.

Two costs count: the number of rounds (time) and the number of messages. Every method starts like [Borůvka's algorithm](/boruvka/): small groups find their cheapest cable to the outside and join along it.

A group that is a long thin path is slow, because news must walk along it. Fast methods mix two ideas. They grow groups only until each has about $\sqrt{n}$ computers. Then they send the few remaining choices to one place over a [BFS tree](/breadth-first-search-distributed/), which has depth $D$. No method can beat about $D + \sqrt{n}$ rounds on some networks.

## Definition

**Network.** A connected undirected graph $G = (V, E)$ with $n$ nodes, $m$ edges and hop diameter $D$, with a weight $w(e)$ on each edge. Each node has a unique identifier of $O(\log n)$ bits. Weights are integers polynomial in $n$, so a weight fits in one message. Ties are broken by the identifiers of the endpoints, so we may assume that the weights are distinct and the MST $T$ is unique ([MST uniqueness](/mst-uniqueness/)).

**Input.** Each node $v$ knows its identifier and the weights of its incident edges. In most results it also knows $n$ (or a polynomial upper bound on it). In the KT0 setting a node does not know the identifiers of its neighbours. In the KT1 setting it does.

**Output.** Each node $v$ marks each incident edge as in $T$ or not in $T$. The two ends of an edge must agree.

**Costs.**

- [Round complexity](/round-complexity/): the number of synchronous rounds until all nodes have their output.
- [Message complexity](/message-complexity/): the total number of messages.
- In the [asynchronous model](/asynchronous-model/), time is measured with the assumption that each message takes at most one time unit.

A problem is called *global* when its round complexity depends on $D$. The MST is global: the weight of one edge far away can change which edge is in $T$. A local problem such as [MIS](/distributed-mis/) has round complexity that does not depend on $D$.

Notation on this page: $n$ nodes, $m$ edges, $D$ the hop diameter, $B = O(\log n)$ the bits in one message, and $\tilde{O}$ hides factors polylogarithmic in $n$.

## Variants

- **Asynchronous MST.** No clock and only message delays. [GHS](/gallager-humblet-spira/) solves it with $O(m + n \log n)$ messages.
- **Approximate MST.** Find a spanning tree of weight at most $\alpha$ times the minimum. The lower bound stays almost the same for each $\alpha$ (see Bounds).
- **[MST verification](/mst-verification/).** Check that a marked subgraph is an MST. It has the same lower bound as the construction.
- **Spanning tree with no weights.** A [distributed spanning tree](/distributed-spanning-tree/), for example a [BFS tree](/breadth-first-search-distributed/), takes only $O(D)$ rounds. Weights make the problem hard.
- **[Congested clique](/congested-clique-model/).** Every pair of nodes can talk, and only the input graph is sparse. MST takes $O(\log \log n)$ rounds deterministically (Lotker, Patt-Shamir, Pavlov and Peleg, 2005), and $O(1)$ rounds with randomization (Jurdziński and Nowicki, SODA 2018).
- **Special graph classes.** Planar graphs, graphs of bounded genus or treewidth, and graphs with small mixing time have faster algorithms. See [low-congestion shortcuts](/low-congestion-shortcuts/).
- **Leader election.** Each MST algorithm also elects a leader, for example an end of the final core edge. See [Awerbuch's election](/awerbuch-leader-election/).

## Examples

**A Borůvka run in CONGEST.** Take the graph with 6 nodes and these edges (endpoints and weight): $01{:}3$, $12{:}1$, $23{:}6$, $34{:}2$, $45{:}5$, $05{:}4$, $14{:}7$, $25{:}8$. The algorithm below runs $\lceil \log_2 6 \rceil = 3$ phases of $3n + 2 = 20$ rounds.

| phase | MOE of each fragment | fragments after the phase |
|---|---|---|
| 1 | $\{0\}{:}3$, $\{1\}{:}1$, $\{2\}{:}1$, $\{3\}{:}2$, $\{4\}{:}2$, $\{5\}{:}4$ | $\{0,1,2,5\}$, $\{3,4\}$ |
| 2 | $\{0,1,2,5\}{:}5$, $\{3,4\}{:}5$ | $\{0,1,2,3,4,5\}$ |
| 3 | none | unchanged |

The tree has the weights $\{1, 2, 3, 4, 5\}$, as with [Kruskal's algorithm](/kruskal/). In phase 1 the core edges are $12$ and $34$, because both ends chose them. The run takes 60 rounds and 83 messages, and the largest message has 9 bits. The [GHS page](/gallager-humblet-spira/) runs the same graph in the asynchronous model.

**Why the diameter is not enough.** A ring of $n$ nodes has $D = \lfloor n/2 \rfloor$, and the MST drops the heaviest edge. The two ends of that edge must learn that it is the heaviest, which takes about $n/2$ rounds. So $\Omega(D)$ is needed. The [Peleg-Rubinovich](/peleg-rubinovich-lower-bound/) graphs have $D = O(\log n)$ but still need about $\sqrt{n}$ rounds: many long paths must send their information over a small tree of shortcuts.

## Known algorithms

**Borůvka in CONGEST (SynchGHS).** This is the algorithm of the implementation on this page, as in Lynch, Section 4.4. It assumes that the nodes know $n$. It has $\lceil \log_2 n \rceil$ phases of $3n + 2$ rounds. A fragment is a rooted subtree of $T$, with the root's identifier as its name. In each phase:

1. Each node sends the name of its fragment to all neighbours (1 round).
2. Each node finds its lightest edge to another fragment. A convergecast finds the minimum over the fragment at the root (at most $n$ rounds).
3. The root broadcasts the weight of this minimum outgoing edge (MOE) in the fragment (at most $n$ rounds).
4. The node at the MOE sends Connect over it (1 round). An edge with a Connect from both ends is a *core*.
5. The larger end of each core takes its identifier as the new name and floods it over the new tree, which also sets the new parents (at most $n$ rounds).

By the [cut property](/cut-property/), each MOE is in $T$. The fragments and their MOEs form a forest in which each tree has exactly one core. Each fragment joins at least one other, so the number of fragments at least halves in each phase. After $\lceil \log_2 n \rceil$ phases one fragment remains. A phase sends at most $2m$ name messages and at most $4n$ other messages, so the total is $O(n \log n)$ rounds and $O(m \log n)$ messages. Each message holds one name or one weight, which is $O(\log n)$ bits.

The phase length is fixed because a fragment can be a path of $\Theta(n)$ nodes even when $D$ is small. This is the bottleneck that the later algorithms remove.

**The landscape.** Times are in rounds for the synchronous results and in time units for the asynchronous ones.

| algorithm | year | time | messages | notes |
|---|---|---|---|---|
| [Gallager, Humblet and Spira](/gallager-humblet-spira/) | 1983 | $O(n \log n)$ | $O(m + n \log n)$ | asynchronous, deterministic |
| Awerbuch, STOC 1987 | 1987 | $O(n)$ | $O(m + n \log n)$ | asynchronous, deterministic, optimal for $D = \Theta(n)$ |
| Garay, Kutten and Peleg | 1993, 1998 | $O(D + n^{0.614} \log^* n)$ | $O(m + n^{1.614})$ | the first time sublinear in $n$ |
| Kutten and Peleg | 1995, 1998 | $O(D + \sqrt{n} \log^* n)$ | $O(m + n^{1.5})$ | GKP with a better first part |
| Elkin, JCSS 2006 | 2006 | $\tilde{O}(\mu(G, w) + \sqrt{n})$ | $O(m + n^{1.5})$ | randomized; $\mu(G, w)$ is the MST radius, a parameter of the weighted graph |
| Pandurangan, Robinson and Scquizzato, STOC 2017 | 2017 | $\tilde{O}(D + \sqrt{n})$ | $\tilde{O}(m)$ | randomized Las Vegas; the first optimal in both |
| Elkin, PODC 2017 | 2017 | $\tilde{O}(D + \sqrt{n})$ | $\tilde{O}(m)$ | deterministic and simple |
| Haeupler, Hershkowitz and Wajc, PODC 2018 | 2018 | $\tilde{O}(D + \sqrt{n})$ | $\tilde{O}(m)$ | deterministic |

In the table, $\log^*$ is the [iterated logarithm](/iterated-logarithm/). The asynchronous time bounds improved from $O(n \log n)$ to $O(n \log \log n)$ (Chin and Ting, 1985), to $O(n \log^* n)$ (Gafni, 1985) and to $O(n)$ (Awerbuch).

**The two-part scheme of GKP.** The sublinear algorithms share one plan.

- *Part 1, controlled Borůvka.* Run Borůvka phases, but cap the fragment diameter, so that phase $i$ takes $O(2^i)$ rounds. Stop when about $\sqrt{n}$ fragments of diameter $O(\sqrt{n})$ are left. This takes $\tilde{O}(\sqrt{n})$ rounds.
- *Part 2, the Pipeline algorithm (Peleg).* Build a BFS tree of depth $D$. Each node sends inter-fragment edges up the tree in increasing order of weight. It drops an edge that closes a cycle with the edges it already sent, by the [cycle property](/cycle-property/). Each node sends at most (the number of fragments) $- 1$ edges, so this takes $O(D + \sqrt{n})$ rounds.

The message-optimal algorithms of 2017 and 2018 replace the BFS pipeline by a cheaper scheme, so that the messages drop to $\tilde{O}(m)$ while the rounds stay $\tilde{O}(D + \sqrt{n})$.

## Bounds

**Rounds.** Every algorithm needs $\Omega(D)$ rounds (the ring example). The [Peleg-Rubinovich lower bound](/peleg-rubinovich-lower-bound/) (2000) shows $\Omega(D + \sqrt{n}/\log n)$ rounds for deterministic algorithms, on graphs of diameter $D = \Omega(\log n)$ with $B = O(\log n)$. Elkin (SIAM J. Comput. 2006) extended it to approximation. Das Sarma et al. (SIAM J. Comput. 2012) showed $\Omega(D + \sqrt{n/(B \log n)})$ rounds for any approximation ratio, also for randomized Monte Carlo algorithms. So $\tilde{\Theta}(D + \sqrt{n})$ is the round complexity, up to polylog factors. Small diameters behave differently: for $D = 3$ and $D = 4$ the lower bounds are $\tilde{\Omega}(n^{1/4})$ and $\tilde{\Omega}(n^{1/3})$ (Lotker, Patt-Shamir and Peleg, 2006; Das Sarma et al., Theorem 5.1), and for $D = 2$ there is an $O(\log n)$ round algorithm.

**Messages.** In the KT0 setting, each algorithm needs $\Omega(m)$ messages, even with randomization (Kutten et al., J. ACM 2015). With $\Omega(D + \sqrt{n})$ rounds and $\Omega(m)$ messages, the algorithms of 2017 and 2018 are optimal in both measures up to polylog factors.

**Bits.** The bound on the message size matters. With messages of $B$ bits, the round lower bound is $\tilde{\Omega}(\sqrt{n/B})$. In the [LOCAL model](/local-model/) with no limit on the size, MST takes $O(D)$ rounds: collect the whole graph at one node.

## Reductions

- **MST gives connectivity.** Give each edge of a subgraph $H$ weight 0 and each other edge weight 1. The MST has weight 0 exactly when $H$ is a connected spanning subgraph, so [connected components of a subgraph](/distributed-connected-components/) reduce to MST in CONGEST.
- **Lower bounds go the other way.** Das Sarma et al. prove the lower bound first for verification problems (for example: is $H$ a connected spanning subgraph?), by a simulation of a two-party [communication](/communication-complexity/) protocol for [set disjointness](/disjointness-problem/). Then they reduce verification to MST and to many other problems, such as min cut and shortest paths.
- **Leader election.** An MST algorithm elects a leader with $O(n)$ more messages, so the $\Omega(m)$ message bound for election also applies to MST.

## Applications

- **Broadcast with few messages.** A message sent along a spanning tree costs $n - 1$ messages. The MST also minimizes the total cost of the tree when the weights are link costs.
- **A base for other algorithms.** [Awerbuch's leader election](/awerbuch-leader-election/) and many [synchronizers](/synchronizer/) build a spanning tree first. The MST scheme of fragments is reused for [connected components](/distributed-connected-components/), [min cut](/distributed-min-cut/) and [low-congestion shortcuts](/low-congestion-shortcuts/).
- **A benchmark for lower bounds.** The $\tilde{\Omega}(D + \sqrt{n})$ bound for MST is the starting point for the lower bounds of [shortest paths](/distributed-shortest-paths/), [min cut](/distributed-min-cut/) and [max flow](/distributed-max-flow/) in CONGEST.

## References
