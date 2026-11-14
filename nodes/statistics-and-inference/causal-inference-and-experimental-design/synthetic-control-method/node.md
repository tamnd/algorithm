---
tag: 1N66SX
kind: algorithm
slug: synthetic-control-method
name: Synthetic control method
aliases:
- Abadie synthetic control
area: statistics-and-inference/causal-inference-and-experimental-design
level: advanced
summary: Builds a weighted mix of control units that matches the treated unit before the intervention, and estimates the effect by the gap after it.
model: real-ram
complexity:
  vars: {k: "the number of pre-period features", J: "the number of donor units", t: "the number of gradient iterations"}
  time: {worst: Θ(t (k J^2 + J^3)), best: Θ(k J^2 + J^3)}
  space: {extra: Θ(k J + J^2)}
properties: {deterministic: true, weights_nonnegative_and_sum_to_one: true, convex_problem: true, exact_kkt_certificate_in_rational_arithmetic: true, placebo_pvalue_valid_under_exchangeability: true}
history:
  year: 2003
  people: [Alberto Abadie, Javier Gardeazabal, Alexis Diamond, Jens Hainmueller]
  note: Abadie and Gardeazabal (2003) built a synthetic Basque Country from other Spanish regions to measure the cost of terrorism. Abadie, Diamond and Hainmueller (2010) gave the general method, its factor-model justification and the placebo test, with California's tobacco program as the example.
prereqs: [potential-outcomes-framework, difference-in-differences, permutation-test]
see_also: [quadratic-programming, projected-gradient-descent, kkt-conditions, cross-validation, average-treatment-effect, regression-discontinuity-design, inverse-probability-weighting, ridge-regression]
sources:
  - paper: doi:10.1257/000282803321455188
    title: Alberto Abadie and Javier Gardeazabal, The economic costs of conflict, a case study of the Basque Country, American Economic Review 93(1), 2003
    locator: pp. 113 to 132 (the first synthetic control, built from other Spanish regions)
  - paper: doi:10.1198/jasa.2009.ap08746
    title: Alberto Abadie, Alexis Diamond and Jens Hainmueller, Synthetic control methods for comparative case studies, estimating the effect of California's tobacco control program, Journal of the American Statistical Association 105(490), 2010
    locator: pp. 493 to 505 (the estimator, the bias bound under a factor model, placebo inference)
  - paper: doi:10.1111/ajps.12116
    title: Alberto Abadie, Alexis Diamond and Jens Hainmueller, Comparative politics and the synthetic control method, American Journal of Political Science 59(2), 2015
    locator: pp. 495 to 510 (German reunification, cross-validation of the predictor weights, leave-one-out checks)
  - paper: doi:10.1257/jel.20191450
    title: Alberto Abadie, Using synthetic controls, feasibility, data requirements, and methodological aspects, Journal of Economic Literature 59(2), 2021
    locator: pp. 391 to 425 (when the method is appropriate, the role of the pre-period fit, inference)
  - paper: doi:10.1145/1390156.1390191
    title: John Duchi, Shai Shalev-Shwartz, Yoram Singer and Tushar Chandra, Efficient projections onto the l1-ball for learning in high dimensions, ICML 2008
    locator: pp. 272 to 279 (the sort-based projection onto the simplex)
  - paper: doi:10.1137/080716542
    title: Amir Beck and Marc Teboulle, A fast iterative shrinkage-thresholding algorithm for linear inverse problems, SIAM Journal on Imaging Sciences 2(1), 2009
    locator: pp. 183 to 202 (the O(1/t) rate of the basic proximal gradient method, of which projected gradient is a case; general locator, the theorem number was not checked)
  - paper: doi:10.1080/01621459.2021.1929245
    title: Eli Ben-Michael, Avi Feller and Jesse Rothstein, The augmented synthetic control method, Journal of the American Statistical Association 116(536), 2021
    locator: pp. 1789 to 1803 (bias correction with an outcome model when the pre-period fit is imperfect)
  - paper: doi:10.1257/aer.20190159
    title: Dmitry Arkhangelsky, Susan Athey, David A. Hirshberg, Guido W. Imbens and Stefan Wager, Synthetic difference-in-differences, American Economic Review 111(12), 2021
    locator: pp. 4088 to 4118 (unit and time weights combined with two-way fixed effects)
