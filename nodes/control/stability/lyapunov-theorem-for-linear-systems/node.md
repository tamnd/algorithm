---
tag: QCRCV8
kind: theorem
slug: lyapunov-theorem-for-linear-systems
name: Lyapunov theorem for linear systems
aliases:
- Lyapunov matrix equation stability test
area: control/stability
level: core
summary: A is Hurwitz if and only if for each positive definite Q the equation A^T P + PA = -Q has a positive definite solution P. The solution is then unique.
prereqs: [hurwitz-matrix, lyapunov-equation, lyapunov-function]
see_also: [lyapunov-equation, hurwitz-matrix, lyapunov-direct-method, lyapunov-indirect-method, exponential-stability, observability-gramian, linear-matrix-inequality, routh-hurwitz-criterion]
sources:
  - paper: doi:10.1080/00207179208934253
    title: "A. M. Lyapunov, The general problem of the stability of motion, translated by A. T. Fuller, International Journal of Control 55(3), 531-773, 1992"
    locator: the second method applied to linear equations with constant coefficients, where the quadratic form is found from a linear system of equations
  - paper: doi:10.1115/1.3662604
    title: "R. E. Kalman and J. E. Bertram, Control system analysis and design via the second method of Lyapunov: I, continuous-time systems, Journal of Basic Engineering 82(2), 371-393, 1960"
    locator: stability of linear stationary systems and the estimate of transient behavior from a quadratic Lyapunov function
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 4.3, Linear Systems and Linearization (the Lyapunov equation, the integral formula for P and the proof)
  - paper: doi:10.1016/0022-247X(62)90030-6
    title: A. Ostrowski and H. Schneider, Some theorems on the inertia of general matrices, Journal of Mathematical Analysis and Applications 4, 72-84, 1962
    locator: the inertia theorem for the Lyapunov equation
  - book: isbn:9780521467131
    title: Roger A. Horn and Charles R. Johnson, Topics in Matrix Analysis, Cambridge University Press, 1991
    locator: Chapter 2, Stable matrices and inertia
---

This theorem says that a real square matrix $A$ is [Hurwitz](/hurwitz-matrix/), with every eigenvalue in the open left half plane, exactly when the linear matrix equation $A^T P + P A = -Q$ has a symmetric positive definite solution $P$ for a symmetric positive definite $Q$. The theorem is a stability test: it turns a question about eigenvalues into a linear system for the entries of $P$ and a check that $P > 0$. The [Lyapunov equation](/lyapunov-equation/) page is about the equation itself, as a problem of numerical linear algebra, and about the algorithms that solve it; that page writes the equation in the transposed form $A X + X A^T = -Q$. This page is about what the solution says about $A$. It also gives the quadratic [Lyapunov function](/lyapunov-function/) $V(x) = x^T P x$ for $\dot x = A x$.

## Statement

Here $P > 0$ means that $P$ is symmetric positive definite, and $Q \ge 0$ means symmetric positive semidefinite.

**Theorem.** For $A \in \mathbb{R}^{n \times n}$ the following are equivalent.

1. $A$ is Hurwitz: $\operatorname{Re} \lambda < 0$ for every eigenvalue $\lambda$ of $A$.
2. There are symmetric matrices $P > 0$ and $Q > 0$ with $A^T P + P A = -Q$.
3. For every symmetric $Q > 0$ the equation $A^T P + P A = -Q$ has exactly one solution $P$, and this $P$ is symmetric positive definite.

When $A$ is Hurwitz, the solution for any symmetric $Q$ is

$$P = \int_0^\infty e^{A^T t}\, Q\, e^{A t}\, dt .$$

**Theorem (observable form).** Let $C \in \mathbb{R}^{p \times n}$ and let the pair $(A, C)$ be [observable](/observability/). Then $A$ is Hurwitz if and only if $A^T P + P A = -C^T C$ has a solution $P > 0$. The solution is then unique, and it is the [observability Gramian](/observability-gramian/) $\int_0^\infty e^{A^T t} C^T C e^{A t}\, dt$.

## In plain words

To check whether a linear system settles down, one would normally compute all the eigenvalues of its matrix. The theorem gives another way. Pick any positive weight, for example the identity. Solve one linear system of equations for an unknown symmetric matrix. Then check whether the answer is positive definite, which is a simple factorization. If it is, the system settles down from every starting state, and the answer also gives an energy-like quantity that falls along every motion. If the answer is not positive definite, or if the equations have no unique answer, the system does not settle down. No eigenvalue is needed for any step. The answer also measures the total weighted energy of the motion from each starting state, summed over all time.

## Proof

**Two facts.** For a real matrix, $A^T = A^*$. For any $n \times n$ matrix $X$, the product rule gives

$$\frac{d}{dt}\left(e^{A^T t} X e^{A t}\right) = e^{A^T t} \left(A^T X + X A\right) e^{A t} . \tag{1}$$

