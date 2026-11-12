---
tag: 45RF44
kind: algorithm
slug: principal-component-analysis
name: Principal component analysis
aliases:
- PCA
- proper orthogonal decomposition
area: machine-learning/dimensionality-reduction
level: intro
summary: "Project centered data onto the k orthogonal directions of largest variance: the top eigenvectors of the covariance matrix, or the top right singular vectors of the data."
model: real-ram
complexity:
  vars: {n: the number of points, d: the number of features, k: the number of components}
  time: {worst: "O(n d^2 + d^3)"}
  space: {extra: "O(d^2 + n k)"}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1901
  people: [Karl Pearson, Harold Hotelling]
  note: Pearson (1901) found the line and plane of closest fit to a cloud of points. Hotelling (1933) derived the components as the directions of maximum variance and named them principal components.
prereqs: [covariance-matrix, symmetric-eigenproblem, singular-value-decomposition]
see_also: [explained-variance, reconstruction-error, whitening, kernel-pca, probabilistic-pca, randomized-pca, karhunen-loeve-transform, jacobi-eigenvalue-algorithm]
sources:
  - paper: doi:10.1080/14786440109462720
    title: Karl Pearson, On lines and planes of closest fit to systems of points in space, Philosophical Magazine, Series 6, 2(11), 559-572, 1901
    locator: the line and the plane that minimize the sum of squared perpendicular distances, through the centroid, along the axes of the correlation ellipsoid
  - paper: doi:10.1037/h0071325
    title: Harold Hotelling, Analysis of a complex of statistical variables into principal components, Journal of Educational Psychology 24(6), 417-441, and 24(7), 498-520, 1933
    locator: the components as successive directions of maximum variance of a set of correlated variables
  - book: isbn:9780387954424
    title: I. T. Jolliffe, Principal Component Analysis, second edition, Springer, 2002
    locator: Chapter 1 (definition and derivation), Chapter 2 (properties of population components, Section 2.3 on the correlation matrix) and Chapter 3 (properties of sample components)
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 12.1 (12.1.1 the maximum variance formulation, 12.1.2 the minimum error formulation, 12.1.4 PCA for high-dimensional data)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 14.5.1 (principal components and the SVD of the centered data matrix)
  - paper: doi:10.1007/BF02288367
    title: Carl Eckart and Gale Young, The approximation of one matrix by another of lower rank, Psychometrika 1(3), 211-218, 1936
    locator: the best approximation of lower rank in the least squares sense, from the singular value decomposition
---

Principal component analysis (PCA) replaces $d$ correlated features by $k \le d$ new coordinates, the principal components. They are the projections of the centered data onto the $k$ orthonormal directions of largest variance. The directions are the top $k$ eigenvectors of the [covariance matrix](/covariance-matrix/), or the top $k$ right singular vectors of the centered data matrix ([singular value decomposition](/singular-value-decomposition/)). The same subspace also minimizes the mean squared distance from the points to their projections. PCA is exact and has no local optima; the cost is $O(n d^2 + d^3)$ through the covariance matrix or $O(n d \min(n, d))$ through the SVD.

## In plain words

Think of a cloud of points in space, shaped like a flat, long cigar. Most of its spread is along the long axis, some along the width, and almost none along the thickness. PCA finds these axes. The first axis is the direction in which the points spread the most. The second axis is at right angles to the first and has the most spread of the rest, and so on.

To make the data smaller, keep only the first few axes and give each point its coordinates along them. You lose only the small spread along the axes you drop. Put another way, the kept axes form the flat sheet that passes closest to all the points. Maximum spread and minimum loss give the same answer.

## The problem

**Input.** A data matrix $X$ with $n$ rows $x_1, \ldots, x_n \in \mathbb{R}^d$ (the points, in Euclidean space), and the number of components $k$ with $0 \le k \le d$.

**Output.** A mean $\bar x$, a $d \times k$ matrix $W$ with orthonormal columns $w_1, \ldots, w_k$ (the principal directions, also called loadings), the eigenvalues $\lambda_1 \ge \cdots \ge \lambda_d$ of the covariance, and the $n \times k$ score matrix $Z$ with rows $z_i = W^T(x_i - \bar x)$.

