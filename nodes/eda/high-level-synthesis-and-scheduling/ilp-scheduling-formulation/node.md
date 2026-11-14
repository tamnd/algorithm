---
tag: FXNRG0
kind: technique
slug: ilp-scheduling-formulation
name: ILP formulation of operation scheduling
aliases:
- ALPS scheduling
- integer programming scheduling for HLS
area: eda/high-level-synthesis-and-scheduling
level: core
summary: Writes high-level synthesis scheduling as a 0-1 integer program with one variable per operation and step, plus precedence and resource rows, solved exactly.
prereqs: [binary-integer-programming, resource-constrained-scheduling, latency-constrained-scheduling, asap-alap-scheduling]
see_also: [lp-relaxation, mixed-integer-programming, sdc-scheduling, force-directed-scheduling, list-scheduling, depth-first-branch-and-bound, total-unimodularity, sdc-modulo-scheduling]
sources:
  - paper: doi:10.1109/43.75629
    title: Cheng-Tsung Hwang, Jiahn-Humg Lee and Yu-Chin Hsu, A formal approach to the scheduling problem in high level synthesis, IEEE Transactions on Computer-Aided Design 10(4), 464 to 475, 1991
    locator: the 0-1 model with variables only inside the ASAP to ALAP window, time-constrained, resource-constrained and feasible scheduling, and the extensions to chaining, multicycle and pipelined units, functional pipelining and loop folding
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 5, Scheduling Algorithms (the integer linear programming model in the section on scheduling with resource constraints)
---

The ILP formulation writes the scheduling problems of [high-level synthesis](/high-level-synthesis/) as a [0-1 integer program](/binary-integer-programming/). There is one binary variable $x_{v,t}$ for each operation $v$ and each step $t$ in which $v$ may start, equal to 1 when $v$ starts in step $t$. Linear rows say that each operation starts once, that it starts after its predecessors end, and that no step uses more units of a type than allowed. The same rows serve [resource-constrained scheduling](/resource-constrained-scheduling/), with the latency as the objective, and [latency-constrained scheduling](/latency-constrained-scheduling/), with the unit counts as variables and the cost as the objective. A general solver then gives a proved optimum. Hwang, Lee and Hsu (1991) made the model practical in their ALPS scheduler by creating variables only inside the window from the ASAP to the ALAP start of each operation.

## In plain words

Make a grid with one row per operation and one column per clock step. Each operation must put exactly one mark in its row, in the step where it starts. Rules on the grid say that a mark must come after the marks of the operations it needs, and that one column cannot hold more multiplies than there are multipliers. A solver for this kind of yes or no grid puzzle then finds the best placement of the marks. It is slow on big graphs, but its answer is the true best.

## When it applies

Use it when an exact schedule is worth the solver time: graphs with tens to a few hundred operations, a moderate number of steps, and a good solver at hand. It also gives the reference optimum for judging heuristics such as [list scheduling](/list-scheduling/) and [force-directed scheduling](/force-directed-scheduling/). It needs an upper bound $L$ on the latency to fix the columns. A list schedule gives one.

It fits any constraint that is linear in the start indicators: precedences with delays, unit limits per step, timing windows, mutually exclusive operations, and unit limits modulo an initiation interval. It does not fit costs that are not linear in the indicators, such as the exact multiplexer area of a binding, without more variables.

## The template

Let $G = (V, E)$ be the sequencing graph, $d(v) \ge 1$ the delays, $t(v)$ the types, and $L$ a latency bound. Let $[a(v), b(v)]$ be the ASAP and ALAP starts for $L$, from [ASAP and ALAP scheduling](/asap-alap-scheduling/). Every schedule has $a(v) \le s(v) \le b(v)$, so only these steps get a variable.

1. **Variables.** $x_{v,t} \in \{0, 1\}$ for $v \in V$ and $a(v) \le t \le b(v)$.
2. **One start.** $\sum_{t} x_{v,t} = 1$ for each $v$. The start step is then $s(v) = \sum_t t\, x_{v,t}$.
3. **Precedence.** For each edge $(u, v)$, $\sum_t t\, x_{v,t} - \sum_t t\, x_{u,t} \ge d(u)$.
4. **Resources.** For each type $k$ and step $j$,
$$\sum_{v : t(v) = k} \ \sum_{\tau = j - d(v) + 1}^{j} x_{v,\tau} \le a_k,$$
which counts the operations of type $k$ that are busy in step $j$.
5. **Objective.** For resource-constrained scheduling, add a sink $z$ after every operation and minimize $s(z)$. For latency-constrained scheduling, make each $a_k$ an integer variable and minimize $\sum_k c_k a_k$.
6. **Solve.** Give the model to a 0-1 or [mixed integer](/mixed-integer-programming/) solver, which runs [branch and bound](/depth-first-branch-and-bound/) on the [LP relaxation](/lp-relaxation/).
7. **Read the schedule.** $s(v)$ is the $t$ with $x_{v,t} = 1$.

**Why it is exact.** Integer solutions and schedules match one to one. Given a schedule $s$ within $L$, set $x_{v, s(v)} = 1$ and all other variables to 0. Then row 2 holds, row 3 is $s(v) - s(u) \ge d(u)$, and row 4 counts, for each $k$ and $j$, the operations of type $k$ with $j - d(v) + 1 \le s(v) \le j$, which are exactly those busy in step $j$. Conversely, a 0-1 solution has exactly one 1 per operation by row 2, so it defines $s$, and the same reading of rows 3 and 4 shows that $s$ is a schedule. Both maps keep the objective, so an optimal integer solution is an optimal schedule.

