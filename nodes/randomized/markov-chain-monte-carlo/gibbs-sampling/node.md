---
tag: JKAGEE
kind: algorithm
slug: gibbs-sampling
name: Gibbs sampling
aliases:
- Gibbs sampler
- heat-bath sampling
- heat-bath algorithm
area: randomized/markov-chain-monte-carlo
level: intro
summary: Sample a multivariate distribution by redrawing one coordinate at a time from its conditional distribution given the others. Each update is a Metropolis-Hastings step that is always accepted.
solves: [sampling-from-stationary-distribution]
model: word-ram
complexity:
  vars: {T: the number of sweeps, d: the number of coordinates, k: the largest domain size of a coordinate, c: the cost of one evaluation of the unnormalized target}
  time: {worst: Θ(T d k c)}
  space: {extra: Θ(d + k)}
properties: {in_place: true, online: true, deterministic: false, recursive: false}
history:
  year: 1984
  people: [Stuart Geman, Donald Geman]
  note: Geman and Geman named the method and used it for image restoration in 1984. Gelfand and Smith brought it to Bayesian statistics in 1990.
prereqs: [metropolis-hastings, markov-chain]
see_also: [glauber-dynamics, slice-sampling, swendsen-wang, ising-model, hard-core-model, markov-random-field, acceptance-probability, mcmc-autocorrelation]
sources:
  - paper: doi:10.1109/TPAMI.1984.4767596
    title: Stuart Geman and Donald Geman, Stochastic relaxation, Gibbs distributions, and the Bayesian restoration of images, IEEE Transactions on Pattern Analysis and Machine Intelligence 6(6), 1984
    locator: pages 721 to 741 (the Gibbs sampler, its convergence for a positive distribution on a finite space, and annealing)
  - paper: doi:10.1080/01621459.1990.10476213
    title: Alan E. Gelfand and Adrian F. M. Smith, Sampling-based approaches to calculating marginal densities, Journal of the American Statistical Association 85(410), 1990
    locator: pages 398 to 409 (the Gibbs sampler for Bayesian marginal densities)
  - paper: doi:10.1063/1.1703954
    title: Roy J. Glauber, Time-dependent statistics of the Ising model, Journal of Mathematical Physics 4(2), 1963
    locator: pages 294 to 307 (single-spin flip dynamics of the Ising model)
  - book: isbn:9780387212395
    title: Christian P. Robert and George Casella, Monte Carlo Statistical Methods, second edition, Springer, 2004
    locator: Chapter 9 (the two-stage Gibbs sampler) and Chapter 10 (the multi-stage Gibbs sampler, scans, and the Gibbs sampler as Metropolis-Hastings)
  - book: isbn:9781470429621
    title: David A. Levin, Yuval Peres and Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, AMS, 2017
    locator: Section 3.3, Glauber dynamics
---

Gibbs sampling draws from a distribution $\pi$ on a product space $\mathcal{X}_1 \times \cdots \times \mathcal{X}_d$ by a [Markov chain](/markov-chain/) that redraws one coordinate at a time from its full conditional distribution $\pi(x_i \mid x_{-i})$. Each such update is a [Metropolis-Hastings](/metropolis-hastings/) step whose [acceptance probability](/acceptance-probability/) is always 1, so it leaves $\pi$ invariant. A *systematic scan* updates the coordinates in a fixed order; a *random scan* picks one coordinate uniformly at random at each step. The method needs no step size, but it can be very slow when the coordinates are strongly correlated.

## In plain words

You want samples of many variables at once, but you only know how to sample one variable when all the others are fixed. Gibbs sampling uses only that skill.

Start with any values. Pick one variable. Forget its value, and draw a new one from its distribution given the current values of all the other variables. Then do the same with the next variable, and go on round and round.

Each redraw keeps the right distribution: if the old values were a correct sample, the new values are a correct sample too. So after many rounds the values behave like samples from the joint distribution. When two variables are tied closely together, each one can only move a little while the other stays fixed, so the walk is slow.

## The problem

The input is an unnormalized target $\tilde\pi = Z\pi$ on $\mathcal{X} = \mathcal{X}_1 \times \cdots \times \mathcal{X}_d$, a start $x^{(0)}$ with $\tilde\pi(x^{(0)}) > 0$, a number of steps $T$, and a scan rule. The method needs a way to draw from each full conditional

$$\pi(v \mid x_{-i}) = \frac{\tilde\pi(x_1, \ldots, x_{i-1}, v, x_{i+1}, \ldots, x_d)}{\sum_{v'}\tilde\pi(x_1, \ldots, x_{i-1}, v', x_{i+1}, \ldots, x_d)}, \qquad x_{-i} = (x_j)_{j \ne i}.$$

On this page each $\mathcal{X}_i$ is finite, so the conditional is a table that we normalize. For continuous coordinates the sum becomes an integral, and the method needs a sampler for the conditional, for example a conjugate formula, [rejection sampling](/rejection-sampling/) or [slice sampling](/slice-sampling/). The output is a Markov chain $X_1, \ldots, X_T$ with $\pi$ as a stationary distribution. Pr, E and Var are probability, expectation and variance; $P$ is a transition matrix.

