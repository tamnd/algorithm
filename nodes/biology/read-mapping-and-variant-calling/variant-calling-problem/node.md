---
tag: N4M0K6
kind: problem
slug: variant-calling-problem
name: Variant calling
aliases:
- SNP calling
- small variant calling
area: biology/read-mapping-and-variant-calling
level: core
summary: Given reads aligned to a reference, find the positions where a sample differs from it and assign a genotype with a confidence.
prereqs: [read-mapping, read-pileup, genotype-likelihood]
see_also: [bayesian-genotype-calling, variant-call-format, haplotype-based-variant-calling, somatic-variant-calling, structural-variant-detection, variant-quality-score-recalibration, variant-normalization, precision-and-recall]
sources:
  - paper: doi:10.1038/nrg2986
    title: Rasmus Nielsen, Joshua S. Paul, Anders Albrechtsen and Yun S. Song, Genotype and SNP calling from next-generation sequencing data, Nature Reviews Genetics 12(6), 2011
    locator: pp. 443 to 451 (the difference between SNP calling and genotype calling, the steps before calling, and single-sample and multi-sample methods)
  - paper: doi:10.1038/ng.806
    title: Mark A. DePristo, Eric Banks, Ryan Poplin and others, A framework for variation discovery and genotyping using next-generation DNA sequencing data, Nature Genetics 43(5), 2011
    locator: pp. 491 to 498 (the three phases of data processing, variant discovery and genotyping, and filtering)
  - paper: doi:10.1093/bioinformatics/btr509
    title: Heng Li, A statistical framework for SNP calling, mutation discovery, association mapping and population genetical parameter estimation from sequencing data, Bioinformatics 27(21), 2011
    locator: pp. 2987 to 2993 (calling from genotype likelihoods across many samples)
  - url: https://arxiv.org/abs/1207.3907
    title: Erik Garrison and Gabor Marth, Haplotype-based variant detection from short-read sequencing, arXiv 1207.3907, 2012
    locator: the sections on the model and on the detection of haplotypes in a window (FreeBayes)
  - paper: doi:10.1038/nbt.4235
    title: Ryan Poplin, Pi-Chuan Chang, David Alexander and others, A universal SNP and small-indel variant caller using deep neural networks, Nature Biotechnology 36(10), 2018
    locator: pp. 983 to 987 (DeepVariant, genotype calling from images of the pileup with a convolutional network)
  - paper: doi:10.1038/nbt.2835
    title: Justin M. Zook, Brad Chapman, Jason Wang and others, Integrating human sequence data sets provides a resource of benchmark SNP and indel genotype calls, Nature Biotechnology 32(3), 2014
    locator: pp. 246 to 251 (the Genome in a Bottle benchmark calls for NA12878 and their confident regions)
---

Variant calling takes the reads of a sample, [mapped](/read-mapping/) to a reference genome, and finds where the sample differs from the reference: single-nucleotide variants (SNVs) and short insertions and deletions (indels). For each variant it gives the genotype of the sample, such as heterozygous or homozygous, and how sure the call is. The reads have errors and some are mapped to the wrong place, so the problem is statistical: a mismatch in one read is weak evidence, and the caller must weigh many reads and their qualities. The output is usually a [VCF](/variant-call-format/) file.

## In plain words

You have many short pieces of text copied from one book, with some typing mistakes, and you know where in a reference copy of the book each piece belongs. You want to find the places where this book really differs from the reference.

At each place, look at all the pieces that cover it. If one piece in thirty has another letter, it is likely a mistake. If about half of them have the other letter, this book has two versions there, one like the reference and one not. If almost all have it, both versions differ. The task is to make that choice for every place, and to say how sure you are.

## Definition

**Input.**

- A reference genome $R$, with positions 1 to $G$, as in VCF.
- Reads from one or more samples, mapped to $R$, with base qualities and [mapping qualities](/mapping-quality/), usually in a sorted BAM file.
- The ploidy of each sample, which is 2 for human autosomes.

**Output.** A list of variant records. Each record has a position, a reference allele and one or more alternate alleles, a site quality, and for each sample a genotype and a genotype quality.

**The statistical form.** At a candidate site with alleles $r$ and $a$, a diploid sample has a genotype $g \in \{0, 1, 2\}$, the number of copies of $a$. With the data $D$ of the reads that cover the site, the caller reports the posterior

