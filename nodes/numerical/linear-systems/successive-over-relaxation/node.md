---
tag: MJSE1P
kind: algorithm
slug: successive-over-relaxation
name: Successive over-relaxation
aliases:
- SOR
- over-relaxation
- relaxed Gauss-Seidel
area: numerical/linear-systems
level: core
summary: Gauss-Seidel with a relaxation factor omega that can speed convergence.
solves: [linear-system-solving]
model: floating-point-model
complexity:
  vars: {n: "the order of A", m: "the number of nonzeros of A", k: "the number of sweeps"}
  time: {worst: "Θ(k (n + m))", best: "Θ(n + m)"}
  space: {extra: Θ(n)}
  flops: {worst: "k (4m + 4n)"}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [matrix-splitting, gauss-seidel-method, spectral-radius]
see_also: [ostrowski-reich-theorem, jacobi-method, chebyshev-iteration, conjugate-gradient-method, multigrid-method, preconditioning, poisson-equation, positive-definite-matrix]
sources:
  - paper: doi:10.1090/S0002-9947-1954-0059635-7
    title: David M. Young, Iterative methods for solving partial difference equations of elliptic type, Transactions of the American Mathematical Society 76, 1954
    locator: consistently ordered matrices, the relation between the eigenvalues of the SOR and Jacobi iteration matrices, and the optimal relaxation factor
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 4.1, Jacobi, Gauss-Seidel, and SOR (the splitting, SSOR, block versions); Section 4.2, Convergence (regular splittings, the SPD case, consistently ordered matrices)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 11.2, The Classical Iterations (Jacobi, Gauss-Seidel, SOR and SSOR, convergence for symmetric positive definite matrices)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 6.5, Basic Iterative Methods (the convergence of SOR for the model problem and the optimal omega)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 17, Stationary Iterative Methods (forward and backward error analysis of splitting iterations, including SOR)
---

Successive over-relaxation (SOR) solves $A x = b$ by sweeping through the unknowns as [Gauss-Seidel](/gauss-seidel-method/) does, but moving each unknown $\omega$ times as far as Gauss-Seidel would. For $\omega = 1$ it is Gauss-Seidel. For symmetric positive definite $A$ it converges exactly when $0 < \omega < 2$, and for the matrices of elliptic difference equations a well chosen $\omega$ cuts the number of sweeps from $O(n^2)$ to $O(n)$ for a one-dimensional grid of $n$ points. Each sweep costs about $2\,\mathrm{nnz}(A)$ flops and reads $A$ once, so it is limited by memory traffic, not by arithmetic.

## In plain words

Go through the equations one at a time. For each one, work out the value of its own unknown that would make that equation hold exactly, using the newest values of all the others. Gauss-Seidel just takes that value. SOR overshoots it: it moves past the value by a fixed factor, because on many problems the corrections keep pointing the same way and going further saves many rounds. Too little overshoot is slow, too much makes the values swing and blow up. Between the two lies a best amount, which for some classic problems can be computed in advance.

## The problem

**Notation.** $A \in \mathbb{R}^{n \times n}$ with $a_{ii} \ne 0$, $b \in \mathbb{R}^n$, $x$ the solution of $A x = b$. Write $A = D - E - F$ with $D$ diagonal, $E$ strictly lower and $F$ strictly upper triangular. $x_k$ is the iterate after $k$ sweeps, $r_k = b - A x_k$ its [residual](/residual/) and $e_k = x_k - x$ its error. The SOR iteration matrix is
$$G_\omega = (D - \omega E)^{-1}\big((1 - \omega) D + \omega F\big),$$
and $J = D^{-1}(E + F)$ is the [Jacobi](/jacobi-method/) iteration matrix, with spectral radius $\mu = \rho(J)$. $\kappa_2(A)$ is the 2-norm condition number and $u = 2^{-53}$ the unit roundoff of binary64.

**Input.** $A$ (stored by sparse rows), $b$, a relaxation factor $\omega$, a start $x_0$, a tolerance and a sweep limit.

**Output.** $x_k$ with $\|r_k\|_2 \le \mathrm{tol}\,\|b\|_2$, or the last iterate and a flag saying the limit was reached. SOR is the [matrix splitting](/matrix-splitting/) $A = M_\omega - N_\omega$ with $M_\omega = D/\omega - E$, so $x_{k+1} = x_k + M_\omega^{-1} r_k$ and $e_{k+1} = G_\omega e_k$.

