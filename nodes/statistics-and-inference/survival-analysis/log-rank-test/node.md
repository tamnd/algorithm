---
tag: W9TSMC
kind: algorithm
slug: log-rank-test
name: Log-rank test
aliases:
- Mantel-Cox test
- Mantel-Haenszel log-rank test
area: statistics-and-inference/survival-analysis
level: core
summary: Compares survival curves of groups by the observed minus expected events at each event time, summed over time. It is the locally most powerful rank test under proportional hazards.
model: real-ram
complexity:
  vars: {n: the number of subjects, b: the number of random relabellings in the permutation version}
  time: {worst: Θ(n log n), permutation: Θ(b n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1966
  people: [Nathan Mantel, Richard Peto, Julian Peto, David R. Cox]
  note: Mantel (1966) combined the 2 x 2 tables at the event times by the Mantel-Haenszel method. Peto and Peto (1972) named it the logrank test and showed its local optimality, and it is the score test of the Cox model (Cox 1972).
prereqs: [censoring, hazard-function, statistical-hypothesis-test, p-value]
see_also: [kaplan-meier-estimator, cox-proportional-hazards-model, score-test, mann-whitney-u-test, permutation-test, fisher-exact-test, sample-size-determination, nelson-aalen-estimator]
sources:
  - paper: "Nathan Mantel, Evaluation of survival data and two new rank order statistics arising in its consideration, Cancer Chemotherapy Reports 50(3), 1966"
    locator: pp. 163 to 170 (the sum over event times of observed minus expected deaths, with the hypergeometric variances)
  - paper: doi:10.2307/2344317
    title: Richard Peto and Julian Peto, Asymptotically efficient rank invariant test procedures, Journal of the Royal Statistical Society Series A 135(2), 1972
    locator: from p. 185 (the logrank test, its name, and its asymptotic efficiency against proportional hazards alternatives)
  - paper: doi:10.1093/biomet/68.1.316
    title: David Schoenfeld, The asymptotic properties of nonparametric tests for comparing survival distributions, Biometrika 68(1), 1981
    locator: pp. 316 to 319 (the limit law under proportional hazards alternatives near the null, which gives the required number of events)
  - book: isbn:9780387953991
    title: John P. Klein and Melvin L. Moeschberger, Survival Analysis, Techniques for Censored and Truncated Data, 2nd edition, Springer, 2003
    locator: Chapter 7 (hypothesis testing, with the log-rank test, its weighted forms and the k-sample and stratified versions)
  - book: isbn:9780387945194
    title: Per Kragh Andersen, Ørnulf Borgan, Richard D. Gill and Niels Keiding, Statistical Models Based on Counting Processes, Springer, 1993
    locator: Chapter V (the k-sample tests with weight processes and their large-sample theory by martingale methods)
---

The log-rank test compares the survival of two (or more) groups when some event times are right censored. At each distinct event time $t_j$ it forms the $2 \times 2$ table of group against event among the subjects still at risk, and compares the observed number of events in group 1 with the number expected if both groups had the same [hazard](/hazard-function/). The differences are summed over all event times and divided by the square root of the summed hypergeometric variances. Under the null hypothesis of equal hazards the result is asymptotically standard normal, so its square is asymptotically chi-square with one degree of freedom. It is the [score test](/score-test/) of the [Cox model](/cox-proportional-hazards-model/) with a group indicator, and it has the highest asymptotic local power among rank tests when the hazards are proportional.

## In plain words

Two groups of patients are followed over time, and some leave the study before their outcome is known. Each time someone has the event, look at everyone still being followed just before. If the two treatments were equally good, the event would be equally likely to fall on any of them, so the share falling in group 1 should match group 1's share of the people at risk. Add up, over all event times, how many events group 1 actually had and how many it should have had by this fair share. A large difference, measured against how much such a total varies by chance, says that the groups differ.

## The problem

**Model.** Observations $(y_i, \delta_i, g_i)$, $i = 1, \ldots, n$, with $y_i = \min(T_i, C_i)$, $\delta_i = 1\{T_i \le C_i\}$ and a group label $g_i \in \{0, 1\}$. The subjects are independent, and censoring is independent within each group (see [censoring](/censoring/)). Group $g$ has hazard $h_g(t)$ and survival function $S_g(t)$.

**Hypotheses.** $H_0: h_1(t) = h_0(t)$ for all $t$ (equivalently $S_1 = S_0$) on the range where both groups are observed. The alternative is two-sided, $S_1 \ne S_0$. The one-sided form uses the sign of $U$ below. The test is built to detect $h_1(t) = \theta\, h_0(t)$ with $\theta \ne 1$ (proportional hazards).

**Statistic.** At the distinct event times $t_1 < \cdots < t_k$ of the pooled sample let $n_j$ and $n_{1j}$ be the numbers at risk ($y_i \ge t_j$) overall and in group 1, $n_{0j} = n_j - n_{1j}$, and $d_j$ and $d_{1j}$ the events overall and in group 1. Then

$$E_{1j} = \frac{d_j\, n_{1j}}{n_j}, \qquad V_j = \frac{n_{1j}\, n_{0j}\, d_j\,(n_j - d_j)}{n_j^2\,(n_j - 1)} \ (V_j = 0 \text{ if } n_j = 1),$$

$$U = \sum_{j=1}^k (d_{1j} - E_{1j}) = O_1 - E_1, \qquad V = \sum_{j=1}^k V_j, \qquad X^2 = \frac{U^2}{V}.$$

The weighted log-rank family uses $U_w = \sum_j w_j (d_{1j} - E_{1j})$ and $V_w = \sum_j w_j^2 V_j$ with a weight $w_j$ that depends only on the data before $t_j$ and on $n_j$, $d_j$.

**Null distribution.** Asymptotic. Given the risk sets and the total $d_j$ at $t_j$, $d_{1j}$ is hypergeometric under $H_0$ with mean $E_{1j}$ and variance $V_j$, as in [Fisher's exact test](/fisher-exact-test/) for that one table. The centred terms are uncorrelated across event times, and $U/\sqrt V \to N(0, 1)$ as $n \to \infty$, so $X^2 \to \chi^2_1$. The proof is in the correctness file. A permutation version, which permutes the group labels among the $n$ observed pairs $(y_i, \delta_i)$, is exact only when the two groups have the same censoring distribution.

**Rejection rule and p-value.** Reject at level $\alpha$ when $X^2 > \chi^2_{1, 1 - \alpha}$. The p-value is $P(\chi^2_1 > X^2)$, computed as an upper tail without cancellation. Since $\chi^2_1$ is the square of a standard normal, this equals the two-sided normal p-value $2P(Z > |U|/\sqrt V)$. The size is only near $\alpha$ in finite samples.

## The algorithm

```pseudo id=main
LOG-RANK(y[1..n], δ[1..n], g[1..n], weight rule w)
L1  sort the indices 1..n by y
L2  r ← n;  r1 ← number of i with g[i] = 1;  U ← 0;  V ← 0
L3  i ← 1
L4  while i ≤ n
L5      t ← y of the i-th sorted index;  d ← 0;  d1 ← 0;  m ← 0;  m1 ← 0
L6      while i ≤ n and y of the i-th sorted index = t: m ← m + 1;  m1 ← m1 + g;  if δ = 1 then d ← d + 1;  d1 ← d1 + g;  i ← i + 1
L7      if d > 0 then
L8          E ← d · r1 / r;  v ← r1 (r - r1) d (r - d) / (r² (r - 1)), or 0 if r = 1;  compute the weight w
L9          U ← U + w (d1 - E);  V ← V + w² v
L10     r ← r - m;  r1 ← r1 - m1                ▷ everyone at t, censored or not, leaves after t
L11 X² ← U² / V;  return U, V, X² and the chi-square upper tail of X² with 1 degree of freedom
```

The code supports five weight rules: the log-rank $w_j = 1$; Gehan's $w_j = n_j$; Tarone and Ware's $w_j = \sqrt{n_j}$; Peto and Peto's $w_j = \prod_{t_l \le t_j}(1 - d_l/(n_l + 1))$; and the Fleming-Harrington $G^{\rho, \gamma}$ weight $w_j = \hat S(t_j-)^\rho (1 - \hat S(t_j-))^\gamma$, where $\hat S$ is the pooled [Kaplan-Meier estimate](/kaplan-meier-estimator/). With `exact=True` the table and $U$ and $V$ are exact fractions for the rational weights. A second function gives the two-sided permutation p-value, exact by enumeration for small $n$ or by $b$ random relabellings with the $(1 + \#)/(1 + b)$ rule. The p-value uses the chi-square tail of the shared `stdist` helper.

## Example

The leukemia trial of Freireich et al. (1963), as listed by Gehan (1965), has 21 patients on 6-MP (group 1, 9 relapses and 12 censored remissions) and 21 on placebo (group 0, 21 relapses, none censored). The data are on the [Kaplan-Meier page](/kaplan-meier-estimator/). The pooled sample has 17 distinct event times. The first rows and the rows where 6-MP patients relapse are:

| $t_j$ | $n_j$ | $n_{1j}$ | $d_j$ | $d_{1j}$ | $E_{1j}$ | $V_j$ |
|---|---|---|---|---|---|---|
| 1 | 42 | 21 | 2 | 0 | 1 | 0.4878 |
| 2 | 40 | 21 | 2 | 0 | 21/20 | 0.4860 |
| 6 | 33 | 21 | 3 | 3 | 21/11 | 0.6508 |
| 7 | 29 | 17 | 1 | 1 | 17/29 | 0.2426 |
| 8 | 28 | 16 | 4 | 0 | 16/7 | 0.8707 |
| 10 | 23 | 15 | 1 | 1 | 15/23 | 0.2268 |
| 13 | 16 | 12 | 1 | 1 | 3/4 | 0.1875 |
| 16 | 14 | 11 | 1 | 1 | 11/14 | 0.1684 |
| 22 | 9 | 7 | 2 | 1 | 14/9 | 0.3025 |
| 23 | 7 | 6 | 2 | 1 | 12/7 | 0.2041 |

At $t = 1$, $V_1 = 21 \cdot 21 \cdot 2 \cdot 40/(42^2 \cdot 41) = 20/41$. Over all 17 rows, $O_1 = 9$ against $E_1 = 19.2505$, so $U = -10.2505$; $V = 6.25696$; $X^2 = 16.793$, and the p-value is $P(\chi^2_1 > 16.793) = 4.17 \times 10^{-5}$. The placebo group had $O_0 = 21$ against $E_0 = 10.7495$. The 6-MP group relapsed less than equal hazards would predict. The weighted versions give $X^2 = 13.46$ (Gehan, $p = 2.4 \times 10^{-4}$), $15.12$ (Tarone-Ware), $14.08$ (Peto-Peto) and $13.05$ (Fleming-Harrington with $\rho = 0$, $\gamma = 1$).

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows that the pass of lines L4 to L10 builds the table of $(t_j, n_j, n_{1j}, d_j, d_{1j})$, by the same invariant as for Kaplan-Meier. It then proves, for event times on a finite grid, that under $H_0$ and independent censoring $d_{1j}$ given the past and $d_j$ is hypergeometric with mean $E_{1j}$ and variance $V_j$, that the terms $w_j(d_{1j} - E_{1j})$ are uncorrelated martingale differences, and that $U/\sqrt V \to N(0, 1)$ by a central limit theorem for a sum of independent terms plus Slutsky's theorem. Finally it shows that $U$ is the score of the Cox partial likelihood at $\beta = 0$, and that $V$ is its information when there are no ties.

## Complexity

The sort in line L1 costs $\Theta(n \log n)$. Lines L4 to L10 process each subject once, with $O(1)$ work per subject and per event time, so the pass costs $\Theta(n)$ and the test $\Theta(n \log n)$ time and $\Theta(n)$ extra space in the [real RAM](/real-ram/) model. The permutation version with $b$ relabellings costs $\Theta(b\, n \log n)$ as coded; sorting once and keeping the order makes it $\Theta(b\, n)$. Full enumeration costs $\binom{n}{n_1}$ passes and is feasible only for small $n$. All terms of $V$ are non-negative, so $V$ has no cancellation; $U$ is a sum of signed terms, and the exact mode removes its rounding error.

## Properties

- **Score test of the Cox model.** With covariate $x_i = g_i$, the log partial likelihood with Breslow's tie handling has score $U$ at $\beta = 0$ and information $\sum_j d_j n_{1j} n_{0j}/n_j^2$. With no tied event times this is $V$. With ties, $V$ has the extra factor $(n_j - d_j)/(n_j - 1) \le 1$ of the hypergeometric variance.
- **Asymptotic efficiency.** Against proportional hazards alternatives $h_1 = \theta h_0$ with $\theta$ near 1, the log-rank test is asymptotically efficient among rank tests (Peto and Peto 1972). Gehan's and Peto's weights put more weight on early times and are efficient against alternatives such as a shift of a logistic distribution; the Fleming-Harrington $G^{0, 1}$ weight emphasizes late differences.
- **Number of events.** Under proportional hazards with equal allocation, $U/\sqrt V$ is approximately $N(\sqrt{D/4}\,\log\theta, 1)$, where $D$ is the number of events (Schoenfeld 1981). So a two-sided test at level $\alpha$ with power $1 - \beta$ needs about $D = 4(z_{1 - \alpha/2} + z_{1 - \beta})^2/(\log\theta)^2$ events: 66 events for $\theta = 2$, $\alpha = 0.05$ and power 0.8. See [sample-size determination](/sample-size-determination/).
- **No censoring.** With no censoring and no ties, Gehan's $U$ equals $2W - n_1 n_0$, where $W$ is the number of pairs in which the group-1 time is the smaller: Gehan's test is then the [Mann-Whitney test](/mann-whitney-u-test/) with a different variance.
- **Gehan's pair form.** Gehan's $U = \sum_{i:\, g_i = 1}\sum_{l:\, g_l = 0}[\phi(i, l) - \phi(l, i)]$, where $\phi(a, b) = 1$ if $a$ has an observed event and $b$ is known to outlast it ($y_b > y_a$, or $y_b = y_a$ with $b$ censored).

Measured size and power, two-sided at $\alpha = 0.05$. Event times are exponential; censoring is exponential with rate 0.2 in both groups, plus administrative censoring at time 3; $r = 4000$ replications, except $r = 2000$ for the last row. "Crossing" means group 1 has hazard 2 before time 0.4 and 0.4 after, against hazard 1 in group 0, so the survival curves cross at $t = 1.07$.

| setting | $n_1 + n_0$ | seed | log-rank | Gehan | FH $G^{0,1}$ |
|---|---|---|---|---|---|
| $H_0$ | 10 + 10 | 12 | 0.061 | 0.052 | 0.082 |
| $H_0$ | 30 + 30 | 11 | 0.059 | 0.057 | 0.063 |
| $H_0$, censoring rate 2 in group 1 and none in group 0 | 15 + 45 | 13 | 0.053 | 0.050 | 0.074 |
| hazard ratio 2 | 30 + 30 | 14 | 0.680 | 0.561 | 0.574 |
| crossing | 30 + 30 | 15 | 0.056 | 0.170 | 0.234 |
| crossing | 100 + 100 | 16 | 0.050 | 0.423 | 0.617 |

In the hazard ratio 2 row the expected number of events is 51.6, for which Schoenfeld's formula predicts power 0.70. In the crossing rows the early excess and the late deficit of events in group 1 cancel in $U$, and the log-rank test has no power at all, whatever the sample size.

## Variants and improvements

- **Weighted log-rank tests.** The weights above, chosen before seeing the data. A max-combination of several weighted statistics with a joint null distribution keeps the size while guarding against several shapes of alternative.
- **k groups.** With groups $1, \ldots, K$, form the vector $U_g = \sum_j (d_{gj} - d_j n_{gj}/n_j)$ for $g = 1, \ldots, K - 1$ and its covariance from the multivariate hypergeometric law, $\mathrm{Cov}(U_g, U_h) = \sum_j d_j(n_j - d_j)\, n_{gj}(1\{g = h\} n_j - n_{hj})/(n_j^2(n_j - 1))$. The quadratic form $U^{\mathsf T}V^{-1}U$ is asymptotically $\chi^2_{K-1}$. For ordered groups, a trend test uses scores $s_g$ and has one degree of freedom.
- **Stratified test.** Compute $U^{(s)}$ and $V^{(s)}$ within each stratum and add them before forming $X^2$. This is the Mantel-Haenszel combination of the tables over strata as well as over time.
- **Permutation version.** Permuting labels gives an exact test when the censoring distributions are equal. With heavy censoring in the smaller group and none in the larger, it was far too conservative in a simulation: size 0.006 at nominal 0.05 ($n_1 = 15$, $n_0 = 45$, $r = 500$ data sets, $b = 199$ relabellings, seed 17), while the asymptotic test had 0.052.
- **Restricted mean survival time.** When hazards are not proportional, comparing the areas under the two survival curves up to a time $\tau$ gives an interpretable effect measure and a test.

## When to use it

Use the log-rank test as the primary comparison of survival between randomized groups, especially when proportional hazards is plausible. Report it with the Kaplan-Meier curves and a hazard ratio from the Cox model. If early differences matter more, or the curves are expected to converge, prespecify a weighted test. If the curves may cross, prespecify a test that can detect that (a combination test or a restricted mean comparison); do not choose the weight after looking at the curves.

## Pitfalls

- **Crossing hazards.** As measured above, opposite differences at early and late times cancel. A non-significant log-rank test does not show that the curves are equal.
- **Choosing the weight after the fact.** Trying several weights and reporting the smallest p-value inflates the size.
- **Ties and censoring at the same time.** Count censorings at $t_j$ as at risk at $t_j$, and use the hypergeometric variance with the $(n_j - d_j)/(n_j - 1)$ factor when events are tied.
- **Permutation with unequal censoring.** Group labels are exchangeable only if the censoring is the same in both groups.
- **Informative or group-dependent dropout.** Independent censoring within each group is required. If patients leave one arm because of side effects that predict their outcome, the test compares the wrong hazards.
- **Not an effect size.** $X^2$ and the p-value do not measure how different the groups are. Give the hazard ratio or the difference in survival at a fixed time with an interval.
- **Small samples.** The size can exceed $\alpha$ slightly, as in the 10 + 10 row above; the Fleming-Harrington $G^{0,1}$ statistic, which rests on the few late events, deviates more.

## Implementations

## History

Nathan Mantel (1966) proposed to treat each event time as a $2 \times 2$ table and to combine the tables by the method of Mantel and Haenszel (1959) for stratified tables. Richard and Julian Peto (1972) derived the same statistic as a locally most powerful rank invariant test, named it the logrank test because it uses the scores of the logarithm of the estimated survival, and also gave the Peto-Peto weights. Cox (1972) showed that it is the score test of his proportional hazards model, and in the Cox literature it is sometimes called the Mantel-Cox test. The weighted family grew from Gehan's (1965) generalization of the Wilcoxon test, Breslow's (1970) generalization of the Kruskal-Wallis test, Tarone and Ware (1977), and Harrington and Fleming (1982). Schoenfeld (1981) gave the power formula still used to plan trials.

## References
