---
tag: WA0R57
kind: theorem
slug: lpt-bound
name: LPT approximation bound
aliases:
- (4/3-1/(3m))-approximation theorem
- Graham's LPT bound
area: approximation/scheduling-approximation
level: core
summary: LPT is within a factor 4/3-1/(3m) of the optimal makespan.
prereqs: [longest-processing-time-first, list-scheduling-bound]
see_also: [longest-processing-time-first, list-scheduling-bound, sorted-balance, multifit-bound, machine-covering, makespan-lower-bounds, hochbaum-shmoys-ptas, makespan-minimization]
sources:
  - paper: doi:10.1137/0117039
    title: "R. L. Graham, Bounds on multiprocessing timing anomalies, SIAM Journal on Applied Mathematics 17(2), 1969"
    locator: the theorem that the decreasing list gives at most 4/3 - 1/(3m) times the optimum, and the example that reaches it (pp. 416-429 for the paper)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 2.3 (the longest processing time rule, the 4/3 analysis with the case of jobs longer than OPT/3)
  - book: isbn:9780534949686
    title: Dorit S. Hochbaum (editor), Approximation Algorithms for NP-Hard Problems
    locator: Chapter 1, L. A. Hall, Approximation algorithms for scheduling (the LPT bound)
---

The LPT bound states that [longest processing time first](/longest-processing-time-first/) on $m$ identical machines always has makespan at most $\frac43 - \frac1{3m}$ times the optimum. Graham proved it in 1969, together with a family of instances that reaches the bound exactly for each $m$. The proof splits on the length of the job that ends last: a short last job is handled by the [average load bound](/makespan-lower-bounds/), and when all jobs are longer than a third of the optimum, LPT is optimal.

## Statement

There are $n$ jobs with processing times $p_j \ge 0$ and $m \ge 1$ identical machines; $n$ is the number of jobs and $m$ the number of machines. LPT sorts the jobs so that $p_1 \ge p_2 \ge \cdots \ge p_n$ and gives each job, in this order, to a machine with the smallest current load. $\mathrm{OPT}$ is the optimal makespan and $\mathrm{LPT}$ the makespan of the algorithm.

*Ratio convention.* This is a minimization problem, and a ratio $\rho \ge 1$ means $\mathrm{LPT} \le \rho \cdot \mathrm{OPT}$ on every instance.

**Theorem (Graham 1969).**

1. For every instance of $P \mid\mid C_{\max}$, $\mathrm{LPT} \le \left(\frac43 - \frac1{3m}\right)\mathrm{OPT}$.
2. If every job is longer than $\mathrm{OPT}/3$, then $\mathrm{LPT} = \mathrm{OPT}$.
3. For each $m \ge 1$, the instance with two jobs each of length $2m - 1, 2m - 2, \ldots, m + 1$ and three jobs of length $m$ has $\mathrm{OPT} = 3m$ and $\mathrm{LPT} = 4m - 1$.

The bound is absolute. By part 3, it is tight for the algorithm for each $m$. It is not tight for the problem, which has a [PTAS](/hochbaum-shmoys-ptas/). The proof compares with the average load bound $\mathrm{OPT} \ge \frac1m \sum_j p_j$ and with a counting argument in the spirit of the pigeonhole [lower bounds](/makespan-lower-bounds/).

## In plain words

Look at the task that ends last. If it is short, at most a third of the best finish time, then the usual argument for the greedy rule gives a finish time at most the shared total plus that short task, and so at most one third more than the best.

If it is long, then, because the tasks were sorted, every task is longer than a third of the best finish time. Then no worker can do three of them in the best plan, so the best plan gives each worker one or two tasks. On such inputs the sorted greedy rule pairs the tasks as well as the best plan does, and it is exactly optimal.

## Proof

Rename the jobs so that $p_1 \ge \cdots \ge p_n$ is the LPT order. For a list $J$, write $\mathrm{LPT}(J)$ and $\mathrm{OPT}(J)$.

**Prefix property.** The assignment of jobs $1, \ldots, l$ is the same for the list $J$ and for its prefix $(1, \ldots, l)$, because each step of LPT depends only on the earlier steps and the current job.

**Part 2, as a lemma.** Let $T > 0$. *If $\mathrm{OPT}(J) \le T$ and every job of $J$ is longer than $T/3$, then $\mathrm{LPT}(J) \le T$.* We use induction on $n$; for $n = 0$ the claim is clear. For $n \ge 1$, the prefix $(1, \ldots, n - 1)$ satisfies the same conditions, so by induction and the prefix property, all loads are at most $T$ before job $n$. Let $t$ be the smallest load then; LPT puts job $n$ on a machine of load $t$. Suppose that $t + p_n > T$.

Each machine has load at most $T$ and only jobs longer than $T/3$, so at most $2$ jobs. An empty machine would give $t = 0$ and $t + p_n = p_n \le T$, so each machine has $1$ or $2$ jobs. Let $a$ machines have one job and $b$ have two, so $a + b = m$ and $n - 1 = a + 2b$. If job $j$ is alone, then $p_j \ge t > T - p_n$, and for every other job $k$, $p_j + p_k \ge p_j + p_n > T$. So in an optimal schedule, each of these $a$ jobs is alone on its machine. The other $2b + 1$ jobs are then on $b$ machines with at most $2$ jobs each, which is impossible. So $t + p_n \le T$, and $\mathrm{LPT}(J) \le T$.

