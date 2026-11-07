---
tag: 4VFJZ5
kind: algorithm
slug: companion-matrix-method
name: Companion matrix method
aliases:
- eigenvalue method for polynomial roots
- roots via companion matrix
- MATLAB roots method
area: numerical/root-finding
level: advanced
summary: Builds the companion matrix of p, whose characteristic polynomial is p/a0, balances it, and computes all its eigenvalues by the shifted QR algorithm. Backward stable in the matrix, O(n^3) work.
solves: [polynomial-root-finding]
model: real-ram
complexity:
  vars: {n: "the degree of the polynomial", K: "the cap on the QR steps for one eigenvalue"}
  time: {worst: "O(K n^3)", average: "O(n^3)"}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false, bracketing: false, derivative_free: true, simultaneous: true, backward_stable: true}
prereqs: [polynomial-root-finding, qr-algorithm, eigenvalue]
see_also: [jenkins-traub-algorithm, aberth-ehrlich-method, durand-kerner-method, wilkinson-polynomial, root-conditioning, gershgorin-circle-theorem, bernoulli-method, polynomial-deflation]
sources:
  - paper: "Alan Edelman and H. Murakami, Polynomial roots from companion matrix eigenvalues, Mathematics of Computation 64(210), 763-776, 1995"
    locator: the backward error of the computed roots in terms of the coefficients, and the effect of balancing
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Sections 7.4 and 7.5 (Hessenberg form, the shifted QR step, deflation and the practical QR algorithm) and the discussion of balancing
  - paper: "B. N. Parlett and C. Reinsch, Balancing a matrix for calculation of eigenvalues and eigenvectors, Numerische Mathematik 13, 293-304, 1969"
    locator: the balancing algorithm by diagonal similarities with powers of the radix
  - paper: "Kim-Chuan Toh and Lloyd N. Trefethen, Pseudozeros of polynomials and pseudospectra of companion matrices, Numerische Mathematik 68, 403-425, 1994"
    locator: the comparison of pseudozero sets and companion matrix pseudospectra, with and without balancing
  - paper: "Jared L. Aurentz, Thomas Mach, Raf Vandebril and David S. Watkins, Fast and backward stable computation of roots of polynomials, SIAM Journal on Matrix Analysis and Applications 36(3), 942-973, 2015"
    locator: the structured QR algorithm on the companion matrix in O(n^2) time and its backward stability
---

The companion matrix method finds all the roots of a polynomial $p(x) = a_0x^n + a_1x^{n-1} + \cdots + a_n$ at once by turning them into [eigenvalues](/eigenvalue/). The companion matrix
$$C = \begin{pmatrix} -a_1/a_0 & -a_2/a_0 & \cdots & -a_{n-1}/a_0 & -a_n/a_0 \\ 1 & 0 & \cdots & 0 & 0 \\ 0 & 1 & \cdots & 0 & 0 \\ \vdots & & \ddots & & \vdots \\ 0 & 0 & \cdots & 1 & 0 \end{pmatrix}$$
has characteristic polynomial $\det(zI - C) = p(z)/a_0$, so its eigenvalues, with algebraic multiplicities, are the roots of $p$. The method balances $C$ by a diagonal similarity and runs the shifted [QR algorithm](/qr-algorithm/), which is backward stable for the matrix and needs no starting guesses. It costs $O(n^3)$ operations and $O(n^2)$ storage in the plain form. This is what MATLAB's roots and NumPy's numpy.roots do, and it is the default general-purpose polynomial solver.

## In plain words

Every polynomial is the characteristic polynomial of a simple matrix whose first row holds the coefficients and which has ones just below the diagonal. Eigenvalue algorithms are among the most carefully engineered tools in numerical computing, so the easiest robust way to get all the roots is to write down that matrix and hand it to an eigenvalue solver. You pay with $n^2$ storage and $n^3$ work where specialized root finders need less, but you get global convergence in practice and a strong guarantee about the error.

