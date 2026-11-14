---
title: A periodic steady state is a root of x(T) − x(0), and shooting Newton uses the monodromy matrix
proves: [correctness]
status: full
---

We use the notation of the page. The circuit is $f(x) + \frac{d}{dt} q(x) = u(t)$ with $N$ unknowns, $f$ and $q$ continuously differentiable with Jacobians $G(x)$ and $C(x)$, and $u(t + T) = u(t)$. The step is $h = T/S$, $t_k = kh$, $u_k = u(t_k)$, and $\theta = \tfrac12$ (trapezoidal rule) or $\theta = 1$ (backward Euler). One step from $x_k$ to $x_{k+1}$ solves

$$E_k(x_k, x_{k+1}) = q(x_{k+1}) - q(x_k) + h\big[\theta\,(f(x_{k+1}) - u_{k+1}) + (1 - \theta)(f(x_k) - u_k)\big] = 0. \tag{1}$$

Put $A_k = C(x_{k+1}) + \theta h\, G(x_{k+1})$ and $B_k = C(x_k) - (1 - \theta) h\, G(x_k)$, so that $\partial E_k/\partial x_{k+1} = A_k$ and $\partial E_k/\partial x_k = -B_k$. We assume that every $A_k$ met is nonsingular and that (1) has exactly one solution $x_{k+1}$ in the region where the iterates stay. Then (1) defines a step map $x_{k+1} = \psi_k(x_k)$, and by the implicit function theorem $\psi_k$ is continuously differentiable with $\psi_k'(x_k) = A_k^{-1} B_k$. The period map is $P = \psi_{S-1} \circ \cdots \circ \psi_0$.

## Fixed points are periodic steady states

**Theorem 1.** Let $x_0, x_1, x_2, \ldots$ solve (1) for every $k \ge 0$. The sequence is periodic with period $S$ (that is, $x_{k+S} = x_k$ for all $k$) if and only if $x_S = x_0$, that is, if and only if $x_0$ is a root of $r(x_0) = P(x_0) - x_0$.

*Proof.* If the sequence is $S$-periodic, then $x_S = x_0$. Conversely, $u_{k+S} = u(t_k + T) = u_k$, and $f$ and $q$ do not depend on time, so $E_{k+S} = E_k$ and $\psi_{k+S} = \psi_k$ for every $k$. Suppose $x_S = x_0$. By induction on $k$, if $x_{k+S} = x_k$ then $x_{k+1+S} = \psi_{k+S}(x_{k+S}) = \psi_k(x_k) = x_{k+1}$. $\square$

The same argument holds for the exact solution. If the initial value problem has a unique solution from every consistent state, the solution from $x(0)$ satisfies $x(t + T) = x(t)$ for all $t$ if and only if $x(T) = x(0)$, because $t \mapsto x(t + T)$ solves the same equation with the same value at $t = 0$. So the periodic steady state of the circuit is a root of $x(T) - x(0)$, and the discrete problem replaces $x(T)$ by $P(x_0)$.

## The Newton matrix is the monodromy matrix minus the identity

**Theorem 2.** Let $\Phi_0 = I$ and $\Phi_{k+1} = A_k^{-1} B_k \Phi_k$. Then $\Phi_S = P'(x_0)$, and the step of line L6, $(\Phi_S - I)\Delta = -r(x_0)$, is the Newton step for $r$.

*Proof.* By the chain rule, $\partial x_{k+1}/\partial x_0 = \psi_k'(x_k)\, \partial x_k/\partial x_0 = A_k^{-1} B_k\, \partial x_k / \partial x_0$, with $\partial x_0/\partial x_0 = I$. So $\partial x_k/\partial x_0 = \Phi_k$ for every $k$ by induction, and $r'(x_0) = \Phi_S - I$. $\square$

$\Phi_S$ is the monodromy matrix of the discrete map: it carries a small change of the state at $t = 0$ to its change one period later. The cost of $\Phi_S$ is small next to the transient itself, because $A_k$ is the matrix that the last Newton iteration of step $k$ has already factored.

