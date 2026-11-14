---
tag: 162MZ5
kind: problem
slug: multi-threshold-voltage-assignment
name: Multiple threshold voltage assignment
aliases:
- dual-Vt assignment
- multi-Vt optimization
area: eda/power-reliability-and-manufacturability
level: advanced
summary: Choose a low or high threshold voltage cell for each gate so that leakage is least while every timing path still meets its required time.
prereqs: [leakage-power, static-timing-analysis, knapsack-problem]
see_also: [gate-sizing, tilos, clustered-voltage-scaling, knapsack-dynamic-programming, weak-np-hardness, lagrangian-relaxation, binary-integer-programming, power-gating]
sources:
  - paper: "Liqiong Wei, Zhanping Chen, Mark Johnson, Kaushik Roy and Vivek De, Design and optimization of low voltage high performance dual threshold CMOS circuits, Proceedings of the 35th Design Automation Conference, 489 to 494, 1998"
    title: Liqiong Wei, Zhanping Chen, Mark Johnson, Kaushik Roy and Vivek De, Design and optimization of low voltage high performance dual threshold CMOS circuits, Proceedings of the 35th Design Automation Conference, 489 to 494, 1998
    locator: the dual threshold problem, a high threshold for gates off the critical paths and a low threshold on them, with the leakage and delay models
  - paper: "Liqiong Wei, Zhanping Chen, Kaushik Roy, Mark C. Johnson, Yibin Ye and Vivek K. De, Design and optimization of dual-threshold circuits for low-voltage low-power applications, IEEE Transactions on Very Large Scale Integration (VLSI) Systems 7(1), 16 to 24, 1999"
    title: Liqiong Wei, Zhanping Chen, Kaushik Roy, Mark C. Johnson, Yibin Ye and Vivek K. De, Design and optimization of dual-threshold circuits for low-voltage low-power applications, IEEE Transactions on Very Large Scale Integration (VLSI) Systems 7(1), 16 to 24, 1999
    locator: the journal form of the problem and of its algorithm for the threshold assignment
  - paper: doi:10.1109/4.52187
    title: Takayasu Sakurai and A. Richard Newton, Alpha-power law MOSFET model and its applications to CMOS inverter delay and other formulas, IEEE Journal of Solid-State Circuits 25(2), 584 to 594, 1990
    locator: the delay of a gate as a function of the supply and threshold voltages, with the fitted exponent alpha
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: the NP-completeness of 0-1 knapsack in its decision form, and the meaning of NP-complete in the weak sense
---

Multiple threshold voltage assignment is the problem of choosing, for each gate of a circuit, one of a few versions of its cell that differ only in the threshold voltage $V_T$ of their transistors, so that the total leakage power is least and every timing path still meets its required time. A low threshold gives a fast cell that leaks much. A high threshold gives a slower cell that leaks much less, often 10 to 20 times less for a step of 100 mV. Most gates of a circuit are not on a critical path, so they can take the high threshold with no loss of speed, and only the gates on the near-critical paths need the low one. Modern libraries offer two to four threshold flavors of every cell, and every flow for low leakage does this assignment. The problem is NP-hard even on a single chain of gates, by a direct reduction from 0-1 knapsack, and on a chain it is exactly a knapsack, so it is NP-hard only in the weak sense there.

## In plain words

Each gate comes in two versions with the same function: a fast one that wastes much power even when idle, and a slow one that wastes little. You want the slow version wherever you can afford it.

The catch is the clock. Every path from an input to an output must finish in time. Putting slow gates on a path uses up its spare time, and gates that share many paths use up the spare time of all of them. So the choice is a puzzle: pick which gates to slow down so that the most leakage is saved and no path is late.

## Definition

**Instance.** A combinational circuit as a directed acyclic graph of gates $V$, as in [static timing analysis](/static-timing-analysis/). For each gate $v$ and each threshold flavor $t$ from a small set, ordered from lowest to highest $V_T$, a delay $d_t(v)$ and a leakage $\ell_t(v)$, with $d_t(v)$ not falling and $\ell_t(v)$ not rising as $V_T$ rises. A required time $T$ at the outputs, with arrival time 0 at the inputs. In the dual case there are two flavors, L and H.

**Output.** An assignment $\tau : V \to$ flavors such that, for every path $p$ from an input to an output,

$$ \sum_{v \in p} d_{\tau(v)}(v) \le T, $$

with the least total leakage $\sum_{v \in V} \ell_{\tau(v)}(v)$. If the all-L assignment misses $T$, there is no feasible assignment.

