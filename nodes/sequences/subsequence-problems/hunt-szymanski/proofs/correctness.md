---
title: The Hunt-Szymanski thresholds give the LCS length and the links give an LCS
proves: [correctness]
status: full
---

We use the pseudocode of the page. A *match* is a pair $(i, j)$ with $x_i = y_j$. A *chain* of length $k$ is a list of matches $(i_1, j_1), \ldots, (i_k, j_k)$ with $i_1 < \cdots < i_k$ and $j_1 < \cdots < j_k$. The common subsequences of $X$ and $Y$ with a fixed embedding are exactly the chains: the chain spells $x_{i_1} \cdots x_{i_k}$. For $0 \le i \le m$ define

$$T_i[k] = \min\{ j_k : (i_1, j_1), \ldots, (i_k, j_k) \text{ is a chain with } i_k \le i \},$$

with $T_i[0] = 0$ (the empty chain) and $T_i[k] = \infty$ if no chain of length $k$ has all rows at most $i$. So $T_i[k]$ is the smallest $j$ such that $X[1 \ldots i]$ and $Y[1 \ldots j]$ have a common subsequence of length $k$.

**Lemma 1 (monotone).** If $T_i[k] < \infty$ for some $k \ge 1$, then $T_i[k - 1] < T_i[k]$.

*Proof.* Drop the last match of a chain of length $k$ that ends in column $T_i[k]$. This gives a chain of length $k - 1$ with all rows at most $i$ that ends in a column below $T_i[k]$ (or the empty chain, with end 0). $\square$

**Lemma 2 (row update).** For $i \ge 1$ and $k \ge 1$,

$$T_i[k] = \min\big( T_{i-1}[k],\ \min\{ j : (i, j) \text{ is a match and } T_{i-1}[k - 1] < j \} \big).$$

*Proof.* A chain with rows at most $i$ either has all rows at most $i - 1$, or its last match is in row $i$; then it has only one match in row $i$, since rows strictly increase, and the rest is a chain of length $k - 1$ with rows at most $i - 1$ that ends in a column below $j$. Such a rest exists if and only if $T_{i-1}[k - 1] < j$. Conversely, each such rest followed by $(i, j)$ is a chain. Taking the smallest last column over both kinds gives the formula. $\square$

**Lemma 3 (one row of the loop).** Suppose that before row $i$, $T[k] = T_{i-1}[k]$ for all $k$. Then after the loop of line L4 for row $i$, $T[k] = T_i[k]$ for all $k$.

*Proof.* Let the matches of row $i$ be $(i, j_1), \ldots, (i, j_s)$ with $j_1 > \cdots > j_s$, the order of line L4, and let $k_t$ be the index that line L5 returns for $j_t$. Writes of line L7 only lower an entry, and each value written in this row is some $j_{t'}$.

*Claim.* When $(i, j_t)$ is handled, each entry changed earlier in this row holds a value greater than $j_t$, and each other entry $k$ holds $T_{i-1}[k]$. This holds because the values written before are $j_1, \ldots, j_{t-1}$, all greater than $j_t$.

*The index $k_t$.* For $k < k_t$, $T[k] < j_t$, so by the claim $T[k]$ is unchanged and $T_{i-1}[k] = T[k] < j_t$. At $k_t$, $T_{i-1}[k_t] \ge j_t$: if $T[k_t]$ is unchanged, $T_{i-1}[k_t] = T[k_t] \ge j_t$; if it was changed, then $T_{i-1}[k_t]$ is larger than each value written at $k_t$, and these are larger than $j_t$. With Lemma 1, $k_t$ is the smallest $k$ with $T_{i-1}[k] \ge j_t$.

*The update.* By Lemma 2, $j_t$ is a candidate for $T_i[k]$ exactly when $T_{i-1}[k - 1] < j_t$, that is, when $k \le k_t$. For $k < k_t$ the candidate does not matter, because $T_{i-1}[k] < j_t$. So $T_i[k] = \min(T_{i-1}[k], \min\{ j_t : k_t = k \})$. Lines L6 and L7 lower $T[k_t]$ to $j_t$ if $j_t$ is smaller, so after the row each $T[k]$ is this minimum, which is $T_i[k]$. $\square$

**Lemma 4 (links).** Whenever line L7 sets $T[k] = j$ in row $i$, $\mathrm{link}[k]$ is a chain of length $k$ whose last match is $(i, j)$.

*Proof.* By induction over the writes. $\mathrm{link}[0] = \mathrm{nil}$ is the empty chain, which ends in column $T[0] = 0$. At a write of line L7 in row $i$, the entry $k - 1$ has not been changed in row $i$ (by the claim in the proof of Lemma 3, since $T[k - 1] < j$), so $\mathrm{link}[k - 1]$ was set in an earlier row, or is the empty chain, and by induction it is a chain whose last match has row below $i$ and column $T[k - 1] < j$. Appending $(i, j)$ gives a chain of length $k$. $\square$

**Theorem.** HUNT-SZYMANSKI returns a longest common subsequence of $X$ and $Y$.

*Proof.* Before row 1, $T = T_0$: $T_0[0] = 0$ and $T_0[k] = \infty$ for $k \ge 1$, which is line L2. By Lemma 3 and induction on $i$, after the loop $T = T_m$. A common subsequence of length $k$ exists if and only if $T_m[k] < \infty$, and no chain is longer than $\min(m, n)$, so $\ell$ of line L8 is $\mathrm{lcs}(X, Y)$. By Lemma 4, $\mathrm{link}[\ell]$ is a chain of length $\ell$, and lines L9 and L10 output its items in the order of the chain, which is a common subsequence of length $\mathrm{lcs}(X, Y)$. $\blacksquare$

**Cost.** Each match is handled once in line L4, with one binary search over at most $\min(m, n) + 1$ entries in line L5 and $O(1)$ other work, so the loop takes $O(r \log n + m)$ time, and at most $r$ link nodes are made.
