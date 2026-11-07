---
tag: PAMN7C
kind: algorithm
slug: implicitly-restarted-arnoldi
name: Implicitly restarted Arnoldi method
aliases:
- IRAM
- ARPACK method
- implicitly restarted Lanczos
area: numerical/eigenproblems
level: advanced
summary: Keeps an m-step Arnoldi factorization and compresses it to k steps with shifted QR steps on H_m. This restarts with a polynomial filter applied to the start vector, at no cost in products with A.
solves: [nonsymmetric-eigenproblem]
model: floating-point-model
complexity:
  vars: {n: "the order of A", k: "the number of wanted eigenvalues", m: "the maximum basis size, k < m", r: "the number of restarts", z: "the cost of one product with A"}
  time: {worst: O(r m^2 n + r m z + r m^3)}
  space: {worst: Θ(m n)}
  flops: {per_restart: "4(m^2 - k^2) n + 2m k n"}
  matvecs: {total: "k + (r + 1)(m - k)"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: true}
history:
  year: 1992
  people: [Danny C. Sorensen, Richard B. Lehoucq, Chao Yang]
  note: Sorensen introduced implicit restarting in 1992; Lehoucq, Sorensen and Yang released it as the ARPACK library in 1998.
prereqs: [arnoldi-iteration, qr-algorithm]
see_also: [lanczos-algorithm, nonsymmetric-eigenproblem, symmetric-eigenproblem, francis-double-shift-qr, subspace-iteration, chebyshev-polynomials, deflation, generalized-eigenvalue-problem]
sources:
  - paper: doi:10.1137/0613025
    title: D. C. Sorensen, Implicit application of polynomial filters in a k-step Arnoldi method, SIAM Journal on Matrix Analysis and Applications 13, 1992
    locator: pp. 357 to 385 (the implicit restart, exact shifts and convergence in the symmetric case)
  - book: isbn:9780898714074
    title: R. B. Lehoucq, D. C. Sorensen and C. Yang, ARPACK Users' Guide, Solution of Large-Scale Eigenvalue Problems with Implicitly Restarted Arnoldi Methods, SIAM, 1998
    locator: Chapter 4, The Implicitly Restarted Arnoldi Method (exact shifts, convergence test and deflation)
  - book: isbn:9781611970722
    title: Yousef Saad, Numerical Methods for Large Eigenvalue Problems, revised edition, SIAM Classics in Applied Mathematics 66, 2011
    locator: Chapter 7, Filtering and Restarting Techniques (implicit restarts and their relation to polynomial filters)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 10.5, Large Sparse Unsymmetric Problems (implicit restarting of the Arnoldi factorization and the Krylov-Schur method)
  - book: isbn:9780898714715
    title: Zhaojun Bai, James Demmel, Jack Dongarra, Axel Ruhe and Henk van der Vorst (eds.), Templates for the Solution of Algebraic Eigenvalue Problems, SIAM, 2000
    locator: Chapter 7, Non-Hermitian Eigenvalue Problems (the implicitly restarted Arnoldi method), and Chapter 4 (implicitly restarted Lanczos)
  - paper: "G. W. Stewart, A Krylov-Schur algorithm for large eigenproblems, SIAM Journal on Matrix Analysis and Applications 23, 2001, pp. 601 to 614"
    title: G. W. Stewart, A Krylov-Schur algorithm for large eigenproblems
    locator: restarting through a Schur form, equivalent to implicit restarting with exact shifts
---

The implicitly restarted Arnoldi method computes $k$ eigenvalues of a large matrix while storing at most $m$ basis vectors, with $k < m \ll n$. It extends an [Arnoldi](/arnoldi-iteration/) factorization from $k$ to $m$ steps, then applies $m - k$ shifted [QR](/qr-algorithm/) steps to the small Hessenberg matrix $H_m$ and keeps the first $k$ columns. The result is the $k$-step factorization that Arnoldi would have built from the filtered start vector $\psi(A) q_1$, with $\psi(z) = \prod_j (z - \mu_j)$, and no product with $A$ is spent on it. With the unwanted Ritz values as shifts, each restart removes their directions. This is the method of ARPACK, MATLAB's `eigs` and SciPy's `eigs` and `eigsh`.

## In plain words

Plain Arnoldi gets better with every step, but it must keep every vector it has built, and each new step costs more than the last. After some steps the memory is full. A restart throws the basis away and starts again from a better start vector, made by mixing the good approximate answers.

