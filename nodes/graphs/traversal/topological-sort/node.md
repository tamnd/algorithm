---
tag: KDXVF9
kind: algorithm
slug: topological-sort
name: Topological sort
aliases:
- topological sorting
area: graphs/traversal
level: intro
summary: Produces a topological ordering by reversing DFS finish order.
solves: [topological-ordering, cycle-detection]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true}
prereqs: [depth-first-search, topological-ordering, depth-first-orders]
see_also: [kahns-algorithm, topological-ordering-theorem, edge-classification, discovery-and-finish-times, dfs-cycle-detection, dag-shortest-paths, kosaraju-sharir, dynamic-topological-order]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.4, Topological sort (the procedure TOPOLOGICAL-SORT, the lemma on back edges and the correctness theorem)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.2, Directed graphs (directed cycle detection, DepthFirstOrder and Topological, reverse postorder in a DAG is a topological sort)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 3, Section 3.3.2, Directed acyclic graphs (linearize by decreasing post numbers)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 3.6, Directed acyclic graphs and topological ordering
---

Topological sort by depth-first search lists the vertices of a [directed acyclic graph](/directed-acyclic-graph/) in decreasing order of their DFS finish times. A run of [depth-first search](/depth-first-search/) puts each vertex at the front of a list when it finishes, and in an acyclic graph each edge $(u, v)$ has $v$ finished before $u$, so the list is a [topological ordering](/topological-ordering/). The same run detects a directed cycle: it meets a vertex that is still being explored exactly when the graph is not acyclic. The algorithm takes $\Theta(n + m)$ time on a graph with $n$ vertices and $m$ edges in [adjacency lists](/adjacency-list/), like [Kahn's algorithm](/kahns-algorithm/), the other classical method.

## In plain words

Explore the graph depth first. When you have explored everything that a vertex leads to, that vertex is done. Write it at the front of a list.

A vertex is done only after everything it points to is done. So everything it points to is already on the list, behind it. When the search ends, each vertex is in front of all the vertices it points to, which is what we want.

If the search ever follows an edge to a vertex that it is still in the middle of, that vertex leads back to itself. Then there is a loop, and no valid order exists.

## The problem

Given a directed graph $G = (V, E)$, return a list of all its vertices in which each edge $(u, v)$ has $u$ before $v$, or report that $G$ has a directed cycle, in which case no such list exists by the [topological ordering theorem](/topological-ordering-theorem/).

## The algorithm

The colours are as in DFS: *white* before the visit of a vertex, *gray* while its visit runs, *black* after it. The list $L$ starts empty and gets vertices at its front.

```pseudo id=main
TOPOLOGICAL-SORT(G)
L1  for each vertex u ∈ V do color[u] ← WHITE
L2  L ← empty linked list
L3  for each vertex u ∈ V do
L4      if color[u] = WHITE then VISIT(G, u)
L5  return L

VISIT(G, u)
L6  color[u] ← GRAY
L7  for each v ∈ Adj[u] do
L8      if color[v] = GRAY then stop and report "G has a cycle"
L9      if color[v] = WHITE then VISIT(G, v)
L10 color[u] ← BLACK
L11 insert u at the front of L                          ▷ u is finished
```

This is DFS without the clock. The order in which line L11 runs is the order of the finish times $f$, so $L$ is the [reverse postorder](/depth-first-orders/), the vertices in decreasing order of $f$. Line L8 is the test for a back edge, from [edge classification](/edge-classification/): an edge to a gray vertex goes to an ancestor. Without line L8, the procedure still returns a list, but on a graph with a cycle that list is not a topological ordering.

To return a cycle as a certificate, keep the parents $\pi$ as in DFS. When line L8 finds the gray vertex $v$ from $u$, the vertices $v, \ldots, \pi[\pi[u]], \pi[u], u$ on the tree path, followed by the edge $(u, v)$, form a cycle.

## Example

Take the acyclic graph with vertices 0 to 6 and these lists.

| $u$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $\mathrm{Adj}[u]$ | 1, 3, 2 | 2 | none | 2, 4 | none | 4, 6 | none |

| step | event | gray vertices | $L$ after the step |
|---|---|---|---|
| 1 | VISIT(0) | 0 | empty |
| 2 | VISIT(1), from 0 | 0 1 | empty |
| 3 | VISIT(2), from 1 | 0 1 2 | empty |
| 4 | 2 has no edges: finish 2 | 0 1 | 2 |
| 5 | finish 1 | 0 | 1, 2 |
| 6 | VISIT(3), from 0 | 0 3 | 1, 2 |
| 7 | edge $3 \to 2$: 2 is black, skip; VISIT(4), from 3 | 0 3 4 | 1, 2 |
| 8 | finish 4 | 0 3 | 4, 1, 2 |
| 9 | finish 3 | 0 | 3, 4, 1, 2 |
| 10 | edge $0 \to 2$: 2 is black, skip; finish 0 | none | 0, 3, 4, 1, 2 |
| 11 | VISIT(5), new root | 5 | 0, 3, 4, 1, 2 |
| 12 | edge $5 \to 4$: 4 is black, skip; VISIT(6), from 5 | 5 6 | 0, 3, 4, 1, 2 |
| 13 | finish 6 | 5 | 6, 0, 3, 4, 1, 2 |
| 14 | finish 5 | none | 5, 6, 0, 3, 4, 1, 2 |

The output is $5, 6, 0, 3, 4, 1, 2$. Each of the 8 edges goes forward in it. The DFS times are $d = (1, 2, 3, 6, 7, 11, 12)$ and $f = (10, 5, 4, 9, 8, 14, 13)$, and the output is the vertices sorted by decreasing $f$.

**With a cycle.** Add the edge $2 \to 0$, so the list of 2 is $0$. At step 4, VISIT(2) scans the edge $2 \to 0$ while 0 is gray. Line L8 stops and reports a cycle. The gray path $0, 1, 2$ with the edge $2 \to 0$ is the cycle.

## Correctness

If $G$ is acyclic, the output contains each vertex once, and for each edge $(u, v)$, $v$ is inserted before $u$, so $u$ ends up in front of $v$. The reason: when VISIT$(u)$ scans the edge, $v$ is not gray, because a gray $v$ would be an ancestor of $u$ and close a cycle. If $v$ is white, it is visited and finished inside the visit of $u$. If $v$ is black, it is already finished. In both cases $v$ is inserted before line L11 runs for $u$. If $G$ has a cycle, the first vertex $x$ of the cycle to turn gray reaches the rest of the cycle through white vertices, so by the [white-path theorem](/white-path-theorem/) the vertex before $x$ on the cycle is visited inside the visit of $x$, and its scan of the edge to $x$ finds $x$ gray. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model, with the graph as adjacency lists.

- **Lines L1 to L4.** $\Theta(n)$ time besides the visits.
- **Visits.** VISIT$(u)$ is called only when $u$ is white and makes it gray at once, so it is called at most one time for each vertex, and exactly one time each if no cycle is found.
- **Scans.** The loop of line L7 runs through $\mathrm{Adj}[u]$ one time, with $O(1)$ work per entry besides the call, so the scans take $O(m)$ in total. Line L11 takes $O(1)$ with a linked list, or with an array that is filled from the end.

So the time is $\Theta(n + m)$ in the worst case, and on every acyclic input. If a cycle is found early, the run can stop after $\Theta(n)$ time, the cost of line L1, which is the best case. The extra space is $\Theta(n)$ for the colours and the list, plus the recursion stack, whose depth is at most $n$.

## Properties

- **Deterministic.** The output depends on the order of line L3 and of the lists. Different orders can give different topological orderings, and all of them are valid.
- **Recursive.** The natural form is recursive, with depth up to $n$ on a path. The implementation below uses an explicit stack.
- **Not online.** The first vertex of the output is known only at the very end, because $L$ is built from the back. [Kahn's algorithm](/kahns-algorithm/) outputs from the front.
- **Detects cycles.** The same run is a complete test for directed cycles. This is [DFS cycle detection](/dfs-cycle-detection/).

## Variants and improvements

- **Postorder, then reverse.** Append each finished vertex to an array and reverse the array at the end. Also $\Theta(n + m)$. See [depth-first orders](/depth-first-orders/).
- **Sort by finish time.** Run DFS with the clock, then sort the vertices by decreasing $f$. A counting sort on the keys $1, \ldots, 2n$ keeps this linear, but line L11 makes the sort unnecessary.
- **Kahn's algorithm.** Output a vertex of in-degree zero and remove it, repeatedly. Same cost, no recursion, and it gives a lexicographically smallest ordering with a priority queue. See [Kahn's algorithm](/kahns-algorithm/).
- **Strong components.** On a graph with cycles, the reverse postorder is still useful. The [Kosaraju-Sharir algorithm](/kosaraju-sharir/) uses it to order the second DFS, and the result is the components in a topological ordering of the [condensation graph](/condensation-graph/).
- **Incremental.** When edges arrive one at a time, recomputing the order each time costs $\Theta(n + m)$ per edge. See [incremental topological ordering](/incremental-topological-ordering/).

## When to use it

Use DFS topological sort when you already run a DFS, when you also want the cycle as a certificate, or when the graph is given as a function that lists the successors of a vertex, so that in-degrees are not known in advance. Use [Kahn's algorithm](/kahns-algorithm/) when the recursion depth is a problem, when you want the output from the front as it is produced, or when you want a specific ordering, such as the lexicographically smallest.

## Pitfalls

- **No cycle test.** Without line L8, the procedure returns a list for every graph. On a graph with a cycle it is not a topological ordering, and nothing warns about it.
- **One visited flag.** The cycle test must tell gray from black. An edge to a black vertex is a forward or cross edge and is harmless. With one "visited" flag, a diamond $0 \to 1$, $0 \to 2$, $1 \to 3$, $2 \to 3$ looks like a cycle.
- **Preorder instead of postorder.** Listing the vertices when they are discovered is not a topological ordering: with the edges $0 \to 1$ and $2 \to 1$ and the roots in the order $0, 1, 2$, the preorder is $0, 1, 2$, and $2 \to 1$ goes backwards.
- **Forgotten roots.** A single VISIT from one vertex lists only the vertices it reaches. Keep the loop of line L3.
- **Deep recursion.** A path of $10^5$ vertices overflows the default Python recursion limit.

## Implementations

## History

Cormen, Leiserson, Rivest and Stein present topological sort as an application of DFS, with the proof that a directed graph is acyclic exactly when a DFS finds no back edge. Dasgupta, Papadimitriou and Vazirani and Sedgewick and Wayne give the same method as ordering by decreasing post numbers, the reverse postorder. The older method of removing vertices with no predecessors is Kahn's, from 1962.

## References
