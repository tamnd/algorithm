---
title: Correctness of cyclic reduction
proves: [correctness, termination]
status: full
---

Exact arithmetic. A level acts on a tridiagonal system of order $N \ge 2$ with rows $a_i x_{i-1} + b_i x_i + c_i x_{i+1} = d_i$, $a_0 = c_{N-1} = 0$. Let $E = \{0, 2, 4, \ldots\}$ and $O = \{1, 3, 5, \ldots\}$ be the even and odd indices below $N$.

**Lemma 1 (one level is a Schur complement).** Suppose $b_k \ne 0$ for every $k \in E$. Write $A$ in the order $(E, O)$ as $\begin{pmatrix} D_E & A_{EO} \\ A_{OE} & A_{OO} \end{pmatrix}$. Then $D_E$ is diagonal, $A_{OO}$ is diagonal, and the Schur complement $S = A_{OO} - A_{OE} D_E^{-1} A_{EO}$, with right-hand side $d_O - A_{OE} D_E^{-1} d_E$, is the tridiagonal system of line L6.

*Proof.* Two indices of the same parity differ by at least $2$, so they are not coupled, and both diagonal blocks are diagonal. Row $i \in O$ of $A_{OE}$ has the entries $a_i$ in column $i - 1$ and $c_i$ in column $i + 1$ (if $i + 1 < N$). Column $j \in O$ of $A_{EO}$ has $c_{j-1}$ in row $j - 1$ and $a_{j+1}$ in row $j + 1$. So $(A_{OE} D_E^{-1} A_{EO})_{ij}$ is a sum over $k \in \{i - 1, i + 1\} \cap \{j - 1, j + 1\}$, which is empty unless $|i - j| \le 2$. For $j = i$ it is $a_i c_{i-1}/b_{i-1} + c_i a_{i+1}/b_{i+1}$, so $S_{ii} = b_i + \alpha_i c_{i-1} + \gamma_i a_{i+1}$. For $j = i - 2$ only $k = i - 1$ contributes, $a_i a_{i-1}/b_{i-1}$, so $S_{i,i-2} = \alpha_i a_{i-1}$; symmetrically $S_{i,i+2} = \gamma_i c_{i+1}$. The right-hand side is $d_i + \alpha_i d_{i-1} + \gamma_i d_{i+1}$ in the same way. (When $i + 1 = N$, the terms with $i + 1$ are absent, as in line L5.) $\square$

**Theorem 2 (one level is exact).** Under the hypothesis of Lemma 1, $x$ solves $A x = d$ if and only if $x_O$ solves $S x_O = d_O - A_{OE} D_E^{-1} d_E$ and, for each $i \in E$, $x_i = (d_i - a_i x_{i-1} - c_i x_{i+1})/b_i$.

*Proof.* The block system is $D_E x_E + A_{EO} x_O = d_E$ and $A_{OE} x_E + A_{OO} x_O = d_O$. The first gives $x_E = D_E^{-1}(d_E - A_{EO} x_O)$, which is line L11, and substituting it into the second gives the reduced system. Conversely these two relations imply both block equations. $\square$

**Theorem 3 (the algorithm is elimination without pivoting on $P A P^T$).** Let $P$ order the indices as the even indices of level $0$, then (in original numbering) those eliminated at level $1$, and so on, ending with the single index of the last level. The pivots used by the algorithm are, in order, the pivots of Gaussian elimination without pivoting on $P A P^T$. Hence the algorithm runs without a zero pivot if and only if all leading principal minors of $P A P^T$ are nonzero, and then it returns $A^{-1} d$.

*Proof.* Eliminating the first block of $P A P^T$, the diagonal block $D_E$, by Gaussian elimination uses the pivots $b_k$, $k \in E$, unchanged, since no elimination step touches another row of $E$; what remains is exactly the Schur complement $S$ of Lemma 1. Induct on the levels: the pivots of the next block are the even diagonal entries of $S$, and so on, and the last pivot is the $1 \times 1$ system of line L7. Gaussian elimination without pivoting completes if and only if the leading principal minors are nonzero, since the $k$-th pivot is the ratio of the $k$-th and $(k-1)$-th minors. By Theorem 2 at every level, the back substitution returns the solution. $\square$

In particular, if $A$ is singular then so is $P A P^T$, its last leading minor is $\det(P A P^T) = 0$, and the algorithm stops with a zero pivot.

**Theorem 4 (diagonal dominance improves).** If $\beta = \beta(A) = \max_i (|a_i| + |c_i|)/|b_i| < 1$, then every $b_k \ne 0$ and the reduced matrix satisfies $\beta(S) \le \beta^2$.

*Proof.* Fix $i \in O$ and write $p = |a_i|$, $q = |c_i|$, $s = |c_{i-1}|/|b_{i-1}|$ and $t = |a_{i+1}|/|b_{i+1}|$ (with $q = t = 0$ when $i + 1 = N$). Dominance of rows $i - 1$ and $i + 1$ gives $|a_{i-1}|/|b_{i-1}| \le \beta - s$ and $|c_{i+1}|/|b_{i+1}| \le \beta - t$. Hence
$$|S_{i,i-2}| + |S_{i,i+2}| = p\frac{|a_{i-1}|}{|b_{i-1}|} + q\frac{|c_{i+1}|}{|b_{i+1}|} \le \beta(p + q) - (ps + qt),$$
$$|S_{ii}| \ge |b_i| - ps - qt.$$
Since $p + q \le \beta |b_i|$, the first bound is at most $\beta^2 |b_i| - (ps + qt) \le \beta^2(|b_i| - ps - qt) \le \beta^2 |S_{ii}|$, using $\beta^2 \le 1$. Also $|S_{ii}| \ge |b_i| - (p + q)\beta \ge (1 - \beta^2)|b_i| > 0$. $\square$

**Theorem 5 (SPD is preserved).** If $A$ is symmetric positive definite, then $P A P^T$ is, every Schur complement of a symmetric positive definite matrix is symmetric positive definite, and all pivots are positive. $\square$

**Termination.** Each pass of line L2 maps $N \ge 2$ to $\lfloor N/2 \rfloor$, with $1 \le \lfloor N/2 \rfloor < N$, so after $\lfloor \log_2 n \rfloor$ passes $N = 1$; the back substitution pops the same number of systems. The algorithm either raises at a zero pivot or returns. $\blacksquare$
