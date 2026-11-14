---
tag: GVS3R2
kind: algorithm
slug: inverse-probability-weighting
name: Inverse probability weighting
aliases:
- IPW
- inverse probability of treatment weighting
- IPTW
area: statistics-and-inference/causal-inference-and-experimental-design
level: core
summary: Weights each unit by one over the probability of the treatment it received, so the weighted sample mimics a randomized experiment.
model: real-ram
complexity:
  vars: {n: "the number of units"}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, single_pass: true, unbiased_with_known_propensity: true, needs_positivity: true, ht_form_shift_equivariant: false, hajek_form_shift_equivariant: true}
history:
  year: 1987
  people: [Paul R. Rosenbaum, James M. Robins]
  note: The weight is the Horvitz-Thompson weight of survey sampling (1952). Rosenbaum used weighting by the estimated propensity score for causal effects in 1987, and Robins, Rotnitzky and Zhao developed inverse probability weighted estimating equations in 1994.
prereqs: [propensity-score, horvitz-thompson-estimator]
see_also: [augmented-inverse-probability-weighting, propensity-score-matching, rosenbaum-sensitivity-analysis, importance-sampling, off-policy-evaluation, missing-data-mechanism, stratified-sampling, m-estimator]
sources:
  - paper: doi:10.1080/01621459.1952.10483446
    title: D. G. Horvitz and D. J. Thompson, A generalization of sampling without replacement from a finite universe, Journal of the American Statistical Association 47(260), 1952
    locator: pp. 663 to 685 (the weight one over the inclusion probability and the unbiasedness of the weighted total)
  - paper: doi:10.1080/01621459.1987.10478441
    title: Paul R. Rosenbaum, Model-based direct adjustment, Journal of the American Statistical Association 82(398), 1987
    locator: pp. 387 to 394 (weighting by the inverse of the estimated propensity score)
  - paper: doi:10.1080/01621459.1994.10476818
    title: James M. Robins, Andrea Rotnitzky and Lue Ping Zhao, Estimation of regression coefficients when some regressors are not always observed, Journal of the American Statistical Association 89(427), 1994
    locator: pp. 846 to 866 (inverse probability weighted estimating equations and their augmented form)
  - paper: doi:10.1111/1468-0262.00442
    title: Keisuke Hirano, Guido W. Imbens and Geert Ridder, Efficient estimation of average treatment effects using the estimated propensity score, Econometrica 71(4), 2003
    locator: pp. 1161 to 1189 (weighting by a nonparametric estimate of the propensity score reaches the efficiency bound)
  - paper: doi:10.1002/sim.1903
    title: Jared K. Lunceford and Marie Davidian, Stratification and weighting via the propensity score in estimation of causal treatment effects, a comparative study, Statistics in Medicine 23(19), 2004
    locator: pp. 2937 to 2960 (the weighted estimators, their sandwich variances, and the effect of estimating the propensity score)
  - paper: doi:10.1093/biomet/asn055
    title: Richard K. Crump, V. Joseph Hotz, Guido W. Imbens and Oscar A. Mitnik, Dealing with limited overlap in estimation of average treatment effects, Biometrika 96(1), 2009
    locator: pp. 187 to 199 (trimming units with propensity scores near 0 or 1)
  - book: isbn:9780521885881
    title: Guido W. Imbens and Donald B. Rubin, Causal Inference for Statistics, Social, and Biomedical Sciences, Cambridge University Press, 2015
    locator: Chapter 12 (unconfounded treatment assignment) and Chapter 14 (assessing overlap)
  - book: isbn:9781420076165
    title: Miguel A. Hernán and James M. Robins, Causal Inference, What If, Chapman and Hall/CRC, 2020
    locator: Chapter 2 (randomized experiments and weighting) and Chapter 12 (IP weighting)
---

Inverse probability weighting (IPW) estimates the [average treatment effect](/average-treatment-effect/) $\tau = \mathbb{E}[Y(1) - Y(0)]$ from data in which the treatment was not assigned with equal chances. Each treated unit gets weight $1/e(X_i)$ and each control gets weight $1/(1 - e(X_i))$, where $e(x) = \Pr[T = 1 \mid X = x]$ is the [propensity score](/propensity-score/). The weighted treated units then stand for the whole sample as if all had been treated, and the weighted controls stand for the whole sample as if none had been treated. Under [ignorability](/ignorability/), positivity and [SUTVA](/sutva/), and with known propensities, the estimate is unbiased; this is the [Horvitz-Thompson estimator](/horvitz-thompson-estimator/) applied once to each treatment arm. It takes one pass over the data.

