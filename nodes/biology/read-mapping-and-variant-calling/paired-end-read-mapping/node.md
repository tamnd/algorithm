---
tag: 0K9R9Q
kind: problem
slug: paired-end-read-mapping
name: Paired-end read mapping
aliases:
- mate pair mapping
- mate rescue
area: biology/read-mapping-and-variant-calling
level: core
summary: Map both reads of a pair to a reference so that their strands and distance fit the library's insert size distribution. Seed and extend is used for each read, with mate rescue.
prereqs: [read-mapping, paired-end-reads, seed-and-extend]
see_also: [bwa, bowtie, minimap2, mapping-quality, sam-alignment-format, discordant-read-pair-method, smith-waterman, semi-global-alignment]
sources:
  - paper: doi:10.1093/bioinformatics/btp324
    title: Heng Li and Richard Durbin, Fast and accurate short read alignment with Burrows-Wheeler transform, Bioinformatics 25(14), 2009
    locator: pp. 1754 to 1760, Methods, the part on paired-end mapping (the insert size estimated from the data, the pairing of hits, and the Smith-Waterman search for an unmapped mate)
  - paper: doi:10.1101/gr.078212.108
    title: Heng Li, Jue Ruan and Richard Durbin, Mapping short DNA sequencing reads and calling variants using mapping quality scores, Genome Research 18(11), 2008
    locator: pp. 1851 to 1858, Methods (paired-end reads in Maq and the mapping quality of a pair)
  - url: https://arxiv.org/abs/1303.3997
    title: Heng Li, Aligning sequence reads, clone sequences and assembly contigs with BWA-MEM, arXiv 1303.3997, 2013
    locator: Section 2, the part on paired-end mapping (the pair score with an insert size penalty and the mate rescue step)
  - paper: doi:10.1038/nmeth.1923
    title: Ben Langmead and Steven L. Salzberg, Fast gapped-read alignment with Bowtie 2, Nature Methods 9(4), 2012
    locator: pp. 357 to 359 (paired-end alignment, concordant and discordant pairs)
  - url: https://samtools.github.io/hts-specs/SAMv1.pdf
    title: The SAM/BAM Format Specification, version 1.6, hts-specs
    locator: Section 1.4 (the FLAG bits of paired reads, RNEXT, PNEXT and TLEN)
---

Paired-end read mapping is [read mapping](/read-mapping/) for [read pairs](/paired-end-reads/): the two reads come from the two ends of one DNA fragment, so they must map to opposite strands at a distance that fits the length of the fragments in the library. The constraint helps in two ways. A read that falls in a repeat can be placed by its uniquely mapped mate, and a read with too many errors for the seed search can be found by a direct alignment near its mate, which is called *mate rescue*. Mappers such as [BWA](/bwa/), [Bowtie](/bowtie/) 2 and [minimap2](/minimap2/) solve the problem with [seed and extend](/seed-and-extend/) on each read and a pairing step. This page is about mapping the pairs; the reads and their insert sizes are on [paired-end reads](/paired-end-reads/).

## In plain words

Two short lines are torn from the two ends of one strip of paper, and the strips in this batch are all about the same length. You look for each line in a long book. One line fits in only one place. The other fits in two places, because the book repeats a sentence. Only one of those two places is about one strip length away from the first line, so that is the answer.

Sometimes one line has so many smudges that you cannot find it by searching for short exact pieces. But you know roughly where it must be: about one strip length from its partner. So you compare it letter by letter against just that part of the book, which is a small and cheap search.

## Definition

Positions are 1-based, as in SAM.

**Input.**

- A reference $R$ of length $G$ over $\{A, C, G, T\}$.
- Read pairs $(x_1, x_2)$, each read of length about $L$, with base qualities.
- A library model: the expected orientation, which for standard Illumina paired-end libraries is FR (the leftmost read on the forward strand and the other on the reverse strand, pointing toward each other), and an insert size distribution $f$ on the fragment length $t$. Often $f$ is close to normal with mean $\mu$ and standard deviation $\sigma$, and mappers estimate it from the pairs whose two reads map uniquely.
- A scoring scheme for single reads, as in [read mapping](/read-mapping/).

**Placements.** A placement of a pair gives each read a position, a strand and an alignment. If the reads lie on one chromosome in the expected orientation, the *observed template length* $t$ runs from the leftmost aligned base of the left read to the rightmost aligned base of the right read.

**Output.** For each pair, the placement that maximizes the pair score

$$S = s_1 + s_2 + \lambda \log f(t)$$

over placements in the expected orientation, where $s_1$ and $s_2$ are the alignment scores of the two reads and $\lambda$ converts the log density into score units. If the best such placement is much worse than the best placements of the two reads alone, the reads are reported separately as a *discordant* or unpaired pair. The output also flags whether the pair is *proper* (SAM flag 0x2), and gives each read a [mapping quality](/mapping-quality/) that takes the pair into account.

**The probabilistic form.** With the scores replaced by log-likelihoods, $S$ is the log of $P(x_1 \mid u_1) P(x_2 \mid u_2) f(t)$, so maximizing $S$ is finding the most probable joint origin of the two reads, and the posterior over joint origins gives the mapping quality of the pair.

## Variants

