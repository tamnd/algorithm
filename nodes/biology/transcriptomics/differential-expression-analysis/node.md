---
tag: JWJYYT
kind: problem
slug: differential-expression-analysis
name: Differential expression analysis
aliases:
- DE analysis
- differential gene expression
area: biology/transcriptomics
level: core
summary: Find the genes whose expression differs between conditions beyond biological variation, from few replicates and many genes.
prereqs: [library-size-normalization, negative-binomial-count-model, false-discovery-rate]
see_also: [negative-binomial-count-model, dispersion-shrinkage, moderated-t-statistic, benjamini-hochberg-procedure, storey-q-value, generalized-linear-model, gene-set-enrichment-analysis, over-representation-analysis]
sources:
  - paper: doi:10.1186/s13059-014-0550-8
    title: Michael I. Love, Wolfgang Huber and Simon Anders, Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2, Genome Biology 15(12) (2014), article 550
    locator: the negative binomial GLM per gene with size factors as offsets, the shrunk dispersions, the Wald test and the likelihood ratio test, and the Benjamini-Hochberg adjustment after independent filtering
  - paper: doi:10.1093/bioinformatics/btp616
    title: Mark D. Robinson, Davis J. McCarthy and Gordon K. Smyth, edgeR, a Bioconductor package for differential expression analysis of digital gene expression data, Bioinformatics 26(1) (2010), pages 139 to 140
    locator: the edgeR package, with TMM normalization, negative binomial dispersions moderated by empirical Bayes, and the exact test
  - paper: doi:10.1093/nar/gks042
    title: Davis J. McCarthy, Yunshun Chen and Gordon K. Smyth, Differential expression analysis of multifactor RNA-Seq experiments with respect to biological variation, Nucleic Acids Research 40(10) (2012), pages 4288 to 4297
    locator: GLMs for designs with several factors, the biological coefficient of variation, and the trended dispersion
  - paper: doi:10.2202/1544-6115.1027
    title: Gordon K. Smyth, Linear models and empirical Bayes methods for assessing differential expression in microarray experiments, Statistical Applications in Genetics and Molecular Biology 3(1) (2004), Article 3
    locator: linear models per gene with contrasts, and the moderated t and F statistics
  - paper: doi:10.1186/gb-2014-15-2-r29
    title: Charity W. Law, Yunshun Chen, Wei Shi and Gordon K. Smyth, voom, precision weights unlock linear model analysis tools for RNA-seq read counts, Genome Biology 15(2) (2014), article R29
    locator: log counts per million with weights from the mean-variance trend, so that the linear model methods of limma apply to RNA-seq
  - paper: doi:10.1186/gb-2010-11-10-r106
    title: Simon Anders and Wolfgang Huber, Differential expression analysis for sequence count data, Genome Biology 11(10) (2010), article R106
    locator: the negative binomial model with a mean-dependent variance, and the exact test between two conditions
---

Differential expression analysis is the problem of finding the genes whose mean expression differs between conditions, such as treated and untreated samples, by more than the variation between biological replicates explains. The data are thousands of genes measured in a few samples, often three per condition. So each gene has too few replicates for a reliable test on its own, and testing thousands of genes at once produces many false positives unless the error rate is controlled over the whole list. The standard solution for RNA-seq is a [generalized linear model](/generalized-linear-model/) per gene with a [negative binomial](/negative-binomial-count-model/) distribution, size factors from [library size normalization](/library-size-normalization/) as offsets, a dispersion shared across genes by [dispersion shrinkage](/dispersion-shrinkage/), and [false discovery rate](/false-discovery-rate/) control over the genes. For microarrays and log-scale data, the [moderated t-statistic](/moderated-t-statistic/) plays the same role.

## In plain words

You grow cells with and without a drug, three dishes each, and count the RNA of every gene. You want the list of genes the drug changes. The trouble is that three dishes of the same kind already differ from each other, so a difference between the groups means something only if it is large compared with that natural spread. With only three dishes, the spread of a single gene is hard to measure, so methods borrow strength from the thousands of other genes. And with twenty thousand genes, some will look changed by pure chance, so you control the fraction of false hits in the final list instead of testing each gene as if it were the only one.

## Definition

**Input.** A matrix of counts $K_{gj} \ge 0$ for genes $g = 1, \dots, n$ and samples $j = 1, \dots, m$; a design matrix $X$ of size $m \times p$ that describes the conditions and other known factors, such as batch or donor; and a contrast $c \in \mathbb{R}^p$, or a set of coefficients, that states the comparison of interest.

