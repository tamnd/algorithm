---
title: With a type-stable pool and a claim bit, lock-free reference counting frees a node only when no process holds it, frees it once, and frees every node that loses its last reference
proves: [correctness]
status: full
---

**Setting.** There are $n$ asynchronous processes on a sequentially consistent shared memory with atomic reads, writes, fetch-and-add and compare-and-swap. Nodes come from a type-stable pool: a freed node stays a node, its field $rc$ keeps its value across free and reuse, and a fetch-and-add on $rc$ of a free node is allowed. Every other access to a free node is an error. We use the lines L1 to L7 of the page, with steps of 2 at L2 and L5. Allocation from the pool adds 1 to $rc$. The client follows three rules.

1. **Counted references.** A process reads or writes a field of a node $x$ other than $rc$ only while it holds a reference to $x$: one returned by SAFE_READ, or its own new node. It reads a source $a.f$ at L1 and L3 only while $a$ is a root or a node it holds.
2. **Counted links.** Before a CAS writes $x$ into a shared word, the process adds 2 to $rc$ of $x$, or gives up a reference it holds; after a failed CAS it releases that count. After a CAS removes a link to $y$, it calls RELEASE($y$) once. Each held reference is released once.
3. **No cycles.** The links between nodes form no cycle.

For a node $x$, let $c(x)$ be the number of links to $x$ in shared words, plus the number of references to $x$ that processes hold, plus the number of increments at L2 on $x$ whose SAFE_READ has not yet returned or released at L4. Call $x$ **claimed** from a successful CAS at L6 until its next allocation.

**Lemma 1 (count invariant).** At every time, $rc(x) = 2 c(x)$ if $x$ is allocated and not claimed, and $rc(x) = 2 c(x) + 1$ if $x$ is claimed or free.

*Proof.* By induction over the steps. A new node starts with $rc = 1$ and is free; allocation adds 1 and gives the process one reference, so both sides grow by 1 or 2 in step. L2 adds 2 and one pending increment. A successful check at L3 turns the pending increment into a held reference. L5 subtracts 2 and removes one reference, link or pending increment. The CAS at L6 moves $rc$ from 0 to 1 and makes $x$ claimed. The free at L7 changes neither $rc$ nor $c$. Rule 2 keeps the links matched to the counts. $\square$

**Lemma 2 (a claim needs no references).** When the CAS at L6 claims $x$, then $c(x) = 0$. After that, until $x$ is allocated again, $x$ has no links and no process holds it.

*Proof.* The CAS succeeds on $rc = 0$, which by Lemma 1 means $c(x) = 0$ and $x$ not claimed. A new link to $x$ needs a process that holds $x$ or a count added for the link (rule 2), and a new held reference needs a check at L3 that finds $x$ in a source, so a link. Neither can start from $c(x) = 0$ without a link: an increment at L2 adds only a pending count, and its check at L3 fails while $x$ has no link. So $x$ stays without links and holders until it is allocated again. $\square$

**Theorem 1 (safety).** No process accesses a field other than $rc$ of a node that is free.

*Proof.* By rule 1, such an access is made while the process holds $x$, from a time when $x$ was allocated. While the reference is held, $c(x) \ge 1$, so by Lemma 1, $rc(x) \ge 2$ and the CAS at L6 cannot claim $x$. Only the claimer frees $x$ at L7, so $x$ is not free while the reference is held. The read of $q.next$ at L7 is by the claimer before the free. $\square$

**Theorem 2 (no double free).** Each allocation of a node is freed at most once.

*Proof.* After a claim, $rc$ is odd until the next allocation, by Lemma 1, so no other CAS at L6 from 0 succeeds. Only the claimer frees. $\square$

**Theorem 3 (no leak without holders).** If at some time $c(x) = 0$ and $x$ is allocated and not claimed, then some process frees $x$, or has a pending step that will try to.

*Proof.* By Lemma 1, $rc(x) = 0$, so the step that made $rc(x)$ equal to 0 was a decrement at L5 that returned 2, and its process goes on to L6. Its CAS fails only if $rc(x) \ne 0$ at that time. Then either another process claimed $x$, or an increment at L2 came after the decrement. Such an increment comes from a SAFE_READ that read $x$ at L1 before $x$ lost its last link. Its check at L3 fails, because $x$ has no link and gets no new link (the argument of Lemma 2), so it calls RELEASE, and its decrement returns 2 when it removes the last count, which starts a new try at L6. Each process has at most one such pending increment, so after a finite number of tries some CAS at L6 claims $x$, and its process frees $x$ at L7. It then releases the link $x.next$, and the same argument frees each node of the chain that loses its last reference. Rule 3 makes this chain finite. $\square$

**Theorem 4 (the DCAS version).** If L2 and L3 are replaced by one double compare-and-swap that adds 1 to $rc$ of $q$ only if $a.f = q$, then Theorems 1 to 3 hold without a type-stable pool and without the claim bit.

*Proof.* Each increment now happens at a time when $a.f = q$, so $x$ has a link and $c(x) \ge 1$. So no step ever touches a free node, and once $c(x) = 0$ no increment can happen until $x$ is allocated again. Exactly one decrement takes $rc$ from 1 to 0, and its process frees $x$. $\square$

**Theorem 5 (cost and garbage).** SAFE_READ costs 3 steps when the source does not change, and is lock free: it retries only after the source changed. RELEASE costs $O(1)$ steps plus 2 steps per node of the chain it frees. A process that holds $x$ keeps alive every node reachable from $x$. In the Treiber stack, the field $next$ of a node never changes after its push, so a stopped process keeps alive at most the nodes that were below its nodes when they were pushed. In the Michael and Scott queue, the field $next$ of the last node changes at each enqueue, so a stopped process that holds a dequeued node keeps alive every node enqueued after it, and the garbage has no bound. $\square$

Theorems 1 to 5 give the correctness of the method. $\blacksquare$
