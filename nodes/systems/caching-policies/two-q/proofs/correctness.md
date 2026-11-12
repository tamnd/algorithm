---
title: Full 2Q keeps disjoint queues within their sizes, always frees a slot, and is FIFO when Kout is 0
proves: [correctness]
status: full
---

We use the pseudocode of the page, a buffer of capacity $k \ge 1$, parameters $0 \le K_{in} < k$ and $K_{out} \ge 0$, all queues empty at the start, and a request sequence $\sigma_1 \ldots \sigma_n$. The resident pages are $R = A1_{in} \cup A_m$.

**Invariant.** After each request:

1. $A1_{in}$, $A1_{out}$ and $A_m$ are pairwise disjoint;
2. $|R| = |A1_{in}| + |A_m| \le k$;
3. $|A1_{out}| \le K_{out}$;
4. the requested page is in $R$.

*Proof.* By induction on the requests. The empty queues satisfy parts 1 to 3.

*RECLAIM frees a slot when $|R| = k$.* If $|A1_{in}| > K_{in}$, then $A1_{in}$ is not empty and line L12 pages out its tail. Otherwise $|A_m| = k - |A1_{in}| \ge k - K_{in} \ge 1$, so line L15 pages out the tail of $A_m$. In both cases $|R|$ drops to $k - 1$. Line L13 adds the identifier of a page that is no longer resident, and it was not in $A1_{out}$ before by part 1, since it was in $A1_{in}$. Line L14 brings $A1_{out}$ back to at most $K_{out}$ entries. If $|R| < k$, line L10 returns at once. So after RECLAIM, parts 1 and 3 hold and $|R| \le k - 1$.

*The four cases.* Lines L1 and L2 reorder $A_m$, and lines L3 and L4 change nothing, so the invariant holds and $p \in R$. At lines L5 to L7, $p$ leaves $A1_{out}$, RECLAIM makes $|R| \le k - 1$, and $p$ joins $A_m$; it is in no other queue, since it was in $A1_{out}$ only, by part 1. A page paged out by this RECLAIM is not $p$, which was not resident, and its identifier, if added to $A1_{out}$, is not $p$. At lines L8 and L9, $p$ is in no queue, RECLAIM makes room, and $p$ joins $A1_{in}$. In all cases $|R| \le k$ and $p \in R$. $\square$

The tests check parts 1 to 4 after each request, and compare the code with a direct implementation with Python lists on random traces and random parameters.

**Claim (FIFO as a special case).** If $K_{out} = 0$, full 2Q has the same hits and misses as FIFO with $k$ pages, for any $K_{in} < k$.

*Proof.* With $K_{out} = 0$, line L14 removes each identifier right after line L13 adds it, so $A1_{out}$ stays empty, line L5 never applies, and no page enters $A_m$. So $A_m$ is always empty, and $R = A1_{in}$. Then RECLAIM, when $|R| = k$, has $|A1_{in}| = k > K_{in}$, so it pages out the tail of $A1_{in}$, the page that entered first. A hit in $A1_{in}$ changes nothing. These are the rules of FIFO on the queue $A1_{in}$. $\square$

**Scan resistance.** Assume that $|A1_{in}| > K_{in}$ at some time, and that from then on each request is to a page that is in no queue. Each such request runs RECLAIM. If a slot is free, nothing is paged out. Otherwise RECLAIM pages out the tail of $A1_{in}$, because $|A1_{in}| > K_{in}$. Then the new page joins $A1_{in}$. So $|A1_{in}|$ never shrinks, the condition $|A1_{in}| > K_{in}$ stays true, and no page of $A_m$ is paged out, however long the scan is. The tests check this with $k = 8$ and a scan of 200 new pages.

**Cost.** Each queue is a hash map with a doubly linked list in insertion order, so membership, removal, moves to the head and removal of the tail take $O(1)$ expected time. Each request runs a constant number of such steps. The space is $\Theta(k + K_{out})$, which is $\Theta(k)$ for $K_{out} = O(k)$.
