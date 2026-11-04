---
tag: 8PZPPQ
kind: data-structure
slug: priority-r-tree
name: Priority R-tree
aliases:
- PR-tree
area: data-structures/spatial-structures
level: research
summary: R-tree variant with worst-case query guarantees built by placing extreme-coordinate objects in priority nodes.
implements: [spatial-index]
model: external-memory-model
complexity:
  vars: {N: the number of rectangles, B: the most entries in a node (one disk block), T: the number of reported rectangles, M: the number of rectangles that fit in memory}
  time: {search: "O(sqrt(N/B) + T/B)", build: "O((N/B) log(N/B) / log(M/B))"}
  space: {total: O(N/B)}
history:
  year: 2004
  people: [Lars Arge, Mark de Berg, Herman J. Haverkort, Ke Yi]
  note: Arge, de Berg, Haverkort and Yi introduced the priority R-tree at ACM SIGMOD 2004, the first R-tree whose window queries are optimal in the worst case.
prereqs: [r-tree, kd-tree, bulk-loading]
see_also: [r-tree, str-packing, hilbert-r-tree, r-star-tree, kd-tree, bulk-loading, external-memory-model, orthogonal-range-searching]
sources:
  - paper: doi:10.1145/1007568.1007608
    title: Lars Arge, Mark de Berg, Herman J. Haverkort and Ke Yi, The priority R-tree, a practically efficient and worst-case optimal R-tree, Proceedings of ACM SIGMOD 2004, pp. 347 to 358
    locator: the pseudo-PR-tree with its four priority leaves and four-dimensional k-d split, the bottom-up construction of the PR-tree, the query bound of O(sqrt(N/B) + T/B) I/Os with its lower bound for any R-tree, the LPR-tree, and the experiments
  - paper: doi:10.1145/280277.280279
    title: Volker Gaede and Oliver Günther, Multidimensional access methods, ACM Computing Surveys 30(2), 1998, pp. 170 to 231
    locator: Section 5, the R-tree family and the transformation of rectangles into points of twice the dimension
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 2, Object-Based and Image-Based Image Representations, the section on the R-tree and its bulk loading
---

The priority R-tree, or PR-tree, is a static [R-tree](/r-tree/) built by a rule that gives a guarantee for every window query: with $N$ rectangles and nodes of $B$ entries, a query that reports $T$ rectangles reads $O(\sqrt{N/B} + T/B)$ nodes, and no R-tree can do better in the worst case. Other packed R-trees, such as [STR](/str-packing/) and the [Hilbert R-tree](/hilbert-r-tree/), are fast on usual data, but some inputs make them read almost all nodes for a query that reports nothing. The PR-tree sees each rectangle as a point in four dimensions, and groups the rectangles with the most extreme sides into *priority leaves* before it splits the rest as a [k-d tree](/kd-tree/) does. Arge, de Berg, Haverkort and Yi introduced it in 2004.

## In plain words

An R-tree packs boxes into bags and bags into bigger bags. A search opens every bag whose frame touches the question. If the boxes are long and thin, a bad packing gives bags whose frames are large and empty, and a search opens many bags and finds nothing in them.

The PR-tree fills its bags in a careful order. For each group of boxes, it first makes four special bags: one with the boxes that reach farthest to the left, one with those that reach farthest down, one with those that reach farthest to the right, and one with those that reach farthest up. Only then does it cut the other boxes into two halves and repeat. This makes sure that a search that opens a bag usually gets something from it. It then packs the bags into bigger bags by the same rule.

## The abstract type

The PR-tree implements a static [spatial index](/spatial-index/): it is built once from a set of rectangles, and then answers `search(q)`, which reports every stored rectangle that meets the window $q$. Insertions and deletions are possible in the dynamic variant, the LPR-tree.

## Representation

The PR-tree is an R-tree: each node holds at most $B$ entries, each a rectangle and a pointer, the rectangle of an internal entry is the [MBR](/minimum-bounding-rectangle/) of its child, and every leaf is at the same depth. The difference is only in how the rectangles are grouped into leaves, and the leaves into nodes.

**Rectangles as points.** A rectangle $[x_1, x_2] \times [y_1, y_2]$ is the point $(x_1, y_1, x_2, y_2)$ in four dimensions. A rectangle meets $q = [a_1, a_2] \times [b_1, b_2]$ if and only if $x_1 \le a_2$, $y_1 \le b_2$, $x_2 \ge a_1$ and $y_2 \ge b_1$, so the answer to a query is the set of points in an *orthant*, the product of four half lines.

**Pseudo-PR-tree.** On a set $S$ of rectangles, a pseudo-PR-tree is a tree whose leaves are groups of at most $B$ rectangles:

- if $|S| \le B$, one leaf holds $S$;
- otherwise, four *priority leaves* take out, in turn, the $B$ rectangles of $S$ with the smallest $x_1$, then of those left the $B$ with the smallest $y_1$, the $B$ with the largest $x_2$, and the $B$ with the largest $y_2$;
- the rectangles left are split in two halves at the median of one coordinate, which cycles through $x_1, y_1, x_2, y_2$ with the depth, as in a four-dimensional k-d tree, and each half gets its own pseudo-PR-tree.

