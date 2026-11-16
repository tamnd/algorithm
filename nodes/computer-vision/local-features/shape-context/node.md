---
tag: A629T3
kind: algorithm
slug: shape-context
name: Shape context
aliases:
- shape context descriptor
area: computer-vision/local-features
level: advanced
summary: Describe each point of a shape by the log-polar histogram of the other points around it, then match two shapes by the least-cost assignment of chi-square costs between histograms.
solves: [object-recognition]
model: real-ram
complexity:
  vars: {n: the number of points of the first shape, m: the number of points of the second shape, K: the number of bins of a histogram}
  time: {worst: O(n^2 + m^2 + n m K + (n + m)^3), average: O(n^2 + m^2 + n m K + (n + m)^3), best: O(n^2 + m^2 + n m K + (n + m)^3)}
  space: {extra: O((n + m)^2 + (n + m) K)}
properties: {deterministic: true, exact: true, translation_invariant: true, scale_invariant: true, rotation_invariant: false, heuristic: false}
history:
  year: 2000
  people: [Serge Belongie, Jitendra Malik, Jan Puzicha]
  note: Belongie, Malik and Puzicha introduced shape contexts in 2000 and gave the full method with thin plate spline alignment and digit and object recognition in IEEE TPAMI in 2002.
prereqs: [feature-descriptor, hungarian-algorithm]
see_also: [assignment-problem, jonker-volgenant-algorithm, chi-squared-goodness-of-fit-test, chamfer-distance, point-set-chamfer-distance, non-rigid-registration, generalized-hough-transform, canny-edge-detector]
sources:
  - paper: doi:10.1109/34.993558
    title: Serge Belongie, Jitendra Malik and Jan Puzicha, Shape matching and object recognition using shape contexts, IEEE Transactions on Pattern Analysis and Machine Intelligence 24(4), 509-522, 2002
    locator: Section 3.1 (the log-polar histogram, 5 bins for log r and 12 for the angle, the chi-square cost), Section 3.2 (bipartite matching in O(N^3), dummy nodes), Section 3.3 (normalization by the mean distance, the tangent frame), Section 4 (modeling transformations, regularized thin plate splines), Section 4.3 (computational demands), Section 6.1 (MNIST), Appendix A (the radial range 0.125 to 2)
  - paper: doi:10.1002/nav.3800020109
    title: Harold W. Kuhn, The Hungarian method for the assignment problem, Naval Research Logistics Quarterly 2(1-2), 83-97, 1955
    locator: the whole paper (the assignment algorithm)
---

The shape context is a descriptor for a point on a shape, where a shape is a finite set of points, for example points sampled from the edges of an image. For a point $p_i$ it counts the other points of the shape in bins that are uniform in log distance and in angle around $p_i$. The histogram tells where the rest of the shape is, as seen from $p_i$, with more detail near $p_i$ than far away. To match two shapes, the method computes a chi-square cost between each histogram of one shape and each histogram of the other, and finds the one-to-one matching of least total cost with the [Hungarian algorithm](/hungarian-algorithm/). Belongie, Malik and Puzicha then aligned the shapes with a thin plate spline and used the matching cost for recognition of digits, objects and trademarks.

## In plain words

Stand on one point of a drawing and look around. Draw rings at growing distances, each ring twice as far as the one before or so, and cut the rings into 12 slices like a pie. Count how many points of the drawing fall into each piece. The counts form the description of the point where you stand. A point at the tip of the letter A sees most of the letter below it. A point at the foot sees most of it above and to one side. To compare two drawings, find the pairing of their points that makes the descriptions of paired points most alike in total. If the drawings show the same shape, the pairs are the same parts of the shape.

## The problem

The input is two finite point sets $P = \{p_1, \dots, p_n\}$ and $Q = \{q_1, \dots, q_m\}$ in the plane, the numbers of bins $n_r$ and $n_\theta$, the radial range $[r_{\mathrm{in}}, r_{\mathrm{out}})$ and an optional dummy cost $\varepsilon_d$. Let $\alpha_P$ be the mean distance between the $n^2$ ordered pairs of points of $P$, as in Section 3.3 of the paper. For $p_i$ and $j \ne i$, let

$$r_{ij} = \frac{\lVert p_j - p_i \rVert}{\alpha_P}, \qquad \theta_{ij} = \operatorname{atan2}(y_j - y_i,\, x_j - x_i) \in [0, 2\pi).$$

The radial bin of $r$ is $\lfloor n_r \log(r / r_{\mathrm{in}}) / \log(r_{\mathrm{out}} / r_{\mathrm{in}}) \rfloor$, and the angle bin of $\theta$ is $\lfloor n_\theta \theta / 2\pi \rfloor$. The shape context of $p_i$ is the histogram $h_i$ of the bins of the vectors $p_j - p_i$ with $r_{\mathrm{in}} \le r_{ij} < r_{\mathrm{out}}$, divided by its total. The paper uses $n_r = 5$, $n_\theta = 12$ and the range from $0.125$ to $2$, which gives $K = 60$ bins and the bin edges $0.125, 0.218, 0.379, 0.660, 1.149, 2$ in units of the mean distance.

