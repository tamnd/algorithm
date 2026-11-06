---
tag: AWGFBV
kind: problem
slug: network-motif-enumeration
name: Network motif enumeration
aliases:
- motif counting
- graphlet counting
area: graphs/network-analysis
level: advanced
summary: Enumerate or count all occurrences of small subgraph patterns.
model: word-ram
complexity:
  vars: {n: the number of vertices, k: "the pattern size, a fixed constant"}
  time: {worst: O(n^k)}
prereqs: [network-motif, subgraph-isomorphism, triangle-counting]
see_also: [network-motif, triangle-counting, triangle-listing-by-degree, subgraph-isomorphism, color-coding, clique-problem, streaming-triangle-counting-problem, graph-isomorphism-problem]
sources:
  - paper: doi:10.1109/TCBB.2006.51
    title: Sebastian Wernicke, Efficient detection of network motifs, IEEE/ACM Transactions on Computational Biology and Bioinformatics 3(4), 347 to 359 (2006)
    locator: the ESU algorithm that lists each connected induced subgraph of size k exactly once, and its sampling version RAND-ESU
  - paper: doi:10.1093/bioinformatics/bth163
    title: N. Kashtan, S. Itzkovitz, R. Milo and U. Alon, Efficient sampling algorithm for estimating subgraph concentrations and detecting network motifs, Bioinformatics 20(11), 1746 to 1758 (2004)
    locator: the edge-sampling estimator of subgraph concentrations and its bias correction
  - paper: doi:10.1093/bioinformatics/btt717
    title: Tomaž Hočevar and Janez Demšar, A combinatorial approach to graphlet counting, Bioinformatics 30(4), 559 to 565 (2014)
    locator: the ORCA method, which counts the orbits of graphlets with 4 and 5 vertices for every vertex from a system of linear equations between orbit counts
  - paper: doi:10.1145/210332.210337
    title: Noga Alon, Raphael Yuster and Uri Zwick, Color-coding, Journal of the ACM 42(4), 844 to 856 (1995)
    locator: the method of random colourings for finding and counting paths, trees and other patterns of bounded treewidth with k vertices in time exponential only in k
  - paper: doi:10.1126/science.298.5594.824
    title: R. Milo, S. Shen-Orr, S. Itzkovitz, N. Kashtan, D. Chklovskii and U. Alon, Network motifs, simple building blocks of complex networks, Science 298(5594), 824 to 827 (2002)
    locator: the counting of all patterns with 3 and 4 vertices in the real network and in randomized networks
---

Network motif enumeration asks, for a graph $G$ and a small size $k$, how many times each connected pattern on $k$ vertices occurs in $G$ as an induced subgraph; the listing version asks for the occurrences themselves. These counts are the raw material of [network motifs](/network-motif/), which compare them with the counts in random graphs, and of graphlet statistics. The standard exact method, Wernicke's ESU, lists every connected set of $k$ vertices exactly once and classifies it, and faster methods count without listing, by algebraic relations between the counts or by random sampling. For general $k$ the problem contains counting [cliques](/clique-problem/), so no algorithm is expected to run in time $f(k) \cdot n^{O(1)}$.

## In plain words

Pick a small number, such as three or four. Look at every group of that many members of a network that are linked together, and sort the groups by their shape: three members in a chain, three in a closed triangle, four in a square, four around a hub, and so on. The task is to count how many groups of each shape the network has.

There are few shapes, but the groups can be very many, because a large network has a huge number of small groups. Good methods avoid looking at the same group twice, skip groups that are not linked together, and sometimes count shapes from simpler counts without listing any group.

## Definition

**Input.** A graph $G = (V, E)$ with $n$ vertices and $m$ edges, given as an [adjacency list](/adjacency-list/), undirected or directed, and an integer $k \ge 2$. Weights are ignored.

**Output.** For each pattern $H$ (a connected, or weakly connected, graph on $k$ vertices up to isomorphism), the number $N_G(H)$ of sets $S \subseteq V$ of size $k$ whose induced subgraph $G[S]$ is isomorphic to $H$. In the listing version, the sets $S$ with their patterns.

Sets that induce a disconnected subgraph are not counted; $G$ itself may be disconnected, and then every counted set lies in one component. Each set is counted once, not once per labelling or per automorphism.

## Variants

- **Non-induced counts.** Count the subgraphs of $G$ isomorphic to $H$, induced or not. For a fixed $k$, the vectors of induced and non-induced counts are related by an invertible linear map: a non-induced copy of $H$ sits inside exactly one induced pattern, and each induced pattern contains a fixed number of copies of each smaller-edged pattern.
- **Orbit counts (graphlet degrees).** For each vertex $v$ and each orbit of the automorphism group of each pattern, count the occurrences in which $v$ plays that role. This gives a vector per vertex, with 73 entries for patterns on 2 to 5 vertices.
- **One pattern.** Count a single given pattern, such as triangles ([triangle counting](/triangle-counting/)), $k$-cliques, or $k$-paths. This is subgraph counting, the counting form of [subgraph isomorphism](/subgraph-isomorphism/).
- **Approximate counts.** Estimate the counts, or the relative frequencies of the patterns, by sampling connected sets.
- **Streaming and distributed.** Count with one pass over the edges, as in the [streaming triangle counting problem](/streaming-triangle-counting-problem/), or on many machines.

## Examples

