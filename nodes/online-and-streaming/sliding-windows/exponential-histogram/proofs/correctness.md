---
title: The exponential histogram keeps the window sum with relative error below 1/k
proves: [correctness]
status: full
---

The notation is that of the page: $L = \lceil k/2 \rceil \ge 1$, $t$ is the current time, $W$ is the window size, and items are integers in $\{0, \ldots, R\}$. An item of value $v$ at time $i$ is $v$ units with timestamp $i$. List all units read so far in the order of insertion by line L4, $u_1, u_2, \ldots, u_M$; their timestamps do not decrease. Let $n_j$ be the number of buckets at level $j$, and let $r^*$ be the largest level with $n_j > 0$.

**Invariants.** After each call of EH-UPDATE:

- (I1) There is an index $q$ such that the buckets, from the oldest to the newest, cover consecutive blocks of $u_{q+1}, \ldots, u_M$, in order. The size of each bucket is the length of its block, and its timestamp is the timestamp of the last unit of its block.
- (I2) Each bucket has timestamp greater than $t - W$.
- (I3) Each unit $u_1, \ldots, u_q$ has timestamp at most $t - W$.
- (I4) The sizes do not decrease from the newest bucket to the oldest one.
- (I5) If there is a bucket, then $L \le n_j \le L + 1$ for $0 \le j < r^*$, $1 \le n_{r^*} \le L + 1$, and $n_j = 0$ for $j > r^*$.

**Lemma 1.** The invariants hold after each update.

*Proof.* With no buckets and no units, they hold. Assume that they hold before an update, and let $t$ be the new time set by line L1.

*Line L2.* Each pass removes the oldest bucket while its timestamp is at most $t - W$. It is the first block of (I1), so (I1) holds with a larger $q$. Its units have timestamps at most its own timestamp, since timestamps do not decrease along the units, so (I3) holds. When the loop stops, the oldest bucket, if any, has timestamp greater than $t - W$. By (I1) the timestamps of the buckets do not decrease from the oldest to the newest, so all of them are greater than $t - W$, and (I2) holds. (I4) holds because buckets leave from one end. For (I5): by (I4) the oldest bucket is at level $r^*$. Each removal lowers $n_{r^*}$ by one; when it reaches 0 and $r^* \ge 1$, the new largest level $r^* - 1$ has $L$ or $L + 1 \ge 1$ buckets, so (I5) holds after each pass.

*Lines L3 to L8.* Each pass of L3 appends a new unit $u_{M+1}$ with timestamp $t$, and line L4 adds the block $\{u_{M+1}\}$ at the newest end. Its timestamp $t$ is greater than $t - W$ and its size 1 is the smallest, so (I1), (I2) and (I4) hold. Line L7 joins the two oldest buckets of level $j$. By (I4) the buckets of one size are consecutive in the order, so their blocks are consecutive and their union is one block of size $2^{j+1}$. Its last unit is the last unit of the newer bucket, so the newer timestamp is the right one for (I1), and (I2) holds since the timestamp is an old one. The new bucket is older than the buckets left at level $j$ and newer than those of level $j + 1$, so it is the newest bucket of level $j + 1$, and (I4) holds. (I3) is not affected. The proof that (I5) holds after the cascade is word for word the proof of Lemma 1 of the [DGIM proof](/dgim-algorithm/): one bucket enters level 0, each level that reaches $L + 2$ drops to $L$ and passes one bucket up, and the cascade stops at a level that had $L$ (now $L + 1$), at the largest level (now at most $L + 1$), or at a new largest level with 1 bucket. $\square$

**Lemma 2 (the answer).** Let $1 \le w \le W$, let $s$ be the sum of the last $w$ items and let $\hat s$ be the value of EH-QUERY$(w)$. If $s = 0$ then $\hat s = 0$. If $s \ge 1$ then $|\hat s - s| \le (2^r - 1)/2$ and
$$\frac{|\hat s - s|}{s} \le \frac{2^r - 1}{2(L(2^r - 1) + 1)} < \frac{1}{2L} \le \frac{1}{k},$$
where $2^r$ is the size found in line L10.

*Proof.* The sum $s$ is the number of units with timestamp greater than $t - w$. The units in no bucket have timestamps at most $t - W \le t - w$ by (I3). A bucket with timestamp at most $t - w$ has all its units at timestamps at most $t - w$. So if $B$ is empty, $s = 0$ and the answer is 0.

Otherwise let $O$ be the oldest bucket of $B$, of size $2^r$. Each newer bucket holds units that come after the last unit of $O$ in the order, so their timestamps are at least the timestamp of $O$, which is greater than $t - w$; these units are all counted in $s$, and these buckets are the other buckets of $B$. The last unit of $O$ is counted in $s$, and perhaps some of its other units. So $s = S + x$ with $1 \le x \le 2^r$, and $|\hat s - s| = |(2^r + 1)/2 - x| \le (2^r - 1)/2$, which is 0 when $r = 0$.

If $r \ge 1$, each level $j < r$ is below the largest level, so it has at least $L$ buckets by (I5), and by (I4) they are newer than $O$, so in $B$. Thus $S \ge L(2^r - 1)$ and $s \ge L(2^r - 1) + 1$, which gives the bound. The last step uses $2L \ge k$. $\square$

**Lemma 3 (the number of buckets).** After each update the number of buckets is at most $(L + 1)(\rho + 1)$ with $\rho = \lfloor \log_2((WR - 1)/L + 1) \rfloor$, when $WR \ge 1$.

*Proof.* Apply Lemma 2 with $w = W$: all buckets are in $B$ by (I2), the oldest one has size $2^{r^*}$, and $WR \ge s \ge L(2^{r^*} - 1) + 1$, since the window has at most $W$ items of value at most $R$. So $r^* \le \rho$, and each of the levels $0, \ldots, r^*$ has at most $L + 1$ buckets by (I5). $\square$

**Space and time.** By (I2) each timestamp is in $(t - W, t]$, so it is determined by its residue modulo $W$ and by $t \bmod W$; the oldest bucket at line L2 has age in $\{1, \ldots, W\}$, and a residue 0 there means age $W$. So each bucket takes $\lceil \log_2 W \rceil$ bits, and by Lemma 3 the space is $O(k \log(WR) \log W)$ bits, plus $O(\log(WR))$ levels with counts of $O(\log k)$ bits and the total of $O(\log(WR))$ bits. Each merge lowers the number of buckets by one and each unit raises it by one, so the number of merges is at most the number of units; each bucket is removed by line L2 at most once. So $m$ updates with values $v_1, \ldots, v_m$ cost $O(m + \sum_i v_i)$, which is $O(1 + v)$ amortized per item of value $v$. A single unit causes at most $r^* + 1 \le \rho + 1$ merges, so one item costs $O(v \log(WR))$ plus its expiries in the worst case. $\square$
