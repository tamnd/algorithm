---
tag: 7FA87V
kind: theorem
slug: white-path-theorem
name: White-path theorem
area: graphs/traversal
level: core
summary: A vertex is a DFS descendant of another exactly when it is reachable through white vertices at discovery time.
prereqs: [parenthesis-theorem, depth-first-search]
see_also: [discovery-and-finish-times, dfs-forest, edge-classification, topological-ordering-theorem, kosaraju-sharir, tarjan-scc, cycle-detection]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.3, Depth-first search (the white-path theorem, and its use for the classification of edges in undirected graphs), Section 20.4 (acyclic graphs and back edges) and Section 20.5 (strongly connected components)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 22.3, Theorem 22.9 (White-path theorem)
---

The white-path theorem describes the subtree of a vertex in a [depth-first search](/depth-first-search/) by the state of the search at one moment: when DFS discovers $u$, the descendants of $u$ will be exactly the vertices that $u$ can reach by a path of vertices that are all still undiscovered (white). It holds for directed and undirected graphs and for each order of the vertices and the lists. It is the main tool in the correctness proofs of DFS algorithms: [cycle detection](/cycle-detection/), [topological sort](/topological-sort/) and the [strong components](/strongly-connected-components/) algorithms of [Kosaraju and Sharir](/kosaraju-sharir/) and of [Tarjan](/tarjan-scc/).

## Statement

Let $G = (V, E)$ be a directed or undirected graph, and run DFS$(G)$ as on the [depth-first search](/depth-first-search/) page, with the colours white, gray and black and the [discovery and finish times](/discovery-and-finish-times/) $d$ and $f$. A path is *white at time $t$* if each of its vertices is white at time $t$. By the moment "just before $d[u]$" we mean the moment just before line L5 of the call DFS-VISIT$(u)$ makes $u$ gray.

**Theorem (white-path theorem).** For any two vertices $u$ and $v$, the vertex $v$ is a descendant of $u$ in the [depth-first forest](/dfs-forest/) if and only if, just before $d[u]$, there is a path from $u$ to $v$ in $G$ that is white.

Each vertex counts as a descendant of itself, and the path with the single vertex $u$ is white just before $d[u]$. Some authors say the same thing at time $d[u]$, with "all vertices of the path except $u$ are white".

## In plain words

When the search arrives at a new vertex, it is about to explore everything below it. The question is what "below it" will turn out to be.

The answer: look at all the vertices the search has not touched yet. The new vertex will collect exactly those that it can reach by walking only through untouched vertices. A vertex that it can reach only through a vertex that the search has already seen will not end up below it, because the search got to that part earlier, from somewhere else.

So one look at the graph, at the right moment, tells the whole shape of the subtree. That makes this theorem the easiest way to prove facts about depth-first search.

## Proof

We use the corollary of the [parenthesis theorem](/parenthesis-theorem/): $w$ is a proper descendant of $u$ if and only if $d[u] < d[w] < f[w] < f[u]$. A vertex $w$ is white just before $d[u]$ exactly when $w = u$ or $d[w] > d[u]$, because the times are distinct and a vertex is white until its discovery time.

**Only if.** Let $v$ be a descendant of $u$. If $v = u$, the path with one vertex is white. Else let $u = w_0, w_1, \ldots, w_k = v$ be the path from $u$ to $v$ in the forest. Each pair $(w_{i-1}, w_i)$ is a tree edge, so it is an edge of $G$, and the sequence is a path of $G$. For $i \ge 1$, the vertex $w_i$ is a proper descendant of $u$, so $d[u] < d[w_i]$ by the corollary, and $w_i$ is white just before $d[u]$. So the path is white.

**If.** Let $u = x_0, x_1, \ldots, x_k = v$ be a path of $G$ that is white just before $d[u]$. Assume, for a contradiction, that some vertex of the path is not a descendant of $u$, and let $x_j$ be the first such vertex. Then $j \ge 1$, because $x_0 = u$ is a descendant of itself. The vertex $y = x_{j-1}$ is a descendant of $u$, so $f[y] \le f[u]$: this is equality if $y = u$ and the corollary otherwise.

