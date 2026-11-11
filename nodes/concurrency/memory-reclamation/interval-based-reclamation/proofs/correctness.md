---
title: 2GEIBR never frees a node that a process may still access, and a stopped process holds back only the nodes whose lifetimes meet its reserved interval
proves: [correctness]
status: full
---

**Setting.** There are $n$ asynchronous processes on a sequentially consistent shared memory with atomic reads, writes, fetch-and-add and compare-and-swap. $E$ is the global epoch. Each process $p$ owns one shared reservation $Res[p]$, which is nil or a pair $[lo_p, up_p]$, and keeps a private copy of it. Each node $x$ has a birth epoch $b_x$, the value of $E$ read just before its allocation, and gets a retire epoch $r_x$ at L8. We use the lines L1 to L11 of the page. The client follows three rules.

1. **Protect before use.** Inside one operation, a process accesses a node $x$ only if it got $x$ from PROTECT in that operation and $x$ was reachable from a root at the read at L3, or $x$ is its own new node. The client makes sure that $x$ was reachable, as with hazard pointers: the stack reads $x$ from the root, and the dequeue reads the head again before it uses $head.next$.
2. **Retire after unlink.** RETIRE($x$) is called once per allocation of $x$, after the step that removed the last link to $x$.
3. **No resurrection.** A retired node is not linked again before it is freed.

**Lemma 1.** $E$ never decreases. The only write to it is a fetch-and-add of 1. $\square$

**Lemma 2 (the reservation only grows).** Between L2 and L7 of one operation of $p$, $lo_p$ does not change and $up_p$ does not decrease.

*Proof.* L2 sets both ends to $e$. L6 keeps $lo_p$ and sets $up_p$ to a value of $E$ read at L4, which by Lemma 1 is at least the value read before, at L1 or at an earlier L4, that is now in $up_p$. Nothing else writes $Res[p]$ before L7. $\square$

**Lemma 3 (the reservation covers the node).** Let PROTECT of $p$ return $x$ with the read at L3 at time $t_1$ and the read at L4 at time $t_2 > t_1$, which returned $u = up_p$. Then $Res[p] = [lo_p, u]$ from some time $t_0 < t_1$ until L7, up to growth of $up_p$, and $b_x \le u$ and $r_x \ge lo_p$.

*Proof.* The value $u$ was written to $Res[p]$ at L2 or L6 at a time $t_0$, after a read of $E = u$ at L1 or L4 at a time $t_r < t_0$. The read at L3 at $t_1$ comes after $t_0$ in program order. By Lemma 1, $E = u$ during $[t_r, t_2]$, which contains $t_1$. At $t_1$, $x$ is reachable from a root by rule 1, so $x$ was allocated before $t_1$, and its birth was read before that: $b_x \le E(t_1) = u$. By rules 2 and 3, $x$ is unlinked after $t_1$ and retired after that, so the read at L8 that sets $r_x$ comes after $t_1$, and $r_x \ge E(t_1) = u \ge lo_p$. By Lemma 2 the interval only grows until L7. $\square$

**Theorem 1 (safety).** No process accesses a node after it is freed.

*Proof.* Let $p$ access $x$ at time $t$ in an operation, where $x$ came from PROTECT as in Lemma 3. Suppose this incarnation of $x$ is freed at L11 by $q$ at a time $t_f < t$. The node entered the list of $q$ at L8, after its retire, so after $t_1$. The scan that frees it reads $Res[p]$ at L9 at a time $t_s$ with $t_0 < t_1 < t_s < t_f < t$. Since $p$ has not reached L7 by time $t$, at $t_s$ the slot holds $[lo_p, u']$ with $u' \ge u$ by Lemma 2. By Lemma 3, $b_x \le u \le u'$ and $r_x \ge lo_p$, so the test at L10 keeps $x$, a contradiction. A node that $p$ allocated itself in the operation is not retired before $p$ links it, and after that it is covered in the same way. $\square$

The reservation covers every node that PROTECT returned in the operation, not only the last one. So, unlike hazard pointers, a reader does not need one slot per pointer it holds.

**Theorem 2 (no double free).** Each node is in one retire list once per incarnation (rule 2), and L11 removes it when it frees it. $\square$

**Theorem 3 (bound).** For a reserved interval $I$, let $L(I)$ be the number of retired nodes whose lifetime $[b_x, r_x]$ meets $I$, and let $L$ be the largest $L(I)$ over the intervals that are reserved at one time. Then each retire list holds at most $R + nL$ nodes, and at most $n (R + nL)$ retired nodes are unfreed, even if processes stop at any steps.

*Proof.* A scan keeps a node only if its lifetime meets one of the at most $n$ intervals it read at L9, so after a scan the list holds at most $nL$ nodes. The list grows by one per RETIRE, and a scan starts as soon as it holds $R$ nodes. So it never holds more than $\max(R, nL + 1) \le R + nL$ nodes. $\square$

**Corollary (a stopped process).** A process that stops with $Res[p] = [lo, u]$ holds back only nodes born at or before $u$ and retired at or after $lo$. When $E$ moves once in every $F$ allocations of each process, at most $nF$ nodes are born in one epoch, and at most $n (F - 1)$ in the first one. So the stopped process holds back at most the nodes that are alive at epoch $lo$ and the at most $nF$ nodes born in each epoch of $[lo, u]$. The interval does not grow while the process is stopped, so this number does not grow with the run.

*Proof.* A node born after $u$ fails $b_x \le u$, and a node retired before $lo$ fails $r_x \ge lo$. A node that meets the interval is alive at $lo$ or is born in $[lo, u]$. A process does the fetch-and-add before the read of $E$ in each of its allocations whose count is a multiple of $F$. So in one epoch $e$ it allocates at most one node after its own increment and $F - 1$ more, and its next allocation is born after $e$. In the first epoch there is no own increment before the first $F - 1$ allocations. $\square$

**Theorem 4 (cost).** PROTECT is lock free: a pass fails at L5 only if $E$ changed since the last write of the reservation, which needs an allocation by some process. When $E$ did not move, PROTECT costs two reads and no write. RETIRE and the scan are wait free, with $O(n + R)$ steps per scan.

*Proof.* After the write at L6 the private copy of $up_p$ is the value just read, so a second failure needs a new increment of $E$. $\square$

Theorems 1 to 4 give the correctness of the method. $\blacksquare$
