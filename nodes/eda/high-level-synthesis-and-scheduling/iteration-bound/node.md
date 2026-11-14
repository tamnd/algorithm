---
tag: RPHN78
kind: theorem
slug: iteration-bound
name: Iteration bound
aliases:
- Renfors-Neuvo iteration bound
- maximum loop bound
area: eda/high-level-synthesis-and-scheduling
level: core
summary: The sample period of a recursive data flow graph can be no less than the largest ratio of loop delay to loop register count, a bound met by retiming and unfolding.
prereqs: [minimum-ratio-problem, difference-constraints]
see_also: [dsp-unfolding, dsp-folding, retiming, karp-minimum-mean-cycle, dinkelbach-algorithm, negative-cycle-detection, synchronous-dataflow, sdc-modulo-scheduling]
sources:
  - paper: "Markku Renfors and Yrjö Neuvo, The maximum sampling rate of digital filters under hardware speed constraints, IEEE Transactions on Circuits and Systems CAS-28(3), 196 to 202, 1981"
    title: Markku Renfors and Yrjö Neuvo, The maximum sampling rate of digital filters under hardware speed constraints, IEEE Transactions on Circuits and Systems CAS-28(3), 196 to 202, 1981
    locator: the bound on the sample period of a recursive filter from its loops, and its attainment
  - book: isbn:9780471241867
    title: Keshab K. Parhi, VLSI Digital Signal Processing Systems, Design and Implementation, Wiley, 1999
    locator: Chapter 2 (2.3 loop bound and iteration bound, 2.4 algorithms for computing the iteration bound, 2.5 multirate graphs)
  - paper: doi:10.1109/12.73588
    title: Keshab K. Parhi and David G. Messerschmitt, Static rate-optimal scheduling of iterative data-flow programs via optimum unfolding, IEEE Transactions on Computers 40(2), 1991
    locator: rate-optimal schedules that reach the iteration bound after unfolding
---

The iteration bound is a lower bound on how fast a recursive computation, such as a digital filter with feedback, can run, however much hardware it gets. The computation is a data flow graph whose nodes take time and whose loops carry delays, the registers that hold past values. Every loop must finish its whole chain of operations within the iterations that its delays allow, so its total time divided by its number of delays is a least time per iteration. The iteration bound $T_\infty$ is the largest of these ratios over all loops. Renfors and Neuvo stated it for digital filters in 1981. This page proves that no schedule beats it and that a periodic schedule on unlimited processors reaches it exactly.

## Statement

A data flow graph (DFG) is a directed graph $G = (V, E)$ with a computation time $t(v) \ge 0$ on each node and a number of delays $w(e) \in \mathbb{Z}_{\ge 0}$ on each edge, such that every directed cycle has at least one delay. Node $v$ runs once in each iteration $k = 0, 1, 2, \ldots$. An edge $e = (u, v)$ with $w(e)$ delays means that iteration $k$ of $v$ uses the result of iteration $k - w(e)$ of $u$; for $k < w(e)$ it uses an initial value instead. For a directed cycle $C$, write $t(C)$ for the sum of the times of its nodes and $w(C)$ for the sum of the delays of its edges. The iteration bound is
$$T_\infty = \max_{C} \frac{t(C)}{w(C)},$$
the maximum over the directed simple cycles, and $T_\infty = 0$ if $G$ has no cycle.

A schedule on unlimited processors gives each run a real start time $s(v, k) \ge 0$ such that for every edge $e = (u, v)$ and every $k \ge w(e)$,
$$s(v, k) \ge s(u, k - w(e)) + t(u).$$
Any number of runs may overlap. The iteration period of the schedule is
$$T(s) = \liminf_{k \to \infty} \max_{v \in V} \frac{s(v, k)}{k}.$$

**Theorem.** Every schedule satisfies $T(s) \ge T_\infty$. There is a schedule of the form $s(v, k) = k T_\infty + \sigma_v$ with constants $\sigma_v \ge 0$, so the bound is attained.

The cycle that reaches the maximum is called a critical loop. Computing $T_\infty$ is a maximum cycle ratio problem: it is the [minimum ratio problem](/minimum-ratio-problem/) with the signs of the times reversed.

## In plain words

Think of a loop in a filter as a relay race that must hand the baton back to its own start. Each delay on the loop gives the race one more sample period to finish. If the steps around a loop take 3 nanoseconds in total and the loop holds 2 delays, the loop can produce a new value no faster than once every 1.5 nanoseconds on average, however many adders and multipliers are bought, because each step must wait for the one before it. The slowest loop, measured this way, sets the speed limit for the whole filter. Parts of the graph with no loop never limit the speed, since they can be pipelined as deeply as one likes.

## Proof

*The bound.* Let $C$ be a directed simple cycle through the nodes $v_0, v_1, \ldots, v_{m-1}$ in order, with edges $e_i = (v_i, v_{i+1})$ and $v_m = v_0$, and let $W = w(C) \ge 1$. Start at iteration $k \ge W$ of $v_0$ and follow the edges of $C$ backward. The edge $e_{m-1}$ gives $s(v_0, k) \ge s(v_{m-1}, k - w(e_{m-1})) + t(v_{m-1})$, and the edge before it bounds that start in turn. After going once around, the iteration index has dropped by exactly $W$, and every index on the way lies between $k - W \ge 0$ and $k$, so every inequality applies. Adding them gives
$$s(v_0, k) \ge s(v_0, k - W) + t(C).$$
Applying this $j$ times, for $k = jW + r$ with $0 \le r < W$, gives $s(v_0, k) \ge j \, t(C) + s(v_0, r) \ge \lfloor k / W \rfloor \, t(C)$. Dividing by $k$ and letting $k \to \infty$,
$$\liminf_{k \to \infty} \frac{s(v_0, k)}{k} \ge \frac{t(C)}{W}.$$
So $T(s) \ge t(C) / w(C)$ for every cycle $C$, and hence $T(s) \ge T_\infty$.

