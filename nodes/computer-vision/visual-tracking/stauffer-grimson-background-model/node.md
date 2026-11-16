---
tag: 193Y4C
kind: algorithm
slug: stauffer-grimson-background-model
name: Adaptive Gaussian mixture background model
aliases:
- Stauffer-Grimson model
- MOG background subtraction
area: computer-vision/visual-tracking
level: core
summary: Model each pixel by a few Gaussians updated online, call the heavy narrow ones background, and mark pixels that fit none of them as foreground.
solves: [background-subtraction]
model: real-ram
complexity:
  vars: {P: the number of pixels in a frame, K: the number of Gaussians per pixel, N: the number of frames}
  time: {worst: O(N P K log K)}
  space: {extra: O(P K)}
properties: {deterministic: true, online: true, iterative: false, exact: false}
history:
  year: 1999
  people: [Chris Stauffer, W. Eric L. Grimson]
  note: "Stauffer and Grimson presented the adaptive mixture model at CVPR 1999 and used it in the tracking system of their TPAMI paper of 2000; earlier systems such as Pfinder used one Gaussian per pixel."
prereqs: [background-subtraction, gaussian-mixture-model, exponential-moving-average]
see_also: [vibe-background-subtraction, background-subtraction, gaussian-mixture-model, expectation-maximization, kernel-density-estimation, stochastic-approximation, mathematical-morphology, connected-component-labeling]
sources:
  - paper: doi:10.1109/CVPR.1999.784637
    title: "Chris Stauffer and W. Eric L. Grimson, Adaptive background mixture models for real-time tracking, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 1999, vol. 2, 246-252"
    locator: "the sections on the online mixture update and on the background model estimate"
  - paper: doi:10.1109/34.868677
    title: "Chris Stauffer and W. Eric L. Grimson, Learning patterns of activity using real-time tracking, IEEE Transactions on Pattern Analysis and Machine Intelligence 22(8), 2000, 747-757"
    locator: "the description of the adaptive background model in the tracking system"
  - paper: doi:10.1109/ICPR.2004.1333992
    title: "Zoran Zivkovic, Improved adaptive Gaussian mixture model for background subtraction, International Conference on Pattern Recognition (ICPR), 2004, vol. 2, 28-31"
    locator: "the whole paper (the number of components chosen per pixel)"
  - paper: doi:10.1109/34.598236
    title: "Christopher R. Wren, Ali Azarbayejani, Trevor Darrell and Alex P. Pentland, Pfinder: real-time tracking of the human body, IEEE Transactions on Pattern Analysis and Machine Intelligence 19(7), 1997, 780-785"
    locator: "the background model with one Gaussian per pixel"
  - paper: doi:10.1016/j.cosrev.2014.04.001
    title: "Thierry Bouwmans, Traditional and recent approaches in background modeling for foreground detection: an overview, Computer Science Review 11, 2014, 31-66"
    locator: "the survey of mixture models and their variants"
---

The adaptive Gaussian mixture background model of Stauffer and Grimson is an online method for [background subtraction](/background-subtraction/). Each [pixel](/pixel/) has its own [mixture](/gaussian-mixture-model/) of $K$ Gaussians over its values, with $K$ from 3 to 5. Each new value updates the mixture with a fixed learning rate. The components with large weight and small variance are taken as the background, because the background is what the pixel shows most of the time and with little change. A value that fits none of them is foreground. The mixture lets one pixel have several background values, such as a leaf and the sky behind it, or a flickering screen. [ViBe](/vibe-background-subtraction/) solves the same problem without a parametric model: it keeps raw past values per pixel and replaces them at random. The page [background subtraction](/background-subtraction/) states the problem and compares the methods.

## In plain words

A fixed camera looks at a scene. Each pixel keeps a short list of the values it usually shows, with a weight for how often it shows each one and a spread for how much that value varies. When a new picture comes, each pixel checks if its value is close to one of the values on its list. If it is, that entry gets more weight and moves a little toward the new value. If not, the pixel replaces its weakest entry with the new value. The entries that are frequent and steady are the background. A pixel is marked as moving when its value fits no background entry. A car that parks for long becomes background after a while.

## The problem

The input is a sequence of gray images of the same size from a fixed camera; a color version uses vectors with a diagonal covariance. The output for each frame is a binary mask, 1 for foreground and 0 for background. The method is online: the mask of frame $t$ depends only on frames $1$ to $t$.

