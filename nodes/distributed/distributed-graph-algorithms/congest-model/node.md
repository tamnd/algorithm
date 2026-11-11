---
tag: ECCJVR
kind: model
slug: congest-model
name: CONGEST model
aliases:
- CONGEST(B)
- bounded-bandwidth distributed model
area: distributed/distributed-graph-algorithms
level: core
summary: The LOCAL model with a bandwidth limit, in which each edge carries a message of O(log n) bits in each direction per round. Problems with O(D) rounds in LOCAL can need about sqrt(n) or n rounds here.
prereqs: [local-model, synchronous-model, breadth-first-search-distributed]
see_also: [local-model, congested-clique-model, round-complexity, message-complexity, distributed-mst, low-congestion-shortcuts, peleg-rubinovich-lower-bound, diameter-lower-bound-distributed]
sources:
  - book: isbn:9780898714647
    title: David Peleg, Distributed Computing, A Locality-Sensitive Approach, SIAM, 2000
    locator: Chapter 2 (the CONGEST model and the bandwidth limit) and Chapters 3 and 4 (broadcast, convergecast and pipelined upcasts and downcasts)
  - url: https://jukkasuomela.fi/da2020/da2020.pdf
    title: Juho Hirvonen and Jukka Suomela, Distributed Algorithms 2020, online textbook
    locator: Chapter 5 (the CONGEST model, bandwidth limitations and all-pairs shortest paths)
  - paper: doi:10.1137/S0097539700369740
    title: David Peleg and Vitaly Rubinovich, A near-tight lower bound on the time complexity of distributed minimum-weight spanning tree construction, SIAM Journal on Computing 30(5), 1427-1442, 2000
    locator: the lower bound of about sqrt(n) / log n rounds for MST on graphs of small diameter
  - paper: doi:10.1145/1993636.1993686
    title: Atish Das Sarma, Stephan Holzer, Liah Kor, Amos Korman, Danupon Nanongkai, Gopal Pandurangan, David Peleg and Roger Wattenhofer, Distributed verification and hardness of distributed approximation, STOC 2011
    locator: lower bounds of about sqrt(n / log n) + D rounds for MST, shortest paths and verification problems, by reduction from two-party communication complexity
  - paper: doi:10.1137/1.9781611973099.91
    title: Silvio Frischknecht, Stephan Holzer and Roger Wattenhofer, Networks cannot compute their diameter in sublinear time, SODA 2012
    locator: the lower bound of about n / log n rounds for computing the diameter, even on graphs of constant diameter
  - paper: doi:10.1137/S0097539794261118
    title: Juan A. Garay, Shay Kutten and David Peleg, A sublinear time distributed algorithm for minimum-weight spanning trees, SIAM Journal on Computing 27(1), 302-316, 1998
    locator: the first MST algorithm in o(n) rounds
  - paper: doi:10.1006/jagm.1998.0929
    title: Shay Kutten and David Peleg, Fast distributed construction of small k-dominating sets and applications, Journal of Algorithms 28(1), 40-66, 1998
    locator: MST in O(sqrt(n) log* n + D) rounds
---

The CONGEST model is the [LOCAL model](/local-model/) with a limit on bandwidth. The network is again the input graph, nodes have unique identifiers and work in synchronous rounds, but in each round a node can send only $B$ bits on each edge, usually $B = O(\log n)$: enough for a constant number of identifiers, distances or weights. Peleg (2000) named the model. It separates two obstacles that LOCAL merges: *distance*, which costs $D$ rounds in both models, and *congestion*, which appears when much information must cross a small cut. Many problems that take $O(D)$ rounds in LOCAL need $\tilde{\Theta}(\sqrt{n} + D)$ rounds in CONGEST, such as the [minimum spanning tree](/distributed-mst/), or $\tilde{\Theta}(n)$ rounds, such as the exact [diameter](/distributed-diameter/).

## The machine

