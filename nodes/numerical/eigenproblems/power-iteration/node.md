---
tag: F8BB9Q
kind: algorithm
slug: power-iteration
name: Power iteration
aliases:
- power method
- von Mises iteration
area: numerical/eigenproblems
level: core
summary: Multiply a unit vector by A again and again. When one eigenvalue is strictly largest in modulus, the vector turns to its eigenvector at the rate |λ_2/λ_1| per step.
solves: [eigenvalue-problem]
model: floating-point-model
complexity:
  vars: {n: "the order of A", z: "the number of nonzeros of A", k: "the number of iterations"}
  time: {worst: Θ(k z + k n)}
  space: {extra: Θ(n)}
  matvecs: {worst: "k"}
  flops: {worst: "2 k z + 9 k n"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: true}
history:
  year: 1929
  people: [Richard von Mises, Hilda Pollaczek-Geiringer]
  note: Von Mises and Pollaczek-Geiringer described the iteration in 1929 in a survey of practical methods for linear equations and eigenvalues.
prereqs: [eigenvalue, eigenvector, rayleigh-quotient]
see_also: [inverse-iteration, rayleigh-quotient-iteration, subspace-iteration, lanczos-algorithm, arnoldi-iteration, perron-frobenius-theorem, pagerank, deflation]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 7.3.1, The Power Method (nonsymmetric case); Section 8.2.1, The Power Method (symmetric case, the squared rate of the Rayleigh quotient)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 27, Rayleigh Quotient, Inverse Iteration (Algorithm 27.1 and Theorem 27.1 on the rates)
  - book: isbn:9781611970722
    title: Yousef Saad, Numerical Methods for Large Eigenvalue Problems, revised edition, SIAM Classics in Applied Mathematics 66, 2011
    locator: Chapter 4, Section 4.1, Single Vector Iterations (the power method, shifts and inverse iteration)
  - book: isbn:9780898714029
    title: Beresford N. Parlett, The Symmetric Eigenvalue Problem, SIAM Classics in Applied Mathematics 20, 1998
    locator: Chapter 4, Simple Vector Iterations (the power method and the residual bounds)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 4.4.1, Power Method
  - paper: "R. von Mises and H. Pollaczek-Geiringer, Praktische Verfahren der Gleichungsauflösung, Zeitschrift für Angewandte Mathematik und Mechanik 9, 1929"
    title: R. von Mises and H. Pollaczek-Geiringer, Praktische Verfahren der Gleichungsauflösung
    locator: ZAMM 9 (1929), pp. 58 to 77 and 152 to 164
  - book: "J. H. Wilkinson, The Algebraic Eigenvalue Problem, Oxford University Press, 1965"
    title: J. H. Wilkinson, The Algebraic Eigenvalue Problem
    locator: Chapter 9, Iterative Methods (the power method, its acceleration and its error analysis)
---

Power iteration finds the [eigenvalue](/eigenvalue/) of largest modulus of a square matrix $A$ and its [eigenvector](/eigenvector/) by repeated products $q \leftarrow A q / \|A q\|$. If $|\lambda_1| > |\lambda_2|$ and the start has a component along $v_1$, the angle between $q_k$ and $v_1$ shrinks like $|\lambda_2/\lambda_1|^k$, and the [Rayleigh quotient](/rayleigh-quotient/) $\rho(q_k)$ converges at the same rate, or at the rate $|\lambda_2/\lambda_1|^{2k}$ when $A$ is symmetric. It needs only products with $A$ and $O(n)$ memory, so it works for huge sparse matrices such as the web graph of [PageRank](/pagerank/), but it is slow when the ratio is near 1 and fails when no eigenvalue is strictly dominant.

## In plain words

Take any starting arrow and apply the matrix to it, then shrink the result back to length one, and repeat. Each step stretches every hidden direction of the matrix by its own factor. The direction with the biggest factor grows faster than all the others, so after many steps it is the only one left that matters. The arrow then points along that direction, and the amount by which the matrix stretches it is the biggest factor. How fast this happens depends on how much bigger the biggest factor is than the second biggest. If the two are close, it takes many steps; if they are the same size, the arrow never settles.