## The algorithm

```pseudo id=main
SOR(A, b, ω, x_0, tol, maxiter)
L1  x ← x_0
L2  for k ← 1 to maxiter do
L3      for i ← 1 to n do
L4          s ← b_i − Σ_{j ≠ i} a_ij x_j           ▷ x_j is already new for j < i, still old for j > i
L5          x_i ← (1 − ω) x_i + ω s / a_ii         ▷ ω = 1 gives the Gauss-Seidel value s / a_ii
L6      if ‖b − A x‖_2 ≤ tol · ‖b‖_2 then return (x, k, converged)
L7  return (x, maxiter, not converged)
```

Line L5 overwrites $x_i$ at once, so only one vector is stored. The value $s/a_{ii}$ is the Gauss-Seidel update, and L5 can be read as $x_i \leftarrow x_i + \omega(s/a_{ii} - x_i)$: the step of Gauss-Seidel scaled by $\omega$.

## Example

**One sweep by hand.** Take $A = \mathrm{tridiag}(-1, 4, -1)$ of order 3, $b = (3, 2, 3)^T$ (so $x = (1, 1, 1)^T$), $x_0 = 0$ and $\omega = 6/5$. Line L5 gives
$$x_1 = \tfrac65 \cdot \tfrac34 = \tfrac{9}{10}, \quad x_2 = \tfrac65 \cdot \tfrac{2 + 0.9}{4} = \tfrac{87}{100}, \quad x_3 = \tfrac65 \cdot \tfrac{3 + 0.87}{4} = \tfrac{1161}{1000}.$$
Here $\mu = \sqrt2/4$, Young's formula gives $\omega_{\mathrm{opt}} = 1.0334$ and $\rho(G_{\omega_{\mathrm{opt}}}) = 0.0334$ against $\rho(G_1) = \mu^2 = 1/8$. Reaching a relative residual of $10^{-10}$ takes 12 sweeps with $\omega = 1$, 9 with $\omega_{\mathrm{opt}}$, 15 with $\omega = 1.2$ and 34 with $\omega = 1.5$: on a strongly diagonally dominant matrix there is little to gain and overshooting only hurts.

**The model problem.** For $A = \mathrm{tridiag}(-1, 2, -1)$ of order $n$ (the one-dimensional Poisson matrix), $b = (1, \ldots, 1)^T$, $x_0 = 0$ and a relative residual of $10^{-8}$, the implementation gives these sweep counts. The theoretical count is $\log(10^{-8})/\log \rho(G_\omega)$ with $\mu = \cos(\pi/(n+1))$.

| $n$ | $\omega_{\mathrm{opt}}$ | Gauss-Seidel sweeps | SOR sweeps at $\omega_{\mathrm{opt}}$ |
|---|---|---|---|
| 10 | 1.560 | 223 | 40 |
| 20 | 1.741 | 818 | 78 |
| 40 | 1.858 | 3120 | 152 |
| 80 | 1.925 | 12178 | 300 |

Doubling $n$ multiplies the Gauss-Seidel count by about 4 and the optimal SOR count by about 2. For $n = 20$ and other values of $\omega$:

| $\omega$ | $\rho(G_\omega)$ | predicted | observed |
|---|---|---|---|
| 1.0 | 0.9778 | 820 | 818 |
| 1.5 | 0.9317 | 260 | 263 |
| 1.741 | 0.7406 | 61 | 78 |
| 1.9 | 0.9000 | 175 | 189 |
| 2.2 | at least 1.2 | diverges | residual above $10^5$ after 60 sweeps |

At $\omega_{\mathrm{opt}}$ the observed count exceeds the prediction because $G_{\omega_{\mathrm{opt}}}$ has a Jordan block for its dominant eigenvalue, so $\|e_k\|$ behaves like $k\,\rho^k$ rather than $\rho^k$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). One sweep is $x_{k+1} = x_k + M_\omega^{-1}(b - A x_k)$, so $x$ is a fixed point, any limit solves $A x = b$, and $e_k = G_\omega^k e_0$. Hence SOR converges for every $x_0$ if and only if $\rho(G_\omega) < 1$. Two results bound $\omega$:

- **Kahan (1958).** $\det G_\omega = (1 - \omega)^n$, so $\rho(G_\omega) \ge |\omega - 1|$, and $0 < \omega < 2$ is necessary for every $A$.
- **[Ostrowski-Reich](/ostrowski-reich-theorem/).** If $A$ is symmetric positive definite, $0 < \omega < 2$ is also sufficient. Conversely, for symmetric $A$ with positive diagonal, convergence for some $\omega \in (0, 2)$ implies that $A$ is positive definite.

**Young's theory.** If $A$ is *consistently ordered* (for instance block tridiagonal with diagonal blocks $D_i$, or a five-point Laplacian in red-black or natural ordering) and the eigenvalues of $J$ are real with $\mu < 1$, then each eigenvalue $\lambda$ of $G_\omega$ satisfies $(\lambda + \omega - 1)^2 = \lambda\,\omega^2 \nu^2$ for some eigenvalue $\nu$ of $J$. From this:
$$\omega_{\mathrm{opt}} = \frac{2}{1 + \sqrt{1 - \mu^2}}, \qquad \rho(G_{\omega_{\mathrm{opt}}}) = \omega_{\mathrm{opt}} - 1, \qquad \rho(G_1) = \mu^2,$$
with $\rho(G_\omega) = \omega - 1$ for $\omega \ge \omega_{\mathrm{opt}}$ and $\rho(G_\omega) = \tfrac14\big(\omega\mu + \sqrt{\omega^2\mu^2 - 4(\omega - 1)}\big)^2$ below it. For the model problem $\mu = \cos(\pi/(n+1))$, so $\rho(G_1) \approx 1 - \pi^2/(n+1)^2$ while $\rho(G_{\omega_{\mathrm{opt}}}) \approx 1 - 2\pi/(n+1)$: the number of sweeps for a fixed reduction drops from $O(n^2)$ to $O(n)$. The same holds for the two-dimensional five-point Laplacian with $n$ points per side. These are proved for consistently ordered matrices only.

**In floating point.** The bounds above are exact-arithmetic statements. With rounding, the residual of the iterates stalls at a level of order $u\,\|A\|\,\|x\|$; for the $n = 20$ model problem the observed level is $2.1 \times 10^{-14}$ in the $\infty$-norm, with $\|A\|_\infty = 4$ and $\|x\|_\infty = 55$, so asking for $10^{-18}$ never succeeds. Higham (Chapter 17) gives forward and backward error bounds for stationary iterations including SOR; their constants involve $|M_\omega^{-1}|(|M_\omega| + |N_\omega|)$ and can be large when $\rho(G_\omega)$ is near 1. On stopping, $\|e_k\|_2/\|x\|_2 \le \kappa_2(A)\,\mathrm{tol}$ holds for the residual actually achieved; it is a worst-case bound.

## Complexity

One sweep (lines L3 to L5) costs $2\,\mathrm{nnz}(A) + 2n$ flops, and the residual test at line L6 another $2\,\mathrm{nnz}(A) + 2n$; checking the residual every few sweeps, or using the size of the update instead, halves the cost. Extra storage is $O(n)$ beyond $A$. Each sweep streams all of $A$ from memory and does two flops per stored nonzero, so on current hardware the speed is set by memory bandwidth, about 12 bytes per nonzero in compressed sparse row form.

The number of sweeps for a reduction by $\varepsilon$ is about $\log \varepsilon/\log \rho(G_\omega)$. For the $d$-dimensional model problem with $N = n^d$ unknowns, Gauss-Seidel needs $O(n^2)$ sweeps and optimal SOR $O(n)$, so optimal SOR costs $O(N^{1 + 1/d})$ flops; [conjugate gradients](/conjugate-gradient-method/) match this without needing $\omega$, and [multigrid](/multigrid-method/) reaches $O(N)$.

## Properties

- **Deterministic and in place.** The sweep overwrites $x$; only $b$, $x$ and the diagonal are stored besides $A$.
- **Order dependent.** Unlike Jacobi, the result of a sweep depends on the ordering of the unknowns; the ordering also decides whether $A$ is consistently ordered.
- **Sequential within a sweep.** $x_i$ needs the new $x_j$ for $j < i$. Red-black (and multicolor) orderings make each color independent and parallel.
- **Not symmetric.** $M_\omega$ is not symmetric, so SOR is not a symmetric preconditioner for conjugate gradients; SSOR is.
- **Smoothing.** For $\omega$ near 1 it damps the oscillatory part of the error fast and the smooth part slowly, which is why Gauss-Seidel, not optimal SOR, is the usual multigrid smoother.

