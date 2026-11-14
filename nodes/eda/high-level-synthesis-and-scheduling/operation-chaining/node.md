---
tag: GYHK03
kind: technique
slug: operation-chaining
name: Operation chaining
aliases:
- chaining of operations
- multicycling
area: eda/high-level-synthesis-and-scheduling
level: core
summary: Places dependent operations in one control step when their delays fit the clock period, or spreads a slow operation over several steps, trading states for clock time.
prereqs: [asap-alap-scheduling, dag-longest-path]
see_also: [sdc-scheduling, ilp-scheduling-formulation, path-based-scheduling, static-timing-analysis, setup-and-hold-constraints, retiming, ripple-carry-adder, resource-constrained-scheduling]
sources:
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 5, Schedule Optimization (chaining and multicycle operations in scheduling)
  - paper: doi:10.1109/43.75629
    title: Cheng-Tsung Hwang, Jiahn-Humg Lee and Yu-Chin Hsu, A formal approach to the scheduling problem in high level synthesis, IEEE Transactions on Computer-Aided Design 10(4), 464 to 475, 1991
    locator: the extensions of the 0-1 model to chaining and to multicycle and pipelined units
  - paper: doi:10.1145/1146909.1147025
    title: Jason Cong and Zhiru Zhang, An efficient and versatile scheduling algorithm based on SDC formulation, Proceedings of the 43rd Design Automation Conference, 433 to 438, 2006
    locator: the chaining constraints from the longest combinational delay between two operations and the clock period
---

Operation chaining lets a scheduler in [high-level synthesis](/high-level-synthesis/) put an operation in the same control step as an operation whose result it uses, when the combinational delays of the two, plus the register overhead, fit in one clock period. The result goes from one unit straight into the next through wires and multiplexers, with no register between them. A chain uses fewer control steps, and so fewer controller states and fewer registers, at the price of a longer path in each step. The opposite case is an operation that is slower than one clock period: it is spread over several consecutive steps, a multicycle operation, and its unit and inputs stay busy for all of them. Both cases match the schedule to the clock period: chaining packs fast operations into one period, and the multicycle case lets a slow one take several. The time to run a block is the number of steps times the period, so the two choices together decide it.

## In plain words

Picture a clock that ticks at fixed times, and a box of results that is filled at each tick. If an add takes a third of a tick, it is a waste to wait for the next tick before the next add uses its result. Chaining lets two or three quick steps run back to back inside one tick, as long as they all finish before it ends. A slow step, such as a big multiply that needs two ticks, does the reverse: it starts at one tick and its result is ready only two ticks later, and nothing may disturb its inputs in between. The design tool picks, for each step, the right way to fill the ticks.

## When it applies

Chaining applies when the clock period is set by something other than the fastest operations: by the slowest unit, by the memory, or by a target frequency for the whole chip. Then fast operations, such as adds, compares, logic and shifts, leave slack in each period, and chaining uses it. It needs a delay model per operation type and bit width, and a known clock period $T$ before scheduling.

The multicycle case applies when some operation takes longer than $T$, such as a wide multiply or divide, and pipelining that unit is too costly. With a pipelined unit, the operation still has a latency of several steps, but the unit accepts a new operation each step, which is a different trade.

## The template

Let each operation $v$ have a combinational delay $d(v)$, and let $\delta$ be the register overhead per step: the clock to output delay plus the setup time. A step may hold a set of chained operations exactly when every combinational path inside it fits:
$$\mathrm{arr}(v) = d(v) + \max\{\mathrm{arr}(u) : u \to v,\ u \text{ in the same step as } v\}, \qquad \mathrm{arr}(v) + \delta \le T,$$
with the maximum over an empty set equal to 0. This is a [longest path](/dag-longest-path/) computation over the data flow graph of one step, the same arrival time that [static timing analysis](/static-timing-analysis/) computes later on the netlist.

1. **Estimate the delays.** Give each operation a delay from a library that knows the type and bit width, and add the delay of the multiplexers in front of shared units.
2. **Find the multicycle operations.** An operation with $d(v) + \delta > T$ gets $k(v) = \lceil (d(v) + \delta)/T \rceil$ steps. Its successors start at least $k(v)$ steps later. Its unit is busy for all $k(v)$ steps unless it is pipelined, and its input registers must hold their values for all of them.
3. **Write the chaining rule as a rule on steps.** For each pair $u, v$ joined by a combinational path with the largest delay $D(u, v)$, the pair cannot share a step when $D(u, v) + \delta > T$. In [SDC scheduling](/sdc-scheduling/) this becomes the difference constraint $s_v - s_u \ge 1$ for such pairs, and Cong and Zhang (2006) give the general form for paths that span several periods.
4. **Schedule.** Any scheduler can enforce the rule: a list scheduler tracks the arrival time of each value inside the current step and admits an operation only if it still fits; an [ILP model](/ilp-scheduling-formulation/) adds rows that forbid the bad pairs from sharing a step.
5. **Tell the timing tools.** A multicycle operation is a multicycle path for static timing analysis: its setup check is relaxed to $k(v)$ periods. Without that, the tools report it as a violation, or worse, the design is signed off with a wrong check.

