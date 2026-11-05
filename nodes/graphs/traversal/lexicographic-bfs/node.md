---
tag: SYYZ0S
kind: algorithm
slug: lexicographic-bfs
name: Lexicographic breadth-first search
aliases:
- LexBFS
area: graphs/traversal
level: advanced
summary: A BFS variant that orders vertices by lexicographic labels, used in chordal graph recognition.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [breadth-first-search, chordal-graph, perfect-elimination-ordering, partition-refinement]
see_also: [maximum-cardinality-search, chordal-graph-coloring, maximal-clique, treewidth, elimination-ordering, bfs-layers, bipartite-graph-recognition, certifying-algorithms]
sources:
  - paper: doi:10.1137/0205021
    title: Donald J. Rose, R. Endre Tarjan and George S. Lueker, Algorithmic aspects of vertex elimination on graphs, SIAM Journal on Computing 5(2), 266 to 283 (1976)
    locator: the algorithm LEX P with lexicographic labels, its linear-time implementation by a list of label classes, and the theorem that it yields a perfect elimination ordering exactly for chordal graphs
  - book: isbn:9780444515308
    title: Martin Charles Golumbic, Algorithmic Graph Theory and Perfect Graphs, second edition
    locator: Chapter 4, Triangulated graphs (perfect elimination orderings, and their recognition by lexicographic breadth-first search)
  - paper: doi:10.1016/s0304-3975(97)00241-7
    title: Michel Habib, Ross McConnell, Christophe Paul and Laurent Viennot, Lex-BFS and partition refinement, with applications to transitive orientation, interval graph recognition and consecutive ones testing, Theoretical Computer Science 234(1-2), 59 to 84 (2000)
    locator: the description of LexBFS as partition refinement, and its applications
  - paper: doi:10.1007/978-3-540-30559-0_1
    title: Derek G. Corneil, Lexicographic breadth first search, a survey, Graph-Theoretic Concepts in Computer Science (WG 2004), Lecture Notes in Computer Science 3353, 1 to 19
    locator: the definition by labels, the four-point property of LexBFS orderings, and the multi-sweep algorithms
---

Lexicographic breadth-first search (LexBFS) is a [breadth-first search](/breadth-first-search/) with a special rule for ties: among the vertices that may come next, it takes one whose set of already visited neighbours is largest in a lexicographic sense, where a neighbour visited earlier counts more than all neighbours visited later. Rose, Tarjan and Lueker introduced it in 1976 to recognize [chordal graphs](/chordal-graph/): a graph is chordal if and only if the reverse of a LexBFS order is a [perfect elimination ordering](/perfect-elimination-ordering/), and this can be checked in linear time. With [partition refinement](/partition-refinement/), LexBFS runs in $\Theta(n + m)$ time. Repeated LexBFS sweeps, each one breaking ties by the previous order, also recognize interval graphs, unit interval graphs and cographs, and find good vertices for the diameter.

## In plain words

Plain breadth-first search visits the neighbours of the start, then their neighbours, and so on, but it does not care in which order it takes vertices that are equally far away. LexBFS makes that choice in a fixed way.

Give each waiting vertex a list of the visited vertices it is joined to. Compare two lists like words in a dictionary, where the first visited vertex is the first letter. Always visit next a waiting vertex with the "largest" list. A vertex joined to the first visited vertex beats every vertex that is not, and among those, a vertex joined to the second one wins, and so on.

On a graph with no long cycle without a shortcut, this order has a strong property: when read backwards, each vertex is joined to a group of earlier vertices that are all joined to each other.

## The problem

The input is a simple undirected graph $G = (V, E)$ given by adjacency lists, and a start vertex. The output is an order $\sigma = (v_1, \ldots, v_n)$ of $V$ that obeys the LexBFS rule below. The main use is the recognition problem for [chordal graphs](/chordal-graph/): decide whether every cycle of length at least 4 has a chord, and if so give a [perfect elimination ordering](/perfect-elimination-ordering/).

**Labels.** Before step $i$, the vertices $v_1, \ldots, v_{i-1}$ are visited. The *label* of an unvisited vertex $x$ is the set $\ell(x) = N(x) \cap \{v_1, \ldots, v_{i-1}\}$. For two labels $A \ne B$, write $A \succ B$ if the first visited vertex of the symmetric difference $A \triangle B$ lies in $A$. This is the lexicographic order of the labels written as words of visit positions, with a missing letter counting as less. Rose, Tarjan and Lueker give vertex $v_j$ the number $n + 1 - j$ and append numbers to labels, which gives the same order.