## In plain words

Suppose people with a mild illness got the new drug one time in four, and people with a severe illness three times in four. Then the treated group has too few mild cases. Each treated mild case had a one in four chance of being treated, so it stands in for four mild people. Each treated severe case stands in for four thirds of a severe person. After weighting, the treated group has the same mix of mild and severe cases as the full sample, and the same holds for the controls with weights one over the chance of no treatment. The difference of the weighted means compares like with like.

This only works if the treatment chance depends on things we measured, and if every kind of person had some chance of each treatment.

## The problem

The two parts of the problem are kept apart: what the data can identify, and how to estimate it.

**Identification.** Each unit has [potential outcomes](/potential-outcomes-framework/) $Y(1)$ and $Y(0)$, a treatment $T \in \{0, 1\}$ and covariates $X$ measured before treatment. The units $(X_i, T_i, Y_i(0), Y_i(1))$ are independent draws from one distribution. The estimand is $\tau = \mathbb{E}[Y(1) - Y(0)]$. The assumptions are:

1. *Consistency and [SUTVA](/sutva/).* The observed outcome is $Y = T\,Y(1) + (1 - T)\,Y(0)$: one version of each treatment, and no effect of other units' treatments.
2. *[Ignorability](/ignorability/).* $(Y(0), Y(1)) \perp T \mid X$: given $X$, the treatment does not depend on the potential outcomes.
3. *Positivity.* $0 < e(X) < 1$ with probability 1.

Under these assumptions,

$$\mathbb{E}[Y(1)] = \mathbb{E}\left[\frac{T\,Y}{e(X)}\right], \qquad \mathbb{E}[Y(0)] = \mathbb{E}\left[\frac{(1 - T)\,Y}{1 - e(X)}\right],$$

so $\tau$ is a function of the distribution of the observed $(X, T, Y)$. Positivity can be checked in part from data: estimated propensities near 0 or 1 show where it fails or nearly fails. Ignorability cannot be checked from the observed data, and SUTVA is a claim about the design. Both rest on knowledge of how the treatment was assigned.

**Estimation.** The input is $n$ triples $(T_i, Y_i, e_i)$ with $e_i = e(X_i)$. The propensity is known in a designed experiment with unequal assignment chances, and must be estimated in an observational study, for example by [logistic regression](/logistic-regression/). The output is two estimates of $\tau$:

$$\hat\tau_{\mathrm{HT}} = \frac1n\sum_{i=1}^n\left(\frac{T_iY_i}{e_i} - \frac{(1 - T_i)Y_i}{1 - e_i}\right), \qquad \hat\tau_{\mathrm{H}} = \frac{\sum_i T_iY_i/e_i}{\sum_i T_i/e_i} - \frac{\sum_i (1 - T_i)Y_i/(1 - e_i)}{\sum_i (1 - T_i)/(1 - e_i)}.$$

The first is the Horvitz-Thompson form, and the second is the Hájek form, which divides each weighted sum by the sum of its weights instead of by $n$.

## The algorithm

```pseudo id=main
IPW-ATE(T, Y, e)                             ▷ n units; needs 0 < e_i < 1
L1  a1 ← 0;  a0 ← 0;  w1 ← 0;  w0 ← 0
L2  for i ← 1 to n do
L3      if e_i ≤ 0 or e_i ≥ 1 then error "positivity fails"
L4      if T_i = 1 then a1 ← a1 + Y_i / e_i;  w1 ← w1 + 1 / e_i
L5      else a0 ← a0 + Y_i / (1 - e_i);  w0 ← w0 + 1 / (1 - e_i)
L6  τ_HT ← (a1 - a0) / n
L7  τ_H ← a1 / w1 - a0 / w0                  ▷ needs w1 > 0 and w0 > 0
L8  return (τ_HT, τ_H)
```

Line L3 stops on a propensity of 0 or 1, where the weight is infinite or the unit can only ever be in one arm. Lines L4 and L5 build the weighted sums of each arm. With known propensities, $w_1$ and $w_0$ both have expectation $n$, but in a given sample they differ from $n$; line L6 divides by $n$ and line L7 divides by the sums.

