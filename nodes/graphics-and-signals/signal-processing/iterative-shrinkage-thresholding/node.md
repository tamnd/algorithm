---
tag: XSY6C1
kind: algorithm
slug: iterative-shrinkage-thresholding
name: Iterative shrinkage-thresholding algorithm
aliases:
- ISTA
area: graphics-and-signals/signal-processing
level: advanced
summary: Gradient step on the least squares misfit, then soft thresholding, repeated. It finds a sparse minimizer of the L1-penalized fit at rate O(1/k).
solves: [sparse-signal-recovery]
model: real-ram
complexity:
  vars: {m: the number of measurements, n: the number of unknowns, k: the number of iterations, L: "an upper bound on the largest eigenvalue of A^T A (the step is 1/L)", R: "the distance from x_0 to a minimizer", ε: "the target accuracy F(x_k) - F* ≤ ε"}
  time: {worst: Θ(k m n)}
  space: {extra: Θ(m + n)}
  steps: {worst: "⌈L R^2 / (2 ε)⌉"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2004
  people: [Ingrid Daubechies, Michel Defrise, Christine De Mol, Amir Beck, Marc Teboulle]
  note: Daubechies, Defrise and De Mol (2004) proved that the thresholded Landweber iteration converges. Beck and Teboulle (2009) proved the O(1/k) bound on the objective gap.
prereqs: [sparse-signal-recovery, proximal-operator, gradient-descent]
see_also: [proximal-gradient-method, fista, lasso-regression, basis-pursuit, orthogonal-matching-pursuit, coordinate-descent, compressed-sensing, signal-denoising]
sources:
  - paper: doi:10.1002/cpa.20042
    title: Ingrid Daubechies, Michel Defrise and Christine De Mol, An iterative thresholding algorithm for linear inverse problems with a sparsity constraint, Communications on Pure and Applied Mathematics 57(11), 2004
    locator: pages 1413 to 1457 (the thresholded Landweber iteration and the proof that it converges in norm)
  - paper: doi:10.1137/080716542
    title: Amir Beck and Marc Teboulle, A fast iterative shrinkage-thresholding algorithm for linear inverse problems, SIAM Journal on Imaging Sciences 2(1), 2009
    locator: Section 3, Theorem 3.1 (the O(1/k) bound on the objective gap with the step 1/L)
  - paper: doi:10.1137/070698920
    title: Elaine T. Hale, Wotao Yin and Yin Zhang, Fixed-point continuation for l1-minimization, methodology and convergence, SIAM Journal on Optimization 19(3), 2008
    locator: pages 1107 to 1130 (finite identification of the zero entries and the signs, linear convergence after that, and continuation in the penalty)
  - paper: doi:10.1109/18.382009
    title: David L. Donoho, De-noising by soft-thresholding, IEEE Transactions on Information Theory 41(3), 1995
    locator: pages 613 to 627 (soft thresholding of wavelet coefficients, the one-step case with an orthonormal matrix)
  - book: isbn:9781611974980
    title: Amir Beck, First-Order Methods in Optimization, SIAM, 2017
    locator: the chapter on the proximal gradient method (the l1-penalized least squares case and its rate)
---

The iterative shrinkage-thresholding algorithm minimizes $F(x) = \tfrac12\|Ax - y\|_2^2 + \lambda\|x\|_1$, the $\ell_1$-penalized least squares fit used for [sparse signal recovery](/sparse-signal-recovery/) and the [lasso](/lasso-regression/). Each step is one [gradient descent](/gradient-descent/) step on the misfit with step $1/L$, followed by soft thresholding at $\lambda/L$, which is the [proximal operator](/proximal-operator/) of the penalty. It needs only products with $A$ and $A^{\mathsf T}$, its iterates are sparse, and its objective gap is at most $L\|x_0 - x^*\|^2/(2k)$. This page treats the $\ell_1$ case; the general method is the [proximal gradient method](/proximal-gradient-method/).

## In plain words

You want a signal that explains the measurements well and has few nonzero entries. A weight sets the trade between these two goals.

Start from a guess, such as all zeros. Compute how the guess misses the measurements, and move the guess a small step in the direction that reduces the miss. Then shrink every entry toward zero by a fixed amount, and set each entry that is smaller than that amount to exactly zero. Repeat.

The step size comes from how strongly the measurement process can amplify a signal, so each step is safe. The shrink step is what makes the answer sparse. When a guess does not change any more, it is the best possible trade between the two goals. After some steps the set of zero entries stops changing, and from then on the method closes in on the answer quickly.

## The problem

**Input.** A matrix $A \in \mathbb R^{m \times n}$, a vector $y \in \mathbb R^m$, a penalty $\lambda > 0$, a number $L \ge \lambda_{\max}(A^{\mathsf T}A) = \|A\|_2^2$, a start $x_0 \in \mathbb R^n$ and a number of steps $K$.

**Output.** An iterate $x_K$ with $F(x_K) - F^* \le L\|x_0 - x^*\|_2^2/(2K)$, where $F^*$ is the minimum of $F(x) = \tfrac12\|Ax - y\|_2^2 + \lambda\|x\|_1$ and $x^*$ is a minimizer.

**Cost model.** The [real RAM](/real-ram/). With rational data and a rational $L$, every iterate is rational and can be computed exactly.

## The algorithm

The soft threshold at level $t \ge 0$ is $S_t(v) = \operatorname{sign}(v)\max(|v| - t, 0)$, applied to each entry.

```pseudo id=main
SHRINK-THRESHOLD(A, y, λ, L, x₀, K)
L1  x ← x₀                              ▷ x₀ = 0 is the usual start
L2  for k ← 1 to K:
L3      g ← Aᵀ(Ax − y)                  ▷ gradient of ½‖Ax − y‖²
L4      v ← x − g / L                   ▷ gradient step with step 1/L
L5      x ← S_{λ/L}(v)                  ▷ shrink each entry by λ/L, and zero it inside [−λ/L, λ/L]
L6  return x
```

Line L3 is the only expensive line: one product with $A$ and one with $A^{\mathsf T}$. When $A$ is a partial Fourier matrix or a wavelet synthesis, these are fast transforms and no matrix is stored. Line L5 is the proximal map of $(\lambda/L)\|\cdot\|_1$, which separates into one scalar problem per entry.

## Example

Let $A = \begin{pmatrix} 1 & 1 & 0 \\ 0 & 1 & 1 \end{pmatrix}$, $y = (3, 1)$ and $\lambda = \tfrac12$. The matrix $AA^{\mathsf T} = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ has eigenvalues $3$ and $1$, so $L = 3$ is the tight step bound, and the threshold is $\lambda/L = \tfrac16$.

The unique minimizer is $x^* = (\tfrac32, 1, 0)$ with $F^* = \tfrac{11}{8}$. At $x^*$, $A^{\mathsf T}(y - Ax^*) = (\tfrac12, \tfrac12, 0)$: the first two entries equal $\lambda$ times the sign of $x^*_j$, and the third lies strictly inside $[-\lambda, \lambda]$.

From $x_0 = 0$, line L3 gives $g = -A^{\mathsf T}y = (-3, -4, -1)$, line L4 gives $v = (1, \tfrac43, \tfrac13)$, and line L5 subtracts $\tfrac16$ from each entry: $x_1 = (\tfrac56, \tfrac76, \tfrac16)$. In the second step, $v = (\tfrac76, \tfrac{25}{18}, \tfrac1{18})$, and the third entry is below the threshold, so $x_2 = (1, \tfrac{11}9, 0)$. Here $R^2 = \|x_0 - x^*\|^2 = \tfrac{13}4$, so the bound is $LR^2/(2k) = \tfrac{39}{8k}$.

| $k$ | $x_k$ | $F(x_k) - F^*$ | bound $\tfrac{39}{8k}$ |
|---|---|---|---|
| 0 | $(0, 0, 0)$ | $\tfrac{29}8$ | |
| 1 | $(\tfrac56, \tfrac76, \tfrac16)$ | $\tfrac{19}{72} \approx 0.264$ | $4.875$ |
| 2 | $(1, \tfrac{11}9, 0)$ | $\tfrac{41}{648} \approx 0.0633$ | $2.4375$ |
| 3 | $(\tfrac{59}{54}, \tfrac{67}{54}, 0)$ | $\tfrac{125}{2916} \approx 0.0429$ | $1.625$ |
| 4 | $(\tfrac{31}{27}, \tfrac{197}{162}, 0)$ | $\tfrac{1709}{52488} \approx 0.0326$ | $1.21875$ |
| 10 | | $\approx 6.35 \times 10^{-3}$ | $0.4875$ |
| 20 | | $\approx 4.17 \times 10^{-4}$ | $0.24375$ |
| 30 | | $\approx 2.74 \times 10^{-5}$ | $0.1625$ |

From $k = 2$ on, the third entry stays $0$ and the first two stay positive. On that face the step is a fixed affine map, and the error in the first two entries is multiplied by $I - G/3$ with $G = A_S^{\mathsf T}A_S = \begin{pmatrix} 1 & 1 \\ 1 & 2 \end{pmatrix}$. Its slowest factor is $1 - \tfrac{3 - \sqrt5}{6} = \tfrac{3 + \sqrt5}6 \approx 0.873$, so the gap drops by $\big(\tfrac{3+\sqrt5}6\big)^2 \approx 0.762$ per step, which the exact iterates show from $k = 10$ on.

The minimizer $x^*$ is shrunk: the sparse vector $(2, 1, 0)$ fits $y$ exactly and is also the [basis pursuit](/basis-pursuit/) solution. A least squares refit on the support $\{1, 2\}$ of $x^*$ gives $(2, 1, 0)$ back. With $\lambda \ge \|A^{\mathsf T}y\|_\infty = 4$, the minimizer is $0$ and the iteration never leaves $x_0 = 0$.

## Correctness

The full proofs are below. Three facts carry them.

**Fixed points are exactly the minimizers.** Write $c = A^{\mathsf T}(y - Ax)$. Entry by entry, $x = S_{\lambda/L}(x + c/L)$ holds exactly when $c_j = \lambda\operatorname{sign}(x_j)$ for $x_j \ne 0$ and $|c_j| \le \lambda$ for $x_j = 0$. These are the optimality conditions $0 \in A^{\mathsf T}(Ax - y) + \lambda\,\partial\|x\|_1$, and $F$ is convex. The value of $L$ does not change the set of fixed points.

**Each step is a descent step with a distance bound.** For a quadratic misfit, $\tfrac12\|A(x^+ - x)\|^2 \le \tfrac L2\|x^+ - x\|^2$ when $L \ge \lambda_{\max}(A^{\mathsf T}A)$. With the subgradient that line L5 gives, this yields $F(x_{k+1}) \le F(z) + \tfrac L2(\|x_k - z\|^2 - \|x_{k+1} - z\|^2)$ for every $z$. Taking $z = x_k$ shows that $F$ never goes up, and summing with $z = x^*$ gives $F(x_k) - F^* \le L\|x_0 - x^*\|^2/(2k)$. The [proximal gradient method](/proximal-gradient-method/) page has this argument for a general smooth part.

**The support is found in finitely many steps.** The iterates converge to a minimizer $x^*$. If $|c^*_j| < \lambda$ for every $j$ with $x^*_j = 0$, then line L4 sends those entries into the open interval $(-\lambda/L, \lambda/L)$ after finitely many steps, so line L5 sets them to $0$, and the other entries take the signs of $x^*$.

## Complexity

Each iteration costs $\Theta(mn)$ for the two products in line L3 with a dense $A$, and $\Theta(n)$ for lines L4 and L5. With a fast transform, such as a fast Fourier or [fast wavelet transform](/fast-wavelet-transform/), it costs $O(n \log n)$ or $O(n)$ instead. Extra space is $\Theta(m + n)$ for the residual and the iterate.

The bound $L R^2/(2k)$ gives $\lceil L R^2/(2\varepsilon)\rceil$ iterations for accuracy $\varepsilon$ in the worst case. After the support and signs are fixed, the error on the support $S$ falls by the factor $1 - \mu_{\min}/L$ per step, where $\mu_{\min}$ is the smallest eigenvalue of $A_S^{\mathsf T}A_S$, whenever $A_S$ has full column rank. In sparse recovery the support is small and $A_S$ is well conditioned under the [restricted isometry property](/restricted-isometry-property/), so this local phase is fast. The number of steps before the support settles has no good a priori bound.

## Properties

- **Sparse iterates.** Every entry with $|v_j| \le \lambda/L$ becomes exactly $0$, so the iterates are sparse from the first step, unlike the iterates of a subgradient method.
- **The zero threshold.** $x^* = 0$ is a minimizer exactly when $\|A^{\mathsf T}y\|_\infty \le \lambda$. Then line L5 maps $0$ to $0$, and the run from $x_0 = 0$ stays there. So the useful range of the penalty is $0 < \lambda < \|A^{\mathsf T}y\|_\infty$.
- **Shrinkage bias.** Nonzero entries of $x^*$ are pulled toward zero, by a size of order $\lambda$. Even without noise, $x^*$ is not the sparse vector that produced $y$.
- **Link to basis pursuit.** As $\lambda \to 0$, every limit point of the minimizers is a solution of [basis pursuit](/basis-pursuit/), $\min\|x\|_1$ subject to $Ax = y$, when $y$ is in the range of $A$.
- **Orthonormal case.** If $A^{\mathsf T}A = I$, then $L = 1$ and one step from any start gives the exact minimizer $S_\lambda(A^{\mathsf T}y)$. This is soft thresholding of wavelet coefficients for [signal denoising](/signal-denoising/).
- **Non-unique minimizers.** When $m < n$, $F$ need not be strictly convex. The iterates still converge to one minimizer, which can depend on $x_0$.

## Variants and improvements

- **Acceleration.** [FISTA](/fista/) adds a momentum term to the same two lines and gets $O(1/k^2)$, with the same cost per step.
- **Continuation.** Solve for a decreasing sequence of penalties, from near $\|A^{\mathsf T}y\|_\infty$ down to the target $\lambda$, and start each run at the previous answer. Large penalties have small supports and converge fast, and the warm starts keep the supports small on the way down (Hale, Yin and Zhang 2008).
- **Debiasing.** After the support is found, refit the nonzero entries by [least squares](/least-squares-problem/), as [orthogonal matching pursuit](/orthogonal-matching-pursuit/) does at every step. This removes the shrinkage bias, as in the example.
- **Iterative hard thresholding.** Replace line L5 by keeping the $s$ largest entries and zeroing the rest. This targets the sparsity $s$ directly, not the $\ell_1$ penalty, and has recovery guarantees under the restricted isometry property.
- **Weighted and group thresholds.** A penalty $\sum_j w_j|x_j|$ gives the threshold $w_j\lambda/L$ per entry. A group penalty $\sum_G \|x_G\|_2$ gives block soft thresholding, which shrinks the norm of each group.
- **Unknown $L$.** Use the backtracking rule of the proximal gradient method, or estimate $\|A\|_2^2$ by a few steps of [power iteration](/power-iteration/).

## When to use it

Use it when $A$ is large and given as a fast operator, such as a partial Fourier matrix in [compressed sensing](/compressed-sensing/) or a blur followed by a wavelet synthesis in deconvolution, and moderate accuracy is enough. It needs two products per step, no matrix factorization, and no tuning beyond $\lambda$ and $L$. In practice, use [FISTA](/fista/) with the same lines for speed. For statistics problems with explicit columns, [coordinate descent](/coordinate-descent/) on the lasso is often faster. For small problems where an exact sparse solution is needed, solve [basis pursuit](/basis-pursuit/) as a linear program.

## Pitfalls

- **A step that is too long.** With $L$ below $\lambda_{\max}(A^{\mathsf T}A)$ the bound fails, and with $L < \lambda_{\max}/2$ the iteration can diverge. The squared Frobenius norm of $A$ is a safe bound, but it can be much larger than $\|A\|_2^2$ and makes every step short.
- **Small penalties are slow.** As $\lambda$ decreases, the supports grow and the local factor $1 - \mu_{\min}/L$ moves toward $1$. Use continuation.
- **Taking the minimizer as the signal.** The minimizer is biased toward zero. Debias before you read off values.
- **Stopping on the step length.** A small change between iterates can hide a large gap. A better test is the duality gap: with $r = y - Ax$ and $u = r \cdot \min(1, \lambda/\|A^{\mathsf T}r\|_\infty)$, the dual value $\langle u, y\rangle - \tfrac12\|u\|^2$ is a lower bound on $F^*$.
- **Columns of different scale.** The penalty treats all entries alike, so columns with large norms are favored. Normalize the columns, or use weights.

## Implementations

## History

Donoho (1995) showed that soft thresholding of wavelet coefficients removes noise well, which is the one-step case with an orthonormal matrix. In the early 2000s several groups used thresholding inside an iteration to solve deconvolution and other linear inverse problems with wavelet sparsity. Daubechies, Defrise and De Mol (2004) studied this iteration as a thresholded Landweber method and proved that it converges in norm, also in infinite dimensions. Hale, Yin and Zhang (2008) proved that the zero entries and the signs are found in finitely many steps, and that convergence is linear after that, and they used continuation in the penalty. Beck and Teboulle (2009) proved the $O(1/k)$ bound on the objective gap and introduced the accelerated version.

## References
