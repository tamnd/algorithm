---
tag: 3Y8GXW
kind: definition
slug: state-transition-matrix
name: State-transition matrix
aliases:
- transition matrix of a linear system
area: control/modeling-and-identification
level: core
summary: The matrix Phi(t, t0) that maps the state at time t0 to the state at time t of a linear, possibly time-varying, system.
prereqs: [matrix-exponential, linear-time-varying-system]
see_also: [matrix-exponential, variation-of-constants-formula, linear-time-varying-system, picard-lindelof-theorem, controllability-gramian, exponential-stability, gronwall-inequality, markov-chain]
sources:
  - book: isbn:9780134412054
    title: Wilson J. Rugh, Linear System Theory, second edition, Prentice Hall, 1996
    locator: Chapter 3, State Equation Solution (existence by the Peano-Baker series); Chapter 4, Transition Matrix Properties; Chapter 5, Two Important Cases (time-invariant and periodic); Chapter 20 (discrete time)
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 4.6, Linear Time-Varying Systems and Linearization; Example 4.22 (an A(t) with constant eigenvalues in the left half plane and an unbounded solution)
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Chapter 4 (solution of linear time-varying state equations by a fundamental matrix)
  - book: isbn:9780387984896
    title: Eduardo D. Sontag, Mathematical Control Theory, Deterministic Finite Dimensional Systems, second edition, Springer, 1998
    locator: the material on linear time-varying systems and their fundamental solutions
---

The state-transition matrix $\Phi(t, t_0)$ of the linear system $\dot x = A(t) x$ is the $n \times n$ matrix that maps the state at time $t_0$ to the state at time $t$: $x(t) = \Phi(t, t_0)\, x(t_0)$ for every solution. For a constant matrix $A$ it is the [matrix exponential](/matrix-exponential/) $e^{A(t - t_0)}$. For a time-varying $A(t)$ it is the sum of the Peano-Baker series, and in general it is not the exponential of $\int_{t_0}^t A(\sigma)\, d\sigma$. With an input, the [variation of constants formula](/variation-of-constants-formula/) writes the full solution of a [linear time-varying system](/linear-time-varying-system/) in terms of $\Phi$.

## Definition

Let $A : J \to \mathbb{R}^{n \times n}$ be continuous on an interval $J$. (Piecewise continuous, or locally integrable, is enough; then the equations below hold for almost every $t$.) The *state-transition matrix* of $\dot x = A(t) x$ is the function $\Phi : J \times J \to \mathbb{R}^{n \times n}$ such that, for each fixed $t_0 \in J$, $t \mapsto \Phi(t, t_0)$ is the solution of the matrix equation

$$\frac{\partial}{\partial t} \Phi(t, t_0) = A(t)\, \Phi(t, t_0), \qquad \Phi(t_0, t_0) = I.$$

Column $j$ of $\Phi(t, t_0)$ is the solution that starts at the unit vector $e_j$ at time $t_0$. By linearity, the solution from any $x_0$ is $x(t) = \Phi(t, t_0) x_0$.

**Existence: the Peano-Baker series.** Define $M_0(t) = I$ and $M_{k+1}(t) = \int_{t_0}^{t} A(\sigma) M_k(\sigma)\, d\sigma$. Then

$$\Phi(t, t_0) = I + \int_{t_0}^{t} A(\sigma_1)\, d\sigma_1 + \int_{t_0}^{t} A(\sigma_1) \int_{t_0}^{\sigma_1} A(\sigma_2)\, d\sigma_2\, d\sigma_1 + \cdots = \sum_{k \ge 0} M_k(t).$$

The partial sums are the Picard iterates of the integral equation $\Phi(t, t_0) = I + \int_{t_0}^t A(\sigma) \Phi(\sigma, t_0)\, d\sigma$. Let $a(t) = |\int_{t_0}^t \|A(\sigma)\|\, d\sigma|$. Induction gives $\|M_k(t)\| \le a(t)^k / k!$, so the series converges absolutely and uniformly on every compact interval, and $\|\Phi(t, t_0)\| \le e^{a(t)}$. Term by term differentiation shows that the sum solves the matrix equation, and it is the only solution because the equation is linear in $\Phi$, so the [Picard-Lindelöf theorem](/picard-lindelof-theorem/) applies to each column. The bound also follows from the [Grönwall inequality](/gronwall-inequality/).

