---
tag: HY4WA6
kind: problem
slug: link-analysis-ranking
name: Link-analysis ranking
aliases:
- web ranking
- hub and authority ranking
area: graphs/network-analysis
level: core
summary: Score the nodes of a hyperlink or citation graph by their importance.
prereqs: [directed-graph, centrality, eigenvector-centrality, markov-chain]
see_also: [pagerank, hits-algorithm, personalized-pagerank, katz-centrality, eigenvector-centrality, degree-centrality, simrank, power-iteration]
sources:
  - paper: doi:10.1145/1052934.1052942
    title: Allan Borodin, Gareth O. Roberts, Jeffrey S. Rosenthal and Panayiotis Tsaparas, Link analysis ranking, algorithms, theory, and experiments, ACM Transactions on Internet Technology 5(1), 231 to 297 (2005)
    locator: the definition of a link analysis ranking algorithm, the survey of InDegree, PageRank, HITS and SALSA, and the results on stability and similarity
  - paper: doi:10.1016/S0169-7552(98)00110-X
    title: Sergey Brin and Lawrence Page, The anatomy of a large-scale hypertextual Web search engine, Computer Networks and ISDN Systems 30(1-7), 107 to 117 (1998)
    locator: Section 2.1, PageRank (the formula with the damping factor d and the random surfer)
  - paper: doi:10.1145/324133.324140
    title: Jon M. Kleinberg, Authoritative sources in a hyperlinked environment, Journal of the ACM 46(5), 604 to 632 (1999)
    locator: the hub and authority scores and their characterization by the principal eigenvectors of the matrices A^T A and A A^T
  - paper: doi:10.1145/382979.383041
    title: R. Lempel and S. Moran, SALSA, the stochastic approach for link-structure analysis, ACM Transactions on Information Systems 19(2), 131 to 160 (2001)
    locator: the two random walks on the bipartite hub and authority graph
  - book: isbn:9780691122021
    title: Amy N. Langville and Carl D. Meyer, Google's PageRank and Beyond, The Science of Search Engine Rankings, Princeton University Press, 2006
    locator: Chapters 4 to 6 (the mathematics of PageRank, dangling nodes, the damping factor and convergence) and Chapter 11 (HITS)
---

Link-analysis ranking is the problem of giving each node of a [directed graph](/directed-graph/) of links, such as web pages and their hyperlinks or papers and their citations, a score of importance that is computed from the links alone. A link from $u$ to $v$ is read as a vote of $u$ for $v$, and the main methods weight each vote by the score of the voter, which makes the scores a fixed point of a linear map. The best-known solutions are [PageRank](/pagerank/), which follows a random surfer, and the [HITS algorithm](/hits-algorithm/), which gives each node a hub score and an authority score.

## In plain words

A search engine finds thousands of pages that contain your words. It must decide which ones to show first. The text alone is easy to fake, but the links between pages are written by many different people.

So treat a link as a vote. A page that many pages link to is probably useful. But a vote from an important page should count more than a vote from an unknown page. That makes the definition go in a circle: a page is important when important pages link to it. The methods of this problem break the circle by repeating the vote counting many times until the scores stop changing.

## Definition

**Input.** A directed graph $G = (V, E)$ with $n$ nodes and $m$ arcs, where an arc $(u, v)$ means that $u$ links to or cites $v$. Self-loops are usually removed, and parallel arcs merged. The basic problem has no weights. Some inputs also give a query, which selects a subgraph, or a set of trusted nodes.

**Output.** A vector $x \in \mathbb{R}_{\ge 0}^V$ of scores, or the ranking of $V$ that it induces. Borodin and co-authors define a link-analysis ranking algorithm as a function from graphs on $n$ nodes to such vectors.

**What makes it a problem.** There is no single correct vector. Each method fixes a rule, and the rules below are the standard ones. Let $A$ be the adjacency matrix, $A_{uv} = 1$ when $(u, v) \in E$, and $d^+(u)$ the out-degree.

- **In-degree.** $x_v = \sum_u A_{uv}$. Simple, but easy to inflate with many links from unimportant nodes.
- **PageRank.** For a damping factor $0 < d < 1$, $x$ is the unique probability vector with
$$x_v = \frac{1 - d}{n} + d \sum_{u : (u,v) \in E} \frac{x_u}{d^+(u)} + d \sum_{u : d^+(u) = 0} \frac{x_u}{n}.$$
It is the stationary distribution of a random surfer who follows a random out-link with probability $d$ and jumps to a uniform node otherwise; a node with no out-links, a *dangling node*, sends the surfer to a uniform node.
- **HITS.** Two vectors: an authority score $a$ and a hub score $h$ with $a \propto A^{\mathsf T} h$ and $h \propto A a$. So $a$ is a principal eigenvector of $A^{\mathsf T} A$ and $h$ one of $A A^{\mathsf T}$.
- **SALSA.** Like HITS, but each vote is divided by the out-degree of the hub and the in-degree of the authority, which makes the scores stationary distributions of two random walks.

**Disconnected graphs and dangling nodes.** Without the jump term, the PageRank walk can be trapped in a set of nodes with no arcs out, and its stationary vector need not be unique. The jump term $(1 - d)/n$ makes the chain irreducible and aperiodic, so the vector exists and is unique, on any graph. HITS has no such term: if the largest eigenvalue of $A^{\mathsf T} A$ is repeated, which happens for example when two parts of the graph give the same value, the limit of the iteration depends on the start vector.

