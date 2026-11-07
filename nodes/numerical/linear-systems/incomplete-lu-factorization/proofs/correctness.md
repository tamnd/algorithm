---
title: ILU satisfies the pattern equations and terminates
proves: [correctness, termination]
status: full
---

Exact arithmetic. Notation of the page. Let $K$ be the set of positions $(i, j)$ kept by the algorithm (entries of the working row with final level at most $p$; for $p = 0$, the pattern of $A$). Write $l_{ii} = 1$, $l_{ik}$ for the stored strict lower entries and $u_{kj}$ for the stored upper entries; positions not in $K$ hold $0$.

**Lemma 1 (order of updates).** When row $i$ uses $k$ in L3, the entry $w_k$ has received every update $w_k \leftarrow w_k - l_{ik'} u_{k'k}$ with $k' < k$ that the algorithm will ever make.

*Proof.* An update to $w_k$ comes from a multiplier column $k'$ with $k > k'$ (L4 runs over $j > k'$). The heap pops columns in increasing order and every column is pushed before it can be popped, and a column $k$ created by L6 from $k'$ satisfies $k > k'$, so it is pushed while $k'$ is being processed, before $k$ is popped. Hence all $k' < k$ that are ever processed are processed before $k$. The level of $w_k$ also changes only in those updates, so the test $\mathrm{lev}_{ik} \le p$ in L2 uses the final level. $\square$

**Lemma 2 (row identity).** After row $i$ is finished, for every position $j$ present in the working row,
$$w_j = a_{ij} - \sum_{k \in S_i, \ k < j} l_{ik} u_{kj},$$
where $S_i$ is the set of processed multiplier columns of row $i$ and $u_{kj} = 0$ when it is not stored. For $j < i$ this is the value of $w_j$ just before the division in L3, after which $l_{ij} = w_j / u_{jj}$.

*Proof.* $w$ starts as row $i$ of $A$ (absent entries read as $0$). Each processed $k$ subtracts $l_{ik} u_{kj}$ from $w_j$ for every $j > k$ with $u_{kj} \ne 0$ stored; for $j$ not yet present, L6 creates $w_j = -l_{ik} u_{kj} = 0 - l_{ik} u_{kj}$ when $p > 0$. When $p = 0$, a position $j$ absent from row $i$ of $A$ is never kept, so its value does not matter. Terms with $u_{kj} = 0$ contribute nothing. By Lemma 1 every $k < j$ in $S_i$ has been applied before $w_j$ is read in L3 (for $j < i$) or at the end (for $j \ge i$). $\square$

**Theorem 1 (pattern equations).** If no ZERO-PIVOT is returned, then $(L U)_{ij} = a_{ij}$ for every $(i, j) \in K$.

*Proof.* $(L U)_{ij} = \sum_{k \le \min(i, j)} l_{ik} u_{kj}$. Only $k$ with $l_{ik} \ne 0$ stored contribute, that is $k = i$ or $k \in S_i$ kept with level $\le p$; a processed column $k$ that is later dropped cannot exist, since L2 processes only $k$ with final level $\le p$ (Lemma 1) and those are kept in L7. Case $j \ge i$: $u_{ij} = w_j$, so by Lemma 2, $a_{ij} = u_{ij} + \sum_{k \in S_i, k < i} l_{ik} u_{kj} = \sum_{k \le i} l_{ik} u_{kj}$ (with $l_{ii} = 1$; $k \in S_i$ implies $k < i \le j$). Case $j < i$: $l_{ij} u_{jj} = w_j = a_{ij} - \sum_{k \in S_i, k < j} l_{ik} u_{kj}$, so $a_{ij} = \sum_{k \le j} l_{ik} u_{kj}$. $\square$

**Corollary (exact LU).** If $K$ contains every position that becomes nonzero in Gaussian elimination without pivoting (for example when $p \ge n - 1$, since levels along any elimination path are at most $n - 2$, or when $A$ is tridiagonal), then nothing is dropped, $(L U)_{ij} = a_{ij}$ on all positions where $L U$ can be nonzero, and on the remaining positions both sides are $0$; so $L U = A$, the unique LU factorization without pivoting.

**Theorem 2 (termination).** Row $i$ pushes each column at most once at the start or at its creation in L6, so the heap delivers at most $n$ columns; each processed column performs at most $n$ updates. Hence each row finishes after finitely many steps, and after $n$ rows the code returns $L$, $U$, or ZERO-PIVOT as soon as a pivot $u_{kk} = 0$ is met in L3 or L7. $\blacksquare$
