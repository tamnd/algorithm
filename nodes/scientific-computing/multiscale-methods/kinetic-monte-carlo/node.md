---
tag: SFQPD9
kind: algorithm
slug: kinetic-monte-carlo
name: Kinetic Monte Carlo
aliases:
- Bortz-Kalos-Lebowitz algorithm
- n-fold way
- residence time algorithm
area: scientific-computing/multiscale-methods
level: core
summary: Simulates a system that moves by rare events with known rates. Each step draws an exponential waiting time from the total rate and picks one event with probability proportional to its rate.
model: real-ram
complexity:
  vars: {M: the number of possible events in the current state, N: the number of events in the run}
  time: {worst: O(N M)}
  space: {extra: O(M)}
properties: {deterministic: false, randomized: true, exact: true, iterative: true}
history:
  year: 1975
  people: [Alfred B. Bortz, Malvin H. Kalos, Joel L. Lebowitz]
  note: Bortz, Kalos and Lebowitz gave the rejection-free n-fold way for Ising spin systems in 1975. Gillespie gave the same direct method for chemical reactions in 1976. Fichthorn and Weinberg discussed in 1991 when the simulated time is a physical time.
prereqs: [markov-chain, inverse-transform-sampling]
see_also: [gillespie-algorithm, harmonic-transition-state-theory, molecular-dynamics, temperature-accelerated-dynamics, parallel-replica-dynamics, tau-leaping, alias-method, chemical-master-equation]
sources:
  - paper: doi:10.1016/0021-9991(75)90060-1
    title: A. B. Bortz, M. H. Kalos and J. L. Lebowitz, A new algorithm for Monte Carlo simulation of Ising spin systems, Journal of Computational Physics 17(1), 1975, 10-18
    locator: the n-fold way, with classes of spins by their flip rate and the time per step
  - paper: doi:10.1007/978-1-4020-5295-8_1
    title: Arthur F. Voter, Introduction to the kinetic Monte Carlo method, in Radiation Effects in Solids, NATO Science Series, Springer, 2007, 1-23
    locator: the residence time algorithm, the exponential waiting time and the rates from transition state theory
  - paper: doi:10.1063/1.461138
    title: Kristen A. Fichthorn and W. H. Weinberg, Theoretical foundations of dynamical Monte Carlo simulations, Journal of Chemical Physics 95(2), 1991, 1090-1096
    locator: the conditions under which the Monte Carlo time is a physical time (a Poisson process for each event)
  - paper: doi:10.1016/0021-9991(76)90041-3
    title: Daniel T. Gillespie, A general method for numerically simulating the stochastic time evolution of coupled chemical reactions, Journal of Computational Physics 22(4), 1976, 403-434
    locator: the direct method, the same algorithm for well-mixed chemical reactions
---

Kinetic Monte Carlo (KMC) simulates a system that moves from state to state by rare, separate events, each with a known rate, for example an atom that hops between sites of a crystal surface. In the current state it adds the rates of all possible events, draws the time to the next event from an exponential law with that total rate, and picks one event with probability proportional to its rate. Each step is one event, so KMC reaches seconds or hours of physical time, where [molecular dynamics](/molecular-dynamics/) with a step of about 1 fs needs about $10^{10}$ steps for one event that takes 25 microseconds. The algorithm is the same as the [Gillespie algorithm](/gillespie-algorithm/) of chemical kinetics; the difference is the setting: in KMC the states are atomic configurations and the rates usually come from [harmonic transition state theory](/harmonic-transition-state-theory/), not from reaction propensities.

## In plain words

Think of a crystal surface with a few loose atoms on it. Most of the time each atom only shakes in its site. Now and then one atom jumps to a next site. A simulation of the shaking wastes almost all its work.

Kinetic Monte Carlo skips the shaking. It needs a list of every jump that can happen now, with a rate for each one: how often that jump happens on average. A fast jump is more likely to come first. So the method picks a jump at random, with a chance in proportion to its rate. Then it moves the clock forward by a random waiting time. The waiting time is short when the total rate is high. Then the list changes, and the method repeats. The result is a random history of jumps with the correct statistics, if the list is complete and the rates are right.

## The problem

The input is a continuous-time Markov jump process given by its rates: for each state $x$, a finite list of events $j = 1, \ldots, M$ with rates $k_j(x) > 0$ (in $\mathrm{s}^{-1}$) and target states $y_j(x)$. The process stays in $x$ for a random time, then jumps to $y_j$, and the time and the choice obey

$$P(\text{event } j \text{ happens in } [t, t + dt) \mid \text{state } x \text{ at } t) = k_j(x)\, dt + o(dt).$$

The output is a sample path $(t_0, x_0), (t_1, x_1), \ldots$ of this process up to a time $t_{\mathrm{end}}$, and time averages along it. The probabilities $p(x, t)$ of the states solve the master equation $dp(y)/dt = \sum_x p(x) k_{x \to y} - p(y) \sum_z k_{y \to z}$ (see the [chemical master equation](/chemical-master-equation/)); KMC samples paths of this equation and does not solve it.

