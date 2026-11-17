---
tag: X92GPF
kind: algorithm
slug: base-quality-score-recalibration
name: Base quality score recalibration
aliases:
- BQSR
area: biology/read-mapping-and-variant-calling
level: advanced
summary: Re-estimate base qualities from the observed mismatch rate at known non-variant sites, binned by reported quality, cycle and sequence context.
model: word-ram
complexity:
  vars: {n: the number of training bases, m: the number of bases to recalibrate, k: the number of non-empty bins}
  time: {worst: Θ(n + m), average: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(k)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2011
  people: [Mark A. DePristo, Eric Banks, Ryan Poplin]
  note: Described as a step of the GATK framework for variant discovery, with the covariates read group, reported quality, machine cycle and dinucleotide context, and dbSNP to mask known variant sites.
prereqs: [phred-quality-score, read-pileup, duplicate-read-marking]
see_also: [bayesian-genotype-calling, genotype-likelihood, variant-quality-score-recalibration, variant-calling-problem, empirical-bayes, isotonic-regression, maximum-likelihood-estimation, read-error-correction]
sources:
  - paper: doi:10.1038/ng.806
    title: Mark A. DePristo, Eric Banks, Ryan Poplin and others, A framework for variation discovery and genotyping using next-generation DNA sequencing data, Nature Genetics 43(5), 2011
    locator: pp. 491 to 498, the section on base quality score recalibration and its supplementary methods (the covariates, the dbSNP masking and the additive model on the Phred scale)
  - paper: doi:10.1101/gr.107524.110
    title: Aaron McKenna, Matthew Hanna, Eric Banks and others, The Genome Analysis Toolkit, a MapReduce framework for analyzing next-generation DNA sequencing data, Genome Research 20(9), 2010
    locator: pp. 1297 to 1303 (the GATK framework of walkers in which the recalibrator runs)
  - paper: doi:10.1101/gr.8.3.186
    title: Brent Ewing and Phil Green, Base-calling of automated sequencer traces using phred. II. Error probabilities, Genome Research 8(3), 1998
    locator: pp. 186 to 194 (quality values as calibrated error probabilities, checked against observed errors)
---

Base quality score recalibration (BQSR) corrects the base qualities that the sequencer reports. A base of [quality](/phred-quality-score/) 30 should be wrong 1 time in 1000, but the quality tables of a machine are made for average conditions, so the real error rate drifts with the run, the lane, the position of the base in the read and the bases before it. BQSR counts the mismatches with the reference at sites that are taken to be free of true variants, in bins by read group, reported quality, cycle and context, and replaces each quality with the error rate observed in its bins. The method is the one of the GATK pipeline of DePristo et al. (2011), and the code on this page leaves out several parts of the GATK tool, listed below.

## In plain words

The sequencer gives every base a score that says how much to trust it. Those scores are often a little wrong: some bases are worse than their score says, for example near the end of a read or after a G.

To fix them, look at many places in the genome where the sample is known to match the reference. There, every base that does not match is an error. Put the bases into groups by their score, by their place in the read and by the base before them, and count how often each group is wrong. Then give each base a new score that matches the error rate of its groups. Bases in a group that is wrong more often than its score says get a lower score.

## The problem

**Input.** Mapped reads, after [duplicate marking](/duplicate-read-marking/), and a set of known variant sites such as dbSNP. At each covered reference position that is not a known variant, each aligned base is one training observation $(g, q, c, x, \mu)$: the read group $g$, the reported quality $q$, the cycle $c$ (the 0-based position of the base in the read), the context $x$ (the previous base and this one, as read; none for the first base), and $\mu = 1$ if the base differs from the reference, else 0.

**Output.** A new integer quality for every base of every read, such that within each bin of the covariates the mean error probability that the new qualities give matches the observed mismatch rate.

For a bin $B$ with $m_B$ mismatches among $n_B$ observations, the empirical quality is

$$\hat Q_B = -10 \log_{10} \frac{m_B + 1}{n_B + 2},$$

where the 1 and the 2 are one pseudo-mismatch and one pseudo-match, so that a bin with no mismatch gets a finite quality.

## The algorithm

The model is additive on the Phred scale. With $n_g$ the number of observations of group $g$ and $S_g$ the sum of their reported error probabilities $10^{-q/10}$,

$$Q_{\mathrm{recal}} = q + \Delta_0(g) + \Delta_1(g, q) + \Delta_2(g, q, c) + \Delta_2(g, q, x),$$

where each $\Delta$ is the gap between the empirical quality of a bin and what the terms before it predict.

```pseudo id=main
FIT(observations)
L1  T ← empty count tables; S ← empty sums
L2  for each observation (g, q, c, x, μ) do
L3      add one base and μ mismatches to the bins (g), (g, q), (g, q, c) and, if x exists, (g, q, x)
L4      S[g] ← S[g] + 10^(-q/10)

RECALIBRATE-BASE(T, g, q, c, x)
L5  Δ0 ← Q̂(g) - (-10 log10(S[g] / n_g))
L6  Δ1 ← Q̂(g, q) - (q + Δ0), or 0 if the bin is empty
L7  Δ2 ← the sum over the covariates c and x of Q̂(g, q, ·) - (q + Δ0 + Δ1), each 0 if its bin is empty
L8  return q + Δ0 + Δ1 + Δ2

RECALIBRATE-READ(T, g, bases, qualities)
L9  for each base i, with cycle i and context bases[i-1..i] do r ← RECALIBRATE-BASE(T, g, q_i, i, x_i)
L10     q'_i ← round(r), clamped to the range 1 to 93
```

A base whose read group was not in the training data keeps its reported quality. Line L10 clamps to 93 because that is the largest quality that Phred+33 can print as one character.

## Example

One read group with all bases reported as Q30. At cycle 0 there are 9998 training bases with 9 mismatches, and at cycle 1 there are 9998 with 99 mismatches. No contexts are used.

- The group has 108 mismatches in 19996 bases, so $\hat Q(g) = -10 \log_{10}(109 / 19998) = 22.6356$. The reported qualities predict $-10 \log_{10}(0.001) = 30$, so $\Delta_0 = -7.3644$.
- The bin $(g, 30)$ is the whole group, so $\hat Q(g, 30) = 22.6356 = 30 + \Delta_0$ and $\Delta_1 = 0$.
- Cycle 0 has $\hat Q = -10 \log_{10}(10 / 10000) = 30$, so $\Delta_2 = 7.3644$ and the new quality is 30.
- Cycle 1 has $\hat Q = -10 \log_{10}(100 / 10000) = 20$, so $\Delta_2 = -2.6356$ and the new quality is 20.

The bases of cycle 0 were right to claim Q30, and those of cycle 1 were ten times worse than they claimed. A read "AC" with qualities 30, 30 comes out as 30, 20.

## Correctness

The sums telescope. By the definition of $\Delta_1$, $q + \Delta_0 + \Delta_1 = \hat Q(g, q)$, so

$$Q_{\mathrm{recal}} = \hat Q(g, q, c) + \hat Q(g, q, x) - \hat Q(g, q), \qquad 10^{-Q_{\mathrm{recal}}/10} = \frac{\hat p(g, q, c)\, \hat p(g, q, x)}{\hat p(g, q)}.$$

With one covariate, the new quality is exactly the empirical quality of the base's $(q, c)$ bin. With two, it is the product of the two marginal error rates over the rate of the $q$ bin. If within a $q$ bin the true error rate is $p_q \alpha_c \beta_x$, with independent multiplicative effects of the cycle and the context, and the cycle and the context of a base are independent, then this quotient tends to $p_q \alpha_c \beta_x$ with probability 1 as the training data grows, by the strong law of large numbers. The full proof is in proofs/correctness.md.

## Complexity

- **Time.** Fitting touches four bins per observation and recalibrating computes four empirical qualities per base. The bins have bounded keys (qualities up to 93, cycles up to the read length, 16 contexts, and the read groups), so arrays indexed by the key give $O(1)$ time per step and $\Theta(n + m)$ in total. The code uses hash tables, which give the same bound in expectation.
- **Space.** $\Theta(k)$ for the $k$ non-empty bins, which is small: a few groups times 93 qualities times the read length.
- **In practice.** The cost is in reading the BAM file twice, once to count and once to write the new qualities.

## Properties

- **Exact for its model.** The output is a fixed function of the counts. It is calibrated within each $(q, c)$ bin when only the cycle is used; with more covariates it is calibrated under the product model above.
- **Deterministic.** Given the training sites, there is no randomness.
- **Two passes.** All counts must be in before any base is recalibrated.
- **Order of the qualities.** The new quality can reorder the bases: a Q30 base at a bad cycle can get a lower quality than a Q25 base at a good one. That is the point of the method.

## Variants and improvements

The GATK tool differs from this page in several ways, which the code leaves out.

- **Priors on the deltas.** GATK estimates each $\Delta$ with a prior centered on the level above, so a bin with few observations stays near the coarser estimate instead of jumping to its own noisy rate. In the plain version on this page the levels cancel exactly, as above.
- **Indel qualities.** GATK also fits base insertion and base deletion qualities with the same covariates, which its indel-aware callers use.
- **Cycle of the second read.** GATK gives the cycles of the second read of a pair negative numbers, so the two reads get separate bins.
- **Strand and context.** For reverse-strand reads GATK takes the context in the direction of sequencing, by reverse complementing.
- **Low-quality tails.** Bases at the end of a read with a very low quality are not used as training data or changed.
- **Binned output.** To keep files small, the new qualities can be rounded to a few levels, the binning of modern Illumina instruments.
- **Other recalibrators.** Tools that train a statistical model, such as a [logistic regression](/logistic-regression/) on the covariates, or that fit a monotone map from reported to observed quality, as in [isotonic regression](/isotonic-regression/), solve the same problem.

## When to use it

BQSR was a standard step of the GATK best practices for germline short variant calling, between duplicate marking and the [variant caller](/variant-calling-problem/), because callers such as [Bayesian genotype calling](/bayesian-genotype-calling/) put the base qualities straight into the [genotype likelihoods](/genotype-likelihood/). It needs a good set of known variant sites for the organism; without one, true variants count as errors. It matters less with data whose qualities are already well calibrated or binned to few levels, and with callers that learn their own error model from the reads.

## Pitfalls

- **Unmasked variants.** A training site that is truly variant in the sample makes every alternate base count as an error. In a species with no variant database, a common workaround is to call variants once, mask the confident ones and recalibrate, sometimes for several rounds.
- **Mixing read groups.** Lanes and runs have their own error profiles. Wrong or missing read group tags merge them into one bin set.
- **Too little data.** Small targeted panels give sparse bins. The add-one counts bias the error rate of a small bin up, and a bin with few bases gives a noisy quality.
- **Recalibrating twice.** Running the tool on reads that were already recalibrated gives no new information and can shift the qualities further.
- **Clamping and rounding.** Qualities are stored as integers in 1 to 93; rounding moves the error rate by a factor of at most $10^{0.05}$, which is about 1.12.

## Implementations

## History

That base qualities should match the observed error rate goes back to phred, whose quality values were checked against the errors observed in reads of known sequence (Ewing and Green, 1998). For short reads, the recalibrator ran in the GATK framework of McKenna et al. (2010), and DePristo et al. (2011) described it as part of their framework: the covariates read group, reported quality, machine cycle and dinucleotide, the masking of the sites in dbSNP 129, and the additive model on the Phred scale. GATK 4 splits it into two tools, one that builds the tables and one that applies them.

## References
