---
title: Factored form, l2 stability, convergence and conservation of the Peaceman-Rachford ADI scheme
proves: [correctness]
status: full
---

**Setting.** $u_t = \kappa(u_{xx} + u_{yy})$ on $[0, \ell_x] \times [0, \ell_y]$, $\kappa > 0$, with $u = 0$ on the boundary. The grid has $\Delta x = \ell_x/m_x$, $\Delta y = \ell_y/m_y$ and step $\Delta t$, with $r_x = \kappa\Delta t/\Delta x^2$ and $r_y = \kappa\Delta t/\Delta y^2$. Interior grid functions $V = (V_{ij})$, $1 \le i \le m_x - 1$, $1 \le j \le m_y - 1$, carry the norm $\|V\| = (\Delta x\Delta y\sum_{ij}V_{ij}^2)^{1/2}$, a multiple of the Euclidean norm. Let $D_x$ act on each row as $\operatorname{tridiag}(1, -2, 1)$ in $i$ with zero boundary values, and let $D_y$ act in the same way in $j$. Put $A = \tfrac{r_x}{2}D_x$ and $B = \tfrac{r_y}{2}D_y$. One step of the scheme is
$$(I - A)U^* = (I + B)U^n, \qquad (I - B)U^{n+1} = (I + A)U^*. \tag{1}$$

## Lemma 1 (the step is well defined and has a factored form)

$I - A$ and $I - B$ are invertible, and (1) holds if and only if
$$(I - A)(I - B)U^{n+1} = (I + A)(I + B)U^n. \tag{2}$$
This equals the 2D Crank-Nicolson step $(I - A - B)U^{n+1} = (I + A + B)U^n$ plus the extra term $AB(U^{n+1} - U^n)$ on the left.

*Proof.* $-D_x$ and $-D_y$ are symmetric positive definite (Lemma 2 below), so $I - A$ and $I - B$ are symmetric with eigenvalues at least 1. From (1), $U^*$ is unique, and $U^{n+1}$ is unique. Multiply the first equation of (1) by $I + A$ and use $(I + A)(I - A) = (I - A)(I + A)$, which holds because both are polynomials in $A$. This gives $(I - A)(I + A)U^* = (I + A)(I + B)U^n$. The second equation gives $(I + A)U^* = (I - B)U^{n+1}$, so (2) follows. Equation (2) has a unique solution, because $I - A$ and $I - B$ are invertible, so it is equivalent to (1). Expanding both sides of (2) gives the last claim. This argument does not need $A$ and $B$ to commute. $\square$

## Lemma 2 (common eigenvectors)

For $1 \le k \le m_x - 1$ and $1 \le l \le m_y - 1$, let $v^{(k,l)}_{ij} = \sin(k\pi i/m_x)\sin(l\pi j/m_y)$, $s_k = \sin^2(k\pi/(2m_x))$ and $\sigma_l = \sin^2(l\pi/(2m_y))$. Then $D_xv^{(k,l)} = -4s_kv^{(k,l)}$ and $D_yv^{(k,l)} = -4\sigma_lv^{(k,l)}$. The vectors $v^{(k,l)}$ are orthogonal and form a basis. So $A$ and $B$ are symmetric and commute.

*Proof.* In each row the factor $\sin(k\pi i/m_x)$ is an eigenvector of the 1D second difference with eigenvalue $-4s_k$, by $\sin(\phi(i - 1)) + \sin(\phi(i + 1)) = 2\cos\phi\sin(\phi i)$ and $2\cos\phi - 2 = -4\sin^2(\phi/2)$. It vanishes at $i = 0$ and $i = m_x$, so the boundary rows are correct. The same holds in $j$. Products of the two orthogonal 1D bases give an orthogonal basis of the $(m_x - 1)(m_y - 1)$-dimensional space. Two matrices that are diagonal in the same basis commute. $\square$

## Theorem 1 (amplification factor and unconditional $l^2$ stability)

The step (1) maps $v^{(k,l)}$ to $g_{kl}v^{(k,l)}$ with
$$g_{kl} = \frac{1 - 2r_xs_k}{1 + 2r_xs_k}\cdot\frac{1 - 2r_y\sigma_l}{1 + 2r_y\sigma_l}, \qquad |g_{kl}| < 1.$$
Hence the step matrix $G$ satisfies $\|GV\| \le \|V\|$ for every $V$ and every $\Delta t > 0$.

*Proof.* By (2) and Lemma 2, $G = (I - B)^{-1}(I - A)^{-1}(I + A)(I + B)$, and every factor is diagonal in the basis $v^{(k,l)}$ with the eigenvalues $1 \mp 2r_xs_k$ and $1 \mp 2r_y\sigma_l$. Since $0 < s_k < 1$ and $r_x > 0$, we have $|1 - 2r_xs_k| < 1 + 2r_xs_k$, and the same in $y$. $G$ is symmetric because it is a product of commuting symmetric matrices. So its 2-norm is $\max|g_{kl}| < 1$. $\square$

The tests check that after three steps a single mode equals $g_{kl}^3v^{(k,l)}$ to $10^{-13}$, and that the norm of random data never grows over ten steps with $r_x = r_y = 50$. The hand example on the page is $g_{11}$ with $m_x = m_y = 4$ and $r = 1$.

**Remark (slow damping).** As $r_x \to \infty$, the factor for $k = m_x - 1$ tends to $-1$, and the same holds in $y$. So $g_{m_x-1, m_y-1} \to +1$. Stability holds, but the roughest modes are hardly damped. This is the reason for the pitfall on the page.

## Lemma 3 (consistency)

