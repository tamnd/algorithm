---
tag: 84M8SP
kind: model
slug: congested-clique-model
name: Congested clique model
aliases:
- Congested Clique
- CONGESTED CLIQUE model
- clique model with bounded bandwidth
area: distributed/distributed-graph-algorithms
level: advanced
summary: n nodes, one per vertex of the input graph, exchange O(log n)-bit messages between every pair in each synchronous round. Distance costs nothing, so only the volume of communication counts.
prereqs: [congest-model, local-model, minimum-spanning-tree]
see_also: [congest-model, local-model, distributed-mst, distributed-triangle-enumeration, distributed-apsp, mapreduce-model, mrc-model, bsp-model]
sources:
  - paper: doi:10.1137/S0097539704441848
    title: Zvi Lotker, Boaz Patt-Shamir, Elan Pavlov and David Peleg, Minimum-weight spanning tree construction in O(log log n) communication rounds, SIAM Journal on Computing 35(1), 120-131, 2005
    locator: the model of a complete network with O(log n)-bit messages and the deterministic MST algorithm in O(log log n) rounds
  - paper: doi:10.1145/2484239.2501983
    title: Christoph Lenzen, Optimal deterministic routing and sorting on the congested clique, PODC 2013, 42-50
    locator: deterministic routing in O(1) rounds when every node is the source and the destination of at most n messages, and sorting n^2 keys in O(1) rounds
  - paper: doi:10.1145/2933057.2933103
    title: Mohsen Ghaffari and Merav Parter, MST in log-star rounds of congested clique, PODC 2016
    locator: randomized MST in O(log* n) rounds
  - paper: doi:10.1137/1.9781611975031.167
    title: Tomasz Jurdziński and Krzysztof Nowicki, MST in O(1) rounds of congested clique, SODA 2018
    locator: randomized MST in O(1) rounds
  - paper: doi:10.1007/s00446-016-0270-2
    title: Keren Censor-Hillel, Petteri Kaski, Janne H. Korhonen, Christoph Lenzen, Ami Paz and Jukka Suomela, Algebraic methods in the congested clique, Distributed Computing 32(6), 461-478, 2019
    locator: matrix multiplication in O(n^(1 - 2/omega)) rounds and its use for triangle counting, girth and all-pairs shortest paths
  - paper: doi:10.1145/2611462.2611493
    title: Andrew Drucker, Fabian Kuhn and Rotem Oshman, On the power of the congested clique model, PODC 2014
    locator: simulation of the model by circuits, so that strong lower bounds for explicit problems would give new circuit lower bounds
  - paper: doi:10.1016/j.tcs.2015.09.029
    title: James W. Hegeman and Sriram V. Pemmaraju, Lessons from the congested clique applied to MapReduce, Theoretical Computer Science 608, 268-281, 2015
    locator: simulation of congested clique algorithms in MapReduce-style models with a matching number of rounds, under conditions on memory and machines
---

The congested clique is a model of distributed graph computation in which the communication network is a complete graph, whatever the input graph is. There are $n$ nodes, one for each vertex of the input graph $G$, and each node first knows only its own edges of $G$. In every synchronous round, every node can send a different message of $O(\log n)$ bits to every other node. Lotker, Patt-Shamir, Pavlov and Peleg (2005) introduced it with an MST algorithm in $O(\log \log n)$ rounds. Since every pair of nodes is one hop apart, distance costs nothing; what remains is *congestion*: each node can send and receive only $O(n \log n)$ bits per round. The model is the opposite extreme to [LOCAL](/local-model/), where bandwidth is free and distance is the cost, and it is closely related to the MPC and [MapReduce](/mapreduce-model/) models of parallel computing.

## The machine

**Notation.** The input is a graph $G = (V, E)$ with $n = |V|$ nodes, $m = |E|$ edges and largest degree $\Delta$, possibly with integer weights of $O(\log n)$ bits. The communication graph is the complete graph $K_n$ on $V$, so its diameter is 1; the diameter of $G$ plays no role in the cost.

**Nodes.** Node $v$ has a unique identifier, usually from $\{1, \dots, n\}$, and knows $n$, all identifiers, and its incident edges of $G$ with their weights. Memory and local computation are unbounded.

**Rounds.** Synchronous and fault-free. In each round, each node sends a message of at most $B = O(\log n)$ bits to each other node (the $n - 1$ messages can differ), receives the $n - 1$ messages addressed to it and computes. So each node sends and receives $O(n \log n)$ bits per round, and the whole network moves $O(n^2 \log n)$ bits per round.

**Variants.** In the *broadcast congested clique* each node sends the same message to all others in a round. Some papers allow $B$ other than $\Theta(\log n)$, or randomness; the bounds below say which.

## What it counts

**Rounds.** The number of rounds until every node knows its part of the output, in the worst case over input graphs of $n$ nodes. See [round complexity](/round-complexity/). Messages are not counted, since $\Theta(n^2)$ of them per round are free.

**What can be done in one round.** Each node can tell all other nodes $O(\log n)$ bits, for example its degree, a flag, or one edge. A node with $d$ edges needs $d$ rounds to send them all to one chosen node on their direct link, but about $2\lceil d/(n-1) \rceil$ rounds if it first spreads them over other nodes, which then relay them.

