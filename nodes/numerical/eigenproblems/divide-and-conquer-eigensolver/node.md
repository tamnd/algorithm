---
tag: J2346G
kind: algorithm
slug: divide-and-conquer-eigensolver
name: Divide-and-conquer eigensolver
aliases:
- Cuppen's method
- divide and conquer for the symmetric tridiagonal eigenproblem
- tridiagonal divide and conquer
area: numerical/eigenproblems
level: advanced
summary: Split a symmetric tridiagonal matrix into two halves plus a rank-one term, solve the halves recursively, and merge by solving a secular equation. Fast in practice because of deflation.
solves: [tridiagonal-eigenproblem]
model: floating-point-model
complexity:
  vars: {n: "the order of the tridiagonal matrix T"}
  time: {worst: O(n^3), typical: O(n^2.3)}
  space: {worst: Θ(n^2)}
  flops: {vectors_no_deflation: "4n^3/3", values_only: "O(n^2)"}
properties: {deterministic: true, in_place: false, recursive: true, iterative: false}
history:
  year: 1981
  people: [Jan J. M. Cuppen, Jack J. Dongarra, Danny C. Sorensen, Ming Gu, Stanley C. Eisenstat]
  note: Cuppen proposed the method in 1981; Dongarra and Sorensen added deflation and a parallel code in 1987; Gu and Eisenstat made the eigenvectors numerically orthogonal in 1995.
