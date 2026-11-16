---
tag: 792P0V
kind: technique
slug: cost-aggregation
name: Cost aggregation
aliases:
- support aggregation
area: computer-vision/stereo-and-dense-reconstruction
level: core
summary: Replace each matching cost by a weighted sum of the costs at the same disparity over a support region, a box, an adaptive window or a tree, before choosing disparities.
prereqs: [cost-volume, stereo-matching-cost]
see_also: [block-matching-stereo, adaptive-support-weights, guided-filter, bilateral-filter, integral-image, box-blur, semi-global-matching, minimum-spanning-tree]
sources:
  - paper: doi:10.1023/A:1014573219977
    title: Daniel Scharstein and Richard Szeliski, A taxonomy and evaluation of dense two-frame stereo correspondence algorithms, International Journal of Computer Vision 47(1-3), 2002, 7-42
    locator: the part on aggregation of the matching cost (square windows, shiftable windows, Gaussian weights and diffusion as filters of the disparity space image)
  - paper: doi:10.1109/TPAMI.2012.156
    title: Asmaa Hosni, Christoph Rhemann, Michael Bleyer, Carsten Rother and Margrit Gelautz, Fast cost-volume filtering for visual correspondence and beyond, IEEE Transactions on Pattern Analysis and Machine Intelligence 35(2), 2013, 504-511
    locator: the guided filter applied to each slice of the cost volume, in time independent of the window size
  - paper: doi:10.1109/TPAMI.2006.70
    title: Kuk-Jin Yoon and In So Kweon, Adaptive support-weight approach for correspondence search, IEEE Transactions on Pattern Analysis and Machine Intelligence 28(4), 2006, 650-656
    locator: support weights from color similarity and distance in both windows
  - paper: "Qingxiong Yang, A non-local cost aggregation method for stereo matching, IEEE Conference on Computer Vision and Pattern Recognition, 2012"
    locator: aggregation on a minimum spanning tree of the image and the two pass computation in linear time
  - paper: "Daniel Scharstein and Richard Szeliski, Stereo matching with nonlinear diffusion, International Journal of Computer Vision 28(2), 1998"
    locator: aggregation by repeated local averaging that stops where the evidence is strong
  - paper: "Ke Zhang, Jiangbo Lu and Gauthier Lafruit, Cross-based local stereo matching using orthogonal integral images, IEEE Transactions on Circuits and Systems for Video Technology 19(7), 2009"
    locator: the cross-shaped adaptive support regions and their sums with integral images along rows and columns
---

Cost aggregation replaces each entry $C(p, d)$ of the [cost volume](/cost-volume/) by a weighted sum of the costs $C(q, d)$ of other pixels $q$ at the same disparity, $C_A(p, d) = \sum_q w(p, q)\, C(q, d)$, so that the cost of a pixel uses the evidence of its support region and not of the pixel alone. It is the second step of [stereo matching](/stereo-matching/) in the taxonomy of Scharstein and Szeliski (2002). Each disparity slice is filtered on its own, so aggregation is image filtering applied $D$ times: a box filter in [block matching](/block-matching-stereo/), a bilateral weight in [adaptive support weights](/adaptive-support-weights/), the [guided filter](/guided-filter/) in Hosni et al. (2013), or a filter on a tree in Yang (2012). The methods differ in the weights and in their cost per entry.

## In plain words

The cost of one pixel is a weak guess: noise, flat areas and repeated patterns make many disparities look equally good. Neighbors that lie on the same surface have the same disparity, so their costs at that disparity should be low too. Aggregation adds up the costs of the neighbors at each disparity, and the true disparity, where the whole surface agrees, wins more clearly. The hard part is to choose which neighbors to trust. A plain square trusts all of them, including pixels on another surface; better methods trust neighbors of similar color, or neighbors connected to the pixel without crossing an edge.

## When it applies

- The method chooses disparities from the costs, by winner-takes-all or by an optimizer, and the pixel costs are noisy or ambiguous.
- The scene is mostly made of surfaces that are smooth in depth, so that a pixel and most of its support have nearly the same disparity. This is an assumption about the scene; it fails at depth edges and on thin structures.
- The weight $w(p, q)$ does not depend on $d$, or depends on it only through the right image, so that each slice can be filtered as an image. The weight must be the same for all disparities of a pixel, or the aggregated costs of different disparities are not comparable.

## The template

```pseudo id=main
AGGREGATE(C, w)
L1  for d ← 0 to D - 1 do
L2      A ← SLICE(C, d)                       ▷ an H × W image of costs
L3      A ← FILTER(A, w)                       ▷ the hole: box, Gaussian, bilateral, guided, tree
L4      SET-SLICE(C, d, A)
L5  return C
```

