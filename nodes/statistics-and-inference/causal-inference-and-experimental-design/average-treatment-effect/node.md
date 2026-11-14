---
tag: 8JF2FH
kind: definition
slug: average-treatment-effect
name: Average treatment effect
aliases:
- ATE
area: statistics-and-inference/causal-inference-and-experimental-design
level: intro
summary: The mean over a population of the difference between the outcome under treatment and under control. The ATT averages only over the treated units.
prereqs: [potential-outcomes-framework, sutva]
see_also: [ignorability, randomized-experiment, inverse-probability-weighting, propensity-score-matching, augmented-inverse-probability-weighting, local-average-treatment-effect, simpsons-paradox, double-machine-learning]
sources:
  - paper: doi:10.1214/ss/1177012031
    title: Jerzy Splawa-Neyman, D. M. Dabrowska and T. P. Speed, On the application of probability theory to agricultural experiments, essay on principles, Section 9, Statistical Science 5(4), 1990
    locator: pp. 465 to 472 (the mean of the potential yields of a variety over all plots, and the difference of two such means)
  - paper: doi:10.1037/h0037350
    title: Donald B. Rubin, Estimating causal effects of treatments in randomized and nonrandomized studies, Journal of Educational Psychology 66(5), 1974
    locator: pp. 688 to 701 (the average causal effect over a set of units)
  - book: isbn:9780521885881
    title: Guido W. Imbens and Donald B. Rubin, Causal Inference for Statistics, Social, and Biomedical Sciences, Cambridge University Press, 2015
    locator: Section 1.10 (finite sample, population, treated and conditional causal estimands)
  - book: isbn:9781420076165
    title: Miguel A. Hernán and James M. Robins, Causal Inference, What If, Chapman and Hall/CRC, 2020
    locator: Chapter 1 (the average causal effect, effect measures and their scales; general locator)
  - paper: doi:10.1080/01621459.1986.10478354
    title: Paul W. Holland, Statistics and causal inference, Journal of the American Statistical Association 81(396), 1986
    locator: pp. 945 to 960 (the average causal effect as the statistical solution to the fundamental problem)
---

The average treatment effect, ATE, is the mean of the unit-level effects $Y_i(1) - Y_i(0)$ over a population. No unit effect can ever be observed, because each unit shows only one of its two [potential outcomes](/potential-outcomes-framework/). The average is different: it equals $\mathbb{E}[Y(1)] - \mathbb{E}[Y(0)]$, a difference of two means, and each mean can be learned from the units that got that treatment if the assignment is random or ignorable. This is why most of causal inference targets averages. The average treatment effect on the treated, ATT, is the same average taken over the treated units only.

## Definition

Assume [SUTVA](/sutva/), so each unit $i$ has two potential outcomes $Y_i(1)$ and $Y_i(0)$ with real values, and let $\tau_i = Y_i(1) - Y_i(0)$.

- The **sample average treatment effect** of $n$ fixed units is $\tau_S = \frac1n\sum_{i=1}^n \tau_i$.
- If $(Y(0), Y(1))$ has a distribution over a population with finite means, the **population average treatment effect** is $\tau = \mathbb{E}[Y(1) - Y(0)]$.
- For covariates $X$ fixed before treatment, the **conditional average treatment effect** is $\tau(x) = \mathbb{E}[Y(1) - Y(0) \mid X = x]$, and $\tau = \mathbb{E}[\tau(X)]$.

Because expectation is linear, $\tau = \mathbb{E}[Y(1)] - \mathbb{E}[Y(0)]$. So the ATE depends only on the two marginal distributions, of $Y(1)$ and of $Y(0)$, and not on how they are paired within units. This is the property that makes it identifiable. When the outcome is binary, $\tau$ is the causal risk difference $\Pr[Y(1) = 1] - \Pr[Y(0) = 1]$.

The ATE is a property of the science, not of a data set. It is *identified* when it can be written as a function of the law of the observed data $(X, T, Y)$:

- under randomization, $T \perp (Y(0), Y(1))$, and then $\tau = \mathbb{E}[Y \mid T = 1] - \mathbb{E}[Y \mid T = 0]$;
- under [ignorability](/ignorability/) given $X$ with overlap $0 < \Pr[T = 1 \mid X] < 1$, and then $\tau = \mathbb{E}\big[\mathbb{E}[Y \mid T = 1, X] - \mathbb{E}[Y \mid T = 0, X]\big]$.

Estimation from a sample is a separate step. The [randomized experiment](/randomized-experiment/) page proves that the difference in means is unbiased for $\tau_S$ under complete randomization, and [inverse probability weighting](/inverse-probability-weighting/), [propensity score matching](/propensity-score-matching/) and [augmented inverse probability weighting](/augmented-inverse-probability-weighting/) estimate the second formula.

**Variants: the effect on the treated and on the controls.** The average treatment effect on the treated is $\tau_{\mathrm{ATT}} = \mathbb{E}[Y(1) - Y(0) \mid T = 1]$, and the effect on the controls is $\tau_{\mathrm{ATC}} = \mathbb{E}[Y(1) - Y(0) \mid T = 0]$. In a sample, $\tau_{\mathrm{SATT}}$ is the mean of $\tau_i$ over the units with $T_i = 1$. The ATT answers "what did the treatment do for those who got it", which is the question for a program already in place. The ATE answers "what would treating everyone do".

**Relation to the ATE.** Let $p = \Pr[T = 1]$ with $0 < p < 1$. Then
$$\tau = p\,\tau_{\mathrm{ATT}} + (1 - p)\,\tau_{\mathrm{ATC}}.$$
*Proof.* By the law of total expectation, $\mathbb{E}[\tau_i] = \Pr[T = 1]\,\mathbb{E}[\tau_i \mid T = 1] + \Pr[T = 0]\,\mathbb{E}[\tau_i \mid T = 0]$. $\square$

