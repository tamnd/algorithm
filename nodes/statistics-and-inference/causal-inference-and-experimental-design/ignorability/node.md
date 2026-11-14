---
tag: 39SR07
kind: definition
slug: ignorability
name: Ignorability
aliases:
- unconfoundedness
- conditional exchangeability
- no unmeasured confounding
area: statistics-and-inference/causal-inference-and-experimental-design
level: core
summary: Treatment is independent of the potential outcomes given the covariates. With overlap, it lets observational data identify causal effects.
prereqs: [potential-outcomes-framework, average-treatment-effect, conditional-expectation]
see_also: [propensity-score, inverse-probability-weighting, backdoor-criterion, missing-data-mechanism, rosenbaum-sensitivity-analysis, instrumental-variables-estimation, difference-in-differences, structural-causal-model]
sources:
  - paper: doi:10.1093/biomet/70.1.41
    title: Paul R. Rosenbaum and Donald B. Rubin, The central role of the propensity score in observational studies for causal effects, Biometrika 70(1), 1983
    locator: pp. 41 to 55 (the definition of strongly ignorable treatment assignment)
  - paper: doi:10.1214/aos/1176344064
    title: Donald B. Rubin, Bayesian inference for causal effects, the role of randomization, The Annals of Statistics 6(1), 1978
    locator: pp. 34 to 58 (ignorable assignment mechanisms)
  - paper: doi:10.1093/biomet/87.3.706
    title: Guido W. Imbens, The role of the propensity score in estimating dose-response functions, Biometrika 87(3), 2000
    locator: pp. 706 to 710 (weak unconfoundedness, one potential outcome at a time)
  - book: isbn:9780521885881
    title: Guido W. Imbens and Donald B. Rubin, Causal Inference for Statistics, Social, and Biomedical Sciences, Cambridge University Press, 2015
    locator: Chapter 3 (assignment mechanisms, individualistic, probabilistic and unconfounded) and Chapter 12 (unconfounded treatment assignment)
  - book: isbn:9781420076165
    title: Miguel A. Hernán and James M. Robins, Causal Inference, What If, Chapman and Hall/CRC, 2020
    locator: Chapter 3 (exchangeability, positivity and consistency in observational studies) and Chapter 7 (confounding; general locator)
  - book: isbn:9780521895606
    title: Judea Pearl, Causality, Models, Reasoning, and Inference, second edition, Cambridge University Press, 2009
    locator: Chapter 3 (the back-door criterion and the adjustment formula)
---

Ignorability is the assumption that, among units with the same covariates, who got the treatment has nothing to do with how they would respond to either treatment. It says that the data came from a randomized experiment run separately at each covariate value, with probabilities that may be unknown. Together with overlap, it identifies the [average treatment effect](/average-treatment-effect/) from observational data, and it is the assumption behind [inverse probability weighting](/inverse-probability-weighting/), [propensity score matching](/propensity-score-matching/) and regression adjustment. Rubin (1978) defined ignorable assignment, and Rosenbaum and Rubin (1983) gave the form used today. It cannot be tested from the data, so a study that relies on it must argue for it from knowledge of how treatment was chosen.

## Definition

Work in the [potential outcomes framework](/potential-outcomes-framework/) with [SUTVA](/sutva/): each unit has covariates $X$, measured before treatment, a binary treatment $T$, potential outcomes $Y(0)$ and $Y(1)$, and observed outcome $Y = TY(1) + (1 - T)Y(0)$. Let $e(x) = \Pr[T = 1 \mid X = x]$.

- **Strong ignorability** (Rosenbaum and Rubin, 1983) is the pair of conditions
$$(Y(0), Y(1)) \perp T \mid X \qquad\text{and}\qquad 0 < e(X) < 1 \text{ with probability 1}.$$
The first is *unconfoundedness* and the second is *overlap* or *positivity*.
- **Weak unconfoundedness** (Imbens, 2000) asks only $Y(t) \perp T \mid X$ for each $t$ separately, not for the pair. It is enough for every result on this page.
- **Mean ignorability** asks only $\mathbb{E}[Y(t) \mid T, X] = \mathbb{E}[Y(t) \mid X]$ for each $t$. It is enough to identify means.

In the finite population setting, Rubin's *ignorable* assignment mechanism is one with $\Pr[T = t \mid X, Y(0), Y(1)] = \Pr[T = t \mid X]$. The names conditional exchangeability (Hernán and Robins) and no unmeasured confounding say the same thing.

**Identification.** Under weak unconfoundedness, overlap and consistency, for $t \in \{0, 1\}$,
$$\mathbb{E}[Y(t)] = \mathbb{E}\big[\mathbb{E}[Y \mid T = t, X]\big] = \mathbb{E}\Big[\frac{\mathbf{1}[T = t]\,Y}{\Pr[T = t \mid X]}\Big].$$
*Proof.* By the tower rule, $\mathbb{E}[Y(t)] = \mathbb{E}\big[\mathbb{E}[Y(t) \mid X]\big]$. Overlap makes $\Pr[T = t \mid X] > 0$, so the conditional mean given $T = t$ and $X$ is defined. By unconfoundedness, $\mathbb{E}[Y(t) \mid X] = \mathbb{E}[Y(t) \mid T = t, X]$. On the event $T = t$, consistency gives $Y(t) = Y$, so this is $\mathbb{E}[Y \mid T = t, X]$. For the second form, $\mathbb{E}\big[\mathbf{1}[T = t]Y \mid X\big] = \mathbb{E}\big[\mathbf{1}[T = t]Y(t) \mid X\big] = \Pr[T = t \mid X]\,\mathbb{E}[Y(t) \mid X]$, by consistency and then unconfoundedness; divide by $\Pr[T = t \mid X]$ and take expectations. $\square$

