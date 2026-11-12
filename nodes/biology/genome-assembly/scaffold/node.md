---
tag: PMV3KV
kind: definition
slug: scaffold
name: Scaffold
area: biology/genome-assembly
level: intro
summary: An ordered list of contigs, each with a strand, with an estimated gap length between consecutive contigs. It is written as one sequence with runs of N in the gaps.
prereqs: [contig, paired-end-reads]
see_also: [scaffolding, gap-filling, n50, assembly-quality-assessment, repeat-resolution, genome-assembly-problem]
sources:
  - paper: doi:10.1145/585265.585267
    title: Daniel H. Huson, Knut Reinert and Eugene W. Myers, The greedy path-merging algorithm for contig scaffolding, Journal of the ACM 49(5) (2002)
    locator: pp. 603 to 615, Sections 1 to 3 (scaffold as pieces of known relative orientation and approximate distance; the contig-mate-pair graph and the length of a mate-edge, Figure 2)
  - paper: doi:10.1101/gr.1536204
    title: Mihai Pop, Daniel S. Kosack and Steven L. Salzberg, Hierarchical scaffolding with Bambus, Genome Research 14(1) (2004)
    locator: pp. 149 to 159 (scaffolds built from contigs and mate-pair links)
---

A scaffold is an ordered list of [contigs](/contig/), each with a strand, with an estimated length for the gap between each two consecutive contigs. The contigs come from the assembly, and the order, the strands and the gap lengths come from long-range links, usually [read pairs](/paired-end-reads/) whose two reads land in different contigs. Huson, Reinert and Myers describe a scaffold as a collection of pieces of sequence of known relative orientation and approximate distance. A scaffold is the output of [scaffolding](/scaffolding/), and the input of [gap filling](/gap-filling/).

## Definition

Let $\mathcal{C}$ be a set of contigs, each a string over $\{\mathtt{A}, \mathtt{C}, \mathtt{G}, \mathtt{T}\}$. For a contig $c$, write $c^{+} = c$ and $c^{-}$ for its reverse complement. A **scaffold** is a sequence

$$\big( (c_1, o_1), g_1, (c_2, o_2), g_2, \ldots, g_{r-1}, (c_r, o_r) \big),$$

where $c_1, \ldots, c_r$ are distinct contigs of $\mathcal{C}$, each **orientation** $o_i$ is $+$ or $-$, and each **gap estimate** $g_i$ is an integer, often with a standard deviation $\sigma_i$. The claim of the scaffold is that the genome contains $c_1^{o_1}$, then about $g_1$ unknown letters, then $c_2^{o_2}$, and so on, on one strand of one molecule.

The **scaffold sequence** is $c_1^{o_1}\, \mathtt{N}^{g_1}\, c_2^{o_2}\, \mathtt{N}^{g_2} \cdots c_r^{o_r}$, where $\mathtt{N}^{g}$ is a run of $g$ letters $\mathtt{N}$. The letters $\mathtt{N}$ mark the gaps; their number is the estimate, not a known length.

Two scaffolds describe the same object if one is the other read from the other strand: reverse the list and change each $+$ to $-$ and each $-$ to $+$. The gaps stay the same, in reverse order.

**Gap estimate from read pairs.** Let a library have a mean insert size $m$ and a standard deviation $\sigma$, where the insert size is the distance from the start of one read to the start of its mate. If one read lies at distance $d_A$ from the right end of contig $A$, pointing to the right, and its mate lies at distance $d_B$ from the left end of contig $B$, pointing to the left, the pair gives the estimate $g = m - d_A - d_B$. This is the length that Huson, Reinert and Myers give to a mate-edge. The mean of $n$ such estimates has a standard deviation of about $\sigma / \sqrt{n}$.

## Examples and non-examples

**A gap from four pairs.** Contig $A$ has length 5,000 and contig $B$ has length 3,000. A library has $m = 2{,}000$ and $\sigma = 100$. Four pairs join the right end of $A$ to the left end of $B$:

| pair | $d_A$ | $d_B$ | $g = 2000 - d_A - d_B$ |
|---|---|---|---|
| 1 | 800 | 300 | 900 |
| 2 | 1,000 | 140 | 860 |
| 3 | 650 | 400 | 950 |
| 4 | 720 | 390 | 890 |

The mean is 900, with a standard deviation of about $100 / \sqrt{4} = 50$. The scaffold is $((A, +), 900, (B, +))$, and its sequence has length $5{,}000 + 900 + 3{,}000 = 8{,}900$.

**A contig on the other strand.** In the pairs above, the read in $A$ aligns to the forward strand of $A$ and its mate aligns to the reverse strand of $B$. If both reads align to the forward strands of their contigs, then $B$ lies on the other strand relative to $A$, $d_B$ is measured from the right end of $B$, and the scaffold is $((A, +), g, (B, -))$.

**One contig.** A single contig is a scaffold with $r = 1$ and no gaps.

**A negative gap.** If the estimate is negative, the two contigs probably overlap and the assembler did not join them. One choice is to align the two ends and merge the contigs if they match; another is to keep a short run of $\mathtt{N}$ between them as a marker.

**Non-example: a set of contigs.** Contigs that the links put in one connected group, but with no order or no strands, are not a scaffold. The scaffold must fix both.

**Non-example: a contradictory list.** If two contigs in a list occupy the same positions by their gap estimates, and their sequences do not match there, the list is not a consistent scaffold of any genome. Scaffolding methods check for this case.

## Related definitions

- **[Contig](/contig/).** A gapless sequence that the assembly supports letter by letter. A scaffold joins contigs over gaps whose sequence is not known.
- **Scaffold N50.** The [N50](/n50/) computed over scaffold lengths, gaps included. It is usually much larger than the contig N50 of the same assembly, which is why [assembly quality assessment](/assembly-quality-assessment/) reports both.
- **Misjoin.** A scaffold that joins two contigs that are not adjacent in the genome, or that gives one the wrong strand. It comes from chimeric pairs or from links that land in [repeats](/genome-repeat/).
- **[Scaffolding](/scaffolding/).** The problem of computing scaffolds from contigs and links.
- **[Gap filling](/gap-filling/).** The problem of replacing the runs of $\mathtt{N}$ by sequence.

## References