So an internal node of the pseudo-PR-tree has up to six children: four priority leaves and two subtrees. It is not an R-tree, since its leaves are at different depths.

**PR-tree.** The leaves of a pseudo-PR-tree on the data are the leaves of the PR-tree. To make the next level, take the MBRs of the nodes of the current level, build a pseudo-PR-tree on them, and make each of its leaves a node whose children are the nodes in that leaf. Repeat until one node is left, the root.

## Operations

```pseudo id=main
PSEUDO-PR-LEAVES(S, B, depth)
L1  if |S| ≤ B then return [S]
L2  for key in (smallest x1, smallest y1, largest x2, largest y2):
L3      take the B rectangles of S best by key out of S, and make them a leaf
L4  axis ← depth mod 4; sort what is left of S by that coordinate
L5  return the four leaves, then PSEUDO-PR-LEAVES of each half with depth + 1
BUILD(S, B)
L6  level ← one node for each group of PSEUDO-PR-LEAVES(S, B, 0)
L7  while level has more than one node:
L8      level ← one node for each group of PSEUDO-PR-LEAVES({(MBR(u), u) : u in level}, B, 0)
SEARCH(u, q)
L9  for each entry (r, x) of u:
L10     if r meets q then if u is a leaf, report x
L11         else SEARCH(x, q)
```

**Search.** The search is the R-tree search: go into each child whose box meets the window. The guarantee comes from the shape of the tree, not from the search.

**Why priority leaves help.** Consider a node of the pseudo-PR-tree and its priority leaf of smallest $x_1$. A query reaches this leaf when the box of the leaf meets $q$. The leaf holds the $B$ rectangles of the subtree that reach farthest left. If the query meets the subtree at all but the leaf gives fewer than $B$ answers, the query must have its boundary in a special place in the four-dimensional space. The paper shows that the nodes where this happens are those of the k-d tree whose region meets a two-dimensional face of the orthant, and a k-d tree in four dimensions with $N/B$ leaves has $O(\sqrt{N/B})$ such nodes. Every other visited leaf reports $B$ rectangles, which costs $O(T/B)$ in all.

**Updates.** The PR-tree is static. The LPR-tree of the same paper keeps a few PR-trees of growing sizes and rebuilds them by the logarithmic method, which keeps the query bound and allows insertions and deletions.

## Example

Take $B = 3$ and 16 unit squares $[x, x+1] \times [y, y+1]$, with lower left corners A $(1, 1)$, B $(2, 9)$, C $(3, 4)$, D $(4, 7)$, E $(5, 2)$, F $(6, 6)$, G $(7, 10)$, H $(8, 3)$, I $(9, 8)$, J $(10, 1)$, K $(11, 5)$, L $(12, 9)$, M $(13, 3)$, N $(14, 7)$, O $(15, 1)$ and P $(16, 6)$.

**Level 0.** The pseudo-PR-tree on the 16 squares makes these leaves. Ties go to the square with the smaller corner.

| leaf | rule | squares | box |
|---|---|---|---|
| 1 | smallest $x_1$ | A, B, C | $[1, 4] \times [1, 10]$ |
| 2 | smallest $y_1$ of the rest | J, O, E | $[5, 16] \times [1, 3]$ |
| 3 | largest $x_2$ of the rest | P, N, M | $[13, 17] \times [3, 8]$ |
| 4 | largest $y_2$ of the rest | G, L, I | $[7, 13] \times [8, 11]$ |
| 5 | k-d split on $x_1$, left half | D, F | $[4, 7] \times [6, 8]$ |
| 6 | k-d split on $x_1$, right half | H, K | $[8, 12] \times [3, 6]$ |

After the four priority leaves, D, F, H and K are left; they are split at the median of $x_1$, and each half has at most 3 squares, so it is a leaf.

**Level 1.** The six leaf boxes are the input of a new pseudo-PR-tree. The 3 with the smallest $x_1$ are leaves 1, 5 and 2 (with $x_1$ = 1, 4, 5); the 3 left, leaves 6, 3 and 4, make the next priority leaf. So level 1 has two nodes: $\{1, 5, 2\}$ with box $[1, 16] \times [1, 10]$, and $\{6, 3, 4\}$ with box $[7, 17] \times [3, 11]$. **Level 2** is the root over these two. The height is 2.

**Search.** SEARCH($[5, 10] \times [5, 9]$): the root meets both children. In the first, leaf 5 meets $q$ and reports D (it touches $x = 5$) and F; leaf 1 ends at $x = 4$ and leaf 2 at $y = 3$, so they are skipped. In the second, leaf 6 meets $q$ but reports nothing (H and K lie outside), leaf 4 reports I, and leaf 3 starts at $x = 13$ and is skipped. The answer is D, F, I, after reading 6 nodes.

