---
title: The cosine coefficients reproduce the density, the cosine series solves Poisson's equation with a zero normal derivative, and the field is minus its gradient
proves: [correctness, termination, running time]
status: full
---

Let $M \ge 1$, let $\rho$ be an $M \times M$ array, and write $\omega_u = \pi u / M$, $C_u(t) = \cos(\omega_u t)$ and $S_u(t) = \sin(\omega_u t)$. Bin $x$ has its center at $t = x + \frac12$. Line L5 computes

$$ a_{uv} = c_u c_v \sum_{x, y} \rho_{xy} \, C_u(x + \tfrac12) \, C_v(y + \tfrac12), \qquad c_0 = \tfrac1M, \; c_u = \tfrac2M \; (u \ge 1). $$

**Lemma 1 (orthogonality at the bin centers).** For $0 \le u, u' \le M - 1$,

$$ \sum_{x=0}^{M-1} C_u(x + \tfrac12) \, C_{u'}(x + \tfrac12) = \begin{cases} M & u = u' = 0, \\ M / 2 & u = u' \ge 1, \\ 0 & u \ne u'. \end{cases} $$

*Proof.* Write $\theta_k = \pi k / (2M)$ and $s_k = \sum_{x=0}^{M-1} \cos\bigl((2x + 1) \theta_k\bigr)$. Then $s_0 = M$. For $0 < |k| < 2M$, $s_k$ is the real part of $\sum_x e^{i (2x+1) \theta_k} = e^{i \theta_k} \frac{1 - e^{i \pi k}}{1 - e^{2 i \theta_k}}$, where the denominator is not 0. If $k$ is even, $e^{i \pi k} = 1$ and the sum is 0. If $k$ is odd, the sum is $\frac{2 e^{i \theta_k}}{1 - e^{2 i \theta_k}} = \frac{2}{e^{-i \theta_k} - e^{i \theta_k}} = \frac{i}{\sin \theta_k}$, which has real part 0. So $s_k = 0$ for $0 < |k| < 2M$. By the product formula, the sum of the lemma is $\frac12 (s_{u + u'} + s_{u - u'})$. Both indices lie in $(-2M, 2M)$. If $u = u' = 0$ both are 0, giving $M$. If $u = u' \ge 1$, the first is $2u \ne 0$ and the second 0, giving $M / 2$. If $u \ne u'$, both are nonzero, giving 0. $\square$

**Theorem 1 (the transform is exact).** For every bin, $\rho_{xy} = \sum_{u, v} a_{uv} C_u(x + \frac12) C_v(y + \frac12)$, and $a_{00}$ is the mean $\bar\rho$ of $\rho$.

*Proof.* The $M$ vectors $(C_u(x + \frac12))_{x}$ are pairwise orthogonal and nonzero by Lemma 1, so they are a basis of $\mathbb{R}^M$, and the products of two of them are a basis of the $M \times M$ arrays. Write $\rho = \sum b_{uv} C_u C_v$ in this basis. Taking the inner product with $C_u C_v$ and using Lemma 1 twice gives $\sum_{x, y} \rho_{xy} C_u C_v = b_{uv} \cdot \frac{1}{c_u} \cdot \frac{1}{c_v}$, so $b_{uv} = a_{uv}$. For $u = v = 0$, $a_{00} = \frac{1}{M^2} \sum_{x, y} \rho_{xy} = \bar\rho$. $\blacksquare$

**Theorem 2 (Poisson's equation and the field).** Let $\tilde\rho(t_x, t_y) = \sum_{u, v} a_{uv} C_u(t_x) C_v(t_y)$, the cosine interpolant of $\rho$; by Theorem 1 it equals $\rho$ at the bin centers. The function $\psi = \sum_{(u, v) \ne (0, 0)} \frac{a_{uv}}{\omega_u^2 + \omega_v^2} C_u C_v$ satisfies $-\nabla^2 \psi = \tilde\rho - \bar\rho$ on $[0, M]^2$, its normal derivative is 0 on the border, and its integral over the square is 0. The field of line L5 is $\xi = -\nabla \psi$ in length units.

*Proof.* For $(u, v) \ne (0, 0)$, $\omega_u^2 + \omega_v^2 > 0$, so every term is defined. $\nabla^2 (C_u(t_x) C_v(t_y)) = -(\omega_u^2 + \omega_v^2) C_u C_v$, so $-\nabla^2 \psi = \sum_{(u, v) \ne (0, 0)} a_{uv} C_u C_v = \tilde\rho - a_{00} = \tilde\rho - \bar\rho$ by Theorem 1. The derivative of $C_u(t_x)$ is $-\omega_u S_u(t_x)$, which is 0 at $t_x = 0$ and at $t_x = M$, because $\omega_u M = \pi u$. So $\partial \psi / \partial t_x = 0$ on the vertical sides, and in the same way $\partial \psi / \partial t_y = 0$ on the horizontal sides. Each term with $(u, v) \ne (0, 0)$ has one factor $C_u$ with $u \ge 1$ or $C_v$ with $v \ge 1$, whose integral over $[0, M]$ is $\sin(\pi u) / \omega_u = 0$, so $\int \psi = 0$. Finally $-\partial \psi / \partial t_x = \sum \frac{a_{uv} \omega_u}{\omega_u^2 + \omega_v^2} S_u C_v$, and $t_x = x / B$ gives the factor $\frac1B$ in $\xi_x = -\partial \psi / \partial x$; the same holds for $\xi_y$. $\blacksquare$

A uniform $\rho$ has $a_{uv} = 0$ for $(u, v) \ne (0, 0)$ by Theorem 1 and Lemma 1, so $\psi = 0$ and $\xi = 0$: a spread placement feels no density force.

**Theorem 3 (termination and running time).** The loop of lines L3 to L11 runs at most the given number $k$ of times. One iteration costs $O(P + n + M^2 \log M)$ time with FFT-based transforms, and $O(P + n + M^3)$ with the separable direct sums of the implementation, if no cell overlaps more than a constant number of bins.

*Proof.* The implementation stops at the iteration limit even if $\tau$ stays above $\tau^*$. The value and gradient of $W_\gamma$ visit each pin a constant number of times, $O(P)$. Line L4 clears $M^2$ bins and adds each cell to $O(1)$ bins. A separable direct transform does $M$ sums of length $M$ for each of $M^2$ outputs, twice, so $O(M^3)$; a DCT or DST of length $M$ by the FFT costs $O(M \log M)$, and $2M$ of them cost $O(M^2 \log M)$. Lines L6 to L10 do $O(1)$ work per cell, and $\tau$ costs $O(M^2)$. $\blacksquare$
