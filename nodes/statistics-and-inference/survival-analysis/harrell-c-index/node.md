---
tag: JWHWF0
kind: definition
slug: harrell-c-index
name: Harrell's concordance index
aliases:
- C-index
- concordance statistic
area: statistics-and-inference/survival-analysis
level: core
summary: The fraction of comparable pairs in which the unit with the higher predicted risk fails first. It extends the area under the ROC curve to censored data.
prereqs: [censoring, roc-auc, kendall-tau-distance]
see_also: [mann-whitney-u-test, u-statistic, ranking-comparison-kendall-tau, counting-inversions, inverse-probability-weighting, cox-proportional-hazards-model, kaplan-meier-estimator, cross-validation]
sources:
  - paper: doi:10.1001/jama.1982.03320430047030
    title: Frank E. Harrell Jr, Robert M. Califf, David B. Pryor, Kerry L. Lee and Robert A. Rosati, Evaluating the yield of medical tests, JAMA 247(18), 1982
    locator: pp. 2543 to 2546 (the concordance index for censored survival times, the fraction of usable patient pairs whose predictions and outcomes agree)
  - paper: "Frank E. Harrell Jr, Kerry L. Lee and Daniel B. Mark, Multivariable prognostic models, issues in developing models, evaluating assumptions and adequacy, and measuring and reducing errors, Statistics in Medicine 15(4), 1996"
    locator: pp. 361 to 387 (the c index as a measure of predictive discrimination, its relation to Somers' rank correlation, and its use with censored data)
  - paper: doi:10.1002/sim.4154
    title: Hajime Uno, Tianxi Cai, Michael J. Pencina, Ralph B. D'Agostino and L. J. Wei, On the C-statistics for evaluating overall adequacy of risk prediction procedures with censored survival data, Statistics in Medicine 30(10), 2011
    locator: pp. 1105 to 1117 (the dependence of Harrell's C on the censoring distribution, and the inverse probability of censoring weighted estimator of the truncated concordance)
---

Harrell's concordance index, or C-index, measures how well a risk score ranks subjects by their event times when some of the times are censored. A pair of subjects is comparable when the shorter observed time is an event, so it is known who failed first. The pair is concordant when the subject who failed first has the higher predicted risk. The C-index is the fraction of comparable pairs that are concordant, with ties in the score counted as one half. It is 1 for a perfect ranking, 1/2 for a score unrelated to the outcome, and 0 for a perfectly reversed one. Without censoring and with a binary outcome it is the [area under the ROC curve](/roc-auc/), and without censoring and ties it is a linear function of [Kendall's tau](/kendall-tau-distance/). With censoring its limit depends on the censoring distribution, which is why Uno's weighted version exists.

## Definition

**Data.** Subjects $i = 1, \ldots, n$ with an observed time $y_i = \min(T_i, C_i)$, an event indicator $\delta_i = 1\{T_i \le C_i\}$ (see [censoring](/censoring/)), and a risk score $\eta_i$, where a larger $\eta_i$ predicts an earlier event. For a Cox model, $\eta_i = x_i^{\mathsf T}\hat\beta$; for a model that predicts survival times, $\eta_i$ is minus the predicted time.

**Comparable pairs.** An ordered pair $(i, j)$ is comparable when subject $i$ is known to fail before subject $j$:

$$\delta_i = 1 \quad\text{and}\quad \big(y_j > y_i \ \text{ or } \ (y_j = y_i \text{ and } \delta_j = 0)\big).$$

A censored subject at the same time as an event is taken to outlast it, as in the risk sets of the [Kaplan-Meier estimator](/kaplan-meier-estimator/). Two events at the same time, and any pair whose earlier time is censored, are not comparable.

**Counts and index.** Over the comparable pairs let $N_c$ be the number with $\eta_i > \eta_j$ (concordant), $N_d$ the number with $\eta_i < \eta_j$ (discordant) and $N_t$ the number with $\eta_i = \eta_j$. Then

$$C = \frac{N_c + \tfrac12 N_t}{N_c + N_d + N_t},$$

defined when at least one pair is comparable. Somers' $D = 2C - 1 = (N_c - N_d)/(N_c + N_d + N_t)$ is the same information on the scale $[-1, 1]$.

**Population value.** With independent pairs, independent censoring and continuous $T$, $C$ converges to

$$P(\eta_i > \eta_j \mid A) + \tfrac12 P(\eta_i = \eta_j \mid A), \qquad A = \{T_i < T_j,\ T_i \le C_i,\ T_i < C_j\},$$

the concordance among pairs whose earlier failure falls before both censoring times. When there is no censoring, $A = \{T_i < T_j\}$ and the limit is the concordance probability $P(\eta_i > \eta_j \mid T_i < T_j) + \frac12 P(\eta_i = \eta_j \mid T_i < T_j)$. With censoring, $A$ gives more weight to pairs whose earlier failure is early, so the limit depends on the censoring distribution as well as on the score and the outcome.

## Examples and non-examples

**A hand count.** Five subjects with times $2, 3^+, 5, 7^+, 8$ (a plus marks a censored time) and risk scores $0.9, 0.5, 0.6, 0.1, 0.3$. The censored subjects $3^+$ and $7^+$ cannot be the earlier member of a pair, and the subject at 8 has no one after it, so the comparable pairs are those starting at 2 and at 5:

| pair | scores | verdict |
|---|---|---|
| $(2, 3^+)$ | $0.9 > 0.5$ | concordant |
| $(2, 5)$ | $0.9 > 0.6$ | concordant |
| $(2, 7^+)$ | $0.9 > 0.1$ | concordant |
| $(2, 8)$ | $0.9 > 0.3$ | concordant |
| $(5, 7^+)$ | $0.6 > 0.1$ | concordant |
| $(5, 8)$ | $0.6 > 0.3$ | concordant |

All 6 of the $\binom52 = 10$ pairs that are comparable agree, so $C = 1$, although the score ranks $3^+$ above 5 and $7^+$ below 8: those pairs carry no information. Swapping the scores of the subjects at 5 and 8 makes $(5, 8)$ discordant, and $C = 5/6$.

**A binary outcome.** Without censoring and with two possible times, the comparable pairs are the (case, control) pairs, and $C$ is the [Mann-Whitney](/mann-whitney-u-test/) estimate of $P(\eta_{\text{case}} > \eta_{\text{control}}) + \frac12 P(\text{tie})$, the AUC. With case scores $0.8, 0.4$ and control scores $0.6, 0.2, 0.4$: the case at 0.8 beats all three controls; the case at 0.4 loses to 0.6, beats 0.2 and ties 0.4. So $C = (4 + \frac12)/6 = 0.75$.

**No censoring and no ties.** Every one of the $\binom n2$ pairs is comparable. A pair is discordant exactly when the ordering by risk (largest first) and the ordering by time (earliest first) disagree on it, so $N_d$ is the [Kendall tau distance](/kendall-tau-distance/) $K$ between the two orderings and $C = 1 - K/\binom n2 = (1 - \tau)/2$, where $\tau$ is Kendall's rank correlation between $\eta$ and $T$. Counting the pairs directly costs $O(n^2)$; sorting by time and counting [inversions](/counting-inversions/) of the risk order gives $O(n \log n)$, and the same counting with a Fenwick tree over the risk ranks handles censoring and ties.

**Dependence on censoring.** In a simulation with $x \sim N(0, 1)$, $T$ exponential with rate $e^{x}$, the true score $\eta = x$, censoring exponential and independent of $(x, T)$, $n = 200$ and $r = 300$ replications per row, the mean of Harrell's $C$ grew with the censoring, while Uno's $C$ with $\tau = 1$ stayed near its target. The targets, from five uncensored samples of 40000 (seed 1), are $0.725$ for the full concordance and $0.731$ for the concordance restricted to $T_i < 1$.

| censoring rate | seed | censored | Harrell's $C$, mean (sd) | Uno's $C_{\tau = 1}$, mean (sd) |
|---|---|---|---|---|
| 0 | 21 | 0% | 0.725 (0.019) | 0.731 (0.023) |
| 0.5 | 22 | 36% | 0.733 (0.024) | 0.731 (0.024) |
| 2 | 23 | 64% | 0.745 (0.034) | 0.735 (0.033) |
| 5 | 24 | 79% | 0.751 (0.042) | 0.736 (0.066) |

Under proportional hazards the high-risk subjects leave the risk set first, so later pairs are harder to order, and heavier censoring removes exactly those later pairs. Two studies that apply the same model to populations with different follow-up can therefore report different values of $C$.

**Non-examples.**

- **Not calibration.** Any strictly increasing transformation of the scores leaves $C$ unchanged. A model whose predicted 5-year risks are all ten times too high can have $C = 0.9$. Calibration needs a separate check.
- **Not a property of the model alone.** $C$ depends on the spread of risk in the population. The same model has a lower $C$ in a population where everyone has similar covariates, as in a trial with narrow inclusion criteria.
- **Censoring ignored.** Counting every pair as if each censored time were an event, or discarding the censored subjects, gives a different number, which is not Harrell's $C$. In the hand example, treating $3^+$ and $7^+$ as events adds the pairs $(3, 5)$, $(3, 7)$, $(3, 8)$ and $(7, 8)$, of which $(3, 5)$ and $(7, 8)$ are discordant, so the value becomes $8/10$.
- **A risk that changes with time.** $C$ needs one score per subject. When predicted survival curves cross, as in a model with time-varying effects, the ranking depends on the horizon. Then use a time-dependent measure at a stated horizon instead.
- **A sign error.** A value below 1/2 usually means that a predicted survival time was used as a risk score. Then $1 - C$ is the intended value.

## Related definitions

- **Uno's C.** With $\hat G$ the [Kaplan-Meier](/kaplan-meier-estimator/) estimate of the censoring survival $P(C > t)$ and a horizon $\tau$ with $\hat G(\tau) > 0$, Uno et al. (2011) weight each comparable pair with $y_i < y_j$ and $y_i < \tau$ by $\hat G(y_i)^{-2}$. If censoring is independent of $(T, \eta)$, then $P(T_i \le C_i, T_i < C_j \mid T_i, T_j, \eta) = G(T_i)\, G(T_i-)$ for $T_i < T_j$, so this [inverse probability weighting](/inverse-probability-weighting/) removes the censoring from the limit, which becomes $P(\eta_i > \eta_j \mid T_i < T_j, T_i < \tau)$ plus half the tie probability. The code here uses $\hat G(y_i-)$, which differs only when a censoring coincides with an event.
- **Area under the ROC curve.** The binary case above. A time-dependent AUC at a horizon $t$ compares the subjects with $T \le t$ against those with $T > t$.
- **Kendall's tau and Somers' D.** $C = (1 - \tau)/2$ without censoring and ties, and $D = 2C - 1$ in general. See also [comparing rankings with Kendall's tau](/ranking-comparison-kendall-tau/).
- **U-statistics.** $N_c$, $N_d$ and the number of comparable pairs are, after division by $n(n - 1)$, [U-statistics](/u-statistic/) of order 2, so $C$ is a ratio of U-statistics and asymptotically normal; its standard error can be computed by U-statistic theory or by the jackknife.
- **Use in model checking.** When the model is fitted and evaluated on the same data, $C$ is optimistic. Estimate it by [cross-validation](/cross-validation/) or bootstrap correction. For a [Cox model](/cox-proportional-hazards-model/), $\eta_i = x_i^{\mathsf T}\hat\beta$, and with one binary covariate $C$ is a censored version of the Mann-Whitney statistic.

## References
