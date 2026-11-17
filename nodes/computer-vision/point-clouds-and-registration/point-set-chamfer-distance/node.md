---
tag: J3N3YK
kind: definition
slug: point-set-chamfer-distance
name: Chamfer distance between point sets
aliases:
- symmetric chamfer distance
area: computer-vision/point-clouds-and-registration
level: core
summary: "The sum over both point sets of the squared distance from each point to its nearest point in the other set: a common loss and score for point clouds, but not a metric."
prereqs: [point-cloud, nearest-neighbor-search]
see_also: [hausdorff-distance, chamfer-distance, distance-transform, kd-tree, point-cloud-registration, non-rigid-registration, iterative-closest-point, approximate-nearest-neighbor]
sources:
  - paper: arxiv:1612.00603
    title: "Haoqiang Fan, Hao Su and Leonidas Guibas, A point set generation network for 3D object reconstruction from a single image, Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2017)"
    locator: "Section 4.3, the Chamfer distance as the sum, in both directions, of the squared distance from each point to its nearest neighbour in the other set, used as a loss beside the earth mover's distance"
  - paper: "H. G. Barrow, J. M. Tenenbaum, R. C. Bolles and H. C. Wolf, Parametric correspondence and chamfer matching: two new techniques for image matching, Proceedings of the 5th International Joint Conference on Artificial Intelligence (IJCAI 1977), 659-663"
    title: "H. G. Barrow, J. M. Tenenbaum, R. C. Bolles and H. C. Wolf, Parametric correspondence and chamfer matching: two new techniques for image matching, Proceedings of the 5th International Joint Conference on Artificial Intelligence (IJCAI 1977), 659-663"
    locator: "Chamfer matching: an edge template is scored by the values of a distance transform of the image edges under its points"
---

The chamfer distance between two finite point sets measures how far each point of one set is from the nearest point of the other, in both directions, and adds it all up. It is cheap to compute with a [nearest neighbour search](/nearest-neighbor-search/), it needs no correspondence between the points, and it has a gradient almost everywhere. For these reasons it is the standard loss for neural networks that output [point clouds](/point-cloud/), and a common score for how well a reconstruction or a [registration](/point-cloud-registration/) fits. This page uses the form of Fan, Su and Guibas (2017): squared distances, summed over the points of both sets. Other papers use means instead of sums, or plain distances instead of squared ones; these forms differ by constant factors or in their sensitivity to far points, and a paper should always say which one it uses. The name comes from chamfer matching in images (Barrow et al., 1977), which is a different, one-sided measure on an image grid.

## Definition

Let $S_1$ and $S_2$ be finite, nonempty subsets of $\mathbb{R}^d$. The chamfer distance is

$$d_{\mathrm{CD}}(S_1, S_2) = \sum_{x \in S_1} \min_{y \in S_2} \|x - y\|_2^2 + \sum_{y \in S_2} \min_{x \in S_1} \|x - y\|_2^2 .$$

Each sum is a one-sided chamfer distance: the first says how well $S_2$ covers the points of $S_1$, and the second how well $S_1$ covers the points of $S_2$.

Other forms in use:

- **Mean form.** Divide each sum by the size of its set, $\frac{1}{|S_1|} \sum_{x \in S_1} \cdots + \frac{1}{|S_2|} \sum_{y \in S_2} \cdots$. Many libraries compute this form, so that the value does not grow with the number of points.
- **Plain distances.** Use $\|x - y\|_2$ instead of its square. A far point then counts less, and the value has the units of a length.
- **One-sided form.** Keep only one of the two sums, for example when $S_2$ is a full model and $S_1$ a partial scan of it.

**Properties.** $d_{\mathrm{CD}}$ is symmetric, it is at least 0, and it is 0 exactly when $S_1 = S_2$: if it is 0, every point of each set lies in the other. It is not a metric, because it breaks the triangle inequality, as the examples show. It ignores how many times a point is repeated, so it does not compare densities.

