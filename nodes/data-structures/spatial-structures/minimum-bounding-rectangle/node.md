---
tag: GH5J0H
kind: definition
slug: minimum-bounding-rectangle
name: Minimum bounding rectangle
aliases:
- MBR
- bounding box
area: data-structures/spatial-structures
level: intro
summary: Smallest axis-aligned box enclosing a set of geometric objects, used as the key in most spatial trees.
prereqs: [bounding-volume]
see_also: [axis-aligned-bounding-box, overlap-and-dead-space, r-tree, object-partitioning, bounding-volume-hierarchy, minimum-enclosing-circle, separating-axis-theorem]
sources:
  - paper: doi:10.1145/602259.602266
    title: Antonin Guttman, R-trees, a dynamic index structure for spatial searching, Proceedings of ACM SIGMOD 1984
    locator: Section 2 (index records as the smallest rectangle that spatially contains the object) and Section 3 (the insertion algorithm, which chooses the subtree whose rectangle needs the least enlargement)
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 4, Bounding Volumes, Section 4.2 Axis-aligned Bounding Boxes (the min-max and center-radius forms, the overlap test, and the box of a set of points)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 2, Object-Based and Image-Based Image Representations (minimum bounding boxes as approximations of objects, and the R-tree)
---

A minimum bounding rectangle (MBR) of a bounded set of points in the plane is the smallest rectangle with sides parallel to the coordinate axes that contains the set. In $d$ dimensions the same object is an axis-parallel box, and graphics calls it an [axis-aligned bounding box](/axis-aligned-bounding-box/). It is the simplest [bounding volume](/bounding-volume/): it takes $2d$ numbers, it is built in one pass, and two boxes are tested for overlap with $2d$ comparisons. Most spatial trees, from the [R-tree](/r-tree/) to the [bounding volume hierarchy](/bounding-volume-hierarchy/), store an MBR as the key of each entry and use it to filter out objects before an exact test.

## Definition

A *box* in $\mathbb{R}^d$ is a product of closed intervals
$$B = [\ell_1, h_1] \times [\ell_2, h_2] \times \cdots \times [\ell_d, h_d], \qquad \ell_i \le h_i,$$
and is written by its two corners $\ell = (\ell_1, \ldots, \ell_d)$ and $h = (h_1, \ldots, h_d)$.

Let $S \subset \mathbb{R}^d$ be nonempty and bounded. The **minimum bounding rectangle** of $S$ is
$$\operatorname{MBR}(S) = \prod_{i=1}^{d} \Big[ \inf_{p \in S} p_i ,\ \sup_{p \in S} p_i \Big].$$
For a finite family of objects $o_1, \ldots, o_n$, each a bounded set, the MBR of the family is $\operatorname{MBR}(o_1 \cup \cdots \cup o_n)$.

**It is the least box that contains $S$.** If a box $B$ with corners $\ell, h$ contains $S$, then $\ell_i \le p_i \le h_i$ for each $p \in S$ and each axis $i$, so $\ell_i \le \inf_{p} p_i$ and $h_i \ge \sup_p p_i$, and $\operatorname{MBR}(S) \subseteq B$. The MBR itself contains $S$, because each coordinate of each point lies between its infimum and its supremum. So $\operatorname{MBR}(S)$ is the intersection of all boxes that contain $S$, it is unique, and it has the least volume and the least perimeter among them. When $S$ is closed (for example, a finite set of points or polygons), each infimum and supremum is attained, so each face of the MBR touches $S$.

**Operations on boxes.** Let $A$ and $B$ be boxes with corners $(a^{\ell}, a^{h})$ and $(b^{\ell}, b^{h})$.

- *Union box*: $\operatorname{MBR}(A \cup B)$ has corners $\min(a^{\ell}_i, b^{\ell}_i)$ and $\max(a^{h}_i, b^{h}_i)$ on each axis. Since the infimum of a union is the smaller infimum, $\operatorname{MBR}(S \cup T) = \operatorname{MBR}(\operatorname{MBR}(S) \cup \operatorname{MBR}(T))$. So the box of a node of a tree is computed from the boxes of its children, without the objects.
- *Overlap test*: $A \cap B \ne \emptyset$ if and only if $a^{\ell}_i \le b^{h}_i$ and $b^{\ell}_i \le a^{h}_i$ for each axis $i$. A product of sets is nonempty exactly when each factor is, and two closed intervals meet exactly when each one starts before the other ends. When the boxes meet, $A \cap B$ is again a box, with corners $\max(a^{\ell}_i, b^{\ell}_i)$ and $\min(a^{h}_i, b^{h}_i)$.
- *Containment*: $B \subseteq A$ if and only if $a^{\ell}_i \le b^{\ell}_i$ and $b^{h}_i \le a^{h}_i$ for each $i$.
- *Measures*: the volume (area for $d = 2$) is $\prod_i (h_i - \ell_i)$, and the *margin* is $\sum_i (h_i - \ell_i)$, which is half the perimeter for $d = 2$. The *enlargement* of $A$ by $B$ is $\operatorname{vol}(\operatorname{MBR}(A \cup B)) - \operatorname{vol}(A)$.
- *Distance*: the Euclidean distance from a point $q$ to $A$ is $\sqrt{\sum_i \delta_i^2}$ with $\delta_i = \max(a^{\ell}_i - q_i,\ 0,\ q_i - a^{h}_i)$. It is a lower bound on the distance from $q$ to each object inside $A$, which is the basis of branch-and-bound [nearest neighbor search](/nearest-neighbor-search/) in spatial trees.

