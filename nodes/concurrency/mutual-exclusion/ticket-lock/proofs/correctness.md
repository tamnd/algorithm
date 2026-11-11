---
title: The ticket lock gives mutual exclusion, FIFO order and starvation freedom, with at most n + 2 remote references per passage in the CC model
proves: [correctness]
status: full
---

**Setting.** There are $n$ asynchronous processes on a sequentially consistent memory. $next$ and $serving$ are shared counters, 0 at the start. $\mathrm{FETCH\text{-}AND\text{-}ADD}(next, 1)$ returns the old value of $next$ and adds 1, in one atomic step. We use the lines L1 to L6 of the page with unbounded counters, and we treat counters modulo $M$ at the end. Critical sections are finite, and a fair run gives infinitely many steps to every process that is not in its remainder section. The backoff of L5 is finite.

A process *holds* ticket $t$ from its L1 step that returns $t$ until its L6 step. A process that holds a ticket is in its entry, critical or exit section, and it holds one ticket at a time.

**Lemma 1 (distinct tickets).** The L1 steps return $0, 1, 2, \ldots$ in the order in which they happen. After $m$ such steps, $next = m$.

*Proof.* Only L1 changes $next$, by 1, atomically, and $next$ starts at 0. $\square$

**Lemma 2 (invariant).** At every time, either no process is in its critical or exit section and $serving$ is the smallest ticket that has not yet been released; or exactly one process is in its critical or exit section (before its L6 step), and it holds ticket $serving$. In both cases, every released ticket is smaller than $serving$, and every ticket that is held is at least $serving$.

*Proof.* By induction on the steps. At the start no ticket exists and $serving = 0 = next$. Consider the steps that matter.

- An L1 step creates the ticket $next \ge serving$, which is held and not released. The invariant still holds.
- A process $p$ with ticket $t$ passes L4 only after a read at L3 that returns $t$. At the time of that read $serving = t$, and $p$ is waiting. If some process $q$ were in its critical or exit section, then by induction $q$ would hold ticket $serving = t$, but tickets are distinct by Lemma 1. So no process is in its critical or exit section, and no process can write $serving$ until $p$ itself leaves. So when $p$ enters, $p$ is the only process in its critical or exit section, and it holds ticket $serving$.
- An L6 step by the process $p$ with ticket $t = serving$ writes $t + 1$ and releases $t$. Every ticket below $t$ was released before by induction, so $t + 1$ is the smallest ticket not released, and no process is in its critical or exit section.

Only L6 writes $serving$, and only a process in its exit section runs L6, so no other step changes $serving$. $\square$

**Lemma 3 (mutual exclusion).** At most one process is in its critical section at any time.

*Proof.* This is part of Lemma 2. $\square$

**Lemma 4 (FIFO order).** Processes enter their critical sections in the order of their tickets, which is the order of their L1 steps. So if $p$ finishes its doorway before $q$ starts its doorway, $q$ does not enter before $p$.

*Proof.* By Lemma 2, $serving$ takes the values $0, 1, 2, \ldots$ in order, each by one L6 step, and the process with ticket $t$ enters only while $serving = t$. So the entry with ticket $t$ comes before the L6 step that makes $serving = t + 1$, which comes before the entry with ticket $t + 1$. By Lemma 1, earlier doorways give smaller tickets. $\square$

**Lemma 5 (starvation freedom).** In a fair run, every process that takes a ticket enters its critical section.

*Proof.* Let $p$ hold ticket $t$, and let $s_0 = serving$ when $p$ takes it. By Lemma 2, the tickets $s_0, \ldots, t - 1$ are held by other processes, one ticket each, so $t - s_0 \le n - 1$. Assume that $serving = u < t$ from some time on. Then by Lemma 2 the holder of ticket $u$ either is in its critical or exit section, which ends in a finite number of its steps with L6, or it is waiting; in the second case no process is in its critical section, and the holder of $u$ reads $serving = u$ at its next L3 (the backoff is finite) and enters. Either way $serving$ changes, which is a contradiction. So $serving$ reaches $t$, and then $p$ reads $t$ at its next L3 and enters, because no other process can write $serving$ before $p$ leaves. $\square$

**Lemma 6 (remote references in the CC model).** One passage makes at most $n + 2$ remote memory references in the CC model, without backoff and with it.

*Proof.* In the CC model a step is remote if it is an atomic update or a write, or a read of a word that another process wrote since the last access of the reader to it. L1 is one remote step and L6 is one. The first read of $serving$ at L3 may miss. Each later read misses only if some L6 step wrote $serving$ since the previous read of $p$. While $p$ waits with ticket $t$, the L6 steps move $serving$ from $s_0$ to $t$ by Lemma 2, so there are $t - s_0 \le n - 1$ of them. So the reads of $p$ make at most $1 + (n - 1) = n$ remote references, and the passage at most $n + 2$. Backoff only removes reads. $\square$

The bound is tight. If processes $0, \ldots, n - 1$ take tickets in that order and then run in rounds, the last process reads $serving$ once after each of the $n - 1$ handovers, so it pays exactly $n + 2$. The test file checks this for $n$ from 2 to 8.

**Lemma 7 (bounded counters).** If L1, L5 and L6 count modulo $M$ with $M \ge n$, Lemmas 2 to 6 still hold.

*Proof.* By the proof of Lemma 5, while $p$ waits with ticket $t$, $serving \in \{t - n + 1, \ldots, t\}$ in unbounded counting. For two such values the difference is less than $n \le M$, so they are equal modulo $M$ only if they are equal. So the test at L4 gives the same answer with residues as with unbounded counters, and L5 computes the same distance. $\square$

For $M < n$ the argument fails, and the test file finds a run with $M = 2$ and three processes in which two processes hold ticket 0 at the same time and both enter.

Lemmas 3, 4 and 5 show that the ticket lock solves the mutual exclusion problem with FIFO order and starvation freedom, and Lemma 6 gives the CC cost of a passage. $\blacksquare$
