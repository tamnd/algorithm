---
tag: YS9H4Q
kind: data-structure
slug: top-tree
name: Top tree
aliases:
- top trees
area: graphs/dynamic-graphs
level: research
summary: Hierarchical clustering of a dynamic tree that supports general path and subtree aggregates.
implements: [dynamic-tree]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [dynamic-tree, tree-contraction, binary-tree]
see_also: [rake-compress-tree, link-cut-tree, euler-tour-tree, frederickson-topology-trees, dynamic-tree-path-queries, holm-de-lichtenberg-thorup, tree-diameter, monoid]
sources:
  - paper: doi:10.1145/1103963.1103966
    title: Stephen Alstrup, Jacob Holm, Kristian de Lichtenberg and Mikkel Thorup, Maintaining information in fully dynamic trees with top trees, ACM Transactions on Algorithms 1(2), 243 to 264 (2005)
    locator: Sections 2 and 3 (clusters, boundary vertices, the merges compress and rake, the interface link, cut and expose, O(log n) time per operation via topology trees) and the applications to diameters, centers and medians
  - paper: "Robert E. Tarjan and Renato F. Werneck, Self-adjusting top trees, Proceedings of the 16th ACM-SIAM Symposium on Discrete Algorithms (SODA 2005), 813 to 822"
    locator: the whole paper (top trees built on a rake-compress decomposition of splay trees, O(log n) amortized time per operation)
  - paper: doi:10.1137/0214055
    title: Greg N. Frederickson, Data structures for on-line updating of minimum spanning trees, with applications, SIAM Journal on Computing 14(4), 781 to 798 (1985)
    locator: the topology trees on which the worst-case implementation of top trees is built
---

A top tree represents each tree of a dynamic forest by a binary tree of **clusters**: connected sets of edges with at most two **boundary vertices**, where each inner cluster is the merge of two child clusters that share a vertex. A merge is a **compress**, which joins two path clusters at a vertex of degree two, or a **rake**, which hangs a point cluster on another cluster. The user stores information in the clusters and gives two functions that combine the information of the two children; the structure calls them and never looks inside. The operation expose$(u, v)$ makes $u$ and $v$ the boundary of the root, so the root holds the aggregate of the path from $u$ to $v$, and with suitable information also of whole trees, subtrees, diameters, centers and medians. Alstrup, Holm, de Lichtenberg and Thorup (1997, journal 2005) introduced top trees, with link, cut and expose in $O(\log n)$ worst-case time, deterministically; they are fully dynamic.

## In plain words

Cut a tree into small pieces, each a few connected edges. Glue the pieces two at a time into larger pieces, and keep gluing until one piece is the whole tree. Each piece may touch the rest of the tree at no more than two points, so it acts like a single edge or like a single dangling branch.

Each piece carries a small note, such as the length of the route between its two touching points. When two pieces are glued, the note of the new piece is computed from the two old notes only.

To ask about the route between two vertices, ask the structure to keep those two vertices as the touching points of the whole tree. The note at the top then answers the question. Changes to the tree regroup only a few pieces.

## The abstract type

The structure keeps a forest on the vertices $0, \ldots, n - 1$, with a weight on each edge, and supports:

- **link**$(u, v, w)$: add the edge $\{u, v\}$ with weight $w$, if $u$ and $v$ are in different trees;
- **cut**$(u, v)$: remove the edge $\{u, v\}$;
- **expose**$(u, v)$: return the root cluster of the tree of $u$ and $v$ with boundary $\{u, v\}$, or nil if they are in different trees; expose$(u, u)$ returns the root with boundary $\{u\}$.

The user supplies the information in a base cluster (one edge) and two functions: **compress**$(A, B)$ for two path clusters $(a, c)$ and $(c, b)$, and **rake**$(A, B)$ for a point cluster $A$ hung on $B$. Path sum, path maximum, the total weight of a tree, and the [diameter of a tree](/tree-diameter/) are all such information. This implementation keeps the path sum, the path maximum and the total weight, and offers path sum, path max, tree total and connected. It is the most general form of the [dynamic tree](/dynamic-tree/) interface.

## Representation

For a cluster $C$ in a tree $T$, a vertex of $C$ is a **boundary vertex** if it touches an edge of $T$ outside $C$ or is one of the exposed vertices. A cluster with two boundary vertices $a, b$ is a **path cluster**, and its **cluster path** is the tree path from $a$ to $b$; a cluster with one boundary vertex is a **point cluster**. The two merges are:

