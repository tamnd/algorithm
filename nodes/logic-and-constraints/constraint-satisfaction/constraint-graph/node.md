---
tag: K0EB03
kind: definition
slug: constraint-graph
name: Constraint graph
aliases:
- constraint network
- constraint hypergraph
- primal graph
- primal constraint graph
area: logic-and-constraints/constraint-satisfaction
level: intro
summary: Graph with a vertex per variable and an edge between variables that share a constraint; hyperedges for non-binary constraints.
prereqs: [constraint-satisfaction-problem, graph, hypergraph]
see_also: [dual-graph-transformation, treewidth, tree-decomposition, elimination-ordering, freuder-theorem, tree-structured-csp, cutset-conditioning, bucket-elimination]
sources:
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 2, Constraint networks (primal graph, hypergraph and dual graph), and Chapter 4, Directional consistency (width, induced width and the induced graph)
  - paper: doi:10.1145/322290.322292
    title: Eugene C. Freuder, A sufficient condition for backtrack-free search, Journal of the ACM 29(1), 1982
    locator: pages 24 to 32 (ordered constraint graphs, the width of an ordering and of a graph, and the greedy minimum width order)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, 2020
    locator: Chapter 6, Sections 6.1 and 6.5 (the constraint graph of map colouring and the structure of problems)
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 7, Tractable structures for constraint satisfaction problems, by Rina Dechter
---

The constraint graph of a [constraint satisfaction problem](/constraint-satisfaction-problem/) is the [graph](/graph/) with one vertex for each variable and an edge between two variables that occur together in some constraint. For constraints of higher arity, the constraint [hypergraph](/hypergraph/) keeps each scope as one hyperedge. The graph forgets the relations and keeps only the shape of the problem, and parameters of this shape, such as the width of an order or the [treewidth](/treewidth/), bound the cost of [tree-structured](/tree-structured-csp/), [cutset](/cutset-conditioning/) and [elimination](/bucket-elimination/) algorithms.

## Definition

Let $P = (X, D, C)$ be a CSP with variables $x_1, \ldots, x_n$ and $m$ constraints, where each constraint $(S, R)$ has a scope $S \subseteq X$ of $r$ variables.

- The **constraint hypergraph** $H(P)$ has vertex set $X$ and one hyperedge $S$ for each scope of a constraint.
- The **constraint graph**, or *primal graph*, $G(P)$ has vertex set $X$ and an edge $\{x_i, x_j\}$, $i \ne j$, whenever $x_i$ and $x_j$ lie in a common scope. Each scope of size $r$ becomes a clique on $r$ vertices.
- For a *binary* CSP, each constraint on two variables gives one edge, so the primal graph and the hypergraph agree (up to unary constraints, which add no edge). We write $e$ for the number of edges; if no two constraints have the same scope, $e$ is the number of binary constraints.
- The **dual graph** has one vertex for each constraint and an edge between two constraints whose scopes share a variable, labelled with the shared variables. It is the graph behind the [dual encoding](/dual-graph-transformation/).
- The **incidence graph** is the bipartite graph with the variables on one side, the constraints on the other, and an edge from a variable to each constraint that contains it. It is the graph of the hidden variable encoding.

**Orders, width and induced width.** An *ordered graph* is a graph with a total order $x_{\pi(1)}, \ldots, x_{\pi(n)}$ of its vertices. The *width* of a vertex is the number of its neighbours that come earlier in the order. The width of the order is the largest width of a vertex, and the width of the graph is the least width over all orders. The *induced graph* along the order is made by going through the vertices from last to first and joining all earlier neighbours of each vertex, the neighbours added before included. The *induced width* $w^\ast$ of the order is the width of its induced graph, and the induced width of the graph is the least $w^\ast$ over all orders.

Notation: $n$ variables, $m$ constraints, $e$ edges of a binary constraint graph, $d$ the largest domain size, $w$ a width and $w^\ast$ an induced width.

## Examples and non-examples

**Map colouring.** The Australia problem has the variables WA, NT, SA, Q, NSW, V and T, and the 9 edges WA-NT, WA-SA, NT-SA, NT-Q, SA-Q, SA-NSW, SA-V, Q-NSW and NSW-V. T is an isolated vertex. The graph has cycles, for example WA-NT-SA. In the order SA, WA, NT, Q, NSW, V, T the vertices have 0, 1, 2, 2, 2, 2 and 0 earlier neighbours, so the width is 2. Every pair of earlier neighbours here is already joined, so the induced graph adds no edge and the induced width is also 2. Removing SA leaves the path WA-NT-Q-NSW-V and the isolated T, which is a forest, so $\{SA\}$ is a cycle cutset of size 1.

**A ternary constraint.** The constraints $x_0 + x_1 = x_2$, $x_2 \ne x_3$ and $x_1 < x_3$ give the hypergraph with hyperedges $\{x_0, x_1, x_2\}$, $\{x_2, x_3\}$ and $\{x_1, x_3\}$. The primal graph has the triangle $x_0 x_1 x_2$ and the edges $x_2 x_3$ and $x_1 x_3$. Along the order $x_0, x_1, x_2, x_3$, the vertex $x_3$ has the earlier neighbours $x_1, x_2$, which are joined already, and $x_2$ has $x_0, x_1$. So the induced width is 2.

**Sudoku.** The binary form has 81 vertices, and each cell is joined to the 20 cells of its row, column and box, so the graph is 20-regular with 810 edges.

**A tree.** A chain $x_1 < x_2 < \cdots < x_n$ has a path as its constraint graph, of width 1 in the order $x_1, \ldots, x_n$. Any tree has width 1 in a parent-first order, because each vertex has only its parent before it.

**Non-example: the graph does not fix the answer.** The triangle on $X, Y, Z$ with domains $\{1, 2\}$ is the constraint graph of the problem with constraints $\ne$, which has no solution, and also of the problem with constraints $=$, which has two. The graph alone cannot decide a CSP. Structural results bound the cost from the graph, not the answer.

**Non-example: two constraints on one pair.** Two constraints on the same two variables give one edge of the primal graph. Results stated in $e$ assume they are intersected into one relation first.

## Related definitions

- [Constraint satisfaction problem](/constraint-satisfaction-problem/): the object whose shape this graph records.
- [Hypergraph](/hypergraph/) and [graph](/graph/): the underlying notions.
- [Treewidth](/treewidth/) and [tree decomposition](/tree-decomposition/): the induced width of a graph equals its treewidth, because an elimination order of induced width $w^\ast$ gives a tree decomposition of width $w^\ast$ and back. See [elimination ordering](/elimination-ordering/), [perfect elimination ordering](/perfect-elimination-ordering/) and [chordal graph](/chordal-graph/).
- [Degeneracy](/degeneracy/): the width of a graph in the sense above is its degeneracy. Freuder (1982) found a minimum width order by repeatedly placing a vertex of least degree last and deleting it.
- **Cycle cutset.** A set of vertices whose removal leaves a forest. A smallest one is a minimum [feedback vertex set](/feedback-vertex-set-problem/). See [cutset conditioning](/cutset-conditioning/).
- **Acyclic hypergraph.** A hypergraph with a join tree. The CSP is then solvable like an [acyclic join](/acyclic-join-evaluation/), in time polynomial in the size of the relations.
- [Dual encoding](/dual-graph-transformation/): the binary CSP whose constraint graph is the dual graph.
- [Freuder's theorem](/freuder-theorem/): strong $(w+1)$-consistency and an order of width $w$ give backtrack-free search.
- [Bucket elimination](/bucket-elimination/): its time and space are exponential in the induced width of the order it uses.

## References
