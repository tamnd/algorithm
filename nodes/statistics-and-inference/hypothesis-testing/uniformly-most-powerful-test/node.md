---
tag: 1APRNZ
kind: definition
slug: uniformly-most-powerful-test
name: Uniformly most powerful test
aliases:
- UMP test
area: statistics-and-inference/hypothesis-testing
level: core
summary: A level-alpha test whose power is at least that of every other level-alpha test at every parameter value in the alternative. It exists for one-sided problems with a monotone likelihood ratio.
prereqs: [statistical-hypothesis-test, statistical-power, type-i-and-type-ii-errors, neyman-pearson-lemma]
see_also: [karlin-rubin-theorem, z-test, binomial-test, student-t-test, likelihood-ratio-test, score-test, exponential-family-distribution, test-interval-duality]
sources:
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 8.3.2 (most powerful tests, the definition of a UMP test, Theorem 8.3.12 and Theorem 8.3.17, and the two-sided normal example)
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Chapter 3 (uniformly most powerful tests, Theorem 3.4.1 for families with a monotone likelihood ratio) and Chapter 4 (uniformly most powerful unbiased tests)
  - paper: doi:10.1098/rsta.1933.0009
    title: Jerzy Neyman and Egon S. Pearson, On the problem of the most efficient tests of statistical hypotheses, Philosophical Transactions of the Royal Society of London, Series A 231 (1933), pages 289 to 337
    locator: the common best critical region for a class of alternatives
---

A uniformly most powerful (UMP) test is a [hypothesis test](/statistical-hypothesis-test/) of level $\alpha$ that has the largest [power](/statistical-power/) among all level-$\alpha$ tests, at every parameter value of the alternative at the same time. The word "uniformly" is the strong part: one test must win against every alternative, not only against one chosen in advance. Such a test exists for one-sided problems in families with a monotone likelihood ratio, by the [Karlin-Rubin theorem](/karlin-rubin-theorem/), and it usually does not exist for two-sided problems. When it does not exist, the theory restricts the class of tests, for example to unbiased tests.

## Definition

Let $X$ have a distribution $P_\theta$ from a family $\{P_\theta : \theta \in \Theta\}$, and let $\Theta_0$ and $\Theta_1$ be disjoint subsets of $\Theta$. Consider the null hypothesis $H_0: \theta \in \Theta_0$ against the alternative $H_1: \theta \in \Theta_1$. A test is a function $\phi$ from the sample space to $[0, 1]$, and $\phi(x)$ is the probability that the test rejects $H_0$ on the data $x$. Its power function is
$$\beta_\phi(\theta) = E_\theta\,\phi(X), \qquad \theta \in \Theta.$$
The test has level $\alpha$ when $\sup_{\theta \in \Theta_0} \beta_\phi(\theta) \le \alpha$. Its size is this supremum.

**Definition.** A test $\phi$ of level $\alpha$ is uniformly most powerful at level $\alpha$ if, for every test $\psi$ of level $\alpha$,
$$\beta_\phi(\theta) \ge \beta_\psi(\theta) \quad \text{for every } \theta \in \Theta_1.$$

So $\phi$ is a most powerful test of $H_0$ against each simple alternative $\theta_1 \in \Theta_1$, and the same test works for all of them. When $\Theta_1$ has only one point, a UMP test is a most powerful test, and the [Neyman-Pearson lemma](/neyman-pearson-lemma/) says that it exists and gives its form. The definition allows randomized tests. With discrete data, a UMP test at a given $\alpha$ is usually randomized, and the best non-randomized test is UMP only at its own size.

Two remarks follow from the definition.

- **Equivalent tests.** If $\phi$ and $\phi'$ are both UMP at level $\alpha$, they have the same power at every $\theta \in \Theta_1$. By the necessity part of the Neyman-Pearson lemma, applied at each simple alternative, they agree almost everywhere off the set where the likelihood ratio equals the threshold.
- **Dependence on $\alpha$.** UMP is a property of a test at one level. A family of tests indexed by $\alpha$ is UMP when each member is. The one-sided tests below are UMP at every $\alpha$, and their p-values are then defined from one statistic.

