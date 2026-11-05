---
tag: T9JPRR
kind: concept
slug: dfs-forest
name: Depth-first forest
aliases:
- DFS forest
- depth-first tree
area: graphs/traversal
level: intro
summary: The collection of trees formed by the parent pointers of a complete DFS over all vertices.
prereqs: [depth-first-search, tree]
see_also: [bfs-tree, parenthesis-theorem, white-path-theorem, edge-classification, discovery-and-finish-times, connected-components, tremaux-traversal, spanning-forest]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.3, Depth-first search (the predecessor subgraph of DFS, the depth-first forest and its trees)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 3, Section 3.2 (the DFS search tree of an undirected graph, connected components) and Section 3.3 (the DFS forest of a directed graph)
  - paper: doi:10.1137/0201010
    title: Robert E. Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 146 to 160 (1972)
    locator: the section on depth-first search (the palm tree, a DFS tree of an undirected graph with its fronds)
---

The depth-first forest of a run of [depth-first search](/depth-first-search/) is the graph on all vertices whose edges are the pairs $(\pi[v], v)$ of a vertex and the vertex from which DFS discovered it. Each call of DFS-VISIT from the outer loop starts a new tree, so the forest has one tree for each root. In an undirected graph, the trees are spanning trees of the [connected components](/connected-components/), and each non-tree edge joins an ancestor and a descendant. In a directed graph the trees depend on the order in which the roots are tried, and the [parenthesis theorem](/parenthesis-theorem/) and the [white-path theorem](/white-path-theorem/) describe their structure.

## In plain words

Each time depth-first search reaches a new vertex, it got there along one edge from a vertex it was already exploring. Remember that edge for each vertex. These remembered edges never form a loop, because each one points from an older vertex to a newer one. So they form one or more trees.

When the search runs out of vertices it can reach, it picks a new starting vertex that it has not seen, and a new tree begins. The set of all these trees is the depth-first forest. Its trees tend to be tall and thin, because the search goes as deep as it can before it turns back.

## The idea

**Definition.** Let DFS$(G)$ run on $G = (V, E)$ and set the parents $\pi$. The *depth-first forest* is $G_\pi = (V, E_\pi)$ with

$$E_\pi = \{ (\pi[v], v) : v \in V,\ \pi[v] \ne \mathrm{NIL} \}.$$

Its edges are the *tree edges* of [edge classification](/edge-classification/). A vertex with $\pi[v] = \mathrm{NIL}$ is a *root*: it is a vertex that line L4 of DFS picks while it is still white. A *depth-first tree* is one connected part of $G_\pi$, with its root.

**It is a forest.** Each tree edge $(\pi[v], v)$ has $d[\pi[v]] < d[v]$, because $v$ is discovered inside the call of its parent. So the chain $v, \pi[v], \pi[\pi[v]], \ldots$ has strictly decreasing discovery times, never repeats a vertex, and ends at a root. Each non-root has exactly one parent, so $G_\pi$ has $n - k$ edges for $k$ roots and is a forest of $k$ rooted trees. The [depth-first search](/depth-first-search/) page proves this in full.

**What a tree contains.** By the [white-path theorem](/white-path-theorem/), the tree of a root $r$ holds exactly the vertices that $r$ reaches by a path of white vertices just before $d[r]$. The vertices of earlier trees are black at that moment, so the tree of $r$ is the set of vertices reachable from $r$ in the graph without the earlier trees.

