---
tag: 4WXY88
kind: problem
slug: connected-components
name: Connected components
aliases:
- Connected component labeling
- Weakly connected components (directed)
area: graphs/connectivity
level: intro
summary: Partition the vertices of an undirected graph into maximal sets that are mutually reachable.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m)}
prereqs: [connected-graph, depth-first-search]
see_also: [generic-component-growing, breadth-first-search, union-find-connectivity, spanning-forest, strongly-connected-components, weakly-connected-graph, dynamic-connectivity, flood-fill]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 19.1, Disjoint-set operations (the procedure CONNECTED-COMPONENTS), Section 20.3, Depth-first search, and Appendix B.4, Graphs
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.5, Case study, union-find, and Section 4.1, Undirected graphs (the class CC, connected components with depth-first search)
  - paper: doi:10.1145/362248.362272
    title: John Hopcroft and Robert Tarjan, Algorithm 447, Efficient algorithms for graph manipulation, Communications of the ACM 16(6), 372 to 378 (1973)
    locator: the whole paper (linear-time partition into connected components and biconnected components)
  - paper: doi:10.1145/1391289.1391291
    title: Omer Reingold, Undirected connectivity in log-space, Journal of the ACM 55(4), Article 17 (2008)
    locator: the main theorem (undirected s-t connectivity in deterministic logarithmic space)
---

The connected components problem asks to split the vertices of an [undirected graph](/undirected-graph/) into its *components*: the largest sets of vertices in which each two vertices are joined by a path. Each component, with the edges inside it, is a [connected graph](/connected-graph/), and no edge runs between two components. One [depth-first search](/depth-first-search/) or [breadth-first search](/breadth-first-search/) solves it in $\Theta(n + m)$ time, which is optimal, and a [disjoint-set](/disjoint-set/) structure solves it while the edges arrive one at a time. It is the first step of many graph programs, because most questions about a graph can be answered for each component on its own.

## In plain words

Think of a road map of many islands with bridges between some of them. Two towns are in the same group when you can drive from one to the other, maybe through other towns. The groups are the components. Each town is in exactly one group, and no road leaves a group.

To find the groups, start at any town that has no group yet, and visit every town that you can reach from it. All of them form one group. Then pick a new town that has no group yet and do the same. When every town has a group, you are done. Each road is looked at a fixed number of times, so the work grows with the number of towns plus the number of roads.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $V = \{0, 1, \ldots, n-1\}$ and $m = |E|$, usually given as [adjacency lists](/adjacency-list/). Parallel edges and [self-loops](/self-loop/) are allowed. They never change the answer, because a path never uses a loop or two copies of one edge.

**Relation.** Write $u \sim v$ when $G$ has a path from $u$ to $v$. This is an [equivalence relation](/equivalence-relation/) (see [connected graph](/connected-graph/) for the proof). Its classes $C_1, \ldots, C_k$ are the *components*. The subgraph induced by a class contains every edge that touches the class, since the two ends of an edge are joined by a path of length 1.

**Output.** The number $k$ of components and a label $c : V \to \{0, 1, \ldots, k-1\}$ such that

$$\forall u, v \in V : \quad c(u) = c(v) \iff u \sim v.$$

Any numbering of the classes is a correct answer. Programs often fix one: the classes are numbered in the order of their smallest vertex, or each vertex is labelled by the smallest vertex of its class.

**Directed graphs.** For a [directed graph](/directed-graph/), the *weakly connected components* are the components of the undirected graph that forgets the directions. The [strongly connected components](/strongly-connected-components/) are a different problem: they need a directed path in both directions.

## Variants

- **Counting.** Output only $k$. The lower bound below also holds for this variant, because each input pair in its proof has two different values of $k$.
- **Queries.** Answer many questions "is $u \sim v$?". After one labelling, each question takes $O(1)$ time. One question alone is undirected [graph reachability](/graph-reachability/).
- **Spanning forest.** Output a [spanning forest](/spanning-forest/): one tree for each component. A search gives it for free through its parent pointers, and $m - (n - k)$ edges are not in it.
- **Incremental.** The edges arrive one by one and queries come between them. [Union-find connectivity](/union-find-connectivity/) answers in $O(\alpha(n))$ amortized time per operation. See [incremental connectivity](/incremental-connectivity/).
- **Decremental and fully dynamic.** Edges are also deleted. See [decremental connectivity](/decremental-connectivity/) and [dynamic connectivity](/dynamic-connectivity/).
- **Pixel images.** The vertices are pixels and the edges join neighbouring pixels of the same colour. This is [flood fill](/flood-fill/) or component labelling in image processing, where scan-line methods and union-find are common.
- **Weak components of a directed graph.** Add each edge in both directions and solve the undirected problem.

## Examples

The graph has $n = 9$ vertices and these 9 edges: $\{0,1\}$, $\{1,2\}$, $\{2,0\}$, $\{3,4\}$ twice (parallel), $\{5,6\}$, $\{6,7\}$, $\{5,7\}$, and the loop $\{8,8\}$.

| vertex | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| label $c$ | 0 | 0 | 0 | 1 | 1 | 2 | 2 | 2 | 3 |

So $k = 4$, and the components are $\{0, 1, 2\}$, $\{3, 4\}$, $\{5, 6, 7\}$ and $\{8\}$. The vertex 8 has a loop but no other neighbour, so it is a component alone. A spanning forest has $n - k = 5$ edges, so $9 - 5 = 4$ edges are left out: one edge of each triangle, one of the two parallel edges, and the loop.

More small cases:

