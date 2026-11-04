---
title: The LCRQ is a linearizable, lock-free FIFO queue
proves: [correctness, linearizability, progress]
status: full
---

We use the pseudocode of the page. Reads, the fetch-and-add and the closing of a tail word, the fetch-and-add of a head word, the CAS2 of a cell and the CAS of a pointer are atomic. Items are distinct (tag them with the enqueue that made them). The specification is the sequential FIFO queue, where dequeue returns EMPTY on an empty queue.

## Part 1: one CRQ

Fix a CRQ $C$ with ring size $R$. An *enqueue attempt with ticket* $t$ is one round of lines L1 to L6 whose fetch-and-add returned $t$ with the bit open; a *dequeue attempt with ticket* $h$ is one round of lines L7 to L14. Tickets are distinct for each counter, since fetch-and-add hands out each value once. A cell $i$ serves tickets $i, i + R, i + 2R, \ldots$; its *round* is its $idx$.

**Lemma 1 (cells move forward).** Every successful CAS2 on cell $i$ keeps $idx \equiv i \pmod R$ and either raises $idx$ or keeps $idx$ and changes $(safe, val)$ in one of two ways: $\bot \to x$ with $safe$ set to 1 (line L5, which may also raise $idx$), or $safe$ from 1 to 0 with the same item (line L11). A cell never returns to a state it had before, so a CAS2 that succeeds compares against the state that was read, with no ABA.

*Proof.* Line L5 replaces $(s, idx, \bot)$ by $(1, t, x)$ with $idx \le t$ and $t \equiv i$. Lines L10 and L12 set $idx$ to $h + R > idx$, since $idx \le h$ there (line L9 exits otherwise). Line L11 only clears $safe$. For a fixed $idx$, the state can go from $\bot$ to an item once (afterwards line L5 needs $\bot$, and the only way back to $\bot$ is lines L10 and L12, which raise $idx$), and from $safe = 1$ to $0$ once. So the sequence of states of the cell is strictly increasing in the order (idx, then val set, then safe cleared, the latter two in either order), and no state repeats. $\square$

**Lemma 2 (who takes an item).** An item stored by the enqueue attempt with ticket $t$ (line L5, giving $idx = t$) is removed from its cell only by line L10 of the dequeue attempt with ticket $t$.

*Proof.* Only line L10 removes an item, and it requires $idx = h$. After line L5 the $idx$ stays $t$ until the item is removed (only lines L10 and L12 raise it, and line L12 needs $\bot$). So $h = t$. $\square$

**Lemma 3 (tickets match).** Let $E$ be an enqueue attempt with ticket $t$ and let $D$ be the dequeue attempt with ticket $t$, if any.
(a) If $E$ stores its item, then $D$, if it runs line L8 at all, returns that item.
(b) If $D$ exits its inner loop without an item, then $E$ does not store, either before or after.

*Proof.* Consider the moment when cell $c = t \bmod R$ first has $idx > t$, or first holds the item of ticket $t$; one of these happens before either attempt can succeed with ticket $t$, and by Lemma 1 they cannot both precede each other.

(a) Suppose $E$ stored, so $c = (\cdot, t, x)$ from that CAS2 on. By Lemma 1 the $idx$ of $c$ stays $t$ until $x$ is removed, and by Lemma 2 only $D$ removes it. When $D$ reads the cell, either the item is there with $idx = t = h$, and line L10 is tried; a failed CAS2 means the cell changed, which only $D$ itself or line L11 can cause (clearing $safe$ keeps $idx$ and $x$), so $D$ retries and eventually succeeds, since line L11 succeeds at most once. Or the cell is earlier than $E$'s CAS2 in Lemma 1's order, with $idx \le t$; then $D$ tries line L11 or L12. Line L12 with $idx \le t$ and $\bot$ would raise $idx$ above $t$ before $E$'s CAS2, which then fails, a contradiction; so that CAS2 of $D$ fails, and $D$ rereads. Line L11 needs an item of an older round, $idx < t$. A success of line L11 makes $D$ give up, so we must exclude it: after it, the cell holds an item with $idx < t$ and $safe = 0$, and when its dequeuer takes it, the cell becomes $(0, t, \bot)$ (line L10 gives $idx + R = t$, the only round between). Now $E$ can store only through line L4 with $s = 0$, which needs $head \le t$; but $D$ took ticket $t$ before line L11, so $head > t$ from then on. So $E$ cannot store after the success of line L11, and it did not store before it, since the cell then held an older item. This contradicts the assumption that $E$ stored, so line L11 does not succeed for $D$, and $D$ returns $x$.