With $T = \mathrm{OPT}(J)$, this proves part 2.

**Part 1.** If all jobs have length $0$, both sides are $0$. Otherwise let $l$ be a job that ends last, and $J' = (1, \ldots, l)$. By the prefix property, $\mathrm{LPT}(J') = \mathrm{LPT}(J)$, and $\mathrm{OPT}(J') \le \mathrm{OPT}(J)$. In $J'$, job $l$ is a shortest job. Let $T = \mathrm{OPT}(J')$ and let $t$ be the start of job $l$, the smallest load before it. Then $t \le \frac1m \sum_{k < l} p_k$, so

$$\mathrm{LPT}(J') = t + p_l \le \frac1m \sum_{k \le l} p_k + \Big(1 - \frac1m\Big) p_l \le T + \Big(1 - \frac1m\Big) p_l .$$

If $p_l \le T/3$, this is at most $(\frac43 - \frac1{3m})\,T$. If $p_l > T/3$, every job of $J'$ is longer than $T/3$, and the lemma gives $\mathrm{LPT}(J') \le T$. In both cases $\mathrm{LPT}(J) \le (\frac43 - \frac1{3m})\,\mathrm{OPT}(J') \le (\frac43 - \frac1{3m})\,\mathrm{OPT}(J)$.

**Part 3.** The big jobs are $s_k = 2m - \lceil k/2 \rceil$ for $k = 1, \ldots, 2m - 2$, and they are followed by three jobs of length $m$. The total is $2 \sum_{x = m+1}^{2m-1} x + 3m = 3m(m - 1) + 3m = 3m^2$.

*The optimum is $3m$.* It is at least $3m^2 / m = 3m$. The big jobs, as a multiset, are symmetric under $x \mapsto 3m - x$, so they split into $m - 1$ pairs of sum $3m$. These pairs and the triple $\{m, m, m\}$ fill $m$ machines to exactly $3m$.

*LPT gives $4m - 1$.* The first $m$ jobs go one to each machine, with loads $s_1 \ge \cdots \ge s_m$. For $k$ from $m$ down to $3$, the next job $2m + 1 - k$ goes to a machine of load $s_k$, the smallest load among the machines that still have one job; if two such machines have the same load, either choice gives the same loads. Call it machine $k$. Its new load is

$$s_k + s_{2m+1-k} = 3m - 1,$$

which is checked separately for even $k = 2a$, where the terms are $2m - a$ and $m + a - 1$, and for odd $k = 2a - 1$, where they are $2m - a$ and $m + a - 1$ too. This load exceeds the loads $2m - 1$ of machines 1 and 2, so the next job again goes to a machine with one job. After the $2m - 2$ big jobs, machines 1 and 2 have load $2m - 1$ and the others $3m - 1$. The first two jobs of length $m$ bring machines 1 and 2 to $3m - 1$, and the third goes on a machine of load $3m - 1$ and ends at $4m - 1$.

So $\mathrm{LPT}/\mathrm{OPT} = \frac{4m - 1}{3m} = \frac43 - \frac1{3m}$. For $m = 1$ there are no big jobs, and both values are $3$. $\blacksquare$

## Consequences

- **LPT is a $\frac43$-approximation** for $P \mid\mid C_{\max}$ that costs only a sort and a heap.
- **Two machines.** For $m = 2$ the bound is $\frac76$, reached by $(3, 3, 2, 2, 2)$, where LPT gives $7$ and the optimum is $6$.
- **The $\frac32$ proof is weaker.** The short proof of [Sorted-Balance](/sorted-balance/), which uses $\mathrm{OPT} \ge 2 p_{m+1}$, gives only $\frac32 - \frac1{2m}$ for the same algorithm.
- **Many jobs per machine.** If the machine that ends last has $k \ge 3$ jobs, Coffman and Sethi (1976) showed that the ratio is at most $\frac{k+1}{k} - \frac1{km}$ (cited, not proved here). So LPT is close to optimal when there are many jobs per machine.
- **Machine covering.** The same schedule has smallest load at least $\frac34$ of the best smallest load; see [machine covering](/machine-covering/).

## Tightness

- **For the algorithm.** Part 3 reaches $\frac43 - \frac1{3m}$ exactly for each $m$, so no smaller constant holds for LPT.
- **For the problem.** The problem has a [PTAS](/hochbaum-shmoys-ptas/), so $\frac43$ is not a hardness threshold. [MULTIFIT](/multifit-algorithm/) gets $\frac{13}{11} + 2^{-k}$ with the same sort; see [the MULTIFIT bound](/multifit-bound/).
- **Where the analysis is tight.** In the tight family, the last job is exactly $\mathrm{OPT}/3$, at the border of the two cases of the proof.

## History

Graham (1966) proved $2 - \frac1m$ for arbitrary lists. In 1969 he proved that the decreasing list gives $\frac43 - \frac1{3m}$, with the family of part 3. Coffman and Sethi (1976) refined the bound by the number of jobs on the critical machine. The proof with the case split at $\mathrm{OPT}/3$ is the one in textbooks such as Williamson and Shmoys.

## References