**Two equivalent goals.** With $C = \frac{1}{n}\sum_i (x_i - \bar x)(x_i - \bar x)^T$:

- *Maximum variance* (Hotelling): maximize the variance of the projected data, $\operatorname{tr}(W^T C W)$, over all $W$ with $W^T W = I_k$.
- *Minimum reconstruction error* (Pearson): minimize $\frac{1}{n}\sum_i \|x_i - b - W W^T (x_i - b)\|^2$ over all such $W$ and all offsets $b$.

The proof below shows that both have the solution $W = [v_1, \ldots, v_k]$, the eigenvectors of $C$ for its $k$ largest eigenvalues, with $b = \bar x$. The optimal values are $\lambda_1 + \cdots + \lambda_k$ and $\lambda_{k+1} + \cdots + \lambda_d$; the second is the [reconstruction error](/reconstruction-error/) of PCA. The choice of the divisor $n$ or $n - 1$ in $C$ scales all eigenvalues by the same factor and does not change $W$.

## The algorithm

```pseudo id=main
PCA(X, k)                                  ▷ X has the points x_1 .. x_n as rows
L1  μ ← (1/n) Σ_i x_i
L2  for i ← 1 to n do y_i ← x_i − μ        ▷ center the data
L3  C ← (1/n) Σ_i y_i y_iᵀ                  ▷ the d × d covariance matrix
L4  (λ_1 .. λ_d, v_1 .. v_d) ← eigenpairs of C, sorted so that λ_1 ≥ … ≥ λ_d
L5  W ← [v_1, …, v_k]
L6  for i ← 1 to n do z_i ← Wᵀ y_i         ▷ the scores
L7  return μ, W, (λ_1 .. λ_d), (z_1 .. z_n)
```

Line L4 is a dense symmetric eigenproblem. The implementation uses the cyclic [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/). Each Jacobi rotation zeroes one off-diagonal pair of $C$; a sweep visits all pairs, and the sum of squares of the off-diagonal entries converges to zero quadratically. Libraries instead reduce $C$ to tridiagonal form and run the [QR algorithm](/qr-algorithm/) or a divide and conquer solver (see [symmetric eigenproblem](/symmetric-eigenproblem/)). The reconstruction of a point from its scores is $\hat x_i = \mu + W z_i$, and a new point $x$ gets the scores $W^T(x - \mu)$ with the training mean $\mu$.

**The SVD route.** Replace lines L3 and L4 by a thin SVD $X_c = U\Sigma V^T$ of the centered $n \times d$ matrix. Then $v_j$ is the $j$-th right singular vector, $\lambda_j = \sigma_j^2 / n$, and the scores are $U_k \Sigma_k$. This route never forms $X_c^T X_c$, which squares the condition number, so it is the more accurate one in floating point.

## Example

Take the $n = 8$ points $(13, 11, 9)$, $(9, 15, 7)$, $(5, 7, 17)$, $(1, 11, 15)$, $(7, -1, -3)$, $(3, 3, -5)$, $(-1, -5, 5)$, $(-5, -1, 3)$ in $\mathbb{R}^3$, and $k = 2$.

Line L1 gives $\mu = (4, 5, 6)$. Lines L2 and L3 give

$$C = \begin{pmatrix} 29 & 22 & 4 \\ 22 & 44 & 26 \\ 4 & 26 & 53 \end{pmatrix}, \qquad \operatorname{tr} C = 126.$$

Line L4 runs Jacobi sweeps. The table gives the norm of the off-diagonal part and the diagonal at the start of each sweep.

| sweep | off-diagonal norm | diagonal |
|---|---|---|
| 0 | 48.497 | 29, 44, 53 |
| 1 | 8.834 | 9.977, 80.703, 35.320 |
| 2 | 0.0614 | 9.000026, 80.999974, 36.000000 |
| 3 | $2.1 \times 10^{-12}$ | 9, 81, 36 |

The eigenvalues are $81, 36, 9$, with the unit eigenvectors $v_1 = \frac{1}{3}(1, 2, 2)$, $v_2 = \frac{1}{3}(2, 1, -2)$ and $v_3 = \frac{1}{3}(2, -2, 1)$, each up to sign. Line L5 keeps $W = [v_1, v_2]$. Line L6 gives the scores

