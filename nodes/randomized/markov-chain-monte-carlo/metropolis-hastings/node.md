---
tag: F19R05
kind: algorithm
slug: metropolis-hastings
name: Metropolis-Hastings algorithm
aliases:
- Metropolis algorithm
- Metropolis-Hastings sampler
area: randomized/markov-chain-monte-carlo
level: intro
summary: A Markov chain with stationary distribution π. Draw y from a proposal Q(x, ·) and move to y with probability min(1, π(y)Q(y, x) / (π(x)Q(x, y))), else stay at x.
solves: [sampling-from-stationary-distribution]
model: real-ram
complexity:
  vars: {T: the number of steps, c: the cost of one evaluation of the unnormalized target plus one proposal draw}
  time: {worst: Θ(T c)}
  space: {extra: Θ(1)}
properties: {in_place: true, online: true, deterministic: false, recursive: false}
history:
  year: 1953
  people: [Nicholas Metropolis, Arianna W. Rosenbluth, Marshall N. Rosenbluth, Augusta H. Teller, Edward Teller, W. Keith Hastings]
  note: Metropolis, the Rosenbluths and the Tellers gave the rule for a symmetric proposal in 1953. Hastings gave the general ratio for an asymmetric proposal in 1970.
prereqs: [markov-chain, stationary-distribution, detailed-balance]
see_also: [acceptance-probability, proposal-distribution, random-walk-metropolis, independence-sampler, gibbs-sampling, hamiltonian-monte-carlo, simulated-annealing, effective-sample-size]
sources:
  - paper: doi:10.1063/1.1699114
    title: Nicholas Metropolis, Arianna W. Rosenbluth, Marshall N. Rosenbluth, Augusta H. Teller and Edward Teller, Equation of state calculations by fast computing machines, Journal of Chemical Physics 21(6), 1953
    locator: pages 1087 to 1092 (the method with a symmetric move and the acceptance rule)
  - paper: doi:10.1093/biomet/57.1.97
    title: W. Keith Hastings, Monte Carlo sampling methods using Markov chains and their applications, Biometrika 57(1), 1970
    locator: pages 97 to 109 (the general acceptance ratio for an asymmetric proposal)
  - paper: doi:10.1214/aos/1176325750
    title: Luke Tierney, Markov chains for exploring posterior distributions, Annals of Statistics 22(4), 1994
    locator: Section 2 (the Metropolis-Hastings kernel on a general state space) and Section 3 (convergence under irreducibility and aperiodicity)
  - book: isbn:9780387212395
    title: Christian P. Robert and George Casella, Monte Carlo Statistical Methods, second edition, Springer, 2004
    locator: Chapter 7, The Metropolis-Hastings algorithm
  - book: isbn:9781470429621
    title: David A. Levin, Yuval Peres and Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, AMS, 2017
    locator: Section 3.2, Metropolis chains
---

The Metropolis-Hastings algorithm builds a [Markov chain](/markov-chain/) whose [stationary distribution](/stationary-distribution/) is a given target $\pi$. At each step it draws a candidate from a [proposal distribution](/proposal-distribution/) and accepts it with the [acceptance probability](/acceptance-probability/) $\min(1, r)$, where $r$ is the Metropolis-Hastings ratio. The chain satisfies [detailed balance](/detailed-balance/) with respect to $\pi$, and it needs $\pi$ only up to a constant factor. It is the general frame of most [MCMC](/sampling-from-stationary-distribution/) methods: [random-walk Metropolis](/random-walk-metropolis/), the [independence sampler](/independence-sampler/), [MALA](/metropolis-adjusted-langevin-algorithm/) and [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/) are special cases.

## In plain words

You want random samples from a distribution, but you can only compute how likely each state is relative to another state. You cannot list all states, and you do not know the total weight.

So you walk. From your current state, you suggest a new state by some easy random rule. If the new state is more likely, you usually go there. If it is less likely, you go there only with a probability equal to how much less likely it is, and otherwise you stay where you are and count the old state again. A correction term fixes the case where the rule suggests some moves more often than their reverse moves.

