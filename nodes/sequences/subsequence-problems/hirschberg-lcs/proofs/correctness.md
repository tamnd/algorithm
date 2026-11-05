---
title: Hirschberg's algorithm returns a longest common subsequence
proves: [correctness]
status: full
---

We use the pseudocode of the page. Write $\mathrm{lcs}(U, V)$ for the length of a longest common subsequence of $U$ and $V$, $U^R$ for the reverse of $U$, $X[a \ldots b] = x_a \cdots x_b$ and $Y[a \ldots b] = y_a \cdots y_b$, both empty if $a > b$.

**Lemma 1 (LCS-ROW).** LCS-ROW$(X, Y)$ returns $R$ with $R[j] = \mathrm{lcs}(X, Y[1 \ldots j])$ for $0 \le j \le n$.

*Proof.* Let $L(i, j) = \mathrm{lcs}(X[1 \ldots i], Y[1 \ldots j])$. We show by induction on $i$ that after $i$ rounds of the loop of line L9, $R[j] = L(i, j)$ for all $j$. For $i = 0$, line L8 sets $R[j] = 0 = L(0, j)$.

Let $i \ge 1$ and assume $R[j] = L(i - 1, j)$ for all $j$ before round $i$. Inside the round we show by induction on $j$ that, before the iteration $j$ of line L11, $R[0 \ldots j - 1]$ holds $L(i, 0), \ldots, L(i, j - 1)$, $R[j \ldots n]$ holds $L(i - 1, j), \ldots, L(i - 1, n)$, and $\mathrm{diag} = L(i - 1, j - 1)$. Before $j = 1$ this holds: $R[0] = 0 = L(i, 0)$ is never written, the rest of $R$ is the old row, and line L10 sets $\mathrm{diag} = 0 = L(i - 1, 0)$. In iteration $j$, line L12 sets $\mathrm{up} = L(i - 1, j)$, and line L13 writes $L(i - 1, j - 1) + 1$ if $x_i = y_j$, and $\max(L(i - 1, j), L(i, j - 1))$ if not. By the LCS recurrence (the corollary of the [optimal substructure theorem](/lcs-optimal-substructure/)) this is $L(i, j)$. Line L14 sets $\mathrm{diag} = L(i - 1, j)$, which is the value needed for $j + 1$. After $j = n$ the whole row holds $L(i, \cdot)$. $\square$

**Lemma 2 (reversal).** $Z$ is a common subsequence of $U$ and $V$ if and only if $Z^R$ is a common subsequence of $U^R$ and $V^R$. So $\mathrm{lcs}(U, V) = \mathrm{lcs}(U^R, V^R)$.

*Proof.* If $Z = u_{i_1} \cdots u_{i_k}$ with $i_1 < \cdots < i_k$, then $Z^R$ is the subsequence of $U^R$ at the positions $|U| + 1 - i_k < \cdots < |U| + 1 - i_1$. The same holds for $V$, and the converse is the same statement applied to $Z^R$. $\square$

By Lemmas 1 and 2, after lines L4 and L5 of a call with $m \ge 2$,

$$F[j] = \mathrm{lcs}(X[1 \ldots h], Y[1 \ldots j]), \qquad B[n - j] = \mathrm{lcs}(X[h+1 \ldots m]^R, Y[j+1 \ldots n]^R) = \mathrm{lcs}(X[h+1 \ldots m], Y[j+1 \ldots n]),$$

since the first $n - j$ items of $Y^R$ are $Y[j+1 \ldots n]^R$.

**Lemma 3 (split).** For each $0 \le h \le m$,

$$\mathrm{lcs}(X, Y) = \max_{0 \le j \le n} \big( \mathrm{lcs}(X[1 \ldots h], Y[1 \ldots j]) + \mathrm{lcs}(X[h+1 \ldots m], Y[j+1 \ldots n]) \big).$$

