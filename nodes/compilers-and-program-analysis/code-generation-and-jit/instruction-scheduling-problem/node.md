---
tag: JX5Y00
kind: problem
slug: instruction-scheduling-problem
name: Instruction scheduling
aliases:
- instruction scheduling problem
area: compilers-and-program-analysis/code-generation-and-jit
level: core
summary: Order the instructions of a block or region so that dependences and machine resources are respected and the run time is least.
prereqs: [basic-block, data-dependence, directed-acyclic-graph, np-complete, precedence-constrained-scheduling]
see_also: [list-scheduling, list-scheduling-bound, trace-scheduling, superblock-scheduling, software-pipelining, iterative-modulo-scheduling, register-allocation-problem, resource-constrained-scheduling]
sources:
  - paper: doi:10.1145/2166.357217
    title: John L. Hennessy and Thomas R. Gross, Postpass code optimization of pipeline constraints, ACM TOPLAS 5(3), 1983, 422-448
    locator: the model of a pipeline that stalls when an instruction reads a result too early, the statement that finding an optimal order with arbitrary latencies is NP-complete, and a heuristic that reorders the instructions of a basic block
  - paper: doi:10.1145/12276.13312
    title: Philip B. Gibbons and Steven S. Muchnick, Efficient instruction scheduling for a pipelined architecture, Proceedings of the SIGPLAN '86 Symposium on Compiler Construction, 1986, 11-16
    locator: list scheduling of the dependence DAG of a basic block for a pipelined machine, with priorities from stalls, the number of successors and the length of the longest path
  - paper: doi:10.1016/S0022-0000(75)80008-0
    title: Jeffrey D. Ullman, NP-complete scheduling problems, Journal of Computer and System Sciences 10(3), 1975, 384-393
    locator: the NP-completeness of scheduling unit-time jobs with precedence constraints on a number of processors that is part of the input
  - paper: doi:10.1287/opre.26.1.22
    title: Jan Karel Lenstra and Alexander H. G. Rinnooy Kan, Complexity of scheduling under precedence constraints, Operations Research 26(1), 1978, 22-35
    locator: the reduction from clique that makes it NP-complete to decide whether unit-time jobs with precedence constraints fit in three time slots
  - paper: doi:10.1145/59287.59291
    title: David Bernstein and Izidor Gertner, Scheduling expressions on a pipelined processor with a maximal delay of one cycle, ACM TOPLAS 11(1), 1989, 57-66
    locator: an optimal polynomial algorithm for one pipelined processor when every delay is 0 or 1 cycle
  - paper: doi:10.1145/155183.155190
    title: Krishna V. Palem and Barbara B. Simons, Scheduling time-critical instructions on RISC machines, ACM TOPLAS 15(4), 1993, 632-658
    locator: scheduling instructions with latencies and deadlines on pipelined processors, with an optimal algorithm for small latencies and bounds for greedy schedules
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 12 (Instruction Scheduling), the dependence graph, list scheduling and regional scheduling
  - book: isbn:9781558603202
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Chapter 17 (Code Scheduling), basic block scheduling, cross-block scheduling and software pipelining
---

Instruction scheduling chooses the order, and on a machine that issues several instructions per cycle the grouping, of the instructions of a program. The order must keep every dependence, and each instruction must wait until the results it reads are ready. In each cycle, the machine resources must suffice. The goal is the fewest cycles. Modern processors are pipelined: a load can take three cycles before its result is ready, while the processor could start other instructions in the meantime. A good order fills these waiting cycles with independent work. This page states the problem and proves that it is NP-complete. The scheduler pages give the methods.

## In plain words

A processor works like an assembly line. It can start a new instruction every cycle, but some results take several cycles to come out. If the next instruction needs a result that is not ready, the processor waits and does nothing. The compiler can avoid many of these waits by moving instructions that do not depend on each other into the gaps. It must never move an instruction before one whose result it needs. It must also not use more adders or memory ports in one cycle than the processor has. Instruction scheduling chooses such an order with as few cycles as possible. For more than a few instructions, no fast method is known that always finds the best order.

## Definition

The *dependence graph* of a basic block is a [directed acyclic graph](/directed-acyclic-graph/) $G = (V, A)$ with one vertex for each instruction. There is an arc $(u, v)$ when $v$ must come after $u$ (see [data dependence](/data-dependence/)):

- a *true* dependence: $v$ reads a value that $u$ writes;
- an *anti* dependence: $v$ writes a value or a memory cell that $u$ reads;
- an *output* dependence: both write the same value or cell.

Each arc has a *delay* $\delta(u, v) \ge 0$. Each instruction $i$ has a *latency* $d_i \ge 1$, the number of cycles until its result is ready. For a true dependence $\delta(u, v) = d_u$. For anti and output dependences the delay is 0 or 1, as the machine needs.

