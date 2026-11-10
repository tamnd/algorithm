---
tag: CGM810
kind: algorithm
slug: metropolis-adjusted-langevin-algorithm
name: Metropolis-adjusted Langevin algorithm
aliases:
- MALA
- Langevin Monte Carlo
- Langevin-Hastings algorithm
area: randomized/markov-chain-monte-carlo
level: advanced
summary: Metropolis-Hastings with the proposal y = x + (h/2)∇log π(x) + √h Z, one Euler step of the Langevin diffusion. In d dimensions h can scale as d^(−1/3), and the best acceptance rate is 0.574.
solves: [sampling-from-stationary-distribution]
model: real-ram
complexity:
  vars: {T: the number of steps, d: the dimension, c: the cost of one evaluation of the log target and its gradient}
  time: {worst: Θ(T (d + c))}
  space: {extra: Θ(d)}
properties: {in_place: true, online: true, deterministic: false, recursive: false}
history:
  year: 1996
  people: [Gareth O. Roberts, Richard L. Tweedie, Jeffrey S. Rosenthal, Peter J. Rossky, Julian Besag]
  note: Rossky, Doll and Friedman used Langevin proposals with a Metropolis test in chemistry in 1978. Roberts and Tweedie analysed MALA and named it in 1996, and Roberts and Rosenthal found the rate 0.574 in 1998.
prereqs: [metropolis-hastings, random-walk-metropolis]
see_also: [hamiltonian-monte-carlo, hamiltonian-dynamics, acceptance-probability, proposal-distribution, no-u-turn-sampler, effective-sample-size]
sources:
  - paper: doi:10.2307/3318418
    title: Gareth O. Roberts and Richard L. Tweedie, Exponential convergence of Langevin distributions and their discrete approximations, Bernoulli 2(4), 1996
    locator: pages 341 to 363 (the unadjusted and the Metropolis-adjusted Langevin algorithms, and when they converge geometrically)
  - paper: doi:10.1111/1467-9868.00123
    title: Gareth O. Roberts and Jeffrey S. Rosenthal, Optimal scaling of discrete approximations to Langevin diffusions, Journal of the Royal Statistical Society Series B 60(1), 1998
    locator: pages 255 to 268 (step size of order d^(-1/3) and the acceptance rate 0.574)
  - paper: doi:10.1063/1.436415
    title: Peter J. Rossky, Jimmie D. Doll and Harold L. Friedman, Brownian dynamics as smart Monte Carlo simulation, Journal of Chemical Physics 69(10), 1978
    locator: pages 4628 to 4633 (force-biased proposals corrected by a Metropolis test)
  - paper: doi:10.1214/ss/1015346320
    title: Gareth O. Roberts and Jeffrey S. Rosenthal, Optimal scaling for various Metropolis-Hastings algorithms, Statistical Science 16(4), 2001
    locator: pages 351 to 367 (a survey that compares the scaling of random-walk Metropolis and MALA)
  - paper: doi:10.1111/j.1467-9868.2010.00765.x
    title: Mark Girolami and Ben Calderhead, Riemann manifold Langevin and Hamiltonian Monte Carlo methods, Journal of the Royal Statistical Society Series B 73(2), 2011
    locator: pages 123 to 214 (MALA with a position-dependent metric)
---

The Metropolis-adjusted Langevin algorithm (MALA) is the [Metropolis-Hastings](/metropolis-hastings/) algorithm with a proposal that moves along the gradient of $\log\pi$. From $x \in \mathbb{R}^d$ it proposes

$$y = x + \frac{h}{2}\nabla\log\pi(x) + \sqrt h\,Z, \qquad Z \sim \mathcal{N}(0, I_d),$$

which is one Euler step of size $h$ of the Langevin diffusion $dX_t = \frac12\nabla\log\pi(X_t)\,dt + dB_t$, a diffusion that has $\pi$ as its stationary law. The proposal is not symmetric, so the [acceptance probability](/acceptance-probability/) contains the Hastings factor $q(x \mid y)/q(y \mid x)$. Without the test, the chain is the unadjusted Langevin algorithm (ULA), whose stationary law is not $\pi$. Roberts and Tweedie (1996) studied both. Roberts and Rosenthal (1998) showed that for product targets in $d$ dimensions the step size can be of order $d^{-1/3}$, against $d^{-1}$ for [random-walk Metropolis](/random-walk-metropolis/), with the best acceptance rate near $0.574$. MALA is the same as [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/) with one leapfrog step.

## In plain words

A random-walk sampler steps in a random direction. MALA first looks at the slope of the target at the current point and moves a little uphill, toward more likely places, and then adds a random step. The proposals are better, so they can be larger.