*Proof.* ($\ge$) Fix $j$. Let $Z_1$ be an LCS of $X[1 \ldots h]$ and $Y[1 \ldots j]$ and $Z_2$ an LCS of $X[h+1 \ldots m]$ and $Y[j+1 \ldots n]$. The positions of $Z_1$ in $X$ are at most $h$ and those of $Z_2$ are above $h$, and the same holds in $Y$ with $j$. So $Z_1 Z_2$ is a common subsequence of $X$ and $Y$, of length $|Z_1| + |Z_2|$.

($\le$) Let $Z$ be an LCS of $X$ and $Y$, of length $\ell$, with positions $i_1 < \cdots < i_\ell$ in $X$ and $j_1 < \cdots < j_\ell$ in $Y$, where $x_{i_t} = y_{j_t} = z_t$. Let $s$ be the number of $t$ with $i_t \le h$, so $i_1, \ldots, i_s \le h < i_{s+1}, \ldots, i_\ell$. Let $j = j_s$ if $s \ge 1$ and $j = 0$ if $s = 0$. Then $z_1 \cdots z_s$ is a common subsequence of $X[1 \ldots h]$ and $Y[1 \ldots j]$, and $z_{s+1} \cdots z_\ell$ is a common subsequence of $X[h+1 \ldots m]$ and $Y[j+1 \ldots n]$, since $j_{s+1} > j_s = j$. So $\ell = s + (\ell - s)$ is at most the term of the maximum for this $j$. $\square$

**Theorem.** For all $X$ and $Y$, HIRSCHBERG$(X, Y)$ returns a common subsequence of $X$ and $Y$ of length $\mathrm{lcs}(X, Y)$.

*Proof.* Induction on $m$.

*Base.* If $m = 0$ or $n = 0$, the only common subsequence is empty, and line L1 returns it. If $m = 1$ and $n \ge 1$, $\mathrm{lcs}(X, Y)$ is 1 if $x_1$ occurs in $Y$ and 0 otherwise, and line L2 returns $\langle x_1 \rangle$ or the empty sequence, which are common subsequences of these lengths.

*Step.* Let $m \ge 2$, so $1 \le h = \lfloor m/2 \rfloor < m$ and both halves of $X$ are shorter than $X$. By Lemmas 1 to 3, line L6 picks $k$ with

$$F[k] + B[n - k] = \max_j \big( F[j] + B[n - j] \big) = \mathrm{lcs}(X, Y).$$

By the induction hypothesis, the first call of line L7 returns a common subsequence $Z_1$ of $X[1 \ldots h]$ and $Y[1 \ldots k]$ of length $F[k]$, and the second returns a common subsequence $Z_2$ of $X[h+1 \ldots m]$ and $Y[k+1 \ldots n]$ of length $B[n - k]$. As in the ($\ge$) part of Lemma 3, $Z_1 Z_2$ is a common subsequence of $X$ and $Y$. Its length is $F[k] + B[n - k] = \mathrm{lcs}(X, Y)$. $\square$

**Termination.** Each recursive call has a shorter first sequence ($h < m$ and $m - h < m$ for $m \ge 2$), so the recursion ends.

**Cost.** Let $C(m, n)$ be the number of cells that LCS-ROW fills in a call on lengths $m$ and $n$, and let $c(1) = 0$ and $c(m) = m + c(\lceil m/2 \rceil)$ for $m \ge 2$. Then $c$ is non-decreasing and $C(m, n) \le c(m) \, n$. For $m \le 1$, $C = 0$. For $m \ge 2$, the call fills $hn + (m - h)n = mn$ cells and

$$C(m, n) \le mn + c(h) k + c(m - h)(n - k) \le mn + c(\lceil m/2 \rceil) n = c(m) n,$$

because $h, m - h \le \lceil m/2 \rceil$. Unrolling, $c(m) \le m + \lceil m/2 \rceil + \lceil m/4 \rceil + \cdots$, and since $\lceil m/2^t \rceil < m/2^t + 1$ and the sum has at most $\lceil \log_2 m \rceil$ terms, $c(m) < 2m + \lceil \log_2 m \rceil$. So the algorithm fills fewer than $(2m + \lceil \log_2 m \rceil) n$ cells, and at least the $mn$ cells of the top call. $\blacksquare$
