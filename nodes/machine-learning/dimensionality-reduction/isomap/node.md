---
tag: HKAVDA
kind: algorithm
slug: isomap
name: Isomap
aliases:
- isometric feature mapping
- isometric mapping
area: machine-learning/dimensionality-reduction
level: core
summary: "Approximate geodesic distances by shortest paths in a nearest neighbor graph, then embed them with classical MDS."
model: real-ram
complexity:
  vars: {n: the number of points, d: the input dimension, k: the number of neighbors, m: the output dimension}
  time: {worst: "O(n^2 d + n^2 k log n + n^3)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2000
  people: [Joshua B. Tenenbaum, Vin de Silva, John C. Langford]
  note: Tenenbaum, de Silva and Langford published Isomap in Science in December 2000, in the same issue as locally linear embedding.
prereqs: [classical-mds, k-nearest-neighbor-graph, all-pairs-shortest-paths, manifold-learning]
see_also: [dijkstra, locally-linear-embedding, hessian-eigenmaps, semidefinite-embedding, kernel-pca, manifold-hypothesis, sammon-mapping, connected-components]
sources:
  - paper: doi:10.1126/science.290.5500.2319
    title: Joshua B. Tenenbaum, Vin de Silva and John C. Langford, A global geometric framework for nonlinear dimensionality reduction, Science 290(5500), 2000, pages 2319 to 2323
    locator: the three steps (neighborhood graph, shortest paths, classical MDS), the residual variance plots and the examples on face images and handwritten digits
  - paper: "Mira Bernstein, Vin de Silva, John C. Langford and Joshua B. Tenenbaum, Graph approximations to geodesics on embedded manifolds, technical report, Department of Psychology, Stanford University, December 2000"
    locator: the main theorem, which bounds the ratio of graph distances to geodesic distances for a dense enough sample
  - paper: "Vin de Silva and Joshua B. Tenenbaum, Global versus local methods in nonlinear dimensionality reduction, Advances in Neural Information Processing Systems 15, 2003"
    locator: landmark Isomap and conformal Isomap
  - paper: doi:10.1073/pnas.1031596100
    title: David L. Donoho and Carrie Grimes, Hessian eigenmaps, locally linear embedding techniques for high-dimensional data, PNAS 100(10), 2003
    locator: the discussion of the convexity condition that Isomap needs, and the example where it fails
  - paper: "Yoshua Bengio, Jean-François Paiement, Pascal Vincent, Olivier Delalleau, Nicolas Le Roux and Marie Ouimet, Out-of-sample extensions for LLE, Isomap, MDS, Eigenmaps, and spectral clustering, Advances in Neural Information Processing Systems 16, 2004"
    locator: the kernel form of Isomap and its extension to new points
---

Isomap is a method of [manifold learning](/manifold-learning/) that maps points on a curved surface in a space of many dimensions to a few coordinates, with distances along the surface kept. Tenenbaum, de Silva and Langford (2000) estimated the distance along the surface, the geodesic distance, by the length of the shortest path in a graph that joins each point to its nearest neighbors, and then applied [classical MDS](/classical-mds/) to these graph distances. When the data lie on a manifold that is isometric to a convex region of $\mathbb{R}^m$ and the sample is dense enough, the result is close to the true flat coordinates, up to a rigid motion.

## In plain words

Picture a rolled sheet of paper with dots on it. Two dots on adjacent layers of the roll can be close in space but far apart on the paper. Isomap wants the distances on the paper. It finds them in two steps. First, it joins each dot to its few closest dots, because close dots are close on the paper too. Then it measures the distance between any two dots as the length of the shortest chain of such short links, like a walk along the paper. With these walking distances in hand, it lays the dots out flat with classical MDS, which is the standard way to draw points from a table of distances.

## The problem

The input is $n$ points $x_1, \dots, x_n \in \mathbb{R}^d$, a neighborhood rule (the $k$ nearest neighbors, or all points within distance $\varepsilon$), and an output dimension $m$. The model is that the points lie on, or close to, a manifold $\mathcal{M}$ of dimension $m$ with geodesic distance $d_{\mathcal{M}}$. The output is $y_1, \dots, y_n \in \mathbb{R}^m$ with $\|y_i - y_j\| \approx d_{\mathcal{M}}(x_i, x_j)$ for all pairs. If $\mathcal{M}$ is isometric to a convex set in $\mathbb{R}^m$, such $y_i$ exist with equality, and they are the coordinates of the points in that set.

## The algorithm

```pseudo id=main
ISOMAP(x_1..x_n, k or ε, m)
L1  G ← the graph that joins i and j, with weight ‖x_i − x_j‖, if one is a k-nearest neighbor of the other (or if ‖x_i − x_j‖ ≤ ε)
L2  for each vertex s do
L3      D_G[s, ·] ← the shortest path distances from s in G, by Dijkstra's algorithm
L4  if some D_G[s, t] = ∞ then fail: G is not connected
L5  B ← −1/2 J D_G^(2) J, with J = I − (1/n) 1 1ᵀ and D_G^(2) the entrywise squares
L6  (λ_1, v_1), …, (λ_m, v_m) ← the m largest eigenpairs of B
L7  y_i ← (√λ_1 v_1[i], …, √λ_m v_m[i]) for each i
L8  return y_1, …, y_n
```

Lines L1 to L4 compute the graph distances. Line L1 makes the [k-nearest neighbor graph](/k-nearest-neighbor-graph/) symmetric. Lines L2 and L3 solve the [all pairs shortest paths](/all-pairs-shortest-paths/) problem with [Dijkstra's algorithm](/dijkstra/) from each vertex; the paper used [Floyd-Warshall](/floyd-warshall/), which gives the same distances. Lines L5 to L7 are [classical MDS](/classical-mds/) on these distances: double centering, the top eigenvectors, and a scaling by the square roots of the eigenvalues.

## Example

Take the five points $(0,1), (0,0), (1,0), (2,0), (2,1)$ that form a U shape, and the radius $\varepsilon = 1$. Each point is joined only to the next point along the U, so the graph is a path with five vertices and unit edges, and $D_G[i, j] = |i - j|$. The two ends are at straight-line distance 2, but at graph distance 4.

Double centering the path metric gives $B = x x^\top$ with $x = (-2, -1, 0, 1, 2)$, so the eigenvalues are $10, 0, 0, 0, 0$. The output for $m = 1$ is the coordinates $2, 1, 0, -1, -2$ (the sign of an eigenvector is arbitrary): Isomap unbends the U into a straight segment of length 4, and the second eigenvalue 0 says that one dimension is enough.

With $\varepsilon = 2$ the graph also joins the two ends directly, and it joins some pairs of points that are two steps apart along the U. The graph distance between the ends drops from 4 to 2, and the eigenvalues become $4.414, 1.554, 0, -0.022, -0.414$. The output is no longer one-dimensional. This is a *short circuit*: one edge that jumps across the gap of the U.

## Correctness

The method is correct in the following sense, with the proofs in the proofs section below.

- **Classical MDS step.** If the graph distances equal the Euclidean distances of some points $z_1, \dots, z_n \in \mathbb{R}^m$, lines L5 to L7 return the $z_i$ up to a rigid motion. This is the exact recovery theorem of classical MDS.
- **Graph distances never undercut on a convex sheet.** If the points lie on a flat convex region (or on a manifold isometric to one) and every graph edge is a straight segment in that region, then each graph distance is at least the true distance, by the triangle inequality.
- **The upper bound needs dense sampling.** Bernstein, de Silva, Langford and Tenenbaum (2000) proved that for any $\lambda_1, \lambda_2 \in (0, 1)$, if the manifold is geodesically convex, $\varepsilon$ is small compared with the minimum radius of curvature and the branch separation of the manifold, and the sample is dense enough compared with $\varepsilon$, then $(1 - \lambda_1) d_{\mathcal{M}} \le D_G \le (1 + \lambda_2) d_{\mathcal{M}}$ for all pairs, with high probability for random samples. The condition on $\varepsilon$ rules out short circuits like the one in the example.

Together these give consistency: the graph distances converge to the geodesic distances, and classical MDS of distances that are close to Euclidean is close to the true configuration.

## Complexity

- **Neighbor graph (line L1).** $O(n^2 d)$ with a brute force search, which is what the implementation does, plus $O(n^2 \log n)$ to sort. A tree or an approximate index makes it faster for small $d$.
- **Shortest paths (lines L2 to L3).** The graph has at most $nk$ edges, so Dijkstra with a binary heap from each vertex costs $O(n \cdot nk \log n) = O(n^2 k \log n)$. Floyd-Warshall costs $O(n^3)$.
- **Classical MDS (lines L5 to L7).** Double centering costs $O(n^2)$. A full dense eigendecomposition costs $O(n^3)$. The $m$ top eigenvectors by [Lanczos](/lanczos-algorithm/) cost about $O(n^2 m)$ per restart.
- **Memory.** $\Theta(n^2)$ for the dense matrix $D_G$ and for $B$.

The quadratic memory and the cubic eigendecomposition limit plain Isomap to some thousands of points. Landmark Isomap runs Dijkstra only from $\ell \ll n$ landmark points, so for a fixed $\ell$ its cost grows close to linearly in $n$.

## Properties

- **Global.** Isomap keeps all pairwise geodesic distances, not only local ones. So it keeps the large-scale shape of the manifold, but one bad edge changes many distances.
- **A spectral gap shows the dimension.** On a manifold of dimension $m$, the eigenvalues of $B$ drop after the $m$-th. The paper plots the *residual variance* $1 - R^2(D_G, D_Y)$ against $m$ for the same purpose.
- **Needs convexity.** If the manifold is isometric to a non-convex region of $\mathbb{R}^m$, such as a sheet with a hole, the geodesic distances go around the hole and are not the Euclidean distances of the flat coordinates. The embedding is then distorted. [Hessian eigenmaps](/hessian-eigenmaps/) does not need this condition.
- **A kernel method.** For a Euclidean $D_G$, Isomap is [kernel PCA](/kernel-pca/) with the kernel $-\frac12 J D_G^{(2)} J$. In general $B$ can have negative eigenvalues, and the kernel is not positive semidefinite.

## Variants and improvements

- **Landmark Isomap.** de Silva and Tenenbaum (2003) compute the graph distances from a few landmark points only, apply classical MDS to the landmarks, and place every other point by distance-based triangulation from its distances to the landmarks.
- **Conformal Isomap.** The same paper rescales each edge by the local density, so that Isomap recovers conformal (angle-keeping) maps, not only isometric ones.
- **Out-of-sample extension.** Bengio et al. (2004) write Isomap as an eigenfunction problem of a data-dependent kernel. A new point gets coordinates from its graph distances to the training points, by a Nyström-type formula.
- **Other graph rules.** The $\varepsilon$ rule, a mutual $k$-nearest neighbor rule, or the removal of edges with a large flow through them, all aim to avoid short circuits.

## When to use it

Use Isomap when the data lie on one smooth sheet that is close to flat when unrolled, with no holes, and the sample is dense. It gives a global layout in which large distances mean something. For sheets with holes or uneven curvature, use [Hessian eigenmaps](/hessian-eigenmaps/) or [local tangent space alignment](/local-tangent-space-alignment/). For noisy data or data with clusters, local methods such as [Laplacian eigenmaps](/laplacian-eigenmaps/) or neighbor embeddings such as [t-SNE](/t-sne/) are usually more robust.

## Pitfalls

- **Short circuits.** A $k$ or $\varepsilon$ that is too large joins points across a fold, as in the example. The graph distances then collapse, and the embedding folds. Check the edges against the expected spacing, and try a few values.
- **A disconnected graph.** A $k$ or $\varepsilon$ that is too small leaves the graph in pieces, and some distances are infinite. The implementation raises an error. Run Isomap on each [connected component](/connected-components/) separately, or add edges.
- **Non-convex manifolds.** Holes and concave boundaries bend the geodesics, and the embedding is then distorted near them.
- **Noise.** Noise across the manifold adds short edges between layers. Denoise or use a smaller neighborhood.
- **Negative eigenvalues.** Graph distances are rarely exactly Euclidean, so $B$ has negative eigenvalues. Keep only the positive top $m$, and use their size, not a fixed $m$, to judge the fit.

## Implementations

## History

Tenenbaum, de Silva and Langford published Isomap in Science in December 2000, in the same issue as [locally linear embedding](/locally-linear-embedding/) by Roweis and Saul. The two papers made nonlinear dimensionality reduction by graphs and eigenvectors a field of its own. The companion technical report by Bernstein, de Silva, Langford and Tenenbaum gave the convergence guarantee for the graph distances. de Silva and Tenenbaum then proposed the landmark and conformal variants, and Donoho and Grimes analyzed the convexity condition and removed it with Hessian eigenmaps.

## References
