---
tag: R90KN4
kind: technique
slug: random-projection
name: Random projection
aliases:
- random projection method
- Gaussian random projection
area: machine-learning/dimensionality-reduction
level: core
summary: "Reduce dimension by multiplying the data with a random matrix that approximately preserves distances."
prereqs: [johnson-lindenstrauss-lemma, variance]
see_also: [sparse-random-projection, fast-johnson-lindenstrauss-transform, principal-component-analysis, randomized-pca, random-hyperplane-lsh, count-sketch, restricted-isometry-property, approximate-nearest-neighbor-search]
sources:
  - paper: doi:10.1145/502512.502546
    title: Ella Bingham and Heikki Mannila, Random projection in dimensionality reduction, applications to image and text data, Proceedings of the 7th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD), 2001, pages 245 to 250
    locator: the experiments that compare random projection, sparse random projection, PCA and the discrete cosine transform on image and text data
  - paper: doi:10.1016/S0022-0000(03)00025-4
    title: Dimitris Achlioptas, Database-friendly random projections, Johnson-Lindenstrauss with binary coins, Journal of Computer and System Sciences 66(4), 2003, pages 671 to 687
    locator: Theorem 1.1 (entries +1 or -1 with probability 1/2 each, or sqrt(3) times +1, 0, -1 with probabilities 1/6, 2/3, 1/6, and k >= (4 + 2 beta)(eps^2/2 - eps^3/3)^(-1) log n)
  - paper: doi:10.1002/rsa.10073
    title: Sanjoy Dasgupta and Anupam Gupta, An elementary proof of a theorem of Johnson and Lindenstrauss, Random Structures and Algorithms 22(1), 2003, pages 60 to 65
    locator: Theorem 2.1 (the bound on k for a Gaussian projection)
  - paper: doi:10.1137/090771806
    title: Nathan Halko, Per-Gunnar Martinsson and Joel A. Tropp, Finding structure with randomness, probabilistic algorithms for constructing approximate matrix decompositions, SIAM Review 53(2), 2011, pages 217 to 288
    locator: Section 4 (the randomized range finder, a random projection of the column space)
  - paper: "Tamás Sarlós, Improved approximation algorithms for large matrices via random projections, Proceedings of the 47th IEEE Symposium on Foundations of Computer Science (FOCS), 2006, pages 143 to 152"
    locator: the sketched least squares regression with a Johnson-Lindenstrauss transform
---

Random projection reduces the dimension of data by multiplying each point by one random matrix. Each new coordinate is a random linear combination of the old coordinates. By the [Johnson-Lindenstrauss lemma](/johnson-lindenstrauss-lemma/), $k = O(\varepsilon^{-2} \log n)$ new coordinates keep all pairwise distances among $n$ points within a factor $1 \pm \varepsilon$, whatever the input dimension $d$. The matrix does not depend on the data, so the method needs no training, works on streams, and costs one matrix product. Bingham and Mannila (2001) showed that it works well on real image and text data, and Achlioptas (2003) showed that the entries can be simple $\pm 1$ values.

## In plain words

You have points with very many coordinates and you want fewer coordinates. Make a table of random numbers with one row for each old coordinate and one column for each new coordinate. To get the new coordinates of a point, take a weighted sum of its old coordinates for each column, with the random numbers as weights, and scale the result.

Use the same table for every point, including points that come later. Distances between points then stay almost the same, with high probability. The table never looks at the data, so you can make it before the data exist.

## When it applies

- **Euclidean geometry is what matters.** The downstream method uses Euclidean distances or inner products: [nearest neighbor search](/approximate-nearest-neighbor-search/), [k-means](/k-means/), kernel machines with a linear or RBF kernel, least squares, linear classifiers.
- **The input dimension is large compared with $\log n$.** The guarantee needs $k \approx 8 \varepsilon^{-2} \ln n$; there is no gain unless $d$ is much larger than that.
- **A worst-case promise is wanted.** The bound holds for every pair, for every data set, with high probability over the matrix only.
- **The data cannot be seen in advance.** Streams, distributed data, privacy settings and sketches need a map that is fixed before the data arrive.
- **Training a data-dependent map is too expensive.** [Principal component analysis](/principal-component-analysis/) needs a decomposition of a $d \times d$ matrix or of the data; random projection needs only a matrix product.

