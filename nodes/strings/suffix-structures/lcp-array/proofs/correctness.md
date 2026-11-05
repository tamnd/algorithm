---
title: LCP-BUILD computes the LCP array, and the queries return the LCP of two suffixes
proves: [correctness, termination, time.worst]
status: full
---

**Notation.** $T = T[0 \ldots n-1]$, $n \ge 1$, and $T_p = T[p \ldots n-1]$ for $0 \le p \le n$, so $T_n$ is the empty string. The order $<$ on strings is the lexicographic order in which a proper prefix is smaller. $SA$ lists $T_0, \ldots, T_{n-1}$ in increasing order, and $RANK$ is its inverse. For $RANK[p] > 0$ let $\mathrm{pred}(p) = SA[RANK[p] - 1]$ and $\ell(p) = \mathrm{lcp}(T_{\mathrm{pred}(p)}, T_p)$. The claim is that after LCP-BUILD, $LCP[0] = 0$ and $LCP[RANK[p]] = \ell(p)$ for each $p$ with $RANK[p] > 0$.

**Lemma 1 (sandwich).** If $x \le y \le z$, then $\mathrm{lcp}(x, z) \le \mathrm{lcp}(x, y)$ and $\mathrm{lcp}(x, z) \le \mathrm{lcp}(y, z)$.

*Proof.* Let $k = \mathrm{lcp}(x, z)$ and $c = x[0 \ldots k-1] = z[0 \ldots k-1]$. Suppose that $y$ does not start with $c$, and let $j < k$ be the first index where $y$ and $c$ differ: either $|y| = j$, or $y[j] \ne c[j]$. If $|y| = j$ or $y[j] < c[j]$, then $y < x$, because $x$ starts with $c$ and so $x$ is longer than $j$ and agrees with $y$ before $j$. If $y[j] > c[j]$, then $y > z$ for the same reason. Both contradict $x \le y \le z$. So $y$ starts with $c$, and both inequalities follow. $\square$

**Lemma 2 (drop one symbol).** Let $RANK[p] > 0$ and $\ell(p) = h \ge 2$. Then $p + 1 < n$, $RANK[p+1] > 0$ and $\ell(p+1) \ge h - 1$.

*Proof.* Let $q = \mathrm{pred}(p)$. Both $T_q$ and $T_p$ have length at least $h \ge 2$ and $T[q] = T[p]$. Then $T_{q+1}$ and $T_{p+1}$ are $T_q$ and $T_p$ without their equal first symbol. They are nonempty, they share a prefix of length $h - 1$, and $T_{q+1} < T_{p+1}$, because removing an equal first symbol keeps the order. So $T_{p+1}$ is not the smallest suffix, which gives $RANK[p+1] > 0$. The suffix $T_{\mathrm{pred}(p+1)}$ is the largest suffix below $T_{p+1}$, so $T_{q+1} \le T_{\mathrm{pred}(p+1)} < T_{p+1}$. By Lemma 1, $\ell(p+1) = \mathrm{lcp}(T_{\mathrm{pred}(p+1)}, T_{p+1}) \ge \mathrm{lcp}(T_{q+1}, T_{p+1}) \ge h - 1$. $\square$

**Theorem 1 (LCP-BUILD).** Line L1 makes $RANK$ the inverse of $SA$. Then the loop of line L3 keeps this invariant at the start of round $p$:

> **(K)** For each $p' < p$, the entry $LCP[RANK[p']]$ holds $0$ if $RANK[p'] = 0$ and $\ell(p')$ otherwise. Also $0 \le h$, and if $RANK[p] > 0$ then $h \le \ell(p)$. If $h \ge 1$, then $RANK[p] > 0$.

*Initialization.* At $p = 0$ no entry is claimed, and $h = 0$ by line L2.

