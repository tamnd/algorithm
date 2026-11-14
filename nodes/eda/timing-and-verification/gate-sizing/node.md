---
tag: D5Q8V0
kind: problem
slug: gate-sizing
name: Gate sizing
aliases:
- transistor sizing
area: eda/timing-and-verification
level: core
summary: Choose a size for each gate from a library so that the circuit meets its delay target with least area or power.
prereqs: [static-timing-analysis, elmore-delay]
see_also: [tilos, lagrangian-relaxation-gate-sizing, geometric-programming, logical-effort, van-ginneken-buffer-insertion, strong-np-hardness, convex-optimization-problem, timing-driven-placement]
sources:
  - paper: "Wing Ning Li, Strongly NP-hard discrete gate-sizing problems, IEEE Transactions on Computer-Aided Design 13(8), 1045 to 1051, 1994"
    locator: the strong NP-hardness of gate sizing with discrete sizes
  - paper: "Chung-Ping Chen, Chris C. N. Chu and D. F. Wong, Fast and exact simultaneous gate and wire sizing by Lagrangian relaxation, IEEE Transactions on Computer-Aided Design 18(7), 1014 to 1025, 1999"
    locator: the continuous problem under the Elmore delay and its exact solution
  - paper: doi:10.1287/opre.1050.0254
    title: Stephen Boyd, Seung-Jean Kim, Dinesh D. Patil and Mark A. Horowitz, Digital circuit optimization via geometric programming, Operations Research 53(6), 2005
    locator: gate sizing with posynomial delay models as a geometric program
  - book: isbn:9789048195909
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, Springer, 2011
    locator: Chapter 8, Timing Closure, Section 8.5.1, Gate Sizing
---

Gate sizing is the problem of choosing the size of every gate of a circuit, from a library of sizes or from an interval, so that every path meets the delay target and the total area or power is least. A larger gate drives its load faster but costs area and power, and it loads the gates that drive it, so a size change helps one delay and hurts another. With the Elmore delay and continuous sizes, every delay is a posynomial in the sizes and the problem is a [geometric program](/geometric-programming/), which convex optimization solves exactly. With discrete sizes the problem is strongly NP-hard (Li, 1994). It is one of the main steps of timing closure, next to buffer insertion and placement.

## In plain words

Every logic gate on a chip comes in several sizes. A big gate is fast when it drives a heavy load, but it takes more room and more power, and it is itself a heavy load for the gate in front of it.

The circuit has a clock period to meet. Every path from an input to an output must be fast enough. The task is to pick a size for each gate so that all paths are fast enough and the chip spends as little room or power as possible on it.

If any size in a range is allowed, the problem has a single best answer that good methods find. If only the sizes of a library are allowed, it becomes a hard puzzle.

## Definition

**Input.** A DAG of gates $0, \dots, n - 1$, the timing graph of [static timing analysis](/static-timing-analysis/). For each gate $i$: an intrinsic delay $p_i \ge 0$, a drive resistance $r_i / x_i$ and an input capacitance $c_i x_i$ at size $x_i$, an area $a_i x_i$, a fixed load $f_i \ge 0$ of wires and outputs, and a set $\mathcal S_i$ of allowed sizes. A delay target $T$.

**Delay.** The delay of gate $i$ is the [Elmore delay](/elmore-delay/) of its switch-level RC model,
$$ D_i(x) = p_i + \frac{r_i}{x_i} \Big( f_i + \sum_{j \in \mathrm{out}(i)} c_j x_j \Big). $$
The arrival time of a gate is the latest arrival time of its fanins plus $D_i$, starting from 0 before the gates without fanins, and the circuit delay $\Delta(x)$ is the latest arrival time.

**Output.** Sizes $x_i \in \mathcal S_i$ with $\Delta(x) \le T$ that minimize $\sum_i a_i x_i$, or the answer that no sizes meet $T$.

In the *continuous* problem $\mathcal S_i$ is an interval $[\ell_i, h_i]$; in the *discrete* problem it is a finite set. Each $D_i$ is a sum of monomials in $x$ with positive coefficients, a posynomial, so the continuous problem with one constraint $\sum_{h \in Q} D_h \le T$ per path $Q$, or with arrival time variables, is a geometric program. After $x_i = e^{y_i}$ it is a [convex optimization problem](/convex-optimization-problem/).

## Variants

- **Discrete or continuous sizes.** Standard cell libraries offer a few sizes of each cell, so the discrete form is the real one. The continuous form is solved first and rounded.
- **Power instead of area.** Dynamic power grows with the switched capacitance $\sum_i c_i x_i$ weighted by activity, so it has the same form with other weights. Leakage power leads to the related choice of threshold voltage for each cell.
- **Delay under an area budget.** Swap the roles: minimize $\Delta(x)$ subject to $\sum_i a_i x_i \le A$. For a single path with no area cost, the fastest sizing has the closed form of [logical effort](/logical-effort/).
- **Gate and wire sizing.** The widths of the wire segments of each RC interconnect tree are variables too, with the same posynomial form.
- **Sizing with buffers.** On long nets, inserting buffers changes the structure of the circuit; see [van Ginneken buffer insertion](/van-ginneken-buffer-insertion/). Both are often solved together.
- **Finer granularity.** Each device inside a gate can get its own size. The model is the same at the level of single devices.
- **Other delay models.** With table models of cell libraries, the delays are no longer posynomials and the continuous problem is no longer convex.

