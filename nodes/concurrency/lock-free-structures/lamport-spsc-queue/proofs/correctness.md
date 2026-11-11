---
title: The Lamport queue is linearizable and wait-free under sequential consistency
proves: [correctness, linearizability, progress]
status: full
---

We use the pseudocode of the page, with two asynchronous processes, the producer $p$ (only enq) and the consumer $q$ (only deq), atomic reads and writes, and sequential consistency. Write $T$ and $H$ for the values of `tail` and `head` at a given time.

**Lemma 1 (monotone counters).** Only $p$ writes `tail`, and only $q$ writes `head`. Each write raises the counter by one. So both counters only grow, and a process always knows the current value of its own counter.

*Proof.* The only writes are L4 (by $p$, of $t + 1$ where $t$ is the value $p$ read at L1, which is current, since $p$ is the only writer) and L9 (the same for $q$). ∎

**Lemma 2 (invariant).** At all times $0 \le T - H \le N$.

*Proof.* At the start $T = H = 0$. A write at L4 sets $T$ to $t + 1$, where $t = T$ and the test at L2 saw $t - h < N$ for a value $h$ read at L1. Since $H \ge h$ by Lemma 1, $T - H \le t + 1 - h \le N$ after the write. A write at L9 sets $H$ to $h + 1$, where $h = H$ and the test at L7 saw $t \ne h$ for a value $t$ of `tail` read at L6; by Lemma 1 and the invariant at that time, $t > h$, and $T \ge t$, so $T - H \ge t - h - 1 \ge 0$ after the write. ∎

Call the item written by the enq that set `tail` to $i + 1$ *item $i$*. It is written in slot $i \bmod N$.

**Lemma 3 (slots).** (a) When $q$ reads slot $h \bmod N$ at L8, item $h$ is in that slot. (b) When $p$ writes item $t$ into slot $t \bmod N$ at L3, the consumer has finished its read of item $t - N$ (if $t \ge N$).

*Proof.* (b) At L1, $p$ read $h$ with $t - h < N$, so $h \ge t - N + 1$. So $q$ had written `head` $\ge t - N + 1$ before this read, and its write of `head` $= t - N + 1$ at L9 came after its read of item $t - N$ at L8. (a) At L6, $q$ read $t > h$, so the write of `tail` $= h + 1$ at L4 came before, and it came after the write of item $h$ at L3. Between that write and the read at L8, the only write to the same slot is of item $h + N$, which by (b) comes only after $q$ finishes reading item $h$. ∎

**Theorem 1 (linearizability).** Each history is linearizable with respect to a bounded FIFO queue of capacity $N$.

*Proof.* Take these points: a successful enq at its write at L4; a successful deq at its write at L9; FULL at the read of `head` in L1; EMPTY at the read of `tail` in L6. Each point is a step of the operation, so it lies in its interval. Order the operations by their points; we show that each result is the result of the sequential queue in this order.

We claim that just after each point, the sequential queue holds items $H, H + 1, \ldots, T - 1$ in this order. This holds at the start. At an L4 point, $T$ grows by one and the new item $T - 1$ is the argument of this enq, which joins the back, as in the sequential queue; the sequential queue must not be full, and indeed $T - H < N$ before the step by Lemma 2 and the test at L2. At an L9 point, $H$ grows by one; the deq returns the value it read at L8, which by Lemma 3(a) is item $H$, the front item, and the sequential queue is not empty, since $T > H$. At a FULL point, the read of `head` returns $h = H$ with $T - H = t - h = N$, since $T = t$ (only $p$ writes `tail`), so the sequential queue is full. At an EMPTY point, the read of `tail` returns $t = T$ with $t = h = H$ (only $q$ writes `head`), so the sequential queue is empty. Points of the other kinds do not change $T$ or $H$. ∎

**Theorem 2 (wait-freedom).** Each enq ends in at most 4 of its own steps and each deq in at most 4, whatever the other process does. No step is a read-modify-write step.

*Proof.* The code has no loop and no wait. An enq does 2 reads and returns, or 2 reads and 2 writes. A deq does 2 reads and returns, or 3 reads and 1 write. ∎

**Remark (weak memory).** The proof uses sequential consistency in Lemma 3: in (a), the write at L3 must be visible to $q$ when the write at L4 is; in (b), the read at L8 must be done when the write at L9 is visible to $p$. Release stores at L4 and L9 and acquire loads of the other counter give exactly these two orders, and the rest of the proof does not depend on the order of accesses.
