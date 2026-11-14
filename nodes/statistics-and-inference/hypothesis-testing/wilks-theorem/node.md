---
tag: H9N9RF
kind: theorem
slug: wilks-theorem
name: Wilks' theorem
aliases:
- Wilks' phenomenon
area: statistics-and-inference/hypothesis-testing
level: core
summary: Under regularity and a true null, twice the log likelihood ratio tends to a chi-squared law with degrees of freedom equal to the number of constrained parameters.
prereqs: [likelihood-ratio-test, asymptotic-normality-of-mle, slutsky-theorem, fisher-information-matrix, score-function]
see_also: [wald-test, score-test, deviance-statistic, chi-squared-goodness-of-fit-test, akaike-information-criterion, empirical-likelihood, parametric-bootstrap, delta-method]
sources:
  - paper: doi:10.1214/aoms/1177732360
    title: S. S. Wilks, The large-sample distribution of the likelihood ratio for testing composite hypotheses, Annals of Mathematical Statistics 9(1) (1938), pages 60 to 62
    locator: the chi-squared limit with h degrees of freedom for h fixed parameters
  - book: isbn:9780521784504
    title: A. W. van der Vaart, Asymptotic Statistics, Cambridge University Press, 1998
    locator: Chapter 16 (likelihood ratio tests, the chi-squared limit for smooth hypotheses and the case of a boundary)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 10.3.1 (the asymptotic distribution of the likelihood ratio test statistic)
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Part II (large-sample theory), the chapters on likelihood ratio, Wald and Rao score tests in quadratic mean differentiable families
  - paper: doi:10.1080/01621459.1987.10478472
    title: Steven G. Self and Kung-Yee Liang, Asymptotic properties of maximum likelihood estimators and likelihood ratio tests under nonstandard conditions, Journal of the American Statistical Association 82(398) (1987), pages 605 to 610
    locator: the mixture of chi-squared laws when the true value is on the boundary
  - paper: doi:10.1093/biomet/64.2.247
    title: Robert B. Davies, Hypothesis testing when a nuisance parameter is present only under the alternative, Biometrika 64(2) (1977), pages 247 to 254
    locator: the failure of the chi-squared limit when a parameter is not identified under the null
---

Wilks' theorem gives the large-sample null distribution of the [likelihood ratio test](/likelihood-ratio-test/). If the null hypothesis fixes $r$ of the $k$ parameters of a regular model, or more generally restricts the parameter to a smooth surface of dimension $k - r$, then twice the log of the maximized likelihood ratio converges in distribution to $\chi^2_r$ when the null is true. The limit does not depend on the model, on the true parameter or on the parameters left free, which is why one table serves every likelihood ratio test. The theorem fails at the edges of its conditions: on the boundary of the parameter space, and when a parameter is not identified under the null.

## Statement

Let $X_1, \dots, X_n$ be iid with density $f(x; \theta)$, $\theta \in \Theta \subseteq \mathbb R^k$. Let $\ell(\theta) = \sum_i \log f(X_i; \theta)$ be the log-likelihood, $U_n(\theta) = \nabla \ell(\theta)$ the [score](/score-function/) of the sample and $I(\theta)$ the [Fisher information](/fisher-information-matrix/) of one observation. Let $\hat\theta$ maximize $\ell$ over $\Theta$ and $\hat\theta_0$ maximize $\ell$ over the null set $\Theta_0$. The likelihood ratio statistic is
$$\Lambda_n = 2\left(\ell(\hat\theta) - \ell(\hat\theta_0)\right) = -2\log\frac{\sup_{\theta \in \Theta_0} L(\theta; X)}{\sup_{\theta \in \Theta} L(\theta; X)}.$$

**Conditions.** Let $\theta_0$ be the true value.

