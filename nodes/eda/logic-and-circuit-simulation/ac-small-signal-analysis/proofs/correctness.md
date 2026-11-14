---
title: AC analysis gives the exact sinusoidal steady state of the linearized circuit
proves: [correctness]
status: full
---

We use the notation of the page. The circuit is $f(x) + \frac{d}{dt} q(x) = u(t)$ in MNA form, $x_0$ is a DC operating point ($f(x_0) = u_0$), and $G = \partial f/\partial x(x_0)$, $C = \partial q/\partial x(x_0)$ are the real $N \times N$ matrices of the small-signal model. The AC sources are the complex vector $b$: entry $k$ of $b$ is the phasor $A e^{j\phi}$ of the source in row $k$, meaning the time signal $\operatorname{Re}(A e^{j\phi} e^{j\omega t}) = A\cos(\omega t + \phi)$. AC analysis computes $X(\omega) = (G + j\omega C)^{-1} b$ and an output $H(j\omega) = \ell^{\mathsf T} X(\omega)$.

**The linearized circuit.** If the sources are $u_0 + \varepsilon\, \beta(t)$ and the solution $x(t, \varepsilon)$ that starts at $x_0$ is differentiable in $\varepsilon$, then $y = \partial x/\partial \varepsilon$ at $\varepsilon = 0$ satisfies

$$G y + C \dot y = \beta(t), \qquad y(0) = 0. \tag{1}$$

*Derivation.* Differentiate $f(x) + \frac{d}{dt} q(x) = u_0 + \varepsilon \beta$ in $\varepsilon$: $\frac{\partial f}{\partial x}(x)\, y + \frac{d}{dt}\big(\frac{\partial q}{\partial x}(x)\, y\big) = \beta$, and at $\varepsilon = 0$ the solution is the constant $x_0$, so the Jacobians are the constants $G$ and $C$. $\square$

So $x(t, \varepsilon) = x_0 + \varepsilon y(t) + O(\varepsilon^2)$ on a bounded time interval: (1) is the small-signal model. Differentiability in $\varepsilon$ holds for smooth $f$ and $q$ and an index-1 DAE by the standard dependence of solutions on parameters (see the DAE texts cited on the page); it is assumed here. Everything below is exact for (1).

**Theorem 1 (the phasor solution).** If $Y = G + j\omega C$ is nonsingular and $YX = b$, then $x_p(t) = \operatorname{Re}(X e^{j\omega t})$ solves

$$G x + C \dot x = \operatorname{Re}(b\, e^{j\omega t}) \tag{2}$$

for all $t$, and it is the only solution of the form $\operatorname{Re}(Z e^{j\omega t})$ with a constant complex vector $Z$.

*Proof.* $G$ and $C$ are real, so $\operatorname{Re}$ commutes with them, and $\frac{d}{dt} \operatorname{Re}(X e^{j\omega t}) = \operatorname{Re}(j\omega X e^{j\omega t})$. So

$$G x_p + C \dot x_p = \operatorname{Re}\big((G + j\omega C) X e^{j\omega t}\big) = \operatorname{Re}(b\, e^{j\omega t}).$$

For uniqueness, suppose $\operatorname{Re}(Z e^{j\omega t})$ solves (2), and let $W = Y Z - b$. Then $\operatorname{Re}(W e^{j\omega t}) = 0$ for all $t$. At $t = 0$ this gives $\operatorname{Re} W = 0$, and at $\omega t = \pi/2$ (if $\omega > 0$) it gives $\operatorname{Re}(jW) = -\operatorname{Im} W = 0$, so $W = 0$ and $Z = Y^{-1} b = X$. For $\omega = 0$ the form is the constant $\operatorname{Re} Z$, and only $\operatorname{Re} Z$ is determined; it equals $G^{-1} \operatorname{Re} b$. $\square$

By linearity, several sources at the same frequency with phasors $b_1, b_2, \ldots$ give $X = Y^{-1}(b_1 + b_2 + \cdots)$, and the transfer function from one source to the output is $\ell^{\mathsf T} Y^{-1} b_k$.

