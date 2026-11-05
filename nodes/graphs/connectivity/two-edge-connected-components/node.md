---
tag: N1HX24
kind: problem
slug: two-edge-connected-components
name: Two-edge-connected components
aliases:
- 2-edge-connected components
- Bridge-connected components
area: graphs/connectivity
level: core
summary: Remove all bridges; the remaining connected components are the 2-edge-connected components.
prereqs: [two-edge-connected-graph, bridge-finding, connected-components, low-link]
see_also: [bridge, biconnected-components, block-cut-tree, strong-orientation, edge-connectivity, gomory-hu-tree, menger-theorem, tarjan-scc]
sources:
  - paper: doi:10.1016/0020-0190(74)90003-9
    title: Robert E. Tarjan, A note on finding the bridges of a graph, Information Processing Letters 2(6), 160 to 161 (1974)
    locator: the whole paper (bridges and 2-edge-connected components in linear time from a spanning tree in preorder)
  - paper: doi:10.1137/0201010
    title: Robert E. Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 146 to 160 (1972)
    locator: the sections on depth-first search and biconnected components (the low point on which the bridge test rests)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Problem 22-2, Articulation points, bridges, and biconnected components (the bridge test by low values)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 1.2, Paths, cycles, and trails (an edge is a cut-edge exactly when it lies on no cycle), and Section 4.1, Cuts and connectivity
---

The two-edge-connected components of an undirected graph are its maximal parts that no single edge removal can split. Two vertices are in the same component exactly when they are joined by two paths with no edge in common, and the components are what is left when every [bridge](/bridge/) is deleted. Contracting each component to a point turns the graph into a forest whose edges are the bridges, the *bridge tree*. One [depth-first search](/depth-first-search/) with [low-link values](/low-link/) finds them in $\Theta(n + m)$ time.

## In plain words

Think of a road network where any one road might be closed for repairs. Two towns are firmly linked if, whatever single road is closed, you can still drive from one to the other. Firmly linked towns form groups.

The roads that break this are the bridges: roads whose closure splits the network. Delete every bridge, and the pieces that remain are exactly the groups. Inside a group, every road lies on a loop, so there is always a detour. Between groups, the only links are bridges, and they form a tree: there is exactly one chain of bridges from one group to another.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges. [Parallel edges](/multigraph/) and [self-loops](/self-loop/) are allowed, and two parallel copies of an edge are different edges. A loop is never a bridge, and an edge with a parallel copy is never a bridge.

**Output.** A label $comp[v]$ for each vertex such that $comp[u] = comp[v]$ exactly when $u \equiv v$, where

$$u \equiv v \iff u = v \text{ or } G \text{ has two edge-disjoint } u\text{-}v \text{ paths.}$$

