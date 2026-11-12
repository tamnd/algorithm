---
tag: J2JFH9
kind: algorithm
slug: sparse-random-projection
name: Sparse random projection
aliases:
- Achlioptas projection
- database-friendly random projection
- very sparse random projection
- sparse Johnson-Lindenstrauss transform
area: machine-learning/dimensionality-reduction
level: advanced
summary: "A random projection whose matrix is mostly zeros, with entries +-sqrt(s) at density 1/s; it keeps distances like a Gaussian one at a fraction of the cost."
model: real-ram
complexity:
  vars: {d: the input dimension, k: the target dimension, s: the inverse of the density, "nnz(x)": the number of nonzero coordinates of the point}
  time:
    worst: "O(d k / s)"
  space:
    extra: "O(d k / s)"
properties:
  deterministic: false
  exact: false
  online: true
  recursive: false
history:
  year: 2003
  people: [Dimitris Achlioptas]
  note: "Achlioptas proved the Johnson-Lindenstrauss guarantee for +-1 entries and for a matrix with two thirds zeros; Li, Hastie and Church (2006) took the density down to 1/sqrt(d), and Kane and Nelson (2014) gave s nonzeros per column."
prereqs: [random-projection, johnson-lindenstrauss-lemma, variance]
see_also: [fast-johnson-lindenstrauss-transform, count-sketch, linear-sketch, ams-sketch, k-wise-independence, random-hyperplane-lsh, principal-component-analysis]
sources:
  - paper: doi:10.1016/S0022-0000(03)00025-4
    title: Dimitris Achlioptas, Database-friendly random projections, Johnson-Lindenstrauss with binary coins, Journal of Computer and System Sciences 66(4), 2003, pages 671 to 687
    locator: Theorem 1.1 (the two distributions, k >= (4 + 2 beta)(eps^2/2 - eps^3/3)^(-1) log n, success probability at least 1 - n^(-beta)) and the moment comparison with the Gaussian
  - paper: doi:10.1145/1150402.1150436
    title: Ping Li, Trevor J. Hastie and Kenneth W. Church, Very sparse random projections, Proceedings of the 12th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD), 2006, pages 287 to 296
    locator: the very sparse matrix with s = sqrt(d), the exact variances of the norm and inner product estimators, and the asymptotic normality
  - paper: doi:10.1145/2559902
    title: Daniel M. Kane and Jelani Nelson, Sparser Johnson-Lindenstrauss transforms, Journal of the ACM 61(1), 2014, Article 4
    locator: the block construction with s = O(eps^-1 log(1/delta)) nonzeros per column and k = O(eps^-2 log(1/delta)) rows
  - paper: doi:10.1145/502512.502546
    title: Ella Bingham and Heikki Mannila, Random projection in dimensionality reduction, applications to image and text data, Proceedings of the 7th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD), 2001, pages 245 to 250
    locator: the experiments with the sparse matrix of Achlioptas on image and text data
---

Sparse random projection is a [random projection](/random-projection/) in which most entries of the random matrix are zero. Each entry is $+\sqrt{s}$ or $-\sqrt{s}$ with probability $1/(2s)$ each, and 0 otherwise. Achlioptas (2003) proved that $s = 1$ (random signs) and $s = 3$ (two thirds zeros) keep the full [Johnson-Lindenstrauss](/johnson-lindenstrauss-lemma/) guarantee with the same target dimension as a Gaussian matrix. Li, Hastie and Church (2006) used $s = \sqrt{d}$, which makes the cost per point $\sqrt{d}$ times smaller and works well when no single coordinate dominates a vector. Kane and Nelson (2014) gave a different sparse construction with exactly $s$ nonzeros per input coordinate and a guarantee for every vector.

## In plain words

A random projection makes new coordinates as random weighted sums of the old ones. Here most weights are zero, so each new coordinate is a sum over only a few old coordinates, with random signs. The few weights that are not zero are made larger, so that on average lengths stay the same.

