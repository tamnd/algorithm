---
tag: 3SPJK1
kind: model
slug: potential-outcomes-framework
name: Potential outcomes framework
aliases:
- Rubin causal model
- Neyman-Rubin causal model
- counterfactual outcomes
area: statistics-and-inference/causal-inference-and-experimental-design
level: intro
summary: Each unit has one outcome per treatment, of which only one is seen. Causal effects are contrasts of these potential outcomes, and causal inference is a missing data problem.
prereqs: [random-variable, conditional-expectation]
see_also: [sutva, average-treatment-effect, randomized-experiment, ignorability, structural-causal-model, missing-data-mechanism, permutation-test, horvitz-thompson-estimator]
sources:
  - paper: doi:10.1214/ss/1177012031
    title: Jerzy Splawa-Neyman, D. M. Dabrowska and T. P. Speed, On the application of probability theory to agricultural experiments, essay on principles, Section 9, Statistical Science 5(4), 1990
    locator: pp. 465 to 472 (the 1923 notation of potential yields of each plot under each variety, translated)
  - paper: doi:10.1037/h0037350
    title: Donald B. Rubin, Estimating causal effects of treatments in randomized and nonrandomized studies, Journal of Educational Psychology 66(5), 1974
    locator: pp. 688 to 701 (the causal effect for a unit as the difference of two outcomes, and its use in nonrandomized studies)
  - paper: doi:10.1214/aos/1176344064
    title: Donald B. Rubin, Bayesian inference for causal effects, the role of randomization, The Annals of Statistics 6(1), 1978
    locator: pp. 34 to 58 (the assignment mechanism and ignorable assignment)
  - paper: doi:10.1080/01621459.1986.10478354
    title: Paul W. Holland, Statistics and causal inference, Journal of the American Statistical Association 81(396), 1986
    locator: pp. 945 to 960 (the fundamental problem of causal inference and the name Rubin's model)
  - book: isbn:9780521885881
    title: Guido W. Imbens and Donald B. Rubin, Causal Inference for Statistics, Social, and Biomedical Sciences, Cambridge University Press, 2015
    locator: Chapter 1 (potential outcomes, SUTVA in Section 1.6, causal estimands in Section 1.10) and Chapter 3 (assignment mechanisms)
  - book: isbn:9780521895606
    title: Judea Pearl, Causality, Models, Reasoning, and Inference, second edition, Cambridge University Press, 2009
    locator: Chapter 7 (potential responses defined from structural models, and the equivalence of the two languages)
---

The potential outcomes framework is the model of causation used in most of statistics. Each unit has one outcome for each treatment it could receive: $Y_i(1)$ if treated and $Y_i(0)$ if not. The causal effect of the treatment on unit $i$ is a comparison of the two, such as $Y_i(1) - Y_i(0)$. Only one of them is ever observed, the one for the treatment the unit actually got, so every causal question is a question about values that are missing. What makes it possible to answer such questions is knowledge of the *assignment mechanism*, the rule that decided who got which treatment. Neyman wrote down potential outcomes for field trials in 1923, Rubin extended the model to observational studies from 1974 on, and Holland (1986) named it Rubin's model and stated its central difficulty.

## The machine

**Units and treatments.** There are $n$ units, $i = 1, \ldots, n$, and a treatment $T_i \in \{0, 1\}$ for each (1 for treated, 0 for control). Each unit may also have covariates $X_i$, measured before the treatment and not affected by it. Treatments with more than two levels work in the same way, with one potential outcome per level.

**Potential outcomes.** Each unit has two fixed numbers, $Y_i(1)$ and $Y_i(0)$. Together they form the *science table*, an $n \times 2$ table that does not depend on who is treated. Writing the outcome of unit $i$ as a function of its own treatment only is an assumption, [SUTVA](/sutva/): no interference between units, and one version of each treatment.

**Assignment mechanism.** The treatment vector $T = (T_1, \ldots, T_n)$ is drawn from a distribution $\Pr[T = t \mid X, Y(0), Y(1)]$. In a [randomized experiment](/randomized-experiment/) the experimenter chooses this distribution and knows it. In an observational study it is unknown, and assumptions such as [ignorability](/ignorability/) take its place.

**Observation.** The observed outcome is
$$Y_i = T_iY_i(1) + (1 - T_i)Y_i(0).$$
This is the *consistency* equation. For a treated unit, $Y_i(0)$ is missing, and for a control, $Y_i(1)$ is missing. The data are $(X_i, T_i, Y_i)$ for each unit.

**Estimands.** The effect for unit $i$ is $\tau_i = Y_i(1) - Y_i(0)$. The [average treatment effect](/average-treatment-effect/) of the $n$ units is $\tau_S = \frac1n\sum_i \tau_i$. If the units are a random sample from a large population, the population average is $\tau = \mathbb{E}[Y(1) - Y(0)]$, and the conditional average effect is $\tau(x) = \mathbb{E}[Y(1) - Y(0) \mid X = x]$. The randomness then comes from the sampling of units as well as from the assignment.

There are two modes of inference. In the *finite population* mode, the science table is fixed and only $T$ is random; this is the view of Fisher's and Neyman's randomization analyses. In the *superpopulation* mode, the rows $(X_i, Y_i(0), Y_i(1), T_i)$ are independent draws from one distribution, and expectations are over both.

## What it counts

- **Missing half.** The science table has $2n$ entries, and the data show $n$ of them. No unit effect $\tau_i$ is ever observed. Holland (1986) called this the fundamental problem of causal inference.
- **Assignments.** With a binary treatment there are $2^n$ possible assignment vectors. Complete randomization uses the $\binom{n}{n_1}$ vectors with $n_1$ treated units, each with probability $1/\binom{n}{n_1}$. Exact randomization inference visits all of them, or a random sample of them, as in the [permutation test](/permutation-test/).
- **What data can fix.** Under randomization, the data fix the two marginal distributions, of $Y(1)$ and of $Y(0)$, but not their joint distribution. So averages of $\tau_i$ are identified, but the variance of $\tau_i$, the median of $\tau_i$ and the share of units harmed by the treatment are not.

## Relation to other models

- **Structural causal models.** In a [structural causal model](/structural-causal-model/), the potential response $Y_x(u)$ is the value of $Y$ in the model with the equation of $X$ replaced by $X := x$. So every structural model defines potential outcomes, and $\mathbb{E}[Y(1)] = \mathbb{E}[Y \mid \mathrm{do}(T = 1)]$. Pearl (2009, Chapter 7) shows that the two languages prove the same results from the same assumptions. The graphs of the structural model make it easier to state and check assumptions such as the [back-door criterion](/backdoor-criterion/); potential outcomes make it easier to state estimands and the role of the design.
- **Missing data.** Treat $(Y_i(0), Y_i(1))$ as complete data and $T_i$ as the indicator of which part is observed. Ignorable assignment is then the same condition as data missing at random, and the [missing-data mechanism](/missing-data-mechanism/) page gives the terms. [Inverse probability weighting](/inverse-probability-weighting/) is the same idea in both settings.
- **Survey sampling.** In the finite population mode, the treated units are a random sample of the science table's first column, and the controls of its second column. The [Horvitz-Thompson estimator](/horvitz-thompson-estimator/) of each column mean is the bridge between the two fields.
- **Randomization tests.** Fisher's sharp null hypothesis $Y_i(1) = Y_i(0)$ for every $i$ fills in the whole science table from the data, so the law of any statistic over the assignments is known exactly. This is the logic of the [permutation test](/permutation-test/) and [Fisher's exact test](/fisher-exact-test/).

