---
tag: K0GFYT
kind: algorithm
slug: diffusion-posterior-sampling
name: Diffusion posterior sampling
aliases:
- DPS
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: research
summary: Sample from the posterior of an inverse problem by guiding each reverse step of a trained diffusion model with an approximate likelihood gradient.
model: real-ram
complexity:
  vars: {N: the number of reverse steps, a: the cost of one call to A plus one call to its adjoint, g: the cost of one call to the score network plus one vector-Jacobian product through it (outside this page), n: the signal length, m: the number of data values}
  time: {worst: O(N (a + g))}
  space: {extra: O(n + m)}
properties: {deterministic: false, iterative: true, learned: true, matrix_free: true, exact: false}
history:
  year: 2023
  people: [Hyungjin Chung, Jeongsol Kim, Michael T. McCann, Marc L. Klasky, Jong Chul Ye]
  note: "Chung and coauthors replaced the intractable likelihood of a noisy diffusion state by the likelihood of its Tweedie denoised estimate, which gave a guidance step for general and nonlinear forward models with Gaussian or Poisson noise."
prereqs: [bayesian-inverse-problem, conditional-expectation, backpropagation]
see_also: [compressed-sensing-generative-models, plug-and-play-priors, langevin-dynamics, jensens-inequality, image-inpainting, super-resolution, phase-retrieval, linear-gaussian-inverse-problem]
sources:
  - paper: arxiv:2209.14687
    title: "Hyungjin Chung, Jeongsol Kim, Michael T. McCann, Marc L. Klasky and Jong Chul Ye, Diffusion posterior sampling for general noisy inverse problems, International Conference on Learning Representations (ICLR), 2023"
    locator: "Algorithm 1 (the sampler for Gaussian noise), Proposition 1 (Tweedie's formula for the denoised estimate), Theorem 1 (the bound on the Jensen gap), and the experiments on FFHQ and ImageNet"
  - paper: arxiv:2006.11239
    title: "Jonathan Ho, Ajay Jain and Pieter Abbeel, Denoising diffusion probabilistic models, Advances in Neural Information Processing Systems 33, 2020"
    locator: "the forward process, the posterior q(x_{t-1} | x_t, x_0) of the reverse step, and the sampling algorithm"
  - paper: doi:10.1198/jasa.2011.tm11181
    title: "Bradley Efron, Tweedie's formula and selection bias, Journal of the American Statistical Association 106(496), 2011"
    locator: Tweedie's formula for the posterior mean under Gaussian noise
---

Diffusion posterior sampling (DPS) draws approximate samples from the posterior $p(x \mid y)$ of an inverse problem $y = A(x) + n$, using a diffusion model trained only on clean signals. A diffusion model generates a signal by starting from noise and running $N$ reverse steps, each guided by a learned score $s(x, t) \approx \nabla\log p_t(x)$. DPS adds to each reverse step a gradient step on $\|y - A(\hat x_0)\|^2$, where $\hat x_0$ is the denoised estimate of the current state by [Tweedie's formula](/conditional-expectation/). Chung, Kim, McCann, Klasky and Ye (2023) introduced it. It needs no retraining for a new forward model and works for nonlinear $A$, but it is an approximation: even with the exact score it does not sample the true posterior, as the example below shows in closed form.

## In plain words

A diffusion model learns to remove a little noise from an image, many times in a row. If you start from pure noise and keep removing noise, a clean, realistic image slowly appears.

To reconstruct a measured image, DPS does the same, with one change. After each noise removal step, it makes a quick guess of what the final clean image will be. It takes the measurements of that guess and compares them with the real measurements. Then it pushes the current noisy image a little in the direction that makes the guess fit the measurements better. At the end you get a realistic image that also agrees with the data. Running it again with new random noise gives a different image, which shows how uncertain the answer is.

## The problem

The model is $y = A(x_0) + n$ with $n \sim N(0, \sigma^2 I)$, where $A$ may be linear or a differentiable nonlinear map. The prior is the distribution of training signals, known only through a score network. The forward diffusion is $x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1 - \bar\alpha_t}\,\varepsilon$ with $\bar\alpha_t = \prod_{s \le t}(1 - \beta_s)$ for a schedule $\beta_1, \ldots, \beta_N$, and $\alpha_t = 1 - \beta_t$, $\bar\alpha_0 = 1$.

