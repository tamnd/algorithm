---
title: Convergence and rounding error of the Jacobi method
proves: [correctness, termination]
status: full
---

Notation of the page: $A = D + L + U$ with $a_{ii} \ne 0$, $G = G_J = -D^{-1}(L + U) = I - D^{-1} A$, $c = D^{-1} b$, $q = \|G\|_\infty$. Line L8 of the pseudocode computes $x_{k+1} = G x_k + c$, since $(b_i - s_i)/a_{ii} = c_i + (G x_k)_i$.

**Lemma 1 (fixed point).** $A x = b$ if and only if $x = G x + c$.

*Proof.* $x = G x + c \iff D x = -(L + U) x + b \iff (D + L + U) x = b$. $\square$

**Theorem 1 (error recursion).** If $A x = b$ then $e_k = x - x_k$ satisfies $e_k = G^k e_0$.

*Proof.* Subtract $x_{k+1} = G x_k + c$ from $x = G x + c$: $e_{k+1} = G e_k$. Induct on $k$. $\square$

**Theorem 2 (convergence criterion).** $x_k \to x$ for every $x_0$ if and only if $\rho(G) < 1$.

*Proof.* By Theorem 1, convergence for every $x_0$ means $G^k v \to 0$ for every $v$, that is $G^k \to 0$. If $\rho(G) < 1$, then for any $\delta > 0$ there is a norm with $\|G\| \le \rho(G) + \delta$ (Horn and Johnson, Lemma 5.6.10); with $\delta = (1 - \rho(G))/2$ this gives $\|G^k\| \le \|G\|^k \to 0$. If $\rho(G) \ge 1$, take an eigenpair $G v = \lambda v$ with $|\lambda| \ge 1$ and $v \ne 0$. If $\lambda$ is real, $v$ can be taken real, and $e_0 = v$ gives $\|e_k\| = |\lambda|^k \|v\| \not\to 0$. If $\lambda$ is not real, $v = v_1 + i v_2$ with $v_1, v_2$ real, and $G^k v_1, G^k v_2$ cannot both tend to $0$, since then $G^k v = \lambda^k v$ would too. $\square$

**Theorem 3 (diagonal dominance).** If $\sum_{j \ne i} |a_{ij}| < |a_{ii}|$ for every $i$, then $q < 1$ and $\|e_k\|_\infty \le q^k \|e_0\|_\infty$. In particular $A$ is nonsingular and $x_k \to x$.

*Proof.* $\|G\|_\infty = \max_i \sum_{j \ne i} |a_{ij}| / |a_{ii}| < 1$. If $A v = 0$, Lemma 1 with $b = 0$ gives $v = G v$, so $\|v\|_\infty \le q \|v\|_\infty$ and $v = 0$. Theorem 1 then gives $\|e_k\|_\infty \le \|G\|_\infty^k \|e_0\|_\infty$. $\square$

**Theorem 4 (rounding).** Assume the [floating point model](/floating-point-model/) $\mathrm{fl}(a \circ b) = (a \circ b)(1 + \delta)$ with $|\delta| \le u$, with no underflow or overflow, and $m u < 1$ for $m = n + 1$. Let $A$ be strictly row diagonally dominant, $A x = b$, and suppose $p = q (1 + \gamma_{n+1}) < 1$. Let $\hat x_k$ be the iterates that the pseudocode computes in floating point, with $s_i$ summed in any order. Then for all $k \ge 0$
$$\|x - \hat x_k\|_\infty \le p^k \|x - \hat x_0\|_\infty + \frac{\gamma_{n+1}(1 + 2q)}{1 - p} \|x\|_\infty .$$

*Proof.* Fix $k$ and $i$, and write $y = \hat x_k$. Line L3 computes $\hat s_i = \sum_{j \ne i} a_{ij} y_j (1 + \theta_j)$, where $1 + \theta_j$ is a product of at most $n - 1$ factors $(1 + \delta)^{\pm 1}$: one for the multiplication and at most $n - 2$ for the additions. Line L8 then rounds a subtraction and a division, so
$$\hat x_{k+1, i} = \frac{b_i (1 + \eta_0) - \sum_{j \ne i} a_{ij} y_j (1 + \eta_j)}{a_{ii}},$$
where each $1 + \eta_j$ is a product of at most $n + 1$ factors $(1 + \delta)^{\pm 1}$. By Higham, Lemma 3.1, $|\eta_j| \le \gamma_{n+1}$. Hence $\hat x_{k+1} = G y + c + \xi_k$ with
$$|\xi_{k,i}| \le \gamma_{n+1} \Bigl( |c_i| + \sum_{j \ne i} \frac{|a_{ij}|}{|a_{ii}|} |y_j| \Bigr), \qquad \|\xi_k\|_\infty \le \gamma_{n+1} \bigl( \|c\|_\infty + q \|y\|_\infty \bigr).$$
Since $x = G x + c$, the error $\hat e_k = x - \hat x_k$ satisfies $\hat e_{k+1} = G \hat e_k - \xi_k$. Also $c = (I - G) x$ gives $\|c\|_\infty \le (1 + q) \|x\|_\infty$, and $\|y\|_\infty \le \|x\|_\infty + \|\hat e_k\|_\infty$. So
$$\|\hat e_{k+1}\|_\infty \le q \|\hat e_k\|_\infty + \gamma_{n+1} \bigl( (1 + q) \|x\|_\infty + q \|x\|_\infty + q \|\hat e_k\|_\infty \bigr) = p \|\hat e_k\|_\infty + \beta,$$
with $\beta = \gamma_{n+1} (1 + 2q) \|x\|_\infty$. By induction, $\|\hat e_k\|_\infty \le p^k \|\hat e_0\|_\infty + \beta (1 + p + \cdots + p^{k-1}) \le p^k \|\hat e_0\|_\infty + \beta / (1 - p)$. $\square$

**Theorem 5 (termination and output).** The pseudocode stops after at most $k_{\max} + 1$ executions of lines L2 to L4 and $k_{\max}$ sweeps. If it returns CONVERGED, then the vector $r$ that it computed for the returned $x$ in line L4 satisfies $\|r\|_\infty \le \text{tol} \cdot \|b\|_\infty$.

*Proof.* The outer loop runs over $k = 0, \ldots, k_{\max}$, and line L6 returns at $k = k_{\max}$ at the latest. Line L5 is the only place that returns CONVERGED, and it tests exactly this inequality for the current $x$, which lines L2 to L4 used. Line L8 changes $x$ only after the test. $\square$

$\blacksquare$
