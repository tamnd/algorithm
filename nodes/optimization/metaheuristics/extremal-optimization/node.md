---
tag: ZRWP63
kind: algorithm
slug: extremal-optimization
name: Extremal optimization
aliases:
- EO
- tau-EO
area: optimization/metaheuristics
level: research
summary: Local search that gives each variable a local fitness, ranks the variables, and always changes a poor one, chosen by a power law over the ranks. It has no acceptance test.
solves: [global-optimization]
model: real-ram
complexity:
  vars: {k: the number of steps, n: the number of variables, d: the largest number of variables that share a term with one variable}
  time: {worst: O(k n (d + log n))}
  space: {extra: O(n)}
properties: {deterministic: false, iterative: true, anytime: true, population: false}
history:
  year: 2000
  people: [Stefan Boettcher, Allon G. Percus]
  note: Boettcher and Percus proposed extremal optimization in 1999 and 2000, after the Bak and Sneppen model of evolution.
prereqs: [local-search, ising-model]
see_also: [simulated-annealing, maximum-cut, graph-partitioning-problem, local-optimum, fitness-function, binary-heap]
sources:
  - paper: "Stefan Boettcher and Allon G. Percus, Nature's way of optimizing, Artificial Intelligence 119(1-2), 2000"
    title: Stefan Boettcher and Allon G. Percus, Nature's way of optimizing
    locator: pages 275 to 286 (basic EO and tau-EO on graph partitioning)
  - paper: doi:10.1103/PhysRevLett.86.5211
    title: Stefan Boettcher and Allon G. Percus, Optimization with extremal dynamics, Physical Review Letters 86(23), 2001
    locator: pages 5211 to 5214 (tau-EO on spin glasses, and the choice of tau near 1 + 1/ln n)
  - paper: doi:10.1103/PhysRevLett.71.4083
    title: Per Bak and Kim Sneppen, Punctuated equilibrium and criticality in a simple model of evolution, Physical Review Letters 71(24), 1993
    locator: pages 4083 to 4086 (the model that replaces the least fit species)
  - book: isbn:9780470278581
    title: El-Ghazali Talbi, Metaheuristics, From Design to Implementation, Wiley, 2009
    locator: Chapter 2, single-solution based metaheuristics
---

Extremal optimization (EO) is a [local search](/local-search/) method for problems whose objective is a sum of terms over the variables. It gives each variable a local fitness, ranks the variables from the worst to the best, and changes the variable of rank $k$, where $k$ is drawn with probability proportional to $k^{-\tau}$. The change is always made, with no acceptance test, and the method keeps the best solution it has seen. Boettcher and Percus proposed it in 1999 and 2000, after the Bak and Sneppen model of evolution. The only guarantee is the weak one of any walk that can reach every solution: with enough steps it sees a global minimum with probability tending to 1.

## In plain words

Think of a team where each member gets a score for how well they fit with the others. A simple rule is: always replace the worst member. But that rule can get stuck, since the same few members keep getting replaced in a loop.

Extremal optimization ranks the members from the worst to the best. It then picks one to change, mostly from the bottom of the list, but now and then from higher up. The chance falls fast as you go up the list. The change is always made, even if the whole team gets worse for a moment.

It does not ask if the change is good. It only keeps a copy of the best team it has seen.

## The problem

The input is a set of $n$ variables, a solution $s$ that gives a value to each variable, an objective $C(s)$ to minimize, and a local fitness $\lambda_i(s)$ for each variable $i$, with a large $\lambda_i$ meaning that $i$ is in a good state. EO needs $C$ to be built from the $\lambda_i$, usually $C(s) = -\tfrac{1}{2}\sum_i \lambda_i(s)$ or a similar sum, so that improving poor variables tends to improve $C$. The goal is a solution with a small $C$, ideally a global minimum.

The standard test case is the $\pm J$ spin glass, an [Ising model](/ising-model/) with random signs. The variables are the spins $s_i \in \{-1, +1\}$, the couplings are $J_{ij} = J_{ji} \in \{-1, 0, +1\}$, and
$$E(s) = -\sum_{i < j} J_{ij} s_i s_j, \qquad \lambda_i(s) = s_i \sum_{j \ne i} J_{ij} s_j, \qquad E(s) = -\tfrac{1}{2}\sum_i \lambda_i(s).$$
Flipping spin $i$ changes the energy by exactly $2\lambda_i$. Finding a ground state is the same as a [maximum cut](/maximum-cut/) with weights $\pm 1$, which is NP-hard in general.