With one third of the weights not zero, the result is as good as with Gaussian weights, and the work is three times smaller. With far fewer weights not zero, the work is much smaller still, but a point whose length sits in one or two coordinates can be missed by every sum, so its length is badly estimated.

## The problem

Input: $n$ points $x_1, \ldots, x_n \in \mathbb{R}^d$ (rows of a matrix $X$), a target dimension $k$, and an accuracy $\varepsilon \in (0, 1)$.
Output: points $y_1, \ldots, y_n \in \mathbb{R}^k$ with $y_i = f(x_i)$ for a linear map $f$, such that with high probability

$$(1 - \varepsilon) \|x_i - x_j\|^2 \le \|y_i - y_j\|^2 \le (1 + \varepsilon) \|x_i - x_j\|^2 \quad\text{for all } i, j.$$

The map must be chosen without looking at the points, and computing $f(x)$ should cost much less than the $dk$ operations of a dense matrix.

## The algorithm

```pseudo id=main
SPARSE-RANDOM-PROJECTION(x_1..x_n ∈ ℝ^d, k, s)
L1  for j ← 1 to k do                                ▷ draw column j of R
L2      C_j ← empty list
L3      for i ← 1 to d do
L4          u ← uniform number in [0, 1)
L5          if u < 1/(2s) then append (i, +1) to C_j
L6          else if u < 1/s then append (i, −1) to C_j
L7  for each point x do
L8      for j ← 1 to k do
L9          y_j ← √(s/k) · Σ_{(i, σ) ∈ C_j} σ · x_i
L10     output y
```

Lines L1 to L6 draw the $d \times k$ matrix $R$ with $R_{ij} = \sigma \sqrt{s}$ for each stored pair $(i, \sigma)$ and $R_{ij} = 0$ otherwise. Only the nonzero entries are stored, as signs; the scale $\sqrt{s}$ and the factor $1/\sqrt{k}$ are applied once in line L9. So $y = x R / \sqrt{k}$. The choice of $s$ names the method:

| $s$ | nonzero fraction | name |
|---|---|---|
| 1 | 1 | Rademacher (random sign) projection |
| 3 | 1/3 | Achlioptas sparse projection |
| $\sqrt{d}$ | $1/\sqrt{d}$ | very sparse projection (Li, Hastie and Church) |

**The block construction (Kane and Nelson).** Choose $k = b s$ and split the $k$ output coordinates into $s$ blocks of $b$. For each input coordinate $i$ and each block, choose one row of the block uniformly and one random sign $\sigma$, and set that entry to $\sigma / \sqrt{s}$. Every column of this $k \times d$ matrix $S$ has exactly $s$ nonzeros, and $f(x) = S x$ costs $O(s \cdot \mathrm{nnz}(x))$. With $s = 1$ this is the [count sketch](/count-sketch/) matrix.

## Example

Take $x = (1, 2, -2, 0)$, so $\|x\|^2 = 9$ and $\sum_i x_i^4 = 1 + 16 + 16 = 33$. One output coordinate $y_1 = \langle x, r \rangle$ (with $k = 1$) estimates $\|x\|^2$ by $y_1^2$. The exact variance of this estimate is $2\|x\|^4 + (s - 3) \sum_i x_i^4$ (see Correctness):

| $s$ | variance of $y_1^2$ |
|---|---|
| 1 | $162 - 66 = 96$ |
| 3 | $162$ (the same as a Gaussian column) |
| 4 | $162 + 33 = 195$ |

With $k$ output coordinates the variance is divided by $k$.

For a spike, $x = e_1$, the variance is $2 + (s - 3) = s - 1$. With $s = 3$ it is 2, as for a Gaussian. With $s = \sqrt{d} = 100$ for $d = 10^4$ it is 99, about 50 times the Gaussian variance. In that case $y_1$ is nonzero only when the single entry $R_{11}$ is nonzero, which happens with probability $1/100$, so most output coordinates of a spike are 0.

A seeded run on 20 Gaussian points in $\mathbb{R}^{300}$ with $s = 3$ and $k = 250$ keeps all 190 squared distances within a factor $1 \pm 0.5$, and about one third of the matrix entries are nonzero.

