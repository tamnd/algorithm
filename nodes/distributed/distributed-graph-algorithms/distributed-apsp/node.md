---
tag: 5J9KE7
kind: problem
slug: distributed-apsp
name: Distributed all-pairs shortest paths
aliases:
- distributed APSP
area: distributed/distributed-graph-algorithms
level: advanced
summary: Every node learns its distance to every other node. Unweighted APSP takes O(n) rounds in CONGEST by pipelined BFS, weighted APSP takes Õ(n), and Ω(n/log n) rounds are needed.
model: congest-model
complexity:
  vars: {n: the number of nodes, m: the number of edges, D: the hop diameter}
  time: {worst: Õ(n)}
  messages: {worst: O(n m)}
prereqs: [all-pairs-shortest-paths, breadth-first-search-distributed, congest-model, distributed-shortest-paths, round-complexity]
see_also: [distributed-diameter, diameter-lower-bound-distributed, distributed-shortest-paths, distributed-approximate-sssp, breadth-first-search-distributed, all-pairs-shortest-paths, distance-vector-routing, congested-clique-model]
sources:
  - paper: "Stephan Holzer and Roger Wattenhofer, Optimal distributed all pairs shortest paths and applications, PODC 2012"
    locator: pages 355 to 364, the APSP algorithm by BFS waves started in DFS order of a BFS tree, and the O(n) bound
  - paper: "David Peleg, Liam Roditty and Elad Tal, Distributed algorithms for network diameter and girth, ICALP 2012"
    locator: the O(n) algorithm for APSP and the diameter in unweighted networks, and the girth
  - paper: "Aaron Bernstein and Danupon Nanongkai, Distributed exact weighted all-pairs shortest paths in near-linear time, STOC 2019"
    locator: the randomized Õ(n) bound for weighted APSP; arXiv 1811.03337
  - paper: doi:10.1145/3055399.3055452
    title: Michael Elkin, Distributed exact shortest paths in sublinear time, STOC 2017
    locator: pages 757 to 770, the weighted APSP bound Õ(n^(5/3))
  - paper: "Chien-Chung Huang, Danupon Nanongkai and Thatchaphol Saranurak, Distributed exact weighted all-pairs shortest paths in Õ(n^(5/4)) rounds, FOCS 2017"
    locator: the Õ(n^(5/4)) bound
  - paper: "Udit Agarwal, Vijaya Ramachandran, Valerie King and Matteo Pontecorvi, A deterministic distributed algorithm for exact weighted all-pairs shortest paths in Õ(n^(3/2)) rounds, PODC 2018"
    locator: the deterministic Õ(n^(3/2)) bound
  - paper: "Danupon Nanongkai, Distributed approximation algorithms for weighted shortest paths, STOC 2014"
    locator: the (1+ε) approximation of APSP in Õ(n/ε) rounds, and the Ω̃(n) lower bound for approximate APSP
  - paper: "Silvio Frischknecht, Stephan Holzer and Roger Wattenhofer, Networks cannot compute their diameter in sublinear time, SODA 2012"
    locator: pages 1150 to 1162, Ω(n/log n) for the diameter, which APSP gives in O(D) more rounds
---

In distributed all-pairs shortest paths (APSP), each node of a network learns its distance to each other node. It is the distributed form of [all-pairs shortest paths](/all-pairs-shortest-paths/), and the "all sources" form of [distributed SSSP](/distributed-shortest-paths/). In the [CONGEST model](/congest-model/), unweighted APSP takes $O(n)$ rounds: start one [BFS](/breadth-first-search-distributed/) from each node, at times chosen so that no two BFS waves ever need the same link in the same round (Holzer and Wattenhofer, PODC 2012; Peleg, Roditty and Tal, ICALP 2012). Weighted APSP takes $\tilde{O}(n)$ rounds (Bernstein and Nanongkai, STOC 2019). A simple counting argument shows that $\Omega(n/\log n)$ rounds are needed, so APSP is solved up to log factors. Unlike SSSP, the bound depends on $n$ and not on the diameter.

## In plain words