After many steps, the fraction of time that the walk spends in each state approaches the target probability of that state. The steps are not independent, so they carry less information than independent samples.

## The problem

The input is a target distribution $\pi$ on a state space $\mathcal{X}$, given as an unnormalized density or mass function $\tilde\pi = Z\pi$ with an unknown constant $Z > 0$, and a proposal kernel $Q$: for each $x$, a distribution $Q(x, \cdot)$ that we can draw from and whose density $Q(x, y)$ we can evaluate (with respect to the same reference measure as $\pi$: counting measure for a discrete space, Lebesgue measure on $\mathbb{R}^d$). The output is a sequence $X_1, X_2, \ldots, X_T$ that is a Markov chain with $\pi$ as a stationary distribution. Averages $\frac{1}{T}\sum_t f(X_t)$ then estimate $E_\pi[f]$. This is the problem of [sampling from a stationary distribution](/sampling-from-stationary-distribution/).

Notation on this page: $P$ is the transition kernel of the chain, $\pi$ its stationary distribution, Pr, E and Var are probability, expectation and variance, and $t_{\mathrm{mix}}$ is the [mixing time](/mixing-time/). The model of randomness is one draw from $Q(x, \cdot)$ and one uniform real $u \in [0, 1)$ for each step. In floating point, $u$ has finitely many values, so the acceptance probability is exact only up to the resolution of $u$ (about $2^{-53}$ for a double).

## The algorithm

```pseudo id=main
METROPOLIS-HASTINGS(π̃, Q, x0, T)          ▷ π̃ = Z·π, and π̃(x0) > 0
L1  x ← x0
L2  for t ← 1 to T do
L3      draw y from Q(x, ·)
L4      r ← π̃(y) Q(y, x) / (π̃(x) Q(x, y))    ▷ Z cancels
L5      draw u uniformly from [0, 1)
L6      if u < r then x ← y                  ▷ accept with probability min(1, r)
L7      X_t ← x                              ▷ a rejection repeats the old state
L8  return X_1, …, X_T
```

Line L3 draws the candidate. Line L4 computes the Metropolis-Hastings ratio. Since $y$ was drawn from $Q(x, \cdot)$, $Q(x, y) > 0$, and $\tilde\pi(x) > 0$ holds by induction from line L1, so the ratio is defined. If $Q(y, x) = 0$ or $\tilde\pi(y) = 0$, then $r = 0$ and the move is never accepted. Line L6 accepts with probability $\Pr(u < r) = \min(1, r)$. Line L7 records the state after the step, also when the step was rejected. This repeat is part of the method: dropping rejected steps from the output gives a wrong distribution.

When $Q$ is symmetric, $Q(x, y) = Q(y, x)$, the ratio is $\tilde\pi(y)/\tilde\pi(x)$. This is the original Metropolis rule of 1953. The factor $Q(y, x)/Q(x, y)$ is the Hastings correction of 1970.

In code, compute $\log r = \log\tilde\pi(y) + \log Q(y, x) - \log\tilde\pi(x) - \log Q(x, y)$ and accept when $\log r \ge 0$ or $u < e^{\log r}$. This avoids overflow and underflow of $\tilde\pi$ in high dimension. Keep $\log\tilde\pi(x)$ of the current state, so that each step evaluates the target once.

## Example

Take three states $0, 1, 2$ with $\tilde\pi = (1, 2, 3)$, so $\pi = (1/6, 1/3, 1/2)$. The proposal picks one of the two other states with probability $1/2$ each. It is symmetric, so $r = \tilde\pi(y)/\tilde\pi(x)$. Start at $x_0 = 0$.

| step | $x$ | $y$ | $r$ | $u$ | accept | $X_t$ |
|---|---|---|---|---|---|---|
| 1 | 0 | 2 | 3 | 0.62 | yes | 2 |
| 2 | 2 | 1 | 2/3 | 0.81 | no | 2 |
| 3 | 2 | 0 | 1/3 | 0.25 | yes | 0 |
| 4 | 0 | 1 | 2 | 0.97 | yes | 1 |
| 5 | 1 | 2 | 3/2 | 0.05 | yes | 2 |
| 6 | 2 | 1 | 2/3 | 0.40 | yes | 1 |

