---
tag: E6NC45
kind: algorithm
slug: ld-score-regression
name: LD score regression
aliases:
- LDSC
- linkage disequilibrium score regression
area: biology/population-genetics
level: research
summary: "Regresses GWAS chi-squared statistics on the LD scores of the SNPs, so that the slope estimates the SNP heritability and the intercept measures confounding such as stratification."
model: real-ram
complexity:
  vars: {M: the number of SNPs, w: the number of SNPs in an LD window, n: the size of the reference panel, B: the number of jackknife blocks}
  time: {worst: Θ(M w n + B M), average: Θ(M w n + B M), best: Θ(M w n + B M)}
  space: {extra: Θ(M n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2015
  people: [Brendan K. Bulik-Sullivan, Po-Ru Loh, Hilary K. Finucane, Benjamin M. Neale]
  note: "Bulik-Sullivan and coworkers introduced LD score regression in 2015 to separate the inflation of GWAS statistics due to polygenic signal from the inflation due to confounding, from summary statistics only."
prereqs: [linkage-disequilibrium, genome-wide-association-study, weighted-least-squares]
see_also: [genomic-control, snp-heritability-estimation, mixed-model-association, jackknife-resampling, linear-regression, method-of-moments, genetic-principal-components]
sources:
  - paper: doi:10.1038/ng.3211
    title: Brendan K. Bulik-Sullivan, Po-Ru Loh, Hilary K. Finucane, Stephan Ripke, Jian Yang, Schizophrenia Working Group of the Psychiatric Genomics Consortium, Nick Patterson, Mark J. Daly, Alkes L. Price and Benjamin M. Neale, LD Score regression distinguishes confounding from polygenicity in genome-wide association studies, Nature Genetics 47(3), 2015
    locator: pp. 291-295 (equation 1, the LD scores from a 1 cM window, the regression weights and the block jackknife)
  - paper: doi:10.1111/j.0006-341X.1999.00997.x
    title: Bernie Devlin and Kathryn Roeder, Genomic control for association studies, Biometrics 55(4), 1999
    locator: pp. 997-1004 (the inflation factor that LD score regression refines)
---

LD score regression separates the two reasons why the test statistics of a [genome-wide association study](/genome-wide-association-study/) can be larger than expected under the null. Confounding, such as population stratification, raises all statistics by about the same amount. Polygenic signal raises the statistic of a SNP in proportion to how many other SNPs it tags through [linkage disequilibrium](/linkage-disequilibrium/), its LD score. A regression of the chi-squared statistics on the LD scores therefore estimates the SNP heritability from the slope and the confounding from the intercept. It needs only the summary statistics of the study and LD scores from a reference panel.

## In plain words

In a study of a trait with many small genetic effects, a marker near many other markers picks up the effects of all its neighbours, so its test statistic tends to be large. A marker with few neighbours picks up less. Problems in the study design, such as a mix of ancestries, make all markers look stronger by about the same amount, no matter how many neighbours they have. The method counts the neighbours of each marker in a reference sample. It then fits a straight line of the test statistic against this count. A steep line means much real genetic signal, and a line that starts high means a problem in the study. The method can also say how much of the trait the markers explain.

## The problem

**Input.** Association statistics $\chi^2_j$ for $J$ SNPs from a GWAS of $N$ people, the LD scores $l_j = \sum_k r^2_{jk}$ of these SNPs over a window, and the number $M$ of SNPs that the heritability refers to. In this version the LD scores are computed from a reference panel of genotypes with genetic positions.

**Model.** Under a polygenic model in which every standardized SNP has an effect of mean $0$ and variance $h^2 / M$,

$$\mathrm E[\chi^2_j \mid l_j] = \frac{N h^2}{M} l_j + N a + 1,$$

where $h^2$ is the SNP heritability and $N a$ is the inflation from confounding (equation 1 of Bulik-Sullivan and coworkers 2015).

**Output.** The estimates of $h^2$ and of the intercept $1 + N a$, their standard errors, and the ratio $(\text{intercept} - 1) / (\overline{\chi^2} - 1)$, the part of the mean inflation that the intercept explains.

## The algorithm

```pseudo id=main
LD-SCORE-REGRESSION(reference genotypes, positions, window, χ², N, M, B)
L1  for each SNP j, for each SNP k > j with pos_k - pos_j ≤ window do
L2      r̃² ← r²_jk - (1 - r²_jk)/(n - 2); add r̃² to l_j and l_k (each l_j starts at 1)
L3  h² ← M (mean χ² - 1)/(N mean l); a ← 1
    repeat for a few rounds
L4      w_j ← 1 / (max(l_j, 1) (a + N h² l_j / M)²)
L5      (a, b) ← weighted least squares fit of χ²_j = a + b l_j
L6      h² ← b M / N
L7  for each block t of consecutive SNPs, refit lines L5 and L6 without block t, with w fixed
L8  return h², a, their block jackknife standard errors, and (a - 1)/(mean χ² - 1)
```

Line L2 corrects the upward bias of the sample $r^2$ in a panel of $n$ people, about $1/n$ per pair, which adds up over a window. The first weight in line L4 lowers SNPs in high LD, whose statistics are counted many times through their neighbours. The second is the inverse of the variance of $\chi^2_j$ under the model. The block [jackknife](/jackknife-resampling/) of line L7 accounts for the correlation of nearby statistics.

**What this version leaves out.** The ldsc software reads LD scores computed in advance from a large panel, with a 1 cM window and a separate set of regression SNPs. It filters SNPs by allele frequency and very large statistics, can fix the intercept in a first step, partitions the heritability over annotations, estimates genetic correlations, and converts $h^2$ to the liability scale for case-control traits. None of this is in the code.

## Example

Take four SNPs with LD scores $1, 2, 3, 4$ and statistics $1.6, 1.9, 2.6, 2.9$, from a study with $N = 20{,}000$, and let $M = 10{,}000$. Use equal weights so that the fit is by hand.

- The means are $\bar l = 2.5$ and $\overline{\chi^2} = 2.25$.
- $\sum (l - \bar l)(\chi^2 - \overline{\chi^2}) = 0.975 + 0.175 + 0.175 + 0.975 = 2.3$ and $\sum (l - \bar l)^2 = 5$, so the slope is $0.46$ and the intercept is $2.25 - 0.46 \cdot 2.5 = 1.10$.
- $h^2 = 0.46 \cdot 10{,}000 / 20{,}000 = 0.23$.
- The ratio is $(1.10 - 1)/(2.25 - 1) = 0.08$. So 8% of the mean inflation is due to confounding, and the rest is polygenic signal.

The starting value of line L3 is $10{,}000 \cdot 1.25 / (20{,}000 \cdot 2.5) = 0.25$, which assumes an intercept of exactly 1. [Genomic control](/genomic-control/) would divide all four statistics by one factor and so treat all of the inflation as confounding.

## Correctness

Write the GWAS statistics as $z = \sqrt N R \beta + \varepsilon + \sqrt{N a}\, s$, with the LD matrix $R$, polygenic effects $\beta$ of variance $h^2/M$ each, sampling noise $\varepsilon$ of covariance $R$, and confounding $s$ of variance $1$ per SNP. The three parts are independent with mean $0$, so $\mathrm E[z_j^2] = N h^2 \sum_k R_{jk}^2 / M + 1 + N a$, which is the model equation. Weighted least squares with weights that depend only on the LD scores is linear in $\chi^2$, so it returns the slope and intercept of this line in expectation, and exactly when the points lie on the line. The corrected $r^2$ of line L2 has mean 0 for unlinked SNPs and mean $\rho^2 + O(1/n)$ in general, so the panel LD scores estimate $l_j$. The full proof is below.

## Complexity

- **LD scores.** Each SNP is paired with the $w$ SNPs of its window, and each correlation costs $\Theta(n)$ over the panel, so $\Theta(M w n)$. The scores are computed once per panel and reused for every trait.
- **Regression.** Each round costs $\Theta(J)$. The jackknife in the code refits from scratch, $\Theta(B J)$. With sums per block it costs $\Theta(J + B)$.
- **Space.** $\Theta(M n)$ for the standardized panel; the regression needs $\Theta(J)$.
- **No individual data.** The study enters only through $J$ statistics and its sample size.

## Properties

- **Separates confounding from polygenicity.** Under the model, confounding that does not depend on LD affects only the intercept.
- **LD from another sample.** The LD scores can come from a different, smaller sample of the same ancestry, because only the expected LD enters the model.
- **Depends on the panel.** If the panel ancestry differs from the study, the LD scores are wrong, and the slope and the intercept are both biased.
- **Less precise than REML.** With individual genotypes, [SNP heritability estimation](/snp-heritability-estimation/) by REML uses all pairs of people and has a smaller standard error.
- **A method of moments.** The fit matches the mean of $\chi^2_j$ to the model line and uses no likelihood, so it does not need the joint law of the statistics.

## Variants and improvements

- **Partitioned heritability.** Regress on several LD scores, one per functional annotation, to estimate how much heritability each annotation holds.
- **Genetic correlation.** Regress the product $z_{1j} z_{2j}$ of the statistics of two traits on $l_j$, to estimate their genetic correlation from summary statistics.
- **Constrained intercept.** Fix the intercept at 1 when the study is known to be free of confounding, to estimate $h^2$ with a smaller standard error.
- **Effects that depend on frequency and LD.** Models that let the effect variance depend on allele frequency and on LD fit real traits better.

## When to use it

- Checking whether the inflation of a GWAS comes from confounding or from polygenic signal, before or instead of [genomic control](/genomic-control/).
- Estimating SNP heritability when only summary statistics are available.
- Estimating the genetic correlation of many pairs of traits from published summary statistics.
- Finding the cell types and annotations enriched in heritability.

## Pitfalls

- **Small samples.** The standard errors are large unless $N$ is in the tens of thousands, because the signal per SNP is small.
- **Panel mismatch.** LD scores from a panel of a different ancestry, or computed on a different set of SNPs, bias both the slope and the intercept.
- **Regions of long-range LD.** The major histocompatibility complex and some inversions have LD beyond the window and very large statistics in many studies. They are usually left out.
- **Corrected statistics.** Statistics already divided by the genomic control factor have their intercept pushed down, and the slope with it.
- **Choice of $M$.** $h^2$ refers to the $M$ SNPs used to define the model, often the common SNPs of the panel. A different $M$ changes the estimate in proportion.

## Implementations

## History

The [genomic control](/genomic-control/) of Devlin and Roeder (1999) treats all inflation of the null statistics as confounding. With the large GWAS of the early 2010s it became clear that a polygenic trait inflates the statistics even in a well-controlled study, so a large inflation factor no longer showed that a study was confounded. Bulik-Sullivan and coworkers (2015) used the LD scores of the SNPs to separate the two, since only the polygenic signal grows with the LD score. They found that in many large studies most of the inflation is polygenic signal. The same idea, with products of statistics or with several LD scores, was then used for genetic correlations and for partitioning heritability by annotation.

## References
