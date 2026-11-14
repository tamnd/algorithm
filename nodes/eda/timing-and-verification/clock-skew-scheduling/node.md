---
tag: K3PCDZ
kind: algorithm
slug: clock-skew-scheduling
name: Clock skew scheduling
aliases:
- useful skew
- Fishburn skew optimization
- clock schedule optimization
area: eda/timing-and-verification
level: advanced
summary: Fishburn's choice of clock arrival times at registers to shorten the clock period, a system of difference constraints solved by linear programming or cycle ratio.
model: real-ram
complexity:
  vars: {n: the number of registers, m: the number of register-to-register paths, R: the number of rounds, Δ: "the least period minus the start period, for integer delays"}
  time: {per_round: O(n m), total: O(R n m), integer_data: O(n^3 m Δ)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1990
  people: [John P. Fishburn]
  note: Fishburn stated clock skew optimization as a linear program in IEEE Transactions on Computers in 1990. Shenoy, Brayton and Sangiovanni-Vincentelli gave graph algorithms for it in 1992, and Albrecht, Korte, Schietke and Vygen tied it to maximum mean weight cycles.
prereqs: [setup-and-hold-constraints, difference-constraints, bellman-ford]
see_also: [negative-cycle-detection, karp-minimum-mean-cycle, dinkelbach-algorithm, fractional-programming, retiming, minimum-area-retiming, clock-tree-synthesis, static-timing-analysis]
sources:
  - paper: doi:10.1109/12.55696
    title: John P. Fishburn, Clock skew optimization, IEEE Transactions on Computers 39(7), 945 to 951, 1990
    locator: the setup (zero clocking) and hold (double clocking) constraints on each pair of registers, and the linear program for the least period
  - paper: "Narendra Shenoy, Robert K. Brayton and Alberto L. Sangiovanni-Vincentelli, Graph algorithms for clock schedule optimization, Proceedings of ICCAD 1992, 132 to 136"
    locator: the constraint graph of the clock schedule and the parametric shortest path view of the least period
  - paper: doi:10.1016/S0166-218X(01)00339-0
    title: Christoph Albrecht, Bernhard Korte, Jürgen Schietke and Jens Vygen, Maximum mean weight cycle in a digraph and minimizing cycle time of a logic chip, Discrete Applied Mathematics 123(1-3), 103 to 127, 2002
    locator: the least period as a maximum mean weight cycle when only the setup constraints are present
---

Clock skew scheduling chooses, for each register of a synchronous circuit, the time at which the clock edge reaches it, so that the clock period can be shorter than the longest path delay. The [setup and hold constraints](/setup-and-hold-constraints/) of every register-to-register path become [difference constraints](/difference-constraints/) on these clock arrival times. John Fishburn stated the problem as a linear program in 1990. The least period is a cycle ratio of the constraint graph, and the page computes it exactly by raising the period to the ratio of each [negative cycle](/negative-cycle/) that [Bellman-Ford](/bellman-ford/) finds, until none is left.

## In plain words

With a single clock, every register normally gets the clock edge at the same time. Then the clock period must be at least the slowest path between two registers. But some paths are fast and some are slow. If the clock reaches the end of a slow path a little later, that path gets more time, and the path that starts at that register gets less time. When the slow and the fast paths alternate, the clock period can go down.

There are limits. A path that is too fast can let the new data overwrite the old data before the next register has read it, so a register cannot be shifted too far. Each limit says that the clock time of one register minus that of another is at most some amount. A period works exactly when no loop of these limits adds up to a contradiction.

## The problem

Registers are $1, \ldots, n$. A path $p$ from register $i$ to register $j$ has a largest delay $d_{\max}(p)$ and a smallest delay $d_{\min}(p)$, from the clock pin of $i$ to the data pin of $j$. The registers have setup time $t_s$ and hold time $t_h$. With clock arrival times $c_1, \ldots, c_n$ and period $T$, each path must meet, in the notation of the [setup and hold](/setup-and-hold-constraints/) page with $c_{\text{launch}} = c_i$ and $c_{\text{capture}} = c_j$,

$$ c_i + d_{\max}(p) + t_s \le c_j + T, \qquad c_i + d_{\min}(p) \ge c_j + t_h. $$

The task is the least $T$ for which some $c$ meets all constraints, and such a $c$. The difference $c_i - c_j$ is the *skew* between the two registers. With all $c_i$ equal (zero skew), the least period is $\max_p (d_{\max}(p) + t_s)$, valid when every $d_{\min}(p) \ge t_h$.

Each constraint has the form $c_u - c_v \le w$. In the *constraint graph* it is an edge $v \to u$ of weight $w$: a setup edge $j \to i$ of weight $T - d_{\max}(p) - t_s$ and a hold edge $i \to j$ of weight $d_{\min}(p) - t_h$. By the theorem of difference constraints, $T$ is valid if and only if no cycle has negative weight. A cycle $C$ with $k_C$ setup edges has weight $k_C T - S_C$, where $S_C$ is the sum of $d_{\max} + t_s$ over its setup edges minus the sum of $d_{\min} - t_h$ over its hold edges. So the least period is the largest cycle ratio
$$ T^* = \max_{C,\ k_C \ge 1} \frac{S_C}{k_C}, $$
provided that no cycle of hold edges alone is negative; if one is, no period works. This is a [fractional programming](/fractional-programming/) problem over the cycles of a graph.

## The algorithm

```pseudo id=main
CLOCK-SKEW-SCHEDULE(registers, paths, t_s, t_h)
L1  if Bellman-Ford finds a negative cycle among the hold edges alone then return "no period works"
L2  T ← max over paths p of d_max(p) − d_min(p) + t_s + t_h
L3  loop
L4      run Bellman-Ford on the constraint graph at period T, from distance 0 at every node
L5      if no negative cycle is found then
L6          return T and c ← the distances, shifted so that the smallest is 0
L7      C ← the negative simple cycle found;  k ← its number of setup edges;  S ← k T − weight(C)
L8      T ← S / k
```

Line L2 is a lower bound: adding the setup and hold constraint of one path gives $T \ge d_{\max} - d_{\min} + t_s + t_h$. Line L7 always has $k \ge 1$, because line L1 removed the case of a negative cycle with no setup edge. Line L8 raises $T$ to the value at which the cycle $C$ has weight exactly 0. This is the iteration of [Dinkelbach](/dinkelbach-algorithm/) applied to the cycle ratio: each round either proves the current period valid or finds a cycle with a larger ratio.

## Example

Three registers $R_1, R_2, R_3$ have $t_s = t_h = 1$ and four paths:

| path | $d_{\max}$ | $d_{\min}$ | setup edge and weight | hold edge and weight |
| --- | --- | --- | --- | --- |
| $R_1 \to R_2$ | 9 | 5 | $R_2 \to R_1$, $T - 10$ | $R_1 \to R_2$, $4$ |
| $R_2 \to R_3$ | 3 | 2 | $R_3 \to R_2$, $T - 4$ | $R_2 \to R_3$, $1$ |
| $R_3 \to R_1$ | 4 | 1 | $R_1 \to R_3$, $T - 5$ | $R_3 \to R_1$, $0$ |
| $R_1 \to R_3$ | 6 | 2 | $R_3 \to R_1$, $T - 7$ | $R_1 \to R_3$, $1$ |

With zero skew the period is $9 + 1 = 10$. Line L2 starts at $T = 6$, from the paths $R_1 \to R_2$ and $R_1 \to R_3$.

| round | $T$ | negative cycle found | $k$ | $S$ | new $T$ |
| --- | --- | --- | --- | --- | --- |
| 1 | 6 | setup edges $R_1 \to R_3 \to R_2 \to R_1$ | 3 | 19 | 19/3 |
| 2 | 19/3 | hold $R_1 \to R_3$, setup $R_3 \to R_2 \to R_1$ | 2 | 13 | 13/2 |
| 3 | 13/2 | none | | | |

The least period is $T^* = 13/2$, with the schedule $c = (0, 7/2, 1)$. At this schedule the setup constraints of $R_1 \to R_2$ ($0 + 9 + 1 = 7/2 + 13/2$) and $R_2 \to R_3$ ($7/2 + 3 + 1 = 1 + 13/2$) and the hold constraint of $R_1 \to R_3$ ($0 + 2 = 1 + 1$) are tight. These three form the critical cycle of round 2. The short path $R_1 \to R_3$ stops the schedule from moving $R_3$ later, which would help the slow path $R_1 \to R_2 \to R_3$. Without the hold constraints the answer would be $19/3$, the mean of $d_{\max} + t_s$ over the loop $R_1 \to R_2 \to R_3 \to R_1$. The period drops from 10 to 6.5, by 35 percent, so the clock frequency can rise by a factor of $10 / 6.5 \approx 1.54$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). By the theorem of difference constraints a period is valid exactly when no simple cycle of the constraint graph is negative, so the valid periods form the half line $T \ge T^*$. The start $T_0$ is at most $T^*$, and each round moves $T$ to the ratio $S_C / k_C$ of a cycle that is negative at the current $T$, which is larger than $T$ and at most $T^*$. So $T \le T^*$ holds all the time, and when Bellman-Ford finds no negative cycle, $T$ is valid, so $T = T^*$. The distances of Bellman-Ford are a valid schedule.

