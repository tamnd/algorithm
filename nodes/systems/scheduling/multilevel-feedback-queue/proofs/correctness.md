---
title: The MLFQ simulation meets Rules 1 to 5, the accounting rule bounds the time above each level, and the boost bounds the wait
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page, with $k \ge 1$ queues, quanta $q_i \ge 1$, allotments $A_i \ge q_i$ and boost period $S$ ($S = 0$ means no boost). A job is *ready* at tick $t$ if it has arrived, is not finished, and is not in an I/O wait. Tick $t$ is the pass of the loop of line L2 that starts with this value of $t$.

**Claim 1 (queues hold the ready jobs).** After line L5 of each tick, each ready job $j$ is in exactly one queue, the queue $Q[\mathit{lvl}_j]$, and no other job is in a queue.

*Proof.* By induction on the ticks. Before tick 0 no job has arrived and the queues are empty. Line L3 moves all queued jobs to $Q[0]$ and sets every level to 0, so the claim holds after it. Line L4 appends a job whose I/O ends, which becomes ready, to $Q[\mathit{lvl}_j]$. Line L5 appends a new job to $Q[0]$, and its level is 0. In lines L8 to L11, the job $j$ that ran either leaves $Q[i]$ because it finishes or blocks (line L10), and so stops being ready, or it moves from $Q[i]$ to $Q[\mathit{lvl}_j]$ when its level changed (line L11), or it stays in $Q[i]$ with $\mathit{lvl}_j = i$. No other job changes queue or level. $\square$

**Rule 1.** By Claim 1, line L6 returns the smallest level of a ready job, and the job that runs is in that queue. So no ready job has a smaller level than the job that runs. Rules 2, 3 and 5 are lines L11, L5 and L3. Rule 4 is line L9.

**Claim 2 (the accounting invariant).** Fix a job $j$ and an interval of ticks with no boost. At the end of each tick in it, $\mathit{used}_j$ is the CPU time of $j$ since the later of the last boost, its arrival and its last change of level.

*Proof.* The counter is 0 at arrival (Rule 3) and after a boost (line L3). Line L8 adds 1 in each tick that $j$ runs. Line L9 sets it to 0 exactly when the level changes, or when a job at level $k - 1$ uses $A_{k-1}$ ticks and stays at $k - 1$. No other line changes it; in particular line L10 does not reset it when $j$ blocks. $\square$

**Theorem 1 (the accounting bound).** Between two consecutive boosts, let $u$ be the CPU time that job $j$ has used since the later of the boost and its arrival. Then

$$\mathit{lvl}_j = \min\Bigl\{k - 1,\ \max\{\ell \ge 0 : A_0 + \cdots + A_{\ell - 1} \le u\}\Bigr\}.$$

So in one boost period, job $j$ runs at most $A_0 + \cdots + A_{\ell - 1}$ ticks at levels below $\ell$, for each $\ell \le k - 1$, whatever its pattern of I/O.

*Proof.* By induction on $u$. For $u = 0$ the level is 0 and the formula gives 0. Assume the formula for $u$, with level $\ell < k - 1$. By Claim 2, $\mathit{used}_j = u - (A_0 + \cdots + A_{\ell - 1})$, which is at most $A_\ell - 1$ because the formula gives $\ell$ and not $\ell + 1$. When $j$ runs one more tick, $\mathit{used}_j$ grows by 1. Line L9 moves $j$ down exactly when the new value is $A_\ell$, that is, when $u + 1 = A_0 + \cdots + A_\ell$, which is when the formula changes from $\ell$ to $\ell + 1$. At level $k - 1$ both sides stay $k - 1$. The level depends only on $u$, so a job is at a level below $\ell$ only while $u < A_0 + \cdots + A_{\ell - 1}$, and each of those ticks adds 1 to $u$. $\square$

Under Rules 4a and 4b the theorem fails: the counter is reset at each I/O, so a job that blocks after $A_0 - 1$ ticks each time never leaves level 0, and $u$ grows without bound at level 0.

**Theorem 2 (the boost bound).** Let a boost happen at tick $t$, let at most $n$ jobs be in the system (arrived and not finished) during the ticks $t, \ldots, t + (n - 1) q_0$, and let $(n - 1) q_0 < S$. If job $j$ is ready at tick $t$ and stays ready until it runs, then it runs in one of the ticks $t, t + 1, \ldots, t + (n - 1) q_0$.

*Proof.* After line L3 of tick $t$, job $j$ is in $Q[0]$ with at most $n - 1$ jobs ahead of it. Jobs that join $Q[0]$ later (lines L4, L5 and L11) join at the tail, behind $j$. No boost happens before tick $t + S > t + (n - 1) q_0$. While $j$ is in $Q[0]$, $Q[0]$ is not empty, so by Rule 1 the head of $Q[0]$ runs in each tick. The head was boosted at $t$ with $\mathit{slice} = 0$, so after at most $q_0$ ticks it leaves the head: it finishes or blocks (line L10), or it moves down or to the tail at line L11, since $\mathit{slice}$ reaches $q_0$ by then. Each job ahead of $j$ leaves the head once and goes behind $j$ or out of $Q[0]$, so after at most $(n - 1) q_0$ ticks $j$ is the head, and it runs in the next tick. $\square$

**Termination.** Let $R$ be the sum, over the jobs that have arrived and are not finished, of the CPU ticks and the I/O ticks that each still has to do. After the last arrival, $R$ only falls. In a tick in which some job is ready, a job runs (by Claim 1 and line L6), so $R$ falls by at least 1. In a tick in which no job is ready but some job is unfinished, that job is in an I/O wait, which becomes one tick shorter, so $R$ falls by at least 1. So the loop of line L2 ends at most $R$ ticks after the last arrival. $\blacksquare$
