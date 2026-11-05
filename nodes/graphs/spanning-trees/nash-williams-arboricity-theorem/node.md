---
tag: BRDHC8
kind: theorem
slug: nash-williams-arboricity-theorem
name: Nash-Williams arboricity theorem
area: graphs/spanning-trees
level: advanced
summary: Arboricity equals the maximum over subgraphs H of ceil(|E(H)| / (|V(H)| - 1)).
prereqs: [arboricity, spanning-forest, graphic-matroid]
see_also: [nash-williams-tutte-theorem, spanning-tree-packing, degeneracy, planar-graph, matroid, edge-coloring, spanning-tree-polytope, matroid-intersection-theorem]
sources:
  - paper: doi:10.1112/jlms/s1-39.1.12
    title: C. St. J. A. Nash-Williams, Decomposition of finite graphs into forests, Journal of the London Mathematical Society 39 (1964), 12
    locator: the whole paper (a one-page note with the theorem)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer Graduate Texts in Mathematics 173 (2017)
    locator: Chapter 2, Section 2.4, Tree-packing and arboricity (the theorem, derived from the tree-packing theorem)
  - paper: doi:10.1007/BF01758774
    title: Harold N. Gabow and Herbert H. Westermann, Forests, frames, and games, Algorithms for matroid sums and applications, Algorithmica 7 (1992), 465-497
    locator: the whole paper (algorithms that compute the arboricity and a cover by forests)
  - paper: doi:10.1137/0214017
    title: Norishige Chiba and Takao Nishizeki, Arboricity and subgraph listing algorithms, SIAM Journal on Computing 14(1) (1985), 210-223
    locator: the lemma that bounds the sum over edges uv of min(deg u, deg v) by 2a(G)m, and its use for planar graphs
---

The Nash-Williams arboricity theorem gives the least number of forests whose union is all the edges of a graph. It says that this number, the [arboricity](/arboricity/), equals the largest value of $\lceil |E(H)| / (|V(H)| - 1) \rceil$ over the subgraphs $H$ with at least two vertices. The bound is clearly necessary, since a forest on $|V(H)|$ vertices has at most $|V(H)| - 1$ edges, and the theorem says that the densest subgraph is the only obstacle. Nash-Williams proved it in 1964, as the covering counterpart of his tree-packing theorem.

## Statement

Let $G = (V, E)$ be a finite undirected multigraph without self-loops; parallel edges are allowed and count as different edges. The *arboricity* $a(G)$ is the least $k$ such that $E$ is the union of $k$ [forests](/spanning-forest/), and $a(G) = 0$ when $E$ is empty.

**Theorem (Nash-Williams 1964).** If $E \ne \emptyset$, then

$$a(G) = \max_{H} \left\lceil \frac{|E(H)|}{|V(H)| - 1} \right\rceil,$$

the maximum over the subgraphs $H$ of $G$ with $|V(H)| \ge 2$. Equivalently, $E$ is the union of $k$ forests if and only if $|E(H)| \le k\,(|V(H)| - 1)$ for every subgraph $H$ with at least one vertex.

It is enough to take *induced* subgraphs $H = G[S]$, since adding edges between the vertices of $H$ only raises the ratio, and connected ones, since the ratio of a disjoint union is at most the largest ratio of its parts.

**Connectivity and weights.** The graph need not be connected; the forests need not be spanning trees, and the theorem holds for each graph as it is. There are no weights, so ties do not arise. A self-loop is in no forest, so graphs with self-loops have no cover by forests, and they are excluded.

## In plain words

You want to paint every link of a network with as few colors as possible, so that the links of each color never close a loop. The fewest colors you need is the arboricity.

Look at any part of the network. Links of one color without a loop on a set of points are at most one fewer than the number of points. So that part needs at least its number of links divided by one fewer than its number of points, rounded up. The theorem says that the worst part of the network decides the answer: the largest such value is always enough colors.

## Proof

**The lower bound.** Let $E = F_1 \cup \cdots \cup F_k$ with each $F_i$ a forest, and let $H$ be a subgraph with $|V(H)| \ge 2$. The edges of $F_i$ in $H$ form a forest on $V(H)$, so there are at most $|V(H)| - 1$ of them. Hence $|E(H)| \le k(|V(H)| - 1)$ and $k \ge \lceil |E(H)| / (|V(H)| - 1) \rceil$.

**The upper bound.** Let $k$ be the maximum in the theorem, so $|E(H)| \le k(|V(H)| - 1)$ for every subgraph $H$ with at least one vertex. We use the matroid union theorem for the [graphic matroid](/graphic-matroid/) $M$ on $E$, whose independent sets are the forests and whose rank is $r(F) = |V| - c(F)$, with $c(F)$ the number of components of $(V, F)$.

