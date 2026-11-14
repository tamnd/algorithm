---
tag: MZX1D5
kind: definition
slug: p-value
name: P-value
aliases:
- observed significance level
area: statistics-and-inference/hypothesis-testing
level: intro
summary: The probability, under the null hypothesis, of a test statistic at least as extreme as the one observed. Rejecting when it is at most alpha gives a level-alpha test.
prereqs: [statistical-hypothesis-test, type-i-and-type-ii-errors]
see_also: [z-test, binomial-test, e-variable, bayes-factor, lindley-paradox, false-discovery-rate, fisher-combined-probability-test, permutation-test]
sources:
  - url: https://psychclassics.yorku.ca/Fisher/Methods/
    title: Ronald A. Fisher, Statistical Methods for Research Workers, Oliver and Boyd, 1925, online text of the first edition
    locator: Chapter III, section 12 (P as the probability of a deviation at least as large, and the 5% point)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 8.3.4 (p-values, the definition of a valid p-value and the theorem that the tail probability is valid)
  - book: isbn:9780387402727
    title: Larry Wasserman, All of Statistics, Springer, 2004
    locator: Section 10.2 (p-values, their interpretation and their uniform distribution under the null)
  - paper: doi:10.1080/00031305.2016.1154108
    title: "Ronald L. Wasserstein and Nicole A. Lazar, The ASA statement on p-values: context, process, and purpose, The American Statistician 70(2), 2016, pp. 129 to 133"
    locator: The six principles on the use and interpretation of p-values
---

The p-value of a [statistical hypothesis test](/statistical-hypothesis-test/) is the probability, computed under the null hypothesis $H_0$, of a test statistic at least as extreme as the one observed. Small values mean that the data would be unusual if $H_0$ were true. It is valid in a precise sense: under $H_0$, the probability that it is at most $u$ is at most $u$, so the rule "reject when $p \le \alpha$" has level $\alpha$ for every $\alpha$ at once. It is uniform on $[0, 1]$ under a simple null with a continuous statistic and stochastically larger than uniform for a discrete one. It is not the probability that $H_0$ is true.

## Definition

Let $T(X)$ be a test statistic whose large values are evidence against $H_0: \theta \in \Theta_0$, and let $t = T(x)$ be its observed value. The p-value is

$$p(x) = \sup_{\theta \in \Theta_0} P_\theta\big(T(X) \ge t\big).$$

For a simple null $\Theta_0 = \{\theta_0\}$ this is $P_{\theta_0}(T \ge t_{\text{obs}})$. For a two-sided test with a statistic whose null law is symmetric about 0, it is $P_{\theta_0}(|T| \ge |t|)$, twice the one-sided tail. For an asymmetric discrete null law there are several two-sided rules (doubling the smaller tail, or summing the probabilities of outcomes no more likely than the observed one), and they can differ.

**Validity.** For every $\theta \in \Theta_0$ and every $u \in [0, 1]$, $P_\theta(p(X) \le u) \le u$.

*Proof.* Fix $\theta \in \Theta_0$ and let $G(s) = P_\theta(T \ge s)$, which is non-increasing in $s$. Since $p(X) \ge G(T(X))$, it suffices to show $P_\theta(G(T) \le u) \le u$. The set $\{s : G(s) \le u\}$ is an interval going to $+\infty$ with left end $s^*$. If it contains $s^*$, then $\{G(T) \le u\} = \{T \ge s^*\}$, whose probability is $G(s^*) \le u$. If not, then $\{G(T) \le u\} = \{T > s^*\}$, whose probability is $\lim_{s \downarrow s^*}G(s) \le u$. $\square$

**Uniform when continuous.** If $\Theta_0 = \{\theta_0\}$ and $T$ has a continuous distribution under $\theta_0$, then $G$ is continuous and $P(G(T) \le u) = u$ for all $u$: the p-value is exactly uniform on $[0, 1]$, and the test "reject when $p \le \alpha$" has size exactly $\alpha$. If $T$ is discrete, $p$ takes finitely or countably many values and $P(p \le u) < u$ for most $u$: the p-value is stochastically larger than uniform, and the test is conservative.

**Monte Carlo p-value.** If the null law of $T$ cannot be computed but can be sampled, draw $T_1^*, \dots, T_b^*$ independently from it and use

