---
tag: YS8QZ8
kind: algorithm
slug: dfs-cycle-detection
name: DFS-based cycle detection
aliases:
- back-edge cycle detection
- three-colour cycle detection
area: graphs/paths-and-cycles
level: intro
summary: Depth-first search with white, gray and black vertices; the first edge to a gray vertex closes a cycle, and the parent edges give it. Linear time.
solves: [cycle-detection, cycle-detection-in-graph]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m), best: Θ(1)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true, certifying: true}
history:
  year: 1972
  people: [Robert Tarjan]
  note: Tarjan's 1972 paper made depth-first search with back edges the standard tool for linear-time graph algorithms, cycle tests among them.
prereqs: [depth-first-search, edge-classification, white-path-theorem]
see_also: [cycle-detection-in-graph, kahns-algorithm, topological-sort, union-find-connectivity, dfs-forest, iterative-depth-first-search, wait-for-graph]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.3, Depth-first search (white, gray and black vertices, the white-path theorem and edge classification) and Section 20.4, Topological sort (the lemma that a directed graph is acyclic if and only if DFS gives no back edge)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.1, Undirected graphs (the class Cycle) and Section 4.2, Directed graphs (the class DirectedCycle)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Section 3.3, Depth-first search in directed graphs (a directed graph has a cycle if and only if its DFS reveals a back edge)
  - paper: doi:10.1137/0201010
    title: Robert E. Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 146 to 160 (1972)
    locator: the whole paper
---

DFS-based cycle detection runs a [depth-first search](/depth-first-search/) that colours each vertex white (not seen), gray (on the current path) or black (finished), and it stops at the first edge from the current vertex to a gray vertex. That edge, with the tree edges on the path from the gray vertex down to the current vertex, is a [cycle](/simple-cycle/); if the search ends without such an edge, the graph is acyclic. It works on directed and undirected graphs, also on [multigraphs](/multigraph/) with [self-loops](/self-loop/), and it runs in $\Theta(n + m)$ time with $\Theta(n)$ extra space. It solves both [cycle detection](/cycle-detection/) and [finding a cycle](/cycle-detection-in-graph/).

## In plain words

Walk through the graph as far as you can, and keep a list of the points on the way from the start to where you are now. When you leave a point for good, take it off the list.

At each point, look at each arrow out of it. If the arrow goes to a point on the list, you have walked in a circle: the circle is the part of the list from that point to here, plus this arrow. If the arrow goes to a new point, go there. If it goes to a point that is already finished, ignore it, because nothing from there leads back to here.

In a graph with two-way lines, do not count the line you just came along as a way back, but do count a second line between the same two points.

## The problem

The input is a graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$ and $m$ edges, each with an identifier, and a flag that says if it is directed. An edge $e$ from $u$ to $v$ is in the list $\mathrm{Out}[u]$ as the pair $(e, v)$. In the undirected case, an edge $\{u, v\}$ with $u \ne v$ is in both $\mathrm{Out}[u]$ and $\mathrm{Out}[v]$, and a self-loop is in its list one time. Parallel edges and self-loops are allowed.

The output is a list of edge identifiers $(e_1, \ldots, e_k)$ that forms a cycle: the edges are distinct, they can be walked in this order (in the directed case, along their directions), the walk ends where it starts, and it passes no vertex twice. If there is no cycle, the output is NIL.

## The algorithm

Each vertex $v$ has a colour and the edge $pe[v]$ by which the search discovered it. For an edge $e$ from $u$ to $v$, we write $\mathrm{tail}(e) = u$, read in the direction in which the search used it.

```pseudo id=main
DFS-CYCLE(G)
L1  for each vertex u ∈ V do color[u] ← WHITE, pe[u] ← NIL
L2  for each vertex u ∈ V do
L3      if color[u] = WHITE then
L4          C ← VISIT(u); if C ≠ NIL then return C
L5  return NIL                                         ▷ G is acyclic

VISIT(u)
L6  color[u] ← GRAY
L7  for each (e, v) ∈ Out[u], skipping e = pe[u] if G is undirected do
L8      if color[v] = GRAY then return CYCLE(e, u, v)  ▷ e closes a cycle
L9      if color[v] = WHITE then pe[v] ← e; C ← VISIT(v); if C ≠ NIL then return C
L10 color[u] ← BLACK; return NIL

CYCLE(e, u, v)
L11 C ← (e); x ← u
L12 while x ≠ v do C ← (pe[x]) · C; x ← tail(pe[x])
L13 return C
```

