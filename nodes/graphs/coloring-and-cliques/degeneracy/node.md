---
tag: 547NP2
kind: concept
slug: degeneracy
name: Degeneracy
aliases:
- k-core number
area: graphs/coloring-and-cliques
level: core
summary: Smallest k such that every subgraph has a vertex of degree at most k.
prereqs: [degree, induced-subgraph, greedy-coloring]
see_also: [degeneracy-ordering, k-core, k-core-decomposition, arboricity, delta-plus-one-bound, chromatic-number, sparse-graph, bron-kerbosch]
sources:
  - paper: doi:10.4153/CJM-1970-125-1
    title: Don R. Lick and Arthur T. White, k-degenerate graphs, Canadian Journal of Mathematics 22(5), 1082 to 1096 (1970)
    locator: the whole paper (the definition of k-degenerate graphs and their basic properties)
  - paper: doi:10.1145/2402.322385
    title: David W. Matula and Leland L. Beck, Smallest-last ordering and clustering and graph coloring algorithms, Journal of the ACM 30(3), 417 to 427 (1983)
    locator: the whole paper (the smallest-last order, its linear-time computation, and coloring with degeneracy plus one colors)
  - paper: doi:10.1016/S0021-9800(68)80081-X
    title: G. Szekeres and H. S. Wilf, An inequality for the chromatic number of a graph, Journal of Combinatorial Theory 4(1), 1 to 3 (1968)
    locator: the whole paper (χ(G) ≤ 1 + max over subgraphs of the minimum degree)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 5.2, Colouring vertices (the colouring number col(G), equal to the degeneracy plus one)
  - paper: doi:10.1137/0214017
    title: Norishige Chiba and Takao Nishizeki, Arboricity and subgraph listing algorithms, SIAM Journal on Computing 14(1), 210 to 223 (1985)
    locator: the whole paper (listing triangles and cliques in time bounded by arboricity times the number of edges)
---

The degeneracy of a [graph](/graph/) is the largest minimum degree of any of its subgraphs. Equivalently, it is the smallest $k$ such that every subgraph has a vertex of [degree](/degree/) at most $k$, and a graph with this property is called *$k$-degenerate*. It is computed in linear time by repeatedly removing a vertex of minimum degree, the [smallest-last ordering](/degeneracy-ordering/). Degeneracy measures how sparse a graph is everywhere: it bounds the [chromatic number](/chromatic-number/), the clique number and the edge count, and many algorithms for sparse graphs run fast when it is small.

## In plain words

Take a network and keep deleting a point with the fewest lines, until nothing is left. Each time, note how many lines that point still had. The largest number you noted is the degeneracy.

A small degeneracy means the network is thin everywhere: no part of it, however you cut it out, is dense. Trees have degeneracy 1, road maps and other flat drawings have at most 5, and a group where everyone knows everyone has a large one.

Small degeneracy makes many problems easier. You can color the network with one more color than the degeneracy, and you can find all tight groups quickly.

## The idea

Let $G = (V, E)$ be a finite simple undirected graph with $n$ vertices and $m$ edges, and write $\delta(H)$ for the minimum degree of a graph $H$. The degeneracy is

$$\mathrm{dgn}(G) = \max \{ \delta(H) : H \subseteq G,\ V(H) \ne \emptyset \},$$

and $\mathrm{dgn}(G) = 0$ for the empty graph. It is enough to take induced subgraphs, since adding the missing edges of $G[V(H)]$ does not lower any degree.

**Three equivalent forms.** For each integer $k \ge 0$ the following are equivalent:

1. $\mathrm{dgn}(G) \le k$: every non-empty subgraph has a vertex of degree at most $k$.
2. There is an order $v_1, \ldots, v_n$ of $V$ in which each $v_i$ has at most $k$ neighbors among $v_{i+1}, \ldots, v_n$.
3. The $(k+1)$-[core](/k-core/) of $G$ is empty: $G$ has no non-empty subgraph of minimum degree at least $k + 1$.

From 1 to 2: remove a vertex of degree at most $k$, then a vertex of degree at most $k$ in what is left, and so on. From 2 to 1: in a subgraph $H$, the vertex of $H$ that comes first in the order has all its neighbors in $H$ later in the order, so at most $k$ of them. Form 3 is form 1 restated. The order of form 2 is the smallest-last order, and the number $\mathrm{dgn}(G) + 1$ is called the *colouring number* $\mathrm{col}(G)$ in Diestel.

**Bounds.** Let $d = \mathrm{dgn}(G)$.

