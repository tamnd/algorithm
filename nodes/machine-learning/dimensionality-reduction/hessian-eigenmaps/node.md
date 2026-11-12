---
tag: MMQJ8B
kind: algorithm
slug: hessian-eigenmaps
name: Hessian eigenmaps
aliases:
- Hessian LLE
- HLLE
area: machine-learning/dimensionality-reduction
level: advanced
summary: "Estimate the Hessian of functions in local tangent coordinates and take the null space of the summed squared Hessian. It recovers isometric coordinates without convexity."
model: real-ram
complexity:
  vars: {n: the number of points, d: the input dimension, k: the number of neighbors, m: the output dimension}
  time: {worst: "O(n^2 d + n k^2 d + n k^3 + n k^2 m^4 + n^3)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2003
  people: [David L. Donoho, Carrie Grimes]
  note: Donoho and Grimes published Hessian eigenmaps in PNAS in 2003 to recover the parameters of manifolds that are locally isometric to a region of Euclidean space that need not be convex.
prereqs: [locally-linear-embedding, principal-component-analysis, gram-schmidt-process]
see_also: [local-tangent-space-alignment, isomap, laplacian-eigenmaps, semidefinite-embedding, symmetric-eigenproblem, manifold-hypothesis, intrinsic-dimension]
sources:
  - paper: doi:10.1073/pnas.1031596100
    title: David L. Donoho and Carrie Grimes, Hessian eigenmaps, locally linear embedding techniques for high-dimensional data, PNAS 100(10), 2003, pages 5591 to 5596
    locator: the functional H(f) as the integral of the squared tangent Hessian, the theorem that its null space holds the constant and the isometric coordinates, the steps of the algorithm, and the Swiss roll with a hole
  - paper: doi:10.1126/science.290.5500.2323
    title: Sam T. Roweis and Lawrence K. Saul, Nonlinear dimensionality reduction by locally linear embedding, Science 290(5500), 2000
    locator: the local framework that Hessian eigenmaps builds on (neighborhoods, a sparse quadratic form, bottom eigenvectors)
  - paper: doi:10.1137/S1064827502419154
    title: Zhenyue Zhang and Hongyuan Zha, Principal manifolds and nonlinear dimensionality reduction via tangent space alignment, SIAM Journal on Scientific Computing 26(1), 2004
    locator: the closely related alignment of local tangent coordinates
---

Hessian eigenmaps, also called Hessian LLE, is a method of [manifold learning](/manifold-learning/) by Donoho and Grimes (2003). It estimates, in each neighborhood, the Hessian (the matrix of second derivatives) of a function on the data, in local tangent coordinates found by PCA. It sums the squared Hessian over all neighborhoods into one quadratic form, and returns a basis of its null space: the functions with zero Hessian, which are the constant and the linear functions of the true coordinates. If the manifold is locally isometric to a connected region of $\mathbb{R}^m$, the result is the isometric coordinates, even when the region is not convex, where [Isomap](/isomap/) fails.

## In plain words

A function that changes at a constant rate along a flat sheet, like the distance east, has no curvature: its second derivatives are zero everywhere on the sheet. If the sheet is bent in space without stretching, the function still has no curvature when measured along the sheet. Hessian eigenmaps looks for exactly these functions. In each small neighborhood it fits a flat coordinate system, and it measures how much a function curves in those coordinates. It then searches for functions that are flat in every neighborhood at once. Up to a shift and a linear change, those are the flat coordinates of the unrolled sheet, and gaps or holes in the sheet do not change that.

## The problem

The input is $n$ points $x_1, \dots, x_n \in \mathbb{R}^d$, a number of neighbors $k$, and an output dimension $m$. The model is that $x_i = \psi(\theta_i)$, where $\Theta \subset \mathbb{R}^m$ is open and connected and $\psi: \Theta \to \mathbb{R}^d$ is a local isometry: it keeps the lengths of curves. For a smooth function $f$ on the manifold $\mathcal{M} = \psi(\Theta)$, let $H_f^{\tan}(x)$ be its Hessian in orthonormal coordinates of the tangent space at $x$, and

$$\mathcal{H}(f) = \int_{\mathcal{M}} \|H_f^{\tan}(x)\|_F^2 \, dx .$$

Donoho and Grimes prove that $\mathcal{H}$ has a null space of dimension $m + 1$, spanned by the constant function and the $m$ coordinate functions $\theta_1, \dots, \theta_m$ (as functions of $x$). The task is to estimate $\mathcal{H}$ from the sample and find its null space.

## The algorithm

```pseudo id=main
HESSIAN-EIGENMAPS(x_1..x_n, k, m)
L1  for each i do                                ▷ N_i: the point x_i and its k nearest neighbors
L2      X ← the (k+1) × d matrix of the points of N_i, centered at their mean
L3      U ← the top m left singular vectors of X   ▷ tangent coordinates by local PCA
L4      A ← the columns [1, U_1, …, U_m, U_a U_b for 1 ≤ a ≤ b ≤ m]   ▷ entrywise products
L5      Q ← the Gram-Schmidt orthonormalization of the columns of A; H_i ← the last m(m+1)/2 columns of Q, transposed
L6      H[N_i, N_i] ← H[N_i, N_i] + H_iᵀ H_i
L7  v_1, …, v_{m+1} ← the eigenvectors of H for the m + 1 smallest eigenvalues; discard the constant v_1
L8  Y ← [v_2, …, v_{m+1}], followed by a linear normalization of the coordinates
L9  return Y
```

Line L4 needs $k + 1 \ge 1 + m + m(m+1)/2$, so that the columns are independent. For $m = 2$ this is $k \ge 5$.

Lines L4 and L5 build a local Hessian estimator. A function $f$ on $N_i$ is a vector in $\mathbb{R}^{k+1}$. Its least squares fit by a quadratic in the tangent coordinates is $c + \sum_a g_a u_a + \sum_{a \le b} h_{ab} u_a u_b$, and the coefficients $h_{ab}$ estimate the Hessian. After Gram-Schmidt, the last $m(m+1)/2$ columns of $Q$ are orthogonal to the constant and the linear columns, so $H_i f$ is zero for every affine function of the tangent coordinates and measures the quadratic part for the others. Line L6 adds the local squared norms $\|H_i f\|^2$ into one $n \times n$ matrix with $f^\top H f = \sum_i \|H_i f_{N_i}\|^2$, an estimate of $\mathcal{H}(f)$.

Line L8 fixes the linear freedom in the null space. The null space contains the true coordinates only up to an invertible linear map, and Donoho and Grimes add a final step that picks a basis in which the coordinates are isometric. The implementation returns the orthonormal basis of the null space, scaled by $\sqrt n$, without that step, so its output equals the true coordinates up to an affine map.

## Example

Take the points $0, 1, 2, 3, 4$ on a line, $k = 2$ and $m = 1$. The neighborhood of point 2 is $\{1, 2, 3\}$, with tangent coordinates $u = (-1, 0, 1)$ after centering (up to sign). The columns of line L4 are $\mathbf{1} = (1, 1, 1)$, $u = (-1, 0, 1)$ and $u^2 = (1, 0, 1)$. Gram-Schmidt gives $(1,1,1)/\sqrt3$, then $(-1,0,1)/\sqrt2$, and then

$$u^2 - \tfrac23\mathbf{1} = \left(\tfrac13, -\tfrac23, \tfrac13\right), \quad \text{normalized to } H_i = \frac{1}{\sqrt6}(1, -2, 1).$$

So the local Hessian estimator is the second difference $f_1 - 2f_2 + f_3$, scaled by $1/\sqrt6$. The points 0 and 1 both have the neighborhood $\{0, 1, 2\}$, and the points 3 and 4 both have $\{2, 3, 4\}$, each with the same estimator. Summing,

$$6H = \begin{pmatrix} 2 & -4 & 2 & 0 & 0 \\ -4 & 9 & -6 & 1 & 0 \\ 2 & -6 & 8 & -6 & 2 \\ 0 & 1 & -6 & 9 & -4 \\ 0 & 0 & 2 & -4 & 2 \end{pmatrix}.$$

The constant $(1,1,1,1,1)$ and the coordinate $(0,1,2,3,4)$ have every second difference equal to 0, so both are in the null space. The other eigenvalues of $H$ are $0.176, 1.667, 3.157$. After the constant is discarded, the output is $\pm(-1.414, -0.707, 0, 0.707, 1.414)$.

A larger case shows the point of the method. Take 40 points on a jittered grid with spacing 0.5 on the L-shaped region $[0, 3]^2$ without $(1.5, 3]^2$, which is not convex, and place it in a tilted plane in $\mathbb{R}^3$. With $k = 8$, Hessian eigenmaps returns coordinates from which a linear fit recovers the true $(u, v)$ with a relative residual of about $10^{-14}$. Isomap with the same graph has a residual of about 0.05, because its geodesics around the inner corner are longer than the straight distances in the plane of the L.

## Correctness

The continuous result is the theorem of Donoho and Grimes: for a local isometry from an open connected $\Theta \subset \mathbb{R}^m$, the null space of $\mathcal{H}$ is spanned by the constant and the coordinate functions. The discrete facts proved in the proofs section below are these.

- **Affine functions are in the null space.** If the tangent coordinates in each neighborhood are an affine image of the true coordinates (true on a flat sheet, and close to true on a curved one when the neighborhoods are small), then every affine function of the true coordinates satisfies $Hf = 0$.
- **The estimator measures the quadratic part.** For a quadratic $f$ in the tangent coordinates, $H_i f$ depends only on its second-order coefficients.
- **The embedding is the null space.** $H$ is positive semidefinite. If its null space has dimension $m + 1$, lines L7 and L8 return a basis of the true coordinates, up to an affine map.

The convexity of $\Theta$ plays no role: the argument is local, and connectivity is needed only so that a function with zero Hessian on each neighborhood is affine on the whole region.

## Complexity

- **Neighbors.** $O(n^2 d)$ by brute force.
- **Local PCA.** $O(k^2 d + k^3)$ per point for the $(k+1) \times d$ matrix.
- **Local Hessian estimators.** Line L4 has $p = 1 + m + m(m+1)/2$ columns, which is $O(m^2)$. Gram-Schmidt costs $O(k p^2) = O(k m^4)$, and line L6 costs $O(k^2 m^2)$ per point.
- **Eigenvectors.** $H$ is sparse, with $O(nk^2)$ nonzero entries, so a sparse solver finds the bottom $m + 1$ eigenvectors cheaply. The implementation uses a dense Jacobi solver, $O(n^3)$ per sweep.
- **Memory.** $O(nk^2)$ with sparse storage, $O(n^2)$ in the implementation.

The number of columns grows as $m^2/2$, and the neighborhoods must be at least that large. This makes the method expensive and less stable for $m$ above a few.

## Properties

- **Isometric, not only affine.** With the final normalization, the output is the true coordinates up to a rigid motion, while [LLE](/locally-linear-embedding/) gives an affine image.
- **No convexity needed.** The parameter region only has to be open and connected. Holes and concave boundaries are allowed.
- **Local and sparse.** Like LLE, each point interacts only with its neighbors.
- **Sensitive to noise and to small neighborhoods.** Second derivatives are harder to estimate than first derivatives, so the local estimator needs more neighbors than LLE and is more sensitive to noise.

## Variants and improvements

- **Local tangent space alignment.** [LTSA](/local-tangent-space-alignment/) uses the same tangent coordinates but asks that the global coordinates be an affine image of them in each neighborhood. It needs fewer neighbors, because it fits only the first-order part.
- **Weighted neighborhoods.** Weighting the points in the least squares fit, or choosing the neighborhood size per point, makes the estimator more robust where the sampling is uneven.
- **Out-of-sample points.** A new point can be given the coordinates of the local affine fit of its neighbors' coordinates in its tangent coordinates.

## When to use it

Use Hessian eigenmaps when the data lie on a manifold that is close to isometric to a flat region with holes or a non-convex boundary, the sample is dense and clean, and the dimension $m$ is small, say 1 to 3. For noisy data or larger $m$, [LTSA](/local-tangent-space-alignment/) is usually more stable at a lower cost. For convex regions, [Isomap](/isomap/) gives a similar answer with a simpler method.

## Pitfalls

- **Too few neighbors.** With $k + 1 < 1 + m + m(m+1)/2$, the columns of line L4 are dependent and the estimator is undefined. In practice $k$ should be well above this bound.
- **A wrong $m$.** If $m$ is set too small, the tangent coordinates miss a direction of the manifold, and the second derivatives along it are not measured.
- **Eigenvalues close to 0.** Small eigenvalues that are not exactly 0 make the bottom eigenvectors hard to separate. Check the gap between the $(m+1)$-st and the $(m+2)$-nd smallest eigenvalues.
- **Skipping the normalization.** Without the final step of line L8, the output is only an affine image of the true coordinates and should not be read as distances.

## Implementations

## History

Donoho and Grimes published Hessian eigenmaps in PNAS in 2003. They analyzed when LLE and Isomap recover the true parameters of a manifold, found that Isomap needs the parameter region to be convex, and built a method from the null space of a Hessian functional that needs only local isometry and connectivity. Their examples included a Swiss roll with a rectangular hole, on which Isomap distorts the embedding and Hessian eigenmaps does not. Zhang and Zha's local tangent space alignment appeared in the following year on the same local principle.

## References
