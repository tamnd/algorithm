---
tag: 96HC4H
kind: problem
slug: bipartite-graph-test
name: Two-colorability (bipartite test)
aliases:
- Two-colorability
area: graphs/coloring-and-cliques
level: intro
summary: Problem of deciding whether a graph's vertices can be colored with two colors so no edge joins same-colored vertices.
prereqs: [bipartite-graph, graph-coloring]
see_also: [bipartiteness-testing, bipartite-odd-cycle-theorem, bipartite-testing, bipartiteness-check, k-coloring, 2-sat, odd-cycle-transversal, bipartite-double-cover]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A1.1, problem GT4, Graph K-colorability (polynomial for K = 2, NP-complete for K = 3), and Appendix A3.1, problem SP4, Set splitting
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 3.4, Testing bipartiteness, an application of breadth-first search
  - paper: doi:10.1016/0022-0000(80)90060-4
    title: John M. Lewis and Mihalis Yannakakis, The node-deletion problem for hereditary properties is NP-complete, Journal of Computer and System Sciences 20(2), 219 to 230 (1980)
    locator: the main theorem (deleting the fewest vertices to reach a hereditary property, here bipartiteness, is NP-hard)
  - paper: doi:10.1145/1391289.1391291
    title: Omer Reingold, Undirected connectivity in log-space, Journal of the ACM 55(4), article 17 (2008)
    locator: the main theorem and its corollaries (problems in SL, among them bipartiteness, are in L)
---

Two-colorability asks whether the vertices of an undirected [graph](/graph/) can be colored with two colors so that each edge joins two vertices of different colors. The graphs with this property are the [bipartite graphs](/bipartite-graph/), and by the [odd cycle theorem](/bipartite-odd-cycle-theorem/) they are the graphs with no cycle of odd length. It is the case $k = 2$ of the [$k$-coloring problem](/k-coloring/), and it is the boundary of hardness: two colors take $\Theta(n + m)$ time, while three colors are NP-complete. This page places the problem in the coloring family. The search algorithm is on [bipartiteness testing](/bipartiteness-testing/), and the traversal view is on [bipartiteness checking](/bipartiteness-check/).

## In plain words

You must split a group of people into two teams, and some pairs of people refuse to be on the same team. Is there a split that works for everyone?

With two teams there is never a real choice. Once you put one person on a team, everyone who refuses that person must go to the other team, and so on. So you can just follow the forced moves and see if a conflict appears.

With three teams the moves are no longer forced, and no fast method is known. That is why two colors are easy and three colors are hard.

## Definition

**Input.** A finite undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges. Parallel edges are allowed; a self-loop makes the answer NO.

**Question.** Is there a map $c : V \to \{0, 1\}$ with $c(u) \ne c(v)$ for each edge $\{u, v\} \in E$? Equivalently: is $\chi(G) \le 2$? Is there a partition $V = A \cup B$ with no edge inside $A$ and no edge inside $B$?

**Certificates.** A YES answer has the coloring $c$ as a certificate. A NO answer has an odd cycle as a certificate. Both are checked in linear time, so the problem has short proofs both ways, without any complexity assumption.

## Variants

- **Search.** Output the 2-coloring, or an odd cycle. A [breadth-first search](/breadth-first-search/) gives both ([bipartiteness testing](/bipartiteness-testing/)).
- **Counting.** A bipartite graph with $c$ [connected components](/connected-components/) has exactly $2^c$ proper 2-colorings, because each component has two colorings, and they are chosen independently. So counting is in polynomial time, unlike counting 3-colorings.
- **Extension.** Some vertices already have a color. The forced moves still decide the problem in linear time, component by component.
- **List 2-coloring.** Each vertex has a list of at most 2 allowed colors from a larger palette. This reduces to [2-SAT](/2-sat/) and is polynomial.
- **Dynamic and streaming.** Keep the answer while edges are inserted and deleted ([dynamic bipartiteness](/dynamic-bipartiteness/)). Incremental insertions alone are handled by a [union-find with parity](/dsu-with-parity/).
- **Near-bipartite.** Delete the fewest vertices to make $G$ bipartite. This is [odd cycle transversal](/odd-cycle-transversal/), which is NP-hard (Lewis and Yannakakis 1980).
- **Hypergraphs.** Two-color the vertices of a [hypergraph](/hypergraph/) so that no edge is monochromatic. This is *set splitting*, and it is NP-complete already when each edge has 3 vertices.
- **Three colors.** The [three-coloring](/three-coloring/) problem is NP-complete.

