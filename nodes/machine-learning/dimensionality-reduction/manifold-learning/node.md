---
tag: JZDF07
kind: concept
slug: manifold-learning
name: Manifold learning
aliases:
- nonlinear dimensionality reduction
area: machine-learning/dimensionality-reduction
level: core
summary: "Methods that find low-dimensional coordinates for data that lie near a curved manifold, usually from a neighbor graph and the eigenvectors of a matrix built on it."
prereqs: [principal-component-analysis, multidimensional-scaling]
see_also: [isomap, locally-linear-embedding, laplacian-eigenmaps, diffusion-maps, semidefinite-embedding, t-sne, manifold-hypothesis, intrinsic-dimension]
sources:
  - paper: doi:10.1126/science.290.5500.2319
    title: Joshua B. Tenenbaum, Vin de Silva and John C. Langford, A global geometric framework for nonlinear dimensionality reduction, Science 290(5500), 2000
    locator: the formulation of the problem as the recovery of the coordinates of a manifold, and the global approach
  - paper: doi:10.1126/science.290.5500.2323
    title: Sam T. Roweis and Lawrence K. Saul, Nonlinear dimensionality reduction by locally linear embedding, Science 290(5500), 2000
    locator: the local approach by linear reconstructions in each neighborhood
  - paper: "Vin de Silva and Joshua B. Tenenbaum, Global versus local methods in nonlinear dimensionality reduction, Advances in Neural Information Processing Systems 15, 2003"
    locator: the distinction between global and local methods
  - paper: "Yoshua Bengio, Jean-François Paiement, Pascal Vincent, Olivier Delalleau, Nicolas Le Roux and Marie Ouimet, Out-of-sample extensions for LLE, Isomap, MDS, Eigenmaps, and spectral clustering, Advances in Neural Information Processing Systems 16, 2004"
    locator: the common view of these methods as eigenfunctions of a data-dependent kernel, and the Nyström formula for new points
  - book: isbn:9780387393506
    title: John A. Lee and Michel Verleysen, Nonlinear Dimensionality Reduction, Springer, 2007
    locator: Chapters 4 and 5 (distance preservation and topology preservation)
---

Manifold learning is the family of methods that find a few coordinates for data in a space of many dimensions under the assumption that the data lie on or near a smooth curved surface of low dimension, a manifold. Linear methods such as [principal component analysis](/principal-component-analysis/) can only find a flat subspace. Manifold learning methods use the local geometry, usually through a graph that joins each point to its nearest neighbors, to follow the curve of the manifold. Most of them end with an eigenvalue problem on a matrix built from that graph.

## In plain words

A photo of a face has thousands of pixels, but if the only thing that changes between photos is the angle of the head, the photos really vary in one direction only. They lie along a curve in the space of all pictures. Manifold learning tries to find that hidden direction from the photos alone. It relies on one fact: close photos are similar in a simple, almost linear way. So the methods look at small groups of close points, describe each group, and then glue the descriptions into one map. The methods differ in what they keep: some keep all distances measured along the curve, others keep only which points are neighbors.

## The idea

The data are $x_1, \dots, x_n \in \mathbb{R}^D$. The model is that $x_i = \phi(z_i)$, or close to it, for unknown $z_i \in \mathbb{R}^m$ with $m \ll D$ and a smooth map $\phi$ whose image is a manifold $\mathcal{M}$. The goal is to find $y_i \in \mathbb{R}^m$ that recover the $z_i$, up to a transformation that the method cannot detect, such as a rigid motion or an affine map. This model is the [manifold hypothesis](/manifold-hypothesis/), and $m$ is the [intrinsic dimension](/intrinsic-dimension/).

Almost all methods follow the same three steps.

1. **A neighbor graph.** Join each point to its $k$ nearest neighbors or to all points within a radius $\varepsilon$ (a [k-nearest neighbor graph](/k-nearest-neighbor-graph/)). Close points in $\mathbb{R}^D$ are taken to be close on $\mathcal{M}$.
2. **A matrix from local geometry.** Describe each neighborhood: by distances, by the weights of a linear reconstruction, by a heat kernel, or by a local tangent space. Combine the descriptions in an $n \times n$ matrix.
3. **An eigenvalue problem.** Read the coordinates from a few eigenvectors of that matrix: the top ones for a Gram matrix, or the bottom ones, after the constant, for a Laplacian-type matrix.

**Global and local methods.** de Silva and Tenenbaum (2003) sort the methods into two groups.

