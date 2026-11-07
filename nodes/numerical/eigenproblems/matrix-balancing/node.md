---
tag: T97X37
kind: algorithm
slug: matrix-balancing
name: Matrix balancing
aliases:
- Parlett-Reinsch balancing
- diagonal scaling
- Osborne balancing
area: numerical/eigenproblems
level: advanced
summary: A diagonal similarity D^-1 A D, with powers of 2 on the diagonal, that evens out row and column norms before an eigenvalue computation. It is exact in floating point and can shrink the norm a lot.
solves: [nonsymmetric-eigenproblem]
model: floating-point-model
complexity:
  vars: {n: "the order of A", s: "the number of sweeps"}
  time: {worst: O(s n^2)}
  space: {extra: Θ(n)}
  flops: {worst: "6 s n^2"}
properties: {deterministic: true, in_place: true, recursive: false, iterative: true}
history:
  year: 1969
  people: [Beresford N. Parlett, Christian Reinsch]
  note: Parlett and Reinsch published the radix-based balancing procedure in 1969, refining Osborne's 1960 iteration; it became EISPACK's balanc and LAPACK's xGEBAL.
prereqs: [similarity-transformation, nonsymmetric-eigenproblem]
see_also: [qr-algorithm, hessenberg-reduction, condition-number, eigenvalue-condition-number, backward-error-analysis, schur-decomposition, matrix-norms, pseudospectrum]
sources:
  - paper: "B. N. Parlett and C. Reinsch, Balancing a matrix for calculation of eigenvalues and eigenvectors, Numerische Mathematik 13, 1969"
    title: Balancing a matrix for calculation of eigenvalues and eigenvectors
    locator: Numer. Math. 13 (1969), pp. 293 to 304
  - paper: "E. E. Osborne, On pre-conditioning of matrices, Journal of the ACM 7(4), 1960"
    title: On pre-conditioning of matrices
    locator: J. ACM 7(4) (1960), pp. 338 to 345
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 7.5.7, Balancing
  - paper: "D. S. Watkins, A case where balancing is harmful, Electronic Transactions on Numerical Analysis 23, 2006"
    title: A case where balancing is harmful
    locator: ETNA 23 (2006), pp. 1 to 4
  - paper: "R. James, J. Langou and B. R. Lowery, On matrix balancing and eigenvector computation, arXiv:1401.5766, 2014"
    title: On matrix balancing and eigenvector computation
    locator: arXiv:1401.5766 (2014), Sections 2 to 4
  - paper: "T.-Y. Chen and J. W. Demmel, Balancing sparse matrices for computing eigenvalues, Linear Algebra and its Applications 309, 2000"
    title: Balancing sparse matrices for computing eigenvalues
    locator: Linear Algebra Appl. 309 (2000), pp. 261 to 287
---

Matrix balancing replaces a square matrix $A$ by $B = D^{-1} A D$, where $D$ is diagonal with powers of the machine radix on its diagonal, chosen so that for every index $i$ the off-diagonal parts of row $i$ and column $i$ have about the same norm. Because it is a [similarity transformation](/similarity-transformation/), $B$ has the same eigenvalues as $A$; because the scale factors are powers of 2, every scaled entry is computed exactly, so $B$ has *exactly* the eigenvalues of $A$, with no rounding error at all. The point is that backward stable eigenvalue algorithms such as the [QR algorithm](/qr-algorithm/) make errors of size $u \|B\|$ rather than $u \|A\|$, and for badly scaled (graded) matrices $\|B\|$ can be smaller than $\|A\|$ by many orders of magnitude. The Parlett-Reinsch procedure sweeps over the indices, rescales one row and column at a time, and stops when a full sweep changes nothing; it costs $O(n^2)$ per sweep, negligible against the $O(n^3)$ of the eigenvalue computation that follows.

## In plain words

