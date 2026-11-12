---
title: Under priority inheritance a job is blocked by at most min(n, m) critical sections
proves: [correctness]
status: full
---

**Setting.** One processor runs a finite set of jobs. Each job $J$ has a release time $r_J$, a base priority $p(J)$, and the base priorities are distinct. A job runs, locks and unlocks binary semaphores, and does nothing else: it does not suspend itself. Critical sections are properly nested, and a job ends with no lock held. Lock and unlock actions take no time. In each step the algorithm of the page computes the blockers (line L3) and the current priorities $p^*$ (line L4), and runs or lets act the ready job with the largest $p^*$ (line L5). We study a run that has no deadlock, that is, line L7 never stops it. The protocol does not prevent deadlock, so this condition is necessary.

A job is *pending* at time $t$ if $r_J \le t$ and it is not finished. A pending job is *waiting* if line L10 found its lock held; it then waits for the holder $b(J)$ of that lock. It is *ready* if it is pending and not waiting. An *outermost critical section* of a job is a critical section that starts when the job holds no lock. We say that $J$ is *blocked* in time slot $[s, s+1)$ if $J$ is pending at $s$ and a job $L$ with $p(L) < p(J)$ runs in that slot.

**Lemma 1 (current priorities).** At each step, $p^*(J) \ge p(J)$ for each job, and $p^*(b(X)) \ge p^*(X)$ for each waiting job $X$. A job $L$ with $p^*(L) > p(L)$ holds a lock.

*Proof.* Line L4 starts from $p^* = p$ and only raises values. It stops when no waiting job $X$ has $p^*(X) > p^*(b(X))$, which is the second claim. A value $p^*(L)$ rises above $p(L)$ only when some job waits for $L$, and a job waits for $L$ only for a lock that $L$ holds. $\square$

**Lemma 2 (chains end at a ready job).** At a step with no deadlock, for each pending job $J$ there is a ready job $K$ with $p^*(K) \ge p(J)$.

*Proof.* Follow $J, b(J), b(b(J)), \ldots$ while the current job is waiting. Each job in the chain is pending, because only a pending job holds a lock. If the chain visits a job twice, its jobs form a cycle in which each job waits for a lock that the next one holds. No job on the cycle is ready, so none of them can run and free a lock, and they wait forever. This is a deadlock, which the setting excludes. So the chain has no repeat, and as the set of jobs is finite, it ends at a job $K$ that is not waiting, that is, a ready job. By Lemma 1, applied along the chain, $p^*(K) \ge p^*(J) \ge p(J)$. $\square$

**Lemma 3 (a lower job runs only in an old critical section).** Let $J$ be pending at time $s$, and let a job $L$ with $p(L) < p(J)$ run in slot $[s, s+1)$. Then at time $s$, $L$ is inside an outermost critical section that it entered before $r_J$.

*Proof.* Line L5 chose $L$, so $p^*(L) \ge p^*(K)$ for the ready job $K$ of Lemma 2, and $p^*(L) \ge p(J) > p(L)$. By Lemma 1, $L$ holds a lock at $s$, so it is inside an outermost critical section. Let $e$ be the time of the lock action that opened it. Assume that $e \ge r_J$. Then $J$ is pending at time $e$, as $r_J \le e \le s$ and $J$ is not finished at $s$. Just before this lock action, $L$ holds no lock, so no job waits for $L$ and $p^*(L) = p(L)$ by Lemma 1. Line L5 chose $L$ for the lock action, so $p(L) \ge p^*(K')$ for the ready job $K'$ that Lemma 2 gives for $J$ at that step. But $p^*(K') \ge p(J) > p(L)$, which is a contradiction. So $e < r_J$. $\square$

**Theorem.** Let $n$ be the number of jobs with base priority lower than $p(J)$, and let $m$ be the number of distinct semaphores that these jobs lock in outermost critical sections. In a run with no deadlock, all slots in which $J$ is blocked fall inside at most $\min(n, m)$ outermost critical sections. These sections belong to distinct jobs and start with distinct semaphores. The total blocking of $J$ is at most the sum, over the lower jobs, of the longest outermost critical section of each.

*Proof.* By Lemma 3, each blocking slot of $J$ lies inside an outermost critical section of a lower job that was entered before $r_J$ and not yet left at $r_J$, since it is still open at the slot $s \ge r_J$. At time $r_J$ a job is inside at most one outermost critical section, so these sections belong to distinct jobs and there are at most $n$ of them. The semaphore that opens an outermost critical section is held for the full section, and a semaphore has at most one holder at a time. So two sections that are both open at $r_J$ start with distinct semaphores, and there are at most $m$ of them. A section that is left is not open again, so each of them contributes at most its own length. $\blacksquare$

**Remarks.** The bound counts critical sections, not jobs of medium priority: a job $M$ with $p(L) < p(M) < p(J)$ that locks nothing never runs while $J$ waits for $L$, because $p^*(L) \ge p(J) > p(M)$ in that time. The bound can be reached: in the chained example of the page, $J_1$ is blocked once by each of two lower jobs. The setting assumes no deadlock; two jobs that lock two semaphores in opposite orders can deadlock under this protocol.
