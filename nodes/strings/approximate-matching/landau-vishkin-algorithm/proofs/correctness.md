---
title: The Landau-Vishkin algorithm computes the furthest rows of the diagonals
proves: [correctness]
status: full
---

Indices are 0-based, $|P| = m$, $|T| = n$, $k \ge 0$, and $d$ is the Levenshtein distance. Let $C[i][j]$, for $0 \le i \le m$ and $0 \le j \le n$, be the Sellers table. By the correctness proof of [Sellers' algorithm](/sellers-algorithm/), $C[0][j] = 0$, $C[i][0] = i$, and for $i, j \ge 1$

$$C[i][j] = \min\bigl(C[i][j-1] + 1,\; C[i-1][j] + 1,\; C[i-1][j-1] + [P[i-1] \ne T[j-1]]\bigr). \tag{R}$$

Diagonal $d$, for $-m \le d \le n$, is the set of cells $(i, i + d)$ with $s_d \le i \le t_d$, where $s_d = \max(0, -d)$ and $t_d = \min(m, n - d)$. Its first cell has the value $C[s_d][s_d + d] = s_d$ by the boundary values.

**Lemma 1 (columns).** For $1 \le i \le m$ and $0 \le j \le n$: $C[i-1][j] - 1 \le C[i][j] \le C[i-1][j] + 1$.

*Proof.* For $j = 0$ the values are $i - 1$ and $i$. Let $j \ge 1$. The right inequality is a term of (R). For the left one, induct on $j$. By (R), $C[i][j]$ is one of three terms, and we show each term is at least $C[i-1][j] - 1$. The term $C[i-1][j] + 1$ is. The term $C[i-1][j-1] + c$, with $c \in \{0, 1\}$, is at least $C[i-1][j] - 1$, because (R) for row $i - 1$ gives $C[i-1][j] \le C[i-1][j-1] + 1$ when $i \ge 2$, and $C[0][j] = 0 \le C[0][j-1] + 1$ when $i = 1$. The term $C[i][j-1] + 1$ is at least $C[i-1][j-1] - 1 + 1 = C[i-1][j-1]$ by the induction hypothesis for column $j - 1$, and $C[i-1][j-1] \ge C[i-1][j] - 1$ as just shown. $\square$

**Lemma 2 (rows).** For $0 \le i \le m$ and $1 \le j \le n$: $C[i][j-1] - 1 \le C[i][j] \le C[i][j-1] + 1$.

*Proof.* For $i = 0$ both values are 0. Let $i \ge 1$. The right inequality is a term of (R). For the left one, induct on $i$, with the claim for row $i - 1$ known. The term $C[i][j-1] + 1$ is at least $C[i][j-1] - 1$. The term $C[i-1][j] + 1$ is at least $C[i-1][j-1] - 1 + 1 = C[i-1][j-1]$ by the hypothesis for row $i - 1$, and $C[i-1][j-1] \ge C[i][j-1] - 1$ by Lemma 1. The term $C[i-1][j-1] + c$ is at least $C[i-1][j-1] \ge C[i][j-1] - 1$ by Lemma 1. $\square$

**Lemma 3 (diagonals).** For $1 \le i \le m$ and $1 \le j \le n$: $C[i-1][j-1] \le C[i][j] \le C[i-1][j-1] + 1$, and $C[i][j] = C[i-1][j-1]$ when $P[i-1] = T[j-1]$.

*Proof.* The right inequality is the third term of (R) with $c \le 1$. For the left one, each term of (R) is at least $C[i-1][j-1]$: the first because $C[i][j-1] + 1 \ge C[i-1][j-1]$ by Lemma 1, the second because $C[i-1][j] + 1 \ge C[i-1][j-1]$ by Lemma 2, and the third because $c \ge 0$. When $P[i-1] = T[j-1]$, the third term is $C[i-1][j-1]$, so $C[i][j] \le C[i-1][j-1]$, and equality follows. $\square$

By Lemma 3 the values along a diagonal never decrease. So for $e \ge 0$ the set $\{i : s_d \le i \le t_d,\ C[i][i + d] \le e\}$ is an initial run $s_d, \ldots, L$ of the diagonal, or empty. Define $L[d][e]$ as its largest element, and $L[d][e] = -\infty$ when it is empty. Since the first cell has the value $s_d$, the set is empty exactly when $e < s_d$.

**Lemma 4.** Line L7 sets $L[d][e]$ to the true value, for every $e$ with $0 \le e \le k$ and every $d$ with $\max(-e, -m) \le d \le n$. For $d < \max(-e, -m)$ the true value is $-\infty$.

*Proof.* The last claim holds because $d < -e$ gives $s_d = -d > e$, and diagonals $d < -m$ have no cells. The terms of line L5 that refer to such diagonals, or to $e - 1 = -1$, are $-\infty$ in the program and in the truth. Induct on $e$, and assume that the stored values of row $e - 1$ are true (no assumption for $e = 0$). Fix $d$ with $\max(-e, -m) \le d \le n$, so $s_d \le e$ and $s_d \le t_d$. Let $\lambda$ be the true $L[d][e]$; it exists since $s_d \le e$. Let $r_0$ be the value of $r$ after line L6.

*Step 1: the cell $(r_0, r_0 + d)$ lies on diagonal $d$ and has a value at most $e$.* Line L6 gives $r_0 \le t_d$, and line L4 gives $r_0 \ge s_d$, since $s_d \le t_d$. Because the values on the diagonal never decrease, it suffices to find a cell of diagonal $d$ with a row at least $r_0$ and a value at most $e$. Let $r_0'$ be the value of $r$ after line L5, so $r_0 = \min(r_0', t_d)$. One term gives $r_0'$.

