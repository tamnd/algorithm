---
tag: 2MXQ9Z
kind: problem
slug: discrete-algebraic-riccati-equation
name: Discrete-time algebraic Riccati equation
aliases:
- DARE
area: control/optimal-and-predictive-control
level: core
summary: Find the stabilizing symmetric solution P of the fixed point equation of the discrete Riccati recursion, which gives the discrete LQR gain.
model: real-ram
prereqs: [lqr-problem, stabilizability, detectability]
see_also: [continuous-algebraic-riccati-equation, stabilizing-riccati-solution-theorem, infinite-horizon-lqr, finite-horizon-lqr, kleinman-iteration, kalman-filter, linear-mpc, zero-order-hold-discretization]
sources:
  - book: isbn:9780486457666
    title: Brian D. O. Anderson and John B. Moore, Optimal Control, Linear Quadratic Methods, Prentice Hall, 1990 (Dover reprint, 2007)
    locator: the discrete-time regulator and its Riccati equation
  - book: isbn:9781886529434
    title: Dimitri P. Bertsekas, Dynamic Programming and Optimal Control, Volume I, fourth edition, Athena Scientific, 2017
    locator: Section 3.1, Linear Systems and Quadratic Cost, with the convergence of the Riccati recursion to the algebraic equation
  - book: isbn:0134565673
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 21, Discrete Time Control
  - book: isbn:9780198537953
    title: Peter Lancaster and Leiba Rodman, Algebraic Riccati Equations, Clarendon Press, Oxford, 1995
    locator: the discrete-time equation and its symplectic matrix
  - paper: doi:10.1109/TAC.1971.1099755
    title: G. A. Hewer, An iterative technique for the computation of the steady state gains for the discrete optimal regulator, IEEE Transactions on Automatic Control 16(4), 382-384, 1971
    locator: Newton's method for the DARE, one discrete Lyapunov equation per step
  - book: isbn:9781611972085
    title: Dario A. Bini, Bruno Iannazzo and Beatrice Meini, Numerical Solution of Algebraic Riccati Equations, SIAM, 2012
    locator: the discrete-time equation, cyclic reduction and doubling
---

The discrete-time algebraic Riccati equation (DARE) is the matrix equation

$$P = A^T P A - A^T P B (R + B^T P B)^{-1} B^T P A + Q$$

in a symmetric unknown $P \in \mathbb{R}^{n \times n}$. The problem is to find its stabilizing solution: the solution for which $A - B K$ is Schur, with $K = (R + B^T P B)^{-1} B^T P A$. This $K$ is the constant optimal gain of the infinite-horizon discrete [LQR problem](/lqr-problem/), and $x_0^T P x_0$ is the optimal cost. The equation is the fixed point of the backward Riccati recursion of [finite-horizon LQR](/finite-horizon-lqr/), so running that recursion long enough is one way to solve it ([infinite-horizon LQR](/infinite-horizon-lqr/)). With $A$ and $B$ replaced by $A^T$ and $C^T$, it gives the steady-state gain of the [Kalman filter](/kalman-filter/). The continuous-time counterpart is the [CARE](/continuous-algebraic-riccati-equation/).

## In plain words

A sampled system is steered step by step, and each step costs something for the state and something for the input. The best total cost from a state is a bowl-shaped function, held by a symmetric matrix. If the horizon has no end, one step later the future looks exactly the same as now. So the matrix must reproduce itself: the cost of one step plus the best cost from the next state must give back the same matrix. That condition is the discrete Riccati equation. It has several solutions, and only one belongs to a controller that brings the state to zero. The simplest way to find it is to repeat the one-step update from zero until it stops changing. Faster methods use Newton steps or an eigenvalue problem of twice the size.

## Definition

Input: $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $Q = Q^T \ge 0$ and $R = R^T > 0$. For symmetric $P \ge 0$ the matrix $R + B^T P B$ is positive definite, and the Riccati map is

$$F(P) = Q + A^T P A - A^T P B (R + B^T P B)^{-1} B^T P A.$$

A solution is a symmetric $P$ with $P = F(P)$ and $R + B^T P B$ invertible. It is stabilizing if $A - B K$ is Schur, with $K = (R + B^T P B)^{-1} B^T P A$. Output: the stabilizing solution $P$ and the gain $K$, or the report that none exists.

**Facts about the answer.**