**Undirected graphs.** In an undirected graph, the trees of a full DFS are exactly the connected components, each with a spanning tree. Let $C$ be a component, and let $T'$, with root $r'$, be the first tree that holds a vertex $x$ of $C$. Just before $d[r']$, no vertex of $C$ is in an earlier tree, so all of $C$ is white. The tree path from $r'$ to $x$ is white at that moment, so $r'$ is in $C$, and $r'$ reaches each vertex of $C$ by a path inside $C$, which is white. By the white-path theorem, all of $C$ is in $T'$. A tree is connected, so it holds no vertex outside $C$. So each tree is exactly one component, and its tree edges form a spanning tree of that component. Each non-tree edge joins an ancestor and a descendant, by the theorem on the [edge classification](/edge-classification/) page that undirected DFS has only tree and back edges. Tarjan called such a tree, with its back edges, a *palm tree*. A rooted spanning tree with this property is also called a [Trémaux](/tremaux-traversal/) tree.

**Directed graphs.** In a directed graph, the forest depends on the order of the roots and of the lists, and so does the number of trees. A tree need not be a strongly connected set, and a strongly connected component lies inside one tree: by the white-path theorem, its first discovered vertex is an ancestor of all the others.

**Depth.** A depth-first tree can be a path even if the graph has a short route to each vertex. On the [complete graph](/complete-graph/) $K_n$, every DFS tree is a path with $n$ vertices, while every BFS tree is a star. This is the opposite of the [breadth-first tree](/bfs-tree/), whose paths are shortest paths.

## Examples

Use the directed graph with vertices 0 to 6 and the lists $0: 1, 3, 2$; $1: 2$; $2: 0$; $3: 2, 4$; $4$: none; $5: 4, 6$; $6: 5$.

| roots tried in the order | trees (root first, then the vertices in discovery order) | parent pointers $\pi[0], \ldots, \pi[6]$ |
|---|---|---|
| 0, 1, 2, 3, 4, 5, 6 | $\{0, 1, 2, 3, 4\}$, $\{5, 6\}$ | NIL, 0, 1, 0, 3, NIL, 5 |
| 6, 5, 4, 3, 2, 1, 0 | $\{6, 5, 4\}$, $\{3, 2, 0, 1\}$ | 2, 0, 3, NIL, 5, 6, NIL |
| 4, 2, 1, 0, 3, 5, 6 | $\{4\}$, $\{2, 0, 1, 3\}$, $\{5, 6\}$ | 2, 0, NIL, 0, NIL, NIL, 5 |

In the first run, the tree of 0 has the tree edges $0 \to 1$, $1 \to 2$, $0 \to 3$ and $3 \to 4$, and the tree of 5 has $5 \to 6$. Each tree has one edge fewer than vertices: $7 - 2 = 5$ tree edges in all. In the third run, the root 4 has no outgoing edge, so it is a tree on its own, and the forest has three trees and 4 tree edges. The strong component $\{0, 1, 2\}$ lies inside one tree in each run, and so does $\{5, 6\}$.

**Undirected example.** Take the undirected graph with vertices 0 to 7 and the edges $\{0,1\}$, $\{0,2\}$, $\{1,3\}$, $\{2,3\}$, $\{2,4\}$, $\{3,5\}$, $\{4,5\}$, $\{5,6\}$, with sorted lists. A full DFS discovers $0, 1, 3, 2, 4, 5, 6$ in one tree, which is the path $0, 1, 3, 2, 4, 5, 6$, and then the single vertex 7 as a second tree. The two trees are the two connected components. The non-tree edges $\{0, 2\}$ and $\{3, 5\}$ join an ancestor and a descendant.

## Where it is used

- **[Connected components](/connected-components/).** In an undirected graph, each tree of a full DFS is one component.
- **[Edge classification](/edge-classification/).** The types of the other edges are defined by the forest.
- **[Articulation points](/articulation-point/) and [bridges](/bridge-finding/).** The root is a cut vertex exactly when it has two or more children, and the other tests use subtrees of the forest and their back edges.
- **[Strongly connected components](/strongly-connected-components/).** In the second pass of [Kosaraju-Sharir](/kosaraju-sharir/), each tree of the DFS of the [transpose graph](/transpose-graph/) is one component.
- **[Topological sort](/topological-sort/).** The finish times of the forest give the order.
- **[Spanning forests](/spanning-forest/).** A DFS forest is a spanning forest of an undirected graph in linear time.

## References
