---
tag: 85H8BD
kind: algorithm
slug: mean-shift-tracking
name: Mean shift tracking
aliases:
- kernel-based object tracking
- Comaniciu-Ramesh-Meer tracker
area: computer-vision/visual-tracking
level: core
summary: Track a target by moving its window up the Bhattacharyya similarity of kernel-weighted color histograms with mean shift steps.
solves: [visual-object-tracking]
model: real-ram
complexity:
  vars: {m: the number of pixels in the window, B: the number of histogram bins, k: the iteration limit per frame, j: the halving limit per iteration}
  time: {worst: Θ(k (j + 1) (m + B)), average: Θ(k (j + 1) (m + B)), best: Θ(m + B)}
  space: {extra: Θ(m + B)}
properties: {deterministic: true, exact: false, local: true, iterative: true, online: true}
history:
  year: 2000
  people: [Dorin Comaniciu, Visvanathan Ramesh, Peter Meer]
  note: Comaniciu, Ramesh and Meer used the mean shift procedure to maximize the Bhattacharyya coefficient between a target histogram and a candidate histogram (CVPR 2000), and gave the full kernel-based framework in 2003.
prereqs: [mean-shift, kernel-density-estimation, visual-object-tracking]
see_also: [camshift, mean-shift-segmentation, correlation-filter-tracking, condensation-algorithm, kalman-filter, tracking-by-detection, kanade-lucas-tomasi-tracker, histogram-equalization]
sources:
  - paper: doi:10.1109/TPAMI.2003.1195991
    title: Dorin Comaniciu, Visvanathan Ramesh and Peter Meer, Kernel-based object tracking, IEEE Transactions on Pattern Analysis and Machine Intelligence 25(5), 2003, 564 to 577
    locator: the whole paper (the kernel-weighted histograms, the Bhattacharyya coefficient, its linearization, the weights, the Epanechnikov step and the halving test)
  - paper: doi:10.1109/CVPR.2000.854761
    title: Dorin Comaniciu, Visvanathan Ramesh and Peter Meer, Real-time tracking of non-rigid objects using mean shift, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2000, volume 2, 142 to 149
    locator: the whole paper (the first form of the tracker)
  - paper: doi:10.1109/34.1000236
    title: Dorin Comaniciu and Peter Meer, Mean shift, a robust approach toward feature space analysis, IEEE Transactions on Pattern Analysis and Machine Intelligence 24(5), 2002, 603 to 619
    locator: the whole paper (the mean shift procedure and its convergence argument)
  - paper: doi:10.1016/j.patcog.2006.10.016
    title: Xiangru Li, Zhanyi Hu and Fuchao Wu, A note on the convergence of the mean shift, Pattern Recognition 40(6), 2007, 1756 to 1762
    locator: the whole paper (the gap in the earlier convergence proof)
---

Mean shift tracking follows a target through a video by its colors. The target is described by a histogram of the colors in an elliptical window, where pixels near the center count more than pixels near the border. In each new frame the tracker starts at the old position and moves the window to make the histogram under it as similar as possible to the target histogram, with the Bhattacharyya coefficient as the measure of similarity. Each move is one step of the [mean shift](/mean-shift/) procedure: the new center is a weighted mean of the pixel positions in the window, with large weights on pixels whose color is more frequent in the target than in the current window. The method was given by Comaniciu, Ramesh and Meer in 2000 and 2003. It is a local search for one [visual object tracking](/visual-object-tracking/) problem, with no training and a few iterations per frame.

## In plain words

We know what colors the target has, for example a red shirt with a bit of blue. In the next picture we put a window where the target was. The window shows some red, some blue and some background. Pixels with a color that the target has more of than the window has get a strong vote, and pixels with background colors get almost no vote. The new window center is the average position of the votes. Because the target has moved, the strong votes sit on the side where it went, so the window moves that way. We repeat until the window stops moving. The color mix does not care about the shape of the target, so it works for a person who bends or turns, but it cannot tell two things of the same colors apart.

## The problem

Images are [digital images](/digital-image/) indexed $I[v][u]$, with the center of pixel $(u, v)$ at the point $(u, v)$. Each pixel has a bin $b(x) \in \{1, \ldots, B\}$, for example the gray value divided into $B$ equal ranges, or a quantized color. A window has a center $y$ and half axes $h = (h_u, h_v)$; for a pixel $x$ let

$$
r(x; y) = \Big( \frac{x_u - y_u}{h_u} \Big)^2 + \Big( \frac{x_v - y_v}{h_v} \Big)^2, \qquad k(r) = \max(1 - r, 0),
$$

where $k$ is the profile of the Epanechnikov kernel. The candidate histogram at $y$ is

$$
p_u(y) = C \sum_{x : r(x; y) < 1} k(r(x; y)) \, [b(x) = u], \qquad C = \Big( \sum_{x : r(x; y) < 1} k(r(x; y)) \Big)^{-1},
$$

so $\sum_u p_u(y) = 1$, and it is a [kernel density estimate](/kernel-density-estimation/) of the colors in the window. The target model $q$ is the same histogram computed in the first frame at the given window. The similarity is the Bhattacharyya coefficient

