---
tag: 8G9YHV
kind: theorem
slug: neyman-pearson-lemma
name: Neyman-Pearson lemma
aliases:
- Neyman-Pearson fundamental lemma
area: statistics-and-inference/hypothesis-testing
level: core
summary: For a simple null against a simple alternative, the test that rejects when the likelihood ratio exceeds a threshold is the most powerful test of its size.
prereqs: [statistical-hypothesis-test, type-i-and-type-ii-errors, statistical-power, likelihood-function]
see_also: [uniformly-most-powerful-test, karlin-rubin-theorem, likelihood-ratio-test, z-test, linear-programming-problem, sequential-probability-ratio-test, bayes-factor, e-variable]
sources:
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 8.3.2, Theorem 8.3.12 (the Neyman-Pearson lemma) and the corollary after it (the form in terms of a sufficient statistic)
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Section 3.2, Theorem 3.2.1 (existence, sufficiency and necessity, with randomized tests) and Corollary 3.2.1 (the power exceeds the size); Section 3.6, Theorem 3.6.1 (the generalized lemma)
  - paper: doi:10.1098/rsta.1933.0009
    title: Jerzy Neyman and Egon S. Pearson, On the problem of the most efficient tests of statistical hypotheses, Philosophical Transactions of the Royal Society of London, Series A 231 (1933), pages 289 to 337
    locator: the most efficient critical region for a simple hypothesis against a simple alternative
---

The Neyman-Pearson lemma solves the simplest testing problem completely. The data come from one of two fully specified distributions, $f_0$ under the null and $f_1$ under the alternative, and the lemma says that the most powerful test at level $\alpha$ rejects when the likelihood ratio $f_1(x)/f_0(x)$ is above a threshold, with randomization at the threshold when the data are discrete. It also says that such a test exists for every $\alpha$, and that every most powerful test has this form, except on the set where the ratio equals the threshold. It is the base of the theory of optimal tests: [uniformly most powerful tests](/uniformly-most-powerful-test/), the [Karlin-Rubin theorem](/karlin-rubin-theorem/) and unbiased tests all start from it.

## Statement

Let $X$ take values in a set $\mathcal X$, and let $f_0 = f(\cdot\,; \theta_0)$ and $f_1 = f(\cdot\,; \theta_1)$ be its densities under $H_0: \theta = \theta_0$ and $H_1: \theta = \theta_1$, with respect to a common measure $\nu$. For discrete data $\nu$ is the counting measure and the integrals below are sums. For continuous data $\nu$ is the Lebesgue measure. A common measure always exists, for example $\nu = P_0 + P_1$. Both hypotheses are simple: each names a single distribution.

A test is a measurable function $\phi: \mathcal X \to [0, 1]$. On the data $x$, the test rejects $H_0$ with probability $\phi(x)$. A non-randomized test takes only the values 0 and 1. The size of $\phi$ is $E_0\phi(X) = \int \phi f_0 \, d\nu$, its [power](/statistical-power/) is $E_1\phi(X) = \int \phi f_1 \, d\nu$, and $\phi$ has level $\alpha$ when its size is at most $\alpha$. A test is most powerful at level $\alpha$ when no other test of level $\alpha$ has more power.

**Theorem (Neyman and Pearson, 1933).** Let $0 \le \alpha \le 1$.

1. **Sufficiency.** Let $0 \le k < \infty$, and let $\phi$ be a test with $E_0\phi(X) = \alpha$ and
$$\phi(x) = \begin{cases} 1 & \text{if } f_1(x) > k f_0(x), \\ 0 & \text{if } f_1(x) < k f_0(x), \end{cases}$$
with any value in $[0, 1]$ on the set $\{f_1 = k f_0\}$. Then $\phi$ is most powerful at level $\alpha$. For $\alpha = 0$, the test $\phi(x) = 1$ if $f_0(x) = 0$ and $\phi(x) = 0$ otherwise (the case $k = \infty$) is also most powerful at level 0.
2. **Existence.** For every $\alpha$ there is a test of the form in part 1, with a constant value $\gamma \in [0, 1]$ on the set $\{f_1 = k f_0\}$. For $\alpha = 0$ the test with $k = \infty$ is allowed.
3. **Necessity.** Let $\phi^*$ be most powerful at level $\alpha$, and let $\phi$ and $k$ be as in part 2. Then $\phi^* = \phi$ $\nu$-almost everywhere on the set $\{f_1 \ne k f_0\}$. Also, $\phi^*$ has size exactly $\alpha$, unless some test of size less than $\alpha$ has power 1.

