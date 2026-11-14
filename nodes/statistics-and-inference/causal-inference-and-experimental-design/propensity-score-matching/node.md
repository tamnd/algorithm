---
tag: SWSA9A
kind: algorithm
slug: propensity-score-matching
name: Propensity score matching
aliases:
- PSM
area: statistics-and-inference/causal-inference-and-experimental-design
level: core
summary: Pairs each treated unit with one or more control units of close propensity score and estimates the effect from the matched differences.
model: real-ram
complexity:
  vars: {m: "the number of treated units", n: "the number of control units, with m ≤ n"}
  time: {worst: Θ(m n + n log n), best: Θ(m n + n log n)}
  space: {extra: Θ(m n)}
properties: {deterministic: true, optimal_total_distance: true, uses_each_control_once: true, target: ATT}
history:
  year: 1985
  people: [Paul R. Rosenbaum, Donald B. Rubin]
  note: Rosenbaum and Rubin introduced the propensity score in 1983 and showed in 1985 how to build a matched control group with it. Rosenbaum gave optimal matching by network flows in 1989.
prereqs: [propensity-score, assignment-problem]
see_also: [inverse-probability-weighting, rosenbaum-sensitivity-analysis, hungarian-algorithm, min-cost-flow-problem, monge-property, k-nearest-neighbors, wilcoxon-signed-rank-test, logistic-regression]
sources:
  - paper: doi:10.1093/biomet/70.1.41
    title: Paul R. Rosenbaum and Donald B. Rubin, The central role of the propensity score in observational studies for causal effects, Biometrika 70(1), 1983
    locator: pp. 41 to 55 (the balancing property and matching on the propensity score)
  - paper: doi:10.1080/00031305.1985.10479383
    title: Paul R. Rosenbaum and Donald B. Rubin, Constructing a control group using multivariate matched sampling methods that incorporate the propensity score, The American Statistician 39(1), 1985
    locator: pp. 33 to 38 (nearest available matching on the propensity score and Mahalanobis matching within calipers)
  - paper: doi:10.1080/01621459.1989.10478868
    title: Paul R. Rosenbaum, Optimal matching for observational studies, Journal of the American Statistical Association 84(408), 1989
    locator: pp. 1024 to 1032 (optimal pair matching as a minimum cost flow, compared with greedy matching)
  - paper: doi:10.1111/j.1468-0262.2006.00655.x
    title: Alberto Abadie and Guido W. Imbens, Large sample properties of matching estimators for average treatment effects, Econometrica 74(1), 2006
    locator: pp. 235 to 267 (the bias of matching estimators and their variance)
  - paper: doi:10.3982/ECTA6474
    title: Alberto Abadie and Guido W. Imbens, On the failure of the bootstrap for matching estimators, Econometrica 76(6), 2008
    locator: pp. 1537 to 1557 (the standard bootstrap is not valid for nearest neighbour matching with replacement)
  - paper: doi:10.1198/106186006X137047
    title: Ben B. Hansen and Stephanie Olsen Klopfer, Optimal full matching and related designs via network flows, Journal of Computational and Graphical Statistics 15(3), 2006
    locator: pp. 609 to 627 (full matching as a minimum cost flow)
  - paper: doi:10.3982/ECTA11293
    title: Alberto Abadie and Guido W. Imbens, Matching on the estimated propensity score, Econometrica 84(2), 2016
    locator: pp. 781 to 807 (the large sample distribution with an estimated score and the variance adjustment)
  - paper: doi:10.1002/pst.433
    title: Peter C. Austin, Optimal caliper widths for propensity-score matching when estimating differences in means and differences in proportions in observational studies, Pharmaceutical Statistics 10(2), 2011
    locator: pp. 150 to 161 (a caliper of 0.2 standard deviations of the logit of the score)
  - paper: doi:10.1214/09-STS313
    title: Elizabeth A. Stuart, Matching methods for causal inference, a review and a look forward, Statistical Science 25(1), 2010
    locator: pp. 1 to 21 (distance measures, matching methods and balance diagnostics)
  - paper: doi:10.1017/pan.2019.11
    title: Gary King and Richard Nielsen, Why propensity scores should not be used for matching, Political Analysis 27(4), 2019
    locator: pp. 435 to 454 (the propensity score paradox)
  - book: isbn:9780387989679
    title: Paul R. Rosenbaum, Observational Studies, second edition, Springer, 2002
    locator: Chapter 10, pp. 295 to 331 (constructing matched sets and strata)
