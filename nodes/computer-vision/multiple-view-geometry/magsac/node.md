---
tag: RA0N0V
kind: algorithm
slug: magsac
name: MAGSAC
aliases:
- marginalizing sample consensus
- MAGSAC++
area: computer-vision/multiple-view-geometry
level: research
summary: "RANSAC with no inlier threshold, scoring and refining each model by marginalizing a robust cost over a range of noise scales."
solves: [robust-model-fitting]
model: real-ram
complexity:
  vars: {n: the number of data items, k: "the number of samples drawn, at most a set cap"}
  time: {worst: Θ(k n), average: Θ(k n), best: Θ(k n)}
  space: {extra: Θ(n)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2019
  people: [Daniel Barath, Jiri Matas, Jana Noskova, Maksym Ivashechkin]
  note: "Barath, Matas and Noskova published MAGSAC at CVPR 2019. Barath, Noskova, Ivashechkin and Matas published MAGSAC++, with a closed-form loss and a reweighted least squares step, at CVPR 2020."
prereqs: [ransac, msac, iteratively-reweighted-least-squares]
see_also: [msac, mlesac, lo-ransac, prosac, ransac-iteration-bound, robust-model-fitting, m-estimator, homography-estimation]
sources:
  - paper: doi:10.1109/CVPR.2019.01044
    title: "Daniel Barath, Jiri Matas and Jana Noskova, MAGSAC: marginalizing sample consensus, IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR 2019), arXiv:1803.07469"
    locator: "The definition of sigma-consensus, the marginalization of the model quality over the noise scale, and the termination criterion"
  - paper: "Daniel Barath, Jana Noskova, Maksym Ivashechkin and Jiri Matas, MAGSAC++, a fast, reliable and accurate robust estimator, IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR 2020), arXiv:1912.05909"
    title: "Daniel Barath, Jana Noskova, Maksym Ivashechkin and Jiri Matas, MAGSAC++, a fast, reliable and accurate robust estimator, CVPR 2020"
    locator: "The MAGSAC++ quality function, its weight and loss in terms of incomplete gamma functions, and the iteratively reweighted least squares form of sigma-consensus++"
  - paper: doi:10.1109/TPAMI.2012.257
    title: "Rahul Raguram, Ondrej Chum, Marc Pollefeys, Jiri Matas and Jan-Michael Frahm, USAC: a universal framework for random sample consensus, IEEE Transactions on Pattern Analysis and Machine Intelligence 35(8), 2013, 2022-2038"
    locator: "The framework of sampling, scoring and local optimization that MAGSAC builds on"
---

MAGSAC (marginalizing sample consensus) is a variant of [RANSAC](/ransac/) that needs no inlier threshold. RANSAC and [MSAC](/msac/) need a threshold $T$ that separates inliers from outliers, and the result can change a lot with $T$. MAGSAC asks only for an upper bound $\sigma_{\max}$ on the noise scale. It treats the unknown scale $\sigma$ as uniform on $[0, \sigma_{\max}]$ and averages, or marginalizes, the inlier density over it. This gives a smooth weight $w(r)$ for each residual $r$ and a bounded loss $\rho(r) = \int_0^r x\,w(x)\,dx$. A model is scored by the sum of the losses, and each new best model is refined by a weighted least squares fit with the weights $w$. Barath, Matas and Noskova published MAGSAC in 2019. MAGSAC++ (Barath, Noskova, Ivashechkin and Matas, 2020) gave the loss in closed form and wrote the refinement as [iteratively reweighted least squares](/iteratively-reweighted-least-squares/). This page describes MAGSAC++.

## In plain words

Plain RANSAC needs a fixed distance limit: points closer than the limit count as good, points farther count as bad. If the limit is too tight, good points are lost. If it is too loose, bad points get in. The right limit depends on the noise, which is often not known.

MAGSAC does not choose one limit. It tries all limits up to a maximum and averages the results. A point that is close to the guess counts as good for almost every limit, so it gets a large weight. A point that is a little farther counts as good only for the loose limits, so it gets a smaller weight. A point beyond the largest limit gets no weight. The guess with the smallest total penalty wins, and the weights then pull it to a better fit.

## The problem

The input is data $D = \{x_1, \ldots, x_n\}$, a minimal solver for samples of $s$ items, a residual $r(\theta, x) \ge 0$ with $\nu$ degrees of freedom, a noise bound $\sigma_{\max}$, a confidence $p$ and a cap $k_{\max}$. The model of the noise is: for an inlier, $r/\sigma$ follows a chi distribution with $\nu$ degrees of freedom, cut at a quantile $k$. The goal is a model of small quality

$$Q(\theta) = \sum_{i=1}^{n} \rho\big(r(\theta, x_i)\big).$$

This is an M-estimator form of [robust model fitting](/robust-model-fitting/) with a bounded loss. The code fits a 2D affine map $q = A p + b$ from $s = 3$ point pairs, with $r = \lVert A p + b - q \rVert$ and $\nu = 2$. For $\nu = 2$ the weight is

$$w(r) = \frac{1}{\sigma_{\max}} \sqrt{\frac{\pi}{2}} \Big(\operatorname{erfc}\big(\tfrac{r}{\sqrt{2}\,\sigma_{\max}}\big) - \operatorname{erfc}\big(\tfrac{k}{\sqrt{2}}\big)\Big) \text{ for } r < k\sigma_{\max}, \qquad w(r) = 0 \text{ after}.$$

For other $\nu$, the papers write $w$ and $\rho$ with incomplete gamma functions. For $\nu = 2$ they reduce to $\operatorname{erf}$ and $\operatorname{erfc}$.

## The algorithm

```pseudo id=main
MAGSAC++(D, σ_max, p, k_max)                 ▷ n = |D|, s items per sample
L1  θ* ← none, Q* ← ∞, k ← k_max, t ← 0
L2  while t < k do
L3      t ← t + 1
L4      θ ← FIT-MINIMAL(s distinct items of D, drawn uniformly at random)
L5      if θ is none then continue                ▷ degenerate sample
L6      Q ← Σ_i ρ(r(θ, x_i))
L7      if Q < Q* then
L8          θ' ← SIGMA-CONSENSUS++(θ)
L9          if Q(θ') < Q then θ ← θ', Q ← Q(θ')
L10         θ* ← θ, Q* ← Q
L11         k ← min(k_max, stopping count of θ* averaged over noise scales)
L12 return θ*, Q*

SIGMA-CONSENSUS++(θ)
L13 repeat a fixed number of times
L14     w_i ← w(r(θ, x_i)) for i = 1, …, n
L15     θ ← argmin over θ of Σ_i w_i r(θ, x_i)²
L16 return θ
```

Lines L6 and L7 replace the inlier count of RANSAC with the marginalized loss. Lines L13 to L15 are iteratively reweighted least squares: items with a small residual get a large weight, and items beyond $k\sigma_{\max}$ get weight 0. Line L11 of the code takes the scales $\sigma_j = j\,\sigma_{\max}/d$ for $j = 1, \ldots, d$, counts the items with $r \le k\sigma_j$, applies the RANSAC formula $\lceil \log(1-p)/\log(1-w_j^s) \rceil$ to each ratio $w_j$, caps each count at $k_{\max}$ and takes the mean. MAGSAC also defines a stopping rule that takes the unknown noise scale into account. The rule of the code is a simple version of this idea, not the formula of the papers.

## Example

Take $\sigma_{\max} = 0.5$ and the 7 point pairs $(0,0) \to (1, 0.1)$, $(1,0) \to (2,0)$, $(0,1) \to (1,1)$, $(1,1) \to (2.1, 1)$ and $(2,1) \to (3,1)$, which follow a shift by $(1, 0)$ with small errors, and the outliers $(2,2) \to (5,-1)$ and $(0,2) \to (-2,4)$. The code uses $k = \sqrt{-2 \ln 0.01} \approx 3.035$, the 0.99 quantile of the chi distribution with 2 degrees of freedom, so items with $r \ge k\sigma_{\max} \approx 1.517$ get weight 0 and the largest loss, $\rho_{\max} \approx 0.3050$.

| sample | residuals of the 7 pairs | $Q$ |
|---|---|---|
| pairs 1, 2, 3 | 0, 0, 0, 0.141, 0.2, 3.36, 3.66 | $0.0213 + 0.0395 + 2(0.3050) = 0.6708$ |
| pairs 1, 5, 6 | 0, 1.85, 3.52, 1.71, 0, 0, 10.6 | 1.2199 |
| pairs 1, 2, 4 | 0, 0, 0.141, 0, 0.141, 3.41, 3.72 | 0.6525 |

A sample with an outlier puts the other inliers far from the model, so it pays $\rho_{\max}$ many times. The two outliers cost the same $\rho_{\max}$ for every good model, however far they are. Now polish the first model. Its weights are $2.50$ for the three exact pairs, $1.94$ and $1.72$ for the next two and 0 for the outliers. One weighted fit lowers $Q$ to $0.6227$, and after the second step $Q = 0.62259$ with $A = \begin{pmatrix} 1 & 0.032 \\ -0.020 & 0.96 \end{pmatrix}$ and $b = (1, 0.06)$. Over all 32 samples of 3 pairs that are not collinear, the least $Q$ is 0.6323, so the polished model is better than every minimal model. With $p = 0.99$ and $d = 10$, line L11 gives $k = 11$, and for the seeds 0 to 3 the run stops after 11 rounds with $Q = 0.62259$.

## Correctness

Four facts make the method sound (proofs below). First, $w(r)$ is equal to the density of the residual of an inlier, averaged over $\sigma$ uniform on $[0, \sigma_{\max}]$, with the density at each $\sigma$ cut at $k\sigma$. Second, $w$ is non-negative and non-increasing, so $\rho$ is non-decreasing and constant beyond $k\sigma_{\max}$: a far outlier adds a fixed cost and cannot pull the model. Third, the closed form of $\rho$ in the code has derivative $r\,w(r)$ and value 0 at 0. Fourth, one step of lines L14 and L15 never increases $Q$. The function $v \mapsto \rho(\sqrt{v})$ is concave, so the weighted squares give an upper bound of $Q$ that touches it at the current model. The loop keeps the invariant that $\theta^*$ has the least $Q$ among all models it has evaluated, and it ends after at most $k_{\max}$ rounds. As for RANSAC, the result is optimal only if a good sample is drawn, so the stopping rule is a heuristic.

## Complexity

One round costs the minimal solver, $O(1)$ for a fixed model type, plus $n$ residuals and losses, so $\Theta(n)$ in the [real RAM](/real-ram/), with $\operatorname{erf}$ and $\exp$ at unit cost. A new best model also costs a fixed number of weighted fits of $O(n)$ each, and the stopping count costs $O(d\,n)$. With a fixed number of reweighting steps and a fixed $d$, $k$ rounds cost $\Theta(k n)$, the same order as RANSAC. A round has a larger constant than in RANSAC, because the loss uses $\operatorname{erfc}$ and $\exp$. The extra space is $\Theta(n)$ for the residuals and weights.

## Properties

- **No hard threshold.** Only $\sigma_{\max}$ is needed. Changing $\sigma_{\max}$ changes the loss smoothly. The papers report better accuracy than threshold-based methods on homography and epipolar geometry benchmarks (an experimental result).
- **Bounded loss.** $\rho$ is constant beyond $k\sigma_{\max}$, as the truncated quadratic of MSAC is beyond $T$.
- **Monotone refinement.** Each reweighting step does not increase $Q$, a majorize-minimize argument.
- **Randomized.** Like RANSAC, the result depends on the samples drawn.

## Variants and improvements

- **MAGSAC (2019)** approximates the marginalization over $\sigma$ by fits at a finite set of noise scales. MAGSAC++ replaces it with the closed-form loss and the reweighted least squares step, which is faster.
- **Progressive NAPSAC.** The MAGSAC++ paper also proposes a sampler that first draws samples from small neighborhoods and then from larger ones.
- **[MSAC](/msac/)** and **[MLESAC](/mlesac/)** are the threshold-based scores that MAGSAC generalizes.
- **[LO-RANSAC](/lo-ransac/)** refines each new best model too, but with a fixed threshold.
- **[PROSAC](/prosac/)** changes the sampling order and can be combined with the MAGSAC++ score.

## When to use it

Use MAGSAC++ when the noise level is not known well enough to choose a threshold, for example when the same pipeline runs on images of different sizes or quality. It fits the same problems as RANSAC: [homographies](/homography-estimation/), [fundamental matrices](/fundamental-matrix/) and [essential matrices](/essential-matrix/). If a good threshold is known and speed matters most, [MSAC](/msac/) with [LO-RANSAC](/lo-ransac/) is simpler.

## Pitfalls

- **The degrees of freedom.** The weight depends on $\nu$, the dimension of the residual. Use the $\nu$ that matches the residual, for example 2 for a point-to-point error in the image and 1 for a point-to-line error.
- **The scale of $\sigma_{\max}$.** $\sigma_{\max}$ is an upper bound, not the noise level. A value that is far too large lets outliers get weight.
- **Degenerate weighted fits.** If fewer than $s$ items have non-zero weight, the weighted normal equations are singular. Keep the old model in that case.
- **Numerics of erfc.** For large arguments, compute $\operatorname{erfc}$ directly, not as $1 - \operatorname{erf}$, to keep small weights accurate.

## Implementations

The Python code fits a 2D affine map with $s = 3$ and $\nu = 2$. The functions `magsac_weight` and `magsac_loss` give the closed forms of $w$ and $\rho$, and `sigma_consensus_pp` is the reweighting loop of lines L13 to L16. The weighted fit solves two $3 \times 3$ normal equations by Gaussian elimination. The tests check $w$ against a numerical integral over $\sigma$, $\rho$ against a numerical integral of $x\,w(x)$, the descent of each reweighting step and the example.

## History

Barath, Matas and Noskova posted MAGSAC on arXiv in 2018 and published it at CVPR 2019. They proposed to remove the inlier threshold of RANSAC by marginalizing over the noise scale, with a new quality function and a new termination criterion. Barath, Noskova, Ivashechkin and Matas published MAGSAC++ at CVPR 2020. It derives the weight and the loss with incomplete gamma functions, writes the refinement as iteratively reweighted least squares, and adds the Progressive NAPSAC sampler. The idea of a bounded robust loss goes back to the M-estimators of robust statistics, and its use in RANSAC to [MSAC](/msac/) and [MLESAC](/mlesac/) of Torr and Zisserman (2000).

## References