$$
\rho(y) = \sum_{u=1}^B \sqrt{p_u(y)\, q_u},
$$

which is 1 when $p(y) = q$ and lies in $[0, 1]$ by the Cauchy-Schwarz inequality. In each frame the task is to find a local maximum of $\rho$ near the previous center.

A first-order expansion of $\sqrt{p_u}$ around $p_u(y_0)$, with $C$ held fixed, gives

$$
\rho(y) \approx \tfrac12 \rho(y_0) + \tfrac{C}{2} \sum_i w_i\, k(r(x_i; y)), \qquad w_i = \sqrt{\frac{q_{b(x_i)}}{p_{b(x_i)}(y_0)}} .
$$

The second term is a weighted kernel density of pixel positions, and the mean shift step climbs it.

## The algorithm

```pseudo id=main
MEAN-SHIFT-STEP(I, q, y₀, h, ε, k_max, j_max)
L1   ρ₀ ← Σ_u √(p_u(y₀) q_u)
L2   repeat up to k_max times
L3       for each pixel xᵢ with r(xᵢ; y₀) < 1 do wᵢ ← √(q_{b(xᵢ)} / p_{b(xᵢ)}(y₀))
L4       y₁ ← Σᵢ wᵢ xᵢ / Σᵢ wᵢ                                  ▷ the Epanechnikov mean shift step
L5       ρ₁ ← Σ_u √(p_u(y₁) q_u)
L6       while ρ₁ < ρ₀ and fewer than j_max halvings are done do
L7           y₁ ← (y₀ + y₁) / 2;  ρ₁ ← Σ_u √(p_u(y₁) q_u)
L8       if ρ₁ < ρ₀ then return y₀
L9       if |y₁ - y₀| < ε then return y₁
L10      y₀ ← y₁
L11  return y₀
```

The tracker computes $q$ once, at the given window in the first frame, and calls MEAN-SHIFT-STEP once per frame, starting from the center found in the frame before. With the Epanechnikov profile, the derivative $-k'$ is 1 inside the window, so the mean shift step of line L4 is a plain weighted mean of the pixel positions; other profiles weight each pixel also by $-k'(r)$. Line L6 is the test of Comaniciu, Ramesh and Meer: the step climbs the linearized coefficient, and if the true coefficient went down, the step is halved. The cap $j_{\max}$ and the return at line L8 are added so that the procedure always stops.

## Example

**The weights.** Take two bins, bright and dark, a target model $q = (0.75, 0.25)$ and a window with $p(y_0) = (0.5, 0.5)$. Then $\rho(y_0) = \sqrt{0.375} + \sqrt{0.125} = 0.9659$. A bright pixel gets the weight $\sqrt{0.75 / 0.5} = 1.2247$ and a dark pixel $\sqrt{0.25 / 0.5} = 0.7071$, so the weighted mean of line L4 moves toward the bright pixels. A bin that the target does not have gets the weight 0.

**One frame.** The frames are $64 \times 64$ with gray noise from 0 to 95. The target is an ellipse with half axes 8 and 6; its left half has values from 200 to 239, its right half values from 130 to 159, and the noise is drawn again in each frame (seed 4). The window has $h = (8, 6)$, there are $B = 16$ bins of width 16, and $\varepsilon = 0.1$. The model $q$ has five nonzero bins: 0.278 and 0.275 for the bins of 128 to 159, and 0.118, 0.174 and 0.155 for the bins of 192 to 239. In frame 1 the target has moved from $(16, 20)$ to $(18.5, 21.5)$. At the old center the window still holds noise, and the background bins get weight 0, while the bins of 128 to 159 get the weights 1.447 and 1.570 because they are rarer in the window than in the model. The iterations are:

| Step | Center $y_1$ | $\rho(y_1)$ | Move | Distance to truth |
|---|---|---|---|---|
| start | $(16, 20)$ | 0.8926 | | 2.915 |
| 1 | $(17.9872, 20.5816)$ | 0.9803 | 2.071 | 1.052 |
| 2 | $(18.4890, 21.0929)$ | 0.9949 | 0.716 | 0.407 |
| 3 | $(18.6726, 21.3436)$ | 0.9977 | 0.311 | 0.233 |
| 4 | $(18.6176, 21.4553)$ | 0.9980 | 0.125 | 0.126 |

The fifth step lands on the same point up to rounding, and the loop stops. The halving of line L6 was not needed here. Over 12 frames with a motion of $(2.5, 1.5)$ per frame, the largest error is 0.162 pixel and the smallest coefficient is 0.990.

**The reach.** A step can only see pixels inside the window, so the target must overlap the window at the old position. With the target moved 6 or 14 pixels to the right, the tracker finds it within 0.08 pixel. Moved 18 pixels, the ellipse no longer overlaps the window of half width 8, every weight is 0, and the tracker stays at the old position with $\rho = 0$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows four facts.