**Ties.** Equal scores are common: nodes with the same in-links get equal PageRank. A ranking must state its tie rule, and an iterative method stops at a tolerance, so two scores closer than the tolerance should be treated as tied.

## Variants

- **Query-dependent ranking.** HITS and SALSA run on a small *focused subgraph* built from the pages that match a query and their neighbours. PageRank is query-independent and computed once.
- **Personalized ranking.** Replace the uniform jump by a jump to a chosen set of nodes: [personalized PageRank](/personalized-pagerank/). It scores nodes by their closeness to that set.
- **Weighted graphs.** Split the vote of $u$ in proportion to the arc weights instead of equally.
- **Walk counts.** [Katz centrality](/katz-centrality/) counts all walks into a node, damped by length, and is the solution of a linear system much like PageRank.
- **Undirected graphs.** On an undirected connected graph, the walk without jumps has the stationary value $\deg(v)/2m$, so PageRank with $d \to 1$ tends to degree. The [eigenvector centrality](/eigenvector-centrality/) is the undirected analogue of HITS.
- **Similarity instead of importance.** [SimRank](/simrank/) uses the same recursive idea to score pairs of nodes.

## Examples

Take the nodes 0 to 5 and the arcs $0 \to 1$, $0 \to 2$, $1 \to 2$, $1 \to 5$, $2 \to 0$, $3 \to 2$, $4 \to 2$, $4 \to 3$. Node 5 is dangling.

| node | in-degree | PageRank, $d = 0.85$ | authority | hub |
|---|---|---|---|---|
| 0 | 1 | 0.3052 | 0 | 0.5251 |
| 1 | 1 | 0.1708 | 0.2399 | 0.5251 |
| 2 | 4 | 0.3107 | 0.9096 | 0 |
| 3 | 1 | 0.0586 | 0.2399 | 0.4155 |
| 4 | 0 | 0.0411 | 0 | 0.5251 |
| 5 | 1 | 0.1137 | 0.2399 | 0 |

The authority and hub vectors have Euclidean norm 1. All three methods put node 2 first. Node 0 has one in-link, but it comes from node 2, which passes all its PageRank to node 0, so PageRank puts node 0 a close second, far above nodes 1, 3 and 5, which also have one in-link. HITS gives node 0 the authority score 0: its only in-link comes from node 2, which links to no good authority and so has hub score 0. The largest eigenvalue of $A^{\mathsf T} A$ here is $(5 + \sqrt{21})/2 \approx 4.791$, and it is simple, so the HITS vectors are unique. The PageRank values sum to 1; node 4 has the smallest value, $(1 - d)/6$ plus its share of the dangling mass, since nothing links to it.

## Known algorithms

| algorithm | output | cost per iteration |
|---|---|---|
| In-degree count | in-degrees | $O(n + m)$ once |
| [PageRank](/pagerank/) by [power iteration](/power-iteration/) | stationary vector of the surfer | $O(n + m)$ |
| [HITS algorithm](/hits-algorithm/) | hub and authority vectors | $O(n + m)$ |
| [Personalized PageRank](/personalized-pagerank/) by push methods | approximate scores near a seed | depends on the seed and the tolerance, not on $n$ |
| [Katz centrality](/katz-centrality/) by iteration | damped walk counts | $O(n + m)$ |

## Bounds

- **PageRank converges geometrically.** The map $x \mapsto$ the right side of the PageRank equation is a contraction with factor $d$ in the $\ell_1$ norm on probability vectors, so after $k$ iterations from any probability vector the $\ell_1$ error is at most $2 d^k$. With $d = 0.85$, about 50 iterations give an error below $10^{-3}$, and about 110 below $10^{-7}$, whatever the size of the graph.
- **HITS converges at the rate of an eigengap.** The power iteration for $A^{\mathsf T} A$ converges at the rate $\lambda_2 / \lambda_1$ of its two largest eigenvalues, which can be close to 1, and it may not converge to a unique vector when $\lambda_1 = \lambda_2$.
- **Exact solutions.** PageRank is the solution of the linear system $(I - d P^{\mathsf T}) x = \frac{1 - d}{n} \mathbf{1}$, where $P$ is the row-stochastic matrix of the surfer without jumps. Direct solvers take $O(n^3)$ time, so iteration is used for large graphs.
- **Stability.** Borodin and co-authors study how much a ranking can change when a few arcs change. The HITS vectors can change a lot after a small change of the graph when the gap $\lambda_1 - \lambda_2$ is small, while the in-degree scores change only at the nodes whose in-links change.

## Reductions

- **To an eigenvector problem.** Each method is the principal eigenvector of a non-negative matrix: the Google matrix for PageRank, $A^{\mathsf T} A$ and $A A^{\mathsf T}$ for HITS. The Perron-Frobenius theorem gives existence, and uniqueness when the matrix is irreducible.
- **To a linear system.** PageRank and Katz centrality are solutions of sparse linear systems $(I - c M) x = b$, and can use any linear solver.
- **To a random walk.** PageRank and SALSA are stationary distributions of [Markov chains](/markov-chain/), so they can be estimated by simulating short walks.

## Applications

- Web search: ordering the pages that match a query, combined with text relevance.
- Citation analysis: ranking papers, authors and journals.
- Recommendation and social networks: ranking accounts to follow, with personalized variants.
- Spam detection: TrustRank-style methods spread trust from a seed of known good pages, as a personalized PageRank.

## References
