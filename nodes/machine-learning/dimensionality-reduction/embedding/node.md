---
tag: GV9TQA
kind: definition
slug: embedding
name: Embedding
aliases:
- embedding map
- metric embedding
- low-distortion embedding
area: machine-learning/dimensionality-reduction
level: intro
summary: "A mapping of points into a space, usually lower-dimensional, that preserves chosen structure."
prereqs: [metric-space]
see_also: [johnson-lindenstrauss-lemma, trustworthiness-and-continuity, metric-tree-embedding, node-embedding, multidimensional-scaling, manifold-hypothesis, sparsest-cut-problem, intrinsic-dimension]
sources:
  - paper: doi:10.1007/BF02776078
    title: Jean Bourgain, On Lipschitz embedding of finite metric spaces in Hilbert space, Israel Journal of Mathematics 52(1-2), 1985, pages 46 to 52
    locator: the theorem that every n-point metric space embeds into Hilbert space with distortion O(log n), by distances to random subsets
  - paper: doi:10.1007/BF01200757
    title: Nathan Linial, Eran London and Yuri Rabinovich, The geometry of graphs and some of its algorithmic applications, Combinatorica 15(2), 1995, pages 215 to 245
    locator: the randomized algorithm for Bourgain's embedding into O(log^2 n) dimensions, and the Omega(log n) lower bound for expander graphs
  - book: isbn:9780387953731
    title: Jiří Matoušek, Lectures on Discrete Geometry, Graduate Texts in Mathematics 212, Springer, 2002
    locator: Chapter 15 (embedding finite metric spaces into normed spaces; Section 15.1 on distortion, Section 15.5 on the lower bound via expanders, Section 15.7 on Bourgain's theorem)
  - paper: doi:10.1090/conm/026/737400
    title: William B. Johnson and Joram Lindenstrauss, Extensions of Lipschitz mappings into a Hilbert space, Contemporary Mathematics 26, 1984, pages 189 to 206
    locator: the dimension reduction lemma for n points of Hilbert space
---

An embedding is a map that places the objects of one space into another space, usually a simpler or lower-dimensional one, so that some chosen structure survives. In dimensionality reduction the objects are data points and the structure is the distances or the neighborhoods between them; in topology it is the shape of the space; in machine learning practice it is often a learned vector for each word, item or graph node. The standard measure of quality for distances is the distortion: the factor by which the map can stretch one distance relative to another. Two results set the scale: the [Johnson-Lindenstrauss lemma](/johnson-lindenstrauss-lemma/) embeds $n$ Euclidean points into $O(\varepsilon^{-2}\log n)$ dimensions with distortion $1 + \varepsilon$, and Bourgain's theorem (1985) embeds any $n$-point metric space into Euclidean space with distortion $O(\log n)$.

## Definition

**Metric embedding.** Let $(X, \rho)$ and $(Y, \sigma)$ be [metric spaces](/metric-space/). A map $f : X \to Y$ is an embedding with distortion at most $\alpha \ge 1$ if there is a scale $c > 0$ such that for all $x, x' \in X$

$$c\, \rho(x, x') \;\le\; \sigma\big(f(x), f(x')\big) \;\le\; \alpha\, c\, \rho(x, x').$$

The distortion of $f$ is the least such $\alpha$. Equivalently, it is the product of the expansion $\max \sigma(f(x), f(x')) / \rho(x, x')$ and the contraction $\max \rho(x, x') / \sigma(f(x), f(x'))$, over pairs $x \ne x'$. A map with distortion 1 is an isometry up to scale. A map that sends two points to the same place has infinite distortion and is not an embedding. For a finite metric space $X$, $c_2(X)$ is the least distortion of an embedding of $X$ into a Euclidean space of any dimension.

**Topological and smooth embedding.** A continuous map $f : M \to Y$ is a (topological) embedding if it is a homeomorphism from $M$ onto its image $f(M)$. A smooth map of manifolds is a smooth embedding if it is a topological embedding and its derivative is injective at every point. By the Whitney embedding theorem, every smooth $m$-dimensional manifold has a smooth embedding into $\mathbb{R}^{2m}$.

**Embedding in data analysis.** Given points $x_1, \ldots, x_n$ in $\mathbb{R}^D$ or in a metric space, an embedding is a list of points $y_1, \ldots, y_n \in \mathbb{R}^k$, often with $k$ much smaller than $D$, with $y_i$ the image of $x_i$. Some methods give a map $f$ that applies to new points ([PCA](/principal-component-analysis/), [random projection](/random-projection/)); others give only the $y_i$ ([t-SNE](/t-sne/), [MDS](/multidimensional-scaling/)). Quality is measured by the distortion, by a stress function of the distances, or by rank measures of neighborhoods such as [trustworthiness and continuity](/trustworthiness-and-continuity/).

**Bourgain's theorem (1985).** Every metric space with $n$ points has an embedding into Euclidean space with distortion $O(\log n)$. The construction: for each scale $j = 1, \ldots, \lceil \log_2 n \rceil$ and each of $O(\log n)$ repetitions, choose a random subset $S$ that contains each point with probability $2^{-j}$, and use the coordinate $x \mapsto \rho(x, S)$, the distance to the nearest point of $S$. Each coordinate is 1-Lipschitz, and for every pair some scale separates the two points by a fair share of their distance. Linial, London and Rabinovich (1995) showed that this gives $O(\log^2 n)$ dimensions with high probability, and that $O(\log n)$ is the best possible distortion: the shortest path metrics of constant-degree expander graphs have $c_2(X) = \Omega(\log n)$.

## Examples and non-examples

- **Subspaces and rotations.** The inclusion of $\mathbb{R}^m$ in $\mathbb{R}^D$, a rotation, and a translation are isometric embeddings: distortion 1.
- **Points in Euclidean space.** Any $n$ points of a Euclidean space lie in an affine subspace of dimension $n - 1$, so they embed isometrically into $\mathbb{R}^{n-1}$. The [Johnson-Lindenstrauss lemma](/johnson-lindenstrauss-lemma/) lowers the dimension to $O(\varepsilon^{-2}\log n)$ at distortion $\sqrt{(1+\varepsilon)/(1-\varepsilon)} = 1 + O(\varepsilon)$, and this dimension is the best possible ([Johnson-Lindenstrauss optimality](/johnson-lindenstrauss-optimality/)).
- **The 4-cycle needs distortion $\sqrt{2}$.** Let $X$ be the cycle $a, b, c, d$ with edges of length 1, so the two diagonals have length 2. For any four points of a Euclidean space, $\|a - b\|^2 + \|b - c\|^2 + \|c - d\|^2 + \|d - a\|^2 - \|a - c\|^2 - \|b - d\|^2 = \|a - b + c - d\|^2 \ge 0$ (expand both sides). If an embedding does not shrink any distance and stretches each by at most $\alpha$, the diagonals give at least $4 + 4 = 8$ and the edges at most $4\alpha^2$, so $\alpha \ge \sqrt{2}$. The corners of a unit square attain it: edges stay 1 and diagonals become $\sqrt{2}$ instead of 2.
- **A star with three leaves.** Let a center be at distance 1 from three leaves that are at distance 2 from each other. In a Euclidean space, a point at distance 1 from two points at distance 2 must be their midpoint, and one point cannot be the midpoint of three different pairs. So this tree has no isometric embedding into any Euclidean space, though it embeds isometrically into $\ell_1$, like every tree metric.
- **Trees and tree embeddings.** [Metric tree embedding](/metric-tree-embedding/) goes the other way: it maps a metric into a random tree with expected distortion $O(\log n)$ ([FRT tree embedding](/frt-tree-embedding/)), which makes many problems easy to solve on the tree.
- **Graph node embeddings.** [Node embedding](/node-embedding/) methods map the nodes of a graph to vectors so that nearby or similar nodes get nearby vectors. They are embeddings in the data-analysis sense; their quality is judged by downstream tasks, not by a distortion bound.
- **A neighbor embedding.** [t-SNE](/t-sne/) and [UMAP](/umap/) output points in the plane that keep local neighborhoods but freely change large distances. Their distortion is usually large; they are measured by neighborhood preservation instead.
- **Non-example: a projection that collapses points.** Projecting the points $(0, 0)$ and $(0, 1)$ onto the first coordinate sends both to 0. The result is not an embedding of those points, whatever the quality of the other distances.
- **Non-example: dimension reduction in $\ell_1$.** There is no analogue of the Johnson-Lindenstrauss lemma for $\ell_1$: Brinkman and Charikar (2005) found $n$-point subsets of $\ell_1$ that need dimension $n^{\Omega(1/\alpha^2)}$ for distortion $\alpha$.

## Related definitions

- **Bi-Lipschitz map:** a map whose expansion and contraction are both finite; on a finite set every injective map is bi-Lipschitz, and the distortion is the product of the two constants.
- **Isometry:** distortion 1 with scale 1.
- **[Manifold hypothesis](/manifold-hypothesis/):** the assumption that data are the image of a low-dimensional manifold under an embedding into $\mathbb{R}^D$.
- **[Intrinsic dimension](/intrinsic-dimension/):** a lower limit on the target dimension of a faithful embedding of a set.
- **[Trustworthiness and continuity](/trustworthiness-and-continuity/):** rank-based measures of how an embedding keeps neighborhoods, for maps where the distortion is not meaningful.
- **[Sparsest cut](/sparsest-cut-problem/):** the problem where Linial, London and Rabinovich used Bourgain's embedding, through $\ell_1$, for an $O(\log n)$ approximation.

## References
