---
tag: HW5E27
kind: algorithm
slug: benjamini-yekutieli-procedure
name: Benjamini-Yekutieli procedure
aliases:
- BY procedure
area: statistics-and-inference/hypothesis-testing
level: advanced
summary: Run Benjamini-Hochberg at level q / (1 + 1/2 + ... + 1/m). This controls the FDR at (m_0/m) q under any dependence, at a level about ln m times smaller.
model: real-ram
complexity:
  vars: {m: the number of hypotheses}
  time: {worst: Θ(m log m), best: Θ(m log m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2001
  people: [Yoav Benjamini, Daniel Yekutieli]
  note: Benjamini and Yekutieli proved in The Annals of Statistics in 2001 that Benjamini-Hochberg controls the FDR under positive regression dependence, and that the harmonic factor makes it valid under any dependence.
prereqs: [benjamini-hochberg-procedure, false-discovery-rate]
see_also: [bonferroni-correction, storey-q-value, e-variable, harmonic-series, multiple-comparisons-problem, hochberg-procedure]
sources:
  - paper: doi:10.1214/aos/1013699998
    title: Yoav Benjamini and Daniel Yekutieli, The control of the false discovery rate in multiple testing under dependency, The Annals of Statistics 29(4) (2001), pages 1165 to 1188
    locator: the step-up procedure with constants k q / (m sum_(i=1..m) 1/i) and its FDR control under arbitrary dependence, and the PRDS condition for the plain procedure
  - paper: doi:10.1111/j.2517-6161.1995.tb02031.x
    title: Yoav Benjamini and Yosef Hochberg, Controlling the false discovery rate, a practical and powerful approach to multiple testing, Journal of the Royal Statistical Society, Series B 57(1) (1995), pages 289 to 300
    locator: the linear step-up procedure that the Benjamini-Yekutieli procedure rescales, and the example with 15 p-values
---

The Benjamini-Yekutieli procedure (BY) is the [Benjamini-Hochberg procedure](/benjamini-hochberg-procedure/) run at the smaller level $q/c_m$, where $c_m = \sum_{i=1}^m 1/i$ is the $m$-th harmonic number. It sorts the p-values, finds the largest $k$ with $p_{(k)} \le kq/(mc_m)$, and rejects $H_{(1)}, \dots, H_{(k)}$. Its [false discovery rate](/false-discovery-rate/) is at most $(m_0/m)q$ under any dependence among the p-values, with only the validity of each null p-value assumed. That is the reason to use it. The price is power: $c_m$ is about $\ln m + 0.577$, so the thresholds are 2.93 times smaller than those of BH for $m = 10$ and 7.49 times smaller for $m = 1000$. The factor cannot be removed in general: there are joint laws of valid p-values under which plain BH has FDR exactly $qc_m$.

## In plain words

Benjamini-Hochberg keeps the share of false discoveries low when the tests behave independently, or when they tend to move together in the same direction. If the tests can depend on each other in strange ways, false discoveries can pile up and the guarantee fails. This method repairs that by making the bar stricter by a fixed factor that grows slowly with the number of tests: about 3 for ten tests, about 5 for a hundred, about 7.5 for a thousand. After that change the method works for any pattern of dependence. You pay for this safety with fewer discoveries, so use it only when you cannot argue that the dependence is harmless.

## The problem

**Input.** P-values $p_1, \dots, p_m$ for hypotheses $H_1, \dots, H_m$, and a target FDR level $q \in (0, 1]$.

**Output.** The rejected set, and the adjusted p-values $\tilde p_i$, with $H_i$ rejected exactly when $\tilde p_i \le q$.

**Error rate controlled.** The false discovery rate $E[V/\max(R, 1)]$, strongly, over every configuration of true and false nulls.

**Dependence and level.** Arbitrary. If each null p-value is valid, $P(p_i \le u) \le u$, then $\text{FDR} \le (m_0/m)q$, in finite samples. No condition is put on the joint law. The bound is attained when $m_0 = m$, by the construction in the proof. Under independence BY is just BH at $q/c_m$, so its FDR is exactly $(m_0/m)q/c_m$.

## The algorithm

```pseudo id=main
BY(p₁, …, p_m, q)                       ▷ p-values in [0, 1], FDR level q
L1  c ← 1 + 1/2 + … + 1/m
L2  sort the indices so that p_(1) ≤ … ≤ p_(m)
L3  k ← m; while k ≥ 1 and m · c · p_(k) > k · q do
L4      k ← k − 1
L5  reject H_(1), …, H_(k)
L6  run ← 1; for r ← m down to 1 do       ▷ adjusted p-values
L7      run ← min(run, m · c · p_(r) / r); p̃_(r) ← run
L8  return (rejected set, p̃)
```

Lines L2 to L8 are the BH algorithm with $q$ replaced by $q/c_m$. The implementation computes $c_m$ as an exact fraction when the inputs are fractions, and with a correctly rounded sum of floats otherwise. For very large $m$, $c_m = \ln m + \gamma + 1/(2m) + O(m^{-2})$ with $\gamma = 0.5772\ldots$, see the [harmonic series](/harmonic-series/).

## Example

**Four p-values.** $p = (0.004, 0.011, 0.02, 0.6)$ at $q = 0.05$. Here $c_4 = 25/12 = 2.0833$.

| $k$ | $p_{(k)}$ | BH threshold $kq/m$ | BY threshold $kq/(mc_4)$ |
|---|---|---|---|
| 1 | 0.004 | 0.0125 | 0.006 |
| 2 | 0.011 | 0.025 | 0.012 |
| 3 | 0.02 | 0.0375 | 0.018 |
| 4 | 0.6 | 0.05 | 0.024 |

BH rejects three, since 0.02 is below 0.0375. BY rejects two: 0.011 is below 0.012, but 0.02 is above 0.018 and 0.6 is above 0.024.

**The 15 p-values of Benjamini and Hochberg (1995).** At $q = 0.05$, $c_{15} = 3.3182$, and the BY thresholds are $k \cdot 0.0010046$. The first three p-values, 0.0001, 0.0004 and 0.0019, pass, and none of 0.0095, 0.0201, ..., 0.3240 passes its threshold, so BY rejects three, against four for BH. The adjusted p-values start 0.005, 0.01, 0.0315, 0.1182, 0.2001.

**The worst case for BH, by hand.** Take $m = 2$, both nulls true, and this joint law. With probability $q$, pick one of the two indices at random, set its p-value to $q/2$ and the other to 1. With probability $q/2$, set both to $q$. Otherwise set both to 1. Each p-value then has $P(p_i \le q/2) = q/2$ and $P(p_i \le q) = q$, and it is valid. BH at $q$ rejects one hypothesis in the first case and two in the second, all of them false, so its FDR is $q + q/2 = qc_2$. BY at $q$ uses $q/c_2$ in place of $q$, and the same construction at $q/c_2$ shows that its FDR $q$ can be reached.

## Correctness

The [proof](proofs/correctness.md) shows $\text{FDR} \le (m_0/m)q$ under arbitrary dependence. Write $t_k = kq'/m$ for the thresholds at level $q' = q/c_m$, fix a true null $H_i$, and let $A_k$ be the event that $H_i$ is rejected and $R = k$. The events $A_k$ are disjoint, and $A_k \subseteq \{p_i \le t_k\}$ because a rejected hypothesis has $p_i \le t_R$. Writing $1/k$ as a telescoping sum gives
$$\sum_{k=1}^m \frac{P(A_k)}{k} = \sum_{j=1}^m \Big(\frac1j - \frac1{j+1}\Big)P\Big(\bigcup_{k \le j}A_k\Big) + \frac{P(\bigcup_k A_k)}{m+1} \le \sum_{j=1}^m \frac{t_j}{j(j+1)} + \frac{t_m}{m+1} = \frac{q'}{m}\Big(\sum_{j=2}^{m+1}\frac1j + \frac{m}{m+1}\Big) = \frac{q'}{m}c_m = \frac qm,$$
using only $P(\bigcup_{k \le j}A_k) \le P(p_i \le t_j) \le t_j$. Summing over the $m_0$ true nulls gives the bound. The same argument with $q$ in place of $q'$ shows that plain BH has $\text{FDR} \le (m_0/m)qc_m$, and the construction in the proof attains this when $m_0 = m$ and $qc_m \le 1$.

The tests check the rejections against BH at $q/c_m$ in exact rational arithmetic, and the bound under arbitrary dependence exactly. In the second check the null p-values are uniform on $\{1/24, \dots, 1\}$ and are coupled through random permutations of one shared uniform index, which gives many different dependence structures with valid marginals; the FDR is summed over the 24 outcomes as a fraction. The worst-case law is built for $m \le 5$ and gives FDR exactly $qc_m$ for BH and exactly $q$ for BY.

## Complexity

The harmonic number takes $\Theta(m)$ additions at line L1, the sort at line L2 takes $\Theta(m\log m)$ on a [real RAM](/real-ram/), and the rest takes $\Theta(m)$. So the time is $\Theta(m\log m)$ and the extra space $\Theta(m)$. As for BH, the rejections alone can be found in $\Theta(m)$ time by counting the p-values in buckets instead of sorting.

## Properties

- **FDR at $(m_0/m)q$ under any dependence.** Proved, in finite samples, with only valid null p-values.
- **Sharp.** No constant smaller than $c_m$ works for every dependence with BH's linear thresholds: the construction gives FDR $qc_m$ for BH at $q$.
- **Conservative in common cases.** Under independence or PRDS, BY has FDR $(m_0/m)q/c_m$ or less, far below $q$.
- **Between BH and Bonferroni.** Its first threshold is $q/(mc_m)$, below the Bonferroni level $q/m$. Its last threshold is $q/c_m$. For small $k$ it is stricter than Bonferroni at the same level, and for $k > c_m$ it is more lenient, so neither rejection set contains the other in general.
- **Monotone and step-up.** As for BH: lowering a p-value never removes a rejection.

## Variants and improvements

- **Other shapes.** Blanchard and Roquain showed that BH with the thresholds $q\beta(k)/m$ controls the FDR under any dependence when $\beta(k) = \sum_{j \le k}j\nu(\{j\})$ for a probability distribution $\nu$ on $\{1, \dots, m\}$. BY is the case $\nu(\{j\}) \propto 1/j$. Other choices of $\nu$ give more power where many rejections are expected.
- **e-BH.** For [e-values](/e-variable/), the BH rule $e_{(k)} \ge m/(kq)$ controls the FDR at $(m_0/m)q$ under any dependence without a harmonic factor. Turning p-values into e-values loses power, so this helps when the evidence comes as e-values in the first place.
- **Use the dependence.** When the joint law is known or can be resampled, permutation and bootstrap methods, as in the [Westfall-Young procedure](/westfall-young-procedure/) for the FWER, use the actual dependence and lose less.
- **FWER instead.** [Bonferroni](/bonferroni-correction/) and [Holm](/holm-bonferroni-method/) also work under any dependence, and for small $m$ they can reject as much as BY.

## When to use it

Use BY when the FDR is the right error rate, the dependence between the tests is unknown and could be negative, and a conservative result is acceptable. Examples are two-sided tests on correlated statistics with signs of both kinds, or tests that share data in complex ways. When the tests are independent, or positively dependent as for one-sided tests on positively correlated normal statistics, plain [BH](/benjamini-hochberg-procedure/) is valid and much more powerful. Many analysts use BH even with mild unknown dependence, because simulations rarely show its FDR above $q$; BY is the choice when a proof is required.

## Pitfalls

- **Using it by default.** Under independence BY controls the FDR at about $q/\ln m$, not $q$. Reporting "FDR at 5%" then hides a much stricter error rate and a large loss of power.
- **Writing $\ln m$ for $c_m$.** $\ln m < c_m$, so dividing by $\ln m$ gives a level that is too large and voids the proof. Use the exact sum, or $\ln m + 1$ as an upper bound.
- **Applying the factor twice.** Software that reports BY adjusted p-values already includes $c_m$; compare them with $q$, not with $q/c_m$.

## Implementations

## History

Benjamini and Hochberg (1995) proved control of the FDR for independent test statistics. Benjamini and Yekutieli (2001) extended it to positive regression dependence on the subset of true nulls, which covers one-sided tests on positively correlated normal statistics, and showed that dividing the level by $\sum_{i=1}^m 1/i$ gives control under any dependence. Later work showed that this factor is the best possible for the linear thresholds, and Blanchard and Roquain placed the method in a family of dependence-free step-up rules.

## References
