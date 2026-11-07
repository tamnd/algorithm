---
tag: DE4SM2
kind: concept
slug: sturm-sequence-eigenvalue-count
name: Sturm sequence
aliases:
- Sturm's theorem for matrices
- Sturm count
- eigenvalue count by inertia
- Sturm sequence eigenvalue count
area: numerical/eigenproblems
level: advanced
summary: For a symmetric tridiagonal T and a number x, the signs of the leading minors of T - x I, or of the pivots of its LDL^T factorization, count the eigenvalues below x in O(n) flops.
prereqs: [tridiagonal-eigenproblem]
see_also: [bisection-eigenvalue-algorithm, mrrr-algorithm, cauchy-interlacing-theorem, polynomial-root-finding, symmetric-eigenproblem, characteristic-polynomial, positive-definite-matrix, inverse-iteration]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.4.1 (Sturm sequence methods, the count of eigenvalues below a value and bisection)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 5.3.4 (bisection and inverse iteration, the inertia count and its backward stability), Section 5.2 (Sylvester's law of inertia)
  - book: isbn:9780898714029
    title: Beresford N. Parlett, The Symmetric Eigenvalue Problem, SIAM Classics in Applied Mathematics 20, 1998
    locator: Chapter 3 (counting eigenvalues, Sylvester's inertia theorem) and Chapter 7 (tridiagonal form and Sturm sequences)
  - book: "J. H. Wilkinson, The Algebraic Eigenvalue Problem, Oxford University Press, 1965"
    title: J. H. Wilkinson, The Algebraic Eigenvalue Problem
    locator: Chapter 5 (the Sturm sequence property of the leading principal minors and its error analysis)
  - paper: "James W. Demmel, Inderjit Dhillon and Huan Ren, On the correctness of some bisection-like parallel eigenvalue algorithms in floating point arithmetic, Electronic Transactions on Numerical Analysis 3, 1995"
    title: On the correctness of some bisection-like parallel eigenvalue algorithms in floating point arithmetic
    locator: Electron. Trans. Numer. Anal. 3 (1995), pp. 116 to 149
---

A Sturm sequence count tells how many eigenvalues of a real symmetric tridiagonal matrix $T$ lie below a given number $x$, without computing any of them. With $a_1, \dots, a_n$ on the diagonal and $b_1, \dots, b_{n-1}$ next to it, the recurrence $q_1 = a_1 - x$, $q_k = a_k - x - b_{k-1}^2 / q_{k-1}$ produces the pivots of the factorization $T - x I = L D L^T$, and the number of negative $q_k$ equals the number of eigenvalues of $T$ that are less than $x$. Each count costs about $4n$ flops, and two counts give the number of eigenvalues in an interval. This is the engine of the [bisection eigenvalue algorithm](/bisection-eigenvalue-algorithm/) and of [MRRR](/mrrr-algorithm/), and the computed count is backward stable: it is the exact count for a nearby tridiagonal matrix.

## In plain words

Given a symmetric table with numbers only on the diagonal and next to it, and a test value, we want to know how many of the table's special values are smaller than the test value. We subtract the test value from the diagonal and run down the table once, computing one number per row from the previous one. Each of these numbers is either positive or negative. The count of negative ones is the answer. Doing this for two test values tells how many special values lie between them, which lets a program close in on any one of them by halving the interval.

## The idea

**Notation.** $T$ is real symmetric tridiagonal of order $n$, $T_k$ its leading $k \times k$ principal submatrix, $\lambda_1 \ge \dots \ge \lambda_n$ its eigenvalues, and $p_k(x) = \det(T_k - x I)$ with $p_0 = 1$. $u$ is the unit roundoff. $\nu(x)$ is the number of eigenvalues of $T$ less than $x$.

**The inertia form.** If no pivot vanishes, Gaussian elimination without pivoting gives $T - x I = L D L^T$ with $L$ unit lower bidiagonal and $D = \operatorname{diag}(q_1, \dots, q_n)$, where

$$q_1 = a_1 - x, \qquad q_k = a_k - x - \frac{b_{k-1}^2}{q_{k-1}} \quad (k = 2, \dots, n).$$

By Sylvester's law of inertia, $T - x I$ and $D$ have the same numbers of negative, zero and positive eigenvalues, because they are congruent. The eigenvalues of $T - x I$ are $\lambda_i - x$. So $\nu(x)$ is the number of negative $q_k$, and the number of zero $q_k$ is the multiplicity of $x$ as an eigenvalue when the factorization exists.

**The determinant form.** Since $q_k = p_k(x) / p_{k-1}(x)$, the same count is the number of sign changes in the sequence $p_0(x), p_1(x), \dots, p_n(x)$, which satisfies the three-term recurrence $p_k(x) = (a_k - x) p_{k-1}(x) - b_{k-1}^2 p_{k-2}(x)$. For unreduced $T$ the zeros of $p_{k-1}$ strictly interlace those of $p_k$ ([Cauchy interlacing](/cauchy-interlacing-theorem/)), which makes $(p_n, p_{n-1}, \dots, p_0)$ a Sturm sequence in the classical sense of Sturm's 1829 theorem on real roots of polynomials. The pivot form is preferred in practice: the $p_k$ overflow or underflow for large $n$, while the $q_k$ stay of the size of the entries.

**Intervals and bisection.** The number of eigenvalues in $[\alpha, \beta)$ is $\nu(\beta) - \nu(\alpha)$. To find $\lambda_{n-k+1}$, the $k$-th smallest, start from an interval that contains the whole spectrum (for example from the [Gershgorin discs](/gershgorin-circle-theorem/)) and halve it, keeping the half where $\nu$ passes $k$. Each step costs one count, $O(n)$ flops, and halves the width.

**Zero pivots.** If some $q_{k-1} = 0$, the next division is undefined. Codes either replace $q_{k-1}$ by a tiny number such as $-u \, |b_{k-1}|$, or rely on IEEE arithmetic, where $b^2 / 0 = \infty$ and $q_k = -\infty$, which counts correctly (Demmel, Dhillon and Ren 1995). The choice affects only whether $x$ itself is counted as below or above an eigenvalue equal to it.

**Backward stability.** Kahan's analysis (1966) shows that, without overflow, the computed pivots $\hat q_k$ are the exact pivots for $T' - x I$, where $T'$ has the same diagonal and off-diagonal entries $b'_k$ with $|b'_k - b_k| \le c \, u \, |b_k|$ for a small constant $c$. So the computed count is the exact count $\nu'(x)$ for a matrix $T'$ whose eigenvalues differ from those of $T$ by $O(u)\|T\|_2$, by [Weyl's inequality](/weyls-inequality/). The computed count need not be monotone in $x$ for every implementation and machine; Demmel, Dhillon and Ren (1995) give the conditions under which it is, which bisection needs for its correctness proof.

**Dense and banded matrices.** For a full symmetric $A$, $\nu(x)$ is the number of negative eigenvalues of $D$ in a symmetric indefinite factorization $A - x I = L D L^T$ with Bunch-Kaufman pivoting, at $n^3/3$ flops per count. Sparse codes use this for spectrum slicing: the inertia of a sparse factorization checks that a shift-invert Lanczos run found every eigenvalue in an interval.

## Examples

**The second difference matrix, $n = 4$.** $T$ with $a_k = 2$ and $b_k = -1$ has the eigenvalues $0.38197$, $1.38197$, $2.61803$, $3.61803$. At $x = 1.5$ the pivots are $q_1 = 0.5$, $q_2 = 0.5 - 1/0.5 = -1.5$, $q_3 = 0.5 - 1/(-1.5) = 1.16667$ and $q_4 = 0.5 - 1/1.16667 = -0.35714$. Two are negative, so $\nu(1.5) = 2$, and indeed two eigenvalues are below $1.5$. The determinants are $p_0, \dots, p_4 = 1, 0.5, -0.75, -0.875, 0.3125$, with sign pattern $+, +, -, -, +$ and two sign changes. As a check, $p_4(1.5) = \prod_i (\lambda_i - 1.5) = 0.3125$.

**A close pair.** For Wilkinson's $W_{21}^+$ ($a_k = |11 - k|$, $b_k = 1$, $n = 21$), the count at $x = 10.74619418290336$, between the two largest eigenvalues $10.746194182903322$ and $10.746194182903393$, is $\nu(x) = 20$ in exact rational arithmetic. Seventy bisection steps on the exact count separate the two eigenvalues, which differ by only $7.16 \times 10^{-14}$; in floating point, bisection pins down each to within a few units of $u \|T\|_2$, but cannot always say which count belongs to which eigenvalue of the pair.

**A zero pivot.** For $T = \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$ (eigenvalues $0$ and $2$) and $x = 1$, $q_1 = 0$. Replacing it by $-\epsilon$ gives $q_2 = 0 + 1/\epsilon > 0$, so the count is 1, which is right: exactly one eigenvalue lies below $1$.

## Where it is used

- **Bisection.** LAPACK `xSTEBZ` finds selected eigenvalues of a tridiagonal matrix, or all eigenvalues in an interval, by bisection on the count; it parallelizes over intervals with no communication ([bisection eigenvalue algorithm](/bisection-eigenvalue-algorithm/)).
- **MRRR.** [MRRR](/mrrr-algorithm/) applies the count to a factored representation $L D L^T$ of a shifted $T$ (the stationary qd transform), which gives eigenvalues to high relative accuracy before the eigenvectors are computed.
- **Inverse iteration.** The count certifies how many eigenvalues an [inverse iteration](/inverse-iteration/) shift is near, and the twisted factorizations of MRRR are built from the same pivots run forwards and backwards.
- **Spectrum slicing.** Sparse eigensolvers count eigenvalues in $[\alpha, \beta)$ by the inertia of two sparse factorizations, to check completeness.
- **Positive definiteness.** $\nu(0) = 0$ and no zero pivot means $T$ is [positive definite](/positive-definite-matrix/); the count at $0$ is a cheap test.
- **History.** Sturm (1829) counted real roots of a polynomial by sign changes in the Euclidean remainder sequence of $p$ and $p'$. Givens (1954) applied the leading-minor sequence to tridiagonal matrices after his reduction by rotations, and Wilkinson's 1965 book and Kahan's 1966 report gave the error analysis that made the method reliable.

## References
