---
title: Polka keeps obstruction freedom but does not prevent livelock
proves: [correctness]
status: full
---

**Model.** Threads run transactions that open objects, one at a time, for exclusive access, and then commit. A step is: a restart after an abort (L8); one step of backoff; an open of a free object (L1, L2); a call of RESOLVE against the active owner $B$ of the next object, which either aborts $B$ by compare-and-swap and takes the object (L4, then L1, L2), or starts a backoff of $2^{\mathrm{tries}}$ steps and increments the counter (L5 to L7); or a commit (L9). Aborting $B$ frees all objects of $B$. The random spin of the paper is modelled by its mean length, as a number of steps of the waiting thread; threads are asynchronous, and the scheduler chooses which thread takes the next step.

Safety is the job of the STM and does not depend on the answers of the manager, so we prove only progress properties.

**Lemma 1 (each conflict ends).** Suppose $A$ calls RESOLVE for object $o$, and at each later call of $A$ for $o$ the same active transaction $B$ owns $o$ and $d = \mathrm{prio}(B) - \mathrm{prio}(A)$ has the same value. Then $A$ aborts $B$ at call $\max(d, 0) + 1$, and before it spends $\sum_{i=0}^{d-1} 2^i = 2^d - 1$ steps of backoff (none if $d \le 0$).

*Proof.* The counter of $A$ is reset only on L2, when $A$ gets an object, so it is $0, 1, 2, \ldots$ at the successive calls for $o$. While $\mathrm{tries}(A) < d$, the test on L3 fails, and L5 sets a backoff of $2^{\mathrm{tries}(A)}$ steps. The first call with $\mathrm{tries}(A) \ge d$ is call $\max(d, 0) + 1$, and it returns ABORT-ENEMY on L4. $\square$

If the owner changes between calls, because it commits or is aborted, the object may become free, and then $A$ opens it at once. If $\mathrm{prio}(B)$ grows, then $B$ is taking steps and is not stopped.

**Theorem 1 (obstruction freedom).** If, from some time on, only the thread of $A$ takes steps, then $A$ commits within a bounded number of its own steps.

*Proof.* No other thread takes steps, so no other transaction changes a priority, aborts $A$ or takes an object. If $A$ is aborted at that time, its next step restarts it. Then, for each of its objects, either the object is free or owned by $A$ (one step), or its owner $B$ is frozen, so $\mathrm{prio}(B)$ is fixed. The priority of $A$ changes only when $A$ gets an object, so during the conflict over this object the gap $d$ is fixed too, and Lemma 1 applies: $A$ takes at most $d + 2^d$ steps for the object, counting the waits, the backoff and the call that aborts $B$. The priorities of the frozen transactions are fixed numbers, and the priority of $A$ only grows, so each gap is at most $D = \max_B \mathrm{prio}(B) - \mathrm{prio}(A)$ at the time $A$ starts to run alone. With $k$ objects to open, $A$ commits within $1 + k(D + 2^D) + 1$ of its own steps. $\square$

The tests check the exact count $d + (2^d - 1) + 2$ for a transaction with one object that is held by a stopped transaction of priority $d$, for $d$ from 2 to 5.

**Theorem 2 (no livelock freedom).** There is a fair infinite run with two transactions in which no transaction commits.

*Proof.* Let $T_0$ open $x$ then $y$, and $T_1$ open $y$ then $x$. Let $S_p$ be the state where $T_0$ owns $x$ and has $\mathrm{prio}(T_0) = p + 1$, $T_1$ owns nothing and has $\mathrm{prio}(T_1) = p$, both are active, both counters are 0, and no backoff is pending. Run, in order:

1. $T_0$ opens $y$, which is free (L1, L2). Now $\mathrm{prio}(T_0) = p + 2$, and $T_0$ is ready to commit.
2. $T_1$ alone: it wants $y$, owned by $T_0$, with gap $d = 2$. By Lemma 1, after 2 waits and 3 backoff steps it aborts $T_0$ and takes $y$, which frees $x$. Now $\mathrm{prio}(T_1) = p + 1$.
3. $T_0$ restarts (L8) and keeps $\mathrm{prio}(T_0) = p + 2$.
4. $T_1$ opens $x$, which is free. Now $\mathrm{prio}(T_1) = p + 2$, and $T_1$ is ready to commit.
5. $T_0$ wants $x$, owned by $T_1$, with gap $(p + 2) - (p + 2) = 0$. The test on L3 holds with $\mathrm{tries}(T_0) = 0$, so $T_0$ aborts $T_1$ and takes $x$. Now $\mathrm{prio}(T_0) = p + 3$.
6. $T_1$ restarts and keeps $\mathrm{prio}(T_1) = p + 2$.

The state is now $S_{p+2}$. Polka decides only on priority differences, so from $S_{p+2}$ the same schedule is enabled and gives the same steps, and the round repeats for ever. Both threads take steps in each round, so the run is fair, and in it no transaction commits. $\blacksquare$

The run needs the scheduler to keep $T_0$ idle during the whole backoff of step 2. In real time, with random spin times and threads that run at similar speeds, this is unlikely to happen again and again, which is why Polka works in practice; but the manager itself does not exclude it. The implementation finds this cycle by a search of the state graph, from $S_0$ after the single step in which $T_0$ opens $x$, and replays it.