**Corollary.** Let $0 < \alpha < 1$, and let $\beta$ be the power of the most powerful level-$\alpha$ test. Then $\alpha \le \beta$, and $\alpha < \beta$ unless $P_0 = P_1$.

The ratio $f_1(x)/f_0(x)$ is the likelihood ratio $L(\theta_1; x)/L(\theta_0; x)$ of the [likelihood function](/likelihood-function/), so the test of part 1 is a likelihood ratio test in the original sense. The [likelihood ratio test](/likelihood-ratio-test/) for composite hypotheses is a different procedure that only borrows the idea.

## In plain words

Two stories could explain your data, and each story says exactly how likely every possible outcome is. You must pick the outcomes where you will reject the first story. You can afford only a fixed total chance of rejecting it when it is true, and you want the largest possible chance of rejecting it when the second story is true. Think of a budget. Each outcome costs its chance under the first story and pays its chance under the second. The best plan is to buy outcomes in the order of their pay per cost, which is the likelihood ratio, until the budget runs out. If the budget runs out in the middle of an outcome, you buy part of it by flipping a biased coin. No other plan pays more.

## Proof

All integrals are with respect to $\nu$, and the argument $x$ is often dropped.

**Part 1, sufficiency.** Let $\psi$ be any test of level $\alpha$, so $\int \psi f_0 \le \alpha$. We show that
$$(\phi(x) - \psi(x))\,(f_1(x) - k f_0(x)) \ge 0 \quad \text{for every } x.$$
If $f_1(x) > k f_0(x)$, then $\phi(x) = 1 \ge \psi(x)$, so both factors are nonnegative. If $f_1(x) < k f_0(x)$, then $\phi(x) = 0 \le \psi(x)$, so both factors are nonpositive. If $f_1(x) = k f_0(x)$, the second factor is 0. Integrate the inequality:
$$\int \phi f_1 - \int \psi f_1 \ \ge\ k\left(\int \phi f_0 - \int \psi f_0\right) = k\left(\alpha - \int \psi f_0\right) \ \ge\ 0,$$
because $k \ge 0$ and $\int \psi f_0 \le \alpha$. So $E_1\phi \ge E_1\psi$.

For the case $k = \infty$ and $\alpha = 0$, let $\psi$ be any test with $\int \psi f_0 = 0$. Then $\psi = 0$ almost everywhere on $\{f_0 > 0\}$, so $\int \psi f_1 = \int_{\{f_0 = 0\}} \psi f_1 \le \int_{\{f_0 = 0\}} f_1 = \int \phi f_1$.

**Part 2, existence.** For $\alpha = 0$, the test with $k = \infty$ has size $\int_{\{f_0 = 0\}} f_0 = 0$. Let now $0 < \alpha \le 1$. Under $P_0$, the set $\{f_0 = 0\}$ has probability 0, so the ratio $R(X) = f_1(X)/f_0(X)$ is defined with probability 1. For $c \ge 0$ put
$$a(c) = P_0(f_1(X) > c f_0(X)) = P_0(R(X) > c).$$
The function $a$ is nonincreasing and continuous from the right, because it is one minus a distribution function. By Markov's inequality, $a(c) \le E_0 R(X)/c \le 1/c$, since $E_0 R(X) = \int_{\{f_0 > 0\}} f_1 \le 1$. So $a(c) \to 0$ as $c \to \infty$, and the number
$$k = \inf\{c \ge 0 : a(c) \le \alpha\}$$
is finite. By right continuity, $a(k) \le \alpha$. Next, $P_0(R(X) \ge k) \ge \alpha$: if $k = 0$ the left side is 1, and if $k > 0$ then $a(c) > \alpha$ for each $c < k$, and $P_0(R \ge k) = \lim_{c \uparrow k} a(c) \ge \alpha$. So $P_0(R(X) = k) = P_0(R \ge k) - a(k) \ge \alpha - a(k) \ge 0$. Put
$$\gamma = \frac{\alpha - a(k)}{P_0(R(X) = k)} \text{ if } P_0(R(X) = k) > 0, \qquad \gamma = 0 \text{ otherwise}.$$
Then $0 \le \gamma \le 1$. Let $\phi = 1$ on $\{f_1 > k f_0\}$, $\phi = \gamma$ on $\{f_1 = k f_0\}$ and $\phi = 0$ on $\{f_1 < k f_0\}$. The set $\{f_0 = 0\}$ has $P_0$-probability 0, so
$$E_0\phi(X) = a(k) + \gamma\,P_0(R(X) = k) = \alpha.$$
In the second case of $\gamma$ this holds because $P_0(R = k) = 0$ forces $a(k) = P_0(R \ge k) \ge \alpha$, so $a(k) = \alpha$.