**Notation.** The network is a simple connected undirected graph with $n$ nodes, $m$ edges, diameter $D$ and largest degree $\Delta$. $\tilde{O}$ and $\tilde{\Omega}$ hide factors polylogarithmic in $n$.

**Nodes.** As in [LOCAL](/local-model/): each node has a unique identifier of $O(\log n)$ bits, knows its [ports](/port-numbering/), its input and usually $n$ (or a polynomial upper bound), and has unbounded memory and free local computation. Edge weights, if any, are integers of $O(\log n)$ bits, known at both ends.

**Rounds.** Synchronous and fault-free. In each round each node sends at most one message of at most $B$ bits on each port (different messages on different ports are allowed), receives the messages of its neighbours and computes. Each edge carries $B$ bits in each direction per round.

**The bandwidth.** CONGEST, without a parameter, means $B = c \lceil \log_2 (n+1) \rceil$ for a constant $c$. Larger $B$ is written CONGEST($B$). A message of $B$ bits can be split into $\lceil B / \log n \rceil$ standard messages, so CONGEST($B$) is simulated in CONGEST with a slowdown of $O(B/\log n)$.

**Variants.** *Broadcast CONGEST* requires the same message on all ports in a round. In *KT0* nodes start without the identifiers of their neighbours; in *KT1* they know them. Round counts are the same up to one round, but message counts can differ; see [broadcast](/broadcast-problem/).

## What it counts

**Rounds.** The main measure, as in LOCAL: the number of rounds until all nodes have stopped, in the worst case, as a function of $n$, $D$ and sometimes $\Delta$ or the weights. See [round complexity](/round-complexity/).

**Messages.** Because messages are short, their number is also a fair measure of total communication, and many papers bound it: for example $O(m)$ for [BFS](/breadth-first-search-distributed/) and $O(m + n \log n)$ for [MST](/gallager-humblet-spira/). See [message complexity](/message-complexity/).

**Congestion and dilation.** For a set of messages routed on paths, the *dilation* is the longest path and the *congestion* is the most messages that use one edge. A schedule needs at least $\max(\text{congestion}, \text{dilation})$ rounds, and simple random delays reach $O(\text{congestion} + \text{dilation} \cdot \log n)$; this is the basic tool of CONGEST algorithms, as in [low-congestion shortcuts](/low-congestion-shortcuts/).

## Relation to other models

- **[LOCAL](/local-model/).** CONGEST is LOCAL with messages cut to $O(\log n)$ bits. Every CONGEST algorithm runs in LOCAL in the same number of rounds, so LOCAL lower bounds hold here too. In LOCAL every solvable problem takes at most $D + 1$ rounds; in CONGEST the gap can be large.
- **[Congested clique](/congested-clique-model/).** The same bandwidth, but every pair of nodes can talk, whatever the input graph. Distance is no longer an obstacle, only congestion.
- **[Port numbering](/port-numbering/).** Without identifiers; usually studied in the LOCAL form.
- **Two-party communication.** If the network has a cut of $k$ edges, $t$ rounds of CONGEST send at most $2ktB$ bits across it. So a function whose two-party communication complexity is $C$ needs $t \ge C/(2kB)$ rounds when its two halves of input lie on the two sides. Most CONGEST lower bounds use this, with set disjointness as $C$.
- **Parallel models.** CONGEST is the message-passing analogue of [Pregel](/pregel-model/) and vertex-centric graph systems, where each vertex sends small messages to its neighbours in supersteps.

