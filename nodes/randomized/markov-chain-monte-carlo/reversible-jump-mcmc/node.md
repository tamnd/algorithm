---
tag: 183JNF
kind: algorithm
slug: reversible-jump-mcmc
name: Reversible-jump MCMC
aliases:
- RJMCMC
- trans-dimensional MCMC
- reversible jump Markov chain Monte Carlo
area: randomized/markov-chain-monte-carlo
level: research
summary: Metropolis-Hastings across models of different dimension. Pad θ with u ~ g, map (θ, u) by a bijection h, and accept with the target ratio, divided by g(u) and multiplied by |det ∇h|.
solves: [sampling-from-stationary-distribution]
model: real-ram
complexity:
  vars: {T: the number of steps, d: the largest dimension of a model, c: the cost of one evaluation of the target}
  time: {worst: Θ(T (c + d))}
  space: {extra: Θ(d)}
properties: {in_place: true, online: true, deterministic: false, recursive: false}
history:
  year: 1995
  people: [Peter J. Green, Sylvia Richardson]
  note: Green introduced reversible-jump MCMC in 1995 for Bayesian model choice, and Richardson and Green applied it to mixtures with an unknown number of components in 1997.
prereqs: [metropolis-hastings, acceptance-probability]
see_also: [proposal-distribution, gibbs-sampling, parallel-tempering, independence-sampler, random-walk-metropolis, effective-sample-size, mixing-time]
sources:
  - paper: doi:10.1093/biomet/82.4.711
    title: Peter J. Green, Reversible jump Markov chain Monte Carlo computation and Bayesian model determination, Biometrika 82(4), 1995
    locator: pages 711 to 732 (the general construction, dimension matching and the acceptance probability with the Jacobian)
  - paper: doi:10.1111/1467-9868.00095
    title: Sylvia Richardson and Peter J. Green, On Bayesian analysis of mixtures with an unknown number of components (with discussion), Journal of the Royal Statistical Society Series B 59(4), 1997
    locator: pages 731 to 792 (split and merge moves, and birth and death moves, for normal mixtures)
  - paper: doi:10.1111/j.2517-6161.1995.tb02042.x
    title: Bradley P. Carlin and Siddhartha Chib, Bayesian model choice via Markov chain Monte Carlo methods, Journal of the Royal Statistical Society Series B 57(3), 1995
    locator: pages 473 to 484 (the product space method with pseudo priors)
  - paper: doi:10.1111/1467-9868.03711
    title: Stephen P. Brooks, Paolo Giudici and Gareth O. Roberts, Efficient construction of reversible jump Markov chain Monte Carlo proposal distributions, Journal of the Royal Statistical Society Series B 65(1), 2003
    locator: pages 3 to 39 (how to choose the jump proposals)
  - paper: doi:10.1214/aos/1016120364
    title: Matthew Stephens, Bayesian analysis of mixture models with an unknown number of components, an alternative to reversible jump methods, Annals of Statistics 28(1), 2000
    locator: pages 40 to 74 (a birth and death process in continuous time)
  - paper: doi:10.1111/j.1467-9574.2012.00516.x
    title: David I. Hastie and Peter J. Green, Model choice using reversible jump Markov chain Monte Carlo, Statistica Neerlandica 66(3), 2012
    locator: pages 309 to 338 (a review of the method and its practice)
---

