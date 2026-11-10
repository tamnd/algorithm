---
tag: 8S8XNZ
kind: algorithm
slug: hamiltonian-monte-carlo
name: Hamiltonian Monte Carlo
aliases:
- HMC
- hybrid Monte Carlo
area: randomized/markov-chain-monte-carlo
level: advanced
summary: Adds a Gaussian momentum p, runs L leapfrog steps of Hamiltonian dynamics, flips p and accepts with probability min(1, e^(−ΔH)). It makes long moves that are still accepted.
solves: [sampling-from-stationary-distribution]
model: real-ram
complexity:
  vars: {T: the number of iterations, L: the number of leapfrog steps per iteration, d: the dimension, c: the cost of one gradient of the log target}
  time: {worst: Θ(T L (d + c))}
  space: {extra: Θ(d)}
properties: {in_place: true, online: true, deterministic: false, recursive: false}
history:
  year: 1987
  people: [Simon Duane, Anthony D. Kennedy, Brian J. Pendleton, Duncan Roweth, Radford M. Neal]
  note: Duane, Kennedy, Pendleton and Roweth introduced hybrid Monte Carlo for lattice field theory in 1987. Neal brought it to statistics in the 1990s and wrote the standard review in 2011.
prereqs: [hamiltonian-dynamics, metropolis-hastings]
see_also: [no-u-turn-sampler, metropolis-adjusted-langevin-algorithm, random-walk-metropolis, verlet-integration, detailed-balance, effective-sample-size, gibbs-sampling]
sources:
  - paper: doi:10.1016/0370-2693(87)91197-X
    title: Simon Duane, A. D. Kennedy, Brian J. Pendleton and Duncan Roweth, Hybrid Monte Carlo, Physics Letters B 195(2), 1987
    locator: pages 216 to 222 (molecular dynamics steps with a Metropolis test, exact for any step size)
  - book: isbn:9781420079418
    title: Steve Brooks, Andrew Gelman, Galin L. Jones and Xiao-Li Meng (editors), Handbook of Markov Chain Monte Carlo, Chapman and Hall/CRC, 2011
    locator: Chapter 5, Radford M. Neal, MCMC using Hamiltonian dynamics, pages 113 to 162 (the algorithm, the proof of detailed balance, tuning, and scaling with dimension)
  - book: isbn:9780387947242
    title: Radford M. Neal, Bayesian Learning for Neural Networks, Lecture Notes in Statistics 118, Springer, 1996
    locator: the chapter on Monte Carlo implementation (hybrid Monte Carlo for neural network posteriors)
  - paper: doi:10.3150/12-BEJ414
    title: Alexandros Beskos, Natesh Pillai, Gareth Roberts, Jesus-Maria Sanz-Serna and Andrew Stuart, Optimal tuning of the hybrid Monte Carlo algorithm, Bernoulli 19(5A), 2013
    locator: pages 1501 to 1534 (step size of order d^(-1/4) and the acceptance rate 0.651 for product targets)
---

Hamiltonian Monte Carlo (HMC) is a [Metropolis-Hastings](/metropolis-hastings/) method that uses the gradient of $\log\pi$ to make long moves. It treats the state $q \in \mathbb{R}^d$ as the position of a particle with potential energy $U(q) = -\log\tilde\pi(q)$, adds a momentum $p \sim \mathcal{N}(0, I)$, and follows [Hamiltonian dynamics](/hamiltonian-dynamics/) for $L$ leapfrog steps of size $\varepsilon$. The end point, with its momentum flipped, is the proposal. It is accepted with probability $\min(1, e^{H(q, p) - H(q', p')})$, where $H = U + |p|^2/2$. Leapfrog keeps volume and is reversible, so this simple test makes the chain exactly $\pi$-invariant for every $\varepsilon$ and $L$. Leapfrog nearly keeps $H$, so the acceptance probability stays high even for proposals far from $q$. HMC was introduced by Duane, Kennedy, Pendleton and Roweth (1987) as hybrid Monte Carlo, and Neal (2011) is the standard account. The [No-U-Turn sampler](/no-u-turn-sampler/) chooses $L$ automatically.

## In plain words

Picture the target as a landscape where likely places are low. To move, you give a ball at your current point a random kick and let it roll for a while. It speeds up downhill and slows uphill, so it travels far but stays in low areas. Where it stops is the proposal.

The computer moves the ball in small steps, so the energy at the end is a little off. A final test accepts or rejects the move based on this energy error. The test makes the method exact, and because the error is small, almost all moves are accepted. The cost is that you need the slope of the landscape at every small step.

## The problem

The input is a function $\log\tilde\pi$ with $\tilde\pi = Z\pi$ positive and differentiable on $\mathbb{R}^d$, its gradient, a start $q_0$, a step size $\varepsilon > 0$, a number of leapfrog steps $L \ge 1$ and a number of iterations $T$. The output is a Markov chain $X_1, \ldots, X_T$ with $\pi$ as a stationary distribution; this is [sampling from a stationary distribution](/sampling-from-stationary-distribution/). The mass matrix is the identity here. A general mass matrix $M$ is the same as running this algorithm on the linearly transformed target. The model of randomness is $d$ standard normal reals and one uniform real in $[0, 1)$ per iteration.

