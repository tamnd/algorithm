---
tag: WWCQDX
kind: concept
slug: rna-sequencing
name: RNA sequencing
aliases:
- RNA-seq
area: biology/transcriptomics
level: intro
summary: 'Measuring the transcripts of a sample by converting RNA to cDNA, sequencing fragments, and counting the reads that come from each gene or isoform.'
prereqs: [read-mapping]
see_also: [spliced-read-alignment, transcript-assembly, transcript-abundance-estimation, rpkm-and-fpkm, transcripts-per-million, differential-expression-analysis, single-cell-rna-sequencing, paired-end-reads]
sources:
  - paper: doi:10.1038/nmeth.1226
    title: Ali Mortazavi, Brian A. Williams, Kenneth McCue, Lorian Schaeffer and Barbara Wold, Mapping and quantifying mammalian transcriptomes by RNA-Seq, Nature Methods 5(7) (2008)
    locator: pp. 621 to 628 (the protocol, reads across splice junctions, and RPKM)
  - paper: doi:10.1038/nrg2484
    title: Zhong Wang, Mark Gerstein and Michael Snyder, RNA-Seq, a revolutionary tool for transcriptomics, Nature Reviews Genetics 10(1) (2009)
    locator: pp. 57 to 63 (the steps of an experiment and the challenges of the analysis)
  - paper: doi:10.1186/s13059-016-0881-8
    title: Ana Conesa, Pedro Madrigal, Sonia Tarazona, David Gomez-Cabrero, Alejandra Cervera, Andrew McPherson, Michał Wojciech Szcześniak, Daniel J. Gaffney, Laura L. Elo, Xuegong Zhang and Ali Mortazavi, A survey of best practices for RNA-seq data analysis, Genome Biology 17 (2016)
    locator: Article 13 (design, read mapping, quantification and normalization)
---

RNA sequencing, or RNA-seq, measures which transcripts a sample holds and how much of each. The RNA is copied into complementary DNA (cDNA), cut into short fragments, and sequenced, which gives millions of short reads. The reads are then placed on a genome or a set of known transcripts, and the number of reads that fall on each gene or isoform is the measure of its expression. Mortazavi, Williams, McCue, Schaeffer and Wold (2008) showed the method on mouse tissues, with reads that cross splice junctions and a count normalized by length and depth. Most of the computational problems of the area start from these reads: [spliced alignment](/spliced-read-alignment/), [transcript assembly](/transcript-assembly/) and [abundance estimation](/transcript-abundance-estimation/).

## In plain words

A cell copies some of its genes into messenger molecules. A gene that is busy makes many copies, and a quiet gene makes few. RNA sequencing takes all the messages of a sample, breaks them into short pieces, and reads each piece.

To find out where a piece came from, you look it up in the genome. Then you count the pieces for each gene. More pieces means more messages, but a long message also gives more pieces than a short one, and a deeper run gives more pieces of everything. So the counts must be corrected for length and for the size of the run before you compare them.

Many genes make several versions of their message, which share some parts. A piece from a shared part fits more than one version, so the counts per version must be estimated, not just read off.

## The idea

**The experiment.** An RNA-seq experiment has these steps.

1. Extract the RNA of the sample. Most of it is ribosomal RNA, so the protocol keeps the messenger RNA, for example by its poly-A tail, or removes the ribosomal RNA.
2. Cut the RNA, or later the cDNA, into fragments of a few hundred bases.
3. Copy the fragments into cDNA with reverse transcriptase, add adapters, and amplify them by PCR.
4. Sequence one end of each fragment (single-end reads) or both ends ([paired-end reads](/paired-end-reads/)).

**Reads cross exons.** A messenger RNA is spliced: the introns are cut out and the exons are joined. A read from a junction of two exons is therefore not a contiguous substring of the genome. Its first part matches the end of one exon and its second part matches the start of the next exon, which can be thousands of bases away. Plain [read mapping](/read-mapping/) does not find such reads. This is the problem of [spliced read alignment](/spliced-read-alignment/).

**The count model.** In the usual model, the fragments are a random sample of the cDNA molecules. A transcript $t$ with $c_t$ copies per cell and length $\ell_t$ gives a share of fragments proportional to $c_t \ell_t$. This is a model assumption, not a theorem: real libraries have positional bias, GC bias and bias from the random primers, and methods correct for them in part. Under the model, the count $C$ of a transcript must be divided by its length $L$ and by the total number of reads $N$ before transcripts and samples can be compared.

