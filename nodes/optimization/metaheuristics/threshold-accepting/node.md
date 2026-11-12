---
tag: 89MGMB
kind: algorithm
slug: threshold-accepting
name: Threshold accepting
area: optimization/metaheuristics
level: advanced
summary: Local search that accepts each neighbor whose objective is worse by less than a threshold, and lowers the threshold over time. The acceptance test has no random number.
solves: [global-optimization]
model: real-ram
complexity:
  vars: {k: the number of steps, c: the cost of one proposal and one change of the objective, s: the size of one solution}
  time: {worst: O(k c)}
  space: {extra: O(s)}
properties: {deterministic: false, iterative: true, anytime: true, population: false}
history:
  year: 1990
  people: [Gunter Dueck, Tobias Scheuer]
  note: Dueck and Scheuer proposed threshold accepting in 1990 as a simpler form of simulated annealing.
prereqs: [simulated-annealing, local-search]
see_also: [great-deluge-algorithm, cooling-schedule, metropolis-criterion, hill-climbing, late-acceptance-hill-climbing, traveling-salesman-problem, local-optimum]
sources:
  - paper: doi:10.1016/0021-9991(90)90201-B
    title: Gunter Dueck and Tobias Scheuer, Threshold accepting, a general purpose optimization algorithm appearing superior to simulated annealing, Journal of Computational Physics 90(1), 1990
    locator: pages 161 to 175
  - paper: doi:10.1006/jcph.1993.1010
    title: Gunter Dueck, New optimization heuristics, the great deluge algorithm and the record-to-record travel, Journal of Computational Physics 104(1), 1993
    locator: pages 86 to 92 (threshold accepting compared with the two new rules)
  - paper: "Ingo Althöfer and Klaus-Uwe Koschnick, On the convergence of threshold accepting, Applied Mathematics and Optimization 24, 1991"
    title: Ingo Althöfer and Klaus-Uwe Koschnick, On the convergence of threshold accepting
    locator: pages 183 to 195
  - book: isbn:9780470278581
    title: El-Ghazali Talbi, Metaheuristics, From Design to Implementation, Wiley, 2009
    locator: Chapter 2, Section 2.4, Simulated annealing, and its variants with deterministic acceptance
---

Threshold accepting is a [local search](/local-search/) method that moves to a random neighbor whenever the neighbor is worse by less than a threshold $\tau$, and lowers $\tau$ step by step to 0. It is [simulated annealing](/simulated-annealing/) with the random [Metropolis criterion](/metropolis-criterion/) replaced by a fixed test. Dueck and Scheuer proposed it in 1990. The proposals are still random, so the method is randomized, and it has no Boltzmann equilibrium and no simple convergence theorem. Its main use is the same as that of simulated annealing, on combinatorial problems with a cheap move.

## In plain words

You walk on a rough landscape and look for its lowest point. At each step you look at one random spot next to you. If that spot is lower, you go there. If it is higher, you still go there, but only if it is less than a fixed amount higher. That amount is the threshold.

At the start the threshold is large, so you can climb over small hills and leave poor valleys. Then you make the threshold smaller in stages. At the end you go only downhill or along flat ground, and you stop in a valley.

There is no coin toss when you decide. The same spot at the same threshold is always accepted or always refused. Only the choice of the spot to look at is random.

## The problem

The input is a finite set $S$ of solutions, an objective $f : S \to \mathbb{R}$ to minimize, a random move that draws a neighbor $y \in N(x)$ of a solution $x$, a nonincreasing sequence of thresholds $\tau_1 \ge \tau_2 \ge \dots \ge \tau_J > 0$, and a number $L$ of steps at each threshold. The goal is a solution with a small value of $f$, ideally a global minimum, the [global optimization](/global-optimization/) problem on a finite set.

## The algorithm

```pseudo id=main
THRESHOLD-ACCEPTING(x₀, f, N, τ₁ ≥ … ≥ τ_J, L)
L1  x ← x₀, best ← x₀
L2  for j ← 1 to J do
L3      repeat L times
L4          y ← a random neighbor of x
L5          if f(y) − f(x) < τ_j then             ▷ no random number here
L6              x ← y
L7              if f(x) < f(best) then best ← x
L8  return best
```