**The model of one pixel.** The pixel holds $K$ components $(w_k, \mu_k, \sigma_k^2)$ with $w_k \ge 0$ and $\sum_k w_k = 1$. The paper models the recent history of the pixel as the mixture density $\sum_k w_k \, \eta(x \mid \mu_k, \sigma_k^2)$, where $\eta$ is the Gaussian density. The parameters are the learning rate $\alpha$, the background fraction $T$, and the variance $v_0$ and weight $w_0$ of a new component.

## The algorithm

```pseudo id=main
SG-PIXEL(x, the components (w_k, μ_k, σ_k²), α, T, v_0, w_0)
L1   order the components by w_k / σ_k, largest first; m ← the first k with |x - μ_k| ≤ 2.5 σ_k, or none
L2   if there is none: replace the last component by (w_0, x, v_0), scale the other weights to sum 1 - w_0, and return foreground
L3   for each k: w_k ← (1 - α) w_k + α [k = m]
L4   ρ ← α η(x | μ_m, σ_m²);  μ_m ← (1 - ρ) μ_m + ρ x;  σ_m² ← (1 - ρ) σ_m² + ρ (x - μ_m)²
L5   order the components again by w_k / σ_k; B ← the smallest b with w_(1) + ... + w_(b) > T
L6   return background if m is one of the first B components, else foreground
```

The paper replaces the least probable component when nothing matches, with the current value as its mean, a high variance and a low weight, and then renormalizes the weights. Line L2 renormalizes so that the new weight is exactly $w_0$, which makes the bounds below exact. The variance update of line L4 uses the new mean. Line L4 uses the factor $\rho = \alpha \eta$ of the paper; many implementations use $\rho = \alpha / w_m$ instead, which learns faster (see the pitfalls). The implementation also keeps $\sigma^2 \ge 4$, so that the density stays finite for a constant pixel. Components that never received a value have weight 0 and match nothing.

The defaults of the implementation are $K = 3$, $\alpha = 0.01$, $T = 0.7$, $v_0 = 900$ (a standard deviation of 30) and $w_0 = 0.05$. They are tuned values for 8-bit gray images, not values from the paper.

## Example

**One pixel.** The pixel has three components, written as $(w, \mu, \sigma)$: $(0.6, 50, 4)$, $(0.3, 120, 10)$ and $(0.1, 200, 30)$. The ratios $w / \sigma$ are $0.15$, $0.03$ and $0.0033$, so that is also the order. With $T = 0.7$, the first weight $0.6$ is not above $T$ and the first two give $0.9$, so $B = 2$: the components around 50 and 120 are the background. Let $\alpha = 0.01$.

- **$x = 126$.** It is not within $2.5 \times 4 = 10$ of 50, but it is within $25$ of 120, so it matches the second component. The weights become $(0.594, 0.307, 0.099)$. The factor is $\rho = 0.01 \times e^{-0.18} / \sqrt{2 \pi \cdot 100} \approx 0.000333$, so the mean moves from 120 to $120 + 6\rho \approx 120.002$. The match is among the first $B$, so the pixel is background.
- **$x = 200$.** It matches the third component, and the weights become $(0.594, 0.297, 0.109)$. The order stays the same, the first two weights still sum to $0.891 > 0.7$, and $B$ stays 2. The third component is not background, so the pixel is foreground.
- **$x = 90$.** It is 40 from 50, 30 from 120 and 110 from 200, outside $10$, $25$ and $75$, so nothing matches. The last component becomes $(0.05, 90, 30)$, and the other weights are scaled to $0.633$ and $0.317$. The pixel is foreground.

**A parked object.** A pixel shows 50 for 200 frames, so one component has weight 1. Then an object stops on it and the pixel shows 200 from then on. In the first frame no component matches, and the new component has weight $w_0 = 0.05$. After $t$ more frames its weight is $1 - 0.95 \times 0.99^t$. It is background as soon as the weight of the old component, $0.95 \times 0.99^t$, is at most $T = 0.7$, which first happens at $t = 31$. The old component still has weight $0.70$ then, so the value 50 is also still background when the object leaves.

**A short video.** A $16 \times 16$ textured background with noise of standard deviation 2 is shown for 35 frames, and then a $6 \times 6$ bright square moves across it. In the 15 frames with the square, all 480 square pixels are foreground and no background pixel is.

## Correctness

The method is a heuristic: nothing proves that the background components are the true background. The proved facts are about the update rules. The proofs are in [proofs/correctness.md](proofs/correctness.md).

