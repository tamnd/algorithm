---
tag: MA7Z7G
kind: algorithm
slug: benjamini-hochberg-procedure
name: Benjamini-Hochberg procedure
aliases:
- BH procedure
- linear step-up procedure
area: statistics-and-inference/hypothesis-testing
level: core
summary: Sort the p-values and reject the k smallest, for the largest k with p_(k) <= k q / m. With independent null p-values the FDR is exactly (m_0/m) q, so at most q.
model: real-ram
complexity:
  vars: {m: the number of hypotheses}
  time: {worst: Θ(m log m), best: Θ(m log m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1995
  people: [Yoav Benjamini, Yosef Hochberg]
  note: Benjamini and Hochberg defined the false discovery rate and gave this step-up procedure in JRSS B in 1995. Its rule is the global test of Simes (1986) turned into a rule for single hypotheses.
prereqs: [false-discovery-rate, p-value]
see_also: [benjamini-yekutieli-procedure, storey-q-value, hochberg-procedure, holm-bonferroni-method, local-false-discovery-rate, knockoff-filter, multiple-comparisons-problem, e-variable]
sources:
  - paper: doi:10.1111/j.2517-6161.1995.tb02031.x
    title: Yoav Benjamini and Yosef Hochberg, Controlling the false discovery rate, a practical and powerful approach to multiple testing, Journal of the Royal Statistical Society, Series B 57(1) (1995), pages 289 to 300
    locator: the linear step-up procedure, the proof that it controls the FDR at (m_0/m) q for independent test statistics, and the example with 15 p-values
  - paper: doi:10.1214/aos/1013699998
    title: Yoav Benjamini and Daniel Yekutieli, The control of the false discovery rate in multiple testing under dependency, The Annals of Statistics 29(4) (2001), pages 1165 to 1188
    locator: FDR control at (m_0/m) q under positive regression dependence on the subset of true nulls (PRDS), and the bound for arbitrary dependence
  - paper: doi:10.1093/biomet/73.3.751
    title: R. J. Simes, An improved Bonferroni procedure for multiple tests of significance, Biometrika 73(3) (1986), pages 751 to 754
    locator: the global test that rejects when p_(j) <= j alpha / n for some j, which is the Benjamini-Hochberg rule under the global null
---

The Benjamini-Hochberg procedure (BH) tests $m$ hypotheses and controls the [false discovery rate](/false-discovery-rate/), the expected proportion of false rejections among the rejections. It sorts the p-values, $p_{(1)} \le \dots \le p_{(m)}$, finds the largest $k$ with $p_{(k)} \le kq/m$, and rejects $H_{(1)}, \dots, H_{(k)}$. When the null p-values are independent of each other and of the non-null ones, its FDR is at most $(m_0/m)q$, and exactly $(m_0/m)q$ when the null p-values are uniform, whatever the false nulls are. Here $m_0$ is the number of true nulls. The thresholds $kq/m$ grow linearly from $q/m$, the Bonferroni level, to $q$, so BH rejects far more than the FWER methods when many effects are real. It is the most used multiple testing method in genomics and other large-scale screening.

## In plain words

You have many tests and expect some real effects among them. Instead of asking that no false alarm ever happens, you ask that false alarms make up only a small share of what you report, on average. Sort the results from the most convincing to the least. The most convincing one must pass a very strict bar, the second a bar twice as easy, the third three times as easy, and so on. Then find the last result in the list that passes its own bar, and report it and everything above it, even the ones above it that missed their own bar. The more results look convincing, the more lenient the method gets. This is what makes it powerful when there are many real effects.

## The problem

**Input.** P-values $p_1, \dots, p_m$ for hypotheses $H_1, \dots, H_m$, and a target FDR level $q \in (0, 1]$. The set of true nulls is $I_0$, with $m_0$ elements.

**Output.** The rejected set $\{i : p_i \le kq/m\}$ for the $k$ above, and the adjusted p-values $\tilde p_i$, with $H_i$ rejected exactly when $\tilde p_i \le q$.

**Error rate controlled.** The false discovery rate $E[V/\max(R, 1)]$, where $V$ is the number of rejected true nulls and $R$ the number of rejections. Control is strong, over every configuration of true and false nulls.

**Dependence and level.**

- Independent null p-values, independent of the non-null p-values: $\text{FDR} \le (m_0/m)q$ in finite samples, with equality when each null p-value is exactly uniform. This is proved below.
- Positive regression dependence on the subset of true nulls (PRDS), as for one-sided tests on normal vectors with nonnegative correlations: $\text{FDR} \le (m_0/m)q$ (Benjamini and Yekutieli 2001). This is cited, not proved here.
- Arbitrary dependence: $\text{FDR} \le (m_0/m)q\sum_{i=1}^m 1/i$, and this bound can be attained. The [Benjamini-Yekutieli procedure](/benjamini-yekutieli-procedure/) runs BH at $q/\sum_{i=1}^m 1/i$ for this case.

**FWER.** Under the global null BH is the Simes test, so it controls the FWER weakly at $q$ for independent p-values. It does not control the FWER strongly.

## The algorithm

```pseudo id=main
BH(p₁, …, p_m, q)                       ▷ p-values in [0, 1], FDR level q
L1  sort the indices so that p_(1) ≤ … ≤ p_(m)
L2  k ← m; while k ≥ 1 and m · p_(k) > k · q do
L3      k ← k − 1                        ▷ step up: from the largest p-value down
L4  reject H_(1), …, H_(k)
L5  run ← 1; for r ← m down to 1 do       ▷ adjusted p-values
L6      run ← min(run, m · p_(r) / r)
L7      p̃_(r) ← run
L8  return (rejected set, p̃)
```

Lines L2 and L3 look for the last p-value below its line, starting from the largest one. All hypotheses before it are rejected at line L4, even those whose own p-value lies above its own threshold. That is the step-up rule. The test at line L2 multiplies, $m p_{(k)} > kq$, instead of dividing, so that the decisions do not change with rounding and agree with the adjusted p-values. Ties do not matter: the rejected set is $\{i : p_i \le kq/m\}$, which does not depend on how the sort orders tied values.

**Equivalent descriptions.**

- **Graph.** Plot $p_{(k)}$ against $k$, draw the line through the origin with slope $q/m$, and reject everything up to the last point on or below the line.
- **Counting.** With $N(t) = \#\{i : p_i \le t\}$, the number of rejections is $R = \max\{k : N(kq/m) \ge k\}$. So $t = Rq/m$ is the largest threshold with $mt/N(t) \le q$, where $mt/N(t)$ is the estimate of the FDR of the rule "reject $p_i \le t$" when all $m$ nulls are counted as true.
- **Self-consistency.** The rejected set is the largest set $S$ such that $p_i \le |S|q/m$ for every $i \in S$.

## Example

**The 15 p-values of Benjamini and Hochberg (1995).** The p-values are 0.0001, 0.0004, 0.0019, 0.0095, 0.0201, 0.0278, 0.0298, 0.0344, 0.0459, 0.3240, 0.4262, 0.5719, 0.6528, 0.7590 and 1.000, at $q = 0.05$, so the thresholds are $k/300$.

| $k$ | $p_{(k)}$ | $kq/m$ | $p_{(k)} \le kq/m$ | adjusted $\tilde p_{(k)}$ |
|---|---|---|---|---|
| 1 | 0.0001 | 0.0033 | yes | 0.0015 |
| 2 | 0.0004 | 0.0067 | yes | 0.003 |
| 3 | 0.0019 | 0.01 | yes | 0.0095 |
| 4 | 0.0095 | 0.0133 | yes | 0.0356 |
| 5 | 0.0201 | 0.0167 | no | 0.0603 |
| 6 | 0.0278 | 0.02 | no | 0.0639 |
| 7 | 0.0298 | 0.0233 | no | 0.0639 |
| 8 | 0.0344 | 0.0267 | no | 0.0645 |
| 9 | 0.0459 | 0.03 | no | 0.0765 |
| 10 | 0.3240 | 0.0333 | no | 0.486 |

The last row that passes is $k = 4$, so BH rejects four hypotheses. [Bonferroni](/bonferroni-correction/), [Holm](/holm-bonferroni-method/) and [Hochberg](/hochberg-procedure/) at $\alpha = 0.05$ reject three. The adjusted value at $k = 6$ is a running minimum: $15 \cdot 0.0278/6 = 0.0695$ is lowered to $15 \cdot 0.0298/7 = 0.0639$ by line L6.

**Step-up at work.** For $p = (0.01, 0.03, 0.028, 0.04)$ at $q = 0.1$, the thresholds are 0.025, 0.05, 0.075 and 0.1, and every sorted p-value passes, so all four are rejected. For $p = (0.03, 0.03, 0.9)$ at $q = 0.05$, the row $k = 2$ passes, $0.03 \le 2 \cdot 0.05/3 = 0.0333$, so both 0.03 values are rejected although each is above the first threshold $0.05/3$.

**The level by hand.** Take $m = 2$, $H_2$ false with $p_2 = 0$, and $H_1$ true with $p_1$ uniform. BH rejects $H_2$ always, since $0 \le q/2$, and rejects $H_1$ exactly when $p_1 \le 2q/2 = q$, with $R = 2$. So $V/R = 1/2$ with probability $q$ and 0 otherwise, and $\text{FDR} = q/2 = (m_0/m)q$.

## Correctness

The [proof](proofs/correctness.md) shows that $\text{FDR} = (m_0/m)q$ for independent uniform null p-values. It is a leave-one-out argument. Fix a true null $H_i$ and set $p_i$ to 0. Let $C_k^{(i)}$ be the event that BH then rejects exactly $k$ hypotheses. This event depends only on the other p-values. A short lemma shows that $H_i$ is rejected with $R = k$ exactly when $p_i \le kq/m$ and $C_k^{(i)}$ holds. So
$$E\left[\frac{\mathbf 1\{H_i \text{ rejected}\}}{\max(R, 1)}\right] = \sum_{k=1}^m \frac1k P\left(p_i \le \frac{kq}{m}\right)P(C_k^{(i)}) = \frac qm\sum_{k=1}^m P(C_k^{(i)}) = \frac qm,$$
by independence and uniformity, since the events $C_k^{(i)}$ partition the sample space. Summing over the $m_0$ true nulls gives $(m_0/m)q$. A valid but not uniform null p-value, $P(p_i \le u) \le u$, turns the second equality into $\le$.

The tests check this identity exactly. With $m = 4$ and $q = 2/5$, every threshold $kq/m = k/10$ is a point of the grid $\{1/10, \dots, 1\}$, so a null p-value uniform on that grid satisfies $P(p_i \le kq/m) = kq/m$ exactly. Summing over all $10^{m_0}$ values of the null p-values in rational arithmetic gives an FDR of exactly $m_0/10$ for each $m_0 = 1, \dots, 4$ and each choice of the non-null p-values. The tests also compare BH with a brute force over all subsets, using the self-consistency description, and measure the FDR by Monte Carlo for independent and for equicorrelated normal statistics. The equicorrelated case is PRDS, so the measured FDR is checked against $(m_0/m)q$ there too, but that bound is only measured, not proved.

## Complexity

On a [real RAM](/real-ram/), sorting at line L1 takes $\Theta(m\log m)$ time, which is the [sorting problem](/sorting-problem/). Lines L2 to L7 take $\Theta(m)$. So the time is $\Theta(m\log m)$, and the extra space is $\Theta(m)$.

The rejections alone need no sort. Put each $p_i$ into the bucket $b_i = \lceil mp_i/q\rceil$, the first $k$ with $mp_i \le kq$, with bucket $m + 1$ for $p_i > q$. Then $N(kq/m)$ is the [prefix sum](/prefix-sums/) of the bucket counts up to $k$, and $R$ is the largest $k$ with $N(kq/m) \ge k$. This is the idea of [counting sort](/counting-sort/) and takes $\Theta(m)$ time. The implementation gives both versions and checks that they agree, including on ties and values that fall exactly on a threshold.

## Properties

- **FDR at $(m_0/m)q$ for independent tests.** Exact, in finite samples, for every configuration of the false nulls. The bound is conservative by the factor $m_0/m$, which [Storey's method](/storey-q-value/) estimates and removes.
- **Weak FWER control.** Under the global null, $V = R$, the FDR is the FWER, and BH is the Simes test of size $q$.
- **More powerful than FWER methods.** The $k$-th threshold $kq/m$ is at least the Holm and Hochberg threshold $q/(m - k + 1)$, because $k(m - k + 1) \ge m$ for $1 \le k \le m$. So at the same level BH rejects a superset of what [Hochberg's procedure](/hochberg-procedure/) rejects, and so of Holm and Bonferroni.
- **Step-up.** It rejects $H_{(1)}, \dots, H_{(k)}$ for the largest passing $k$, so a hypothesis is rejected whenever enough other p-values are small.
- **Monotone.** Lowering any p-value never removes a rejection: $N(t)$ only grows, so $R$ only grows, and the thresholds with it.
- **Adjusted p-values.** $\tilde p_{(r)} = \min_{j \ge r}\min(1, mp_{(j)}/j)$. They are often called BH q-values, but they are not the same as Storey's q-values, which also estimate $\pi_0 = m_0/m$.

## Variants and improvements

- **Benjamini-Yekutieli.** BH at $q/\sum_{i=1}^m 1/i$ controls the FDR under any dependence. See [Benjamini-Yekutieli procedure](/benjamini-yekutieli-procedure/).
- **Adaptive BH.** Estimate $\pi_0 = m_0/m$ and run BH at $q/\hat\pi_0$. With a suitable estimator this still controls the FDR at $q$ under independence; see [Storey's q-value](/storey-q-value/).
- **Weighted BH.** Use $p_i/w_i$ with weights that average 1, to give prior favourites a larger threshold. Under independence and fixed weights the FDR is still at most $q$.
- **e-BH.** For [e-values](/e-variable/), reject the $k$ largest for the largest $k$ with $e_{(k)} \ge m/(kq)$. This controls the FDR at $(m_0/m)q$ under any dependence (Wang and Ramdas 2022).
- **Knockoffs.** In variable selection for regression, the [knockoff filter](/knockoff-filter/) uses a BH-like stopping rule on signed statistics, with an estimate of $V$ built from fake copies of the variables.
- **Local fdr.** The Bayesian view of BH estimates a tail-area false discovery rate; the [local false discovery rate](/local-false-discovery-rate/) gives the posterior probability for each case instead.

## When to use it

Use BH when $m$ is large, when you expect a fair number of real effects, and when a small proportion of false discoveries is acceptable, as in screening for genes, proteins, brain voxels or features for follow-up. The tests should be independent or positively dependent; for one-sided tests on positively correlated normal or $t$ statistics this is the case. For arbitrary dependence use [Benjamini-Yekutieli](/benjamini-yekutieli-procedure/), at a large cost in power. When many nulls are false, [Storey's method](/storey-q-value/) gains power by estimating $m_0$. When every single rejection must be right, as for the primary end points of a clinical trial, control the [family-wise error rate](/family-wise-error-rate/) instead.

## Pitfalls

- **Reading the level as a bound for one study.** FDR control is a bound on the mean proportion. In one study the proportion of false discoveries can be much larger than $q$.
- **Rejecting only the hypotheses below their own threshold.** That is a step-down reading of the rule, and it rejects less than BH. In the 15 p-value example both readings give 4, but for $(0.03, 0.03, 0.9)$ the step-down reading rejects nothing.
- **Two-sided p-values under positive correlation.** PRDS holds for one-sided tests on positively correlated normal statistics. It need not hold for two-sided tests, although simulations usually show that BH still works there.
- **Discrete p-values.** For discrete tests BH is conservative, because $P(p_i \le kq/m)$ is below $kq/m$.
- **Choosing $q$ or the family after seeing the result.** As with any error rate, the guarantee holds only when the level and the set of hypotheses are fixed in advance.

## Implementations

## History

Simes (1986) proposed the rule "reject the global null if $p_{(j)} \le j\alpha/m$ for some $j$" as a global test, and noted that it does not control the FWER for single hypotheses. Benjamini and Hochberg (1995) introduced the false discovery rate and showed that the same rule, applied to single hypotheses, controls this new error rate for independent test statistics. Benjamini and Yekutieli (2001) proved control under positive dependence and gave the correction for arbitrary dependence. Storey (2002) and Storey, Taylor and Siegmund (2004) gave the adaptive version, the q-value and a martingale proof of the control.

## References
