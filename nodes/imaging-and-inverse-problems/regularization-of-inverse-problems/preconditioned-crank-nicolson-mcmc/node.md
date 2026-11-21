---
tag: 63HRT4
kind: algorithm
slug: preconditioned-crank-nicolson-mcmc
name: Preconditioned Crank-Nicolson MCMC
aliases:
- pCN sampler
- pCN
- preconditioned Crank-Nicolson
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: research
summary: "A Metropolis-Hastings sampler whose proposal keeps a Gaussian prior invariant, so its acceptance rate does not fall as the discretization is refined."
solves: [sampling-from-stationary-distribution]
model: real-ram
complexity:
  vars: {N: the number of steps, n: the dimension of the discretized unknown, T: the cost of one misfit evaluation, D: the cost of one prior draw}
  time: {worst: Θ(N (n + D + T)), average: Θ(N (n + D + T)), best: Θ(N (n + D + T))}
  space: {extra: Θ(N n)}
properties: {randomized: true, exact_invariance: true, needs_prior_density: false, dimension_robust: true}
history:
  year: 2013
  people: [Simon L. Cotter, Gareth O. Roberts, Andrew M. Stuart, David White]
  note: "Beskos, Roberts, Stuart and Voss (2008) used Crank-Nicolson proposals for diffusion bridges. Cotter, Roberts, Stuart and White (2013) named pCN and set it in the function-space view of Bayesian inverse problems."
prereqs: [metropolis-hastings, bayesian-inverse-problem, random-walk-metropolis]
see_also: [randomize-then-optimize, metropolis-adjusted-langevin-algorithm, hamiltonian-monte-carlo, independence-sampler, linear-gaussian-inverse-problem, crank-nicolson-method, effective-sample-size, gaussian-process]
sources:
  - paper: doi:10.1214/13-STS421
    title: S. L. Cotter, G. O. Roberts, A. M. Stuart and D. White, MCMC methods for functions, modifying old algorithms to make them faster, Statistical Science 28(3), 2013
    locator: pages 424 to 446
  - paper: doi:10.1142/S0219493708002378
    title: Alexandros Beskos, Gareth Roberts, Andrew Stuart and Jochen Voss, MCMC methods for diffusion bridges, Stochastics and Dynamics 8(3), 2008
    locator: pages 319 to 350
  - paper: doi:10.1214/13-AAP982
    title: Martin Hairer, Andrew M. Stuart and Sebastian J. Vollmer, Spectral gaps for a Metropolis-Hastings algorithm in infinite dimensions, Annals of Applied Probability 24(6), 2014
    locator: pages 2455 to 2490
  - paper: doi:10.1017/S0962492910000061
    title: Andrew M. Stuart, Inverse problems, a Bayesian perspective, Acta Numerica 19, 2010
    locator: pages 451 to 559
---

Preconditioned Crank-Nicolson (pCN) is a Metropolis-Hastings method for posteriors of the form "Gaussian prior times likelihood". From the state $u$ it proposes $v = m_0 + \sqrt{1 - \beta^2}\,(u - m_0) + \beta\xi$, where $\xi$ is a fresh draw from the centred prior $N(0, C)$ and $\beta \in (0, 1]$ is a step size, and it accepts $v$ with probability $\min\{1, \exp(\Phi(u) - \Phi(v))\}$, where $\Phi$ is the data misfit. The proposal leaves the prior invariant, so the prior cancels from the acceptance ratio and only the likelihood is left. This makes the method well defined on a function space, and its acceptance rate stays the same when the mesh of the discretization is refined. Random-walk Metropolis, in contrast, needs a step size that goes to zero as the dimension grows. Cotter, Roberts, Stuart and White (2013) introduced the name and the function-space view; Hairer, Stuart and Vollmer (2014) proved a dimension-independent spectral gap.

## In plain words

You want samples of an unknown function that fit the data, and you started with a Gaussian guess about what such functions look like. A plain random walk adds random noise to the current function. In fine resolution almost every such step makes the function rougher than the prior allows, so almost all steps are rejected. pCN instead shrinks the current function a little toward the prior mean and adds a fresh prior-like function. If there were no data, every such step would be accepted. So the only reason to reject a step is that it fits the data worse, and that does not get harder when you refine the grid.

## The problem

Sample the posterior of a [Bayesian inverse problem](/bayesian-inverse-problem/) with a Gaussian prior $\mu_0 = N(m_0, C)$ and misfit $\Phi(u) = \frac12\lVert\Gamma^{-1/2}(y - G(u))\rVert^2$:

$$\mu^y(du) = \frac1Z\exp(-\Phi(u))\,\mu_0(du).$$