**Theorem 2 (it is the steady state).** Suppose the pencil is regular, $\det(G + sC) \not\equiv 0$, and every root $s$ of $\det(G + sC) = 0$ has $\operatorname{Re} s < 0$. Then $G + j\omega C$ is nonsingular for every real $\omega$, and every solution of (2) with consistent initial values tends to $x_p$ as $t \to \infty$.

*Proof.* The roots of $\det(G + sC)$ are not on the imaginary axis, so $Y$ is nonsingular. The difference $d = x - x_p$ solves $G d + C \dot d = 0$. For a regular pencil there are nonsingular $P$, $Q$ (the Weierstrass canonical form; see Brenan, Campbell and Petzold, Chapter 2) with

$$P C Q = \begin{pmatrix} I & 0 \\ 0 & M \end{pmatrix}, \qquad P G Q = \begin{pmatrix} J & 0 \\ 0 & I \end{pmatrix},$$

where $M$ is nilpotent, $M^\nu = 0$. With $d = Q (w_1, w_2)$, the system splits into $\dot w_1 + J w_1 = 0$ and $M \dot w_2 + w_2 = 0$. The second gives $w_2 = -M \dot w_2 = M^2 \ddot w_2 = \cdots = (-M)^\nu w_2^{(\nu)} = 0$. The first gives $w_1(t) = e^{-Jt} w_1(0)$, and $\det(G + sC) = \det(P)^{-1} \det(Q)^{-1} \det(J + sI) \det(I + sM)$ with $\det(I + sM) = 1$, so the eigenvalues of $-J$ are exactly the roots $s$, all with negative real part, and $w_1 \to 0$. $\square$

The roots of $\det(G + sC)$ are the natural frequencies (poles) of the linearized circuit. A passive circuit of positive resistors, capacitors and inductors has no roots in the open right half plane, but a lossless LC loop puts roots on the imaginary axis, where $Y$ is singular at the resonance. An amplifier with feedback may have roots in the right half plane; AC analysis then still returns $X$ (Theorem 1), but the sinusoidal response is not what a transient simulation settles to.

**Theorem 3 (the transfer function).** For the Laplace transforms of (1) with $y(0) = 0$ and $\beta(t) = b\, v(t)$ for a scalar input $v$, the output is $\ell^{\mathsf T} \hat y(s) = H(s) \hat v(s)$ with $H(s) = \ell^{\mathsf T} (G + sC)^{-1} b$, and AC analysis evaluates $H$ on the imaginary axis, $s = j\omega$.

*Proof.* The transform of $C\dot y$ is $sC\hat y - C y(0) = sC\hat y$, so $(G + sC)\hat y = b\, \hat v$, and $H(s)$ is defined wherever $G + sC$ is nonsingular. $\square$

**Theorem 4 (zero frequency).** If $G$ is nonsingular, $H(0) = \ell^{\mathsf T} G^{-1} b$ is the derivative of the DC output $\ell^{\mathsf T} x_{\mathrm{DC}}(\sigma)$ with respect to $\sigma$, where $x_{\mathrm{DC}}(\sigma)$ is the operating point for the DC sources $u_0 + \sigma b$ (real $b$).

*Proof.* The operating point solves $f(x) = u_0 + \sigma b$. Its Jacobian in $x$ at $\sigma = 0$ is $G$, which is nonsingular, so by the implicit function theorem $x_{\mathrm{DC}}$ is differentiable near $\sigma = 0$ with $G\, x_{\mathrm{DC}}'(0) = b$. $\square$

**Summary.** AC analysis is exact for the linearized circuit (1): Theorem 1 gives the unique sinusoidal solution, Theorem 2 shows it is the steady state when the linearized circuit is stable, and Theorem 3 identifies it with the transfer function. The approximation is in (1) itself, the first-order term in the amplitude $\varepsilon$; the test on the page measures that the fundamental of a transient simulation of the nonlinear circuit departs from the AC result by an amount that grows like $\varepsilon^2$.
