---
title: Gram-Schmidt computes the thin QR factorization
proves: [correctness, termination]
status: full
---

Exact arithmetic. $A = [a_1, \ldots, a_n] \in \mathbb{R}^{m \times n}$, $S_j = \operatorname{span}\{a_1, \ldots, a_j\}$, $S_0 = \{0\}$. Write $a_k^{(j)}$ for the content of column $k$ after the first $j$ passes of the outer loop of MGS ($a_k^{(0)} = a_k$).

**Lemma 1 (MGS invariant).** Suppose passes $1, \ldots, j$ of MGS completed. Then $q_1, \ldots, q_j$ are orthonormal, $\operatorname{span}\{q_1, \ldots, q_i\} = S_i$ for $i \le j$, and for every $k > j$
$$a_k^{(j)} = a_k - \sum_{i=1}^{j} r_{ik} q_i, \qquad q_i^T a_k^{(j)} = 0 \ (i \le j), \qquad r_{ik} = q_i^T a_k \ (i \le j).$$

*Proof.* Induction on $j$; $j = 0$ is empty. Assume it for $j - 1$. Pass $j$ sets $q_j = a_j^{(j-1)} / r_{jj}$ with $r_{jj} = \|a_j^{(j-1)}\|_2 > 0$ (lines L2 to L4). By the hypothesis $a_j^{(j-1)}$ is orthogonal to $q_1, \ldots, q_{j-1}$, so $q_1, \ldots, q_j$ are orthonormal. Also $a_j^{(j-1)} = a_j - \sum_{i<j} r_{ij} q_i$ lies in $S_j$ and $a_j$ lies in $\operatorname{span}\{q_1, \ldots, q_j\}$, so with $\operatorname{span}\{q_1, \ldots, q_{j-1}\} = S_{j-1}$ the spans agree. For $k > j$, line L6 sets $r_{jk} = q_j^T a_k^{(j-1)} = q_j^T a_k - \sum_{i<j} r_{ik} q_j^T q_i = q_j^T a_k$, and line L7 gives $a_k^{(j)} = a_k^{(j-1)} - r_{jk} q_j$, which is the displayed formula. Then $q_j^T a_k^{(j)} = r_{jk} - r_{jk} = 0$, and for $i < j$, $q_i^T a_k^{(j)} = q_i^T a_k^{(j-1)} - r_{jk} q_i^T q_j = 0$. $\square$

**Theorem 1 (MGS).** If $A$ has rank $n$, MGS does not fail and returns $Q$ with $Q^T Q = I$ and $R$ upper triangular with $r_{jj} > 0$ and $A = Q R$. If $A$ has rank less than $n$, MGS fails at the least $j$ with $a_j \in S_{j-1}$.

*Proof.* Before pass $j$, Lemma 1 gives $a_j^{(j-1)} = a_j - P_{j-1} a_j$, where $P_{j-1} = \sum_{i<j} q_i q_i^T$ is the orthogonal projector onto $S_{j-1}$, since $r_{ij} = q_i^T a_j$. So $r_{jj} = 0$ exactly when $a_j \in S_{j-1}$. With rank $n$ this never happens. Then $a_j = a_j^{(j-1)} + \sum_{i<j} r_{ij} q_i = \sum_{i \le j} r_{ij} q_i$, which is column $j$ of $Q R$ with $r_{ij} = 0$ for $i > j$. If the rank is less than $n$, some $a_j$ lies in $S_{j-1}$; at the least such $j$ the passes before it succeed and pass $j$ meets $r_{jj} = 0$ in line L3. $\square$

**Theorem 2 (CGS gives the same factors).** If $A$ has rank $n$, CGS returns the same $Q$ and $R$ as MGS; it fails at the same step otherwise.

*Proof.* Induction on $j$. If $q_1, \ldots, q_{j-1}$ agree, line C2 computes $r_{ij} = q_i^T a_j$, which by Lemma 1 is what MGS uses, and line C3 computes $v = a_j - \sum_{i<j} r_{ij} q_i = a_j^{(j-1)}$. So $r_{jj}$ and $q_j$ agree. $\square$

**Theorem 3 (uniqueness and the determinant formula).** If $A = Q R = Q' R'$ are two thin QR factorizations with positive diagonals, then $Q = Q'$ and $R = R'$. Moreover $r_{jj}^2 = \det G_j / \det G_{j-1}$, where $G_j$ is the leading $j \times j$ block of $G = A^T A$ and $\det G_0 = 1$.

*Proof.* $A^T A = R^T R = R'^T R'$ are two Cholesky factorizations of the positive definite $A^T A$, and the Cholesky factor with positive diagonal is unique (see the [Cholesky decomposition](/cholesky-decomposition/)). So $R = R'$ and $Q = A R^{-1} = Q'$. The leading block satisfies $G_j = R_j^T R_j$ with $R_j$ the leading block of $R$, so $\det G_j = \prod_{i \le j} r_{ii}^2$, and the ratio of consecutive determinants is $r_{jj}^2$. $\square$

**Termination.** All loops have fixed bounds; the procedures stop after $n$ outer passes or at the first failure. $\square$

$\blacksquare$
