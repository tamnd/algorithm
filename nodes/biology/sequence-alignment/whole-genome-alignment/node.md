---
tag: C31DKC
kind: problem
slug: whole-genome-alignment
name: Whole-genome alignment
aliases:
- genome-scale alignment
- genome-to-genome alignment
area: biology/sequence-alignment
level: advanced
summary: Align two or more complete genomes into blocks of homologous sequence, with rearrangements, duplications and both strands allowed. Practical methods anchor, chain and extend.
prereqs: [colinear-chaining, maximal-exact-match, local-alignment]
see_also: [mummer, seed-chaining, multiple-sequence-alignment, sorting-by-reversals, minimap2, global-alignment, seed-and-extend, edit-distance-hardness]
sources:
  - paper: doi:10.1093/nar/27.11.2369
    title: Arthur L. Delcher, Simon Kasif, Robert D. Fleischmann, Jeremy Peterson, Owen White and Steven L. Salzberg, Alignment of whole genomes, Nucleic Acids Research 27(11), 1999
    locator: pages 2369 to 2376, MUM anchors, the longest increasing subsequence chain and the classes of gaps
  - paper: doi:10.1101/gr.809403
    title: Scott Schwartz, W. James Kent, Arian Smit, Zheng Zhang, Robert Baertsch, Ross C. Hardison, David Haussler and Webb Miller, Human-mouse alignments with BLASTZ, Genome Research 13(1), 2003
    locator: pages 103 to 107, spaced seeds, gapped extension and the interpolation between alignments
  - paper: doi:10.1073/pnas.1932072100
    title: W. James Kent, Robert Baertsch, Angie Hinrichs, Webb Miller and David Haussler, Evolution's cauldron, duplication, deletion, and rearrangement in the mouse and human genomes, Proceedings of the National Academy of Sciences USA 100(20), 2003
    locator: pages 11484 to 11489, the definitions of chains and nets and the chaining algorithm
  - paper: doi:10.1101/gr.2289704
    title: Aaron C. E. Darling, Bob Mau, Frederick R. Blattner and Nicole T. Perna, Mauve, multiple alignment of conserved genomic sequence with rearrangements, Genome Research 14(7), 2004
    locator: pages 1394 to 1403, multi-MUM anchors and locally collinear blocks
  - paper: doi:10.1038/s41586-020-2871-y
    title: Joel Armstrong, Glenn Hickey, Mark Diekhans and colleagues, Progressive Cactus is a multiple-genome aligner for the thousand-genome era, Nature 587, 2020
    locator: pages 246 to 251, reference-free progressive alignment of hundreds of genomes along a guide tree
  - paper: doi:10.1093/bioinformatics/bty191
    title: Heng Li, Minimap2, pairwise alignment for nucleotide sequences, Bioinformatics 34(18), 2018
    locator: pages 3094 to 3100, the presets for aligning assemblies and the chaining with gap costs
  - paper: doi:10.1089/cmb.1994.1.337
    title: Lusheng Wang and Tao Jiang, On the complexity of multiple sequence alignment, Journal of Computational Biology 1(4), 1994
    locator: pages 337 to 348, NP-hardness of multiple alignment under the sum-of-pairs score
---

Whole-genome alignment is the problem of finding all the homologous parts of two or more complete genomes and aligning them base by base. Unlike [global alignment](/global-alignment/) of two genes, it cannot assume that the sequences are in the same order: in evolution, segments of a genome are inverted, moved, duplicated and lost. So the answer is not one alignment but a set of *alignment blocks*, each aligning segments of the genomes, on either strand, that descend from one ancestral segment. The genomes have millions to billions of bases, so methods use exact or near-exact *anchors*, chain them, and align between them; nearly all are heuristics.

## In plain words

Two related species share most of their DNA, but over time pieces of it have been turned around, cut out, copied or moved. To compare the two genomes, we want to know which piece of one matches which piece of the other, and how they line up letter by letter.

So the answer is a set of blocks. Each block says "this stretch of the first genome and that stretch of the second genome come from the same ancestral stretch", together with an alignment of the letters. The order of the blocks along the two genomes shows how the genome was rearranged.

## Definition

**Input.** Genomes $G_1, \ldots, G_k$ over $\{A, C, G, T\}$, each a set of chromosomes, a scoring scheme for alignments, and often a phylogenetic tree.

**Output.** A set of alignment blocks. Each block is a [multiple alignment](/multiple-sequence-alignment/) of segments, where a segment is an interval of one genome on one strand. Usually each position of a genome lies in at most one block, and the blocks should cover as much homologous sequence as possible, with high alignment scores and few blocks.

For two genomes, a common model uses three levels:

- a *local alignment* is a gapped alignment of a segment of $G_1$ with a segment of $G_2$;
- a *chain* is a sequence of local alignments that are in the same order and on the same relative strand in both genomes, scored as the sum of the alignment scores minus gap costs between them;
- a *net* is a hierarchy of chains: the best chains are chosen first, and the gaps they leave in the reference are filled by lower-scoring chains, as with an insertion inside a larger block.

No single score is standard. Each method fixes its own balance between alignment score, number of blocks and rearrangement events. That is why this page lists tools as examples and not as solutions to one exact problem.

## Variants

- **Collinear or with rearrangements.** For two strains of one species, a single collinear chain often covers almost all of both genomes. Between species, the blocks need not be collinear and can be on opposite strands.
- **Pairwise or multiple.** Multiple whole-genome alignment of $k$ genomes, often along a tree, contains [multiple sequence alignment](/multiple-sequence-alignment/) as a special case.
- **Reference-based or reference-free.** A reference-based alignment projects each genome onto one reference; a reference-free alignment treats all genomes the same, and its blocks can contain sequence absent from any one genome.
- **Orthology or all homology.** The alignment may keep only the best match of each position (orthologs), as nets do, or also report duplicated copies (paralogs).
- **Nucleotide or translated.** For distant genomes, matches are found between protein translations, as in the PROmer mode of [MUMmer](/mummer/).

