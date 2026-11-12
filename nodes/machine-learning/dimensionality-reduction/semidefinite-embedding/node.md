---
tag: 6YS5CD
kind: algorithm
slug: semidefinite-embedding
name: Semidefinite embedding
aliases:
- maximum variance unfolding
- MVU
area: machine-learning/dimensionality-reduction
level: advanced
summary: "Find the centered Gram matrix of largest trace that keeps all distances between neighbors, a semidefinite program, then embed with its top eigenvectors as in classical MDS."
model: real-ram
complexity:
  vars: {n: the number of points, d: the input dimension, k: the number of neighbors, s: the number of solver steps}
  time: {worst: "O(n^2 d + s n^3)"}
  space: {extra: "O(n^2 + n k^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2004
  people: [Kilian Q. Weinberger, Lawrence K. Saul]
  note: Weinberger and Saul introduced semidefinite embedding in 2004, at CVPR and, with Sha, at ICML, and later called it maximum variance unfolding.
prereqs: [classical-mds, semidefinite-programming, k-nearest-neighbor-graph, manifold-learning]
see_also: [isomap, kernel-pca, augmented-lagrangian-method, projected-gradient-descent, jacobi-eigenvalue-algorithm, locally-linear-embedding, laplacian-eigenmaps, t-sne]
sources:
  - paper: "Kilian Q. Weinberger and Lawrence K. Saul, Unsupervised learning of image manifolds by semidefinite programming, Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2004, volume 2, pages 988 to 995"
    locator: the constraints on neighbors and on pairs of points with a common neighbor, the centering constraint, the objective trace(K), the SDP and the eigenvector embedding
  - paper: "Kilian Q. Weinberger and Lawrence K. Saul, Unsupervised learning of image manifolds by semidefinite programming, International Journal of Computer Vision 70(1), 2006, pages 77 to 90"
    locator: the journal version, with the argument that maximizing the variance unfolds the manifold and the experiments on images
  - paper: "Kilian Q. Weinberger, Fei Sha and Lawrence K. Saul, Learning a kernel matrix for nonlinear dimensionality reduction, Proceedings of the 21st International Conference on Machine Learning (ICML), 2004"
    locator: the view of the SDP solution as a learned kernel matrix for kernel PCA
  - paper: "Jun Sun, Stephen Boyd, Lin Xiao and Persi Diaconis, The fastest mixing Markov process on a graph and a connection to a maximum variance unfolding problem, SIAM Review 48(4), 2006"
    locator: the dual of the maximum variance unfolding problem
---

Semidefinite embedding (SDE), also called maximum variance unfolding (MVU), is a method of [manifold learning](/manifold-learning/) by Weinberger and Saul (2004). It looks for an arrangement of the points that keeps the distance between each pair of neighbors and spreads the points as far apart as possible. The unknown is the Gram matrix $K$ of the output points, and the problem is a [semidefinite program](/semidefinite-programming/): maximize $\operatorname{tr}(K)$ over centered positive semidefinite matrices with linear constraints on the neighbor distances. The output coordinates come from the top eigenvectors of $K$, as in [classical MDS](/classical-mds/).

## In plain words

Imagine the points as beads, and tie each bead to its nearest beads with rigid sticks of the right length. Now pull all beads away from the center as hard as you can. The sticks keep each small group of beads in shape, but the whole chain or sheet straightens out, like a crumpled piece of paper pulled flat by its edges. When nothing can move any further, measure where the beads are. Because the result is flat, a few coordinates are enough to describe it. Finding the most spread-out arrangement is a convex problem, so it has no false local optima.

## The problem

The input is $n$ points $x_1, \dots, x_n \in \mathbb{R}^d$, a number of neighbors $k$, and an output dimension $m$. Let $E$ be the set of pairs $(i, j)$ such that $j$ is one of the $k$ nearest neighbors of $i$, or $i$ and $j$ are both neighbors of a third point. The second kind of pair holds the angles between the neighbors of a point fixed. The problem is

$$\max_{K \in \mathbb{R}^{n \times n}} \operatorname{tr}(K) \quad \text{subject to} \quad K \succeq 0, \quad \sum_{i,j}K_{ij} = 0, \quad K_{ii} + K_{jj} - 2K_{ij} = \|x_i - x_j\|^2 \text{ for } (i, j) \in E .$$

If $K$ is the Gram matrix of output points $y_1, \dots, y_n$, the last constraint says $\|y_i - y_j\| = \|x_i - x_j\|$, the centering constraint says $\sum_iy_i = 0$, and $\operatorname{tr}(K) = \sum_i\|y_i\|^2$ is the variance of the output, up to the factor $n$.

## The algorithm

```pseudo id=main
SEMIDEFINITE-EMBEDDING(x_1..x_n, k, m)
L1  E ← the k-nearest-neighbor pairs, and the pairs of points that are neighbors of a common point
L2  D_ij ← ‖x_i − x_j‖² for each (i, j) ∈ E
L3  K ← argmax tr(K) subject to K ⪰ 0, Σ_ij K_ij = 0, K_ii + K_jj − 2K_ij = D_ij for (i, j) ∈ E
L4  λ_1 ≥ … ≥ λ_m, v_1, …, v_m ← the top m eigenpairs of K
L5  y_i ← (√λ_1 v_1(i), …, √λ_m v_m(i))
L6  return y_1, …, y_n
```

Line L3 is the semidefinite program. Weinberger and Saul solve it with a general interior point SDP solver. The implementation uses a simpler solver, which is not the interior point method of the papers: an [augmented Lagrangian method](/augmented-lagrangian-method/) whose inner steps are [projected gradient](/projected-gradient-descent/) steps. It starts from the centered Gram matrix of the input, which is feasible. Each step moves $K$ along $I - \sum_{c}(\mu_c + \rho g_c)A_c$, where $g_c$ is the error of constraint $c$ and $A_c$ its matrix, and then projects $K$ back onto the centered positive semidefinite matrices. That projection is $JKJ$ with $J = I - \frac1n\mathbf{1}\mathbf{1}^\top$, followed by setting the negative eigenvalues to 0, with a [Jacobi](/jacobi-eigenvalue-algorithm/) eigensolver that starts from the eigenvectors of the step before. After each inner loop, the multipliers are updated by $\mu_c \leftarrow \mu_c + \rho g_c$. The solver is slow and only meant for small inputs, but it solves the same convex problem, and its multipliers give a certificate of optimality.

## Example

Take three points $A = (0, 0)$, $B = (1, 0)$, $C = (1, 1.5)$ and $k = 1$. The nearest neighbor of $A$ is $B$, that of $B$ is $A$, and that of $C$ is $B$, so $E = \{AB, BC\}$: only $|AB| = 1$ and $|BC| = 1.5$ are fixed. No point has two neighbors, so no pair is added.

For centered points, $\operatorname{tr}(K) = \frac1n\sum_{i<j}\|y_i - y_j\|^2 = \frac13\big(1 + 2.25 + |AC|^2\big)$. The input has $|AC|^2 = 3.25$, so its trace is $13/6 \approx 2.167$. By the triangle inequality, $|AC| \le |AB| + |BC| = 2.5$, so the largest trace is $\frac13(1 + 2.25 + 6.25) = 19/6 \approx 3.167$, reached when $A$, $B$ and $C$ lie on a line with $B$ between them. The optimal $K$ has rank 1, and the output is

$$y_A = -7/6, \quad y_B = -1/6, \quad y_C = 4/3 ,$$

the bent path unfolded into a straight segment. The implementation finds this $K$ to within $10^{-5}$.

On eight points of a half circle of radius 1 in $\mathbb{R}^3$, with a little noise and $k = 2$, the solver raises the trace from $5.61$ to $7.94$, puts more than 99 percent of it in the first eigenvalue, and the multipliers give a dual bound that agrees with the trace to within $10^{-5}$.

## Correctness

The proofs are in the proofs section below.

- **The constraints mean what they say.** A centered positive semidefinite $K$ is the Gram matrix of points $y_i$ with $\sum_iy_i = 0$, and then $K_{ii} + K_{jj} - 2K_{ij} = \|y_i - y_j\|^2$ and $\operatorname{tr}(K) = \frac{1}{2n}\sum_{i,j}\|y_i - y_j\|^2$.
- **The input is feasible, so the output spreads at least as much.** The centered Gram matrix of the input satisfies all constraints, so the optimal trace is at least the input variance.
- **The problem has a solution if the graph is connected.** Each $\|y_i - y_j\|$ is at most the length of a path of neighbor edges from $i$ to $j$, so the feasible set is bounded, and it is closed. The maximum exists, and since the problem is convex, every local maximum is global. On a disconnected graph the trace is unbounded.
- **Weak duality gives a certificate.** If $J(\sum_c\mu_cA_c - I)J \succeq 0$, then $\operatorname{tr}(K) \le \sum_c\mu_cD_c$ for every feasible $K$. The tests check this bound with the multipliers of the solver.
- **The solver's projection is exact.** $JKJ$ with the negative eigenvalues set to 0 is the nearest centered positive semidefinite matrix in the Frobenius norm.

There is no general theorem that the output recovers the coordinates of a manifold. Weinberger and Saul argue that maximizing the variance unfolds it, and that holds on their examples, but the local constraints can also leave a curved output.

## Complexity

- **Neighbors (lines L1 and L2).** $O(n^2 d)$ by brute force, with $|E| = O(nk^2)$ constraints.
- **The SDP (line L3).** An interior point method works with an $n \times n$ matrix variable and $O(nk^2)$ constraints. Its cost grows quickly with $n$, and the original method is practical only up to a few thousand points.
- **The simple solver.** Each step costs $O(nk^2)$ for the gradient and a Jacobi eigendecomposition, $O(n^3)$ per sweep; with a warm start, few sweeps are needed. The number of steps $s$ depends on the conditioning of the problem.
- **Embedding (lines L4 and L5).** $O(n^3)$ for the eigendecomposition of $K$.
- **Memory.** $O(n^2)$ for $K$, plus $O(nk^2)$ for the constraints.

The cost of the SDP is the main limit of the method. The landmark versions below reduce it.

## Properties

- **Convex.** The SDP has no false local optima, and its solution does not depend on a starting point, unlike [SMACOF](/smacof/) or [Sammon mapping](/sammon-mapping/).
- **Local isometry.** The distances between neighbors, and between pairs with a common neighbor, are kept exactly.
- **A learned kernel.** $K$ is a kernel matrix for the data, and line L4 is [kernel PCA](/kernel-pca/) with this kernel. Weinberger, Sha and Saul present the method as learning a kernel for nonlinear dimensionality reduction.
- **Low rank in practice.** Maximizing the trace tends to produce a $K$ with few large eigenvalues, so the eigenvalue spectrum gives an estimate of the [intrinsic dimension](/intrinsic-dimension/).
- **No map for new points.** The output is defined only for the input points.

## Variants and improvements

- **Landmark MVU.** Weinberger, Packer and Saul (2005) write $K = QLQ^\top$, where each point is a fixed linear combination of a few landmark points, from the LLE reconstruction weights, and solve a much smaller SDP over $L$.
- **Inequality constraints.** Replace the equalities by $\|y_i - y_j\| \le \|x_i - x_j\|$, or add slack terms, which keeps the problem feasible with noise and lets the solver shrink some distances.
- **Colored MVU and supervised forms.** Add a term that aligns $K$ with side information, such as labels, which gives an embedding that respects both the neighbors and the labels.
- **Dual and graph views.** Sun, Boyd, Xiao and Diaconis show that the dual of MVU is a problem of the fastest mixing Markov process on the neighbor graph, which links MVU with spectral graph methods.
- **First-order solvers.** Projected gradient methods, as in the implementation, or low-rank factorizations $K = YY^\top$ trade the guarantees of interior point methods for a much lower cost per step.

## When to use it

Use semidefinite embedding when you have a few hundred to a few thousand points on a manifold that is close to isometric to a flat region, and you want an output that keeps local distances, with no local optima. It gives clean results on image manifolds such as rotations of an object. For larger data, use the landmark version, or [Isomap](/isomap/), which also keeps distances and costs much less. For pictures of clusters, a neighbor embedding such as [t-SNE](/t-sne/) is a better fit.

## Pitfalls

- **A disconnected graph.** Then the components can drift apart forever, and the trace is unbounded. Make sure the neighbor graph is connected.
- **Infeasible noise.** The input is always feasible for the equality constraints, but if the distances are changed, for example by rounding, they may not be realizable, and the SDP has no solution. Use the inequality or slack form.
- **A wrong $k$.** With $k$ too small, the constraints do not hold the local shape, and the output can fold or collapse in some directions. With $k$ too large, the constraints cross folds of the manifold and stop the unfolding.
- **The cost.** A general SDP solver needs memory and time far beyond those of spectral methods. Plan for the landmark version for large data.
- **Solver tolerance.** A first-order solver stops with small but nonzero constraint errors. Check the largest error, as the tests do, before trusting the distances.

## Implementations

## History

Weinberger and Saul introduced semidefinite embedding in 2004, at CVPR, and with Sha at ICML, where they presented it as learning a kernel matrix for kernel PCA. In 2005 Weinberger, Packer and Saul gave the landmark version for larger data, and the 2006 journal paper in the International Journal of Computer Vision, together with an AAAI paper that year, used the name maximum variance unfolding. In 2006, Sun, Boyd, Xiao and Diaconis showed that the dual problem is the fastest mixing Markov process on the neighbor graph. The method was an early use of semidefinite programming for dimensionality reduction, and it showed that a kernel for kernel PCA can be learned from the data.

## References