prereqs: [tridiagonal-eigenproblem, secular-equation, deflation]
see_also: [symmetric-eigenproblem, tridiagonalization, mrrr-algorithm, bisection-eigenvalue-algorithm, qr-algorithm, cauchy-interlacing-theorem, golub-kahan-svd-algorithm, jacobi-eigenvalue-algorithm]
sources:
  - paper: doi:10.1007/BF01396757
    title: J. J. M. Cuppen, A divide and conquer method for the symmetric tridiagonal eigenproblem, Numerische Mathematik 36, 1981
    locator: pp. 177 to 195 (the rank-one tearing, the secular equation and the recursion)
  - paper: doi:10.1137/0908018
    title: J. J. Dongarra and D. C. Sorensen, A fully parallel algorithm for the symmetric eigenvalue problem, SIAM Journal on Scientific and Statistical Computing 8, 1987
    locator: pp. s139 to s154 (deflation by small z components and by rotations, the root finder)
  - paper: doi:10.1137/S0895479892241287
    title: M. Gu and S. C. Eisenstat, A divide-and-conquer algorithm for the symmetric tridiagonal eigenproblem, SIAM Journal on Matrix Analysis and Applications 16, 1995
    locator: pp. 172 to 191 (recomputing z by Loewner's formula, orthogonal eigenvectors, stability)
  - paper: doi:10.1007/BF01396012
    title: J. R. Bunch, C. P. Nielsen and D. C. Sorensen, Rank-one modification of the symmetric eigenproblem, Numerische Mathematik 31, 1978
    locator: pp. 31 to 48 (interlacing, the rational root finder for the secular equation)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 5.3.3, Divide-and-Conquer (the secular equation, deflation, Loewner's theorem and the cost)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.4, More Methods for Tridiagonal Problems (divide and conquer, rank-one tearing, the secular equation)
---

The divide-and-conquer eigensolver computes all eigenvalues and eigenvectors of a real symmetric tridiagonal matrix $T$. It writes $T$ as a block diagonal matrix with two tridiagonal halves plus a rank-one correction, solves both halves recursively, and then finds the eigenvalues of the merged problem $D + \rho z z^T$ as the roots of the [secular equation](/secular-equation/) $1 + \rho \sum_j z_j^2 / (d_j - \lambda) = 0$, one root in each gap between consecutive $d_j$. Eigenvectors follow from an explicit formula. Without [deflation](/deflation/) it costs $4n^3/3$ flops for the eigenvectors, mostly in matrix multiplication. With deflation, which is common, it is much faster in practice and the fastest LAPACK method for the full [tridiagonal eigenproblem](/tridiagonal-eigenproblem/) with vectors (`xSTEDC`). Numerically orthogonal eigenvectors need the Gu-Eisenstat trick of recomputing $z$ from the computed eigenvalues.

## In plain words

A tridiagonal matrix is a chain: each row talks only to its two neighbors. Cut the chain in the middle and you get two independent halves, plus a small correction for the one link you cut. Solve each half the same way, cutting it again, until the pieces have one row each.

To glue two solved halves back together, you need to know how the one cut link changes the answers. Each new eigenvalue lies between two old ones, so finding it means searching a known short interval for the root of one simple function. Often an old answer is already good enough, because the cut barely affects it, and then no search is needed at all. This shortcut is what makes the method fast.

## The problem

**Notation.** $T \in \mathbb{R}^{n \times n}$ is symmetric tridiagonal with diagonal $a_1, \dots, a_n$ and off-diagonal $b_1, \dots, b_{n-1}$. Its eigenvalues are $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_n$ with unit eigenvectors $q_1, \dots, q_n$, so $T = Q \Lambda Q^T$. $e_k$ is the $k$th unit vector and $u$ is the unit roundoff.

**Input.** $a$ and $b$.

**Output.** $\Lambda = \operatorname{diag}(\lambda_i)$ and an orthogonal $Q$ with $T Q = Q \Lambda$, up to rounding.

**The tearing.** With $m = \lfloor n/2 \rfloor$ and $\rho = b_m$,
$$T = \begin{pmatrix} T_1 & 0 \\ 0 & T_2 \end{pmatrix} + \rho\, v v^T, \qquad v = e_m + e_{m+1},$$
where $T_1$ is the leading $m \times m$ block with $a_m$ replaced by $a_m - \rho$, and $T_2$ is the trailing block with $a_{m+1}$ replaced by $a_{m+1} - \rho$. If $T_i = Q_i D_i Q_i^T$, then
$$T = Q (D + \rho z z^T) Q^T, \qquad Q = \operatorname{diag}(Q_1, Q_2), \quad D = \operatorname{diag}(D_1, D_2), \quad z = Q^T v,$$
and $z$ is the last row of $Q_1$ followed by the first row of $Q_2$.

## The algorithm

```pseudo id=main
DC-EIG(T)                  ▷ symmetric tridiagonal, diagonal a, off-diagonal b
L1  if n = 1 then return (a_1), (1)
L2  m ← ⌊n/2⌋;  ρ ← b_m;  T₁ ← T[1..m] with a_m − ρ;  T₂ ← T[m+1..n] with a_m+1 − ρ
L3  (D₁, Q₁) ← DC-EIG(T₁);  (D₂, Q₂) ← DC-EIG(T₂)
L4  d ← (D₁, D₂);  z ← (last row of Q₁, first row of Q₂);  Q ← diag(Q₁, Q₂)
L5  deflate: if |ρ z_i| is tiny, keep (d_i, Q e_i); if d_i ≈ d_j, rotate z so that z_j = 0 and keep (d_j, Q e_j)
L6  for each of the K remaining poles, solve 1 + ρ Σ z_j² / (d_j − λ) = 0 for λ_i in its interval
L7  ẑ_j ← sign(z_j) (Π_i (λ_i − d_j) / (ρ Π_i≠j (d_i − d_j)))^½      ▷ Loewner, Gu-Eisenstat
L8  s_i ← (D − λ_i I)⁻¹ ẑ / ‖(D − λ_i I)⁻¹ ẑ‖₂ for i = 1, …, K
L9  Q ← [Q_kept S, Q_deflated]       ▷ one matrix product, the main cost
L10 return the eigenvalues and the columns of Q, sorted
```

The implementation scales the merge so that $\|z\|_2 = 1$ ($\rho \leftarrow \rho \|z\|_2^2$), and it handles $\rho < 0$ by solving with $-D$ and $|\rho|$ and negating the roots. For $\rho > 0$ and sorted distinct poles $d_1 < \dots < d_K$, the roots satisfy $d_i < \lambda_i < d_{i+1}$, and the last one lies in $(d_K, d_K + \rho)$. Line L6 uses a safeguarded rational iteration in the style of Bunch, Nielsen and Sorensen: near the current point it models each half of the sum by a constant plus one pole term and takes the root of the model, falling back to bisection of the bracket. Every root is stored as $d_{\text{org}} + \tau$ with the nearer pole as origin, so the differences $d_j - \lambda_i = (d_j - d_{\text{org}}) - \tau$ in lines L7 and L8 are accurate. The deflation tolerance is $8u \max(\max_j |d_j|, \rho)$.

## Example

Take $n = 4$, $a = (2, 2, 2, 2)$ and $b = (1, 1, 1)$, with eigenvalues $2 + 2\cos(k\pi/5)$: $3.618034$, $2.618034$, $1.381966$, $0.381966$.

Tearing at $m = 2$ with $\rho = 1$ gives $T_1 = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}$ and $T_2 = \begin{pmatrix} 1 & 1 \\ 1 & 2 \end{pmatrix}$. Each is solved by one merge of two $1 \times 1$ pieces, and each has eigenvalues $(3 \pm \sqrt 5)/2 = 2.618034$ and $0.381966$. The top merge has
$$d = (0.381966,\ 2.618034,\ 0.381966,\ 2.618034), \qquad z = (-0.850651,\ -0.525731,\ -0.850651,\ -0.525731).$$
Every pole appears twice. After scaling to $\|z\|_2 = 1$ ($\rho = 2$), line L5 rotates each pair of equal poles so that one $z$ entry becomes zero, and two eigenpairs deflate: $0.381966$ and $2.618034$, with no root finding. The remaining secular equation has $K = 2$:
$$1 + 2\left(\frac{0.7236068}{0.3819660 - \lambda} + \frac{0.2763932}{2.6180340 - \lambda}\right) = 0,$$
with roots $1.381966$, between the two poles, and $3.618034$, above the top pole. They took 3 function evaluations in total. All four eigenvalues agree with $2 + 2\cos(k\pi/5)$ to $4u$ in relative terms.

Larger runs of the implementation:

| matrix | $n$ | merges | deflated | roots solved | evaluations per root | orthogonality |
|---|---|---|---|---|---|---|
| $\operatorname{tridiag}(-1, 2, -1)$ | 100 | 99 | 180 | 492 | 4.3 | $6.7 \times 10^{-16}$ |
| random Gaussian, seed 1 | 128 | 127 | 52 | 844 | 4.5 | $1.2 \times 10^{-15}$ |
| $W_{21}^+$ | 21 | 20 | 0 | 94 | 4.6 | $8.9 \times 10^{-16}$ |
| four glued $W_{11}^+$ | 44 | 43 | 78 | 166 | 4.4 | $6.7 \times 10^{-16}$ |

The Wilkinson matrix $W_{21}^+$ has its top two eigenvalues $10.746194182903$ only $7.1 \times 10^{-14}$ apart, and the computed eigenvectors are still orthogonal to $8.9 \times 10^{-16}$. That is the effect of line L7.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md).

