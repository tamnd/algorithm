---
tag: F1FA66
kind: theorem
slug: bernstein-von-mises-theorem
name: Bernstein-von Mises theorem
aliases:
- Bayesian central limit theorem
area: statistics-and-inference/bayesian-statistics
level: advanced
summary: In regular parametric models the posterior tends to a normal law centred at the MLE with the inverse Fisher information over n as covariance, whatever smooth prior is used.
prereqs: [asymptotic-normality-of-mle, credible-interval, total-variation-distance, fisher-information-matrix, bayesian-inference]
see_also: [laplace-approximation, jeffreys-prior, reference-prior, m-estimator, wald-test, confidence-interval, dirichlet-process, bayesian-information-criterion]
sources:
  - book: isbn:9780521496032
    title: "A. W. van der Vaart, Asymptotic Statistics, Cambridge University Press, 1998"
    locator: Chapter 10, Section 10.2 (Theorem 10.1, the Bernstein-von Mises theorem in total variation, and its proof); Chapter 7 (differentiability in quadratic mean and local asymptotic normality)
  - paper: "L. Le Cam, On some asymptotic properties of maximum likelihood estimates and related Bayes' estimates, University of California Publications in Statistics 1, 1953"
    locator: pages 277 to 329 (the asymptotic normality of posterior distributions and Bayes estimates)
  - paper: doi:10.1214/aos/1017938917
    title: "David Freedman, Wald Lecture: On the Bernstein-von Mises theorem with infinite-dimensional parameters, Annals of Statistics 27(4), 1999"
    locator: pages 1119 to 1141 (failure of the theorem for a Gaussian prior in an infinite-dimensional normal model)
  - paper: doi:10.1214/aos/1176349830
    title: "Persi Diaconis and David Freedman, On the consistency of Bayes estimates, Annals of Statistics 14(1), 1986"
    locator: pages 1 to 26 (inconsistent posteriors in nonparametric problems)
  - paper: doi:10.1214/12-EJS675
    title: "B. J. K. Kleijn and A. W. van der Vaart, The Bernstein-Von-Mises theorem under misspecification, Electronic Journal of Statistics 6, 2012"
    locator: pages 354 to 381 (the normal limit under a wrong model, and why credible sets are then not confidence sets)
  - book: isbn:9781439840955
    title: "Andrew Gelman, John B. Carlin, Hal S. Stern, David B. Dunson, Aki Vehtari and Donald B. Rubin, Bayesian Data Analysis, 3rd edition, CRC Press, 2013"
    locator: Chapter 4 (normal approximations to the posterior and large-sample theory) and Appendix B (outline of proofs of the asymptotic theorems)
---

The Bernstein-von Mises theorem says that in a regular parametric model with a fixed number of parameters, the posterior distribution is close, for large samples, to a normal law centred at the maximum likelihood estimate (or any efficient estimator) with covariance equal to the inverse Fisher information divided by $n$. The approximation holds in total variation, in probability under the true parameter, and it holds for every prior with a continuous positive density at the true value, so the prior stops mattering at first order. Its main use is as a bridge: under its conditions, Bayesian credible intervals are asymptotic frequentist confidence intervals. It can fail when the model is not regular, when the true value is on the boundary, and when the parameter is infinite-dimensional.

## Statement

Let $X_1, \ldots, X_n$ be iid with density $f(x \mid \theta)$, let $\theta_0$ be the true value, and let $\pi(d\theta \mid X_1, \ldots, X_n)$ be the posterior under a prior $\pi$. Let $I(\theta)$ be the [Fisher information](/fisher-information-matrix/) of one observation. The version below is Theorem 10.1 of van der Vaart (1998). Assume:

1. the parameter space $\Theta$ is an open subset of $\mathbb{R}^k$, with $k$ fixed (it does not grow with $n$), and $\theta_0 \in \Theta$;
2. the model is differentiable in quadratic mean at $\theta_0$, and $I(\theta_0)$ is nonsingular;
3. for every $\varepsilon > 0$ there is a sequence of tests $\phi_n$ with $E_{\theta_0}[\phi_n] \to 0$ and $\sup_{\lVert\theta - \theta_0\rVert \ge \varepsilon} E_\theta[1 - \phi_n] \to 0$ (uniformly consistent tests);
4. the prior has a density with respect to Lebesgue measure that is continuous and positive in a neighbourhood of $\theta_0$.

Then, with $\hat\theta_n$ the maximum likelihood estimator or any other estimator with $\sqrt n(\hat\theta_n - \theta_0) - I(\theta_0)^{-1} n^{-1/2}\sum_i \dot\ell_{\theta_0}(X_i) \to 0$ in probability, where $\dot\ell_\theta$ is the score,

