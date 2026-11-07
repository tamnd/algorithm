---
tag: 19QPY7
kind: algorithm
slug: incomplete-cholesky-factorization
name: Incomplete Cholesky factorization
aliases:
- IC
- IC(0)
- ICCG
- incomplete Cholesky preconditioner
area: numerical/linear-systems
level: advanced
summary: Cholesky with dropped fill-in, used as a preconditioner for symmetric systems.
model: floating-point-model
complexity:
  vars: {n: "the order of A", c: "the largest number of nonzeros in a row of the lower triangle of A", f: "the number of nonzeros of L"}
  time: {worst: O(n c^2)}
  space: {extra: Θ(f)}
  flops: {solve: "4 f - 2 n"}
  square_roots: {worst: "n"}
properties: {deterministic: true, in_place: false, recursive: false}
prereqs: [cholesky-decomposition, positive-definite-matrix, sparse-matrix, fill-in]
see_also: [incomplete-lu-factorization, conjugate-gradient-method, preconditioning, cholesky-decomposition, fill-in, multigrid-method, diagonally-dominant-matrix, sparse-linear-systems]
sources:
  - paper: doi:10.1090/S0025-5718-1977-0438681-4
    title: J. A. Meijerink and H. A. van der Vorst, An iterative solution method for linear systems of which the coefficient matrix is a symmetric M-matrix, Mathematics of Computation 31(137), 1977
    locator: pp. 148 to 162 (existence of incomplete Cholesky for M-matrices with any pattern, and ICCG)
  - paper: doi:10.1016/0021-9991(78)90098-0
    title: David S. Kershaw, The incomplete Cholesky-conjugate gradient method for the iterative solution of systems of linear equations, Journal of Computational Physics 26(1), 1978
    locator: pp. 43 to 65 (the 4 by 4 SPD example with a negative pivot and the diagonal fix)
  - paper: doi:10.1090/S0025-5718-1980-0559195-7
    title: Thomas A. Manteuffel, An incomplete factorization technique for positive definite linear systems, Mathematics of Computation 34(150), 1980
    locator: pp. 473 to 497 (the shifted factorization of A + alpha diag(A) and existence for H-matrices)
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 10.3, ILU Factorization Preconditioners (the symmetric case); Section 10.3.4, Modified ILU; Section 9.2, Preconditioned Conjugate Gradient
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 11.5.6 (incomplete Cholesky preconditioners)
  - paper: doi:10.1137/S1064827597327334
    title: Chih-Jen Lin and Jorge J. Moré, Incomplete Cholesky factorizations with limited memory, SIAM Journal on Scientific Computing 21(1), 1999
    locator: pp. 24 to 45 (fill by memory budget and adaptive shifts)
---

Incomplete Cholesky factorization computes a sparse lower triangular $L$ with $L L^T \approx A$ for a symmetric positive definite sparse matrix $A$, by running the [Cholesky decomposition](/cholesky-decomposition/) but discarding fill-in outside an allowed pattern. In the zero fill version IC(0), $L$ has the pattern of the lower triangle of $A$ and $(L L^T)_{ij} = a_{ij}$ on that pattern. Used as a preconditioner $M = L L^T$ for the [conjugate gradient method](/conjugate-gradient-method/) it gives ICCG, one of the most used solvers for elliptic PDEs since Meijerink and van der Vorst (1977) proved that it exists for every M-matrix. For a general SPD matrix it can break down with a nonpositive pivot: Kershaw (1978) gave a $4 \times 4$ example, and the standard remedy is to factor a shifted matrix $A + \alpha \operatorname{diag}(A)$.

## In plain words

Exact Cholesky on a sparse matrix fills many zero positions with nonzeros. Incomplete Cholesky does the same computation but keeps only the positions that were nonzero in the original matrix, or a few more, and ignores everything else. The result is a cheap triangular factor that is only roughly right.

It is used to speed up the conjugate gradient method: each step solves with the cheap factor, which steers the method so that it needs far fewer steps. Sometimes the shortcut fails with a negative number under a square root, and then one adds a little to the diagonal and tries again.

## The problem

**Notation.** As in [solving linear systems](/linear-system-solving/): $A \in \mathbb{R}^{n \times n}$ symmetric, $u = 2^{-53}$, $\gamma_n = n u/(1 - n u)$, $\kappa(\cdot)$ the condition number. $P$ is the lower pattern, the set of $(i, j)$ with $j \le i$ and $a_{ij} \ne 0$ (for IC(0)), always containing the diagonal. $M = L L^T$ is the preconditioner and $R = L L^T - A$. $f$ is the number of nonzeros of $L$.

