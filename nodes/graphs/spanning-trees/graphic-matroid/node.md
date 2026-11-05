---
tag: RNBCVN
kind: concept
slug: graphic-matroid
name: Graphic matroid
aliases:
- cycle matroid
area: graphs/spanning-trees
level: core
summary: The matroid whose independent sets are the edge sets of forests; its bases are spanning forests.
prereqs: [matroid, spanning-tree, simple-cycle]
see_also: [kruskal, matroid-greedy-algorithm, fundamental-cycle, arboricity, spanning-tree-packing, matroid-intersection, spanning-tree-polytope, linear-matroid]
sources:
  - book: isbn:9780199603398
    title: James Oxley, Matroid Theory, second edition, Oxford University Press (2011)
    locator: Section 1.1 (the cycle matroid of a graph) and Chapter 5, Graphic matroids
  - paper: doi:10.2307/2371182
    title: "Hassler Whitney, On the abstract properties of linear dependence, American Journal of Mathematics 57(3) (1935), 509-533"
    locator: the whole paper (matroids are defined with the forests of a graph as a model)
  - paper: doi:10.1007/BF01584082
    title: "Jack Edmonds, Matroids and the greedy algorithm, Mathematical Programming 1 (1971), 127-136"
    locator: the whole paper (the greedy algorithm is optimal on matroids, with spanning trees as the main example)
  - book: isbn:9780898711875
    title: Robert E. Tarjan, Data Structures and Network Algorithms, SIAM (1983)
    locator: Chapter 6, Minimum Spanning Trees (the remarks on matroids)
---

