---
tag: QVE4K5
kind: algorithm
slug: locally-linear-embedding
name: Locally linear embedding
aliases:
- LLE
area: machine-learning/dimensionality-reduction
level: core
summary: "Write each point as a weighted sum of its neighbors with weights that sum to one, then find low-dimensional points that the same weights reconstruct best."
model: real-ram
complexity:
  vars: {n: the number of points, d: the input dimension, k: the number of neighbors, m: the output dimension}
  time: {worst: "O(n^2 d + n k^2 d + n k^3 + n^3)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2000
  people: [Sam T. Roweis, Lawrence K. Saul]
  note: Roweis and Saul published locally linear embedding in Science in December 2000, in the same issue as Isomap.
prereqs: [manifold-learning, k-nearest-neighbor-graph, symmetric-eigenproblem]
see_also: [isomap, hessian-eigenmaps, local-tangent-space-alignment, laplacian-eigenmaps, least-squares-problem, kernel-pca, manifold-hypothesis, t-sne]
sources:
  - paper: doi:10.1126/science.290.5500.2323
    title: Sam T. Roweis and Lawrence K. Saul, Nonlinear dimensionality reduction by locally linear embedding, Science 290(5500), 2000, pages 2323 to 2326
    locator: the reconstruction cost with the sum-to-one constraint, the embedding cost, and the bottom eigenvectors of M = (I − W)ᵀ(I − W)
  - paper: "Lawrence K. Saul and Sam T. Roweis, Think globally, fit locally: unsupervised learning of low dimensional manifolds, Journal of Machine Learning Research 4, 2003, pages 119 to 155"
    locator: the solution for the weights from the local Gram matrix, the regularization when k is larger than the input dimension, and the complexity of each step
  - paper: doi:10.1073/pnas.1031596100
    title: David L. Donoho and Carrie Grimes, Hessian eigenmaps, locally linear embedding techniques for high-dimensional data, PNAS 100(10), 2003
    locator: the analysis of LLE and its relation to a Laplacian-type operator
  - paper: "Yoshua Bengio, Jean-François Paiement, Pascal Vincent, Olivier Delalleau, Nicolas Le Roux and Marie Ouimet, Out-of-sample extensions for LLE, Isomap, MDS, Eigenmaps, and spectral clustering, Advances in Neural Information Processing Systems 16, 2004"
    locator: the kernel form of LLE and the extension to new points
---

Locally linear embedding (LLE) is a method of [manifold learning](/manifold-learning/) by Roweis and Saul (2000). It describes each point by the weights that best reconstruct it as a linear combination of its nearest neighbors, with the weights summing to one, and then finds low-dimensional points that the same weights reconstruct as well as possible. The weights do not change under rotation, scaling and translation, so they capture the local geometry of a manifold that is close to flat in each neighborhood. Both steps are closed-form: a small linear system per point and one sparse eigenvalue problem.

## In plain words

Look at each point and its few closest points. If the data lie on a smooth surface, a small piece of it is almost flat, so the point is almost an average of its neighbors with some weights, like a point on a line between two others. LLE first finds these weights for every point. It then looks for new points in two dimensions, one for each original point, such that each new point is again the same weighted average of its neighbors' new points. Because the weights only describe the local shape, the new points keep each neighborhood but are free to unroll the surface as a whole.

## The problem

The input is $n$ points $x_1, \dots, x_n \in \mathbb{R}^d$, a number of neighbors $k$, and an output dimension $m$. The model is that the points lie on or near a smooth manifold of dimension $m$. LLE minimizes two costs in turn. The reconstruction cost is

$$\varepsilon(W) = \sum_i \Big\| x_i - \sum_{j \in N(i)} w_{ij} x_j \Big\|^2, \quad \text{with } \sum_j w_{ij} = 1 \text{ and } w_{ij} = 0 \text{ for } j \notin N(i),$$

where $N(i)$ is the set of the $k$ nearest neighbors of $x_i$. With $W$ fixed, the embedding cost is

$$\Phi(Y) = \sum_i \Big\| y_i - \sum_j w_{ij} y_j \Big\|^2 = \operatorname{tr}(Y^\top M Y), \qquad M = (I - W)^\top (I - W),$$

over $Y \in \mathbb{R}^{n \times m}$ with the constraints $\sum_i y_i = 0$ and $\frac1n Y^\top Y = I$. The constraints remove the trivial solution $Y = 0$ and the freedom of translation, rotation and scale.

## The algorithm

```pseudo id=main
LLE(x_1..x_n, k, m, reg)
L1  N(i) ← the k nearest neighbors of x_i, for each i
L2  for each i do
L3      C_st ← (x_s − x_i)ᵀ (x_t − x_i) for s, t ∈ N(i)          ▷ the local Gram matrix
L4      C ← C + reg · tr(C) · I                                 ▷ needed when k > d or the neighbors are affinely dependent
L5      w_i ← the solution of min wᵀ C w subject to 1ᵀ w = 1
L6  M ← (I − W)ᵀ (I − W)
L7  v_1, …, v_{m+1} ← the eigenvectors of M for the m + 1 smallest eigenvalues; discard v_1 = 1/√n
L8  Y ← √n [v_2, …, v_{m+1}]
L9  return Y
```

Line L5 is a least squares problem with one linear constraint. Since $\sum_j w_{ij} = 1$, the reconstruction error of point $i$ is $\|\sum_j w_{ij}(x_i - x_j)\|^2 = w_i^\top C w_i$. If $C$ is invertible, the solution is $w_i = C^{-1}\mathbf{1} / (\mathbf{1}^\top C^{-1}\mathbf{1})$: solve $C w = \mathbf{1}$ and divide by the sum. The implementation solves the equivalent bordered system $\begin{pmatrix} C & \mathbf{1} \\ \mathbf{1}^\top & 0 \end{pmatrix}\begin{pmatrix} w \\ \mu \end{pmatrix} = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$, which also has a unique solution when $C$ is singular but the neighbors are affinely independent.

Line L7 discards the constant vector. Each row of $W$ sums to 1, so $(I - W)\mathbf{1} = 0$ and $M\mathbf{1} = 0$: the constant is always an eigenvector with eigenvalue 0. It would put all points at one place. When $M$ has more than one zero eigenvalue, an eigensolver can return any basis of the null space, so the implementation moves the constant out of the way by adding $c\,\mathbf{1}\mathbf{1}^\top/n$ with $c$ above all eigenvalues, and then takes the $m$ smallest eigenvectors.

## Example

Take the five points $0, 1, 2, 3, 4$ on a line, with $k = 2$. The middle points $1, 2, 3$ have one neighbor on each side, and the weights are $\frac12, \frac12$: each is the midpoint of its neighbors. The end point $0$ has the neighbors $1$ and $2$, and the weights solve $w_1 + w_2 = 1$, $w_1 \cdot 1 + w_2 \cdot 2 = 0$, so $w_1 = 2$, $w_2 = -1$: the point is an extrapolation. The end point $4$ gets $w_3 = 2$, $w_2 = -1$ in the same way. All reconstructions are exact.

The matrix $M = (I - W)^\top (I - W)$ is

$$M = \begin{pmatrix} 5/4 & -5/2 & 5/4 & 0 & 0 \\ -5/2 & 21/4 & -3 & 1/4 & 0 \\ 5/4 & -3 & 7/2 & -3 & 5/4 \\ 0 & 1/4 & -3 & 21/4 & -5/2 \\ 0 & 0 & 5/4 & -5/2 & 5/4 \end{pmatrix},$$

with each row summing to 0. Its eigenvalues are $0, 0, 0.315, 6.25, 9.936$. The null space holds the constant vector and the coordinate vector $(0, 1, 2, 3, 4)$, because both are reconstructed exactly by the weights. After the constant is discarded, line L8 returns $\pm(-1.414, -0.707, 0, 0.707, 1.414)$: the centered coordinates, scaled so that their mean square is 1. LLE recovers a line up to an affine map, not up to a rigid motion.

## Correctness

The proofs are in the proofs section below. The main facts are these.

- **The weights.** Line L5 gives the unique minimizer of the reconstruction error of point $i$ when the regularized $C$ is positive definite on the vectors with zero sum. The weights do not change if all points are rotated, scaled by the same factor or translated.
- **The embedding.** $M$ is symmetric and positive semidefinite, and $\Phi(Y) = \operatorname{tr}(Y^\top M Y)$. Under the constraints, the minimum of $\Phi$ is the sum of the $m$ smallest eigenvalues of $M$ on the vectors orthogonal to $\mathbf{1}$, attained by line L8. This is the Ky Fan form of the [Courant-Fischer theorem](/courant-fischer-theorem/).
- **Flat data.** If each point is reconstructed exactly by its neighbors and the points are an affine image of $z_i \in \mathbb{R}^m$, then every coordinate of $z$ is in the null space of $M$. If the null space is exactly the span of $\mathbf{1}$ and these coordinates, LLE returns an affine image of the $z_i$.

LLE does not, in general, recover an isometric parametrization: it recovers the null space only up to an affine map, and with $\frac1n Y^\top Y = I$ it whitens the result. [Hessian eigenmaps](/hessian-eigenmaps/) and [local tangent space alignment](/local-tangent-space-alignment/) were designed to fix this.

## Complexity

- **Neighbors (line L1).** $O(n^2 d)$ by brute force, which is what the implementation does.
- **Weights (lines L2 to L5).** $O(k^2 d)$ to build each Gram matrix and $O(k^3)$ to solve each system, so $O(n k^2 d + n k^3)$ in total.
- **Embedding (lines L6 to L8).** $M$ has $O(nk^2)$ nonzero entries. A sparse eigensolver such as [Lanczos](/lanczos-algorithm/) finds the bottom eigenvectors in about $O(m n k^2)$ per iteration. The implementation forms $M$ densely and uses a Jacobi solver, which costs $O(n^3)$ per sweep.
- **Memory.** $O(nk)$ for $W$ and $O(nk^2)$ for a sparse $M$. The implementation uses $O(n^2)$.

The sparse eigenproblem makes LLE cheaper than [Isomap](/isomap/), which needs a dense matrix of all graph distances.

## Properties

- **Local.** Only the neighborhoods enter $W$. Points that are far apart are not forced to stay far apart, and the layout at large scale can fold.
- **Affine, not isometric.** Any affine image of the true coordinates has the same reconstruction cost. LLE fixes the remaining freedom with the whitening constraint, so the output can be stretched compared with the true shape.
- **Sensitive to $k$ and to the regularization.** The regularizer in line L4 changes the weights, and the result can change with its value. Too small $k$ disconnects the graph; too large $k$ joins points across folds.
- **No explicit map.** Like most spectral methods, LLE embeds the given points only.

## Variants and improvements

- **Out-of-sample points.** Compute the weights of a new point $x$ with respect to its neighbors in the training set, and set $y = \sum_j w_j y_j$. Bengio et al. (2004) derive the same formula from a kernel view.
- **Hessian LLE and LTSA.** [Hessian eigenmaps](/hessian-eigenmaps/) replaces the reconstruction weights by an estimate of the Hessian in local tangent coordinates, and [local tangent space alignment](/local-tangent-space-alignment/) aligns local PCA coordinates. Both recover isometric coordinates where LLE does not.
- **Modified LLE.** Zhang and Wang use several weight vectors per point, from the small singular directions of the local Gram matrix, to make the weights better conditioned when $k > m$.
- **Supervised and linear forms.** Neighborhood preserving embedding is a linear approximation of LLE, in the same way as [locality preserving projections](/locality-preserving-projections/) is for [Laplacian eigenmaps](/laplacian-eigenmaps/).

## When to use it

Use LLE when the data lie on a smooth manifold that is well sampled and you want a fast, sparse method with a closed-form solution. It suits images or signals with a few degrees of freedom. For a result that keeps distances, prefer [Hessian eigenmaps](/hessian-eigenmaps/), [local tangent space alignment](/local-tangent-space-alignment/) or [Isomap](/isomap/). For noisy data or a visual map of clusters, [t-SNE](/t-sne/) or UMAP is usually a better choice.

## Pitfalls

- **Forgetting the regularizer.** When $k > d$, the local Gram matrix $C$ is singular, and the plain solve of $Cw = \mathbf{1}$ fails or gives huge weights. Add the regularizer of line L4.
- **Keeping the constant eigenvector.** The smallest eigenvector of $M$ is the constant. Keeping it maps all points to one value. With a degenerate null space, discard it by projection, not by position in the sorted list.
- **Near-zero eigenvalues from a disconnected graph.** Each connected component of the neighbor graph adds an eigenvalue near 0, and the embedding then separates the components and loses the shape inside them. Check the graph, or increase $k$.
- **Duplicate points.** A duplicate makes a column of $C$ zero and the weights undefined. Remove duplicates first.
- **Judging the result by its scale.** The whitening constraint sets the scale of each output axis to 1. The output size says nothing about the size of the manifold.

## Implementations

## History

Roweis and Saul published LLE in Science in December 2000, in the same issue as [Isomap](/isomap/). It was one of the two papers that started the field of spectral manifold learning. Saul and Roweis (2003) gave a longer account with the regularization, the choice of $k$ and the complexity. Donoho and Grimes (2003) and Zhang and Zha (2004) then built Hessian eigenmaps and LTSA on the same local framework.

## References
