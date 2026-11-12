---
tag: QJJDF9
kind: concept
slug: eigengap-heuristic
name: Eigengap heuristic
aliases:
- eigengap
- spectral gap heuristic for the number of clusters
area: machine-learning/clustering
level: advanced
summary: "Choose the number of clusters k that maximizes λ_{k+1} - λ_k for the sorted eigenvalues of a graph Laplacian. Davis-Kahan explains why; no theorem says it is right."
prereqs: [laplacian-matrix, eigenvalue, spectral-clustering]
see_also: [davis-kahan-theorem, weyls-inequality, normalized-cut, elbow-method, gap-statistic, silhouette-coefficient, stochastic-block-model, lanczos-algorithm]
sources:
  - paper: doi:10.1007/s11222-007-9033-z
    title: "Ulrike von Luxburg, A tutorial on spectral clustering, Statistics and Computing 17(4), 2007, pages 395 to 416"
    locator: "Section 8.3 (choosing the number of clusters, the eigengap heuristic and Figure 4), Section 7 (the perturbation theory view, with the Davis-Kahan theorem as Theorem 7) and Section 8.2 (the eigengap and the convergence of eigensolvers)"
  - paper: doi:10.1137/0707001
    title: "Chandler Davis and W. M. Kahan, The rotation of eigenvectors by a perturbation. III, SIAM Journal on Numerical Analysis 7(1), 1970, pages 1 to 46"
    locator: the sin θ theorem
  - paper: "Lihi Zelnik-Manor and Pietro Perona, Self-tuning spectral clustering, Advances in Neural Information Processing Systems 17 (NIPS 2004), MIT Press, 2005, pages 1601 to 1608"
    locator: the section on estimating the number of groups (the eigengap fails on noisy data; the alignment cost of rotated eigenvectors is proposed instead)
---

The eigengap heuristic chooses the number of clusters $k$ for [spectral clustering](/spectral-clustering/). Sort the eigenvalues of a graph Laplacian as $0 = \lambda_1 \le \lambda_2 \le \cdots \le \lambda_n$, and take the $k$ that makes the gap $\lambda_{k+1} - \lambda_k$ the largest, usually among $k \le k_{\max}$. When the similarity graph has exactly $k$ connected components, the first $k$ eigenvalues are 0 and $\lambda_{k+1} > 0$, so the rule is exact. For a graph close to that case, the [Davis-Kahan theorem](/davis-kahan-theorem/) says that a large gap makes the first $k$ eigenvectors stable, and these are the vectors that spectral clustering uses. It is a heuristic: on noisy or overlapping clusters the gaps are small and similar, and the rule can give any answer.

## In plain words

Make a graph of the data: a dot for each point, and a strong line between similar points. If the dots form three separate groups, three numbers of the graph (its smallest eigenvalues) are exactly zero, and the fourth number jumps up. If the groups are joined by a few weak lines, the first three numbers are small but not zero, and there is still a big jump after the third.

So list the numbers from small to large and look for the biggest jump. The count before the jump is the guess for the number of groups. This works well when the groups are clear. When the groups overlap, the numbers rise slowly with no big jump, and the guess is not reliable. Then look at the numbers yourself, or use another method.

## The idea

**The rule.** Let $L_{\mathrm{sym}}$ be the normalized Laplacian of the similarity graph (or $L_{\mathrm{rw}}$, which has the same eigenvalues, or $L = D - W$). Compute its smallest eigenvalues $\lambda_1 \le \cdots \le \lambda_{k_{\max}+1}$ and put

$$\hat k = \arg\max_{1 \le k \le k_{\max}} \;(\lambda_{k+1} - \lambda_k).$$

Von Luxburg (Section 8.3) states the rule in this form and shows it on a plot of the first ten eigenvalues (her Figure 4). Some tools start at $k = 2$, because $\lambda_2 - \lambda_1 = \lambda_2$ is often large and $k = 1$ is not a useful answer.

**Why it works in the ideal case.** The multiplicity of the eigenvalue 0 of each of $L$, $L_{\mathrm{rw}}$ and $L_{\mathrm{sym}}$ equals the number of connected components (see [spectral clustering](/spectral-clustering/), where this is proved). The spectrum of a graph with components $A_1, \ldots, A_k$ is the union of the spectra of the components. Each component contributes one zero, and its second eigenvalue is positive because it is connected. So $\lambda_1 = \cdots = \lambda_k = 0$ and $\lambda_{k+1}$ is the least second eigenvalue among the components. All gaps before $k$ are 0, and the gap at $k$ is $\lambda_{k+1} > 0$.

**Why it can work near the ideal case.** Write the observed matrix as $L' = L^0 + H$, where $L^0$ belongs to an ideal graph with $k$ components and $H$ is a small symmetric perturbation with $\lVert H \rVert_2 \le \varepsilon$. Two facts from matrix perturbation theory apply.

