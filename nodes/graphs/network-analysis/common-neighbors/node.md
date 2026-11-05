---
tag: CQP4WB
kind: definition
slug: common-neighbors
name: Common neighbors
area: graphs/network-analysis
level: intro
summary: The number of vertices adjacent to both u and v, a basic score of how similar two vertices are and how likely they are to link.
prereqs: [graph, neighborhood]
see_also: [adamic-adar-index, link-prediction, node-similarity, triadic-closure, clustering-coefficient, adjacency-matrix]
sources:
  - paper: doi:10.1002/asi.20591
    title: David Liben-Nowell and Jon Kleinberg, The link-prediction problem for social networks, Journal of the American Society for Information Science and Technology 58(7), 1019 to 1031 (2007)
    locator: the section on methods based on node neighborhoods (common neighbors, Jaccard's coefficient, Adamic/Adar, preferential attachment), and the tables of results
  - paper: doi:10.1103/PhysRevE.64.025102
    title: M. E. J. Newman, Clustering and preferential attachment in growing networks, Physical Review E 64, 025102 (2001)
    locator: the whole paper (the probability of a new collaboration as a function of the number of common neighbours)
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 7, Measures and metrics (the section on similarity, cosine similarity and the count of common neighbours)
---

The common-neighbors score of two [vertices](/vertex/) $u$ and $v$ is the number of vertices adjacent to both, $|N(u) \cap N(v)|$. It equals the number of paths of length 2 between $u$ and $v$, so it is the entry $(A^2)_{uv}$ of the square of the [adjacency matrix](/adjacency-matrix/). It is the simplest score for [node similarity](/node-similarity/) and for [link prediction](/link-prediction/): two people with many friends in common are likely to become friends, which is the idea of [triadic closure](/triadic-closure/).

## Definition

Let $G = (V, E)$ be a simple undirected graph and $N(x)$ the [neighborhood](/neighborhood/) of $x$. For $u, v \in V$,

$$\mathrm{CN}(u, v) = |N(u) \cap N(v)|.$$

With the adjacency matrix $A$, $\mathrm{CN}(u, v) = \sum_{w} A_{uw} A_{wv} = (A^2)_{uv}$, because the term for $w$ is 1 exactly when $u - w - v$ is a path of length 2. On the diagonal, $(A^2)_{uu} = d(u)$.

**Normalized forms.** The raw count favours pairs of high degree. Common normalizations, for pairs where the denominator is not 0, are

- the *Jaccard coefficient* $\dfrac{|N(u) \cap N(v)|}{|N(u) \cup N(v)|}$;
- the *cosine* or Salton index $\dfrac{|N(u) \cap N(v)|}{\sqrt{d(u)\, d(v)}}$;
- the [Adamic-Adar index](/adamic-adar-index/), which weights each common neighbour $w$ by $1/\log d(w)$.

**Directed graphs.** In a directed graph there are two counts: the number of common out-neighbours $|N^+(u) \cap N^+(v)|$, which is the bibliographic coupling of $u$ and $v$, and the number of common in-neighbours $|N^-(u) \cap N^-(v)|$, which is the co-citation count. They are the entries of $A A^\top$ and $A^\top A$.

**Weighted graphs.** With weights $w \ge 0$ on the edges, one common choice is $\sum_{x} w(u, x)\, w(x, v)$, the entry of $W^2$ for the weight matrix $W$. Other choices, such as the sum of the minima, exist. Each one must be named.

**Ties and disconnected graphs.** The score is a small integer, so many pairs tie. A ranked list of candidate links must break ties, for example by a second score such as Adamic-Adar, or at random with a fixed seed. If $u$ and $v$ are at distance more than 2, and in particular in different components, then $\mathrm{CN}(u, v) = 0$. So the score cannot rank pairs that are far apart: they all tie at 0.

**Cost.** For one pair, with the neighbours of the vertex of larger degree in a hash set, the score takes $O(\min(d(u), d(v)))$ expected time. With sorted adjacency lists, a merge takes $O(d(u) + d(v))$ time. To get all pairs with a positive score, list for each $w$ all pairs of its neighbours. This takes $\Theta\bigl(n + \sum_w \binom{d(w)}{2}\bigr)$ time, the number of paths of length 2, which can be $\Theta(n^2)$ even when $m = n - 1$ (a star). A dense matrix product computes $A^2$ in $O(n^\omega)$ time.

## Examples and non-examples

**A worked example.** Take the undirected graph with the vertices 0 to 6 and the 9 edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$. The table lists the non-adjacent pairs with a positive score. All other non-adjacent pairs, such as $\{0, 4\}$, score 0.

| pair | common neighbours | CN | Jaccard |
|---|---|---|---|
| 0, 3 | 1, 2 | 2 | 2/3 |
| 1, 4 | 3 | 1 | 1/5 |
| 2, 4 | 3 | 1 | 1/5 |
| 3, 5 | 4 | 1 | 1/4 |
| 3, 6 | 4 | 1 | 1/4 |

As a link predictor, CN puts $\{0, 3\}$ first and then has a four-way tie. Jaccard breaks the tie in favour of $\{3, 5\}$ and $\{3, 6\}$, because $N(3) \cup N(5) = \{1, 2, 4, 6\}$ is smaller than $N(1) \cup N(4) = \{0, 2, 3, 5, 6\}$.

**A star.** In the star $K_{1,k}$, any two leaves have exactly one common neighbour, the centre. So all $\binom{k}{2}$ pairs of leaves tie with CN = 1.

**A complete bipartite graph.** In $K_{a,b}$, two vertices on the same side have the whole other side in common, so their CN is $b$ or $a$, while two vertices on opposite sides are adjacent and have CN = 0.

**Non-examples.**

- The number of common neighbours is not a distance. Two vertices at distance 2 can have CN = 1 or CN = 100, and two adjacent vertices can have CN = 0.
- $(A^3)_{uv}$ counts walks of length 3, not common neighbours. It is the next term of the [Katz](/katz-centrality/) family of path-counting scores.
- In a [multigraph](/multigraph/), $(A^2)_{uv}$ counts paths with multiplicity, so it can be larger than $|N(u) \cap N(v)|$.

## Related definitions

- [Adamic-Adar index](/adamic-adar-index/): common neighbours weighted by the inverse log of their degree.
- [Link prediction](/link-prediction/) and [node similarity](/node-similarity/): the problems that use the score.
- [Triadic closure](/triadic-closure/) and [clustering coefficient](/clustering-coefficient/): the closed triangles that a high count tends to produce.
- [Structural equivalence](/structural-equivalence/): two vertices with exactly the same neighbours.
- [SimRank](/simrank/): a recursive similarity in which the neighbours need only be similar, not equal.

## References
