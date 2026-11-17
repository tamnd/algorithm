---
tag: PVZKT3
kind: problem
slug: somatic-variant-calling
name: Somatic variant calling
aliases:
- tumor-normal variant calling
area: biology/read-mapping-and-variant-calling
level: advanced
summary: Find mutations present in tumour cells but not in the germline, from paired tumour and normal reads with low allele fractions.
prereqs: [variant-calling-problem, genotype-likelihood]
see_also: [haplotype-based-variant-calling, bayesian-genotype-calling, likelihood-ratio-test, binomial-distribution, fisher-exact-test, copy-number-segmentation, structural-variant-detection, false-discovery-rate]
sources:
  - paper: doi:10.1038/nbt.2514
    title: Kristian Cibulskis, Michael S. Lawrence, Scott L. Carter and others, Sensitive detection of somatic point mutations in impure and heterogeneous cancer samples, Nature Biotechnology 31(3), 2013
    locator: the sections on the variant detection statistic of the tumor (a log odds of a variant model against a reference model), the test of the normal sample, and the filters of artifacts
  - paper: doi:10.1093/bioinformatics/bts271
    title: Christopher T. Saunders, Wendy S. W. Wong, Sajani Swamy and others, Strelka, accurate somatic small-variant calling from sequenced tumor-normal sample pairs, Bioinformatics 28(14), 2012
    locator: the sections on the joint model of the allele frequencies of the tumor and the normal sample
---

Somatic variant calling finds the mutations that arose in a tumor during the life of a patient, and separates them from the variants that the patient inherited. The usual input is two sets of reads from the same person, one from the tumor and one from normal tissue such as blood. A variant that is in the tumor and not in the normal sample is somatic. The problem is harder than germline calling in two ways. A tumor sample is a mix of tumor and normal cells, and the tumor cells themselves form subclones, so a somatic mutation can be in a small and unknown share of the reads, not at the fixed fractions of 1/2 and 1. And the true mutations are rare, often a few per million bases, so even a small rate of artifacts gives many false calls.

## In plain words

A tumor grows from one cell that got some changes in its DNA, and it keeps getting more changes as it grows. To find them, read the DNA of the tumor and of healthy tissue from the same person. The changes that only the tumor has are the ones you want.

But a tumor sample also holds healthy cells, and the tumor cells are not all the same. So a real change may show up in only a few of the reads, about as rarely as a reading error. The task is to tell such rare real changes from errors, and to make sure the healthy tissue truly lacks them.

## Definition

**Input.** Reads of a tumor sample $T$ and of a matched normal sample $N$, mapped to a reference, with base qualities. Often also a panel of normal samples from other people, and a list of common germline variants.

**Output.** A list of somatic variants (substitutions, insertions and deletions, and in some tools larger events), each with a score, and often the allele fraction in the tumor.

**The allele fraction.** Let the purity $\rho$ be the share of tumor cells in the sample, and take a region with two copies in every cell. A mutation on one copy, in a subclone that holds a share $c$ of the tumor cells, is on $\rho c / 2$ of the reads in expectation. With $\rho = 0.4$ and a clonal mutation ($c = 1$), that is 0.2. With a subclone of $c = 0.25$, it is 0.05. Copy number changes in the tumor change this fraction again, which is why somatic calling and [copy number analysis](/copy-number-segmentation/) are often done together.

**A common form of the test.** At a candidate site with $k$ alternative reads among $n$ tumor reads, compare a model with allele fraction $f$ to the model $f = 0$. With base error rate $e$, an alternative read has probability $f(1 - e) + (1 - f)e/3$. The tumor score is the log odds

$$\mathrm{LOD}_T = \log_{10} \frac{P(\text{reads} \mid f = \hat f)}{P(\text{reads} \mid f = 0)}, \qquad \hat f = k / n,$$

and the normal sample must support $f = 0$ against a heterozygous germline variant, $f = 1/2$, with a score $\mathrm{LOD}_N$. MuTect (Cibulskis et al., 2013) uses two such scores with thresholds. This is a [likelihood ratio test](/likelihood-ratio-test/) with a fitted fraction, not a choice among three genotypes as in [Bayesian genotype calling](/bayesian-genotype-calling/).

## Variants

