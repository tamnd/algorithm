---
tag: 8WRT4F
kind: definition
slug: controllability-gramian
name: Controllability Gramian
aliases:
- reachability Gramian
area: control/state-space-control
level: core
summary: "W_c(t), the integral of e^(As)BB^T e^(A^T s) from 0 to t, is positive definite exactly for controllable pairs. For Hurwitz A the infinite integral exists and solves AW + WA^T + BB^T = 0."
prereqs: [controllability, matrix-exponential, positive-definite-matrix]
see_also: [observability-gramian, kalman-rank-condition, lyapunov-equation, minimum-energy-control, hankel-singular-values, balanced-realization, h2-norm, hurwitz-matrix]
sources:
  - paper: "R. E. Kalman, Contributions to the theory of optimal control, Boletín de la Sociedad Matemática Mexicana (2) 5, 102-119, 1960"
    locator: controllability tested by the nonsingularity of the gramian integral, and the minimum energy control
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 6.2 (the finite horizon gramian W_c(t) and the input that reaches a given state) and Section 7.4 (gramians of asymptotically stable systems and balanced realization)
  - book: isbn:9780134565675
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 3, Linear Dynamical Systems (controllability and the Lyapunov equations for the gramians when A is Hurwitz)
  - book: isbn:9780898715293
    title: Athanasios C. Antoulas, Approximation of Large-Scale Dynamical Systems, SIAM, 2005
    locator: Chapter 4 (the reachability gramian, finite and infinite, and the energy to reach a state)
---

The controllability gramian of a linear system $\dot x = A x + B u$ is the symmetric matrix $W_c(t) = \int_0^t e^{As} B B^T e^{A^T s} ds$. It is positive definite exactly when the pair $(A, B)$ is [controllable](/controllability/), and its inverse gives the least input energy needed to reach each state. The finite horizon form exists for every $A$. The infinite integral $W_c = \int_0^\infty e^{As} B B^T e^{A^T s} ds$ exists when $A$ is [Hurwitz](/hurwitz-matrix/), and then it is the solution of the [Lyapunov equation](/lyapunov-equation/) $A W_c + W_c A^T + B B^T = 0$. Its dual is the [observability gramian](/observability-gramian/), and the two together give the [Hankel singular values](/hankel-singular-values/).

## Definition

**Notation.** $A \in \mathbb{R}^{n \times n}$ and $B \in \mathbb{R}^{n \times m}$; the time $t$ is in seconds; $e^{At}$ is the [matrix exponential](/matrix-exponential/). For symmetric matrices, $P > 0$ means positive definite and $P \ge 0$ positive semidefinite.

**Finite horizon gramian.** For $t > 0$,

$$W_c(t) = \int_0^t e^{As} B B^T e^{A^T s}\, ds \in \mathbb{R}^{n \times n}.$$

It exists for every $A$. Its properties:

- $W_c(t)$ is symmetric and $W_c(t) \ge 0$, since $v^T W_c(t) v = \int_0^t |B^T e^{A^T s} v|^2 ds$.
- $W_c(t)$ grows with $t$: $W_c(t_2) - W_c(t_1) \ge 0$ for $t_2 \ge t_1$.
- $\operatorname{range} W_c(t) = \operatorname{range} [B, AB, \dots, A^{n-1} B]$ for every $t > 0$ (proof on [Kalman rank condition](/kalman-rank-condition/), Step 2). So $W_c(t) > 0$ for some $t > 0$ if and only if $W_c(t) > 0$ for all $t > 0$, if and only if $(A, B)$ is controllable.
- $W_c$ solves the matrix differential equation $\dot W_c = A W_c + W_c A^T + B B^T$ with $W_c(0) = 0$. Proof: the derivative of the integral is $e^{At} B B^T e^{A^T t}$, and $A W_c(t) + W_c(t) A^T = \int_0^t \frac{d}{ds} \bigl(e^{As} B B^T e^{A^T s}\bigr) ds = e^{At} B B^T e^{A^T t} - B B^T$.

**Infinite horizon gramian.** If $A$ is Hurwitz, $|e^{As}|$ decays exponentially, so the limit

$$W_c = \lim_{t \to \infty} W_c(t) = \int_0^\infty e^{As} B B^T e^{A^T s}\, ds$$

exists. Letting $t \to \infty$ in the identity of the last property gives

$$A W_c + W_c A^T + B B^T = 0 .$$

For Hurwitz $A$ no two eigenvalues have $\lambda_i + \lambda_j = 0$, so this equation has exactly one solution, and it is the gramian. Then $W_c > 0$ if and only if $(A, B)$ is controllable. If $A$ is not Hurwitz, the integral can diverge, and a solution of the algebraic equation, when one exists, need not be a gramian.

**Minimum energy.** Let $(A, B)$ be controllable and $t > 0$. Among all inputs on $[0, t]$ that steer $x(0) = 0$ to $x(t) = x_1$, the least value of $\int_0^t |u(s)|^2 ds$ is

$$E_{\min}(x_1, t) = x_1^T W_c(t)^{-1} x_1 ,$$

