---
tag: FD84D6
kind: data-structure
slug: block-cut-tree
name: Block-cut tree
aliases:
- Block tree
- Articulation tree
area: graphs/connectivity
level: core
summary: A tree whose nodes are the blocks and articulation points of a connected graph.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m)}
  space: {extra: Θ(n)}
prereqs: [biconnected-components, articulation-point, hopcroft-tarjan-biconnectivity]
see_also: [biconnected-graph, two-edge-connected-components, condensation-graph, lowest-common-ancestor, dynamic-biconnectivity, articulation-point-finding, bridge, ear-decomposition]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 3.1, 2-connected graphs and subgraphs (the block graph, and the lemma that the block graph of a connected graph is a tree)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 4.1, Cuts and connectivity (blocks and the block-cutpoint graph)
  - paper: "Frank Harary and Geert Prins, The block-cutpoint-tree of a graph, Publicationes Mathematicae Debrecen 13, 103 to 107 (1966)"
    locator: the definition of the block-cutpoint tree and the proof that it is a tree
  - paper: doi:10.1145/362248.362272
    title: John Hopcroft and Robert Tarjan, Algorithm 447, Efficient algorithms for graph manipulation, Communications of the ACM 16(6), 372 to 378 (1973)
    locator: the biconnected components algorithm used to build the tree
---

The block-cut tree of a connected [undirected graph](/undirected-graph/) has one node for each block (each [biconnected component](/biconnected-components/), bridge, or isolated vertex) and one node for each [articulation point](/articulation-point/), with an edge between a block and each articulation point in it. It is always a tree, and it shows how the graph hangs together: the blocks are the rooms and the articulation points are the doors between them. Built in $\Theta(n + m)$ time by one [depth-first search](/depth-first-search/), it answers questions such as "does every path from $u$ to $v$ pass through $x$?" and "do $u$ and $v$ lie on a common cycle?" by looking at a tree path. For a graph that is not connected, the same construction gives a forest with one tree for each component. It is the undirected cousin of the [condensation](/condensation-graph/) of a directed graph.

## In plain words

Cut a network at its weak points: the towns whose loss splits it. Each tightly knit piece that is left is a block. Now draw a small map with one dot for each block and one dot for each weak town, and join a block to each weak town that it touches.

This map never has a loop, so it is a tree. A trip from one town to another in the network must pass the weak towns on the tree path between them, in that order, and it need not pass any other weak town. So a question about all the routes in a big network becomes a question about one path in a small tree.

## The abstract type

The structure is built once from a graph and does not change. It offers:

- BUILD$(G)$: make the structure for the graph $G$ on the vertices $0, \ldots, n-1$.
- NODE$(v)$: the tree node of the vertex $v$: the cut node of $v$ if $v$ is an articulation point, and otherwise the one block that holds $v$.
- SEPARATES$(x, u, v)$, for distinct $u, v, x$ in one component: does every path from $u$ to $v$ pass through $x$?
- SAME-BLOCK$(u, v)$, for $u \neq v$: is there a block that holds both? For non-adjacent $u$ and $v$ this asks whether they lie on a common cycle.

The tree itself, with the vertex sets of the blocks, is also available for algorithms that work block by block.

## Representation

$G$ is given by $n$ and a list of edges, with parallel edges and [self-loops](/self-loop/) allowed. Loops are ignored, since a loop is a block of its own that touches one vertex and changes no articulation point. Parallel edges are handled by the Hopcroft-Tarjan search through edge identifiers.

- **Blocks.** The vertex sets $B_0, \ldots, B_{b-1}$ of the blocks of the non-loop edges, in the order in which the search closes them, and then a block $\{v\}$ for each vertex $v$ with no non-loop edge. Block $i$ is the tree node $i$.
- **Cut nodes.** The articulation points $x_0 < x_1 < \cdots < x_{c-1}$. The cut node of $x_j$ is the tree node $b + j$.
- **Tree.** Adjacency lists of the $b + c$ nodes, and for each node its parent, its children in order, and the interval $[\mathrm{tin}, \mathrm{tout}]$ of a depth-first search of the tree. Each tree is rooted at a block node.
- **Vertex map.** The array $\mathrm{node}[v]$.

**Invariants.** The node graph is a forest, every edge joins a block node to a cut node, every cut node has at least two neighbours, every root is a block node, a vertex lies in two or more blocks if and only if it is an articulation point, and $\mathrm{node}[v]$ is the cut node of $v$ or the one block that holds $v$. The implementation checks all of them in check_invariant.

