---
tag: QMX934
kind: technique
slug: regression-discontinuity-design
name: Regression discontinuity design
aliases:
- regression discontinuity
area: statistics-and-inference/causal-inference-and-experimental-design
level: core
summary: When treatment is assigned by a score crossing a cutoff, estimate the effect by the jump in the outcome regression at the cutoff, using local linear fits.
prereqs: [potential-outcomes-framework, average-treatment-effect, instrumental-variables-estimation]
see_also: [local-polynomial-regression, weighted-least-squares, local-average-treatment-effect, two-stage-least-squares, kernel-density-estimation, bias-variance-tradeoff, difference-in-differences, cross-validation]
sources:
  - paper: doi:10.1037/h0044319
    title: Donald L. Thistlethwaite and Donald T. Campbell, Regression-discontinuity analysis, an alternative to the ex post facto experiment, Journal of Educational Psychology 51(6), 1960
    locator: pp. 309 to 317 (the design, with National Merit certificates of merit as the treatment)
  - paper: doi:10.1111/1468-0262.00183
    title: Jinyong Hahn, Petra Todd and Wilbert van der Klaauw, Identification and estimation of treatment effects with a regression-discontinuity design, Econometrica 69(1), 2001
    locator: pp. 201 to 209 (identification under continuity, the fuzzy design as a local instrumental variables problem, local linear estimation)
  - paper: doi:10.1016/j.jeconom.2007.05.001
    title: Guido W. Imbens and Thomas Lemieux, Regression discontinuity designs, a guide to practice, Journal of Econometrics 142(2), 2008
    locator: pp. 615 to 635 (local linear fits, the pooled regression form, graphs and checks)
  - paper: doi:10.1093/restud/rdr043
    title: Guido Imbens and Karthik Kalyanaraman, Optimal bandwidth choice for the regression discontinuity estimator, The Review of Economic Studies 79(3), 2012
    locator: pp. 933 to 959 (the mean squared error optimal bandwidth and its plug-in estimate)
  - paper: doi:10.3982/ECTA11757
    title: Sebastian Calonico, Matias D. Cattaneo and Rocío Titiunik, Robust nonparametric confidence intervals for regression-discontinuity designs, Econometrica 82(6), 2014
    locator: pp. 2295 to 2326 (bias correction with a variance that accounts for it)
  - paper: doi:10.1016/j.jeconom.2007.05.005
    title: Justin McCrary, Manipulation of the running variable in the regression discontinuity design, a density test, Journal of Econometrics 142(2), 2008
    locator: pp. 698 to 714 (testing for a jump in the density of the running variable)
  - paper: doi:10.1016/j.jeconom.2007.05.004
    title: David S. Lee, Randomized experiments from non-random selection in U.S. House elections, Journal of Econometrics 142(2), 2008
    locator: pp. 675 to 697 (close elections, and why imprecise control of the score makes the design as good as local randomization)
  - paper: doi:10.1080/07350015.2017.1366909
    title: Andrew Gelman and Guido Imbens, Why high-order polynomials should not be used in regression discontinuity designs, Journal of Business and Economic Statistics 37(3), 2019
    locator: pp. 447 to 456 (noisy weights and poor coverage of global polynomial fits)
---

A regression discontinuity design estimates the effect of a treatment that is given to units whose score $X$, the running variable, is at or above a known cutoff $c$. Units just above and just below the cutoff are alike in everything except the treatment, so a jump in the mean outcome at $c$ is the effect of the treatment for units at the cutoff. The estimate fits a straight line to the outcome on each side of the cutoff, using only units within a bandwidth $h$ and giving more weight to units closer to $c$, and takes the difference of the two lines at $c$. It needs no assumption about how the treatment was chosen apart from the rule itself, and no ignorability. It needs the outcome means to be continuous in the score at the cutoff, which fails if units can move their score across it. When crossing the cutoff only raises the chance of treatment, the fuzzy design divides the jump in the outcome by the jump in the treatment rate, an [instrumental variables](/instrumental-variables-estimation/) estimate at the cutoff.

## In plain words

A scholarship goes to every student who scores 80 or more on a test. Students with 79 and students with 81 are, for practical purposes, the same: one or two questions apart, which is luck. If students just above 80 later earn more than students just below, the difference is the effect of the scholarship, not of being a better student, because the better students are on both sides in almost equal measure.

We cannot compare students at exactly 80 on both sides, because there are none. So we draw a line through the data just left of 80 and one just right, and read off where each line hits 80.

