---
tag: F0G01M
kind: concept
slug: low-link
name: Low-link values
aliases:
- Low-point
- Low values
area: graphs/connectivity
level: core
summary: For each DFS vertex, the smallest discovery time reachable via one back edge from its subtree.
prereqs: [depth-first-search, discovery-and-finish-times, edge-classification, dfs-forest]
see_also: [articulation-point-finding, bridge-finding, tarjan-scc, hopcroft-tarjan-biconnectivity, two-edge-connected-components, strong-orientation, parenthesis-theorem]
sources:
  - paper: doi:10.1137/0201010
    title: Robert E. Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 146 to 160 (1972)
    locator: the sections on biconnected components (LOWPT) and on strongly connected components (LOWLINK)
  - paper: doi:10.1145/362248.362272
    title: John Hopcroft and Robert Tarjan, Algorithm 447, Efficient algorithms for graph manipulation, Communications of the ACM 16(6), 372 to 378 (1973)
    locator: the biconnected components algorithm (the low point of a vertex)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Problem 22-2, Articulation points, bridges, and biconnected components (the value low[v] and the criteria for articulation points and bridges)
  - book: isbn:9780521736534
    title: Shimon Even, Graph Algorithms, second edition, edited by Guy Even, Cambridge University Press (2012)
    locator: Chapter 3, Depth-first search (lowpoints, nonseparable components and strong components)
---

