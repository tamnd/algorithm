---
tag: QKFZ5S
kind: definition
slug: butcher-tableau
name: Butcher tableau
aliases:
- Butcher array
- Runge-Kutta tableau
area: numerical/differential-equations
level: core
summary: The table of coefficients (A, b, c) that defines an s-stage Runge-Kutta method. Its shape tells explicit from implicit methods, and its entries give the order and the stability function.
prereqs: [ode-initial-value-problem]
see_also: [runge-kutta-methods, butcher-order-conditions, classical-runge-kutta-4, embedded-runge-kutta-pairs, implicit-runge-kutta-methods, gauss-legendre-runge-kutta, absolute-stability, explicit-midpoint-method]
sources:
  - book: isbn:9781119121503
    title: John C. Butcher, Numerical Methods for Ordinary Differential Equations, third edition, Wiley, 2016
    locator: Chapter 2 (Runge-Kutta methods introduced with their tableaux) and Chapter 3 (Runge-Kutta methods, order conditions, implicit methods, stability)
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.1 (definition of explicit Runge-Kutta methods and the tableau notation), Section II.7 (implicit Runge-Kutta methods)
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Section IV.3 (stability function of implicit Runge-Kutta methods as a quotient of determinants)
  - paper: doi:10.1017/S1446788700027932
    title: J. C. Butcher, Coefficients for the study of Runge-Kutta integration processes, Journal of the Australian Mathematical Society 3 (1963) 185-201
    locator: the coefficient array of a Runge-Kutta method and its order conditions
---

A Butcher tableau is the array of coefficients $(A, b, c)$ that defines an $s$-stage [Runge-Kutta method](/runge-kutta-methods/) for the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$. The matrix $A$ says how the stages are combined, the weights $b$ say how the stages build the new value, and the nodes $c$ say at which times inside the step the stages are taken. Butcher introduced the notation together with his theory of [order conditions](/butcher-order-conditions/), and it is now the standard way to write down, compare and analyse Runge-Kutta methods.

## Definition

**Notation.** The step is $h$, $t_n$ is the current time and $y_n \in \mathbb{R}^d$ the current value.

An $s$-stage Runge-Kutta method is given by a matrix $A = (a_{ij}) \in \mathbb{R}^{s \times s}$ and vectors $b, c \in \mathbb{R}^s$. One step computes the stage derivatives $k_1, \dots, k_s$ and the new value by
$$k_i = f\Big(t_n + c_i h,\; y_n + h \sum_{j=1}^{s} a_{ij} k_j\Big) \quad (i = 1, \dots, s), \qquad y_{n+1} = y_n + h\sum_{i=1}^{s} b_i k_i.$$
The vectors $Y_i = y_n + h\sum_j a_{ij}k_j$ are the stage values. The **Butcher tableau** writes the coefficients as
$$\begin{array}{c|ccc} c_1 & a_{11} & \cdots & a_{1s} \\ \vdots & \vdots & & \vdots \\ c_s & a_{s1} & \cdots & a_{ss} \\ \hline & b_1 & \cdots & b_s \end{array}$$

**Conventions and classes.**

- Almost all methods satisfy the **row-sum condition** $c_i = \sum_j a_{ij}$. Then the method gives the same result on $y' = f(t, y)$ and on the equivalent autonomous system for $(t, y)$.
- **Explicit**: $A$ is strictly lower triangular ($a_{ij} = 0$ for $j \ge i$). Each $k_i$ is computed from $k_1, \dots, k_{i-1}$, with one evaluation of $f$. The zero entries on and above the diagonal are often left blank.
- **Diagonally implicit (DIRK)**: $A$ is lower triangular with some $a_{ii} \ne 0$. The stages are solved one after another, each a system of dimension $d$. **Singly diagonally implicit (SDIRK)**: all $a_{ii}$ equal, so one LU factorization of $I - h a_{ii} J$ serves all stages.
- **Fully implicit**: $A$ is a full matrix. All stages are coupled in one system of dimension $sd$.
- **Embedded pair**: a second weight row $\hat b$ under $b$ gives a second solution $\hat y_{n+1} = y_n + h\sum_i \hat b_i k_i$ of another order from the same stages; the difference estimates the error ([embedded pairs](/embedded-runge-kutta-pairs/)).
- **FSAL** (first same as last): the last row of $A$ equals $b$ and $c_s = 1$, so the last stage of a step is the first stage of the next, and an accepted step costs one evaluation less.

**What the tableau determines.**

- *Consistency and order.* The method is [consistent](/consistency/) if and only if $\sum_i b_i = 1$. It has order 2 if also $\sum_i b_i c_i = 1/2$ (under the row-sum condition). The full set of conditions, one for each rooted tree, is in [Butcher order conditions](/butcher-order-conditions/).
- *Stability function.* On $y' = \lambda y$ with $z = h\lambda$, the method gives $y_{n+1} = R(z)y_n$ with
$$R(z) = 1 + z\, b^T(I - zA)^{-1}\mathbf{1} = \frac{\det(I - zA + z\,\mathbf{1}b^T)}{\det(I - zA)},$$
where $\mathbf{1} = (1, \dots, 1)^T$. *Proof.* The stage equations become $K = \lambda y_n \mathbf{1} + zAK$ for $K = (k_i)$, so $K = \lambda y_n (I - zA)^{-1}\mathbf{1}$ and $y_{n+1} = y_n + h b^T K = (1 + z b^T (I - zA)^{-1}\mathbf{1}) y_n$. The second form follows from the matrix determinant lemma $\det(M + uv^T) = \det(M)(1 + v^T M^{-1}u)$ with $M = I - zA$, $u = z\mathbf{1}$ and $v = b$. $\square$ For an explicit method $\det(I - zA) = 1$, so $R$ is a polynomial of degree at most $s$.
- *Cost.* An explicit tableau costs $s$ evaluations of $f$ per step. An implicit one costs a nonlinear solve of dimension $sd$ (fully implicit) or $s$ solves of dimension $d$ (DIRK).

