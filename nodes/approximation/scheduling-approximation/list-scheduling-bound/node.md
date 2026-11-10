---
tag: BYZM6P
kind: theorem
slug: list-scheduling-bound
name: Graham's bound for list scheduling
aliases:
- (2-1/m)-approximation theorem
- Graham's bound
area: approximation/scheduling-approximation
level: core
summary: Any list schedule has makespan at most (2-1/m) times the optimum.
prereqs: [list-scheduling, makespan-lower-bounds, approximation-ratio]
see_also: [list-scheduling, lpt-bound, graham-anomalies, critical-path-lower-bound, precedence-constrained-scheduling, list-scheduling-competitive-ratio, sorted-balance, multifit-bound]
sources:
  - paper: doi:10.1002/j.1538-7305.1966.tb01709.x
    title: "R. L. Graham, Bounds for certain multiprocessing anomalies, Bell System Technical Journal 45(9), 1966"
    locator: the bound 2 - 1/m for list schedules with precedence constraints and the examples that reach it (pp. 1563-1581 for the paper)
  - paper: doi:10.1137/0117039
    title: "R. L. Graham, Bounds on multiprocessing timing anomalies, SIAM Journal on Applied Mathematics 17(2), 1969"
    locator: the restatement of the bound 2 - 1/m and its comparison with the sorted list (pp. 416-429 for the paper)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 2.3 (the analysis of list scheduling, the lower bounds, and the precedence version)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 11.1 (the analysis of Greedy-Balance, statements (11.1) to (11.3))
---

Graham's bound states that every [list schedule](/list-scheduling/) on $m$ identical machines has makespan at most $2 - \frac1m$ times the optimum, for every order of the list, and also when the jobs have precedence constraints. Graham proved it in 1966, and it is one of the first worst-case analyses of an approximation algorithm. The proof compares the schedule with the two [lower bounds](/makespan-lower-bounds/) on the optimum: the average load and the longest job, or the longest chain under precedence constraints. The bound is tight for list scheduling: a long job at the end of the list reaches it.

## Statement

There are $n$ jobs with processing times $p_j \ge 0$ and $m \ge 1$ identical machines; $n$ is the number of jobs and $m$ the number of machines. A *list schedule* takes the jobs in a fixed order and, whenever a machine is free and a job is ready, starts the first ready job of the list on it. Without precedence constraints, every job is ready at time $0$, and the rule gives each job, in list order, to a machine with the smallest load. $\mathrm{OPT}$ is the optimal makespan, and $\mathrm{ALG}$ the makespan of the list schedule.

*Ratio convention.* This is a minimization problem, and a ratio $\rho \ge 1$ means $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance.

**Theorem (Graham 1966).**

1. For $P \mid\mid C_{\max}$ and any list, if job $l$ ends last, then
$$\mathrm{ALG} \le \frac1m \sum_j p_j + \Big(1 - \frac1m\Big) p_l \le \Big(2 - \frac1m\Big)\mathrm{OPT}.$$
2. For $P \mid \mathrm{prec} \mid C_{\max}$ and any list, $\mathrm{ALG} \le \frac1m \sum_j p_j + (1 - \frac1m) L \le (2 - \frac1m)\,\mathrm{OPT}$, where $L$ is the largest total time of a chain in the precedence graph.
3. For each $m$, there is an instance of $P \mid\mid C_{\max}$ with $\mathrm{ALG} = (2 - \frac1m)\,\mathrm{OPT}$.

The bound is absolute. It is tight for the algorithm by part 3. It is not tight for $P \mid\mid C_{\max}$, which has a [PTAS](/hochbaum-shmoys-ptas/). For $P \mid \mathrm{prec} \mid C_{\max}$, it is tight up to $\varepsilon$ under a variant of the unique games conjecture (Svensson 2010).

## In plain words

Look at the worker who ends last, and at the last task he got. When he got it, every other worker was at least as busy as he was, because the rule always picks the least busy worker. So up to that moment the whole team was working, and that moment is at most the total work shared equally. The task itself is no longer than the longest task. The best plan also needs at least the shared total, and at least the longest task, so the rule ends within twice the best.

With tasks that must wait for other tasks, a worker can stand still. But he only stands still when no task is ready, and that means some task of one long waiting line is still running. So the time when someone stands still is at most the length of that line, which the best plan also needs.

## Proof

**Part 1.** If all jobs have length $0$, both sides are $0$. Otherwise, let job $l$ end last and start at $S_l$, so $\mathrm{ALG} = S_l + p_l$. The rule put $l$ on a machine of smallest load, so at that moment all $m$ machines had load at least $S_l$. These loads come from jobs other than $l$, so $m S_l \le \sum_{j \ne l} p_j = \sum_j p_j - p_l$. Hence

$$\mathrm{ALG} = S_l + p_l \le \frac1m \sum_j p_j + \Big(1 - \frac1m\Big)p_l .$$

The [average load bound](/makespan-lower-bounds/) gives $\frac1m \sum_j p_j \le \mathrm{OPT}$, and the largest job bound gives $p_l \le \mathrm{OPT}$. Since $1 - \frac1m \ge 0$, $\mathrm{ALG} \le \mathrm{OPT} + (1 - \frac1m)\mathrm{OPT} = (2 - \frac1m)\mathrm{OPT}$.

**Part 2.** Let $C = \mathrm{ALG}$, and call a time $t \in [0, C)$ *idle* if at least one machine runs no job at $t$. Let $I$ be the total length of the idle times.

