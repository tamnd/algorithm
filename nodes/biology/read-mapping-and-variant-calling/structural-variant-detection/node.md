---
tag: 0Y4ED5
kind: problem
slug: structural-variant-detection
name: Structural variant detection
aliases:
- SV calling
area: biology/read-mapping-and-variant-calling
level: core
summary: Find deletions, insertions, inversions, duplications and translocations of 50 bases or more from reads aligned to a reference.
prereqs: [variant-calling-problem, paired-end-read-mapping, sequencing-coverage]
see_also: [discordant-read-pair-method, split-read-method, read-depth-copy-number-analysis, copy-number-segmentation, variation-graph, genome-repeat, variant-call-format, somatic-variant-calling]
sources:
  - paper: doi:10.1038/nrg2958
    title: Can Alkan, Bradley P. Coe and Evan E. Eichler, Genome structural variation discovery and genotyping, Nature Reviews Genetics 12(5), 2011
    locator: the sections on the classes of structural variants, the four signals of sequencing data (read pairs, read depth, split reads and assembly) and the figure of the signature of each class
  - paper: doi:10.1101/gr.092981.109
    title: Seungtai Yoon, Zhenyu Xuan, Vladimir Makarov, Kenny Ye and Jonathan Sebat, Sensitive and accurate detection of copy number variants using read depth of coverage, Genome Research 19(9), 2009
    locator: pp. 1586 to 1592 (the read depth signal for deletions and duplications)
  - paper: doi:10.1126/science.1149504
    title: Jan O. Korbel, Alexander Eckehart Urban, Jason P. Affourtit and others, Paired-end mapping reveals extensive structural variation in the human genome, Science 318(5849), 2007
    locator: the description of the read-pair signal and of the classes of events found in two human genomes
  - paper: doi:10.1093/bioinformatics/btp394
    title: Kai Ye, Marcel H. Schulz, Quan Long, Rolf Apweiler and Zemin Ning, Pindel, a pattern growth approach to detect break points of large deletions and medium sized insertions from paired-end short reads, Bioinformatics 25(21), 2009
    locator: the description of the split-read signal and its base-level breakpoints
---

Structural variant detection finds the large changes in a genome: deletions, insertions, inversions, duplications and translocations, usually of 50 bases or more. They are too large for a normal read alignment to show as a mismatch or a short gap, so a caller looks for the indirect traces they leave in the mapped reads. The four main traces are pairs that map at the wrong distance or orientation, reads that map in two parts, changes in the depth of coverage, and contigs assembled from the reads. Each trace sees some classes of events and misses others, so callers combine them.

## In plain words

Think of the reference as a map of a long road, and of the sample as the real road, which has some missing parts, some extra parts and some parts turned around.

You cannot see the whole road, only many short photos of it, taken in pairs a set distance apart. A missing part shows up as photo pairs that look too far apart on the map. A turned part shows a photo that faces the wrong way. A photo that shows two places of the map at once marks the exact edge of a change. And a part of the road that is there twice gets twice as many photos.

## Definition

**Input.** A reference genome and the reads of a sample mapped to it, usually paired reads with a known distribution of the insert size, or long reads.

**Output.** A list of events, each with a type, its breakpoints on the reference (with a confidence interval when they are not exact), its size and, if possible, a genotype. In a [VCF](/variant-call-format/) file, these are records with fields such as SVTYPE, END and SVLEN, or breakend records for joins between two places.

**The classes.**

| class | change in the sample | example of a cause |
|---|---|---|
| deletion | a part of the reference is missing | loss of a gene copy |
| insertion | new sequence between two reference bases | a mobile element |
| inversion | a part of the reference is reversed and complemented | recombination between inverted repeats |
| tandem duplication | a part is present twice, side by side | replication errors |
| interspersed duplication | a copy of a part is somewhere else | retrotransposition |
| translocation | a part of one chromosome is joined to another | common in cancer |

Deletions and duplications change the copy number of the bases and are also called copy number variants. Inversions, translocations and many insertions do not change the copy number of the reference bases, so they are *balanced* with respect to the reference. Events that combine several of these changes are *complex*.

The size of 50 bases is a convention that separates structural variants from the small insertions and deletions of the [variant calling problem](/variant-calling-problem/), not a property of the events.

## Variants

