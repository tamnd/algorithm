---
tag: 398WVT
kind: algorithm
slug: duplicate-read-marking
name: Duplicate read marking
aliases:
- PCR duplicate removal
- duplicate marking
area: biology/read-mapping-and-variant-calling
level: core
summary: Flag reads or pairs that start at the same positions on the same strand as copies of one molecule, and keep the one of best quality.
model: word-ram
complexity:
  vars: {n: the number of templates (pairs and single reads), b: the total number of bases and CIGAR operations}
  time: {worst: O(n log n + b), average: O(n + b), best: Θ(n + b)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2009
  people: [Heng Li]
  note: The SAMtools paper of 2009 had a command, rmdup, that removed reads with the same outer positions. Picard MarkDuplicates, from the Broad Institute, marks them instead and became the standard step of GATK pipelines.
prereqs: [sam-alignment-format, paired-end-read-mapping, hash-table]
see_also: [umi-deduplication, read-pileup, sequencing-coverage, paired-end-reads, base-quality-score-recalibration, variant-calling-problem, lander-waterman-model, radix-sort]
sources:
  - url: https://github.com/broadinstitute/picard/blob/master/src/main/java/picard/sam/markduplicates/MarkDuplicates.java
    title: Picard MarkDuplicates, source and documentation in the class comment, master branch of the broadinstitute/picard repository
    locator: the class documentation (5' positions of both reads, ranking by the sum of base qualities, the 0x400 flag, optical duplicates, REMOVE_DUPLICATES) and the pass that marks pairs and then fragments
  - url: https://github.com/samtools/htsjdk/blob/master/src/main/java/htsjdk/samtools/DuplicateScoringStrategy.java
    title: htsjdk DuplicateScoringStrategy, master branch of the samtools/htsjdk repository
    locator: the method that sums the base qualities of at least 15 and caps the sum, and the list of scoring strategies
  - paper: doi:10.1093/bioinformatics/btp352
    title: Heng Li, Bob Handsaker, Alec Wysoker, Tim Fennell, Jue Ruan, Nils Homer, Gabor Marth, Goncalo Abecasis, Richard Durbin and 1000 Genome Project Data Processing Subgroup, The Sequence Alignment/Map format and SAMtools, Bioinformatics 25(16), 2009
    locator: pp. 2078 to 2079 (the SAMtools commands, among them the removal of potential PCR duplicates)
  - paper: doi:10.1038/ng.806
    title: Mark A. DePristo, Eric Banks, Ryan Poplin and others, A framework for variation discovery and genotyping using next-generation DNA sequencing data, Nature Genetics 43(5), 2011
    locator: pp. 491 to 498 (duplicate marking as a step of the data processing before variant discovery)
  - url: https://samtools.github.io/hts-specs/SAMv1.pdf
    title: The SAM/BAM Format Specification, version 1.6, hts-specs
    locator: Section 1.4, FLAG bit 0x400 (PCR or optical duplicate)
---

Duplicate read marking finds reads that are copies of one original DNA fragment and flags all but one of them. Copies come from the PCR amplification of the library, and from the sequencer, when one cluster on the flow cell is read as two (optical duplicates). Copies are not independent evidence: an error made in an early PCR cycle shows up in every copy, so a caller that counts them as separate reads can call a false variant. The standard method, that of Picard MarkDuplicates, calls two read pairs duplicates when both of their unclipped 5' ends lie at the same positions on the same strands, keeps the pair with the highest sum of base qualities, and sets the SAM flag 0x400 on the others. It marks the reads and does not remove them, unless the user asks for that.

## In plain words

Before sequencing, the DNA pieces are copied many times. If two reads start and end at exactly the same places, they are most likely copies of one piece, because two different pieces rarely break at the same two places. Copies are a problem: if the first copy had a mistake, all copies have it, and the mistake looks like it was seen many times.

So group the reads by where they start and end and on which strand. In each group, keep the read with the best quality and put a mark on the others. Later tools skip the marked reads. Reads that come alone, without a partner, are grouped by their start only. A lone read that starts where a pair starts is marked, because the pair tells more.

## The problem

Positions are 1-based, as in [SAM](/sam-alignment-format/). The input is a list of templates. A template is a pair, with both reads mapped, or a fragment, a single-end read or a read whose mate did not map. Each read has a library, a chromosome, a position, a CIGAR string, a strand and base qualities.

The **unclipped 5' end** of a read is the reference position where its first sequenced base would lie if the clipped bases were aligned: for a forward read, POS minus the length of the leading soft and hard clips; for a reverse read, POS plus the reference span minus 1, plus the length of the trailing clips. The **end key** of a read is (library, chromosome, unclipped 5' end, strand). The **score** of a read is the sum of its base qualities that are at least 15, capped at 16383, and the score of a template is the sum over its reads.

**Output.** The set of templates to mark:

- a pair is marked if another pair has the same two end keys and a higher score;
- a fragment is marked if a pair has an end at its end key, or if another fragment has the same end key and a higher score.

Ties in the score go to the template that comes first in the input.

## The algorithm

```pseudo id=main
MARK-DUPLICATES(T_1, ..., T_n)
L1  P ← empty map; F ← empty map; E ← empty set
L2  for i ← 1 to n do
L3      if T_i is a pair (r, r') then append i to P[sorted(key(r), key(r'))]; add key(r) and key(r') to E
L4      else append i to F[key(r)] for the read r of T_i
L5  D ← empty set
L6  for each list S in P do add to D every index of S except the one of largest (score, -index)
L7  for each key k with list S in F do
L8      if k ∈ E then add every index of S to D
L9      else add to D every index of S except the one of largest (score, -index)
L10 return D
```

Line L3 sorts the two end keys, so that the order of the mates in the input does not matter. The set $E$ collects every end of every pair, which line L8 needs to mark the fragments that sit on a pair end. Lines L6 and L9 keep the one template of largest rank $(\text{score}, -i)$, which is unique because no two templates have the same index.

## Example

Eight templates, all on chromosome 1 and in library L1 unless said otherwise, with reads of 10 bases.

| template | reads (POS, CIGAR, strand, qualities) | end keys | score |
|---|---|---|---|
| a | (100, 10M, +, ten Q30), (290, 10M, -, ten Q30) | 100+, 299- | 600 |
| b | (102, 2S8M, +, nine Q30 and one Q10), (290, 10M, -, ten Q30) | 100+, 299- | 570 |
| c | (100, 10M, +, ten Q30), (291, 10M, -, ten Q30) | 100+, 300- | 600 |
| d | (100, 10M, +, ten Q30) | 100+ | 300 |
| e | (500, 10M, +, ten Q20) | 500+ | 200 |
| f | (500, 10M, +, ten Q40) | 500+ | 400 |
| g | (500, 10M, -, ten Q40) | 509- | 400 |
| h | (100, 10M, +, ten Q30), library L2 | 100+ in L2 | 300 |

The first read of b starts at 102 after 2 soft-clipped bases, so its unclipped 5' end is 100, the same as that of a. The reverse reads at 290 with 10M end at 299, which is their 5' end. The Q10 base of b does not count in its score.

- Line L6 groups a and b, which have the ends 100+ and 299-, and marks b, the one of lower score. Pair c differs in one end, 300- instead of 299-, so it is alone and kept.
- Line L8 marks fragment d, because 100+ is an end of pairs a and c.
- Line L9 groups e and f at 500+ and marks e. Fragment g is on the other strand, with the 5' end 509-, and h is in another library, so both are kept.

The marked set is $\{b, d, e\}$.

## Correctness

Line L3 sends two pairs to the same list exactly when they have the same multiset of two end keys, because two multisets of two elements are equal exactly when their sorted tuples are. Line L4 sends two fragments to the same list exactly when they have the same end key, and $E$ ends up as the set of all pair ends. In each list, lines L6 and L9 keep only the template of largest rank, so a template is marked exactly when another template of its list ranks higher, which is the rule for pairs and for fragments that sit on no pair end. Line L8 marks every fragment on a pair end. The proof also shows that the unclipped 5' end computed from POS and the CIGAR string is the one of the definition. The full proof is in proofs/correctness.md.

## Complexity

- **Time.** Computing the end keys and the scores reads every base quality and every CIGAR operation once, which is $\Theta(b)$. With hash maps, lines L2 to L4 take $O(n)$ expected time and lines L5 to L9 touch each template a constant number of times, so the total is $O(n + b)$ expected. Picard sorts the read ends instead, in $O(n \log n)$ comparisons, which also works when the ends do not fit in memory, by sorting on disk.
- **Space.** $\Theta(n)$ for the keys and the lists. A version that streams a coordinate-sorted file needs to keep only the templates whose first end is at the current position and the mates still to come, which is much less than $n$ in practice.
- **Chance duplicates.** For $N$ single-end reads on a genome of length $G$, a read shares its 5' end and strand with at least one other read by chance with probability about $1 - e^{-N/(2G)}$. At 30x coverage with reads of 100 bases, $N/G = 0.3$ and the probability is 13.9%, so single-end marking at high depth also marks many reads that are not copies. For pairs with an insert size of standard deviation 30, at the same depth, the chance that both ends match is about 0.07%.

## Properties

- **Exact for its rule.** It returns exactly the set of the rule above. The rule is a model of what a copy looks like; it is not certain that two marked reads are copies or that two kept reads are not.
- **Deterministic.** The tie rule makes the output a function of the input order. Picard has its own tie rule, so in a tie it can keep another template of the group, but it marks the same number.
- **Independent of the mate order.** Swapping the two reads of a pair does not change the result.
- **Marking, not removing.** The output is a set of flags. Callers and coverage tools skip reads with flag 0x400 by default, and the reads stay in the file for other uses.

## Variants and improvements

- **Optical duplicates.** Picard also looks at the tile and the x and y coordinates of the cluster, which it reads from the read names. Duplicates in one group whose clusters lie within a set pixel distance of each other are counted as optical, and the count goes into the metrics file. The default distance is 100; the documentation suggests 2500 for patterned flow cells. The code of this page leaves optical duplicates out.
- **Read groups and libraries.** Duplicates are only looked for within a library, because two libraries come from separate PCR reactions.
- **Other scores.** Besides the sum of base qualities, htsjdk has a strategy by the total mapped reference length and a random one.
- **Unique molecular identifiers.** If each fragment carries a random barcode before PCR, reads with the same positions but different barcodes come from different fragments. [UMI deduplication](/umi-deduplication/) groups by position and barcode, and allows for errors in the barcode.
- **samtools markdup.** A second widely used tool, which works on a coordinate-sorted file after `samtools fixmate` has added the mate information to each record.
- **Library size estimate.** From the number of duplicates, Picard estimates how many distinct fragments the library holds, with a model in the spirit of the [Lander-Waterman](/lander-waterman-model/) model.

## When to use it

Use it on whole-genome and exome data before [base quality score recalibration](/base-quality-score-recalibration/) and [variant calling](/variant-calling-problem/), as in the GATK pipeline of DePristo et al. (2011). Skip it, or use UMIs, for amplicon sequencing, where all reads of one target start at the same primer and are duplicates by the rule without being PCR copies of one fragment. For PCR-free libraries the rule still finds optical duplicates. For RNA sequencing of highly expressed genes, reads pile up by chance, so many marked reads are not copies; count them with care.

## Pitfalls

- **Removing instead of marking.** The alias "PCR duplicate removal" describes an older practice. The method marks reads, both PCR and optical copies, and the user may remove them.
- **Clipped reads.** Grouping by POS instead of the unclipped 5' end misses copies where one read has a soft clip that the other lacks, as with template b of the example.
- **Reverse strand.** The 5' end of a reverse read is its rightmost base, not POS. Using POS for both strands groups the wrong reads.
- **Single-end data at high depth.** At high coverage many independent reads share a 5' end by chance, as computed above. Marking them lowers the depth and the power to call variants, with no gain.
- **Secondary and supplementary records.** They carry the duplicate flag of their primary record; they must not be scored as templates of their own.
- **Multiple libraries in one read group.** If the library field is wrong, reads from separate libraries are compared, and real distinct fragments are marked.

## Implementations

## History

Duplicate reads were known from the first short-read projects. The SAMtools paper of Li et al. (2009) listed a command, `rmdup`, that removed potential PCR duplicates with the same outer coordinates. Picard MarkDuplicates, from the Broad Institute, marks instead of removing, scores reads by the sum of their base qualities and counts optical duplicates. It is the duplicate step of the GATK pipeline of DePristo et al. (2011).

## References