*Claim: there is a chain $j_1 \to j_2 \to \cdots \to j_k$ such that at every idle time, some job of the chain is running.* Build the chain backwards. Let $j_k$ be a job that ends last, so $C_{j_k} = C$. When $j_s$ is chosen, stop if it has no predecessor; otherwise let $j_{s-1}$ be a predecessor of $j_s$ with the largest completion time. Now take a time $t < S_{j_s}$ with $t \ge C_{j_{s-1}}$, or any $t < S_{j_s}$ if $j_s$ is the first job of the chain. At $t$, all predecessors of $j_s$ are done, so $j_s$ is ready and not yet started. The rule never leaves a machine free while a job is ready, so $t$ is not idle. The intervals $[0, S_{j_1})$, $[S_{j_1}, C_{j_1})$, $[C_{j_1}, S_{j_2})$, $\ldots$, $[S_{j_k}, C_{j_k})$ cover $[0, C)$, and the gaps between the jobs of the chain contain no idle time. So every idle time lies in some interval $[S_{j_s}, C_{j_s})$, when $j_s$ runs. This proves the claim.

At an idle time, at most $m - 1$ machines are idle, because one machine runs a job of the chain. The idle times have total length at most $\sum_{s} p_{j_s} \le L$. So the total idle machine time is at most $(m - 1) L$. The machines are busy for $\sum_j p_j$ in total, so

$$m C \le \sum_j p_j + (m - 1) L, \qquad C \le \frac1m \sum_j p_j + \Big(1 - \frac1m\Big) L .$$

Every schedule runs the jobs of a chain one after another, so $L \le \mathrm{OPT}$; this is the [critical path lower bound](/critical-path-lower-bound/). With $\frac1m \sum_j p_j \le \mathrm{OPT}$, we get $C \le (2 - \frac1m)\,\mathrm{OPT}$. Without precedence constraints, the longest chain is a single job, and part 2 is part 1 with $p_l$ replaced by $\max_j p_j$.

**Part 3.** Take $m(m - 1)$ jobs of length $1$, followed in the list by one job of length $m$. The rule spreads the unit jobs evenly, so each machine has load $m - 1$ when the long job comes. The long job starts at $m - 1$ and ends at $2m - 1$. The optimum is $m$: the long job alone on one machine, and $m$ unit jobs on each of the other $m - 1$ machines; it cannot be less than the long job. So $\mathrm{ALG}/\mathrm{OPT} = (2m - 1)/m = 2 - \frac1m$. $\blacksquare$

## Consequences

- **A 2-approximation and an online algorithm.** List scheduling has ratio $2 - \frac1m$ and needs no knowledge of later jobs, so it is $(2 - \frac1m)$-competitive for online makespan; see [the competitive ratio of list scheduling](/list-scheduling-competitive-ratio/).
- **An estimate of the optimum.** With $\mathrm{LB} = \max(\frac1m \sum_j p_j, \max_j p_j)$, part 1 gives $\mathrm{LB} \le \mathrm{OPT} \le (2 - \frac1m)\,\mathrm{LB}$. So the search interval $[\mathrm{LB}, 2\,\mathrm{LB}]$ of [dual approximation](/dual-approximation/) and of [MULTIFIT](/multifit-algorithm/) contains $\mathrm{OPT}$.
- **Two list schedules are close.** Any two list schedules of the same instance differ by a factor of at most $2 - \frac1m$. Graham (1966) also showed that a list schedule on $m'$ machines is at most $1 + \frac{m - 1}{m'}$ times a list schedule on $m$ machines; see [Graham's anomalies](/graham-anomalies/).
- **Small jobs.** Part 1 also gives $\mathrm{ALG} \le \mathrm{OPT} + (1 - \frac1m)\max_j p_j$. If every job is at most $\varepsilon \cdot \mathrm{OPT}$, the ratio is at most $1 + \varepsilon$. The [Hochbaum-Shmoys PTAS](/hochbaum-shmoys-ptas/) uses this for its small jobs.
- **Sorted lists.** If the last job is short, the bound is better. Sorting the list makes the last job short, which leads to [the LPT bound](/lpt-bound/) $\frac43 - \frac1{3m}$ and the $\frac32$ proof of [Sorted-Balance](/sorted-balance/).

## Tightness

- **For the algorithm.** Part 3 reaches $2 - \frac1m$ exactly for each $m$, without precedence constraints. So no better ratio holds for list scheduling in arbitrary order.
- **For the problem without precedence.** $P \mid\mid C_{\max}$ has a PTAS, so the bound is not a hardness threshold. A sorted list already gives $\frac43 - \frac1{3m}$.
- **For the problem with precedence.** $P \mid \mathrm{prec} \mid C_{\max}$ is NP-hard to approximate within $\frac43 - \varepsilon$, even with unit times, unless P = NP (Lenstra and Rinnooy Kan 1978). Svensson (2010) showed that a ratio $2 - \varepsilon$ is hard under a variant of the unique games conjecture. These results are cited, not proved here; see [precedence-constrained scheduling](/precedence-constrained-scheduling/).
- **Online.** For $m = 2$ and $m = 3$, no deterministic online algorithm beats $2 - \frac1m$ (Faigle, Kern and Turán 1989). For large $m$, better online algorithms exist; see [online makespan minimization](/online-makespan-minimization/).

## History

Graham (1966) studied multiprocessor systems in which a set of tasks with precedence constraints runs on identical processors under a priority list. He proved that any list schedule is within a factor $2 - \frac1m$ of the optimum, gave examples that reach the factor, and showed the anomalies of list scheduling. His 1969 paper restated the bound and added the sorted list. The result is now taught as the first example of an approximation ratio, for example in Kleinberg and Tardos as the analysis of Greedy-Balance.

## References