Take the fan on $0, \ldots, 5$: the hub 0 joined to $1, \ldots, 5$, and the path $1 - 2 - 3 - 4 - 5$. Its 9 edges give the degrees $5, 2, 3, 3, 3, 2$.

**$k = 3$.** Of the $\binom{6}{3} = 20$ sets, 13 are connected: 4 triangles ($\{0, i, i+1\}$ for $i = 1, \ldots, 4$) and 9 open paths. The open paths also follow from the identity

$$N(\text{open path}) = \sum_v \binom{d(v)}{2} - 3\, N(\text{triangle}) = (10 + 1 + 3 + 3 + 3 + 1) - 12 = 9,$$

since each vertex $v$ is the middle of $\binom{d(v)}{2}$ connected triples, and each triangle contains three of them.

**$k = 4$.** Of the 15 sets, 12 are connected. The counts are:

| pattern | count | occurrences |
|---|---|---|
| star $K_{1,3}$ | 1 | $\{0, 1, 3, 5\}$ |
| path $P_4$ | 2 | $\{1, 2, 3, 4\}$, $\{2, 3, 4, 5\}$ |
| triangle with a pendant edge (paw) | 6 | |
| diamond ($K_4$ minus an edge) | 3 | $\{0, i, i+1, i+2\}$ for $i = 1, 2, 3$ |
| cycle $C_4$ | 0 | |
| clique $K_4$ | 0 | |

The 3 sets that are not connected are $\{1, 2, 4, 5\}$, $\{1, 2, 3, 5\}$ and $\{1, 3, 4, 5\}$.

## Known algorithms

- **Brute force.** Test all $\binom{n}{k}$ sets for connectivity and classify each connected one. Time $O(n^k)$ for a fixed $k$.
- **ESU (Wernicke 2006).** Grow connected sets from a root $v$, adding only vertices with larger numbers than $v$, and taking each new vertex from an *extension set* that holds the neighbours of the current set that are larger than $v$ and were not already neighbours before the last vertex was added. Each connected induced set of size $k$ is produced exactly once, from its smallest vertex, so the time is the number of connected $k$-sets times a polynomial in $k$ and the degrees. Each set is then classified by a canonical form, for example with nauty; for small $k$ a lookup table of the $2^{\binom{k}{2}}$ adjacency patterns is faster. The search uses an explicit stack, without recursion.
- **RAND-ESU.** Follow each branch of the ESU tree at depth $d$ with probability $p_d$; every connected set is sampled with the same probability $\prod_d p_d$, so the counts divided by it are unbiased estimates. The earlier edge-sampling method of Kashtan and coauthors samples sets with unequal probabilities and needs a correction.
- **Counting by equations.** Counts of larger patterns follow from counts of smaller ones and of a few special patterns, as in the identity for open paths above. ORCA uses such linear relations between orbit counts to count all orbits of patterns with 4 vertices in $O(m \Delta)$ time and those with 5 vertices in $O(m \Delta^2)$ time, where $\Delta$ is the largest degree, listing only cliques and a few other patterns directly.
- **Triangles and degree ordering.** For $k = 3$, the counts follow from the degrees and the triangle count, and [listing by degree](/triangle-listing-by-degree/) gives the triangles in $O(m^{3/2})$ time.
- **[Color-coding](/color-coding/).** Colour the vertices at random with $k$ colours and count the *colourful* occurrences by dynamic programming; for paths and trees this takes $2^{O(k)} m$ time per colouring, and repeating it gives approximate counts. Bressan and others built fast motif samplers on this idea.

## Bounds

- **Output size.** In the complete graph every one of the $\binom{n}{k}$ sets is an occurrence, so listing needs $\Omega(n^k)$ time in the worst case for fixed $k$; only counting can beat this.
- **Clique hardness.** The $k$-clique is one of the patterns, so any algorithm for the counts also counts $k$-cliques. Counting $k$-cliques is #W[1]-hard with parameter $k$, so an algorithm with time $f(k) \cdot n^{O(1)}$ would be a major surprise. The best known clique algorithms, by fast [matrix multiplication](/matrix-multiplication-exponent/) (Nešetřil and Poljak), take about $n^{\omega k/3}$ time.
- **Small $k$.** For $k = 3$ the problem is as hard as counting triangles, which is linked to [Boolean matrix multiplication](/boolean-matrix-multiplication/) and the [triangle detection hypothesis](/triangle-detection-hypothesis/).

## Reductions

- **From $k$-clique counting.** Run any motif counter with size $k$ and read off the count of $K_k$.
- **To smaller counts.** The induced counts of patterns on $k$ vertices are a fixed invertible linear transform of the non-induced counts, and many non-induced counts are polynomials in degree statistics and in the counts of cliques and cycles. So a few hard counts (cliques, cycles) plus linear algebra give the whole vector.
- **Classification to graph isomorphism.** Assigning a pattern to each found set is the [graph isomorphism problem](/graph-isomorphism-problem/) on $k$ vertices, which for small $k$ is a table lookup.

## Applications

- [Network motifs](/network-motif/): the counts in the real network against those in randomized networks.
- Network comparison: the graphlet degree distribution and graphlet frequency vectors compare protein interaction networks and other biological networks.
- Vertex features: orbit counts per vertex are input features for link prediction and vertex classification.
- Social networks: the triad census of directed triads, and the [clustering coefficient](/clustering-coefficient/) from triangles and triples.

## References