Each computer in a network must learn how many links away every other computer is. One way: every computer sends out a wave, "I am $u$, and you are $k$ links from me", and each computer passes each wave on once.

With $n$ waves at the same time, two waves can want the same cable in the same round, and a cable carries one small message in each round. The trick is to start the waves one after another, along a walk over a tree, so that a later wave can never catch up with an earlier one. Then all $n$ waves finish in about $3n$ rounds.

This is the best possible up to a log factor: a computer with only one cable may need to learn about $n$ separate facts, and its one cable brings few of them in each round.

## Definition

**Input.** A connected undirected graph $G = (V, E)$ with $n$ nodes, $m$ edges and hop diameter $D$. In the weighted version each edge has a weight $w(e) \in \{0, 1, \ldots, W\}$ with $W = n^{O(1)}$. Each node has a unique identifier of $O(\log n)$ bits and knows its own edges.

**Output.** Each node $v$ outputs $d(u, v)$ for each $u \in V$, together with the identifier $u$. Often each node also outputs, for each $u$, a neighbour that is next on a shortest path to $u$, so that the outputs form routing tables.

**Cost.** The number of synchronous rounds, with one message of $B = O(\log n)$ bits on each link in each direction in each round.

The output of one node has $\Theta(n \log n)$ bits. This is the main difference from SSSP, where each node outputs one number, and it is why the bounds depend on $n$ and not on $\sqrt{n} + D$.

## Variants

- **Unweighted APSP.** All weights are 1. This is $n$ BFS runs, and it takes $\Theta(n)$ rounds up to a log factor.
- **Weighted APSP.** The weights are integers. Bellman-Ford from each node in turn gives $O(n^2)$ rounds. The bound came down to $\tilde{O}(n)$ (see the table below).
- **Approximate APSP.** Each node learns each distance within a factor $1 + \epsilon$. Nanongkai (STOC 2014) gives $\tilde{O}(n/\epsilon)$ rounds. The lower bound below holds for every ratio, so approximation saves at most log factors.
- **Few sources.** With $k$ sources, the same scheme of BFS waves gives unweighted distances in $O(k + D)$ rounds with a careful schedule. This is the base of the [diameter](/distributed-diameter/) approximations.
- **The [congested clique](/congested-clique-model/).** Every pair of nodes can talk, and APSP is about as hard as matrix multiplication over a semiring. Censor-Hillel et al. (PODC 2015) give $\tilde{O}(n^{1/3})$ rounds for weighted APSP and fewer rounds for the unweighted case.
- **The [LOCAL model](/local-model/).** With messages of any size, collect the graph at all nodes in $O(D)$ rounds.

## Examples

**A trace of pipelined BFS.** Take the graph on 6 nodes with the edges $01, 02, 13, 23, 34, 45$. The root is node 0, and its eccentricity is 4.

- *Phase 1.* The BFS tree from node 0 has the parents $1 \to 0$, $2 \to 0$, $3 \to 1$, $4 \to 3$, $5 \to 4$. The echo of the leaves reaches the root at the end of round 8.
- *Phase 2.* The token walks the tree in DFS order, children by increasing identifier: $0, 1, 3, 4, 5$, then back up to $0$, then $2$. A node starts its wave in the round after the token first arrives, and the token moves on in the next round.

| node | 0 | 1 | 3 | 4 | 5 | 2 |
|---|---|---|---|---|---|---|
| start round of its wave | 9 | 11 | 13 | 15 | 17 | 23 |

From node 5 back to node 2, the token needs five moves ($5 \to 4 \to 3 \to 1 \to 0 \to 2$), so node 2 starts at round 23. Its wave reaches the farthest node, node 5 at distance 3, in round $23 + 3 - 1 = 25$, which is the last round. Node 5 ends with the distances $d(0, 5) = 4$, $d(1, 5) = 3$, $d(2, 5) = 3$, $d(3, 5) = 2$, $d(4, 5) = 1$. The run sends 99 messages: 72 wave messages ($n$ waves, each sent once in each direction over each of the 6 edges), 17 messages in phase 1 and 10 moves of the token. In no round does a link carry two wave messages.

## Known algorithms

