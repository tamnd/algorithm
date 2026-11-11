---
title: The Herlihy-Wing queue is linearizable, and its enqueue has no fixed linearization point
proves: [correctness, linearizability, progress]
status: full
---

We use the pseudocode of the page, with asynchronous processes that may crash, atomic read, write, fetch-and-add and swap, sequential consistency, an infinite array, and distinct items. The sequential specification is the FIFO queue in which deq is enabled only on a non-empty queue. We write $\mathrm{slot}(a)$ for the index that the FAA of enq($a$) returned. The linearizability proof uses one cited theorem, stated below; the rest is proved here.

**Lemma 1.** (a) Distinct enqueues get distinct slots, and $\mathrm{slot}(a) < \mathrm{slot}(b)$ if and only if the FAA of enq($a$) comes before the FAA of enq($b$). (b) Each slot is written by at most one store, the store of the enqueue that owns it. (c) A swap returns either NONE or the item of the owner of its slot, and for each slot at most one swap returns an item, and only after the store.

*Proof.* (a) is the definition of fetch-and-add: the values it returns are $0, 1, 2, \ldots$ in the order of the steps. (b) follows from (a), since a store writes only the slot that its own FAA returned. (c) A slot holds NONE until its owner stores its item, and after that only swaps change it, each to NONE. The first swap after the store returns the item, and every later swap returns NONE, since nobody writes the slot again. ∎

**Cited theorem (Henzinger, Sezgin and Vafeiadis, CONCUR 2013).** Let $H$ be a history of a queue in which each item is enqueued at most once and no dequeue returns EMPTY. Then $H$ is linearizable with respect to the FIFO queue if none of these three patterns occurs in $H$ (or in a completion of $H$):

- **(VFresh)** a dequeue returns an item that no enqueue in $H$ has as argument;
- **(VRepet)** two dequeues return the same item;
- **(VOrd)** enq($a$) responds before enq($b$) is invoked, some dequeue $d_b$ returns $b$, and either no dequeue returns $a$, or the dequeue $d_a$ that returns $a$ is invoked after $d_b$ responds.

**Theorem 1 (linearizability).** Each history $H$ of the queue is linearizable.

*Proof.* Complete $H$ by letting each pending dequeue that has done a swap that returned an item respond with that item (its next step is the return at L7), and by dropping the other pending dequeues; pending enqueues stay pending. (VFresh) and (VRepet) do not occur, by Lemma 1(c): a swap returns only an item that its owner stored, and each item at most once.

For (VOrd), let enq($a$) respond before enq($b$) is invoked, and let $d_b$ return $b$. The store of $a$ comes before the FAA of $b$, and so does the FAA of $a$; by Lemma 1(a), $\mathrm{slot}(a) < \mathrm{slot}(b)$. Consider the scan of $d_b$ that took $b$. It read `back` at L4 and then visited slots $0, 1, \ldots$ up to $\mathrm{slot}(b)$, so the value it read was larger than $\mathrm{slot}(b)$, and the read came after the FAA of $b$, and so after the store of $a$. The scan swapped slot $\mathrm{slot}(a)$ before slot $\mathrm{slot}(b)$, and it got NONE there, since it did not return $a$. The store of $a$ came before this swap, so by Lemma 1(c) an earlier swap, of some dequeue $d_a$, returned $a$. That swap is a step of $d_a$ that comes before a step of $d_b$, so $d_a$ is invoked before $d_b$ responds. So (VOrd) does not occur. By the cited theorem, $H$ is linearizable. ∎

**Theorem 2 (no fixed linearization point).** There is no rule that assigns to each enqueue one fixed step of its own (always the FAA, or always the store) as a linearization point that works for all runs.

*Proof.* Take the prefix $P$: $p$ does the FAA of enq($x$) and gets slot 0; then $q$ runs enq($y$), with its FAA (slot 1) and its store, and enq($y$) responds. Extend $P$ in two ways. Run 1: a dequeuer reads `back` $= 2$, swaps slot 0 (NONE) and slot 1 ($y$), and returns $y$; then $p$ stores $x$; then a second dequeue returns $x$. Run 2: $p$ stores $x$; then the dequeuer returns $x$ from slot 0, and then $y$ from slot 1. In any linearization, the two enqueues come in the order of the dequeues that return their items. So Run 1 needs enq($y$) before enq($x$), and Run 2 needs enq($x$) before enq($y$). The point of enq($y$) is in $P$ in both runs, since enq($y$) completed in $P$.

If the rule picks the FAA, then in Run 1 the point of enq($x$) is the first step of the run, before both steps of enq($y$), so enq($x$) comes first, which Run 1 forbids. If the rule picks the store, then in Run 2 the point of enq($x$) is after $P$, so after the point of enq($y$), and enq($y$) comes first, which Run 2 forbids. ∎

**Theorem 3 (progress).** (a) Each enqueue completes in exactly 2 of its own steps. (b) There is a run with infinitely many steps and no completed operation, so the queue is not lock-free. (c) If from some time on there is always an item that is stored and not yet taken, and some dequeue keeps taking steps, then some dequeue completes.

*Proof.* (a) is the code. (b) One process calls deq on an empty queue and nobody else runs: each scan reads `back` $= 0$ and finds nothing, for ever. (c) Let $T$ be such a time and $d$ a dequeue that keeps running. Each of its scans is finite, since it visits $r$ slots for the value $r$ it read. Take a scan of $d$ that starts after $T$, and an item $a$ that is stored and not taken when the scan reads `back`. That read comes after the FAA of $a$, so the scan visits the slot of $a$. When it does, either $a$ is still there, and $d$ takes it and returns, or some other dequeue took $a$ in between, and that dequeue returns at L7 right after its swap. ∎

The progress in (c) is per object, not per operation: one dequeue can lose each race and never return, as the page shows.
