---
tag: Y06F76
kind: algorithm
slug: edmonds-johnson-algorithm
name: Edmonds-Johnson algorithm
aliases:
- Edmonds-Johnson route inspection algorithm
area: graphs/paths-and-cycles
level: advanced
summary: Solves the undirected Chinese postman problem by pairing the odd vertices with a minimum weight perfect matching on shortest path distances, then taking an Euler circuit.
solves: [chinese-postman-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, k: the number of vertices of odd degree}
  time: {worst: O(n^3), best: Θ(n + m)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1973
  people: [Jack Edmonds, Ellis L. Johnson]
  note: Edmonds and Johnson reduced the postman problem to shortest paths and weighted matching in Mathematical Programming in 1973, giving the first polynomial algorithm.
prereqs: [chinese-postman-problem, minimum-weight-perfect-matching, dijkstra, hierholzer-algorithm]
see_also: [edmonds-blossom, eulers-theorem-eulerian-graphs, all-pairs-shortest-paths, bitmask-dp, fleury-algorithm, rural-postman-problem, eulerian-circuit, handshaking-lemma]
sources:
  - paper: doi:10.1007/BF01580113
    title: Jack Edmonds and Ellis L. Johnson, Matching, Euler tours and the Chinese postman, Mathematical Programming 5, 88 to 124 (1973)
    locator: the whole paper (the reduction to shortest paths and minimum weight perfect matching, T-joins, and the directed case)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer (2018)
    locator: Chapter 12, Section 12.2, T-joins (the Chinese postman problem and the reduction of a minimum T-join to weighted matching)
  - book: isbn:9780471558941
    title: William J. Cook, William H. Cunningham, William R. Pulleyblank and Alexander Schrijver, Combinatorial Optimization, Wiley (1998)
    locator: Chapter 5, Optimal matchings, and its section on T-joins and postman problems
  - paper: "Kwan Mei-Ko, Graphic programming using odd or even points, Chinese Mathematics 1, 273 to 277 (1962)"
    locator: the whole paper (the problem)
---

The Edmonds-Johnson algorithm solves the undirected [Chinese postman problem](/chinese-postman-problem/): it finds a shortest closed walk that uses every edge of a connected graph with nonnegative weights at least once. It computes shortest path distances between the $k$ vertices of odd degree, pairs them up by a [minimum weight perfect matching](/minimum-weight-perfect-matching/), adds a second copy of each edge on the matched shortest paths, and returns an [Eulerian circuit](/eulerian-circuit/) of the result. With [Dijkstra's algorithm](/dijkstra/) and the [blossom algorithm](/edmonds-blossom/) it runs in $O(n^3)$ time. The input is an undirected multigraph, with parallel edges, self-loops and isolated vertices allowed.

## In plain words

To walk every street and come home, a postman must repeat some streets wherever an odd number of streets meet. Each such crossing needs one extra pass, and an extra pass joins two such crossings by some route. So the extra walking is a set of routes, each joining two odd crossings, with every odd crossing used exactly once.

The cheapest route between two crossings is a shortest path. The only real choice is which odd crossing to join with which, and finding the cheapest way to pair them is a classical problem with a fast method. Once the extra routes are added, every crossing is even, and a walk that uses every street exactly once exists and is easy to find.

## The problem

The input is an undirected multigraph $G = (V, E)$ with $n$ vertices, $m$ edges and a weight $w(e) \ge 0$ on each edge. The output is a closed walk that uses every edge at least once and has the least total weight, counted with repetition, or NIL if the edges of $G$ are not all in one component, since then no such walk exists. A self-loop adds 2 to the degree of its vertex; by the [handshaking lemma](/handshaking-lemma/), the number $k$ of odd vertices is even.

## The algorithm

Write $d(s, t)$ for the shortest path distance in $G$.

```pseudo id=main
EDMONDS-JOHNSON(G, w)
L1  if the edges of G are not all in one component then return NIL
L2  T ← the set of vertices of odd degree
L3  for each t ∈ T do compute shortest paths from t with Dijkstra's algorithm
L4  M ← a minimum weight perfect matching of the complete graph on T, where {s, t} weighs d(s, t)
L5  X ← for each {s, t} ∈ M, a copy of every edge on a shortest s-t path
L6  C ← an Eulerian circuit of the multigraph G + X, by Hierholzer's algorithm
L7  return C, of weight w(E) + w(X)
```

If $T$ is empty, $G$ is Eulerian, $X$ is empty, and the algorithm is [Hierholzer's algorithm](/hierholzer-algorithm/). Each copy in $X$ is mapped back to its original edge in the output, so the walk lists original edges, some of them twice or more.

**About the implementation.** The Python code here uses a [dynamic program over subsets](/bitmask-dp/) for line L4: the lowest unmatched odd vertex is paired with each other unmatched one, in $O(2^k k)$ time. This is exact but exponential in $k$, so the code is meant for small numbers of odd vertices. A polynomial implementation uses the blossom algorithm in its place.

## Example

The graph is $K_4$ on the vertices $0, 1, 2, 3$ with the weights $w(01) = 1$, $w(12) = 2$, $w(23) = 1$, $w(30) = 3$, $w(02) = 4$ and $w(13) = 5$, of total weight 16. Every vertex has degree 3, so $T = \{0, 1, 2, 3\}$. The shortest path distances are:

| | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| 0 | 0 | 1 | 3 | 3 |
| 1 | 1 | 0 | 2 | 3 |
| 2 | 3 | 2 | 0 | 1 |
| 3 | 3 | 3 | 1 | 0 |

For example $d(0, 2) = 3$ along $0, 1, 2$, which is less than the direct edge of weight 4, and $d(1, 3) = 3$ along $1, 2, 3$. Four points have three perfect matchings:

| matching | weight |
|---|---|
| $\{0, 1\}, \{2, 3\}$ | $1 + 1 = 2$ |
| $\{0, 2\}, \{1, 3\}$ | $3 + 3 = 6$ |
| $\{0, 3\}, \{1, 2\}$ | $3 + 2 = 5$ |

The best is $\{0, 1\}, \{2, 3\}$, so $X$ is a second copy of the edges $01$ and $23$. In $G + X$ the degrees are $4, 4, 4, 4$, and an Euler circuit such as $0, 1, 0, 2, 3, 2, 1, 3, 0$ uses every edge once and $01$ and $23$ twice. Its weight is $16 + 2 = 18$, the optimum.

## Correctness

The full proof is in the [correctness proof](proofs/correctness/). In outline, a closed walk that covers all edges is the same as an Eulerian circuit of $G + X$, where $X$ is the multiset of repeated uses. $G + X$ is Eulerian exactly when $X$ has odd degree at the vertices of $T$ and even degree elsewhere, a *$T$-join*. So the optimum is $w(E)$ plus the least weight of a $T$-join. A cheapest $T$-join can be taken as a set of edges with no repetition, and any such set contains $|T|/2$ edge-disjoint trails that pair up $T$. Each trail weighs at least the distance between its ends, so every $T$-join weighs at least the minimum perfect matching of line L4. Conversely, the union of the matched shortest paths in line L5 is a $T$-join of exactly that weight. So $X$ is a cheapest $T$-join, and the circuit of line L6 is optimal.

## Complexity

Line L1 is one search, $O(n + m)$. Line L3 runs Dijkstra's algorithm $k \le n$ times, in $O(k(m + n \log n))$ time with a Fibonacci heap, which is $O(n^3)$ at most. The blossom algorithm finds the matching of line L4 on $k$ points in $O(k^3)$ time. $X$ has at most $(k/2)(n - 1)$ edges, so lines L5 and L6 take $O(m + kn)$ time. The total is $O(n^3)$, and $O(n + m)$ when $G$ is Eulerian. The space is $O(n^2)$ for the distances, or $O(kn)$ if only the rows of the odd vertices are kept.

With the subset dynamic program, line L4 takes $O(2^k k)$ time and $O(2^k)$ space instead.

## Properties

- **Exact.** The result is optimal, not an approximation.
- **Each edge at most twice.** A cheapest $X$ never needs two copies of the same edge, since both could be removed without changing any parity. So an optimal walk uses each edge once or twice.
- **Bounded cost.** The answer is at most $2 w(E)$, since doubling every edge is one valid $X$.
- **Undirected only.** The directed problem uses a [minimum cost flow](/min-cost-flow-problem/) instead of a matching, and the mixed problem is NP-hard.

## Variants and improvements

- **Directed postman.** Replace the matching by a transportation problem from the vertices with more in-arcs to those with more out-arcs, with shortest path costs; Edmonds and Johnson treat this case too.
- **Open walk.** For a covering walk that need not be closed, the two ends may stay odd: try each pair of odd vertices as ends, or add a dummy vertex joined to all odd vertices by edges of weight 0.
- **Few odd vertices.** For small $k$ the subset dynamic program of the implementation is simpler than the blossom algorithm and fast in practice.
- **Rural postman.** If only some edges must be covered, the problem becomes NP-hard; Frederickson's heuristic uses the same matching idea with a [minimum spanning tree](/minimum-spanning-tree/) to connect the components of required edges, with a 3/2 approximation guarantee.
- **Sparse graphs.** Faster shortest path and matching algorithms improve the bound when $m$ is much less than $n^2$.

## When to use it

Use it to plan routes that must cover every edge of an undirected network: street cleaning, snow removal, mail delivery on two-sided streets, inspection of lines or pipes. If all degrees are already even, use Hierholzer's algorithm directly. For one-way streets use the directed version, and for a mix of one-way and two-way streets use integer programming or a heuristic.

## Pitfalls

- **Matching on the edges of $G$ only.** Two odd vertices that are not adjacent can still be paired; the matching is on the complete graph with shortest path distances.
- **Greedy pairing.** Pairing the closest odd vertices first is not optimal in general; the matching must be computed exactly.
- **Negative weights.** With a negative edge the problem has no optimum, since the walk can go back and forth on that edge. The implementation rejects such input.
- **Disconnected input.** Isolated vertices are harmless, but edges in two components have no covering walk; check line L1.
- **Forgetting loops in the degree.** A self-loop adds 2 to the degree, so it never makes a vertex odd.

## Implementations

## History

Kwan Mei-Ko posed the problem in 1962 and gave an optimality condition for the set of repeated edges, which led to an improvement method but not to a polynomial algorithm. Alan Goldman named it the Chinese postman problem. Edmonds and Johnson solved it in 1973, using Edmonds' weighted matching algorithm from 1965 and introducing the notion of a $T$-join, which became a standard tool of combinatorial optimization.

## References