The vertex $x_j$ was white just before $d[u]$ and $x_j \ne u$, so $d[u] < d[x_j]$. Next we show $d[x_j] < f[y]$. The call DFS-VISIT$(y)$ runs its loop of line L6 over $\mathrm{Adj}[y]$, which contains $x_j$, before it sets $f[y]$ at line L10. When the loop reaches $x_j$, there are two cases. If $x_j$ is white, line L9 calls DFS-VISIT$(x_j)$ with $\pi[x_j] = y$, so $x_j$ is a child of $y$ and a descendant of $u$, which contradicts the choice of $x_j$. So $x_j$ is not white at that moment. Then it was discovered before that moment, which is before $f[y]$. So $d[x_j] < f[y]$.

Together, $d[u] < d[x_j] < f[y] \le f[u]$. So the intervals $[d[u], f[u]]$ and $[d[x_j], f[x_j]]$ share the point $d[x_j]$ and are not disjoint. By the parenthesis theorem one contains the other, and because $d[u] < d[x_j]$ the interval of $x_j$ lies inside the interval of $u$. By the theorem, $x_j$ is then a descendant of $u$. This contradicts the choice of $x_j$. So all vertices of the path, $v$ among them, are descendants of $u$. $\blacksquare$

## Consequences

- **Reachability.** Call DFS-VISIT$(s)$ when all vertices are white. A path from $s$ is white just before $d[s]$ exactly when it is a path, so the tree of $s$ holds exactly the vertices reachable from $s$. This is the correctness of DFS for [graph reachability](/graph-reachability/).
- **Back edges and cycles.** A directed graph has a cycle if and only if a DFS finds a back edge. If $C$ is a cycle and $v$ is its first vertex to be discovered, then just before $d[v]$ the rest of $C$ is white, so the vertex $u$ before $v$ on $C$ becomes a descendant of $v$, and the edge $(u, v)$ goes from a descendant to an ancestor. See the [topological ordering theorem](/topological-ordering-theorem/) and [cycle detection](/cycle-detection/).
- **Undirected graphs.** In a DFS of an undirected graph, each edge is a tree edge or a back edge (see [edge classification](/edge-classification/)). For an edge $\{u, v\}$ with $d[u] < d[v]$, the vertex $v$ is white just before $d[u]$, so it becomes a descendant of $u$, and the edge joins an ancestor and a descendant.
- **Strong components.** In a DFS of a directed graph, the first vertex discovered in a strongly connected component is an ancestor of all other vertices of the component: just before its discovery, the whole component is white and reachable from it inside the component. Both the [Kosaraju-Sharir](/kosaraju-sharir/) and the [Tarjan](/tarjan-scc/) algorithms rest on this fact.
- **Trémaux trees.** In a connected undirected graph, the trees that DFS gives are exactly the rooted spanning trees in which each edge of the graph joins an ancestor and a descendant (see [Trémaux traversal](/tremaux-traversal/)). The white-path theorem gives the direction "each DFS tree has this property".

## Tightness

The condition "white" cannot be replaced by "reachable". In the DFS of the [depth-first search](/depth-first-search/) example, with the edge $3 \to 2$, vertex 3 reaches vertex 2 by an edge. But 2 is black at $d[3] = 6$, because $f[2] = 4$, and 2 is not a descendant of 3: their intervals $[3, 4]$ and $[6, 9]$ are disjoint. In the same way, 5 reaches 4 by an edge, but 4 is already black at $d[5] = 11$, and 4 is in the other tree.

The moment of the test also matters. Just before $d[0] = 1$, all vertices are white, and the white paths from 0 reach $\{0, 1, 2, 3, 4\}$, which is the tree of 0. Vertex 5 is white too, but no path from 0 reaches it, so it is not in the tree. A test at a later time, when more vertices are gray or black, can miss descendants that are already discovered.

## History

The theorem in this form, with the name "white-path theorem", is from the section on depth-first search in Cormen, Leiserson, Rivest and Stein. The same property of DFS trees, phrased with the order of discovery instead of colours, is used in the proofs of the classical DFS algorithms for strong components and biconnected components.

## References