## The algorithm

```pseudo id=main
TAU-EO(s, λ, C, τ, K)
L1  best ← s
L2  for t ← 1 to K do
L3      compute λ_i(s) for all i
L4      order the variables so that λ_π(1) ≤ λ_π(2) ≤ … ≤ λ_π(n)
L5      draw a rank k with P(k) = k^(−τ) / Σ_{m=1}^{n} m^(−τ)
L6      change variable π(k) to a new value      ▷ always, no test
L7      if C(s) < C(best) then best ← s
L8  return best
```

For spins, the new value of line L6 is the flip $s_i \leftarrow -s_i$. In graph partitioning, Boettcher and Percus move the chosen vertex to the other part and then move a random vertex of the other part back, to keep the parts equal. The implementation breaks ties in line L4 by the index of the variable.

Basic EO is the limit $\tau \to \infty$: always change the worst variable. Boettcher and Percus report that $\tau$ near $1 + 1/\ln n$ works well on their test problems. That is an empirical rule with a heuristic argument, not a theorem.

## Example

Take $n = 12$ spins with all 66 couplings $J_{ij} \in \{-1, +1\}$ drawn with seed 1, and the start $s = (1, \dots, 1)$ with $E = -4$. An exhaustive search over the $2^{12}$ configurations gives the ground energy $-28$. With $\tau = 1.4$ and seed 0, the first 9 steps are:

| step | rank $k$ | spin | $\lambda_i$ | $E$ before | $E$ after |
|---|---|---|---|---|---|
| 1 | 6 | 5 | 1 | $-4$ | $-2$ |
| 2 | 4 | 5 | $-1$ | $-2$ | $-4$ |
| 3 | 1 | 2 | $-5$ | $-4$ | $-14$ |
| 4 | 1 | 8 | $-1$ | $-14$ | $-16$ |
| 5 | 2 | 0 | 1 | $-16$ | $-14$ |
| 6 | 1 | 11 | $-5$ | $-14$ | $-24$ |
| 7 | 4 | 5 | 1 | $-24$ | $-22$ |
| 8 | 1 | 7 | $-3$ | $-22$ | $-28$ |
| 9 | 2 | 5 | 1 | $-28$ | $-26$ |

Each change is exactly $2\lambda_i$. Steps 1, 5, 7 and 9 make the energy worse, and EO makes them anyway. After step 8 the solution is a ground state, and $best$ keeps it.

**Measured results.** Take $n = 16$ spins with couplings drawn with seed 1, the start $(1, \dots, 1)$ with $E = 0$, and the ground energy $-38$ from an exhaustive search. Over 100 runs (seeds 0 to 99), the number of runs whose best energy was $-38$ was:

| $\tau$ | $K = 50$ | $K = 200$ | $K = 1000$ |
|---|---|---|---|
| 0 (random flips) | 0 | 1 | 9 |
| 1.0 | 31 | 90 | 100 |
| 1.361 $= 1 + 1/\ln 16$ | 52 | 94 | 100 |
| 2.0 | 33 | 87 | 100 |
| 3.0 | 18 | 47 | 91 |
| 50 (almost basic EO) | 0 | 0 | 0 |

With $\tau = 50$, rank 1 is drawn with probability above $1 - 10^{-14}$, so all 100 runs follow the same deterministic path, which cycles without reaching the ground state. On the smaller instance with 12 spins, every $\tau \ge 1$ reached the ground state in all 100 runs with $K = 200$, so that instance does not separate the values of $\tau$.

## Correctness

EO returns the best solution it visited, by the same [loop invariant](/loop-invariant/) as simulated annealing. The other claims are exact facts about one step.

