---
tag: KDEN2N
kind: problem
slug: stereo-matching
name: Stereo matching
aliases:
- stereo correspondence
- dense stereo
area: computer-vision/stereo-and-dense-reconstruction
level: core
summary: For each pixel of one rectified image, find the disparity of the matching pixel in the other image of a stereo pair.
prereqs: [disparity, stereo-rectification]
see_also: [stereo-matching-cost, cost-volume, cost-aggregation, block-matching-stereo, semi-global-matching, graph-cut-stereo, multi-view-stereo, optical-flow]
sources:
  - paper: doi:10.1023/A:1014573219977
    title: Daniel Scharstein and Richard Szeliski, A taxonomy and evaluation of dense two-frame stereo correspondence algorithms, International Journal of Computer Vision 47(1-3), 2002, 7-42
    locator: the whole paper (the four steps of matching cost, aggregation, optimization and refinement, the taxonomy of methods, and the evaluation by the percentage of bad pixels)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 12, Depth estimation (dense correspondence, local methods and global optimization)
  - paper: "Yuri Boykov, Olga Veksler and Ramin Zabih, Fast approximate energy minimization via graph cuts, IEEE Transactions on Pattern Analysis and Machine Intelligence 23(11), 2001"
    locator: the proof that minimizing the energy with the Potts smoothness term is NP-hard, and the expansion and swap moves
---

Stereo matching is the problem of finding, for each pixel of one image of a rectified stereo pair, the [disparity](/disparity/) of the pixel in the other image that sees the same scene point. After [rectification](/stereo-rectification/) the match lies in the same row, so the search is one dimensional, over a range of $D$ disparities. The result is a dense disparity map, which [depth from disparity](/depth-from-disparity/) turns into depths. The problem is hard because many pixels look alike (textureless areas, repeated patterns), because some pixels have no match at all (occlusions), and because the two cameras see a surface under slightly different light and shape.

## In plain words

You have two photos taken side by side, already lined up so that each row of one photo shows the same strip of the scene as the same row of the other. For each pixel of the left photo, find where the same spot of the scene is in the right photo. It is somewhere to the left in the same row, and the distance is the disparity. Comparing single pixels does not work well, because many pixels have the same color. So every method compares small areas, or asks that neighbors have similar disparities, or both. Some pixels see a part of the scene that the other camera cannot see, and they have no correct answer.

## Definition

**Input.** Two rectified images $I_L$ and $I_R$ of $W \times H$ pixels, with the right camera at the baseline $b > 0$ along $+X$ of the left one, and a disparity range $0 \le d < D$ (or $d_{\min} \le d \le d_{\max}$). Pixel $(u, v)$ is in column $u$ and row $v$.

**Output.** A disparity map $d_L$ that gives each pixel $(u, v)$ of the left image a disparity $d_L(u, v)$, so that $(u, v)$ in $I_L$ and $(u - d_L(u, v), v)$ in $I_R$ see the same scene point. The map can also mark pixels as invalid. Disparities are integers or, after refinement, real numbers.

**What counts as correct.** The problem is an estimation problem: the true disparity is a property of the scene, and the images do not determine it. Benchmarks compare $d_L$ with a ground truth map and count the bad pixels, the pixels with $\lvert d_L - d_{\text{true}} \rvert > \delta$ for a threshold $\delta$ such as 1 pixel, in all areas, in textureless areas and near depth edges (Scharstein and Szeliski 2002).

**Energy form.** Most methods choose $d$ to make an energy small:

$$E(d) = \sum_{p} C(p, d_p) + \sum_{(p, q) \in \mathcal N} V(d_p, d_q),$$

where $C(p, d)$ is the [matching cost](/stereo-matching-cost/) of pixel $p$ at disparity $d$, stored in a [cost volume](/cost-volume/), $\mathcal N$ is the set of neighbor pairs, and $V$ is a smoothness term such as the Potts term $V = \lambda [d_p \ne d_q]$ or a truncated linear term. Local methods drop the second sum and use an [aggregated](/cost-aggregation/) cost in the first. The energy is a model, not the definition of correct: the minimum of $E$ is not always the true map.

## Variants

- **Sparse matching.** Match only distinctive points, as in feature matching. Dense matching, the subject here, gives every pixel a value or marks it invalid.
- **Integer or subpixel.** Integer disparities, then [subpixel refinement](/subpixel-disparity-refinement/) to a fraction of a pixel.
- **With occlusions.** Mark each pixel as matched or occluded, often by a [left-right consistency check](/left-right-consistency-check/) or inside the energy.
- **Unrectified or many views.** Search along epipolar lines that are not rows, or use many cameras: [plane sweep stereo](/plane-sweep-stereo/) and [multi-view stereo](/multi-view-stereo/).
- **Motion.** Without rectification and with moving objects, the match is a 2D vector: [optical flow](/optical-flow/), and with depth, [scene flow](/scene-flow/).

## Examples

