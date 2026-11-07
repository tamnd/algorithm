---
tag: BE4Y2X
kind: algorithm
slug: dqds-algorithm
name: dqds algorithm
aliases:
- differential quotient-difference with shifts
- dqds
- differential qd algorithm with shifts
area: numerical/eigenproblems
level: research
summary: Computes all singular values of a bidiagonal matrix to high relative accuracy by shifted Cholesky LR steps on the squared entries, with no subtraction of large terms.
solves: [singular-value-decomposition]
model: floating-point-model
complexity:
  vars: {n: "the order of the bidiagonal matrix B"}
  time: {per_step: O(n), typical: O(n^2)}
  space: {worst: Θ(n)}
  flops: {per_transform: "5n", newton_shift: "4n", typical_total: "40n^2"}
properties: {deterministic: true, in_place: true, recursive: false, iterative: true}
history:
  year: 1994
  people: [K. Vince Fernando, Beresford N. Parlett, Heinz Rutishauser, Osni A. Marques]
  note: Rutishauser invented the quotient-difference algorithm in 1954; Fernando and Parlett gave its differential form with shifts and proved its high relative accuracy in 1994; Parlett and Marques wrote the LAPACK implementation.
prereqs: [singular-value-decomposition, cholesky-decomposition]
see_also: [golub-kahan-svd-algorithm, mrrr-algorithm, tridiagonal-eigenproblem, qr-algorithm, bisection-eigenvalue-algorithm, divide-and-conquer-eigensolver, weyls-inequality, deflation]
sources:
  - paper: doi:10.1007/s002110050024
    title: K. V. Fernando and B. N. Parlett, Accurate singular values and differential qd algorithms, Numerische Mathematik 67, 1994
    locator: pp. 191 to 229 (the dqd and dqds transforms, the link to Cholesky LR, positivity, the mixed relative error analysis)
  - paper: doi:10.1016/S0024-3795(00)00010-0
    title: B. N. Parlett and O. A. Marques, An implementation of the dqds algorithm (positive case), Linear Algebra and its Applications 309, 2000
    locator: pp. 217 to 259 (shift strategy, flipping, deflation tests, the LAPACK xLASQ routines)
  - paper: doi:10.1007/BF01600331
    title: H. Rutishauser, Der Quotienten-Differenzen-Algorithmus, Zeitschrift für angewandte Mathematik und Physik 5, 1954
    locator: pp. 233 to 251 (the original qd scheme)
  - paper: doi:10.1137/0911052
    title: J. Demmel and W. Kahan, Accurate singular values of bidiagonal matrices, SIAM Journal on Scientific and Statistical Computing 11, 1990
    locator: pp. 873 to 912 (relative perturbation theory for bidiagonal matrices, zero-shift QR)
  - paper: doi:10.1137/060678762
    title: K. Aishima, T. Matsuo, K. Murota and M. Sugihara, On convergence of the dqds algorithm for singular value computation, SIAM Journal on Matrix Analysis and Applications 30, 2008
    locator: pp. 522 to 537 (global convergence and the asymptotic rate under a class of shift strategies)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 5.4, Algorithms for the Singular Value Decomposition (high relative accuracy for bidiagonal matrices, dqds)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.6, Computing the SVD (the bidiagonal phase and its alternatives)
  - book: "J. H. Wilkinson, The Algebraic Eigenvalue Problem, Oxford University Press, 1965"
    title: J. H. Wilkinson, The Algebraic Eigenvalue Problem
    locator: Chapter 8, The LR and QR algorithms (Cholesky LR and its relation to QR on positive definite matrices)
---