Because the uphill push is not the same in both directions, a correction is needed: the test compares how likely the move is forward and backward, and it accepts or rejects. Without this test, the sampler is slightly wrong, and it can even run away to infinity for some targets.

## The problem

The input is a function $\log\tilde\pi$, with $\tilde\pi = Z\pi$ positive and continuously differentiable on $\mathbb{R}^d$, its gradient, a start $x_0$, a step size $h > 0$ and a number of steps $T$. The output is a Markov chain $X_1, \ldots, X_T$ with $\pi$ as a stationary distribution, as in [sampling from a stationary distribution](/sampling-from-stationary-distribution/). Write $\mu(x) = x + \frac h2\nabla\log\tilde\pi(x)$, so that the proposal density is $q(y \mid x) = (2\pi h)^{-d/2}\exp(-|y - \mu(x)|^2/(2h))$. Note that $\nabla\log\tilde\pi = \nabla\log\pi$. The model of randomness is $d$ standard normal reals and one uniform real per step.

## The algorithm

```pseudo id=main
MALA(log π̃, ∇log π̃, x0, h, T)
L1  x ← x0
L2  for t ← 1 to T do
L3      draw Z ~ N(0, I_d)
L4      y ← x + (h/2) ∇log π̃(x) + √h Z
L5      r ← π̃(y) q(x | y) / (π̃(x) q(y | x)),  where q(b | a) = exp(−|b − a − (h/2)∇log π̃(a)|² / (2h))
L6      draw u uniformly from [0, 1)
L7      if u < r then x ← y
L8      X_t ← x
L9  return X_1, …, X_T
```

The constant $(2\pi h)^{-d/2}$ cancels in line L5, and so does $Z$. In code, line L5 is computed in logarithms, and the gradient at $x$ is kept from the step that accepted $x$, so each step costs one new value and one new gradient.

## Example

Take $\pi = \mathcal{N}(0, 1)$, so $\nabla\log\pi(x) = -x$ and $\mu(x) = (1 - h/2)x$. With $h = 0.5$, $\mu(x) = 0.75x$, and $x_0 = 1$.

| step | $x$ | $\mu(x)$ | $Z$ | $y = \mu(x) + \sqrt{0.5}\,Z$ | $r$ | $u$ | $X_t$ |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 0.75 | 0.6 | 1.1743 | 0.9766 | 0.4 | 1.1743 |
| 2 | 1.1743 | 0.8807 | $-1.2$ | 0.0322 | 1.0899 | 0.95 | 0.0322 |
| 3 | 0.0322 | 0.0241 | 0.3 | 0.2363 | 0.9966 | 0.5 | 0.2363 |

The drift pulls every proposal toward the mode, so the ratios are close to 1. In step 2, the target ratio $\pi(y)/\pi(x) = 1.99$ is large, but the reverse proposal from $0.0322$ to $1.1743$ is less likely than the forward one, and the Hastings factor brings $r$ down to $1.09$.

**Why the test is needed.** On $\mathcal{N}(0, 1)$ the unadjusted chain is $X_{t+1} = (1 - h/2)X_t + \sqrt h\,Z_t$, an AR(1) chain. For $0 < h < 4$ its stationary law is $\mathcal{N}(0, \sigma_h^2)$ with $\sigma_h^2 = h/(1 - (1 - h/2)^2) = 1/(1 - h/4)$. So with $h = 1$ the unadjusted chain has variance $4/3$, not 1, and for $h \ge 4$ it diverges. MALA with the same $h$ has the correct variance 1. The tests check both numbers.

## Correctness

**Theorem.** For every $h > 0$, the MALA chain satisfies [detailed balance](/detailed-balance/) with respect to $\pi$, so $\pi$ is stationary. If $\nabla\log\pi$ is continuous, the chain is $\pi$-irreducible and aperiodic, so it converges to $\pi$ in total variation from $\pi$-almost every start.

The proposal has a positive density $q(y \mid x)$, and line L5 is the Metropolis-Hastings ratio for it, so the general proof applies. The proof file gives the details and also derives the stationary variance of the unadjusted chain. Convergence can be slow. Roberts and Tweedie (1996) showed that the Langevin diffusion itself converges exponentially fast for many targets for which the discretizations behave badly. When the tails of $\pi$ are lighter than Gaussian, for example $\pi(x) \propto e^{-x^4}$, the unadjusted chain can be transient: from a far point, the drift step overshoots to an even farther point. MALA then rejects such moves and stays put, so it does not run away, but it is not geometrically ergodic. Geometric ergodicity holds for targets whose tails behave in a way close to Gaussian.