- The equation has a second form. With $A_K = A - B K$, a solution satisfies $P = Q + K^T R K + A_K^T P A_K$. This is a Stein (discrete Lyapunov) equation in $P$ for a fixed $K$.
- A stabilizing solution is positive semidefinite: from the second form, $P = \sum_{k \ge 0} (A_K^T)^k (Q + K^T R K) A_K^k$, and the sum converges because $A_K$ is Schur.
- There is at most one stabilizing solution. Completing the square and summing, as in Lemma 2 of the [infinite-horizon LQR proof](/infinite-horizon-lqr/), shows that $x_0^T P x_0$ is the minimal cost over all inputs with $x_k \to 0$. That minimum does not depend on $P$, and $x_0$ is arbitrary, so two stabilizing solutions are equal.
- If $(A, B)$ is stabilizable and $(Q^{1/2}, A)$ is detectable, the stabilizing solution exists. It is the only positive semidefinite solution, and the Riccati recursion from $P_0 = 0$ converges to it (the [stabilizing solution theorem](/stabilizing-riccati-solution-theorem/) and the infinite-horizon LQR page).
- With $G = B R^{-1} B^T$ and $A$ invertible, $P$ solves the DARE if and only if the column space of $\begin{bmatrix} I \\ P \end{bmatrix}$ is invariant under the symplectic matrix $Z = \begin{bmatrix} A + G A^{-T} Q & -G A^{-T} \\ -A^{-T} Q & A^{-T} \end{bmatrix}$. Its eigenvalues come in pairs $\lambda$ and $1 / \bar\lambda$, and the stabilizing solution belongs to the invariant subspace of the eigenvalues with $|\lambda| < 1$.

## Variants

- **Cross term.** For the cost $x^T Q x + 2 x^T S u + u^T R u$, the equation is $P = A^T P A - (A^T P B + S)(R + B^T P B)^{-1}(B^T P A + S^T) + Q$, and the gain is $K = (R + B^T P B)^{-1} (B^T P A + S^T)$.
- **Singular input weight.** In discrete time $R$ may be singular, provided $R + B^T P B$ stays invertible at the solution. This happens in deadbeat-like problems and in sampled-data problems with a cost that is integrated between the samples.
- **Filter form.** $\Sigma = A \Sigma A^T - A \Sigma C^T (C \Sigma C^T + V)^{-1} C \Sigma A^T + W$ for the prediction error covariance of the steady-state Kalman filter. It is the DARE of $(A^T, C^T, W, V)$.
- **No input.** With $B = 0$ the DARE is the Stein equation $P = A^T P A + Q$, and its solution is stabilizing exactly when $A$ is Schur.
- **Without A invertible.** The symplectic matrix needs $A^{-1}$. The pencil $\begin{bmatrix} A & 0 \\ -Q & I \end{bmatrix} - z \begin{bmatrix} I & G \\ 0 & A^T \end{bmatrix}$ does not. It comes from the costate equations $x_{k+1} = A x_k - G \lambda_{k+1}$ and $\lambda_k = Q x_k + A^T \lambda_{k+1}$, and the [QZ algorithm](/qz-algorithm/) handles it.
- **Discounted cost.** A discount $\gamma$ gives the DARE of $(\sqrt\gamma\, A, \sqrt\gamma\, B)$.

## Examples

**Scalar.** With $n = m = 1$ and $b \ne 0$, $F(p) = q + a^2 r p / (r + b^2 p)$. The DARE becomes the quadratic

$$b^2 p^2 + (r - q b^2 - a^2 r)\, p - q r = 0,$$

and the closed loop is $a - b K = a r / (r + b^2 p)$.

- $a = b = q = r = 1$: $p^2 - p - 1 = 0$, so $p = (1 + \sqrt 5) / 2 \approx 1.618034$, the golden ratio. $K = p / (1 + p) \approx 0.618034$ and the closed loop is $0.381966$. The other root $(1 - \sqrt 5)/2$ is negative, and its closed loop $1 / (1 + (1 - \sqrt 5)/2) \approx 2.618034$ is not Schur. The Riccati recursion from $p_0 = 0$ gives $1, 3/2, 8/5, 21/13, \dots$, ratios of Fibonacci numbers.
- $a = 2$, $b = q = r = 1$: $p^2 - 4 p - 1 = 0$, so $p = 2 + \sqrt 5 \approx 4.236068$, $K \approx 1.618034$ and the closed loop is $2 / (1 + p) \approx 0.381966$.
- $a = 2$, $b = r = 1$ and $q = 0$ (not detectable): $p^2 - 3 p = 0$. The root $p = 0$ gives the closed loop $2$. The root $p = 3$ gives $K = 3/2$ and the closed loop $1/2$, so it is the stabilizing solution. The recursion from $p_0 = 0$ stays at $0$ and never finds it.
- $a = b = r = 1$ and $q = 0$: $p^2 = 0$, and the only solution $p = 0$ gives the closed loop $1$. There is no stabilizing solution, because the mode at $1$ is unobservable and on the unit circle.