*Maintenance.* If $RANK[p] = 0$, then by (K) $h = 0$, line L4 writes $LCP[0] = 0$ and keeps $h = 0$, and $h = 0$ satisfies (K) for $p + 1$. Otherwise line L5 sets $q = \mathrm{pred}(p)$. Since $h \le \ell(p)$, the first $h$ symbols of $T_p$ and $T_q$ are equal. Line L6 increases $h$ while the next symbols exist and are equal, so it stops exactly at $h = \ell(p)$. Line L7 writes the right value. Line L8 sets $h = \max(\ell(p) - 1, 0)$. If $\ell(p) \ge 2$, Lemma 2 gives $RANK[p+1] > 0$ and $h = \ell(p) - 1 \le \ell(p+1)$. If $\ell(p) \le 1$, then $h = 0$. In both cases (K) holds at the start of round $p + 1$.

*Termination.* The loop runs for $p = 0, \ldots, n-1$ and stops. Each inner loop stops, because $h$ grows by 1 in each step and is bounded by $n - p$. At the end, (K) with $p = n$ covers every position, and $RANK$ is a bijection onto the indices $0, \ldots, n-1$, so every entry of $LCP$ is right. $\square$

**Theorem 2 (time).** Line L6 increases $h$ at most $2n$ times in total, so LCP-BUILD takes $\Theta(n)$ time.

*Proof.* The value $h$ is at most $n$ at all times. It decreases only at line L8, by 1, at most once in each of the $n$ rounds. Line L4 does not change it, because $h = 0$ there by (K). So the number of increases is at most the final value plus the number of decreases, which is at most $n + n$. Each round does $O(1)$ other work, and the failed test that ends line L6 costs $O(1)$ for each round. $\square$

**Lemma 3 (LCP of two ranks).** For $0 \le i < j < n$, $\mathrm{lcp}(T_{SA[i]}, T_{SA[j]}) = \min LCP[i+1 \ldots j]$.

*Proof.* Write $S_k = T_{SA[k]}$ and $m = \min LCP[i+1 \ldots j]$. For any strings, $\mathrm{lcp}(x, z) \ge \min(\mathrm{lcp}(x, y), \mathrm{lcp}(y, z))$, because $x$ and $y$ agree on the first $\mathrm{lcp}(x, y)$ symbols, and $y$ and $z$ on the first $\mathrm{lcp}(y, z)$. Applying this along $S_i, S_{i+1}, \ldots, S_j$ gives $\mathrm{lcp}(S_i, S_j) \ge m$. For the other direction, pick $k$ with $i < k \le j$ and $LCP[k] = m$. Since $S_i \le S_{k-1} < S_k \le S_j$, Lemma 1 applied twice gives $\mathrm{lcp}(S_i, S_j) \le \mathrm{lcp}(S_{k-1}, S_j) \le \mathrm{lcp}(S_{k-1}, S_k) = m$. $\square$

**Theorem 3 (queries).** LCP-RANKS$(i, j)$ returns $\mathrm{lcp}(T_{SA[i]}, T_{SA[j]})$ for $0 \le i < j < n$, and LCE$(p, q)$ returns $\mathrm{lcp}(T_p, T_q)$ for $0 \le p, q < n$.

*Proof.* By induction on $k$, $M[k][i] = \min LCP[i \ldots i + 2^k - 1]$: for $k = 0$ it is $LCP[i]$, and the range of length $2^k$ is the union of the two ranges of length $2^{k-1}$ that start at $i$ and at $i + 2^{k-1}$. In line L9, $L = j - i \ge 1$ and $2^k \le L < 2^{k+1}$. The ranges $[i+1, i+2^k]$ and $[j - 2^k + 1, j]$ lie inside $[i+1, j]$, and since $2^{k+1} \ge L + 1$ the second starts no later than one place after the end of the first, so together they cover $[i+1, j]$. The minimum over a union is the minimum of the two minima, so line L10 returns $\min LCP[i+1 \ldots j]$, which is the claim by Lemma 3. For LCE, if $p = q$ the answer is $|T_p| = n - p$ (line L11). Otherwise lines L12 and L13 call LCP-RANKS with the two ranks in increasing order, and $T_{SA[RANK[p]]} = T_p$. $\blacksquare$
