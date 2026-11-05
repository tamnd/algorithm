---
tag: 97Q3XX
kind: concept
slug: edge-classification
name: Edge classification in DFS
aliases:
- tree, back, forward and cross edges
area: graphs/traversal
level: core
summary: Tree, back, forward and cross edges, distinguished by DFS timestamps in directed graphs.
prereqs: [discovery-and-finish-times, parenthesis-theorem]
see_also: [white-path-theorem, dfs-forest, topological-ordering-theorem, topological-sort, cycle-detection, articulation-point, strongly-connected-components, bfs-layers]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.3, Depth-first search (the subsection Classification of edges, the colour rule and the theorem that an undirected DFS has only tree and back edges), and Section 20.4 (no back edges in an acyclic graph)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 3, Section 3.3.1, Types of edges (the table of pre and post orders for each type)
  - paper: doi:10.1137/0201010
    title: Robert E. Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 146 to 160 (1972)
    locator: the sections on the palm tree of an undirected graph and on directed graphs (fronds and cross-links)
---

Edge classification sorts the edges of a graph into four types by their place relative to the [depth-first forest](/dfs-forest/) of a [depth-first search](/depth-first-search/): tree edges, back edges, forward edges and cross edges. DFS can label each edge at the moment it scans the edge, by the colour of the far end, and afterwards by comparing the [discovery and finish times](/discovery-and-finish-times/) of the two ends. In an undirected graph only tree edges and back edges occur. Back edges are the edges that close cycles, so this classification is the base of [cycle detection](/cycle-detection/), [topological sort](/topological-sort/), [articulation points](/articulation-point/) and [strong components](/strongly-connected-components/).

## In plain words

Depth-first search builds a family tree: each vertex has the vertex it came from as its parent. Every edge of the graph now has a place relative to this tree.

Some edges are the tree itself. Some go from a vertex up to one of its ancestors: these close a loop. Some go from a vertex down to a descendant, but skip over the tree path: these are shortcuts. The rest go sideways, to a vertex that is neither above nor below, in an earlier part of the tree or in an earlier tree.

The search can tell the type at once, by the state of the vertex at the other end: not yet seen, still open, or already done.

## The idea

Let $G = (V, E)$ be a directed graph and fix one run of DFS$(G)$, with its forest, its parents $\pi$ and its times $d$ and $f$. Each vertex is a descendant of itself. An edge $(u, v) \in E$ is

- a **tree edge** if $\pi[v] = u$;
- a **back edge** if $v$ is an ancestor of $u$ (this includes a self-loop $u = v$);
- a **forward edge** if $v$ is a proper descendant of $u$ and $(u, v)$ is not a tree edge;
- a **cross edge** in all other cases: neither end is an ancestor of the other.

The four types do not overlap, and each edge has one of them. The type depends on the run: another order of the lists gives another forest and other types.

**Colour rule.** When the call DFS-VISIT$(u)$ examines the edge $(u, v)$ at line L7, let $c$ be the colour of $v$ at that moment. Then the edge is a tree edge if $c$ is white, a back edge if $c$ is gray, a forward edge if $c$ is black and $d[u] < d[v]$, and a cross edge if $c$ is black and $d[v] < d[u]$.

**Time rule.** By the [parenthesis theorem](/parenthesis-theorem/), the four times of the two ends of an edge $(u, v)$, $u \ne v$, are in one of these orders:

| type | order of the times |
|---|---|
| tree or forward | $d[u] < d[v] < f[v] < f[u]$ |
| back | $d[v] < d[u] < f[u] < f[v]$ |
| cross | $d[v] < f[v] < d[u] < f[u]$ |

The fourth order, $d[u] < f[u] < d[v] < f[v]$, never occurs for an edge. So a cross edge always goes from a vertex to a vertex that finished earlier, and for each edge that is not a back edge, $f[v] < f[u]$.

**Proof of the colour rule.** Look at the moment when DFS-VISIT$(u)$ examines $(u, v)$. The call of $u$ is the top call of the stack.

- *White.* Line L9 calls DFS-VISIT$(v)$ after line L8 sets $\pi[v] = u$, so the edge is a tree edge. Conversely, $\pi[v]$ is set to $u$ only in this way.
- *Gray.* The call of $v$ is active. The gray vertices are the vertices on the call stack, and each is the parent of the next one above it, so they form the tree path from a root to $u$. So $v$ is an ancestor of $u$, and the edge is a back edge.
- *Black, $d[u] < d[v]$.* The vertex $v$ was discovered after $u$ and has finished, so $d[u] < d[v] < f[v]$, and $f[v]$ is before the present moment, which is before $f[u]$. By the corollary of the parenthesis theorem, $v$ is a proper descendant of $u$. It was not white when the edge was examined, so the edge is not a tree edge: it is a forward edge.
- *Black, $d[v] < d[u]$.* The vertex $v$ is finished and $u$ is not, so $f[v] < f[u]$. If $d[u] < f[v]$, then $u$ was discovered while $v$ was gray, so $u$ is a descendant of $v$ and the parenthesis theorem gives $f[u] < f[v]$, which is false. So $d[v] < f[v] < d[u] < f[u]$. The intervals are disjoint, neither vertex is an ancestor of the other, and the edge is a cross edge.

