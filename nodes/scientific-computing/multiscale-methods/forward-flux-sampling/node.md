---
tag: 0GTKCK
kind: algorithm
slug: forward-flux-sampling
name: Forward flux sampling
area: scientific-computing/multiscale-methods
level: research
summary: Estimates rare transition rates by firing trial runs from a series of interfaces between two states and keeping those that reach the next interface.
model: real-ram
complexity:
  vars: {n_0: the length of the first run in steps, n: the number of interfaces after the first, M: the number of trial runs per interface, l: the mean length of a trial run in steps, G: the cost of one step, d: the number of coordinates of a state}
  time: {expected: O((n_0 + n M l) G)}
  space: {extra: O(M d)}
properties: {deterministic: false, randomized: true, exact: false, iterative: false, unbiased_given_first_run: true}
history:
  year: 2005
  people: [Rosalind J. Allen, Patrick B. Warren, Pieter Rein ten Wolde]
  note: Allen, Warren and ten Wolde gave forward flux sampling in 2005 for the switching of genetic networks, which are stochastic and not in equilibrium.
prereqs: [markov-chain, monte-carlo-integration]
see_also: [transition-path-sampling, subset-simulation, sequential-monte-carlo, importance-sampling, gillespie-algorithm, collective-variable, kinetic-monte-carlo]
sources:
  - paper: doi:10.1103/PhysRevLett.94.018104
    title: Rosalind J. Allen, Patrick B. Warren and Pieter Rein ten Wolde, Sampling rare switching events in biochemical networks, Physical Review Letters 94(1), 2005, 018104
    locator: the interfaces, the flux through the first interface and the product of the crossing probabilities
  - paper: doi:10.1063/1.2140273
    title: Rosalind J. Allen, Daan Frenkel and Pieter Rein ten Wolde, Simulating rare events in equilibrium or nonequilibrium stochastic systems, The Journal of Chemical Physics 124(2), 2006, 024102
    locator: the direct method and its variants, with a comparison of their efficiency
  - paper: doi:10.1088/0953-8984/21/46/463102
    title: Rosalind J. Allen, Chantal Valeriani and Pieter Rein ten Wolde, Forward flux sampling for rare event simulations, Journal of Physics Condensed Matter 21(46), 2009, 463102
    locator: the review of the method, the choice of the interfaces and the error analysis
---

Forward flux sampling (FFS) estimates the rate of a rare transition from a state $A$ to a state $B$ by splitting it into a chain of more likely steps. An order parameter $\lambda$ and interfaces $\lambda_0 < \lambda_1 < \cdots < \lambda_n$ separate the two states. One ordinary run in $A$ measures the flux $\Phi_{A,0}$ of trajectories that leave $A$ and cross $\lambda_0$, and stores the crossing points. From these points, trial runs estimate the probability to reach $\lambda_1$ before going back to $A$; the points where they reach $\lambda_1$ start the next stage, and so on. The rate is the product $k_{AB} = \Phi_{A,0} \prod_i P(\lambda_{i+1} | \lambda_i)$. FFS uses only forward simulation, so it works for dynamics that are not reversible and not in equilibrium, such as biochemical networks simulated with the [Gillespie algorithm](/gillespie-algorithm/).

## In plain words

Climbing a high wall in one jump almost never works. So mark ledges on the wall. First count how often climbers leave the ground and reach the lowest ledge. Then, from the climbers on that ledge, send many up and count how many reach the next ledge before falling back to the ground. Those who arrive become the starting group for the next ledge.

The chance to get to the top is the product of the chances from ledge to ledge. Each of these chances is not small, so a few hundred tries measure it well. The rate of reaching the top is the rate of reaching the first ledge times this product.

## The problem

