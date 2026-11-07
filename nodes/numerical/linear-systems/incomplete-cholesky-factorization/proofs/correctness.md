---
title: IC(0) satisfies the pattern equations and terminates
proves: [correctness, termination]
status: full
---

Exact arithmetic. Notation of the page; write $\tilde a_{ij} = (1 + \alpha \delta_{ij}) a_{ij}$, the entries of $A + \alpha \operatorname{diag}(A)$. Entries of $L$ outside $P$ are $0$.

**Theorem 1 (pattern equations).** If the code returns $L$, then $L$ is lower triangular with positive diagonal, $l_{ij} \ne 0$ only for $(i, j) \in P$, and $(L L^T)_{ij} = \tilde a_{ij}$ for all $(i, j) \in P$.

*Proof.* Rows are built in order and only positions in $P$ are written, so the pattern claim holds, and $l_{ii} = \sqrt d > 0$ by L6 and L7. Fix $(i, j) \in P$ with $j < i$. When L3 runs, rows $1, \dots, i - 1$ are complete and $l_{ik}$ for $k < j$ has already been computed (increasing order in L2). So
$$(L L^T)_{ij} = \sum_{k \le j} l_{ik} l_{jk} = \sum_{k < j} l_{ik} l_{jk} + l_{ij} l_{jj},$$
and only $k$ with $(i, k) \in P$ and $(j, k) \in P$ contribute to the sum; L3 sums exactly these terms and L4 sets $l_{ij} l_{jj} = a_{ij} - \sum_{k < j} l_{ik} l_{jk}$. So $(L L^T)_{ij} = a_{ij} = \tilde a_{ij}$. For the diagonal, $(L L^T)_{ii} = \sum_{j < i} l_{ij}^2 + l_{ii}^2 = \sum_{j < i} l_{ij}^2 + d = (1 + \alpha) a_{ii}$ by L5 and L7. By symmetry of $L L^T$ and of $A$, the equations hold for the transposed positions too. $\square$

**Corollary (full pattern).** If $P$ is the whole lower triangle, Theorem 1 gives $L L^T = A + \alpha \operatorname{diag}(A)$ entrywise, so $L$ is its Cholesky factor, which is unique among lower triangular factors with positive diagonal.

**Lemma 2 (breakdown means a bad pivot).** If the code returns BREAKDOWN at row $i$, then $d = \tilde a_{ii} - \sum_{j < i} l_{ij}^2 \le 0$ for the rows already computed. If $P$ is the whole lower triangle, this happens if and only if $A + \alpha \operatorname{diag}(A)$ is not positive definite.

*Proof.* The first claim is L5 and L6. For the full pattern, rows $1, \dots, i - 1$ form the Cholesky factor $L_{i-1}$ of the leading block $\tilde A_{i-1}$, and $d$ is the Schur complement $\tilde a_{ii} - \tilde a_i^T \tilde A_{i-1}^{-1} \tilde a_i$, whose sign is the sign of $\det \tilde A_i / \det \tilde A_{i-1}$. By Sylvester's criterion all $d > 0$ exactly when the matrix is positive definite. $\square$

**Theorem 3 (termination).** Each row performs at most $i - 1$ executions of L3 and L4, each a finite sum, and one of L5 to L7. So after at most $n$ rows the code returns $L$, or BREAKDOWN at the first row with $d \le 0$. $\blacksquare$
