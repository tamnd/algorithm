---
tag: YBXSKF
kind: problem
slug: betweenness-centrality-computation
name: Betweenness centrality computation
aliases:
- computing betweenness centrality
area: graphs/network-analysis
level: core
summary: Given a graph, compute the betweenness centrality of every vertex.
prereqs: [betweenness-centrality, single-source-shortest-paths]
see_also: [brandes-algorithm, betweenness-centrality, all-pairs-shortest-paths, breadth-first-search, dijkstra, girvan-newman-algorithm, closeness-centrality]
sources:
  - paper: doi:10.1080/0022250X.2001.9990249
    title: Ulrik Brandes, A faster algorithm for betweenness centrality, Journal of Mathematical Sociology 25(2), 163 to 177 (2001)
    locator: Sections 3 to 5 (the earlier cubic method, the dependency recursion, and the O(nm) and O(nm + n^2 log n) bounds)
  - paper: doi:10.1016/j.socnet.2007.11.001
    title: Ulrik Brandes, On variants of shortest-path betweenness centrality and their generic computation, Social Networks 30(2), 136 to 145 (2008)
    locator: the whole paper (endpoints, edge betweenness, bounded distance and group variants)
  - paper: doi:10.1142/S0218127407018403
    title: Ulrik Brandes and Christian Pich, Centrality estimation in large networks, International Journal of Bifurcation and Chaos 17(7), 2303 to 2318 (2007)
    locator: the whole paper (estimates from a sample of source vertices, and the choice of the sample)
  - paper: doi:10.1007/s10618-015-0423-0
    title: Matteo Riondato and Evgenios M. Kornaropoulos, Fast approximation of betweenness centrality through sampling, Data Mining and Knowledge Discovery 30(2), 438 to 475 (2016)
    locator: the whole paper (sampling of shortest paths, with a sample size bounded by the VC dimension and the vertex diameter)
  - paper: doi:10.1016/j.entcs.2016.03.005
    title: Michele Borassi, Pierluigi Crescenzi and Michel Habib, Into the square, on the complexity of some quadratic-time solvable problems, Electronic Notes in Theoretical Computer Science 322, 51 to 67 (2016)
    locator: the web of reductions from the quadratic k-SAT variant (the problem of the betweenness centrality of a vertex)
  - paper: doi:10.1137/1.9781611973730.112
    title: Amir Abboud, Fabrizio Grandoni and Virginia Vassilevska Williams, Subcubic equivalences between graph centrality problems, APSP and diameter, SODA 2015, 1681 to 1697
    locator: the results on betweenness centrality (subcubic equivalence with APSP for weighted graphs)
---

