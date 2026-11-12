---
tag: 6R1Y3F
kind: problem
slug: read-mapping
name: Read mapping
aliases:
- short-read alignment
- sequence read alignment
- read alignment
area: biology/sequence-alignment
level: core
summary: Find where each sequencing read comes from in a reference genome, allowing for a few errors and both strands. Practical mappers index the genome and are heuristics.
prereqs: [approximate-string-matching, edit-distance]
see_also: [semi-global-alignment, seed-and-extend, kmer-index, fm-index, bowtie, bwa, minimap2, paired-end-reads]
sources:
  - paper: doi:10.1101/gr.078212.108
    title: Heng Li, Jue Ruan and Richard Durbin, Mapping short DNA sequencing reads and calling variants using mapping quality scores, Genome Research 18(11), 2008
    locator: pages 1851 to 1858, the definition of mapping quality and the hash-based search with spaced seeds (Maq)
  - paper: doi:10.1186/gb-2009-10-3-r25
    title: Ben Langmead, Cole Trapnell, Mihai Pop and Steven L. Salzberg, Ultrafast and memory-efficient alignment of short DNA sequences to the human genome, Genome Biology 10(3), 2009
    locator: article R25, Background and Results (the read mapping task, the FM-index search and its limits)
  - paper: doi:10.1093/bioinformatics/btp324
    title: Heng Li and Richard Durbin, Fast and accurate short read alignment with Burrows-Wheeler transform, Bioinformatics 25(14), 2009
    locator: pages 1754 to 1760, Sections 2.4 and 2.5 (exact and inexact matching with the FM-index)
  - paper: doi:10.1093/bioinformatics/bty191
    title: Heng Li, Minimap2, pairwise alignment for nucleotide sequences, Bioinformatics 34(18), 2018
    locator: pages 3094 to 3100, Section 2 (minimizer seeds, chaining and mapping quality for long and short reads)
  - paper: doi:10.1145/1007352.1007374
    title: Richard Cole, Lee-Ad Gottlieb and Moshe Lewenstein, Dictionary matching and indexing with errors and don't cares, Proceedings of the 36th ACM Symposium on Theory of Computing (STOC), 2004
    locator: pages 91 to 100, the k-errata tree (a text index for queries with up to k mismatches)
  - book: isbn:9781107078536
    title: Veli Mäkinen, Djamal Belazzougui, Fabio Cunial and Alexandru I. Tomescu, Genome-Scale Algorithm Design
    locator: Chapter 10, Read alignment (pattern partitioning, backtracking on the BWT and paired-end mapping)
---

Read mapping is the problem of finding, for each short DNA string from a sequencing machine (a *read*), the place in a known reference genome that it most likely comes from. The read is a noisy copy of a piece of one strand of the genome, so the match must allow a few substitutions and small gaps, and the read may come from the reverse complement strand. Formally, each read is an instance of [approximate string matching](/approximate-string-matching/) against the genome, but the scale (a genome of $3 \times 10^9$ bases and hundreds of millions of reads) rules out a scan of the genome per read. All practical mappers build an index of the genome once, and nearly all of them are heuristics: they can miss the best place or report a wrong one, and they attach a *mapping quality* to each answer.

## In plain words

A sequencing machine cannot read a whole genome in one piece. It breaks many copies of the DNA into small fragments and reads a short stretch of each one, a few hundred letters at most for the common machines. Each stretch is a read. If we already have the genome of the same species, we can find where each read comes from by searching for it in that genome.

The search is hard for three reasons. The read has errors from the machine and real differences from the reference, so an exact search is not enough. The read can come from either strand of the DNA, so we must also search for its reverse complement. And genomes repeat themselves, so a read can fit equally well in many places. A mapper finds the best place, says how sure it is, and does this fast enough for a billion reads.

## Definition

**Input.**