The cost of matching $p_i$ with $q_j$ is the chi-square statistic

$$C_{ij} = \frac{1}{2} \sum_{k=1}^{K} \frac{(h_i(k) - h_j(k))^2}{h_i(k) + h_j(k)},$$

with $0/0$ taken as $0$. Since $h_i$ and $h_j$ sum to 1, $0 \le C_{ij} \le 1$. For $n = m$ the output is the permutation $\pi$ that minimizes $\sum_i C_{i \pi(i)}$, which is the [assignment problem](/assignment-problem/). With dummy nodes, each point can stay unmatched at the cost $\varepsilon_d$, and the cost matrix is padded to a square.

## The algorithm

```pseudo id=main
SHAPE-CONTEXT-MATCH(P, Q, ε_d)
L1  α ← the mean of ‖p_j - p_i‖ over all n^2 ordered pairs of P   ▷ the same for Q
L2  for each point p_i of P do                                   ▷ the same for Q
L3      for each j ≠ i, find the log r bin and the θ bin of (p_j - p_i) / α
L4      add 1 to that bin of h_i if r is in [r_in, r_out)
L5      divide h_i by its total
L6  C_ij ← 1/2 Σ_k (h_i(k) - h_j(k))^2 / (h_i(k) + h_j(k)) for each p_i of P and q_j of Q
L7  if n ≠ m or ε_d is given then pad C to a square matrix with dummy rows and columns of cost ε_d
L8  π ← the least-cost assignment of C, by the Hungarian method
L9  return π, with the points matched to dummies left unmatched, and its cost
```

Line L8 uses the shortest augmenting path form of the Hungarian method with row and column potentials, which takes $O(N^3)$ time for an $N \times N$ matrix. The paper uses the faster algorithm of Jonker and Volgenant, see the [Jonker-Volgenant algorithm](/jonker-volgenant-algorithm/), which solves the same problem.

With $\varepsilon_d$ given, our code pads to $(n + m) \times (n + m)$: a real row and a dummy column, or a dummy row and a real column, cost $\varepsilon_d$, and two dummies cost $0$. So each unmatched point of either shape costs $\varepsilon_d$, and a point stays unmatched exactly when no real partner is cheaper, as the paper says. Without $\varepsilon_d$ and with $n \ne m$, the smaller side is padded with the cost 1, which every assignment pays the same number of times.

### Alignment and shape distance

In the paper, the matching is one step of a loop. From the matched pairs, the method fits a regularized thin plate spline that maps one shape onto the other, warps the shape, and computes new shape contexts and a new matching, for a few iterations. The shape distance used for recognition is a weighted sum of the shape context cost, an appearance cost and the bending energy of the spline. The page implements the descriptor and the matching; the spline fit is a separate step.

## Example

Take the five points $(0, 0)$, $(1, 0)$, $(0, 1)$, $(-1, 0)$ and $(0, -1)$, a plus sign. The 25 ordered pairs have the distances 0 five times, 1 eight times, $\sqrt 2$ eight times and 2 four times, so

$$\alpha = \frac{8 + 8\sqrt 2 + 8}{25} \approx 1.0925 .$$

From the center, the four points are at $r = 1/\alpha \approx 0.915$, which is in the radial bin 3 (counted from 0), between 0.660 and 1.149. Their angles 0, 90, 180 and 270 degrees fall into the angle bins 0, 3, 6 and 9 of 30 degrees each. So the shape context of the center has $1/4$ in each of the bins $(3, 0)$, $(3, 3)$, $(3, 6)$ and $(3, 9)$.

From $(1, 0)$, the center is at $r = 0.915$ and angle 180 degrees, bin $(3, 6)$. The point $(-1, 0)$ is at $r = 2/\alpha \approx 1.831$ and 180 degrees, bin $(4, 6)$. The points $(0, 1)$ and $(0, -1)$ are at $r = \sqrt 2/\alpha \approx 1.294$ and the angles 135 and 225 degrees, bins $(4, 4)$ and $(4, 7)$. The two histograms share only the bin $(3, 6)$, where both hold $1/4$. Each of the other six bins holds $1/4$ in one histogram and 0 in the other, and adds $(1/4)^2 / (1/4) = 1/4$ to the sum. So $C = \frac{1}{2} \cdot \frac{6}{4} = 0.75$. Two opposite arm ends, $(1, 0)$ and $(-1, 0)$, share no bin, and their cost is the largest possible value, 1.

If the second shape is the same plus sign scaled by $0.5$, moved, and with the points listed in another order, the histograms are the same as before, the cost of the true matching is 0, and the Hungarian method returns that permutation.

## Correctness

The proof in `proofs/correctness.md` shows that:

- The histograms do not change under a translation and under a scaling by $s > 0$ of a shape, since the vectors $p_j - p_i$ do not change under a translation, and both the distances and $\alpha$ are multiplied by $s$.
- $0 \le C_{ij} \le 1$, and $C_{ij} = 0$ exactly when the two histograms are equal.
- The Hungarian method returns an assignment of least total cost, by the duality of the assignment problem.
- With the padding of line L7, an optimal assignment of the padded matrix gives an optimal partial matching in which each unmatched point costs $\varepsilon_d$.