The full transition matrix has $P(x, y) = \frac12\min(1, \tilde\pi(y)/\tilde\pi(x))$ for $y \ne x$, and the rest of the row on the diagonal:

$$P = \begin{pmatrix} 0 & 1/2 & 1/2 \\ 1/4 & 1/4 & 1/2 \\ 1/6 & 1/3 & 1/2 \end{pmatrix}.$$

Detailed balance holds: $\pi(0)P(0, 1) = \frac16\cdot\frac12 = \frac1{12} = \frac13\cdot\frac14 = \pi(1)P(1, 0)$, and in the same way $\pi(0)P(0,2) = \pi(2)P(2,0) = \frac1{12}$ and $\pi(1)P(1,2) = \pi(2)P(2,1) = \frac16$. Then $\pi P = \pi$. For example, column 0 gives $\frac16\cdot 0 + \frac13\cdot\frac14 + \frac12\cdot\frac16 = \frac16$.

**The Hastings correction.** On the cycle of four states with a uniform target, let the proposal move one step clockwise with probability $2/3$ and one step counter-clockwise with probability $1/3$. A clockwise move has $r = (1/3)/(2/3) = 1/2$, and a counter-clockwise move has $r = 2$. So the chain moves each way with probability $1/3$ and stays with probability $1/3$: the correction makes the chain reversible.

## Correctness

**Theorem.** Let $P$ be the kernel of one step (lines L3 to L7). For all states $x \ne y$, $\pi(x)P(x, y) = \pi(y)P(y, x)$. So $\pi$ is a stationary distribution of $P$.

The key step is one line: for $x \ne y$,

$$\pi(x)Q(x, y)\min\!\Big(1, \frac{\pi(y)Q(y, x)}{\pi(x)Q(x, y)}\Big) = \min\big(\pi(x)Q(x, y), \pi(y)Q(y, x)\big),$$

and the right side is symmetric in $x$ and $y$. The full proof, with the general state space and the mass at rejection, is in the proof file. Stationarity alone does not give convergence. On a finite space, if $P$ is irreducible and aperiodic, then $P^t(x, \cdot) \to \pi$ for every start $x$ by the convergence theorem of [ergodic](/ergodicity/) chains. On a general space, Tierney (1994) gives convergence in total variation for $\pi$-almost every start when $P$ is $\pi$-irreducible and aperiodic.

## Complexity

Each step does one proposal draw, one evaluation of $\tilde\pi$ at $y$ (the value at $x$ is kept), at most two evaluations of $Q$, and one uniform draw. So $T$ steps take $\Theta(T c)$ time, where $c$ is the cost of one target evaluation and one proposal draw. The working space is $\Theta(1)$ states, plus the output if it is stored.

The time to a good sample is a different question. It is $T$ times the cost of a step, where $T$ must exceed the [burn-in](/burn-in/) and the run must be long enough for the [effective sample size](/effective-sample-size/) to reach the needed value. Both depend on the [mixing time](/mixing-time/) of $P$, which depends on $\pi$ and $Q$ and can be exponential in the dimension. No general bound holds. Proved bounds exist for special cases, for example the [independence sampler](/independence-sampler/) with bounded weights, and log-concave targets with [random-walk Metropolis](/random-walk-metropolis/) or [MALA](/metropolis-adjusted-langevin-algorithm/). For most applied runs only empirical diagnostics are available, and a diagnostic cannot prove convergence.

## Properties

