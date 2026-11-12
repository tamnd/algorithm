---
tag: 4EKXJJ
kind: technique
slug: overlap-layout-consensus
name: Overlap-layout-consensus assembly
aliases:
- OLC
area: biology/genome-assembly
level: core
summary: "Assembly paradigm in three steps: find the overlaps between reads, lay the reads out along paths of an overlap graph, then call a consensus sequence for each path."
prereqs: [overlap-detection, overlap-graph, genome-assembly-problem]
see_also: [string-graph, consensus-sequence-calling, greedy-shortest-common-superstring, de-bruijn-assembly, unitig, read-error-correction, lander-waterman-model, hybrid-assembly]
sources:
  - paper: doi:10.1007/BF01188580
    title: John D. Kececioglu and Eugene W. Myers, Combinatorial algorithms for DNA sequence assembly, Algorithmica 13(1/2), 1995
    locator: pp. 7 to 51, fragment assembly split into overlap, layout and consensus (multiple alignment) phases
  - paper: doi:10.1126/science.287.5461.2196
    title: Eugene W. Myers et al., A whole-genome assembly of Drosophila, Science 287(5461), 2000
    locator: pp. 2196 to 2204, the Celera assembler, its overlapper, unitigs and scaffolds
  - paper: doi:10.1093/bioinformatics/bti1114
    title: Eugene W. Myers, The fragment assembly string graph, Bioinformatics 21(suppl 2), 2005
    locator: pp. ii79 to ii85, the string graph as the layout structure
  - paper: doi:10.1101/gr.215087.116
    title: Sergey Koren, Brian P. Walenz, Konstantin Berlin, Jason R. Miller, Nicholas H. Bergman and Adam M. Phillippy, Canu, scalable and accurate long-read assembly via adaptive k-mer weighting and repeat separation, Genome Research 27(5), 2017
    locator: pp. 722 to 736, an OLC assembler for noisy long reads that corrects, trims and then assembles
  - paper: doi:10.1093/bioinformatics/btw152
    title: Heng Li, Minimap and miniasm, fast mapping and de novo assembly for noisy long sequences, Bioinformatics 32(14), 2016
    locator: pp. 2103 to 2110, overlap and layout without a consensus step
  - paper: doi:10.1101/gr.214270.116
    title: Robert Vaser, Ivan Sović, Niranjan Nagarajan and Mile Šikić, Fast and accurate de novo genome assembly from long uncorrected reads, Genome Research 27(5), 2017
    locator: pp. 737 to 746, Racon, a consensus step by partial-order alignment after a layout without consensus
  - paper: doi:10.1016/j.ygeno.2010.03.001
    title: Jason R. Miller, Sergey Koren and Granger Sutton, Assembly algorithms for next-generation sequencing data, Genomics 95(6), 2010
    locator: pp. 315 to 327, the OLC, de Bruijn graph and greedy families of assemblers
---

Overlap-layout-consensus (OLC) is an assembly paradigm with three steps: compute the overlaps between all pairs of reads, find a layout of the reads as paths in a graph of these overlaps, and compute a consensus sequence for each path from the reads aligned on it. It works with whole reads, so it uses all the information of reads that are long compared to the repeats. Most assemblers for Sanger reads and for long single-molecule reads follow it; short-read assemblers mostly use the de Bruijn graph instead.

## In plain words

You have many copies of a book, each cut into random strips, and some letters on the strips are wrong. First, you compare the strips in pairs and note which ones share text at their ends. Next, you use these notes to put the strips in order, one after another, as a long row with overlaps. Last, for each column of the row, you read the letter on all strips that cover it and write down the letter that most strips agree on.

The third step corrects most single wrong letters, because the other strips at that place have the right letter. The second step is the hard one: text that occurs twice in the book makes two orders look equally good.

## When it applies

