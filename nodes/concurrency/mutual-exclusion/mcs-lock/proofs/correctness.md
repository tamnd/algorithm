---
title: The MCS lock gives mutual exclusion, FIFO order and starvation freedom, with O(1) remote references per passage in the CC and DSM models
proves: [correctness]
status: full
---

**Setting.** There are $n$ asynchronous processes on a sequentially consistent memory. $tail$ supports read, fetch-and-store (swap) and compare-and-swap, each atomic. Process $p$ uses its own node $p$, with fields $p.locked$ and $p.next$, and only $p$ passes this node to LOCK and UNLOCK. We use the lines L1 to L10 of the page. Critical sections are finite, and a fair run gives infinitely many steps to every process that is not in its remainder section.

**The queue.** Let $Q$ be the sequence of processes defined as follows. A process joins the end of $Q$ at its L2 step. It leaves $Q$ at its successful compare-and-swap at L8, or at its write of L10. The first process of $Q$ is the *head*. A process in $Q$ is in its entry, critical or exit section.

**Lemma 1 (invariant).** At every time:

1. $tail$ is the last process of $Q$, or $nil$ if $Q$ is empty.
2. If $q$ directly follows $p$ in $Q$, then $q$ got $pred = p$ at L2. If $q$ has done L5, then $p.next = q$; if not, then $p.next = nil$.
3. The last process $p$ of $Q$ has $p.next = nil$. (A process does L1 before L2, so it has done L1 when it joins $Q$.)
4. Every process in $Q$ other than the head has $pred \ne nil$, is between L2 and the end of L6, and if it has done L4 and the head has not yet written L10 to it, its flag is true.
5. Only the head can be past L6 (in its critical or exit section).

*Proof.* By induction on the steps. At the start $Q$ is empty and $tail = nil$. We check each step that changes $tail$, a $next$ field, a flag, or $Q$.

- *L1 of $p$.* $p$ is not in $Q$. It writes $p.next = nil$, which matters only for part 3 once $p$ joins.
- *L2 of $p$.* The swap returns the old $tail$, which by part 1 is the last process $r$ of $Q$ or $nil$, and writes $p$. Now $p$ is the last process of $Q$ and $tail = p$ (part 1). If $r \ne nil$, then $p$ follows $r$ with $pred = r$, and $r.next = nil$ by part 3 for $r$, so part 2 holds; $p$ is not the head, so it must be before L6, which it is. If $r = nil$, $Q$ was empty and $p$ is the head. Part 3 holds for $p$ by its L1.
- *L4 of $p$.* $p$ is in $Q$ and not the head (it has $pred \ne nil$; by part 4 the head could have written L10 to it only after reading $p$ from its $next$, which needs L5 of $p$, which comes later). So the flag becomes true and stays true until that L10.
- *L5 of $p$.* It writes $pred.next = p$, where $pred$ is the process before $p$ in $Q$ by part 2. Part 2 now holds with $pred.next = p$.
- *L6 of $p$ reads false.* By part 4 a process that is not the head and has done L4 reads true until the head writes L10 to it. So $p$ is the head when it passes L6. Part 5 holds.
- *Successful CAS at L8 by $p$.* $p$ is past L6, so it is the head by part 5. The CAS succeeds only if $tail = p$, so $p$ is also the last process of $Q$, so $Q = (p)$. After the step, $Q$ is empty and $tail = nil$.
- *Failed CAS at L8 by $p$.* $tail \ne p$, so by part 1 some process $q$ follows $p$ in $Q$. Nothing changes.
- *L10 of $p$.* $p$ is the head. It read $succ \ne nil$ from $p.next$ at L7 or L9. By part 2, $succ$ is the process $q$ that follows $p$ in $Q$. The write clears $q.locked$, and $p$ leaves $Q$, so $q$ becomes the head. Part 4 now allows $q$ to pass L6.

No other step changes $tail$, a $next$ field, a flag or $Q$. $\square$

**Lemma 2 (mutual exclusion).** At most one process is in its critical section at any time.

*Proof.* A process in its critical section is in $Q$ and past L6 (or entered at L3 with $pred = nil$, which makes it the head at once). By part 5 of Lemma 1 it is the head, and $Q$ has one head. $\square$

**Lemma 3 (FIFO order).** Processes enter their critical sections in the order of their L2 steps.

*Proof.* $Q$ is ordered by L2 steps. A process leaves $Q$ only as the head (Lemma 1), and only the head enters (Lemma 2). When the head leaves at L10, the next head is its successor in $Q$; when it leaves at L8, $Q$ becomes empty. So the heads, and so the entries, follow the order of $Q$. $\square$

**Lemma 4 (starvation freedom).** In a fair run, every process that runs L2 enters its critical section, and every exit section finishes.

*Proof.* Consider the head $h$ of $Q$. If $h$ is in its entry section, it is past L6 or will pass it: by part 4 it waits only on its own flag, and as the head its flag was cleared by its predecessor's L10 (or it had $pred = nil$ and skips L6). So $h$ enters, and leaves its critical section after a finite number of steps. In the exit section, if L7 returns a process, $h$ writes L10. If it returns $nil$ and the CAS succeeds, $h$ is done. If the CAS fails, a process $q$ follows $h$ in $Q$ by part 1, and $q$ has done L2 but maybe not L5. Between L2 and L5 there is no loop, so $q$ does L5 in a bounded number of its own steps, after which $h$ reads $q$ at L9 and writes L10. So every head leaves $Q$ after a finite time, and by Lemma 3 every process in $Q$ becomes the head. $\square$

**Lemma 5 (remote references in the CC model).** A passage makes at most 8 remote references in the CC model.

*Proof.* In the CC model a write or an atomic step is at most one RMR, and a read is an RMR only if another process wrote the location since the last access of the reader. Entry section: L1, L2, L4 and L5 are at most one each. In L6, $p$ reads $p.locked$, which it wrote itself at L4; the only other write to it during the passage is the single L10 of its predecessor (Lemma 1, part 4). So the reads of L6 miss at most once. That is at most 5. Exit section: the field $p.next$ is written by $p$ at L1 and by at most one other process, its successor, at L5 (Lemma 1, part 2). So the reads of L7 and L9 miss at most once in all. With the CAS of L8 and the write of L10, the exit section makes at most $1 + 1 + 1 = 3$. The total is at most 8. $\square$

**Lemma 6 (remote references in the DSM model).** If the node of each process lives in its own memory module, a passage makes at most 4 remote references in the DSM model.

*Proof.* L1, L4, L6, L7 and L9 access the node of the caller, so they are local. The other steps are L2 and L5 in the entry section and L8 and L10 in the exit section, one access each, so a passage makes at most 4 remote references, whatever the length of the waits. $\square$

Lemmas 2, 3 and 4 show that the MCS lock solves the mutual exclusion problem with FIFO order and starvation freedom, and Lemmas 5 and 6 give the RMR bounds of the page. $\blacksquare$
