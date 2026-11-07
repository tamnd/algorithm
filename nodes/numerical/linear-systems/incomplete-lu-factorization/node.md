---
tag: YZPFA2
kind: algorithm
slug: incomplete-lu-factorization
name: Incomplete LU factorization
aliases:
- ILU
- ILU(0)
- ILU(p)
- ILUT
area: numerical/linear-systems
level: advanced
summary: LU with dropped fill-in, used as a sparse preconditioner.
model: floating-point-model
complexity:
  vars: {n: "the order of A", c: "the largest number of entries in a working row (for ILU(0), in a row of A)", f: "the number of nonzeros of L + U"}
  time: {worst: O(n c^2)}
  space: {extra: Θ(f)}
  flops: {solve: "2 f - n"}
properties: {deterministic: true, in_place: false, recursive: false}
prereqs: [lu-decomposition, sparse-matrix, fill-in, preconditioning]
see_also: [incomplete-cholesky-factorization, gmres, bicgstab, preconditioning, fill-in, compressed-sparse-row, multigrid-method, sparse-linear-systems]
sources:
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 10.3, ILU Factorization Preconditioners (Algorithm 10.4 ILU(0) in IKJ form, Section 10.3.3 level of fill and Algorithm 10.5 ILU(p), Section 10.3.4 modified ILU); Section 10.4, Threshold Strategies and ILUT
  - paper: doi:10.1090/S0025-5718-1977-0438681-4
    title: J. A. Meijerink and H. A. van der Vorst, An iterative solution method for linear systems of which the coefficient matrix is a symmetric M-matrix, Mathematics of Computation 31(137), 1977
    locator: pp. 148 to 162 (Theorem 2.3, existence of incomplete factorizations of M-matrices for any pattern, and the regular splitting)
  - paper: "Howard C. Elman, A stability analysis of incomplete LU factorizations, Mathematics of Computation 47(175), 1986"
    title: H. C. Elman, A stability analysis of incomplete LU factorizations
    locator: pp. 191 to 217 (unstable triangular solves for convection-dominated problems)
  - paper: doi:10.1002/nla.1680010405
    title: Yousef Saad, ILUT, a dual threshold incomplete LU factorization, Numerical Linear Algebra with Applications 1(4), 1994
    locator: pp. 387 to 402 (dropping by size with a row fill limit)
  - paper: doi:10.1007/BF01932020
    title: Ivar Gustafsson, A class of first order factorization methods, BIT 18, 1978
    locator: pp. 142 to 156 (modified incomplete factorization and the h^-1 condition number for the model problem)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 40, Preconditioning (incomplete factorizations)
  - paper: doi:10.1137/140968896
    title: Edmond Chow and Aftab Patel, Fine-grained parallel incomplete LU factorization, SIAM Journal on Scientific Computing 37(2), 2015
    locator: pp. C169 to C193 (ILU as a fixed point of the pattern equations, computed by sweeps)
---

An incomplete LU factorization computes a unit lower triangular $L$ and an upper triangular $U$ that are sparse, with $A \approx L U$, by running Gaussian elimination but throwing away fill-in that falls outside an allowed pattern. ILU(0) keeps exactly the pattern of $A$, so $L + U$ costs no more storage than $A$ and $(L U)_{ij} = a_{ij}$ on that pattern; ILU($p$) keeps fill up to level $p$; ILUT drops entries by size. The product $M = L U$ is never formed. It is used as a [preconditioner](/preconditioning/): a Krylov method such as [GMRES](/gmres/) or [BiCGSTAB](/bicgstab/) works with $M^{-1} A$, and applying $M^{-1}$ costs one sparse forward and one backward substitution. For M-matrices the factorization exists for any pattern and gives a convergent splitting (Meijerink and van der Vorst 1977); for general matrices it can break down or produce triangular factors so ill conditioned that the preconditioner is useless.

## In plain words

Exact elimination on a sparse matrix tends to fill in many zeros with nonzero numbers, which costs memory and time. Incomplete LU does the same elimination but simply refuses to create most of these new numbers: it keeps only the positions that were nonzero to begin with, or a few more. The result is not an exact factorization, only a cheap approximate one.

That approximate factorization is then used to guide an iterative solver, which removes the remaining error in far fewer steps than without it.

## The problem

**Notation.** As in [solving linear systems](/linear-system-solving/): $A \in \mathbb{R}^{n \times n}$ sparse, $u = 2^{-53}$, $\kappa(\cdot)$ the condition number. $P \subseteq \{1, \dots, n\}^2$ is the allowed pattern, containing the diagonal; for ILU(0), $P$ is the set of $(i, j)$ with $a_{ij} \ne 0$. $R = L U - A$ is the residual matrix of the factorization. $f$ is the number of nonzeros of $L + U$ (strict lower part of $L$ plus all of $U$).