**Part 3, necessity.** Let $\phi^*$ be most powerful at level $\alpha$ and let $\phi$, $k$ be the test of part 2. First take $k < \infty$. Let $S = \{x : \phi^*(x) \ne \phi(x)\} \cap \{x : f_1(x) \ne k f_0(x)\}$. By the case analysis of part 1, applied with $\psi = \phi^*$, the product $(\phi - \phi^*)(f_1 - k f_0)$ is nonnegative everywhere, and it is strictly positive on $S$. If $\nu(S) > 0$, then
$$\int \phi f_1 - \int \phi^* f_1 > k\left(\alpha - \int \phi^* f_0\right) \ge 0,$$
so $\phi$ has more power than $\phi^*$, which contradicts the choice of $\phi^*$. So $\nu(S) = 0$.

For the size, suppose $E_0\phi^* < \alpha$. Both tests are most powerful, so $E_1\phi = E_1\phi^*$, and the integral of the nonnegative product is
$$0 \le \int (\phi - \phi^*)(f_1 - k f_0) = -k\left(\alpha - E_0\phi^*\right).$$
This forces $k = 0$. With $k = 0$, $\phi = 1$ on $\{f_1 > 0\}$, so $E_1\phi^* = E_1\phi = 1$, and $\phi^*$ is a test of size less than $\alpha$ with power 1.

For $k = \infty$, $\alpha = 0$ and $\phi^*$ has level 0, so $\phi^* = 0$ almost everywhere on $\{f_0 > 0\}$, where $f_1 < \infty \cdot f_0$. On $\{f_0 = 0, f_1 > 0\}$, if $\phi^* < 1$ on a set of positive $\nu$-measure, then $\int \phi^* f_1 < \int \phi f_1$, against the choice of $\phi^*$. So $\phi^* = \phi$ almost everywhere on $\{f_1 \ne k f_0\}$ in this case too. $\square$

**Proof of the corollary.** The constant test $\psi \equiv \alpha$ has size $\alpha$ and power $\alpha$, so $\beta \ge \alpha$. Suppose $\beta = \alpha$. Then $\psi \equiv \alpha$ is most powerful, and by part 3 it equals 0 or 1 almost everywhere on $\{f_1 \ne k f_0\}$. It takes neither value, so $\nu(f_1 \ne k f_0) = 0$, that is $f_1 = k f_0$ almost everywhere. Both are densities, so integration gives $k = 1$, and then $P_0 = P_1$. $\square$

## Consequences

- **The test depends on the data only through the likelihood ratio.** If $T$ is a [sufficient statistic](/sufficient-statistic/), the factorization $f(x; \theta) = g(t(x); \theta)\,h(x)$ makes the ratio a function of $t(x)$, so the most powerful test is a function of $T$.
- **The normal mean.** Let $X_1, \dots, X_n$ be iid $N(\mu, \sigma^2)$ with $\sigma$ known, and test $\mu = \mu_0$ against $\mu = \mu_1$ with $\mu_1 > \mu_0$. The log of the ratio is $\frac{n(\mu_1 - \mu_0)}{\sigma^2}\left(\bar x - \frac{\mu_0 + \mu_1}{2}\right)$, which increases in $\bar x$. So the most powerful test rejects when $\bar x > c$, and the size condition gives $c = \mu_0 + z_{1-\alpha}\sigma/\sqrt n$, with $z_p$ the lower $p$-quantile of $N(0, 1)$. This is the one-sided [z-test](/z-test/). With $n = 4$, $\sigma = 1$, $\mu_0 = 0$, $\mu_1 = 1$ and $\alpha = 0.05$, the test rejects when $\bar x > 0.8224$, and its power is $\Phi(2 - 1.6449) = 0.6388$.
- **From one alternative to many.** In the normal example the rejection region does not depend on $\mu_1$, only on its sign. So the same test is most powerful against every $\mu_1 > \mu_0$, and it is a [uniformly most powerful test](/uniformly-most-powerful-test/). The [Karlin-Rubin theorem](/karlin-rubin-theorem/) turns this observation into a theorem for families with a monotone likelihood ratio.
- **A linear program.** The problem "maximize $\int \phi f_1$ subject to $\int \phi f_0 \le \alpha$ and $0 \le \phi \le 1$" is a [linear program](/linear-programming-problem/) in $\phi$, a continuous knapsack problem. The lemma says that the greedy order by the ratio of value to cost is optimal, and the threshold $k$ is the [Lagrange multiplier](/lagrange-multiplier/) of the size constraint. On a finite sample space, every extreme point of the feasible set of tests with size exactly $\alpha$ is 0 or 1 at every point except at most one.
- **Bayes tests.** With prior weights $\pi_0, \pi_1 > 0$ on the two hypotheses, the test that minimizes $\pi_0 E_0\phi + \pi_1(1 - E_1\phi)$ rejects when $f_1/f_0 > \pi_0/\pi_1$. It has the form of part 1 with $k = \pi_0/\pi_1$, so every Bayes test is most powerful at its own size. The ratio $f_1/f_0$ is the [Bayes factor](/bayes-factor/) of two simple hypotheses.
- **Sequential and anytime tests.** Wald's [sequential probability ratio test](/sequential-probability-ratio-test/) applies the same ratio to data that arrive one at a time. Under $H_0$ the ratio $f_1(X)/f_0(X)$ has expectation at most 1, so it is an [e-variable](/e-variable/).
- **Generalizations.** The generalized lemma (Lehmann and Romano, Theorem 3.6.1) maximizes $\int \phi f_{m+1}$ subject to $m$ integral constraints. It gives the uniformly most powerful unbiased tests of exponential families.

