---
tag: PNFW75
kind: technique
slug: dsp-folding
name: Folding transformation
aliases:
- Parhi folding
- time-multiplexing transformation
area: eda/high-level-synthesis-and-scheduling
level: advanced
summary: Maps several operations of a data flow graph onto one hardware unit by time multiplexing and computes the registers each folded edge needs from a folding equation.
prereqs: [retiming, iteration-bound, difference-constraints]
see_also: [dsp-unfolding, sdc-modulo-scheduling, resource-binding, register-binding, bellman-ford, finite-state-machine-with-datapath, iir-filter, fir-filter]
sources:
  - book: isbn:9780471241867
    title: Keshab K. Parhi, VLSI Digital Signal Processing Systems, Design and Implementation, Wiley, 1999
    locator: Chapter 6 (6.2 the folding transformation and the folding equation, retiming for folding, 6.3 and 6.4 register minimization, 6.5 multirate folding)
  - paper: "Keshab K. Parhi, Ching-Yi Wang and Andrew P. Brown, Synthesis of control circuits in folded pipelined DSP architectures, IEEE Journal of Solid-State Circuits 27(1), 29 to 43, 1992"
    title: Keshab K. Parhi, Ching-Yi Wang and Andrew P. Brown, Synthesis of control circuits in folded pipelined DSP architectures, IEEE Journal of Solid-State Circuits 27(1), 29 to 43, 1992
    locator: the folding of data flow graphs onto pipelined units, the register counts of the folded edges, and the control circuits of the switches
  - paper: "Charles E. Leiserson and James B. Saxe, Retiming synchronous circuitry, Algorithmica 6, 5 to 35, 1991"
    title: Charles E. Leiserson and James B. Saxe, Retiming synchronous circuitry, Algorithmica 6, 5 to 35, 1991
    locator: retiming as a system of difference constraints, used here to make every folded edge nonnegative
---

Folding is the opposite of [unfolding](/dsp-unfolding/): it runs several operations of a data flow graph on one hardware unit, one after another, so that a design needs fewer adders and multipliers at the price of a faster clock. With folding factor $N$, every unit repeats a cycle of $N$ clock steps, and in each step it runs the operation that the folding set puts there. The folded circuit needs registers to hold each result from the step in which it leaves its unit to the step in which its consumer runs, and switches that route the right value into each unit input at the right step. The folding equation gives the number of registers of each edge in closed form, and when some count comes out negative, a [retiming](/retiming/) found from a system of [difference constraints](/difference-constraints/) repairs it or proves that no retiming can. The method is due to Parhi and his students, and Parhi's 1999 textbook gives it in the form used here.

## In plain words

A kitchen has one oven but a recipe with three baking steps per batch. The cook bakes the three steps in a fixed rotation, one per hour, so a batch comes out every three hours. Something baked in the first hour may be needed only in the third, so it sits on a shelf in between. Folding works out, for each step of the recipe, how many hours its result must sit on the shelf. If the answer is negative, the result would be needed before it is ready; then some old results are moved around the recipe, without changing what the recipe makes, until every wait is zero or more.

## When it applies

- The graph is a data flow graph as on the [iteration bound](/iteration-bound/) page, such as a digital filter, and its sample rate is much lower than the clock rate the hardware can reach. Then $N$ operations can share a unit.
- The operations come in a few types (adds, multiplies), so a few units can serve many operations.
- A schedule and binding are given or can be chosen: the folding set, which gives each operation a unit and a step in $\{0, \ldots, N - 1\}$. This is a [modulo schedule](/sdc-modulo-scheduling/) with initiation interval $N$, written in the language of signal processing.
- The units may be pipelined: a unit $H$ with $P_H$ stages gives its result $P_H$ steps after it starts, and can start a new operation every step.

## The template

The input is a data flow graph with edges $e = (U, V)$ carrying $w(e)$ delays, the folding factor $N$, and a folding set: each operation $U$ gets a unit $H_U$ and a folding order $u \in \{0, \ldots, N - 1\}$, written in lower case, with no two operations on one unit sharing an order. Iteration $l$ of $U$ then runs in clock step $Nl + u$ on $H_U$, and its result is ready at step $Nl + u + P_{H_U}$, written $P_U$ for short.

```pseudo id=main
FOLD(G, N, H, order, P)
L1  for each edge e = U → V do D_F(e) ← N · w(e) − P_U + v − u
L2  if some D_F(e) < 0 then
L3      solve r(U) − r(V) ≤ ⌊D_F(e) / N⌋ for every edge e = U → V, with r ≥ 0
L4      if there is no solution then fail: no retiming makes this folding set work
L5      for each edge e = U → V do w(e) ← w(e) + r(V) − r(U); recompute D_F(e) by L1
L6  for each edge e = U → V do
L7      wire the output of H_U through a chain of D_F(e) registers to an input switch of H_V
L8      close that switch in the steps Nl + v, l = 0, 1, 2, ...
L9  return the folded circuit
```

