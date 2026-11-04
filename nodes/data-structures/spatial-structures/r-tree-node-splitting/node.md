---
tag: JVT7MB
kind: problem
slug: r-tree-node-splitting
name: R-tree node splitting
aliases:
- overflow node split
area: data-structures/spatial-structures
level: advanced
summary: Divide the entries of an overflowing R-tree node into two groups with small bounding boxes.
prereqs: [r-tree, minimum-bounding-rectangle]
see_also: [quadratic-split, r-star-tree, r-tree, overlap-and-dead-space, x-tree, str-packing, partition-problem, bulk-loading]
sources:
  - paper: doi:10.1145/602259.602266
    title: Antonin Guttman, R-trees, a dynamic index structure for spatial searching, Proceedings of ACM SIGMOD 1984, pp. 47 to 57
    locator: Section 3.5 (the node splitting problem with the total area as the measure, and the exhaustive, quadratic and linear algorithms)
  - paper: doi:10.1145/93597.98741
    title: Norbert Beckmann, Hans-Peter Kriegel, Ralf Schneider and Bernhard Seeger, The R*-tree, an efficient and robust access method for points and rectangles, Proceedings of ACM SIGMOD 1990
    locator: Section 2 (the criteria of area, margin, overlap and storage use) and Section 4.2 (the split by sorted distributions, ChooseSplitAxis and ChooseSplitIndex)
  - paper: "Yván J. García, Mario A. López and Scott T. Leutenegger, On optimal node splitting for R-trees, Proceedings of the 24th International Conference on Very Large Data Bases (VLDB), 1998, pp. 334 to 344"
    title: García, López and Leutenegger, On optimal node splitting for R-trees, VLDB 1998
    locator: the exact polynomial-time split algorithm and the experiments that compare optimal splits with the heuristics
  - paper: "Chuan-Heng Ang and T. C. Tan, New linear node splitting algorithm for R-trees, Advances in Spatial Databases (SSD 1997), Lecture Notes in Computer Science 1262, pp. 339 to 349"
    title: Ang and Tan, New linear node splitting algorithm for R-trees, SSD 1997
    locator: the split that assigns each entry to the side of the node it is closer to, along each axis
  - url: https://www.cse.cuhk.edu.hk/~taoyf/course/wst501/notes/lec13.pdf
    title: Yufei Tao, Lecture notes on R-trees, Chinese University of Hong Kong
    locator: the section on node splitting (the problem with the sum of perimeters, the O(B^4) exact method from the four coordinates of each box, and the faster method attributed to García and others)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 2, Object-Based and Image-Based Image Representations, the section on the R-tree and its node splitting methods
---

R-tree node splitting is the problem that an [R-tree](/r-tree/) must solve each time a node overflows: divide its $M + 1$ entries, each a rectangle, into two groups of at least $m$ entries so that the two bounding rectangles are good for later queries. "Good" is a cost function, usually the total area of the two boxes, their total margin, or the area they share. The split decides the shape of the tree, so it is the main difference between R-tree variants. The exact problem can be solved in polynomial time for a fixed dimension, but the exact methods are slow for the node sizes used on disk, and practical trees use heuristics such as the [quadratic split](/quadratic-split/) of Guttman or the sorted split of the [R*-tree](/r-star-tree/).

## In plain words

A bag holds one box too many and must become two bags. Each new bag must hold at least a fixed number of boxes. Each bag is as big as the smallest frame around its boxes.

Queries open a bag when the question touches its frame. So you want frames that are small, that do not cover each other much, and that are not long and thin. The problem is to choose which boxes go into which bag to make the frames good in that sense.

There are many ways to divide the boxes, about $2^{M}$ of them, so trying all of them is too slow for a bag of 50 boxes.

## Definition

**Input.** Rectangles $E_1, \ldots, E_n$ in $\mathbb{R}^d$, with $n \ge 2$ (in a tree, $n = M + 1$), and a minimum fill $m$ with $1 \le m \le n/2$.

**Output.** A partition $\{1, \ldots, n\} = G_1 \cup G_2$ with $G_1 \cap G_2 = \emptyset$ and $|G_1|, |G_2| \ge m$.

