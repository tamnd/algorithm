---
title: The wrap-around rule gives a feasible preemptive schedule of optimal makespan
proves: [correctness]
status: full
---

We use the pseudocode of the page. There are $n$ jobs with times $p_j \ge 0$ and $m \ge 1$ identical machines, and $C^* = \max(\frac1m \sum_j p_j, \max_j p_j)$ is the value of line L1. Let $P = \sum_j p_j$. If $C^* = 0$, all jobs have length $0$, no piece is made, and the empty schedule is optimal; so let $C^* > 0$. All proofs below are full.

**Lemma 1 (lower bound).** Every preemptive schedule has makespan at least $C^*$.

*Proof.* Let the makespan be $C$. The machines give at most $mC$ units of processing time in $[0, C)$, and the jobs need $P$, so $C \ge P/m$. A job runs on at most one machine at a time, so job $j$ needs at least $p_j$ units of wall time in $[0, C)$, and $C \ge p_j$. $\square$

**Lemma 2 (filling order).** Write the position of the rule as the number $F = (i - 1)C^* + t$, the total time placed so far. Then each piece made at line L7 is the interval of positions $[F, F + d)$ for the current $F$, line L8 adds $d$ to $F$, and line L9 does not change $F$. So the pieces of all jobs, in order, cover the positions $[0, P)$ without gaps or overlaps, with job $j$ on $[P_{j-1}, P_j)$, where $P_j = p_1 + \cdots + p_j$.

*Proof.* At line L7, the piece is $[t, t + d)$ on machine $i$, that is the positions $[F, F + d)$. Line L8 sets $t \leftarrow t + d$, so $F$ grows by $d$. Line L9 replaces $(i, t)$ by $(i + 1, 0)$ only when $t = C^*$, and $(i - 1)C^* + C^* = iC^* + 0$. Line L6 takes $d \le C^* - t$, so a piece never passes the end of a machine. The inner loop for job $j$ ends when $r = 0$, so it places exactly $p_j$ units. $\square$

**Lemma 3 (machines used).** Every piece lies on a machine $i \le m$ and in the time interval $[0, C^*]$.

*Proof.* By Lemma 2, the last position used is $P \le mC^*$. A piece at positions $[F, F + d)$ with $F < P \le mC^*$ lies on machine $i = \lfloor F / C^* \rfloor + 1 \le m$, and line L6 keeps it inside $[0, C^*]$. $\square$

**Lemma 4 (each job is on one machine at a time).** Each job has at most two pieces. If job $j$ has two pieces, they are $[t, C^*)$ on machine $i$ and $[0, d_2)$ on machine $i + 1$ with $d_2 \le t$, so they do not overlap in time.

*Proof.* Job $j$ covers the positions $[P_{j-1}, P_j)$, an interval of length $p_j \le C^*$. An interval of length at most $C^*$ contains at most one multiple of $C^*$ in its interior, so it meets at most two machines, and job $j$ has at most two pieces. If it has two, the first is $[t, C^*)$ on machine $i$, with $t = P_{j-1} - (i - 1)C^*$, and the second is $[0, d_2)$ on machine $i + 1$ with $d_2 = p_j - (C^* - t)$. Since $p_j \le C^*$, $d_2 \le t$. The half-open intervals $[0, d_2)$ and $[t, C^*)$ are disjoint. $\square$

**Theorem.** The pieces form a feasible preemptive schedule with makespan $C^*$, and this is optimal. At most $m - 1$ jobs are split.

*Proof.* By Lemma 2, two pieces never share a position, so on one machine they never overlap in time, and each job gets exactly $p_j$ units. By Lemma 4, no job runs on two machines at once. By Lemma 3, all pieces lie in $[0, C^*]$ on machines $1, \ldots, m$, so the makespan is at most $C^*$, and by Lemma 1 it is exactly $C^*$ and optimal. A job is split only at a boundary between machine $i$ and $i + 1$, there are $m - 1$ such boundaries inside $[0, mC^*)$, and by Lemma 4 each split job uses only one of them. $\blacksquare$

**Corollary (the nonpreemptive gap).** If $C^* > 0$, the nonpreemptive optimum of the same instance is less than $2C^*$.

*Proof.* For each split job, delete its second piece and put the job whole on its first machine $i$. The first piece $[t, C^*)$ has positive length, so the second piece is shorter than $p_j \le C^*$, and machine $i$ gets an extra load less than $C^*$. Each machine $i$ is the first machine of at most one split job, the one that crosses its end. So every machine has load less than $C^* + C^* = 2C^*$, and running each machine's jobs back to back gives a nonpreemptive schedule of makespan less than $2C^*$. $\blacksquare$