---

The synthetic control method estimates the effect of an intervention on one unit, such as a state that passes a law, when no single untreated unit is a good comparison. It looks for nonnegative weights, summing to one, on the untreated units (the donor pool) so that the weighted average of their outcomes before the intervention tracks the treated unit's outcomes. This weighted average is the synthetic control. After the intervention, the gap between the treated unit and its synthetic control estimates the effect, period by period. The weights solve a small convex quadratic program over the simplex. This page solves it by projected gradient descent, stops with the Frank-Wolfe gap, which bounds the error, and finishes by solving the KKT conditions on the support exactly, which certifies the answer. Inference comes from placebo runs that treat each donor in turn as if it were treated.

## In plain words

California raised its cigarette tax in 1988. To see what the law did to cigarette sales, we need California's sales without the law, which never happened. No other state looks like California. But a blend of several states might. If that blend matched California's sales year by year for the years before 1988, it is a fair guess for what California would have done after 1988 without the law. The difference after 1988 is the estimate.

The weights are nonnegative and add to one, so the blend is an average of real states and never extrapolates outside them. They are found by fitting the past, without looking at the outcomes after the intervention.

## The problem

**Identification.** Unit 1 is treated from period $T_0 + 1$ on; units $2, \dots, J + 1$ are never treated. For $t > T_0$ the target is the effect on the treated unit, $\tau_{1t} = Y_{1t}(1) - Y_{1t}(0)$, of which $Y_{1t}(1) = Y_{1t}$ is observed. The missing $Y_{1t}(0)$ is estimated by $\sum_j w_jY_{jt}$. Abadie, Diamond and Hainmueller (2010) justify this with a linear factor model, $Y_{it}(0) = \delta_t + \theta_t^\top Z_i + \lambda_t^\top\mu_i + \varepsilon_{it}$, with observed covariates $Z_i$ and unobserved factor loadings $\mu_i$. If weights reproduce the treated unit's $Z_1$ and its whole pre-period path, they must also roughly reproduce its $\mu_1$, so the bias after $T_0$ is small, and it shrinks as the number of pre-periods grows relative to the noise. Unlike [difference in differences](/difference-in-differences/), the factor model allows different units to load differently on common trends. This argument is cited, not proved here.

**Estimation.** Collect $k$ pre-period features of the treated unit in $x_1$: the outcomes in some or all of the pre-periods, and covariates. Collect the same features of the donors in the columns of the $k \times J$ matrix $X_0$. With feature weights $v > 0$, $V = \operatorname{diag}(v)$, the weights are

$$w^* \in \arg\min_{w \in \Delta}(x_1 - X_0w)^\top V(x_1 - X_0w), \qquad \Delta = \{w : w_j \ge 0,\ \textstyle\sum_jw_j = 1\}.$$

The estimate for $t > T_0$ is $\hat\tau_{1t} = Y_{1t} - \sum_jw_j^*Y_{jt}$. Choosing $v$ is a separate outer problem: Abadie and coauthors pick $v$ to minimize the pre-period prediction error of the outcome, or by cross-validation over an early and a late part of the pre-period. This page takes $v$ as given, all ones by default.

## The algorithm

The problem is a [quadratic program](/quadratic-programming/) with $J$ variables, one equality and $J$ bounds. [Projected gradient descent](/projected-gradient-descent/) fits it well, because projection onto the simplex is cheap:

```pseudo id=main
SYNTH(x₁, X₀, v, ε)
L1  w ← (1/J, …, 1/J);  L ← 2 Σ_r Σ_j v_r X₀[r][j]²
L2  repeat
L3      g ← -2 X₀ᵀ V (x₁ - X₀ w)                       ▷ the gradient
L4      γ ← gᵀw - min_j g_j                            ▷ Frank-Wolfe gap, at least f(w) - min f
L5      if γ ≤ ε(1 + f(w)) or (every 20th pass) the KKT system on the support of w has a valid solution then exit the loop
L6      w ← Π_Δ(w - g/L)                               ▷ projection: sort, shift, clip at 0
L7  solve 2AᵀVA w_S - ν1 = 2AᵀV x₁, 1ᵀw_S = 1 exactly on S = {j : w_j > 0}, A = X₀[:, S]; keep it if w_S > 0 and g_j ≥ ν off S
L8  return w
```

