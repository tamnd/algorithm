---
tag: 6VY8RZ
kind: problem
slug: continuous-algebraic-riccati-equation
name: Continuous-time algebraic Riccati equation
aliases:
- CARE
area: control/optimal-and-predictive-control
level: core
summary: Find a symmetric P with A^T P + PA - PBR^(-1)B^T P + Q = 0 such that A - BR^(-1)B^T P is Hurwitz.
model: real-ram
prereqs: [lqr-problem, lyapunov-equation, stabilizability, detectability]
see_also: [discrete-algebraic-riccati-equation, stabilizing-riccati-solution-theorem, hamiltonian-matrix, schur-method-riccati, kleinman-iteration, infinite-horizon-lqr, kalman-bucy-filter, dgkf-h-infinity-synthesis]
sources:
  - paper: doi:10.1137/0306044
    title: W. M. Wonham, On a matrix Riccati equation of stochastic control, SIAM Journal on Control 6(4), 681-697, 1968
    locator: the algebraic Riccati equation of the regulator and its positive semidefinite solution
  - paper: "Vladimír Kučera, A contribution to matrix quadratic equations, IEEE Transactions on Automatic Control 17(3), 344-347, 1972"
    locator: the existence and uniqueness of the stabilizing solution under stabilizability and detectability
  - book: isbn:9780198537953
    title: Peter Lancaster and Leiba Rodman, Algebraic Riccati Equations, Clarendon Press, Oxford, 1995
    locator: the continuous-time equation, its Hermitian solutions and their order
  - book: isbn:0134565673
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 13, Algebraic Riccati Equations
  - paper: doi:10.1109/TAC.1979.1102178
    title: Alan J. Laub, A Schur method for solving algebraic Riccati equations, IEEE Transactions on Automatic Control 24(6), 913-921, 1979
    locator: the computation of the stabilizing solution from an ordered Schur form of the Hamiltonian matrix
  - book: isbn:9781611972085
    title: Dario A. Bini, Bruno Iannazzo and Beatrice Meini, Numerical Solution of Algebraic Riccati Equations, SIAM, 2012
    locator: the survey of solution methods, with Newton, doubling and the matrix sign function
---

The continuous-time algebraic Riccati equation (CARE) is the matrix equation

$$A^T P + P A - P B R^{-1} B^T P + Q = 0$$

in a symmetric unknown $P \in \mathbb{R}^{n \times n}$. The problem is to find its stabilizing solution: the solution for which $A - B R^{-1} B^T P$ is Hurwitz. This solution gives the optimal gain $K = R^{-1} B^T P$ of the infinite-horizon [LQR problem](/lqr-problem/) and the optimal cost $x_0^T P x_0$. The same equation, with $A$ and $B$ replaced by $A^T$ and $C^T$, gives the gain of the steady-state [Kalman-Bucy filter](/kalman-bucy-filter/). The CARE is quadratic in $P$, so it can have many solutions or none. The [stabilizing solution theorem](/stabilizing-riccati-solution-theorem/) gives when the stabilizing one exists, and the [Hamiltonian matrix](/hamiltonian-matrix/) gives all solutions in terms of its invariant subspaces. The discrete-time counterpart is the [DARE](/discrete-algebraic-riccati-equation/).

## In plain words

For a linear system with a quadratic cost, the best cost from any state is a bowl-shaped function of the state, and a symmetric matrix holds its shape. This matrix must satisfy one balance condition: the rate at which the cost falls along the best motion must equal the cost being paid at that moment. Written out, that condition is the Riccati equation. It is quadratic in the unknown matrix, like the scalar equation for the roots of a parabola, so there are usually several solutions. Only one of them belongs to a controller that brings the state back to zero. That one is the answer to look for. Numerical methods find it by a matrix eigenvalue problem of twice the size, or by a sequence of linear matrix equations.

## Definition

Input: $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $Q = Q^T \ge 0$ and $R = R^T > 0$. Write $G = B R^{-1} B^T$, which is symmetric and positive semidefinite. The Riccati map is

$$\mathcal{R}(P) = A^T P + P A - P G P + Q.$$

A solution is a symmetric $P$ with $\mathcal{R}(P) = 0$. It is stabilizing if $A - G P$ is Hurwitz. Output: the stabilizing solution $P$ and the gain $K = R^{-1} B^T P$, or the report that no stabilizing solution exists.

**Facts about the answer.**

