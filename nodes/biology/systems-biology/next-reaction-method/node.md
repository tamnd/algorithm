---
tag: KRZQSZ
kind: algorithm
slug: next-reaction-method
name: Next reaction method
aliases:
- Gibson-Bruck algorithm
area: biology/systems-biology
level: advanced
summary: An exact stochastic simulation that keeps one firing time per reaction in a priority queue and updates only the reactions a firing affects.
model: real-ram
complexity:
  vars: {n: the number of species, m: the number of reactions, d: the largest number of reactions whose propensity one firing changes, N: the expected number of reaction events in the run}
  time: {expected: O(m + N (n + d log m))}
  space: {extra: Θ(n + m + m d)}
properties: {deterministic: false, randomized: true, exact: true, recursive: false}
history:
  year: 2000
  people: [Michael A. Gibson, Jehoshua Bruck]
  note: Gibson and Bruck turned the first reaction method into the next reaction method in the Journal of Physical Chemistry A in 2000, with a dependency graph, reused clocks and an indexed priority queue.
prereqs: [first-reaction-method, indexed-priority-queue]
see_also: [gillespie-algorithm, binary-heap, priority-queue, event-driven-simulation, kinetic-monte-carlo, tau-leaping, chemical-master-equation, stoichiometric-matrix]
sources:
  - paper: doi:10.1021/jp993732q
    title: Michael A. Gibson and Jehoshua Bruck, Efficient exact stochastic simulation of chemical systems with many species and many channels, Journal of Physical Chemistry A 104(9), 2000, 1876-1889
    locator: the dependency graph, the reuse of the putative times by rescaling, the indexed priority queue, and the proof that the method is exact
  - paper: doi:10.1063/1.2799998
    title: David F. Anderson, A modified next reaction method for simulating chemical systems with time dependent propensities and delays, Journal of Chemical Physics 127(21), 2007, 214107
    locator: the formulation by unit-rate internal clocks of each reaction, which also covers propensities that drop to 0
  - paper: doi:10.1016/0021-9991(76)90041-3
    title: Daniel T. Gillespie, A general method for numerically simulating the stochastic time evolution of coupled chemical reactions, Journal of Computational Physics 22(4), 1976, 403-434
    locator: the first reaction method, on which the next reaction method is built
---

The next reaction method is an exact simulation method for the jump process of the [chemical master equation](/chemical-master-equation/). It starts from the [first reaction method](/first-reaction-method/), which draws a new exponential clock for every reaction at every step, and removes the waste. The clock of a reaction that did not fire is still valid after the event, by the memoryless property of the exponential law: only its rate may have changed, and then the remaining time can be rescaled. So the method stores one absolute firing time per reaction in an [indexed priority queue](/indexed-priority-queue/), fires the reaction at the top, draws a fresh clock only for that reaction, and recomputes the propensities and the times only for the reactions that the firing affects, as listed in a dependency graph. An event then costs one random number and $O(d \log m)$ queue work, where $d$ is the number of affected reactions, instead of $\Theta(m)$. The paths have exactly the same law as those of the [Gillespie algorithm](/gillespie-algorithm/).

## In plain words

Give every reaction an alarm clock set to the moment it would happen if nothing else changed. Keep the clocks in a line ordered by their alarm times, so the next one to ring is always in front.

When the front clock rings, that reaction happens, and the counts change. Most reactions do not care about this change, so their clocks stay as they are. For the few reactions that use the molecules that changed, the clocks must speed up or slow down: a reaction that became twice as likely should ring in half the time it still had left. Only the reaction that just happened gets a brand new clock.

So each step needs one new random number and touches only a few clocks, even in a cell model with thousands of reactions.

## The problem

**Input.** A network with $n$ species and $m$ reactions: change vectors $\nu_j$, propensity functions $a_j(x) \ge 0$, and for each $j$ the set of species that $a_j$ reads; a start state $x_0$; an end time $T$; a source of random numbers.

**Output.** Event times and the states just after them, with the same law as the jump process $X$ of the chemical master equation on $[0, T]$.

**The dependency graph.** $G[\mu]$ lists $\mu$ itself and every reaction $k$ whose propensity reads a species that $\nu_\mu$ changes. After $\mu$ fires, the propensities of the reactions outside $G[\mu]$ are the same as before. For the dimerization network $R_1: 2A \to B$, $R_2: B \to 2A$, $R_3: B \to \emptyset$, $R_1$ and $R_2$ change $A$ and $B$, and $R_3$ changes $B$, so $G[R_1] = \{R_1, R_2, R_3\}$, $G[R_2] = \{R_1, R_2, R_3\}$ and $G[R_3] = \{R_2, R_3\}$.

## The algorithm