- A reference $R$ of length $N$ over $\{A, C, G, T\}$, the chromosomes joined into one string. Letters that are not known are written N and match nothing.
- A set of reads. Each read $P$ has length $m$, typically 50 to 300 for short reads and thousands to tens of thousands for long reads, with higher error rates for the long ones.
- An error model: a bound $k$ on the number of mismatches ([Hamming distance](/k-mismatch-problem/)), or on the number of differences ([edit distance](/edit-distance/)), or a scoring scheme with match, mismatch and gap scores, usually [affine gaps](/affine-gap-alignment/).

**Output.** For each read, a *mapping*: a position $p$ in $R$, a strand, and an alignment of the whole read $P$ (or of its reverse complement $\overline{P}$) to a substring of $R$ that starts at $p$. The read is aligned end to end and the reference is not, so the alignment is [semi-global](/semi-global-alignment/). Most mappers also allow *soft clipping*, which leaves the ends of the read unaligned, and then the alignment is close to a [local alignment](/local-alignment/).

**Two versions of the question.**

- *All mappings.* Report every $(p, \text{strand})$ where the read matches within $k$ mismatches or $k$ differences. This is a well-defined combinatorial problem.
- *Best mapping.* Report the place of the best score, and break ties at random. This is what most users want, because a read comes from one place.

**Mapping quality.** Li, Ruan and Durbin (2008) defined the mapping quality of a reported place as $Q = -10 \log_{10} \Pr[\text{the place is wrong}]$, estimated from the scores of the best and of the second best place. A read that fits two places equally well gets a quality near 0. Downstream tools use this number to discount reads from repeats.

## Variants

- **Exact mapping.** Find all exact occurrences of $P$ and $\overline{P}$. With an [FM-index](/fm-index/), backward search counts them in $O(m)$ steps, independent of $N$.
- **k-mismatch and k-difference mapping.** Report all places within Hamming distance or edit distance $k$, usually with $k \le 3$ for short reads. This is the [k-mismatch problem](/k-mismatch-problem/) and the [k-differences problem](/k-differences-problem/) with an indexed text and many patterns.
- **Scored mapping.** Maximize an alignment score with affine gaps. This is the version of [BWA](/bwa/)-MEM, Bowtie 2 and [minimap2](/minimap2/).
- **Paired-end mapping.** Two reads come from the two ends of one fragment of roughly known length, on opposite strands. A pair of places that fits these constraints is preferred, which can rescue a read that falls in a repeat. See [paired-end reads](/paired-end-reads/).
- **Spliced mapping.** Reads from RNA can span introns, so the alignment may contain long gaps that follow splice signals.
- **Long-read mapping.** Reads of thousands of bases with many insertions and deletions are mapped by chaining seeds and aligning between them. See [seed chaining](/seed-chaining/).
- **Mapping to a graph.** When the reference is a variation graph, the read is aligned to a path in the graph. See [sequence-to-graph alignment](/sequence-to-graph-alignment/).

## Examples

Let $R = \texttt{ACGTTGCATGTCGCATGATGCATGAGAGCTACGTTGCATGTCGCAT}$, with $N = 46$, and allow up to 2 mismatches on either strand. Positions start at 0.

| read | best place | strand | mismatches | other places within 2 mismatches |
|---|---|---|---|---|
| GCATGAGAGC | 19 | + | 0 | none |
| GCATGAGTGC | 19 | + | 1 | none |
| ACGTAGCTCT | 24 | − | 0 | none |
| TTGCATGTCG | 3 and 33 | + | 0 | tie |

The second read differs from $R[19 \ldots 28]$ in one letter, a machine error or a real variant; a mapper reports the mismatch, and a variant caller later counts how many reads show the same letter there. The third read occurs nowhere on the forward strand, but its reverse complement AGAGCTACGT is $R[24 \ldots 33]$. The fourth read lies in the repeat $R[0 \ldots 15] = R[30 \ldots 45]$, so two places are equally good. A mapper reports one of them and gives it a mapping quality near 0; no method can do better from this read alone.

## Known algorithms

