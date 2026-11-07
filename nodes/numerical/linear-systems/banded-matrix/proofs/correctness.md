---
title: Band LU keeps the band and is backward stable
proves: [correctness, termination]
status: full
---

Indices are 1-based. $A$ is $n \times n$ with $a_{ij} = 0$ for $i - j > p$ or $j - i > q$. $A^{(k)}$ is the array after step $k - 1$ of BandLU ($A^{(1)} = A$). Dense Gaussian elimination without pivoting (GE) computes, at step $k$, $l_{ik} = a^{(k)}_{ik} / a^{(k)}_{kk}$ for all $i > k$ and $a^{(k+1)}_{ij} = a^{(k)}_{ij} - l_{ik} a^{(k)}_{kj}$ for all $i, j > k$.

**Lemma 1 (band invariant).** For every $k$, $A^{(k)}$ computed by GE satisfies $a^{(k)}_{ij} = 0$ whenever $i - j > p$ or $j - i > q$.

*Proof.* Induction on $k$; $k = 1$ is the hypothesis. Suppose it holds for $A^{(k)}$, and let $i, j > k$ with $i - j > p$. We need $a^{(k)}_{ij} - l_{ik} a^{(k)}_{kj} = 0$. Here $a^{(k)}_{ij} = 0$ by the hypothesis. Since $j > k$, $i - k > i - j > p$, so $a^{(k)}_{ik} = 0$ and $l_{ik} = 0$. The case $j - i > q$ is symmetric: $a^{(k)}_{ij} = 0$ and, since $i > k$, $j - k > j - i > q$, so $a^{(k)}_{kj} = 0$. Entries with $i \le k$ or $j \le k$ do not change at step $k$, except the multipliers $l_{ik}$, which are zero for $i > k + p$. $\square$

**Theorem 1 (BandLU equals GE).** If all pivots $a^{(k)}_{kk}$ are nonzero, BandLU returns the same $L$ and $U$ as GE, $L$ has lower bandwidth $p$, $U$ has upper bandwidth $q$, and $A = L U$. If some pivot is zero, both fail at the same step.

*Proof.* At step $k$, BandLU computes $l_{ik}$ for $k < i \le \min(k + p, n)$ (lines L3 and L4) and updates $a_{ij}$ for $k < i \le \min(k + p, n)$, $k < j \le \min(k + q, n)$ (lines L5 to L7). By Lemma 1 the multipliers that GE computes for $i > k + p$ are zero, and the entries $a^{(k)}_{kj}$ for $j > k + q$ are zero, so every update of GE that BandLU skips subtracts $0$. Thus the two arrays agree after each step, by induction, and the pivots agree too. The bandwidths follow from Lemma 1, and $A = L U$ is the standard property of GE. $\square$

**Theorem 2 (pivoting).** With partial pivoting over rows $k$ to $\min(k + p, n)$, the computed $U$ has $u_{ij} = 0$ for $j - i > p + q$, and the nonzero multipliers of step $k$ lie in rows $k + 1$ to $\min(k + p, n)$.

*Proof.* Claim: before step $k$, every row $i \ge k$ of the working array has its nonzeros in columns at most $\max(i + q, k - 1 + p + q)$. Also all rows $i > k - 1 + p$ are untouched original rows with no nonzero in column $k - 1$ or before, since no elimination step $k' < k$ reached them ($i > k' + p$). At step $k$ the candidate rows are $k \le r \le \min(k + p, n)$, all with nonzeros in columns at most $\max(r + q, k - 1 + p + q) \le k + p + q$. After the swap and the update, rows $k + 1$ to $k + p$ have nonzeros in columns at most $k + p + q$, which preserves the claim for step $k + 1$, and the pivot row $k$, which becomes row $k$ of $U$, has nonzeros in columns at most $k + p + q$. Rows below $k + p$ are untouched and have no nonzero in column $k$, so the multipliers of step $k$ are in rows $k + 1$ to $\min(k + p, n)$. $\square$

**Theorem 3 (backward error).** In the floating point model, with no underflow or overflow and $w u < 1$, $w = \min(p, q) + 1$, if BandLU runs to completion then $\hat L \hat U = A + \Delta A$ with $|\Delta A| \le \gamma_w |\hat L| |\hat U|$.

*Proof.* The value finally stored at $(i, j)$ is obtained from $a_{ij}$ by subtracting the products $\hat l_{ik} \hat u_{kj}$ for $\max(1, i - p, j - q) \le k < \min(i, j)$, in increasing order of $k$, and then, if $i > j$, dividing by $\hat u_{jj}$. The number $m$ of products is at most $\min(i, j) - \max(i - p, j - q) \le \min(p, q)$: if $i \le j$ it is at most $i - (j - q) \le q$ and at most $i - (i - p) = p$; the case $i > j$ is the same with the roles exchanged. Higham, Lemma 8.4, applied to $y = (c - \sum_{k=1}^{m} a_k b_k)/b_{m+1}$ (with $b_{m+1} = 1$ when $i \le j$) gives $|a_{ij} - \sum_{k \le \min(i,j)} \hat l_{ik} \hat u_{kj}| \le \gamma_{m+1} \sum_{k \le \min(i, j)} |\hat l_{ik}| |\hat u_{kj}|$, with $\hat l_{ii} = 1$. Since $\gamma_{m+1} \le \gamma_w$, this is the claim entrywise. $\square$

**Theorem 4 (termination).** BandLU stops after $n$ steps or at the first zero pivot; `lu_pivoted` stops after $n$ steps or when column $k$ has no nonzero candidate, which happens only if $A$ is singular.

*Proof.* All loops have fixed bounds. If at step $k$ all of $a^{(k)}_{kk}, \ldots, a^{(k)}_{\min(k+p, n), k}$ are zero, then by Theorem 2 column $k$ of the working array is zero in rows $k$ to $n$. The working array is $M A$ with $M$ nonsingular (a product of permutations and unit lower triangular matrices), and its leading $k$ columns have rank at most $k - 1$, so $A$ is singular. $\square$

$\blacksquare$
