---
tag: P6MXFM
kind: algorithm
slug: binomial-test
name: Binomial test
aliases:
- exact binomial test
area: statistics-and-inference/hypothesis-testing
level: intro
summary: Tests H_0 p = p_0 from x successes in n independent trials with the exact Binomial(n, p_0) law. Valid for every n; size at most alpha; O(n) time.
model: real-ram
complexity:
  vars: {n: the number of trials}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1710
  people: [John Arbuthnot, H. O. Lancaster]
  note: Arbuthnot compared male and female christenings in London for 82 years and computed (1/2)^82, a one-sided binomial test with p_0 = 1/2. Lancaster proposed the mid-p value in 1961.
prereqs: [binomial-distribution, statistical-hypothesis-test, p-value]
see_also: [clopper-pearson-interval, wilson-score-interval, test-interval-duality, mcnemar-test, sign-test, score-test, binomial-tail-bounds, karlin-rubin-theorem]
sources:
  - book: isbn:9780470463635
    title: Alan Agresti, Categorical Data Analysis, third edition, Wiley, 2013
    locator: Section 1.4 (statistical inference for binomial parameters, the exact test and the mid p-value) and Chapter 16 (small-sample exact inference)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 8.3 (methods of evaluating tests, the size of a test and p-values)
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Chapter 3 (uniformly most powerful tests, p-values and families with monotone likelihood ratio)
  - paper: doi:10.1098/rstl.1710.0011
    title: John Arbuthnot, An argument for Divine Providence, taken from the constant regularity observed in the births of both sexes, Philosophical Transactions of the Royal Society 27, 1710
    locator: pp. 186 to 190 (82 years of christenings in London, each with more males than females)
  - paper: doi:10.1080/01621459.1961.10482105
    title: H. O. Lancaster, Significance tests in discrete distributions, Journal of the American Statistical Association 56(294), 1961
    locator: The whole paper (the mid-p value)
---

The binomial test checks a hypothesis about the success probability $p$ of independent trials. It uses the count $X$ of successes in $n$ trials and the exact null law $\text{Binomial}(n, p_0)$ of $X$, so it needs no normal approximation and is valid for every $n$. The one-sided p-value is a binomial tail. The two-sided p-value has two common definitions, which can give different answers; this page and its code use the sum of the probabilities of all outcomes that are at most as likely as the observed one, and offer doubling of the smaller tail as an option.

## In plain words

You flip a coin 10 times and see 8 heads. Is the coin fair? If it is fair, you can list the chance of each possible number of heads, from 0 to 10. Then you add up the chances of the results that are as surprising as 8 heads, or more surprising. That sum is the p-value. Here it is about 0.11, so 8 heads in 10 flips is not strong evidence against a fair coin.

Nothing is approximated. The chances come straight from counting. Because the count can only take whole values, the test cannot hit a chosen error rate such as 5% exactly. It always stays at or below it.

## The problem

**Model.** $X_1, \ldots, X_n$ are independent Bernoulli$(p)$ trials, and $X = \sum_i X_i$ is the number of successes, so $X \sim \text{Binomial}(n, p)$ with the [binomial distribution](/binomial-distribution/). The number of trials $n$ is fixed before the data are seen.

**Hypotheses.** $H_0 : p = p_0$ against one of $H_1 : p > p_0$ (one-sided, "greater"), $H_1 : p < p_0$ (one-sided, "less") or $H_1 : p \ne p_0$ (two-sided).

**Statistic.** The observed count $x$. Write $b(k) = \binom{n}{k} p_0^k (1 - p_0)^{n-k}$ for the null probability of $k$ successes.

**Null distribution.** Exact: $X \sim \text{Binomial}(n, p_0)$ under $H_0$, for every $n$.

**P-values.**

