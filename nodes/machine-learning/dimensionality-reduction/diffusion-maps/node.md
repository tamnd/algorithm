---
tag: T8KPAP
kind: algorithm
slug: diffusion-maps
name: Diffusion maps
aliases:
- diffusion map
area: machine-learning/dimensionality-reduction
level: advanced
summary: "Turn a kernel into a random walk P = D⁻¹K and map each point to the eigenvectors of P scaled by λᵗ, so that Euclidean distance equals diffusion distance at time t."
model: real-ram
complexity:
  vars: {n: the number of points, d: the input dimension, m: the output dimension}
  time: {worst: "O(n^2 d + n^3)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2006
  people: [Ronald R. Coifman, Stéphane Lafon]
  note: Coifman and Lafon published diffusion maps in Applied and Computational Harmonic Analysis in 2006, after a 2005 PNAS paper with Lee, Maggioni, Nadler, Warner and Zucker.
prereqs: [laplacian-eigenmaps, markov-chain, stationary-distribution]
see_also: [spectral-clustering, kernel-pca, laplacian-matrix, heat-equation, isomap, power-iteration, symmetric-eigenproblem, manifold-learning]
sources:
  - paper: doi:10.1016/j.acha.2006.04.006
    title: Ronald R. Coifman and Stéphane Lafon, Diffusion maps, Applied and Computational Harmonic Analysis 21(1), 2006, pages 5 to 30
    locator: the Markov chain p(x, y) = k(x, y)/d(x), the diffusion distance and its expression by the eigenvectors, the diffusion map Ψ_t, the truncation by the eigenvalue decay, and the α family of normalizations with the limits α = 0, 1/2 and 1
  - paper: doi:10.1073/pnas.0500334102
    title: R. R. Coifman, S. Lafon, A. B. Lee, M. Maggioni, B. Nadler, F. Warner and S. W. Zucker, Geometric diffusions as a tool for harmonic analysis and structure definition of data, diffusion maps, PNAS 102(21), 2005
    locator: the first presentation of diffusion maps and diffusion distances
  - paper: "Boaz Nadler, Stéphane Lafon, Ronald R. Coifman and Ioannis G. Kevrekidis, Diffusion maps, spectral clustering and reaction coordinates of dynamical systems, Applied and Computational Harmonic Analysis 21(1), 2006"
    locator: the links with spectral clustering and with the Fokker-Planck operator
---

Diffusion maps is a method of [manifold learning](/manifold-learning/) by Coifman and Lafon (2006). It turns a similarity kernel on the data into a random walk, whose step from a point goes most likely to its close neighbors. The coordinates of a point are the eigenvectors of the walk matrix at that point, each multiplied by its eigenvalue to the power $t$. In these coordinates, the Euclidean distance between two points equals their diffusion distance: the difference between the distributions of a walk of $t$ steps started at each of them. A normalization parameter $\alpha$ controls the effect of the sampling density, and $\alpha = 1$ removes it.

## In plain words

Drop a drop of ink at one data point and let it spread, but only to close neighbors at each step. After a few steps the ink covers a small region around the start point. Two points are close in the diffusion sense if ink dropped at one and ink dropped at the other spread to the same places. This distance is robust: two points joined by many paths through the data are close, and a single stray link does not make them close. Diffusion maps finds coordinates in which this ink distance is the ordinary straight-line distance. The number of steps sets the scale: more steps blur small details and keep the large shapes.

## The problem

The input is $n$ points $x_1, \dots, x_n \in \mathbb{R}^d$, a kernel width $\varepsilon$, a normalization $\alpha \in [0, 1]$, a time $t \ge 1$ and an output dimension $m$. From the kernel, build a [Markov chain](/markov-chain/) with transition matrix $P$ and [stationary distribution](/stationary-distribution/) $\pi$. Let $p_t(x, \cdot)$ be row $x$ of $P^t$. The diffusion distance at time $t$ is

$$D_t(x, y)^2 = \sum_z \frac{\big(p_t(x, z) - p_t(y, z)\big)^2}{\pi(z)} .$$

The goal is a map $\Psi_t$ into $\mathbb{R}^m$ with $\|\Psi_t(x) - \Psi_t(y)\| \approx D_t(x, y)$, and with equality when $m = n - 1$.

## The algorithm

```pseudo id=main
DIFFUSION-MAP(x_1..x_n, ε, α, t, m)
L1  K_ij ← exp(−‖x_i − x_j‖² / ε)
L2  q_i ← Σ_j K_ij;  K_ij ← K_ij / (q_i^α q_j^α)          ▷ α = 1 removes the density
L3  d_i ← Σ_j K_ij;  P ← D⁻¹ K;  π_i ← d_i / Σ_j d_j     ▷ a random walk with stationary π
L4  find P ψ_l = λ_l ψ_l with 1 = λ_0 > |λ_1| ≥ … ≥ |λ_{n−1}| and Σ_i π_i ψ_l(i)² = 1
L5  discard λ_0 = 1 and its constant eigenvector ψ_0
L6  Ψ_t(x_i) ← (λ_1^t ψ_1(i), …, λ_m^t ψ_m(i))
L7  return Ψ_t
```

Line L2 is the $\alpha$ normalization. The kernel sum $q_i$ estimates the sampling density at $x_i$, and dividing by $q_i^\alpha q_j^\alpha$ reduces its effect. Coifman and Lafon show that, as $\varepsilon \to 0$ on a dense sample of a manifold, the generator of the walk tends to the Laplace-Beltrami operator for $\alpha = 1$, independent of the density. For $\alpha = 0$ it is the operator of the normalized graph Laplacian, as in [Laplacian eigenmaps](/laplacian-eigenmaps/), which depends on the density. For $\alpha = 1/2$ it is a Fokker-Planck operator.

Line L4 uses the fact that $P$ is similar to the symmetric matrix $S = D^{-1/2}KD^{-1/2}$. If $Sv = \lambda v$ with $\|v\| = 1$, then $\psi = v/\sqrt\pi$ (entry by entry) solves $P\psi = \lambda\psi$ and has $\sum_i\pi_i\psi(i)^2 = 1$. So the eigenvalues are real and at most 1 in absolute value, and the implementation uses a [symmetric eigensolver](/symmetric-eigenproblem/). For the Gaussian kernel, $S$ is positive semidefinite, so all $\lambda_l \ge 0$.

## Example

Take a graph with three vertices in a path, with self-loops, $K = \begin{pmatrix}1&1&0\\1&1&1\\0&1&1\end{pmatrix}$, and $\alpha = 0$. The degrees are $d = (2, 3, 2)$, so $\pi = (2/7, 3/7, 2/7)$ and

$$P = \begin{pmatrix}1/2&1/2&0\\1/3&1/3&1/3\\0&1/2&1/2\end{pmatrix}.$$

The eigenvectors are the constant with $\lambda_0 = 1$, then $(1, 0, -1)$ with $\lambda_1 = 1/2$, and $(3, -4, 3)$ with $\lambda_2 = -1/6$. Scaled so that $\sum_i\pi_i\psi(i)^2 = 1$, they are $\psi_1 = \sqrt{7/4}\,(1, 0, -1) = (1.323, 0, -1.323)$ and $\psi_2 = (3, -4, 3)/\sqrt{12} = (0.866, -1.155, 0.866)$.

At $t = 1$, the rows of $P$ for the two end vertices differ by $(1/2, 0, -1/2)$, so $D_1(0, 2)^2 = 2 \cdot \frac{1/4}{2/7} = 7/4$. In the map, the two ends differ only in the first coordinate, by $\lambda_1(\psi_1(0) - \psi_1(2)) = \frac12 \cdot 2\sqrt{7/4}$, whose square is $7/4$. For the vertices 0 and 1, the rows differ by $(1/6, 1/6, -1/3)$, so $D_1(0, 1)^2 = \frac{7}{72} + \frac{7}{108} + \frac{7}{18} = \frac{119}{216}$. In the map, the squared distance is $\frac14 \cdot \frac74 + \frac{1}{36} \cdot \frac{49}{12} = \frac{7}{16} + \frac{49}{432} = \frac{119}{216}$, the same.

## Correctness

The proofs are in the proofs section below.

- **The walk.** $P$ has rows that sum to 1, and $\pi$ satisfies $\pi^\top P = \pi^\top$ and the detailed balance $\pi_iP_{ij} = \pi_jP_{ji}$, because the normalized kernel is symmetric.
- **The spectral decomposition.** With $\psi_l$ as in line L4 and $\varphi_l = \pi\psi_l$ (entry by entry), $p_t(x, z) = \sum_l\lambda_l^t\psi_l(x)\varphi_l(z)$.
- **The distance identity.** $D_t(x, y)^2 = \sum_{l \ge 1}\lambda_l^{2t}\big(\psi_l(x) - \psi_l(y)\big)^2 = \|\Psi_t(x) - \Psi_t(y)\|^2$ when all $n - 1$ coordinates are kept. The term $l = 0$ drops out because $\psi_0$ is constant.
- **Truncation.** Keeping only the $m$ coordinates with the largest $|\lambda_l|$ gives $D_t(x, y)^2$ up to an error of at most $|\lambda_{m+1}|^{2t}\big(1/\pi(x) + 1/\pi(y)\big)$, which falls fast in $t$ when $|\lambda_{m+1}|$ is well below 1.

The test suite checks the distance identity exactly, with $P^t$ computed in rational arithmetic, on a five-vertex graph for $\alpha = 0$ and $1$ and $t = 1, 2, 3$.

## Complexity

- **Kernel (lines L1 to L3).** $O(n^2 d)$ for the distances and $O(n^2)$ for the normalizations.
- **Eigenvectors (line L4).** $O(n^3)$ for a dense solver; the implementation uses a Jacobi solver, $O(n^3)$ per sweep. With a truncated kernel, set to 0 beyond a few $\sqrt\varepsilon$, the matrix is sparse, and [Lanczos](/lanczos-algorithm/) finds the top $m + 1$ eigenpairs much faster.
- **The map (line L6).** $O(nm)$.
- **Memory.** $O(n^2)$ for a dense kernel.

Changing $t$ only rescales the coordinates, so the whole family $\Psi_t$ costs one eigendecomposition.

## Properties

- **A multiscale distance.** Small $t$ keeps fine detail. Large $t$ damps all coordinates with small $|\lambda_l|$ and keeps only the slow, large-scale structure, such as clusters.
- **Robust to noise and to short cuts.** The diffusion distance averages over all paths of $t$ steps, so one spurious edge changes it little, unlike the shortest path distance of [Isomap](/isomap/).
- **Density control.** $\alpha = 0$ gives the normalized graph Laplacian, $\alpha = 1/2$ a Fokker-Planck operator, and $\alpha = 1$ the Laplace-Beltrami operator, which depends only on the geometry.
- **Links.** For $\alpha = 0$, the eigenvectors $\psi_l$ are those of Laplacian eigenmaps up to one common scale factor, because $P\psi = \lambda\psi$ is $L\psi = (1 - \lambda)D\psi$ with $L = D - K$. Large $t$ gives the coordinates used in [spectral clustering](/spectral-clustering/).
- **Not isometric.** The output keeps diffusion distances, not distances along the manifold.

## Variants and improvements

- **Sparse kernels.** Keep only the $k$ nearest neighbors in the kernel, then symmetrize. The matrix is sparse, and the method scales to large $n$.
- **Self-tuning widths.** Use a width $\varepsilon_i$ for each point, from the distance to its $k$-th neighbor, so that dense and sparse regions get similar numbers of neighbors.
- **Out-of-sample points.** The Nyström formula $\psi_l(x) = \frac{1}{\lambda_l}\sum_jp(x, x_j)\psi_l(x_j)$ extends each eigenvector to a new point. Coifman and Lafon also study geometric harmonics for this extension.
- **Vector diffusion maps.** Singer and Wu replace the scalar kernel by a kernel with rotations between tangent spaces, which also describes how vector fields move on the manifold.

## When to use it

Use diffusion maps when the data lie near a manifold or form clusters, and you need an embedding whose distances are robust to noise and short cuts, at a scale that you can choose with $t$. It is widely used for the slow variables of molecular simulations and other dynamical systems. If the sampling density is uneven and you care only about the shape, use $\alpha = 1$. For a two-dimensional picture of many clusters, a neighbor embedding such as [t-SNE](/t-sne/) usually gives a clearer view.

## Pitfalls

- **The kernel width.** With $\varepsilon$ far below the squared nearest neighbor distances, the walk cannot move, and the kernel graph falls apart. With $\varepsilon$ too large, the walk jumps across the whole set, and the geometry is lost. The implementation raises an error if the kernel graph is disconnected.
- **Keeping the constant.** $\psi_0$ is constant with $\lambda_0 = 1$ and carries no information. Discard it.
- **Repeated eigenvectors of one direction.** On an elongated manifold, the next eigenvectors after $\psi_1$ can be functions of $\psi_1$, such as $\cos 2\theta$ after $\cos\theta$. They add no new direction, and the output dimension must then be chosen with care.
- **Forgetting the eigenvalue scaling.** Without the factors $\lambda_l^t$, the distances in the map are not diffusion distances, and $t$ has no effect.
- **Negative eigenvalues.** With a kernel that is not positive semidefinite, such as a graph without self-loops, some $\lambda_l$ are negative, and $\lambda_l^t$ changes sign with $t$. Order the coordinates by $|\lambda_l|$, as the implementation does.

## Implementations

## History

Coifman, Lafon and colleagues introduced diffusion maps and diffusion distances in PNAS in 2005, and Coifman and Lafon gave the full theory in Applied and Computational Harmonic Analysis in 2006, in an issue on diffusion maps and wavelets. Their work joined the graph Laplacian methods of machine learning, such as [Laplacian eigenmaps](/laplacian-eigenmaps/), with harmonic analysis and with the theory of Markov chains, and the $\alpha$ normalization separated the geometry of a manifold from the distribution of the samples on it. In the same issue, Nadler, Lafon, Coifman and Kevrekidis linked diffusion maps with spectral clustering and with the slow coordinates of stochastic dynamical systems.

## References
