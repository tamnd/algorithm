---
tag: GWX6WX
kind: problem
slug: graph-compression
name: Graph compression
aliases:
- web graph compression
area: graphs/graph-representation
level: research
summary: Store a large graph in as few bits as possible while supporting neighbour queries.
prereqs: [compressed-sparse-row, adjacency-list, elias-gamma-coding]
see_also: [webgraph-compression, succinct-graph-representation, compressed-sparse-row, elias-fano-encoding, rank-select-dictionary, information-theoretic-bound, reverse-cuthill-mckee, pagerank]
sources:
  - paper: doi:10.1145/988672.988752
    title: Paolo Boldi and Sebastiano Vigna, The WebGraph framework I, compression techniques, Proceedings of the 13th International World Wide Web Conference (WWW 2004)
    locator: pages 595 to 602, gap encoding of successor lists, reference compression with copy lists, intervals, zeta codes, and the bits per link on web crawls
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 9 (Graphs), the worst-case lower bound, the succinct representations of general and planar graphs, k2-trees and the compression of web and social graphs
  - paper: "Nieves R. Brisaboa, Susana Ladra and Gonzalo Navarro, k2-trees for compact web graph representation, String Processing and Information Retrieval (SPIRE 2009), Lecture Notes in Computer Science 5721, Springer, 2009"
    locator: pages 18 to 30, the k2-tree of the adjacency matrix with direct and reverse neighbour queries
---

Graph compression is the problem of storing a [graph](/graph/) in as few bits as possible while still answering neighbour queries on the stored form, without first decompressing it. A plain [compressed sparse row](/compressed-sparse-row/) array uses about $\log_2 n$ bits for each [edge](/edge/), which for a web graph with billions of vertices is more than 30 bits per edge. Real graphs have structure that a general count does not see, such as neighbours with close numbers and vertices with similar lists, and compressors that use it store web graphs in a few bits per edge with neighbour queries still fast. For arbitrary graphs no method beats the counting lower bound $\log_2 \binom{n^2}{m}$.

## In plain words

A big graph, such as the links between web pages, takes a lot of memory if each link is written as a full page number. But the links are not random. A page links mostly to pages on the same site, so the page numbers in its list are close together, and the differences between them are small numbers that take few bits. Two pages next to each other often have nearly the same links, so one list can say "copy that list, but drop these and add those."

The goal is not only to make the file small. A program must still ask "what are the links of page $v$?" and get the answer quickly, by decoding only the part of the file that holds $v$.

## Definition

**Input.** A directed graph $G = (V, E)$ with $V = \{0, \ldots, n - 1\}$ and $m = |E|$ arcs, unweighted, with $E \subseteq V \times V$. An undirected graph is stored as the directed graph with both arcs of each edge, or with only the arc from the smaller to the larger end.

**Output.** A bit string $S(G)$ and a query procedure that, given $S(G)$ and a vertex $v$, lists the out-neighbours $N^+(v)$ in increasing order. Some variants also ask for the in-neighbours $N^-(v)$, for the out-degree $d^+(v)$, or for the adjacency query "is $(u, v) \in E$?".

**Goal.** Make $|S(G)|$, the number of bits, small, while each query takes time close to $O(1 + d^+(v))$, or within a factor polylogarithmic in $n$. The cost is often reported as *bits per link*, $|S(G)| / m$.

**Baseline.** A [CSR](/compressed-sparse-row/) array with fixed-width entries stores $n + 1$ offsets of $\lceil \log_2 (m + 1) \rceil$ bits and $m$ targets of $\lceil \log_2 n \rceil$ bits, so about $m \log_2 n + n \log_2 m$ bits, and lists $N^+(v)$ in $\Theta(1 + d^+(v))$ time. An [adjacency list](/adjacency-list/) with pointers costs a constant factor more.

## Variants

- **Static or dynamic.** Most compressors are static: built once, then queried. Dynamic compressed graphs, which support inserting and deleting arcs, cost more bits or slower queries.
- **Successors only, or both directions.** Web graph methods often store $G$ and its transpose separately. A k2-tree of the adjacency matrix answers both kinds of query from one structure.
- **Labelled or unlabelled.** If only the graph up to isomorphism matters, up to $\log_2 n! \approx n \log_2 n$ bits can be saved by choosing the numbering. This is the reason that the choice of vertex order is part of the problem.
- **Graph classes.** For a class with few graphs, such as [trees](/tree/) or [planar graphs](/planar-graph/), the target is a constant number of bits per vertex; see [succinct graph representation](/succinct-graph-representation/).
- **Lossy.** [Sparsification](/sparsification/) and graph summarisation drop or merge edges and keep only some properties, such as cuts or distances. This page is about lossless compression.
- **Weighted or attributed.** Weights or labels on the arcs are stored as a second sequence aligned with the targets and compressed separately.