**Corollary 1 (local convergence).** If $f$ and $q$ are twice continuously differentiable and $\Phi_S - I$ is nonsingular at a root $x^*$, then the full-step iteration converges quadratically from every start close enough to $x^*$. This is the local theorem for [Newton's method for systems](/newton-method-for-systems/) applied to $r$, whose derivative is Lipschitz near $x^*$ under these assumptions.

## Linear circuits

**Theorem 3.** Let $f(x) = Gx$ and $q(x) = Cx$ with constant matrices, and let $\Phi_S - I$ be nonsingular. Then:

1. $r$ is affine, so Newton reaches its unique root in one step from any start.
2. If $u(t) = \operatorname{Re}(U e^{j\omega t})$ with $\omega = 2\pi/T$, the discrete steady state is $x_k = \operatorname{Re}(X_d e^{j\omega t_k})$, where $(G + s_d C) X_d = U$ and, with $z = e^{j\omega h}$,

$$s_d = \frac{2}{h}\,\frac{z - 1}{z + 1} = j\,\frac{2}{h}\tan\frac{\omega h}{2} \quad (\theta = \tfrac12), \qquad s_d = \frac{1 - z^{-1}}{h} \quad (\theta = 1),$$

provided $G + s_d C$ and $G + \bar s_d C$ are nonsingular.

3. For the trapezoidal rule $s_d = j\omega\big(1 + \tfrac{(\omega h)^2}{12} + O(h^4)\big)$, so $X_d$ differs from the AC phasor $X = (G + j\omega C)^{-1} U$ by $O(h^2)$; for backward Euler $s_d - j\omega = O(h)$.

*Proof.* 1. Each $\psi_k$ is affine, $\psi_k(x) = A^{-1}(Bx + c_k)$ with constant $A$ and $B$, so $P$ and $r$ are affine and $r(x_0 + \Delta) = r(x_0) + (\Phi_S - I)\Delta$; the Newton step makes this zero.

2. Put $y_k = X_d e^{j\omega t_k}$, so $y_{k+1} = z y_k$. For $\theta = \tfrac12$, the step (1) applied to $y$ with the complex source $U e^{j\omega t_k}$ reads $\big(C(z - 1) + \tfrac h2 G(z + 1)\big) y_k = \tfrac h2 (z + 1) U e^{j\omega t_k}$. Divide by $\tfrac h2(z + 1)$, which is nonzero because $\omega h < \pi$, to get $(G + s_d C) X_d = U$. For $\theta = 1$, $C(z - 1) y_k + hG z y_k = hz\,U e^{j\omega t_k}$; divide by $hz$. The recurrence is real and linear, so the real part of a complex solution is a solution for the real source. The sequence is $S$-periodic because $z^S = 1$, so by Theorem 1 and the uniqueness in 1 it is the discrete steady state. Finally $(z - 1)/(z + 1) = j\tan(\omega h/2)$ for $|z| = 1$.

3. $\tan y = y + y^3/3 + O(y^5)$ gives $\tfrac2h\tan\tfrac{\omega h}2 = \omega + \omega^3 h^2/12 + O(h^4)$. For backward Euler, $(1 - e^{-j\omega h})/h = j\omega + \omega^2 h/2 + O(h^2)$. Near $s = j\omega$ the map $s \mapsto (G + sC)^{-1}U$ is differentiable when $G + j\omega C$ is nonsingular, so $X_d - X = O(|s_d - j\omega|)$. $\square$

## Algebraic rows and the trapezoidal rule

MNA equations are differential-algebraic: the row of a voltage source, for example, is $e_p - e_q = v(t)$ and has no charge term.

**Lemma 4.** Let row $a$ of $C(x)$ be zero for every $x$ and let row $a$ of $f$ be linear, $f_a(x) = g^{\mathsf T} x$. Then $g^{\mathsf T}\Phi_S = (-1)^S g^{\mathsf T}$ for the trapezoidal rule, and $g^{\mathsf T}\Phi_S = 0$ for backward Euler. So for the trapezoidal rule with even $S$, $g^{\mathsf T}(\Phi_S - I) = 0$ and the Newton matrix is singular.

*Proof.* Row $a$ of $A_k$ is $\theta h\, g^{\mathsf T}$ and row $a$ of $B_k$ is $-(1 - \theta) h\, g^{\mathsf T}$. Row $a$ of $A_k \Phi_{k+1} = B_k \Phi_k$ gives $\theta\, g^{\mathsf T}\Phi_{k+1} = -(1 - \theta)\, g^{\mathsf T}\Phi_k$. For $\theta = \tfrac12$ this is $g^{\mathsf T}\Phi_{k+1} = -g^{\mathsf T}\Phi_k$, and $S$ steps from $\Phi_0 = I$ give $(-1)^S g^{\mathsf T}$. For $\theta = 1$ it is $g^{\mathsf T}\Phi_{k+1} = 0$. $\square$

The cause is that the trapezoidal rule does not damp the algebraic part: an error in $g^{\mathsf T}x$ changes sign at every step and never decays. The remedies are backward Euler or another damped method, an odd $S$, or shooting on the state variables only (capacitor charges and inductor fluxes), which is the form in which Aprille and Trick stated the method.

## What is not proved

- **Existence and uniqueness** of a periodic steady state, and the nonsingularity of $\Phi_S - I$ at the root, are assumed. A Floquet multiplier (an eigenvalue of $\Phi_S$) equal to 1 makes the Newton matrix singular; this is always the case for an autonomous oscillator, which needs the period as an extra unknown.
- **Nonlinear discretization error.** Theorem 3 gives the $O(h^2)$ error of the trapezoidal rule only for linear circuits. For nonlinear circuits the error is measured on the page.
- **Global convergence.** The step limit is a heuristic; Newton can fail from a poor start.
- **The speed of plain transient analysis.** Near the steady state the error of a plain transient run is multiplied by about $\Phi_S$ each period, so it falls like the $p$th power of the spectral radius of $\Phi_S$, as for any [fixed-point iteration](/fixed-point-iteration/). The page measures this; it is not proved here for the nonlinear map.
- **Matrix-free Krylov solvers** for $(\Phi_S - I)\Delta = -r$ are not covered.
