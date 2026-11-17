---
tag: RS20ZP
kind: definition
slug: genotype-likelihood
name: Genotype likelihood
aliases:
- GL
area: biology/read-mapping-and-variant-calling
level: core
summary: The probability of the reads at a site given each possible genotype, computed from base qualities under an independent error model.
prereqs: [read-pileup, phred-quality-score, likelihood-function]
see_also: [bayesian-genotype-calling, variant-call-format, variant-calling-problem, base-quality-score-recalibration, mapping-quality, binomial-distribution, hardy-weinberg-principle, genotype-imputation]
sources:
  - paper: doi:10.1093/bioinformatics/btr509
    title: Heng Li, A statistical framework for SNP calling, mutation discovery, association mapping and population genetical parameter estimation from sequencing data, Bioinformatics 27(21), 2011
    locator: pp. 2987 to 2993, Section 2 (the likelihood of the reads at a site for a sample of ploidy m, with g copies of the alternate allele)
  - paper: doi:10.1038/nrg2986
    title: Rasmus Nielsen, Joshua S. Paul, Anders Albrechtsen and Yun S. Song, Genotype and SNP calling from next-generation sequencing data, Nature Reviews Genetics 12(6), 2011
    locator: pp. 443 to 451, the section on genotype calling (genotype likelihoods from base qualities, and their use in single-sample and multi-sample calling)
  - paper: doi:10.1101/gr.078212.108
    title: Heng Li, Jue Ruan and Richard Durbin, Mapping short DNA sequencing reads and calling variants using mapping quality scores, Genome Research 18(11), 2008
    locator: pp. 1851 to 1858, Methods (the consensus genotype calling of Maq from the bases and qualities at a site)
  - url: https://samtools.github.io/hts-specs/VCFv4.3.pdf
    title: The Variant Call Format Specification, VCFv4.3, hts-specs
    locator: Section 1.6.2 (the genotype fields GL and PL and the order of the genotypes)
---

A genotype likelihood is the probability of the reads that cover one site of one sample, computed once for each genotype that the sample could have there. It is a [likelihood](/likelihood-function/): a function of the genotype for fixed data, not a probability distribution over the genotypes. The usual model takes the bases of the [pileup column](/read-pileup/) as independent given the genotype and reads the error rate of each base from its [Phred quality](/phred-quality-score/). Callers combine the likelihoods with a prior in [Bayesian genotype calling](/bayesian-genotype-calling/), and [VCF](/variant-call-format/) stores them in the fields GL and PL.

## Definition

Fix a site with reference allele $r$ and alternate allele $a$, and a sample of ploidy $m$, which is 2 for a diploid. The genotype $g \in \{0, 1, \dots, m\}$ is the number of copies of $a$. The data $D$ are the read bases $b_1, \dots, b_n$ at the site with their qualities $Q_1, \dots, Q_n$, and $e_i = 10^{-Q_i/10}$.

**The error model.** A read that comes from a chromosome with allele $A$ shows the base $b$ with probability

$$P(b \mid A) = \begin{cases} 1 - e & \text{if } b = A, \\ e / 3 & \text{otherwise,} \end{cases}$$

so an error turns the base into each of the three others with the same probability.

**The genotype likelihood.** Each read comes from one of the $m$ chromosomes, chosen uniformly, and the reads are independent given $g$. Then

$$L(g) = P(D \mid g) = \prod_{i=1}^{n} \left( \frac{g}{m} P(b_i \mid a) + \frac{m - g}{m} P(b_i \mid r) \right).$$

For a diploid, the three values are $L(0) = \prod_i P(b_i \mid r)$, $L(2) = \prod_i P(b_i \mid a)$, and $L(1) = \prod_i \frac{1}{2}\bigl(P(b_i \mid r) + P(b_i \mid a)\bigr)$. For several alternate alleles, the genotype is a multiset of $m$ alleles and the factor of read $i$ is the mean of $P(b_i \mid A)$ over the alleles $A$ of the multiset.