- Greater: $P_{hi}(x) = \sum_{k \ge x} b(k) = P_{p_0}(X \ge x)$.
- Less: $P_{lo}(x) = \sum_{k \le x} b(k) = P_{p_0}(X \le x)$.
- Two-sided, the minimum-likelihood rule: $p_{ml}(x) = \sum_{k : b(k) \le b(x)} b(k)$. The outcomes "at least as extreme" are those that are at most as likely under $H_0$.
- Two-sided, the doubling rule: $p_d(x) = \min\{1, 2 \min(P_{lo}(x), P_{hi}(x))\}$.

The two rules agree when $p_0 = 1/2$, where the law is symmetric. For other $p_0$ they differ, and neither one is always the smaller (see the example).

**Rejection rule.** Reject $H_0$ at level $\alpha$ when $p(x) \le \alpha$. The size is at most $\alpha$ for every $n$ and $p_0$ (proved in Correctness). It equals $\alpha$ only when $\alpha$ happens to be one of the finitely many attainable tail sums, so the test is conservative.

## The algorithm

```pseudo id=main
BINOMIAL-TEST(x, n, p0, alternative)
L1  w[k] ← C(n, k) p0^k (1 - p0)^(n - k) for k = 0 .. n    ▷ in log space with lgamma
L2  P_hi ← w[x] + w[x + 1] + ... + w[n]
L3  P_lo ← w[0] + w[1] + ... + w[x]
L4  if alternative = greater then return P_hi
L5  if alternative = less then return P_lo
L6  t ← w[x] · (1 + δ)                         ▷ δ = 10^-7 absorbs rounding in ties
L7  P ← sum of w[k] over all k with w[k] ≤ t
L8  return min(1, P)
```

Line L1 computes $\log b(k) = \operatorname{lgamma}(n + 1) - \operatorname{lgamma}(k + 1) - \operatorname{lgamma}(n - k + 1) + k \log p_0 + (n - k) \log(1 - p_0)$ and then takes $\exp$. This avoids the overflow of $\binom{n}{k}$ and the underflow of $p_0^k$ for large $n$; see [binomial coefficient computation](/binomial-coefficient-computation/) for the exact integer route. The cases $p_0 = 0$ and $p_0 = 1$ are point masses and are handled apart. Lines L2 and L3 sum each tail directly. The code uses `math.fsum` for the sums. The doubling rule replaces lines L6 to L8 by $\min(1, 2 \min(P_{lo}, P_{hi}))$.

## Example

**A fair coin.** $n = 10$, $x = 8$, $p_0 = 1/2$. The null probabilities are $\binom{10}{k}/1024$: 1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1, each over 1024. The one-sided p-value is $P_{hi}(8) = (45 + 10 + 1)/1024 = 7/128 = 0.0547$. Line L6 sets $t = 45/1024$, and the outcomes with $b(k) \le t$ are $k = 0, 1, 2, 8, 9, 10$. So $p_{ml}(8) = 112/1024 = 7/64 = 0.1094$, which is also $2 P_{hi}(8)$.

**An asymmetric null.** $n = 10$, $p_0 = 0.2$. The null probabilities are:

| $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $b(k)$ | 0.10737 | 0.26844 | 0.30199 | 0.20133 | 0.08808 | 0.02642 | 0.00551 | 0.00079 | 0.00007 | 0.000004 | 0.0000001 |

- $x = 5$: $P_{hi}(5) = 0.0327934976$. No outcome below the mode has a probability as small as $b(5) = 0.0264$, so $p_{ml}(5) = 0.0328$, while $p_d(5) = 0.0656$. At $\alpha = 0.05$ the minimum-likelihood rule rejects and the doubling rule does not.
- $x = 0$: $P_{lo}(0) = 0.8^{10} = 0.1073741824$ and $p_d(0) = 0.2147483648$. The outcomes with $b(k) \le b(0)$ are $k = 0$ and $k = 4, \ldots, 10$, so $p_{ml}(0) = 0.228248064$. Here the minimum-likelihood rule gives the larger value.

