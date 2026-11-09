---
tag: GR1N56
kind: concept
slug: decomposable-searching-problem
name: Decomposable searching problem
aliases:
- decomposable search problem
- Bentley decomposability
- logarithmic method
- Bentley-Saxe method
- static-to-dynamic transformation
area: geometry/range-searching
level: advanced
summary: Search problem whose answer on a union of disjoint sets can be combined from the answers on each part, enabling dynamization.
prereqs: [binary-counter-increment, amortized-cost, orthogonal-range-searching]
see_also: [dynamic-range-searching, global-rebuilding, lazy-rebuilding, log-structured-merge-tree, binary-counter-increment, kd-tree, nearest-neighbor-search, orthogonal-range-counting]
sources:
  - paper: doi:10.1016/0020-0190(79)90117-0
    title: Jon Louis Bentley, Decomposable searching problems, Information Processing Letters 8(5), 1979, pages 244 to 251
    locator: the definition of decomposability and the binary transformation (DOI to be checked)
  - paper: doi:10.1016/0196-6774(80)90015-2
    title: Jon Louis Bentley and James B. Saxe, Decomposable searching problems I. Static-to-dynamic transformation, Journal of Algorithms 1(4), 1980, pages 301 to 358
    locator: the logarithmic method, its amortized analysis and the trade-offs between query and insertion time
  - book: isbn:9783540123309
    title: Mark H. Overmars, The Design of Dynamic Data Structures, Lecture Notes in Computer Science 156, Springer, 1983
    locator: Chapter 5 (decomposable searching problems, weak deletions, amortized bounds) and Chapter 6 (worst case bounds)
  - paper: doi:10.1016/0020-0190(81)90093-4
    title: Mark H. Overmars and Jan van Leeuwen, Worst-case optimal insertion and deletion methods for decomposable searching problems, Information Processing Letters 12(4), 1981, pages 168 to 173
    locator: worst case insertion bounds by building the next block in the background (DOI to be checked)
  - book: isbn:9783540136422
    title: Kurt Mehlhorn, Data Structures and Algorithms 3, Multi-dimensional Searching and Computational Geometry, Springer, 1984
    locator: Chapter VII, Section 1, A general approach to dynamization
---

A searching problem is decomposable when its answer for a query $x$ on a union $A \cup B$ of disjoint sets can be computed in constant time from the answers on $A$ and on $B$. Range counting (add the counts), range reporting (concatenate the lists), range emptiness (take the or) and nearest neighbor search (take the closer point) are decomposable; membership in the convex hull is not. Bentley and Saxe showed that every decomposable problem with a static structure can be made dynamic by the logarithmic method: the set is split into blocks whose sizes are distinct powers of two, like the binary digits of $n$, and an insertion merges blocks as a binary counter carries. A static structure with build time $P(n)$ and query time $Q(n)$ then supports insertions in $O((P(n)/n) \log n)$ amortized time and queries in $O(Q(n) \log n)$ time.

## In plain words

Some questions about a set can be answered piece by piece. To count the points in a rectangle, one can split the points into groups, count in each group, and add up the counts. To find the closest point to a target, one can find the closest point in each group and keep the best. Questions with this property are called decomposable.

This makes it easy to handle a growing set. Keep the points in groups of sizes one, two, four, eight and so on, at most one group of each size. A new point forms a group of size one; if there already is one, the two are merged into a group of size two, and so on, like carrying in binary addition. Each group is a fixed structure, rebuilt only when merged. A question is asked of every group and the answers are combined.

## The idea

**Decomposability.** A searching problem assigns to a query $x$ and a finite set $A$ an answer $Q(x, A)$. It is **decomposable** if there is an operation $\square$, computable in $O(1)$ time, such that for all disjoint $A$ and $B$,

$$Q(x, A \cup B) = Q(x, A) \;\square\; Q(x, B).$$

For range counting $\square$ is $+$, for reporting it is the disjoint union, for emptiness it is the logical and of the two "empty" answers, and for nearest neighbor search it is the minimum by distance.

**The logarithmic method.** Write $n = \sum_i b_i 2^i$ in binary. Keep one static structure $D_i$ on a block of exactly $2^i$ elements for each $i$ with $b_i = 1$. Then:

- **Query.** Ask each of the at most $\lfloor \log_2 n \rfloor + 1$ blocks and combine with $\square$. The time is $\sum_i Q(2^i) = O(Q(n) \log n)$, and $O(Q(n))$ if $Q(n) = n^{\varepsilon}$ for a fixed $\varepsilon > 0$, because the terms then grow geometrically.
- **Insertion.** Find the smallest $j$ with $b_j = 0$. The new element and the blocks $D_0, \dots, D_{j-1}$ hold $1 + 1 + 2 + \dots + 2^{j-1} = 2^j$ elements; build $D_j$ on them from scratch and discard $D_0, \dots, D_{j-1}$.

**Analysis.** Assume $P(n)/n$ is nondecreasing. An element moves only to blocks of larger index, so it takes part in at most $\lfloor \log_2 n \rfloor + 1$ builds, and in a build of size $s \le n$ it is charged $P(s)/s \le P(n)/n$. Over $n$ insertions the total build time is $O(P(n) \log n)$, so each insertion costs $O((P(n)/n) \log n)$ amortized. When $P(n) = n^{1 + \varepsilon}$ the sum over the levels is geometric and the amortized cost is $O(P(n)/n)$. The space is $\sum_i S(2^i) = O(S(n))$ if $S(n)/n$ is nondecreasing. This mirrors the amortized analysis of the [binary counter](/binary-counter-increment/).

**Deletions.** If the static structure supports a weak deletion, which marks an element as gone without changing the shape of the structure, then deletions are handled by marking, and the whole structure is rebuilt once half of the elements are marked. Queries must ignore marked elements; for counting, a group weight or a count of marked elements in each canonical subset does this. With [global rebuilding](/global-rebuilding/) the bounds remain amortized; Overmars and van Leeuwen made insertions worst case by building each block gradually in the background while the old blocks are still in use.

**Trade-offs.** The base $2$ is a choice. With blocks of sizes that are powers of a larger base $b$, and up to $b - 1$ blocks per size, the query looks at $O(b \log_b n)$ blocks and an element is rebuilt $O(\log_b n)$ times. Bentley and Saxe give a family of such trade-offs, from $O(\log n)$ blocks down to $O(1)$ blocks at a cost of $n^{\varepsilon}$ per insertion.

## Examples

**Range counting with eleven points.** Insert, in order, the points $(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6), (3,2), (5,5), (8,4)$. After the eighth insertion the eight points form one block. Then $(3,2)$ forms a block of size $1$, $(5,5)$ merges with it into a block of size $2$, and $(8,4)$ forms a new block of size $1$. Now $n = 11 = 1011_2$ and the blocks are:

| block | points | count in $[3, 7] \times [2, 6]$ |
|---|---|---|
| $D_3$, size 8 | $(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)$ | 3: $(5,4), (6,6), (7,2)$ |
| $D_1$, size 2 | $(3,2), (5,5)$ | 2, with $(3,2)$ on a corner |
| $D_0$, size 1 | $(8,4)$ | 0 |

The answer is $3 + 2 + 0 = 5$. Inserting a twelfth point $(6,2)$ carries twice: it joins $D_0$ into a block of size $2$, which joins $D_1$ into a block $D_2$ of size $4$, holding $(3,2), (5,5), (8,4), (6,2)$. Now $12 = 1100_2$, the blocks are $D_3$ and $D_2$, and the same query gives $3 + 3 = 6$.

**Nearest neighbor.** For the query point $(7,3)$ and the three blocks above, the nearest points are $(7,2)$ in $D_3$ at squared distance $1$, $(5,5)$ in $D_1$ at squared distance $8$ and $(8,4)$ in $D_0$ at squared distance $2$; the minimum, $(7,2)$, is the nearest point overall.

**A problem that is not decomposable.** "Is $q$ inside the convex hull of the set?" For $A = \{(0,0), (2,0)\}$, $B = \{(0,2), (2,2)\}$ and $q = (1,1)$, the point $q$ is in the hull of $A \cup B$ but in neither hull of $A$ nor of $B$, so no combination of the two answers "no" can give "yes". Similarly the $k$-th smallest element is not decomposable, while the rank of a value is.

## Where it is used

- **[Dynamic range searching](/dynamic-range-searching/)**: kd-trees, partition trees and other static structures become dynamic with a logarithmic overhead.
- **[Nearest neighbor search](/nearest-neighbor-search/)** with insertions, from static Voronoi diagram structures.
- **[Log-structured merge trees](/log-structured-merge-tree/)** in databases follow the same pattern: sorted runs of geometrically growing sizes are merged in the background.
- **Halfspace and extreme point queries**: "the point of the set that is extreme in direction $u$" is decomposable, so static hull structures give insertion-only dynamic ones.
- **Offline algorithms** that process operations in time order, which split the timeline into blocks in the same binary way.

## References
