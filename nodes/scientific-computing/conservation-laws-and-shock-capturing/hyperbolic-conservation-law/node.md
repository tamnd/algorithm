---
tag: BH1Q8B
kind: definition
slug: hyperbolic-conservation-law
name: Hyperbolic conservation law
aliases:
- system of conservation laws
area: scientific-computing/conservation-laws-and-shock-capturing
level: intro
summary: "A system U_t + F(U)_x = 0. The conservation form says each quantity changes only by its flux. The system is hyperbolic when F'(U) has real eigenvalues and a full set of eigenvectors."
prereqs: [pde-classification, advection-equation]
see_also: [burgers-equation, euler-equations-of-gas-dynamics, shallow-water-equations, weak-solution-of-conservation-law, method-of-characteristics, riemann-problem, finite-volume-method, rankine-hugoniot-conditions]
sources:
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Chapter 2 (conservation laws and differential equations; Section 2.9 hyperbolicity of linear systems, Section 2.11 hyperbolicity of quasilinear and nonlinear systems), Section 11.12 (manipulating conservation laws)
  - book: isbn:9783540252023
    title: Eleuterio F. Toro, Riemann Solvers and Numerical Methods for Fluid Dynamics, third edition, Springer, 2009
    locator: Section 2.4 (conservation laws; 2.4.1 integral forms, 2.4.3 characteristic fields)
---

A hyperbolic conservation law is a system of partial differential equations $U_t + F(U)_x = 0$ with two separate properties. The first property is the conservation form: each component of $U$ changes in an interval only by what its flux $F(U)$ carries through the ends of the interval. The second property is hyperbolicity: the flux Jacobian $A(U) = F'(U)$ has real eigenvalues and a full set of eigenvectors, so the solution is made of waves that move at finite speeds. A system can have one property without the other. The definition here is the base of this sub-area. A [weak solution](/weak-solution-of-conservation-law/) gives a meaning to discontinuous solutions, the [Rankine-Hugoniot conditions](/rankine-hugoniot-conditions/) fix the speed of a jump, the [Lax entropy condition](/lax-entropy-condition/) selects the physical jumps, and the [Lax-Wendroff theorem](/lax-wendroff-theorem/) says what a conservative scheme converges to.

## Definition

Let $\Omega \subseteq \mathbb{R}^m$ be an open set of states and $F : \Omega \to \mathbb{R}^m$ a $C^1$ function, the flux. The equation

$$U_t + F(U)_x = 0, \qquad U(x, t) \in \Omega, \quad x \in \mathbb{R}, \ t > 0,$$

is a **system of conservation laws** in one space dimension. For $m = 1$ it is a scalar conservation law $u_t + f(u)_x = 0$.

- **Conservation form.** For a smooth solution and any interval $[a, b]$,
$$\frac{d}{dt}\int_a^bU(x, t)\,dx = F(U(a, t)) - F(U(b, t)).$$
This integral form is the physical law. It also makes sense for discontinuous $U$, and the differential form follows from it only where $U$ is smooth.
- **Hyperbolicity.** The system is **hyperbolic** at $U$ if $A(U) = F'(U)$ is diagonalizable with real eigenvalues $\lambda_1(U) \le \dots \le \lambda_m(U)$ and right eigenvectors $r_1(U), \dots, r_m(U)$. It is **strictly hyperbolic** if the eigenvalues are distinct. The system is hyperbolic if this holds at every $U \in \Omega$.

The eigenvalues are the speeds of the characteristic fields. Field $p$ is **genuinely nonlinear** if $\nabla\lambda_p(U)\cdot r_p(U) \ne 0$ for all $U$, and **linearly degenerate** if $\nabla\lambda_p(U)\cdot r_p(U) = 0$ for all $U$. In $d$ space dimensions the system is $U_t + \sum_iF_i(U)_{x_i} = 0$, and hyperbolicity asks that $\sum_in_iF_i'(U)$ is diagonalizable with real eigenvalues for every unit vector $n$.

## Examples and non-examples

- **Linear advection**, $u_t + au_x = 0$: $A = a$ is real, so the law is hyperbolic, with one wave of speed $a$. See [advection equation](/advection-equation/).
- **Burgers' equation**, $u_t + (u^2/2)_x = 0$: $A(u) = u$. The field is genuinely nonlinear, because $\lambda'(u) = 1 \ne 0$. Smooth data such as $u_0 = -x$ near $0$ form a shock in finite time. See [Burgers' equation](/burgers-equation/).
- **The wave equation as a system.** With $U = (v, w)$ and $F(U) = (-w, -v)$, the matrix $A = \begin{pmatrix} 0 & -1 \\ -1 & 0 \end{pmatrix}$ has eigenvalues $-1$ and $1$ with eigenvectors $(1, 1)$ and $(1, -1)$. The system is strictly hyperbolic.
- **Not hyperbolic: complex eigenvalues.** $A = \begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}$ has eigenvalues $\pm i$. The system $v_t + w_x = 0$, $w_t - v_x = 0$ is the Cauchy-Riemann system in $(x, t)$. It is in conservation form, but it is elliptic, and the initial value problem is ill posed.
- **Not hyperbolic: a missing eigenvector.** $A = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$ has the real double eigenvalue 1 but only the eigenvector $(1, 0)$. The system is called weakly hyperbolic. With $U = (v, w)$, the solution of $U_t + AU_x = 0$ is $w = w_0(x - t)$ and $v = v_0(x - t) - t\,w_0'(x - t)$, so it loses a derivative, and the problem is not well posed in $L^2$.
- **Hyperbolic but not conservative.** $u_t + uu_x = 0$ is hyperbolic. It agrees with Burgers' equation for smooth solutions, but it is not in conservation form, and so it does not fix the speed of a shock. For smooth solutions it also gives $(u^2/2)_t + (u^3/3)_x = 0$. For the jump from $u_L = 1$ to $u_R = 0$, Burgers' equation gives the shock speed $\frac{1/2 - 0}{1 - 0} = \frac12$, and the second law gives $\frac{1/3 - 0}{1/2 - 0} = \frac23$. The two conservation laws have the same smooth solutions and different weak solutions (LeVeque 2002, Section 11.12).
- **Physical systems.** The [Euler equations of gas dynamics](/euler-equations-of-gas-dynamics/) have the speeds $u - c$, $u$ and $u + c$. The [shallow water equations](/shallow-water-equations/) have $u - \sqrt{gh}$ and $u + \sqrt{gh}$, where $h$ is the water depth. Both are strictly hyperbolic where the density or the depth is positive.

## Related definitions

- **Balance law.** $U_t + F(U)_x = S(U, x)$ with a source term, for example the bottom slope in shallow water (LeVeque 2002, Chapter 17).
- **Quasilinear form.** $U_t + A(U)U_x = 0$. It is equivalent to the conservation form only for smooth solutions.
- **Characteristic variables.** For a linear system $A = R\Lambda R^{-1}$, and $W = R^{-1}U$ satisfies $m$ decoupled advection equations $w_{p,t} + \lambda_pw_{p,x} = 0$. See [method of characteristics](/method-of-characteristics/).
- **Riemann problem.** The conservation law with data that are constant on each side of $x = 0$. Its solution is the building block of Godunov-type schemes. See [Riemann problem](/riemann-problem/).
- **Classification of PDEs.** Hyperbolic, parabolic and elliptic equations. See [classification of PDEs](/pde-classification/).

## References
