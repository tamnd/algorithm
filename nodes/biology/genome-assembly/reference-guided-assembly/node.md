---
tag: RRNQF2
kind: problem
slug: reference-guided-assembly
name: Reference-guided assembly
aliases:
- reference-based assembly
area: biology/genome-assembly
level: core
summary: "Reconstruct a genome from reads with the help of the genome of a related individual or species, by mapping the reads to it or by ordering de novo contigs along it."
prereqs: [read-mapping, contig, genome-assembly-problem]
see_also: [scaffolding, consensus-sequence-calling, colinear-chaining, minimap2, bwa, gap-filling, assembly-quality-assessment, hybrid-assembly]
sources:
  - paper: doi:10.1093/bib/5.3.237
    title: Mihai Pop, Adam Phillippy, Arthur L. Delcher and Steven L. Salzberg, Comparative genome assembly, Briefings in Bioinformatics 5(3), 2004
    locator: pp. 237 to 248, assembly of reads aligned to the genome of a related organism (AMOScmp) and the problems of divergence and rearrangements
  - paper: doi:10.1186/s12859-017-1911-6
    title: Heidi E. L. Lischer and Kentaro K. Shimizu, Reference-guided de novo assembly approach improves genome reconstruction for related species, BMC Bioinformatics 18, 2017
    locator: article 474, a pipeline that maps reads to a related reference, assembles them per region de novo, and merges the results
  - paper: doi:10.1186/s13059-022-02823-7
    title: Michael Alonge, Ludivine Lebeigle, Melanie Kirsche, Katie Jenike, Shujun Ou, Sergey Aganezov, Xingang Wang, Zachary B. Lippman, Michael C. Schatz and Sergey Soyk, Automated assembly scaffolding using RagTag elevates a new tomato system for high-throughput genome editing, Genome Biology 23, 2022
    locator: article 258, ordering and orienting contigs by their alignments to a reference, and correcting contigs at alignment conflicts
  - paper: doi:10.1093/bioinformatics/bty191
    title: Heng Li, Minimap2, pairwise alignment for nucleotide sequences, Bioinformatics 34(18), 2018
    locator: pp. 3094 to 3100, alignment of reads and of contigs to a reference genome
---

Reference-guided assembly is the problem of reconstructing the genome of a sample from its sequencing reads with the help of the known genome of a related individual or species. In one form the reads are mapped to the reference and the differences are applied to it; in the other form the reads are assembled de novo and the reference is used only to order, orient and check the contigs. Both forms are cheaper and give longer sequences than assembly without a reference, but they can only find what the reference lets them see. Most of a reference-guided method is a workflow of standard tools; the algorithmic parts are read mapping, consensus calling, the alignment of contigs, and ordering along the reference.

## In plain words

You have the pieces of a torn book and a complete copy of an older edition. Instead of fitting the pieces to each other, you can put each piece next to the place where it matches the old edition, and then copy the old edition with the changes that your pieces show. This is fast and gives a complete text.

The danger is that you see only the changes that are small. A new chapter that the old edition does not have finds no place, and a moved chapter is put where it was in the old edition. A safer way is to fit the pieces to each other first, and use the old edition only to put the long rebuilt passages in order.

## Definition

**Model.** The sample genome $X$ has length $G$ and is sequenced by $N$ reads of length about $L$, with coverage $c = NL/G$ and a per-base error rate $p$. The reference $R$ is a genome that differs from $X$ by substitutions, small indels, and structural changes: large insertions, deletions, inversions, duplications and moves. Let $d$ be the fraction of positions where $X$ and $R$ differ by a substitution. The graph, where there is one, is the assembly graph of the de novo step.

**Mapping-based form.** Input: reads and $R$. Output: a sequence $X'$ obtained from $R$ by applying the differences that the reads support, and the positions of $R$ where the reads give no support. Algorithmic core: [read mapping](/read-mapping/) of each read to $R$, then [consensus calling](/consensus-sequence-calling/) at each position of $R$.

**Contig-ordering form.** Input: contigs or scaffolds from a de novo assembly, and $R$. Output: an order and orientation of the contigs, with gap lengths, such that the order agrees with the positions of their alignments to $R$; optionally, contigs are cut where their alignment changes place abruptly. Algorithmic core: alignment of each contig to $R$ with seeds and [colinear chaining](/colinear-chaining/), then sorting by reference position.

**Hybrid form.** Map the reads to $R$ to sort them into regions, assemble each region de novo, and merge the results; reads that do not map are assembled separately. This is the approach of Lischer and Shimizu (2017).

## Variants

