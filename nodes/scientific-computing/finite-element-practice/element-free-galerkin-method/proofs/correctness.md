---
title: MLS shape functions reproduce their basis, and EFG is exact for linear solutions under the integration constraint
proves: [correctness]
status: partial
---

**Setting.** Nodes $x_1, \ldots, x_n$ in $[a, b]$, weights $w_I \ge 0$ that are continuously differentiable with $w_I(x) > 0$ exactly when $|x - x_I| < d_I$, a basis $p(x) = (p_1(x), \ldots, p_m(x))$ of polynomials, $A(x) = \sum_I w_I(x)\,p(x_I)p(x_I)^\top$ and $\phi_I(x) = p(x)^\top A(x)^{-1} w_I(x)\,p(x_I)$. Let $U$ be the set of points where $A(x)$ is nonsingular. The status is partial because the convergence rates are cited from the literature and measured, not proved here (Remark 2).

**Lemma 1 (the MLS fit).** For $x \in U$ and any data $a_I$, the minimizer of $J(c) = \sum_I w_I(x)\,(p(x_I)^\top c - a_I)^2$ is unique, and $p(x)^\top c(x) = \sum_I \phi_I(x)\,a_I$.

*Proof.* $J$ is a convex quadratic in $c$ with Hessian $2A(x)$. If $A(x)$ is nonsingular it is positive definite, since $c^\top A c = \sum_I w_I (p(x_I)^\top c)^2 \ge 0$. So the unique minimizer solves $A(x)\,c = \sum_I w_I(x)\,p(x_I)\,a_I$, and $p(x)^\top c(x) = \sum_I p(x)^\top A^{-1} w_I\,p(x_I)\,a_I$. $\square$

**Theorem 1 (reproduction).** For $x \in U$ and every $q = p^\top \beta$ in the span of the basis, $\sum_I \phi_I(x)\,q(x_I) = q(x)$. On the open set $U$ the $\phi_I$ are continuously differentiable and $\sum_I \phi_I'(x)\,q(x_I) = q'(x)$.

*Proof.* Take $a_I = q(x_I) = p(x_I)^\top\beta$. Then $J(\beta) = 0$, which is the minimum, so $c(x) = \beta$ by uniqueness and the fit is $p(x)^\top\beta = q(x)$. The entries of $A(x)$ are continuously differentiable, and the inverse of a nonsingular matrix is a smooth function of its entries, so each $\phi_I$ is continuously differentiable on $U$. The identity $\sum_I \phi_I(x)\,q(x_I) = q(x)$ holds on the open set $U$, so its derivative holds too. $\square$

With $q = 1$ this gives $\sum_I \phi_I = 1$, a partition of unity, and $\sum_I \phi_I' = 0$. The formula for $\phi_I'$ on the page is the product rule with $(A^{-1})' = -A^{-1}A'A^{-1}$: with $\gamma = A^{-1}p$, $\gamma' = A^{-1}p' - A^{-1}A'A^{-1}p = A^{-1}(p' - A'\gamma)$, and $\phi_I = w_I\,\gamma^\top p(x_I)$.

**Theorem 2 (the constraints).** Any solution of the system of line L6 satisfies $u_h(a) = u_a$ and $u_h(b) = u_b$.

*Proof.* The last two rows of the system are $\sum_I G_{Ib}\,a_I = g_b$, and $G_{Ib} = \phi_I(x_b)$, so they read $u_h(x_b) = g_b$. $\square$

**Theorem 3 (linear exactness under the integration constraint).** Let the basis contain $1$ and $x$, let $[a, b] \subset U$, and let $f = 0$ and $u^*(x) = \alpha + c\,x$ with $u_a = u^*(a)$ and $u_b = u^*(b)$. Suppose the quadrature $Q$ of line L1 satisfies the integration constraint

$$Q[\phi_I'] = \sum_Q w_Q\,\phi_I'(x_Q) = \phi_I(b) - \phi_I(a) \quad \text{for every } I.$$

If the matrix of line L6 is nonsingular, its solution is $a_I = u^*(x_I)$ and $\lambda = (c, -c)$, and then $u_h = u^*$ on $[a, b]$.

*Proof.* Put $a^*_I = u^*(x_I)$ and $\lambda^* = (c, -c)$. By Theorem 1, $\sum_J \phi_J'(x)\,a^*_J = c$ for every $x$, so row $I$ of the first block is

$$\sum_J K_{IJ}\,a^*_J + \phi_I(a)\,c - \phi_I(b)\,c = \sum_Q w_Q\,\phi_I'(x_Q)\,c + c\,(\phi_I(a) - \phi_I(b)) = 0 = F_I,$$

by the integration constraint and $f = 0$. The last rows hold by Theorem 1: $\sum_I \phi_I(x_b)\,a^*_I = u^*(x_b) = g_b$. So $(a^*, \lambda^*)$ solves the system, and it is the only solution because the matrix is nonsingular. Finally $u_h(x) = \sum_I \phi_I(x)\,u^*(x_I) = u^*(x)$ by Theorem 1. $\square$

**Remark 1 (when the constraint holds).** The exact integral satisfies the constraint by the fundamental theorem of calculus, so the constraint asks the quadrature to integrate each $\phi_I'$ exactly. The $\phi_I$ are rational on each interval between breakpoints $x_I \pm d_I$ and $x_I \pm d_I/2$, so a Gauss rule on cells whose ends are these breakpoints converges very fast but is not exact. The reference test measures a patch test error of $6 \times 10^{-15}$ with 8 points on such cells, $4.9 \times 10^{-5}$ with 3 points on cells of one node interval, and $7.5 \times 10^{-3}$ with nodal integration, which violates the constraint. If the constraint fails, the same computation shows that the residual of $(a^*, \lambda^*)$ in row $I$ is $c\,(Q[\phi_I'] - \phi_I(b) + \phi_I(a))$, so the error is proportional to the defect of the constraint.

**Remark 2 (convergence, cited).** For exact integration and a quasi uniform node set with supports proportional to the spacing, the MLS approximation with a basis of degree $k$ has interpolation errors $O(h^{k+1})$ in $L^2$ and $O(h^k)$ in $H^1$, and the Galerkin method with multipliers inherits these rates when the multiplier space is stable. This is the standard result of the meshfree literature (Belytschko, Lu and Gu 1994, and Liu 2003). The reference tests measure the rates $2$ and $1$ for $k = 1$ and close to $3$ and $2$ for $k = 2$.