1. $\Theta$ is an open subset of $\mathbb R^k$.
2. $\Theta_0$ is a smooth submanifold of dimension $k - r$, with $1 \le r \le k$. Concretely, near $\theta_0$ there are an open set $H \subseteq \mathbb R^{k-r}$ and a twice continuously differentiable map $g: H \to \Theta$ with $\Theta_0 = g(H)$ near $\theta_0$, $\theta_0 = g(\eta_0)$, and a $k \times (k - r)$ Jacobian $J = Dg(\eta_0)$ of full rank $k - r$. The case $r = k$ is a simple null, $\Theta_0 = \{\theta_0\}$.
3. $\theta_0$ is an interior point of $\Theta$, and $\eta_0$ is an interior point of $H$.
4. The model is regular at $\theta_0$, as needed for the [asymptotic normality of the MLE](/asymptotic-normality-of-mle/): the model is identifiable, the support of $f$ does not depend on $\theta$, $\log f(x; \theta)$ has three continuous derivatives in $\theta$ that are bounded near $\theta_0$ by a function $M(x)$ with $E_{\theta_0} M(X) < \infty$, and $I(\theta_0)$ is finite and positive definite.
5. $\hat\theta$ and $\hat\theta_0$ are consistent for $\theta_0$ under $\theta_0$.

**Theorem (Wilks, 1938).** Under conditions 1 to 5, when $\theta_0 \in \Theta_0$ is true,
$$\Lambda_n \xrightarrow{d} \chi^2_r \qquad (n \to \infty).$$

So the test that rejects when $\Lambda_n \ge \chi^2_{r, 1-\alpha}$, the upper $\alpha$ point of $\chi^2_r$, has size that tends to $\alpha$. The size is only near $\alpha$ for finite $n$.

## In plain words

You fit a model twice: once with all its knobs free, and once with some knobs held at the values the null claims. The free fit is always at least as good. The question is whether it is better by more than chance would allow. The theorem says how much better it gets by chance alone, when the null is true and the sample is large. The gain, measured on a log scale and doubled, behaves like a sum of squares of independent bell-curve draws, one for each knob that the null held fixed. It does not matter what the model is or what the other knobs are. So the same table works for every such comparison, provided the model is smooth and the held values are not at an edge of what is allowed.

## Proof

We prove the case of one parameter with a simple null, $k = r = 1$ and $\Theta_0 = \{\theta_0\}$, in full, using the asymptotic normality of the MLE. Then we sketch the general case and give a precise source.