- **Mate rescue.** When one read maps with confidence and the other has no good hit, align the other read, or its reverse complement, against the window of the reference where the insert size model says it must be, on the expected strand. For a left read at $u_1$, a right read of length $L$ and inserts within $4\sigma$ of the mean, the window runs from $u_1 + \mu - 4\sigma - L$ to $u_1 + \mu + 4\sigma - 1$. The alignment is a [Smith-Waterman](/smith-waterman/) or [semi-global](/semi-global-alignment/) alignment of $L$ bases against a window of $O(\sigma + L)$ bases, which is cheap. The alias "mate rescue" names this step, not the whole problem.
- **Mate pairs.** Mate pair libraries have long inserts, thousands of bases, made by circularizing long fragments, and their reads face away from each other (RF orientation). The problem is the same with another orientation and another $f$. The alias "mate pair mapping" uses that name loosely, since standard paired-end reads are not mate pairs.
- **Unknown insert size.** Mappers estimate $\mu$ and $\sigma$ from a batch of pairs whose reads both map uniquely, using robust statistics such as quartiles so that pairs from structural variants do not distort the estimate.
- **Hard bounds.** Bowtie 2 takes a smallest and a largest fragment length, `-I` and `-X`, and calls a pair concordant only inside them, in place of a density $f$.
- **Split and chimeric pairs.** When the best alignment of a read is in two parts, the parts are written as a primary and a supplementary record, and only one part is paired with the mate.

## Examples

**Scoring the insert size.** Take $\mu = 300$ and $\sigma = 30$. For a normal density $f$,

| $t$ | $\log_{10} f(t)$ | penalty against $t = 300$ in Phred units |
|---|---|---|
| 300 | $-1.876$ | 0 |
| 350 | $-2.479$ | 6.0 |
| 420 | $-5.351$ | 34.7 |

So a pair with $t = 350$ costs as much as one mismatch at a base of quality 6, while $t = 420$, four standard deviations away, costs as much as a mismatch at a Q35 base.

**A read in a repeat.** Read $x_1$ maps uniquely on the forward strand at 1000. Read $x_2$, of length 100, matches equally well on the reverse strand at 1251 and at 50001. The first placement gives $t = 1251 + 100 - 1000 = 351$, and the second gives $t = 49101$, where $f$ is practically 0. So the pair goes to 1251, and $x_2$ gets a high mapping quality, although on its own its MAPQ would be 3 at best, the value of a two-way tie.

**Mate rescue.** Read $x_2$ has eight mismatches spaced evenly over its 100 bases, so no exact match of 19 or more bases survives (19 is the default smallest seed of BWA-MEM), and the seed search finds nothing. Its mate maps at 1000 on the forward strand. The rescue step aligns the reverse complement of $x_2$ to the reference window from 1080 to 1419, the window of the rule above with $\mu = 300$ and $\sigma = 30$, and finds the alignment at 1251 with eight mismatches.

## Known algorithms

| mapper | single-read search | pairing |
|---|---|---|
| Maq | hashing of spaced seeds | pairs the hits within a maximal distance and gives a pair mapping quality |
| [BWA](/bwa/) (BWA-backtrack, `sampe`) | FM-index backtracking for each read | estimates the insert size from the data, pairs the hits, and rescues an unmapped mate by Smith-Waterman alignment in the window |
| BWA-MEM | maximal exact matches, chaining, extension | pair score with an insert size penalty; rescue near the mate |
| [Bowtie](/bowtie/) 2 | FM-index seeds and dynamic programming | concordant pairs inside `-I` and `-X`, with search near the mate |
| [minimap2](/minimap2/) (short-read mode) | [minimizer](/minimizer/) seeds and chaining | pairs the chains of the two reads |

All of these are heuristics: they look at a limited set of candidate places for each read, so they can miss the best pair.

## Bounds

- **Exact solution in polynomial time.** With the semi-global alignment scores of each read at each position of $R$ on both strands, computed in $O(G L)$ time per read, the best FR pair is the maximum over $u_1$ of $s_1(u_1)$ plus the best $s_2(u_2) + \lambda \log f(u_2 + L - u_1)$ over the $u_2$ in the window allowed by $f$. With a window of width $w$, this costs $O(G w)$, so the exact problem is polynomial but far too slow for genomes and $10^8$ pairs.
- **Cost of mate rescue.** One rescue is an alignment of $L$ bases against $O(\sigma + L)$ bases, which is $O(L (\sigma + L))$ time, independent of $G$.
- **Ambiguity.** If both reads fall in a repeat longer than the insert, every copy gives the same pair score, and no method can tell them apart. Longer inserts make this rarer, which is one use of mate pair libraries.

## Reductions

- **To two read mapping instances and a join.** Map each read on its own, keeping several candidate places, then join the two lists under the orientation and distance constraint. With the lists sorted by position, the join is a merge in time linear in their lengths plus the number of joined pairs.
- **Mate rescue to local alignment.** One rescue is a [local](/smith-waterman/) or [semi-global](/semi-global-alignment/) alignment in a window.
- **From structural variant detection.** Pairs that cannot be placed in the expected orientation and distance are the input of the [discordant read pair method](/discordant-read-pair-method/).

## Applications

- **Variant calling in repeats.** Pairing gives many reads in repeats a usable mapping quality, so [variant calling](/variant-calling-problem/) works in more of the genome.
- **Structural variants.** A pair whose distance or orientation does not fit $f$ points to a deletion, an insertion, an inversion or a translocation; see [structural variant detection](/structural-variant-detection/).
- **Duplicate marking.** [Duplicate marking](/duplicate-read-marking/) uses the 5' ends of both reads of a pair, which is more specific than one end.
- **Library checks.** The insert size distribution that the mapper estimates is itself a quality check of the library.

## References