**A trivial upper bound, proved here.** Every problem on $G$ whose output at each node has $O(\log n)$ bits is solved in at most $n$ rounds: in rounds $1, \dots, n - 1$, each node $v$ sends its incident edges of $G$ one per round to node 1 on their direct link, which takes $\deg(v) \le n - 1$ rounds; node 1 then knows $G$, computes a solution, and in one more round sends each node its output. Faster algorithms spread the load over all links, and this is where routing comes in.

**Routing (cited).** Lenzen (2013) shows that if every node is the source of at most $n$ messages and the destination of at most $n$ messages, of $O(\log n)$ bits each, then all of them can be delivered deterministically in $O(1)$ rounds, without the nodes knowing the pattern in advance. So any communication pattern that respects these per-node limits costs a constant number of rounds. A corollary: node 1 can collect any $m'$ words from the network in $O(\lceil m' / n \rceil)$ rounds, and the whole graph in $O(m/n + 1)$ rounds, which is $O(1)$ when $m = O(n)$. Lenzen (2013) also sorts $n^2$ keys, $n$ per node, in $O(1)$ rounds.

## Relation to other models

- **[CONGEST](/congest-model/).** The same bandwidth per link, but in CONGEST the links are the edges of $G$. A CONGEST algorithm runs in the congested clique in the same number of rounds, since the clique contains $G$; the converse fails, since the clique can move $\Theta(n^2 \log n)$ bits per round between any parts of $G$. CONGEST lower bounds of the form $\tilde{\Omega}(\sqrt{n} + D)$ or $\tilde{\Omega}(n)$ come from small cuts and do not carry over.
- **[LOCAL](/local-model/).** On a complete communication graph with unbounded messages, every problem takes one round (every node sends its edges to every other node). The congested clique is that setting with the bandwidth of CONGEST.
- **MPC and MapReduce.** In the massively parallel computation model, $M$ machines with $S$ words of memory each exchange messages in rounds, each machine sending and receiving at most $S$ words. With $M = n$ and $S = \Theta(n)$ this is close to the congested clique with Lenzen routing. Hegeman and Pemmaraju (2015, cited) show that congested clique algorithms can be run in [MapReduce](/mapreduce-model/)-style models such as [MRC](/mrc-model/) with a matching number of rounds, under conditions on memory and on the number of machines. So results and techniques move between the two settings.
- **[BSP](/bsp-model/).** The congested clique is close to a BSP machine with $n$ processors, unit-cost barriers and an $h$-relation limit of $h = n$ words per superstep, with the input graph distributed by vertices.
- **Circuits.** Drucker, Kuhn and Oshman (2014, cited) show that the model can be simulated by circuits of moderate size and depth, so that a strong round lower bound for an explicit problem would give a circuit lower bound that is not known today. This explains why almost no super-constant lower bounds are known for the unrestricted model.

## Known results in the model

All bounds below are cited. They hold for the standard model with $O(\log n)$-bit messages.

| problem | rounds | source |
|---|---|---|
| routing, $n$ messages per node in and out | $O(1)$, deterministic | Lenzen 2013 |
| sorting $n^2$ keys | $O(1)$, deterministic | Lenzen 2013 |
| [MST](/distributed-mst/) | $O(\log \log n)$, deterministic | Lotker, Patt-Shamir, Pavlov and Peleg 2005 |
| [MST](/distributed-mst/) | $O(\log^* n)$, randomized | Ghaffari and Parter 2016 |
| [MST](/distributed-mst/) | $O(1)$, randomized | Jurdziński and Nowicki 2018 |
| matrix multiplication, semiring | $O(n^{1/3})$ | Censor-Hillel et al. 2019 |
| matrix multiplication, ring | $O(n^{1 - 2/\omega})$, with $\omega$ the matrix multiplication exponent | Censor-Hillel et al. 2019 |
| [triangle](/distributed-triangle-enumeration/) detection and counting | $O(n^{1 - 2/\omega})$ via matrix multiplication; listing in $\tilde{O}(n^{1/3})$ (Dolev, Lenzen and Peled 2012) | Censor-Hillel et al. 2019 |
| [APSP](/distributed-apsp/), integer weights | $\tilde{O}(n^{1/3})$, via semiring matrix multiplication | Censor-Hillel et al. 2019 |
| [APSP](/distributed-apsp/), unweighted undirected | $n^{1 - 2/\omega + o(1)}$ | Censor-Hillel et al. 2019 |

**The MST algorithm of Lotker et al. (sketch).** The algorithm runs Borůvka-style phases on fragments of the [minimum spanning tree](/minimum-spanning-tree/). In a phase, if every fragment has at least $k$ nodes, each fragment finds its $k$ lightest edges to $k$ distinct other fragments, and its nodes together can send these to a single coordinator. The coordinator merges fragments with these edges, and the [cut property](/minimum-spanning-tree/) keeps the result correct. After the phase, each new fragment has at least about $k^2$ nodes, so the minimum fragment size squares in each phase: $2, 4, 16, 256, \dots$, and after $O(\log \log n)$ phases one fragment remains. Each phase takes $O(1)$ rounds, because the many links of a large fragment carry its edges in parallel.

**Lower bounds.** For the unrestricted model, no super-constant lower bound is known for any natural problem, and the circuit simulation of Drucker, Kuhn and Oshman explains why. Lower bounds are known for the broadcast congested clique and for restricted algorithms.

## References
