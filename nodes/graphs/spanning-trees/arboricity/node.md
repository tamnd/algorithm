---
tag: CCCXPE
kind: concept
slug: arboricity
name: Arboricity
aliases:
- graph arboricity
area: graphs/spanning-trees
level: advanced
summary: The minimum number of forests needed to cover all edges of a graph.
prereqs: [graphic-matroid, spanning-forest, tree-edge-count]
see_also: [nash-williams-arboricity-theorem, spanning-tree-packing, degeneracy, triangle-counting, planar-graph, matroid, nash-williams-tutte-theorem, graphic-matroid]
sources:
  - paper: doi:10.1112/jlms/s1-39.1.12
    title: "C. St. J. A. Nash-Williams, Decomposition of finite graphs into forests, Journal of the London Mathematical Society 39 (1964), 12"
    locator: the whole paper (the formula for the arboricity)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer Graduate Texts in Mathematics 173 (2017)
    locator: Chapter 2, Section 2.4, Tree-packing and arboricity
  - paper: doi:10.1137/0214017
    title: "Norishige Chiba and Takao Nishizeki, Arboricity and subgraph listing algorithms, SIAM Journal on Computing 14(1) (1985), 210-223"
    locator: the whole paper (triangle and clique listing in time proportional to the arboricity times m)
---

The arboricity $a(G)$ of an undirected graph $G$ is the least number of forests whose union is the edge set of $G$. A forest on $n_H$ vertices has at most $n_H - 1$ edges, so a subgraph $H$ with $m_H$ edges needs at least $\lceil m_H / (n_H - 1) \rceil$ forests, and the Nash-Williams theorem says that the densest subgraph decides it:

$$a(G) = \max_{H \subseteq G,\ n_H \ge 2} \left\lceil \frac{m_H}{n_H - 1} \right\rceil.$$

Arboricity is a measure of how sparse a graph is everywhere, not only on average. It is within a factor 2 of the [degeneracy](/degeneracy/), it is at most 3 for [planar graphs](/planar-graph/), and it bounds the running time of many algorithms on sparse graphs, such as triangle listing in $O(m \, a(G))$ time.

## In plain words

Take a network and try to split its links into groups, so that no group has a loop. The arboricity is the smallest number of groups that works.

A part of the network with many links and few points needs many groups, because a group without loops can only hold one link fewer than the number of points it touches. The main theorem says that this is the only reason: the densest part of the network decides how many groups are needed.

A small arboricity means that every part of the network is sparse. Many algorithms run fast on such networks.

## The idea

Let $G = (V, E)$ be a finite undirected graph. Self-loops are in no forest, so the arboricity is defined for graphs without self-loops; parallel edges are allowed. A graph with no edges has arboricity 0.

**Definition.** $a(G)$ is the least $k$ such that $E = F_1 \cup \dots \cup F_k$ with each $F_i$ a forest. The forests can be taken disjoint, since a subset of a forest is a forest. In terms of the [graphic matroid](/graphic-matroid/) $M(G)$, $a(G)$ is the least number of independent sets that cover the ground set.

**The lower bound.** If $E$ is covered by $k$ forests, then each subgraph $H$ with $n_H$ vertices and $m_H$ edges is covered by their restrictions to $H$, each of which is a forest on $n_H$ vertices with at most $n_H - 1$ edges. So $m_H \le k (n_H - 1)$, and

$$a(G) \ge \max_{H,\ n_H \ge 2} \left\lceil \frac{m_H}{n_H - 1} \right\rceil.$$

The maximum may be taken over induced subgraphs, since adding the edges between the vertices of $H$ only raises $m_H$.

**The Nash-Williams theorem (1964).** The lower bound is exact. One proof uses Edmonds' matroid partition theorem: the ground set of a matroid with rank function $r$ can be covered by $k$ independent sets if and only if $|X| \le k \, r(X)$ for each subset $X$. For $M(G)$, $r(X) = n_X - c_X$, where $n_X$ and $c_X$ count the vertices touched by $X$ and the components of $(V(X), X)$; applied to each component of $X$, the condition becomes the condition $m_H \le k (n_H - 1)$ on connected subgraphs. The full statement and its proof are on the page of the [Nash-Williams arboricity theorem](/nash-williams-arboricity-theorem/). The related theorem of Nash-Williams and Tutte on [spanning tree packing](/spanning-tree-packing/) counts disjoint spanning trees instead; see the [Nash-Williams-Tutte theorem](/nash-williams-tutte-theorem/).