- **Theorem: the weights.** After every update the weights are nonnegative and sum to 1.
- **Theorem: the means stay in range.** Every mean is a convex combination of values the pixel has shown, so it stays between their minimum and maximum.
- **Theorem: a heavy component is background.** A component with weight at least $1 - T$ is always among the first $B$, whatever its variance.
- **Theorem: the weight of a matched component.** If one component matches in $t$ frames in a row, its weight is $1 - (1 - w)(1 - \alpha)^t$, where $w$ is its weight before the run. Each weight is an [exponential moving average](/exponential-moving-average/) of its match indicator.
- **Theorem: absorption time.** If a new value creates a component and then matches it in every frame, the pixel is background after at most $\lceil \ln(T / (1 - w_0)) / \ln(1 - \alpha) \rceil$ frames. With $\alpha = 0.01$, $T = 0.7$ and $w_0 = 0.05$ this is 31. This bound is derived on this page, not taken from the paper.
- **Not proved.** The mixture is not a maximum likelihood fit. The update assigns each value to one component, like an online [k-means](/k-means/) step, instead of the soft assignment of [expectation maximization](/expectation-maximization/), and nothing guarantees convergence to a fit of the true distribution.

## Complexity

Let $P$ be the number of pixels, $K$ the number of components per pixel and $N$ the number of frames, in the [real RAM](/real-ram/) model with $\exp$ and square root at unit cost. One pixel update sorts the $K$ components twice and touches each a constant number of times, so it costs $O(K \log K)$, or $O(K)$ with an insertion step that keeps the order. One frame costs $O(P K \log K)$ and a video $O(N P K \log K)$. The model takes $O(P K)$ space. The pixels are independent, so the update is easy to run in parallel.

## Properties

- **Online and per pixel.** Each pixel is handled alone, with no neighbors.
- **Multimodal.** A pixel can have several background values, as long as each has weight; a single Gaussian cannot.
- **Adaptive.** Changes of light and objects that stop become background after a number of frames set by $\alpha$ and $T$.
- **Deterministic.** The output depends only on the input and the parameters.

## Variants and improvements

- **Zivkovic's model.** It chooses the number of components per pixel online and drops components whose weight becomes negative under a prior.
- **Faster learning.** $\rho = \alpha / w_m$ makes a new component learn its mean and variance fast, because its weight is small.
- **Shadows.** In color, a pixel whose color is the background color with less brightness is often a shadow and is not marked as foreground.
- **Post processing.** [Morphological opening](/morphological-opening/) and [connected component labeling](/connected-component-labeling/) remove isolated pixels and group the rest into objects.
- **Nonparametric models.** [Kernel density estimation](/kernel-density-estimation/) over recent values and [ViBe](/vibe-background-subtraction/) avoid the Gaussian form.

## When to use it

Use it for a fixed camera with a background that changes slowly or moves in a repeating way, such as trees, water or flicker, when the mask must be produced in real time and frame by frame. It is a standard baseline. Do not use it for a moving camera, for scenes where objects stop for long and must stay foreground, or when a scene with sudden light changes must not give a full-frame false alarm.

## Pitfalls

- **Slow learning with $\rho = \alpha \eta$.** The density $\eta$ is small, often below 0.05, so $\rho$ is much smaller than $\alpha$. In the short video above the variance of a background component is still about 894 after 50 frames, from $v_0 = 900$. Use $\rho = \alpha / w$ or start with a smaller $v_0$.
- **Absorbed objects.** A person who stands still becomes background after the absorption time, and then shows as foreground "ghost" pixels where the background reappears if the old component was dropped.
- **Variance collapse.** On a pixel with constant value the variance goes to 0, and the smallest noise breaks the match. Keep a floor on the variance.
- **$T$ too small.** With $T$ below the weight of the main component, $B = 1$, and a second background value, such as the sky behind a leaf, is foreground.
- **Mixing the two orders.** The background test uses the order by $w / \sigma$ after the update. Testing against the order before the update, or against weight alone, gives a different mask.

## Implementations

The Python file models gray pixels, with the update of the paper by default and $\rho = \alpha / w$ as an option. The tests compare the background set with its definition by search, check the weight invariant and the closed form of the weights, check the example above, check that the parked object becomes background at exactly frame 31, check that an alternating pixel is background with $K = 3$ and never with $K = 1$, and run the moving square video.

## History

Wren, Azarbayejani, Darrell and Pentland modeled each background pixel by one Gaussian in their Pfinder system of 1997. In 1999, Stauffer and Grimson replaced it by an adaptive mixture of Gaussians per pixel, updated online, so that a pixel could have more than one background value and the model could follow slow changes. They used it in a tracking system that ran in real time and learned patterns of activity, described in their 2000 paper. Zivkovic made the number of components adaptive in 2004. Surveys such as Bouwmans (2014) list the mixture model as one of the most used and extended background models.

## References
