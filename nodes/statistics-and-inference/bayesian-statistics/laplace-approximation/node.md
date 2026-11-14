---
tag: M8AVZX
kind: technique
slug: laplace-approximation
name: Laplace approximation
aliases:
- Laplace's method for posteriors
area: statistics-and-inference/bayesian-statistics
level: core
summary: Approximates a posterior by a normal law centred at its mode with covariance the inverse Hessian of minus the log posterior. It also approximates the marginal likelihood.
history:
  year: 1774
  people: [Pierre-Simon Laplace, Luke Tierney, Joseph B. Kadane, Robert E. Kass]
  note: Laplace (1774) approximated beta integrals of the binomial posterior by expanding the log integrand at its maximum. Tierney and Kadane (1986) made the method a standard tool for posterior moments and marginal densities, and Kass, Tierney and Kadane (1990) gave conditions for its O(1/n) error.
prereqs: [bayesian-inference, marginal-likelihood, maximum-a-posteriori-estimation, newton-raphson-method, cholesky-decomposition]
see_also: [bayesian-information-criterion, bernstein-von-mises-theorem, stirling-approximation, integrated-nested-laplace-approximation, variational-inference, bridge-sampling, nested-sampling, importance-sampling]
sources:
  - paper: doi:10.1214/ss/1177013620
    title: "Stephen M. Stigler, Laplace's 1774 memoir on inverse probability, Statistical Science 1(3), 1986"
    locator: pages 359 to 378 (Stigler's introduction and the English translation of Laplace's Memoir on the probability of the causes of events, where the beta integral of the binomial posterior is approximated at its maximum; general locator)
  - paper: doi:10.1080/01621459.1986.10478240
    title: "Luke Tierney and Joseph B. Kadane, Accurate approximations for posterior moments and marginal densities, Journal of the American Statistical Association 81(393), 1986"
    locator: pages 82 to 86 (the fully exponential form, the ratio of two Laplace approximations with relative error O(n^-2), and the approximation of marginal posterior densities)
  - paper: "Robert E. Kass, Luke Tierney and Joseph B. Kadane, The validity of posterior expansions based on Laplace's method, in Bayesian and Likelihood Methods in Statistics and Econometrics, Essays in Honor of George A. Barnard (S. Geisser, J. S. Hodges, S. J. Press and A. Zellner, eds.), North-Holland, 1990"
    title: Kass, Tierney and Kadane 1990
    locator: pages 473 to 488 (regularity conditions under which the Laplace approximation of a posterior integral has relative error O(1/n); general locator)
  - paper: doi:10.1080/01621459.1995.10476572
    title: "Robert E. Kass and Adrian E. Raftery, Bayes factors, Journal of the American Statistical Association 90(430), 1995"
    locator: pages 773 to 795 (the Laplace approximation of the marginal likelihood, its error, and the Schwarz criterion as a cruder version; general locator)
  - book: isbn:9780486642215
    title: "N. G. de Bruijn, Asymptotic Methods in Analysis, 3rd edition, Dover, 1981"
    locator: Chapter 4, The Laplace method for integrals (4.2 a general case, 4.4 asymptotic expansions, 4.5 the Gamma function, 4.6 multiple integrals)
  - book: isbn:9781439840955
    title: "Andrew Gelman, John B. Carlin, Hal S. Stern, David B. Dunson, Aki Vehtari and Donald B. Rubin, Bayesian Data Analysis, 3rd edition, CRC Press, 2013"
    locator: Chapter 4, Section 4.1 (normal approximation to the posterior) and Chapter 13 (modal and distributional approximations); general locator
---

The Laplace approximation replaces a posterior by a normal law. Write $\ell(\theta) = \log f(x \mid \theta) + \log \pi(\theta)$ for the log of likelihood times prior, $\hat\theta$ for its maximum (the posterior mode) and $H = -\nabla^2 \ell(\hat\theta)$ for the curvature there. Then the posterior is approximately $N(\hat\theta, H^{-1})$, and the [marginal likelihood](/marginal-likelihood/) $Z = m(x) = \int f(x \mid \theta)\pi(\theta)\, d\theta$ is approximately