Line L8 is the only new line compared with plain depth-first search. In a directed graph, an edge to a gray vertex is a back edge in the sense of [edge classification](/edge-classification/), and an edge to a black vertex is a forward or cross edge, which line L9 ignores.

In an undirected graph, line L7 skips one edge: the tree edge by which $u$ was discovered. It is skipped by its identifier, not by its other end, so a second edge between $u$ and its parent is not skipped, and it closes a cycle of length 2. A self-loop at $u$ meets $u$ gray at line L8 and gives the cycle $(e)$ of length 1, in both cases.

## Example

The directed graph has 6 vertices and the edges below; each list $\mathrm{Out}[u]$ is in the order of the identifiers.

| edge | $e_0$ | $e_1$ | $e_2$ | $e_3$ | $e_4$ | $e_5$ | $e_6$ |
|---|---|---|---|---|---|---|---|
| arc | $0 \to 1$ | $0 \to 2$ | $1 \to 3$ | $2 \to 3$ | $3 \to 4$ | $4 \to 2$ | $5 \to 4$ |

| step | current vertex | edge scanned | colour of the head | action |
|---|---|---|---|---|
| 1 | 0 | $e_0$ | 1 white | $pe[1] = e_0$, visit 1 |
| 2 | 1 | $e_2$ | 3 white | $pe[3] = e_2$, visit 3 |
| 3 | 3 | $e_4$ | 4 white | $pe[4] = e_4$, visit 4 |
| 4 | 4 | $e_5$ | 2 white | $pe[2] = e_5$, visit 2 |
| 5 | 2 | $e_3$ | 3 gray | cycle |

At step 5 the gray vertices are $0, 1, 3, 4, 2$, the current path. CYCLE$(e_3, 2, 3)$ starts with $C = (e_3)$ and $x = 2$. Then $pe[2] = e_5$ gives $C = (e_5, e_3)$ and $x = 4$, and $pe[4] = e_4$ gives $C = (e_4, e_5, e_3)$ and $x = 3$, which ends the loop. The output is the cycle $3 \to 4 \to 2 \to 3$. The edges $e_1$ and $e_6$ are never scanned, and vertex 5 is never visited: the search stops at the first cycle.

Without the edge $e_5$ the search finds no gray head. It finishes 4, 3, 1, then scans $e_1$ from 0 and visits 2, whose edge $e_3$ goes to the black vertex 3 and is ignored. Then it visits 5, whose edge goes to the black vertex 4. The output is NIL, and the reverse of the finish order, $5, 0, 2, 1, 3, 4$, is a [topological ordering](/topological-ordering/) that proves it.

For an undirected example, take $e_0 = \{0, 1\}$, $e_1 = \{1, 2\}$, $e_2 = \{2, 3\}$ and $e_3 = \{3, 1\}$. The search goes from 0 to 1 to 2 to 3. At 3 it skips $e_2$, its own tree edge, and scans $e_3$ to the gray vertex 1. The output is $(e_1, e_2, e_3)$.

## Correctness

The full proof is in the [correctness proof](proofs/correctness/). It rests on one fact of depth-first search: at each moment the gray vertices, in the order in which they became gray, form a path of tree edges, and the current vertex is the last one. So when an edge $e$ goes from the current vertex $u$ to a gray vertex $v$, the walk up the $pe$ edges from $u$ reaches $v$, and these tree edges with $e$ form a cycle with no repeated vertex.

If the search ends with NIL, there is no cycle. For a directed graph, suppose there is a cycle, and let $v$ be its first vertex to become gray. When $v$ becomes gray, the rest of the cycle is white, so by the [white-path theorem](/white-path-theorem/) the vertex $w$ before $v$ on the cycle becomes a descendant of $v$, and $w$ scans its edge to $v$ while $v$ is still gray. Line L8 then returns. For an undirected graph, if NIL is returned then each edge was either a tree edge or met at a black vertex. An edge met at a black vertex was already scanned from that vertex, so all edges are tree edges, and tree edges form a forest, which has no cycle.

## Complexity