**Model.** The genome is a string of length $G$. The input is $N$ reads of length about $L$, with coverage $c = NL/G$. Each base is wrong with a probability $p$, independently, by substitution, insertion or deletion. The graph is an [overlap graph](/overlap-graph/) or a [string graph](/string-graph/) on the reads.

OLC fits when:

- the reads are long, so that $L$ is larger than most repeats of the genome, as for Sanger reads of about 1 kb and long reads of 10 kb or more;
- the error rate is high or the errors include insertions and deletions, which break $k$-mers but not alignments;
- the number of reads is small enough for the overlap step, which compares many pairs.

For hundreds of millions of short reads, the overlap step is too expensive, and [de Bruijn graph assembly](/de-bruijn-assembly/) is the usual choice.

## The template

```pseudo id=main
OLC-ASSEMBLE(reads, ℓ)
L1  reads ← PREPARE(reads)                   ▷ hole: trim, correct errors, or keep the reads
L2  E ← OVERLAP(reads, ℓ)                    ▷ hole: exact or approximate overlap detection
L3  H ← GRAPH(reads, E)                      ▷ hole: overlap graph or string graph
L4  H ← SIMPLIFY(H)                          ▷ hole: contained reads, transitive edges, tips, bubbles
L5  P ← LAYOUT(H)                            ▷ hole: greedy merging or maximal non-branching paths
L6  for each path p in P do
L7      place the reads of p at the summed offsets of its edges
L8      output CONSENSUS(the placed reads)    ▷ hole: majority vote, partial-order alignment, polishing
```

**The holes.**

- PREPARE removes adapters and low-quality ends, and can correct the reads with the other reads; see [read error correction](/read-error-correction/).
- OVERLAP is [overlap detection](/overlap-detection/): exact suffix-prefix matches, or approximate overlaps from seeds, [minimizers](/minimizer/) or MinHash, with or without base-level alignment.
- GRAPH and SIMPLIFY give the structure on which the layout is a path. The string graph removes contained reads and transitive edges; [assembly graph simplification](/assembly-graph-simplification/) then removes tips and bubbles.
- LAYOUT chooses paths. A greedy layout merges the pair with the longest overlap first, as in the [greedy superstring](/greedy-shortest-common-superstring/) algorithm. A graph layout outputs the maximal non-branching paths, the [unitigs](/unitig/), and stops at each branch.
- CONSENSUS turns the placed reads into one sequence; see [consensus calling](/consensus-sequence-calling/).

**Cost.** Let $m$ be the number of reads after PREPARE and $n$ their total length. Comparing all pairs by alignment costs $O(m^2 L^2)$ in the worst case, so practical OVERLAP holes are filters, and their cost is close to linear in $n$ plus the number of candidate pairs, as observed for the tools on the overlap detection page. Under the coverage model without repeats, the number of true overlaps is about $N c$, the layout is linear in the size of the graph, and a majority-vote consensus over a fixed layout reads each base of each read once, so it costs $O(n)$.

**Example.** The genome is `TACGGATCATGCATT`, with $G = 15$. Five reads of length 7 start at positions 0, 2, 4, 6 and 8, so $N = 5$, $L = 7$ and $c = 35/15 \approx 2.3$. Read 1 has an error: it is `CGGTTCA`, while the genome has `CGGATCA` there.

1. OVERLAP with $\ell = 3$ and at most one mismatch in five bases finds 7 pairs: four of length 5, with one mismatch in $(0, 1)$ and in $(1, 2)$, and three of length 3.
2. GRAPH and SIMPLIFY remove the three overlaps of length 3, which are transitive, and leave the chain $0 \to 1 \to 2 \to 3 \to 4$ with offset 2 on each edge.
3. LAYOUT outputs this one path. The reads are placed at 0, 2, 4, 6 and 8.
4. CONSENSUS reads each column. At position 5, read 0 has `A`, read 1 has `T` and read 2 has `A`, so the majority is `A`. Every other column has no disagreement.