**Cost.** By brute force it takes $\Theta(|S_1| \cdot |S_2|)$ time. With a [k-d tree](/kd-tree/) on each set and $n = |S_1| + |S_2|$, the $n$ nearest neighbour queries take $O(\log n)$ time each on well spread points in low dimension, so about $O(n \log n)$ in all.

## Examples and non-examples

**A small case.** In the plane, let $S_1 = \{(0, 0), (2, 0)\}$ and $S_2 = \{(0, 1), (3, 0), (3, 1)\}$.

| Point | Set | Nearest in the other set | Squared distance |
|---|---|---|---|
| $(0, 0)$ | $S_1$ | $(0, 1)$ | 1 |
| $(2, 0)$ | $S_1$ | $(3, 0)$ | 1 |
| $(0, 1)$ | $S_2$ | $(0, 0)$ | 1 |
| $(3, 0)$ | $S_2$ | $(2, 0)$ | 1 |
| $(3, 1)$ | $S_2$ | $(2, 0)$ | 2 |

So $d_{\mathrm{CD}} = (1 + 1) + (1 + 1 + 2) = 6$. The mean form gives $2/2 + 4/3 \approx 2.333$, and the form with plain distances gives $1 + 1 + 1 + 1 + \sqrt{2} \approx 5.414$. The [Hausdorff distance](/hausdorff-distance/), the largest of these nearest distances, is $\sqrt{2}$.

**The triangle inequality fails.** On the line, let $S_1 = \{0\}$, $S_2 = \{1\}$ and $S_3 = \{2\}$. Then $d_{\mathrm{CD}}(S_1, S_3) = 4 + 4 = 8$, but $d_{\mathrm{CD}}(S_1, S_2) + d_{\mathrm{CD}}(S_2, S_3) = 2 + 2 = 4$. The squares cause this. The form with plain distances fails too, for another reason: with $S_1 = \{0\}$, $S_2 = \{0, 1\}$ and $S_3 = \{1, 1.1, 1.2\}$, it gives $1 + 3.3 = 4.3$ from $S_1$ to $S_3$, but only $1$ from $S_1$ to $S_2$ plus $1 + 0.3 = 1.3$ from $S_2$ to $S_3$. Each point of $S_3$ adds its own term, so a set with many points far from a small set gets a large value.

**Density is not seen.** Let $S_1$ be 100 points spread evenly on a segment, and $S_2$ the same 100 points plus 900 more points packed near one end. Each point of $S_2$ has a near point in $S_1$, and each point of $S_1$ lies in $S_2$, so the chamfer distance is small, although the two sets sample the segment in very different ways. A measure that moves mass from one set to the other, such as the earth mover's distance with equal total weight on each set, sees this difference.

**Not the image chamfer distance.** The [chamfer distance transform](/chamfer-distance/) of an image gives each pixel an approximate distance to the nearest edge pixel, by two raster passes with small integer weights. Chamfer matching (Barrow et al., 1977) scores an edge template at a pose by the values of such a [distance transform](/distance-transform/) under the template points. That score is one-sided, from the template to the image, and it lives on a pixel grid. The point set chamfer distance is two-sided and uses exact Euclidean distances between points.

## Related definitions

- **Hausdorff distance.** The [Hausdorff distance](/hausdorff-distance/) replaces each sum by a maximum and uses plain distances: $\max(\max_{x} \min_{y} \|x - y\|, \max_{y} \min_{x} \|x - y\|)$. It is a metric on finite sets. Each term of $d_{\mathrm{CD}}$ is at most its square, so $d_{\mathrm{CD}} \le (|S_1| + |S_2|) \cdot d_H^2$, and the mean form with plain distances is at most $2 d_H$. One far outlier sets the Hausdorff distance, but it is only one term in the chamfer sum.
- **Earth mover's distance.** For two sets of the same size, it is the smallest mean distance over all one-to-one matches, an [assignment problem](/assignment-problem/). It sees densities, but it costs much more to compute.
- **Registration costs.** The cost that [ICP](/iterative-closest-point/) lowers at each step is the one-sided chamfer distance from the moved source to the target, and some [non-rigid registration](/non-rigid-registration/) methods use the two-sided form as their data term.

## References