$$\hat p = \frac{1 + \#\{i : T_i^* \ge t\}}{1 + b} .$$

Under a simple null, $T, T_1^*, \dots, T_b^*$ are $b + 1$ exchangeable values, so the rank of $T$ among them is uniform (with ties broken against rejection) and $P(\hat p \le u) \le u$ exactly, for every $b$. The version without the two 1s can be 0 and is not valid.

## Examples and non-examples

**A continuous statistic.** Nine packs from a machine set to 500 g, with known $\sigma = 4$ g, have mean $4525/9 = 502.78$ g, so the [z-test](/z-test/) statistic is $z = 25/12 = 2.0833$. The two-sided p-value is $2P(Z \ge 2.0833) = 0.037221$ and the one-sided p-value for $H_1: \mu > 500$ is 0.018610.

**A discrete statistic.** With $X \sim \text{Binomial}(10, 1/2)$ under $H_0$ and $H_1: p > 1/2$, the p-value $P_{1/2}(X \ge x)$ takes the values 0.3770, 0.1719, 0.0547, 0.0107 and 0.000977 at $x = 6, 7, 8, 9, 10$ (exact sums). So $P(p \le 0.05) = P(X \ge 9) = 0.0107$, far below 0.05: the test "reject when $p \le 0.05$" has size 0.0107. The exact [binomial test](/binomial-test/) has this property at every $n$.

**The p-value mixes the effect and the sample size.** A one-sample z-test of a mean shifted by $0.01\sigma$ with $n = 10^6$ gives $z = 10$ and $p = 1.5 \times 10^{-23}$; a shift of $0.5\sigma$ with $n = 10$ gives $z = 1.581$ and $p = 0.114$. For a two-sample t-test with the same sample [effect size](/effect-size/) $d = 0.3$ and $n$ per group (so $t = 0.3\sqrt{n/2}$ with $2n - 2$ degrees of freedom), the two-sided p-value is 0.511 at $n = 10$, 0.137 at $n = 50$, 0.0029 at $n = 200$ and $2.6 \times 10^{-11}$ at $n = 1000$.

**Non-example: the probability that $H_0$ is true.** $p$ is computed assuming $H_0$; it is $P(\text{data this extreme} \mid H_0)$, not $P(H_0 \mid \text{data})$. The second needs a prior probability for $H_0$ and is a Bayesian quantity; with a [Bayes factor](/bayes-factor/) the two can disagree sharply, most of all at large $n$ ([Lindley's paradox](/lindley-paradox/)).

**Non-example: the type I error rate.** The level $\alpha$ of the rule is fixed before the data. Reporting "$p = 0.003$, so the error rate is 0.3%" mixes a property of the data with a property of the procedure.

**Non-example: evidence for the null.** $p = 0.4$ does not show that $H_0$ is true: with low power, a real effect gives large p-values most of the time. "Not significant" is not "no effect".

The ASA statement of 2016 (Wasserstein and Lazar) puts two of these points as principles: "A p-value, or statistical significance, does not measure the size of an effect or the importance of a result", and "By itself, a p-value does not provide a good measure of evidence regarding a model or hypothesis."

## Related definitions

- **Significance level.** The threshold $\alpha$ fixed in advance; the test rejects when $p \le \alpha$. The p-value is the smallest level at which the observed data would lead to rejection, hence the name observed significance level.
- **Mid-p-value.** For a discrete statistic, $P(T > t) + \tfrac12 P(T = t)$. It is closer to uniform on average but is not valid in the sense above.
- **Adjusted p-values.** In multiple testing, p-values modified so that comparing them with $\alpha$ controls a family-wise error rate or a [false discovery rate](/false-discovery-rate/).
- **[E-variable](/e-variable/).** A nonnegative statistic with expectation at most 1 under $H_0$. By Markov's inequality $\min(1, 1/E)$ is a valid p-value, and e-variables can be multiplied across independent studies and monitored continuously.
- **Combining p-values.** For independent tests with continuous statistics, [Fisher's method](/fisher-combined-probability-test/) uses $-2\sum\log p_i$, which is chi-square with $2k$ degrees of freedom under all the nulls.

## References