In materials, an event is a jump over a saddle of the potential energy, and its rate is $k = \nu \exp(-E_a / (k_B T))$ with a barrier $E_a$ and a prefactor $\nu$, often of order $10^{12}$ to $10^{13}\ \mathrm{s}^{-1}$. Here $k_B$ is the Boltzmann constant and $T$ the temperature.

## The algorithm

```pseudo id=main
KINETIC-MONTE-CARLO(x, EVENTS, t_end)
L1  t ← 0
L2  while t < t_end do
L3      (k_1, y_1), ..., (k_M, y_M) ← EVENTS(x)
L4      R ← k_1 + ... + k_M                         ▷ total escape rate of x
L5      if R = 0 then return                         ▷ no event is possible
L6      draw u_1 uniform in [0, 1) and u_2 uniform in (0, 1]
L7      Δt ← -ln(u_2) / R                            ▷ exponential waiting time
L8      if t + Δt ≥ t_end then add f(x) (t_end - t) to the average, t ← t_end, return
L9      add f(x) Δt to the average                   ▷ x holds during the wait
L10     j ← the smallest index with k_1 + ... + k_j > u_1 R
L11     t ← t + Δt, x ← y_j
L12     record (t, x)
L13 return x, t, the path and the time average of f
```

Line L7 is [inverse transform sampling](/inverse-transform-sampling/) of the exponential law with rate $R$: if $u_2$ is uniform on $(0, 1]$, then $P(-\ln u_2 / R > s) = P(u_2 < e^{-Rs}) = e^{-Rs}$. Line L10 picks event $j$ with probability $k_j / R$, because $u_1 R$ is uniform on $[0, R)$ and the interval of event $j$ has length $k_j$. Line L9 weights the observable $f$ with the time that the system stays in $x$, which is the correct weight for a time average. The two random numbers are independent, and so are the waiting time and the choice, as the proof shows.

The variant of Bortz, Kalos and Lebowitz groups the events into classes with equal rates, picks a class by its total rate and then a member uniformly. This is the same distribution with a shorter search.

## Example

**A two-state system by hand.** Let state A go to B with rate $k_{AB} = 1$ and B go to A with rate $k_{BA} = 3$, in units of $\mathrm{s}^{-1}$. Each state has one event, so line L10 always picks it, and only $u_2$ matters. Start in A at $t = 0$:

| step | state | $R$ | $u_2$ | $\Delta t = -\ln(u_2) / R$ | $t$ after the jump | new state |
|---|---|---|---|---|---|---|
| 1 | A | 1 | 0.5 | 0.693147 | 0.693147 | B |
| 2 | B | 3 | 0.9 | 0.035120 | 0.728268 | A |
| 3 | A | 1 | 0.3 | 1.203973 | 1.932241 | B |
| 4 | B | 3 | 0.6 | 0.170275 | 2.102515 | A |

The time in A is $0.693147 + 1.203973 = 1.897120$ of $2.102515$, a fraction of 0.9023 after four events. The exact long-time fraction is $k_{BA} / (k_{AB} + k_{BA}) = 3/4$, because the mean time in A is $1/k_{AB} = 1$ and the mean time in B is $1/k_{BA} = 1/3$. A run with `random.Random(1)` gives these fractions:

| $t_{\mathrm{end}}$ | events | fraction of time in A |
|---|---|---|
| 10 | 18 | 0.8420 |
| 100 | 151 | 0.7839 |
| 1000 | 1500 | 0.7562 |
| 10000 | 15109 | 0.7477 |

The error of a time average falls like $N^{-1/2}$ in the number $N$ of events, as for any [Monte Carlo integration](/monte-carlo-integration/).

**A choice among three events.** In a state with rates $1, 2, 3$, the total is $R = 6$. With $u_1 = 0.4$, line L10 looks for the first partial sum above $u_1 R = 2.4$: the sums are $1, 3, 6$, so it picks event 2. The waiting time has mean $1/R = 1/6$ and standard deviation $1/6$, whatever event follows.

**Why KMC is needed.** An adatom hop with $\nu = 10^{13}\ \mathrm{s}^{-1}$ and $E_a = 0.5$ eV at $T = 300$ K, where $k_B T = 0.025852$ eV, has the rate $k = 10^{13} e^{-0.5 / 0.025852} = 3.98 \times 10^{4}\ \mathrm{s}^{-1}$. The mean time between hops is $25.1$ microseconds, which is $2.5 \times 10^{10}$ MD steps of 1 fs. KMC does one step per hop. At $T = 600$ K the rate is $6.31 \times 10^{8}\ \mathrm{s}^{-1}$: the rates of activated events change by orders of magnitude with the temperature.

## Correctness

The claim is that the path is an exact sample of the Markov jump process, up to the quality of the random numbers and rounding. The key fact is the race of exponential clocks: if each event $j$ has an independent exponential clock with rate $k_j$, the first clock to ring rings at a time with the exponential law of rate $R = \sum_j k_j$, it is clock $j$ with probability $k_j / R$, and the time and the index are independent. Lines L6 to L10 draw exactly this pair. By the Markov property, the process after the jump starts afresh from $y_j$, so the loop repeats the same step. The full proof is below; it also shows that the time average of line L9 converges to the stationary average when the chain is irreducible and has finitely many states.

