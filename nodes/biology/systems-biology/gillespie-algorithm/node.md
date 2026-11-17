---
tag: TDM41K
kind: algorithm
slug: gillespie-algorithm
name: Gillespie algorithm
aliases:
- stochastic simulation algorithm
- Gillespie direct method
area: biology/systems-biology
level: core
summary: 'Simulate the chemical master equation exactly: draw an exponential time to the next reaction from the total propensity, then pick the reaction.'
model: real-ram
complexity:
  vars: {n: the number of species, m: the number of reactions, N: the expected number of reaction events in the run}
  time: {expected: Θ(N (m + n))}
  space: {extra: Θ(n + m)}
properties: {deterministic: false, randomized: true, exact: true, recursive: false}
history:
  year: 1976
  people: [Daniel T. Gillespie]
  note: Gillespie gave the direct method and the first reaction method in the Journal of Computational Physics in 1976, and applied the direct method to coupled reactions in the Journal of Physical Chemistry in 1977.
prereqs: [chemical-master-equation, inverse-transform-sampling]
see_also: [first-reaction-method, next-reaction-method, tau-leaping, kinetic-monte-carlo, finite-state-projection, stochastic-sir-model, alias-method, event-driven-simulation]
sources:
  - paper: doi:10.1016/0021-9991(76)90041-3
    title: Daniel T. Gillespie, A general method for numerically simulating the stochastic time evolution of coupled chemical reactions, Journal of Computational Physics 22(4), 1976, 403-434
    locator: the reaction probability density function and the direct method that samples it
  - paper: doi:10.1021/j100540a008
    title: Daniel T. Gillespie, Exact stochastic simulation of coupled chemical reactions, Journal of Physical Chemistry 81(25), 1977, 2340-2361
    locator: the derivation of the next reaction density, the direct method, and the worked examples
  - paper: doi:10.1016/0378-4371(92)90283-V
    title: Daniel T. Gillespie, A rigorous derivation of the chemical master equation, Physica A 188(1-3), 1992, 404-425
    locator: the physical conditions under which the propensity description, and so the simulation, is exact
  - book: isbn:9781138549289
    title: Darren J. Wilkinson, Stochastic Modelling for Systems Biology, 3rd edition, CRC Press, 2018
    locator: the chapter on stochastic simulation algorithms (the direct method and its variants)
---

The Gillespie algorithm draws one exact sample path of the jump process whose probabilities solve the [chemical master equation](/chemical-master-equation/). It does not solve the equation. It simulates the reactions one at a time: from the current molecule counts it draws the waiting time to the next reaction from an exponential law whose rate is the sum of all propensities, then picks which reaction fires with probability proportional to its propensity, applies it, and repeats. Every step uses two uniform random numbers and $\Theta(m)$ work for $m$ reactions. The paths have exactly the law of the master equation, so averages over many runs converge to the true moments and probabilities. This version is the *direct method*. Gillespie gave a second, equivalent version in the same 1976 paper, the [first reaction method](/first-reaction-method/), and the [next reaction method](/next-reaction-method/) is a faster form of that one.

## In plain words

A cell holds a few hundred molecules of a few kinds, and each kind of reaction happens now and then, at random. Reactions with more fuel around happen more often.

To play this forward, add up how eager all the reactions are right now. The bigger that total, the sooner something happens, so draw a random wait that is short on average when the total is large. Then decide what happened: spin a wheel where each reaction has a slice as wide as its eagerness. Change the counts as that reaction says, move the clock forward by the wait, and do it again.

Each run is one possible story of the cell. Run it many times and count how often each outcome turns up, and you get the chances that the exact equation would give.

## The problem

**Input.** A network with $n$ species and $m$ reactions: for each reaction $j$ a change vector $\nu_j \in \mathbb{Z}^n$ and a propensity function $a_j(x) \ge 0$ of the state $x \in \mathbb{N}^n$. A start state $x_0$, an end time $T$, and a source of uniform random numbers. The propensities usually come from stochastic [mass action](/mass-action-kinetics/): $c$ for a source, $c\, x_A$ for $A \to \ldots$, $c\, x_A x_B$ for $A + B \to \ldots$, and $c\, x_A (x_A - 1)/2$ for $2A \to \ldots$, with $c = 2k/(N_A V)$ in the last case for a deterministic rate constant $k$ in molar units.

**Output.** The event times $0 < t_1 < t_2 < \ldots \le T$ and the states just after them, such that the path has the same law as the Markov jump process $X$ of the chemical master equation on $[0, T]$. The state at time $T$ is the last recorded state.

**The next reaction density.** Given $X(t) = x$, let $\tau$ be the time to the next reaction and $J$ the reaction. With $a_0(x) = \sum_j a_j(x)$,

$$\Pr(\tau \in [s, s + ds),\ J = j) = a_j(x)\, e^{-a_0(x) s}\, ds .$$

So $\tau$ is exponential with rate $a_0(x)$, $J = j$ with probability $a_j(x)/a_0(x)$, and the two are independent. The direct method samples the two factors one after the other.

