---
tag: TSSGNC
kind: definition
slug: variant-call-format
name: Variant Call Format
aliases:
- VCF
area: biology/read-mapping-and-variant-calling
level: intro
summary: A tab-separated text format for sequence variants, one line per site with position, REF and ALT alleles, a Phred-scaled QUAL, filters, annotations and per-sample genotypes.
prereqs: [phred-quality-score, sam-alignment-format]
see_also: [variant-calling-problem, variant-normalization, genotype-likelihood, bayesian-genotype-calling, variant-quality-score-recalibration, read-pileup, haplotype-phasing, genotype-imputation]
sources:
  - paper: doi:10.1093/bioinformatics/btr330
    title: Petr Danecek, Adam Auton, Goncalo Abecasis, Cornelis A. Albers, Eric Banks, Mark A. DePristo, Robert E. Handsaker, Gerton Lunter, Gabor T. Marth, Stephen T. Sherry, Gilean McVean, Richard Durbin and 1000 Genomes Project Analysis Group, The variant call format and VCFtools, Bioinformatics 27(15), 2011
    locator: pp. 2156 to 2158 (the format, its header, the fixed fields and the genotype columns, and VCFtools)
  - url: https://samtools.github.io/hts-specs/VCFv4.3.pdf
    title: The Variant Call Format Specification, VCFv4.3, hts-specs
    locator: Section 1.6.1 (the fixed fields, including the padding base of indels) and Section 1.6.2 (the genotype fields GT, GQ, GL and PL, and the order of the genotypes)
---

The Variant Call Format (VCF) stores the output of [variant calling](/variant-calling-problem/): the sites where one or more samples differ from a reference genome, the alleles at each site, how sure the caller is, and the genotype of each sample. A VCF file is plain text, with meta-information lines that start with `##`, one header line that starts with `#CHROM`, and one tab-separated line per site. It was defined for the 1000 Genomes Project by Danecek et al. (2011); this page follows version 4.3 of the specification. BCF is the binary form, as BAM is for [SAM](/sam-alignment-format/).

## Definition

Positions are 1-based in VCF text. A data line has eight fixed fields, then, if there are samples, a FORMAT field and one column per sample.

| # | field | meaning |
|---|---|---|
| 1 | CHROM | the reference sequence |
| 2 | POS | the 1-based position of the first base of REF |
| 3 | ID | identifiers such as a dbSNP rs number, or `.` |
| 4 | REF | the reference allele, one or more bases that must match the reference at POS |
| 5 | ALT | the alternate alleles, separated by commas, or `.` if none |
| 6 | QUAL | the Phred-scaled quality of the claim made in ALT, or `.` |
| 7 | FILTER | `PASS`, or the names of the filters that the site fails |
| 8 | INFO | site annotations as `key=value` pairs separated by semicolons |
| 9 | FORMAT | the keys of the sample fields, separated by colons, for example `GT:GQ:PL` |
| 10 ... | samples | the values for each sample, in the order of FORMAT |

**QUAL.** For a site with ALT alleles, QUAL is $-10 \log_{10} P(\text{the site has no ALT allele} \mid \text{data})$ on the [Phred scale](/phred-quality-score/). A QUAL of 30 says the caller gives a 1 in 1000 chance that the site is not variant.

**Indels and the padding base.** REF and ALT of an insertion or a deletion include the base before the event, so that no allele is empty. A deletion of the bases CA after a T is written REF `TCA`, ALT `T`. If the event is at position 1, the base after the event is used instead. Because an indel in a repeat can sit at several positions, one event has several valid lines; [variant normalization](/variant-normalization/) picks one.

**Genotype (GT).** The alleles of a sample, as numbers: 0 for REF, 1 for the first ALT, 2 for the second, and so on, separated by `/` when the phase is unknown and by `|` when it is known. So `0/1` is a heterozygote of unknown phase, `1|0` a phased heterozygote with the ALT allele on the first haplotype, `1/1` a homozygote for the ALT allele, and `./.` a missing call. For a biallelic diploid site, GT `0/0`, `0/1` and `1/1` are the genotypes $g = 0, 1, 2$, where $g$ is the number of ALT alleles.

