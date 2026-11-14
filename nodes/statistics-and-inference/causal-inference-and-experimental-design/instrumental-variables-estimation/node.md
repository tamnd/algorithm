---
tag: CM6TM9
kind: technique
slug: instrumental-variables-estimation
name: Instrumental variables estimation
aliases:
- IV estimation
- instrumental variable method
area: statistics-and-inference/causal-inference-and-experimental-design
level: core
summary: Identifies a causal effect under unmeasured confounding with a variable that moves the treatment but affects the outcome only through it.
prereqs: [potential-outcomes-framework, randomized-experiment, regression-f-test]
see_also: [two-stage-least-squares, local-average-treatment-effect, instrumental-variable-identification, generalized-method-of-moments, fieller-theorem, test-interval-duality, errors-in-variables-regression, regression-discontinuity-design]
sources:
  - paper: "Philip G. Wright, The Tariff on Animal and Vegetable Oils, Macmillan, New York, 1928"
    title: Philip G. Wright, The Tariff on Animal and Vegetable Oils, Macmillan, 1928
    locator: Appendix B (the first instrumental variables estimates of supply and demand elasticities; cited from Stock and Trebbi 2003)
  - paper: doi:10.1257/089533003769204416
    title: James H. Stock and Francesco Trebbi, Retrospectives, who invented instrumental variable regression?, Journal of Economic Perspectives 17(3), 2003
    locator: pp. 177 to 194 (the history of Wright's Appendix B and of the method)
  - paper: doi:10.1214/aoms/1177730090
    title: T. W. Anderson and Herman Rubin, Estimation of the parameters of a single equation in a complete system of stochastic equations, The Annals of Mathematical Statistics 20(1), 1949
    locator: pp. 46 to 63 (the limited information estimator and the test of the coefficients that does not depend on the strength of the instruments)
  - paper: doi:10.2307/2171753
    title: Douglas Staiger and James H. Stock, Instrumental variables regression with weak instruments, Econometrica 65(3), 1997
    locator: the article starting on p. 557 (weak-instrument asymptotics, bias toward OLS, size distortion of Wald tests)
  - paper: doi:10.2307/2937954
    title: Joshua D. Angrist and Alan B. Krueger, Does compulsory school attendance affect schooling and earnings?, The Quarterly Journal of Economics 106(4), 1991
    locator: pp. 979 to 1014 (quarter of birth as an instrument for schooling)
  - paper: doi:10.2307/2951620
    title: Guido W. Imbens and Joshua D. Angrist, Identification and estimation of local average treatment effects, Econometrica 62(2), 1994
    locator: the article starting on p. 467 (what the ratio identifies when effects vary)
  - book: isbn:9780691120355
    title: Joshua D. Angrist and Jörn-Steffen Pischke, Mostly Harmless Econometrics, Princeton University Press, 2009
    locator: Chapter 4, Instrumental Variables in Action (general locator, the section numbers were not checked)
---

Instrumental variables estimation recovers the causal effect of a treatment $D$ on an outcome $Y$ when unmeasured confounders affect both, so that neither a regression of $Y$ on $D$ nor any adjustment for measured covariates can remove the bias. It needs a third variable $Z$, the instrument, that moves $D$, has no path to $Y$ except through $D$, and is as good as randomly assigned. Then the effect of $Z$ on $Y$ is the effect of $Z$ on $D$ times the effect of $D$ on $Y$, and the effect of $D$ on $Y$ is the ratio of two estimable effects: $\beta = \operatorname{Cov}(Z, Y)/\operatorname{Cov}(Z, D)$, which for a binary instrument is the Wald ratio of the differences in means. The technique is the identification argument; [two-stage least squares](/two-stage-least-squares/) is the estimator that carries it to several instruments and covariates. With effects that vary across units, the ratio is the [local average treatment effect](/local-average-treatment-effect/) of the units the instrument moves. With weak instruments the ratio is badly behaved, and the Anderson-Rubin test gives confidence sets that stay valid.

## In plain words

Suppose we want to know whether a training course raises wages, but the people who take it are more motivated, and motivation also raises wages. Comparing takers and non-takers mixes the two. Now suppose the course was advertised by letter to a random half of the people. The letter makes taking the course more likely, and it cannot affect wages by itself.

Compare the two halves. The half that got letters took the course more often, by some amount, and earned more, by some other amount. Because the halves were formed at random, motivation is the same in both, so the extra earnings can only come through the extra course-taking. Dividing the extra earnings by the extra course-taking gives the effect of the course per person who took it because of the letter. The letter is the instrument.

## When it applies

The setting is a treatment $D$, an outcome $Y$, and unobserved $U$ that affects both. The instrument $Z$ must satisfy three conditions, written here in [potential outcomes](/potential-outcomes-framework/) $Y(d, z)$ and $D(z)$:

- **Relevance.** $Z$ changes $D$: $\operatorname{Cov}(Z, D) \ne 0$. This is testable with the first-stage regression of $D$ on $Z$.
- **Exclusion.** $Z$ affects $Y$ only through $D$: $Y(d, z) = Y(d)$ for all $d, z$. This is an assumption about the world and cannot be tested from $(Z, D, Y)$ alone with one instrument.
- **Independence.** $Z$ is as good as randomly assigned: $Z$ is independent of $(Y(d), D(z))$ for all $d, z$. It holds by design when $Z$ is randomized, and otherwise it is an assumption, often made conditional on covariates $X$.

Then two different targets are identified, under two different extra assumptions:

- **Constant effects.** If $Y = \alpha + \beta D + \varepsilon$ with the same $\beta$ for every unit and $\operatorname{Cov}(Z, \varepsilon) = 0$, then $\operatorname{Cov}(Z, Y) = \beta\operatorname{Cov}(Z, D) + \operatorname{Cov}(Z, \varepsilon) = \beta\operatorname{Cov}(Z, D)$, and relevance gives $\beta = \operatorname{Cov}(Z, Y)/\operatorname{Cov}(Z, D)$.
- **Heterogeneous effects with a binary $Z$ and $D$.** If no unit takes the treatment because the instrument is off and refuses it because it is on (monotonicity), the same ratio equals $\mathbb{E}[Y(1) - Y(0) \mid D(1) > D(0)]$, the average effect among the compliers. The [LATE theorem page](/local-average-treatment-effect/) proves this.

The technique is not needed when the treatment is randomized or when [ignorability](/ignorability/) given measured covariates is credible: then the instrument only adds variance. It does not help when no defensible instrument exists, which is the usual case.

## The template

**Identification.** The estimand is $\beta$ in the constant effect model or the complier effect under monotonicity. The identification formula is the ratio of the reduced form to the first stage,

$$\beta = \frac{\operatorname{Cov}(Z, Y)}{\operatorname{Cov}(Z, D)}, \qquad \text{for binary } Z: \quad \beta = \frac{\mathbb{E}[Y \mid Z = 1] - \mathbb{E}[Y \mid Z = 0]}{\mathbb{E}[D \mid Z = 1] - \mathbb{E}[D \mid Z = 0]}.$$

The two forms agree for a binary $Z$, because $\operatorname{Cov}(Z, V) = p(1 - p)(\mathbb{E}[V \mid Z = 1] - \mathbb{E}[V \mid Z = 0])$ for any $V$, with $p = \Pr[Z = 1]$. The sample versions agree exactly too, which the tests check with fractions.

**Estimation.** With one instrument and one treatment the steps are below. The holes are the instrument, the covariates (handled by adding them to both regressions, which is 2SLS), and the level $\alpha$.

```pseudo id=main
INSTRUMENT-ANALYSIS(Y, D, Z, α)                      ▷ one treatment, one instrument, n units
L1  first stage: slope π̂ of D on (1, Z) and its F statistic F₁
L2  reduced form: slope ρ̂ of Y on (1, Z)
L3  β̂ ← ρ̂ / π̂                                ▷ = s_ZY / s_ZD; the Wald ratio for binary Z
L4  residuals Y - ȳ - β̂ (D - d̄); σ̂² ← their sum of squares / (n - 2); se ← σ̂ √s_ZZ / |s_ZD|
L5  AR set ← {b : F statistic of Z in the regression of Y - b D on (1, Z) ≤ F_{1, n-2, 1-α}}
L6  return (β̂, se, F₁, AR set)
```

Here $s_{ZY} = \sum_i(Z_i - \bar z)(Y_i - \bar y)$ and so on. The estimate $\hat\beta$ is consistent when the three conditions hold and $\operatorname{Cov}(Z, D) \ne 0$, and $\hat\beta \pm t\,\mathrm{se}$ is a valid large-sample interval when the instrument is strong. Both fail together when the instrument is weak.

**The Anderson-Rubin set.** The Anderson-Rubin (AR) test of Line L5 tests each value $b$ by asking whether $Z$ predicts $Y - bD$. Under $\beta = b$, $Y - bD = \alpha + \varepsilon$ does not depend on $Z$, so with normal errors independent of $Z$ the statistic

$$\mathrm{AR}(b) = (n - 2)\frac{r_b^2}{1 - r_b^2}, \qquad r_b = \operatorname{corr}(Z, Y - bD),$$

has exactly the $F_{1, n - 2}$ law, whatever the value of $\operatorname{Cov}(Z, D)$. Without normality it is still asymptotically valid. The set of $b$ not rejected is found in closed form. With $c(b) = s_{ZY} - b\,s_{ZD}$, $s_{ww}(b) = s_{YY} - 2b\,s_{YD} + b^2s_{DD}$ and $q = F_{1, n - 2, 1 - \alpha}$, the condition $\mathrm{AR}(b) \le q$ is

$$c(b)^2 - \kappa\,s_{ZZ}\,s_{ww}(b) \le 0, \qquad \kappa = \frac{q}{n - 2 + q},$$

a quadratic inequality in $b$ with leading coefficient $s_{ZD}^2 - \kappa s_{ZZ}s_{DD}$. That coefficient is positive exactly when the first-stage statistic $F_1 = (n - 2)r_{ZD}^2/(1 - r_{ZD}^2)$ exceeds $q$, since both say $r_{ZD}^2 > \kappa$. So the set is a bounded interval if and only if the first stage is significant at level $\alpha$, and otherwise it is the complement of an interval or the whole line. An unbounded set is the honest answer when the data cannot tell the effect apart from infinity: as $b \to \pm\infty$, $\mathrm{AR}(b) \to F_1$. When it is an interval, it contains $\hat\beta$, where $c = 0$. This is the test-inversion of [test-interval duality](/test-interval-duality/), and the shapes are those of [Fieller's](/fieller-theorem/) set for a ratio, for the same reason. The tests check the closed form against a grid of 801 values of $b$ and check the bounded-if-and-only-if-significant rule.

**Worked example.** Eight units, the same data as on the 2SLS page:

| $Z$ | $D$ | $Y$ |
| --- | --- | --- |
| 0 | 0, 0, 0, 1 | 1, 2, 3, 6 |
| 1 | 1, 1, 1, 0 | 5, 6, 4, 2 |

The centred sums are $s_{ZZ} = 2$, $s_{ZD} = 1$, $s_{ZY} = 5/2$, $s_{DD} = 2$, $s_{YD} = 13/2$, $s_{YY} = 207/8$. So $\hat\beta = (5/2)/1 = 5/2$, which is also $(17/4 - 3)/(3/4 - 1/4)$. The residual sum of squares is $207/8 - 2 \cdot \frac52 \cdot \frac{13}{2} + \frac{25}{4} \cdot 2 = 47/8$, so $\hat\sigma^2 = 47/48$ and $\mathrm{se} = \sqrt{47/48 \cdot 2}/1 = 1.40$; the usual 95% interval with $t_{6} = 2.447$ is $(-0.92, 5.92)$. But the first stage is weak: $r_{ZD}^2 = 1/4$, so $F_1 = 6 \cdot \frac{1/4}{3/4} = 2$, far below $F_{1, 6, 0.95} = 5.99$. The 95% Anderson-Rubin set is the whole real line: no value of the effect can be rejected, and the $t$ interval was false comfort. At level $\alpha = 0.30$, where $q = 1.27 < 2$, the set is the interval $(-2.51, 3.91)$. For $b = 0$, $\mathrm{AR}(0) = 6 \cdot (5/2)^2/(2 \cdot 207/8 - 25/4) = 75/91$.

**Simulation.** $Y = D + \varepsilon$, $D = \pi Z + v$, $\operatorname{corr}(\varepsilon, v) = 0.8$, $n = 50$, 2000 samples each, all numbers measured:

| first-stage $\pi$ | AR rejects $\beta = 1$ | $t$ test rejects $\beta = 1$ | AR set bounded | median of $\hat\beta$ | mean of OLS |
| --- | --- | --- | --- | --- | --- |
| 0.05 | 0.052 | 0.121 | 0.06 | 1.715 | 1.800 |
| 0.3 | 0.048 | 0.090 | 0.53 | 1.019 | 1.734 |
| 1.0 | 0.050 | 0.046 | 1.00 | 1.001 | 1.400 |

The AR test keeps its 5% size in every row. With a weak instrument the ratio estimate sits near OLS and the $t$ test rejects a true value two to three times too often.

## Classic examples

- **Supply and demand.** Wright (1928), in Appendix B of a book on the tariff on animal and vegetable oils, estimated the elasticities of supply and demand for butter and flaxseed. Price and quantity are set together by both curves, so a regression of one on the other estimates neither. A variable that shifts supply only, such as yield per acre, traces out the demand curve, and one that shifts demand only traces out supply. Stock and Trebbi (2003) describe the history.
- **Quarter of birth and schooling.** Angrist and Krueger (1991) noted that compulsory schooling laws let students leave at an age, not at a grade, so those born early in the year can leave with slightly less schooling. Quarter of birth is the instrument for years of schooling in a wage equation. The study is also the standard warning about weak and many instruments (Bound, Jaeger and Baker 1995, on the [2SLS page](/two-stage-least-squares/)).
- **Randomized trials with noncompliance.** Assignment to treatment is a randomized instrument for the treatment actually received. The ratio of the intention-to-treat effect on the outcome to its effect on uptake is the effect among compliers.
- **Draft lottery.** The Vietnam-era draft lottery numbers were random and changed the chance of military service; Angrist used them to estimate the effect of service on later earnings.
- **Mendelian randomization.** Genetic variants that affect an exposure, such as a variant that changes alcohol tolerance, are assigned at conception, roughly at random given the parents' genes. The exclusion restriction fails if the variant has other effects (pleiotropy).
- **Measurement error.** If $D$ is measured with error, a second independent measurement of the same quantity is an instrument for the first, and removes the attenuation bias of [errors in variables](/errors-in-variables-regression/).

## Variations

- **Several instruments and covariates.** Use [two-stage least squares](/two-stage-least-squares/), or efficient [GMM](/generalized-method-of-moments/) with heteroskedastic errors. Extra instruments allow Sargan's test of overidentifying restrictions.
- **Limited information maximum likelihood.** Anderson and Rubin (1949): less biased than 2SLS with weak or many instruments; with one instrument it equals the ratio estimate.
- **Weak-instrument-robust tests.** With several instruments the AR test loses power because its degrees of freedom grow with the number of instruments; the conditional likelihood ratio test of Moreira and the K test of Kleibergen keep the size with better power.
- **Control function.** Add the first-stage residual to the outcome regression. In linear models this equals 2SLS; in nonlinear models it is a different estimator with its own assumptions.
- **Conditional instruments.** If $Z$ is random only given covariates $X$, add $X$ to both stages, or weight by the instrument propensity score (Abadie's kappa weighting).
- **Fuzzy regression discontinuity.** Crossing a cutoff is an instrument for the treatment near the cutoff; the estimate is a ratio of two jumps. See the [regression discontinuity page](/regression-discontinuity-design/).
- **System identification.** Control engineering uses the same idea to estimate a dynamic model from noisy data, with delayed inputs as instruments: see [instrumental variable identification](/instrumental-variable-identification/).

## Pitfalls

- **Defending the exclusion restriction with data.** With one instrument it cannot be tested. A balance table of covariates across instrument values supports independence, not exclusion.
- **Weak instruments.** A first-stage $F$ below about 10 makes the ratio biased toward OLS and the $t$ interval too narrow. Report the first stage and use the AR set.
- **Ignoring heterogeneity.** With varying effects, the estimate is the effect for compliers, who may be a small and unusual group. Two valid instruments can give two different answers, and neither is the average effect over everyone.
- **Defiers.** If some units do the opposite of what the instrument pushes, the ratio is a difference of complier and defier effects and can even have the wrong sign.
- **Small first stage in a large sample.** A significant first stage with a tiny effect on $D$ means that a tiny direct effect of $Z$ on $Y$ (a small violation of exclusion) is divided by a tiny number and becomes a large bias.
- **Reading the reduced form as the effect.** The reduced form $\mathbb{E}[Y \mid Z = 1] - \mathbb{E}[Y \mid Z = 0]$ is the effect of the instrument (the intention-to-treat effect), not of the treatment; it is smaller by the factor $\mathbb{E}[D \mid Z = 1] - \mathbb{E}[D \mid Z = 0]$.

## Exercises

1. Show that for a binary $Z$ with $p = \Pr[Z = 1]$, $\operatorname{Cov}(Z, V) = p(1 - p)(\mathbb{E}[V \mid Z = 1] - \mathbb{E}[V \mid Z = 0])$, and conclude that the covariance ratio is the Wald ratio.
   <details><summary>Answer</summary>$\operatorname{Cov}(Z, V) = \mathbb{E}[ZV] - p\,\mathbb{E}[V] = p\,\mathbb{E}[V \mid Z = 1] - p(p\,\mathbb{E}[V \mid Z = 1] + (1 - p)\mathbb{E}[V \mid Z = 0]) = p(1 - p)(\mathbb{E}[V \mid Z = 1] - \mathbb{E}[V \mid Z = 0])$. The factor $p(1 - p)$ cancels in the ratio.</details>
2. In a trial, 40% of those assigned to treatment take it and 5% of those assigned to control get it anyway. The mean outcome is 12.0 in the assigned group and 11.3 in the control group. What is the ratio estimate, and what does it estimate?
   <details><summary>Answer</summary>$0.7/0.35 = 2.0$. Under monotonicity it is the average effect among the 35% of units who take the treatment if and only if assigned to it.</details>
3. Suppose $Z$ has a direct effect $\gamma$ on $Y$, so $Y = \alpha + \beta D + \gamma Z + \varepsilon$. Show that the ratio tends to $\beta + \gamma\operatorname{Var}(Z)/\operatorname{Cov}(Z, D)$, and explain why a weak instrument makes a small $\gamma$ dangerous.
   <details><summary>Answer</summary>$\operatorname{Cov}(Z, Y) = \beta\operatorname{Cov}(Z, D) + \gamma\operatorname{Var}(Z) + \operatorname{Cov}(Z, \varepsilon)$ and the last term is 0, so the ratio of the sample covariances tends to $\beta + \gamma\operatorname{Var}(Z)/\operatorname{Cov}(Z, D)$. A weak instrument has a small $\operatorname{Cov}(Z, D)$, so the bias term is a small $\gamma$ divided by a small number and can be large.</details>
4. Show that $\mathrm{AR}(b) \to F_1$ as $b \to \pm\infty$.
   <details><summary>Answer</summary>$Y - bD = -b(D - Y/b)$, and the correlation is unchanged by the factor $-b$, so $r_b^2 \to \operatorname{corr}(Z, D)^2 = r_{ZD}^2$.</details>
5. Use the code to find the smallest $\alpha$ at which the AR set of the worked example is bounded. (It is the p-value of the first-stage $F$ test, $\Pr[F_{1, 6} > 2] \approx 0.207$.)

## References
