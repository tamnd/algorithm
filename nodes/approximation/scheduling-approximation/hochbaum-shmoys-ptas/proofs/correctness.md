---
title: The Hochbaum-Shmoys scheme is a (1 + 1/k)-approximation
proves: [correctness]
status: full
---

We use the notation of the page. The times $p_1, \ldots, p_n$ are positive integers, there are $m$ identical machines, $k \ge 1$ is an integer, $P = \sum_j p_j$ and $\mathrm{LB} = \max(\max_j p_j, \lceil P/m \rceil)$. For a guess $T$, a job is long if $p_j > T/k$, its rounded size is $r_j = \lfloor p_j k^2/T \rfloor$, and a configuration is a nonzero vector of counts of rounded sizes whose total size is at most $k^2$. $\mathrm{OPT}$ is the least makespan.

**Lemma 1 (rounded sizes).** If $T/k < p_j \le T$, then $k \le r_j \le k^2$ and $r_j T/k^2 \le p_j < (r_j + 1) T/k^2$.

*Proof.* From $p_j k^2/T > k$ and $p_j k^2/T \le k^2$, the floor $r_j$ lies between $k$ and $k^2$, because $k$ and $k^2$ are integers. The two inequalities are the definition of the floor, $r_j \le p_j k^2/T < r_j + 1$, multiplied by $T/k^2$. $\square$

**Lemma 2 (a configuration is short).** A configuration holds at most $k$ jobs, and the long jobs that it stands for have total time less than $T + T/k$.

*Proof.* Each rounded size is at least $k$ by Lemma 1, and the sizes add up to at most $k^2$, so there are at most $k$ jobs. By Lemma 1 the total time is less than $\sum (r_j + 1) T/k^2 \le (k^2 + k) T/k^2 = T + T/k$, where the sum runs over the jobs of the configuration. $\square$

**Lemma 3 (the dynamic program).** The value $f(\mathbf{a})$ of line L8 is the least number of machines that hold all long jobs when each machine holds a configuration.

*Proof.* By induction on the number of long jobs. For no jobs, $f(\mathbf{0}) = 0$. Otherwise, in a best packing, some machine holds a configuration $\mathbf{c} \le \mathbf{a}$, and the other machines pack $\mathbf{a} - \mathbf{c}$, so they are at least $f(\mathbf{a} - \mathbf{c})$ by induction, and the packing uses at least $1 + f(\mathbf{a} - \mathbf{c}) \ge f(\mathbf{a})$ machines. Conversely, the choice of $\mathbf{c}$ that gives the minimum, followed by a best packing of $\mathbf{a} - \mathbf{c}$, uses exactly $f(\mathbf{a})$ machines. Jobs of the same rounded size are exchangeable for the count vector, so line L10 can place real jobs for each count. $\square$

**Lemma 4 (a failure is a proof).** If $\mathrm{DUAL}(p, m, k, T)$ returns FAIL, then $\mathrm{OPT} > T$.

*Proof.* We show the contrapositive: assume $\mathrm{OPT} \le T$ and fix an optimal schedule.

- Line L6. Each job lies on a machine with load at most $T$, so $p_j \le T$ for all $j$.
- Line L9. Look at one machine of the optimal schedule and its long jobs. By Lemma 1, $\sum r_j \le \sum p_j k^2/T \le k^2$, because the machine has load at most $T$. So the long jobs of each machine form a configuration, or none at all. Machines with no long jobs can be dropped, so the long jobs fit in at most $m$ configurations, and by Lemma 3, $M \le m$.
- Line L13. Suppose that a short job $j$ finds every machine with load above $T$. Then the jobs already placed have total time above $mT$, so $P > mT$ and $\mathrm{OPT} \ge P/m > T$, which is a contradiction.

So no line returns FAIL. $\square$

**Lemma 5 (a success is good).** If $\mathrm{DUAL}(p, m, k, T)$ returns a schedule, its makespan is at most $(1 + 1/k) T$.

*Proof.* After line L10, each machine holds the long jobs of at most one configuration, so its load is less than $T + T/k$ by Lemma 2. Then each short job is placed on a machine $i$ with $\mathrm{load}(i) \le T$, by line L13, and has $p_j \le T/k$, so after the step the load of $i$ is at most $T + T/k$. Loads of other machines do not change. By induction over the short jobs, every load stays at most $T + T/k$. $\square$

**Lemma 6 (the search).** At line L5, $hi \le \mathrm{OPT}$ and $\mathrm{DUAL}(p, m, k, hi)$ does not fail.

*Proof.* List scheduling places each job on a machine of least load, which is at most $P/m$ at that moment, so its makespan is at most $P/m + \max_j p_j \le 2\,\mathrm{LB}$. So $\mathrm{OPT} \le 2\,\mathrm{LB}$, and by Lemma 4 the test at $2\,\mathrm{LB}$ does not fail. Also $\mathrm{LB} \le \mathrm{OPT}$, since the longest job lies on one machine, the average load is $P/m$, and $\mathrm{OPT}$ is an integer.

The loop keeps two facts: the test does not fail at $hi$, and either $lo = \mathrm{LB}$ or the test failed at $lo - 1$. Both hold at line L1. In line L4, if the test succeeds at $mid$, the new $hi = mid$ keeps the first fact; otherwise the new $lo = mid + 1$ keeps the second. Since $lo \le mid < hi$, the interval gets shorter, so the loop ends with $lo = hi$. If $lo = \mathrm{LB}$, then $hi = \mathrm{LB} \le \mathrm{OPT}$. Otherwise the test failed at $lo - 1$, so $\mathrm{OPT} > lo - 1$ by Lemma 4, and as $\mathrm{OPT}$ is an integer, $\mathrm{OPT} \ge lo = hi$. $\square$

**Theorem.** For every integer $k \ge 1$, $\mathrm{HS\text{-}PTAS}(p, m, k)$ returns a schedule with makespan at most $(1 + 1/k)\,\mathrm{OPT}$.

*Proof.* By Lemma 6, line L5 returns a schedule at some $T = hi \le \mathrm{OPT}$. By Lemma 5 its makespan is at most $(1 + 1/k) T \le (1 + 1/k)\,\mathrm{OPT}$. $\blacksquare$

**Running time.** The rounded sizes lie in $\{k, \ldots, k^2\}$, so a count vector has $d = k^2 - k + 1$ entries, each between 0 and $n$. There are at most $(n + 1)^d$ count vectors and at most $(k + 1)^d$ configurations, since each count in a configuration is at most $k$. Each value $f(\mathbf{a})$ looks at all configurations, with $O(d)$ work for each, so the test takes $O((n + 1)^d (k + 1)^d d + nm)$ time, which is polynomial in $n$ and $m$ for fixed $k$. The search calls it $O(\log \mathrm{LB})$ times, which is polynomial in the input length.