**Variance.** Let $\psi_i = T_iY_i/e_i - (1 - T_i)Y_i/(1 - e_i)$, so that $\hat\tau_{\mathrm{HT}}$ is the mean of the $\psi_i$. With known propensities, the $\psi_i$ are independent and identically distributed, and

$$v_{\mathrm{HT}} = \frac{S_\psi^2}{n}, \qquad S_\psi^2 = \frac{1}{n - 1}\sum_{i=1}^n (\psi_i - \hat\tau_{\mathrm{HT}})^2$$

(divisor $n - 1$) is an unbiased estimate of $\operatorname{Var}[\hat\tau_{\mathrm{HT}}]$. The Hájek form is an [M-estimator](/m-estimator/), and its sandwich estimate is $v_{\mathrm{H}} = \frac{1}{n^2}\sum_i \phi_i^2$ (divisor $n$) with $\phi_i = \frac{n}{w_1}\frac{T_i(Y_i - \hat\mu_1)}{e_i} - \frac{n}{w_0}\frac{(1 - T_i)(Y_i - \hat\mu_0)}{1 - e_i}$, where $\hat\mu_1 = a_1/w_1$ and $\hat\mu_0 = a_0/w_0$. The interval $\hat\tau \pm z_{1 - \alpha/2}\sqrt{v}$ is a normal [confidence interval](/confidence-interval/) of approximate level $1 - \alpha$. Both variance estimates treat $e$ as known; with an estimated propensity they are approximations (see the pitfalls).

## Example

Eight patients have a stratum $x$ (0 for mild, 1 for severe), a treatment and an outcome. The design treated mild patients with probability $1/4$ and severe patients with probability $3/4$.

| unit | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| $x$ | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 |
| $T$ | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 |
| $Y$ | 8 | 7 | 6 | 5 | 7 | 4 | 3 | 1 |
| $e$ | 1/4 | 1/4 | 1/4 | 1/4 | 1/4 | 3/4 | 3/4 | 3/4 |
| weight | 4 | 4 | 4/3 | 4/3 | 4/3 | 4/3 | 4/3 | 4 |

The naive difference of means is $(8 + 7 + 4 + 3)/4 - (6 + 5 + 7 + 1)/4 = 5.5 - 4.75 = 3/4$. It compares a treated group that is half severe with a control group that is one quarter severe.

Lines L4 and L5 give $a_1 = 4 \cdot 8 + 4 \cdot 7 + \tfrac43 \cdot 4 + \tfrac43 \cdot 3 = 208/3$, $w_1 = 32/3$, $a_0 = \tfrac43(6 + 5 + 7) + 4 \cdot 1 = 28$ and $w_0 = 8$. Line L6 gives $\hat\tau_{\mathrm{HT}} = (208/3 - 28)/8 = 26/3 - 7/2 = 31/6 \approx 5.17$. Line L7 gives $\hat\tau_{\mathrm{H}} = 13/2 - 7/2 = 3$. The two forms disagree because $w_1 = 32/3$ is not $n = 8$: in this sample the treated weights add up to more than the sample, and the Horvitz-Thompson treated mean $26/3$ is larger than every treated outcome.

With the empirical propensities instead, $\hat e = 2/5$ in the mild stratum (2 of 5 treated) and $\hat e = 2/3$ in the severe stratum (2 of 3), and both forms give $15/8$. That is the stratified estimate: the mild stratum has mean difference $7.5 - 6 = 1.5$, the severe stratum $3.5 - 1 = 2.5$, and $\tfrac58 \cdot 1.5 + \tfrac38 \cdot 2.5 = 15/8$. The proofs show that this agreement is exact for every discrete $X$.

The example has no known true effect; it shows the arithmetic. The tests check the general claims by exact enumeration.

## Correctness

The proofs below establish, in exact arithmetic:

- the loops compute the two formulas;
- *design-based unbiasedness*: for fixed potential outcomes and any random assignment with known $\pi_i = \Pr[T_i = 1]$ strictly between 0 and 1, $\mathbb{E}[\hat\tau_{\mathrm{HT}}]$ equals the sample average treatment effect $\frac1n\sum_i (Y_i(1) - Y_i(0))$; for independent assignment the variance has a closed form;
- *identification and unbiasedness in the superpopulation*: under consistency, ignorability and positivity, $\mathbb{E}[TY/e(X)] = \mathbb{E}[Y(1)]$ and $\mathbb{E}[(1 - T)Y/(1 - e(X))] = \mathbb{E}[Y(0)]$, so $\mathbb{E}[\hat\tau_{\mathrm{HT}}] = \tau$, and $v_{\mathrm{HT}}$ is unbiased for its variance;
- the Hájek form is [consistent](/consistent-estimator/), by the [law of large numbers](/law-of-large-numbers/);
- under complete randomization both forms equal the difference in means;
- with a discrete $X$ and the empirical propensities, both forms equal the stratified estimate, and the ATT form equals the stratified ATT.

The coverage of the normal intervals, the bias of the Hájek form in finite samples, and the behaviour with estimated propensities from a model are not proved here; the numbers on this page about them are measured by simulation.

## Complexity

Each pass of the loop L2 to L5 does a comparison and two divisions and two additions, so the estimate takes $\Theta(n)$ time in both the best and the worst case, and $\Theta(1)$ extra space for the four sums. The estimate can run on a stream. The variance estimates take a second pass, because $\psi_i$ and $\phi_i$ use the estimate; a single pass with running sums of $\psi_i$ and $\psi_i^2$ also works for $v_{\mathrm{HT}}$, at some cost in rounding error. Estimating the propensity, for example by logistic regression, is a separate cost and usually the larger one.

## Properties

- **Unbiased with known propensities.** The Horvitz-Thompson form is unbiased for the ATE under ignorability and positivity, and for the sample ATE in a randomized design with known, unequal assignment chances. No model for the outcome is needed.
- **The Hájek form stays in range.** $\hat\mu_1 = a_1/w_1$ is a weighted average of the treated outcomes, so it lies between their minimum and maximum. The Horvitz-Thompson mean $a_1/n$ need not: in the example it is $26/3$, above the largest treated outcome 8.
- **Shift equivariance.** Adding a constant $c$ to every outcome adds 0 to $\hat\tau_{\mathrm{H}}$ but adds $c(w_1 - w_0)/n$ to $\hat\tau_{\mathrm{HT}}$. In the example, adding 3 to every outcome raises $\hat\tau_{\mathrm{HT}}$ by $3 \cdot (32/3 - 8)/8 = 1$.
- **Complete randomization.** If $e_i = n_1/n$ for every unit, then $w_1 = w_0 = n$, and both forms are the difference in means of the [randomized experiment](/randomized-experiment/).
- **Stratification.** With a discrete $X$ and $\hat e(x)$ the treated share of stratum $x$, both forms equal $\sum_x \frac{n_x}{n}(\bar Y_{1x} - \bar Y_{0x})$, the stratified estimate, as in the example. The tests check this exactly on 500 random tables.
- **Large weights.** The variance of $\psi_i$ contains $\mathbb{E}[Y(1)^2/e(X)] + \mathbb{E}[Y(0)^2/(1 - e(X))]$, which grows without bound as $e$ approaches 0 or 1, even when positivity holds.

## Variants and improvements

- **Weighting for the effect on the treated.** The ATT $\mathbb{E}[Y(1) - Y(0) \mid T = 1]$ keeps the treated units with weight 1 and gives each control weight $e_i/(1 - e_i)$, which turns the control group into a copy of the treated group's covariate mix. The Hájek form is $\bar Y_{\text{treated}} - \sum_{T_i = 0} \frac{e_i}{1 - e_i}Y_i \big/ \sum_{T_i = 0}\frac{e_i}{1 - e_i}$. It needs only $e(X) < 1$, not $e(X) > 0$.
- **Stabilized weights.** Multiplying the treated weights by $\Pr[T = 1]$ and the control weights by $\Pr[T = 0]$ keeps the weights near 1 on average. In a weighted regression of $Y$ on $T$ this does not change the estimate, which is the Hájek form; it matters in models with more terms, such as marginal structural models.
- **Trimming.** Crump, Hotz, Imbens and Mitnik (2009) drop units whose estimated propensity is outside $[\beta, 1 - \beta]$, with $\beta$ chosen from the data and often near 0.1. The estimand changes to the ATE of the units that remain, and the report must say so.
- **Estimated propensities.** Hirano, Imbens and Ridder (2003) show that weighting by a suitably flexible nonparametric estimate of $e$ gives an estimator with the smallest possible asymptotic variance among regular estimators of the ATE, smaller than weighting by the true $e$.
- **Doubly robust estimators.** [Augmented IPW](/augmented-inverse-probability-weighting/) adds an outcome regression and stays consistent if either the propensity model or the outcome model is right. [TMLE](/targeted-maximum-likelihood-estimation/) and [double machine learning](/double-machine-learning/) build on the same estimating function.
- **Other uses of the weight.** The same weight appears in [importance sampling](/importance-sampling/), in [off-policy evaluation](/off-policy-evaluation/) of a new policy from logged actions, and in analysis of data missing at random (see [missing-data mechanisms](/missing-data-mechanism/)).