**LexBFS rule.** At each step $i$, the vertex $v_i$ has a label that is largest, under $\succ$, among the unvisited vertices. The first vertex is the start vertex, and ties may be broken in any way.

## The algorithm

The algorithm keeps the unvisited vertices in an ordered list of classes. Two vertices are in the same class exactly when they have the same label, and the classes are sorted by decreasing label.

```pseudo id=main
LEXBFS(G, s)
L1  L ← a list with one class that holds all of V, with s first
L2  for i ← 1 to n do
L3      C ← the first class of L, v ← a vertex of C (the first one), remove v from C
L4      σ[i] ← v
L5      for each neighbour w of v that is not visited do
L6          let D be the class of w
L7          if D has not been split at step i then insert a new empty class D′ just before D in L
L8          move w from D to D′, and delete D from L if it is now empty
L9  return σ
```

A class that becomes empty at line L3 is deleted as well. Line L7 creates at most one new class $D'$ per class $D$ and per step, and the vertices of $D'$ are those of $D$ that are adjacent to $v$.

**Chordal graph recognition.** Run LEXBFS. Then the graph is chordal if and only if, for each vertex $x$, the neighbours of $x$ visited before $x$ form a clique. Rose, Tarjan and Lueker check this in linear time: for each $x$, let $p(x)$ be the latest visited of these earlier neighbours, and test that all other earlier neighbours of $x$ are neighbours of $p(x)$.

## Example

