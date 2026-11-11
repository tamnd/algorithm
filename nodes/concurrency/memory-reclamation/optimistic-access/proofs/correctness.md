---
title: Correctness of the simplified optimistic access scheme
proves: [correctness]
status: full
---

We prove three facts about the simplified scheme on the Treiber stack and the Michael and Scott queue: a value read from a freed node is never used, a node is never freed while a thread can still make a CAS on it or with it, and at most $n R$ retired nodes are unfreed.

**Model and rules.** Threads run asynchronously on a sequentially consistent memory. Nodes come from a type-stable pool: a read of a freed node returns some value and does not fault. A thread reads shared nodes only through L1 to L3, and makes a CAS only after L4 and L5 for every node that the CAS reads or writes, other than the static root. A thread clears $W[t]$ only at L3 or L5, and then it restarts its operation from the root with no value kept from before. A node is retired once, by the thread whose CAS removed it from the structure, and freed only at L8 of the recycle of that thread. Hazard pointers stay set from L4 until the end of the operation.

Call the **attempt start** $s$ of a thread the later of the start of its operation and its last clearing of $W[t]$. A node is **reachable** at a time if it is on the list from the root (for the queue, from the head) at that time.

**Fact P (structure).** In both structures, if a node $y$ was reachable at a time $u$ and is not in the pool at a later time $v$, then $y.next$ at time $v$ is nil or a node that was reachable at some time in $[u, v]$.

*Proof.* In the stack, $next$ is written only by a push on its own new node, before the node is linked, so $y.next$ is the same at $u$ and $v$, and at $u$ it named a reachable node or nil. In the queue, $next$ is written only by the CAS from nil to a new node, on the last node; the new node becomes reachable at that CAS. A removed node has a non-nil $next$, which does not change until the node is freed. $\square$

**Lemma 1.** Let $t$ be in an attempt that started at $s$. Every node address that $t$ obtains in this attempt, from the root or from a read that passed L2, names a node that was reachable at some time at or after $s$ and that was not freed between that time and the read that gave the address.

**Lemma 2.** If a read of $t$ at L1, at time $\tau$, reads a node $x$ that is in the pool at $\tau$, then the check at L2 that follows sees $W[t] = $ true.

*Proof of both, by induction on the reads of the attempt.* The root is static, and a node read from the root at time $\tau_0 \ge s$ was reachable at $\tau_0$. For Lemma 2, let the read at $\tau$ be of node $x$, whose address $t$ got earlier in the attempt. By Lemma 1 for that earlier read, $x$ was reachable at some time $u \ge s$ and not freed between $u$ and the time $t$ got the address. Since $x$ is in the pool at $\tau$, some recycle freed $x$ at L8 at a time in $(u, \tau)$. That recycle freed only nodes that were in its thread's list before its L6, and $x$ was removed from the structure before it was retired; since $x$ was reachable at $u$, the removal, the retire and that L6 all came after $u \ge s$. So L6 set $W[t]$ to true after $s$, and by the definition of $s$, $t$ did not clear it since. L2 follows L1 with no step of $t$ between them, so L2 sees true.

For Lemma 1, a read of $y.next$ that passes L2 was made while $y$ was not in the pool, by Lemma 2. By the induction hypothesis $y$ was reachable at some $u \ge s$, so by Fact P the value names nil or a node that was reachable at a time in $[u, \tau] \subseteq [s, \tau]$. $\square$

**Theorem 1 (stale values are not used).** Every value that a thread uses, to follow a pointer, to return or to give to a CAS, was read at L1 from a node that was not in the pool at that time.

*Proof.* A value is used only after its L2 passed, and by Lemma 2 such a read did not read a node in the pool. $\square$

**Theorem 2 (no free under a CAS).** Let $t$ pass L5 in an attempt with start $s$, with $HP[t] \ni x$, and later make a CAS that involves $x$. Then no L8 frees $x$ between the read at which $t$ got the address of $x$ and the CAS.

*Proof.* Take a recycle $r$ that frees $x$ at L8 in that interval. As in Lemma 2, its L6 came after $s$. Case 1: the L6 of $r$ came before the L5 of $t$. Then $W[t]$ was true at L5, because $t$ did not clear it between L6 and L5 (its only steps between L4 and L5 are writes of hazard pointers). So $t$ restarts and makes no CAS in this attempt, a contradiction. Case 2: the L6 of $r$ came after the L5 of $t$. Then the L7 of $r$ came after L4 of $t$, while $HP[t]$ still named $x$, so $x \in H$ and $r$ kept $x$, a contradiction. $\square$

**Consequence.** By Theorem 2, the address of a node in a CAS is not freed and reused between the read and the CAS, so a CAS that succeeds compares against the same node that the thread read: there is no ABA on these nodes, and the CAS on $tail.next$ in the queue never writes into a freed node. With Theorem 1, each operation behaves as it does with no reclamation at all, so the stack and the queue stay linearizable.

**Theorem 3 (bound).** With $R > n K$, at most $n R$ retired nodes are unfreed at any time.

*Proof.* A thread's list grows by one per retire and is recycled when it reaches $R$. A recycle keeps only nodes in $H$, and $|H| \le n K < R$. So each list holds at most $R$ nodes at any time, and there are $n$ lists. A thread that stops at any point keeps at most $K$ nodes in its hazard pointers, which is already counted in $H$. $\square$

The test file checks Theorems 1 and 2 on every interleaving of small stack and queue runs and on random runs, shows that the scheme with no checks at L2 and L5 loses a value, and checks Theorem 3 with $n = 3$, $K = 2$ and $R = 12$: under a stall, the peak is 21 to 24 against the bound 36. $\blacksquare$
