---
tag: R8R2C0
kind: algorithm
slug: simulated-annealing
name: Simulated annealing
aliases:
- annealing
- SA
area: optimization/metaheuristics
level: intro
summary: Local search that accepts a worse neighbor with probability exp(-Δ/T) while the temperature T falls. With T_k = c/log k and c at least the deepest trap depth, it converges to a global minimum.
solves: [global-optimization]
model: real-ram
complexity:
  vars: {k: the number of steps, c: the cost of one proposal and one change of the objective, s: the size of one solution}
  time: {worst: O(k c)}
  space: {extra: O(s)}
properties: {deterministic: false, iterative: true, anytime: true, population: false}
history:
  year: 1983
  people: [Scott Kirkpatrick, C. Daniel Gelatt, Mario P. Vecchi, Vladimír Černý]
  note: Kirkpatrick, Gelatt and Vecchi published the method in Science in 1983. Černý published the same idea for the traveling salesman problem in 1985. Both use the acceptance rule of Metropolis and others from 1953.
prereqs: [local-search, metropolis-criterion, markov-chain]
see_also: [cooling-schedule, simulated-annealing-convergence, metropolis-hastings, threshold-accepting, great-deluge-algorithm, hill-climbing, tabu-search, traveling-salesman-problem]
sources:
  - paper: doi:10.1126/science.220.4598.671
    title: Scott Kirkpatrick, C. Daniel Gelatt and Mario P. Vecchi, Optimization by simulated annealing, Science 220(4598), 1983
    locator: pages 671 to 680
  - paper: doi:10.1007/BF00940812
    title: Vladimír Černý, Thermodynamical approach to the traveling salesman problem, an efficient simulation algorithm, Journal of Optimization Theory and Applications 45(1), 1985
    locator: pages 41 to 51
  - paper: doi:10.1063/1.1699114
    title: Nicholas Metropolis, Arianna W. Rosenbluth, Marshall N. Rosenbluth, Augusta H. Teller and Edward Teller, Equation of state calculations by fast computing machines, Journal of Chemical Physics 21(6), 1953
    locator: pages 1087 to 1092 (the acceptance rule)
  - paper: doi:10.1287/moor.13.2.311
    title: Bruce Hajek, Cooling schedules for optimal annealing, Mathematics of Operations Research 13(2), 1988
    locator: pages 311 to 329 (Theorem 1, the necessary and sufficient condition on the schedule)
  - book: isbn:9780470278581
    title: El-Ghazali Talbi, Metaheuristics, From Design to Implementation, Wiley, 2009
    locator: Chapter 2, Single-solution based metaheuristics, Section 2.4, Simulated annealing
  - book: doi:10.1007/978-94-015-7744-1
    title: Peter J. M. van Laarhoven and Emile H. L. Aarts, Simulated Annealing, Theory and Applications, Reidel, 1987
    locator: the chapters on the Markov chain model and on cooling schedules
---