**One row.** Let the right row be $I_R = (10, 50, 90, 10, 10, 10)$ and the left row its shift by one pixel, $I_L = (10, 10, 50, 90, 10, 10)$, so the true disparity is 1 everywhere. With the cost $|I_L(u) - I_R(u - d)|$ and $0 \le d \le 2$:

- At $u = 2$ ($I_L = 50$) the costs for $d = 0, 1, 2$ are $40, 0, 40$. The match is clear: $d = 1$.
- At $u = 3$ ($I_L = 90$) the costs are $80, 0, 40$: again $d = 1$.
- At $u = 5$ ($I_L = 10$) the costs are $0, 0, 0$, because $I_R$ is $10$ at columns 5, 4 and 3. Each disparity fits, and one pixel cannot decide.
- At $u = 4$ the costs of the pixel alone are $0, 0, 80$, a tie between $d = 0$ and $d = 1$. The window of columns 3 to 5 gives the sums $80, 0, 120$, because it contains the textured pixel at $u = 3$, and the tie is gone. At $u = 5$ the window of columns 4 and 5 still gives $0, 0, 80$: it is too far from the texture.

This is the problem of textureless areas: the answer must come from neighbors, by a larger window, by aggregation or by a smoothness term.

**Occlusion.** In the left image, the background just left of a near object is hidden from the right camera. Those pixels have no true match, and any method that gives every pixel a disparity is wrong there.

## Known algorithms

The taxonomy of Scharstein and Szeliski (2002) splits a stereo method into four steps: matching cost, aggregation, disparity computation or optimization, and refinement. The pages of this area follow it.

| method | step it is about | time | model |
|---|---|---|---|
| [block matching](/block-matching-stereo/) | box aggregation and winner-takes-all | $\Theta(W H D)$ | local |
| [census transform](/census-transform/) | a matching cost robust to light changes | $\Theta(W H D)$ for the costs | local |
| [adaptive support weights](/adaptive-support-weights/) | aggregation with edge-aware weights | $O(W H D r^2)$ | local |
| guided filter aggregation (Hosni et al. 2013), see [cost aggregation](/cost-aggregation/) | edge-aware aggregation in time independent of $r$ | $\Theta(W H D)$ | local |
| [scanline dynamic programming](/scanline-dynamic-programming-stereo/) | exact minimum of $E$ on each row alone | $O(W D)$ per row for simple $V$ | global on a row |
| [semi-global matching](/semi-global-matching/) | sums of 1D minimizations along 8 or 16 paths | $\Theta(W H D)$ per path | semi-global |
| [graph cut stereo](/graph-cut-stereo/), [alpha expansion](/alpha-expansion/) | approximate minimum of $E$ on the 2D grid | a min cut per move | global |
| [belief propagation](/belief-propagation/) | approximate minimum by messages on the grid | $O(W H D)$ per iteration with fast messages | global |
| [PatchMatch stereo](/patchmatch-stereo/) | random search over slanted planes | independent of $D$ | local with propagation |

## Bounds

- **Output size.** Any method writes $W H$ values, so it takes $\Omega(W H)$ time. A method that looks at every disparity of every pixel, as a full cost volume does, takes $\Omega(W H D)$. PatchMatch avoids the factor $D$ by sampling.
- **Local methods.** With box aggregation by running sums or an [integral image](/integral-image/), winner-takes-all takes $\Theta(W H D)$ time, independent of the window size.
- **One row.** The energy $E$ restricted to one row is a chain, and dynamic programming finds its exact minimum in $O(W D^2)$ time, or $O(W D)$ for the Potts and linear terms.
- **The full grid.** Minimizing $E$ on the 2D grid with the Potts term is NP-hard (Boykov, Veksler and Zabih 2001), by a reduction from multiway cut. For a convex $V$ of $d_p - d_q$, an exact minimum is computable by one minimum cut on a graph of $W H D$ nodes (Ishikawa 2003). In practice the methods above are approximations, and their quality is measured on benchmarks, not proved.

## Reductions

- **To labeling.** Stereo matching with the energy $E$ is a labeling problem on a [Markov random field](/markov-random-field/) with $D$ labels per pixel. Any MRF method applies, which is why graph cuts and belief propagation entered stereo.
- **From general camera pairs.** An unrectified pair reduces to this problem by [stereo rectification](/stereo-rectification/), as long as the epipoles are outside the images.
- **To optical flow.** Stereo matching is optical flow with the vertical component fixed at zero and the horizontal one at most zero. A flow method can solve it, with more work and less accuracy.
- **To depth.** A disparity map gives a depth map by $Z = f b / d$, see [depth from disparity](/depth-from-disparity/).

## Applications

Depth for robots, cars and drones from a pair of cameras; 3D models of buildings and terrain from aerial images; depth for view synthesis and refocusing in phone cameras; and the first step of [depth map fusion](/depth-map-fusion/) in 3D scanning.

## References