## Complexity

One step costs one evaluation of $\log\tilde\pi$ and one gradient at the proposal, plus $O(d)$ other work, so $T$ steps take $\Theta(T(d + c))$ time and $\Theta(d)$ memory.

**Optimal scaling (Roberts and Rosenthal 1998).** Let the target be a product $\pi_d(x) = \prod_{i=1}^d f(x_i)$ of a fixed smooth density $f$, under smoothness and moment conditions on $\log f$ and its derivatives, let $h = \ell^2d^{-1/3}$, and start the chain in stationarity. Then, with time sped up by the factor $d^{1/3}$, each coordinate converges to a Langevin diffusion with speed $\ell^2a(\ell)$, where $a(\ell) = 2\Phi(-K\ell^3)$ is the limit of the mean acceptance rate and $K > 0$ depends on $f$. The speed is largest when $a(\ell) = 0.574$, for every $f$. For $f = \mathcal{N}(0, 1)$, $K = 1/8$, so the best $\ell$ is $1.65$; a test checks the rate on $\mathcal{N}(0, I_{400})$. So MALA needs $O(d^{1/3})$ steps for each unit of diffusion time, against $O(d)$ for random-walk Metropolis and $O(d^{1/4})$ leapfrog steps for HMC (Beskos et al. 2013).

The hypothesis of a stationary start matters more for MALA than for random-walk Metropolis. Christensen, Roberts and Rosenthal (2005) showed that from a start in the tails, the step must be smaller, of order $d^{-1/2}$, for the chain to reach the bulk of the target.

## Properties

- **Uses the gradient.** It needs $\nabla\log\tilde\pi$ but not the normalizing constant.
- **Not symmetric.** The Hastings factor is required. Leaving it out gives a chain with the wrong stationary law.
- **One tuning parameter.** The step size $h$, set for a mean acceptance rate near $0.574$ in high dimension.
- **Exact for every $h$.** The discretization error of the Euler step affects only the acceptance rate.
- **Local.** Each step is short, so MALA still moves diffusively, unlike long HMC trajectories.

## Variants and improvements

- **Preconditioned MALA.** Use $y = x + \frac h2A\nabla\log\pi(x) + \sqrt h\,A^{1/2}Z$ with a fixed positive definite $A$ close to the covariance of $\pi$, and the matching Hastings factor.
- **Riemann manifold MALA** (Girolami and Calderhead 2011). Let $A$ depend on $x$, for example through the Fisher information.
- **Unadjusted Langevin algorithm.** Skip the test. It is biased, with an error that goes to 0 with $h$, and it is used when the Metropolis test is too expensive or in large-data settings with stochastic gradients.
- **Truncated drift.** Cap the size of the drift term $\frac h2\nabla\log\pi(x)$ to avoid the overshoot in light tails (Roberts and Tweedie 1996).
- **[HMC](/hamiltonian-monte-carlo/).** HMC with $L = 1$ leapfrog step of size $\varepsilon$ is MALA with $h = \varepsilon^2$, and more leapfrog steps give better scaling.

## When to use it

Use MALA for smooth targets in moderate to high dimension when a gradient is available and the target is close to Gaussian in its tails, or as a building block, for example inside Gibbs sampling. For most such targets [HMC](/hamiltonian-monte-carlo/) or [NUTS](/no-u-turn-sampler/) is more efficient per gradient, but MALA is simpler to analyse and to tune.

## Pitfalls

- **Forgetting the Hastings factor.** With only $\pi(y)/\pi(x)$ in line L5, the chain is wrong.
- **Large steps in light tails.** Far from the mode, the drift $\frac h2\nabla\log\pi$ can be huge, the proposals land far out, and the chain stops moving. Start near the mode, or truncate the drift.
- **Tuning on the transient phase.** The rate 0.574 is for a chain in stationarity. During [burn-in](/burn-in/), a smaller $h$ may be needed.
- **Badly scaled targets.** As for random-walk Metropolis, one step size for all directions must fit the smallest scale. Precondition.

## Implementations

## History

Rossky, Doll and Friedman (1978) proposed "smart Monte Carlo" in chemistry: a Brownian dynamics step with the force as drift, corrected by a Metropolis test. Besag suggested the same idea for statistics in 1994, in a discussion of Grenander and Miller. Roberts and Tweedie (1996) named and analysed the Metropolis-adjusted Langevin algorithm, and showed how the unadjusted and adjusted chains can fail. Roberts and Rosenthal (1998) proved the optimal scaling with rate 0.574.

## References
