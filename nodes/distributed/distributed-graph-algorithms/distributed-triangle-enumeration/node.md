---
tag: 7GRAF4
kind: problem
slug: distributed-triangle-enumeration
name: Distributed triangle enumeration
aliases:
- distributed triangle listing
- distributed triangle detection
area: distributed/distributed-graph-algorithms
level: research
summary: Each triangle of the graph must be output by some node. In the congested clique and in CONGEST this takes n^(1/3) rounds, up to polylogarithmic factors.
model: congest-model
complexity:
  vars: {n: the number of nodes}
  time: {worst: "Õ(n^(1/3))"}
prereqs: [triangle-counting, congest-model, congested-clique-model]
see_also: [triangle-counting, triangle-listing-by-degree, triangle-finding, boolean-matrix-multiplication, streaming-triangle-counting, arboricity, congested-clique-model, distributed-connected-components]
sources:
  - paper: doi:10.1007/978-3-642-33651-5_14
    title: Danny Dolev, Christoph Lenzen and Shir Peled, Tri, tri again, finding triangles and small subgraphs in a distributed setting, DISC 2012, LNCS 7611
    locator: pages 195 to 209, the partition algorithm TriPartition for the congested clique, deterministic in O(n^(1/3)/log n) rounds (Remark 1), and the bound with the arboricity; arXiv 1201.6652
  - paper: doi:10.1145/3087801.3087811
    title: Taisuke Izumi and François Le Gall, Triangle finding and listing in CONGEST networks, PODC 2017
    locator: pages 381 to 389, finding in O(n^(2/3) (log n)^(2/3)) and listing in O(n^(3/4) log n) rounds of CONGEST, and the lower bound Ω(n^(1/3)/log n) for listing, also in the congested clique
  - paper: "Yi-Jun Chang, Seth Pettie and Hengjie Zhang, Distributed triangle detection via expander decomposition, SODA 2019"
    locator: the abstract, detection, counting and enumeration in Õ(n^(1/2)) rounds of CONGEST; arXiv 1807.06624
  - paper: "Yi-Jun Chang and Thatchaphol Saranurak, Improved distributed expander decomposition and nearly optimal triangle enumeration, PODC 2019"
    locator: the abstract, enumeration in Õ(n^(1/3)) rounds of CONGEST, which matches the lower bound up to polylogarithmic factors
  - paper: doi:10.1145/3460900
    title: Gopal Pandurangan, Peter Robinson and Michele Scquizzato, On the distributed complexity of large-scale graph computations, ACM Transactions on Parallel Computing 8(2), 2021
    locator: the lower bound for triangle enumeration in the k-machine model and its consequence Ω̃(n^(1/3)) for the congested clique; the conference version is SPAA 2018, pages 405 to 414
  - paper: "Keren Censor-Hillel, Petteri Kaski, Janne H. Korhonen, Christoph Lenzen, Ami Paz and Jukka Suomela, Algebraic methods in the congested clique, PODC 2015"
    locator: triangle detection and counting by matrix multiplication in O(n^(1 - 2/ω)) rounds of the congested clique
---

In distributed triangle enumeration, each triangle $\{x, y, z\}$ of a graph $G$ must be output by at least one node. In the [CONGEST model](/congest-model/), the network is $G$. In the [congested clique](/congested-clique-model/), all $n$ nodes can talk to each other, and $G$ is only the input: each node knows its own edges of $G$. In both models a message has $O(\log n)$ bits, and the round complexity is $\tilde{\Theta}(n^{1/3})$. In the congested clique, Dolev, Lenzen and Peled (DISC 2012) list all triangles in $O(n^{1/3}/\log n)$ rounds, deterministically, by a partition of the nodes into $n^{1/3}$ parts. Izumi and Le Gall (PODC 2017), and also Pandurangan, Robinson and Scquizzato (SPAA 2018), show that $\Omega(n^{1/3}/\log n)$ rounds are needed. In CONGEST the upper bound took longer: $\tilde{O}(n^{3/4})$ (Izumi and Le Gall), then $\tilde{O}(n^{1/2})$ (Chang, Pettie and Zhang, SODA 2019), then $\tilde{O}(n^{1/3})$ (Chang and Saranurak, PODC 2019).

This page is about the round complexity of listing triangles when the graph is spread over the nodes of a network. The sequential algorithms are [triangle counting](/triangle-counting/) and [listing by degree](/triangle-listing-by-degree/). The streaming version is [streaming triangle counting](/streaming-triangle-counting/), and the quantum query problem is [triangle finding](/triangle-finding/).

## In plain words

Each computer knows its own friends. A triangle is three computers that are all friends with each other. Together, the computers must write down each triangle.