Whether the least-cost matching pairs the right parts of two different drawings of a shape is not a theorem. It is the measured behavior of the descriptor, reported in Sections 4.2 and 6 of the paper.

## Complexity

The model is the [real RAM](/real-ram/), with $\log$ and $\operatorname{atan2}$ in $O(1)$ time. Let $K = n_r n_\theta$.

- Line L1 takes $O(n^2)$ time for $P$ and $O(m^2)$ for $Q$.
- Lines L2 to L5 take $O(n^2 + n K)$ time for $P$ and $O(m^2 + m K)$ for $Q$.
- Line L6 takes $O(n m K)$ time.
- Line L8 takes $O(N^3)$ time with $N = \max(n, m)$, or $N = n + m$ with dummies.

So the total time is $O(n^2 + m^2 + n m K + (n + m)^3)$, and the assignment dominates for $K$ fixed. The extra space is $O((n + m)^2)$ for the cost matrix and $O((n + m) K)$ for the histograms. The paper samples about 100 points per shape. It reports that one comparison with three iterations of matching and spline fitting took about 200 ms on a 500 MHz Pentium III; this is a measurement from 2002, not a bound.

## Properties

- **Translation and scale invariance.** Exact, by the normalization with the mean distance.
- **Rotation.** Not invariant in the plain form. The relative frame of Section 3.3 measures angles from the tangent at each point and gives full rotation invariance, which the paper notes is wrong for tasks such as telling 6 from 9.
- **Locality and global context.** Each histogram covers the whole shape out to twice the mean distance, so it is a rich descriptor, but it is sensitive to occlusion of large parts.
- **Log-polar bins.** The bins are finer near the point. The paper explains this as a positional uncertainty that grows linearly with the distance.
- **Outliers.** Dummy nodes let outliers stay unmatched. Outliers still change the histograms of the other points and the mean distance.
- **The sampling.** The points are samples of the shape, not special points. Different samplings of the same contour give similar, not equal, histograms.

## Variants and improvements

- **Tangent frame.** Measure angles relative to the tangent at each point for rotation invariance.
- **Appearance and tangent terms.** For MNIST the paper adds a tangent angle term with weight 0.1 to the cost.
- **Inner-distance shape context.** Ling and Jacobs replace the Euclidean distance by the shortest path inside the shape, which helps with articulated shapes.
- **3D shape context.** Frome and coauthors use spherical bins on range data.
- **Fast pruning.** For retrieval in large sets, later work of Mori, Belongie and Malik prunes candidates by comparing a few representative shape contexts before the full matching.
- **Other matchings.** The [Jonker-Volgenant algorithm](/jonker-volgenant-algorithm/) solves the same assignment faster in practice. A greedy matching is cheaper but not optimal.
- **Related distances.** The [chamfer distance](/chamfer-distance/) compares shapes without correspondences, and the [generalized Hough transform](/generalized-hough-transform/) votes for a pose.

## When to use it

Use shape contexts to match and compare silhouettes, contours, handwritten characters and logos, where the shape carries more information than the texture. They are a good choice when you need point correspondences between two shapes, for example to start a [non-rigid registration](/non-rigid-registration/). The cubic cost of the assignment limits the number of points to a few hundred. For keypoint matching between photographs, a descriptor of the image patch is a better choice.

## Pitfalls

- **The mean distance.** The paper divides by the mean over the $n^2$ pairs, which includes the $n$ zero distances. Some codes take the mean over pairs with $i \ne j$, which is larger by the factor $n / (n - 1)$. The bins then shift. Use the same rule on both shapes.
- **Points outside the range.** Points nearer than $r_{\mathrm{in}}$ or farther than $r_{\mathrm{out}}$ are not counted in our code. Some codes put them into the first or the last bin. The histograms of a shape with many close points can then be quite different.
- **Image coordinates.** With $v$ pointing down, the angle goes clockwise on the screen. This does not matter if both shapes use the same rule.
- **Empty histograms.** A point with no other point in range has an empty histogram. The chi-square cost against another empty histogram is 0.
- **Ties in the assignment.** Symmetric shapes, such as the plus sign, have several matchings of equal cost. Any of them is optimal.
- **The dummy cost.** If $\varepsilon_d$ is too small, all points go to dummies. If $\varepsilon_d > 1/2$, an optimal solution never leaves a point of each shape unmatched, because matching the two costs at most 1 and leaving both costs $2\varepsilon_d$. Then the dummies only take the extra points of the larger shape.

## Implementations

## History

Belongie, Malik and Puzicha introduced shape contexts in a 2000 conference paper and gave the full method in IEEE TPAMI in 2002. They used about 100 points sampled from Canny edges, the Jonker-Volgenant assignment algorithm and regularized thin plate splines. On MNIST, with 20,000 training digits and a 3-nearest-neighbor classifier, they reported a test error of 0.63 percent, a benchmark result of 2002. Shape contexts were also used for trademark retrieval and for 3D object recognition from views.

## References
