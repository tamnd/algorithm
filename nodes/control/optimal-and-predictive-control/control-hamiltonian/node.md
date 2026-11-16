---
tag: VG8FXN
kind: definition
slug: control-hamiltonian
name: Hamiltonian of an optimal control problem
aliases:
- control Hamiltonian
- Pontryagin Hamiltonian
area: control/optimal-and-predictive-control
level: core
summary: The function H = lambda_0 L(x, u) + lambda^T f(x, u) of state, input and costate. The optimal input minimizes it at each time, and its gradients give the state and costate equations.
prereqs: [optimal-control-problem, lagrange-multiplier]
see_also: [costate, pontryagin-maximum-principle, hamiltonian-matrix, hamiltonian-systems, transversality-conditions, euler-lagrange-equation, singular-arc, hamilton-jacobi-bellman-equation]
sources:
  - book: isbn:9780691151878
    title: Daniel Liberzon, Calculus of Variations and Optimal Control Theory, A Concise Introduction, Princeton University Press, 2012
    locator: Section 2.4 (the Hamiltonian formalism of the calculus of variations), Section 3.4 (the variational approach and the Hamiltonian) and Section 4.1 (the statement of the maximum principle)
  - book: isbn:9780486434841
    title: Donald E. Kirk, Optimal Control Theory, An Introduction, Prentice-Hall, 1970 (Dover reprint, 2004)
    locator: Section 5.1 (necessary conditions for optimal control, with the Hamiltonian)
  - paper: "L. S. Pontryagin, V. G. Boltyanskii, R. V. Gamkrelidze and E. F. Mishchenko, The Mathematical Theory of Optimal Processes, translated by K. N. Trirogoff, edited by L. W. Neustadt, Interscience, 1962 (Russian edition 1961)"
    locator: Chapter 1 (the function H and the statement of the maximum principle)
---

The Hamiltonian of an optimal control problem joins the running cost and the dynamics into one scalar function of the state $x$, the input $u$ and a multiplier vector $\lambda$, the [costate](/costate/). In the [maximum principle](/pontryagin-maximum-principle/), the optimal input minimizes the Hamiltonian over the allowed inputs at each time, and the derivatives of the Hamiltonian give the equations of the state and the costate. This area uses the minimum form, with the sign convention of the definition below.

## Definition

Take the [optimal control problem](/optimal-control-problem/) with dynamics $\dot x = f(x, u)$, $x \in \mathbb{R}^n$, $u \in U \subseteq \mathbb{R}^m$, and running cost $L(x, u)$, where $f$ and $L$ are $C^1$ in $x$ (and in $u$, where the derivative in $u$ is used). The **Hamiltonian** is the function

$$H(x, u, \lambda, \lambda_0) = \lambda_0 L(x, u) + \lambda^T f(x, u), \qquad x \in \mathbb{R}^n,\ u \in U,\ \lambda \in \mathbb{R}^n,\ \lambda_0 \in \{0, 1\}.$$

The number $\lambda_0$ is the cost multiplier. In the normal case $\lambda_0 = 1$ and one writes $H(x, u, \lambda) = L(x, u) + \lambda^T f(x, u)$. The abnormal case $\lambda_0 = 0$ is explained on the page of the [maximum principle](/pontryagin-maximum-principle/). For time-varying data, $H(t, x, u, \lambda, \lambda_0) = \lambda_0 L(t, x, u) + \lambda^T f(t, x, u)$.

Along a pair of functions $x(t)$ and $\lambda(t)$, the **canonical equations** are

$$\dot x = \frac{\partial H}{\partial \lambda} = f(x, u), \qquad \dot \lambda = -\frac{\partial H}{\partial x} = -\lambda_0 L_x(x, u)^T - f_x(x, u)^T \lambda.$$

The first is the dynamics. The second is the costate equation.

The **minimized Hamiltonian** is $h(x, \lambda, \lambda_0) = \inf_{u \in U} H(x, u, \lambda, \lambda_0)$. The minimum condition of the maximum principle says that an optimal input satisfies $H(x^*(t), u^*(t), \lambda(t), \lambda_0) = h(x^*(t), \lambda(t), \lambda_0)$ at almost every $t$.

The **switching function** of a control-affine problem, where $f = f_0(x) + G(x) u$ and $L = L_0(x) + c(x)^T u$, is the coefficient of $u$ in $H$: $\sigma(x, \lambda, \lambda_0) = \lambda_0 c(x) + G(x)^T \lambda \in \mathbb{R}^m$.

## Examples and non-examples