- *The eigenvalues move little.* By [Weyl's inequality](/weyls-inequality/), $|\lambda_i(L') - \lambda_i(L^0)| \le \varepsilon$ for each $i$. The eigenvalues of a Laplacian are at least 0, so $\lambda_j(L') \in [0, \varepsilon]$ for $j \le k$. Each gap before $k$ is then at most $\varepsilon$, and the gap at $k$ is at least $\lambda_{k+1}(L^0) - 2\varepsilon$. So if $\lambda_{k+1}(L^0) > 3\varepsilon$ and no later gap (up to $k_{\max}$) is larger, the rule returns the true $k$.
- *The eigenvectors move little.* The [Davis-Kahan $\sin\theta$ theorem](/davis-kahan-theorem/) (von Luxburg, Theorem 7) bounds the angles between the span of the first $k$ eigenvectors of $L^0$ and that of $L'$ by $\lVert H \rVert / \delta$, where $\delta$ is the distance between the first $k$ eigenvalues and the rest of the spectrum. With the first $k$ eigenvalues near 0, $\delta$ is about the eigengap. A large gap means that the rows of the computed eigenvector matrix are close to the ideal rows, which take only $k$ distinct values, so k-means finds the components.

The two facts justify the choice of a $k$ with a large gap, but they assume that an ideal $L^0$ with a small $H$ exists. Nothing in the data proves that. This is why the rule is a heuristic, not an algorithm with a guarantee.

**A third reason.** The [Lanczos method](/lanczos-algorithm/) and subspace iteration converge to the first $k$ eigenvectors at a speed set by the gap $\lambda_{k+1} - \lambda_k$ (von Luxburg, Section 8.2). A $k$ with a large gap also makes the eigenvectors cheap and accurate to compute.

## Examples

All values are the eigenvalues of $L_{\mathrm{sym}}$, computed by a script and checked by hand from the block structure. Each block is a complete graph on 4 vertices with edge weight 1.

| graph | smallest eigenvalues | gaps $\lambda_{k+1} - \lambda_k$ for $k = 1, 2, 3, 4$ | $\hat k$ |
|---|---|---|---|
| 3 blocks, no edges between | $0, 0, 0, 4/3, \ldots$ | $0, 0, 1.333, 0$ | 3 |
| 3 blocks, weight 0.05 between | $0, 0.176, 0.176, 1.294, \ldots$ | $0.176, 0, 1.118, 0$ | 3 |
| 4 blocks in 2 pairs, 0.2 inside a pair, 0.01 across | $0, 0.041, 0.433, 0.433, 1.258$ | $0.041, 0.392, 0, 0.825$ | 4 |
| 4 blocks in 2 pairs, 0.5 inside a pair, 0.01 across | $0, 0.031, 0.803, 0.803, 1.197$ | $0.031, 0.772, 0, 0.394$ | 2 |
| 3 blocks, weight 0.6 between | $0, 0.923, 0.923, 1.128, \ldots$ | $0.923, 0, 0.205, 0$ | 1 |

**Clean and weak links.** In the first two rows the answer is 3. With weight 0.05 between the blocks, each degree is $3 + 8 \cdot 0.05 = 3.4$. A vector that is constant on each block, with sum zero, gives $\lambda = 1 - 2.8/3.4 = 3/17 \approx 0.176$. A vector with sum zero inside one block gives $1 + 1/3.4 = 22/17 \approx 1.294$. The gap at 3 is $19/17$.

**Two scales.** In rows 3 and 4 the same four blocks form two pairs. When the pairs are loose (0.2), the largest gap is at 4. When they are tight (0.5), the largest gap is at 2, because the pairs now look like two clusters. Both answers describe a real structure. The heuristic returns one level of a hierarchy and does not say that the other exists.

**Overlap.** In row 5 the blocks are joined by weight 0.6, more than half of the weight inside. The values are $12/13$ (twice) and then $44/39$. The largest gap is at $k = 1$. If $k \ge 2$ is forced, the rule gives 3, but with a gap of only $8/39 \approx 0.205$.

**A random graph.** Take 12 vertices in 3 planted groups of 4, and join each pair with probability 0.6 inside a group and 0.4 across (seed 5 of the script). The first eight eigenvalues are $0, 0.574, 0.604, 0.807, 0.915, 0.922, 1.111, 1.270$, and the gaps for $k = 2, \ldots, 7$ are $0.029, 0.203, 0.108, 0.007, 0.189, 0.159$. The rule gives 3, but 6 is almost as good. This is the case that von Luxburg warns about: the clusters are not well separated, and the heuristic is ambiguous.

## Where it is used

- **Spectral clustering.** It is the standard first guess for $k$ in [spectral clustering](/spectral-clustering/) and in the $k$-way [normalized cut](/normalized-cut/).
- **Community detection.** On a [stochastic block model](/stochastic-block-model/) with well separated communities, the number of isolated eigenvalues (outside the bulk of the spectrum) counts the communities. The eigengap is the same idea.
- **Low rank.** The same rule picks the rank of a matrix from a gap in its singular values, as in the scree plot of principal component analysis.
- **Other rules for $k$.** When there is no clear gap, compare with the [elbow method](/elbow-method/), the [gap statistic](/gap-statistic/) or the [silhouette coefficient](/silhouette-coefficient/). Zelnik-Manor and Perona (2004) reported that the eigengap fails on noisy data, and chose $k$ by how well the rotated eigenvectors align with the coordinate axes.

**Pitfalls.** The rule needs a good similarity graph: a width $\sigma$ that is too small makes many components and many zero eigenvalues, and one that is too large hides all gaps. Use the eigenvalues of a normalized Laplacian, not of $W$. Always limit $k$ to a range, because large gaps also appear high in the spectrum. Do not report $\hat k$ as the number of clusters without a look at the plot of eigenvalues.

## References