Some tables of numbers have huge entries in one corner and tiny ones in another, only because of the units in which things were measured. A method that finds the special numbers of the table makes small mistakes compared with the biggest entry, so the tiny entries get swamped. Balancing changes the units: it multiplies one row by a number and divides the matching column by the same number, which leaves the special numbers alone. It picks these numbers so that each row and its matching column end up about the same size. It only uses factors of two, which a computer can apply with no mistake at all.

## The problem

**Notation.** $A \in \mathbb R^{n \times n}$ (or complex), $D = \operatorname{diag}(d_1, \dots, d_n)$ with $d_i = \beta^{e_i}$ for the radix $\beta$ (2 in binary arithmetic) and integers $e_i$. For the current matrix $B$, $c_i = \sum_{j \ne i} |b_{ji}|$ and $r_i = \sum_{j \ne i} |b_{ij}|$ are the off-diagonal 1-norms of column $i$ and row $i$, and $S(B) = \sum_{i \ne j} |b_{ij}|$ is the total off-diagonal mass, so $S = \sum_i c_i = \sum_i r_i$. $u$ is the unit roundoff. A matrix is irreducible when its directed graph (an edge $i \to j$ for each $a_{ij} \ne 0$, $i \ne j$) is [strongly connected](/strongly-connected-graph/).

**Input.** A square matrix $A$, the radix $\beta$, and a cap on the number of sweeps.

**Output.** $B = D^{-1} A D$ and the vector $d$, with $\operatorname{spec}(B) = \operatorname{spec}(A)$ exactly. On CONVERGED, no single index $i$ can be rescaled by a power of $\beta$ so as to lower $c_i + r_i$ by 5 percent. Eigenvectors of $A$ are recovered as $x = D y$ from eigenvectors $y$ of $B$.

## The algorithm

```pseudo id=main
BALANCE(A, β, maxsweeps)
L1  d ← (1, …, 1)
L2  for sweep ← 1 to maxsweeps do
L3      done ← true
L4      for i ← 1 to n do
L5          c ← Σ_{j≠i} |a_ji|;  r ← Σ_{j≠i} |a_ij|           ▷ column and row norms, without the diagonal
L6          if c = 0 or r = 0 then continue                    ▷ nothing to balance against
L7          f ← the power of β with r/β ≤ c f² < r β           ▷ two short while loops, exact
L8          if c f + r / f < 0.95 (c + r) then                 ▷ accept only a real improvement
L9              column i ← f · column i;  row i ← row i / f;  d_i ← f d_i;  done ← false
L10     if done then return (A, d, sweep, CONVERGED)
L11 return (A, d, maxsweeps, NOT-CONVERGED)
```

Line L9 replaces $A$ by $F^{-1} A F$ with $F = \operatorname{diag}(1, \dots, f, \dots, 1)$; it multiplies $c$ by $f$, divides $r$ by $f$, and leaves the diagonal entry $a_{ii}$ alone. Line L7 makes the new column and row norms agree to within a factor of $\beta$: the scaled ratio $c f^2 / r$ lies in $[1/\beta, \beta)$, and among all powers of $\beta$ this choice minimizes $c f + r / f$. The factor 0.95 stops the sweeps from chasing tiny gains. LAPACK's xGEBAL first permutes the matrix to isolate eigenvalues that can be read off directly (rows or columns whose off-diagonal part is zero), and then balances the remaining block in the same way.

## Example

Take $S = \mathbf 1 \mathbf 1^T + \operatorname{diag}(0, 1, 2, 3)$, a symmetric matrix with ones off the diagonal and $1, 2, 3, 4$ on it, and grade it: $A = G S G^{-1}$ with $G = \operatorname{diag}(1, 10^3, 10^6, 10^9)$, so $a_{ij} = 1000^{i - j}$ off the diagonal (rounded to the nearest doubles). Then $\|A\|_F = 1.000001 \times 10^9$, and the characteristic polynomial of the stored $A$ is $t^4 - 10 t^3 + 29 t^2 - 28 t + 6$ up to the rounding of the entries, with eigenvalues $0.296090$, $1.392275$, $2.507749$, $5.803886$.

