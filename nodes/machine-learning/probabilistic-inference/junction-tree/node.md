---
tag: 1CEHTH
kind: data-structure
slug: junction-tree
name: Junction tree
aliases:
- clique tree
- join tree
- junction tree of a triangulated graph
area: machine-learning/probabilistic-inference
level: advanced
summary: "A tree whose nodes are the maximal cliques of a triangulated graph, in which the cliques that hold any one vertex form a connected subtree."
model: word-ram
complexity:
  vars: {n: the number of vertices, k: the number of cliques, w: the induced width of the order}
  time: {worst: "O(n^3)"}
  space: {extra: "O(n w + k)"}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [elimination-ordering, chordal-graph, tree-decomposition, maximum-spanning-tree]
see_also: [junction-tree-algorithm, variable-elimination, perfect-elimination-ordering, treewidth, kruskal, maximum-cardinality-search, belief-propagation, bayesian-network]
sources:
  - paper: "Finn V. Jensen and Frank Jensen, Optimal junction trees, Proceedings of the Tenth Conference on Uncertainty in Artificial Intelligence (UAI 1994), pages 360 to 366"
    title: Jensen and Jensen 1994
    locator: a spanning tree of the clique graph of a triangulated graph is a junction tree exactly when it has maximum total separator weight
  - paper: doi:10.1111/j.2517-6161.1988.tb01721.x
    title: "Steffen L. Lauritzen and David J. Spiegelhalter, Local computations with probabilities on graphical structures and their application to expert systems, Journal of the Royal Statistical Society, Series B 50(2), 1988, pages 157 to 224"
    locator: the moral graph, triangulation, and the ordering of the cliques with the running intersection property
  - paper: doi:10.1016/0095-8956(74)90094-X
    title: "Fănică Gavril, The intersection graphs of subtrees in trees are exactly the chordal graphs, Journal of Combinatorial Theory, Series B 16(1), 1974, pages 47 to 56"
    locator: the characterization of chordal graphs by trees of their cliques
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, Principles and Techniques, MIT Press, 2009
    locator: "Chapter 10, Section 10.1 (clique trees, the running intersection property) and Section 10.4 (constructing a clique tree from a chordal graph by a maximum spanning tree)"
---

A junction tree (also called a clique tree or join tree) of a [chordal graph](/chordal-graph/) $H$ is a tree whose nodes are the maximal [cliques](/clique/) of $H$, such that for each vertex $x$ the cliques that hold $x$ form a connected subtree. This is the *running intersection property*. Each tree edge carries a *separator*, the intersection of its two cliques. A junction tree is a [tree decomposition](/tree-decomposition/) whose bags are cliques, and it is the data structure on which the [junction tree algorithm](/junction-tree-algorithm/) does exact inference. One way to build it: triangulate the graph along an [elimination ordering](/elimination-ordering/), keep the maximal cliques, and join them by a [maximum spanning tree](/maximum-spanning-tree/) with the separator sizes as weights.

## In plain words

Many graphs have loops, and loops make exact inference hard. A junction tree removes the loops by grouping the vertices into overlapping groups, the cliques, and arranging the groups in a tree.

The groups must agree with each other. If two groups both hold a vertex, every group on the tree path between them must hold it too. Then information about that vertex can travel along the path without loss.

To get such groups, add edges until every long cycle has a shortcut. Then the largest fully connected groups are the nodes. To link them, prefer the pairs that share the most vertices. The tree you get this way always has the agreement rule.

## The abstract type

The structure stores a set of cliques of a graph on the vertices $0, \ldots, n-1$ and a tree on them, and it supports these operations:

- BUILD$(G, \pi)$: make the junction tree of $G$ triangulated along the order $\pi$.
- SEPARATORS(): the separator $C_i \cap C_j$ of each tree edge $\{i, j\}$.
- FIND-CLIQUE$(S)$: a clique that holds the whole set $S$, or none. The junction tree algorithm uses it to place each factor of a model in one clique.
- PATH$(a, b)$: the cliques on the tree path from $a$ to $b$.
- WIDTH(): the size of the largest clique minus one.

There is no insert or delete: a change of the graph means a new build.

## Representation

A list of cliques $C_1, \ldots, C_k$, each a set of vertices, and a list of $k - 1$ tree edges $\{i, j\}$. The invariant has three parts:

1. **Tree.** The edges form a spanning tree on the $k$ cliques.
2. **Cover.** Each vertex of $G$ is in some clique, and for each edge $uv$ of $G$ some clique holds both $u$ and $v$.
3. **Running intersection.** For each vertex $x$, the cliques that hold $x$ induce a connected subtree. Equivalently, for each two cliques $C_i$, $C_j$, the set $C_i \cap C_j$ lies in every clique on the path between them.

The separators need not be stored: each is the intersection of the two cliques at its edge. A separator $S_{ij}$ splits the tree, and in a probabilistic model it makes the variables on the two sides [conditionally independent](/conditional-independence/) given $S_{ij}$.

## Operations

```pseudo id=main
BUILD-JUNCTION-TREE(G, π)
L1  H ← G; C ← an empty list
L2  for each vertex v in the order π do
L3      B ← {v} ∪ N_H(v)                         ▷ v and its current neighbours
L4      join each pair of N_H(v) in H; delete v from H
L5      if B is not a subset of a clique in C then append B to C
L6  for each pair i < j of cliques do weight(i, j) ← |C_i ∩ C_j|
L7  sort the pairs by weight, largest first
L8  for each pair (i, j) in this order do         ▷ Kruskal with union-find
L9      if C_i and C_j are in different trees then
L10         add the tree edge (i, j); join the two trees
```