The four cases cover all colours, and they give four different types, so the colour rule and the definition agree. The table follows from the same cases. The fourth order is impossible because $u$ examines the edge before $f[u]$, and at that moment $v$ is either discovered already or is discovered at once, so $d[v] < f[u]$. $\square$

**Undirected graphs.** In an undirected graph, the edge $\{u, v\}$ is in both lists, and it gets its type when DFS first examines it, from either end. Then:

**Theorem.** In a DFS of an undirected graph, each edge is a tree edge or a back edge.

*Proof.* Let $\{u, v\}$ be an edge with $d[u] < d[v]$. The list of $u$ contains $v$, so $v$ is discovered before $u$ finishes, and by the corollary of the parenthesis theorem (or the [white-path theorem](/white-path-theorem/)), $v$ is a descendant of $u$. If DFS first examines the edge from $u$, then $v$ is still white at that moment: else $v$ would have been discovered while $u$ was gray, its call would have ended before $u$ continues, and during its call $v$ would have examined the edge first. So the edge is a tree edge. If DFS first examines the edge from $v$, then $u$ is gray at that moment, because it is an ancestor of $v$ whose call is still active, and the edge is a back edge. $\square$

**Breadth-first search.** A BFS forest has a similar but simpler classification by [layers](/bfs-layers/). In an undirected graph, each non-tree edge joins two vertices in the same layer or in adjacent layers. In a directed graph, an edge $(u, v)$ always has $\mathrm{dist}[v] \le \mathrm{dist}[u] + 1$, and BFS never produces a forward edge.

## Examples

Run DFS on the directed graph with vertices 0 to 6 and the lists $0: 1, 3, 2$; $1: 2$; $2: 0$; $3: 2, 4$; $4$: none; $5: 4, 6$; $6: 5$. The times are $d = (1, 2, 3, 6, 7, 11, 12)$ and $f = (10, 5, 4, 9, 8, 14, 13)$ for the vertices 0 to 6.

| edge | colour of the far end when examined | times | type |
|---|---|---|---|
| $0 \to 1$ | white | | tree |
| $1 \to 2$ | white | | tree |
| $2 \to 0$ | gray | $d[0] < d[2] < f[2] < f[0]$ | back |
| $0 \to 3$ | white | | tree |
| $3 \to 2$ | black, $d[2] = 3 < d[3] = 6$ | $f[2] = 4 < d[3] = 6$ | cross |
| $3 \to 4$ | white | | tree |
| $0 \to 2$ | black, $d[0] = 1 < d[2] = 3$ | $[3, 4] \subset [1, 10]$ | forward |
| $5 \to 4$ | black, $d[4] = 7 < d[5] = 11$ | $f[4] = 8 < d[5] = 11$ | cross |
| $5 \to 6$ | white | | tree |
| $6 \to 5$ | gray | $[12, 13] \subset [11, 14]$ | back |

There are 5 tree edges, 2 back edges, 1 forward edge and 2 cross edges. The back edges close the cycles $0, 1, 2$ and $5, 6$. The cross edge $5 \to 4$ goes between the two trees, and $3 \to 2$ goes inside one tree, from a later branch to an earlier one.

**The order matters.** If the list of 0 is $2, 1, 3$ instead, DFS goes from 0 to 2 first. Then $0 \to 2$ is a tree edge, $1 \to 2$ is a cross edge, and there is no forward edge. The number of back edges can also change, but a graph with a cycle always has at least one, and a graph without cycles never has one.

**Undirected example.** On the cycle with the edges $\{0,1\}$, $\{1,2\}$, $\{2,3\}$, $\{3,0\}$ and sorted lists, DFS from 0 goes $0, 1, 2, 3$ by tree edges, and when 3 examines $\{3, 0\}$, vertex 0 is gray, so this edge is a back edge. No forward or cross edge appears.

## Where it is used

- **Cycles.** A directed graph is acyclic if and only if a DFS finds no back edge. The [topological ordering theorem](/topological-ordering-theorem/) proves this, and [cycle detection](/cycle-detection/) uses it.
- **[Topological sort](/topological-sort/).** Without back edges, $f[v] < f[u]$ for each edge $(u, v)$, so the decreasing order of finish times is a topological ordering.
- **Cut vertices and bridges.** In an undirected graph there are only tree and back edges. A [low-link](/low-link/) value records the highest ancestor that a subtree reaches by one back edge, which gives [articulation points](/articulation-point/) and [bridges](/bridge-finding/).
- **Strong components.** [Tarjan's algorithm](/tarjan-scc/) treats back edges and cross edges into the current stack in the same way, and ignores cross edges to finished components.
- **Bipartite graphs.** In an undirected graph, a back edge between two vertices whose depths have the same parity closes an odd cycle. See [bipartiteness checking](/bipartiteness-check/).

## References
