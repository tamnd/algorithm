---
tag: BN6ZMV
kind: concept
slug: scree-plot
name: Scree plot
aliases:
- scree test
- scree graph
area: machine-learning/dimensionality-reduction
level: intro
summary: "A plot of the eigenvalues of a covariance or correlation matrix in decreasing order. The elbow of the curve is a heuristic for the number of components to keep."
prereqs: [explained-variance, principal-component-analysis]
see_also: [factor-analysis, elbow-method, eigengap-heuristic, reconstruction-error, probabilistic-pca]
sources:
  - paper: doi:10.1207/s15327906mbr0102_10
    title: Raymond B. Cattell, The scree test for the number of factors, Multivariate Behavioral Research 1(2), 245-276, 1966
    locator: the plot of the eigenvalues against their rank, and the rule to stop where the straight scree of small eigenvalues begins
  - paper: doi:10.1007/BF02289447
    title: John L. Horn, A rationale and test for the number of factors in factor analysis, Psychometrika 30(2), 179-185, 1965
    locator: parallel analysis, the comparison of the observed eigenvalues with those of uncorrelated random data of the same size
  - book: isbn:9780387954424
    title: I. T. Jolliffe, Principal Component Analysis, second edition, Springer, 2002
    locator: Section 6.1.3 (the scree graph and the log-eigenvalue diagram) and Section 6.1 in general (rules for choosing the number of components)
  - paper: doi:10.1177/001316446002000116
    title: Henry F. Kaiser, The application of electronic computers to factor analysis, Educational and Psychological Measurement 20(1), 141-151, 1960
    locator: the eigenvalue-greater-than-one rule that the scree test is often compared with
---

A scree plot shows the eigenvalues $\lambda_1 \ge \lambda_2 \ge \cdots \ge \lambda_d$ of a covariance or correlation matrix against their index $j$, or the [explained variance](/explained-variance/) ratios $\lambda_j / \sum_i \lambda_i$. Cattell (1966) proposed it to choose the number of factors in [factor analysis](/factor-analysis/): the large eigenvalues form a steep slope, and the small ones lie on a flat line, like the scree of loose stones at the foot of a cliff. The components before the bend, the *elbow*, are kept. The rule is a visual heuristic with no guarantee; parallel analysis (Horn 1965) is a less subjective alternative.

## In plain words

After a principal component analysis, each component comes with a number that says how much of the spread of the data it holds. Sort these numbers from large to small and draw them as points on a line chart. Often the first few are large and then the curve bends and goes on almost flat. The flat part looks like the pile of rubble at the bottom of a cliff, which is what "scree" means.

The idea is that the steep part is the real structure and the flat part is noise. So you keep the components before the bend. Different people can see the bend in different places, so the plot is a guide and not a test. A second method draws the same curve for pure random data of the same size, and keeps the components that beat the random curve.

## The idea

**The plot.** Compute the eigenvalues of the [covariance matrix](/covariance-matrix/) (or of the correlation matrix, if the features are standardized) by [PCA](/principal-component-analysis/), and draw the points $(j, \lambda_j)$ for $j = 1, \ldots, d$, joined by lines. A variant plots $\log \lambda_j$ (the log-eigenvalue diagram, Jolliffe Section 6.1.3), which makes a geometric decay of the noise eigenvalues look straight. Another variant plots the cumulative ratio $R_k$.

**The elbow rule (Cattell).** Find the index from which the remaining points lie close to a straight, nearly flat line. Keep the components before that index. Authors differ on whether the component at the elbow itself is kept. The rule assumes a model in which the data are a few strong components plus noise with a flat spectrum; it gives no help when the eigenvalues decay smoothly.

**Why noise gives a slope, not a flat line.** Even when the true covariance is the identity, the sample eigenvalues spread out: for $n$ points of $d$ independent standard normal features, with $d / n \to \gamma \in (0, 1]$, the largest sample eigenvalue tends to $(1 + \sqrt\gamma)^2$ and the smallest to $(1 - \sqrt\gamma)^2$ (the Marchenko-Pastur law). So the "scree" itself is tilted, and a fixed threshold such as Kaiser's rule $\lambda_j > 1$ keeps noise components.

**Parallel analysis (Horn 1965).** Draw many data sets of the same size $n \times d$ with independent normal features, compute the eigenvalues of their correlation matrices, and average them for each index $j$. Keep component $j$ while the observed $\lambda_j$ is above the random value for index $j$. A common variant uses the 95th percentile of the random eigenvalues instead of the mean, which keeps fewer components. Parallel analysis is still a heuristic: it compares against a null model of no correlation at all, and it ignores that the first real components change the distribution of the later sample eigenvalues.

**Related rules.** The [elbow method](/elbow-method/) of clustering applies the same visual idea to the k-means cost as a function of $k$. The [eigengap heuristic](/eigengap-heuristic/) of spectral clustering looks for the largest gap between consecutive eigenvalues of a graph Laplacian.

## Examples

**A clear elbow.** Generate $n = 200$ points with $d = 10$ features from a model with three factors: feature $j$ is $0.8$ times factor $(j \bmod 3)$ plus normal noise with standard deviation $0.6$ (`random.Random(2026)`). The eigenvalues of the correlation matrix are

$$3.259,\ 2.437,\ 2.105,\ 0.396,\ 0.388,\ 0.356,\ 0.289,\ 0.277,\ 0.268,\ 0.226.$$

The curve drops from 2.105 to 0.396 and is flat after that. The elbow is at index 4, so the plot suggests three components, the true number. Kaiser's rule also keeps three.

**An unclear elbow.** Use the same model with the factor weights $0.8$, $0.45$ and $0.3$ for the three factors. The eigenvalues are now $3.167, 1.821, 1.382, 0.853, 0.805, 0.568, 0.482, 0.347, 0.298, 0.276$.

```text
 j   λ_j    random mean  random 95%
 1  3.167  ################################  1.355  1.453
 2  1.821  ##################                1.252  1.326
 3  1.382  ##############                    1.174  1.239
 4  0.853  ########                          1.093  1.162
 5  0.805  ########                          1.016  1.065
 6  0.568  ######                            0.956  1.001
 7  0.482  #####                             0.893  0.944
 8  0.347  ###                               0.831  0.877
 9  0.298  ###                               0.753  0.814
10  0.276  ###                               0.677  0.734
```

One reader sees the elbow after the first eigenvalue and keeps one component; another sees it at index 4 and keeps three. Parallel analysis with 100 random $200 \times 10$ data sets (`random.Random(7)`) gives the mean and the 95th percentile columns. The first three observed eigenvalues are above both, and the fourth (0.853) is below both, so parallel analysis keeps three components.

**The PCA example.** The eigenvalues $81, 36, 9$ of the eight points of the [PCA](/principal-component-analysis/) page decay by a factor of 2.25 and then 4. With three points the plot has no flat part, and the scree test cannot be applied. This is a common case: with few features the plot carries little information.

## Where it is used

- Choosing the number of components in [principal component analysis](/principal-component-analysis/), together with the cumulative [explained variance](/explained-variance/).
- Choosing the number of factors in [factor analysis](/factor-analysis/), its original use.
- Choosing the latent dimension of [probabilistic PCA](/probabilistic-pca/), where a likelihood-based choice (for example a held-out likelihood) is an alternative.
- Choosing the rank of a truncated [singular value decomposition](/singular-value-decomposition/), for example in [latent semantic analysis](/latent-semantic-analysis/), where the plot shows the singular values.
- The same visual reasoning appears in the [elbow method](/elbow-method/) for k-means and the [eigengap heuristic](/eigengap-heuristic/) for spectral clustering.

## References