The hole is the filter of line L3, with the weight $w(p, q)$ that it applies. Two questions decide it. First, which pixels may support $p$: a fixed window, a window that adapts its shape, or every pixel of the image with a weight that decays along a path. Second, the cost: a filter whose weights depend only on $q - p$ can use running sums or an [integral image](/integral-image/) and costs $O(1)$ per entry, while weights that depend on the image need either a fast edge-aware filter or $O(r^2)$ work per entry. A normalized form divides by $\sum_q w(p, q)$; it does not change winner-takes-all when this sum does not depend on $d$, but it does when invalid entries near the border are left out.

## Classic examples

- **Box window.** [Block matching](/block-matching-stereo/) sums the costs over a square, in $\Theta(W H D)$ time with an integral image or a [box blur](/box-blur/). It blurs depth edges: a near object looks larger by up to the radius of the window.
- **Gaussian and shiftable windows.** Scharstein and Szeliski (2002) compared Gaussian weights and shiftable windows, which take the best of the windows that contain the pixel, computed by a box filter followed by a min filter.
- **Cross-based support.** Zhang, Lu and Lafruit (2009) grow, for each pixel, arms along the row and the column while the color stays close, and sum over the cross-shaped region with integral images of rows and columns. The region follows edges and the cost stays $O(1)$ per entry.
- **Adaptive support weights.** [Adaptive support weights](/adaptive-support-weights/) weight each pixel of a large window by its color similarity and distance to the center in both images, a joint [bilateral filter](/bilateral-filter/) of each slice, at $\Theta(r^2)$ per entry.
- **Guided filter.** Hosni et al. (2013) filter each slice with the [guided filter](/guided-filter/), guided by the left image. It is edge-aware and uses box sums only, so the whole step costs $\Theta(W H D)$ for any radius.
- **Tree filter.** Yang (2012) builds a [minimum spanning tree](/minimum-spanning-tree/) of the 4-connected pixel grid with edge weights $|I(p) - I(q)|$, and sets $w(p, q) = \exp(-\Delta(p, q) / \sigma)$, where $\Delta$ is the sum of the edge weights on the tree path. Every pixel supports every other one, and two passes over the tree compute all sums in $\Theta(W H)$ per slice.
- **Paths of semi-global matching.** [Semi-global matching](/semi-global-matching/) sums, over 8 or 16 directions, costs that are minimized along 1D paths with a smoothness penalty. Hirschmüller calls this an aggregation, but it is a minimization, not a weighted sum.

**A tree example.** Take a row of four pixels with intensities $(10, 12, 90, 92)$, the costs $(5, 1, 9, 7)$ at one disparity, and $\sigma = 10$. On a row the tree is the row itself, and the edge weights give $S = e^{-\Delta/\sigma}$ of $0.8187$, $0.0004$ and $0.8187$ between neighbors. The aggregated costs $\sum_q S(p, q) C(q)$ are $(5.824, 5.100, 14.733, 14.370)$. For pixel 1 that is $1 + 0.8187 \cdot 5$ plus less than $0.01$ from the other side of the edge between 12 and 90. A box of three pixels gives $5 + 1 + 9 = 15$ at pixel 1 and mixes the two surfaces. The two pass rule of Yang, $C^{\uparrow}(p) = C(p) + \sum_{c} S(p, c) C^{\uparrow}(c)$ from the leaves to the root and $C_A(c) = S(p, c) C_A(p) + (1 - S(p, c)^2) C^{\uparrow}(c)$ from the root down, gives the same four numbers.

## Variations

- **Symmetric weights.** Use the weights of both images, as adaptive support weights do, or of the left image only, which is cheaper and nearly as good in many scenes.
- **Multi-scale aggregation.** Aggregate at several resolutions and combine the results, so that large flat areas get support from far away.
- **Iterative diffusion.** Repeat a small local average many times, a discrete diffusion of each slice; Scharstein and Szeliski (1998) proposed a nonlinear version that stops where the evidence is strong.
- **Learned aggregation.** Deep stereo networks process the cost volume with 3D convolutions or learned guided filters, which aggregate across disparities as well as pixels.

## Pitfalls

- **Weights that depend on $d$ in the wrong way.** If the sum of weights changes with $d$ and the result is not normalized, larger windows at some disparities win for no reason. Normalize, or keep the support the same for all $d$.
- **Invalid entries.** The first $d$ columns of slice $d$ have no match. Summing their large invalid values ruins the sums near the left border; leave them out and normalize, or mark the border as invalid.
- **Foreground fattening.** Any support that crosses a depth edge favors the more textured side, usually the near object. Box windows show this most.
- **Color edges that are not depth edges.** Edge-aware weights cut the support at texture edges inside a surface, which leaves small, weak supports in highly textured areas.
- **Overflow.** Sums of integer costs over large windows need wide words; see the bounds on the [block matching](/block-matching-stereo/) page.

## References
