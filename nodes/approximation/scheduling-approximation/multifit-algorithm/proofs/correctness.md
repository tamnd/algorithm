---
title: MULTIFIT is feasible and has makespan at most (r + 2^-k) OPT
proves: [correctness]
status: full
---

We use the pseudocode of the page. There are $n$ jobs with times $p_j \ge 0$ and $m \ge 1$ machines. $A = \frac1m \sum_j p_j$, $\mathrm{OPT}$ is the optimal makespan, and $\mathrm{FFD}(J, C)$ is the call of lines L8 to L11 on the jobs $J$ with capacity $C$. We say that a capacity $C$ *succeeds* if this call does not fail. All proofs below are full. The constants $1.22$ and $\frac{13}{11}$ are only cited, on [the MULTIFIT bound](/multifit-bound/).

**Lemma 1 (a success is a schedule).** If $C$ succeeds, the call returns at most $m$ bins, each job is in exactly one bin, and each bin has load at most $C$.

*Proof.* Line L10 adds a job to a bin only if the new load is at most $C$. Line L11 opens a bin only for a job with $p_j \le C$ and only while fewer than $m$ bins are open. Each job is placed once. $\square$

So line L7 returns a schedule on at most $m$ machines with makespan at most $\mathrm{hi}$, provided that $\mathrm{hi}$ succeeds.

**Lemma 2 (prefix property).** Let the jobs be sorted as in line L8. For each $l$, the bins of $\mathrm{FFD}(J, C)$ restricted to jobs $1, \ldots, l$ are the bins of $\mathrm{FFD}((1, \ldots, l), C)$, and the call on $J$ fails at job $l$ if and only if the call on $(1, \ldots, l)$ fails at job $l$.

*Proof.* The rounds of lines L9 to L11 for jobs $1, \ldots, l$ read only the bins built so far and the sizes of these jobs. $\square$

**Lemma 3 (the upper end succeeds).** Every capacity $C \ge \max(2A, \max_j p_j)$ succeeds.

*Proof.* Suppose the call fails at job $x$. Since $p_x \le C$, it fails because $m$ bins are open and $x$ fits in none, so each bin has load $\ell_b > C - p_x$. At most one bin has load at most $C/2$. Indeed, if bins $b < b'$ both had load at most $C/2$, then the first job of $b'$ has size at most $C/2$, and when it came, bin $b$ already existed with load at most $C/2$, since loads only grow. So it fits into $b$, and line L10 would have chosen $b$ or an earlier bin. Let $b$ be the bin with the smallest load. The other $m - 1$ bins have load more than $C/2$, and $\ell_b + p_x > C$. All these jobs are distinct, so

$$\sum_j p_j \ge \sum_{b'} \ell_{b'} + p_x > (m - 1)\frac{C}{2} + C \ge \frac{mC}{2} \ge mA = \sum_j p_j ,$$

which is a contradiction. $\square$

**Lemma 4 (a capacity that always succeeds).** Let $r_0 = \frac43 - \frac1{3m}$. Every capacity $C \ge r_0 \cdot \mathrm{OPT}$ succeeds.

*Proof.* Suppose the call fails at job $x$, with the jobs sorted. By Lemma 2, the call on $J' = (1, \ldots, x)$ also fails at $x$, and $x$ is a shortest job of $J'$. Let $T = \mathrm{OPT}(J') \le \mathrm{OPT}$. Since $p_x \le T \le C$, the failure means that $m$ bins hold the jobs $1, \ldots, x - 1$ and each has load $\ell_b > C - p_x$.

*Case $p_x \le T/3$.* Adding the loads, $\sum_{j \in J'} p_j - p_x > m(C - p_x)$, so

$$C < \frac1m \sum_{j \in J'} p_j + \Big(1 - \frac1m\Big)p_x \le T + \Big(1 - \frac1m\Big)\frac{T}{3} = r_0\, T \le r_0 \cdot \mathrm{OPT},$$

by the [average load bound](/makespan-lower-bounds/) for $J'$. This contradicts $C \ge r_0 \cdot \mathrm{OPT}$.

*Case $p_x > T/3$.* Every job of $J'$ is at least $p_x$, so longer than $T/3$. In an optimal schedule of $J'$, each machine has at most $2$ jobs. Let $a$ of the $m$ bins hold exactly one job, so $m - a$ bins hold at least two. If bin $b$ holds only job $y$, then $p_y = \ell_b > C - p_x \ge T - p_x$, and $p_y + p_z \ge p_y + p_x > T$ for every other job $z$ of $J'$. So in the optimal schedule, $y$ is alone on its machine. These $a$ jobs fill $a$ machines, and the other $|J'| - a$ jobs are on $m - a$ machines with at most $2$ each, so $|J'| - a \le 2(m - a)$. But the bins hold $|J'| - 1 \ge a + 2(m - a)$ jobs, so $|J'| - a \ge 2(m - a) + 1$. This is a contradiction. $\square$

**Theorem.** Let $r \ge 1$ be a constant such that every capacity $C \ge r \cdot \mathrm{OPT}$ succeeds. Then MULTIFIT with $k$ steps returns a schedule with makespan at most $(r + 2^{-k})\,\mathrm{OPT}$. By Lemma 4, this holds with $r = \frac43 - \frac1{3m}$.

*Proof.* If $n = 0$ there is nothing to show. Write $\mathrm{lo}_0, \mathrm{hi}_0$ for the values of line L2. We show that after each step of lines L3 to L6:

1. $\mathrm{hi}$ succeeds;
2. $\mathrm{lo} \le r \cdot \mathrm{OPT}$;
3. $\mathrm{hi} - \mathrm{lo}$ is half of its value before the step.

At the start, (1) is Lemma 3, and (2) holds because $\mathrm{lo}_0 = \max(A, \max_j p_j) \le \mathrm{OPT}$ by the [lower bounds](/makespan-lower-bounds/) and $r \ge 1$. In a step, line L4 takes the midpoint $C$. If $C$ succeeds, line L5 sets $\mathrm{hi} = C$, which keeps (1), and $\mathrm{lo}$ does not change. If $C$ fails, then $C < r \cdot \mathrm{OPT}$ by the choice of $r$, and line L6 sets $\mathrm{lo} = C$, which keeps (2). In both cases the interval is halved, which is (3).

The first interval is short. If $\max_j p_j \ge 2A$, then $\mathrm{hi}_0 = \mathrm{lo}_0$. If $A \le \max_j p_j < 2A$, then $\mathrm{hi}_0 - \mathrm{lo}_0 = 2A - \max_j p_j \le A$. If $\max_j p_j < A$, then $\mathrm{hi}_0 - \mathrm{lo}_0 = A$. So $\mathrm{hi}_0 - \mathrm{lo}_0 \le A \le \mathrm{OPT}$.

After $k$ steps, by (3) and (2), $\mathrm{hi} \le \mathrm{lo} + 2^{-k} A \le r \cdot \mathrm{OPT} + 2^{-k}\mathrm{OPT}$. By (1) and Lemma 1, line L7 returns a schedule on at most $m$ machines with makespan at most $\mathrm{hi}$. $\blacksquare$

**Remarks.** The proof does not assume that success is monotone in $C$, and it is not: the page gives an instance that succeeds at $60$ and fails at $61$. The theorem only needs the threshold $r$. Coffman, Garey and Johnson proved that $r = 1.22$ is a valid threshold, Yue proved $r = \frac{13}{11}$, and Friesen's example shows that no $r < \frac{13}{11}$ is valid for all $m$; see [the MULTIFIT bound](/multifit-bound/).
