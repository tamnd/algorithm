---
tag: CBFVG5
kind: definition
slug: clustering-coefficient
name: Clustering coefficient
aliases:
- local clustering coefficient
- transitivity
- global clustering coefficient
area: graphs/network-analysis
level: intro
summary: The fraction of pairs of neighbours of a vertex that are adjacent, and the graph-wide fraction of closed triples.
prereqs: [graph, degree, neighborhood]
see_also: [triadic-closure, triangle-counting, compact-forward-algorithm, small-world-network, watts-strogatz-model, ego-network, erdos-renyi-model]
sources:
  - paper: doi:10.1038/30918
    title: Duncan J. Watts and Steven H. Strogatz, Collective dynamics of small-world networks, Nature 393, 440 to 442 (1998)
    locator: the definition of the clustering coefficient C as the mean over the vertices of the local fraction
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 7, Measures and metrics (the section on transitivity, with the global and the local clustering coefficient)
  - paper: doi:10.1137/S003614450342480
    title: M. E. J. Newman, The structure and function of complex networks, SIAM Review 45(2), 167 to 256 (2003)
    locator: the section on transitivity or clustering (the two definitions, and why their values differ)
  - paper: doi:10.7155/jgaa.00108
    title: Thomas Schank and Dorothea Wagner, Approximating clustering coefficient and transitivity, Journal of Graph Algorithms and Applications 9(2), 265 to 275 (2005)
    locator: the whole paper (the sampling estimators and the weighted relation between the two coefficients)
---

The clustering coefficient measures how often two neighbours of a [vertex](/vertex/) are also neighbours of each other. The *local* coefficient of $v$ is the fraction of pairs of neighbours of $v$ that are joined by an edge. The *global* coefficient, also called transitivity, is the fraction of paths of length 2 in the whole graph that close into a triangle. Social networks have high values, because a friend of a friend is often a friend; this is [triadic closure](/triadic-closure/).

## Definition

Let $G = (V, E)$ be a simple undirected graph, let $N(v)$ be the [neighborhood](/neighborhood/) of $v$ and $k_v = |N(v)|$ its [degree](/degree/). Let

$$T(v) = \bigl|\{\{x, y\} \subseteq N(v) : \{x, y\} \in E\}\bigr|$$

be the number of edges among the neighbours of $v$, which is the number of triangles that contain $v$.

**Local clustering coefficient.** For $k_v \ge 2$,

$$C(v) = \frac{T(v)}{\binom{k_v}{2}} = \frac{2\,T(v)}{k_v (k_v - 1)}.$$

So $0 \le C(v) \le 1$, and $C(v) = 1$ exactly when $N(v)$ is a clique. For $k_v < 2$ there is no pair of neighbours and $C(v)$ is undefined. Some programs set it to 0 and some leave such vertices out of the average; the two choices give different averages, so a report must say which one it uses.

**Average clustering coefficient** (Watts and Strogatz, 1998). Over the set $V_2$ of the vertices with $k_v \ge 2$,

$$\bar C = \frac{1}{|V_2|} \sum_{v \in V_2} C(v).$$

**Global clustering coefficient, or transitivity.** A *connected triple* centred at $v$ is a path $x - v - y$ with $x \ne y$. There are $\sum_v \binom{k_v}{2}$ of them. Each triangle closes exactly three of them, one at each corner. So

$$C_{\Delta} = \frac{3 \times (\text{number of triangles})}{\text{number of connected triples}} = \frac{\sum_v T(v)}{\sum_v \binom{k_v}{2}}.$$

The second form shows that $C_{\Delta}$ is the mean of the $C(v)$ weighted by $\binom{k_v}{2}$, while $\bar C$ gives each vertex the same weight. So $C_\Delta$ is dominated by the vertices of high degree, and the two numbers can differ a lot.

**Directed and weighted graphs.** The definitions above are for undirected graphs without weights. A directed graph is usually made undirected first, by keeping an edge when an arc exists in either direction. Versions that keep the directions or use the weights exist, but they are not the same number, and they are not treated here.

**Disconnected graphs.** Both coefficients are local sums, so they are defined on a disconnected graph without change: a component without a triangle adds 0 to the numerator, and its triples still count in the denominator of $C_\Delta$.