**Model.** For each gene, the counts follow $E[K_{gj}] = s_jq_{gj}$ with $\ln q_{gj} = x_j^\top\beta_g$, where $s_j$ is the size factor of sample $j$ and $x_j$ is row $j$ of $X$. The variance is $\operatorname{Var}(K_{gj}) = \mu_{gj} + \alpha_g\mu_{gj}^2$, where $\alpha_g$ is the dispersion of gene $g$. Its square root is the biological coefficient of variation.

**Hypotheses.** For each gene, $H_{0g}: c^\top\beta_g = 0$. In a comparison of two groups, $c^\top\beta_g$ is the log fold change of gene $g$.

**Output.** A set $R$ of genes declared differentially expressed, usually with an estimate and a standard error of each log fold change, a p-value per gene, and an adjusted p-value. The requirement is on the whole list: the false discovery rate $E[V/\max(|R|, 1)]$, where $V$ is the number of true nulls in $R$, is at most a target $q$, such as 0.05 or 0.1.

**What makes it hard.** The number of residual degrees of freedom per gene, $m - p$, is small, so the gene-wise estimates of $\alpha_g$ or of the variance are poor. The number of tests $n$ is large, so the multiplicity correction is strong. The counts are discrete and their variance depends on their mean, so tests for normal data do not apply directly.

## Variants

- **Two groups.** The simplest design: $X$ has an intercept and a group indicator, and the test is on the group coefficient. edgeR also has an exact test for this case, which conditions on the total count of each gene.
- **Several factors.** Paired samples, batches or donors enter $X$ as extra columns. Putting a known batch in the design is the usual alternative to [batch effect correction](/batch-effect-correction/) before the analysis.
- **Several coefficients at once.** Time courses or several treatments are tested with a [likelihood ratio test](/likelihood-ratio-test/) of a reduced model, or with a moderated F test in limma.
- **A threshold on the effect.** Test $|c^\top\beta_g| \le \tau$ against $|c^\top\beta_g| > \tau$ instead of $c^\top\beta_g = 0$, which ranks genes by biological importance rather than by significance alone. Filtering a list of significant genes by fold change after the test does not control the error rate for this hypothesis.
- **Continuous data.** Microarray log intensities, or RNA-seq log counts with precision weights (voom), use linear models with the [moderated t-statistic](/moderated-t-statistic/).
- **Transcripts.** Differential expression of transcripts, or differential use of transcripts within a gene, uses estimated counts from [transcript abundance estimation](/transcript-abundance-estimation/), which carry extra uncertainty.
- **Single cells.** In [single-cell RNA sequencing](/single-cell-rna-sequencing/), cells from one donor are not independent replicates. Summing the counts of each donor into a pseudobulk sample and using the bulk methods treats the donors as the replicates.

## Examples

**Why biological variation matters.** Take one gene with mean count 100 in condition A and 150 in condition B, equal size factors, and 3 replicates per condition. The log fold change is $\ln 1.5 = 0.405$. By the [delta method](/delta-method/), the variance of the log of a group mean is about $(1/\mu + \alpha)/3$. With $\alpha = 0.1$, a biological coefficient of variation of 0.32, the standard error of the log fold change is $\sqrt{(0.01 + 0.1)/3 + (0.0067 + 0.1)/3} = 0.269$, so $z = 1.51$ and the two-sided p-value is 0.13. A [Poisson](/poisson-distribution/) model, with $\alpha = 0$, gives a standard error of 0.075, $z = 5.44$ and a p-value of $5 \times 10^{-8}$. The Poisson model ignores the variation between replicates, and it would call this gene, and many genes with no real change, highly significant.

**Why shrinkage matters.** Three genes, three samples per group, on the log scale:

| gene | difference | $s^2$ | t | p | moderated t | moderated p |
|---|---|---|---|---|---|---|
| 1 | 0.5 | 0.01 | 6.12 | 0.0036 | 3.54 | 0.0077 |
| 2 | 1.3 | 0.785 | 1.80 | 0.147 | 2.46 | 0.0391 |
| 3 | 0.35 | 0.0025 | 8.57 | 0.0010 | 2.65 | 0.0294 |