**Decision version.** Given also a bound $B$, is there a feasible assignment with total leakage at most $B$?

The fixed delays $d_t(v)$ are a simplification. In a real cell the delay also depends on the load, including the wires, whose delay models such as the [Elmore delay](/elmore-delay/) estimate, on the input slope and on the sizes of the other gates, and the timing of the full circuit is checked by static timing analysis. The leakage $\ell_t(v)$ is often weighted by the probability of each input state, since the leakage of a cell depends on its inputs.

**What is fitted.** The subthreshold leakage of a transistor is close to $I_0 e^{(V_{GS} - V_T)/(n\, v_T)}$, where $v_T = kT/q \approx 25.9$ mV at 300 K is the thermal voltage (here $T$ is the temperature, a different use of the letter), and the slope factor $n$, usually between 1.2 and 1.6, and the prefactor $I_0$ are fitted to measured or simulated devices, as on the [leakage power](/leakage-power/) page. With $n = 1.5$, a step of 100 mV in $V_T$ cuts the leakage by $e^{0.1/(1.5 \cdot 0.02585)} \approx 13$. The delay follows the alpha-power law of Sakurai and Newton (1990), $d \propto C V_{DD} / (V_{DD} - V_T)^a$, with the exponent $a$ fitted, between 1 and 2 for short channels. With $V_{DD} = 1$ V, $V_T$ of 0.3 V and 0.4 V and $a = 1.3$, the high flavor is slower by $(0.7/0.6)^{1.3} \approx 1.22$. In practice the library gives $d_t$ and $\ell_t$ in tables from characterization, and the formulas only explain their trend.

## Variants

- **Dual-Vt and multi-Vt.** Two flavors, or three to four flavors such as ultra-low, low, standard and high threshold.
- **With gate sizing.** Choose the size and the threshold of each gate together. The delay of a gate then depends on the sizes of the gates it drives, as on the [gate sizing](/gate-sizing/) page.
- **With supply voltages.** Choose both a supply and a threshold for each gate, which adds the level conversion rules of [clustered voltage scaling](/clustered-voltage-scaling/).
- **Per transistor or per stack.** Give a high threshold to some transistors of a cell only, for example those in a series stack, at a finer grain than a cell.
- **Statistical.** The thresholds vary from die to die and within a die, so the leakage and the delays are random, and the target is a yield or a high percentile of the leakage.
- **Standby and active.** In standby, [power gating](/power-gating/) cuts the leakage of whole blocks, and the threshold assignment matters for the leakage while the block is active.

## Examples

**A small circuit.** Gate $a$ feeds gates $b$ and $c$, which both feed gate $d$. The paths are $a b d$ and $a c d$, and $T = 45$ ps. The table gives the delays in ps and the leakages in nW.

| gate | $d_L$ | $d_H$ | $\ell_L$ | $\ell_H$ |
|---|---|---|---|---|
| a | 10 | 12 | 13 | 1 |
| b | 20 | 25 | 39 | 3 |
| c | 10 | 12 | 13 | 1 |
| d | 10 | 12 | 13 | 1 |

With all gates at L the paths take 40 ps and 30 ps, and the leakage is 78 nW. The path $a b d$ has only 5 ps of slack. Gate $b$ at H uses all of it, and then $a$ and $d$ must stay at L, but $c$ can go to H: the assignment $\{b, c\}$ at H gives delays of 45 ps and 32 ps and a leakage of 30 nW. The other way to use the slack of $a b d$ is $a$ and $d$ at H, 2 ps each, with $c$ also at H: delays of 44 ps and 36 ps and a leakage of 42 nW. This choice moves three gates to H and saves less than the choice that moves two. An enumeration of all 16 assignments shows that $\{b, c\}$ is the unique optimum. Gates $a$ and $d$ are on both paths, so each picosecond added to them costs slack on both, while the large gate $b$ saves the most leakage per picosecond.

**A chain is a knapsack.** On a chain of gates $1, \ldots, n$ there is one path. With two flavors, moving gate $j$ to H costs $d_H(j) - d_L(j)$ of the slack $T - \sum_j d_L(j)$ and saves $\ell_L(j) - \ell_H(j)$ of leakage. Choosing the set of gates at H is a 0-1 [knapsack](/knapsack-problem/) with these weights, values and capacity.

## Known algorithms

