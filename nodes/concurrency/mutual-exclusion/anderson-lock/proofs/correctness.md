---
title: Anderson's lock gives mutual exclusion, FIFO order and starvation freedom, with O(1) remote references per passage in the CC model
proves: [correctness]
status: full
---

**Setting.** There are $n$ asynchronous processes on a sequentially consistent memory. $next\_slot$ is a counter with atomic fetch-and-add, 0 at the start. $slot[0..n - 1]$ are atomic registers with $slot[0] = HAS\_LOCK$ and the others $MUST\_WAIT$ at the start. We use the lines L1 to L6 of the page, and $x \bmod n$ is the residue in $\{0, \ldots, n - 1\}$. Critical sections are finite, and a fair run gives infinitely many steps to every process that is not in its remainder section.

**Tickets.** Number the L1 steps of the run $0, 1, 2, \ldots$ in order, and call the number of its L1 step the *ticket* of the process in that passage. A process *holds* its ticket from its L1 step to its L6 step.

**Lemma 1 (places).** The process with ticket $m$ gets $place = m \bmod n$ at L3.

*Proof.* Every change of $next\_slot$ adds $1$ (at L1) or $-n$ (at L2). So after $m$ L1 steps and any number of L2 steps, $next\_slot \equiv m \pmod n$. The L1 step with ticket $m$ comes after $m$ earlier L1 steps, so it returns a value $\equiv m \pmod n$, and L3 takes the residue. $\square$

Let $r$ be the number of L6 steps so far. Call the process with ticket $r$, if it exists, the *head*.

**Lemma 2 (invariant).** At every time:

1. The held tickets are exactly $r, r + 1, \ldots, next - 1$, where $next$ is the number of L1 steps so far, and $next - r \le n$.
2. Either (a) $slot[r \bmod n] = HAS\_LOCK$, every other slot is $MUST\_WAIT$, and every process that holds a ticket is before L5 in its entry section; or (b) every slot is $MUST\_WAIT$, and the head is after L5 and before L6, and every other process that holds a ticket is before L5.

*Proof.* By induction on the steps. At the start $r = next = 0$, and (a) holds. Consider each step that changes the invariant.

- *L1.* It creates ticket $next$, so the held tickets stay an interval. Each process holds at most one ticket, so at most $n$ are held. The new process is before L5. Part 2 is unchanged.
- *L4 reads $HAS\_LOCK$.* The reader $p$ holds ticket $m$ and reads $slot[m \bmod n]$ by Lemma 1. In case (b) no slot is $HAS\_LOCK$, so we are in case (a), and $m \equiv r \pmod n$. By part 1, $r \le m \le r + n - 1$, so $m = r$: $p$ is the head. Nothing changes yet.
- *L5.* The writer $p$ has passed L4, so by the case above it is the head, in case (a), and it writes $MUST\_WAIT$ to $slot[r \bmod n]$. Now every slot is $MUST\_WAIT$, and the head is after L5: case (b).
- *L6.* Only a process after L5 runs L6, so by induction we are in case (b) and the writer is the head, with ticket $r$. It releases ticket $r$ and writes $HAS\_LOCK$ to $slot[(r + 1) \bmod n]$. Now the count is $r + 1$, the held tickets are $r + 1, \ldots, next - 1$, and case (a) holds for $r + 1$.

Reads that return $MUST\_WAIT$, L2 and L3 change neither part. $\square$

**Lemma 3 (mutual exclusion).** At most one process is in its critical section at any time.

*Proof.* A process in its critical section is after L5 and before L6. By Lemma 2, only the head can be there. $\square$

**Lemma 4 (FIFO order).** Processes enter in the order of their tickets, so in the order of their doorways (L1).

*Proof.* By Lemma 2, only the head passes L4, and the head changes from ticket $r$ to ticket $r + 1$ only at the L6 of ticket $r$, after it has entered. $\square$

**Lemma 5 (starvation freedom).** In a fair run, every process that runs L1 enters its critical section.

*Proof.* Let $p$ hold ticket $m$. The tickets $r, \ldots, m - 1$ are held by at most $n - 1$ other processes. Assume that $r$ stops growing at a value $r \le m$. If the head is after L5, it finishes its critical section and runs L6, which increases $r$. Otherwise case (a) holds, so $slot[r \bmod n] = HAS\_LOCK$ and stays so, and the head finishes L2 and L3 and reads $HAS\_LOCK$ at L4, then runs L5, enters, and runs L6. Either way $r$ grows, which is a contradiction. So $r$ reaches $m$, and $p$ enters by the same argument. $\square$

**Lemma 6 (remote references in the CC model).** If each slot lies on its own cache line, a passage makes at most 6 remote references in the CC model.

*Proof.* Let $p$ hold ticket $m$ and place $i = m \bmod n$. L1 and L2 are at most two atomic steps, so at most two RMRs. L5 and L6 are one write each. It remains to count the misses of the reads of L4. A read misses only if $slot[i]$ was written by another process since the previous access of $p$ to it (with padding, no write to another slot touches its line). Which steps write $slot[i]$ while $p$ waits, from its L1 to its last read of L4?

- L5 steps write the slot of their own place. The only other ticket with place $i$ that can be in its entry section is $m - n$ or $m + n$. Ticket $m + n$ is created only after $m$ is released, by part 1 of Lemma 2. Ticket $m - n$ was released before the L1 of $p$, because at that time the held tickets are an interval that contains $m$ and has at most $n$ elements. So no L5 step of another process writes $slot[i]$ while $p$ waits.
- L6 steps of ticket $j$ write $slot[(j + 1) \bmod n]$. This is $slot[i]$ only if $j \equiv m - 1 \pmod n$, and the only such ticket that is held while $p$ waits is $m - 1$. Its L6 writes $slot[i]$ once.

So the reads of L4 miss at most twice: at the first read, and at the first read after the L6 of ticket $m - 1$. The total is at most $2 + 2 + 1 + 1 = 6$. $\square$

If all slots share one cache line, every L5 and L6 step of every process invalidates the line in the cache of $p$, and there are up to $2(n - 1)$ such steps while $p$ waits. Then the bound is $O(n)$, and the test file measures $2n + 2$ in a round robin run.

**Lemma 7 (DSM model).** In the DSM model, with $slot[i]$ in the memory module of process $i$, a passage has no bound on its remote references.

*Proof.* Take two processes. In a passage in which process 0 gets place 1, every read of L4 by process 0 is remote. Let process 1 stay in its critical section for any number of steps of process 0 in that time. Then the passage of process 0 makes that many RMRs. The test file finds an unbounded passage for $n = 2$. $\square$

Lemmas 3, 4 and 5 show that Anderson's lock solves the mutual exclusion problem with FIFO order and starvation freedom, and Lemmas 6 and 7 give its RMR costs. $\blacksquare$