## Variants and improvements

- **SSOR.** A forward sweep followed by a backward sweep. Its iteration matrix is similar to a symmetric matrix when $A$ is symmetric, so it can be accelerated by [Chebyshev iteration](/chebyshev-iteration/) or used as a [preconditioner](/preconditioning/) for conjugate gradients, with $M = \frac{\omega}{2 - \omega}(D/\omega - E) D^{-1}(D/\omega - E^T)$ (Saad, Section 4.1).
- **Block SOR.** $D$ becomes block diagonal (for example one grid line per block), each step solves a small system, often by the [Thomas algorithm](/thomas-algorithm/); it converges faster per sweep.
- **Adaptive $\omega$.** Estimate $\mu$ from the ratio of successive update norms during Gauss-Seidel sweeps and set $\omega$ by Young's formula; it is safer to err above $\omega_{\mathrm{opt}}$, where $\rho(G_\omega) = \omega - 1$ grows linearly, than below, where it grows with infinite slope.
- **Under-relaxation.** $0 < \omega < 1$ can make a divergent Gauss-Seidel converge on some nonsymmetric problems, and is used to stabilize nonlinear iterations.

## When to use it

Use SOR for large sparse systems that come from elliptic equations on regular grids, when the optimal $\omega$ is known or easy to estimate, memory is tight and a simple matrix-free kernel is wanted. As a stand-alone solver it has largely been replaced by preconditioned [conjugate gradients](/conjugate-gradient-method/) and [multigrid](/multigrid-method/); it survives as a smoother, as SSOR preconditioning, and in teaching. Do not use it on indefinite or strongly nonsymmetric matrices without a convergence argument.

## Pitfalls

- **$\omega$ outside $(0, 2)$.** The iteration cannot converge for all starts, whatever $A$ is (Kahan).
- **Not SPD.** For a symmetric indefinite $A$ it diverges for every $\omega$; the matrix $\begin{pmatrix} 1 & 2 \\ 2 & 1 \end{pmatrix}$ gives iterates above $10^{100}$ in a few hundred sweeps. For nonsymmetric $A$, Gauss-Seidel may diverge where Jacobi converges: $\begin{pmatrix} 1 & 2 & -2 \\ 1 & 1 & 1 \\ 2 & 2 & 1 \end{pmatrix}$ has $\rho(J) = 0$ and $\rho(G_1) = 2$.
- **Using Young's formula outside its hypotheses.** It needs a consistently ordered matrix with real Jacobi spectrum; elsewhere $\omega_{\mathrm{opt}}$ from it can be far off.
- **Sensitivity just below $\omega_{\mathrm{opt}}$.** $\rho(G_\omega)$ has a square-root singularity at $\omega_{\mathrm{opt}}$, so underestimating $\mu$ slightly costs many sweeps.
- **Small residual, large error.** The stopping test bounds the residual; the error can still be $\kappa(A)$ times larger, and $\kappa_2$ of the model problem grows like $n^2$.
- **A tolerance below the rounding level.** The residual stalls near $u\,\|A\|\,\|x\|$, so the loop runs to `maxiter`.

## Implementations

## History

Relaxation methods were used by hand by Southwell in the 1940s, who over-relaxed individual residuals by judgment. David Young's 1950 Harvard thesis, published as the 1954 paper, made over-relaxation systematic for computers: he introduced consistently ordered matrices (property A), related the SOR eigenvalues to the Jacobi eigenvalues and derived $\omega_{\mathrm{opt}}$. Frankel (1950) gave the same method for the Laplace equation under the name extrapolated Liebmann method. Reich (1949) and Ostrowski (1954) proved convergence for symmetric positive definite matrices, and Kahan's 1958 thesis gave the bound $\rho(G_\omega) \ge |\omega - 1|$. Varga's *Matrix Iterative Analysis* (1962) and Young's *Iterative Solution of Large Linear Systems* (1971) collected the theory.

## References
