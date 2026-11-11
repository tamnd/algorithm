---
tag: NAT4P4
kind: concept
slug: message-complexity
name: Message complexity
aliases:
- number of messages
- bit complexity
area: distributed/distributed-graph-algorithms
level: intro
summary: The total number of messages that a distributed algorithm sends, in the worst case over inputs and schedules. It trades against time; flooding is fast with many messages, a token is slow with few.
prereqs: [synchronous-model, asynchronous-model]
see_also: [round-complexity, broadcast-problem, flooding, depth-first-search, gallager-humblet-spira, ring-election-lower-bound, congest-model, synchronizer]
sources:
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 2 (communication complexity as the number of messages), Chapter 3 (leader election in a synchronous ring, the TimeSlice algorithm and the comparison-based lower bound)
  - book: isbn:9780898714647
    title: David Peleg, Distributed Computing, A Locality-Sensitive Approach, SIAM, 2000
    locator: Chapter 2 (message and bit complexity) and Chapter 3 (the message cost of broadcast and convergecast)
  - paper: doi:10.1145/77600.77618
    title: Baruch Awerbuch, Oded Goldreich, David Peleg and Ronen Vainish, A trade-off between information and communication in broadcast protocols, Journal of the ACM 37(2), 238-256, 1990
    locator: the dependence of the message cost of broadcast on what nodes know about their neighbourhood, with the Omega(m) lower bound in the restricted setting
  - paper: doi:10.1145/2699440
    title: Shay Kutten, Gopal Pandurangan, David Peleg, Peter Robinson and Amitabh Trehan, On the complexity of universal leader election, Journal of the ACM 62(1), article 7, 2015
    locator: the Omega(m) message lower bound for leader election and broadcast in KT0, also for randomized algorithms, the Omega(D) time bound, and algorithms that come close to both bounds
  - paper: doi:10.1145/357195.357200
    title: Robert G. Gallager, Pierre A. Humblet and Philip M. Spira, A distributed algorithm for minimum-weight spanning trees, ACM Transactions on Programming Languages and Systems 5(1), 66-77, 1983
    locator: the MST algorithm with at most 5 n log2 n + 2 m messages
---

The message complexity of a distributed algorithm is the total number of messages it sends, over all nodes and all edges, in the worst case. It measures the work of the network, while [round complexity](/round-complexity/) measures time, and the two often trade against each other. When messages may be large, one also counts the *bit complexity*, the total number of bits. Lower bounds are stated in the parameters $n$, $m$, $D$ and $\Delta$, and usually $\Omega(n)$ or $\Omega(m)$ messages are needed for global tasks. The alias "communication complexity" is common in the distributed literature, but it should not be confused with two-party communication complexity, which counts bits between two players and is used to prove [CONGEST](/congest-model/) round lower bounds.

## In plain words

Think of a group of people who pass notes along fixed links. Message complexity counts how many notes they pass in total until the task is done.

One way to spread news is to have everyone pass it to every neighbour at once. It is fast, but many notes cross each link. Another way is to pass a single token around, one person at a time, with a list of who has already seen it. It uses few notes, but it is slow.

So a method can save notes or save time, and often not both. Message complexity is the count of notes, in the worst case.

## The idea

**Notation and model.** A connected network with $n$ nodes, $m$ edges, diameter $D$ and largest degree $\Delta$; reliable channels and no failures. Nodes have unique identifiers. In *KT0* a node knows only its ports at the start; in *KT1* it knows the identifiers of its neighbours. Both synchronous and asynchronous timing are used, and the page says which.

**Definition.** For a deterministic algorithm, the message complexity is the largest number of messages sent in any execution, over all graphs of the class, identifiers, inputs and, in asynchronous models, all delivery schedules. For randomized algorithms, a bound that holds with high probability or in expectation. A message of the [CONGEST](/congest-model/) model has $O(\log n)$ bits, so there the message and bit complexities differ by a factor of $O(\log n)$ at most.

**The trivial lower bound.** In a broadcast from one node, every other node must receive at least one message, so $n - 1$ messages are needed. Whether $\Omega(m)$ messages are needed depends on knowledge: in KT0 every algorithm needs $\Omega(m)$ (Kutten et al. 2015, also for randomized algorithms; a simple deterministic proof is on the [broadcast page](/broadcast-problem/)), but in KT1 there are broadcast algorithms with $o(m)$ messages.

