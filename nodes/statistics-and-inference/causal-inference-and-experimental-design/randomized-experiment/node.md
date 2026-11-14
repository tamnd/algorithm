---
tag: AT76DD
kind: concept
slug: randomized-experiment
name: Randomized experiment
aliases:
- randomized controlled trial
- RCT
area: statistics-and-inference/causal-inference-and-experimental-design
level: intro
summary: An experiment in which chance assigns the treatments, so treatment is independent of the potential outcomes and simple contrasts estimate causal effects.
prereqs: [potential-outcomes-framework, average-treatment-effect]
see_also: [randomized-block-design, permutation-test, fisher-exact-test, cuped, fisher-yates-shuffle, sutva, ignorability, local-average-treatment-effect]
sources:
  - book: "R. A. Fisher, The Design of Experiments, Oliver and Boyd, Edinburgh, 1935"
    title: The Design of Experiments
    locator: Chapter II (the lady tasting tea, randomization as the physical basis of the test of significance; chapter-level locator)
  - paper: doi:10.1214/ss/1177012031
    title: Jerzy Splawa-Neyman, D. M. Dabrowska and T. P. Speed, On the application of probability theory to agricultural experiments, essay on principles, Section 9, Statistical Science 5(4), 1990
    locator: pp. 465 to 472 (the mean and variance of the difference of means over random assignments of plots)
  - book: isbn:9780521885881
    title: Guido W. Imbens and Donald B. Rubin, Causal Inference for Statistics, Social, and Biomedical Sciences, Cambridge University Press, 2015
    locator: Chapter 4 (classes of randomized experiments), Chapter 5 (Fisher's exact p-values) and Chapter 6 (Neyman's repeated sampling approach)
  - book: isbn:9780387989679
    title: Paul R. Rosenbaum, Observational Studies, second edition, Springer, 2002
    locator: Chapter 2, pp. 19 to 70 (randomized experiments, randomization tests and their exactness)
  - paper: doi:10.1214/12-AOS1008
    title: Kari Lock Morgan and Donald B. Rubin, Rerandomization to improve covariate balance in experiments, The Annals of Statistics 40(2), 2012
    locator: pp. 1263 to 1282 (rerandomization with a Mahalanobis distance criterion)
  - book: isbn:9781420076165
    title: Miguel A. Hernán and James M. Robins, Causal Inference, What If, Chapman and Hall/CRC, 2020
    locator: Chapter 2 (randomized experiments, exchangeability, conditional randomization and standardization; general locator)
---

A randomized experiment assigns treatments to units by a chance device that the experimenter controls. Because the device cannot see the units' [potential outcomes](/potential-outcomes-framework/), the treated and control groups differ only by chance in everything that matters for the outcome, measured or not. So the treated group's mean outcome estimates what everyone's mean would be under treatment, the control group's mean does the same for control, and their difference estimates the [average treatment effect](/average-treatment-effect/). Fisher made randomization the basis of experimental design in the 1920s and 1930s, and Neyman gave its repeated-sampling analysis in 1923. It is the reference design that all methods for observational data try to imitate.

## In plain words

You want to know if a fertilizer helps. If you choose which plots get it, you may pick the plots that look best, and then the fertilized plots do better for reasons that have nothing to do with the fertilizer. If a coin chooses, no such reason can line up with the treatment except by luck. On average over all the coin tosses, the fertilized plots and the others start out the same, so the difference you see at harvest is, on average, the effect of the fertilizer. Luck can still make one group better at the start, and the size of that luck is known from the coin, so you can say how sure you are. You do not need to know what makes plots grow. You only need the coin to be fair and the plots not to affect each other.

## The idea

Let $n$ units have potential outcomes $Y_i(1)$ and $Y_i(0)$, and assume [SUTVA](/sutva/). A randomized experiment is an assignment mechanism $\Pr[T = t]$ that the experimenter picks, with $0 < \Pr[T_i = 1] < 1$ for each unit, and that does not depend on the potential outcomes. The usual designs are:

- **Bernoulli trial.** Each unit is treated with probability $p$ on its own. The number treated is random and can be 0.
- **Completely randomized.** Exactly $n_1$ of the $n$ units are treated, and each of the $\binom{n}{n_1}$ treated sets has the same probability. A uniform shuffle such as the [Fisher-Yates shuffle](/fisher-yates-shuffle/) followed by treating the first $n_1$ units draws such a set.
- **Blocked or stratified.** Units are grouped by covariates, and each block is completely randomized on its own, as in the [randomized block design](/randomized-block-design/). Pairs are blocks of size 2.
- **Cluster randomized.** Whole groups, such as schools or villages, are randomized. This is the usual answer when units inside a group interfere.
- **Rerandomization.** Draw a completely randomized assignment, and draw again until a covariate balance measure is below a threshold fixed in advance (Morgan and Rubin, 2012). The analysis must use the restricted set of assignments.

**Unbiasedness of the difference in means.** Under complete randomization, let $\hat\tau = \frac1{n_1}\sum_{i : T_i = 1} Y_i - \frac1{n_0}\sum_{i : T_i = 0} Y_i$ with $n_0 = n - n_1$, both at least 1. Then $\mathbb{E}[\hat\tau] = \tau_S = \frac1n\sum_i (Y_i(1) - Y_i(0))$, the expectation being over the assignment only, with the potential outcomes fixed.

*Proof.* By consistency, $\hat\tau = \frac1{n_1}\sum_i T_iY_i(1) - \frac1{n_0}\sum_i (1 - T_i)Y_i(0)$, where the potential outcomes are constants and only the $T_i$ are random. Under complete randomization, the number of treated sets that contain unit $i$ is $\binom{n-1}{n_1-1}$, so $\Pr[T_i = 1] = \binom{n-1}{n_1-1}/\binom{n}{n_1} = n_1/n$, and $\Pr[T_i = 0] = n_0/n$. By linearity of expectation,
$$\mathbb{E}[\hat\tau] = \frac1{n_1}\sum_i \frac{n_1}{n}Y_i(1) - \frac1{n_0}\sum_i \frac{n_0}{n}Y_i(0) = \frac1n\sum_i Y_i(1) - \frac1n\sum_i Y_i(0) = \tau_S. \quad\square$$

The proof uses only SUTVA and the design. It needs no model for the outcomes, no normality and no large sample. The same argument applied to each block shows that the block-weighted difference in means is unbiased in a blocked design. In a Bernoulli trial the plain difference in means is not exactly unbiased, because $n_1$ is random and may be 0; the [Horvitz-Thompson estimator](/horvitz-thompson-estimator/) with the known probability $p$ is, as the [inverse probability weighting](/inverse-probability-weighting/) page proves.

**Variance.** Neyman showed that under complete randomization
$$\mathrm{Var}(\hat\tau) = \frac{S_1^2}{n_1} + \frac{S_0^2}{n_0} - \frac{S_\tau^2}{n},$$
where $S_1^2$, $S_0^2$ and $S_\tau^2$ are the variances, with divisor $n - 1$, of $Y_i(1)$, of $Y_i(0)$ and of $\tau_i$ over the $n$ units. This page states the formula and checks it on the example below; Imbens and Rubin (2015, Chapter 6) give the proof. The term $S_\tau^2$ depends on how the potential outcomes pair up, which no data show. The usual estimate $s_1^2/n_1 + s_0^2/n_0$, built from the sample variances in the two groups, drops that term. It is unbiased for the first two terms, so it is conservative, and exact when the effect is constant.

**Randomization inference.** Fisher's sharp null hypothesis says $Y_i(1) = Y_i(0)$ for every unit. Under it, the observed outcomes are the outcomes under any assignment, so the law of any test statistic over the $\binom{n}{n_1}$ assignments is known exactly. The p-value is the share of assignments whose statistic is at least as extreme as the observed one. This is the [permutation test](/permutation-test/), and with a binary outcome it is [Fisher's exact test](/fisher-exact-test/). The test is exact for any $n$, but the smallest p-value it can give is $1/\binom{n}{n_1}$ for a one-sided test.

