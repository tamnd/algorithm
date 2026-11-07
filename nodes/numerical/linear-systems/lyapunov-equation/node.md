---
tag: BM6Y5D
kind: problem
slug: lyapunov-equation
name: Lyapunov equation
aliases:
- continuous Lyapunov equation
- algebraic Lyapunov equation
- Stein equation (discrete form)
area: numerical/linear-systems
level: advanced
summary: Solve AX + XA^T = -Q for X, a special case of the Sylvester equation.
model: floating-point-model
complexity:
  vars: {n: "the order of A"}
  time: {worst: Θ(n^3)}
prereqs: [sylvester-equation, positive-definite-matrix]
see_also: [schur-decomposition, cholesky-decomposition, adi-method, qr-algorithm, neumann-series, spectral-radius, eigenvalue-problem, krylov-subspace]
sources:
  - paper: doi:10.1145/361573.361582
    title: Richard H. Bartels and G. W. Stewart, Algorithm 432, Solution of the matrix equation AX + XB = C, Communications of the ACM 15(9), 1972
    locator: the Schur method, including the symmetric case B = A^T
  - paper: doi:10.1093/imanum/2.3.303
    title: S. J. Hammarling, Numerical solution of the stable, non-negative definite Lyapunov equation, IMA Journal of Numerical Analysis 2(3), 1982
    locator: computing the Cholesky factor of the solution directly from a factor of Q, for the continuous and discrete equations
  - paper: doi:10.1137/130912839
    title: Valeria Simoncini, Computational methods for linear matrix equations, SIAM Review 58(3), 2016
    locator: the Lyapunov equation in control, low-rank solutions, ADI and Krylov subspace projection methods
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 16, The Sylvester Equation (the Lyapunov equation as a special case, its perturbation theory and the accuracy of the Schur method)
---

The (continuous) Lyapunov equation asks for $X \in \mathbb{R}^{n \times n}$ with
$$A X + X A^T = -Q,$$
for given $A \in \mathbb{R}^{n \times n}$ and symmetric $Q$. It is the [Sylvester equation](/sylvester-equation/) with $B = A^T$. Lyapunov's theorem ties it to stability: if every eigenvalue of $A$ has negative real part and $Q$ is positive definite, the solution is unique, symmetric and positive definite, and conversely. Dense problems are solved in $O(n^3)$ flops by the Bartels-Stewart or Hammarling methods; large sparse ones with low-rank $Q$ by ADI and Krylov methods that return a low-rank factor of $X$.

## In plain words

A linear system that changes in time is stable if every motion dies out. The Lyapunov equation turns that question about all future times into a single matrix equation. Its solution adds up, over all time, how strongly a steady push in each direction is felt. If the system is stable the sum is finite and the solution is a well-behaved positive matrix; if not, no such solution exists. The same matrix also measures how much energy it takes to steer the system and how much of its state can be seen from outside.

## Definition

**Notation.** $\Lambda(A) = \{\lambda_i\}$; $A$ is *stable* (Hurwitz) if $\mathrm{Re}\,\lambda_i < 0$ for all $i$, and *Schur stable* if its [spectral radius](/spectral-radius/) is below $1$. $X \succ 0$ means [positive definite](/positive-definite-matrix/), $X \succeq 0$ positive semidefinite. $u = 2^{-53}$; $\hat X$ is a computed solution.

**Input.** $A$ and symmetric $Q$ (often $Q = B B^T$ with $B \in \mathbb{R}^{n \times p}$, $p \ll n$).

**Output.** $X$ with $A X + X A^T + Q = 0$.

**Solvability.** By the Sylvester theory, the solution is unique for every $Q$ if and only if $\lambda_i + \lambda_j \ne 0$ for all $i, j$; it is then symmetric whenever $Q$ is, since $X^T$ solves the same equation.

**Theorem (Lyapunov).** If $A$ is stable, then for every $Q$ the unique solution is
$$X = \int_0^\infty e^{A t} Q\, e^{A^T t}\, dt,$$
and $Q \succeq 0$ implies $X \succeq 0$, $Q \succ 0$ implies $X \succ 0$. Conversely, if for some $Q \succ 0$ there is a solution $X \succ 0$, then $A$ is stable.

*Proof sketch.* Stability makes $\|e^{At}\|$ decay exponentially, so the integral converges, and $A X + X A^T = \int_0^\infty \frac{d}{dt}\big(e^{At} Q e^{A^T t}\big)\, dt = -Q$. The integrand is $\succeq 0$ (or $\succ 0$) for every $t$. For the converse, if $A^T v = \lambda v$ with $v \ne 0$, then $-v^* Q v = v^*(A X + X A^T) v = 2\,\mathrm{Re}(\lambda)\, v^* X v$, so $\mathrm{Re}\,\lambda < 0$. $\square$

## Variants

- **Discrete Lyapunov (Stein) equation.** $A X A^T - X + Q = 0$. If $\rho(A) < 1$ the solution is $X = \sum_{k \ge 0} A^k Q (A^T)^k$, a matrix [Neumann series](/neumann-series/), and the analogue of Lyapunov's theorem holds with Schur stability.
- **The transposed equation** $A^T X + X A = -Q$, which gives the observability Gramian.
- **Generalized Lyapunov equation** $A X E^T + E X A^T = -Q$ for descriptor systems, solved through the QZ form.
- **Low-rank right side.** $Q = B B^T$ with $p \ll n$. For stable $A$ the singular values of $X$ often decay fast, and $X \approx Z Z^T$ with $Z$ of few columns.
- **Algebraic Riccati equation.** $A^T X + X A - X G X + Q = 0$; Newton's method for it solves a Lyapunov equation at each step.