So $\tau - \tau_{\mathrm{ATT}} = (1 - p)(\tau_{\mathrm{ATC}} - \tau_{\mathrm{ATT}})$, and the ATT equals the ATE exactly when the ATT equals the ATC. In the six-unit science table of the examples below, with units 3, 4 and 6 treated, $\tau_{\mathrm{SATT}} = (0 + 3 + 0)/3 = 1$, the effect on the controls is $(2 + 4 + 3)/3 = 3$, and $\tau_S = \frac12 \cdot 1 + \frac12 \cdot 3 = 2$.

**When the ATT equals the ATE.** Three common cases:

- the effect is constant, $\tau_i = c$ for all units;
- the treatment is independent of the effect, as in a randomized experiment, where $T \perp (Y(0), Y(1))$ gives $\mathbb{E}[\tau_i \mid T = 1] = \mathbb{E}[\tau_i]$;
- under ignorability given $X$, $\tau_{\mathrm{ATT}} = \mathbb{E}[\tau(X) \mid T = 1]$ and $\tau = \mathbb{E}[\tau(X)]$, so they agree when $\tau(x)$ does not vary with $x$, or when $X$ has the same law in both groups.

In observational data, the treated are usually selected for reasons linked to the gain, and the two differ.

**Weaker assumptions for the ATT.** The ATT needs only half of ignorability. Since $\mathbb{E}[Y(1) \mid T = 1] = \mathbb{E}[Y \mid T = 1]$ is observed, only $\mathbb{E}[Y(0) \mid T = 1]$ must be identified. If $Y(0) \perp T \mid X$ and $\Pr[T = 1 \mid X] < 1$, then
$$\mathbb{E}[Y(0) \mid T = 1] = \mathbb{E}\big[\mathbb{E}[Y(0) \mid T = 1, X] \mid T = 1\big] = \mathbb{E}\big[\mathbb{E}[Y \mid T = 0, X] \mid T = 1\big],$$
using the tower rule, then ignorability for $Y(0)$, then consistency on the controls. Every treated covariate value needs controls nearby, but untreated values need no treated units. This is why [propensity score matching](/propensity-score-matching/) of each treated unit to controls estimates the ATT.

**Other averages.** The *conditional* effect $\tau(x)$ is the target when effects differ across groups and treatment decisions depend on $x$. The *local* average treatment effect, on the [local average treatment effect](/local-average-treatment-effect/) page, averages over the compliers, the units whose treatment follows a randomized instrument; it is what [instrumental variables estimation](/instrumental-variables-estimation/) identifies when ignorability fails.

## Examples and non-examples

**Example: a science table.** Six units have $Y(0) = (3, 2, 5, 4, 1, 6)$ and $Y(1) = (5, 6, 5, 7, 4, 6)$, so $\tau = (2, 4, 0, 3, 3, 0)$ and $\tau_S = 12/6 = 2$. The mean of $Y(1)$ is $33/6$ and the mean of $Y(0)$ is $21/6$, and their difference is also 2, as linearity says.

**Non-example: the median effect.** The median of the unit effects $(0, 0, 2, 3, 3, 4)$ is $2.5$. The median of $Y(1)$ is $5.5$ and the median of $Y(0)$ is $3.5$, so the difference of the medians is $2$. The median is not linear, so the median of the differences is not the difference of the medians. The second is identified from the two marginals, but the first is not: it depends on how the outcomes pair up within units, which no data show. The [potential outcomes framework](/potential-outcomes-framework/) page gives two science tables with the same marginals and different unit effects.

**Non-example: the naive difference.** In the table, treat units 3, 4 and 6. The observed means are 6 for the treated and 2 for the controls, so the naive difference is 4, not 2. It splits as $4 = 1 + 3$: an effect of 1 on the treated plus a selection bias of 3, because the treated units would have done better without treatment ($Y(0)$ mean 5 against 2). The naive difference estimates the ATE only when the assignment does not depend on the potential outcomes. Here it is not even the ATT, which is 1.

**Non-example: the odds ratio is not an average effect.** Take a binary outcome and a binary covariate $X$, with $\Pr[X = 1] = 1/2$ and no confounding. In stratum $X = 0$, $\Pr[Y(0) = 1] = 1/2$ and $\Pr[Y(1) = 1] = 4/5$. In stratum $X = 1$, these are $1/5$ and $1/2$. In both strata the risk difference is $3/10$ and the odds ratio is $4$. Over the population, $\Pr[Y(0) = 1] = 7/20$ and $\Pr[Y(1) = 1] = 13/20$, so the risk difference is $3/10$ again, but the odds ratio is $(13/7)/(7/13) = 169/49 \approx 3.45$, smaller than in every stratum. The risk difference is an average of unit differences, so it averages over strata; the odds ratio is not, so the marginal and the conditional odds ratios differ even without confounding. This is called non-collapsibility.

## Related definitions

- [Potential outcomes framework](/potential-outcomes-framework/): the model in which unit effects and their averages are defined.
- [SUTVA](/sutva/): needed so that $Y_i(1)$ and $Y_i(0)$ are single numbers.
- [Ignorability](/ignorability/): the assumption under which the ATE is identified from observational data.
- [Randomized experiment](/randomized-experiment/): the design under which the difference in means is unbiased for the ATE.
- [Simpson's paradox](/simpsons-paradox/): shows why a pooled difference in rates may not estimate the ATE when the groups differ in a confounder.
- [Local average treatment effect](/local-average-treatment-effect/): the average over compliers.

## References
