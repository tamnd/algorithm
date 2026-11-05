---
tag: PM9EGC
kind: algorithm
slug: greedy-coloring
name: Greedy coloring
aliases:
- first-fit coloring
area: graphs/coloring-and-cliques
level: intro
summary: Visit vertices in a fixed order and give each the smallest color unused by its neighbors.
solves: [graph-coloring]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [graph-coloring, adjacency-list, degree]
see_also: [delta-plus-one-bound, degeneracy-ordering, dsatur, welsh-powell-algorithm, chromatic-number, online-graph-coloring-problem]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 5.2, Colouring vertices (the greedy algorithm, the bound Δ + 1 and the colouring number)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 5.1, Vertex colorings and upper bounds (the greedy coloring algorithm and the Welsh-Powell bound)
  - paper: doi:10.1093/comjnl/10.1.85
    title: D. J. A. Welsh and M. B. Powell, An upper bound for the chromatic number of a graph and its application to timetabling problems, The Computer Journal 10(1), 85 to 86 (1967)
    locator: the whole paper (the order by non-increasing degree and the bound max min(d_i + 1, i))
  - paper: doi:10.1145/2402.322385
    title: David W. Matula and Leland L. Beck, Smallest-last ordering and clustering and graph coloring algorithms, Journal of the ACM 30(3), 417 to 427 (1983)
    locator: the smallest-last order and its use for greedy coloring
---

Greedy coloring visits the vertices of a graph in a fixed order and gives each vertex the smallest color that none of its already colored neighbors has. It produces a proper [coloring](/graph-coloring/) in $\Theta(n + m)$ time, with at most $\Delta + 1$ colors, where $\Delta$ is the maximum [degree](/degree/). The number of colors depends strongly on the order: some order always gives the [chromatic number](/chromatic-number/), and a bad order can use $n/2$ colors on a graph that needs 2. Most coloring heuristics are greedy coloring with a clever order.

## In plain words

Number the colors 1, 2, 3 and so on. Take the vertices one by one, in a list that you fix at the start. For each vertex, look at its neighbors that already have a color. Give the vertex the smallest color that none of them has.

A vertex never waits for a later vertex, and a color never changes. So the method is fast, and the result is always a valid coloring.

A vertex with few neighbors can only see a few colors, so it never needs a large color. That is why the method uses at most one color more than the largest number of neighbors. But the method does not look ahead. In a bad list, it can use many more colors than necessary.

## The problem

The input is a simple undirected graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, given as [adjacency lists](/adjacency-list/), and an order $\sigma = (v_1, \ldots, v_n)$ of $V$. The output is a proper coloring $c : V \to \{1, 2, \ldots\}$: $c(u) \ne c(v)$ for each edge $\{u, v\}$. The algorithm does not promise the least number of colors. Finding that number is NP-hard (see [graph coloring](/graph-coloring/)).

## The algorithm

```pseudo id=main
GREEDY-COLORING(G, σ)                  ▷ σ = (v1, ..., vn) is an order of V
L1  for each vertex v do c[v] ← 0       ▷ 0 means "not colored"
L2  for i ← 1 to n do  (v ← vi)
L3      for each neighbor w of v do
L4          if c[w] > 0 then used[c[w]] ← v
L5      k ← 1
L6      while used[k] = v do k ← k + 1
L7      c[v] ← k
L8  return c
```

The array $\mathrm{used}[1 \ldots n+1]$ starts with a value that is not a vertex. Line L4 stamps the colors of the colored neighbors of $v$ with the name $v$. So the test of line L6 sees only the stamps of the current vertex, and the array never needs to be cleared. Line L6 stops at the first color that no colored neighbor of $v$ has.

## Example

The *crown graph* on 6 vertices has the vertices $a_1, a_2, a_3, b_1, b_2, b_3$, and $a_i$ is adjacent to $b_j$ when $i \ne j$. It is bipartite with sides $\{a_1, a_2, a_3\}$ and $\{b_1, b_2, b_3\}$, so 2 colors are enough. Color it in the order $a_1, b_1, a_2, b_2, a_3, b_3$.

| step | vertex | colored neighbors and their colors | stamped colors | color given |
|---|---|---|---|---|
| 1 | $a_1$ | none | none | 1 |
| 2 | $b_1$ | none ($a_1$ is not a neighbor) | none | 1 |
| 3 | $a_2$ | $b_1 = 1$ | 1 | 2 |
| 4 | $b_2$ | $a_1 = 1$ | 1 | 2 |
| 5 | $a_3$ | $b_1 = 1$, $b_2 = 2$ | 1, 2 | 3 |
| 6 | $b_3$ | $a_1 = 1$, $a_2 = 2$ | 1, 2 | 3 |

The result uses 3 colors. In the order $a_1, a_2, a_3, b_1, b_2, b_3$, each $a_i$ gets color 1, and each $b_j$ sees only color 1 and gets color 2. The crown graph on $2k$ vertices, colored in the order $a_1, b_1, \ldots, a_k, b_k$, uses $k$ colors: $a_i$ and $b_i$ both get color $i$.

## Correctness

**Theorem.** GREEDY-COLORING returns a proper coloring. Each vertex $v$ gets a color $c(v) \le d^-(v) + 1$, where $d^-(v)$ is the number of neighbors of $v$ that come before $v$ in $\sigma$. So it uses at most $\Delta + 1$ colors.

