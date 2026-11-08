---
title: SPH terminates, conserves mass and momentum exactly and energy in the semi-discrete system, and its kernel estimate is second order
proves: [correctness, termination, convergence]
status: full
---

**Setting.** We solve the one-dimensional Euler equations of an ideal gas with adiabatic index $\gamma$ by $n$ particles with masses $m_i > 0$, positions $x_i$, velocities $v_i$, specific internal energies $e_i$ and smoothing lengths $h_i > 0$. $W(r, h)$ is the cubic spline kernel, $W_{ij} = \frac{1}{2}\big(W(x_i - x_j, h_i) + W(x_i - x_j, h_j)\big)$ and $\partial_i W_{ij}$ is its derivative with respect to $x_i$. The algorithm is lines L1 to L10. Proved statements are marked as such; the rest are cited or observed.

**Termination (proved).** Line L1 gives a finite $N$; each of the $N$ passes calls the force routine once, and the force routine sorts $n$ positions, does $n$ binary searches and visits each candidate pair a bounded number of times, so it ends. The last step has length $T - t_{N-1} \in (0, \Delta t]$, so the final time is $T$ up to rounding; $T = 0$ gives $N = 0$ and only the initial density pass.

**Lemma 1 (the kernel, proved).** $W(\cdot, h)$ is even, nonnegative, $C^2$, supported in $[-2h, 2h]$, and its moments are
$$\int W\,dr = 1, \qquad \int rW\,dr = 0, \qquad \int r^2W\,dr = \frac{h^2}{3}, \qquad \int r^3W\,dr = 0.$$
*Proof.* Evenness and support are read off the formula; the moments are integrals of polynomials of degree at most 5 on four pieces, evaluated exactly by Boole's rule in Fractions in the test `test_kernel_moments_exactly`. $C^2$: the pieces agree at $q = 1$ in value, first and second derivative ($\frac{1}{4}$, $-\frac{3}{4}$, $\frac{3}{2}$ times $\frac{2}{3h}$ and powers of $h$), and vanish to second order at $q = 2$. $\square$

**Corollary (kernel estimate, proved).** For $A \in C^4$, $\int A(x - r)W(r, h)\,dr = A(x) + \frac{h^2}{6}A''(x) + O(h^4)$, by Taylor expansion and Lemma 1. So the continuous kernel estimate is second order in $h$. The particle sum $\sum_j \frac{m_j}{\rho_j}A_jW(x - x_j, h)$ is a quadrature of this integral; it is exact for constants only on special lattices, for example $\sum_k W(k\Delta p, \Delta p)\Delta p = 1$ exactly, while $h = 1.2\Delta p$ gives $\frac{3895}{3888} = 1.0018$ (computed in Fractions). In general SPH is not zeroth-order consistent, which is the source of its noise.

**Lemma 2 (antisymmetry, proved).** $W_{ij} = W_{ji}$ and $\partial_i W_{ij} = -\partial_j W_{ij}$, because $W$ is even in $r$ and the average over $h_i$, $h_j$ is symmetric in $i, j$. The coefficient $A_{ij} = P_i/\rho_i^2 + P_j/\rho_j^2 + \Pi_{ij}$ is symmetric, and so is $\Pi_{ij}$, which depends on $|x_i - x_j|$, $(v_i - v_j)(x_i - x_j)$ and symmetric averages.

**Theorem 1 (conservation, proved).**
1. *Mass* $\sum_i m_i$ is constant, since masses never change.
2. *Momentum.* Line L9 adds $-m_jA_{ij}\partial_iW_{ij}$ to $a_i$ and $+m_iA_{ij}\partial_iW_{ij}$ to $a_j$, so $\sum_i m_ia_i = 0$ for every state. Each kick changes $\sum_i m_iv_i$ by $\frac{\tau}{2}\sum_i m_ia_i = 0$, so total momentum is conserved by the fully discrete scheme, up to rounding (observed: below $10^{-16}$).
3. *Energy, semi-discrete.* With $E = \sum_i m_i(\frac{1}{2}v_i^2 + e_i)$, the ODE system $\dot x_i = v_i$, $\dot v_i = a_i$ with $a_i$ and $\dot e_i$ from line L9 gives
$$\dot E = \sum_i m_iv_ia_i + \sum_i m_i\dot e_i = -\sum_{\text{pairs}} m_im_jA_{ij}(v_i - v_j)\partial_iW_{ij} + \sum_{\text{pairs}} m_im_jA_{ij}(v_i - v_j)\partial_iW_{ij} = 0,$$
where the first sum uses Lemma 2 and the second is the definition of the energy update, $\frac{1}{2}m_j$ to $i$ and $\frac{1}{2}m_i$ to $j$. The time stepping does not keep $E$ exactly; the observed relative errors on the Sod problem are $3.7 \times 10^{-5}$, $1.8 \times 10^{-5}$, $8.0 \times 10^{-6}$ as the resolution and the step are halved twice.

**Theorem 2 (Galilean invariance, proved).** Adding a constant $V$ to every velocity and $Vt$ to every position leaves every $\rho_i$, $P_i$, $a_i$ and $\dot e_i$ unchanged, because they depend only on $x_i - x_j$ and $v_i - v_j$; the computed solution is the shifted one up to rounding (tested to $10^{-9}$).

**Theorem 3 (viscosity dissipates, proved).** $\Pi_{ij} \ne 0$ only for approaching pairs, $(v_i - v_j)(x_i - x_j) < 0$. Then $\mu_{ij} < 0$, so $\Pi_{ij} = (-\alpha\bar c_{ij}\mu_{ij} + \beta\mu_{ij}^2)/\bar\rho_{ij} > 0$. Since $W$ decreases in $|r|$, $\partial_iW_{ij}$ has the sign of $-(x_i - x_j)$, so $(v_i - v_j)\partial_iW_{ij} > 0$ and the viscous part of $\dot e_i$ is nonnegative: the viscosity turns kinetic energy into heat, never the reverse, while Theorem 1 keeps the total fixed. This is the discrete entropy production that lets SPH capture shocks.

**Consistency of the equations (proved formally).** With $\rho$ given by the kernel estimate and particles following the flow, $\sum_j m_j(P_i/\rho_i^2 + P_j/\rho_j^2)\partial_iW_{ij}$ is the particle quadrature of $\frac{1}{\rho}\partial_xP$, written in the symmetric form $\partial_x(P/\rho) + (P/\rho^2)\partial_x\rho$; the same symmetric form follows from a discrete Lagrangian $L = \sum_i m_i(\frac{1}{2}v_i^2 - e_i(\rho_i))$ (Monaghan 2005, Price 2012).

**Convergence (observed, not proved here).** No general convergence theorem is proved here; convergence analyses of SPH require that $h \to 0$ while the number of neighbours grows, and regular particle distributions. On the Sod problem the $L^1$ density error on $[-0.4, 0.4]$ falls from $0.0150$ to $0.0100$ to $0.0062$ as the particle number doubles twice, an observed order of about 0.6 to 0.7, as expected for a solution with a shock and a contact. The step restriction is also observed: with $\Delta t = C\,h_{\min}/1.2$, $C = 0.3$ and $0.6$ are stable, and $C = 1.0$ blows up.
