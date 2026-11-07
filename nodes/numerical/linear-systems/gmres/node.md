---
tag: JYTTHH
kind: algorithm
slug: gmres
name: GMRES
aliases:
- generalized minimal residual method
- GMRES(m)
- restarted GMRES
area: numerical/linear-systems
level: advanced
summary: Krylov method for general nonsymmetric systems that minimizes the residual over the subspace.
solves: [linear-system-solving]
model: floating-point-model
complexity:
  vars: {n: "the order of A", z: "the number of nonzeros of A", k: "the number of Arnoldi steps", m: "the restart length"}
  time: {worst: O(k z + k^2 n), restarted: O(k z + k m n)}
  space: {extra: Θ(k n), restarted: Θ(m n)}
  matvecs: {worst: "k"}
  flops: {worst: "2 k z + 2 k^2 n + O(k n)"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: true}
prereqs: [krylov-subspace, arnoldi-iteration, givens-rotations, least-squares-problem]
see_also: [conjugate-gradient-method, minres, biconjugate-gradient, bicgstab, preconditioning, gram-schmidt-process, incomplete-lu-factorization, sparse-linear-systems]
sources:
  - paper: doi:10.1137/0907058
    title: Youcef Saad and Martin H. Schultz, GMRES, a generalized minimal residual algorithm for solving nonsymmetric linear systems, SIAM Journal on Scientific and Statistical Computing 7(3), 1986
    locator: pp. 856 to 869 (the algorithm, the Givens update of the residual norm, Proposition 2 on breakdown and the convergence bound for diagonalizable A)
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 6.5, GMRES (Algorithm 6.9, Proposition 6.10 on the residual norm, Section 6.5.3 practical implementation, Section 6.5.6 restarting); Section 6.11.4, Convergence of GMRES
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 35, GMRES (Theorem 35.2 on the polynomial bound)
  - book: isbn:9780898713961
    title: Anne Greenbaum, Iterative Methods for Solving Linear Systems, SIAM, 1997
    locator: Section 2.1, GMRES; Section 3.2, GMRES and nonnormal matrices; Section 3.4 (any nonincreasing convergence curve is possible)
  - paper: doi:10.1137/050631574
    title: Christopher C. Paige, Miroslav Rozložník and Zdeněk Strakoš, Modified Gram-Schmidt (MGS), least squares, and backward stability of MGS-GMRES, SIAM Journal on Matrix Analysis and Applications 28(1), 2006
    locator: pp. 264 to 284 (MGS-GMRES is backward stable for sufficiently nonsingular A)
  - paper: doi:10.1137/S0895479894275030
    title: Anne Greenbaum, Vlastimil Pták and Zdeněk Strakoš, Any nonincreasing convergence curve is possible for GMRES, SIAM Journal on Matrix Analysis and Applications 17(3), 1996
    locator: pp. 465 to 469 (Theorem 1)
  - paper: doi:10.1137/0720023
    title: Stanley C. Eisenstat, Howard C. Elman and Martin H. Schultz, Variational iterative methods for nonsymmetric systems of linear equations, SIAM Journal on Numerical Analysis 20(2), 1983
    locator: pp. 345 to 357 (the bound for restarted methods when the symmetric part is positive definite)
---

GMRES solves a general nonsingular linear system $A x = b$ by choosing, at step $k$, the vector $x_k$ in the affine [Krylov subspace](/krylov-subspace/) $x_0 + \mathcal K_k(A, r_0)$ whose residual $\|b - A x_k\|_2$ is smallest. It builds an orthonormal basis of the subspace with the [Arnoldi iteration](/arnoldi-iteration/), reduces the minimization to a small [least squares problem](/least-squares-problem/) with an upper Hessenberg matrix, and solves that with [Givens rotations](/givens-rotations/), which update the residual norm at every step for free. Saad and Schultz (1986) introduced it. Its residuals never increase and it terminates in at most $n$ steps in exact arithmetic, but step $k$ costs $O(k n)$ flops and $O(k n)$ storage, so in practice it is restarted every $m$ steps as GMRES($m$), which can stagnate.

## In plain words

GMRES keeps a growing list of directions, one new direction per multiplication by the matrix, and makes them perpendicular to each other. At every step it asks which combination of all directions found so far gives the smallest misfit, and that question is a tiny fitting problem that is cheap to update. Since the list only grows, the misfit can only shrink.

The price is that every direction must be kept and compared with the next one, so time and memory grow with each step. Practical codes therefore throw the list away every few dozen steps and start again from the current answer.

## The problem