**Fractional arboricity.** The value $\max_H m_H / (n_H - 1)$, without the ceiling, is the *fractional arboricity*. It is the least total weight of forests, with real weights, that covers each edge at least once.

**Degeneracy.** The degeneracy $d(G)$ is the largest minimum degree over all subgraphs. Then

$$a(G) \le d(G) \le 2 a(G) - 1 \quad \text{when } G \text{ has an edge}.$$

*Proof.* Order the vertices by removing, again and again, a vertex of least degree in what remains. Each vertex has at most $d(G)$ edges to vertices that come later. Number these edges $1, 2, \dots$ at each vertex, and let $F_i$ be the set of edges with number $i$. In $F_i$, each vertex has at most one edge to a later vertex, so following these edges strictly increases the position, and $F_i$ has no cycle. So $a(G) \le d(G)$. Conversely, each subgraph $H$ with $n_H \ge 2$ has $m_H \le a(G)(n_H - 1)$ edges, so its average degree is less than $2 a(G)$, and it has a vertex of degree at most $2 a(G) - 1$. $\square$

**Orientations.** If $E$ is covered by $k$ forests, root each tree of each forest and direct each edge toward the root. Each vertex then has out-degree at most 1 in each forest, so at most $k$ in total. An orientation with all out-degrees at most $k$ lets an algorithm store, at each vertex, only its out-neighbors, and still find each edge.

**Computing it.** The arboricity, and a cover by $a(G)$ forests, can be computed in polynomial time by matroid partitioning, an augmenting path method on the forests. The degeneracy order gives a cover by at most $2 a(G) - 1$ forests in $O(n + m)$ time, which is enough for most algorithmic uses.

## Examples

| graph | $a(G)$ | densest part |
|---|---|---|
| a forest with an edge | 1 | each tree: $m_H = n_H - 1$ |
| a cycle $C_n$ | 2 | the cycle: $\lceil n / (n - 1) \rceil = 2$ |
| $K_n$, $n \ge 2$ | $\lceil n / 2 \rceil$ | the whole graph: $\binom{n}{2} / (n - 1) = n / 2$ |
| $K_{3,3}$ | 2 | the whole graph: $\lceil 9 / 5 \rceil$ |
| a planar graph | at most 3 | each planar $H$ with $n_H \ge 3$ has $m_H \le 3 n_H - 6 < 3 (n_H - 1)$ |
| two vertices with $k$ parallel edges | $k$ | the whole graph: $k / 1$ |

**A graph with six vertices.** Take the vertices $a$ to $f$ and the edges $ab$, $ac$, $bc$, $bd$, $cd$, $ce$, $de$, $df$, $ef$. The whole graph gives $\lceil 9/5 \rceil = 2$, and so does its densest part $\{a, b, c, d\}$ with 5 edges: $\lceil 5/3 \rceil = 2$. Two forests suffice: the spanning tree $\{bc, bd, ef, ac, ce\}$ and the rest, $\{ab, cd, de, df\}$, which has no cycle. So $a(G) = 2$.

**The complete graph $K_4$.** It has 6 edges on 4 vertices, so it needs $\lceil 6/3 \rceil = 2$ forests, and the two paths $1, 2, 3, 4$ and $3, 1, 4, 2$ cover it with no common edge.

## Where it is used

- **Triangle and clique listing.** Chiba and Nishizeki (1985) list all triangles of a graph in $O(m \, a(G))$ time, and all cliques of a fixed size $k$ in $O(k \, m \, a(G)^{k-2})$ time. Since $a(G) \le \lceil \sqrt{2m} \rceil$ for every graph, this gives $O(m^{3/2})$ for triangles; see [triangle counting](/triangle-counting/).
- **Sparse graph data structures.** The orientation with out-degree at most $a(G)$, or the degeneracy orientation with out-degree at most $2a(G) - 1$, answers adjacency queries in $O(a(G))$ time with $O(n + m)$ space.
- **Planar graphs.** Planar graphs have arboricity at most 3 and degeneracy at most 5, which gives linear-time algorithms for many problems on them.
- **Tree packing and network strength.** Arboricity is the covering counterpart of [spanning tree packing](/spanning-tree-packing/): one asks how few forests cover the edges, the other how many disjoint spanning trees fit inside. Both come from the matroid union theorem on the graphic matroid.
- **Distributed and parallel algorithms.** Forest decompositions are used to color and to find independent sets in graphs of small arboricity, with the number of colors bounded in terms of $a(G)$.

## References
