---
tag: T4RCRV
kind: algorithm
slug: hochberg-procedure
name: Hochberg procedure
aliases:
- Hochberg step-up procedure
area: statistics-and-inference/hypothesis-testing
level: core
summary: 'A step-up form of Holm: find the largest k with p_(k) <= alpha / (m - k + 1) and reject H_(1) to H_(k). It controls the FWER when the Simes inequality holds, as under independence or MTP2.'
model: real-ram
complexity:
  vars: {m: the number of hypotheses}
  time: {worst: Θ(m log m), best: Θ(m log m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1988
  people: [Yosef Hochberg, R. John Simes]
  note: Simes (1986) proposed a global test and conjectured a rule for single hypotheses. Hochberg (1988) gave the step-up procedure and proved that it controls the family-wise error rate whenever the Simes test is valid.
prereqs: [holm-bonferroni-method]
see_also: [bonferroni-correction, closed-testing-principle, benjamini-hochberg-procedure, westfall-young-procedure, family-wise-error-rate, multiple-comparisons-problem]
sources:
  - paper: doi:10.1093/biomet/75.4.800
    title: Yosef Hochberg, A sharper Bonferroni procedure for multiple tests of significance, Biometrika 75(4) (1988), pages 800 to 802
    locator: the step-up procedure with thresholds alpha / (m - k + 1), and its family-wise error control through closed testing with Simes tests
  - paper: doi:10.1093/biomet/73.3.751
    title: R. J. Simes, An improved Bonferroni procedure for multiple tests of significance, Biometrika 73(3) (1986), pages 751 to 754
    locator: the global test that rejects when p_(j) <= j alpha / n for some j, of size exactly alpha for independent continuous p-values
  - paper: doi:10.1093/biomet/75.2.383
    title: G. Hommel, A stagewise rejective multiple test procedure based on a modified Bonferroni test, Biometrika 75(2) (1988), pages 383 to 386
    locator: closed testing with Simes local tests, which rejects at least as much as Hochberg
  - paper: doi:10.1080/01621459.1997.10473682
    title: Sanat K. Sarkar and Chung-Kuei Chang, The Simes method for multiple hypothesis testing with positively dependent test statistics, Journal of the American Statistical Association 92(440) (1997), pages 1601 to 1608
    locator: the Simes inequality for positively dependent statistics, including equicorrelated normal and t statistics
  - paper: doi:10.1214/aos/1028144846
    title: Sanat K. Sarkar, Some probability inequalities for ordered MTP2 random variables, a proof of the Simes conjecture, The Annals of Statistics 26(2) (1998), pages 494 to 504
    locator: the Simes inequality for p-values that are multivariate totally positive of order 2
---

The Hochberg procedure uses the same thresholds as [Holm's method](/holm-bonferroni-method/), $\alpha/(m - k + 1)$ for the $k$-th smallest p-value, but it reads the sorted list from the other end. It starts at the largest p-value and moves down until it finds a $p_{(k)} \le \alpha/(m - k + 1)$; it then rejects $H_{(1)}, \dots, H_{(k)}$. Each hypothesis that Holm rejects, Hochberg rejects too. The price is an assumption: the [family-wise error rate](/family-wise-error-rate/) is at most $\alpha$ when the Simes inequality holds for the true nulls, which is the case under independence and under positive dependence of the MTP2 kind. Under negative dependence it can exceed $\alpha$. The adjusted p-value of $H_{(k)}$ is $\min_{j \ge k}\min(1, (m - j + 1)p_{(j)})$.

## In plain words

Holm's method checks the strongest result first and stops at the first weak one. Hochberg's method checks the weakest result first. If even the weakest result passes the ordinary level, every result is accepted as real. If not, it drops that result and checks the next weakest against a level twice as strict, and so on. The first result that passes takes all the stronger results with it. This finds every effect that Holm finds, and sometimes more, but it is safe only when the tests do not pull against each other. With independent tests, or tests that tend to move together, the chance of any false alarm stays below the chosen level.

## The problem

**Input.** P-values $p_1, \dots, p_m$ and a level $\alpha \in (0, 1)$. $I_0$ is the set of true nulls, $m_0 = |I_0|$, and $p_{(1)} \le \dots \le p_{(m)}$ are the sorted p-values.

**Output.** The rejected set $\{H_{(1)}, \dots, H_{(r)}\}$ with $r = \max\{k : p_{(k)} \le \alpha/(m - k + 1)\}$, or the empty set when there is no such $k$; and the adjusted p-values $\tilde p_{(k)} = \min_{j \ge k}\min(1, (m - j + 1)p_{(j)})$.

**Error rate controlled.** Strong control of the family-wise error rate, $P(V \ge 1) \le \alpha$ for every $I_0$, under the condition below.

**Dependence.** The control holds whenever the null p-values satisfy the Simes inequality,
$$P\Big(p_{(j:I_0)} \le \frac{j\alpha}{m_0} \text{ for some } j\Big) \le \alpha,$$
where $p_{(j:I_0)}$ is the $j$-th smallest null p-value. This holds with equality for independent uniform null p-values (Simes 1986, proved on this page), for MTP2 p-values (Sarkar 1998), and for several positively dependent families, among them one-sided tests on equicorrelated normal statistics with nonnegative correlation (Sarkar and Chang 1997). The last two are cited, not proved. It fails for some negatively dependent laws. The control is exact in finite samples, as an inequality, under these conditions.

## The algorithm

```pseudo id=main
HOCHBERG(p₁, …, p_m, α)                ▷ p-values in [0, 1], level α
L1  sort the indices so that p_(1) ≤ … ≤ p_(m)
L2  k ← m; while k ≥ 1 and (m − k + 1) · p_(k) > α do
L3      k ← k − 1
L4  reject H_(1), …, H_(k)              ▷ none when k = 0
L5  run ← 1; for j ← m down to 1 do     ▷ adjusted p-values
L6      run ← min(run, (m − j + 1) · p_(j))
L7      p̃_(j) ← run
L8  return (rejected set, p̃)
```

Lines L2 and L3 move down from the largest p-value. The first $k$ that passes is the largest one, and every smaller rank is rejected with it, whatever its own comparison gives.

## Example

**Where Hochberg gains.** For $p = 0.04$ and $0.045$ at $\alpha = 0.05$, Hochberg first checks $0.045 \le 0.05/1$, which holds, so it rejects both. Holm first checks $0.04 \le 0.05/2 = 0.025$, which fails, so it rejects neither.

**Four p-values.** $0.01, 0.02, 0.03, 0.045$ at $\alpha = 0.05$.

| $k$ | $p_{(k)}$ | threshold $\alpha/(m - k + 1)$ | $(m - k + 1)p_{(k)}$ | Hochberg adjusted | Holm adjusted |
|---|---|---|---|---|---|
| 1 | 0.01 | 0.0125 | 0.04 | 0.04 | 0.04 |
| 2 | 0.02 | 0.016667 | 0.06 | 0.045 | 0.06 |
| 3 | 0.03 | 0.025 | 0.06 | 0.045 | 0.06 |
| 4 | 0.045 | 0.05 | 0.045 | 0.045 | 0.06 |

Line L2 checks $k = 4$ first: $0.045 \le 0.05$ holds, so Hochberg rejects all four. Holm passes $k = 1$, fails at $k = 2$ and rejects one. The two columns of adjusted p-values come from the same products: Hochberg takes running minima from the bottom of the table, Holm running maxima from the top.

**Fifteen p-values.** On the 15 p-values of Benjamini and Hochberg (1995), line L2 checks $1.000 > 0.05$, $0.7590 > 0.025$, and so on down to $0.0095 > 0.05/12 = 0.004167$, and stops at $0.0019 \le 0.05/13 = 0.003846$. So $k = 3$ and Hochberg rejects the same 3 as Holm. The adjusted p-values are 0.0015, 0.0056, 0.0247, 0.114, 0.2211, 0.2682, 0.2682, 0.2752, 0.3213, and 1 for the last six. They are at most Holm's, which are 0.278 instead of 0.2682 for the sixth and seventh.

## Correctness

Two facts give the control. The first is combinatorial: every hypothesis that Hochberg rejects is also rejected by the closed testing procedure that tests each intersection $H_I$ with the Simes test, "reject when $p_{(j:I)} \le j\alpha/|I|$ for some $j$". With $a = m - r + 1$, at least $\max(1, |I| - a + 1)$ elements of any $I$ that holds a rejected hypothesis have rank at most $r$, so their p-values are at most $p_{(r)} \le \alpha/a$, and $(a - 1)(|I| - a) \ge 0$ gives the Simes condition. Taking $I = I_0$, a false rejection implies that the Simes test rejects $H_{I_0}$. The second fact is probabilistic: the Simes test of $H_{I_0}$ has level $\alpha$ under the dependence conditions above. For independent uniform p-values this is an equality, proved by induction on the number of p-values, conditioning on the largest. The [correctness proof](proofs/correctness.md) gives both parts in full, and an exact two-hypothesis law with uniform marginals under which the family-wise error rate is $3\alpha/2$. The tests check the inclusion against brute-force closed Simes testing over all subsets for $m \le 7$, the equality by exact counting on a grid and by simulation, and the counterexample in exact arithmetic.

## Complexity

On a [real RAM](/real-ram/), the sort at line L1 takes $\Theta(m\log m)$ comparisons, and lines L2 to L7 take $\Theta(m)$. So the time is $\Theta(m\log m)$, or $\Theta(m)$ on sorted input. The extra space is $\Theta(m)$. Closed Simes testing over all $2^m - 1$ intersections is exponential; the usual algorithm for Hommel's procedure reduces it to $\Theta(m^2)$ time, and Hochberg is a fast and slightly conservative shortcut of it.

**Numerical stability.** As for Holm, compare products $(m - k + 1)p_{(k)}$ with $\alpha$, so that the rejections agree with the adjusted p-values in floating point, and compute small p-values from the upper tail directly.

## Properties

- **Strong FWER control under the Simes condition.** Proved for independent p-values; cited for MTP2 and positively dependent normal statistics.
- **More powerful than Holm.** The rejected set always contains Holm's, and $\tilde p_i$ is at most Holm's adjusted p-value.
- **Less powerful than Hommel.** Every Hochberg rejection is a rejection of closed Simes testing, which can reject more.
- **Step-up.** One p-value that passes its threshold carries all smaller p-values with it, even those above their own thresholds.
- **Not valid under arbitrary dependence.** For two hypotheses there is a law with uniform marginals and family-wise error rate $3\alpha/2$.
- **Monotone.** Lowering any p-value never removes a rejection.

## Variants and improvements

- **Hommel's procedure.** Closed testing with Simes local tests, from Hommel (1988). It rejects at least as much as Hochberg under the same conditions. See the [closed testing principle](/closed-testing-principle/).
- **The Simes global test.** Reject the global null when $p_{(j)} \le j\alpha/m$ for some $j$. It is the local test inside Hochberg's and Hommel's methods, and its rule is the one of the [Benjamini-Hochberg procedure](/benjamini-hochberg-procedure/), which uses it for each $k$ to control a different error rate.
- **Rom's procedure.** Rom (1990) replaced Hochberg's thresholds with slightly larger ones computed so that the error rate is exactly $\alpha$ under independence.
- **Under arbitrary dependence.** Use [Holm's method](/holm-bonferroni-method/), or the Hommel-type correction of the Simes test by the factor $\sum_{i=1}^m 1/i$, the same factor as in the [Benjamini-Yekutieli procedure](/benjamini-yekutieli-procedure/).

## When to use it

Use Hochberg instead of Holm when the test statistics are independent or positively dependent, for example one-sided tests of several treatments against a shared control, which are positively correlated. The gain is largest when most of the p-values are moderately small, so that the largest one already passes. When the dependence is unknown or can be negative, as for two-sided tests on correlated statistics with no further structure, use Holm. When raw data are available, the [Westfall-Young procedure](/westfall-young-procedure/) often gains more than either.

## Pitfalls

- **Two-sided tests.** Positive dependence of the statistics does not always carry over to two-sided p-values, which are functions of absolute values. Check that the Simes inequality is known to hold for the family at hand before using Hochberg.
- **Reading the rule as Holm's.** Hochberg's comparison runs from the largest p-value down, and the first success rejects all smaller ones. Stopping at the first failure from the bottom gives Holm's method.
- **Adjusted p-values with the wrong running extreme.** Hochberg uses running minima from the largest p-value; Holm uses running maxima from the smallest. Mixing them gives adjusted p-values that do not match either rule.
- **Claiming the gain without the condition.** If a reviewer cannot check that the Simes inequality holds, report Holm.

## Implementations

## History

Simes (1986) proposed a global test that rejects the intersection of all nulls when $p_{(j)} \le j\alpha/m$ for some $j$, and proved that its size is exactly $\alpha$ for independent tests. He also suggested using it to reject single hypotheses, without a proof of control. Hochberg (1988) gave the step-up rule with Holm's thresholds and proved strong control through closed testing with Simes local tests, and in the same year Hommel published the full closed Simes procedure. Whether the Simes inequality holds under positive dependence was open for some years. Sarkar and Chang (1997) proved it for a class of positively dependent statistics, and Sarkar (1998) proved it for MTP2 p-values, the "Simes conjecture".

## References