The projection $\Pi_\Delta(u)$ sorts $u$, finds the largest $\rho$ with $u_{(\rho)} > \frac1\rho(\sum_{l \le \rho}u_{(l)} - 1) = \theta$, and returns $\max(u_j - \theta, 0)$ (Duchi et al. 2008). The gradient loop runs in floating point. Line L7 runs in the input arithmetic, so with fractions it returns exact rational weights, together with the multiplier $\nu$ that certifies them.

## Example

Three donors, three pre-periods and one post-period; columns are donors:

| period | treated | donor 1 | donor 2 | donor 3 |
| --- | --- | --- | --- | --- |
| 1 (pre) | 7 | 5 | 7 | 8 |
| 2 (pre) | 4 | 5 | 9 | 6 |
| 3 (pre) | 4 | 3 | 0 | 3 |
| 4 (post) | 10 | 6 | 8 | 7 |

In period 2 the treated value 4 is below every donor, so no blend can fit exactly. SYNTH stops at its first KKT check after 19 gradient steps and returns $w = (1/2, 0, 1/2)$. Check by hand: on the edge $w = (a, 0, 1 - a)$ the synthetic path is $(8 - 3a, 6 - a, 3)$, the residuals are $(3a - 1, a - 2, 1)$, and the loss $(3a - 1)^2 + (a - 2)^2 + 1$ has derivative $20a - 10$, zero at $a = 1/2$, where the loss is $1/4 + 9/4 + 1 = 7/2$. To see that leaving donor 2 out is right, compute the gradient at $w$: with residual $e = (1/2, -3/2, 1)$, $g = -2X_0^\top e = (4, 20, 4)$. The donors in use share the value $\nu = 4$, and donor 2 has the larger value 20, so moving weight to it raises the loss: the KKT conditions hold, and by the certificate theorem $w$ is optimal. The post-period synthetic value is $(6 + 7)/2 = 6.5$, so the estimated effect is $10 - 6.5 = 3.5$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The objective is convex, so for any feasible $w$ with gradient $g$, $f(w) - \min f \le g^\top w - \min_jg_j$: the gap of line L4 is a computable bound on the error. When the KKT system of line L7 has a solution with positive weights and no off-support gradient entry below $\nu$, the gap is zero and $w$ is a minimizer. The projection formula is proved from the KKT conditions of the projection problem. The trace bound $L \ge \lambda_{\max}(2X_0^\top VX_0)$ makes $1/L$ a safe step, and the $O(L/t)$ rate of projected gradient is cited (Beck and Teboulle 2009). The minimizer is unique when $X_0$ has full column rank, and in every case some minimizer has at most $k + 1$ positive weights.

The placebo p-value $\#\{u : R_u \ge R_0\}/(J + 1)$, where $R_u$ is the ratio of post-period to pre-period root mean squared prediction error with unit $u$ treated as the treated one, is valid when the units are exchangeable under the null; the proof is the usual rank argument of a [permutation test](/permutation-test/).

The tests check the KKT conditions exactly in fractions on 60 random problems, compare the loss against every point of a simplex grid with step 1/120 for three donors, check the gap bound exactly at random feasible points, check the projection against random points of the simplex, and run the placebo test. In the placebo test, 8 units load on one common trend with 10 pre-periods and 4 post-periods (seed 2026). With an effect of 5 on unit 1, its ratio is 12.2 against at most 6.8 for the placebos, so $p = 1/8$, the smallest possible value. With no effect, 9 of 40 samples (0.225) gave $p \le 0.25$, against 0.25 expected. Here the units are exchangeable by construction, so the expected share is exactly 0.25 and the difference is sampling noise.

## Complexity

