---
tag: Q3HK4E
kind: definition
slug: network-motif
name: Network motif
aliases:
- graphlet
- subgraph motif
area: graphs/network-analysis
level: advanced
summary: Small connected subgraph that occurs far more often than in random networks.
prereqs: [subgraph-isomorphism, configuration-model, triangle-counting]
see_also: [network-motif-enumeration, triangle-counting, subgraph-isomorphism, configuration-model, clustering-coefficient, triadic-closure, color-coding, graph-motif]
sources:
  - paper: doi:10.1126/science.298.5594.824
    title: R. Milo, S. Shen-Orr, S. Itzkovitz, N. Kashtan, D. Chklovskii and U. Alon, Network motifs, simple building blocks of complex networks, Science 298(5594), 824 to 827 (2002)
    locator: the definition of motifs by comparison with randomized networks that keep the degrees, the criteria for significance, and the motifs found in gene regulation, neuron, food web, electronic circuit and web networks
  - paper: doi:10.1038/ng881
    title: Shai S. Shen-Orr, Ron Milo, Shmoolik Mangan and Uri Alon, Network motifs in the transcriptional regulation network of Escherichia coli, Nature Genetics 31, 64 to 68 (2002)
    locator: the feed-forward loop, the single-input module and the dense overlapping regulons as motifs of the E. coli network
  - paper: doi:10.1093/bioinformatics/btl301
    title: Nataša Pržulj, Biological network comparison using graphlet degree distribution, Bioinformatics 23(2), e177 to e183 (2007)
    locator: the 30 graphlets on 2 to 5 vertices, their 73 automorphism orbits, and the graphlet degree distribution
  - paper: doi:10.1038/nrg2102
    title: Uri Alon, Network motifs, theory and experimental approaches, Nature Reviews Genetics 8, 450 to 461 (2007)
    locator: the review of the functions of the feed-forward loop and the other transcription motifs
  - book: isbn:9780521387071
    title: Stanley Wasserman and Katherine Faust, Social Network Analysis, Methods and Applications, Cambridge University Press, 1994
    locator: Chapter 14, Triads (the triad census of the 16 isomorphism types of directed triads)
---

A network motif is a small connected pattern of links, such as a triangle or a feed-forward loop, that occurs in a network much more often than in random networks with the same [degrees](/degree/). Milo and coauthors (2002) defined motifs this way and found that different kinds of networks, such as gene regulation, neurons and food webs, are rich in different patterns. A *graphlet* is any small connected induced subgraph, counted without the comparison; graphlet counts describe a network's local shape. Counting the occurrences is the [motif enumeration](/network-motif-enumeration/) problem.

## Definition

**Patterns.** Fix a size $k$, usually 3 to 5. A *pattern* is a graph $H$ on $k$ vertices that is connected (weakly connected, if directed), taken up to isomorphism. The patterns can be listed by brute force for small $k$:

| $k$ | undirected patterns | directed patterns |
|---|---|---|
| 2 | 1 | 2 |
| 3 | 2 | 13 |
| 4 | 6 | 199 |
| 5 | 21 | 9364 |

The 2 + 6 + 21 undirected patterns, with the single edge, are Pržulj's 30 graphlets.

**Occurrences.** Let $G$ be a graph of the same kind (directed or not). An *occurrence* of $H$ is a set $S$ of $k$ vertices such that the subgraph of $G$ induced on $S$ is isomorphic to $H$. The *count* $N_G(H)$ is the number of such sets. Some papers count *non-induced* occurrences instead, the subgraphs of $G$ (not necessarily induced) that are isomorphic to $H$; the two counts are related by a linear transformation, but they differ, so the choice must be stated. The definition uses only the presence of edges: weights are ignored, and a weighted network is first thresholded. $G$ need not be connected; occurrences lie inside its connected components, since $H$ is connected.

**The null model.** Let $\mathcal R$ be a distribution on random graphs with the same vertex set as $G$ and the same degrees: in-degrees and out-degrees for a directed graph, and usually also the number of mutual (two-way) links at each vertex. It is sampled by repeated edge swaps that replace $a \to b$ and $c \to d$ by $a \to d$ and $c \to b$ when no loop or repeated arc results, or by the [configuration model](/configuration-model/). Write $\mu_H$ and $\sigma_H$ for the mean and the standard deviation of $N_R(H)$ for $R \sim \mathcal R$, estimated from samples. The *Z-score* of $H$ is

