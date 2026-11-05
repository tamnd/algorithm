---
tag: 7VG548
kind: algorithm
slug: eppstein-galil-italiano-nissenzweig
name: Eppstein-Galil-Italiano-Nissenzweig algorithm
aliases:
- EGINN dynamic MST
area: graphs/dynamic-graphs
level: research
summary: Dynamic minimum spanning forest using sparsification.
solves: [dynamic-minimum-spanning-tree]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n^(1/2))}
  space: {extra: O(m)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [sparsification, minimum-spanning-tree, kruskal]
see_also: [frederickson-topology-trees, holm-de-lichtenberg-thorup, dynamic-minimum-spanning-tree, worst-case-update-time, link-cut-tree, dynamic-connectivity, nagamochi-ibaraki-certificate, global-rebuilding]
sources:
  - paper: doi:10.1145/265910.265914
    title: David Eppstein, Zvi Galil, Giuseppe F. Italiano and Amnon Nissenzweig, Sparsification, a technique for speeding up dynamic graph algorithms, Journal of the ACM 44(5), 669 to 696 (1997)
    locator: Section 2 (the sparsification tree and its analysis) and Section 3 (minimum spanning forests in O(n^(1/2)) worst-case time per update)
  - paper: doi:10.1137/0214055
    title: Greg N. Frederickson, Data structures for on-line updating of minimum spanning trees, with applications, SIAM Journal on Computing 14(4), 781 to 798 (1985)
    locator: the main result (O(m^(1/2)) worst-case time per update with topology trees), used at each node of the sparsification tree
  - paper: doi:10.1145/502090.502095
    title: Jacob Holm, Kristian de Lichtenberg and Mikkel Thorup, Poly-logarithmic deterministic fully-dynamic algorithms for connectivity, minimum spanning tree, 2-edge, and biconnectivity, Journal of the ACM 48(4), 723 to 760 (2001)
    locator: Section 1 (the earlier O(n^(1/2)) worst-case bound and the new O(log^4 n) amortized bound for minimum spanning forests)
---

The Eppstein-Galil-Italiano-Nissenzweig algorithm keeps the [minimum spanning forest](/minimum-spanning-tree/) of a graph under edge insertions and deletions in $O(n^{1/2})$ worst-case time per update, deterministically. It applies [sparsification](/sparsification/): the edges are split into groups of $n$ edges at the leaves of a balanced tree, and each node keeps the minimum spanning forest of the forests of its two children, so every node graph has fewer than $2n$ edges. An update changes at most two groups and the forests on their paths to the root, and each node runs Frederickson's $O(m^{1/2})$ structure on its $O(n)$ edges. The result, published in 1997 after a 1992 conference version, improved Frederickson's $O(m^{1/2})$ bound and was the best worst-case deterministic bound for many years.

## In plain words

The cheapest way to connect all the points of a network keeps fewer links than there are points, even if the network has a huge number of links. This method uses that fact again and again.

Cut the list of links into piles of at most $n$ links, one pile per leaf of a tree. At each node of the tree, keep the cheapest connecting set of the links that its two children keep. Each child keeps fewer than $n$ links, so every node works on fewer than $2n$ links.

The top node then keeps the cheapest connecting set of the whole network. When a link is added or removed, only its pile changes, so only the nodes on the way from that pile to the top need new answers.

## The problem

The input is a graph on $n$ vertices with real edge weights, and a sequence of operations: insert an edge with a weight, delete an edge, and report the minimum spanning forest (or its weight). After each operation the algorithm must report the forest of the current graph. This is the fully dynamic form of the [dynamic minimum spanning tree](/dynamic-minimum-spanning-tree/) problem. Ties between equal weights are broken by a fixed order of the edges, such as the order of insertion, so the forest is unique.

## The algorithm

The **sparsification tree** has the groups $E_1, \ldots, E_g$ at its leaves, each of at most $n$ edges, and all groups but the last one are full. For a node $x$, let $F(x)$ be its stored forest: at a leaf, the minimum spanning forest of its group; at an internal node, the minimum spanning forest of $F(\mathrm{left}(x)) \cup F(\mathrm{right}(x))$.

```pseudo id=main
INSERT(e)
L1  add e to the last group, or to a new group if the last one is full
L2  RECOMPUTE-PATH(the leaf of that group)

DELETE(e)
L3  remove e from its group E_i
L4  move one edge of the last group into E_i; drop the last group if it is empty
L5  RECOMPUTE-PATH(E_i); RECOMPUTE-PATH(the last group)

RECOMPUTE-PATH(leaf)
L6  for each node x on the path from the leaf to the root:
L7      F(x) ← the minimum spanning forest of F(left(x)) ∪ F(right(x))   ▷ at a leaf: of its group
REPORT
L8  return F(root)
```

Line L4 keeps every group but the last full, so the number of groups is $\lceil m/n \rceil$ and the tree has depth $O(\log(m/n))$. Line L7 is the work of each node. With [Kruskal's algorithm](/kruskal/) it costs $O(n \log n)$. In the paper, each node instead keeps a dynamic minimum spanning forest structure of Frederickson on its own graph. The certificate is **stable**: one edge change in a child's forest changes the parent's forest by at most one inserted and one deleted edge, so each node receives $O(1)$ edge changes per update and passes $O(1)$ changes up.

The implementation recomputes each node by Kruskal's algorithm and rebuilds the tree when the number of groups passes a power of two.

## Example

Take $K_4$ with the weights $w(01) = 1$, $w(12) = 2$, $w(23) = 3$, $w(03) = 4$, $w(02) = 5$, $w(13) = 6$, inserted in the order 01, 02, 03, 12, 13, 23, so $n = 4$ gives the groups $E_1 = \{01, 02, 03, 12\}$ and $E_2 = \{13, 23\}$.

| step | $E_1$ | $E_2$ | $F(E_1)$ | $F(E_2)$ | $F(\text{root})$ | weight |
|---|---|---|---|---|---|---|
| after the inserts | 01, 02, 03, 12 | 13, 23 | 01, 12, 03 | 23, 13 | 01, 12, 23 | 6 |
| delete 12 | 01, 02, 03, 23 | 13 | 01, 23, 03 | 13 | 01, 23, 03 | 8 |

In the first row, the forest of $E_1$ drops 02, which is the heaviest edge on the cycle 0, 1, 2. The root sees $\{01, 12, 03, 23, 13\}$ and keeps 01, 12, 23: then 03 closes the cycle 0, 1, 2, 3 and 13 closes the cycle 1, 2, 3. Deleting 12 empties a place in $E_1$, so line L4 moves 23 from the last group into it. The root then keeps 01, 23, 03 with weight 8, which is the minimum spanning forest of $K_4$ without the edge 12. The edge 02 is never kept above the leaf, because 0 and 2 are joined by cheaper paths in every node.

## Correctness

The key fact is that a minimum spanning forest is a strong certificate. Let $\mathrm{MSF}(G)$ be the unique minimum spanning forest with ties broken by the fixed order. By the cycle rule, an edge outside $\mathrm{MSF}(G)$ is the heaviest edge of some cycle of $G$, so it is also outside the minimum spanning forest of any graph that contains $G$. Hence $\mathrm{MSF}(G_1 \cup G_2) = \mathrm{MSF}(\mathrm{MSF}(G_1) \cup \mathrm{MSF}(G_2))$. By induction up the tree, $F(x)$ is the minimum spanning forest of all edges in the groups below $x$, and $F(\text{root})$ is $\mathrm{MSF}(G)$. Every operation recomputes exactly the nodes whose groups below them changed. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Node size.** Each forest has at most $n - 1$ edges, so every node graph has at most $2n - 2$ edges, and every leaf at most $n$.
- **With Kruskal at each node.** Line L7 costs $O(n \log n)$, and an update recomputes two paths of $O(\log(m/n))$ nodes, so an update takes $O(n \log n \log(m/n))$ time in the worst case. This is the version of the implementation; it is already faster than recomputing from scratch when $m$ is much larger than $n$.
- **With Frederickson's structure at each node.** Each node graph has $O(n)$ edges, so each of its updates takes $O(n^{1/2})$ worst-case time, and by stability each node does $O(1)$ of them per update. The simple tree gives $O(n^{1/2} \log(m/n))$. The paper removes the $\log(m/n)$ factor with groups whose sizes shrink geometrically toward the root, which gives $O(n^{1/2})$ worst-case time per update.
- **Space.** $O(m)$ for the groups, plus $O(n)$ per internal node, which is $O(m)$ in total since there are $O(m/n)$ nodes.
- **Kind of bound.** Worst case per update and deterministic, apart from rebuilding when $m$ doubles or halves, which [global rebuilding](/global-rebuilding/) spreads over later updates.

## Properties

- **Fully dynamic.** Insertions and deletions in any order.
- **Worst case.** The bound holds for every single update, unlike the amortized bound of the [Holm-de Lichtenberg-Thorup algorithm](/holm-de-lichtenberg-thorup/).
- **Deterministic.**
- **Black box.** The node algorithm can be replaced: any dynamic minimum spanning forest algorithm with update time $f(m)$ becomes one with time about $f(O(n))$.

## Variants and improvements

- **Other properties.** The same tree with other strong certificates gives $O(n^{1/2})$ worst-case time per update for connectivity, 2-edge connectivity and bipartiteness, and bounds for higher connectivity; see [sparsification](/sparsification/).
- **Amortized polylogarithmic.** Holm, de Lichtenberg and Thorup (2001) gave $O(\log^4 n)$ amortized time per update for minimum spanning forests, deterministically, and later work lowered this bound.
- **Insertions only.** With insertions only, a [link-cut tree](/link-cut-tree/) gives $O(\log n)$ amortized time: a new edge that closes a cycle replaces the heaviest edge of that cycle if it is lighter.
- **Worst-case subpolynomial.** Later randomized algorithms improved the worst-case bound below $n^{1/2}$, to $n^{o(1)}$ per update.

## When to use it

Use it when every update needs a guaranteed time bound and the graph is dense, so that $n^{1/2}$ is much smaller than $m^{1/2}$. In practice the simple form with a static algorithm at each node is often the best choice, because it is easy to write and its cost depends on $n$, not on $m$. When amortized bounds are acceptable, the polylogarithmic algorithms are faster on large graphs.

## Pitfalls

- **Ties.** With equal weights and no fixed tie order, two nodes can choose different forests, and a single update can change many edges of a node forest. This breaks stability and the time bound. Break ties by edge id.
- **Groups that are not full.** If deletions leave many groups half empty, the tree has more nodes than $\lceil m/n \rceil$ and the depth grows. Line L4 keeps all groups but the last full.
- **Moving an edge changes two leaves.** After line L4, both the group that lost the deleted edge and the last group changed; recompute both paths.
- **Too small graphs.** For $m \le n$ there is one group, and the method is the same as running the node algorithm on the whole graph.

## Implementations

## History

Frederickson (1985) gave the first sublinear fully dynamic minimum spanning tree algorithm, with $O(m^{1/2})$ worst-case time per update, using topology trees. Eppstein, Galil, Italiano and Nissenzweig presented sparsification at FOCS 1992 and published the full paper in the Journal of the ACM in 1997, lowering the bound to $O(n^{1/2})$ and giving many other results with the same technique. Holm, de Lichtenberg and Thorup (2001) reached polylogarithmic amortized bounds. For worst-case time, $O(n^{1/2})$ remained the best deterministic bound for about two decades.

## References
