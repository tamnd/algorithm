---
title: The priority ceiling protocol prevents deadlock and blocks a job for at most one critical section
proves: [correctness]
status: full
---

**Setting.** One processor runs a finite set of jobs with distinct base priorities $p(J)$ and release times $r_J$. A job runs, locks and unlocks binary semaphores, and does nothing else; it does not suspend itself, it never locks a semaphore that it holds, its critical sections are properly nested, and it ends with no lock held. The ceiling $c(S)$ of a semaphore is the highest base priority of a job that uses $S$, so $c(S) \ge p(J)$ whenever $J$ uses $S$. For a job $J$, $\Pi_J$ is the highest ceiling of a semaphore held by a job other than $J$, or $-\infty$ if there is none.

A job that has asked for $S$ is *denied* while $S$ is held or $p^*(J) \le \Pi_J$ (lines L3 and L10). A denied job waits for its *blocker*, the holder of a held semaphore of highest ceiling. Line L4 sets $p^*(x) = p(x)$ and then raises the current priority of each blocker to at least that of each job that waits for it. A job is *ready* if it is pending and not denied. Line L5 picks the ready job of largest $p^*$. A job that holds a lock is a *holder*. An *outermost critical section* starts when the job holds no lock. Slot $[s, s+1)$ is a *blocking slot* of $J$ if $J$ is pending at $s$ and a job $L$ with $p(L) < p(J)$ runs in it.

**Invariant (INV).** After each computation of lines L3 and L4, let $K_1, \ldots, K_r$ be the holders, ordered by the time at which each took its current outermost lock. Then

1. for $i < k$, $p(K_k) > c(R)$ for every semaphore $R$ held by $K_i$;
2. each denied job holds no lock, and its blocker is $K_r$;
3. $K_r$ is ready.

Two facts follow at once. First, since $K_k$ uses each lock it holds, (1) gives $c(R') \ge p(K_k) > c(R)$ for a lock $R'$ of $K_k$ and a lock $R$ of $K_i$, $i < k$. So every held semaphore of highest ceiling is held by $K_r$, and the blocker of (2) is well defined. Second, by (2) only $K_r$ can wait for nobody and have a job wait for it, so $p^*(x) = p(x)$ for every job $x \ne K_r$.

(4) *No holder other than $K_r$ is picked by line L5.* For $i < r$, $p^*(K_i) = p(K_i) \le c(R) < p(K_r) \le p^*(K_r)$ for a lock $R$ of $K_i$, by (1), and $K_r$ is ready by (3).

**Lemma 1.** INV holds at each step.

*Proof.* At the start there is no holder and no denied job. Assume INV before a step and look at the action of the job $j$ that line L5 picks.

*A lock is granted to $j$.* If $j$ holds no lock, then $p^*(j) = p(j)$, and the grant needs $p(j) > \Pi_j$, the highest ceiling of all held locks. So $j$ becomes $K_{r+1}$ and (1) holds. The new lock $S$ has $c(S) \ge p(j)$, so the highest ceiling is now held by $j$. If $j$ is a holder, then $j = K_r$ by (4), the order does not change, and $K_r$ keeps its locks of highest ceiling. In both cases a denied job stays denied: the set of held locks only grows, and its own $p^*$ equals its base priority. Its blocker is the new top holder, so (2) holds. The new top holder has no request open, so (3) holds.

*A lock is refused to $j$.* If $j = K_r$, then $p^*(K_r) \ge p(K_r) > \Pi_{K_r}$ by (1). The semaphore $S$ it asks for is not held by $K_r$ itself, and if $K_i$ with $i < r$ held it, then $c(S) \ge p(K_r) > c(S)$ by (1), which is false. So $K_r$ is never refused. By (4), $j$ is not another holder. So $j$ holds no lock, a held lock exists, and its blocker is $K_r$, as (2) needs.

*$j$ frees a lock.* Then $j = K_r$ by (4). If $j$ still holds a lock, the order is the same and (1) holds for a subset of the locks. If $j$ frees its last lock, it leaves the list, and (1) holds for the rest. Line L3 then decides again which jobs are denied. A job that is still denied holds no lock, and its blocker is the new top holder, which holds the lock of highest ceiling. The new top holder has had no request open since it took its first lock, because only a job with no lock can be refused. So (2) and (3) hold.

*$j$ runs, or the processor idles, or a job is released or ends.* No lock changes hands. A new job holds no lock and has no request open. An ending job holds no lock. So INV still holds. $\square$

**Lemma 2 (no deadlock).** Line L7 never stops the run.

*Proof.* Let some job be pending. If $r \ge 1$, then $K_r$ is pending and ready by (3). If $r = 0$, then no job is denied by (2), so each pending job is ready. In both cases line L6 finds a ready job. $\square$

**Lemma 3 (who blocks).** Let $s$ be a blocking slot of $J$, with $L$ running. Then $L = K_r$ at time $s$, $p^*(L) \ge p(J)$, and $L$ holds a lock of ceiling at least $p(J)$.

*Proof.* If $J$ is ready, line L5 gives $p^*(L) \ge p^*(J) \ge p(J) > p(L)$. If $J$ is denied, its blocker $K_r$ is ready and $p^*(K_r) \ge p^*(J) \ge p(J)$, so again $p^*(L) \ge p(J) > p(L)$. Then $L$ inherited a priority, so by (2) $L = K_r$, and some denied job $x$ has $p(x) = p^*(L) \ge p(J)$ (the case $x = J$ is allowed). The job $x$ is denied, so either it asked for a held semaphore $S$, with $c(S) \ge p(x)$ because $x$ uses $S$, or $p(x) \le \Pi_x$. In both cases a held lock has ceiling at least $p(x) \ge p(J)$, and the lock of highest ceiling is held by $K_r = L$. $\square$

**Lemma 4 (the lock is old).** In the setting of Lemma 3, $L$ held at time $r_J$ a lock of ceiling at least $p(J)$, and it held that lock without a break until $s$.

*Proof.* Among the locks that $L$ holds at $s$ with ceiling at least $p(J)$, take the one, $R$, that $L$ took first, at time $h$. Assume that $h \ge r_J$. At time $h$, $J$ is pending, and line L5 picks $L$ for its lock action. The argument of Lemma 3 applies to any step in which a lower job is picked while $J$ is pending, so at time $h$, before it takes $R$, $L$ already holds a lock $R'$ with $c(R') \ge p(J)$. Locks are properly nested and $L$ took $R'$ before $R$, so $L$ frees $R'$ after $R$, and it still holds $R'$ at $s$. This contradicts the choice of $R$. So $h < r_J$. $\square$

**Theorem.** In each run, no deadlock occurs. A job $J$ has blocking slots in at most one outermost critical section of one job of lower priority, and that section locks a semaphore of ceiling at least $p(J)$. So the blocking time of $J$ is at most the longest such section among the jobs of lower priority.

*Proof.* Lemma 2 gives the first claim. Let two distinct jobs $L_1$ and $L_2$ of lower priority both run in blocking slots of $J$. By Lemma 4, at time $r_J$ each $L_k$ held a lock $R_k$ with $c(R_k) \ge p(J)$. So both were holders at $r_J$; say $L_1$ comes before $L_2$ in the order of INV. Then (1) gives $p(L_2) > c(R_1) \ge p(J)$, which contradicts $p(L_2) < p(J)$. So all blocking slots belong to one job $L$. By Lemma 4 they lie in the outermost critical section that $L$ was in at time $r_J$, without a break, and this section contains $R$. Once it ends, $L$ cannot run in a blocking slot of $J$ again, as a later slot would need a lock held at $r_J$. $\blacksquare$