## The algorithm

```pseudo id=main
DIRECT-METHOD(x0, ν, a, T)
L1  t ← 0; x ← x0; record (0, x)
L2  loop
L3      compute a_j(x) for j = 1, ..., m and a0 ← a_1(x) + ... + a_m(x)
L4      if a0 = 0 then return the record
L5      τ ← -ln(1 - U1) / a0 with U1 uniform on [0, 1)
L6      if t + τ > T then return the record
L7      u ← U2 · a0 with U2 uniform on [0, 1)
L8      j ← the smallest index with a_1(x) + ... + a_j(x) > u
L9      t ← t + τ; x ← x + ν_j
L10     record (t, x)
```

Line L5 is [inverse transform sampling](/inverse-transform-sampling/) of the exponential law. Line L8 is inverse transform sampling of the discrete law $a_j / a_0$ by a linear search over the cumulative sums. Line L6 discards the last waiting time: the process stays in $x$ until after $T$, so $x$ is the state at $T$, and the reaction is not fired.

## Example

Take immigration-death: $R_1: \emptyset \to X$ with propensity $a_1 = 10$, and $R_2: X \to \emptyset$ with propensity $a_2 = x$ (rate 1 per molecule). Start from $x_0 = 2$ and use Python's `random.Random(1)`.

| step | $a_1, a_2$ | $a_0$ | $\tau$ | $u$ | fires | $t$ after | $x$ after |
|---|---|---|---|---|---|---|---|
| 1 | 10, 2 | 12 | 0.0120 | 10.1692 | $R_2$ | 0.0120 | 1 |
| 2 | 10, 1 | 11 | 0.1312 | 2.8058 | $R_1$ | 0.1432 | 2 |
| 3 | 10, 2 | 12 | 0.0570 | 5.3939 | $R_1$ | 0.2002 | 3 |
| 4 | 10, 3 | 13 | 0.0811 | 10.2534 | $R_2$ | 0.2813 | 2 |
| 5 | 10, 2 | 12 | 0.0082 | 0.3402 | $R_1$ | 0.2895 | 3 |
| 6 | 10, 3 | 13 | 0.1390 | 5.6260 | $R_1$ | 0.4285 | 4 |

In step 1 the cumulative sums are 10 and 12, and $u = 10.1692$ falls in $[10, 12)$, so $R_2$ fires. In step 2 the sums are 10 and 11, and $u = 2.8058 < 10$, so $R_1$ fires. The count drifts up toward the stationary mean 10.

To check a simulator, use networks with a known law. Pure death $X \to \emptyset$ at rate 1 per molecule from 100 molecules gives $X(1)$ Binomial$(100, e^{-1})$, with mean 36.787944 and variance 23.254416. Immigration-death with rates 10 and 1 has the stationary law [Poisson](/poisson-distribution/)$(10)$, and from $x_0 = 0$, $X(1)$ is Poisson$(10(1 - e^{-1})) = $ Poisson$(6.321206)$. The tests of the implementation compare the sample means and the histograms of many runs with these laws.

## Correctness

The next reaction density follows from the definition of the propensity: the probability that nothing fires in $[t, t + s)$ satisfies $p_0'(s) = -a_0(x) p_0(s)$, so $p_0(s) = e^{-a_0(x) s}$, and then reaction $j$ fires in $[s, s + ds)$ with probability $a_j(x)\, ds$. Line L5 gives $\tau$ with density $a_0 e^{-a_0 s}$, and line L8 gives $J = j$ with probability $a_j / a_0$, independent of $\tau$, so one step has the joint density $a_j e^{-a_0 s}$. Each step uses fresh random numbers and depends on the past only through $x$, which matches the strong Markov property of $X$. By induction on the number of events, the recorded path has the law of $X$ on $[0, T]$. The full proof is below.

## Complexity

- **Per event.** Line L3 recomputes $m$ propensities, line L8 scans up to $m$ cumulative sums, and line L9 changes up to $n$ counts. So a step costs $\Theta(m + n)$ with a constant number of random numbers.
- **Per run.** The number of events $N$ is random. Its mean is $\mathbb{E}[N] = \int_0^T \mathbb{E}[a_0(X(t))]\, dt$, because events come at the rate $a_0$. For pure death from $x_0$ at rate $c$ it is $x_0(1 - e^{-cT})$; for immigration-death at stationarity it is $2bT$, where $b$ is the immigration rate. The expected time is $\Theta(\mathbb{E}[N](m + n))$.
- **Large networks.** With a dependency graph, line L3 only updates the propensities that the last reaction changed, and $a_0$ is updated by the differences. The search in line L8 is then the bottleneck, $\Theta(m)$ per step; a tree of partial sums makes it $O(\log m)$.
- **Space.** $\Theta(n + m)$ for the state and the propensities, plus the record. Recording only the state on a fixed time grid keeps the output small.
- **Systems with fast reactions.** The cost is set by the number of events, not by the time span. A fast reversible reaction that fires $10^6$ times per second costs $10^6$ steps per simulated second even if its net effect is small.

