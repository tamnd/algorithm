---
title: The suffix array gives the last column of the sorted rotations, and the columns group symbols by context
proves: [correctness]
status: full
---

We use the notation of the page. $T = T[0 \ldots n-1]$ is over $\Sigma$, $T' = T\$$ has length $N = n + 1$, the sentinel $\$$ is not in $\Sigma$ and is smaller than each symbol of $\Sigma$. For $0 \le i < N$, the suffix $S_i = T'[i \ldots N-1]$ and the rotation $R_i = T'[i \ldots N-1]\,T'[0 \ldots i-1]$. Strings are compared in lexicographic order.

**Lemma 1 (no suffix is a prefix of another).** For $i \ne j$, neither of $S_i$ and $S_j$ is a prefix of the other.

*Proof.* Take $i > j$, so $|S_i| < |S_j|$. If $S_i$ were a prefix of $S_j$, then the last symbol of $S_i$, which is $\$$, would equal the symbol of $S_j$ at index $|S_i| - 1 < |S_j| - 1$. That symbol is $T'[j + |S_i| - 1]$ with $j + |S_i| - 1 < N - 1$, so it is a symbol of $T$, not $\$$. This is a contradiction, because $\$$ occurs only at index $N - 1$ of $T'$. A longer string is never a prefix of a shorter one. $\square$

**Lemma 2 (rotations compare like suffixes).** For $i \ne j$: $R_i < R_j$ if and only if $S_i < S_j$. In particular the $N$ rotations are pairwise distinct.

*Proof.* By Lemma 1, $S_i$ and $S_j$ differ at some index $p < \min(|S_i|, |S_j|)$; let $p$ be the first such index. $S_i$ is a prefix of $R_i$ and $S_j$ is a prefix of $R_j$, so $R_i$ and $R_j$ agree on indices $0$ to $p - 1$ and differ at index $p$, with the same two symbols as $S_i$ and $S_j$. So $R_i$ and $R_j$ are different, and they compare in the same way as $S_i$ and $S_j$. $\square$

**Theorem 1 (the algorithm computes the BWT).** Let $SA$ be the suffix array of $T'$. For each row $r$, the $r$-th smallest rotation is $R_{SA[r]}$, and the value that lines L4 and L5 write to $L[r]$ is its last symbol. So $L$ is the last column of the matrix of sorted rotations.

*Proof.* $SA$ lists $0, \ldots, N-1$ so that $S_{SA[0]} < S_{SA[1]} < \cdots$. By Lemma 2, also $R_{SA[0]} < R_{SA[1]} < \cdots$, so row $r$ is $R_{SA[r]}$. The last symbol of $R_i$ is $T'[i - 1]$ when $i \ge 1$, and $T'[N-1] = \$$ when $i = 0$. Line L4 handles $SA[r] = 0$ and line L5 handles $SA[r] \ge 1$, so $L[r]$ is the last symbol of row $r$. The loop of line L3 runs over each $r$ from $0$ to $n = N - 1$ once and ends. $\blacksquare$

**Corollary (a permutation).** The map $r \mapsto (SA[r] - 1) \bmod N$ is a bijection of $\{0, \ldots, N-1\}$, as the composition of the permutation $SA$ and a cyclic shift. So $L$ holds each symbol of $T'$ exactly once, and $\$$ exactly once.

**Lemma 3 (blocks of a common prefix).** Let $X_0 \le X_1 \le \cdots \le X_{m-1}$ be strings of length at least $k$ in sorted order, and let $w$ have length $k$. Then the indices $r$ with $w$ a prefix of $X_r$ form an interval of consecutive integers.

*Proof.* Take $a < b < c$ with $w$ a prefix of $X_a$ and of $X_c$. Suppose $w$ is not a prefix of $X_b$. Since $|X_b| \ge k$, there is a first index $p < k$ with $X_b[p] \ne w[p]$. If $X_b[p] < w[p]$, then $X_b < X_a$, because the two agree before $p$ and $X_a[p] = w[p]$; this contradicts $X_a \le X_b$. If $X_b[p] > w[p]$, then $X_b > X_c$ in the same way, which contradicts $X_b \le X_c$. So $w$ is a prefix of $X_b$. $\square$

**Theorem 2 (context grouping).** Let $w \in \Sigma^k$ with $1 \le k \le n$. The rows whose rotation starts with $w$ form an interval $[b, e)$ of rows, and the multiset $\{L[r] : b \le r < e\}$ equals the multiset $\{T'[(j - 1) \bmod N] : 0 \le j \le n - k,\ T[j \ldots j+k-1] = w\}$, that is, the symbols just before the occurrences of $w$ in $T$, where the symbol before position $0$ is $\$$.

*Proof.* All rotations have length $N > k$, so Lemma 3 applies to the sorted rotations and the rows with prefix $w$ form an interval. Row $r$ is $R_i$ with $i = SA[r]$ (Theorem 1). $R_i$ starts with $w$ if and only if $T'[i \ldots i+k-1] = w$ read around the circle. Since $w$ has no $\$$ and $\$$ is at index $N - 1$, the $k$ symbols from $i$ do not reach index $N-1$, so $i + k - 1 \le N - 2 = n - 1$, and $R_i$ starts with $w$ if and only if $w$ occurs in $T$ at position $i$. The map $r \mapsto SA[r]$ is a bijection, so the rows of the interval correspond one to one to the occurrences $j$ of $w$ in $T$, and the last symbol of the row of $j$ is $T'[(j - 1) \bmod N]$ by Theorem 1. $\blacksquare$

**Consequence for the entropy.** Let $T_w$ be the string of the symbols just before the occurrences of $w$ at positions $j \ge 1$ of $T$. By Theorem 2, the block of $w$ in $L$ is a permutation of $T_w$ with one extra $\$$ exactly when $T$ starts with $w$. The rows that are in no block are the rows $R_i$ whose first $k$ symbols hold $\$$, that is $i \ge N - k$: there are $k$ of them. Since $H_0$ of a string depends only on the multiset of its symbols, $\sum_{w} |T_w|\, H_0(T_w) = n H_k(T)$ is, up to these $k + 1$ symbols, the cost of coding each block of $L$ with its own zero-order model.