**The trade-off with time (proved here).** Take synchronous broadcast from a node $s$ in KT1.

- *Flooding.* $s$ sends to all its neighbours in round 1, and every other node, in the round after it first hears the message, sends to all neighbours except the one it heard from first. Each node sends once, so the count is $\deg(s) + \sum_{v \ne s} (\deg(v) - 1) = 2m - n + 1$. The time is $\mathrm{ecc}(s) \le D$ rounds.
- *Depth-first token.* A single token carries the set of visited identifiers. A node that holds it sends it to one neighbour that is not in the set, or, if there is none, back to the node it first got the token from. Each tree edge of the depth-first tree carries the token exactly twice, once down and once back, and no other edge carries it, because the sender knows the identifiers behind its ports and skips visited nodes. So the count is $2(n - 1)$ messages, and the time is $2(n - 1)$ rounds.

On the complete graph $K_n$, flooding uses $(n-1) + (n-1)(n-2) = (n-1)^2$ messages in 2 rounds (and the first round alone informs everyone), while the token uses $2(n-1)$ messages in $2(n-1)$ rounds. The token's messages carry up to $n$ identifiers, so its bit complexity is $O(n^2 \log n)$; in CONGEST it would be split into $O(n)$ messages per hop.

**Extreme trade-offs.** In a synchronous ring with known $n$, the TimeSlice algorithm (Lynch 1996, Chapter 3) elects the node with the smallest identifier $u_{\min}$ with only $n$ messages: in phase $i$, which lasts $n$ rounds, the node with identifier $i$ starts a token, if it exists. The time is about $n \cdot u_{\min}$ rounds, not bounded by any function of $n$. Algorithms that only compare identifiers need $\Omega(n \log n)$ messages on a synchronous ring (Frederickson and Lynch 1987), so the use of identifiers as numbers, which TimeSlice makes, buys the saving with time.

## Examples

| task | model | messages | time | page |
|---|---|---|---|---|
| broadcast by flooding | any | $2m - n + 1$, since each node sends once | $D$ | [flooding](/flooding/) |
| broadcast by DFS token | KT1 | $2(n - 1)$ | $2(n - 1)$ | [depth-first search](/depth-first-search/) |
| broadcast | KT0 | $\Omega(m)$ for every algorithm | | [broadcast](/broadcast-problem/) |
| broadcast with acknowledgement | any | $2m$ | $O(D)$ synchronous | [echo algorithm](/echo-algorithm/) |
| aggregate on a known tree | any | $n - 1$ | height of the tree | [convergecast](/convergecast/) |
| leader election in a ring | asynchronous | $\Theta(n \log n)$ | $O(n)$ | [ring election lower bound](/ring-election-lower-bound/) |
| leader election, general graph | KT0 | $\Omega(m)$, nearly matched | $\Omega(D)$, nearly matched | Kutten et al. 2015 |
| MST | asynchronous | $O(m + n \log n)$ | $O(n \log n)$ | [GHS](/gallager-humblet-spira/) |
| synchronous algorithm with $M$ messages and $T$ rounds, on an asynchronous network | asynchronous | $O(M + mT)$ with synchronizer $\alpha$ | $O(T)$ | [synchronizer](/synchronizer/) |
| termination detection of a diffusing computation with $B$ messages | asynchronous | $B$ control messages | $O(n)$ after termination | [Dijkstra-Scholten](/dijkstra-scholten/) |

## Where it is used

- **Energy and bandwidth.** In sensor and wireless networks every transmission costs energy, and in shared networks every message uses capacity, so algorithms with few messages are preferred even when they are slower.
- **Lower bounds.** Message lower bounds such as $\Omega(n \log n)$ on rings and $\Omega(m)$ in KT0 show which savings are impossible, and they often use the same indistinguishability arguments as round lower bounds.
- **Overhead of control layers.** Synchronizers, [termination detection](/termination-detection/) and snapshots add control messages, and their cost is stated as a message complexity relative to the basic algorithm.
- **Parallel graph systems.** In [Pregel](/pregel-model/) and other vertex-centric systems, the number of messages per superstep sets the network load, so the same counting applies.

## References