**A stronger precedence row.** Row 3 is one row per edge. For unit delays it can be replaced, for each edge $(u, v)$ and step $j$, by
$$\sum_{\tau \ge j} x_{u,\tau} + \sum_{\tau \le j} x_{v,\tau} \le 1,$$
which says that $u$ starts at $j$ or later and $v$ starts at $j$ or earlier cannot both hold. For delay $d(u)$, replace $\tau \le j$ in the second sum by $\tau \le j + d(u) - 1$. Integer solutions are the same. Every fractional solution of these rows also meets row 3, so the LP relaxation is at least as tight. The price is one row per edge and step.

**Size.** There are $\sum_v (b(v) - a(v) + 1) \le |V|(L + 1)$ variables, $|V| + |E|$ rows of kinds 2 and 3, and $|K| \cdot L$ rows of kind 4. Tight windows from a good bound $L$ make the model much smaller.

## Classic examples

- **The small gap.** Take two independent operations of one type with one unit, delay 1, a sink $z$, and $L = 2$. The best integer schedule runs them in steps 0 and 1, so $s(z) = 2$. The LP relaxation can set $x_{v,0} = x_{v,1} = \tfrac12$ for both, which meets the resource rows with equality and gives $s(v) = \tfrac12$. Then row 3 allows $s(z) = \tfrac32$. So the LP bound is $\tfrac32$ against the optimum 2, and the solver must branch.
- **The differential equation example.** With $L = 4$ and unit delays, the windows of the [high-level synthesis](/high-level-synthesis/) example give 21 variables for 11 operations, against 44 for the full grid. The operations $v_1$ to $v_5$ lie on paths of 4 steps and have one step each, $v_6$ and $v_7$ have 2, and $v_8$ to $v_{11}$ have 3. The optimum for latency-constrained scheduling with unit costs needs 2 multipliers and 2 ALUs, as on the [latency-constrained scheduling](/latency-constrained-scheduling/) page.
- **ALPS.** Hwang, Lee and Hsu solved time-constrained, resource-constrained and feasible scheduling, the last a test whether given unit counts and a latency bound admit any schedule. They also modeled chaining, multicycle and pipelined units, functional pipelining, loop folding, mutually exclusive operations and bus limits, and the lifetimes of variables, all in the same 0-1 form.

## Variations

- **Pipelined units.** In row 4, count only the start step: replace the inner sum by $x_{v,j}$.
- **Modulo resources.** For a loop with initiation interval $II$, the resource row for residue $r$ sums $x_{v,\tau}$ over all $\tau \equiv r \pmod{II}$ and over the busy steps. This is an exact model of modulo scheduling. See [SDC modulo scheduling](/sdc-modulo-scheduling/) for a faster heuristic.
- **Module selection.** Use $x_{v,t,k}$ for each type $k$ that can run $v$, with $\sum_{t,k} x_{v,t,k} = 1$ and the delay of $k$ in the precedence rows.
- **Mutually exclusive operations.** Two operations on different arms of a branch can share a unit in one step. Count them as one in row 4, for example with one row per set of operations that can run together.
- **Timing windows.** A rule $s(v) - s(u) \le c$ is the linear row $\sum_t t\, x_{v,t} - \sum_t t\, x_{u,t} \le c$.
- **Register and lifetime costs.** Lifetimes are linear in the starts, so a cost on the sum of lifetimes adds no new variable. The exact register count needs one more variable per step.
- **Difference constraints only.** If the resource rows are dropped and the starts are used as integer variables directly, every row has the form $s(v) - s(u) \ge c$. That matrix is [totally unimodular](/total-unimodularity/), so an LP solves it. This is the idea of [SDC scheduling](/sdc-scheduling/), which then handles resources by a heuristic order.

## Pitfalls

- **No bound, no model.** The columns need a latency bound. A bound that is too small makes the model infeasible, and one that is too large makes it big. Use a list schedule for an upper bound and the critical path for a lower bound.
- **Weak rows.** The one-row-per-edge precedence gives a weak LP bound, and the solver spends time branching. The stronger rows help on hard instances.
- **Multicycle operations.** Row 4 must count every busy step of an operation, not only its start, unless the unit is pipelined. A model that counts only starts for a non-pipelined unit allows two operations on one unit at the same time.
- **Fractional reading.** Read the schedule only from an integer solution. Rounding an LP solution does not keep the precedences in general.
- **Symmetry.** Units of one type are identical, and many schedules have the same cost. Solvers waste time on symmetric branches unless the model or the solver breaks the symmetry.
- **Scale.** The number of variables grows with $|V| \cdot L$. Models with thousands of operations and long latencies are out of reach of exact solving in reasonable time, which is why heuristic schedulers dominate in tools.

## Exercises

1. Show that the stronger precedence row for unit delays implies $s(v) - s(u) \ge 1$ for every fractional solution that meets the one-start rows.
2. Write the model for the chain $v_1 \to v_2 \to v_3$ of unit multiplies, one multiplier and $L = 3$. How many variables remain after the windows are applied?
3. Give a family of graphs where the LP bound of the template with row 3 stays near half of the optimal latency.
4. Write the resource rows for a pipelined multiplier of delay 2 under modulo scheduling with $II = 3$.

## References