| point | $z_{i1}$ | $z_{i2}$ |
|---|---|---|
| (13, 11, 9) | 9 | 6 |
| (9, 15, 7) | 9 | 6 |
| (5, 7, 17) | 9 | -6 |
| (1, 11, 15) | 9 | -6 |
| (7, -1, -3) | -9 | 6 |
| (3, 3, -5) | -9 | 6 |
| (-1, -5, 5) | -9 | -6 |
| (-5, -1, 3) | -9 | -6 |

The first score has variance $81 = \lambda_1$ and the second $36 = \lambda_2$, and the two are uncorrelated. The two kept components hold $117 / 126 \approx 92.9\%$ of the total variance. Each point lies at distance 3 from the plane $\mu + \operatorname{span}(v_1, v_2)$, along $\pm v_3$, so the mean squared reconstruction error is $9 = \lambda_3$. For example, $(13, 11, 9)$ is reconstructed as $(4,5,6) + 9 v_1 + 6 v_2 = (11, 13, 8)$, and the difference $(2, -2, 1) = 3 v_3$ has squared length 9.

## Correctness

Four short facts give the result. (1) The projected variance of a frame $W$ is $\operatorname{tr}(W^T C W)$. (2) For any offset $b$, the reconstruction error is the error with offset $\bar x$ plus a nonnegative term, so the best subspace goes through the mean. (3) By Pythagoras, the error with offset $\bar x$ equals $\operatorname{tr} C - \operatorname{tr}(W^T C W)$, so the two goals are one. (4) By the Ky Fan inequality, $\operatorname{tr}(W^T C W) \le \lambda_1 + \cdots + \lambda_k$, with equality at $W = [v_1, \ldots, v_k]$. The answer is unique up to the signs of the columns when $\lambda_1 > \cdots > \lambda_{k+1}$. When $\lambda_k = \lambda_{k+1}$ the best subspace is not unique, and inside a repeated eigenvalue any rotation of the eigenvectors is as good. The full proof is in the proofs file. In the SVD form, the result is the Eckart-Young theorem on the [singular value decomposition](/singular-value-decomposition/) page: $U_k \Sigma_k V_k^T$ is the best approximation of rank $k$ to $X_c$ in the Frobenius norm.

## Complexity

The model is the real RAM: each arithmetic operation on a real number costs one unit.

- Lines L1 and L2 take $O(n d)$ operations.
- Line L3 takes $O(n d^2)$ operations, or half of that with symmetry.
- Line L4 takes $O(d^3)$ operations for a dense symmetric eigensolver to working precision. A Jacobi sweep costs $O(d^3)$, and the number of sweeps is small (3 in the example) because of the quadratic convergence; it is not bounded by a constant in the worst case, but the tridiagonal QR method has an $O(d^3)$ bound.
- Line L6 takes $O(n d k)$ operations.

So the total is $O(n d^2 + d^3)$, and the extra memory is $O(d^2)$ for $C$ plus $O(n k)$ for the scores. The thin SVD of the $n \times d$ matrix costs $O(n d \min(n, d))$. When $n < d$ (for example, images or genes) this is better: it is the same as working with the $n \times n$ Gram matrix $X_c X_c^T$ (Bishop, Section 12.1.4). When only $k \ll \min(n, d)$ components are needed, [Lanczos](/lanczos-algorithm/) or [randomized PCA](/randomized-pca/) costs about $O(n d k)$.

## Properties

- **Deterministic and global.** There are no local optima and no starting point. The only freedom is the sign of each component and the rotation inside repeated eigenvalues.
- **Nested.** The best subspace of dimension $k$ contains the best one of dimension $k - 1$, when the eigenvalues are distinct. So one computation serves each $k$.
- **Uncorrelated scores.** The score covariance is $\operatorname{diag}(\lambda_1, \ldots, \lambda_k)$.
- **Invariant to rotation and translation** of the data. The components rotate with the data.
- **Not invariant to scaling.** Multiplying one feature by a constant changes the components. PCA on the correlation matrix, that is on standardized features, is a different method with different answers.
- **Linear.** PCA finds only flat subspaces. [Kernel PCA](/kernel-pca/) and [manifold learning](/manifold-learning/) find curved structure.

