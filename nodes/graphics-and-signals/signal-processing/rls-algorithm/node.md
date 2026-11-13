---
tag: BJHGVT
kind: algorithm
slug: rls-algorithm
name: Recursive least squares
aliases:
- RLS
area: graphics-and-signals/signal-processing
level: advanced
summary: "Keep the exact solution of a weighted, regularized least squares problem up to date on each new sample with the Sherman-Morrison formula: O(M^2) per sample and no matrix inverse."
solves: [adaptive-filtering]
model: real-ram
complexity:
  vars: {M: the number of taps, N: the number of samples}
  time: {worst: O(N M^2)}
  space: {extra: O(M^2)}
properties: {deterministic: true, online: true, recursive: false, exact: true}
history:
  year: 1950
  people: [Robin L. Plackett]
  note: "Plackett showed in 1950 how to update a least squares estimate when a new observation arrives without solving the normal equations again; the method became a standard adaptive filter in the 1970s."
prereqs: [adaptive-filtering, least-squares-problem]
see_also: [lms-algorithm, kalman-filter, sherman-morrison-formula, woodbury-identity, ridge-regression, normal-equations, qr-decomposition, linear-regression]
sources:
  - book: isbn:9780132671453
    title: "Simon Haykin, Adaptive Filter Theory, fifth edition, Pearson, 2014"
    locator: "Chapter 9 (the method of least squares) and Chapter 10 (the RLS algorithm: the matrix inversion lemma, the update recursions, the choice of the start value, and the convergence analysis)"
  - paper: "R. L. Plackett, Some theorems in least squares, Biometrika 37(1/2), 1950"
    locator: "pages 149 to 157, the recursive update of the least squares estimate and of its covariance when one observation is added"
  - book: isbn:9780133457117
    title: "Steven M. Kay, Fundamentals of Statistical Signal Processing, Volume I, Estimation Theory, Prentice Hall, 1993"
    locator: "Chapter 8 (least squares, including sequential least squares and its weighted form)"
  - book: isbn:9780131873742
    title: "John G. Proakis and Dimitris G. Manolakis, Digital Signal Processing, Principles, Algorithms, and Applications, fourth edition, Pearson Prentice Hall, 2007"
    locator: "Chapter 13 (adaptive filters: the recursive least squares algorithms for direct-form FIR filters and their properties)"
---

The recursive least squares (RLS) algorithm adapts the taps of an FIR filter so that, after every sample, they are the exact solution of a least squares problem on all the data so far. Older errors get the weight $\lambda^{\text{age}}$ for a forgetting factor $0 < \lambda \le 1$, and the start value adds a small ridge penalty. Instead of solving the [normal equations](/normal-equations/) again for each sample, RLS keeps the inverse $P$ of the weighted correlation matrix and updates it with the [Sherman-Morrison formula](/sherman-morrison-formula/), a rank-one case of the [Woodbury identity](/woodbury-identity/). Each sample costs $O(M^2)$ operations for $M$ taps, more than the $O(M)$ of the [LMS algorithm](/lms-algorithm/). In return, RLS converges in a few times $M$ samples, whatever the spread of the eigenvalues of the input correlation matrix, and for $\lambda = 1$ it has no excess error in the limit.

## In plain words

You want the filter weights that best explain all the data seen so far, in the sense of the smallest sum of squared errors. Solving that problem from scratch for each new sample would be slow. RLS keeps a summary of the past, a matrix that says how sure it is about each weight and how the weights depend on each other. When a new sample arrives, it predicts the target with the current weights, looks at the error, and corrects the weights by an amount that the summary says is right. It then updates the summary. The result is exactly the best answer for all the data, but each step takes only a few passes over the matrix. A forgetting factor below one makes old data count less, so the filter can follow changes.

## The problem

