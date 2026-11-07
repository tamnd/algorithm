---
tag: TXN1K8
kind: algorithm
slug: hagers-condition-estimator
name: Hager's condition estimator
aliases:
- Hager-Higham estimator
- Hager's method
- 1-norm condition estimator
- LACON
area: numerical/linear-systems
level: research
summary: Estimate the 1-norm condition number cheaply from a few solves with the factorization.
model: floating-point-model
complexity:
  vars: {n: "the order of A", t: "the iteration limit, 5 in LAPACK"}
  time: {worst: O(t n^2)}
  space: {extra: Θ(n)}
  products: {worst: "2 t + 1"}
  flops: {worst: "4 t n^2 + 2 n^2 + O(t n)"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: true}
prereqs: [condition-number, matrix-norms, lu-decomposition]
see_also: [condition-number, power-iteration, lup-decomposition, linear-system-solving, iterative-refinement, growth-factor, hilbert-matrix, back-substitution]
sources:
  - paper: doi:10.1137/0905023
    title: William W. Hager, Condition estimates, SIAM Journal on Scientific and Statistical Computing 5(2), 1984
    locator: pp. 311 to 316 (the 1-norm estimator as ascent on a convex function, and the local maximum test)
  - paper: doi:10.1145/50063.214386
    title: Nicholas J. Higham, FORTRAN codes for estimating the one-norm of a real or complex matrix, with applications to condition estimation (Algorithm 674), ACM Transactions on Mathematical Software 14(4), 1988
    locator: pp. 381 to 396 (the refined algorithm used in LAPACK xLACON, the iteration limit and the alternative vector)
  - paper: doi:10.1137/S0895479899356080
    title: Nicholas J. Higham and Françoise Tisseur, A block algorithm for matrix 1-norm estimation, with an application to 1-norm pseudospectra, SIAM Journal on Matrix Analysis and Applications 21(4), 2000
    locator: pp. 1185 to 1201 (the block estimator behind MATLAB condest and normest1)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 15, Condition Number Estimation (the p-norm power method, Hager's estimator and its LAPACK form, counterexamples)
  - paper: doi:10.1137/0716029
    title: A. K. Cline, C. B. Moler, G. W. Stewart and J. H. Wilkinson, An estimate for the condition number of a matrix, SIAM Journal on Numerical Analysis 16(2), 1979
    locator: pp. 368 to 375 (the LINPACK estimator that preceded Hager's)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 3.5, Improving and Estimating Accuracy (condition estimation)
  - paper: "David W. Boyd, The power method for l^p norms, Linear Algebra and its Applications 9, 1974"
    title: The power method for l^p norms
    locator: pp. 95 to 101
---

Hager's estimator computes a lower bound for $\|B\|_1$, usually exact or within a factor $3$, using only a few products with $B$ and $B^T$. Applied to $B = A^{-1}$ with an existing LU factorization, every product is a pair of triangular solves costing $2 n^2$ flops, so the 1-norm condition number $\kappa_1(A) = \|A\|_1 \|A^{-1}\|_1$ is estimated in $O(n^2)$ flops, typically $4$ or $5$ solves, against the $2 n^3$ of forming the inverse. The method maximizes the convex function $f(x) = \|B x\|_1$ over the unit 1-norm ball, whose maximum is at a vertex $\pm e_j$, by moving from vertex to vertex along a subgradient. Each step increases the estimate strictly, and the stopping test certifies a local maximum. Higham's refinement, used in LAPACK's `xGECON` through `xLACON`, adds an iteration limit, a test for repeated sign vectors and an extra probe vector. Without it the method can fail by an arbitrary factor, and even with it counterexamples exist, so the result is an estimate and not a bound from above.

## In plain words

Knowing how sensitive a linear system is matters as much as solving it, but the exact sensitivity needs the inverse matrix, which costs much more than the solve. This estimator asks a few clever questions instead. It solves the system for a test right-hand side, looks at the signs of the answer, and uses them to pick the next test that should give a bigger answer. After two or three rounds the answer stops growing, and its size is the estimate. It is never too large, it is usually exactly right, and it costs about as much as a few extra solves.

## The problem

Given $B \in \mathbb{R}^{n \times n}$ through the operations $x \mapsto B x$ and $x \mapsto B^T x$, estimate $\|B\|_1 = \max_j \sum_i |b_{ij}|$. For condition estimation $B = A^{-1}$, applied with the factors of $P A = L U$.

**Notation.** $e = (1, \ldots, 1)^T$, $e_j$ the unit vectors, $f(x) = \|B x\|_1$, $\xi = \operatorname{sign}(y)$ with $\operatorname{sign}(0) = 1$, and $z = B^T \xi$. Since $f(x) \ge \xi^T B x = z^T x$ for every $x$, with equality at the point where $\xi$ was taken, $z$ is a subgradient of $f$. The estimate is $\gamma \le \|B\|_1$, and $t$ is the iteration limit. $\hat\kappa_1 = \|A\|_1 \gamma$ is the condition estimate and $u = 2^{-53}$.

## The algorithm

```pseudo id=main
NORM1-ESTIMATE(B, Bᵀ, n, t)
L1  x ← e / n
L2  for it ← 1 to t do
L3      y ← B x
L4      if it > 1 and ‖y‖₁ ≤ γ then stop the loop; γ ← ‖y‖₁
L5      ξ ← sign(y); if ξ equals the previous ξ then stop the loop
L6      z ← Bᵀ ξ
L7      j ← an index with |z_j| = ‖z‖_∞
L8      if it > 1 and ‖z‖_∞ ≤ zᵀ x then stop the loop  (local maximum)
L9      x ← e_j
L10 b ← ((−1)^i (1 + i/(n − 1)))ᵢ; γ ← max(γ, 2 ‖B b‖₁ / (3n))
L11 return γ
```

This is Higham's form. Hager's original applies the test of line L8 also at the first iteration, has no limit $t$, and omits lines L5 (second half) and L10. For the condition number, call it with $B x = U^{-1} L^{-1} P x$ and $B^T x = P^T L^{-T} U^{-T} x$, and multiply by $\|A\|_1$.

## Example

Take $A = \operatorname{tridiag}(-1, 2, -1)$ of order $3$, so $\|A\|_1 = 4$ and $A^{-1} = \frac14 \begin{pmatrix} 3 & 2 & 1 \\ 2 & 4 & 2 \\ 1 & 2 & 3 \end{pmatrix}$, $\|A^{-1}\|_1 = 2$.

| it | $x$ | $y = A^{-1} x$ | $\|y\|_1$ | $z = A^{-T} \xi$ | $z^T x$ | action |
|---|---|---|---|---|---|---|
| 1 | $\frac13 e$ | $(\frac12, \frac23, \frac12)$ | $\frac53$ | $(\frac32, 2, \frac32)$ | $\frac53$ | $x \leftarrow e_2$ |
| 2 | $e_2$ | $(\frac12, 1, \frac12)$ | $2$ | | | $\xi$ repeated, stop |

The probe of line L10 is $b = (1, -\frac32, 2)$, with $A^{-1} b = (\frac12, 0, 1)$ and $2 \cdot \frac32 / 9 = \frac13 < 2$. So $\gamma = 2$ and $\hat\kappa_1 = 8 = \kappa_1(A)$, exactly, after $4$ solves. Hager's original form reaches the same $\gamma$, stopping instead at line L8 because $\|z\|_\infty = 2 = z^T e_2$.

## Correctness

The proofs are in `proofs/correctness.md`. Exact arithmetic.

1. **Lower bound (proved).** Every candidate is $\|B v\|_1 / \|v\|_1$ for a nonzero $v$, so $\gamma \le \|B\|_1$; the alternative of line L10 is scaled by $\|b\|_1 = 3n/2$.
2. **The maximum is at a vertex (proved).** $f$ is convex and the unit 1-norm ball is the convex hull of $\pm e_j$, so $\max_{\|x\|_1 = 1} f(x) = \max_j \|B e_j\|_1 = \|B\|_1$.
3. **Strict ascent (proved, Hager 1984).** If $\|z\|_\infty > z^T x$, then $f(e_j) \ge |z_j| > z^T x = f(x)$. So until the stopping test holds, each iteration strictly increases the estimate.
4. **Local optimality (proved, Hager 1984).** If $\|z\|_\infty \le z^T x$ and $y$ has no zero entries, then $f(w) \le f(x)$ for every $w$ in the unit ball close enough to $x$: $x$ is a local maximum.
5. **Termination (proved).** After the first iteration $x$ is a vertex, and by item 3 no vertex is visited twice, so Hager's form stops within $n + 1$ iterations and Higham's within $t$.
6. **Not a guarantee (proved by counterexample).** For $B = I - (1 - \delta) e e^T / n$, $B e = \delta e$ and $z = \delta e$, so Hager's form stops at once with $\gamma = \delta$ while $\|B\|_1 \approx 2$; the ratio is arbitrarily bad. Higham's form skips the test at the first step and finds the exact value here, but there are matrices on which it also underestimates by an arbitrary factor (Higham 2002, Chapter 15).

**Quality in practice (observed).** On $500$ random integer matrices $B$ of order up to $9$ the estimate is exact $57\%$ of the time, and over $89\%$ of the time for $B = A^{-1}$ of random integer $A$. The worst ratio found on $150$ random Gaussian matrices, a quarter of them with tiny diagonals, is above $0.2$. For the [Hilbert matrices](/hilbert-matrix/) of order $2$ to $10$ the estimate agrees with $\kappa_1$ to $10^{-4}$ and $\hat\kappa_1(H_{10}) \approx 3.5 \times 10^{13}$, using at most $5$ solves. Higham reports that the LAPACK estimator is within a factor $3$ of the true value in almost all cases tested.

**Floating point.** The solves are backward stable when the factorization is, so each computed $y$ is the exact $(A + \Delta A)^{-1} x$ for a small $\Delta A$ depending on $x$; when $\kappa_1(A) u \ll 1$ this changes the estimate by a relative amount of order $\kappa_1(A) u$, which is harmless since only the order of magnitude is wanted. When $\kappa_1(A) u \gtrsim 1$ the estimate is still of the order of $1/u$ or larger, correctly signalling that the matrix is singular to working precision. An exact zero pivot is reported as singular.

## Complexity

Each iteration makes one product with $B$ and one with $B^T$, and line L10 one more, so at most $2 t + 1$ products: $11$ for $t = 5$, and in practice $4$ or $5$. With LU factors each product costs $2 n^2 + O(n)$ flops (a forward and a back substitution), giving at most $4 t n^2 + 2 n^2 + O(t n)$ flops, compared with $\frac23 n^3$ for the factorization. The other operations of an iteration are $O(n)$. The extra storage is the vectors $x$, $y$, $\xi$, $z$, $b$: $\Theta(n)$. Proofs are in `proofs/complexity.md`.

## Properties

- **Matrix free**: only products with $B$ and $B^T$, so it estimates $\|A^{-1}\|_1$, $\| |A^{-1}| |A| \|_\infty$ (Skeel's condition number, by a diagonal scaling of the products) or the norm of any operator given implicitly.
- **Lower bound** in exact arithmetic, and deterministic.
- **The 1-norm and $\infty$-norm**: $\|A^{-1}\|_\infty = \|A^{-T}\|_1$, so the same code with the roles of the solves exchanged gives $\kappa_\infty$; the 2-norm condition number is within a factor $n$.
- **Cheap**: $O(n^2)$ against the $O(n^3)$ factorization, so LAPACK drivers (`xGESVX`, `xPOSVX`) always return it as `RCOND`.

## Variants and improvements

- **The LINPACK estimator** (Cline, Moler, Stewart and Wilkinson 1979). Chooses the right-hand side of $U^T y = d$ with $d_i = \pm 1$ greedily to make $y$ large, then solves once more. Comparable cost, with known counterexamples (Cline and Rew 1983).
- **Boyd's power method for $p$-norms** (1974). Hager's method is its $p = 1$ case; for $1 < p < \infty$ the iteration converges to a local maximum of $\|B x\|_p / \|x\|_p$.
- **Block estimator** (Higham and Tisseur 2000). Iterates with $t'$ columns at once, starting from $e$ and random $\pm 1$ vectors, and avoids parallel columns; with $t' = 2$ it is MATLAB's `condest` and `normest1`, and it underestimates by more than a small factor very rarely. Being random, it can be rerun to gain confidence.
- **Componentwise and structured estimates.** Estimating $\| |A^{-1}| g \|_\infty$ for a positive vector $g$ gives the componentwise condition numbers and the error bounds returned by LAPACK's expert drivers.
- **Incremental estimators** (Bischof 1990). Update a 2-norm estimate of a triangular factor column by column, used in rank-revealing QR.
- **Randomized estimators.** Products with Gaussian vectors give probabilistic bounds on $\|B\|_2$ or $\|B\|_F$ with explicit failure probabilities (Dixon 1983; Kenney and Laub).

## When to use it

Use it after every LU or Cholesky solve where the user needs to know whether the answer can be trusted: compare $\hat\kappa_1 u$ with the accuracy needed, or with $1$ to detect numerical singularity. Use it to choose between a direct solve and a more careful method, to drive [iterative refinement](/iterative-refinement/) and error bounds, and inside algorithms that need norm estimates of implicitly given matrices (matrix functions, pseudospectra). When a guaranteed upper bound is needed, it is not the right tool; compute the inverse or use interval methods.

## Pitfalls

- **Underestimation.** The result is a lower bound and can be wrong by a large factor; Hager's form fails on $B = I - (1 - \delta) e e^T / n$. Use Higham's form or the block version, and treat the estimate as an order of magnitude.
- **It needs $B^T$.** Forgetting the transpose, or solving with $A$ instead of $A^T$ in the second product, silently gives a wrong ascent direction.
- **Reciprocal or not.** LAPACK returns $\mathrm{RCOND} = 1/\hat\kappa_1$, to avoid overflow for singular matrices; mixing the two conventions inverts the conclusion.
- **Estimates of a different matrix.** In floating point the estimate is for the computed factors, that is for $A + \Delta A$; for a nearly singular $A$ this is all one can expect.
- **Sign of zero.** $\operatorname{sign}(0)$ must be $1$ (or $-1$) consistently, otherwise $\xi$ has zeros and the ascent can stall.

## Implementations

## History

Before 1979 condition numbers were rarely reported because computing $\|A^{-1}\|$ seemed to cost as much as the inverse. Cline, Moler, Stewart and Wilkinson introduced the LINPACK estimator, which made `RCOND` routine. Hager (1984) observed that the 1-norm of $A^{-1}$ is the maximum of a convex function over a polytope and gave the ascent method, which is the $p = 1$ case of Boyd's 1974 power method. Higham (1988) analysed its failures, added the safeguards and the alternative vector, and his Fortran codes became LAPACK's `xLACON`, later `xLACN2`. Higham and Tisseur (2000) generalized it to the block estimator used in MATLAB.

## References
