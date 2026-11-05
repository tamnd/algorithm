---
tag: AFEY7W
kind: algorithm
slug: five-color-algorithm
name: Five-color algorithm
aliases:
- Heawood's five-color algorithm
area: graphs/planar-graphs
level: core
summary: Color a planar graph with 5 colors by peeling off vertices of degree at most 5 and freeing a color with a Kempe chain interchange when needed.
solves: [graph-coloring]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(n^2)}
  space: {extra: Θ(n)}
properties: {deterministic: true, needs_embedding: false, recursive: false}
history:
  year: 1890
  people: [Percy John Heawood, Alfred Bray Kempe]
  note: Kempe introduced the chain interchange in his 1879 proof of the four color theorem; Heawood found the error in 1890 and showed that the argument proves five colors.
prereqs: [five-color-theorem, kempe-chain, graph-coloring, planar-graph, degeneracy]
see_also: [four-color-theorem, euler-formula, greedy-coloring, breadth-first-search, chromatic-number, jordan-curve-theorem, rotation-system]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 5, Colouring, Section 5.1, Colouring maps and planar graphs (the five colour theorem and its proof by Kempe chains)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 6.3, Coloring of planar graphs (the five color theorem)
  - paper: "Norishige Chiba, Takao Nishizeki and Nobuji Saito, A linear 5-coloring algorithm of planar graphs, Journal of Algorithms 2(4), 317 to 327 (1981)"
    locator: the linear-time algorithm
  - paper: "David W. Matula, Yossi Shiloach and Robert E. Tarjan, Two linear-time algorithms for five-coloring a planar graph, Technical Report STAN-CS-80-830, Stanford University, 1980"
    locator: the two linear-time algorithms
  - paper: "Percy J. Heawood, Map-colour theorem, Quarterly Journal of Pure and Applied Mathematics 24, 332 to 338 (1890)"
    locator: the error in Kempe's proof and the five colour theorem
---

The five-color algorithm colors the vertices of a simple [planar graph](/planar-graph/) with at most 5 colors so that adjacent vertices get different colors. It removes vertices of degree at most 5 one by one, then puts them back in reverse order. A vertex that comes back has at most 5 colored neighbours; if they use all 5 colors, a [Kempe chain](/kempe-chain/) interchange frees one. This is the constructive form of the proof of the [five color theorem](/five-color-theorem/), and it runs in $O(n^2)$ time in the worst case; more careful versions run in linear time.

## In plain words

A network that you can draw on paper without crossing lines always has a dot with at most five lines. Take it out, put it on a pile, and repeat until no dot is left.

Now take the dots from the pile in reverse order and give each one a color. Each dot sees at most five neighbours that already have a color. If they use four colors or fewer, one of the five colors is free.

If the five neighbours use all five colors, pick two colors, say red and blue. Start at the red neighbour and collect all dots you can reach through red and blue dots. If the blue neighbour is not in this group, swap red and blue in the group. Now no neighbour is red, and the new dot takes red. The flat drawing makes sure that one of the pairs always works.

## The problem

Given a simple undirected graph $G = (V, E)$ with $n$ vertices, by adjacency lists, find a map $c : V \to \{0, 1, 2, 3, 4\}$ with $c(u) \ne c(v)$ for each edge $uv$. Such a map exists when $G$ is planar, by the [five color theorem](/five-color-theorem/). The algorithm needs no embedding: the input is only the graph, with no [rotation system](/rotation-system/) and no coordinates. The proof of correctness uses a plane drawing, but the algorithm never sees it. If $G$ is not planar, the algorithm either returns a valid 5-coloring or reports failure.

## The algorithm

```pseudo id=main
FIVE-COLOR(G)                          ▷ G simple, by adjacency lists; no embedding
L1  Q ← the vertices of degree at most 5; S ← empty list
L2  while Q is not empty do
L3      v ← pop Q; mark v removed; append v to S
L4      for each neighbour u of v not removed do deg[u] ← deg[u] − 1; if deg[u] = 5 then push u on Q
L5  if some vertex is not removed then fail ("not planar")
L6  for each v in S, from last to first do
L7      owner ← for each color k used by a colored neighbour of v, one such neighbour
L8      if fewer than 5 colors are used then c(v) ← least color not used; continue
L9      for each pair of colors i < j do
L10         x ← owner[i]; y ← owner[j]
L11         K ← the vertices reachable from x by a path whose vertices are colored i or j
L12         if y ∉ K then swap colors i and j on K; c(v) ← i; continue with the next v
L13     fail ("not planar")
L14 return c
```

