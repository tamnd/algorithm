---
tag: Q44QVJ
kind: algorithm
slug: snp-heritability-estimation
name: SNP heritability estimation
aliases:
- GREML
- GCTA-GREML
- genomic-relatedness-based restricted maximum likelihood
area: biology/population-genetics
level: advanced
summary: "Estimates the fraction of trait variance explained by all genotyped SNPs, by REML in a mixed model whose random effect has the genomic relationship matrix as covariance."
model: real-ram
complexity:
  vars: {n: the number of individuals, m: the number of SNPs, r: the number of relationship matrices, t: the number of iterations}
  time: {worst: Θ(n^2 m + t (n^3 + r n^2)), average: Θ(n^2 m + t (n^3 + r n^2)), best: Θ(n^2 m + n^3)}
  space: {extra: Θ(r n^2)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2010
  people: [Jian Yang, Beben Benyamin, Peter M. Visscher]
  note: "Yang and coworkers fitted a mixed model with a relationship matrix from 294,831 SNPs to the height of 3,925 unrelated people in 2010, and found that the SNPs explain about 45% of its variance."
prereqs: [linear-mixed-model, restricted-maximum-likelihood, fisher-scoring]
see_also: [mixed-model-association, ld-score-regression, kinship-coefficient, henderson-mixed-model-equations, expectation-maximization, newton-raphson-method, delta-method, cholesky-decomposition]
sources:
  - paper: doi:10.1038/ng.608
    title: Jian Yang, Beben Benyamin, Brian P. McEvoy, Scott Gordon, Anjali K. Henders, Dale R. Nyholt, Pamela A. Madden, Andrew C. Heath, Nicholas G. Martin, Grant W. Montgomery, Michael E. Goddard and Peter M. Visscher, Common SNPs explain a large proportion of the heritability for human height, Nature Genetics 42(7), 2010
    locator: pp. 565-569 (the model with a SNP relationship matrix and the height estimate)
  - paper: doi:10.1016/j.ajhg.2010.11.011
    title: Jian Yang, S. Hong Lee, Michael E. Goddard and Peter M. Visscher, GCTA, a tool for genome-wide complex trait analysis, American Journal of Human Genetics 88(1), 2011
    locator: pp. 76-82 (the genomic relationship matrix and the REML fit with the average information algorithm)
  - paper: doi:10.2307/2533274
    title: Arthur R. Gilmour, Robin Thompson and Brian R. Cullis, Average information REML, an efficient algorithm for variance parameter estimation in linear mixed models, Biometrics 51(4), 1995
    locator: from p. 1440 (the average information matrix as the mean of the observed and expected information)
---

SNP heritability estimation measures how much of the variance of a trait the genotyped SNPs explain together, without finding any single SNP. It fits a [linear mixed model](/linear-mixed-model/) in which the genetic part of the trait has the genomic relationship matrix as covariance, and estimates the two variance components by [restricted maximum likelihood](/restricted-maximum-likelihood/). The usual solver is the average information algorithm, a Newton-type method whose curvature matrix is cheap to compute. The ratio of the genetic component to the total is the SNP heritability $h^2_{\mathrm{SNP}}$.

## In plain words

Two unrelated people still share a little more or a little less of their genome than average. If the trait is partly genetic, pairs who share more should also have slightly more similar trait values. The method measures the genetic similarity of every pair from the SNPs, then asks how strongly trait similarity follows it. A strong link means the SNPs explain much of the trait. The answer comes from a likelihood that splits the total variance into a genetic part and a noise part. An iterative search finds the split under which the observed traits are most probable. Each step uses the slope of the likelihood and a cheap measure of its curvature. The search stops when the split no longer changes.

## The problem

**Input.** A trait $y \in \mathbb R^n$, a matrix $X$ of $p$ fixed covariates with full column rank, and $r \ge 1$ symmetric relationship matrices $A_1, \dots, A_r$ of size $n \times n$. With one matrix, $A$ is the genomic relationship matrix, with entries $A_{jk} = \frac1m \sum_i (x_{ji} - 2p_i)(x_{ki} - 2p_i) / (2p_i(1 - p_i))$ off the diagonal for genotypes $x \in \{0, 1, 2\}$ and allele frequencies $p_i$.

**Model.**

$$y = X \beta + g_1 + \dots + g_r + e, \qquad g_k \sim N(0, \sigma_k^2 A_k), \qquad e \sim N(0, \sigma_e^2 I),$$

so $V = \operatorname{Var}(y) = \sum_k \sigma_k^2 A_k + \sigma_e^2 I$. Write $\theta = (\sigma_1^2, \dots, \sigma_r^2, \sigma_e^2)$ and $V_k = \partial V / \partial \theta_k$, which is $A_k$ or $I$.

**Output.** The REML estimate $\hat\theta$, the SNP heritability $h^2_{\mathrm{SNP}} = \sum_k \hat\sigma_k^2 / (\sum_k \hat\sigma_k^2 + \hat\sigma_e^2)$ and its standard error.

The REML log-likelihood is, up to a constant,

$$\ell_R(\theta) = -\tfrac12 \bigl[\log\det V + \log\det(X^\top V^{-1} X) + y^\top P y\bigr], \qquad P = V^{-1} - V^{-1} X (X^\top V^{-1} X)^{-1} X^\top V^{-1}.$$

## The algorithm

```pseudo id=main
GREML(y, X, A_1, ..., A_r)
L1  θ ← (v, ..., v) with v = Var(y)/(r + 1)
L2  V ← Σ_k θ_k A_k + θ_e I; P ← V⁻¹ - V⁻¹X(XᵀV⁻¹X)⁻¹XᵀV⁻¹; ℓ ← ℓ_R(θ)
    repeat
L3      d_k ← -½ [tr(P V_k) - yᵀ P V_k P y] for each component k
L4      AI_kl ← ½ yᵀ P V_k P V_l P y
L5      Δ ← AI⁻¹ d (in the first round, the EM-REML step Δ_k = θ_k² (yᵀPV_kPy - tr(PV_k))/n)
L6      θ ← θ + Δ, halving Δ until V is positive definite and ℓ_R does not go down; update P, ℓ
    until the gain in ℓ_R is below a tolerance
L7  h² ← Σ_k θ_k / (Σ_k θ_k + θ_e)
L8  return θ, h², and the standard error of h² from AI⁻¹ by the delta method
```

The vector $d$ of line L3 is the gradient of $\ell_R$. The matrix of line L4 is the mean of the observed and the expected information, but it needs only the $r + 1$ vectors $V_k P y$, not the traces of products of $n \times n$ matrices. Components that the step would make negative are set to a small positive floor, $10^{-6} \operatorname{Var}(y)$ in the code. The standard error of line L8 uses the gradient of $h^2$ in $\theta$, $\sigma_e^2 / \sigma_P^4$ for each genetic component and $-\sum_k \sigma_k^2 / \sigma_P^4$ for $\sigma_e^2$, with $\sigma_P^2$ the total.

## Example

Take three pairs of identical twins, so that $A$ is 1 within a pair and 0 between pairs, with the trait values $(1, 3)$, $(5, 7)$ and $(9, 11)$ and only an intercept in $X$. With this $A$ the model is the balanced one-way layout, and REML has the closed form of the analysis of variance.

- The pair means are 2, 6 and 10, and the grand mean is 6.
- Within pairs, each pair has the sum of squares 2, so $\mathrm{MSW} = 6/3 = 2$.
- Between pairs, $\mathrm{SSB} = 2 (16 + 0 + 16) = 64$ with 2 degrees of freedom, so $\mathrm{MSB} = 32$.
- So $\hat\sigma_e^2 = \mathrm{MSW} = 2$, $\hat\sigma_g^2 = (\mathrm{MSB} - \mathrm{MSW})/2 = 15$, and $h^2 = 15/17 = 0.882$.

The code starts at $\theta = (7, 7)$ from $\operatorname{Var}(y) = 14$ and reaches $(15, 2)$ in 7 rounds. At the estimate, $\mathrm{AI}^{-1}$ has the diagonal $770/3$ and $8/3$, which are $2\,\mathrm{MSB}^2/(2 \cdot 4) + 2\,\mathrm{MSW}^2/(3 \cdot 4)$ and $2\,\mathrm{MSW}^2/3$, the sampling variances of the two estimates. The delta method gives the standard error 0.143 for $h^2$.

## Correctness

Differentiating $\log\det V$, $\log\det(X^\top V^{-1} X)$ and $y^\top P y$ with the identity $\partial P / \partial \theta_k = -P V_k P$ gives the score of line L3. Because $V$ is linear in $\theta$, the observed information is $-\frac12 \operatorname{tr}(P V_k P V_l) + y^\top P V_k P V_l P y$ and the expected information is $\frac12 \operatorname{tr}(P V_k P V_l)$, so their mean is the matrix of line L4. This matrix is a Gram matrix in the semidefinite form $P$, so when it is positive definite the step $\mathrm{AI}^{-1} d$ points uphill, and halving it in line L6 ends with $\ell_R$ not lower than before. A limit point in the interior with a positive definite AI matrix therefore has $d = 0$, a stationary point of the REML likelihood. The full proof is below.

## Complexity

- **Relationship matrix.** Building $A$ from $m$ SNPs costs $\Theta(n^2 m)$, once.
- **Each round.** A Cholesky factor and the inverse of $V$ cost $\Theta(n^3)$. Forming $P$ costs $O(n^2 p)$, and the score and the AI matrix cost $O(r n^2)$ for the products $V_k P y$ and the traces, and $O(r^2 n)$ for the entries of AI.
- **Rounds.** Near the maximum the method converges like a Newton method, and a few to a few tens of rounds are usual. The tests use at most a few tens.
- **Space.** $\Theta(r n^2)$ for the matrices.
- **One matrix.** With $r = 1$, an eigendecomposition of $A$ makes $V$ diagonal for every $\theta$, as in [mixed model association](/mixed-model-association/). Each round then costs $O(n p^2)$ after one $\Theta(n^3)$ step.

## Properties

- **Increasing likelihood.** With the step halving of line L6, $\ell_R$ never goes down from one round to the next.
- **Invariant to the fixed effects.** REML uses only the error contrasts $K^\top y$ with $K^\top X = 0$, so the estimate does not depend on $\beta$.
- **A lower bound on heritability.** The SNPs capture the causal variants only through linkage disequilibrium, so $h^2_{\mathrm{SNP}}$ is in general below the narrow-sense heritability from family studies.
- **Partitioning.** With one matrix per chromosome, per class of allele frequency or per annotation, the components add up to the total SNP heritability.
- **Standard error falls like $1/n$.** For unrelated people the off-diagonal entries of $A$ are small, and the information about $\sigma_g^2$ grows with the number of pairs, $n^2$.

## Variants and improvements

- **Several components.** Fit $r > 1$ matrices at once to split the SNP heritability between genome regions, as in the test with two halves of the SNPs.
- **Spectral form.** With one matrix, rotate the data by the eigenvectors of $A$ and search over the variance ratio, as for association testing.
- **Case-control traits.** Fit the linear model to the 0/1 status, then transform the estimate to the liability scale with the disease prevalence and the case fraction of the sample.
- **Methods of moments.** Haseman-Elston regression and its multi-component forms regress the products of trait values on the entries of $A$. They need no matrix inverse and scale to biobanks, with larger standard errors.
- **Summary statistics only.** [LD score regression](/ld-score-regression/) estimates the SNP heritability from association statistics and a reference panel, without individual genotypes.

## When to use it

- Measuring how much of a trait the genotyped SNPs explain, in a sample of individual-level genotypes.
- Comparing the SNP heritability with the pedigree heritability, to see how much is missing from the SNPs.
- Splitting the genetic variance between chromosomes, functional annotations or allele frequency classes.
- Estimating the genetic correlation of two traits with a bivariate model on the same samples.

## Pitfalls

- **Close relatives.** With relatives in the sample, shared environment and causal variants not tagged by the SNPs both raise the similarity of relatives, and the estimate is no longer a SNP heritability. Remove one person from each pair above a small relatedness cutoff.
- **Population structure.** Ancestry differences show in $A$ and can follow the trait for non-genetic reasons. Add principal components as covariates.
- **Boundary estimates.** With small samples, the maximum is often at $\sigma_g^2 = 0$ or $\sigma_e^2 = 0$. The usual standard error and the chi-squared test of the likelihood ratio do not apply at the boundary.
- **A matrix that is not positive semidefinite.** The genomic relationship matrix with the usual diagonal can have small negative eigenvalues. The step must keep $V$ positive definite.
- **Linkage disequilibrium and frequency.** The estimate assumes that every standardized SNP has the same expected contribution. When this is wrong, for example because rare SNPs or SNPs in regions of low linkage disequilibrium contribute more, the estimate is biased.
- **Cost.** The $\Theta(n^3)$ per round limits the exact method to tens of thousands of people.

## Implementations

## History

Before 2010, the genome-wide association studies of height had found SNPs that together explained only a few percent of its variance, although family studies put its heritability near 80%. Yang and coworkers (2010) asked how much all SNPs explain together and fitted a mixed model with a relationship matrix from 294,831 SNPs to 3,925 unrelated people. They found about 45%, which showed that much of the missing heritability is in many SNPs of small effect, not detected one by one. The GCTA software (Yang and coworkers 2011) made the method a standard tool. Its REML solver is the average information algorithm of Gilmour, Thompson and Cullis (1995), from animal breeding, where mixed models with pedigree relationship matrices had been fitted for decades.

## References
