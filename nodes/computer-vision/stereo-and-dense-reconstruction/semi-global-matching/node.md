---
tag: NJ87X5
kind: algorithm
slug: semi-global-matching
name: Semi-global matching
aliases:
- SGM
- Hirschmuller semi-global matching
area: computer-vision/stereo-and-dense-reconstruction
level: core
summary: Sum, over 8 or 16 directions, 1D dynamic programs on the cost volume with small and large jump penalties, then take the best disparity per pixel.
solves: [stereo-matching]
model: word-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, D: the number of disparities, R: the number of path directions}
  time: {worst: Θ(W H D R), average: Θ(W H D R), best: Θ(W H D R)}
  space: {extra: Θ(W H D)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2005
  people: [Heiko Hirschmüller]
  note: Hirschmüller presented semi-global matching with a mutual information cost at CVPR 2005 and gave the full method, with the subtraction that bounds the path costs, in TPAMI in 2008.
prereqs: [stereo-matching, cost-volume, scanline-dynamic-programming-stereo]
see_also: [stereo-matching-cost, census-transform, cost-aggregation, left-right-consistency-check, subpixel-disparity-refinement, graph-cut-stereo, viterbi-algorithm, patchmatch-stereo]
sources:
  - paper: doi:10.1109/TPAMI.2007.1166
    title: Heiko Hirschmüller, Stereo processing by semiglobal matching and mutual information, IEEE Transactions on Pattern Analysis and Machine Intelligence 30(2), 2008, 328-341
    locator: Equation 11 (the energy with the penalties P1 and P2), Equation 12 (the recursion of the path cost), Equation 13 (the same recursion with the minimum of the previous pixel subtracted), the bound L <= Cmax + P2, the advice that the number of paths must be at least 8 and should be 16, and the adaptation of P2 to the intensity gradient
  - paper: doi:10.1109/CVPR.2005.56
    title: Heiko Hirschmüller, Accurate and efficient stereo processing by semi-global matching and mutual information, IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR 2005), 807-814
    locator: the first presentation of the method
  - paper: doi:10.1023/A:1014573219977
    title: Daniel Scharstein and Richard Szeliski, A taxonomy and evaluation of dense two-frame stereo correspondence algorithms, International Journal of Computer Vision 47(1-3), 2002, 7-42
    locator: the scanline optimization (SO) method, a single horizontal pass of the same kind of recursion
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 12, Depth estimation (semi-global matching among the global and semi-global methods)
---

Semi-global matching (SGM) is a method for dense [stereo matching](/stereo-matching/) that sits between local and global methods. It starts from a [cost volume](/cost-volume/) $C(p, d)$, the cost of giving pixel $p$ the [disparity](/disparity/) $d$. Along a straight line through the image, a dynamic program finds the best disparity sequence under a smoothness model with two penalties: a small $P_1$ for a change of one disparity step, and a large $P_2$ for any larger jump. SGM runs this program along 8 or 16 directions that end at each pixel, adds the results, and gives each pixel the disparity of least sum. Each direction costs $\Theta(W H D)$ and the work is regular, so SGM is fast and maps well to hardware. It is one of the most used stereo methods in practice, in robotics, cars and aerial mapping, and it is far less streaky than [dynamic programming on single scanlines](/scanline-dynamic-programming-stereo/).

## In plain words

For each pixel we have a cost for every possible depth. Choosing the cheapest depth for each pixel alone gives noisy results. So we want neighboring pixels to agree, but we also want to allow real depth edges. Imagine walking along a line toward a pixel. As you walk, you keep the best total cost for each depth, where a small change of depth from one pixel to the next costs a little and a big jump costs more. Do this from 8 or 16 directions, add the totals at each pixel, and pick the depth with the smallest sum. Each direction is cheap, and together they smooth the result in every direction.

## The problem