A computer can find its own triangles if it learns which of its friends are friends with each other. But a popular computer has many friends, and asking about all pairs takes too many messages. The trick in the congested clique is to share the work: cut the computers into a few groups, give each computer one choice of three groups, and send it only the friendships between those groups. Each computer then gets about the same amount of data, and all links carry about the same load.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $n$ nodes and unique identifiers $0, \ldots, n - 1$. Each node knows its neighbours in $G$.

**Communication.** In CONGEST, a node can send one message of $O(\log n)$ bits on each edge of $G$ in each round. In the congested clique, it can send one such message to each other node in each round.

**Output.**

- **Enumeration** (listing): each triangle is output by at least one node. A node may output a triangle that does not contain it.
- **Detection**: some node outputs "yes" if $G$ has a triangle, and all nodes output "no" otherwise.
- **Counting**: all nodes learn the number of triangles.
- **Local listing**: each node lists the triangles that contain it. This is harder: a node of degree $\Delta$ in a dense graph can be in $\Theta(\Delta^2)$ triangles.

## Variants

- **Detection versus enumeration.** Detection needs only one bit of output, and the lower bound for enumeration does not apply to it. In the congested clique, detection takes $O(n^{1 - 2/\omega})$ rounds by fast [matrix multiplication](/boolean-matrix-multiplication/) (Censor-Hillel et al., PODC 2015), where $\omega$ is the exponent of matrix multiplication. That is less than $n^{0.16}$, below the $n^{1/3}$ of enumeration.
- **Graphs of small arboricity.** Dolev, Lenzen and Peled also give a bound in terms of the [arboricity](/arboricity/) $A$, which is much smaller than $n^{1/3}$ for sparse graphs.
- **Other small subgraphs.** Cliques $K_s$, cycles and other patterns of fixed size. The same partition idea lists $K_s$ in the congested clique in $O(n^{1 - 2/s})$ rounds up to log factors.
- **The k-machine model.** The graph is spread over $k$ machines at random. Pandurangan, Robinson and Scquizzato give tight bounds there, and the congested clique bound is the case $k = n$.

## Examples

**The partition algorithm on 8 nodes.** Take $n = 8$ and the edges of $K_4$ on $\{0, 1, 2, 3\}$, the triangle $\{4, 5, 7\}$, and the edge $3 4$. The cube root is $q = 2$, so there are two parts, the even nodes and the odd nodes, by $v \bmod 2$. Each node $t$ is the receiver of one ordered triple of parts $(a, b, c)$ with $t = 4a + 2b + c$, and lists the triangles $x < y < z$ with $x, y, z$ in the parts $a, b, c$.

| triangle | parts of $x, y, z$ | lister $t$ |
|---|---|---|
| $\{0, 1, 2\}$ | (0, 1, 0) | 2 |
| $\{0, 1, 3\}$ | (0, 1, 1) | 3 |
| $\{0, 2, 3\}$ | (0, 0, 1) | 1 |
| $\{1, 2, 3\}$ | (1, 0, 1) | 5 |
| $\{4, 5, 7\}$ | (0, 1, 1) | 3 |

Node 1, for the triple $(0, 0, 1)$, must learn the pairs between the even nodes and between the even and the odd nodes with the smaller one even: 16 bits in all. Node 0 reports $(0, 1)$, $(0, 2)$, $(0, 3)$, $(0, 4)$ to node 1, and node 2 reports $(2, 3)$, $(2, 4)$, $(2, 5)$, $(2, 6)$. The whole run moves 112 bits. No node receives more than 22 bits, and no link carries more than 4 bits in a phase. With $B = 3$ bits per message, the two phases take 1 and 2 rounds.

## Known algorithms

**The partition algorithm in the congested clique (Dolev, Lenzen and Peled).** This is the plan that the implementation follows, with a relay plan of its own for the routing.

1. Let $q = \lfloor n^{1/3} \rfloor$. Node $v$ is in part $v \bmod q$, so each part has at most $s = \lceil n/q \rceil \approx n^{2/3}$ nodes.
2. Node $t < q^3$ is the receiver of the ordered triple $(a, b, c)$ with $t = a q^2 + b q + c$. It lists each triangle $x < y < z$ with $x, y, z$ in the parts $a, b, c$. Each triangle has one such triple, so each triangle is listed exactly once.
3. Receiver $t$ needs one bit (edge or no edge) for each pair $x < y$ in the parts $(a, b)$, $(b, c)$ and $(a, c)$. That is at most $3 \cdot s(s + 1)/2 \approx 1.5\, n^{4/3}$ bits.
4. One end of each pair reports its bit: $x$ reports $\{x, y\}$ if $(y - x) \bmod n \le n/2$ (ties at $n/2$ go to the smaller end), so each node reports about half of its pairs. The tests check that each node sends and receives at most $1.5\, s(s + 1)$ bits.
5. Route the bits in two phases through relays: from the reporter to a relay, and from the relay to the receiver. All nodes know which pairs each reporter sends to each receiver and through which relay, since the plan depends only on $n$. So a message holds only bits, with no labels.

