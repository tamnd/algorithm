---
tag: B1EQ7A
kind: problem
slug: chinese-postman-problem
name: Chinese postman problem
aliases:
- route inspection problem
area: graphs/paths-and-cycles
level: core
summary: Find a shortest closed walk that traverses every edge of a weighted graph at least once. Polynomial for undirected and directed graphs, NP-hard for mixed graphs.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n^3)}
prereqs: [eulers-theorem-eulerian-graphs, eulerian-circuit, minimum-weight-perfect-matching]
see_also: [edmonds-johnson-algorithm, rural-postman-problem, traveling-salesman-problem, min-cost-flow-problem, hierholzer-algorithm, all-pairs-shortest-paths, edmonds-blossom, eulerian-path-problem]
sources:
  - paper: "Kwan Mei-Ko, Graphic programming using odd or even points, Chinese Mathematics 1, 273 to 277 (1962)"
    locator: the whole paper (the problem and the first method, by improving a set of repeated edges)
  - paper: doi:10.1007/BF01580113
    title: Jack Edmonds and Ellis L. Johnson, Matching, Euler tours and the Chinese postman, Mathematical Programming 5, 88 to 124 (1973)
    locator: the whole paper (the undirected problem by shortest paths and minimum weight perfect matching, and the directed problem by a flow)
  - paper: doi:10.1145/321958.321974
    title: Christos H. Papadimitriou, On the complexity of edge traversing, Journal of the ACM 23(3), 544 to 554 (1976)
    locator: the whole paper (the postman problem on mixed graphs is NP-complete)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer (2018)
    locator: Chapter 12, b-matchings and T-joins (Section 12.2, the Chinese postman problem as a minimum weight T-join)
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer (2008)
    locator: Chapter 3, Section 3.3 and its notes on the Chinese postman problem
---

The Chinese postman problem asks for a shortest closed walk that uses every edge of a connected weighted graph at least once. If the graph has an [Eulerian circuit](/eulerian-circuit/), that circuit is the answer; otherwise some edges must be walked twice, and the problem is to choose the cheapest set of repeated edges that makes all degrees even. For undirected graphs, the cheapest repetition pairs up the odd vertices by a [minimum weight perfect matching](/minimum-weight-perfect-matching/) on their shortest path distances, which gives an $O(n^3)$ algorithm by [Edmonds and Johnson](/edmonds-johnson-algorithm/); for directed graphs, a [minimum cost flow](/min-cost-flow-problem/) does the same. For graphs with both directed and undirected edges the problem is NP-hard.

## In plain words

A postman must walk along every street of his district at least once and come back to the post office, and he wants to walk as little as possible. If at every crossing an even number of streets meet, he can walk each street exactly once. If not, he must walk some streets twice.

At a crossing with an odd number of streets, he arrives one time more than he leaves, or the other way round, so he needs one extra pass through it. The best plan is to pair up these odd crossings and, for each pair, walk the shortest way between them a second time. The hard part is to choose the pairs well, and there is a fast method for that.

## Definition

**Input.** A connected graph $G = (V, E)$ with $n$ vertices and $m$ edges and a weight $w(e) \ge 0$ on each edge. In the undirected version all edges are undirected; in the directed version all edges are arcs and $G$ must be strongly connected; in the mixed version both kinds occur. Parallel edges and self-loops are allowed. Isolated vertices are ignored: "connected" refers to the vertices with edges.

**Output.** A closed walk $W$ that traverses each edge at least once, arcs in their direction, and has the least total weight $w(W) = \sum_{e \in W} w(e)$, counted with repetition.

**Why the weights are nonnegative.** A closed walk may use an edge any number of times. With an undirected edge of negative weight, walking it back and forth adds a negative amount each time, so there is no shortest walk. In the directed version, a negative directed cycle has the same effect.