The graphic matroid of an undirected graph $G = (V, E)$, also called its cycle matroid $M(G)$, is the [matroid](/matroid/) on the ground set $E$ whose independent sets are the edge sets that contain no cycle, that is, the forests. Its bases are the [spanning forests](/spanning-forest/) of $G$, which are the [spanning trees](/spanning-tree/) when $G$ is connected; its circuits are the [simple cycles](/simple-cycle/); and the rank of an edge set $X$ is $n - c(X)$, where $c(X)$ is the number of components of $(V, X)$. The graphic matroid is the reason the [minimum spanning tree](/minimum-spanning-tree/) problem is solved by a greedy algorithm: [Kruskal's algorithm](/kruskal/) is the [matroid greedy algorithm](/matroid-greedy-algorithm/) on $M(G)$.

## In plain words

Think of the roads of a network as items, and call a set of roads "free" when it has no loop. Free sets behave the same way as sets of independent vectors in linear algebra. A part of a free set is free. If one free set is larger than another, some road of the larger set can be added to the smaller set and keep it free.

These two rules are what a matroid needs, so the free sets form a matroid, the graphic matroid. Its largest free sets are the trees that connect every town. The smallest sets that are not free are the loops.

Because the free sets form a matroid, the simple greedy rule works: take the roads from the cheapest up, and keep each road that does not close a loop.

## The idea

Let $G = (V, E)$ be a finite undirected graph with $n$ vertices. Parallel edges and self-loops are allowed, and $G$ need not be connected. For $X \subseteq E$, let $c(X)$ be the number of components of the graph $(V, X)$; an isolated vertex counts as one component. Write $c(G) = c(E)$.

**Definition.** The graphic matroid is $M(G) = (E, \mathcal{I})$ with

$$\mathcal{I} = \{ F \subseteq E : F \text{ contains no cycle} \}.$$

A self-loop is a cycle with one edge, so it is in no independent set: it is a *loop* of the matroid. Two parallel edges form a cycle with two edges, so they are *parallel elements* of the matroid.

**It is a matroid.** The empty set has no cycle, and a subset of a forest is a forest. For the exchange axiom, a forest $F$ on $n$ vertices has $c(F) = n - |F|$ components, because each tree with $k$ vertices has $k - 1$ edges. Let $A, B$ be forests with $|A| < |B|$. If each edge of $B$ had both ends in one tree of $A$, each component of $(V, B)$ would lie inside a component of $(V, A)$, so $c(B) \ge c(A)$, that is $n - |B| \ge n - |A|$, a contradiction. So some edge $e \in B$ joins two different trees of $A$, and $A \cup \{e\}$ is a forest.

**The parts of the matroid in graph terms.**

| matroid notion | in $M(G)$ |
|---|---|
| independent set | forest |
| basis | spanning forest; spanning tree if $G$ is connected |
| circuit | simple cycle (a self-loop, two parallel edges, or a longer cycle) |
| rank $r(X)$ | $n - c(X)$ |
| rank of $M(G)$ | $n - c(G)$; $n - 1$ if $G$ is connected |
| closure of $X$ | $X$ and each edge whose ends are joined by a path in $X$ |
| fundamental circuit of $e$ for a basis $T$ | the [fundamental cycle](/fundamental-cycle/) $C_T(e)$ |
| cocircuit | a minimal [cut](/cut/), also called a bond |

The rank formula holds because a spanning forest of $(V, X)$ has $n - c(X)$ edges, and each maximal forest inside $X$ is a spanning forest of $(V, X)$.

**Representation over a field.** Orient each edge $(u, v)$ in any way, and let its column in a $|V| \times |E|$ matrix have $+1$ in row $u$, $-1$ in row $v$ and $0$ elsewhere; a self-loop gets the zero column. A set of edges is a forest if and only if its columns are linearly independent, over each field. So $M(G)$ is a [linear matroid](/linear-matroid/). Over $\mathbb{F}_2$, the signs do not matter and the matrix is the unsigned [incidence matrix](/incidence-matrix/). The proof over $\mathbb{F}_2$: the columns of a cycle sum to zero, since each vertex of the cycle meets two of its edges. Conversely, if a nonempty set of columns sums to zero, each vertex has even degree in that edge set, and a nonempty edge set with all degrees even contains a cycle, since a forest with an edge has a leaf.

**Greedy.** For a weight on the elements, the greedy algorithm that scans them in non-decreasing order and keeps each one that leaves the set independent finds a minimum weight basis of each matroid (Edmonds, 1971). On $M(G)$, "independent" means "no cycle", the test is a [disjoint-set](/disjoint-set/) query, and the algorithm is Kruskal's. Conversely, a family of sets closed under subsets on which greedy is optimal for every weight is a matroid, see the [matroid greedy theorem](/matroid-greedy-theorem/).

## Examples

**A triangle.** For the triangle on $a, b, c$, each pair of edges is a forest and the whole set is a cycle. So $M(G)$ has rank 2, three bases and one circuit: it is the [uniform matroid](/uniform-matroid/) $U_{2,3}$.

**A graph with six vertices.** Take the vertices $a$ to $f$ and the edges $ab$, $ac$, $bc$, $bd$, $cd$, $ce$, $de$, $df$, $ef$. The graph is connected, so $M(G)$ has rank $6 - 1 = 5$, and its 55 bases are the 55 spanning trees. For the basis $T = \{bc, bd, ef, ac, ce\}$, the fundamental circuit of $de$ is $\{de, ec, cb, bd\}$. The set $X = \{ab, bc, ca, ef\}$ has rank $6 - 3 = 3$, since $(V, X)$ has the three components $\{a, b, c\}$, $\{d\}$ and $\{e, f\}$; its closure is $X$ itself, since no other edge has both ends in one component.

**A complete graph.** For $K_4$, the matroid has 6 elements and rank 3. Its bases are the 16 spanning trees of $K_4$, by [Cayley's formula](/cayley-formula/), and its circuits are the four triangles and the three 4-cycles.

**A non-example.** The uniform matroid $U_{2,4}$, with four elements in which each two are independent and each three are dependent, is not graphic. If it were $M(G)$, no element would be a self-loop and no two would be parallel, since all pairs are independent. Each three edges would contain a cycle, which must then be a triangle. If $\{e_1, e_2, e_3\}$ and $\{e_1, e_2, e_4\}$ are both triangles, then $e_3$ and $e_4$ both join the free ends of the path $e_1 e_2$, so they are parallel, a contradiction.

## Where it is used

- **Minimum spanning trees.** Kruskal's algorithm is greedy on $M(G)$, and the [cut property](/cut-property/) and the [cycle property](/cycle-property/) are the cocircuit and circuit forms of the matroid exchange. The [greedy MST algorithm](/greedy-mst-algorithm/) of Tarjan is the same pair of steps.
- **Arboricity and tree packing.** The union of $k$ copies of $M(G)$ is a matroid, and its rank formula gives the Nash-Williams theorems on [arboricity](/arboricity/) and on [spanning tree packing](/spanning-tree-packing/).
- **Matroid intersection.** A branching of a directed graph is a set of arcs that is a forest in the underlying undirected graph and has in-degree at most 1 at each vertex, so branchings are the common independent sets of $M(G)$ and a [partition matroid](/partition-matroid/). [Matroid intersection](/matroid-intersection/) then solves weighted branching problems, and also spanning trees with colour constraints.
- **Polyhedra.** The convex hull of the spanning trees is the [spanning tree polytope](/spanning-tree-polytope/), the base polytope of $M(G)$.
- **Exchange walks.** Each two bases of a matroid are joined by a sequence of single exchanges, so each two spanning trees are joined by moves $T - f + e$. This is the basis of [spanning tree enumeration](/spanning-tree-enumeration/) and of the [second-best MST](/second-best-mst/).

## References