*Rounds.* Let $\Delta$ be the most bits that one node sends or receives. In a bipartite multigraph with a vertex for each sender, a vertex for each receiver and one edge for each bit, the maximum degree is $\Delta$. By König's theorem, its edges have a proper coloring with $\Delta$ colors. Send each bit of color $c$ through relay $c \bmod n$. Then each link carries at most $\lceil \Delta / n \rceil$ bits in each phase, that is $O(n^{1/3})$ bits, and each phase takes $O(n^{1/3} / \log n)$ rounds with messages of $\log n$ bits. The implementation uses a greedy plan in place of the coloring, with the cap $\lceil \Delta/n \rceil + 1$ on each link. The tests check that the greedy plan always finds room, that the listed triangles are exactly the triangles of a brute force search, and that the rounds stay within $2 \lceil (\lceil 1.5\, s(s + 1)/n \rceil + 1) / \lceil \log_2 n \rceil \rceil$. The plan does not depend on the input, so the number of rounds is a function of $n$ only.

Dolev, Lenzen and Peled give the bound $O(n^{1/3}/\log n)$ in Remark 1 of their paper. Lenzen's later deterministic routing for the congested clique gives the same bound for any such plan of bits, since each node sends and receives $O(n^{4/3})$ bits.

**CONGEST.**

| result | task | rounds |
|---|---|---|
| each node sends its neighbour list to its neighbours | listing | $O(\Delta)$ |
| Izumi and Le Gall, PODC 2017 | finding | $O(n^{2/3} (\log n)^{2/3})$ |
| Izumi and Le Gall, PODC 2017 | listing | $O(n^{3/4} \log n)$ |
| Chang, Pettie and Zhang, SODA 2019 | detection, counting, listing | $\tilde{O}(n^{1/2})$ |
| Chang and Saranurak, PODC 2019 | listing | $\tilde{O}(n^{1/3})$ |

*Sketch.* The fast CONGEST algorithms use an expander decomposition: remove a small fraction of the edges so that each remaining part has high conductance. A part with high conductance can route like a congested clique among its nodes with only a small loss, so each part runs a version of the partition algorithm. The removed edges form a sparser graph, and the algorithm recurses on it. Chang and Saranurak made the decomposition faster, which gave the $\tilde{O}(n^{1/3})$ bound.

## Bounds

**Lower bound $\Omega(n^{1/3}/\log n)$ for listing.** It holds in the congested clique, and so in CONGEST, which is weaker. *Sketch of the counting idea.* A random graph $G(n, 1/2)$ has about $n^3/48$ triangles, so some node outputs at least about $n^2/48$ of them. A set of $e$ edges contains at most $O(e^{3/2})$ triangles, so this node must be sure of $\Omega(n^{4/3})$ edges. At the start, a node knows only its own $n - 1$ pairs, and each other edge of a random graph is one bit of new information, so the node must receive $\Omega(n^{4/3})$ bits. It receives at most $O(n \log n)$ bits in a round. So it needs $\Omega(n^{1/3}/\log n)$ rounds. Izumi and Le Gall make this exact with an argument from information theory. Pandurangan, Robinson and Scquizzato prove a general bound for the k-machine model that gives the same $\tilde{\Omega}(n^{1/3})$ for the congested clique.

**Detection.** No lower bound of this kind is known for detection, since one bit of output does not need much information at any node.

So enumeration has round complexity $\tilde{\Theta}(n^{1/3})$ in both models. In CONGEST the upper bound is not a simple consequence of the congested clique one, since the network may have small cuts, which is why the expander decomposition is needed.

## Reductions

- **To matrix multiplication.** Detection and counting reduce to the product $A^2$ of the adjacency matrix, and the congested clique computes matrix products fast, which gives the $O(n^{1 - 2/\omega})$ bound.
- **From routing.** The partition algorithm is a fixed routing task: each node sends and receives $O(n^{4/3})$ bits. Any deterministic routing scheme for the congested clique turns it into rounds.
- **Expander parts to the congested clique.** In CONGEST, each part of high conductance simulates the congested clique algorithm with small overhead.

## Applications

- **Graph analysis.** The number of triangles and the clustering coefficient measure how much the friends of a node know each other, a basic statistic of social networks.
- **Small subgraph detection.** Triangles are the first case of the detection of fixed patterns, and the same tools apply to $K_4$, cycles and other small subgraphs.
- **A test case for models.** Triangle listing is the standard example of a problem whose difficulty comes from congestion and not from distance: it takes only one round in the [LOCAL model](/local-model/), but $\tilde{\Theta}(n^{1/3})$ rounds with small messages.

## References
