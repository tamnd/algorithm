---
tag: YB8C7J
kind: algorithm
slug: bayesian-genotype-calling
name: Bayesian genotype calling
aliases:
- Bayesian SNP calling
area: biology/read-mapping-and-variant-calling
level: core
summary: Combine genotype likelihoods with a prior from allele frequency or heterozygosity, and call the genotype of highest posterior probability.
solves: [variant-calling-problem]
model: real-ram
complexity:
  vars: {n: the number of reads at the site}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 2008
  people: [Heng Li, Jue Ruan, Richard Durbin]
  note: Maq called the consensus genotype of a sample from the bases and qualities at each site with a Bayesian model. Li (2011) and the GATK UnifiedGenotyper of DePristo et al. (2011) extended the approach to many samples.
prereqs: [genotype-likelihood, bayes-theorem, read-pileup]
see_also: [variant-call-format, hardy-weinberg-principle, maximum-a-posteriori-estimation, log-sum-exp-trick, site-frequency-spectrum, expectation-maximization, haplotype-based-variant-calling, base-quality-score-recalibration]
sources:
  - paper: doi:10.1101/gr.078212.108
    title: Heng Li, Jue Ruan and Richard Durbin, Mapping short DNA sequencing reads and calling variants using mapping quality scores, Genome Research 18(11), 2008
    locator: pp. 1851 to 1858, Methods (the consensus genotype calling of Maq, with a prior on the heterozygote and the Phred-scaled consensus quality)
  - paper: doi:10.1093/bioinformatics/btr509
    title: Heng Li, A statistical framework for SNP calling, mutation discovery, association mapping and population genetical parameter estimation from sequencing data, Bioinformatics 27(21), 2011
    locator: pp. 2987 to 2993, Section 2 (genotype likelihoods, the posterior of the genotype, and the estimation of the allele frequency across samples)
  - paper: doi:10.1038/ng.806
    title: Mark A. DePristo, Eric Banks, Ryan Poplin and others, A framework for variation discovery and genotyping using next-generation DNA sequencing data, Nature Genetics 43(5), 2011
    locator: pp. 491 to 498, the section on SNP discovery and genotyping (the Bayesian model of the UnifiedGenotyper and the prior from the heterozygosity)
  - paper: doi:10.1038/nrg2986
    title: Rasmus Nielsen, Joshua S. Paul, Anders Albrechtsen and Yun S. Song, Genotype and SNP calling from next-generation sequencing data, Nature Reviews Genetics 12(6), 2011
    locator: pp. 443 to 451, the section on probabilistic genotype calling (priors from a fixed rate or from the allele frequencies of a population)
---

