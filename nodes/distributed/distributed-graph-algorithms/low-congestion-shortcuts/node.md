---
tag: ZR4C34
kind: concept
slug: low-congestion-shortcuts
name: Low-congestion shortcuts
aliases:
- shortcut graphs
- tree-restricted shortcuts
area: distributed/distributed-graph-algorithms
level: research
summary: For disjoint connected parts of a network, subgraphs that give each part small diameter while each edge serves few parts. Quality c + d bounds MST and min-cut rounds in CONGEST.
prereqs: [congest-model, distributed-mst, boruvka, breadth-first-search-distributed, planar-graph]
see_also: [distributed-mst, peleg-rubinovich-lower-bound, distributed-min-cut, distributed-approximate-sssp, low-diameter-decomposition, network-decomposition, treewidth, graph-genus]
sources:
  - paper: doi:10.1137/1.9781611974331.ch16
    title: Mohsen Ghaffari and Bernhard Haeupler, Distributed algorithms for planar networks II, low-congestion shortcuts, MST, and min-cut, SODA 2016
    locator: pages 202 to 219 (the definition, the O(D + n^(1/2)) shortcuts for general graphs, the O(D log D) shortcuts for planar graphs in Section 3, and MST and min cut from shortcuts)
  - paper: "Bernhard Haeupler, Taisuke Izumi and Goran Zuzic, Low-congestion shortcuts without embedding, PODC 2016"
    locator: pages 451 to 460 (tree-restricted shortcuts, the block parameter, Theorem 1 the construction in Õ(b(D + c)) rounds, Corollary 1 MST in Õ(bD + c) rounds); journal version in Distributed Computing, doi:10.1007/s00446-020-00383-2
  - paper: "Bernhard Haeupler, Taisuke Izumi and Goran Zuzic, Near-optimal low-congestion shortcuts on bounded parameter graphs, DISC 2016"
    locator: pages 158 to 172 (shortcuts for graphs of bounded genus, treewidth and pathwidth)
  - paper: "Mohsen Ghaffari, Near-optimal scheduling of distributed algorithms, PODC 2015"
    locator: Theorem 1.3, the random-delay schedule of many algorithms in O(c + d log n) rounds after O(d log^2 n) rounds of setup
---

A low-congestion shortcut helps the parts of a network talk inside themselves at the same time. Take disjoint connected parts $S_1, \ldots, S_N$ of a network $G$. A shortcut gives each part $S_i$ a subgraph $H_i$ of $G$, so that $G[S_i] \cup H_i$ has small diameter (the *dilation* $d$) while each edge is in few of these subgraphs (the *congestion* $c$). Ghaffari and Haeupler defined them in 2016 and showed that MST and approximate min cut take $\tilde{O}(c + d)$ rounds in [CONGEST](/congest-model/) when good shortcuts can be built. Every graph has shortcuts of quality $O(D + \sqrt{n})$, which matches the [Peleg-Rubinovich lower bound](/peleg-rubinovich-lower-bound/). Planar graphs have shortcuts of quality $O(D \log D)$, so MST there takes $\tilde{O}(D)$ rounds.

## In plain words

Groups of computers in a network each want to find the smallest number in their group. A group that is a long thin chain is slow, because the news walks along the chain one link at a time.

The fix is to let a group borrow links that belong to other groups, as a short cut. But if many groups borrow the same link, they must wait for each other, because each link carries one small message in each round. A good shortcut keeps both numbers small: the longest walk inside each group with its borrowed links, and the number of groups that share any one link. The sum of the two numbers is about the number of rounds that all groups need.

## The idea

**Definition (Ghaffari and Haeupler).** Let $G = (V, E)$ be a graph and let $S_1, \ldots, S_N$ be disjoint subsets of $V$, each of which induces a connected subgraph $G[S_i]$. A $(c, d)$ shortcut is a family of subgraphs $H_1, \ldots, H_N$ of $G$ such that:

1. *Dilation.* For each $i$, the graph $G[S_i] \cup H_i$ has diameter at most $d$.
2. *Congestion.* Each edge $e \in E$ is in at most $c$ of the graphs $G[S_i] \cup H_i$.

The *quality* is $c + d$. A graph family has good shortcuts if each partition of each graph of the family has shortcuts of small quality.

**Why the quality is the right measure.** Suppose that each node of $S_i$ holds a value and all of $S_i$ must learn the minimum. One part alone does this in $O(d)$ rounds by a convergecast and a broadcast on a BFS tree of $G[S_i] \cup H_i$. All parts at once must share edges, and each edge carries the messages of at most $c$ parts. Ghaffari's random-delay schedule runs $N$ algorithms, each of $d$ rounds and with at most $c$ messages on each edge in total, in $O(c + d \log n)$ rounds after a setup of $O(d \log^2 n)$ rounds. So one aggregation step in all parts takes $\tilde{O}(c + d)$ rounds.