What the proof does not cover is the model. KMC is exact for the rate model it is given. If an event is missing from the catalog, or a rate is wrong, the path is a correct sample of a wrong process. Rates from harmonic transition state theory are an approximation with their own hypotheses.

## Complexity

In the [real RAM](/real-ram/) model, one step costs one call of EVENTS, $M$ additions for line L4 and up to $M$ additions and comparisons for line L10, so $\Theta(M)$ apart from EVENTS. A run of $N$ events costs $O(N M)$ and $O(M)$ extra space.

- **Search.** A binary tree of partial sums (a sum tree, or a [Fenwick tree](/fenwick-tree/)) gives line L10 in $O(\log M)$ time, and a change of one rate in $O(\log M)$ time.
- **Update.** On a lattice, one event changes only the rates of nearby sites, so the catalog update is $O(1)$ per step at fixed range, and a step costs $O(\log M)$ with the tree.
- **Physical time.** The mean step is $1/R$. If the fastest event is much faster than the events of interest, most steps go to the fast event and the run advances slowly. This is a property of the rates, not of the algorithm.

## Properties

- **Rejection free.** Each step makes one event. The older rejection method proposes an event with a fixed upper bound of the rates and rejects it with probability $1 - k_j / k_{\max}$; it gives the same process with more steps when the rates differ much.
- **Exact in time.** The waiting times are exponential, not the mean $1/R$. A fixed increment $1/R$ gives the correct mean time but the wrong distribution of times.
- **No time step.** There is no discretization error in time, unlike [tau-leaping](/tau-leaping/).
- **Randomized.** The output is a random path. Two runs with different seeds differ, and averages need many events.

## Variants and improvements

- **Lattice KMC.** The states are occupations of the sites of a fixed lattice, and the catalog is a short table of local moves with fixed barriers. This is the fastest and most common form.
- **On-the-fly or adaptive KMC.** The catalog is built in each new state by saddle searches, for example with the [dimer method](/dimer-method/), and rates come from [harmonic transition state theory](/harmonic-transition-state-theory/). The catalog may be incomplete, and the method gives a bound on what it misses only with extra assumptions.
- **[First reaction method](/first-reaction-method/).** Draw one exponential time for each event and take the smallest. This is the same distribution with $M$ random numbers per step.
- **Time-dependent rates.** If the rates change with time, for example in a temperature ramp, line L7 must solve $\int_t^{t + \Delta t} R(s)\, ds = -\ln u_2$ instead.
- **Accelerated dynamics.** [Parallel replica dynamics](/parallel-replica-dynamics/), [hyperdynamics](/hyperdynamics/) and [temperature accelerated dynamics](/temperature-accelerated-dynamics/) find the events by molecular dynamics instead of from a list.

## When to use it

Use KMC when the dynamics is a sequence of rare events whose types and rates you know, and the time scale of interest is far beyond molecular dynamics: diffusion and growth on surfaces, annealing of radiation damage, vacancy diffusion in alloys, catalysis. Use molecular dynamics when you do not know the events, or when the motion is not a sequence of separate events, for example in a liquid. Use [tau-leaping](/tau-leaping/) when many events fire in a short time and their exact order is not important.

## Pitfalls

- **A missing event.** The catalog of line L3 must hold every event that can happen. An event that is not in the list never happens, and nothing in the run shows this.
- **The logarithm of zero.** Line L6 must draw $u_2$ in $(0, 1]$, for example as $1 - u$ with $u$ in $[0, 1)$. With $u_2 = 0$, line L7 gives an infinite time.
- **A fixed time increment.** Writing $\Delta t = 1/R$ in line L7 keeps the mean time but gives wrong waiting time distributions and wrong time correlations.
- **Unweighted averages.** An average over the recorded states without the weights $\Delta t$ of line L9 is an average over events, not over time. It gives the wrong value: in the two-state example it gives 1/2, not 3/4.
- **The low barrier problem.** If two states are joined by a very fast event, the run flips between them at almost every step and the clock hardly moves. Merge such states into one, or use an accelerated variant.
- **Rates without detailed balance.** For a system in thermal equilibrium the rates must satisfy [detailed balance](/detailed-balance/) with respect to the Boltzmann distribution. Rates from barriers of the same saddle seen from both sides do; rates fitted one by one may not.

## Implementations

## History

Bortz, Kalos and Lebowitz published the n-fold way for Ising spin systems in 1975. It removes the rejected moves of the Metropolis method at low temperature by grouping the spins into classes by their flip rate. Gillespie published the same direct method for coupled chemical reactions in 1976. Fichthorn and Weinberg discussed in 1991 the conditions under which the simulated time is a physical time. Voter's 2007 chapter gives the method as it is used in materials science, with rates from transition state theory.

## References
