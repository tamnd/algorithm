---
title: Each round of Manber-Myers sorts the suffixes by twice as many symbols
proves: [correctness, termination]
status: full
---

Let $S = S[0 \ldots n-1]$ with $n \ge 1$, $S_i = S[i \ldots n-1]$, and $S_i^h$ the prefix of length $\min(h, n-i)$ of $S_i$; for $i \ge n$, $S_i^h$ is the empty string $\varepsilon$, which is smaller than each nonempty string. We use the split lemma proved on the [suffix array](/suffix-array/) page: $S_i^{2h} = S_i^h \cdot S_{i+h}^h$, and

$$S_i^{2h} < S_j^{2h} \iff S_i^h < S_j^h, \text{ or } S_i^h = S_j^h \text{ and } S_{i+h}^h < S_{j+h}^h. \qquad (1)$$

**Invariant (I$_h$).** $SA$ is a permutation of $\{0, \ldots, n-1\}$ with $S_{SA[0]}^h \le \cdots \le S_{SA[n-1]}^h$, and for each $i$, $B[i]$ is the least rank $r$ with $S_{SA[r]}^h = S_i^h$. So $B[i] = B[j]$ if and only if $S_i^h = S_j^h$, and $B[i] < B[j]$ if and only if $S_i^h < S_j^h$. Extend $B$ by $B[i] = -1$ for $i \ge n$; then the last two statements also hold for $i, j \ge n$, with $\varepsilon$.

**Initialization.** Line L1 sorts by the first symbol, so $SA$ is ordered by $S_i^1$. Line L2 gives each run of equal first symbols the rank of its first member. So (I$_1$) holds before the first test of line L4.

**Maintenance.** Assume (I$_h$) before a round. For each bucket $x$ (a value of $B$), let $P_x = \{\, i : B[i] = x \,\}$ and $c_x = |P_x|$. By (I$_h$) the bucket occupies the ranks $x, \ldots, x + c_x - 1$.

*Each position is placed exactly once, in its bucket.* Line L6 places the positions $i$ with $n - h \le i \le n-1$. Line L7 places $j = SA[r] - h$ for each $r$ with $SA[r] \ge h$, that is, each $j$ with $0 \le j \le n - 1 - h$, once, since $SA$ is a permutation. Together these are all positions, each once. A position $i$ goes to slot $next[B[i]]$, which starts at $B[i]$ and grows by one at each placement into that bucket. Since bucket $B[i]$ receives exactly $c_{B[i]}$ placements, the slots used are $B[i], \ldots, B[i] + c_{B[i]} - 1$, which are the ranks of the bucket. So line L8 makes $SA$ a permutation in which each bucket keeps its range of ranks, and the buckets stay in increasing order of $S_i^h$.

*Inside a bucket, the order is by the second half.* Take $i, j$ in the same bucket with $S_{i+h}^h < S_{j+h}^h$. We show that $i$ is placed before $j$. If $i + h \ge n$, then $i$ is placed in line L6, before all placements of line L7, and before $j$ unless $j$ is also placed in line L6. But two different positions $i, j \ge n - h$ in the same bucket would have $S_i^h = S_i$ and $S_j^h = S_j$ of different lengths (if both are at least $n - h$, their suffixes have length at most $h$), so they are not in the same bucket. If $i + h < n$, then $j + h < n$ too (since $S_{j+h}^h > S_{i+h}^h \ge \varepsilon$ is nonempty), both are placed in line L7, at the ranks $r_i$ and $r_j$ of $i + h$ and $j + h$ in the old $SA$. By (I$_h$), $S_{i+h}^h < S_{j+h}^h$ implies $r_i < r_j$. So $i$ is placed first, in a smaller slot.

*So the new $SA$ is ordered by $2h$-prefixes.* Take ranks $r < r'$ of the new $SA$ with $p = SA[r]$ and $q = SA[r']$. If $p$ and $q$ are in different buckets, the bucket of $p$ comes first, so $S_p^h < S_q^h$ and by (1) $S_p^{2h} < S_q^{2h}$. If they are in the same bucket, the previous paragraph shows that $S_{p+h}^h \le S_{q+h}^h$ (otherwise $q$ would have been placed first), and by (1) $S_p^{2h} \le S_q^{2h}$.

*Line L9 gives the new buckets.* By (I$_h$), $B[p] = B[q]$ and $B[p+h] = B[q+h]$ hold if and only if $S_p^h = S_q^h$ and $S_{p+h}^h = S_{q+h}^h$, that is, by the split, if and only if $S_p^{2h} = S_q^{2h}$. Since the new $SA$ is sorted by $2h$-prefixes, equal $2h$-prefixes are contiguous, and line L9 gives each run the rank of its first member. After line L10, (I$_{2h}$) holds with the new value of $h$.

**Termination.** Each round doubles $h$, so the test $h < n$ of line L4 fails after at most $\lceil \lg n \rceil$ rounds.

**Result.** The loop ends when $B$ has $n$ distinct values or when $h \ge n$. In the second case $S_i^h = S_i$ for all $i$, and different suffixes are different strings, so $B$ has $n$ distinct values in both cases. Then all $h$-prefixes are different, and by (I$_h$) $S_{SA[0]}^h < \cdots < S_{SA[n-1]}^h$. Two suffixes with different $h$-prefixes compare like these prefixes: they differ at a position less than $h$ inside both, or one prefix is shorter than $h$, so it is the whole suffix, and it is a proper prefix of the other suffix. Hence $S_{SA[0]} < \cdots < S_{SA[n-1]}$, and line L11 returns the suffix array. $\blacksquare$