## Known results in the model

**A worked science table.** Six units have these potential outcomes.

| unit | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $Y_i(0)$ | 3 | 2 | 5 | 4 | 1 | 6 |
| $Y_i(1)$ | 5 | 6 | 5 | 7 | 4 | 6 |
| $\tau_i$ | 2 | 4 | 0 | 3 | 3 | 0 |

The average effect is $\tau_S = 12/6 = 2$. Suppose units 3, 4 and 6 are treated, the units that would do best without treatment. The data show $Y = (3, 2, 5, 7, 1, 6)$, and the difference of the observed means is $(5 + 7 + 6)/3 - (3 + 2 + 1)/3 = 6 - 2 = 4$, twice the true average effect.

**The naive difference splits into an effect and a bias.** For any assignment with treated set $A$ (of size $n_1$) and control set $B$ (of size $n_0$), write $\bar Y_A(t)$ for the mean of $Y_i(t)$ over $A$. Then
$$\bar Y_A(1) - \bar Y_B(0) = \underbrace{\bar Y_A(1) - \bar Y_A(0)}_{\text{effect on the treated}} + \underbrace{\bar Y_A(0) - \bar Y_B(0)}_{\text{selection bias}}.$$
*Proof.* Add and subtract $\bar Y_A(0)$. By consistency, the left side is the observed difference of means. $\square$

In the table, the treated units 3, 4 and 6 have mean effect $(0 + 3 + 0)/3 = 1$, and their untreated outcomes average $5$ against $2$ for the controls, so $4 = 1 + 3$. The selection bias is a difference in $Y(0)$ between the groups, which the data cannot show, because $Y(0)$ is missing for the treated. The same identity holds in the superpopulation, with conditional expectations given $T$.

**Randomization removes the bias on average.** If the treated set is chosen completely at random, each unit is treated with probability $n_1/n$, the expected selection bias is 0, and the difference of means is unbiased for $\tau_S$. The [randomized experiment](/randomized-experiment/) page proves this and gives the exact randomization distribution for the table above: 20 assignments, with mean exactly 2 and variance $16/15$.

**Identification under ignorability.** If $(Y(0), Y(1)) \perp T \mid X$ and $0 < \Pr[T = 1 \mid X] < 1$, then $\mathbb{E}[Y(t)] = \mathbb{E}\big[\mathbb{E}[Y \mid T = t, X]\big]$ for $t = 0, 1$. The [ignorability](/ignorability/) page proves this, and the [propensity score](/propensity-score/) page shows that conditioning on $\Pr[T = 1 \mid X]$ alone is enough.

**The joint law is not identified.** Two science tables can give the same observed data under every assignment and still differ in their unit effects. Take two units with $Y(0) = (0, 1)$. In table I, $Y(1) = (0, 1)$, so $\tau = (0, 0)$. In table II, $Y(1) = (1, 0)$, so $\tau = (1, -1)$. Under the design that treats one of the two at random, the observed outcome of the treated unit is 0 or 1 with probability $1/2$ each in both tables, and the same holds for the control. Indeed, the law of the data depends only on the multiset $\{Y_i(1)\}$ in the treated position and $\{Y_i(0)\}$ in the control position, and the two tables have the same multisets. Both have $\tau_S = 0$, but in table II half of the units are harmed. So the share of units harmed by the treatment, and the variance of $\tau_i$, cannot be learned from such data without further assumptions. This is why the Neyman variance estimate in a randomized experiment is conservative: the term $S_\tau^2$ that it leaves out is not identified.

**What is proved and what is not.** The identities above are exact algebra. Unbiasedness under randomization and identification under ignorability are proved on the linked pages. Statements about the coverage of confidence intervals built on these results are approximate and are measured by simulation on the pages of the estimators.

## References