## The problem

**Notation.** $A \in \mathbb C^{n \times n}$ (often real) with eigenvalues ordered by modulus, $|\lambda_1| \ge |\lambda_2| \ge \dots \ge |\lambda_n|$, and eigenvectors $v_i$. The ratio $|\lambda_2 / \lambda_1|$ sets the speed. $\rho(x) = x^* A x / x^* x$ is the Rayleigh quotient and $u$ the unit roundoff. $z$ is the number of nonzeros of $A$; a product $A q$ costs about $2z$ flops ($2n^2$ for a dense matrix).

Given $A$ (only through products $q \mapsto A q$), a start $x_0 \ne 0$, a tolerance $\mathrm{tol}$ and a limit $\mathrm{maxit}$, return a scalar $\rho$ and a unit vector $q$ with a small residual $\|A q - \rho q\|_2 \le \mathrm{tol} \, \|A q\|_2$, and the flag CONVERGED; or the last pair and NOT-CONVERGED. This is the dominant-eigenpair case of the [eigenvalue problem](/eigenvalue-problem/).

## The algorithm

```pseudo id=main
POWER-ITERATION(A, x₀, tol, maxit)
L1  q ← x₀ / ‖x₀‖₂
L2  for k ← 1 to maxit do
L3      z ← A q                                   ▷ the only access to A
L4      ρ ← q* z                                  ▷ Rayleigh quotient, since ‖q‖₂ = 1
L5      r ← z − ρ q                               ▷ residual of the pair (ρ, q)
L6      if ‖r‖₂ ≤ tol · ‖z‖₂ then return (ρ, q, k, CONVERGED)
L7      if k = maxit then return (ρ, q, k, NOT-CONVERGED)
L8      q ← z / ‖z‖₂
```

Line L3 is the only use of $A$. Line L4 is the Rayleigh quotient of the current unit vector, which is the best estimate of the eigenvalue for that vector. Line L5 forms the residual of the same pair, and line L6 stops when it is small relative to $\|A q\|_2 \le \|A\|_2$. The test in line L6 also covers $A q = 0$: then $r = 0$ and the pair $(0, q)$ is returned before line L8 would divide by zero. The normalization of line L8 keeps the numbers in range; without it $A^k x_0$ overflows or underflows. The test uses the residual and not the change $q_k - q_{k-1}$, because for a negative or complex $\lambda_1$ the vector $q_k$ changes sign or phase at every step even when it has converged in direction.

## Example

Let $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$, with $\lambda_1 = 3$, $v_1 = (1, 1)^T / \sqrt 2$, $\lambda_2 = 1$, and $x_0 = (1, 0)^T$. Here $A^k x_0 = \bigl((3^k + 1)/2, (3^k - 1)/2\bigr)^T$, so $\tan\theta_k = 3^{-k}$ and $\rho_k = (3 \cdot 9^k + 1)/(9^k + 1)$, with the error $3 - \rho_k = 2/(9^k + 1)$. The value $\rho$ is the one of line L4 at step $k + 1$, computed from $q_k$.

| $k$ | $q_k$ | $\rho(q_k)$ | $3 - \rho(q_k)$ | $\lVert r_k \rVert_2$ | $\tan\theta_k$ |
|---|---|---|---|---|---|
| 0 | (1.000000, 0.000000) | 2.000000 | 1.000e+00 | 1.000e+00 | 1.000e+00 |
| 1 | (0.894427, 0.447214) | 2.800000 | 2.000e-01 | 6.000e-01 | 3.333e-01 |
| 2 | (0.780869, 0.624695) | 2.975610 | 2.439e-02 | 2.195e-01 | 1.111e-01 |
| 3 | (0.732793, 0.680451) | 2.997260 | 2.740e-03 | 7.397e-02 | 3.704e-02 |
| 4 | (0.715782, 0.698324) | 2.999695 | 3.048e-04 | 2.469e-02 | 1.235e-02 |
| 5 | (0.710011, 0.704191) | 2.999966 | 3.387e-05 | 8.230e-03 | 4.115e-03 |