## Examples and non-examples

**One-sided normal mean (UMP).** Let $X_1, \dots, X_n$ be iid $N(\mu, \sigma^2)$ with $\sigma$ known, and test $H_0: \mu \le \mu_0$ against $H_1: \mu > \mu_0$. The test that rejects when $\bar X \ge \mu_0 + z_{1-\alpha}\sigma/\sqrt n$, with $z_p$ the lower $p$-quantile of $N(0, 1)$, is UMP at level $\alpha$. This is the one-sided [z-test](/z-test/). Its rejection region is the most powerful one against each single $\mu_1 > \mu_0$, and it does not depend on $\mu_1$. Its power increases in $\mu$, so the size over the composite null is attained at $\mu_0$.

**One-sided binomial (UMP, randomized).** Let $K$ be binomial with $n = 10$ trials, and test $H_0: p \le 1/2$ against $H_1: p > 1/2$ at $\alpha = 0.05$. Under $p = 1/2$, $P(K \ge 9) = 11/1024 \approx 0.0107$ and $P(K \ge 8) = 56/1024 \approx 0.0547$, so no non-randomized test of the form "reject for large $K$" has size exactly $0.05$. The UMP test rejects when $K \ge 9$, and when $K = 8$ it rejects with probability
$$\gamma = \frac{0.05 - 11/1024}{45/1024} = \frac{67}{75} \approx 0.8933.$$
Its power, compared with the non-randomized test "reject when $K \ge 9$":

| true $p$ | UMP test | $K \ge 9$ |
|---|---|---|
| 0.6 | 0.1544 | 0.0464 |
| 0.7 | 0.3579 | 0.1493 |
| 0.8 | 0.6456 | 0.3758 |
| 0.9 | 0.9091 | 0.7361 |

In practice the [binomial test](/binomial-test/) reports a p-value and does not randomize. It is then conservative, with size $0.0107$ here.

**Two-sided normal mean (no UMP test).** Take $n = 1$, $\sigma = 1$, $H_0: \mu = 0$ against $H_1: \mu \ne 0$, and $\alpha = 0.05$. Against $\mu = 1$, the most powerful test rejects when $X \ge 1.6449$, with power $0.2595$. Against $\mu = -1$, it rejects when $X \le -1.6449$, also with power $0.2595$. A UMP test would have power $0.2595$ at both points. At $\mu = 1$ it would be most powerful, so by the necessity part of the Neyman-Pearson lemma it would be the test "reject when $X \ge 1.6449$" up to a null set. That test has power only $0.0041$ at $\mu = -1$. So no UMP test exists. The usual two-sided test, which rejects when $|X| \ge 1.96$, has power $0.1701$ at both points. It is UMP among unbiased tests.

| true $\mu$ | reject when $X \ge 1.645$ | reject when $X \le -1.645$ | reject when $\lvert X \rvert \ge 1.96$ |
|---|---|---|---|
| $-1$ | 0.0041 | 0.2595 | 0.1701 |
| $-0.5$ | 0.0160 | 0.1261 | 0.0791 |
| 0.5 | 0.1261 | 0.0160 | 0.0791 |
| 1 | 0.2595 | 0.0041 | 0.1701 |