The input is $y$, functions for $A$ and the adjoint of its derivative ($A^T$ for linear $A$), a score function $s(x, t)$ with its vector-Jacobian product $v \mapsto J_s(x, t)^Tv$, the schedule, and step sizes. The output is one random signal $x_0$. The goal is that $x_0$ is a draw from $p(x_0 \mid y)$; DPS reaches this only approximately.

## The algorithm

The posterior score is $\nabla\log p_t(x_t \mid y) = \nabla\log p_t(x_t) + \nabla\log p(y \mid x_t)$. The first term is the score network. The second is intractable, because $p(y \mid x_t) = E[p(y \mid x_0) \mid x_t]$ is an integral over all clean signals. DPS replaces it by $p(y \mid \hat x_0)$, with $\hat x_0 = E[x_0 \mid x_t]$ from Tweedie's formula. This is Algorithm 1 of Chung et al., with steps indexed $t = N, \ldots, 1$.

```pseudo id=main
DPS(y, A, A^T, s, J_s^T, ᾱ_1..ᾱ_N, ζ)
L1  x ← a draw from N(0, I)
L2  for t = N down to 1
L3      ŝ ← s(x, t)                                     ▷ a given network
L4      x̂_0 ← (x + (1 - ᾱ_t) ŝ) / sqrt(ᾱ_t)             ▷ Tweedie's formula
L5      x' ← c_x x + c_0 x̂_0 + sqrt(β̃_t) z,  z from N(0, I)   ▷ the DDPM step
L6      g ← ∇_x ||y - A(x̂_0)||^2                        ▷ through x̂_0 and the network
L7      ζ_t ← ζ' / ||y - A(x̂_0)||
L8      x ← x' - ζ_t g
L9  return x
```

In line L5, $c_x = \sqrt{\alpha_t}(1 - \bar\alpha_{t-1})/(1 - \bar\alpha_t)$, $c_0 = \sqrt{\bar\alpha_{t-1}}\beta_t/(1 - \bar\alpha_t)$ and $\tilde\beta_t = \beta_t(1 - \bar\alpha_{t-1})/(1 - \bar\alpha_t)$: this is the reverse step of DDPM (Ho, Jain and Abbeel 2020) with $x_0$ replaced by $\hat x_0$. The paper calls the noise level $\tilde\sigma_t$ and leaves it to the DDPM sampler; the code uses $\tilde\beta_t$. Line L6 is one [backpropagation](/backpropagation/) through the network, since $\hat x_0$ depends on $x$ through $s$:

$$g = \frac{2}{\sqrt{\bar\alpha_t}}\big(I + (1 - \bar\alpha_t)J_s^T\big)A^T\big(A\hat x_0 - y\big).$$

Line L7 is the normalized step of the paper, with $\zeta'$ a tuned constant; the paper reports values between 0.1 and 1. The step that follows from the reverse SDE with Gaussian noise is $\zeta_t = \beta_t/(2\sigma^2\sqrt{\alpha_t})$, and the implementation accepts either.

## Example

**One step by hand.** Take a one-dimensional prior $N(0, 1)$, so that $p_t = N(0, 1)$ and the exact score is $-x$. Take $\bar\alpha_t = 0.5$, $\bar\alpha_{t-1} = 0.8$, so $\beta_t = 1 - 0.5/0.8 = 0.375$. Let $x_t = 1$, $A = 1$, $y = 1$ and $\zeta' = 0.5$.