Each operation takes $\Theta(d)$ time, and the MBR of $n$ points takes $\Theta(dn)$ time: one minimum and one maximum per axis.

## Examples and non-examples

- **A point set.** For $S = \{(1, 5), (4, 2), (3, 7)\}$, $\operatorname{MBR}(S) = [1, 4] \times [2, 7]$. Its area is $3 \cdot 5 = 15$ and its margin is $3 + 5 = 8$. Each of its four sides touches a point of $S$: $(1, 5)$ is on the left side, $(4, 2)$ on the right and the bottom sides, and $(3, 7)$ on the top side.
- **Union and enlargement.** Let $A = [1, 4] \times [2, 7]$ and $B = [3, 6] \times [6, 9]$. Then $\operatorname{MBR}(A \cup B) = [1, 6] \times [2, 9]$, with area 35. The enlargement of $A$ by $B$ is $35 - 15 = 20$. The boxes overlap, and $A \cap B = [3, 4] \times [6, 7]$, with area 1.
- **Distance.** From $q = (8, 0)$ to $A$: $\delta_1 = 8 - 4 = 4$ and $\delta_2 = 2 - 0 = 2$, so the distance is $\sqrt{20} \approx 4.472$. The nearest point of $A$ is its corner $(4, 2)$.
- **A diagonal segment.** The segment from $(0, 0)$ to $(10, 10)$ has the MBR $[0, 10]^2$ of area 100, while the segment has area 0. Each point of the box off the diagonal is [dead space](/overlap-and-dead-space/): a query that hits only that part of the box passes the filter but finds nothing. This is the main weakness of the MBR for long thin objects that are not parallel to an axis.
- **Non-example: the box of the intersection.** For $A = \{(0, 0), (2, 2)\}$ and $B = \{(0, 2), (2, 0)\}$, the boxes $\operatorname{MBR}(A) = \operatorname{MBR}(B) = [0, 2]^2$ are equal, but $A \cap B = \emptyset$. In general only $\operatorname{MBR}(A \cap B) \subseteq \operatorname{MBR}(A) \cap \operatorname{MBR}(B)$ holds. So the overlap of two boxes is a necessary test for the overlap of two objects, not a sufficient one; a spatial query that uses boxes needs an exact *refinement* step on the candidates it finds.
- **Non-example: the smallest rotated rectangle.** The rectangle of least area that contains a set, with any orientation, is an *oriented bounding box*, not an MBR. For the diagonal segment above it has area 0. It fits better but needs more numbers and a costlier overlap test, the [separating axis](/separating-axis-theorem/) test. The [rotating calipers](/rotating-calipers/) find it for a convex polygon.
- **Non-example: an unbounded set.** A half-plane or a line not parallel to an axis has no MBR, since some infimum or supremum is infinite.

## Related definitions

- [Axis-aligned bounding box](/axis-aligned-bounding-box/): the same box, under its name in graphics and collision detection.
- [Bounding volume](/bounding-volume/): the general idea of a simple shape that contains a complex one; spheres, oriented boxes and $k$-DOPs are other choices.
- [Overlap and dead space](/overlap-and-dead-space/): the two quality measures of a set of MBRs in a spatial index.
- [Minimum enclosing circle](/minimum-enclosing-circle/) and [minimum enclosing ball](/minimum-enclosing-ball/): the smallest disk or ball, which is invariant under rotation, unlike the MBR.
- [Convex hull](/convex-hull/): the smallest convex set that contains $S$. It is contained in the MBR, and both have the same extreme coordinates on each axis.
- [Object partitioning](/object-partitioning/): the index design that groups objects and stores the MBR of each group, as in the [R-tree](/r-tree/).

## References
