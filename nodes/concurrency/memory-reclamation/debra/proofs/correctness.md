---
title: DEBRA never frees a node that an active operation may access, and DEBRA+ bounds the garbage of each process even when others stop
proves: [correctness]
status: full
---

**Setting.** There are $n$ asynchronous processes on a sequentially consistent shared memory with atomic reads, writes and compare-and-swap. $G$ is the global epoch. $A[p]$ is the announcement of $p$, a pair (epoch, quiescent bit). Process $p$ keeps a private epoch $seen_p$, a counter $checked_p$, and three bags. We use the lines L1 to L10 of the page. An *operation* of $p$ runs from its write at L4, at a time $t_4$, to its write at L10. In DEBRA+, a signal sent to $p$ at L6 is handled by $p$ before its next shared step: in the read phase $p$ drops every pointer it holds and starts the operation again from L1; in the write phase it goes on, and it has already written its reservations, one per pointer that the write phase uses. The client follows three rules.

1. **Access inside an operation.** A process accesses a node only inside an operation, and only a node that was not retired before $t_4$ of that operation (for DEBRA+: of the latest restart of that operation).
2. **Retire after unlink.** Each node is retired once per allocation, inside an operation, after the step that removed its last link.
3. **No resurrection.** A retired node is not linked again before it is freed.

**Lemma 1.** $G$ only grows, by one at a time. Every check in one *round* of $p$, that is, the checks that bring $checked_p$ from 0 to $n$ before the compare-and-swap at L8 from $e$ to $e + 1$, is made in an operation whose read at L1 returned $e$.

*Proof.* The only write to $G$ is at L8 from $e$ to $e + 1$. L2 sets $checked_p$ to 0 whenever $p$ reads a new epoch at L1, so all checks that count towards one compare-and-swap follow reads of the same value $e$. $\square$

**Lemma 2 (an active operation holds the epoch, plain DEBRA).** Let an operation of $p$ write $A[p] = (e_p, \text{false})$ at $t_4$, and let $g_0 = G(t_4)$. Then $G \le g_0 + 1$ until the operation ends.

*Proof.* $e_p$ was read at L1 before $t_4$, so $e_p \le g_0$. Suppose $G$ goes from $f$ to $f + 1$ with $f \ge g_0 + 1$ while the operation runs. By Lemma 1, every check of that round followed a read of $G = f > g_0$, so it came after $t_4$; in particular the check of $p$ read $A[p] = (e_p, \text{false})$ with $e_p \le g_0 < f$. That check fails at L5, so the round is not complete, a contradiction. $\square$

**Lemma 3 (three rotations are two epochs).** Let $q$ retire $x$ at L9 at a time $t_r$, and let $g_r = G(t_r)$. If $q$ frees $x$ at L3, then $G \ge g_r + 2$ at some time before the free.

*Proof.* $x$ goes into the current bag. That bag is emptied at the third rotation after $t_r$. Each rotation happens in a later operation of $q$, when its read at L1 returns a value larger than $seen_q$. Let the three values be $v_1 < v_2 < v_3$. They are read after $t_r$, so $v_1 \ge g_r$, and $v_3 \ge v_1 + 2 \ge g_r + 2$. $\square$

**Theorem 1 (safety of DEBRA).** No process accesses a node after it is freed.

*Proof.* Let $p$ access $x$ inside an operation with $t_4$ and $g_0$ as in Lemma 2. By rule 1, $x$ is retired at a time $t_r > t_4$, so $g_r \ge g_0$. By Lemma 3, $G$ reaches $g_r + 2 \ge g_0 + 2$ before the free, and by Lemma 2 that happens after the operation of $p$ ends. So the access is before the free. $\square$

**Theorem 2 (safety of DEBRA+).** No process accesses a node after it is freed.

*Proof.* Lemma 2 changes in one way: the check of $p$ in a round can also pass because $p$ was signalled at L6, or still had a pending signal. Let the round that moves $G$ from $g_0 + 1$ to $g_0 + 2$ pass its check of $p$ at a time $t_s$ through a signal sent at a time $t'_s \le t_s$ and not yet handled. Then $p$ takes no shared step in $[t'_s, t_s]$, and its first step after $t'_s$ handles the signal. Now take an access of $p$ to $x$ with a pointer obtained after its latest $t_4$. If the access comes before $t'_s$, it comes before $G$ reaches $g_0 + 2$, hence before the free, as in Theorem 1. If $p$ handles the signal in the read phase, it drops the pointer to $x$ and announces again, so it makes no later access with that pointer. If $p$ handles the signal in the write phase, it wrote its reservations before its check of the signal flag after the reservations; that check found no signal, so it came before $t'_s$, and the reservations were written before $t'_s$. A free of $x$ happens after $G$ reaches $g_0 + 2$, so after $t_s$, and its reads of the reservations at L3 come after $t'_s$. They see the reservation of $x$, and L3 keeps $x$. In the write phase, $p$ accesses only reserved nodes. If the check of a round passes because $A[p]$ is quiescent or current, Lemma 2 applies as before. $\square$

**Theorem 3 (no double free).** Each node enters one bag of the process that retired it, once per incarnation by rule 2. L3 either frees it and drops it, or keeps it in the new current bag; it is freed at most once. $\square$

**Theorem 4 (bound for DEBRA+).** Suppose that each operation retires at most one node. Then at every time, each process holds at most $B = T + 3(n + 1) + 3nK$ nodes in its bags, whatever the other processes do, so at most $nB$ retired nodes are unfreed.

*Proof.* Each emptied bag keeps at most $nK$ reserved nodes, one per slot read at L3. If at an operation of $q$ the bags hold at least $T$ nodes, the check at L5 and L6 passes: either the checked process is quiescent or current, or it has a pending signal, or $q$ signals it now. So while the bags hold at least $T$ nodes at every operation, $checked_q$ grows by one per operation, and after at most $n$ operations $q$ tries the compare-and-swap at L8. Whether it succeeds or not, $G > seen_q$ afterwards, so the next operation rotates. Hence two rotations are at most $n + 1$ operations apart. Now fix a time $\tau$ and let $o$ be the last operation of $q$ before $\tau$ that began with fewer than $T$ nodes; just after $o$ the bags hold at most $T$ nodes. Every bag at $\tau$ holds the nodes kept at its last emptying (at most $nK$), plus the nodes retired while it was current. The nodes that were present just after $o$ count at most $T$. Every bag that became current after $o$ was current for at most $n + 1$ operations, and so got at most $n + 1$ new nodes; the bag current at $o$ got at most $n + 1$ after $o$ by the same argument. Three bags give at most $T + 3(n + 1) + 3nK$. $\square$

**Plain DEBRA is not robust.** If $p$ stops inside an operation, Lemma 2 holds forever, so $G \le g_0 + 1$, and by Lemma 3 no node retired after that is freed.

Theorems 1 to 4 give the correctness of DEBRA and DEBRA+. $\blacksquare$