**Input.** A cost volume $C(p, d) \ge 0$ for the pixels $p$ of a $W \times H$ image and the disparities $d \in \{0, \dots, D - 1\}$, penalties $0 \le P_1 \le P_2$, and a set $R$ of directions. The cost comes from a [matching cost](/stereo-matching-cost/): Hirschmüller used mutual information, and the [census transform](/census-transform/) is a common choice.

**Output.** A disparity map. Hirschmüller (2008) defines the energy

$$E(f) = \sum_p C(p, f_p) + \sum_{\{p,q\} \in \mathcal{N}} \Big(P_1 [\,|f_p - f_q| = 1\,] + P_2 [\,|f_p - f_q| > 1\,]\Big),$$

whose exact minimum over a 2D grid is NP-hard to find in general. SGM does not minimize it. It minimizes it exactly along each 1D path and combines the paths.

## The algorithm

For a direction $r$, the path cost of pixel $p$ is

$$L_r(p, d) = C(p, d) + \min\big(L_r(p - r, d),\ L_r(p - r, d - 1) + P_1,\ L_r(p - r, d + 1) + P_1,\ \min_k L_r(p - r, k) + P_2\big) - \min_k L_r(p - r, k),$$

with $L_r(p, d) = C(p, d)$ when $p - r$ is outside the image.

```pseudo id=main
SGM(C, P1, P2, R)
L1  S(p, d) ← 0 for all pixels p and disparities d
L2  for each direction r in R do
L3      for each pixel p, in an order that visits p - r before p do
L4          if p - r is outside the image then L_r(p, d) ← C(p, d) for all d
L5          else m ← min over k of L_r(p - r, k)
L6              for each d: L_r(p, d) ← C(p, d) + min(L_r(p - r, d), L_r(p - r, d ± 1) + P1, m + P2) - m
L7          S(p, d) ← S(p, d) + L_r(p, d) for all d
L8  for each pixel p: f_p ← the least d with the least S(p, d)
L9  return f
```

The 8 directions are the horizontal, vertical and diagonal steps in both senses; the 16 directions add the eight knight moves such as $(2, 1)$. The subtraction of $m$ in line L6 does not change which $d$ is best along the path, but it keeps the values bounded.

## Example

A row of three pixels with $D = 3$, $P_1 = 2$, $P_2 = 6$ and the costs below. The middle pixel is noisy: alone, its best disparity is 1, while its neighbors clearly want 0.

| pixel | $C(p, \cdot)$ | $L_{\rightarrow}$ | $L_{\leftarrow}$ | $S$ | winner |
|---|---|---|---|---|---|
| 0 | (0, 5, 9) | (0, 5, 9) | (0, 6, 12) | (0, 11, 21) | 0 |
| 1 | (4, 3, 9) | (4, 5, 15) | (4, 5, 15) | (8, 10, 30) | 0 |
| 2 | (0, 5, 9) | (0, 6, 12) | (0, 5, 9) | (0, 11, 21) | 0 |

From left to right at pixel 1, with $L_{\rightarrow}(0) = (0, 5, 9)$ and $m = 0$: for $d = 0$ the best is $\min(0, 5 + 2, 0 + 6) = 0$, so $L = 4 + 0$; for $d = 1$ it is $\min(5, 0 + 2, 9 + 2, 6) = 2$, so $L = 3 + 2 = 5$; for $d = 2$ it is $\min(9, 5 + 2, 6) = 6$, so $L = 15$. At pixel 2, $m = 4$ is subtracted: $L_{\rightarrow}(2, 1) = 5 + \min(5, 4 + 2, 15 + 2, 4 + 6) - 4 = 6$. The sum $S$ picks disparity 0 at pixel 1, where winner-takes-all on $C$ alone picks 1.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). SGM is not exact for the 2D energy; what can be proved is that each path cost is exact for its 1D problem. Without the subtraction, the recursion is the [Viterbi](/viterbi-algorithm/) recursion for the chain of pixels along the ray: the four candidates of line L6 are exactly the least value of $L_r(p - r, k) + V(k, d)$, with $V$ equal to 0, $P_1$ or $P_2$. The subtraction removes a constant from all $d$ at each pixel, and the constants add up along the ray, so $L_r(p, d)$ equals the least chain energy of the ray ending at $p$ with disparity $d$, minus a number that does not depend on $d$. Each step adds a value between 0 and $P_2$ to $C(p, d)$, which gives the bound $C(p, d) \le L_r(p, d) \le C_{\max} + P_2$.