## The algorithm

```pseudo id=main
HAMILTONIAN-MONTE-CARLO(log π̃, ∇log π̃, q0, ε, L, T)
L1  q ← q0
L2  for t ← 1 to T do
L3      draw p ~ N(0, I_d)
L4      (q', p') ← (q, p)
L5      repeat L times                          ▷ leapfrog for H(q, p) = −log π̃(q) + |p|²/2
L6          p' ← p' + (ε/2) ∇log π̃(q')
L7          q' ← q' + ε p'
L8          p' ← p' + (ε/2) ∇log π̃(q')
L9      p' ← −p'                                ▷ makes the proposal map an involution
L10     draw u uniformly from [0, 1)
L11     if u < exp(H(q, p) − H(q', p')) then q ← q'
L12     X_t ← q
L13 return X_1, …, X_T
```

The gradient at the end of one leapfrog step is the gradient at the start of the next, so an implementation computes $L + 1$ gradients per iteration, not $2L$. The flip in line L9 does not change $H$, and the next iteration draws a fresh $p$, so the flip has no effect on the output. It is there to make the proof work. Line L11 compares logarithms in code.

## Example

Take $\pi = \mathcal{N}(0, 1)$, so $H(q, p) = (q^2 + p^2)/2$, with $\varepsilon = 1/2$ and $L = 4$, from $q_0 = 1$. The leapfrog values are exact fractions; the table rounds them.

| iteration | $q$ | drawn $p$ | $q'$ after 4 steps | $\Delta H = H' - H$ | $\min(1, e^{-\Delta H})$ | $u$ | $X_t$ |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 0 | $-223/512 = -0.4355$ | $-0.0253$ | 1 | 0.5 | $-0.4355$ |
| 2 | $-0.4355$ | 1.5 | 1.5842 | 0.0725 | 0.9301 | 0.95 | $-0.4355$ |
| 3 | $-0.4355$ | $-0.8$ | $-0.5540$ | 0.0037 | 0.9963 | 0.2 | $-0.5540$ |

The trajectory length is $L\varepsilon = 2$, so iteration 1 moves from 1 to $-0.44$; the exact flow would give $\cos 2 = -0.416$. The energy errors are a few hundredths, so acceptance probabilities are near 1. Iteration 2 proposes a long move, from $-0.44$ to $1.58$, and is rejected only because $u = 0.95$ is above $0.93$. A [random-walk Metropolis](/random-walk-metropolis/) step of that length would be accepted much less often.

## Correctness

**Theorem.** For every $\varepsilon > 0$ and $L \ge 1$, the chain $(X_t)$ has $\pi$ as a stationary distribution. More precisely, each iteration leaves the joint density $\bar\pi(q, p) \propto \tilde\pi(q)e^{-|p|^2/2}$ invariant, and its $q$-marginal is $\pi$.

The proof is in the proof file. Each iteration is two moves. Line L3 replaces $p$ by a fresh draw from its conditional law under $\bar\pi$, which is a [Gibbs](/gibbs-sampling/) step and keeps $\bar\pi$. Lines L4 to L11 are a Metropolis-Hastings step with a deterministic proposal $z \mapsto G(z)$, where $G = F \circ \Psi_\varepsilon^L$ is $L$ leapfrog steps followed by the momentum flip $F$. By the properties shown on the [Hamiltonian dynamics](/hamiltonian-dynamics/) page, $G$ is its own inverse and has Jacobian determinant 1. For such a map, accepting with probability $\min(1, \bar\pi(G(z))/\bar\pi(z)) = \min(1, e^{H(z) - H(G(z))})$ gives [detailed balance](/detailed-balance/) by a change of variables. Without the flip, $\Psi_\varepsilon^L$ is not an involution, and the reverse move would not be proposed.

Invariance is not convergence. HMC can fail to be ergodic for special choices of $\varepsilon$ and $L$. On $\mathcal{N}(0, 1)$ with $\varepsilon = \sqrt2$ and $L = 2$, two leapfrog steps map $(q, p)$ to $(-q, -p)$ exactly, so every proposal is accepted and the chain only alternates between $q_0$ and $-q_0$. Drawing $\varepsilon$ or $L$ at random at each iteration removes such resonances. Under smoothness and tail conditions, HMC is geometrically ergodic (Livingstone, Betancourt, Byrne and Girolami 2019 give such conditions).

## Complexity

One iteration costs $L + 1$ gradient evaluations, one target evaluation and $O(Ld)$ other work, so $T$ iterations cost $\Theta(TL(d + c))$ time. The memory is $\Theta(d)$ for $q$, $p$ and one gradient.