**Size.** Let $k$ be the number of trees. An articulation point in $t$ blocks is counted $t$ times in the block sizes, so $\sum_i |B_i| = n + b - k$. In a tree with $b_t$ blocks and $n_t$ vertices, either the tree is one block $\{v\}$, or every block has at least two vertices, so $2 b_t \le n_t + b_t - 1$. Hence $b \le n$, the tree has $b + c \le 2n$ nodes and $b + c - k$ edges, and the structure takes $\Theta(n)$ space after BUILD.

## Operations

```pseudo id=main
BUILD(G)
L1  run the Hopcroft-Tarjan algorithm on G without loops: blocks B_0 .. B_{b−1}, articulation points A;
    add a block {v} for each vertex v with no non-loop edge
L2  make a block node β_i for each block, and a cut node γ_x for each x ∈ A
L3  for each block B_i and each x ∈ B_i ∩ A do add the tree edge {β_i, γ_x}
L4  for each v ∉ A do node[v] ← the β_i with v ∈ B_i; for each x ∈ A do node[x] ← γ_x
L5  root each tree at a block node; one depth-first search sets parent, children, tin and tout

ANCESTOR(a, c)                             ▷ is a an ancestor of c, or equal to c?
L6  return tin[a] ≤ tin[c] and tout[c] ≤ tout[a]

CHILD-TOWARD(a, c)                         ▷ a is a proper ancestor of c
L7  binary search the children of a, sorted by tin, for the last child s with tin[s] ≤ tin[c]; return s

SEPARATES(x, u, v)                         ▷ u, v, x distinct; u and v in one component
L8  if x ∉ A then return false
L9  g ← γ_x, a ← node[u], b ← node[v], p ← ANCESTOR(g, a), q ← ANCESTOR(g, b)
L10 if p ≠ q then return true              ▷ g is above exactly one of them
L11 if not p then return false             ▷ g is above neither
L12 return CHILD-TOWARD(g, a) ≠ CHILD-TOWARD(g, b)

SAME-BLOCK(u, v)                           ▷ u ≠ v
L13 a ← node[u], b ← node[v]
L14 if neither a nor b is a cut node then return a = b
L15 if exactly one is a cut node, say a, then return parent[b] = a or parent[a] = b
L16 return parent[parent[a]] = b or parent[parent[b]] = a or parent[a] = parent[b]
```

SEPARATES uses the fact that a node $g$ is on the tree path between $a$ and $b$ if and only if it is an ancestor of exactly one of them, or of both with $a$ and $b$ under different children of $g$. SAME-BLOCK uses the fact that the blocks that hold an articulation point $x$ are exactly the tree neighbours of $\gamma_x$: its parent and its children.

## Example

The graph has $n = 7$ vertices and 10 edges: a triangle $0, 1, 2$ with a second copy of $\{0, 1\}$, the edge $\{2, 3\}$, a triangle $3, 4, 5$, the edge $\{5, 6\}$, and a loop at 6. The search closes the blocks in the order

| block node | vertex set | kind |
|---|---|---|
| $\beta_0$ | $\{5, 6\}$ | bridge |
| $\beta_1$ | $\{3, 4, 5\}$ | biconnected |
| $\beta_2$ | $\{2, 3\}$ | bridge |
| $\beta_3$ | $\{0, 1, 2\}$ | biconnected, with a parallel edge |

and the articulation points are 2, 3 and 5, with the cut nodes $\gamma_2, \gamma_3, \gamma_5$. The loop at 6 gives no node. The tree is the path

$$\beta_3 - \gamma_2 - \beta_2 - \gamma_3 - \beta_1 - \gamma_5 - \beta_0,$$

rooted at $\beta_3$, the last block closed, which holds the start vertex 0 of the search. So $\mathrm{node}[0] = \mathrm{node}[1] = \beta_3$, $\mathrm{node}[4] = \beta_1$, $\mathrm{node}[6] = \beta_0$, and $\mathrm{node}[x] = \gamma_x$ for $x = 2, 3, 5$. The tree has $4 + 3 = 7$ nodes and 6 edges.

