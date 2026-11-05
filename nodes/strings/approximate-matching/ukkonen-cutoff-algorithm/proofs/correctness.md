---
title: Ukkonen's cut-off algorithm reports exactly the ends of the approximate matches
proves: [correctness]
status: full
---

Indices are 0-based, $|P| = m$, $|T| = n$, $k \ge 0$. Let $C[i][j]$ be the Sellers table, so $C[0][j] = 0$, $C[i][0] = i$, and for $i, j \ge 1$

$$C[i][j] = \min\bigl(C[i][j-1] + 1,\; C[i-1][j] + 1,\; C[i-1][j-1] + \delta_{ij}\bigr), \qquad \delta_{ij} = [P[i-1] \ne T[j-1]], \tag{R}$$

by the correctness proof of [Sellers' algorithm](/sellers-algorithm/). Let $\ell_j = \max\{i : C[i][j] \le k\}$, which exists since $C[0][j] = 0$.

**Lemma 1.** For $j \ge 1$: $\ell_j \le \ell_{j-1} + 1$.

*Proof.* Lemma 3 of the [Landau-Vishkin proof](/landau-vishkin-algorithm/) gives $C[i-1][j-1] \le C[i][j]$ for $i, j \ge 1$. If $\ell_j \ge 1$, then $C[\ell_j - 1][j-1] \le C[\ell_j][j] \le k$, so $\ell_{j-1} \ge \ell_j - 1$. If $\ell_j = 0$ the claim is trivial. $\square$

A stored number $s$ is *valid* for a true value $v$ when $s = v$ if $v \le k$, and $s > k$ if $v > k$.

**Lemma 2.** Let $a, b, c$ be valid for $A, B, D$, and $\delta \in \{0, 1\}$. Then $\min(a + 1, b + 1, c + \delta)$ is valid for $V = \min(A + 1, B + 1, D + \delta)$.

*Proof.* Each stored term is at least $\min(\text{true term}, k + 1)$: a stored input equals the true one, or both are above $k$, and then the stored term is above $k$. If $V \le k$, some true term equals $V \le k$, so its input is at most $k$ and stored exactly, and the stored term equals $V$. All other stored terms are at least $\min(\text{true term}, k + 1) \ge V$. So the minimum is $V$. If $V > k$, every true term is above $k$, so every stored term is above $k$, and so is the minimum. $\square$

**Lemma 3 (invariant).** After line L3, and after each pass of the loop of line L4 for column $j$, the following hold. (a) $lact = \ell_j$. (b) For $0 \le i \le \min(\ell_j + 1, m)$, the stored $C[i]$ is valid for $C[i][j]$.

*Proof.* Column 0: line L1 stores the true values $C[i][0] = i$, so (b) holds for all rows. The last row with $i \le k$ is $\min(k, m)$, so line L2 gives (a).

Column $j \ge 1$, assuming (a) and (b) for column $j - 1$. Line L5 sets $top = \min(\ell_{j-1} + 1, m)$. Line L6 keeps $C[0] = 0$, which is the true value. By induction on $i = 1, \ldots, top$, line L8 computes a value valid for $C[i][j]$. Its inputs are the stored $C[i]$, still of column $j - 1$ and valid by (b) since $i \le top$; the new $C[i-1]$, valid by the induction on $i$; and $prev$, the old $C[i-1]$ of column $j - 1$, valid by (b). Lemma 2 applied to (R) gives validity.

So rows 0 to $top$ hold valid values for column $j$. By Lemma 1, $\ell_j \le top$. Every row $i$ with $\ell_j < i \le top$ has a true value above $k$ and so a stored value above $k$, and row $\ell_j$ has a stored value equal to its true value, at most $k$. Hence the loop of line L9, which starts at $top$ and stops at the first stored value at most $k$, stops at $\ell_j$. This gives (a).

For (b): rows 0 to $\ell_j$ are valid. If $\ell_j < m$, row $\ell_j + 1$ has a true value above $k$ by the definition of $\ell_j$, and line L11 stores $k + 1$, which is valid. $\square$

**Theorem.** UKKONEN-CUTOFF$(P, T, k)$ reports, in increasing order, exactly the positions $j \in \{0, \ldots, n\}$ such that $d(P, T[h \ldots j)) \le k$ for some $h \le j$.

*Proof.* By the definition of the Sellers table, $j$ is such a position exactly when $C[m][j] \le k$, that is, when $\ell_j = m$. By Lemma 3(a), line L3 for $j = 0$ and line L10 for $j \ge 1$ report $j$ exactly when $\ell_j = m$. The columns are handled in increasing order of $j$. $\blacksquare$
