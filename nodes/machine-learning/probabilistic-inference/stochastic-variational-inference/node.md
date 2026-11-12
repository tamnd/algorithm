---
tag: MB3DWW
kind: algorithm
slug: stochastic-variational-inference
name: Stochastic variational inference
aliases:
- SVI
area: machine-learning/probabilistic-inference
level: research
summary: "Variational inference for large data sets: optimize local factors on a minibatch, then take a natural gradient step on the global factors with Robbins-Monro step sizes."
solves: [marginal-inference, partition-function-computation]
model: real-ram
complexity:
  vars: {T: the number of iterations, b: the minibatch size, c: the cost of the local step for one data point, g: the number of global variational parameters}
  time: {worst: "O(T (b c + g))"}
  space: {extra: "O(g + b c)"}
properties: {deterministic: false, exact: false, online: true, recursive: false}
history:
  year: 2013
  people: [Matthew D. Hoffman, David M. Blei, Chong Wang, John Paisley]
  note: "Hoffman, Blei, Wang and Paisley (JMLR 2013) showed that for conditionally conjugate models the natural gradient of the ELBO in the global parameters is a simple difference, and turned coordinate ascent into a stochastic method that sees one minibatch at a time."
prereqs: [variational-inference, natural-gradient-descent, robbins-monro-conditions, exponential-family-distribution]
see_also: [black-box-variational-inference, stochastic-gradient-descent, latent-dirichlet-allocation, gaussian-mixture-model, mean-field-approximation, evidence-lower-bound, fisher-information-matrix, variational-autoencoder]
sources:
  - paper: "Matthew D. Hoffman, David M. Blei, Chong Wang and John Paisley, Stochastic variational inference, Journal of Machine Learning Research 14, 2013"
    title: Hoffman, Blei, Wang and Paisley 2013
    locator: "conditionally conjugate models with global and local variables, the natural gradient of the ELBO as the intermediate parameter minus the current one, the minibatch algorithm, and the step size schedule (t + tau)^(-kappa)"
  - paper: "Shun-ichi Amari, Natural gradient works efficiently in learning, Neural Computation 10(2), 1998"
    title: Amari 1998
    locator: the natural gradient under the Fisher information metric
  - paper: "Herbert Robbins and Sutton Monro, A stochastic approximation method, Annals of Mathematical Statistics 22(3), 1951"
    title: Robbins and Monro 1951
    locator: stochastic approximation with step sizes whose sum diverges and whose sum of squares converges
  - paper: "Masa-aki Sato, Online model selection based on the variational Bayes, Neural Computation 13(7), 2001"
    title: Sato 2001
    locator: an online variational Bayes method for exponential family models that is an early form of the same update
  - paper: "Matthew D. Hoffman, David M. Blei and Francis Bach, Online learning for latent Dirichlet allocation, Advances in Neural Information Processing Systems 23, 2010"
    title: Hoffman, Blei and Bach 2010
    locator: the online variational Bayes algorithm for latent Dirichlet allocation that SVI generalizes
---

Stochastic variational inference (SVI) scales [variational inference](/variational-inference/) to data sets too large for one pass per update. It applies to conditionally conjugate models with *global* variables $\beta$, shared by all data, and *local* variables $z_n$, one per data point. Each iteration samples a minibatch, fits the local factors of its points given the current global factors, forms an *intermediate* global parameter $\hat\lambda$ as if the minibatch were the whole data set repeated, and moves the global parameter part of the way toward it: $\lambda \leftarrow (1 - \rho_t)\lambda + \rho_t \hat\lambda$. Hoffman, Blei, Wang and Paisley showed that $\hat\lambda - \lambda$ is an unbiased estimate of the [natural gradient](/natural-gradient-descent/) of the ELBO, so with step sizes that meet the [Robbins-Monro conditions](/robbins-monro-conditions/), SVI is stochastic natural gradient ascent and reaches a local optimum, the same kind of point as batch coordinate ascent.

## In plain words

Some models describe millions of documents or images. Classic variational inference must look at every data point before it can improve its overall picture even once, which is too slow.

SVI looks at a small random handful of data points at a time. For each of them it works out the details, such as which topic a word belongs to, using the current overall picture. It then asks: if the whole data set looked like this handful, what would the overall picture be? It moves the current picture a small step toward that answer. The steps get smaller over time, so the random errors of each handful average out. After many steps the picture is the same as the one the slow method would find, but at a small fraction of the cost.

