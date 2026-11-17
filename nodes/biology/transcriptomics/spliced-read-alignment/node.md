---
tag: FKJA1K
kind: problem
slug: spliced-read-alignment
name: Spliced read alignment
aliases:
- RNA-seq read mapping
area: biology/transcriptomics
level: core
summary: 'Align RNA-seq reads to a genome while allowing long gaps at introns, so that one read can span two or more exons.'
prereqs: [rna-sequencing, read-mapping]
see_also: [maximal-mappable-prefix-alignment, spliced-alignment-problem, exon-chaining, fm-index, minimizer, sam-alignment-format, smith-waterman, seed-and-extend]
sources:
  - paper: doi:10.1093/bioinformatics/btp120
    title: Cole Trapnell, Lior Pachter and Steven L. Salzberg, TopHat, discovering splice junctions with RNA-Seq, Bioinformatics 25(9) (2009)
    locator: pp. 1105 to 1111 (unspliced mapping with Bowtie, islands of coverage, and junctions between islands)
  - paper: doi:10.1093/bioinformatics/bts635
    title: Alexander Dobin, Carrie A. Davis, Felix Schlesinger, Jorg Drenkow, Chris Zaleski, Sonali Jha, Philippe Batut, Mark Chaisson and Thomas R. Gingeras, STAR, ultrafast universal RNA-seq aligner, Bioinformatics 29(1) (2013)
    locator: pp. 15 to 21 (seed search by maximal mappable prefixes in a suffix array, then clustering, stitching and scoring)
  - paper: doi:10.1038/nmeth.3317
    title: Daehwan Kim, Ben Langmead and Steven L. Salzberg, HISAT, a fast spliced aligner with low memory requirements, Nature Methods 12(4) (2015)
    locator: pp. 357 to 360 (a global FM index and many small local FM indexes)
  - paper: doi:10.1093/bioinformatics/bty191
    title: Heng Li, Minimap2, pairwise alignment for nucleotide sequences, Bioinformatics 34(18) (2018)
    locator: pp. 3094 to 3100 (spliced alignment of long reads with minimizer chaining and an intron gap cost)
  - paper: doi:10.1038/nmeth.1226
    title: Ali Mortazavi, Brian A. Williams, Kenneth McCue, Lorian Schaeffer and Barbara Wold, Mapping and quantifying mammalian transcriptomes by RNA-Seq, Nature Methods 5(7) (2008)
    locator: pp. 621 to 628 (reads that cross splice junctions)
---

Spliced read alignment is the [read mapping](/read-mapping/) problem for [RNA-seq](/rna-sequencing/) reads. A read comes from a spliced messenger RNA, so it can be made of pieces of two or more exons that lie far apart in the genome. A spliced aligner must place each piece and accept the long gap between them as an intron, while it still rejects long gaps that are only noise. The gaps can be tens of thousands of bases long, the pieces at the ends of a read can be very short, and the genome is billions of bases long, so exact dynamic programming is too slow and all practical tools seed with an index first. The main short-read tools are TopHat, STAR and HISAT, and minimap2 is the main tool for long reads.

## In plain words

A message from a gene is a copy of some parts of the gene glued together, with the parts in between cut out. A read from the message can hold the end of one part and the start of the next.

When you look for such a read in the genome, its front half is found in one place and its back half is found further along, maybe thousands of letters later. You must find both places and say that the letters between them were cut out.

This is hard for three reasons. The genome is huge. The cut can be very long. And if only a few letters of the read sit on one side of the cut, those few letters fit in many places by chance. The cut points usually begin and end with the same short signal letters, which helps to choose the right place.

## Definition

**Input.** A genome $G$ of length $n$, a read $R$ of length $m$, a scoring for matches, mismatches and short gaps, an intron length range $[I_{\min}, I_{\max}]$, and an intron penalty $p(I)$, which may depend on the length of the intron and on the bases at its two ends.

