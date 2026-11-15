---
title: The two-stage URL frontier hands out each URL once and never breaks a host's politeness gap
proves: [correctness]
status: full
---

The frontier has front queues $F_1, \ldots, F_F$ ($F_1$ has the highest priority), back queues $Q_1, \ldots, Q_B$ with $F, B \ge 1$, a set Seen, a map owner from back queues to hosts, a map queue from hosts to back queues, a min-heap of pairs $(t, j)$, a set Free of back queues, and a map next from hosts to times. The line numbers are those of the pseudocode on the page: ADD is L1 and L2, NEXT is L3 to L10, and REFILL is L11 to L16. All queues are FIFO. The gap of host $h$ is $\delta(h) \ge 0$. Calls to NEXT receive times now that do not decrease.

Call $Q_j$ *active* if it has an owner, and *free* if $j \in$ Free. A URL is *waiting* if it is in a front queue or a back queue.

**Lemma 1 (invariants).** Before and after each call of ADD and NEXT:

1. Each back queue is either free, empty, with no owner and no heap entry, or active, not empty, with an owner $h$, $\mathrm{queue}(h) = j$, and exactly one heap entry $(t, j)$.
2. Every URL in an active $Q_j$ has the host $\mathrm{owner}(j)$, and queue is a one-to-one map from the owners to their queues. So a host is in at most one back queue.
3. Each URL of Seen is either waiting in exactly one queue or has been returned by NEXT, and not both.
4. For an active queue with owner $h$ and heap entry $(t, j)$: if next$(h)$ is defined, then $t \ge \mathrm{next}(h)$.

*Proof.* At the start all back queues are free and Seen is empty, so the claims hold. ADD changes only Seen and one front queue (lines L1 and L2): a URL that was not in Seen goes to exactly one front queue, so claim 3 holds and the other claims do not involve front queues.

Consider REFILL$(j, \mathit{now})$, called with $Q_j$ empty, without an owner and without a heap entry. Each round of lines L12 and L13 moves the head $u$ of one front queue, with host $h$. If $h$ owns a queue $Q_k$ (line L14), $u$ goes to the tail of $Q_k$, which keeps claim 2; $Q_k$ was active and stays so. Otherwise (line L15) $Q_j$ gets owner $h$, the URL $u$ and the one heap entry $(\max(\mathit{now}, \mathrm{next}(h)), j)$, whose time is at least next$(h)$ when next$(h)$ is defined; then REFILL returns. If the front queues run empty first, line L16 makes $Q_j$ free. In each case each moved URL is in exactly one queue, and $Q_j$ ends active or free.

Consider NEXT. Line L3 calls REFILL on free queues, which keeps the claims by the paragraph above. Line L5 removes the heap entry $(t, j)$ of an active queue, and line L6 removes the head $u$ of $Q_j$, which is returned at line L10, so claim 3 holds for $u$. Line L7 sets $\mathrm{next}(h) = s + \delta(h)$ for $h = \mathrm{owner}(j)$. If $Q_j$ still has URLs, line L8 inserts $(\mathrm{next}(h), j)$, the one entry of $Q_j$, which meets claim 4 with equality. Else line L9 removes the owner, so $Q_j$ is empty with no owner and no entry, and REFILL makes it active or free. No other heap entry changes, and next changes only for $h$, whose only queue is $Q_j$ by claim 2, so claim 4 holds for all other queues. $\square$

**Theorem 2 (each URL once).** NEXT returns each URL at most once. If NEXT returns nothing, the frontier holds no waiting URL.

*Proof.* The first claim is claim 3 of Lemma 1, together with the test of line L1, which stops a URL from entering twice. For the second, suppose line L4 finds the heap empty. By claim 1 no queue is active, so all $B \ge 1$ back queues are free and empty. The loop of line L3 stopped, and Free is not empty, so no URL is in a front queue. $\square$

A crawl that adds the links of each fetched page and stops when NEXT returns nothing and no fetch is still running therefore fetches every URL that is reachable from the seeds. If a reachable URL were never fetched, take the first one on a link path from a seed; the page before it on the path was fetched, so the URL was added and is in Seen, and by claim 3 it is either waiting, which Theorem 2 rules out at the end, or returned.

**Theorem 3 (politeness).** If NEXT returns a URL of host $h$ with start time $s$, then any URL of $h$ that NEXT returns later has a start time of at least $s + \delta(h)$.

*Proof.* When the URL with start $s$ is returned, line L5 has removed the only heap entry of the queue of $h$, and line L7 sets $\mathrm{next}(h) = s + \delta(h)$. Until $h$ is served again, next$(h)$ does not change, because line L7 changes next only for the host it serves. A later URL of $h$ is served from a heap entry $(t, j)$ with owner $h$ that was inserted after this point, at line L8 or at line L15, so $t \ge \mathrm{next}(h) = s + \delta(h)$ by claim 4 of Lemma 1. Line L6 gives the start time $\max(\mathit{now}, t) \ge t$. $\square$

The map next keeps the time even after the host loses its back queue. Without it, a host whose queue empties and whose new URL arrives soon after could get a fresh queue with the time now and be contacted again too early. The test file has this case.

**Theorem 4 (order of the front stage).** URLs leave each front queue in the order in which they entered it. With the strict selector, a URL leaves the front stage only when all front queues of higher priority are empty.

*Proof.* Line L2 appends at the tail and line L13 removes the head, so each front queue is FIFO. The strict selector at line L12 takes the least $i$ with $F_i$ not empty. $\square$

The order in which URLs are fetched is not the priority order. A URL of a host that must wait stays in its back queue, and URLs of other hosts, perhaps of lower priority, go first. Priority decides which URLs enter the back stage first; politeness decides when they leave it.

**Cost.** ADD costs $O(1)$ expected time with a hash set for Seen. Each URL moves once from the front stage to the back stage, and each move costs $O(F)$ for the selector plus $O(1)$ expected for the host lookup. Each REFILL inserts at most one heap entry, and each NEXT extracts one, so the heap work is $O(\log B)$ for each URL moved and each call of NEXT. For a crawl with $U$ distinct URLs and $R$ calls of NEXT, the total time is $O(U (F + \log B) + R \log B)$ expected. The space is $O(U + B + H)$, where $H$ is the number of hosts in the map next.