**Scaling with dimension.** For a product target $\pi_d(q) = \prod_i f(q_i)$ with smooth $f$, Beskos et al. (2013) showed that the step size must shrink like $\varepsilon = \ell d^{-1/4}$ to keep the acceptance rate bounded away from 0, and that the efficiency is best when about $65.1\%$ of proposals are accepted. With a fixed trajectory length $L\varepsilon$, this needs $O(d^{1/4})$ leapfrog steps for each nearly independent draw. Under similar product hypotheses, [random-walk Metropolis](/random-walk-metropolis/) needs $O(d)$ steps and [MALA](/metropolis-adjusted-langevin-algorithm/) needs $O(d^{1/3})$ steps. Each step of all three costs $O(d)$ plus one evaluation.

## Properties

- **Exact for any step size.** The leapfrog error affects only the acceptance rate, not the stationary distribution.
- **Needs gradients.** The target must be differentiable, and $\nabla\log\tilde\pi$ must be computed, usually by automatic differentiation.
- **Non-diffusive.** A trajectory moves in a consistent direction for time $L\varepsilon$, so the distance covered grows linearly in $L$ until the trajectory turns back. Random-walk methods cover only the square root of the number of steps.
- **Two tuning parameters.** $\varepsilon$ controls the energy error and the acceptance rate. $L\varepsilon$ controls how far a proposal goes. Too short trajectories behave like random walks, and too long ones waste work by coming back.
- **Reversible in $q$.** Because the momentum is drawn fresh at each iteration, the chain $(X_t)$ on positions is reversible with respect to $\pi$. The proof file shows this.

## Variants and improvements

- **[The No-U-Turn sampler](/no-u-turn-sampler/)** (Hoffman and Gelman 2014) builds the trajectory by doubling until it starts to turn back, so $L$ need not be chosen. With dual averaging for $\varepsilon$, it is the default in Stan and PyMC.
- **Mass matrix.** A kinetic energy $p^\top M^{-1}p/2$ with $M^{-1}$ close to the covariance of $\pi$ makes the target look isotropic to the dynamics. It is usually estimated during [burn-in](/burn-in/).
- **[MALA](/metropolis-adjusted-langevin-algorithm/).** HMC with $L = 1$ is MALA with step size $\varepsilon^2$.
- **Partial momentum refreshment** (Horowitz 1991). Replace $p$ by $\alpha p + \sqrt{1 - \alpha^2}\,\xi$ instead of a fresh draw, and do not undo the flip after a rejection.
- **Riemannian manifold HMC** (Girolami and Calderhead 2011). A position-dependent mass matrix, with an implicit integrator, adapts to the local curvature.
- **Higher-order and split integrators.** Other symmetric volume-preserving integrators also give valid HMC, as long as the proposal map is an involution with Jacobian 1.

## When to use it

Use HMC, usually as NUTS, for smooth targets with tens to many thousands of continuous parameters, such as Bayesian hierarchical models and regression models. It needs gradients, so it does not apply directly to discrete parameters, which must be summed out or updated by other moves. It also struggles with targets whose curvature changes strongly from place to place, such as the funnel shapes of some hierarchical models, and with well-separated modes, where [parallel tempering](/parallel-tempering/) can help.

## Pitfalls

- **Too large a step size.** The leapfrog method is unstable when $\varepsilon$ is larger than about 2 divided by the square root of the largest eigenvalue of the Hessian of $U$ (exactly 2 for $\mathcal{N}(0, 1)$). Then the energy error explodes and nearly all proposals are rejected. Software reports such trajectories as divergent transitions, and they often point to regions the chain cannot explore.
- **A fixed, resonant trajectory length.** As in the example of the correctness section, fixed $\varepsilon$ and $L$ can make the chain periodic or slow on a Gaussian target. Jitter $\varepsilon$ or $L$.
- **Wrong gradients.** An error in $\nabla\log\tilde\pi$ does not change the test of line L11, so the chain still targets $\pi$, but the acceptance rate drops for no clear reason. Check gradients against finite differences.
- **Forgetting the flip in a variant.** In variants that keep the momentum between iterations, the flip matters, and leaving it out gives the wrong target.
- **Discontinuous targets.** At a jump of $\log\tilde\pi$, the gradient gives no information, the energy error is large, and the acceptance rate drops.

## Implementations

## History

Duane, Kennedy, Pendleton and Roweth (1987) introduced hybrid Monte Carlo for simulations of lattice quantum chromodynamics. The name "hybrid" refers to the mix of molecular dynamics and a Monte Carlo test, which made the dynamics exact. Neal used the method for Bayesian neural networks in his 1996 book and wrote the review that made it standard in statistics (Neal 2011, in the Handbook of Markov Chain Monte Carlo). Beskos et al. (2013) proved the scaling with dimension. Hoffman and Gelman (2014) introduced the No-U-Turn sampler, which made HMC usable without hand tuning.

## References
