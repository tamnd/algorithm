---
tag: 1GNVWG
kind: algorithm
slug: kleinman-iteration
name: Kleinman iteration
aliases:
- Newton-Kleinman method
- Newton method for the Riccati equation
area: control/optimal-and-predictive-control
level: advanced
summary: Solves the algebraic Riccati equation by Newton's method, each step a Lyapunov equation, from a stabilizing initial gain.
solves: [continuous-algebraic-riccati-equation, discrete-algebraic-riccati-equation]
model: real-ram
complexity:
  vars: {n: the number of states, m: the number of inputs, k: the number of Newton steps}
  time: {worst: "O(k (n^6 + m^3))", bartels_stewart: "O(k (n^3 + m^3))"}
  space: {extra: "O(n^4 + m^2)"}
properties: {deterministic: true, exact: false, recursive: false, iterative: true}
history:
  year: 1968
  people: [David L. Kleinman]
  note: "Kleinman (1968) gave the iteration for the continuous-time equation and proved monotone convergence; Hewer (1971) gave the discrete-time version."
prereqs: [continuous-algebraic-riccati-equation, lyapunov-equation, newton-method-for-systems, kronecker-product]
see_also: [schur-method-riccati, stabilizing-riccati-solution-theorem, infinite-horizon-lqr, discrete-algebraic-riccati-equation, policy-iteration, quadratic-convergence, lyapunov-theorem-for-linear-systems, sylvester-equation]
sources:
  - paper: doi:10.1109/TAC.1968.1098829
    title: David L. Kleinman, On an iterative technique for Riccati equation computations, IEEE Transactions on Automatic Control 13(1), 114-115, 1968
    locator: the iteration, the stability of each gain and the monotone convergence
  - paper: doi:10.1109/TAC.1971.1099755
    title: G. A. Hewer, An iterative technique for the computation of the steady state gains for the discrete optimal regulator, IEEE Transactions on Automatic Control 16(4), 382-384, 1971
    locator: the discrete-time iteration with one discrete Lyapunov equation per step
  - book: isbn:9780198537953
    title: Peter Lancaster and Leiba Rodman, Algebraic Riccati Equations, Clarendon Press, Oxford, 1995
    locator: the Newton method for the continuous and the discrete equation
  - book: isbn:9781611972085
    title: Dario A. Bini, Bruno Iannazzo and Beatrice Meini, Numerical Solution of Algebraic Riccati Equations, SIAM, 2012
    locator: the chapter on Newton's method and its convergence
---

Kleinman iteration solves the [continuous algebraic Riccati equation](/continuous-algebraic-riccati-equation/) (CARE) $A^T P + P A - P B R^{-1} B^T P + Q = 0$ for its stabilizing solution by Newton's method. It starts from a gain $K_0$ that makes $A - B K_0$ Hurwitz. Each step computes the cost matrix $P_k$ of the current gain by one [Lyapunov equation](/lyapunov-equation/) and then sets the new gain $K_{k+1} = R^{-1} B^T P_k$. The cost matrices decrease monotonically to the solution, every gain on the way is stabilizing, and the convergence is quadratic. Hewer's version does the same for the [discrete algebraic Riccati equation](/discrete-algebraic-riccati-equation/) with a discrete Lyapunov equation per step. The method needs a stabilizing start, which the [Schur method](/schur-method-riccati/) does not. In return each step is a linear problem, and a good start gives the solution in a few steps. In the language of dynamic programming, it is [policy iteration](/policy-iteration/) for the infinite-horizon [LQR problem](/lqr-problem/).

## In plain words

You already have a controller that keeps the system stable, but it is not optimal. First measure how much it costs: for a linear controller and a quadratic cost, the cost from every start state is held in one matrix, and that matrix solves a linear equation. Then design the controller that would be best if this cost matrix were the true one. The new controller is never worse, and it is still stable. Measure its cost, improve again, and repeat. Each round fixes most of the remaining error, so the number of correct digits roughly doubles per round once you are close.

## The problem

