---
tag: EQDSXM
kind: definition
slug: closeness-centrality
name: Closeness centrality
area: graphs/network-analysis
level: intro
summary: The centrality of a vertex is the inverse of its average shortest-path distance to the other vertices.
prereqs: [centrality, shortest-path, breadth-first-search]
see_also: [harmonic-centrality, degree-centrality, betweenness-centrality, eccentricity, all-pairs-shortest-paths, dijkstra]
sources:
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 7, Measures and metrics (the section on closeness centrality, with the harmonic mean form for disconnected networks)
  - book: isbn:9780521387071
    title: Stanley Wasserman and Katherine Faust, Social Network Analysis, Methods and Applications, Cambridge University Press, 1994
    locator: Chapter 5, Centrality and prestige (actor closeness centrality, and the closeness measure for graphs that are not connected)
  - paper: doi:10.1007/BF02289527
    title: Gert Sabidussi, The centrality index of a graph, Psychometrika 31(4), 581 to 603 (1966)
    locator: the definition of the index as the inverse of the sum of distances
  - paper: doi:10.1080/15427951.2013.865686
    title: Paolo Boldi and Sebastiano Vigna, Axioms for centrality, Internet Mathematics 10(3-4), 222 to 262 (2014)
    locator: Section 2 (closeness and harmonic centrality on graphs that are not connected)
---

Closeness centrality is the [centrality](/centrality/) measure that scores a [vertex](/vertex/) $v$ by how near it is to all other vertices: it is $n - 1$ divided by the sum of the [shortest-path](/shortest-path/) distances from $v$ to the others, so it is the inverse of the mean distance. A vertex from which every other vertex is one step away has closeness 1. The measure is defined only when every other vertex is reachable, and the fixes for a disconnected graph give different rankings, which is why [harmonic centrality](/harmonic-centrality/) is often used in its place.

## Definition

Let $G = (V, E)$ be a connected undirected graph with $n \ge 2$ vertices, and let $d(v, u)$ be the number of edges on a shortest path from $v$ to $u$. The **farness** of $v$ is $\sum_{u \in V} d(v, u)$, and the **closeness centrality** of $v$ is

$$C_C(v) = \frac{n - 1}{\sum_{u \in V,\, u \ne v} d(v, u)}.$$

Each of the $n - 1$ other vertices is at distance at least 1, so the sum is at least $n - 1$ and $0 < C_C(v) \le 1$, with $C_C(v) = 1$ exactly when $v$ is adjacent to all other vertices. Sabidussi's original index is $1/\sum_u d(v, u)$, without the factor $n - 1$. The factor does not change the ranking inside one graph.

**Weighted graphs.** If each edge has a length $w(e) > 0$, then $d(v, u)$ is the weighted shortest-path distance, which [Dijkstra's algorithm](/dijkstra/) computes. A weight that measures the strength of a tie must first be turned into a length, for example $1/w$.

**Directed graphs.** In a directed graph, $d(v, u)$ uses directed paths. The *out-closeness* uses the distances from $v$, and the *in-closeness* uses the distances to $v$. Both need the graph to be strongly connected for the formula above to be defined.

**Disconnected graphs.** When some $u$ is not reachable from $v$, then $d(v, u) = \infty$ and the formula gives 0 to every vertex. There are three common fixes. Let $R(v)$ be the set of vertices reachable from $v$, with $v \in R(v)$, and $r = |R(v)|$.

- *Inside the component.* Use $(r - 1)/\sum_{u \in R(v)} d(v, u)$. This favours vertices in small components: each vertex of an isolated edge gets the score 1.
- *Wasserman and Faust.* Multiply by the share of the graph that is reachable:
$$C_{WF}(v) = \frac{r - 1}{n - 1} \cdot \frac{r - 1}{\sum_{u \in R(v)} d(v, u)},$$
and set $C_{WF}(v) = 0$ when $r = 1$.
- *Harmonic.* Replace the inverse of the sum by the sum of the inverses, $\sum_{u \ne v} 1/d(v, u)$ with $1/\infty = 0$. This is [harmonic centrality](/harmonic-centrality/).

**Ties.** Equal scores are common in graphs with symmetries, and closeness values in a large graph with a small diameter crowd into a narrow range, so a small change in the graph can swap the order of many vertices. A ranking must say how it breaks ties.

**Cost.** One score needs the distances from one vertex: $O(n + m)$ time with [breadth-first search](/breadth-first-search/) on an unweighted graph, and $O(m + n \log n)$ with Dijkstra's algorithm and a Fibonacci heap on a weighted graph. All $n$ scores need [all-pairs shortest paths](/all-pairs-shortest-paths/): $O(nm)$ time without weights, and $O(nm + n^2 \log n)$ with weights.

## Examples and non-examples

**A worked example.** Take the undirected graph with the vertices 0 to 6 and the 9 edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$, a dense group and a triangle joined by the edge $\{3, 4\}$. The table gives the distances from each vertex, by BFS.

| $v$ | distances to $0, 1, \ldots, 6$ | farness | $C_C(v)$ |
|---|---|---|---|
| 0 | 0 1 1 2 3 4 4 | 15 | 6/15 = 0.400 |
| 1 | 1 0 1 1 2 3 3 | 11 | 6/11 = 0.545 |
| 2 | 1 1 0 1 2 3 3 | 11 | 6/11 = 0.545 |
| 3 | 2 1 1 0 1 2 2 | 9 | 6/9 = 0.667 |
| 4 | 3 2 2 1 0 1 1 | 10 | 6/10 = 0.600 |
| 5 | 4 3 3 2 1 0 1 | 14 | 6/14 = 0.429 |
| 6 | 4 3 3 2 1 1 0 | 14 | 6/14 = 0.429 |

Vertex 3 is the most central. All four vertices 1 to 4 have degree 3, but closeness separates them.

**A disconnected graph.** Take the path $0 - 1 - 2$ and the separate edge $3 - 4$, so $n = 5$.

| $v$ | $r$ | inside the component | $C_{WF}(v)$ | harmonic |
|---|---|---|---|---|
| 1 | 3 | 2/2 = 1 | (2/4)(2/2) = 0.5 | 2 |
| 0, 2 | 3 | 2/3 | (2/4)(2/3) = 1/3 | 1.5 |
| 3, 4 | 2 | 1/1 = 1 | (1/4)(1/1) = 0.25 | 1 |

The component-only score ties the centre of the path with the ends of the small edge. The other two scores rank vertex 1 first and the vertices 3 and 4 last.

**Non-examples.**

- The *eccentricity* $\max_u d(v, u)$ is not closeness. It uses only the farthest vertex. Its minimum gives the centre of the graph, see [eccentricity](/eccentricity/).
- The inverse of the mean of the inverses is not closeness either: that is the harmonic mean distance, the basis of [harmonic centrality](/harmonic-centrality/). For vertex 0 above, the mean distance is $15/6 = 2.5$, while the harmonic mean distance is $6/(1 + 1 + 1/2 + 1/3 + 1/4 + 1/4) = 6/(10/3) = 1.8$.

## Related definitions

- [Harmonic centrality](/harmonic-centrality/): the sum of inverse distances, defined on all graphs.
- [Degree centrality](/degree-centrality/): only the distance-1 term.
- [Betweenness centrality](/betweenness-centrality/): counts the shortest paths through a vertex, not their lengths.
- [Eccentricity](/eccentricity/): the largest distance from a vertex.
- [Effective diameter](/effective-diameter/): a statistic of the whole distribution of distances.
- [All-pairs shortest paths](/all-pairs-shortest-paths/): the computation that all scores need.

## References