## Examples and non-examples

Explicit Euler, the [explicit midpoint rule](/explicit-midpoint-method/) and [Heun's method](/heuns-method/):
$$\begin{array}{c|c} 0 & 0 \\ \hline & 1 \end{array} \qquad \begin{array}{c|cc} 0 & & \\ \tfrac12 & \tfrac12 & \\ \hline & 0 & 1 \end{array} \qquad \begin{array}{c|cc} 0 & & \\ 1 & 1 & \\ \hline & \tfrac12 & \tfrac12 \end{array}$$

The [classical Runge-Kutta method](/classical-runge-kutta-4/), explicit with 4 stages and order 4:
$$\begin{array}{c|cccc} 0 & & & & \\ \tfrac12 & \tfrac12 & & & \\ \tfrac12 & 0 & \tfrac12 & & \\ 1 & 0 & 0 & 1 & \\ \hline & \tfrac16 & \tfrac13 & \tfrac13 & \tfrac16 \end{array}$$
One step for $y' = y$, $y_0 = 1$, $h = 0.1$: $k_1 = 1$, $k_2 = 1 + 0.05 \cdot 1 = 1.05$, $k_3 = 1 + 0.05 \cdot 1.05 = 1.0525$, $k_4 = 1 + 0.1 \cdot 1.0525 = 1.10525$, and $y_1 = 1 + \tfrac{0.1}{6}(1 + 2.1 + 2.105 + 1.10525) = 1.10517083$, against $e^{0.1} = 1.10517092$.

Implicit methods: [backward Euler](/backward-euler-method/), the implicit midpoint rule, the trapezoidal rule (with an explicit first stage), and the 2-stage [Gauss method](/gauss-legendre-runge-kutta/) of order 4:
$$\begin{array}{c|c} 1 & 1 \\ \hline & 1 \end{array} \qquad \begin{array}{c|c} \tfrac12 & \tfrac12 \\ \hline & 1 \end{array} \qquad \begin{array}{c|cc} 0 & 0 & 0 \\ 1 & \tfrac12 & \tfrac12 \\ \hline & \tfrac12 & \tfrac12 \end{array} \qquad \begin{array}{c|cc} \tfrac12 - \tfrac{\sqrt3}{6} & \tfrac14 & \tfrac14 - \tfrac{\sqrt3}{6} \\ \tfrac12 + \tfrac{\sqrt3}{6} & \tfrac14 + \tfrac{\sqrt3}{6} & \tfrac14 \\ \hline & \tfrac12 & \tfrac12 \end{array}$$
For the Gauss method the determinant formula gives $R(z) = (1 + z/2 + z^2/12)/(1 - z/2 + z^2/12)$, the $(2,2)$ Padé approximant of $e^z$. At $z = -1$ both forms give $0.368421$ (against $e^{-1} = 0.367879$), and at $z = -10$ both give $0.302326$.

**Non-example: an inconsistent tableau.** $A = (0)$, $c = (0)$, $b = (2)$ is a valid table of numbers, but $\sum b_i = 2$, so the method computes the solution of $y' = 2f$, not of $y' = f$.

**Non-example: not a Runge-Kutta method.** A [linear multistep method](/linear-multistep-methods/) such as Adams-Bashforth uses values from earlier steps, and no tableau $(A, b, c)$ describes it; general linear methods need a larger array of four matrices.

**A tableau that breaks the row-sum condition.** Take Heun's tableau but with $c_2 = 0$ instead of 1. The second stage then evaluates $f$ at time $t_n$ at a point that approximates the solution at $t_n + h$. On $y' = t$ the step gives $y_n + ht_n$ instead of $y_n + ht_n + h^2/2$, so the order drops from 2 to 1 on this non-autonomous problem, while on autonomous problems nothing changes.

## Related definitions

- **[Runge-Kutta methods](/runge-kutta-methods/).** The family of methods that tableaux describe.
- **[Butcher order conditions](/butcher-order-conditions/).** For each rooted tree $\tau$ with $|\tau| \le p$, a polynomial equation in $(A, b, c)$; order $p$ holds if and only if all of them hold.
- **Simplifying assumptions** $B(p)$: $\sum_i b_i c_i^{k-1} = 1/k$ for $k \le p$; $C(q)$: $\sum_j a_{ij}c_j^{k-1} = c_i^k/k$ for $k \le q$; $D(r)$: $\sum_i b_i c_i^{k-1}a_{ij} = b_j(1 - c_j^k)/k$ for $k \le r$. They are used to build high-order implicit methods such as Gauss and [Radau IIA](/radau-iia-methods/).
- **[Embedded Runge-Kutta pairs](/embedded-runge-kutta-pairs/).** Tableaux with two weight rows, used for [adaptive step size control](/adaptive-step-size-control/).
- **[Stability function](/absolute-stability/).** The rational function $R(z)$ computed from the tableau above.

## References
