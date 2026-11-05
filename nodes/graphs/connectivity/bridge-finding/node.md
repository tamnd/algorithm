---
tag: 4K6X3Z
kind: problem
slug: bridge-finding
name: Bridge finding
aliases:
- Cut edge finding
area: graphs/connectivity
level: intro
summary: Find all edges whose removal increases the number of connected components.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m)}
prereqs: [bridge, connected-components]
see_also: [hopcroft-tarjan-biconnectivity, articulation-point-finding, two-edge-connected-components, low-link, online-bridge-finding, strong-orientation, edge-connectivity]
sources:
  - paper: doi:10.1016/0020-0190(74)90003-9
    title: Robert E. Tarjan, A note on finding the bridges of a graph, Information Processing Letters 2(6), 160 to 161 (1974)
    locator: the whole note (a linear-time bridge test on a spanning tree with preorder numbers)
  - paper: doi:10.1137/0201010
    title: Robert E. Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 146 to 160 (1972)
    locator: Section 4, low points in a depth-first search tree
  - paper: doi:10.1016/j.ipl.2013.01.016
    title: Jens M. Schmidt, A simple test on 2-vertex- and 2-edge-connectivity, Information Processing Letters 113(7), 241 to 244 (2013)
    locator: the chain decomposition and the bridge test (an edge is a bridge if and only if it is in no chain)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 20, Problem 20-2, Articulation points, bridges, and biconnected components (Problem 22-2 in the third edition)
---

Bridge finding is the problem of listing every [bridge](/bridge/) of an [undirected graph](/undirected-graph/): every edge whose removal increases the number of [connected components](/connected-components/). An edge is a bridge if and only if it lies on no cycle. The obvious method removes each edge in turn and counts the components, in $\Theta(m(n + m))$ time. One [depth-first search](/depth-first-search/) with [low-link](/low-link/) values does it in $\Theta(n + m)$ time, which is optimal. The bridges split the graph into its [2-edge-connected components](/two-edge-connected-components/), and they are the single links whose failure cuts a network.

## In plain words

A network of towns and roads may have a road that is the only link between two parts of the network. If that road is closed, the network falls apart. The task is to find all such roads.

A road is such a link exactly when no round trip uses it. So walk the network once, deep first. Each road that the walk takes into a new town is a tree road. Each other road is a short cut back to a town that the walk saw earlier. A tree road is a weak link when no short cut from the part of the walk below it climbs back above it. One walk finds every weak link.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $V = \{0, 1, \ldots, n-1\}$ and $m = |E|$, in [adjacency lists](/adjacency-list/). $E$ is a multiset: parallel edges and [self-loops](/self-loop/) are allowed, and each edge has an identifier, so two parallel edges are two different edges. The graph need not be connected.

**Output.** The set

$$\mathrm{Br}(G) = \{\, e \in E : c(G - e) > c(G) \,\},$$

where $G - e$ is $G$ without the edge $e$ and $c(H)$ is the number of components of $H$. Removing one edge raises $c$ by at most one, so $e \in \mathrm{Br}(G)$ means $c(G - e) = c(G) + 1$.

**Loops and parallel edges.** A loop is never a bridge, since its two ends are the same vertex. Two or more parallel edges between $u$ and $v$ are never bridges, since each one of them closes a cycle with another. So parallel edges change the answer: the graph with the two vertices 0 and 1 and one edge has one bridge, and the graph with two copies of that edge has none. An algorithm that sees only which pairs of vertices are adjacent gives the wrong answer here.

## Variants

- **Decision.** Is $\mathrm{Br}(G)$ empty? For a connected graph with at least two vertices, this asks whether $G$ is [2-edge-connected](/two-edge-connected-graph/).
- **Components.** Output the [2-edge-connected components](/two-edge-connected-components/): the components of $G$ minus all bridges. Contracting each one to a vertex gives the *bridge tree* (a forest if $G$ is not connected), whose edges are the bridges.
- **Vertices instead of edges.** [Articulation point finding](/articulation-point-finding/) lists the vertices whose removal disconnects the graph.
- **Sets of edges.** The smallest set of edges whose removal disconnects the graph is the [edge connectivity](/edge-connectivity/) problem. Bridges are the case of size 1.
- **Online and dynamic.** Keep the bridges while edges are added ([online bridge finding](/online-bridge-finding/)), or added and deleted ([dynamic biconnectivity](/dynamic-biconnectivity/) and [dynamic connectivity](/dynamic-connectivity/)).
- **Directed graphs.** A *strong bridge* is an edge whose removal increases the number of [strongly connected components](/strongly-connected-components/). It is a different problem.

## Examples

The graph has $n = 7$ vertices and 10 edges: a triangle $0, 1, 2$ with a second copy of $\{0, 1\}$, the edge $\{2, 3\}$, a triangle $3, 4, 5$, the edge $\{5, 6\}$, and a loop at 6. A depth-first search from 0, with the lists in increasing order, visits $0, 1, 2, 3, 4, 5, 6$ in this order along one path, so $d[v] = v + 1$. The tree edge into $v$ is the edge from $v - 1$; for $v = 1$ it is the first copy of $\{0, 1\}$.

| tree edge | $\{0,1\}$ | $\{1,2\}$ | $\{2,3\}$ | $\{3,4\}$ | $\{4,5\}$ | $\{5,6\}$ |
|---|---|---|---|---|---|---|
| lower end $v$ | 1 | 2 | 3 | 4 | 5 | 6 |
| $d[\text{parent}]$ | 1 | 2 | 3 | 4 | 5 | 6 |
| $\mathrm{low}[v]$ | 1 | 1 | 4 | 4 | 4 | 7 |
| bridge | no | no | yes | no | no | yes |