## The problem

**The model.** Global variables $\beta$, and for each $n = 1, \ldots, N$ a local variable $z_n$ and an observation $x_n$, with $p(\beta, z, x) = p(\beta) \prod_n p(z_n, x_n \mid \beta)$. The model is *conditionally conjugate*: the complete conditional of $\beta$ is in an [exponential family](/exponential-family-distribution/) with natural parameter

$$\eta_g(x, z) = \alpha + \sum_{n=1}^N t(x_n, z_n),$$

and each complete conditional of $z_n$ is in an exponential family as well. Mixture models, [latent Dirichlet allocation](/latent-dirichlet-allocation/) and hidden Markov models are of this kind.

**The family.** Mean field, $q(\beta; \lambda) \prod_n q(z_n; \phi_n)$, with $q(\beta; \lambda)$ in the same exponential family as the complete conditional. Coordinate ascent (CAVI) alternates $\phi_n \leftarrow$ the optimum given $\lambda$, for all $n$, and $\lambda \leftarrow \hat\lambda = \alpha + \sum_n \mathbb{E}_{\phi_n}[t(x_n, z_n)]$. Each global update needs a pass over all $N$ points.

**The example model.** A one-dimensional Gaussian mixture with $K$ components of unit variance and equal weights, means $\mu_k \sim \mathcal{N}(0, s_0^2)$, and $q(\mu_k) = \mathcal{N}(m_k, v_k)$ with natural parameters $\lambda_k = (m_k / v_k, 1 / v_k)$. The local step is $\phi_{nk} \propto \exp(m_k x_n - \tfrac12(m_k^2 + v_k))$, and $\hat\lambda_k = (\sum_n \phi_{nk} x_n,\ 1/s_0^2 + \sum_n \phi_{nk})$.

## The algorithm

```pseudo id=main
SVI(x_1..x_N, α, b, τ, κ, T)
L1  λ ← an initial value
L2  for t ← 1 to T do
L3      sample a minibatch B of b indices, uniformly
L4      for each n in B: φ_n ← the optimal local factor given λ and x_n
L5      λ̂ ← α + (N / b) Σ_{n ∈ B} E_{φ_n}[t(x_n, z_n)]
L6      ρ_t ← (t + τ)^(−κ)
L7      λ ← (1 − ρ_t) λ + ρ_t λ̂
L8  return λ
```

The step sizes $\rho_t = (t + \tau)^{-\kappa}$ with $\tau \ge 0$ and $\kappa \in (0.5, 1]$ satisfy $\sum_t \rho_t = \infty$ and $\sum_t \rho_t^2 < \infty$. The local factors are not stored; each one is computed again whenever its point is sampled.

**Why it is a natural gradient step.** With the local factors fixed, the gradient of the ELBO in $\lambda$ is $\nabla^2 a_g(\lambda)\,(\hat\lambda - \lambda)$, where $a_g$ is the log normalizer of $q(\beta; \lambda)$. The matrix $\nabla^2 a_g(\lambda)$ is the [Fisher information](/fisher-information-matrix/) of $q$, so the natural gradient, the gradient multiplied by the inverse Fisher information, is just $\hat\lambda - \lambda$. The minibatch version of $\hat\lambda$ is unbiased, because each point appears with probability $b/N$ and is scaled by $N/b$.

## Example

Draw $N = 500$ points: each picks one of the centers $-4$, $0$, $3$ at random and adds standard normal noise (seed 1). Fit $K = 3$ components with $s_0 = 10$, starting from the means $-1, 0, 1$ with variance $1$.

**Batch CAVI** converges in 50 sweeps (largest change below $10^{-12}$), each sweep a pass over all 500 points. The fixed point has means $(-3.8483, 0.1549, 3.0676)$ and variances $(0.00668, 0.00578, 0.00564)$.

**SVI** with minibatches of $b = 50$, $\tau = 1$ and $\kappa = 0.9$ (seed 3) gives these largest errors of the means against the CAVI fixed point:

| iterations | points visited | largest error of a mean |
|---|---|---|
| 100 | 5000 (10 passes) | 0.0399 |
| 1000 | 50000 | 0.0079 |
| 10000 | 500000 | 0.0028 |