**Reformulation.** Let $X$ be the multiset of edge copies used more than once, each copy counted once for each extra use. Then $W$ uses each edge of $E + X$ exactly once, so $E + X$ has an Eulerian circuit, and $w(W) = w(E) + w(X)$. Conversely, any multiset $X$ of copies of edges of $G$ such that $E + X$ is Eulerian gives a walk of weight $w(E) + w(X)$, by [Euler's theorem](/eulers-theorem-eulerian-graphs/). So the problem is to find the cheapest such $X$:

- undirected: $X$ must have odd degree exactly at the odd vertices $T$ of $G$, that is, $X$ is a *$T$-join*;
- directed: at each vertex $v$, $X$ must have $\mathrm{out}_X(v) - \mathrm{in}_X(v) = \mathrm{in}_G(v) - \mathrm{out}_G(v)$.

## Variants

- **Undirected.** Polynomial: shortest paths plus a minimum weight perfect matching on the odd vertices, by Edmonds and Johnson (1973).
- **Directed.** Polynomial: a minimum cost flow from the vertices with more incoming than outgoing arcs to those with more outgoing than incoming arcs, along shortest paths. It requires strong connectivity; otherwise there is no closed walk through all arcs.
- **Mixed.** NP-hard: Papadimitriou (1976) proved that the postman problem on graphs with both arcs and undirected edges is NP-complete, even for planar graphs with degree at most 3 and unit weights. Deciding whether a mixed graph has an Eulerian circuit, with no repetition, is polynomial by a flow.
- **Windy postman.** Undirected edges whose cost depends on the direction of travel; NP-hard in general, since it contains the mixed case.
- **Rural postman.** Only a subset of the edges must be traversed; NP-hard, since with all required edges of weight 0 it contains the [traveling salesman problem](/traveling-salesman-problem/). See the [rural postman problem](/rural-postman-problem/).
- **Open postman walk.** The walk need not be closed. Add one edge between two odd vertices, or try the pair of ends; with two odd vertices the answer is an Eulerian trail.
- **$k$ postmen.** Several walks from a depot that together cover all edges, minimizing the longest one; NP-hard for $k \ge 2$.

## Examples

**One pair of odd vertices.** The undirected graph on $0, 1, 2, 3$ has the edges $01$ (weight 1), $12$ (2), $23$ (1), $30$ (3) and $02$ (4), of total weight 11. The odd vertices are 0 and 2, each of degree 3. Their distance is 3, along $0, 1, 2$. Repeating $01$ and $12$ makes all degrees even, and the closed walk $0, 1, 2, 1, 0, 2, 3, 0$ has weight $11 + 3 = 14$, which is optimal. Repeating the edge $02$ itself would cost 4.

**$K_4$ with unit weights.** All four vertices are odd. There are three ways to pair them, and each pair is joined by an edge of weight 1, so the best $X$ is a perfect matching of two edges, and the answer is $6 + 2 = 8$.

**Eulerian input.** If all degrees are even, $X = \emptyset$ and the answer is $w(E)$, found by [Hierholzer's algorithm](/hierholzer-algorithm/).

**Directed.** The arcs $0 \to 1$ (1), $1 \to 2$ (1), $2 \to 0$ (1) and $0 \to 2$ (2), of total weight 5. Vertex 0 has one more arc out than in, and vertex 2 one more in than out, so one extra path from 2 to 0 is needed; the cheapest is the arc $2 \to 0$, of weight 1. The optimal walk $0 \to 1 \to 2 \to 0 \to 2 \to 0$ has weight 6.

**No solution.** The directed path $0 \to 1$ has no closed walk through its arc, since it is not strongly connected. An undirected graph with edges in two components has no covering walk either.

## Known algorithms

| version | method | time |
|---|---|---|
| undirected | [Edmonds-Johnson](/edmonds-johnson-algorithm/): [all-pairs shortest paths](/all-pairs-shortest-paths/) among the odd vertices, a [minimum weight perfect matching](/minimum-weight-perfect-matching/) on them with the [blossom algorithm](/edmonds-blossom/), then an Euler circuit | $O(n^3)$ |
| directed | shortest paths and a [minimum cost flow](/min-cost-flow-problem/) (a transportation problem) from the vertices with more in-arcs to those with more out-arcs | polynomial |
| mixed | integer programming, or approximation; the best known factor is 3/2 by an algorithm of Raghavachari and Veerasamy | exponential in the worst case |
| undirected, small number $k$ of odd vertices | dynamic programming over subsets of odd vertices | $O(2^k k^2)$ after the shortest paths |

Kwan Mei-Ko's original method starts with any set of repeated edges that makes all degrees even and improves it: the set is optimal if and only if no edge is repeated more than once and on every cycle the repeated edges weigh at most half of the cycle. This gives a correct but not polynomial algorithm.

## Bounds

The answer is at least $w(E)$, with equality if and only if $G$ is Eulerian (for positive weights), and at most $2 w(E)$, since doubling every edge makes all degrees even. In the undirected version, an optimal $X$ never uses an edge more than once, so every edge is walked at most twice; if an edge is in $X$ twice, removing both copies keeps all parities and does not increase the weight.

The $O(n^3)$ bound comes from the shortest paths and from the blossom algorithm for minimum weight perfect matching on the at most $n$ odd vertices. Faster matching algorithms give better bounds for sparse graphs.

## Reductions

- **Undirected postman to $T$-join to matching.** The cheapest $X$ is a minimum weight $T$-join for $T$ the odd vertices. For nonnegative weights, a minimum $T$-join is the union of $|T|/2$ edge-disjoint shortest paths that pair up $T$, and the best pairing is a minimum weight perfect matching in the complete graph on $T$ with shortest path distances as weights (Edmonds and Johnson).
- **Directed postman to transportation.** Each vertex $v$ with $\delta(v) = \mathrm{in}(v) - \mathrm{out}(v) > 0$ supplies $\delta(v)$ units, each vertex with $\delta(v) < 0$ demands $-\delta(v)$ units, and sending a unit from $u$ to $v$ costs the shortest path distance $d(u, v)$. An optimal transportation plan gives the extra paths.
- **Hamiltonian cycle to rural postman.** Put a required self-loop of weight 0 at each vertex and make the original edges optional with weight 1. A closed walk that covers all loops visits every vertex, so for $n \ge 3$ a Hamiltonian cycle exists if and only if there is a covering walk of weight $n$. This is why the rural version is NP-hard.

## Applications

Planning routes for mail delivery, street sweeping, snow ploughs, garbage collection, meter reading and road or power line inspection, where every street or line must be covered. In testing, a shortest sequence of inputs that exercises every transition of a finite state machine is a directed postman tour of its state graph.

## References
