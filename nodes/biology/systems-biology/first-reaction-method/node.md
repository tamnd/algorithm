---
tag: 4TMPNZ
kind: algorithm
slug: first-reaction-method
name: First reaction method
aliases:
- Gillespie first reaction method
area: biology/systems-biology
level: core
summary: Exact stochastic simulation that draws a tentative firing time for every reaction and fires the earliest, equivalent to the direct method.
model: real-ram
complexity:
  vars: {n: the number of species, m: the number of reactions, N: the expected number of reaction events in the run}
  time: {expected: Θ(N (m + n))}
  space: {extra: Θ(n + m)}
properties: {deterministic: false, randomized: true, exact: true, recursive: false}
history:
  year: 1976
  people: [Daniel T. Gillespie]
  note: Gillespie gave the first reaction method next to the direct method in his 1976 paper in the Journal of Computational Physics, and showed that the two sample the same law.
prereqs: [chemical-master-equation]
see_also: [gillespie-algorithm, next-reaction-method, tau-leaping, kinetic-monte-carlo, event-driven-simulation, inverse-transform-sampling, priority-queue, finite-state-projection]
sources:
  - paper: doi:10.1016/0021-9991(76)90041-3
    title: Daniel T. Gillespie, A general method for numerically simulating the stochastic time evolution of coupled chemical reactions, Journal of Computational Physics 22(4), 1976, 403-434
    locator: the first reaction method and the proof that it samples the reaction probability density function
  - paper: doi:10.1021/jp993732q
    title: Michael A. Gibson and Jehoshua Bruck, Efficient exact stochastic simulation of chemical systems with many species and many channels, Journal of Physical Chemistry A 104(9), 2000, 1876-1889
    locator: the discussion of the first reaction method as the starting point of the next reaction method
  - book: isbn:9781138549289
    title: Darren J. Wilkinson, Stochastic Modelling for Systems Biology, 3rd edition, CRC Press, 2018
    locator: the chapter on stochastic simulation algorithms (the first reaction method)
---

The first reaction method draws exact sample paths of the jump process of the [chemical master equation](/chemical-master-equation/), like the direct method of the [Gillespie algorithm](/gillespie-algorithm/), but it organizes each step in another way. In every step it gives each reaction its own exponential clock, with the rate equal to the reaction's current propensity, and fires the reaction whose clock rings first. The time of the event is the smallest clock. The minimum of independent exponential clocks is exponential with the sum of the rates, and the index of the minimum has probabilities proportional to the rates, so the step has exactly the law of a step of the direct method. Gillespie gave both methods in the same 1976 paper. The first reaction method costs up to $m$ random numbers per event for $m$ reactions, against 2 for the direct method, so it is rarely the fastest choice. Its value is as the basis of the [next reaction method](/next-reaction-method/), which keeps the clocks and reuses them.

## In plain words

Every kind of reaction in the cell gets its own alarm clock. A reaction that is likely to happen soon gets a clock that tends to ring early. Set all the clocks at random, see which one rings first, and let that reaction happen. Move time forward to that moment and change the counts.

Now the counts are different, so the chances have changed. Throw all the clocks away, set new ones for the new counts, and look again for the first to ring. Keep going until you reach the end time.

This gives exactly the same kind of story as spinning a wheel to pick the reaction, but it needs one random number for every kind of reaction, every time.

## The problem

**Input.** A network with $n$ species and $m$ reactions: change vectors $\nu_j \in \mathbb{Z}^n$ and propensity functions $a_j(x) \ge 0$; a start state $x_0$; an end time $T$; a source of random numbers.

**Output.** Event times and the states just after them, with the same law as the Markov jump process $X$ of the chemical master equation on $[0, T]$. The state at $T$ is the last recorded state.

The next reaction of $X$ from state $x$ comes after a time $\tau$ and is reaction $J$, with the joint density $a_j(x) e^{-a_0(x) s}$, where $a_0 = \sum_j a_j$. The method samples this density by a minimum of clocks.

## The algorithm

```pseudo id=main
FIRST-REACTION(x0, ν, a, T)
L1  t ← 0; x ← x0; record (0, x)
L2  loop
L3      compute a_j(x) for j = 1, ..., m
L4      best ← ∞; μ ← none
L5      for j ← 1 to m with a_j(x) > 0 do
L6          τ_j ← an exponential random number with rate a_j(x)
L7          if τ_j < best then best ← τ_j; μ ← j
L8      if μ = none then return the record
L9      if t + best > T then return the record
L10     t ← t + best; x ← x + ν_μ
L11     record (t, x)
```

Line L5 skips the reactions with a zero propensity: their clocks are infinite, and they cannot fire. Line L8 stops when no reaction can fire. Line L9 stops without firing when the first clock rings after $T$, so the current state is the state at $T$.

## Example

Take immigration-death again: $R_1: \emptyset \to X$ with $a_1 = 10$, and $R_2: X \to \emptyset$ with $a_2 = x$. Start from $x_0 = 2$ and draw the clocks with Python's `random.Random(1)`, $R_1$ first.

| step | $a_1, a_2$ | $\tau_1$ | $\tau_2$ | fires | $t$ after | $x$ after |
|---|---|---|---|---|---|---|
| 1 | 10, 2 | 0.0144 | 0.9401 | $R_1$ | 0.0144 | 3 |
| 2 | 10, 3 | 0.1443 | 0.0982 | $R_2$ | 0.1126 | 2 |
| 3 | 10, 2 | 0.0684 | 0.2985 | $R_1$ | 0.1810 | 3 |
| 4 | 10, 3 | 0.1054 | 0.5182 | $R_1$ | 0.2864 | 4 |
| 5 | 10, 4 | 0.0099 | 0.0072 | $R_2$ | 0.2936 | 3 |