Bayesian genotype calling decides the genotype of a sample at one site from the reads that cover it. It computes the [genotype likelihood](/genotype-likelihood/) of each genotype from the bases and their qualities, multiplies it by a prior, normalizes by [Bayes' theorem](/bayes-theorem/), and calls the genotype of highest posterior probability. The prior is what lets the method resist a few sequencing errors, and the posterior gives the confidence of the call on the Phred scale, the GQ and QUAL fields of [VCF](/variant-call-format/). Maq used this scheme in 2008, and it is the core of per-site callers such as bcftools and the GATK UnifiedGenotyper.

## In plain words

At one place in the genome, a person can have the reference letter on both chromosomes, on one, or on neither. Each read that covers the place shows a letter, and each letter has a score that says how often such a letter is a mistake.

For each of the three choices, work out how likely the reads would be if that choice were true. Then weigh each choice by how common it is before you look at any reads: most places match the reference, so that choice starts far ahead. Pick the choice that comes out with the most weight, and report how much weight is left for the others. Little weight left means a sure call.

## The problem

At a site with reference allele $r$ and one alternate allele $a$, a diploid sample has genotype $g \in \{0, 1, 2\}$, the number of copies of $a$. The data $D$ are the read bases and qualities of the [pileup](/read-pileup/) column, $(b_1, Q_1), \dots, (b_n, Q_n)$. Given a prior $\pi(g)$, find the posterior $P(g \mid D)$, the genotype $\hat g$ that maximizes it, and

$$\mathrm{GQ} = -10 \log_{10}\bigl(1 - P(\hat g \mid D)\bigr), \qquad \mathrm{QUAL} = -10 \log_{10} P(g = 0 \mid D).$$

The model is that of [genotype likelihood](/genotype-likelihood/): a base of quality $Q$ has error rate $e = 10^{-Q/10}$, it shows the true allele with probability $1 - e$ and each other base with probability $e/3$, each read comes from either chromosome with probability $1/2$, and the reads are independent given $g$.

**Priors.** Two priors are common.

- **From the heterozygosity.** With $\theta$ the expected rate of differences between two chromosomes, $\pi = (1 - 3\theta/2, \theta, \theta/2)$. GATK's default heterozygosity is $\theta = 0.001$, about the rate for humans.
- **From an allele frequency.** If the frequency of $a$ in the population is $f$, the [Hardy-Weinberg](/hardy-weinberg-principle/) prior is $\pi = ((1-f)^2, 2f(1-f), f^2)$.

The first prior follows from the neutral [site frequency spectrum](/site-frequency-spectrum/) for three sequences, the reference and the two chromosomes of the sample. A site is segregating with one derived copy with probability about $\theta$ and with two with probability about $\theta/2$. Given one derived copy, it is on a chromosome of the sample with probability $2/3$, which makes a heterozygote, and on the reference with probability $1/3$, which makes the sample homozygous for $a$. Given two, they are on the reference and one chromosome with probability $2/3$, a heterozygote, and on both chromosomes with probability $1/3$. So $P(g = 1) = \frac{2}{3}\theta + \frac{2}{3}\cdot\frac{\theta}{2} = \theta$ and $P(g = 2) = \frac{1}{3}\theta + \frac{1}{3}\cdot\frac{\theta}{2} = \theta/2$, to first order in $\theta$.

## The algorithm

The sums are in logarithms, with the [log-sum-exp trick](/log-sum-exp-trick/), so that a deep pileup does not underflow.

```pseudo id=main
BAYES-GENOTYPE(pileup, r, a, π)
L1  λ[g] ← ln π(g) for g = 0, 1, 2
L2  for each read (b, Q) in the pileup do
L3      e ← 10^(-Q/10)
L4      for g ← 0 to 2 do
L5          λ[g] ← λ[g] + ln((g/2) P(b | a, e) + (1 - g/2) P(b | r, e))
L6  z ← LOG-SUM-EXP(λ[0], λ[1], λ[2])
L7  post[g] ← exp(λ[g] - z) for g = 0, 1, 2
L8  ĝ ← the g of largest λ[g], ties to the smaller g
L9  w ← LOG-SUM-EXP(λ[g] for g ≠ ĝ) - z
L10 return ĝ, post, GQ = -10 w / ln 10, QUAL = -10 (λ[0] - z) / ln 10
```

At line L6, $\lambda[g] = \ln \pi(g) + \ln P(D \mid g)$, so $z$ is $\ln P(D)$ and line L7 gives the posterior. Line L9 is the log of $1 - P(\hat g \mid D)$, computed from the other two terms instead of by a subtraction, which keeps its precision when the call is sure. If the alternate allele is not given, the code takes the most common non-reference base of the pileup, with ties in ACGT order.

## Example

Six reads at a site with $r = A$ and $a = G$: A at qualities 30, 30, 20, and G at 30, 20, 10. The genotype likelihoods are $\log_{10} P(D \mid g) = -7.4366, -1.8428, -9.4819$, which is PL 56, 0, 76.

With the prior from $\theta = 0.001$, $\pi = (0.9985, 0.001, 0.0005)$, the posterior is

| $g$ | genotype | posterior |
|---|---|---|
| 0 | A/A | 0.002538 |
| 1 | A/G | 0.997462 |
| 2 | G/G | $1.14 \times 10^{-8}$ |

The call is A/G with $\mathrm{GQ} = 25.96$. Here QUAL is almost the same, 25.96, because nearly all of the weight that is not on A/G is on A/A. The likelihood ratio of A/G to A/A is about $4 \times 10^5$, but the prior ratio is $0.001 / 0.9985$, so the posterior ratio is about 390.

With the Hardy-Weinberg prior for $f = 0.3$, a common variant, $\pi = (0.49, 0.42, 0.09)$ and the call is A/G with $\mathrm{GQ} = 55.26$. The same reads give a surer call when the variant is known to be common.

Two more cases, with the $\theta$ prior:

- **One G among ten Q30 reads.** The call is A/A, with a posterior of 0.002932 for A/G. One base with a 1 in 1000 error rate, against nine reference bases, is not enough to overturn a prior of 1000 to 1 against the heterozygote.
- **Two G reads at Q30.** The posteriors are 0.000148, 0.333432 and 0.666420, and the call is G/G with $\mathrm{GQ} = 4.77$, but $\mathrm{QUAL} = 38.29$. The site is surely variant, but two reads cannot tell G/G from A/G.

## Correctness

For one read, the probability of its base given $g$ is the mixture in line L5, by the law of total probability over the chromosome it came from. The reads are independent given $g$, so the likelihood is the product of the read terms, which line L5 adds in logarithms. The product of the mixtures is also the sum, over all $2^n$ ways to assign the reads to the two chromosomes, of the probability of the bases under that assignment; the test checks the code against that brute force sum. After the loop, $\lambda[g] = \ln(\pi(g) P(D \mid g))$, so lines L6 and L7 give the posterior by Bayes' theorem, line L8 the maximum a posteriori genotype, and lines L9 and L10 the stated GQ and QUAL. The full proof, which needs $0 < e < 1$ for every read, is in proofs/correctness.md.

## Complexity

- **Time.** $\Theta(n)$ per site: three log terms per read. A genome at 30x has about $3 \times 10^9$ sites times 30 reads, so callers first skip the sites where no read differs from the reference by more than a threshold.
- **Space.** $\Theta(1)$ beyond the pileup, since the reads can be added one at a time.
- **More alleles.** With $k$ alleles, a diploid has $k(k+1)/2$ genotypes, and the cost is $\Theta(n k^2)$.

## Properties

- **Exact for its model.** The posterior is computed exactly, up to rounding. The model itself, independent reads with calibrated qualities, is an approximation.
- **Incremental.** Each read adds one term to each $\lambda[g]$, so a caller can update the call as reads arrive.
- **Prior dominance at low depth.** With no reads, the posterior is the prior and the call is A/A. As the depth grows, the likelihood dominates and the prior matters less.
- **Phred outputs.** GQ uses the posterior of the called genotype. GATK writes GQ in another way, as the gap between the two smallest PL values capped at 99, so values from two callers need care.

## Variants and improvements

- **Multi-sample calling.** Li (2011) estimates the allele frequency $f$ of a site from the genotype likelihoods of all samples by [expectation maximization](/expectation-maximization/) and uses it in a Hardy-Weinberg prior, so samples with few reads borrow strength from the others.
- **Mapping quality.** Many callers mix in the chance that the read is misplaced, or cap each base quality at the mapping quality of the read.
- **Indels.** Per-site callers can score indels as alleles with the probability of the read given each allele, but [haplotype-based calling](/haplotype-based-variant-calling/) does this better, with a pair HMM over candidate haplotypes.
- **Dependent errors.** Some callers give less weight to repeated errors on the same strand at the same site, which the independent model overcounts.
- **Somatic and pooled samples.** Allele fractions other than 0, 1/2 and 1 replace the three genotypes; see [somatic variant calling](/somatic-variant-calling/).

## When to use it

Use it for SNVs at sites where the reads are well aligned, for one or many samples, and when you need a calibrated posterior. It is fast and simple, and it is the reference point for other callers. For indels and for clusters of nearby variants, prefer haplotype-based callers. At low coverage, pass the likelihoods to population methods instead of calling hard genotypes.

## Pitfalls

- **Wrong qualities.** Overstated base qualities make errors look like evidence; run [base quality score recalibration](/base-quality-score-recalibration/) first.
- **Duplicates.** PCR copies are not independent reads; mark them with [duplicate marking](/duplicate-read-marking/).
- **Misaligned indels.** Reads aligned across an indel can show false SNVs near it.
- **The prior in a population with another rate.** A fixed $\theta = 0.001$ is set for humans. Another species, or a known common variant, needs another prior.
- **GQ versus QUAL.** A site can be surely variant while the genotype is unsure, as in the two-read example.

## Implementations

## History

Maq (Li, Ruan and Durbin, 2008) called the consensus genotype of a sample with a Bayesian model of the bases and qualities at each site, and gave the consensus quality on the Phred scale. In 2011, Li described a framework for many samples in samtools, and DePristo et al. described the UnifiedGenotyper of GATK, both with priors of this form. The review of Nielsen et al. (2011) set out the difference between SNP calling and genotype calling and the role of the prior.

## References
