---
tag: H05ZK6
kind: algorithm
slug: classical-mds
name: Classical MDS
aliases:
- Torgerson scaling
- principal coordinates analysis
- Torgerson-Gower scaling
area: machine-learning/dimensionality-reduction
level: core
summary: "Double center the squared distance matrix and take its top eigenvectors. Exact for Euclidean distances, and the same as PCA on Euclidean points."
model: real-ram
complexity:
  vars: {n: the number of points, k: the output dimension}
  time: {worst: "O(n^3)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1952
  people: [Warren S. Torgerson, John C. Gower, Gale Young, Alston S. Householder, Isaac J. Schoenberg]
  note: Schoenberg (1935) and Young and Householder (1938) gave the test for a Euclidean distance matrix. Torgerson (1952) made it a scaling method, and Gower (1966) named it principal coordinates analysis.
prereqs: [multidimensional-scaling, symmetric-eigenproblem, positive-definite-matrix]
see_also: [principal-component-analysis, isomap, smacof, kernel-pca, semidefinite-embedding, singular-value-decomposition, jacobi-eigenvalue-algorithm, hoffman-wielandt-theorem]
sources:
  - paper: doi:10.1007/BF02288916
    title: Warren S. Torgerson, Multidimensional scaling, I. Theory and method, Psychometrika 17(4), 1952, pages 401 to 419
    locator: the scalar product matrix from distances and its factorization
  - paper: doi:10.1093/biomet/53.3-4.325
    title: John C. Gower, Some distance properties of latent root and vector methods used in multivariate analysis, Biometrika 53(3/4), 1966, pages 325 to 338
    locator: principal coordinates analysis and its relation to principal components
  - paper: doi:10.2307/1968654
    title: Isaac J. Schoenberg, Remarks to Maurice Fréchet's article, Annals of Mathematics 36(3), 1935, pages 724 to 732
    locator: the criterion for a distance matrix to embed in a Euclidean space
  - paper: doi:10.1007/BF02287916
    title: Gale Young and Alston S. Householder, Discussion of a set of points in terms of their mutual distances, Psychometrika 3(1), 1938, pages 19 to 22
    locator: the Euclidean test by a positive semidefinite matrix and the dimension as its rank
  - book: isbn:9780387251509
    title: Ingwer Borg and Patrick J. F. Groenen, Modern Multidimensional Scaling, second edition, Springer, 2005
    locator: Chapter 12 (Classical scaling) and Chapter 19 (Euclidean embeddings)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 14.8 (Multidimensional scaling)
---

Classical MDS is the eigenvector method of [multidimensional scaling](/multidimensional-scaling/): it turns a matrix of distances into a matrix of inner products by double centering, and takes the top $k$ [eigenvectors](/eigenvector/) of that matrix as coordinates. When the distances come from points in a Euclidean space, it recovers those points exactly, up to a rotation, a reflection and a translation. On such data it gives the same coordinates as [principal component analysis](/principal-component-analysis/). The double-centered matrix also gives an exact test of whether a distance matrix is Euclidean at all.

## In plain words

You have a table of distances between towns, but no map. Distances do not tell you where the origin is or which way north points, but they do fix the shape. Classical MDS puts the origin at the center of all the towns. From the distances it then works out, for each pair of towns, the product of their positions as seen from this center. This table of products holds the same information as the map. Its main directions, found by an eigenvector computation, are the axes of the map, and the size of each direction says how spread out the towns are along it. Keep the largest few directions and you get a map in a few dimensions. If the distances could not come from any flat map, a direction with a negative size appears, and this shows the problem.

## The problem

The input is a symmetric $n \times n$ matrix $D = (d_{ij})$ with $d_{ii} = 0$ and $d_{ij} \ge 0$, and a target dimension $k$. Here $n$ is the number of points and $k$ is the output dimension. The output is a configuration $X \in \mathbb{R}^{n \times k}$, one row $x_i$ for each point. We call $D$ *Euclidean of dimension $p$* when there are points $z_1, \ldots, z_n \in \mathbb{R}^p$ with $d_{ij} = \|z_i - z_j\|$ for all $i, j$.

Write $D^{(2)}$ for the matrix of the squared entries $d_{ij}^2$, $\mathbf{1}$ for the vector of ones, and $J = I - \frac{1}{n}\mathbf{1}\mathbf{1}^\top$ for the centering matrix. The double-centered matrix is

$$B = -\tfrac{1}{2} J D^{(2)} J, \qquad b_{ij} = -\tfrac{1}{2}\left(d_{ij}^2 - r_i - r_j + g\right),$$

where $r_i = \frac{1}{n}\sum_j d_{ij}^2$ is a row mean and $g = \frac{1}{n}\sum_i r_i$ is the grand mean. Classical MDS minimizes the *strain* $\|B - XX^\top\|_F$ over all $X \in \mathbb{R}^{n \times k}$. This is a different criterion from the stress of [SMACOF](/smacof/), which compares distances, not inner products.

## The algorithm

```pseudo id=main
CLASSICAL-MDS(D, k)
L1  n ← the number of rows of D
L2  A ← the matrix with entries a_ij = d_ij²
L3  r_i ← (1/n) Σ_j a_ij for each i, and g ← (1/n) Σ_i r_i
L4  B ← the matrix with entries b_ij = −(a_ij − r_i − r_j + g) / 2
L5  (λ_1 ≥ … ≥ λ_n, v_1, …, v_n) ← the eigenvalues of B and orthonormal eigenvectors
L6  s_j ← √(max(λ_j, 0)) for j = 1, …, k
L7  X ← the n × k matrix with columns s_1 v_1, …, s_k v_k
L8  return X and λ_1, …, λ_n
```

Lines L2 to L4 compute $-\frac12 J D^{(2)} J$ in $O(n^2)$ operations, without a matrix product. Line L5 is a [symmetric eigenproblem](/symmetric-eigenproblem/). The implementation uses the cyclic [Jacobi method](/jacobi-eigenvalue-algorithm/), which is simple and accurate for small $n$. For large $n$ and small $k$, the [Lanczos algorithm](/lanczos-algorithm/) finds the top $k$ eigenpairs with matrix vector products only. Line L6 sets an axis to zero when its eigenvalue is not positive, because no real coordinate has a negative square.

## Example

Take the corners of a 3 by 4 rectangle, $(0,0), (3,0), (3,4), (0,4)$. The input is only the distance matrix, and the output does not know the corners.

$$D = \begin{pmatrix} 0 & 3 & 5 & 4 \\ 3 & 0 & 4 & 5 \\ 5 & 4 & 0 & 3 \\ 4 & 5 & 3 & 0 \end{pmatrix}, \qquad B = \frac{1}{4}\begin{pmatrix} 25 & 7 & -25 & -7 \\ 7 & 25 & -7 & -25 \\ -25 & -7 & 25 & 7 \\ -7 & -25 & 7 & 25 \end{pmatrix}.$$

Each row of $D^{(2)}$ is a permutation of $0, 9, 16, 25$, so $r_i = 25/2$ for each $i$ and $g = 25/2$. Then $b_{ij} = -\frac12(d_{ij}^2 - 25/2)$, which gives $b_{11} = 25/4$, $b_{12} = -\frac12(9 - 25/2) = 7/4$, $b_{13} = -25/4$ and $b_{14} = -7/4$. This $B$ is the Gram matrix of the centered corners $(\mp 3/2, \mp 2)$, as the theory below says.

The eigenvalues of $B$ are $16, 9, 0, 0$. Two are positive, so the distances are Euclidean of dimension 2. The output for $k = 2$ is

| point | first axis | second axis |
|---|---|---|
| (0, 0) | −2 | 1.5 |
| (3, 0) | −2 | −1.5 |
| (3, 4) | 2 | −1.5 |
| (0, 4) | 2 | 1.5 |

This is the rectangle again, centered at the origin, and turned by a quarter turn, so that its long side lies on the first axis. Its six distances equal the input. The first eigenvalue $16 = 4 \cdot 2^2$ is the sum of squares of the coordinates on the long axis, and $9 = 4 \cdot 1.5^2$ is the same for the short axis.

**A non-example.** The shortest path metric of the star with one center and three leaves has $d = 1$ from the center to each leaf and $d = 2$ between two leaves. Then

$$B = \frac{1}{16}\begin{pmatrix} -3 & 1 & 1 & 1 \\ 1 & 21 & -11 & -11 \\ 1 & -11 & 21 & -11 \\ 1 & -11 & -11 & 21 \end{pmatrix}$$

has the eigenvalues $2, 2, 0, -\frac14$, with the eigenvector $(3, -1, -1, -1)$ for $-\frac14$. So no set of points in any Euclidean space has these distances. Each leaf pair would need the center at its midpoint, and three leaves cannot share one midpoint pairwise. Classical MDS still returns a planar map, but its distances are not the input distances.

## Correctness

The method rests on three facts. The full proofs are in the proofs section below.

- **Distances give inner products.** If $d_{ij} = \|z_i - z_j\|$, then $B = Z_c Z_c^\top$, where $Z_c$ holds the points minus their mean. The terms $\|z_i\|^2$ and $\|z_j\|^2$ in $d_{ij}^2 = \|z_i\|^2 + \|z_j\|^2 - 2 z_i^\top z_j$ are removed by $J$, because $J\mathbf{1} = 0$.
- **The Euclidean test (Schoenberg 1935; Young and Householder 1938).** $D$ is Euclidean of dimension $p$ if and only if $B$ is [positive semidefinite](/positive-definite-matrix/) with rank at most $p$. The points $X = V_p \Lambda_p^{1/2}$ then have exactly the distances $D$, and two configurations with the same distances differ by a rigid motion.
- **Optimality.** For any symmetric $B$, the output minimizes the strain $\|B - XX^\top\|_F$ over all $n \times k$ matrices $X$. This follows from the [Hoffman-Wielandt theorem](/hoffman-wielandt-theorem/).

## Complexity

- **Forming $B$.** Lines L2 to L4 cost $\Theta(n^2)$ operations and $\Theta(n^2)$ memory. The input itself is $\Theta(n^2)$.
- **The eigenproblem.** A full symmetric eigendecomposition costs $O(n^3)$ operations, by tridiagonal reduction and the QR algorithm, or by the Jacobi method in practice. Only the top $k$ eigenpairs are needed. A Lanczos or [power iteration](/power-iteration/) method costs $O(n^2)$ per matrix vector product, and the number of products depends on the gaps between the eigenvalues.
- **Memory.** $\Theta(n^2)$ for $B$ and $\Theta(n k)$ for the output.

These bounds are worst case for the direct method. There is no iteration on the configuration itself, so there is no local minimum and no starting point.

## Properties

- **Exact on Euclidean input.** If $D$ is Euclidean of dimension $p \le k$, the output distances equal the input distances.
- **Equal to PCA on Euclidean points.** If $D$ comes from the rows of a data matrix $X_0$ with the Euclidean norm, the output equals the first $k$ PCA scores of $X_0$, up to the sign of each axis. Write $J X_0 = U S W^\top$ as a [singular value decomposition](/singular-value-decomposition/). Then $B = U S^2 U^\top$, and $U_k S_k = J X_0 W_k$ is the projection on the first $k$ principal axes. PCA does a $d \times d$ eigenproblem and classical MDS an $n \times n$ one, so PCA is cheaper when $d < n$.
- **Nested.** The solution for $k$ dimensions is the first $k$ columns of the solution for $k + 1$ dimensions. Stress-based methods do not have this property.
- **Explained strain.** The ratio $\sum_{j \le k} \lambda_j / \sum_{j: \lambda_j > 0} \lambda_j$ is the share of the spread kept by $k$ axes. It is the analogue of the [explained variance](/explained-variance/) of PCA.
- **Centered.** The columns of $X$ sum to zero, because the eigenvectors of nonzero eigenvalues are orthogonal to $\mathbf{1}$, and $B\mathbf{1} = 0$.

## Variants and improvements

- **Kernel view.** $B$ is a centered Gram matrix, so classical MDS is [kernel PCA](/kernel-pca/) with the kernel $-\frac12 d^2$. [Isomap](/isomap/) runs classical MDS on graph distances, and [semidefinite embedding](/semidefinite-embedding/) learns the Gram matrix directly.
- **Landmark MDS.** De Silva and Tenenbaum run classical MDS on a few landmark points and place each other point from its distances to the landmarks. This avoids the $n \times n$ eigenproblem.
- **Non-Euclidean input.** When $B$ has negative eigenvalues, one can drop them (this is what line L6 does), add a constant to the off-diagonal distances until $B$ is positive semidefinite, or switch to a stress method such as [SMACOF](/smacof/) and start it from the classical solution.
- **Weights and missing entries.** Classical MDS needs every entry of $D$. With missing or weighted entries, use a stress method.

## When to use it

Use classical MDS when the dissimilarities are close to Euclidean distances, or when you need a fast, deterministic start for an iterative method. Use it to test whether a distance matrix is Euclidean and to find its dimension: count the positive eigenvalues of $B$. If you have the data points and the Euclidean norm, use [PCA](/principal-component-analysis/) instead, which gives the same answer from a smaller matrix. Do not use it when large distances are unreliable: the strain is dominated by the largest entries of $B$, so large distances drive the result.

## Pitfalls

- **Forgetting the square.** Double centering is applied to the squared distances $D^{(2)}$, not to $D$. With $D$ the result is wrong even on exact Euclidean input.
- **Negative eigenvalues.** Taking $\sqrt{\lambda_j}$ of a negative eigenvalue gives a complex number. Check the sign, report it, and set the axis to zero or drop it.
- **Reading the axes.** The output is fixed only up to a rotation inside each eigenspace of a repeated eigenvalue, and up to the sign of each axis. Two programs can give different, equally correct pictures.
- **Strain is not stress.** Classical MDS is optimal for the inner products, not for the distances. On non-Euclidean input, a stress method can give distances that fit better.
- **Truncation of near-zero eigenvalues.** On exact Euclidean data, rounding makes the zero eigenvalues small numbers of either sign. Use a tolerance relative to $\lambda_1$ when you count the dimension.

## Implementations

## History

Schoenberg (1935) and Young and Householder (1938) showed that a distance matrix is Euclidean exactly when a matrix of inner products built from it is positive semidefinite, and that its rank is the dimension. Torgerson (1952) turned this into a method for psychological data: estimate the distances, convert them to inner products, and factor the result. Gower (1966) studied the method as an ordination for any distance or similarity coefficient, named it principal coordinates analysis, and showed its relation to principal components.

## References