- **Tumor only.** Without a matched normal sample, germline variants must be removed with population databases and a panel of normals, and rare inherited variants remain a source of false calls.
- **Several samples of one tumor.** Samples from several places or times show which mutations are in all cells and which are in subclones.
- **Low fractions.** Liquid biopsies (DNA of the tumor in the blood) and early detection need fractions of 1% or less, which need very deep sequencing and molecular barcodes that tag each original DNA molecule.
- **Larger events.** Somatic [structural variants](/structural-variant-detection/) and copy number changes, often from the same data.

## Examples

All examples use base quality 30, so $e = 10^{-3}$.

- **A clonal mutation in an impure sample.** Purity 0.4 and 60 tumor reads give an expected fraction of 0.2. With 12 alternative reads, $\mathrm{LOD}_T = 28.7$: the variant is clear.
- **A few reads.** With 3 alternative reads of 60, $\mathrm{LOD}_T = 5.27$, and with 2 it is 3.15. The calls depend on the threshold, and 2 or 3 reads can also come from an artifact of the library that repeats, which no test of independent errors catches.
- **The normal sample.** With 30 normal reads that all show the reference allele, $\mathrm{LOD}_N = 30 \log_{10}((1 - e)/0.5) = 9.03$ against a heterozygous germline variant. If one of the 30 reads shows the alternative allele, $\mathrm{LOD}_N$ drops to 5.55; the variant may be germline, or the normal sample may hold a few tumor cells.

## Known algorithms

| method | approach |
|---|---|
| MuTect | a log odds of the tumor reads under a variant model against a reference model, a test of the normal sample, and filters of artifacts (Cibulskis et al., 2013) |
| Strelka | a joint Bayesian model of the allele frequencies in the tumor and in the normal sample (Saunders et al., 2012) |
| Mutect2 | the local assembly and pair HMM of [haplotype-based variant calling](/haplotype-based-variant-calling/), with a somatic model of the allele fraction |
| tests of two proportions | the counts of the tumor and of the normal sample in a $2 \times 2$ table, tested with [Fisher's exact test](/fisher-exact-test/), as in simple callers |

After calling, filters remove the known kinds of artifacts: reads from one strand only, bases at the ends of reads, low [mapping quality](/mapping-quality/), changes of C to T from the damage in fixed tissue, changes of G to T from oxidation during the preparation of the library, and sites that are noisy in a panel of normal samples.

## Bounds

- **Power is set by depth.** If a mutation is on a share $f$ of the reads and a call needs $k$ alternative reads, the chance of a call at depth $n$ is $P(\mathrm{Bin}(n, f) \ge k)$, a tail of the [binomial distribution](/binomial-distribution/). For $k = 3$: at $f = 0.2$ it is 0.956 at depth 30 and 0.9998 at depth 60; at $f = 0.05$ it is 0.188 at depth 30, 0.583 at depth 60 and 0.882 at depth 100. Small subclones need deep coverage.
- **The error floor.** A base quality of 30 means one error in 1000 bases, so at a fraction near $10^{-3}$, a true mutation and an error give the same counts. Lower fractions need errors to be removed, for example by the consensus of the reads of one molecule.
- **Many tests.** A genome has about $3 \times 10^9$ sites and a typical tumor has a few thousand to a few hundred thousand mutations, so the rate of false calls per site must be very low; see [false discovery rate](/false-discovery-rate/).
- **The normal sample.** If tumor cells are in the normal sample, as in blood cancers, the normal reads show somatic mutations, and a strict test of the normal sample removes true calls.

## Reductions

- **From germline calling.** With purity 1, one clone and two copies, the possible fractions are 0, 1/2 and 1, and the problem is [variant calling](/variant-calling-problem/) in two samples followed by a comparison of their genotypes.
- **To a test of two samples.** At one site, the question is whether the fraction in the tumor is above zero and the fraction in the normal sample is zero, a pair of hypothesis tests.
- **To clonal analysis.** The allele fractions of the calls, corrected for purity and copy number, are the input of methods that infer the subclones and their tree.

## Applications

- **Cancer genomics.** Catalogs of the mutations of each type of tumor, and the genes that are mutated more often than expected.
- **Clinical oncology.** Mutations that guide the choice of a drug, such as changes in EGFR, BRAF or KRAS.
- **Mutational signatures.** The spectrum of the somatic changes shows the processes that made them, such as tobacco smoke or ultraviolet light.
- **Monitoring.** Following the fraction of known tumor mutations in the blood during treatment.

## References