The unknown $u$ may be a vector in $\mathbb{R}^n$ that comes from discretizing a function. The input is a way to evaluate $\Phi$, a way to draw from $N(0, C)$, a start $u_0$, a step size $\beta \in (0, 1]$ and a number of steps $N$. The output is a Markov chain $u_1, \dots, u_N$ whose law converges to $\mu^y$, and the rate of accepted moves.

## The algorithm

```pseudo id=main
PCN(Phi, draw_prior, u_0, beta, N, m_0)   ▷ prior N(m_0, C), draw_prior returns xi ~ N(0, C)
L1  u ← u_0, Phi_u ← Phi(u)
L2  for k = 1, ..., N
L3      xi ← draw_prior()
L4      v ← m_0 + sqrt(1 - beta²) (u - m_0) + beta xi
L5      Phi_v ← Phi(v)
L6      draw U uniform on (0, 1]; if log U < Phi_u - Phi_v
L7          u ← v, Phi_u ← Phi_v, count the move as accepted
L8      append u to the chain
L9  return the chain and (number of accepted moves) / N
```

Line L1 evaluates the misfit at the start and keeps it, so each step needs one new evaluation. Line L3 draws from the prior covariance: with a Karhunen-Loeve basis this is a sum of basis functions with independent Gaussian weights, and with a dense covariance it is $L z$ with a Cholesky factor $L$ and $z \sim N(0, I)$. Line L4 is the proposal. If $u$ has the prior law, so does $v$, because $(1 - \beta^2)C + \beta^2C = C$. Lines L5 and L6 accept with probability $\min\{1, e^{\Phi(u) - \Phi(v)}\}$. The prior density is not in this ratio. Line L8 stores the current state, which is the old one after a rejection.

The name comes from the Crank-Nicolson scheme. Discretize the Langevin equation $du = -(u - m_0)\,dt + \sqrt{2C}\,dW$, which has the prior as its invariant law, with the implicit midpoint rule ([Crank-Nicolson](/crank-nicolson-method/)) and time step $\delta$. This gives line L4 with $\sqrt{1 - \beta^2} = (2 - \delta)/(2 + \delta)$ and $\beta^2 = 8\delta/(2 + \delta)^2$. The covariance $C$ in the noise term is the preconditioner. The case $\beta = 1$ is the [independence sampler](/independence-sampler/) with the prior as proposal.

## Example

A scalar problem: $y = au + \eta$ with $a = 0.1$, $\eta \sim N(0, 0.05^2)$, prior $N(0, 1)$ and $y = 0.12$. The posterior is $N(0.96, 0.2)$; see the [Bayesian inverse problem](/bayesian-inverse-problem/) page. Each run has 20000 steps from $u_0 = 0$ with `random.Random(1)`, and the statistics drop the first 1000 states.

| $\beta$ | acceptance | sample mean | sample variance |
|---|---|---|---|
| 0.1 | 0.935 | 0.997 | 0.182 |
| 0.3 | 0.808 | 0.963 | 0.196 |
| 0.5 | 0.689 | 0.967 | 0.195 |
| 0.9 | 0.453 | 0.958 | 0.204 |
| 1.0 | 0.326 | 0.959 | 0.203 |

Small $\beta$ gives a high acceptance rate but small moves, and its estimates are the worst here. A high acceptance rate alone does not mean good mixing.

The effect of the dimension: prior variances $1/k^2$ for $k = 1, \dots, n$ (a Karhunen-Loeve type prior), one observation of $\sum_ku_k/k$ with value $0.5$ and noise standard deviation $0.1$, $\beta = 0.3$, 2000 steps, `random.Random(2)`. Random-walk Metropolis uses the proposal $u + \beta\xi$ with the same $\xi$.

| $n$ | pCN acceptance | random-walk acceptance |
|---|---|---|
| 10 | 0.384 | 0.294 |
| 100 | 0.371 | 0.043 |
| 1000 | 0.376 | 0.000 |

pCN keeps its rate. The random walk loses it, because $\lVert C^{-1/2}\beta\xi\rVert^2$ grows like $\beta^2n$, and the prior ratio in its acceptance test goes to zero. These are measurements with fixed seeds.

## Correctness

The proof is in `proofs/correctness.md`. The loop has $N$ passes, so the method stops. If $u \sim N(m_0, C)$ and $v$ is made by line L4, then $(u, v)$ and $(v, u)$ have the same Gaussian law, because their cross-covariance $\sqrt{1 - \beta^2}\,C$ is symmetric. So the proposal is reversible for the prior. Then

$$\mu^y(du)\,q(u, dv)\,a(u, v) = Z^{-1}\min\{e^{-\Phi(u)}, e^{-\Phi(v)}\}\,\mu_0(du)\,q(u, dv)$$