---

Propensity score matching (PSM) estimates the effect of a treatment from observational data by pairing each treated unit with a control unit that has nearly the same [propensity score](/propensity-score/) $e(x) = \Pr[T = 1 \mid X = x]$. Units with equal propensity scores have the same distribution of the covariates $X$, so the matched controls form a group that looks like the treated group on $X$. The mean of the paired differences estimates the average effect on the treated (ATT). This page gives the optimal way to form the pairs on a one-dimensional score: sort both groups and run a $\Theta(mn)$ dynamic program, which finds the pairs with the least total score distance. It is a special case of the [assignment problem](/assignment-problem/) that needs no general matching algorithm.

## In plain words

Each treated person gets a twin from the untreated group: someone whose chance of treatment, worked out from what we know about them, was about the same. If two people had the same chance, then whatever made one get treated and the other not was, as far as the measured facts go, a coin toss. Comparing the twins' outcomes and averaging gives the effect of the treatment on the kind of people who got it.

The common shortcut lets each treated person in turn take the closest twin still free. That can leave a later person with a poor twin. Sorting both lists by score and matching in order, with a small table to decide which controls to skip, gives the smallest total gap.

## The problem

**Identification.** The estimand is the ATT, $\tau_{\mathrm{ATT}} = \mathbb{E}[Y(1) - Y(0) \mid T = 1]$, in the notation of the [potential outcomes framework](/potential-outcomes-framework/). It needs [SUTVA](/sutva/) and consistency, $Y = TY(1) + (1 - T)Y(0)$; ignorability for the control outcome, $Y(0) \perp T \mid X$; and overlap for the treated, $e(X) < 1$ with probability 1. By the [propensity score](/propensity-score/) theorem, ignorability given $X$ implies ignorability given $e(X)$, so
$$\tau_{\mathrm{ATT}} = \mathbb{E}\big[\,Y - \mathbb{E}[Y \mid T = 0, e(X)]\,\big|\, T = 1\big].$$
A control with the same score as a treated unit is a draw from the right conditional distribution. Ignorability cannot be checked from data; overlap can be checked by comparing the score distributions of the two groups.

**Estimation.** The input is $m$ treated units with scores $s_1, \ldots, s_m$ and $n \ge m$ controls with scores $c_1, \ldots, c_n$. The scores are usually estimated, for example by [logistic regression](/logistic-regression/) of $T$ on $X$, and often put on the logit scale. A *pair matching* is a one-to-one map $\sigma$ from the treated units to distinct controls. The matching problem is to find a $\sigma$ that minimizes the total distance
$$\operatorname{cost}(\sigma) = \sum_{i=1}^m |s_i - c_{\sigma(i)}|.$$
The estimate is then $\hat\tau = \frac1m\sum_{i=1}^m \big(Y_i^{\text{treated}} - Y_{\sigma(i)}^{\text{control}}\big)$.

The whole procedure has four steps: estimate the score; drop or flag units outside the overlap; match; check that the matched groups are balanced on every covariate, and if not, change the score model and match again. Only after balance is acceptable are the outcomes used.

## The algorithm

```pseudo id=main
OPTIMAL-PAIR-MATCH(s[1..m], c[1..n])        ▷ treated and control scores, m ≤ n
L1  sort s and c in increasing order, keeping the original indices
L2  D[0][j] ← 0 for j = 0..n;  D[i][j] ← ∞ for 1 ≤ i ≤ m and j < i
L3  for i ← 1 to m do
L4      for j ← i to n do
L5          D[i][j] ← min(D[i][j - 1], D[i - 1][j - 1] + |s_i - c_j|)
L6  trace back from (m, n): if j > i and D[i][j - 1] = D[i][j], skip c_j and go to (i, j - 1); else pair s_i with c_j and go to (i - 1, j - 1)
L7  return D[m][n] and the pairs
```

$D[i][j]$ is the least total distance for matching the $i$ smallest treated scores to distinct controls among the $j$ smallest control scores. Line L5 has two choices for the largest control $c_j$: leave it unused, or pair it with $s_i$, the largest treated score of the first $i$. The proof shows that these two choices are enough, because some optimal matching never crosses: if $s_a \le s_b$, the control of $a$ is at most the control of $b$. Line L6 follows the choices back to recover the pairs.

