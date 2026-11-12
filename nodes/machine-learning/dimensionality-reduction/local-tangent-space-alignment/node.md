---
tag: 8CGP5G
kind: algorithm
slug: local-tangent-space-alignment
name: Local tangent space alignment
aliases:
- LTSA
area: machine-learning/dimensionality-reduction
level: advanced
summary: "Find local PCA tangent coordinates in each neighborhood, then find global coordinates that are an affine image of each local set, from the bottom eigenvectors of an alignment matrix."
model: real-ram
complexity:
  vars: {n: the number of points, d: the input dimension, k: the number of neighbors, m: the output dimension}
  time: {worst: "O(n^2 d + n k^2 d + n k^3 + n^3)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2004
  people: [Zhenyue Zhang, Hongyuan Zha]
  note: Zhang and Zha published local tangent space alignment in the SIAM Journal on Scientific Computing in 2004, after a technical report in 2002.
prereqs: [locally-linear-embedding, principal-component-analysis]
see_also: [hessian-eigenmaps, isomap, laplacian-eigenmaps, singular-value-decomposition, symmetric-eigenproblem, manifold-hypothesis, intrinsic-dimension]
sources:
  - paper: doi:10.1137/S1064827502419154
    title: Zhenyue Zhang and Hongyuan Zha, Principal manifolds and nonlinear dimensionality reduction via tangent space alignment, SIAM Journal on Scientific Computing 26(1), 2004, pages 313 to 338
    locator: the local tangent coordinates by local PCA, the alignment error, the matrix B = S W Wᵀ Sᵀ with W_i = I − G_i G_iᵀ, the 2nd to (d+1)-st eigenvectors, and the error analysis
  - paper: doi:10.1073/pnas.1031596100
    title: David L. Donoho and Carrie Grimes, Hessian eigenmaps, locally linear embedding techniques for high-dimensional data, PNAS 100(10), 2003
    locator: the related null space method with local tangent coordinates
  - paper: doi:10.1126/science.290.5500.2323
    title: Sam T. Roweis and Lawrence K. Saul, Nonlinear dimensionality reduction by locally linear embedding, Science 290(5500), 2000
    locator: the local framework with neighborhoods, a sparse quadratic form and the bottom eigenvectors
---

Local tangent space alignment (LTSA) is a method of [manifold learning](/manifold-learning/) by Zhang and Zha (2004). In each neighborhood it finds local coordinates on the tangent space by [principal component analysis](/principal-component-analysis/). It then looks for one set of global coordinates such that, in each neighborhood, the global coordinates are an affine image of the local ones, with the smallest total error. This alignment problem is solved by the bottom eigenvectors of a sparse symmetric matrix, after the constant vector is discarded.

## In plain words

Think of a large map made by pasting together many small photos taken from above, each with its own position and angle. Each photo is accurate on its own, but the photos do not agree on where north is or where the origin is. LTSA has one such "photo" per point: the flat coordinates of its neighbors found by PCA. It looks for one big map in which every small photo fits after a shift, a turn and a stretch. Because every point is in several photos, the photos overlap and pin down the big map. The best fit comes from an eigenvalue problem.

## The problem

The input is $n$ points $x_1, \dots, x_n \in \mathbb{R}^d$, a number of neighbors $k$, and an output dimension $m$. For each $i$, let $N_i$ be the point $x_i$ and its $k$ nearest neighbors, $s = k + 1$ points, and let $\Theta_i \in \mathbb{R}^{m \times s}$ be their local tangent coordinates. The unknowns are the global coordinates $T = [\tau_1, \dots, \tau_n] \in \mathbb{R}^{m \times n}$ and, for each $i$, an affine map. With $T_i$ the columns of $T$ in $N_i$ and $J_s = I - \frac1s\mathbf{1}\mathbf{1}^\top$, the alignment error is

$$\sum_i \min_{L_i} \big\| T_i J_s - L_i\Theta_i \big\|_F^2,$$

minimized over $T$ with $TT^\top = I$, which fixes the scale and removes the trivial solution.

## The algorithm

```pseudo id=main
LTSA(x_1..x_n, k, m)
L1  for each i do                                ▷ N_i: the point x_i and its k nearest neighbors, s = k + 1
L2      X ← the s × d matrix of the points of N_i, centered at their mean
L3      G_i ← [1/√s · 1, g_1, …, g_m], with g_1..g_m the top m left singular vectors of X
L4      W_i ← I − G_i G_iᵀ
L5      B[N_i, N_i] ← B[N_i, N_i] + W_i
L6  v_1, …, v_{m+1} ← the eigenvectors of B for the m + 1 smallest eigenvalues; discard the constant v_1
L7  T ← [v_2, …, v_{m+1}]ᵀ
L8  return T
```

Lines L2 and L3 are local PCA: the singular vectors $g_1, \dots, g_m$ hold the tangent coordinates of the $s$ points, scaled to unit length, and the column $\mathbf{1}/\sqrt s$ accounts for the translation. Since $\mathbf{1}$ is orthogonal to the centered columns, $G_i$ has orthonormal columns, and $W_i$ is the orthogonal projection onto the complement of their span. A vector $f$ on $N_i$ has $W_i f = 0$ exactly when $f$ is an affine function of the local tangent coordinates.

Line L5 assembles $B = \sum_i S_i W_i S_i^\top$, where $S_i$ selects the rows of $N_i$. Zhang and Zha write $B = SWW^\top S^\top$; since $W_i$ is a projection, $W_iW_i^\top = W_i$, and the two forms agree. The error of a global coordinate vector $f$ is $f^\top Bf = \sum_i \|W_i f_{N_i}\|^2$, and the alignment error of $T$ is $\operatorname{tr}(TBT^\top)$.

## Example

Take the points $0, 1, 2, 3, 4$ on a line in $\mathbb{R}^2$, with $k = 2$ and $m = 1$. The neighborhood of point 2 is $\{1, 2, 3\}$, with the centered tangent coordinates $(-1, 0, 1)$, so $g_1 = (-1, 0, 1)/\sqrt2$ and $G_i = [(1,1,1)/\sqrt3,\ (-1,0,1)/\sqrt2]$. The complement of these two columns in $\mathbb{R}^3$ is spanned by $(1, -2, 1)/\sqrt6$, so

$$W_i = \frac16\begin{pmatrix} 1 & -2 & 1 \\ -2 & 4 & -2 \\ 1 & -2 & 1 \end{pmatrix}.$$

The points 0 and 1 both have the neighborhood $\{0, 1, 2\}$, and the points 3 and 4 both have $\{2, 3, 4\}$, so

$$6B = \begin{pmatrix} 2 & -4 & 2 & 0 & 0 \\ -4 & 9 & -6 & 1 & 0 \\ 2 & -6 & 8 & -6 & 2 \\ 0 & 1 & -6 & 9 & -4 \\ 0 & 0 & 2 & -4 & 2 \end{pmatrix}.$$

The null space holds the constant and $(0, 1, 2, 3, 4)$, and the other eigenvalues of $B$ are $0.176, 1.667, 3.157$. The output, a unit vector orthogonal to the constant, is $\pm(-2, -1, 0, 1, 2)/\sqrt{10} = \pm(-0.632, -0.316, 0, 0.316, 0.632)$. For neighborhoods of three points on a curve, this $B$ is the same as the matrix of [Hessian eigenmaps](/hessian-eigenmaps/): with $s = m + 2$, both methods keep the one direction that is not affine.

On 40 points of a jittered grid on the non-convex L-shaped region $[0, 3]^2$ without $(1.5, 3]^2$, placed in a tilted plane in $\mathbb{R}^3$, LTSA with $k = 6$ gives two zero eigenvalues and then $0.062$, and a linear fit from its output recovers the true coordinates with a relative residual of about $10^{-13}$. When the same sheet is rolled onto a cylinder of radius 2, the residual is about $0.005$.

## Correctness

The proofs are in the proofs section below.

- **The local fit.** For fixed $T$, the best affine map in neighborhood $i$ leaves the error $\|T_i W_i\|_F^2$, so the alignment error equals $\operatorname{tr}(TBT^\top)$.
- **The global minimum.** $B$ is symmetric positive semidefinite with $B\mathbf{1} = 0$. Over $T$ with $TT^\top = I$ and rows orthogonal to $\mathbf{1}$, the minimum of $\operatorname{tr}(TBT^\top)$ is the sum of the $m$ smallest eigenvalues of $B$ on $\mathbf{1}^\perp$, attained by line L7.
- **Exact recovery on flat data.** If, in each neighborhood, the tangent coordinates are an affine image of the true coordinates, then each true coordinate is in the null space of $B$. If the null space has dimension $m + 1$, the output spans the centered true coordinates, so it is an affine image of them.

## Complexity

- **Neighbors.** $O(n^2 d)$ by brute force.
- **Local PCA.** $O(k^2 d + k^3)$ per point for the singular vectors of an $s \times d$ matrix, through the $s \times s$ Gram matrix.
- **Assembly.** $O(k^2 m)$ per point for $W_i$.
- **Eigenvectors.** $B$ has $O(nk^2)$ nonzero entries, so a sparse solver is cheap. The implementation forms $B$ densely and uses a Jacobi solver, $O(n^3)$ per sweep.
- **Memory.** $O(nk^2)$ with sparse storage, $O(n^2)$ in the implementation.

LTSA needs only $k \ge m$ neighbors for the local PCA, fewer than the $m + m(m+1)/2$ of [Hessian eigenmaps](/hessian-eigenmaps/), and its local step costs less.

## Properties

- **Local and sparse.** Each point interacts only with the points of the neighborhoods it is in.
- **Affine recovery.** The output is the true coordinates up to an affine map, then normalized to orthonormal rows. Distances in the output are therefore not the distances on the manifold.
- **No convexity needed.** Only overlaps between neighborhoods are used, so holes and concave boundaries are allowed.
- **A first-order method.** LTSA fits the first-order (affine) part of each neighborhood, so it is more stable than Hessian eigenmaps when the neighborhoods are small or noisy.

## Variants and improvements

- **Linear LTSA.** Restricting the global coordinates to a linear projection of the data gives a map for new points, in the same way as [locality preserving projections](/locality-preserving-projections/) does for [Laplacian eigenmaps](/laplacian-eigenmaps/).
- **Adaptive neighborhoods.** Choosing $k$ per point from the local curvature or from the size of the trailing singular values helps where the sampling is uneven.
- **Out-of-sample points.** Find the tangent coordinates of a new point in the neighborhood of its nearest neighbors, and apply the affine map that best aligns those coordinates with the neighbors' global coordinates.
- **Reconstruction.** Zhang and Zha also use the local affine maps in reverse to reconstruct points on the manifold from the global coordinates, which gives an estimate of a principal manifold.

## When to use it

Use LTSA when the data lie on a smooth manifold of known dimension that is close to flat in each neighborhood, possibly with holes, and you need a global parametrization. It is a good default among the local spectral methods, as it is cheaper and more stable than [Hessian eigenmaps](/hessian-eigenmaps/) and less distorted than [LLE](/locally-linear-embedding/) on uneven samples. For a picture of clusters, a neighbor embedding such as [t-SNE](/t-sne/) is a better fit.

## Pitfalls

- **A wrong $m$.** The local PCA keeps $m$ directions. If $m$ is too small, a direction of the manifold is treated as noise; if it is too large, noise is treated as a direction of the manifold.
- **Neighborhoods that cross folds.** As with every graph method, a $k$ that is too large joins points on different layers of the manifold, and the alignment then glues them together.
- **Keeping the constant eigenvector.** $B\mathbf{1} = 0$ always. With a degenerate null space, discard the constant by projection, not by its position in the sorted list.
- **Reading the scale.** The constraint $TT^\top = I$ sets the length of each output axis to 1, so the output scale says nothing about the size of the manifold.

## Implementations

## History

Zhang and Zha circulated LTSA as a technical report in 2002 and published it in the SIAM Journal on Scientific Computing in 2004, with an error analysis of the alignment step. It combined local PCA with the eigenvector solution of [LLE](/locally-linear-embedding/), and gave a first-order counterpart to the Hessian eigenmaps of Donoho and Grimes. LTSA became one of the standard local methods and is part of common software libraries for manifold learning.

## References