## Correctness

The full proofs are in the [correctness proof](proofs/correctness.md). There are three results.

1. **Unbiased with exact variance.** For every $s \ge 1$ and every $x$, $\mathbb{E}\|f(x)\|^2 = \|x\|^2$ and $\operatorname{Var}\|f(x)\|^2 = \frac{1}{k}\big(2\|x\|^4 + (s - 3)\sum_i x_i^4\big)$. The only facts used are $\mathbb{E}R_{ij} = 0$, $\mathbb{E}R_{ij}^2 = 1$, $\mathbb{E}R_{ij}^4 = s$, symmetry, and independence.
2. **The Johnson-Lindenstrauss guarantee for $s \in \{1, 3\}$.** For these two values every even moment of an entry is at most the matching moment of $N(0, 1)$: $\mathbb{E}R_{ij}^{2m} = s^{m-1} \le (2m - 1)!!$. Then every moment of $\langle x, r \rangle^2$ is at most the Gaussian one, and the upper tail bound of the Gaussian proof carries over unchanged. Achlioptas also proves the lower tail with the Gaussian constant, so $k \ge (4 + 2\beta)(\varepsilon^2/2 - \varepsilon^3/3)^{-1} \ln n$ gives all pairs within $1 \pm \varepsilon$ with probability at least $1 - n^{-\beta}$. The proof file gives a self-contained version of the lower tail with a slightly larger constant.
3. **The block construction.** For $S$ with $s$ blocks of $b$ rows, $\mathbb{E}\|Sx\|^2 = \|x\|^2$ and $\operatorname{Var}\|Sx\|^2 = \frac{2}{bs}\big(\|x\|^4 - \sum_i x_i^4\big)$, which is never more than the Gaussian variance $2\|x\|^4 / k$. Kane and Nelson prove the tail bound: $k = O(\varepsilon^{-2} \log(1/\delta))$ and $s = O(\varepsilon^{-1} \log(1/\delta))$ give $\Pr[\,|\|Sx\|^2 - \|x\|^2| > \varepsilon\|x\|^2] < \delta$ for every $x$.

For $s > 3$ the fourth moment $s$ is larger than the Gaussian value 3, and no bound of the JL form holds for all $x$ with the same $k$: the spike $e_1$ shows this. Li, Hastie and Church prove that $\langle x, r \rangle$ is asymptotically normal for $s = o(d)$ when the vectors have no dominant coordinate, so the variance is then close to the Gaussian $2\|x\|^4$.

## Complexity

- **Drawing the matrix.** $O(dk)$ random numbers as written; with a skip-ahead sampler (draw the gap to the next nonzero) the cost is $O(dk/s)$ expected, the number of nonzeros.
- **Applying to one dense point.** $O(dk/s)$ expected operations, against $O(dk)$ for a Gaussian matrix. For $s = 3$ this is a factor 3; for $s = \sqrt{d}$ it is a factor $\sqrt{d}$.
- **Applying to a sparse point.** $O(k \cdot \mathrm{nnz}(x) / s)$ expected with $R$ stored by rows. The block construction takes exactly $s \cdot \mathrm{nnz}(x)$ operations.
- **Space.** $O(dk/s)$ expected for the nonzeros, stored as signs (one bit each plus an index), or $O(1)$ for a seed when the entries are made again on demand.
- **Arithmetic.** With $s \in \{1, 3\}$ the sum in line L9 uses only additions and subtractions; the one multiplication by $\sqrt{s/k}$ comes at the end. This is the "database-friendly" property of Achlioptas: it runs in SQL with integer arithmetic.

## Properties

