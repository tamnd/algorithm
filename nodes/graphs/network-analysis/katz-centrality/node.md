---
tag: PF0CR0
kind: definition
slug: katz-centrality
name: Katz centrality
aliases:
- Katz index
- Katz status index
area: graphs/network-analysis
level: advanced
summary: Weighted count of walks of all lengths, damped by an attenuation factor.
prereqs: [centrality, walk, adjacency-matrix, spectral-radius]
see_also: [eigenvector-centrality, degree-centrality, pagerank, link-prediction, neumann-series, perron-frobenius-theorem, hits-algorithm, harmonic-centrality]
sources:
  - paper: doi:10.1007/BF02289026
    title: Leo Katz, A new status index derived from sociometric analysis, Psychometrika 18(1), 39 to 43 (1953)
    locator: the whole paper (the status of a person as the number of chains of choices that end at that person, each chain of length k weighted by a^k, and the closed form with the inverse of I − aC)
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 7, Measures and metrics (the section on Katz centrality, the form x = αAx + β1, and the condition α < 1/κ1)
  - paper: doi:10.1086/228631
    title: Phillip Bonacich, Power and centrality, a family of measures, American Journal of Sociology 92(5), 1170 to 1182 (1987)
    locator: the family c(α, β) = α(I − βR)^(-1)R1, which contains degree for β = 0 and tends to eigenvector centrality as β tends to 1/λ1
  - paper: doi:10.1002/asi.20591
    title: David Liben-Nowell and Jon Kleinberg, The link-prediction problem for social networks, Journal of the American Society for Information Science and Technology 58(7), 1019 to 1031 (2007)
    locator: the Katz score of a pair of vertices as a link predictor
---

Katz centrality scores a [vertex](/vertex/) by the number of [walks](/walk/) that end at it, of every length, where a walk of length $k$ counts $\alpha^k$ for an attenuation factor $0 < \alpha < 1/\rho(A)$. Short walks count most, so the score mixes the local view of [degree centrality](/degree-centrality/) with the global view of [eigenvector centrality](/eigenvector-centrality/), and gives every vertex a positive base score, so that it works on directed graphs where eigenvector centrality is zero for many vertices. The same sum for a pair of vertices is the Katz index, used in [link prediction](/link-prediction/).

## Definition

Let $G$ be a graph on the vertices $1, \ldots, n$ with [adjacency matrix](/adjacency-matrix/) $A$, where $A_{uv}$ is the number or the weight of the edges from $u$ to $v$. For an undirected graph $A$ is symmetric. Let $\rho(A)$ be the [spectral radius](/spectral-radius/) of $A$, the largest absolute value of its eigenvalues. The entry $(A^k)_{uv}$ is the number of walks of length $k$ from $u$ to $v$, weighted by the products of the weights.

**Katz centrality.** For $0 < \alpha < 1/\rho(A)$, the **Katz centrality** of $v$ is

$$x_v = \sum_{k=1}^{\infty} \alpha^k \sum_{u} (A^k)_{uv},$$

the damped count of all walks of length at least 1 that end at $v$. In matrix form, with $\mathbf{1}$ the vector of all ones,

$$x = \left( (I - \alpha A^{\mathsf T})^{-1} - I \right) \mathbf{1}.$$

**The condition on $\alpha$.** The series $\sum_k \alpha^k (A^{\mathsf T})^k$ is a [Neumann series](/neumann-series/). It converges, and equals $(I - \alpha A^{\mathsf T})^{-1}$, when $\alpha \rho(A) < 1$. For $A \ne 0$ with non-negative entries, $\rho(A)$ is itself an eigenvalue with a non-negative eigenvector, by the [Perron-Frobenius theorem](/perron-frobenius-theorem/), so for $\alpha \ge 1/\rho(A)$ the sum diverges at the vertices that the eigenvector reaches; the definition does not apply. If $\rho(A) = 0$, as in a directed acyclic graph, every $\alpha > 0$ is allowed and the sum is finite.

**Newman's form.** Newman writes the score as the solution of $x = \alpha A^{\mathsf T} x + \beta \mathbf{1}$, that is $x = \beta (I - \alpha A^{\mathsf T})^{-1} \mathbf{1}$, where $\beta > 0$ is a base score that every vertex gets. With $\beta = 1$, this is the definition above plus 1 at every vertex, so it gives the same ranking. The scale is arbitrary in both forms, and only the ranking and the ratios matter.

