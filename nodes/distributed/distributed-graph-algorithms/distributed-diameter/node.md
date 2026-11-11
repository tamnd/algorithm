---
tag: 5JD8RM
kind: problem
slug: distributed-diameter
name: Distributed network diameter
aliases:
- distributed diameter computation
- distributed eccentricity
area: distributed/distributed-graph-algorithms
level: advanced
summary: The nodes compute the largest hop distance in their network. Exact takes Θ(n) rounds in CONGEST up to a log factor, a 3/2-approximation O((n log n)^(1/2) + D), and a 2-approximation O(D).
model: congest-model
complexity:
  vars: {n: the number of nodes, D: the hop diameter}
  time: {worst: O(n)}
prereqs: [distributed-apsp, breadth-first-search-distributed, convergecast, congest-model, tree-diameter]
see_also: [diameter-lower-bound-distributed, distributed-apsp, network-diameter-estimation, breadth-first-search-distributed, distributed-shortest-paths, distributed-approximate-sssp, convergecast, tree-diameter]
sources:
  - paper: "Stephan Holzer and Roger Wattenhofer, Optimal distributed all pairs shortest paths and applications, PODC 2012"
    locator: pages 355 to 364, APSP and the exact diameter in O(n) rounds
  - paper: "David Peleg, Liam Roditty and Elad Tal, Distributed algorithms for network diameter and girth, ICALP 2012"
    locator: the O(n) algorithm for the exact diameter, and the earlier 3/2-approximation
  - paper: "Stephan Holzer, David Peleg, Liam Roditty and Roger Wattenhofer, Distributed 3/2-approximation of the diameter, DISC 2014"
    locator: brief announcement, pages 562 to 564, the O((n log n)^(1/2) + D) algorithm
  - paper: "Liam Roditty and Virginia Vassilevska Williams, Fast approximation algorithms for the diameter and radius of sparse graphs, STOC 2013"
    locator: the sequential estimator with floor(2D/3) <= estimate <= D
  - paper: doi:10.1137/1.9781611973099.91
    title: Silvio Frischknecht, Stephan Holzer and Roger Wattenhofer, Networks cannot compute their diameter in sublinear time, SODA 2012
    locator: pages 1150 to 1162, the Ω(n/log n) lower bound for the exact diameter
  - paper: "Amir Abboud, Keren Censor-Hillel and Seri Khoury, Near-linear lower bounds for distributed distance computations, even in sparse networks, DISC 2016"
    locator: Theorem 1.2, Ω(n/log^3 n) rounds for a (3/2 - ε)-approximation; arXiv 1605.05109
  - paper: "Monika Henzinger, Sebastian Krinninger and Danupon Nanongkai, A deterministic almost-tight distributed algorithm for approximating single-source shortest paths, STOC 2016"
    locator: the abstract, a (2 + o(1))-approximation of the weighted diameter in n^(1/2+o(1)) + D^(1+o(1)) rounds; arXiv 1504.07056
---

In the distributed diameter problem, the nodes of a network compute its diameter $D$: the largest number of hops on a shortest path between two nodes. Often each node also computes its *eccentricity*, its largest distance to another node. The node that runs the algorithm is a part of the graph that it measures. In the [CONGEST model](/congest-model/), the exact diameter takes $O(n)$ rounds, through [all-pairs shortest paths](/distributed-apsp/), and the [diameter lower bound](/diameter-lower-bound-distributed/) shows that $\Omega(n/\log n)$ rounds are needed even when $D$ is a small constant. Approximation helps: one BFS gives a 2-approximation in $O(D)$ rounds, and a $3/2$-approximation takes $O(\sqrt{n \log n} + D)$ rounds (Holzer, Peleg, Roditty and Wattenhofer, 2014). Any ratio below $3/2$ again needs near-linear rounds.

This page is about a network that measures itself in rounds of communication. The page [network diameter estimation](/network-diameter-estimation/) covers the same quantity from the side of measurement and sampling, and [tree diameter](/tree-diameter/) is the sequential problem on trees.

## In plain words

The diameter of a network is the number of links on the longest of all shortest routes. Each computer can find its own longest route (its eccentricity) if it knows its distance to every other computer, and then the computers find the largest of these numbers together.

To learn all distances, every computer sends out a wave, and the waves are started one after another so that they do not block each other. This takes about $3n$ rounds. Surprisingly, no method can be much faster, even when every pair of computers is only three links apart.

A rough answer is cheap: the longest route from any one computer is at least half the diameter. An answer within a factor $3/2$ needs waves from only about $\sqrt{n}$ computers.

## Definition

**Input.** A connected undirected graph $G = (V, E)$ with $n$ nodes. Each node has a unique identifier of $O(\log n)$ bits and knows its neighbours. The distance $d(u, v)$ is the number of links on a shortest path.

**Output.** For the exact problem, each node outputs