- **compress**: path clusters $(a, c)$ and $(c, b)$, where $c$ is not exposed and has no other edges, become the path cluster $(a, b)$; its path is the union of the two paths;
- **rake**: a point cluster at $c$ and another cluster with $c$ on its boundary become a cluster with the boundary of the second; its path is that of the second.

A **top tree** of $T$ is a binary tree whose leaves are the edges of $T$, whose inner nodes are these merges, and whose root is $T$ itself. The implementation builds it by contraction, as in a [rake-compress tree](/rake-compress-tree/), but keeps the exposed vertices $u$ and $v$ out of every rake and compress, and splits each removal into binary merges.

```pseudo id=main
EXPOSE(u, v)
L1  make a base cluster for each edge of the tree of u; u and v are exposed
L2  while a vertex other than u and v is live:
L3      choose each live leaf x that is not exposed (of two adjacent leaves, the smaller)
L4      choose live x of degree 2, not exposed, coin heads, neighbor coins tails, no unexposed leaf neighbor; if none is chosen, choose one
L5      for each chosen leaf x with neighbor y: rake the point cluster at x onto the edge cluster (x, y); hang the result at y
L6      for each chosen x of degree 2 with edges (a, x), (x, b): rake its point cluster onto (a, x); compress into (a, b)
L7  rake the point clusters at u and v onto the path cluster (u, v), or join them at u if u = v
L8  return the root; path queries read its path information
```

Line L4 picks an independent set of degree-two vertices by coins; when only the path from $u$ to $v$ is left and no coin is right, it compresses one vertex anyway, so every round makes progress. Each removal of line L5 or L6 is a sequence of binary merges, so every cluster above the edges has exactly two children.

## Operations

**Link and cut.** In the structures of the papers, a link or a cut changes $O(\log n)$ clusters: the top tree is cut into the top trees of the parts on the way up, and the user information of each new cluster is computed again by compress and rake. The implementation on this page keeps only the edge set and builds the top tree of the exposed tree in each expose, in time linear in the size of that tree, expected over the coins; this shows the clusters and the merges, not the update bound.

**Expose.** Alstrup et al. reach expose$(u, v)$ by changing $O(\log n)$ clusters near the root so that $u$ and $v$ become boundary vertices of the root, using topology trees of [Frederickson](/frederickson-topology-trees/) on a ternary version of the tree. Tarjan and Werneck reach it with splay trees, as in [link-cut trees](/link-cut-tree/): the path from $u$ to $v$ becomes the root path, and the other subtrees are raked onto it.

**Queries.** Path sum and path max read the root after expose$(u, v)$. The total weight of the tree of $u$ is the total of the root after expose$(u, u)$. Non-local queries, such as the center or the median of a tree, descend from the root and choose at each merge the child that holds the answer, using only the information of the two children.

## Example

Take the tree on 7 vertices with the edges $01$ (weight 4), $12$ (1), $23$ (7), $14$ (2), $45$ (3) and $56$ (5), with the seed 3, and call expose$(3, 6)$. Vertices 3 and 6 stay; the others are removed in this order, each by binary merges:

| removed | merges | new cluster | path sum | path max | total |
|---|---|---|---|---|---|
| 0 (rake) | the leaf edge $01$ becomes a point cluster at 1 | point at 1 | | | 4 |
| 4 (compress) | $(1, 4) + (4, 5)$ | $(1, 5)$ | 5 | 3 | 5 |
| 5 (compress) | $(1, 5) + (5, 6)$ | $(1, 6)$ | 10 | 5 | 10 |
| 1 (compress) | rake the point at 1 onto $(1, 2)$, then $(2, 1) + (1, 6)$ | $(2, 6)$ | 11 | 5 | 15 |
| 2 (compress) | $(3, 2) + (2, 6)$ | $(3, 6)$ | 18 | 7 | 22 |

The root is the path cluster $(3, 6)$. Its path sum 18 is $7 + 1 + 2 + 3 + 5$, its path max 7 is the edge $23$, and its total 22 is the weight of the whole tree, which includes the edge $01$ off the path. The raked point cluster adds to the total but not to the path values, exactly as the rake function says.

## Correctness

