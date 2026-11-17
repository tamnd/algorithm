---
tag: GFD87X
kind: technique
slug: genome-wide-association-study
name: Genome-wide association study
aliases:
- GWAS
- genome-wide association scan
area: biology/population-genetics
level: core
summary: "Tests each of many variants across the genome for association with a trait, one at a time, and keeps the variants that pass a genome-wide significance threshold."
prereqs: [chi-squared-test-of-independence, linear-regression, bonferroni-correction]
see_also: [genomic-control, mixed-model-association, ld-score-regression, genotype-imputation, likelihood-ratio-test, genetic-principal-components, logistic-regression, linkage-disequilibrium]
sources:
  - paper: doi:10.1016/j.ajhg.2017.06.005
    title: Peter M. Visscher, Naomi R. Wray, Qian Zhang, Pamela Sklar, Mark I. McCarthy, Matthew A. Brown and Jian Yang, 10 years of GWAS discovery, biology, function, and translation, American Journal of Human Genetics 101(1), 2017
    locator: pp. 5-22 (a review of the design, the results and the uses of GWAS from 2007 to 2017)
  - paper: doi:10.1126/science.273.5281.1516
    title: Neil Risch and Kathleen Merikangas, The future of genetic studies of complex human diseases, Science 273(5281), 1996
    locator: pp. 1516-1517 (the argument that association tests over the whole genome have more power than linkage scans for small effects, and a significance level for about a million tests)
  - paper: doi:10.1002/gepi.20303
    title: Itsik Pe'er, Roman Yelensky, David Altshuler and Mark J. Daly, Estimation of the multiple testing burden for genomewide association studies of nearly all common variants, Genetic Epidemiology 32(4), 2008
    locator: pp. 381-385 (the effective number of independent tests of common variants, estimated from dense genotype data)
---

A genome-wide association study (GWAS) tests each of hundreds of thousands to millions of genetic variants for association with a trait, one variant at a time. For a case-control trait, each test compares the allele frequencies of cases and controls, for example with a [chi-squared test](/chi-squared-test-of-independence/) on a table of allele counts or with [logistic regression](/logistic-regression/). For a quantitative trait, each test is a [linear regression](/linear-regression/) of the trait on the genotype. Because so many tests are made, only variants that pass a very small threshold, by convention $p < 5 \times 10^{-8}$, are reported. A significant variant is usually not the cause itself but is in [linkage disequilibrium](/linkage-disequilibrium/) with it, so a GWAS finds regions, not genes.

## In plain words

Take many people with a disease and many without it, and read a large number of single-letter positions in the DNA of each. At every position, check whether one letter is more common in the people with the disease. Most positions show only small random differences. Because so many positions are checked, some will show large differences by chance alone, so a difference counts only if it is far too large to be explained by chance. A position that passes this strict check marks a region of the genome that affects the disease. The position itself is often only a neighbour of the real cause. People of different ancestry can differ at many positions for reasons that have nothing to do with the disease, so the study must correct for ancestry.

## When it applies

- The trait is measured in many people, thousands to hundreds of thousands, with genotypes at many variants across the genome. The effects of single common variants on complex traits are small, so small samples find almost nothing.
- The aim is to find regions of the genome with an effect, without a prior guess of which genes matter. A study of candidate genes tests only the genes chosen in advance.
- The variants are common enough to be tested one at a time. For rare variants, single tests have little power, and tests that pool the variants of a gene are used.
- The samples are unrelated people of similar ancestry, or the method corrects for relatedness and structure, as [mixed model association](/mixed-model-association/) does.

## The template

1. **Genotype and check the data.** Remove samples and variants with many missing calls, variants far from Hardy-Weinberg proportions in the controls, and duplicate or related samples, unless the model handles relatedness.
2. **Impute.** Fill in variants that were not on the array from a reference panel by [genotype imputation](/genotype-imputation/), so that the scan covers the common variants of the genome and studies with different arrays can be combined.
3. **Control for structure.** Compute the leading [genetic principal components](/genetic-principal-components/) of the genotypes and use them as covariates, or fit a mixed model with a relationship matrix.
4. **Test each variant.** For variant $j$ with genotype or dosage $g_{ij}$ of person $i$, fit $y_i = \alpha + \beta_j g_{ij} + \gamma^\top c_i + e_i$ for a quantitative trait, or the same model on the log-odds scale for a binary trait, with covariates $c_i$. Test $\beta_j = 0$ with a Wald test, a score test or a [likelihood ratio test](/likelihood-ratio-test/). Without covariates, a binary trait can be tested with a chi-squared test on the $2 \times 2$ table of allele counts, or with the Cochran-Armitage trend test on the $2 \times 3$ table of genotype counts.
5. **Check calibration.** Compare the distribution of the statistics with the null law in a quantile-quantile plot. The inflation factor $\lambda$ of [genomic control](/genomic-control/) and the intercept of [LD score regression](/ld-score-regression/) show whether confounding remains.
6. **Apply the threshold.** Report variants with $p < 5 \times 10^{-8}$. This is about a [Bonferroni correction](/bonferroni-correction/) of a family-wise error rate of $0.05$ for one million independent tests, $0.05 / 10^6 = 5 \times 10^{-8}$.
7. **Group the hits into loci.** Nearby significant variants are correlated through linkage disequilibrium and usually mark one signal. Keep the lead variant of each region, and test the others conditional on it to find independent signals.
8. **Replicate.** Test the lead variants in an independent sample, or combine studies in a meta-analysis.

