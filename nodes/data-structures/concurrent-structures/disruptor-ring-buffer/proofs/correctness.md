---
title: The Disruptor ring buffer is a linearizable bounded broadcast channel
proves: [correctness, linearizability, progress]
status: full
---

We use the pseudocode of the page, with ring size $N$. Every read and write of one sequence number, and the fetch-and-add of line L1, is atomic, and reads see the last write (sequential consistency of the shared words). Each consumer $c$ is one thread, so its calls of CONSUME do not overlap; it is the only writer of $c.seq$. The dependency graph of the consumers has no cycle. Let $x_s$ be the item of the producer that got $s$ at line L1.

**Lemma 1 (monotone sequences).** $R.claim$, $R.cursor$ and every $c.seq$ never decrease. The cursor takes the values $-1, 0, 1, 2, \ldots$ in this order, and $R.cursor \ge s$ holds exactly from the moment the producer of $s$ runs line L5.

*Proof.* Line L1 only adds. A producer with number $s$ sets the cursor to $s$ at line L5 only after it has read the value $s - 1$ at line L4, and no other producer can write the cursor in between: a write of $s'$ needs the value $s' - 1$, the numbers are distinct, and the only producer that waits for the value $s - 1$ is the one with $s$. So each write raises the cursor by 1. Consumer $c$ sets $c.seq$ at line L9 to $a \ge next = c.seq + 1$, read at line L6, and nobody else writes $c.seq$ between lines L6 and L9. $\square$

**Lemma 2 (reads of a minimum).** If a thread reads several monotone words one after another and computes the minimum $m$ of the values, then $m$ is at most the true minimum of the words at the time of the last read.

*Proof.* Each value read is at most the current value of its word at every later time, so the minimum of the values is at most the minimum of the current values at the time of the last read. $\square$

**Lemma 3 (invariant).** At all times, for each consumer $c$ and each $d \in c.deps$, $c.seq \le d.seq \le R.cursor$. Also, a producer passes line L2 with number $s$ only when $s - N \le c.seq$ for all consumers $c$.

*Proof.* The value $a$ written at line L9 is at most the cursor and each $d.seq$ at the time of the reads of line L7 (Lemma 2 for the minimum), and by Lemma 1 these values only grow until line L9. So the inequalities hold after each write of $c.seq$, and writes of other words only make them easier. The last claim is the condition of line L2 together with Lemma 2. $\square$

**Lemma 4 (slots).** If a consumer $c$ reads slot $s \bmod N$ at line L8 in a call with $next \le s \le a$, it reads $x_s$.

*Proof.* At line L7, $c$ read a value at least $a \ge s$ from the cursor, so by Lemma 1 the producer of $s$ has run line L5, and hence line L3 before it: the slot got $x_s$. The only later writes to this slot are by producers of $s + kN$ with $k \ge 1$ at line L3, after they passed line L2. By Lemma 3, that needs $s + kN - N \ge s$ to be at most $c.seq$ at some time, so $c.seq \ge s$. But during this call $c.seq = next - 1 < s$ until line L9, which comes after line L8. So the slot still holds $x_s$ when $c$ reads it. $\square$

**The abstraction.** At each moment, let $P$ be the list $x_0, \ldots, x_{R.cursor}$, and $pos_c = c.seq + 1$. Initially $P$ is empty and every $pos_c = 0$. Only line L5 changes $P$, and only line L9 changes $pos_c$.

**Theorem (linearizability).** Each history of the ring buffer is linearizable with respect to the sequential broadcast channel of the page.

*Proof.* Linearize each publish that has run line L5 at that step, and each consume that has run line L9 at that step; remove other pending calls. Each point lies inside its call, so the order of the points extends real-time order. We show that, at each point, the abstract operation is allowed and gives the same change and result.

A publish with number $s$ at line L5. By Lemma 1, before this step $R.cursor = s - 1$, so $|P| = s$, and the step appends $x_s$, the abstract publish, with result $s = |P| - 1$ after the append. The abstract precondition $|P| - \min_c pos_c < N$, that is $s - N \le \min_c c.seq$, held when the producer passed line L2 (Lemma 3), and it still holds at line L5 because every $c.seq$ only grows.

A consume of $c$ at line L9, with $next$ and $a$ as in the code. Then $pos_c = next$ before the step, and $a \ge next$. At line L7, $a$ was at most the cursor and every $d.seq$ for $d \in c.deps$ (Lemma 2), and these only grow, so at line L9 $a + 1 \le |P|$ and $a + 1 \le pos_d$. So the abstract consume may choose the end $a + 1$, and it sets $pos_c$ to $a + 1$, as line L9 does. By Lemma 4 the batch returned is $x_{next}, \ldots, x_a$, which is $P[pos_c .. a]$, the abstract result. $\square$

**Theorem (progress).** No thread holds a lock. A thread waits only at line L2, line L4 or line L7, and:

1. A consume of $c$ at line L7 passes within $O(|c.deps|)$ of its own steps after a moment from which the abstract consume of $c$ is allowed, that is, $\min(|P|, \min_{d \in c.deps} pos_d) > pos_c$.
2. A publish at line L2 passes within $O(k)$ of its own steps, for $k$ consumers, after a moment from which the gate condition $s - N \le \min_c c.seq$ holds; with one producer this is exactly the abstract condition that the ring is not full.
3. A publish with number $s$ waits at line L4 only until the producers of all smaller numbers have run line L5. With one producer, it never waits at line L4.
4. So with one producer, every call finishes within $O(k + b)$ of its own steps, where $b$ is the batch size, once its abstract operation is allowed: the structure is wait-free apart from the waits that the abstract type itself demands.

*Proof.* Part 1: from that moment on, each reading of line L7 gives a minimum of at least the values at its first read, which by Lemma 1 are at least those at the moment, so the test passes on the next round, after $O(|c.deps|)$ steps. Lines L8 to L10 take $O(b)$ steps. Part 2 is the same argument for line L2. With one producer, $R.claim = |P|$ while the producer is outside a call, so $s = |P|$ and the gate condition is the abstract condition. Part 3 is Lemma 1: the cursor reaches $s - 1$ when the producer of $s - 1$ runs line L5, and by induction this needs the producers of all smaller numbers. With one producer, all smaller numbers were published by its earlier calls. Part 4 combines parts 1 to 3.

With many producers the structure is blocking: a producer that stops between lines L1 and L5 stops all producers with larger numbers at line L4, and, once the ring fills, all consumers at line L7. If no thread stops and every consumer keeps calling CONSUME, every publish finishes. Take the smallest pending number $s$. All smaller numbers are published, so $R.cursor = s - 1$ and the producer of $s$ waits only at line L2. Go through the consumers in an order in which each comes after its dependencies, which exists since the graph has no cycle. A consumer with no dependencies sees the cursor at $s - 1$ and, by part 1, reaches $c.seq = s - 1$ within its next calls; a consumer whose dependencies have all reached $s - 1$ does the same. So every $c.seq$ reaches $s - 1 \ge s - N$, the gate opens, and by part 2 and part 3 the publish of $s$ finishes. By induction on $s$ every publish finishes. $\blacksquare$