## Variants and improvements

- **Correlation PCA.** Standardize each feature to unit variance first, that is, take the eigenvectors of the correlation matrix. Use it when the features have different units.
- **Large or streaming data.** [Incremental PCA](/incremental-pca/) updates an SVD batch by batch. [Randomized PCA](/randomized-pca/) finds the top $k$ components with a random range finder.
- **Probabilistic PCA.** [Probabilistic PCA](/probabilistic-pca/) is a Gaussian latent variable model whose maximum likelihood solution spans the PCA subspace. [Factor analysis](/factor-analysis/) gives each feature its own noise variance.
- **Sparse and robust PCA.** [Sparse PCA](/sparse-pca/) asks for loadings with few nonzero entries. [Robust PCA](/robust-pca/) splits the data into a low-rank part and sparse gross errors.
- **Nonlinear PCA.** [Kernel PCA](/kernel-pca/) runs PCA in a feature space. A linear [autoencoder](/autoencoder/) with squared loss spans the PCA subspace at its optimum.
- **Whitening.** Divide each score by $\sqrt{\lambda_j}$ to get unit variance in all directions ([whitening](/whitening/)).
- **The same eigenbasis elsewhere.** In signal processing it is the [Karhunen-Loève transform](/karhunen-loeve-transform/), the optimal decorrelating transform for coding. In fluid dynamics it is the proper orthogonal decomposition.

## When to use it

Use PCA as the first step for linear dimensionality reduction: to compress, to plot data in two or three dimensions, to remove noise in the small components, and to decorrelate features before another method. Use the SVD route when the data fit in memory, and the covariance route when $d$ is small and $n$ is huge, since $C$ can be accumulated in one pass. Use [linear discriminant analysis](/linear-discriminant-analysis/) when you have class labels and want directions that separate the classes; PCA ignores labels, and the direction of largest variance can carry no class information. Use [independent component analysis](/independent-component-analysis/) when you want statistically independent sources instead of uncorrelated ones. Use [t-SNE](/t-sne/) or [UMAP](/umap/) when the goal is a 2D picture of clusters and not a linear map. To choose $k$, see [explained variance](/explained-variance/) and the [scree plot](/scree-plot/).

## Pitfalls

- **No centering.** If line L2 is left out, line L3 computes the second moment matrix $\hat\Sigma + \bar x \bar x^T$, and the first "component" points toward the mean of the data. Center with the training mean, and use the same mean for new points.
- **Mixed units.** For the covariance $\begin{pmatrix} 5 & 3 \\ 3 & 2 \end{pmatrix}$ the first direction is $(0.851, 0.526)$. Multiply the second feature by 10 (meters to decimeters) and the covariance becomes $\begin{pmatrix} 5 & 30 \\ 30 & 200 \end{pmatrix}$, with first direction $(0.149, 0.989)$. On the correlation matrix of any two features, the directions are always $(1, \pm 1)/\sqrt 2$. Decide on the scale before line L3.
- **Forming the covariance in floating point.** Line L3 squares the singular values, so the relative accuracy of the small eigenvalues is lost when $\sigma_j / \sigma_1$ is near the square root of the machine epsilon. Use the SVD of $X_c$ when the small components matter.
- **Signs and ties.** Line L4 returns each eigenvector up to sign, and different libraries return different signs. Fix a sign rule before comparing runs. With repeated eigenvalues, individual components are not defined; compare subspaces, not vectors.
- **Variance is not importance.** A feature with large variance and no meaning (a noisy sensor) dominates the first component.

## Implementations

## History

Karl Pearson (1901) asked for the line and the plane that fit a set of points best, in the sense of the least sum of squared perpendicular distances, and found that they pass through the centroid along the major axes of the ellipsoid of the data. Harold Hotelling (1933) derived the components again as directions of maximum variance for the analysis of psychological test scores, and gave them their name. Eckart and Young (1936) proved that the truncated singular value decomposition is the best low-rank approximation in the least squares sense. The same expansion appears for random processes as the Karhunen-Loève expansion and in fluid mechanics as the proper orthogonal decomposition. Jolliffe's book is the standard reference for the statistics of PCA.

## References