After 10000 iterations the variances match those of CAVI to $2 \times 10^{-4}$. On this small data set, batch CAVI is faster; SVI wins when $N$ is so large that one pass is expensive and a few passes already give a good answer.

## Correctness

- **The natural gradient.** For a conditionally conjugate model with fixed local factors, the natural gradient of the ELBO in the global parameters is $\hat\lambda - \lambda$. With $\rho = 1$ and the full data, the SVI step is the CAVI step.
- **Unbiased minibatches.** With the local factors at their optimum given $\lambda$, which depends only on $\lambda$ and the point, the minibatch $\hat\lambda$ has expected value equal to the full-data $\hat\lambda$.
- **Fixed points.** The expected step is zero exactly at the fixed points of CAVI.
- **Convergence.** With Robbins-Monro step sizes, the theory of stochastic approximation gives convergence to a local optimum of the ELBO under regularity conditions (Hoffman et al. rely on it; it is not proved here).

The proofs of the first three points are in the correctness proof.

## Complexity

The costs are in the [real RAM](/real-ram/) model.

- **One iteration.** $b$ local steps of cost $c$ each and an update of the $g$ global parameters: $O(b c + g)$. For the mixture, $c = O(K)$ and $g = 2K$.
- **Iterations.** Not bounded. The error falls roughly like the step size, so the schedule sets the speed.
- **Memory.** $O(g)$ for the global parameters and $O(b c)$ for the local factors of one minibatch. The local factors of the whole data set are never stored, which also makes SVI usable on a data stream.

## Properties

- **Per-iteration cost independent of $N$.** Only the minibatch is touched.
- **Unbiased natural gradient steps.** Natural gradients follow the geometry of the family and need no step size tuning per coordinate.
- **Same fixed points as CAVI.** Including the same local optima, so the start still matters.
- **Random.** The result depends on the minibatches; with decreasing steps the noise dies out.
- **Online.** Works on a stream of data points, with $N$ as the assumed size of the population.

## Variants and improvements

- **Online LDA.** The first instance, for latent Dirichlet allocation (Hoffman, Blei and Bach 2010).
- **Adaptive step sizes.** Learning rates set from estimates of the gradient noise instead of a fixed schedule.
- **Nonconjugate models.** When $\hat\lambda$ has no closed form, [black-box variational inference](/black-box-variational-inference/) or reparameterization gradients replace the closed-form natural gradient, with the same minibatch scaling.
- **Structured SVI.** Keeps some dependence between global and local variables in $q$ for a better approximation.
- **Amortized inference.** The [variational autoencoder](/variational-autoencoder/) replaces the per-point local step by a network that predicts $\phi_n$ from $x_n$.

## When to use it

Use SVI for a conditionally conjugate model with so much data that one full pass per global update is too slow, such as topic models on millions of documents. Use batch CAVI on small data sets, where it converges in fewer passes. For a model without closed-form complete conditionals, use a stochastic gradient method on the ELBO such as BBVI.

## Pitfalls

- **Forgetting the $N/b$ scaling.** Without it, the minibatch acts as the whole data set, and the posterior is far too wide.
- **Step sizes.** A constant $\rho$ never removes the noise; $\kappa \le 0.5$ breaks the Robbins-Monro conditions; a very small $\tau$ makes the first steps forget the start at once, which can lock in a bad local optimum.
- **Local steps not converged.** For models such as LDA, the local step is itself iterative. If it stops too early, the estimate is biased.
- **Local optima.** SVI inherits them from the ELBO. Try several starts.
- **Minibatch size.** Very small minibatches make each step very noisy. In the example, $b = 50$ converged much faster than $b = 10$ for the same number of iterations.

## Implementations

## History

Sato (2001) gave an online variational Bayes method for exponential family models with a similar update. Hoffman, Blei and Bach (2010) built online variational Bayes for latent Dirichlet allocation and fit topic models to millions of documents. Hoffman, Blei, Wang and Paisley (2013) gave the general form: for any conditionally conjugate model with global and local variables, the natural gradient of the ELBO in the global parameters is the intermediate parameter minus the current one, and minibatch estimates of it, with Robbins-Monro step sizes, give stochastic variational inference.

## References
