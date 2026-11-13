---
tag: DYGENX
kind: problem
slug: water-jug-problem
name: Water jug problem
aliases:
- Die Hard water jugs
- Two-jug problem
area: games-and-search/puzzles
level: intro
summary: "Measure an exact amount of water with jugs of fixed capacities by filling, emptying and pouring; with two jugs of a and b units, c is measurable exactly when gcd(a, b) divides c and c <= max(a, b)."
prereqs: [greatest-common-divisor, breadth-first-search]
see_also: [bezouts-identity, extended-euclidean-algorithm, linear-diophantine-equation, state-space, implicit-graph, missionaries-and-cannibals, tower-of-hanoi, np-hard]
sources:
  - paper: doi:10.1016/S0304-3975(01)00060-3
    title: "Paolo Boldi, Massimo Santini and Sebastiano Vigna, Measuring with jugs, Theoretical Computer Science 282(2), 2002"
    locator: "pp. 259-270"
  - paper: doi:10.1016/j.tcs.2008.01.003
    title: "Min-Zheng Shieh and Shi-Chun Tsai, Jug measuring: algorithms and complexity, Theoretical Computer Science 396(1-3), 2008"
    locator: "pp. 50-62"
---

The water jug problem asks for a sequence of steps that leaves an exact amount of water in a jug, when the only tools are jugs of fixed capacities without marks, a tap and a drain. With two jugs of $a$ and $b$ units, an amount $c$ can be measured exactly when $\gcd(a, b)$ divides $c$ and $c \le \max(a, b)$, which is [Bézout's identity](/bezouts-identity/) in the form of a puzzle. A shortest solution comes from a [breadth-first search](/breadth-first-search/) over at most $(a + 1)(b + 1)$ states, and with many jugs the shortest solution is [NP-hard](/np-hard/) to find.

## In plain words

You have a small jug and a large jug, neither with any marks, a tap and a sink. You want exactly four litres. You can fill a jug to the top, empty it into the sink, or pour one jug into the other until the first is empty or the second is full. Each step leaves every jug either empty, full, or holding what pouring left in it. So you can only reach amounts that the two sizes can build by adding and taking away whole jugfuls. With jugs of three and five litres, four is possible: fill the five, pour it into the three, empty the three, pour the two that remain into it, fill the five again and top up the three. Jugs of four and six litres can never give an odd amount.

## Definition

**Instance.** Capacities $a, b \ge 1$ and a target $c \ge 0$, all integers.

**States.** A state is a pair $(x, y)$ with $0 \le x \le a$ and $0 \le y \le b$: the amounts in jug A and jug B. The start is $(0, 0)$.

**Steps.** There are six kinds of step:

- fill A: $(x, y) \to (a, y)$; fill B: $(x, y) \to (x, b)$;
- empty A: $(x, y) \to (0, y)$; empty B: $(x, y) \to (x, 0)$;
- pour A into B: $(x, y) \to (x - t, y + t)$ with $t = \min(x, b - y)$;
- pour B into A: $(x, y) \to (x + u, y - u)$ with $u = \min(y, a - x)$.

**Problem.** Decide whether some sequence of steps from $(0, 0)$ reaches a state with $x = c$ or $y = c$, and if so find a shortest one.

The steps define a directed graph on the states, because a step cannot always be undone in one step: "empty A" takes $(2, 5)$ to $(0, 5)$ for jugs of 3 and 5, and no step takes $(0, 5)$ back to $(2, 5)$.

## Variants

- **Total amount.** The target is $c$ units in the two jugs together. With two jugs every multiple of $\gcd(a, b)$ from 0 to $a + b$ is reachable as a total.
- **Three jugs and no tap.** The classical decanting puzzle has jugs of 8, 5 and 3 units, the large one full, and asks to split the 8 units into two halves of 4 using only pours. There is no tap and no drain, so the total stays 8.
- **Many jugs.** With $k$ jugs and a tap, Boldi, Santini and Vigna study which amounts are measurable and give upper and lower bounds on the number of steps.
- **Cost of steps.** Some versions count only pours, or charge each step by the volume of water it moves.

## Examples

**Die Hard.** In the 1995 film *Die Hard with a Vengeance* the heroes must leave exactly 4 gallons on a scale, with jugs of 3 and 5 gallons. Write the state as (A, B) with A the 3-gallon jug. A shortest solution has 6 steps:

| step | action | state |
|---|---|---|
| 1 | fill B | (0, 5) |
| 2 | pour B into A | (3, 2) |
| 3 | empty A | (0, 2) |
| 4 | pour B into A | (2, 0) |
| 5 | fill B | (2, 5) |
| 6 | pour B into A | (3, 4) |

The other approach, filling the 3-gallon jug and pouring it into the 5-gallon jug, needs 8 steps.

**Shortest solutions for the jugs 3 and 5.**

| target $c$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| fewest steps | 0 | 4 | 2 | 1 | 6 | 1 |

The 16 reachable states are the pairs with $x \in \{0, 3\}$ or $y \in \{0, 5\}$, which is $2(3 + 5)/1 = 16$.

**Impossible targets.** With jugs of 4 and 6, only even amounts appear, so 3 is never measured. With jugs of 3 and 5, the amount 6 does not fit in either jug, although it is reachable as a total.

**Bachet's 8, 5 and 3.** From (8, 0, 0) the shortest way to (4, 4, 0) uses 7 pours: (3, 5, 0), (3, 2, 3), (6, 2, 0), (6, 0, 2), (1, 5, 2), (1, 4, 3), (4, 4, 0). Of the 24 triples with sum 8 that fit the jugs, 16 are reachable.

## Known algorithms

- **The gcd test.** Compute $g = \gcd(a, b)$ with the [Euclidean algorithm](/euclidean-algorithm/) and answer yes exactly when $g \mid c$ and $c \le \max(a, b)$. This takes $O(\log \min(a, b))$ arithmetic steps and gives no plan.
- **Breadth-first search.** Run a [breadth-first search](/breadth-first-search/) on the [implicit graph](/implicit-graph/) of states from $(0, 0)$, with six successors per state, and stop at the first state that holds $c$ in a jug. Parent links give a shortest plan. A table over all $(a + 1)(b + 1)$ pairs costs $O(ab)$; with a hash set the search touches only the $2(a + b)/g$ reachable states, so it costs $O((a + b)/g)$ expected time and space; this is pseudo-polynomial, because $a$ and $b$ are written in $O(\log a + \log b)$ bits.
- **The two cycling runs.** Run A into B: fill A when it is empty, otherwise empty B when it is full, otherwise pour A into B. Run B into A is the mirror. When B is the larger jug, the run A into B passes through every measurable amount (see the proof below). On every pair of capacities up to 20, the shorter of the two runs to reach $c$ is a shortest solution.
- **Plans from Bézout coefficients.** Let B be the larger jug and $g \mid c < b$. The [extended Euclidean algorithm](/extended-euclidean-algorithm/) gives the smallest $u \ge 0$ with $ua \equiv c \pmod b$, and the run A into B holds $c$ in B right after the $u$-th fill of A has been poured out. So the length and shape of that run follow in $O(\log b)$ arithmetic steps, without a search.
- **Many jugs.** Shieh and Tsai give a pseudo-polynomial algorithm for the fewest steps and a polynomial approximation based on [LLL lattice reduction](/lll-algorithm/).

## Bounds

**The gcd rule.** Let $g = \gcd(a, b)$. Then $c$ can be left in one jug if and only if $g \mid c$ and $0 \le c \le \max(a, b)$.

*Necessity.* In the start state both amounts are 0, a multiple of $g$. Fill and empty set an amount to $0$, $a$ or $b$, all multiples of $g$. A pour moves $t = \min(x, b - y)$ or $u = \min(y, a - x)$ units, a multiple of $g$ when $x$ and $y$ are. So every reachable amount is a multiple of $g$, and an amount in a jug is at most its capacity.

*Sufficiency.* Let B be the larger jug, $b \ge a$, and run A into B. Count the fills of A. Right after the $k$-th fill of A has been poured out completely, B holds $ka \bmod b$ units: the system has received $ka$ units from the tap and lost a multiple of $b$ to the drain, B holds less than $b$, and if B was exactly full the next step empties it. Since $a/g$ and $b/g$ are coprime, the residues $ka \bmod b$ for $k = 0, 1, \dots, b/g - 1$ are all the multiples of $g$ in $[0, b)$. So every multiple of $g$ below $b$ appears in B, and $b$ itself appears after "fill B". $\square$

**Reachable states.** Every step leaves at least one jug empty or full, so every reachable state lies on the boundary of the $a \times b$ rectangle, and both amounts are multiples of $g$. Exactly $2(a + b)/g$ such states exist, and all of them are reachable. A shortest solution therefore has at most $2(a + b)/g - 1$ steps.

**Complexity.** With $k$ jugs, deciding whether a given amount is measurable within a given number of steps is NP-complete, so finding a shortest solution is NP-hard (Shieh and Tsai). With two jugs the BFS above is polynomial in $a + b$, and the test of the gcd rule is polynomial in the input length.

## Reductions

- **Linear Diophantine equations.** A two-jug plan that fills A $u$ times and empties B $v$ times ends with $ua - vb$ units in total, so measurability reduces to the [linear Diophantine equation](/linear-diophantine-equation/) $ua - vb = c$ with $u, v \ge 0$, plus the capacity limit.
- **State-space search.** The puzzle is a small [state space](/state-space/) with a directed move relation, the same shape as [missionaries and cannibals](/missionaries-and-cannibals/), [Tower of Hanoi](/tower-of-hanoi/) and the [sliding tile puzzle](/sliding-tile-puzzle/), so any [graph reachability](/graph-reachability/) or shortest path method applies.

## Applications

- Teaching the [greatest common divisor](/greatest-common-divisor/) and [Bézout's identity](/bezouts-identity/): the sufficiency proof is the proof that $ka \bmod b$ runs through all multiples of $g$.
- Teaching [state-space search](/state-space-search/): the graph is small enough to draw, and it shows directed moves and unreachable states.
- Measuring with containers: the same arithmetic decides which doses a set of fixed measures can give.

## References