Each reaction $k$ has a propensity $a_k$ and a firing time $\tau_k$ in the queue. A reaction whose propensity is 0 has $\tau_k = \infty$ and keeps its unused unit clock $r_k$.

```pseudo id=main
NEXT-REACTION(x0, ν, a, G, T)
L1  t ← 0; x ← x0; record (0, x)
L2  for k ← 1 to m do r ← Exp(1); a_k ← a_k(x); if a_k > 0 then τ_k ← t + r / a_k else τ_k ← ∞; r_k ← r
L3  build an indexed min-queue Q on τ_1, ..., τ_m
L4  loop
L5      (τ_μ, μ) ← the minimum of Q
L6      if τ_μ = ∞ or τ_μ > T then return the record
L7      t ← τ_μ; x ← x + ν_μ; record (t, x)
L8      for each k in G[μ] do
L9          a_new ← a_k(x)
L10         if k = μ then r ← Exp(1)
            else if a_new = a_k then skip to the next k
L11         else if a_k > 0 then r ← a_k (τ_k - t) else r ← r_k
            a_k ← a_new; if a_new > 0 then τ_k ← t + r / a_new else τ_k ← ∞; r_k ← r
L12         update the key of k in Q to τ_k
```

Line L11 is the reuse rule. The quantity $r = a_k(\tau_k - t)$ is the part of the reaction's unit-rate clock that has not been used yet. Dividing it by the new propensity gives the new remaining time, so $\tau_k^{\text{new}} = t + (a_k^{\text{old}} / a_k^{\text{new}})(\tau_k - t)$. When a propensity drops to 0, the unused part is stored in $r_k$ and used again when the propensity becomes positive.

## Example

Immigration-death: $R_1: \emptyset \to X$ with $a_1 = 10$, $R_2: X \to \emptyset$ with $a_2 = x$, from $x_0 = 2$, with Python's `random.Random(1)`. Each firing changes $X$, which $R_2$ reads, so $G[R_1] = G[R_2] = \{R_1, R_2\}$.

Line L2 draws $r = (0.1443, 1.8802)$, so $\tau_1 = 0.1443 / 10 = 0.0144$ and $\tau_2 = 1.8802 / 2 = 0.9401$.

| event | fires at | $x$ | new $\tau_1$ | unused clock of $R_2$ | new $\tau_2$ |
|---|---|---|---|---|---|
| 1 | 0.0144 ($R_1$) | 3 | 0.1587 | $2(0.9401 - 0.0144) = 1.8514$ | $0.0144 + 1.8514/3 = 0.6315$ |
| 2 | 0.1587 ($R_1$) | 4 | 0.1882 | $3(0.6315 - 0.1587) = 1.4184$ | $0.1587 + 1.4184/4 = 0.5133$ |
| 3 | 0.1882 ($R_1$) | 5 | 0.2566 | $4(0.5133 - 0.1882) = 1.3004$ | $0.1882 + 1.3004/5 = 0.4483$ |
| 4 | 0.2566 ($R_1$) | 6 | 0.3163 | $5(0.4483 - 0.2566) = 0.9585$ | $0.2566 + 0.9585/6 = 0.4163$ |

The new $\tau_1$ comes from a fresh draw each time (1.4430, 0.2945, 0.6841, 0.5969, each divided by 10). The death reaction never fires in these four events, and it never gets a new random number: its single clock, drawn at the start, is used up step by step (1.8802, 1.8514, 1.4184, 1.3004, 0.9585) while its rate grows with $x$. The first four events use $2 + 4 = 6$ random numbers; the first reaction method would use 10. The tests of the implementation check the queue against a brute-force minimum, the dependency graph of small networks, the Binomial law of pure death, the [Poisson](/poisson-distribution/) laws of immigration-death, the law of a dimerization network against the direct method, and the count of $m + N$ random numbers for $N$ events.

## Correctness

Call $r_k = a_k(\tau_k - t)$ the residual of reaction $k$, in the units of a unit-rate clock. Between events the state, and so each $a_k$, is constant, so each residual goes down by $a_k s$ in a time $s$, and line L11 stores exactly this value. Just after each event, given the whole history, the residuals are independent unit exponentials: the reaction that fired got a fresh one, and for every other reaction the history says only that $r_k > a_k s$, and an exponential conditioned in this way is again exponential by the memoryless property. So the numbers $r_k / a_k$ are independent exponentials with the rates $a_k(x)$, and their minimum has the next reaction density $a_j e^{-a_0 s}$ of the first reaction method. Induction on the events gives the law of the path. The full proof is below.

## Complexity

