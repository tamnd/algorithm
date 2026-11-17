---
tag: 594N0V
kind: definition
slug: phred-quality-score
name: Phred quality score
aliases:
- Phred score
- base quality score
area: biology/read-mapping-and-variant-calling
level: intro
summary: "The error probability p of a base call written as Q = -10 log10 p, so Q20 means a 1 in 100 chance of error. The same scale is used for mapping and variant qualities."
prereqs: [probability-space]
see_also: [mapping-quality, sam-alignment-format, variant-call-format, base-quality-score-recalibration, genotype-likelihood, read-pileup, read-error-correction, expected-value]
sources:
  - paper: doi:10.1101/gr.8.3.175
    title: Brent Ewing, LaDeana Hillier, Michael C. Wendl and Phil Green, Base-calling of automated sequencer traces using phred. I. Accuracy assessment, Genome Research 8(3), 1998
    locator: pp. 175 to 185 (the phred base caller and its accuracy on trace data)
  - paper: doi:10.1101/gr.8.3.186
    title: Brent Ewing and Phil Green, Base-calling of automated sequencer traces using phred. II. Error probabilities, Genome Research 8(3), 1998
    locator: pp. 186 to 194 (the quality value q = -10 log10 p and its calibration against observed errors)
  - paper: doi:10.1093/nar/gkp1137
    title: Peter J. A. Cock, Christopher J. Fields, Naohisa Goto, Michael L. Heuer and Peter M. Rice, The Sanger FASTQ file format for sequences with quality scores, and the Solexa/Illumina FASTQ variants, Nucleic Acids Research 38(6), 2010
    locator: pp. 1767 to 1771 (the Phred and Solexa scales, the ASCII offsets 33 and 64, and the conversions)
  - url: https://samtools.github.io/hts-specs/SAMv1.pdf
    title: The SAM/BAM Format Specification, version 1.6, hts-specs
    locator: Section 1.2 (the Phred scale) and Section 1.4 (the MAPQ and QUAL fields)
---

A Phred quality score is an error probability written on a logarithmic scale: a call with error probability $p$ has quality $Q = -10 \log_{10} p$. Each step of 10 in $Q$ is a factor of 10 in $p$, so Q20 is a 1 in 100 chance that the call is wrong and Q30 a 1 in 1000 chance. The scale comes from the phred base caller of Ewing and Green (1998), which gave each base of a sequencing trace such a value. Today the same scale is used for the base qualities of reads, for the [mapping quality](/mapping-quality/) of an alignment, and for the QUAL and GQ fields of a [VCF](/variant-call-format/) record.

## Definition

Let $p \in (0, 1]$ be the probability that a claim is wrong, for example the claim that the base at one position of a read is the base the sequencer reported. Its **Phred quality** is

$$Q = -10 \log_{10} p, \qquad p = 10^{-Q/10}.$$

So $Q \ge 0$, $Q = 0$ means the claim is certainly wrong, and $Q$ grows without bound as $p \to 0$. In files the value is rounded to an integer. The scale says nothing about how $p$ was found: the phred program looked up $p$ in tables calibrated against known sequence, a modern base caller uses its own model, and an aligner or a variant caller computes $p$ from a likelihood. A quality is *calibrated* when, among all calls with quality $Q$, the share of wrong calls is close to $10^{-Q/10}$.

**Encoding in FASTQ and SAM.** A base quality is stored as one printable ASCII character, with code $Q + 33$. This is the Sanger or Phred+33 encoding, used by FASTQ files today and by the QUAL field of SAM. The SAM specification also uses the Phred scale for the MAPQ field, with 255 meaning that the mapping quality is not available. Some older Illumina pipelines (versions 1.3 to 1.7) wrote $Q + 64$ instead, and the oldest Solexa files used a different scale,

$$Q_{\text{Solexa}} = -10 \log_{10} \frac{p}{1 - p},$$

with offset 64. The two scales agree for small $p$ and differ for large $p$; the conversion is $Q = 10 \log_{10}\bigl(10^{Q_{\text{Solexa}}/10} + 1\bigr)$.

**Expected number of errors.** For a read with qualities $Q_1, \ldots, Q_L$, the expected number of wrong bases is $\sum_{i=1}^{L} 10^{-Q_i/10}$, by linearity of [expectation](/expected-value/). Read filters that drop reads with more than a set number of expected errors use this sum.

## Examples and non-examples

**The common values.** Each step of 10 is one more correct digit.

| $Q$ | $p$ | accuracy |
|---|---|---|
| 10 | 0.1 | 90% |
| 20 | 0.01 | 99% |
| 30 | 0.001 | 99.9% |
| 40 | 0.0001 | 99.99% |

Values in between follow the formula: $p = 0.05$ gives $Q = 13.01$, which a file stores as 13.

**A FASTQ quality string.** The string `IIII?55+` has the codes 73, 73, 73, 73, 63, 53, 53, 43, so the qualities are 40, 40, 40, 40, 30, 20, 20, 10. The expected number of errors in these eight bases is $4 \times 0.0001 + 0.001 + 2 \times 0.01 + 0.1 = 0.1214$. Almost all of it comes from the last base, which is typical: the tail of a short read often holds most of its expected errors.

**Solexa against Phred.** At $p = 0.1$ the Solexa score is $-10 \log_{10}(0.1 / 0.9) = 9.54$, close to the Phred score 10. At $p = 0.5$ the Solexa score is 0 and the Phred score is 3.01. A Solexa score can be negative, down to $-5$ in practice, while a Phred score cannot.

**Non-example: the average of qualities.** Phred scores do not average. Two bases of Q40 and Q10 have the mean quality 25, which stands for $p = 0.00316$. Their mean error probability is $(0.0001 + 0.1) / 2 = 0.05005$, which is Q13.0. To combine qualities, convert to probabilities first, then convert back.

**Non-example: a quality that is not calibrated.** A base caller may report Q35 for bases whose observed error rate is 1 in 500, which is Q27. The number is still written on the Phred scale, but it is not the Phred score of the true error rate. [Base quality score recalibration](/base-quality-score-recalibration/) estimates the true rate from mismatches against a reference and rewrites the values.

**Non-example: binned qualities.** Many current Illumina instruments write only a few distinct quality values, so each written value stands for a range of error probabilities. The values are still on the Phred scale, but the resolution is coarse, and two bases with the same written value may differ in their true error rates.

## Related definitions

- **Base quality.** The Phred score of one base call, stored per base in FASTQ and in the QUAL field of [SAM](/sam-alignment-format/). The alias "base quality score" names this use only; the scale is also used for the qualities below.
- **Mapping quality.** The Phred score of the probability that a read is placed at the wrong location; see [mapping quality](/mapping-quality/).
- **Variant quality.** QUAL in a [VCF](/variant-call-format/) record is the Phred score of the probability that the site has no variant, and GQ is the Phred score of the probability that the called genotype is wrong; see [Bayesian genotype calling](/bayesian-genotype-calling/).
- **Phred-scaled likelihood.** The PL field of VCF stores $-10 \log_{10}$ of each [genotype likelihood](/genotype-likelihood/), shifted so that the best genotype has 0. It is not an error probability, so it is not a Phred quality in the strict sense.
- **Error model.** Genotype likelihoods turn a base quality into $P(\text{read base} \mid \text{true base})$, most often $1 - p$ for a match and $p/3$ for each mismatch.
- **Use in a pileup.** A [read pileup](/read-pileup/) lists, for each reference position, the bases of the reads that cover it together with their qualities.

## References