The common alternative is *greedy* or *nearest available* matching: take the treated units in some order (often by decreasing score) and give each the nearest control not yet used. It costs $O(mn)$ with a scan, but its total distance can be larger than the optimum. Matching *with replacement* lets every treated unit take its nearest control, even one already used; a binary search in the sorted controls finds it in $O(\log n)$ time.

## Example

Two treated units have scores 0.40 and 0.50, and three controls have scores 0.20, 0.48 and 0.62. The outcomes are 9 and 12 for the treated, and 3, 7 and 10 for the controls.

Both lists are already sorted. The table $D$ from lines L2 to L5 is:

| $D[i][j]$ | $j = 0$ | $j = 1$ (0.20) | $j = 2$ (0.48) | $j = 3$ (0.62) |
|---|---|---|---|---|
| $i = 0$ | 0 | 0 | 0 | 0 |
| $i = 1$ (0.40) | $\infty$ | 0.20 | 0.08 | 0.08 |
| $i = 2$ (0.50) | $\infty$ | $\infty$ | 0.22 | 0.20 |

For example, $D[2][3] = \min(D[2][2], D[1][2] + |0.50 - 0.62|) = \min(0.22, 0.20) = 0.20$. The trace back pairs 0.50 with 0.62, then finds $D[1][2] = 0.08 < D[1][1] = 0.20$ and pairs 0.40 with 0.48. The total distance is 0.20, and the estimate is $\frac12\big((9 - 7) + (12 - 10)\big) = 2$.

Greedy matching in decreasing order of score gives 0.50 its nearest control 0.48 first. Then 0.40 is left with 0.20 (distance 0.20) and 0.62 (distance 0.22), and takes 0.20. The total distance is $0.02 + 0.20 = 0.22$, and the estimate is $\frac12\big((12 - 7) + (9 - 3)\big) = 5.5$. Matching with replacement gives both treated units the control 0.48, total distance $0.08 + 0.02 = 0.10$, and the estimate $\frac12(2 + 5) = 3.5$.

The three rules give three different answers on the same data. The greedy rule used the poor pair (0.40, 0.20).

## Correctness

The proof shows that OPTIMAL-PAIR-MATCH returns a matching of least total distance $\sum_i |s_i - c_{\sigma(i)}|$ among all one-to-one matchings, and that the pairs it returns have that cost. The key step is an exchange argument: if two pairs cross, swapping their controls does not increase the cost, because $|\cdot|$ is convex. The same proof works for any convex function of $s_i - c_j$, such as the squared distance.

The proof is about the matching step only. That a matched estimate is close to the ATT is a statistical claim with extra conditions. The balancing property on the [propensity score page](/propensity-score/) proves that exact matches on the true score give the right control distribution. With approximate matches and estimated scores, the behaviour of the estimate is shown here only by simulation.

## Complexity

Sorting takes $\Theta(m\log m + n\log n)$ time. Line L5 runs $\sum_{i=1}^m (n - i + 1) = m(n + 1) - m(m - 1)/2$ times, which is between $m(n + 1)/2$ and $mn$, so $\Theta(mn)$, each in constant time. The trace back takes at most $m + n$ steps. The total is $\Theta(mn + n\log n)$ in every case. The table needs $\Theta(mn)$ space; if only the cost is needed, two rows suffice, $\Theta(n)$.

In comparison, a general assignment problem with an arbitrary distance matrix, as needed for Mahalanobis distance on several covariates, takes $O(n^3)$ time with the [Hungarian algorithm](/hungarian-algorithm/) or a [minimum cost flow](/min-cost-flow-problem/) solver. The one-dimensional score lets the dynamic program do the same job faster. The reason is the uncrossing inequality of the proof: on sorted scores, the matrix of distances $|s_i - c_j|$ has the [Monge property](/monge-property/).

## Properties