**Pipelined BFS (Holzer and Wattenhofer).** The algorithm of the implementation on this page.

1. *Build a BFS tree.* Node 0 (or an elected leader) floods join messages. Each node takes the first sender as its parent and tells it. An echo from the leaves tells the root when the tree $T$ is complete. This takes $O(D)$ rounds.
2. *Walk the tree.* A token starts at the root and walks $T$ in depth-first order. When the token first arrives at a node $v$, then in the next round $v$ starts its BFS wave and holds the token. In the round after that, $v$ passes the token to its next unvisited child, or back to its parent.
3. *BFS waves.* A wave from $u$ is a message $(u, k)$. When a node $x$ first gets a wave of $u$, with the value $k$, it records $d(u, x) = k$ and, in the next round, sends $(u, k + 1)$ to all its neighbours. It ignores later copies of the same wave.
4. *Stop.* Each node knows $n$ and stops when it has heard $n$ waves.

The token message and a wave message can share one link in the same round. Both fit in one message of $O(\log n)$ bits.

**The no-collision lemma.** Let $S_u$ be the round in which $u$ starts its wave. Then for all $u \ne v$:

$$|S_u - S_v| \ge d(u, v) + 1.$$

*Proof.* Let $u$ be visited before $v$. Between $S_u$ and $S_v$, the token walks the tree from $u$ to $v$, one link in each round, and it waits one round at $v$ before $v$ starts. The walk from $u$ to $v$ has at least $d_T(u, v) \ge d(u, v)$ links, so $S_v - S_u \ge d(u, v) + 1$. $\square$

**Lemma (each node gets at most one new wave in each round).** The wave of $u$ first reaches $x$ in round $S_u + d(u, x) - 1$, for $x \ne u$.

*Proof.* By induction on $d(u, x)$, each node at distance $k$ from $u$ first gets the wave of $u$ at the end of round $S_u + k - 1$, with the value $k$. The neighbours of $u$ get it in round $S_u$. A node $x$ at distance $k + 1$ has a neighbour at distance $k$, which forwards in round $S_u + k$, and no neighbour at distance less than $k$, so it cannot get the wave sooner. Now let $u$ start before $v$. By the triangle inequality $d(u, x) \le d(u, v) + d(v, x)$, so

$$S_v + d(v, x) \ge S_u + d(u, v) + 1 + d(v, x) \ge S_u + d(u, x) + 1 > S_u + d(u, x).$$

So the two waves reach $x$ in different rounds. $\square$

**Corollary.** Each node forwards at most one wave in each round, so each link carries at most one wave message in each direction in each round. No wave is ever delayed, and the value $k$ that a node records is its true distance. This holds without any queues or priorities.

**Round bound.** Phase 1 takes at most $2D + 2$ rounds: $D$ for the flood and $D + 2$ for the echo. In phase 2 the token makes one start round at each of the $n$ nodes and at most $2(n - 1)$ moves, so the last wave starts by round $3n - 2$ of phase 2. It reaches all nodes in at most $D - 1$ more rounds. So the total is at most $3n + 3D = O(n)$ rounds. Holzer and Wattenhofer state a tighter count, and the tests check the bound $r_0 + 3n + D - 3$, where $r_0$ is the length of phase 1.

**Weighted APSP.** All bounds are in rounds and hide polylog factors.

| algorithm | year | rounds | notes |
|---|---|---|---|
| Bellman-Ford from each node in turn | classic | $O(n^2)$ | deterministic |
| Elkin, STOC 2017 | 2017 | $\tilde{O}(n^{5/3})$ | randomized |
| Huang, Nanongkai and Saranurak, FOCS 2017 | 2017 | $\tilde{O}(n^{5/4})$ | randomized |
| Agarwal, Ramachandran, King and Pontecorvi, PODC 2018 | 2018 | $\tilde{O}(n^{3/2})$ | deterministic |
| Bernstein and Nanongkai, STOC 2019 | 2019 | $\tilde{O}(n)$ | randomized; optimal up to polylog factors |
| Nanongkai, STOC 2014 | 2014 | $\tilde{O}(n/\epsilon)$ | $(1 + \epsilon)$-approximate |

