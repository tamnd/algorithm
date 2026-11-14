---
tag: TY76BZ
kind: technique
slug: group-sequential-design
name: Group sequential design
aliases:
- group sequential trial
- interim analysis
area: statistics-and-inference/time-series-and-sequential-analysis
level: advanced
summary: A trial plan that analyses the data at a few interim points and may stop early, with boundaries chosen so that the overall type I error stays at alpha.
prereqs: [z-test, statistical-power, multiple-comparisons-problem]
see_also: [obrien-fleming-boundary, alpha-spending-function, sequential-probability-ratio-test, mixture-sequential-probability-ratio-test, confidence-sequence, sample-size-determination, family-wise-error-rate, numerical-integration]
sources:
  - paper: doi:10.2307/2343787
    title: P. Armitage, C. K. McPherson and B. C. Rowe, Repeated significance tests on accumulating data, Journal of the Royal Statistical Society, Series A 132(2) (1969)
    locator: the inflation of the type I error when a fixed-sample test is repeated, and the recursive numerical integration that computes it
  - paper: doi:10.1093/biomet/64.2.191
    title: Stuart J. Pocock, Group sequential methods in the design and analysis of clinical trials, Biometrika 64(2) (1977), pages 191 to 199
    locator: group sequential tests with a constant critical value and a fixed number of equally spaced analyses
  - paper: doi:10.2307/2530245
    title: Peter C. O'Brien and Thomas R. Fleming, A multiple testing procedure for clinical trials, Biometrics 35(3) (1979), pages 549 to 556
    locator: the boundary that is strict at early analyses and near the fixed-sample value at the last one
  - paper: doi:10.1093/biomet/70.3.659
    title: K. K. Gordon Lan and David L. DeMets, Discrete sequential boundaries for clinical trials, Biometrika 70(3) (1983), pages 659 to 663
    locator: the alpha spending function, which removes the need to fix the number and times of the analyses
  - book: isbn:9780849303166
    title: Christopher Jennison and Bruce W. Turnbull, Group Sequential Methods with Applications to Clinical Trials, Chapman and Hall/CRC, 2000
    locator: Chapter 2 (two-sided tests, the Pocock and O'Brien-Fleming tests and their tables of constants)
---

A group sequential design is a plan to analyse a study at a small number $K$ of planned points, called interim analyses, and to stop at the first analysis where the evidence is strong enough. Testing at the usual level at every analysis inflates the type I error, because each analysis is one more chance for noise to cross the line: five looks at the 1.96 critical value give a false positive rate of 14.2%, not 5%. A group sequential design replaces the single critical value by a boundary $c_1, \ldots, c_K$, computed from the joint normal distribution of the test statistics, so that the probability of crossing at any analysis is exactly $\alpha$. The price is a maximum sample size a few percent larger than the fixed-sample one; the gain is a smaller expected sample size when the effect is real. Pocock (1977) and O'Brien and Fleming (1979) gave the first designs for clinical trials, and Lan and DeMets (1983) made the analysis times flexible with [alpha spending](/alpha-spending-function/).

## In plain words

A medical trial takes years. If the new treatment clearly works, or clearly harms patients, it is wrong to wait until the end to find out. So an independent committee looks at the data a few times while the trial runs. But each look is a new chance to be fooled by luck. If the committee used the normal threshold every time, it would declare a false success much more often than planned. A group sequential design fixes this before the trial starts. It sets a stricter threshold for each look, so that the total chance of a false success over all looks is still the planned 5%. Common designs make the early thresholds very strict and keep the last one close to the usual value.

## When it applies

- The data arrive over time, and the number of analyses is small, usually 2 to 10, and planned in advance. With [alpha spending](/alpha-spending-function/), only the maximum information needs to be planned.
- At each analysis the test statistic is, at least approximately, a normal $Z$ statistic for one parameter $\theta$, such as a difference of means, a log hazard ratio or a log odds ratio. Then the statistics at the different analyses have the canonical joint distribution described below.
- The question is a test of $H_0: \theta = 0$, two-sided or one-sided, with a planned [power](/statistical-power/) against an effect $\delta$.
- Stopping early has a real value: ethics in a clinical trial, cost or time in an industrial experiment.

## The template

Let $\hat\theta_k$ be the estimate of $\theta$ at analysis $k$, $I_k = 1/\operatorname{Var}(\hat\theta_k)$ the information, and $Z_k = \hat\theta_k\sqrt{I_k}$ the [z statistic](/z-test/). Write $t_k = I_k/I_K$ for the information fractions.

```pseudo id=main
GROUP-SEQUENTIAL(K, α, β, δ, w_1..w_K)        ▷ shape w_k: 1/sqrt(t_k) for O'Brien-Fleming, 1 for Pocock
L1  plan information fractions 0 < t_1 < ... < t_K = 1
L2  find C with P_0(|Z_k| ≥ C·w_k for some k ≤ K) = α     ▷ recursive integration and bisection
L3  find I_max with P_δ(|Z_k| ≥ C·w_k for some k ≤ K) = 1 - β
L4  for k ← 1 to K do
L5      collect data until the information is t_k·I_max, and compute Z_k
L6      if |Z_k| ≥ C·w_k then stop and reject H_0
L7  stop and do not reject H_0
```

**The canonical joint distribution.** For normal data with known variance, the score $S_k = Z_k\sqrt{I_k}$ is a sum of the observations scaled by the variance, so it has independent normal increments:
$$S_k - S_{k-1} \sim N\bigl(\theta(I_k - I_{k-1}),\; I_k - I_{k-1}\bigr), \qquad S_0 = 0, \; I_0 = 0.$$
So $Z_k \sim N(\theta\sqrt{I_k}, 1)$ and $\operatorname{Cov}(Z_j, Z_k) = \sqrt{I_j/I_k}$ for $j \le k$. Large-sample theory gives the same joint distribution, approximately, for estimates in most regular models (Jennison and Turnbull 2000). Everything in lines L2 and L3 depends on the data only through this distribution, which is why one set of tables serves all such trials.

**Why the plain repetition fails.** Under $H_0$ the $Z_k$ are positively correlated but far from equal, so each look adds a new chance to cross. With equally spaced looks and the critical value 1.96 every time, the probability of at least one crossing is:

| looks $K$ | 1 | 2 | 3 | 5 | 10 |
|---|---|---|---|---|---|
| $P_0(\text{some } \lvert Z_k \rvert \ge 1.96)$ | 0.0500 | 0.0831 | 0.1073 | 0.1417 | 0.1934 |

It tends to 1 as $K$ grows, by the law of the iterated logarithm. This is the [multiple comparisons problem](/multiple-comparisons-problem/) for correlated statistics; a [Bonferroni correction](/bonferroni-correction/) would be valid but wastes most of the correlation.

**Line L2: recursive integration.** The probability of no crossing before analysis $k$ is an integral over the region $|S_j| < C w_j\sqrt{I_j}$, $j < k$. Because the increments are independent, the sub-density $g_k$ of $S_k$ on that region satisfies
$$g_k(s) = \int_{-b_{k-1}}^{b_{k-1}} g_{k-1}(u)\,\frac{1}{\sigma_k}\varphi\left(\frac{s - u - \theta\Delta_k}{\sigma_k}\right)du, \qquad \Delta_k = I_k - I_{k-1}, \; \sigma_k = \sqrt{\Delta_k},$$
with $b_j = C w_j\sqrt{I_j}$. Armitage, McPherson and Rowe (1969) introduced this recursion. Each step is one [numerical integration](/numerical-integration/), so the crossing probability costs $O(K m^2)$ for $m$ grid points per stage. It increases with $\theta$ away from 0 and decreases as $C$ grows, so [bisection](/bisection-method/) on $C$ finds the constant. The [O'Brien-Fleming boundary](/obrien-fleming-boundary/) page gives the algorithm and its proof.

**Line L3: the inflation factor.** A group sequential test with the same $\alpha$ and power needs more maximum information than the fixed-sample test, which needs $I_{\text{fix}} = (z_{1-\alpha/2} + z_{1-\beta})^2/\delta^2$ (see [sample size determination](/sample-size-determination/)). The ratio $R = I_{\max}/I_{\text{fix}}$ depends only on $K$, $\alpha$, $\beta$ and the shape, not on $\delta$.

**Example: five equally spaced analyses, $\alpha = 0.05$ two-sided, power 90%.** Here $(z_{0.975} + z_{0.9})^2 = 10.507$.

| | O'Brien-Fleming | Pocock |
|---|---|---|
| $z$ boundaries $c_1, \ldots, c_5$ | 4.562, 3.226, 2.634, 2.281, 2.040 | 2.413 at every look |
| $P_0$ of crossing first at look 1 to 5 | 0.00001, 0.00125, 0.00764, 0.01668, 0.02442 | 0.01581, 0.01171, 0.00902, 0.00731, 0.00615 |
| inflation factor $R$ | 1.0265 | 1.2065 |
| expected information under $\theta = \delta$, fraction of $I_{\text{fix}}$ | 0.750 | 0.685 |
| expected information under $\theta = \delta/2$ | 0.961 | 1.052 |
| expected information under $\theta = 0$ | 1.019 | 1.177 |

Both designs spend a total of 0.05. The O'Brien-Fleming design spends almost nothing early, costs only 2.7% more information at most, and saves a quarter of the information on average when the planned effect is real. The Pocock design stops earlier when the effect is large, but its maximum is 21% larger and its last critical value, 2.413, is far above 1.96.

**What is exact and what is not.** The level $\alpha$ is exact for normal data with known variance, up to the error of the quadrature, which is below $10^{-6}$ in the computations of the example. With estimated variances or with large-sample statistics it holds only approximately. The expected sample sizes are exact expectations under the canonical distribution, not simulations.

## Classic examples

- **The O'Brien-Fleming design.** The [O'Brien-Fleming boundary](/obrien-fleming-boundary/) uses $c_k = C/\sqrt{t_k}$, constant on the score scale. It is the most common design for efficacy in clinical trials, because a trial that stops early must show overwhelming evidence and the final analysis is almost unchanged.
- **The Pocock design.** Pocock (1977) used the same $c_k$ at every analysis. It is described as a variant on the [O'Brien-Fleming boundary](/obrien-fleming-boundary/) page.
- **Alpha spending.** Lan and DeMets (1983) specify the cumulative error $f(t)$ instead of the shape, and compute each $c_k$ when analysis $k$ occurs. The [alpha spending function](/alpha-spending-function/) page gives the computation and the common choices of $f$.
- **Repeated confidence intervals.** The intervals $\hat\theta_k \pm c_k/\sqrt{I_k}$ contain $\theta$ at all $K$ analyses at once with probability $1 - \alpha$. They are a [confidence sequence](/confidence-sequence/) on the $K$ planned times.
- **The continuous limit.** As $K \to \infty$ with a constant boundary on the likelihood ratio scale, the plan becomes a fully sequential test such as the [SPRT](/sequential-probability-ratio-test/) or, for an unknown effect, the [mixture SPRT](/mixture-sequential-probability-ratio-test/).

## Variations

- **One-sided tests and futility.** A one-sided design rejects for large $Z_k$ only. An inner boundary $a_k$ stops for futility when $Z_k \le a_k$. Binding futility boundaries are included in the computation of $\alpha$; nonbinding ones are ignored there, so the trial may continue past them without inflating the error.
- **Wang-Tsiatis family.** $c_k = C\,t_k^{\Delta - 1/2}$ with $0 \le \Delta \le 1/2$ joins the O'Brien-Fleming shape ($\Delta = 0$) and the Pocock shape ($\Delta = 1/2$).
- **Haybittle-Peto rule.** Use $|Z_k| \ge 3$ at every interim analysis and the plain critical value at the end. The extra error is small, and the rule is simple to explain, but the level is not exactly $\alpha$.
- **Error spending.** [Alpha spending](/alpha-spending-function/) also has a version for $\beta$, which builds futility boundaries from a planned spending of the type II error.
- **Sample size re-estimation and adaptive designs.** The information plan can be changed at an interim analysis, if the test statistic is adjusted, for example by combining the stage-wise p-values with fixed weights.

## Pitfalls

- **Looks that were not planned.** A design with fixed $K$ and $t_k$ loses its guarantee if the analyses happen at other times or more often. Use alpha spending when the timing is uncertain.
- **Estimation after stopping.** The estimate $\hat\theta_k$ at the stopping analysis is biased away from 0, because the trial stops when it is large. The naive confidence interval $\hat\theta_k \pm 1.96/\sqrt{I_k}$ is not valid. Use repeated confidence intervals or an ordering of the sample space designed for this purpose.
- **Reporting the final p-value as usual.** At the last O'Brien-Fleming analysis the critical value is 2.040, not 1.96. A trial with $|Z_5| = 2.0$ does not reject, even though the fixed-sample p-value is below 0.05.
- **Approximate normality early.** At the first analysis the information is small. Large-sample approximations for survival or binary data can be poor there, which matters most for the Pocock design that spends much of its error early.
- **Too many looks.** The plan is for a few planned looks. For continuous monitoring, a [mixture SPRT](/mixture-sequential-probability-ratio-test/) or a [confidence sequence](/confidence-sequence/) is the right tool.

## Exercises

1. For normal data with known variance $\sigma^2$, let $I_k = n_k/\sigma^2$. Show that $\operatorname{Cov}(Z_j, Z_k) = \sqrt{I_j/I_k}$ for $j \le k$.
2. With two equally spaced looks at critical value 1.96, show that the type I error is $1 - P(|Z_1| < 1.96, |Z_2| < 1.96)$ where $(Z_1, Z_2)$ is bivariate normal with correlation $\sqrt{1/2}$, and check by numerical integration that it is 0.0831.
3. Show that the O'Brien-Fleming boundary $c_k = C/\sqrt{t_k}$ is the constant $C\sqrt{I_K}$ on the score scale $S_k$.
4. Show that the inflation factor $R$ does not depend on $\delta$. Hint: write the power as a function of the drift $\delta\sqrt{I_{\max}}$ of the canonical process.

## References