$$D = \max_{u, v \in V} d(u, v) = \max_{v \in V} \mathrm{ecc}(v), \qquad \mathrm{ecc}(v) = \max_{u \in V} d(u, v).$$

In the *eccentricity* problem, each node $v$ outputs $\mathrm{ecc}(v)$. For an $\alpha$-approximation, each node outputs $\widetilde{D}$ with $D/\alpha \le \widetilde{D} \le D$. Some authors state the $3/2$-approximation as $\lfloor 2D/3 \rfloor \le \widetilde{D} \le D$, which allows the rounding.

**Cost.** The number of synchronous rounds, with one message of $O(\log n)$ bits on each link in each direction in each round. The diameter $D$ is part of the output, so the algorithm cannot use it as a known parameter. The number of rounds of a BFS, about $D$, is a lower bound for every version.

## Variants

- **Eccentricities, radius and center.** The radius is $\min_v \mathrm{ecc}(v)$, and the center is the set of nodes that attain it. All follow from APSP. Abboud, Censor-Hillel and Khoury show near-linear lower bounds for the approximation of the radius and of all eccentricities too.
- **Weighted diameter.** With weights on the links, the diameter is the largest weighted distance. One approximate SSSP gives a factor about 2. Henzinger, Krinninger and Nanongkai (STOC 2016) state a $(2 + o(1))$-approximation in $n^{1/2 + o(1)} + D^{1 + o(1)}$ rounds. See [distributed approximate SSSP](/distributed-approximate-sssp/).
- **The [congested clique](/congested-clique-model/).** All pairs can talk, and the diameter follows from APSP algorithms based on matrix multiplication, with a sublinear number of rounds.
- **The [LOCAL model](/local-model/).** Collect the whole graph in $O(D)$ rounds. The lower bound is about the message size only.

## Examples

**The exact algorithm on a small graph.** Take the graph on 6 nodes with the edges $01, 02, 13, 23, 34, 45$.

| node | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| eccentricity | 4 | 3 | 3 | 2 | 3 | 4 |

So $D = 4$ (the pair $0, 5$), the radius is 2 and the center is node 3. In the simulation of the implementation, the BFS tree takes 8 rounds, the pipelined waves take 17 rounds, the convergecast of the largest eccentricity takes 5 rounds and the broadcast down the tree takes 4 rounds: 34 rounds in all. The BFS from node 0 alone gives $\mathrm{ecc}(0) = 4$, so the 2-approximation is exact here. From node 3 it would give 2, and $2 \le D \le 4$.

**Why one BFS loses a factor 2.** On a path with $2k + 1$ nodes, the middle node has eccentricity $k$, and $D = 2k$. So the bound $\mathrm{ecc}(v) \ge D/2$ is tight.

## Known algorithms

**Exact, in $O(n)$ rounds.** This is the algorithm of the implementation on this page.

1. Build a BFS tree $T$ from a leader, with an echo ($O(D)$ rounds).
2. Run [pipelined BFS](/distributed-apsp/): a token walks $T$ in DFS order, and each node starts its BFS wave when the token first reaches it. By the no-collision lemma of the APSP page, no two waves need the same link in the same round, and all waves end within $3n + D$ rounds.
3. Each node $v$ takes $\mathrm{ecc}(v)$ as the largest distance that it learned.
4. A [convergecast](/convergecast/) on $T$ computes the largest eccentricity at the root, and a broadcast sends it to all nodes ($O(D)$ rounds).

In total, $O(n + D) = O(n)$ rounds. The same steps with the minimum give the radius.

**2-approximation, in $O(D)$ rounds.** Run one BFS from any node $v$ and output $\widetilde{D} = \mathrm{ecc}(v)$, found by a convergecast. By the triangle inequality $d(a, b) \le d(a, v) + d(v, b) \le 2\,\mathrm{ecc}(v)$ for every pair, so $\mathrm{ecc}(v) \le D \le 2\,\mathrm{ecc}(v)$.

**3/2-approximation, in $O(\sqrt{n \log n} + D)$ rounds.** Holzer, Peleg, Roditty and Wattenhofer run the estimator of Roditty and Vassilevska Williams. Let $s = \lceil \sqrt{n \ln n} \rceil$.

1. Sample a set $S$: each node joins with probability about $(\ln n)/s$, so $|S| = \tilde{O}(\sqrt{n})$. Run BFS from each node of $S$.
2. Let $w$ be a node with the largest distance $d(w, S)$ to the set $S$. Run BFS from $w$.
3. Let $N_s(w)$ be the $s$ nodes closest to $w$ (ties broken by identifier). Run BFS from each node of $N_s(w)$.
4. Output $\widetilde{D}$, the largest eccentricity of all the BFS sources.

