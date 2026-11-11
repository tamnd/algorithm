---
tag: XE692K
kind: problem
slug: distributed-shortest-paths
name: Distributed single-source shortest paths
aliases:
- distributed SSSP
- distributed shortest path problem
area: distributed/distributed-graph-algorithms
level: core
summary: Every node of a weighted network learns its distance to a source and its next hop. Exact SSSP in CONGEST takes between about √n + D and n^(2/5) D^(2/5) + √n + D rounds.
model: congest-model
complexity:
  vars: {n: the number of nodes, D: the hop diameter}
  time: {worst: Ω(n^(1/2)/log n + D)}
prereqs: [single-source-shortest-paths, congest-model, distributed-bellman-ford, breadth-first-search-distributed, round-complexity]
see_also: [distributed-approximate-sssp, distributed-apsp, distributed-bellman-ford, peleg-rubinovich-lower-bound, hopset, distributed-mst, dijkstra, distance-vector-routing]
sources:
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Section 4.3 (BellmanFord, the synchronous algorithm) and Section 15.4 (AsynchBellmanFord)
  - paper: doi:10.1137/11085178X
    title: Atish Das Sarma, Stephan Holzer, Liah Kor, Amos Korman, Danupon Nanongkai, Gopal Pandurangan, David Peleg and Roger Wattenhofer, Distributed verification and hardness of distributed approximation, SIAM Journal on Computing 41(5), 2012
    locator: pages 1235 to 1265, the lower bound for approximate shortest s-t paths of any polynomial ratio
  - paper: doi:10.1145/3055399.3055452
    title: Michael Elkin, Distributed exact shortest paths in sublinear time, STOC 2017
    locator: pages 757 to 770, the first sublinear exact SSSP algorithm
  - paper: doi:10.1145/3188745.3188948
    title: Mohsen Ghaffari and Jason Li, Improved distributed algorithms for exact shortest paths, STOC 2018
    locator: the Õ(n^(3/4) D^(1/4)) bound
  - paper: "Sebastian Forster and Danupon Nanongkai, A faster distributed single-source shortest paths algorithm, FOCS 2018"
    locator: the Õ((nD)^(1/2)) and Õ(n^(1/2) D^(1/4) + n^(3/5) + D) bounds
  - paper: doi:10.1145/3382734.3405729
    title: Shiri Chechik and Doron Mukhtar, Single-source shortest paths in the CONGEST model with improved bound, PODC 2020
    locator: pages 464 to 473, the Õ(n^(1/2) D^(1/4) + D) bound
  - paper: "Nairen Cao and Jeremy T. Fineman, Parallel exact shortest paths in almost linear work and square root depth, SODA 2023"
    locator: pages 4354 to 4372, the distributed corollary with Õ(n^(2/5+o(1)) D^(2/5) + n^(1/2) + D) rounds
  - paper: doi:10.1145/3564246.3585235
    title: Václav Rozhoň, Bernhard Haeupler, Anders Martinsson, Christoph Grunau and Goran Zuzic, Parallel breadth-first search and exact shortest paths and stronger notions for approximate distances, STOC 2023
    locator: pages 321 to 334, the reduction from exact to approximate directed distances
  - paper: doi:10.1145/3519935.3520074
    title: Václav Rozhoň, Christoph Grunau, Bernhard Haeupler, Goran Zuzic and Jason Li, Undirected (1+ε)-shortest paths via minor-aggregates, STOC 2022
    locator: pages 478 to 487, deterministic (1+ε)-approximate SSSP from minor aggregations
---

In the distributed single-source shortest paths problem (SSSP), the nodes of a weighted network compute their distances from one source node $s$. Each node knows only the weights of its own edges, and at the end each node knows its distance $d(s, v)$ and the neighbour that comes next on a shortest path back to $s$. In the [CONGEST model](/congest-model/), [distributed Bellman-Ford](/distributed-bellman-ford/) solves the problem in $n - 1$ rounds. No algorithm can use fewer than about $\sqrt{n} + D$ rounds, where $D$ is the hop diameter. Since Elkin (2017), exact algorithms with a sublinear number of rounds are known, and the best ones take $\tilde{O}(n^{2/5 + o(1)} D^{2/5} + \sqrt{n} + D)$ rounds. The approximate version is on the page [distributed approximate SSSP](/distributed-approximate-sssp/).

## In plain words

Computers in a network are joined by cables, and each cable has a length. One computer is the source. Each computer must learn how far it is from the source along the shortest route, and which neighbour to send a packet to so that the packet reaches the source.

No computer sees the whole network, and each cable carries one small message in each round. The simple method passes improved distances to the neighbours until nothing changes. A shortest route can have almost $n$ cables, so the simple method can take almost $n$ rounds, even when every computer is only a few cables away from the source. Fast methods use a few far jumps to cut long routes into short pieces.

## Definition

**Input.** A connected undirected graph $G = (V, E)$ with $n$ nodes and $m$ edges, a weight $w(e) \ge 0$ on each edge, and a source $s \in V$. Each node has a unique identifier of $O(\log n)$ bits and knows the weights of its own edges. The source knows that it is the source. The weights are integers in $\{0, 1, \ldots, W\}$ with $W = n^{O(1)}$, so that one weight fits in one message.