**Peeling (lines L1 to L5).** The queue $Q$ holds the vertices whose degree in the remaining graph is at most 5. Removing $v$ lowers the degree of each remaining neighbour by 1, and a vertex enters $Q$ when its degree drops to 5, so each vertex enters $Q$ once. Every planar graph has a vertex of degree at most 5, and every subgraph of a planar graph is planar, so for a planar input the loop removes all vertices. The order $S$ is a 5-degenerate order (see [degeneracy](/degeneracy/)): each vertex has at most 5 neighbours that come after it in $S$.

**Coloring (lines L6 to L13).** When $v$ is colored, its colored neighbours are exactly its neighbours that come after it in $S$, so there are at most 5 of them. If they use fewer than 5 colors, line L8 takes a free color, as [greedy coloring](/greedy-coloring/) does. Otherwise $v$ has exactly 5 colored neighbours, one of each color. For a pair $i, j$, the set $K$ of line L11 is the Kempe chain of $x$: the connected component of $x$ in the subgraph induced by the vertices of colors $i$ and $j$. A [breadth-first search](/breadth-first-search/) finds it. If $y$ is not in it, swapping $i$ and $j$ on $K$ keeps the coloring proper, makes $x$ color $j$ and leaves $y$ color $j$, so no neighbour of $v$ has color $i$.

## Example

Take the maximal planar graph with 8 vertices and the 18 edges $01, 02, 06, 07, 16, 17, 23, 24, 25, 26, 27, 34, 35, 37, 45, 56, 57, 67$. The degrees are 4, 3, 6, 4, 3, 5, 5, 6.

**Peeling.** At the start $Q = [0, 1, 3, 4, 5, 6]$ (vertices 2 and 7 have degree 6), and $Q$ is used as a stack. Removing 6 lowers the degrees of 2 and 7 to 5, so they enter $Q$. The removal order is $S = 6, 7, 2, 5, 4, 3, 1, 0$.

**Coloring.** In reverse order: vertex 0 gets 0; 1 sees color 0 and gets 1; 3 sees nothing colored and gets 0; 4 sees 0 and gets 1; 5 sees 0 and 1 and gets 2; 2 sees 0, 1, 2 and gets 3; 7 sees 0, 1, 2, 3 and gets 4.

**Kempe step for vertex 6.** Its neighbours $0, 1, 2, 5, 7$ have the colors $0, 1, 3, 2, 4$, all five.

| pair $i, j$ | $x$, $y$ | chain $K$ of $x$ | $y \in K$? |
|---|---|---|---|
| 0, 1 | 0, 1 | $\{0, 1\}$, since 0 and 1 are adjacent | yes, try the next pair |
| 0, 2 | 0, 5 | $\{0\}$: the neighbours 1, 2, 7 of 0 have colors 1, 3, 4 | no |

Swapping on $K = \{0\}$ gives vertex 0 the color 2. Now no neighbour of 6 has color 0, so 6 gets 0. The result is $c = (2, 1, 3, 0, 1, 2, 0, 4)$ for the vertices 0 to 7. It is a proper coloring with 5 colors; this graph contains the triangle $2, 5, 7$ with the common neighbour 3, a $K_4$, so it needs at least 4.

## Correctness

