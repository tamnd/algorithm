---
tag: A8T6DS
kind: algorithm
slug: randomized-pca
name: Randomized PCA
aliases:
- randomized principal component analysis
- randomized SVD for PCA
- PCA by randomized subspace iteration
area: machine-learning/dimensionality-reduction
level: advanced
summary: "Find the top k principal components from a random sketch of the centered data: multiply by a Gaussian matrix, orthonormalize, do a few power steps, then take the SVD of a small matrix."
model: real-ram
complexity:
  vars: {n: the number of points, d: the number of features, k: the number of components, p: the oversampling, q: the number of power iterations}
  time: {worst: "O((q + 1) n d (k + p) + (q + 1) (n + d) (k + p)^2)"}
  space: {extra: "O((n + d) (k + p))"}
properties: {deterministic: false, randomized: true, exact: false, online: false, recursive: false}
history:
  year: 2011
  people: [Nathan Halko, Per-Gunnar Martinsson, Joel A. Tropp]
  note: "Halko, Martinsson and Tropp (SIAM Review, 2011) unified earlier work on random sketches of matrices into the range finder with oversampling and power iterations, and proved bounds on the expected error. Rokhlin, Szlam and Tygert (2009) gave a randomized algorithm for PCA in the same years."
prereqs: [principal-component-analysis, singular-value-decomposition, qr-decomposition]
see_also: [incremental-pca, subspace-iteration, power-iteration, lanczos-algorithm, random-projection, johnson-lindenstrauss-lemma, gram-schmidt-process, latent-semantic-analysis]
sources:
  - paper: doi:10.1137/090771806
    title: Nathan Halko, Per-Gunnar Martinsson and Joel A. Tropp, Finding structure with randomness, probabilistic algorithms for constructing approximate matrix decompositions, SIAM Review 53(2), 217-288, 2011
    locator: Algorithm 4.1 (randomized range finder), Algorithm 4.4 (randomized subspace iteration), Algorithm 5.1 (direct SVD), Section 1.6 (cost), Theorems 10.5 and 10.6 (expected Frobenius and spectral error with a Gaussian test matrix) and Corollary 10.10 (power scheme)
  - paper: doi:10.1137/080736417
    title: Vladimir Rokhlin, Arthur Szlam and Mark Tygert, A randomized algorithm for principal component analysis, SIAM Journal on Matrix Analysis and Applications 31(3), 1100-1124, 2009
    locator: the randomized algorithm for the top principal components with power iterations, and its error analysis
  - paper: doi:10.1007/BF02288367
    title: Carl Eckart and Gale Young, The approximation of one matrix by another of lower rank, Psychometrika 1(3), 211-218, 1936
    locator: the best rank-k approximation is the truncated SVD, so sigma_{k+1} is the smallest spectral error of a rank-k basis
---

Randomized PCA finds the top $k$ principal components of $n$ points in $\mathbb{R}^d$ without a full eigendecomposition. It multiplies the centered data matrix by a random Gaussian matrix with $k + p$ columns, so that the product captures most of the leading column space, orthonormalizes the result, and optionally sharpens it with $q$ power iterations. Then it projects the data on this small basis and takes the exact [SVD](/singular-value-decomposition/) of the small matrix. This is the randomized range finder with subspace iteration of Halko, Martinsson and Tropp (2011), applied to [PCA](/principal-component-analysis/). The cost is $O(n d k)$ for fixed $p$ and $q$, against $O(n d \min(n, d))$ for a full SVD, and the expected error is within a small factor of the best possible error $\sigma_{k+1}$.

## In plain words

PCA looks for the few directions in which the data spread the most. A full method looks at all $d$ directions, which is slow when $d$ and $n$ are large.

Randomized PCA takes a short cut. Mix the features at random into $k + p$ new "probe" features and compute their values for every point. A random mix almost always has a part along each of the main directions, and the main directions are large, so the probe columns span roughly the main directions. Then do the exact computation inside this small space. If the probes are not good enough, multiply by the data matrix and its transpose a few more times: each step makes the big directions grow faster than the small ones, so the space lines up better with the main directions.

## The problem

**Input.** An $n \times d$ data matrix $X$ whose rows are points, a target number of components $k$, an oversampling $p \ge 0$, a number of power iterations $q \ge 0$ and a source of random numbers.