**Notation.** As in [solving linear systems](/linear-system-solving/): $A \in \mathbb{R}^{n \times n}$ nonsingular, $b \in \mathbb{R}^n$, $x_k$ the $k$th iterate, $r_k = b - A x_k$, $\mathcal K_k(A, r_0) = \operatorname{span}\{r_0, A r_0, \dots, A^{k-1} r_0\}$, $\kappa(A)$ the condition number, $u = 2^{-53}$, $\gamma_n = n u / (1 - n u)$. $z$ is the number of nonzeros of $A$; one matvec costs about $2 z$ flops.

Given $A$ (only through products $v \mapsto A v$), $b$, a start $x_0$, a tolerance $\mathrm{tol}$ and a step limit, return $x_k$ with $\|r_k\|_2 \le \mathrm{tol} \cdot \|b\|_2$ and the flag CONVERGED, or the best iterate found and NOT-CONVERGED. If $A$ is singular on the Krylov space, report BREAKDOWN.

## The algorithm

Let $\beta = \|r_0\|_2$ and $v_1 = r_0 / \beta$. After $j$ Arnoldi steps, $V_{j+1} = [v_1, \dots, v_{j+1}]$ has orthonormal columns and $A V_j = V_{j+1} \bar H_j$ with $\bar H_j$ upper Hessenberg of size $(j + 1) \times j$. For $x = x_0 + V_j y$,
$$\|b - A x\|_2 = \|\beta v_1 - V_{j+1} \bar H_j y\|_2 = \|\beta e_1 - \bar H_j y\|_2,$$
so the step reduces to a $(j+1) \times j$ least squares problem. Rotations $G_1, \dots, G_j$ reduce $\bar H_j$ to $\begin{pmatrix} R_j \\ 0 \end{pmatrix}$ with $R_j$ upper triangular, and turn $\beta e_1$ into $g = (g_1, \dots, g_{j+1})$; then $y = R_j^{-1} g_{1:j}$ and $\|r_j\|_2 = |g_{j+1}|$.

```pseudo id=main
GMRES(A, b, x, tol, m, kmax)                ▷ x is the start x₀; m is the restart length
L1  r ← b − A x;  β ← ‖r‖₂;  if β ≤ tol · ‖b‖₂ or kmax steps done then return (x, status)
L2  v₁ ← r / β;  g ← (β, 0, …, 0)
L3  for j ← 1 to m do
L4      w ← A v_j
L5      for i ← 1 to j do  h_ij ← v_iᵀ w;  w ← w − h_ij v_i      ▷ modified Gram-Schmidt
L6      h_{j+1,j} ← ‖w‖₂;  v_{j+1} ← w / h_{j+1,j}
L7      apply G₁, …, G_{j−1} to column j of H;  choose G_j to zero h_{j+1,j};  g ← G_j g
L8      if |g_{j+1}| ≤ tol · ‖b‖₂ or h_{j+1,j} = 0 then leave the loop
L9  solve R_j y = g_{1:j} by back substitution;  x ← x + V_j y
L10 go to L1                                  ▷ restart from the new x
```

The rotation in L7 with $\rho = (h_{jj}^2 + h_{j+1,j}^2)^{1/2}$ is $c = h_{jj}/\rho$, $s = h_{j+1,j}/\rho$, and it sets $g_{j+1} \leftarrow -s g_j$, $g_j \leftarrow c g_j$. If $\rho = 0$, then $A$ is singular on $\mathcal K_j$ and the code returns BREAKDOWN with the iterate of step $j - 1$. With $m = n$ the loop never restarts (full GMRES). The test in L8 uses the updated residual $|g_{j+1}|$; the implementation confirms it with a true residual after L9.

## Example

Take
$$A = \begin{pmatrix} 2 & 1 & 0 \\ 0 & 2 & 1 \\ 0 & 0 & 2 \end{pmatrix}, \quad b = \begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix}, \quad x_0 = 0,$$
so $x = (1/8, -1/4, 1/2)$, $r_0 = b$ and $\beta = 1$, $v_1 = e_3$.

- **Step 1.** $w = A e_3 = (0, 1, 2)$, $h_{11} = 2$, $w \leftarrow (0, 1, 0)$, $h_{21} = 1$, $v_2 = e_2$. The rotation has $\rho = \sqrt 5$, $c = 2/\sqrt 5$, $s = 1/\sqrt 5$, so $g = (2/\sqrt 5, -1/\sqrt 5)$ and $\|r_1\|_2 = 1/\sqrt 5 \approx 0.447$. Indeed $x_1 = \alpha e_3$ minimizes $\|e_3 - \alpha (0, 1, 2)\|_2$ at $\alpha = 2/5$, with squared residual $1/5$.
- **Step 2.** $w = A e_2 = (1, 2, 0)$, $h_{12} = 0$, $h_{22} = 2$, $w \leftarrow (1, 0, 0)$, $h_{32} = 1$, $v_3 = e_1$. So
$$\bar H_2 = \begin{pmatrix} 2 & 0 \\ 1 & 2 \\ 0 & 1 \end{pmatrix}.$$
Applying $G_1$ to the new column $(0, 2, 1)$ gives $(2/\sqrt 5, 4/\sqrt 5, 1)$; then $\rho = \sqrt{21/5}$ and $|g_3| = 1/\sqrt{21} \approx 0.218$.
- **Step 3.** $w = A e_1 = (2, 0, 0)$, $h_{13} = h_{23} = 0$, $h_{33} = 2$ and $h_{43} = 0$: a lucky breakdown, since $\mathcal K_3 = \mathbb{R}^3$. Now $g_4 = 0$ and back substitution gives $x_3 = x$.