The implicit restart does this cheaply and safely. It looks at the approximate answers that are not wanted, and it uses them to remove from the start vector the parts that point toward them. It does this by working only on the small table of coefficients, not on the big matrix, and it keeps the part of the work that is still useful. Then it continues with ordinary Arnoldi steps until the memory is full again.

## The problem

**Notation.** $A \in \mathbb{C}^{n \times n}$ with eigenvalues $\lambda_1, \dots, \lambda_n$, ordered by the wanted criterion: by decreasing modulus ($|\lambda_1| \ge \dots \ge |\lambda_n|$, "LM") or by decreasing real part ("LR"). A $j$-step Arnoldi factorization is
$$A V_j = V_j H_j + f_j e_j^T, \qquad V_j^* V_j = I, \qquad V_j^* f_j = 0,$$
with $H_j$ upper Hessenberg. Its Ritz pairs are $(\theta_i, V_j y_i)$ with $H_j y_i = \theta_i y_i$ and $\|y_i\|_2 = 1$. $u$ is the unit roundoff.

Given a routine for $x \mapsto A x$, a start vector $b$, the number $k$ of wanted eigenvalues, a basis limit $m > k$ and a tolerance, compute $k$ Ritz pairs that approximate $\lambda_1, \dots, \lambda_k$ with residuals $\|A x_i - \theta_i x_i\|_2 \le \mathrm{tol} \cdot \max(|\theta_i|, u^{2/3})$, using $O(mn)$ storage.

## The algorithm

```pseudo id=main
IRAM(A, b, k, m, tol)
L1  build A V_k = V_k H_k + f_k e_kᵀ by k Arnoldi steps from b
L2  repeat
L3      extend to A V_m = V_m H_m + f_m e_mᵀ by m − k more Arnoldi steps
L4      compute the Ritz pairs (θᵢ, yᵢ) of H_m; sort them; wanted θ₁..θ_k, shifts μ₁..μ_{m−k}
L5      if ‖f_m‖₂ |e_mᵀ yᵢ| ≤ tol · max(|θᵢ|, u^{2/3}) for i ≤ k then return θᵢ, V_m yᵢ
L6      Q ← I_m
L7      for j ← 1 to m − k do
L8          factor H_m − μⱼ I = QⱼRⱼ;  H_m ← Qⱼ* H_m Qⱼ;  Q ← Q Qⱼ
L9      f_k ← (V_m Q e_{k+1}) h_{k+1,k} + f_m Q_{m,k}
L10     V_k ← V_m Q [e₁ … e_k];  H_k ← leading k × k block of H_m
```

Line L3 is plain Arnoldi, continued from $f_k$; it costs $m - k$ products with $A$. Lines L6 to L10 are the implicit restart; they use only $H_m$, $V_m$ and $f_m$. Each $Q_j$ is upper Hessenberg, so $Q$ has $m - k$ nonzero subdiagonals, and its last row is zero in columns $1, \dots, k - 1$. That is why truncation to $k$ columns in line L10 keeps an Arnoldi factorization with the residual of line L9. The shifts in line L4 are the exact shifts of Sorensen: the unwanted Ritz values. The implementation works in complex arithmetic, uses classical Gram-Schmidt run twice in line L3, and applies each shift by an explicit QR step with Givens rotations on the small matrix. ARPACK uses real double-shift steps for real matrices instead.

## Example

Take the $100 \times 100$ upper bidiagonal matrix of the [Arnoldi example](/arnoldi-iteration/), with diagonal $1, \dots, 100$ and superdiagonal 1, and a random start vector (seed 1, entries uniform in $[-1, 1]$). Ask for the $k$ eigenvalues of largest modulus with $\mathrm{tol} = 10^{-10}$:

| $k$ | $m$ | restarts | products with $A$ | largest error $\lvert\theta_i - \lambda_i\rvert$ |
|---|---|---|---|---|
| 1 | 6 | 45 | 231 | $3.2 \times 10^{-9}$ |
| 3 | 10 | 27 | 199 | $2.8 \times 10^{-9}$ |
| 4 | 12 | 19 | 164 | $2.7 \times 10^{-9}$ |
| 4 | 20 | 7 | 132 | $9.1 \times 10^{-10}$ |
| 4 | 30 | 4 | 134 | $1.7 \times 10^{-11}$ |
| 4 | 45 | 2 | 127 | $1.7 \times 10^{-13}$ |