The inputs are an input signal $x[0], x[1], \ldots$, a desired signal $d[0], d[1], \ldots$, a number of taps $M$, a forgetting factor $0 < \lambda \le 1$ and a regularization $\delta > 0$. Let $u_i = (x[i], \ldots, x[i-M+1])$ with zeros before $x[0]$. After time $n$, the output is the tap vector that minimizes

$$C_n(w) = \sum_{i=0}^{n} \lambda^{n-i}\, (d[i] - w^T u_i)^2 + \lambda^{n+1} \delta\, \|w\|^2,$$

the weighted [least squares problem](/least-squares-problem/) with a ridge term. Its solution is $w_n = \Phi_n^{-1} z_n$ with $\Phi_n = \lambda^{n+1}\delta I + \sum_i \lambda^{n-i} u_i u_i^T$ and $z_n = \sum_i \lambda^{n-i} d[i]\, u_i$. This is the deterministic form of [adaptive filtering](/adaptive-filtering/): it uses the data, not their statistics.

## The algorithm

```pseudo id=main
RLS(x, d, M, λ, δ)                                ▷ 0 < λ ≤ 1, δ > 0
L1  w ← (0, .., 0); P ← δ⁻¹ I                      ▷ M taps, M × M matrix
L2  for n ← 0, 1, 2, ... do
L3      u ← (x[n], x[n − 1], .., x[n − M + 1])     ▷ x[m] = 0 for m < 0
L4      π ← P u
L5      k ← π / (λ + uᵀ π)                          ▷ the gain vector
L6      ξ ← d[n] − wᵀ u                             ▷ the a priori error
L7      w ← w + k · ξ
L8      P ← (P − k πᵀ) / λ
L9  return w, P
```

Line L1 is the start value: $P = \Phi_{-1}^{-1}$ with $\Phi_{-1} = \delta I$, which is the source of the ridge term in $C_n$. A small $\delta$, so a large $P$, says that the start taps are very uncertain. Line L4 computes $P u$ once, because lines L5 and L8 both need it. Line L5 is the gain, which says how much each tap should move per unit of error on this sample. Line L6 is the error of the old taps on the new sample, and line L7 corrects the taps. Line L8 is the Sherman-Morrison update of $\Phi_n^{-1} = (\lambda \Phi_{n-1} + u u^T)^{-1}$; the division by $\lambda$ makes the old data count less. There is no matrix inverse and no division except by the scalar $\lambda + u^T \pi$, which is at least $\lambda$.

## Example

Use the data of the LMS example: $d[n] = x[n] + \frac12 x[n-1]$ on $x = (1, -1, 2, 0, 1, -2)$, so $d = (1, -\frac12, \frac32, 1, 1, -\frac32)$, with $M = 2$, $\lambda = 1$ and $\delta = 1$, so $P = I$ at the start.

| $n$ | $u$ | $u^T \pi$ | $k$ (line L5) | $\xi$ (line L6) | $w$ after line L7 |
|---|---|---|---|---|---|
| 0 | $(1, 0)$ | $1$ | $(1/2,\ 0)$ | $1$ | $(1/2,\ 0)$ |
| 1 | $(-1, 1)$ | $3/2$ | $(-1/5,\ 2/5)$ | $0$ | $(1/2,\ 0)$ |
| 2 | $(2, -1)$ | $7/5$ | $(1/4,\ -1/12)$ | $1/2$ | $(5/8,\ -1/24)$ |
| 3 | $(0, 2)$ | $7/3$ | $(3/20,\ 7/20)$ | $13/12$ | $(63/80,\ 27/80)$ |
| 4 | $(1, 0)$ | $7/40$ | $(7/47,\ 3/47)$ | $17/80$ | $(77/94,\ 33/94)$ |
| 5 | $(-2, 1)$ | $24/47$ | $(-11/71,\ 2/71)$ | $-10/47$ | $(121/142,\ 49/142)$ |

