---
tag: V5B4MS
kind: algorithm
slug: kernel-pca
name: Kernel PCA
aliases:
- kernel principal component analysis
- KPCA
- nonlinear PCA with kernels
area: machine-learning/dimensionality-reduction
level: advanced
summary: "Do PCA in the feature space of a kernel using only the n x n Gram matrix: center it, find its top eigenvectors, scale them, and project points with kernel values."
model: real-ram
complexity:
  vars: {n: the number of points, d: the input dimension, k: the number of components}
  time: {worst: "O(n^2 d + n^3)", per_step: "O(n d + n k)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: true, iterative: false, online: false, recursive: false}
history:
  year: 1998
  people: [Bernhard Schölkopf, Alexander Smola, Klaus-Robert Müller]
  note: "Schölkopf, Smola and Müller applied the kernel trick, known from support vector machines, to PCA, giving nonlinear components from an eigenproblem of the size of the data set."
prereqs: [principal-component-analysis, kernel-trick]
see_also: [mercer-theorem, representer-theorem, classical-mds, isomap, spectral-clustering, kernel-k-means, kernel-ridge-regression, support-vector-machine]
sources:
  - paper: doi:10.1162/089976698300017467
    title: Bernhard Schölkopf, Alexander Smola and Klaus-Robert Müller, Nonlinear component analysis as a kernel eigenvalue problem, Neural Computation 10(5), 1299-1319, 1998
    locator: Section 2 (the eigenproblem n lambda alpha = K alpha, the normalization lambda_k (alpha^k . alpha^k) = 1 and the projection of a test point) and Appendix A (centering in feature space)
  - paper: "Sebastian Mika, Bernhard Schölkopf, Alex Smola, Klaus-Robert Müller, Matthias Scholz and Gunnar Rätsch, Kernel PCA and de-noising in feature spaces, Advances in Neural Information Processing Systems 11, 536-542, 1999"
    title: Mika et al. 1999
    locator: the pre-image problem and the fixed-point iteration for the Gaussian kernel, with de-noising experiments
  - paper: doi:10.1109/TNN.2004.837781
    title: James T. Kwok and Ivor W. Tsang, The pre-image problem in kernel methods, IEEE Transactions on Neural Networks 15(6), 1517-1525, 2004
    locator: a non-iterative pre-image from distances in feature space, by multidimensional scaling
  - book: isbn:9780262194754
    title: Bernhard Schölkopf and Alexander J. Smola, Learning with Kernels, MIT Press, 2002
    locator: Chapter 14 (kernel feature extraction, kernel PCA) and Chapter 18 (pre-images)
---

Kernel PCA is [principal component analysis](/principal-component-analysis/) in the feature space of a kernel. A kernel $k(a, b) = \langle \Phi(a), \Phi(b) \rangle$ computes inner products after a nonlinear map $\Phi$, which can have a huge or infinite dimension. Schölkopf, Smola and Müller (1998) showed that PCA in that space needs only the $n \times n$ Gram matrix $K_{ij} = k(x_i, x_j)$: center it with $K' = K - \mathbf{1}_n K - K \mathbf{1}_n + \mathbf{1}_n K \mathbf{1}_n$, find its top eigenvectors $\alpha$, scale each one so that $\lambda \|\alpha\|^2 = 1$, and compute the component scores of any point from its kernel values with the training points. With the linear kernel it is ordinary PCA. With a nonlinear kernel the components are nonlinear functions of the input, which can reveal curved structure.

## In plain words

Ordinary PCA finds straight directions. If the data lie on a curve or on two rings around the same center, no straight direction describes them well.

The idea is to lift each point into a much larger space of features, such as all products of coordinates, where the curved structure becomes straight, and do PCA there. The lifted space can be too large to write down. But PCA needs only the inner products between points, and a kernel function gives the inner product of two lifted points directly from the original points. This is the [kernel trick](/kernel-trick/). So the method builds the table of kernel values between all pairs of points, adjusts it so that the lifted points have mean zero, and finds the main directions of this table.

## The problem

**Input.** Points $x_1, \ldots, x_n$ in a set $\mathcal{X}$ (often $\mathbb{R}^d$), a positive semidefinite kernel $k$, and a number of components $k_c$.

**Output.** For $j = 1, \ldots, k_c$, the eigenvalues $\lambda_j$ of the centered Gram matrix $K'$ (the feature-space variances are $\lambda_j / n$), coefficient vectors $\alpha^j \in \mathbb{R}^n$ with $\lambda_j \|\alpha^j\|^2 = 1$, and a map that gives the score of any point $t$ on component $j$. The feature-space principal direction is $V^j = \sum_i \alpha^j_i (\Phi(x_i) - \bar\Phi)$, a unit vector, where $\bar\Phi$ is the mean of the $\Phi(x_i)$.

## The algorithm

Write $\mathbf{1}_n$ for the $n \times n$ matrix whose entries are all $1/n$.

```pseudo id=main
KERNEL-PCA(x_1..x_n, k, k_c)
L1  K ← [k(x_i, x_j)]                               ▷ n × n Gram matrix
L2  K' ← K − 1_n K − K 1_n + 1_n K 1_n                ▷ centering in feature space
L3  (λ_j, v_j) ← eigenpairs of K', λ_1 ≥ λ_2 ≥ …
L4  for j ← 1 to k_c with λ_j > 0 do
L5      α^j ← v_j / √λ_j                             ▷ so that λ_j ‖α^j‖² = 1 and ‖V^j‖ = 1
    PROJECT(t)
L6  κ_i ← k(x_i, t) for i = 1..n
L7  κ̃_i ← κ_i − mean(κ) − mean of row i of K + mean of K
L8  return (Σ_i α^j_i κ̃_i) for j = 1..k_c
```

**Why it works.** An eigenvector $V$ of the feature covariance $\bar C = \frac1n \sum_i \tilde\Phi_i \tilde\Phi_i^T$ with a nonzero eigenvalue lies in the span of the centered features $\tilde\Phi_i = \Phi(x_i) - \bar\Phi$, so $V = \sum_i \alpha_i \tilde\Phi_i$. Substituting into $\bar C V = \lambda_{\bar C} V$ gives the $n \times n$ eigenproblem $K'\alpha = n\lambda_{\bar C}\, \alpha$. The squared norm of $V$ is $\alpha^T K' \alpha = \lambda \|\alpha\|^2$ with $\lambda = n\lambda_{\bar C}$ the eigenvalue of $K'$, which explains the scaling in L5. The score of a point $t$ is $\langle V, \Phi(t) - \bar\Phi\rangle = \sum_i \alpha_i \langle \tilde\Phi_i, \Phi(t) - \bar\Phi\rangle$, and L7 expands these inner products into kernel values. For a training point the score is $(K'\alpha)_j = \lambda \alpha_j$.