**Attained size.** For $n = 10$, $p_0 = 1/2$, the one-sided test at $\alpha = 0.05$ rejects for $x \in \{9, 10\}$, because $P_{hi}(8) = 0.0547 > 0.05$. Its size is $11/1024 = 0.0107$, far below $0.05$. The two-sided test rejects for $x \in \{0, 1, 9, 10\}$, with size $22/1024 = 0.0215$.

**A small tail.** For $n = 1000$, $x = 700$, $p_0 = 1/2$, the exact upper tail is $8.83 \times 10^{-38}$. Line L2 returns this to 9 digits. Computing it as $1 - P_{lo}(699)$ in double precision returned $2.2 \times 10^{-13}$, which is wrong by 24 orders of magnitude.

All the numbers above come from exact `Fraction` sums, and the tests check the code against them.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Lines L1 to L8 return the tail sums of the definitions. Validity rests on one lemma: if $p(x) = P(T(X) \ge T(x))$ for some ordering $T$ of the finite sample space, then $P(p(X) \le u) \le u$ for every $u$. The set $\{x : p(x) \le u\}$ is contained in the tail $\{T \ge T(x^*)\}$ of its own smallest member $x^*$, and that tail has probability $p(x^*) \le u$. The one-sided p-values use $T(x) = \pm x$, and the minimum-likelihood p-value uses $T(x) = -b(x)$. For the doubling rule, $p_d(x) \le \alpha$ forces one tail to be at most $\alpha/2$, and the two events have probability at most $\alpha/2$ each. The tolerance $\delta$ in line L6 can only enlarge the p-value, so it keeps the bound.

## Complexity

Line L1 does $n + 1$ evaluations, each with three $\operatorname{lgamma}$ values, two logarithms reused across $k$ and one $\exp$. Lines L2, L3 and L7 are linear scans. So the time is $\Theta(n)$ and the extra space is $\Theta(n)$ for the list $w$. A one-sided p-value alone can be found without the list: $P_{hi}(x) = I_{p_0}(x, n - x + 1)$, the regularized incomplete beta function, which a continued fraction evaluates without a sum of $n$ terms. The [Clopper-Pearson interval](/clopper-pearson-interval/) uses this identity. For the two-sided rule the terms $b(k)$ fall on each side of the mode, so a binary search can find the cut on the other side of the mode, but the sum itself still costs $\Theta(n)$ terms in the simple form. For a quick upper bound with no sum, the [Chernoff bound](/chernoff-bound/) gives $P_{hi}(x) \le \exp(-n D(x/n \,\Vert\, p_0))$ for $x \ge n p_0$, where $D$ is the binary relative entropy; see [binomial tail bounds](/binomial-tail-bounds/). A bound is not a p-value, but it is a valid conservative one.

## Properties

- **Exact.** The null law is exact for every $n$. No large-sample condition such as $n p_0 \ge 5$ is needed.
- **Conservative.** The size is at most $\alpha$, and equals $\alpha$ only at the attainable values. For $n = 10$, $p_0 = 1/2$ and $\alpha = 0.05$, the one-sided size is $0.0107$.
- **Power.** The family $\text{Binomial}(n, p)$ has a monotone likelihood ratio in $x$, so the test that rejects for $x \ge c$ is uniformly most powerful among the tests of its own size against $p > p_0$, by the [Karlin-Rubin theorem](/karlin-rubin-theorem/). With $n = 20$, $p_0 = 1/2$ and $\alpha = 0.05$, it rejects for $x \ge 15$ (size $0.0207$), and its power at $p = 0.75$ is $0.617$. The randomized test that also rejects at $x = 14$ with probability $0.793$ has size exactly $0.05$ and power $0.751$. No uniformly most powerful test exists against the two-sided alternative.
- **The two-sided rule matters.** For asymmetric nulls the two rules can disagree at $\alpha = 0.05$, as the example shows. Say which one you use.
- **Discrete p-value.** The p-value takes at most $n + 1$ values, so its null law is not uniform. It is stochastically larger than uniform, which is the meaning of the validity bound.

## Variants and improvements