The *machine* issues at most $W$ instructions per cycle, its *issue width*. Each instruction has a class $c(i)$, such as memory or arithmetic, and at most $\mathrm{cap}(c)$ instructions of class $c$ can issue in one cycle. The units are pipelined: an instruction uses its unit only in the cycle where it issues.

A *schedule* gives each instruction an issue cycle $t_i \in \{0, 1, 2, \ldots\}$ such that:

1. $t_v \ge t_u + \delta(u, v)$ for every arc $(u, v)$;
2. at most $W$ instructions have the same $t_i$, and at most $\mathrm{cap}(c)$ of them have class $c$.

Its *length* is $\max_i (t_i + d_i)$, the cycle when the last result is ready. The problem is to find a schedule of least length. In the decision form, an integer $T$ is also given, and the question is whether a schedule of length at most $T$ exists.

Unit latencies, one class and width $m$ give exactly the scheduling problem $P \mid \mathrm{prec}, p_j = 1 \mid C_{\max}$ of [precedence-constrained scheduling](/precedence-constrained-scheduling/): an instruction is a unit job, an issue cycle is a time slot, and the length is the [makespan](/makespan/).

## Variants

- **Local scheduling** orders the instructions of one [basic block](/basic-block/), the form defined above.
- **Global or regional scheduling** moves instructions across block boundaries. The region is a likely path ([trace scheduling](/trace-scheduling/)), a path with one entry ([superblock scheduling](/superblock-scheduling/)), or a tree of blocks. Moving an instruction above a branch or below a join needs extra care so that the other paths still compute the same values.
- **Loop scheduling** overlaps the iterations of a loop ([software pipelining](/software-pipelining/)). The goal is a short interval between the starts of two iterations, not a short block. [Iterative modulo scheduling](/iterative-modulo-scheduling/) is the main algorithm.
- **Scheduling with register pressure.** Moving loads early makes more values live at once and can force spills. A scheduler before [register allocation](/register-allocation-problem/) often limits the number of live values. A scheduler after allocation must also respect the anti and output dependences that register reuse adds. This is the phase ordering problem between the two.
- **Out-of-order processors** reorder instructions in hardware within a window. A compiler scheduler still helps for long latencies and for in-order cores, such as many embedded and VLIW processors, where the order in the code is the order of execution.

## Examples

**Filling load delays.** The block below reads three values. Loads have latency 3, multiplications 2 and additions 1. The machine issues one instruction per cycle.

```
a = load x
b = a * 3
c = load y
d = c + 1
e = b + d
f = load z
g = e * f
```

The arcs are $a \to b$ (delay 3), $c \to d$ (3), $b \to e$ (2), $d \to e$ (1), $e \to g$ (1) and $f \to g$ (3). An in-order processor that runs the instructions as written stalls whenever an operand is not ready. It issues `a` at cycle 0, `b` at 3, `c` at 4, `d` at 7, `e` at 8, `f` at 9 and `g` at 12, so the length is $12 + 2 = 14$.

A list scheduler gives each instruction its *height*, the longest sum of delays on a path from it to the end, plus the latency of the last instruction. The heights are $a$: 8, $c$: 7, $b$: 5, $f$: 5, $d$: 4, $e$: 3, $g$: 2. In each cycle it issues the ready instruction of greatest height:

| cycle | ready | issue |
|---|---|---|
| 0 | $a, c, f$ | $a$ |
| 1 | $c, f$ | $c$ |
| 2 | $f$ | $f$ |
| 3 | $b$ | $b$ |
| 4 | $d$ | $d$ |
| 5 | $e$ | $e$ |
| 6 | $g$ | $g$ |

The length is $6 + 2 = 8$. No schedule is shorter, because the path $a \to b \to e \to g$ alone needs $3 + 2 + 1 + 2 = 8$ cycles. So this order is optimal, and it is almost twice as fast as the order in the code. A machine with width 2 and one memory port gains nothing more here, for the same reason. A script found the same length 8 by trying every schedule.

**The longest path rule can lose.** Take six instructions on the same machine, with loads of latency 3 and additions of latency 1:

```
i = j + 1
u = load i
v = u + 1
w = load k
y = w + 1
z = w * 2
```

Here the multiplication has latency 1. The arcs are $i \to u$ (delay 1), $u \to v$ (3), $w \to y$ (3) and $w \to z$ (3). The heights are $i$: 5, $u$: 4, $w$: 4, and 1 for the rest. The list scheduler issues $i$ at cycle 0, then $u$ and $w$ at cycles 1 and 2 in either order. At cycle 3 nothing is ready, so it waits, and it ends at length 7. The schedule $w, i, u, y, z, v$ at cycles 0 to 5 keeps every delay ($u$ at 2 and $v$ at 5, $w$ at 0 and $y$, $z$ at 3 and 4) and has length 6, which is optimal because six instructions need six cycles. The instruction with the longest path should not go first here, because $w$ has two successors that can fill the gap.

