---
tag: SEFHQG
kind: algorithm
slug: condensation-algorithm
name: CONDENSATION algorithm
aliases:
- conditional density propagation
- Isard-Blake tracker
area: computer-vision/visual-tracking
level: core
summary: Track contours in clutter by a particle filter over shape and motion, weighting each sample by image measurements along its contour.
solves: [visual-object-tracking]
model: real-ram
complexity:
  vars: {N: the number of samples, T: the number of frames, d: the dimension of the shape space, M: the number of normals of the contour, L: the reach of the search along a normal in pixels}
  time: {worst: Θ(T N (log N + d² + M L)), average: Θ(T N (log N + d² + M L)), best: Θ(T N (log N + d² + M L))}
  space: {extra: Θ(N d)}
properties: {deterministic: false, exact: false, local: false, iterative: false, online: true}
history:
  year: 1996
  people: [Michael Isard, Andrew Blake]
  note: Isard and Blake presented CONDENSATION at ECCV in 1996 and in the International Journal of Computer Vision in 1998. It tracked curves in dense clutter by propagating a sample set of contours through learned dynamics and an edge-based observation density.
prereqs: [particle-filter, active-contours]
see_also: [kalman-filter, bayes-filter, resampling, importance-sampling, hidden-markov-model, markov-chain, mean-shift-tracking, visual-object-tracking]
sources:
  - paper: doi:10.1023/A:1008078328650
    title: Michael Isard and Andrew Blake, CONDENSATION, conditional density propagation for visual tracking, International Journal of Computer Vision 29(1), 1998, 5 to 28
    locator: Sections 3 to 6 (factored sampling, the algorithm in Figure 6 on page 12, the dynamics of equations 10 to 12, the observation densities of equations 13 to 16 on pages 13 to 15) and Section 7.1 (1000 samples on a cluttered sequence)
  - paper: "Michael Isard and Andrew Blake, Visual tracking by stochastic propagation of conditional density, European Conference on Computer Vision (ECCV), Cambridge, 1996, 343 to 356"
    locator: the whole paper (the first version of the method)
  - paper: doi:10.1049/ip-f-2.1993.0015
    title: Neil J. Gordon, David J. Salmond and Adrian F. M. Smith, Novel approach to nonlinear/non-Gaussian Bayesian state estimation, IEE Proceedings F 140(2), 1993, 107 to 113
    locator: the whole paper (the bootstrap filter, the same sampling scheme developed for target tracking)
---

The CONDENSATION algorithm tracks the outline of an object through a video when the background is full of edges that look like the outline. Instead of one best guess, it keeps a set of $N$ guesses, called samples, each a full contour with its own position, shape and motion, and each with a weight. In each frame it picks samples in proportion to their weights, moves each one by a random motion model, and weights it by how well the edges of the image line up with its contour along short lines normal to the curve. The weighted set approximates the probability density of the contour given all images so far, so it can hold several hypotheses at once and keep a hypothesis alive while the object is hidden. Michael Isard and Andrew Blake published the method in 1996 and 1998. It is a [particle filter](/particle-filter/), the bootstrap filter of Gordon, Salmond and Smith, with a contour state and an edge-based observation density. This page is about those vision parts, and the particle filter page covers the general filter.

## In plain words

Imagine a hundred people each holding a cut-out of the object's outline over a photo of a messy room. Each person places the cut-out somewhere plausible and scores it by how many edges in the photo fall right on its border. For the next photo, the people with high scores get copied more, the low scorers drop out, and everyone nudges their copy a little in the direction the object was moving, plus some random wobble. Then everyone scores again. If two places look equally good, the crowd can split between them until the photos make the answer clear. If the object is hidden, nobody scores well, so the crowd just keeps drifting along with the motion and spreads out until the object reappears.

## The problem