**Log and Phred forms.** VCF stores $\mathrm{GL}(g) = \log_{10} L(g)$, and $\mathrm{PL}(g) = -10 \log_{10} L(g)$ rounded to an integer and shifted so that the smallest value is 0. The shift does not lose anything that a caller needs, because the posterior of [Bayesian genotype calling](/bayesian-genotype-calling/) depends only on the ratios $L(g) / L(g')$.

**Other terms in the model.** Many callers add more to $P(b \mid A)$: the chance $10^{-M/10}$ that the read is mapped to the wrong place, from its [mapping quality](/mapping-quality/) $M$, or a cap of each base quality at the read's mapping quality. Haplotype-based callers replace the factor of each base with the probability of the whole read given a candidate haplotype, computed with a [pair HMM](/pair-hmm/).

## Examples and non-examples

**A heterozygous site.** Six reads cover a site with $r = A$ and $a = G$: three show A with qualities 30, 30, 20, and three show G with qualities 30, 20, 10. For a diploid:

| $g$ | genotype | $L(g)$ | $\log_{10} L(g)$ | PL |
|---|---|---|---|---|
| 0 | A/A | $3.659 \times 10^{-8}$ | $-7.4366$ | 56 |
| 1 | A/G | $0.014361$ | $-1.8428$ | 0 |
| 2 | G/G | $3.297 \times 10^{-10}$ | $-9.4819$ | 76 |

For $g = 1$ each factor is close to $1/2$, so $L(1)$ is close to $2^{-6} = 0.015625$. For $g = 0$, the three G bases each contribute $e_i / 3$, which is small, and the Q10 base contributes the most of them, $0.1 / 3$. The likelihoods favor the heterozygote by a factor of about $4 \times 10^5$ over A/A.

**Two reads.** Two G reads of quality 30 at a site with $r = A$ give $L(2) = (1 - 0.001)^2 = 0.998$, $L(1) = 0.2497$ and $L(0) = 1.11 \times 10^{-7}$. The likelihood of G/G is only 4 times that of A/G, since a heterozygote shows G on both reads with probability about $1/4$. With low depth, the likelihoods alone cannot tell a heterozygote from a homozygote, which is why the prior matters there.

**Non-example: the likelihoods do not sum to 1.** In the first example, the three values sum to 0.0144. They are probabilities of the data, one for each genotype, not probabilities of the genotypes. Turning them into genotype probabilities needs a prior, as in [Bayes' theorem](/bayes-theorem/).

**Non-example: dependent reads.** If three of the six reads are PCR copies of one fragment, an error in that fragment appears three times, and the product over the reads counts it three times. The model assumes independent reads, which is one reason for [duplicate marking](/duplicate-read-marking/) before calling.

**Non-example: a wrong quality.** If the Q30 bases are really wrong 1 time in 200, the model overstates how unlikely an error is, and a few errors at one site look like a heterozygote. [Base quality score recalibration](/base-quality-score-recalibration/) corrects the qualities before the likelihoods are computed.

## Related definitions

- **Read pileup.** The likelihood is a function of one pileup column; see [read pileup](/read-pileup/).
- **Prior and posterior.** With a prior $P(g)$, such as the [Hardy-Weinberg](/hardy-weinberg-principle/) prior from an allele frequency, the posterior is $P(g \mid D) = L(g) P(g) / \sum_{g'} L(g') P(g')$; see [Bayesian genotype calling](/bayesian-genotype-calling/).
- **Counts form.** If all bases have the same error rate $e$ and $k$ of the $n$ bases show $a$, then for a heterozygote each base shows $a$ with probability about $1/2$, and the likelihood is a [binomial](/binomial-distribution/) term in $k$ up to a factor that does not depend on $g$.
- **Use without calling.** Imputation and population methods can use the likelihoods directly, without first calling a genotype, which keeps the uncertainty of low-coverage data; see [genotype imputation](/genotype-imputation/) and Li (2011).
- **VCF fields.** GL and PL, and the order of the genotypes for several alternate alleles, are on [Variant Call Format](/variant-call-format/).

## References