The angle and the residual shrink by $1/3 = |\lambda_2/\lambda_1|$ per step, and the eigenvalue error by $1/9$, because $A$ is symmetric. With $\mathrm{tol} = 10^{-12}$ the method stops at step 26, with $\|r\|_2 = 2.4 \times 10^{-12}$.

## Correctness

**Backward error on success.** When line L6 returns, $(\rho, q)$ is an exact eigenpair of $A + E$ with $E = -r q^*$ and $\|E\|_2 = \|r\|_2 \le \mathrm{tol} \, \|A\|_2$. This holds for every $A$, with no assumption on the spectrum.

**Convergence.** By induction, $q_k = A^k x_0 / \|A^k x_0\|_2$. Assume $A$ is diagonalizable, $|\lambda_1| > |\lambda_2|$, and $x_0 = \sum_i c_i v_i$ with $c_1 \ne 0$. Then

$$\frac{A^k x_0}{c_1 \lambda_1^k} = v_1 + \sum_{i \ge 2} \frac{c_i}{c_1} \Bigl(\frac{\lambda_i}{\lambda_1}\Bigr)^k v_i,$$

so $\sin\angle(q_k, v_1) = O(|\lambda_2/\lambda_1|^k)$ and $|\rho(q_k) - \lambda_1| = O(|\lambda_2/\lambda_1|^k)$. For a Hermitian $A$ with orthonormal $v_i$, the sharp form is $\tan\theta_k \le |\lambda_2/\lambda_1|^k \tan\theta_0$ and $|\rho(q_k) - \lambda_1| \le (\lambda_{\max} - \lambda_{\min}) \sin^2\theta_k$. Then $\|r_k\|_2 \to 0$ and $\|A q_k\|_2 \to |\lambda_1| > 0$, so line L6 succeeds for each $\mathrm{tol} > 0$ in exact arithmetic. The full proof is in the proof file.

## Complexity

- **Per step.** One product with $A$ ($2z$ flops) and $9n$ flops for lines L4 to L8 in real arithmetic: $2n$ for $q^* z$, $2n$ for $r$, $4n$ for the two norms and $n$ for the division. The extra memory is the three vectors $q$, $z$ and $r$, $\Theta(n)$.
- **Number of steps (proved, Hermitian case).** Since $\|r_k\|_2 \le \sqrt 2 (\lambda_{\max} - \lambda_{\min}) \sin\theta_k$, the residual test with tolerance $\mathrm{tol}$ passes once $\sqrt 2 (\lambda_{\max} - \lambda_{\min}) \tan\theta_0 \, |\lambda_2/\lambda_1|^k \le \mathrm{tol} \, |\lambda_1|$ (to first order, since $\|A q_k\| \to |\lambda_1|$), that is after about $\log(C/\mathrm{tol}) / \log|\lambda_1/\lambda_2|$ steps, with $C$ fixed by $A$ and $x_0$. For $|\lambda_2/\lambda_1| = 0.9$ and $\mathrm{tol} = 10^{-12}$ that is about 260 steps; for $0.999$, about 28000.
- **General case.** The same bound holds with a constant that also contains $\kappa(V) = \|V\| \|V^{-1}\|$ for $A = V \Lambda V^{-1}$. If $\lambda_1$ has a Jordan block of size $m \ge 2$, the error decays only like $1/k$.

## Properties

- **Matrix-free.** Only products $A q$ are needed, so $A$ can be sparse, structured, or given by a program.
- **Linear convergence.** The rate is $|\lambda_2/\lambda_1|$ for the vector and for the residual; it does not improve as the iteration proceeds.
- **Backward stable steps.** Each computed product is $(A + \Delta) q$ with $|\Delta| \le \gamma_n |A|$ entrywise, where $\gamma_n = n u / (1 - n u)$, and normalization errors are of order $u$, so rounding does not change the limit: the method reaches a residual of order $n u \|A\|$ and stalls there.
- **Rounding helps the start.** A start with $c_1 = 0$ converges in exact arithmetic to a lower eigenvector, but rounding errors usually create a component along $v_1$ that then grows. A diagonal matrix keeps exact zeros, so this does not happen there.