The implementation computes the eigenpairs in L3 with the cyclic Jacobi method.

## Example

**Linear kernel.** Take the eight points of the [PCA](/principal-component-analysis/) page and $k(a, b) = a^T b$. The centered points are $(9, 6, 3), (5, 10, 1), \ldots$, and $K'$ is their Gram matrix; its first row is $(126, 108, 54, 36, -36, -54, -108, -126)$, and every row sums to zero. The eigenvalues of $K'$ are $648, 288, 72$, which divided by $n = 8$ are the covariance eigenvalues $81, 36, 9$ of ordinary PCA. The first coefficient vector is $\alpha^1 = \pm(1, 1, 1, 1, -1, -1, -1, -1)/72$, and indeed $648 \cdot 8 / 72^2 = 1$. The training scores $648\, \alpha^1_j = \pm 9$ are the PCA scores, and the scores on the other components are $\pm 6$ and $\pm 3$. The new point $(5, 7, 8) = \mu + (1, 2, 2)$ gets the score $3$ on the first component and $0$ on the others, as $(1, 2, 2) \cdot (1, 2, 2)/3 = 3$.

**Two rings.** Put eight points on the circle of radius 1 and eight on the circle of radius 3 (turned by 0.2 radians), all around the origin. Linear PCA finds two equal eigenvalues and mixes the rings: no straight direction separates them. With the Gaussian kernel $k(a, b) = \exp(-0.5\|a - b\|^2)$, the first kernel component has the eigenvalue $2.1717$ and gives the score $+0.368$ to every point of the inner ring and $-0.368$ to every point of the outer ring (up to sign). One nonlinear component separates the rings completely.

**De-noising.** Forty points on the unit circle with Gaussian noise of standard deviation $0.15$ have the mean distance $0.112$ from the circle. Project them on the first four components of the Gaussian kernel with $\gamma = 0.5$ and map the projections back with the pre-image iteration below. The mean distance falls to $0.051$.

## Correctness

The proofs file shows: the centering formula of L2 and L7 gives the inner products of the centered features; every eigenvector of $K'$ with a positive eigenvalue $\lambda$ gives an eigenvector of the feature covariance with eigenvalue $\lambda / n$, and every such eigenvector arises this way; the scaling $\lambda\|\alpha\|^2 = 1$ makes $V$ a unit vector; different eigenvalues give orthogonal $V$; and the projection of L6 to L8 is the inner product with $V$. With the linear kernel this reduces to ordinary PCA, by the identity between the nonzero eigenvalues of $X_c X_c^T$ and $X_c^T X_c$. So kernel PCA has all the optimality properties of PCA, in feature space: the first $k_c$ components give the subspace of feature space with the largest variance and the smallest squared [reconstruction error](/reconstruction-error/) among all $k_c$-dimensional subspaces.

**The pre-image problem.** A point in feature space, such as the projection $P\Phi(t) = \bar\Phi + \sum_j \beta_j V^j$ with $\beta_j$ the scores of $t$, is in general not the image $\Phi(z)$ of any input $z$. To get a result in the input space, for example a de-noised point, one looks for $z$ that minimizes $\|\Phi(z) - P\Phi(t)\|^2$. Mika et al. (1999) wrote $P\Phi(t) = \sum_i \gamma_i \Phi(x_i)$, with $\gamma_i = \sum_j \beta_j \alpha^j_i + \frac1n (1 - \sum_l \sum_j \beta_j \alpha^j_l)$, and showed that for the Gaussian kernel a stationary point satisfies

