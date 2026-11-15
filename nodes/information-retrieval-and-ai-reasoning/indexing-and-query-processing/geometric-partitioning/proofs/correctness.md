---
title: Geometric partitioning keeps all postings, follows a radix-r counter, and writes each posting at most (r-1)(1 + floor(log_r m)) times
proves: [correctness, complexity]
status: full
---

Fix the radix $r \ge 2$ and the buffer size $b \ge 1$. Let $X$ be the set of postings added so far, all distinct, with $|X| = T = mb + s$ and $0 \le s < b$. So $m$ is the number of flushes. Write $m = \sum_{k \ge 1} \delta_k r^{k-1}$ with base-$r$ digits $0 \le \delta_k \le r - 1$. We show that after each call of GEOM-ADD:

> **(G1)** the buffer $Z$ holds $s$ postings;
>
> **(G2)** partition $P_k$ holds exactly $\delta_k r^{k-1} b$ postings, for each $k \ge 1$;
>
> **(G3)** $Z$ and the partitions are pairwise disjoint, sorted, and their union is $X$.

1. **Base.** With $X$ empty, $m = s = 0$, all digits are 0 and all partitions are empty.

2. **A call with no flush.** Line L1 adds the new posting to $Z$ in sorted position. If $|Z| < b$ after that, nothing else changes, $s$ grows by one, $m$ does not change, and the posting is new. (G1) to (G3) hold.

3. **A call with a flush.** Else $|Z| = b$ after line L1. The capacity of $P_k$ is $(r - 1) r^{k-1} b$, and by (G2) $P_k$ is at capacity exactly when $\delta_k = r - 1$. Lines L3 and L4 find the least $k$ with $\delta_k < r - 1$. Such a $k$ exists because $m$ has finitely many nonzero digits. So $\delta_1 = \cdots = \delta_{k-1} = r - 1$. The merge of line L5 has $b + \sum_{i=1}^{k-1} (r - 1) r^{i-1} b + \delta_k r^{k-1} b = b + (r^{k-1} - 1) b + \delta_k r^{k-1} b = (\delta_k + 1) r^{k-1} b$ postings. In base $r$, adding 1 to $m$ turns the $k - 1$ low digits $r - 1$ into 0, adds 1 to digit $k$, which is at most $r - 1$ after the change, and leaves the higher digits alone. So after line L6, with $P_1, \ldots, P_{k-1}$ and $Z$ empty and $P_k$ holding the merge result, (G2) holds for $m + 1$, and (G1) holds with $s = 0$. The merge of sorted disjoint lists gives their sorted union, and the postings of the merged sources are moved, not copied, so (G3) holds.

4. **Queries.** By (G3), the list of a term over $X$ is the disjoint union of its lists in $Z$ and in each partition. Lines L7 and L8 return it in document order.

5. **The size of each merge.** Let flush number $t$ be the one that takes the count from $t - 1$ to $t$. The low digits of $t - 1$ that equal $r - 1$ are the low digits of $t$ that equal 0, so $k - 1 = v_r(t)$, the number of times $r$ divides $t$, and by step 3 the merge writes $(\delta_k + 1) r^{k-1} b = (t \bmod r^{k}) \, b$ postings, where $\delta_k + 1$ is digit $k$ of $t$. The total after $m$ flushes is $b \sum_{t=1}^{m} (t \bmod r^{v_r(t) + 1})$.

6. **Writes of one posting.** A posting is written once in each flush that includes it in line L5. Fix a level $k$. The posting enters $P_k$ in some flush, which sets digit $k$ to some value $\delta \ge 1$ and writes the posting once. While it stays in $P_k$, it is written again only by flushes that stop at level $k$, and each of them adds 1 to digit $k$. A flush that stops at a higher level moves the posting out of $P_k$ for good, because partitions only move postings to higher levels. Digit $k$ can grow from $\delta$ to at most $r - 1$, so the posting is written at most $1 + (r - 1 - \delta) \le r - 1$ times at level $k$. A flush can reach level $k$ only when $m \ge r^{k-1}$, so the levels used satisfy $k \le 1 + \lfloor \log_r m \rfloor$. Hence each posting is written at most $(r - 1)(1 + \lfloor \log_r m \rfloor)$ times, and the total over all postings is at most $T (r - 1)(1 + \lfloor \log_r m \rfloor)$.

7. **The number of partitions.** By (G2), the nonempty partitions are those with a nonzero digit, so at most $1 + \lfloor \log_r m \rfloor$ of them exist, and a query reads at most that many partitions plus the buffer. $\blacksquare$