The input is a video and a model of the object: a shape space of contours, a dynamical model and an observation model. The output in each frame is an estimate of the contour, or the whole set of samples, which approximates the conditional density $p(x_t \mid Z_t)$ of the state $x_t$ given the images $Z_t = (z_1, \ldots, z_t)$. This is a solution to the [visual object tracking](/visual-object-tracking/) problem in which the state is a curve.

**Shape space.** A contour is a parametric curve, usually a B-spline $r(s) = (B(s)^{\mathsf T} Q^x, B(s)^{\mathsf T} Q^y)$, $0 \le s \le L$. Its control points are restricted to a low-dimensional space, $(Q^x, Q^y) = W X + \bar Q$, where $X$ has dimension $d$, for example the 6 parameters of planar affine changes of a template $\bar Q$.

**Dynamics.** A second-order autoregressive model in discrete time,

$$
x_t - \bar x = A (x_{t-1} - \bar x) + B w_t, \qquad w_t \sim N(0, I),
$$

with the stacked state $x_t = (X_{t-1}, X_t)$. Isard and Blake learn $A$, $\bar x$ and $B$ from training sequences by maximum likelihood.

**Observations.** Along $M$ normals of the hypothesized contour, an edge detector finds features at signed offsets $\nu$ from the curve. On one normal, if the object is not seen with probability $q$ and the clutter is a Poisson process with density $\lambda$, the observation density is

$$
p(z \mid x) \propto 1 + \frac{1}{\sqrt{2\pi}\, \sigma \alpha} \sum_m \exp\Big( -\frac{\nu_m^2}{2 \sigma^2} \Big), \qquad \alpha = q \lambda,
$$

where $\sigma$ is the standard deviation of a true edge about the curve. The density of the whole contour is the product over the normals. The paper also uses a cheaper form with the nearest feature only,

$$
p(z \mid x) \propto \exp\Big( -\sum_{m=1}^M \frac{1}{2 r M} \min(\nu_1(s_m)^2, \mu^2) \Big),
$$

where $\nu_1(s_m)$ is the offset of the nearest feature on normal $m$ and $\mu$ caps the cost of a missing or far feature.

## The algorithm

```pseudo id=main
STEP(the old set {(s_j, π_j, c_j)} with c_0 = 0 and c_j = c_{j-1} + π_j, the image z_t)
L1   for n ← 1 to N do  r ← a uniform random number in [0, c_N]
L2       j ← the smallest index with c_j ≥ r, by binary subdivision;  s' ← s_j      ▷ select
L3       s_n ← A s' + B w with w a vector of standard normal numbers               ▷ predict
L4       π_n ← p(z_t | x_t = s_n), the product of the densities of the normals      ▷ measure
L5   divide every π_n by their sum
L6   c_0 ← 0;  c_n ← c_{n-1} + π_n for n = 1, ..., N
L7   return the estimate Σ_n π_n s_n and the new set {(s_n, π_n, c_n)}
```