One gradient step costs $\Theta(kJ)$ for the gradient and $\Theta(J\log J)$ for the projection. A KKT check costs $\Theta(ks^2 + s^3)$ for a support of size $s \le J$, and runs every 20 steps, so $t$ steps cost $\Theta(t(kJ^2 + J^3))$ in the worst case, and the final exact solve costs $\Theta(kJ^2 + J^3)$ arithmetic operations. In practice $s$ is small. Measured on 100 random problems with $k = 30$ features and $J = 20$ donors: median 79 steps, maximum 319, total 2.1 s of CPU in pure Python. The worst case of the gradient phase is $t = O(L/\varepsilon)$ steps. Extra space is $\Theta(kJ)$ for the copy of the data and $\Theta(J^2)$ for the KKT system. The placebo test repeats the fit $J + 1$ times.

## Properties

- The weights are nonnegative and sum to one, so the synthetic control is a convex combination of donors and cannot extrapolate outside their range.
- The weights are sparse: some minimizer uses at most $k + 1$ donors, and in practice few donors get weight.
- The weights are chosen without the post-period outcomes, which keeps the analyst from tuning the fit to the result.
- Adding the same constant to the treated unit and to every donor does not change the weights, because they sum to one. A shift of one unit alone does change them, so a treated unit with a different level must be matched by level too; synthetic difference in differences removes that need.
- With fraction inputs the polished weights are exact rationals and carry their own certificate $\nu$.

## Variants and improvements

- **Predictor weights.** Choosing $v$ by minimizing pre-period outcome fit is a bilevel problem; Abadie, Diamond and Hainmueller (2015) use cross-validation over two halves of the pre-period instead.
- **Penalized weights.** Adding a penalty that favours donors close to the treated unit makes the solution unique and sparse.
- **Augmented synthetic control.** Ben-Michael, Feller and Rothstein (2021) correct the bias of an imperfect fit with an outcome model, such as a [ridge regression](/ridge-regression/), allowing weights outside the simplex.
- **Synthetic difference in differences.** Arkhangelsky et al. (2021) weight both units and pre-periods and add unit fixed effects, which removes level differences that the plain method must fit.
- **Several treated units.** Fit a synthetic control for each and average, or fit one for the average of the treated units.
- **Solvers.** Any quadratic programming method works: active set methods, interior point, or Frank-Wolfe steps, whose iterates are sparse by construction.

## When to use it

Use it for comparative case studies: one or a few treated aggregate units, such as countries, states or cities, a long pre-period, and a donor pool of similar units that were not exposed. The pre-period fit must be good, and the treated unit must lie inside or near the range of the donors. With many treated units and short panels, [difference in differences](/difference-in-differences/) or regression methods are better. With large samples of individuals and measured confounders, use [inverse probability weighting](/inverse-probability-weighting/) or related estimators instead.

## Pitfalls

- **A poor pre-period fit.** If the synthetic control does not track the treated unit before the intervention, the post-period gap is not credible. Report the pre-period root mean squared error and the plot.
- **Treated units outside the donors' range.** A unit with the highest values of all cannot be matched by a convex combination; the fit will have a systematic gap.
- **Spillovers into the donor pool.** If the law in California changed smoking in Nevada, Nevada is not a valid donor.
- **Matching on all pre-period outcomes and nothing else.** Some authors put each pre-period outcome in $x_1$, which makes covariates irrelevant; this is a choice and should be reported.
- **Overfitting with many donors and few pre-periods.** When $J$ is large compared with the number of pre-periods, a close fit may come from noise. Use a smaller donor pool of similar units.
- **Reading the placebo p-value as a sampling p-value.** It measures how unusual the treated gap is among placebo gaps; its validity needs exchangeability, and with $J$ donors it cannot be below $1/(J + 1)$.

## Implementations

## History

Abadie and Gardeazabal (2003) estimated the economic cost of terrorism in the Basque Country by comparing it with a combination of other Spanish regions, mostly Catalonia and Madrid. Abadie, Diamond and Hainmueller (2010) made the method general. They studied California's Proposition 99 tobacco program of 1988 with a donor pool of 38 states, justified the estimator under a factor model, and introduced inference by placebo runs on every donor. Abadie, Diamond and Hainmueller (2015) applied it to German reunification and added cross-validation. Abadie (2021) reviewed when the method is appropriate. Later work combined it with outcome models (Ben-Michael, Feller and Rothstein 2021) and with difference in differences (Arkhangelsky et al. 2021).

## References
