---
title: The Vyukov queue is a linearizable try queue, its try operations are lock-free, and one stalled producer blocks it
proves: [correctness, linearizability, progress]
status: full
---

We use the pseudocode of the page with its model: asynchronous processes that may crash, atomic read, write and CMPXCHG, sequential consistency, and counters that do not wrap. Position $pos$ uses cell $c(pos) = pos \bmod N$. The *producer of $pos$* is the enq whose CMPXCHG at L6 moved `enqPos` from $pos$ to $pos + 1$; the *consumer of $pos$* is the deq whose CMPXCHG at L17 moved `deqPos` from $pos$ to $pos + 1$. Since a counter changes only by these steps, and each changes it by one, each position has at most one producer and at most one consumer, and `enqPos` and `deqPos` count the claims so far.

**Lemma 1 (cell protocol).** For every position $pos$:

1. `seq` of $c(pos)$ takes the value $pos$ before the producer of $pos$ claims, and keeps it until that producer writes $pos + 1$ at L11;
2. the value $pos + 1$ stays until the consumer of $pos$ writes $pos + N$ at L22;
3. the producer of $pos$ writes `data` at L10 while `seq` $= pos$, and the consumer of $pos$ reads `data` at L21 while `seq` $= pos + 1$.

*Proof.* By induction on time. At the start, cell $i$ has `seq` $= i$, which is the free value for position $i$, $0 \le i < N$. The writes to `seq` are L11 (by the producer of $pos$, value $pos + 1$) and L22 (by the consumer of $pos$, value $pos + N$, the free value for position $pos + N$, which uses the same cell). So the values of one cell, in order, are $i, i + 1, i + N, i + N + 1, i + 2N, \ldots$, provided that each write happens in the right state.

The producer of $pos$ read `seq` $= pos$ at L3 with this $pos$, and then its CMPXCHG found `enqPos` $= pos$. The value $pos$ in $c(pos)$ can be replaced only by the producer of $pos$ (at L11), who has not claimed yet at the read. So at the claim, and until its own L11, `seq` $= pos$; its L10 falls in this time. The same argument for the consumer: it read `seq` $= pos + 1$ at L14 and claimed; only the consumer of $pos$ replaces the value $pos + 1$; so `seq` $= pos + 1$ from the claim until its own L22, and L21 falls in this time. Since `seq` $= pos + 1$ is written only after L10, the consumer reads the item of the producer of $pos$. ∎

**Lemma 2 (bounds).** At all times `deqPos` $\le$ `enqPos` $\le$ `deqPos` $+ N$.

*Proof.* A consumer claims $pos$ only after reading `seq` $= pos + 1$, which requires that the producer of $pos$ has claimed, so `deqPos` $\le$ `enqPos`. A producer claims $pos$ only after reading `seq` $= pos$ in $c(pos)$; for $pos \ge N$ that value was written by the consumer of $pos - N$, which therefore claimed earlier, so after the claim `enqPos` $= pos + 1 \le$ `deqPos` $+ N$. ∎

**Theorem 1 (linearizability as a try queue).** Each history is linearizable with respect to the bounded FIFO queue of capacity $N$ in which enq may return FULL and deq may return EMPTY at any time with no effect.

*Proof.* Put a successful enq at its claim (L6), a successful deq at its claim (L17), and a FULL or EMPTY result at its last read of `seq` (L3 or L14). Each point is a step of the operation. A pending operation that has claimed gets its claim as its point, and its result, if it ever returned, would be the one its point gives; other pending operations are dropped.

Define the abstract state at a time as the items of the positions `deqPos`, ..., `enqPos` $- 1$, in order, where the item of a position is the argument of its producer. A claim at L6 appends the argument of the claimer at the back; by Lemma 2, the queue had fewer than $N$ items before it. A claim at L17 removes the item of position `deqPos`, which is the front; by Lemma 1(3), the consumer returns exactly this item. FULL and EMPTY do not change the counters, and the try queue accepts them in every state. So the order of the points is a legal sequential history with the same results. ∎

**Theorem 2 (not linearizable as a strict queue).** There is a history that is not linearizable with respect to the bounded queue in which deq returns EMPTY only on an empty queue.

*Proof.* The run of the example: $p$ claims position 0 and stops; $q$ completes enq$(0)$ at position 1; then $r$ runs deq(), reads `seq` $= 0$ in cell 0, and returns EMPTY. In any linearization, enq$(0)$ by $q$ comes before the deq of $r$, since it responded first. So the queue is not empty at the point of the deq, whatever is done with the pending enq of $p$. ∎

**Theorem 3 (progress).** (a) Alone, each operation ends in at most 5 steps. (b) The try operations are lock-free: in each infinite run, infinitely many operations end. (c) The queue is not lock-free as a FIFO queue whose dequeue waits for an item: if a producer stops after its claim and before L11, then no consumer gets any item from then on, although later producers may have put up to $N - 1$ items in.

*Proof.* (a) Alone, the first read of the counter is current, so the first iteration either returns FULL or EMPTY (2 steps) or claims (3 steps) and then does 2 more steps.

(b) A loop iteration that does not return either fails its CMPXCHG, so another claim on the same counter succeeded after the read of $pos$, or reads $d > 0$, so `seq` is ahead of $pos$, which by Lemma 1 needs a claim of a position $\ge pos$, so the counter moved past the value $pos$ that this process read. Either way, there is a successful claim between the start of the iteration and its end. In an infinite run with finitely many crashes, an infinite number of failed iterations gives an infinite number of claims, and all but finitely many of them are made by processes that keep running, which end their operation 2 steps after the claim.

(c) Let the producer of $pos$ stop with `seq` $= pos$ in $c(pos)$. By Lemma 2, `deqPos` $\le pos$. Each consumer that reaches position $pos$ reads `seq` $= pos \ne pos + 1$ and returns EMPTY; no consumer can claim $pos$, so `deqPos` never passes $pos$, and no item of a position $> pos$ is ever returned. A producer can claim at most positions $pos + 1, \ldots, pos + N - 1$; position $pos + N$ needs `seq` $= pos + N$ in $c(pos)$, which only the consumer of $pos$ writes. ∎