The holes are the factor $N$, the folding set (which unit and which step for each operation), the pipelining $P$ of each unit, and the register sharing done after L7 (below, under variations). Line L3 is solved like any system of difference constraints: read each row as $r(V) \ge r(U) - \lfloor D_F(e)/N \rfloor$, start from $r = 0$, and raise values as in [Bellman-Ford](/bellman-ford/) for longest paths until no row is violated. This gives the least solution with $r \ge 0$, and if values still rise after $|V|$ passes, a cycle makes the system infeasible. The input node has no incoming edge, so it keeps $r = 0$.

**The folding equation.** Iteration $l$ of $U$ is ready at step $Nl + u + P_U$. Edge $e$ says that iteration $l + w(e)$ of $V$ uses it, and that iteration runs at step $N(l + w(e)) + v$. The value must wait between the two steps, so it needs
$$D_F(U \to V) = N(l + w(e)) + v - (Nl + u + P_U) = N w(e) - P_U + v - u$$
registers, the same for every $l$. A negative count means that $V$ would need the value before $U$ has made it.

**The retiming condition.** After a retiming $r$, edge $e$ has $w_r(e) = w(e) + r(V) - r(U)$ delays, as on the [retiming](/retiming/) page, so its count becomes
$$D_F'(e) = N w_r(e) - P_U + v - u = D_F(e) + N\,(r(V) - r(U)).$$
This is at least 0 exactly when $r(U) - r(V) \le D_F(e)/N$, and since the left side is an integer, exactly when $r(U) - r(V) \le \lfloor D_F(e)/N \rfloor$. These are the rows of L3. A retiming keeps the function of the graph, so the folded circuit of the retimed graph computes the same output stream, with the output of a node $V$ for sample $l$ now in iteration $l + r(V)$.

**When no retiming exists.** The system of L3 has a solution exactly when no cycle of the constraint graph is negative, that is, when every directed cycle $C$ of the data flow graph has $\sum_{e \in C} \lfloor D_F(e)/N \rfloor \ge 0$. Around a cycle the orders $v - u$ cancel, so
$$\sum_{e \in C} D_F(e) = N\,w(C) - \sum_{U \in C} P_U.$$
Since a floor is at most its argument, a folding set can work only if $N w(C) \ge \sum_{U \in C} P_U$ on every cycle: $N$ clock steps per iteration must be at least the [iteration bound](/iteration-bound/) of the graph with the times $P_U$. The floors make the exact test stronger than this bound, and a bad choice of orders can fail it even when the bound holds.

**Why the folded circuit is right.** By L8, unit $H_V$ runs $V$ at the steps $Nl + v$ and nothing else in those steps, since the orders on one unit are distinct. By the folding equation, the value of $U$ that iteration $l$ of $V$ needs leaves $H_U$ exactly $D_F'(e)$ steps before, so it is at the end of the register chain of L7 at that step. By induction on the steps, each unit computes the value of the retimed graph for the iteration it runs.

## Classic examples

**A second-order recursive filter on one adder and one multiplier.** Take $y(n) = x(n) + 3 y(n - 2) + 5 y(n - 3)$: an adder $A$ that sums $x(n)$ and two products, a multiplier $B$ by 3 with edges $A \to B$ (0 delays) and $B \to A$ (2 delays), and a multiplier $C$ by 5 with edges $A \to C$ (1 delay) and $C \to A$ (2 delays). Fold with $N = 2$ onto one adder and one multiplier, each with $P = 1$ stage, with orders $A: 0$, $B: 0$, $C: 1$. The input $X$ is read at order 0 with $P = 0$.

| edge | $w$ | $D_F$ by L1 | after $r(B) = 1$ |
| --- | --- | --- | --- |
| $X \to A$ | 0 | $0 - 0 + 0 - 0 = 0$ | 0 |
| $A \to B$ | 0 | $0 - 1 + 0 - 0 = -1$ | 1 |
| $B \to A$ | 2 | $4 - 1 + 0 - 0 = 3$ | 1 |
| $A \to C$ | 1 | $2 - 1 + 1 - 0 = 2$ | 2 |
| $C \to A$ | 2 | $4 - 1 + 0 - 1 = 2$ | 2 |

