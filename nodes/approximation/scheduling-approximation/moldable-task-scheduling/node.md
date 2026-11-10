---
tag: MMHVAD
kind: problem
slug: moldable-task-scheduling
name: Moldable task scheduling
aliases:
- malleable task scheduling
- P|any|Cmax
- scheduling parallelizable tasks
area: approximation/scheduling-approximation
level: research
summary: Each task chooses its number of processors, which determines its running time.
prereqs: [makespan-minimization, scheduling-notation, list-scheduling]
see_also: [strip-packing, bin-packing, list-scheduling-bound, makespan-lower-bounds, dual-approximation, ptas, precedence-constrained-scheduling, uniform-machine-scheduling]
sources:
  - paper: "J. Turek, J. L. Wolf and P. S. Yu, Approximate algorithms for scheduling parallelizable tasks, Proceedings of the 4th ACM Symposium on Parallel Algorithms and Architectures (SPAA), 1992"
    locator: the reduction from moldable to rigid tasks by trying a small set of allotments, and the 2-approximation
  - paper: "W. Ludwig and P. Tiwari, Scheduling malleable and nonmalleable parallel tasks, Proceedings of the 5th ACM-SIAM Symposium on Discrete Algorithms (SODA), 1994"
    locator: the faster choice of the allotment, which keeps the ratio 2
  - paper: "G. Mounié, C. Rapine and D. Trystram, A 3/2-approximation algorithm for scheduling independent monotonic malleable tasks, SIAM Journal on Computing 37(2), 2007"
    locator: the dual approximation with ratio 3/2 + ε for monotone tasks
  - paper: "K. Jansen and L. Porkolab, Linear-time approximation schemes for scheduling malleable parallel tasks, Algorithmica 32(3), 2002"
    locator: the approximation scheme for a fixed number of processors
  - paper: "J. Du and J. Y.-T. Leung, Complexity of scheduling parallel task systems, SIAM Journal on Discrete Mathematics 2(4), 1989"
    locator: the NP-hardness results for parallel tasks with a fixed or a free number of processors
---

Moldable task scheduling is [makespan minimization](/makespan-minimization/) for parallel tasks whose number of processors is a choice. There are $m$ identical processors, and task $j$ runs for time $t_j(k)$ if it gets $k$ of them. A schedule chooses for each task its number of processors, its *allotment*, and a start time, and the task then holds that many processors without a break until it ends. The goal is the least [makespan](/makespan/). The problem contains $P \mid\mid C_{\max}$ and is strongly NP-hard. Simple methods reach ratio 2, and for tasks whose speed-up behaves in the usual way, a ratio of $3/2 + \varepsilon$ is known.

## In plain words

You run a computer with many processors and a list of programs. Each program can use one processor or several, and more processors make it end sooner, but usually with some waste. You must decide how many processors each program gets and when it starts, so that all programs end as early as possible.

If you give every program all processors, they run one after the other and the waste adds up. If you give every program one processor, a long program may finish very late. The best plan sits between these extremes, and finding it is hard. Good methods first choose the number of processors of each program with care and then pack the programs like boxes in a strip.

## Definition

**Input.** An integer $m \ge 1$, the number of processors, and $n$ tasks. Task $j$ has a time $t_j(k) > 0$ for each $k \in \{1, \ldots, m\}$, the time it takes on $k$ processors. Its *work* on $k$ processors is $w_j(k) = k \cdot t_j(k)$.

**Output.** For each task an allotment $k_j \in \{1, \ldots, m\}$ and a start time $S_j \ge 0$, such that at every time $t$ the tasks that run at $t$, those with $S_j \le t < S_j + t_j(k_j)$, use at most $m$ processors in total. The processors of a task need not be adjacent.

**Goal.** Minimize $C_{\max} = \max_j (S_j + t_j(k_j))$. The least value is $\mathrm{OPT}$.

**Monotone tasks.** A task is *monotone* if $t_j(k)$ does not grow with $k$ and $w_j(k)$ does not shrink with $k$: more processors never slow a task down and never save work. This is the usual model of a parallel program with overhead, and several results below need it.

*Ratio convention.* This is a minimization problem. An algorithm has ratio $\rho \ge 1$ if $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance. All ratios here are absolute and worst case, and $m$ is part of the input unless the text says otherwise.

| symbol | meaning |
|---|---|
| $n$, $m$ | the number of tasks and the number of processors |
| $t_j(k)$, $w_j(k)$ | the time and the work of task $j$ on $k$ processors |
| $k_j$, $S_j$ | the allotment and the start time of task $j$ in a schedule |
| $\mathrm{OPT}$, $\mathrm{ALG}$ | the optimal makespan, and the makespan of an algorithm |

## Variants

- **Rigid tasks, $P \mid \mathrm{size}_j \mid C_{\max}$.** The allotment of each task is fixed. With unit times this is [bin packing](/bin-packing/) with bins of size $m$.
- **Contiguous processors.** The processors of a task must be adjacent, as on a line of processors. Rigid tasks then become [strip packing](/strip-packing/): rectangles of width $k_j$ and height $t_j$ in a strip of width $m$.
- **Malleable tasks.** The number of processors of a task may change while it runs. In older papers, including those of Turek, Wolf and Yu and of Ludwig and Tiwari, "malleable" means what is called moldable here, which is why the two names are mixed in the literature.
- **Precedence constraints.** Tasks form a graph, as in [precedence-constrained scheduling](/precedence-constrained-scheduling/). Constant ratios are known for monotone tasks, with larger constants than in the independent case.
- **Fixed number of processors.** For constant $m$, Jansen and Porkolab (2002) gave a PTAS that runs in linear time in $n$.

