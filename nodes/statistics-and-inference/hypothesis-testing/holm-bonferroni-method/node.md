---
tag: 7A4AQ3
kind: algorithm
slug: holm-bonferroni-method
name: Holm-Bonferroni method
aliases:
- Holm's step-down procedure
- Holm procedure
area: statistics-and-inference/hypothesis-testing
level: core
summary: Sort the p-values and reject while the k-th smallest is at most alpha / (m - k + 1). It controls the FWER under any dependence and is uniformly more powerful than Bonferroni.
model: real-ram
complexity:
  vars: {m: the number of hypotheses}
  time: {worst: Θ(m log m), best: Θ(m log m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1979
  people: [Sture Holm]
  note: Holm published the sequentially rejective Bonferroni test in the Scandinavian Journal of Statistics in 1979. Its link to the closed testing principle of Marcus, Peritz and Gabriel (1976) was seen soon after.
prereqs: [bonferroni-correction, family-wise-error-rate]
see_also: [closed-testing-principle, hochberg-procedure, westfall-young-procedure, benjamini-hochberg-procedure, multiple-comparisons-problem, sorting-problem, order-statistic]
sources:
  - paper: doi:10.2307/4615733
    title: Sture Holm, A simple sequentially rejective multiple test procedure, Scandinavian Journal of Statistics 6(2) (1979), pages 65 to 70
    locator: the sequentially rejective Bonferroni test and the proof that it controls the multiple level of significance under any dependence
  - paper: doi:10.1093/biomet/63.3.655
    title: Ruth Marcus, Eric Peritz and K. R. Gabriel, On closed testing procedures with special reference to ordered analysis of variance, Biometrika 63(3) (1976), pages 655 to 660
    locator: the closed testing principle, of which Holm's method is the case with Bonferroni local tests
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Chapter 9 (multiple testing; the Holm procedure and its strong control of the family-wise error rate)
---

Holm's method tests $m$ hypotheses with strong control of the [family-wise error rate](/family-wise-error-rate/) under any dependence, as the [Bonferroni correction](/bonferroni-correction/) does, but it rejects at least as many hypotheses, and often more. It sorts the p-values, $p_{(1)} \le \dots \le p_{(m)}$, compares the smallest with $\alpha/m$, the next with $\alpha/(m - 1)$, and so on, with $p_{(k)}$ against $\alpha/(m - k + 1)$, and it stops at the first p-value that fails. Every hypothesis before the stop is rejected. The adjusted p-value of $H_{(k)}$ is $\max_{j \le k}\min(1, (m - j + 1)p_{(j)})$. The method is the shortcut of the [closed testing principle](/closed-testing-principle/) with a Bonferroni test for each intersection of nulls, which is one way to see why it works.

## In plain words

The Bonferroni correction makes every test pass a very strict level, as if all the hypotheses could be false alarms. Holm's method uses that strict level only for the most convincing result. Once that result is accepted as real, it no longer needs protection, so the next most convincing result is judged as if there were one test fewer, with a slightly easier level. Each step makes the level a little easier, until a result fails, and then the method stops. Nothing after the first failure is accepted. The guarantee is the same as for Bonferroni: the chance of at least one false alarm stays below the level you chose, whatever the relation between the tests.

## The problem

**Input.** P-values $p_1, \dots, p_m$ for hypotheses $H_1, \dots, H_m$, and a level $\alpha \in (0, 1)$. The set of true nulls is $I_0$, with $m_0$ elements, and every null p-value is valid: $P(p_i \le u) \le u$ for $i \in I_0$ and $u \in [0, 1]$.

**Output.** A set of rejected hypotheses, and the adjusted p-values $\tilde p_i$. For $\alpha < 1$, $H_i$ is rejected exactly when $\tilde p_i \le \alpha$.

**Error rate controlled.** Strong control of the family-wise error rate: $P(V \ge 1) \le \alpha$ for every configuration $I_0$ of true nulls, where $V$ is the number of true nulls rejected.

**Dependence.** Arbitrary. The control is exact in finite samples, as an inequality, and it uses only the validity of the null p-values.

**Power.** Holm rejects a superset of what Bonferroni rejects, on every data set, since its first threshold is $\alpha/m$ and the others are larger. The [Hochberg procedure](/hochberg-procedure/) rejects a superset of what Holm rejects, but it needs a condition on the dependence.

## The algorithm

```pseudo id=main
HOLM(p₁, …, p_m, α)                    ▷ p-values in [0, 1], level α
L1  sort the indices so that p_(1) ≤ … ≤ p_(m)
L2  k ← 1; while k ≤ m and (m − k + 1) · p_(k) ≤ α do
L3      reject H_(k)
L4      k ← k + 1
L5  run ← 0; for k ← 1 to m do         ▷ adjusted p-values
L6      run ← max(run, min(1, (m − k + 1) · p_(k)))
L7      p̃_(k) ← run
L8  return (rejected set, p̃)
```

The test at line L2 multiplies instead of dividing, so that the rejections agree with the adjusted p-values even in floating point. Tied p-values get the same decision: if $p_{(k)} = p_{(k+1)}$ and $H_{(k)}$ passes, then $H_{(k+1)}$ faces a larger threshold with the same value, so it passes too.

## Example

**Holm against Bonferroni.** Four p-values, $0.005, 0.011, 0.020, 0.040$, at $\alpha = 0.05$.

| $k$ | $p_{(k)}$ | threshold $\alpha/(m - k + 1)$ | L2 | adjusted $\tilde p_{(k)}$ |
|---|---|---|---|---|
| 1 | 0.005 | 0.0125 | reject | 0.02 |
| 2 | 0.011 | 0.016667 | reject | 0.033 |
| 3 | 0.020 | 0.025 | reject | 0.04 |
| 4 | 0.040 | 0.05 | reject | 0.04 |

Holm rejects all four. Bonferroni compares each with $0.0125$ and rejects only the first two. The last adjusted p-value is $\max(0.04, 1 \cdot 0.04) = 0.04$; at $k = 3$ it is $\max(0.033, 2 \cdot 0.02) = 0.04$.

**The stop rule.** For $0.02, 0.02, 0.9$ at $\alpha = 0.05$, the first comparison is $0.02 > 0.05/3 = 0.016667$, so Holm stops and rejects nothing, even though $0.02 \le 0.05/2$. A step-up rule would reject both: this is the case where [Hochberg's procedure](/hochberg-procedure/) gains.

**Fifteen p-values.** On the 15 p-values of Benjamini and Hochberg (1995) (0.0001, 0.0004, 0.0019, 0.0095, 0.0201, 0.0278, 0.0298, 0.0344, 0.0459, 0.3240, 0.4262, 0.5719, 0.6528, 0.7590, 1.000), the thresholds start at 0.003333, 0.003571, 0.003846 and 0.004167. The first three p-values pass and 0.0095 fails, so Holm rejects 3, as Bonferroni does. The adjusted p-values are 0.0015, 0.0056, 0.0247, 0.114, 0.2211, 0.278, 0.278, 0.278, 0.3213, and 1 for the last six. The seventh and eighth are raised from 0.2682 and 0.2752 to 0.278 by the running maximum at line L6.

## Correctness

The direct argument is short. Let $j^*$ be the rank of the smallest p-value among the true nulls. Holm rejects a prefix of the sorted list, so it rejects some true null only if it reaches and rejects $H_{(j^*)}$, which needs $p_{(j^*)} \le \alpha/(m - j^* + 1)$. The $j^* - 1$ hypotheses before it are all false nulls, so $j^* - 1 \le m - m_0$, and the threshold is at most $\alpha/m_0$. So a false rejection implies $\min_{i \in I_0}p_i \le \alpha/m_0$, and the union bound over the $m_0$ true nulls gives probability at most $\alpha$.

The second argument shows where the method comes from. Under the [closed testing principle](/closed-testing-principle/), test each intersection $H_I = \bigcap_{i \in I}H_i$ with the Bonferroni test "reject when $|I|\min_{i \in I}p_i \le \alpha$", and reject $H_i$ when every $H_I$ with $i \in I$ is rejected. The worst subset for $H_{(k)}$ is a tail $\{(j), \dots, (m)\}$ with $j \le k$, so closed testing rejects $H_{(k)}$ exactly when $(m - j + 1)p_{(j)} \le \alpha$ for all $j \le k$, which is Holm's rule. The [correctness proof](proofs/correctness.md) gives both arguments in full and the formula for the adjusted p-values. The tests compare Holm with closed testing over all $2^m - 1$ intersections, in exact rational arithmetic, for $m \le 8$.

## Complexity

On a [real RAM](/real-ram/), sorting at line L1 takes $\Theta(m\log m)$ comparisons with any optimal comparison sort, which is the [sorting problem](/sorting-problem/). The loops at lines L2 to L7 take $\Theta(m)$. So the time is $\Theta(m\log m)$, or $\Theta(m)$ when the p-values arrive sorted. The extra space is $\Theta(m)$ for the order and the outputs.

Only the rejections are cheaper: the method rejects the $r$ smallest p-values for some $r$, and a partial sort or repeated [selection](/order-statistic/) finds them in $O(m + r\log m)$ time with a heap. Closed testing done naively needs all $2^m - 1$ intersections, so the shortcut turns an exponential computation into a sort.

**Numerical stability.** Compare $(m - k + 1)p_{(k)}$ with $\alpha$ directly from the p-values. Do not form p-values as $1 - \text{CDF}$, which rounds small p-values to 0 or loses their digits; compute them from the upper tail.

## Properties

- **Strong FWER control under any dependence.** Proved above, with no condition except the validity of the null p-values.
- **Uniformly more powerful than Bonferroni.** Every hypothesis that Bonferroni rejects, Holm rejects. The adjusted p-values satisfy $\tilde p_i \le \min(1, mp_i)$.
- **Step-down.** Holm starts from the smallest p-value and stops at the first acceptance. Its decisions depend on all the p-values, through their ranks.
- **Monotone.** Lowering any p-value never removes a rejection.
- **Consonant.** When the closed procedure with Bonferroni local tests rejects an intersection $H_I$, Holm rejects the $H_i$ with the smallest p-value in $I$. So the shortcut loses no single hypothesis that the full closed procedure would reject.

## Variants and improvements

- **Holm-Šidák.** Replace $\alpha/(m - k + 1)$ by $1 - (1 - \alpha)^{1/(m - k + 1)}$. This is valid under independence and for two-sided tests on a normal vector, and a little more powerful.
- **Weighted Holm.** With weights $w_i \ge 0$, compare $p_i/w_i$, and at each step test the remaining $p_i$ against $w_i\alpha/\sum_{j \text{ remaining}}w_j$. This is closed testing with weighted Bonferroni local tests.
- **Shaffer's method.** When the hypotheses are logically related, as pairwise comparisons of means are, some sets of true nulls are impossible, and the threshold at step $k$ can use the largest number of nulls that can still be true. Shaffer proposed this in 1986.
- **Hochberg and Hommel.** Closed testing with Simes local tests gives Hommel's method; its conservative shortcut is [Hochberg's](/hochberg-procedure/) step-up rule with Holm's thresholds. Both need independence or positive dependence.
- **Resampling.** The [Westfall-Young](/westfall-young-procedure/) step-down method replaces $\alpha/(m - k + 1)$ by a permutation quantile of the maximum statistic over the remaining hypotheses, which uses the dependence.
- **Gatekeeping and graphical methods.** When the hypotheses have an order of importance, closed testing with weighted Bonferroni tests passes the level of a rejected hypothesis on to others. Holm is the case where the level is shared equally.

## When to use it

Use Holm wherever you would use Bonferroni and all p-values are known together: the guarantee and the assumptions are the same, and it is never worse. It is the standard default for a small family of tests with strict error control, such as the secondary end points of a trial. When the tests are independent or positively dependent, the [Hochberg procedure](/hochberg-procedure/) gains a little power. When raw data are available and the tests are correlated, the [Westfall-Young procedure](/westfall-young-procedure/) gains more. When $m$ is large, control the [false discovery rate](/false-discovery-rate/) instead.

## Pitfalls

- **Continuing after a failure.** Holm stops at the first acceptance. Comparing every $p_{(k)}$ with its threshold and rejecting each that passes is not Holm's method and does not control the error rate.
- **Adjusted p-values without the running maximum.** $(m - k + 1)p_{(k)}$ alone can decrease in $k$; without line L6, a later hypothesis can get a smaller adjusted p-value than an earlier one and be "rejected" after the stop.
- **Confidence intervals.** Bonferroni gives simultaneous intervals at level $1 - \alpha/m$ each. Holm's step-down thresholds do not turn into intervals in the same simple way, so do not report intervals at level $1 - \alpha/(m - k + 1)$ as if they were simultaneous.
- **Changing $m$.** Adding or removing hypotheses after seeing the data changes the thresholds and voids the guarantee.

## Implementations

## History

Sture Holm published the method in 1979 as a "sequentially rejective Bonferroni test", with a direct proof of strong control under any dependence. Marcus, Peritz and Gabriel had introduced the closed testing principle three years before, and it was soon seen that Holm's method is the shortcut of closed testing with Bonferroni local tests. Šidák's inequality gave the Holm-Šidák variant. Hochberg (1988) turned the order around into a step-up rule, and Hommel (1988) gave the full closed version with Simes tests. Weighted and graphical versions, used to test ordered families of end points in clinical trials, are later extensions of the same idea.

## References
