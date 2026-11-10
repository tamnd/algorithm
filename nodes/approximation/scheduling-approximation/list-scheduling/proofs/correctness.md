---
title: List scheduling is feasible and has makespan at most (2 - 1/m) OPT
proves: [correctness]
status: full
---

We use the pseudocode of the page. There are $n$ jobs with times $p_1, \ldots, p_n \ge 0$, in the order of the list, and $m \ge 1$ identical machines. For a machine $i$ and a step $j$, let $L_i^{(j)}$ be the total time of the jobs among $1, \ldots, j$ that line L4 puts on $i$. The proofs below are full.

**Lemma 1 (heap invariant).** Before the round of line L2 for job $j$, the heap $H$ holds exactly one pair for each machine $i$, and that pair is $(L_i^{(j-1)}, i)$.

*Proof.* By induction on $j$. For $j = 1$, line L1 puts $(0, i)$ for each $i$, and $L_i^{(0)} = 0$. Suppose the claim holds before job $j$. Line L3 removes one pair $(t, i)$ with $t = L_i^{(j-1)}$. Line L4 puts job $j$ on $i$, so $L_i^{(j)} = t + p_j$ and the other loads do not change. Line L5 inserts $(t + p_j, i)$. So after the round, $H$ holds one pair per machine with the loads $L^{(j)}$. $\square$

**Lemma 2 (feasibility).** Line L6 returns a schedule in which every job runs once, every machine runs one job at a time, and no machine is idle before its last job ends. Its makespan is $\max_i L_i^{(n)}$.

*Proof.* Line L4 assigns each job exactly once. By Lemma 1, job $j$ starts at $S_j = L_{\sigma(j)}^{(j-1)}$, the total time of the earlier jobs on the same machine. So the jobs on one machine run back to back in list order: each starts when the one before it ends. Hence there is no overlap and no idle time, and the last job on $i$ ends at $L_i^{(n)}$. By Lemma 1 after the last round, the largest load in $H$ is $\max_i L_i^{(n)}$, which is the makespan. If $n = 0$, all loads are $0$ and so is the makespan. $\square$

**Lemma 3 (the start of a job).** For each job $j$, $S_j \le \frac1m \sum_{k < j} p_k$.

*Proof.* Line L3 takes the smallest load, so $S_j = \min_i L_i^{(j-1)}$. The smallest of $m$ numbers is at most their mean, and the loads $L_i^{(j-1)}$ add up to $\sum_{k < j} p_k$. $\square$

**Theorem.** Let $\mathrm{ALG}$ be the makespan of list scheduling for any list order, and $\mathrm{OPT}$ the optimal makespan. Then $\mathrm{ALG} \le (2 - \frac1m)\,\mathrm{OPT}$.

*Proof.* If $n = 0$, both sides are $0$. Otherwise let $l$ be a job that ends last, so $\mathrm{ALG} = S_l + p_l$. By Lemma 3,

$$S_l \le \frac1m \sum_{k < l} p_k \le \frac1m \Big( \sum_{k=1}^{n} p_k - p_l \Big).$$

So

$$\mathrm{ALG} = S_l + p_l \le \frac1m \sum_{k=1}^{n} p_k + \Big(1 - \frac1m\Big) p_l .$$

By the [average load bound](/makespan-lower-bounds/), $\frac1m \sum_k p_k \le \mathrm{OPT}$, and by the largest job bound, $p_l \le \max_k p_k \le \mathrm{OPT}$. Since $1 - \frac1m \ge 0$,

$$\mathrm{ALG} \le \mathrm{OPT} + \Big(1 - \frac1m\Big)\mathrm{OPT} = \Big(2 - \frac1m\Big)\mathrm{OPT}. \qquad \blacksquare$$

**Tightness.** Take $m(m - 1)$ jobs of length $1$ followed by one job of length $m$. The unit jobs fill all machines evenly to load $m - 1$, so the long job starts at $m - 1$ and ends at $2m - 1$. The optimum is $m$: put the long job alone on one machine and $m$ unit jobs on each of the others. The ratio is $(2m - 1)/m = 2 - \frac1m$.