- The term $s_d$: the first cell has the value $s_d \le e$.
- The term $L[d][e-1] + 1 = i + 1$, with $C[i][i + d] \le e - 1$. If $i < t_d$, the cell $(i + 1, i + 1 + d)$ has a value at most $e$ by Lemma 3. If $i = t_d$, the cell $(t_d, t_d + d)$ has a value at most $e - 1$, and $r_0 = t_d$.
- The term $L[d-1][e-1] = i$, with $C[i][i + d - 1] \le e - 1$. If $i + d \le n$, the cell $(i, i + d)$ lies on diagonal $d$, since $i \le m$, and its value is at most $e$ by Lemma 2. Else $i + d - 1 = n$, so $i \ge 1$ and $i - 1 = n - d = t_d$ (as $i - 1 < m$). The cell $(i - 1, n)$ has a value at most $e$ by Lemma 1, and $r_0 = t_d = i - 1$.
- The term $L[d+1][e-1] + 1 = i + 1$, with $C[i][i + d + 1] \le e - 1$. If $i < m$, the cell $(i + 1, i + 1 + d)$ lies on diagonal $d$ and has a value at most $e$ by Lemma 1. Else $i = m$, and the cell $(m, m + d)$ lies on diagonal $d$ with a value at most $e$ by Lemma 2, and $r_0 = t_d = m$.

*Step 2: $L[d][e] \le \lambda$.* Line L7 adds $q = \mathrm{LCE}(r_0, r_0 + d)$. For $0 \le u < q$ we have $P[r_0 + u] = T[r_0 + d + u]$, so by Lemma 3 the cells $(r_0 + u + 1, r_0 + d + u + 1)$ all have the value of the cell $(r_0, r_0 + d)$, which is at most $e$ by Step 1. They lie on diagonal $d$ because the LCE stops at the end of $P$ or $T$. So the row $r_0 + q$ is in the run, and $r_0 + q \le \lambda$.

*Step 3: $L[d][e] \ge \lambda$.* Let $\mu$ be the least row with $s_d \le \mu \le \lambda$ such that $P[u] = T[u + d]$ for all $u$ with $\mu \le u < \lambda$. It is enough to show $r_0 \ge \mu$: then $\mu \le r_0 \le \lambda$ by Step 2, all characters from row $r_0$ to row $\lambda$ are equal, and the LCE reaches at least $\lambda$.

If $\mu = s_d$, line L4 gives $r_0' \ge s_d$, and $t_d \ge \lambda \ge \mu$ gives $r_0 \ge \mu$. Else $\mu > s_d$, so $\mu \ge 1$ and $\mu + d \ge 1$, and $P[\mu - 1] \ne T[\mu + d - 1]$ by the choice of $\mu$. The value $v = C[\mu][\mu + d]$ is at most $e$, because $\mu \le \lambda$. By (R) with a mismatch, $v$ is one plus one of $C[\mu-1][\mu+d-1]$, $C[\mu][\mu+d-1]$ and $C[\mu-1][\mu+d]$, so $v \ge 1$, $e \ge 1$, and that cell has a value at most $e - 1$.

- If $C[\mu-1][\mu+d-1] \le e - 1$, the cell is on diagonal $d$, so the true $L[d][e-1] \ge \mu - 1$, and the first term of line L5 is at least $\mu$.
- If $C[\mu][\mu+d-1] \le e - 1$, the cell is on diagonal $d - 1$, so $L[d-1][e-1] \ge \mu$.
- If $C[\mu-1][\mu+d] \le e - 1$, the cell is on diagonal $d + 1$, so $L[d+1][e-1] + 1 \ge \mu$.

By the induction hypothesis the stored values of row $e - 1$ are the true ones, so $r_0' \ge \mu$, and $r_0 = \min(r_0', t_d) \ge \mu$ since $t_d \ge \lambda \ge \mu$. $\square$

**Theorem.** LANDAU-VISHKIN$(P, T, k)$ reports, in increasing order, exactly the positions $j \in \{0, \ldots, n\}$ such that $d(P, T[h \ldots j)) \le k$ for some $h \le j$.

*Proof.* Such a $j$ is a match exactly when $C[m][j] \le k$, by the definition of the Sellers table. The cell $(m, j)$ lies on diagonal $d = j - m$, with $-m \le d \le n - m$, and it is the last cell of that diagonal, since $t_d = m$ there. Because the values on the diagonal never decrease, $C[m][m + d] \le k$ holds exactly when $L[d][k] = m$. For $d < -k$ we have $L[d][k] = -\infty \ne m$. By Lemma 4 with $e = k$, the stored values are the true ones, so line L8 reports exactly the matches. It reports them in increasing order of $d$, which is increasing order of $j = m + d$. $\blacksquare$
