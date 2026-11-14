---
title: The per-point counts are inversion counts, the selection returns the repeated median slope, and the breakdown point is floor(n/2)/n
proves: [correctness]
status: full
---

**Setting.** The data are $(x_1, y_1), \ldots, (x_n, y_n)$. For $x_i \ne x_j$, $s_{ij} = s_{ji} = (y_j - y_i)/(x_j - x_i)$. Point $i$ has $d_i$ slopes, one for each $j$ with $x_j \ne x_i$. For $d_i > 0$, its median is $m_i$, the $k_i$-th smallest of its slopes with $k_i = \lfloor d_i/2 \rfloor + 1$ (the high median). Let $n'$ be the number of points with $d_i > 0$ and $K = \lceil n'/2 \rceil$. The repeated median slope $b$ is the $K$-th smallest of the $n'$ values $m_i$ (the low median). For a value $v$ and a point $j$, $\ell_j(v)$ and $e_j(v)$ are the numbers of slopes of $j$ that are $< v$ and $\le v$.

## Part 1. The per-point counts

The keys of the points at a slope $s$ are $y_i - s x_i$, with the limit orders $(x_i, y_i)$ at $-\infty$ and $(-x_i, y_i)$ at $+\infty$, as on the [Theil-Sen](/theil-sen-estimator/) page.

**Lemma 1.** For $lo < hi$, list the points by the key at $lo$, ties by the key at $hi$, and let $w$ be the keys at $hi$ in this order. The pair $\{i, j\}$ is an inversion of $w$ if and only if $x_i \ne x_j$ and $lo < s_{ij} < hi$.

*Proof.* For $x_i < x_j$, $(y_j - s x_j) - (y_i - s x_i) = (x_j - x_i)(s_{ij} - s)$. So the key of $j$ is above the key of $i$ at $lo$ exactly when $s_{ij} > lo$ (at $-\infty$, always), and below it at $hi$ exactly when $s_{ij} < hi$ (at $+\infty$, always). The opposite pattern would need $s_{ij} < lo < hi < s_{ij}$. Pairs with $x_i = x_j$ compare by $y$ at every $s$, so they keep their order. Pairs tied at $lo$ are listed in their order at $hi$. So the inversions are the pairs in opposite strict order at $lo$ and at $hi$, which are the pairs with $lo < s_{ij} < hi$. $\square$

**Lemma 2.** The merge sort in `per_point_between` adds to each point the number of inversions it belongs to.

*Proof.* Merge sort counts each inversion $(a, b)$, $a$ before $b$ and $w_a > w_b$, in exactly one merge: the one where $a$ is in the left half and $b$ in the right half. In that merge, when the right item $b$ is output, the left items not yet output are exactly the left items $> w_b$, and $b$ gets their number. When a left item $a$ is output, the right items already output are exactly the right items $< w_a$, and $a$ gets their number. So each inversion adds 1 to both its points. $\square$

So line L7 computes $\ell_j(v) = $ count$(-\infty, v)_j$ and $e_j(v) = d_j - $ count$(v, +\infty)_j$ for all $j$ in $O(n \log n)$ time, and line L1 computes $d_j = $ count$(-\infty, +\infty)_j$. Then
$$m_j < v \iff \ell_j(v) \ge k_j, \qquad m_j \le v \iff e_j(v) \ge k_j,$$
because the $k_j$-th smallest slope is below $v$ exactly when at least $k_j$ slopes are.

## Part 2. The selection

**Lemma 3.** A value $v$ is the $K$-th smallest of the $m_j$ if and only if $\#\{j : m_j < v\} < K \le \#\{j : m_j \le v\}$.

*Proof.* As for any multiset: the $K$-th smallest is $\le v$ exactly when at least $K$ values are $\le v$, and it is not $< v$ exactly when fewer than $K$ values are $< v$. $\square$

**Invariant.** At line L5, with $lo$ and $hi$ the last values set at line L10 (first $-\infty$ and $+\infty$), the set $A$ is $\{j : lo < m_j < hi\}$, and $\#\{j : m_j \le lo\} < K \le \#\{j : m_j < hi\}$. So $b = m_j$ for some $j \in A$.