## The template

Input: an $n \times d$ data matrix $X$ (one point per row), a target dimension $k$, and an entry distribution $\mathcal{D}$ with mean 0 and variance 1.

1. Choose $k$. For a guarantee on all pairs, take $k \ge (4 + 2\beta)(\varepsilon^2/2 - \varepsilon^3/3)^{-1} \ln n$; then all pairs are within $1 \pm \varepsilon$ with probability at least $1 - n^{-\beta}$. In practice, $k$ is often set by validation of the downstream task.
2. Draw a $d \times k$ matrix $R$ with independent entries from $\mathcal{D}$, or store a seed and make the entries again when needed.
3. Output $Y = X R / \sqrt{k}$. A new point $x$ maps to $x R / \sqrt{k}$ with the same $R$.
4. Run the downstream method on $Y$.

The common choices for $\mathcal{D}$:

| name | entries | source |
|---|---|---|
| Gaussian | $N(0, 1)$ | Indyk and Motwani 1998, Dasgupta and Gupta 2003 |
| Rademacher | $+1$ or $-1$, each with probability $1/2$ | Achlioptas 2003 |
| Achlioptas sparse | $\sqrt{3} \cdot (+1, 0, -1)$ with probabilities $1/6, 2/3, 1/6$ | Achlioptas 2003 |

**Why it works.** For one fixed vector $x$ and one column $r$ of $R$, the value $\langle x, r \rangle$ has mean 0 and $\mathbb{E}\langle x, r \rangle^2 = \sum_j x_j^2 \mathbb{E} r_j^2 = \|x\|^2$, because the cross terms have mean 0. So $\|x R\|^2 / k$ is an average of $k$ independent unbiased estimates of $\|x\|^2$. The variance of one estimate is

$$\operatorname{Var} \langle x, r \rangle^2 = 2\|x\|^4 + (\mathbb{E} r_j^4 - 3) \sum_j x_j^4 .$$

The fourth moment is 3 for the Gaussian and the Achlioptas sparse entries, and 1 for Rademacher entries, so Rademacher entries never have a larger variance than Gaussian entries. For $x = (1, 2, -2, 0)$ with $\|x\|^2 = 9$ and $\sum x_j^4 = 33$, one Rademacher column gives variance $162 - 66 = 96$, and one Gaussian column gives 162. Averaging over $k$ columns divides the variance by $k$. Concentration bounds of the [Chernoff](/chernoff-bound/) type then give the $e^{-\Omega(k \varepsilon^2)}$ tails behind the lemma, and a union bound over the pairs finishes the argument.

**Inner products.** The same map estimates inner products: $\mathbb{E}\langle x R, y R \rangle / k = \langle x, y \rangle$. One Gaussian column has variance $\|x\|^2 \|y\|^2 + \langle x, y \rangle^2$; one Rademacher column has variance $\|x\|^2 \|y\|^2 + \langle x, y \rangle^2 - 2 \sum_j x_j^2 y_j^2$. The error is additive, of order $\|x\| \|y\| / \sqrt{k}$.

**Cost.** Making $Y$ takes $O(ndk)$ time for dense $X$ and $O(k \cdot \mathrm{nnz}(X))$ for sparse $X$. The matrix takes $dk$ numbers, or one seed.

## Classic examples

- **Image and text data (Bingham and Mannila 2001).** On image windows and on term-document data, random projection kept pairwise distances and inner products with small error. It was close to PCA in accuracy and much faster, and the sparse Achlioptas matrix was as accurate as the dense Gaussian one.
- **Approximate nearest neighbors (Indyk and Motwani 1998).** Project to $O(\varepsilon^{-2} \log n)$ dimensions and search there; a $(1 + \varepsilon)$-approximate neighbor in the small space is a $(1 + O(\varepsilon))$-approximate neighbor in the original space. See [approximate nearest neighbor](/approximate-nearest-neighbor/).
- **Randomized low-rank approximation.** Multiply a matrix $A$ by a random $d \times (r + p)$ matrix to get a sketch of its column space, then compute an SVD of the small matrix. This is the randomized range finder of Halko, Martinsson and Tropp and the base of [randomized PCA](/randomized-pca/).
- **Sketching least squares (Sarlós 2006).** Replace $\min_x \|Ax - b\|$ by $\min_x \|S(Ax - b)\|$ for a random projection $S$ with few rows; the solution is within $1 + \varepsilon$ of the optimum.
- **Compressed sensing.** A random Gaussian or $\pm 1$ matrix with $O(s \log(d/s))$ rows has the [restricted isometry property](/restricted-isometry-property/) with high probability, which lets $s$-sparse signals be recovered from the projection; see [compressed sensing](/compressed-sensing/).
- **Sign random projection.** Keep only the sign of each projected coordinate. The fraction of sign agreements estimates the angle between two vectors; this is [random hyperplane LSH](/random-hyperplane-lsh/) and [SimHash](/simhash/).