- **Mid-p value.** $P_{p_0}(X > x) + \tfrac{1}{2} P_{p_0}(X = x)$ (Lancaster 1961). It is less conservative and its null mean is $1/2$, but its size can exceed $\alpha$ slightly. For $n = 10$, $p_0 = 0.2$ and $x = 4$, the mid-p value is $0.0768$, against $P_{hi}(4) = 0.1209$.
- **Randomized test.** Reject on the boundary outcome with a probability chosen to make the size exactly $\alpha$, as in the power example. It is optimal in theory but rarely used, since two analysts with the same data can reach different decisions.
- **Normal approximation.** The score statistic $z = (x - n p_0)/\sqrt{n p_0 (1 - p_0)}$ is approximately standard normal for large $n$; it is the [score test](/score-test/) and a form of the [z-test](/z-test/). Its size can be far from $\alpha$ when $n p_0$ is small. A continuity correction subtracts $1/2$ from $\lvert x - n p_0 \rvert$.
- **Inverting the test.** The set of $p_0$ that the test does not reject is a confidence set, by [test-interval duality](/test-interval-duality/). The doubling rule gives the [Clopper-Pearson interval](/clopper-pearson-interval/). The minimum-likelihood rule gives the Sterne interval, which need not be an interval: for $n = 30$ and $x = 1$, the set of $p_0$ not rejected at $\alpha = 0.05$ is about $(0.0017, 0.1632)$ together with the short piece $(0.1751, 0.1772)$, by a scan of $p_0$ on a grid of step $10^{-6}$. Blaker (2000) gives a rule whose inversion behaves better.
- **Special cases.** The [sign test](/sign-test/) is a binomial test with $p_0 = 1/2$ on the signs of paired differences, and the exact [McNemar test](/mcnemar-test/) is a binomial test on the discordant pairs.

## When to use it

Use it for a single proportion when the trials are independent with a common $p$ and $n$ was fixed in advance, and above all when $n$ is small or $p_0$ is near 0 or 1, where the normal approximation fails. With large $n$ and $p_0$ away from the ends, the score test gives nearly the same answer. To report an effect, pair the test with a confidence interval: Clopper-Pearson for a guarantee at every $p$, or [Wilson](/wilson-score-interval/) for intervals that are shorter on average.

## Pitfalls

- **Which two-sided rule.** R's `binom.test` uses the minimum-likelihood rule with a relative tolerance of $10^{-7}$. Other software doubles the smaller tail. Results differ for $p_0 \ne 1/2$.
- **Subtracting from 1.** $1 - P_{lo}(x - 1)$ loses all digits when the upper tail is small. Sum the tail directly, as line L2 does.
- **The stopping rule.** The p-value depends on how the data were collected. For 9 heads and 3 tails with $p_0 = 1/2$ and the one-sided alternative, a fixed $n = 12$ gives $P(X \ge 9) = 299/4096 = 0.0730$. If the coin was instead tossed until the third tail, the count of heads is negative binomial and $P(\text{at least 9 heads}) = 67/2048 = 0.0327$. The likelihood is the same in both cases, but the p-values are not.
- **Dependence and heterogeneity.** Clustered trials or a $p$ that varies between trials make the variance of $X$ larger than $n p (1 - p)$, and the test then rejects too often.
- **Size is not $\alpha$.** Report the attained size or the p-value, not only "significant at 5%". Power and sample size calculations must use the attained size, which jumps as $n$ changes.

## Implementations

## History

John Arbuthnot (1710) noted that in each of the 82 years from 1629 to 1710 more boys than girls were christened in London, and that under even chances this has probability $(1/2)^{82}$. This is the first recorded significance test, and it is a one-sided binomial test, or a sign test. The Neyman-Pearson theory of the 1930s put the test in its modern form, with a fixed level and the optimality of the one-sided test. Lancaster (1961) proposed the mid-p value to reduce the conservatism of discrete tests. The question of the two-sided p-value for asymmetric discrete nulls has no single answer; textbooks such as Agresti's give both rules.

## References