**Sampled double integrator.** The double integrator sampled with a zero-order hold of period 1 gives $A = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$ and $B = \begin{bmatrix} 1/2 \\ 1 \end{bmatrix}$. With $Q = I$ and $R = 1$, the stabilizing solution, to six decimals, is

$$P = \begin{bmatrix} 2.367101 & 1.118034 \\ 1.118034 & 2.587483 \end{bmatrix}, \qquad K = \begin{bmatrix} 0.434483 & 1.028466 \end{bmatrix},$$

where $P_{12}$ agrees with $\sqrt 5 / 2$ to 59 digits in a computation with 60 digits (a measurement). The closed loop eigenvalues are $0.377146 \pm 0.215723 i$, with modulus $0.434483$. These are the numbers of the [infinite-horizon LQR](/infinite-horizon-lqr/) example. In double precision, 22 passes of the recursion give a DARE residual of $2.9 \times 10^{-15}$ in the 2-norm.

## Known algorithms

- Value iteration: the Riccati recursion $P_{j+1} = F(P_j)$ from $P_0 = 0$ ([infinite-horizon LQR](/infinite-horizon-lqr/)). Each pass costs $O(n^3 + m^3)$. The derivative of $F$ at the solution is the map $D \mapsto A_K^T D A_K$, so the convergence is linear with ratio $\rho(A_K)^2$, where $\rho$ is the [spectral radius](/spectral-radius/). In the golden ratio example, the ratio is $0.381966^2 \approx 0.1459$.
- Hewer's method (1971), the discrete version of the [Kleinman iteration](/kleinman-iteration/): from a gain $K_0$ with $A - B K_0$ Schur, solve the Stein equation $P_k = Q + K_k^T R K_k + (A - B K_k)^T P_k (A - B K_k)$ and update $K_{k+1} = (R + B^T P_k B)^{-1} B^T P_k A$. The iterates decrease to the solution and converge quadratically.
- Schur methods: an ordered Schur form of the symplectic matrix, or an ordered QZ form of the pencil above when $A$ is singular or badly conditioned. They cost $O(n^3)$.
- Doubling and cyclic reduction. A doubling pass doubles the horizon that the recursion covers, so $k$ passes reach the horizon $2^k$, and the convergence is quadratic (see Bini, Iannazzo and Meini).

## Bounds

- Exactness (a theorem): the entries of $P$ are algebraic numbers, and $(1 + \sqrt 5)/2$ shows that they can be irrational even for integer data. There is no exact finite rational algorithm in general.
- Cost: $O(n^3 + m^3)$ arithmetic operations per pass or per Newton step with dense methods. Newton steps in Kronecker form cost $O(n^6)$ each.
- Count: as for the CARE, the solutions correspond to $n$-dimensional invariant subspaces of the symplectic matrix with a nonsingular top block, so there are at most $\binom{2n}{n}$ when its eigenvalues are distinct.
- Sensitivity (a rule of thumb): the DARE is badly conditioned when the symplectic matrix has eigenvalues close to the unit circle, that is, when the optimal closed loop is close to the edge of the unit disk.

## Reductions

- **DARE to a fixed point.** It is the fixed point of the finite-horizon recursion, so its solution is the limit of finite-horizon costs under the hypotheses above.
- **DARE to a sequence of Stein equations.** Newton's method, as in Hewer's method.
- **DARE to an eigenvalue problem.** The stabilizing solution is $P = X_2 X_1^{-1}$ for a basis $\begin{bmatrix} X_1 \\ X_2 \end{bmatrix}$ of the stable deflating subspace of the pencil, or of the stable invariant subspace of $Z$.
- **Filter to regulator.** The Kalman filter equation for $(A, C, W, V)$ is the DARE of $(A^T, C^T, W, V)$.
- **CARE and DARE.** A Cayley transform maps one into the other, under invertibility conditions, so a solver for one can solve the other.
- **Sampled-data LQR.** A continuous cost integrated between samples, with a zero-order hold input, gives a DARE with a cross term $S$ and a full weight $Q$ computed from matrix exponentials.

## Applications

- The constant gain of discrete-time LQR, used whenever the controller runs on a computer with a fixed sample time.
- The steady-state gain and error covariance of the [Kalman filter](/kalman-filter/).
- The terminal cost and the local controller of [linear MPC](/linear-mpc/): $x^T P x$ with $P$ from the DARE makes the finite-horizon cost equal the infinite-horizon cost near the origin.
- Discrete-time H2 and H-infinity synthesis, and the discrete bounded real lemma.
- Econometric and economic models with quadratic loss, where the same equation appears in linear quadratic dynamic programming.

## References
