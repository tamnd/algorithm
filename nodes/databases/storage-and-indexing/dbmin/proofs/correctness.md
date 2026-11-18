---
title: DBMIN keeps its locality sets within their bounds and isolated, always finds a free frame, and MRU gains at least l - 1 hits per pass of a loop
proves: [correctness]
status: full
---

We use the notation of the page: $B$ frames; for each locality set $L$ of an active query, its bound $l(L)$, its pages $P(L)$ and its size $r(L) = |P(L)|$; the global table $G$ of the pages in memory, with $owner(p)$ either a set or none; and the free list $F$, a list of frames that hold either a page with no owner or nothing. Let $\Lambda = \sum_L l(L)$ over the sets of active queries.

**Invariant.**

1. Every page of $G$ is in exactly one frame. A page with an owner $L$ is in $P(L)$ and not on $F$; a page with no owner is on $F$. So the sets $P(L)$ are disjoint, and the frames are split between the sets and $F$: $\sum_L r(L) + |F| = B$.
2. $r(L) \le l(L)$ for every active set.
3. $\Lambda < B$, or there is no active query.

**Lemma 1.** If the invariant holds when line L8 runs, the free list is not empty.

*Proof.* By parts 1 to 3, $|F| = B - \sum_L r(L) \ge B - \Lambda \ge 1$. $\square$

**Lemma 2.** REQUEST keeps the invariant.

*Proof.* In the first case (lines L1 to L3) only usage statistics change. In the shared case (lines L4 and L5) nothing changes. Otherwise $p$ becomes a page of $L$: either it was on $F$ with no owner and line L6 removes it, or line L8 takes a frame from $F$ (possible by Lemma 1) and drops the page it held from $G$, so that page leaves memory, and line L9 reads $p$ into the frame. At this point the frame of $p$ is in neither $F$ nor any set, so $\sum_L r(L) + |F| = B - 1$. If $r(L) = l(L)$, lines L11 and L12 move the victim $q \in P(L)$ to $F$ with no owner, which keeps the sum at $B - 1$ and makes $r(L) = l(L) - 1$. Line L13 adds $p$ to $L$, which restores the sum to $B$ and gives $r(L) \le l(L)$. Every page still has one frame and one place, so part 1 holds; part 3 does not change. $\square$

**Lemma 3.** START and FINISH keep the invariant.

*Proof.* START activates a query only if $\Lambda$ plus its bounds is less than $B$, and its new sets are empty, so parts 1 to 3 hold after it. FINISH moves the pages of the query's sets to $F$ with no owner, which keeps part 1, and lowers $\Lambda$; each activation at line L19 passes the same test as START. $\square$

**Theorem 1 (isolation).** The pages of a locality set $L$ change only during requests made through $L$. In particular, no request of another query removes a page from $P(L)$, and a running query never waits for frames.

*Proof.* Pages enter $P(L)$ only at line L13 and leave only at line L11, both in a request through $L$, or when the query of $L$ finishes. Lines L6 and L8 of other requests take pages only from $F$, which by part 1 holds no page of $P(L)$. By Lemma 1 a request always finds a frame, so it never waits. $\square$

**Theorem 2 (sets as separate caches).** Suppose no page is requested through two different sets while it is in memory (no sharing). Then, after every request, $P(L)$ is exactly the content of a separate cache of $l(L)$ pages that runs the policy of $L$ on the requests made through $L$. The number of disk reads is at most the sum, over the sets, of the misses of those separate caches.

*Proof.* Without sharing, line L4 is never true. So for each request through $L$ of page $p$, if $p \in P(L)$ the statistics are updated, which is what the separate cache does on a hit; otherwise $p$ joins $P(L)$, and if the set was full the policy's victim among the old pages leaves first, which is what the separate cache does on a miss. By induction over the requests through $L$, the two contents are equal, and the policy statistics agree too. A disk read happens at line L9 only if $p$ is not in memory, so in particular $p \notin P(L)$, which is a miss of the separate cache. $\square$

**Theorem 3 (MRU on a loop).** Consider a separate cache of $l \ge 2$ pages with the MRU policy, and the requests $0, 1, \ldots, L - 1$, repeated, with $L > l$. Every pass after the first has at least $l - 1$ hits. LRU with $l$ pages on the same requests has no hits at all.

*Proof.* After each request, the page just requested is in the cache and is the most recently used one. Let $K$ be the cache without the page of the last request. After the first $l$ requests the cache is full and $|K| = l - 1$, and $|K|$ stays $l - 1$:

- On a miss for $p$, the victim is the most recently used page, the page $p'$ of the previous request, and $p$ takes its place. So $K$ does not change.
- On a hit for $p$, $p$ was in $K$ (it is not $p'$, since consecutive requests differ when $L \ge 2$). Now $p$ is the last page and $p'$ joins $K$. So $K$ loses $p$ and gains $p'$.

So a page leaves $K$ only when it is requested, and then the request is a hit. At the start of any pass after the first, $K$ holds $l - 1$ pages. Each of them is requested once during the pass, and until it is requested it stays in $K$, so that request is a hit. This gives at least $l - 1$ hits in the pass.

For LRU, at a request of page $p$ after the first $l$ requests, the cache holds the $l$ pages requested most recently. They are the $l$ requests just before, which are $l$ distinct pages other than $p$, because $p$ was last requested $L > l$ requests earlier. So every request misses. $\square$

By Theorem 2, a looping file instance in DBMIN with an MRU set of size $l$ has at most $L - l + 1$ disk reads per pass after the first, and the free list can only save more.

**What is not proved.** The sizes and policies of the table on the page are rules from the paper, justified by the reference patterns and by simulation. Whether DBMIN gives more throughput than another policy depends on the workload; Chou and DeWitt measured it, and this note proves only the invariants and the loop bound above.
