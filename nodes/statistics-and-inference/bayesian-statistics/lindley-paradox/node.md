---
tag: Q8ZSZF
kind: theorem
slug: lindley-paradox
name: Lindley paradox
aliases:
- Jeffreys-Lindley paradox
area: statistics-and-inference/bayesian-statistics
level: advanced
summary: With a diffuse prior and a large sample, data that reject a point null at any fixed significance level can still make a Bayes factor favour that null.
prereqs: [bayes-factor, z-test, p-value, marginal-likelihood]
see_also: [savage-dickey-density-ratio, bayesian-information-criterion, e-variable, jeffreys-prior, improper-prior, likelihood-ratio-test, bernstein-von-mises-theorem, neyman-pearson-lemma]
sources:
  - paper: "Dennis V. Lindley, A statistical paradox, Biometrika 44(1/2), 1957"
    title: Lindley 1957
    locator: pages 187 to 192 (the normal mean with a point null and a prior of fixed spread; general locator)
  - paper: "Maurice S. Bartlett, A comment on D. V. Lindley's statistical paradox, Biometrika 44(3/4), 1957"
    title: Bartlett 1957
    locator: pages 533 to 534 (the dependence of the posterior probability on the spread of the prior; general locator)
  - book: isbn:9780198503682
    title: "Harold Jeffreys, Theory of Probability, 3rd edition (1961), reprinted in Oxford Classic Texts in the Physical Sciences, Oxford University Press, 1998"
    locator: Chapter 5 (significance tests with one new parameter) and Appendix B (the grades of K)
  - paper: "Glenn Shafer, Lindley's paradox, Journal of the American Statistical Association 77(378), 1982"
    title: Shafer 1982
    locator: the paper and its discussion (general locator)
  - paper: "James O. Berger and Thomas Sellke, Testing a point null hypothesis: the irreconcilability of P values and evidence, Journal of the American Statistical Association 82(397), 1987"
    title: Berger and Sellke 1987
    locator: lower bounds on the posterior probability of a point null over classes of priors (general locator)
  - paper: doi:10.1080/01621459.1995.10476572
    title: "Robert E. Kass and Adrian E. Raftery, Bayes factors, Journal of the American Statistical Association 90(430), 1995"
    locator: the Schwarz approximation to the log Bayes factor and the remarks on diffuse priors (general locator)
---

The Lindley paradox is a limit theorem about the [Bayes factor](/bayes-factor/) for a point null hypothesis. If the test statistic stays at a value that a [z-test](/z-test/) calls significant, for example $z = 1.96$, and the sample size grows, then the Bayes factor in favour of the null goes to infinity. So the same data can reject the null at the 5% level and give the null a posterior probability near 1. The two answers differ because they answer different questions, and the theorem makes the difference exact.

## Statement

Let $x_1, \dots, x_n$ be independent $N(\theta, \sigma^2)$ with $\sigma > 0$ known, and let $\bar x$ be their mean. Compare

$$M_0: \theta = \theta_0, \qquad M_1: \theta \sim N(\theta_0, \tau^2), \quad \tau > 0,$$

and write $z = \sqrt n\, (\bar x - \theta_0)/\sigma$ for the z-statistic.

**Theorem.**