A tree edge from the parent $u$ to $v$ is a bridge if and only if $\mathrm{low}[v] > d[u]$. So $\mathrm{Br}(G) = \{\{2, 3\}, \{5, 6\}\}$. The second copy of $\{0, 1\}$ is a back edge from 1 to 0, which is one reason that $\mathrm{low}[1] = 1$; the loop at 6 gives $\mathrm{low}[6]$ nothing new, and the loop and all edges that are not tree edges are never bridges.

More small cases:

| graph | $\mathrm{Br}(G)$ |
|---|---|
| a tree, or a forest | all edges |
| a cycle, or a [complete graph](/complete-graph/) $K_n$ with $n \ge 3$ | empty |
| two triangles joined by one edge | that edge |
| two vertices with two parallel edges | empty |
| one vertex with a loop | empty |
| no edges at all | empty |

## Known algorithms

| algorithm | time | remark |
|---|---|---|
| Remove each edge and count the components | $\Theta(m(n + m))$ | $m$ runs of a [component search](/connected-components/) |
| Low points ([Hopcroft-Tarjan](/hopcroft-tarjan-biconnectivity/)) | $\Theta(n + m)$ | one depth-first search; a tree edge $(u, v)$ is a bridge if and only if $\mathrm{low}[v] > d[u]$ |
| Covering counts | $\Theta(n + m)$ | one depth-first search; for each back edge from $x$ up to $y$, add 1 at $x$ and $-1$ at $y$; the sum over the subtree of $v$ counts the back edges over the tree edge into $v$, and the edge is a bridge if and only if the sum is 0 |
| Tarjan's note (1974) | $\Theta(n + m)$ | any [spanning tree](/spanning-tree/) with preorder numbers and subtree sizes, not only a depth-first one |
| Chain decomposition (Schmidt, 2013) | $\Theta(n + m)$ | split the edges into chains along a depth-first search; an edge is a bridge if and only if it is in no chain |

All of them must skip the tree edge to the parent by its identifier, not by the parent vertex. If the search skips every edge to the parent vertex, a parallel copy of the tree edge is never seen as a back edge, and the tree edge is wrongly reported as a bridge.

The low-point test holds because every edge that is not a tree edge of a depth-first search joins a vertex to one of its ancestors ([edge classification](/edge-classification/)). So the tree edge into $v$ lies on a cycle if and only if some back edge leaves the subtree of $v$ and lands at $u$ or above, which is $\mathrm{low}[v] \le d[u]$. The full proof is on the algorithm page.

## Bounds

**Upper bound.** $O(n + m)$ time in the [word RAM](/word-ram/) model with adjacency lists, by one depth-first search.

**Lower bound.** Each deterministic algorithm reads $\Omega(n + m)$ list entries in the worst case.

*Proof.* For the term $m$: let $A$ and $B$ be two disjoint copies of the [complete graph](/complete-graph/) $K_t$ with $t \ge 3$, joined by one edge $e = \{a, b\}$ with $a \in A$ and $b \in B$. Then $e$ is a bridge. Suppose the algorithm reads neither list entry of an edge $\{a_1, a_2\}$ of $A$ and neither entry of an edge $\{b_1, b_2\}$ of $B$. Rewrite these four unread entries so that the two edges become $\{a_1, b_2\}$ and $\{b_1, a_2\}$. In the new graph, $A$ and $B$ are still connected inside, because $K_t$ minus one edge is connected, and they are now joined by a second edge, so $e$ lies on a cycle and is no longer a bridge. The algorithm sees the same input and gives the same output, so it is wrong on one of the two graphs. Hence it reads an entry of every edge of $A$ or of every edge of $B$, which is at least $t(t-1)/2$ entries, a constant fraction of $m$. For the term $n$: if two isolated vertices $x$ and $y$ have unread lists, adding the edge $\{x, y\}$ creates a bridge without changing what the algorithm reads. So all but one of the isolated vertices are read. $\square$

**Space.** $\Theta(n)$ words for the times, the low values and the stack of the search, in addition to the input. The stack can be $n$ deep, so programs use an explicit stack instead of recursion.

## Reductions

- **To connectivity, $m$ times.** $e \in \mathrm{Br}(G)$ if and only if $G - e$ has more components than $G$. This is the brute-force method.
- **To articulation points.** Subdivide each edge $e = \{u, v\}$ that is not a loop by a new vertex $w_e$. Then $e$ is a bridge of $G$ if and only if $w_e$ is an [articulation point](/articulation-point/) of the new graph. The new graph has at most $n + m$ vertices and $2m$ edges, so this costs $O(n + m)$.
- **From blocks.** Given the [biconnected components](/biconnected-components/), the bridges are the blocks with exactly one edge that is not a loop.
- **To 2-edge-connectivity.** A connected graph with $n \ge 2$ is [2-edge-connected](/two-edge-connected-graph/) if and only if $\mathrm{Br}(G)$ is empty, so this test costs $O(n + m)$, much less than a general [edge connectivity](/edge-connectivity/) computation.

## Applications

- Find the single links of a computer, power or road network whose failure cuts some users off.
- **One-way streets.** By Robbins' theorem a connected graph has a [strong orientation](/strong-orientation/) if and only if it has no bridge. Bridge finding gives the test, and the same depth-first search gives the orientation: tree edges down, back edges up.
- **Euler tours.** [Fleury's algorithm](/fleury-algorithm/) for an [Eulerian path](/eulerian-path/) crosses a bridge of the remaining graph only when it has no other choice.
- Build the bridge tree, then answer queries such as "which links must every route from $u$ to $v$ use?" as the bridges on the tree path between the components of $u$ and $v$.

## References
