---
title: FTCS is stable for r at most 1/2 and then converges with error O(Δt + Δx^2) in the maximum norm
proves: [correctness, termination, stability, convergence]
status: full
---

**Setting.** The problem is $u_t = \kappa u_{xx}$ for $0 < x < 1$, $0 < t \le T$, with $\kappa > 0$, $u(x, 0) = u_0(x)$, $u(0, t) = g_L(t)$, $u(1, t) = g_R(t)$. The grid is $x_j = j\Delta x$ with $\Delta x = 1/J$, $t^n = n\Delta t$, and $r = \kappa\Delta t/\Delta x^2$. We use the maximum norm $\|v\|_\infty = \max_j |v_j|$ over the grid points.

**Lemma 1 (the loop).** After iteration $n$ of the loop of line L3, the array holds $U^{n+1}$, where $U^0_j = u_0(x_j)$, $U^{n+1}_j = U^n_j + r(U^n_{j+1} - 2U^n_j + U^n_{j-1})$ for $0 < j < J$, $U^{n+1}_0 = g_L(t^{n+1})$ and $U^{n+1}_J = g_R(t^{n+1})$. The algorithm stops after $N$ iterations.

*Proof.* Induction on $n$. Line L2 copies $U^0$. Line L4 computes the interior values of $U^{n+1}$ from the old array only (the new values go to a second array $v$), line L5 sets the two boundary values, and line L6 makes $v$ the current array. The loop is a for loop with $N$ iterations. $\square$

**Lemma 2 (maximum principle).** If $0 \le r \le \tfrac12$, then for $0 < j < J$, $U^{n+1}_j$ is a convex combination of $U^n_{j-1}$, $U^n_j$, $U^n_{j+1}$. Hence $\min(\min_j U^n_j, \text{boundary}) \le U^{n+1}_j \le \max(\max_j U^n_j, \text{boundary})$, and with zero boundary values $\|U^{n+1}\|_\infty \le \|U^n\|_\infty$.

*Proof.* $U^{n+1}_j = r U^n_{j-1} + (1 - 2r)U^n_j + r U^n_{j+1}$. The three weights are non-negative exactly when $r \le \tfrac12$, and they sum to $1$. $\square$

**Lemma 3 (truncation error).** Assume that $u_{tt}$ and $u_{xxxx}$ are continuous on $[0, 1] \times [0, T]$, with $M_t = \max|u_{tt}|$ and $M_x = \max|u_{xxxx}|$. Insert the exact solution into the scheme and define $\tau^n_j$ by

$$u(x_j, t^{n+1}) = u(x_j, t^n) + r\big(u(x_{j+1}, t^n) - 2u(x_j, t^n) + u(x_{j-1}, t^n)\big) + \Delta t\, \tau^n_j.$$

Then $|\tau^n_j| \le \tfrac12 \Delta t M_t + \tfrac{1}{12}\kappa\Delta x^2 M_x$.

*Proof.* By Taylor's formula in $t$, $u(x_j, t^{n+1}) - u(x_j, t^n) = \Delta t\, u_t(x_j, t^n) + \tfrac12 \Delta t^2 u_{tt}(x_j, \theta)$ for some $\theta$. By Taylor's formula to fourth order in $x$, $u(x_{j+1}, t^n) - 2u(x_j, t^n) + u(x_{j-1}, t^n) = \Delta x^2 u_{xx}(x_j, t^n) + \tfrac{1}{12}\Delta x^4 u_{xxxx}(\xi, t^n)$ for some $\xi$, by the intermediate value theorem applied to the two remainders. Multiply the second identity by $r = \kappa \Delta t/\Delta x^2$, subtract, and use $u_t = \kappa u_{xx}$: $\Delta t\,\tau^n_j = \tfrac12 \Delta t^2 u_{tt} - \tfrac{1}{12}\kappa\Delta t\Delta x^2 u_{xxxx}$. $\square$

**Theorem (convergence).** Under the assumptions of Lemma 3 and $r \le \tfrac12$, the error $e^n_j = u(x_j, t^n) - U^n_j$ satisfies

$$\|e^n\|_\infty \le t^n\left(\tfrac12\Delta t M_t + \tfrac{1}{12}\kappa\Delta x^2 M_x\right) \quad \text{for } t^n \le T.$$

*Proof.* Subtract the scheme from the identity of Lemma 3. For $0 < j < J$, $e^{n+1}_j = r e^n_{j-1} + (1 - 2r)e^n_j + r e^n_{j+1} + \Delta t\,\tau^n_j$, and $e^{n+1}_0 = e^{n+1}_J = 0$ because the boundary values are exact. By Lemma 2 the convex combination has absolute value at most $\|e^n\|_\infty$, so $\|e^{n+1}\|_\infty \le \|e^n\|_\infty + \Delta t \max_j|\tau^n_j|$. Since $e^0 = 0$, summing $n$ such inequalities gives the bound. $\blacksquare$

**Theorem (the bound $r \le \tfrac12$ is sharp).** With zero boundary values, one step is $U^{n+1} = A U^n$ on the interior values, where $A$ is the symmetric matrix $I + rT$ and $T$ is the tridiagonal matrix with $-2$ on the diagonal and $1$ beside it. Its eigenvectors are $v^{(k)}_j = \sin(k\pi x_j)$, $k = 1, \ldots, J-1$, with eigenvalues $g_k = 1 - 4r\sin^2(k\pi\Delta x/2)$. Hence $\|A^n\|_2 = \max_k |g_k|^n$. If $r \le \tfrac12$, every $|g_k| \le 1$. If $r > \tfrac12$, then $g_{J-1} = 1 - 4r\cos^2(\pi\Delta x/2) \to 1 - 4r < -1$ as $\Delta x \to 0$, so for all small $\Delta x$ the norm $\|A^n\|_2$ grows geometrically in $n$, and no bound uniform in $\Delta x$ holds on $[0, T]$.

*Proof.* The identity $\sin(k\pi x_{j+1}) + \sin(k\pi x_{j-1}) = 2\cos(k\pi\Delta x)\sin(k\pi x_j)$ gives $T v^{(k)} = (2\cos(k\pi\Delta x) - 2)v^{(k)} = -4\sin^2(k\pi\Delta x/2)v^{(k)}$, and the boundary entries vanish because $\sin(0) = \sin(k\pi) = 0$. The $J-1$ vectors are orthogonal, and $A$ is symmetric, so its $2$-norm is its spectral radius. For $r \le \tfrac12$, $0 \le 4r\sin^2 \le 2$ gives $-1 \le g_k \le 1$. The limit for $k = J-1$ follows from $\sin((J-1)\pi/(2J)) = \cos(\pi/(2J))$. $\blacksquare$
