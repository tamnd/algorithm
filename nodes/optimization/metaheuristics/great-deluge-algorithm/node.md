---
tag: HPWTJM
kind: algorithm
slug: great-deluge-algorithm
name: Great deluge algorithm
aliases:
- great deluge
- GDA
area: optimization/metaheuristics
level: advanced
summary: Local search that accepts any neighbor whose objective is below a level, and lowers the level after each accepted move. The level bounds how many moves it can make.
solves: [global-optimization]
model: real-ram
complexity:
  vars: {k: the number of steps, c: the cost of one proposal and one value of the objective, s: the size of one solution}
  time: {worst: O(k c)}
  space: {extra: O(s)}
properties: {deterministic: false, iterative: true, anytime: true, population: false}
history:
  year: 1993
  people: [Gunter Dueck]
  note: Dueck proposed the great deluge algorithm and record-to-record travel in 1993, after threshold accepting.
prereqs: [threshold-accepting, local-search]
see_also: [simulated-annealing, cooling-schedule, late-acceptance-hill-climbing, hill-climbing, local-optimum, traveling-salesman-problem]
sources:
  - paper: doi:10.1006/jcph.1993.1010
    title: Gunter Dueck, New optimization heuristics, the great deluge algorithm and the record-to-record travel, Journal of Computational Physics 104(1), 1993
    locator: pages 86 to 92 (the rule with the rising water level for maximization, and record-to-record travel)
  - paper: "Edmund K. Burke, Yuri Bykov, James P. Newall and Sanja Petrovic, A time-predefined local search approach to exam timetabling problems, IIE Transactions 36(6), 2004"
    title: Edmund K. Burke, Yuri Bykov, James P. Newall and Sanja Petrovic, A time-predefined local search approach to exam timetabling problems
    locator: pages 509 to 528 (the level that falls by a fixed amount at each step, set from the time budget)
  - paper: doi:10.1016/0021-9991(90)90201-B
    title: Gunter Dueck and Tobias Scheuer, Threshold accepting, a general purpose optimization algorithm appearing superior to simulated annealing, Journal of Computational Physics 90(1), 1990
    locator: pages 161 to 175
  - book: isbn:9780470278581
    title: El-Ghazali Talbi, Metaheuristics, From Design to Implementation, Wiley, 2009
    locator: Chapter 2, the section on the variants of simulated annealing (great deluge and record-to-record travel)
---

The great deluge algorithm is a [local search](/local-search/) method that moves to a random neighbor whenever the value of the objective at the neighbor is below a level $B$, and lowers the level by a fixed amount $\rho$ after each accepted move. Dueck proposed it in 1993, after [threshold accepting](/threshold-accepting/). The test compares the neighbor with the level only, not with the current solution, so a worse neighbor is accepted when it is still below the level. Because the level falls with each move and the objective is bounded below, the number of accepted moves is at most $\lceil (B_0 - f^*)/\rho \rceil$. There is no result that says it finds a global minimum.

## In plain words

Think of a landscape in heavy rain, and of a walker who must keep dry feet. The water rises a little each time the walker takes a step. The walker looks at one random spot next to them and goes there if that spot is above the water. It does not matter if the spot is lower or higher than where the walker stands now.

At first the water is low, so the walker can go almost anywhere. As the water rises, more and more of the land is under water, and the walker is pushed onto the high islands. At the end the walker is stuck on one island, and the hope is that it is the highest one.

For a problem where low is good, turn this upside down: the level falls, and the walker must stay below it.

## The problem

The input is a finite set $S$ of solutions, an objective $f : S \to \mathbb{R}$ to minimize, a random move that draws a neighbor $y \in N(x)$ of a solution $x$, a start level $B_0$, a decrement $\rho > 0$ (Dueck calls it the rain speed) and a number of steps $K$. The goal is a solution with a small value of $f$, ideally a global minimum, the [global optimization](/global-optimization/) problem on a finite set. We write $f^* = \min_S f$.