- **Optimal for any convex distance.** The same table gives the least total $|s - c|$, the least total $(s - c)^2$, or the least total of any convex function of the difference.
- **Pairing does not change the mean estimate.** For one-to-one matching without replacement, $\hat\tau$ is the treated mean minus the mean of the chosen controls, so it depends only on which controls are chosen, not on who is paired with whom. The pairs matter for paired analyses, such as the [signed rank test](/wilcoxon-signed-rank-test/) and [Rosenbaum's sensitivity analysis](/rosenbaum-sensitivity-analysis/), and for balance checks within pairs.
- **Targets the ATT.** Every treated unit is used and only some controls, so the estimate describes the treated group. To estimate the ATE, also match each control to treated units, or use [inverse probability weighting](/inverse-probability-weighting/).
- **Balance in distribution, not exact.** By the balancing property, units with exactly equal true scores have the same covariate distribution. Pairs with close scores can still differ a lot in $X$; balance holds only on average over many pairs.

## Variants and improvements

- **Calipers.** Do not pair units whose scores differ by more than a caliper; unmatched treated units are dropped, which changes the estimand to the treated units with good matches. Austin (2011) recommends a caliper of 0.2 standard deviations of the logit of the score.
- **Mahalanobis matching within calipers.** Rosenbaum and Rubin (1985) match on the Mahalanobis distance of key covariates among the controls within a propensity caliper. This needs a general assignment or network flow solver.
- **Matching with replacement and k nearest neighbours.** Each treated unit takes its $k$ nearest controls, which may repeat, as in [k-nearest neighbours](/k-nearest-neighbors/). This lowers bias when good controls are scarce and raises variance when a few controls are used many times. Abadie and Imbens (2006) give its large sample theory and a bias correction.
- **Optimal full matching and network flows.** Rosenbaum (1989) formulated optimal matching as a [minimum cost flow](/min-cost-flow-problem/); Hansen and Klopfer (2006) extended it to full matching, where each matched set has one treated unit and several controls or one control and several treated units.
- **Subclassification.** Cut the score into five or more strata and compare within strata; this is the discrete form of matching and of weighting.
- **Variance with an estimated score.** Abadie and Imbens (2016) derive the large sample distribution of matching on an estimated score. For the ATE, ignoring the estimation of the score gives a conservative variance; for the ATT the correction can go either way.

## When to use it

Use propensity score matching when there are many controls and fewer treated units, the target is the effect on the treated, and the analysis needs a matched sample that can be inspected and checked for balance, or analysed as pairs. Use the optimal algorithm here in place of greedy matching: on a single score it costs little more. When the estimand is the ATE, or when the controls are few, [inverse probability weighting](/inverse-probability-weighting/) or a doubly robust method uses the data better. Always follow it with a balance check, and with a [sensitivity analysis](/rosenbaum-sensitivity-analysis/) for unmeasured confounding.

## Pitfalls

- **Matching without replacement can leave bias.** In a simulation with $X$ uniform on $[0, 1]$, $e(x) = 0.1 + 0.5x$, $Y(0) = 3x + \varepsilon$ with $\varepsilon \sim N(0, 0.5^2)$, effect $1 + x$, $n = 300$ and 500 repetitions (seed 2026), the naive difference of means was off from the sample ATT by 0.552 on average. Optimal pair matching on the true score cut the error to 0.073, greedy matching to 0.083, and matching with replacement to 0.001. Near $x = 1$ there are about three treated units for every two controls, so pairs without replacement must reach down to controls with smaller scores. These numbers are measured, not proved.
- **Good score matches are not good covariate matches.** Two units with equal scores can have very different $X$. King and Nielsen (2019) show that once the matched sample is nearly balanced, pruning further on the score can make covariate balance worse. Check balance on each covariate, for example with standardized mean differences, and not on the score alone.
- **Checking balance with the outcome in view.** Choosing the score model by looking at the estimated effect turns matching into a search for a result. Fix the matched sample before looking at the outcomes.
- **Discarded units change the estimand.** Calipers and trimming drop treated units without a match. The estimate then describes the matched treated units, not all treated units.
- **The naive variance.** Treating the pairs as a random sample of independent pairs ignores the estimation of the score and, with replacement, the reuse of controls. Abadie and Imbens (2008) show that the standard bootstrap is not valid for matching with replacement.
- **Matching cannot fix unmeasured confounding.** Like every method based on ignorability, PSM balances only the measured covariates.

## Implementations

## History

Rosenbaum and Rubin (1983) defined the propensity score and proved that matching on it balances the covariates. In 1985 they compared nearest available matching on the score with Mahalanobis matching within score calipers and recommended the latter. Rosenbaum (1989) showed that optimal matching is a network flow problem and compared it with greedy matching. Abadie and Imbens (2006, 2016) gave the large sample theory of matching estimators, with and without an estimated score. Stuart (2010) reviews the methods and the balance checks.

## References