$$Z_H = \frac{N_G(H) - \mu_H}{\sigma_H}.$$

**Motifs.** $H$ is a *motif* of $G$ when $N_G(H)$ is significantly above $\mu_H$: a large $Z_H$, or a small empirical probability $\Pr[N_R(H) \ge N_G(H)]$. Milo and coauthors also asked for a minimum number of occurrences, so that a pattern seen once or twice does not count, and for the excess $N_G(H) - \mu_H$ to be a noticeable fraction of $\mu_H$. A pattern significantly *below* the null model is an *anti-motif*. For $k = 4$ and more, the null model often also keeps the counts of the patterns on 3 vertices, so that a 4-vertex motif is not just a consequence of many triangles.

Since the definition depends on the null model, on the threshold and on induced or non-induced counting, "motif" always means "motif with respect to a stated null model".

## Examples and non-examples

**The feed-forward loop.** The directed pattern $x \to y$, $y \to z$, $x \to z$, with no other arcs among the three, is the *feed-forward loop* (FFL). It is the main motif of the transcription networks of *E. coli* and yeast (Shen-Orr and coauthors): a regulator $x$ acts on a target $z$ both directly and through a second regulator $y$, which can filter out short pulses of input.

**A motif in a small network.** Join four feed-forward loops on $\{0, 1, 2\}$, $\{3, 4, 5\}$, $\{6, 7, 8\}$ and $\{9, 10, 11\}$ by the arcs $2 \to 3$, $5 \to 6$, $8 \to 9$ and $11 \to 0$. This graph has 12 vertices, 16 arcs and $N_G(\mathrm{FFL}) = 4$ induced FFLs. Over 1000 random graphs with the same in-degrees and out-degrees, made by edge swaps, the FFL count had mean $0.33$ and standard deviation $0.53$, and no sample reached 4 (the largest was 3). So $Z \approx 6.9$, and the FFL is a motif of this graph.

**A non-motif with the same count range.** A graph on 8 vertices with the 13 arcs $0 \to 1$, $1 \to 2$, $0 \to 2$, $0 \to 3$, $3 \to 4$, $0 \to 4$, $2 \to 5$, $4 \to 5$, $2 \to 6$, $5 \to 6$, $6 \to 7$, $1 \to 7$ and $3 \to 7$ has 3 induced FFLs, but its random versions have $2.1$ on average, with a standard deviation of about $1.0$, and 34 percent of them have 3 or more. Its $Z \approx 0.9$, so the FFL is not a motif there: the high count follows from the degrees, mostly from the vertex 0 with out-degree 3.

**Triangles in social networks.** In an undirected friendship network, the triangle is usually a strong motif: the [clustering coefficient](/clustering-coefficient/) is far above that of a random graph with the same degrees, because of [triadic closure](/triadic-closure/).

**Non-examples.**

- A pattern that is not connected, such as two disjoint edges, is not a motif or a graphlet: its count is mostly determined by the counts of its parts.
- A frequent pattern is not a motif by frequency alone. In almost any sparse network the path on three vertices is the most frequent pattern, but it is rarely above its count in the null model.
- The [graph motif](/graph-motif/) problem of computational biology is a different notion: it asks for a connected set of vertices whose colours form a given multiset, with no fixed shape.

## Related definitions

- [Network motif enumeration](/network-motif-enumeration/): the computational problem of counting all occurrences of all patterns of size $k$.
- [Subgraph isomorphism](/subgraph-isomorphism/): finding one occurrence of a given pattern, NP-hard when the pattern is part of the input; motifs keep $k$ small.
- [Triangle counting](/triangle-counting/): the count of the only cyclic pattern on 3 vertices.
- [Clustering coefficient](/clustering-coefficient/): a ratio of the two undirected patterns on 3 vertices, triangles against connected triples.
- [Configuration model](/configuration-model/): the standard null model with given degrees.
- Graphlet degree vector: for each vertex, the number of graphlets that touch it in each automorphism orbit (73 orbits for graphlets on 2 to 5 vertices), used to compare vertices and networks.
- Triad census: the counts of all 16 isomorphism types of directed graphs on 3 vertices (including the 3 that are not connected), a classical tool of social network analysis.
- [Color-coding](/color-coding/): a randomized method that counts occurrences of patterns with $k$ vertices in time exponential only in $k$.

## References