The test is strict, so with $\tau_j > 0$ an improvement or an equal move is always accepted. Dueck and Scheuer lower the threshold in stages. A common choice is a linear sequence $\tau_j = \tau_1 (J - j + 1)/J$, or a sequence taken from the distribution of the changes $|f(y) - f(x)|$ observed in a trial run.

## Example

Take the 8 states $0, \dots, 7$ on a cycle from the [simulated annealing](/simulated-annealing/) page, with the two cycle neighbors and

| state | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $f$ | 3 | 1 | 4 | 2 | 5 | 0 | 3 | 6 |

Use the thresholds $4, 3.5, 3, 2.5, 2, 1.5, 1, 0.5$ with $L = 5$ steps each, from $x_0 = 0$. With a fixed seed, the first 16 steps are:

| step | $\tau$ | $x$ | $y$ | $f(y) - f(x)$ | accepted |
|---|---|---|---|---|---|
| 1 | 4 | 0 | 7 | 3 | yes |
| 2 | 4 | 7 | 6 | $-3$ | yes |
| 3 | 4 | 6 | 5 | $-3$ | yes |
| 4 | 4 | 5 | 6 | 3 | yes |
| 5 | 4 | 6 | 5 | $-3$ | yes |
| 6 | 3.5 | 5 | 6 | 3 | yes |
| 7 | 3.5 | 6 | 7 | 3 | yes |
| 8 | 3.5 | 7 | 6 | $-3$ | yes |
| 9 | 3.5 | 6 | 5 | $-3$ | yes |
| 10 | 3.5 | 5 | 4 | 5 | no |
| 11 to 15 | 3 | 5 | 6 | 3 | no |
| 16 | 2.5 | 5 | 4 | 5 | no |

Once $\tau \le 3$, the global minimum 5 has no acceptable neighbor, so the walk stays there to the end.

The test of line L5 makes the traps different from those of simulated annealing. What matters is the largest *single* rise on a path out of a trap, not the total climb. From state 1, the two paths to state 5 have the rises $3, 3$ (through states 2, 3 and 4) and $2, 3$ (through states 0, 7 and 6). So a run that is in state 1 when $\tau$ drops to 3 or below never leaves the set $\{0, 1\}$. The total climb out of state 1 is 4, but a threshold of 3.5 is enough to leave it.

Over 100 runs (seeds 0 to 99) from state 0 with these thresholds, the best solution was the global minimum in 57 runs for $L = 5$, in 85 runs for $L = 10$ and in 99 runs for $L = 25$.

On 8 random points in the unit square (seed 3), with the 2-opt move and the thresholds $0.3 \cdot (10 - j + 1)/10$ for $j = 1, \dots, 10$ and $L = 100$, all 20 runs (seeds 0 to 19) found the optimal tour of length 2.7179. For this instance the mean rise of a random 2-opt move that goes up is about 0.36.

## Correctness

Threshold accepting always returns a solution that it visited, with the least value of $f$ among the visited solutions, by the same [loop invariant](/loop-invariant/) as simulated annealing. Its other guarantees are exact statements about which moves can happen. Let $G_\tau$ be the directed graph on $S$ with an edge $x \to y$ when $y \in N(x)$ and $f(y) - f(x) < \tau$.

1. **Every move is an edge of $G_{\tau_1}$.** An accepted move at stage $j$ is an edge of $G_{\tau_j} \subseteq G_{\tau_1}$, since the thresholds do not increase. So the walk stays in the set of states that $G_{\tau_1}$ reaches from $x_0$. If that set has no state better than some value, the method never finds one.
2. **The last stages are a descent.** Let $\delta$ be the smallest positive rise $f(y) - f(x)$ over all $x$ and $y \in N(x)$. At a stage with $\tau_j \le \delta$, only moves with $f(y) \le f(x)$ are accepted, so $f(x)$ does not increase from then on.
3. **The walk is a Markov chain** with the transition probabilities $R(x, y) \cdot [f(y) - f(x) < \tau_j]$. Unlike simulated annealing at a fixed temperature, it does not have the Boltzmann distribution as its equilibrium. A state $x$ with $f(x) - f(y) \ge \tau_j$ for every neighbor $y$ can never be entered at stage $j$.