The ordinary t-test, on 4 degrees of freedom, ranks gene 3 first, only because its three values happen to be very close together. The moderated t-statistic uses a prior variance of 0.05 on 4 prior degrees of freedom, estimated from all genes, as computed on its page. It pulls gene 3's tiny variance up and gene 2's large variance down, and it ranks gene 1 first. The [Benjamini-Hochberg](/benjamini-hochberg-procedure/) adjusted p-values are 0.0230, 0.0391 and 0.0391 for genes 1, 2 and 3 with the moderated test, and 0.0054, 0.147 and 0.0031 with the ordinary test.

**Adjusted p-values and q-values.** The adjusted p-value of a gene is the smallest target $q$ at which the Benjamini-Hochberg procedure would reject it. It is not a [q-value](/storey-q-value/) in Storey's sense. A q-value also estimates the fraction $\pi_0$ of true nulls and is smaller by about that factor. Reports should say which of the two they give.

## Known algorithms

- **Negative binomial GLM with shrunk dispersions.** DESeq2 fits the model by [iteratively reweighted least squares](/iteratively-reweighted-least-squares/), shrinks the dispersions toward a trend over the mean, and tests with a [Wald test](/wald-test/) or a likelihood ratio test. Its results function applies Benjamini-Hochberg with a target of 0.1 by default, after independent filtering of genes with low mean counts. edgeR shares the dispersions by weighted likelihood and offers an exact test, a likelihood ratio test, and quasi-likelihood F tests.
- **Linear models with the moderated t-statistic.** limma fits a linear model per gene on log-scale data and shrinks the residual variances by empirical Bayes. With voom weights it applies to RNA-seq counts.
- **Rank-based tests.** The [Mann-Whitney U test](/mann-whitney-u-test/) or a [permutation test](/permutation-test/) per gene makes no distributional assumption, but needs many samples. It suits large cohorts, not three replicates.
- **Multiple testing.** The [Benjamini-Hochberg procedure](/benjamini-hochberg-procedure/) is the default. Storey's q-value and the [local false discovery rate](/local-false-discovery-rate/) are alternatives. All of them assume the p-values are valid, so they inherit any error of the model.

## Bounds

- **No replicates, no gene-wise variance.** With one sample per condition, $m - p = 0$, so the data of a gene say nothing about its own dispersion. Any test must take the dispersion from other genes or from an assumption. This is a theorem about the model, not a property of a method.
- **Permutation tests with few samples.** With $r$ samples per group, there are $\binom{2r}{r}$ ways to split the samples into two groups. A permutation p-value is at least $1/\binom{2r}{r}$, which is $1/20 = 0.05$ for $r = 3$. So, for any target $q < 0.05$, no gene can be called, whatever its counts. This is one reason why parametric models are used.
- **Detectable effect.** In a large-count approximation, the variance of a log fold change with $r$ replicates per group is about $2\alpha/r$. A two-sided z-test at level 0.05 with power 0.8 then detects a log fold change of about $2.80\sqrt{2\alpha/r}$. With $\alpha = 0.1$, this is a fold change of 2.06 for $r = 3$ and 1.49 for $r = 10$, before the multiplicity correction makes it larger. This is an approximation for planning, not a guarantee.
- **Error control.** Benjamini-Hochberg at target $q$ controls the false discovery rate at $q\,n_0/n$, where $n_0$ is the number of true nulls, when the p-values of the true nulls are independent or positively dependent. For genes in pathways, which are correlated, the conditions are not checked in practice, so the guarantee is a heuristic there.

## Reductions

- **To parallel tests.** The problem splits into $n$ tests of one gene each, linked only through the shared dispersion prior and the [multiple comparisons](/multiple-comparisons-problem/) correction. This is what makes the methods fast: the cost is linear in $n$.
- **From normalization.** Library size normalization enters as the offsets $\ln s_j$. An error in the size factors moves the log fold changes of all genes by the same amount, and so turns into many false calls in one direction.
- **To gene set analysis.** The output of the problem is the input of [over-representation analysis](/over-representation-analysis/), which takes the list $R$, and of [gene set enrichment analysis](/gene-set-enrichment-analysis/), which takes the ranking of all genes by their statistics.

## Applications

The problem appears in every study that compares conditions with transcriptomics: cases against controls, treated against untreated cells, tissues, developmental stages and time courses. It is used to find marker genes of cell types from single-cell data with pseudobulk samples, to find the targets of a transcription factor after it is knocked down, and, with the same count models, in proteomics, metagenomics and CRISPR screens, where the data are also counts per feature in few samples.

## References
