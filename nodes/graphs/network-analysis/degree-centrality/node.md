---
tag: TN684S
kind: definition
slug: degree-centrality
name: Degree centrality
area: graphs/network-analysis
level: intro
summary: The centrality of a vertex is its degree, often divided by n - 1.
prereqs: [centrality, degree]
see_also: [degree, in-degree-and-out-degree, degree-distribution, closeness-centrality, betweenness-centrality, eigenvector-centrality, k-core, stationary-distribution]
sources:
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 7, Measures and metrics (the section on degree centrality)
  - book: isbn:9780521387071
    title: Stanley Wasserman and Katherine Faust, Social Network Analysis, Methods and Applications, Cambridge University Press, 1994
    locator: Chapter 5, Centrality and prestige (actor degree centrality, degree prestige and group degree centralization)
  - paper: doi:10.1016/0378-8733(78)90021-7
    title: Linton C. Freeman, Centrality in social networks, conceptual clarification, Social Networks 1(3), 215 to 239 (1979)
    locator: the section on degree-based measures (the relative degree and the degree centralization of a graph)
---

Degree centrality is the [centrality](/centrality/) measure that scores a [vertex](/vertex/) by its [degree](/degree/), the number of edges at the vertex, usually divided by $n - 1$ so that the score is between 0 and 1. It is the simplest centrality and the cheapest to compute: all scores take $O(n + m)$ time from an [adjacency list](/adjacency-list/). In a directed graph it splits into in-degree centrality, often called prestige, and out-degree centrality.

## Definition

Let $G = (V, E)$ be a simple undirected graph with $n \ge 2$ vertices. The **degree centrality** of $v \in V$ is

$$C_D(v) = d(v), \qquad \text{and the normalized form is} \qquad C_D'(v) = \frac{d(v)}{n - 1}.$$

Since $0 \le d(v) \le n - 1$ in a simple graph, $0 \le C_D'(v) \le 1$. The value 1 means that $v$ is adjacent to every other vertex, and 0 means that $v$ is isolated.

**Directed graphs.** For a directed graph, the *in-degree centrality* is $d^-(v)/(n-1)$ and the *out-degree centrality* is $d^+(v)/(n-1)$, see [in-degree and out-degree](/in-degree-and-out-degree/). In-degree counts the choices that $v$ receives, and out-degree counts the choices that $v$ makes.

**Weighted graphs.** With a weight $w(u, v) > 0$ on each edge, the *strength* $s(v) = \sum_{u \in N(v)} w(u, v)$ replaces the degree. Strength treats a weight as the size of a tie, not as a length. With multigraphs and self-loops, the degree follows the rules of the [degree](/degree/) page, and the bound $d(v) \le n - 1$ no longer holds.

**Degree centralization.** Freeman's centralization of the whole graph compares each degree with the largest one, $d^* = \max_v d(v)$:

$$C_D(G) = \frac{\sum_{v \in V} \bigl(d^* - d(v)\bigr)}{(n - 1)(n - 2)}, \qquad n \ge 3.$$

The denominator is the value of the sum for the star $K_{1, n-1}$, where $d^* = n - 1$ and the $n - 1$ leaves each add $n - 2$. The star is the graph with the largest sum, so $0 \le C_D(G) \le 1$, with $C_D(G) = 0$ exactly for the regular graphs.

**Ties and disconnected graphs.** Many vertices share each degree value, so a ranking by degree has many ties. Report them, or break them by a second key, such as the vertex number or another centrality. The degree is local, so it is defined in the same way for a disconnected graph, and each component is scored on its own. The normalizing factor $n - 1$ still uses the size of the whole graph.

**Cost.** With adjacency lists that store their lengths, one score takes $O(1)$ time, and all scores take $O(n)$ time. From an edge list, all degrees take $\Theta(n + m)$ time with one pass that adds 1 to both ends of each edge. From an [adjacency matrix](/adjacency-matrix/), they take $\Theta(n^2)$ time.

## Examples and non-examples

**A worked example.** Take the undirected graph with the vertices 0 to 6 and the 9 edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$. Here $n - 1 = 6$.

| vertex | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $d(v)$ | 2 | 3 | 3 | 3 | 3 | 2 | 2 |
| $C_D'(v)$ | 1/3 | 1/2 | 1/2 | 1/2 | 1/2 | 1/3 | 1/3 |

The vertices 1, 2, 3 and 4 tie for first. Vertex 3 is an end of the only edge between the two groups, but it gets the same score as vertex 1. Degree does not see this, while [betweenness centrality](/betweenness-centrality/) does. The centralization is $C_D(G) = (1 + 0 + 0 + 0 + 0 + 1 + 1)/(6 \cdot 5) = 3/30 = 0.1$.

**A star.** In $K_{1,4}$, the centre has $C_D' = 1$ and each leaf has $C_D' = 1/4$. The centralization is $4 \cdot 3/(4 \cdot 3) = 1$.

**A directed example.** In the directed graph with arcs $0 \to 1$, $0 \to 2$, $1 \to 2$, $3 \to 2$, vertex 2 has in-degree 3 and out-degree 0, and vertex 0 has in-degree 0 and out-degree 2. So vertex 2 has the highest prestige and vertex 0 the highest activity.

**A random walk.** On a connected undirected graph, the walk that moves to a uniform random neighbour has the [stationary distribution](/stationary-distribution/) $\pi(v) = d(v)/2m$. To check it, $\sum_{u \in N(v)} \pi(u) \cdot \frac{1}{d(u)} = \sum_{u \in N(v)} \frac{1}{2m} = \frac{d(v)}{2m}$. So in the long run, the walk spends time at each vertex in proportion to its degree, and degree centrality ranks the vertices exactly as this walk does.

**Non-examples.**

- The number of vertices within distance 2 of $v$ is not the degree centrality. It is the size of the second ball of the [neighborhood function](/neighborhood-function/).
- In a multigraph, the number of distinct neighbours $|N(v)|$ and the degree $d(v)$ differ when there are parallel edges, so "degree centrality" must say which one it counts.
- A high degree is not a high [eigenvector centrality](/eigenvector-centrality/). In the example above, vertices 1 and 4 have the same degree, but the eigenvector score of 1 is about 1.6 times that of 4.

## Related definitions

- [Degree](/degree/) and [in-degree and out-degree](/in-degree-and-out-degree/): the counts that the measure uses.
- [Degree distribution](/degree-distribution/): the fraction of vertices with each degree.
- [Closeness centrality](/closeness-centrality/), [betweenness centrality](/betweenness-centrality/) and [eigenvector centrality](/eigenvector-centrality/): measures that look past the neighbours.
- [k-core](/k-core/): the core number refines the degree by asking that the neighbours also have a high degree.
- [Ego network](/ego-network/): the subgraph of a vertex and its neighbours, whose size is $d(v) + 1$.

## References