At $n = 1$ the old taps already predict $d[1]$ exactly, so $\xi = 0$ and only $P$ changes. Check the last row against the batch answer: $\sum u u^T = \begin{bmatrix} 11 & -5 \\ -5 & 7 \end{bmatrix}$, so $\Phi_5 = \begin{bmatrix} 12 & -5 \\ -5 & 8 \end{bmatrix}$ with determinant $71$, and $P = \Phi_5^{-1} = \frac{1}{71}\begin{bmatrix} 8 & 5 \\ 5 & 12 \end{bmatrix}$, which is the matrix that line L8 leaves. With $z_5 = \sum d[i]\, u_i = (\frac{17}{2}, -\frac32)$, $\Phi_5^{-1} z_5 = (\frac{121}{142}, \frac{49}{142}) \approx (0.852, 0.345)$. The taps are below the true $(1, \frac12)$ because the ridge term $\|w\|^2$ from $\delta = 1$ is still large next to six samples; it fades as $\Phi_n$ grows.

## Correctness

**Claim.** After the pass for time $n$, $P = \Phi_n^{-1}$ and $w = \Phi_n^{-1} z_n$, the unique minimizer of $C_n$. For $\lambda = 1$ this is the regularized batch least squares answer $(\delta I + \sum_i u_i u_i^T)^{-1} \sum_i d[i]\, u_i$, set by the start value $P = \delta^{-1} I$.

**Key invariant.** $P \Phi_n = I$ and $w = P z_n$, where $\Phi_n = \lambda \Phi_{n-1} + u_n u_n^T$ and $z_n = \lambda z_{n-1} + d[n]\, u_n$.

Line L8 keeps the first part because of the Sherman-Morrison formula, and the same formula gives $\Phi_n^{-1} u_n = k$, which turns $\Phi_n^{-1} z_n$ into $w + k\, \xi$, the update of line L7. The full proof is below. The tests check the claim exactly in fractions on 500 random problems, for $\lambda = 1$ and for $\lambda < 1$, and to $10^{-9}$ in floating point.

## Complexity

Line L4 costs $M^2$ multiplications, line L5 costs $M$ multiplications and $M$ divisions, lines L6 and L7 cost $2M$, and line L8 costs $M^2$ multiplications and $M^2$ divisions by $\lambda$, which become multiplications by $1/\lambda$. So each sample costs about $2M^2 + O(M)$ multiplications, or $1.5 M^2$ if line L8 uses the symmetry of $P$, and $N$ samples cost $O(N M^2)$ in the [real RAM](/real-ram/). This is far less than solving the normal equations again on each sample, $O(M^3)$ per sample. The extra space is $O(M^2)$ for $P$. For a tapped delay line, the shift structure of $u$ allows fast RLS algorithms with $O(M)$ operations per sample.

## Properties

- **Exact at every step.** The taps are the exact minimizer of $C_n$ after every sample, not an approximation that converges to it. In exact arithmetic the implementation reproduces the batch answer in fractions.
- **Fast convergence.** RLS whitens the input through $P$, so its speed does not depend on the eigenvalue spread of the input correlation matrix. As a rule of thumb it converges in about $2M$ samples, against hundreds or thousands for LMS on colored input.
- **No excess error for $\lambda = 1$.** In a stationary setting, the taps converge to the Wiener solution and their error falls like $1/n$. For $\lambda < 1$ the filter has a memory of about $1/(1 - \lambda)$ samples, the taps keep a jitter that grows with $1 - \lambda$ and $M$, and the filter can follow changes.
- **The start value is a ridge penalty.** $\delta$ acts like [ridge regression](/ridge-regression/) with weight $\lambda^{n+1}\delta$. For $\lambda = 1$ its influence on the answer falls like $1/n$; for $\lambda < 1$ it fades exponentially.
- **Link with the Kalman filter.** RLS is the [Kalman filter](/kalman-filter/) for a constant state $w$ observed through $d[n] = u_n^T w + v[n]$, with $P$ as the error covariance divided by the noise variance; the forgetting factor plays the role of process noise that inflates the covariance.
- **The error shrinks on the current sample.** The error after the update is $\frac{\lambda}{\lambda + u^T P u}$ times the error before it. It is never larger in size, and it is smaller whenever $u \ne 0$ and the error before it is not zero.
- **Numerical behavior.** In floating point, the update of line L8 can lose the symmetry and the positive definiteness of $P$, above all for $\lambda < 1$ over long runs, and the filter then diverges. Square-root and QR-based forms avoid this.

