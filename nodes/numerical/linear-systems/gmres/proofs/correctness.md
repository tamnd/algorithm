---
title: GMRES minimizes the residual over the Krylov subspace and terminates
proves: [correctness, termination]
status: full
---

Exact arithmetic throughout. Notation of the page: $A$ nonsingular of order $n$, $r_0 = b - A x_0 \ne 0$, $\beta = \|r_0\|_2$, $\mathcal K_j = \mathcal K_j(A, r_0)$, $\mathcal P_j^0$ the polynomials of degree at most $j$ with value $1$ at $0$. Let $d$ be the grade of $r_0$: the least $d$ with $A^d r_0 \in \mathcal K_d$. Then $\dim \mathcal K_j = j$ for $j \le d$ and $d \le n$.

**Lemma 1 (Arnoldi).** For $j \le d$, after step $j$ of L4 to L6 the vectors $v_1, \dots, v_j$ are orthonormal and span $\mathcal K_j$, $h_{j+1,j} = 0$ if and only if $j = d$, and if $j < d$ then $v_{j+1}$ is a unit vector orthogonal to $v_1, \dots, v_j$ with $\operatorname{span}\{v_1, \dots, v_{j+1}\} = \mathcal K_{j+1}$. In all cases $A v_j = \sum_{i=1}^{j+1} h_{ij} v_i$ (with $h_{j+1,j} v_{j+1}$ read as $0$ when $h_{j+1,j} = 0$), that is $A V_j = V_{j+1} \bar H_j$.

*Proof.* Induction on $j$. For $j = 1$, $v_1 = r_0 / \beta$ spans $\mathcal K_1$. Assume the claim for $v_1, \dots, v_j$. Modified Gram-Schmidt in L5 subtracts from $w = A v_j$ its components along $v_1, \dots, v_j$ one at a time; because the $v_i$ are orthonormal, the coefficient $v_i^T w$ computed from the partially reduced $w$ equals $v_i^T A v_j$ (the earlier subtractions are along vectors orthogonal to $v_i$). So the final $w = A v_j - \sum_{i \le j} h_{ij} v_i$ is orthogonal to $v_1, \dots, v_j$, and $A v_j = \sum_{i \le j} h_{ij} v_i + w$. Since $v_j \in \mathcal K_j$ has a nonzero component along $A^{j-1} r_0$ (the $v_i$ span a strictly increasing chain), $A v_j \in \mathcal K_{j+1} \setminus \mathcal K_j$ when $\dim \mathcal K_{j+1} = j + 1$, i.e. when $j < d$; then $w \ne 0$, $h_{j+1,j} = \|w\|_2 > 0$ and $v_{j+1} = w / h_{j+1,j}$ completes an orthonormal basis of $\mathcal K_{j+1}$. When $j = d$, $A v_j \in A \mathcal K_d \subseteq \mathcal K_d$, so $w = 0$. $\square$

**Lemma 2 (least squares form).** For $x = x_0 + V_j y$, $\|b - A x\|_2 = \|\beta e_1 - \bar H_j y\|_2$.

*Proof.* $b - A x = r_0 - A V_j y = \beta v_1 - V_{j+1} \bar H_j y = V_{j+1} (\beta e_1 - \bar H_j y)$, and $V_{j+1}$ has orthonormal columns, so it preserves the 2-norm. (If $h_{j+1,j} = 0$ the last row of $\bar H_j$ is zero and the same holds with $V_j$.) $\square$

**Lemma 3 (Givens).** Let $Q_j = G_j \cdots G_1$ be the product of the rotations formed in L7, each acting on two consecutive coordinates. Then $Q_j \bar H_j = \begin{pmatrix} R_j \\ 0 \end{pmatrix}$ with $R_j$ upper triangular, $Q_j \beta e_1 = g$, and
$$\min_y \|\beta e_1 - \bar H_j y\|_2 = |g_{j+1}|,$$
attained at $y = R_j^{-1} g_{1:j}$ when $R_j$ is nonsingular.