**Cost.** Both coefficients reduce to [triangle counting](/triangle-counting/). The [compact-forward algorithm](/compact-forward-algorithm/) counts all $T(v)$ in $O(m^{3/2})$ time. Sampling also works: pick a uniform random connected triple and test whether it is closed. The fraction of closed samples estimates $C_\Delta$, and by the Hoeffding bound $O(\varepsilon^{-2} \log(1/\delta))$ samples give an additive error at most $\varepsilon$ with probability at least $1 - \delta$. Schank and Wagner give this method and the similar one for $\bar C$.

## Examples and non-examples

**A worked example.** Take the undirected graph with the vertices 0 to 6 and the 9 edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$. It has three triangles: $\{0,1,2\}$, $\{1,2,3\}$ and $\{4,5,6\}$.

| $v$ | $N(v)$ | $k_v$ | $\binom{k_v}{2}$ | $T(v)$ | $C(v)$ |
|---|---|---|---|---|---|
| 0 | 1, 2 | 2 | 1 | 1 | 1 |
| 1 | 0, 2, 3 | 3 | 3 | 2 | 2/3 |
| 2 | 0, 1, 3 | 3 | 3 | 2 | 2/3 |
| 3 | 1, 2, 4 | 3 | 3 | 1 | 1/3 |
| 4 | 3, 5, 6 | 3 | 3 | 1 | 1/3 |
| 5 | 4, 6 | 2 | 1 | 1 | 1 |
| 6 | 4, 5 | 2 | 1 | 1 | 1 |

The average is $\bar C = (1 + \frac23 + \frac23 + \frac13 + \frac13 + 1 + 1)/7 = 5/7 \approx 0.714$. The sums are $\sum T(v) = 9 = 3 \cdot 3$ and $\sum \binom{k_v}{2} = 15$, so $C_\Delta = 9/15 = 0.6$.

**The two coefficients far apart.** The friendship graph $F_k$ has a hub joined to $2k$ vertices, which are paired by $k$ more edges. Each of the $2k$ outer vertices has $C = 1$, and the hub has $k$ triangles among $\binom{2k}{2}$ pairs, so $C = 1/(2k - 1)$. For $k = 5$, $\bar C = (10 + \frac19)/11 = 91/99 \approx 0.919$, while $C_\Delta = 3 \cdot 5/55 = 3/11 \approx 0.273$. As $k$ grows, $\bar C \to 1$ and $C_\Delta = 3/(2k + 1) \to 0$.

**Standard graphs.**

- The [complete graph](/complete-graph/) $K_n$, $n \ge 3$: every coefficient is 1.
- A [tree](/tree/), a cycle of length at least 4, and every [bipartite graph](/bipartite-graph/): there is no triangle, so every coefficient is 0.
- The [Erdős-Rényi graph](/erdos-renyi-model/) $G(n, p)$: each pair of neighbours of $v$ is adjacent with probability $p$, on its own, so $\mathbb{E}[C(v) \mid k_v \ge 2] = p$. With a fixed average degree $c = p(n-1)$, this is $c/(n-1) \to 0$. Real social networks have much larger values, which is the point of the [Watts-Strogatz model](/watts-strogatz-model/).

**Non-examples.**

- The density $m / \binom{n}{2}$ of the whole graph is not a clustering coefficient. A graph made of many disjoint triangles has density near 0 and clustering 1.
- The number of triangles alone is not a clustering coefficient: a vertex of degree 100 in 10 triangles has $C = 10/4950 \approx 0.002$.
- $\bar C$ and $C_\Delta$ are not two estimates of the same quantity. They are different statistics, as $F_k$ shows.

## Related definitions

- [Triadic closure](/triadic-closure/): the social process that makes the coefficient high.
- [Triangle counting](/triangle-counting/): the computation behind both coefficients.
- [Small-world network](/small-world-network/) and [Watts-Strogatz model](/watts-strogatz-model/): high clustering with short paths.
- [Ego network](/ego-network/): $C(v)$ is the edge density of the ego network of $v$ with the ego removed.
- [Rich-club coefficient](/rich-club-coefficient/): the edge density among the vertices of high degree.

## References
