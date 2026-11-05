---
tag: SQQF87
kind: definition
slug: graph-traversal
name: Graph traversal
aliases:
- graph search
- graph exploration
area: graphs/traversal
level: intro
summary: Systematically visiting every vertex reachable from a start vertex, each exactly once.
prereqs: [graph, walk]
see_also: [breadth-first-search, depth-first-search, whatever-first-search, graph-reachability, tree-traversal, graph-exploration, lexicographic-bfs, maximum-cardinality-search]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 20, Elementary Graph Algorithms (the introduction, Section 20.2 and Section 20.3)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 5, Basic Graph Algorithms (the sections on whatever-first search and its important variants)
  - paper: doi:10.1137/050623498
    title: Derek G. Corneil and Richard M. Krueger, A unified view of graph searching, SIAM Journal on Discrete Mathematics 22(4), 1259 to 1276 (2008)
    locator: the whole paper (characterizations of the vertex orders of generic search, BFS, DFS, LexBFS and LexDFS)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 3.2, Graph connectivity and graph traversal
---

A graph traversal, or graph search, is a procedure that visits each vertex reachable from a start vertex exactly one time, where each new vertex is reached through an edge from a vertex that was visited before. Its result is an order of the reachable vertices, and with it a tree of the edges through which the vertices were first reached. [Breadth-first search](/breadth-first-search/) and [depth-first search](/depth-first-search/) are the two classic traversals, and [whatever-first search](/whatever-first-search/) is the generic form that contains both.

## Definition

Let $G = (V, E)$ be a [graph](/graph/), directed or undirected, and $s \in V$. In an undirected graph, read each edge $\{u, v\}$ as the two directed edges $(u, v)$ and $(v, u)$. Let $R(s)$ be the set of vertices $v$ such that there is a [walk](/walk/) from $s$ to $v$; it contains $s$.

**Traversal order.** A *traversal order from $s$* is a sequence $\sigma = (v_1, v_2, \ldots, v_k)$ of distinct vertices such that

1. $v_1 = s$;
2. for each $i$ with $2 \le i \le k$, there is an index $j < i$ with $(v_j, v_i) \in E$;
3. no edge $(v_j, w) \in E$ has $w \notin \{v_1, \ldots, v_k\}$.

Condition 2 says that each new vertex is reached by an edge from a vertex already visited. Condition 3 says that the traversal does not stop while an edge leads out of the visited set.

**Traversal tree.** A *traversal tree* of $\sigma$ is a choice, for each $i \ge 2$, of one parent $p(v_i) = v_j$ with $j < i$ and $(v_j, v_i) \in E$.

**Proposition.** For each traversal order from $s$, the set $\{v_1, \ldots, v_k\}$ is exactly $R(s)$, and each traversal tree is a tree on $R(s)$ with root $s$ in which the path from $s$ to each vertex follows edges of $G$.

*Proof.* Let $S = \{v_1, \ldots, v_k\}$. First, $S \subseteq R(s)$, by induction on $i$: $v_1 = s \in R(s)$, and for $i \ge 2$ the vertex $v_i$ has a parent $v_j$ with $j < i$, which is in $R(s)$ by the induction hypothesis, so a walk to $v_j$ followed by the edge $(v_j, v_i)$ is a walk to $v_i$. Next, $R(s) \subseteq S$. Take $w \in R(s)$ and a walk $s = x_0, x_1, \ldots, x_r = w$. If $w \notin S$, let $t$ be the least index with $x_t \notin S$. Then $t \ge 1$, $x_{t-1} \in S$ and $(x_{t-1}, x_t) \in E$, which contradicts condition 3. For the tree, each $v_i$ with $i \ge 2$ has one parent with a smaller index, so following parents strictly decreases the index, never repeats a vertex and ends at $v_1 = s$. So the parent edges form a tree on $S$ with root $s$, and each of them is an edge of $G$. $\square$

**Full traversal.** A *full traversal* of $G$ visits all of $V$. It is a sequence of traversal orders from start vertices $s_1, s_2, \ldots$, where each $s_{t+1}$ is a vertex not visited before and the $t$-th search ignores edges to vertices of earlier searches. Its trees form a spanning forest of $G$. For an undirected graph, the trees of a full traversal are spanning trees of the [connected components](/connected-components/).

