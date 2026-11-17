---
tag: BVJ7P8
kind: definition
slug: transcripts-per-million
name: Transcripts per million
aliases:
- TPM
area: biology/transcriptomics
level: intro
summary: Length-normalized counts scaled to sum to one million in each sample, the relative molar abundance of each transcript.
prereqs: [rpkm-and-fpkm]
see_also: [rpkm-and-fpkm, transcript-abundance-estimation, em-isoform-quantification, pseudoalignment, library-size-normalization, median-of-ratios-normalization, tmm-normalization]
sources:
  - paper: doi:10.1093/bioinformatics/btp692
    title: Bo Li, Victor Ruotti, Ron M. Stewart, James A. Thomson and Colin N. Dewey, RNA-Seq gene expression estimation with read mapping uncertainty, Bioinformatics 26(4) (2010), pages 493 to 500
    locator: the nucleotide fractions and transcript fractions of the RSEM model, and transcripts per million as the transcript fraction times one million
  - paper: doi:10.1186/1471-2105-12-323
    title: Bo Li and Colin N. Dewey, RSEM, accurate transcript quantification from RNA-Seq data with or without a reference genome, BMC Bioinformatics 12 (2011), article 323
    locator: the TPM output of RSEM and the effective length used to convert nucleotide fractions to transcript fractions
  - paper: doi:10.1007/s12064-012-0162-3
    title: Günter P. Wagner, Koryu Kin and Vincent J. Lynch, Measurement of mRNA abundance using RNA-seq data, RPKM measure is inconsistent among samples, Theory in Biosciences 131(4) (2012), pages 281 to 285
    locator: the argument that a unit of relative molar abundance must have the same mean in every sample, which TPM has and RPKM does not
---

Transcripts per million (TPM) is a unit of expression for RNA-seq. For each transcript, divide its read count by its effective length, then scale these rates so that they sum to one million in the sample. The result estimates how many of every million transcript molecules in the sample are copies of this transcript. Li et al. (2010) defined it as the transcript fraction of the RSEM model times $10^6$, and Wagner, Kin and Lynch (2012) argued that it should replace [RPKM and FPKM](/rpkm-and-fpkm/). TPM is the same as FPKM up to one factor per sample, and that factor makes the total the same in every sample. It is still a relative unit: when one transcript goes up, the TPM of every other transcript goes down.

## Definition

Let transcript $i$ have the count $C_i$ (reads or fragments, possibly an expected count from [EM isoform quantification](/em-isoform-quantification/)) and the effective length $\tilde L_i$, the number of positions where a fragment can start, about $L_i - \bar\ell + 1$ for a mean fragment length $\bar\ell$. Then
$$\mathrm{TPM}_i = 10^6\,\frac{C_i/\tilde L_i}{\sum_j C_j/\tilde L_j}.$$
For a gene, the TPM is the sum of the TPM values of its transcripts.

**What it estimates.** Suppose the sample holds the transcripts in the proportions $\tau_1, \tau_2, \dots$ by molecule, with $\sum_i\tau_i = 1$, and each fragment comes from a uniform position of a uniform molecule. A molecule of transcript $i$ offers $\tilde L_i$ start positions, so the expected share of fragments from transcript $i$ is $\theta_i = \tau_i\tilde L_i/\sum_j\tau_j\tilde L_j$. Solving for $\tau$ gives $\tau_i = (\theta_i/\tilde L_i)/\sum_j(\theta_j/\tilde L_j)$. With $\theta_i$ estimated by $C_i/N$, this is $\mathrm{TPM}_i/10^6$. Li et al. (2010) call $\theta$ the nucleotide fractions and $\tau$ the transcript fractions. This is a model with uniform fragment starts; real libraries have positional and sequence biases, which tools such as Salmon model.

**Properties that follow from the formula.**

- The TPM values of a sample sum to $10^6$, so their mean over $n$ transcripts is $10^6/n$ in every sample with the same annotation.
- Multiplying every count of a sample by $c > 0$ does not change its TPM values. So TPM removes depth.
- $\mathrm{TPM}_i = 10^6\,\mathrm{FPKM}_i/\sum_j\mathrm{FPKM}_j$ in the same sample, because FPKM is $C_i/\tilde L_i$ times the factor $10^9/N$, which cancels.

## Examples and non-examples

**The check values.** Three transcripts have lengths 1000, 2000 and 500 bases and 100 fragments each. The rates $C_i/L_i$ are 0.1, 0.05 and 0.2, with sum 0.35.

| transcript | $L_i$ | $C_i$ | rate | TPM | FPKM |
|---|---|---|---|---|---|
| 1 | 1000 | 100 | 0.1 | 285714 | 333333 |
| 2 | 2000 | 100 | 0.05 | 142857 | 166667 |
| 3 | 500 | 100 | 0.2 | 571429 | 666667 |

So $\mathrm{TPM}_1 = 10^6 \cdot 0.1/0.35 = 285714$, and $285714 = 10^6 \cdot 333333/1166667$, the FPKM rescaled. The short transcript 3 has the largest TPM: the same number of fragments from a shorter molecule means more molecules.

**Depth does not matter.** If the sample is sequenced twice as deeply, with 200 fragments for each transcript, the rates double and the TPM values stay 285714, 142857 and 571429.

**Non-example: TPM as an absolute level.** In a second sample, transcripts 1 and 2 have the same number of molecules as before, and transcript 3 has 10 times more. The expected rates become 0.1, 0.05 and 2.0, with sum 2.15, so the TPM values are 46512, 23256 and 930233. The TPM of transcript 1 fell by a factor of 6.1, but the transcript did not change. TPM measures a share, and shares must move when one part grows. To compare samples, [library size normalization](/library-size-normalization/) assumes that most genes do not change and finds the factor per sample under that assumption. [TMM](/tmm-normalization/) and [median of ratios](/median-of-ratios-normalization/) do this on counts. Spike-in RNA of known amount is the only way to measure absolute change.

**Non-example: TPM as input to a count test.** TPM values are not counts, and their variance does not follow a [negative binomial model](/negative-binomial-count-model/). For [differential expression analysis](/differential-expression-analysis/), use the counts, or the estimated counts with an offset for the average transcript length, as tximport does for gene-level tests.

## Related definitions

- [RPKM and FPKM](/rpkm-and-fpkm/): the same length-normalized rates scaled by $10^9/N$ in place of $10^6/\sum_j C_j/\tilde L_j$. Their sum changes between samples, and that is the difference from TPM.
- Counts per million (CPM): $10^6 C_i/N$, with no length correction.
- [Transcript abundance estimation](/transcript-abundance-estimation/): the problem of finding the fractions $\theta$ and $\tau$ when reads are compatible with many transcripts. RSEM, kallisto and Salmon report TPM from its solution.
- [Pseudoalignment](/pseudoalignment/): a fast way to find the compatible transcripts of each read, before the fractions are estimated.

## References