## Known algorithms

- **List scheduling.** Build the dependence graph, give each instruction a priority, and go cycle by cycle, issuing the ready instructions of highest priority that the resources allow. It is the method of almost every compiler, often with the height as the main priority and the number of successors or the register pressure to break ties (Gibbons and Muchnick 1986). It is the [list scheduling](/list-scheduling/) of Graham with three changes. Time goes in cycles, and an instruction is ready $\delta$ cycles after its predecessor *issues*, not when that predecessor ends. A unit is busy for one cycle even when the result comes later. And there are several classes of units. So a cycle can be empty while every unit is free, because each ready instruction waits for a latency, and the proof of [Graham's bound](/list-scheduling-bound/), which counts busy machines, does not apply as written.
- **Optimal methods.** Branch and bound over the list orders, or an integer linear program with a 0-1 variable for each instruction and cycle, find the optimum for blocks of a few dozen instructions. They are used for hot code and to judge heuristics.
- **Polynomial special cases.** Unit latencies on one issue slot need no scheduling at all, since any topological order has length $|V|$. With delays of 0 or 1 on one issue slot, an optimal schedule can be found in polynomial time (Bernstein and Gertner 1989). With unit latencies, one class and two issue slots, the [Coffman-Graham algorithm](/coffman-graham-algorithm/) is optimal. With unit latencies and an in-tree, [Hu's algorithm](/hu-algorithm/) is optimal for any width.
- **Regional schedulers.** [Trace scheduling](/trace-scheduling/) and [superblock scheduling](/superblock-scheduling/) list-schedule a long path and repair the other paths. [Iterative modulo scheduling](/iterative-modulo-scheduling/) schedules loops.

## Bounds

**Theorem 1.** The decision form is in NP.

*Proof.* A schedule with length at most $T$ has every $t_i < T$, so it is a certificate of polynomial size. Conditions 1 and 2 and the length are checked in time $O(|V| + |A|)$ with one counter per cycle and class. $\square$

**Theorem 2 (Ullman 1975).** The decision form is NP-complete when the issue width is part of the input, even with one class and all latencies 1.

*Proof.* With these restrictions, a schedule is a map from the instructions to cycles where each arc goes to a later cycle and each cycle holds at most $W$ instructions, and its length is the last cycle plus 1. This is word for word a schedule of unit jobs on $W$ identical machines with precedence constraints, and its makespan. So the two decision problems are the same. The second is NP-complete, and the reduction from clique of Lenstra and Rinnooy Kan is given on the page on [precedence-constrained scheduling](/precedence-constrained-scheduling/). $\square$

Real processors have a fixed width, so Theorem 2 does not settle the case that matters. The next theorem does: one issue slot is enough for hardness once the latencies are part of the input. Hennessy and Gross (1983) stated this; here is a complete proof by a reduction from [clique](/clique-problem/).

**Theorem 3.** The decision form is strongly NP-complete for a machine with issue width 1 and one class, when the latencies are part of the input.

*Proof.* Take a graph $H$ with $n$ vertices and $e$ edges and an integer $k$ with $2 \le k \le n$. The question is whether $H$ has a clique of $k$ vertices. Let $l = k(k-1)/2$. If $l > e$ the answer is no, and we output a fixed instance with answer no. Otherwise let

$$L = n + e, \quad h_2 = l + n - k, \quad h_3 = e - l, \quad T = 2L + n + e.$$

The instance has three kinds of instructions, with every delay equal to the latency of the source:

- a *vertex* instruction $x_a$ for each vertex $a$, with latency $L$;
- an *edge* instruction $y_{ab}$ for each edge $ab$, with latency 1, and the arcs $x_a \to y_{ab}$ and $x_b \to y_{ab}$;
- a chain $s_0 \to s_1 \to \cdots \to s_{2L-1}$ of $2L$ *frame* instructions. The delays along the chain are $k + 1$ from $s_0$, then 1 up to $s_{L-1}$, then $h_2 + 1$ from $s_{L-1}$, then 1 up to $s_{2L-2}$, then $h_3 + 1$ from $s_{2L-2}$. Each frame instruction has the latency of its outgoing arc, and $s_{2L-1}$ has latency 1.

There are $n + e + 2L = T$ instructions. The delays along the chain add up to $(k + 1) + (L - 2) + (h_2 + 1) + (L - 2) + (h_3 + 1) = 2L + k + h_2 + h_3 - 1 = T - 1$, since $k + h_2 + h_3 = n + e$.

*Frames are fixed.* In a schedule of length at most $T$, every $t_i \le T - 1$, since $d_i \ge 1$. With one issue slot, the $T$ instructions fill the cycles $0$ to $T - 1$ exactly. The chain needs $t(s_{2L-1}) - t(s_0) \ge T - 1$, so $s_0$ is at cycle 0, $s_{2L-1}$ is at cycle $T - 1$, and every chain arc is tight. So the frame takes cycle 0, the $L - 1$ cycles from $k + 1$ up to $k + L - 1$, the $L - 1$ cycles from $k + L + h_2$ up to $k + 2L + h_2 - 2$, and cycle $T - 1$. The free cycles form three holes: $H_1 = [1, k]$ with $k$ cycles, $H_2 = [k + L, k + L + h_2 - 1]$ with $h_2$ cycles, and $H_3$ with $h_3$ cycles just before $T - 1$.

*No edge in $H_1$.* An edge instruction issues at least $L$ cycles after a vertex instruction, so at cycle $L$ or later, and $L = n + e > k$ because $n \ge k$ and $e \ge l \ge 1$. So $H_1$ holds $k$ vertex instructions. Call their vertices $K$.

*Edges in $H_2$ have both ends in $K$.* If an end of $y_{ab}$ is not in $K$, its vertex instruction is at cycle $k + L$ or later, since the cycles between $H_1$ and $H_2$ belong to the frame. Then $y_{ab}$ is at cycle $k + 2L$ or later, which is after $H_2$, because $L \ge h_2$.

*A schedule gives a clique.* $H_2$ holds $h_2 = l + (n - k)$ instructions. Each is one of the $n - k$ vertex instructions outside $K$, or an edge instruction with both ends in $K$. A set of $k$ vertices spans at most $l$ edges. So $H_2$ holds exactly $l$ edges inside $K$, and $K$ is a clique of size $k$.

*A clique gives a schedule.* Put the frame as above, the clique $K$ in $H_1$, the other $n - k$ vertices and the $l$ edges inside $K$ in $H_2$, and the other $e - l$ edges in $H_3$, each hole in any order. An edge in $H_2$ issues at $k + L$ or later and its ends at $k$ or earlier. An edge in $H_3$ issues at $k + 2L + h_2 - 1$ or later and its ends at $k + L + h_2 - 1$ or earlier. So every delay holds. The last result of a vertex instruction is ready at $k + 2L + h_2 - 1 \le T$ at most, since $l \le e + 1$. Every frame instruction is ready at the issue cycle of the next one, and every other instruction issues by $T - 2$ with latency 1. So the length is at most $T$.

The instance has $3(n + e)$ instructions and all numbers are at most $T$, so the reduction is polynomial even when the numbers are written in unary. With Theorem 1, the problem is strongly NP-complete. $\square$

A script built this instance for 43 random graphs with 3 to 5 vertices and $k$ from 2 to 4, and solved each with an exact search over all schedules that did not use the fixed frame. The schedule existed exactly for the 33 graphs with a clique.

**Open cases.** With a fixed width and latencies bounded by a constant, the complexity is not known in general. The case of width 3, one class and unit latencies is the scheduling problem $P3 \mid \mathrm{prec}, p_j = 1 \mid C_{\max}$, a famous open question.

**Lower bounds on the length.** Simple bounds still help to judge a schedule:

- **Path bound.** Every schedule is at least as long as the longest path, where a path counts the delays of its arcs and the latency of its last instruction. In the first example this bound is 8 and is reached.
- **Resource bound.** Every schedule has length at least $\lceil |V| / W \rceil$, and at least $\lceil n_c / \mathrm{cap}(c) \rceil$ for each class $c$ with $n_c$ instructions. In the second example $|V| = 6$ gives the bound 6.
- **List schedules.** A list schedule leaves no cycle empty while an instruction is ready and a unit for it is free, but it can still be longer than the optimum, as the second example shows. By Theorem 3, no rule that runs in polynomial time gives an optimal schedule on every block unless P = NP.

## Reductions

- **From precedence-constrained scheduling.** Unit latencies, one class and width $m$ give $P \mid \mathrm{prec}, p_j = 1 \mid C_{\max}$, as in Theorem 2. [Resource-constrained scheduling](/resource-constrained-scheduling/) in high-level synthesis is the same problem with operations in place of instructions and functional units in place of issue slots.
- **From clique.** Theorem 3 above.
- **To integer programming.** A 0-1 variable $z_{i,\tau}$ says that $i$ issues at cycle $\tau$. Each instruction has exactly one cycle, each cycle and class have a capacity, and each arc gives a linear constraint on $\sum_\tau \tau z_{i,\tau}$. Exact schedulers solve this model.

## Applications

Every compiler for a pipelined processor has an instruction scheduler. It matters most for in-order and VLIW processors, where the code order is the run order, and for long-latency operations such as loads and floating-point arithmetic on any processor. The same problem appears in high-level synthesis, where operations are scheduled on hardware units, and in the scheduling of tasks with communication delays on parallel machines.

## References
