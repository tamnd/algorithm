---
title: LPT is feasible and has makespan at most (4/3 - 1/(3m)) OPT
proves: [correctness]
status: full
---

We use the pseudocode of the page. Rename the jobs in the order $\pi$ of line L1, so that $p_1 \ge p_2 \ge \cdots \ge p_n \ge 0$, and let $m \ge 1$ be the number of machines. For a list $J$ of jobs, $\mathrm{LPT}(J)$ is the makespan of the algorithm and $\mathrm{OPT}(J)$ the optimal makespan. The proofs below are full.

**Lemma 1 (feasibility).** LPT returns an assignment of every job to one machine, and the machines run their jobs back to back with no overlap.

*Proof.* Lines L2 to L8 are [list scheduling](/list-scheduling/) on the list $1, \ldots, n$. Its heap invariant says that before round $k$ the heap holds each machine once with the total time of its jobs among $1, \ldots, k - 1$. So each job is assigned once, and it starts when the earlier jobs of its machine are done. $\square$

**Lemma 2 (prefix property).** For each $l$, the assignment of jobs $1, \ldots, l$ by LPT on the full list is the same as the assignment by LPT on the list $1, \ldots, l$ alone.

*Proof.* Round $k$ of lines L3 to L7 reads only the heap, which depends only on the rounds before it, and $p_k$. So the first $l$ rounds do not depend on the jobs after $l$. $\square$

**Lemma 3 (all jobs long).** Let $T > 0$. If $\mathrm{OPT}(J) \le T$ and every job of $J$ is longer than $T/3$, then $\mathrm{LPT}(J) \le T$.

*Proof.* By induction on the number $n$ of jobs. For $n = 0$ the claim is clear. Let $n \ge 1$. The list $1, \ldots, n - 1$ also has an optimum at most $T$ and only jobs longer than $T/3$, so by induction and Lemma 2, every machine has load at most $T$ after round $n - 1$. Let $t$ be the smallest of these loads. LPT puts job $n$ on a machine of load $t$, so it is enough to show $t + p_n \le T$. Suppose instead that $t + p_n > T$.

Each machine has load at most $T$ after round $n - 1$, and each job is longer than $T/3$, so each machine has at most $2$ jobs. If a machine had no job, then $t = 0$ and $t + p_n = p_n \le \mathrm{OPT}(J) \le T$, which is false. So each machine has $1$ or $2$ jobs. Let $a$ machines have one job and $b$ machines have two, so $a + b = m$ and $n - 1 = a + 2b$.

Let job $j$ be alone on its machine. Its load is $p_j \ge t > T - p_n$. Every other job $k$ has $p_k \ge p_n$, so $p_j + p_k > T$. Hence, in an optimal schedule of $J$ with makespan at most $T$, job $j$ shares its machine with no other job. These $a$ jobs use $a$ machines alone. The other $n - a = 2b + 1$ jobs must go on the remaining $m - a = b$ machines, and each of these machines holds at most $2$ jobs longer than $T/3$, so at most $2b$ jobs. This is a contradiction. So $t + p_n \le T$. $\square$

**Theorem.** $\mathrm{LPT}(J) \le \left(\frac43 - \frac1{3m}\right)\mathrm{OPT}(J)$ for every list $J$.

*Proof.* If all jobs have length $0$, both sides are $0$. Otherwise let $l$ be a job that ends last in the LPT schedule of $J$, and let $J' = (1, \ldots, l)$. By Lemma 2, LPT on $J'$ builds the same schedule for these jobs, so job $l$ ends last there too and $\mathrm{LPT}(J') = \mathrm{LPT}(J)$. Also $\mathrm{OPT}(J') \le \mathrm{OPT}(J)$, since removing jobs cannot make the optimum larger. So it is enough to prove the bound for $J'$, in which job $l$ is the shortest job and ends last. Write $T = \mathrm{OPT}(J')$.

Job $l$ starts at the smallest load $t$ after round $l - 1$. The smallest of $m$ loads is at most their mean, so $t \le \frac1m \sum_{k < l} p_k$, and

$$\mathrm{LPT}(J') = t + p_l \le \frac1m \sum_{k \le l} p_k + \Big(1 - \frac1m\Big) p_l \le T + \Big(1 - \frac1m\Big) p_l ,$$

where the last step is the [average load bound](/makespan-lower-bounds/).

*Case $p_l \le T/3$.* Then $\mathrm{LPT}(J') \le T + (1 - \frac1m)\frac{T}{3} = (\frac43 - \frac1{3m})\,T$.

*Case $p_l > T/3$.* Every job of $J'$ is at least $p_l$, so every job is longer than $T/3$. By Lemma 3, $\mathrm{LPT}(J') \le T$, which is at most $(\frac43 - \frac1{3m})\,T$.

In both cases $\mathrm{LPT}(J) = \mathrm{LPT}(J') \le (\frac43 - \frac1{3m})\,\mathrm{OPT}(J') \le (\frac43 - \frac1{3m})\,\mathrm{OPT}(J)$. $\blacksquare$

**Optimal cases.** If $n \le m$, each job gets its own machine, and the makespan is $\max_j p_j \le \mathrm{OPT}$. If every job is longer than $\mathrm{OPT}/3$, Lemma 3 with $T = \mathrm{OPT}$ shows that LPT is optimal.

**Tightness.** The family with two jobs each of length $2m - 1, 2m - 2, \ldots, m + 1$ and three jobs of length $m$ has $\mathrm{OPT} = 3m$ and $\mathrm{LPT} = 4m - 1$, so the ratio $\frac43 - \frac1{3m}$ is reached for each $m$. The proof is on [the LPT bound](/lpt-bound/).
