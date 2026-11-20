---
title: Self-consistency, the Hellmann-Feynman forces and energy conservation for the toy model
proves: [correctness]
status: full
---

The toy model has $N$ atoms at positions $x_1, \dots, x_N$ on a line, distances $r_{ij} = |x_i - x_j| > 0$, the symmetric matrix $H_0(X)$ with $(H_0)_{ii} = 0$ and $(H_0)_{ij} = t(r_{ij}) = -t_0 e^{-a(r_{ij} - d_0)}$, and the energy
$$E(X, c) = 2 c^T H_0(X) c + U \sum_i c_i^4 + \Phi(X), \qquad \Phi(X) = \sum_{i < j} A e^{-b(r_{ij} - d_0)},$$
for $c$ on the unit sphere $S = \{c \in \mathbb R^N : |c| = 1\}$. Let $H(c) = H_0 + U\,\mathrm{diag}(c_1^2, \dots, c_N^2)$.

**Claim 1 (SCF fixed points are stationary points).** For fixed $X$, $c \in S$ is a stationary point of $E(X, \cdot)$ on $S$ if and only if $H(c)\, c = \epsilon\, c$ for some $\epsilon$. In particular, a fixed point of the SCF map (take an eigenvector of $H(c)$) is a stationary point.

*Proof.* $\nabla_c E = 4 H_0 c + 4 U (c_1^3, \dots, c_N^3)^T = 4 H(c)\, c$. By the Lagrange multiplier rule, $c$ is stationary on $S$ if and only if $\nabla_c E = 2\mu c$ for some $\mu$, that is $H(c)\, c = (\mu / 2)\, c$. $\square$

$E(X, \cdot)$ is continuous on the compact set $S$, so it has a minimizer, which is a stationary point by Claim 1. The code takes the lowest eigenvector of $H$ at each SCF iteration; when the iteration converges, its limit is a stationary point. This note does not prove that it is the global minimizer or that the iteration converges; the iteration counts on the page are measurements.

**Claim 2 (Hellmann-Feynman forces).** Suppose that near $X$ there is a continuously differentiable map $X \mapsto c(X) \in S$ of stationary points (for example, by the implicit function theorem, when the stationary point is nondegenerate on $S$). Then for $E_{\text{BO}}(X) = E(X, c(X))$,
$$\frac{\partial E_{\text{BO}}}{\partial x_k} = \frac{\partial E}{\partial x_k}(X, c) = 2 c^T \frac{\partial H_0}{\partial x_k} c + \frac{\partial \Phi}{\partial x_k}.$$
For the toy model this is
$$\frac{\partial E_{\text{BO}}}{\partial x_k} = \sum_{j \ne k} \mathrm{sgn}(x_k - x_j) \bigl(4 c_k c_j\, a t_0 e^{-a(r_{kj} - d_0)} - b A e^{-b(r_{kj} - d_0)}\bigr),$$
which is minus the force computed by the code.

*Proof.* By the chain rule, $\partial_{x_k} E_{\text{BO}} = \partial_{x_k} E + \nabla_c E \cdot \partial_{x_k} c$. By Claim 1, $\nabla_c E = 2 \mu c$. Since $|c(X)|^2 = 1$ for all $X$, differentiating gives $c \cdot \partial_{x_k} c = 0$. So the second term is 0. The $U$ term does not depend on $X$. In $2 c^T H_0 c = 2 \sum_{i \ne j} c_i c_j t(r_{ij})$, each pair $\{i, j\}$ appears twice, so it contributes $4 c_i c_j t(r_{ij})$. With $t'(r) = a t_0 e^{-a(r - d_0)}$, $\partial r_{kj} / \partial x_k = \mathrm{sgn}(x_k - x_j)$ and $\frac{d}{dr} A e^{-b(r - d_0)} = -b A e^{-b(r - d_0)}$, the formula follows. $\square$

The sign of $c$ is not fixed by the eigensolver, but $E$ and the force depend only on products $c_i c_j$, which do not change under $c \to -c$.

**Claim 3 (energy errors are second order, force errors first order).** Let $c^*$ be a stationary point and $c \in S$ with $|c - c^*| = \delta$. Then $E(X, c) - E(X, c^*) = O(\delta^2)$ and $\partial_{x_k} E(X, c) - \partial_{x_k} E(X, c^*) = O(\delta)$, with constants that depend on $X$ only.

*Proof.* Let $\mathcal L(c) = E(X, c) - \mu (|c|^2 - 1)$ with the multiplier $\mu$ of $c^*$. Then $\nabla \mathcal L(c^*) = 0$ and $\mathcal L$ is a polynomial, so Taylor's theorem gives $\mathcal L(c) - \mathcal L(c^*) = O(\delta^2)$. On $S$, $\mathcal L = E$. The partial derivative $\partial_{x_k} E(X, c)$ is a quadratic polynomial in $c$, hence Lipschitz on $S$, which gives the second bound. $\square$

This is why an incomplete SCF gives a good energy but forces that are not its gradient: the force error is first order in the SCF error, and in general it does not vanish to that order. Such forces do not come from any potential, so the total energy is no longer conserved, which is the drift measured on the page.

**Claim 4 (the dynamics).** Let $X(t)$ solve $M_k \ddot x_k = -\partial E_{\text{BO}} / \partial x_k$ with $E_{\text{BO}}$ continuously differentiable. Then $\mathcal H = \frac12 \sum_k M_k \dot x_k^2 + E_{\text{BO}}(X)$ is constant in time.

*Proof.* $d\mathcal H / dt = \sum_k M_k \dot x_k \ddot x_k + \sum_k \partial_{x_k} E_{\text{BO}}\, \dot x_k = \sum_k \dot x_k (M_k \ddot x_k + \partial_{x_k} E_{\text{BO}}) = 0$. $\square$

Lines L4, L5 and L8 are velocity Verlet for this system, which is symplectic, time reversible and second order (see [Verlet integration](/verlet-integration/) and [symplectic integrators](/symplectic-integrators/)). For a smooth potential and a small enough step, its energy error stays bounded and of order $h^2$ over long times, through the [shadow Hamiltonian](/shadow-hamiltonian/). This matches the measured spread on the page, which falls by about 4 when $h$ halves. The guarantee needs exact forces of one fixed potential. With the SCF started from the previous step and stopped at a tolerance, the force map depends on the history, the method is no longer exactly symplectic or reversible, and the energy can drift.

**Claim 5 (the dimer).** For $N = 2$ and $U = 0$, $E_{\text{BO}}(r) = -2 t_0 e^{-a(r - d_0)} + A e^{-b(r - d_0)}$. With $t_0 = a = d_0 = A = 1$ and $b = 2$, the minimum is $E_{\text{BO}}(1) = -1$ and $E_{\text{BO}}''(1) = 2$.

*Proof.* $H = H_0 = \begin{pmatrix} 0 & t \\ t & 0 \end{pmatrix}$ has eigenvalues $\pm t$, and the minimum of $2 c^T H_0 c$ on $S$ is twice the lowest eigenvalue, $-2|t(r)| = -2 t_0 e^{-a(r - d_0)}$. Add $\Phi$. With the given constants, $E(r) = -2 e^{-(r - 1)} + e^{-2(r - 1)}$, $E'(r) = 2 e^{-(r - 1)} - 2 e^{-2(r - 1)}$ vanishes at $r = 1$, and $E''(1) = -2 + 4 = 2$. $\square$