(b) $D$ exits in three ways. By line L9, the cell had $idx > t$; by Lemma 1 it keeps $idx > t$, and $E$'s line L4 or L5 fails from then on; and $E$ did not store before, since then $idx$ would have stayed $t$ until $D$ removed the item. By line L12, the same holds from that CAS2 on. By line L11, the argument of (a) shows that $E$ cannot store afterwards, and it did not store before, since the cell held an older item until then and line L5 needs $\bot$. $\square$

**Lemma 4 (closed means closed).** Once the closed bit of $C.tail$ is set, every later attempt returns CLOSED at line L2 and stores nothing. FIX-STATE never clears the bit.

*Proof.* The bit is cleared by no step: fetch-and-add keeps it, and line L15 CASes only from an open tail to an open tail. $\square$

**Lemma 5 (empty).** If a dequeue attempt with ticket $h$ reads at line L13 a tail counter $t_\varepsilon \le h + 1$ at time $\tau$, then every enqueue attempt that has taken a ticket $t$ before $\tau$ has $t \le h$, and each such attempt with $t < h$ has a dequeue attempt with ticket $t$ that took its ticket before $\tau$.

*Proof.* The tail counter only grows, except at line L15, which sets it to the head counter when that is larger. The tickets handed out so far are below the current counter $t_\varepsilon$, so $t \le h$. The head counter was above $h \ge t$ at $\tau$, so every ticket below $h$ has been taken by a dequeue attempt. $\square$

**Linearization of a CRQ.** Call an enqueue attempt *successful* if it stores. Define the points:

- A successful enqueue attempt with ticket $t$: $L(E_t)$ = its fetch-and-add at line L1. For a CRQ created at line L18 with its first item, the item has ticket 0 and its point is defined in Part 2.
- A dequeue that returns the item of ticket $t$: $L(D_t) = \max(F^D_t, F^E_t, L(D_{t'}))$, where $F^D_t$ and $F^E_t$ are the fetch-and-adds of the two attempts and $t'$ is the largest successful ticket below $t$; when several points coincide, enqueues come first, then dequeues in ticket order.
- A dequeue that returns EMPTY: its read of the tail at line L13, at time $\tau$.

Each point is inside its call: $L(D_t)$ is at or after $F^D_t$, and before the return of $D_t$, since $D_t$ returns only after $E_t$ stored (after $F^E_t$) and, by induction, after $L(D_{t'})$ (the item of $t'$ is taken by the attempt with ticket $t' < t$, which got its ticket before $D_t$; if $D_{t'}$ has not returned yet, its point is at most the later of its own two fetch-and-adds and the point before it, all of which precede the return of $D_t$, as each of them is a fetch-and-add that handed out a smaller ticket than $F^D_t$ or $F^E_t$, and so happened earlier).

**Theorem 1 (a CRQ is a linearizable queue that may refuse enqueues).** In the order of the points, the enqueues are in ticket order, the dequeues that return items are in ticket order, each item is dequeued after it is enqueued, and at every EMPTY point all enqueued items have been dequeued. So the sequence is a legal history of a FIFO queue.

*Proof.* Enqueue points are fetch-and-adds on the tail, so they are in ticket order. Dequeue points are in ticket order by their definition. $L(D_t) \ge F^E_t = L(E_t)$, and ties put enqueues first. Since enqueues and dequeues of items are both in ticket order and Lemma 3 pairs each item with the dequeue of its own ticket, the $k$-th dequeue returns the $k$-th enqueued item: before $L(D_t)$ all successful enqueues with tickets below $t$ are linearized (for $t'' < t$, the fetch-and-add $F^E_{t''}$ is before $F^E_t$, since the tail hands out tickets in increasing order), and those with tickets above $t$ that are linearized before $L(D_t)$ come after the item of $t$ in the queue. So $D_t$ removes the front.

For an EMPTY at $\tau$ with ticket $h$: by Lemma 5, each enqueue linearized before $\tau$ has ticket $t \le h$. Its ticket is not $h$: the attempt with ticket $h$ cannot store by Lemma 3(b). For $t < h$, the dequeue attempt with ticket $t$ took its ticket before $\tau$, and by Lemma 3(a) it returns the item; its point $\max(F^D_t, F^E_t, L(D_{t'}))$ is before $\tau$ by induction on $t$, since both fetch-and-adds were before $\tau$. So every item enqueued before $\tau$ is dequeued before $\tau$, and the queue is empty at $\tau$. If $\tau$ ties with a dequeue point, that point is a fetch-and-add, which is a different step; there are no ties. Pending calls: a pending enqueue that stored is kept, and a pending dequeue whose ticket matches a stored item is completed with that item (Lemma 3(a)); the others are removed. $\square$

## Part 2: the list of CRQs

**Lemma 6 (the list).** (a) $C.next$ changes once, from NIL, by line L18, and only after $C$ is closed. (b) $Q.tail$ and $Q.head$ move only to the next CRQ in the list. (c) $Q.head$ moves from $C$ only after some dequeue saw $C.next \ne$ NIL and then had an attempt on $C$ return EMPTY.

*Proof.* (a) Line L18 runs only after CRQ-ENQUEUE returned CLOSED, which happens after the bit was set, by the caller or another thread (lines L2 and L6). (b) and (c) by lines L16 and L22. $\square$

**The abstract queue.** Let $Q$ be the concatenation, in list order from $Q.head$ to the end, of the CRQ queues of Theorem 1. For a CRQ $N$ created at line L18 with item $x$, linearize the enqueue of $x$ at the CAS of $C.next$ that links $N$; this is inside the call.

**Theorem 2 (linearizability).** The LCRQ is linearizable with respect to the sequential FIFO queue.

*Proof.* Use the points of Theorem 1 for each CRQ, and the CAS of $C.next$ for first items. Every enqueue call is linearized once: its last attempt stored, or its CAS at line L18 linked its CRQ; earlier attempts returned CLOSED and did nothing (Lemma 4). Every dequeue call that returns an item is linearized at the point of its last attempt.

Items enter $Q$ at the end: an enqueue that stores into $C$ does so while $C$ is open, so while $C.next$ is NIL by Lemma 6(a), and $C$ is then the last CRQ. A new CRQ is appended only after $C$ is closed, so no item enters $C$ afterwards. So the order of enqueue points is the order of items in $Q$.

Items leave $Q$ at the front: a dequeue attempt on $C$ returns an item of $C$, the front of $C$ by Theorem 1. All CRQs before $C$ in $Q$ are empty at that point: $Q.head$ moved past each of them only after a drain (Lemma 6(c)) that returned EMPTY after their $next$ was set, so after they were closed, and a closed CRQ that was empty at a point stays empty (no more items enter it by Lemma 4). So the item is the front of $Q$.

An LCRQ EMPTY is returned at line L20 after an attempt on $C$ returned EMPTY at its point $\tau$, and $C.next$ was NIL at a later read. At $\tau$, $C$ is empty, CRQs before $C$ are empty as above, and there is no CRQ after $C$, since $C.next$ was still NIL later. So $Q$ is empty at $\tau$. Since all points are inside their calls, real time is respected. $\square$

## Part 3: progress

**Theorem 3 (lock-freedom).** In every infinite execution in which some operation is pending, infinitely many operations finish.

*Proof.* Suppose that from some moment on no operation finishes. Each attempt of CRQ-ENQUEUE or CRQ-DEQUEUE finishes in a bounded number of its own steps, except for the retries of the inner loop of lines L8 to L12 and of FIX-STATE. A retry of lines L8 to L12 happens only after a CAS2 failed, so after another CAS2 on the same cell succeeded, and by Lemma 1 a cell has at most two changes per round before its round grows; a round grows only through a dequeue ticket of that round, and tickets are only handed out by fetch-and-adds, each a step of an attempt. FIX-STATE retries only if the tail changed, which also needs another step to succeed. So infinitely many attempts are made.

Enqueue side: each CRQ-ENQUEUE call returns CLOSED after at most $patience$ failed tries (line L6), so each call makes finitely many tries per CRQ. If a call gets CLOSED, it either links a new CRQ and finishes, or its CAS of line L18 fails because another call linked one, and that call then finishes after one more step, or $Q.tail$ moves on and it tries the new CRQ. So infinitely many enqueue tries without a finished enqueue are impossible: with finitely many threads, some enqueue would close a CRQ and link a new one, and finish.

Dequeue side: a dequeue attempt that does not return an item finds $t > h + 1$ at line L13 and retries; this means an enqueue attempt took a ticket above $h + 1$. Infinitely many such retries need infinitely many enqueue tickets, which the enqueue side excludes from some moment on (no enqueue tries without finished enqueues means no tickets). After that, the next attempt of a dequeue sees $t \le h + 1$ and returns EMPTY, or returns an item. At line L20, a dequeue either returns EMPTY or moves to the next CRQ; there are finitely many CRQs, since no new one is linked, so it finishes. Both contradict the assumption. $\blacksquare$