The first set is drawn from a prior density, for example a Gaussian around a hand-placed contour, or the steady state of the dynamics run with no measurements. Lines L1 and L2 are the selection, with replacement, so a heavy sample can be chosen many times and a light one not at all. In line L3 the copies of one sample first move together (the deterministic part $A s'$) and then split (the random part $B w$). Line L7 can report any moment of the set, not only the mean.

## Example

**One normal by hand.** Take $\sigma = 1$ pixel and $\alpha = 0.05$, so the constant in front of the sum is $1 / (\sqrt{2\pi} \cdot 0.05) \approx 7.98$. A normal with no feature has density 1. One feature exactly on the curve gives $1 + 7.98 = 8.98$. One feature 1 pixel away gives $1 + 7.98\, e^{-1/2} \approx 5.84$, and 2 pixels away $1 + 7.98\, e^{-2} \approx 2.08$. A feature far away adds almost nothing, so the density does not punish a missing edge more than the constant level 1: this is what lets a hypothesis survive an occlusion.

**Selection by hand.** With weights $(0.1, 0.2, 0.3, 0.4)$ the cumulative weights are $(0.1, 0.3, 0.6, 1.0)$. The random number $r = 0.45$ selects index 3, the first with $c_j \ge 0.45$. Each index is selected for an interval of $r$ of length equal to its weight. In 20,000 draws the test sees each frequency within 0.012 of its weight.

**Tracking a circle in clutter.** The implementation uses a circle of radius 8 as the contour, so the shape space is the translations ($d = 2$, state $(X_{t-1}, X_t)$, $A$ with damping 1, noise 1 pixel), $M = 16$ normals probed from $-6$ to $6$ pixels, $\sigma = 1$, $\alpha = 0.05$ and $N = 300$ samples. These are this page's choices. The $60 \times 60$ edge maps have 4% of the pixels set at random as clutter, and the circle moves by $(2, 1.5)$ pixels per frame. In frames 5 and 6 the circle is missing. The errors of the weighted mean over frames 1 to 11 are 0.43, 0.22, 0.08, 0.07, then 0.95 and 3.14 while the circle is hidden, then 2.05 when it comes back, then 0.09, 0.38, 0.18 and 0.13 pixel. During the occlusion every sample has density near the clutter level, so the set keeps moving with the velocities of its samples and spreads; when the circle returns, the samples near it get almost all the weight.

**A sharp density.** In a scene with two circles centered at $(20, 30)$ and $(42, 30)$ and no clutter, the log-likelihood is 40.29 at both centers, 33.40 one pixel off, and 12.18 halfway between. A one-pixel error costs a factor near $e^{6.9} \approx 1000$ in weight. Started between two such circles 20 pixels apart, with 400 samples, the set kept both modes only in some runs. In others one mode got all the weight at the first step. With a density this sharp, few samples carry the weight, and the selection can drop a mode by chance. A larger $\sigma$, more samples or a smoother density keep both modes longer.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows these facts.

- **Theorem: selection.** With $r$ uniform on $[0, c_N]$, the smallest $j$ with $c_j \ge r$ is index $k$ with probability $\pi_k / c_N$, and bisection finds it in $O(\log N)$ comparisons.
- **Theorem: one step is factored sampling.** Given the old set, the new samples are independent draws from the predicted prior $q(x) = \sum_j \pi_j p(x \mid s_j)$, and for every bounded $g$ the weighted mean $\sum_n \pi_n g(s_n)$ converges almost surely, as $N \to \infty$, to the posterior mean of $g$ under the prior $q$ and the observation density.
- **Theorem: the dynamics.** The update of line L3 is the second-order autoregressive model. With no noise and damping 1 it keeps a constant velocity.
- **Theorem: the observation density.** The density of one normal follows from the clutter model above, is at least 1 and bounded, and equals 1 when there is no feature. So a frame with no features leaves all weights equal.

The behavior over many frames for a fixed $N$, and whether the tracked contour is the object, are not proved. They depend on the models and on the number of samples, and the experiments of the paper are evidence, not proof.

## Complexity

Selection costs $O(\log N)$ per sample by bisection, prediction $O(d^2)$ for the matrix product, and measurement $O(M L)$ for $M$ normals probed at $2L + 1$ points. Normalization and the cumulative weights cost $O(N)$. A frame costs $\Theta(N (\log N + d^2 + M L))$, and $T$ frames cost $T$ times that. The extra space is $\Theta(N d)$ for the samples and their weights. In practice the measurement dominates. Isard and Blake used $N = 1000$ in their first experiment. The cost of selection can be cut to $O(1)$ per sample with systematic [resampling](/resampling/), which draws one random number for all samples and walks through the cumulative weights once.

## Properties

- **Multimodal.** The set can represent several hypotheses at once, which a [Kalman filter](/kalman-filter/) cannot.
- **Robust to clutter.** The observation density is never 0, so a few missing or false edges do not kill a correct hypothesis.
- **Survives short occlusions.** With no features, the weights stay equal and the samples follow the dynamics.
- **Randomized.** Two runs with different seeds give different sets and slightly different estimates.
- **Fixed cost.** The number of samples is fixed, so the time per frame is bounded and does not depend on the image content.
- **No covariance algebra.** Unlike the Kalman filter, there is no Riccati equation, only sampling and evaluation of the density.

## Variants and improvements

- **ICONDENSATION.** Isard and Blake later combined the contour samples with samples drawn near color blobs found by a low-level detector, by importance sampling, so the tracker can recover from a lost track.
- **Mixed discrete and continuous states.** Add a discrete label, such as the kind of motion, to each sample and switch it by a [Markov chain](/markov-chain/).
- **Partitioned and annealed sampling.** For articulated bodies with many dimensions, sample one part of the state at a time, or anneal the observation density over several layers.
- **Color-based particle filters.** Replace the edge density by the similarity of color histograms, as in the kernel used by [mean-shift tracking](/mean-shift-tracking/).
- **Better proposals.** Draw the predicted samples from a density that already uses the new image, and correct by importance weights.
- **Systematic or residual resampling.** Lower the variance of the selection step and its cost.

## When to use it

Use CONDENSATION, or a particle filter with a contour state, when the background is cluttered, the motion is fast or erratic, and the density of the state can have several peaks. Examples are a hand or a head in front of a busy background, or a leaf among leaves. It needs a shape model and a dynamical model, ideally learned from training data. If the density is close to a single Gaussian, a [Kalman filter](/kalman-filter/) or an [extended Kalman filter](/extended-kalman-filter/) is cheaper and has no sampling noise. For a target described by its appearance instead of its outline, use an appearance tracker such as [mean-shift tracking](/mean-shift-tracking/) or a [correlation filter](/correlation-filter-tracking/).

## Pitfalls

- **Too few samples for the dimension.** The number of samples needed grows quickly with the dimension of the shape space. A 12-dimensional state with a few hundred samples leaves large parts of the density empty.
- **A density that is too sharp.** With a small $\sigma$, one sample takes almost all the weight, the selection copies it, and the set collapses to one point. The example shows a factor of about 1000 per pixel.
- **Underflow.** The product over many normals can underflow. Add logarithms and subtract the largest before taking the exponential, as the implementation does.
- **Weights of zero sum.** If the density can be 0, a frame with no good hypothesis makes all weights 0. The constant 1 of the clutter model avoids this.
- **Dynamics that do not match.** If the true motion is faster than the noise of the model allows, no sample lands near the object, and the tracker loses it with no warning.
- **Reporting only the mean.** With two modes, the mean lies between them, on no object. Report the largest mode as well when the density can be multimodal.

## Implementations

The Python code tracks a circle of fixed radius with the state of the second-order model, on synthetic edge maps. It implements the density of one normal (equation 13 of the paper) and the nearest-feature form (equation 16), the selection by binary subdivision with the module `bisect`, the prediction and the normalization in log space. The tests check the selection against its definition and its frequencies, the densities by hand, the constant density with no features, the constant velocity of the dynamics, the two equal peaks of a two-circle scene, and tracking through clutter and a two-frame occlusion.

## History

Kalman filter trackers for curves, developed by Blake and colleagues in the early 1990s, failed in clutter because a single Gaussian cannot hold two explanations of the edges. In 1996 Michael Isard and Andrew Blake presented CONDENSATION at ECCV, and in 1998 they published the full method in the International Journal of Computer Vision. It applies factored sampling, a method of Grenander and colleagues for single images, to each frame of a sequence. The same scheme was developed at the same time for target tracking and statistics: the bootstrap filter of Gordon, Salmond and Smith (1993) and the Monte Carlo filter of Kitagawa (1996). Isard and Blake extended it to ICONDENSATION in 1998. The method made particle filters common in computer vision, for tracking people, hands and faces, and for robot localization.

## References