Line L5 never fails for a planar graph, because each remaining graph is planar and so has a vertex of degree at most 5, by [Euler's formula](/euler-formula/). The coloring stays proper after each step: line L8 picks a color that no colored neighbour has, and a Kempe swap exchanges two colors on a whole component of the two-colored subgraph, so an edge between $K$ and the rest cannot have both ends of the same color. The main point is that line L13 is never reached. Fix a plane drawing and let $x_1, \ldots, x_5$ be the colored neighbours of $v$ in the cyclic order of the edges at $v$. If the chain of $x_1$ in the colors of $x_1, x_3$ contained $x_3$, then a path through it, together with $v$, would form a cycle that by the [Jordan curve theorem](/jordan-curve-theorem/) puts $x_2$ inside and $x_4$ outside, or the reverse. A chain of $x_2$ in the colors of $x_2, x_4$ cannot cross that cycle, since it has no vertex of the cycle. So one of the two pairs succeeds. Each loop is finite, so the algorithm stops. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $m$ be the number of edges; a simple planar graph has $m \le 3n - 6$ for $n \ge 3$, so $m = O(n)$.

- **Peeling.** Each vertex is removed once, and each edge lowers a degree at most once in each direction: $O(n + m) = O(n)$.
- **A vertex without a swap.** Lines L7 and L8 take $O(\deg(v))$, so $O(m)$ over all such vertices.
- **A vertex with a swap.** At most 10 pairs, and each search of line L11 takes $O(n + m)$. So $O(n)$ for each such vertex.

The total is $O(n^2)$ in the worst case, and $O(n)$ when no swap is needed. The extra space is $\Theta(n)$ for degrees, flags, the order, the colors and the search. The bound $O(n^2)$ is an upper bound for this simple form; linear-time versions (below) avoid long chain searches.

## Properties

- **No embedding needed.** The algorithm tries all pairs of colors instead of the two pairs that the plane drawing points to. This costs a factor of at most 5 and removes the need for a [planarity test](/planarity-testing/).
- **Certifying on bad inputs.** On a non-planar input the algorithm may still succeed; whatever it returns is a proper coloring with at most 5 colors.
- **Not optimal.** Deciding whether a planar graph has a 3-coloring is [NP-complete](/np-complete/), so the algorithm makes no attempt to use fewer colors. Every planar graph has a 4-coloring by the [four color theorem](/four-color-theorem/), but known algorithms for it are much more complex.
- **Deterministic and iterative.** No recursion is needed: the order is an explicit list and the chain is found by breadth-first search.

## Variants and improvements

- **Linear time by merging two neighbours.** If $v$ has degree 5, two of its neighbours are not adjacent, because otherwise the five neighbours would form a $K_5$ in a planar graph. Contract the two edges from $v$ to those neighbours; the result is planar, since it is a [minor](/graph-minor/) of a planar graph. Color it, and give both neighbours the color of the merged vertex, so $v$ sees at most 4 colors. Matula, Shiloach and Tarjan (1980) and Chiba, Nishizeki and Saito (1981) turned this idea, or a Kempe step with a short chain, into algorithms that run in $O(n)$ time.
- **Six colors.** Without the Kempe step, the same peeling with greedy coloring uses at most 6 colors, in $O(n)$ time.
- **Four colors.** The proof of the [four color theorem](/four-color-theorem/) also gives a 4-coloring algorithm that runs in $O(n^2)$ time, at the price of a large table of configurations.
- **Use the embedding.** With a rotation system, the algorithm tests only the two pairs $x_1, x_3$ and $x_2, x_4$ that the proof names.

## When to use it

Use it when a planar graph, such as a map or the graph of a mesh, needs a coloring with few colors and a short proof that the number is small: register allocation for planar interference graphs, map coloring, scheduling on planar conflict graphs. For colorings of general graphs, use [greedy coloring](/greedy-coloring/) with a degeneracy order, which gives at most one more color than the [degeneracy](/degeneracy/). When the [chromatic number](/chromatic-number/) itself is needed, use an exact method.

## Pitfalls

- **Testing only one pair.** Without an embedding, the pair $x_1, x_3$ of the proof is not known, and a single fixed pair can fail. Try all pairs, or compute the rotation at $v$.
- **Searching the wrong subgraph.** The chain must use only vertices that are already colored, with colors $i$ or $j$. Uncolored vertices, including $v$, have no color and are not in it.
- **Multigraphs.** Parallel edges break the degree bound of [Euler's formula](/euler-formula/); remove them first. A loop makes coloring impossible.
- **Recursion depth.** A recursive form, which removes one vertex and recurses, has depth $n$. The explicit order of lines L1 to L5 avoids this.

## Implementations

## History

Kempe published a proof of the four color theorem in 1879 that used the chain interchange. In 1890 Heawood showed that Kempe's argument fails for a vertex of degree 5 with four colors, and that the same argument proves that five colors suffice. The algorithm on this page is that proof, run on the graph (Diestel, Section 5.1; West, Section 6.3). Matula, Shiloach and Tarjan, and Chiba, Nishizeki and Saito, gave linear-time 5-coloring algorithms in 1980 and 1981.

## References
