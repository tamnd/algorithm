---
tag: HRTZ5C
kind: algorithm
slug: mixed-model-association
name: Mixed model association testing
aliases:
- EMMAX
- linear mixed model GWAS
- LMM association test
area: biology/population-genetics
level: advanced
summary: "Tests each variant in a linear mixed model whose random effect has the genetic relationship matrix as covariance, to control for structure and relatedness."
model: real-ram
complexity:
  vars: {n: the number of individuals, M: the number of tested SNPs, p: the number of fixed covariates}
  time: {worst: Θ(n^3 + M n^2), average: Θ(n^3 + M n^2), best: Θ(n^3 + M n^2)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2008
  people: [Hyun Min Kang, Noah A. Zaitlen, Eleazar Eskin]
  note: "Kang and coworkers made the mixed model test fast with a spectral form of the REML likelihood in 2008, and in 2010 estimated the variance components once for the whole scan."
prereqs: [linear-mixed-model, restricted-maximum-likelihood, genome-wide-association-study]
see_also: [snp-heritability-estimation, genomic-control, genetic-principal-components, kinship-coefficient, henderson-mixed-model-equations, weighted-least-squares, golden-section-search, wald-test]
sources:
  - paper: doi:10.1534/genetics.107.080101
    title: Hyun Min Kang, Noah A. Zaitlen, Claire M. Wade, Andrew Kirby, David Heckerman, Mark J. Daly and Eleazar Eskin, Efficient control of population structure in model organism association mapping, Genetics 178(3), 2008
    locator: pp. 1709-1723 (the spectral form of the ML and REML likelihoods in the variance ratio, and the grid and Newton search)
  - paper: doi:10.1038/ng.548
    title: Hyun Min Kang, Jae Hoon Sul, Susan K. Service, Noah A. Zaitlen, Sit-yee Kong, Nelson B. Freimer, Chiara Sabatti and Eleazar Eskin, Variance component model to account for sample structure in genome-wide association studies, Nature Genetics 42(4), 2010
    locator: pp. 348-354 (variance components estimated once under the null, then generalized least squares for each marker)
  - paper: doi:10.1038/nmeth.1681
    title: Christoph Lippert, Jennifer Listgarten, Ying Liu, Carl M. Kadie, Robert I. Davidson and David Heckerman, FaST linear mixed models for genome-wide association studies, Nature Methods 8(10), 2011
    locator: pp. 833-835 (the spectral rotation with a low-rank relationship matrix, linear in the number of individuals)
---

Mixed model association testing runs a [genome-wide association study](/genome-wide-association-study/) in a sample with population structure or relatives. It adds to the regression of the trait on each SNP a random effect $u$ whose covariance is proportional to a genetic relationship matrix $K$, so that people who share more of their genome are allowed to have more similar traits. One eigendecomposition of $K$ makes the covariance diagonal, after which the variance components are found by a one-dimensional search, and each SNP costs one rotation and a small [weighted least squares](/weighted-least-squares/) fit. It corrects structure and relatedness better than one constant factor or a few principal components.

## In plain words

If a sample mixes groups of different ancestry, or contains relatives, people who are closely related tend to have similar traits and similar genotypes at many places. A plain test then finds links between the trait and many markers that have nothing to do with it. A mixed model first measures, from the genotypes, how related each pair of people is. It then lets the trait of related people be similar for that reason alone, and asks whether a marker adds anything beyond it. To keep a scan of millions of markers fast, the model fixes how much of the trait is explained by relatedness once, before the scan, and then tests the markers one by one with this fixed amount.

## The problem

**Input.** A trait $y \in \mathbb R^n$ for $n$ individuals, a matrix $X$ of $p$ covariates (a column of ones and, for example, age and sex), a genetic relationship matrix $K$ of size $n \times n$, and $M$ SNPs, each a dosage vector $g_j \in \{0, 1, 2\}^n$.

**Model.** For SNP $j$,

$$y = X \beta + g_j b_j + u + e, \qquad u \sim N(0, \sigma_g^2 K), \qquad e \sim N(0, \sigma_e^2 I),$$

so $\operatorname{Var}(y) = \sigma_g^2 (K + \delta I)$ with $\delta = \sigma_e^2 / \sigma_g^2$. This is a [linear mixed model](/linear-mixed-model/) with one variance component besides the noise.

**Output.** For each SNP, the estimate $\hat b_j$, its standard error and a test of $b_j = 0$.

$K$ is usually the genomic relationship matrix, the average over SNPs of products of standardized genotypes. It estimates twice the [kinship coefficient](/kinship-coefficient/) of each pair, relative to the sample.

## The algorithm

```pseudo id=main
MIXED-MODEL-SCAN(y, X, K, g_1, ..., g_M)
L1  K = U diag(s) U^T, an eigendecomposition
L2  ỹ ← U^T y, X̃ ← U^T X
L3  δ̂ ← the δ that maximizes the REML profile ℓ_R(δ), with weights 1/(s_i + δ) on the rotated rows
L4  σ̂_g² ← R(δ̂)/(n - p), σ̂_e² ← δ̂ σ̂_g²
L5  for j ← 1 to M do g̃ ← U^T g_j
L6      b̂_j, Var(b̂_j) ← weighted least squares of ỹ on [X̃, g̃] with weights 1/(σ̂_g² (s_i + δ̂))
L7      T_j ← b̂_j² / Var(b̂_j); p_j ← P(χ²_1 > T_j)
L8  return T, p
```

After the rotation of line L2, the covariance is diagonal: $\operatorname{Var}(\tilde y) = \sigma_g^2 \operatorname{diag}(s + \delta)$. So each evaluation of the [REML](/restricted-maximum-likelihood/) profile in line L3 is a weighted regression with $n$ rows and $p$ columns. The search is a grid of 100 points over $\log \delta \in [-10, 10]$, then [golden-section search](/golden-section-search/) around the best point. Line L7 is a [Wald test](/wald-test/) with the variance components held fixed.

## Example

Take two pairs of full sibs and the relationship matrix $K$ with 1 on the diagonal, $1/2$ within each pair and 0 between the pairs. The trait is $y = (1, 3, 2, 6)$, the only covariate is the intercept, and the SNP is $g = (0, 1, 1, 2)$. Fix $\sigma_g^2 = \sigma_e^2 = 1$, so $\delta = 1$.

- The eigenvectors of $K$ are the sum and the difference within each pair, $(1, 1, 0, 0)/\sqrt2$ with eigenvalue $3/2$, $(1, -1, 0, 0)/\sqrt2$ with $1/2$, and the same for the second pair. The weights are $1/(3/2 + 1) = 0.4$ for the sums and $1/(1/2 + 1) = 2/3$ for the differences.
- Rotated, $\tilde y = (4, -2, 8, -4)/\sqrt2$, the intercept is $(\sqrt2, 0, \sqrt2, 0)$ and $\tilde g = (1, -1, 3, -1)/\sqrt2$.
- The weighted cross products are $\sum w x^2 = 1.6$, $\sum w x g = 1.6$, $\sum w g^2 = 8/3$, $\sum w x y = 4.8$ and $\sum w g y = 7.6$. The determinant of the $2 \times 2$ system is $1.6 \cdot 8/3 - 1.6^2 = 128/75$.
- So $\hat b = 1.6 (7.6 - 4.8) / (128/75) = 2.625$, $\operatorname{Var}(\hat b) = 1.6 / (128/75) = 15/16$, and $T = 2.625^2 / 0.9375 = 7.35$, with $p = 0.0067$.

Ordinary least squares on the same data gives $\hat b = 2.5$. The mixed model gives more weight to the differences within pairs, where the SNP and the trait vary together beyond what the shared family background explains.

## Correctness

$U$ is orthogonal, so $(K + \delta I)^{-1} = U \operatorname{diag}(1/(s + \delta)) U^\top$ and $\log\det(K + \delta I) = \sum_i \log(s_i + \delta)$. Every quadratic form and determinant of the REML likelihood therefore has the same value in the rotated coordinates, where it is a weighted sum. Maximizing over $\sigma_g^2$ in closed form leaves a function of $\delta$ alone. In the same way, the weighted regression of line L6 gives exactly the generalized least squares estimate $\hat b$ and its variance $[(Z^\top V^{-1} Z)^{-1}]_{jj}$ on the original data. If $V$ were the true covariance, $T$ would be exactly chi-squared with 1 degree of freedom under the null. With $V$ estimated once under the null, it is a close approximation for SNPs of small effect. The full proof is below.

## Complexity

- **Time.** The eigendecomposition costs $\Theta(n^3)$ once. Each evaluation of $\ell_R$ costs $O(n p^2)$, and the search uses about 150 of them. Each SNP costs $\Theta(n^2)$ for the rotation $U^\top g$ and $O(n p^2)$ for the fit. With $p$ small, the total is $\Theta(n^3 + M n^2)$.
- **Space.** $\Theta(n^2)$ for $U$. The genotypes are streamed one SNP at a time.
- **Re-estimating per SNP.** Repeating line L3 for each SNP, the exact REML test, costs $O(n p^2)$ per evaluation and SNP, after rotating the SNP. It is affordable because of the rotation.
- **Low rank.** If $K = W W^\top / m$ with $m < n$ SNPs, the thin singular value decomposition of $W$ costs $O(n m^2)$, and each SNP costs $O(n m)$. This is the route of FaST-LMM (Lippert and coworkers 2011), linear in $n$.

## Properties

- **Controls structure and relatedness at once.** Population structure, family structure and cryptic relatedness all show in $K$, and the model does not need to know which is which.
- **Exact for known components.** With the true $\sigma_g^2$ and $\sigma_e^2$ the test is exact under the model. Estimating them once loses a little power for SNPs of large effect.
- **Same ranking as the exact test for small effects.** Most SNPs explain a tiny part of the variance, so the null components are close to the per-SNP components.
- **Not a fixed factor.** Unlike [genomic control](/genomic-control/), the correction depends on the SNP: a SNP whose frequency follows the structure of $K$ is corrected more.
- **Gains power with polygenic traits.** The random effect absorbs part of the background genetic variance, so the residual variance shrinks and the test of a real SNP gains power.

## Variants and improvements

- **Exact per-SNP REML.** Re-estimate $\delta$ for every SNP. This is the original form of Kang and coworkers (2008), exact but slower.
- **Leave one chromosome out.** Build $K$ from all chromosomes except the one of the tested SNP. Otherwise the SNP is in $K$ and partly explains itself, which lowers power (proximal contamination).
- **Low-rank and sparse relationship matrices.** Build $K$ from a subset of SNPs, or keep only the entries of close relatives, to save time on large samples.
- **Bayesian and mixture random effects.** Methods with a mixture prior on SNP effects replace the single variance component and gain power for traits with a few large effects.
- **Binary traits.** The linear model on a 0/1 trait works for balanced designs but can be miscalibrated for unbalanced case-control ratios. Logistic mixed models with a saddle point approximation fix this.

## When to use it

- Association studies in samples with relatives, such as founder populations, family cohorts or model organism strains.
- Large biobanks, where cryptic relatedness is common and PCA alone leaves inflation.
- Samples with complex structure, such as admixed populations or inbred lines.
- When genomic control or a few principal components do not bring the inflation of the null statistics down.

## Pitfalls

- **The SNP in its own matrix.** If $K$ includes the tested SNP and its neighbours, the test loses power. Use the leave-one-chromosome-out matrix.
- **Inflation under polygenicity.** With many causal SNPs of small effect, even a correct mixed model scan has an inflation factor above 1, because the real signal is spread over many SNPs in linkage disequilibrium with the causal ones. Judge confounding by the intercept of [LD score regression](/ld-score-regression/), not by the inflation factor alone.
- **Non-positive-definite $K$.** The genomic relationship matrix with the usual diagonal can have small negative eigenvalues. $K + \delta I$ is then positive definite only for $\delta$ above them, and the search must stay in that range.
- **Variance ratio at the edge.** If the REML maximum is at the edge of the search range, the trait shows no genetic variance in this sample, and the model reduces to ordinary least squares.
- **Environment that follows ancestry.** If an environmental factor is shared by relatives but not captured by $K$, the model does not remove it.

## Implementations

## History

Yu and coworkers (2006) used a mixed model with a kinship matrix to map traits in maize and other plants, where structure and relatedness are strong. The REML fit for each marker was slow. Kang and coworkers (2008) rotated the data by the eigenvectors of the kinship matrix, so that each likelihood evaluation became a weighted sum. Kang and coworkers (2010) then estimated the variance components once under the null, which made a genome-wide scan in humans cost little more than a regression. Lippert and coworkers (2011) used a low-rank relationship matrix to make the cost linear in the sample size. Later methods for biobanks with hundreds of thousands of people use iterative solvers instead of an eigendecomposition.

## References
