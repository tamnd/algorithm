---
title: CLOCK keeps a valid cache, is FIFO without reuse, and misses at most k times as often as MIN
proves: [correctness]
status: full
---

We use the pseudocode of the page, with the bit set at load (line L11), a cache of capacity $k \ge 1$ that starts empty, and a request sequence $\sigma_1 \ldots \sigma_n$. Say that the hand *passes* frame $i$ when line L8 or line L10 runs with $h = i$. Only a pass can change the page in a frame or clear a bit.

**Claim 1 (validity).** After each request, the frames in use hold distinct pages, exactly the cached pages, the requested page is among them, and at most $k$ frames are in use. Each miss with a full cache ends.

*Proof.* By induction on the requests. A hit changes one bit. A miss with a free frame puts $p$ in it; $p$ was not cached, so the pages stay distinct. A miss with a full cache runs the loop of lines L7 to L9. Each pass at line L8 clears a bit, and no bit is set during the loop, so after at most $k$ steps the hand meets a clear bit and the loop ends. Lines L10 and L11 replace one page by $p$, which was not cached. $\square$

**Claim 2 (second chance queue).** While the cache is full, let $Q$ be the list of pages read from the frame at the hand around the circle. Then CLOCK acts on $Q$ as follows: a hit sets the bit of the page; at a miss, while the head of $Q$ has a set bit, it moves to the tail with a clear bit; then the head is removed and $p$ is added at the tail with a set bit.

*Proof.* Line L8 clears the bit at the hand and line L9 moves the hand one step, so the old head is now read last: it moved to the tail. Line L11 replaces the head by $p$, and line L12 moves the hand past it, so the old head is gone and $p$ is read last. $\square$

When the cache becomes full, $h = 0$ and frames $0, \ldots, k - 1$ hold the pages in load order, so $Q$ starts in load order. The tests check CLOCK against a direct implementation of this queue.

**Claim 3 (FIFO without reuse).** If no request of $\sigma$ is a hit for CLOCK, CLOCK evicts the same pages as FIFO, at the same times, so FIFO has no hit either.

*Proof.* Without hits, a bit is set only at a load. While the cache is full, we show by induction that $Q$ is a list of pages with a clear bit, in load order, followed by pages with a set bit, in load order, and that each page with a clear bit was loaded before each page with a set bit. This holds when the cache becomes full, with all bits set. At a miss, if the head has a clear bit, it is the oldest load; it is evicted and $p$ is added at the tail with a set bit, which keeps the form. If the head has a set bit, there is no page with a clear bit, so all $k$ bits are set. The loop moves all $k$ pages to the tail in turn, which gives the same order with all bits clear, and then the head, the oldest load, is evicted and $p$ is added. Again the form holds. In both cases the victim is the oldest load, which is the FIFO victim. Since the two caches start equal and evict the same pages, they hold the same pages at all times and have the same hits. $\square$

If each page comes back only after at least $k$ other distinct pages, FIFO has no hit, and by the claim CLOCK also has none and agrees with FIFO. The tests check this case.

**Claim 4 (conservative).** Let $\tau$ be a contiguous part of $\sigma$ that requests at most $k$ distinct pages. Then CLOCK has at most $k$ misses on the requests of $\tau$.

*Proof.* We show that no page misses twice inside $\tau$. If $k = 1$, a second miss on $p$ needs a request to another page between the two, so $\tau$ requests two distinct pages, a contradiction. Let $k \ge 2$, and assume that page $p$ misses at times $t_1 < t_2$ inside $\tau$. At $t_1$, $p$ is loaded into a frame $f$ with a set bit, and the hand moves to the next frame. Let $e$ be the time when $p$ is evicted, with $t_1 < e < t_2$, by a miss on a page $q$. At $e$ the hand passes $f$ and the bit of $f$ is clear. The bit was set at $t_1$, so some earlier pass over $f$ after $t_1$ cleared it; let $e_1$ be the last such pass before the eviction.

Between the pass at $e_1$ and the eviction at $e$, the hand passes each frame $j \ne f$ exactly once; call this the second pass of $j$. The hand also passed $j$ once in the turn that ended at $e_1$, which started at frame $f + 1$ after the load at $t_1$; call it the first pass of $j$. Both passes are after the load at $t_1$ and before the eviction at $e$. Let $x$ be the page in frame $j$ just after its second pass.

- If the second pass evicts, $x$ is loaded there at a miss at a time in $(t_1, e]$, and in fact before $e$, because the miss at $e$ loads $q$ into $f$.
- If the second pass clears the bit, $x$ was in $j$ with a set bit. Since the first pass, the page in $j$ did not change, so $x$ was either loaded at the first pass or kept there with a clear bit and then hit. In both cases $x$ was requested at a time in $(t_1, e)$.

No pass over $j$ happens between its second pass and $e$, so $x$ is still cached at $e$. So just before the miss at $e$, the other $k - 1$ frames hold pages that were requested in $(t_1, e)$. They are distinct from each other and from $p$, by claim 1. The page $q$ is requested at $e$ and is not cached just before, so it differs from all of them. So the part $[t_1, e]$ of $\sigma$, which is inside $\tau$, requests at least $k + 1$ distinct pages: $p$, the $k - 1$ others and $q$. This contradicts the hypothesis. So each of the at most $k$ distinct pages of $\tau$ misses at most once in $\tau$. $\square$

**Claim 5 (the bound).** $\mathrm{CLOCK}_k(\sigma) \le k \cdot \mathrm{MIN}_k(\sigma)$, with both caches empty at the start.

*Proof.* Cut $\sigma$ into phases, each the longest part, from where the last one ended, with at most $k$ distinct pages. Let $m$ be the number of phases. By claim 4, CLOCK has at most $k m$ misses. Each phase except the last, together with the first request of the next phase, requests $k + 1$ distinct pages; this forces a miss of any policy with $k$ pages in each of $m - 1$ disjoint windows that do not hold the first request of $\sigma$, which is a miss too. This is the count on the [FIFO](/fifo-replacement/) page. So MIN has at least $m$ misses, and the bound follows. $\square$

**The bit at load matters.** Claim 4 uses the set bit at load: it is what protects $p$ at the first pass over $f$. If a page is loaded with a clear bit, the hand can evict it at the first pass, and the claim fails. With $k = 2$, on $(0, 0, 1, 2, 1, 1, 0, 2, 0)^m$, that variant misses 6 times per round after the first, while MIN misses twice per round, so its ratio tends to 3, larger than $k$.

**Cost.** A hit is a hash lookup and one bit write. At a miss, each step of the hand except the last clears a bit. A bit is set only by a request, so the number of clearing steps over the whole run is at most $n$, and the number of final steps is the number of misses. So the total time is $O(n)$ expected, and one miss takes $O(k)$ in the worst case. The space is $\Theta(k)$.
