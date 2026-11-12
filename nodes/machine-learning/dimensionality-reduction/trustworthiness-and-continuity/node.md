---
tag: B3SH8J
kind: definition
slug: trustworthiness-and-continuity
name: Trustworthiness and continuity
aliases:
- trustworthiness
- trustworthiness measure
area: machine-learning/dimensionality-reduction
level: advanced
summary: "Rank-based measures of how well an embedding preserves local neighbourhoods."
prereqs: [embedding, k-nearest-neighbor-search]
see_also: [t-sne, umap, stochastic-neighbor-embedding, self-organizing-map, multidimensional-scaling, principal-component-analysis, k-nearest-neighbor-graph, ranking-comparison-kendall-tau]
sources:
  - paper: doi:10.1007/3-540-44668-0_68
    title: Jarkko Venna and Samuel Kaski, Neighborhood preservation in nonlinear projection methods, an experimental study, Artificial Neural Networks (ICANN 2001), Lecture Notes in Computer Science 2130, Springer, 2001, pages 485 to 491
    locator: the definition of trustworthiness by the ranks of false neighbors, and its use to compare nonlinear projection methods
  - paper: doi:10.1016/j.neunet.2006.05.014
    title: Jarkko Venna and Samuel Kaski, Local multidimensional scaling, Neural Networks 19(6), 2006, pages 889 to 899
    locator: Section 3.2, equations (14) (trustworthiness M1(k)) and (15) (continuity M2(k)) with the factor 2/(Nk(2N - 3k - 1)), the rule for ties, and the value about 0.5 for random neighborhoods
  - paper: doi:10.1186/1471-2105-4-48
    title: Samuel Kaski, Janne Nikkilä, Merja Oja, Jarkko Venna, Petri Törönen and Eero Castrén, Trustworthiness and metrics in visualizing similarity of gene expression, BMC Bioinformatics 4, 2003, article 48
    locator: trustworthiness and the preservation of the original neighborhoods applied to visualizations of gene expression data
  - paper: "John A. Lee and Michel Verleysen, Quality assessment of dimensionality reduction, rank-based criteria, Neurocomputing 72(7-9), 2009, pages 1431 to 1443"
    locator: the co-ranking matrix, and trustworthiness and continuity written as sums over its blocks
---

Trustworthiness and continuity are two numbers in $[0, 1]$ that measure how well an [embedding](/embedding/) keeps the $k$ nearest neighbors of each point. Trustworthiness asks whether the neighbors seen in the embedding are real: it penalizes points that are close in the embedding but far in the original data. Continuity asks whether the real neighbors are still seen: it penalizes points that are close in the data but pushed apart by the embedding. Venna and Kaski introduced trustworthiness in 2001 and gave both measures in the form below in 2006. They use only ranks of distances, so they suit methods such as [t-SNE](/t-sne/) and [UMAP](/umap/) that keep neighborhoods and freely change large distances, where the distortion of the embedding is not a useful number.

## Definition

Let $x_1, \ldots, x_n$ be the original points and $y_1, \ldots, y_n$ their images in the embedding. For $i \ne j$:

- $r(i, j)$ is the rank of $x_j$ among the other points by distance from $x_i$ in the original space, with 1 for the nearest;
- $\hat r(i, j)$ is the same rank by distance from $y_i$ in the embedding;
- $N_k(i)$ and $\hat N_k(i)$ are the sets of the $k$ nearest neighbors of $i$ in the original space and in the embedding;
- $U_k(i) = \hat N_k(i) \setminus N_k(i)$ is the set of false neighbors (close in the embedding only), and $V_k(i) = N_k(i) \setminus \hat N_k(i)$ the set of missed neighbors (close in the original space only).

For $1 \le k < n/2$, the trustworthiness and the continuity are

$$T(k) = 1 - \frac{2}{n k (2n - 3k - 1)} \sum_{i=1}^{n} \sum_{j \in U_k(i)} \big(r(i, j) - k\big),$$

$$C(k) = 1 - \frac{2}{n k (2n - 3k - 1)} \sum_{i=1}^{n} \sum_{j \in V_k(i)} \big(\hat r(i, j) - k\big).$$

A false neighbor $j$ of $i$ costs $r(i, j) - k \ge 1$, how far beyond the $k$-neighborhood it really is. A missed neighbor costs $\hat r(i, j) - k$, how far outside the $k$-neighborhood the embedding put it. Continuity is the trustworthiness with the two spaces exchanged.

**The factor.** For one point $i$, the false neighbors are at most $k$ distinct points with input ranks in $\{k + 1, \ldots, n - 1\}$. Their total cost is at most the sum for the $k$ largest ranks $n - 1, \ldots, n - k$, which are all above $k$ because $k < n/2$:

$$\sum_{t=1}^{k} (n - t - k) = k(n - k) - \frac{k(k + 1)}{2} = \frac{k (2n - 3k - 1)}{2}.$$

