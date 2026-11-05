---
tag: 26VQS5
kind: theorem
slug: brooks-theorem
name: Brooks' theorem
aliases:
- Brooks theorem
area: graphs/coloring-and-cliques
level: core
summary: A connected graph that is neither complete nor an odd cycle can be colored with Delta colors.
prereqs: [delta-plus-one-bound, greedy-coloring, chromatic-number, biconnected-components]
see_also: [delta-plus-one-bound, chromatic-number, greedy-coloring, degeneracy, bipartite-odd-cycle-theorem, vizing-theorem, graph-coloring, list-coloring]
sources:
  - paper: doi:10.1017/S030500410002168X
    title: R. L. Brooks, On colouring the nodes of a network, Proceedings of the Cambridge Philosophical Society 37(2), 194 to 197 (1941)
    locator: the whole paper (the theorem)
  - paper: doi:10.1016/0095-8956(75)90089-1
    title: L. Lovász, Three short proofs in graph theory, Journal of Combinatorial Theory, Series B 19(3), 269 to 271 (1975)
    locator: the proof of Brooks' theorem (greedy coloring in a well-chosen order)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 5.2, Colouring vertices, Theorem 5.2.4 (Brooks 1941)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 5.1, Vertex colorings and upper bounds (Brooks' theorem with the proof of Lovász)
---

Brooks' theorem says that a connected [graph](/graph/) with maximum degree $\Delta$ can be colored with $\Delta$ colors unless it is a complete graph or an odd cycle. So the [$\Delta + 1$ bound](/delta-plus-one-bound/) of [greedy coloring](/greedy-coloring/) is reached only by these two families, and every other connected graph saves one color. The proof of Lovász (1975) shows that greedy coloring itself reaches $\Delta$ colors in a well-chosen order, and the proof gives a linear-time algorithm.

## Statement

Let $G$ be a finite simple connected undirected graph with maximum degree $\Delta$.

**Theorem (Brooks 1941).** If $G$ is neither a complete graph nor a cycle of odd length, then $\chi(G) \le \Delta$.

Equivalently, for every connected graph, $\chi(G) = \Delta + 1$ holds exactly when $G = K_{\Delta + 1}$, or $\Delta = 2$ and $G$ is an odd cycle. For a graph that is not connected, the theorem applies to each component.

## In plain words

Greedy coloring never needs more than one color above the largest number of neighbors that any point has. Brooks' theorem says that this extra color is almost never needed. Only two kinds of connected networks need it: those where every point is joined to every other point, and loops with an odd number of points.

The trick is the order. Color the points far from a chosen point first and that point last. Each point then has a neighbor still waiting, so it sees at most one fewer colored neighbor than its degree. Only the last point needs care, and the proof arranges that two of its neighbors share a color.

## Proof

This is the proof of Lovász (1975). Greedy coloring gives each vertex the smallest color not used by its colored neighbors, so a vertex with at most $\Delta - 1$ colored neighbors at its turn gets a color in $\{1, \ldots, \Delta\}$.

**Small degrees.** If $\Delta \le 1$, $G$ is $K_1$ or $K_2$, which are complete. If $\Delta = 2$, $G$ is a path or a cycle; it is not complete, so it has at least 3 vertices if it is a path, and it is an even cycle otherwise, and in both cases $\chi(G) = 2 = \Delta$. From now on $\Delta \ge 3$.

**Tool: ordering toward a root.** Let $H$ be a connected graph and $r$ a vertex of $H$. List the vertices of $H$ by non-increasing distance from $r$ in $H$, ending with $r$. Every vertex $w \ne r$ has a neighbor that comes later in the list: the next vertex on a shortest path from $w$ to $r$. So in greedy coloring along this list, $w$ has at most $\deg(w) - 1 \le \Delta - 1$ colored neighbors at its turn.

**Case 1: $G$ is not $\Delta$-regular.** Pick $r$ with $\deg(r) \le \Delta - 1$ and color greedily toward $r$. Each $w \ne r$ gets a color at most $\Delta$ by the tool, and $r$ has at most $\Delta - 1$ neighbors in all. So $\chi(G) \le \Delta$.

**Case 2: $G$ is $\Delta$-regular and has a cut vertex $x$.** Let $C_1, \ldots, C_k$ be the components of $G - x$, with $k \ge 2$, and $G_i = G[C_i \cup \{x\}]$. Each $G_i$ is connected, and $x$ has degree at most $\Delta - 1$ in $G_i$ because $x$ has neighbors in every $C_j$. By Case 1 applied with $r = x$ (every degree in $G_i$ is at most $\Delta$), each $G_i$ has a coloring with colors in $\{1, \ldots, \Delta\}$. Permute the colors in each $G_i$ so that $x$ has color 1 in all of them. The union is a proper coloring of $G$, since the $G_i$ share only $x$.

