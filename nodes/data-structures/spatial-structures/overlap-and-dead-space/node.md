---
tag: 38PMR2
kind: definition
slug: overlap-and-dead-space
name: Overlap and dead space
aliases:
- bounding-region overlap
area: data-structures/spatial-structures
level: core
summary: 'Two quality measures of a spatial index: overlap is shared area between sibling regions, dead space is covered area that holds no data.'
prereqs: [minimum-bounding-rectangle]
see_also: [object-partitioning, r-tree, r-star-tree, r-plus-tree, r-tree-node-splitting, space-partitioning, spatial-index]
sources:
  - paper: doi:10.1145/93597.98741
    title: Norbert Beckmann, Hans-Peter Kriegel, Ralf Schneider and Bernhard Seeger, The R*-tree, an efficient and robust access method for points and rectangles, Proceedings of ACM SIGMOD 1990
    locator: the optimization criteria for directory rectangles (area covered, overlap, margin and storage utilization) and the definition of the overlap of an entry
  - paper: "Timos Sellis, Nick Roussopoulos and Christos Faloutsos, The R+-tree, a dynamic index for multi-dimensional objects, Proceedings of the 13th International Conference on Very Large Data Bases (VLDB), 1987"
    locator: the discussion of coverage and overlap, and the clipping of objects to avoid overlap among siblings
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 2, Object-Based and Image-Based Image Representations (object hierarchies such as the R-tree, and the methods that remove overlap by disjoint decomposition)
---

Overlap and dead space are two measures of how well the regions of a [spatial index](/spatial-index/) fit the data. *Overlap* is the volume that two sibling regions share, so a query in that part must search both. *Dead space* is the volume that a region covers but that no object inside it covers, so a query there passes the filter of the region and then finds nothing. Indexes that group objects into [bounding rectangles](/minimum-bounding-rectangle/), such as the [R-tree](/r-tree/), trade the two against each other, and the split and insertion rules of the [R*-tree](/r-star-tree/) aim to make both small.

## Definition

Let $N$ be a node of a spatial index, with region $R \subset \mathbb{R}^d$ and children with regions $R_1, \ldots, R_m \subseteq R$. Write $\operatorname{vol}$ for volume (area when $d = 2$).

- The **coverage** of $N$ is $\operatorname{cov}(N) = \sum_{i=1}^{m} \operatorname{vol}(R_i)$.
- The **overlap** of $N$ is the total pairwise shared volume
$$\operatorname{ov}(N) = \sum_{1 \le i < j \le m} \operatorname{vol}(R_i \cap R_j).$$
The R*-tree also uses the overlap of one entry, $\operatorname{ov}(R_k) = \sum_{i \ne k} \operatorname{vol}(R_k \cap R_i)$.
- The **multiply covered volume** of $N$ is $\operatorname{vol}\{x : x \text{ lies in at least two of the } R_i\}$. It is at most $\operatorname{ov}(N)$, with equality when no point lies in three regions, because a point in exactly $c \ge 2$ regions is counted $\binom{c}{2} \ge 1$ times in the sum.
- Let $C \subseteq R$ be the part of the space that the data inside $N$ occupies: the union of the children's regions for a directory node, or the union of the objects for a leaf. The **dead space** of $N$ is
$$\operatorname{dead}(N) = \operatorname{vol}(R \setminus C) = \operatorname{vol}(R) - \operatorname{vol}(C).$$

A node of a space-partitioning index, such as a [k-d tree](/kd-tree/) or a [quadtree](/quadtree/), has children whose regions are disjoint and cover $R$, so its overlap and its dead space with respect to its children are both 0. The measures matter for [object partitioning](/object-partitioning/), where each region is the minimum bounding rectangle of its contents.

**Why they cost time.** A point query at $q$ must enter each child $i$ with $q \in R_i$. If $q$ is uniform in $R$, then by linearity of expectation the expected number of children that it enters is
$$\sum_{i=1}^m \Pr[q \in R_i] = \frac{\operatorname{cov}(N)}{\operatorname{vol}(R)},$$
and the probability that it enters two or more is the multiply covered volume over $\operatorname{vol}(R)$. With no overlap, a point query follows at most one path from the root. With overlap, it may follow many. Dead space adds visits that report nothing, since a query point in $R_i \setminus C_i$ enters child $i$ for no result.

## Examples and non-examples

- **Measures of one node.** Let $R = [0, 10]^2$ and the children $R_1 = [0, 6]^2$, $R_2 = [4, 10]^2$ and $R_3 = [0, 3] \times [7, 10]$. Only $R_1$ and $R_2$ meet, in $[4, 6]^2$, so $\operatorname{ov}(N) = 4$. The coverage is $36 + 36 + 9 = 81$ and the union has area $81 - 4 = 77$, so the dead space of $N$ with respect to its children is $100 - 77 = 23$. A uniform query point enters $0.81$ children on average: it enters none with probability $0.23$, one with probability $0.73$ and two with probability $0.04$.
- **Dead space of a leaf.** A leaf that holds the two squares $[0, 2]^2$ and $[4, 6]^2$ has the MBR $[0, 6]^2$ of area 36. The objects cover 8, so the dead space is 28, which is 78 percent of the box.
- **Two groupings of the same data.** Take the four unit squares in the corners of $[0, 10]^2$: $a = [0, 1]^2$, $b = [9, 10] \times [0, 1]$, $c = [0, 1] \times [9, 10]$ and $d = [9, 10]^2$, and two leaves of two objects each. The grouping $\{a, d\}, \{b, c\}$ gives two leaves with the same MBR $[0, 10]^2$: overlap 100 and dead space $100 - 2 = 98$ in each leaf. The grouping $\{a, b\}, \{c, d\}$ gives $[0, 10] \times [0, 1]$ and $[0, 10] \times [9, 10]$: overlap 0 and dead space $10 - 2 = 8$ in each leaf. The data are the same; only the grouping changes, and this is the choice that a [node split](/r-tree-node-splitting/) makes.
- **Overlap that no grouping removes.** The two rectangles $[0, 10] \times [4, 6]$ and $[4, 6] \times [0, 10]$ cross, and they share the square $[4, 6]^2$ of area 4. If they are in different leaves, the two leaf MBRs overlap by at least 4. Only an index that cuts objects into parts and stores a part in each region, as the [R+-tree](/r-plus-tree/) does, gets zero overlap here, at the price of storing such an object more than once.
- **Non-example: overlap between non-siblings.** A region of one subtree and a region of another subtree at a different depth may also intersect. The definition counts only siblings, because only siblings compete for the same step of a search. If two regions in different subtrees meet, their ancestors that are siblings also meet, since they contain them, so the overlap already shows at that level.
- **Non-example: dead space of a query.** The part of a query rectangle that holds no objects is not dead space. Dead space is a property of the index, not of a query.

## Related definitions

- [Minimum bounding rectangle](/minimum-bounding-rectangle/): the region shape for which these measures are usually computed.
- [Object partitioning](/object-partitioning/) and [space partitioning](/space-partitioning/): the two designs of a spatial index; the first has overlap and dead space, the second has neither but may split or copy objects.
- [R*-tree](/r-star-tree/): an R-tree whose insertion picks the subtree with the least increase of overlap at the leaf level, and whose split minimizes margin, then overlap, then area.
- [R+-tree](/r-plus-tree/): an R-tree variant with no overlap among siblings, by clipping.
- The **margin** (the sum of the side lengths of a box) is a third measure. Of all boxes with a given area, a square has the least margin, so a small margin means boxes that are close to square.

## References