- **Theorem: one step raises the weighted density.** For fixed weights $w_i \ge 0$ and the Epanechnikov profile, the weighted mean $y_1$ of the points in the window at $y_0$ satisfies $f(y_1) - f(y_0) \ge W |y_1 - y_0|_h^2$, where $f(y) = \sum_i w_i k(r(x_i; y))$ and $W$ is the weight inside the window. The proof uses only the convexity of $k$.
- **Theorem: finite stopping with fixed weights.** Repeating the step with fixed weights reaches a fixed point after finitely many steps, because every iterate is the mean of a subset of the points and $f$ strictly increases.
- **Heuristic: the step climbs a surrogate.** The tracker step climbs the linearization of $\rho$ shown above, not $\rho$ itself. The normalizer $C$ changes with $y$ on a pixel grid and the weights change at every iteration, so $\rho$ can go down. That is why line L6 exists.
- **Theorem: the accepted coefficients never decrease, and the procedure stops** after at most $k_{\max} (j_{\max} + 1)$ histogram evaluations. This follows from lines L6 to L9.

The convergence of the general mean shift sequence of points is a different question. Comaniciu and Meer (2002) gave a proof, and Li, Hu and Wu (2007) showed that the proof has a gap. Nothing here claims that the tracker finds the true target; the coefficient is a similarity score, and a background patch with the same colors scores as well.

## Complexity

One iteration reads the $m$ pixels of the window for the weights and the step, and $m$ more pixels for the new histogram, plus $O(B)$ for the coefficient. Each halving costs one more histogram. So one frame costs $\Theta(k (j + 1)(m + B))$ in the worst case and $\Theta(m + B)$ when the first step is already below $\varepsilon$. The extra space is $\Theta(B)$ for the histograms, plus $\Theta(m)$ if the window pixels are stored. The cost does not depend on the size of the image, only on the window, which is why the method ran in real time on the computers of 2000.

## Properties

- **Local.** It finds a local maximum near the start. The target must overlap the window of the old position, as the reach example shows.
- **Shape-free.** The histogram ignores where the colors are inside the window, so bending, rotation and partial deformation change $q$ little.
- **Sensitive to similar colors.** A background region with the target's colors is a second maximum of $\rho$.
- **Fixed scale.** The plain method keeps $h$ fixed; a target that grows or shrinks needs a scale rule (see the variants).
- **Deterministic and training-free.** There is nothing to learn beyond the first histogram.

## Variants and improvements

- **Scale search.** Comaniciu, Ramesh and Meer run the search with a few window sizes around the current one and keep the size with the best coefficient, then smooth the size over time.
- **Background-weighted histogram.** Lower the model weight of colors that are frequent in a ring around the target, so that the background has less pull.
- **[CAMShift](/camshift/).** Replace the coefficient by a back-projected probability image and adapt the window size and orientation from the moments of that image at each frame.
- **Prediction.** Start the search at the position that a [Kalman filter](/kalman-filter/) predicts, so that faster targets stay inside the reach.
- **Scale space.** Collins (2003) ran mean shift in a joint space of position and scale.
- **Other kernels and features.** A Gaussian profile gives a weighted step with weights $-k'(r)$, and the histogram can be built from color, texture or gradient orientation.

## When to use it

Use mean shift tracking when the target has a distinctive color distribution, the motion between frames is smaller than the window, and you need a very cheap tracker with no training, for example for faces, hands or colored objects in a fixed scene. Do not use it when the background has the same colors, the target is gray and textured (use [correlation filters](/correlation-filter-tracking/) or [KLT](/kanade-lucas-tomasi-tracker/) points), or the scale changes a lot.

## Pitfalls

- **Bins with $p_u(y_0) = 0$.** The weight $\sqrt{q_u / p_u(y_0)}$ is only needed for bins that occur in the window, and those have $p_u(y_0) > 0$ because every pixel inside the window has positive kernel weight. Compute $p$ from the same window as the weights, or the division fails.
- **No overlap.** If every weight in the window is 0, there is no step. Return the old position and report the low coefficient, as the reach example does.
- **Too many bins.** With many bins and a small window, each bin holds a few pixels and the histogram is noisy. With too few bins, target and background share bins.
- **An endless halving loop.** Without a cap, line L6 can halve forever when rounding keeps $\rho_1$ a little below $\rho_0$. Cap it and keep the old point.
- **Model drift.** Updating $q$ at every frame lets the background into the model over time. Keep the first model, or update it slowly and only when the coefficient is high.

## Implementations

## History

The mean shift procedure goes back to Fukunaga and Hostetler (1975), who used it to find the modes of a density estimate, and Cheng (1995) generalized it. Comaniciu and Meer applied it to segmentation and clustering in image space, and Comaniciu, Ramesh and Meer (2000) used it for tracking: they wrote the Bhattacharyya coefficient between a target histogram and a candidate histogram, linearized it, and showed that the mean shift step on a weighted density climbs the linearization. Their 2003 paper "Kernel-based object tracking" gave the full framework, with the Epanechnikov kernel, the halving test, scale adaptation and the background-weighted histogram. Bradski (1998) had used mean shift on a color probability image for face tracking in [CAMShift](/camshift/). Li, Hu and Wu (2007) pointed out a gap in the 2002 convergence proof of mean shift.

## References
