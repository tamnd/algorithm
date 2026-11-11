---
title: Karma keeps obstruction freedom but does not prevent livelock
proves: [correctness]
status: full
---

**Model.** Threads run transactions that open objects, one at a time, for exclusive access, and then commit. A step is: a restart after an abort; one step of a backoff interval of $I \ge 0$ steps; an open of a free object (L1, L2); a call of RESOLVE against the active owner $B$ of the next object, which either aborts $B$ by compare-and-swap and takes the object (L4, then L1 and L2), or increments the counter and starts a backoff interval (L5 to L7); or a commit (L9). Aborting $B$ frees all objects of $B$. Threads are asynchronous; the scheduler chooses which thread takes the next step.

Safety (what values transactions see, and when they commit) is the job of the STM and does not depend on the answers of the manager, so we prove only progress properties.

**Lemma 1 (bounded wait).** Suppose $A$ calls RESOLVE against $B$ for an object $o$, and the same attempt of $B$ owns $o$ during all later calls of $A$ for $o$. Let $d = \mathrm{prio}(B) - \mathrm{prio}(A)$ at the first call, and let $B$ open at most $\ell$ more objects in this attempt. Then $A$ aborts $B$ after at most $\max(0, d + \ell + 1)$ intervals of waiting.

*Proof.* While $A$ waits for $o$, it opens no object, so $\mathrm{prio}(A)$ does not change, and $\mathrm{tries}(A)$ is not reset by L2. Each call that returns WAIT adds one to $\mathrm{tries}(A)$ (L5). The priority of $B$ grows only on L1, once per object that $B$ opens, so it is at most $\mathrm{prio}(A) + d + \ell$. After $t$ waits, the test of L3 is $\mathrm{prio}(A) + t > \mathrm{prio}(B)$, which holds as soon as $t > d + \ell$. So the call after at most $\max(0, d + \ell + 1)$ waits returns ABORT-ENEMY. $\square$

If $B$ does not take steps while $A$ waits, then $\ell = 0$ in effect and the bound is $\max(0, d + 1)$, which is exact: for $t \le d$ the test fails. The tests check this case for $-3 \le d \le 5$.

**Theorem 1 (obstruction freedom).** If, from some time on, only the thread of $A$ takes steps, then $A$ commits after a bounded number of its own steps.

*Proof.* The other transactions are frozen, so their priorities and the owners of objects change only through $A$. If $A$ is aborted at that time, its next step restarts it. Then $A$ walks through its list of $k$ objects. For each object, either it is free or owned by $A$ (one step), or its owner $B$ is a frozen active transaction. In the last case, by Lemma 1 with $\ell = 0$, $A$ aborts $B$ after at most $\max(0, d + 1)$ waits, each of $1 + I$ steps, and $d$ is bounded by the largest priority of a frozen transaction. No other thread can abort $A$, so $A$ reaches the end of its list and commits. The number of steps is at most $1 + \sum_{i=1}^{k} (1 + (1 + I) \max(0, d_i + 1)) + 1$. $\square$

**Theorem 2 (no livelock freedom).** There is a fair infinite run with two transactions in which no transaction commits.

*Proof.* Let $T_0$ open $x$ then $y$, and $T_1$ open $y$ then $x$, with $I = 1$. Start from the state $S$ where $T_0$ owns $x$ with priority $p + 1$, and $T_1$ owns nothing with priority $p$, both active and with zero counters. Run, in order:

1. $T_0$ opens $y$; priorities $p + 2$ and $p$; $T_0$ is ready to commit.
2. $T_1$ calls RESOLVE three times (each followed by its backoff step): $p + 0$, $p + 1$ and $p + 2$ are not more than $p + 2$, so it waits each time. At the fourth call, $p + 3 > p + 2$, so it aborts $T_0$ and takes $y$; priorities $p + 2$ and $p + 1$.
3. $T_0$ restarts and keeps priority $p + 2$.
4. $T_1$ opens $x$, which is free; priorities $p + 2$ and $p + 2$.
5. $T_0$ wants $x$: $p + 2 > p + 2$ is false, so it waits; after the backoff step, $p + 3 > p + 2$, and it aborts $T_1$ and takes $x$; priorities $p + 3$ and $p + 2$.
6. $T_1$ restarts and keeps priority $p + 2$.

The state is now $S$ with $p$ replaced by $p + 2$. Every decision of Karma depends only on the difference of priorities and on the counters, so the same schedule applies again, for ever. Both threads take steps in every round, and no transaction commits. $\blacksquare$

The run is not a failure of the STM: each abort is allowed, and obstruction freedom only promises progress to a thread that runs alone. A scheduler in real time that lets $T_0$ run during the three backoff intervals of step 2 ends the cycle, which is why Karma works well in practice.