**The scalar case.** Then $\hat\theta_0 = \theta_0$. Consistency and condition 3 put $\hat\theta$ in an open interval around $\theta_0$ with probability tending to 1, and there $\ell'(\hat\theta) = 0$. On this event, Taylor's theorem with the Lagrange remainder gives a point $\theta^*$ between $\theta_0$ and $\hat\theta$ with
$$\ell(\theta_0) = \ell(\hat\theta) + \ell'(\hat\theta)(\theta_0 - \hat\theta) + \tfrac12 \ell''(\theta^*)(\theta_0 - \hat\theta)^2 = \ell(\hat\theta) + \tfrac12 \ell''(\theta^*)(\hat\theta - \theta_0)^2.$$
So
$$\Lambda_n = \frac{-\ell''(\theta^*)/n}{I(\theta_0)} \cdot \left(\sqrt{n I(\theta_0)}\,(\hat\theta - \theta_0)\right)^2.$$
For the first factor, $-\ell''(\theta_0)/n$ is a mean of iid terms with expectation $I(\theta_0)$, so it converges in probability to $I(\theta_0)$ by the [law of large numbers](/law-of-large-numbers/). By condition 4 and the mean value theorem, $|\ell''(\theta^*) - \ell''(\theta_0)|/n \le |\theta^* - \theta_0| \cdot \frac1n\sum_i M(X_i)$, which is $o_p(1) \cdot O_p(1) = o_p(1)$. So the first factor converges in probability to 1. For the second factor, $\sqrt{n I(\theta_0)}(\hat\theta - \theta_0) \to N(0, 1)$ in distribution by the asymptotic normality of the MLE, so its square converges to $\chi^2_1$ by the continuous mapping theorem. By [Slutsky's theorem](/slutsky-theorem/), the product converges to $\chi^2_1$. The event where $\ell'(\hat\theta) = 0$ fails has probability tending to 0, so it does not change the limit. $\square$

**The general case (sketch).** Write $Z_n = U_n(\theta_0)/\sqrt n$, which converges to $N(0, I)$ with $I = I(\theta_0)$ by the [central limit theorem](/central-limit-theorem/). The same Taylor argument, now in $k$ dimensions, gives
$$2\left(\ell(\hat\theta) - \ell(\theta_0)\right) = Z_n^\top I^{-1} Z_n + o_p(1).$$
Under the null, the restricted model is a regular model in $\eta \in H$ with score $J^\top U_n(g(\eta))$ and information $J^\top I J$ at $\eta_0$. Applied to it, the same argument gives
$$2\left(\ell(\hat\theta_0) - \ell(\theta_0)\right) = Z_n^\top J (J^\top I J)^{-1} J^\top Z_n + o_p(1).$$
Subtract, and put $Y_n = I^{-1/2} Z_n$, which converges to $N(0, I_k)$:
$$\Lambda_n = Y_n^\top (I_k - P)\,Y_n + o_p(1), \qquad P = I^{1/2} J (J^\top I J)^{-1} J^\top I^{1/2}.$$
The matrix $P$ is symmetric and $P^2 = P$, so it is the orthogonal projection onto the column space of $I^{1/2} J$, which has dimension $k - r$. Then $I_k - P$ is a projection of rank $r$, and for $Y \sim N(0, I_k)$ the quadratic form $Y^\top (I_k - P) Y$ is a sum of $r$ squares of independent standard normals, that is $\chi^2_r$. The continuous mapping theorem and Slutsky's theorem finish the argument. A complete proof of this form, under weaker conditions (differentiability in quadratic mean), is in van der Vaart (1998), Chapter 16. Wilks (1938) proved the case where $\Theta_0$ fixes $r$ coordinates of $\theta$.

## Consequences

- **Degrees of freedom count constraints.** The number $r$ is $\dim\Theta - \dim\Theta_0$: the number of free parameters lost under the null. For the multinomial with $m$ cells and fully specified cell probabilities, $r = m - 1$, and the likelihood ratio statistic is the G-statistic $2\sum_j O_j \log(O_j/E_j)$. For independence in an $a \times b$ table, $r = (a - 1)(b - 1)$, as for the [chi-squared test of independence](/chi-squared-test-of-independence/).
- **A model-free calibration.** The limit does not depend on the nuisance parameters. This is the property that the alias "Wilks' phenomenon" names, and it also holds for some nonparametric likelihoods, such as the [empirical likelihood](/empirical-likelihood/).
- **Equivalence with the Wald and score statistics.** The same expansion shows that the [Wald statistic](/wald-test/) and the [score statistic](/score-test/) both equal $Y_n^\top(I_k - P)Y_n + o_p(1)$ under the null. So the three tests have the same $\chi^2_r$ limit and differ by $o_p(1)$.
- **Local power.** Under alternatives $\theta_n = \theta_0 + h/\sqrt n$, the statistic converges to a noncentral $\chi^2_r(\delta)$, where $\delta$ is the squared length of the component of $I^{1/2}h$ orthogonal to the column space of $I^{1/2}J$. This gives approximate power and sample sizes.
- **Deviance and model choice.** In generalized linear models, differences of [deviance](/deviance-statistic/) between nested models are likelihood ratio statistics, and Wilks' theorem calibrates them. The penalty $2k$ of the [Akaike information criterion](/akaike-information-criterion/) comes from the same expansion.

**How fast the limit is reached.** The theorem only says that the size tends to $\alpha$. Two exact computations show how far it can be for small $n$.

For a binomial count with $p_0 = 1/2$, $\Lambda_n = 2[K\log(K/(np_0)) + (n - K)\log((n - K)/(n(1 - p_0)))]$, and the exact probability of $\Lambda_n \ge 3.8415$ under the null is a finite sum:

| $n$ | 10 | 20 | 50 | 100 | 1000 |
|---|---|---|---|---|---|
| exact size, $p_0 = 0.5$ | 0.1094 | 0.0414 | 0.0649 | 0.0569 | 0.0537 |

The size moves above and below 0.05 because $K$ is discrete, and it settles slowly.

For a normal mean with unknown variance, $\Lambda_n = n\log(1 + T^2/(n - 1))$, where $T$ is the [Student t](/student-t-test/) statistic. This is an exact monotone function of $|T|$, so the exact size of the nominal 5% test is $P(|t_{n-1}| \ge \sqrt{(n - 1)(e^{3.8415/n} - 1)})$:

| $n$ | 3 | 5 | 10 | 20 | 50 | 200 |
|---|---|---|---|---|---|---|
| exact size | 0.1502 | 0.0979 | 0.0703 | 0.0593 | 0.0536 | 0.0509 |
| $E_0\Lambda_n$ | 1.8409 | 1.4019 | 1.1725 | 1.0803 | 1.0308 | 1.0076 |
| size of $\Lambda_n / E_0\Lambda_n$ | 0.0485 | 0.0497 | 0.0499 | 0.0500 | 0.0500 | 0.0500 |

The last row is the Bartlett correction (Bartlett, 1937): divide $\Lambda_n$ by its null mean, which has the form $r(1 + b/n + O(n^{-2}))$. Here $T^2/(n - 1)$ is a ratio $A/B$ of independent $\chi^2_1$ and $\chi^2_{n-1}$ variables, so $E_0\Lambda_n = n\left(\psi(n/2) - \psi((n - 1)/2)\right) = 1 + \tfrac{3}{2n} + O(n^{-2})$, with $\psi$ the digamma function. Under regularity, the corrected statistic has a $\chi^2_r$ law with error $O(n^{-2})$ instead of $O(n^{-1})$. The corrected sizes in the table are computed for each $n$; the $O(n^{-2})$ rate is the general theorem.

## Tightness

**The boundary.** Let $X_1, \dots, X_n$ be iid $N(\mu, 1)$ with $\Theta = [0, \infty)$, and test $\mu = 0$. Then $\hat\mu = \max(\bar X, 0)$ and $\Lambda_n = n\bar X^2\,\mathbf 1\{\bar X > 0\}$. Under the null $\sqrt n\bar X \sim N(0, 1)$, so $\Lambda_n$ is 0 with probability $1/2$ and $\chi^2_1$ with probability $1/2$, exactly, for every $n$. The limit is the mixture $\tfrac12\chi^2_0 + \tfrac12\chi^2_1$, not $\chi^2_1$. Using the $\chi^2_1$ cut $3.8415$ gives size $0.025$. The correct 5% cut is $\chi^2_{1, 0.90} = 2.7055$. Chernoff (1954) found the general form: on the boundary, the limit is the distance of a normal vector to a cone. Self and Liang (1987) gave the mixtures of chi-squared laws for variance components and other common cases. Condition 1 or 3 fails here.

**A parameter not identified under the null.** Test one normal component against a mixture of two, or no change against a change at an unknown time. Under the null, the location of the second component, or the time of change, does not appear in the model. Condition 4 fails, the statistic is the supremum of a random process over this parameter, and its limit is not $\chi^2$. For a normal mixture whose second mean can be any real number, the likelihood ratio statistic is not even bounded in probability. Davies (1977) gave bounds for the tail of such suprema.

**The number of parameters grows.** If the model has a nuisance parameter for each pair of observations (the Neyman-Scott problem), the MLE is not consistent and the chi-squared limit fails. Condition 5 fails.

**Misspecification.** If the true distribution is not in the model, the limit is a weighted sum of independent $\chi^2_1$ variables, with weights from the sandwich of the information and the variance of the score. The plain $\chi^2_r$ reference is then wrong.

**Discreteness and small samples.** The tables above show sizes from 0.04 to 0.15 for a nominal 0.05. For small $n$, use an exact test, a Bartlett correction or a [parametric bootstrap](/parametric-bootstrap/) of $\Lambda_n$.

## History

Neyman and Pearson proposed the likelihood ratio criterion in 1928. Samuel S. Wilks proved in 1938, in a three-page note in the Annals of Mathematical Statistics, that $-2\log\lambda$ has a limiting chi-squared distribution with as many degrees of freedom as the hypothesis fixes parameters. Wald (1943) extended the theory and proved the asymptotic equivalence of the likelihood ratio test with his own test. Chernoff (1954) treated the boundary case, Bartlett (1937) had already proposed the scale correction for a test of equal variances, and Lawley (1956) gave the general form of the correction. Self and Liang (1987) and Davies (1977, 1987) worked out the main nonstandard cases.

## References