## When it applies

Each unit has a running variable $X$ with a density positive around $c$, potential outcomes $Y(0)$ and $Y(1)$, and treatment $T$.

- **Sharp design.** $T = \mathbf{1}[X \ge c]$. The target is $\tau = \mathbb{E}[Y(1) - Y(0) \mid X = c]$.
- **Fuzzy design.** $\Pr[T = 1 \mid X = x]$ jumps at $c$ but not from 0 to 1. The target is the average effect at the cutoff for the units whose treatment changes when their score crosses it.

**Identification in the sharp design.** Assume $\mu_0(x) = \mathbb{E}[Y(0) \mid X = x]$ and $\mu_1(x) = \mathbb{E}[Y(1) \mid X = x]$ are continuous at $c$. Then

$$\tau = \lim_{x \downarrow c}\mathbb{E}[Y \mid X = x] - \lim_{x \uparrow c}\mathbb{E}[Y \mid X = x].$$

*Proof.* For $x \ge c$ every unit is treated, so $\mathbb{E}[Y \mid X = x] = \mu_1(x)$, and the right limit is $\mu_1(c)$ by continuity. For $x < c$ no unit is treated, so $\mathbb{E}[Y \mid X = x] = \mu_0(x)$, and the left limit is $\mu_0(c)$. The difference is $\mu_1(c) - \mu_0(c) = \tau$. $\blacksquare$

The proof uses nothing about how $X$ relates to the potential outcomes away from $c$: $X$ may be strongly related to them, as test scores are to later earnings. Continuity is what can fail. If units know the rule and can adjust their score, those who sort just above the cutoff differ from those just below, and $\mu_0$ jumps at $c$. Lee (2008) showed that if units control their score only imprecisely, with a random part whose density is continuous, then continuity holds, and treatment near the cutoff is as good as randomly assigned.

**Identification in the fuzzy design.** Hahn, Todd and van der Klaauw (2001) show that the ratio of the jump in $\mathbb{E}[Y \mid X]$ to the jump in $\mathbb{E}[T \mid X]$ is the average effect for compliers at the cutoff, under continuity and a monotonicity condition. This is the [local average treatment effect theorem](/local-average-treatment-effect/) with $\mathbf{1}[X \ge c]$ as the instrument, applied in the limit at $c$. The page cites this result and does not prove the limit argument.

The design does not apply when the cutoff is not known, when the running variable is discrete with few values near $c$, when other treatments change at the same cutoff, or when there is evidence of sorting.

## The template

**Estimation.** Local linear regression on each side with the triangular kernel:

```pseudo id=main
RDD(x, y, c, h)                          ▷ sharp design, bandwidth h > 0
L1  wᵢ ← max(0, 1 - |xᵢ - c| / h)
L2  (a₋, b₋) ← WLS of y on (1, x - c) with weights w over the units with x < c
L3  (a₊, b₊) ← WLS of y on (1, x - c) with weights w over the units with x ≥ c
L4  τ̂ ← a₊ - a₋
L5  se ← √(Σᵢ ℓᵢ² eᵢ²) over both sides     ▷ ℓᵢ the weight of yᵢ in its side's intercept, eᵢ the residual
L6  return (τ̂, se)
```

The cost is $\Theta(n)$. The fuzzy design runs RDD on $y$ and on $T$ and divides the two jumps; its standard error linearizes the ratio. Choosing $h$ is the hard part and is an input of the code. Imbens and Kalyanaraman (2012) give a plug-in bandwidth that minimizes the mean squared error of $\hat\tau$, and Calonico, Cattaneo and Titiunik (2014) correct the bias of that choice and widen the interval to account for the correction.

**Why local linear and not local constant.** At a boundary, a weighted mean of $y$ near $c$ has bias of order $h$ when the regression function has a slope, because all the data lie on one side. A local line removes that term and leaves bias of order $h^2$ (Hahn, Todd and van der Klaauw 2001). This is the boundary property of [local polynomial regression](/local-polynomial-regression/). The fit on one side is a [weighted least squares](/weighted-least-squares/) problem in closed form. With weighted means $\bar v = \sum w_iv_i/\sum w_i$, $\bar y$ and $S_v = \sum w_i(v_i - \bar v)^2$ for $v_i = x_i - c$, the intercept is

$$a = \sum_i \ell_i y_i, \qquad \ell_i = \frac{w_i}{\sum_j w_j} - \frac{\bar v\,w_i(v_i - \bar v)}{S_v}.$$