Input: real matrices $A$ ($n \times n$), $B$ ($n \times m$), $Q = Q^T \ge 0$, $R = R^T > 0$, and a gain $K_0$ ($m \times n$) with $A - B K_0$ Hurwitz. Assume that $(Q^{1/2}, A)$ is [detectable](/detectability/). Output: the stabilizing solution $P$ of the CARE and the optimal gain $K = R^{-1} B^T P$. The existence of $K_0$ means that $(A, B)$ is [stabilizable](/stabilizability/), so by the [stabilizing solution theorem](/stabilizing-riccati-solution-theorem/) the stabilizing solution exists; the proof of this page also shows it directly.

## The algorithm

```pseudo id=main
KLEINMAN-ITERATION(A, B, Q, R, K_0)
L1  K ← K_0                                        ▷ A - B K_0 must be Hurwitz
L2  for k ← 0, 1, 2, ...
L3      A_k ← A - B K
L4      solve A_k^T P + P A_k + Q + K^T R K = 0 for P   ▷ Lyapunov equation
L5      K ← R^(-1) B^T P
L6      if P is close to the previous P then return P, K
```

Line L1 takes the starting gain. The code checks that $A - B K_0$ is Hurwitz from the roots of its characteristic polynomial and stops with an error otherwise. Line L3 forms the closed loop matrix of the current gain. Line L4 computes $P_k$, the cost matrix of the gain $K_k$: with $u = -K_k x$, the cost $\int_0^\infty (x^T Q x + u^T R u)\, dt$ equals $x_0^T P_k x_0$. The implementation solves it in the Kronecker form

$$\left( I \otimes A_k^T + A_k^T \otimes I \right) \operatorname{vec} P = -\operatorname{vec}\left( Q + K_k^T R K_k \right),$$

a linear system of size $n^2$, with the [Kronecker product](/kronecker-product/). Line L5 is the improvement step: $K_{k+1}$ minimizes $u^T R u + 2 u^T B^T P_k x$ over $u$ for each $x$. Line L6 stops when the largest entry of $P_k - P_{k-1}$ is at most $10^{-13}$ times the largest entry of $P_k$, or after 50 steps. With exact rational data the code can run a fixed number of steps and returns exact fractions.

Line L4 is Newton's step for the map $\mathcal{R}(X) = A^T X + X A - X G X + Q$, with $G = B R^{-1} B^T$. Its derivative at $P_{k-1}$ is $E \mapsto (A - G P_{k-1})^T E + E (A - G P_{k-1})$, and $A - G P_{k-1} = A_k$. The Newton equation $\mathcal{R}'(P_{k-1})[P_k - P_{k-1}] = -\mathcal{R}(P_{k-1})$ simplifies to $A_k^T P_k + P_k A_k + Q + P_{k-1} G P_{k-1} = 0$, which is line L4 because $K_k^T R K_k = P_{k-1} G P_{k-1}$.

The discrete-time version (Hewer 1971) solves $P = A_k^T P A_k + Q + K_k^T R K_k$ in line L4, with the Kronecker form $(I - A_k^T \otimes A_k^T) \operatorname{vec} P = \operatorname{vec}(Q + K_k^T R K_k)$, and sets $K_{k+1} = (R + B^T P_k B)^{-1} B^T P_k A$ in line L5. It needs $A - B K_0$ Schur. The implementation has it as `hewer`.

## Example

Double integrator: $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $Q = I$, $R = 1$, and $K_0 = \begin{bmatrix} 1 & 1 \end{bmatrix}$, so $A - B K_0 = \begin{bmatrix} 0 & 1 \\ -1 & -1 \end{bmatrix}$ has the characteristic polynomial $s^2 + s + 1$ and is Hurwitz. The solution is $P = \begin{bmatrix} \sqrt 3 & 1 \\ 1 & \sqrt 3 \end{bmatrix}$. In exact arithmetic every $P_k$ has the form $\begin{bmatrix} p_k & 1 \\ 1 & p_k \end{bmatrix}$, and the next gain is $K_{k+1} = \begin{bmatrix} 1 & p_k \end{bmatrix}$:

| $k$ | $K_k$ | $\det(s I - A_k)$ | $p_k$ | $p_k - \sqrt 3$ |
|---|---|---|---|---|
| 0 | $[1,\ 1]$ | $s^2 + s + 1$ | $2$ | $2.68 \times 10^{-1}$ |
| 1 | $[1,\ 2]$ | $s^2 + 2 s + 1$ | $7/4$ | $1.79 \times 10^{-2}$ |
| 2 | $[1,\ 7/4]$ | $s^2 + 1.75 s + 1$ | $97/56$ | $9.20 \times 10^{-5}$ |
| 3 | $[1,\ 97/56]$ | $s^2 + 1.732143 s + 1$ | $18817/10864$ | $2.45 \times 10^{-9}$ |
| 4 | $[1,\ 18817/10864]$ | $s^2 + 1.732051 s + 1$ | $1.7320508075688772$ | below $10^{-15}$ |

To check row 0 by hand: with $P_0 = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$, $A_0^T P_0 = \begin{bmatrix} -1 & -2 \\ 1 & -1 \end{bmatrix}$, and $A_0^T P_0 + P_0 A_0 = \begin{bmatrix} -2 & -1 \\ -1 & -2 \end{bmatrix} = -(Q + K_0^T K_0)$. The values $p_k$ decrease, every closed loop polynomial has positive coefficients and so is Hurwitz, and the error is roughly squared at each step: $0.268^2 / 4 \approx 0.018$. Here the iteration is exactly Newton's method for $x^2 = 3$, that is $p_{k+1} = (p_k + 3 / p_k)/2$.

In discrete time, Hewer's version for $a = b = q = r = 1$ from $K_0 = 1$ gives $p_k = 2, 13/8, 610/377, 1346269/832040$, ratios of Fibonacci numbers, which converge to the golden ratio $(1 + \sqrt 5)/2$.

## Correctness

The full proof is in proofs/correctness.md. Write $D_k = K_k - K_{k+1}$. The key identity is

$$A_{k+1}^T P_k + P_k A_{k+1} + Q + K_{k+1}^T R K_{k+1} = -D_k^T R D_k,$$

which follows from line L4 and $B^T P_k = R K_{k+1}$. It gives three facts. First, $A_{k+1}$ is Hurwitz: an eigenvector $v$ with $\operatorname{Re} \lambda \ge 0$ would give $Q v = 0$ and $A v = \lambda v$, which detectability excludes. Second, subtracting line L4 for step $k + 1$ gives a Lyapunov equation for $P_k - P_{k+1}$ with right side $D_k^T R D_k \ge 0$, so $P_k \ge P_{k+1}$. Third, the sequence is decreasing and bounded below by 0, so it converges, and the limit solves the CARE and is stabilizing. The error $E_k = P_k - P$ satisfies $A_{k+1}^T E_{k+1} + E_{k+1} A_{k+1} + E_k G E_k = 0$, which gives $P_k \ge P$ and $\|E_{k+1}\| \le c \|E_k\|^2$.

The tests check the exact sequences of the example, check in exact rational arithmetic on random problems that every gain is stabilizing and that $P_k - P_{k+1}$ is positive semidefinite (all principal minors at least 0), check quadratic convergence on the double integrator, and compare 400 random problems with the stable eigenvalues of the [Hamiltonian matrix](/hamiltonian-matrix/) and 80 discrete problems with the Riccati recursion.

## Complexity

In the [real RAM](/real-ram/), per step:

- Line L3 costs $O(n^2 m)$.
- Line L4 forms $Q + K^T R K$ in $O(n m^2 + n^2 m)$ and the Kronecker matrix of size $n^2$ in $O(n^4)$, and solves it by Gaussian elimination in $O(n^6)$.
- Line L5 solves with $R$ for $n$ right sides, $O(m^3 + m^2 n + n^2 m)$.
- Line L6 costs $O(n^2)$.