- **FPKM** (fragments per kilobase of transcript per million fragments) is $C \cdot 10^9 / (L \cdot N)$. RPKM, the version of Mortazavi and colleagues for reads, has the same form. See [RPKM and FPKM](/rpkm-and-fpkm/).
- **TPM** (transcripts per million) first divides each count by its length, $r_t = C_t / L_t$, and then scales the rates to sum to $10^6$: $\mathrm{TPM}_t = 10^6 \cdot r_t / \sum_u r_u$. See [transcripts per million](/transcripts-per-million/). TPM values add up to $10^6$ in every sample, and FPKM values do not.

In practice the length $L$ is an *effective length*, the number of positions at which a fragment can start, which is shorter than the transcript by about the mean fragment length.

**Isoforms share reads.** Alternative splicing makes several isoforms from one gene, and gene families share sequence. A read that fits two isoforms cannot be counted for both. The usual answer is a [maximum likelihood](/maximum-likelihood-estimation/) estimate of the isoform abundances, found by [EM](/em-isoform-quantification/), in which each shared read is split among the isoforms that it fits.

**The analysis.** A typical analysis aligns the reads to the genome with a spliced aligner, or maps them to a transcript set by [pseudoalignment](/pseudoalignment/) or [selective alignment](/selective-alignment/). It then estimates the abundances, normalizes them, and compares conditions by [differential expression analysis](/differential-expression-analysis/). Without a good genome, the transcripts are first built by [de novo transcriptome assembly](/de-novo-transcriptome-assembly/).

This page uses 1-based genome positions, as in the SAM format.

## Examples

**Normalizing three transcripts.** Three transcripts have lengths 1000, 2000 and 500 bases, and each gets 100 reads, so $N = 300$.

| transcript | length $L$ | count $C$ | FPKM $= C \cdot 10^9 / (L N)$ | rate $C / L$ | TPM |
|---|---|---|---|---|---|
| $t_1$ | 1000 | 100 | 333333 | 0.1 | 285714 |
| $t_2$ | 2000 | 100 | 166667 | 0.05 | 142857 |
| $t_3$ | 500 | 100 | 666667 | 0.2 | 571429 |

The rates add up to 0.35, so $\mathrm{TPM}_1 = 10^6 \cdot 0.1 / 0.35 \approx 285714$. The counts are equal, but the short transcript $t_3$ has four times as many copies as $t_2$, because a copy of $t_3$ gives a quarter of the fragments that a copy of $t_2$ gives. The FPKM values here are large because only 300 reads are counted; with millions of reads they are in the usual range.

**A read across a junction.** Exon 1 ends at genome position 1060, the intron covers positions 1061 to 1560, and exon 2 starts at 1561. A read of 100 bases starts at position 1001. Its first 60 bases match positions 1001 to 1060, and its last 40 bases match positions 1561 to 1600. In the [SAM format](/sam-alignment-format/) its alignment is the CIGAR string `60M500N40M`: 60 aligned bases, a skip of 500 reference bases for the intron, and 40 aligned bases. An unspliced aligner can at best align the first 60 bases and clip the rest.

**The count depends on the length.** Two genes have the same number of messages per cell. Gene A has a transcript of 4000 bases and gene B one of 1000 bases. Under the count model, A gets about four times as many reads as B. A raw count would call A four times as expressed, and both FPKM and TPM correct this.

## Where it is used

- **Gene expression.** Expression levels of all genes at once, and [differential expression](/differential-expression-analysis/) between conditions, with count models such as the [negative binomial](/negative-binomial-count-model/).
- **Isoforms and splicing.** New exons, splice junctions and isoforms, found by [transcript assembly](/transcript-assembly/), and changes in isoform use between conditions.
- **New organisms.** A transcript set for a species without a reference genome, by [de novo assembly](/de-novo-transcriptome-assembly/).
- **Single cells.** [Single-cell RNA-seq](/single-cell-rna-sequencing/) measures thousands of cells one by one, with molecule barcodes that are counted after [UMI deduplication](/umi-deduplication/).
- **Variants in RNA.** Allele-specific expression, RNA editing and fusion genes, where reads cross the junction of two genes.

## References
