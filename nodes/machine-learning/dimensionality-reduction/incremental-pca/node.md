---
tag: 0NPZBY
kind: algorithm
slug: incremental-pca
name: Incremental PCA
aliases:
- online PCA
- incremental principal component analysis
- sequential Karhunen-Loeve algorithm with mean update
area: machine-learning/dimensionality-reduction
level: advanced
summary: "Update a thin SVD of the centered data batch by batch, with a correction column for the moving mean, so PCA never holds all the data. Exact when no rank is truncated."
model: real-ram
complexity:
  vars: {d: the number of features, k: the number of kept components, m: the batch size, N: the total number of points}
  time: {worst: "O((N / m) (d (k + m)^2 + (k + m)^3))", update: "O(d (k + m)^2 + (k + m)^3)"}
  space: {extra: "O(d (k + m))"}
properties: {deterministic: true, online: true, recursive: false}
history:
  year: 2008
  people: [David A. Ross, Jongwoo Lim, Ruei-Sung Lin, Ming-Hsuan Yang]
  note: Levy and Lindenbaum (2000) gave the Sequential Karhunen-Loeve update of a thin SVD. Ross, Lim, Lin and Yang (2008) added the mean update and analyzed the forgetting factor, for visual tracking.
prereqs: [principal-component-analysis, singular-value-decomposition]
see_also: [randomized-pca, covariance-matrix, streaming-model, gram-schmidt-process, stochastic-approximation, karhunen-loeve-transform, reconstruction-error, subspace-iteration]
sources:
  - paper: doi:10.1007/s11263-007-0075-7
    title: David A. Ross, Jongwoo Lim, Ruei-Sung Lin and Ming-Hsuan Yang, Incremental learning for robust visual tracking, International Journal of Computer Vision 77(1-3), 125-141, 2008
    locator: Section 3.1 (the SKL algorithm, Lemma 1 on the scatter of a concatenation, and Figure 1, the incremental PCA algorithm with mean update) and Section 3.1.1 (the forgetting factor, Lemma 2 and the modified mean update)
  - paper: "A. Levy and M. Lindenbaum, Sequential Karhunen-Loeve basis extraction and its application to images, IEEE Transactions on Image Processing 9(8), 1371-1374, 2000"
    title: Levy and Lindenbaum 2000
    locator: the Sequential Karhunen-Loeve update of the leading singular vectors when a block of new columns arrives, and the forgetting factor
  - paper: doi:10.1080/00031305.1983.10483115
    title: Tony F. Chan, Gene H. Golub and Randall J. LeVeque, Algorithms for computing the sample variance, analysis and recommendations, The American Statistician 37(3), 242-247, 1983
    locator: the formula that combines the sums of squares of two batches with a term in the difference of their means
  - paper: doi:10.1007/BF00275687
    title: Erkki Oja, Simplified neuron model as a principal component analyzer, Journal of Mathematical Biology 15(3), 267-273, 1982
    locator: the stochastic update w <- w + eta y (x - y w) with y = w^T x, which converges to the first principal direction
---

Incremental PCA keeps the top $k$ principal components of a data stream without storing the stream. It holds the mean, the count and a thin [singular value decomposition](/singular-value-decomposition/) $U \operatorname{diag}(\sigma)$ of the centered data seen so far. When a batch of $m$ new points arrives, it centers them on their own mean, adds one extra column that corrects for the change of the mean, and computes the SVD of a small $(k + m + 1)$-column matrix. This is the algorithm of Ross, Lim, Lin and Yang (2008), built on the Sequential Karhunen-Loeve update of Levy and Lindenbaum (2000). Without truncation it gives exactly the result of batch [PCA](/principal-component-analysis/). With truncation to $k$ components it is an approximation, and it is exact when the data have rank at most $k$.

## In plain words

Batch PCA needs all the data at once. When the data come in pieces, or do not fit in memory, you want to update the answer piece by piece.