## The problem

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates and $e_k = x_k - x^*$ the error. A method has [order](/order-of-convergence/) $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$, with $0 < C < 1$ when $q = 1$. A root has [multiplicity](/multiplicity-of-roots/) $m$ when $f(x^*) = \cdots = f^{(m-1)}(x^*) = 0 \ne f^{(m)}(x^*)$. The cost is the number of evaluations of $f$ (and of $f'$ where a method uses it). A method of order $q$ that needs $w$ evaluations in each step has efficiency index $q^{1/w}$.

Here $f = p$ with real or complex coefficients and $a_0 \ne 0$; the output is the multiset of all $n$ roots. The method never evaluates $p$, so the cost is counted in QR steps (sweeps) on the active block, each $O(n^2)$ on a Hessenberg matrix, rather than in evaluations. The stopping rule is per eigenvalue: a subdiagonal entry is set to zero when $|h_{l,l-1}| \le u(|h_{l-1,l-1}| + |h_{l,l}|)$ with $u = 2^{-52}$, and the run fails if one eigenvalue takes more than $K$ steps.

## The algorithm

```pseudo id=main
COMPANION-ROOTS(a, K):
L1   strip leading zero coefficients;  remove trailing zero coefficients and record a root 0 for each
L2   C <- the companion matrix of a  (upper Hessenberg)
L3   balance C: repeat D^-1 C D with D diagonal of powers of 2 until row and column norms are close
L4   hi <- n;  while hi >= 1:
L5       lo <- the smallest index such that h_{l,l-1} is negligible for no l in lo+1..hi;  set the negligible entry to 0
L6       if lo = hi then output h_{hi,hi};  hi <- hi - 1;  continue
L7       mu <- the Wilkinson shift from the trailing 2 x 2 block (an exceptional shift every 10 steps)
L8       QR step on the block lo..hi:  H - mu I = Q R by Givens rotations;  H <- R Q + mu I
L9       if this eigenvalue has used K steps then return "failed"
L10  return the outputs, with the recorded zero roots
```

Line L2 needs no work: $C$ is already upper Hessenberg, the form the QR algorithm wants. Line L3 matters: the coefficients of $p$ can differ by many orders of magnitude, and so do the entries of $C$, while the QR algorithm's error is proportional to the norm of the matrix. Balancing with powers of 2 changes no eigenvalue and introduces no rounding error, and it can reduce the norm enormously. Lines L5 and L6 deflate: once a subdiagonal entry is negligible, the matrix splits and the bottom diagonal entry is an eigenvalue. Line L8 is a unitary similarity, so it preserves the eigenvalues, and it keeps the Hessenberg form, so it costs $O(n^2)$. The reference code works in complex arithmetic with single shifts; library codes use Francis's real double-shift step, which keeps real polynomials in real arithmetic.

## Example

For $p(x) = x^3 - 6x^2 + 11x - 6 = (x - 1)(x - 2)(x - 3)$,
$$C = \begin{pmatrix} 6 & -11 & 6 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{pmatrix}, \qquad \det(zI - C) = z^3 - 6z^2 + 11z - 6.$$
The vector $(\lambda^2, \lambda, 1)$ is an eigenvector for each root $\lambda$: for $\lambda = 2$, $C(4, 2, 1)^T = (24 - 22 + 6, 4, 2)^T = 2(4, 2, 1)^T$. The QR iteration with balancing finds the three eigenvalues in 7 sweeps in all, with errors below $10^{-15}$. On $x^4 + 3x^2 + 6x + 10$ it returns $-1 \pm i$ and $1 \pm 2i$ in 12 sweeps, and on $x^{30} - 1$ it returns the 30 roots of unity with errors below $4 \times 10^{-15}$ in 89 sweeps.

Balancing decides the fate of the degree-20 [Wilkinson polynomial](/wilkinson-polynomial/) $\prod_{k=1}^{20}(x - k)$, whose companion matrix has norm about $5 \times 10^{19}$. With balancing the largest root error is $0.058$, and the roots near 20 come out as 19.002 and 20.000. Without balancing the computed eigenvalues are nonsense: the largest is about $45 \pm 8i$, an error of about 30. The roots of this polynomial are so sensitive that rounding the coefficients to double precision already moves some of them by about $10^{-4}$ or more, so no method working from the floating point coefficients can do much better than the balanced result.

## Correctness

The characteristic polynomial of $C$ is exactly $p/a_0$, by expanding $\det(zI - C)$ along its first row, so the eigenvalues with algebraic multiplicities are the roots with multiplicities. Balancing and every QR step are similarities, so they preserve the eigenvalues; deflation replaces a negligible subdiagonal entry by 0, which is a perturbation of relative size at most $u$ of the neighbouring diagonal entries. The loop ends after at most $nK$ QR steps. Global convergence of the shifted QR iteration with these shifts is not proved for general matrices; it is the observed behaviour, and the cap turns any failure into the status "failed". The computed eigenvalues are the exact eigenvalues of $C + E$ with $\|E\| = O(u\|C\|)$ (the backward stability of the QR algorithm), and Edelman and Murakami showed that, with balancing, this usually corresponds to small relative perturbations of the coefficients. The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

Each QR step on the active block of size $m$ costs $O(m^2)$ with Givens rotations on a Hessenberg matrix. On the 500 random test polynomials of degree 2 to 12 the method used on average fewer than 3 steps per root, which gives the usual $O(n^3)$ total, about $10n^3$ flops for the real double-shift code. Storage is $\Theta(n^2)$. Structured QR algorithms that exploit the fact that $C$ is unitary plus rank one, such as that of Aurentz, Mach, Vandebril and Watkins, bring the cost down to $O(n^2)$ time and $O(n)$ storage while staying backward stable.

## Properties

- Finds all roots, real and complex, with multiplicities, without starting guesses.
- Backward stable for the balanced matrix: the computed roots are the exact roots of a polynomial that is the characteristic polynomial of a nearby matrix (proved for the QR algorithm; see the sources).
- Accuracy at a root of multiplicity $m$ behaves like $u^{1/m}$: $6 \times 10^{-9}$, $6 \times 10^{-6}$ and $10^{-4}$ for $m = 2, 3, 4$ in the tests, as for any method working on perturbed coefficients.
- Roots of very different sizes are all found, though small roots of a polynomial with large coefficients may have large relative errors.
- Uses $O(n^2)$ memory, which limits plain implementations to degrees of a few thousand.

## Variants and improvements

- **Real double-shift QR (Francis).** For real coefficients, pairs of complex conjugate shifts keep everything real; this is LAPACK's dhseqr and what MATLAB and NumPy call.
- **Fast structured QR.** Algorithms that exploit the unitary plus rank one structure of $C$ (Aurentz, Mach, Vandebril and Watkins; Bini, Eidelman, Gemignani and Gohberg) run in $O(n^2)$ time.
- **Colleague and comrade matrices.** For polynomials in a Chebyshev or other orthogonal basis, the analogous matrices give roots without converting to the monomial basis, which avoids a very ill-conditioned change of basis.
- **Polishing.** One or two steps of [Newton's method](/newton-raphson-method/) on $p$ from each computed eigenvalue improve the forward error when the roots are well conditioned.
- **Bounds.** [Gershgorin's theorem](/gershgorin-circle-theorem/) applied to the balanced companion matrix gives inclusion discs for the roots.

## When to use it

Use it as the default when you need all the roots of a polynomial of low or moderate degree, say up to a few hundred, and want robustness without tuning. For very high degree or when only a few roots are wanted, prefer [Aberth's method](/aberth-ehrlich-method/) with good starting points, a fast structured QR code, or a local method. For a polynomial that comes from an eigenvalue problem, go back to the matrix: forming the characteristic polynomial and then finding its roots loses accuracy.

## Pitfalls

- L1: dividing by a tiny leading coefficient makes huge entries; strip exact zeros, and treat a nearly zero $a_0$ as a sign of roots near infinity.
- L3: skipping balancing can destroy the result, as the Wilkinson polynomial example shows; on that example the unbalanced error is about 30 and the balanced one $0.058$.
- L5: the deflation test must be relative to nearby entries, not to $\|C\|$ alone, or small roots of a polynomial with large coefficients lose all relative accuracy.
- L7: with plain Rayleigh shifts the iteration can stall on matrices with symmetric spectra such as that of $x^n - 1$; the Wilkinson shift and the occasional exceptional shift avoid this in practice.
- L9: the cap is what makes the loop finite; a "failed" status is rare, but code that ignores it may return too few roots.

## Implementations

## History

The companion matrix goes back to Frobenius's work on normal forms of matrices in the nineteenth century. Turning root finding into an eigenvalue problem became practical with the QR algorithm of Francis and Kublanovskaya (1961), and Cleve Moler made it the method of MATLAB's roots function. Toh and Trefethen (1994) and Edelman and Murakami (1995) analysed its stability and the role of balancing, the latter showing that the method is close to backward stable in the coefficients. Since about 2010, structured QR algorithms have made the approach fast as well as stable.

## References
