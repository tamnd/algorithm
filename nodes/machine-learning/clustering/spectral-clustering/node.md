---
tag: FGDG1R
kind: algorithm
slug: spectral-clustering
name: Spectral clustering
aliases:
- Ng-Jordan-Weiss clustering
- normalized spectral clustering
- unnormalized spectral clustering
area: machine-learning/clustering
level: advanced
summary: "Build a similarity graph, take the eigenvectors of the k smallest eigenvalues of a graph Laplacian, and run k-means on the rows of the eigenvector matrix."
solves: [clustering-problem]
model: real-ram
complexity:
  vars: {n: the number of points, d: the number of features, k: the number of clusters (given), t: the number of k-means iterations}
  time: {worst: "O(n^2 d + n^3 + n k^2 t)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2000
  people: [Jianbo Shi, Jitendra Malik, Andrew Y. Ng, Michael I. Jordan, Yair Weiss]
  note: Shi and Malik published the normalized cut method in 2000. Ng, Jordan and Weiss gave the variant with the symmetric normalized Laplacian and row normalization at NIPS 2001. Von Luxburg's tutorial of 2007 put the variants side by side.
prereqs: [clustering-problem, laplacian-matrix, eigenvector, k-means]
see_also: [normalized-cut, eigengap-heuristic, kernel-k-means, laplacian-eigenmaps, cheeger-inequality, graph-partitioning-problem, davis-kahan-theorem, lanczos-algorithm]
sources:
  - paper: doi:10.1007/s11222-007-9033-z
    title: "Ulrike von Luxburg, A tutorial on spectral clustering, Statistics and Computing 17(4), 2007, pages 395 to 416"
    locator: "Section 2 (similarity graphs), Section 3 (Propositions 1 to 4 on L, L_sym and L_rw), Section 4 (the three algorithms), Section 8 (practical details) and Section 9 (history)"
  - paper: doi:10.1109/34.868688
    title: "Jianbo Shi and Jitendra Malik, Normalized cuts and image segmentation, IEEE Transactions on Pattern Analysis and Machine Intelligence 22(8), 2000, pages 888 to 905"
    locator: Section 2 (the normalized cut and its relaxation to the generalized eigenproblem) and Section 3 (the grouping algorithm)
  - paper: "Andrew Y. Ng, Michael I. Jordan and Yair Weiss, On spectral clustering: analysis and an algorithm, Advances in Neural Information Processing Systems 14 (NIPS 2001), MIT Press, 2002, pages 849 to 856"
    locator: Section 2 (the algorithm with the normalized affinity matrix and row normalization) and Section 3 (the analysis of the ideal case and its perturbation)
  - paper: "Inderjit S. Dhillon, Yuqiang Guan and Brian Kulis, Kernel k-means, spectral clustering and normalized cuts, Proceedings of the 10th ACM SIGKDD Conference (KDD 2004), pages 551 to 556"
    locator: the equivalence of the weighted kernel k-means objective and the normalized cut objective
---

Spectral clustering groups $n$ data points by the eigenvectors of a [graph Laplacian](/laplacian-matrix/). It builds a similarity graph on the points, takes the [eigenvectors](/eigenvector/) of the $k$ smallest eigenvalues of a Laplacian of that graph, and runs [k-means](/k-means/) on the rows of the $n \times k$ eigenvector matrix. When the graph has exactly $k$ [connected components](/connected-components/), the rows are the same within a component and different across components, so the method returns the components. With a dense eigensolver it costs $O(n^3)$ time and $O(n^2)$ memory; like k-means, it has no global guarantee on general input.

## In plain words

Draw a dot for each data point. Join two dots by a line when the points are similar, and make the line thicker when they are more similar. A good clustering cuts only a few thin lines.

Now think of the lines as springs and let the dots vibrate. The slowest ways of vibration move whole groups of dots together, because a group that is held together by many strong springs moves as one block. The slowest vibrations are the eigenvectors of the graph Laplacian. Give each dot new coordinates: how much it moves in each of the slowest vibrations. Dots of the same group now sit almost on top of each other, far from the other groups. A simple method such as k-means then finds the groups. The groups can have any shape, for example two rings one inside the other, which k-means on the raw points cannot separate.

## The problem

The data model is a similarity graph. The input is a symmetric matrix $W = (w_{ij})$ of size $n \times n$ with $w_{ij} \ge 0$ and $w_{ii} = 0$, and the number of clusters $k$, which is given. The output is a partition of $\{1, \ldots, n\}$ into at most $k$ clusters. This is one form of the [clustering problem](/clustering-problem/), and the method is a relaxation of the [normalized cut](/normalized-cut/) and RatioCut objectives.

When the data are points $x_1, \ldots, x_n \in \mathbb{R}^d$, $W$ comes from one of three similarity graphs (von Luxburg, Section 2):

- **$\varepsilon$-neighborhood graph.** $w_{ij} = 1$ if $\lVert x_i - x_j \rVert \le \varepsilon$, else 0.
- **$k$-nearest-neighbor graph.** Join $i$ and $j$ if $j$ is among the $k$ nearest neighbors of $i$ *or* $i$ is among those of $j$. The *mutual* version needs *and*. This $k$ counts neighbors, not clusters.
- **Fully connected graph.** $w_{ij} = \exp(-\lVert x_i - x_j \rVert^2 / (2\sigma^2))$ for all $i \ne j$, the Gaussian similarity with width $\sigma$.

Let $d_i = \sum_j w_{ij}$ be the degree of vertex $i$ and $D = \mathrm{diag}(d_1, \ldots, d_n)$. The three Laplacians are

$$L = D - W, \qquad L_{\mathrm{sym}} = D^{-1/2} L D^{-1/2} = I - D^{-1/2} W D^{-1/2}, \qquad L_{\mathrm{rw}} = D^{-1} L = I - D^{-1} W.$$

$L$ and $L_{\mathrm{sym}}$ are symmetric and positive semidefinite. $L_{\mathrm{rw}}$ is not symmetric, but $L_{\mathrm{rw}} u = \lambda u$ if and only if $L u = \lambda D u$, if and only if $L_{\mathrm{sym}} (D^{1/2} u) = \lambda D^{1/2} u$. The normalized forms need $d_i > 0$ for each $i$.

**Fact (von Luxburg, Propositions 2 and 4).** The multiplicity of the eigenvalue 0 of $L$, of $L_{\mathrm{rw}}$ and of $L_{\mathrm{sym}}$ equals the number $c$ of connected components $A_1, \ldots, A_c$ of the graph. The eigenspace of 0 is spanned by the indicator vectors $\mathbb{1}_{A_1}, \ldots, \mathbb{1}_{A_c}$ for $L$ and $L_{\mathrm{rw}}$, and by $D^{1/2}\mathbb{1}_{A_1}, \ldots, D^{1/2}\mathbb{1}_{A_c}$ for $L_{\mathrm{sym}}$. The proof is in the correctness proof below; the [Laplacian matrix](/laplacian-matrix/) page proves the case of $L$ by the quadratic form $x^T L x = \sum_{i<j} w_{ij}(x_i - x_j)^2$.

## The algorithm

The three variants of von Luxburg (Section 4) differ only in the matrix and in one extra step.

- **Unnormalized spectral clustering:** the first $k$ eigenvectors of $L$.
- **Shi and Malik:** the first $k$ generalized eigenvectors of $L u = \lambda D u$, that is, the eigenvectors of $L_{\mathrm{rw}}$.
- **Ng, Jordan and Weiss:** the first $k$ eigenvectors of $L_{\mathrm{sym}}$, with each row scaled to length 1.

"First $k$" means the eigenvectors of the $k$ smallest eigenvalues.

```pseudo id=main
SPECTRAL-CLUSTERING(W, k, variant)
L1  d_i ← Σ_j w_ij for each i,  D ← diag(d_1, ..., d_n)
L2  if variant = unnormalized then M ← D − W
L3  else M ← I − D^(−1/2) W D^(−1/2)          ▷ L_sym; needs each d_i > 0
L4  find orthonormal eigenvectors v_1, ..., v_k of M for its k smallest eigenvalues
L5  U ← the n × k matrix with columns v_1, ..., v_k
L6  if variant = Shi-Malik then U ← D^(−1/2) U    ▷ now L U = D U Λ: eigenvectors of L_rw
L7  if variant = NJW then divide each row of U by its Euclidean norm
L8  y_i ← row i of U, for i = 1, ..., n             ▷ a point in R^k
L9  c ← K-MEANS(y_1, ..., y_n; k)                   ▷ k-means++ seeding, then Lloyd
L10 return the clusters A_j = { i : c_i = j }, for j = 1, ..., k
```

Line L6 computes the generalized eigenvectors through the symmetric matrix $L_{\mathrm{sym}}$, because a symmetric eigensolver is stable and returns orthonormal vectors. The sign and, for a repeated eigenvalue, the basis of the eigenvectors in line L4 are arbitrary. The method does not depend on them: k-means sees only the distances between the rows, and a change of basis of the eigenspace is an orthogonal map of $\mathbb{R}^k$, which keeps all distances. This holds when $\lambda_k < \lambda_{k+1}$, so that the eigenspace in line L4 is well defined.

## Example

Take six vertices: two triangles $\{0, 1, 2\}$ and $\{3, 4, 5\}$ with weight 1 on each edge, and one weak edge $\{2, 3\}$ with weight $0.1$. The degrees are 2 for vertices 0, 1, 4 and 5, and 2.1 for vertices 2 and 3.

| matrix | its six eigenvalues, rounded |
|---|---|
| $L$ | 0, 0.0638, 3, 3, 3, 3.1362 |
| $L_{\mathrm{sym}}$ | 0, 0.0314, 1.4524, 1.5, 1.5, 1.5162 |

One eigenvalue is 0, because the graph is connected. The second is small, because the weak edge almost cuts the graph. The second eigenvector of $L$ is $\pm(-0.4169, -0.4169, -0.3903, 0.3903, 0.4169, 0.4169)$: it is negative on one triangle and positive on the other. With $k = 2$, the rows of $U$ are:

| vertex | unnormalized, row of $U$ | NJW, row after line L7 |
|---|---|---|
| 0, 1 | (0.408, −0.417) | (0.700, −0.715) |
| 2 | (0.408, −0.390) | (0.722, −0.692) |
| 3 | (0.408, 0.390) | (0.722, 0.692) |
| 4, 5 | (0.408, 0.417) | (0.700, 0.715) |

The first column is constant: it is the eigenvector $\mathbb{1}/\sqrt{6}$ of $L$ (and $D^{1/2}\mathbb{1}$ scaled, for $L_{\mathrm{sym}}$). The rows form two tight groups, and k-means returns $\{0, 1, 2\}$ and $\{3, 4, 5\}$ for each of the three variants.

Now remove the weak edge. Then $L$ has the eigenvalues $0, 0, 3, 3, 3, 3$, and $L_{\mathrm{sym}}$ has $0, 0, 1.5, 1.5, 1.5, 1.5$. The two eigenvectors for 0 are $\mathbb{1}_{\{0,1,2\}}/\sqrt{3}$ and $\mathbb{1}_{\{3,4,5\}}/\sqrt{3}$, up to a rotation of the pair. The rows of $U$ take exactly two values, and the method returns the two components.

## Correctness

Spectral clustering has no general optimality guarantee: it solves a relaxation, and k-means can stop at a local optimum. What holds exactly is the *ideal case*. If the graph has exactly $k$ connected components (and each $d_i > 0$ for the normalized variants), then each variant returns exactly the components, with probability 1 over the k-means++ seeding. The key step is the fact above: the columns of $U$ span the indicator vectors, so $U = H R$ with $H$ the $n \times k$ matrix of indicator columns and $R$ an invertible $k \times k$ matrix. Row $i$ of $U$ is the row of $R$ of the component of $i$, and the rows of an invertible matrix are distinct. So there are exactly $k$ distinct points, one per component, and k-means++ picks each of them as a center. The full proof, with the NJW row scaling, is in the correctness proof.

For a graph that is close to the ideal case, the [Davis-Kahan theorem](/davis-kahan-theorem/) bounds the angle between the computed eigenspace and the ideal one by the size of the perturbation over the [eigengap](/eigengap-heuristic/) $\lambda_{k+1} - \lambda_k$ (von Luxburg, Section 7). This explains why the method works when the clusters are well separated, but it does not give a bound on the clustering error by itself.

## Complexity

The costs are in the [real RAM](/real-ram/) model, for a dense matrix.

- **Similarity graph.** All pairwise distances cost $\Theta(n^2 d)$. The $k$-nearest-neighbor graph by sorting costs $O(n^2 \log n)$ more.
- **Laplacian.** Lines L1 to L3 cost $\Theta(n^2)$.
- **Eigenvectors.** A dense symmetric eigensolver ([tridiagonalization](/tridiagonalization/) and the [QR algorithm](/qr-algorithm/)) costs $O(n^3)$. The [Jacobi method](/jacobi-eigenvalue-algorithm/) of the implementation costs $\Theta(n^3)$ per sweep and converges quadratically, so few sweeps are needed in practice. For a sparse graph with $m$ edges, the [Lanczos method](/lanczos-algorithm/) or [subspace iteration](/subspace-iteration/) finds the first $k$ eigenvectors with $O(m)$ work per matrix product; the number of iterations depends on the gap $\lambda_{k+1} - \lambda_k$ (von Luxburg, Section 8.2).
- **k-means.** Each Lloyd iteration costs $\Theta(n k^2)$, because the points are in $\mathbb{R}^k$.

The total is $O(n^2 d + n^3 + n k^2 t)$ time with a dense eigensolver, and $\Theta(n^2)$ memory for $W$. With a sparse $k$-nearest-neighbor graph the memory is $O(n k')$ for $k'$ neighbors per point.

## Properties

- **Any cluster shape.** The clusters are the dense parts of the similarity graph, not convex cells as in k-means. Two concentric rings are separated when the graph does not join them.
- **Not deterministic.** The k-means step depends on its seeds. The eigenvectors are unique only up to sign and rotation, which does not change the output.
- **The number of clusters is an input.** The [eigengap heuristic](/eigengap-heuristic/) is one way to choose it.
- **Sensitive to the graph.** The choice of graph and of $\varepsilon$, of the number of neighbors or of $\sigma$ changes the result. Von Luxburg (Section 8.1) recommends the $k$-nearest-neighbor graph as a first choice.

## Variants and improvements

- **Recursive bipartition.** Shi and Malik split the graph by the second generalized eigenvector and recurse on each part; see [normalized cut](/normalized-cut/).
- **Which Laplacian.** Unnormalized clustering relaxes RatioCut, and the normalized variants relax Ncut (von Luxburg, Section 5). Von Luxburg recommends $L_{\mathrm{rw}}$ (Section 8.5), because the normalized variants also make the clusters internally well connected.
- **Kernel k-means.** A weighted [kernel k-means](/kernel-k-means/) objective equals the normalized cut objective (Dhillon, Guan and Kulis 2004), so kernel k-means iterations can replace the eigenvector step.
- **Embedding only.** Lines L1 to L8 alone are [Laplacian eigenmaps](/laplacian-eigenmaps/), a dimensionality reduction method; [diffusion maps](/diffusion-maps/) scale the eigenvectors by powers of the eigenvalues.
- **Large graphs.** Lanczos on a sparse graph, or a low-rank approximation of $W$ (for example the Nystrom method) for a dense one.

## When to use it

Use spectral clustering when the clusters are connected regions of irregular shape, when the input is a graph or a similarity matrix rather than points, or when k-means fails because the clusters are not convex. Do not use it for a very large dense similarity matrix, where the $O(n^2)$ memory and $O(n^3)$ time are too high, unless the graph is sparse. When the clusters are compact and convex, plain k-means is cheaper and gives similar results. When the density of the clusters varies and the number of clusters is unknown, [DBSCAN](/dbscan/) or [HDBSCAN](/hdbscan/) can be a better fit.

## Pitfalls

- **Too many components.** If the similarity graph has more connected components than $k$, line L4 returns indicator vectors of some components only, and the result depends on an arbitrary basis. Make the graph connected, or check the number of zero eigenvalues first (von Luxburg, Section 8.1).
- **Isolated vertices.** Line L3 divides by $\sqrt{d_i}$. A point with no neighbor has $d_i = 0$. Remove it, or use the unnormalized variant.
- **Forgetting the row normalization.** With $L_{\mathrm{sym}}$, the rows of $U$ in the ideal case are $\sqrt{d_i}$ times the row of the component, so vertices of low degree lie near the origin. Line L7 removes the factor. The Shi and Malik variant gets the same effect from line L6.
- **Taking the largest eigenvalues.** Line L4 uses the smallest eigenvalues of the Laplacian. The largest eigenvalues of $D^{-1/2} W D^{-1/2} = I - L_{\mathrm{sym}}$ are the same vectors; mixing the two forms is a common bug.
- **Bad width $\sigma$.** A very small $\sigma$ makes each point its own component; a very large one makes $W$ nearly constant. Choose $\sigma$ near the typical distance to the nearest neighbors.

## Implementations

## History

Von Luxburg (Section 9) traces the method to Donath and Hoffman (1973), who partitioned graphs with eigenvectors of the adjacency matrix, and to Fiedler (1973), who related bipartitions to the second eigenvector of the Laplacian. Shi and Malik (2000) introduced the normalized cut and its relaxation for image segmentation. Ng, Jordan and Weiss (2001) gave the variant with $L_{\mathrm{sym}}$ and the row normalization, with an analysis of the ideal case by perturbation theory. Von Luxburg's tutorial (2007) compared the three variants and derived them from graph cuts, random walks and perturbation theory.

## References
