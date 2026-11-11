---
tag: BCTDPX
kind: problem
slug: distributed-connected-components
name: Distributed connected components
aliases:
- distributed connectivity
- distributed component labeling
area: distributed/distributed-graph-algorithms
level: intro
summary: Every node learns a label that is the same for all nodes of its connected component. Label propagation and Borůvka-style merging solve it in CONGEST; a subgraph needs about √n + D rounds.
model: congest-model
complexity:
  vars: {n: the number of nodes, m: the number of edges, D: the hop diameter}
  time: {worst: O(n log n)}
  messages: {worst: O(m log n)}
prereqs: [connected-components, congest-model, flooding, boruvka, convergecast]
see_also: [connected-components, union-find-connectivity, distributed-mst, shiloach-vishkin, random-mate-contraction, low-congestion-shortcuts, mrc-model, mapreduce-model]
sources:
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Section 4.4 (SynchGHS, the Borůvka-style merging in synchronous rounds that the implementation follows)
  - book: isbn:9780898714647
    title: David Peleg, Distributed Computing, A Locality-Sensitive Approach, SIAM, 2000
    locator: the chapters on the basic algorithms (flooding, the tree constructions and the MST)
  - paper: doi:10.1137/11085178X
    title: Atish Das Sarma, Stephan Holzer, Liah Kor, Amos Korman, Danupon Nanongkai, Gopal Pandurangan, David Peleg and Roger Wattenhofer, Distributed verification and hardness of distributed approximation, SIAM Journal on Computing 41(5), 2012
    locator: pages 1235 to 1265, the lower bound Ω(D + (n/(B log n))^(1/2)) for the verification of connected spanning subgraphs and of s-t connectivity
  - paper: "Ramakrishna Thurimella, Sub-linear distributed algorithms for sparse certificates and biconnected components, Journal of Algorithms 23(1), 1997"
    locator: the connected components of a subgraph in O(D + n^(1/2) log* n) rounds, from the MST algorithm of Kutten and Peleg
  - paper: "Tomasz Jurdziński and Krzysztof Nowicki, MST in O(1) rounds of congested clique, SODA 2018"
    locator: pages 2620 to 2632, the randomized MST, and so connectivity, in O(1) rounds of the congested clique
  - paper: doi:10.1137/1.9781611974331.ch16
    title: Mohsen Ghaffari and Bernhard Haeupler, Distributed algorithms for planar networks II, low-congestion shortcuts, MST, and min-cut, SODA 2016
    locator: pages 202 to 219, MST and so subgraph connectivity in Õ(D) rounds on planar networks
---

In distributed connected components, each node of a graph learns a label, so that two nodes have the same label exactly when they are in the same [connected component](/connected-components/). The usual label is the smallest identifier in the component. There are two settings. In the first, the network itself is the graph, and each component works alone. In the second, the graph is a subgraph $H$ of a larger connected network $G$, and the nodes may use all links of $G$ to talk. In the [CONGEST model](/congest-model/), the first setting is easy: [flooding](/flooding/) the smallest label takes as many rounds as the largest component diameter. The second setting is as hard as [distributed MST](/distributed-mst/): it takes $\tilde{\Theta}(\sqrt{n} + D)$ rounds, where $D$ is the diameter of $G$.

This page is about networks that compute their own components by messages. The sequential problem and its algorithms are on [connected components](/connected-components/) and [union-find connectivity](/union-find-connectivity/), and the shared-memory parallel algorithms are [Shiloach-Vishkin](/shiloach-vishkin/) and [random-mate contraction](/random-mate-contraction/).

## In plain words

Some computers are joined by cables, but the cables do not join all of them into one network. Each computer must learn which group it belongs to, where a group is all computers that can reach each other.

The simple method: each computer says its own number, and then keeps and passes on the smallest number it has heard. After a while, each group agrees on its smallest number. This takes as many rounds as the longest shortest route in a group.

