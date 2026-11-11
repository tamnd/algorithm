---
title: Hazard pointers never free a node that a process may still access, and keep at most n R retired nodes unfreed
proves: [correctness]
status: full
---

**Setting.** There are $n$ asynchronous processes on a sequentially consistent shared memory with atomic reads, writes and compare-and-swap. Each process $p$ owns $K$ single-writer slots $HP[p][0..K-1]$. A client data structure is a set of nodes reachable from fixed roots. We use the lines L1 to L10 of the page. The client follows three rules.

1. **Protect before use.** A process accesses a field of a node $x$ only if it got $x$ from a call of PROTECT on slot $i$ that returned at L4, it has not written slot $i$ since then, and $x$ was reachable from a root at the read at L3. The client makes sure of the last part: the Treiber stack reads $x$ from the root itself, and the dequeue of the Michael and Scott queue reads the head again after it read $head.next$, and uses $next$ only if the head did not change.
2. **Retire after unlink.** A process calls RETIRE($x$) only after a step of its own removed the last link to $x$, so that $x$ is not reachable from a root when RETIRE starts. Each node is retired once per allocation.
3. **No resurrection.** A node that is not reachable is never linked again until it is freed and allocated anew.

We call the time from an allocation of $x$ to its next free an *incarnation* of $x$.

**Lemma 1.** Let $p$ return $x$ from PROTECT at time $t_3$ (its read at L3), with the matching write of L2 at time $t_2 < t_3$. Then the incarnation of $x$ that is current at $t_3$ was reachable at $t_3$, and it was not retired before $t_3$.

*Proof.* By rule 1, $x$ is reachable at $t_3$. By rule 2, RETIRE($x$) for this incarnation starts only after $x$ stops being reachable, and by rule 3 it cannot become reachable again within the incarnation. So the retire is after $t_3$. $\square$

**Lemma 2.** If a scan by process $q$ frees $x$ at L9, then for every slot $HP[p][i]$, the read of that slot at L7 in this scan happened after $x$ was retired.

*Proof.* $q$ appends $x$ to its private list at L5, inside RETIRE($x$), and a node enters a scan only through that list. The scan that frees $x$ starts at L6 of the same or a later RETIRE call of $q$, so all its reads at L7 come after L5 for $x$. $\square$

**Theorem 1 (safety).** No process accesses a node after it is freed.

*Proof.* Suppose $p$ accesses $x$ at time $t$ under the protection of slot $i$, and let $t_2 < t_3 < t$ be the times of its L2 and L3 steps for that protection. By rule 1, $HP[p][i] = x$ during all of $[t_2, t]$. Suppose for contradiction that the incarnation of $x$ current at $t_3$ is freed at a time $t_f < t$. By Lemma 1 it is retired at a time $t_r > t_3$. By Lemma 2, the scan that frees it reads $HP[p][i]$ at a time $t_s$ with $t_r < t_s < t_f$. Then $t_2 < t_3 < t_r < t_s < t_f < t$, so $t_s \in [t_2, t]$ and the read returned $x$. The scan therefore adds $x$ to $plist$ and keeps $x$ at L8. This contradicts the free at $t_f$. If the incarnation is freed at a time $t_f > t$, the access is before the free. $\square$

**Theorem 2 (no double free).** A node is freed at most once per incarnation.

*Proof.* A node is freed only from the private list of the process that retired it. By rule 2 it is retired once per incarnation, so it is in one list once, and L9 removes it from that list when it frees it. $\square$

**Theorem 3 (bound).** Let $R > nK$. At every time, the list of each process holds at most $R$ nodes, so at most $nR$ retired nodes are not yet freed. This holds even if some processes stop forever at any step.

*Proof.* A scan keeps only nodes named by some slot that it read at L7. There are $nK$ slots and each names at most one node, so after a scan the list holds at most $nK < R$ nodes. The list grows by one per RETIRE, and a scan starts at L6 as soon as the list holds $R$ nodes. So the list never holds more than $R$ nodes. A stopped process holds at most its own list of $R$ nodes and keeps at most $K$ other nodes alive through its slots; neither number grows while it is stopped. Summing over the $n$ lists gives $nR$. $\square$

**Theorem 4 (cost).** PROTECT is lock free: an attempt fails at L3 only if the field $a.f$ changed between L1 and L3, which is a step of another process that changed the structure. With $R = nK + \Omega(nK)$, for example $R = 2nK$, a scan frees at least $R - nK = \Omega(R)$ nodes and takes $O(nK + R)$ steps when $plist$ is a hash set, so the amortized cost of RETIRE is $O(1)$ expected steps per node. RETIRE and the scan are wait free: they contain no loop that waits for another process.

*Proof.* The first claim is the text of L3. For the second, after a scan the list holds at most $nK$ nodes, so the next scan starts after at least $R - nK$ more calls of RETIRE, and frees at least $R - nK$ nodes. The scan reads $nK$ slots and looks up each of at most $R$ list nodes once. Charging the scan to the $R - nK$ calls since the last one gives $O((nK + R)/(R - nK)) = O(1)$ per call. $\square$

Theorems 1 to 4 together give the correctness of the method. $\blacksquare$