Given $A$ in [CSR](/compressed-sparse-row/) form and a fill rule, compute $L$ (unit lower) and $U$ (upper) with nonzeros only in $P$ such that
$$(L U)_{ij} = a_{ij} \quad \text{for all } (i, j) \in P,$$
or report a zero pivot. Then $R$ is zero on $P$: the factorization is exact where it is allowed to be.

## The algorithm

The IKJ (row) form of elimination processes row $i$ against the earlier rows of $U$. Levels of fill measure how indirect a fill entry is: original nonzeros have level 0, and an entry created from $l_{ik}$ and $u_{kj}$ gets level $\mathrm{lev}_{ik} + \mathrm{lev}_{kj} + 1$ (Saad, Section 10.3.3). ILU($p$) keeps entries of level at most $p$.

```pseudo id=main
ILU(A, p)                                        ▷ w is a sparse working copy of row i of A
L1  for i ← 1 to n do
L2      for each k < i present in w, in increasing order, with lev_ik ≤ p do
L3          w_k ← w_k / u_kk                     ▷ the multiplier l_ik
L4          for each j > k with u_kj ≠ 0 do
L5              if w_j is present then w_j ← w_j − w_k u_kj;  lev_ij ← min(lev_ij, lev_ik + lev_kj + 1)
L6              else if p > 0 then w_j ← −w_k u_kj;  lev_ij ← lev_ik + lev_kj + 1      ▷ new fill
L7      drop entries with lev_ij > p;  L_i ← w_{j<i};  U_i ← w_{j≥i};  if u_ii = 0 then return ZERO-PIVOT
```

The increasing order in L2 is kept with a heap, since L6 can create new columns $j < i$. For $p = 0$, L6 never fires and the code is ILU(0) (Saad, Algorithm 10.4). Applying $M^{-1}$ to a vector solves $L y = r$ forward and $U z = y$ backward.

## Example

The 5-point Laplacian on a $2 \times 2$ grid, unknowns numbered row by row:
$$A = \begin{pmatrix} 4 & -1 & -1 & 0 \\ -1 & 4 & 0 & -1 \\ -1 & 0 & 4 & -1 \\ 0 & -1 & -1 & 4 \end{pmatrix}.$$
Exact LU fills positions $(2, 3)$ and $(3, 2)$: eliminating row 1 from row 3 puts $-1/4$ at $(3, 2)$. ILU(0) drops it. Row by row:

- Row 2: $l_{21} = -1/4$, $u_{22} = 4 - 1/4 = 15/4$; the update would create $(2, 3)$, which is dropped.
- Row 3: $l_{31} = -1/4$, $u_{33} = 15/4$, and $(3, 2)$ is dropped.
- Row 4: $l_{42} = l_{43} = (-1)/(15/4) = -4/15$, $u_{44} = 4 - 4/15 - 4/15 = 52/15$.

So $L U - A = R$ has exactly two nonzeros, $r_{23} = r_{32} = 1/4$, both outside the pattern, as the theory requires. The exact factor has $u_{44} = 24/7 \approx 3.43$ against ILU's $52/15 \approx 3.47$. The test file checks this in rational arithmetic, and checks $(LU)_{ij} = a_{ij}$ on the pattern for 500 random sparse matrices.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md).

1. **Pattern equations.** In exact arithmetic, if no zero pivot occurs, the output satisfies $(L U)_{ij} = a_{ij}$ for all $(i, j)$ in the kept pattern, $L$ is unit lower triangular and $U$ upper triangular. If the kept pattern contains every fill entry (for instance $p \ge n - 1$), $L U = A$ is the exact LU factorization without pivoting.
2. **Termination.** Every row does finitely many updates; the code either returns $L$, $U$ or ZERO-PIVOT.
3. **Existence for M-matrices** (Meijerink and van der Vorst 1977, Theorem 2.3; quoted, not proved here). If $A$ is a nonsingular M-matrix, the incomplete factorization exists for any pattern containing the diagonal, all pivots are positive, $L$ and $U$ are M-matrices, and $A = L U - R$ with $R \ge 0$ is a regular splitting, so $\rho(I - (L U)^{-1} A) < 1$. Manteuffel (1980) extended existence to H-matrices. The test file observes that Richardson iteration $x \leftarrow x + M^{-1}(b - A x)$ converges on a convection-diffusion M-matrix, much faster than Jacobi.

There is no such guarantee for indefinite or strongly nonsymmetric $A$: pivots can be zero or tiny even when $A$ is well conditioned, as for $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$.

**Floating point and stability.** The computation is Gaussian elimination without pivoting restricted to a pattern, so each computed entry satisfies the usual rounding bound: $\hat L \hat U = A + R + \Delta$ on the pattern with $|\Delta| \le \gamma_c |\hat L| |\hat U|$, where $c$ is the number of terms in an entry (the same argument as for [LU](/lu-decomposition/); proved, worst case). The real danger is not rounding but instability of the triangular factors: Elman (1986) showed that for convection-dominated problems $\|L^{-1}\|$ and $\|U^{-1}\|$ can grow exponentially with $n$ although no pivot is small, so $M^{-1} r$ is dominated by amplified noise. A cheap diagnostic is $\|(L U)^{-1} e\|_\infty$ for $e = (1, \dots, 1)$, a lower bound for $\|M^{-1}\|_\infty$ (Chow and Saad 1997, observed).