1. **Each step is a known change.** For the spin glass, flipping spin $i$ changes $E$ by $2\lambda_i$, and $E = -\tfrac{1}{2}\sum_i \lambda_i$.
2. **Every variable can be chosen.** For a finite $\tau$, each rank $k$ has probability at least $p = n^{-\tau}/\sum_{m=1}^{n} m^{-\tau} > 0$, so each spin is flipped with probability at least $p$ at each step, whatever the state.
3. **A weak convergence result.** By Claim 2, from any state, the walk reaches a given ground state in at most $n$ steps with probability at least $p^n$. So the probability that $K$ steps never see a ground state is at most $(1 - p^n)^{\lfloor K/n \rfloor}$, which tends to 0. For $n = 12$ and $\tau = 1.4$, $p \approx 0.014$ and $p^n$ is about $10^{-22}$, so this bound says nothing useful for a real budget.

The proofs are below. There is no result that EO finds a ground state faster than this bound in general, and basic EO ($\tau = \infty$) has no such result at all, since it is deterministic once ties are fixed and can cycle.

## Complexity

Line L3 costs $O(nd)$ if each variable shares terms with at most $d$ others, and line L4 costs $O(n \log n)$ by sorting. So $K$ steps cost $O(Kn(d + \log n))$, with $O(n)$ extra space. A flip of spin $i$ changes only $\lambda_i$ and the $\lambda_j$ of its neighbors, so an implementation can update $d + 1$ values instead of $n$. For large $n$, Boettcher and Percus suggest keeping the variables in a [binary heap](/binary-heap/) ordered by $\lambda$ and drawing the rank from the levels of the heap. This gives an approximate ranking at a cost of about $O(d \log n)$ per step. The implementation on this page recomputes and sorts, which is simpler and fine for small $n$.

## Properties

- **No acceptance test.** Every step changes the solution. The walk leaves a local minimum on the next step, so no [cooling schedule](/cooling-schedule/) is needed.
- **One parameter.** Only $\tau$ is set, and it does not depend on the units of $C$, since only the ranks of the $\lambda_i$ matter.
- **Invariant under monotone changes of the fitness.** Replacing every $\lambda_i$ by $g(\lambda_i)$ for an increasing $g$ gives the same ranks and the same run.
- **Needs a local fitness.** The method uses the structure of $C$ as a sum over variables. For a black-box $C$, a local fitness must be made up, for example from the change of $C$ when one variable changes, which costs $n$ values of $C$ per step.
- **Anytime.** $best$ is valid at each step.

## Variants and improvements

- **Basic EO** ($\tau = \infty$): always change the worst variable. It is deterministic up to ties and often cycles.
- **Generalized EO.** De Sousa and Ramos encode the solution in bits and define the fitness of a bit as the change of $C$ when that bit is flipped. This makes the rank rule work on a black-box objective, at the cost of $n$ values of $C$ per step.
- **EO with a cheap local search.** Run a [hill climbing](/hill-climbing/) step from the best solution at the end, or alternate EO with short descents.
- **Population EO.** Run several EO walks and share the best solution between them.

## When to use it

Use EO on problems where the objective is a sum of local terms and a local fitness is natural: spin glasses, [graph partitioning](/graph-partitioning-problem/), graph coloring and satisfiability with a count of unsatisfied clauses per variable. It has one parameter and no temperature to calibrate, which makes it easy to try. Compare it with [simulated annealing](/simulated-annealing/), [tabu search](/tabu-search/) and [WalkSAT](/walksat/) under the same budget, since none of them is better on all problems.

## Pitfalls

- **Basic EO cycles.** With $\tau = \infty$ the walk often repeats a short cycle, as in the table above. Use a finite $\tau$.
- **A $\tau$ that is too small.** Near $\tau = 0$ the rank is close to uniform and the method is a random walk, which found the ground state in only 9 of 100 runs with 1000 steps above.
- **Forgetting to keep $best$.** The current solution is often worse than the best one, since every step changes it.
- **Ties in the ranks.** With integer fitness values, many variables share a rank. How ties are broken changes the run. Fix the rule.
- **The local fitness must match the objective.** If improving the worst $\lambda_i$ does not tend to lower $C$, the method has no reason to work.

## Implementations

## History

Bak and Sneppen proposed in 1993 a model of evolution in which the least fit species and its neighbors are replaced by random ones at each step. The model shows self-organized criticality: long quiet periods broken by avalanches of change. Boettcher and Percus turned this rule into an optimization method in 1999 and 2000, first on graph partitioning, and introduced the power law over the ranks ($\tau$-EO) to stop the cycling of basic EO. In 2001 they applied it to spin glasses.

## References