**Particular traversals.** A traversal is defined by its rule for the next vertex. In [breadth-first search](/breadth-first-search/), the parent of each $v_i$ is its earliest neighbour in $\sigma$, and the positions of the parents $p(v_2), p(v_3), \ldots$ never decrease, so the vertices come in order of distance from $s$. In [depth-first search](/depth-first-search/), the next vertex is a neighbour of the most recently visited vertex that still has an unvisited neighbour. Corneil and Krueger (2008) state these rules, and those of [lexicographic BFS](/lexicographic-bfs/) and lexicographic DFS, as conditions on triples and quadruples of vertices of the order.

**Cost.** A traversal that reads each adjacency list one time takes $\Theta(n_s + m_s)$ time on the reachable part, with $n_s = |R(s)|$ and $m_s$ the number of edges out of $R(s)$, in the [word RAM](/word-ram/) model with [adjacency lists](/adjacency-list/).

## Examples and non-examples

Take the undirected graph with vertices 0 to 7 and the edges $\{0,1\}$, $\{0,2\}$, $\{1,3\}$, $\{2,3\}$, $\{2,4\}$, $\{3,5\}$, $\{4,5\}$, $\{5,6\}$. Vertex 7 has no edge, so $R(0) = \{0, 1, \ldots, 6\}$.

| sequence | traversal order from 0? | why |
|---|---|---|
| 0 1 2 3 4 5 6 | yes, the BFS order | each vertex has an earlier neighbour, and no edge leaves the set |
| 0 1 3 2 4 5 6 | yes, the DFS preorder | 3 follows 1, 2 follows 3, 4 follows 2, 5 follows 4, 6 follows 5 |
| 0 2 4 5 6 3 1 | yes | a DFS gives it when the lists of 0 and 5 start with 2 and 6 |
| 0 3 1 2 4 5 6 | no | 3 has no neighbour among the earlier vertices, which are only 0 |
| 0 1 2 3 4 5 | no | the edge $\{5, 6\}$ leaves the set, so condition 3 fails |
| 0 1 2 3 4 5 6 7 | no | 7 has no earlier neighbour; a full traversal starts a new search at 7 instead |
| 0 1 0 2 | no | a vertex appears twice; this is a [walk](/walk/), not a traversal |

**Counting.** The number of traversal orders depends on the shape of the graph. For a path $0, 1, \ldots, n-1$ started at 0 there is exactly one. For a star with centre 0 and $k$ leaves, started at 0, each order of the leaves is allowed, so there are $k!$ traversal orders. For the triangle on $\{0, 1, 2\}$ started at 0, there are 2.

**Non-example: a tour of an agent.** A robot that walks along the edges of an unknown graph must also walk back along edges it already used, so its route is a walk with repeated vertices. That route is a solution of [graph exploration](/graph-exploration/), and the order in which it first sees the vertices is a traversal order.

## Related definitions

- **[Graph reachability](/graph-reachability/).** The problem whose answer is the set $R(s)$ of the proposition.
- **[Whatever-first search](/whatever-first-search/).** The generic algorithm: keep a bag of edges to examine, and take any edge out of it. Each traversal order is an output of it, for some choice of the bag.
- **[Breadth-first search](/breadth-first-search/)** and **[depth-first search](/depth-first-search/).** The traversals with a queue and with a stack.
- **[Tree traversal](/tree-traversal/).** The special case of a rooted tree, with its own orders: [preorder](/preorder-traversal/), [inorder](/inorder-traversal/), [postorder](/postorder-traversal/) and [level order](/level-order-traversal/).
- **[Depth-first orders](/depth-first-orders/).** The preorder, postorder and reverse postorder of a DFS.
- **[Lexicographic BFS](/lexicographic-bfs/)** and **[maximum cardinality search](/maximum-cardinality-search/).** Traversals with a special tie-breaking rule, used on chordal graphs.
- **[Graph exploration](/graph-exploration/).** The version in which an agent walks the graph and pays for each step.

## References