**Genotype likelihoods (GL and PL).** GL holds $\log_{10} P(\text{data} \mid \text{genotype})$ for each genotype, and PL holds the Phred-scaled values $-10 \log_{10} P(\text{data} \mid \text{genotype})$, rounded to integers, usually shifted so that the smallest is 0. The genotypes are in a fixed order: for a diploid sample, the genotype with alleles $j \le k$ has index $k (k + 1) / 2 + j$. With one ALT allele the order is 0/0, 0/1, 1/1; with two it is 0/0, 0/1, 1/1, 0/2, 1/2, 2/2.

**Genotype quality (GQ).** The specification defines GQ as the Phred-scaled probability that the called genotype is wrong, conditioned on the site being variant. Callers compute it in different ways. A posterior caller can write $-10 \log_{10}(1 - P(\text{called genotype} \mid \text{data}))$, and GATK writes the gap between the two smallest PL values, capped at 99. Read the header line of GQ, or the documentation of the caller, before comparing values from two tools.

## Examples and non-examples

**A heterozygous SNV.** Six reads cover position 1000 of chromosome 20, where the reference has A. Three show A with qualities 30, 30, 20, and three show G with qualities 30, 20, 10. The [genotype likelihoods](/genotype-likelihood/) for $g = 0, 1, 2$ are $\log_{10}$ values $-7.4366$, $-1.8428$ and $-9.4819$, which give PL 56, 0, 76. With the prior of [Bayesian genotype calling](/bayesian-genotype-calling/) for $\theta = 0.001$, the posterior of the heterozygote is 0.997462, and both QUAL and the posterior GQ come out as 25.96. The VCF line is

```
#CHROM  POS   ID  REF  ALT  QUAL   FILTER  INFO  FORMAT    sample1
20      1000  .   A    G    25.96  PASS    DP=6  GT:GQ:PL  0/1:26:56,0,76
```

with tabs in the file in place of the runs of spaces. With the PL gap rule, the same sample would get GQ 56.

**A deletion in a repeat.** On a reference that starts `GTCACACAGT`, a haplotype that lacks one copy of CA is `GTCACAGT`. The lines with POS 2, REF `TCA`, ALT `T` and with POS 6, REF `ACA`, ALT `A` describe the same haplotype. The first is the normalized form: it is as short as possible and as far left as possible.

**Two ALT alleles.** A site with REF `A` and ALT `G,T` has six diploid genotypes, so PL has six values, in the order 0/0, 0/1, 1/1, 0/2, 1/2, 2/2. A sample with GT `1/2` carries one G and one T and no A.

**Non-example: QUAL is not GQ.** QUAL is about the site: is any sample variant? GQ is about one sample: is this genotype right, given that the site is variant? A site can have a high QUAL from many carriers while one sample has a low GQ because it has two reads.

**Non-example: a filtered site is still a record.** A line whose FILTER is not PASS stays in the file. Tools that want only good sites must skip it. [Variant quality score recalibration](/variant-quality-score-recalibration/) writes its result into FILTER in this way.

**Non-example: BCF positions.** In BCF, the binary form, positions are 0-based, as in BAM. Only the text form is 1-based.

## Related definitions

- **REF and ALT.** The alleles of a site; the padding base and the choice among equal forms are above and on [variant normalization](/variant-normalization/).
- **Phred scale.** QUAL, GQ and PL use it; see [Phred quality score](/phred-quality-score/).
- **Genotype likelihood.** The value that GL and PL store; see [genotype likelihood](/genotype-likelihood/).
- **Phase.** The `|` separator records which alleles lie on the same chromosome; [haplotype phasing](/haplotype-phasing/) computes it from many samples.
- **Imputed genotypes.** [Genotype imputation](/genotype-imputation/) writes genotypes and their probabilities for sites that were not sequenced, often in VCF.
- **gVCF.** A VCF that also has lines for blocks of non-variant positions with their confidence, so that samples called one at a time can be combined later.

## References
