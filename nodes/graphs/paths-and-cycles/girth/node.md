---
tag: W2PBPB
kind: definition
slug: girth
name: Girth
area: graphs/paths-and-cycles
level: core
summary: The length of a shortest cycle in a graph, or infinity if the graph has no cycle. Defined for undirected and directed graphs and multigraphs.
prereqs: [simple-cycle, graph]
see_also: [shortest-cycle-problem, itai-rodeh-girth-algorithm, bipartite-graph, planar-graph, chromatic-number, cycle-detection-in-graph, breadth-first-search, probabilistic-method]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 1.3, Paths and cycles (the definition of girth, the bound of girth by twice the diameter plus one, and the bounds that relate girth, minimum degree and order)
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer (2008)
    locator: Section 2.2, Paths and cycles (girth and circumference)
  - paper: doi:10.1137/0207033
    title: Alon Itai and Michael Rodeh, Finding a minimum circuit in a graph, SIAM Journal on Computing 7(4), 413 to 423 (1978)
    locator: the whole paper (computing the girth in O(nm) time, and faster methods based on matrix multiplication)
  - paper: doi:10.4153/CJM-1959-003-9
    title: Paul Erdős, Graph theory and probability, Canadian Journal of Mathematics 11, 34 to 38 (1959)
    locator: the whole paper (graphs with large girth and large chromatic number)
---

The girth $g(G)$ of a [graph](/graph/) $G$ is the length of a shortest [cycle](/simple-cycle/) in $G$, and $g(G) = \infty$ if $G$ has no cycle. Large girth means that the graph looks like a tree around each vertex, up to distance about $g/2$. The girth of an undirected graph is computed by [breadth-first search](/breadth-first-search/) from every vertex in $O(nm)$ time; see the [shortest cycle problem](/shortest-cycle-problem/).

## Definition

Let $G$ be an undirected graph. A cycle of length $k$ is a closed walk $v_0, e_1, v_1, \ldots, e_k, v_k = v_0$ with $k \ge 1$, distinct edges and distinct vertices $v_0, \ldots, v_{k-1}$. The **girth** of $G$ is

$$g(G) = \min \{ k : G \text{ has a cycle of length } k \},$$

with $g(G) = \infty$ when the set is empty, that is when $G$ is a forest.

- **Simple graphs.** A cycle has at least 3 vertices, so $g(G) \ge 3$.
- **Multigraphs.** A [self-loop](/self-loop/) is a cycle of length 1, and two parallel edges form a cycle of length 2. So $g(G) = 1$ if $G$ has a loop, and otherwise $g(G) = 2$ if $G$ has parallel edges. Many books define girth only for simple graphs; with this convention the definition extends without change.
- **Directed graphs.** The *directed girth* of a directed graph $D$ is the length of a shortest directed cycle. Here $u \to v \to u$ is a cycle of length 2 even without parallel arcs, and a loop has length 1. A directed graph has finite directed girth if and only if it is not acyclic. The directed girth of $D$ can be larger than the girth of its underlying undirected graph: a transitive tournament (a complete graph with each edge directed from the smaller to the larger vertex) has directed girth $\infty$ but its underlying graph is complete.

Isolated vertices and connected components without cycles do not change the girth, and the girth of a graph is the least girth of its components.

## Examples and non-examples

| graph | girth | why |
|---|---|---|
| a tree or forest | $\infty$ | no cycle |
| the cycle $C_n$, $n \ge 3$ | $n$ | its only cycle |
| the complete graph $K_n$, $n \ge 3$ | 3 | any three vertices form a triangle |
| the complete bipartite graph $K_{a, b}$, $a, b \ge 2$ | 4 | bipartite, so no triangle, and $a_1 b_1 a_2 b_2$ is a 4-cycle |
| the hypercube $Q_d$, $d \ge 2$ | 4 | bipartite, and two coordinates give a 4-cycle |
| the Petersen graph | 5 | no triangle and no 4-cycle; the outer 5-cycle |
| the Heawood graph | 6 | the incidence graph of the Fano plane: two points lie on one common line, so no 4-cycle |
| a vertex with a loop | 1 | the loop |
| two vertices joined by two edges | 2 | the two parallel edges |