*The maximum is over simple cycles.* A closed walk splits into simple cycles $C_1, \ldots, C_r$, and its ratio is $\sum t(C_i) / \sum w(C_i)$, a mediant of the ratios $t(C_i) / w(C_i)$, which is at most the largest of them. So closed walks give nothing larger, and the maximum exists since there are finitely many simple cycles.

*Attainment.* Let $T = T_\infty$ and ask for constants $\sigma$ with
$$\sigma_v - \sigma_u \ge t(u) - T \, w(e) \quad \text{for every edge } e = (u, v).$$
These are [difference constraints](/difference-constraints/). Read them as a graph with an arc $u \to v$ of weight $t(u) - T w(e)$. A cycle $C$ of this graph has weight $t(C) - T w(C) \le 0$ by the choice of $T$, so there is no positive cycle. Add a source with arcs of weight 0 to every node; the longest path distances from it exist, are at least 0, and satisfy every constraint. Set $s(v, k) = k T + \sigma_v$. Then for each edge, $s(v, k) - s(u, k - w(e)) = T w(e) + \sigma_v - \sigma_u \ge t(u)$, so $s$ is a schedule, and $T(s) = T$. $\blacksquare$

The same argument with $T < T_\infty$ finds a positive cycle, which is how a parametric search decides whether a given period is feasible: [negative cycle detection](/negative-cycle-detection/) on the weights $T w(e) - t(u)$, inside a binary search on $T$ or inside the [Dinkelbach method](/dinkelbach-algorithm/). With one delay on every edge the ratio is a cycle mean, and [Karp's algorithm](/karp-minimum-mean-cycle/) applies; Parhi's book (Chapter 2.4) reduces the general case to a cycle mean on a graph whose nodes are the delays.

## Consequences

- **Retiming cannot beat it.** A [retiming](/retiming/) keeps the number of delays on every cycle. A cycle $C$ with $w(C)$ delays is cut by them into at most $w(C)$ paths with no delay, whose times add to $t(C)$, so one of them takes at least $t(C) / w(C)$. Hence every retimed circuit has a clock period of at least $T_\infty$, and of at least $\lceil T_\infty \rceil$ when all times are integers.
- **Unfolding reaches it.** Unfolding by $J$ multiplies the iteration bound by $J$ while one iteration now handles $J$ samples, so the bound per sample stays $T_\infty$. When $J T_\infty$ is an integer, the unfolded graph can have a clock period that matches its bound; the [unfolding](/dsp-unfolding/) page proves the factor $J$ and works an example.
- **Folding needs it.** In the [folding transformation](/dsp-folding/) the registers around a cycle add up to $N w(C) - \sum P_U$, so a folding with factor $N$ exists only if every cycle has $N w(C) \ge \sum P_U$, the iteration bound of the folded hardware in clock cycles.
- **Modulo scheduling.** The recurrence bound RecMII of [SDC modulo scheduling](/sdc-modulo-scheduling/) is the same ratio, rounded up to an integer initiation interval.
- **Dataflow throughput.** The throughput of a [synchronous dataflow](/synchronous-dataflow/) graph on unlimited processors is the inverse of the iteration bound of its homogeneous expansion, and the throughput of a [latency-insensitive design](/latency-insensitive-design/) is a cycle ratio of the same kind.

## Tightness

The attainment part shows that the bound cannot be raised for real-valued start times on unlimited processors. With a clock, it is tight only up to the unfolding factor, as this example shows.

Take the filter $y(n) = x(n) + 3 y(n - 2) + 5 y(n - 3)$, with one adder $A$ of time 1 and two multipliers $B$ (by 3) and $C$ (by 5) of time 2. The edges are $A \to B$ with no delay and $B \to A$ with 2 delays, and $A \to C$ with 1 delay and $C \to A$ with 2 delays. The loop $A \to B \to A$ has ratio $(1 + 2) / 2 = 3/2$, and the loop $A \to C \to A$ has ratio $(1 + 2) / 3 = 1$, so $T_\infty = 3/2$ and $A \to B \to A$ is the critical loop.

The constraints of the proof with $T = 3/2$ give $\sigma_B = \sigma_A + 1$ and allow $\sigma_A = \sigma_C = 0$. So $A$ and $C$ start iteration $k$ at time $1.5 k$ and $B$ starts at $1.5 k + 1$: two samples every 3 time units, which meets the bound. A clocked circuit with no unfolding has an integer period, and the consequence above gives at least $\lceil 3/2 \rceil = 2$; the critical path of the graph as given is $A \to B$, of length 3, and a retiming reaches 2. Unfolding by 2 gives a graph with iteration bound 3 and critical path 3, so 1.5 time units per sample.

## History

Renfors and Neuvo (1981) derived the bound for recursive digital filters built from adders and multipliers, and showed that it can be reached. Parhi and Messerschmitt (1991) showed that unfolding by a suitable factor gives a program that can be scheduled to reach it, which they called rate optimal. Parhi's 1999 textbook made the iteration bound the first tool of DSP architecture design, with algorithms to compute it and its extension to multirate graphs.

## References