Each cluster made by the contraction is a connected set of edges, and its boundary is the set of its vertices that are exposed or touch edges outside it; this holds for the base clusters and is kept by every merge, because a compress removes only the vertex $c$, which has no other edges, and a rake removes only a leaf vertex that is not exposed. So the cluster path of a compress is the concatenation of the two cluster paths, and the information computed by the user's compress is that of the joined path; a rake keeps the path of its second argument. When the loop ends, only $u$ and $v$ are live, the live edge between them is a path cluster whose cluster path is the tree path from $u$ to $v$, and every other edge lies in a point cluster at $u$ or $v$; raking these keeps the path. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Papers.** Link, cut and expose take $O(\log n)$ worst-case time in the structure of Alstrup et al., and $O(\log n)$ amortized time in the self-adjusting top trees of Tarjan and Werneck, each with $O(\log n)$ calls to the user's merge functions, assuming they take constant time. Non-local searches take $O(\log n)$ time as well.
- **Space.** $\Theta(n)$: a top tree of a tree with $m$ edges has $m$ leaves and $m - 1$ merges.
- **This implementation.** Expose on a tree with $k$ vertices takes $O(k)$ expected time, with $O(\log k)$ rounds of contraction in expectation; link and cut take $O(k)$ time to check connectivity. It is meant as a reference for the merges and for testing, not for speed.
- **Determinism.** The structure of Alstrup et al. is deterministic, and so is the splay-based one. The coins of this implementation are a fixed hash of the vertex and the round.

## Variants

- **Self-adjusting top trees.** Tarjan and Werneck (2005) implement top trees on a rake-compress view of splay trees, with amortized bounds and good speed in practice; they also give contracting variants and compare them with link-cut trees and [Euler tour trees](/euler-tour-tree/).
- **Rake-compress trees.** [RC-trees](/rake-compress-tree/) also use clusters with at most two boundary vertices, built by randomized contraction and kept by change propagation; they have no exposed path, and path queries walk up the cluster tree.
- **Topology trees.** [Frederickson's topology trees](/frederickson-topology-trees/) cluster vertices of a tree of degree at most three, and were the first structure of this kind; top trees can be built on them.
- **Applications.** Top trees keep the diameter, center and median of dynamic trees, and they are used for the trees inside fully dynamic 2-edge connectivity and biconnectivity, as in the [Holm-de Lichtenberg-Thorup algorithm](/holm-de-lichtenberg-thorup/), and for [dynamic tree path queries](/dynamic-tree-path-queries/) in general.

## When to use it

Use top trees when a forest changes by links and cuts and the queries need information that is not just a sum along a path or over a subtree: the farthest vertex, the diameter, the center, or the nearest marked vertex. For path aggregates only, a [link-cut tree](/link-cut-tree/) is simpler; for connectivity and subtree sums, an [Euler tour tree](/euler-tour-tree/) is simpler. Top trees pay off when the merge functions are natural and the alternative would be a special structure for each query.

## Pitfalls

- **Rake keeps the path of the second cluster.** The point cluster's own path information must not enter the path values of the result; only its totals do. Mixing them gives path sums that count side branches.
- **Exposed vertices are boundary vertices.** A compress at an exposed vertex would hide the end of the query path. The vertices $u$ and $v$ must never be removed during expose.
- **Leaf edges are point clusters.** An edge to a leaf that is not exposed has only one boundary vertex, so its path values have no meaning above it.
- **Orientation of path clusters.** For non-commutative information, such as the sequence of edges along a path, a compress must know which boundary vertex is which; the merge functions need the orientation, or the cluster must store both directions.
- **Expensive merge functions.** The time bounds count calls to the merge functions; information of size more than constant, such as a sorted list, makes each call slow.

## Implementations

## History

Frederickson (1985) introduced topology trees, which cluster the vertices of a tree of bounded degree hierarchically, for dynamic minimum spanning trees. Alstrup, Holm, de Lichtenberg and Thorup presented top trees at ICALP 1997, with diameters of dynamic trees as an application, and published the full paper in ACM Transactions on Algorithms in 2005, where they define the interface with user merge functions and expose. Tarjan and Werneck (2005) gave self-adjusting top trees based on splay trees, and with Werneck's thesis showed that they are practical. Later work gave simpler implementations of top trees on top of splay trees.

## References