- There is at most one stabilizing solution. If $P_1$ and $P_2$ are both stabilizing, the difference $D = P_1 - P_2$ satisfies $(A - G P_1)^T D + D (A - G P_2) = 0$. This is a Sylvester equation whose two coefficient matrices are both Hurwitz, so its only solution is $D = 0$.
- If $(A, B)$ is stabilizable and $(Q^{1/2}, A)$ is detectable, the stabilizing solution exists and is positive semidefinite ([Kučera 1972](/stabilizing-riccati-solution-theorem/)). It is then the only positive semidefinite solution.
- The stabilizing solution, when it exists, is the largest symmetric solution: $P \ge X$ for every symmetric $X$ with $\mathcal{R}(X) = 0$. Proof: with $D = X - P$, the identity $\mathcal{R}(X) = \mathcal{R}(P) + (A - GP)^T D + D (A - GP) - D G D$ gives $(A - GP)^T D + D (A - GP) = D G D \ge 0$, and a Lyapunov equation with a Hurwitz matrix and a positive semidefinite right side has a solution $D \le 0$.
- $P$ solves the CARE if and only if the column space of $\begin{bmatrix} I \\ P \end{bmatrix}$ is invariant under the Hamiltonian matrix $H = \begin{bmatrix} A & -G \\ -Q & -A^T \end{bmatrix}$. Indeed $H \begin{bmatrix} I \\ P \end{bmatrix} = \begin{bmatrix} I \\ P \end{bmatrix} (A - G P)$ is the same as $-Q - A^T P = P A - P G P$. The stabilizing solution belongs to the stable invariant subspace of $H$.

## Variants

- **Cross term.** For the cost $x^T Q x + 2 x^T S u + u^T R u$, the equation is $A^T P + P A - (P B + S) R^{-1} (B^T P + S^T) + Q = 0$, and the gain is $K = R^{-1} (B^T P + S^T)$. It is the CARE of the data $A - B R^{-1} S^T$ and $Q - S R^{-1} S^T$.
- **Indefinite quadratic term.** In [H-infinity control](/h-infinity-control-problem/) and the [bounded real lemma](/bounded-real-lemma/), the matrix $G$ is $B_2 B_2^T - \gamma^{-2} B_1 B_1^T$ or a similar difference, which need not be positive semidefinite. The stabilizing solution is still read from the Hamiltonian matrix, but the positive semidefinite theory of this page does not apply.
- **Riccati inequality.** $\mathcal{R}(P) \ge 0$, which is an [LMI](/linear-matrix-inequality/) in $P$ after a Schur complement. When the stabilizing solution exists, the same identity shows that it bounds every solution of the inequality from above.
- **Generalized CARE.** With a descriptor matrix $E$, the equation is $A^T P E + E^T P A - E^T P G P E + Q = 0$, solved through a [generalized eigenvalue problem](/generalized-eigenvalue-problem/).
- **Riccati differential equation.** $-\dot P = \mathcal{R}(P)$ with a terminal value. It is the finite-horizon version ([finite-horizon LQR](/finite-horizon-lqr/)), and the CARE is its equilibrium.
- **Filter form.** $A P + P A^T - P C^T V^{-1} C P + W = 0$ for the error covariance of the Kalman-Bucy filter. It is the CARE of $(A^T, C^T, W, V)$.

## Examples

**Scalar.** With $n = m = 1$ the CARE is $(b^2 / r) p^2 - 2 a p - q = 0$. For $b \ne 0$ the roots are

$$p = \frac{r}{b^2} \left( a \pm \sqrt{a^2 + b^2 q / r} \right), \qquad a - \frac{b^2}{r} p = \mp \sqrt{a^2 + b^2 q / r}.$$

The plus sign gives the stabilizing solution. For $a = b = q = r = 1$, $p = 1 + \sqrt 2 \approx 2.414214$, the gain is $1 + \sqrt 2$ and the closed loop is $-\sqrt 2$. The other root $1 - \sqrt 2$ is negative and gives the closed loop $+\sqrt 2$.

**Double integrator.** With $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $Q = I$, $R = 1$ and $P = \begin{bmatrix} p_1 & p_2 \\ p_2 & p_3 \end{bmatrix}$, the three entries of the CARE are $1 - p_2^2 = 0$, $p_1 - p_2 p_3 = 0$ and $2 p_2 - p_3^2 + 1 = 0$. The choice $p_2 = -1$ gives $p_3^2 = -1$, so there is no real solution with it. The choice $p_2 = 1$ gives $p_3 = \pm \sqrt 3$ and $p_1 = p_3$. So the equation has exactly two real symmetric solutions:

$$P_+ = \begin{bmatrix} \sqrt 3 & 1 \\ 1 & \sqrt 3 \end{bmatrix}, \qquad P_- = \begin{bmatrix} -\sqrt 3 & 1 \\ 1 & -\sqrt 3 \end{bmatrix}.$$

$P_+$ is positive definite and gives $K = \begin{bmatrix} 1 & \sqrt 3 \end{bmatrix}$ and the closed loop polynomial $s^2 + \sqrt 3\, s + 1$, which is Hurwitz. $P_-$ is negative definite and gives $s^2 - \sqrt 3\, s + 1$, with both roots in the right half plane. As the order statement says, $P_+ - P_- = 2 \sqrt 3\, I \ge 0$.

**No quadratic term.** With $B = 0$ the CARE is the [Lyapunov equation](/lyapunov-equation/) $A^T P + P A + Q = 0$, and the stabilizing solution exists exactly when $A$ is Hurwitz. For $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$ and $Q = I$, the solution is $P = \begin{bmatrix} 5/4 & 1/4 \\ 1/4 & 1/4 \end{bmatrix}$.

