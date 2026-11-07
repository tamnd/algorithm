---
title: Convergence of the Gauss-Seidel method
proves: [correctness, termination]
status: full
---

Notation of the page: $A = D + L + U$ with $a_{ii} \ne 0$, $M = D + L$, $G = G_{GS} = -M^{-1} U$, $c = M^{-1} b$. One execution of lines L5 to L7 maps $x_k$ to $x_{k+1}$ with
$$x_{k+1, i} = \frac{1}{a_{ii}} \Bigl( b_i - \sum_{j < i} a_{ij} x_{k+1, j} - \sum_{j > i} a_{ij} x_{k, j} \Bigr), \qquad i = 1, \ldots, n,$$
because when row $i$ is processed, the entries $j < i$ already hold the new values and the entries $j > i$ still hold the old ones. Multiplying by $a_{ii}$ and collecting terms: $(D + L) x_{k+1} = b - U x_k$, that is $x_{k+1} = G x_k + c$.

**Theorem 1 (fixed point and error recursion).** $A x = b$ if and only if $x = G x + c$. If $A x = b$, then $e_{k+1} = G e_k$, and $x_k \to x$ for every $x_0$ if and only if $\rho(G) < 1$.

*Proof.* $x = G x + c \iff (D + L) x = b - U x \iff A x = b$. Subtracting, $e_{k+1} = G e_k$. The last claim is the general criterion for $e_k = G^k e_0$, proved as Theorem 2 of the [Jacobi](/jacobi-method/) correctness proof. $\square$

**Theorem 2 (one coordinate update, symmetric positive definite $A$).** Let $A$ be symmetric positive definite, $A x = b$, and let $y'$ differ from $y$ only in entry $i$, with $y'_i = (b_i - \sum_{j \ne i} a_{ij} y_j)/a_{ii}$. Let $\rho_i = (b - A y)_i$. Then $\|x - y'\|_A^2 = \|x - y\|_A^2 - \rho_i^2 / a_{ii}$.

*Proof.* $y'_i - y_i = (b_i - \sum_j a_{ij} y_j)/a_{ii} = \rho_i / a_{ii}$, so $y' = y + t e_i$ with $t = \rho_i / a_{ii}$ ($e_i$ the unit vector). With $d = x - y$, $\|d - t e_i\|_A^2 = \|d\|_A^2 - 2 t e_i^T A d + t^2 a_{ii}$ by symmetry. Since $A d = b - A y$, $e_i^T A d = \rho_i$, and the right side is $\|d\|_A^2 - 2 \rho_i^2 / a_{ii} + \rho_i^2 / a_{ii}$. $\square$

**Theorem 3 (convergence for symmetric positive definite $A$).** If $A$ is symmetric positive definite, then $\|G v\|_A < \|v\|_A$ for every real $v \ne 0$, hence $\|G\|_A < 1$ and $\rho(G) < 1$. So Gauss-Seidel converges for every $x_0$, and $\|e_k\|_A$ decreases monotonically.

*Proof.* Apply one sweep to the system $A y = 0$ (solution $0$) from $y = v$. By the formula above the sweep produces $G v$, and by Theorem 2 each of the $n$ coordinate updates does not increase $\|y\|_A$. If $\|G v\|_A = \|v\|_A$, then every update had $\rho_i = 0$, so no update changed $y$, and at the moment row $i$ was processed $y = v$ and $(A v)_i = -\rho_i = 0$. So $A v = 0$ and $v = 0$. Thus $\|G v\|_A < \|v\|_A$ for $v \ne 0$. The function $v \mapsto \|G v\|_A$ is continuous on the compact set $\{\|v\|_A = 1\}$, so its maximum $\|G\|_A$ is attained and is below 1. For any norm, $\rho(G) = \lim_k \|G^k\|^{1/k} \le \|G\|$ (Gelfand's formula, valid for the operator norm of a real matrix on $\mathbb{R}^n$ since all norms on the finite-dimensional space of matrices are equivalent). So $\rho(G) \le \|G\|_A < 1$. Monotonicity is $\|e_{k+1}\|_A = \|G e_k\|_A < \|e_k\|_A$ for $e_k \ne 0$. $\square$

**Theorem 4 (strict row diagonal dominance).** Let $\alpha_i = \sum_{j < i} |a_{ij}| / |a_{ii}|$, $\beta_i = \sum_{j > i} |a_{ij}| / |a_{ii}|$, and suppose $\alpha_i + \beta_i < 1$ for all $i$. Let $\eta = \max_i \beta_i / (1 - \alpha_i)$ and $q = \max_i (\alpha_i + \beta_i)$. Then $\eta \le q < 1$ and $\|e_{k+1}\|_\infty \le \eta \|e_k\|_\infty$.

*Proof.* $\beta_i \le (\alpha_i + \beta_i)(1 - \alpha_i)$ is equivalent to $0 \le \alpha_i (1 - \alpha_i - \beta_i)$, which holds; so $\beta_i / (1 - \alpha_i) \le \alpha_i + \beta_i \le q$. From $(D + L) e_{k+1} = -U e_k$, $e_{k+1, i} = -\bigl(\sum_{j < i} a_{ij} e_{k+1, j} + \sum_{j > i} a_{ij} e_{k, j}\bigr)/a_{ii}$. We show $|e_{k+1, i}| \le \eta \|e_k\|_\infty$ by induction on $i$. If it holds for all $j < i$, then $|e_{k+1, i}| \le \alpha_i \eta \|e_k\|_\infty + \beta_i \|e_k\|_\infty$, and $\alpha_i \eta + \beta_i \le \eta$ because $\beta_i \le \eta (1 - \alpha_i)$. The case $i = 1$ has $\alpha_1 = 0$. $\square$

**Theorem 5 (one sweep in floating point).** In the floating point model with $(n + 1) u < 1$, the computed sweep satisfies $(D + L + \Delta L) \hat x_{k+1} + (U + \Delta U) \hat x_k = b + \Delta b$ with $|\Delta L| \le \gamma_{n+1} |L|$, $|\Delta U| \le \gamma_{n+1} |U|$ and $|\Delta b| \le \gamma_{n+1} |b|$, for any order of summation in line L6.

*Proof.* In line L6 each term $a_{ij} x_j$ is formed with one rounding and then takes part in at most $n - 2$ additions; line L7 adds a subtraction and a division. So $\hat x_{k+1, i} = \bigl(b_i (1 + \eta_0) - \sum_{j \ne i} a_{ij} x_j (1 + \eta_j)\bigr)/a_{ii}$ with each $1 + \eta_j$ a product of at most $n + 1$ factors $(1 + \delta)^{\pm 1}$, so $|\eta_j| \le \gamma_{n+1}$ (Higham, Lemma 3.1). Multiply by $a_{ii}$ and set $(\Delta L)_{ij} = a_{ij} \eta_j$ for $j < i$, $(\Delta U)_{ij} = a_{ij} \eta_j$ for $j > i$, $(\Delta b)_i = b_i \eta_0$. $\square$

**Theorem 6 (termination and output).** The pseudocode stops after at most $k_{\max}$ sweeps. If it returns CONVERGED, the residual computed in line L2 for the returned $x$ satisfies $\|r\|_\infty \le \text{tol} \cdot \|b\|_\infty$.

*Proof.* The outer loop has $k_{\max} + 1$ iterations and line L4 returns in the last one. Only line L3 returns CONVERGED, after testing that inequality for the current $x$, which no line changes before the return. $\square$

$\blacksquare$