$$\Big\lVert\, \pi(\cdot \mid X_1, \ldots, X_n) - N\big(\hat\theta_n,\ (n I(\theta_0))^{-1}\big) \Big\rVert_{TV} \to 0 \quad \text{in } P_{\theta_0}\text{-probability}.$$

Here $\lVert \cdot \rVert_{TV}$ is the [total variation distance](/total-variation-distance/). The same holds with $I(\hat\theta_n)$ in place of $I(\theta_0)$ when $I$ is continuous at $\theta_0$. Condition 3 holds, for example, when $\Theta$ is compact and the model is identifiable with continuous densities, or when the MLE is consistent in a suitable uniform sense.

## In plain words

When you have a lot of data from a well-behaved model with a fixed, small number of unknowns, your updated belief about the unknowns ends up shaped like a bell curve. The centre of the bell is the value that best fits the data. Its width shrinks like one over the square root of the sample size, and it is set by how much one observation tells you about the unknowns. Your starting belief does not matter much in the end, as long as it did not rule out the true value and was smooth near it. So for large samples, a Bayesian and a frequentist who use the same model report nearly the same interval. That agreement needs the conditions: a smooth model, a true value inside the allowed range, and a fixed number of unknowns.

## Proof

This is a sketch; the full proof is in van der Vaart (1998), Section 10.2. Work with the local parameter $h = \sqrt n(\theta - \theta_0)$.

**Step 1: the likelihood is locally normal.** Differentiability in quadratic mean gives local asymptotic normality: for every bounded sequence $h_n$,

$$\sum_{i=1}^n \log\frac{f(X_i \mid \theta_0 + h_n/\sqrt n)}{f(X_i \mid \theta_0)} = h_n^\top I(\theta_0)\Delta_n - \tfrac12 h_n^\top I(\theta_0) h_n + o_P(1),$$

where $\Delta_n = I(\theta_0)^{-1} n^{-1/2}\sum_i \dot\ell_{\theta_0}(X_i)$ converges in distribution to $N(0, I(\theta_0)^{-1})$ (van der Vaart, Theorem 7.2). As a function of $h$, the right side is the log of a $N(\Delta_n, I(\theta_0)^{-1})$ density, up to a constant.

**Step 2: the prior is locally flat.** The posterior density of $h$ is proportional to $\pi(\theta_0 + h/\sqrt n)$ times the likelihood ratio. On a ball $\lVert h \rVert \le M$, continuity and positivity of $\pi$ at $\theta_0$ give $\pi(\theta_0 + h/\sqrt n)/\pi(\theta_0) \to 1$ uniformly. So on every fixed ball the posterior of $h$, renormalized to the ball, is close in total variation to $N(\Delta_n, I(\theta_0)^{-1})$ renormalized to the ball.

**Step 3: the posterior concentrates at rate $1/\sqrt n$.** The tests of condition 3, together with the positive prior mass near $\theta_0$, show that the posterior mass of $\{\lVert h \rVert > M_n\}$ tends to 0 in probability for every $M_n \to \infty$. This step uses the tests to rule out distant $\theta$, and the local normality to sharpen the rate from consistency to $1/\sqrt n$ (van der Vaart, Lemma 10.3 and the proof of Theorem 10.1).

**Step 4: combine.** Steps 2 and 3 give $\lVert \pi(h \in \cdot \mid X) - N(\Delta_n, I(\theta_0)^{-1}) \rVert_{TV} \to 0$ in probability. Total variation does not change under the affine map $h \mapsto \theta_0 + h/\sqrt n$, and $\theta_0 + \Delta_n/\sqrt n = \hat\theta_n + o_P(n^{-1/2})$ for an efficient $\hat\theta_n$. Two normal laws with the same covariance and means $o_P(n^{-1/2})$ apart, on the scale $n^{-1/2}$, are close in total variation. $\square$

**A computed case.** For $X \sim$ Binomial$(n, p)$ with the uniform prior and $s = 0.3n$ successes, the posterior is Beta$(1 + s, 1 + n - s)$ and the theorem's normal law is $N(\hat p, \hat p(1 - \hat p)/n)$ with $\hat p = 0.3$. Their total variation distance, by numerical integration on 200000 equal cells of $[0, 1]$ plus the normal mass outside $[0, 1]$, is 0.0843 for $n = 10$, 0.0243 for $n = 100$ and 0.0074 for $n = 1000$. Each tenfold increase of $n$ divides it by about $\sqrt{10}$.

## Consequences

### The Bayesian reading