**Properties.** For all $t, \tau, \sigma \in J$:

1. *Composition.* $\Phi(t, \sigma)\, \Phi(\sigma, \tau) = \Phi(t, \tau)$. Both sides solve the matrix equation in $t$ and agree at $t = \sigma$.
2. *Inverse.* $\Phi(t, \tau)$ is invertible and $\Phi(t, \tau)^{-1} = \Phi(\tau, t)$, from property 1 with $t = \tau$.
3. *Derivative in the second argument.* $\frac{\partial}{\partial \tau} \Phi(t, \tau) = -\Phi(t, \tau) A(\tau)$. Differentiate $\Phi(t, \tau)\Phi(\tau, t) = I$ in $\tau$.
4. *Determinant (Liouville's formula).* $\det \Phi(t, \tau) = \exp\left(\int_\tau^t \operatorname{tr} A(\sigma)\, d\sigma\right)$.
5. *Fundamental matrices.* If $X(t)$ is any invertible solution of $\dot X = A(t) X$, then $\Phi(t, \tau) = X(t) X(\tau)^{-1}$.
6. *Adjoint system.* The transition matrix of $\dot z = -A(t)^T z$ is $\Phi(\tau, t)^T$.
7. *Time-invariant case.* If $A$ is constant, $\Phi(t, \tau) = e^{A(t - \tau)}$, which depends only on $t - \tau$.
8. *Commuting case.* If $A(t)$ commutes with $\int_\tau^t A(\sigma)\, d\sigma$ for all $t$, then $\Phi(t, \tau) = \exp\left(\int_\tau^t A(\sigma)\, d\sigma\right)$. This holds for $A(t) = a(t) M$ with a fixed $M$, and for diagonal $A(t)$, but it fails in general.
9. *Periodic case.* If $A(t + T) = A(t)$, then $\Phi(t + T, \tau + T) = \Phi(t, \tau)$. The matrix $\Phi(\tau + T, \tau)$ is the *monodromy matrix*. The solutions all tend to 0 if and only if all eigenvalues of the monodromy matrix have modulus less than 1 (Floquet theory; Rugh 1996, Chapter 5).

**With an input.** For $\dot x = A(t) x + B(t) u$, the solution is $x(t) = \Phi(t, t_0) x_0 + \int_{t_0}^t \Phi(t, s) B(s) u(s)\, ds$. The proof is on the [variation of constants formula](/variation-of-constants-formula/) page.

**Discrete time.** For $x_{k+1} = A_k x_k$, the transition matrix is $\Phi(k, j) = A_{k-1} A_{k-2} \cdots A_j$ for $k > j$, and $\Phi(j, j) = I$. Composition holds for $k \ge \ell \ge j$. Unlike the continuous case, $\Phi(k, j)$ can be singular, because a factor $A_i$ can be singular; then the system cannot be run backward.

**Computation.** In practice $\Phi(t, t_0)$ is computed by integrating the matrix equation with an ODE method such as [Runge-Kutta methods](/runge-kutta-methods/), $n$ columns at once. The Peano-Baker series is a tool for proofs; summing it numerically needs nested quadratures. Over a long interval, compute $\Phi$ on short pieces and multiply them with property 1.

## Examples and non-examples

**Time-invariant.** For $A = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}$, $\Phi(t, \tau) = \begin{bmatrix} \cos(t - \tau) & \sin(t - \tau) \\ -\sin(t - \tau) & \cos(t - \tau) \end{bmatrix}$.

**A commuting time-varying example.** Let $A(t) = \begin{bmatrix} -1 & e^{2t} \\ 0 & -1 \end{bmatrix} = -I + e^{2t} N$ with $N = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$. All $A(t)$ commute with each other, so property 8 applies. Solving the equations directly gives $x_2(t) = e^{-(t - \tau)} x_2(\tau)$ and then

$$\Phi(t, \tau) = \begin{bmatrix} e^{-(t - \tau)} & \tfrac12 \left(e^{t + \tau} - e^{3\tau - t}\right) \\ 0 & e^{-(t - \tau)} \end{bmatrix}.$$

