---
tag: NJN0YT
kind: concept
slug: wilkinson-shift
name: Wilkinson shift
aliases:
- Wilkinson's shift
area: numerical/eigenproblems
level: advanced
summary: The QR shift equal to the eigenvalue of the trailing 2 by 2 block nearer the last diagonal entry. It never stalls on symmetric tridiagonal matrices and usually converges cubically.
prereqs: [qr-algorithm, tridiagonal-eigenproblem]
see_also: [rayleigh-quotient-iteration, francis-double-shift-qr, symmetric-eigenproblem, deflation, golub-kahan-svd-algorithm, rayleigh-quotient, hessenberg-reduction, inverse-iteration]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.3 (the implicit symmetric tridiagonal QR step with the Wilkinson shift and the symmetric QR algorithm)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 29, QR Algorithm with Shifts (the Rayleigh and Wilkinson shifts, the failure of the Rayleigh shift on a symmetric 2 by 2 matrix)
  - book: isbn:9780898714029
    title: Beresford N. Parlett, The Symmetric Eigenvalue Problem, SIAM Classics in Applied Mathematics 20, 1998
    locator: Chapter 8, The QL and QR Algorithms (shift strategies, Wilkinson's shift and the global convergence theorem)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 5.3.1, Tridiagonal QR Iteration (the Wilkinson shift and its convergence)
  - paper: "J. H. Wilkinson, Global convergence of tridiagonal QR algorithm with origin shifts, Linear Algebra and its Applications 1, 1968"
    title: Global convergence of tridiagonal QR algorithm with origin shifts
    locator: Linear Algebra Appl. 1 (1968), pp. 409 to 420
  - paper: "W. Hoffmann and B. N. Parlett, A new proof of global convergence for the tridiagonal QL algorithm, SIAM Journal on Numerical Analysis 15, 1978"
    title: A new proof of global convergence for the tridiagonal QL algorithm
    locator: SIAM J. Numer. Anal. 15(5) (1978), pp. 929 to 937
---

The Wilkinson shift is the shift $\mu$ used in each step of the [QR algorithm](/qr-algorithm/) that equals the eigenvalue of the trailing $2 \times 2$ block of the current matrix nearer its last diagonal entry. For a symmetric tridiagonal matrix with trailing block $\begin{pmatrix} a_{n-1} & b_{n-1} \\ b_{n-1} & a_n \end{pmatrix}$ it is

$$\mu = a_n - \frac{\operatorname{sign}(\delta) \, b_{n-1}^2}{|\delta| + \sqrt{\delta^2 + b_{n-1}^2}}, \qquad \delta = \frac{a_{n-1} - a_n}{2},$$

with $\operatorname{sign}(0)$ taken as $1$. Compared with the Rayleigh shift $\mu = a_n$, it uses one more row of information, and this removes the symmetric cases where the Rayleigh shift sits exactly between two eigenvalues and the iteration stalls. Wilkinson proved in 1968 that, with this shift, the symmetric tridiagonal QR algorithm converges for every input; in practice the last off-diagonal entry goes to zero cubically, and about two QR steps per eigenvalue suffice.

## In plain words

The QR method improves a table step by step, and each step works best when it is given a good guess of one answer. The simplest guess is the bottom-right number. That guess can fail badly: for some tables it lies exactly halfway between two answers, and then the method does not move at all. Wilkinson's idea is to look at the small two by two corner at the bottom right, solve that tiny problem exactly, and use whichever of its two answers is closer to the bottom-right number. This guess is never stuck halfway, and it gets very good very fast.

## The idea

**Notation.** $T$ is real symmetric tridiagonal with diagonal $a_1, \dots, a_n$ and off-diagonal $b_1, \dots, b_{n-1}$, unreduced. A QR step with shift $\mu$ maps $T$ to $T' = R Q + \mu I$, where $T - \mu I = Q R$; $T'$ is again symmetric tridiagonal, and it is orthogonally similar to $T$. Convergence means $b'_{n-1} \to 0$, after which $a_n$ is an eigenvalue and the problem deflates to order $n - 1$.

**Why shifts matter.** The last column of $Q$ is the result of one step of [inverse iteration](/inverse-iteration/) on $T$ with shift $\mu$ from $e_n$, so the step is fast when $\mu$ is close to an eigenvalue. With $\mu = a_n = \rho(e_n)$, the [Rayleigh quotient](/rayleigh-quotient/) of $e_n$, the step is one step of [Rayleigh quotient iteration](/rayleigh-quotient-iteration/), which converges cubically near an eigenvector but can fail to converge from a symmetric start.

**The failure of the Rayleigh shift.** For $T = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$, $\mu = a_2 = 0$, and $T - 0 I$ is orthogonal, so $Q = T$, $R = I$ and $T' = T$: the step changes nothing. The two eigenvalues $\pm 1$ are at equal distance from $0$, and inverse iteration from $e_2$ cannot prefer one. The same happens for every $\begin{pmatrix} a & b \\ b & a \end{pmatrix}$.

**The fix.** The Wilkinson shift is an eigenvalue of the trailing block, and here it is $\pm 1$, an exact eigenvalue of $T$; then $T - \mu I$ is singular, its QR factorization has $r_{22} = 0$, and the step deflates at once. In general the shift is never equidistant in the way that defeats the Rayleigh shift, because it is chosen as the nearer of two candidates.

**The formula.** The eigenvalues of the block are $(a_{n-1} + a_n)/2 \pm \sqrt{\delta^2 + b_{n-1}^2}$. Choosing the one nearer $a_n$ and rewriting the difference $a_n - \mu$ by rationalizing gives the expression above, which has no cancellation; codes use a scaled square root such as `hypot` to avoid overflow in $\delta^2 + b^2$.

**Convergence results.**

- *Global convergence (proved).* For every unreduced symmetric tridiagonal $T$, the QR algorithm with the Wilkinson shift drives $b_{n-1}$ to zero (Wilkinson 1968; a shorter proof is in Hoffmann and Parlett 1978, and the result is in Parlett Chapter 8). No such theorem holds for the Rayleigh shift.
- *Local rate (proved for the generic case, observed in general).* Once $b_{n-1}$ is small and $a_n$ is near a simple eigenvalue, the Wilkinson shift and the Rayleigh shift differ by $O(b_{n-1}^2)$, and both give $|b'_{n-1}| = O(|b_{n-1}|^3)$, the cubic rate of Rayleigh quotient iteration for symmetric matrices (TB Lecture 29; Parlett Chapter 8). The worst-case rate guaranteed by the global theorem is slower; cubic convergence is what is seen almost always.
- *Step count (observed).* About 2 steps per eigenvalue or fewer, which is the basis of the $O(n^2)$ flop count for all eigenvalues and of the $6n^3$ count with eigenvectors; no theorem bounds the total.

**Nonsymmetric matrices.** For an upper Hessenberg $H$, the same rule picks the eigenvalue of the trailing $2 \times 2$ block nearer $h_{nn}$; for real $H$ it may be complex, so real codes use both eigenvalues of the block at once in the [Francis double-shift QR](/francis-double-shift-qr/) step. No global theorem exists: for the cyclic permutation matrix the trailing block has both eigenvalues $0$, the shift is $0$, and the step is the identity, so practical codes add exceptional shifts.

## Examples

**The $2 \times 2$ case.** For $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$, $\delta = 0$ and $\mu = 0 - 1 \cdot 1 / (0 + 1) = -1$. One step deflates exactly. The implementation on the [QR algorithm](/qr-algorithm/) page takes 1 step with the Wilkinson shift; with the Rayleigh shift it stalls until its exceptional shift after 10 steps, and needs 13 steps in all.

**Cubic decrease.** For $T = \begin{pmatrix} 2 & 1 & 0 \\ 1 & 3 & 1 \\ 0 & 1 & 4 \end{pmatrix}$, with eigenvalues $3 - \sqrt 3$, $3$, $3 + \sqrt 3$, $\delta = -0.5$ and the first Wilkinson shift is $\mu = 4 + 1/(0.5 + \sqrt{1.25}) = 4.618034$. The values of $|b_2|$ after successive steps are $9.45 \times 10^{-2}$, $1.21 \times 10^{-5}$ and $8.3 \times 10^{-18}$. The ratios $|b'_2| / |b_2|^3$ are $0.014$ and $0.0047$, so the decrease is cubic, and the whole matrix is diagonal after 4 steps. With the Rayleigh shift the same matrix takes 7 steps, with $|b_2| = 0.745, 0.272, 7.2 \times 10^{-3}, 1.2 \times 10^{-7}, 6.3 \times 10^{-22}$.

**A symmetric stall.** For the second difference matrix of order 5 ($a_k = 2$, $b_k = -1$), the first Rayleigh shift $\mu = 2$ happens to be an eigenvalue, so the first step deflates exactly, but on the remaining block of order 4 the value $|b_3|$ stays between $1.0$ and $1.1$ for nine steps until the exceptional shift breaks the symmetry; the Rayleigh run takes 21 steps. The Wilkinson shift of the trailing block $\begin{pmatrix} 2 & -1 \\ -1 & 2 \end{pmatrix}$ is $1$ or $3$, both exact eigenvalues ($2 - 2\cos(k\pi/6)$ for $k = 2, 4$), and the run takes 8 steps, deflating twice exactly in the first two.

## Where it is used

- **Symmetric tridiagonal QR and QL.** LAPACK `xSTEQR` and `xSTERF` use the Wilkinson shift with the implicit QL or QR step, choosing the direction by the grading of the matrix ([symmetric eigenproblem](/symmetric-eigenproblem/)).
- **The SVD.** The [Golub-Kahan SVD algorithm](/golub-kahan-svd-algorithm/) takes the Wilkinson shift of the trailing $2 \times 2$ block of $B^T B$, computed from the entries of the bidiagonal $B$ without forming the product.
- **Nonsymmetric QR.** The complex single-shift QR algorithm uses it directly; the Francis double shift uses the two eigenvalues of the same block, which for real input is the real-arithmetic form of the same idea.
- **Deflation strategies.** Shifts taken from larger trailing blocks, as in multishift QR and aggressive early [deflation](/deflation/), extend the idea from a $2 \times 2$ block to blocks of order tens or hundreds.

## References