**Output.** Each node $v$ outputs $\text{dist}_v = d(s, v)$, the least weight of a path from $s$ to $v$, and $\text{parent}_v$, a neighbour $u$ with $d(s, v) = d(s, u) + w(u, v)$ (none for $s$). The parent edges then form a [shortest path tree](/shortest-path-tree/) rooted at $s$.

**Cost.** The main measure is the number of synchronous rounds. In each round, each edge carries one message of $O(\log n)$ bits in each direction. The *hop diameter* $D$ is the diameter of $G$ when all weights are 1. It is a lower bound on the rounds for any problem that needs information from the far side of the network.

The distance $d(s, v)$ uses the weights, but the cost of communication uses hops. This mismatch is the core of the problem: a shortest path can have $\Theta(n)$ edges in a graph of hop diameter 2.

## Variants

- **Unweighted SSSP.** With all weights 1, SSSP is a BFS from $s$ and takes $O(D)$ rounds. See [distributed BFS](/breadth-first-search-distributed/).
- **Approximate SSSP.** Each node outputs $\widetilde{d}(v)$ with $d(s, v) \le \widetilde{d}(v) \le (1 + \epsilon) d(s, v)$. This is easier: $\tilde{O}(\sqrt{n} + D)$ rounds suffice. See [distributed approximate SSSP](/distributed-approximate-sssp/).
- **Directed graphs.** The weights and the paths are directed, but each link still carries messages in both directions. Most of the recent exact algorithms work in this setting, and $D$ is the hop diameter of the underlying undirected graph.
- **Many sources.** With $k$ sources, or all $n$ nodes as sources, the problem is $k$-source shortest paths or [all-pairs shortest paths](/distributed-apsp/). APSP needs $\tilde{\Omega}(n)$ rounds.
- **The LOCAL model.** With messages of any size, all nodes can send their edges to $s$ in $O(D)$ rounds. Then $s$ runs [Dijkstra's algorithm](/dijkstra/) and sends the answers back. So the problem is only hard because of the limit on the message size.
- **The asynchronous model.** The asynchronous Bellman-Ford algorithm is always correct, but it can send exponentially many messages. See [distributed Bellman-Ford](/distributed-bellman-ford/).
- **The congested clique.** Every pair of nodes can talk directly. Exact SSSP there is easier than in CONGEST, and $(1 + \epsilon)$-approximate SSSP takes polylogarithmic rounds (Becker et al., 2017).

## Examples

**A hub defeats the hop diameter.** Take a path $v_0, v_1, \ldots, v_{n-2}$ with weight 1 on each edge, and a hub $h$ joined to each $v_i$ by an edge of weight $n$. The source is $s = v_0$. Each pair of nodes is at most 2 hops apart through the hub, so $D = 2$. But each path through the hub costs at least $n$, while $d(s, v_i) = i \le n - 2$. So the shortest path to $v_{n-2}$ is the path itself, with $n - 2$ edges.

[Bellman-Ford](/distributed-bellman-ford/) needs $n - 2$ rounds here, because after round $r$ each node knows only the best paths with at most $r$ edges. The hop diameter is 2, so the gap between $O(D)$ and $\Theta(n)$ is as large as possible. An algorithm with $o(n)$ rounds must send information about the path to far places through the hub, and the hub edges have limited bandwidth. This is the tension that the lower bound makes exact.

**A small run of Bellman-Ford.** The page [distributed Bellman-Ford](/distributed-bellman-ford/) traces the synchronous algorithm on a graph of 5 nodes. The estimates after each round are the shortest distances over at most $r$ hops, and the final values appear after round 4.

## Known algorithms

**Exact SSSP in CONGEST.** All bounds are in rounds and hide polylogarithmic factors.

| algorithm | year | rounds | notes |
|---|---|---|---|
| [Bellman-Ford](/distributed-bellman-ford/) | 1958 | $O(n)$ | deterministic and simple; also correct when asynchronous |
| Elkin, STOC 2017 | 2017 | $\tilde{O}(n^{5/6})$ for $D \le \sqrt{n}$, $\tilde{O}(n^{2/3} D^{1/3})$ for larger $D$ | the first sublinear exact algorithm |
| Ghaffari and Li, STOC 2018 | 2018 | $\tilde{O}(n^{3/4} D^{1/4})$ | also $n^{3/4 + o(1)} + \min(n^{3/4} D^{1/6}, n^{6/7}) + D$ |
| Forster and Nanongkai, FOCS 2018 | 2018 | $\tilde{O}(\sqrt{n D})$ or $\tilde{O}(\sqrt{n} D^{1/4} + n^{3/5} + D)$ | randomized |
| Chechik and Mukhtar, PODC 2020 | 2020 | $\tilde{O}(\sqrt{n} D^{1/4} + D)$ | randomized; also for directed graphs |
| Cao and Fineman, SODA 2023; Rozhoň et al., STOC 2023 | 2023 | $\tilde{O}(n^{2/5 + o(1)} D^{2/5} + \sqrt{n} + D)$ | directed graphs; exact from approximate |

**Approximate SSSP in CONGEST.** The details are on the page [distributed approximate SSSP](/distributed-approximate-sssp/).

| algorithm | year | ratio | rounds |
|---|---|---|---|
| Nanongkai, STOC 2014 | 2014 | $1 + o(1)$ | $\tilde{O}(\sqrt{n} D^{1/4} + D)$, randomized |
| Henzinger, Krinninger and Nanongkai, STOC 2016 | 2016 | $1 + o(1)$ | $n^{1/2 + o(1)} + D^{1 + o(1)}$, deterministic |
| Becker, Karrenbauer, Krinninger and Lenzen, DISC 2017 | 2017 | $1 + \epsilon$ | $\tilde{O}((\sqrt{n} + D)\, \epsilon^{-O(1)})$, deterministic |
| Rozhoň, Grunau, Haeupler, Zuzic and Li, STOC 2022 | 2022 | $1 + \epsilon$ | $\tilde{O}(\sqrt{n} + D)$ for constant $\epsilon$, deterministic |

**The common plan of the sublinear exact algorithms.** This is a sketch, not the algorithm of one paper.

1. Sample a set $S$ of about $\sqrt{n}$ *skeleton* nodes, with $s \in S$. Then with high probability each shortest path has a node of $S$ in each run of about $\sqrt{n} \log n$ consecutive edges.
2. Run Bellman-Ford from all nodes of $S$ for $h \approx \sqrt{n} \log n$ hops. This gives the $h$-hop distances between the skeleton nodes. This step is the expensive one, because many Bellman-Ford runs share each edge.
3. Solve SSSP on the small *skeleton graph* on $S$, with these distances as edge weights. The skeleton graph can have $|S|^2 \approx n$ edges, so to send all of it over a BFS tree takes $O(n + D)$ rounds, which is too slow. The papers solve this step with a hopset, a recursion or an approximate method.
4. Each node $v$ sets $d(s, v) = \min_{x \in S} (d(s, x) + d_h(x, v))$.

The papers differ in how they do steps 2 and 3 with fewer rounds. They use different sample sizes, [hopsets](/hopset/), scaling of the weights, and the BFS tree to send the skeleton data.

## Bounds

**Lower bound.** Each algorithm for SSSP needs $\Omega(D)$ rounds, because the farthest node must hear from $s$. Elkin (STOC 2004) and Das Sarma et al. (SIAM J. Comput. 2012) proved that even approximate SSSP, with any polynomial ratio, needs $\Omega(\sqrt{n}/\log n + D)$ rounds on some graphs, also for randomized algorithms. The proof uses the graphs of the [Peleg-Rubinovich lower bound](/peleg-rubinovich-lower-bound/) and a reduction from two-party [set disjointness](/disjointness-problem/). So $\tilde{\Omega}(\sqrt{n} + D)$ rounds are needed for exact and for approximate SSSP.

**Upper bounds.** For approximate SSSP, the gap is closed: $\tilde{O}(\sqrt{n} + D)$ rounds suffice for a constant $\epsilon$. For exact SSSP, the best bound $\tilde{O}(n^{2/5 + o(1)} D^{2/5} + \sqrt{n} + D)$ matches the lower bound when $D \le n^{1/4}$, up to the $n^{o(1)}$ factor. For larger $D$ the gap is still open.

**Messages.** Bellman-Ford sends $2m$ messages in each round, so $O(mn)$ in all. A BFS tree alone needs $\Omega(m)$ messages in the worst case.

## Reductions

- **Unweighted SSSP is BFS.** Replace an edge of integer weight $w$ by a path of $w$ edges, and run BFS. This is correct, but the number of rounds grows with the distances, so it helps only when the weights are small.
- **From verification.** Das Sarma et al. reduce the question "are $s$ and $t$ joined in the subgraph $H$?" to approximate shortest paths: give weight 1 to each edge of $H$ and a weight much larger than $n$ times the ratio to the other edges. Then an approximation of the $s$-$t$ distance within the ratio shows whether $s$ and $t$ are joined in $H$.
- **Exact from approximate.** Rozhoň et al. (STOC 2023) show that in directed graphs an algorithm for strongly $(1 + \epsilon)$-approximate distances gives exact distances at almost no extra cost. The bound of Cao and Fineman uses this kind of step.
- **To APSP.** SSSP from every node gives APSP, and APSP gives the [diameter](/distributed-diameter/). In CONGEST these problems need $\tilde{\Omega}(n)$ rounds, far more than SSSP.

## Applications

- **Routing tables.** The parent pointer of each node is its next hop toward $s$. Repeated for each destination, this is the [distance vector routing](/distance-vector-routing/) of RIP and the early ARPANET.
- **Diameter and radius estimates.** One SSSP from any node $s$ gives $\max_v d(s, v)$, which is between half the weighted diameter and the weighted diameter.
- **Building blocks.** SSSP and its approximations are steps in distributed algorithms for [min cut](/distributed-min-cut/), [max flow](/distributed-max-flow/), low-stretch trees and [network decompositions](/low-diameter-decomposition/).

## References