**MST from shortcuts.** Run [Borůvka](/boruvka/) as in [distributed MST](/distributed-mst/): the fragments are the parts. In each phase, each fragment finds its minimum outgoing edge by one aggregation, and the fragments merge. There are $O(\log n)$ phases, and each takes $\tilde{O}(c + d)$ rounds if shortcuts for the current fragments can be built in that time. So MST takes $\tilde{O}(c + d)$ rounds. The same frame gives $(1 + \epsilon)$-approximate [min cut](/distributed-min-cut/) and, with more work, approximate [shortest paths](/distributed-approximate-sssp/).

**Shortcuts for every graph.** Let $T$ be a BFS tree of depth $D$. Call a part *large* if it has at least $\sqrt{n}$ nodes. At most $\sqrt{n}$ parts are large. Give each large part $H_i = T$, and give each small part $H_i = \emptyset$. A large part then has diameter at most $2D$ in $G[S_i] \cup T$, and a small part has diameter less than $\sqrt{n}$. Each edge is in at most $\sqrt{n}$ trees and in one part, so $c \le \sqrt{n} + 1$ and $d \le \max(2D, \sqrt{n})$. The quality is $O(D + \sqrt{n})$. This gives the $\tilde{O}(D + \sqrt{n})$ MST algorithm, and the Peleg-Rubinovich graphs show that no better quality is possible in general.

**Tree-restricted shortcuts.** Haeupler, Izumi and Zuzic restrict each $H_i$ to the edges of one BFS tree $T$. Then $H_i$ is a forest, and its *block parameter* $b$ is the largest number of components of $H_i$ that touch $S_i$. Such a shortcut can be built without knowing the structure of the graph (for example, without a planar embedding), in $\tilde{O}(b(D + c))$ rounds, and MST then takes $\tilde{O}(bD + c)$ rounds.

## Examples

**A wheel.** Take a cycle of $n - 1$ nodes and one hub joined to every cycle node. The diameter is 2. Let the parts be arcs of the cycle. An arc of length $k$ has diameter $k - 1$ alone. Let $H_i$ be the spokes of the nodes of $S_i$, plus the hub. Then $G[S_i] \cup H_i$ has diameter at most 2, and each spoke is in one part only, so the congestion is 1. The quality is $O(1)$, although an arc can have about $n$ nodes. The parts do share the hub node, but a node is not a bottleneck in CONGEST, only an edge.

**A planar graph.** Ghaffari and Haeupler proved that each partition of a planar graph of diameter $D$ has shortcuts with congestion $O(D \log D)$ and dilation $O(D \log D)$. They first get congestion $O(D)$ and dilation $O(D^2)$, then they balance the two. They also show that $\Omega(D \log D / \log \log D)$ is needed in some planar graphs. So MST and $(1 + \epsilon)$-approximate min cut take $\tilde{O}(D)$ rounds on planar graphs.

**Other families.** The table gives the tree-restricted bounds of Haeupler, Izumi and Zuzic (DISC 2016 and PODC 2016).

| family | block parameter $b$ | congestion $c$ | MST rounds |
|---|---|---|---|
| general | 1 | $O(\sqrt{n})$ | $\tilde{O}(D + \sqrt{n})$ |
| pathwidth $k$ | $O(k)$ | $O(k)$ | $\tilde{O}(kD)$ |
| [treewidth](/treewidth/) $k$ | $O(k)$ | $O(k \log n)$ | $\tilde{O}(kD)$ |
| planar | $O(\log D)$ | $O(D \log D)$ | $\tilde{O}(D)$ |
| [genus](/graph-genus/) $g$ | $O(\sqrt{g})$ | $O(g D \log D)$ | $\tilde{O}(gD)$ |

Later work found good shortcuts for graphs that exclude a fixed minor, for expanders and for graphs with high connectivity. For graphs of constant diameter $D \ge 3$, the MST lower bounds of Lotker, Patt-Shamir and Peleg and of Elkin are also lower bounds on the shortcut quality.

## Where it is used

- **Global problems on special networks.** MST, [connectivity of a subgraph](/distributed-connected-components/) and approximate [min cut](/distributed-min-cut/) in $\tilde{O}(c + d)$ rounds, which is $\tilde{O}(D)$ on planar graphs and bounded genus graphs. This beats the general $\tilde{\Omega}(D + \sqrt{n})$ bound, which holds only on special non-planar graphs.
- **Shortest paths.** Approximate [SSSP](/distributed-approximate-sssp/) and DFS trees in planar graphs use shortcuts as a step, for aggregation over many parts.
- **Universal optimality.** Later work by Haeupler, Wajc and Zuzic (2021) shows that, for each fixed network topology, the best shortcut quality is about the best round complexity of MST on that topology.
- **Message-optimal MST.** Haeupler, Hershkowitz and Wajc (PODC 2018) gave a deterministic MST algorithm with $\tilde{O}(D + \sqrt{n})$ rounds and $\tilde{O}(m)$ messages, in a frame that also covers shortcut-based algorithms.

## References