Take the chordal graph with vertices 0 to 6 and the edges $\{0,3\}$, $\{1,2\}$, $\{1,3\}$, $\{1,6\}$, $\{2,6\}$, $\{3,4\}$, $\{3,6\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$, with sorted lists, and start at 0.

| step | classes before the step (first class first) | visit | labels of the waiting vertices after the visit |
|---|---|---|---|
| 1 | $\{0, 1, 2, 3, 4, 5, 6\}$ | 0 | $3: \{0\}$; others: $\emptyset$ |
| 2 | $\{3\}, \{1, 2, 4, 5, 6\}$ | 3 | $1, 4, 6: \{3\}$; $2, 5: \emptyset$ |
| 3 | $\{1, 4, 6\}, \{2, 5\}$ | 1 | $6: \{3, 1\}$; $4: \{3\}$; $2: \{1\}$; $5: \emptyset$ |
| 4 | $\{6\}, \{4\}, \{2\}, \{5\}$ | 6 | |
| 5 | $\{4\}, \{2\}, \{5\}$ | 4 | |
| 6 | $\{2\}, \{5\}$ | 2 | |
| 7 | $\{5\}$ | 5 | |

The LexBFS order is $0, 3, 1, 6, 4, 2, 5$. At step 4, vertex 6 wins over 4 because both are joined to 3, and 6 is also joined to 1. Vertex 4 wins over 2 because 4 is joined to 3, which was visited before 1.

The earlier neighbours of each vertex are: $3: \{0\}$; $1: \{3\}$; $6: \{3, 1\}$; $4: \{3, 6\}$; $2: \{1, 6\}$; $5: \{6, 4\}$. Each pair is an edge, so the reverse order $5, 2, 4, 6, 1, 3, 0$ is a perfect elimination ordering, and the graph is chordal.

**Plain BFS is not enough.** A BFS with sorted lists visits $0, 3, 1, 4, 6, 2, 5$. Then the earlier neighbours of 6 are 3, 1 and 4, and 1 and 4 are not adjacent, so the reverse of this BFS order is not a perfect elimination ordering, although the graph is chordal.

**A graph that is not chordal.** On the 4-cycle $0, 1, 2, 3$, LexBFS from 0 visits $0, 1, 3, 2$. The earlier neighbours of 2 are 1 and 3, which are not adjacent, so the test reports that the graph is not chordal.

## Correctness

The classes always group the unvisited vertices by label and are sorted by decreasing label: when $v$ is visited, the label of each unvisited neighbour gains $v$, which is later than every vertex already in a label, so it moves above the vertices of its old class and stays below every higher class. So the first class holds the vertices with the largest label, and the order obeys the LexBFS rule. For the chordal test, the key fact is that a LexBFS order has the *four-point property*: if $a$, $b$, $c$ are visited in this order, $ac \in E$ and $ab \notin E$, then some $d$ visited before $a$ has $db \in E$ and $dc \notin E$. In a chordal graph this forbids two non-adjacent earlier neighbours of a vertex, because they would lead to a chordless cycle. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model. The classes are a doubly linked list, each class is a doubly linked list of vertices, and each vertex points to its class, so lines L3, L6, L7 and L8 take $O(1)$ time each. A class records the last step at which it was split, together with its new class.

- **Line L3.** One time per vertex: $\Theta(n)$.
- **Lines L5 to L8.** One time per list entry of a visited vertex: $\Theta(m)$ in total, counting both ends of each edge.

So the time is $\Theta(n + m)$, and the extra space is $\Theta(n)$ for the classes and the pointers. The chordal test adds $O(n + m)$: it groups the tests "$y$ is a neighbour of $p(x)$" by $p(x)$ and does all tests for one vertex with one marking pass over its list.

## Properties

- **It is a BFS.** A LexBFS order is a breadth-first order: a vertex joined to an earlier visited vertex always beats one that is not, so the vertices are visited by increasing distance from the start.
- **Four-point property.** If $a <_\sigma b <_\sigma c$, $ac \in E$ and $ab \notin E$, then there is $d <_\sigma a$ with $db \in E$ and $dc \notin E$.
- **Prefix property.** For each $i$, the order $v_1, \ldots, v_i$ is a LexBFS order of the induced subgraph on $\{v_1, \ldots, v_i\}$.
- **Chordal graphs.** $G$ is chordal if and only if the reverse of one, or every, LexBFS order is a perfect elimination ordering. In particular, the last vertex of a LexBFS of a chordal graph is simplicial.
- **Deterministic** once the tie-breaking rule is fixed, as in line L3.

## Variants and improvements

- **Label version.** Rose, Tarjan and Lueker keep the labels as strings of numbers and sort them in buckets. The partition refinement form of Habib, McConnell, Paul and Viennot is simpler to program and has the same bound.
- **Multi-sweep LexBFS.** LexBFS$^+$ runs a new LexBFS and breaks each tie by taking the vertex that came last in the previous order. A fixed number of such sweeps recognizes unit interval graphs (three sweeps, Corneil) and interval graphs (six sweeps, Corneil, Olariu and Stewart).
- **Maximum cardinality search.** [Maximum cardinality search](/maximum-cardinality-search/) replaces the label set by its size. It is simpler and also gives a perfect elimination ordering on chordal graphs, but it is not a BFS.
- **Lexicographic DFS.** The same idea with the most recently visited neighbour counting most gives LexDFS, which is used for cocomparability graphs.
- **Uses of the order.** On a chordal graph, the perfect elimination ordering gives in linear time a maximum clique, an optimal [colouring](/chordal-graph-coloring/), all [maximal cliques](/maximal-clique/) and a clique tree, which is a tree decomposition of width one less than the clique number.

## When to use it

Use LexBFS to test whether a graph is chordal and to get a perfect elimination ordering, for example before sparse [Gaussian elimination](/gaussian-elimination/) without fill-in, or before the clique algorithms for chordal graphs. Use multi-sweep LexBFS for the recognition of interval and unit interval graphs and for a good estimate of the diameter of special graph classes. For distances alone, plain [breadth-first search](/breadth-first-search/) is enough. For chordality alone, [maximum cardinality search](/maximum-cardinality-search/) is a little simpler to code.

## Pitfalls

- **Breaking ties as in plain BFS.** Any BFS order is not enough, as the example shows. The ties must follow the labels.
- **Comparing labels by size.** Comparing $|\ell(x)|$ instead of $\ell(x)$ gives maximum cardinality search, a different order. It also works for chordality, but not for the multi-sweep algorithms that rely on LexBFS.
- **Placing the new class after the old one.** The vertices adjacent to $v$ must go before the rest of their class. Placing them after reverses the comparison.
- **Splitting a class twice in one step.** A class must get at most one new class per step, or vertices with equal labels end up in different classes.
- **Reading the order the wrong way.** The perfect elimination ordering is the *reverse* of the LexBFS order: the last visited vertex is eliminated first.

## Implementations

## History

Donald Rose, Robert Tarjan and George Lueker introduced lexicographic breadth-first search in 1976, in a paper on vertex elimination for sparse systems of equations, as a linear-time way to find a perfect elimination ordering of a chordal graph or to decide that none exists. Golumbic's book made it a standard tool of algorithmic graph theory. Habib, McConnell, Paul and Viennot described it in 2000 as partition refinement and used it for transitive orientation and interval graph recognition. Corneil and coauthors developed multi-sweep LexBFS algorithms, and Corneil surveyed the method in 2004.

## References
