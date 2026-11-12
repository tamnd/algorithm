---
tag: TQZ5JY
kind: definition
slug: intrinsic-dimension
name: Intrinsic dimension
aliases:
- intrinsic dimension of data
area: machine-learning/dimensionality-reduction
level: core
summary: "The minimal number of coordinates needed to describe data without significant loss."
prereqs: [metric-space]
see_also: [intrinsic-dimension-estimation, manifold-hypothesis, intrinsic-dimensionality, curse-of-dimensionality, principal-component-analysis, manifold-learning, embedding, cover-tree]
sources:
  - paper: doi:10.1103/PhysRevLett.50.346
    title: Peter Grassberger and Itamar Procaccia, Characterization of strange attractors, Physical Review Letters 50(5), 1983, pages 346 to 349
    locator: the correlation integral C(r) and the correlation exponent nu defined by C(r) ~ r^nu
  - paper: "Peter Grassberger and Itamar Procaccia, Measuring the strangeness of strange attractors, Physica D 9(1-2), 1983, pages 189 to 208"
    locator: the inequalities between the correlation exponent, the information dimension and the capacity (box-counting) dimension
  - paper: doi:10.1109/SFCS.2003.1238226
    title: Anupam Gupta, Robert Krauthgamer and James R. Lee, Bounded geometries, fractals, and low-distortion embeddings, Proceedings of the 44th IEEE Symposium on Foundations of Computer Science (FOCS), 2003, pages 534 to 543
    locator: the definition of the doubling dimension of a metric space
  - book: "Kenneth Falconer, Fractal Geometry, Mathematical Foundations and Applications, 3rd edition, Wiley, 2014"
    locator: Chapter 2 (Hausdorff dimension) and Chapter 3 (box-counting dimension and its relation to the Hausdorff dimension)
  - book: isbn:9780387393506
    title: John A. Lee and Michel Verleysen, Nonlinear Dimensionality Reduction, Springer, 2007
    locator: Chapter 3 (the definitions of intrinsic dimension, the capacity, information and correlation dimensions, and their estimators)
---

The intrinsic dimension of a data set is the number of coordinates that are really needed to describe it, as opposed to the number of coordinates it is given in. Images with $10^4$ pixels that vary only by the angle of a rotating object have intrinsic dimension 1. There is no single definition. The topological dimension counts the degrees of freedom of a set, the box-counting and correlation dimensions measure how the number of points within distance $r$ grows with $r$, and the doubling dimension measures how many small balls cover a large one. For a smooth $m$-dimensional manifold with a well-behaved measure all of these give $m$; for fractals, noisy data and finite samples they can differ, and the answer depends on the scale. The page [intrinsic dimension estimation](/intrinsic-dimension-estimation/) covers how to measure it from data.

## Definition

Let $A$ be a subset of a [metric space](/metric-space/) $(X, \rho)$, usually $\mathbb{R}^D$ with the Euclidean distance, and let $\mu$ be a probability measure on $A$ that models how data points are drawn. Write $B(x, r) = \{y : \rho(x, y) < r\}$.

**Manifold dimension.** If $A$ is a submanifold of $\mathbb{R}^D$ (every point has a neighborhood in $A$ that is homeomorphic to an open set of $\mathbb{R}^m$), its intrinsic dimension is $m$. The ambient dimension $D$ plays no role.

**Topological (covering) dimension.** $\dim_T A$ is the least $m$ such that every finite open cover of $A$ has a refinement in which no point lies in more than $m + 1$ sets. It is an integer, it is invariant under homeomorphisms, and it equals $m$ for an $m$-manifold.

**Box-counting dimension.** Let $N(r)$ be the least number of sets of diameter at most $r$ that cover a bounded set $A$. Then

$$\dim_B A = \lim_{r \to 0} \frac{\ln N(r)}{\ln(1/r)},$$

when the limit exists; otherwise the upper and lower box-counting dimensions use $\limsup$ and $\liminf$. The value can be a fraction. The Hausdorff dimension $\dim_H$ is a refinement that allows sets of different sizes in the cover; always $\dim_T A \le \dim_H A \le \underline{\dim}_B A$.

**Correlation dimension (Grassberger and Procaccia 1983).** For independent $X, X'$ with law $\mu$, the correlation integral is $C(r) = \Pr[\rho(X, X') < r]$, and

$$\nu = \lim_{r \to 0} \frac{\ln C(r)}{\ln r}.$$

For a sample $x_1, \ldots, x_N$, the sample version is $C_N(r) = \frac{2}{N(N-1)} \#\{i < j : \rho(x_i, x_j) < r\}$, the fraction of pairs closer than $r$. Grassberger and Procaccia showed that $\nu$ is at most the information dimension, which is at most the box-counting dimension, with equality for a uniform measure on a nice set.

