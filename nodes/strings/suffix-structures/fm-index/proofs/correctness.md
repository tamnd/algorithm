---
title: Backward search and LF walks on the FM-index are correct
proves: [correctness, termination, time.worst]
status: full
---

**Notation.** $T = T[0 \ldots n-1]$ has symbols coded $1, \ldots, \sigma$, and $T' = T\$$ with $\$ = 0$, unique and smallest. Positions and rows are 0-based, $T'_p = T'[p \ldots n]$, and $SA$ is the suffix array of $T'$, so the suffixes $T'_{SA[0]} < \cdots < T'_{SA[n]}$. $L[i] = T'[SA[i] - 1]$ when $SA[i] > 0$ and $L[i] = \$$ otherwise. $C[c]$ is the number of symbols of $T'$ smaller than $c$, and $\mathrm{rank}_c(L, i) = |\{ r < i : L[r] = c \}|$. Since $\$$ is unique and smallest, no suffix of $T'$ is a prefix of another, and suffixes compare at the first position where they differ.

**Lemma 1 (block of a symbol).** The rows whose suffixes start with $c$ are exactly $C[c], \ldots, C[c] + n_c - 1$, where $n_c$ is the number of $c$ in $T'$.

*Proof.* The suffixes are sorted, so those that start with smaller symbols come first, and there are $C[c]$ of them, one for each position that holds a smaller symbol. $\square$

**Lemma 2 (LF).** Let $L[i] = c$ with $SA[i] = p > 0$. Then $SA[C[c] + \mathrm{rank}_c(L, i)] = p - 1$.

*Proof.* Let $i_0 < i_1 < \cdots$ be the rows with $L[r] = c$, and $p_j = SA[i_j]$, so $T'_{p_j - 1} = c\,T'_{p_j}$. Since $T'_{p_0} < T'_{p_1} < \cdots$, the suffixes $c\,T'_{p_0} < c\,T'_{p_1} < \cdots$ are in the same order. These are all the suffixes that start with $c$: a suffix $T'_q$ with $T'[q] = c$ has $q < n$, since $c \ne \$$, so $T'_{q+1}$ exists, and $L$ at its row is $c$. By Lemma 1 they fill the rows $C[c]$ onward in this order. Row $i = i_j$ has $\mathrm{rank}_c(L, i) = j$, so the suffix $T'_{p - 1}$ is at row $C[c] + j$. $\square$

**Lemma 3 (backward step).** Let $Q$ be a string and $[sp, ep)$ the rows whose suffixes start with $Q$. For a symbol $c$ of $T$, the rows whose suffixes start with $cQ$ are $[C[c] + \mathrm{rank}_c(L, sp), C[c] + \mathrm{rank}_c(L, ep))$.

*Proof.* A suffix $T'_q$ starts with $cQ$ if and only if $T'[q] = c$ and $T'_{q+1}$ starts with $Q$, that is, the row $i$ of $T'_{q+1}$ is in $[sp, ep)$ and $L[i] = c$. By Lemma 2, the row of $T'_q$ is $C[c] + \mathrm{rank}_c(L, i)$. As $i$ runs over the rows in $[sp, ep)$ with $L[i] = c$, $\mathrm{rank}_c(L, i)$ takes the consecutive values $\mathrm{rank}_c(L, sp), \ldots, \mathrm{rank}_c(L, ep) - 1$. $\square$

**Theorem 1 (count).** Lines L1 to L5 return the range of rows whose suffixes start with $P$, or the empty range if $P$ does not occur; $ep - sp$ is the number of occurrences.

*Proof.* Before the loop, the range $[0, n + 1)$ is all rows, which start with the empty string. Each round applies Lemma 3 with $c = P[j]$ and $Q = P[j+1 \ldots m-1]$. If $c$ is not in $T$, no suffix starts with $cQ$. Once a range is empty, all later ranges are empty, so stopping early is correct. After the loop the range is that of $P$. The occurrences of a nonempty $P$ in $T$ are the suffixes of $T'$ that start with $P$, one row each, since $P$ does not contain $\$$. $\square$

**Theorem 2 (locate).** For each row $i$ of the range, lines L7 to L9 report $SA[i]$, after at most $s - 1$ LF steps.

*Proof.* Invariant: $SA[i_{\text{start}}] = SA[i] + t$. It holds with $t = 0$. If $SA[i]$ is not sampled, then $SA[i] \bmod s \ne 0$, so $SA[i] > 0$ and Lemma 2 gives $SA[\mathrm{LF}(i)] = SA[i] - 1$, and $t$ grows by 1. The position drops by one per step and every multiple of $s$, including 0, is sampled, so the loop stops after at most $s - 1$ steps and reports $SA[i] + t = SA[i_{\text{start}}]$. $\square$

**Theorem 3 (extract).** The extraction returns $T[l \ldots r-1]$.

*Proof.* It starts at the row $i$ of a sampled position $p \ge r$, with $p \le n$. While $p > l$, $SA[i] = p > 0$, so $L[i] = T'[p - 1]$, and Lemma 2 moves to the row of $p - 1$. So it reads $T[p-1], T[p-2], \ldots, T[l]$, and keeps those at positions below $r$. $\square$

**Time.** The loop of L2 runs $m$ times with two rank queries each. Each reported occurrence takes at most $s - 1$ LF steps, each one rank query. With checkpoints every $b$ rows, a rank query scans fewer than $b$ symbols; with a wavelet tree it takes $O(\log \sigma)$ time. So `count` is $O(m b)$ or $O(m \log \sigma)$, `locate` adds $O(k s b)$ or $O(k s \log \sigma)$, and extract takes $p - l < r - l + s$ steps. All loops are bounded, so the operations terminate. $\blacksquare$