- $\delta(G) \le d \le \Delta(G)$.
- $m \le d n - \binom{d+1}{2}$ for $n \ge d$: in the order of form 2, the vertex $v_i$ has at most $\min(d, n - i)$ later neighbors, and $\sum_{i=1}^{n} \min(d, n - i) = d n - \binom{d+1}{2}$. In particular $m < d n$.
- $\binom{d+1}{2} \le m$, so $d \le \sqrt{2m}$: a subgraph of minimum degree $d$ has at least $d + 1$ vertices and at least $d(d+1)/2$ edges.
- $\omega(G) \le d + 1$ and $\chi(G) \le d + 1$. The second is the bound of Szekeres and Wilf; see the [$\Delta + 1$ bound](/delta-plus-one-bound/).
- With the [arboricity](/arboricity/) $a(G)$, the least number of forests that cover $E$: $a(G) \le d \le 2 a(G) - 1$ when $m \ge 1$. The left side holds because the order of form 2 splits the edges into $d$ forests (give the later neighbors of each vertex the labels $1, \ldots, d$; each label class has at most one edge from each vertex to a later one, so it has no cycle). The right side holds because, by the [Nash-Williams theorem](/nash-williams-arboricity-theorem/), a subgraph with $h$ vertices has at most $a(G)(h - 1)$ edges, hence a vertex of degree at most $2a(G)(h-1)/h < 2a(G)$.

**Computing it.** The [smallest-last ordering](/degeneracy-ordering/) computes $\mathrm{dgn}(G)$ and the order of form 2 in $\Theta(n + m)$ time with buckets indexed by degree. The same process gives the core number of every vertex, which is the [$k$-core decomposition](/k-core-decomposition/).

## Examples

| graph | $n$ | $\Delta$ | degeneracy |
|---|---|---|---|
| no edges | $n$ | 0 | 0 |
| forest with at least one edge | $n$ | any | 1 |
| cycle $C_n$ | $n$ | 2 | 2 |
| grid $P_r \times P_s$, $r, s \ge 2$ | $rs$ | up to 4 | 2 |
| outerplanar graph | $n$ | any | at most 2 |
| planar graph | $n$ | any | at most 5 |
| Petersen graph | 10 | 3 | 3 |
| hypercube $Q_t$ | $2^t$ | $t$ | $t$ |
| $K_{s,t}$, $s \le t$ | $s + t$ | $t$ | $s$ |
| $K_n$ | $n$ | $n - 1$ | $n - 1$ |
| star $K_{1, n-1}$ | $n$ | $n - 1$ | 1 |

The planar bound holds because each planar graph with $h \ge 3$ vertices has at most $3h - 6$ edges, so average degree below 6, and the same holds for each subgraph. The icosahedron is 5-regular and planar, so the bound 5 is reached. A $k$-regular graph has degeneracy exactly $k$, as the Petersen graph and $Q_t$ show.

**A worked case.** Take the graph on $0, \ldots, 6$ with the edges $01, 02, 12, 13, 23, 24, 34, 35, 45, 06, 56$. Its minimum degree is 2 (vertex 6). Removing 6 leaves 0 and 5 with degree 2, and removing minimum-degree vertices one by one never meets a degree above 2, so the degeneracy is 2 although $\Delta = 4$. The edge bound is tight here: $m = 11 = 2 \cdot 7 - \binom{3}{2}$. The graph has a triangle, so $\chi = \omega = 3 = d + 1$.

**The star.** For $K_{1, n-1}$, $\Delta = n - 1$ while $d = 1$. Bounds in terms of $d$ are much better than bounds in terms of $\Delta$ for graphs with a few vertices of high degree, which is the common shape of real networks.

## Where it is used

- **Coloring.** [Greedy coloring](/greedy-coloring/) in the reverse smallest-last order uses at most $d + 1$ colors. For planar graphs this gives a linear-time 6-coloring, the starting point of the [five color algorithm](/five-color-algorithm/).
- **Clique listing.** The [Bron-Kerbosch algorithm](/bron-kerbosch/) with its outer loop in degeneracy order lists all maximal cliques in $O(d\, n\, 3^{d/3})$ time (Eppstein, Löffler and Strash 2010). Each vertex together with its later neighbors spans at most $d + 1$ vertices, so cliques of a fixed size $k$ can be listed in $O(n\, d^{k-1})$ time.
- **Triangle and subgraph listing.** Orient each edge toward the vertex that is later in the smallest-last order. Each vertex has out-degree at most $d$, so all triangles are found in $O(m d)$ time, as in [triangle listing by degree](/triangle-listing-by-degree/). Chiba and Nishizeki gave the bound in terms of arboricity, which is within a factor 2 of $d$.
- **Network analysis.** The $k$-cores of a social or biological network, the maximal subgraphs of minimum degree $k$, mark its dense center; the degeneracy is the index of the deepest non-empty core.
- **Parameterized algorithms.** Many problems that are hard in general, such as dominating set and independent set, have [fixed-parameter](/fixed-parameter-tractable/) algorithms on graphs of bounded degeneracy, or in terms of $d$ and the solution size.
- **Sparse graph classes.** Bounded degeneracy is a common definition of a [sparse graph](/sparse-graph/) class. Planar graphs, graphs of bounded [treewidth](/treewidth/), and graphs that exclude a fixed minor all have bounded degeneracy.

## References
