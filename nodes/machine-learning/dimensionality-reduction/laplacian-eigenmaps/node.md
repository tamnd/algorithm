---
tag: N1D05V
kind: algorithm
slug: laplacian-eigenmaps
name: Laplacian eigenmaps
aliases:
- Laplacian eigenmap
- spectral embedding
area: machine-learning/dimensionality-reduction
level: core
summary: "Build a neighbor graph with heat kernel weights and embed the points with the solutions of L y = λ D y for the smallest nonzero eigenvalues of the graph Laplacian."
model: real-ram
complexity:
  vars: {n: the number of points, d: the input dimension, k: the number of neighbors, m: the output dimension}
  time: {worst: "O(n^2 d + n^3)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2003
  people: [Mikhail Belkin, Partha Niyogi]
  note: Belkin and Niyogi presented Laplacian eigenmaps at NIPS in 2001 and published the full paper in Neural Computation in 2003, with the link to the Laplace-Beltrami operator.
prereqs: [manifold-learning, laplacian-matrix, generalized-eigenvalue-problem]
see_also: [spectral-clustering, diffusion-maps, locality-preserving-projections, locally-linear-embedding, isomap, heat-equation, rayleigh-quotient, k-nearest-neighbor-graph]
sources:
  - paper: doi:10.1162/089976603321780317
    title: Mikhail Belkin and Partha Niyogi, Laplacian eigenmaps for dimensionality reduction and data representation, Neural Computation 15(6), 2003, pages 1373 to 1396
    locator: the three steps (adjacency graph, heat kernel or simple-minded weights, the eigenproblem L f = λ D f with f_0 left out), the justification by the weighted sum of squared distances, the link to the Laplace-Beltrami operator and the heat kernel, and the connection with LLE
  - paper: "Mikhail Belkin and Partha Niyogi, Laplacian eigenmaps and spectral techniques for embedding and clustering, Advances in Neural Information Processing Systems 14, 2002"
    locator: the conference version of the method
  - paper: "Mikhail Belkin and Partha Niyogi, Convergence of Laplacian eigenmaps, Advances in Neural Information Processing Systems 19, 2007"
    locator: the convergence of the eigenvectors of the graph Laplacian to the eigenfunctions of the Laplace-Beltrami operator for uniform samples
  - book: isbn:9780821803158
    title: Fan R. K. Chung, Spectral Graph Theory, American Mathematical Society, 1997
    locator: Chapter 1 (the normalized Laplacian and its eigenvalues)
---

Laplacian eigenmaps is a method of [manifold learning](/manifold-learning/) by Belkin and Niyogi (2003). It builds a graph that joins each point to its nearest neighbors, gives each edge a weight that decreases with the distance, and maps the points to the solutions of the generalized eigenvalue problem $Ly = \lambda Dy$ of the graph [Laplacian](/laplacian-matrix/) for the smallest nonzero eigenvalues. These solutions are the functions on the graph that vary least across edges, so close points get close coordinates. On a dense sample of a manifold they approximate the eigenfunctions of the Laplace-Beltrami operator.

## In plain words

Join each point to its few nearest points with springs, stronger for closer points. Now look for a way to place all points on a line so that the springs are stretched as little as possible in total. Putting every point at the same place would be cheating, so the method asks for a spread-out answer in which no point is favored. The best placement keeps neighbors together and lets points that are far apart along the graph drift apart. For a second coordinate, it asks for the next best placement that is unrelated to the first. These placements are eigenvectors of a matrix built from the springs.

## The problem

The input is $n$ points $x_1, \dots, x_n \in \mathbb{R}^d$, a neighborhood rule ($k$ nearest neighbors or a radius $\varepsilon$), a kernel width $t$, and an output dimension $m$. With a symmetric weight matrix $W \ge 0$, the degree matrix $D = \operatorname{diag}(\sum_j W_{ij})$ and the Laplacian $L = D - W$, the goal is

$$\min_{Y \in \mathbb{R}^{n \times m}} \sum_{i,j} W_{ij}\|y_i - y_j\|^2 = 2\operatorname{tr}(Y^\top LY) \quad \text{subject to } Y^\top DY = I,\ Y^\top D\mathbf{1} = 0 .$$

The first constraint removes the trivial answer $Y = 0$ and fixes the scale. The second removes the constant vector, which gives a cost of 0. The weight $D_{ii}$ in the constraints gives more importance to points with many close neighbors.

## The algorithm

```pseudo id=main
LAPLACIAN-EIGENMAPS(x_1..x_n, k or ε, t, m)
L1  G ← the graph that joins i and j if one is a k-nearest neighbor of the other (or if ‖x_i − x_j‖ ≤ ε)
L2  W_ij ← exp(−‖x_i − x_j‖² / t) for each edge of G, and 0 otherwise   ▷ or W_ij ← 1 ("simple-minded")
L3  D_ii ← Σ_j W_ij;  L ← D − W
L4  solve L y = λ D y for the m + 1 smallest eigenvalues 0 = λ_0 < λ_1 ≤ … ≤ λ_m, with yᵀ D y = 1
L5  discard y_0 = the constant vector; Y ← [y_1, …, y_m]
L6  return Y
```

Line L4 is a symmetric-definite [generalized eigenvalue problem](/generalized-eigenvalue-problem/). With $z = D^{1/2}y$ it becomes the ordinary problem $Nz = \lambda z$ for the normalized Laplacian $N = D^{-1/2}LD^{-1/2}$, which is how the implementation solves it, with a [Jacobi](/jacobi-eigenvalue-algorithm/) eigensolver. The same $y$ are the right eigenvectors of the random walk matrix $P = D^{-1}W$, with eigenvalue $1 - \lambda$. The graph must be connected: then $\lambda_0 = 0$ is simple and the constant is its only eigenvector.

## Example

Take five points $0, 1, 2, 3, 4$ on a line, the radius $\varepsilon = 1$ and unit weights. The graph is a path, $D = \operatorname{diag}(1, 2, 2, 2, 1)$, and

$$L = \begin{pmatrix} 1 & -1 & 0 & 0 & 0 \\ -1 & 2 & -1 & 0 & 0 \\ 0 & -1 & 2 & -1 & 0 \\ 0 & 0 & -1 & 2 & -1 \\ 0 & 0 & 0 & -1 & 1 \end{pmatrix}.$$

For a path with $n$ vertices, the solutions are $\lambda_k = 1 - \cos\frac{\pi k}{n-1}$ and $y_k[j] \propto \cos\frac{\pi kj}{n-1}$, $j = 0, \dots, n-1$. For an inner vertex, $(Ly)_j = 2y_j - y_{j-1} - y_{j+1} = 2(1 - \cos\theta)y_j$ by the sum formula for cosines, which is $\lambda D_{jj}y_j$; the two end vertices check in the same way. Here $n = 5$: the eigenvalues are $0, 0.293, 1, 1.707, 2$, and the first coordinate is

$$y_1 = \tfrac12(1, 0.707, 0, -0.707, -1),$$

scaled so that $y_1^\top Dy_1 = 1$. The order of the points is kept, but the spacing is not: equally spaced inputs give a cosine profile, with the end points closer together than the middle ones. Laplacian eigenmaps keeps neighborhoods, not distances.

## Correctness

The proofs are in the proofs section below.

- **The cost is the Laplacian form.** $\frac12\sum_{i,j}W_{ij}(f_i - f_j)^2 = f^\top Lf$ for each $f \in \mathbb{R}^n$, so $L$ is positive semidefinite and $L\mathbf{1} = 0$.
- **The constant is the only trivial solution on a connected graph.** If $f^\top Lf = 0$, then $f_i = f_j$ across each edge with a positive weight, so $f$ is constant on each connected component.
- **The eigenvectors solve the problem.** Under $Y^\top DY = I$ and $Y^\top D\mathbf{1} = 0$, the minimum of $\operatorname{tr}(Y^\top LY)$ is $\lambda_1 + \dots + \lambda_m$, attained by the generalized eigenvectors of line L5. This is the [Rayleigh quotient](/rayleigh-quotient/) principle for the pencil $(L, D)$.

Belkin and Niyogi also show that, on a manifold, the analogous continuous problem is solved by the eigenfunctions of the Laplace-Beltrami operator, and that the heat kernel weights make the graph Laplacian an approximation of that operator. Their later work proves that the graph eigenvectors converge to those eigenfunctions as the sample grows and $t$ shrinks at a suitable rate.

## Complexity

- **Graph (lines L1 and L2).** $O(n^2 d)$ by brute force, plus $O(n^2 \log n)$ to sort.
- **Eigenproblem (line L4).** $L$ is sparse with $O(nk)$ nonzero entries. A sparse solver such as [Lanczos](/lanczos-algorithm/) finds the $m + 1$ smallest eigenpairs in about $O(nkm)$ work per iteration. The implementation uses dense matrices and a Jacobi solver, $O(n^3)$ per sweep.
- **Memory.** $O(nk)$ with sparse storage, $O(n^2)$ in the implementation.

The sparse eigenproblem makes Laplacian eigenmaps one of the cheapest spectral methods.

## Properties

- **Local.** Only neighbors enter the cost, so far points are not pushed apart except through the constraints. The method keeps neighborhoods, not distances.
- **Few parameters.** $k$ or $\varepsilon$ and the kernel width $t$. The simple-minded weights $W_{ij} = 1$ remove $t$.
- **A link with clustering.** On a graph with weakly linked clusters, the first coordinates are close to constant on each cluster. This is the basis of [spectral clustering](/spectral-clustering/), which runs k-means on the same coordinates.
- **A link with LLE.** Belkin and Niyogi show that, under some conditions, the matrix of [LLE](/locally-linear-embedding/) approximates the square of the Laplacian, so LLE finds approximately the same eigenvectors.
- **Not isometric.** The output scale is set by $Y^\top DY = I$, and equal spacing on the manifold is not kept, as in the example.

## Variants and improvements

- **Locality preserving projections.** [LPP](/locality-preserving-projections/) restricts $y$ to linear functions of the input, $y_i = a^\top x_i$, which gives a projection for new points.
- **Diffusion maps.** [Diffusion maps](/diffusion-maps/) use the same random walk $P = D^{-1}W$, normalize the kernel to remove the effect of the sampling density, and scale the coordinates by powers of the eigenvalues, so that distances in the embedding equal diffusion distances.
- **Unnormalized and symmetric forms.** Using $Lz = \lambda z$ (without $D$) or the eigenvectors $z$ of $N$ (without the change $y = D^{-1/2}z$) gives related embeddings, which are also common in spectral clustering.
- **Out-of-sample points.** A Nyström formula, $y(x) = \frac{1}{1 - \lambda}\sum_j \frac{W(x, x_j)}{\sum_l W(x, x_l)}y_j$, extends each coordinate to a new point $x$ from the random walk form $Py = (1 - \lambda)y$.

## When to use it

Use Laplacian eigenmaps when you need a fast, sparse embedding that keeps neighborhoods, for example as features for clustering or for semi-supervised learning on a graph. It works well when the data form a few smooth pieces and the exact distances do not matter. For an embedding that keeps distances, use [Isomap](/isomap/) or [LTSA](/local-tangent-space-alignment/). For a picture with clear clusters, [t-SNE](/t-sne/) or UMAP is usually better.

## Pitfalls

- **A disconnected graph.** Each component adds an eigenvalue 0, and the first coordinates then only label the components. The implementation raises an error. Embed each component separately, or increase $k$ or $\varepsilon$.
- **A bad kernel width.** With $t$ far below the squared edge lengths, the weights are close to 0, and the graph is almost disconnected. With $t$ far above them, all weights are close to 1, and the heat kernel is no better than the simple-minded weights.
- **Keeping the constant.** The smallest solution $y_0$ is constant and carries no information. Discard it.
- **Reading distances.** The coordinates keep the order of neighborhoods but stretch and compress the distances, so they should not be used as distances on the manifold.
- **Repeated eigenvalues.** On symmetric data, such as a square grid, two eigenvalues can be equal, and the matching coordinates are then defined only up to a rotation between them.

## Implementations

## History

Belkin and Niyogi presented Laplacian eigenmaps at NIPS in 2001 and published the full paper in Neural Computation in 2003. The graph Laplacian was already a central tool in spectral graph theory and in spectral partitioning. Their contribution was to use its eigenvectors as coordinates for data on a manifold and to connect the graph Laplacian with heat kernel weights to the Laplace-Beltrami operator. The paper also linked the method to LLE and to spectral clustering, and their later work proved the convergence of the graph eigenvectors to the manifold eigenfunctions.

## References