- *Global methods* try to keep a quantity for all pairs of points. [Isomap](/isomap/) keeps the geodesic distances, estimated by shortest paths in the graph. [Semidefinite embedding](/semidefinite-embedding/) keeps the local distances and pulls all other points as far apart as it can. These methods build dense $n \times n$ matrices and keep the large-scale shape, but a single wrong edge (a short circuit) can damage the whole result.
- *Local methods* keep only properties of each neighborhood. [Locally linear embedding](/locally-linear-embedding/), [Hessian eigenmaps](/hessian-eigenmaps/), [local tangent space alignment](/local-tangent-space-alignment/), [Laplacian eigenmaps](/laplacian-eigenmaps/) and [diffusion maps](/diffusion-maps/) are in this group. Their matrices are sparse, which makes them faster, and they can handle more kinds of manifolds, but the large-scale layout is less reliable.

**A common kernel view.** Bengio et al. (2004) showed that classical MDS, Isomap, LLE, Laplacian eigenmaps and spectral clustering all compute the leading eigenvectors of a data-dependent kernel matrix $\tilde K$, normalized in a method-specific way. The embedding of a training point $x_i$ in coordinate $l$ is then, up to a scale, $v_l[i]$, where $v_l$ is the $l$-th eigenvector of $\tilde K$. This puts the methods next to [kernel PCA](/kernel-pca/), with the difference that the kernel is built from the data and need not be positive semidefinite.

**The out-of-sample problem.** Most of these methods return coordinates for the given points only, not a map $f: \mathbb{R}^D \to \mathbb{R}^m$. A new point would need a new run. Three answers are common.

- *The Nyström formula.* Using the kernel view, Bengio et al. define the coordinate of a new point $x$ as $f_l(x) = \frac{\sqrt n}{\lambda_l}\sum_i v_l[i]\,\tilde K(x, x_i)$, where $\tilde K(x, \cdot)$ is the kernel extended to $x$ by the same formula as for the training points. At a training point $x_i$ it gives $\sqrt n\, v_l[i]$, the training coordinate up to the same scale for all points.
- *Local reconstruction.* Write the new point as a combination of its neighbors, as in LLE, and apply the same weights to the neighbors' coordinates.
- *A linear or parametric map.* Restrict the map to a family and fit it with the same criterion. [Locality preserving projections](/locality-preserving-projections/) does this with a linear map for Laplacian eigenmaps. A neural network does it in a parametric embedding or an [autoencoder](/autoencoder/).

## Examples

- **The Swiss roll.** Points on the surface $(t\cos t, h, t\sin t)$ for $t$ in an interval longer than one turn. Points on adjacent layers are close in $\mathbb{R}^3$ but far on the surface. PCA and [classical MDS](/classical-mds/) on straight-line distances project the layers on top of each other. Isomap and LLE, with a small enough neighborhood, unroll the sheet to the rectangle of $(t, h)$.
- **A U shape.** The five points $(0,1), (0,0), (1,0), (2,0), (2,1)$ with each point joined to the next one: the graph distances are $|i - j|$, and Isomap returns five equally spaced points on a line. The [Isomap](/isomap/) page works through the numbers.
- **Images of one object.** Tenenbaum et al. (2000) used images of a face that change in pose and lighting, and found the pose angles and the lighting direction as the coordinates. Roweis and Saul (2000) used images of faces and words in a document collection.
- **A flat sheet with a hole.** A flat rectangle with a square removed, isometrically bent into $\mathbb{R}^3$. Isomap distorts the result because its geodesics go around the hole. Hessian eigenmaps and LTSA recover the flat coordinates, because they only use local geometry.

## Where it is used

- **Visualization.** A 2D or 3D map of data such as images, gene expression profiles or documents. For this use, neighbor embeddings such as [t-SNE](/t-sne/) and [UMAP](/umap/) have mostly replaced the spectral methods, and [trustworthiness and continuity](/trustworthiness-and-continuity/) measure how well a map keeps neighborhoods.
- **Feature extraction.** The coordinates are inputs to a classifier or a regression model, for example in face recognition with [locality preserving projections](/locality-preserving-projections/).
- **Semi-supervised learning.** The graph Laplacian of the data, as in [Laplacian eigenmaps](/laplacian-eigenmaps/), defines smooth functions on the data and spreads labels along the manifold.
- **Clustering.** [Spectral clustering](/spectral-clustering/) uses the same eigenvectors as Laplacian eigenmaps and then runs k-means on them.
- **Scientific data.** Diffusion maps find slow variables in molecular dynamics and reaction coordinates in chemical systems.

## References
