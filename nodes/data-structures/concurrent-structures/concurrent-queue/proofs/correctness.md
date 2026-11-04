---
title: The one-lock queue is linearizable and deadlock-free
proves: [correctness, linearizability, progress]
status: full
---

We use the pseudocode of the page. A *history* is a finite sequence of call and return events of the threads. A call is *complete* if its return is in the history and *pending* otherwise. The lock satisfies mutual exclusion: at each moment at most one thread holds it. We say that a call *enters* when it completes line L2 or line L6 (the lock is now held by it), and that it *leaves* when it executes line L5, line L11 or the release of line L8.

**Lemma 1 (one at a time).** The critical sections of the calls are disjoint in time and are totally ordered. A call that enters leaves after $O(1)$ of its own steps, and it changes $Q.head$, $Q.tail$ and the next field of a node only while it holds the lock.

*Proof.* Mutual exclusion gives disjointness, and disjoint intervals of a line are totally ordered. Each critical section is straight-line code of at most four steps (lines L3 and L4, or lines L7 to L11). Lines L3, L4 and L9 are the only writes to $Q.head$, $Q.tail$ or a next field of a node in the list, and each one is inside a critical section. Line L1 writes the fields of a new node that no other thread can reach until line L3 links it. $\square$

Number the critical sections $c_1, c_2, \ldots$ in the order of Lemma 1, and let $o_k$ be the call that runs $c_k$. Let $S_k$ be the sequential history $o_1, \ldots, o_k$ of the queue type, with the arguments of the calls, and let $s_k$ be the queue state after $S_k$ (with $s_0$ empty).

**Lemma 2 (the invariant).** For each $k \ge 0$, after $c_k$ leaves (for $k = 0$, at the start): the list from $Q.head$ is finite, $Q.tail$ is its last node, the values after $Q.head$ are $s_k$, and the result of $o_k$ is the result of its call in $S_k$.

*Proof.* By induction on $k$. For $k = 0$ the constructor makes one sentinel node that is both $Q.head$ and $Q.tail$, with no node after it, and $s_0$ is empty.

Let $k \ge 1$ and assume the claim for $k - 1$. Between the end of $c_{k-1}$ and the start of $c_k$ no thread holds the lock, so by Lemma 1 nothing changes the list, $Q.head$ or $Q.tail$. So when $c_k$ starts, the claim for $k - 1$ still describes the list. By Lemma 1, $c_k$ runs alone, so its steps act on this state as sequential code does.

- If $o_k$ is enq$(x)$: line L3 sets the next field of the last node to the new node $n$, whose next is nil, and line L4 makes $Q.tail = n$. The list is still finite, $n$ is its last node, and the values after $Q.head$ are $s_{k-1} \cdot x = s_k$. The call returns nothing, as in $S_k$.
- If $o_k$ is deq and $s_{k-1}$ is empty: no node follows $Q.head$, so line L7 reads nil and line L8 returns EMPTY without a write. The state is $s_k = s_{k-1}$, and EMPTY is the sequential result.
- If $o_k$ is deq and $s_{k-1} = y \cdot t$: line L7 reads the node $f$ that holds $y$. Line L9 makes $f$ the new head, so the values after $Q.head$ are $t = s_k$. The tail does not change. It is still the last node, and it is still reachable: if $f$ was the last node, then $f = Q.tail$ is now the sentinel. Line L10 reads $y$, the sequential result. $\square$

**Theorem (linearizability).** Each history $H$ of the one-lock queue is linearizable with respect to the sequential queue type.

*Proof.* First remove each pending call from $H$. This changes no result of a complete call. A pending call that has not entered has changed nothing that another thread can read (line L1 writes only a new node that is not linked). A pending call that has entered holds the lock until the end of $H$, so its critical section is the last one, and no other call enters after it and reads what it wrote. So the complete calls are $o_1, \ldots, o_m$ for some $m$, and Lemma 2 applies to each of them.

Let the linearization point of each complete call be the moment it enters. This moment lies after the call starts, and before it returns, because the call leaves after it enters and returns after it leaves. The order of the linearization points is the order $o_1, o_2, \ldots$ of Lemma 1. So the sequential history $S$ in this order keeps the real-time order of $H$: if $a$ returns before $b$ starts, the point of $a$ is before the return of $a$, which is before the start of $b$, which is before the point of $b$. By Lemma 2, each call has in $H$ the result it has in $S$. So $S$ is a legal sequential queue history with the same calls and results as the completed $H$, in an order that extends the real-time order. $\square$

**Theorem (progress).** If the lock is deadlock-free, then the queue is deadlock-free: if some call is pending and no thread stops, then some call returns. If the lock is starvation-free, then each call of a thread that does not stop returns.

*Proof.* A thread holds the lock for at most four of its own steps (Lemma 1), and then releases it on each path, including the early return of line L8. So a thread that holds the lock and keeps taking steps releases it. If calls wait at line L2 or L6, deadlock-freedom of the lock gives that some waiting call enters; it then leaves and returns after $O(1)$ steps. With a starvation-free lock each waiting call enters, and then returns. $\blacksquare$

The queue is not [lock-free](/lock-freedom/): if the thread that holds the lock stops, for example because it is preempted for ever, then no other call can return.