| query | tree reasoning | answer |
|---|---|---|
| SEPARATES$(3, 0, 6)$ | $\gamma_3$ is an ancestor of $\beta_0$ but not of $\beta_3$ | true |
| SEPARATES$(3, 4, 5)$ | $\gamma_3$ is an ancestor of both $\beta_1$ and $\gamma_5$, through the same child $\beta_1$ | false |
| SEPARATES$(2, 0, 1)$ | $\gamma_2$ is an ancestor of neither $\beta_3$ nor $\beta_3$ | false |
| SAME-BLOCK$(2, 3)$ | the parent of $\gamma_3$ is $\beta_2$, and the parent of $\beta_2$ is $\gamma_2$ | true: the bridge $\{2, 3\}$ |
| SAME-BLOCK$(3, 5)$ | both have the neighbour $\beta_1$: it is the parent of $\gamma_5$ and a child of $\gamma_3$ | true |
| SAME-BLOCK$(2, 5)$ | $\gamma_2$ and $\gamma_5$ are 4 steps apart | false |

## Correctness

The node graph is a forest: it is connected inside each component of $G$, because a path of $G$ moves from one block to the next only at a shared vertex, which is an articulation point. It has no cycle, because a cycle through $\beta$ and $\gamma_x$ in the node graph would give a path in $G - x$ between two neighbours of $x$ in different blocks, and such a path would put the two edges at $x$ on a common cycle.

A path of $G$ from $u$ to $v$, cut at the points where it moves from one block to the next, gives a walk in the tree from $\mathrm{node}[u]$ to $\mathrm{node}[v]$, and every such walk visits all nodes of the tree path. Conversely, along the tree path we can go through each block without touching an articulation point $x$ whose node is off the path, because each block stays connected without any one of its vertices. So $x$ separates $u$ from $v$ exactly when $\gamma_x$ is on the tree path, which lines L9 to L12 test with the intervals. The blocks that hold an articulation point are its tree neighbours, which gives SAME-BLOCK. The full proof is below.

## Complexity

| operation | time |
|---|---|
| BUILD | $\Theta(n + m)$ |
| NODE, ANCESTOR, SAME-BLOCK | $O(1)$ |
| CHILD-TOWARD, SEPARATES | $O(\log n)$, from the binary search over the children |

BUILD runs one depth-first search of $G$ and one of the tree, which has at most $2n$ nodes. During BUILD the stack of edges takes $O(m)$ space; after it, the blocks, the tree and the arrays take $\Theta(n)$ space.

SEPARATES can be made $O(1)$: test whether $g$ is the [lowest common ancestor](/lowest-common-ancestor/) of $a$ and $b$ with an $O(1)$ LCA structure, built in $O(n)$ time.

## Variants

- **Counting cut vertices on a path.** Store at each node the number of cut nodes on its path to the root. With an LCA query, the number of articulation points that every $u$-$v$ path must pass is a difference of these counts.
- **Block graph.** The graph whose vertices are the blocks, with two blocks adjacent when they share a vertex. It is not a tree in general (three blocks at one vertex form a triangle), so the block-cut tree is the more useful form.
- **Bridge tree.** Contract each [2-edge-connected component](/two-edge-connected-components/) to a node; the bridges are the edges of the tree. It answers "must every path from $u$ to $v$ use the edge $e$?" in the same way.
- **SPQR tree.** Splits each block further at pairs of vertices, for 3-connectivity. It is much harder to build.
- **Dynamic.** When edges are inserted and deleted, the tree changes; see [dynamic biconnectivity](/dynamic-biconnectivity/).

## When to use it

Use it when one graph gets many queries about single points of failure: which towns lie on every route between two towns, and whether two vertices share a cycle. Use it also to split an algorithm by blocks, for example on cactus graphs, where every block is an edge or a cycle and many hard problems become dynamic programs over the tree. For one query, a direct search of $G - x$ is simpler.

## Pitfalls

- **The vertex of a cut node.** An articulation point appears in several blocks. Use its cut node, not one of its blocks, as NODE$(x)$, or SEPARATES gives wrong answers for queries that start or end at an articulation point.
- **Isolated vertices.** A vertex with no edge, or only loops, is in no edge block. Give it a block of its own, or NODE is undefined there.
- **Loops in the vertex sets.** If loops are kept as blocks, a vertex with a loop lies in two blocks without being an articulation point, and the invariant "two or more blocks if and only if articulation point" fails.
- **Rooting at a cut node.** The test in line L16 assumes that cut nodes have parents. Root each tree at a block node.
- **Disconnected input.** The structure is a forest. SEPARATES$(x, u, v)$ has no meaning when $u$ and $v$ are in different components.

## Implementations

## History

Gallai and, independently, Harary and Prins (1966) introduced the tree of blocks and cut points; Harary and Prins called it the block-cutpoint tree and proved that it is a tree for every connected graph. The linear-time construction follows from the biconnected components algorithm of Hopcroft and Tarjan (1973).

## References
