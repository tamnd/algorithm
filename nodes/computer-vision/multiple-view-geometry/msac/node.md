---
tag: S7R7BT
kind: algorithm
slug: msac
name: MSAC
aliases:
- M-estimator sample consensus
area: computer-vision/multiple-view-geometry
level: advanced
summary: "RANSAC that scores a model by a truncated quadratic cost of the residuals instead of the inlier count, so it prefers models that fit the inliers well."
solves: [robust-model-fitting]
model: real-ram
complexity:
  vars: {n: the number of data items, k: "the number of samples drawn, at most a set cap"}
  time: {worst: Θ(k n), average: Θ(k n), best: Θ(k n)}
  space: {extra: Θ(n)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2000
  people: [Philip H. S. Torr, Andrew Zisserman]
  note: "Torr and Zisserman defined MSAC in their MLESAC paper in Computer Vision and Image Understanding (2000), as the RANSAC loop with the redescending M-estimator cost of a truncated quadratic."
prereqs: [ransac, m-estimator]
see_also: [mlesac, magsac, lo-ransac, ransac-iteration-bound, least-median-of-squares, huber-m-estimator, robust-model-fitting]
sources:
  - paper: doi:10.1006/cviu.1999.0832
    title: "Philip H. S. Torr and Andrew Zisserman, MLESAC: a new robust estimator with application to estimating image geometry, Computer Vision and Image Understanding 78(1), 2000, 138-156"
    locator: "The section that compares the RANSAC cost with the truncated quadratic cost of MSAC, before the definition of MLESAC"
  - paper: doi:10.1109/TPAMI.2012.257
    title: "Rahul Raguram, Ondrej Chum, Marc Pollefeys, Jiri Matas and Jan-Michael Frahm, USAC: a universal framework for random sample consensus, IEEE Transactions on Pattern Analysis and Machine Intelligence 35(8), 2013, 2022-2038"
    locator: "The part of the survey on model verification and the choice of the cost function"
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 4.7, Robust estimation (the distance threshold from the chi-square distribution)"
---

MSAC (M-estimator sample consensus) is a variant of [RANSAC](/ransac/) that changes only the score of a model. RANSAC counts the inliers, the items whose residual is at most a threshold $T$, so all inliers count the same and a model that passes close to them does not beat a model that passes near the edge of the band. MSAC gives each item the cost $\min(r^2, T^2)$: an inlier pays its squared residual and an outlier pays the constant $T^2$. The model of least total cost wins. This is the truncated quadratic, a redescending [M-estimator](/m-estimator/) cost, which is where the name comes from. Torr and Zisserman (2000) introduced it together with [MLESAC](/mlesac/). The change costs nothing extra per item, and it makes the result less sensitive to the choice of $T$.

## In plain words

RANSAC asks each guess one question: how many points are close enough? Every close point gets one vote, whether it lies right on the guess or just inside the limit. So two guesses can tie even though one of them clearly fits better.

MSAC asks a finer question. Every close point adds a penalty equal to the square of its distance, so points right on the guess cost almost nothing. Every far point adds the same fixed penalty, the square of the limit, however far it is. The guess with the smallest total penalty wins. Far points still cannot pull the answer, because their penalty has a ceiling. Close points now say how well the guess fits them.

## The problem

The input is as for [RANSAC](/ransac/): data $D = \{x_1, \ldots, x_n\}$, a minimal solver for samples of $s$ items, a residual $r(\theta, x)$, a threshold $T$, a confidence $p$ and a cap $k_{\max}$. The goal is a model of small truncated quadratic cost

$$C(\theta) = \sum_{i=1}^{n} \rho\big(r(\theta, x_i)\big), \qquad \rho(r) = \min(r^2, T^2).$$

A model of least cost is a solution of [robust model fitting](/robust-model-fitting/) with this M-estimator. MSAC searches only the models of minimal samples, so it is a randomized heuristic for this goal, as RANSAC is for maximum consensus.

## The algorithm

```pseudo id=main
MSAC(D, s, T, p, k_max)                      ▷ n = |D|
L1  θ* ← none, C* ← ∞, I* ← ∅, k ← k_max, t ← 0
L2  while t < k do
L3      t ← t + 1
L4      S ← s distinct items of D, drawn uniformly at random
L5      θ ← FIT-MINIMAL(S)                    ▷ none for a degenerate sample
L6      if θ is none then continue
L7      e_i ← r(θ, x_i)² for i = 1, …, n
L8      C ← Σ_i min(e_i, T²)
L9      if C < C* then
L10         θ* ← θ, C* ← C
L11         I* ← {x_i : e_i ≤ T²}
L12         k ← min(k_max, ⌈log(1 − p) / log(1 − (|I*|/n)^s)⌉)
L13 if θ* is none then return failure
L14 θ ← FIT-LEAST-SQUARES(I*)
L15 return θ, I*, C*
```

Lines L7 and L8 replace the inlier count of RANSAC. Line L12 is the adaptive stopping rule of RANSAC, with the inlier ratio of the model of least cost so far. Unlike in RANSAC, this ratio can drop when a better model has fewer inliers, so $k$ can grow again, but never above $k_{\max}$. Line L14 refits the model to the inliers of the best model, as in RANSAC.

The threshold $T$ is a design choice. For a residual of one dimension with Gaussian noise of standard deviation $\sigma$, a common choice is $T^2 = 3.84\,\sigma^2$, the 95 percent point of a chi-square variable with one degree of freedom (Hartley and Zisserman, Section 4.7).

## Example

Take the 7 points $(0,0), (1,0.1), (2,0), (3,0.1), (4,0)$, which lie near $y = 0$, and the outliers $(1,2), (3,-2)$. Use lines with $s = 2$, the point-to-line distance, $T = 0.25$ (so $T^2 = 0.0625$) and $p = 0.99$. Three samples:

| $t$ | sample | line | inliers | cost $C$ | $C^*$ | $k$ |
|---|---|---|---|---|---|---|
| 1 | $(1,0.1), (3,0.1)$ | $y = 0.1$ | 5 | $3(0.01) + 2(0.0625) = 0.155$ | 0.155 | 7 |
| 2 | $(2,0), (1,2)$ | $2x + y = 4$ | 3 | $0.25$ | 0.155 | 7 |
| 3 | $(0,0), (4,0)$ | $y = 0$ | 5 | $2(0.01) + 2(0.0625) = 0.145$ | 0.145 | 7 |

The line $2x + y = 4$ passes exactly through $(2,0)$ and both outliers, so its cost is $4 T^2 = 0.25$. The lines $y = 0.1$ and $y = 0$ have the same five inliers. RANSAC sees a tie and keeps the first one, $y = 0.1$. MSAC prefers $y = 0$, because its inliers are closer. With $w = 5/7$, the stopping rule gives $\lceil \log 0.01 / \log(1 - 25/49) \rceil = 7$. Over all 21 pairs of points, the least cost is 0.145, so no later sample can replace $y = 0$, and the refit on the five inliers gives $y = 0.04$, the mean height of the five points.

## Correctness

MSAC keeps an invariant at line L2: $\theta^*$ has the least cost among the models of the samples drawn so far, and $C^*$ is that cost. The loop ends after at most $k_{\max}$ rounds, because $t$ grows by 1 in each round and line L12 never sets $k$ above $k_{\max}$. The probabilistic guarantee of RANSAC carries over in a weaker form. Suppose a model of least cost $\theta_{\min}$ is the model of every sample inside its inlier set $I$, and the samples are independent. Then a run of at least $K$ rounds returns cost $C(\theta_{\min})$ with probability at least $1 - (1 - q)^K$, where $q$ is the probability that a sample lies in $I$. The stopping rule gives this count only if the best model so far has at least $|I|$ inliers, which is not always true, so for MSAC the rule is a heuristic. The proof is below.

## Complexity

One round costs the minimal solver, $O(1)$ for a fixed model type, plus $n$ residuals and a sum, so $\Theta(n)$ in the [real RAM](/real-ram/), the same as a round of RANSAC. With $k$ rounds the time is $\Theta(k n)$, and the extra space is $\Theta(n)$ for the squared residuals and the inlier set. The number of rounds $k$ is random and at most $k_{\max}$. When the best model has inlier ratio $w$, the rule of line L12 asks for about $\log(1 - p)/\log(1 - w^s)$ rounds, as in the [iteration bound](/ransac-iteration-bound/).

## Properties

- **Same loop as RANSAC.** Only the score differs. The cost per round is the same up to a constant.
- **Bounded influence.** An outlier adds $T^2$ however large its residual is, so a far outlier cannot move the result (the cost is redescending, the same as the inlier count).
- **Finer ranking.** Models with the same inliers are ranked by how well they fit them, so ties of RANSAC are broken in favor of the better fit (a theorem about the score, shown in the example). Torr and Zisserman report that this gives more accurate models at no extra cost (a benchmark result of their paper).
- **Less sensitive to $T$.** For a fixed model, the cost is a continuous function of $T$, while the inlier count jumps by whole items. An item that crosses the threshold changes the cost by almost nothing.

## Variants and improvements

- **[MLESAC](/mlesac/)** replaces the truncated quadratic with the negative log-likelihood of a mixture of Gaussian inliers and uniform outliers, and estimates the mixing weight for each model.
- **[MAGSAC](/magsac/)** removes the fixed threshold: it marginalizes the cost over a range of noise scales.
- **[LO-RANSAC](/lo-ransac/)** with the truncated quadratic cost in its local step (LO+ of Lebeda, Matas and Chum, 2012) combines MSAC scoring with local optimization.
- **Other M-estimator costs.** A [Huber cost](/huber-m-estimator/) is not bounded, so a far outlier still pulls the result; robust samplers use bounded costs such as the truncated quadratic.
- **[Least median of squares](/least-median-of-squares/)** scores a model by the median squared residual, which needs no threshold but fails beyond half outliers.

## When to use it

Use MSAC in place of plain RANSAC in almost every case: it costs the same per round, needs the same threshold and breaks the ties of the inlier count by the quality of fit. Use it when the result is the input to a refinement that minimizes a squared error, because the two costs agree inside the band. If the noise level is not known well, consider [MAGSAC](/magsac/). If the score of each model must be cheap to compare early, as in [preemptive RANSAC](/preemptive-ransac/), any additive cost works, the truncated quadratic included.

## Pitfalls

- **The stopping rule uses inliers.** The best model by cost does not always have the most inliers. Compute the inlier ratio of line L12 from the best model by cost, and do not mix the two scores.
- **Units of $T$.** The cost is in squared residual units. Use the same residual in the cost, the inlier set and the refit, for example the [Sampson distance](/sampson-distance/) for the fundamental matrix.
- **Comparing costs across data sets.** The cost depends on $n$ and on $T$. Compare costs only for the same data and threshold.
- **No refit.** As in RANSAC, the model of the minimal sample is noisy. Refit on the inlier set.

## Implementations

The Python code fits a line in the plane with $s = 2$. The loop takes the minimal solver, the residual and the refit as arguments. The function `msac_cost` gives the truncated quadratic cost of any model, which the tests use to check the invariant on every sampled model.

## History

Torr and Zisserman published MSAC in 2000, in their paper on MLESAC in Computer Vision and Image Understanding. They observed that RANSAC minimizes a cost that is 0 for an inlier and 1 for an outlier, so it is an M-estimator with a step function, and that a truncated quadratic gives a better estimate at the same cost. The idea comes from the M-estimators of robust statistics, which Huber introduced in 1964. In the USAC framework of Raguram, Chum, Pollefeys, Matas and Frahm (2013), the truncated quadratic score is a standard part, and later methods such as [MAGSAC](/magsac/) take it as the base cost to improve on.

## References
