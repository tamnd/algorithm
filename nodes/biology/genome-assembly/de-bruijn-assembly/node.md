---
tag: 0WN504
kind: algorithm
slug: de-bruijn-assembly
name: de Bruijn graph assembly
aliases:
- de Bruijn assembler
- Eulerian assembly
area: biology/genome-assembly
level: core
summary: Count the k-mers of the reads, keep the frequent ones, build their de Bruijn graph and output the strings of its maximal non-branching paths as contigs.
solves: [genome-assembly-problem]
model: word-ram
complexity:
  vars: {T: the total length of the reads, k: the k-mer length, m: the number of distinct kept k-mers}
  time: {expected: O(k·T), worst: O(k·T + k·m·log m)}
  space: {extra: O(k·m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1995
  people: [Ramana M. Idury, Michael S. Waterman]
  note: Idury and Waterman proposed to assemble shotgun reads from their k-mers in 1995. EULER (2001) made the method practical, and Velvet (2008) and SPAdes (2012) adapted it to short reads.
prereqs: [de-bruijn-graph, eulerian-path, kmer-counting, unitig]
see_also: [overlap-layout-consensus, string-graph, tip-removal, bubble-popping, assembly-graph-simplification, eulerian-superpath-problem, repeat-resolution, contig]
sources:
  - paper: doi:10.1089/cmb.1995.2.291
    title: Ramana M. Idury and Michael S. Waterman, A new algorithm for DNA sequence assembly, Journal of Computational Biology 2(2) (1995)
    locator: pp. 291 to 306
  - paper: doi:10.1073/pnas.171285098
    title: Pavel A. Pevzner, Haixu Tang and Michael S. Waterman, An Eulerian path approach to DNA fragment assembly, Proceedings of the National Academy of Sciences 98(17) (2001)
    locator: pp. 9748 to 9753 (EULER, error correction before the graph, the Eulerian superpath problem)
  - paper: doi:10.1101/gr.074492.107
    title: Daniel R. Zerbino and Ewan Birney, Velvet, algorithms for de novo short read assembly using de Bruijn graphs, Genome Research 18(5) (2008)
    locator: pp. 821 to 829 (tips, Tour Bus, coverage cutoff)
  - paper: doi:10.1089/cmb.2012.0021
    title: Anton Bankevich and others, SPAdes, a new genome assembly algorithm and its applications to single-cell sequencing, Journal of Computational Biology 19(5) (2012)
    locator: pp. 455 to 477 (the multisized graph, bulge removal, the paired de Bruijn graph)
  - paper: doi:10.1038/nbt.2023
    title: Phillip E. C. Compeau, Pavel A. Pevzner and Glenn Tesler, How to apply de Bruijn graphs to genome assembly, Nature Biotechnology 29(11) (2011)
    locator: pp. 987 to 991
  - paper: doi:10.1007/978-3-540-74126-8_27
    title: Paul Medvedev, Konstantinos Georgiou, Gene Myers and Michael Brudno, Computability of models for sequence assembly, WABI 2007, LNCS 4645
    locator: pp. 289 to 301 (the shortest superwalk in a de Bruijn graph is NP-hard)
---

De Bruijn graph assembly turns a set of sequencing reads into contigs without comparing the reads to each other. It counts the $k$-mers of the reads, keeps those seen often enough, builds the [de Bruijn graph](/de-bruijn-graph/) of the kept $k$-mers, and outputs the string of each maximal non-branching path, the [unitigs](/unitig/), as [contigs](/contig/). The work is linear in the total read length, which is why short-read assemblers such as EULER, Velvet and SPAdes use it. It does not find the genome: a repeat of length at least $k - 1$ joins paths that the genome keeps apart, and the assembler stops the contigs there.

## In plain words

Cut every read into short overlapping words of the same length $k$. A genome position that many reads cover gives the same word many times. A word with a read error is rare, so you drop the rare words.

Now chain the words. Two words follow each other if the end of the first one is the start of the second one. Where each word has exactly one possible next word, you can glue the words without doubt. Where a word has two possible next words, the genome has a repeat or an error there, and you cannot tell which way the genome goes. So you stop at these places. Each piece that you glued without doubt is a contig.

## The problem

The model is the shotgun model of the [genome assembly problem](/genome-assembly-problem/). An unknown genome $S$ of length $G$ is cut into $N$ reads of length $L$ at random positions, so the coverage is $c = NL/G$. In this page the reads come from one strand, and each letter is wrong with a small probability (substitution errors only). The input is the reads and an integer $k \ge 2$. The output is a set of strings, the contigs. Each contig must be a substring of $S$ in the error-free case, and the contigs together should cover as much of $S$ as possible.

The assembler works on the edge-centric de Bruijn graph of order $k$: one vertex for each $(k-1)$-mer and one edge for each kept $k$-mer $x$, from its prefix $x[1 \ldots k-1]$ to its suffix $x[2 \ldots k]$. The genome, read from left to right, is a walk in this graph that uses each $k$-mer of $S$. With full coverage and no errors, it is an [Eulerian path](/eulerian-path/) of the graph in which each edge has the multiplicity of its $k$-mer in $S$. The graph itself is defined on the [de Bruijn graph](/de-bruijn-graph/) page. This page is about how an assembler uses it.

## The algorithm

The input is the list of reads $R$, the length $k$, and a count threshold $t \ge 1$. A vertex is *simple* if it has exactly one edge in and one edge out.

```pseudo id=main
DE-BRUIJN-ASSEMBLY(R, k, t)
L1  C ← an empty map from k-mers to counts
L2  for each read r in R do
L3      for each k-mer x of r do C[x] ← C[x] + 1
L4  E ← {x : C[x] ≥ t}                          ▷ the solid k-mers
L5  build G: an edge x from x[1 .. k−1] to x[2 .. k] for each x in E
L6  simplify G                                   ▷ optional: tips, bubbles, low coverage
L7  for each vertex u of G that is not simple do
L8      for each edge e out of u do
L9          follow e and then the only out-edge, while the head is simple; output the path
L10 for each edge e on no path yet do follow it around its cycle; output the cycle
L11 return the strings spelled by the output paths
```

Lines L1 to L3 are [k-mer counting](/kmer-counting/). Line L4 is the error filter: with coverage $c$, a true $k$-mer is seen about $c(L-k+1)/L$ times, and a $k$-mer that holds an error is seen about once. The [k-mer spectrum](/kmer-spectrum/) of the reads shows where to put $t$. Line L6 is where real assemblers remove [tips](/tip-removal/) and [bubbles](/bubble-popping/); see [assembly graph simplification](/assembly-graph-simplification/). Lines L7 to L10 compact the graph into its unitigs. A path that starts at a non-simple vertex and passes only simple vertices has no choice at any step, so it is a part of each walk through it. Line L10 catches the components that are one cycle of simple vertices, which have no non-simple vertex to start from.

The implementation takes the simplification of line L6 as an optional function on the set of kept $k$-mers, and keeps the reads on one strand. Real assemblers add the reverse complement of each read, or store each $k$-mer together with its reverse complement as one canonical $k$-mer.

## Example

Take the genome $S = \mathtt{GATGCATACGCCTTTA}$ ($G = 16$), with $k = 4$ and $t = 1$. The genome has no repeated 3-mer. The reads have length 8 and start at positions 0, 3, 6 and 8: $\mathtt{GATGCATA}$, $\mathtt{GCATACGC}$, $\mathtt{TACGCCTT}$, $\mathtt{CGCCTTTA}$. So $N = 4$, $L = 8$ and $c = 32/16 = 2$.

Lines L1 to L3 find 13 distinct 4-mers:

| 4-mer | count | 4-mer | count | 4-mer | count |
|---|---|---|---|---|---|
| GATG | 1 | CATA | 2 | CGCC | 2 |
| ATGC | 1 | ATAC | 1 | GCCT | 2 |
| TGCA | 1 | TACG | 2 | CCTT | 2 |
| GCAT | 2 | ACGC | 2 | CTTT | 1 |
| | | | | TTTA | 1 |

The graph has 14 vertices, the 3-mers $\mathtt{GAT}, \mathtt{ATG}, \ldots, \mathtt{TTA}$. The vertex $\mathtt{GAT}$ has in-degree 0, $\mathtt{TTA}$ has out-degree 0, and the other 12 are simple. Line L7 starts only at $\mathtt{GAT}$, line L9 follows the 13 edges to $\mathtt{TTA}$, and line L11 returns one contig, $\mathtt{GATGCATACGCCTTTA} = S$.

Now take a genome with a repeat: $S = \mathtt{CC\,GTA\,A\,GTA\,TT\,GTA\,G}$ ($G = 15$), where $\mathtt{GTA}$ occurs three times, with $k = 4$. Let the reads be all 12 of its 4-mers, which are distinct. The vertex $\mathtt{GTA}$ has in-degree 3 and out-degree 3. The graph has two Eulerian paths, which spell
$\mathtt{CCGTAAGTATTGTAG}$ and $\mathtt{CCGTATTGTAAGTAG}$.
Both genomes have the same $k$-mers, so no assembler that only sees $k$-mers can choose. The output is the four unitigs $\mathtt{CCGTA}$, $\mathtt{GTAAGTA}$, $\mathtt{GTAG}$ and $\mathtt{GTATTGTA}$. Each is a substring of both genomes. They overlap in the repeat $\mathtt{GTA}$, and the order between them is the job of [repeat resolution](/repeat-resolution/).

## Correctness

Three facts hold; [the proof](proofs/correctness.md) gives them in full. First, lines L7 to L10 output each unitig exactly once, and each kept $k$-mer is on exactly one path. Second, if the reads are error-free, each $k$-mer of $S$ occurs at least $t$ times, and no $(k-1)$-mer occurs twice in $S$, then the output is the single contig $S$. Third, with the same coverage assumption and no condition on repeats, each contig is a substring of $S$ when the first and the last $(k-1)$-mer of $S$ occur only once in $S$. The proof of the third fact follows the genome walk: it cannot stop at a simple vertex and it has only one way to leave one, so it runs through each unitig from start to end.

The third fact needs the condition on the ends. For $S = \mathtt{AABABAA}$ and $k = 3$, the unitig $\mathtt{BAA}, \mathtt{AAB}$ spells $\mathtt{BAAB}$, which is not in $S$, because the genome walk starts in the middle of it. For a circular genome the condition is not needed; this is the model in which the [contig](/contig/) page defines safe strings.

## Complexity

Let $T$ be the total length of the reads and $m$ the number of distinct kept $k$-mers, so $m \le T$. Lines L1 to L3 look at $T - N(k-1)$ $k$-mers. With a [hash table](/hash-table/) on strings, each one costs $O(k)$ expected time, so counting is $O(kT)$ expected. Line L5 adds $m$ edges in $O(km)$ expected time. Lines L7 to L10 visit each edge once, at $O(k)$ for each hash lookup, so $O(km)$. The total is $O(kT)$ expected time and $O(km)$ space. If $k \le 32$, a $k$-mer fits in one 64-bit word with 2 bits for each letter, and a rolling update makes each step $O(1)$, so the time becomes $O(T)$ expected.

The implementation sorts the $k$-mers to get a fixed output order, which adds $O(km \log m)$. The space is the limit in practice. Each substitution error makes up to $k$ new $k$-mers, so with an error rate of 1%, $L = 100$, $k = 31$ and $c = 30$, a read holds about $70 \cdot (1 - 0.99^{31}) \approx 19$ false $k$-mers, and the reads hold about $0.19 \cdot c \cdot G \approx 5.7G$ distinct false $k$-mers against $G$ true ones. This is why line L4 comes before line L5, and why large assemblers count $k$-mers with Bloom filters or on disk.

The choice of $k$ is a trade. A repeat of length at least $k - 1$ joins two parts of the graph, so a small $k$ makes many short contigs. A large $k$ lowers the $k$-mer coverage $c(L-k+1)/L$, so more true $k$-mers fall under $t$ and leave gaps. With $c = 30$ and $L = 100$, the $k$-mer coverage is 21 for $k = 31$ and 9 for $k = 71$.

## Properties

- **Deterministic.** The output depends only on the multiset of $k$-mers, not on the order of the reads.
- **Not exact.** It does not return the genome. It returns the parts that it can fix without a choice, and these are shorter than the genome as soon as $S$ has a repeat of length $k - 1$.
- **Free of pairwise read comparison.** Unlike [overlap-layout-consensus](/overlap-layout-consensus/), it never aligns two reads. Two reads that share a $k$-mer meet in the same edge.
- **Loses the read context.** A read longer than $k$ is a walk in the graph, but after line L3 only its $k$-mers remain. EULER keeps the reads as paths for this reason; see the [Eulerian superpath problem](/eulerian-superpath-problem/).
- **Sensitive to errors.** One wrong letter in the middle of a read makes up to $k$ false $k$-mers, which form a [bubble](/bubble-popping/) or, near a read end, a [tip](/tip-removal/).

## Variants and improvements

- **Both strands.** Add the reverse complement of each read, or store canonical $k$-mers and use a bidirected graph. An odd $k$ avoids $k$-mers that equal their own reverse complement.
- **EULER.** Pevzner, Tang and Waterman (2001) correct the reads before they build the graph, and then use the reads as paths in the graph to resolve repeats shorter than the reads. Their target is an Eulerian walk that contains each read path.
- **Velvet.** Zerbino and Birney (2008) remove tips shorter than $2k$, merge bubbles with the Tour Bus search, and then cut edges below a coverage threshold. Breadcrumb uses read pairs to join long nodes.
- **SPAdes.** Bankevich and others (2012) build graphs for several values of $k$ and combine them, so that a small $k$ fills coverage gaps and a large $k$ resolves repeats. They use read pairs through the paired de Bruijn graph.
- **Compacted graph construction.** BCALM 2 and TwoPaCo build the unitigs directly from the $k$-mers in parallel without the full graph in memory; see [unitig](/unitig/).

## When to use it

Use it for many short accurate reads, where the number of reads makes all-against-all overlaps too slow. Bacterial genomes, transcriptomes and the first stage of large short-read assemblies are the main uses. For long reads with many errors, a $k$-mer of length 31 is often wrong, and the [string graph](/string-graph/) or [overlap-layout-consensus](/overlap-layout-consensus/) approach works better. When you have a close reference genome, [reference-guided assembly](/reference-guided-assembly/) is often enough.

## Pitfalls

- **Expecting one contig.** With real genomes the output is many contigs, and the breaks are at repeats and coverage gaps. Report the [N50](/n50/) and check with [assembly quality assessment](/assembly-quality-assessment/), not only the number of contigs.
- **Forgetting the reverse strand.** If you keep only one strand of each read, each region of the genome appears in two unrelated parts of the graph.
- **A threshold that is too high.** Line L4 also removes true $k$-mers at low coverage. Choose $t$ from the valley of the $k$-mer spectrum, not from a fixed number.
- **Unitigs at the genome ends.** In a linear genome a unitig can run across the start or the end of $S$ and spell a string that is not in $S$, as the $\mathtt{BAAB}$ example shows.
- **Isolated cycles.** A component made only of simple vertices has no start vertex. Without line L10, its $k$-mers are lost.
- **Recursion in compaction.** A unitig can have millions of edges. Follow it with a loop, not with recursion.

## Implementations

## History

Pevzner proposed in 1989 to reconstruct a DNA string from its $k$-mers as an Eulerian path problem, for sequencing by hybridization. Idury and Waterman (1995) applied the idea to shotgun reads: they cut the reads into $k$-mers and assembled them through the de Bruijn graph. Pevzner, Tang and Waterman (2001) made it work on real Sanger data with EULER, which corrects errors first and keeps the reads as paths. Short reads from 2007 on made the method the standard one: Velvet (Zerbino and Birney, 2008), ABySS, SOAPdenovo and SPAdes (Bankevich and others, 2012) are all de Bruijn assemblers. Medvedev, Georgiou, Myers and Brudno (2007) showed that the question "what is the shortest genome that walks through the graph and contains each read as a path" is NP-hard, which is one reason the assemblers return unitigs and not a full walk.

## References
