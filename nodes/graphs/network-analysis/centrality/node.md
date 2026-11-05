---
tag: S9TQAT
kind: concept
slug: centrality
name: Centrality
aliases:
- centrality index
- centrality measure
area: graphs/network-analysis
level: intro
summary: A score for each vertex that says how important or central the vertex is in a network.
prereqs: [graph, degree, shortest-path]
see_also: [degree-centrality, closeness-centrality, harmonic-centrality, betweenness-centrality, eigenvector-centrality, katz-centrality, pagerank, k-core]
sources:
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 7, Measures and metrics (the sections on degree, eigenvector, Katz, PageRank, hubs and authorities, closeness and betweenness centrality)
  - book: isbn:9780521387071
    title: Stanley Wasserman and Katherine Faust, Social Network Analysis, Methods and Applications, Cambridge University Press, 1994
    locator: Chapter 5, Centrality and prestige
  - paper: doi:10.1016/0378-8733(78)90021-7
    title: Linton C. Freeman, Centrality in social networks, conceptual clarification, Social Networks 1(3), 215 to 239 (1979)
    locator: the whole paper (degree, betweenness and closeness, and the centralization of a graph)
  - paper: doi:10.1080/15427951.2013.865686
    title: Paolo Boldi and Sebastiano Vigna, Axioms for centrality, Internet Mathematics 10(3-4), 222 to 262 (2014)
    locator: Sections 2 and 3 (the measures compared, and the size, density and score-monotonicity axioms)
---

A centrality measure is a function that gives each [vertex](/vertex/) of a [graph](/graph/) a real number, its score, so that a larger score means a more important vertex in some sense that the measure fixes. There is no single centrality: the [degree](/degree/) counts neighbours, [closeness](/closeness-centrality/) and [betweenness](/betweenness-centrality/) use [shortest paths](/shortest-path/), and [eigenvector centrality](/eigenvector-centrality/) and [PageRank](/pagerank/) use the scores of the neighbours. On the same graph, these measures can rank the vertices in different orders.

## In plain words

In a group of friends, who is the most important person? One answer is the person with the most friends. Another is the person who can reach everyone in the fewest steps. A third is the person that many messages must pass through, because that person joins two groups. A fourth is the person whose friends are themselves important.

Each answer is a rule that turns the network into one number for each person. Such a rule is a centrality measure. The rules do not agree. A person who joins two groups can have few friends but carry a lot of traffic. So before you compute a centrality, decide what "important" means for your question, and pick the measure that matches it.

## The idea

Let $G = (V, E)$ be a graph with $n$ vertices and $m$ edges. A centrality index is a map $c : V \to \mathbb{R}$. An index must depend only on the structure of the graph: if $\phi$ is an isomorphism from $G$ to $G'$, then $c_{G'}(\phi(v)) = c_G(v)$. So two vertices that a symmetry of the graph exchanges get the same score. Only the order of the scores matters for a ranking, so a measure is often given up to a positive factor.

The common measures fall into a few families.

| family | the score of $v$ depends on | examples |
|---|---|---|
| local | the edges at $v$ | [degree centrality](/degree-centrality/) |
| distance | the distances $d(v, u)$ to the other vertices | [closeness centrality](/closeness-centrality/), [harmonic centrality](/harmonic-centrality/), [eccentricity](/eccentricity/) |
| path counting | the share of shortest paths that pass through $v$ | [betweenness centrality](/betweenness-centrality/) |
| spectral | the scores of the neighbours of $v$, a fixed point of a linear map | [eigenvector centrality](/eigenvector-centrality/), [Katz centrality](/katz-centrality/), [PageRank](/pagerank/), [HITS](/hits-algorithm/) |
| cohesion | the densest part of the graph that holds $v$ | the core number of the [k-core](/k-core/) |

**Directed and weighted graphs.** Each family has a directed form. In a directed graph, the in-degree and the scores from in-links measure *prestige* (others point to $v$), and the out-degree measures activity. With edge weights, a distance measure uses weighted shortest paths, where a weight is a length, and a spectral measure uses the weighted [adjacency matrix](/adjacency-matrix/), where a weight is a strength. Mixing up the two readings of a weight is a common mistake: a strong tie is a short distance, not a long one.

**Disconnected graphs.** Distance measures need a rule for $d(v, u) = \infty$. Classic closeness is not defined there, which is why [harmonic centrality](/harmonic-centrality/) adds $1/d(v, u)$ and lets $1/\infty = 0$. Spectral measures on a graph that is not strongly connected can give a zero score to many vertices, which is one reason for the damping in [PageRank](/pagerank/) and in [Katz centrality](/katz-centrality/).

