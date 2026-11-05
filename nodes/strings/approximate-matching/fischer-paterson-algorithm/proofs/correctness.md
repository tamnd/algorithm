---
title: The Fischer-Paterson method computes all Hamming distances
proves: [correctness]
status: full
---

Indices are 0-based, $1 \le m \le n$, and $h[i] = |\{ r \in \{0, \ldots, m-1\} : P[r] \ne T[i + r] \}|$ for $0 \le i \le n - m$. Let $S$ be the set of distinct symbols of $P$. For $c \in S$, $x_c[q] = [P[m-1-q] = c]$ for $0 \le q < m$, and for a block start $b$, $y_{c,b}[j] = [T[b + j] = c]$ for $0 \le j < \ell_b$, where $\ell_b = \min(2m - 1, n - b)$. All other entries of the vectors of length $N$ are 0, and $N \ge 3m - 2$.

**Lemma 1 (one block, one symbol).** Let $z = x_c * y_{c,b}$ be the linear convolution, $z[s] = \sum_{q + j = s} x_c[q]\, y_{c,b}[j]$. For each $t$ with $0 \le t \le m - 1$ and $b + t \le n - m$,

$$z[t + m - 1] = |\{ r \in \{0, \ldots, m-1\} : P[r] = c \text{ and } T[b + t + r] = c \}|.$$

*Proof.* $z[t + m - 1] = \sum_{q=0}^{m-1} x_c[q]\, y_{c,b}[t + m - 1 - q]$, since $x_c[q] = 0$ for $q \ge m$ and the index $j = t + m - 1 - q$ is at least $t \ge 0$. Substitute $r = m - 1 - q$, which runs over $0, \ldots, m - 1$: the term is $[P[r] = c] \cdot y_{c,b}[t + r]$. Here $t + r \le 2m - 2 < 2m - 1$ and $b + t + r \le (n - m) + (m - 1) = n - 1$, so $t + r < \ell_b$ and $y_{c,b}[t + r] = [T[b + t + r] = c]$. The sum of the products of the two indicators counts the stated set. $\square$

**Lemma 2 (the transform is exact).** Line L6 returns $z$ exactly.

*Proof.* $x_c$ has nonzero entries only below $m$ and $y_{c,b}$ only below $2m - 1$, so $z[s] = 0$ for $s > 3m - 3$, and the linear convolution has length at most $3m - 2 \le N$. The pointwise product of the transforms of length $N$ gives the cyclic convolution $\tilde z[s] = \sum_{q + j \equiv s \pmod N} x_c[q]\, y_{c,b}[j]$. A pair with $q + j \ge N$ would need $q + j \ge 3m - 2$, but $q + j \le (m - 1) + (2m - 2) = 3m - 3$. So $\tilde z = z$. Over the integers modulo the prime $p = 998244353$, the number-theoretic transform satisfies the same convolution theorem, because $N$ is a power of two that divides $p - 1$, so a primitive $N$-th root of unity exists. So the result is $z[s] \bmod p$. Each $z[s]$ is a count of at most $m$ pairs, and $0 \le z[s] \le m < p$, so $z[s] \bmod p = z[s]$. $\square$

**Lemma 3 (the blocks).** Each $i \in \{0, \ldots, n - m\}$ receives a contribution in line L7 from exactly one block per symbol, the one with $b = m \lfloor i / m \rfloor$, at $t = i - b$.

*Proof.* The blocks have $b = 0, m, 2m, \ldots$ with $b \le n - m$. Line L7 of block $b$ adds to $A[b + t]$ for $0 \le t \le \min(m, n - m + 1 - b) - 1$, that is, for the starts $b, \ldots, \min(b + m - 1, n - m)$. These ranges are disjoint for different $b$, since each has length at most $m$ and they start $m$ apart, and their union is $\{0, \ldots, n - m\}$, since the last block has $b > n - 2m$ and its range ends at $n - m$. The block that contains $i$ is the one with $b \le i < b + m$, that is, $b = m \lfloor i/m \rfloor$, and this $b \le i \le n - m$ is one of the blocks of line L4. $\square$

**Theorem.** FP-HAMMING returns $h$.

*Proof.* By Lemmas 1 to 3, after the loops,

$$A[i] = \sum_{c \in S} |\{ r : P[r] = c \text{ and } T[i + r] = c \}|.$$

For each $r$, the condition $P[r] = c = T[i + r]$ holds for at most one $c$, namely $c = P[r] \in S$, and it holds for that $c$ exactly when $P[r] = T[i + r]$. So the sets in the sum are disjoint, and their union is $\{ r : P[r] = T[i + r] \}$. So $A[i] = m - h[i]$, and line L8 returns $h[i] = m - A[i]$. $\blacksquare$
