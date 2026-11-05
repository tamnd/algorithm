---
title: Turbo-BM outputs exactly the valid shifts
proves: [correctness, termination]
status: full
---

**Claim.** For a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$, TURBO-BOYER-MOORE$(T, P)$ stops and outputs exactly the shifts $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order.

For $m = 0$, line L2 outputs every shift, which is correct, so let $m \ge 1$. A shift $s'$ is *valid* when $s' + m \le n$ and $T[s' \ldots s'+m-1] = P$. We use the tables as defined on the page: $\mathrm{gs}[i]$ is the smallest $d \ge 1$ with (G1) $P[k-d] = P[k]$ for all $k$ with $i < k < m$ and $k \ge d$, and (G2) $i - d < 0$ or $P[i-d] \ne P[i]$; $\mathrm{gs}[0]$ is the smallest period $p$ of $P$ (the boyer-moore page proves this and that GOOD-SUFFIX computes the table); $\lambda(c)$ is the largest $k \le m - 2$ with $P[k] = c$, or $-1$.

**Invariant.** At the start of each iteration of line L5 with window $s$, write $\mathit{sh}$ for the value of $\mathit{shift}$ and $L = m - \mathit{sh} - u$, $R = m - \mathit{sh} - 1$. Then:

(I1) no valid shift lies in $[0, s)$ other than those already output, and every shift output so far is valid;

(I2) if $u > 0$, then $0 \le L$, and $T[s + k] = P[k]$ for $L \le k \le R$; moreover the factor $w = T[s+L \ldots s+R]$ equals the suffix $P[m-u \ldots m-1]$ of length $u$.

Initially $s = 0$ and $u = 0$, so both hold.

**Lemma 1 (the scan).** Under (I2), the loop of lines L7 and L8 stops with $i < 0$ exactly when $s$ is valid, and otherwise with $i \ge 0$, $P[i] \ne T[s+i]$ and $P[k] = T[s+k]$ for $i < k < m$.

*Proof.* The loop compares positions from $m - 1$ down. Line L8 skips positions only when $u \ne 0$ and $i$ has just become $R$; it then sets $i$ to $L - 1$, so the skipped positions are $L, \ldots, R$, where $T[s+k] = P[k]$ by (I2). So the invariant "$P[k] = T[s+k]$ for $i < k < m$" holds throughout, and the loop stops either at $i < 0$, when all positions match, or at a compared position $i$ with $P[i] \ne T[s+i]$. $\square$

Line L10 therefore outputs $s$ exactly when $s$ is valid. It remains to show that the shift added at line L19 skips no valid shift, that it is at least 1, and that (I2) holds for the next window.

**Lemma 2 (shift after a match).** If $s$ is valid, no shift $s + d$ with $1 \le d < p$ is valid, and (I2) holds at $s + p$ with $u = m - p$.

*Proof.* If $s$ and $s + d$ are both valid with $d < p \le m$, then for $d \le k < m$, $P[k] = T[s + k] = P[k - d]$, so $d$ is a period of $P$ smaller than $p$, which is impossible. For (I2): the new $L = m - p - (m - p) = 0$ and $R = m - p - 1$. For $0 \le k \le R$, $T[s + p + k] = P[p + k]$ since $s$ is valid, and $P[p + k] = P[k]$ since $p$ is a period. The factor is $P[p \ldots m-1]$, the suffix of length $m - p$. $\square$

Now let the scan stop at $i \ge 0$ with $a = T[s+i] \ne P[i] = b$, and $v = m - 1 - i$, so the text matches the suffix $z = P[i+1 \ldots m-1]$ of length $v$.

**Lemma 3 (bad character and good suffix).** No shift $s + d$ with $1 \le d < \max(\mathrm{gs}[i], i - \lambda(a))$ is valid.

*Proof.* Let $s + d$ be valid with $d \ge 1$. For $i < k < m$ with $k \ge d$, $P[k - d] = T[s + k] = P[k]$, which is (G1). If $i - d \ge 0$, then $P[i - d] = T[s + i] = a \ne b = P[i]$, which is (G2). So $d \ge \mathrm{gs}[i]$ by minimality. Also, if $i - d \ge 0$ then $P[i-d] = a$ with $i - d \le m - 2$, so $\lambda(a) \ge i - d$, that is $d \ge i - \lambda(a)$; if $i - d < 0$ then $d \ge i + 1 \ge i - \lambda(a)$ since $\lambda(a) \ge -1$. $\square$

**Lemma 4 (turbo shift).** If $u > 0$ and $v < u$, no shift $s + d$ with $1 \le d < u - v$ is valid.

*Proof.* Let $s + d$ be valid with $1 \le d < u - v$; then $d < u$. By (I2), $T[s+k] = P[k]$ for $L \le k \le R$, and since $s + d$ is valid, $T[s + k] = P[k - d]$ for $k \ge d$. So $P[k] = P[k - d]$ for $\max(L, d) \le k \le R$, and in particular for $L + d \le k \le R$. As $P[L \ldots R] = w$ by (I2), this says $w[j] = w[j + d]$ for $0 \le j < u - d$: $w$ has period $d$.

The occurrence at $s + d$ ends at text position $s + m - 1 + d$, and its suffix of length $u$, which is $w$, occupies the text positions $s + m + d - u$ to $s + m - 1 + d$. Since $d < u - v$, the position $s + i = s + m - 1 - v$ lies in this range, at index $j = u - 1 - v - d \ge 0$ of $w$. So $w[u - 1 - v - d] = a$. By the period $d$, $w[u - 1 - v] = a$. But $w$ is the suffix of $P$ of length $u > v$, so $w[u - 1 - v] = P[m - 1 - v] = P[i] = b \ne a$, a contradiction. $\square$

If $v \ge u$ or $u = 0$, the value $u - v \le 0$ excludes nothing, so in all cases Lemmas 3 and 4 show that no shift $s + d$ with $1 \le d < \max(u - v, i - \lambda(a), \mathrm{gs}[i])$ is valid. Line L15 sets $\mathit{shift}$ to this maximum, which is at least $\mathrm{gs}[i] \ge 1$.

**Lemma 5 (the new memory).** If line L17 runs, (I2) holds at $s + \mathit{shift}$ with $u' = \min(m - \mathit{shift}, v)$; if line L18 runs, (I2) holds trivially with $u' = 0$.

*Proof.* Let $d = \mathit{shift} = \mathrm{gs}[i]$ and $u' = \min(m - d, v)$; if $u' = 0$ there is nothing to show. The new values are $L' = m - d - u' \ge 0$ and $R' = m - d - 1$. For $L' \le k \le R'$, the text position $s + d + k$ is position $k + d$ of the old window, with $k + d \ge m - u' \ge m - v = i + 1$, so $T[s + d + k] = P[k + d]$ by Lemma 1. By (G1) for $d$, applied to the index $k + d$, which satisfies $i < k + d < m$ and $k + d \ge d$, we get $P[k + d] = P[k]$. So $T[s + d + k] = P[k]$, and the factor is $P[m - u' \ldots m - 1]$, the suffix of length $u'$. $\square$

**Proof of the claim.** By Lemmas 2 to 5, each iteration moves $s$ by at least 1, outputs $s$ exactly when it is valid, skips no valid shift, and keeps (I2). By induction, (I1) holds at every iteration. The loop stops when $s > n - m$; there are at most $n - m + 1$ iterations, and each inner scan stops after at most $m$ steps because $i$ decreases at each step. At the end, (I1) gives that the output is exactly the set of valid shifts, in increasing order because $s$ only increases. $\blacksquare$