## Tightness

**Randomization is needed for discrete data.** Let $X$ take the values 1, 2, 3, 4 with
$$f_0 = (0.4, 0.3, 0.2, 0.1), \qquad f_1 = (0.1, 0.2, 0.3, 0.4),$$
and let $\alpha = 0.25$. The ratios $f_1/f_0$ are $1/4, 2/3, 3/2, 4$. The most powerful test rejects at $x = 4$ (size 0.1). The budget left is $0.15$, so at $x = 3$, with $f_0(3) = 0.2$, it rejects with probability $\gamma = 0.15/0.2 = 3/4$. The threshold is $k = 3/2$. The size is exactly $0.25$, and the power is $0.4 + \tfrac34 \cdot 0.3 = 0.625$. The non-randomized tests of level $0.25$ reject on $\emptyset$, $\{3\}$ or $\{4\}$, and the best of them, $\{4\}$, has power only $0.4$. An enumeration over the extreme points of the linear program of the previous section gives the same optimum, $5/8$, in exact arithmetic. A non-randomized test of the form of part 1 is most powerful only at its own size, which here is one of the attainable values $0, 0.1, 0.3, 0.6, 1$.

**The set where the ratio equals $k$.** Part 3 says nothing about $\phi^*$ on $\{f_1 = k f_0\}$, and it cannot. In the example above, any test that rejects at $x = 4$ and spends $0.15$ of size at $x = 3$ is most powerful. If two points tie at the threshold, the size left can be split between them in any proportion.

**Simple hypotheses only.** The proof uses one density for each hypothesis. Against the two-sided alternative $\mu \ne \mu_0$ of the normal example, the most powerful test against $\mu_1 > \mu_0$ rejects for large $\bar x$, and the most powerful test against $\mu_1 < \mu_0$ rejects for small $\bar x$. No single test is most powerful against both, so no uniformly most powerful test exists. For a composite null, the lemma applies to a least favorable distribution on the null (Lehmann and Romano, Chapter 3), which is not always easy to find.

**The power can equal the size.** The corollary needs $P_0 \ne P_1$. If the two distributions are equal, every test has power equal to its size, and the data carry no information.

## History

Neyman and Pearson introduced the likelihood ratio criterion in 1928, as a principle for choosing a test. In their 1933 paper "On the problem of the most efficient tests of statistical hypotheses", they posed the problem of the best critical region of given size for a simple hypothesis against a simple alternative, and they proved that the region where the ratio of the two likelihoods exceeds a constant is the solution. They also showed that the same region can be best against a whole class of alternatives, which led to the uniformly most powerful tests. The statement used today, with randomized tests and with the three parts of existence, sufficiency and necessity, is the one of Lehmann's book Testing Statistical Hypotheses (1959). Dantzig and Wald (1951) gave the measure-theoretic form of the generalized lemma, and the connection with linear programming made it a standard example of duality.

## References
