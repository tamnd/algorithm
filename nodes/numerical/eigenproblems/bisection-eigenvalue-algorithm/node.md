---
tag: SXNY4P
kind: algorithm
slug: bisection-eigenvalue-algorithm
name: Bisection for tridiagonal eigenvalues
aliases:
- bisection eigenvalue method
- Sturm sequence bisection
- Givens bisection method
area: numerical/eigenproblems
level: core
summary: Find any chosen eigenvalue of a symmetric tridiagonal matrix by halving an interval, using the count of negative pivots of T − xI, which equals the number of eigenvalues below x.
solves: [tridiagonal-eigenproblem]
model: floating-point-model
complexity:
  vars: {n: "the order of T", k: "the number of wanted eigenvalues", s: "the number of bisection steps per eigenvalue, about 53 for full precision"}
  time: {worst: Θ(k n s)}
  space: {extra: O(1)}
  flops: {worst: "4k n s"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: true}
history:
  year: 1954
  people: [Wallace Givens, William Kahan, J. H. Wilkinson]
  note: Givens used Sturm sequences of a tridiagonal matrix in 1954; Kahan's 1966 analysis showed that the counts are exact for a nearby matrix.
prereqs: [sturm-sequence-eigenvalue-count, tridiagonal-eigenproblem, gershgorin-circle-theorem]
see_also: [inverse-iteration, tridiagonalization, mrrr-algorithm, divide-and-conquer-eigensolver, qr-algorithm, weyls-inequality, cauchy-interlacing-theorem, dqds-algorithm]
sources:
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 5.3.4, Bisection and Inverse Iteration (Kahan's count, its error analysis and the cost)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.4.1 and 8.4.2, Eigenvalues by Bisection and the Sturm sequence property
  - book: isbn:9780898714029
    title: Beresford N. Parlett, The Symmetric Eigenvalue Problem, SIAM Classics in Applied Mathematics 20, 1998
    locator: Chapter 3, Counting Eigenvalues (Sylvester's inertia theorem and the triangular factorization count)
  - book: "J. H. Wilkinson, The Algebraic Eigenvalue Problem, Oxford University Press, 1965"
    title: J. H. Wilkinson, The Algebraic Eigenvalue Problem
    locator: Chapter 5, Sections 37 to 47 (Sturm sequences and the error analysis of bisection)
  - paper: "W. Kahan, Accurate eigenvalues of a symmetric tri-diagonal matrix, Technical Report CS41, Computer Science Department, Stanford University, 1966"
    title: W. Kahan, Accurate eigenvalues of a symmetric tri-diagonal matrix
    locator: the backward error of the computed count
  - paper: "W. Barth, R. S. Martin and J. H. Wilkinson, Calculation of the eigenvalues of a symmetric tridiagonal matrix by the method of bisection, Numerische Mathematik 9, 1967, pp. 386 to 393"
    title: W. Barth, R. S. Martin and J. H. Wilkinson, Calculation of the eigenvalues of a symmetric tridiagonal matrix by the method of bisection
    locator: the Handbook procedure bisect
---

Bisection computes selected eigenvalues of a real symmetric tridiagonal matrix $T$ by shrinking an interval around each one. The tool is the count $c(x)$, the number of eigenvalues of $T$ below $x$. It equals the number of negative pivots in the factorization $T - xI = L D L^T$ and costs $O(n)$ flops. A count at the midpoint tells which half holds the $k$-th eigenvalue. Each step gains one binary digit, so about 53 steps give full double precision. Any eigenvalue, or all eigenvalues in an interval, can be found independently and in parallel, and the computed count is exactly right for a matrix within a few units of roundoff of $T$.

## In plain words

To find an eigenvalue, you only need a way to ask: how many eigenvalues are smaller than this number? For a tridiagonal symmetric matrix, a short pass over the matrix answers this question. The answer is the number of negative values in a simple running sequence.

Start with an interval that holds all eigenvalues. Ask the question at the middle of the interval. If enough eigenvalues are below the middle, the one you want is in the lower half; else it is in the upper half. Repeat. Each question cuts the interval in half, so a fixed number of questions gives the eigenvalue to full precision. The method is slow compared with other methods when you want all eigenvalues, but it is very reliable, and it can find just the ones you want.

## The problem

**Notation.** $T$ is real symmetric tridiagonal of order $n$ with diagonal $a_1, \dots, a_n$ and off-diagonal $b_1, \dots, b_{n-1}$. Its eigenvalues in increasing order are $\mu_1 \le \dots \le \mu_n$, so that $\mu_k$ is the $k$-th smallest. In the decreasing order $\lambda_1 \ge \dots \ge \lambda_n$ of this area, $\mu_k = \lambda_{n+1-k}$. The count is $c(x) = \#\{i : \mu_i < x\}$, and $u$ is the unit roundoff.

Given $T$ and an index $k$ (or an interval), compute $\mu_k$ (or all eigenvalues in the interval) to a given tolerance. A dense symmetric matrix is first reduced to this form by [tridiagonalization](/tridiagonalization/).

## The algorithm

```pseudo id=main
BISECT(T, k, τ)                               ▷ returns μ_k, the k-th smallest eigenvalue
L1  [ℓ, h] ← Gershgorin interval of T, widened slightly
L2  while h − ℓ > max(τ, 2u · max(|ℓ|, |h|)) do
L3      x ← (ℓ + h) / 2;  if x = ℓ or x = h then exit the loop
L4      if NEGCOUNT(T, x) ≥ k
L5          then h ← x  else ℓ ← x                 ▷ invariant: c(ℓ) < k ≤ c(h)
L6  return (ℓ + h) / 2

NEGCOUNT(T, x)                                ▷ number of eigenvalues of T below x
L7  c ← 0;  d ← 1
L8  for i ← 1 to n do d ← (aᵢ − x) − b²ᵢ₋₁ / d  (with b₀ = 0);  if |d| < π_min then d ← −π_min
L9      if d < 0 then c ← c + 1
L10 return c
```

The pivots $d_i$ of line L8 are those of Gaussian elimination on $T - xI$ without pivoting. By Sylvester's law of inertia, the number of negative pivots equals the number of negative eigenvalues of $T - xI$, that is $c(x)$. The safeguard with $\pi_{\min} = \text{SAFMIN} \cdot \max(1, \max_i b_i^2)$ avoids division by zero and overflow, as in LAPACK. Lines L1 to L6 find one eigenvalue; to find all of them, call BISECT for $k = 1, \dots, n$, or split intervals so that the counts computed for one eigenvalue also narrow the others.

## Example

Take the Toeplitz matrix $T = \operatorname{tridiag}(-1, 2, -1)$ of order 4, with eigenvalues $2 - 2\cos(j\pi/5)$: 0.381966, 1.381966, 2.618034, 3.618034. The Gershgorin interval is $[0, 4]$. At $x = 1.5$ the pivots are $d_1 = 0.5$, $d_2 = 0.5 - 1/0.5 = -1.5$, $d_3 = 0.5 + 1/1.5 = 1.166667$ and $d_4 = 0.5 - 1/1.166667 = -0.357143$. Two are negative, so $c(1.5) = 2$. To find $\mu_2$:

| step | $x$ | $c(x)$ | new interval |
|---|---|---|---|
| 1 | 2 | 2 | $[0, 2]$ |
| 2 | 1 | 1 | $[1, 2]$ |
| 3 | 1.5 | 2 | $[1, 1.5]$ |
| 4 | 1.25 | 1 | $[1.25, 1.5]$ |
| 5 | 1.375 | 1 | $[1.375, 1.5]$ |
| 6 | 1.4375 | 2 | $[1.375, 1.4375]$ |
| 7 | 1.40625 | 2 | $[1.375, 1.40625]$ |
| 8 | 1.390625 | 2 | $[1.375, 1.390625]$ |

The widening of line L1 changes these numbers only in the fifteenth digit. After 54 steps the interval has relative width $2u$, and the result is $1.381966011250105$, which equals $2 - 2\cos(2\pi/5)$ to all digits shown.

A harder case is Wilkinson's matrix $W_{21}^+$ with $a_i = |11 - i|$ and $b_i = 1$. Its two largest eigenvalues, about 10.746194182903, differ by only $7.5 \times 10^{-14}$. Bisection separates them: the exact count at the midpoint of the two computed values is 20.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md).

1. **The count.** If all pivots are nonzero, $T - xI = L D L^T$ with $D = \operatorname{diag}(d_i)$. By Sylvester's law of inertia ([Sturm count](/sturm-sequence-eigenvalue-count/)), $c(x)$ is the number of negative $d_i$. The pivots are ratios of consecutive leading principal minors, the classical Sturm sequence.
2. **Invariant.** The start satisfies $c(\ell) = 0 < k \le n = c(h)$ because of the [Gershgorin theorem](/gershgorin-circle-theorem/). The update of line L5 keeps $c(\ell) < k \le c(h)$, so $\mu_k \in [\ell, h)$ throughout.
3. **Termination.** Each step halves the interval, so with an absolute tolerance $\tau$ the loop ends after $\lceil \log_2((h_0 - \ell_0)/\tau) \rceil$ steps. With $\tau = 0$ it ends when no floating-point number lies strictly between $\ell$ and $h$, at the latest.
4. **Floating point (Kahan).** In IEEE arithmetic the computed count at $x$ is the exact count of a matrix $\tilde T$ with the same diagonal and $\tilde b_i = b_i(1 + \eta_i)$, $|\eta_i| \le 2.5u + O(u^2)$. So the result is an eigenvalue of $\tilde T$ to within the final interval width. By [Weyl's inequality](/weyls-inequality/), it has an absolute error of order $u \|T\|_2$. The computed count is also monotone in $x$ (Demmel, Dhillon and Ren 1995), so the bracketing argument holds in floating point.

## Complexity

- **One count.** About $4n$ flops: one subtraction, one division, one more subtraction and a comparison per entry; $3n$ if the $b_i^2$ are stored.
- **One eigenvalue.** $s$ counts, where $s = \lceil \log_2(\text{width}/\tau) \rceil$ is proved. Full double precision needs about 53 steps when the eigenvalue is not tiny compared with the interval, and more for tiny eigenvalues computed to relative accuracy.
- **All eigenvalues.** $\Theta(n^2 s)$ flops, about $200n^2$ for full precision. The tridiagonal QR algorithm and dqds also need $O(n^2)$ flops but with a much smaller constant; for them the count rests on about two iterations per eigenvalue, which is observed, not proved. So bisection is slower when all eigenvalues are wanted, but much faster when only a few are wanted.
- **Space.** $O(1)$ beyond $T$. Each eigenvalue is computed independently, so the method parallelizes trivially.

## Properties

- **Selective.** It computes the $k$-th eigenvalue, or all eigenvalues in $[\alpha, \beta)$ (their number is $c(\beta) - c(\alpha)$), without computing the others.
- **Guaranteed and predictable.** The number of steps does not depend on the spectrum, unlike shifted QR, and the error bound holds for each eigenvalue.
- **Backward stable,** with an absolute error of order $u\|T\|$. For matrices whose small eigenvalues are determined to high relative accuracy by the off-diagonal entries, for example $T$ with zero diagonal, which arises from the SVD of a bidiagonal matrix, it gives high relative accuracy (Demmel and Kahan 1990).
- **Linear convergence** with the ratio $1/2$, slow compared with the quadratic or cubic rate of Newton and QR methods.

## Variants and improvements

- **Interval splitting.** Keep a list of intervals with their counts, and split until each holds one eigenvalue; counts computed for one eigenvalue are reused for its neighbours (Barth, Martin and Wilkinson 1967; LAPACK `xSTEBZ`).
- **Faster local convergence.** Once an interval holds one eigenvalue, switch to a superlinear method on the characteristic polynomial, such as the secant or Laguerre iteration, or to the [Rayleigh quotient iteration](/rayleigh-quotient-iteration/), keeping the count as a safeguard.
- **Multisection.** Evaluate counts at several points at once on vector or parallel hardware.
- **Eigenvectors.** Follow bisection with [inverse iteration](/inverse-iteration/) (LAPACK `xSTEIN`). Clusters then need reorthogonalization, which the [MRRR algorithm](/mrrr-algorithm/) avoids by using relatively robust representations and the same counting idea on $L D L^T$.
- **Banded and dense matrices.** The inertia of $A - xI$ by a symmetric indefinite factorization gives a count for any symmetric matrix, at a cost of $O(n^3)$ per count for dense $A$; this is used for large sparse problems with sparse factorizations ("spectrum slicing").

## When to use it

Use bisection when you need a few eigenvalues of a symmetric tridiagonal matrix, eigenvalues in a given interval, eigenvalues by index (for example the median), or guaranteed error bounds. It also suits parallel machines. It is part of the LAPACK path for selected eigenpairs (`xSTEBZ` with `xSTEIN`, and inside `xSTEMR`). For all eigenvalues of a dense matrix, the QR algorithm, [divide and conquer](/divide-and-conquer-eigensolver/) or [dqds](/dqds-algorithm/) are faster.

## Pitfalls

- **Using the minors $p_i(x)$ directly.** The minors overflow or underflow for moderate $n$; use the ratios $d_i$ of line L8.
- **Division by zero.** A pivot can be exactly zero; replace it by $-\pi_{\min}$ as in line L8, and choose $\pi_{\min}$ so that $b_i^2 / \pi_{\min}$ cannot overflow.
- **An interval that is too tight.** If the start interval is the exact Gershgorin interval, rounding can make $c(h) < n$; widen it as in line L1.
- **Expecting relative accuracy in general.** For $T = \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$ the eigenvalue 0 is computed as about $-1.1 \times 10^{-16}$. The count is exact only for a nearby matrix, and no method can do better from the stored entries.
- **Applying it to a nonsymmetric tridiagonal matrix.** The inertia argument needs symmetry. A real nonsymmetric tridiagonal matrix with $b_i c_i > 0$ can first be symmetrized by a diagonal similarity.

## Implementations

## History

Givens (1954) reduced a symmetric matrix to tridiagonal form by rotations and found its eigenvalues by bisection on the Sturm sequence of the leading principal minors. Wilkinson analysed the method in the early 1960s and in his 1965 book. The Handbook procedure `bisect` of Barth, Martin and Wilkinson (1967) became the standard code. Kahan's 1966 report used the ratio form of the recurrence and proved that the computed count is exact for a matrix with tiny relative changes in the off-diagonal entries. Demmel and Kahan (1990) used it for high relative accuracy of bidiagonal singular values, and Demmel, Dhillon and Ren (1995) proved its monotonicity in IEEE arithmetic, as needed for parallel codes.

## References
