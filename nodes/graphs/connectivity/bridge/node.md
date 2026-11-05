---
tag: 4FNN59
kind: definition
slug: bridge
name: Bridge
aliases:
- Cut edge
- Isthmus
area: graphs/connectivity
level: intro
summary: An edge whose removal increases the number of connected components.
prereqs: [connected-graph, connected-components]
see_also: [articulation-point, bridge-finding, two-edge-connected-graph, two-edge-connected-components, k-edge-connected-graph, hopcroft-tarjan-biconnectivity, strong-orientation]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 1.4, Connectivity (bridges and edge separators)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 1.2, Paths, cycles, and trails (cut-edges, and the theorem that an edge is a cut-edge if and only if it lies on no cycle)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 20, Problem 20-2, Articulation points, bridges, and biconnected components (Problem 22-2 in the third edition)
  - paper: doi:10.2307/2303897
    title: Herbert E. Robbins, A theorem on graphs, with an application to a problem of traffic control, American Mathematical Monthly 46(5), 281 to 283 (1939)
    locator: the main theorem (a graph has a strongly connected orientation if and only if it is connected and has no bridge)
---

A bridge, or cut edge, of an [undirected graph](/undirected-graph/) is an edge whose removal increases the number of [connected components](/connected-components/). An edge is a bridge exactly when it lies on no cycle, so a bridge is the only link between two parts of the graph. A connected graph with no bridge is [2-edge-connected](/two-edge-connected-graph/), and only such a graph can be made [strongly connected](/strongly-connected-graph/) by giving each edge a direction ([strong orientation](/strong-orientation/)). All bridges can be found in $O(n + m)$ time with one [depth-first search](/depth-first-search/), as the [bridge finding](/bridge-finding/) page shows.

## Definition

Let $G = (V, E)$ be an undirected graph, where $E$ is a multiset: parallel edges and [self-loops](/self-loop/) are allowed. For an edge $e$, let $G - e$ be $G$ with this one copy of the edge removed and all vertices kept. Let $c(H)$ be the number of components of $H$. Then

$$e \text{ is a bridge of } G \iff c(G - e) > c(G).$$

Here a *cycle* is a closed trail $x_0, e_1, x_1, \ldots, e_k, x_k = x_0$ with $k \ge 1$, distinct edges, and distinct vertices $x_0, \ldots, x_{k-1}$. So a loop is a cycle of length 1, and two parallel edges form a cycle of length 2.

**Theorem.** An edge $e$ is a bridge if and only if $e$ lies on no cycle of $G$.

*Proof.* Let $e$ join $u$ and $v$. If $e$ lies on a cycle, the rest of the cycle is a $u$-$v$ walk in $G - e$. Then each walk of $G$ that uses $e$ can replace $e$ by this walk, so any two vertices joined in $G$ are joined in $G - e$, and $c(G - e) = c(G)$. Conversely, suppose that $e$ is not a bridge. If $e$ is a loop, it is a cycle by itself. Otherwise $u$ and $v$ are still joined in $G - e$: else the component of $G$ that contains them would split. Take a $u$-$v$ path in $G - e$. With $e$ it forms a cycle that contains $e$. $\square$

Two consequences follow at once. A loop is never a bridge. An edge with a parallel copy is never a bridge, because the two copies form a cycle.

**Removing a bridge adds exactly one component.** Let the bridge $e = \{u, v\}$ lie in the component $C$. Each vertex $x$ of $C$ has a path to $u$ in $C$. If the path does not use $e$, it is in $C - e$. If it does, the part before $e$ is a path in $C - e$ from $x$ to $u$ or to $v$. So $C - e$ has at most two components, those of $u$ and of $v$, and $c(G - e) = c(G) + 1$.

**Bridges form a forest.** The bridges of $G$ contain no cycle, since each edge of such a cycle would lie on a cycle. So a graph on $n$ vertices has at most $n - 1$ bridges, and a [tree](/tree/) has exactly $n - 1$: in a tree every edge is a bridge. Every bridge lies in each [spanning forest](/spanning-forest/) of $G$, since a spanning forest has the same components as $G$.

**Depth-first search.** In a [depth-first forest](/dfs-forest/) of $G$, every bridge is a tree edge, because a back edge closes a cycle with the tree path. A tree edge from $u$ to its child $v$ is a bridge if and only if no edge other than this one joins the subtree of $v$ to a vertex outside it. The [Hopcroft-Tarjan algorithm](/hopcroft-tarjan-biconnectivity/) tests this with [low-link](/low-link/) values.

**Bridges and articulation points.** If $\{u, v\}$ is a bridge and $u$ has a neighbour other than $v$, then $u$ is an [articulation point](/articulation-point/). An articulation point need not touch a bridge: two triangles that share a vertex have one articulation point and no bridge.

**Directed graphs.** The definition is for undirected graphs. In a directed graph, an edge whose removal increases the number of [strongly connected components](/strongly-connected-components/) is called a *strong bridge*; it is a different notion with different algorithms.

## Examples and non-examples

The graph below has $n = 7$ vertices and 10 edges: a triangle $0, 1, 2$ with a second copy of $\{0, 1\}$, the edge $\{2, 3\}$, a triangle $3, 4, 5$, the edge $\{5, 6\}$, and a loop at 6.

| edge | on a cycle? | $c(G - e)$ | bridge? |
|---|---|---|---|
| $\{0, 1\}$, either copy | yes, the other copy, and the triangle | 1 | no |
| $\{1, 2\}$, $\{2, 0\}$ | yes, the triangle | 1 | no |
| $\{2, 3\}$ | no | 2 | yes |
| $\{3, 4\}$, $\{4, 5\}$, $\{5, 3\}$ | yes, the triangle | 1 | no |
| $\{5, 6\}$ | no | 2 | yes |
| the loop at 6 | yes, itself | 1 | no |

The bridges are $\{2, 3\}$ and $\{5, 6\}$, and they form a forest. Removing $\{2, 3\}$ leaves the components $\{0, 1, 2\}$ and $\{3, 4, 5, 6\}$. The ends 2, 3 and 5 of the bridges have other neighbours, so they are articulation points.

More cases:

| graph | bridges |
|---|---|
| a tree on $n$ vertices | all $n - 1$ edges |
| a cycle | none |
| two vertices joined by two parallel edges | none |
| a single edge $\{0, 1\}$ | the edge; neither end is an articulation point |
| two triangles sharing a vertex | none, but the shared vertex is an articulation point |
| two triangles joined by one edge | that edge |

**A common error.** Code for simple graphs often skips "the edge back to the parent vertex" in a depth-first search. On the graph with two parallel edges between 0 and 1, this code skips both copies and reports a bridge. The search must skip only the one edge that it came in by, by its identity, not by its other end.

## Related definitions

- [Articulation point](/articulation-point/): the same idea for a vertex.
- [Cut](/cut/): the set of edges between a vertex set $S$ and its complement. A bridge is a cut with one edge.
- [2-edge-connected graph](/two-edge-connected-graph/) and [k-edge-connected graph](/k-edge-connected-graph/): connected graphs where no set of fewer than 2, or $k$, edges disconnects the graph.
- [2-edge-connected components](/two-edge-connected-components/): the parts left when all bridges are removed.
- [Strong orientation](/strong-orientation/): a graph has one if and only if it is connected and has no bridge (Robbins' theorem).
- [Bridge finding](/bridge-finding/): the problem of listing all bridges.

## References