## Examples

**A $2 \times 2$ stable case.** For $A = \begin{pmatrix} -1 & 1 \\ 0 & -2 \end{pmatrix}$ and $Q = I$, the unique solution is
$$X = \begin{pmatrix} 7/12 & 1/12 \\ 1/12 & 1/4 \end{pmatrix},$$
which is positive definite ($\det X = 5/36$), as Lyapunov's theorem predicts. Entry $(2,2)$ checks as $-2 \cdot \tfrac14 - 2 \cdot \tfrac14 = -1$.

**Nonnormality makes $X$ large.** For $A = \begin{pmatrix} -1 & a \\ 0 & -1 \end{pmatrix}$ and $Q = I$, both eigenvalues are $-1$, but the solution has $x_{11} = a^2/4 + 1/2$, $x_{12} = a/4$, $x_{22} = 1/2$: $\|X\|$ is $0.75$ for $a = 1$, $25.5$ for $a = 10$ and $2500.5$ for $a = 100$. The integral formula explains it: $\|e^{At}\|$ grows transiently to about $a/e$ before it decays.

**An unstable case.** For $A = (1)$, $Q = (1)$: $2x = -1$ gives $X = -\tfrac12 \prec 0$, consistent with the converse of the theorem. For $A = \mathrm{diag}(1, -1)$ the equation is singular, since $\lambda_1 + \lambda_2 = 0$.

## Known algorithms

- **Bartels-Stewart.** Real Schur form $A = U T U^T$, then $T Y + Y T^T = -U^T Q U$ by substitution, $X = U Y U^T$; about $25 n^3$ flops for the Schur form and $O(n^3)$ for the rest, with symmetry halving the triangular solve.
- **Hammarling's method (1982).** For stable $A$ and $Q = B B^T$, compute the Cholesky factor $L$ of $X = L L^T$ directly from a factor of $Q$, without forming $Q$ or $X$. The computed $X$ is then positive semidefinite by construction, which matters when $X$ is nearly singular.
- **Kronecker form.** The order $n^2$ (or $n(n+1)/2$ using symmetry) linear system, for very small $n$ only.
- **Sign function iteration.** Newton's iteration for the matrix sign function, which uses only inversions and parallelizes well on dense hardware.
- **Large sparse problems.** Low-rank [ADI](/adi-method/) with shifts (the factored form of Penzl and of Li and White), extended and rational [Krylov](/krylov-subspace/) projection, which need solves with $A - s I$ and return $Z$ with $X \approx Z Z^T$ (Simoncini, 2016).

## Bounds

- **Cost.** Dense methods need $\Theta(n^3)$ flops, the cost of a Schur decomposition; the input already has $n^2$ entries. Low-rank methods cost a number of shifted sparse solves proportional to the rank of the computed factor.
- **Residual (proved).** As for the Sylvester equation, the Schur method gives a small relative residual, $\|A\hat X + \hat X A^T + Q\|_F \le c_n\, u\, \|A\|_F \|\hat X\|_F$ for a modest $c_n$ (Higham, Chapter 16).
- **Backward error and conditioning.** Because the equation has the structure $B = A^T$, the backward error that respects the structure can exceed the relative residual; the forward error is governed by $\mathrm{sep}(A, -A^T)$, which for nonnormal stable $A$ can be much smaller than $2\min_i|\mathrm{Re}\,\lambda_i|$, as in the example with large $a$.
- **Definiteness in floating point.** For nearly singular $X \succeq 0$, the Bartels-Stewart $\hat X$ may have small negative eigenvalues of order $u\|X\|$; Hammarling's factored form avoids this.
- **Decay of singular values.** For stable normal $A$ and rank-$p$ $Q$, the singular values of $X$ decay geometrically at a rate set by the spread of the spectrum, which justifies low-rank methods; for nonnormal $A$ the decay can be slower (observed, with bounds in special cases).

## Reductions

- **To the Sylvester equation:** $B = A^T$, $C = -Q$.
- **To a linear system:** $(I \otimes A + A \otimes I)\,\mathrm{vec}(X) = -\mathrm{vec}(Q)$, of order $n^2$.
- **Continuous to discrete:** the Cayley transform $A_d = (I - A)^{-1}(I + A)$ maps a stable $A$ to a Schur stable $A_d$ and the continuous equation to a Stein equation with $Q_d = 2 (I - A)^{-1} Q (I - A)^{-T}$.
- **Stability testing:** deciding whether $A$ is stable reduces to solving the equation with $Q = I$ and testing $X \succ 0$, for instance by attempting a [Cholesky decomposition](/cholesky-decomposition/), though computing eigenvalues is usually simpler and more reliable.

## Applications

- **Stability and Lyapunov functions.** $V(x) = x^T X^{-1} x$, or $x^T P x$ with $A^T P + P A = -Q$, is a quadratic Lyapunov function for $\dot x = A x$.
- **Gramians.** For $\dot x = A x + B u$, $y = C x$, the controllability Gramian solves $A W + W A^T + B B^T = 0$ and the observability Gramian $A^T W + W A + C^T C = 0$; they measure the energy needed to reach a state and the energy a state produces.
- **Model reduction.** Balanced truncation uses both Gramians to discard states that are hard to reach and hard to observe, with an a priori error bound.
- **Covariance of linear stochastic systems.** The stationary covariance of $dx = A x\, dt + B\, dw$ solves the Lyapunov equation with $Q = B B^T$.
- **Norms of systems.** The $H_2$ norm of a transfer function is $\sqrt{\mathrm{trace}(C W C^T)}$ with $W$ the controllability Gramian.

## References
