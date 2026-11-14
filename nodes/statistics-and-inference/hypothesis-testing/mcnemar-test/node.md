---
tag: H919BT
kind: algorithm
slug: mcnemar-test
name: McNemar's test
aliases:
- McNemar test for paired proportions
area: statistics-and-inference/hypothesis-testing
level: core
summary: Tests a change in a paired binary outcome using only the discordant pairs, whose split is binomial with p = 1/2 under the null.
model: real-ram
complexity:
  vars: {m: the number of discordant pairs b + c}
  time: {worst: Θ(m), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1947
  people: [Quinn McNemar, Allen L. Edwards]
  note: McNemar gave the statistic (b - c)^2/(b + c) for correlated proportions in 1947. Edwards proposed the continuity correction in 1948.
prereqs: [binomial-test, statistical-hypothesis-test, p-value]
see_also: [fisher-exact-test, sign-test, chi-squared-test-of-independence, chi-squared-goodness-of-fit-test, binomial-distribution, score-test, central-limit-theorem, test-interval-duality]
sources:
  - paper: doi:10.1007/BF02295996
    title: Quinn McNemar, Note on the sampling error of the difference between correlated proportions or percentages, Psychometrika 12(2), 1947
    locator: pp. 153 to 157 (the statistic for the change between two correlated proportions)
  - paper: "Allen L. Edwards, Note on the correction for continuity in testing the significance of the difference between correlated proportions, Psychometrika 13, 1948"
    title: Edwards 1948
    locator: the corrected statistic (|b - c| - 1)^2/(b + c)
  - book: isbn:9780470463635
    title: Alan Agresti, Categorical Data Analysis, third edition, Wiley, 2013
    locator: Chapter 11 (models for matched pairs, with the comparison of dependent proportions and McNemar's test)
---

McNemar's test checks whether a binary outcome changes between two paired measurements, such as the same people before and after a treatment, or the two members of matched pairs. Only the discordant pairs, those that changed, carry information about the change. If there is no change in the margins, a discordant pair is equally likely to go either way, so given the number $m = b + c$ of discordant pairs, the count $b$ is $\text{Binomial}(m, 1/2)$. The exact test is a [binomial test](/binomial-test/) on that count, and the classical statistic $(b - c)^2/(b + c)$ is its large-sample chi-square form.

## In plain words

Ask 100 people a yes-or-no question twice, before and after a debate. Most give the same answer both times, and they tell you nothing about a shift. Look only at the people who changed their answer. If the debate had no effect, a changer is as likely to switch from yes to no as from no to yes, like a fair coin. So the question becomes: is the split among the changers too lopsided for a fair coin? With 15 changes one way and 5 the other, the chance of a split at least that uneven is about 4%.

## The problem

**Model.** $N$ independent pairs with a binary outcome on each member. The paired table is

| | second: yes | second: no |
|---|---|---|
| first: yes | $a$ | $b$ |
| first: no | $c$ | $d$ |

with cell probabilities $\pi_{11}, \pi_{12}, \pi_{21}, \pi_{22}$. The first margin has $P(\text{yes}) = \pi_{11} + \pi_{12}$ and the second $\pi_{11} + \pi_{21}$.

**Hypotheses.** $H_0$: marginal homogeneity, $\pi_{11} + \pi_{12} = \pi_{11} + \pi_{21}$, which is $\pi_{12} = \pi_{21}$. $H_1$: $\pi_{12} \ne \pi_{21}$. The code is two-sided.

**Statistic.** The discordant counts $b$ and $c$, with $m = b + c$; and $X^2 = (b - c)^2/(b + c)$.

**Null distribution.** Exact and conditional: given $m$, $b \sim \text{Binomial}(m, 1/2)$, whatever the concordant cells are. Asymptotic: $X^2$ tends to the chi-square law with 1 degree of freedom as the number of pairs grows with $\pi_{12} + \pi_{21} > 0$ fixed.

**Rejection rule and size.** Reject when $p \le \alpha$. The exact test has size at most $\alpha$ for every $m$ (proved). The asymptotic test can exceed $\alpha$ for small $m$; the corrected test stayed below $\alpha$ for every $m \le 300$ in an exact computation (measured, not proved).

**P-values.** Exact: $p = \min\{1, 2 P(B \le \min(b, c))\}$ for $B \sim \text{Binomial}(m, 1/2)$; since the law is symmetric, doubling the smaller tail and the minimum-likelihood rule agree. Asymptotic: $p = P(\chi^2_1 > X^2)$. Corrected (Edwards): $p = P(\chi^2_1 > (\lvert b - c \rvert - 1)^2/(b + c))$, with $\lvert b - c \rvert - 1$ floored at 0.

**Sensitivity and power.** The power depends on the discordant probabilities, not on the margins alone: given $m$, $b \sim \text{Binomial}(m, \pi_{12}/(\pi_{12} + \pi_{21}))$. Many concordant pairs mean few informative pairs. For $N = 100$, $\pi_{12} = 0.15$ and $\pi_{21} = 0.05$, the exact two-sided test at $\alpha = 0.05$ has power $0.544$ (computed by summing over all tables).

## The algorithm

```pseudo id=main
MCNEMAR(b, c, method)
L1  m ← b + c;  if m = 0 then return 1
L2  if method = exact then
L3      s ← C(m, 0) + C(m, 1) + ... + C(m, min(b, c))     ▷ exact integers, C(m, k+1) = C(m, k)(m - k)/(k + 1)
L4      return min(1, 2 s / 2^m)
L5  X2 ← (b - c)^2 / m, or max(0, |b - c| - 1)^2 / m if method = corrected
L6  return P(χ²₁ > X2)                                 ▷ upper tail of chi-square with 1 degree of freedom
```

The concordant counts $a$ and $d$ are not inputs. Line L3 is exact, so the p-value is a `Fraction` before the final conversion. Line L6 uses `chi2_sf` from the shared helper module, the regularized upper incomplete gamma function $Q(1/2, X^2/2)$; with 1 degree of freedom it equals $\operatorname{erfc}(\sqrt{X^2/2})$.

## Example

**Opinion before and after a debate.** Of 100 people, $a = 40$ said yes both times, $d = 40$ said no both times, $b = 15$ changed from yes to no and $c = 5$ from no to yes. Support fell from 55% to 45%.

- Asymptotic: $X^2 = (15 - 5)^2/20 = 5.0$, $p = 0.02535$.
- Corrected: $X^2 = 9^2/20 = 4.05$, $p = 0.04417$.
- Exact: $m = 20$, $P(B \le 5) = (1 + 20 + 190 + 1140 + 4845 + 15504)/2^{20} = 21700/1048576$, so $p = 43400/1048576 = 5425/131072 = 0.04139$.

All three reject at $\alpha = 0.05$, the exact one only just. Treating the two answers as independent samples instead, a two-sample chi-square test on $55/100$ against $45/100$ gives $X^2 = 2.0$ and $p = 0.157$: ignoring the pairing throws away the fact that 80 people did not change.

**Small counts.** With $b = 9$, $c = 2$: asymptotic $p = 0.0348$, corrected $0.0704$, exact $67/1024 = 0.0654$. With $b = 6$, $c = 1$: asymptotic $0.0588$, corrected $0.1306$, exact $1/8$. The asymptotic test is the most liberal. With $b = 4$, $c = 0$ it gives $X^2 = 4$ and $p = 0.0455$, so it rejects, while the exact p-value is $2/16 = 0.125$.

The tests check every number above, the fractions exactly.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The pairs are independent, so given which pairs are discordant, each one is (yes, no) with probability $\theta = \pi_{12}/(\pi_{12} + \pi_{21})$ independently, and $\theta = 1/2$ under $H_0$. The exact p-value is the tail $P(\lvert 2B - m \rvert \ge \lvert b - c \rvert)$, which by symmetry is twice the lower tail at $\min(b, c)$, and the tail lemma of the binomial test gives size at most $\alpha$ given $m$, hence overall. Algebra gives $X^2 = Z^2$ with $Z = (b - m/2)/\sqrt{m/4}$, the standardized binomial count, so the [central limit theorem](/central-limit-theorem/) gives the chi-square limit as $m \to \infty$.

## Complexity

The exact method sums $\min(b, c) + 1$ binomial coefficients, each from the previous one with one multiplication and one exact division, so it takes $\Theta(\min(b, c) + 1)$ arithmetic operations, at most $\Theta(m)$, on integers of at most $m$ bits. The asymptotic and corrected methods take $\Theta(1)$ operations plus one incomplete gamma evaluation. Only a running sum and one term are stored. For very large $m$ the exact tail can instead be found from the regularized incomplete beta function in floating point, as on the binomial test page.

## Properties

- **Exact test: conservative.** Given $m$, the exact size at $\alpha = 0.05$ is at most 0.05 and jumps with $m$: for example 0.0414 at $m = 20$ and 0.0129 at $m = 14$.
- **Asymptotic test: can be liberal.** Given $m$, its exact size exceeded 0.05 for 144 of the values $m = 0, \ldots, 300$, with the worst case $0.125$ at $m = 4$. Averaged over $m$, for $N = 50$ pairs with $\pi_{12} = \pi_{21} = 0.1$, the sizes are $0.0221$ (exact), $0.0429$ (asymptotic) and $0.0218$ (corrected); for $N = 100$ and $\pi_{12} = \pi_{21} = 0.15$, the asymptotic size is $0.0520$, above $\alpha$. These are exact sums over all tables; a simulation with 10000 repetitions (seed 1) agrees for $N = 50$ within sampling error.
- **Corrected test: close to exact.** Edwards's correction gives sizes close to the exact test's, sometimes smaller: at $m = 17$ the corrected size is $0.0127$ while the exact size is $0.0490$.
- **Power.** For the alternative in the problem section, the powers at $\alpha = 0.05$ are $0.544$ (exact), $0.527$ (corrected) and $0.639$ (asymptotic, which does not hold its size).
- **Uses only discordant pairs.** Adding concordant pairs does not change the test. This is right for testing the margins, but the size of the change in proportions, $(b - c)/N$, does depend on $N$.
- **Same as a score test.** $X^2$ is the score statistic for $\pi_{12} = \pi_{21}$ in the multinomial model, and also the square of the [sign test](/sign-test/) statistic on the pair differences.

## Variants and improvements

- **Mid-p value.** Replace $P(B \le \min(b, c))$ by $P(B < \min(b, c)) + \tfrac12 P(B = \min(b, c))$ before doubling. It is less conservative but can exceed $\alpha$.
- **Confidence interval.** For the difference of the paired proportions $\delta = (\pi_{12} - \pi_{21})$, the estimate is $(b - c)/N$ with variance estimate $\big((b + c) - (b - c)^2/N\big)/N^2$; a Wald interval follows, and score-type intervals behave better for small counts. For $\theta = \pi_{12}/(\pi_{12} + \pi_{21})$, the [Clopper-Pearson interval](/clopper-pearson-interval/) on $b$ out of $m$ inverts the exact test, by [test-interval duality](/test-interval-duality/).
- **More categories.** For a $k \times k$ paired table, Bowker's test of symmetry (1948) and the Stuart-Maxwell test of marginal homogeneity extend McNemar's test. For a binary outcome under $k$ conditions, Cochran's Q test (1950) does.
- **Stratified pairs.** With strata, the conditional logistic model for matched pairs generalizes the test, and the Mantel-Haenszel form combines the strata.

## When to use it

Use it for a binary outcome measured twice on the same units, or on matched pairs, when the question is whether the proportion of "yes" changed. Use the exact form when $b + c$ is small, say below 25 to 30, or always, since it is cheap. For independent samples use [Fisher's exact test](/fisher-exact-test/) or the [chi-squared test](/chi-squared-test-of-independence/) instead.

## Pitfalls

- **Testing association instead of change.** A chi-squared test of independence on the paired table asks whether the first and second answers are related, which they nearly always are. It does not test a change in the margins.
- **Ignoring the pairing.** Treating the two measurements as independent samples gets the variance wrong; in the example the p-value rose from 0.025 to 0.157.
- **The asymptotic test with few discordant pairs.** With $m < 10$ its size can be far above $\alpha$, as at $m = 4$. R's `mcnemar.test` applies the continuity correction by default.
- **Reading "no significant change" as "no change".** A large concordant group with few discordant pairs gives little power, however large $N$ is.

## Implementations

## History

Quinn McNemar (1947) derived the standard error of the difference between two correlated proportions and the statistic $(b - c)^2/(b + c)$, with its chi-square reference. Allen L. Edwards (1948) proposed the continuity correction. The exact conditional form is the binomial sign test applied to the discordant pairs, which goes back to Arbuthnot's sign test of 1710. Bowker (1948) extended the idea to symmetry in square tables and Cochran (1950) to several matched conditions.

## References