The eigenvalues of $A(t)$ are $-1, -1$ at every $t$, yet $\Phi(t, 0)_{12} = \sinh t$ grows without bound. The matrix depends on both times, not on $t - \tau$ alone: $\Phi(1, 0)_{12} = \sinh 1 = 1.1752$, while $\Phi(2, 1)_{12} = (e^3 - e)/2 = 8.6836$. Liouville's formula gives $\det \Phi(t, \tau) = e^{-2(t - \tau)}$, which matches the product of the diagonal entries.

**A non-commuting example (Khalil 2002, Example 4.22).** Let

$$A(t) = \begin{bmatrix} -1 + 1.5 \cos^2 t & 1 - 1.5 \sin t \cos t \\ -1 - 1.5 \sin t \cos t & -1 + 1.5 \sin^2 t \end{bmatrix}.$$

Then

$$\Phi(t, 0) = \begin{bmatrix} e^{0.5 t} \cos t & e^{-t} \sin t \\ -e^{0.5 t} \sin t & e^{-t} \cos t \end{bmatrix}.$$

To check the first column, differentiate $x_1 = e^{0.5t} \cos t$: $\dot x_1 = e^{0.5t}(0.5 \cos t - \sin t)$, and the first row of $A(t)$ times the column gives $e^{0.5t}(-\cos t + 1.5 \cos^3 t - \sin t + 1.5 \sin^2 t \cos t) = e^{0.5t}(0.5 \cos t - \sin t)$. The second row and the second column check the same way. Here $\operatorname{tr} A(t) = -0.5$, and $\det \Phi(t, 0) = e^{-0.5t}$, as Liouville's formula says. At $t = 2$,

$$\Phi(2, 0) = \begin{bmatrix} -1.1312 & 0.1231 \\ -2.4717 & -0.0563 \end{bmatrix}, \qquad \exp\left(\int_0^2 A(\sigma)\, d\sigma\right) = \begin{bmatrix} -0.2719 & 0.4240 \\ -0.8051 & -0.0974 \end{bmatrix},$$

so the exponential of the integral is not the transition matrix. The matrix $A(t)$ has period $\pi$, and the monodromy matrix is $\Phi(\pi, 0) = \operatorname{diag}(-e^{\pi/2}, -e^{-\pi}) = \operatorname{diag}(-4.8105, -0.0432)$. One eigenvalue has modulus above 1, so the system is unstable, although the eigenvalues of $A(t)$ are $-0.25 \pm 0.6614 i$ for every $t$.

**Non-example: frozen-time exponentials.** The product $e^{A(t_0) \Delta}$ over one step is not $\Phi(t_0 + \Delta, t_0)$; it is a first-order approximation. Products of frozen exponentials over many small steps converge to $\Phi$ as the step goes to 0, like Euler's method.

**Discrete singular example.** With $A_0 = A_1 = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $\Phi(2, 0) = A_1 A_0 = 0$. Every initial state reaches 0 in two steps, and the initial state cannot be recovered from $x_2$.

## Related definitions

- **Matrix exponential.** The transition matrix of a time-invariant system. See [matrix exponential](/matrix-exponential/).
- **Fundamental matrix.** Any $n \times n$ invertible solution $X(t)$ of $\dot X = A(t) X$. The transition matrix is the fundamental matrix normalized at $t_0$: $\Phi(t, t_0) = X(t) X(t_0)^{-1}$.
- **Uniform exponential stability.** The system $\dot x = A(t) x$ is uniformly exponentially stable if there are $c, \lambda > 0$ with $\|\Phi(t, \tau)\| \le c e^{-\lambda (t - \tau)}$ for all $t \ge \tau$. The two examples above show that the eigenvalues of $A(t)$ do not decide it. See [exponential stability](/exponential-stability/) and the [linear time-varying system](/linear-time-varying-system/) page.
- **Controllability gramian.** For the time-varying system, $W(t_0, t_1) = \int_{t_0}^{t_1} \Phi(t_1, s) B(s) B(s)^T \Phi(t_1, s)^T\, ds$. The system is controllable on $[t_0, t_1]$ if and only if $W$ is invertible. See [controllability gramian](/controllability-gramian/).
- **Transition matrix of a Markov chain.** A different object with the same name: the matrix of probabilities $P(s, t)$ of moving between states of a [Markov chain](/markov-chain/). For a time-homogeneous continuous-time chain with generator $Q$, $P(s, t) = e^{Q(t - s)}$, which is the state-transition matrix of the forward equation $\dot p^T = p^T Q$.

## References