1. **Tearing.** The identity $T = \operatorname{diag}(T_1, T_2) + \rho v v^T$ holds entrywise, and $T = Q (D + \rho z z^T) Q^T$ follows with $z = Q^T v$.
2. **Deflation.** If $z_i = 0$, then $(d_i, e_i)$ is an eigenpair of $D + \rho z z^T$. If $d_i = d_j$, a rotation in the $(i, j)$ plane commutes with $D$ and can zero $z_j$. The dropped quantities in line L5 are below the tolerance, a backward perturbation of size $O(u \|T\|_2)$.
3. **Secular equation and interlacing.** If every $z_j \ne 0$ and the $d_j$ are distinct, $\lambda$ is an eigenvalue of $D + \rho z z^T$ exactly when $f(\lambda) = 1 + \rho \sum_j z_j^2 / (d_j - \lambda) = 0$. The eigenvector is $(D - \lambda I)^{-1} z$, and for $\rho > 0$ there is exactly one root in each interval $(d_i, d_{i+1})$ and one in $(d_K, d_K + \rho \|z\|_2^2)$.
4. **Loewner's formula.** Given any $\lambda_1, \dots, \lambda_K$ that strictly interlace the $d_j$, the vector $\hat z$ of line L7 makes them the exact eigenvalues of $D + \rho \hat z \hat z^T$. So lines L7 and L8 compute exact eigenvectors of a nearby matrix. Because $\hat z$ is close to $z$ when the roots are accurate, the result is numerically orthogonal (Gu and Eisenstat 1995).
5. **Recursion.** Induction on $n$, with the base case $n = 1$.

## Complexity

