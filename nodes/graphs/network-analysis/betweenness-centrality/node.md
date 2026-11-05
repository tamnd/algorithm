---
tag: J9XXYK
kind: definition
slug: betweenness-centrality
name: Betweenness centrality
aliases:
- shortest-path betweenness
- vertex betweenness
area: graphs/network-analysis
level: core
summary: The centrality of a vertex is the sum, over pairs of other vertices, of the fraction of their shortest paths that pass through it.
prereqs: [centrality, shortest-path]
see_also: [brandes-algorithm, betweenness-centrality-computation, closeness-centrality, girvan-newman-algorithm, ego-network, structural-holes]
sources:
  - paper: doi:10.2307/3033543
    title: Linton C. Freeman, A set of measures of centrality based on betweenness, Sociometry 40(1), 35 to 41 (1977)
    locator: the whole paper (the definition by the fraction of geodesics, and the normalized form)
  - paper: doi:10.1080/0022250X.2001.9990249
    title: Ulrik Brandes, A faster algorithm for betweenness centrality, Journal of Mathematical Sociology 25(2), 163 to 177 (2001)
    locator: Section 3 (the counting of shortest paths, the Bellman criterion and the pair dependency)
  - paper: doi:10.1016/j.socnet.2007.11.001
    title: Ulrik Brandes, On variants of shortest-path betweenness centrality and their generic computation, Social Networks 30(2), 136 to 145 (2008)
    locator: the whole paper (endpoints, edge betweenness, bounded distance and other variants)
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 7, Measures and metrics (the section on betweenness centrality)
---