The model of randomness is one uniform real $u \in [0, 1)$ for each coordinate update (inverse transform on the conditional table), plus one uniform index in $\{1, \ldots, d\}$ for each random-scan step.

## The algorithm

```pseudo id=main
GIBBS-SAMPLING(π̃, x0, T, scan)               ▷ x = (x_1, …, x_d), each x_i in a finite set D_i
L1  x ← x0
L2  for t ← 1 to T do
L3      if scan = systematic then order ← (1, 2, …, d)
L4      else order ← (i) with i uniform in {1, …, d}
L5      for each i in order do
L6          draw v from π(· | x_{−i}), with Pr(v) ∝ π̃(x_1, …, x_{i−1}, v, x_{i+1}, …, x_d)
L7          x_i ← v
L8      X_t ← a copy of x
L9  return X_1, …, X_T
```

With the systematic scan, one step of the loop of line L2 is a *sweep*: it updates each coordinate once, in order. With the random scan, one step updates one coordinate, so $d$ random-scan steps cost about one sweep. Line L6 computes the $|D_i|$ weights of the candidate values, adds them, and draws by inverse transform: it takes the first value whose running total exceeds $u$ times the total. The draw ignores the old value of $x_i$, and nothing is ever rejected.

## Example

Take two binary variables with $\tilde\pi(0,0) = 4$, $\tilde\pi(0,1) = 1$, $\tilde\pi(1,0) = 2$, $\tilde\pi(1,1) = 3$, so $\pi = (0.4, 0.1, 0.2, 0.3)$ in the order $00, 01, 10, 11$. The conditionals are:

| given | conditional |
|---|---|
| $x_2 = 0$ | $\Pr(x_1 = 1) = 2/6 = 1/3$ |
| $x_2 = 1$ | $\Pr(x_1 = 1) = 3/4$ |
| $x_1 = 0$ | $\Pr(x_2 = 1) = 1/5$ |
| $x_1 = 1$ | $\Pr(x_2 = 1) = 3/5$ |

A systematic sweep from $x = (0, 0)$ with the uniforms $u = 0.70$ and then $u = 0.50$: the first update draws $x_1$ given $x_2 = 0$; since $0.70 \ge 2/3 = \Pr(x_1 = 0)$, it takes $x_1 = 1$. The second draws $x_2$ given $x_1 = 1$; since $0.50 \ge 2/5 = \Pr(x_2 = 0)$, it takes $x_2 = 1$. So $X_1 = (1, 1)$.

The exact kernels, with rows and columns in the order $00, 01, 10, 11$, are

$$P_{\mathrm{sys}} = \begin{pmatrix} 8/15 & 2/15 & 2/15 & 1/5 \\ 1/5 & 1/20 & 3/10 & 9/20 \\ 8/15 & 2/15 & 2/15 & 1/5 \\ 1/5 & 1/20 & 3/10 & 9/20 \end{pmatrix}, \qquad P_{\mathrm{rand}} = \begin{pmatrix} 11/15 & 1/10 & 1/6 & 0 \\ 2/5 & 9/40 & 0 & 3/8 \\ 1/3 & 0 & 11/30 & 3/10 \\ 0 & 1/8 & 1/5 & 27/40 \end{pmatrix}.$$

Both satisfy $\pi P = \pi$. The random scan is reversible. The systematic scan is not: $\pi(00)P_{\mathrm{sys}}(00, 01) = 0.4 \cdot 2/15 = 4/75$, but $\pi(01)P_{\mathrm{sys}}(01, 00) = 0.1 \cdot 1/5 = 1/50$. The rows of $P_{\mathrm{sys}}$ for $00$ and $10$ are equal, because the sweep first overwrites $x_1$.

**A slow case.** Let $\pi$ be the bivariate normal with unit variances and correlation $\rho$. Then $x_1 \mid x_2 \sim \mathcal{N}(\rho x_2, 1 - \rho^2)$, and symmetrically. One systematic sweep gives $x_1' = \rho x_2 + \sqrt{1 - \rho^2}\,\xi_1$ and $x_2' = \rho x_1' + \sqrt{1 - \rho^2}\,\xi_2$, so the sequence of second coordinates is the AR(1) process $x_2' = \rho^2 x_2 + \eta$ with $\operatorname{Var}\eta = 1 - \rho^4$. Its lag-$k$ [autocorrelation](/mcmc-autocorrelation/) is $\rho^{2k}$, and its integrated autocorrelation time is $(1 + \rho^2)/(1 - \rho^2)$. For $\rho = 0.99$ this is about $99.5$: a run of $10^5$ sweeps is worth about $1000$ independent draws.

## Correctness

**Theorem.** For each $i$, the single-coordinate kernel $K_i(x, y) = \pi(y_i \mid x_{-i})\,\mathbf{1}[y_{-i} = x_{-i}]$ is reversible with respect to $\pi$. Hence the random-scan kernel $\frac1d\sum_i K_i$ is reversible with respect to $\pi$, and the systematic-scan kernel $K_1K_2\cdots K_d$ leaves $\pi$ invariant.

