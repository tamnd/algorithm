---
tag: 63JY8R
kind: technique
slug: variational-inference
name: Variational inference
aliases:
- variational Bayes
- variational Bayesian inference
- coordinate ascent variational inference
- CAVI
area: machine-learning/probabilistic-inference
level: advanced
summary: "Approximate a posterior p(z | x) by the member of a tractable family Q that maximizes the ELBO, which is the same as to minimize KL(q || p(z | x))."
prereqs: [evidence-lower-bound, bayesian-inference, exponential-family-distribution]
see_also: [mean-field-approximation, black-box-variational-inference, stochastic-variational-inference, expectation-propagation, expectation-maximization, variational-autoencoder, coordinate-descent, gibbs-sampling]
sources:
  - paper: doi:10.1023/A:1007665907178
    title: "Michael I. Jordan, Zoubin Ghahramani, Tommi S. Jaakkola and Lawrence K. Saul, An introduction to variational methods for graphical models, Machine Learning 37(2), 1999"
    locator: "the block approach to variational methods (the lower bound from Jensen's inequality, the KL divergence to the posterior, and mean field for Boltzmann machines)"
  - paper: doi:10.1080/01621459.2017.1285773
    title: "David M. Blei, Alp Kucukelbir and Jon D. McAuliffe, Variational inference: a review for statisticians, Journal of the American Statistical Association 112(518), 2017"
    locator: "Section 2 (the ELBO, the mean-field family and coordinate ascent variational inference, Algorithm 1), Section 3 (a Bayesian mixture of Gaussians) and Section 5 (open problems, including the underestimated variance)"
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: "Section 10.1 (10.1.1 factorized distributions and the optimal factor, 10.1.2 the two-dimensional Gaussian example, 10.1.3 the univariate Gaussian with unknown mean and precision) and Section 10.2 (the variational mixture of Gaussians)"
  - paper: doi:10.1561/2200000001
    title: "Martin J. Wainwright and Michael I. Jordan, Graphical models, exponential families, and variational inference, Foundations and Trends in Machine Learning 1(1-2), 2008"
    locator: "Chapter 3 (the variational representation of the log partition function) and Chapter 5 (mean field methods)"
---

Variational inference turns the computation of a posterior into an optimization problem. You choose a family $\mathcal{Q}$ of distributions over the hidden variables $z$ that are easy to work with, and you search $\mathcal{Q}$ for the member $q$ that maximizes the [evidence lower bound](/evidence-lower-bound/) (ELBO). Because $\log p(x) = \mathrm{ELBO}(q) + \mathrm{KL}(q \,\|\, p(z \mid x))$, this $q$ is also the member of $\mathcal{Q}$ closest to the posterior in this KL divergence. The basic algorithm is coordinate ascent variational inference (CAVI), which updates one factor of $q$ at a time; [stochastic](/stochastic-variational-inference/) and [black-box](/black-box-variational-inference/) variational inference scale it to large data and to models with no closed form updates.

## In plain words

Exact Bayesian inference asks for a distribution over the unknowns that is often impossible to compute. Sampling methods draw many random guesses from it. Variational inference does something else: it picks a simple shape, for example "each unknown has its own bell curve, and the unknowns do not depend on each other", and it adjusts the settings of that shape until it fits the true answer as well as it can.

The fit is measured by one number that can be computed without knowing the true answer. Raising this number always brings the simple shape closer to the truth. So inference becomes a search for the best settings, and you can use all the tools of optimization. The price is that the answer is only as good as the shape you chose, and the method tends to be too sure of itself.

## When it applies