**The Katz index of a pair.** The matrix $S = (I - \alpha A)^{-1} - I = \sum_{k \ge 1} \alpha^k A^k$ has the entry $S_{uv}$, the damped count of walks from $u$ to $v$. Katz centrality is the column sum of $S$. As a score of the pair $\{u, v\}$, $S_{uv}$ is a predictor of a future edge.

**Directed, weighted and disconnected graphs.** For a [directed graph](/directed-graph/), the definition counts walks that end at $v$, so it measures how much $v$ is pointed at; using $A$ in place of $A^{\mathsf T}$ counts the walks that start at $v$. Weights enter through $A$. On a graph with several components, $S$ is zero between components, every component is scored on its own, and $\rho(A)$ is the largest spectral radius of a component, so a small, dense part limits $\alpha$ for the whole graph. Every vertex with an in-edge has a positive score, and a vertex with no in-edge has score 0, or $\beta$ in Newman's form.

**Ties.** Two vertices that an automorphism of $G$ swaps have equal scores. Scores computed by iteration are approximate, so ranks of scores that differ by less than the error are ties.

## Examples and non-examples

**A small undirected graph.** Take the vertices 0 to 6 and the edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$. Its spectral radius is about $2.7093$, so $\alpha < 0.3691$. The numbers of walks of length 1 to 3 that end at each vertex, and the Katz centrality for $\alpha = 1/5$, are:

| vertex | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| walks of length 1 (degree) | 2 | 3 | 3 | 3 | 3 | 2 | 2 |
| walks of length 2 | 6 | 8 | 8 | 9 | 7 | 5 | 5 |
| walks of length 3 | 16 | 23 | 23 | 23 | 19 | 12 | 12 |
| $x_v$ for $\alpha = 1/5$ | 53/57 | 151/114 | 151/114 | 26/19 | 68/57 | 91/114 | 91/114 |
| $x_v$, decimal | 0.930 | 1.325 | 1.325 | 1.368 | 1.193 | 0.798 | 0.798 |

Vertices 1, 2, 3 and 4 tie in degree. Katz centrality with $\alpha = 1/5$ puts vertex 3 first, since it has the most walks of length 2, and vertex 4 last of the four. Eigenvector centrality, the limit $\alpha \to 1/\rho(A)$, ranks 1 and 2 above 3, since the long walks concentrate in the dense group $\{0, 1, 2, 3\}$. So $\alpha$ moves the ranking between the local and the global view.

**A directed acyclic graph.** On the path $0 \to 1 \to 2$, $\rho(A) = 0$, and $x = (0, \alpha, \alpha + \alpha^2)$ for every $\alpha > 0$. Eigenvector centrality is zero on every vertex here, so it says nothing, while Katz centrality still ranks the end of the path first.

**Non-example: $\alpha$ too large.** On the triangle, $\rho(A) = 2$. For $\alpha = 1/2$ the number of walks of length $k$ ending at a vertex is $2^k$, so the terms $\alpha^k 2^k = 1$ do not shrink, and the sum diverges. The formula $(I - \alpha A)^{-1}$ fails too, since $I - \frac12 A$ is singular.

**Non-example: degree is not a special case for fixed $\alpha$.** For every fixed $\alpha > 0$, Katz centrality counts longer walks too, so two vertices of equal degree can get different scores, as vertices 1 and 4 above. Only the limit $x/\alpha$ as $\alpha \to 0$ is the in-degree.

## Related definitions

- **[Degree centrality](/degree-centrality/)** is the limit of $x/\alpha$ as $\alpha \to 0$.
- **[Eigenvector centrality](/eigenvector-centrality/)** is the limit of the direction of $x$ as $\alpha \to 1/\rho(A)$ from below, when the leading eigenvalue is simple. Bonacich's power centrality family $c(\alpha, \beta) = \alpha (I - \beta A)^{-1} A \mathbf{1}$ contains both ends, and also allows $\beta < 0$, which rewards being linked to vertices with few links.
- **[PageRank](/pagerank/)** is Katz centrality with each vote divided by the out-degree of the voter, $x = \alpha A^{\mathsf T} D^{-1} x + \beta \mathbf{1}$, which stops a vertex with many out-links from passing on a large score.
- **[HITS](/hits-algorithm/)** uses walks that alternate between forward and backward edges.
- **Communicability** replaces $\alpha^k$ by $1/k!$, which gives the matrix exponential $e^{A}$ and needs no bound on the parameter.
- **[Harmonic centrality](/harmonic-centrality/)** also damps far vertices, but by the inverse of the distance, and counts each vertex once instead of counting walks.

## References