## Examples

**The bound on the running example.** The directed graph on $\{0, \ldots, 4\}$ with the arcs $(0,1), (0,2), (1,2), (2,3), (3,1), (3,4)$ has $n = 5$ and $m = 6$. Its CSR arrays $\mathit{off} = [0, 2, 3, 4, 6, 6]$ and $\mathit{adj} = [1, 2, 2, 3, 1, 4]$ take $6 \cdot 3 + 6 \cdot 3 = 36$ bits with 3-bit entries. There are $\binom{25}{6} = 177\,100$ directed graphs on 5 labelled vertices with 6 arcs, loops allowed, so some of them need $\lceil \log_2 177\,100 \rceil = 18$ bits under any encoding. For such a small graph the gap is a constant factor; for large sparse graphs the question is the factor in front of $m$.

**Gap encoding.** Let vertex $x = 15$ have the sorted successor list $13, 15, 16, 17, 20, 21, 23, 24$. WebGraph writes the first successor relative to $x$ and each later one as the gap to the previous one, minus 1:

| successor | 13 | 15 | 16 | 17 | 20 | 21 | 23 | 24 |
|---|---|---|---|---|---|---|---|---|
| value written | $13 - 15 = -2$, mapped to 3 | 1 | 0 | 0 | 2 | 0 | 1 | 0 |
| Elias gamma code of value + 1 | 5 bits | 3 | 1 | 1 | 3 | 1 | 3 | 1 |

The first value can be negative, so it is mapped to a natural number: $z \ge 0$ to $2z$, and $z < 0$ to $2|z| - 1$. The list then takes $18$ bits, plus 7 bits for the [Elias gamma code](/elias-gamma-coding/) of the out-degree plus 1, $\gamma(9)$. So 25 bits for 8 arcs, about 3.1 bits per link, against $8 \cdot 30 = 240$ bits for 30-bit vertex numbers.

**Reference compression.** Let vertex 16 have the list $13, 15, 16, 17, 21, 23, 24, 30$. It is close to the list of 15, so WebGraph writes a *reference* $r = 1$ (use the list of vertex $16 - 1$), a *copy list* of 8 bits $1\,1\,1\,1\,0\,1\,1\,1$ that keeps all the successors of 15 except 20, and the *extra* successor 30, gap encoded. The copy list itself is stored as run lengths, so long equal runs are cheap.

**Intervals.** A run of consecutive successors, such as $15, 16, 17$, is written as its left end and its length, which helps on graphs with many runs of this kind.

## Known algorithms

| method | idea | queries | typical cost |
|---|---|---|---|
| CSR with fixed-width entries | baseline | $N^+(v)$ in $\Theta(1 + d^+(v))$ | $\approx m \log_2 n$ bits |
| gaps and universal codes | sort each list, write gaps in [Elias gamma](/elias-gamma-coding/), [delta](/elias-delta-coding/) or zeta codes, or in [variable-byte](/variable-byte-encoding/) code | $N^+(v)$ by sequential decoding, from a stored bit offset of $v$ | depends on the locality of the numbering |
| [Elias-Fano](/elias-fano-encoding/) per list | write the list as a monotone sequence with $\approx 2 + \log_2 (n / d)$ bits per element | $N^+(v)$, and the $i$-th successor in $O(1)$, with [rank and select](/rank-select-dictionary/) | worst-case bound, little use of similarity |
| WebGraph (Boldi and Vigna, 2004) | gaps, reference compression within a window of previous lists, intervals, zeta codes | $N^+(v)$ in $O(d^+(v))$ times the reference chain length, which is bounded by a parameter | a few bits per link on web crawls in URL order |
| k2-tree (Brisaboa, Ladra and Navarro, 2009) | split the adjacency matrix into $k^2$ blocks recursively and store one bit for each nonempty block, level by level | $N^+(v)$ and $N^-(v)$, by descending the tree with rank on bit vectors | small when the ones of the matrix cluster |
| reordering, then any method above | number the vertices so that neighbours get close numbers: URL order, BFS order, [label propagation](/label-propagation-algorithm/) layers, or [reverse Cuthill-McKee](/reverse-cuthill-mckee/) | as for the method used | often a large factor smaller than with a random order |
| grammar and virtual nodes | replace a dense bipartite subgraph $A \times B$ by a new vertex with arcs $A \to w \to B$, as in [grammar-based compression](/grammar-based-compression/) | $N^+(v)$ by expanding virtual vertices | good on graphs with many shared lists |

