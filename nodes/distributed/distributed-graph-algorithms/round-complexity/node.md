---
tag: 6CMCBB
kind: concept
slug: round-complexity
name: Round complexity
aliases:
- time complexity in distributed models
- round number
- distributed time complexity
area: distributed/distributed-graph-algorithms
level: core
summary: The number of synchronous rounds until every node has stopped, in the worst case. In asynchronous networks, time with message delays scaled to at most one unit plays the same role.
prereqs: [local-model, synchronous-model, asynchronous-model]
see_also: [message-complexity, local-model, congest-model, congested-clique-model, synchronizer, flooding, echo-algorithm, diameter-lower-bound-distributed]
sources:
  - book: isbn:9780898714647
    title: David Peleg, Distributed Computing, A Locality-Sensitive Approach, SIAM, 2000
    locator: Chapter 2 (time complexity in the synchronous and asynchronous models, with the normalization of delays) and Chapter 3 (the Omega(D) bound for broadcast)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 2 (the synchronous network model, rounds and time complexity) and Chapter 14 (the asynchronous network model, time with an upper bound on delays)
  - paper: doi:10.1145/4221.4227
    title: Baruch Awerbuch, Complexity of network synchronization, Journal of the ACM 32(4), 804-823, 1985
    locator: the time measure for asynchronous networks with message delays of at most one unit, and the cost of simulating synchronous rounds
  - url: https://jukkasuomela.fi/da2020/da2020.pdf
    title: Juho Hirvonen and Jukka Suomela, Distributed Algorithms 2020, online textbook
    locator: Chapters 3 to 5 (running time as the number of rounds in the PN, LOCAL and CONGEST models)
---

The round complexity of a distributed algorithm is the number of communication rounds it needs before every node has stopped with its output. It is the main measure of speed in the synchronous models of distributed graph computing, [LOCAL](/local-model/), [CONGEST](/congest-model/) and the [congested clique](/congested-clique-model/), where in one round every node can send one message to each neighbour. Since a message moves one hop per round, round complexity measures how far information must travel, and the diameter $D$ is the natural yardstick. For asynchronous networks, where there are no rounds, the same role is played by *time* with every message delay scaled to at most one unit. Round complexity is the counterpart of [message complexity](/message-complexity/), which counts the total communication; this page is about time only.

## In plain words

Think of a group of people who can only speak to their direct neighbours, and only at the stroke of a clock. At each stroke, everyone may say one thing to each neighbour. Round complexity is the number of strokes until everyone has the answer.

News moves one neighbour per stroke, so a person far away needs many strokes to hear from you. That is why the size of the network, measured as the longest shortest route between two people, often sets the cost.

Without a common clock, we ask instead how long the task takes if every message takes at most one unit of time to arrive. Then slow and fast messages both count, and the worst case decides.

## The idea

**Notation and model.** The network is a connected graph with $n$ nodes, $m$ edges, diameter $D$ and largest degree $\Delta$. Unless a page says otherwise, there are no failures, nodes have unique identifiers, and messages go only along edges.

**Synchronous round complexity.** In a synchronous model, an execution is a sequence of rounds; in each one every node sends, receives and computes. The round complexity $T(n)$ of an algorithm is the largest number of rounds, over all graphs in the class with $n$ nodes and over all identifiers, port numberings and inputs, until every node has stopped. Bounds are often given in several parameters, such as $O(D)$, $O(\log^* n)$ or $\tilde{O}(\sqrt{n} + D)$. Some papers count rounds until every node has *output*, even if it keeps sending; usually this changes the bound by at most a constant factor.

**Randomized algorithms.** The round complexity is a bound that holds with high probability, usually at least $1 - 1/n$, or in expectation. Las Vegas algorithms are always correct and have a random running time; Monte Carlo algorithms stop in a fixed number of rounds and may fail with small probability.

**Asynchronous time.** In an asynchronous network there are no rounds. To measure time, assume that each message is delivered within at most one unit of time after it is sent and that local computation takes no time. The *time complexity* is the largest time, over all executions with delays in $[0, 1]$, from the start until all nodes have stopped (Awerbuch 1985; Lynch 1996). The bound is used only for analysis: the algorithm must be correct for every finite delay. Any synchronous algorithm can be run on an asynchronous network with a [synchronizer](/synchronizer/), which turns $T$ rounds into $O(T)$ time at a cost in messages.