## Properties

- **Exact.** The paths have exactly the law of the jump process of the chemical master equation, up to the quality of the random numbers and floating point rounding. There is no step size and no bias.
- **Randomized.** Each run is one sample. Estimates of means and probabilities have Monte Carlo error of order $1/\sqrt{R}$ for $R$ runs, by the [central limit theorem](/central-limit-theorem/).
- **Two random numbers per event.** One for the time and one for the reaction. A run with $N$ events uses $2N + 1$ numbers when it stops at $T$, because the last waiting time is drawn and discarded.
- **Same law, different paths.** The first reaction method and the next reaction method give paths with the same law, but they use the random numbers in another way, so for the same seed they give different paths.
- **Not tied to mass action.** The proof uses only that the propensities depend on the current state. Any propensity function that is $\ge 0$ works, for example Hill functions of a reduced model, but then the result is only as good as the model.

## Variants and improvements

- **First reaction method.** Draw one exponential clock per reaction and fire the one that rings first ([first reaction method](/first-reaction-method/), Gillespie 1976). It is equivalent in law and slower when $m$ is large.
- **Next reaction method.** Keep the clocks of the reactions that did not fire, rescale them when their propensities change, and hold them in an [indexed priority queue](/indexed-priority-queue/) ([next reaction method](/next-reaction-method/), Gibson and Bruck 2000). It uses about one random number per event and $O(\log m)$ queue work.
- **Optimized and sorting direct methods.** Order the reactions by how often they fire, so that the linear search of line L8 stops early in most steps (Cao, Li and Petzold 2004; the sorting direct method updates the order during the run).
- **Composition and rejection.** Group the reactions by the size of their propensity into bins of powers of 2, pick a bin, then pick a reaction in the bin by [rejection sampling](/rejection-sampling/). The expected work per event does not depend on $m$ (Slepoy, Thompson and Plimpton 2008). For a fixed set of weights, the [alias method](/alias-method/) does the same in $O(1)$, but propensities change at every step.
- **Tau-leaping.** Fire many reactions in one step of length $\tau$ by Poisson draws ([tau-leaping](/tau-leaping/)). It is faster when counts are large, and it is an approximation.
- **Time-dependent propensities and delays.** If the propensities depend on $t$ (a growing volume, a periodic input), line L5 is no longer valid. Anderson's modified next reaction method handles this case and delays.

## When to use it

Use it when counts are small enough that single reactions matter (gene expression, signaling with few molecules, epidemics in a small group), when exact sample paths are needed, and when the number of events in the time span is affordable. It is the reference method against which the approximate methods are checked. If the state space is small enough to list, [finite state projection](/finite-state-projection/) gives the distribution with an error bound and no sampling error. If every species has large counts, [tau-leaping](/tau-leaping/), the [chemical Langevin equation](/chemical-langevin-equation/), or the deterministic rate equations are much faster.

## Pitfalls

- **The rate constant.** The propensity uses the stochastic constant $c$, not the molar constant $k$. For $A + B$, $c = k/(N_A V)$; for $2A$, $c = 2k/(N_A V)$ with the propensity $c\, x_A(x_A - 1)/2$. A wrong factor of 2 for dimerization gives the wrong equilibrium, and nothing in the output shows it.
- **The last step.** When $t + \tau > T$, the run must stop without firing the reaction. Firing it and then stopping biases the state at $T$.
- **Sampling on a grid.** The state at a grid time $s$ is the state after the last event at or before $s$. Taking the state of the first event after $s$, or interpolating between events, gives a biased estimate.
- **Rounding in the search.** The cumulative sum can end slightly below $u$ when $u$ is close to $a_0$. The search must then return the last reaction with a positive propensity, never a reaction with $a_j = 0$, which could make a count negative.
- **The logarithm.** Use $-\ln(1 - U)$ with $U$ in $[0, 1)$, or a library exponential sampler. $-\ln U$ is infinite when $U = 0$.
- **One run is not an answer.** A single path shows one possible behavior. Means, variances and probabilities need many runs with independent random streams, and the report needs the Monte Carlo error.

## Implementations

## History

Kendall simulated a birth-death process by hand with random numbers in 1950, and Bortz, Kalos and Lebowitz used the same idea of an exponential waiting time and a choice by rate for spin systems in 1975 (see [kinetic Monte Carlo](/kinetic-monte-carlo/)). Gillespie derived the next reaction density for chemical reactions from first principles and gave the direct method and the first reaction method in the Journal of Computational Physics in 1976. His 1977 paper in the Journal of Physical Chemistry made the direct method known to chemists, with simulations of the Lotka reactions, the Brusselator and the Oregonator. In 1992 he showed that the chemical master equation, and so the simulation, is exact for a well-stirred gas in thermal equilibrium. The method became central to systems biology around 2000, when experiments showed noise in gene expression, and it is in tools such as COPASI, StochKit, GillesPy2 and the BioNetGen and VCell packages.

## References