- **Only ratios of $\pi$.** The constant $Z$ cancels in line L4. This is why the method fits Bayesian posteriors and Boltzmann distributions $\pi(x) \propto e^{-E(x)/kT}$, whose normalizing constant is unknown.
- **Reversible.** The chain satisfies detailed balance, so $P$ is self-adjoint on $L^2(\pi)$ and has real eigenvalues on a finite space.
- **Correlated output.** Consecutive states are dependent, and rejections repeat states. The variance of an average depends on the [autocorrelation](/mcmc-autocorrelation/) of the chain.
- **Free choice of $Q$.** Any proposal with $Q(x, y) > 0 \iff Q(y, x) > 0$ gives a correct kernel. The choice of $Q$ decides the speed, not the correctness.

## Variants and improvements

- **[Random-walk Metropolis](/random-walk-metropolis/).** $y = x + \sigma Z$ with a symmetric $Z$. The Hastings factor is 1.
- **[Independence sampler](/independence-sampler/).** $Q(x, y) = q(y)$ does not depend on $x$.
- **[Gibbs sampling](/gibbs-sampling/).** The proposal is the full conditional of one coordinate, and $r = 1$ always.
- **[MALA](/metropolis-adjusted-langevin-algorithm/) and [HMC](/hamiltonian-monte-carlo/).** The proposal uses the gradient of $\log\pi$. HMC proposes the end of a simulated trajectory.
- **Other acceptance rules.** Barker's rule $r/(1 + r)$ also gives detailed balance, but by Peskun's theorem it gives a larger asymptotic variance. See [acceptance probability](/acceptance-probability/).
- **Moves between spaces of different dimension.** [Reversible-jump MCMC](/reversible-jump-mcmc/) adds a Jacobian factor to $r$.
- **Several temperatures.** [Parallel tempering](/parallel-tempering/) runs chains for $\pi^{\beta}$ and swaps their states.
- **Optimization.** [Simulated annealing](/simulated-annealing/) runs the Metropolis rule with a temperature that decreases, to find a minimum of $E$, not to sample.

## When to use it

Use Metropolis-Hastings when you can evaluate $\tilde\pi$ but cannot sample $\pi$ directly, for example a posterior with an unknown normalizing constant. If you can sample $\pi$ directly, or by [rejection sampling](/rejection-sampling/) with a good envelope, do that: independent samples are better than a chain. If the full conditionals are easy to sample, [Gibbs sampling](/gibbs-sampling/) needs no tuning. On a smooth density in many dimensions, use a gradient method such as [HMC](/hamiltonian-monte-carlo/) or [NUTS](/no-u-turn-sampler/). For a target with well separated modes, plain MH is slow, and [parallel tempering](/parallel-tempering/) helps.

## Pitfalls

- **Dropping the rejected steps.** Line L7 must record $x$ also after a rejection. A chain that outputs only accepted states has the wrong distribution.
- **Forgetting the Hastings factor.** With an asymmetric $Q$, the ratio $\tilde\pi(y)/\tilde\pi(x)$ in line L4 gives a wrong stationary distribution. Use the full ratio $\tilde\pi(y)Q(y, x) / (\tilde\pi(x)Q(x, y))$.
- **Overflow.** For a density with $10^3$ factors, $\tilde\pi$ underflows to 0. Compute line L4 in logarithms.
- **Recomputing with new randomness.** If $\tilde\pi(x)$ is an estimate with random noise, recomputing it at each step breaks the proof. Keep the stored value for the current state (this is the pseudo-marginal method).
- **A bad start.** If $\tilde\pi(x_0) = 0$, line L4 divides by 0. Start in the support.
- **Trusting one chain.** A chain that has not found a second mode looks converged. Run several chains from dispersed starts and use the [Gelman-Rubin diagnostic](/gelman-rubin-diagnostic/), but no diagnostic proves convergence.

## Implementations

## History

Metropolis, A. Rosenbluth, M. Rosenbluth, A. Teller and E. Teller published the method in 1953, to compute the equation of state of a system of hard disks on the MANIAC computer at Los Alamos. Their moves were symmetric, and they accepted a move with probability $\min(1, e^{-\Delta E/kT})$. Hastings (1970) gave the general ratio for asymmetric proposals and put the method into statistics. Tierney (1994) gave the theory of the method on general state spaces, with conditions for convergence and central limit theorems.

## References
