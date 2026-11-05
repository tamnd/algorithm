---
tag: 8E77R4
kind: algorithm
slug: recursive-largest-first
name: Recursive largest first
aliases:
- RLF
area: graphs/coloring-and-cliques
level: advanced
summary: Builds one color class at a time as a maximal independent set, starting from the most constrained vertices.
solves: [graph-coloring]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, k: the number of colors used}
  time: {worst: O(n^2 + k m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [graph-coloring, maximal-independent-set, welsh-powell-algorithm]
see_also: [dsatur, greedy-coloring, lawler-chromatic-number, delta-plus-one-bound, chromatic-number, k-coloring]
sources:
  - paper: doi:10.6028/jres.084.024
    title: Frank Thomson Leighton, A graph coloring algorithm for large scheduling problems, Journal of Research of the National Bureau of Standards 84(6), 489 to 506 (1979)
    locator: the RLF algorithm, its selection rules and its O(n^3) bound
  - book: isbn:9783319257280
    title: R. M. R. Lewis, A Guide to Graph Colouring, Algorithms and Applications, Springer, 2016
    locator: Chapter 3, Bounds and constructive algorithms (the RLF algorithm and its comparison with greedy and DSatur)
---

Recursive largest first (RLF) is a heuristic for [graph coloring](/graph-coloring/) that builds the colors one at a time, each as a [maximal independent set](/maximal-independent-set/) of the vertices that are still uncolored. It chooses the members of a class greedily: first the uncolored vertex with the most uncolored neighbors, then repeatedly the candidate with the most neighbors among the vertices that the class has already ruled out. Leighton designed it in 1979 for exam timetabling, and it usually uses fewer colors than [Welsh-Powell](/welsh-powell-algorithm/) and often fewer than [DSatur](/dsatur/), at a higher cost of $O(n^2 + km)$ time.

## In plain words

Fill one color at a time, and make each color take as many vertices as it can. Start the color with the busiest vertex, the one with the most uncolored neighbors.

Each vertex in the color rules out its neighbors for this color. When choosing the next vertex for the color, prefer one that is linked to many of the vertices already ruled out. Adding it rules out few new vertices, because most of its neighbors are out already, so more room is left for later members. When no vertex can join, close the color and start the next one with the vertices still left.

## The problem

The input is a simple undirected graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, given as [adjacency lists](/adjacency-list/). The output is a proper coloring $c : V \to \{1, \ldots, k\}$. The algorithm does not promise the least $k$; finding it is NP-hard.

## The algorithm

$U$ is the set of uncolored vertices. While a class is built, $P$ holds the candidates, the vertices of $U$ with no neighbor in the class, and $W$ holds the vertices of $U$ that have a neighbor in the class.

```pseudo id=main
RLF(G)
L1  U ← V, k ← 0
L2  while U ≠ ∅ do
L3      k ← k + 1, P ← U, W ← ∅
L4      v ← the vertex of P with the most neighbors in U, ties by smaller index
L5      loop
L6          c[v] ← k, remove v from P and from U
L7          move every neighbor of v that is in P from P to W
L8          if P = ∅ then leave the loop
L9          v ← the vertex of P with the most neighbors in W, ties by fewest neighbors in P, then smaller index
L10 return c
```

Line L4 starts the class with the most constrained uncolored vertex. Line L9 is Leighton's rule: a candidate with many neighbors in $W$ has few neighbors left in $P$ to remove, so the class can keep growing. The class closes at line L8 when no candidate is left; then every uncolored vertex is in $W$, and these vertices form the $U$ of the next class.

The implementation keeps, for each vertex, the number of its neighbors in $P$ and in $W$. When a vertex leaves $P$ (line L6 or line L7), the counts of its neighbors change by one, so the scan of line L9 reads the counts in $O(1)$ per candidate.

## Example

Take the graph with 7 vertices and the edges $02, 04, 05, 06, 13, 23, 24, 34, 46$.

| class | step | chosen | why | moved to $W$ | $P$ after |
|---|---|---|---|---|---|
| 1 | L4 | 0 | 4 neighbors in $U$, tie with 4, smaller index | 2, 4, 5, 6 | 1, 3 |
| 1 | L9 | 3 | 2 neighbors in $W$ (2 and 4), against 0 for vertex 1 | 1 | none |
| 2 | L4 | 4 | 2 neighbors in $U = \{1, 2, 4, 5, 6\}$ | 2, 6 | 1, 5 |
| 2 | L9 | 1 | tie at 0 and 0, smaller index | none | 5 |
| 2 | L9 | 5 | only candidate | none | none |
| 3 | L4 | 2 | $U = \{2, 6\}$, tie at 0, smaller index | none | 6 |
| 3 | L9 | 6 | only candidate | none | none |

The coloring is $c = (1, 2, 3, 1, 2, 2, 3)$ on the vertices $0, \ldots, 6$, with 3 colors. The graph has the triangle $\{2, 3, 4\}$, so 3 is optimal.

The rule of line L9 matters on the crown graph, $K_{t,t}$ minus a perfect matching, with the vertices labeled $a_1, b_1, a_2, b_2, \ldots$. All degrees are equal, so Welsh-Powell colors greedily in this order and uses $t$ colors. RLF starts with $a_1$, which rules out every $b_j$ with $j \ne 1$; then every $a_i$ has $t - 2$ neighbors in $W$ while $b_1$ has none, so the class takes all of the $a_i$, and RLF uses 2 colors.

## Correctness

**Claim.** RLF stops and returns a proper coloring. Each class $k$ is a maximal independent set of $G[U_k]$, where $U_k$ is the set $U$ when class $k$ starts, and so each vertex $v$ gets a color at most $\deg(v) + 1$.

During the loop of class $k$, the sets $C_k$ (the vertices colored $k$ so far), $P$ and $W$ partition $U_k$; no vertex of $P$ has a neighbor in $C_k$; and every vertex of $W$ has one. Line L6 adds to $C_k$ a vertex of $P$, so $C_k$ stays independent, and line L7 restores the invariant. When $P$ is empty, every vertex of $U_k \setminus C_k$ is in $W$, which is maximality. Each class has at least one vertex, so the outer loop runs at most $n$ times. The full proof is below.

## Complexity

**Time.** For each class, line L3 and the counts take $O(n + m)$ time. Each vertex of $U_k$ leaves $P$ once in class $k$, at line L6 or line L7, and updates the counts of its neighbors, which is $O(m)$ per class. Line L9 scans the candidates once for each member of the class, which costs $O(n)$ per colored vertex and $O(n^2)$ over the whole run. With $k$ classes the total is $O(n^2 + k(n + m))$, which is $O(n^2 + km)$. Since $k \le \Delta + 1$, this is $O(n^2 + \Delta m)$, and in the worst case $O(n^3)$ as Leighton stated.

**Space.** The sets and the two counters per vertex use $\Theta(n)$ extra words.

## Properties

- **Proper and bounded.** The coloring is proper, and $c(v) \le \deg(v) + 1$, so it uses at most $\Delta + 1$ colors.
- **Maximal classes.** Every class is a maximal independent set of the graph that is left. A vertex of color $j$ has a neighbor in each of the colors $1, \ldots, j - 1$.
- **Deterministic.** With the tie rules above, the output depends only on the labeled graph.
- **Not exact.** It can use more than $\chi(G)$ colors, and no heuristic of this kind has a good worst-case ratio, since $\chi$ is hard to approximate within $n^{1 - \varepsilon}$.

## Variants and improvements

- **Faster data structures.** Bucket queues keyed by the count of neighbors in $W$ make line L9 cheaper on sparse graphs.
- **As a step of exact or metaheuristic methods.** RLF gives the starting coloring for tabu search and the initial upper bound for branch and bound; the class-by-class view is also the idea behind exact algorithms over [maximal independent sets](/lawler-chromatic-number/).
- **Maximum independent sets instead.** Replacing the greedy class by a maximum independent set of $G[U]$ gives a coloring within a factor of about $\ln n$ of optimal, as in greedy set cover, at an exponential cost per class.

## When to use it

Use RLF when the quality of a heuristic coloring matters more than the time, for graphs of up to some thousands of vertices: exam timetables, register allocation in compilers that can afford quadratic time, and initial solutions for local search. For very large sparse graphs, [greedy coloring](/greedy-coloring/) in a good order or DSatur is faster.

## Pitfalls

- **Counting neighbors in the wrong set.** Line L4 counts neighbors in $U$, but line L9 counts neighbors in $W$. Counting in $U$ at line L9 gives a different and usually worse algorithm.
- **Stale counts.** A vertex that moves from $P$ to $W$ must update the counts of all its neighbors, including those already in $W$, or later classes start from wrong values.
- **Recomputing from scratch.** Counting neighbors in $W$ anew at each step of line L9 costs $O(m)$ per step and $O(nm)$ per class.

## Implementations

## History

Frank Thomson Leighton introduced RLF in 1979 at the National Bureau of Standards, for scheduling large sets of exams and compared it with degree-order heuristics such as that of Welsh and Powell. Later experimental studies, collected in Lewis's book, found it among the best constructive heuristics for coloring.

## References