The proofs are below. No result like Hajek's theorem gives a threshold sequence with a guarantee. Althöfer and Koschnick (1991) proved that sequences of thresholds exist under which threshold accepting reaches a global optimum with probability as close to 1 as wanted, but the proof does not give a practical rule to choose them.

## Complexity

Each step does one proposal and one change $f(y) - f(x)$, so $J$ stages of $L$ steps cost $O(JL \cdot c)$, where $c$ is the cost of a proposal and of the change. It saves the exponential function and the random number of the Metropolis test, which matters only when $c$ is very small. The extra space is $O(s)$ for $x$ and $best$. The number of steps for a given quality has no general bound, as for simulated annealing.

## Properties

- **Deterministic acceptance, randomized method.** Line L5 has no random number, but line L4 has. The old alias "deterministic annealing" refers to this acceptance test only.
- **Invariant under a shift of $f$.** Adding a constant to $f$ changes nothing. Multiplying $f$ by $a > 0$ needs the thresholds multiplied by $a$.
- **Single rise, not total climb.** A threshold $\tau$ lets the walk climb any height in steps smaller than $\tau$ each. This is the main difference from simulated annealing, where a long climb is unlikely even if each step is small.
- **Anytime.** $best$ is valid at each step.

## Variants and improvements

- **[Great deluge algorithm](/great-deluge-algorithm/).** Accept $y$ when $f(y)$ is below a falling level, an absolute bound instead of a bound on the change.
- **Record-to-record travel.** Accept $y$ when $f(y) < f(best) + D$ for a fixed deviation $D$. Dueck proposed it with the great deluge in 1993.
- **[Late acceptance hill climbing](/late-acceptance-hill-climbing/).** Compare $f(y)$ with the value of the current solution some fixed number of steps ago.
- **Thresholds from data.** Take the thresholds from the quantiles of the changes $|f(y) - f(x)|$ seen in a trial run, which removes the units of $f$. Winker and Fang used such data-driven sequences in statistics and econometrics.

## When to use it

Use threshold accepting where you would use [simulated annealing](/simulated-annealing/): a combinatorial problem with a natural move, a change of the objective that is cheap to compute, and many [local optima](/local-optimum/). It has one parameter less to think about, since there is no temperature to calibrate against the distribution of changes, but the thresholds play the same role. Run it with the same budget against simulated annealing, [iterated local search](/iterated-local-search/) and [tabu search](/tabu-search/) before you trust it on a new problem.

## Pitfalls

- **Equality in the test.** With $f(y) - f(x) \le \tau$ instead of $<$, a final threshold of 0 still accepts equal moves, and with $<$ it does not. Decide which you want, since plateaus are common in combinatorial problems.
- **A threshold in the wrong units.** If $\tau_1$ is much larger than the typical rise, the first stages are a random walk. If it is smaller than the smallest rise $\delta$, the method is a [hill climbing](/hill-climbing/) from the start.
- **Thresholds that drop too fast.** The walk can be left in a trap whose exit needs a single rise larger than all later thresholds, and it will stay there.
- **The name.** "Deterministic annealing" also names a different method of Rose and others for clustering, which minimizes a free energy over soft assignments. Do not mix them.
- **The title of the paper.** Dueck and Scheuer reported better results than simulated annealing on their test problems. That is a measurement on some instances, not a theorem.

## Implementations

## History

Dueck and Scheuer published threshold accepting in 1990 in the Journal of Computational Physics, with experiments on the traveling salesman problem. Dueck added the great deluge algorithm and record-to-record travel in 1993. Althöfer and Koschnick studied its convergence in 1991.

## References