The dqds algorithm computes all singular values of an $n \times n$ upper bidiagonal matrix $B$, each to high relative accuracy, in $O(n^2)$ flops in practice. It works on the squares $q_k = a_k^2$ and $e_k = b_k^2$ of the entries. One transform with shift $\tau$ maps $(q, e)$ to $(\hat q, \hat e)$ with $\hat B^T \hat B = B B^T - \tau I$. This is one Cholesky LR step, written so that it never subtracts large numbers. When $\tau$ is below $\sigma_n^2$ every quantity stays positive. Fernando and Parlett proved that this makes every singular value, the tiny ones too, as accurate as the data allows. The shifts add up to $\sigma_n^2$, the last $e$ goes to zero, and the problem deflates. LAPACK uses dqds (`xLASQ1`) whenever only singular values of a bidiagonal matrix are wanted. That covers `xBDSQR` without vectors, so dense SVDs without vectors go through it too.

## In plain words

After a matrix has been squeezed down to a thin band of two diagonals, its singular values still have to be found. Some of them may be tiny, many orders of magnitude below the largest. A method that rounds every result relative to the largest one gives tiny values with no correct digits.

This method squares the band entries and repeatedly rewrites them into a new set with the same answers. All the answers are lowered by a known amount, and that amount is added to a running total. Every number it computes is positive and is formed from products, quotients and sums of positive numbers. Nothing cancels, so every result keeps nearly full precision. The last entry of the upper diagonal shrinks quickly. When it is negligible, the running total plus the last diagonal entry is one answer, and the band gets one row shorter.

## The problem

**Notation.** $B$ is real upper bidiagonal with diagonal $a_1, \dots, a_n$ and superdiagonal $b_1, \dots, b_{n-1}$. Its singular values are $\sigma_1 \ge \dots \ge \sigma_n \ge 0$, the square roots of the eigenvalues of $B^T B$ and of $B B^T$. The qd variables are $q_k = a_k^2$ and $e_k = b_k^2$. They define the bidiagonal with diagonal $\sqrt{q_k}$ and superdiagonal $\sqrt{e_k}$, which has the same singular values as $B$, because signs can be moved out by diagonal $\pm 1$ factors. $S$ is the accumulated shift and $u = 2^{-53}$ is the unit roundoff.

**Input.** The $2n - 1$ entries of $B$, real and of any sign. A dense matrix is first reduced to this form by the bidiagonalization phase of the [Golub-Kahan SVD algorithm](/golub-kahan-svd-algorithm/).

**Output.** $\sigma_1 \ge \dots \ge \sigma_n$, with no singular vectors.

## The algorithm

```pseudo id=main
DQDS(a_1..a_n, b_1..b_n-1)
L1  q_k ← a_k², e_k ← b_k²;  S ← 0
L2  while n > 0: if n = 1 or e_n-1 ≤ u² (S + q_n) then record S + q_n, n ← n − 1, and repeat L2
L3      τ ← 1 / Σ_j c_j with c_1 = 1/q_1, c_j = (1 + e_j-1 c_j-1)/q_j  (Newton lower bound for σ_min²); τ ← 0 if some q_k = 0
L4      d ← q_1 − τ
L5      for k ← 1 to n − 1 do
L6          q̂_k ← d + e_k
L7          ê_k ← e_k · (q_k+1 / q̂_k)
L8          d ← d · (q_k+1 / q̂_k) − τ;  if d < 0 then τ was too large: set τ ← 0 and go to L4
L9      q̂_n ← d;  (q, e) ← (q̂, ê)
L10     S ← S + τ
L11 return the square roots of the recorded values, sorted in decreasing order
```

Lines L4 to L9 are one dqds transform. If $\hat q_k = 0$ at L6, then $d = e_k = 0$. The block splits there, so the code sets $\hat e_k = 0$ and $d = q_{k+1} - \tau$. The shift at L3 is the step Newton's method takes on $\det(BB^T - xI)$ from $x = 0$, namely $1/\operatorname{tr}((BB^T)^{-1}) = 1/\lVert B^{-1}\rVert_F^2$. It is a lower bound for $\sigma_n^2$, so in exact arithmetic the test at L8 never fires. In floating point $\tau$ can land a few ulps above $\sigma_n^2$, and L8 then retries with $\tau = 0$.

## Example