Balancing with $\beta = 2$ takes 3 sweeps and 7 accepted scalings and returns $d = (2^{-24}, 2^{-14}, 2^{-4}, 2^{6})$: consecutive ratios are $2^{10} = 1024$, the power of 2 nearest to the grading factor 1000. The balanced matrix is

$$B = \begin{pmatrix} 1 & 1.024 & 1.048576 & 1.073742 \\ 0.976563 & 2 & 1.024 & 1.048576 \\ 0.953674 & 0.976563 & 3 & 1.024 \\ 0.931323 & 0.953674 & 0.976563 & 4 \end{pmatrix}, \qquad \|B\|_F = 6.484215,$$

and its exact characteristic polynomial, computed in rational arithmetic, is identical to that of $A$. Running the implementation of the [QR algorithm](/qr-algorithm/) on both, the largest eigenvalue error is $4.1 \times 10^{-11}$ for $A$ and $8.3 \times 10^{-16}$ for $B$, in line with the bounds $u \|A\|_F = 1.1 \times 10^{-7}$ and $u \|B\|_F = 7.2 \times 10^{-16}$. These numbers come from a script and are checked by the tests.

## Correctness

The full proofs are in [proofs/correctness.md](proofs/correctness.md); the argument:

- **Exact similarity.** Each accepted step multiplies column $i$ by a power of $\beta$ and divides row $i$ by it. In floating point with radix $\beta$ this only changes exponents, so it is exact barring overflow and underflow, and the computed $B$ equals $D^{-1} A D$ exactly. Hence $\det(tI - B) = \det(tI - A)$ as polynomials, and the eigenvalues are unchanged, not merely perturbed by $O(u)$. The tests check the identity of the exact characteristic polynomials.
- **Each step lowers the off-diagonal mass.** Scaling index $i$ changes only the entries of row $i$ and column $i$ off the diagonal, so $S$ changes by $(c f + r / f) - (c + r) < -0.05 (c + r)$. So $S$ strictly decreases with every accepted step.
- **Termination.** The sweep cap bounds the work. Without the cap, for irreducible $A$ the procedure still stops: the bound $S(B) \le S(A)$ caps every exponent difference $e_k - e_j$ along an edge of the graph, strong connectivity then caps every difference in both directions, so only finitely many matrices $B$ can occur, and a strictly decreasing $S$ cannot cycle among them.
- **Local optimality at convergence.** On CONVERGED, for every $i$ with $c_i r_i \ne 0$ and every integer $m$, $c_i \beta^m + r_i \beta^{-m} \ge 0.95 (c_i + r_i)$, because the factor of line L7 is the best power of $\beta$ and was rejected. The tests check this for every index and every $m$ from $-8$ to $8$.

## Complexity

**Per sweep (counted from the pseudocode).** Line L5 reads $2(n - 1)$ entries for each $i$, about $4n^2$ flops per sweep with the absolute values, and each accepted scaling costs $2n$ multiplications, at most $2n^2$ per sweep, for at most $6 n^2$ flops per sweep. The loops of line L7 run $O(|\log_\beta(r / c)|)$ times.

**Number of sweeps.** No useful worst-case bound is known for this exact rule; the irreducible-case argument above is finite but not quantitative. In the tests, 200 random graded matrices of order 2 to 12 with grading up to $10^{\pm 8}$ needed at most 6 sweeps, 3.8 on average. Polynomial bounds for variants of Osborne's iteration were proved only recently (Ostrovsky, Rabani and Yousefi, 2017). In practice the cost is $O(n^2)$ times a small number, against the $10 n^3$ to $25 n^3$ of the [QR algorithm](/qr-algorithm/).

**Space.** In place, plus the vector $d$.

## Properties

