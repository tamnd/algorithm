---
tag: V5VT5P
kind: concept
slug: assembly-quality-assessment
name: Assembly quality assessment
aliases:
- assembly evaluation
area: biology/genome-assembly
level: core
summary: "Measure a genome assembly on three axes: contiguity (N50, NG50), correctness (misassemblies, base errors, QV) and completeness (genome fraction, conserved genes, k-mers)."
prereqs: [n50, contig, genome-assembly-problem]
see_also: [lander-waterman-model, scaffold, consensus-sequence-calling, kmer-spectrum, read-mapping, genome-repeat, sequencing-coverage, reference-guided-assembly]
sources:
  - paper: doi:10.1093/bioinformatics/btt086
    title: Alexey Gurevich, Vladislav Saveliev, Nikolay Vyahhi and Glenn Tesler, QUAST, quality assessment tool for genome assemblies, Bioinformatics 29(8), 2013
    locator: pp. 1072 to 1075, the metrics with and without a reference, NA50 and the misassembly types
  - paper: doi:10.1093/bioinformatics/btv351
    title: Felipe A. Simão, Robert M. Waterhouse, Panagiotis Ioannidis, Evgenia V. Kriventseva and Evgeny M. Zdobnov, BUSCO, assessing genome assembly and annotation completeness with single-copy orthologs, Bioinformatics 31(19), 2015
    locator: pp. 3210 to 3212, complete, duplicated, fragmented and missing single-copy orthologs
  - paper: doi:10.1186/s13059-020-02134-9
    title: Arang Rhie, Brian P. Walenz, Sergey Koren and Adam M. Phillippy, Merqury, reference-free quality, completeness, and phasing assessment for genome assemblies, Genome Biology 21, 2020
    locator: article 245, the k-mer based consensus quality value and k-mer completeness
  - paper: doi:10.1016/j.ygeno.2010.03.001
    title: Jason R. Miller, Sergey Koren and Granger Sutton, Assembly algorithms for next-generation sequencing data, Genomics 95(6), 2010
    locator: pp. 315 to 327, contig and scaffold metrics and the errors of assemblers
---

Assembly quality assessment is the measurement of how good a genome assembly is, along three axes: contiguity, correctness and completeness. Contiguity asks how long the contigs are, correctness asks how many joins and bases are wrong, and completeness asks how much of the genome the assembly contains. No single number captures all three, and each number can be improved at the cost of another, so tools such as QUAST, BUSCO and Merqury report a set of metrics.

## In plain words

You rebuilt a torn book from its pieces and want to know how well you did. First, how long are your rebuilt passages? A few long passages are better than many short ones. Second, are the passages right? A passage can join two parts of the book that do not belong together, or it can have wrong letters. Third, is everything there? Some pages may be missing.

If you have a clean copy of the book, you compare against it. If you do not, you check other things: whether well-known chapters appear exactly once, and whether every short word in your text also occurs in the torn pieces. Long passages are easy to get by joining pieces carelessly, so length alone says little.

## The idea

**Model.** The genome has length $G$ and is sequenced by $N$ reads of length about $L$, so the coverage is $c = NL/G$. The assembly is a set of contigs, or scaffolds, of lengths $\ell_1 \ge \ell_2 \ge \cdots$ with total $A = \sum_i \ell_i$. Base accuracy is given as a Phred quality value $\mathrm{QV} = -10 \log_{10} e$, where $e$ is the error rate per base; QV 40 means one error in $10^4$ bases.

**Contiguity.** The [N50](/n50/) is the largest $\ell_j$ such that $\ell_1 + \cdots + \ell_j \ge A/2$, and L50 is that index $j$. NG50 uses $G/2$ in place of $A/2$, so that assemblies of different total size are compared against the same target. N$x$ and NG$x$ use $x$ percent. For a reference-free estimate of what to expect, the [Lander-Waterman model](/lander-waterman-model/) gives the expected number of contigs under random read positions, and [genome repeats](/genome-repeat/) longer than the reads limit the contig length further.