$$\hat Z = e^{\ell(\hat\theta)}\, (2\pi)^{d/2} \det(H)^{-1/2}, \qquad \log \hat Z = \ell(\hat\theta) + \frac d2 \log 2\pi - \frac12 \log\det H,$$

for $d$ parameters. It is exact when $\ell$ is quadratic. For $n$ observations from a regular model the relative error $\hat Z/Z - 1$ is $O(1/n)$. The cost is one optimization and one Hessian, so it is often thousands of times cheaper than sampling.

## In plain words

Near its highest point, most smooth hills look like a bell. The Laplace approximation finds the top of the hill of the posterior, measures how sharply the hill curves there, and replaces the hill by the bell with the same top and the same curvature. The volume under a bell has a formula, so you also get the total volume under the hill, which is the evidence for the model. With much data the hill is narrow and very close to a bell, so the answer is good. With little data, a lopsided hill, a hill cut off by a wall, or two hills, the bell is a poor copy, and the answer can be far off.

## When it applies

- **The log posterior is smooth, with one dominant interior mode.** The theorem below needs four derivatives near the mode and a mode that is clearly higher than everything far from it.
- **Many observations per parameter.** The error is $O(1/n)$ with a constant that grows with the dimension $d$. In the examples below the error is about $0.03$ nats per parameter at $n = 10$ and $0.0003$ at $n = 1000$.
- **Unconstrained parameters.** Map a probability to its logit, a variance to its logarithm, and include the Jacobian of the map in $\ell$. A mode on the boundary breaks the method.
- **Not for discrete parameters, and not for multimodal posteriors.** Use [importance sampling](/importance-sampling/), [bridge sampling](/bridge-sampling/) or [nested sampling](/nested-sampling/) instead.