The gap methods depend on the numbering of the vertices: a list of $d$ successors spread over a range of width $R$ costs about $d \log_2 (R / d)$ bits with good codes. So the problem includes choosing a permutation of $V$, and the reordering step is often the most important one.

## Bounds

- **Counting lower bound.** There are $\binom{n^2}{m}$ directed graphs on $n$ labelled vertices with $m$ arcs, loops allowed, so each encoding uses at least $\lceil \log_2 \binom{n^2}{m} \rceil$ bits on some of them. For $m \le n^2/2$ this is $m \log_2 (n^2 / m) + \Theta(m)$ bits. For simple undirected graphs the count is $\binom{\binom{n}{2}}{m}$. See [information-theoretic bound](/information-theoretic-bound/).
- **Random graphs do not compress.** A graph of the [Erdős-Rényi model](/erdos-renyi-model/) with a given $m$ is uniform over the $\binom{n^2}{m}$ graphs, so its expected encoding length is at least $\log_2 \binom{n^2}{m} - O(1)$ bits. Compression below this needs structure that random graphs do not have.
- **Meeting the bound.** Write each arc $(u, v)$ as the integer $un + v$ in $[0, n^2)$ and store the sorted sequence of these $m$ integers with [Elias-Fano](/elias-fano-encoding/). This takes $m (2 + \lceil \log_2 (n^2 / m) \rceil)$ bits plus lower-order terms, within $O(m)$ bits of the counting bound, and [select](/rank-select-dictionary/) returns the $i$-th arc in $O(1)$ time. The arcs out of $u$ form one contiguous range, so after one search for the first integer at least $un$, the list $N^+(u)$ comes out in $O(1 + d^+(u))$ time.
- **Classes.** A class with $2^{O(n)}$ unlabelled graphs on $n$ vertices can be stored in $O(n)$ bits. Trees take $2n + o(n)$ bits with [balanced parentheses](/balanced-parentheses-representation/), and Turán gave an encoding of planar graphs in $12n$ bits; later work brought planar graphs close to the counting bound, with fast queries. See [succinct graph representation](/succinct-graph-representation/).

## Reductions

- **To string compression.** Writing the adjacency matrix row by row as a bit string and applying any lossless compressor, such as [LZW](/lzw/), gives a valid encoding, but neighbour queries then need decompression. The compressors above keep the lists separately addressable.
- **To vertex ordering.** For the gap codes, the cost of a numbering $\pi$ is about $\sum_{(u,v) \in E} \log_2 |\pi(u) - \pi(v)|$, the *minimum logarithmic arrangement* problem. Chierichetti and others showed in 2009 that finding the best $\pi$ is NP-hard, as is the related minimum linear arrangement problem, so practical systems use heuristics such as BFS order and label propagation.
- **From [bandwidth reduction](/bandwidth-reduction/).** A numbering with small bandwidth $\max_{(u,v)} |\pi(u) - \pi(v)| = \beta$ gives each gap at most $\beta$, so $O(m \log \beta)$ bits.

## Applications

- **Web graphs.** Crawls with billions of pages and tens of billions of links are kept in main memory for [PageRank](/pagerank/), link analysis and spam detection; this was the purpose of WebGraph.
- **Social networks.** Friendship and follower graphs are compressed with BFS or label propagation orders, though they have less locality than web graphs.
- **Graph processing systems.** In-memory and out-of-core systems store the graph in a compressed CSR so that more of it fits in cache and memory bandwidth is spent on fewer bits.
- **Bioinformatics and knowledge graphs.** Large sparse relations, such as de Bruijn graphs of reads or the triples of a knowledge base, use k2-trees and related structures.
- **Indexes.** The postings lists of an inverted index are the successor lists of a bipartite graph between terms and documents, and use the same gap codes.

## References