Betweenness centrality computation is the problem of finding the [betweenness centrality](/betweenness-centrality/) of every [vertex](/vertex/) of a graph: for each $v$, the sum over pairs $s, t$ of the fraction of shortest $s$-$t$ paths that pass through $v$. The direct method counts shortest paths for all pairs and sums the fractions, in $\Theta(n^3)$ time. [Brandes' algorithm](/brandes-algorithm/) of 2001 solves it in $O(nm)$ time without weights and $O(nm + n^2 \log n)$ with positive weights, and this is still the bound used in practice. Under standard conjectures, no algorithm is much faster in the worst case, so large graphs use sampling.

## In plain words

Picture a road map. For each pair of towns, look at all fastest routes between them. A town in the middle of many of these routes is a place that a lot of traffic must pass. The betweenness of a town counts this: for each pair of other towns, it gets the share of their fastest routes that go through it.

The problem is to find this number for every town at once. The plain way looks at every pair of towns and every possible middle town, which is slow for a large map. The better way runs one search from each town and passes the counts back from the far towns to the near ones. For huge maps, one runs the search from only some of the towns and scales the result.

## Definition

**Input.** A graph $G = (V, E)$ with $n = |V|$ and $m = |E|$, directed or undirected, and optionally a length $w(e) > 0$ for each edge. Without lengths, each edge has length 1.

**Output.** For each $v \in V$, the value

$$C_B(v) = \sum_{\substack{s \ne v \ne t,\ s \ne t \\ \sigma_{st} > 0}} \frac{\sigma_{st}(v)}{\sigma_{st}},$$

where $\sigma_{st}$ is the number of shortest $s$-$t$ paths and $\sigma_{st}(v)$ the number of those that pass through $v$. The sum is over ordered pairs; for an undirected graph the usual output is half of it, the sum over unordered pairs. The output may also be normalized, see [betweenness centrality](/betweenness-centrality/).

**Conventions that the output depends on.** Unreachable pairs, with $\sigma_{st} = 0$, add nothing. Pairs with several shortest paths split their unit equally among them; this is part of the definition, not a choice. Lengths must be positive: with zero-length edges, the number of shortest paths can be infinite when a zero-length cycle exists, and with negative lengths shortest paths need not exist.

**Exact arithmetic.** The counts $\sigma_{st}$ can grow exponentially in $n$: a chain of $k$ diamonds has $2^k$ shortest paths between its ends. Floating-point counts are usual in practice, but they lose exactness; exact values need big integers or rationals.

## Variants

- **One vertex.** Compute $C_B(v)$ for a single given $v$. In the worst case this is as hard as all vertices for weighted dense graphs, by the equivalences of Abboud, Grandoni and Vassilevska Williams.
- **Edge betweenness.** Compute for each edge the share of shortest paths that use it. The same dependency method gives it in the same time; the [Girvan-Newman algorithm](/girvan-newman-algorithm/) recomputes it after each edge removal.
- **Endpoints, bounded distance, groups.** Count the ends of the paths too, count only paths of length at most $k$, or count paths through a set of vertices. Brandes (2008) treats these with one scheme.
- **Approximation.** Return estimates $\tilde C_B(v)$ with $|\tilde C_B(v) - C_B(v)| \le \varepsilon\, n(n-1)$ for all $v$, with probability at least $1 - \delta$. Sampling methods do this, see below.
- **Top $k$.** Return the $k$ vertices of largest betweenness, possibly approximately.
- **Dynamic.** Keep the values up to date when edges are added or removed.

## Examples

**A worked example.** Take the undirected graph with the vertices 0 to 6 and the 9 edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$. The output, over unordered pairs, is

| $v$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $C_B(v)$ | 0 | 2 | 2 | 9 | 8 | 0 | 0 |

The [Brandes' algorithm](/brandes-algorithm/) page traces how one search from vertex 0 produces its share of these values.

**A directed example.** Take the arcs $0 \to 1$, $1 \to 2$, $0 \to 3$, $3 \to 2$, $2 \to 4$. The pairs with a path through an inner vertex are $(0, 2)$ with the two paths $0, 1, 2$ and $0, 3, 2$; $(0, 4)$ with the two paths $0, 1, 2, 4$ and $0, 3, 2, 4$; $(1, 4)$ through 2; and $(3, 4)$ through 2. So $C_B(1) = C_B(3) = \frac12 + \frac12 = 1$, $C_B(2) = 1 + 1 + 1 = 3$, and $C_B(0) = C_B(4) = 0$. No vertex reaches 0 and 4 reaches nothing, which the sum handles by leaving those pairs out.

**A weighted example.** Take the triangle $a, b, c$ with lengths $w(a, b) = 1$, $w(b, c) = 1$ and $w(a, c) = 2$. The pair $\{a, c\}$ has two shortest paths of length 2: the edge $a c$ and the path $a, b, c$. So $C_B(b) = 1/2$. With $w(a, c) = 3$, the only shortest path is $a, b, c$ and $C_B(b) = 1$. With $w(a, c) = 1.5$, $C_B(b) = 0$.

## Known algorithms

| algorithm | graphs | time | space |
|---|---|---|---|
| all-pairs counts, then a sum over all triples $s, v, t$ | any, positive lengths | $\Theta(n^3)$ | $\Theta(n^2)$ |
| [Brandes' algorithm](/brandes-algorithm/) with [breadth-first search](/breadth-first-search/) | no lengths | $O(nm)$ | $O(n + m)$ |
| Brandes' algorithm with [Dijkstra's algorithm](/dijkstra/) and a Fibonacci heap | positive lengths | $O(nm + n^2 \log n)$ | $O(n + m)$ |
| source sampling (Brandes and Pich) | any | $O(km)$ or $O(k(m + n \log n))$ for $k$ sources | $O(n + m)$ |
| path sampling (Riondato and Kornaropoulos) | any | depends on the sample size, which is bounded by the vertex diameter, not by $n$ | $O(n + m)$ |

**The direct method.** Compute the distances $d(s, t)$ and the counts $\sigma_{st}$ for all pairs, for example by one BFS or Dijkstra run from each source that also counts paths, or by [Floyd-Warshall](/floyd-warshall/) with counts. Then for each triple, add $\sigma_{sv}\sigma_{vt}/\sigma_{st}$ to $C_B(v)$ when $d(s, v) + d(v, t) = d(s, t)$. The triple loop costs $\Theta(n^3)$ time and the tables $\Theta(n^2)$ space.

**Source sampling.** Write $\delta_{s\bullet}(v) = \sum_{t} \sigma_{st}(v)/\sigma_{st}$, so $C_B(v) = \sum_s \delta_{s \bullet}(v)$ over ordered pairs. Pick sources $s_1, \ldots, s_k$ uniformly and independently, and return $\tilde C_B(v) = \frac{n}{k} \sum_{i} \delta_{s_i \bullet}(v)$. Each term has mean $\frac1n \sum_s \delta_{s\bullet}(v)$, so $\mathbb{E}[\tilde C_B(v)] = C_B(v)$: the estimate is unbiased. Each $\delta_{s\bullet}(v)$ is in $[0, n - 2]$, so the Hoeffding bound and a [union bound](/union-bound/) over the $n$ vertices give an additive error of at most $\varepsilon\, n(n-2)$ for all vertices at once with probability at least $1 - \delta$, when $k \ge \frac{1}{2\varepsilon^2} \ln \frac{2n}{\delta}$. Brandes' dependency pass computes $\delta_{s\bullet}$ for one source in $O(m)$ time without lengths.

## Bounds

- **Upper bound.** $O(nm)$ time for graphs without lengths and $O(nm + n^2 \log n)$ with positive lengths, both by Brandes (2001), in the [word RAM](/word-ram/) model with $O(1)$-time arithmetic on the counts.
- **Lower bound, trivial.** The output has $n$ numbers and the input must be read, so $\Omega(n + m)$.
- **Conditional lower bounds, dense weighted graphs.** Abboud, Grandoni and Vassilevska Williams show that computing the betweenness centrality of one vertex in a weighted graph is equivalent to [all-pairs shortest paths](/all-pairs-shortest-paths/) under subcubic reductions. So an $O(n^{3 - \varepsilon})$ algorithm for it would refute the [APSP conjecture](/apsp-conjecture/).
- **Conditional lower bounds, quadratic time.** Borassi, Crescenzi and Habib (2016) put the betweenness centrality of a given vertex in a web of reductions from a quadratic-time variant of $k$-SAT: a truly subquadratic algorithm for it, with time $O(n^{2 - \varepsilon})$ on the graphs of their reduction, would refute the strong exponential time hypothesis. Since all vertices are at least as hard as one, Brandes' $O(nm)$ bound, which is $O(n^2)$ on sparse graphs, cannot be improved by a polynomial factor on such graphs under this hypothesis.

## Reductions

- **To single-source shortest paths.** Brandes' algorithm makes $n$ calls of a single-source shortest-path search that also counts the paths, plus a linear-time pass for each. So betweenness costs at most $n$ times the cost of [single-source shortest paths](/single-source-shortest-paths/) with path counting.
- **From APSP, for weighted graphs.** The subcubic equivalence above goes both ways: a subcubic algorithm for APSP gives one for betweenness of a vertex, and the reverse holds.
- **To edge betweenness.** Vertex betweenness of the graph in which each edge is subdivided by a new vertex, with half the length on each part, gives edge betweenness. The cost grows from $n$ to $n + m$ vertices; a direct edge version of Brandes' pass avoids this.

## Applications

- Finding brokers and bridges in social networks; see [structural holes](/structural-holes/) and [ego networks](/ego-network/).
- Community detection by the [Girvan-Newman algorithm](/girvan-newman-algorithm/), which removes edges of high edge betweenness.
- Vulnerability of road, power and communication networks: vertices and links whose loss makes many routes longer.
- Load estimates in routing, since betweenness is the traffic under shortest-path routing with one unit for each pair.

## References