**A spliced alignment** of $R$ to $G$ splits the read into consecutive parts $R = R_1 R_2 \cdots R_k$ and aligns each part $R_j$ to a genome segment $G[a_j..b_j]$, with $b_j < a_{j+1}$ and an intron $G[b_j + 1..a_{j+1} - 1]$ whose length is in $[I_{\min}, I_{\max}]$. Its score is the sum of the alignment scores of the parts minus the penalties of the $k - 1$ introns. The first and last parts may be clipped at the read ends.

**Output.** The best-scoring spliced alignment of $R$ and of its reverse complement, or all alignments within a margin of the best when the read fits several places. Positions are 1-based, as in the [SAM format](/sam-alignment-format/), where an intron is the operation `N` of the CIGAR string.

**Splice signals.** Most introns start with GT and end with AG on the strand of the gene, the canonical motif; GC-AG and AT-AC are rarer. Aligners give canonical introns a smaller penalty, which is a heuristic based on this measured bias, not a rule without exceptions.

This problem is not the same as the [spliced alignment problem](/spliced-alignment-problem/) of gene finding. There, a set of candidate exons is given, and the task is to choose a chain of them whose spliced sequence is closest to a target sequence. In spliced read alignment no exons are given; the read itself shows where the exons are. The [exon chaining](/exon-chaining/) problem is the scoring core of that other problem.

## Variants

- **Short reads.** Reads of 50 to 150 bases with few errors and at most a few junctions each. The short end pieces are the main difficulty.
- **Long reads.** Full-length cDNA reads of thousands of bases with more errors and many junctions. Here most reads cross junctions, and indels near the junctions move them.
- **Paired-end reads.** The two reads of a [pair](/paired-end-reads/) must align on the same transcript, at a distance that fits the fragment length after the introns are removed.
- **With known junctions.** A gene annotation, or a first pass over all reads, gives a set of junctions. A second pass aligns the reads again with these junctions as cheap introns. STAR calls this the two-pass mode.
- **To the transcriptome.** Aligning to the known transcripts needs no introns, but a read then fits every isoform that shares its sequence, and new junctions are not found. [Pseudoalignment](/pseudoalignment/) and [selective alignment](/selective-alignment/) work in this setting.
- **Chimeric reads.** Reads that join two genes, two strands or two chromosomes come from fusion genes or circular RNA and need an alignment with parts that are not colinear.

## Examples

**Two exact alignments, one signal.** Let the genome be $G = \texttt{TTACGGTCCCCCCAGATTGG}$, of length 20, and the read $R = \texttt{ACGATT}$, with $I_{\min} = 5$. There are two exact spliced alignments with one intron, both with an intron of 10 bases:

| parts | genome segments | intron | intron sequence | motif |
|---|---|---|---|---|
| ACG + ATT | 3..5 and 16..18 | 6..15 | GTCCCCCCAG | GT-AG, canonical |
| AC + GATT | 3..4 and 15..18 | 5..14 | GGTCCCCCCA | GG-CA, not canonical |

Both have six matches. They differ only in where the junction is, because the base G at position 5 that ends exon 1 is the same as the base G at position 15 that ends the intron, so the junction can slide by one place. The splice signal chooses the first one, with the CIGAR `3M10N3M`. Sliding junctions like this are common, and aligners use the motif to fix one position.

**A short anchor fits by chance.** A read crosses a junction with only 8 bases on the exon 2 side. If the genome were random, a fixed string of 8 bases would occur by chance about $W / 4^8 = W / 65536$ times in a window of $W$ bases. With an allowed intron range of $W = 500\,000$ bases, that is about 7.6 chance places for the anchor. This is a calculation under a random genome model, and real genomes have repeats, so the true number is often larger. Aligners therefore ask for a minimum anchor length on junctions that no other read supports.

**A read across three exons.** A read of 150 bases with 40, 30 and 80 bases on three exons, and introns of 1200 and 300 bases, has the CIGAR `40M1200N30M300N80M`. The middle piece of 30 bases is found only if the seed search looks for it near the other two pieces or finds it unique in the whole genome.

## Known algorithms