| approach | idea | exact for the stated model? | examples |
|---|---|---|---|
| online scan | dynamic programming over $R$ for each read | yes | [Sellers](/sellers-algorithm/), [Myers bit-parallel](/myers-bit-parallel-algorithm/) |
| pattern partitioning | split the read into $k + 1$ pieces; one must match exactly | yes, as a filter, if all hits are checked | [pigeonhole filtering](/pigeonhole-filtering/) |
| hash index of the reads or the genome | look up k-mers or spaced seeds, then check candidates | depends on the seed set | Maq, SSAHA, [BLAT](/blat/) |
| FM-index with backtracking | search the read letter by letter from its end, and branch on substitutions | yes if the search is not cut off; tools cut it off | [Bowtie](/bowtie/), [BWA](/bwa/) (BWA-backtrack) |
| variable-length seeds | find the [maximal exact matches](/maximal-exact-match/) of the read, chain and extend them | no, heuristic | BWA-MEM |
| sampled seeds and chaining | look up [minimizers](/minimizer/), [chain](/seed-chaining/) the hits, align the gaps | no, heuristic | [minimap2](/minimap2/) |

The online scan costs $O(Nm)$ time per read, or $O(N \lceil m/w \rceil)$ with words of $w$ bits, which is about $3 \times 10^9$ steps per read for a human genome: far too slow for $10^8$ reads. The index-based methods do the work of the genome once, and then spend time that depends on $m$ and on the number of candidate places, not on $N$.

## Bounds

- **Lower bound.** Each read must be read, and each reported place must be written, so a query takes $\Omega(m + \mathit{occ})$ time. For exact mapping an FM-index of $R$ comes close: it counts the occurrences in $O(m)$ steps for a constant alphabet, and the time to list each one depends on how densely the suffix array is sampled. The BWT of a DNA genome takes $2N$ bits, plus the rank tables and the samples.
- **Mismatches.** The number of strings at Hamming distance at most $k$ from a read is $\sum_{i \le k} \binom{m}{i} 3^i$, so a search that tries each of them, as plain backtracking does in the worst case, costs $\Theta(m^k)$ steps for fixed $k$. Cole, Gottlieb and Lewenstein (2004) gave an index, the k-errata tree, that answers a k-mismatch query in about $m + (c \log N)^k / k! + \mathit{occ}$ time with an index of size about $N (c \log N)^k / k!$, for a constant $c$. Mappers use simpler indexes and pruning instead.
- **Ambiguity.** Some reads cannot be placed by any method: when $P$ occurs in two places of $R$ with the same score, the data does not tell them apart. The fraction of such reads depends on the read length and on the repeats of the genome, not on the algorithm.

## Reductions

- **To approximate string matching.** Mapping one read with up to $k$ differences, on one strand, is exactly approximate string matching with pattern $P$ and text $R$. Both strands are two instances, with $P$ and $\overline{P}$.
- **To exact matching.** If $P$ matches within $k$ mismatches or differences, then one of $k + 1$ disjoint pieces of $P$ occurs exactly. This reduces mapping to exact searches in an index followed by verification, the basis of [seed-and-extend](/seed-and-extend/) with guaranteed sensitivity.
- **Paired-end mapping.** It reduces to mapping each read and then joining the two lists of places under a distance constraint.
- **Graph mapping.** If the reference is a single path, [sequence-to-graph alignment](/sequence-to-graph-alignment/) is read mapping with semi-global alignment.

## Applications

- **Resequencing and variant calling.** Reads from an individual are mapped to the reference, and the columns of the stacked alignments show the single-letter variants and small insertions and deletions of that individual.
- **Counting.** In RNA sequencing and ChIP sequencing, the number of reads mapped to a gene or region measures its activity.
- **Assembly with a reference.** Mapped reads give the order of the new genome in [reference-guided assembly](/reference-guided-assembly/).
- **Structural variants.** Reads and pairs that map in pieces, or with an unexpected distance or orientation, point to large deletions, inversions and translocations.

## References