Every run finds 100, 99, 98 and 97 (as many as asked). The errors are larger than the relative residual tolerance because $A$ is not normal; they are within the [eigenvalue condition number](/eigenvalue-condition-number/) times the residual. For comparison, unrestarted Arnoldi from the same vector still has relative residuals $1.2 \times 10^{-9}$, $2.1 \times 10^{-8}$, $5.4 \times 10^{-7}$ and $1.2 \times 10^{-6}$ for the top four Ritz values after 60 steps, so it would need more than 60 stored vectors. With $m = 12$ the restarted method needs only 12 vectors and 164 products. A larger $m$ reduces the number of restarts and products, at more storage and more orthogonalization work per restart.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md).

1. **The factorization survives the restart.** If $A V_m = V_m H_m + f_m e_m^T$ is an Arnoldi factorization, then after lines L6 to L10, $A V_k^+ = V_k^+ H_k^+ + f_k^+ e_k^T$ is again one: $V_k^+$ has orthonormal columns, $H_k^+$ is upper Hessenberg and $V_k^{+*} f_k^+ = 0$.
2. **Polynomial filter.** The new first basis vector is $v_1^+ = \psi(A) v_1 / \|\psi(A) v_1\|_2$ with $\psi(z) = \prod_{j=1}^{m-k} (z - \mu_j)$, up to a scalar of modulus one. By uniqueness of the Arnoldi factorization from a given unit start vector, the restart gives exactly the $k$ steps of Arnoldi from $\psi(A) v_1$, and $\operatorname{span}(V_k^+) = \psi(A) K_k(A, v_1)$.
3. **Exact shifts.** If the shifts are the $m - k$ unwanted eigenvalues of $H_m$ and every intermediate Hessenberg matrix stays unreduced, then the eigenvalues of $H_k^+$ are the $k$ wanted Ritz values. No wanted information is lost.
4. **Stopping test.** By the Arnoldi residual identity, $\|A x_i - \theta_i x_i\|_2 = \|f_m\|_2 |e_m^T y_i|$, so line L5 tests backward errors exactly.
5. **Termination.** The implementation stops after a fixed maximum number of restarts, or at a breakdown, which means that an invariant subspace was found and the Ritz pairs are exact. Convergence itself is not guaranteed for general $A$. For Hermitian $A$ with exact shifts, Sorensen (1992) proved that the wanted Ritz values converge. A start vector deficient in the wanted directions, or a wanted set that splits a cluster, can stall the iteration.

## Complexity

- **Products with $A$.** $k$ for line L1 and $m - k$ per pass through line L3, so $k + (r + 1)(m - k)$ in total after $r$ restarts. This count is exact; $r$ itself is observed.
- **Orthogonalization.** Step $j$ costs $4 j n$ flops per Gram-Schmidt pass. Line L3 with two passes costs $8 n \sum_{j=k}^{m-1} j \approx 4 (m^2 - k^2) n$ flops per restart.
- **Restart.** Line L10 forms $k + 1$ combinations of $m$ vectors, $2 m (k + 1) n$ flops. Lines L6 to L8 and the Ritz pairs of L4 cost $O(m^3)$ flops, which is small when $m \ll n$.
- **Storage.** $(m + 1) n$ numbers for $V_m$ and $f_m$, plus $O(m^2)$. This is the point of the method: storage does not grow with the number of products.
- **Number of restarts.** It depends on the gap between wanted and unwanted eigenvalues, on the nonnormality of $A$ and on $m - k$. No useful a priori bound is known for general $A$. In the example, $r$ falls from 19 to 2 as $m$ grows from 12 to 45 at $k = 4$. ARPACK's guide recommends $m \ge 2k$ as a default.

## Properties

- **Product-free restart.** The filter $\psi(A)$ of degree $m - k$ is applied without any product with $A$; the $m - k$ products of the next extension are the only ones.
- **Accumulated filter.** After $r$ restarts the start vector is $\Psi(A) b$ for a polynomial $\Psi$ of degree $r(m - k)$, the product of all filters so far. Its roots are chosen adaptively by the Ritz values.
- **Stability.** The restart uses only unitary transformations of the small factorization, and it is backward stable in the same sense as the QR algorithm. An explicit restart, by contrast, forms a new start vector and loses the useful part of the old basis.
- **Hermitian case.** For Hermitian $A$, $H_m$ is real symmetric tridiagonal, and the method is the implicitly restarted Lanczos method of ARPACK's symmetric drivers (`eigsh` in SciPy).
- **Locking and purging.** Converged wanted Ritz values can be locked and converged unwanted ones purged, by [deflation](/deflation/) inside the factorization (Lehoucq and Sorensen 1996).