The method keeps a short summary of the old data: the mean, the number of points, the main directions and how much spread there is along each one. When new points arrive, it puts the summary and the new points side by side and finds the main directions of this small combined table. The new mean differs from the old one, and this shift adds spread of its own, so the method adds one more column to account for it. Then it keeps the best $k$ directions and forgets the rest. If nothing important is forgotten, the result is the same as PCA on all the data.

## The problem

**Input.** A sequence of batches $B_1, B_2, \ldots$ of points in $\mathbb{R}^d$, with $m_t$ points in batch $t$, a number of components $k$, and optionally a forgetting factor $f \in (0, 1]$.

**State.** After the batches seen so far, which hold $n$ points with mean $\mu$ and scatter matrix $S = \sum_i (x_i - \mu)(x_i - \mu)^T$: a $d \times r$ matrix $U$ with orthonormal columns ($r \le k$) and singular values $\sigma_1 \ge \cdots \ge \sigma_r$, such that $U \operatorname{diag}(\sigma^2) U^T$ approximates $S$.

**Output after each batch.** The updated $\mu$, $n$, $U$ and $\sigma$. The principal directions are the columns of $U$, and the covariance eigenvalues (divisor $n$) are $\sigma_j^2 / n$. With $f = 1$ and no truncation, $U \operatorname{diag}(\sigma^2) U^T = S$ exactly.

## The algorithm

The new batch $B$ has the $m$ points $b_1, \ldots, b_m$ as columns. The update follows Figure 1 of Ross et al.:

```pseudo id=main
IPCA-UPDATE(U, σ, μ, n, B, k, f)              ▷ starts from r = 0 columns, n = 0
L1  μ_B ← (1/m) Σ_j b_j;  μ' ← (f n μ + m μ_B) / (f n + m)
L2  B̂ ← [b_1 − μ_B, …, b_m − μ_B, √(n m / (n + m)) (μ_B − μ)]   ▷ the last column only if n > 0
L3  P ← Uᵀ B̂;  E ← B̂ − U P                    ▷ the part of B̂ outside span U
L4  B̃ ← orth(E)                              ▷ an orthonormal basis of span E, by Gram-Schmidt
L5  R ← [ f diag(σ)   P ;  0   B̃ᵀ E ]          ▷ (r + p) × (r + m + 1), p = number of columns of B̃
L6  (Ũ, σ̃) ← left singular vectors and singular values of R, in decreasing order
L7  U ← [U  B̃] Ũ, keep the first k columns;  σ ← the first k values of σ̃
L8  return U, σ, μ', f n + m
```

**Why the extra column.** The scatter of the union of two sets $A$ and $B$ with $n$ and $m$ points is (Ross et al., Lemma 1; Chan, Golub and LeVeque 1983)

$$S_{A \cup B} = S_A + S_B + \frac{n m}{n + m} (\mu_B - \mu_A)(\mu_B - \mu_A)^T .$$

The last term is the outer product of the extra column of L2 with itself, and $S_B$ is the product of the other columns of $\hat B$ with their transposes. So $S_{A \cup B} = U \Sigma^2 U^T + \hat B \hat B^T$, the Gram matrix of the columns of $[U\Sigma, \hat B]$, and its eigenvectors are the left singular vectors of that $d \times (r + m + 1)$ matrix.

**Why the small SVD suffices.** Since $E$ lies in the span of $\tilde B$, $[U\ \tilde B] R = [U \Sigma,\ U P + E] = [U\Sigma,\ \hat B]$. If $R = \tilde U \tilde\Sigma \tilde V^T$, then $[U \Sigma, \hat B] = ([U\ \tilde B] \tilde U) \tilde\Sigma \tilde V^T$, and $[U\ \tilde B]\tilde U$ has orthonormal columns. So the left singular vectors of the large matrix come from those of $R$, which has only $r + p \le k + m + 1$ rows. The right factor $\tilde V$, whose size would grow with $n$, is never needed.

The implementation computes the SVD of L6 with the one-sided Jacobi method of Hestenes on $R^T$, and L4 with modified [Gram-Schmidt](/gram-schmidt-process/) applied twice, which drops columns whose remaining norm is at the rounding level.