So $\tau = \mathbb{E}\big[\mathbb{E}[Y \mid T = 1, X] - \mathbb{E}[Y \mid T = 0, X]\big]$, the adjustment formula. For the effect on the treated, $Y(0) \perp T \mid X$ and $e(X) < 1$ suffice, as the [average treatment effect](/average-treatment-effect/) page shows.

**What can be checked.** Unconfoundedness is not testable. The data fix the law of $(X, T, Y)$, which says nothing about $Y(0)$ among the treated or $Y(1)$ among the controls. For any law of the observed data, and any choice of $\mathbb{E}[Y(0) \mid T = 1, X]$, there is a joint law of $(X, T, Y(0), Y(1))$ that gives those observed data, so the data cannot tell an ignorable mechanism from one that is not. Overlap is about observed quantities, so it can be checked, in part, by estimating $e(x)$ and looking for values near 0 or 1. Indirect checks exist: an outcome measured before treatment, or a *negative control* outcome that the treatment cannot affect, should show no effect under the adjustment. A pass makes ignorability more plausible but does not prove it. [Rosenbaum sensitivity analysis](/rosenbaum-sensitivity-analysis/) asks how strong a failure would have to be to change the conclusion.

## Examples and non-examples

**Example: treatment by severity.** Patients are mild or severe with probability $1/2$ each. Doctors treat a mild patient with probability $1/4$ and a severe one with probability $3/4$, and nothing else enters the choice. The recovery rate of mild patients is $0.6$ untreated and $0.8$ treated, and of severe patients $0.1$ untreated and $0.4$ treated. Given severity, treatment is a coin toss, so ignorability given severity holds by construction, and overlap holds since $1/4$ and $3/4$ are inside $(0, 1)$. The treated are three quarters severe, so the raw recovery rates are $\frac14 \cdot 0.8 + \frac34 \cdot 0.4 = 0.5$ for the treated and $\frac34 \cdot 0.6 + \frac14 \cdot 0.1 = 0.475$ for the controls: a naive difference of $0.025$. The adjustment formula gives $\frac12(0.8 - 0.6) + \frac12(0.4 - 0.1) = 0.25$, the true effect. The [structural causal model](/structural-causal-model/) page uses the same numbers.

**Example: a randomized experiment.** If $T$ is assigned by a coin with a known probability, then $T \perp (Y(0), Y(1))$ with no covariates at all, and also given any pre-treatment $X$. A stratified experiment with probabilities that differ by stratum is ignorable given the strata, but not marginally.

**Non-example: an unmeasured confounder.** In the example above, suppose severity is not recorded. Treatment is not independent of $Y(0)$ any more, because severe patients are both more often treated and less likely to recover untreated. Ignorability given the empty set of covariates fails, and the naive $0.025$ is far from $0.25$. Ignorability is always relative to a set $X$: it holds given severity and fails without it.

**Non-example: adjusting for a variable after treatment.** Let $M$ be a blood marker that the treatment changes and that also affects recovery. Conditioning on $M$ compares treated and untreated patients with the same marker, so part of the treatment's effect is removed, and the formula no longer gives $\mathbb{E}[Y(1)] - \mathbb{E}[Y(0)]$. Covariates in $X$ must be fixed before treatment.

**Non-example: adjusting for a collider.** Suppose $X$ is a pre-treatment variable caused by two unmeasured variables, one that affects treatment and one that affects outcome, and neither affects the other's target. Without $X$, treatment and potential outcomes are independent. Conditioning on $X$ makes the two unmeasured causes dependent, and so it breaks ignorability that held without it. In graph terms, $X$ opens a path that was blocked; the [back-door criterion](/backdoor-criterion/) and [d-separation](/d-separation/) say which sets are safe. Adding covariates does not always help.

**Non-example: no overlap.** If doctors always treat severe patients, $e(\text{severe}) = 1$, and no severe control exists. Unconfoundedness may hold, but $\mathbb{E}[Y(0) \mid \text{severe}]$ is not identified, and the ATE is not either. The effect on the mild patients still is.

## Related definitions

- [Propensity score](/propensity-score/): if ignorability holds given $X$, it holds given the single number $e(X)$.
- [SUTVA](/sutva/) and the [average treatment effect](/average-treatment-effect/): the other assumption and the estimand of the identification result.
- [Missing-data mechanism](/missing-data-mechanism/): with $T$ as the indicator of which potential outcome is seen, ignorability is the causal form of missing at random.
- [Back-door criterion](/backdoor-criterion/): a graphical condition on $X$ under which ignorability given $X$ holds in a [structural causal model](/structural-causal-model/).
- [Instrumental variables estimation](/instrumental-variables-estimation/), [difference-in-differences](/difference-in-differences/) and the [regression discontinuity design](/regression-discontinuity-design/): designs that replace ignorability by other assumptions when confounders are not measured.
- [Rosenbaum sensitivity analysis](/rosenbaum-sensitivity-analysis/): a bound on how a given departure from ignorability can change a test.

## References
