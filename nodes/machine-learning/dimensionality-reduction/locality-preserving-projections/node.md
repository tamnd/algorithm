---
tag: 3ZFNH0
kind: algorithm
slug: locality-preserving-projections
name: Locality preserving projections
aliases:
- LPP
area: machine-learning/dimensionality-reduction
level: advanced
summary: "A linear form of Laplacian eigenmaps: find the projection directions a that solve X L Xᵀ a = λ X D Xᵀ a, so neighbors stay close and new points have a map."
model: real-ram
complexity:
  vars: {n: the number of points, d: the input dimension, k: the number of neighbors, m: the output dimension}
  time: {worst: "O(n^2 d + n d^2 + d^3)"}
  space: {extra: "O(n^2 + d^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2003
  people: [Xiaofei He, Partha Niyogi]
  note: He and Niyogi presented locality preserving projections at NIPS in 2003 as a linear approximation of Laplacian eigenmaps.
prereqs: [laplacian-eigenmaps, principal-component-analysis, generalized-eigenvalue-problem]
see_also: [linear-discriminant-analysis, cholesky-decomposition, courant-fischer-theorem, local-tangent-space-alignment, spectral-clustering, kernel-pca, laplacian-matrix]
sources:
  - paper: "Xiaofei He and Partha Niyogi, Locality preserving projections, Advances in Neural Information Processing Systems 16, 2004, pages 153 to 160"
    locator: the three steps (adjacency graph, heat kernel or simple-minded weights, the eigenproblem X L Xᵀ a = λ X D Xᵀ a), the justification as a linear approximation of Laplacian eigenmaps, and the kernel form
  - paper: "Xiaofei He, Shuicheng Yan, Yuxiao Hu, Partha Niyogi and Hong-Jiang Zhang, Face recognition using Laplacianfaces, IEEE Transactions on Pattern Analysis and Machine Intelligence 27(3), 2005, pages 328 to 340"
    locator: the PCA step before LPP when X D Xᵀ is singular, and the links of LPP with PCA and LDA
  - paper: doi:10.1162/089976603321780317
    title: Mikhail Belkin and Partha Niyogi, Laplacian eigenmaps for dimensionality reduction and data representation, Neural Computation 15(6), 2003
    locator: the graph Laplacian problem L y = λ D y that LPP restricts to linear functions
---

Locality preserving projections (LPP) is a linear method of dimensionality reduction by He and Niyogi (2003). It has the same goal as [Laplacian eigenmaps](/laplacian-eigenmaps/): points that are neighbors in a graph should get close coordinates. But it only allows coordinates that are linear functions of the input, $y_i = a^\top x_i$. The directions $a$ are the solutions of a $d \times d$ [generalized eigenvalue problem](/generalized-eigenvalue-problem/). The result is a projection matrix, like that of [PCA](/principal-component-analysis/), so a new point is mapped by one matrix product.

## In plain words

Laplacian eigenmaps places each point freely so that neighbors stay close. That works for the points you have, but it gives no rule for a new point. LPP asks a narrower question: among all ways of looking at the data from one direction, which view keeps neighbors closest together? The answer is a direction, and a direction can be used for any point, old or new. PCA looks for the view where the points are most spread out. LPP looks for the view where the neighbors are least spread out, relative to the spread of all the points. The two views can be very different, as the example shows.

## The problem

The input is $n$ points $x_1, \dots, x_n \in \mathbb{R}^d$, the rows of $X \in \mathbb{R}^{n \times d}$, a neighborhood rule, a kernel width $t$, and an output dimension $m$. With the weight matrix $W$, the degree matrix $D$ and the Laplacian $L = D - W$ of the neighbor graph, the cost of a direction $a \in \mathbb{R}^d$ is

$$\frac12\sum_{i,j}W_{ij}\big(a^\top x_i - a^\top x_j\big)^2 = a^\top X^\top LXa ,$$

and the goal is to minimize it subject to $a^\top X^\top DXa = 1$. For $m$ directions, the columns of $A = [a_0, \dots, a_{m-1}]$ satisfy $A^\top X^\top DXA = I$, and the cost is $\operatorname{tr}(A^\top X^\top LXA)$. He and Niyogi write the points as columns, which gives the same problem in the form $XLX^\top a = \lambda XDX^\top a$.

## The algorithm

```pseudo id=main
LPP(x_1..x_n, k or ε, t, m)
L1  G ← the graph that joins i and j if one is a k-nearest neighbor of the other (or if ‖x_i − x_j‖ ≤ ε)
L2  W_ij ← exp(−‖x_i − x_j‖² / t) for each edge of G, and 0 otherwise   ▷ or W_ij ← 1
L3  D_ii ← Σ_j W_ij;  L ← D − W
L4  P ← Xᵀ L X;  Q ← Xᵀ D X                     ▷ d × d matrices
L5  solve P a = λ Q a for the m smallest eigenvalues λ_0 ≤ … ≤ λ_{m−1}, with aᵀ Q a = 1
L6  A ← [a_0, …, a_{m−1}]
L7  return A                                     ▷ a point x, new or old, maps to y = Aᵀ x
```

Lines L1 to L3 are the same as in Laplacian eigenmaps. Line L5 needs $Q$ to be positive definite, which holds when $X$ has full column rank and every point has a neighbor. The implementation factors $Q = RR^\top$ with [Cholesky](/cholesky-decomposition/), finds the eigenpairs of the symmetric matrix $R^{-1}PR^{-\top}$ with a Jacobi solver, and maps each eigenvector $z$ back to $a = R^{-\top}z$. When $Q$ is singular, as for images with more pixels than samples, the Laplacianfaces paper first projects the data onto its leading principal components.

## Example

Take six points in two rows: $(0, 0.75), (1, 0.75), (2, 0.75)$ and $(0, -0.75), (1, -0.75), (2, -0.75)$. With the radius $\varepsilon = 1$ and unit weights, the graph joins the neighbors in each row, and no edge crosses between the rows, which are $1.5$ apart. The degrees are $1, 2, 1$ in each row.

A direction $a = (a_1, a_2)$ changes by $a_1$ along each of the four edges, so $P = \operatorname{diag}(4, 0)$. The degree weighted sums give $Q = \operatorname{diag}(12, 4.5)$. The solutions are:

- $\lambda_0 = 0$ with $a_0 = (0, 1/\sqrt{4.5}) = (0, 0.471)$. The projections are $+0.354$ for the top row and $-0.354$ for the bottom row.
- $\lambda_1 = 4/12 = 1/3$ with $a_1 = (1/\sqrt{12}, 0) = (0.289, 0)$.

PCA picks the horizontal direction, because the variance along it ($2/3$) is larger than the vertical variance ($0.5625$), and that view mixes the two rows. LPP picks the vertical direction, which is constant on each row and so separates them. A new point $(10, 0.75)$ maps to $0.354$, the value of the top row.

## Correctness

The proofs are in the proofs section below.

- **The cost is a quadratic form.** $\frac12\sum_{i,j}W_{ij}(a^\top x_i - a^\top x_j)^2 = a^\top Pa$ with $P = X^\top LX$ positive semidefinite, and $a^\top Qa = \sum_i D_{ii}(a^\top x_i)^2$.
- **The eigenvectors solve the problem.** If $Q$ is positive definite, then over $A$ with $A^\top QA = I$, the minimum of $\operatorname{tr}(A^\top PA)$ is $\lambda_0 + \dots + \lambda_{m-1}$, attained by line L6.
- **The link with Laplacian eigenmaps.** LPP is Laplacian eigenmaps restricted to the linear functions $f = Xa$. With $X = I_n$ (one feature per point), $P = L$ and $Q = D$, and LPP solves exactly $Ly = \lambda Dy$. In general, by the [Courant-Fischer theorem](/courant-fischer-theorem/), the $l$-th LPP eigenvalue is at least the $l$-th eigenvalue of $Ly = \lambda Dy$.

## Complexity

- **Graph (lines L1 and L2).** $O(n^2 d)$ by brute force.
- **The matrices (line L4).** $LX$ costs $O(nkd)$ with a sparse $L$, and $X^\top(LX)$ and $X^\top DX$ cost $O(nd^2)$.
- **The eigenproblem (line L5).** $O(d^3)$ for the Cholesky factor and the symmetric eigenproblem, independent of $n$.
- **Mapping a new point.** $O(dm)$, a matrix product.
- **Memory.** $O(nk + d^2)$ with sparse storage. The implementation stores $W$ densely, $O(n^2 + d^2)$.

When $n$ is much larger than $d$, LPP is much cheaper than Laplacian eigenmaps, whose eigenproblem has size $n$.

## Properties

- **Linear.** The output is a projection matrix, so LPP gives a map for new points and can be used as a preprocessing step, as PCA is.
- **Local.** Only the graph edges enter the cost, so LPP keeps neighborhoods, while PCA keeps the global variance.
- **Supervised use.** If the graph joins points of the same class, LPP tends to find directions that keep each class together. The Laplacianfaces paper shows that, with suitable weights within each class, LPP gives the directions of [linear discriminant analysis](/linear-discriminant-analysis/).
- **Not centered.** The constraint $a^\top X^\top DXa = 1$ uses the raw coordinates. Implementations often center the data first, which changes $Q$ but not $P$.

## Variants and improvements

- **Kernel LPP.** He and Niyogi also give a kernel form, which replaces $x$ by a feature map $\phi(x)$ through the [kernel trick](/kernel-trick/). With a kernel matrix of full rank this reduces to Laplacian eigenmaps on the training points.
- **PCA first.** Projecting onto the leading principal components before LPP makes $Q$ invertible and removes noise directions.
- **Orthogonal LPP.** Asking for orthonormal directions $a$, instead of $Q$-orthonormal ones, gives an orthogonal projection, so the output can be mapped back to the input space by $A$.
- **Neighborhood preserving embedding.** The same restriction to linear functions applied to [LLE](/locally-linear-embedding/) gives a linear form of LLE, and a linear form of [LTSA](/local-tangent-space-alignment/) exists in the same way.

## When to use it

Use LPP when you need a fast linear map that keeps neighborhoods and applies to new data, for example as features before a nearest-neighbor classifier, as in face recognition. It is most useful when the data have more samples than dimensions, or after a PCA step. If you only need coordinates for a fixed data set, use [Laplacian eigenmaps](/laplacian-eigenmaps/). If the manifold is strongly curved, no linear projection can unfold it.

## Pitfalls

- **A singular $Q$.** With $d > n$ or with linearly dependent features, $Q$ is singular, and the generalized eigenproblem has no unique answer. The implementation raises an error; reduce the dimension first.
- **Trivial directions.** If the points lie in an affine hyperplane that does not pass through the origin, some direction $a$ gives the same value $a^\top x_i$ for all points, with $\lambda = 0$. That direction carries no information. Center the data, or discard it.
- **A bad kernel width.** As in Laplacian eigenmaps, $t$ far below the squared edge lengths makes the weights almost 0, and $t$ far above them makes the heat kernel no better than unit weights.
- **Smallest, not largest.** LPP keeps the smallest eigenvalues of $Pa = \lambda Qa$. Taking the largest gives the directions that separate neighbors most.

## Implementations

## History

He and Niyogi presented locality preserving projections at NIPS in 2003, two years after Laplacian eigenmaps, to give a linear map that also works on new points. In 2005, He, Yan, Hu, Niyogi and Zhang applied it to face recognition under the name Laplacianfaces, with a PCA step before LPP, and related it to the eigenfaces of PCA and the Fisherfaces of LDA. LPP started a family of linear graph-based methods, which includes linear forms of LLE and LTSA.

## References
