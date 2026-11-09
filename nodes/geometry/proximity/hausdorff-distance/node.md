---
tag: HJ9H2W
kind: definition
slug: hausdorff-distance
name: Hausdorff distance
aliases:
- directed Hausdorff distance
- Pompeiu-Hausdorff distance
area: geometry/proximity
level: intro
summary: Maximum over points of one set of the distance to the nearest point of the other set; a measure of shape dissimilarity.
prereqs: [euclidean-distance, metric-space]
see_also: [frechet-distance, point-to-segment-distance, bichromatic-closest-pair, voronoi-diagram, nearest-neighbor-search, proximity-problems]
sources:
  - paper: doi:10.1109/34.232073
    title: Daniel P. Huttenlocher, Gregory A. Klanderman and William J. Rucklidge, Comparing images using the Hausdorff distance, IEEE Transactions on Pattern Analysis and Machine Intelligence 15(9), 1993
    locator: Section 2 (the directed and undirected Hausdorff distance of finite point sets, the metric property, and the computation with a Voronoi diagram)
  - paper: "Helmut Alt, Bernd Behrends and Johannes Blömer, Approximate matching of polygonal shapes, Annals of Mathematics and Artificial Intelligence 13, 1995, 251-265"
    locator: the Hausdorff distance between two sets of segments in O((m + n) log(m + n)) time with Voronoi diagrams
  - paper: "Helmut Alt and Leonidas J. Guibas, Discrete geometric shapes: matching, interpolation, and approximation, in J.-R. Sack and J. Urrutia (eds.), Handbook of Computational Geometry, Elsevier, 2000, 121-153"
    locator: the sections on the Hausdorff distance and the Fréchet distance (definitions, algorithms for point sets, segments and polygons)
---

The Hausdorff distance between two sets $A$ and $B$ is the smallest $\varepsilon$ such that each point of $A$ is within $\varepsilon$ of some point of $B$ and each point of $B$ is within $\varepsilon$ of some point of $A$. Its one-sided form, the *directed* Hausdorff distance $h(A, B)$, asks only for the first condition. It is a [metric](/metric-space/) on the non-empty compact sets of $\mathbb{R}^d$ and the standard measure of how far apart two shapes are, when the order of points along them does not matter. For finite sets it is a max of mins of [Euclidean distances](/euclidean-distance/), and the comparisons can be done on squared distances.

## Definition

Let $A, B \subseteq \mathbb{R}^d$ be non-empty and compact, and let $\|p - q\|$ be the Euclidean distance. The distance from a point $a$ to the set $B$ is $\mathrm{dist}(a, B) = \min_{b \in B} \|a - b\|$; the minimum exists because $B$ is compact.

The **directed Hausdorff distance** from $A$ to $B$ is

$$h(A, B) = \max_{a \in A} \ \min_{b \in B} \ \|a - b\| .$$

The **Hausdorff distance** is the larger of the two directions:

$$H(A, B) = \max\{\, h(A, B),\ h(B, A) \,\}.$$

**Equivalent form.** For $\varepsilon \ge 0$ let $A_\varepsilon = \{x : \mathrm{dist}(x, A) \le \varepsilon\}$ be the closed $\varepsilon$-neighbourhood of $A$. Then $h(A, B) = \min\{\varepsilon \ge 0 : A \subseteq B_\varepsilon\}$ and

$$H(A, B) = \min\{\, \varepsilon \ge 0 : A \subseteq B_\varepsilon \text{ and } B \subseteq A_\varepsilon \,\}.$$

**Metric.** On the family of non-empty compact subsets of $\mathbb{R}^d$, $H$ is a metric:

- $H(A, B) \ge 0$, and $H(A, B) = 0$ if and only if $A = B$. If $H(A, B) = 0$, each $a \in A$ has $\mathrm{dist}(a, B) = 0$, so $a \in B$ because $B$ is closed; by symmetry $A = B$.
- $H(A, B) = H(B, A)$ by the definition.
- $H(A, C) \le H(A, B) + H(B, C)$. For $a \in A$, take $b \in B$ with $\|a - b\| = \mathrm{dist}(a, B) \le h(A, B)$, then $c \in C$ with $\|b - c\| \le h(B, C)$. So $\mathrm{dist}(a, C) \le \|a - c\| \le h(A, B) + h(B, C)$. Taking the maximum over $a$ gives $h(A, C) \le h(A, B) + h(B, C) \le H(A, B) + H(B, C)$, and the same argument in the other direction bounds $h(C, A)$.

The directed distance $h$ is not symmetric, so it is not a metric. For finite sets with $|A| = m$ and $|B| = n$, the definition is an $O(mn)$ computation, and since squaring is increasing on $[0, \infty)$,

$$h(A, B)^2 = \max_{a \in A} \min_{b \in B} \|a - b\|^2,$$

which is exact on integer input.

## Examples and non-examples

- **Two finite sets.** Let $A = \{(0,0), (4,0), (4,3)\}$ and $B = \{(0,1), (4,0)\}$. The squared distances from the points of $A$ to their nearest points in $B$ are $1$, $0$ and $9$, so $h(A, B) = 3$. From $B$ to $A$ they are $1$ and $0$, so $h(B, A) = 1$. Hence $H(A, B) = 3$. The point $(4, 3)$ alone makes the distance large: the Hausdorff distance is sensitive to a single outlier.
- **A segment against its end points.** Let $A$ be the segment from $(0, 0)$ to $(2, 0)$ and $B = \{(0, 0), (2, 0)\}$. Then $h(B, A) = 0$, but $h(A, B) = 1$, reached at the midpoint $(1, 0)$. So for sets of segments the maximum is not always at a vertex: it can be inside an edge, where the edge crosses the [Voronoi diagram](/voronoi-diagram/) of the other set.
- **Same image, different order.** The segment $P$ from $(0, 0)$ to $(4, 0)$ and the polyline $Q$ through $(0, 0)$, $(4, 0)$, $(0, 0)$, $(4, 0)$ cover the same points, so $H(P, Q) = 0$. Their [Fréchet distance](/frechet-distance/) is $2$, because $Q$ goes back and forth. The Hausdorff distance ignores the order of the points along a curve; the Fréchet distance does not, and it is always at least as large.
- **A non-example: sets that are not closed.** For the open interval $A = (0, 1)$ and the closed interval $B = [0, 1]$ of the real line, the supremum form of the definition gives $H(A, B) = 0$ although $A \ne B$. This is why the metric is defined on compact (closed and bounded) sets.
- **A non-example: the closest pair distance.** $\min_{a \in A} \min_{b \in B} \|a - b\|$ is the [bichromatic closest pair](/bichromatic-closest-pair/) distance, a min of mins. It is zero when the sets share one point, however different they are elsewhere, so it is not a distance between shapes.

## Related definitions

- [Fréchet distance](/frechet-distance/): a distance between curves that respects the order along them; it is an upper bound on the Hausdorff distance of their images.
- [Bichromatic closest pair](/bichromatic-closest-pair/): the min of mins, against the max of mins of this page.
- [Nearest neighbor search](/nearest-neighbor-search/): $\mathrm{dist}(a, B)$ is one nearest neighbor query; the directed Hausdorff distance is the maximum over a batch of queries, so a [kd-tree](/kd-tree/) or a [Voronoi diagram](/voronoi-diagram/) of $B$ computes it fast.
- [Distance from a point to a segment](/point-to-segment-distance/): the inner minimum when $B$ is a polygon or a polyline.

## References