**Forgetting.** With $f < 1$ the old singular values are multiplied by $f$, so the contribution of a batch to the scatter shrinks by $f^2$ at each later update (Ross et al., Lemma 2). The mean uses the weight $f n$ for the old data, and the effective count $n \leftarrow f n + m$ tends to $m / (1 - f)$ for constant batch size. This lets the components follow a slowly changing source, as in visual tracking.

## Example

Feed the eight points of the [PCA](/principal-component-analysis/) page, $(13, 11, 9), (9, 15, 7), (5, 7, 17), (1, 11, 15), (7, -1, -3), (3, 3, -5), (-1, -5, 5), (-5, -1, 3)$, in batches of 3, 3 and 2 points, with $k = 3$ and $f = 1$.

| after batch | $n$ | $\mu$ | eigenvalues $\sigma_j^2 / n$ |
|---|---|---|---|
| 1 | 3 | $(9, 11, 11)$ | 34.4222, 5.5778 |
| 2 | 6 | $(6.3333, 7.6667, 6.6667)$ | 83.2410, 20.7590, 9 |
| 3 | 8 | $(4, 5, 6)$ | 81, 36, 9 |

After the first batch the three points span a plane, so $r = 2$. In the second update, $\hat B$ has four columns: the three centered new points and $\sqrt{3 \cdot 3 / 6}\,(\mu_B - \mu) = \sqrt{1.5}\,\big((11, 13, 7)/3 - (9, 11, 11)\big) = \sqrt{1.5}\,(-16, -20, -26)/3$, since the second batch has the mean $(11, 13, 7)/3$. After the third batch the result is that of batch PCA: the eigenvalues $81, 36, 9$ and the components $\pm(1, 2, 2)/3$, $\pm(2, 1, -2)/3$, $\pm(2, -2, 1)/3$.

With $k = 2$, the second update drops the direction $\pm(2, -2, 1)/3$ with eigenvalue 9. The final result still has the exact top two components $81, 36$ here, because that direction is an eigenvector of the scatter of the first six points and of the scatter of all eight, so removing it does not change the other two. In general the dropped part is lost for good, and later batches cannot recover it.

## Correctness

The invariant is: after each update with $f = 1$ and no truncation, $\mu$ and $n$ are the mean and the count of all points seen, and $U \operatorname{diag}(\sigma^2) U^T$ is their scatter matrix, with $U$ orthonormal. The mean update in L1 is the weighted mean of two means. The scatter part follows from the merge formula and the identity $[U\ \tilde B] R = [U\Sigma, \hat B]$ shown above. Then the columns of $U$ are eigenvectors of the covariance $S / n$ with eigenvalues $\sigma_j^2 / n$, the same as batch PCA; when the eigenvalues are distinct, each column is unique up to sign. If the data have rank at most $k$ after centering, truncation in L7 only drops zero singular values, so the result is exact as well. The full proof is in the proofs file.

With truncation of nonzero singular values the algorithm is a heuristic: it computes the exact PCA of a perturbed data set, in which each dropped part is removed at the time it was dropped. The error is small when the dropped singular values are small at every step, but the method has no general bound against the batch answer.

## Complexity

In the real RAM, with $r \le k$ and the batch size $m$:

- L1 and L2 take $O(d m)$.
- L3 takes $O(d k m)$.
- L4 takes $O(d (k + m)^2)$ for Gram-Schmidt against $U$ and among the new columns.
- L5 takes $O(d (k + m)^2)$ for $\tilde B^T E$.
- L6 is the SVD of a matrix of size at most $(k + m + 1) \times (k + m + 1)$, $O((k + m)^3)$ for a dense method (a Jacobi sweep costs this, and few sweeps are needed).
- L7 takes $O(d (k + m) k)$.

So one update costs $O(d (k + m)^2 + (k + m)^3)$ and the memory is $O(d (k + m))$, independent of the number $n$ of points seen. For $N$ points in batches of size $m$ the total is $O((N/m)(d (k + m)^2 + (k + m)^3))$. With $m$ about $k$ this is $O(N d k)$, the same order as one pass of [randomized PCA](/randomized-pca/), against $O(N d^2 + d^3)$ for batch PCA through the covariance.

