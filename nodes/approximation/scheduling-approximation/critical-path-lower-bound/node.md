---
tag: NX7HGC
kind: concept
slug: critical-path-lower-bound
name: Critical path lower bound
aliases:
- longest chain bound
- chain bound
- critical path bound
area: approximation/scheduling-approximation
level: intro
summary: The longest precedence chain is a lower bound on the makespan.
prereqs: [makespan, makespan-lower-bounds, directed-acyclic-graph]
see_also: [list-scheduling-bound, precedence-constrained-scheduling, hu-algorithm, coffman-graham-algorithm, critical-path, critical-path-method, dag-longest-path, job-shop-scheduling]
sources:
  - paper: doi:10.1002/j.1538-7305.1966.tb01709.x
    title: "R. L. Graham, Bounds for certain multiprocessing anomalies, Bell System Technical Journal 45(9), 1966"
    locator: the bound 2 - 1/m for list scheduling with precedence constraints, proved with a chain that covers the idle time
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 2.3 (list scheduling with precedence constraints and the chain argument)
  - paper: doi:10.1287/opre.9.6.841
    title: "T. C. Hu, Parallel sequencing and assembly line problems, Operations Research 9(6), 1961"
    locator: the counting form of the bound for unit jobs with tree precedence
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 5 (parallel machines with precedence constraints and the critical path)
---

The critical path lower bound says that no schedule can finish before the longest chain of jobs in the precedence graph is done. If job $j$ has length $p_j$ and the jobs of a chain $j_1 \prec j_2 \prec \cdots \prec j_k$ must run one after the other, then every schedule has [makespan](/makespan/) at least $p_{j_1} + \cdots + p_{j_k}$. With the average load it gives the standard bound $\mathrm{OPT} \ge \max\big(L, \frac{1}{m}\sum_j p_j\big)$ for [precedence-constrained scheduling](/precedence-constrained-scheduling/), where $L$ is the length of a longest chain. Graham's analysis of [list scheduling](/list-scheduling-bound/) compares with exactly this bound.

## In plain words

Some tasks must wait for others. Follow a line of tasks where each one waits for the one before it. These tasks can never run at the same time, however many workers you have. So the whole project takes at least as long as the sum of the times on the longest such line.

This is the critical path. It is one of two quick limits on a plan. The other limit is the total work shared among the workers. A plan that keeps the workers busy whenever it can, and always works on the critical path when it is idle, finishes within about twice the larger of the two limits.

## The idea

**Setting.** There are $n$ jobs with lengths $p_j \ge 0$ and $m$ identical machines. A directed acyclic graph on the jobs gives the precedence: $i \prec j$ means that $j$ starts only after $i$ ends. A *chain* is a sequence $j_1 \prec j_2 \prec \cdots \prec j_k$, and its length is $\sum_{r} p_{j_r}$. Let $L$ be the largest length of a chain, $P = \sum_j p_j$, and $\mathrm{OPT}$ the least makespan.

**The bound.** $\mathrm{OPT} \ge L$, and so $\mathrm{OPT} \ge \max(L, P/m)$.

*Proof.* Take any feasible schedule with start times $S_j$ and a chain $j_1 \prec \cdots \prec j_k$. Each job of the chain starts after the one before it ends, so $S_{j_{r+1}} \ge S_{j_r} + p_{j_r}$. By induction $S_{j_k} + p_{j_k} \ge S_{j_1} + \sum_r p_{j_r} \ge \sum_r p_{j_r}$. The makespan is at least the end of $j_k$. For a chain of length $L$ this gives the first claim. The $m$ machines do $P$ units of work by time $C_{\max}$, so $m \, C_{\max} \ge P$, and the second claim follows. $\square$

The bound does not use $m$, and it is the exact optimum when $m \ge n$, because then each job can start as soon as its predecessors end. It holds for every machine environment where a job runs on one machine at a time, including preemptive schedules.

**Computing it.** $L$ is a longest path in a directed acyclic graph with weights on the vertices. One pass in [topological order](/topological-sort/) computes it in $O(n + e)$ time, where $e$ is the number of arcs: the length of the longest chain that ends at $j$ is $p_j$ plus the largest such value over the immediate predecessors of $j$. See [longest path in a DAG](/dag-longest-path/).

**How it is used: Graham's bound.** Run list scheduling: whenever a machine is idle and some job has all its predecessors done, start such a job. Let $C$ be the makespan. Then $C \le P/m + (1 - 1/m) L \le (2 - 1/m)\,\mathrm{OPT}$.