1. *(Exact formula.)* For every $n \ge 1$ and every data set,
$$B_{01} = \frac{m_0(x)}{m_1(x)} = \sqrt{1 + \frac{n\tau^2}{\sigma^2}}\; \exp\!\Big(-\frac{z^2}{2}\cdot \frac{n\tau^2}{\sigma^2 + n\tau^2}\Big).$$
2. *(Lindley's limit.)* Fix $z$, $\sigma$ and $\tau$. As $n \to \infty$, $B_{01} \to \infty$, and more exactly $B_{01} \big/ \big(\sqrt n\, (\tau/\sigma)\, e^{-z^2/2}\big) \to 1$. So for prior probability $P(M_0) \in (0, 1)$, $P(M_0 \mid x) \to 1$.
3. *(Bartlett's limit.)* Fix $n$, $z$ and $\sigma$. As $\tau \to \infty$, $B_{01} \to \infty$ like $\sqrt n\, (\tau/\sigma)\, e^{-z^2/2}$.
4. *(General prior.)* Replace the normal prior of $M_1$ by any prior density $g$ that is bounded on $\mathbb R$ and continuous and positive at $\theta_0$. Fix $z$ and let $n \to \infty$, so that $\bar x = \theta_0 + \sigma z/\sqrt n$. Then
$$B_{01} \sim \frac{\sqrt n\, \varphi(z)}{\sigma\, g(\theta_0)} \to \infty,$$
where $\varphi$ is the standard normal density. Part 2 is the case $g(\theta_0) = 1/(\tau\sqrt{2\pi})$.

The conditions matter: the null is a point that has positive prior probability, the prior of $M_1$ is proper and does not shrink with $n$, and $g(\theta_0) > 0$. The section on tightness shows what happens when one of them fails.

## In plain words

A significance test asks how surprising the data would be if the null were true. A fixed level, such as 5%, gives the same cut for every sample size. A Bayes factor asks which model predicted the data better. With many observations the estimate sits very close to the null value, at a small distance that the test still calls significant. The alternative model spread its prior belief over a wide range of values, so it gave little probability to that small region. The null put all its belief there. So the null wins the prediction contest, and it wins by more as the sample grows, even though the test keeps rejecting it.

## Proof

**Part 1.** The likelihood factors as
$$\prod_{i=1}^n f(x_i \mid \theta) = h(x)\, \frac{\sqrt n}{\sigma}\varphi\Big(\frac{\sqrt n(\bar x - \theta)}{\sigma}\Big), \qquad h(x) = (2\pi\sigma^2)^{-(n-1)/2} n^{-1/2} \exp\Big(-\frac{\sum_i (x_i - \bar x)^2}{2\sigma^2}\Big),$$
because $\sum_i (x_i - \theta)^2 = \sum_i (x_i - \bar x)^2 + n(\bar x - \theta)^2$. The factor $h(x)$ does not depend on $\theta$, so it cancels in $B_{01}$, and we may work with $\bar x \sim N(\theta, \sigma^2/n)$. Under $M_0$, the density of $\bar x$ is $N(\bar x; \theta_0, \sigma^2/n)$. Under $M_1$, $\bar x = \theta + e$ with $\theta \sim N(\theta_0, \tau^2)$ and $e \sim N(0, \sigma^2/n)$ independent, so its marginal density is $N(\bar x; \theta_0, \sigma^2/n + \tau^2)$. With $v_0 = \sigma^2/n$, $v_1 = \sigma^2/n + \tau^2$ and $d = \bar x - \theta_0$,
$$B_{01} = \sqrt{\frac{v_1}{v_0}}\, \exp\Big(-\frac{d^2}{2v_0} + \frac{d^2}{2v_1}\Big).$$
Here $v_1/v_0 = 1 + n\tau^2/\sigma^2$, and $d^2 = z^2\sigma^2/n$ gives
$$-\frac{d^2}{2v_0} + \frac{d^2}{2v_1} = -\frac{z^2}{2} + \frac{z^2}{2}\cdot\frac{\sigma^2}{\sigma^2 + n\tau^2} = -\frac{z^2}{2}\cdot\frac{n\tau^2}{\sigma^2 + n\tau^2}.$$

**Part 2.** With $z$ fixed, $n\tau^2/(\sigma^2 + n\tau^2) \to 1$, so the exponential factor goes to $e^{-z^2/2} > 0$, and $\sqrt{1 + n\tau^2/\sigma^2}\big/(\sqrt n\,\tau/\sigma) \to 1$. The product of the two limits gives the stated equivalence, and the right side goes to infinity. Then $P(M_0 \mid x) = B_{01} P(M_0)\big/\big(B_{01}P(M_0) + P(M_1)\big) \to 1$ by the odds form of the Bayes factor.

**Part 3.** With $n$ and $z$ fixed, $n\tau^2/(\sigma^2 + n\tau^2) \to 1$ as $\tau \to \infty$, and the same argument applies.

**Part 4.** As in Part 1, $m_0 \propto (\sqrt n/\sigma)\varphi(z)$ and
$$m_1 \propto \int \frac{\sqrt n}{\sigma}\varphi\Big(\frac{\sqrt n(\bar x - \theta)}{\sigma}\Big) g(\theta)\, d\theta = \int \varphi(u)\, g\Big(\bar x - \frac{\sigma u}{\sqrt n}\Big)\, du,$$
with the substitution $u = \sqrt n(\bar x - \theta)/\sigma$ and the same factor $h(x)$ in both. Since $\bar x - \sigma u/\sqrt n = \theta_0 + \sigma(z - u)/\sqrt n \to \theta_0$ for each $u$, continuity of $g$ at $\theta_0$ gives pointwise convergence of the integrand to $\varphi(u)g(\theta_0)$. The integrand is at most $\varphi(u)\sup g$, which is integrable, so dominated convergence gives $m_1/h(x) \to g(\theta_0)$. Hence $B_{01}\big/\big(\sqrt n\varphi(z)/(\sigma g(\theta_0))\big) \to 1$. $\square$

The exact formula of Part 1 agrees with a numerical integration of $m_1$ to a relative error below $10^{-13}$ for the values in the table below.

## Consequences

Take $\tau = \sigma = 1$. The table gives $B_{01}$ from Part 1 at the two-sided 5%, 1% and 0.1% critical values of $z$.

| $z$ (two-sided p) | $n = 1$ | 10 | 100 | 1000 | $10^4$ | $10^5$ | $10^6$ | $B_{01} = 1$ at $n \approx$ |
|---|---|---|---|---|---|---|---|---|
| 1.96 (0.05) | 0.541 | 0.579 | 1.501 | 4.644 | 14.65 | 46.33 | 146.5 | 42 |
| 2.576 (0.01) | 0.269 | 0.163 | 0.376 | 1.151 | 3.626 | 11.46 | 36.25 | 754 |
| 3.291 (0.001) | 0.094 | 0.024 | 0.047 | 0.142 | 0.446 | 1.409 | 4.455 | 50379 |

At $z = 1.96$ and prior odds 1, $P(M_0 \mid x)$ is $0.351$, $0.367$, $0.600$, $0.823$, $0.936$, $0.979$ and $0.993$ along the same row. At $n = 10^4$ the data reject $M_0$ at the 5% level, and on Jeffreys's grades they give strong support to $M_0$.

### Frequentist view

The z-test rejects $M_0$ at level $\alpha$ when $\lvert z\rvert > z_{\alpha/2}$. Under $M_0$, $z \sim N(0, 1)$ for every $n$, so the probability of a false rejection is exactly $\alpha$ for every $n$. For a fixed $\theta \ne \theta_0$, $\lvert z\rvert$ grows like $\sqrt n$ and the power goes to 1. The p-value of $z = 1.96$ is $0.05$ whatever $n$ is. All of these statements are about the distribution of $z$ under fixed parameter values, and none of them is a probability of $M_0$.

### Bayesian view

$B_{01}$ compares how well $M_0$ and $M_1$ predicted the observed $\bar x$. It depends on $z$ and on $n\tau^2/\sigma^2$, not on $z$ alone. Under $M_0$, $z$ stays bounded in probability, so Part 2 gives $B_{01} \to \infty$ in probability: the Bayes factor is consistent for the null. Under a fixed $\theta \ne \theta_0$, $z^2$ grows like $n$, the exponential factor wins, and $B_{01} \to 0$. Data with $z$ fixed at $1.96$ as $n$ grows are typical of neither case: they come from $\theta - \theta_0$ of order $\sigma/\sqrt n$, a region where the prior of $M_1$ has mass of order $1/\sqrt n$.

### What connects them

The connecting result is Lindley's limit, Part 2, written on the log scale:

$$\log B_{01} = \tfrac12 \log n - \tfrac{z^2}{2} + \log\frac{\tau}{\sigma} + o(1).$$

Both views use the same statistic $z$. The test compares $z^2$ with a constant. The Bayes factor compares $z^2$ with $\log n$ plus a constant that depends on the prior. A Bayesian who rejects $M_0$ when $B_{01} < k$ uses the cut $z^2 > \log n + 2\log(\tau/\sigma) - 2\log k + o(1)$, which grows with $n$, so the two rules must disagree for large $n$. The first two terms are $\tfrac12(\mathrm{BIC}_1 - \mathrm{BIC}_0)$ for this model, because twice the maximized log likelihood ratio is $z^2$; so the [Bayesian information criterion](/bayesian-information-criterion/) inherits the same growing cut. With $\tau = \sigma$ the remainder is $o(1)$: $\log B_{01}$ is $0.406$ against $\tfrac12\log n - z^2/2 = 0.382$ at $n = 100$, and the two agree to $2 \times 10^{-4}$ at $n = 10^4$.

A second link holds for every $n$ and every prior. The bound $m_1 \le \sup_\theta f(x \mid \theta)$ on the [Bayes factor](/bayes-factor/) page gives $B_{01} \ge e^{-z^2/2}$, so at $z = 1.96$ no prior on $M_1$ gives $B_{01}$ below $0.1465$, or $P(M_0 \mid x)$ below $0.128$ with prior odds 1. A p-value of 0.05 is therefore never strong evidence against a point null in the Bayes factor sense. Berger and Sellke (1987) give sharper bounds for classes of symmetric priors.

## Tightness

- **The rate $\sqrt n$ is exact.** Part 2 is an equivalence, not a bound, and the table matches it.
- **A prior that shrinks with $n$ removes the paradox.** If $\tau^2 = c\,\sigma^2/n$ for a fixed $c > 0$, Part 1 gives $B_{01} = \sqrt{1 + c}\,\exp\big(-\tfrac{z^2}{2}\cdot\tfrac{c}{1 + c}\big)$, a decreasing function of $\lvert z\rvert$ alone, so $B_{01}$ and the p-value then order data sets in the same way for every $n$. At $z = 1.96$ this is $0.646$, $0.541$ and $0.481$ for $c = 0.5$, $1$ and $4$. Such a prior is chosen for the sample size, which most Bayesians reject as a statement of belief.
- **The point mass is needed.** If $M_0$ is the half line $\theta \le \theta_0$ and the prior is a continuous density, the posterior probability of $M_0$ tends to the one-sided p-value $\Phi(-z)$ as the prior spreads, and there is no paradox.
- **The prior must be proper.** As $\tau \to \infty$ (Part 3), $B_{01} \to \infty$ for every data set, so an improper flat prior on $M_1$ always favours $M_0$. This is why Bayes factors with [improper priors](/improper-prior/) are not defined.
- **The condition $g(\theta_0) > 0$ matters.** If $g$ vanishes at $\theta_0$ (a non-local prior), the denominator of Part 4 goes to 0 faster and $B_{01}$ grows faster than $\sqrt n$.

## History

Jeffreys built his significance tests in *Theory of Probability* (first edition 1939) on a point null with positive prior mass, and he knew that his Bayes factor needed larger $\lvert z\rvert$ for larger samples. Lindley (1957) stated the conflict as a paradox: for any fixed level, a large enough sample gives data that are significant at that level and that make the null very probable. Bartlett (1957) replied that the posterior probability depends on the spread of the prior, so that a flat prior makes it go to 1 for any data, which is Part 3. Shafer (1982) and its discussion, and Berger and Sellke (1987), reopened the debate on how p-values and Bayes factors should be compared. The name Jeffreys-Lindley paradox credits both authors.

## References
