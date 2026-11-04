---
title: The two-lock queue is linearizable and deadlock-free
proves: [correctness, linearizability, progress]
status: full
---

We use the pseudocode of the page. The reads and writes of a next pointer, of $Q.head$ and of $Q.tail$ are atomic, and a node gets its value at line L1 before any other thread can reach it. Each lock gives mutual exclusion. Let $L$ be the list of nodes reachable from $Q.head$ by next pointers, and let $\mathrm{abs}$ be the sequence of the values of the nodes of $L$ after $Q.head$. We call an enqueuer that has executed line L3 but not line L4 *open*.

**Lemma 1 (who writes what).** Only an enqueuer that holds $Q.tlock$ writes a next pointer of a node in $L$ (line L3) or $Q.tail$ (line L4). Only a dequeuer that holds $Q.hlock$ writes $Q.head$ (line L11). So at most one thread is open at a time.

*Proof.* These are the only writes of the code to these fields, and each is between the acquire and the release of the named lock. Line L1 writes the fields of a new node that is not yet in $L$. An open enqueuer holds $Q.tlock$, so there is at most one. $\square$

**Lemma 2 (shape).** At each moment: (a) $L$ is finite and acyclic and its last node $\ell$ has next $=$ nil; (b) if no enqueuer is open, $Q.tail = \ell$; (c) if an enqueuer $E$ is open, $\ell$ is the node $n_E$ that $E$ linked, and $Q.tail$ is the predecessor of $n_E$, which is either in $L$ or was the head just before the head moved to $n_E$.

*Proof.* By induction on the steps of the execution. At the start $L$ is the sentinel alone, $Q.tail = Q.head$, and no enqueuer is open. Only the writes of lines L3, L4 and L11 can change the claims (Lemma 1).

- *Line L3 of $E$.* $E$ holds $Q.tlock$ and no enqueuer is open, so by (b) $Q.tail = \ell$ and $\ell.next = $ nil. The write sets $\ell.next = n_E$, a new node with next nil. So $L$ grows by $n_E$ at the end, stays acyclic, $n_E$ is the last node, and $Q.tail$ is its predecessor. Now $E$ is open and (c) holds.
- *Line L4 of $E$.* $E$ is open, so by (c) $\ell = n_E$. The write sets $Q.tail = n_E = \ell$, and $E$ is no longer open, so (b) holds. $L$ does not change.
- *Line L11 of a dequeuer $D$.* $D$ holds $Q.hlock$, so $Q.head$ has not changed since $D$ read it at line L7, and new_head is the value of $Q.head.next$ that $D$ read at line L8. Next pointers in $L$ are written only from nil to a new node (line L3), so this pointer still equals new_head, and new_head $\ne$ nil by line L9. So the write moves the head one node forward along $L$. $L$ loses its first node, is still finite and acyclic, and $\ell$ does not change, because new_head was in $L$. Claim (b) still holds if no enqueuer is open. If $E$ is open and the old head was $Q.tail$, the predecessor of $n_E$, then the new head is $n_E$, and $Q.tail$ was the head just before; this is the second case of (c). $\square$

**Lemma 3 (the atomic effects).** Define the linearization point of each call: line L3 for an enqueue; line L8 for a dequeue that returns EMPTY; line L11 for a dequeue that returns an item. Then (a) at the point of enq$(x)$, abs changes from $s$ to $s \cdot x$; (b) at the point of a dequeue that returns EMPTY, abs is empty; (c) at the point of a dequeue that returns $y$, abs changes from $y \cdot t$ to $t$; (d) no other step changes abs.

*Proof.* (a) By the case L3 of Lemma 2, line L3 appends the node $n_E$ with value $x$ at the end of $L$, and the head does not change, so abs becomes $s \cdot x$. (b) At line L8 the dequeuer reads $Q.head.next$, which is the current head because it holds $Q.hlock$. It reads nil, so $L$ is the head alone and abs is empty. (c) At line L10 the dequeuer read $y$ as the value of new_head, which is the first node after the head by the case L11 of Lemma 2; values never change after line L1 except on the new sentinel after line L11, where they are no longer part of abs. Line L11 removes the old head, so the first node becomes the head and abs loses exactly its first item $y$. (d) The only steps that change $L$ or the head are lines L3 and L11 (Lemma 1 and Lemma 2); line L4 changes only $Q.tail$, which abs does not use. $\square$

**Theorem (linearizability).** Each history of the two-lock queue is linearizable with respect to the sequential queue.

*Proof.* Take an execution and its history $H$. Each linearization point of Lemma 3 is a step of the call itself, so it lies between the call and its return. Complete $H$ as follows: keep each pending call that has passed its linearization point, with the result that Lemma 3 gives (for an enqueue, none; for a dequeue at line L11, the value read at line L10), and remove the other pending calls. A removed call has made no change to abs, by Lemma 3 (d). Order the kept calls by their linearization points, which are distinct steps. By Lemma 3, applying the calls in this order to the empty sequence gives at each point exactly the change and the result of the sequential queue, so the sequential history $S$ is legal and each call has the same result in $S$ as in $H$. If call $a$ returns before call $b$ starts, the point of $a$ is before the point of $b$, so $S$ keeps the real-time order of $H$. $\square$

**Theorem (deadlock-freedom).** If both locks are deadlock-free, then whenever a call is pending and the threads keep taking steps, some call returns. With starvation-free locks, each call returns.

*Proof.* No thread holds both locks, so no cycle of waits exists. A thread holds a lock for at most four of its own steps and releases it on each path, including the early return of line L9. So if calls wait at a lock, the holder releases it, and by deadlock-freedom of the lock some waiter enters; it then returns after $O(1)$ more steps. With starvation-free locks each waiter enters. $\blacksquare$

**Freeing nodes.** When a dequeuer returns, the old head `node` is no longer in $L$. No enqueuer reads it again: by Lemma 2 (c), it can be $Q.tail$ only while an enqueuer is open, and an open enqueuer performs only line L4 and line L5, which do not read the old tail. No other dequeuer reads it, because the next dequeuer reads the new head. So the node can be freed at line L13.