*Proof.* Let $S_j$ and $C_j = S_j + p_j$ be the start and end of job $j$, and let $j_k$ be a job with $C_{j_k} = C$. Build a chain backward. Given $j_r$, if it has a predecessor, let $j_{r-1}$ be a predecessor of $j_r$ with the largest end time; else stop. During $[C_{j_{r-1}}, S_{j_r})$ the job $j_r$ is available but does not start, so list scheduling keeps all machines busy. In the same way all machines are busy during $[0, S_{j_1})$, because $j_1$ has no predecessor. So $[0, C)$ is covered by times when all machines are busy and by the runs $[S_{j_r}, C_{j_r})$ of the chain jobs. During the run of a chain job at most $m - 1$ machines are idle. The total idle time on all machines is then at most $(m - 1) \sum_r p_{j_r} \le (m - 1) L$. Since $m C = P + \text{idle time}$, we get $C \le P/m + (1 - 1/m) L$. Both $P/m$ and $L$ are at most $\mathrm{OPT}$, which gives the claim. $\square$

The ratio is absolute, and it is measured against the lower bound $\max(L, P/m)$ itself, so it also bounds how far the lower bound can be from $\mathrm{OPT}$: $\max(L, P/m) \le \mathrm{OPT} \le (2 - 1/m) \max(L, P/m)$.

**A sharper count for unit jobs.** For unit jobs, let the level of a job be the number of jobs on a longest chain that starts at it, and let $N(h)$ be the number of jobs of level at least $h$. Each such job has $h - 1$ jobs after it in a chain, so all of them run in the first $C - h + 1$ slots of a schedule of makespan $C$. This gives $\mathrm{OPT} \ge \max_h \big(h - 1 + \lceil N(h)/m \rceil\big)$. The case $h = 1$ is the load bound, and the largest $h$ is the chain bound. [Hu's algorithm](/hu-algorithm/) meets this bound exactly on in-trees.

## Examples

**Five jobs on two machines.** Take jobs $a, b, c, d, e$ with lengths $3, 2, 2, 1, 3$, the arcs $a \prec b$, $a \prec c$, $b \prec d$ and $c \prec d$, and $e$ free. The chains $a, b, d$ and $a, c, d$ have length 6, so $L = 6$, and $P/m = 11/2$. So $\mathrm{OPT} \ge 6$. Machine 1 runs $a$ in $[0, 3)$, $b$ in $[3, 5)$ and $d$ in $[5, 6)$, and machine 2 runs $e$ in $[0, 3)$ and $c$ in $[3, 5)$. The makespan is 6, so this schedule is optimal and the bound is exact.

**The bound is not always exact.** Make $e$ one unit longer, so its length is 4, $P/m = 6$ and $L = 6$. A schedule of makespan 6 must start $a$ at 0, run $b$ and $c$ together in $[3, 5)$ and $d$ in $[5, 6)$. Then each machine has free time only in $[0, 3)$ and in $[5, 6)$, and $e$ fits in neither. So $\mathrm{OPT} = 7$, which the schedule with $e$ in $[0, 4)$, $c$ in $[4, 6)$ and $d$ in $[6, 7)$ reaches.

**The bound can be off by almost a factor 2.** Take unit jobs on $m$ machines: a chain $c_1 \prec c_2 \prec \cdots \prec c_K$, and $mK$ more jobs that each precede $c_1$. Then $L = K + 1$ and $P/m = K + K/m$. The $mK$ jobs fill $K$ slots before $c_1$ can start, and the chain takes $K$ more slots, so $\mathrm{OPT} = 2K$. The counting bound with $h = K + 1$ gives $K + \lceil mK/m \rceil = 2K$, which is exact. For $K \ge m$ the ratio $\mathrm{OPT}/\max(L, P/m) = 2m/(m + 1)$ tends to 2 as $m$ grows.

## Where it is used

- **List scheduling with precedence.** Graham's $(2 - 1/m)$ bound, above, and its use in [precedence-constrained scheduling](/precedence-constrained-scheduling/). The chain argument works for every list order.
- **Exact algorithms for unit jobs.** The counting form is the lower bound in the proofs of [Hu's algorithm](/hu-algorithm/) and of the [Coffman-Graham algorithm](/coffman-graham-algorithm/).
- **Shop scheduling.** In a [job shop](/job-shop-scheduling/), the operations of one job form a chain, so $\mathrm{OPT}$ is at least the longest job and at least the largest machine load. The same two bounds appear for [flow shops](/flow-shop-scheduling/) and [open shops](/open-shop-scheduling/).
- **Parallel computing.** The work and span bound of a parallel program is the same pair: $p$ processors need time at least $\max(T_1/p, T_\infty)$, where $T_\infty$ is the [critical path](/critical-path/) of the computation.
- **Project planning.** The [critical path method](/critical-path-method/) computes $L$ and the slack of each task when the number of workers is unlimited, where the bound is exact.

## References