Let $u$ be the exact solution, and let $u_{ttt}$, $u_{xxtt}$, $u_{yytt}$, $u_{xxxx}$, $u_{yyyy}$ and $u_{xxyyt}$ be continuous and bounded by $K$. Let $u^n$ be the restriction of $u(\cdot, \cdot, t_n)$ to the interior grid, and define $\tau^n$ by
$$(I - A)(I - B)u^{n+1} = (I + A)(I + B)u^n + \Delta t\,\tau^n.$$
Then $\|\tau^n\|_\infty \le K\big(\tfrac{1}{24}\Delta t^2 + \tfrac{\kappa}{4}\Delta t^2 + \tfrac{\kappa}{12}(\Delta x^2 + \Delta y^2) + \tfrac{\kappa^2}{4}\Delta t^2\big)$.

*Proof.* By Lemma 1, $\Delta t\,\tau^n = \Delta t\,\tau^n_{\mathrm{CN}} + AB(u^{n+1} - u^n)$, where $\tau^n_{\mathrm{CN}}$ is the truncation error of 2D Crank-Nicolson. The Crank-Nicolson part is bounded exactly as in the one-dimensional proof on the [Crank-Nicolson](/crank-nicolson-method/) page. The time difference gives $K\Delta t^2/24$. Each of the two space directions gives $K\kappa\Delta x^2/12$ or $K\kappa\Delta y^2/12$ from the second difference, and $K\kappa\Delta t^2/8$ from the trapezoidal average in time. For the extra term, write
$$AB(u^{n+1} - u^n) = \frac{\kappa^2\Delta t^3}{4}\cdot\frac{\delta_x^2\delta_y^2}{\Delta x^2\Delta y^2}\Big(\frac{u^{n+1} - u^n}{\Delta t}\Big).$$
For a function $h$ with continuous $h_{xxyy}$, the mean value theorem applied in $x$ and then in $y$ gives $\delta_x^2\delta_y^2h/(\Delta x^2\Delta y^2) = h_{xxyy}$ at some point. With $h = (u(\cdot, t_{n+1}) - u(\cdot, t_n))/\Delta t$, $h_{xxyy}$ is an average of $u_{xxyyt}$ over $[t_n, t_{n+1}]$, so it is bounded by $K$. Dividing by $\Delta t$ gives the last term. $\square$

So $\tau^n = O(\Delta t^2 + \Delta x^2 + \Delta y^2)$. The extra term of ADI does not lower the order of Crank-Nicolson.

## Theorem 2 (convergence in $l^2$)

Let $e^n = u^n - U^n$ on the interior grid. Then
$$\|e^n\| \le \|e^0\| + t_n\sqrt{\ell_x\ell_y}\,\max_{m < n}\|\tau^m\|_\infty.$$
With exact initial values the error is $O(\Delta t^2 + \Delta x^2 + \Delta y^2)$ in $l^2$, for any relation between $\Delta t$, $\Delta x$ and $\Delta y$.

*Proof.* Subtracting (2) from the definition of $\tau^n$ gives $(I - A)(I - B)e^{n+1} = (I + A)(I + B)e^n + \Delta t\,\tau^n$. So $e^{n+1} = Ge^n + \Delta t\,(I - B)^{-1}(I - A)^{-1}\tau^n$. The matrices $(I - A)^{-1}$ and $(I - B)^{-1}$ are symmetric with eigenvalues in $(0, 1]$, so they do not increase the norm. With Theorem 1, $\|e^{n+1}\| \le \|e^n\| + \Delta t\|\tau^n\|$. Also $\|\tau^n\| \le \sqrt{\ell_x\ell_y}\|\tau^n\|_\infty$, since the grid has fewer than $m_xm_y$ interior points and $\Delta x\Delta y\,m_xm_y = \ell_x\ell_y$. Sum over the steps. $\square$

The max-norm order 2 in the table on the page, for $\Delta t = \Delta x/5$, is observed, not proved here.

## Proposition (conservation with zero-flux boundaries)

For zero normal derivative, the ghost values are $U_{-1,j} = U_{1,j}$, $U_{m_x+1,j} = U_{m_x-1,j}$ and the same in $j$. All grid points $0 \le i \le m_x$, $0 \le j \le m_y$ are unknowns. Let $w_i = \tfrac12$ for $i \in \{0, m_x\}$ and $w_i = 1$ otherwise, and define $\omega_j$ in the same way for $j$. Then the trapezoidal total $H(U) = \Delta x\Delta y\sum_{ij}w_i\omega_jU_{ij}$ satisfies $H(U^*) = H(U^n)$ and $H(U^{n+1}) = H(U^*)$.

*Proof.* On one row, the zero-flux second difference $D_N$ satisfies $w^TD_N = 0$. This is the computation in the conservation proposition on the [Crank-Nicolson](/crank-nicolson-method/) page: each column of $D_N$ sums to 0 with the weights $\tfrac12, 1, \dots, 1, \tfrac12$. So $H(D_xV) = 0$ and $H(D_yV) = 0$ for every grid function $V$, because $H$ sums $w$-weighted rows with the weights $\omega_j$, and in the same way for columns. Apply $H$ to the first equation of (1): $H(U^*) - H(AU^*) = H(U^n) + H(BU^n)$, and the terms with $A$ and $B$ vanish. The second equation is the same. $\square$

The tests confirm the conservation to $10^{-13}$ for $r = 1$ and $r = 5$. With zero-flux boundaries, $WD_N$ is symmetric for $W = \operatorname{diag}(w)$. So $D_N$ is self-adjoint and negative semidefinite in the weighted inner product, and the argument of Theorem 1 gives stability in the weighted norm with factors in $[-1, 1]$. The constant mode has $g = 1$, as conservation requires.