**What is proved and what is measured.** Unbiasedness of $\hat\tau$ and exactness of the randomization test are proved for every sample size. The Neyman variance is stated here and checked exactly on the example. Normal confidence intervals $\hat\tau \pm 1.96\,\widehat{\mathrm{se}}$ rest on a central limit theorem for sampling without replacement, so their coverage is only approximate in finite samples; this page does not measure it.

## Examples

**The randomization distribution of a small experiment.** Six units have $Y(0) = (3, 2, 5, 4, 1, 6)$ and $Y(1) = (5, 6, 5, 7, 4, 6)$, so $\tau_S = 2$. Treat 3 of the 6 completely at random. The 20 possible assignments give these values of $\hat\tau$:

| $\hat\tau$ | 0 | 2/3 | 1 | 4/3 | 5/3 | 2 | 7/3 | 8/3 | 3 | 10/3 | 4 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| assignments | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 |

Their mean is exactly 2, as the theorem says. Their variance is $16/15$. The formula gives $S_1^2 = 11/10$, $S_0^2 = 7/2$ and $S_\tau^2 = 14/5$, so $\frac{11/10}{3} + \frac{7/2}{3} - \frac{14/5}{6} = \frac{11}{30} + \frac{35}{30} - \frac{14}{30} = \frac{16}{15}$, the same value. The expected value of the Neyman estimate over the 20 assignments is $11/30 + 35/30 = 23/15$, larger than $16/15$, as conservativeness says. A single experiment can still give an estimate as far off as 0 or 4.

**A Fisher test on the same units.** Suppose the chance device treats units 2, 4 and 5. The data are $Y = (3, 6, 5, 7, 4, 6)$, and $\hat\tau = 17/3 - 14/3 = 1$. Under the sharp null, the outcomes stay fixed and the 20 assignments give 20 values of the difference in means. Six of them are at least 1 and twelve are at least 1 in absolute value, so the one-sided p-value is $3/10$ and the two-sided one is $3/5$. With 6 units and 3 treated, no two-sided p-value can be smaller than $2/20 = 1/10$, so this experiment can never reject at the 5% level, however large the effect. The sharp null is false here, since four of the six unit effects are not zero; the test has no power at this size.

**The lady tasting tea.** Fisher's example in *The Design of Experiments*: a lady claims she can tell if the milk was poured before the tea. Eight cups are made, four of each kind, in a random order, and she must pick the four with milk first. Under the null that she cannot tell, each of the $\binom84 = 70$ choices is equally likely, so picking all four correctly has probability $1/70$. The randomization of the order is what makes this probability valid.

**A website test.** An online shop shows a new checkout page to a random half of its visitors and the old page to the rest, by hashing a visitor identifier. The difference in purchase rates estimates the effect of the page on purchase. Tests of this kind run in large numbers at internet companies, often with variance reduction from pre-experiment data, as in [CUPED](/cuped/).

## Where it is used

- **Medicine.** Phase III clinical trials compare a new treatment with a standard one or a placebo, with randomization, concealment of the allocation and often blinding. Regulators in most countries require them before approving new drugs.
- **Agriculture and biology.** Field trials of varieties and fertilizers, the setting where Fisher and Neyman built the theory, with blocks and [Latin squares](/latin-square-design/) to control soil differences.
- **Industry and the internet.** A/B tests of products, prices and interfaces, and [factorial designs](/factorial-design/) for processes with several factors.
- **Economics and policy.** Field experiments on schooling, cash transfers and health programs, often cluster randomized by village or school.
- **Imperfect compliance.** When some units do not take the treatment they were assigned, the comparison by assignment estimates the intention-to-treat effect, and the random assignment can serve as an instrument for the [local average treatment effect](/local-average-treatment-effect/).
- **As a benchmark.** Methods for observational data, from [inverse probability weighting](/inverse-probability-weighting/) to [propensity score matching](/propensity-score-matching/), aim to reconstruct the experiment that was not run. [Ignorability](/ignorability/) is the assumption that the data came from a conditionally randomized experiment with unknown probabilities.

## References