These weights satisfy $\sum\ell_i = 1$ and $\sum\ell_iv_i = 0$, so a line $y = \alpha + \beta v$ gives $a = \alpha$ exactly. Hence, if the noise-free outcome is a line on each side, $\hat\tau$ is the true jump for every bandwidth, which the tests check in fractions.

**The pooled regression is exact.** Fit by WLS, with the same kernel weights, $y$ on $(1, T, v, Tv)$ with $T = \mathbf{1}[x \ge c]$. The left units have regressors $(1, 0, v, 0)$ and the right units $(1, 1, v, v)$. Reparametrize as $(\alpha_-, \beta_-) = (\gamma_0, \gamma_2)$ and $(\alpha_+, \beta_+) = (\gamma_0 + \gamma_1, \gamma_2 + \gamma_3)$; the map is one to one and the weighted sum of squares splits into a left part depending only on $(\alpha_-, \beta_-)$ and a right part depending only on $(\alpha_+, \beta_+)$. So the pooled minimum is the pair of side minima, and $\hat\gamma_1 = a_+ - a_-$. The tests check this, and the side fits against a direct solve of the weighted normal equations, exactly in 60 random cases.

**Worked example.** Cutoff $c = 0$, bandwidth $h = 2$:

| $x$ | -2.5 | -1.5 | -1 | -0.5 | 0 | 0.5 | 1 | 1.5 | 2.5 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $y$ | 2 | 1 | 3 | 2 | 6 | 5 | 7 | 6 | 9 |
| $w$ | 0 | 1/4 | 1/2 | 3/4 | 1 | 3/4 | 1/2 | 1/4 | 0 |

The end points get weight 0 and drop out. On the left, $\sum w = 3/2$, $\bar v = -5/6$, $\bar y = 13/6$, $S_v = 5/24$ and $\sum w(v - \bar v)y = 1/12$, so the slope is $2/5$ and the intercept is $13/6 + \frac25 \cdot \frac56 = 5/2$. On the right, $\sum w = 5/2$, $\bar v = 1/2$, $\bar y = 59/10$, $S_v = 5/8$ and $\sum w(v - \bar v)y = 1/4$, so the slope is $2/5$ and the intercept is $59/10 - \frac25 \cdot \frac12 = 57/10$. The jump is $\hat\tau = 57/10 - 5/2 = 16/5$. The pooled regression gives $(5/2, 16/5, 2/5, 0)$, the same jump.

**Simulation.** $X$ uniform on $(-1, 1)$, $c = 0$, $Y = 0.5 + 0.8X + 0.6X^2 + \mathbf{1}[X \ge 0] + \varepsilon$ with $\varepsilon \sim N(0, 0.3^2)$, $n = 1000$, 300 samples each. In the second design the right side has an extra $2X^2$, so the curvature jumps by $4$. All numbers are measured; the predicted bias is the standard leading term for the triangular kernel at a flat design density, $-(h^2/20)(\mu_+'' - \mu_-'')$.

| design | $h$ | mean of $\hat\tau$ | predicted mean | SD | coverage of $\hat\tau \pm 1.96\,\mathrm{se}$ |
| --- | --- | --- | --- | --- | --- |
| same curvature | 0.2 | 0.992 | 1 | 0.086 | 0.94 |
| same curvature | 0.4 | 0.993 | 1 | 0.062 | 0.95 |
| curvature jump 4 | 0.2 | 0.989 | 0.992 | 0.092 | 0.95 |
| curvature jump 4 | 0.4 | 0.971 | 0.968 | 0.062 | 0.93 |
| curvature jump 4 | 0.8 | 0.875 | 0.872 | 0.043 | 0.25 |

A wider bandwidth lowers the standard deviation and raises the bias. At $h = 0.8$ the bias is three standard deviations and the interval misses three times out of four. This is why the bias-corrected interval of Calonico, Cattaneo and Titiunik is preferred when $h$ is chosen to minimize mean squared error, since that choice makes bias and standard deviation of the same order.

## Classic examples