- **Germline calling** of the events that a person inherited, often in many samples together.
- **Somatic calling** of the events in a tumor that the matched normal sample lacks, where the events are often complex and present in only part of the cells; see [somatic variant calling](/somatic-variant-calling/).
- **Copy number only.** Arrays and low-coverage sequencing give only the depth, and the problem becomes the [segmentation of copy number](/copy-number-segmentation/) along the genome.
- **Genotyping of known events.** Given a list of events, decide for each sample whether it carries them, for example by aligning the reads to a [variation graph](/variation-graph/) that contains them.
- **Long reads.** With reads of many thousands of bases, one read often spans a whole event, and the problem is mostly one of [split alignment](/split-read-method/) and of grouping the reads.

## Examples

The examples come from simulations on the pages of the methods.

- **A deletion of 1000 bases seen by read pairs.** With an insert size of $300 \pm 30$ and reads of 50 bases, 18 pairs crossed the deletion and mapped about 1300 bases apart. The [discordant read-pair method](/discordant-read-pair-method/) called it with size 1014 and breakpoint bounds 4997 and 6007 around the true 5000 and 6000. In the same sample, an inversion of 2000 bases gave two groups of pairs with the wrong orientation, and a tandem duplication gave pairs in the wrong order.
- **A deletion of 40 bases seen by split reads.** The same 40 bases are too few to change the span of a pair by much, but reads that crossed the breakpoint mapped in two parts. The [split-read method](/split-read-method/) called it to the base from 14 reads, and an insertion of 7 bases from 8 reads.
- **A gain seen by depth.** A region with three copies in a diploid genome has about 1.5 times the expected number of reads. Windows of read counts, segmented by [CBS](/circular-binary-segmentation/) or an [HMM](/hmm-copy-number-calling/), give its extent but not its exact breakpoints; see [read-depth copy number analysis](/read-depth-copy-number-analysis/).

## Known algorithms

The methods are classed by the signal they use. The table follows the review of Alkan, Coe and Eichler (2011). It is a summary of what each signal can see in principle, not a measurement of any one tool.

| signal | page | sees | misses or does badly |
|---|---|---|---|
| read pairs | [discordant read-pair method](/discordant-read-pair-method/) | deletions, insertions shorter than the insert, inversions, tandem duplications, translocations | exact breakpoints, small events, events in repeats |
| split reads | [split-read method](/split-read-method/) | exact breakpoints of deletions and short insertions, junctions of other types | large insertions with short reads, repeats near the breakpoint |
| read depth | [read-depth copy number analysis](/read-depth-copy-number-analysis/) | deletions and duplications, and their copy number | balanced events, small events, exact breakpoints |
| assembly | local or whole-genome assembly, as in [de Bruijn assembly](/de-bruijn-assembly/) | novel insertions and complex events | events inside long repeats |

Tools such as DELLY combine read pairs and split reads, and many pipelines run several callers and merge their calls, because no signal sees every class. Long reads see most classes with one signal, the split alignment, but at a higher cost per base.

## Bounds

- **The size seen by read pairs.** A deletion changes the span of a pair by its size, so with insert size $\mu \pm \sigma$ and a threshold of $z$ standard deviations, a deletion of less than about $z\sigma$ bases does not make the pairs discordant. With $\sigma = 30$ and $z = 3$, that is 90 bases.
- **Insertions and read pairs.** A pair crosses an insertion of $I$ bases only if its fragment is longer than $I$ plus both reads, so insertions longer than the insert are invisible to pairs.
- **Support.** With $N$ pairs of fragment length $f$ and read length $L$ on a genome of length $G$, about $N (f - 2L)/G$ pairs cross a given breakpoint with both mates outside it. Low coverage means few pairs for each event.
- **Repeats.** An event whose breakpoints lie in repeats longer than the fragments, as in many duplications, cannot be placed by any short-read signal; see [genome repeats](/genome-repeat/).
- **Resolution.** Read pairs and depth give breakpoints only to within about a fragment length or a window. Only split reads and assembly give the exact base.

## Reductions

- **To clustering.** The read-pair method reduces to the [connected components](/connected-components/) of a graph of pairs that agree with each other.
- **To segmentation.** The depth signal reduces to [copy number segmentation](/copy-number-segmentation/) of a sequence of counts.
- **To alignment.** The split-read signal is a split alignment of one read, and genotyping of known events is [sequence-to-graph alignment](/sequence-to-graph-alignment/) on a graph with the events.

## Applications

- **Human genetics.** Many structural variants affect genes, and some cause disease, such as deletions and duplications in developmental disorders.
- **Cancer.** Tumors gain and lose large parts of chromosomes and make fusions of genes by translocations.
- **Population studies.** Catalogs of structural variants in many people, and their genotypes in new samples.
- **Evolution.** Duplications and inversions between species and between populations.

## References
