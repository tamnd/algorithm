---
title: The buffer pool never evicts a pinned page, never loses a reported change, and its CLOCK victim search ends
proves: [correctness]
status: full
---

We use the notation of the page: $B$ frames, the page table $table$, and for each frame $f$ its page $page(f)$ (or none), its pin count $pin(f)$, its dirty bit $dirty(f)$ and, for CLOCK, its reference bit $ref(f)$. Let $disk(p)$ be the bytes of page $p$ on disk and $mem(f)$ the bytes in frame $f$. The *current value* of page $p$ is $mem(table[p])$ if $p$ is in the table, and $disk(p)$ otherwise.

Callers follow the protocol of the page: they change the bytes of a frame only while they hold a pin on it, and they report each change by `unpin(p, true)` before their last unpin of that page.

**Invariant.**

1. $table[p] = f$ if and only if $page(f) = p$, and no page is in two frames.
2. $pin(f) \ge 0$ for every frame, and $pin(f)$ is the number of fetches of $page(f)$ that have not been unpinned yet.
3. If $page(f) = p$, $pin(f) = 0$ and $dirty(f)$ is false, then $mem(f) = disk(p)$.

Part 3 states that a clean unpinned frame holds the same bytes as the disk. A pinned frame may hold changes that are not reported yet; they are reported before the pin count can return to zero.

**Lemma 1.** VICTIM returns only a frame $f$ with $pin(f) = 0$, and FETCH fails at line L7 only if every frame is pinned.

*Proof.* For LRU, VICTIM picks among the frames with pin count zero by definition. For CLOCK, line L19 is reached only after the test at line L17. VICTIM is called only when no frame is free; if no frame has pin count zero, the implementation reports this before the search, which is the failure at line L7. $\square$

**Lemma 2 (termination of CLOCK).** If some frame has pin count zero, VICTIM for CLOCK returns after at most $2B$ steps.

*Proof.* Pin counts do not change during the search. Let $U$ be the nonempty set of frames with pin count zero. In the first $B$ steps the hand visits every frame once. Each frame of $U$ visited with a clear bit is returned at once. Otherwise every frame of $U$ had its bit set and is cleared on its visit, so in the next $B$ steps the hand reaches a frame of $U$ with a clear bit and returns it. $\square$

**Lemma 3.** FETCH, UNPIN, `new_page` and `flush` keep the invariant.

*Proof.* *FETCH on a hit* (lines L1 to L3) adds one pin and one outstanding fetch, which keeps part 2, and changes no bytes. *FETCH on a miss* uses a free frame or a victim $f$ with $pin(f) = 0$ (Lemma 1). If $f$ held a page $q$ and was dirty, line L8 writes $mem(f)$ to disk, so $disk(q)$ becomes the current value of $q$; if it was clean, part 3 already gives $mem(f) = disk(q)$. In both cases, removing $q$ from the table at line L9 does not change the current value of $q$, which is now $disk(q)$. Lines L10 and L11 read $p$ (which was not in the table) into $f$ and set the table entry, so part 1 holds; the pin count is 1 for the one outstanding fetch; and $mem(f) = disk(p)$ with a clear dirty bit, so part 3 holds once the pin is gone if no change is reported. *UNPIN* lowers the pin count by one for one outstanding fetch, and sets the dirty bit if the caller reports a change. If the pin count reaches zero with a clear dirty bit, no caller reported a change since the frame was last clean, so by the protocol no caller changed it, and part 3 holds. *new_page* allocates a page and fetches it with the dirty bit set, so part 3 does not apply to it. *flush* writes a dirty frame and clears its bit, so then $mem(f) = disk(p)$. $\square$

**Theorem.** Under the protocol, starting with all frames free:

(a) a page with a positive pin count stays in the same frame until its pin count returns to zero;

(b) for every page $p$, at every moment when no caller holds a pin on $p$, the current value of $p$ is the value after the last reported change to $p$, or $disk(p)$ at the start if there was none; and after `flush_all`, $disk(p)$ is that value;

(c) the number of disk reads equals the number of misses, and the number of disk writes equals the number of dirty victims plus the number of flushes of dirty frames.

*Proof.* (a) A frame changes its page only at lines L9 to L11 on a miss, and the frame is a victim, which has pin count zero by Lemma 1.

(b) A reported change is a change to $mem(f)$ while $f$ is pinned, followed by setting $dirty(f)$. The frame stays with $p$ while it is pinned, by (a). After that, the bytes of $p$ in memory can leave the pool only at line L8, which writes them to disk because the bit is set. So the current value of $p$ is always the last reported value. `flush_all` writes every dirty frame, and by part 3 every clean frame already agrees with the disk, so afterwards the disk holds the current value of every page.

(c) Line L10 is the only read and runs once per miss (`new_page` does not read). Line L8 and `flush` are the only writes, and each runs only for a dirty frame. $\square$

**The CLOCK step count.** Suppose no frame is pinned during any victim search, as in a sequence where each request is fetched and unpinned at once. Each step of the hand either clears a reference bit or returns a victim. A reference bit is set once per request (a hit or a miss records a use), and a bit can be cleared only after it was set, so over $n$ requests the steps that clear a bit number at most $n$, and the steps that return a victim number at most $m$, the number of misses. So the total work of all victim searches is at most $n + m \le 2n$ steps, which is $O(1)$ amortized per request.

**LRU and the sequential loop.** With $B$ frames and a loop over $B + 1$ pages $0, 1, \ldots, B$, repeated, every request of LRU misses. *Proof.* After the first $B + 1$ requests, and at each later request of page $j$, the pool holds the $B$ pages used most recently, which are the $B$ pages other than $j$, since $j$ was used $B + 1$ requests ago and every other page more recently. So $j$ is not in the pool. $\square$