The algorithm runs $\tilde{O}(\sqrt{n})$ BFS waves. With $k$ sources, a careful schedule finishes $k$ BFS waves in $O(k + D)$ rounds, so the total is $O(\sqrt{n \log n} + D)$ rounds. The implementation on this page computes the estimate with sequential BFS, to check its guarantee.

**Lemma (Roditty and Vassilevska Williams).** If $S$ meets $N_s(w)$, then $\lfloor 2D/3 \rfloor \le \widetilde{D} \le D$.

*Proof.* Each eccentricity is at most $D$, so $\widetilde{D} \le D$. Let $a, b$ be nodes with $d(a, b) = D$, write $D = 3h + z$ with $z \in \{0, 1, 2\}$, and let $T = \lfloor 2D/3 \rfloor$, which is $2h$ for $z \le 1$ and $2h + 1$ for $z = 2$. Assume that $\mathrm{ecc}(w) < T$, else we are done.

*Case 1: $d(w, S) \le h$.* Since $w$ is farthest from $S$, every node is within $h$ of $S$. Take $x \in S$ with $d(a, x) \le h$. Then $\mathrm{ecc}(x) \ge d(x, b) \ge d(a, b) - d(a, x) \ge 2h + z \ge T$.

*Case 2: $d(w, S) > h$.* The set $N_s(w)$ contains a node of $S$, at distance more than $h$ from $w$. So every node at distance at most $h$ from $w$ is in $N_s(w)$, since $N_s(w)$ holds the $s$ closest nodes. We have $d(w, a) \le \mathrm{ecc}(w) \le T - 1$. If $d(w, a) \le h$, then $a \in N_s(w)$, and $\mathrm{ecc}(a) = D$. Else let $w'$ be the node at distance $h$ from $w$ on a shortest path from $w$ to $a$. Then $w' \in N_s(w)$ and $d(w', a) = d(w, a) - h \le T - 1 - h$, so

$$\mathrm{ecc}(w') \ge d(w', b) \ge D - d(w', a) \ge 3h + z - T + 1 + h = 4h + z + 1 - T.$$

This is at least $T$ in each case: for $z = 0$ it is $4h + 1 \ge 2 \cdot 2h$, for $z = 1$ it is $4h + 2 \ge 4h$, and for $z = 2$ it is $4h + 3 \ge 2(2h + 1)$. $\square$

A node joins $S$ with probability $p \approx 3 \ln n / s$, so $S$ misses the $s$ nodes of $N_s(w)$ with probability $(1 - p)^s \le n^{-3}$. The tests check the lemma and how often $S$ meets $N_s(w)$.

**Earlier results.** Before 2014, Holzer and Wattenhofer and, independently, Peleg, Roditty and Tal gave $3/2$-approximations in $O(n^{3/4} + D)$ rounds.

## Bounds

**Exact.** $\Omega(n/\log n)$ rounds, even on graphs of diameter 3, by a reduction from two-party [set disjointness](/disjointness-problem/) with $\Theta(n^2)$ input bits over a cut of $\Theta(n)$ links. See the [diameter lower bound](/diameter-lower-bound-distributed/) for the gadget and the proof. With the $O(n)$ algorithm, the exact diameter has round complexity $\Theta(n)$ up to a log factor.

**Approximate.** A $(3/2 - \epsilon)$-approximation needs $\Omega(n/\log^3 n)$ rounds, even on sparse graphs (Abboud, Censor-Hillel and Khoury, 2016). A $3/2$-approximation takes $O(\sqrt{n \log n} + D)$ rounds, and a 2-approximation $O(D)$ rounds. Every version needs $\Omega(D)$ rounds. So the approximation ratio $3/2$ is a sharp threshold between near-linear and about $\sqrt{n}$ rounds.

## Reductions

- **From APSP.** APSP gives every eccentricity, and a convergecast gives the diameter, in $O(D)$ more rounds.
- **To APSP.** The diameter lower bound is also a lower bound for [APSP](/distributed-apsp/), for the radius and for all eccentricities.
- **From set disjointness.** The lower bound graph encodes the inputs of two players as links on two sides of a small cut. The diameter is small exactly when the two sets are disjoint.
- **From SSSP.** One SSSP or BFS gives the 2-approximation, so the cost of the 2-approximation is the cost of [SSSP](/distributed-shortest-paths/).

## Applications

- **Timeouts and synchronizers.** Many distributed algorithms need an upper bound on $D$ to know how long a flood or a [synchronizer](/synchronizer/) phase must wait. The 2-approximation from one BFS is the usual way to get it.
- **Network analysis.** The diameter, the radius and the center describe how far apart the parts of a network are, for example to place a server at a center node.
- **A model case for lower bounds.** The diameter is the standard example of a problem with a small output that still needs near-linear rounds in CONGEST, unlike [MST](/distributed-mst/) and [SSSP](/distributed-shortest-paths/), which take about $\sqrt{n} + D$.

## References
