---
tag: DBDQ24
kind: algorithm
slug: bonferroni-correction
name: Bonferroni correction
aliases:
- Bonferroni procedure
- Bonferroni adjustment
area: statistics-and-inference/hypothesis-testing
level: intro
summary: Tests each of m hypotheses at level alpha / m. By the union bound the family-wise error rate is at most alpha under any dependence.
model: real-ram
complexity:
  vars: {m: the number of hypotheses}
  time: {worst: Θ(m), best: Θ(m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 1961
  people: [Carlo Emilio Bonferroni, Olive Jean Dunn]
  note: Bonferroni published his probability inequalities in 1936. Dunn used the first of them in 1961 to make simultaneous confidence intervals, and the correction for tests takes its name from the inequality.
prereqs: [family-wise-error-rate, p-value, union-bound]
see_also: [multiple-comparisons-problem, holm-bonferroni-method, hochberg-procedure, closed-testing-principle, westfall-young-procedure, benjamini-hochberg-procedure, fisher-combined-probability-test, tukey-hsd]
sources:
  - paper: doi:10.1080/01621459.1961.10482090
    title: Olive Jean Dunn, Multiple comparisons among means, Journal of the American Statistical Association 56(293) (1961), pages 52 to 64
    locator: the intervals for m linear combinations of means at level alpha / m each, from the first Bonferroni inequality
  - paper: doi:10.1080/01621459.1967.10482935
    title: Zbyněk Šidák, Rectangular confidence regions for the means of multivariate normal distributions, Journal of the American Statistical Association 62(318) (1967), pages 626 to 633
    locator: the inequality P(all |X_i| <= c_i) >= product of P(|X_i| <= c_i) for a normal vector, which gives the level 1 - (1 - alpha)^(1/m)
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Chapter 9, Section 9.1 (the family-wise error rate and the Bonferroni procedure)
---

The Bonferroni correction is the simplest way to test $m$ hypotheses at once. It tests each hypothesis at level $\alpha/m$ instead of $\alpha$, so it rejects $H_i$ when its p-value satisfies $p_i \le \alpha/m$. Equivalently, it reports the adjusted p-value $\tilde p_i = \min(1, mp_i)$ and rejects when $\tilde p_i \le \alpha$. The [union bound](/union-bound/) then shows that the [family-wise error rate](/family-wise-error-rate/), the probability of one or more false rejections, is at most $(m_0/m)\alpha \le \alpha$. This holds for every set of true nulls and every dependence between the tests, with no assumption except that each null p-value is valid. The price is power: the threshold falls like $1/m$, and [Holm's method](/holm-bonferroni-method/) rejects at least as much under the same conditions.

## In plain words

If you run many tests and each one has a small chance of a false alarm, the chance of at least one false alarm grows with the number of tests. With twenty tests at the usual 5% level, it is about 64% when nothing is going on. The Bonferroni correction splits the allowed error between the tests. Each test gets an equal share, so if you run twenty tests, each one must pass a level twenty times stricter. The chance of at least one false alarm is then at most the sum of the shares, which is the level you wanted. This is true whatever the relation between the tests. The cost is that real effects must be much stronger to pass.

## The problem

**Input.** P-values $p_1, \dots, p_m$ for hypotheses $H_1, \dots, H_m$, and a level $\alpha \in (0, 1)$. The set of true nulls is $I_0$, with $m_0 = |I_0|$ elements. Each null p-value is valid: $P(p_i \le u) \le u$ for all $u \in [0, 1]$ and all $i \in I_0$. Nothing is assumed about the joint law of the p-values.

**Output.** The set of rejected hypotheses $\{i : p_i \le \alpha/m\}$ and the adjusted p-values $\tilde p_i = \min(1, mp_i)$. For $\alpha < 1$, $H_i$ is rejected exactly when $\tilde p_i \le \alpha$, so the adjusted p-value is the smallest level at which the procedure rejects $H_i$.

**Error rate controlled.** Strong control of the [family-wise error rate](/family-wise-error-rate/): with $V$ the number of true nulls rejected, $P(V \ge 1) \le (m_0/m)\alpha \le \alpha$ for every $I_0$, and not only under the global null. It also controls the expected number of false rejections, $E[V] \le (m_0/m)\alpha$, which is a stronger statement.

**Dependence.** Arbitrary. The control is exact in finite samples, as an inequality. It is attained: when the events $\{p_i \le \alpha/m\}$, $i \in I_0$, are disjoint and every null p-value is uniform, the family-wise error rate is exactly $(m_0/m)\alpha$.

## The algorithm

```pseudo id=main
BONFERRONI(p₁, …, p_m, α)          ▷ p-values in [0, 1], level α
L1  c ← α / m                        ▷ the per-test level
L2  for i ← 1 to m do
L3      rejectᵢ ← (pᵢ ≤ c)
L4      p̃ᵢ ← min(1, m · pᵢ)          ▷ the adjusted p-value
L5  return (reject, p̃)
```

The order of the p-values does not matter, and no sorting is needed.

## Example

**Fifteen p-values.** Benjamini and Hochberg (1995) used these 15 p-values from a clinical trial: 0.0001, 0.0004, 0.0019, 0.0095, 0.0201, 0.0278, 0.0298, 0.0344, 0.0459, 0.3240, 0.4262, 0.5719, 0.6528, 0.7590, 1.000. Take $\alpha = 0.05$.

| step | value |
|---|---|
| L1: $c = 0.05/15$ | 0.003333 |
| L3: $p_i \le c$ | true for 0.0001, 0.0004, 0.0019; false from 0.0095 on |
| L4: $\tilde p_i = \min(1, 15p_i)$, first nine | 0.0015, 0.006, 0.0285, 0.1425, 0.3015, 0.417, 0.447, 0.516, 0.6885 |
| L4: last six | 1, 1, 1, 1, 1, 1 |

Bonferroni rejects 3 hypotheses. Nine of the raw p-values are below 0.05, so testing each at 0.05 would reject 9. [Holm's method](/holm-bonferroni-method/) also rejects 3 here, and the [Benjamini-Hochberg procedure](/benjamini-hochberg-procedure/) at $q = 0.05$ rejects 4, because it controls a weaker error rate.

**How the threshold shrinks.** The table gives, for independent tests at $\alpha = 0.05$ with all nulls true, the family-wise error rate with no correction, $1 - 0.95^m$, and the per-test levels of Bonferroni and of Šidák, $1 - 0.95^{1/m}$.

| $m$ | no correction | Bonferroni $\alpha/m$ | Šidák |
|---|---|---|---|
| 1 | 0.05 | 0.05 | 0.05 |
| 5 | 0.2262 | 0.01 | 0.010206 |
| 10 | 0.4013 | 0.005 | 0.005116 |
| 20 | 0.6415 | 0.0025 | 0.002561 |
| 100 | 0.9941 | 0.0005 | 0.000513 |

The Šidák level is a little larger, but the two differ by less than 3% of $\alpha/m$ at $\alpha = 0.05$. On the 15 p-values above, the Šidák level is 0.0034137, and it rejects the same 3 hypotheses.

## Correctness

The family-wise error event is the union over $i \in I_0$ of the events $\{p_i \le \alpha/m\}$. By the union bound its probability is at most $\sum_{i \in I_0}P(p_i \le \alpha/m) \le m_0 \cdot \alpha/m$, using only the validity of each null p-value. No independence is used, and $I_0$ is arbitrary, so the control is strong. The same sum bounds $E[V]$, by linearity of expectation. The bound is attained by the law in which $p_i = (U + i/m) \bmod 1$ with one uniform $U$: each $p_i$ is uniform, and the events $\{p_i \le \alpha/m\}$ are disjoint. The [correctness proof](proofs/correctness.md) gives these steps and the equivalence of the two forms of the output. The tests check the attained case exactly, with fractions, on a grid.

## Complexity

On a [real RAM](/real-ram/), the loop at lines L2 to L4 does one comparison and one multiplication per hypothesis, so the time is $\Theta(m)$ in every case. The output takes $\Theta(m)$ space; a streaming version that reads the p-values one at a time and reports each decision uses $O(1)$ extra space, but it must know $m$ in advance.

**Numerical stability.** There is no cancellation. Compare $p_i \le \alpha/m$ or $mp_i \le \alpha$, never $1 - p_i \ge 1 - \alpha/m$, which loses all digits of a small $p_i$. For the Šidák level, $1 - (1 - \alpha)^{1/m}$ cancels for large $m$: with $\alpha = 0.05$ and $m = 10^6$, it is about $5.1 \times 10^{-8}$, a difference of two numbers near 1. The implementation computes it as $-\operatorname{expm1}(\operatorname{log1p}(-\alpha)/m)$, which keeps full relative accuracy.

## Properties

- **Strong FWER control under any dependence.** Proved by the union bound, with no condition on the joint law.
- **Single-step.** The threshold of each test does not depend on the other p-values. Each decision can be made in isolation, in any order.
- **Conservative under dependence.** With positively dependent tests, the true family-wise error rate is below $\alpha$, often far below. If all $m$ p-values are equal, it is $\alpha/m$.
- **Nearly exact under independence for small $\alpha$.** With independent uniform nulls the error rate is $1 - (1 - \alpha/m)^{m_0}$, which is between $\alpha - \alpha^2/2$ and $\alpha$ when $m_0 = m$.
- **Dominated by Holm.** [Holm's method](/holm-bonferroni-method/) rejects every hypothesis that Bonferroni rejects, with the same guarantee.
- **Controls the expected number of false rejections.** $E[V] \le (m_0/m)\alpha$, which bounds the per-family error rate as well.

## Variants and improvements

- **Weighted Bonferroni.** Give $H_i$ the level $w_i\alpha$ with $w_i \ge 0$ and $\sum_i w_i \le 1$. The union bound gives the same control. Weights can come from prior knowledge or from independent data, and they gain power when they put more of $\alpha$ on the false nulls.
- **Šidák correction.** Test each hypothesis at $1 - (1 - \alpha)^{1/m}$. With independent tests the family-wise error rate under the global null is exactly $\alpha$. Šidák (1967) proved the inequality behind it for two-sided tests on a multivariate normal vector with any correlation, so it is valid there too. It can fail for other kinds of dependence, where Bonferroni cannot.
- **Holm's step-down method.** Sort the p-values and compare the $k$-th smallest with $\alpha/(m - k + 1)$. It is uniformly more powerful, with the same assumptions. See [Holm-Bonferroni method](/holm-bonferroni-method/).
- **Hochberg's step-up method.** The same thresholds used from the largest p-value down. It is more powerful again, but it needs independence or positive dependence. See [Hochberg procedure](/hochberg-procedure/).
- **Resampling.** The [Westfall-Young procedure](/westfall-young-procedure/) replaces $\alpha/m$ by a quantile of the minimum p-value under permutations, which adapts to the dependence.
- **Bonferroni confidence intervals.** For $m$ parameters, use $m$ intervals at level $1 - \alpha/m$ each. All $m$ cover at the same time with probability at least $1 - \alpha$. This is Dunn's use of the inequality. For all pairwise differences of normal means, [Tukey's HSD](/tukey-hsd/) is shorter, and for all contrasts, [Scheffé's method](/scheffe-method/).

## When to use it

Use Bonferroni when the number of tests is small, when the dependence between the tests is unknown, and when the control of each false rejection matters, as in a clinical trial with a few primary end points. It is also the right choice when each decision must be made on its own, before the other p-values exist. When the p-values are all available, use [Holm's method](/holm-bonferroni-method/) instead: it has the same guarantee and never rejects less. When $m$ is large and some false rejections are acceptable, control the [false discovery rate](/false-discovery-rate/) instead, for example with the [Benjamini-Hochberg procedure](/benjamini-hochberg-procedure/).

## Pitfalls

- **Counting the tests.** $m$ is the number of tests that were done or could have been reported, not the number that look interesting. Choosing the tests after seeing the data, and correcting only for those, does not control the error rate.
- **Weak and strong control are different.** Bonferroni controls the error for every set of true nulls, but a single global test built from it, "reject the global null if any $p_i \le \alpha/m$", has low power against many small effects. Use [Fisher's method](/fisher-combined-probability-test/) for that question.
- **Highly correlated tests.** With strongly correlated statistics, as for nearby genetic markers, Bonferroni is very conservative. Permutation methods such as [Westfall-Young](/westfall-young-procedure/) can be much more powerful.
- **Adjusted p-values above 1.** $mp_i$ can exceed 1. Cap it at 1, as line L4 does; a reported "adjusted p-value" of 3 is a bug.
- **Not a statement about one test.** A hypothesis that passes $\alpha/m$ is not "significant at $\alpha/m$" in the usual sense; the guarantee is about the family. A result that fails it may still be a true effect: Bonferroni trades power for error control.

## Implementations

## History

Carlo Emilio Bonferroni published his inequalities for the probability of a union of events in 1936, in a paper on the statistical theory of classes. The first of them, $P(\bigcup_i A_i) \le \sum_i P(A_i)$, is much older and goes back to Boole. Olive Jean Dunn used it in 1961 to build simultaneous confidence intervals for several means, each at level $1 - \alpha/m$, and the name "Bonferroni correction" comes from this use. Šidák (1967) proved that, for normal vectors, the product of the marginal probabilities is a lower bound for the joint coverage, which gives the slightly larger per-test level $1 - (1 - \alpha)^{1/m}$. Holm (1979) showed that a sequential use of the same inequality rejects more, with the same guarantee.

## References