**Output.** The mean $\mu$, $k$ orthonormal vectors $v_1, \ldots, v_k \in \mathbb{R}^d$ (the approximate principal directions), and the values $\lambda_j = s_j^2 / n$ (the approximate eigenvalues of the covariance with divisor $n$). With $X_c = X - \mathbf{1}\mu^T$, the quality is measured by the range error $\|(I - Q Q^T) X_c\|_2$, where $Q$ is the $n \times \ell$ basis found by the algorithm and $\ell = k + p$. By the theorem of Eckart and Young no basis with $k$ columns does better than $\sigma_{k+1}$, the $(k+1)$th singular value of $X_c$.

## The algorithm

Write $\ell = \min(k + p, n, d)$ and let $\operatorname{orth}(Y)$ be an orthonormal basis of the column space of $Y$, for example from a thin [QR decomposition](/qr-decomposition/) or [Gram-Schmidt](/gram-schmidt-process/).

```pseudo id=main
RANDOMIZED-PCA(X, k, p, q)
L1  μ ← mean of the rows of X;  X_c ← X − 1 μᵀ
L2  Ω ← d × ℓ matrix of independent N(0, 1) entries
L3  Q ← orth(X_c Ω)                         ▷ n × ℓ, the randomized range finder
L4  for i ← 1 to q do
L5      Q̂ ← orth(X_cᵀ Q)                    ▷ d × ℓ
L6      Q ← orth(X_c Q̂)                     ▷ n × ℓ
L7  B ← Qᵀ X_c                               ▷ ℓ × d, small
L8  (Ũ, s, V) ← SVD of B, values in decreasing order
L9  return μ, the first k columns of V, s_j² / n for j ≤ k
```

Lines L2 and L3 are Algorithm 4.1 of Halko et al. Lines L4 to L6 are their Algorithm 4.4, randomized subspace iteration: the basis spans the range of $(X_c X_c^T)^q X_c \Omega$, and the orthonormalization after every product keeps the small singular values from being lost to rounding. Lines L7 and L8 are their Algorithm 5.1, the direct SVD: if $B = \tilde U \operatorname{diag}(s) V^T$, then $Q Q^T X_c = (Q \tilde U) \operatorname{diag}(s) V^T$ is an exact SVD, so the rows of $V^T$ are the principal directions of the projected data $Q Q^T X_c$.

The implementation computes the SVD in L8 with the one-sided Jacobi method of Hestenes on the columns of $B^T$, which gives the right singular vectors of $B$ directly, and computes orth with modified Gram-Schmidt applied twice.

## Example

**Small case, by hand.** Take the eight points of the [PCA](/principal-component-analysis/) page, with mean $(4, 5, 6)$ and covariance eigenvalues $81, 36, 9$ for the directions $(1, 2, 2)/3$, $(2, 1, -2)/3$, $(2, -2, 1)/3$. Use $k = 1$, $p = 0$, and to make the numbers exact replace the Gaussian $\Omega$ by the fixed vector $\omega = e_1 = (1, 0, 0)$. Then $Q$ is the unit vector along $X_c (X_c^T X_c)^q \omega$, and the output direction is along $(X_c^T X_c)^{q+1} \omega$. Since $e_1 = \tfrac13 v_1 + \tfrac23 v_2 + \tfrac23 v_3$, each power step multiplies the three parts by $8 \cdot 81$, $8 \cdot 36$ and $8 \cdot 9$.

| $q$ | output direction | estimate of $\lambda_1 = 81$ | angle to $v_1$ |
|---|---|---|---|
| 0 | $(0.7919, 0.6008, 0.1092)$ | 46.2414 | 42.5° |
| 1 | $(0.5701, 0.7270, 0.3826)$ | 69.0607 | 21.6° |
| 2 | $(0.4454, 0.7125, 0.5422)$ | 78.0766 | 9.96° |
| 3 | $(0.3844, 0.6904, 0.6129)$ | 80.3917 | 4.46° |

For $q = 0$ the estimate is $\lambda = \omega^T G^2 \omega / (n\, \omega^T G \omega) = 1341/29 = 46.2414$ with $G = X_c^T X_c$. The angle falls by about the factor $36/81$ per step, the ratio of the second and the first eigenvalue. With $p = 2$ the sketch has $\ell = 3 = d$ columns, it spans everything, and the output is exact for every $\Omega$: the implementation returns $81$ and $(1, 2, 2)/3$ up to sign.

