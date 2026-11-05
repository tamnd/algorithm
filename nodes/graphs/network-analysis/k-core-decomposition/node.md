---
tag: 6RCMB9
kind: problem
slug: k-core-decomposition
name: k-core decomposition
aliases:
- core decomposition
- core decomposition problem
- coreness
area: graphs/network-analysis
level: core
summary: Compute the core number of every node.
prereqs: [k-core, degree, adjacency-list]
see_also: [batagelj-zaversnik-algorithm, degeneracy, degeneracy-ordering, dynamic-k-core-decomposition, core-periphery-structure, bucket-sort, greedy-coloring]
sources:
  - paper: doi:10.1007/s11634-010-0079-y
    title: Vladimir Batagelj and Matjaž Zaversnik, Fast algorithms for determining (generalized) core groups in social networks, Advances in Data Analysis and Classification 5(2), 129 to 145 (2011)
    locator: the O(m) algorithm for cores with bucket arrays, and the algorithm for generalized cores
  - paper: doi:10.1145/2402.322385
    title: David W. Matula and Leland L. Beck, Smallest-last ordering and clustering and graph coloring algorithms, Journal of the ACM 30(3), 417 to 427 (1983)
    locator: the linear-time smallest-last ordering and the largest minimum degree of a subgraph
  - paper: doi:10.1109/TPDS.2012.124
    title: Alberto Montresor, Francesco De Pellegrini and Daniele Miorandi, Distributed k-core decomposition, IEEE Transactions on Parallel and Distributed Systems 24(2), 288 to 300 (2013)
    locator: the local update rule, its convergence, and the bound on the number of rounds
  - paper: doi:10.1038/ncomms10168
    title: Linyuan Lü, Tao Zhou, Qian-Ming Zhang and H. Eugene Stanley, The H-index of a network node and its relation to degree and coreness, Nature Communications 7, 10168 (2016)
    locator: the theorem that iterating the H operator from the degrees converges to the core numbers
  - paper: doi:10.1007/s00778-019-00587-4
    title: Fragkiskos D. Malliaros, Christos Giatsidis, Apostolos N. Papadopoulos and Michalis Vazirgiannis, The core decomposition of networks, theory, algorithms and applications, The VLDB Journal 29, 61 to 92 (2020)
    locator: Sections 3 and 4 (algorithms in memory, external memory, distributed and streaming settings)
---

The k-core decomposition problem asks for the core number of each vertex of a graph: the largest $k$ such that the vertex lies in the [k-core](/k-core/), the largest subgraph with minimum degree at least $k$. Repeatedly deleting a vertex of smallest remaining degree solves it, and with an array of buckets indexed by degree, as in the [Batagelj-Zaversnik algorithm](/batagelj-zaversnik-algorithm/), this takes $O(n + m)$ time. The answer also gives the [degeneracy](/degeneracy/) of the graph and a [degeneracy ordering](/degeneracy-ordering/).

## In plain words

Think of a social network. Some people have many friends, but their friends have few other friends. Others sit in a tight group where everyone knows many people of the group. The core number tells these apart.

To compute it, remove the person with the fewest friends left, then update the counts of their friends, and repeat until no one is left. Keep track of the largest "fewest friends" value seen so far. When a person is removed, that running value is their core number. People removed early have small core numbers and sit at the edge of the network. People removed last form its densest part.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, given by [adjacency lists](/adjacency-list/). Self-loops are not allowed. Parallel edges are allowed in the multigraph variant, where degrees count them with multiplicity.

**Output.** The function $\mathrm{core}: V \to \{0, 1, \ldots, n - 1\}$ with

$$\mathrm{core}(v) = \max\{ k \ge 0 : v \in C_k(G) \},$$

where $C_k(G)$ is the [k-core](/k-core/), the largest induced subgraph in which every vertex has at least $k$ neighbours. The answer is unique; there are no ties to break. Each [connected component](/connected-components/) can be solved on its own, since the $k$-core of $G$ is the union of the $k$-cores of its components, and an isolated vertex has core number 0.