## Variants and improvements

- **Krylov-Schur** (Stewart 2001): restart through a Schur form of $H_m$, reorder it so that wanted Ritz values come first, and truncate. With exact shifts this is mathematically equivalent and is simpler to make robust; SLEPc uses it by default.
- **Other shifts.** Any shifts can be used. Leja points or the roots of a scaled [Chebyshev polynomial](/chebyshev-polynomials/) on a region that holds the unwanted spectrum give a filter with known decay, as in Saad's polynomial acceleration.
- **Shift and invert.** Apply the method to $(A - \sigma I)^{-1}$, or to $(A - \sigma B)^{-1} B$ for the [generalized eigenvalue problem](/generalized-eigenvalue-problem/), to find eigenvalues near $\sigma$.
- **Thick restart Lanczos** (Wu and Simon 2000): the Hermitian counterpart of Krylov-Schur.
- **Block versions** start from several vectors, for multiple eigenvalues and matrix-block products.
- **Real double-shift restarts.** For real $A$, ARPACK applies complex conjugate shift pairs in real arithmetic, as in the [Francis double-shift QR](/francis-double-shift-qr/) step.

## When to use it

Use implicitly restarted Arnoldi, or its Krylov-Schur form, for a few eigenvalues of a large sparse or structured matrix when only products $x \mapsto A x$ are available, or when a shift-and-invert factorization is affordable. Typical tasks are the eigenvalues of largest real part for stability of large dynamical systems, the dominant eigenvalues of Markov chains and the lowest modes of large Hermitian matrices (through the Lanczos form). Prefer a dense method, such as the [QR algorithm](/qr-algorithm/), when $n$ is a few thousand or less and many eigenvalues are wanted. Prefer [subspace iteration](/subspace-iteration/) or block methods when products with blocks of vectors are much cheaper than single products.

## Pitfalls

- **Splitting a cluster.** If $k$ cuts through a group of nearly equal or defective eigenvalues, the shifts remove part of the wanted group at every restart. In the implementation's tests, a $3 \times 3$ Jordan block with eigenvalue 4 stalls for 50 restarts with $k = 1$, $m = 6$, and converges in 3 restarts with $k = 3$; the eigenvalue errors are then about $5 \times 10^{-6}$, near the cube root of the residual.
- **Too small $m - k$.** With one or two shifts per restart the filter is weak and the number of restarts grows sharply, as in the first row of the example.
- **Interior eigenvalues without shift and invert.** "Smallest modulus" for a matrix with eigenvalues spread around zero converges very slowly, because Krylov methods find outer eigenvalues first. Factor $A - \sigma I$ and ask for the largest eigenvalues of the inverse instead.
- **Trusting the residual for a nonnormal matrix.** The test of line L5 bounds the backward error. The forward error can be larger by the eigenvalue condition number, as in the example.
- **Losing orthogonality.** The method needs a basis orthogonal to working accuracy. Use a second Gram-Schmidt pass or the DGKS correction in line L3, as ARPACK does.
- **Shifts close to wanted eigenvalues.** If an unwanted Ritz value lies near a wanted eigenvalue, the filter damps the wanted direction. ARPACK reorders and adjusts the split between wanted and unwanted values to avoid this.

## Implementations

## History

Restarting Krylov methods for nonsymmetric eigenproblems had been studied by Saad in the early 1980s, by explicit restarts with filtered start vectors, and Karush had restarted Lanczos as early as 1951. Danny Sorensen observed in 1992 that the restart could be done implicitly, by shifted QR steps on the small Hessenberg matrix, which keeps the factorization and avoids forming the filter polynomial. Richard Lehoucq, Sorensen and Chao Yang developed deflation and robust shift strategies and released ARPACK, documented in its 1998 users' guide. G. W. Stewart's Krylov-Schur method of 2001 gave an equivalent formulation that is easier to implement. ARPACK is the engine behind `eigs` in MATLAB, Octave and SciPy.

## References