**$1 \Rightarrow 3$.** Let $A$ be Hurwitz and $Q > 0$. By the [Hurwitz matrix](/hurwitz-matrix/) page there are $k \ge 1$ and $\lambda > 0$ with $\|e^{At}\| \le k e^{-\lambda t}$, so the integrand of $P$ is bounded in norm by $k^2 \|Q\| e^{-2\lambda t}$, and the integral converges. $P$ is symmetric because the integrand is.

*$P$ solves the equation.* By (1) with $X = Q$,

$$A^T P + P A = \int_0^\infty \frac{d}{dt}\left(e^{A^T t} Q e^{A t}\right) dt = \lim_{T \to \infty} e^{A^T T} Q e^{A T} - Q = -Q .$$

*$P$ is positive definite.* For $x \ne 0$, $x^T P x = \int_0^\infty (e^{At} x)^T Q (e^{At} x)\, dt$. The integrand is continuous and nonnegative, and it is positive at $t = 0$ since $x^T Q x > 0$. So $x^T P x > 0$.

*Uniqueness.* If $P_1$ and $P_2$ are solutions, $X = P_1 - P_2$ satisfies $A^T X + X A = 0$. By (1), $e^{A^T t} X e^{At}$ is constant, so it equals its value $X$ at $t = 0$. It also tends to $0$ as $t \to \infty$. So $X = 0$.

**$3 \Rightarrow 2$.** Take $Q = I$.

**$2 \Rightarrow 1$.** Let $A v = \lambda v$ with $v \in \mathbb{C}^n$, $v \ne 0$. Then $v^* A^T = v^* A^* = \bar\lambda v^*$, and

$$-v^* Q v = v^* (A^T P + P A) v = (\bar\lambda + \lambda)\, v^* P v = 2 \operatorname{Re} \lambda \; v^* P v .$$

Both $v^* Q v$ and $v^* P v$ are positive, because $P$ and $Q$ are real symmetric positive definite. So $\operatorname{Re} \lambda < 0$. $\blacksquare$

**The observable form.** If $A$ is Hurwitz, the same integral with $Q = C^T C$ solves the equation, and the uniqueness argument is the same. For $x \ne 0$, $x^T P x = \int_0^\infty |C e^{At} x|^2\, dt$. This is $0$ only if $C e^{At} x = 0$ for all $t \ge 0$; the derivatives at $t = 0$ then give $C A^k x = 0$ for all $k$, which observability excludes. So $P > 0$. Conversely, let $P > 0$ solve the equation, and let $A v = \lambda v$ with $v \ne 0$. The computation above gives $2 \operatorname{Re} \lambda \; v^* P v = -|C v|^2$. By the [Popov-Belevitch-Hautus test](/popov-belevitch-hautus-test/), observability means $C v \ne 0$ for every eigenvector $v$. So $\operatorname{Re} \lambda < 0$. $\blacksquare$

The integral formula and this proof follow Khalil (2002, Section 4.3).

## Consequences

**A quadratic Lyapunov function.** For $\dot x = A x$ and $V(x) = x^T P x$, $\dot V = x^T (A^T P + P A) x = -x^T Q x$. So the theorem says that a linear system with a Hurwitz matrix always has a quadratic, radially unbounded, strict Lyapunov function, and that a quadratic one is never missing when the system is asymptotically stable. With $\lambda_{\min}(P) |x|^2 \le V \le \lambda_{\max}(P) |x|^2$ it gives the explicit bound

$$|x(t)| \le \sqrt{\lambda_{\max}(P) / \lambda_{\min}(P)}\; e^{-\lambda_{\min}(Q) t / (2 \lambda_{\max}(P))}\, |x(0)| ,$$

as on [exponential stability](/exponential-stability/). Kalman and Bertram (1960) used such bounds to estimate transients.

