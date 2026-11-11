---
title: Hazard eras never free a node that a process may still access, and a stopped process holds back only the nodes alive in its published eras
proves: [correctness]
status: full
---

**Setting.** There are $n$ asynchronous processes on a sequentially consistent shared memory with atomic reads, writes and compare-and-swap. $C$ is the era clock, a shared counter. Each process $p$ owns $K$ single-writer slots $HE[p][0..K-1]$ and keeps a private copy of what it last wrote in each. Each node $x$ has a birth era $b_x$, the value of $C$ read just before its allocation, and gets a retire era $r_x$ at L5. We use the lines L1 to L10 of the page. The client follows three rules.

1. **Protect before use.** A process accesses a node $x$ only if it got $x$ from PROTECT on slot $i$ at L3, slot $i$ has not been written since then, and $x$ was reachable from a root at the read at L1. The client makes sure of the last part, as with hazard pointers: the stack reads $x$ from the root, and the dequeue reads the head again before it uses $head.next$.
2. **Retire after unlink.** RETIRE($x$) is called once per allocation of $x$, after the step that removed the last link to $x$.
3. **No resurrection.** A retired node is not linked again before it is freed.

**Lemma 1.** $C$ never decreases. The only write to it is the compare-and-swap at L6 from $e$ to $e + 1$. $\square$

**Lemma 2 (the published era covers the node).** Let PROTECT on slot $i$ of $p$ return $x$ at L3, where the read at L1 at time $t_1$ returned $x$ and the read at L2 at time $t_2 > t_1$ returned $e$, equal to the private copy. Then $HE[p][i] = e$ from some time $t_4 < t_1$ until the slot is written again, and $b_x \le e \le r_x$.

*Proof.* The private copy equals the slot, since both are written together at L4 and L10. It became $e$ at a write at L4 at time $t_4$ that came after a read of $C = e$ at L2, either in an earlier pass of this loop or in an earlier call; in both cases $t_4 < t_1$. By Lemma 1, $C = e$ during the whole interval from that earlier read to $t_2$, which contains $t_1$. At $t_1$, $x$ is reachable from a root by rule 1, so $x$ was allocated before $t_1$, and $b_x \le C(t_1) = e$. By rules 2 and 3, $x$ is retired after $t_1$, so the read at L5 that sets $r_x$ comes after $t_1$, and $r_x \ge e$ by Lemma 1. $\square$

**Theorem 1 (safety).** No process accesses a node after it is freed.

*Proof.* Let $p$ access $x$ at time $t$ under slot $i$, with $t_4 < t_1 < t_2$ and $e$ as in Lemma 2, and suppose this incarnation of $x$ is freed at L9 by $q$ at a time $t_f < t$. The node entered the list of $q$ at L5, after the retire, which is after $t_1$. The scan that frees it reads every slot at L7 after that, so it reads $HE[p][i]$ at a time $t_s$ with $t_4 < t_1 < t_s < t_f < t$. By rule 1 the slot still holds $e$ at $t_s$. By Lemma 2, $b_x \le e \le r_x$, so L8 keeps $x$, a contradiction. $\square$

**Theorem 2 (no double free).** Each node is in one retire list once per incarnation (rule 2), and L9 removes it when it frees it. $\square$

**Theorem 3 (bound).** Let $L$ be the largest number of retired nodes whose interval $[b_x, r_x]$ contains one given era. Then each retire list holds at most $R + nKL$ nodes at any time, so at most $n (R + nKL)$ retired nodes are unfreed, even if processes stop at any steps.

*Proof.* A scan keeps a node only if its interval contains one of the at most $nK$ eras it read, so after a scan the list holds at most $nKL$ nodes. The list grows by one per RETIRE, and a scan starts as soon as it holds at least $R$ nodes. So it never holds more than $\max(R, nKL + 1) \le R + nKL$ nodes. $\square$

A stopped process keeps at most $K$ eras published, and so holds back at most $KL$ nodes in the lists of the others. Unlike with hazard pointers, $L$ depends on the client: it is the number of nodes alive at one time in one era, which is bounded when the clock moves at least once for every bounded number of allocations.

**Theorem 4 (cost).** PROTECT is lock free: a pass of the loop fails at L3 only if $C$ changed since the last write of the slot, which needs a RETIRE by another process. When the clock did not move, PROTECT costs two reads and no write. RETIRE and the scan are wait free.

*Proof.* The loop retries only when the read at L2 differs from the private copy; after the write at L4 the copy is the value just read, so a second failure needs a new increment of $C$ at L6. $\square$

Theorems 1 to 4 give the correctness of the method. $\blacksquare$