and the input $u^*(s) = B^T e^{A^T (t - s)} W_c(t)^{-1} x_1$ attains it. Proof: let $z = W_c(t)^{-1} x_1$. Step 3 on the Kalman rank condition page shows that $u^*$ reaches $x_1$. Any other input that reaches $x_1$ is $u = u^* + v$ with $\int_0^t e^{A(t - s)} B v(s)\, ds = 0$. Then $\int_0^t u^{*T} v\, ds = z^T \int_0^t e^{A(t-s)} B v\, ds = 0$, so $\int |u|^2 = \int |u^*|^2 + \int |v|^2 \ge \int |u^*|^2$, and $\int_0^t |u^*|^2 ds = z^T W_c(t) z = x_1^T W_c(t)^{-1} x_1$. For a Hurwitz $A$ and a start in the far past ($x(-\infty) = 0$), the same argument gives $x_1^T W_c^{-1} x_1$. States along eigenvectors of $W_c$ with small eigenvalues are the hard ones to reach. See [minimum energy control](/minimum-energy-control/).

**Coordinates.** Under $\bar x = T x$ the gramian becomes $T W_c T^T$. Its eigenvalues change with $T$, so they say nothing by themselves about the system. The eigenvalues of $W_c W_o$, with the observability gramian $W_o$, do not change; their square roots are the Hankel singular values, and a [balanced realization](/balanced-realization/) makes both gramians equal and diagonal.

**Discrete time.** For $x_{k+1} = A x_k + B u_k$, $W_c(N) = \sum_{k=0}^{N-1} A^k B B^T (A^T)^k$, and $W_c(N) > 0$ for $N \ge n$ if and only if the pair is controllable. If $A$ is Schur, the sum to infinity converges and solves the Stein equation $A W_c A^T - W_c + B B^T = 0$.

**Other readings.** If $w$ is white noise of unit intensity and $A$ is Hurwitz, the steady state covariance of $\dot x = A x + B w$ is $W_c$. For a strictly proper $G(s) = C (sI - A)^{-1} B$ with $A$ Hurwitz, the [H2 norm](/h2-norm/) is $\|G\|_2 = \sqrt{\operatorname{trace}(C W_c C^T)}$.

## Examples and non-examples

- **Scalar, the check value.** $a = -1$, $b = 1$: $W_c(t) = \int_0^t e^{-2s} ds = (1 - e^{-2t})/2$, and $W_c = 1/2$, which solves $-2 W + 1 = 0$. The least energy to reach $x_1 = 1$ is $2/(1 - e^{-2t})$: $3.1640$ for $t = 0.5$ s, $2.3130$ for $t = 1$ s and $2.0373$ for $t = 2$ s, with the limit $2 = 1/W_c$. With $c = 1$, $G(s) = 1/(s + 1)$ and $\|G\|_2 = \sqrt{1/2} = 1/\sqrt 2$.
- **Scalar, unstable (non-example for the infinite form).** $a = 1$, $b = 1$: $W_c(t) = (e^{2t} - 1)/2$ grows without bound, so there is no infinite gramian. The algebraic equation $2 W + 1 = 0$ has the solution $W = -1/2$, which is negative and is not a gramian. The least energy to reach $x_1 = 1$ is $2/(e^{2t} - 1)$, which goes to $0$: an unstable mode can be pushed far with little energy if there is time.
- **Double integrator.** $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$: $e^{As} B = (s, 1)^T$, so $W_c(t) = \begin{bmatrix} t^3/3 & t^2/2 \\ t^2/2 & t \end{bmatrix}$ with determinant $t^4/12 > 0$ for $t > 0$. The pair is controllable. $A$ is not Hurwitz, and the infinite gramian does not exist. For $t = 1$ s and $x_1 = (1, 0)$, the least energy is $x_1^T W_c(1)^{-1} x_1 = 12$.
- **A Hurwitz two-state system.** $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$ (eigenvalues $-1$, $-2$), $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$. The solution of $A W + W A^T + B B^T = 0$ is $W_c = \operatorname{diag}(1/12, 1/6)$: here $A W_c = \begin{bmatrix} 0 & 1/6 \\ -1/6 & -1/2 \end{bmatrix}$, and adding its transpose and $B B^T$ gives $0$. With $C = [1, 0]$, $G(s) = 1/((s+1)(s+2))$ and $\|G\|_2^2 = C W_c C^T = 1/12$. The impulse response $e^{-t} - e^{-2t}$ gives the same value: $\int_0^\infty (e^{-t} - e^{-2t})^2 dt = 1/2 - 2/3 + 1/4 = 1/12$.
- **Uncontrollable pair (non-example of a positive definite gramian).** $A = -I_2$, $B = (1, 1)^T$: the Lyapunov equation reads $-2 W + B B^T = 0$, so $W_c = \frac{1}{2} \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}$. It is singular, and its kernel, spanned by $(1, -1)$, is the direction the input cannot reach.

## Related definitions

- [Observability gramian](/observability-gramian/): $\int e^{A^T s} C^T C e^{A s} ds$, the dual object; it is the controllability gramian of $(A^T, C^T)$.
- [Controllability](/controllability/) and [Kalman rank condition](/kalman-rank-condition/): the gramian and the controllability matrix have the same range.
- [Lyapunov equation](/lyapunov-equation/): the linear matrix equation that the infinite gramian solves, with its solution methods. The [Lyapunov theorem for linear systems](/lyapunov-theorem-for-linear-systems/) uses the same equation to test stability.
- [Hankel singular values](/hankel-singular-values/) and [balanced realization](/balanced-realization/): built from both gramians, the base of [balanced truncation](/balanced-truncation/).
- [Minimum energy control](/minimum-energy-control/): the optimal control problem whose value is $x_1^T W_c(t)^{-1} x_1$.
- [H2 norm](/h2-norm/): computed from either gramian.

## References