**Goal.** Minimize a cost $c(B_1, B_2)$ of the two boxes $B_k = \operatorname{MBR}(\{E_i : i \in G_k\})$. The usual costs are

- the *area sum* $\operatorname{vol}(B_1) + \operatorname{vol}(B_2)$, used by Guttman;
- the *margin sum* $\operatorname{margin}(B_1) + \operatorname{margin}(B_2)$, where the margin of a box is the sum of its side lengths, which favors boxes close to squares;
- the *overlap* $\operatorname{vol}(B_1 \cap B_2)$, which counts the area where a point query must follow both nodes;
- weighted mixes of these, or the [dead space](/overlap-and-dead-space/) of the two nodes.

The cost depends only on the two boxes, and each box is the MBR of its group. The number of feasible partitions is $\frac{1}{2}\sum_{k=m}^{n-m} \binom{n}{k}$, which is $2^{n-1} - n - 1$ for $m = 2$.

## Variants

- **Cost function.** As listed above. The R*-tree uses two at once: it chooses the axis by the margin sum, and then the split on that axis by the overlap, with the area sum to break ties.
- **Minimum fill.** With $m = 1$ the problem is easier, and the best split often puts one entry alone. Real trees use $m$ near $0.4 M$, which forbids such splits.
- **Points.** If all entries are points, the boxes are the MBRs of two point sets. This is the case at the leaf level of a point index.
- **Restricted splits.** Allow only *sorted* splits: sort the entries along an axis by a side, and cut the sorted list at a position between $m$ and $n - m$. The R*-tree searches only these, $O(d n)$ candidates.
- **Splits into more groups.** Divide the entries into $k \ge 3$ groups, as in a split that also uses a sibling node. Taken to the whole data set, this is the problem of [bulk loading](/bulk-loading/): partition $n$ rectangles into groups of $M$ with small boxes.
- **Refusing to split.** The [X-tree](/x-tree/) treats the split as optional: if every split has much overlap, it keeps one larger node, a supernode.

## Examples

**Five rectangles with $m = 2$.** Take a $= [0, 2] \times [0, 2]$, b $= [1, 3] \times [5, 7]$, c $= [6, 8] \times [0, 1]$, d $= [7, 9] \times [6, 9]$ and e $= [2, 3] \times [1, 3]$. There are 10 feasible splits, all of sizes 2 and 3. The three best by the area sum are

| group of 2 | group of 3 | boxes | area sum | margin sum | overlap |
|---|---|---|---|---|---|
| c, d | a, b, e | $[6, 9] \times [0, 9]$ and $[0, 3] \times [0, 7]$ | 48 | 44 | 0 |
| b, d | a, c, e | $[1, 9] \times [5, 9]$ and $[0, 8] \times [0, 3]$ | 56 | 46 | 0 |
| a, c | b, d, e | $[0, 8] \times [0, 2]$ and $[1, 9] \times [1, 9]$ | 80 | 52 | 7 |

The split $\{c, d\}$, $\{a, b, e\}$ is the best by all three measures, and the [quadratic split](/quadratic-split/) finds it. The worst splits, $\{a, d\}$ with $\{b, c, e\}$ and $\{b, c\}$ with $\{a, d, e\}$, have area sum 130 and an overlap of 49, since one of their boxes is the whole $[0, 9] \times [0, 9]$.

**The measures can disagree.** For long thin rectangles that cross, the split with the least area sum can have long thin boxes with a large margin, while another split has boxes closer to squares and a larger area. This is the reason the R*-tree uses the margin to choose the axis and the overlap to choose the cut.

**A heuristic that misses.** For A $= [4, 6] \times [0, 1]$, B $= [7, 8] \times [7, 9]$, C $= [0, 3] \times [4, 6]$ and D $= [1, 2] \times [5, 6]$ with $m = 2$, the quadratic split returns area sum 64, while the best split, $\{A, B\}$ and $\{C, D\}$, has area sum 42. See the [quadratic split](/quadratic-split/) for the steps.

## Known algorithms

