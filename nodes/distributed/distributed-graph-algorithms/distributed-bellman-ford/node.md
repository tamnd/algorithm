---
tag: FVKNH6
kind: algorithm
slug: distributed-bellman-ford
name: Distributed Bellman-Ford
aliases:
- distributed shortest paths via Bellman-Ford
- synchronous Bellman-Ford
area: distributed/distributed-graph-algorithms
level: core
summary: Nodes send their distance estimates to their neighbours and relax them. Synchronous rounds give exact distances after n - 1 rounds; asynchronous runs can need exponentially many messages.
solves: [distributed-shortest-paths]
model: synchronous-model
complexity:
  vars: {n: the number of nodes, m: the number of edges}
  time: {worst: O(n)}
  messages: {worst: O(n m)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 1958
  people: [Richard Bellman, Lester R. Ford Jr.]
  note: The sequential method is from Ford (1956) and Bellman (1958). Its distributed form ran in the ARPANET routing of 1969 and later in RIP.
prereqs: [bellman-ford, edge-relaxation, synchronous-model, asynchronous-model, congest-model]
see_also: [distributed-shortest-paths, distance-vector-routing, count-to-infinity, breadth-first-search-distributed, distributed-approximate-sssp, distributed-apsp, shortest-path-tree, dijkstra]
sources:
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Section 4.3 (BellmanFord in the synchronous model, n - 1 rounds) and Section 15.4 (AsynchBellmanFord and its exponential message count)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, second edition, Wiley, 2004
    locator: Chapter 2 (the synchronous and asynchronous message-passing models and the complexity measures)
  - book: isbn:9780521794831
    title: Gerard Tel, Introduction to Distributed Algorithms, second edition, Cambridge University Press, 2000
    locator: Chapter 4, Routing algorithms (the distance-vector method and the Netchange algorithm)
---

Distributed Bellman-Ford computes the distances from a source $s$ to every node of a network. Each node holds an estimate of its distance, sends it to its neighbours, and lowers it when a neighbour's estimate plus the edge weight is smaller. In the [synchronous model](/synchronous-model/) it stops after exactly $n - 1$ rounds with the exact distances and a [shortest path tree](/shortest-path-tree/), using $2m(n - 1)$ messages of $O(\log n)$ bits. In the [asynchronous model](/asynchronous-model/) it is still correct, but some schedules make it send exponentially many messages. It is the distributed form of the [Bellman-Ford algorithm](/bellman-ford/) and the base of [distance-vector routing](/distance-vector-routing/).

## In plain words

Each town knows the roads to its neighbour towns and their lengths. The capital is at distance 0. Every other town starts with "I do not know", which counts as infinity.

Once a day, each town tells its neighbours its best known distance to the capital. A town that hears "I am 5 from the capital" from a neighbour 2 km away knows a way of length 7. If 7 is better than its own number, it takes 7 and remembers that neighbour as the next step.

After one day, the towns next to the capital know a correct route of one road. After $k$ days, every town knows its best route of at most $k$ roads. No shortest route needs more than $n - 1$ roads, so after $n - 1$ days all numbers are correct.

## The problem

The network is a connected undirected graph $G = (V, E)$ with $n$ nodes, $m$ edges and a weight $w(e) \ge 0$ on each edge. One node $s$ is the source. Each node knows its incident edges and their weights, and it knows $n$ (or an upper bound on it). At the end each node $v$ knows $d(s, v)$, the least weight of a path from $s$ to $v$, and a parent, its neighbour on such a path. This is the [single-source shortest path](/single-source-shortest-paths/) problem in a network; see [distributed shortest paths](/distributed-shortest-paths/) for the problem and its other algorithms.

Notation on this page: $n$ nodes, $m$ edges, $d(s, v)$ the distance, $d_r(v)$ the least weight of a walk from $s$ to $v$ with at most $r$ edges.

## The algorithm

Every node runs the same code. In each round, all nodes send, then all nodes receive, then all nodes compute, so in round $r$ each message carries the estimate from the end of round $r - 1$.

```pseudo id=main
BELLMAN-FORD at node v
L1  dist ← 0 if v = s, else ∞; parent ← nil
L2  for round r ← 1 to n − 1 do
L3      send dist to each neighbour
L4      for each message d received from a neighbour u do
L5          if d + w(u, v) < dist then
L6              dist ← d + w(u, v); parent ← u
L7  output dist and parent
```

The estimate is a sum of at most $n - 1$ weights, so when the weights are polynomial in $n$ it fits in $O(\log n)$ bits, and the algorithm runs in the [CONGEST model](/congest-model/).

**The asynchronous version.** With no rounds, a node sends its estimate to all neighbours at the start (only $s$ has a finite one) and again each time line L6 lowers it. There is no round counter, so it stops when no message is in transit. This is AsynchBellmanFord in Lynch, Section 15.4.

## Example

The graph has 5 nodes and the edges $01{:}4$, $02{:}1$, $21{:}2$, $13{:}1$, $23{:}5$, $34{:}3$ (endpoints and weight). The source is node 0. The table shows the estimates at the end of each round.

| round | node 0 | node 1 | node 2 | node 3 | node 4 |
|---|---|---|---|---|---|
| 0 | 0 | ∞ | ∞ | ∞ | ∞ |
| 1 | 0 | 4 | 1 | ∞ | ∞ |
| 2 | 0 | 3 | 1 | 5 | ∞ |
| 3 | 0 | 3 | 1 | 4 | 8 |
| 4 | 0 | 3 | 1 | 4 | 7 |

In round 2, node 1 hears 1 from node 2 and lowers its estimate to $1 + 2 = 3$, and node 3 hears 4 from node 1 (an old value) and takes $4 + 1 = 5$. In round 3, node 3 hears the new 3 from node 1 and takes 4. Node 4 gets its true distance 7 only in round 4, because the shortest path $0, 2, 1, 3, 4$ has 4 edges. Each row equals the $r$-hop distances $d_r$. The parents are $1 \to 2$, $2 \to 0$, $3 \to 1$, $4 \to 3$. The run sends $4 \cdot 2 \cdot 6 = 48$ messages.

## Correctness

**Invariant.** After round $r$ of the synchronous algorithm, $\text{dist}_v = d_r(v)$ for each node $v$. Round $r$ uses the values $d_{r-1}(u)$ of all neighbours, and $d_r(v) = \min(d_{r-1}(v), \min_u (d_{r-1}(u) + w(u, v)))$, because a walk of at most $r$ edges is either a walk of at most $r - 1$ edges or such a walk to a neighbour $u$ plus one edge. The weights are not negative, so a shortest walk can be made a simple path, which has at most $n - 1$ edges. So $d_{n-1}(v) = d(s, v)$, and the parents form a shortest path tree.

**Asynchronous version.** Each estimate is the weight of some walk from $s$, so it is at least $d(s, v)$. The estimates only go down, and they take values in a finite set, so the run stops. When it stops, each node has received the last estimate of each neighbour, so $\text{dist}_v \le \text{dist}_u + w(u, v)$ for each edge. Along a shortest path from $s$ this gives $\text{dist}_v \le d(s, v)$. The proofs are in [the proof page](proofs/correctness/).

## Complexity

**Synchronous.** Exactly $n - 1$ rounds. In each round each node sends one message on each incident edge, so $2m$ messages per round and $2m(n - 1) = O(nm)$ in total. Each message holds one estimate of $O(\log n)$ bits. A node keeps $O(1)$ words besides its edge list.

The bound $n - 1$ is tight for this code: on a path of $n$ nodes with $s$ at one end, the far end gets a finite estimate only in round $n - 1$. A better stopping rule helps when the graph has few hops: a node may stop sending when its estimate did not change, and the run can stop after $h + 1$ rounds, where $h$ is the largest number of edges on a shortest path. To detect that, the nodes need a [termination detection](/termination-detection/) step, for example a [convergecast](/convergecast/) on a tree.

**Asynchronous.** The number of messages can be exponential in $n$. Take the chain $v_0, \ldots, v_k$ with source $v_0$. Between $v_{j-1}$ and $v_j$ there is a direct edge of weight $2^{k-j}$ and a slow path $v_{j-1}, u_j, v_j$ with two edges of weight 0. The slow paths have delay $3^{k-j+1}$ on each edge, so they are slower the closer they are to the source. The node $v_k$ first hears the all-direct path of weight $2^k - 1$, and each later arrival over a slow path lowers its estimate by exactly 1. So $v_k$ takes all $2^k$ values $2^k - 1, 2^k - 2, \ldots, 0$ in turn, and sends each to its neighbours.

| $k$ | nodes $n = 2k + 1$ | values at $v_k$ | messages (asynchronous) | messages (synchronous) |
|---|---|---|---|---|
| 2 | 5 | 4 | 24 | 48 |
| 4 | 9 | 16 | 120 | 192 |
| 6 | 13 | 64 | 504 | 432 |
| 8 | 17 | 256 | 2040 | 768 |

The asynchronous counts are $2^{k+3} - 8$, which is $2^{\Omega(n)}$, while the synchronous count is $2m(n - 1) = 2 \cdot 3k \cdot 2k = 12k^2$. The time with these delays is also exponential. Lynch, Section 15.4, gives this kind of example.

## Properties

- **Exact after $n - 1$ rounds**, with no knowledge of the graph beyond $n$ and the incident edges.
- **Local rule.** Each step uses only the estimates of the neighbours. This is why the same rule runs in routers as [distance-vector routing](/distance-vector-routing/), with one estimate per destination.
- **Self-stabilizing only in part.** With non-negative weights and correct initial values, it converges. After a link failure, the old estimates can be too low, and the rule only lowers estimates, so it does not recover. The distance-vector rule $\text{dist}_v \leftarrow \min_u (\text{dist}_u + w(u, v))$, which also raises estimates, recovers, but it can count to infinity (see Pitfalls).
- **Negative weights.** On a directed graph with negative weights but no negative cycle, the synchronous version is still correct after $n - 1$ rounds, with messages sent along the edges. An undirected edge of negative weight is a negative cycle.

## Variants and improvements

- **Distributed BFS.** With all weights 1, the algorithm is a [distributed BFS](/breadth-first-search-distributed/), and it can stop after $D$ rounds, where $D$ is the diameter. Each node then sends only once, when it first gets an estimate, so the messages drop to $O(m)$.
- **Distance-vector routing.** Each node keeps one estimate for each destination. This is all-pairs Bellman-Ford; RIP uses it with 16 as infinity. See [distance-vector routing](/distance-vector-routing/).
- **Hop-bounded Bellman-Ford.** Run only $h$ rounds to get $d_h$, the best walk with at most $h$ edges. Together with a [hopset](/hopset/), this is the main step of the fast [approximate SSSP](/distributed-approximate-sssp/) algorithms.
- **Faster exact SSSP.** In CONGEST, Bellman-Ford takes $\Theta(n)$ rounds in the worst case even when $D$ is small. Algorithms with $\tilde{O}(\sqrt{n} D^{1/4} + D)$ rounds and better exist; see [distributed shortest paths](/distributed-shortest-paths/).

## When to use it

Use the synchronous version when the network is small, or when the shortest paths have few hops and a termination check is available. Its code is short, it needs only local information, and it sends messages of one number. Use the asynchronous version only with care: it is correct, but its message count has no polynomial bound. A [synchronizer](/synchronizer/) turns the synchronous version into an asynchronous one with $O(nm)$ messages plus the cost of the synchronizer. For large networks with small diameter, use a $\tilde{O}(\sqrt{n} + D)$ approximate method instead.

## Pitfalls

- **Count to infinity.** In the chain $s$, $A$, $B$ with unit weights, $A$ is at distance 1 and $B$ at distance 2. If the link $s$ to $A$ fails, $A$ uses the distance-vector rule and sees only $B$, which still claims 2, so $A$ takes 3. Then $B$ takes 4, $A$ takes 5, and so on. After round $r$ the two estimates are $r + 1$ and $r + 2$. They never stop if infinity is a true infinity, and they take $K - 1$ rounds to reach a cap $K$, as RIP does with $K = 16$. Split horizon and poisoned reverse avoid this two-node loop, but not longer loops. See [count to infinity](/count-to-infinity/).
- **Stopping too early.** Stopping a node when its estimate does not change in one round is wrong: node 4 of the example keeps ∞ in rounds 1 and 2, and only then gets 8 and 7.
- **Using new values in the same round.** If a node uses an estimate that a neighbour computed in the same round, the result depends on the order of the nodes, and the invariant $\text{dist}_v = d_r(v)$ fails. The final answer is still right, but the round count is no longer predictable.
- **Asynchronous message blow-up.** Do not assume that the asynchronous version sends $O(nm)$ messages. The chain above makes it send $2^{\Omega(n)}$.

## Implementations

## History

Ford (1956) and Bellman (1958) gave the sequential method, and Moore (1959) a similar one. The distributed form ran in the routing of the ARPANET from 1969, where each node sent its distance table to its neighbours, and the count-to-infinity problem appeared there. The ARPANET moved to a link-state method in 1979 for this reason. RIP (1988) is still a distance-vector protocol. Lynch's book (1996) gives the synchronous version with its $n - 1$ round bound, and the asynchronous version with its exponential worst case.

## References
