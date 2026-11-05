---
tag: A707GV
kind: problem
slug: node-similarity
name: Node similarity
aliases:
- vertex similarity
area: graphs/network-analysis
level: core
summary: Compute similarity scores between pairs of nodes.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n^2 + n m)}
prereqs: [graph, neighborhood, degree, adjacency-matrix]
see_also: [common-neighbors, adamic-adar-index, simrank, katz-centrality, personalized-pagerank, structural-equivalence, link-prediction, jaccard-similarity]
sources:
  - paper: doi:10.1002/asi.20591
    title: David Liben-Nowell and Jon Kleinberg, The link-prediction problem for social networks, Journal of the American Society for Information Science and Technology 58(7), 1019 to 1031 (2007)
    locator: Section 3, the list of similarity scores (common neighbours, Jaccard, Adamic-Adar, preferential attachment, Katz, hitting time, rooted PageRank, SimRank) and their comparison on coauthorship networks
  - paper: doi:10.1103/PhysRevE.73.026120
    title: E. A. Leicht, Petter Holme and M. E. J. Newman, Vertex similarity in networks, Physical Review E 73(2), 026120 (2006)
    locator: the distinction between structural and regular equivalence, and the similarity defined by a series over paths of all lengths
  - paper: doi:10.1016/S0378-8733(03)00009-1
    title: Lada A. Adamic and Eytan Adar, Friends and neighbors on the Web, Social Networks 25(3), 211 to 230 (2003)
    locator: the score that weights each shared item by one over the logarithm of its frequency
  - paper: doi:10.1140/epjb/e2009-00335-8
    title: Tao Zhou, Linyuan Lü and Yi-Cheng Zhang, Predicting missing links via local information, European Physical Journal B 71(4), 623 to 630 (2009)
    locator: the resource allocation index and the comparison of local indices on real networks
  - paper: doi:10.1145/775047.775126
    title: Glen Jeh and Jennifer Widom, SimRank, a measure of structural-context similarity, Proceedings of the 8th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 538 to 543 (2002)
    locator: the recursive definition and the iterative computation
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 7, Measures and metrics (the section on similarity, with cosine similarity, the Pearson coefficient and regular equivalence)
---

Node similarity asks for a score $s(u, v)$ that is high when two vertices of a graph play similar parts, for one pair, for all pairs, or for the $k$ vertices most similar to a given one. Local scores look at the shared neighbours, as in [common neighbours](/common-neighbors/), the Jaccard index and the [Adamic-Adar index](/adamic-adar-index/); global scores count walks of all lengths, as in the [Katz](/katz-centrality/) score, [SimRank](/simrank/) and [personalized PageRank](/personalized-pagerank/). There is no single correct score: each choice fixes what "similar" means, and the problem is to compute the chosen one quickly. The main use is [link prediction](/link-prediction/).

## In plain words

Two people are probably alike if they have many friends in common. Two web pages are probably on the same topic if the same pages link to both. Node similarity turns this idea into a number for every pair of members in a network.

There are many ways to make the number. The simplest counts shared friends. Better versions give less credit for a shared friend who knows everyone, since that friend says little about the pair, and some versions divide by how many friends each has, so that popular members do not always win.

Other versions look further than direct friends: friends of friends, and longer chains, all count a little. Two members can then be similar even when they share no friend at all, because their friends are alike.

## Definition

**Input.** A graph $G = (V, E)$ with $n$ vertices and $m$ edges, given as an [adjacency list](/adjacency-list/), and a similarity function $s$ chosen from a family such as the ones below. In the *pair* version, a pair $(u, v)$ is also given; in the *single-source* version, a vertex $u$; in the *all-pairs* version, nothing more.

**Output.** The value $s(u, v)$; or the vector $s(u, \cdot)$, or its $k$ largest entries; or the matrix $(s(u, v))_{u, v}$, or its $k$ largest entries, or its entries above a threshold.

**The local scores.** Let $N(v)$ be the [neighbourhood](/neighborhood/) of $v$ and $d(v) = |N(v)|$ its [degree](/degree/). For an undirected graph without weights:

| score | $s(u, v)$ |
|---|---|
| common neighbours | $\lvert N(u) \cap N(v) \rvert$ |
| Jaccard | $\lvert N(u) \cap N(v) \rvert / \lvert N(u) \cup N(v) \rvert$ |
| cosine (Salton) | $\lvert N(u) \cap N(v) \rvert / \sqrt{d(u) d(v)}$ |
| Adamic-Adar | $\sum_{w \in N(u) \cap N(v)} 1 / \ln d(w)$ |
| resource allocation | $\sum_{w \in N(u) \cap N(v)} 1 / d(w)$ |
| preferential attachment | $d(u)\, d(v)$ |

A shared neighbour $w$ has $d(w) \ge 2$, so the Adamic-Adar terms are finite. The Jaccard and cosine scores are set to 0 when both neighbourhoods are empty. The common-neighbour count is the entry $(A^2)_{uv}$ of the square of the [adjacency matrix](/adjacency-matrix/).

**The global scores.**

- *Katz:* $s(u, v) = \sum_{\ell \ge 1} \beta^\ell (A^\ell)_{uv}$, so $S = (I - \beta A)^{-1} - I$, which converges for $0 < \beta < 1/\lambda_{\max}(A)$.
- *SimRank:* $s(u, u) = 1$, and $s(u, v) = \frac{c}{d(u) d(v)} \sum_{a \in N(u)} \sum_{b \in N(v)} s(a, b)$ for $u \ne v$, with $0 < c < 1$.
- *Random walk with restart:* $s(u, v)$ is the entry $v$ of the personalized PageRank vector of $u$.
- *Embedding similarity:* the cosine of the vectors that a [node embedding](/node-embedding/) gives to $u$ and $v$.

**Directed graphs, weights, ties and components.** On a directed graph each local score has two forms: with in-neighbours (co-citation, two papers cited by the same papers) and with out-neighbours (bibliographic coupling, two papers that cite the same papers). With weights, the sets are replaced by the weighted rows of $A$, for example the cosine of the two rows. When the output is a top-$k$ list, ties in the score are broken by the vertex number, and the tie rule must be stated, because the local scores take few distinct values and produce many ties. Two vertices in different connected components have score 0 under every local score, under Katz and under SimRank, and the random walk score is 0 too, since no walk joins them.

## Variants

- **Structural against regular similarity.** The local scores measure [structural equivalence](/structural-equivalence/): two vertices are similar when they have the same neighbours. SimRank and the Leicht-Holme-Newman score measure regular equivalence: two vertices are similar when their neighbours are similar, even with no neighbour in common.
- **Top-$k$ and threshold joins.** Find all pairs with Jaccard score at least $t$, without computing all $n^2$ scores. MinHash and other locality-sensitive hashing schemes for [Jaccard similarity](/jaccard-similarity/) solve this approximately.
- **Approximate single-source scores.** For personalized PageRank and SimRank, Monte Carlo walks and local push methods give each score with an additive error $\varepsilon$ in time independent of $n$.
- **Learned similarity.** Train vertex vectors with [node2vec](/node2vec/) or [DeepWalk](/deepwalk/) and use their inner products.

## Examples

Take the fan on the vertices $0, \ldots, 5$: the hub 0 is joined to all of $1, \ldots, 5$, and $1 - 2 - 3 - 4 - 5$ is a path. The degrees are $5, 2, 3, 3, 3, 2$.

| pair | shared | CN | Jaccard | cosine | Adamic-Adar | RA | Katz, $\beta = 0.2$ |
|---|---|---|---|---|---|---|---|
| $(1, 3)$ | $\{0, 2\}$ | 2 | 2/3 | 0.816 | 1.532 | 8/15 | 0.168 |
| $(2, 4)$ | $\{0, 3\}$ | 2 | 1/2 | 0.667 | 1.532 | 8/15 | 0.192 |
| $(1, 5)$ | $\{0\}$ | 1 | 1/3 | 0.500 | 0.621 | 1/5 | 0.101 |
| $(1, 4)$ | $\{0\}$ | 1 | 1/4 | 0.408 | 0.621 | 1/5 | 0.129 |