| graph | $n$ | $m$ | $k$ |
|---|---|---|---|
| no edges | $n$ | 0 | $n$ |
| a path or a tree | $n$ | $n - 1$ | 1 |
| a [complete graph](/complete-graph/) $K_n$ | $n$ | $n(n-1)/2$ | 1 |
| a forest | $n$ | $m$ | $n - m$ |
| the empty graph | 0 | 0 | 0 |

The forest row holds because each tree with $t$ vertices has $t - 1$ edges, so a forest with $k$ trees has $n - k$ edges.

**Non-example of a correct output.** For the graph above, the labels $[0, 0, 0, 1, 1, 1, 1, 1, 2]$ are wrong: they put 4 and 5 in one class, but no path joins them. The labels $[0, 0, 1, 2, 2, 3, 3, 3, 4]$ are also wrong: they split the triangle $\{0, 1, 2\}$.

## Known algorithms

| algorithm | time | extra space | remark |
|---|---|---|---|
| [Depth-first search](/depth-first-search/) from each unlabelled vertex | $\Theta(n + m)$ | $\Theta(n)$ | each search tree is one component |
| [Breadth-first search](/breadth-first-search/) from each unlabelled vertex | $\Theta(n + m)$ | $\Theta(n)$ | the same, with a queue |
| [Generic component growing](/generic-component-growing/) | $\Theta(n + m)$ | $\Theta(n)$ | the common frame of both searches |
| [Union-find connectivity](/union-find-connectivity/) | $O(n + m \, \alpha(n))$ | $\Theta(n)$ | reads the edges in any order, once; fits a stream of edges |

The searches need the adjacency lists. The union-find method needs only the list of edges, so it is the usual choice when the edges come from a file or a stream, or when edges keep arriving. Here $\alpha$ is the inverse Ackermann function, which is at most 4 for each practical $n$; the bound is the [union-find amortized bound](/union-find-amortized-bound/).

## Bounds

**Upper bound.** $O(n + m)$ time in the [word RAM](/word-ram/) model with adjacency lists, by one search from each unlabelled vertex. Each vertex is labelled once and each list is scanned once.

**Lower bound.** In the same model, each deterministic algorithm reads $\Omega(n + m)$ list entries in the worst case.

*Proof.* For the term $n$: let $G$ have some isolated vertices. If the algorithm never reads the lists of two isolated vertices $x$ and $y$, it gives the same output when the edge $\{x, y\}$ is added to both lists, but then $x$ and $y$ must get the same label and $k$ drops by one. So it reads all but at most one list. For the term $m$: let $H$ be the [complete graph](/complete-graph/) $K_t$ with $t \ge 3$, which has $t(t-1)/2$ edges and no [bridge](/bridge/), and let $G$ be two disjoint copies $A$ and $B$ of $H$, plus any number of isolated vertices, so that $m = t(t-1)$. Suppose that the algorithm, run on $G$, never reads either list entry of some edge $\{a_1, a_2\}$ of $A$ and never reads either list entry of some edge $\{b_1, b_2\}$ of $B$. Change the four unread entries: in the list of $a_1$, the entry $a_2$ becomes $b_2$; in the list of $a_2$, $a_1$ becomes $b_1$; in the list of $b_1$, $b_2$ becomes $a_2$; in the list of $b_2$, $b_1$ becomes $a_1$. The result $G'$ is a valid graph with the same degrees, in which $\{a_1, a_2\}$ and $\{b_1, b_2\}$ are replaced by $\{a_1, b_2\}$ and $\{b_1, a_2\}$. Since $\{a_1, a_2\}$ is not a bridge, $A$ minus this edge is still connected, and the same holds for $B$, so $A$ and $B$ form one component in $G'$. The algorithm reads the same entries on $G$ and on $G'$, so it gives the same output, but the correct outputs differ. So the algorithm reads an entry of every edge of $A$ or of every edge of $B$: at least $m/2$ entries. $\square$

**Space.** Reingold (2008) showed that undirected s-t connectivity, and with it the count of components, can be decided in deterministic $O(\log n)$ space on a Turing machine that reads the graph from a read-only input. The time of that method is a large polynomial, so it matters for complexity theory, not for programs.

## Reductions

- **Components reduce to a spanning forest, and back.** A spanning forest gives the labels by one search on the forest, in $O(n)$ time. The labels give a spanning forest only with one more pass over the edges, for example with union-find.
- **Bipartiteness reduces to components.** Build the *double cover*: two copies $v^0$ and $v^1$ of each vertex, and the edges $\{u^0, v^1\}$ and $\{u^1, v^0\}$ for each edge $\{u, v\}$. A component of $G$ gives two components of the cover if it is bipartite, and one if it has an odd cycle. So $G$ is bipartite if and only if the cover has exactly $2k$ components. The cover has $2n$ vertices and $2m$ edges. See [bipartite testing](/bipartite-testing/).
- **Weak components reduce to components.** Add each directed edge as an undirected edge, in $O(n + m)$ time.
- **Kruskal's algorithm uses incremental components.** [Kruskal's algorithm](/kruskal/) adds an edge exactly when its two ends are in different components of the edges chosen so far.

## Applications

- Split a graph into its components, then run an expensive algorithm (colouring, matching, layout) on each part alone.
- Check that a network is connected, for example that every computer can reach every other one, or that a [spanning tree](/spanning-tree/) exists.
- Label regions of an image: objects in a binary image, areas of one colour in a paint program ([flood fill](/flood-fill/)).
- Single-linkage clustering: join each two points closer than a threshold, then take the components.
- Measure random networks, where the size of the largest component (the [giant component](/giant-component/)) is the main quantity of [percolation](/percolation/).

## References