- **Slack-based greedy rules.** Wei et al. (1998) give gates off the critical paths the high threshold and keep the critical gates at the low one, guided by the slack of each gate. Later rules rank the gates by leakage saved per unit of delay added, in the manner of [TILOS](/tilos/) for gate sizing. These are heuristics with no bound on the gap.
- **[Lagrangian relaxation](/lagrangian-relaxation/).** Move the path constraints into the objective with multipliers on the timing arcs, as for [gate sizing](/gate-sizing/), and solve each gate on its own for fixed multipliers.
- **[Integer linear programming](/binary-integer-programming/).** One 0-1 variable per gate and flavor, with arrival time variables at each gate. Exact, and used for small circuits or for windows of a large one.
- **[Knapsack dynamic programming](/knapsack-dynamic-programming/)** on a chain, with integer delays. Exact in time pseudo-polynomial in $T$.

## Bounds

**Theorem (weak NP-hardness on a chain).** The decision version is NP-complete, even when the circuit is a chain and there are two flavors.

*Proof.* It is in NP: given an assignment, static timing analysis finds the longest path in linear time, and the leakage is a sum. For hardness, reduce from the decision form of 0-1 knapsack: given items $1, \ldots, n$ with positive integer weights $w_j$ and values $p_j$, a capacity $W$ and a target $P$, is there a set $S$ with $\sum_{j \in S} w_j \le W$ and $\sum_{j \in S} p_j \ge P$? Build a chain of $n$ gates. Gate $j$ has $d_L(j) = 1$, $d_H(j) = 1 + w_j$, $\ell_L(j) = p_j + 1$ and $\ell_H(j) = 1$. Set $T = n + W$ and $B = n + \sum_j p_j - P$. Let $S$ be the set of gates at H. The only path has delay $n + \sum_{j \in S} w_j$, which is at most $T$ if and only if $\sum_{j \in S} w_j \le W$. The leakage is $n + \sum_{j \notin S} p_j = n + \sum_j p_j - \sum_{j \in S} p_j$, which is at most $B$ if and only if $\sum_{j \in S} p_j \ge P$. So the chain has a feasible assignment of leakage at most $B$ if and only if the knapsack has a set of weight at most $W$ and value at least $P$. The instance has size polynomial in that of the knapsack, with its numbers written in binary. Since 0-1 knapsack is NP-complete (Garey and Johnson, 1979), so is this problem. $\square$

Also $d_L < d_H$ and $\ell_L > \ell_H$ for every gate, so the hard instances meet the trend of real libraries. A script checked the identity $\text{opt}_{\text{chain}} = n + \sum_j p_j - \text{opt}_{\text{knapsack}}$ by enumeration on 300 random small instances with seed 1.

- **Weak, not strong, on a chain.** The reduction uses large numbers. Conversely, on a chain with integer delays, the problem is a 0-1 knapsack with capacity $T - \sum_j d_L(j)$, which a dynamic program solves in $O(n T)$ time, pseudo-polynomial. So on chains the problem is not NP-hard in the strong sense unless P = NP. See [weak NP-hardness](/weak-np-hardness/).
- **Open here: strong hardness on DAGs.** On a general DAG the constraints are one per path, and a gate on many paths takes slack from all of them. This page does not prove that the problem on DAGs with fixed delays is NP-hard in the strong sense, nor does it give a pseudo-polynomial algorithm for it. We state it as open.
- **Easy cases.** If every path meets $T$ with all gates at H, the all-H assignment is feasible and optimal. If moving any single gate to H makes the circuit miss $T$, the all-L assignment is the only feasible one.
- **What is measured.** The leakage savings that the papers report, often a large fraction of the leakage at no loss of speed, are measurements on their circuits and libraries. This page does not repeat them.

## Reductions

- **From 0-1 knapsack.** On a chain, the problem and 0-1 knapsack reduce to each other, by the theorem above and the example.
- **To integer programming.** The problem is a 0-1 program with a linear objective and one linear constraint per path, or with arrival time variables, one constraint per timing arc.
- **To gate sizing.** Threshold flavors act as discrete sizes with their own delay and leakage, so a solver for discrete [gate sizing](/gate-sizing/) with a leakage objective solves it.

## Applications

- **Leakage reduction in every low-power flow.** After timing closure, the gates with slack are moved to higher threshold flavors.
- **Mixed with other methods.** Threshold assignment works with [clustered voltage scaling](/clustered-voltage-scaling/) for the dynamic power and with [power gating](/power-gating/) for the standby leakage.
- **Engineering changes.** A late swap of a threshold flavor keeps the footprint of the cell, so it can fix timing or leakage without moving any cell.

## References