## Complexity

Proof in [proofs/complexity.md](proofs/complexity.md). Row $i$ has at most $c$ entries in the working row; each multiplier $l_{ik}$ triggers at most $c$ updates (one per entry of $U_k$), and the heap costs $O(c \log c)$. So the factorization takes $O(n c^2)$ time and $\Theta(f)$ storage, and for ILU(0) on a matrix with at most $c$ nonzeros per row, $f = $ the number of nonzeros of $A$. Applying $M^{-1}$ costs $2 f - n$ flops, the same as about one matvec with $A$ for ILU(0).

The triangular solves are sequential recurrences: row $i$ needs the results of earlier rows. On parallel hardware they are limited by the length of the dependency chain (level scheduling) and by memory latency, not by flops; multicolor orderings shorten the chains at the cost of a weaker preconditioner, and iterative (Jacobi-sweep) triangular solves and fine-grained ILU (Chow and Patel 2015) trade exactness for parallelism.

## Properties

- **Exact on the pattern**: $R = L U - A$ vanishes on $P$; for ILU(0), $R$ is supported on the fill positions of the first elimination step that were dropped.
- **Ordering dependent**: different orderings of the unknowns give different $L$, $U$ and different quality; unlike for exact factorization, fill-reducing orderings such as [reverse Cuthill-McKee](/reverse-cuthill-mckee/) or minimum degree can make ILU(0) worse.
- **No pivoting** in the basic form; ILUTP adds column pivoting.
- **Symmetric case**: for symmetric positive definite $A$, the symmetric version is [incomplete Cholesky](/incomplete-cholesky-factorization/), with $U = D L^T$.
- **Model problem**: for the 2D Poisson matrix with mesh width $h$, $\kappa(M^{-1} A) = O(h^{-2})$ for ILU(0), the same order as $\kappa(A)$ with a smaller constant; modified ILU improves this to $O(h^{-1})$ (Gustafsson 1978; proved for the model problem with a diagonal perturbation).

## Variants and improvements

- **ILU($p$)**: level-of-fill dropping, computed symbolically first in production codes.
- **ILUT($\tau$, $m$)** (Saad 1994): drop entries smaller than $\tau$ times the row norm and keep at most $m$ per row in $L$ and in $U$; more robust for nonsymmetric problems, but the fill is less predictable.
- **MILU** (modified ILU): add the dropped entries to the diagonal, so that $L U e = A e$ (row sums preserved); best for elliptic problems, worse for others.
- **Crout ILU** (ILUC) computes a column of $L$ and a row of $U$ at a time and allows better dropping rules (Li, Saad and Chow 2003).
- **Multilevel ILU** (ARMS, ILUPACK) combines ILU with reordering and a Schur complement recursion, related to [algebraic multigrid](/algebraic-multigrid/).
- **Block ILU** for systems of PDEs, and **ILU smoothers** in [multigrid](/multigrid-method/).

## When to use it

Use ILU(0) or ILUT as a first preconditioner for sparse nonsymmetric systems from PDE discretizations with GMRES or BiCGSTAB; it is general, cheap and often reduces the number of iterations by a large factor. For symmetric positive definite problems use incomplete Cholesky or, at large scale, [multigrid](/multigrid-method/). For indefinite or saddle point systems, ILU without pivoting and reordering often fails; use ILUTP, multilevel ILU or problem-specific preconditioners.

## Pitfalls

- **Zero or tiny pivots**: test the pivot against a tolerance relative to the row norm, and shift ($A + \alpha I$) or pivot when it fails; the code raises ZeroPivot for an exact zero.
- **Unstable factors**: a successful factorization can still give a useless $M$; check $\|(L U)^{-1} e\|$ before trusting it.
- **Ordering**: reorder for the preconditioner, not for exact factorization, and test the effect.
- **Too little fill** on hard problems: ILU(0) may barely help; increase $p$ or use ILUT.
- **Singular A**: for $\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$ the second pivot is $0$ and the code reports it; a nonzero pivot sequence does not imply $A$ is nonsingular, since dropped fill changes the pivots.

## Implementations

## History

Incomplete factorizations appear in Buleev (1960) and Varga (1960) for difference equations and in the strongly implicit procedure of Stone (1968), which dropped selected fill entries. Meijerink and van der Vorst (1977) gave the general framework for M-matrices with arbitrary patterns, and with conjugate gradients (ICCG) it became a standard method. Gustafsson (1978) introduced modified factorizations, Watts (1981) and others levels of fill, and Saad (1994) the threshold version ILUT. Elman (1986) analyzed the instability of the factors, and since the 2000s multilevel and parallel variants have dominated research.

## References