The residual history $1, 1/\sqrt 5, 1/\sqrt{21}, 0$ matches the exact minima over $\mathcal K_k$ computed in rational arithmetic by the test file.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). In exact arithmetic:

1. **Arnoldi relation.** As long as $h_{i+1,i} \ne 0$ for $i \le j$, the vectors $v_1, \dots, v_{j+1}$ are orthonormal, span $\mathcal K_{j+1}(A, r_0)$, and $A V_j = V_{j+1} \bar H_j$.
2. **Minimality.** The iterate from L9 is the minimizer of $\|b - A x\|_2$ over $x_0 + \mathcal K_j$, and $|g_{j+1}|$ is its residual norm. Hence $\|r_{j+1}\|_2 \le \|r_j\|_2$, and $\|r_j\|_2 = \min_{p \in \mathcal P_j^0} \|p(A) r_0\|_2$, where $\mathcal P_j^0$ is the set of polynomials of degree at most $j$ with $p(0) = 1$.
3. **Termination.** If $A$ is nonsingular, $\rho \ne 0$ always, and the first $j$ with $h_{j+1,j} = 0$ is the grade $d \le n$ of $r_0$; then $r_d = 0$. So full GMRES returns the exact solution in at most $n$ steps, and every run stops after at most $\mathrm{kmax}$ steps.
4. **Convergence bounds.** If $A = X \Lambda X^{-1}$ is diagonalizable, $\|r_k\|_2 \le \kappa_2(X) \min_{p \in \mathcal P_k^0} \max_{\lambda \in \Lambda(A)} |p(\lambda)| \, \|r_0\|_2$ (Saad and Schultz, Proposition 4; Trefethen and Bau, Theorem 35.2). If $A$ is SPD this gives $\|r_k\|_2 \le 2 \left(\frac{\sqrt{\kappa} - 1}{\sqrt{\kappa} + 1}\right)^k \|r_0\|_2$ with $\kappa = \kappa_2(A)$. If the symmetric part $M = (A + A^T)/2$ is positive definite, every step of GMRES($m$), even with $m = 1$, satisfies $\|r_{k+1}\|_2^2 \le \left(1 - \frac{\lambda_{\min}(M)^2}{\|A\|_2^2}\right) \|r_k\|_2^2$ (Eisenstat, Elman and Schultz 1983), so restarted GMRES converges.

**Floating point.** With modified Gram-Schmidt in L5, the computed solution is backward stable: when $A$ is not too close to singular ($\sigma_{\min}(A) \gg n^2 u \|A\|_F$, a hypothesis stated in Paige, Rozložník and Strakoš 2006), there is a step $k \le n$ at which $\hat x_k$ has normwise backward error $\|b - A \hat x_k\|_2 / (\|A\|_F \|\hat x_k\|_2 + \|b\|_2) = O(n^{c} u)$ for a small constant $c$. The Arnoldi vectors lose orthogonality as the residual decreases, but only once the backward error is already small. This is a theorem, not just an observation; the constant is worst case and pessimistic. The forward error is then of order $\kappa(A)$ times the backward error. Classical Gram-Schmidt without reorthogonalization loses this guarantee. The test file checks the backward error on the [Hilbert matrix](/hilbert-matrix/) $H_8$: it is below $100 n u$, while the forward error is about $\kappa(H_8) u$.

## Complexity

Proof in [proofs/complexity.md](proofs/complexity.md). Step $j$ costs one matvec ($2 z$ flops), $j$ inner products and $j$ vector updates in L5 ($4 j n$ flops), a norm, a scaling and $O(j)$ flops for the rotations. So $k$ steps of full GMRES cost $k$ matvecs plus $2 k^2 n + O(k n)$ flops, and storage of $k + 1$ basis vectors, $(k + 1) n$ words. GMRES($m$) caps both at $O(m n)$ per step and $(m + 1) n$ words. Forming $x$ in L9 costs $2 j n$ flops once per cycle.