$$z = \frac{\sum_i \gamma_i\, k(z, x_i)\, x_i}{\sum_i \gamma_i\, k(z, x_i)},$$

which they use as a fixed-point iteration. It can converge to a local optimum and is sensitive to the start; starting at $t$ is common. Kwok and Tsang (2004) give a non-iterative method based on distances.

## Complexity

In the real RAM, with a kernel that costs $O(d)$ per evaluation: L1 costs $O(n^2 d)$, L2 costs $O(n^2)$, and the full eigendecomposition in L3 costs $O(n^3)$. The memory is $O(n^2)$ for the Gram matrix. Projecting a new point costs $O(n d)$ for the kernel values and $O(n k_c)$ for the scores. Unlike linear PCA, whose cost grows with the dimension $d$ of the covariance matrix, kernel PCA grows with the number of points, so it is limited to some tens of thousands of points without approximations. Only the top $k_c$ eigenpairs are needed, so [Lanczos](/lanczos-algorithm/) or [randomized](/randomized-pca/) methods reduce L3 to about $O(n^2 k_c)$.

## Properties

- **Exact PCA in feature space.** No approximation is made, apart from the eigensolver.
- **Kernel-dependent.** The result depends strongly on the kernel and its parameters, such as the width of the Gaussian kernel.
- **At most $n - 1$ components.** The centered features span a space of dimension at most $n - 1$, even if the feature space is infinite.
- **No explicit inverse map.** The components are functions on the input, but feature-space points have no exact pre-image in general.
- **Unifies spectral methods.** Classical MDS, Isomap, Laplacian eigenmaps and spectral clustering can be written as kernel PCA with special, data-dependent kernels.

## Variants and improvements

- **[Classical MDS](/classical-mds/)** is kernel PCA with the kernel $-\frac12 J D^{(2)} J$ built from squared distances; [Isomap](/isomap/) uses geodesic distances in the same formula.
- **Nyström approximation** (Williams and Seeger 2001) uses $m \ll n$ landmark points to approximate the Gram matrix, with cost $O(n m^2)$.
- **Random features** (Rahimi and Recht 2007) replace the kernel with an explicit low-dimensional random map, after which ordinary PCA applies.
- **Sparse and robust kernel PCA** combine the ideas of [sparse PCA](/sparse-pca/) and [robust PCA](/robust-pca/) with kernels.
- **Kernel Hebbian algorithm** and incremental kernel PCA update the components as points arrive.
- **Learned pre-images** (Bakır, Weston and Schölkopf 2004) fit a regression from feature-space scores back to the input.

## When to use it

Use kernel PCA when the data have nonlinear structure that a known kernel can make linear, when you want nonlinear features for a later classifier, or for de-noising with a pre-image. It works well for up to a few thousand points with exact eigensolvers. Choose the kernel width by cross-validation of the later task, or by a heuristic such as the median distance between points. For very large $n$, use the Nyström method or random features. If you want an embedding of a manifold rather than nonlinear features, methods such as Isomap or [UMAP](/umap/) may be more direct.

## Pitfalls

- **Forgetting to center.** Without L2, the first component points to the feature mean, and the eigenvalues are not variances. New points must be centered with the training means, as in L7, not with their own mean.
- **Wrong normalization.** The eigensolver returns unit vectors $v$; the coefficients must be $v / \sqrt{\lambda}$. With $\alpha = v$ the scores are scaled by $1/\sqrt{\lambda}$ and the components are not unit vectors.
- **Kernel width.** A very narrow Gaussian kernel makes $K$ close to the identity, all eigenvalues nearly equal, and each component describes one point. A very wide kernel is close to $1 - \gamma\|a - b\|^2$, and after centering it gives almost the components of linear PCA. In the two-ring example, $\gamma = 0.1$ and $\gamma = 1$ do not separate the rings on the first component; $\gamma = 0.5$ does.
- **Eigenvalues of $K'$ versus variances.** The eigenvalues of $K'$ are $n$ times the feature-space variances; the [explained variance](/explained-variance/) ratios are the same either way.
- **Pre-images are approximate.** The fixed-point iteration can fail when the denominator is near zero, and the result depends on the start.
- **Cost in $n$.** The $O(n^3)$ eigensolver and $O(n^2)$ memory limit the size of the training set.

## Implementations

## History

Kernels as inner products in feature spaces go back to Aizerman, Braverman and Rozonoer (1964) and were made popular by the support vector machine of Boser, Guyon and Vapnik (1992). Schölkopf, Smola and Müller (1996 technical report, 1998 journal) observed that PCA, too, needs only inner products, and gave kernel PCA with the centering of the Gram matrix and the projection of new points. Mika et al. (1999) posed the pre-image problem and used it for de-noising. Later work showed that many spectral embedding methods are kernel PCA with special kernels (Ham, Lee, Mika and Schölkopf 2004), and scaled the method to large data with the Nyström method and random features.

## References