Since $n m^2 + n^2 m \le 2 (n^3 + m^3)$, one step costs $O(n^6 + m^3)$ and $k$ steps cost $O(k (n^6 + m^3))$. The Kronecker matrix takes $O(n^4)$ space. With the Bartels-Stewart method, which reduces $A_k$ to Schur form and solves a triangular Sylvester equation, line L4 costs $O(n^3)$ and the total is $O(k (n^3 + m^3))$ with $O(n^2 + m^2)$ space. The number of steps $k$ depends on how far $K_0$ is from the optimum; once the error is small, quadratic convergence means about $\log_2$ of the number of correct digits, so a handful of steps.

## Properties

- **Every iterate is stabilizing.** Each $K_k$ is a usable controller, so the iteration can be stopped at any step with a stable closed loop whose cost $x^T P_k x$ is known.
- **Monotone.** $P_0 \ge P_1 \ge \dots \ge P$ in the positive semidefinite order. The cost never increases.
- **Quadratic convergence.** $\|P_{k+1} - P\| \le c \|P_k - P\|^2$, the usual rate of [Newton's method](/newton-method-for-systems/); see [quadratic convergence](/quadratic-convergence/).
- **Global from a stabilizing start.** Unlike Newton's method for general equations, it converges from every stabilizing $K_0$, not only from one close to the solution.
- **Exact steps.** With rational data each $P_k$ is rational, as the example shows, but the limit is not rational in general.

## Variants and improvements

- **Discrete time.** Hewer (1971): a discrete Lyapunov equation per step, as above.
- **Line search.** Newton steps far from the solution can overshoot. An exact line search along the Newton direction keeps the first steps short when $K_0$ is poor.
- **Bartels-Stewart solves.** For larger $n$, use a Schur based Lyapunov solver in line L4 in place of the Kronecker form.
- **Low rank Newton.** For large sparse $A$ and low rank $Q$ and $B$, solve each Lyapunov equation approximately with a low rank factor of $P_k$, so $P_k$ is never formed.
- **Refinement.** Started from the result of the [Schur method](/schur-method-riccati/), one or two steps reduce the residual to the rounding level.
- **Data driven.** Policy iteration that estimates $P_k$ from measured data in place of the Lyapunov equation is used in adaptive and learning control.

## When to use it

Use it when a stabilizing gain is known, for example the current controller of a plant, or the solution of a nearby problem when the data change slowly. It is also a good refinement step after a direct method. When no stabilizing gain is known, the [Schur method](/schur-method-riccati/) is the direct alternative, and it needs no start. The Riccati recursion of [infinite-horizon LQR](/infinite-horizon-lqr/) needs no stabilizing start either, but converges only linearly. For an unstable $A$, find a stabilizing $K_0$ first, for example by pole placement.

## Pitfalls

- **Unstable start.** If $A - B K_0$ is not Hurwitz, line L4 may have no solution or a solution that is not a cost, and the iteration can converge to a solution that does not stabilize, or diverge. Line L1 must check the start; $K_0 = 0$ works only when $A$ itself is Hurwitz.
- **Wrong gain update.** Using $K \leftarrow R^{-1} B^T P_{k-1}$ (the old matrix) in line L5 in place of the new $P$ breaks the identity of the proof and the monotone decrease. Line L5 must use the $P$ just computed in line L4.
- **Wrong Kronecker form.** With column stacking, $\operatorname{vec}(M X) = (I \otimes M) \operatorname{vec} X$ and $\operatorname{vec}(X M) = (M^T \otimes I) \operatorname{vec} X$. Writing $A_k \otimes I$ in line L4 in place of $A_k^T \otimes I$ solves a different equation.
- **Stopping on the gain only.** Stopping when $K$ stops changing can stop early when $B$ is small. Line L6 should test $P$, or the CARE residual.
- **No detectability.** If $(Q^{1/2}, A)$ is not detectable, the gains can lose stability, and the limit may not be stabilizing. Check the closed loop at the end.

## Implementations

## History

Kleinman (1968) proposed the iteration for the CARE and proved that every gain stays stabilizing and that the cost matrices decrease to the solution. Hewer (1971) gave the discrete-time version for the steady state gains of the discrete regulator. Policy iteration in dynamic programming, due to Howard, has the same structure, and Kleinman's iteration is now often described as policy iteration for the linear quadratic problem.

## References