## Examples

| graph | answer | certificate |
|---|---|---|
| empty graph ($n = 0$) | YES | the empty coloring |
| $n$ vertices, no edges | YES | all vertices color 0; there are $2^n$ colorings |
| path $0 - 1 - 2 - 3$ | YES | $c = (0, 1, 0, 1)$ |
| cycle $C_6$ | YES | $c = (0, 1, 0, 1, 0, 1)$ |
| cycle $C_5$ | NO | the cycle itself |
| $K_3$ | NO | the triangle |
| $K_{3,4}$ | YES | the two sides; exactly 2 colorings |
| a tree | YES | the parity of the depth |
| Petersen graph | NO | its outer 5-cycle |
| a vertex with a self-loop | NO | the loop, a cycle of length 1 |

**Non-example of a certificate.** For $C_6$, the map $(0, 1, 1, 0, 0, 1)$ is not a certificate: the edge $\{1, 2\}$ joins two vertices of color 1. A wrong attempt proves nothing; only a full coloring or an odd cycle settles the question.

## Known algorithms

- [Bipartiteness testing](/bipartiteness-testing/) by breadth-first search: $\Theta(n + m)$ time, $\Theta(n)$ extra space, with a 2-coloring or an odd cycle as output.
- The same with [depth-first search](/depth-first-search/): $\Theta(n + m)$ time.
- [Union-find with parity](/dsu-with-parity/): $O(m\, \alpha(n))$ time, and it works when edges arrive one at a time.
- [Greedy coloring](/greedy-coloring/) does not solve the problem: in a bad order it uses 3 or more colors on a bipartite graph. [DSATUR](/dsatur/) does: it colors each bipartite graph with at most 2 colors.

## Bounds

- **Upper bound.** $O(n + m)$ time with adjacency lists, by a graph search.
- **Lower bound, adjacency matrix.** Every correct algorithm must query $\Omega(n^2)$ entries in the worst case. Let $n \ge 4$ be even. On $K_{n/2, n/2}$ the answer is YES, and adding any one edge $\{u, v\}$ inside a side makes a triangle with any vertex of the other side. If the algorithm says YES without querying such a pair $\{u, v\}$, it gives the same answer on the graph with the edge $\{u, v\}$ added, which is wrong. So it must query all $2\binom{n/2}{2}$ pairs inside the sides. With adjacency lists, the time $\Theta(n + m)$ is linear in the size of the input.
- **Space.** The problem is in deterministic logarithmic space, by Reingold's theorem that undirected connectivity is in L.

## Reductions

- **To 2-SAT.** Take a variable $x_v$ for each vertex ("$v$ has color 1") and, for each edge $\{u, v\}$, the clauses $(x_u \lor x_v)$ and $(\lnot x_u \lor \lnot x_v)$. The formula is satisfiable exactly when $G$ is 2-colorable. It has $n$ variables and $2m$ clauses.
- **To undirected connectivity.** Build the [bipartite double cover](/bipartite-double-cover/) $G \times K_2$, with the vertices $(v, 0)$ and $(v, 1)$ and the edges $\{(u, i), (v, 1 - i)\}$. A walk from $(v, 0)$ to $(v, 1)$ is a closed walk of odd length through $v$ in $G$. So $G$ is bipartite exactly when no $(v, 0)$ is connected to $(v, 1)$.
- **From 2-colorability to $k$-colorability.** $G$ is 2-colorable exactly when $G$ joined to a $K_{k-2}$ (each new vertex adjacent to all other vertices) is $k$-colorable. So no hardness flows downward, but the problem is a special case of each $k$-coloring problem.

## Applications

- Scheduling with two time slots or two machines, when pairs of jobs conflict.
- Checking that a graph can be the input of a [bipartite matching](/bipartite-matching/) algorithm, and finding its two sides.
- Testing the consistency of "different" constraints over two values, such as the two sides of a cut or two layers of a circuit board.
- A step inside other algorithms, for example to find the two sides before the proof of [König's theorem](/konig-theorem/) or a [Hall](/hall-theorem/) type argument is applied.

## References