$$P(g \mid D) = \frac{P(D \mid g)\, P(g)}{\sum_{g'} P(D \mid g')\, P(g')},$$

where $P(D \mid g)$ is the [genotype likelihood](/genotype-likelihood/) and $P(g)$ is a prior. *SNP discovery* asks whether the site is variant in any sample, with the site quality $-10 \log_{10} P(\text{no sample carries } a \mid D)$; *genotype calling* asks for each sample's $g$. Nielsen et al. (2011) stress that the two are distinct.

**Small variants.** The word "small" separates SNVs and indels of up to a few tens of bases from structural variants. A size of 50 bases is a common boundary in the literature, but it is a convention, not a rule.

## Variants

- **Germline calling of one sample.** One sample at a time, with a prior from the expected rate of differences, as in [Bayesian genotype calling](/bayesian-genotype-calling/).
- **Joint calling of many samples.** All samples share one site and one allele frequency, so weak evidence in many samples adds up. The prior can be a [Hardy-Weinberg](/hardy-weinberg-principle/) prior with an allele frequency estimated by [expectation maximization](/expectation-maximization/) (Li, 2011).
- **Low-coverage population calling.** At 2x to 6x per sample, single-sample genotypes are poor; the [genotype likelihoods](/genotype-likelihood/) are passed on to [imputation](/genotype-imputation/) or to estimates of the [allele frequency](/allele-frequency/) and the [site frequency spectrum](/site-frequency-spectrum/).
- **Haplotype-based calling.** Callers such as GATK HaplotypeCaller and FreeBayes look at a window and score whole candidate haplotypes, which handles indels and nearby variants better than one site at a time; see [haplotype-based variant calling](/haplotype-based-variant-calling/).
- **Somatic calling.** In tumors, a variant can be in a small share of the cells, so the expected allele fractions are not 0, 1/2 and 1; see [somatic variant calling](/somatic-variant-calling/).
- **Larger events.** Structural variants and copy number changes need other evidence, such as read pairs, split reads and depth; see [structural variant detection](/structural-variant-detection/) and [copy number segmentation](/copy-number-segmentation/).
- **Other ploidies and pools.** Polyploid samples and pools of many individuals change the possible allele fractions, and with them the likelihood.

## Examples

All examples use the reference allele A, the alternate allele G, base qualities on the Phred scale and the prior of [Bayesian genotype calling](/bayesian-genotype-calling/) with $\theta = 0.001$.

- **A clear heterozygote.** Six reads: A at qualities 30, 30, 20 and G at 30, 20, 10. The posterior of A/G is 0.997462, and the site quality is 25.96.
- **One error in ten.** One G and nine A, all Q30. The call is A/A; the posterior of A/G is only 0.002932, because the prior and the nine A reads outweigh one base that has a 1 in 1000 chance of an error.
- **Low depth.** Two G reads, both Q30. The posteriors of A/A, A/G and G/G are 0.000148, 0.333432 and 0.666420. The site is clearly variant (site quality 38.3), but the genotype G/G has a genotype quality of only 4.77, since a heterozygote shows G on both reads with probability $1/4$.
- **An indel in a repeat.** On a reference that starts `GTCACACAGT`, a sample with `GTCACAGT` lacks one copy of CA. The deletion can be written at several positions; the [normalized](/variant-normalization/) record is POS 2, REF `TCA`, ALT `T`.

## Known algorithms

| method | approach | source |
|---|---|---|
| [Bayesian genotype calling](/bayesian-genotype-calling/) | per-site posterior from base qualities and a prior, as in Maq, samtools and bcftools, and GATK UnifiedGenotyper | Li, Ruan and Durbin (2008); Li (2011); DePristo et al. (2011) |
| [Haplotype-based calling](/haplotype-based-variant-calling/) | local assembly or candidate haplotypes in a window, read likelihoods by a [pair HMM](/pair-hmm/) | Garrison and Marth (2012) for FreeBayes; GATK HaplotypeCaller |
| DeepVariant | a convolutional network classifies an image of the pileup at each candidate site into three genotypes | Poplin et al. (2018) |
| [Variant quality score recalibration](/variant-quality-score-recalibration/) | a filter after calling: a mixture model on the site annotations separates real sites from artifacts | DePristo et al. (2011) |

The calls depend on the steps before them as much as on the caller: [read mapping](/read-mapping/), [duplicate marking](/duplicate-read-marking/) and [base quality score recalibration](/base-quality-score-recalibration/). The [paired-end](/paired-end-read-mapping/) placement of the reads decides which repeats can be called at all.

## Bounds

- **Time.** A per-site caller reads each aligned base once and does $O(1)$ work per base and genotype, so it runs in time linear in the total number of aligned bases, about $N L$ for $N$ reads of length $L$. Haplotype-based callers cost more in active regions, where they align every read against every candidate haplotype.
- **Depth.** A heterozygous site with $d$ reads, each from either chromosome with probability 1/2, shows no alternate read with probability $2^{-d}$, and at most one with probability $(1 + d) 2^{-d}$. For $d = 10$ these are 0.098% and 1.07%; for $d = 30$, about $9.3 \times 10^{-10}$ and $2.9 \times 10^{-8}$. With [coverage](/sequencing-coverage/) that varies along the genome, the low-depth sites dominate the missed heterozygotes.
- **Mappability.** If a segment of the genome has an exact copy longer than the reads and the inserts, reads from it cannot be placed, and no caller can tell in which copy a variant lies.
- **Measuring accuracy.** Calls are compared with benchmark sets, such as the Genome in a Bottle calls for NA12878 (Zook et al., 2014), in their confident regions, and the result is given as [precision and recall](/precision-and-recall/). The comparison needs the two sets in the same representation, which [variant normalization](/variant-normalization/) gives for simple cases.

## Reductions

- **To one decision per site.** With a pileup and a fixed allele pair, per-site calling is a choice among $m + 1$ genotypes by [maximum a posteriori estimation](/maximum-a-posteriori-estimation/).
- **From read mapping.** The input is the output of [read mapping](/read-mapping/); a better placement of the reads changes the calls more than any change of the prior.
- **To phasing.** The genotypes of a VCF of unknown phase are the input of [haplotype phasing](/haplotype-phasing/).
- **To filtering.** The raw calls of a sensitive caller are filtered, by hard thresholds on their annotations or by [variant quality score recalibration](/variant-quality-score-recalibration/).

## Applications

- **Clinical genetics.** Finding the variant that causes a rare disease in an exome or genome of a patient and the parents.
- **Population genetics.** Allele frequencies, the site frequency spectrum and estimators such as [Watterson's](/watterson-estimator/) start from variant calls or from genotype likelihoods.
- **Association studies.** Genotypes of many individuals at many sites, often completed by [imputation](/genotype-imputation/).
- **Cancer.** Somatic calls of a tumor against its matched normal.

## References