The edge $A \to B$ is negative: the multiplier would need $y(n)$ in the same step in which the adder starts it. The rows of L3 are $r(A) - r(B) \le -1$ from $A \to B$ and $r(B) - r(A) \le 1$ from $B \to A$, and the others allow 0, so the least solution is $r(B) = 1$ and 0 elsewhere. The retiming moves one delay from $B \to A$ to $A \to B$, so $B$ now multiplies $y(n - 1)$ and $A$ adds that product one sample later, which is the same filter. The cycle sums check the identity: on $A \to B \to A$, $-1 + 3 = 2 \cdot 2 - 2$, and on $A \to C \to A$, $2 + 2 = 2 \cdot 3 - 2$.

The folded circuit runs the adder on $A$ in even steps, and the multiplier on $B$ in even steps and on $C$ in odd steps. The multiplier input is a two-way switch: in even steps it takes the adder output through 1 register with the constant 3, and in odd steps through 2 registers with the constant 5. The adder takes $x$ directly, the multiplier output through 1 register (the product of $B$) and through 2 registers (the product of $C$). The design uses 2 units instead of 3, at twice the clock rate, and the run produces the same output samples as the original filter.

**A serial FIR filter.** An $N$-tap [FIR filter](/fir-filter/) folded with factor $N$ onto one multiplier and one adder is the classic multiply-accumulate loop: each sample takes $N$ steps, one per tap, and the folding equation gives the delay line that feeds the taps in turn.

**Folding after unfolding.** [Unfolding](/dsp-unfolding/) by $J$ followed by folding by $N$ gives hardware that takes $J$ samples every $N$ steps. This is how a design reaches the iteration bound per sample with a chosen number of units.

**High-level synthesis.** In the terms of high-level synthesis, the folding set is a modulo schedule with initiation interval $N$ together with a [resource binding](/resource-binding/), and the folding equation computes the register lifetimes that [register binding](/register-binding/) then packs. The switches and their steps form the controller of a [finite state machine with datapath](/finite-state-machine-with-datapath/), a counter modulo $N$; Parhi, Wang and Brown (1992) synthesize these control circuits for pipelined folded designs.

## Variations

- **Register minimization.** The registers of L7 are counted per edge. The edges that leave one unit can share one delay line with taps, so a unit needs only as many registers as its longest $D_F$; Parhi's book (Chapters 6.3 and 6.4) goes further with a lifetime analysis that finds the least number of registers for all edges at once, and a forward and backward allocation of the values to them.
- **Choosing the folding set.** The template takes the folding set as given. Choosing it is a scheduling and binding problem, NP-hard in general like [resource-constrained scheduling](/resource-constrained-scheduling/), and a bad choice can force more registers or make L3 fail.
- **Multirate folding.** Parhi's book (Chapter 6.5) folds graphs with up-samplers and down-samplers, where operations run at different rates.
- **Folding with a lower bound on the delays.** If a unit needs its operand one step early, for instance because of a register at its input, the rows become $D_F'(e) \ge 1$, which shifts each row of L3 by a constant and keeps the same method.

## Pitfalls

- **A sign slip in the equation.** The count is $N w(e) - P_U + v - u$: the pipeline depth of the source unit, not of the target, and the order of the target minus the order of the source. Using $P_V$ or $u - v$ gives counts that look plausible but put each operand in the wrong step.
- **Dropping the floor.** The row of L3 is $r(U) - r(V) \le \lfloor D_F/N \rfloor$, not $\le D_F/N$ rounded to the nearest integer and not $\lceil D_F/N \rceil$. With a ceiling, an edge with $D_F = -1$ and $N = 2$ gets the row $r(U) - r(V) \le 0$, which allows $r = 0$ and leaves the edge at $-1$.
- **Ignoring the cycle condition.** If some cycle has $N w(C) < \sum P_U$, no folding set and no retiming will work for that $N$; a larger $N$ or less pipelining is needed. If the condition holds but the floors fail, the folding orders are to blame, not $N$.
- **Two operations in one slot.** Two operations with the same unit and the same order would need the unit twice in one step. The folding set must be checked before L1.
- **Forgetting the output shift.** After the retiming, the value of a node with $r(V) > 0$ for sample $l$ appears in iteration $l + r(V)$. Reading the output without this shift gives a stream that is correct but late by $r(V)$ samples.

## Exercises

1. In the example, change the order of $C$ to 0 and the order of $B$ to 1. Compute the five counts $D_F$, the retiming, and the registers of the folded circuit.
2. Show that if every cycle has $N w(C) - \sum P_U \ge N$ times its number of edges, then L3 always has a solution, whatever the orders.
3. Fold the graph of the example with $N = 1$ onto three units with $P = 2$ each. Which cycle fails the condition, and how does this match the iteration bound of the graph with node times 2?
4. Prove that the least solution of L3 with $r \ge 0$ gives $r = 0$ to every node with no incoming edge.

## References