So the double sum is at most $n k (2n - 3k - 1)/2$, and the factor makes $0 \le T(k) \le 1$; the same holds for $C(k)$. For $k > n/2$ the $k$ largest ranks include ranks below $k$, the bound is no longer the maximum, and the formula is not normalized; at $k = n/2$ the bound still holds.

**Properties.**
- $T(k) = 1$ exactly when $\hat N_k(i) = N_k(i)$ for every $i$. Since $|U_k(i)| = |V_k(i)|$, this is also exactly when $C(k) = 1$; the two measures differ only in how they weigh the errors.
- Any map that keeps the order of distances from each point, such as a rotation, a translation, or a scaling, gives $T = C = 1$ for every $k$.
- For random neighborhoods both values are about $0.5$ (Venna and Kaski 2006).
- Ties in distance make the ranks ambiguous. Venna and Kaski treat all orders that agree with the distances as equally likely and average the best and worst case; a simpler rule breaks ties by the index of the point.
- With all ranks computed by sorting, the cost is $O(n^2 \log n)$ time and $O(n^2)$ memory for $n$ points, plus the distance computations.

## Examples and non-examples

**Tearing a line.** Let the original points be $0, 1, \ldots, 6$ on a line, $n = 7$ and $k = 2$, so the factor is $2/(7 \cdot 2 \cdot 7) = 1/49$. The embedding keeps points $0, 1, 2, 3$ in place and moves points $4, 5, 6$ to $10, 11, 12$: a tear between 3 and 4. Ties are broken by index. Only points 3 and 4 change their neighborhoods:

| point | $N_2$ | $\hat N_2$ | false neighbor, cost $r - 2$ | missed neighbor, cost $\hat r - 2$ |
|---|---|---|---|---|
| 3 | $\{2, 4\}$ | $\{1, 2\}$ | 1, rank 3, cost 1 | 4, rank 4, cost 2 |
| 4 | $\{3, 5\}$ | $\{5, 6\}$ | 6, rank 4, cost 2 | 3, rank 3, cost 1 |

Each sum is 3, so $T(2) = C(2) = 1 - 3/49 = 46/49 \approx 0.939$.

**Folding a line.** Keep the same points and move the first four to the positions $3, 1, 0, 2$ (points 4, 5, 6 stay at 4, 5, 6). Point 0 now sits next to point 4 and point 3 next to points 0 and 1. The false neighbor costs sum to 12 and the missed neighbor costs to 9, so $T(2) = 37/49 \approx 0.755$ and $C(2) = 40/49 \approx 0.816$. The fold creates more false neighbors than torn ones, and trustworthiness drops more.

**Projections and neighbor embeddings.** A linear projection such as [PCA](/principal-component-analysis/) never increases distances, so close points stay close and continuity tends to be high; but far points can land on top of each other, which lowers trustworthiness. Methods that pull neighbors together and push others apart, such as [t-SNE](/t-sne/), tend to have high trustworthiness and can tear the data, which lowers continuity. Reporting both, for several $k$, shows which kind of error an embedding makes.

**Non-example: a global distance measure.** An embedding can have $T = C = 1$ for small $k$ and still change large distances by any factor; the measures say nothing about the global layout, the sizes of clusters, or the distances between them. Conversely, an embedding with small distortion of most distances can have low trustworthiness if the few changed distances are among neighbors.

**Non-example: $k > n/2$.** For $n = 6$ and $k = 4$ a point has at most one false neighbor, of rank 5, so its largest possible cost is 1, while $k(2n - 3k - 1)/2 = -2$. The factor is negative there, and the values can leave $[0, 1]$.

## Related definitions

- **Co-ranking matrix (Lee and Verleysen 2009).** The $(n - 1) \times (n - 1)$ matrix $Q$ with $Q_{ab} = \#\{(i, j) : r(i, j) = a,\ \hat r(i, j) = b\}$. Trustworthiness and continuity are weighted sums of its entries in the two blocks outside the upper-left $k \times k$ block, and other rank measures such as the local continuity meta-criterion are sums of other parts of it.
- **[Embedding](/embedding/) distortion:** the metric measure of quality, based on the ratios of distances rather than ranks.
- **[k-nearest neighbor graph](/k-nearest-neighbor-graph/):** $T(k) = C(k) = 1$ exactly when the embedding has the same $k$-nearest neighbor graph as the data.
- **Rank correlation:** [Kendall's tau](/ranking-comparison-kendall-tau/) and similar measures compare whole rankings; trustworthiness and continuity look only at the top $k$ of each point's ranking and weigh errors by their rank.
- **Precision and recall of neighbors:** in the information retrieval view of Venna, Peltonen, Nybo, Aidos and Kaski (2010), a false neighbor is an error of precision and a missed neighbor is an error of recall; trustworthiness and continuity are rank-weighted forms of the two.

## References