**Larger case.** A planted matrix with $n = 200$, $d = 40$, the centered singular values $\sigma_j = 10 \cdot 0.5^{j-1}$ and $k = 5$ has $\sigma_6 = 0.3125$ and $\sigma_{11} = 0.0098$. Five Gaussian seeds give these range errors $\|(I - QQ^T)X_c\|_2$:

| | $q = 0$ | $q = 1$ | $q = 2$ |
|---|---|---|---|
| $p = 0$ | 0.57 to 1.1 | 0.313 to 0.332 | 0.3125 to 0.3138 |
| $p = 5$ | 0.029 to 0.073 | 0.0099 to 0.0104 | 0.0098 |

With $p = 0$ and one or two power steps the error is within a few percent of the best value $\sigma_6$. With $p = 5$ the basis has 10 columns, so the error falls to near $\sigma_{11}$, and the top five singular values come out correct to many digits. Theorem 10.6 bounds the expected error for $p = 5$, $q = 0$ by 1.28; the actual errors are much smaller, because the singular values decay fast. For the slow decay $\sigma_j = 10/\sqrt{j}$ and $p = 5$ the errors are 5.2 to 6.5 for $q = 0$ and 3.2 to 3.6 for $q = 2$, against $\sigma_6 = 4.08$, and here the power steps matter.

## Correctness

Two facts hold for every $\Omega$, in exact arithmetic.

1. The output is the exact PCA of the projected data $Q Q^T X_c$. The vectors $v_j$ are orthonormal and $Q Q^T X_c v_j = s_j u_j$ with orthonormal $u_j = Q \tilde u_j$. If the range of $X_c$ is inside the range of $Q$, then $Q Q^T X_c = X_c$, and the output equals the PCA of $X$.
2. If $X_c$ has rank $r \le \ell$, then with probability 1 the range of $X_c \Omega$ is the whole range of $X_c$, so the result is exact. The reason is that $X_c = U_r \Sigma_r V_r^T$ and $V_r^T \Omega$ is an $r \times \ell$ Gaussian matrix, which has rank $r$ with probability 1. Power steps keep the range, because $(X_c X_c^T)^q X_c \Omega = U_r \Sigma_r^{2q+1} V_r^T \Omega$.

The proofs file proves both facts. For data of full rank the result is an approximation. With a standard Gaussian $\Omega$, $k \ge 2$, $p \ge 2$ and $k + p \le \min(n, d)$, Halko et al. prove (Theorems 10.5 and 10.6)

$$\mathbb{E}\, \|(I - QQ^T) X_c\|_F \le \Big(1 + \frac{k}{p - 1}\Big)^{1/2} \Big(\sum_{j > k} \sigma_j^2\Big)^{1/2},$$

$$\mathbb{E}\, \|(I - QQ^T) X_c\|_2 \le \Big(1 + \sqrt{\frac{k}{p - 1}}\Big) \sigma_{k+1} + \frac{e \sqrt{k + p}}{p} \Big(\sum_{j > k} \sigma_j^2\Big)^{1/2}.$$

With $q$ power steps, Corollary 10.10 gives the same bound for the matrix $(X_c X_c^T)^q X_c$, whose singular values are $\sigma_j^{2q+1}$, raised to the power $1/(2q+1)$. So the factor in front of $\sigma_{k+1}$ tends to 1 as $q$ grows. Halko et al. also show that the error is close to its mean with high probability (Corollary 10.9).

## Complexity

In the real RAM, with $\ell = k + p$:

- L1 takes $O(n d)$.
- L2 draws $d \ell$ numbers.
- L3, L5, L6 and L7 each multiply $X_c$ or $X_c^T$ by $\ell$ vectors, $O(n d \ell)$ each, and orthonormalize $\ell$ vectors of length $n$ or $d$, $O((n + d) \ell^2)$.
- L8 is the SVD of an $\ell \times d$ matrix, $O(d \ell^2)$ per Jacobi sweep, with few sweeps.

The total is $O((q + 1) n d \ell + (q + 1)(n + d) \ell^2)$, so $O(n d k)$ for fixed $p$ and $q$ and $k \le \min(n, d)$. This matches the count $(2q + 2)\, \ell$ products with the matrix in Section 1.6 of Halko et al. The extra memory is $O((n + d) \ell)$ for $Q$, $\hat Q$ and $B$. The implementation forms the centered copy $X_c$ for clarity; a large-scale version uses $X_c \Omega = X \Omega - \mathbf{1} (\mu^T \Omega)$ instead, which needs no copy and keeps a sparse $X$ sparse. The algorithm reads $X$ only $2q + 2$ times, which matters when $X$ is on disk.