*Proof.* At the start every $m_j$ is finite, so $A$ is all kept points, and $0 < K \le n'$. In a round, line L9 returns $v$ if Lemma 3 says it is $b$. Otherwise either $K \le cl = \#\{m_j < v\}$, and line L10 sets $hi \leftarrow v$, or $ce = \#\{m_j \le v\} < K$, and it sets $lo \leftarrow v$. In both cases the inequality holds for the new interval. Line L11 keeps the $j$ with $e_j(lo) < k_j$ ($m_j > lo$) and $\ell_j(hi) \ge k_j$ ($m_j < hi$), using the counts saved at the last change of each end. The values $m_j$ in $(lo, hi)$ number $\#\{m_j < hi\} - \#\{m_j \le lo\} \ge 1$, and $b$ is one of them. $\square$

**Termination.** The pivot $v = m_i$ comes from a point $i \in A$. If the round does not return, the new interval excludes $v$, so $i$ leaves $A$. So $|A|$ drops by at least one in every round, and the loop ends after at most $n'$ rounds with the answer, because $A$ is never empty. The value returned is $b$ by Lemma 3.

**Expected number of rounds.** The pivot is the median of a uniformly random point of $A$. This is randomized [quickselect](/quickselect/) over the multiset $\{m_j : j \in A\}$: with probability at least $1/2$ the pivot has rank between $|A|/4$ and $3|A|/4$ in it, and then at least a quarter of $A$ leaves. So the expected number of rounds is $O(\log n)$. Each round sorts the slopes of one point and runs three merge sorts, $O(n \log n)$ time. The expected total is $O(n \log^2 n)$, and the worst case is $O(n^2 \log n)$.

## Part 3. The breakdown point

Assume the clean data have distinct $x$, so $d_i = n - 1$ for all $i$. Replace $m$ points by arbitrary points.

**Lemma 4.** Among $D$ numbers, $F$ of them free and the rest fixed, the $k$-th smallest can be sent to $+\infty$ exactly when $F \ge D - k + 1$, to $-\infty$ exactly when $F \ge k$, and otherwise it lies between the smallest and the largest fixed number.

*Proof.* To send the $k$-th smallest up, at least $D - k + 1$ values must be large; the fixed ones are bounded. If $F \ge D - k + 1$, send all free values up. The other side is the same. If neither holds, at least one fixed value is $\le$ and one is $\ge$ the $k$-th smallest. $\square$

**Upper bound, $m = \lfloor n/2 \rfloor$ points suffice.** Put the $j$-th bad point at $x = \max_i x_i + j$ and $y = j^2 t$ with $t \to \infty$. All slopes that involve a bad point then tend to $+\infty$ together. A clean point has $D = n - 1$ slopes, $F = m$ of them free, and $k = \lfloor (n-1)/2 \rfloor + 1$, so $D - k + 1 = \lceil (n-1)/2 \rceil = \lfloor n/2 \rfloor = m$, and its median goes to $+\infty$. So do the medians of the bad points, whose slopes are all free. So all $n$ medians, and $b$, go to $+\infty$.

**Lower bound, $m \le \lfloor n/2 \rfloor - 1$ points do not suffice.** Let $[s_{\min}, s_{\max}]$ be the range of the slopes among the clean points; it does not depend on the bad points. Since $n - m \ge 2$ clean points have distinct $x$, every point has a slope, so $n' = n$.

Take a clean point, and let $c$ bad points share its $x$. It has $D = n - 1 - c$ slopes, $F = m - c$ of them free, and $k = \lfloor D/2 \rfloor + 1$, so $D - k + 1 = \lceil D/2 \rceil \le k$. Now $\lceil (n-1)/2 \rceil \le n/2$, so
$$\Big\lceil \frac D2 \Big\rceil \ge \frac{n - 1 - c}{2} \ge \Big\lceil \frac{n-1}2 \Big\rceil - \frac12 - \frac c2 > \Big\lceil \frac{n-1}2 \Big\rceil - 1 - c \ge m - c = F,$$
using $m \le \lfloor n/2 \rfloor - 1 = \lceil (n-1)/2 \rceil - 1$. By Lemma 4, the median of the clean point lies between two of its clean slopes, so in $[s_{\min}, s_{\max}]$.

So at least $n - m$ of the $n$ point medians are in $[s_{\min}, s_{\max}]$, and at most $m$ are free. The outer median has $K = \lceil n/2 \rceil$ and $n - K + 1 = \lfloor n/2 \rfloor + 1$, both larger than $m$. By Lemma 4 again, $b \in [s_{\min}, s_{\max}]$ whatever the bad points are.

So the breakdown point in the replacement sense is
$$\varepsilon^*_n = \frac{\lfloor n/2 \rfloor}{n} \longrightarrow \frac12. \qquad \square$$