## Complexity

Each round is one run of Bellman-Ford over the $2m$ constraint edges, $O(n m)$ time. A cycle found in one round has weight at least 0 in every later round, so no cycle comes back, and the loop stops. For integer delays and setup and hold times, every ratio is $S / k$ with $1 \le k \le n$, two distinct ratios differ by at least $1 / n^2$, and the number of rounds is at most $1 + n^2 (T^* - T_0)$. This bound is pseudo-polynomial; the page does not claim a polynomial bound on the rounds of this iteration. Polynomial methods exist: a [binary search on the answer](/binary-search-on-answer/) with one Bellman-Ford test per step, ended by rounding to the nearest fraction with denominator at most $n$, or [parametric search](/parametric-search/). The extra space is $O(n + m)$.

## Properties

- Exact. The returned period is the least valid period for the given delays, and the schedule meets every constraint at it.
- Deterministic, with exact rational arithmetic.
- The schedule is not unique. Any schedule of the polytope of valid schedules at $T^*$ works, and adding a constant to all $c_i$ changes nothing.
- The least period is never more than the zero skew period when zero skew is valid, since zero skew is one choice of $c$.
- Without hold constraints, $T^*$ is the largest mean of $d_{\max} + t_s$ over the cycles of register-to-register paths, which [Karp's algorithm](/karp-minimum-mean-cycle/) finds in $O(n m)$ time after the weights are negated.

## Variants and improvements

- **Linear program.** Fishburn minimizes $T$ subject to the constraints, a linear program in $n + 1$ variables. He also maximizes the smallest safety margin of all constraints at a fixed period, which gives a schedule more robust against delay variation.
- **Parametric shortest paths.** Shenoy, Brayton and Sangiovanni-Vincentelli treat $T$ as the parameter of a parametric shortest path problem on the constraint graph.
- **Maximum mean cycle.** Albrecht, Korte, Schietke and Vygen show that, with setup constraints only, the least period is a maximum mean weight cycle, and they study fast algorithms for it on the graphs of large chips.
- **Bounded skew windows.** In practice each $c_i$ must lie in a window that the [clock tree](/clock-tree-synthesis/) can deliver. A window $l_i \le c_i \le u_i$ is two more difference constraints with a fixed reference node, so the same algorithm applies.

## When to use it

Use it when the registers are fixed and the clock tree can be built to deliver chosen arrival times, and when the paths around a loop of registers are unbalanced. If the clock tree must have zero skew, use [retiming](/retiming/) instead, which moves the registers across the logic and keeps the clock; [minimum-area retiming](/minimum-area-retiming/) does so with the fewest registers. Both methods reduce to difference constraints, but retiming changes the circuit while skew scheduling changes only the clock times.

## Pitfalls

- Ignoring the hold constraints gives a shorter period that the circuit cannot use. In the example the setup constraints alone give $19/3$, but no schedule meets the hold constraints at that period.
- A cycle of hold edges alone with negative weight makes every period invalid. No skew can fix a race of that kind; the short paths must be made slower.
- A schedule computed for nominal delays has zero margin on its critical cycle. Variation of the clock tree delays breaks it, so a schedule for a real chip keeps a margin, for example with Fishburn's second linear program at a period above $T^*$.
- The word "skew" here is the difference of clock arrival times at two registers of one chip. In distributed systems, [clock skew](/clock-skew/) means the offset between the clocks of two processes, a different idea.
- Floating point Bellman-Ford can report a tiny negative cycle at $T^*$ itself and loop. Use exact rationals or stop when the increase of $T$ is below a tolerance.

## Implementations

## History

Fishburn published clock skew optimization in IEEE Transactions on Computers in 1990, with the setup and hold constraints of each pair of registers and the linear program for the least period. Shenoy, Brayton and Sangiovanni-Vincentelli gave graph algorithms based on the constraint graph at ICCAD 1992. Albrecht, Korte, Schietke and Vygen presented the link to the maximum mean weight cycle at ICCAD 1999 and in the journal version in Discrete Applied Mathematics in 2002.

## References