- **Exact.** No rounding error is introduced: the eigenvalues of $B$ are those of the stored $A$.
- **Diagonal entries unchanged.** $b_{ii} = a_{ii}$, and so is the trace; the sparsity pattern is unchanged as well.
- **Symmetric and normal matrices are already balanced.** For a symmetric matrix $c_i = r_i$, line L7 gives $f = 1$, and nothing happens; balancing helps only nonnormal, badly scaled matrices.
- **Idempotent.** Balancing a balanced matrix accepts no scaling.
- **Not a minimizer.** The result is a local optimum one index at a time, not the minimum of $\|D^{-1} A D\|$ over all $D$, and only to within a factor of $\beta$.

## Variants and improvements

- **Osborne's iteration.** With 2-norms and real (not power of 2) factors $f = \sqrt{r_i / c_i}$, cycling over the indices converges, for irreducible $A$, to the $D$ that minimizes $\|D^{-1} A D\|_F$, at which every row and column have equal off-diagonal 2-norms (Osborne 1960). Parlett and Reinsch replaced the 2-norm by the cheaper 1-norm and rounded the factors to powers of the radix.
- **Permutation first.** Isolating eigenvalues by permutations, as xGEBAL does, gives a block triangular matrix whose middle block is balanced; this also shrinks the problem.
- **Norm used by LAPACK.** Following James, Langou and Lowery (2014), LAPACK 3.5.0 switched xGEBAL from 1-norms to 2-norms, which avoids some cases where balancing made the eigenvectors much less accurate.
- **Sparse and matrix-free balancing.** Chen and Demmel (2000) estimate the norms from products with random vectors, so that only products with $A$ and $A^T$ are needed, for use before Krylov methods.
- **Generalized problems.** For a pencil $(A, B)$, Ward's method scales rows and columns by two different diagonal matrices before the [QZ algorithm](/qz-algorithm/).

## When to use it

Balance by default before computing all eigenvalues of a dense nonsymmetric matrix with the [QR algorithm](/qr-algorithm/), as LAPACK's xGEEV does: it costs nothing worth mentioning and can gain many digits for graded matrices, matrices from models with mixed units, and companion matrices used for [polynomial root finding](/polynomial-root-finding/). Do not balance symmetric matrices (it does nothing), and switch it off when the small entries of $A$ carry no information, as in the pitfall below, or when the eigenvectors must have a small backward error in the original scaling.

## Pitfalls

- **Balancing can be harmful.** If $A$ has tiny entries that are themselves the result of rounding or noise, balancing scales them up to the size of the others and the eigenvalue algorithm treats the noise as significant. Watkins (2006) gives a matrix for which the balanced eigenvalues are much less accurate than the unbalanced ones.
- **Eigenvectors.** An eigenvector $y$ of $B$ with a small residual for $B$ gives $x = Dy$, whose residual for $A$ is scaled by $D$, and can be large relative to $\|A\| \|x\|$ when $D$ has a wide range. James, Langou and Lowery (2014) document this.
- **Reducible matrices.** Rows or columns with zero off-diagonal part must be skipped (line L6), or line L7 divides by zero; such matrices should be permuted first.
- **Overflow and underflow.** With extreme grading the factors can push entries out of range; LAPACK stops scaling an index when the factor would overflow or underflow.
- **Wrong radix.** On a decimal or hexadecimal machine the factors must be powers of that radix, or the scaling is no longer exact.

## Implementations

## History

E. E. Osborne proposed in 1960 to precondition a matrix for eigenvalue computation by a diagonal similarity that equalizes row and column norms, and showed that his iteration reduces the Frobenius norm. Beresford Parlett and Christian Reinsch turned it into the practical procedure of 1969, with 1-norms, powers of the radix and the 5 percent rule, published in the Handbook for Automatic Computation and adopted as EISPACK's balanc and later LAPACK's xGEBAL. Watkins (2006) and James, Langou and Lowery (2014) showed cases where balancing hurts, which led to the change of norm in LAPACK.

## References
