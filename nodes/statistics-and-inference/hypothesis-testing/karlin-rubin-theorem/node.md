---
tag: TQ1ZP7
kind: theorem
slug: karlin-rubin-theorem
name: Karlin-Rubin theorem
aliases:
- monotone likelihood ratio theorem
area: statistics-and-inference/hypothesis-testing
level: advanced
summary: If a one-parameter family has a monotone likelihood ratio in a statistic T, then the test that rejects for large T is uniformly most powerful for a one-sided hypothesis.
prereqs: [neyman-pearson-lemma, uniformly-most-powerful-test, sufficient-statistic, statistical-power]
see_also: [exponential-family-distribution, z-test, binomial-test, test-interval-duality, score-test, likelihood-ratio-test, statistical-decision-theory]
sources:
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 8.3.2 (the definition of a monotone likelihood ratio and Theorem 8.3.17, the Karlin-Rubin theorem)
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Section 3.4, Theorem 3.4.1 (UMP one-sided tests for families with a monotone likelihood ratio, with the monotone power function and the minimization of the error below the null)
  - paper: doi:10.1214/aoms/1177728259
    title: Samuel Karlin and Herman Rubin, The theory of decision procedures for distributions with monotone likelihood ratio, Annals of Mathematical Statistics 27(2) (1956), pages 272 to 299
    locator: the monotone procedures for monotone decision problems and their essential completeness
---

The Karlin-Rubin theorem gives a [uniformly most powerful test](/uniformly-most-powerful-test/) for a one-sided hypothesis $\theta \le \theta_0$ against $\theta > \theta_0$ about a real parameter. The condition is a monotone likelihood ratio: for $\theta < \theta'$, the ratio of the densities at $\theta'$ and $\theta$ is a nondecreasing function of one statistic $T$. Then the test that rejects when $T$ is large, randomized at one point if $T$ is discrete, is UMP at its level, and its power increases in $\theta$. All one-parameter exponential families satisfy the condition, so the theorem covers the one-sided z-test, the binomial and Poisson tests and the test of an exponential mean.

## Statement

Let $X$ have a density $f(x; \theta)$ with respect to a measure $\nu$, for a real parameter $\theta \in \Theta \subseteq \mathbb R$. Write $P_\theta$ and $E_\theta$ for the distribution and the expectation at $\theta$.