## The algorithm

```pseudo id=main
GREAT-DELUGE(x₀, f, N, B₀, ρ, K)
L1  x ← x₀, best ← x₀, B ← B₀
L2  for k ← 1 to K do
L3      y ← a random neighbor of x
L4      if f(y) < B then                  ▷ f(x) is not used in the test
L5          x ← y
L6          B ← B − ρ
L7          if f(x) < f(best) then best ← x
L8  return best
```

Dueck wrote the rule for maximization, with a water level that rises by a fixed amount after each accepted move. The pseudocode is the same rule for minimization. A common start is $B_0 = f(x_0)$, or a bit above it.

## Example

Take the 8 states $0, \dots, 7$ on a cycle from the [simulated annealing](/simulated-annealing/) page, with the two cycle neighbors and

| state | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $f$ | 3 | 1 | 4 | 2 | 5 | 0 | 3 | 6 |

Start at $x_0 = 0$ with $B_0 = 6.5$, above every value, and $\rho = 0.5$. With a fixed seed, the first 13 steps are:

| step | $B$ | $x$ | $y$ | $f(y)$ | accepted |
|---|---|---|---|---|---|
| 1 | 6.5 | 0 | 7 | 6 | yes |
| 2 | 6.0 | 7 | 6 | 3 | yes |
| 3 | 5.5 | 6 | 7 | 6 | no |
| 4 | 5.5 | 6 | 5 | 0 | yes |
| 5 | 5.0 | 5 | 6 | 3 | yes |
| 6 to 8 | 4.5 | 6 | 7 | 6 | no |
| 9 | 4.5 | 6 | 5 | 0 | yes |
| 10 | 4.0 | 5 | 4 | 5 | no |
| 11 | 4.0 | 5 | 6 | 3 | yes |
| 12 | 3.5 | 6 | 5 | 0 | yes |
| 13 | 3.0 | 5 | 6 | 3 | no |

Step 5 accepts a move from the value 0 up to 3, which a [hill climbing](/hill-climbing/) step never does. From step 13 on, $B = 3$, and both neighbors of state 5 have $f \ge 3$, so no move is accepted again.

The level splits the cycle into islands. With $B$ in $(4, 5]$, the states with $f < B$ form the two paths $\{0, 1, 2, 3\}$ and $\{5, 6\}$, since states 4 and 7 are under the level. A walk that is on the first path when the level falls below 5 can never reach state 5.

Over 100 runs (seeds 0 to 99) from state 0 with $B_0 = 6.5$ and $K = 20000$ steps, the best solution was the global minimum in 28 runs for $\rho = 1$ and for $\rho = 0.5$, in 37 runs for $\rho = 0.25$, in 65 runs for $\rho = 0.1$, in 82 runs for $\rho = 0.05$ and in all 100 runs for $\rho = 0.01$. The largest number of accepted moves in a run was 5, 7, 15, 37, 71 and 351, against the bounds $\lceil 6.5/\rho \rceil = 7, 13, 26, 65, 130$ and 650.

On 8 random points in the unit square (seed 3), with the 2-opt move, $B_0$ equal to the length 4.2531 of the start tour $0, 1, \dots, 7$, and $K = 20000$, all 20 runs (seeds 0 to 19) found the optimal tour of length 2.7179 for each of $\rho = 0.01$, $0.003$ and $0.001$.

## Correctness

The method always returns the best solution it visited, by the same [loop invariant](/loop-invariant/) as simulated annealing. The other guarantees are about the level.

1. **Accepted values are below the level.** A state accepted when the level is $B$ has $f < B$. Since $B$ only decreases, once the level is $B$, every later accepted state has $f < B$.
2. **The number of moves is bounded.** If the run accepts $m$ moves, then $m \le \lceil (B_0 - f^*)/\rho \rceil$. After that many moves, the method only rejects.
3. **The current value is close to the level.** After the first accepted move, $f(x) < B + \rho$ at every step.
4. **Islands are traps.** Let $A$ be a set that contains $x$, and assume that every neighbor $j \notin A$ of a state in $A$ has $f(j) \ge B$, for the current level $B$. Then the walk never leaves $A$.