A low-link value is a number that a [depth-first search](/depth-first-search/) computes for each vertex $v$: the smallest discovery number that the search can reach from the subtree of $v$ by following tree edges down and then one non-tree edge. It tells whether the subtree of $v$ has a way "up" past its parent that avoids the tree edge into $v$. In an undirected graph this gives the [articulation points](/articulation-point/) and the [bridges](/bridge/) in linear time. In a directed graph a variant of the same number gives the [strongly connected components](/strongly-connected-components/), in [Tarjan's algorithm](/tarjan-scc/).

## In plain words

Run a depth-first search and number the vertices in the order you first meet them. The search makes a tree. Each vertex has a part of the tree below it, its subtree.

Now ask, for each vertex: from somewhere in my subtree, can I jump by one extra edge, not a tree edge, to a vertex that the search met earlier? The low-link value is the earliest number you can reach this way, or the vertex's own number if no jump helps.

If the subtree below a child of a vertex cannot jump above that vertex, then that vertex is the only door between the subtree and the rest of the graph. Remove the door, and the subtree falls off. That is the whole use of the value: it finds the doors.

## The idea

Run DFS on a graph $G = (V, E)$ and let $d[v] \in \{1, \ldots, n\}$ be the *preorder number* of $v$: $d[v] = i$ when $v$ is the $i$-th vertex discovered. The [discovery times](/discovery-and-finish-times/) of the DFS page, which also count the finish events, have the same order, and only the order matters here. Let $T(v)$ be the set of descendants of $v$ in the [DFS forest](/dfs-forest/), $v$ included. By the [parenthesis theorem](/parenthesis-theorem/), $T(v)$ is the set of vertices with preorder numbers $d[v], d[v] + 1, \ldots, d[v] + |T(v)| - 1$.

### Undirected graphs: the low point

Let $G$ be undirected. Parallel edges and [self-loops](/self-loop/) are allowed. The search must treat edges by their identity, not by their ends: it skips the one edge by which it entered a vertex, and every other edge, including a second copy of that edge, is a non-tree edge. In a DFS of an undirected graph every non-tree edge joins a vertex to one of its ancestors (see [edge classification](/edge-classification/)). Define

$$\mathrm{low}[v] = \min\bigl(\{d[v]\} \cup \{\, d[w] : \text{some non-tree edge joins } x \in T(v) \text{ and } w \,\}\bigr).$$

It satisfies a recurrence over the children $c$ of $v$, so one DFS computes it when each vertex finishes:

$$\mathrm{low}[v] = \min\bigl(d[v],\ \min\{ d[w] : \text{non-tree edge } \{v, w\} \},\ \min\{\mathrm{low}[c] : c \text{ a child of } v\}\bigr).$$

The recurrence holds because $T(v)$ is $\{v\}$ together with the sets $T(c)$ of the children. A loop $\{v, v\}$ adds $d[v]$, which changes nothing.

**Which edges leave a subtree.** Let $c$ be a child of $u$. An edge with one end $x \in T(c)$ and the other end $y \notin T(c)$ is either the tree edge $\{u, c\}$ or a non-tree edge. In the second case $y$ is an ancestor or a descendant of $x$; it is not a descendant, as $y \notin T(c)$, so it is a proper ancestor of $c$, and $d[y] \le d[u]$. Non-tree edges with both ends in $T(c)$ have their upper end in $T(c)$, with $d \ge d[c]$. So

$$\mathrm{low}[c] \le d[u] \iff \text{some edge other than the tree edge } \{u, c\} \text{ joins } T(c) \text{ to a proper ancestor of } c.$$

Two criteria follow. In both, the graph minus $T(c)$, inside the tree of $c$, stays connected by tree edges, and the tree of $c$ is connected, so only the edges out of $T(c)$ matter.

- **Bridges.** The tree edge $\{u, c\}$ is a [bridge](/bridge/) if and only if $\mathrm{low}[c] > d[u]$, which is the same as $\mathrm{low}[c] = d[c]$. *Proof.* After the removal of $\{u, c\}$, the set $T(c)$ is still connected and so is the rest of its DFS tree. They are joined exactly when another edge joins $T(c)$ to a proper ancestor of $c$, that is, when $\mathrm{low}[c] \le d[u]$. A non-tree edge is never a bridge, because its tree path closes a cycle with it. $\square$
- **Articulation points.** A vertex $u$ that is not a root is an [articulation point](/articulation-point/) if and only if it has a child $c$ with $\mathrm{low}[c] \ge d[u]$. A root is one if and only if it has at least two children. *Proof.* Remove $u$. Each $T(c)$ for a child $c$ stays connected. No edge joins $T(c)$ to $T(c')$ for two children, because such an edge would join two vertices of which neither is an ancestor of the other. If $u$ is not a root, the rest of its tree minus $u$ and its subtrees contains the root and is connected through the tree path above $u$. So $T(c)$ is cut off exactly when no edge joins it to a proper ancestor of $u$, that is, when $\mathrm{low}[c] \ge d[u]$. If $u$ is the root, there is no rest, and the subtrees of its children are cut off from each other exactly when there are at least two. $\square$

### Directed graphs: Tarjan's low-link

Let $G$ be directed. Parallel arcs and loops are allowed. Here a non-tree arc can also go to a vertex in another subtree (a cross arc), and such an arc must count only if its target is still in the same strong component. [Tarjan's algorithm](/tarjan-scc/) keeps the vertices whose component is not yet finished on a stack, and defines

$$\mathrm{lowlink}[v] = \min\bigl(d[v],\ \min\{ d[w] : (v, w) \text{ a non-tree arc, } w \text{ on the stack}\},\ \min\{\mathrm{lowlink}[c] : c \text{ a child of } v\}\bigr).$$

**Root criterion.** $v$ is the first vertex discovered in its strong component, its *root*, if and only if $\mathrm{lowlink}[v] = d[v]$ when $v$ finishes. The proof is on the [Tarjan's algorithm](/tarjan-scc/) page.

### Variant definitions

The books do not agree on one definition. Hopcroft and Tarjan use the low point above. Some texts take the minimum over the vertices reached by a path in $T(v)$ followed by one back edge, which is the same set. Some programs replace $d[w]$ by $\mathrm{low}[w]$ for a non-tree edge to an ancestor $w$. In the directed algorithm this still finds the right components, because $\mathrm{lowlink}[w] \le d[w]$ and $w$ is in the same component. In the undirected tests it is wrong, as the pitfall below shows. The values themselves differ between these versions, so code and proofs must use one definition throughout.

## Examples

**Undirected.** Take the vertices 0 to 6 and the edges $\{0,1\}$, $\{1,2\}$, $\{2,0\}$, $\{1,3\}$, $\{3,4\}$, $\{4,1\}$, $\{4,5\}$, two parallel edges $\{5,6\}$, and a loop $\{6,6\}$. The lists follow this order. DFS from 0 visits $0, 1, 2, 3, 4, 5, 6$ along the tree path $0 - 1 - 2$, then $1 - 3 - 4 - 5 - 6$.

| vertex | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $d$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| parent | none | 0 | 1 | 1 | 3 | 4 | 5 |
| low | 1 | 1 | 1 | 2 | 2 | 6 | 6 |

- $\mathrm{low}[2] = 1$ by the edge $\{2, 0\}$, and $\mathrm{low}[4] = 2$ by the edge $\{4, 1\}$.
- $\mathrm{low}[6] = 6$: the second copy of $\{5, 6\}$ is a non-tree edge to $d[5] = 6$. The loop adds $d[6] = 7$.
- **Bridges.** Only $\{4, 5\}$, because $\mathrm{low}[5] = 6 > d[4] = 5$. The edge $\{5, 6\}$ is not a bridge: $\mathrm{low}[6] = 6 = d[5]$, thanks to its parallel copy.
- **Articulation points.** 1 (child 3 has $\mathrm{low}[3] = 2 \ge d[1] = 2$), 4 (child 5 has $6 \ge 5$) and 5 (child 6 has $6 \ge 6$). The root 0 has one child, so it is not one.

**Directed.** Take the graph of the [depth-first search](/depth-first-search/) page, with the lists $0: 1, 3, 2$; $1: 2$; $2: 0$; $3: 2, 4$; $4$: none; $5: 4, 6$; $6: 5$. The preorder numbers and the low-links of Tarjan's algorithm are:

| vertex | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $d$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| lowlink | 1 | 1 | 1 | 3 | 5 | 6 | 6 |

The roots, with $\mathrm{lowlink}[v] = d[v]$, are 0, 4 and 5, one for each component $\{0, 1, 2, 3\}$, $\{4\}$, $\{5, 6\}$. Vertex 3 gets $\mathrm{lowlink}[3] = 3$ from the cross arc $3 \to 2$: vertex 2 is finished but still on the stack, so it is in an unfinished component. The arc $5 \to 4$ does not count, because 4 left the stack when its component $\{4\}$ was output.

**A pitfall in numbers.** Take the vertices 0 to 4 and the edges $\{0,1\}$, $\{1,2\}$, $\{2,0\}$, $\{1,3\}$, $\{3,4\}$, $\{4,1\}$: two triangles that share vertex 1. DFS from 0 gives $d = 1, 2, 3, 4, 5$ for $0, 1, 2, 3, 4$. With the definition above, $\mathrm{low} = 1, 1, 1, 2, 2$, and the child 3 of vertex 1 has $\mathrm{low}[3] = 2 \ge d[1]$, so 1 is an articulation point, which is right. If the back edge $\{4, 1\}$ uses $\mathrm{low}[1] = 1$ instead of $d[1] = 2$, all low values become 1, and the test misses vertex 1.

## Where it is used

- [Articulation point finding](/articulation-point-finding/) and [bridge finding](/bridge-finding/): the two criteria above, in one DFS and $\Theta(n + m)$ time.
- [Biconnected components](/biconnected-components/), by the [Hopcroft-Tarjan algorithm](/hopcroft-tarjan-biconnectivity/): a stack of edges is cut each time a child $c$ of $u$ has $\mathrm{low}[c] \ge d[u]$.
- [Two-edge-connected components](/two-edge-connected-components/): cut at each bridge.
- [Strongly connected components](/strongly-connected-components/), by [Tarjan's algorithm](/tarjan-scc/): a component is output when its root finishes with $\mathrm{lowlink}[v] = d[v]$.
- [Strong orientation](/strong-orientation/): in a connected graph without bridges, orienting the tree edges down and the back edges up gives a strongly connected graph. The proof uses $\mathrm{low}[c] \le d[\text{parent of } c]$ for every non-root $c$.
- [Ear decomposition](/ear-decomposition/) and the [block-cut tree](/block-cut-tree/): built from the same DFS data.

## References
