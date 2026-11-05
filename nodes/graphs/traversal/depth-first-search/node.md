---
tag: Q8B7W6
kind: algorithm
slug: depth-first-search
name: Depth-first search
aliases:
- DFS
area: graphs/traversal
level: intro
summary: Explores as deep as possible along each branch before backtracking, using a stack or recursion.
solves: [graph-reachability]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true}
prereqs: [graph-traversal, stack, recursion, adjacency-list]
see_also: [breadth-first-search, discovery-and-finish-times, parenthesis-theorem, white-path-theorem, edge-classification, dfs-forest, topological-sort, iterative-depth-first-search]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.3, Depth-first search (the procedures DFS and DFS-VISIT, the analysis, the parenthesis theorem, the white-path theorem and the classification of edges)
  - paper: doi:10.1137/0201010
    title: Robert E. Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 146 to 160 (1972)
    locator: the whole paper (depth-first search as a basis for linear-time algorithms for strong components and biconnected components)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 3, Decompositions of graphs (Section 3.2, Depth-first search in undirected graphs, and Section 3.3, Depth-first search in directed graphs)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.1, Undirected graphs (Trémaux exploration and the class DepthFirstSearch), and Section 4.2, Directed graphs
  - book: isbn:9780521736534
    title: Shimon Even, Graph Algorithms, second edition, edited by Guy Even, Cambridge University Press (2012)
    locator: Chapter 3, Depth-First Search (Section 3.1, DFS of undirected graphs, with Trémaux's algorithm)
  - book: "Édouard Lucas, Récréations mathématiques, volume 1, Gauthier-Villars, Paris (1882)"
    locator: Chapter 3, Le jeu des labyrinthes (the first publication of Trémaux's method)
---

Depth-first search (DFS) explores a [graph](/graph/) by always following an edge out of the vertex it reached most recently, and it goes back only when that vertex has no unexplored edge left. It gives each vertex a [discovery time and a finish time](/discovery-and-finish-times/), and its parent pointers form the [depth-first forest](/dfs-forest/). On a graph with $n$ vertices and $m$ edges in [adjacency lists](/adjacency-list/), it runs in $\Theta(n + m)$ time. The time stamps and the forest are the base of many linear-time graph algorithms: [topological sort](/topological-sort/), [strongly connected components](/strongly-connected-components/), [articulation points](/articulation-point/) and [cycle detection](/cycle-detection/).

## In plain words

Think of a walk through a maze with a piece of chalk. At each crossing, you take a corridor that you have not tried yet, and you go as far as you can. When you reach a dead end, or a crossing that you have already marked, you walk back to the last crossing that still has an untried corridor. You stop when you are back at the start and every corridor there is tried.

Depth-first search does this on a graph. It remembers the way back with a [stack](/stack/), or with the calls of a [recursive](/recursion/) function. It writes down the moment it first enters each vertex and the moment it leaves it for good. These two moments tell a lot about the shape of the graph, for example whether it has a cycle.

## The problem

The input is a graph $G = (V, E)$, directed or undirected, with $V = \{0, 1, \ldots, n-1\}$ and adjacency lists $\mathrm{Adj}[u]$. An undirected edge is in both lists. DFS has no single output. Its results are the discovery time $d[u]$, the finish time $f[u]$ and the parent $\pi[u]$ of each vertex. These solve [graph reachability](/graph-reachability/): a call DFS-VISIT$(s)$ on a graph with all vertices white discovers exactly the vertices reachable from $s$. Other problems use the time stamps, as the section on uses below shows.

## The algorithm

Each vertex has a colour. It is *white* before it is discovered, *gray* while its call of DFS-VISIT runs, and *black* when the call is finished. A global clock $time$ counts the events.

```pseudo id=main
DFS(G)
L1  for each vertex u ∈ V do color[u] ← WHITE, π[u] ← NIL
L2  time ← 0
L3  for each vertex u ∈ V do
L4      if color[u] = WHITE then DFS-VISIT(G, u)

DFS-VISIT(G, u)
L5  time ← time + 1, d[u] ← time, color[u] ← GRAY        ▷ u is discovered
L6  for each v ∈ Adj[u] do
L7      if color[v] = WHITE then
L8          π[v] ← u
L9          DFS-VISIT(G, v)
L10 time ← time + 1, f[u] ← time, color[u] ← BLACK       ▷ u is finished
```

The outer loop of line L3 starts a new tree at each vertex that is still white, so every vertex is visited, also in a graph that is not connected. Each vertex that line L4 picks becomes a root of the [depth-first forest](/dfs-forest/). Line L7 is the only test: an edge to a gray or black vertex is looked at and then ignored. The colour of $v$ at that moment is still useful, because it tells the type of the edge $(u, v)$ (see [edge classification](/edge-classification/)).

Each time stamp from 1 to $2n$ is used exactly once, and $d[u] < f[u]$. The recursion keeps the gray vertices on the call stack. At each moment, the gray vertices form the path of the forest from the current root to the vertex whose call runs now. The page [nonrecursive depth-first search](/iterative-depth-first-search/) gives the same procedure with an explicit stack.

## Example

The directed graph has the vertices 0 to 6 and the 10 edges below, with the adjacency lists in the order given.

| $u$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $\mathrm{Adj}[u]$ | 1, 3, 2 | 2 | 0 | 2, 4 | none | 4, 6 | 5 |

| time | event | gray vertices (the stack) |
|---|---|---|
| 1 | discover 0 | 0 |
| 2 | discover 1 (tree edge from 0) | 0 1 |
| 3 | discover 2 (tree edge from 1) | 0 1 2 |
| 4 | finish 2; its edge to 0 meets a gray vertex | 0 1 |
| 5 | finish 1 | 0 |
| 6 | discover 3 (tree edge from 0) | 0 3 |
| 7 | discover 4 (tree edge from 3); before this, the edge $3 \to 2$ met a black vertex | 0 3 4 |
| 8 | finish 4 | 0 3 |
| 9 | finish 3 | 0 |
| 10 | finish 0; its last edge $0 \to 2$ meets a black vertex | none |
| 11 | discover 5 (new root) | 5 |
| 12 | discover 6 (tree edge from 5); before this, the edge $5 \to 4$ met a black vertex | 5 6 |
| 13 | finish 6; its edge to 5 meets a gray vertex | 5 |
| 14 | finish 5 | none |

The result is:

| $u$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $d[u]$ | 1 | 2 | 3 | 6 | 7 | 11 | 12 |
| $f[u]$ | 10 | 5 | 4 | 9 | 8 | 14 | 13 |
| $\pi[u]$ | NIL | 0 | 1 | 0 | 3 | NIL | 5 |

The forest has two trees, rooted at 0 and at 5. Written as brackets, the discovery and finish events are $(0\ (1\ (2\ 2)\ 1)\ (3\ (4\ 4)\ 3)\ 0)\ (5\ (6\ 6)\ 5)$: the brackets are well nested, as the [parenthesis theorem](/parenthesis-theorem/) says. Of the 10 edges, 5 are tree edges, $2 \to 0$ and $6 \to 5$ are back edges, $0 \to 2$ is a forward edge, and $3 \to 2$ and $5 \to 4$ are cross edges. The back edge $2 \to 0$ shows the cycle $0, 1, 2$.

## Correctness

DFS terminates, gives each vertex exactly one discovery time and one finish time, and uses each of the times $1, \ldots, 2n$ once. The parent pointers form a forest whose roots are the vertices picked by line L4. A call DFS-VISIT$(s)$, made when all vertices are white, discovers exactly the vertices reachable from $s$. The key fact is that a vertex is discovered only through an edge from a gray vertex, and that a gray vertex scans its whole list before it turns black. The full proof is below.

The two structural theorems of DFS have their own pages, with full proofs:

- **[Parenthesis theorem](/parenthesis-theorem/).** For any two vertices $u$ and $v$, the intervals $[d[u], f[u]]$ and $[d[v], f[v]]$ are disjoint, or one contains the other. The second case holds exactly when one vertex is a descendant of the other in the forest.
- **[White-path theorem](/white-path-theorem/).** The vertex $v$ is a descendant of $u$ if and only if, at time $d[u]$, there is a path from $u$ to $v$ whose vertices are all white.

## Complexity

The cost is in the [word RAM](/word-ram/) model, with the graph as adjacency lists.

- **Lines L1 to L4.** The two loops over $V$ take $\Theta(n)$ time, not counting the calls.
- **The calls.** DFS-VISIT$(u)$ is called only when $u$ is white, and it makes $u$ gray at once. So it is called exactly one time for each vertex.
- **The scans.** The loop of line L6 runs through $\mathrm{Adj}[u]$ one time, in the call for $u$. The total length of the lists is $\sum_u |\mathrm{Adj}[u]| = m$ for a directed graph and $2m$ for an undirected graph. Each step of the loop takes $O(1)$ time besides the recursive call.

So DFS takes $\Theta(n + m)$ time, in the best and in the worst case, because each list is scanned in full on every input. The extra space is $\Theta(n)$ for the colours, the times and the parents. The stack holds the gray vertices, so its depth is at most $n$, and it is $n$ on a path. With an [adjacency matrix](/adjacency-matrix/), line L6 reads a full row for each vertex, and the time is $\Theta(n^2)$.

## Properties

- **Deterministic.** The result depends on the order of the vertices in line L3 and on the order of each adjacency list. A different order gives a different forest and different times, but the theorems hold for every order.
- **Recursive.** The natural form is recursive. The recursion depth can reach $n$, so programs for large graphs use an explicit stack.
- **No distances.** The tree path from the root to a vertex is a path of the graph, but in general it is not a shortest path. Use [breadth-first search](/breadth-first-search/) for distances.
- **Undirected graphs.** In a DFS of an undirected graph, each edge is a tree edge or a back edge. There are no forward and no cross edges.

## Variants and improvements

- **Single-source DFS.** Call DFS-VISIT$(s)$ once, without the loop of line L3. This visits exactly the vertices reachable from $s$.
- **Nonrecursive DFS.** Keep a stack of pairs (vertex, position in its list). It gives the same times as the recursive form. See [nonrecursive depth-first search](/iterative-depth-first-search/).
- **Stack of vertices.** Push all neighbours of a vertex, and mark a vertex when it is popped. This is a [whatever-first search](/whatever-first-search/) with a stack. It visits the vertices in a depth-first manner, but its order and its parent tree can differ from the recursive DFS, and its stack can hold $\Theta(m)$ items.
- **Orders.** Record the vertices in order of discovery (preorder) or of finish (postorder). The reverse postorder of a directed acyclic graph is a [topological ordering](/topological-ordering/). See [depth-first orders](/depth-first-orders/).
- **Low links.** Keep for each vertex the smallest discovery time that its subtree reaches by one back edge. This gives [articulation points](/articulation-point/), [bridges](/bridge-finding/) and [Tarjan's strong components algorithm](/tarjan-scc/).
- **Depth limit.** Stop at a given depth. This is [depth-limited search](/depth-limited-search/), and with growing limits it is [iterative deepening](/iterative-deepening-search/).
- **Mazes.** Walking a maze in person with marks on the corridors is [Trémaux traversal](/tremaux-traversal/).

## When to use it

Use DFS when the structure of the graph matters more than distances: to find cycles, to sort a directed acyclic graph, to find strong components, cut vertices and bridges, or to explore a search space with little memory. For plain reachability, DFS and [BFS](/breadth-first-search/) cost the same, and either one is fine. On a very large or implicit graph, DFS keeps only the current path, while BFS keeps a whole layer. If you need the fewest edges from the source, use BFS.

## Pitfalls

- **Stack overflow.** On a long path the recursion is $n$ calls deep. Python stops at about 1000 calls by default, and C programs can crash on large graphs. Use an explicit stack for large inputs.
- **Marking too late.** In the recursive form, line L5 must set the colour to gray before the loop of line L6 runs. If the mark is set after the loop, a cycle sends the search around for ever.
- **Gray and black together.** A cycle test in a directed graph must tell gray vertices from black ones. A single "visited" flag cannot tell a back edge, which closes a cycle, from a cross edge, which does not.
- **Forgotten roots.** A single call DFS-VISIT$(s)$ visits only the vertices reachable from $s$. For a forest of the whole graph, and for the time stamps that topological sort needs, keep the loop of line L3.
- **Parent edge in undirected graphs.** In an undirected graph, the edge back to the parent shows up as an edge to a gray vertex. A cycle test must skip this one edge, but not a second, parallel edge to the parent.

## Implementations

## History

Charles Pierre Trémaux found a method to explore a maze with marks on the corridors in the 19th century. Édouard Lucas published it in 1882, and Even's book gives it as the first form of depth-first search. Robert Tarjan showed in 1972 that DFS, with its time stamps and its tree, gives linear-time algorithms for strong components and biconnected components.

## References