**Equivalent form.** Let $v_1, \ldots, v_n$ be any order produced by repeatedly deleting a vertex of minimum degree in the remaining graph, and let $d_i$ be the degree of $v_i$ when it is deleted. Then

$$\mathrm{core}(v_i) = \max_{j \le i} d_j.$$

*Proof.* Fix $k$, and let $i^*$ be the first index with $d_{i^*} \ge k$. Each of $v_1, \ldots, v_{i^*-1}$ had fewer than $k$ remaining neighbours when it was deleted, so these deletions are steps of the peeling for $k$, and the [k-core](/k-core/) page shows that such steps never delete a vertex of $C_k(G)$. At step $i^*$ the remaining set $\{v_{i^*}, \ldots, v_n\}$ has minimum degree $d_{i^*} \ge k$, so it is $k$-dense and lies inside $C_k(G)$. Hence $C_k(G) = \{v_i : i \ge i^*\} = \{v_i : \max_{j \le i} d_j \ge k\}$. If there is no such $i^*$, every vertex is deleted by peeling steps for $k$, and $C_k(G)$ is empty, which agrees with the formula. Taking the largest $k$ gives the claim. $\square$

## Variants

- **Degeneracy only.** Output $\max_v \mathrm{core}(v)$ and an ordering that witnesses it. The same peeling solves it.
- **One $k$.** Output only $C_k(G)$ for a given $k$. A queue of the vertices of degree less than $k$ suffices, in $O(n + m)$ time.
- **Generalized cores.** Replace the degree by a monotone vertex function, such as a weighted degree. Batagelj and Zaversnik solve this in $O(m \log n)$ time with a heap.
- **Directed graphs.** Compute in-cores, out-cores or $(k, l)$-cores, by peeling on in-degrees, out-degrees or both.
- **Dynamic graphs.** Keep the core numbers while edges are inserted and deleted; see [dynamic k-core decomposition](/dynamic-k-core-decomposition/). One edge update changes each core number by at most 1.
- **Distributed and external memory.** The graph is spread over many machines or does not fit in memory. Methods use local rules that need only the values of the neighbours.
- **The $k$-truss decomposition.** The same question for edges, with "the number of triangles that contain the edge" in place of the degree.

## Examples