- The model is a joint distribution $p(x, z)$ that you can evaluate up to a constant, and the query is the posterior $p(z \mid x)$, its moments, or the evidence $p(x)$. In this area $x$ is the data $x_1, \ldots, x_n$ and $z$ holds the latent variables and the parameters that have a prior.
- The exact posterior is intractable: the normalizer $p(x) = \int p(x, z)\, dz$ has no closed form, or a sum over $z$ has exponentially many terms.
- You prefer a fast, deterministic answer to an asymptotically exact one. [Markov chain Monte Carlo](/gibbs-sampling/) is exact in the limit of many samples but can be slow on large data; variational inference is biased but often much faster.
- For the closed form CAVI below, the model should be *conditionally conjugate*: the complete conditional $p(z_j \mid z_{-j}, x)$ of each block is in an [exponential family](/exponential-family-distribution/). Then each optimal factor is in the same family, and the update is a formula. Without this, use gradient methods on the ELBO (the variations below).

## The template

Pick a family. The most common is the *mean-field family* $\mathcal{Q} = \{ q(z) = \prod_{j=1}^m q_j(z_j) \}$, where $z_1, \ldots, z_m$ is a partition of the hidden variables into blocks. The problem is

$$q^* = \arg\max_{q \in \mathcal{Q}} \mathrm{ELBO}(q), \qquad \mathrm{ELBO}(q) = \mathbb{E}_q[\log p(x, z)] - \mathbb{E}_q[\log q(z)].$$

```pseudo id=main
CAVI(p(x, z), the blocks z_1 .. z_m, the initial factors q_1 .. q_m, ε)
L1  repeat
L2      for j ← 1 to m do
L3          q_j(z_j) ← exp(E_{-j}[log p(x, z)]) / normalizer      ▷ E_{-j} averages over q_k for all k ≠ j
L4      L ← ELBO(q_1 · ... · q_m)
L5  until L changed by less than ε
L6  return q_1, ..., q_m
```

**Why line L3 is the best factor.** Fix all factors but $q_j$. Write $\mathbb{E}_{-j}$ for the expectation over $\prod_{k \ne j} q_k$. The ELBO, as a function of $q_j$ alone, is

$$\mathbb{E}_{q_j}\bigl[\mathbb{E}_{-j}[\log p(x, z)]\bigr] - \mathbb{E}_{q_j}[\log q_j] + \text{const} = -\mathrm{KL}(q_j \,\|\, \tilde p_j) + \log C_j + \text{const},$$

where $\tilde p_j(z_j) = \exp(\mathbb{E}_{-j}[\log p(x, z)]) / C_j$ and $C_j$ is its normalizer. The entropies of the other factors are in the constant. The KL divergence is at least 0 and is 0 only at $q_j = \tilde p_j$. So line L3 is the unique maximizer over $q_j$, and no update can lower the ELBO. This is Bishop's equation (10.9) and Algorithm 1 of Blei, Kucukelbir and McAuliffe.

**What is guaranteed.** The sequence of ELBO values does not decrease and is bounded above by $\log p(x)$, so it converges. That is all: CAVI is [coordinate ascent](/coordinate-descent/) on a function that is not concave in $q$ as a whole, so it finds a local optimum, and different starts can give different answers. Each sweep costs one expectation per block, which for conjugate models is a pass over the data: $O(n)$ arithmetic operations per sweep for a model with $n$ data points and a fixed number of global parameters.

**Filling the holes.** The template has three holes: the family (which blocks), the expectations $\mathbb{E}_{-j}[\log p(x, z)]$ (by hand for conjugate models), and the stopping rule. Compute the ELBO at line L4 even if you do not need it: a decrease is a bug.

## Classic examples

**The Gaussian with unknown mean and precision (Bishop 2006, Section 10.1.3).** Data $x_i \sim \mathcal{N}(\mu, \tau^{-1})$, $i = 1, \ldots, n$, with the prior $\tau \sim \mathrm{Gamma}(a_0, b_0)$ (rate $b_0$) and $\mu \mid \tau \sim \mathcal{N}(\mu_0, (\lambda_0 \tau)^{-1})$. Take $q(\mu, \tau) = q(\mu) q(\tau)$. Line L3 gives $q(\mu) = \mathcal{N}(m, l^{-1})$ and $q(\tau) = \mathrm{Gamma}(a, b)$ with