Why is weighted APSP harder than BFS? A weighted shortest path can have many hops, and a weighted wave cannot simply go one link in each round without later improvements. The algorithms of 2017 to 2019 use a skeleton of sampled nodes, hop-bounded runs from many sources, and a way to schedule the many runs so that they share the links.

## Bounds

**A counting lower bound.** *Each algorithm for unweighted APSP needs at least $(n - 3)/(B + 1)$ rounds on some graphs, where $B$ is the number of bits in one message. With $B = O(\log n)$ this is $\Omega(n/\log n)$.*

*Proof.* Take a leaf $\ell$, a hub $h$, a node $c$, and nodes $u_1, \ldots, u_k$ with $k = n - 3$. The edges are $\{\ell, h\}$ and $\{h, c\}$, and for each $i$ either $\{h, u_i\}$ (if $x_i = 1$) or $\{c, u_i\}$ (if $x_i = 0$), for a string $x \in \{0, 1\}^k$. Then $d(\ell, u_i) = 3 - x_i$. All $2^k$ graphs give node $\ell$ the same input: one edge to $h$. So the output of $\ell$ is a function of the messages that it gets over its one link. In each round the link brings either nothing or a message of at most $B$ bits, which is less than $2^{B + 1}$ choices. So in $r$ rounds the messages can take fewer than $2^{r(B + 1)}$ values. The output of $\ell$ has $2^k$ different correct values, one for each $x$, so $2^{r(B + 1)} \ge 2^k$ and $r \ge k/(B + 1)$. For a randomized algorithm that is correct with probability at least $1/2$ for each $x$, fix the random bits of $\ell$ so that it is correct for at least half of the $2^k$ strings $x$. Then one string of messages gives one output, which is correct for at most one $x$, so $2^{r(B + 1)} \ge 2^{k - 1}$ and $r \ge (k - 1)/(B + 1)$. $\blacksquare$

The same graph with the weights $1$ and $W > \alpha$ instead of the two distances shows that each $\alpha$-approximation of weighted APSP needs $\Omega(n/B)$ rounds, for each $\alpha < W$. Nanongkai (STOC 2014) states the $\tilde{\Omega}(n)$ bound for approximate APSP.

**A lower bound for one number.** The counting argument needs a large output at one node. Frischknecht, Holzer and Wattenhofer (SODA 2012) show that even the [diameter](/distributed-diameter/), a single number, needs $\Omega(n/\log n)$ rounds, on graphs of diameter at most 5. See the [diameter lower bound](/diameter-lower-bound-distributed/). Since APSP gives the diameter in $O(D)$ more rounds, this is a second proof of the APSP bound.

**Messages.** Pipelined BFS sends $2m$ messages for each wave, so $2nm$ in all, plus $O(m)$ for the tree and the token.

## Reductions

- **APSP gives the diameter, the radius and the center.** Each node takes the largest of its $n$ distances as its eccentricity, and a convergecast on the BFS tree finds the largest and the smallest in $O(D)$ rounds. See [distributed diameter](/distributed-diameter/).
- **APSP gives the girth.** Peleg, Roditty and Tal use the BFS waves to find the girth of an unweighted network in $O(n)$ rounds: a wave that comes back to a node by a second route closes a cycle.
- **APSP gives routing tables.** In the wave of $u$, the neighbour that first sent $(u, k)$ to $x$ is a next hop from $x$ to $u$.
- **From set disjointness.** The diameter lower bound reduces two-party [set disjointness](/disjointness-problem/) to the diameter, and so to APSP.

## Applications

- **Routing tables.** The output of APSP is the routing table of each node, as in [distance vector routing](/distance-vector-routing/), but computed in one run instead of by repeated updates.
- **Network analysis.** The diameter, the radius, the center, the girth and the closeness centrality of each node all follow from APSP.
- **A tool for other bounds.** The pipelining of $n$ BFS waves is reused in many CONGEST algorithms, for example the $(3/2)$-approximation of the [diameter](/distributed-diameter/), which runs BFS waves from only $\tilde{O}(\sqrt{n})$ sources.

## References