**Local (pointwise) dimension.** At a point $x$ in the support of $\mu$,

$$m(x) = \lim_{r \to 0} \frac{\ln \mu(B(x, r))}{\ln r},$$

so that $\mu(B(x, r)) \approx c(x)\, r^{m(x)}$ for small $r$. Nearest neighbor estimators such as the one of Levina and Bickel and TwoNN estimate this quantity, under the assumption that the density is about constant on small balls.

**Doubling dimension.** The doubling constant $\lambda$ of $(A, \rho)$ is the least number such that every ball of radius $2r$ in $A$ is covered by $\lambda$ balls of radius $r$, for every $r$. The doubling dimension is $\log_2 \lambda$. It is defined for any metric space, at all scales at once, and it governs the cost of search structures such as the [cover tree](/cover-tree/); see [intrinsic dimensionality](/intrinsic-dimensionality/) for its use in similarity search.

**Linear dimension.** The least $m$ such that $A$ lies in an affine subspace of dimension $m$ (or such that the first $m$ principal components explain a chosen fraction of the variance). This is what [principal component analysis](/principal-component-analysis/) measures. It is an upper bound on the other notions for a manifold and can be much larger than them.

## Examples and non-examples

- **A segment, a square, a cube.** A segment in $\mathbb{R}^D$ has every dimension above equal to 1. The unit square placed by an isometry in $\mathbb{R}^{10}$ has dimension 2 in every sense; with the uniform measure, $C(r) \approx \pi r^2$ for small $r$, so $\nu = 2$. The value does not depend on the $10$.
- **A circle.** The unit circle in $\mathbb{R}^2$ has topological, box-counting and correlation dimension 1, but linear dimension 2: no line contains it. Curved data is the main reason why PCA overestimates the intrinsic dimension.
- **The Swiss roll.** A rectangle rolled up in $\mathbb{R}^3$ is a 2-dimensional manifold. PCA reports 3, because the roll fills a 3-dimensional box. [Manifold learning](/manifold-learning/) methods such as [Isomap](/isomap/) recover the 2 coordinates.
- **Rotations of one image.** Images of a fixed object turned through all angles form a closed curve in pixel space: intrinsic dimension 1, ambient dimension the number of pixels.
- **The middle-thirds Cantor set.** Topological dimension 0, box-counting and Hausdorff dimension $\ln 2 / \ln 3 \approx 0.631$. At scale $r = 3^{-j}$ it needs $N(r) = 2^j$ intervals.
- **The Koch curve.** Topological dimension 1, box-counting dimension $\ln 4 / \ln 3 \approx 1.262$.
- **Euclidean space and doubling.** In $\mathbb{R}^m$ a ball of radius $2r$ needs at least $2^m$ balls of radius $r$ (compare volumes), and $5^m$ suffice (a maximal set of points at mutual distance at least $r$ inside it has at most $5^m$ points, by packing balls of radius $r/2$ in a ball of radius $5r/2$). So the doubling dimension of $\mathbb{R}^m$ lies between $m$ and $m \log_2 5 \approx 2.32 m$.
- **Non-example: a finite sample at $r \to 0$.** Every finite set has box-counting, correlation and local dimension 0, because for $r$ below the least distance nothing changes. The definitions are about the set or measure that the sample comes from; estimators must use a range of scales that is small compared with the curvature but large compared with the spacing of the points.
- **Non-example: noise.** A square in $\mathbb{R}^{10}$ with independent Gaussian noise of standard deviation $\sigma$ in all 10 coordinates has, strictly, dimension 10. At scales well above $\sigma$ it looks 2-dimensional, at scales below $\sigma$ 10-dimensional. The useful answer, 2, is a statement about a range of scales, not a limit.
- **Non-example: a space-filling curve.** The image of a Peano curve in the square has topological dimension 2, not 1, although it is the continuous image of a segment. Dimension is invariant under homeomorphisms, not under all continuous maps.

## Related definitions

- [Manifold hypothesis](/manifold-hypothesis/): the assumption that real high-dimensional data lie near a manifold of low intrinsic dimension.
- [Intrinsic dimension estimation](/intrinsic-dimension-estimation/): the problem of computing the value from a sample.
- [Intrinsic dimensionality](/intrinsic-dimensionality/) (similarity search): the doubling dimension, the expansion constant, and the ratio of mean to variance of distances, as measures of the cost of search.
- [Curse of dimensionality](/curse-of-dimensionality/): the sample sizes and search costs that grow exponentially, in the intrinsic dimension rather than the ambient one when the data have structure.
- [Embedding](/embedding/): a map into a space of lower dimension; the intrinsic dimension is a lower limit on the target dimension of a faithful embedding.
- [VC dimension](/vc-dimension/): a different notion, the capacity of a class of functions, not the dimension of the data.

## References