**A scalar problem.** For $\dot x = u$, $L = u^2$ and $U = \mathbb{R}$, the normal Hamiltonian is $H = u^2 + \lambda u$. It is smallest at $u = -\lambda/2$, so $h(\lambda) = -\lambda^2/4$. The costate equation is $\dot\lambda = -H_x = 0$. With $x(0) = 1$, the horizon 1 and the terminal cost $x(1)^2$, the [costate](/costate/) page shows $\lambda = 1$ and $u^* = -1/2$, which agrees with the direct computation on the [optimal control problem](/optimal-control-problem/) page.

**The linear quadratic regulator.** For $\dot x = A x + B u$ and $L = x^T Q x + u^T R u$ with $R > 0$,

$$H = x^T Q x + u^T R u + \lambda^T (A x + B u).$$

$H$ is strictly convex in $u$, and $H_u = 2 R u + B^T \lambda = 0$ gives $u = -\tfrac12 R^{-1} B^T \lambda$. The canonical equations become $\dot x = A x - \tfrac12 B R^{-1} B^T \lambda$ and $\dot\lambda = -2 Q x - A^T \lambda$. With $\mu = \lambda / 2$, the pair $(x, \mu)$ solves the linear system with the [Hamiltonian matrix](/hamiltonian-matrix/)

$$\begin{bmatrix} \dot x \\ \dot \mu \end{bmatrix} = \begin{bmatrix} A & -B R^{-1} B^T \\ -Q & -A^T \end{bmatrix} \begin{bmatrix} x \\ \mu \end{bmatrix}.$$

If $\lambda = 2 P x$, then $u = -R^{-1} B^T P x$, the LQR feedback. The factor 2 comes from the cost without a factor $\tfrac12$, the convention of this area.

**A bounded input.** For $\dot x = u$, $L = 1$ and $U = [-1, 1]$ (a minimum-time problem), $H = \lambda_0 + \lambda u$ is linear in $u$. Its minimum is at $u = -\operatorname{sgn}\lambda$ when $\lambda \ne 0$, and the value is $h = \lambda_0 - |\lambda|$. The Hamiltonian is not differentiable in $u$ at its minimizer, and $H_u = 0$ has no solution. This is why the minimum condition, and not $H_u = 0$, is the general rule. The [bang-bang principle](/bang-bang-control/) starts from this case.

**Non-example: the Hamiltonian of mechanics.** In the calculus of variations, with $f(x, u) = u$, the Hamiltonian of classical mechanics is $H_{\text{mech}}(x, p) = \sup_v (p^T v - L(x, v))$, the Legendre transform of $L$. It is not the control Hamiltonian, but the two are related: $h(x, \lambda, 1) = \inf_v (L + \lambda^T v) = -H_{\text{mech}}(x, -\lambda)$. So the costate is the negative of the momentum $p = L_{\dot x}$ of mechanics, which matches the [Euler-Lagrange equation](/euler-lagrange-equation/) page.

**Non-example: the maximum form.** Pontryagin et al. (1962) and Liberzon (2012) use the function $\langle p, f \rangle + p_0 L$ with a constant $p_0 \le 0$ and maximize it. With $p = -\lambda$ and $p_0 = -\lambda_0$ it equals $-H$, so the maximum of one is the minimum of the other. The two forms give the same optimal inputs, but formulas copied between them change sign. On this site every page, the [maximum principle](/pontryagin-maximum-principle/) page included, uses $H$ as defined above; that page shows the maximum form only to translate it.

**Non-example: the Hamiltonian matrix.** The [Hamiltonian matrix](/hamiltonian-matrix/) is the $2n \times 2n$ matrix of the canonical equations of the LQR problem, shown above. It is a matrix, not a function, and it has a structure of its own (its eigenvalues are symmetric about the imaginary axis).

## Related definitions

- **[Costate](/costate/).** The multiplier $\lambda(t)$ that solves $\dot\lambda = -H_x$, with end conditions from the [transversality conditions](/transversality-conditions/).
- **Constancy of the Hamiltonian.** For a problem whose data do not depend on time, $H(x^*(t), u^*(t), \lambda(t), \lambda_0)$ is constant along an optimal trajectory, and it is 0 if the final time is free. The proof is on the page of the [maximum principle](/pontryagin-maximum-principle/).
- **[Hamiltonian systems](/hamiltonian-systems/).** If the minimizer $u = \kappa(x, \lambda)$ is unique and smooth, the canonical equations with $u = \kappa(x, \lambda)$ form the Hamiltonian system of the function $h(x, \lambda)$. Its flow keeps the symplectic form.
- **Hamiltonian in the HJB equation.** The [Hamilton-Jacobi-Bellman equation](/hamilton-jacobi-bellman-equation/) is $-V_t = h(x, V_x^T, 1)$, so the same minimized Hamiltonian appears there with $\lambda$ replaced by the gradient of the value function.
- **Singular arc.** An interval on which the switching function $\sigma$ is identically zero, so the minimum condition does not fix $u$ ([singular arc](/singular-arc/)).

## References