## Variations

- **Random subspace.** The original map of Johnson and Lindenstrauss projects onto a uniformly random $k$-dimensional subspace and scales by $\sqrt{d/k}$. It has orthonormal rows, which is better when $k$ is close to $d$, but it costs a QR decomposition.
- **[Sparse random projection](/sparse-random-projection/).** Most entries are 0: two thirds for Achlioptas, $1 - 1/\sqrt{d}$ for the very sparse projection of Li, Hastie and Church, and only $s$ nonzeros per column of the transpose in the sparse JL transform of Kane and Nelson. The cost per point drops by the same factor.
- **[Fast Johnson-Lindenstrauss transform](/fast-johnson-lindenstrauss-transform/).** First spread the mass of $x$ with a random sign flip and a Walsh-Hadamard transform, then apply a sparse or sampling matrix. The cost per point is about $O(d \log d)$ instead of $O(dk)$.
- **[Count sketch](/count-sketch/) and feature hashing.** Each input coordinate goes to one output coordinate with a random sign. This is the sparsest case, $s = 1$; it keeps norms of vectors without large single coordinates.
- **Data-dependent maps.** When the data lie close to a low-dimensional subspace, [PCA](/principal-component-analysis/) gives a smaller error for the same $k$. Random projection is often a cheap first step before PCA.

## Pitfalls

- **Missing scale.** Without the factor $1/\sqrt{k}$ all squared distances grow by a factor $k$. Ratios and nearest neighbors stay the same, but distance thresholds and kernel widths break.
- **A different matrix for new points.** Training points and query points must use the same $R$. Store the matrix or its seed with the model.
- **Expecting a gain at small $d$.** For $n = 10^6$ and $\varepsilon = 0.2$ the guarantee asks for $k = 3189$. If $d$ is a few hundred, the projection gives no gain. The bound is worst case; on real data smaller $k$ often works, which must then be checked.
- **Relative error on distances, additive error on inner products.** Inner products of almost orthogonal vectors have errors as large as $\|x\| \|y\| / \sqrt{k}$, so small cosine similarities are noisy.
- **Wrong geometry.** The guarantee is for Euclidean distances only. Distances in $\ell_1$, edit distance or other metrics are not preserved.
- **Sparse inputs become dense.** A dense $R$ turns a sparse $x$ into a dense $k$-vector. Use a sparse $R$, or accept the memory.
- **Low-quality random numbers.** Correlated or periodic generators break the independence that the proof needs. Use a good generator, or a family of hash functions with enough independence for the analysis that is used.

## Exercises

1. Show that $\mathbb{E}\, \|x R\|^2 / k = \|x\|^2$ for any entry distribution with mean 0 and variance 1. Which property of the entries does the proof use besides the first two moments?
2. Prove the variance formula $\operatorname{Var} \langle x, r \rangle^2 = 2\|x\|^4 + (\mu_4 - 3)\sum_j x_j^4$, where $\mu_4 = \mathbb{E} r_j^4$. Check it for $x = (1, 2, -2, 0)$ with Rademacher entries.
3. Show that the Achlioptas sparse distribution has the same first four moments as $N(0, 1)$ in the sense used by exercise 2. Why does that make its variance equal to the Gaussian one?
4. Find the least $k$ of the template for $n = 10^6$, $\varepsilon = 0.2$ and $\beta = 0$. (Answer: 3189.)
5. Let $x = e_1$, a vector with one nonzero coordinate. What is the law of $\|x R\|^2 / k$ for Rademacher entries? What does this say about very sparse matrices on such vectors?

## References