For a sparse $A$ with a few nonzeros per row, the Gram-Schmidt work dominates the matvec once $j$ exceeds about $z / (2n)$. That work is a sequence of inner products, each a global reduction that reads $n$ words for $2 n$ flops, so on modern hardware it is bound by memory traffic and, in parallel, by synchronization latency, not by flops. Variants that use classical Gram-Schmidt with reorthogonalization, or block (s-step) orthogonalization, do fewer passes over memory for the same flops.

## Properties

- **Optimal in the 2-norm of the residual** over $x_0 + \mathcal K_k$, for any nonsingular $A$, using only matvecs with $A$ (no $A^T$).
- **Monotone residuals**: $\|r_{k+1}\|_2 \le \|r_k\|_2$; stagnation (equality) is possible, even for $k < n - 1$.
- **No serious breakdown**: the only breakdown, $h_{j+1,j} = 0$, is lucky (the solution is found) when $A$ is nonsingular.
- **Long recurrences**: cost and storage grow with $k$. By the Faber-Manteuffel theorem no method can be both optimal and short-recurrence for general $A$.
- **Eigenvalues do not tell the whole story** for nonnormal $A$: Greenbaum, Pták and Strakoš (1996) showed that any nonincreasing sequence of residual norms is attained by some $A$ with any prescribed nonzero eigenvalues.

## Variants and improvements

- **Preconditioned GMRES.** Left preconditioning applies GMRES to $M^{-1} A x = M^{-1} b$ and minimizes the preconditioned residual; right preconditioning solves $A M^{-1} y = b$, $x = M^{-1} y$, and minimizes the true residual. [ILU](/incomplete-lu-factorization/) is the usual choice for sparse nonsymmetric $A$.
- **Flexible GMRES** (FGMRES, Saad 1993) allows a different preconditioner at each step, at the cost of storing $M_j^{-1} v_j$ as well.
- **Householder GMRES** (Walker 1988) orthogonalizes with [Householder reflections](/householder-reflections/), for orthogonality to about $u$ at twice the cost.
- **Deflated and augmented restarting** (GMRES-DR, GCRO-DR) keep approximate eigenvectors across restarts to cure the stagnation caused by small eigenvalues.
- **MINRES** is the symmetric specialization, with three-term recurrences; GCR and ORTHOMIN are mathematically equivalent forms that store two vectors per step.
- **Short-recurrence alternatives** for nonsymmetric $A$: [BiCG](/biconjugate-gradient/), QMR, CGS, [BiCGSTAB](/bicgstab/), IDR(s). They use $O(n)$ memory but give up monotone residuals.
- **Mixed precision**: GMRES-based [iterative refinement](/iterative-refinement/) (Carson and Higham 2017) uses a low precision LU as preconditioner.

## When to use it

Use GMRES for nonsymmetric or indefinite sparse systems when a good preconditioner keeps the number of steps small (tens, not thousands), so the growing cost does not matter; it is the most robust Krylov method and the default in most libraries. For SPD matrices use [CG](/conjugate-gradient-method/), and for symmetric indefinite ones MINRES, which have the same optimality with $O(n)$ memory. If memory forbids a large restart length and GMRES($m$) stagnates, try BiCGSTAB or IDR(s), or improve the preconditioner.

## Pitfalls

- **Restart stagnation.** GMRES($m$) can stall forever: for $A = \begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}$ and $r_0 = e_1$, $A r_0 \perp r_0$, so GMRES(1) never moves while full GMRES finishes in two steps. Convergence of GMRES($m$) is guaranteed only under extra hypotheses such as a positive definite symmetric part.
- **Updated versus true residual.** $|g_{j+1}|$ is the residual of the least squares problem, not of the computed $x$; in floating point they agree only down to the level of the backward error. Check $\|b - A \hat x\|_2$ before declaring success.
- **Classical Gram-Schmidt.** Without reorthogonalization the basis loses orthogonality quickly and the least squares solution can be wrong; use MGS or CGS2.
- **Left preconditioning changes the stopping test**: a small $\|M^{-1} r\|$ need not mean a small $\|r\|$ when $M$ is ill conditioned.
- **Singular A.** For singular $A$, GMRES may break down with $\rho = 0$ before reaching a solution even when $b$ is in the range (Brown and Walker 1997); report it instead of dividing by zero.

## Implementations

## History

Krylov subspace methods for nonsymmetric systems that minimize the residual go back to the generalized conjugate residual family of Eisenstat, Elman and Schultz (1983) and to Axelsson's work, but those methods could break down or needed many stored vectors. Saad had used the Arnoldi process for linear systems as the full orthogonalization method (FOM, 1981). Saad and Schultz (1986) combined Arnoldi with an incrementally updated QR factorization of the Hessenberg matrix and named the result GMRES. Walker (1988) gave the Householder version, Saad (1993) the flexible version, and Paige, Rozložník and Strakoš (2006) finally proved the backward stability of MGS-GMRES, which had long been observed.

## References