For large $n$ the posterior is approximately $N(\hat\theta_n, (nI(\hat\theta_n))^{-1})$ whatever smooth positive prior is used. Posterior quantiles are $\hat\theta_n + z_p/\sqrt{nI(\theta_0)} + o_P(n^{-1/2})$ in one dimension, so equal-tailed and highest-density credible intervals become the same interval. This is the justification for the normal approximation at the mode, the [Laplace approximation](/laplace-approximation/), and it explains why the choice among smooth priors, such as the [Jeffreys prior](/jeffreys-prior/) or a [reference prior](/reference-prior/), matters only at order $1/n$.

### The frequentist reading

Under $P_{\theta_0}$, the 1-dimensional equal-tailed $1 - \alpha$ [credible interval](/credible-interval/) is $\hat\theta_n \pm z_{1-\alpha/2}/\sqrt{nI(\theta_0)} + o_P(n^{-1/2})$. By [asymptotic normality of the MLE](/asymptotic-normality-of-mle/), $\sqrt n(\hat\theta_n - \theta_0)$ converges in distribution to $N(0, I(\theta_0)^{-1})$, so the coverage $P_{\theta_0}(\theta_0 \in C_n)$ tends to $1 - \alpha$ for each fixed $\theta_0$: the credible interval is an asymptotic [confidence interval](/confidence-interval/), the same to first order as the [Wald](/wald-test/) interval. In the binomial case with the uniform prior and $p = 0.3$, the exact coverage of the 95% equal-tailed interval, a sum of binomial probabilities, is 0.9244 for $n = 10$, 0.9496 for $n = 100$ and 0.9509 for $n = 1000$; at $n = 1000$ and $x = 300$ the credible interval is $[0.2724, 0.3291]$ and the Wald interval $[0.2716, 0.3284]$. These coverages are measured; the theorem gives only the limit. Posterior means and medians are also asymptotically efficient estimators.

### The bridge

The two readings are statements of different kinds: a posterior probability given the data, and a coverage over repeated samples at a fixed $\theta_0$. This theorem is the general result that connects them, and only under its conditions. Outside them, a credible interval has no coverage guarantee at a fixed $\theta_0$, and the agreement must be checked case by case.

## Tightness

**A support that moves.** For $X_i \sim$ Uniform$(0, \theta)$ the model is not differentiable in quadratic mean. With the prior density $1/\theta$ and $m = \max_i X_i$, the posterior has density $n m^n/\theta^{n+1}$ on $\theta \ge m$, and $P(\theta > m(1 + t/n) \mid X) = (1 + t/n)^{-n} \to e^{-t}$. So the posterior of $n(\theta - m)/m$ tends to an exponential law, not a normal one, and its scale is $1/n$, not $1/\sqrt n$. For $t = 1$ the value is 0.3855, 0.3697 and 0.3681 at $n = 10$, 100 and 1000, against $e^{-1} = 0.3679$.

**A true value on the boundary.** If $p_0 = 0$ in the binomial model, every sample is all zeros, the uniform-prior posterior is Beta$(1, n + 1)$, and $np$ under it tends to an exponential law. Condition 1 fails because $\theta_0$ is not an interior point. The same happens for a variance component equal to 0.

**A prior that misses $\theta_0$.** If the prior density is 0 near $\theta_0$, the posterior concentrates on the nearest point of the prior support and the theorem fails; condition 4 cannot be dropped.

**Infinite dimension.** Freedman (1999) showed that for a Gaussian prior in an infinite-dimensional normal model the posterior and the sampling distribution of the estimator do not agree, even though both are normal, so credible sets need not be confidence sets. Diaconis and Freedman (1986) gave nonparametric problems in which the posterior is not even consistent. Conditions 1 to 3 are where these failures enter.

**A wrong model.** If the data do not come from any $f(\cdot \mid \theta)$, the posterior still concentrates near the parameter $\theta^*$ that minimizes the Kullback-Leibler divergence, with a normal shape, but its covariance is the inverse of the second derivative of that divergence, not the sandwich covariance of the [M-estimator](/m-estimator/) theory. So credible sets do not have the right coverage (Kleijn and van der Vaart, 2012).

## History

Laplace used the normal approximation to the posterior of a binomial proportion in the 1770s and later. Sergei Bernstein (1917) and Richard von Mises (1931) stated versions for multinomial and related models, which gave the theorem its name. Lucien Le Cam (1953) gave the first general proof, together with the efficiency of Bayes estimates, and his later work on local asymptotic normality gave the modern form. Van der Vaart (1998) states it in total variation under differentiability in quadratic mean. Freedman's Wald lecture (1999) brought the infinite-dimensional failures to general attention.

## References