**Peeling.** Take the graph of the [k-core](/k-core/) page: the vertices 0 to 9, the complete graph on $\{0,1,2,3\}$, and the edges $\{0,4\}$, $\{1,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$, $\{6,8\}$, $\{3,8\}$, $\{5,9\}$. Delete a vertex of smallest remaining degree, the smallest label first on ties.

| step | deleted | its degree $d_i$ | running max | remaining degrees after |
|---|---|---|---|---|
| 1 | 7 | 0 | 0 | unchanged |
| 2 | 9 | 1 | 1 | 5: 2 |
| 3 | 5 | 2 | 2 | 4: 3, 6: 2 |
| 4 | 6 | 2 | 2 | 4: 2, 8: 1 |
| 5 | 8 | 1 | 2 | 3: 3 |
| 6 | 4 | 2 | 2 | 0: 3, 1: 3 |
| 7 | 0 | 3 | 3 | 1, 2, 3: 2 |
| 8 to 10 | 1, 2, 3 | 2, 1, 0 | 3 | |

The core numbers of $0, 1, \ldots, 9$ are $3, 3, 3, 3, 2, 2, 2, 0, 2, 1$. At step 5 vertex 8 has degree 1, less than the running maximum 2, and still gets core number 2: the running maximum, not the degree at deletion, is the answer.

**The local rule.** For a list of numbers, the $h$-index is the largest $h$ such that at least $h$ of the numbers are at least $h$. Start with $h_0(v) = \deg(v)$ and set $h_{t+1}(v)$ to the $h$-index of the values $h_t(w)$ of the neighbours $w$ of $v$, for all vertices at once. On the same graph:

| round | values of $0, 1, \ldots, 9$ |
|---|---|
| 0 | 4 4 3 4 4 3 3 0 2 1 |
| 1 | 3 3 3 3 3 2 2 0 2 1 |
| 2 | 3 3 3 3 2 2 2 0 2 1 |
| 3 | no change |

Lü and co-authors prove that this sequence always converges to the core numbers, and Montresor and co-authors give the same rule as a distributed algorithm. Each value never increases from one round to the next and stays at least the core number.

**Extremes.** In a $d$-regular graph, every core number is $d$. In a tree with at least one edge, every non-isolated vertex has core number 1. In a star with $n - 1$ leaves, the centre has degree $n - 1$ and core number 1.

## Known algorithms

| algorithm | idea | time |
|---|---|---|
| [Batagelj-Zaversnik algorithm](/batagelj-zaversnik-algorithm/) | peel by minimum degree, with vertices kept sorted by degree in bucket arrays | $O(n + m)$ |
| Smallest-last ordering (Matula and Beck) | the same peeling, written for colouring; it also yields the degeneracy | $O(n + m)$ |
| Peeling with a binary heap | the same order with a priority queue | $O(m \log n)$ |
| Local $h$-index rule (Lü and co-authors; Montresor and co-authors) | iterate the $h$-index of the neighbours' values | $O(m)$ per round, and at most $\sum_v (\deg(v) - \mathrm{core}(v)) + 1$ rounds |
| [Dynamic k-core decomposition](/dynamic-k-core-decomposition/) | update only the vertices whose core number can change | depends on the update |

## Bounds

- **Upper bound.** $O(n + m)$ time and $O(n)$ extra words on a [word RAM](/word-ram/) with adjacency lists, by the bucket peeling. The degrees are integers in $0$ to $n - 1$, so the buckets replace a [priority queue](/priority-queue/), in the manner of a [bucket sort](/bucket-sort/).
- **Matching lower bound.** The bucket peeling reads each adjacency entry a constant number of times, so it is optimal up to a constant factor among algorithms that read the input. An exact algorithm cannot skip parts of the input in general: a path on $n$ vertices has all core numbers 1, and the single edge between its ends makes them all 2.
- **Rounds of the local rule.** Lü and co-authors show that each value of the local rule never increases and never drops below the core number. Each round before the last lowers some integer value by at least 1, so the number of rounds is at most $\sum_v (\deg(v) - \mathrm{core}(v)) + 1$. Many real graphs need far fewer.

## Reductions

- **To degeneracy and colouring.** The deletion order, reversed, is a [degeneracy ordering](/degeneracy-ordering/). [Greedy colouring](/greedy-coloring/) in that order uses at most $\max_v \mathrm{core}(v) + 1$ colours.
- **To clique search.** Each [clique](/clique/) of size $q$ lies inside the $(q-1)$-core, so a search for a [maximum clique](/maximum-clique/) can first delete all vertices of core number less than the size of the best clique found so far. In the degeneracy order, each vertex has at most $\delta^*$ later neighbours, which bounds the work of [Bron-Kerbosch](/bron-kerbosch/) with pivoting.
- **To densest subgraph.** Let $H$ be a subgraph of largest density $\rho^* = |E(H)|/|V(H)|$. Each vertex of $H$ has at least $\rho^*$ neighbours in $H$, else deleting it raises the density. So $H$ is $\lceil \rho^* \rceil$-dense, and the degeneracy $\delta^*$ is at least $\rho^*$. The $\delta^*$-core has minimum degree $\delta^*$, so its density is at least $\delta^*/2 \ge \rho^*/2$. The innermost core is a 2-approximation of the densest subgraph.

## Applications

- Visualization of large networks, by drawing the shells as rings with the innermost core in the middle.
- Finding influential spreaders: in epidemic models, vertices of large core number are often better seeds than vertices of large degree.
- A filter before costly searches, such as clique finding and [community detection](/community-detection/).
- Describing the hierarchy of the Internet at the level of autonomous systems, and the cohesive groups of social networks.

## References
