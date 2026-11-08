---
title: Consistency, l2 stability, convergence and the maximum principle for Crank-Nicolson
proves: [correctness]
status: full
---

**Setting.** $u_t = \kappa u_{xx}$ on $[0, \ell] \times [0, T]$ with Dirichlet data. The grid is $x_j = j\Delta x$, $\Delta x = \ell/M$, $t_n = n\Delta t$, and $r = \kappa\Delta t/\Delta x^2$. Let $D$ be the $(M - 1) \times (M - 1)$ matrix of $\delta^2$ with zero boundary values, that is $\operatorname{tridiag}(1, -2, 1)$. On interior vectors the norm is $\|V\|_{\Delta x} = (\Delta x\sum_{j=1}^{M-1}V_j^2)^{1/2}$. Note that $\|V\|_{\Delta x} \le \sqrt\ell\,\|V\|_\infty$.

## Lemma 1 (truncation error)

Let $u$ be a solution with $u_{ttt}$, $u_{xxtt}$ and $u_{xxxx}$ continuous and bounded by $K$. Define
$$\tau^n_j = \frac{u(x_j, t_{n+1}) - u(x_j, t_n)}{\Delta t} - \frac{\kappa}{2\Delta x^2}\big(\delta^2u(\cdot, t_{n+1}) + \delta^2u(\cdot, t_n)\big)_j.$$
Then $|\tau^n_j| \le K\big(\tfrac{1}{24}\Delta t^2 + \tfrac{\kappa}{8}\Delta t^2 + \tfrac{\kappa}{12}\Delta x^2\big)$.

*Proof.* Write $m = t_{n+1/2}$. Taylor's theorem with remainder gives $(u(x_j, t_{n+1}) - u(x_j, t_n))/\Delta t = u_t(x_j, m) + \rho_1$ with $|\rho_1| \le K\Delta t^2/24$. For each fixed $t$, $\delta^2u/\Delta x^2 = u_{xx} + \rho_2$ with $|\rho_2| \le K\Delta x^2/12$, by the fourth-order Taylor expansion in $x$ with the mean value form. The average of $u_{xx}$ at $t_{n+1}$ and $t_n$ equals $u_{xx}(x_j, m) + \rho_3$ with $|\rho_3| \le K\Delta t^2/8$. This is the error of the trapezoidal average for a function with second derivative $u_{xxtt}$. Since $u_t = \kappa u_{xx}$ at $(x_j, m)$, the leading terms cancel, and $\tau = \rho_1 - \kappa(\rho_2 + \rho_3)$. $\square$

## Lemma 2 (spectrum)

$D$ is symmetric with orthogonal eigenvectors $v^{(k)}_j = \sin(k\pi j/M)$ and eigenvalues $-4s_k$, $s_k = \sin^2(k\pi/(2M))$, for $k = 1, \dots, M - 1$.

*Proof.* $\sin(k\pi(j-1)/M) + \sin(k\pi(j+1)/M) = 2\cos(k\pi/M)\sin(k\pi j/M)$, and $2\cos\phi - 2 = -4\sin^2(\phi/2)$. The vector vanishes at $j = 0$ and $j = M$, so the boundary rows are correct. A real symmetric matrix with distinct eigenvalues has orthogonal eigenvectors. $\square$

## Theorem 1 (unconditional $l^2$ stability)

For every $r > 0$, the matrices $A = I - \tfrac r2D$ and $B = I + \tfrac r2D$ are symmetric and share the eigenvectors of $D$. $A$ has eigenvalues $1 + 2rs_k \ge 1$, and $C = A^{-1}B$ has eigenvalues $g_k = (1 - 2rs_k)/(1 + 2rs_k) \in (-1, 1)$. Hence $\|CV\|_{\Delta x} \le \|V\|_{\Delta x}$ and $\|A^{-1}V\|_{\Delta x} \le \|V\|_{\Delta x}$.

*Proof.* The eigenvalues follow from Lemma 2. A symmetric matrix has 2-norm equal to its largest eigenvalue modulus, and $\|\cdot\|_{\Delta x}$ is a multiple of the Euclidean norm. Since $0 < s_k < 1$ and $r > 0$, $|1 - 2rs_k| < 1 + 2rs_k$. $\square$