## Properties

- **Randomized.** The result depends on $\Omega$. Fix the seed to make it repeatable.
- **Exact on low rank.** If the centered data have rank at most $k + p$, the answer is exact with probability 1.
- **Pass-efficient.** It reads the data $2q + 2$ times and uses only products with $X_c$ and $X_c^T$, so it works for sparse or implicit matrices.
- **Block method.** The products act on $\ell$ vectors at once, which uses matrix-matrix kernels and parallel hardware well, unlike [Lanczos](/lanczos-algorithm/), which uses one vector at a time.
- **Error controlled by $p$ and $q$.** Oversampling makes a failure unlikely; power steps fix slow decay of the singular values.

## Variants and improvements

- **Power iteration without re-orthonormalization** (Algorithm 4.3 of Halko et al.) computes $(X_c X_c^T)^q X_c \Omega$ directly. It is the same in exact arithmetic, but in floating point the singular values below $\epsilon^{1/(2q+1)} \sigma_1$ are lost.
- **Adaptive range finder** (Algorithm 4.2) adds random columns until an estimate of the error falls below a tolerance, when $k$ is not known.
- **Structured test matrices.** A subsampled randomized Fourier or Hadamard transform, as in the [fast Johnson-Lindenstrauss transform](/fast-johnson-lindenstrauss-transform/), computes $X \Omega$ in $O(n d \log \ell)$ time instead of $O(n d \ell)$. Sparse sign matrices, as in [sparse random projection](/sparse-random-projection/), also work.
- **Single-pass sketches.** When the data can be read only once, sketch both $X_c \Omega$ and $\Psi^T X_c$ and solve a small least squares problem for $B$ (Section 5.5 of Halko et al.).
- **Block Krylov methods** keep all the blocks $X_c \Omega, (X_c X_c^T) X_c \Omega, \ldots$ instead of the last one, and need fewer passes for the same accuracy.
- **[Incremental PCA](/incremental-pca/)** is a deterministic alternative for data that arrive in batches.

## When to use it

Use randomized PCA when $n$ and $d$ are both large, only a small number $k$ of components is needed, and an error near $\sigma_{k+1}$ is acceptable. It is the default solver for this case in several libraries. Take $p$ about 5 to 10, and $q = 1$ or $2$; use larger $q$ when the singular values decay slowly, for example for noisy text or image data. When $d$ is small, compute the covariance and diagonalize it. When high accuracy for each eigenvector is required, use [Lanczos](/lanczos-algorithm/) or the full SVD.

## Pitfalls

- **No oversampling.** With $p = 0$ the error varies a lot from seed to seed, because a square Gaussian matrix is often nearly singular. The bound of Theorem 10.6 needs $p \ge 2$.
- **Slow decay without power steps.** With $q = 0$ and flat singular values, the basis mixes in much noise, and both the directions and the eigenvalues are poor. The eigenvalue estimates are biased low, as in the example.
- **Forgetting to center.** A sketch of $X$ instead of $X_c$ finds the directions of the uncentered data. The first one points to the mean.
- **Power steps without orthonormalization.** Small singular values then underflow relative to the large ones, and the extra power steps make the result worse.
- **Range error is not eigenvector error.** A small range error does not mean that each $v_j$ is accurate when $\sigma_j$ and $\sigma_{j+1}$ are close; the subspace is good, but the individual directions inside it can rotate.

## Implementations

## History

Random projections to speed up low-rank approximation go back to Frieze, Kannan and Vempala (1998) and to Papadimitriou, Raghavan, Tamaki and Vempala (1998, latent semantic indexing). Sarlós (2006) and Martinsson, Rokhlin and Tygert (2006) used Gaussian and structured sketches for the SVD. Rokhlin, Szlam and Tygert (2009) gave a randomized algorithm for PCA with power iterations and an analysis. Halko, Martinsson and Tropp (2011) put these ideas into one framework: a randomized range finder followed by a deterministic factorization of a small matrix, with oversampling, power iterations, and bounds on the average and the tail of the error. Their survey made the method a standard tool, and it is now used by default in libraries such as scikit-learn for large PCA problems.

## References