Reversible-jump MCMC is the [Metropolis-Hastings](/metropolis-hastings/) algorithm on a state space that is a union of spaces of different dimension, $\mathcal{X} = \bigcup_k\{k\} \times \mathbb{R}^{d_k}$. The typical use is Bayesian model choice: $k$ indexes the models, $\theta \in \mathbb{R}^{d_k}$ are the parameters of model $k$, and the target $\pi(k, \theta)$ is the joint posterior of both. A move from model $k$ to model $k'$ with $d_{k'} > d_k$ draws extra random numbers $u \in \mathbb{R}^{d_{k'} - d_k}$ from a density $g$ and maps $(\theta, u)$ to $\theta'$ by a bijection $h$. It accepts with probability

$$\min\Big(1,\ \frac{\pi(k', \theta')\,j(k' \to k)}{\pi(k, \theta)\,j(k \to k')\,g(u)}\,\Big|\det\frac{\partial h(\theta, u)}{\partial(\theta, u)}\Big|\Big),$$

where $j$ gives the probabilities of the move types. The reverse move is deterministic, and it uses the inverse of this ratio. Green (1995) introduced the method. The Jacobian factor is the part that is easy to forget: without it, the chain has the wrong stationary law. The fraction of time the chain spends in model $k$ estimates the posterior probability of model $k$.

## In plain words

Sometimes the question is not only "what are the parameters?" but also "how many parameters are there?". For example: how many groups are in this data? Each answer is a model with its own number of unknowns, and the sampler must move between models.

To go from a model with fewer unknowns to one with more, the sampler draws some new random numbers, combines them with the current unknowns by a fixed recipe, and gets a proposal in the larger model. Then it accepts or rejects, as usual. The test must take into account how the recipe stretches or squeezes space. If it does not, the sampler visits some models too often. To go back, it runs the recipe in reverse.

## The problem

The input is a function $\log\tilde\pi(k, \theta)$, with $\tilde\pi = Z\pi$, for models $k = 0, \dots, K$ of dimensions $d_k$, together with:

- for each $k$, a kernel $P_k$ that keeps $\pi(k, \cdot)$ invariant, for the moves inside a model;
- for each $k < K$, a density $g_k$ on $\mathbb{R}^{r_k}$ with $d_k + r_k = d_{k+1}$, and a differentiable bijection $h_k$ from $\mathbb{R}^{d_k} \times \mathbb{R}^{r_k}$, or an open subset of it, onto the support of $\pi(k + 1, \cdot)$, with a differentiable inverse;
- a start $(k_0, \theta_0)$ and a number of steps $T$.

The output is a Markov chain on $\mathcal{X}$ with stationary law $\pi$, as in [sampling from a stationary distribution](/sampling-from-stationary-distribution/). Here $\pi$ is a density with respect to the sum, over $k$, of Lebesgue measure on $\mathbb{R}^{d_k}$. The condition $d_k + r_k = d_{k+1}$ is called dimension matching.

## The algorithm

```pseudo id=main
REVERSIBLE-JUMP(log π̃, P_0, …, P_K, (g_k, h_k) for k < K, (k, θ), T)
L1  for t ← 1 to T do
L2      draw the move type: inside the model with probability 1/2, up with 1/4, down with 1/4
L3      if inside then θ ← one step of P_k from θ
L4      else if up and k < K then draw u from g_k, and let (k', θ') ← (k + 1, h_k(θ, u))
L5          r ← π̃(k + 1, θ') |det ∇h_k(θ, u)| / (π̃(k, θ) g_k(u))
L6      else if down and k > 0 then let (θ', u) ← h_{k−1}^{−1}(θ) and k' ← k − 1
L7          r ← π̃(k − 1, θ') g_{k−1}(u) / (π̃(k, θ) |det ∇h_{k−1}(θ', u)|)
L8      if a jump was proposed then draw v uniformly from [0, 1), and if v < r then (k, θ) ← (k', θ')
L9      X_t ← (k, θ)
L10 return X_1, …, X_T
```

The move probabilities $j(k \to k + 1) = j(k + 1 \to k) = \frac14$ are equal, so they cancel in lines L5 and L7. An up move from the largest model or a down move from the smallest is rejected at once. The ratio in line L7 is exactly the inverse of the ratio in line L5 for the pair of states involved, so the code computes the up ratio for the reverse move and negates its logarithm.

## Example

**The model.** Model 0 has one parameter, model 1 has two, and

$$\pi(0, \theta) = 0.3\,\varphi(\theta), \qquad \pi(1, \theta_1, \theta_2) = 0.7\,\varphi(\theta_1)\varphi(\theta_2),$$

with $\varphi$ the standard normal density. So the correct model probabilities are $0.3$ and $0.7$. The split move draws $u \sim \mathcal{N}(0, 1)$ and sets $h(\theta, u) = (\theta - u, \theta + u)$. Its derivative is the matrix $\left(\begin{smallmatrix}1 & -1\\ 1 & 1\end{smallmatrix}\right)$, with determinant 2. The merge move sets $\theta = (\theta_1 + \theta_2)/2$ and $u = (\theta_2 - \theta_1)/2$.

**One split by hand.** From $\theta = 0.2$ with $u = 0.5$, the proposal is $(\theta_1, \theta_2) = (-0.3, 0.7)$. Since $\theta_1^2 + \theta_2^2 = 2\theta^2 + 2u^2$,

$$r = \frac{0.7\,\varphi(-0.3)\varphi(0.7)}{0.3\,\varphi(0.2)\varphi(0.5)} \cdot 2 = \frac{14}3e^{-(\theta^2 + u^2)/2} = \frac{14}3e^{-0.145} \approx 4.037,$$

so the split is accepted. The merge from $(-0.3, 0.7)$ back to $0.2$ has ratio $1/4.037 \approx 0.248$.

**The Jacobian matters.** A run of 40000 steps with seed 2 and random-walk Metropolis inside each model spent a fraction $0.7055$ of its time in model 1, with 53 percent of the jumps accepted. A run with seed 3 and without the factor 2 spent a fraction $0.5407$ in model 1. Without the Jacobian the up ratio is half the correct one, so the chain is exact for a target with the weight of model 1 halved, and its fraction is $0.35/0.65 = 7/13 \approx 0.5385$, not $0.7$. The tests check both values against the Monte Carlo error. They also check a map with a Jacobian that is not constant, $h(\theta, u) = (\theta, \theta + e^u)$ with $|\det| = e^u$, onto ordered pairs.

## Correctness

**Theorem.** If each $P_k$ keeps $\pi(k, \cdot)$ invariant, then every move of the algorithm satisfies detailed balance with respect to $\pi$ on $\mathcal{X}$, so $\pi$ is a stationary law of the chain.

Fix $k$, write $h = h_k$, $g = g_k$, and let $J(\theta, u) = |\det\nabla h(\theta, u)|$. Let $a(\theta, u)$ be the acceptance probability of the up move from $(k, \theta)$ with extra variables $u$, and $b(\theta')$ that of the down move from $(k + 1, \theta')$. Lines L5 and L7 give

$$\pi(k, \theta)g(u)\,a(\theta, u) = \min\big(\pi(k, \theta)g(u),\ \pi(k + 1, h(\theta, u))J(\theta, u)\big) = \pi(k + 1, h(\theta, u))J(\theta, u)\,b(h(\theta, u)).$$

For sets $A \subseteq \mathbb{R}^{d_k}$ and $B \subseteq \mathbb{R}^{d_{k+1}}$, the probability flow from $\{k\} \times A$ to $\{k + 1\} \times B$ is the integral of the left side over $\{\theta \in A, h(\theta, u) \in B\}$, times $\frac14$. The change of variables $\theta' = h(\theta, u)$ turns the integral of the right side into $\int_B\pi(k + 1, \theta')b(\theta')\mathbf 1[\theta \in A]\,d\theta'$, where $(\theta, u) = h^{-1}(\theta')$, which is the flow back, times $\frac14$. The Jacobian $J$ is exactly the factor that the change of variables needs. The proof file gives the details, and the tests check the pointwise identity above at random points.

As for all MCMC, convergence needs the chain to be irreducible: the jumps must connect all the models, and the moves inside each model must reach its whole support. Stationarity says nothing about how fast the chain moves between models.

## Complexity

One step evaluates $\tilde\pi$ once at the proposal and computes $h$, its inverse and its Jacobian, which costs $O(d)$ for the maps used in practice, so $T$ steps take $\Theta(T(c + d))$ time and $\Theta(d)$ memory beyond the output. The real cost is statistical. A jump is accepted only when the proposal in the new model is plausible there, and good jumps need proposals adapted to each pair of models. The fraction of time in each model is an average of indicators, and its error depends on the [effective sample size](/effective-sample-size/) of that indicator, which can be small when jumps are rare.

## Properties

- **Exact.** The stationary law is $\pi$ for every choice of $g_k$ and $h_k$ that satisfies the conditions.
- **Model averaging.** One run gives both the posterior model probabilities and the parameters inside each model.
- **Needs the Jacobian.** Every map $h_k$ must be a differentiable bijection with a known Jacobian.
- **Contains ordinary MH.** If all models have the same dimension and $r_k = 0$ with $h_k$ the identity, the jumps are ordinary Metropolis-Hastings moves on the model index.
- **Not automatic.** Its efficiency depends on the jump proposals, which the user must design.

## Variants and improvements

- **Birth and death moves.** Add or remove one component with $h$ close to the identity, as in Richardson and Green (1997). Stephens (2000) replaced the discrete moves by a birth and death process in continuous time.
- **Split and merge moves.** Split one component into two that keep some moments, as in the example. Richardson and Green used them for normal mixtures.
- **Product space methods** (Carlin and Chib 1995). Keep the parameters of all models at all times, with pseudo priors for the models not in use, and run a [Gibbs sampler](/gibbs-sampling/) on the model index. It can be written as a reversible-jump chain on a larger space.
- **Better proposals.** Brooks, Giudici and Roberts (2003) choose the parameters of $g$ and $h$ so that the jump acceptance is high near typical states.
- **Tempering.** For models that are far apart, combine the jumps with [parallel tempering](/parallel-tempering/).

## When to use it

Use reversible-jump MCMC when the number of parameters is itself unknown and should be treated as random: mixtures with an unknown number of components, change points, variable selection, phylogenetic trees and curve fitting with free knots. When there are only a few models, it is often simpler and more accurate to fit each model on its own and to compare them with estimates of their marginal likelihoods.

## Pitfalls

- **A missing or wrong Jacobian.** The chain still runs and looks healthy, but the model probabilities are wrong, as in the example.
- **A missing density of $u$.** The factor $g(u)$ must be in the up ratio, and in the down ratio for the $u$ that the inverse map gives back.
- **Unequal move probabilities.** If $j(k \to k')$ differs from $j(k' \to k)$, for example at the boundary of the model range, the factor $j(k' \to k)/j(k \to k')$ must be in the ratio.
- **A map that is not a bijection.** If $h$ does not cover the support of the larger model, some states can never be merged, and the chain is wrong or not irreducible.
- **Rare jumps.** If almost every jump is rejected, the model probabilities come from a few visits. Check the number of jumps and the effective sample size of the model indicator.
- **Trusting the diagnostics.** A stable fraction of time in each model does not prove convergence: the chain may never have found a model with high probability.

## Implementations

## History

Green (1995) gave the general construction of Metropolis-Hastings on spaces of variable dimension, with dimension matching and the Jacobian in the acceptance ratio, and applied it to Bayesian model determination, for example change point problems. In the same year Carlin and Chib (1995) proposed the product space method. Richardson and Green (1997) used split, merge, birth and death moves for normal mixtures with an unknown number of components, which made the method well known. Stephens (2000) proposed an alternative based on a birth and death process, and Brooks, Giudici and Roberts (2003) studied the choice of proposals. Hastie and Green (2012) reviewed the method.

## References