Lines L1 to L5 are the elimination of [variable elimination](/variable-elimination/), done on the graph only. Each set $B$ is $v$ with its later neighbours in the filled graph $G_\pi^+$, and it is a clique there. Line L5 keeps exactly the maximal cliques: a maximal clique is the set $B$ of its first vertex in $\pi$, and the other sets lie inside an earlier one. So $k \le n$. Lines L6 to L10 are [Kruskal's algorithm](/kruskal/) with the largest weights first, which gives a maximum weight spanning tree of the clique graph. The pairs of weight 0 are in the list, so a disconnected graph still gets one tree.

With $k \le n$ cliques, the elimination costs $O(n^3)$ with adjacency sets in the worst case, the $k^2/2$ weights cost $O(k^2 n)$, the sort $O(k^2 \log k)$ and Kruskal $O(k^2 \alpha(k))$. So the build costs $O(n^3)$.

FIND-CLIQUE$(S)$ scans the cliques in $O(k n)$ time; an index from each vertex to its cliques makes it faster. PATH$(a, b)$ is a search in the tree, in $O(k)$ time. SEPARATORS costs $O(k n)$.

## Example

**A cycle of length five.** Let $G$ be the cycle $0, 1, 2, 3, 4$ with the order $\pi = (0, 1, 2, 3, 4)$.

| step | $v$ | current neighbours | fill edges | $B$ | kept? |
|---|---|---|---|---|---|
| 1 | 0 | 1, 4 | 1-4 | {0, 1, 4} | yes |
| 2 | 1 | 2, 4 | 2-4 | {1, 2, 4} | yes |
| 3 | 2 | 3, 4 | none | {2, 3, 4} | yes |
| 4 | 3 | 4 | none | {3, 4} | no, inside {2, 3, 4} |
| 5 | 4 | none | none | {4} | no |

The clique graph has the weights $|C_1 \cap C_2| = |\{1, 4\}| = 2$, $|C_2 \cap C_3| = |\{2, 4\}| = 2$ and $|C_1 \cap C_3| = |\{4\}| = 1$. Kruskal takes the two edges of weight 2, so the tree is the path $\{0,1,4\} - \{1,2,4\} - \{2,3,4\}$ with the separators $\{1, 4\}$ and $\{2, 4\}$. Vertex 4 is in all three cliques, vertex 1 in the first two, vertex 2 in the last two: each set is connected. The width is 2, the treewidth of a cycle.

The other spanning tree with the edge of weight 1, $\{1,2,4\} - \{0,1,4\} - \{2,3,4\}$, has weight 3 instead of 4, and it breaks the property: vertex 2 is in the two end cliques but not in the middle one.

**The sprinkler network.** The moral graph of $C \to S$, $C \to R$, $S \to W$, $R \to W$ has the edges $CS$, $CR$, $SR$, $SW$, $RW$. With the order $(W, C, S, R)$ no fill is needed, the cliques are $\{S, R, W\}$ and $\{C, S, R\}$, and the one separator is $\{S, R\}$.

## Correctness

The proof has four steps. (1) Line L5 keeps exactly the maximal cliques of the filled graph $H = G_\pi^+$. (2) Some tree on these cliques has the running intersection property, by induction along the reverse of $\pi$. (3) The theorem of Jensen and Jensen: a spanning tree $T$ of the clique graph has the property if and only if it has maximum weight. The key identity is
$$\sum_{\{i,j\} \in T} |C_i \cap C_j| = \sum_x |E(T_x)| \le \sum_x (k_x - 1),$$
where $k_x$ is the number of cliques that hold $x$ and $T_x$ is the forest of tree edges whose two ends hold $x$; equality holds exactly when each $T_x$ is connected. (4) Kruskal returns a maximum weight spanning tree. So the result keeps all three parts of the invariant, and it is a tree decomposition of $G$ of width $w(\pi)$. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

The costs are in the [word RAM](/word-ram/) model, worst case.

| operation | time | notes |
|---|---|---|
| BUILD | $O(n^3)$ | elimination $O(n^3)$, weights $O(k^2 n)$, sort and Kruskal $O(k^2 \log k)$, with $k \le n$ |
| SEPARATORS | $O(k n)$ | one intersection per tree edge |
| FIND-CLIQUE | $O(k n)$ | a scan; $O(1)$ per clique with bit sets |
| PATH | $O(k)$ | a search in the tree |

**Space.** The cliques hold $\sum_i |C_i| \le n (w + 1)$ vertices in total, where $w$ is the induced width of the order, and the tree has $k - 1 \le n - 1$ edges. The list of all pairs used by the build is temporary and has $O(k^2)$ entries.

Faster builds exist. On a chordal graph with $m$ edges, [maximum cardinality search](/maximum-cardinality-search/) gives a perfect elimination ordering and, with it, the cliques and a clique tree in $O(n + m)$ time (Tarjan and Yannakakis 1984). The cost that matters for inference is not the build but the size of the clique tables, $\sum_i d^{|C_i|}$ for domains of size $d$.

## Variants

- **Binary join trees.** Shenoy split the nodes so that each has at most three neighbours, which lowers the cost of the messages of the Shafer-Shenoy architecture.
- **Nonmaximal cliques.** Some builds keep a bag for each eliminated vertex, the sets $B$ of line L3, and join each bag to the bag of its first later neighbour. This is a valid tree decomposition, with more nodes; contracting each nonmaximal bag into a neighbour that holds it gives the junction tree.
- **Weights with domain sizes.** When the variables have different domain sizes, the triangulation should minimize the total table size $\sum_i \prod_{x \in C_i} d_x$, not the width. Among maximum weight spanning trees, Jensen and Jensen break ties by the cost of the separators.
- **Hypergraphs and databases.** In database theory, a join tree of an acyclic hypergraph is the same object: the hyperedges are the nodes, and the running intersection property is the condition of acyclicity.

## When to use it

Build a junction tree when the same model must answer many queries: all single-variable marginals, or the same marginals under many sets of evidence. The build is done once, and each query costs two passes of messages over the tree. For a single query, [variable elimination](/variable-elimination/) is simpler and needs no tree. When the largest clique is too big for its table to fit in memory, the junction tree is not practical, and approximate methods such as [loopy belief propagation](/loopy-belief-propagation/) are used instead.

## Pitfalls

- **A tree that is not of maximum weight.** Joining the cliques by any spanning tree, for example the order in which they were found, can break the running intersection property, as in the cycle example. Use the largest weights first in line L7.
- **Cliques of a graph that is not chordal.** The maximal cliques of a graph with a chordless cycle of length 4 or more have no junction tree. The triangulation of lines L3 and L4 is needed first.
- **Missing the moral edges.** For a [Bayesian network](/bayesian-network/), the graph to triangulate is the moral graph, in which the parents of each node are joined. Without the moral edges, some conditional table has no clique that holds its whole scope.
- **Keeping nonmaximal cliques by mistake.** A test in line L5 against only the last clique, or no test, keeps subsets as nodes. The result can still be a valid decomposition, but the maximum spanning tree argument then needs care with ties, and the tree is larger.

## Implementations

## History

Clique trees of chordal graphs go back to the graph theory of the 1970s: Gavril (1974) proved that the chordal graphs are exactly the intersection graphs of subtrees of a tree, which is the existence of a tree of cliques. Lauritzen and Spiegelhalter (1988) made the moral graph, its triangulation and an ordering of the cliques with the running intersection property the base of exact inference in expert systems. Jensen and Jensen (1994) showed that the junction trees of a triangulated graph are exactly the maximum weight spanning trees of its clique graph, and used this to find junction trees of least cost.

## References