**Theorem (Laplace's method).** Let $I_n = \int g(\theta)\, e^{n h(\theta)}\, d\theta$ over an open $\Theta \subseteq \mathbb{R}^d$. Assume (A1) $h$ has an interior maximum at $\hat\theta$ with $\sup_{\lvert \theta - \hat\theta \rvert \ge \delta} h(\theta) < h(\hat\theta)$ for every $\delta > 0$; (A2) $h$ is four times continuously differentiable near $\hat\theta$ and $H = -\nabla^2 h(\hat\theta)$ is positive definite; (A3) $g$ is twice continuously differentiable near $\hat\theta$ and $g(\hat\theta) \ne 0$; (A4) $\int \lvert g \rvert e^{n_0 h} < \infty$ for some $n_0$. Then

$$I_n = e^{n h(\hat\theta)} \Big(\frac{2\pi}{n}\Big)^{d/2} \det(H)^{-1/2}\, g(\hat\theta)\, \big(1 + O(1/n)\big).$$

If moreover $g > 0$ near $\hat\theta$, the version that expands $\ell_n = n h + \log g$ at its own mode, as the template does, has the same $O(1/n)$ relative error. Both are proved in full in proofs/correctness.md: the proof rescales $\theta - \hat\theta = u/\sqrt n$, shows that the odd third-order terms integrate to zero over a symmetric ball, bounds the rest by $C/n$ with a Gaussian envelope, and bounds the part far from the mode by $e^{-n\eta}$.

What is proved and what is cited. The theorem covers a log-likelihood $n h(\theta)$ with a fixed $h$, which includes Bernoulli data with a fixed share of successes, the setting of the examples. For random data, $h$ changes with $n$; Kass, Tierney and Kadane (1990) give conditions, uniform in $n$, under which the relative error is still $O(1/n)$. That result is cited, not proved here. The $O(n^{-2})$ error of the Tierney and Kadane ratio below is also cited, and it is measured in the table.

## The template

The holes are the log posterior `ℓ` (the model, in the chosen parameterization, Jacobian included) and the start `θ₀`.

```pseudo id=main
LAPLACE(ℓ, ∇ℓ, ∇²ℓ, θ₀)                  ▷ ℓ(θ) = log f(x | θ) + log π(θ), up to a constant
L1  θ ← θ₀
L2  repeat
L3      g ← ∇ℓ(θ);  H ← -∇²ℓ(θ)
L4      L ← CHOLESKY(H)                    ▷ fails if H is not positive definite
L5      solve L Lᵀ s = g                   ▷ the Newton step
L6      t ← 1;  while ℓ(θ + t s) < ℓ(θ) do t ← t/2
L7      θ ← θ + t s
L8  until the step t s is below the tolerance
L9  H ← -∇²ℓ(θ);  L ← CHOLESKY(H)
L10 log Ẑ ← ℓ(θ) + (d/2) log 2π - Σᵢ log Lᵢᵢ
L11 return θ̂ = θ, Σ = H⁻¹, log Ẑ
```

Lines L1 to L8 are [Newton's method](/newton-raphson-method/) for the [posterior mode](/maximum-a-posteriori-estimation/), with step halving so that $\ell$ never falls. Line L4 uses the [Cholesky decomposition](/cholesky-decomposition/): it costs $\Theta(d^3)$ and doubles as the test that the current point is in a concave region. If it fails far from the mode, a common fix is to add a multiple of the identity to $H$ (a Levenberg-Marquardt step). Line L10 uses $\log\det H = 2\sum_i \log L_{ii}$, which never forms the determinant itself, so it cannot overflow. The approximate posterior is $N(\hat\theta, H^{-1})$, and $H^{-1}$ comes from the same factor.

**Trace.** Bernoulli data with $x = 3$ successes in $n = 10$ trials, prior Beta(2, 2), logit scale $\theta = \log(p/(1-p))$. With $\alpha = 2 + 3 = 5$ and $\beta = 2 + 7 = 9$, the log posterior with the Jacobian $p(1 - p)$ is $\ell(\theta) = \alpha \log p + \beta \log(1 - p) - \log B(2, 2)$, with $\ell' = \alpha - (\alpha + \beta)p$ and $-\ell'' = (\alpha + \beta)p(1 - p)$.

| step | $\theta$ | $p$ | $\ell'(\theta)$ | $-\ell''(\theta)$ | $\ell(\theta)$ |
|---|---|---|---|---|---|
| 0 | 0 | 0.5 | $-2$ | 3.5 | $-7.912301$ |
| 1 | $-0.571429$ | 0.360907 | $-0.052702$ | 3.229145 | $-7.333263$ |
| 2 | $-0.587749$ | 0.357151 | $-0.000121$ | 3.214320 | $-7.332832$ |
| 3 | $-0.587787$ | 0.357143 | $0.000000$ | 3.214286 | $-7.332832$ |

The mode is $\hat p = 5/14$, $H = 45/14$, and L10 gives $\log \hat Z = -7.332832 + \frac12\log 2\pi - \frac12 \log(45/14) = -6.997696$. The exact value is $\log B(5, 9) - \log B(2, 2) = -6.977748$, so the error is $0.0199$ nats, a relative error of $2\%$ in $Z$. The approximate posterior of $\theta$ is $N(-0.5878, 0.5578^2)$.

## Classic examples

**Stirling's formula.** $\Gamma(n + 1) = \int_0^\infty t^n e^{-t} dt = n^{n+1}\int_0^\infty e^{n(\log s - s)} ds$. Here $h(s) = \log s - s$ has its maximum at $s = 1$ with $-h''(1) = 1$, and the theorem gives $\sqrt{2\pi n}\, n^n e^{-n}$, which is [Stirling's approximation](/stirling-approximation/). The error in the logarithm is $1/(12n) + O(n^{-3})$:

| $n$ | 1 | 2 | 5 | 10 | 100 | 1000 |
|---|---|---|---|---|---|---|
| $\log \Gamma(n+1) - \log(\text{Laplace})$ | 0.081061 | 0.041341 | 0.016645 | 0.0083306 | 0.00083333 | 0.0000833333 |
| $n \times$ error | 0.0811 | 0.0827 | 0.0832 | 0.0833 | 0.0833 | 0.0833 |

**Beta-binomial evidence, and the parameterization.** Take $x = 0.3n$ successes in $n$ Bernoulli trials and the prior Beta(2, 2). The exact log evidence is $\log B(2 + x, 2 + n - x) - \log B(2, 2)$. The table gives exact minus Laplace, in the probability scale $p$ and in the logit scale (Jacobian included):

| $n$ | exact $\log Z$ | error, $p$ scale | $n \times$ error | error, logit scale | $n \times$ error |
|---|---|---|---|---|---|
| 10 | $-6.977748$ | $-0.055784$ | $-0.558$ | $0.019949$ | $0.199$ |
| 100 | $-63.028491$ | $-0.006711$ | $-0.671$ | $0.002960$ | $0.296$ |
| 1000 | $-613.949377$ | $-0.000685$ | $-0.685$ | $0.000312$ | $0.312$ |
| 10000 | $-6112.878557$ | $-0.0000686$ | $-0.686$ | $0.0000313$ | $0.313$ |

Both errors fall like $1/n$, as the theorem says, but the logit scale is better by a factor of more than two and has the opposite sign. In the logit scale the integral is $\int p^\alpha (1-p)^\beta d\theta = B(\alpha, \beta)$, and the Laplace value is exactly Stirling's formula applied to $\Gamma(\alpha)\Gamma(\beta)/\Gamma(\alpha + \beta)$. So the error is $\mu(\alpha) + \mu(\beta) - \mu(\alpha + \beta)$, where $0 < \mu(z) < 1/(12z)$ is the error of Stirling's formula for $\Gamma(z)$. The [marginal likelihood](/marginal-likelihood/) page has the same check with the flat prior in the $p$ scale.

**The normal-normal model.** $x_i \sim N(\theta, \sigma^2)$ and $\theta \sim N(\mu_0, \tau^2)$. Then $\ell$ is quadratic in $\theta$, Newton stops after one step, and the approximation is exact: $\hat Z$ equals the density of $x$ under $N(\mu_0 \mathbf{1}, \sigma^2 I + \tau^2 \mathbf{1}\mathbf{1}^\top)$. The same holds for every linear-Gaussian model, such as [Bayesian linear regression](/bayesian-linear-regression/) with known noise.

**The Bayesian information criterion.** Keep only the terms of $\log \hat Z$ that grow with $n$: $\ell(\hat\theta) \approx \log f(x \mid \hat\theta_{\mathrm{ML}})$ and $\log\det H \approx d\log n + O(1)$. This gives $\log Z = \log f(x \mid \hat\theta_{\mathrm{ML}}) - \frac d2 \log n + O(1)$, which is minus one half of the [BIC](/bayesian-information-criterion/). The dropped $O(1)$ terms are why BIC is a cruder approximation than Laplace: in the beta-binomial example above the BIC error is $0.361$ nats at $n = 100$ and $0.369$ at $n = 1000$, and it tends to $\frac12\log(2\pi \cdot 0.21) + \log \pi(0.3) = 0.370$ instead of $0$.

**Posterior moments by Tierney and Kadane.** For a positive function $q$, write $\mathbb{E}[q(\theta) \mid x] = \int e^{\ell + \log q} / \int e^{\ell}$ and apply Laplace to the numerator and the denominator separately, each at its own mode (the fully exponential form). Leading error terms cancel in the ratio, and Tierney and Kadane (1986) show a relative error of $O(n^{-2})$. For $q(p) = p$ under the Beta$(2 + x, 2 + n - x)$ posterior, logit scale, $x = 0.3n$:

| $n$ | exact mean | Tierney-Kadane | relative error | $n^2 \times$ relative error | plug-in mode, $n \times$ relative error |
|---|---|---|---|---|---|
| 10 | 0.357143 | 0.357991 | $2.37 \times 10^{-3}$ | 0.237 | $-0.667$ |
| 100 | 0.307692 | 0.307714 | $7.13 \times 10^{-5}$ | 0.713 | $-1.225$ |
| 1000 | 0.300797 | 0.300797 | $8.28 \times 10^{-7}$ | 0.828 | $-1.322$ |

The last column is the error of the posterior mode used as an estimate of the mean: it is $O(1/n)$. The ratio form is $O(n^{-2})$, as measured in the fifth column.

**Larger models.** The same template gives the posterior of [Gaussian process](/gaussian-process/) classification and of Bayesian [logistic regression](/logistic-regression/), and it is the inner step of [INLA](/integrated-nested-laplace-approximation/), which applies it to latent Gaussian models with a sparse precision matrix. The [Bernstein-von Mises theorem](/bernstein-von-mises-theorem/) says that the normal law of this page is the limit of the posterior itself, with the [Fisher information](/fisher-information-matrix/) in place of $H/n$.

## Variations

- **Tierney-Kadane marginal densities.** For $\theta = (\psi, \lambda)$, the marginal posterior of $\psi$ is approximated by $\pi(\psi \mid x) \propto e^{\ell(\psi, \hat\lambda_\psi)} \det(H_{\lambda\lambda}(\psi))^{-1/2}$, a Laplace approximation of the inner integral at each $\psi$. INLA uses this form.
- **Choice of scale.** The approximation depends on the parameterization, as the beta-binomial table shows. Scales that make the posterior more symmetric, such as logits and logarithms of variances, usually give smaller errors.
- **The likelihood mode instead of the posterior mode.** Expanding $\log f$ at the maximum likelihood estimate and treating the prior as $g$ is the form of the theorem. It has the same $O(1/n)$ order.
- **Higher-order terms.** The next term of the expansion involves the third and fourth derivatives of $\ell$ and $\nabla g$, $\nabla^2 g$ at the mode (de Bruijn, Section 4.4). It reduces the error to $O(n^{-2})$ but needs derivatives that are rarely available.
- **Laplace as a proposal.** Use $N(\hat\theta, H^{-1})$, or a heavier-tailed Student $t$ with the same centre and scale, as the proposal of [importance sampling](/importance-sampling/) or as the second density of [bridge sampling](/bridge-sampling/). The Monte Carlo step then removes the bias.
- **Other deterministic approximations.** [Variational inference](/variational-inference/) chooses the normal law that minimizes a Kullback-Leibler divergence, and [expectation propagation](/expectation-propagation/) matches moments factor by factor. Both look at the whole posterior and not only at the mode.

## Pitfalls

- **A mode on the boundary.** A variance with a mode at $0$, or a probability with all successes, has $\nabla \ell(\hat\theta) \ne 0$ and the theorem fails. Work in the logarithm or logit scale with the Jacobian, where the mode moves into the interior.
- **Forgetting the Jacobian.** After the change $p = 1/(1 + e^{-\theta})$, the density in $\theta$ is $f(x \mid p)\pi(p)\, p(1 - p)$. Without the factor $p(1 - p)$, $\hat Z$ is the integral of a different function.
- **Several modes.** Newton finds one mode. $\hat Z$ then counts only the mass near it, and for two equal and well separated modes it is off by a factor of two. Run the optimizer from several starts, and use a sampling method if the modes do not merge.
- **Large dimension.** The error constant grows with $d$. For $d$ independent copies of the trace example, the log error is exactly $d$ times $0.0199$, so $\hat Z$ is off by a factor $e^{0.0199 d}$, which is $7.3$ for $d = 100$. Hierarchical models with one parameter per group have $d$ close to $n$, and the $O(1/n)$ guarantee does not apply.
- **A Hessian that is not positive definite.** If the Cholesky factorization fails at the final point, the point is a saddle or the posterior is flat in some direction (an unidentified parameter). Do not replace $\det H$ by its absolute value; fix the model or the optimizer.
- **Overflow in the determinant.** $\det H$ grows like $n^d$. Compute $\log\det H$ from the Cholesky factor, as in L10.

## Exercises

1. Show that the Laplace approximation of $\int_0^1 p^{a-1}(1-p)^{b-1} dp$ in the logit scale equals the product of Stirling's approximations of $\Gamma(a)\Gamma(b)/\Gamma(a + b)$, and deduce that its log error lies between $-1/(12(a + b))$ and $1/(12a) + 1/(12b)$.
2. In the probability scale, the same integral with $a, b > 1$ is expanded at $p = (a - 1)/(a + b - 2)$. Compute the limit of $n$ times the log error for $a = 2 + 0.3n$, $b = 2 + 0.7n$, and compare it with the value $-0.686$ in the table.
3. Prove that Newton's method from any start reaches the mode of a quadratic $\ell$ in one step, and that the Laplace approximation of a Gaussian integral is exact.
4. For $x_1, \ldots, x_n$ from Poisson($\lambda$) with prior Gamma($a$, $b$), write the Laplace approximation of $\log Z$ in the scale $\log\lambda$ and compare it with the exact negative binomial evidence for $n = 5$ and $n = 50$.
5. Two independent coordinates each have log error $\varepsilon$. Show that the log error of the joint approximation is $2\varepsilon$, and explain what this says about the error for $d$ parameters.

## References