## Complexity

The model is the word RAM with integer costs.

- **Time.** Each direction does $O(D)$ work per pixel, so $\Theta(W H D)$ per direction and $\Theta(W H D R)$ in total. The time does not depend on the data.
- **Space.** $\Theta(W H D)$ for $S$, plus the cost volume. A direction needs only the previous pixel of each path, so the path costs of one direction take $\Theta(W D)$ when the image is traversed row by row.

## Properties

- **Not exact.** The result is not the minimum of the 2D energy, and no bound relates its energy to the minimum.
- **Bounded values.** With the subtraction, $0 \le L_r \le C_{\max} + P_2$, so path costs fit in small integers.
- **Regular and parallel.** All pixels on the same front of a direction are independent, which suits SIMD, GPUs and FPGAs.
- **Edges.** A small $P_1$ allows slanted surfaces, and a large $P_2$ prevents spurious jumps but still allows real depth edges.
- **Direction artifacts.** With few directions, errors spread along the paths and show as streaks; Hirschmüller advises at least 8 directions and suggests 16.

## Variants and improvements

- **Adaptive $P_2$.** Hirschmüller (2008) divides $P_2$ by the intensity difference of the neighbors along the path, $P_2 = P_2' / |I_p - I_{p-r}|$, keeping $P_2 \ge P_1$, so that jumps are cheaper at image edges where depth edges are likely.
- **Post-processing.** A [left-right consistency check](/left-right-consistency-check/) marks occlusions and mismatches, a median filter removes small errors, and [subpixel refinement](/subpixel-disparity-refinement/) fits a parabola to $S$ around the winner.
- **Other costs.** Mutual information in the original, and the [census transform](/census-transform/) in many later systems.
- **Fewer directions.** The directions that point forward in the scan order can all be computed in one pass over the image. Using only those saves memory and time, at some loss of quality.
- **Scanline optimization.** One horizontal direction alone is the SO method of Scharstein and Szeliski (2002).

## When to use it

Use SGM when you need dense depth from a rectified pair at high speed and good quality, for example in robotics, cars or aerial mapping. It is a strong default before learned methods. Use [graph cut stereo](/graph-cut-stereo/) when you need a global minimum of an energy with occlusions and can pay more time, and [block matching](/block-matching-stereo/) when speed matters more than quality.

## Pitfalls

- **Forgetting the subtraction.** Without it, the values grow along the path and overflow small integers. The result is the same in exact arithmetic, but not in 16-bit code.
- **$P_2 < P_1$.** Then a jump of one costs more than a large jump, and the model no longer makes sense. Keep $P_2 \ge P_1$, also after adapting $P_2$.
- **Order of traversal.** For each direction, $p - r$ must be computed before $p$. With diagonal and knight directions, choose the order of rows and columns from the signs of the direction.
- **Penalties and cost scale.** $P_1$ and $P_2$ must be on the same scale as the matching cost. After changing the cost function, choose them again.
- **Uniform data costs.** In large areas with no texture, all directions bring the same weak information, and the result can be wrong over the whole area.

## Implementations

## History

Hirschmüller presented semi-global matching at CVPR 2005, with mutual information as the matching cost. The journal version of 2008 gave the energy, the path recursion with the subtraction and its bound, the advice on the number of paths and the adaptive $P_2$. The idea of aggregating 1D programs builds on scanline optimization and on [dynamic programming stereo](/scanline-dynamic-programming-stereo/). SGM became one of the most used stereo methods in practice, and it was implemented in hardware for real time use.

## References