**Definition (monotone likelihood ratio).** The family has a monotone likelihood ratio (MLR) in a real statistic $T(x)$ if, for all $\theta < \theta'$ in $\Theta$, the distributions $P_\theta$ and $P_{\theta'}$ are distinct, and there is a nondecreasing function $h_{\theta, \theta'}: \mathbb R \to [0, \infty]$ with
$$\frac{f(x; \theta')}{f(x; \theta)} = h_{\theta, \theta'}(T(x))$$
at every $x$ where $f(x; \theta) + f(x; \theta') > 0$. The ratio is $+\infty$ where $f(x; \theta) = 0 < f(x; \theta')$.

**Theorem (Karlin and Rubin, 1956).** Let the family have an MLR in $T$, let $\theta_0 \in \Theta$ and $0 < \alpha < 1$. For constants $c \in \mathbb R$ and $\gamma \in [0, 1]$, let
$$\phi(x) = \begin{cases} 1 & \text{if } T(x) > c, \\ \gamma & \text{if } T(x) = c, \\ 0 & \text{if } T(x) < c, \end{cases} \qquad \beta(\theta) = E_\theta\,\phi(X).$$

1. There are $c$ and $\gamma$ with $\beta(\theta_0) = \alpha$. With them, $\phi$ is a UMP test at level $\alpha$ of $H_0: \theta \le \theta_0$ against $H_1: \theta > \theta_0$.
2. The power function $\beta$ is nondecreasing on $\Theta$, and strictly increasing on the set of $\theta$ where $0 < \beta(\theta) < 1$.
3. For each $\theta' \in \Theta$ with $\beta(\theta') > 0$, the test $\phi$ is UMP at level $\beta(\theta')$ for $\theta \le \theta'$ against $\theta > \theta'$.
4. For each $\theta < \theta_0$, the test $\phi$ minimizes $E_\theta\psi(X)$ among all tests $\psi$ with $E_{\theta_0}\psi(X) = \alpha$.

The test for $H_0: \theta \ge \theta_0$ against $H_1: \theta < \theta_0$ is the mirror image: it rejects when $T$ is small. Casella and Berger state the theorem for a sufficient statistic $T$ with an MLR, a non-randomized test and a continuous $T$; Lehmann and Romano (Theorem 3.4.1) give the form above.

## In plain words

Suppose the data come from a family where a bigger parameter always makes bigger values of one summary number more likely, in a strong sense: as the summary grows, the evidence for the bigger parameter never gets weaker. Then to test "the parameter is at most some value" against "it is bigger", you only need that one number. Reject when it is large. Set the cutoff so that the test makes a false alarm at the boundary value with the allowed probability. This single test is the best one against every bigger parameter at the same time. Its chance to reject also grows as the true parameter grows, so the false alarm rate is never larger below the boundary than at the boundary.

## Proof

Write $f_\theta = f(\cdot\,; \theta)$, and let $P_{\theta}(T \ge c)$ mean $P_\theta(T(X) \ge c)$.

**Step 1 (the constants).** Let $G(t) = P_{\theta_0}(T > t)$. It is nonincreasing and continuous from the right, it tends to 1 as $t \to -\infty$ and to 0 as $t \to \infty$. So $c = \inf\{t : G(t) \le \alpha\}$ is a real number, $G(c) \le \alpha$, and $P_{\theta_0}(T \ge c) = \lim_{t \uparrow c} G(t) \ge \alpha$. Put $\gamma = (\alpha - G(c))/P_{\theta_0}(T = c)$ when $P_{\theta_0}(T = c) > 0$, and $\gamma = 0$ otherwise (then $G(c) = \alpha$). In both cases $0 \le \gamma \le 1$ and $\beta(\theta_0) = G(c) + \gamma P_{\theta_0}(T = c) = \alpha$.

**Step 2 (a lemma).** *Let $\theta' < \theta''$ and suppose $P_{\theta'}(T \ge c) > 0$. Then $\phi$ is a most powerful test of $\theta'$ against $\theta''$ at level $\beta(\theta')$.*