## Correctness

Every rectangle is in exactly one leaf: PSEUDO-PR-LEAVES takes each rectangle out of $S$ once, into a priority leaf, or passes it to exactly one half, and the recursion stops at sets of at most $B$. Each leaf has at most $B$ entries, by the same rule. Each level of BUILD groups the nodes of the level below into nodes of at most $B$ entries, each node of the level below in one group, so all leaves are at the same depth. The rectangle of each entry is the MBR of its child by construction, which is the R-tree invariant, and the R-tree search is correct on any tree with this invariant. BUILD stops: when a level has $L \ge 2$ nodes, the next level has fewer. If $L \le B$ there is one group. Otherwise the first priority leaf holds $B \ge 2$ nodes and every group holds at least one, so there are at most $L - B + 1 < L$ groups. The full proof is in the proofs folder.

## Complexity

The model is the [external memory model](/external-memory-model/): a node is a block of $B$ entries, and memory holds $M$ rectangles.

- **Search.** $O(\sqrt{N/B} + T/B)$ I/Os in the worst case, by the argument above. In $d$ dimensions the bound is $O((N/B)^{1 - 1/d} + T/B)$, with $2d$ priority leaves and a k-d split in $2d$ dimensions.
- **Lower bound.** The paper shows that for any R-tree on some inputs of $N$ rectangles (even points), some window query that reports nothing visits $\Omega(\sqrt{N/B})$ nodes. So the PR-tree is optimal among R-trees. Data structures that are not R-trees, such as the external range trees, can do better for points.
- **Build.** $O(\frac{N}{B} \log_{M/B} \frac{N}{B})$ I/Os, the cost of sorting, with the construction of the paper that builds several levels of the k-d split at once in memory. The simple code here sorts at each node, which costs $O(N \log^2 N)$ time in memory.
- **Space.** $O(N/B)$ nodes. The tree is nearly full: the only nodes that are not full are at the bottom of the recursion of each pseudo-PR-tree.

| operation | cost | case |
|---|---|---|
| search | $O(\sqrt{N/B} + T/B)$ | worst |
| search, $d$ dimensions | $O((N/B)^{1-1/d} + T/B)$ | worst |
| build | $O(\frac{N}{B} \log_{M/B} \frac{N}{B})$ | worst |
| space | $O(N/B)$ | total |

## Variants

- **Pseudo-PR-tree alone.** The pseudo-PR-tree is not balanced, but it already answers queries in $O(\sqrt{N/B} + T/B)$; the PR-tree turns it into an R-tree with leaves at one depth, so it fits the code of any R-tree system.
- **LPR-tree.** The logarithmic PR-tree supports insertions and deletions by keeping $O(\log N)$ PR-trees and rebuilding them as in the logarithmic method, with the same query bound.
- **Higher dimensions.** $2d$ priority leaves and a k-d tree in $2d$ dimensions give the bound $O((N/B)^{1 - 1/d} + T/B)$.
- **Packed trees by a sort order.** [STR packing](/str-packing/) and [Hilbert packing](/hilbert-r-tree/) sort the rectangles by a key and fill nodes in that order. They are simpler and often a little faster on usual data, but they have no worst-case bound.

## When to use it

Use the PR-tree to bulk load an R-tree when the data may be extreme: long thin rectangles, rectangles of very different sizes, or rectangles that cluster in a way that makes the boxes of a packed tree large. In the experiments of the paper it was about as fast as the packed Hilbert R-tree on real map data, and much faster on such extreme data. If the data changes often and in small steps, use the LPR-tree or a dynamic tree such as the [R*-tree](/r-star-tree/), at the cost of the guarantee.

## Pitfalls

- **Order of the priority leaves.** The four leaves are taken in turn from what is left, not each from the whole set; otherwise one rectangle can be in two leaves.
- **Ties.** Many rectangles with the same coordinate make the median split and the priority choices depend on the order. Break ties by a fixed rule, such as the whole rectangle, so that the build is the same every time.
- **Point data.** For points, $x_1 = x_2$ and $y_1 = y_2$, so the four-dimensional points lie on a plane. The structure still works, but a [k-d tree](/kd-tree/) or a [range tree](/range-tree/) on the points may be simpler.
- **Not a dynamic tree.** Inserting into a PR-tree with the R-tree insert rules loses the guarantee. Rebuild, or use the LPR-tree.

## Implementations

## History

The R-tree had no good worst-case bound for window queries, and packed R-trees, which were the best in practice, could be made to read almost all their nodes for empty queries. Earlier work, by Kanth and Singh on lower bounds for index structures that store each object once, and by Agarwal, de Berg, Gudmundsson, Hammar and Haverkort on box-trees and R-trees with near-optimal query time, had studied bounds of this kind. Arge, de Berg, Haverkort and Yi gave in 2004 the first R-tree with this bound for rectangles, the PR-tree, and showed in experiments that it was also practical. A journal version appeared in ACM Transactions on Algorithms in 2008.

## References