$$m = \frac{\lambda_0 \mu_0 + \sum_i x_i}{\lambda_0 + n}, \quad l = (\lambda_0 + n)\, \mathbb{E}[\tau], \quad a = a_0 + \frac{n + 1}{2}, \quad b = b_0 + \frac12 \mathbb{E}_{\mu}\Bigl[\sum_i (x_i - \mu)^2 + \lambda_0 (\mu - \mu_0)^2\Bigr],$$

with $\mathbb{E}[\tau] = a / b$ and $\mathbb{E}_\mu[(x_i - \mu)^2] = (x_i - m)^2 + 1/l$. Only $l$ and $b$ change from sweep to sweep. Take $x = (1.2, 2.3, 1.8, 2.9, 1.8)$, $\mu_0 = 0$, $\lambda_0 = a_0 = b_0 = 1$, and start from $\mathbb{E}[\tau] = 10$.

| sweep | $m$ | $l$ | $a$ | $b$ | $\mathbb{E}[\tau]$ | ELBO |
|---|---|---|---|---|---|---|
| 1 | 1.6667 | 60.0000 | 4 | 3.5267 | 1.13422 | $-9.39152$ |
| 2 | 1.6667 | 6.8053 | 4 | 3.9175 | 1.02106 | $-8.72360$ |
| 3 | 1.6667 | 6.1264 | 4 | 3.9664 | 1.00848 | $-8.72062$ |
| 4 | 1.6667 | 6.0509 | 4 | 3.9725 | 1.00693 | $-8.72058$ |
| 5 | 1.6667 | 6.0416 | 4 | 3.9732 | 1.00674 | $-8.72058$ |

The fixed point has a closed form. Put $l = (\lambda_0 + n) \mathbb{E}[\tau]$ into $b$: then $b = C + 1/(2 \mathbb{E}[\tau])$ with $C = b_0 + \frac12 \bigl[\sum_i (x_i - m)^2 + \lambda_0 (m - \mu_0)^2\bigr]$, and $\mathbb{E}[\tau] = a/b$ gives $\mathbb{E}[\tau] = (a - \frac12)/C = (a_0 + n/2)/C$. Some algebra shows that $C$ equals $b_n$, the rate of the exact Normal-Gamma posterior. So at the fixed point:

- the mean of $q(\mu)$ is the exact posterior mean of $\mu$, here $10/6 \approx 1.6667$;
- $\mathbb{E}_q[\tau]$ is the exact posterior mean of $\tau$, $a_n / b_n = 3.5 / 3.47667 \approx 1.00671$;
- the variance of $q(\mu)$ is $b_n / ((\lambda_0 + n) a_n) \approx 0.1656$, while the exact marginal variance of $\mu$ (a Student t) is $b_n / ((\lambda_0 + n)(a_n - 1)) \approx 0.2318$. The factor $q$ is too narrow by the ratio $(a_n - 1)/a_n = 5/7$.

The map from one $\mathbb{E}[\tau]$ to the next has derivative $1/(2a) = 1/8$ at the fixed point, so the error shrinks by about 8 per sweep, as the table shows. The final ELBO is $-8.72058$, and the exact $\log p(x)$ is $-8.65086$; the gap $0.0697$ is the KL divergence from $q$ to the posterior.

**A correlated Gaussian (Bishop 2006, Section 10.1.2).** For the target $\mathcal{N}(\mu, \Lambda^{-1})$ in two dimensions and $q = q_1(z_1) q_2(z_2)$, line L3 gives $q_j = \mathcal{N}(m_j, \Lambda_{jj}^{-1})$ with $m_1 = \mu_1 - \Lambda_{11}^{-1} \Lambda_{12}(m_2 - \mu_2)$, and the same for $m_2$. The means converge to $\mu$, but the variances are $1/\Lambda_{jj}$, the conditional variances, which are smaller than the marginal variances $(\Lambda^{-1})_{jj}$. With $\Lambda_{11} = \Lambda_{22} = 1$ and $\Lambda_{12} = 0.9$, $q$ has variance 1 per coordinate and the true marginals have variance $1/0.19 \approx 5.26$.