Let $h = h_{\theta', \theta''}$, so that $f_{\theta''}(x) = h(T(x)) f_{\theta'}(x)$ where $f_{\theta'}(x) > 0$, and $h(T(x)) = \infty$ where $f_{\theta'}(x) = 0 < f_{\theta''}(x)$. We find a finite $k \ge 0$ such that $\phi = 1$ where $f_{\theta''} > k f_{\theta'}$ and $\phi = 0$ where $f_{\theta''} < k f_{\theta'}$. The Neyman-Pearson lemma, part 1, then gives the claim, because $\phi$ has size $\beta(\theta')$ at $\theta'$.

Let $A = \{x : T(x) > c\}$, $E = \{x : T(x) = c\}$ and $B = \{x : T(x) < c\}$, all restricted to points where $f_{\theta'} + f_{\theta''} > 0$. Let $a = \sup_{x \in B} h(T(x))$, with $a = 0$ when $B$ is empty. First, $a < \infty$. If not, then by monotonicity $h(T(x)) = \infty$ for every $x$ with $T(x) \ge c$, so $f_{\theta'} = 0$ on $A \cup E$ and $P_{\theta'}(T \ge c) = 0$, against the hypothesis. For the same reason, if $E$ is not empty, the common value $h(c)$ of the ratio on $E$ is finite. Now choose
$$k = h(c) \text{ if } E \ne \emptyset, \qquad k = a \text{ if } E = \emptyset.$$
In both cases $k$ is finite and $a \le k$. Monotonicity of $h$ gives $h(T(x)) \ge k$ on $A$ and $h(T(x)) \le k$ on $B$, and $h = k$ on $E$ in the first case. So the set $\{f_{\theta''} > k f_{\theta'}\}$ is contained in $A$, where $\phi = 1$, and the set $\{f_{\theta''} < k f_{\theta'}\}$ is contained in $B$, where $\phi = 0$. $\square$

**Step 3 (part 2, the power function).** Let $\theta' < \theta''$. If $\beta(\theta') = 0$, then $\beta(\theta'') \ge \beta(\theta')$. Otherwise $P_{\theta'}(T \ge c) \ge \beta(\theta') > 0$, so by Step 2, $\phi$ is most powerful at level $\beta(\theta')$ for $\theta'$ against $\theta''$. The constant test $\psi \equiv \beta(\theta')$ has the same level and power $\beta(\theta')$, so $\beta(\theta'') \ge \beta(\theta')$. If also $\beta(\theta') < 1$, the corollary of the Neyman-Pearson lemma, with $P_{\theta'} \ne P_{\theta''}$, gives $\beta(\theta'') > \beta(\theta')$.

**Step 4 (parts 1 and 3, the UMP property).** Take part 3 first. Let $\beta(\theta') > 0$. By Step 3, $\sup_{\theta \le \theta'} \beta(\theta) = \beta(\theta')$, so $\phi$ has level $\beta(\theta')$ for the null $\theta \le \theta'$. Let $\psi$ be any test with $\sup_{\theta \le \theta'} E_\theta \psi \le \beta(\theta')$, and let $\theta'' > \theta'$. Then $E_{\theta'}\psi \le \beta(\theta')$, so $\psi$ is a level-$\beta(\theta')$ test of $\theta'$ against $\theta''$, and by Step 2, $E_{\theta''}\psi \le \beta(\theta'')$. This holds for every $\theta'' > \theta'$, so $\phi$ is UMP. Part 1 is the case $\theta' = \theta_0$, where $\beta(\theta_0) = \alpha > 0$ by Step 1.

**Step 5 (part 4, below the null).** Let $\theta < \theta_0$. The family indexed by $-\theta$ has an MLR in $-T$, because $f_\theta / f_{\theta_0}$ is a nonincreasing function of $T$. In that family, the test $1 - \phi$ equals 1 when $-T > -c$, $1 - \gamma$ when $-T = -c$ and 0 when $-T < -c$, so it has the form of the theorem with the statistic $-T$. Also $P_{\theta_0}(-T \ge -c) = P_{\theta_0}(T \le c) \ge 1 - \alpha > 0$. By Step 2 in the reversed family, $1 - \phi$ is most powerful for $\theta_0$ against $\theta$ at level $E_{\theta_0}(1 - \phi) = 1 - \alpha$. Let $\psi$ satisfy $E_{\theta_0}\psi = \alpha$. Then $1 - \psi$ has level $1 - \alpha$ at $\theta_0$, so $E_\theta(1 - \phi) \ge E_\theta(1 - \psi)$, that is $E_\theta\phi \le E_\theta\psi$. $\square$

## Consequences

- **Exponential families.** Let $f(x; \theta) = g(x)\exp(\eta(\theta)\,T(x) - A(\theta))$ with $\eta$ strictly increasing. For $\theta < \theta'$ the ratio is $\exp((\eta(\theta') - \eta(\theta))T(x) - A(\theta') + A(\theta))$, which increases in $T(x)$. So every one-parameter [exponential family](/exponential-family-distribution/) with a monotone natural parameter has an MLR in its natural statistic, and for iid samples in the sum $\sum_i T(X_i)$. This covers the normal mean with known variance ($\sum X_i$), the normal variance with known mean ($\sum (X_i - \mu)^2$), the binomial ($K$), the Poisson ($\sum X_i$) and the exponential distribution with mean $\theta$ ($\sum X_i$, with $\eta(\theta) = -1/\theta$).
- **Families outside the exponential class.** The uniform family on $(0, \theta)$ has an MLR in the maximum $M = \max_i X_i$: for $\theta < \theta'$ the ratio is $(\theta/\theta')^n$ when $M \le \theta$ and $+\infty$ when $\theta < M \le \theta'$. The hypergeometric family has an MLR in the number of marked items in the sample, and the noncentral t family has an MLR in $t$ (Kruskal, 1954). A location family $f(x - \theta)$ has an MLR in $x$ exactly when $\log f$ is concave.
- **An example with a continuous statistic.** Let $X_1, \dots, X_{10}$ be iid exponential with mean $\theta$, and test $\theta \le 1$ against $\theta > 1$ at $\alpha = 0.05$. Here $T = \sum X_i$ and $2T/\theta$ has the chi-squared distribution with 20 degrees of freedom. The UMP test rejects when $T > \chi^2_{20, 0.95}/2 = 31.4104/2 = 15.7052$. Its power is $0.4007$ at $\theta = 1.5$, $0.7347$ at $\theta = 2$ and $0.9588$ at $\theta = 3$, and it increases in $\theta$ as part 2 says. For a discrete $T$, the binomial example on the [UMP test](/uniformly-most-powerful-test/) page shows the randomization at $T = c$.
- **The p-value.** For the non-randomized form, the p-value of an observed $t$ is $P_{\theta_0}(T \ge t)$. By part 2 it is also the supremum of $P_\theta(T \ge t)$ over the composite null $\theta \le \theta_0$.
- **Confidence bounds.** By [test-interval duality](/test-interval-duality/), the set of $\theta_0$ that the UMP tests do not reject is a lower confidence bound for $\theta$. It is uniformly most accurate: it covers each false value below $\theta$ with the smallest probability (Lehmann and Romano, Chapter 3).
- **Decision problems.** Karlin and Rubin proved more than the testing result. For any decision problem with a monotone structure, the procedures that are monotone in $T$ form an essentially complete class. This links the theorem to [statistical decision theory](/statistical-decision-theory/).