- **Dynamic programming with an intron state.** A [Smith-Waterman](/smith-waterman/) style alignment with an extra move that skips genome bases at the intron penalty. With a penalty that does not depend on the length, it takes $O(nm)$ time (see Bounds). It is exact for its score but is used only inside small windows.
- **Map first, then split (TopHat).** Trapnell, Pachter and Salzberg (2009) first mapped the reads without splicing with Bowtie, joined the mapped reads into islands of coverage, looked for canonical junctions between nearby islands, and then aligned the unmapped reads across the candidate junctions. This finds junctions only where the islands are visible.
- **Maximal mappable prefixes (STAR).** Dobin and colleagues (2013) find the longest prefix of the read that matches the genome exactly, with a [suffix array](/suffix-array/), and repeat from the next base. The seeds are then clustered in genome windows and stitched with a scoring that allows introns. See [maximal mappable prefix alignment](/maximal-mappable-prefix-alignment/).
- **Hierarchical FM indexes (HISAT).** Kim, Langmead and Salzberg (2015) use one global [FM index](/fm-index/) of the whole genome to place the first part of a read, and tens of thousands of small local FM indexes to place the short remaining pieces near it. The local search is their answer to the short-anchor problem.
- **Minimizer chaining (minimap2).** For long reads, Li (2018) indexes the genome by [minimizers](/minimizer/), chains the shared minimizers with a gap cost that allows long gaps, and runs a final alignment in which a long deletion is cheap if it looks like an intron, with a bonus for the splice signal. See [seed chaining](/seed-chaining/).

All of these follow the [seed and extend](/seed-and-extend/) pattern: an index finds exact or near-exact seeds, and an alignment step joins the seeds and places the junctions. Only the alignment step is exact, and only for its own score inside the window it is given.

## Bounds

- **Exact DP in $O(nm)$ time.** Let $H[i][j]$ be the best score of an alignment of $R[1..i]$ that ends with $R[i]$ at $G[j]$. For a constant intron penalty $p$ and only a minimum length $I_{\min}$, the intron move into $H[i][j]$ comes from $\max_{j' \le j - 1 - I_{\min}} H[i - 1][j'] - p$. This maximum is a running prefix maximum over $j$, so each cell costs $O(1)$, and the whole table costs $O(nm)$ time. With a maximum length $I_{\max}$ too, a sliding window maximum gives the same bound. This is a theorem about the DP. For a human genome of $3 \cdot 10^9$ bases and a read of 100 bases, it is $3 \cdot 10^{11}$ cells per read, which is why the DP runs only in small windows.
- **Index size.** A full suffix array of a genome of $n$ bases takes $n \lceil \log_2 n \rceil$ bits, and STAR keeps an uncompressed one, which needs tens of gigabytes of memory for a human genome. A compressed FM index of the same genome takes a few gigabytes, and HISAT reported a much smaller memory use than STAR. Both are measurements.
- **Ambiguity is unavoidable.** If an exon piece of the read is shorter than the length that is unique in the intron window, no method can place it from the read alone. Paired reads, other reads across the same junction, or an annotation are needed.

## Reductions

- **To local alignment.** Spliced alignment inside one window is local alignment with a special gap whose cost does not grow with length. With an affine gap model, it is a three-state DP like [affine gap alignment](/affine-gap-alignment/) with one more state for the intron.
- **To chaining.** Seed-based tools reduce the global search to [colinear chaining](/colinear-chaining/) of exact matches, where a long gap between two seeds on the genome but not on the read is an intron.
- **To transcript assembly.** The aligned reads, with their junctions, are the input of genome-guided [transcript assembly](/transcript-assembly/), which builds a [splice graph](/splice-graph/) from them.

## Applications

- The first step of genome-guided RNA-seq analysis: counting reads per gene, finding new junctions, and assembling transcripts.
- Variant calling on RNA, allele-specific expression and RNA editing, which need correct alignments near junctions.
- Detection of fusion genes and circular RNA from chimeric alignments.
- Mapping full-length long reads of cDNA to find whole isoforms directly.

## References