In step 2 the death clock $0.0982$ rings before the immigration clock $0.1443$, so a molecule dies at $0.0144 + 0.0982 = 0.1126$. The immigration clock of step 2 is then thrown away, and step 3 draws a new one. The path is not the one the direct method gives with the same seed (it fires $R_2$ first there), because the two methods use the random numbers in another way. The law is the same: the tests of the implementation check the Binomial law of pure death from 100 molecules (mean 36.787944 and variance 23.254416 at $t = 1$), the [Poisson](/poisson-distribution/) laws of immigration-death, and the histogram of a dimerization network against runs of the direct method.

## Correctness

Let $E_j$ be independent exponentials with rates $a_j > 0$, and let $S = \min_j E_j$ with index $M$. The event $\{M = j, S \in [s, s + ds)\}$ is the event that $E_j$ lands in $[s, s + ds)$ and every other clock is later than $s$, with probability $a_j e^{-a_j s} ds \prod_{k \ne j} e^{-a_k s} = a_j e^{-a_0 s} ds$. This is the next reaction density of $X$. So $S$ is exponential with rate $a_0$, $M = j$ with probability $a_j / a_0$, and they are independent, as in the direct method. Each step draws fresh clocks and depends on the past only through $x$, so by induction on the events the path has the law of $X$. The full proof is below.

## Complexity

- **Per event.** Line L3 computes $m$ propensities, lines L5 to L7 draw up to $m$ exponentials and keep the minimum, and line L10 changes up to $n$ counts. So a step costs $\Theta(m + n)$ work, like the direct method, but with up to $m$ logarithms instead of one.
- **Random numbers.** A step uses one number per reaction with a positive propensity, so a run with $N$ events uses up to $m(N + 1)$ numbers, against $2N + 1$ for the direct method. For a network with 1000 reactions this is the dominant cost.
- **Per run.** The number of events has the same law as for the direct method, with mean $\int_0^T \mathbb{E}[a_0(X(t))]\, dt$. The expected time is $\Theta(\mathbb{E}[N](m + n))$.
- **Space.** $\Theta(n + m)$, plus the record.

## Properties

- **Exact.** The paths have the law of the jump process of the chemical master equation, with no step size and no bias.
- **Same law as the direct method.** For the same network and start, the first reaction method and the direct method give the same distribution of paths. For the same seed, they give different paths.
- **Natural for clocks.** Each reaction has its own clock. This makes the method easy to extend to events that are not exponential, for example a reaction with a fixed delay, where a clock for the delayed completion goes into the same minimum.
- **Waste.** All the clocks except one are thrown away at each step, even for reactions whose propensities did not change. By the memoryless property of the exponential law, these clocks are still valid, which is the idea of the next reaction method.

## Variants and improvements

- **Next reaction method.** Keep the clocks of the reactions that did not fire, store absolute firing times in an [indexed priority queue](/indexed-priority-queue/), and change only the clocks whose propensities change, by rescaling ([next reaction method](/next-reaction-method/), Gibson and Bruck 2000). It uses one random number per event.
- **Direct method.** Draw the total waiting time and the reaction separately, with two random numbers per event ([Gillespie algorithm](/gillespie-algorithm/)).
- **Delays.** Put the completion times of delayed reactions in the same set of clocks, and fire whichever comes first. This gives exact methods for reactions with fixed delays, such as transcription and translation.
- **Other event simulators.** The same minimum of clocks is the core of [event-driven simulation](/event-driven-simulation/) and of [kinetic Monte Carlo](/kinetic-monte-carlo/) codes that keep one candidate time per event type.

## When to use it

Use it to teach or to check the exact methods, for networks with a handful of reactions, or as the base of a simulator with delayed or non-exponential events. For an exact simulation of a large network, use the next reaction method, or the direct method with a fast search. For large counts, use an approximate method such as [tau-leaping](/tau-leaping/).

## Pitfalls

- **Zero propensities.** A reaction with $a_j = 0$ must get an infinite clock, not a call to an exponential sampler with rate 0, which fails or returns an infinite value with a division by 0.
- **Ties.** Two equal clocks have probability 0 in exact arithmetic, but they can happen in floating point. Any fixed rule for ties is fine; the code keeps the first.
- **Reusing clocks.** Keeping the clock of a reaction whose propensity changed, without rescaling it, gives the wrong law. Throw it away (this method) or rescale it (the next reaction method).
- **The last step.** If the smallest clock rings after $T$, stop without firing it.
- **Units.** The propensities need the stochastic rate constants: $c = k/(N_A V)$ for $A + B$, and $c = 2k/(N_A V)$ for $2A$ with the propensity $c\, x_A(x_A - 1)/2$.

## Implementations

## History

Gillespie's 1976 paper in the Journal of Computational Physics derived the reaction probability density function $a_j e^{-a_0 s}$ and gave two ways to sample it, the direct method and the first reaction method, with a proof that both are exact. He preferred the direct method for its smaller use of random numbers, and his 1977 paper used it for all its examples. Gibson and Bruck (2000) returned to the first reaction method and showed that, with a dependency graph, rescaled clocks and a priority queue, it becomes the next reaction method, which needs one random number per event.

## References
