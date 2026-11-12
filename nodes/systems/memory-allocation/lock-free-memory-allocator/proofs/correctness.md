---
title: With the tag, the lock-free allocator never hands out a block twice
proves: [correctness]
status: full
---

We prove safety and lock-freedom for the model of the page, in which memory is sequentially consistent and each step of a thread is one read, write or CAS of shared memory. Fix a superblock with descriptor $d$ and $M$ blocks. At any moment let $H$ be the set of its blocks held by the program, let $R$ be the number of blocks reserved for it (the credits plus one, if some heap's Active field names $d$, plus one for each thread that has passed its CAS at L2 or L10 on $d$ and has not yet passed its CAS at L5 or L11), and let $L$ be the list that starts at $d.\mathit{Anchor}.\mathit{avail}$ and follows the first words of blocks.

**Invariant I.** As long as $d$'s superblock has not been given back: (I1) the first $\mathit{count} + R$ elements of $L$ are distinct blocks, none of them in $H$; (I2) $\mathit{count} + R + |H| = M$, except during a FREE, between the moment the program gives the block up and the CAS at L15, when the freed block is in none of the three places.

**Lemma 1 (reservation).** When a thread passes the CAS at L2 or L10 on $d$, the list $L$ has a block for it: $\mathit{count} + R \ge 1$ counts it, and $d$ cannot become EMPTY until that thread's pop succeeds.

*Proof.* The CAS at L2 succeeds on an Active field with $c \ge 0$ credits, which by definition reserved $c + 1$ blocks; it turns one of them into the reservation of this thread, so $R$ does not change. The CAS at L10 moves $m + 1$ blocks from count to reservations, which is allowed since $m + 1 \le a.\mathit{count}$ when $a.\mathit{state}$ is PARTIAL. FREE makes $d$ EMPTY only when $\mathit{count} = M - 1$ before its CAS, so all $M - 1$ other blocks are counted as unreserved and none is reserved; a thread with a reservation would make $R \ge 1$ and contradict (I2). $\square$

**Lemma 2 (pop with the tag).** Let a thread with a reservation read $a = d.\mathit{Anchor}$ at L3 and $\mathit{next}$ from block $a.\mathit{avail}$, and let its CAS at L5 succeed. Then at the moment of the CAS, $a.\mathit{avail}$ is the head of $L$, it is not in $H$, and $\mathit{next}$ is the second element of $L$.

*Proof.* The CAS succeeds only if the anchor equals $a$, tag included. Every successful pop increments the tag, and tags are not reused in the model (the paper's 42-bit tag makes a full wrap practically impossible). So no pop succeeded between the read at L3 and the CAS. Only pops and frees change avail. A FREE sets avail to its own block, which is held until the call, so it differs from $a.\mathit{avail}$, which was free; after that, only a pop could bring avail back to an older head. Since there was no pop and avail is $a.\mathit{avail}$ again at the CAS, no FREE happened either. The CAS steps at L8 and L10 change only count and state. So the list $L$ did not change between the two steps, and the first word of $a.\mathit{avail}$, which only a FREE of that block writes, still holds $\mathit{next}$. $\square$

Without the tag the argument breaks at the first step: pops of $a.\mathit{avail}$ and $\mathit{next}$, followed by frees that bring back the same avail and count, give an anchor equal to $a$ while $\mathit{next}$ is held. The tests run such a schedule and observe a block handed out twice.

**Lemma 3 (I is kept).** Each successful CAS on $d.\mathit{Anchor}$ keeps I.

*Proof.* A pop (L5 or L11) removes the head of $L$, which by Lemma 2 is the block it returns, and ends one reservation: $R$ drops by 1 and $|H|$ grows by 1 when the block reaches the program. If it also takes $m$ credits (L4), count drops by $m$ and $R$ grows by $m$ once UPDATE-ACTIVE runs; if UPDATE-ACTIVE fails at L7, L8 adds the $m$ blocks back to count. Between these steps the $m$ blocks are counted as reserved by the thread that holds them. A FREE (L15) pushes its block on $L$ with its first word set to the old head, and adds 1 to count, or, when $\mathit{count} = M - 1$, sets EMPTY, after which all $M$ blocks are free and the superblock is given back. The reservation CAS at L10 moves blocks from count to reservations. In each case the first $\mathit{count} + R$ elements of $L$ are still the free, unheld blocks. $\square$

**Theorem 1 (safety).** In every schedule of the model with the tag, no block is handed to the program while the program holds it, and no thread reads a superblock that has been given back.

*Proof.* By induction on the steps, with Lemmas 1 to 3, I holds for every superblock. A malloc returns a block only after a successful pop, which by Lemma 2 takes a block outside $H$. A new superblock from L12 is private until L13 publishes it with block 0 already removed from $L$; if L13 fails, no other thread has seen it. A thread reads the first word of a block only at L3 or L11, after it has a reservation, so by Lemma 1 the superblock is not EMPTY and has not been given back. $\square$

**Theorem 2 (lock-freedom).** If some threads take infinitely many steps, then infinitely many calls finish.

*Proof.* Every loop in MALLOC and FREE repeats only after a failed CAS, after reading an EMPTY state, or after all three ways to get a block return null. A CAS fails only if another thread changed the word after it was read, which is a successful CAS or write by that thread. Each such success either ends a call or moves it to a later stage, and each call has finitely many stages before it returns: a reservation, one pop, at most one UPDATE-ACTIVE, at most one put into a partial structure. If three null results at L1 repeat, then between them another thread changed Active or a partial structure, which again is progress of another call. So in any infinite schedule some call keeps advancing through stages and finishes infinitely often. No step waits on another thread, so a thread that stops forever cannot stop the others. $\square$

The tests check Theorem 1 on 600 random schedules with up to four threads and three heaps, and at the end of each schedule check I with $R$ computed from the Active fields. They also run schedules in which one thread stops forever in the middle of a call and check that every other thread finishes all its calls. $\blacksquare$