The tests check $g_k$ (and its $\theta$-scheme form $(1 - 4(1 - \theta)rs_k)/(1 + 4\theta rs_k)$) to rounding error, and check that the $l^2$ norm never grows for $r = 100$.

## Theorem 2 (convergence)

Let $e^n_j = u(x_j, t_n) - U^n_j$ for $j = 1, \dots, M - 1$, with exact boundary values. Then
$$\|e^n\|_{\Delta x} \le \|e^0\|_{\Delta x} + t_n\sqrt\ell\max_m\|\tau^m\|_\infty.$$
So with exact initial values the error is $O(\Delta t^2 + \Delta x^2)$ in $l^2$ for any relation between $\Delta t$ and $\Delta x$.

*Proof.* The exact solution satisfies $Au^{n+1} = Bu^n + b^n + \Delta t\,\tau^n$, where $b^n$ holds the boundary terms. The scheme satisfies the same relation without $\tau^n$ and with the same $b^n$. Subtracting, $e^{n+1} = Ce^n + \Delta t\,A^{-1}\tau^n$. By Theorem 1, $\|e^{n+1}\|_{\Delta x} \le \|e^n\|_{\Delta x} + \Delta t\|\tau^n\|_{\Delta x}$, and $\|\tau^n\|_{\Delta x} \le \sqrt\ell\|\tau^n\|_\infty$. Sum over $n$. $\square$

The max-norm table on the page shows order 2 as well. That is observed, not proved here.

## Theorem 3 (maximum principle for $r \le 1$)

If $r \le 1$, then every new value $U^{n+1}_j$ lies between the minimum and the maximum of $\{U^n_0, \dots, U^n_M, U^{n+1}_0, U^{n+1}_M\}$.

*Proof.* The scheme at node $j$ reads
$$(1 + r)U^{n+1}_j = \tfrac r2\big(U^{n+1}_{j-1} + U^{n+1}_{j+1}\big) + (1 - r)U^n_j + \tfrac r2\big(U^n_{j-1} + U^n_{j+1}\big).$$
All coefficients on the right are nonnegative when $r \le 1$, and they sum to $1 + r$. Let $j$ be an interior index where $U^{n+1}$ is largest among interior nodes, and let $S$ be the maximum of the data set above. If $U^{n+1}_j > S$, then each neighbour value at the new level is at most $U^{n+1}_j$, either because it is interior or because it is boundary data $\le S$. The old values are at most $S$. So $(1 + r)U^{n+1}_j \le rU^{n+1}_j + S$, which gives $U^{n+1}_j \le S$, a contradiction. The minimum is handled in the same way. $\square$

For $r > 1$ the coefficient $1 - r$ is negative, and the theorem fails. The test with a single hot node and $r = 25$ shows a negative centre value after one step.

## Proposition (conservation with zero-flux boundaries)

With ghost values $U_{-1} = U_1$ and $U_{M+1} = U_{M-1}$, the second difference operator $D_N$ on $(U_0, \dots, U_M)$ has rows $(-2, 2)$ at $j = 0$ and $(2, -2)$ at $j = M$. Let $w = (\tfrac12, 1, \dots, 1, \tfrac12)$. Then $w^TD_N = 0$.

*Proof.* Column 0 of $D_N$ has entries $-2$ (row 0) and $1$ (row 1), so $w^T$ times it is $-1 + 1 = 0$. Column 1 has entries $2$, $-2$ and $1$ in rows 0, 1 and 2, giving $1 - 2 + 1 = 0$. Interior columns give $1 - 2 + 1 = 0$, and the last two columns are symmetric to the first two. $\square$

Applying $w^T$ to $(I - \tfrac r2D_N)U^{n+1} = (I + \tfrac r2D_N)U^n$ gives $w^TU^{n+1} = w^TU^n$. So the trapezoidal total heat $\Delta x\,w^TU$ is constant in exact arithmetic, and the tests confirm it to $10^{-14}$.

## Exactness on quadratics

If $u = a + bx + cx^2 + 2c\kappa t$, then $\delta^2u/\Delta x^2 = 2c$ exactly, and $(u^{n+1} - u^n)/\Delta t = 2c\kappa$ exactly, so $\tau = 0$. With exact boundary values, Theorem 2 gives $e^n = 0$ for all $n$. The tests confirm this with time-dependent boundary values.