## Examples

Let four segments of a genome be

- $a = \texttt{GATTACA}$, $b = \texttt{CCGGT}$, $c = \texttt{TTGAC}$, $d = \texttt{ACGTA}$,

so $G_1 = a\,b\,c\,d = \texttt{GATTACACCGGTTTGACACGTA}$. Suppose that in $G_2$ the middle part $b\,c$ was inverted. An inversion reverses the order and takes the reverse complement, so $G_2 = a \cdot \overline{c} \cdot \overline{b} \cdot d$ with $\overline{c} = \texttt{GTCAA}$ and $\overline{b} = \texttt{ACCGG}$:

$G_2 = \texttt{GATTACAGTCAAACCGGACGTA}$.

A global alignment of $G_1$ with $G_2$ matches $a$ and $d$, but it must pay for the inverted middle 10 bases with mismatches and gaps. A whole-genome alignment reports three blocks:

| block | segment of $G_1$ | segment of $G_2$ | strand |
|---|---|---|---|
| 1 | $a$, positions 0 to 6 | positions 0 to 6 | same |
| 2 | $b\,c$, positions 7 to 16 | positions 7 to 16 | opposite |
| 3 | $d$, positions 17 to 21 | positions 17 to 21 | same |

Blocks 1 and 3 form one chain on the same strand; block 2 is a chain on the opposite strand, found by aligning $G_1$ with the reverse complement of $G_2$. Read as a signed order of blocks, $G_2$ is $(+1, -2, +3)$ relative to $G_1$, one reversal away from $(+1, +2, +3)$, which is where the theory of [sorting by reversals](/sorting-by-reversals/) starts.

## Known algorithms

All widely used methods follow the same pipeline: find anchors, chain them, then align and filter. Each tool below is an example of one design.

- **[MUMmer](/mummer/)** (Delcher and colleagues, 1999, and later versions). Anchors are maximal unique matches found with a suffix tree, chained by a longest increasing subsequence; the gaps are aligned with dynamic programming. Suited to close genomes.
- **BLASTZ with chains and nets** (Schwartz and colleagues, 2003; Kent and colleagues, 2003). BLASTZ finds local alignments from spaced seeds with gapped extension. Kent's chaining joins the local alignments into chains with gap costs, as in [colinear chaining](/colinear-chaining/), and the net step builds the hierarchy described above. These chains and nets are the pairwise alignments of the UCSC Genome Browser.
- **Mauve** (Darling and colleagues, 2004). Uses multi-MUMs, exact matches unique in each of several genomes, as anchors, groups them into *locally collinear blocks*, and drops blocks whose weight is too small to be real. It aligns several bacterial genomes with rearrangements.
- **Progressive Cactus** (Armstrong and colleagues, 2020). A reference-free multiple aligner that aligns genomes up a guide tree, with a graph structure (a cactus graph) that represents rearrangements and duplications. It has aligned hundreds of vertebrate genomes.
- **[Minimap2](/minimap2/)** (Li, 2018). Its presets for assemblies align a whole genome to another by minimizer anchors and [seed chaining](/seed-chaining/) with gap costs, followed by extension.

## Bounds

- **Quadratic dynamic programming.** One collinear alignment of genomes of lengths $n$ and $m$ by dynamic programming takes $O(nm)$ time, about $10^{19}$ cells for two mammalian genomes. Under the strong exponential time hypothesis, edit distance has no $O(n^{2-\varepsilon})$ algorithm ([edit distance hardness](/edit-distance-hardness/)), so practical methods use anchors and give up the guarantee of an optimal alignment.
- **Chaining.** With $u$ anchors, the best collinear chain without gap costs takes $O(u \log u)$ time by [colinear chaining](/colinear-chaining/).
- **Multiple alignment.** Optimal multiple alignment under the sum-of-pairs score is NP-hard (Wang and Jiang, 1994), so multiple whole-genome alignment is NP-hard under that score.
- **Rearrangements.** Once the blocks are found, the fewest inversions that turn one signed block order into another can be found in polynomial time, but the unsigned version is NP-hard ([sorting by reversals](/sorting-by-reversals/)).

## Reductions

- **To colinear chaining.** If the anchors are given as intervals in both genomes with weights, the best collinear set is an instance of [colinear chaining](/colinear-chaining/). With point anchors in two genomes and weights equal to length, it is a weighted [longest increasing subsequence](/longest-increasing-subsequence/).
- **To global alignment of gaps.** Between two consecutive anchors of a chain, the remaining problem is a small [global alignment](/global-alignment/) of the two gap strings.
- **From global alignment.** Two genomes with no rearrangement reduce whole-genome alignment to one global alignment, which carries over its quadratic lower bound under SETH.
- **To genome rearrangement.** The blocks, read as signed sequences of block labels, turn the alignment into an instance of [sorting by reversals](/sorting-by-reversals/) or one of its variants.

## Applications

- Comparative genomics: finding sequence conserved between species, which marks genes and regulatory elements.
- Finding structural variants, inversions, translocations and large insertions between assemblies.
- Checking a new genome assembly against a reference or another assembly.
- Mapping coordinates and annotations between genome versions or between species, as the UCSC liftOver tool does with chains.
- Building pangenome graphs from many assemblies, which then serve [sequence-to-graph alignment](/sequence-to-graph-alignment/).

## References