Betweenness centrality scores a [vertex](/vertex/) $v$ by how many [shortest paths](/shortest-path/) between other vertices pass through $v$. When a pair has several shortest paths, $v$ gets the fraction of them that use it. A vertex with high betweenness is a broker: it joins parts of the graph that have few other links, and removing it makes many paths longer. Freeman defined the measure in 1977. The fast way to compute it for all vertices is [Brandes' algorithm](/brandes-algorithm/), in $O(nm)$ time on a graph without weights.

## Definition

Let $G = (V, E)$ be a graph with $n$ vertices, directed or undirected. For $s, t \in V$, let $\sigma_{st}$ be the number of shortest paths from $s$ to $t$, with $\sigma_{ss} = 1$, and let $\sigma_{st}(v)$ be the number of those paths that pass through $v$ as an inner vertex. The **betweenness centrality** of $v$ is

$$C_B(v) = \sum_{\substack{s \ne v \ne t,\ s \ne t \\ \sigma_{st} > 0}} \frac{\sigma_{st}(v)}{\sigma_{st}}.$$

The sum is over ordered pairs in a directed graph. In an undirected graph, $\sigma_{st} = \sigma_{ts}$ and $\sigma_{st}(v) = \sigma_{ts}(v)$, and the usual convention sums over unordered pairs $\{s, t\}$, which is half the sum over ordered pairs. Programs differ here, so a reported value must say which convention it uses.

**The counting rule.** Let $d(s, t)$ be the distance. For $v \notin \{s, t\}$,

$$\sigma_{st}(v) = \begin{cases} \sigma_{sv} \cdot \sigma_{vt} & \text{if } d(s, v) + d(v, t) = d(s, t), \\ 0 & \text{otherwise.} \end{cases}$$

*Proof.* A shortest $s$-$t$ path through $v$ is a path from $s$ to $v$ followed by a path from $v$ to $t$, and its length is at least $d(s, v) + d(v, t)$. If this sum is larger than $d(s, t)$, no shortest path passes through $v$. If it is equal, both parts of such a path must be shortest paths, else the whole path would be longer than $d(s, t)$. Conversely, a shortest $s$-$v$ path and a shortest $v$-$t$ path join into a walk of length $d(s, t)$, which is a shortest path because a shorter walk cannot exist and a walk of the least length repeats no vertex when all lengths are positive. The map from pairs of parts to joined paths is a bijection, so there are $\sigma_{sv} \sigma_{vt}$ such paths. $\square$

**Normalization.** The largest possible value is the number of pairs that do not contain $v$: $(n-1)(n-2)/2$ for unordered pairs in an undirected graph and $(n-1)(n-2)$ for ordered pairs in a directed graph. The star reaches it at its centre. Dividing by it gives a score in $[0, 1]$, for $n \ge 3$.

**Weighted graphs.** With positive edge lengths, the shortest paths and their counts are the weighted ones. Two paths of the same total length both count. With real-valued lengths, floating-point sums can make two paths of equal length look different, which changes the counts. Integer or rational lengths avoid this.

**Disconnected graphs.** A pair with $\sigma_{st} = 0$, that is with $t$ not reachable from $s$, is left out of the sum. So the betweenness of a vertex depends only on the pairs inside its component (in the directed case, the pairs that it can be between). The normalizing factor still uses $n$, which makes vertices of small components score low.

**Ties.** When a pair has several shortest paths, they share the unit of the pair equally. This is a fixed rule of the definition, not a choice of the algorithm. Equal final scores are common, for example among the vertices of a cycle.

**Variants.** *Endpoint betweenness* also counts $v$ when it is $s$ or $t$, which adds $r - 1$ with unordered pairs in an undirected graph, where $r$ is the size of the component of $v$. *Edge betweenness* replaces $v$ by an edge $e$ and counts the shortest paths that use $e$. The [Girvan-Newman algorithm](/girvan-newman-algorithm/) removes the edge of highest edge betweenness, again and again, to find communities. Brandes (2008) treats these and more variants with one algorithm.

**A sum rule.** For a connected undirected graph,

$$\sum_{v \in V} C_B(v) = \sum_{\{s, t\}} \bigl(d(s, t) - 1\bigr).$$

For each pair, $\sum_v \sigma_{st}(v)/\sigma_{st}$ is the mean number of inner vertices on a shortest $s$-$t$ path, and each such path has exactly $d(s, t) - 1$ inner vertices.

## Examples and non-examples

**A worked example.** Take the undirected graph with the vertices 0 to 6 and the 9 edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$, a dense group and a triangle joined by the edge $\{3, 4\}$. Unordered pairs are used.

| $v$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $C_B(v)$ | 0 | 2 | 2 | 9 | 8 | 0 | 0 |
| normalized, $\div 15$ | 0 | 0.133 | 0.133 | 0.600 | 0.533 | 0 | 0 |

- Vertex 3 lies on every shortest path from $\{0, 1, 2\}$ to $\{4, 5, 6\}$: 9 pairs, each with all its shortest paths through 3.
- Vertex 4 lies on every shortest path from $\{0, 1, 2, 3\}$ to $\{5, 6\}$: 8 pairs.
- The pair $\{0, 3\}$ has the two shortest paths $0, 1, 3$ and $0, 2, 3$. So it gives $1/2$ to vertex 1 and $1/2$ to vertex 2. The pairs $\{0, 4\}$, $\{0, 5\}$ and $\{0, 6\}$ do the same, so vertices 1 and 2 get $4 \cdot \frac12 = 2$ each.
- The sum of the scores is 21. The distances of the 21 pairs sum to 42, so the sum rule gives $42 - 21 = 21$.

**A cycle.** In the cycle on the 4 vertices $0, 1, 2, 3$, the pair $\{0, 2\}$ has two shortest paths, through 1 and through 3, and the pair $\{1, 3\}$ has two, through 0 and through 2. So each vertex has $C_B = 1/2$.

**A path.** In the path $0 - 1 - 2 - 3 - 4$, vertex $i$ lies on the unique path of each pair with one end on each side, so $C_B(i) = i\,(4 - i)$: the values are $0, 3, 4, 3, 0$.

**Non-examples.**

- The number of shortest paths through $v$, without division by $\sigma_{st}$, is not the betweenness. In a grid, it counts the many paths of one pair many times, and it can be much larger than the number of pairs.
- *Flow betweenness* and *random-walk betweenness* use all paths or random walks, not only shortest ones. They are different measures, with different values.
- A vertex of high degree need not have high betweenness: in a complete graph every vertex has the largest degree and betweenness 0, because every pair is adjacent.

## Related definitions

- [Brandes' algorithm](/brandes-algorithm/) and [betweenness centrality computation](/betweenness-centrality-computation/): how to compute all scores.
- [Closeness centrality](/closeness-centrality/): uses the lengths of shortest paths, not their count.
- [Girvan-Newman algorithm](/girvan-newman-algorithm/): community detection by edge betweenness.
- [Ego network](/ego-network/): ego betweenness is betweenness inside the ego network.
- [Structural holes](/structural-holes/): the social theory of brokers.

## References