Given $A$ in [CSR](/compressed-sparse-row/) form (both triangles), compute $L$ lower triangular with nonzeros only in $P$, positive diagonal, and
$$(L L^T)_{ij} = a_{ij} \quad \text{for all } (i, j) \in P,$$
or report a nonpositive pivot (BREAKDOWN).

## The algorithm

Row (up-looking) form: row $i$ of $L$ is computed from the earlier rows by a sparse triangular solve restricted to the pattern.

```pseudo id=main
IC0(A, α)                                         ▷ α ≥ 0 is a diagonal shift (α = 0 gives IC(0))
L1  for i ← 1 to n do
L2      for each j < i with (i, j) ∈ P, in increasing order do
L3          s ← a_ij − Σ l_ik l_jk over k < j with (i, k) ∈ P and (j, k) ∈ P
L4          l_ij ← s / l_jj
L5      d ← (1 + α) a_ii − Σ_{j < i} l_ij²
L6      if d ≤ 0 then return BREAKDOWN at row i
L7      l_ii ← √d
```

Applying $M^{-1}$ to a vector is a forward sweep with $L$ and a backward sweep with $L^T$; the implementation does the second one column-oriented on the rows of $L$, so $L^T$ is never stored.

## Example

The $2 \times 2$ grid Laplacian of the [ILU](/incomplete-lu-factorization/) page,
$$A = \begin{pmatrix} 4 & -1 & -1 & 0 \\ -1 & 4 & 0 & -1 \\ -1 & 0 & 4 & -1 \\ 0 & -1 & -1 & 4 \end{pmatrix}.$$
IC(0) gives $l_{11} = 2$, $l_{21} = l_{31} = -1/2$, $l_{22} = l_{33} = \sqrt{15}/2$ (the entry $(3, 2)$, which exact Cholesky would fill with $-1/(2\sqrt{15})$, is dropped), $l_{42} = l_{43} = -1/l_{22} = -2/\sqrt{15}$, and $l_{44} = \sqrt{4 - 4/15 - 4/15} = \sqrt{52/15}$. Squared pivots $4, 15/4, 15/4, 52/15$ are the diagonal of $U$ in ILU(0), as they must be: for symmetric $A$ the two factorizations are related by $L_{\mathrm{IC}} = L_{\mathrm{ILU}} D^{1/2}$ and $U = D L_{\mathrm{ILU}}^T$, with $D$ the diagonal of $U$.

**Kershaw's breakdown.** For
$$A = \begin{pmatrix} 3 & -2 & 0 & 2 \\ -2 & 3 & -2 & 0 \\ 0 & -2 & 3 & -2 \\ 2 & 0 & -2 & 3 \end{pmatrix},$$
which is SPD, the squared pivots of IC(0) are $3$, $5/3$, $3/5$ and then $3 - 4/3 - 20/3 = -5$: the last row has no common pattern with row 3, so nothing compensates the dropped fill and $d < 0$. The shift $\alpha = 0.3$ succeeds and $\alpha = 0.1$ still fails. The test file checks these values exactly.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md).

1. **Pattern equations.** If no breakdown occurs, $L$ is lower triangular with positive diagonal, its pattern is contained in $P$, and $(L L^T)_{ij} = (1 + \alpha \delta_{ij}) a_{ij}$ for $(i, j) \in P$. If $P$ is the full lower triangle, $L$ is the exact Cholesky factor of $A + \alpha \operatorname{diag}(A)$.
2. **Termination.** The code returns after $n$ rows, with $L$ or BREAKDOWN.
3. **Existence for M-matrices** (Meijerink and van der Vorst 1977; quoted). If $A$ is a symmetric M-matrix, every pivot $d$ is positive for any pattern $P$ containing the diagonal, and $A = L L^T - R$ with $R \ge 0$ is a regular splitting. Manteuffel (1980) extended existence to H-matrices (for instance strictly [diagonally dominant](/diagonally-dominant-matrix/) matrices with positive diagonal), and showed that for any SPD $A$ there is a shift $\alpha$ for which the factorization of $A + \alpha \operatorname{diag}(A)$ exists, since it becomes diagonally dominant for large $\alpha$.