## Examples

**Neither extreme is good.** Take $m = 4$ processors and two monotone tasks. Task $A$ has perfect speed-up, $t_A(k) = 8/k$. Task $B$ cannot use extra processors, $t_B(k) = 4$ for all $k$.

| choice | schedule | makespan |
|---|---|---|
| each task on all 4 processors | $A$ in $[0, 2]$, then $B$ in $[2, 6]$ | 6 |
| each task on 1 processor | $A$ in $[0, 8]$ and $B$ in $[0, 4]$ | 8 |
| $A$ on 3 processors, $B$ on 1 | both start at 0; $A$ ends at $8/3$, $B$ at 4 | 4 |

The last choice is optimal, since task $B$ alone needs time 4.

**Lower bounds.** For monotone tasks, $t_j(m)$ is the least time of task $j$ and $w_j(1) = t_j(1)$ its least work, so $\mathrm{OPT} \ge \max_j t_j(m)$ and $\mathrm{OPT} \ge \frac1m \sum_j t_j(1)$. In the example these give $\max(2, 4) = 4$ and $(8 + 4)/4 = 3$, and the first one is tight.

## Known algorithms

| algorithm | ratio $\rho$ | tasks | time |
|---|---|---|---|
| Turek, Wolf and Yu 1992 | 2 | any | polynomial, tries $O(nm)$ allotments |
| Ludwig and Tiwari 1994 | 2 | any | about $O(nm)$ for the allotment, plus the rigid schedule |
| Mounié, Rapine and Trystram 2007 | $3/2 + \varepsilon$ | monotone | polynomial |
| Jansen and Porkolab 2002, fixed $m$ | $1 + \varepsilon$ (PTAS) | any | linear in $n$ for fixed $m$ and $\varepsilon$ |
| Jansen and Thöle 2010 | $1 + \varepsilon$ when $m$ is bounded by a polynomial in $n$ | any | polynomial in that case |

**The idea of the 2-approximation (sketch only).** For a fixed allotment, the tasks are rigid. Write $W$ for the total work and $t_{\max}$ for the longest time under the allotment. Turek, Wolf and Yu use an algorithm for rigid tasks whose makespan is at most $2 \max(W/m, t_{\max})$, so it suffices to choose an allotment that keeps $\max(W/m, t_{\max})$ small. For a guess $T$, give each task the allotment of least work among those with $t_j(k) \le T$. Only $O(nm)$ values of $T$ matter, one for each time $t_j(k)$, and the best of these candidates has $\max(W/m, t_{\max}) \le \mathrm{OPT}$: at $T = \mathrm{OPT}$, each task gets work at most its work in an optimal schedule, so $W \le m \cdot \mathrm{OPT}$, and $t_{\max} \le T$. Ludwig and Tiwari find the best allotment faster. The algorithm for rigid tasks and its proof are in the papers.

**The 3/2 method.** Mounié, Rapine and Trystram use [dual approximation](/dual-approximation/): for a guess $T$, they split the tasks into two shelves of heights $T$ and $T/2$, choose the allotments by a knapsack-like dynamic program that keeps the total work at most $mT$, and repair the shelves so that every task fits in $3T/2$. Monotony is used to bound the work of a task when its allotment changes.

## Bounds

- **Lower bounds on OPT.** $\mathrm{OPT} \ge \max_j \min_k t_j(k)$ and $\mathrm{OPT} \ge \frac1m \sum_j \min_k w_j(k)$. For monotone tasks the minima are at $k = m$ and $k = 1$.
- **Strong NP-hardness.** If $t_j(k) = p_j$ for all $k$, extra processors never help, each task may as well use one, and the problem is $P \mid\mid C_{\max}$. This case is monotone, so the problem is strongly NP-hard even for monotone tasks. Du and Leung (1989) studied the complexity of these models in detail, also for a fixed number of processors.
- **No ratio below 3/2 for general tasks.** If the times are not required to be monotone, a task can be forced to use exactly $s_j$ processors by giving it a huge time on every other allotment. With unit times this embeds bin packing, and deciding whether $\mathrm{OPT} \le 2$ is then as hard as deciding whether the items fit in 2 bins, which contains [partition](/partition-problem/). So no polynomial algorithm has ratio below $3/2$ unless P = NP.
- **The monotone case.** The best ratio known is $3/2 + \varepsilon$. Whether the monotone problem has a PTAS when $m$ is not bounded by a polynomial in $n$ is, as far as is known, open.

## Reductions

**To rigid tasks.** Once the allotment is chosen, the problem is rigid task scheduling, and every approximation for rigid tasks with ratio $\alpha$ against the bound $\max(W/m, t_{\max})$ gives ratio $\alpha$ for moldable tasks by the allotment choice above.

**From identical machines.** Tasks with $t_j(k) = p_j$ give $P \mid\mid C_{\max}$.

**To strip packing.** With contiguous processors and a fixed allotment, the problem is strip packing, and methods for strip packing apply.

## Applications

- Scheduling parallel programs on a supercomputer or a cluster, where each program can run on a chosen number of nodes.
- Scientific workflows whose stages can use more or fewer cores.
- Training many machine learning models at once on a pool of accelerators.

## References