For $(1, 3)$: $N(1) = \{0, 2\}$ and $N(3) = \{0, 2, 4\}$, so the Jaccard score is $2/3$, the Adamic-Adar score is $1/\ln 5 + 1/\ln 3 \approx 0.621 + 0.910$, and the resource allocation score is $1/5 + 1/3 = 8/15$. The hub 0 is a shared neighbour of every pair, and the last two scores give it the least credit. The scores disagree on the order: Jaccard and cosine put $(1, 3)$ first because vertex 1 has few neighbours, while Katz puts $(2, 4)$ first because both ends have degree 3 and so lie on more walks of length 3 and more. The largest eigenvalue of $A$ is about 3.223, so $\beta = 0.2$ is below $1/\lambda_{\max} \approx 0.310$ and the Katz series converges.

**Non-example.** In the [complete bipartite graph](/bipartite-graph/) $K_{3,3}$, two vertices on the same side have Jaccard score 1 and two vertices on opposite sides have score 0, although they are adjacent. A local score says nothing about adjacency itself: it compares neighbourhoods, and the two ends of an edge are not in each other's common neighbourhood.

## Known algorithms

- **One pair, local score.** Put $N(u)$ in a [hash table](/hash-table/) and scan $N(v)$: $O(d(u) + d(v))$ expected time. With sorted lists, a merge takes the same time without hashing.
- **All pairs of common neighbours.** For each vertex $w$ and each pair $a, b$ of its neighbours, add 1 (or $1/d(w)$, or $1/\ln d(w)$) to the entry $(a, b)$. This takes $O(\sum_w d(w)^2) \subseteq O(nm)$ time and gives all the local scores, plus $O(n^2)$ to write a dense output. Alternatively compute $A^2$ by fast [matrix multiplication](/matrix-multiplication-exponent/) in $O(n^\omega)$ time.
- **Katz.** Solve $(I - \beta A) x = e_u$ for one source by [power iteration](/power-iteration/) on the series, with $O(m)$ work per term, or invert the matrix in $O(n^3)$ time for all pairs.
- **SimRank.** The [SimRank algorithm](/simrank/) iterates the recursion on all pairs, with $O(n^2)$ space and $O(\sum_{u, v} d(u) d(v)) = O(m^2)$ time per round.
- **Personalized PageRank.** [Power iteration](/power-iteration/) with restarts, as in [PageRank](/pagerank/), or local push and Monte Carlo methods for one source.
- **Threshold Jaccard joins.** MinHash signatures with banding find the pairs above a threshold with high probability, without comparing every pair; the cost depends on the threshold and on the number of bands.

## Bounds

The all-pairs output has up to $n^2$ entries, so a dense answer needs $\Omega(n^2)$ time. A single local score needs $\Omega(d(u) + d(v))$ time in the worst case for a comparison-based method that reads the lists, since any unread entry could change the intersection. Computing all common-neighbour counts is at least as hard as [Boolean matrix multiplication](/boolean-matrix-multiplication/), by the reduction below, so no combinatorial algorithm is known that does it in $O(n^{3 - \varepsilon})$ time on dense graphs.

## Reductions

**From Boolean matrix multiplication.** Given $n \times n$ Boolean matrices $X$ and $Y$, build a graph on three groups $I$, $K$ and $J$ of $n$ vertices: join $i \in I$ to $k \in K$ when $X_{ik} = 1$, and $k$ to $j \in J$ when $Y_{kj} = 1$. There are no other edges, so the common neighbours of $i$ and $j$ are exactly the $k$ with $X_{ik} = Y_{kj} = 1$, and $|N(i) \cap N(j)| = (XY)_{ij}$ over the integers. So all-pairs common neighbours computes the product, and its Boolean version.

**To matrix multiplication.** In the other direction, the common-neighbour matrix is $A^2$, and the cosine, Jaccard and resource allocation matrices follow from $A^2$, $A D^{-1} A$ and the degrees in $O(n^2)$ more time.

## Applications

- [Link prediction](/link-prediction/): rank the pairs that are not yet joined by their score and predict the top ones. Liben-Nowell and Kleinberg found that the simple Adamic-Adar score did about as well as the global scores on coauthorship networks.
- Recommendation: users who bought similar items, or items bought by similar users, as in collaborative filtering on a [bipartite graph](/bipartite-graph/).
- [Structural equivalence](/structural-equivalence/) and blockmodels: group the vertices whose rows of $A$ are close.
- Clustering: [agglomerative clustering](/agglomerative-clustering/) and [spectral clustering](/spectral-clustering/) take a similarity matrix as input.
- Deduplication of records and entity resolution, where two records are similar when they share attributes.

## References