## Variants and improvements

- **Sliding-window RLS.** Add the new sample and remove the sample $L$ steps old with a second, downdating rank-one step, for an exact least squares answer on the last $L$ samples.
- **QR-decomposition RLS.** Update a triangular factor of $\Phi_n$ by Givens rotations instead of its inverse, as in the [QR decomposition](/qr-decomposition/). It is numerically stable and maps onto systolic arrays.
- **Inverse QR and square-root RLS.** Propagate a square root of $P$ so that the computed $P$ stays symmetric positive definite.
- **Fast RLS and lattice RLS.** For a tapped delay line, the fast transversal filter and the least squares lattice use the shift structure of $u$ to cost $O(M)$ per sample, with the same answer in exact arithmetic but more delicate numerics.
- **Variable and directional forgetting.** Change $\lambda$ with the data, or forget only in the directions that the new input excites, to avoid the windup of $P$ when the input does not excite every direction.
- **Weighted and vector observations.** The same update with a weight per sample, or the [Woodbury identity](/woodbury-identity/) for a block of new observations at once, gives weighted or block RLS.

## When to use it

Use RLS when fast convergence matters, the input is colored, the number of taps is moderate, and $O(M^2)$ operations per sample are affordable: channel equalization in training mode, system identification and control, and adaptive [beamforming](/beamforming/) with few sensors. Use it also as an online solver for [linear regression](/linear-regression/) when the rows arrive one at a time. Use [LMS](/lms-algorithm/) for very long filters or small hardware, and a [Kalman filter](/kalman-filter/) when the taps follow a known dynamic model.

## Pitfalls

- **Windup with forgetting.** With $\lambda < 1$ and an input that stops exciting some direction, for example a long silence, line L8 divides $P$ by $\lambda$ on every sample in that direction, and $P$ grows like $\lambda^{-n}$ until one large input makes a huge jump in line L7. Use $\lambda = 1$ when excitation can stop, add regularization, or use directional forgetting.
- **A wrong start value.** A tiny $P$ in line L1, from a large $\delta$, freezes the taps near zero for a long time, because the gain of line L5 is small. A huge $P$ makes the first steps sensitive to noise. Take $\delta$ small next to the input power, for example $\delta = 0.01\, r_x[0]$, when the signal-to-noise ratio is high.
- **The a posteriori error in line L7.** Line L7 must use $\xi$ from line L6, the error of the taps before the update. Using the error after the update gives a different, wrong recursion.
- **Losing symmetry in floating point.** Computing line L8 as written can make $P$ slightly asymmetric, and the error grows. Compute only the upper triangle and copy it, or use a square-root form.
- **Forgetting the division by λ.** Writing line L8 as $P - k\pi^T$ for $\lambda < 1$ leaves $P$ equal to $\lambda\, \Phi_n^{-1}$ after one step, the error compounds on every later step, and the taps no longer minimize $C_n$. Line L8 must divide by $\lambda$.

## Implementations

## History

Gauss's method of least squares from the early nineteenth century is the starting point. In 1950 Plackett gave the formulas that update a least squares estimate and its covariance when one more observation arrives, which is the recursion of RLS with $\lambda = 1$. Kalman's filter of 1960 contains the same update as a special case, for a state that does not change. In the 1970s RLS and its Kalman form were applied to the fast training of adaptive equalizers for data transmission, and in the late 1970s and the 1980s fast transversal and lattice versions with $O(M)$ operations per sample, and QR-based versions with good numerical behavior, were developed.

## References