**Correctness.** With a reference, QUAST aligns the contigs to it. A misassembly is a breakpoint where the two flanking parts of a contig align far apart on the reference, on opposite strands, or on different chromosomes; QUAST calls these relocations, inversions and translocations. Base errors are counted as mismatches and short indels per 100 kb of aligned sequence. NA50 is the N50 of the aligned blocks after each contig is cut at its misassemblies, so false joins do not raise it. Without a reference, Merqury compares the $k$-mers of the assembly with the $k$-mers of accurate reads. A $k$-mer of the assembly that never occurs in the reads probably contains an error. If $K_a$ of the $K$ $k$-mers of the assembly are absent from the reads, the estimate of the error rate is $e = 1 - (1 - K_a/K)^{1/k}$, which assumes that each base error destroys the $k$ $k$-mers that cover it and that the reads contain every true $k$-mer.

**Completeness.** With a reference, the genome fraction is the share of reference bases covered by aligned contigs, and the duplication ratio is the aligned length divided by the covered length. Without a reference, BUSCO searches the assembly for a set of genes that occur once in almost every genome of a lineage, and reports the percentages of complete single-copy, complete duplicated, fragmented and missing genes. Merqury reports the share of the reliable read $k$-mers that occur in the assembly. A high duplicated count shows that two haplotypes or two copies of a region were kept apart where they should be one, or that one region was assembled twice.

**The three axes conflict.** Joining contigs at every ambiguous branch raises N50 and lowers correctness. Removing short contigs raises N50, because $A$ falls, and lowers completeness. Polishing raises QV but does not change contiguity. Report contiguity together with correctness and completeness, and prefer NG50 and NA50 to N50 when they can be computed.

## Examples

**N50 and NG50.** An assembly has seven contigs of 80, 70, 50, 40, 30, 20 and 10 kb, so $A = 300$ kb.

| metric | how | value |
|---|---|---|
| N50 | $80 + 70 = 150 \ge 150$ | 70 kb, L50 = 2 |
| N90 | $80 + 70 + 50 + 40 + 30 = 270 \ge 270$ | 30 kb |
| NG50, $G = 400$ kb | $80 + 70 + 50 = 200 \ge 200$ | 50 kb |
| NG50, $G = 600$ kb | all contigs needed for 300 kb | 10 kb |

**A false join raises N50.** Suppose the assembler joins the contigs of 70 and 50 kb, but they come from distant places in the genome. The contigs are now 120, 80, 40, 30, 20 and 10 kb, and $120 + 80 = 200 \ge 150$, so N50 rises from 70 to 80 kb. A reference shows one relocation inside the contig of 120 kb; cutting there gives the blocks of the original assembly, so NA50 is 70 kb.

**Short contigs and the denominator.** Add 100 contigs of 1 kb to the first assembly. Then $A = 400$ kb and N50 falls to 50 kb, since $80 + 70 = 150 < 200$ but $80 + 70 + 50 = 200$. Removing them raises N50 back to 70 kb, while NG50 with $G = 400$ kb is 50 kb in both cases.

**Quality values.** One error per 1000, $10^4$ and $10^5$ bases gives QV 30, 40 and 50. With $k = 21$, if 1000 of $10^7$ assembly $k$-mers are absent from the reads, then $e = 1 - (1 - 10^{-4})^{1/21} \approx 4.76 \cdot 10^{-6}$, which is QV 53.2. With 100 such $k$-mers it is QV 63.2.

## Where it is used

- Choosing between assemblers and parameters, such as the $k$ of a [de Bruijn assembler](/de-bruijn-assembly/) or the minimum overlap of an [overlap-layout-consensus](/overlap-layout-consensus/) assembler. QUAST was written to compare several assemblies of the same data in one report.
- Deciding whether to polish: a low QV calls for another round of [consensus calling](/consensus-sequence-calling/), and the QV after polishing shows whether it helped.
- Finding misassemblies to break: alignment to a related genome, or read pairs and long reads that do not map consistently across a join.
- Checking a [reference-guided assembly](/reference-guided-assembly/): there the reference is part of the method, so a reference-based metric against the same reference overstates the quality, and reference-free metrics are needed.
- Reporting a new genome: published assemblies usually give contig and scaffold N50, BUSCO completeness and a QV.

## References