## When to use it

Use IPW when the treatment chances are known from the design, or can be estimated well from measured covariates, and ignorability is credible. It gives one effect estimate for the whole population without a model for the outcome, and it extends to time-varying treatments where regression adjustment fails. Prefer the Hájek form in practice. Check overlap first: if many units have estimated propensities near 0 or 1, the weights are unstable, and [propensity score matching](/propensity-score-matching/) for the ATT, trimming, or a doubly robust method is a better choice. When ignorability is in doubt, follow the estimate with a [sensitivity analysis](/rosenbaum-sensitivity-analysis/).

## Pitfalls

- **Weights near the positivity limit.** In a simulation with $X$ uniform on $[0, 1]$, $e(x) = \beta + (1 - 2\beta)x$, effect $0.5 + x$ (true ATE 1), $n = 200$ and 2000 repetitions (seed 2026), $\beta = 0.2$ gave a standard deviation of 0.278 for the Horvitz-Thompson form and 0.191 for the Hájek form, with interval coverage 0.953 and 0.946. With $\beta = 0.01$ the standard deviations rose to 0.367 and 0.277, the Hájek mean was 1.046 instead of 1, and its 95% interval covered only 0.90 of the time. These numbers are measured, not proved.
- **Estimated propensities treated as known.** Plugging $\hat e$ into $v_{\mathrm{HT}}$ or $v_{\mathrm{H}}$ ignores the estimation step. For the ATE with a correctly specified parametric model fitted by maximum likelihood, Lunceford and Davidian (2004) show that this overstates the variance. In a simulation with 3 strata ($e = 0.2, 0.5, 0.8$), $n = 300$, empirical propensities and 2000 repetitions (seed 77), the nominal 95% Hájek interval covered 0.998 of the time. For the ATT the plug-in variance is not always conservative.
- **A wrong propensity model.** IPW is unbiased only with the right $e$. A logistic model with missing terms leaves imbalance in $X$. Check balance: compare the weighted means of each covariate in the two arms, as the [propensity score page](/propensity-score/) explains.
- **Good prediction is not the goal.** A covariate that predicts $T$ but not $Y$, such as an instrument, makes the weights more extreme and adds variance, and it can amplify the bias from an unmeasured confounder. Choose $X$ for confounding, not for the fit of the treatment model.
- **Weighting cannot fix unmeasured confounding.** If ignorability fails, the weighted arms still differ in the unmeasured variable, and the estimate is biased by an amount the data cannot reveal.
- **The Horvitz-Thompson form out of range.** The treated mean $a_1/n$ can lie above every treated outcome, as in the example, and for a binary outcome it can be above 1. Use the Hájek form, or report both.
- **Mixing estimands.** Weights $1/e$ and $1/(1 - e)$ target the ATE, weights $1$ and $e/(1 - e)$ target the ATT, and trimmed weights target a subpopulation. State which one the analysis reports.

## Implementations

## History

The weight $1/\pi_i$ comes from survey sampling, where Horvitz and Thompson (1952) proved that it makes the estimated total unbiased for any design. Rosenbaum (1987) used weighting by the inverse of an estimated propensity score, in his words model-based direct adjustment, to estimate causal effects from observational data. Robins, Rotnitzky and Zhao (1994) built a general theory of inverse probability weighted estimating equations for missing data, which also gave the augmented, doubly robust form. Hirano, Imbens and Ridder (2003) showed that weighting by an estimated propensity score can be efficient. Lunceford and Davidian (2004) compared weighting with stratification and gave sandwich variances, and Crump, Hotz, Imbens and Mitnik (2009) gave a rule for trimming units with poor overlap.

## References