*Matroid union theorem* (Edmonds; Nash-Williams). For a matroid with rank function $r$ on a finite set $E$, the largest size of a union of $k$ independent sets is $\min_{F \subseteq E} \big( |E \setminus F| + k\, r(F) \big)$.

The set $E$ is a union of $k$ forests if and only if this minimum is $|E|$, that is, if and only if $|F| \le k\, r(F)$ for every $F \subseteq E$. Fix $F$. Let $H_1, \ldots, H_c$ be the components of the graph $(V, F)$, where $H_i$ has $n_i$ vertices and $m_i$ edges of $F$, so $|F| = \sum_i m_i$ and $r(F) = \sum_i (n_i - 1)$. Each $H_i$ is a subgraph of $G$ with at least one vertex, so by the hypothesis $m_i \le k(n_i - 1)$. Summing over $i$ gives $|F| \le k\, r(F)$. So $E$ is the union of $k$ forests, and $a(G) \le k$. $\blacksquare$

Diestel derives the theorem from the [Nash-Williams-Tutte theorem](/nash-williams-tutte-theorem/) on packing spanning trees, applied to a graph with extra edges, which avoids matroids.

## Consequences

- **The example graph.** The graph on $a$ to $f$ with the edges $ab, ac, bc, bd, cd, ce, de, df, ef$ has $9 > 5$ edges, so it is not a forest and $a(G) \ge 2$. Its densest subgraph has ratio $\lceil 9/5 \rceil = 2$, so $a(G) = 2$. Indeed, $\{ac, bc, bd, ce, ef\}$ is a spanning tree, and the other edges $\{ab, cd, de, df\}$ form a forest, a single edge $ab$ and a star at $d$.
- **Complete graphs.** $a(K_n) = \lceil n / 2 \rceil$ for $n \ge 2$: the ratio of $K_n$ itself is $\lceil n / 2 \rceil$, and every subgraph is a smaller complete graph or sparser.
- **Planar graphs.** A simple planar graph with $p \ge 3$ vertices has at most $3p - 6$ edges, so each subgraph has ratio at most $(3p - 6)/(p - 1) < 3$. Hence every simple [planar graph](/planar-graph/) has arboricity at most 3, and the bound is attained, for example by the octahedron with 6 vertices and 12 edges, whose ratio is $\lceil 12/5 \rceil = 3$.
- **Degeneracy.** The arboricity and the [degeneracy](/degeneracy/) $d$ satisfy $a(G) \le d \le 2a(G) - 1$. Orienting each edge towards the vertex removed later in a degeneracy order gives out-degree at most $d$, and the $i$-th out-edges of the vertices form a forest, so $a \le d$. Each subgraph $H$ has at most $a(G)(|V(H)| - 1)$ edges, so its average degree is less than $2a(G)$, and it has a vertex of degree at most $2a(G) - 1$; hence $d \le 2a(G) - 1$.
- **Algorithms.** Chiba and Nishizeki use small arboricity to bound the time of listing triangles and other small subgraphs: the sum over edges $uv$ of $\min(\deg u, \deg v)$ is at most $2 a(G) m$.
- **Packing and covering.** Together with the [Nash-Williams-Tutte theorem](/nash-williams-tutte-theorem/) on [spanning tree packing](/spanning-tree-packing/), it is one of the two classical min-max theorems of matroid union on graphs.

## Tightness

**The ceiling is needed.** $K_3$ has ratio $3/2$, and two forests are needed, since one forest on three vertices has at most two edges.

**Subgraphs are needed.** The ratio of the whole graph alone is not enough. Take $K_5$ and add a long path of $t$ new vertices at one of its vertices. The whole graph has $10 + t$ edges and $4 + t$ in the denominator, a ratio that tends to 1, but the subgraph $K_5$ has ratio $\lceil 10/4 \rceil = 3$, and $a = 3$.

**Parallel edges.** Two vertices joined by $p$ parallel edges have arboricity $p$, the ratio $p/1$. So for multigraphs the arboricity can be much larger than for simple graphs with the same number of vertices.

## History

Nash-Williams published the theorem in 1964 as a one-page note, three years after the packing theorem that he and Tutte had found. Edmonds proved the general covering theorem for matroids in 1965: a matroid on $E$ can be covered by $k$ independent sets if and only if $|F| \le k\, r(F)$ for every $F \subseteq E$. Gabow and Westermann, among others, later gave efficient algorithms to compute the arboricity.

## References