## Properties

- **Online.** Each point is used once, in its batch, and then can be discarded. This fits the [streaming model](/streaming-model/) with $O(d(k + m))$ memory.
- **Exact without truncation.** For $f = 1$ and $k$ at least the rank, the order and size of the batches do not matter.
- **Deterministic.** No random numbers, unlike [randomized PCA](/randomized-pca/) or Oja's rule with random sampling.
- **Order-dependent with truncation.** When nonzero parts are dropped, the result depends on the order and size of the batches.
- **Weighted with forgetting.** With $f < 1$ the result is the PCA of a weighted data set that favors recent batches; it is not the PCA of all the data.

## Variants and improvements

- **Without the mean.** The Sequential Karhunen-Loeve algorithm of Levy and Lindenbaum (2000) is the same update without the mean correction; it computes the SVD of the uncentered data.
- **Covariance accumulation.** When $d$ is small, keep the running mean and $d \times d$ scatter with Welford's update or the merge formula on the [covariance matrix](/covariance-matrix/) page, and diagonalize it when needed. This costs $O(d^2)$ memory and $O(d^2)$ per point, and it is exact.
- **Oja's rule.** Oja (1982) updates one direction per point by $w \leftarrow w + \eta\, y (x - y w)$ with $y = w^T x$, for centered $x$. It is a [stochastic approximation](/stochastic-approximation/) method: with suitable step sizes $\eta$ it converges to the first principal direction, but it is never exact in finite time, it needs a step size, and it gives no eigenvalues. Generalizations to $k$ directions (Sanger's rule, the subspace rule) exist. Incremental SVD is deterministic and exact without truncation, but each update costs more.
- **Brand's incremental SVD** and other low-rank updates of the SVD handle the removal of columns and missing values.
- **Block methods.** Streaming versions of [subspace iteration](/subspace-iteration/) process the data in passes and come with guarantees on the angle to the top subspace.

## When to use it

Use incremental PCA when the data do not fit in memory, when they arrive over time, or when the components must follow a slowly changing source (with $f < 1$). Choose the batch size $m$ at least $k$ so that each update is efficient. If $d$ is small (say up to a few hundred), accumulating the covariance is simpler and exact. If the data fit in memory and only the top $k$ components are needed, [randomized PCA](/randomized-pca/) or [Lanczos](/lanczos-algorithm/) is usually faster and has error bounds.

## Pitfalls

- **Forgetting the mean column.** Without the extra column of L2, the update computes the scatter of the batches around their own means, which misses the spread between the batch means. The error is large when the batches come from different parts of the space, for example sorted data.
- **Truncating too early.** If $k$ is close to the true number of strong components, a direction that is weak in the first batches and strong later is dropped early and lost. Keep a few extra components (oversampling) and report only the top $k$.
- **Loss of orthogonality.** After many updates, rounding errors make the columns of $U$ drift from orthonormal. Gram-Schmidt applied twice in L4, and a stable SVD in L6, keep the drift at the rounding level.
- **Batches of size 1.** They work, but each update then costs $O(d k^2 + k^3)$ for one point; use larger batches when possible.
- **The divisor.** The singular values describe the scatter; divide $\sigma_j^2$ by $n$ (or $n - 1$) to get variances, and by the effective $n$ when $f < 1$.

## Implementations

## History

Updating an SVD when columns are added is an old problem of numerical linear algebra. Levy and Lindenbaum (2000) gave the Sequential Karhunen-Loeve (SKL) algorithm, which updates the leading singular vectors of a growing matrix from a QR decomposition and a small SVD, with a forgetting factor. Ross, Lim, Lin and Yang (2008) observed that the SKL update ignores the change of the mean, proved the scatter merge lemma, added the correction column, and analyzed the forgetting factor, for the appearance model of a visual tracker. Oja (1982) had earlier given a neural update rule for the first principal component, the first of many stochastic methods for streaming PCA.

## References