Simulated annealing is a [local search](/local-search/) method that always moves to a better neighbor, and moves to a worse neighbor with probability $e^{-\Delta/T}$, where $\Delta$ is the increase of the objective and $T$ is a *temperature* that falls over time. This rule is the [Metropolis criterion](/metropolis-criterion/). At a fixed temperature the walk is a [Markov chain](/markov-chain/) whose [stationary distribution](/stationary-distribution/) is the Boltzmann distribution, which puts more mass on better solutions as $T$ falls. With the slow schedule $T_k = c/\log k$ and $c$ at least the depth of the deepest trap, the walk is at a [global minimum](/global-optimization/) with probability tending to 1, by [Hajek's theorem](/simulated-annealing-convergence/). With the fast schedules that people use in practice there is no such guarantee, and the method is a [metaheuristic](/metaheuristic/).

## In plain words

You look for the lowest point of a rough landscape, and you can only feel the ground next to you. A plain downhill walk stops in the first small pit. Simulated annealing sometimes steps uphill on purpose, so that it can climb out of a pit and find a deeper one.

How often it steps uphill depends on a number called the temperature. When the temperature is high, the walk accepts almost any step and wanders over the whole landscape. As the temperature falls, it accepts fewer uphill steps, and only small ones. At the end it is cold, it only goes downhill, and it settles in a pit.

The name comes from metal work. A smith heats metal and cools it slowly, so that the atoms find an orderly state of low energy. Cool it too fast and the metal stays in a disordered state.

## The problem

The input is a finite set $S$ of solutions, an objective $f : S \to \mathbb{R}$ to minimize (the *energy*), and a neighborhood $N(x) \subseteq S$ for each $x$, given by a random move: a proposal distribution $R(x, \cdot)$ on $N(x)$. The goal is a solution $x^* \in S$ with $f(x^*) = f^* = \min_{x \in S} f(x)$, the [global optimization](/global-optimization/) problem on a finite set. A *cooling schedule* $T_1 \ge T_2 \ge \dots > 0$ and a number of steps $K$ are parameters. For a maximization problem, minimize $-f$.

## The algorithm

```pseudo id=main
SIMULATED-ANNEALING(x₀, f, R, T, K)
L1  x ← x₀, best ← x₀
L2  for k ← 1 to K do
L3      y ← a random neighbor of x, drawn from R(x, ·)
L4      Δ ← f(y) − f(x)
L5      if Δ ≤ 0 or random() < exp(−Δ / T_k) then      ▷ the Metropolis criterion
L6          x ← y
L7          if f(x) < f(best) then best ← x
L8  return best
```

Here random() returns a uniform number in $[0, 1)$, so line L5 accepts a worse neighbor with probability exactly $e^{-\Delta/T_k}$. The algorithm returns the best solution it has seen, which can be better than the last one. Code keeps $f(x)$ and $f(best)$ in variables, and in many problems it computes $\Delta$ from the move without a full evaluation of $f(y)$: for a 2-opt move in a tour, $\Delta$ needs four distances.

## Example

Take 8 states $0, \dots, 7$ on a cycle, each with the two states next to it as neighbors, and a uniform proposal. The energies are

| state | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $f$ | 3 | 1 | 4 | 2 | 5 | 0 | 3 | 6 |

State 5 is the global minimum. States 1 and 3 are local minima. From state 1, each path to a lower state climbs to energy 5 or more, so state 1 is a trap of depth $5 - 1 = 4$. State 3 is a trap of depth $4 - 2 = 2$, because it reaches state 1 over state 2.

Start at $x_0 = 0$ with the geometric schedule $T_k = 2 \cdot 0.9^{k-1}$. The column $u$ holds the uniform numbers of a fixed seed.

| $k$ | $T_k$ | $x$ | $y$ | $\Delta$ | $e^{-\Delta/T_k}$ | $u$ | result |
|---|---|---|---|---|---|---|---|
| 1 | 2.000 | 0 | 1 | $-2$ | 1 | | accept |
| 2 | 1.800 | 1 | 0 | 2 | 0.329 | 0.395 | reject |
| 3 | 1.620 | 1 | 0 | 2 | 0.291 | 0.072 | accept |
| 4 | 1.458 | 0 | 7 | 3 | 0.128 | 0.366 | reject |
| 5 | 1.312 | 0 | 7 | 3 | 0.102 | 0.910 | reject |
| 6 | 1.181 | 0 | 7 | 3 | 0.079 | 0.037 | accept |
| 7 | 1.063 | 7 | 0 | $-3$ | 1 | | accept |
| 8 | 0.957 | 0 | 1 | $-2$ | 1 | | accept |
| 9 | 0.861 | 1 | 0 | 2 | 0.098 | 0.241 | reject |
| 10 | 0.775 | 1 | 2 | 3 | 0.021 | 0.059 | reject |

At step 6 the walk climbs to the worst state 7, which a downhill walk never does. But it falls back into state 1, and the temperature drops too fast for it to climb the barrier of height 4 again. After 60 steps it is still at state 1.

Over 100 runs (seeds 0 to 99), from state 0:

| schedule | steps | runs that end at state 5 | runs that see state 5 |
|---|---|---|---|
| $T_k = 2 \cdot 0.9^{k-1}$ | 60 | 7 | 8 |
| $T_k = 5 \cdot 0.99^{k-1}$ | 1000 | 60 | 99 |
| $T_k = 4 / \ln(k + 1)$ | 1000 | 69 | 79 |
| $T_k = 4 / \ln(k + 1)$ | 10000 | 82 | 92 |
| $T_k = 1 / \ln(k + 1)$ | 10000 | 3 | 3 |

The schedule $4/\ln(k+1)$ meets the condition $c \ge 4$ of Hajek's theorem, and its success rate rises with the number of steps, but slowly. With 100 runs a count has a standard deviation of up to 5. For this schedule the exact probability of state 5, from the product of the transition matrices, is $0.593$ after 1000 steps and $0.720$ after 10000 steps. The schedule $1/\ln(k+1)$ does not meet it, and most runs stay in state 1.

On a tour problem with 8 random points in the unit square (seed 3), with the 2-opt move (reverse a segment of the tour) and $T_k = 0.5 \cdot 0.998^{k-1}$ for 2000 steps, all 20 runs (seeds 0 to 19) end with the optimal tour length 2.7179, which brute force over the 5040 tours confirms.

## Correctness

Simulated annealing always returns a solution, and the solution is the best one that it saw: line L7 keeps the [loop invariant](/loop-invariant/) that $f(best) = \min\{f(x_0), \dots, f(x_k)\}$, where $x_i$ is the current solution after step $i$. Nothing more holds for each run. What the method guarantees is a statement about the distribution of $x_k$.

1. **Markov chain.** The sequence $x_0, x_1, \dots$ is a Markov chain with transition probabilities $P_{T_k}(i, j) = R(i, j) \min(1, e^{-(f(j) - f(i))/T_k})$ for $j \ne i$, and the rest of the mass on $i$.
2. **Equilibrium at a fixed temperature.** If $R$ is symmetric, $P_T$ satisfies [detailed balance](/detailed-balance/) with the Boltzmann distribution $\pi_T(i) = e^{-f(i)/T} / Z_T$. So $\pi_T$ is stationary. If the neighborhood graph is connected and $f$ is not constant, the chain is irreducible and aperiodic, and the distribution of $x_k$ converges to $\pi_T$.
3. **Concentration.** As $T \to 0$, $\pi_T$ converges to the uniform distribution on the set $S^*$ of global minima.
4. **Annealing.** If the schedule falls to 0 with $\sum_k e^{-d^*/T_k} = \infty$, where $d^*$ is the depth of the deepest local minimum that is not global, then $\Pr[x_k \in S^*] \to 1$, and this condition is also necessary (Hajek 1988). See [convergence of simulated annealing](/simulated-annealing-convergence/).

On the example, $\pi_T$ at $T = 1$ is $(0.031, 0.226, 0.011, 0.083, 0.004, 0.613, 0.031, 0.002)$, and at $T = 0.2$ it gives state 5 the mass $0.993$. A run of $200\,000$ steps at $T = 1$ from state 0 (seed 1) visits the states with frequencies at total variation distance $0.005$ from $\pi_1$. The proofs of the invariant and of claims 1 to 3 are below.

## Complexity

Each step does one proposal, one change $\Delta$ of the objective and at most one uniform number, so $K$ steps cost $O(K c)$, where $c$ is the cost of a proposal and of $\Delta$. The extra space is one solution besides the input, or two with $best$.

The number of steps for a given quality has no general bound. The facts that are known:

- **The guarantee is asymptotic.** Hajek's schedule $T_k = c/\ln(k+1)$ reaches temperature $T$ only after $k = e^{c/T} - 1$ steps. Let $g > 0$ be the gap between $f^*$ and the next value of $f$. The Boltzmann distribution at $T$ gives $S^*$ the mass $1 - \eta$ or more when $(|S| - 1) e^{-g/T} \le \eta$, and the schedule reaches such a $T$ only after about $((|S| - 1)/\eta)^{c/g}$ steps. When $|S|$ is exponential in the input size, so is this number.
- **Escaping a trap is slow at low temperature.** Each path out of a trap of depth $d$ climbs at least $d$ in total, so the product of the acceptance probabilities of its uphill steps is at most $e^{-d/T}$. The expected time to leave the trap at a fixed temperature grows like $e^{d/T}$ as $T \to 0$.
- **Exponential lower bounds exist.** Sasaki and Hajek (1988) showed for maximum matching that a form of simulated annealing finds a matching of nearly maximum size in polynomial expected time, but that there are graphs on which it needs exponential expected time to find a maximum matching.
- **Problems that are [NP-hard](/np-hard/) stay hard.** No schedule makes simulated annealing a polynomial-time method that finds an optimum of an NP-hard problem with probability $2/3$, unless NP = RP.

## Properties

- **Randomized.** Two runs with different seeds can return different solutions. Fix the seed to repeat a run.
- **Anytime.** Stop it at any step and $best$ is a valid answer.
- **One solution at a time.** It is a single-solution method, not a [population-based search](/population-based-search/).
- **Only differences of $f$ matter.** Adding a constant to $f$ changes nothing. Multiplying $f$ by $a > 0$ is the same as dividing the schedule by $a$, so the temperature must be in the units of $f$.
- **At $T = 0$** line L5 accepts only moves with $\Delta \le 0$, and the method is a randomized [hill climbing](/hill-climbing/) that also accepts equal moves.

## Variants and improvements

- **Schedules.** Geometric $T_k = T_0 \alpha^k$ with $\alpha$ between 0.8 and 0.999 is the common choice. Logarithmic schedules have the theorem but are too slow. Adaptive schedules set $T$ from the observed acceptance rate. See [cooling schedule](/cooling-schedule/).
- **Markov chains of fixed length.** Keep $T$ fixed for $L$ steps, then lower it. Kirkpatrick and others used this form.
- **Reheating and restarts.** Raise $T$ when the walk stalls, or restart from $best$.
- **Deterministic acceptance.** [Threshold accepting](/threshold-accepting/) accepts each move with $\Delta < \tau_k$, and the [great deluge algorithm](/great-deluge-algorithm/) accepts each solution below a falling level. Both drop the random number of line L5.
- **Parallel tempering.** Run copies at several temperatures and swap their states with a Metropolis test. It is a sampling method that also helps optimization.
- **Several objectives.** [Multi-objective simulated annealing](/multi-objective-simulated-annealing/) accepts by a rule on Pareto dominance.

## When to use it

Use simulated annealing on a [combinatorial optimization problem](/combinatorial-optimization-problem/) with a natural move, a cheap $\Delta$ and many local minima, such as the [traveling salesman problem](/traveling-salesman-problem/), placement, [graph partitioning](/graph-partitioning-problem/) or timetabling, when no exact method is fast enough. It needs only the move and the objective, and it is short to write. Compare it with [tabu search](/tabu-search/), [iterated local search](/iterated-local-search/) and restarts of a local search under the same number of evaluations before you trust it. For a problem with an exact method or a good relaxation, such as [linear programming](/linear-programming-problem/), use that method.

## Pitfalls

- **A temperature in the wrong units.** If $T$ is much larger than typical values of $\Delta$, the walk is random; if much smaller, it is hill climbing. Set $T_0$ so that a large fraction of worse moves, for example 0.5 to 0.8, are accepted at the start.
- **Returning the last solution.** At a finite temperature the last solution can be worse than one seen before. Keep $best$.
- **Recomputing $f$.** A full evaluation of $f(y)$ at each step wastes the main advantage. Compute $\Delta$ from the move.
- **Claiming the theorem for a fast schedule.** Hajek's guarantee is for the logarithmic schedule and in the limit. A geometric schedule has no convergence guarantee, so report measured results with the instance, the seeds and the number of runs.
- **An asymmetric proposal.** The Boltzmann distribution is stationary for a symmetric proposal. An asymmetric one needs the [Metropolis-Hastings](/metropolis-hastings/) ratio if the equilibrium matters.
- **Overflow and underflow.** Compute $e^{-\Delta/T}$ only for $\Delta > 0$, and treat $T = 0$ as "reject".

## Implementations

## History

Metropolis, the two Rosenbluths and the two Tellers introduced the acceptance rule in 1953 to sample the equilibrium states of a system of particles. Kirkpatrick, Gelatt and Vecchi turned it into an optimization method in 1983, with the analogy to the annealing of solids, and applied it to the placement and wiring of chips and to the traveling salesman problem. Černý published the same method for the traveling salesman problem in 1985. Geman and Geman in 1984 and Hajek in 1988 proved convergence under logarithmic schedules, and Hajek gave the exact constant.

## References
