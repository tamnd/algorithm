---
title: DGIM keeps the bucket rule and answers with relative error below 1/k
proves: [correctness]
status: full
---

We use the notation of the page: $L = \lceil k/2 \rceil \ge 1$, $t$ is the current time, $W$ is the window size, and level $j$ holds the buckets of size $2^j$. Let $p_1 < p_2 < \cdots < p_M$ be the positions of the 1s read so far. Let $n_j$ be the number of buckets at level $j$, and let $r^*$ be the largest level with $n_j > 0$.

**Invariants.** After each call of DGIM-UPDATE:

- (I1) There is an index $q$ such that the buckets, from the oldest to the newest, cover consecutive blocks of $p_{q+1}, \ldots, p_M$, in order. The size of each bucket is the length of its block, and its timestamp is the last position of its block.
- (I2) Each bucket has timestamp greater than $t - W$.
- (I3) Each 1 that is in no bucket, $p_1, \ldots, p_q$, has position at most $t - W$.
- (I4) The sizes do not decrease from the newest bucket to the oldest one.
- (I5) If there is a bucket, then $L \le n_j \le L + 1$ for $0 \le j < r^*$, $1 \le n_{r^*} \le L + 1$, and $n_j = 0$ for $j > r^*$.

**Lemma 1.** The invariants hold after each update.

*Proof.* Before the first bit there are no buckets, $q = M = 0$, and all invariants hold. Assume that they hold before an update at time $t$, that is, with the current time $t - 1$.

Line L1 sets the time to $t$. By (I2) each bucket had timestamp greater than $t - 1 - W$, so at least $t - W$. Timestamps are distinct positions, and by (I1) they increase from the oldest bucket to the newest. So only the oldest bucket can have timestamp $t - W$. Line L2 removes it in that case. After L2, (I2) holds at time $t$. The removed block is the first block of (I1), so (I1) holds with a larger $q$. The 1s of that block have positions at most its timestamp $t - W$, so (I3) holds; the 1s that were already in no bucket have positions at most $t - 1 - W < t - W$. (I4) holds because a bucket was removed from one end. For (I5), the removed bucket is the oldest one, so by (I4) it has the largest size, level $r^*$. If $n_{r^*}$ stays at least 1, (I5) holds. If it drops to 0 and $r^* \ge 1$, the new largest level is $r^* - 1$, whose count is $L$ or $L + 1$, in $[1, L + 1]$. If it drops to 0 and $r^* = 0$, there are no buckets.

If the bit is 0, nothing else changes, and the invariants hold. If the bit is 1, then $p_M = t$ is the new last 1, and line L4 adds the block $\{t\}$ at the newest end. (I1) holds, its timestamp $t$ is greater than $t - W$ for (I2), and it has the smallest size 1 for (I4).

Line L7 removes the two oldest buckets of level $j$. By (I4) the buckets of one size are consecutive in the order, so these two buckets are neighbours, and their blocks are consecutive. The union is one block of length $2^{j+1}$, and the new bucket takes the timestamp of the newer one, which is the last position of the union, so (I1) holds. Its timestamp is one of the old timestamps, so (I2) holds. The new bucket is older than the buckets left at level $j$ and newer than the buckets of level $j + 1$, which are older by (I4). It is placed as the newest bucket of level $j + 1$, so (I4) holds.

For (I5), consider the loop of lines L6 to L8. We show by induction over the iterations: when the loop examines level $j$, all levels $i < j$ have $n_i = L$, and $n_j$ is one more than its value before the update, while all levels above $j$ have their values from before. At the first test, $j = 0$ and line L4 added one bucket to level 0. If $n_j = L + 2$, line L7 leaves $n_j = L$ and adds one bucket to level $j + 1$, which is the claim for $j + 1$. The loop stops at the first level $j$ with $n_j \le L + 1$, after at most $r^* + 2$ tests, since a level above the largest one starts at 0 and reaches at most 1. At the stop, three cases:

- $j < r^*$: before the update $n_j \in \{L, L + 1\}$, so now $n_j = L + 1$; the levels below are at $L$ and the levels above are unchanged. (I5) holds with the same $r^*$.
- $j = r^*$: before the update $1 \le n_j \le L + 1$, so now $2 \le n_j \le L + 1$, and (I5) holds.
- $j > r^*$: then $j = r^* + 1$, or $j = 0$ when there were no buckets. Level $j$ now has 1 bucket and is the new largest level, and every level below has $L$ buckets. (I5) holds. $\square$

