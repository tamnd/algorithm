---
title: Polite keeps obstruction freedom but does not prevent livelock
proves: [correctness]
status: full
---

**Model.** Threads run transactions that open objects, one at a time, for exclusive access, and then commit. A step is: a restart after an abort; one step of backoff; an open of a free object (L6); a call of RESOLVE against the active owner $B$ of the next object, which either aborts $B$ by compare-and-swap and takes the object (L2, then L6), or starts a backoff of $2^{\mathrm{tries}}$ steps and increments the counter (L3 to L5); or a commit. Aborting $B$ frees all objects of $B$. The random spin of the paper is modelled by its mean length, as a number of steps of the waiting thread; threads are asynchronous, and the scheduler chooses which thread takes the next step.

Safety is the job of the STM and does not depend on the answers of the manager, so we prove only progress properties.

**Lemma 1 (each conflict ends).** If $A$ calls RESOLVE for object $o$ and the same active transaction owns $o$ at each later call of $A$ for $o$, then the $(m+1)$-st call aborts the owner. Before it, $A$ spends $\sum_{i=0}^{m-1} 2^i = 2^m - 1$ steps of backoff.

*Proof.* The counter of $A$ is reset only on L6, when $A$ gets an object, so it is $0, 1, \ldots$ at the successive calls for $o$. Calls $1$ to $m$ see $\mathrm{tries}(A) = 0, \ldots, m - 1 < m$ and set a backoff of $2^0, \ldots, 2^{m-1}$ steps. Call $m + 1$ sees $\mathrm{tries}(A) = m$ and returns ABORT-ENEMY on L2. If the owner changes between calls (it commits or is aborted), the object may become free, and then $A$ opens it at once. $\square$

**Theorem 1 (obstruction freedom).** If, from some time on, only the thread of $A$ takes steps, then $A$ commits within $1 + k(m + 2^m) + 1$ of its own steps, where $k$ is the number of objects $A$ opens.

*Proof.* No other thread takes steps, so no other transaction aborts $A$ or takes an object. If $A$ is aborted at that time, its next step restarts it. Then, for each of its $k$ objects, either the object is free or owned by $A$ (one step), or its owner is a frozen transaction, and by Lemma 1 $A$ takes at most $m$ calls that return WAIT, $2^m - 1$ steps of backoff and one call that aborts the owner and takes the object, so at most $m + 2^m$ steps. Then $A$ commits in one step. $\square$

The tests check the exact count $m + (2^m - 1) + 3$ for a transaction that opens two objects, the first held by a stopped transaction, for $m$ from 0 to 4.

**Theorem 2 (no livelock freedom).** For every $m \ge 0$ there is a fair infinite run with two transactions in which no transaction commits.

*Proof.* Let $T_0$ open $x$ then $y$, and $T_1$ open $y$ then $x$. Start from the state $S$ where $T_0$ owns $x$ and has opened one object, $T_1$ owns nothing, both are active, and no backoff is pending. Run, in order:

1. $T_0$ opens $y$, which is free. $T_0$ is now ready to commit.
2. $T_1$ alone: it wants $y$, owned by $T_0$. By Lemma 1, after $m$ waits and $2^m - 1$ backoff steps it aborts $T_0$ and takes $y$, which frees $x$.
3. $T_0$ restarts.
4. $T_1$ opens $x$, which is free. $T_1$ is now ready to commit.
5. $T_0$ alone: it wants $x$, owned by $T_1$, and in the same way it aborts $T_1$ and takes $x$.
6. $T_1$ restarts.

Polite keeps no state across aborts, and both counters were reset when the objects were taken, so the state is again $S$. Both threads take steps in each round, so the run that repeats the round for ever is fair, and in it no transaction commits. $\blacksquare$

The run needs the scheduler to keep $T_0$ idle during the whole backoff of step 2, and $T_1$ during step 5. In real time, with random spin times and threads that run at similar speeds, this is unlikely to happen again and again, which is why Polite works in practice; but the model shows that the manager itself does not exclude it.