*Proof.* Induction on $j$. Assume $Q_{j-1} \bar H_{j-1} = \begin{pmatrix} R_{j-1} \\ 0 \end{pmatrix}$. The matrix $\bar H_j$ adds a row of zeros (except $h_{j+1,j}$) and a column $j$ with nonzeros only in rows $1, \dots, j + 1$. The rotations $G_1, \dots, G_{j-1}$ act on rows $1, \dots, j$, so they leave $h_{j+1,j}$ alone and turn the first $j - 1$ columns into $\begin{pmatrix} R_{j-1} \\ 0 \end{pmatrix}$ padded with a zero row; this is exactly L7 applying the old rotations to column $j$. Then $G_j$, with $c = h_{jj}/\rho$ and $s = h_{j+1,j}/\rho$, maps the pair $(h_{jj}, h_{j+1,j})$ to $(\rho, 0)$ and mixes only rows $j$ and $j + 1$, where the first $j - 1$ columns are zero. So $Q_j \bar H_j$ is upper triangular with a zero last row. Since $Q_j$ is orthogonal, $\|\beta e_1 - \bar H_j y\|_2 = \|g - \begin{pmatrix} R_j \\ 0 \end{pmatrix} y\|_2$, whose square is $\|g_{1:j} - R_j y\|_2^2 + g_{j+1}^2$. $\square$

**Lemma 4 ($R_j$ is nonsingular).** If $A$ is nonsingular, then $\bar H_j$ has full column rank $j$ for $j \le d$, so every $\rho$ in L7 is nonzero.

*Proof.* $A V_j = V_{j+1} \bar H_j$ (or $V_j H_j$ when $j = d$); the left side has rank $j$ because $A$ is nonsingular and $V_j$ has independent columns. Hence $\bar H_j$ has rank $j$, and so does $R_j$, whose diagonal entries are the values $\rho$. $\square$

**Theorem 1 (correctness).** At the end of a cycle of $j \le d$ steps, the $x$ formed in L9 is the unique minimizer of $\|b - A x\|_2$ over $x_0 + \mathcal K_j$, and its residual norm is $|g_{j+1}|$. Equivalently $\|r_j\|_2 = \min_{p \in \mathcal P_j^0} \|p(A) r_0\|_2$.

*Proof.* Every $x \in x_0 + \mathcal K_j$ is $x_0 + V_j y$ for a unique $y$ (Lemma 1). By Lemmas 2 and 3 the residual is minimized exactly by $y = R_j^{-1} g_{1:j}$ (Lemma 4), with value $|g_{j+1}|$. The polynomial form follows from $\{r_0 - A q(A) r_0 : \deg q \le j - 1\} = \{p(A) r_0 : p \in \mathcal P_j^0\}$. $\square$

**Corollary (monotonicity).** $\mathcal K_j \subseteq \mathcal K_{j+1}$, so within a cycle $|g_{j+2}| \le |g_{j+1}|$; across a restart the new cycle starts from the last iterate, whose residual is the old minimum, so the residual norms never increase.

**Theorem 2 (termination).** If $A$ is nonsingular, full GMRES ($m = n$) returns the exact solution after $d \le n$ steps; every run returns after at most $\mathrm{kmax}$ Arnoldi steps.

*Proof.* At step $d$, $h_{d+1,d} = 0$ (Lemma 1), so L8 leaves the loop. Then $\mathcal K_d$ is $A$-invariant and $A$ restricted to it is nonsingular, so $A^{-1} r_0 \in \mathcal K_d$ and $x_0 + A^{-1} r_0 = A^{-1} b$ lies in $x_0 + \mathcal K_d$, with residual $0$. By Theorem 1 the iterate formed in L9 attains the minimum, which is $0$. For the step limit: each pass of L4 counts one step, the loop and the restart test in L1 stop when the count reaches $\mathrm{kmax}$, and each cycle performs at least one step, so the number of cycles is at most $\mathrm{kmax} + 1$. $\blacksquare$

**Remarks.** (i) If $A$ is singular, Lemma 4 fails and $\rho = 0$ can occur; then $A$ is singular on $\mathcal K_j$, the code stops with BREAKDOWN, and the iterate of step $j - 1$ is returned. (ii) The SPD bound of the page follows from Theorem 1 by choosing $p$ as the scaled Chebyshev polynomial $T_k((\lambda_{\max} + \lambda_{\min} - 2\lambda)/(\lambda_{\max} - \lambda_{\min})) / T_k((\lambda_{\max} + \lambda_{\min})/(\lambda_{\max} - \lambda_{\min}))$, whose maximum on $[\lambda_{\min}, \lambda_{\max}]$ is at most $2 ((\sqrt\kappa - 1)/(\sqrt\kappa + 1))^k$, and using $\|p(A) r_0\|_2 \le \max_{\lambda} |p(\lambda)| \|r_0\|_2$ for symmetric $A$. (iii) The floating-point backward stability of MGS-GMRES is the theorem of Paige, Rozložník and Strakoš (2006); it is quoted, not proved, here.