Each vertex becomes gray once, so VISIT runs at most once per vertex, and each list $\mathrm{Out}[u]$ is scanned at most once. Building the lists and the scans take $\Theta(n + m)$ time in the worst case. CYCLE takes time proportional to the length of the cycle, at most $n$. The colours, the $pe$ edges and the stack take $\Theta(n)$ extra space, besides the lists.

The search stops at the first cycle, so it can be much faster than the worst case: a self-loop at vertex 0 is found in $O(1)$ time after the lists are built. In an undirected graph the search stops after it has scanned at most $n$ list entries that are not cycle edges: each scan of a non-tree edge returns, and there are at most $n - 1$ tree edges. So on an undirected graph that is given as lists the search takes $O(n)$ time, even if $m$ is much larger than $n$.

## Properties

- **Certifying.** A cycle is returned as a list of edges that a user can check. When the answer is NIL, the reverse finish order is a topological ordering in the directed case, and the parent edges form a spanning forest equal to $E$ in the undirected case.
- **Not shortest.** The cycle can be much longer than the shortest cycle of the graph. On the cycle $0 \to 1 \to \cdots \to n-1 \to 0$ with the extra edge $1 \to 0$ last in $\mathrm{Out}[1]$, it returns the cycle of length $n$, not the cycle $0 \to 1 \to 0$.
- **Deterministic.** The output depends on the order of the vertices and of each list.
- **Local.** Run from one vertex $s$ only, it finds a cycle among the vertices reachable from $s$ if one exists.

## Variants and improvements

- **Undirected without colours.** For an undirected graph, two colours suffice: a scanned non-parent edge to any visited vertex closes a cycle. A [union-find](/union-find-connectivity/) structure does the same test on a stream of edges.
- **Topological sort with a certificate.** Record the finish order in line L10. If NIL is returned, the reverse finish order is a [topological sort](/topological-sort/); otherwise the cycle shows that none exists. [Kahn's algorithm](/kahns-algorithm/) gives the same pair of answers without recursion.
- **All back edges.** Do not stop at line L8; record the edge and go on. Each back edge then gives a cycle, and in an undirected graph the back edges give the [fundamental cycles](/fundamental-cycle/) of the DFS tree, which form a [cycle basis](/cycle-basis/).
- **Cycle through a vertex.** In a directed graph, a vertex lies on a cycle if and only if its [strong component](/strongly-connected-components/) has more than one vertex or it has a self-loop.
- **Incremental graphs.** When edges arrive one at a time and the graph must stay acyclic, dynamic topological order structures avoid a new search after each edge.

## When to use it

Use it to test a dependency graph, a state machine or a wait-for graph for cycles and to show the cycle that was found. It is the simplest method with linear time, and it gives the cycle with no extra work. For very deep graphs in a language with a small call stack, use the version with an explicit stack, as the implementation here does, or Kahn's algorithm. To find a short cycle, use breadth-first search instead; see the [shortest cycle problem](/shortest-cycle-problem/).

## Pitfalls

- **Two colours in a directed graph.** An edge to a black vertex is not a cycle in a directed graph. A visited flag alone reports a cycle in the acyclic graph $0 \to 1$, $0 \to 2$, $2 \to 1$.
- **Skipping the parent vertex in an undirected multigraph.** The skip must use the edge identifier. If it skips every edge back to the parent vertex, two parallel edges are not seen as a cycle.
- **Not skipping the parent edge.** In an undirected graph each edge is in two lists, so without the skip every tree edge looks like a cycle of length 2.
- **Forgetting the outer loop.** A search from one vertex tests only the part of the graph reachable from it. Lines L2 to L4 start a search from every vertex that is still white.
- **Recursion depth.** The recursive form can go $n$ calls deep, which overflows the default stack in many languages on a long path.

## Implementations

## History

Tarjan's 1972 paper showed that depth-first search with its back edges gives linear-time algorithms for many graph problems, and the cycle test became one of the standard examples. The method itself is older: it is a direct use of Trémaux's maze search from the nineteenth century, and Knuth's 1968 treatment of topological sorting in the first volume of The Art of Computer Programming already discusses how to report a loop when the input has one. The names white, gray and black for the three states are the notation of the textbook of Cormen, Leiserson, Rivest and Stein.

## References
