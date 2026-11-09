---
tag: ZRSAWH
kind: algorithm
slug: late-acceptance-hill-climbing
name: Late acceptance hill climbing
aliases:
- LAHC
- late acceptance
area: optimization/metaheuristics
level: advanced
summary: Accept a move if it beats the solution from a fixed number of steps earlier.
model: word-ram
complexity:
  vars: {K: the number of iterations, e: the time to draw and evaluate one candidate, L: the length of the history list, s: the size of one solution}
  time: {worst: O(K e + L)}
  space: {extra: O(L + s)}
properties: {deterministic: false, recursive: false}
prereqs: [hill-climbing, local-optimum, neighborhood-structure]
see_also: [hill-climbing, simulated-annealing, threshold-accepting, great-deluge-algorithm, stochastic-local-search, two-opt, traveling-salesman-problem, tabu-list]
sources:
  - paper: doi:10.1016/j.ejor.2016.07.012
    title: Edmund K. Burke and Yuri Bykov, The late acceptance hill-climbing heuristic, European Journal of Operational Research 258(1), 2017
    locator: pp. 70 to 78 (the algorithm, the history list, the case L = 1, tests on the traveling salesman problem and exam timetabling)
  - paper: "Edmund K. Burke and Yuri Bykov, A late acceptance strategy in hill-climbing for exam timetabling problems, PATAT 2008 (Practice and Theory of Automated Timetabling), Montreal, 2008"
    locator: the conference version, the first presentation of the method
  - book: isbn:9781558608726
    title: Holger H. Hoos and Thomas Stützle, Stochastic Local Search, Foundations and Applications, Morgan Kaufmann, 2004
    locator: Section 2.2, 'Simple' SLS Methods, from p. 71 (acceptance rules that allow worse moves, such as threshold acceptance and simulated annealing)
---

Late acceptance hill climbing (LAHC) is a [local search](/local-search/) that accepts a candidate solution if it is no worse than the current solution, or no worse than the current solution was $L$ iterations ago. It keeps the last $L$ costs in a circular list, the *history list*. With $L = 1$ it is plain [hill climbing](/hill-climbing/) that accepts equal moves; with a larger $L$ it can accept worse moves, so it can leave a [local optimum](/local-optimum/). Burke and Bykov introduced it in 2008 and published the full study in 2017. Its appeal is that it has one parameter, $L$, and no cooling schedule, unlike [simulated annealing](/simulated-annealing/). It has no guarantee of reaching a global optimum.

## In plain words

A plain hill climber compares a new step only with where it stands now. Late acceptance compares the new step with where it stood some fixed number of steps ago, too. If the new step is no worse than either of the two, it takes the step.

So the walker can go a little uphill, but never higher than it was a while back. Early in the run, while the walker is high up, that leaves a lot of room. As the walker gets lower, the old positions in its memory get lower too, and the room to go uphill shrinks by itself. In the end the walker behaves like a plain downhill walker. The only setting is how many steps back it looks.

## The problem

The input is a set $S$ of solutions, an objective $f : S \to \mathbb{R}$ to minimize, a way to draw a random neighbor of a solution from a [neighborhood](/neighborhood-structure/) $N$, a start $x_0$, a history length $L \ge 1$ and a number of iterations $K$. The output is the best solution visited. The aim is a global minimum, but the algorithm cannot prove that it found one.

## The algorithm

```pseudo id=main
LATE-ACCEPTANCE(x0, f, N, L, K)
L1  x ← x0, b ← x0
L2  for v ← 0 to L − 1 do C[v] ← f(x0)
L3  for I ← 0 to K − 1 do
L4      y ← a random neighbor of x in N(x)
L5      v ← I mod L
L6      if f(y) ≤ C[v] or f(y) ≤ f(x) then x ← y      ▷ late or plain acceptance
L7      C[v] ← f(x)                                 ▷ store the current cost, accepted or not
L8      if f(x) < f(b) then b ← x
L9  return b
```

Line L5 picks the slot of the circular history list. The slot holds the cost of the current solution from $L$ iterations earlier, or $f(x_0)$ during the first $L$ iterations. Line L6 accepts the candidate if it is no worse than that old cost, or no worse than the current cost. Line L7 writes the current cost into the slot, whether the candidate was accepted or not. Line L8 keeps the best solution, since the current one can get worse.

## Example

Take eight cities in the plane at $(0,0)$, $(4,0)$, $(8,1)$, $(9,5)$, $(6,8)$, $(2,9)$, $(-1,6)$ and $(3,4)$, numbered 0 to 7, with distances rounded to the nearest integer. A candidate is a uniform random [2-opt](/two-opt/) neighbor of the current tour. Start from the tour 0 3 6 1 4 7 2 5 of length 66, with $L = 3$ and the random generator `random.Random(5)` of the Python code. The table shows the first 12 iterations.

