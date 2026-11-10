---
tag: DNB73J
kind: problem
slug: stream-connectivity-problem
name: Connectivity in streams problem
aliases:
- graph connectivity in a stream
- spanning forest in a stream
area: online-and-streaming/streaming-sketches
level: advanced
summary: Decide connectivity or find a spanning forest of a graph whose edges arrive as a stream. Θ(n log n) bits with insertions only, and Θ(n log³ n) bits for a spanning forest with deletions.
prereqs: [streaming-model, connected-components, spanning-forest, disjoint-set, turnstile-model]
see_also: [agm-graph-sketch, l0-sampling-problem, l0-sampler, streaming-maximal-matching-problem, streaming-triangle-counting-problem, dynamic-connectivity, index-problem, bipartiteness-testing]
sources:
  - paper: doi:10.1016/j.tcs.2005.09.013
    title: Joan Feigenbaum, Sampath Kannan, Andrew McGregor, Siddharth Suri and Jian Zhang, On graph problems in a semi-streaming model, Theoretical Computer Science 348(2-3), 2005
    locator: pp. 207 to 216; the definition of the semi-streaming model and the one-pass algorithms for connectivity and bipartiteness
  - paper: doi:10.4230/LIPIcs.APPROX-RANDOM.2015.435
    title: Xiaoming Sun and David P. Woodruff, Tight bounds for graph problems in insertion streams, APPROX-RANDOM 2015
    locator: pp. 435 to 448; the Ω(n log n) bit lower bound for one-pass connectivity, by a reduction from the permutation problem
  - paper: doi:10.1137/1.9781611973099.40
    title: Kook Jin Ahn, Sudipto Guha and Andrew McGregor, Analyzing graph structure via linear measurements, SODA 2012
    locator: pp. 459 to 467; the section on connectivity in dynamic streams
  - url: https://arxiv.org/abs/1807.05135
    title: Jelani Nelson and Huacheng Yu, Optimal lower bounds for distributed and streaming spanning forest computation, SODA 2019
    locator: the main theorems (Ω(n log³ n) bits for a dynamic spanning forest structure, and Ω(log³ n) bits per vertex for distributed sketching of a spanning forest)
  - url: https://arxiv.org/abs/2007.12323
    title: Huacheng Yu, Tight distributed sketching lower bound for connectivity, SODA 2021
    locator: the main theorem (Ω(log³ n) bits average message length for deciding connectivity with error at most 1/4)
  - paper: doi:10.1145/2627692.2627694
    title: Andrew McGregor, Graph stream algorithms, a survey, SIGMOD Record 43(1), 2014
    locator: the sections on connectivity in insertion-only and in dynamic streams
---

The connectivity in streams problem gives the edges of a graph on $n$ vertices one at a time, in any order, and asks whether the graph is connected, or asks for its connected components or a spanning forest. The algorithm reads the stream once and has much less memory than the $\Theta(n^2)$ possible edges. If edges are only inserted, a [disjoint-set](/disjoint-set/) structure solves the problem in $O(n \log n)$ bits, and this is optimal. If edges can also be deleted, the [AGM graph sketch](/agm-graph-sketch/) finds a spanning forest in $O(n \log^3 n)$ bits, which is also optimal. On this page $n$ is the number of vertices and $m$ the number of edges of the final graph.

## In plain words

A city opens and closes roads one at a time, and a clerk hears each change once. At the end, the clerk must say which districts can reach each other. If roads are only opened, the clerk keeps a short note per district saying which group it belongs to, and joins two groups when a road connects them. That is enough, and it needs about one number per district. If roads can also close, a closed road may be the only link between two groups, so the simple notes are not enough. Then the clerk needs random sketches that remember a little about every road, and the memory grows by a few more factors of the number size.

## Definition

**Stream.** The vertex set is $V = [n]$ and is known in advance. The stream is a sequence of updates. In the *insertion-only* model each update inserts an edge $\{u, v\}$. In the *dynamic* (turnstile) model each update inserts or deletes an edge, and a deletion removes an edge that is present. The final graph $G = (V, E)$ is what is left at the end.

**Outputs.** There are three versions, in increasing order of difficulty:

- **Decision.** Is $G$ connected?
- **Components.** Output the partition of $V$ into the connected components of $G$, or the number of components.
- **Spanning forest.** Output a set $F \subseteq E$ that is a forest and has the same components as $G$.

A spanning forest gives the components, and the components give the decision.

**Model.** The algorithm makes one pass, unless the text says otherwise. Space is counted in bits. A randomized algorithm must be correct with probability at least $2/3$, or $1 - \delta$, for each fixed stream. The [semi-streaming model](/streaming-maximal-matching-problem/) of Feigenbaum et al. allows $O(n\,\mathrm{polylog}\,n)$ bits, and both algorithms below fit in it.

## Variants

- **Multiple passes.** Allow $p$ passes over the same stream.
- **k-edge-connectivity.** Decide whether $G$ stays connected after removing any $k - 1$ edges, or output a certificate of that.
- **Bipartiteness** and **minimum spanning tree weight**, which reduce to connectivity (see Reductions).
- **Sliding windows.** Ask about the graph formed by the last $W$ edges.
- **Distributed sketching.** Each vertex sees only its own edges and sends one message to a referee, who must answer. The AGM sketch works here, with $O(\log^3 n)$ bits per vertex.
- **Vertex connectivity, small components, and other properties** studied in the same models.

## Examples

