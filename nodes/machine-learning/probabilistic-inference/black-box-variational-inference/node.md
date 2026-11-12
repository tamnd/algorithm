---
tag: 3YYRHH
kind: algorithm
slug: black-box-variational-inference
name: Black-box variational inference
aliases:
- BBVI
- score function variational inference
- black box VI
area: machine-learning/probabilistic-inference
level: research
summary: "Stochastic gradient ascent on the ELBO with Monte Carlo score function gradients, made usable by Rao-Blackwellization and control variates. It needs only samples from q and values of log p."
solves: [marginal-inference, partition-function-computation]
model: real-ram
complexity:
  vars: {T: the number of iterations, S: the number of samples per iteration, n: the number of factors of q, c: the cost to evaluate the Markov blanket terms of one variable}
  time: {worst: "O(T S n c)"}
  space: {extra: "O(S n)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2014
  people: [Rajesh Ranganath, Sean Gerrish, David M. Blei]
  note: "Ranganath, Gerrish and Blei (AISTATS 2014) made variational inference usable without model-specific derivations, by score function gradients with Rao-Blackwellization and control variates. The reparameterization gradient of Kingma and Welling appeared the same year."
prereqs: [variational-inference, evidence-lower-bound, stochastic-gradient-descent]
see_also: [variational-autoencoder, stochastic-variational-inference, reinforce, adagrad, monte-carlo-integration, mean-field-approximation, wake-sleep-algorithm, importance-sampling]
sources:
  - paper: "Rajesh Ranganath, Sean Gerrish and David M. Blei, Black box variational inference, Proceedings of the 17th International Conference on Artificial Intelligence and Statistics (AISTATS), PMLR 33, 2014"
    title: Ranganath, Gerrish and Blei 2014
    locator: "the score function gradient of the ELBO, Rao-Blackwellization with the Markov blanket of each variable, control variates with the score as the control, and AdaGrad step sizes"
  - paper: "Diederik P. Kingma and Max Welling, Auto-encoding variational Bayes, International Conference on Learning Representations (ICLR), 2014"
    title: Kingma and Welling 2014
    locator: "the reparameterization trick and the stochastic gradient variational Bayes estimator"
  - paper: "John Paisley, David M. Blei and Michael I. Jordan, Variational Bayesian inference with stochastic search, Proceedings of the 29th International Conference on Machine Learning (ICML), 2012"
    title: Paisley, Blei and Jordan 2012
    locator: "score function gradients of the variational objective with control variates"
  - paper: "Ronald J. Williams, Simple statistical gradient-following algorithms for connectionist reinforcement learning, Machine Learning 8, 1992"
    title: Williams 1992
    locator: the REINFORCE (score function) gradient estimator
---

Black-box variational inference (BBVI) fits a [variational](/variational-inference/) distribution $q(z; \lambda)$ to a posterior by stochastic gradient ascent on the [evidence lower bound](/evidence-lower-bound/), with gradients estimated from samples of $q$. The estimator uses the score function identity $\nabla_\lambda \mathcal{L} = \mathbb{E}_q[\nabla_\lambda \log q(z; \lambda)\, (\log p(x, z) - \log q(z; \lambda))]$, which needs only the ability to sample from $q$, evaluate $\log q$ and its gradient, and evaluate $\log p(x, z)$. No derivation for the model is needed, and $z$ can be discrete. The raw estimator has a large variance. Ranganath, Gerrish and Blei made it usable with two variance reductions: Rao-Blackwellization, which keeps only the terms of the Markov blanket of each variable, and control variates, which subtract a multiple of the score. For differentiable models, the reparameterization gradient of Kingma and Welling usually has a much smaller variance.

## In plain words

Variational inference replaces a hard distribution by the best member of a simple family. Finding the best member normally needs a long derivation for each new model.

Black-box variational inference skips the derivation. It draws random guesses from the current simple distribution and checks how well each guess fits the model and the data. It then moves the simple distribution toward the guesses that fit better than it expected. Because the guesses are random, each step is noisy, so the method uses two tricks to calm the noise: each variable only looks at the parts of the model that touch it, and a known zero-average quantity is subtracted to cancel part of the noise. Many small noisy steps then reach a good answer.

## The problem

**The objective.** For a model $p(x, z)$ with observed $x$ and latent $z$, and a family $q(z; \lambda)$, maximize the ELBO

$$\mathcal{L}(\lambda) = \mathbb{E}_{q(z; \lambda)}[\log p(x, z) - \log q(z; \lambda)] = \log p(x) - \mathrm{KL}(q \,\|\, p(\cdot \mid x)).$$

The expected value has no closed form for most models outside the conditionally conjugate exponential family, so coordinate ascent updates are not available.

**The access model.** The algorithm may sample $z \sim q(z; \lambda)$, evaluate $\log q$ and $\nabla_\lambda \log q$, and evaluate $\log p(x, z)$ at a point. It may not differentiate $\log p$ or compute any expected value under $q$ in closed form.

**The family.** Mean field, $q(z; \lambda) = \prod_i q_i(z_i; \lambda_i)$. The implementation uses $q_i = \mathcal{N}(\mu_i, \sigma_i^2)$ with $\lambda_i = (\mu_i, \omega_i)$ and $\sigma_i = e^{\omega_i}$, whose score is $\partial_{\mu_i} \log q_i = (z_i - \mu_i)/\sigma_i^2$ and $\partial_{\omega_i} \log q_i = (z_i - \mu_i)^2/\sigma_i^2 - 1$.

## The algorithm

Let $\log p_i(x, z)$ be the terms of $\log p(x, z)$ that depend on $z_i$: the factors of its Markov blanket. For a sample $z^{(s)}$, factor $i$ gets the summand and the control

$$f_i^{(s)} = \nabla_{\lambda_i} \log q_i(z_i^{(s)})\, \big(\log p_i(x, z^{(s)}) - \log q_i(z_i^{(s)})\big), \qquad h_i^{(s)} = \nabla_{\lambda_i} \log q_i(z_i^{(s)}).$$

The control has expected value zero, so subtracting $a_i h_i$ changes only the variance. The coefficient that minimizes the variance, summed over the $D$ components of $\lambda_i$, is $a_i = \sum_{d} \mathrm{Cov}(f_{i,d}, h_{i,d}) / \sum_{d} \mathrm{Var}(h_{i,d})$, estimated from the samples.

```pseudo id=main
BBVI(log p, q, S, η, T)
L1  λ ← initial value; G ← 0
L2  for t ← 1 to T do
L3      draw z^(1), …, z^(S) from q(z; λ)
L4      for each factor i and sample s: f_i^(s) ← ∇ log q_i(z_i^(s)) (log p_i(x, z^(s)) − log q_i(z_i^(s))); h_i^(s) ← ∇ log q_i(z_i^(s))
L5      a_i ← Σ_d Cov(f_id, h_id) / Σ_d Var(h_id), estimated from the samples
L6      ĝ_i ← (1/S) Σ_s (f_i^(s) − a_i h_i^(s))
L7      G ← G + ĝ²; λ ← λ + η ĝ / √G   (AdaGrad, per coordinate)
L8  return λ
```

The implementation computes $a_i$ for sample $s$ from the other $S - 1$ samples, which keeps the estimate exactly unbiased; the paper uses all $S$ samples, which adds a bias of order $1/S$.

**The reparameterization estimator.** If $z = \mu + \sigma \odot \varepsilon$ with $\varepsilon \sim \mathcal{N}(0, I)$ and $\log p$ is differentiable in $z$, then $\nabla_\mu \mathcal{L} = \mathbb{E}[\nabla_z \log p(x, z)]$ and $\partial_{\omega_i} \mathcal{L} = \mathbb{E}[(\nabla_z \log p)_i\, \sigma_i \varepsilon_i] + 1$, the $1$ being the exact derivative of the entropy. This uses the gradient of the model, which the score estimator does not. It is the estimator of the [variational autoencoder](/variational-autoencoder/).

## Example

Take a Gaussian target $\log p(x, z) = -\tfrac12 z^\top \Lambda z + \eta^\top z + \text{const}$ with

$$\Lambda = \begin{pmatrix} 2 & 0.8 \\ 0.8 & 1 \end{pmatrix}, \qquad \eta = (1, -1).$$

For the mean-field Gaussian family the ELBO and its gradient are known exactly: $\nabla_\mu \mathcal{L} = \eta - \Lambda \mu$ and $\partial_{\omega_i} \mathcal{L} = 1 - \Lambda_{ii} \sigma_i^2$. The optimum is $\mu^\ast = \Lambda^{-1} \eta = (1.3235, -2.0588)$ and $\sigma_i^{\ast 2} = 1/\Lambda_{ii} = (0.5, 1)$, smaller than the true marginal variances $(0.735, 1.471)$, as is usual for mean field.

**The estimators.** At $\mu = (3, 3)$, $\omega = (0, 0)$, the exact gradient is $(\partial_{\mu_1}, \partial_{\omega_1}, \partial_{\mu_2}, \partial_{\omega_2}) = (-7.4, -1.0, -6.4, 0)$. Each estimator was drawn 2000 times with $S = 10$ (seeded). All four have means within sampling error of the exact gradient. The sum of the variances of the four components:

| estimator | total variance |
|---|---|
| score function, plain | 388.4 |
| with Rao-Blackwellization | 254.5 |
| with Rao-Blackwellization and control variate | 175.0 |
| reparameterization | 11.1 |

**A run.** BBVI with $S = 10$, AdaGrad with $\eta = 0.5$, and 2000 iterations from $\mu = 0$, $\omega = 0$ ends at $\mu = (1.358, -2.101)$ and $\sigma^2 = (0.464, 0.956)$. The ELBO goes from $1.338$ to $3.180$; the optimum is $3.182$.

## Correctness

- **The score function identity.** Since $\mathbb{E}_q[\nabla_\lambda \log q] = 0$, the derivative of the $-\log q$ inside the expected value vanishes, and $\nabla_\lambda \mathcal{L} = \mathbb{E}_q[\nabla_\lambda \log q\, (\log p - \log q)]$. The sample average is unbiased.
- **Rao-Blackwellization.** Under mean field, $z_i$ is independent of the other variables, so the terms of $\log p - \log q$ that do not depend on $z_i$ contribute zero to the gradient for $\lambda_i$, and they can be dropped.
- **Control variates.** Subtracting $a\, \nabla \log q_i$ changes nothing in expected value if $a$ is independent of the sample it multiplies.
- **The optimization.** With unbiased estimates of finite variance and step sizes that meet the [Robbins-Monro conditions](/robbins-monro-conditions/), stochastic gradient ascent converges to a local optimum of the ELBO under the usual conditions of stochastic approximation. The ELBO is not concave in general, so the optimum need not be global.

The proofs of the first three points and of the reparameterization formula are in the correctness proof.

## Complexity

The costs are in the [real RAM](/real-ram/) model.

- **One iteration.** $S$ samples of $n$ variables, and for each sample and each factor one evaluation of the Markov blanket terms: $O(S n c)$. Without Rao-Blackwellization, each sample needs one evaluation of the whole $\log p$.
- **Iterations.** Not bounded; the noise of the gradient sets the step size and the number of steps. More samples per step lower the noise by a factor $S$.
- **Memory.** $O(S n)$ for the samples and $O(n)$ for $\lambda$ and the AdaGrad sums.

## Properties

- **Black box.** Only sampling from $q$, $\log q$, its score, and $\log p$ at points. Works for discrete latent variables and models that are not differentiable.
- **Unbiased, high variance.** The plain score function estimator is often too noisy to use; the variance reductions are part of the method.
- **Local optimum.** Like all ELBO methods, it finds a local optimum, and with a mean-field $q$ it underestimates posterior variances.
- **Random.** Results depend on the random samples; the ELBO is only estimated during the run.

## Variants and improvements

- **Reparameterization gradients.** For continuous $z$ and differentiable $\log p$, the estimator of Kingma and Welling has a much smaller variance and is the basis of the variational autoencoder and of automatic differentiation variational inference.
- **Other step sizes.** AdaGrad was used in the paper; RMSProp and Adam are common now.
- **Better control variates.** Learned baselines, as in [REINFORCE](/reinforce/) for reinforcement learning, and combinations of score and reparameterization terms.
- **Stochastic minibatches.** When $\log p$ is a sum over many data points, a minibatch estimate of it adds another level of noise but keeps the estimate unbiased, as in [stochastic variational inference](/stochastic-variational-inference/).
- **Richer families.** Any family that can be sampled and whose $\log q$ and score can be evaluated, including structured and mixture families.

## When to use it

Use BBVI for a model where the coordinate ascent updates of [mean field](/mean-field-approximation/) have no closed form and where the reparameterization gradient is not available, for example with discrete latent variables or a log density that cannot be differentiated. When $z$ is continuous and $\log p$ is differentiable, use the reparameterization gradient instead. For conditionally conjugate models, closed-form coordinate updates or stochastic variational inference converge much faster.

## Pitfalls

- **No variance reduction.** The plain score function estimator often makes progress too slow to be useful.
- **Too few samples for the control variate.** The coefficient $a_i$ is estimated, and with few samples the estimate is noisy. At $\mu = 0$, $\omega = 0$ in the example, with $S = 10$, the control variate raised the total variance from 5.6 to 7.6.
- **Variances collapse or blow up.** Parameterize scales by their logarithm, as here, so that a step cannot make them negative.
- **Reading the ELBO from one sample.** The estimated ELBO is noisy; average over many samples or iterations before judging convergence.
- **Score of the full joint without Rao-Blackwellization.** In a large model, all the terms that do not touch $z_i$ add noise to its gradient.

## Implementations

## History

Score function gradients go back to the likelihood ratio method of stochastic simulation and to Williams's REINFORCE (1992) in reinforcement learning. Paisley, Blei and Jordan (2012) used them for variational inference with control variates. Ranganath, Gerrish and Blei (2014) combined the score function gradient with Rao-Blackwellization over the Markov blanket, control variates and AdaGrad steps into a method that applies to any model that can be evaluated, and called it black box variational inference. In the same year, Kingma and Welling, and independently Rezende, Mohamed and Wierstra, introduced the reparameterization gradient, which led to the variational autoencoder.

## References