**Petersen.** Two adjacent vertices of the Petersen graph have no common neighbour, and two non-adjacent vertices have exactly one, so there is no 3-cycle and no 4-cycle, and the outer 5-cycle shows $g = 5$. The diameter is 2, so the bound $g \le 2\,\mathrm{diam}(G) + 1$ below holds with equality.

**Directed example.** The arcs $0 \to 1$, $1 \to 2$ and $0 \to 2$, together with the directed 4-cycle $3 \to 4 \to 5 \to 6 \to 3$. The underlying undirected graph has the triangle $0, 1, 2$, so its girth is 3. The directed girth is 4, because the triangle is not a directed cycle. Adding the arc $2 \to 0$ makes the directed girth 2, through the directed cycle $0 \to 2 \to 0$.

**Non-example.** The length of a *longest* cycle is the circumference, not the girth. The Petersen graph has girth 5 and circumference 9, since it has a cycle through 9 of its vertices but is not Hamiltonian.

## Related definitions

- **Odd girth and even girth.** The length of a shortest odd cycle, and of a shortest even cycle. A graph is [bipartite](/bipartite-graph/) if and only if its odd girth is $\infty$.
- **Girth and diameter.** If $G$ is connected and has a cycle, then $g(G) \le 2\,\mathrm{diam}(G) + 1$ (Diestel, Section 1.3). Proof idea: take a shortest cycle $C$; if $g(C) \ge 2\,\mathrm{diam}(G) + 2$, two vertices of $C$ at distance $\mathrm{diam}(G) + 1$ on $C$ have a shorter path in $G$, and this path with the shorter arc of $C$ contains a cycle shorter than $C$. Odd cycles $C_{2k+1}$ and the Petersen graph show that the bound is tight.
- **Girth and degree (the Moore bound).** If every vertex has degree at least $d \ge 2$ and $g(G) \ge 2k + 1$, then the vertices at distance less than $k$ from a fixed vertex induce a tree, so $n \ge 1 + d \sum_{i=0}^{k-1} (d - 1)^i$. In particular, a graph with minimum degree at least 3 has girth $O(\log n)$. A $d$-regular graph of girth $g$ with the least number of vertices is a *cage*; the Petersen graph is the $(3, 5)$-cage and the Heawood graph is the $(3, 6)$-cage.
- **Girth and planarity.** A connected [planar graph](/planar-graph/) with $n \ge 3$ vertices and finite girth $g \ge 3$ has at most $g(n - 2)/(g - 2)$ edges, because each face has at least $g$ edges on its boundary. With $g = 3$ this gives $m \le 3n - 6$, and with $g = 4$, for triangle-free planar graphs, $m \le 2n - 4$. The Petersen graph has $n = 10$, $m = 15$ and $g = 5$, and $15 > 5 \cdot 8 / 3$, so it is not planar.
- **Girth and colouring.** Erdős proved in 1959, with the [probabilistic method](/probabilistic-method/), that for all $g$ and $k$ there are graphs with girth greater than $g$ and [chromatic number](/chromatic-number/) greater than $k$. So large girth, a local property, does not limit the chromatic number, a global property.
- **Computing the girth.** Breadth-first search from $s$ reports, for each non-tree edge $uv$, the closed walk of length $d(s, u) + d(s, v) + 1$, which contains a cycle no longer than it. When $s$ lies on a shortest cycle, one of these walks has length exactly $g(G)$, so the minimum over all $s$ is the girth. This takes $O(nm)$ time. See the [Itai-Rodeh algorithm](/itai-rodeh-girth-algorithm/) for this and faster methods, and the [shortest cycle problem](/shortest-cycle-problem/) for directed and weighted versions. Finding any cycle, not a shortest one, is [cycle detection](/cycle-detection-in-graph/).

## References