**Insertion only.** Let $n = 6$ and the stream be $\{1,2\}$, $\{3,4\}$, $\{2,3\}$, $\{1,4\}$, $\{5,6\}$. A disjoint-set structure joins $\{1,2\}$, then $\{3,4\}$, then joins these two groups with $\{2,3\}$. The edge $\{1,4\}$ closes a cycle and is not kept. Then $\{5,6\}$ forms a new group. The answer: two components, $\{1,2,3,4\}$ and $\{5,6\}$, with the spanning forest $\{1,2\}, \{3,4\}, \{2,3\}, \{5,6\}$. The graph is not connected.

**Why deletions are hard.** Add the update "delete $\{2,3\}$" to the stream above. The final graph is still connected on $\{1,2,3,4\}$, through the edge $\{1,4\}$. But the disjoint-set structure threw $\{1,4\}$ away, and it cannot undo the merge either. An algorithm for dynamic streams must keep some information about every edge, even the ones that close cycles, because any of them may become a bridge later.

**A sketch.** The [AGM graph sketch](/agm-graph-sketch/) page traces a stream on 6 vertices with an insert and a delete of $\{3,4\}$, and its sketch returns the forest $\{1,2\}, \{1,3\}, \{4,5\}, \{5,6\}$ in two Borůvka rounds.

## Known algorithms

| algorithm | stream | output | space in bits |
|---|---|---|---|
| store all edges | dynamic | anything | $O(m \log n)$ |
| [disjoint-set](/disjoint-set/) on the stream (Feigenbaum et al. 2005) | insertion only | spanning forest | $O(n \log n)$ |
| [AGM graph sketch](/agm-graph-sketch/) (Ahn, Guha and McGregor 2012) | dynamic | spanning forest, w.h.p. | $O(n \log^3 n)$ |

The disjoint-set algorithm keeps a forest $F$: on each new edge, if its ends are in different trees, add it to $F$ and join the trees. It keeps at most $n - 1$ edges, each in $O(\log n)$ bits. A correctness proof is short: by induction, the trees of $F$ always have the same vertex sets as the components of the edges seen so far, since an edge inside a tree does not change the components and an edge between two trees joins exactly those two.

## Bounds

**Insertion only, Ω(n) by a simple reduction.** Take the [INDEX problem](/index-problem/): Alice holds $x \in \{0, 1\}^k$, Bob holds $j \in [k]$, and Bob must output $x_j$ after one message from Alice. Its randomized one-way communication is $\Omega(k)$. Build a graph on the vertices $s, s', u_1, \ldots, u_k$. Alice streams the edges $\{u_i, s\}$ for all $i$ with $x_i = 1$, and sends the memory of the algorithm to Bob. Bob streams $\{s, s'\}$ and $\{u_i, s'\}$ for all $i \ne j$. Now $u_j$ has an edge only if $x_j = 1$, and every other vertex is joined to $s$ or $s'$, which are joined to each other. So the graph is connected exactly when $x_j = 1$, and any one-pass algorithm for the decision version uses $\Omega(k) = \Omega(n)$ bits.

**Insertion only, Θ(n log n).** Sun and Woodruff (2015) raised the lower bound to $\Omega(n \log n)$ bits for randomized one-pass algorithms that decide connectivity with constant probability, by a reduction from a permutation problem. The disjoint-set algorithm matches it. They proved the same bound for bipartiteness, cycle-freeness and several other properties.

**Dynamic, spanning forest, Θ(n log³ n).** The AGM sketch uses $O(n \log^3 n)$ bits. Nelson and Yu (2019) proved that every data structure that maintains a graph under edge insertions and deletions and outputs a spanning forest with constant probability needs $\Omega(n \log^3 n)$ bits. They proved the matching $\Omega(\log^3 n)$ bits per vertex in distributed sketching.

**Dynamic, decision.** In distributed sketching, Yu (2021) proved that deciding connectivity with error at most $1/4$ still needs $\Omega(\log^3 n)$ bits of average message length, so even the yes or no answer costs as much as the forest there.

**Deterministic and dynamic.** The known sublinear-space algorithms for dynamic streams all use randomness, and their guarantee holds against a stream fixed before the random bits are drawn.

## Reductions

- **Bipartiteness.** Build the double cover with vertices $(v, 0)$ and $(v, 1)$ and, for each edge $\{u, v\}$, the edges $\{(u, 0), (v, 1)\}$ and $\{(u, 1), (v, 0)\}$. A connected component of $G$ is bipartite exactly when it lifts to two components of the double cover, so comparing the numbers of components decides bipartiteness. This works in both models.
- **k-edge-connectivity.** With $k$ independent linear sketches, find a spanning forest $F_1$, delete its edges from the second sketch, find $F_2$, and so on. $F_1 \cup \cdots \cup F_k$ has at most $k(n - 1)$ edges and keeps every cut of size below $k$.
- **Minimum spanning tree weight.** The weight of a minimum spanning tree with weights in $[1, W]$ can be estimated within a factor $1 + \varepsilon$ from the numbers of components of the subgraphs of edges with weight at most $(1 + \varepsilon)^i$, for all $i$.
- **From L0 sampling.** In the dynamic model, the spanning forest problem reduces to [L0 sampling](/l0-sampling-problem/) of signed incidence vectors; see the AGM sketch.
- **From INDEX and from a permutation problem.** These give the lower bounds above.

## Applications

- Analysis of large graphs that arrive as edge streams, such as call graphs, web links and social networks, where only the vertex set fits in memory.
- Dynamic connectivity in distributed systems: each machine sketches its share of the edges, and the sums give the components of the whole graph.
- As a subroutine for bipartiteness, minimum spanning trees, cut sparsifiers and edge connectivity in graph streams.
- Large-scale graph processing systems that keep connectivity sketches on disk, such as GraphZeppelin.

## References
