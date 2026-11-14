---
tag: T6ZNCN
kind: concept
slug: simpsons-paradox
name: Simpson's paradox
aliases:
- Yule-Simpson effect
- reversal paradox
area: statistics-and-inference/causal-inference-and-experimental-design
level: intro
summary: An association that holds in every subgroup can reverse when the groups are pooled. Which answer is causal depends on the causal structure, not on the data.
prereqs: [average-treatment-effect]
see_also: [ignorability, backdoor-criterion, structural-causal-model, mediation-analysis, randomized-experiment, propensity-score, stratified-sampling, randomized-block-design]
sources:
  - paper: doi:10.1093/biomet/2.2.121
    title: G. Udny Yule, Notes on the theory of association of attributes in statistics, Biometrika 2(2), 1903
    locator: pp. 121 to 134 (an association in each sub-population that differs from the association in the pooled population)
  - paper: doi:10.1111/j.2517-6161.1951.tb00088.x
    title: E. H. Simpson, The interpretation of interaction in contingency tables, Journal of the Royal Statistical Society, Series B 13(2), 1951
    locator: pp. 238 to 241 (two 2 by 2 tables with the same direction of association whose sum has none, and the question of which is sensible)
  - paper: doi:10.1126/science.187.4175.398
    title: P. J. Bickel, E. A. Hammel and J. W. O'Connell, Sex bias in graduate admissions, data from Berkeley, Science 187(4175), 1975
    locator: pp. 398 to 404 (the pooled admission rates against the rates by department)
  - paper: doi:10.1136/bmj.292.6524.879
    title: C. R. Charig, D. R. Webb, S. R. Payne and J. E. A. Wickham, Comparison of treatment of renal calculi by open surgery, percutaneous nephrolithotomy, and extracorporeal shockwave lithotripsy, British Medical Journal 292(6524), 1986
    locator: pp. 879 to 882 (success rates by stone size for each treatment)
  - paper: doi:10.1136/bmj.309.6967.1480
    title: Steven A. Julious and Mark A. Mullee, Confounding and Simpson's paradox, British Medical Journal 309(6967), 1994
    locator: pp. 1480 to 1481 (the kidney stone data as an example of the paradox)
  - paper: doi:10.1080/00031305.2014.876829
    title: Judea Pearl, Comment, understanding Simpson's paradox, The American Statistician 68(1), 2014
    locator: pp. 8 to 13 (the causal reading, and why the same data can call for pooling or for stratifying)
  - book: isbn:9780521895606
    title: Judea Pearl, Causality, Models, Reasoning, and Inference, second edition, Cambridge University Press, 2009
    locator: Chapter 6 (Simpson's paradox, confounding and collapsibility)
---

Simpson's paradox is the case where a treatment looks better than another in every subgroup of the data, and worse when the subgroups are pooled. It is not a mistake in arithmetic. The pooled rate of each treatment is an average of its subgroup rates, and the two treatments take this average with different weights, because they were given to different mixes of subgroups. Yule described it in 1903 and Simpson in 1951. The data alone cannot say which answer is right. If the subgroup variable is a cause of both treatment and outcome, the subgroup answer is the causal one; if it is an effect of the treatment, the pooled answer may be. The paradox is one of the clearest reasons why causal questions need causal assumptions.

## In plain words

A hospital has two treatments for kidney stones. Treatment A works better than B on small stones, and also better on large stones. Yet over all patients, B has the higher success rate. How? Doctors gave A mostly to large stones, which are hard to treat, and B mostly to small stones, which are easy. So A's overall rate is pulled down by its hard cases, and B's is pushed up by its easy ones. To compare the treatments fairly, you must compare them on the same kind of patient, which here means within each stone size. But if the subgroup was itself changed by the treatment, comparing within subgroups can hide the effect you want to measure. Which way is right depends on how the variables cause each other.

## The idea

Let $T$ be a treatment, $Y$ a binary outcome and $Z$ a variable that splits the data into groups. The pooled success rate of treatment $t$ is
$$\Pr[Y = 1 \mid T = t] = \sum_z \Pr[Y = 1 \mid T = t, Z = z]\,\Pr[Z = z \mid T = t].$$
The rate is a weighted average of the group rates, and the weights $\Pr[Z = z \mid T = t]$ depend on $t$. A reversal happens when the treatment that is better in each group gets much more of its weight on the groups with low rates.

**No reversal with equal weights.** If $Z$ has the same law in both arms, $\Pr[Z = z \mid T = 1] = \Pr[Z = z \mid T = 0] = \Pr[Z = z]$ for all $z$, and $\Pr[Y = 1 \mid T = 1, Z = z] \ge \Pr[Y = 1 \mid T = 0, Z = z]$ for every $z$, then $\Pr[Y = 1 \mid T = 1] \ge \Pr[Y = 1 \mid T = 0]$.

*Proof.* With equal weights, the difference of the pooled rates is $\sum_z \Pr[Z = z]\big(\Pr[Y = 1 \mid T = 1, Z = z] - \Pr[Y = 1 \mid T = 0, Z = z]\big)$, a sum of terms that are all at least 0. $\square$

So a reversal needs an association between $T$ and $Z$. In a [randomized experiment](/randomized-experiment/), $Z$ measured before treatment is independent of $T$ by design, and a reversal can occur only by chance in a finite sample; a [randomized block design](/randomized-block-design/) on $Z$ removes even that. The same sum with $\Pr[Z = z \mid T = t]$ replaced by one common law, such as $\Pr[Z = z]$, is the *standardized* rate.

**Which answer is causal.** The paradox becomes a question about the causal role of $Z$:

- If $Z$ is a pre-treatment cause of both $T$ and $Y$, a confounder, and nothing else confounds, then treatment is [ignorable](/ignorability/) given $Z$ and the standardized difference $\sum_z \Pr[Z = z]\big(\Pr[Y = 1 \mid 1, z] - \Pr[Y = 1 \mid 0, z]\big)$ is the [average treatment effect](/average-treatment-effect/). The subgroup comparison is the right one.
- If $Z$ is caused by $T$ and in turn affects $Y$, a mediator, then the pooled difference is the total effect of $T$, and comparing within $Z$ removes the part of the effect that goes through $Z$. The pooled comparison answers the question about the total effect, and the stratified one is a question about a direct effect, the subject of [mediation analysis](/mediation-analysis/).

Simpson (1951) gave two tables with the same numbers and different stories, in which common sense chose different answers. Pearl (2014) showed that this is the general rule: the same table can call for pooling or for stratifying, depending on the causal graph. The [back-door criterion](/backdoor-criterion/) on a [structural causal model](/structural-causal-model/) says which variables to stratify on. No statistical test on the table can decide.

**What is proved and what is not.** The no-reversal result and the standardization formulas are exact. The claim that a given standardized number is causal rests on the assumption that the stratifying variable removes all confounding, which the data cannot check. All numbers below are computed from the published counts.

## Examples

**Kidney stones (Charig et al., 1986).** Treatment A is open surgery and treatment B is percutaneous nephrolithotomy. Julious and Mullee (1994) used these counts to show the paradox.

| stone size | A: success / total | rate | B: success / total | rate |
|---|---|---|---|---|
| small | 81 / 87 | 0.931 | 234 / 270 | 0.867 |
| large | 192 / 263 | 0.730 | 55 / 80 | 0.688 |
| all | 273 / 350 | 0.780 | 289 / 350 | 0.826 |

A is better for small stones and for large stones, and B is better over all. The reason is in the weights: small stones are $87/350 = 0.249$ of A's patients and $270/350 = 0.771$ of B's. Stone size affects both the choice of treatment and the chance of success, so it is a confounder, and the comparison within size is the one to trust. Standardized to all 700 patients (357 small, 343 large), the rates are $0.8325$ for A and $0.7789$ for B, a difference of $0.054$ in favor of A. Standardized to A's mix of patients the difference is $0.048$, and to B's mix it is $0.059$; A wins in all three. Whether size is the only confounder is an assumption.

**Berkeley admissions (Bickel, Hammel and O'Connell, 1975).** In the autumn of 1973, the graduate school admitted men at a higher rate than women. The data for the six largest departments are:

| department | men: admitted / applied | rate | women: admitted / applied | rate |
|---|---|---|---|---|
| A | 512 / 825 | 0.62 | 89 / 108 | 0.82 |
| B | 353 / 560 | 0.63 | 17 / 25 | 0.68 |
| C | 120 / 325 | 0.37 | 202 / 593 | 0.34 |
| D | 138 / 417 | 0.33 | 131 / 375 | 0.35 |
| E | 53 / 191 | 0.28 | 94 / 393 | 0.24 |
| F | 22 / 373 | 0.06 | 24 / 341 | 0.07 |
| all six | 1198 / 2691 | 0.445 | 557 / 1835 | 0.304 |

Pooled, men are admitted at $0.445$ and women at $0.304$. By department, women do better in A, B, D and F, and worse in C and E, so the reversal is partial: it is not true that women did better in every department. Standardized to the total applicants of each department, the rates are $0.387$ for men and $0.430$ for women. Women applied more often to departments that admitted few applicants of either sex. Here department is chosen after sex is fixed, so it is a mediator, not a confounder. The stratified comparison answers the question Bickel and colleagues asked, whether departments treated equal applicants unequally; the pooled rate answers a different question, about the total difference including the choice of department.

**Same data, two stories.** Replace "stone size" in the kidney table by a variable measured after treatment, for example blood pressure after the drug, with the same counts. Now the variable is affected by the treatment, and stratifying on it would remove part of the effect. The pooled rates, which favor B, would be the answer for the total effect. Pearl (2014) uses such pairs to make the point that the numbers do not decide.

**A change of measure that is not a reversal.** Take a binary outcome and a binary $Z$ with $\Pr[Z = 1] = 1/2$ and $Z \perp T$, so there is no confounding. In stratum $Z = 0$ the success rates are $1/2$ untreated and $4/5$ treated, and in stratum $Z = 1$ they are $1/5$ and $1/2$. The odds ratio is $4$ in each stratum, but the pooled rates $7/20$ and $13/20$ give an odds ratio of $169/49 \approx 3.45$. The risk difference is $3/10$ in each stratum and pooled. This non-collapsibility of the odds ratio is a property of the measure, not of confounding, and the [average treatment effect](/average-treatment-effect/) page discusses it.

## Where it is used

- **Teaching and checking analyses.** The kidney stone and Berkeley tables are the standard warnings against reading pooled rates as effects in medicine, social science and data journalism.
- **Epidemiology.** Direct standardization of rates to a common population, and stratified estimators such as the Mantel-Haenszel estimator, compare groups within strata of a confounder, here age, sex or severity.
- **Meta-analysis.** Adding the counts of several trials with different allocation ratios can reverse the direction of the trials. Pooling the per-trial effects, not the raw counts, avoids it.
- **Online experiments.** If the share of traffic sent to a new version changes over the days of a test, and the outcome rate also varies by day, the pooled rates can disagree with every daily comparison. A fixed allocation ratio, or analysis by day, avoids it.
- **Observational causal inference.** Adjusting for the [propensity score](/propensity-score/), or stratifying on confounders as in [stratified sampling](/stratified-sampling/), is the systematic form of the stratified comparison. The paradox shows that the choice of what to adjust for is a causal choice.
- **Continuous variables.** The same effect appears in regression: the slope of $Y$ on $T$ can be positive within each group and negative in the pooled data, as when groups with higher $T$ have lower baselines.

## References