- L3 and L4: $\hat s = -1$ and $\hat x_0 = (1 - 0.5)/\sqrt{0.5} = 0.707107$, which is $E[x_0 \mid x_t = 1]$.
- L5: $c_x = \sqrt{0.625} \cdot 0.2/0.5 = 0.316228$, $c_0 = \sqrt{0.8} \cdot 0.375/0.5 = 0.670820$, so the mean is $0.316228 + 0.670820 \cdot 0.707107 = 0.790569$, and $\sqrt{\tilde\beta_t} = \sqrt{0.15} = 0.387298$.
- L6: the residual is $\hat x_0 - y = -0.292893$, and $\partial\hat x_0/\partial x = (1 - 0.5)/\sqrt{0.5} = 0.707107$, so $g = 2 \cdot 0.707107 \cdot (-0.292893) = -0.414214$.
- L7 and L8: $\zeta_t = 0.5/0.292893 = 1.707107$ and $x_{t-1} = 0.790569 + 0.707107 + 0.387298\,z = 1.497676 + 0.387298\,z$.

The guidance moved the state by $0.707107$ toward the data. With the normalized step, the length of this move does not shrink as the residual goes to zero.

**DPS is not the posterior.** Keep the prior $N(0, 1)$ with its exact score, and take $A = 1$, $\sigma^2 = 0.25$ and $y = 1$. The true posterior is $N(0.8, 0.2)$. For a Gaussian prior every step is linear plus Gaussian noise, so the law of the output can be computed exactly. With the DDPM schedule ($N = 1000$, $\beta$ from $10^{-4}$ to $0.02$):

| guidance step $\zeta_t$ | output mean | output variance |
|---|---|---|
| none (prior sampler) | 0 | 0.99107 |
| DPS, $\beta_t/(2\sigma^2\sqrt{\alpha_t})$ | 0.98197 | 0.12167 |
| exact $p(y \mid x_t)$, $\beta_t/(2(\sigma^2 + 1 - \bar\alpha_t)\sqrt{\alpha_t})$ | 0.79999 | 0.19657 |
| true posterior | 0.8 | 0.2 |

The exact likelihood $p(y \mid x_t)$ has the variance $\sigma^2 + \operatorname{Var}(x_0 \mid x_t)$, and DPS drops the second term. So DPS trusts the data too much: its mean is close to $y$ and its spread is too small. The small remaining gap in the variance of the third row comes from the DDPM step itself, whose noise is slightly too small, as the first row shows.

## Correctness

DPS has no theorem that it samples the posterior, and the example shows that it does not, even with the exact score. The proof file proves what each line computes:

1. With the exact score, line L4 is $E[x_0 \mid x_t]$ (Tweedie's formula, Proposition 1 of the paper; a theorem).
2. Line L5 is a draw from the Gaussian $q(x_{t-1} \mid x_t, x_0)$ at $x_0 = \hat x_0$. With the exact score its mean is the true reverse mean, and its variance is too small by a term in $\operatorname{Var}(x_0 \mid x_t)$.
3. Line L6 is the exact gradient of $\|y - A(\hat x_0(x))\|^2$, by the chain rule.
4. For a Gaussian prior and fixed steps, the output is Gaussian with a mean and a variance given by a linear recursion, which gives the table above.

The guidance replaces $E[p(y \mid x_0) \mid x_t]$ by $p(y \mid E[x_0 \mid x_t])$, which is the gap in [Jensen's inequality](/jensens-inequality/). Theorem 1 of the paper bounds this gap by a constant times the posterior mean absolute deviation of $x_0$ given $x_t$. This is a theorem, but the deviation is large at early steps, so it does not give a sampling guarantee. That the samples look good on images is a measurement.

## Complexity

The model is real-ram. Each of the $N$ steps calls the score network once, its vector-Jacobian product once, $A$ once and $A^T$ once. So the time is $O(N(a + g))$, where $a$ is the cost of $A$ plus $A^T$ and $g$ is the cost of a forward and a backward pass through the network, which is outside this page; the backward pass costs a small constant times the forward pass. The extra space is $O(n + m)$ for the state, the estimate and the residual, plus the activations of one forward pass that the backward pass stores. The prior sampler without guidance has the same number of steps but no backward pass, so DPS costs about two to three times as much per sample. The paper uses $N = 1000$ network evaluations on FFHQ.

## Properties

- **Training free.** The score network is trained once on clean signals. A new forward model or noise level needs no retraining.
- **General forward models.** Only $A$ and the adjoint of its derivative are needed, so nonlinear problems such as [phase retrieval](/phase-retrieval/) and nonuniform deblurring fit.
- **Stochastic.** Different random seeds give different outputs; the spread is a rough, not a calibrated, measure of uncertainty.
- **Not exact.** Even with the exact score and many steps, the output law differs from the posterior, as computed above.
- **Soft data fit.** The data are not enforced exactly. With the normalized step the residual of the output is of the size of the last step, not zero.
- **Measured results.** Chung et al. report experiments on FFHQ and ImageNet images of $256 \times 256$ pixels for [inpainting](/image-inpainting/), [super-resolution](/super-resolution/), Gaussian and motion deblurring, phase retrieval and nonuniform deblurring, with Gaussian and Poisson noise, and compare with earlier diffusion and plug-and-play methods. These are measurements on those data sets.

## Variants and improvements

- **Poisson noise.** Replace the squared residual by a weighted residual with weights from the data; the paper treats this case.
- **Other samplers.** The guidance step can be added to DDIM or to a discretized reverse SDE instead of the DDPM step.
- **Projection methods.** For linear $A$, earlier methods replace the guidance by a projection onto the data-consistent set after each step, as in score-based inpainting (Song et al. 2021); this enforces noiseless data exactly but handles noise poorly.
- **Better likelihood approximations.** Use a Gaussian approximation of $p(x_0 \mid x_t)$ with a nonzero covariance, as the exact column of the table does, to reduce the overconfidence.
- **Optimization instead of sampling.** [CSGM](/compressed-sensing-generative-models/) searches the latent space of a generator for one best fit, and [plug-and-play priors](/plug-and-play-priors/) use a denoiser inside an optimization method.

## When to use it

Use DPS when a good diffusion model for the signal class exists, when the forward model changes between tasks or is nonlinear, and when realistic samples matter more than a calibrated posterior. Do not use it when you need correct uncertainty, for example error bars for a measurement; then use a Markov chain Monte Carlo method such as the [Metropolis-adjusted Langevin algorithm](/metropolis-adjusted-langevin-algorithm/) on a model with a known density, or the closed form of a [linear Gaussian problem](/linear-gaussian-inverse-problem/). Do not use it when the time budget allows only a few network evaluations per image.

## Pitfalls

- **Step size.** Too small a step ignores the data; too large a step makes the iterates leave the region where the score network was trained, and the output has artifacts. The best $\zeta'$ depends on the task.
- **Overconfidence.** The output fits the data more tightly than the posterior would, as the example shows. Do not read the sample spread as a posterior variance.
- **Forgetting the network in the gradient.** Line L6 differentiates through $\hat x_0$, which contains the network. Dropping $J_s$ gives a cheaper but different method.
- **Noise level.** With the normalized step, $\sigma$ does not enter the algorithm at all, so the method cannot tell low noise from high noise.
- **Prior mismatch.** The prior is only as good as the training set. For a signal unlike the training data, DPS still returns a realistic signal of the training class.

## Implementations

The score network is a given function: the code takes $s(x, t)$ and its vector-Jacobian product as arguments, with functions for $A$ and $A^T$, and runs lines L1 to L9 around them. The tests build the score by hand, as the exact score of a Gaussian prior or as a small $\tanh$ network with weights from a fixed seed; no network is trained. The tests check the schedule and that the last step returns $\hat x_0$, Tweedie's formula against the exact posterior mean, the guidance gradient against central differences, the exact mean and variance of the sampler against 1500 samples, the two rows of the table, that the unobserved entry of a noiseless inpainting problem follows the prior sampler exactly, and that each step calls the network, $A$ and $A^T$ once.

## History

Score-based and diffusion models (Song and Ermon 2019; Ho, Jain and Abbeel 2020; Song et al. 2021) generate samples by reversing a noising process. Early uses for inverse problems either projected onto the data after each step or trained a conditional model for one task. Chung et al. (2022) added a manifold constraint, and in 2023 Chung, Kim, McCann, Klasky and Ye proposed DPS, which uses the Tweedie estimate to approximate the likelihood of a noisy state and handles noise and nonlinear forward models. Later methods improved the likelihood approximation and the speed.

## References