**Ties.** Equal scores are common, for example among the leaves of a star. A ranking must then either report the ties or break them by a fixed rule, such as the vertex number. A reported top list of $k$ vertices can depend on this rule.

**Normalization.** To compare graphs of different sizes, one divides by the largest possible value, for example $n - 1$ for the degree and $(n-1)(n-2)/2$ for the betweenness in an undirected graph. Freeman also defined the *centralization* of a whole graph: $\sum_v (c^* - c(v))$, where $c^*$ is the largest score, divided by the largest value that this sum takes over all graphs with $n$ vertices. The star has centralization 1 for degree, closeness and betweenness.

**Axioms.** Boldi and Vigna (2014) test the measures against three axioms: the size axiom (in a graph of a $k$-clique and a directed $p$-cycle, the larger part wins when it is much larger), the density axiom (when the clique and the cycle have the same size and are joined, the clique side wins), and score monotonicity (a new arc $x \to y$ raises the score of $y$). In their study, harmonic centrality meets all three, while closeness, betweenness and eigenvector centrality each fail at least one.

## Examples

Take the undirected graph with the vertices 0 to 6 and the 9 edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$. It is a dense group $\{0, 1, 2, 3\}$ and a triangle $\{4, 5, 6\}$, joined by the edge $\{3, 4\}$.

| vertex | degree | sum of distances | closeness $\frac{n-1}{\sum_u d(v,u)}$ | betweenness | eigenvector (max 1) |
|---|---|---|---|---|---|
| 0 | 2 | 15 | 0.400 | 0 | 0.738 |
| 1 | 3 | 11 | 0.545 | 2 | 1.000 |
| 2 | 3 | 11 | 0.545 | 2 | 1.000 |
| 3 | 3 | 9 | 0.667 | 9 | 0.971 |
| 4 | 3 | 10 | 0.600 | 8 | 0.631 |
| 5 | 2 | 14 | 0.429 | 0 | 0.369 |
| 6 | 2 | 14 | 0.429 | 0 | 0.369 |

- Degree gives a four-way tie between 1, 2, 3 and 4.
- Closeness and betweenness both rank vertex 3 first. Each shortest path from $\{0, 1, 2\}$ to $\{4, 5, 6\}$ passes through 3, which gives 9 pairs, and each shortest path from $\{0, 1, 2, 3\}$ to $\{5, 6\}$ passes through 4, which gives 8 pairs.
- Eigenvector centrality ranks 1 and 2 first. They sit in the dense group, and their neighbours have high scores too. Vertex 4 has the same degree as vertex 1 but a much lower eigenvector score, because its neighbours 5 and 6 are weak.
- The largest eigenvalue of the adjacency matrix is about 2.709.

**The star.** In the star $K_{1,k}$ with centre $c$ and $k \ge 2$ leaves, the centre has degree $k$, closeness 1 and betweenness $\binom{k}{2}$, the largest possible values. Each leaf has degree 1, betweenness 0 and closeness $k / (2k - 1)$. All measures agree here.

**A path.** In a path with 5 vertices, the betweenness of the vertices is $0, 3, 4, 3, 0$ and the sums of distances are $10, 7, 6, 7, 10$. The middle vertex wins for both, and the ends tie.

## Where it is used

- Social network analysis: find the leaders, the brokers and the people that hold a group together. See [betweenness centrality](/betweenness-centrality/) and [ego networks](/ego-network/).
- Web search: rank pages by the links that point to them, with [PageRank](/pagerank/) and [HITS](/hits-algorithm/). See [link analysis ranking](/link-analysis-ranking/).
- Infrastructure: find the routers, roads or power lines whose loss cuts the most traffic, with betweenness and edge betweenness. The [Girvan-Newman algorithm](/girvan-newman-algorithm/) removes edges of high betweenness to find communities.
- Epidemics and influence: choose the vertices to vaccinate or to seed, see [influence maximization](/influence-maximization/).
- Algorithms: the cost of computing the measures is its own topic. Degree takes $O(n + m)$ time, closeness and betweenness need all shortest paths (see [Brandes' algorithm](/brandes-algorithm/) and [betweenness centrality computation](/betweenness-centrality-computation/)), and the spectral measures use [power iteration](/power-iteration/).

## References