- **Recursion.** The depth is $\lceil \log_2 n \rceil$, and there are $n - 1$ merges.
- **Eigenvectors, no deflation.** The product of line L9 at a merge of size $p$ costs $p^3$ flops, because $Q$ is block diagonal with two blocks of size $p/2$. Summing over the levels gives $n^3 (1 + 1/4 + 1/16 + \dots) = 4n^3/3$ flops. This is a proved count for the case without deflation. All other work is $O(n^2)$ per level.
- **Root finding.** Each root needs $O(K)$ flops per evaluation of $f$, so a merge of size $K$ costs $O(K^2)$ times the number of evaluations. The implementation needed 4.3 to 4.6 evaluations per root, the final check included. This is observed. LAPACK's root finder `xLAED4` uses a more refined scheme.
- **With deflation.** Deflation removes columns from line L9, and the cost falls with the square of the fraction kept. Deflation is very common in practice, and Demmel reports an observed cost of about $O(n^{2.3})$ flops on average for some matrix classes; this is typical behavior, not a bound.
- **Eigenvalues only.** $O(n^2)$ flops, but then [dqds](/dqds-algorithm/) or the Pal-Walker-Kahan QR are cheaper.
- **Full symmetric matrix.** After [tridiagonalization](/tridiagonalization/) ($4n^3/3$ flops), multiplying by the Householder $Q$ costs $2n^3$ more.

## Properties

- **Backward stable** with the Gu-Eisenstat eigenvectors: $T + E = \hat Q \hat \Lambda \hat Q^T$ with $\|E\|_2 = O(u \|T\|_2)$ and $\|\hat Q^T \hat Q - I\|_2 = O(n u)$.
- **Orthogonal eigenvectors even for clustered eigenvalues**, without reorthogonalization, unlike [inverse iteration](/inverse-iteration/).
- **Mostly matrix multiplication**, so it runs near peak speed on modern hardware, and the two halves are independent, which gives parallelism.
- **Recursive**, but with logarithmic depth.
- **Memory.** $O(n^2)$ workspace for the eigenvector matrices.

## Variants and improvements

- **Leaf solver.** LAPACK stops the recursion at blocks of order about 25 and solves those with the implicit [QR algorithm](/qr-algorithm/).
- **Root finder.** The middle-way scheme of Ren-Cang Li (1993), used in `xLAED4`, needs about two to three iterations per root in practice.
- **Hierarchical matrices.** The product of line L9 is a Cauchy-like matrix, so it can be applied with the fast multipole method or HSS techniques in $O(n^2)$ or less (Gu and Eisenstat 1995; later HSS work).
- **SVD.** The bidiagonal SVD version is LAPACK's `xBDSDC`, used in `xGESDD`; compare the [Golub-Kahan SVD](/golub-kahan-svd-algorithm/).
- **Rank-one updates of a known decomposition.** The merge step alone updates the eigendecomposition of $D + \rho z z^T$, used in updating problems.
- **Alternative for the full spectrum.** [MRRR](/mrrr-algorithm/) gives orthogonal eigenvectors in $O(n^2)$ flops, but it is more delicate.

## When to use it

Use it, as `xSTEDC` or `xSYEVD`, when you need all eigenvalues and eigenvectors of a symmetric tridiagonal or dense symmetric matrix of moderate to large order. It is usually the fastest LAPACK option for that job. For eigenvalues only, use dqds or the QR algorithm without vectors. For a few eigenpairs, use [bisection](/bisection-eigenvalue-algorithm/) with inverse iteration, or MRRR. For a small matrix, the QR algorithm is just as good and simpler.

## Pitfalls

- **Computing eigenvectors from the original $z$.** The formula $(D - \lambda_i I)^{-1} z$ with the computed $\lambda_i$ loses orthogonality when roots are close to poles. Cuppen's original method needed extended precision here, and line L7 fixes this.
- **Computing $d_j - \lambda_i$ by subtraction.** Store each root relative to its nearer pole, as described above, or the differences lose all relative accuracy for roots very close to a pole.
- **Missing the deflation test.** Equal or nearly equal poles make the secular equation degenerate; without deflation the root finder is asked to find a root in an interval of zero width.
- **Sign of $\rho$.** For $\rho < 0$ the roots interlace in the opposite direction; transform to $\rho > 0$.
- **Workspace.** It needs about $n^2$ extra numbers, more than QR or MRRR.

## Implementations

## History

Jan Cuppen introduced the method in 1981, using Golub's 1973 analysis of rank-one modified eigenproblems and the secular equation solver of Bunch, Nielsen and Sorensen (1978). Jack Dongarra and Danny Sorensen showed in 1987 that with deflation it was fast even on serial computers and naturally parallel. Its weakness was the orthogonality of the eigenvectors, which seemed to need extra precision. Ming Gu and Stanley Eisenstat resolved it in 1995 with Loewner's theorem, and the method went into LAPACK as `xSTEDC`.

## References
