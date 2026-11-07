---
title: Correctness of the Levinson-Durbin recursion
proves: [correctness, termination]
status: full
---

Exact arithmetic, $r_0 = 1$. Write $\rho^{(k)} = (r_1, \ldots, r_k)^T$, so $T_{k+1} = \begin{pmatrix} T_k & E_k \rho^{(k)} \\ \rho^{(k)T} E_k & 1 \end{pmatrix}$, and $E_k T_k E_k = T_k$ because $(T_k)_{ij}$ depends only on $|i - j|$.

**Lemma 1 (Durbin step).** Let $T_k$ be nonsingular, $T_k y = -\rho^{(k)}$, and $\beta = 1 + \rho^{(k)T} y \ne 0$. Then $T_{k+1}$ is nonsingular and $T_{k+1} y' = -\rho^{(k+1)}$ for $y' = (y + \alpha E_k y, \alpha)$ with $\alpha = -(r_{k+1} + \rho^{(k)T} E_k y)/\beta$.

*Proof.* The first $k$ rows: $T_k(y + \alpha E_k y) + \alpha E_k \rho^{(k)} = -\rho^{(k)} + \alpha E_k(T_k y + \rho^{(k)}) = -\rho^{(k)}$, using $T_k E_k = E_k T_k$. The last row: $\rho^{(k)T} E_k (y + \alpha E_k y) + \alpha = \rho^{(k)T} E_k y + \alpha(\rho^{(k)T} y + 1) = \rho^{(k)T} E_k y + \alpha\beta = -r_{k+1}$ by the choice of $\alpha$. Nonsingularity follows from Lemma 3. $\square$

The line L4 sum $\sum_{j<k} r_{k-j} y_j$ is $\rho^{(k)T} E_k y$, and line L5 is the formula of the lemma.

**Lemma 2 (Levinson step).** Let $T_k x = (b_0, \ldots, b_{k-1})^T$ and $y$, $\beta$ as in Lemma 1. Then $x' = (x + \mu E_k y, \mu)$ with $\mu = (b_k - \rho^{(k)T} E_k x)/\beta$ solves $T_{k+1} x' = (b_0, \ldots, b_k)^T$.

*Proof.* First $k$ rows: $T_k x + \mu(E_k T_k y + E_k \rho^{(k)}) = T_k x$. Last row: $\rho^{(k)T} E_k x + \mu(\rho^{(k)T} y + 1) = \rho^{(k)T} E_k x + \mu\beta = b_k$. $\square$

Line L10's sum $\sum_{j<k} r_{j+1} x_{k-1-j}$ is $\rho^{(k)T} E_k x$.

**Lemma 3 (the scalar $\beta$).** With $\beta_k = 1 + \rho^{(k)T} y^{(k)}$, we have $\beta_k = \det T_{k+1}/\det T_k$, and $\beta_k = (1 - \alpha_{k-1}^2)\beta_{k-1}$ with $\beta_0 = 1$.

*Proof.* By the block formula for the determinant, $\det T_{k+1} = \det T_k \cdot (1 - \rho^{(k)T} E_k T_k^{-1} E_k \rho^{(k)}) = \det T_k \cdot (1 - \rho^{(k)T} T_k^{-1} \rho^{(k)}) = \det T_k (1 + \rho^{(k)T} y^{(k)})$. For the recurrence, $\rho^{(k+1)T} y^{(k+1)} = \rho^{(k)T}(y + \alpha E_k y) + r_{k+1}\alpha = \rho^{(k)T} y + \alpha(\rho^{(k)T} E_k y + r_{k+1}) = \rho^{(k)T} y - \alpha^2 \beta_k$. So $\beta_{k+1} = \beta_k - \alpha^2\beta_k$. $\square$

**Theorem 4.** If all leading minors of $T$ are nonzero, the procedure LEVINSON returns $T^{-1} b$; at step $k$ it holds $x = x^{(k)}$, $y = y^{(k)}$ (while $k < n - 1$), $\beta = \beta_k$ after line L9.

*Proof.* Induction on $k$. For $k = 1$ (the state before the loop), $x = (b_0)$ solves $T_1 x = b_0$, $y = (-r_1)$ solves $T_1 y = -r_1$, $\alpha = y_0$, $\beta_0 = 1$. At step $k$, line L9 computes $\beta_k$ by Lemma 3, which is nonzero by hypothesis, so Lemmas 2 and 1 give $x^{(k+1)}$ and $y^{(k+1)}$. After $k = n - 1$, $x = x^{(n)} = T^{-1} b$. $\square$

**Theorem 5 (definiteness test).** $T$ is positive definite if and only if $\beta_k > 0$ for $k = 0, \ldots, n - 1$, if and only if $|\alpha_k| < 1$ for $k = 0, \ldots, n - 2$. So LEVINSON with the check either returns $T^{-1}b$ or correctly reports that $T$ is not positive definite.

*Proof.* By Lemma 3, $\det T_k = \prod_{j < k} \beta_j$, so all leading minors are positive (Sylvester's criterion) if and only if all $\beta_j > 0$. Since $\beta_{k+1} = (1 - \alpha_k^2)\beta_k$, with $\beta_0 = 1$, this holds if and only if every $1 - \alpha_k^2 > 0$. If the check fails at step $k$, the first nonpositive $\beta_k$ is $\det T_{k+1}/\det T_k$ with $\det T_k > 0$, so $\det T_{k+1} \le 0$ and $T$ is not positive definite. $\square$

**Termination.** The loop of line L8 runs $n - 1$ times, and each step performs a fixed number of length $k$ operations. $\blacksquare$