The key fact is that when line L7 runs, the stamped colors are exactly the colors of the colored neighbors of $v$. So $v$ gets a color that no earlier neighbor has, and a later neighbor $w$ avoids $c(v)$ in its own turn. The colors stamped for $v$ are at most $d^-(v)$ values, so line L6 stops at a value of at most $d^-(v) + 1$. The full proof is below.

**Every graph has a good order.** Take a proper coloring with $\chi(G)$ colors, and list first the vertices of class 1, then those of class 2, and so on. By induction on the position, greedy gives each vertex of class $i$ a color of at most $i$: its earlier neighbors are in classes $1$ to $i - 1$ (none is in class $i$, as the class is independent), so by the induction hypothesis they use colors of at most $i - 1$ only. So greedy uses at most $\chi(G)$ colors in this order. There are $n!$ orders, so this fact gives no fast algorithm.

## Complexity

The cost is in the [word RAM](/word-ram/) model, with the graph as adjacency lists.

- Line L1 and the start value of $\mathrm{used}$ take $\Theta(n)$ time.
- Lines L3 and L4 run once for each pair $(v, w)$ with $w$ a neighbor of $v$, so $2m$ times in total.
- The loop of line L6 runs $c(v)$ times for $v$, and $c(v) \le d^-(v) + 1 \le \deg(v) + 1$. Over all $v$ this is at most $2m + n$ steps.

So the time is $\Theta(n + m)$ in every case: each adjacency list is read once whatever the input. The extra space is $\Theta(n)$ for $c$ and $\mathrm{used}$. A version that clears a Boolean array after each vertex also runs in $O(n + m)$ time, if it clears only the entries it set.

## Properties

- **Online.** The color of $v$ depends only on the vertices before $v$. So greedy works when the vertices arrive one by one and each needs its color at once. This is the *first-fit* algorithm of [online graph coloring](/online-graph-coloring-problem/).
- **Bound by the order.** The color of $v_i$ is at most $\min(i, d^-(v_i) + 1)$. If $\sigma$ lists the vertices by non-increasing degree $d_1 \ge d_2 \ge \cdots \ge d_n$, then $c(v_i) \le \min(i, d_i + 1)$, so $\chi(G) \le \max_i \min(d_i + 1, i)$ (Welsh and Powell 1967).
- **Grundy property.** Each vertex of color $k$ has a neighbor of each color $1, \ldots, k-1$. A coloring with this property is a *Grundy coloring*, and each Grundy coloring is the output of greedy in some order.
- **Deterministic.** The output depends only on $G$, $\sigma$ and the order of the adjacency lists (the last one does not change the colors).

## Variants and improvements

- **[Welsh-Powell](/welsh-powell-algorithm/).** Use the order of non-increasing degree.
- **[Smallest-last ordering](/degeneracy-ordering/).** Remove a vertex of least degree again and again, and color in the reverse order. Then $d^-(v) \le d$, the [degeneracy](/degeneracy/), and greedy uses at most $d + 1$ colors. This gives 6 colors on planar graphs.
- **[DSATUR](/dsatur/).** Choose the next vertex during the run: the one whose neighbors already show the most colors.
- **[Recursive largest first](/recursive-largest-first/).** Build one color class at a time as a large independent set.
- **Perfect elimination order.** On a [chordal graph](/chordal-graph/), greedy in the reverse of a perfect elimination order is optimal. See [coloring chordal graphs](/chordal-graph-coloring/).
- **Iterated greedy.** Run greedy again with the classes of the last coloring as blocks of the order. By the argument of the good order above, the number of colors never goes up.

## When to use it

Use greedy coloring when you need a valid coloring fast and an optimal one is not required, as in register allocation heuristics or a first solution for a local search. It is the right choice for an online problem. With a smallest-last order, it gives the $d + 1$ guarantee at the same cost, which is much better than $\Delta + 1$ on sparse graphs with a few vertices of high degree. When the number of colors matters more than time, use [DSATUR](/dsatur/) or an exact method such as [Björklund's algorithm](/bjorklund-chromatic-number/) on small graphs.

## Pitfalls

- **Searching for the free color badly.** Testing each color $k = 1, 2, \ldots$ against all neighbors costs $\Theta(\deg(v) \cdot c(v))$ for $v$, which is $\Theta(n^2)$ on dense inputs. Mark the neighbor colors first (line L4), then scan (line L6).
- **Clearing the marks in full.** Clearing an array of size $n$ for each vertex costs $\Theta(n^2)$ in total. Use the stamp $v$ of line L4, or clear only the entries that were set.
- **Trusting the order.** The input order of the vertices is arbitrary, and on a crown graph it can cost $n/2$ colors where 2 are enough. Use a degree-based order.
- **Assuming the bound $\Delta + 1$ is the answer.** By [Brooks' theorem](/brooks-theorem/), $\chi(G) = \Delta + 1$ only when some component of $G$ is a complete graph on $\Delta + 1$ vertices or, for $\Delta = 2$, an odd cycle. A star with $n - 1$ leaves has $\Delta = n - 1$ and $\chi = 2$.

## Implementations

## History

Greedy coloring is the oldest coloring heuristic, and its source is not clear. Welsh and Powell published the order by non-increasing degree and the bound $\max_i \min(d_i + 1, i)$ in 1967, for timetabling. Matula and Beck studied the smallest-last order in 1983.

## References