**Floating point.** Each computed entry is the result of the usual Cholesky recurrence on fewer terms, so $\hat L \hat L^T = A + R + \Delta$ on the pattern with $|\Delta_{ij}| \le \gamma_{c+1} (|\hat L| |\hat L|^T)_{ij}$, $c$ the number of terms (the argument of Higham, Theorem 10.3; proved, worst case). The test file checks the full-pattern case on the [Hilbert matrix](/hilbert-matrix/) $H_8$ against this bound. Rounding can, in principle, turn a tiny positive pivot negative; dropping is the much larger perturbation in practice.

**Effect as a preconditioner** (observed and, for model problems, proved). For the 2D Poisson matrix with mesh width $h$, $\kappa(M^{-1} A) = O(h^{-2})$ as for $A$ itself, but with a much smaller constant; modified IC (MIC), which adds dropped fill to the diagonal, gives $O(h^{-1})$ (Gustafsson 1978). On a $20 \times 20$ grid the test file observes CG needing 64 iterations for a residual reduction of $10^{-8}$ and ICCG 24.

## Complexity

Proof in [proofs/complexity.md](proofs/complexity.md). Row $i$ has at most $c$ entries $l_{ij}$, and each needs a sparse dot product of two rows with at most $c$ entries, so the factorization takes $O(n c^2)$ time, $n$ square roots and $\Theta(f)$ storage; for IC(0), $f$ is the number of nonzeros in the lower triangle of $A$. Applying $M^{-1}$ costs two triangular solves, $4 f - 2 n$ flops, about the cost of one matvec with $A$.

As for ILU, the sequential dependencies of the triangular solves, and not the flops, limit parallel speed; the solves are memory bound, streaming $L$ twice per CG step.

## Properties

- **Symmetric positive definite preconditioner** when it exists, so it can be used with CG (unlike ILU for general matrices).
- **Exact on the pattern**: $R$ vanishes on $P$ (apart from the shift on the diagonal).
- **Ordering dependent**: the natural ordering usually works better for IC(0) than fill-reducing orderings; red-black ordering parallelizes but weakens it.
- **Not guaranteed for SPD matrices**: Kershaw's example shows that SPD alone does not imply existence.

## Variants and improvements

- **IC($p$)** by levels of fill and **ICT** by thresholds, as for [ILU](/incomplete-lu-factorization/).
- **Shifted IC** (Manteuffel 1980): factor $A + \alpha \operatorname{diag}(A)$, increasing $\alpha$ after each breakdown.
- **Modified IC** (Gustafsson 1978): lump dropped fill onto the diagonal so that $M e = A e$.
- **Limited memory IC** (Lin and Moré 1999): keep the largest entries in a fixed memory budget, with adaptive shifts.
- **Robust IC** (Ajiz and Jennings 1984): add dropped entries to both diagonals so that $M$ stays SPD whenever $A$ is.
- **Block and multilevel IC**, and **IC smoothers** in [multigrid](/multigrid-method/).

## When to use it

Use IC(0) with CG for sparse SPD systems from elliptic PDEs or networks when a simple, general preconditioner is wanted and multigrid is not available or not applicable. For very large elliptic problems, multigrid scales better, since ICCG still needs $O(h^{-1})$ iterations. For ill-conditioned problems far from M-matrices, use ICT or limited memory IC with shifts.

## Pitfalls

- **Breakdown**: test for $d \le 0$ and restart with a shift; never take the square root of a negative pivot or use $|d|$.
- **Indefinite or singular A**: the code reports BREAKDOWN, e.g. $d = 0$ for $\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$ and $d = -3$ for $\begin{pmatrix} 1 & 2 \\ 2 & 1 \end{pmatrix}$; a successful factorization does not prove that $A$ is positive definite.
- **Storing only one triangle** of $A$ is fine for the factorization but the CG matvec then needs both.
- **Scaling**: symmetric diagonal scaling of $A$ changes nothing in exact arithmetic for IC(0), but shifts $\alpha \operatorname{diag}(A)$ and thresholds should be relative to it.

## Implementations

## History

Incomplete factorizations of difference operators go back to Buleev and Varga (1960). Meijerink and van der Vorst (1977) defined incomplete Cholesky for general patterns, proved existence for M-matrices and combined it with CG; ICCG quickly became standard in reservoir and plasma simulation. Kershaw (1978) exhibited breakdown for SPD matrices and replaced bad pivots, Gustafsson (1978) introduced modified factorizations, and Manteuffel (1980) the shifted version. Later work added thresholds, memory limits and robust variants that cannot break down.

## References