| $I$ | $v$ | $f(y)$ | $C[v]$ | $f(x)$ before | accepted | $f(x)$ after |
|---|---|---|---|---|---|---|
| 0 | 0 | 60 | 66 | 66 | yes | 60 |
| 1 | 1 | 61 | 66 | 60 | yes, by $C[v]$ | 61 |
| 2 | 2 | 56 | 66 | 61 | yes | 56 |
| 3 | 0 | 61 | 60 | 56 | no | 56 |
| 4 | 1 | 57 | 61 | 56 | yes, by $C[v]$ | 57 |
| 5 | 2 | 50 | 56 | 57 | yes | 50 |
| 6 | 0 | 53 | 56 | 50 | yes, by $C[v]$ | 53 |
| 7 | 1 | 49 | 57 | 53 | yes | 49 |
| 8 | 2 | 49 | 50 | 49 | yes | 49 |
| 9 | 0 | 52 | 53 | 49 | yes, by $C[v]$ | 52 |
| 10 | 1 | 44 | 49 | 52 | yes | 44 |
| 11 | 2 | 50 | 49 | 44 | no | 44 |

At iteration 1 the candidate of length 61 is worse than the current 60, but it is no worse than $C[1] = 66$, the start cost, so it is accepted. At iteration 3 the candidate of length 61 is worse than the current 56 and worse than $C[0] = 60$, the cost after iteration 0, so it is rejected. The slots fill with lower costs as the run goes on, and the room to accept worse moves shrinks. With the same seed and 400 iterations, the run reaches length 33, which is the optimum of this instance by enumeration of all $7!$ tours that start at city 0.

## Correctness

LAHC has no optimality guarantee, so "correct" means the following. The run stops after $K$ iterations and returns the best solution among the visited ones. Each slot $C[v]$, when it is read at iteration $I \ge L$, holds the current cost at the end of iteration $I - L$. From this, the new cost is at most the larger of the current cost and that old cost, and so the largest of the last $L$ current costs never increases. In particular the current solution is never worse than the start, and with $L = 1$ the cost never increases at all. The [full proof](proofs/correctness.md) gives all steps.

## Complexity

Each iteration draws one candidate, evaluates it, and does $O(1)$ work on the list, so the time is $O(K e + L)$, where $e$ is the time to draw and evaluate a candidate and the term $L$ is the time to fill the list at line L2. With an incremental evaluation of the move, $e$ is often $O(1)$: for a 2-opt move the change in tour length depends on four edges. The extra space is the list of $L$ costs and a constant number of solutions, $O(L + s)$.

A larger $L$ lets the search accept more worse moves, so it settles later. On the 10-city instance described below, with 2000 iterations, the average number of accepted worse moves over 30 runs was 0 with $L = 1$, 29 with $L = 10$ and 158 with $L = 50$.

## Properties

- **One parameter.** The only setting is $L$. There is no temperature and no schedule.
- **Invariant to monotone changes of $f$.** The test of line L6 compares costs only. Replace $f$ by $g(f)$ for an increasing $g$, and the run is the same. [Simulated annealing](/simulated-annealing/) does not have this property, since it uses differences of costs.
- **The window maximum never rises.** The largest of the last $L$ current costs does not increase, so the search drifts downhill on that scale, with an implicit schedule set by the run itself.
- **Randomized.** The candidates are random, and different seeds give different runs.
- **No optimality guarantee.** It returns the best solution seen in $K$ iterations, with no proof that it is optimal, or even a local optimum of $N$.

## Variants and improvements

- **$L = 1$.** The method becomes hill climbing with random candidates that accepts equal moves; it can drift along plateaus.
- **Stopping by idle iterations.** Burke and Bykov stop the run after a number of iterations with no improvement, not after a fixed $K$, since the time to settle grows with $L$.
- **Other list-free and schedule-free rules.** [Threshold accepting](/threshold-accepting/) accepts a worse move within a fixed or scheduled threshold, and the [great deluge algorithm](/great-deluge-algorithm/) accepts any move below a level that falls over time. LAHC derives its level from the history of the run.
- **Restarts and hybrids.** As with any local search, several runs from random starts, or a perturbation step as in [iterated local search](/iterated-local-search/), can be added on top.

## When to use it

Use LAHC when you want a method that can leave local optima, has a single parameter, and needs no tuning of a schedule. It suits problems with cheap random moves and incremental evaluation, such as tours and timetables, the two classes on which Burke and Bykov tested it. A larger $L$ usually gives better final solutions but needs more iterations.

On one 10-city instance (cities with integer coordinates in $[0, 100]$ drawn from Python `random.Random(2024)`, optimum 231 by enumeration), 30 runs of 2000 iterations from the tour $0, 1, \ldots, 9$ with seeds 0 to 29 reached the optimum in 21 runs with $L = 1$, 27 with $L = 2$, 25 with $L = 5$ and with $L = 10$, 27 with $L = 20$, and 30 with $L = 50$. This is one small instance, not a ranking. Prefer an exact method on instances this small; prefer [tabu search](/tabu-search/) when a full scan of the neighborhood is cheap.

## Pitfalls

- **Updating the list only on acceptance.** Line L7 writes the current cost every iteration. If the write happens only when a candidate is accepted, the slot no longer holds the cost from $L$ iterations earlier, and the invariant of the proof breaks.
- **Returning the current solution.** The current solution can be worse than the best one seen. Return $b$.
- **Too few iterations for a large $L$.** A large $L$ accepts worse moves for a long time. If $K$ is small compared with $L$, the run stops before the search has settled, and the result can be worse than with a small $L$.
- **Strict test.** Line L6 uses $\le$. With $<$, equal moves are rejected and the search cannot move on a plateau.

## Implementations

## History

Burke and Bykov presented late acceptance at the PATAT conference in 2008, on exam timetabling, and published the full study in the European Journal of Operational Research in 2017, with tests on the traveling salesman problem and on exam timetabling.

## References
