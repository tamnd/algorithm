---
title: The truncated power method never decreases the variance, and sparse PCA is NP-hard
proves: [correctness]
status: full
---

**Setup.** $A$ is a symmetric positive semidefinite $d \times d$ matrix and $1 \le k \le d$. Let $\mathcal{S}_k = \{x \in \mathbb{R}^d : \|x\|_2 = 1, \|x\|_0 \le k\}$ and $f(x) = x^T A x$. The truncated power method maps $x \in \mathcal{S}_k$ to $T(x) = \operatorname{trunc}_k(Ax) / \|\operatorname{trunc}_k(Ax)\|$, where $\operatorname{trunc}_k(y)$ keeps the $k$ entries of largest absolute value and sets the others to zero, when $Ax \ne 0$.

**Lemma 1 (linear step).** For $g \in \mathbb{R}^d$ with $g \ne 0$, the vector $y^\star = \operatorname{trunc}_k(g)/\|\operatorname{trunc}_k(g)\|$ maximizes $g^T y$ over $y \in \mathcal{S}_k$.

*Proof.* Fix a support $F$ with $|F| \le k$. For $y$ supported on $F$ with $\|y\| = 1$, the Cauchy-Schwarz inequality gives $g^T y = g_F^T y_F \le \|g_F\|$, with equality at $y_F = g_F / \|g_F\|$. So the maximum over $\mathcal{S}_k$ is $\max_{|F| \le k} \|g_F\|$, and $\|g_F\|^2 = \sum_{i \in F} g_i^2$ is largest when $F$ holds the $k$ entries of largest absolute value. That is $y^\star$. $\square$

**Theorem 1 (monotonicity).** For $x \in \mathcal{S}_k$ with $Ax \ne 0$, $f(T(x)) \ge f(x)$. If $Ax = 0$, then $f(x) = 0$ and $x$ is a maximizer only when $A = 0$; the method stops there.

*Proof.* Since $A \succeq 0$, $f$ is convex and $f(y) \ge f(x) + \nabla f(x)^T (y - x) = f(x) + 2 (Ax)^T (y - x)$ for all $y$. Put $g = Ax$ and $y = T(x)$. By Lemma 1, $g^T y \ge g^T x$, because $x \in \mathcal{S}_k$. So $f(y) \ge f(x) + 2(g^T y - g^T x) \ge f(x)$. $\square$

**Corollary (convergence of the value and the fixed points).** The values $f(x_t)$ do not decrease and are at most $\lambda_{\max}(A)$, so they converge. If $x = T(x)$ and $F$ is the support of $x$, then $A_{FF}\, x_F = \|\operatorname{trunc}_k(Ax)\|\, x_F$, so $x_F$ is an eigenvector of the principal submatrix $A_{FF}$ with eigenvalue $\|\operatorname{trunc}_k(Ax)\| = f(x)$. In particular, when $k = d$ there is no truncation and the method is the power iteration, and the value converges to $\lambda_{\max}(A)$ from any start that is not orthogonal to the top eigenspace.

*Proof.* The first sentence is Theorem 1 and the Rayleigh bound $f(x) \le \lambda_{\max}(A)$ for $\|x\| = 1$. For a fixed point, $x = \operatorname{trunc}_k(Ax)/c$ with $c = \|\operatorname{trunc}_k(Ax)\|$, so $(Ax)_i = c x_i$ for $i \in F$, and $(Ax)_F = A_{FF} x_F$ because $x$ is zero outside $F$. Then $f(x) = x_F^T A_{FF} x_F = c$. $\square$

**Theorem 2 (NP-hardness).** Deciding whether $\max_{x \in \mathcal{S}_k} x^T A x \ge t$ for a positive semidefinite integer matrix $A$ and integers $k$ and $t$ is NP-hard.

*Proof.* Reduce from CLIQUE: given a graph $G$ on $n$ vertices with adjacency matrix $W$ and maximum degree $\Delta$, and an integer $k \ge 2$, decide whether $G$ has a clique of $k$ vertices. Put $c = \max(\Delta, 1)$, $A = W + c I$ and $t = k - 1 + c$. $A$ is symmetric and diagonally dominant with a nonnegative diagonal, so it is positive semidefinite by the Gershgorin theorem.

The optimum over $\mathcal{S}_k$ is $\max_{|S| = k} \lambda_{\max}(A_{SS}) = c + \max_{|S| = k} \lambda_{\max}(W_{SS})$, because for a fixed support the best unit vector is the top eigenvector of $A_{SS}$, and supports smaller than $k$ can be enlarged without loss (an eigenvalue of a principal submatrix is at most that of a larger one, by Cauchy interlacing). For a set $S$ of $k$ vertices, $W_{SS}$ is a nonnegative symmetric matrix, so $\lambda_{\max}(W_{SS})$ is at most its largest row sum, which is at most $k - 1$. If $S$ is a clique, $W_{SS} = J - I$ and $\lambda_{\max} = k - 1$ for the vector of ones. If $S$ is not a clique, some vertex $u \in S$ has degree less than $k - 1$ in $G[S]$. Let $z \ge 0$ be a unit Perron vector of $W_{SS}$, so $W_{SS} z = \lambda z$ with $\lambda = \lambda_{\max}(W_{SS})$. Summing the rows, $\lambda \sum_i z_i = \sum_j z_j \deg_S(j) \le (k - 1)\sum_j z_j - z_u$. If $z_u > 0$ this gives $\lambda < k - 1$. If $z_u = 0$, then row $u$ of $W_{SS} z = \lambda z$ gives $\sum_{j \sim u} z_j = 0$, so the support of $z$ avoids $u$ and its neighbors, and $\lambda$ is the top eigenvalue of $W$ on a set of at most $k - 1$ vertices, which is at most $k - 2$. In both cases $\lambda < k - 1$. So the optimum is at least $t$ exactly when $G$ has a $k$-clique. The reduction takes polynomial time and CLIQUE is NP-complete. $\blacksquare$

**Remark.** Theorem 1 shows that the truncated power method is an ascent method; it does not find the global optimum in general, as Theorem 2 makes expected (unless P = NP). The worked example on the page shows a start from which it stops at a fixed point that is not optimal.