is symmetric in $(u, v)$, which is detailed balance, and the posterior is invariant. In finite dimension with finite $\Phi$ the chain is irreducible, and averages converge to posterior expectations. All this is a theorem. That the convergence speed does not depend on $n$ is a deeper theorem of Hairer, Stuart and Vollmer (2014), under conditions on $\Phi$, and is cited here; the tables above are measurements.

## Complexity

Each step does one prior draw (line L3), one linear combination of length $n$ (line L4) and one misfit evaluation (line L5). With $D$ the cost of a draw and $T$ that of $\Phi$, $N$ steps cost $\Theta(N(n + D + T))$. A draw costs $\Theta(n)$ with a diagonal or Karhunen-Loeve prior and $\Theta(n^2)$ with a dense Cholesky factor, which costs $\Theta(n^3)$ once. In inverse problems $T$ is usually a forward PDE solve and dominates everything. Storing the chain needs $\Theta(Nn)$ space; running averages need $\Theta(n)$.

## Properties

- Exact: the posterior is invariant for every $\beta \in (0, 1]$, with no discretization bias from the Crank-Nicolson step.
- Prior-reversible proposal: with $\Phi = 0$ every proposal is accepted.
- Robust to mesh refinement: the acceptance rate and, under conditions, the spectral gap do not depend on the dimension of the discretization.
- Needs only $\Phi$ and prior draws. No gradient, and no prior density.
- Scale of $\beta$: acceptance rates of 0.2 to 0.4 are a common target; $\beta$ is tuned in a short pilot run.

## Variants and improvements

- **Non-centred priors.** Line L4 with $m_0$ as written; for a prior $N(m_0, C)$ the misfit is unchanged.
- **Gradient versions.** pCN-Langevin (pCNL) adds a drift term with $C\nabla\Phi$, the analogue of [MALA](/metropolis-adjusted-langevin-algorithm/), and stays well defined on function space (Cotter et al. 2013).
- **Geometry-aware versions.** Replace $C$ in the proposal by a covariance adapted to the posterior, such as a Laplace approximation at the MAP point, so that the step is large in directions the data do not inform and small in those they do. Dimension-independent likelihood-informed (DILI) MCMC and infinite-dimensional manifold methods follow this idea.
- **Hierarchical priors.** If the prior has its own hyperparameters, update them in a [Gibbs](/gibbs-sampling/) step, with care, since the prior and the hyperparameter are strongly coupled in high dimension.
- **Multilevel and delayed acceptance.** Evaluate a cheap coarse model first and the expensive one only if the coarse step passes.

## When to use it

Use pCN when the prior is Gaussian, the unknown is a discretized function, and you want a simple sampler that keeps working when the mesh is refined, for example for PDE-constrained inverse problems with a Gaussian random field prior. It needs no gradients. If the data are very informative, the posterior is much narrower than the prior in some directions, $\beta$ must be small, and mixing is slow; then use a geometry-aware variant, [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/), or [randomize-then-optimize](/randomize-then-optimize/). For non-Gaussian priors, transform them to a Gaussian first, or use another method.

## Pitfalls

- Using the prior density in the test of line L6. The ratio must be $e^{\Phi(u) - \Phi(v)}$ only. Adding the prior ratio counts the prior twice and samples the wrong law.
- Drawing $\xi$ in line L3 from the wrong covariance, for example $N(0, I)$ when the prior is $N(0, C)$. Then the proposal is no longer prior-reversible, and the chain samples the wrong law.
- Forgetting the mean in line L4. With $m_0 \ne 0$ the proposal must shrink $u - m_0$, not $u$.
- Recomputing $\Phi(u)$ in every step instead of keeping it from line L1 or L7. This doubles the cost when $\Phi$ is a PDE solve.
- Taking the acceptance rate from line L9 as a measure of quality. Small $\beta$ gives a high rate and slow mixing; use the [effective sample size](/effective-sample-size/).
- Using `log(random())` in line L6 when the generator can return 0. Draw $U$ in $(0, 1]$.

## Implementations

## History

Crank-Nicolson type proposals that keep a Gaussian reference law invariant appeared in work on sampling diffusion bridges by Beskos, Roberts, Stuart and Voss (2008). Cotter, Roberts, Stuart and White (2013) gave the name pCN, derived it from the Crank-Nicolson scheme, and placed it in the function-space framework of Bayesian inverse problems of Stuart (2010). They note that the same proposal was used earlier by Neal for Gaussian process models. Hairer, Stuart and Vollmer (2014) proved that pCN has a spectral gap that does not depend on the dimension, while that of random-walk Metropolis goes to zero.

## References