Take the graded bidiagonal with $a = (1, 10^{-4}, 10^{-8}, 10^{-12})$ and $b = (1, 10^{-4}, 10^{-8})$. Its singular values range from $1.4$ down to $5 \cdot 10^{-13}$. Then $q = (1, 10^{-8}, 10^{-16}, 10^{-24})$ and $e = (1, 10^{-8}, 10^{-16})$. In this table the vectors show $\hat q$ and $\hat e$ after each transform.

| Step | $n$ | $\tau$ | $\hat q$ | $\hat e$ |
|---|---|---|---|---|
| 1 | 4 | $2.5 \cdot 10^{-25}$ | $(2,\ 1.5 \cdot 10^{-8},\ 1.333 \cdot 10^{-16},\ 4.69 \cdot 10^{-34})$ | $(5 \cdot 10^{-9},\ 6.67 \cdot 10^{-17},\ 7.5 \cdot 10^{-25})$ |
| 2 | 4 | $4.69 \cdot 10^{-34}$ | $(2,\ 1.5 \cdot 10^{-8},\ 1.333 \cdot 10^{-16},\ 0)$ | $(3.75 \cdot 10^{-17},\ 5.93 \cdot 10^{-25},\ 2.64 \cdot 10^{-42})$ |
| 3 | 4 | $0$ | $(2,\ 1.5 \cdot 10^{-8},\ 1.333 \cdot 10^{-16},\ 0)$ | $(2.81 \cdot 10^{-25},\ 5.27 \cdot 10^{-33},\ 0)$ |
| 4 | 3 | $1.333 \cdot 10^{-16}$ | $(2,\ 1.5 \cdot 10^{-8},\ 1.19 \cdot 10^{-24})$ | $(2.11 \cdot 10^{-33},\ 4.68 \cdot 10^{-41})$ |
| 5 | 3 | $1.19 \cdot 10^{-24}$ | $(2,\ 1.5 \cdot 10^{-8},\ 0)$ | $(1.58 \cdot 10^{-41},\ 3.70 \cdot 10^{-57})$ |

After step 1 the shift already has $S = 2.5 \cdot 10^{-25}$, close to $\sigma_4^2$. Step 2 subtracts nearly all of what is left, and $\hat q_4$ rounds to $0$. Step 3 uses $\tau = 0$, because $B$ is now singular, and $e_3$ becomes exactly $0$. So $\sigma_4^2 = S + q_4$ deflates. Two more transforms on the leading $3 \times 3$ part bring $e_2$ below the test, and $e_1$ is then negligible as well. The result is

$$\sigma = (1.414213564140862,\ 1.2247448725823134 \cdot 10^{-4},\ 1.1547005390608457 \cdot 10^{-8},\ 4.9999999859375 \cdot 10^{-13}).$$

This took five transforms with no rejected shift. Each value agrees to within $2 \cdot 10^{-16}$ relative with a reference computed by exact rational Sturm bisection on $B^T B$. On $a = (10^{-12}, 10^{-4}, 10^{-8}, 1)$, $b = (10^{-6}, 10^{-6}, 10^{-2})$, the shifted bidiagonal QR code of the [Golub-Kahan page](/golub-kahan-svd-algorithm/) gets the smallest singular value, $7.07 \cdot 10^{-13}$, with relative error $3.6 \cdot 10^{-13}$. That error is absolute accuracy, $u \sigma_1$ in size. dqds gets it exactly.

## Correctness

The [proof page](proofs/correctness.md) gives the details. In exact arithmetic there are four steps.