## Classic examples

**Multiply, add, add.** Take the chain $m = x \cdot y$ with delay 6 ns, $a_1 = m + u$ and $a_2 = a_1 + w$ with delay 3 ns each, and $\delta = 1$ ns. The total time to run the chain depends on the period:

| $T$ (ns) | Steps | Time (ns) | Grouping |
| --- | --- | --- | --- |
| 13 | 1 | 13 | $\{m, a_1, a_2\}$ chained |
| 10 | 2 | 20 | $\{m, a_1\}$ chained, then $\{a_2\}$ |
| 10, no chaining | 3 | 30 | one operation per step |
| 7 | 2 | 14 | $\{m\}$, then $\{a_1, a_2\}$ chained |
| 4 | 4 | 16 | $m$ over 2 steps, then $a_1$, then $a_2$ |

At $T = 10$, chaining saves a third of the time. At $T = 4$, the multiply needs $\lceil 7/4 \rceil = 2$ steps, and the overhead $\delta$ is paid in every step. The best time here comes from $T = 13$ with one long chain, and from $T = 7$ with chaining in the second step.

- **Add chains in DSP code.** A sum of several products often fits as one multiply and two or three chained adds per step at a clock set by the multiplier.
- **Compare and select.** A compare chained into a multiplexer, as in `max(a, b)`, fits in one step at almost any period, since both parts are fast.

## Variations

- **Bit-level chaining.** Two chained ripple carry adders do not need the sum of their delays: the low bits of the second adder can start as soon as the low bits of the first are ready. A delay model at the bit level gives tighter chains than one that adds whole operation delays. See [ripple carry adder](/ripple-carry-adder/).
- **Chaining across branches.** An operation after a join can chain with operations on either arm, as long as the longest arm fits. [Path-based scheduling](/path-based-scheduling/) handles this by looking at each path.
- **Multicycle versus pipelined.** A pipelined multiplier of latency 2 accepts a new multiply each step, so it costs registers inside the unit but frees the unit at once. A multicycle one keeps the unit busy and needs stable inputs, but has no inner registers.
- **Retiming after scheduling.** [Retiming](/retiming/) can move registers across chained logic after scheduling to balance the steps, when the netlist allows it.
- **Fixed clock versus chosen clock.** When the period is free, the scheduler can sweep $T$ and keep the one that gives the least steps times period, as in the example.

## Pitfalls

- **Wire and multiplexer delay.** The delay of a chain includes the multiplexers in front of shared units and the routing, which grow after binding. A chain that fits in the scheduler can miss timing after binding. Keep a margin, or schedule again with the bound netlist.
- **Register overhead.** Each step costs $\delta$. Many short steps with no chaining spend a large fraction of the time on overhead, as the $T = 4$ row shows.
- **Inputs of a multicycle operation.** The registers that feed a multicycle operation must not change during its steps. A register binder that does not know this may reuse them, which breaks the result.
- **Missing multicycle path constraints.** Synthesis and timing tools assume one period per path unless told otherwise. Each multicycle operation needs a matching constraint, see [setup and hold constraints](/setup-and-hold-constraints/).
- **Delays that depend on width.** The delay of an add depends on its width. A delay table for 32 bits makes chains of narrow operations too short. Pair chaining with [bitwidth analysis](/bitwidth-analysis/).
- **Glitches and power.** Long chains switch many times within a period before they settle, which costs dynamic power.

## Exercises

1. With $d = 6$ for a multiply, $d = 3$ for an add and $\delta = 1$, find the period that gives the least total time for the chain multiply, add, add, add.
2. Show that for a fixed assignment of operations to steps, the rule $\mathrm{arr}(v) + \delta \le T$ for every $v$ holds exactly when every combinational path inside every step has a delay of at most $T - \delta$.
3. A multicycle divide takes 3 steps on a unit that is not pipelined. How many such divides can start in 9 steps on one unit, and how many on a pipelined unit of latency 3?
4. Give a data flow graph where chaining reduces the number of steps but increases the number of units of one type needed for the least latency.

## References
