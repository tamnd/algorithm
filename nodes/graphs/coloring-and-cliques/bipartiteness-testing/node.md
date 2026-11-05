---
tag: S82K2H
kind: algorithm
slug: bipartiteness-testing
name: Bipartiteness testing
aliases:
- Testing bipartiteness
area: graphs/coloring-and-cliques
level: intro
summary: Decides whether a graph is two-colorable by running breadth-first search and checking whether any edge joins two vertices in the same layer.
solves: [bipartite-graph-test]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [breadth-first-search, bipartite-graph, bipartite-odd-cycle-theorem]
see_also: [bipartite-graph-test, bipartiteness-check, bipartite-graph-recognition, bfs-layers, dsu-with-parity, lowest-common-ancestor, graph-coloring]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 3.4, Testing bipartiteness, an application of breadth-first search (the coloring by layers, and the odd cycle through the lowest common ancestor)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.1, Undirected graphs (two-colorability as an application of graph search)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 1.2, Paths, cycles and trails (König's characterization of bipartite graphs by odd cycles)
---

Bipartiteness testing decides whether an undirected graph is [bipartite](/bipartite-graph/), that is, whether its vertices have a proper 2-[coloring](/graph-coloring/). It runs a [breadth-first search](/breadth-first-search/) from each uncolored vertex, colors each vertex by the parity of its layer, and checks each edge. If no edge joins two vertices of one color, the colors are the answer. If one does, its two ends lie in the same layer, and the two tree paths to their common ancestor close an odd cycle, which proves that no 2-coloring exists. The time is $\Theta(n + m)$ with [adjacency lists](/adjacency-list/).

## In plain words

Pick a vertex and paint it white. Paint all its neighbors black. Paint all their unpainted neighbors white, and so on, in rings around the start. This is a breadth-first search, and each vertex gets the color of the parity of its ring.

Each line of the graph joins two neighboring rings or two vertices of the same ring. Lines between neighboring rings are always fine. A line inside one ring joins two vertices of the same color. Then you follow both ends back toward the start until the two routes meet. The two routes and the line form a loop with an odd number of lines, and no painting with two colors can handle such a loop. So the answer is no, and the loop shows why.

## The problem

The input is an undirected graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, as adjacency lists. Self-loops and parallel edges are allowed. The output is either a proper 2-coloring $c : V \to \{0, 1\}$, or an odd cycle of $G$. This is the search version of the [two-colorability problem](/bipartite-graph-test/).

## The algorithm

```pseudo id=main
BIPARTITE-TEST(G)
L1  for each vertex v do color[v] ← NIL, parent[v] ← NIL
L2  for each vertex s with color[s] = NIL do
L3      color[s] ← 0, Q ← a queue that holds only s
L4      while Q is not empty do
L5          u ← DEQUEUE(Q)
L6          for each neighbor w of u do
L7              if color[w] = NIL then color[w] ← 1 − color[u], parent[w] ← u, ENQUEUE(Q, w)
L8              else if color[w] = color[u] then return ODD-CYCLE(u, w)
L9  return color

ODD-CYCLE(u, w)                       ▷ u and w are in the same BFS layer
L10 x ← u, y ← w; while x ≠ y do x ← parent[x], y ← parent[y]   ▷ now x = y = z
L11 return the path u → … → z, then the path z → … → w   ▷ the edge {w, u} closes it
```

Lines L3 to L8 are breadth-first search from $s$, with one more test. The parent pointers form a [BFS tree](/bfs-tree/) of each component. Line L8 fires on the first edge whose two ends have the same color. Line L10 climbs from $u$ and $w$ in lockstep until the two climbs meet at their lowest common ancestor $z$. A self-loop at $u$ gives $w = u$, and the cycle is the single vertex $u$, of length 1.

## Example

The graph has the vertices $0, \ldots, 6$ and the edges $01, 02, 13, 24, 35, 45, 56$. It is a 6-cycle $0, 1, 3, 5, 4, 2$ with a pendant vertex 6. The adjacency lists are in the order of this edge list.

| step | dequeued $u$ | new vertices and their colors | queue after the step |
|---|---|---|---|
| start | | $0 \mapsto 0$ | 0 |
| 1 | 0 | $1 \mapsto 1$, $2 \mapsto 1$ | 1, 2 |
| 2 | 1 | $3 \mapsto 0$ | 2, 3 |
| 3 | 2 | $4 \mapsto 0$ | 3, 4 |
| 4 | 3 | $5 \mapsto 1$ | 4, 5 |
| 5 | 4 | none; the edge 45 has colors 0 and 1 | 5 |
| 6 | 5 | $6 \mapsto 0$ | 6 |
| 7 | 6 | none | empty |

The output is $c = (0, 1, 1, 0, 0, 1, 0)$, with the sides $\{0, 3, 4, 6\}$ and $\{1, 2, 5\}$.

Now add the edge $34$, and keep the lists in the order $01, 02, 13, 24, 35, 34, 45, 56$. Steps 1 to 3 are the same. In step 4, $u = 3$ scans 1, then 5 (new, color 1), then 4, which has color 0 like 3. Line L8 calls ODD-CYCLE$(3, 4)$. The climb goes $3 \to 1 \to 0$ and $4 \to 2 \to 0$ and meets at $z = 0$. The output is the cycle $3, 1, 0, 2, 4$, closed by the edge $43$. It has 5 vertices.

## Correctness

**Theorem.** If BIPARTITE-TEST returns at line L9, the array color is a proper 2-coloring of $G$. If it returns at line L8, the output is a closed walk of odd length in $G$, and a simple cycle when $G$ has no self-loop. In both cases the answer is right: $G$ is bipartite if and only if line L9 is reached.

The key invariant is that within the search from $s$, $\mathrm{color}[v]$ is the parity of the BFS distance $\delta(s, v)$. An edge of $G$ joins two vertices whose distances from $s$ differ by at most 1. So two adjacent vertices of the same color have the same distance, and the climb of line L10 takes the same number of steps from both. The cycle has length $2(\delta(s, u) - \delta(s, z)) + 1$, which is odd. The two tree paths share only $z$, so the cycle is simple. An odd cycle rules out every 2-coloring, by the [odd cycle theorem](/bipartite-odd-cycle-theorem/). If line L9 is reached, each edge was tested at line L8 from at least one end after both ends had colors, so no edge has two ends of one color. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model, with the graph as adjacency lists.

- Line L1 takes $\Theta(n)$ time, and the loop of line L2 looks at each vertex once.
- Each vertex is enqueued at most once, at line L3 or line L7, and dequeued at most once. So lines L6 to L8 scan each adjacency list at most once, $O(m)$ steps in total for the $2m$ list entries.
- ODD-CYCLE runs at most once. Each climb step moves both $x$ and $y$ one layer up, so it takes at most $n$ steps.

The time is $O(n + m)$. It is $\Theta(n + m)$ in the worst case, when $G$ is bipartite and all lists are scanned. The best case is $\Theta(n)$: a graph with a self-loop at vertex 0 stops at once after line L1. The extra space is $\Theta(n)$ for the arrays and the queue.

## Properties

- **Certifying.** Each answer comes with a proof that can be checked in linear time: the coloring, or the odd cycle. This makes the algorithm a standard example of a [certifying algorithm](/certifying-algorithms/).
- **Short odd cycle.** The cycle found has length at most $2\delta(s, u) + 1$, so at most $2r + 1$ where $r$ is the radius of the BFS from $s$. It is not always a shortest odd cycle of $G$.
- **All components.** The loop of line L2 restarts the search in each [connected component](/connected-components/). A bipartite graph with $c$ components has $2^c$ proper 2-colorings, and the output is the one with color 0 at the smallest vertex of each component.
- **Any search order works.** The coloring step needs only that each new vertex gets the color opposite to its parent. The odd cycle step uses the layers of BFS; with [depth-first search](/depth-first-search/), the odd cycle is the tree path between the two ends of the bad edge, which is a back edge.

## Variants and improvements

- **Depth-first version.** Color by DFS. A conflicting edge is a back edge from $u$ to an ancestor $w$ with the same color, and the tree path from $w$ to $u$ plus the edge is an odd cycle. This is the version in Sedgewick and Wayne.
- **Union-find with parity.** Process the edges one by one with a [union-find](/disjoint-set/) that stores the parity of each vertex relative to its root ([DSU with parity](/dsu-with-parity/)). An edge inside one set with equal parities closes an odd cycle. This works online, in $O(m\, \alpha(n))$ time.
- **Dynamic graphs.** Under both insertions and deletions, see [dynamic bipartiteness](/dynamic-bipartiteness/).
- **Testing a bipartite input.** If $G$ is promised to be bipartite, the coloring of line L7 alone, without line L8, gives the two sides.

## When to use it

Use it whenever you need to know whether a graph splits into two sides, or need the sides themselves, for example before a [bipartite matching](/bipartite-matching/) algorithm. Use the BFS version when you want a short odd cycle as a certificate. Use the union-find version when edges arrive one at a time, or when the graph is given as an edge list and you do not want to build adjacency lists. For three or more colors there is no such method; see [graph coloring](/graph-coloring/).

## Pitfalls

- **Searching only from vertex 0.** A disconnected graph needs the loop of line L2. With a single search, a non-bipartite component that does not contain vertex 0 is never seen.
- **Testing only tree edges.** The check of line L8 must run on every scanned edge, including edges to vertices that are already colored. Without line L8 the program colors every graph and always answers yes.
- **Climbing unequal depths.** Line L10 is correct only because $u$ and $w$ are in the same BFS layer. With DFS colors, the two ends of a bad edge are at different depths, and the climb must use the depths, or walk from $u$ up to $w$.
- **Forgetting self-loops.** A self-loop $\{v, v\}$ makes $G$ non-bipartite. Line L8 catches it, as $w = u$ has the color of $u$, but code that skips $w = u$ as "not a real neighbor" misses it.

## Implementations

## History

König proved in 1936 that a graph is bipartite exactly when it has no odd cycle (see the [odd cycle theorem](/bipartite-odd-cycle-theorem/)). The linear-time test by graph search is standard textbook material, and its first publication is not clear. Kleinberg and Tardos present the BFS version, with the odd cycle through the common ancestor, as a basic application of breadth-first search.

## References