**Uniform scale (a two-sided UMP test).** Let $X_1, \dots, X_n$ be iid uniform on $(0, \theta)$, let $M = \max_i X_i$, and test $H_0: \theta = \theta_0$ against $H_1: \theta \ne \theta_0$. The test that rejects when $M > \theta_0$ or $M \le \theta_0\,\alpha^{1/n}$ has size $\alpha$ and is UMP. For $\theta > \theta_0$, on the event $\{M \le \theta_0\}$ the density of the sample under $\theta$ is $(\theta_0/\theta)^n$ times the density under $\theta_0$. So every level-$\alpha$ test $\psi$ has
$$E_\theta \psi \le (\theta_0/\theta)^n\,E_{\theta_0}\psi + P_\theta(M > \theta_0) \le 1 - (1 - \alpha)(\theta_0/\theta)^n,$$
which is the power of the test above. For $\theta < \theta_0$ the same density relation on $\{M \le \theta\}$ gives $E_\theta \psi \le \min(1, \alpha(\theta_0/\theta)^n)$, again the power of the test above. With $n = 5$, $\theta_0 = 1$ and $\alpha = 0.05$, the lower cut is $0.05^{1/5} = 0.5493$, and the power is $0.1526$ at $\theta = 0.8$, $0.6182$ at $\theta = 1.2$ and $0.8749$ at $\theta = 1.5$. A UMP two-sided test exists here because the support moves with $\theta$, which is not the case for the normal mean.

**Cauchy location (no UMP test, one-sided).** Let $X$ have the Cauchy density $1/(\pi(1 + (x - \theta)^2))$, and test $\theta = 0$ against $\theta > 0$. The likelihood ratio $(1 + x^2)/(1 + (x - \theta_1)^2)$ is not monotone in $x$: it tends to 1 as $x \to \pm\infty$. The most powerful region against $\theta_1$ is a set of $x$ near $\theta_1$, and it changes with $\theta_1$. So even a one-sided UMP test does not exist. The family has no monotone likelihood ratio, and the [Karlin-Rubin theorem](/karlin-rubin-theorem/) does not apply.

**Normal mean with unknown variance (UMP only in a smaller class).** For $H_0: \mu \le \mu_0$ with $\sigma$ unknown, the one-sided [Student t-test](/student-t-test/) is UMP among unbiased tests, and also among tests that do not change when the data are rescaled (Lehmann and Romano, Chapters 5 and 6). The nuisance parameter $\sigma$ is the obstacle to a UMP test among all tests.

## Related definitions

- **Most powerful test.** The case of a simple alternative. The [Neyman-Pearson lemma](/neyman-pearson-lemma/) says that it rejects for large values of the likelihood ratio.
- **Monotone likelihood ratio.** A family has a monotone likelihood ratio in a statistic $T$ when $f(x; \theta_2)/f(x; \theta_1)$ is a nondecreasing function of $T(x)$ for $\theta_1 < \theta_2$. The [Karlin-Rubin theorem](/karlin-rubin-theorem/) shows that the test "reject when $T$ is large" is then UMP for one-sided hypotheses. One-parameter [exponential families](/exponential-family-distribution/) have this property in their natural statistic.
- **Unbiased test.** A level-$\alpha$ test is unbiased when $\beta_\phi(\theta) \ge \alpha$ for every $\theta \in \Theta_1$. A UMP unbiased (UMPU) test is UMP within this class. For two-sided problems in exponential families, UMPU tests exist and are given by the generalized Neyman-Pearson lemma (Lehmann and Romano, Chapter 4). The two-sided z-test and t-test are UMPU.
- **Invariant tests.** When a problem does not change under a group of transformations, a UMP invariant test is UMP among the tests that do not change either. The t-test and the F-test of the [regression F-test](/regression-f-test/) page are of this kind.
- **Locally most powerful test.** A test that maximizes the slope of the power function at the boundary $\theta_0$ among level-$\alpha$ tests. For a smooth one-parameter family it rejects for large values of the score $U_n(\theta_0)$, which is the one-sided [score test](/score-test/).
- **Asymptotic optimality.** When no UMP test exists, large-sample theory compares tests by their local power. The [likelihood ratio test](/likelihood-ratio-test/), the [Wald test](/wald-test/) and the score test have the same local power to first order.
- **Duality with intervals.** By [test-interval duality](/test-interval-duality/), inverting a family of UMP one-sided tests gives uniformly most accurate confidence bounds.

## References