## Classic examples

- **An allelic test by hand.** A study has 1,000 cases and 1,000 controls, so 2,000 allele copies in each group. The risk allele is seen 600 times in cases and 500 times in controls, frequencies $0.30$ and $0.25$. The table is $\begin{pmatrix} 600 & 1400 \\ 500 & 1500 \end{pmatrix}$, with $n = 4000$. The statistic is $\chi^2 = n (ad - bc)^2 / ((a + b)(c + d)(a + c)(b + d)) = 4000 \cdot 200{,}000^2 / (2000 \cdot 2000 \cdot 1100 \cdot 2900) = 4000/319 = 12.54$ with 1 degree of freedom, so $p \approx 4.0 \times 10^{-4}$. The allelic odds ratio is $(600 \cdot 1500)/(1400 \cdot 500) = 9/7 = 1.29$. This would be a clear result for one test, but it is far from $5 \times 10^{-8}$, which needs $\chi^2 > 29.72$.
- **The same effect in a larger sample.** With 5,000 cases and 5,000 controls and the same frequencies, every count is 5 times larger. $\chi^2$ is proportional to $n$ when the frequencies are fixed, so $\chi^2 = 20{,}000/319 = 62.70$ and $p \approx 2.4 \times 10^{-15}$. The effect passes the threshold easily. This is why GWAS sample sizes grew from thousands to hundreds of thousands.
- **The threshold.** Risch and Merikangas (1996) argued that association tests over the genome have more power than linkage scans for genes of small effect, and that about a million tests need a level near $5 \times 10^{-8}$. Pe'er and coworkers (2008) estimated from dense genotype data that the common variants of European-ancestry samples behave like about a million independent tests, which supports the same value. The level is a convention, and it is too lax for rare variants and for samples of African ancestry, which have less linkage disequilibrium and so more independent tests.
- **The first large scans.** By 2007, studies of thousands of cases and controls with arrays of several hundred thousand SNPs had found the first reproducible loci for many common diseases. Visscher and coworkers (2017) review the thousands of loci found in the ten years that followed.

## Variations

- **Mixed model association.** Fit a [linear mixed model](/linear-mixed-model/) with a genetic relationship matrix, which corrects for relatedness and structure together and gains power for polygenic traits, see [mixed model association](/mixed-model-association/).
- **Meta-analysis.** Combine the effect estimates of many studies with inverse-variance weights, which gives the power of the combined sample without sharing individual data.
- **Rare variant tests.** Pool the rare variants of a gene into one burden score, or test the variance of their effects, because single tests of rare variants have little power.
- **Phenome-wide scans.** Test one variant against many traits, the reverse design.
- **Summary-statistic methods.** [LD score regression](/ld-score-regression/) estimates heritability and confounding from the statistics alone, and fine-mapping methods find the likely causal variants of a locus.

## Pitfalls

- **Population stratification.** If cases and controls differ in ancestry, every variant whose frequency differs between the ancestries looks associated. Principal components, mixed models and [genomic control](/genomic-control/) are the remedies, and the inflation factor should be checked.
- **Inflation from polygenic signal.** For a highly polygenic trait in a large sample, many statistics are inflated by true small effects. A large $\lambda$ then does not prove confounding, and dividing by it removes true signal. LD score regression separates the two.
- **The winner's curse.** The effect estimate of a variant chosen because it passed the threshold is biased away from zero. Estimate effects in a replication sample.
- **The lead variant is not the cause.** The most significant variant of a locus is often a marker in linkage disequilibrium with the causal variant, and the nearest gene is often not the gene that it acts on.
- **Batch effects.** Cases and controls genotyped in different batches or on different arrays can differ in genotype calls. Such artefacts can pass the threshold and are found by checking the cluster plots of the top variants.
- **Multiple testing beyond the scan.** Testing many traits, models or subgroups adds to the number of tests that the threshold assumes.

## Exercises

1. For the table of the first example, compute the expected counts under independence and check that $\sum (O - E)^2 / E$ gives the same $\chi^2 = 4000/319$.
2. Show that if all four counts of a $2 \times 2$ table are multiplied by $c$, the chi-squared statistic is multiplied by $c$.
3. For a quantitative trait, six people have genotypes $0, 0, 1, 1, 2, 2$ and trait values $1, 2, 2, 3, 3, 4$. Compute the least squares slope of the trait on the genotype and explain what it means.
4. A study tests 2 million imputed variants, of which about 1 million are independent. Explain why a threshold of $0.05 / (2 \times 10^6)$ is stricter than needed, and why $5 \times 10^{-8}$ is still used.
5. Two populations have allele frequencies $0.2$ and $0.6$ at a SNP with no effect on the trait. Cases are 70% from the first population and controls 30%. Compute the allele frequencies of cases and controls, and explain the false association.

## References