- **Setup.** Line L2 draws $m$ numbers and computes $m$ propensities, and line L3 builds a [binary heap](/binary-heap/) in $\Theta(m)$. The dependency graph is computed one time before the run, from the species that each reaction changes and reads.
- **Per event.** Line L5 reads the minimum in $O(1)$. Line L7 changes up to $n$ counts. Lines L8 to L12 run for the $|G[\mu]| \le d$ affected reactions, each with one propensity and one heap update in $O(\log m)$. So an event costs $O(n + d \log m)$, and the run costs $O(m + N(n + d \log m))$ for $N$ events.
- **Random numbers.** $m + N$ in total, about one per event, against $2N + 1$ for the direct method and up to $m(N + 1)$ for the first reaction method.
- **Space.** The heap, the positions of the reactions in the heap, the propensities, the stored clocks, and the graph: $\Theta(n + m + \sum_\mu |G[\mu]|) \subseteq \Theta(n + m + m d)$.
- **In practice.** The $O(\log m)$ queue work and the poor memory locality of a heap can make the method slower than a well-tuned direct method for small and medium networks. Its advantage grows when $m$ is large and $d$ is small, as in large sparse models of signaling or of spatial compartments.

## Properties

- **Exact.** The paths have the law of the jump process of the chemical master equation, like those of the direct method and the first reaction method.
- **One random number per event.** Only the fired reaction draws a new clock.
- **Local updates.** An event touches only the reactions in $G[\mu]$. The cost does not grow with $m$ except through $\log m$.
- **Absolute times.** The queue holds absolute firing times, not waiting times, so the reactions outside $G[\mu]$ need no change at all.
- **Equal propensities.** If the new propensity equals the old one, the time is kept as it is (the skip after line L10). This is the rescaling rule with factor 1, and it saves a heap update.

## Variants and improvements

- **Modified next reaction method.** Anderson (2007) writes each reaction as a unit-rate Poisson process run at the speed $a_k(X(t))$, and tracks for each reaction the internal time used so far and the internal time of its next firing. This is the same reuse in another form. It handles propensities that depend on time and reactions with delays, and it is the base of coupling methods for multilevel Monte Carlo.
- **Other queues.** A binary heap is the usual choice. Bucket queues and calendar queues give $O(1)$ expected time when the firing times are spread evenly, as in [event-driven simulation](/event-driven-simulation/).
- **Direct methods with partial sums.** A tree of partial sums of the propensities lets the direct method update one propensity and pick the reaction in $O(\log m)$, with the same cost order and simpler code. The composition-rejection method of Slepoy, Thompson and Plimpton (2008) has an expected cost per event that does not depend on $m$.
- **Approximate leaps.** For large counts, [tau-leaping](/tau-leaping/) fires many reactions per step and is no longer exact.

## When to use it

Use it for exact simulation of large networks in which each reaction affects few others: genome-scale models of gene expression, signaling cascades, and models with many spatial compartments in which each diffusion jump is a reaction between two neighbors. It is also the right form when some reactions have delays or time-dependent rates, through the modified version. For a network with ten reactions, the direct method is shorter and as fast.

## Pitfalls

- **Missing dependencies.** If $G[\mu]$ leaves out a reaction whose propensity changes, the old time stays in the queue and the law is wrong, with no error message. Compute $G$ from the reactants of each propensity, and include $\mu$ itself.
- **Reusing the fired clock.** The reaction that fired must get a fresh exponential (line L10). Rescaling its old clock, whose residual is 0, would make it fire again at once.
- **Rescaling with the wrong times.** The rule is $\tau_k \leftarrow t + (a_k^{\text{old}} / a_k^{\text{new}})(\tau_k - t)$ with $t$ the time of the current event. Using the time of the previous event, or the waiting time from the previous event, gives a wrong law.
- **Propensities that reach 0.** With $a_k^{\text{new}} = 0$ the rescaling divides by 0. Store the unused clock and set the time to $\infty$, then use the stored clock when the propensity becomes positive again.
- **Heap positions.** An indexed queue must keep the position of each reaction up to date in every swap, or an update moves the wrong entry.
- **Units.** As in every exact method, the propensities need the stochastic rate constants, with $c = 2k/(N_A V)$ and the propensity $c\, x_A(x_A - 1)/2$ for $2A$.

## Implementations

## History

Gillespie (1976) gave the first reaction method and noted that it wastes random numbers. Gibson and Bruck (2000) turned it into the next reaction method: they kept the putative times of the reactions that did not fire, showed that rescaling them keeps the method exact, and used a dependency graph and an indexed priority queue so that the cost per event grows only as $\log m$. Cao, Li and Petzold (2004) showed that a direct method with the reactions sorted by frequency is often faster in practice. Anderson (2007) rewrote the method with internal unit-rate clocks, which extended it to time-dependent propensities and delays.

## References
