---
title: SHARDS gives unbiased distances, is exact at rate 1, and its fixed-size form matches the fixed rate of its current threshold
proves: [correctness]
status: full
---

We use the pseudocode of the page. The trace is $\sigma_1 \cdots \sigma_n$. For a request $t$ to an item $L$ that was used before, let $D_t$ be its true [reuse distance](/reuse-distance/), the number of distinct other items requested since the previous request for $L$, and let $W_t$ be that set of items, so $|W_t| = D_t$. Write $T_x = \mathrm{hash}(x) \bmod P$.

## 1. The distance among sampled items

**Claim 1.** Let $S_T = \{x : T_x < T\}$. If $L \in S_T$, the number of distinct sampled items since the previous request for $L$ is $d_t = |W_t \cap S_T|$, and line L2 returns it.

*Proof.* Line L1 lets through exactly the requests to items of $S_T$, and it lets through all of them. So the subsequence seen by line L2 is the trace restricted to $S_T$. In this subsequence, the items between the two requests for $L$ are the items of $W_t$ that are in $S_T$, and no others.

Line L2 keeps one mark for each item seen, at the time of its last use, in a [Fenwick tree](/fenwick-tree/). When $L$ is requested again, its mark is at the time $p$ of its previous use. Each mark after $p$ belongs to a different item, used after $p$, and each item used after $p$ has its last use after $p$, so it has its mark there. So the number of marks after $p$ is $d_t$. The code counts them as the number of marks in total minus the prefix sum up to $p$. A compaction renumbers the marks in the same order, so it does not change any of these counts. $\square$

**Claim 2.** Model the hash as a random function, so that each $T_x$ is uniform on $\{0, \ldots, P - 1\}$, independently. Then for a request $t$ with $D_t$ finite, $\mathbb{E}[\,d_t \mid L \in S_T\,] = R \cdot D_t$ with $R = T/P$.

*Proof.* The items of $W_t$ are different from $L$, so their hashes are independent of $T_L$. Each of them is in $S_T$ with probability $T/P = R$. By linearity of expectation, $\mathbb{E}[d_t \mid L \in S_T] = \sum_{x \in W_t} \Pr[x \in S_T] = R\,D_t$. $\square$

So the scaled distance $d_t / R = d_t \cdot P/T$ of line L7 is an unbiased estimate of $D_t$. An LRU cache of size $c$ hits request $t$ when $D_t < c$, and line L9 counts the share of sampled requests whose scaled distance is below $c$. Each item is in the sample with probability $R$, so each request is too, and the share of sampled requests that hit is an estimate of the share of all requests that hit. The estimate is not exact: the number of sampled requests varies, mostly because a few popular items carry many requests. SHARDS_adj moves the difference between the expected number $nR$ and the actual number of sampled requests into the first bucket.

## 2. Rate 1 is exact

With $T = P$, each $T_x < P$, so each item is sampled, $d_t = D_t$, and the scaled distance is $D_t$ itself. The histogram is the exact histogram of reuse distances, and line L9 gives $m(c) = 1 - \frac{1}{n} |\{t : D_t < c\}|$, the exact LRU curve. Cold requests go to the cold count in both. $\square$

## 3. The fixed-size form

**Claim 3.** In fixed-size SHARDS, after each request: (a) the threshold $T$ never rose; (b) the set of items with a mark is exactly the set of items seen so far with $T_x < T$; (c) it has at most $s_{\max}$ items.

*Proof.* By induction. At the start nothing is seen and the set is empty.

A request to an item with $T_x \ge T$ changes nothing, and (b) holds since such an item is not in the set. A request to an item already in the set changes only marks. A request to a new item $L$ with $T_L < T$ adds $L$; now the set is the items seen with $T_x < T$, of size at most $s_{\max} + 1$. If the size is $s_{\max} + 1$, lines L4 and L5 let $T_{\max}$ be the largest $T_x$ in the set, remove each item with $T_x = T_{\max}$, and set $T = T_{\max}$. The items that stay are those with $T_x < T_{\max}$, which are exactly the items seen with $T_x$ below the new $T$, so (b) holds. At least one item left, so (c) holds. The new $T$ is at most the old one, which gives (a). $\square$

**Consequence.** Since $T$ only falls, an item with $T_x$ below the current $T$ had $T_x$ below each earlier threshold, so each of its requests was seen and marked. A removed item has $T_x \ge T$ and is never seen again, and its mark is gone. So at each time the marks are those that fixed-rate SHARDS with the current $T$ would hold, and line L2 returns the same distance as fixed-rate SHARDS with rate $T/P$. This is the subset property of the paper: lowering $T$ only removes items, and keeps the full history of the rest.

**The rescale.** A count added while the threshold was $T_{\text{old}}$ stands for about $P/T_{\text{old}}$ requests. After the threshold falls to $T$, a count stands for $P/T$ requests. Multiplying the old count by $T/T_{\text{old}}$ keeps the number of requests it stands for. The code does this lazily: each bucket stores the threshold of its last update and is rescaled when it is next touched or read. The total count is rescaled in the same way, so the ratio of line L9 uses one scale for all buckets.

## 4. Cost

Each request computes one hash, in $O(1)$ time. A sampled request does $O(1)$ Fenwick tree updates and queries over at most $2s + 16$ positions, where $s$ is the number of items with a mark, so $O(\log s)$ time. The marks are renumbered when the array fills; the new array has room for $s + 16$ more uses, so each renumbering of $O(s \log s)$ cost is paid by at least $s + 16$ earlier sampled requests, $O(\log s)$ each. In the fixed-size form a heap of the sampled items gives $T_{\max}$, and each item enters and leaves it at most once. The space is $O(s)$ plus the histogram.