**Other members of the family.**

- The [mean-field approximation](/mean-field-approximation/) for an Ising model is CAVI with one binary factor per spin, and the ELBO is a lower bound on the log [partition function](/partition-function/).
- [Expectation-maximization](/expectation-maximization/) is the case where $\mathcal{Q}$ holds every distribution, so line L3 returns the exact posterior and the bound is tight; the parameters are then updated by maximization.
- The variational mixture of Gaussians (Bishop 2006, Section 10.2) and [latent Dirichlet allocation](/latent-dirichlet-allocation/) are conditionally conjugate models with local latent variables per data point and global parameters; [stochastic variational inference](/stochastic-variational-inference/) runs the same updates on minibatches.
- The [variational autoencoder](/variational-autoencoder/) uses a neural network that outputs the parameters of $q(z \mid x)$ for each data point (amortized inference) and trains it by gradient ascent on the ELBO.

## Variations

- **Structured families.** Keep some dependencies inside $q$, for example a chain or a tree over the blocks. The update of line L3 still applies block by block, and the bound is tighter.
- **Gradient-based VI.** Parametrize $q_\lambda$ and follow $\nabla_\lambda \mathrm{ELBO}$ with [stochastic gradient descent](/stochastic-gradient-descent/). The score function estimator gives [black-box variational inference](/black-box-variational-inference/); the reparameterization estimator gives the training of the variational autoencoder.
- **Natural gradients.** For conditionally conjugate models, the natural gradient of the ELBO in the natural parameters of a global factor is (the line L3 parameter) minus (the current parameter). [Stochastic variational inference](/stochastic-variational-inference/) follows a noisy version of it.
- **Other divergences.** [Expectation propagation](/expectation-propagation/) matches moments, which minimizes $\mathrm{KL}(p \,\|\, q)$ locally; it does not maximize an ELBO. [Loopy belief propagation](/loopy-belief-propagation/) finds stationary points of the [Bethe free energy](/bethe-free-energy/), which is also a variational problem, but over local marginals and with an approximate entropy, so it gives no bound.
- **Variational EM.** When the model has parameters $\theta$ without a prior, alternate CAVI over $q$ with a maximization of the ELBO over $\theta$.

## Pitfalls

- **Too small a variance.** Minimizing $\mathrm{KL}(q \,\|\, p)$ punishes mass of $q$ where $p$ is small and does not punish the opposite. Mean-field $q$ therefore tends to underestimate posterior variances, as in both examples above. Do not read a mean-field credible interval as a calibrated one.
- **Mode seeking.** On a posterior with several modes, $q$ usually locks onto one mode. In a mixture model the modes that differ only by a permutation of the labels are equivalent, so this is harmless there, but in general it hides real uncertainty.
- **Local optima.** CAVI is coordinate ascent on a non-concave objective. Run it from several starts and keep the run with the largest ELBO.
- **Parallel updates.** Line L3 must use the newest factors. If all factors are updated at the same time from the old ones, the ELBO can go down and the iteration can oscillate.
- **Comparing models by the ELBO.** The ELBO is a lower bound with a gap that depends on the model. A larger ELBO does not prove a larger evidence.
- **Support.** If $q$ puts mass where $p(x, z) = 0$, the ELBO is $-\infty$. Choose a family with the right support, for example a Gamma rather than a Gaussian for a precision.

## Exercises

1. Derive the update of $q(\tau)$ in the first example from line L3, and show that the shape $a = a_0 + (n + 1)/2$ is one half larger than the shape of the exact posterior.
2. In the two-dimensional Gaussian example, show that the fixed point is $m = \mu$ for any start and that the error in $m_1$ shrinks by the factor $\Lambda_{12}^2 / (\Lambda_{11} \Lambda_{22})$ per sweep.
3. Show that the derivative of the map $\mathbb{E}[\tau] \mapsto a / (C + 1/(2 \mathbb{E}[\tau]))$ at its fixed point is $1/(2a)$.

## References