**Case 3: $G$ is $\Delta$-regular and 2-connected.** We find three vertices $x, y, z$ with $y, z \in N(x)$, $yz \notin E$, and $G - y - z$ connected. Then give $y$ and $z$ the color 1, and color greedily along the list of $G - y - z$ toward $x$. Each vertex $w \ne x$ has a later neighbor, so at most $\Delta - 1$ colored neighbors, and gets a color at most $\Delta$. The vertex $x$ comes last, with $\Delta$ neighbors, but $y$ and $z$ have the same color, so its neighbors use at most $\Delta - 1$ colors, and $x$ gets a color at most $\Delta$. The coloring is proper: $y$ and $z$ are not adjacent, and greedy coloring is proper.

*Finding $x, y, z$.* Since $G$ is connected and not complete, it has two vertices at distance 2, so some vertex has two non-adjacent neighbors.

- If $G$ is 3-connected, let $x$ be a vertex with two non-adjacent neighbors $y, z$. Removing two vertices leaves $G - y - z$ connected.
- If $G$ is 2-connected but not 3-connected, there is a vertex $x$ such that $G - x$ is connected and has a cut vertex. Then $G - x$ has at least two leaf blocks, $B_1$ and $B_2$, each with exactly one cut vertex of $G - x$. Since $G$ is 2-connected, $x$ has a neighbor in each $B_i$ that is not a cut vertex of $G - x$; otherwise that cut vertex would separate $B_i$ from the rest in $G$. Call these neighbors $y \in B_1$ and $z \in B_2$. They are not adjacent, as they lie in different blocks and are not cut vertices. $G - x - y - z$ is connected, because removing a non-cut vertex from a leaf block keeps $G - x$ connected, and this holds for both. Finally $x$ has degree $\Delta \ge 3$, so it has a neighbor other than $y$ and $z$, and $G - y - z$ is connected.

In all cases $\chi(G) \le \Delta$. $\blacksquare$

**Worked case.** Take the triangular prism: triangles $a_1 a_2 a_3$ and $b_1 b_2 b_3$ and the edges $a_i b_i$. It is 3-regular and 3-connected. Take $x = a_1$, $y = a_2$, $z = b_1$; $a_2 b_1$ is not an edge. Color $a_2$ and $b_1$ with 1. In $G - a_2 - b_1$ the distances from $a_1$ are $a_3: 1$, $b_3: 2$, $b_2: 3$, so the order is $b_2, b_3, a_3, a_1$. Greedy gives $b_2 \mapsto 2$, $b_3 \mapsto 3$, $a_3 \mapsto 2$, $a_1 \mapsto 3$: a proper coloring with $3 = \Delta$ colors.

## Consequences

- **Cubic graphs.** Every connected graph with maximum degree 3 other than $K_4$ is 3-colorable, for example the Petersen graph.
- **Linear-time $\Delta$-coloring.** Each step of the proof is a graph search or a block decomposition, so a $\Delta$-coloring of a connected graph that is neither complete nor an odd cycle is found in $O(n + m)$ time.
- **List coloring.** The theorem extends to [list coloring](/list-coloring/): a connected graph that is not a complete graph, an odd cycle, or more generally a Gallai tree (each block complete or an odd cycle) can be colored from any lists of size $\deg(v)$ (Borodin; Erdős, Rubin and Taylor).
- **Edges.** The analogue for edge coloring is different: by [Vizing's theorem](/vizing-theorem/) every graph has an edge coloring with $\Delta + 1$ colors, and the [chromatic index](/chromatic-index/) is $\Delta$ or $\Delta + 1$.

## Tightness

- **The exceptions are needed.** $K_{\Delta + 1}$ has $\chi = \Delta + 1$, and an odd cycle has $\Delta = 2$ and $\chi = 3$.
- **$\Delta$ is reached by other graphs.** $K_\Delta$ with a pendant vertex attached to one of its vertices has maximum degree $\Delta$ and $\chi = \Delta$. So the bound cannot be lowered to $\Delta - 1$ for all non-complete graphs.
- **One step further.** Borodin and Kostochka conjectured in 1977 that every graph with $\Delta \ge 9$ and no $K_\Delta$ has $\chi \le \Delta - 1$. Reed proved it for $\Delta$ at least a very large constant (1999). The condition $\Delta \ge 9$ is needed: there are graphs with $\Delta = 8$, no $K_8$, and $\chi = 8$.
- **Far from tight in general.** Like the $\Delta + 1$ bound, Brooks' bound is weak for graphs with a few high degrees; the [degeneracy](/degeneracy/) bound is often much better.

## History

R. L. Brooks published the theorem in 1941, when he was a student at Cambridge, in the same group that worked on squaring the square. Many later proofs exist. The proof of Lovász in his 1975 note "Three short proofs in graph theory" is the standard textbook proof, and it shows that the theorem is a statement about greedy coloring in a good order.

## References
