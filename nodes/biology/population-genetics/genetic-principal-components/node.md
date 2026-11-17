---
tag: HDK5SD
kind: algorithm
slug: genetic-principal-components
name: Principal components of genotypes
aliases:
- EIGENSTRAT
- smartpca
area: biology/population-genetics
level: core
summary: "Standardize each site of the genotype matrix, then take the top eigenvectors of the individual by individual matrix to show structure and to correct association tests."
model: real-ram
complexity:
  vars: {n: the number of individuals, m: the number of sites, k: the number of components, T: the number of iterations}
  time: {worst: O(n^2 m + T n^2 k), average: O(n^2 m + T n^2 k), best: O(n^2 m)}
  space: {extra: O(n m + n^2)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2006
  people: [Nick Patterson, Alkes L. Price, David Reich]
  note: "Patterson, Price and Reich described smartpca and a Tracy-Widom test for the number of significant axes in 2006. In the same year Price and coauthors used the axes to correct association tests in EIGENSTRAT. Cavalli-Sforza and coauthors had used principal components of gene frequencies of populations since the 1970s."
prereqs: [principal-component-analysis, allele-frequency, eigenvalue]
see_also: [singular-value-decomposition, power-iteration, population-structure-inference, maximum-likelihood-admixture-estimation, genome-wide-association-study, fixation-index, lanczos-algorithm, mixed-model-association]
sources:
  - paper: doi:10.1371/journal.pgen.0020190
    title: Nick Patterson, Alkes L. Price and David Reich, Population structure and eigenanalysis, PLoS Genetics 2(12), 2006
    locator: e190 (the normalization by sqrt(p(1 - p)) with p the sample allele frequency, the matrix X = MM', and the Tracy-Widom test of the largest eigenvalue)
  - paper: doi:10.1038/ng1847
    title: Alkes L. Price, Nick J. Patterson, Robert M. Plenge, Michael E. Weinblatt, Nancy A. Shadick and David Reich, Principal components analysis corrects for stratification in genome-wide association studies, Nature Genetics 38(8), 2006
    locator: pp. 904-909 (EIGENSTRAT, the adjustment of genotypes and phenotypes along the top axes and the association statistic)
  - paper: doi:10.1371/journal.pgen.1000686
    title: Gil McVean, A genealogical interpretation of principal components analysis, PLoS Genetics 5(10), 2009
    locator: e1000686 (the projection of the samples as a function of the mean coalescence times between pairs)
  - paper: doi:10.1038/nature07331
    title: John Novembre and coauthors, Genes mirror geography within Europe, Nature 456(7218), 2008
    locator: pp. 98-101 (the first two axes of European genotypes match a map of Europe)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, 4th edition, Johns Hopkins University Press, 2013
    locator: Section 8.2 (the power method and orthogonal iteration for symmetric matrices, with their rate of convergence)
---

Principal components of genotypes is the use of [principal component analysis](/principal-component-analysis/) on a matrix of genotypes, with one row per individual and one column per site. Each site is centered and divided by its binomial standard deviation, and the top eigenvectors of the resulting individual by individual matrix give the coordinates of the individuals. The first few axes usually follow ancestry, so a plot of axis 1 against axis 2 shows population structure without a model. The smartpca program of Patterson, Price and Reich (2006) computes the axes and tests how many are significant. EIGENSTRAT, by Price and coauthors (2006), removes the top axes from genotypes and phenotypes before an association test, which corrects for population stratification.

## In plain words

Each person has a row of numbers: for each variant, how many copies they carry. People whose ancestors came from the same place share many variants, so their rows look alike. The method finds the few directions in which the rows differ most. Each person gets a score along each direction. A plot of the scores puts related people close together and often looks like a map of where their ancestors lived.

The same scores help a study that looks for variants linked to a disease. If cases come more often from one group than from another, every variant common in that group looks linked to the disease. Removing the scores from the data first takes out this false signal.

## The problem

**Input.** A genotype matrix $G$ with $n$ rows (individuals) and $m$ columns (biallelic sites), where $g_{ij} \in \{0, 1, 2\}$ is the number of copies of allele 1. A number $k \ge 1$ of axes.

**Normalization.** For site $j$, let $\mu_j = \frac{1}{n} \sum_i g_{ij}$ and $p_j = \mu_j / 2$, the sample allele frequency. Keep the sites with $0 < p_j < 1$, say $m'$ of them, and set

$$M_{ij} = \frac{g_{ij} - \mu_j}{\sqrt{p_j (1 - p_j)}}, \qquad X = \frac{1}{m'} M M^{\mathsf T}.$$

Under [Hardy-Weinberg](/hardy-weinberg-principle/) proportions, $2 p_j (1 - p_j)$ is the variance of $g_{ij}$, so after the scaling every site has variance about 2 and about the same weight in $X$. The matrix $X$ is $n \times n$, symmetric and positive semidefinite. Patterson and coauthors write $X = M M'$; the factor $1/m'$ changes the eigenvalues by a constant and not the eigenvectors.

**Output.** The $k$ largest eigenvalues $\lambda_1 \ge \cdots \ge \lambda_k$ of $X$ and unit eigenvectors $v_1, \ldots, v_k$. The number $v_c(i)$ is the coordinate of individual $i$ on axis $c$. Equivalently, $v_c$ is the $c$-th left singular vector of $M$ in its [singular value decomposition](/singular-value-decomposition/), with singular value $\sqrt{m' \lambda_c}$.

## The algorithm

```pseudo id=main
GENETIC-PCA(G, k, rng)
L1  for each site j do
L2      p_j ← mean of column j / 2; if p_j = 0 or p_j = 1 then skip site j
L3      column j of M ← (column j of G - 2 p_j) / sqrt(p_j (1 - p_j))
L4  X ← M Mᵀ / m'                                  ▷ n × n
L5  Q ← k random Gaussian vectors from rng, orthonormalized
L6  repeat at most T times
L7      Z ← X Q
L8      λ_c ← q_cᵀ z_c for c = 1..k                ▷ Ritz values
L9      Q ← Gram-Schmidt(Z)
L10     if no λ_c changed by more than tol then stop
L11 diagonalize Qᵀ X Q, rotate Q by its eigenvectors, and return the k eigenpairs
```

Lines L1 to L4 build the normalized matrix. Lines L5 to L10 are orthogonal iteration, the block form of [power iteration](/power-iteration/): multiplying by $X$ grows the parts of the vectors along the top eigenvectors faster than the rest, and Gram-Schmidt keeps the $k$ vectors from collapsing onto the first one. Line L11 is the Rayleigh-Ritz step. It solves the small $k \times k$ eigenproblem of $X$ restricted to the span of $Q$, which sorts the vectors and separates close eigenvalues. Large programs replace lines L5 to L11 with a [Lanczos](/lanczos-algorithm/) or randomized method.

**EIGENSTRAT.** With the axes $v_1, \ldots, v_k$, take a site $j$ to test and a phenotype $y$. Remove from the genotype column and from $y$ their means and their projections on $v_1, \ldots, v_k$. Let $r$ be the correlation of the two residual vectors. The statistic $(n - k - 1) r^2$ is compared with a chi-square law with 1 degree of freedom. Because the axes come from all sites, a phenotype that differs between groups only through ancestry has no correlation left after the step.

## Example

Four individuals at four sites. Individuals 1 and 2 come from one group and 3 and 4 from another:

$$G = \begin{pmatrix} 2 & 2 & 0 & 1 \\ 2 & 1 & 0 & 0 \\ 0 & 0 & 2 & 1 \\ 1 & 0 & 2 & 2 \end{pmatrix}.$$

The column means are $1.25, 0.75, 1, 1$, so $p = (0.625, 0.375, 0.5, 0.5)$, and the scale factors are $\sqrt{0.234375} = 0.4841$ for the first two sites and $0.5$ for the last two. The first row of $M$ is $(1.5492, 2.5820, -2, 0)$. Then

$$X = \begin{pmatrix} 3.2667 & 1.9333 & -3.0 & -2.2 \\ 1.9333 & 2.6667 & -2.2 & -2.4 \\ -3.0 & -2.2 & 3.2667 & 1.9333 \\ -2.2 & -2.4 & 1.9333 & 2.6667 \end{pmatrix}.$$

Each row sums to 0, because each column of $M$ has mean 0. The eigenvalues are $9.8433$, $1.4900$, $0.5333$ and $0$, with sum $11.8667$, the trace. The first axis is $v_1 = (0.535, 0.463, -0.535, -0.463)$: it puts individuals 1 and 2 on one side and 3 and 4 on the other, and it carries $9.8433 / 11.8667 = 83$ percent of the total variance. The second axis $(-0.463, 0.535, 0.463, -0.535)$ separates the members within each group. The eigenvector of eigenvalue 0 is $(0.5, 0.5, 0.5, 0.5)$, the direction removed by centering.

## Correctness

Three facts make the method correct. First, after centering, $X \mathbf 1 = 0$, so $X$ is symmetric positive semidefinite with rank at most $n - 1$, and every eigenvector with a positive eigenvalue is orthogonal to $\mathbf 1$: the coordinates of each axis sum to zero. Second, if $\lambda_k > \lambda_{k+1}$ and the start $Q$ has a nonsingular projection on the top $k$ eigenvectors, which a Gaussian start has with probability 1, then the span of $Q$ after $t$ rounds tends to the span of $v_1, \ldots, v_k$, and the error falls like $(\lambda_{k+1} / \lambda_k)^t$. Third, when the span of $Q$ is the top eigenspace, the Rayleigh-Ritz step of line L11 returns the exact eigenpairs. For EIGENSTRAT, the residual step is the orthogonal projection away from the span of $\mathbf 1, v_1, \ldots, v_k$, because these vectors are orthonormal (with $\mathbf 1$ scaled) by the first fact. The chi-square law of the statistic is an approximation, not a theorem. The full proof is below.

## Complexity

- **Normalization.** Lines L1 to L3 take $O(n m)$ time.
- **The matrix $X$.** Line L4 takes $O(n^2 m)$ time and $O(n^2)$ space. This term dominates when $m$ is much larger than $n$, which is usual.
- **Iteration.** Each round of lines L7 to L9 costs $O(n^2 k + n k^2)$. The number of rounds $T$ grows like $\log(1/\varepsilon) / \log(\lambda_k / \lambda_{k+1})$, so a small gap between $\lambda_k$ and $\lambda_{k+1}$ makes it slow.
- **Rayleigh-Ritz.** Line L11 costs $O(n^2 k + k^3)$.
- **Large samples.** For hundreds of thousands of individuals, $X$ does not fit in memory. Programs then multiply by $M$ and $M^{\mathsf T}$ without forming $X$, at $O(n m k)$ per round.

## Properties

- **No model.** The method fits no ancestry model. The axes are summaries of the data, and their meaning has to be read from the sample labels.
- **Genealogy.** McVean (2009) showed that the expected $X$ is a function of the mean coalescence times between pairs of individuals. So the axes reflect the genealogy of the sample, which is also shaped by sample sizes.
- **Sample composition.** A group with many samples pulls the first axes toward its own internal variation, and a small group can stay hidden.
- **The number of axes.** Patterson and coauthors rescale $\lambda_1$ so that the eigenvalues sum to $n - 1$, and compare it, after centering and scaling, with the Tracy-Widom law of the largest eigenvalue of a random matrix. The test is then repeated on the remaining eigenvalues. The 5 percent point of the law is $0.9794$.
- **Admixture.** An individual with ancestry from two groups lies between their clusters, near the point given by its ancestry proportions, when the groups are well separated.

## Variants and improvements

- **Projection.** Compute the axes on reference samples and project new samples onto them, with $v_c$ replaced by $M_{\text{new}} M^{\mathsf T} v_c / (m' \lambda_c)$. Projected samples shrink toward the center, and some programs correct for this shrinkage.
- **LD pruning.** Correlated nearby sites can make an axis follow one region of the genome, such as an inversion. Keeping only weakly correlated sites, or regressing out the previous sites, avoids this.
- **Randomized and Lanczos methods.** For very large $n$, block Lanczos or randomized subspace iteration on $M$ gives the top axes in $O(n m k)$ time per pass.
- **Model-based alternatives.** [Maximum likelihood admixture estimation](/maximum-likelihood-admixture-estimation/) and the [Pritchard-Stephens-Donnelly model](/pritchard-stephens-donnelly-model/) give ancestry proportions with a direct meaning. [Mixed models](/mixed-model-association/) use the full matrix $X$ as a relatedness matrix instead of a few axes.

## When to use it

Use it as the first look at a new genotype data set, to find structure, outliers and duplicate or mislabeled samples, and to choose covariates for a [genome-wide association study](/genome-wide-association-study/). Use model-based methods when you need ancestry proportions, and mixed models when the sample has close relatives or fine structure.

## Pitfalls

- **Monomorphic sites.** A site with $p_j = 0$ or $1$ has a zero scale factor and must be dropped before the division.
- **Relatives.** Close relatives form their own axes. Remove one of each related pair before computing the axes, and project the others.
- **Reading axes as migrations.** Gradients and clusters on a plot can come from different histories, and the same history can give different plots with different sample sizes. The axes do not identify a demographic model.
- **Sign and order.** The sign of an eigenvector is arbitrary, and close eigenvalues can swap order between runs. Compare runs up to sign and rotation.
- **Too few axes.** EIGENSTRAT with too few axes leaves stratification in the test; too many costs a little power. [Genomic control](/genomic-control/) on the test statistics is a check.

## Implementations

## History

Cavalli-Sforza and coauthors used principal components of population allele frequencies from the late 1970s to draw maps of human genetic variation. For individual genotypes at many sites, Patterson, Price and Reich (2006) set the normalization used here, gave the smartpca program and proposed the Tracy-Widom test. In the same year Price and coauthors introduced EIGENSTRAT for association studies. Novembre and coauthors (2008) showed that the first two axes of European genotypes resemble a map of Europe, and McVean (2009) linked the axes to coalescence times.

## References
