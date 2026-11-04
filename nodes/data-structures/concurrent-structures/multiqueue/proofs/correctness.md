---
title: The MultiQueue is a linearizable, deadlock-free relaxed priority queue
proves: [correctness, linearizability, progress]
status: full
---

We use the pseudocode of the page, with $c$ heaps. TRY-LOCK, LOCK and UNLOCK are those of a mutex, and a read of a cached minimum $top$ is one atomic read. The specification is the relaxed priority queue on a multiset $Q$: insert$(x)$ adds $x$; delete-min removes and returns any item of $Q$, and may return EMPTY only if $Q$ is empty.

**Lemma 1 (heaps).** Each heap is changed only by a thread that holds its lock. So, between two changes, each heap is a valid min-heap and its cached minimum is its smallest item, or $+\infty$ if it is empty, at every moment when no thread holds its lock.

*Proof.* The changes are the push at line L2 and the pops at lines L9 and L12. Line L2 runs after the successful TRY-LOCK of line L1 and before line L3. Line L9 runs after the successful TRY-LOCK of line L8 and before the UNLOCK in the same line. Line L12 runs after line L11 has taken every lock and before line L13. Each change is a sequential heap operation followed by an update of $top$, done by the only thread in the heap, so it keeps the heap valid and $top$ correct. $\square$

**The abstraction.** At each moment, $Q$ is the multiset union of the heaps.

**Theorem (linearizability).** Each history of the MultiQueue is linearizable with respect to the relaxed priority queue.

*Proof.* Choose the points: an insert at its push at line L2; a delete-min that returns an item at its pop at line L9 or line L12; a delete-min that returns EMPTY at line L12. Each point is inside its call. Pending calls that have passed their point are completed with their result; the others are removed. The order of the points respects real time.

Only the steps at these points change the heaps, so $Q$ changes only there. The push at line L2 adds $x$ to one heap, so it adds $x$ to $Q$. The pop at line L9 is done after the check that the heap is not empty, under its lock, so it removes an item that is in $Q$ at that moment and returns it. The pop at line L12 likewise. At line L12, if all heaps are empty, the thread holds every lock, so no heap can change at that moment, and $Q$ is empty: EMPTY is allowed. Replaying the points in order therefore gives a legal sequential history of the relaxed specification with the same results. $\square$

**Theorem (progress).** The MultiQueue is deadlock-free: if every thread keeps taking steps and some call is pending, some call finishes. Inserts and the fast path of delete-min (lines L4 to L10) never wait for a lock; they only try one.

*Proof.* Suppose that, from some moment $\tau$ on, no call finishes. We derive a contradiction in four steps.

1. *Single locks.* A thread whose TRY-LOCK succeeds at line L1, or at line L8 on a nonempty heap, finishes its call within a constant number of its own steps. So after $\tau$ no such TRY-LOCK succeeds, and from some $\tau_1 \ge \tau$ on no thread holds a lock that it got at line L1, or at line L8 on a nonempty heap.

2. *Stale tops.* After $\tau$ no pop happens, since a pop is followed within a constant number of steps by the end of the call. So every top read after $\tau$ is exact until the next push, and pushes happen only at line L2, which does not happen after $\tau_1$. A delete-min that reads both tops after $\tau_1$ either sees two empty heaps and goes to the scan, or locks a heap that is nonempty if its TRY-LOCK succeeds. So from some $\tau_2 \ge \tau_1$ on, no thread holds a lock that it got at line L8 either.

3. *Scans.* After $\tau_2$ every held lock belongs to a scan. Scans take locks in increasing index order and never release one before line L13. Take the scan that holds the largest index. Every lock it still needs has a larger index, so no scan holds it, and after $\tau_2$ no other thread does: its next attempts succeed, and it finishes. This contradicts the assumption, unless from some $\tau_3 \ge \tau_2$ on no scan holds any lock.

4. *The end.* After $\tau_3$ no lock is held at all. So the next attempt of any pending call at line L1, line L8 or line L11 succeeds, and by steps 1 to 3 that call finishes.

Each case contradicts the assumption. $\blacksquare$