- Randomized and oblivious: $R$ does not depend on the data, so new points and streams map with the same $R$.
- Linear: $f(x - y) = f(x) - f(y)$, so distance and norm guarantees are the same thing.
- Unbiased for squared norms and for inner products for every $s$.
- For $s = 1$ the variance $2\|x\|^4 - 2\sum x_i^4$ is never above the Gaussian variance; for $s = 3$ it is equal; for $s > 3$ it is larger, by $(s - 3)\sum x_i^4$.
- The worst vectors for large $s$ are the sparse ones, where $\sum x_i^4$ is close to $\|x\|^4$. The best are the flat ones, where $\sum x_i^4 = \|x\|^4 / d$.

## Variants and improvements

- **Very sparse projection** with $s = \sqrt{d}$ or $s = d / \log d$ (Li, Hastie and Church 2006). Fast, with a variance close to the Gaussian one on data with no heavy coordinates.
- **Sparse JL transform** (Kane and Nelson 2014). The block construction above, or a graph construction with $s$ distinct random rows per column. It keeps the JL guarantee for every vector with $s = O(\varepsilon^{-1}\log(1/\delta))$, which is optimal up to a factor $\log(1/\varepsilon)$ by Nelson and Nguyen (2013).
- **[Count sketch](/count-sketch/) and feature hashing.** $s = 1$ in the block construction, with hash functions for the row and the sign instead of stored random numbers. Fast, but it needs vectors with no heavy coordinate.
- **Precondition first.** A random sign flip and a Walsh-Hadamard transform make every vector flat with high probability; after that a very sparse matrix is safe. This is the [fast Johnson-Lindenstrauss transform](/fast-johnson-lindenstrauss-transform/).
- **Limited independence.** The entries need not be fully independent. Hash functions from a family with $O(\log(1/\delta))$-wise independence ([k-wise independence](/k-wise-independence/)) are enough for the moment bounds that the proofs of Kane and Nelson use, which removes the stored matrix.

## When to use it

Use $s = 3$ or $s = 1$ as the default replacement for a Gaussian random projection: the guarantee is the same and the cost is lower. Use $s = \sqrt{d}$ for large dense data whose coordinates are of similar size, such as image features or term counts after normalization, and check the distortion on a sample. Use the block construction or a count sketch for very sparse data such as text, where the cost should depend on $\mathrm{nnz}(x)$. For a guarantee on arbitrary vectors with very low density, use the fast Johnson-Lindenstrauss transform instead.

## Pitfalls

- **Spikes with large $s$.** One-hot features, indicator columns, and vectors with a few large coordinates break the very sparse projection. The variance grows to $s - 1$ times $\|x\|^4$ for a spike.
- **Wrong scale.** The nonzero entries must be $\pm\sqrt{s}$ (or the output scaled by $\sqrt{s/k}$). With entries $\pm 1$ at density $1/s$, all squared norms shrink by a factor $s$.
- **Rows with no nonzero.** For large $s$ and small $k$, some input coordinates fall in no column of $R$ at all, and changes in those coordinates are invisible. The expected number is $d(1 - 1/s)^k \approx d e^{-k/s}$.
- **A different matrix for new points.** As for every random projection, the same matrix or seed must be used for all points.
- **Density counted per column against per entry.** The Achlioptas and Li density is per entry, so the number of nonzeros per column varies. The Kane and Nelson construction fixes it at exactly $s$ per column of $S$; mixing the two parametrizations gives the wrong $s$.

## Implementations

## History

Achlioptas (2001 conference version, 2003 journal) asked whether the Gaussian matrix of the [Johnson-Lindenstrauss lemma](/johnson-lindenstrauss-lemma/) could be replaced by something that runs in a database with only additions. He proved that random signs, and signs with two thirds zeros, give the same bound, by a comparison of moments with the Gaussian. Bingham and Mannila (2001) tested this sparse matrix on image and text data and found it as accurate as the Gaussian one. Li, Hastie and Church (2006) computed the exact variances for every density and proposed $s = \sqrt{d}$. Dasgupta, Kumar and Sarlós (2010) gave the first sparse JL transform with a guarantee for every vector, and Kane and Nelson (2012 conference, 2014 journal) reduced the number of nonzeros per column to $O(\varepsilon^{-1} \log(1/\delta))$.

## References
