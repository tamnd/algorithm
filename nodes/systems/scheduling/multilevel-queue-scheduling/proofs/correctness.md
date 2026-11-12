---
title: Multilevel queue scheduling keeps jobs in their class, conserves work, isolates higher classes and gives the time-slice shares
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. There are $n$ jobs with arrival ticks $a_j \ge 0$, demands $b_j \ge 1$ and classes $c_j \in \{0, \ldots, k-1\}$. A job is *ready* at tick $t$ if $a_j \le t$ and it has run fewer than $b_j$ ticks before $t$. One pass of the loop of line L2 is *tick* $t$, for the value of $t$ at line L3.

**Claim 1 (no movement).** After line L3 of each tick, $Q[i]$ holds exactly the ready jobs of class $i$, and a job runs only at line L7 as the head of $Q[c_j]$.

*Proof.* By induction on the ticks. Before tick 0 all queues are empty. Line L3 appends a job only to $Q[c_j]$, once, at tick $a_j$. Line L8 removes a job from its own queue when it has run $b_j$ ticks, which is the moment it stops being ready. Line L9 moves a job inside its own queue. No other line changes a queue. Line L6 takes the head of the queue that line L4 selected, so the job that runs is in $Q[i]$ with $i = c_j$. $\square$

**Claim 2 (work conservation and termination).** In each tick, the CPU idles only if no job is ready. The loop ends after at most $\max_j a_j + \sum_j b_j + 1$ ticks.

*Proof.* Both forms of SELECT-QUEUE return a queue whenever some queue is non-empty: fixed priority scans all $k$ queues, and time slicing scans the $k$ queues from the current turn. By Claim 1 a queue is non-empty exactly when a ready job of its class exists, so line L5 idles only if no job is ready. After tick $\max_j a_j$ every job has arrived, so while a job is unfinished, each tick runs a job and lowers the total remaining demand $\sum_j (b_j - \text{run}_j)$ by exactly 1. This total is at most $\sum_j b_j$, so it reaches 0 within $\sum_j b_j$ more ticks, and then line L2 stops. $\square$

**Claim 3 (isolation under fixed priority).** Fix a class $c$. Let $J_{\le c}$ be the jobs of classes $0, \ldots, c$. Run the algorithm with fixed priority once on all jobs and once on $J_{\le c}$ only. Then at the start of each tick the queues $Q[0], \ldots, Q[c]$, with their order and the counters $\mathit{used}_j$, are the same in the two runs, and each job of $J_{\le c}$ runs in the same ticks.

*Proof.* By induction on the ticks. At tick 0 all queues are empty in both runs. Assume the queues $0, \ldots, c$ are equal at the start of tick $t$. Line L3 appends the same jobs of classes at most $c$ in both runs, in the same order, so they stay equal. Two cases for line L4.

- Some queue $Q[i]$ with $i \le c$ is non-empty. Fixed priority returns the smallest such $i$ in both runs, because it scans the queues in index order and these queues are equal. Lines L6 to L9 then do the same thing in both runs, and they change only $Q[i]$ and the counter of its head.
- All of $Q[0], \ldots, Q[c]$ are empty. In the second run no job is ready, and the CPU idles. In the first run a job of a class above $c$ may run. In both runs lines L6 to L9 change no queue with index at most $c$.

So the queues $0, \ldots, c$ are equal at the start of tick $t + 1$, and the job of $J_{\le c}$ that runs in tick $t$, if any, is the same. $\square$

**Claim 4 (shares under time slicing).** Assume that from some tick $t_0$ on all $k$ queues stay non-empty, and that a turn of queue 0 starts at $t_0$. Then for each $m \ge 0$, the ticks $t_0 + mS, \ldots, t_0 + (m+1)S - 1$ with $S = \sum_i s_i$ give exactly $s_i$ ticks to queue $i$.

*Proof.* While the queue of the turn is non-empty, SELECT-QUEUE returns it, and the counter of the turn grows by 1 in each tick. When the counter reaches $s_i$, the turn passes to $i + 1 \bmod k$ with a counter of 0. Since no queue is empty, no turn is skipped. So the ticks from $t_0$ on are the turns $0, 1, \ldots, k-1$ of lengths $s_0, \ldots, s_{k-1}$, repeated, and each block of $S$ ticks from $t_0$ is one full cycle. $\square$

**Theorem.** With finitely many jobs, MLQ-SCHEDULE ends with every job finished, $C_j$ is the tick at which job $j$ ran its last tick, and Claims 1, 3 and 4 hold.

*Proof.* Claim 2 gives termination, and the loop ends only when every job has run $b_j$ ticks. Line L8 sets $C_j$ to the tick after the last run of $j$, once. Claims 1, 3 and 4 are proved above. $\blacksquare$
