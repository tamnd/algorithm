---
tag: J0YP9E
kind: definition
slug: mapping-quality
name: Mapping quality
aliases:
- MAPQ
area: biology/read-mapping-and-variant-calling
level: core
summary: The Phred-scaled probability that a read is placed at the wrong location, -10 log10 P(wrong). It is low for reads in repeats. Each aligner computes it by its own rule.
prereqs: [read-mapping, phred-quality-score, bayes-theorem]
see_also: [sam-alignment-format, bwa, bowtie, minimap2, paired-end-read-mapping, genotype-likelihood, genome-repeat, read-pileup]
sources:
  - paper: doi:10.1101/gr.078212.108
    title: Heng Li, Jue Ruan and Richard Durbin, Mapping short DNA sequencing reads and calling variants using mapping quality scores, Genome Research 18(11), 2008
    locator: pp. 1851 to 1858, Methods (the definition of mapping quality as a posterior probability and its approximation from the best and second best hits in Maq)
  - paper: doi:10.1093/bioinformatics/btp324
    title: Heng Li and Richard Durbin, Fast and accurate short read alignment with Burrows-Wheeler transform, Bioinformatics 25(14), 2009
    locator: pp. 1754 to 1760, Methods (the mapping quality of BWA for unique and repeated hits)
  - url: https://samtools.github.io/hts-specs/SAMv1.pdf
    title: The SAM/BAM Format Specification, version 1.6, hts-specs
    locator: Section 1.4, field 5 MAPQ (-10 log10 of the probability that the mapping position is wrong, 255 if not available)
  - paper: doi:10.1038/nmeth.1923
    title: Ben Langmead and Steven L. Salzberg, Fast gapped-read alignment with Bowtie 2, Nature Methods 9(4), 2012
    locator: pp. 357 to 359 (Bowtie 2 and its reporting of alignments)
---

The mapping quality of a read says how sure an aligner is that it put the read in the right place on the reference. It uses the [Phred scale](/phred-quality-score/): MAPQ 30 means a 1 in 1000 chance that the reported position is wrong. A read from a unique part of the genome can get a high value even with a few mismatches, while a read from a [repeat](/genome-repeat/) with two equally good positions gets a value near 0 however well it matches. Li, Ruan and Durbin (2008) defined mapping quality in this way for the Maq aligner; the [SAM](/sam-alignment-format/) format stores it in field 5, and each aligner computes it by its own rule.

## Definition

Let a read $x$ be aligned to a reference, and let $u^*$ be the position the aligner reports. The **mapping quality** of the read is

$$\mathrm{MAPQ} = -10 \log_{10} P(\text{the true origin of } x \text{ is not } u^* \mid x),$$

rounded to an integer. In SAM the value 255 means that the mapping quality is not available.

**The posterior form.** Maq models the read as coming from one position $u$ of the reference, with a uniform prior over the positions. Given $u$, the read bases are independent, and a base of quality $Q_i$ is wrong with probability $e_i = 10^{-Q_i/10}$. So the probability of the read from $u$ is

$$P(x \mid u) = \prod_{i \text{ matches at } u} (1 - e_i) \prod_{i \text{ mismatches at } u} \frac{e_i}{3},$$

and by [Bayes' theorem](/bayes-theorem/)

$$P(u^* \mid x) = \frac{P(x \mid u^*)}{\sum_{u} P(x \mid u)}, \qquad \mathrm{MAPQ} = -10 \log_{10}\bigl(1 - P(u^* \mid x)\bigr).$$

The sum runs over every position of the reference. An aligner can compute only the terms of the hits it finds, so in practice the sum is taken over the best few hits, with a correction for the hits that the search may have missed.

**The approximation.** When the best hit has no mismatch and the second best differs in a few bases, the sum is dominated by those two terms, and

$$\mathrm{MAPQ} \approx Q_{\text{second}} - Q_{\text{best}},$$

where $Q_{\text{hit}}$ is the sum of the qualities of the mismatched bases of that hit. This is the form that Maq approximates, with caps that depend on the number of mismatches its search allows.

**Each aligner has its own rule.** [BWA](/bwa/), [Bowtie](/bowtie/) 2 and [minimap2](/minimap2/) all write MAPQ, but none computes the exact posterior. They map features such as the gap between the best and the second best alignment score, and the number of equally good hits, to a number on the Phred scale with their own tables and caps. BWA writes 0 for a read with several equally best hits. The largest value differs between tools (60 for BWA-MEM and minimap2, 42 for Bowtie 2), so MAPQ values from two aligners are not on the same footing.

## Examples and non-examples

**A unique read.** A read has the best hit with no mismatches and a second hit with one more mismatch at a Q30 base, and no other hit is close. In the posterior form, the ratio of the two likelihoods is $(e/3) / (1 - e)$ with $e = 0.001$, which is $3.34 \times 10^{-4}$, so

$$P(\text{wrong}) = \frac{3.34 \times 10^{-4}}{1 + 3.34 \times 10^{-4}} = 3.34 \times 10^{-4}, \qquad \mathrm{MAPQ} = 34.77.$$

The approximation counts the mismatch as $e$ instead of $e/3$ and gives 30. With two extra Q30 mismatches on the second hit, the posterior form gives 69.53.

**A read in a two-copy repeat.** If the read matches two positions equally well, each has posterior $1/2$, and $\mathrm{MAPQ} = -10 \log_{10}(1/2) = 3.01$. With three equal hits, $P(\text{wrong}) = 2/3$ and $\mathrm{MAPQ} = 1.76$. An aligner reports one of the copies at random, and BWA writes 0.

**The help of the mate.** If the read of the last example is one mate of a [read pair](/paired-end-reads/) and its mate maps uniquely, only one copy of the repeat sits at a distance that fits the insert size. A paired aligner then gives the read a high MAPQ; see [paired-end read mapping](/paired-end-read-mapping/).

**Non-example: the alignment score.** The score of an alignment measures how well the read matches at one position. MAPQ compares that position with the others. A perfect match in a repeat has a top score and MAPQ 0.

**Non-example: a position missing from the reference.** A read from a part of the sample genome that is not in the reference, such as a new copy of a repeat, can map uniquely to the wrong copy with a high MAPQ. The posterior is computed over the reference, so it cannot account for sequence that the reference lacks.

**Non-example: a rule of thumb taken as a definition.** Pipelines often keep only reads with MAPQ at least 20 or at least 30, for example with `samtools view -q`. These cut-offs are habits of common pipelines, not part of the SAM definition, and on the scale of a given aligner they mean different things.

## Related definitions

- **Phred scale.** MAPQ uses the scale of base qualities; see [Phred quality score](/phred-quality-score/).
- **Secondary and supplementary alignments.** Other hits of the same read are written with the flags 0x100 and 0x800 of [SAM](/sam-alignment-format/). The MAPQ of the primary record already accounts for them.
- **Use in genotype calling.** A base of a read with mapping quality $m$ comes from the wrong place with probability $10^{-m/10}$. Some callers mix that into the [genotype likelihood](/genotype-likelihood/), and others cap each base quality at the read's MAPQ so that no base counts for more than its placement.
- **Pileup.** The [pileup](/read-pileup/) format shows the MAPQ of each read at its first base.

## References