The proofs are below. None of them says that a global minimum is reached. Claim 4 shows the opposite: if the walk is on an island without a global minimum when the level falls below the lowest pass to a better island, it will not find one.

## Complexity

Each step does one proposal and one value $f(y)$, so $K$ steps cost $O(K c)$, where $c$ is the cost of a proposal and of the value. The extra space is $O(s)$ for $x$ and $best$. By Claim 2, at most $\lceil (B_0 - f^*)/\rho \rceil$ steps change the solution. This bounds the useful work in moves, but not in steps, since many proposals can be rejected between two moves. The quality for a given budget has no general bound.

## Properties

- **One parameter in the units of $f$.** The decrement $\rho$ sets the speed. A smaller $\rho$ means more moves and, on the instances above, better results.
- **The test ignores $f(x)$.** A move to a worse solution is accepted if it is below the level. This is the main difference from [threshold accepting](/threshold-accepting/), which bounds the change $f(y) - f(x)$.
- **The run ends by itself.** By Claim 2, the walk stops moving after a bounded number of moves, so a stopping rule can be a number of rejections in a row.
- **Invariant under a shift of $f$** if $B_0$ is shifted too. Multiplying $f$ by $a > 0$ needs $B_0$ and $\rho$ multiplied by $a$.
- **Anytime.** $best$ is valid at each step.

## Variants and improvements

- **Record-to-record travel.** Accept $y$ when $f(y) < f(best) + D$ for a fixed deviation $D$. The level follows the best value found, instead of falling at a fixed rate. Dueck proposed it in the same paper.
- **The level of Burke and Bykov.** Accept $y$ when $f(y) \le f(x)$ or $f(y) \le B$, and lower $B$ by $\rho = (B_0 - f_{\text{target}})/K$ at every step, so that the level reaches a target value exactly at the end of the budget of $K$ steps. This ties the speed to the time the user wants to spend, and it is common in timetabling.
- **Late acceptance.** [Late acceptance hill climbing](/late-acceptance-hill-climbing/) compares $f(y)$ with the value of the current solution some fixed number of steps ago.
- **Restarts.** When the walk stops moving, raise the level again and continue. This turns the method into a form of [iterated local search](/iterated-local-search/).

## When to use it

Use the great deluge where you would use [simulated annealing](/simulated-annealing/) or threshold accepting: a combinatorial problem with a natural move, a value that is cheap to compute, and many [local optima](/local-optimum/). The variant of Burke and Bykov is a good choice when the time budget is fixed in advance, since it has one parameter that the budget sets. Compare it with the same budget against the other methods before you trust it on a new problem.

## Pitfalls

- **A level that falls too fast.** By Claim 2, a large $\rho$ allows only a few moves. With $\rho = 1$ on the cycle above, a run makes at most 7 moves, and it found the global minimum in only 28 of 100 runs.
- **Rejected steps are not free.** Near the end, almost every proposal is rejected, so the run can spend most of its steps doing nothing. Stop after a number of rejections in a row.
- **A start level below $f(x_0)$.** The test ignores $f(x)$, so this is allowed, but if no neighbor is below the level, the walk never moves.
- **The test with equality.** With $\le$ instead of $<$, a move to a state equal to the level is accepted. Fix one choice and use it in the bound of Claim 2.
- **Maximization or minimization.** Dueck's paper maximizes with a rising level. Check the direction when you copy the rule.

## Implementations

## History

Dueck proposed the great deluge algorithm and record-to-record travel in 1993 in the Journal of Computational Physics, as simpler relatives of [threshold accepting](/threshold-accepting/) (Dueck and Scheuer, 1990) and of simulated annealing. Burke, Bykov, Newall and Petrovic made the level a function of the time budget in 2004 and used it for exam timetabling.

## References