The other method grows groups like [Borůvka's algorithm](/boruvka/): each small group picks one cable to a neighbouring group, and the two join. The number of groups at least halves each time, so there are few phases, and few messages.

## Definition

**Setting A: the network is the graph.** An undirected graph $H = (V, E_H)$ with $n$ nodes and $m$ edges, which need not be connected. Each node has a unique identifier of $O(\log n)$ bits and knows its neighbours. Messages travel only over the edges of $H$, so nodes in different components never talk.

**Setting B: a subgraph of a network.** A connected network $G = (V, E)$ with hop diameter $D$, and a subgraph $H = (V, E_H)$ with $E_H \subseteq E$. Each node knows which of its links are in $H$. Messages may use all links of $G$.

**Output.** Each node $v$ outputs a label $c(v)$ with $c(u) = c(v)$ if and only if $u$ and $v$ are joined by a path in $H$. A common stronger output is $c(v) = \min\{u : u$ is in the component of $v\}$.

**Cost.** The number of synchronous rounds, with one message of $O(\log n)$ bits on each link in each direction in each round, and the number of messages.

## Variants

- **Connectivity verification.** Decide whether $H$ is connected and spanning, or whether $s$ and $t$ are in the same component of $H$. Das Sarma et al. use these yes or no questions as the base of their lower bounds.
- **Termination.** In setting A, a node cannot see when its component is done. It must know a bound such as $n$, or run an echo on a spanning tree of its component. The round counts below assume that the nodes know $n$.
- **The [congested clique](/congested-clique-model/).** All pairs of nodes can talk, and $H$ is the input. MST, and so connectivity, takes $O(1)$ rounds with randomization (Jurdziński and Nowicki, SODA 2018).
- **Large-scale data models.** In the [MRC model](/mrc-model/) and other [MapReduce](/mapreduce-model/) models, the graph is spread over machines with small memory. Connectivity there is a separate line of work. The iterative label propagation of [Pregel](/pregel-model/) is the same as the first algorithm below.
- **The [LOCAL model](/local-model/).** In setting B, collect $H$ at one node in $O(D)$ rounds. Only the message size makes setting B hard.

## Examples

**Label propagation on 8 nodes.** Take $H$ with the edges $04, 42, 26$ (a path), $15, 57, 71$ (a triangle), and node 3 alone.

| round | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| start | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| 1 | 0 | 1 | 2 | 3 | 0 | 1 | 2 | 1 |
| 2 | 0 | 1 | 0 | 3 | 0 | 1 | 2 | 1 |
| 3 | 0 | 1 | 0 | 3 | 0 | 1 | 0 | 1 |

The last change is in round 3, because node 6 is 3 hops from node 0. A node sends only in the round after its label changed (and all nodes send in round 1), so the run sends 22 messages.

**Borůvka-style merging on the same graph.** Each edge $\{u, v\}$ with $u < v$ gets the weight $8u + v + 1$, so the weights are distinct. In phase 1, nodes 0 and 4 both choose the edge $04$ (weight 5), node 2 chooses $24$ and node 6 chooses $26$, so $\{0, 2, 4, 6\}$ becomes one fragment, named 4 after the larger end of its core edge $04$. In the triangle, nodes 1 and 5 choose $15$ and node 7 chooses $17$, so $\{1, 5, 7\}$ becomes one fragment, named 5. Node 3 has no edge. After phase 1 the fragments are the components. The run still takes all $\lceil \log_2 8 \rceil = 3$ phases of $3 \cdot 8 + 2 = 26$ rounds, 78 rounds in all, and sends 68 messages.

## Known algorithms

**Label propagation (setting A).** Each node $v$ sets $c(v) = v$. In each round, each node whose label changed in the previous round (all nodes in round 1) sends its label to its neighbours, and each node takes the smallest label that it receives if it is smaller than its own.

*What it gives.* By induction on $r$, after round $r$ each node $v$ holds the smallest identifier within $r$ hops of $v$ in $H$. So node $v$ has its final label after $d_H(v, u^*)$ rounds, where $u^*$ is the smallest node of its component, and all labels are final after at most the largest component diameter. Each node changes its label at most once for each distinct value it holds, so the messages are at most $2m$ times the number of rounds. The algorithm does not know when to stop. With a known bound $n$, it stops after $n - 1$ rounds.

**Borůvka-style merging (setting A).** This is the algorithm of the implementation, the SynchGHS scheme of the [distributed MST](/distributed-mst/) page with the distinct weights $u \cdot n + v + 1$ on the edges of $H$. The nodes know $n$. There are $\lceil \log_2 n \rceil$ phases of $3n + 2$ rounds. In each phase, each fragment (a rooted tree of $H$ edges):

1. tells its neighbours its fragment name (1 round),
2. finds its lightest edge to another fragment by a [convergecast](/convergecast/) to the root ($n$ rounds),
3. broadcasts the choice from the root ($n$ rounds),
4. sends Connect over the chosen edge (1 round),
5. lets the larger end of each core edge flood its identifier as the new name over the new tree ($n$ rounds).

*What it gives, exactly.* The weights are distinct, so the chosen edges form a forest by the [cut property](/cut-property/) argument of Borůvka. Each fragment that is not yet a whole component merges with at least one other fragment in each phase. If $c$ is the number of components and $f_p$ the number of fragments after phase $p$, then $f_{p+1} - c \le (f_p - c)/2$. After $\lceil \log_2 n \rceil$ phases, each fragment is a component, and the names of the fragments are the labels. The run takes exactly $\lceil \log_2 n \rceil (3n + 2)$ rounds. Each phase sends at most $2m$ name messages and at most $4n$ other messages, so the total is $O((m + n) \log n)$ messages. Each message holds one name or one weight, which is $O(\log n)$ bits. The tests check each of these claims. The labels are the names of the cores, not the smallest identifiers. One more flood of the minimum over each final tree gives the smallest identifiers, in $n$ more rounds.

The fixed phase length makes this slower in rounds than label propagation, which takes at most $n - 1$ rounds. The merging scheme matters for two other reasons: it sends fewer messages on dense graphs, and it is the base of the fast algorithms of setting B.

**Setting B: through MST.** Give each edge of $H$ the weight 0 and each other edge of $G$ the weight 1, and run an MST algorithm for $G$ (with ties broken by identifiers). The MST edges of weight 0 form a spanning forest of $H$, so two nodes are in the same component of $H$ exactly when the tree path between them has only weight 0 edges. The fast MST algorithms give the labels too, since their fragments of weight 0 edges are the components. So setting B takes $\tilde{O}(\sqrt{n} + D)$ rounds, as MST does. Thurimella (1997) gave $O(D + \sqrt{n} \log^* n)$ rounds with the MST algorithm of Kutten and Peleg. On planar networks and other networks with good [low-congestion shortcuts](/low-congestion-shortcuts/), it takes $\tilde{O}(D)$ rounds.

## Bounds

**Setting A.** Each algorithm needs $\Omega(\text{largest component diameter})$ rounds: on a path whose smallest node is at one end, the other end must hear from it. Label propagation meets this bound. A node also needs $\Omega(m)$ messages in the worst case to learn about all its neighbours.

**Setting B.** Das Sarma et al. (SIAM J. Comput. 2012) show that the verification of a connected spanning subgraph, and $s$-$t$ connectivity in $H$, need $\Omega(D + \sqrt{n/(B \log n)})$ rounds with messages of $B$ bits, even for randomized algorithms, on graphs of diameter $O(\log n)$. The proof is a reduction from two-party [set disjointness](/disjointness-problem/) on the graphs of the [Peleg-Rubinovich bound](/peleg-rubinovich-lower-bound/). With the MST algorithms, setting B has round complexity $\tilde{\Theta}(\sqrt{n} + D)$.

## Reductions

- **Connectivity to MST.** The weights 0 and 1 above reduce setting B to [distributed MST](/distributed-mst/).
- **Lower bounds from verification.** Das Sarma et al. reduce the verification of a connected spanning subgraph to many problems: MST, shortest paths, min cut and others. So the hardness of setting B is the root of the $\tilde{\Omega}(\sqrt{n} + D)$ bounds for those problems.
- **From union-find.** Sequential [union-find](/disjoint-set/) gives the same labels in near-linear time, and the tests use it as the oracle.

## Applications

- **Fault detection.** After links fail, each node learns which part of the network it can still reach, for example to re-elect a leader in each part.
- **A step in other algorithms.** Connectivity of a subgraph is a step in distributed [min cut](/distributed-min-cut/) (to test whether removing a set of edges cuts the graph), in the verification of spanning trees, and in [graph contraction](/graph-contraction/).
- **Graph analysis at scale.** Label propagation is the standard way to find components in vertex-centric systems such as [Pregel](/pregel-model/), where each vertex is a small process that sends messages to its neighbours.

## References