**The indirect method.** The same $P$, computed for the Jacobian $A$ of a nonlinear system at an equilibrium, is a strict Lyapunov function for the nonlinear system near that equilibrium. That is the proof of [Lyapunov's indirect method](/lyapunov-indirect-method/).

**A test with linear algebra only.** For a symmetric $P$ the equation is a linear system of $n(n+1)/2$ equations in $n(n+1)/2$ unknowns. Its matrix in Kronecker form is $I \otimes A^T + A^T \otimes I$ (see [Kronecker product](/kronecker-product/)), whose eigenvalues are the sums $\lambda_i + \lambda_j$ of eigenvalues of $A$. So the equation has a unique solution for every $Q$ exactly when no two eigenvalues of $A$ add up to $0$. To decide Hurwitz, solve the equation for $Q = I$ and test $P > 0$ with a [Cholesky decomposition](/cholesky-decomposition/). Methods that solve the equation in $O(n^3)$ operations are on the [Lyapunov equation](/lyapunov-equation/) page. In exact arithmetic the test gives the same answer as the [Routh-Hurwitz criterion](/routh-hurwitz-criterion/) on the characteristic polynomial, and it avoids forming that polynomial, which can be badly conditioned.

**Inertia.** The theorem is a special case of the inertia theorem of Ostrowski and Schneider (1962). If $A^T P + P A = -Q$ with $Q > 0$ and $P$ symmetric, then $A$ has no eigenvalue on the imaginary axis, $P$ is nonsingular, and the number of eigenvalues of $A$ with negative real part equals the number of positive eigenvalues of $P$; the same holds for positive real parts and negative eigenvalues. So an indefinite solution counts the unstable modes. For $A = \operatorname{diag}(1, -2)$ and $Q = I$, $P = \operatorname{diag}(-1/2, 1/4)$: one negative eigenvalue of $P$, and one eigenvalue of $A$ in the right half plane.

**Inequalities.** Condition 2 can be weakened to the strict matrix inequality $A^T P + P A < 0$ with $P > 0$, which is the same thing with $Q = -(A^T P + P A)$. In this form one $P$ can be searched for that works for several matrices at once, which is a [linear matrix inequality](/linear-matrix-inequality/) problem; see [quadratic stability](/quadratic-stability/) and [common Lyapunov function](/common-lyapunov-function/).

**Discrete time.** For $x_{k+1} = A x_k$ the analogue is the equation $A^T P A - P = -Q$: the [spectral radius](/spectral-radius/) of $A$ is less than 1 if and only if this equation has a solution $P > 0$ for some (and then every) $Q > 0$. The proof is the same, with the sum $\sum_{k \ge 0} (A^T)^k Q A^k$ in place of the integral and $(|\lambda|^2 - 1) v^* P v = -v^* Q v$ in place of the eigenvector step.

## Tightness

**The example with numbers.** For $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$ and $Q = I$, write $P = \begin{bmatrix} p_1 & p_2 \\ p_2 & p_3 \end{bmatrix}$. The three distinct entries of $A^T P + P A = -I$ give

$$-4 p_2 = -1, \qquad p_1 - 3 p_2 - 2 p_3 = 0, \qquad 2 p_2 - 6 p_3 = -1 ,$$

so $p_2 = 1/4$, $p_3 = 1/4$, $p_1 = 5/4$. Then $p_1 > 0$ and $\det P = 5/16 - 1/16 = 1/4 > 0$, so $P > 0$, and $A$ is Hurwitz (its eigenvalues are $-1$ and $-2$). With $C = \begin{bmatrix} 1 & 0 \end{bmatrix}$ and $Q = C^T C = \operatorname{diag}(1, 0)$, the solution is $P = \begin{bmatrix} 11/12 & 1/4 \\ 1/4 & 1/12 \end{bmatrix}$, with $\det P = 1/72 > 0$; this is the observable form, because $C A = \begin{bmatrix} 0 & 1 \end{bmatrix}$.

**Semidefinite $Q$ without observability.** The condition $Q > 0$ in statement 2 cannot be weakened to $Q \ge 0$ alone. For $A = \operatorname{diag}(0, -1)$, $P = I$ and $Q = \operatorname{diag}(0, 2)$, the equation $A^T P + P A = -Q$ holds with $P > 0$, but $A$ has the eigenvalue $0$. The pair $(A, C)$ with $C^T C = Q$ is not observable, since the mode $0$ is not seen. In the other direction, for the Hurwitz matrix $A = -I$ and $Q = \operatorname{diag}(1, 0)$ the unique solution is $P = \operatorname{diag}(1/2, 0)$, which is not positive definite.

**A solution that is not definite.** When $A$ is not Hurwitz, the equation can still have a unique solution, but that solution is not positive definite, as in the inertia example $A = \operatorname{diag}(1, -2)$, $P = \operatorname{diag}(-1/2, 1/4)$. So the test must check $P > 0$; solving the equation is not enough.

**No solution.** For the rotation $A = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}$, $A^T = -A$ and $A^T P + P A = P A - A P$, which has trace $0$. So $A^T P + P A = -I$, with trace $-2$, has no solution. Here the eigenvalues $\pm i$ add up to $0$.

**The choice of $Q$ does not matter, the choice of $V$ does.** Statement 3 holds for every $Q > 0$, but a guessed $P$ need not work: for the same Hurwitz $A$, $P = I$ gives $A^T + A = \begin{bmatrix} 0 & -1 \\ -1 & -6 \end{bmatrix}$, which is indefinite. One must solve for $P$ from $Q$, not choose $P$ first.

**Time-varying systems.** The theorem has no frozen-time version. For $\dot x = A(t) x$, a Hurwitz $A(t)$ at every $t$ does not make the origin asymptotically stable; see [linear time-varying system](/linear-time-varying-system/).

## History

Lyapunov's thesis of 1892 already treated linear equations with constant coefficients by the second method: he showed that for a system whose characteristic roots have negative real parts, a quadratic form with a prescribed derivative can be found from a system of linear equations, and that it is definite. The result became a standard tool of control engineering with the papers of Kalman and Bertram (1960), which also gave the discrete-time form and the transient bounds. Ostrowski and Schneider (1962) extended it to the inertia theorem for matrices that are not Hurwitz. Since the 1990s the inequality form $A^T P + P A < 0$ has been the starting point of methods based on linear matrix inequalities and [semidefinite programming](/semidefinite-programming/).

## References
