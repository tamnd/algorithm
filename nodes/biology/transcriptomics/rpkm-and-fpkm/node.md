---
tag: NX7YC9
kind: definition
slug: rpkm-and-fpkm
name: RPKM and FPKM
aliases:
- reads per kilobase per million
area: biology/transcriptomics
level: intro
summary: Counts of reads or fragments per kilobase of transcript per million mapped reads, an early unit of expression that corrects for length.
prereqs: [rna-sequencing]
see_also: [transcripts-per-million, transcript-abundance-estimation, library-size-normalization, em-isoform-quantification, median-of-ratios-normalization, tmm-normalization, differential-expression-analysis]
sources:
  - paper: doi:10.1038/nmeth.1226
    title: Ali Mortazavi, Brian A. Williams, Kenneth McCue, Lorian Schaeffer and Barbara Wold, Mapping and quantifying mammalian transcriptomes by RNA-Seq, Nature Methods 5(7) (2008), pages 621 to 628
    locator: the definition of RPKM, reads per kilobase of exon model per million mapped reads
  - paper: doi:10.1038/nbt.1621
    title: Cole Trapnell, Brian A. Williams, Geo Pertea, Ali Mortazavi, Gordon Kwan, Marijke J. van Baren, Steven L. Salzberg, Barbara J. Wold and Lior Pachter, Transcript assembly and quantification by RNA-Seq reveals unannotated transcripts and isoform switching during cell differentiation, Nature Biotechnology 28(5) (2010), pages 511 to 515
    locator: FPKM, fragments per kilobase of transcript per million mapped fragments, as the abundance unit of Cufflinks
  - paper: doi:10.1007/s12064-012-0162-3
    title: Günter P. Wagner, Koryu Kin and Vincent J. Lynch, Measurement of mRNA abundance using RNA-seq data, RPKM measure is inconsistent among samples, Theory in Biosciences 131(4) (2012), pages 281 to 285
    locator: the argument that the mean RPKM changes between samples, and the proposal of TPM
  - paper: doi:10.1093/bioinformatics/btp692
    title: Bo Li, Victor Ruotti, Ron M. Stewart, James A. Thomson and Colin N. Dewey, RNA-Seq gene expression estimation with read mapping uncertainty, Bioinformatics 26(4) (2010), pages 493 to 500
    locator: transcript fractions and the comparison of RPKM-like units with transcripts per million
---

RPKM and FPKM are units of expression for RNA-seq. RPKM is the number of reads that map to a transcript or gene, per kilobase of its length, per million mapped reads. FPKM is the same with fragments in place of reads, so that the two mates of a paired-end fragment count once. Both divide by length, because a longer transcript gives more reads at the same molar level, and by the total count, because a deeper library gives more reads for every gene. Mortazavi et al. (2008) defined RPKM, and Trapnell et al. (2010) used FPKM in Cufflinks. The [transcripts per million](/transcripts-per-million/) unit has replaced both for comparisons between samples, because FPKM values of one sample do not sum to a fixed total. Neither unit is a good input for [differential expression analysis](/differential-expression-analysis/), which works on raw counts with size factors.

## Definition

Let transcript (or gene) $i$ have $C_i$ mapped reads or fragments and length $L_i$ in bases, and let $N = \sum_j C_j$ be the total number of mapped reads or fragments in the sample. Then
$$\mathrm{RPKM}_i = \frac{C_i}{(L_i/10^3)(N/10^6)} = \frac{10^9\,C_i}{L_i N}.$$
FPKM has the same formula, with $C_i$ and $N$ counted in fragments. For single-end data the two units are equal.

**Effective length.** A fragment of length $\ell$ can start at only $L_i - \ell + 1$ positions of a transcript of length $L_i$. Tools such as Cufflinks, RSEM and Salmon therefore use an effective length $\tilde L_i$, about $L_i - \bar\ell + 1$ for a mean fragment length $\bar\ell$, in place of $L_i$. For a short transcript this changes the value a lot.

**What $C_i$ is.** When a read maps to more than one transcript, $C_i$ is not a plain count. It is the expected number of reads from transcript $i$, from [EM isoform quantification](/em-isoform-quantification/) or a similar method of [transcript abundance estimation](/transcript-abundance-estimation/). For genes, $C_i$ is often the count of reads on the union of the exons, and then the length of the gene is a choice that the unit depends on.

**Relation to TPM.** In the same sample, with the same lengths,
$$\mathrm{TPM}_i = 10^6\,\frac{C_i/L_i}{\sum_j C_j/L_j} = 10^6\,\frac{\mathrm{FPKM}_i}{\sum_j \mathrm{FPKM}_j},$$
because the factor $10^9/N$ is the same for all $i$ and cancels. So TPM is FPKM rescaled to sum to $10^6$ in each sample, and the two units rank the transcripts of one sample in the same order.

## Examples and non-examples

**The check values.** Three transcripts have lengths 1000, 2000 and 500 bases and 100 fragments each, so $N = 300$.

| transcript | $L_i$ | $C_i$ | FPKM | TPM |
|---|---|---|---|---|
| 1 | 1000 | 100 | 333333 | 285714 |
| 2 | 2000 | 100 | 166667 | 142857 |
| 3 | 500 | 100 | 666667 | 571429 |

For transcript 1, $\mathrm{FPKM} = 10^9 \cdot 100/(1000 \cdot 300) = 333333$. The rates $C_i/L_i$ are 0.1, 0.05 and 0.2, with sum 0.35, so $\mathrm{TPM}_1 = 10^6 \cdot 0.1/0.35 = 285714$. The FPKM values sum to 1166667, not to $10^6$.

**The sum changes with composition.** In a second sample the same transcripts have 100, 100 and 400 fragments, so $N = 600$. The FPKM values are 166667, 83333 and 1333333, with sum 1583333. The TPM values are 105263, 52632 and 842105, with sum $10^6$. The sum of FPKM moved from 1166667 to 1583333 only because the mix of transcripts changed. This is the inconsistency that Wagner, Kin and Lynch (2012) pointed out: the mean FPKM is not the same in two samples, so a value of 10 does not mean the same share of the transcripts in both.

**Non-example: a ratio between samples.** Transcript 1 has FPKM 333333 in the first sample and 166667 in the second. This ratio of 2 does not show that transcript 1 changed. The total $N$ in the denominator depends on every other transcript, and transcript 3 took a larger share of the reads in the second sample. Methods for [library size normalization](/library-size-normalization/) such as [median of ratios](/median-of-ratios-normalization/) and [TMM](/tmm-normalization/) exist to fix this, and they assume that most genes do not change.

**Non-example: input for count models.** FPKM is not a count. A [negative binomial model](/negative-binomial-count-model/) needs the raw counts, because its variance depends on the count scale. Dividing by length and depth first destroys this. Count-based tools put the depth into an offset and leave the length out, since it cancels when the same gene is compared across samples.

## Related definitions

- [Transcripts per million](/transcripts-per-million/): the length-normalized rates scaled to sum to $10^6$ in each sample, an estimate of relative molar abundance. It differs from FPKM only by a factor that is the same for every transcript of one sample.
- Counts per million (CPM): $10^6 C_i/N$, depth-normalized but not length-normalized, used to filter genes with low counts before a test.
- [Library size normalization](/library-size-normalization/): the problem of finding a factor per sample that makes counts comparable across samples. RPKM uses the plain total $N$, which is the simplest and least robust answer.
- [Transcript abundance estimation](/transcript-abundance-estimation/): the problem of finding $C_i$ when reads map to many isoforms.

## References