## Tightness

**Two-sided alternatives.** For $H_0: \theta = \theta_0$ against $\theta \ne \theta_0$ in the normal mean family, the test of part 1 is most powerful against $\theta > \theta_0$ and poor against $\theta < \theta_0$. No UMP test exists, as the [UMP test](/uniformly-most-powerful-test/) page shows with numbers. The MLR gives UMP unbiased tests for two-sided problems only through the generalized Neyman-Pearson lemma (Lehmann and Romano, Chapter 4).

**The MLR condition.** Without it the conclusion can fail even for one-sided problems. For one Cauchy observation with location $\theta$, the ratio $(1 + x^2)/(1 + (x - \theta_1)^2)$ rises and then falls back to 1, the most powerful region against $\theta_1$ depends on $\theta_1$, and no UMP test of $\theta = 0$ against $\theta > 0$ exists.

**One real parameter.** The theorem needs a real parameter and a real statistic. With a nuisance parameter, such as the normal mean with unknown variance, there is in general no UMP one-sided test among all tests, and the [Student t-test](/student-t-test/) is UMP only among unbiased tests or among scale-invariant tests.

**Randomization.** The test has size exactly $\alpha$ only with the randomized value $\gamma$ at $T = c$ when $T$ is discrete. The non-randomized test "reject when $T > c$" is UMP at its own, smaller size.

**Strict increase.** Part 2 claims strict increase only where $0 < \beta < 1$. For the uniform family on $(0, \theta)$ with $n$ observations, the UMP test of $\theta \le 1$ against $\theta > 1$ rejects when $M > (1 - \alpha)^{1/n}$, and its power is 0 for every $\theta \le (1 - \alpha)^{1/n}$, so the power function is flat there.

## History

The theorem carries the names of Samuel Karlin and Herman Rubin because of their 1956 paper in the Annals of Mathematical Statistics, which developed the theory of decision procedures for families with a monotone likelihood ratio and proved that monotone procedures form an essentially complete class. A companion paper by the same authors in the Journal of the American Statistical Association (1956) studied which distributions have a monotone likelihood ratio. The special case for exponential families, and the use of the Neyman-Pearson lemma against each alternative, were known before, from Neyman and Pearson (1933) and from the work of Lehmann. The name "Karlin-Rubin theorem" is common in textbooks such as Casella and Berger. Lehmann and Romano state the same result as Theorem 3.4.1 without the name.

## References