| algorithm | time | result |
|---|---|---|
| exhaustive search | $O(d n 2^n)$ | exact for any cost |
| enumeration of boxes (below) | $O(d n^{2d+1})$ | exact for any symmetric monotone cost, with $m = 1$ |
| García, López and Leutenegger | polynomial in $n$ for fixed $d$ | exact |
| [quadratic split](/quadratic-split/) (Guttman) | $O(d n^2)$ | heuristic, area sum |
| linear split (Guttman) | $O(d n)$ | heuristic, area sum |
| linear split of Ang and Tan | $O(d n)$ | heuristic, balance and overlap |
| [R*-tree](/r-star-tree/) split | $O(d n \log n)$ | exact over sorted splits, by margin then overlap |

Guttman's tests found the linear split almost as good as the quadratic one; later tests, and the R*-tree paper, found the sorted split of the R*-tree clearly better than both. García, López and Leutenegger found that the exact split gives better nodes, but that the gain in query time over a good heuristic is small, while the cost of the split is large. The lecture notes of Tao give, for the margin sum with points, an exact method in $O(n^4)$ time in the plane from the four coordinates that fix each box, and a faster one in $O(n^2)$.

## Bounds

**Input size.** Every algorithm must read the $n$ rectangles, so $\Omega(d n)$ time is needed.

**A polynomial exact method for $m = 1$.** Let the cost be *symmetric* in the two boxes and *monotone*: it does not increase when a box shrinks, as holds for the area sum, the margin sum and the overlap. Take an optimal split $(G_1, G_2)$ with boxes $B_1, B_2$. Each side of $B_1$ lies on a side of an input rectangle, so $B_1$ is fixed by $2d$ coordinates of the input, and there are at most $n^{2d}$ candidates for it. Let $C$ be the set of the entries of $G_2$ that lie inside $B_1$.

- If $C \ne G_2$, move the entries of $C$ to $G_1$. The box $B_1$ does not change, and $B_2$ can only shrink, so the cost does not increase, and both groups are still non-empty. So some optimal split has $G_1 = \{i : E_i \subseteq B_1\}$.
- If $C = G_2$, then every entry lies inside $B_1$. Take any $r \in G_2$ and the split $\{r\}$ against all other entries. Its first box is $E_r \subseteq B_2$ and its second box lies inside $B_1$, so its cost is not larger. So some optimal split has a group of one entry.

So it is enough to try each of the $O(n^{2d})$ candidate boxes $B$, with $G_1$ the entries inside $B$ and $G_2$ the others when both are non-empty, and the $n$ splits with one entry alone. Each costs $O(d n)$ to evaluate, for $O(d n^{2d+1})$ in total. This is polynomial for fixed $d$, but $O(n^5)$ in the plane is far too slow for $n = 50$ at every split; the exact algorithm of García and others is faster. The argument does not apply directly to $m \ge 2$, where moving entries can break the fill of $G_2$.

**Heuristics.** The sources give no bound on the ratio between the cost of a heuristic split and the optimal cost. The example above shows a ratio of $64/42 > 1.5$ for the quadratic split on four rectangles.

## Reductions

- **From a split to a two-cluster problem.** For points and the area or margin sum, the split is a clustering of $n$ points into two clusters with a cost on their bounding boxes, a geometric relative of the [partition problem](/partition-problem/).
- **Sorted splits as a reduction to sorting.** Restricting to sorted splits reduces the search to $d$ sorts and $O(d n)$ prefix and suffix boxes, which is the method of the R*-tree.
- **Bulk loading.** Repeating the split from the top on the whole data, or packing groups from the bottom as in [STR packing](/str-packing/), turns the two-group problem into the many-group problem of building a whole tree.

## Applications

Every dynamic R-tree solves this problem at each node overflow: Guttman's R-tree with the quadratic or linear split, the [R*-tree](/r-star-tree/) with its sorted split, and the [X-tree](/x-tree/) with a split that may be refused. The same problem appears in [bounding volume hierarchies](/bounding-volume-hierarchy/) for ray tracing, where a node is split by a cost that estimates the work of a ray, and in the [SS-tree](/ss-tree/) and the [SR-tree](/sr-tree/), with spheres in place of boxes.

## References