The consensus is `TACGGATCATGCATT`, the genome. With only two reads over position 5, the vote would be a tie, and the base qualities would have to decide.

## Classic examples

- **Greedy assemblers.** The TIGR assembler and other early tools merged reads by the longest overlap first. This is the greedy layout; see [greedy superstring](/greedy-shortest-common-superstring/).
- **Celera assembler.** Myers et al. (2000) assembled the Drosophila genome from Sanger reads with an overlapper, a layout of [unitigs](/unitig/) in an overlap graph, and [scaffolding](/scaffolding/) with mate pairs.
- **String graph assemblers.** SGA builds the [string graph](/string-graph/) of short reads from an FM-index, and miniasm builds it from minimap overlaps of raw long reads. Miniasm has no consensus step, so its contigs have about the error rate of the reads.
- **Canu.** Koren et al. (2017) built Canu from the Celera assembler for noisy long reads. It computes overlaps with MinHash, corrects and trims the reads, and then runs the overlap, layout and consensus steps again on the corrected reads.
- **Racon after miniasm.** Racon fills the missing consensus hole: it maps the reads to the draft contigs and calls a consensus with [partial-order alignment](/partial-order-alignment/).

## Variations

- **Correct first or polish last.** Canu corrects the reads before the overlap step; miniasm with Racon assembles the raw reads and corrects the contigs at the end. The second order is faster, but errors in the reads make the overlaps less exact.
- **Layout without consensus.** If the reads are accurate, as for high-fidelity long reads, the layout alone gives contigs with few errors, and a light polish is enough.
- **OLC and the de Bruijn graph.** A de Bruijn assembler replaces the pairwise overlaps by exact $(k-1)$-overlaps of $k$-mers, which a hash table finds in linear time, but it cuts the reads into $k$-mers and so resolves only repeats shorter than $k$. Some assemblers build a de Bruijn graph first and then use the reads for an OLC-like layout of the long paths.
- **Hybrid assembly.** Long reads give the layout and short accurate reads give the consensus; see [hybrid assembly](/hybrid-assembly/).

## Pitfalls

- **Repeats longer than the reads.** No read spans such a repeat, so the layout has a branch there. A greedy layout picks one branch and can join two distant parts of the genome, which is a misassembly. A graph layout stops at the branch and gives shorter but correct contigs. See [genome repeats](/genome-repeat/).
- **Collapsed repeats in the consensus.** If two copies of a repeat are laid out as one, the consensus mixes reads from both copies, and the differences between the copies look like errors and are voted away.
- **Chimeric reads.** A read made of two pieces from distant places creates false overlaps that join unrelated parts of the genome. Detect them as reads whose overlaps cover the two halves but never the middle.
- **The overlap step dominates.** All-pairs comparison is quadratic in $m$. Without a good filter, OLC does not scale to large numbers of short reads.
- **Both strands.** Reads come from both strands of the DNA. Overlaps must include the reverse complements, and the layout must give each read an orientation.
- **Consensus cannot repair the layout.** A consensus fixes base errors on a correct path. It does not fix reads placed in the wrong order or a path that joins two copies of a repeat.

## Exercises

1. In the example, give the overlaps of length 3 and show that each one is transitive.
2. Show that with $\ell = 2$ and exact overlaps the reads without the error give a false edge, and say which value of $\ell$ removes it.
3. For a column covered by $c$ reads with independent substitution errors at rate $p$, write the probability that a majority vote with $c$ odd gives the wrong base, assuming every wrong read shows the same wrong base. Evaluate it for $c = 5$ and $p = 0.1$.
4. Construct a genome with a repeat longer than the reads for which the greedy layout joins two parts that are not adjacent in the genome.
5. Estimate the number of read pairs that a naive overlap step compares for $G = 3 \cdot 10^9$, $L = 15000$ and $c = 30$, and compare it with the number of true overlaps under the coverage model.

## References