**No detectability.** For $a = 1$, $b = r = 1$ and $q = 0$, the CARE is $2 p - p^2 = 0$. Both $p = 0$ and $p = 2$ are positive semidefinite solutions. Only $p = 2$ is stabilizing (closed loop $-1$), and $p = 0$ leaves the closed loop at $+1$. So positive semidefinite does not imply stabilizing when detectability fails.

**No stabilizing solution.** For $a = 0$, $b = r = 1$ and $q = 0$, the CARE is $-p^2 = 0$. The only solution is $p = 0$, with closed loop $0$, which is not Hurwitz. Here $(q^{1/2}, a)$ has an unobservable mode on the imaginary axis.

## Known algorithms

- [Schur method](/schur-method-riccati/) (Laub 1979): compute an ordered Schur form of the Hamiltonian matrix, take the first $n$ Schur vectors $\begin{bmatrix} U_1 \\ U_2 \end{bmatrix}$, and set $P = U_2 U_1^{-1}$. It costs $O(n^3)$ operations and is the usual dense method. When $R$ is badly conditioned, the QZ form of an extended pencil avoids forming $R^{-1}$ (Van Dooren, 1981; see the [QZ algorithm](/qz-algorithm/)).
- [Kleinman iteration](/kleinman-iteration/): Newton's method on $\mathcal{R}$. Each step solves a [Lyapunov equation](/lyapunov-equation/); from a stabilizing start the iterates decrease to $P$ and converge quadratically. It is also used to refine the result of the Schur method.
- [Infinite-horizon LQR](/infinite-horizon-lqr/) by the Riccati differential equation integrated to steady state. It is simple but slow: the convergence is linear, and the slowest closed loop pole sets its rate.
- The matrix sign function of $H$ and structure-preserving doubling, both with quadratic convergence (see Bini, Iannazzo and Meini).
- For large sparse $A$ with few inputs and low rank $Q$, low-rank Newton methods with ADI or Krylov solvers for the Lyapunov steps compute a low-rank factor of $P$.

## Bounds

- Count (a theorem): every solution, symmetric or not, corresponds to an $n$-dimensional invariant subspace of $H$ with a nonsingular top block. If the $2n$ eigenvalues of $H$ are distinct, $H$ has $\binom{2n}{n}$ invariant subspaces of dimension $n$, so the CARE has at most $\binom{2n}{n}$ solutions, real or complex.
- Exactness (a theorem): the entries of $P$ are algebraic numbers, often irrational, as $1 + \sqrt 2$ shows. No finite rational algorithm gives $P$ exactly in general, and the methods above are iterative.
- Cost: the dense methods use $O(n^3)$ arithmetic operations. Kleinman's method uses $O(n^3)$ per step with the Bartels-Stewart method for the Lyapunov equation, or $O(n^6)$ per step if the Lyapunov equation is solved in Kronecker form.
- Sensitivity (a theorem on an example): take $a = 0$, $b = r = 1$ and $q = \varepsilon > 0$. Then $p = \sqrt\varepsilon$ and $dp / dq = 1 / (2 \sqrt\varepsilon)$, which grows without bound as $\varepsilon \to 0$. The closed loop pole $-\sqrt\varepsilon$ and the eigenvalues $\pm \sqrt\varepsilon$ of $H$ approach the imaginary axis at the same time. In general (a rule of thumb), the CARE is badly conditioned when the Hamiltonian matrix has eigenvalues close to the imaginary axis.

## Reductions

- **CARE to an eigenvalue problem.** The stabilizing solution is $P = X_2 X_1^{-1}$ for any basis $\begin{bmatrix} X_1 \\ X_2 \end{bmatrix}$ of the stable invariant subspace of $H$. This is the base of the Schur method and the sign function method.
- **CARE to a sequence of Lyapunov equations.** Newton's method: $(A - G P_k)^T P_{k+1} + P_{k+1} (A - G P_k) = -(Q + P_k G P_k)$.
- **Filter to regulator.** The filter equation for $(A, C, W, V)$ is the CARE of $(A^T, C^T, W, V)$, so one solver serves both.
- **CARE to DARE.** A bilinear (Cayley) change of variables turns a CARE into a DARE with the same solution, under invertibility conditions. The [bilinear transform](/bilinear-transform/) is the map on the variable $s$.
- **H2 and H-infinity synthesis to CAREs.** The [H2](/h2-optimal-control/) controller needs two CAREs, one for the regulator and one for the filter. The [DGKF H-infinity](/dgkf-h-infinity-synthesis/) controller needs two Riccati equations with indefinite quadratic terms and a coupling condition.

## Applications

- The constant gain of [infinite-horizon LQR](/infinite-horizon-lqr/), and the regulator half of [LQG control](/lqg-control/).
- The steady-state gain of the [Kalman-Bucy filter](/kalman-bucy-filter/), which is the dual of the regulator.
- The bounded real and positive real lemmas, where a Riccati equation or inequality certifies a bound on the H-infinity norm or passivity.
- Spectral factorization of a positive para-Hermitian matrix function, used in Wiener filtering.
- LQG balanced truncation, which balances the solutions of the regulator and the filter CAREs in place of the Gramians, and the terminal cost of [model predictive control](/mpc-stability-theorem/) for continuous-time plants.

## References