The key identity is that for $y_{-i} = x_{-i}$, $\pi(x)K_i(x, y) = \pi(x)\pi(y)/\pi_{-i}(x_{-i})$, which is symmetric in $x$ and $y$; here $\pi_{-i}$ is the marginal of $x_{-i}$. Equivalently, $K_i$ is the Metropolis-Hastings kernel with proposal $Q(x, \cdot) = K_i(x, \cdot)$, and its ratio is $r = 1$. The full proof is in the proof file. Convergence needs more: if $\pi > 0$ on all of the finite product space, each scan is irreducible and aperiodic, so it converges to $\pi$ (Geman and Geman 1984). If $\pi$ has zeros, the chain can be reducible: with $\pi$ uniform on $\{(0,0), (1,1)\}$, no single-coordinate update can leave the start.

## Complexity

On finite domains, line L6 evaluates $\tilde\pi$ at $|D_i| \le k$ points and draws in $O(k)$ time. A sweep costs $\Theta(d k c)$, where $c$ is the cost of one evaluation of $\tilde\pi$, so $T$ sweeps cost $\Theta(T d k c)$. The extra space is the current state and one table of $k$ weights. For a [Markov random field](/markov-random-field/), $\tilde\pi(x)$ is a product of local factors, and the ratio of the candidates needs only the factors that touch $x_i$. For the [Ising model](/ising-model/) on a graph with $n$ vertices and $m$ edges, a sweep then costs $\Theta(n + m)$.

The mixing time depends on $\pi$. For a spin system on a graph of maximum degree $\Delta$ under a high-temperature condition, the random-scan chain ([Glauber dynamics](/glauber-dynamics/)) mixes in $O(n \log n)$ steps; at low temperature, or with near-deterministic constraints, it can need time exponential in $n$. See [Glauber dynamics](/glauber-dynamics/) and the [Ising model](/ising-model/) for the theorems.

## Properties

- **No rejection and no tuning.** There is no step size and no acceptance rate.
- **Needs the conditionals.** The method fits models where each conditional is a small table or a standard distribution, such as graphical models and conjugate Bayesian models.
- **The scans differ.** The random scan is reversible. The systematic scan is not reversible in general, but it leaves $\pi$ invariant. A forward sweep followed by a backward sweep is reversible.
- **Coordinate moves only.** The chain moves along the axes. Strong dependence between coordinates makes each move small, as in the Gaussian example.

## Variants and improvements

- **Blocked Gibbs.** Update a group of coordinates jointly from their joint conditional. This removes the slow mixing inside the block.
- **Collapsed Gibbs.** Integrate some variables out analytically and sample the rest.
- **Metropolis-within-Gibbs.** When a conditional cannot be sampled, replace line L6 by one [Metropolis-Hastings](/metropolis-hastings/) step that targets the conditional. The chain still leaves $\pi$ invariant.
- **Auxiliary variables.** [Slice sampling](/slice-sampling/) and [Swendsen-Wang](/swendsen-wang/) are Gibbs samplers on an extended space with an added variable.
- **Annealing.** Geman and Geman ran the sampler on $\pi^{1/\tau}$ with a decreasing temperature $\tau$ to find a maximum a posteriori image, as in [simulated annealing](/simulated-annealing/).

## When to use it

Use Gibbs sampling when the full conditionals are easy to sample and the coordinates are not too strongly dependent: discrete graphical models, the [Ising](/ising-model/) and [hard-core](/hard-core-model/) models at high temperature or low fugacity, hierarchical models with conjugate priors. When coordinates are strongly correlated, use blocking, a reparametrization, or a joint move such as [HMC](/hamiltonian-monte-carlo/). Near a phase transition of a spin model, a cluster method such as [Swendsen-Wang](/swendsen-wang/) can be much faster.

## Pitfalls

- **Using the old value in line L6.** The new $x_i$ is drawn from the conditional given $x_{-i}$ only. If the code reweights the candidates by anything that depends on the old $x_i$, the kernel is wrong.
- **Using stale values.** Within a sweep, each update must see the values already updated in this sweep. Updating all coordinates from the values at the start of the sweep (a "parallel" update) does not leave $\pi$ invariant in general. For the Ising model on a bipartite graph, a parallel update of all vertices of one color class at once is correct, because they are conditionally independent.
- **Zeros of $\pi$.** With hard constraints, the single-site chain can be reducible. Check irreducibility, or use blocked moves.
- **Calling the systematic scan reversible.** Tools that assume reversibility (for example spectral bounds stated for reversible chains) do not apply to it directly.

## Implementations

## History

Geman and Geman (1984) introduced the name and used the sampler with annealing for Bayesian image restoration with Markov random field priors. The same single-site update had been used in statistical physics as the heat-bath algorithm, and Glauber (1963) studied its continuous-time version for the Ising model. Gelfand and Smith (1990) showed its use for Bayesian marginal densities, which made it a standard tool of applied statistics.

## References