**A gap with LOCAL, proved here.** Let the *dumbbell* $G_n$ be two stars of $n/2$ nodes each whose centres are joined by an edge, so $D = 3$, and let identifiers come from $\{1, \dots, n^2\}$. The task is that every node learns the set of all identifiers. In LOCAL, the gathering algorithm of the [LOCAL page](/local-model/) does it in $D + 1 = 4$ rounds. In CONGEST with $B$-bit messages, every deterministic algorithm needs at least
$$t \ge \frac{\log_2 \binom{n^2 - n/2}{n/2}}{B + 1} \ge \frac{(n/2)\log_2 n}{B + 1}$$
rounds. *Proof.* Fix the identifiers on the right star. The state of the right side after $t$ rounds is determined by its own initial state and the messages that cross the bridge to it, since all other messages stay inside the right side. In each round the bridge carries either no message or a string of at most $B$ bits to the right: at most $2^{B+1}$ choices, so at most $2^{(B+1)t}$ possible states of the right side. The right centre must output the left identifiers, which can be any $n/2$ of the $n^2 - n/2$ unused values, and different choices need different states. So $2^{(B+1)t} \ge \binom{n^2 - n/2}{n/2} \ge (2n - 1)^{n/2} \ge n^{n/2}$. ∎ With $B = c \lceil \log_2(n+1) \rceil$ this is $\Omega(n / c)$ rounds, against 4 in LOCAL. Pipelining, with each node forwarding the smallest identifier it has not yet sent, solves the task in $O(n + D)$ rounds (Peleg 2000, Chapter 4, for pipelined broadcast of many messages, cited); the tests check the bound $n + D$ on small graphs.

## Known results in the model

All bounds below are cited unless a proof is linked. $D$ is the diameter, $n$ the number of nodes.

| problem | upper bound | lower bound |
|---|---|---|
| [BFS](/breadth-first-search-distributed/), [broadcast](/broadcast-problem/), leader election | $O(D)$ | $\Omega(D)$ |
| learn all identifiers (gather $n$ tokens) | $O(n + D)$ by pipelining | $\Omega(n)$ on the dumbbell, where $D = 3$ (proved above) |
| [MST](/distributed-mst/) | $O(\sqrt{n} \log^* n + D)$ (Garay, Kutten and Peleg 1998; Kutten and Peleg 1998) | $\tilde{\Omega}(\sqrt{n} + D)$ ([Peleg and Rubinovich](/peleg-rubinovich-lower-bound/) 2000; Das Sarma et al. 2011) |
| exact SSSP, weighted | $O(n)$ by [Bellman-Ford](/distributed-bellman-ford/); better sublinear bounds on the [shortest paths](/distributed-shortest-paths/) page | $\tilde{\Omega}(\sqrt{n} + D)$, even to approximate (Das Sarma et al. 2011) |
| [diameter](/distributed-diameter/), [APSP](/distributed-apsp/), unweighted | $O(n)$ | $\tilde{\Omega}(n)$ even for $D = O(1)$ ([Frischknecht, Holzer and Wattenhofer](/diameter-lower-bound-distributed/) 2012) |
| [MIS](/distributed-mis/), $(\Delta+1)$-colouring | $O(\log n)$ randomized ([Luby](/luby-mis/), its messages are short) | the LOCAL bounds ([KMW](/kmw-lower-bound/)) |
| [triangle enumeration](/distributed-triangle-enumeration/) | sublinear, see that page | polynomial in $n$, see that page |
| [min cut](/distributed-min-cut/), [max flow](/distributed-max-flow/) | see those pages | $\tilde{\Omega}(\sqrt{n} + D)$ for many of them, by the same reduction |

The bounds of the form $\tilde{\Theta}(\sqrt{n} + D)$ come from one construction: a graph with many long paths, which carry the input of two players, and a tree of small depth, which gives small $D$ but whose edges near the root are a bottleneck. Upper bounds on special graph classes use [low-congestion shortcuts](/low-congestion-shortcuts/) to beat $\sqrt{n}$. The tests of the implementation check that the simulator rejects every message longer than $c \lceil \log_2(n+1) \rceil$ bits under a fixed self-delimiting code, that synchronous BFS fits in this budget, that gathering the whole graph does not, and the dumbbell gap above.

## References