- **Resequencing.** If $X$ and $R$ are from the same species, mapping with small-variant calling gives most of the useful information. The output is often a list of variants instead of a sequence.
- **Comparative assembly.** For a related species, Pop et al. (2004) align the reads to the reference and assemble them in the order of their alignments, which allows larger differences than variant calling.
- **Reference-guided scaffolding.** Tools such as RagTag order and orient de novo contigs along a reference, which is the [scaffolding](/scaffolding/) problem with reference positions in place of read pairs. The gaps between contigs are filled with unknown bases, or later by [gap filling](/gap-filling/).
- **Reference-guided correction.** Cut a contig where one part aligns to a distant place in the reference, on the assumption that the join is a misassembly. This is a heuristic: a true rearrangement of the sample is also cut.

## Examples

**Ordering contigs.** Three de novo contigs align to a reference of 1500 kb as follows:

| contig | reference interval | strand |
|---|---|---|
| $a$ | 500 to 900 kb | + |
| $b$ | 0 to 400 kb | − |
| $c$ | 1000 to 1500 kb | + |

Sorting by the start of the alignment gives $b, a, c$. Contig $b$ aligns to the reverse strand, so it is reverse-complemented. The gaps between the alignments are 100 kb each, so the scaffold is $\bar{b}$, 100 kb of unknown bases, $a$, 100 kb of unknown bases, $c$. If the reference has an inversion that the sample does not have, contig $b$ is turned the wrong way, and nothing in this computation shows it.

**How divergence breaks the seeds.** A mapper finds a read through exact seeds of length $k$. Under substitutions at rate $d$, a fixed seed of length 19 is free of differences with probability $(1 - d)^{19}$, and a read of 150 bases has 132 such seeds:

| $d$ | $(1 - d)^{19}$ | expected exact 19-mers per read |
|---|---|---|
| 0.001 | 0.981 | 129.5 |
| 0.01 | 0.826 | 109.1 |
| 0.05 | 0.377 | 49.8 |
| 0.10 | 0.135 | 17.8 |

In the worst case, $e$ differences split the read into $e + 1$ pieces of total length $150 - e$, so a read with at most 6 differences always has an exact 19-mer, because $7 \cdot 19 + 6 \le 150$. With more differences a read can have none, and the method then loses it.

## Known algorithms

- **Read mapping.** Seed-and-extend mappers with an [FM-index](/fm-index/) or a hash table of [minimizers](/minimizer/), such as [BWA](/bwa/) and [minimap2](/minimap2/). They are heuristics: a read is mapped in close to linear time in its length, observed, but some reads are missed or placed in the wrong copy of a repeat.
- **Consensus or variant calling.** Column votes or likelihood models on the pileup of mapped reads, at $O(n)$ time for $n$ mapped bases given the alignments.
- **Contig alignment.** Seeds, colinear chaining in $O(h \log h)$ time for $h$ seed hits, and alignment of the gaps between the seeds, as in minimap2.
- **Ordering and orientation.** Sort the contigs by the position of their main alignment and take the strand from the alignment, in $O(m \log m)$ time for $m$ contigs. RagTag also scores the alignments of each contig to choose one reference place and to decide whether to cut a contig.

## Bounds

- **Sequence absent from the reference.** In the mapping-based form, a part of $X$ that has no similar part in $R$ gets no reads, so the output cannot contain it, whatever the coverage. The hybrid form recovers it only through the separate assembly of the unmapped reads.
- **Structural changes.** An inversion, a move or a large insertion longer than the reads changes the order of the genome without changing the reads near it much. Mapping-based assembly then copies the order of $R$. Contig ordering copies it too, unless a contig spans the breakpoint.
- **Reference bias.** Reads with more differences from $R$ map less often, as the table shows, so regions of high divergence get lower coverage and their differences are under-called.
- **Repeats.** A read from a repeat that is longer than the read maps to several places equally well, as in de novo assembly; the reference does not remove this ambiguity.

## Reductions

- **To mapping and consensus.** The mapping-based form is [read mapping](/read-mapping/) followed by [consensus calling](/consensus-sequence-calling/) on the reference coordinates.
- **To scaffolding.** The contig-ordering form is [scaffolding](/scaffolding/) in which the links between contigs come from their positions on $R$ in place of paired reads; with one place for each contig, the order is a sort.
- **To chaining.** Placing a contig on $R$ is [colinear chaining](/colinear-chaining/) of its seed hits, followed by alignment between the chained seeds.

## Applications

- Resequencing many individuals of a species with a good reference, as in population studies.
- Assembling strains of bacteria and viruses against a reference strain.
- Ordering and orienting a draft assembly of a new species with the chromosome-level genome of a related species, when no long-range data such as long reads or chromatin contacts are available.
- Checking a de novo assembly: contigs that align in pieces to a close reference show possible misassemblies, and [assembly quality assessment](/assembly-quality-assessment/) uses the same alignments.

## References