The input is a dynamics given as a time step, an order parameter $\lambda$, a test for the state $A$ (with $\lambda < \lambda_0$ on $A$), interfaces $\lambda_0 < \cdots < \lambda_n$ with $B = \{\lambda \ge \lambda_n\}$, the length $n_0$ of the first run, and the number $M$ of trial runs per interface. The output is an estimate of $k_{AB}$, the number of transitions from $A$ to $B$ per unit of time spent in the region of $A$ (the time since the last visit to $A$ rather than to $B$), and, as a by-product, the trajectories that reach $B$. The method assumes that the dynamics is Markov in the variables that are stored at the interfaces.

## The algorithm

```pseudo id=main
FFS(x, step, λ, A, λ_0..λ_n, n_0, M)
L1  run n_0 steps from x in A; Φ ← (first crossings of λ_0 after a visit to A) / (time in the region of A); S_0 ← the crossing points
L2  for i = 0 to n - 1
L3      repeat M times: pick y uniformly at random from S_i
L4          run from y until λ(y) ≥ λ_{i+1} or y ∈ A
L5          if λ(y) ≥ λ_{i+1}: add y to S_{i+1}
L6      P_i ← |S_{i+1}| / M;  if P_i = 0 return 0
L7  return Φ P_0 P_1 ... P_{n-1}
```

Line L1 counts a crossing only on the first arrival at $\lambda \ge \lambda_0$ after the last visit to $A$, and counts time only in the region of $A$; a run that reaches $B$ stops counting until it returns to $A$. Line L4 is a plain forward run of the dynamics. A run that reaches $A$ fails; a run that jumps over several interfaces succeeds, and its end point is already past the next interface as well. Line L3 resamples the stored points with replacement, which keeps the product of line L7 unbiased. The points of $S_n$, with the trial runs that led to them traced back, give sample transition paths.

## Example

Take a Metropolis random walk on the states $0, 1, \ldots, 6$ with the energies $0, 2, 4, 5, 4, 2, 0$ at $\beta = 1$: propose $\pm 1$ with probability 1/2 each, reject a move off the ends, accept with $\min(1, e^{-\Delta E})$. Let $\lambda(x) = x$, $A = \{0\}$ and the interfaces $1, 2, \ldots, 6$, so $B = \{6\}$. For this walk everything is exact. With the committor $q$ (the probability to reach 6 before 0), $q(1) = 0.01756$, each crossing probability is $P(i+1 | i) = q(i)/q(i+1)$, which gives $0.1192, 0.2946, 0.5864, 0.8679, 0.9824$, the flux is $\Phi_{A,0} = \pi(0) p(0,1) / \sum_x \pi(x)(1 - q(x)) = 0.05848$ per step, and the rate is $k_{AB} = \Phi_{A,0}\, q(1) = 1.0270 \times 10^{-3}$ per step.

One run with $n_0 = 20000$, $M = 2000$ and `random.Random(1)` measured the flux 0.05789, the probabilities $0.1255, 0.2945, 0.576, 0.8705, 0.983$, and $k_{AB} = 1.055 \times 10^{-3}$, with 45195 steps of the walk. Over 20 seeds:

| $n_0$ | $M$ | mean estimate | relative standard deviation | largest relative error | steps per run |
|---|---|---|---|---|---|
| 2000 | 200 | $1.011 \times 10^{-3}$ | 0.24 | 0.50 | 4412 to 4727 |
| 2000 | 300 | $1.050 \times 10^{-3}$ | 0.21 | 0.44 | 5636 to 5985 |
| 20000 | 2000 | $1.024 \times 10^{-3}$ | 0.087 | 0.175 | 45003 to 45686 |

For comparison, a direct run of $10^6$ steps saw 537 transitions and gave $1.076 \times 10^{-3}$. With the 45000 steps of one FFS run, a direct run would see about 23 transitions, a relative error of about 0.2, against 0.087 for FFS. These are measurements for this walk; the gain grows as the transition becomes rarer.

## Correctness

