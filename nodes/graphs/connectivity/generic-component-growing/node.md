---
tag: 753N4R
kind: algorithm
slug: generic-component-growing
name: Generic component-growing algorithm
area: graphs/connectivity
level: intro
summary: Builds the connected component of a start vertex by repeatedly adding any vertex adjacent to the current set, the common core of BFS and DFS.
solves: [connected-components, graph-reachability]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [connected-graph, graph-traversal]
see_also: [whatever-first-search, breadth-first-search, depth-first-search, connected-components, union-find-connectivity, flood-fill, prim, spanning-forest]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 3.2, Graph connectivity and graph traversal (the rule "while there is an edge (u, v) with u in R and v not in R, add v to R", and its proof)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 5, Basic graph algorithms (whatever-first search, and counting and labeling components)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.1, Undirected graphs (connected components with depth-first search)
---

The generic component-growing algorithm finds the [connected component](/connected-components/) of a start vertex $s$ in an [undirected graph](/undirected-graph/). It keeps a set $S$ that starts as $\{s\}$, and while some edge joins a vertex of $S$ to a vertex outside $S$, it adds that outside vertex to $S$. It does not say which such edge to use. Every choice ends with $S$ equal to the component of $s$, and the edges used form a [spanning tree](/spanning-tree/) of it. [Breadth-first search](/breadth-first-search/) and [depth-first search](/depth-first-search/) are two ways to make the choice, and [Prim's algorithm](/prim/) is a third. Run from each vertex that has no label yet, it labels all components in $\Theta(n + m)$ time.

## In plain words

You stand in one town and want to know every town you can reach by road. Keep a list of the towns you know you can reach. At first it holds only your own town.

Now look for any road that goes from a town on the list to a town not on the list. Add that town. Do this again and again, in any order you like. When no such road is left, the list is exactly the set of towns you can reach.

The order does not change the final list. It only changes the shape of the roads you used to get there. Taking the newest town first is a depth-first walk, and taking the oldest town first is close to a breadth-first walk.

## The problem

**Input.** An undirected graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, given by [adjacency lists](/adjacency-list/) $\mathrm{Adj}[v]$, where an edge $\{u, v\}$ with $u \ne v$ is in the lists of both ends. $E$ may have parallel edges and [self-loops](/self-loop/); a loop at $v$ is in $\mathrm{Adj}[v]$ once or twice. The graph need not be connected.

**Output.** For one start vertex $s$: the set $C(s)$ of vertices joined to $s$ by a path, and a parent for each vertex of $C(s) \setminus \{s\}$. For the whole graph: a label $\mathrm{comp}[v] \in \{0, \ldots, k-1\}$ for each vertex, with $\mathrm{comp}[u] = \mathrm{comp}[v]$ if and only if $u$ and $v$ are in the same component, and the number $k$ of components. This is the [connected components](/connected-components/) problem.

## The algorithm

The abstract rule is: $S \leftarrow \{s\}$; while some edge $\{u, v\}$ has $u \in S$ and $v \notin S$, choose any such edge and add $v$ to $S$ with $\mathrm{parent}[v] = u$. To find a crossing edge fast, the procedure below keeps a *frontier* $F$: the vertices of $S$ whose lists it has not read to the end. Each vertex $u$ has a pointer $\mathrm{next}[u]$ to the first entry of $\mathrm{Adj}[u]$ that it has not read. The choice of $u$ in line L4 is free.

```pseudo id=main
GROW(G, s, k)                              ▷ comp[s] = nil; label C(s) with k
L1  comp[s] ← k, next[s] ← 0
L2  F ← {s}                                ▷ vertices of S with unread list entries
L3  while F ≠ ∅ do
L4      choose any u ∈ F
L5      if next[u] = |Adj[u]| then remove u from F
        else
L6          v ← Adj[u][next[u]], next[u] ← next[u] + 1
L7          if comp[v] = nil then          ▷ the edge {u, v} crosses the cut
L8              comp[v] ← k, parent[v] ← u, next[v] ← 0, add v to F

COMPONENTS(G)
L9  comp[v] ← nil and parent[v] ← nil for each v ∈ V, k ← 0
L10 for s ← 0 to n − 1 do
L11     if comp[s] = nil then GROW(G, s, k), k ← k + 1
L12 return comp, parent, k
```

The set $S$ of the abstract rule is the set of vertices with $\mathrm{comp}[v] = k$. Line L6 reads one list entry, and line L7 throws it away when it leads back into $S$: this happens for loops, for the second copy of a parallel edge, and for the edge back to the parent.

**Choices for line L4.** Keep $F$ as an array and remove an item by moving the last item into its place.

| rule for line L4 | the search it gives |
|---|---|
| the vertex added last | [depth-first search](/depth-first-search/) order of discovery |
| the vertex added first | a breadth-first order: each vertex is scanned to the end before the next |
| a random vertex | a random spanning tree shape, same components |
| the vertex with the cheapest crossing edge | [Prim's algorithm](/prim/), with a [priority queue](/priority-queue/) over edges |

## Example

The graph has $n = 9$ vertices and 9 edges: $\{0,1\}$, $\{1,2\}$, $\{2,0\}$, $\{3,4\}$ twice (parallel), $\{5,6\}$, $\{6,7\}$, $\{5,7\}$, and the loop $\{8,8\}$. The lists, in the order of the edges, are $\mathrm{Adj}[0] = [1, 2]$, $\mathrm{Adj}[1] = [0, 2]$, $\mathrm{Adj}[2] = [1, 0]$, $\mathrm{Adj}[3] = [4, 4]$, $\mathrm{Adj}[4] = [3, 3]$, $\mathrm{Adj}[5] = [6, 7]$, $\mathrm{Adj}[6] = [5, 7]$, $\mathrm{Adj}[7] = [6, 5]$ and $\mathrm{Adj}[8] = [8]$. Line L4 takes the vertex added last.

| step | $u$ | entry read | action | $F$ after |
|---|---|---|---|---|
| start | | | GROW$(G, 0, 0)$ | $[0]$ |
| 1 | 0 | 1 | add 1, parent 0 | $[0, 1]$ |
| 2 | 1 | 0 | skip | $[0, 1]$ |
| 3 | 1 | 2 | add 2, parent 1 | $[0, 1, 2]$ |
| 4, 5 | 2 | 1, then 0 | skip both | $[0, 1, 2]$ |
| 6, 7 | 2, then 1 | end of list | remove | $[0]$ |
| 8 | 0 | 2 | skip | $[0]$ |
| 9 | 0 | end of list | remove | $[\,]$ |
| start | | | GROW$(G, 3, 1)$ | $[3]$ |
| 10 | 3 | 4 | add 4, parent 3 | $[3, 4]$ |
| 11, 12 | 4 | 3, then 3 | skip both; the second is the parallel edge | $[3, 4]$ |
| 13 to 15 | 4, then 3 | end, 4, end | remove 4; skip the parallel copy; remove 3 | $[\,]$ |

The component of 5 goes like the one of 0, with the parents $\mathrm{parent}[6] = 5$ and $\mathrm{parent}[7] = 6$. GROW$(G, 8, 3)$ reads the loop entry 8, skips it, and stops. The result is $\mathrm{comp} = [0, 0, 0, 1, 1, 2, 2, 2, 3]$ and $k = 4$. The parent pointers give the $n - k = 5$ tree edges $\{0,1\}$, $\{1,2\}$, $\{3,4\}$, $\{5,6\}$, $\{6,7\}$.

With the rule "the vertex added first", the labels are the same, but 0 reads both of its entries first, so $\mathrm{parent}[2] = 0$ and $\mathrm{parent}[7] = 5$: a different spanning tree.

## Correctness

Fix one call GROW$(G, s, k)$ and let $S$ be the set of vertices with label $k$. Two facts hold after each step of the loop of line L3.

1. *Every vertex of $S$ is reachable from $s$.* A vertex enters $S$ in line L8 only when it is a neighbour of a vertex $u$ already in $S$, and the parent pointers give the path back to $s$.
2. *Every list entry that was read leads into $S$, and every vertex of $S$ that is not in $F$ has read all its list.* Line L6 reads an entry; if it leads outside $S$, line L8 puts its end into $S$ at once. Line L5 removes a vertex only when its pointer is at the end.

The loop stops, because each step reads an entry or removes a vertex, and there are finitely many of both. When $F$ is empty, fact 2 says that no edge leaves $S$. If some vertex $w$ reachable from $s$ were outside $S$, the first edge of a path from $s$ to $w$ that leaves $S$ would contradict this. With fact 1, $S$ is exactly the component $C(s)$. Vertices outside $C(s)$ cannot get the label $k$, and COMPONENTS calls GROW once for each component, at its smallest vertex. The full proof is below.

## Complexity

Each step of the loop of line L3 either reads one list entry (lines L6 to L8) or removes one vertex from $F$ (line L5). Over all calls, each of the $\sum_v |\mathrm{Adj}[v]| \le 2m$ entries is read once and each vertex enters and leaves $F$ once. With $O(1)$ time for line L4, the total time is $\Theta(n + m)$; the term $n$ comes from line L9 and the loop of line L10, and the term $m$ from reading every list. This holds in the best case too, since every entry is read.

The extra space is $\Theta(n)$: the arrays comp, parent and next, and $F$, which holds each vertex at most once. A frontier of edges, as in the abstract rule, would need $\Theta(m)$ space.

If line L4 picks by a priority, as in Prim's algorithm, it costs $O(\log n)$ with a [binary heap](/binary-heap/), and the time grows to $O((n + m) \log n)$.

## Properties

- **Any order is correct.** The proof uses no property of the choice in line L4.
- **Spanning forest.** The parent edges form a [spanning forest](/spanning-forest/) of $G$, one tree for each component, with $n - k$ edges.
- **No recursion.** The frontier is an explicit set, so a long path does not overflow a call stack.
- **Order-dependent output.** The labels depend only on the order of the start vertices in line L10. The parents depend on the rule of line L4 and on the order of the lists.

## Variants and improvements

- **[Whatever-first search](/whatever-first-search/).** Keep a bag of edges instead of vertices with pointers. This is the same idea with $O(m)$ space, and it is the form in which the bag's rule gives BFS, DFS and best-first search.
- **Directed graphs.** With out-lists, GROW$(G, s, k)$ finds the vertices [reachable](/reachability/) from $s$. It does not give strongly connected components; see [strongly connected components](/strongly-connected-components/).
- **Union-find.** Read the edges in any order and join the sets of their ends with a [union-find structure](/union-find-connectivity/). This needs no adjacency lists and works on a stream of edges, in $O(m \, \alpha(n))$ time.
- **Grids.** On a grid of pixels the same rule is [flood fill](/flood-fill/).
- **Prim.** Choose the crossing edge of least weight. Then the tree is a [minimum spanning tree](/minimum-spanning-tree/).

## When to use it

Use it to explain and prove graph search once, for all orders. In a program, pick the rule that gives the extra structure you need: BFS for shortest paths in edges, DFS for [low-link](/low-link/) values and [edge classification](/edge-classification/), any rule when you need only the components. If the edges arrive as a list or a stream, use union-find instead.

## Pitfalls

- **Marking late.** Set the label when the vertex enters $F$ (line L8), not when it is chosen. If you mark on removal, a vertex can enter $F$ many times and the space grows to $\Theta(m)$.
- **Loops and parallel edges.** They are read and skipped by line L7, so they need no special case. Code that skips only the entry of the parent vertex, but not other entries that lead into $S$, adds a vertex twice.
- **Directed input.** If an undirected edge is stored in only one list, some vertices are missed. Store both directions.
- **Recursion.** A recursive DFS form fails on a path of $10^5$ vertices in many languages. The frontier form does not.

## Implementations

## History

The rule of growing a set along crossing edges is folklore, and it is older than computers: Trémaux's method for mazes, from the nineteenth century, is a depth-first form of it. Kleinberg and Tardos state it in this generic form and prove it before they give BFS and DFS as two ways to choose the edge. Erickson calls the edge-bag form whatever-first search.

## References