**Lemma 2 (the answer).** Let $1 \le w \le W$, let $c$ be the number of 1s among the last $w$ positions, and let $\hat c$ be the value of DGIM-QUERY$(w)$. If $c = 0$ then $\hat c = 0$. If $c \ge 1$ then
$$|\hat c - c| \le \frac{2^r - 1}{2} \quad\text{and}\quad \frac{|\hat c - c|}{c} \le \frac{2^r - 1}{2(L(2^r - 1) + 1)} < \frac{1}{2L} \le \frac{1}{k},$$
where $2^r$ is the size found in line L10.

*Proof.* The 1s in no bucket have positions at most $t - W \le t - w$ by (I3), so they are outside. A bucket with timestamp at most $t - w$ has all its 1s at positions at most $t - w$, so outside. If $B$ of line L9 is empty, then $c = 0$ and the query returns 0.

Otherwise let $O$ be the oldest bucket of $B$, of size $2^r$. By (I1) the buckets newer than $O$ hold 1s at positions after the timestamp of $O$, which is greater than $t - w$; so all their 1s are inside, and they are exactly the other buckets of $B$. The bucket $O$ has its newest 1 inside, and possibly some of its other 1s. So $c = S + x$ with $1 \le x \le 2^r$. The estimate is $\hat c = S + (2^r + 1)/2$, so $|\hat c - c| = |(2^r + 1)/2 - x| \le (2^r - 1)/2$. If $r = 0$, this is 0.

If $r \ge 1$, then $r \le r^*$, so each level $j < r$ is below the largest level and has at least $L$ buckets by (I5). By (I4) these buckets are newer than $O$, whose size is larger, so they are in $B$ and count in $S$. So $S \ge L \sum_{j < r} 2^j = L(2^r - 1)$ and $c \ge S + 1 \ge L(2^r - 1) + 1$. Then
$$\frac{|\hat c - c|}{c} \le \frac{2^r - 1}{2(L(2^r - 1) + 1)} < \frac{2^r - 1}{2L(2^r - 1)} = \frac{1}{2L}.$$
Finally $2L = 2\lceil k/2 \rceil \ge k$. $\square$

**Lemma 3 (the number of buckets).** After each update the number of buckets is at most $(L + 1)(\rho + 1)$, where $\rho = \lfloor \log_2((W - 1)/L + 1) \rfloor$.

*Proof.* If there are buckets, apply the proof of Lemma 2 with $w = W$. By (I2) all buckets are in $B$, and $O$ is the oldest bucket, of size $2^{r^*}$. The window holds at most $W$ bits, so $W \ge c \ge L(2^{r^*} - 1) + 1$ (for $r^* = 0$ this reads $W \ge 1$). So $2^{r^*} \le (W - 1)/L + 1$ and $r^* \le \rho$. By (I5) each of the levels $0, \ldots, r^*$ has at most $L + 1$ buckets. $\square$

**Space.** By (I2) each kept timestamp $\tau$ satisfies $t - W < \tau \le t$, so the age $t - \tau$ is in $\{0, \ldots, W - 1\}$, and $\tau \bmod W$ with $t \bmod W$ gives it. At line L2 the oldest bucket has age in $\{1, \ldots, W\}$, because it was created before time $t$; an age that is $0 \bmod W$ there means $W$. So a timestamp takes $\lceil \log_2 W \rceil$ bits. A level is a circular array of $L + 2$ slots with a count, so the size of a bucket is not stored. The levels number at most $\rho + 2 \le \log_2 W + 2$, the counts need $O(\log k)$ bits each, and $t \bmod W$ and the total of the sizes (at most $W + 2^{\rho}$, which is less than $2W$) need $O(\log W)$ bits. With Lemma 3 and $L \le (k + 1)/2$, the space is $O(k \log^2 W)$ bits.

**Time.** Each merge in line L7 removes two buckets and adds one, so it lowers the number of buckets by one. Line L4 adds one bucket, once for each 1. The number of buckets is never negative, so after any prefix with $M$ ones there have been at most $M$ merges. Each update does $O(1)$ work besides its merges, so $m$ updates cost $O(m + M) = O(m)$, which is $O(1)$ amortized per bit. One update does at most $r^* + 1 \le \rho + 1 = O(\log W)$ merges, by the proof of Lemma 1. A query with $w = W$ needs the total and the size of the oldest bucket, $O(1)$; a query with $w < W$ scans at most $(L + 1)(\rho + 1) = O(k \log W)$ buckets. $\square$