1. **The transform.** Lines L4 to L9 give $\hat B^T \hat B = BB^T - \tau I$. The diagonal of each side is $\hat q_k + \hat e_{k-1} = q_k + e_k - \tau$. The squared off-diagonal is $\hat q_k \hat e_k = q_{k+1} e_k$. The recurrence for $d_k = q_k - \hat e_{k-1} - \tau$ is the same identity rearranged so that it has no subtraction of $e$'s. So the eigenvalues of $\hat B^T \hat B$ are $\sigma_i^2 - \tau$, and $S + \sigma_i(\hat B)^2$ stays equal to the original $\sigma_i^2$.
2. **Positivity.** $d_k$ is the last Cholesky pivot of $B_k B_k^T - \tau I$, where $B_k$ is the leading $k \times k$ block of $B$. Since $B$ is upper triangular, $B_k^{-1}$ is a block of $B^{-1}$, so $\sigma_{\min}(B_k) \ge \sigma_n$. Hence $\tau < \sigma_n^2$ gives every $d_k > 0$. Conversely, all $\hat q_k > 0$ makes $BB^T - \tau I$ positive definite.
3. **The shift.** $1/\sum_i \sigma_i^{-2} \le \sigma_n^2$, and $c_j = \lVert B^{-1} e_j \rVert_2^2$.
4. **Deflation.** When $e_{n-1} \le u^2 (S + q_n)$, dropping $e_{n-1}$ changes the represented matrix $BB^T + SI$ by a symmetric matrix of 2-norm at most $(u + u^2)(S + q_n)$. By [Weyl's inequality](/weyls-inequality/), no eigenvalue moves by more than that.

The loop stops: each pass either removes a row or counts a transform, and the count is capped at $60n$. Convergence is a separate theorem. With $\tau = 0$, $e_k$ tends to zero like $(\sigma_{k+1}/\sigma_k)^{2t}$ after $t$ steps, as in Rutishauser's qd. Aishima, Matsuo, Murota and Sugihara proved global convergence of dqds for a class of shift strategies.

In floating point, Fernando and Parlett showed that one computed transform is an exact transform of $(q, e)$ perturbed by a few ulps in each entry, and that its output is also off by a few ulps in each entry. Demmel and Kahan showed that relative perturbations of size $\eta$ in the $2n - 1$ entries of a bidiagonal change each singular value by a relative amount of at most about $(2n - 1)\eta$. Together these say that each $\sigma_i$ is computed to a relative error of a small multiple of $u$ per transform, independent of $\sigma_i / \sigma_1$.

## Complexity

- **Per transform.** On an active block of order $m$, one transform costs $m - 1$ divisions and $4(m - 1)$ other flops, about $5m$ flops. The Newton shift costs about $4m$ more. Both counts are exact for the code.
- **Total.** The number of transforms per singular value is observed, not proved. With the plain Newton shift, this implementation used 8.4 transforms per value at $n = 50$, 8.8 at $n = 100$ and 9.1 at $n = 200$, on bidiagonals with entries uniform in $[0.1, 1]$ and seed 1. That gives about $9 \cdot 9m$ flops per deflation, about $40 n^2$ flops in total, so $O(n^2)$ is the typical cost. The rejected shifts in those runs numbered 2, 4 and 31, and each rejection costs one extra transform. LAPACK's `xLASQ` routines use sharper shifts and need fewer transforms. This page does not measure them.
- **Worst case.** No useful bound on the number of transforms is proved. The code stops with an error after $60n$ transforms.
- **Space.** $\Theta(n)$. The algorithm can work in place in one array of $4n$ numbers, as LAPACK does.

## Properties

- **High relative accuracy.** Every singular value, however small, is computed with a relative error of a modest multiple of $u$. This holds when the entries of $B$ determine the values to that accuracy, and by the Demmel-Kahan theory they always do. Shifted QR on $B$ is only absolutely accurate, $O(u \sigma_1)$.
- **Positivity as a test.** A transform succeeds with all $\hat q_k > 0$ exactly when $\tau < \sigma_n^2$, so a failed transform is a cheap test that a shift was too large. This is also how dqds checks an eigenvalue bound.
- **Exact zeros.** If some $a_k = 0$, then $\sigma_n = 0$, and dqds returns it as exactly $0$. The zero-shift pass splits the matrix there.
- **No vectors.** dqds produces values only. Singular vectors need another method, such as [MRRR](/mrrr-algorithm/), [inverse iteration](/inverse-iteration/) or [divide and conquer](/divide-and-conquer-eigensolver/).
- **Sign blind.** Squaring removes the signs of the entries, which do not affect the singular values.

## Variants and improvements

- **qd and LR.** Rutishauser's 1954 qd scheme uses the progressive form $\hat q_k = q_k + e_k - \hat e_{k-1} - \tau$, which subtracts and can lose accuracy. The differential form is what removes that subtraction. Rutishauser's 1958 LR algorithm is the same step for general matrices. For a positive definite matrix, two Cholesky LR steps give the same matrix as one QR step.
- **dqd.** The case $\tau = 0$. It converges linearly, at rate $(\sigma_{k+1}/\sigma_k)^2$. It is closely related to the zero-shift bidiagonal QR of Demmel and Kahan.
- **The LAPACK implementation (Parlett and Marques).** `xLASQ1` to `xLASQ6` add several pieces:
  - shifts from the pivot $d_{\min}$ and from $2 \times 2$ and $3 \times 3$ analysis;
  - ping-pong storage that keeps both $(q, e)$ and $(\hat q, \hat e)$;
  - flipping the matrix when its top is smaller than its bottom;
  - deflation of one or two values at a time;
  - checks for underflow and overflow.
- **Faster convergence.** Aishima and co-workers studied shift strategies that give cubic or superquadratic asymptotic convergence. Nakatsukasa, Aishima and Yamazaki added aggressive early deflation.
- **Eigenvalues of tridiagonals.** For a positive definite tridiagonal $T = LL^T$, dqds on the Cholesky factor gives the eigenvalues of $T$ to high relative accuracy. MRRR uses this inside the [tridiagonal eigenproblem](/tridiagonal-eigenproblem/) solver `xSTEGR` to refine eigenvalues of each $LDL^T$ representation.

## When to use it

Use dqds when you need the singular values of a bidiagonal matrix, or of a dense matrix after bidiagonalization, and no vectors. It is the fastest standard method for that job and the only common one that also gets tiny singular values to full relative accuracy. For a few values in an interval, [bisection](/bisection-eigenvalue-algorithm/) on the associated tridiagonal is cheaper. If you need vectors as well, pair it with MRRR, or use [divide and conquer](/divide-and-conquer-eigensolver/) or bidiagonal [QR](/golub-kahan-svd-algorithm/).

## Pitfalls

- **Overflow and underflow.** Squaring doubles the exponent range. Entries near $10^{\pm 154}$ overflow or underflow in $q$ and $e$. Scale $B$ by a power of 2 first.
- **Shift too large.** In floating point even a provable lower bound can land just above $\sigma_n^2$. The algorithm must detect a negative $d$ and redo the transform with a smaller shift, never accept negative values.
- **Accumulated shift.** The recorded value is $S + q_n$, not $q_n$. Forgetting $S$, or adding $\tau$ to $S$ before the transform is accepted, gives wrong values.
- **Deflation tests.** A test of the form $e_{n-1} \le u\,(\text{something large})$ keeps backward stability but destroys relative accuracy for graded matrices. The test must compare $e_{n-1}$ with the deflated value $S + q_n$ itself.
- **Forming $B^T B$.** Building the tridiagonal $B^T B$ and running a symmetric eigensolver on it loses relative accuracy for small $\sigma_i$. dqds never forms it.
- **Ordering.** Values come out in deflation order, not sorted. Sort at the end.

## Implementations

## History

Heinz Rutishauser introduced the quotient-difference algorithm in 1954 to find poles of continued fractions and zeros of polynomials. He then turned it into the LR algorithm (1958), a forerunner of QR. For decades qd was seen as unstable. In 1990 Demmel and Kahan showed that bidiagonal matrices determine their singular values to high relative accuracy and gave a zero-shift QR that attains it. Fernando and Parlett found in 1994 that the differential form of qd with shifts keeps that accuracy while running faster than QR. Parlett and Marques turned it into the LAPACK routines `xLASQ1` to `xLASQ6`, released with LAPACK 3.0 in 1999.

## References