By the edge form of [Menger's theorem](/menger-theorem/), for $u \ne v$ this is the same as "no single edge meets every $u$-$v$ path", that is, $\lambda(u, v) \ge 2$.

**Theorem.** Let $B$ be the set of bridges of $G$. Then $u \equiv v$ if and only if $u$ and $v$ are in the same connected component of $G - B$. In particular $\equiv$ is an equivalence relation, its classes induce [2-edge-connected](/two-edge-connected-graph/) subgraphs, and contracting each class gives a forest whose edges are the bridges.

*Proof.* We use that an edge is a bridge exactly when it lies on no cycle (see [2-edge-connected graph](/two-edge-connected-graph/)).

Let $u \ne v$ be joined by a path $P$ in $G - B$, and let $e$ be any edge. If $e \notin P$, $P$ is a $u$-$v$ path in $G - e$. If $e \in P$, then $e$ is not a bridge, so it lies on a cycle $C$, and replacing $e$ in $P$ by $C - e$ gives a $u$-$v$ walk, hence a path, in $G - e$. So no single edge meets every $u$-$v$ path, and $u \equiv v$.

Conversely, let $u$ and $v$ be in different components of $G - B$. If they are in different components of $G$, there is no $u$-$v$ path at all. Else take a $u$-$v$ path $P$ of $G$; it is not in $G - B$, so it uses a bridge $b = \{x, y\}$, once, with $x$ before $y$. The part of $P$ from $u$ to $x$ and the part from $y$ to $v$ avoid $b$, and $x$ and $y$ are in different components of $G - b$, so $u$ and $v$ are in different components of $G - b$. So $b$ meets every $u$-$v$ path, and $u \not\equiv v$.

A class $K$ is a component of $G - B$. A bridge has its ends in different classes, because it lies on no cycle, so a path of $G - B$ between its ends would close one. So the edges of $G$ inside $K$ are the edges of $G - B$ inside $K$. Each of them lies on a cycle of $G$; a cycle contains no bridge, so the cycle lies in $G - B$, and as it is connected it lies in $K$. So $G[K]$ is connected and every edge lies on a cycle in it: it is 2-edge-connected. Finally, contract each class. A cycle in the contracted graph uses some bridge $b$ once, and joining its edges by paths inside the classes gives a closed walk of $G$ that uses $b$ exactly once. The rest of this walk joins the ends of $b$ in $G - b$, which is impossible. So the contracted graph is a forest. $\square$

## Variants

- **Edge version.** Some texts call the classes of edges, not of vertices, the components: each non-bridge edge goes to the class of its ends, and each bridge is left alone. This is the same information.
- **Bridge tree.** Output the forest of the theorem, with the classes as nodes and the bridges as edges. Then the bridges on every $u$-$v$ path of $G$ are the edges of the tree path between the classes of $u$ and $v$, and their number is the tree distance.
- **$k$-edge-connected components.** For $k \ge 3$, define $u \equiv_k v$ when $\lambda(u, v) \ge k$. This is still an equivalence relation, as $\lambda(u, w) \ge \min(\lambda(u, v), \lambda(v, w))$, and a [Gomory-Hu tree](/gomory-hu-tree/) gives all of its classes: delete the tree edges of weight less than $k$. Unlike the case $k = 2$, a class need not induce a connected subgraph. Join $u$ and $v$ by three paths of length 2 through $a$, $b$ and $c$: then $\lambda(u, v) = 3$, but $a$, $b$ and $c$ have degree 2, so the classes for $k = 3$ are $\{u, v\}$, $\{a\}$, $\{b\}$, $\{c\}$, and $\{u, v\}$ induces no edge.
- **Vertex version.** The [biconnected components](/biconnected-components/) split the edges at [articulation points](/articulation-point/) instead of at bridges. Each biconnected component that is not a single bridge lies inside one two-edge-connected component, and the two-edge-connected components are the connected unions of these blocks.
- **Directed graphs.** The arc analogue, classes of vertices that stay strongly connected after any one arc removal, is a different and harder problem, not covered here.

## Examples

**A small graph.** Take the vertices 0 to 7 and the edges $\{0,1\}$, $\{1,2\}$, $\{2,0\}$, $\{1,3\}$, $\{3,4\}$, $\{4,1\}$, $\{4,5\}$, two parallel edges $\{5,6\}$, and a loop $\{6,6\}$; vertex 7 has no edge. This is the example of [low-link values](/low-link/), with one more vertex. The only bridge is $\{4, 5\}$: every other edge lies on a cycle, the edge $\{5, 6\}$ on the 2-cycle formed with its copy. Deleting it leaves the components $\{0, 1, 2, 3, 4\}$, $\{5, 6\}$ and $\{7\}$. The bridge tree is one edge, between $\{0, 1, 2, 3, 4\}$ and $\{5, 6\}$, and the isolated node $\{7\}$.

Vertex 1 is an articulation point, so the class $\{0, 1, 2, 3, 4\}$ consists of two blocks, the triangles $\{0, 1, 2\}$ and $\{1, 3, 4\}$, joined at 1. Two-edge-connected components do not split at articulation points.

**Trees.** In a tree every edge is a bridge, so every vertex is its own class, and the bridge tree is the tree itself.

**Dumbbell.** Two triangles joined by one edge have two classes, the two triangles.

**Bowtie.** Two triangles that share a vertex have no bridge, so they form one class, although they are two biconnected components.

## Known algorithms

| Algorithm | Time | Extra space | Idea |
|---|---|---|---|
| Bridges, then components | $\Theta(n + m)$ | $\Theta(n)$ | Find bridges by the low-point test, then search $G - B$ |
| One-pass DFS with a stack | $\Theta(n + m)$ | $\Theta(n)$ | Pop a class when a tree edge turns out to be a bridge |
| Tarjan's 1974 method | $\Theta(n + m)$ | $\Theta(n)$ | Any spanning tree in preorder, with subtree sizes and the range of preorder numbers reached by non-tree edges |
| Union-find over tree paths | $O(m \, \alpha(n))$ | $\Theta(n)$ | Each non-tree edge merges the classes along its tree path |

**Bridges, then components.** Run a DFS that skips only the one edge it entered a vertex by (by edge identity, so a parallel copy counts as a non-tree edge), and compute $d$ and $\mathrm{low}$. A tree edge from $p$ to $c$ is a bridge exactly when $\mathrm{low}[c] > d[p]$ (see [low-link values](/low-link/) and [bridge finding](/bridge-finding/)). Then run [connected components](/connected-components/) on the graph without the bridges.

**One pass.** Push each vertex on a stack when it is discovered. When the search returns from $c$ to its parent $p$ and $\mathrm{low}[c] > d[p]$, pop the stack down to $c$; the popped vertices form one class. After the root finishes, the vertices left on the stack form the class of the root. This mirrors [Tarjan's SCC algorithm](/tarjan-scc/), and the correctness proof has the same shape: the vertices above $c$ are the descendants of $c$ not yet assigned, and these are exactly the class of $c$.

**Union-find.** Take a spanning forest. A non-tree edge $\{u, v\}$ closes a cycle with the tree path from $u$ to $v$, so all vertices on that path are in one class. Merge them, jumping over already merged parts with a [disjoint-set](/disjoint-set/) structure. The tree edges that are never covered are the bridges. This method also handles edges that arrive one at a time.

## Bounds

- **Upper bound.** $\Theta(n + m)$ time and $\Theta(n)$ extra words, by the DFS methods.
- **Lower bound.** On adjacency lists any algorithm must read $\Omega(n + m)$ entries in the worst case. It must touch every vertex to label it. And if it leaves some entry unread, the adversary can let that entry be either a loop or a parallel copy of a bridge of the rest; the first answer keeps the bridge and the second removes it, so the outputs differ.
- **Equivalence with bridges.** Given the classes, the bridges are the edges whose ends have different labels; given the bridges, the classes are the components of $G - B$. Both conversions take $\Theta(n + m)$ time, so the two problems have the same complexity.

## Reductions

- **To bridge finding and connected components**, by the theorem above.
- **From strong orientation.** A connected graph has a [strong orientation](/strong-orientation/) exactly when it has one class. So deciding whether a strong orientation exists reduces to this problem.
- **To biconnected components.** The classes are the connected components of the union of all biconnected components that are not single bridges, so an algorithm for [biconnected components](/biconnected-components/) also solves this problem in linear time.
- **To maximum flow**, for one pair: $u \equiv v$ exactly when the maximum number of edge-disjoint $u$-$v$ paths is at least 2, which two augmenting paths decide in $O(m)$ time. This is useful for a single query, not for all classes.

## Applications

- **Network reliability.** In a communication or road network, a bridge is a single point of failure. The classes are the parts that survive any single link failure intact, and the bridge tree shows which failures cut which parts apart.
- **One-way streets.** By Robbins' theorem, the streets of a town can all be made one-way with every place still reachable from every other exactly when the street graph has one class. In general, the streets inside each class can be oriented strongly, and the bridges must stay two-way.
- **Path queries.** With the bridge tree and a [lowest common ancestor](/lowest-common-ancestor/) structure, the number of bridges that every $u$-$v$ path must cross is a tree distance, answered in $O(1)$ time after linear preprocessing.
- **Building blocks.** The classes are a first step for [edge connectivity](/edge-connectivity/) and for algorithms on 3-edge-connected components and on [ear decompositions](/ear-decomposition/).

## References
