---
tag: 3GWPBP
kind: algorithm
slug: mlesac
name: MLESAC
aliases:
- maximum likelihood estimation sample consensus
area: computer-vision/multiple-view-geometry
level: advanced
summary: "RANSAC that scores each model by the likelihood of a mixture of Gaussian inliers and uniform outliers; for each model, EM estimates only the mixing weight."
solves: [robust-model-fitting]
model: real-ram
complexity:
  vars: {n: the number of data items, k: "the number of samples drawn, at most a set cap", m: the number of EM steps for each model}
  time: {worst: Θ(k m n), average: Θ(k m n), best: Θ(k m n)}
  space: {extra: Θ(n)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2000
  people: [Philip H. S. Torr, Andrew Zisserman]
  note: "Torr and Zisserman published MLESAC in Computer Vision and Image Understanding in 2000, for the robust estimation of image geometry such as the fundamental matrix."
prereqs: [ransac, maximum-likelihood-estimation, expectation-maximization]
see_also: [msac, magsac, ransac-iteration-bound, lo-ransac, prosac, m-estimator, robust-model-fitting]
sources:
  - paper: doi:10.1006/cviu.1999.0832
    title: "Philip H. S. Torr and Andrew Zisserman, MLESAC: a new robust estimator with application to estimating image geometry, Computer Vision and Image Understanding 78(1), 2000, 138-156"
    locator: "The definition of MLESAC: the mixture model of the errors, the estimation of the mixing parameter by EM and the comparison with RANSAC and MSAC"
  - paper: doi:10.1007/3-540-47969-4_6
    title: "Ben J. Tordoff and David W. Murray, Guided sampling and consensus for motion estimation, European Conference on Computer Vision 2002, Lecture Notes in Computer Science 2350, 82-96"
    locator: "Guided MLESAC: match scores as prior inlier probabilities in the sampling and in the mixture"
  - paper: doi:10.1109/TPAMI.2012.257
    title: "Rahul Raguram, Ondrej Chum, Marc Pollefeys, Jiri Matas and Jan-Michael Frahm, USAC: a universal framework for random sample consensus, IEEE Transactions on Pattern Analysis and Machine Intelligence 35(8), 2013, 2022-2038"
    locator: "The part of the survey on model verification and the choice of the cost function"
---

MLESAC (maximum likelihood estimation sample consensus) is a variant of [RANSAC](/ransac/) that scores a model by a likelihood instead of an inlier count. It models the residual of an item as a mixture: with probability $\gamma$ the item is an inlier, and its residual is Gaussian with a known standard deviation $\sigma$; with probability $1 - \gamma$ it is an outlier, and its residual is uniform on a range of size $v$. For each model from a minimal sample, a few steps of [expectation maximization](/expectation-maximization/) estimate the mixing weight $\gamma$, and nothing else, because the model itself is fixed by the sample. The model of largest likelihood wins. Torr and Zisserman (2000) introduced MLESAC together with [MSAC](/msac/), which uses a truncated quadratic instead.

## In plain words

RANSAC and MSAC need a hard limit that splits points into good and bad. MLESAC uses a softer rule. It says: a good point is near the guess, with small errors much more likely than large ones; a bad point can be anywhere in the picture with the same chance. Each point then gets a degree of belief that it is good.

Before a guess can be scored, MLESAC must know what fraction of the points are good. It does not know, so it starts at one half and improves the fraction a few times: it computes the belief of each point and takes their average as the new fraction.

The score of the guess is how well this mix of good and bad points explains all the points at once. The guess with the best score wins.

## The problem

The input is data $D = \{x_1, \ldots, x_n\}$, a minimal solver for samples of $s$ items, a residual $r(\theta, x)$, the inlier noise $\sigma$, the size $v$ of the range of outlier residuals, a confidence $p$, a cap $k_{\max}$ and a number $m$ of EM steps. With $\phi_\sigma(e) = \exp(-e^2/2\sigma^2) / (\sqrt{2\pi}\,\sigma)$, the negative log-likelihood of a model with mixing weight $\gamma$ is

$$L(\theta, \gamma) = -\sum_{i=1}^{n} \log\Big(\gamma\, \phi_\sigma\big(r(\theta, x_i)\big) + \frac{1 - \gamma}{v}\Big).$$

The goal is a model of small $\min_\gamma L(\theta, \gamma)$. MLESAC searches only the models of minimal samples, so it is a randomized heuristic for this goal, a case of [robust model fitting](/robust-model-fitting/) by [maximum likelihood](/maximum-likelihood-estimation/).

## The algorithm

```pseudo id=main
MLESAC(D, s, σ, v, p, k_max, m)              ▷ n = |D|
L1  θ* ← none, L* ← ∞, γ* ← 0, k ← k_max, t ← 0
L2  while t < k do
L3      t ← t + 1
L4      S ← s distinct items of D, drawn uniformly at random
L5      θ ← FIT-MINIMAL(S)                    ▷ none for a degenerate sample
L6      if θ is none then continue
L7      g_i ← φ_σ(r(θ, x_i)) for i = 1, …, n
L8      γ ← 1/2
L9      repeat m times
L10         z_i ← γ g_i / (γ g_i + (1 − γ)/v) for i = 1, …, n
L11         γ ← (1/n) Σ_i z_i
L12     L ← − Σ_i log(γ g_i + (1 − γ)/v)
L13     if L < L* then
L14         θ* ← θ, L* ← L, γ* ← γ
L15         k ← min(k_max, ⌈log(1 − p) / log(1 − γ^s)⌉)
L16 if θ* is none then return failure
L17 θ ← weighted least squares on D with the weights z_i of θ* and γ*
L18 return θ, γ*, L*
```

Lines L8 to L11 are EM for one unknown. The E step of line L10 computes $z_i$, the posterior probability that item $i$ is an inlier. The M step of line L11 sets $\gamma$ to their mean. The model $\theta$ stays fixed: EM here does not refit the model, it only estimates the inlier fraction for the model at hand. Line L15 is the adaptive rule of RANSAC with $\gamma$ as the inlier ratio. Line L17 is a final refit; the code uses a weighted least squares fit with the weights $z_i$, a choice of this code.

## Example

Take the 7 points $(0,0), (1,0.1), (2,0), (3,0.1), (4,0), (1,2), (3,-2)$, lines with $s = 2$, the point-to-line distance, $\sigma = 0.1$, $v = 10$ and $m = 5$. Three samples:

| $t$ | sample | line | $\gamma$ after 1 step | $\gamma$ after 5 steps | $L$ |
|---|---|---|---|---|---|
| 1 | $(1,0.1), (3,0.1)$ | $y = 0.1$ | 0.6903 | 0.7040 | 3.3040 |
| 2 | $(2,0), (1,2)$ | $2x + y = 4$ | 0.4181 | 0.4139 | 9.7382 |
| 3 | $(0,0), (4,0)$ | $y = 0$ | 0.6925 | 0.7050 | 2.8107 |

The slanted line passes exactly through 3 of the 7 points, and EM gives it $\gamma \approx 0.41$, a little below $3/7 \approx 0.43$, because the other points are far. The lines $y = 0.1$ and $y = 0$ both have five close points, but $y = 0$ is closer to them, so its likelihood is larger and $L$ is smaller: MLESAC prefers $y = 0$, as [MSAC](/msac/) does. With $\gamma = 0.705$, line L15 gives $\lceil \log 0.01 / \log(1 - 0.705^2) \rceil = 7$ rounds. The weighted refit gives the line $y = 0.0398$; the weights of the two outliers are almost 0.

## Correctness

MLESAC keeps an invariant at line L2: $\theta^*$ has the least value of $L$ among the models of the samples drawn so far, where $L$ is computed with the $\gamma$ of $m$ EM steps from $1/2$. The loop ends after at most $k_{\max}$ rounds. For a fixed model, $\ell(\gamma) = -L(\theta, \gamma)$ is concave in $\gamma$, and one EM step is $\gamma' = \gamma + \gamma(1 - \gamma)\,\ell'(\gamma)/n$, which never decreases $\ell$ (the ascent property of EM). So more EM steps only make the score of a model better, and a fixed point inside $(0, 1)$ is the maximum likelihood weight. The guarantee of the sampling part is the same as for MSAC: if the model of least score is the model of every sample in its inlier set, a run of $K$ rounds finds it with probability at least $1 - (1 - q)^K$. The stopping rule with $\gamma$ is a heuristic. The proof is below.

## Complexity

One round costs the minimal solver, $O(1)$ for a fixed model type, then $n$ densities in line L7, $m$ EM steps of $\Theta(n)$ each and one sum of $n$ logarithms, so $\Theta(m n)$ in the [real RAM](/real-ram/) with $\exp$ and $\log$ as unit-cost operations. With $k$ rounds the time is $\Theta(k m n)$, against $\Theta(k n)$ for RANSAC and MSAC. With a small fixed $m$, the cost per round is a constant factor more than MSAC. The extra space is $\Theta(n)$. The number of rounds $k$ is random, at most $k_{\max}$, and follows the [iteration bound](/ransac-iteration-bound/) with $\gamma$ in place of the inlier ratio.

## Properties

- **Soft inliers.** Each item has a posterior inlier probability $z_i$ instead of a yes or no label.
- **Two parameters instead of a threshold.** MLESAC needs $\sigma$ and $v$. An implicit threshold remains: an item is more likely an inlier than an outlier when $\gamma\,\phi_\sigma(e) > (1 - \gamma)/v$.
- **EM estimates only $\gamma$.** The model is the model of the sample. The EM is a one-dimensional fit, cheap and with a unique optimum, since the log-likelihood is concave in $\gamma$ (a theorem).
- **Bounded influence.** A far outlier adds about $-\log((1 - \gamma)/v)$ to $L$ whatever its residual is, so, as for MSAC, its influence has a ceiling.
- **Accuracy.** Torr and Zisserman report that MLESAC gives more accurate fundamental matrices than RANSAC in their experiments (a benchmark result).

## Variants and improvements

- **[MSAC](/msac/)** is the cheaper relative: a truncated quadratic cost with no EM. Each round costs one pass over the data.
- **Guided MLESAC.** Tordoff and Murray (2002) use the match scores of the feature matcher as prior inlier probabilities, both to choose the samples and in the mixture. [PROSAC](/prosac/) uses the ordering of the scores instead of their values.
- **[MAGSAC](/magsac/)** keeps a likelihood view but removes the fixed $\sigma$ by marginalizing over it.
- **[LO-RANSAC](/lo-ransac/)** adds local optimization of the best model, which works with any of these scores.
- **More EM.** One can run EM over both $\gamma$ and the model, which turns the last step into an iteratively reweighted fit, as in the [iteratively reweighted least squares](/iteratively-reweighted-least-squares/) step of MAGSAC++.

## When to use it

Use MLESAC when the inlier noise $\sigma$ is known well, the outliers spread over a known range, and an accurate score matters more than a few EM steps per model. If the outlier range $v$ is not known, or the speed of each round matters, use [MSAC](/msac/). If $\sigma$ is not known well, use [MAGSAC](/magsac/).

## Pitfalls

- **The wrong $v$.** The implicit threshold falls as the outlier density $1/v$ grows. If $v$ is too small, true inliers with moderate residuals are explained as outliers. If $v$ is too large, outliers near the model are explained as inliers. Set $v$ from the range of residuals that are possible, for example the size of the search window in pixels.
- **Numerical underflow.** For large residuals $\phi_\sigma(e)$ underflows to 0. The mixture term $(1 - \gamma)/v$ keeps the logarithm finite, so do not drop it, and do not compute the log of the Gaussian term alone.
- **EM from a bad start.** The concavity makes the start harmless in the limit, but with few EM steps the estimate of $\gamma$ is not converged. Use the same $m$ for all models so that their scores are comparable.
- **$\gamma$ for stopping.** $\gamma$ is an estimate of the inlier ratio for the best model so far, not a bound on the ratio of the best model overall, so the stopping rule is a heuristic.

## Implementations

The Python code fits a line in the plane with $s = 2$. The functions `em_mixing` and `mixture_nll` give the EM estimate of $\gamma$ and the score of any model, and the tests use them to check the ascent of EM and the invariant on every sampled model.

## History

Torr and Zisserman published MLESAC in 2000 in Computer Vision and Image Understanding, for the estimation of the fundamental matrix and other image relations. They gave the mixture of a Gaussian and a uniform distribution for the errors, the EM estimate of the mixing weight and the MSAC cost as a cheaper alternative. Tordoff and Murray (2002) added guided sampling with prior inlier probabilities from the match scores. The likelihood view led to the marginalization over $\sigma$ in [MAGSAC](/magsac/) (2019).

## References