**The basic lower bound (proved here).** Call a problem *global* if some node's correct output depends on the input of a node at distance $D$. In every synchronous model where messages move along edges, a node's state after $r$ rounds depends only on the nodes at distance at most $r$ (the [locality theorem](/local-model/)). So every algorithm for a global problem needs at least $D$ rounds on some input. Broadcast, leader election, counting $n$, and spanning tree construction with a [BFS](/breadth-first-search-distributed/) root are global in this sense, so each needs $\Omega(D)$ rounds. The same argument in the asynchronous model, with all delays equal to 1, gives time $\Omega(D)$.

**What can be faster than $D$.** Problems with local correctness conditions, such as colouring, maximal independent sets or matchings, need not wait for distant information. Their round complexity is a function of $n$ and $\Delta$ and can be far below $D$, such as $O(\log^* n)$ for 3-colouring a cycle whose diameter is $n/2$. This is the subject of the [LOCAL](/local-model/) model.

## Examples

| task | model | round complexity | page |
|---|---|---|---|
| broadcast from one node | any synchronous | $\mathrm{ecc}(s) \le D$, optimal | [flooding](/flooding/) |
| broadcast with acknowledgement | synchronous | $2\,\mathrm{ecc}(s)$ or $2\,\mathrm{ecc}(s) + 1$ | [echo algorithm](/echo-algorithm/) |
| broadcast with acknowledgement | asynchronous, delays at most 1 | $O(n)$; the echo tree can have height $n - 1$ | [echo algorithm](/echo-algorithm/) |
| BFS tree | synchronous | $\mathrm{ecc}(r)$ or $\mathrm{ecc}(r) + 1$ | [distributed BFS](/breadth-first-search-distributed/) |
| any solvable problem | LOCAL | at most $D + 1$ | [LOCAL](/local-model/) |
| 3-colouring a cycle | LOCAL | $\Theta(\log^* n)$ | [Cole-Vishkin](/cole-vishkin/), [Linial](/linial-coloring-lower-bound/) |
| MST | CONGEST | $\tilde{\Theta}(\sqrt{n} + D)$ | [distributed MST](/distributed-mst/) |
| diameter | CONGEST | $\tilde{\Theta}(n)$ | [diameter lower bound](/diameter-lower-bound-distributed/) |
| MST | congested clique | $O(1)$, randomized | [congested clique](/congested-clique-model/) |

**Rounds versus asynchronous time.** The echo algorithm shows that the two measures can differ for the same algorithm. In synchronous rounds the echo tree is a BFS tree, of height at most $D$. With delays in $[0, 1]$, an adversary can make messages along a long path arrive first, so the tree, and the time of the echo phase, can grow to $n - 1$ even when $D = 1$. A synchronizer or a layered construction restores $O(D)$ time.

**Rounds versus messages.** Flooding needs $D$ rounds and $\Theta(m)$ messages. A depth-first token that knows the identifiers of the neighbours needs $2(n-1)$ rounds and $2(n-1)$ messages. Which is better depends on the measure; see [message complexity](/message-complexity/) for the count.

## Where it is used

- **Comparing distributed algorithms.** Round complexity is the first number given for algorithms in LOCAL, CONGEST and the congested clique, and lower bounds such as [Linial's](/linial-coloring-lower-bound/), [KMW](/kmw-lower-bound/) and the [CONGEST lower bounds](/peleg-rubinovich-lower-bound/) are statements about it.
- **Locality.** In LOCAL, an algorithm of $r$ rounds is the same as a function of radius-$r$ neighbourhoods, so round complexity measures how local a problem is. This links distributed computing to [locally checkable labellings](/locally-checkable-labeling/), local computation algorithms and parallel algorithms.
- **Parallel and BSP computing.** The number of supersteps of a [BSP](/bsp-model/) or [Pregel](/pregel-model/) program and the number of rounds of MPC are round complexities of the same kind, and the techniques move between them.
- **Asynchronous systems.** Time with unit delays bounds latency in real networks, and synchronizers translate between rounds and time.

## References