## Variants and improvements

- **Shifts.** Power iteration on $A - \sigma I$ has the rate $\max_{i \ne 1} |\lambda_i - \sigma| / |\lambda_1 - \sigma|$. For a symmetric $A$ with eigenvalues in $[\lambda_n, \lambda_1]$ the best fixed shift for $\lambda_1$ is $\sigma = (\lambda_2 + \lambda_n)/2$.
- **[Inverse iteration](/inverse-iteration/).** Power iteration on $(A - \sigma I)^{-1}$ converges to the eigenvalue nearest $\sigma$, at the rate $|\lambda_j - \sigma| / |\lambda_k - \sigma|$ for the two nearest.
- **[Rayleigh quotient iteration](/rayleigh-quotient-iteration/).** Inverse iteration with the shift $\rho(q_k)$ at each step; cubic convergence for symmetric $A$.
- **[Subspace iteration](/subspace-iteration/).** Iterate a block of $p$ vectors and orthonormalize; the $i$th vector converges at the rate $|\lambda_{p+1}/\lambda_i|$.
- **[Deflation](/deflation/).** After $(\lambda_1, v_1)$ is found, iterate with a matrix whose dominant eigenvalue is $\lambda_2$, for example $A - \lambda_1 v_1 v_1^T$ for a symmetric $A$.
- **Krylov methods.** The iterates span the Krylov space $\mathcal K_k(A, x_0) = \operatorname{span}\{x_0, A x_0, \dots, A^{k-1} x_0\}$, but power iteration keeps only the last vector. The [Lanczos algorithm](/lanczos-algorithm/) and the [Arnoldi iteration](/arnoldi-iteration/) use the whole space for the same number of products and converge much faster.

## When to use it

Use it when only products with $A$ are possible, memory is tight, and the dominant eigenvalue is well separated, as for the stationary vector of a Markov chain with a spectral gap or for [PageRank](/pagerank/), where the damping factor bounds the ratio. Use it also as a cheap estimate of $\|A\|_2$ (power iteration on $A^T A$) or of the [spectral radius](/spectral-radius/). For several eigenvalues, interior eigenvalues, or a ratio near 1, use [Lanczos](/lanczos-algorithm/), [Arnoldi](/arnoldi-iteration/) or [implicitly restarted Arnoldi](/implicitly-restarted-arnoldi/); for a dense matrix that fits in memory, the [QR algorithm](/qr-algorithm/) gives all eigenvalues in $O(n^3)$ flops.

## Pitfalls

- **No dominant eigenvalue.** If $|\lambda_1| = |\lambda_2|$ with $\lambda_1 \ne \lambda_2$, for example the pair $\pm 1$ of $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ or a complex pair $1 \pm 2i$ of a real matrix, the vector does not converge. Line L7 must end the loop; a code without it runs forever.
- **Stopping on the change of the vector.** A test $\|q_k - q_{k-1}\| \le \mathrm{tol}$ in place of line L6 never passes when $\lambda_1 < 0$, because $q_k$ flips sign. Test the residual.
- **Stopping on the change of the eigenvalue.** A small change $|\rho_k - \rho_{k-1}|$ can occur long before convergence when the ratio is near 1: the change is about $(1 - |\lambda_2/\lambda_1|)$ times the error. Only the residual bounds the backward error.
- **A residual relative to the eigenvalue.** A test $\|r\| \le \mathrm{tol} \, |\rho|$ fails for a zero or tiny dominant eigenvalue; line L6 compares with $\|A q\|$, and a code can compare with an estimate of $\|A\|$.
- **No normalization.** Computing $A^k x_0$ and normalizing only at the end overflows or underflows after a few hundred steps. Line L8 normalizes at each step.

## Implementations

## History

Richard von Mises and Hilda Pollaczek-Geiringer described the iteration in 1929, in a survey of practical methods for solving linear equations and computing eigenvalues. It was the standard way to compute a dominant eigenvalue on the first computers, and Wilkinson's book of 1965 gives its error analysis and many of its variants.

## References