- **Merit awards.** Thistlethwaite and Campbell (1960) compared students just above and below the score that earned a National Merit certificate of merit, the first use of the design.
- **Close elections.** Lee (2008) compared U.S. House districts where a party barely won with those where it barely lost, to measure the incumbency advantage. Vote share is hard to control precisely, which supports continuity.
- **Class size.** Angrist and Lavy used Maimonides' rule, which splits a class when enrollment passes 40, as a fuzzy design: enrollment crossing a multiple of 40 lowers the class size.
- **Age thresholds.** The legal drinking age, pension eligibility and school entry dates assign treatment by age crossing a cutoff, with age as the running variable.
- **Credit scores and test scores.** Many decisions by firms and schools use a score cutoff, which makes the design common in practice.

## Variations

- **Fuzzy design.** Ratio of two jumps; equivalent to [2SLS](/two-stage-least-squares/) with $\mathbf{1}[X \ge c]$ as the instrument and the same kernel weights and side-specific slopes.
- **Bandwidth choice.** The Imbens-Kalyanaraman plug-in bandwidth, the Calonico-Cattaneo-Titiunik bandwidth with robust bias-corrected intervals, or [cross-validation](/cross-validation/) of the fit near the cutoff.
- **Other kernels and degrees.** The triangular kernel is optimal for boundary estimation in a minimax sense; the uniform kernel gives a plain local regression. Local quadratic fits are used for bias correction. Global polynomials of high degree are a bad choice: Gelman and Imbens (2019) show their implicit weights are noisy and their intervals under-cover.
- **Covariates.** Adding predetermined covariates can reduce variance but must not change the estimand; a covariate that jumps at the cutoff is a warning sign.
- **Regression kink design.** If the treatment intensity changes slope, not level, at the cutoff, the effect is the ratio of the kinks.
- **Multiple cutoffs and geographic boundaries.** Several cutoffs can be pooled after normalizing the running variable; a border between regions gives a two-dimensional running variable.
- **Local randomization.** In a small window around $c$, treat assignment as random and use a [permutation test](/permutation-test/), which avoids the extrapolation of the line.

## Pitfalls

- **Sorting.** If units can push their score over the cutoff, the units just above differ from those just below. Check the density of $X$ for a jump at $c$ (McCrary 2008), and check that predetermined covariates do not jump.
- **High-order global polynomials.** They fit well far from the cutoff and badly at it. Use local linear fits.
- **Reporting the interval at the MSE-optimal bandwidth without bias correction.** The bias is of the same order as the standard deviation, so the plain interval under-covers.
- **Reading the estimate as an average effect for everyone.** It is the effect at the cutoff. Units far from the cutoff may respond differently.
- **Discrete running variables.** With few distinct values near $c$, the local fits extrapolate from coarse points, and the usual standard errors are too small.
- **Other policies at the same cutoff.** An age of 65 changes pension and health insurance at once, and the jump is their combined effect.

## Exercises

1. Show that the local constant estimate (weighted means on each side) has bias of order $h$ when $\mu_0$ and $\mu_1$ have the same nonzero slope $\beta$ at $c$, for a uniform design density.
   <details><summary>Answer</summary>On the right the weighted mean of $\mu_1(c) + \beta v$ is $\mu_1(c) + \beta\bar v_+$ with $\bar v_+ \approx h/3$ for the triangular kernel, and on the left $\mu_0(c) + \beta\bar v_-$ with $\bar v_- \approx -h/3$. The difference is $\tau + 2\beta h/3$.</details>
2. In the worked example, add 10 to $y$ at $x = 2.5$. What changes?
   <details><summary>Answer</summary>Nothing: its weight is 0 because $\lvert 2.5\rvert > h$.</details>
3. Prove that $\sum_i\ell_i v_i = 0$.
   <details><summary>Answer</summary>$\sum w_iv_i/\sum w_j = \bar v$, and $\sum w_i(v_i - \bar v)v_i = S_v$, so $\sum\ell_iv_i = \bar v - \bar v S_v/S_v = 0$.</details>
4. A fuzzy design has a jump of 0.4 in the treatment rate and of 1.2 in the outcome. What is the estimate, and for whom?
   <details><summary>Answer</summary>3, the average effect at the cutoff for units whose treatment switches when their score crosses $c$.</details>
5. Explain why a placebo cutoff, a value of $c'$ away from $c$ where no treatment changes, should give a jump near zero, and what a large placebo jump suggests.
   <details><summary>Answer</summary>Away from $c$ both sides of $c'$ have the same treatment, so under continuity of $\mu_0$ and $\mu_1$ the true jump at $c'$ is 0. A large estimate there means the regression function has jumps or sharp bends that the local lines do not follow, so a jump at $c$ may also come from the shape of the function and not from the treatment.</details>

## References