The proof is in the correctness proof of this page. Every transition to $B$ starts with a first crossing of $\lambda_0$, and the excursion after a crossing at $y$ ends in $B$ with probability $u(y)$, the probability to reach $\lambda_n$ before $A$. So the rate is the flux times the average of $u$ over the crossing points, which is $\Phi_{A,0} P(\lambda_n | \lambda_0)$. To reach $\lambda_n$ the excursion must reach each interface in turn; by the strong Markov property at each interface, the expected product of the stage estimates $\hat P_i$, given the first run, is exactly the average of $u$ over $S_0$. So the estimate is unbiased given the first run, and consistent as $n_0$ grows. This needs the dynamics to be Markov in the stored state: if hidden variables, such as velocities that are not stored, carry memory across an interface, the restarted runs have the wrong law.

## Complexity

The first run costs $n_0$ steps, and each of the $n$ stages costs $M$ trial runs of mean length $l$, so the work is $O((n_0 + n M l) G)$ in the [real RAM](/real-ram/) model, with $O(M d)$ memory for the stored points. The variance of the probability estimate is about $\sum_i (1 - P_i) / (M P_i)$ in relative terms if the stages were independent; interfaces placed so that each $P_i$ is not small, and more trials where $P_i$ is small, reduce it. The trial runs of a stage are independent and run in parallel.

## Properties

- **Forward in time only.** No time reverse, no equilibrium and no detailed balance are needed.
- **Unbiased given the first run.** The product of the stage estimates has the right mean for any number of trials.
- **Paths as a by-product.** The successful trials, traced back, are sample transition paths.
- **Needs an order parameter.** The interfaces must separate $A$ from $B$; unlike [transition path sampling](/transition-path-sampling/), the order parameter is part of the method, although it does not need to be a good reaction coordinate.

## Variants and improvements

- **Branched growth.** Each point at an interface fires its own fixed number of trials, which builds a tree of paths and keeps their ancestry.
- **The Rosenbluth method.** A single path is grown through the interfaces with a weight, as in polymer growth.
- **Adaptive interfaces.** The interfaces are placed after a pilot run so that the probabilities $P_i$ are about equal.
- **[Subset simulation](/subset-simulation/)** and multilevel splitting are the same idea in reliability analysis and applied probability: a rare event as a product of conditional probabilities estimated by [sequential Monte Carlo](/sequential-monte-carlo/).
- **Transition interface sampling** uses the same interfaces with path sampling moves for reversible dynamics.

## When to use it

Use FFS for rare switching in stochastic systems that are not in equilibrium, such as genetic switches, and for nucleation and other rare events where a simple order parameter is available and the dynamics can be restarted from a stored state. Use [transition path sampling](/transition-path-sampling/) when the dynamics is reversible and no order parameter is known, and [kinetic Monte Carlo](/kinetic-monte-carlo/) when the rates of the elementary events are known.

## Pitfalls

- **Lost memory.** If the stored state at an interface does not include all the variables of the Markov dynamics, the trial runs start from the wrong distribution.
- **Interfaces that are too far apart.** If some $P_i$ is very small, few or no trials succeed, and the estimate has a large variance or is 0.
- **Few points at an interface.** All later stages descend from these points; if they are few, the later trials are strongly correlated and the error is larger than the binomial formula suggests.
- **Counting crossings wrongly.** Only the first crossing of $\lambda_0$ after a visit to $A$ counts, and the time in the region of $B$ must not be counted.
- **A first interface inside A.** The first interface must lie outside the state $A$, so that the trajectories that cross it are leaving.

## Implementations

## History

Allen, Warren and ten Wolde introduced forward flux sampling in 2005 to compute the switching rates of genetic toggle switches, which are stochastic and far from equilibrium, so that methods based on detailed balance did not apply. Allen, Frenkel and ten Wolde compared the direct method with the branched and Rosenbluth versions in 2006, and Allen, Valeriani and ten Wolde reviewed the method in 2009. The idea of splitting a rare event at intermediate levels goes back to the splitting methods of Monte Carlo for particle transport.

## References