## Examples

**A chain of two gates.** A fixed driver of size 1 drives gate 1, which drives gate 2, which drives a load $f_2 = 8$. All $p_i = r_i = c_i = a_i = 1$ and the sizes are $\{1, 2, 4\}$. The delay is $(1 + x_1) + (1 + x_2 / x_1) + (1 + 8 / x_2)$ and the area, with the driver, is $1 + x_1 + x_2$.

| $x_1$ \\ $x_2$ | 1 | 2 | 4 |
| --- | --- | --- | --- |
| 1 | delay 13, area 3 | delay 10, area 4 | delay 10, area 6 |
| 2 | delay 13.5, area 4 | delay 10, area 5 | delay 9, area 7 |
| 4 | delay 15.25, area 6 | delay 11.5, area 7 | delay 10, area 9 |

The delay is not monotone in the sizes: $(4, 1)$ is slower than $(1, 1)$, because the large gate 1 sees the same weak driver and drives a small gate. For $T = 10$ the least area is 4, at $(1, 2)$. For $T = 9$ only $(2, 4)$ is feasible, with area 7. By the inequality of arithmetic and geometric means, $x_1 + x_2 / x_1 + 8 / x_2 \ge 3 \cdot 8^{1/3} = 6$, so no sizes, even continuous ones, give a delay below 9; the bound is met only at the equal stage ratios $x_1 = 2$, $x_2 = 4$.

**Rounding loses.** For $T = 9.5$ the continuous optimum is $x_1 \approx 1.241$, $x_2 \approx 2.414$, with area about $4.655$. Among the library sizes only $(2, 4)$ meets $9.5$, with area 7. Rounding the continuous answer to the nearest sizes $(1, 2)$ misses the target.

## Known algorithms

- **[TILOS](/tilos/)** (Fishburn and Dunlop, 1985). Greedy: from the smallest sizes, repeatedly make the gate on the critical path with the best delay gain per area one step larger. Sound and fast, but not optimal, and it can fail when a sizing exists.
- **[Lagrangian relaxation gate sizing](/lagrangian-relaxation-gate-sizing/)** (Chen, Chu and Wong, 1998). Multipliers on the timing edges that conserve flow, and a closed-form local resizing for fixed multipliers. Exact for the continuous problem under the Elmore delay, since there is no duality gap.
- **Geometric programming solvers.** Interior point methods solve the continuous problem to any accuracy in polynomial time; Boyd, Kim, Patil and Horowitz describe this for digital circuits.
- **Rounding and local search for discrete sizes.** The continuous answer is rounded and repaired by local moves, or the relaxation is used with library cells directly. These give no guarantee.

## Bounds

- **Discrete sizes.** Li (1994) proved that gate sizing with discrete sizes is [strongly NP-hard](/strong-np-hardness/), so it has no pseudo-polynomial algorithm unless P = NP. The known exact methods take exponential time in the worst case.
- **Continuous sizes.** The problem is convex after the change of variables $x_i = e^{y_i}$, so a local minimum is global and the optimum is unique when the area weights are positive. It is solvable to accuracy $\varepsilon$ in time polynomial in the size of the input and $\log(1/\varepsilon)$ by interior point methods.
- **Feasibility.** The least possible delay is itself the optimum of a geometric program. For a chain without area cost and without bounds on the sizes, it is reached when all stage delays above the intrinsic ones are equal, as in the example.

## Reductions

- **To geometric programming.** The continuous problem, with arrival time variables, is a geometric program; with $x_i = e^{y_i}$ it is a convex program in $(y, A)$.
- **To a dual over flows.** By the KKT conditions, the Lagrangian dual of the continuous problem ranges over multipliers that obey [flow conservation](/flow-conservation/) on the timing graph, and the arrival times drop out. This is the basis of Lagrangian relaxation gate sizing.
- **From hard discrete problems.** The NP-hardness of the discrete form is shown by reductions from known NP-hard problems in Li (1994).

## Applications

- **Timing closure.** After placement and routing, gates on failing paths are made larger and gates with spare time smaller, often many times in a flow.
- **Power reduction.** Gates off the critical paths are made smaller to save dynamic power, with the delay target as the constraint.
- **Area recovery.** After synthesis and buffering, sizing removes area that the timing does not need.
- **Simultaneous optimization.** Together with buffer insertion and [timing-driven placement](/timing-driven-placement/), it decides most of the delay of a design that a placer and router have fixed.

## References
