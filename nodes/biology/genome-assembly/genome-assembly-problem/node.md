---
tag: 942W2Z
kind: problem
slug: genome-assembly-problem
name: Genome assembly problem
aliases:
- de novo genome assembly
area: biology/genome-assembly
level: intro
summary: Reconstruct a genome from many short, overlapping, error-prone reads. Repeats make the answer ambiguous, so assemblers output the parts that every consistent genome shares.
prereqs: [shotgun-sequencing, kmer, np-hard]
see_also: [shortest-common-superstring, overlap-layout-consensus, string-graph, de-bruijn-assembly, genome-repeat, chinese-postman-problem, unitig, contig]
sources:
  - paper: doi:10.1089/cmb.2009.0005
    title: Niranjan Nagarajan and Mihai Pop, Parametric complexity of sequence assembly, theory and applications to next generation sequencing, Journal of Computational Biology 16(7) (2009)
    locator: pp. 897 to 908 (the Assembly Problem, Theorems 1 to 7)
  - paper: doi:10.1186/1471-2105-11-21
    title: Carl Kingsford, Michael C. Schatz and Mihai Pop, Assembly complexity of prokaryotic genomes using short reads, BMC Bioinformatics 11 (2010)
    locator: Article 21 (counting the reconstructions with the BEST theorem)
  - paper: doi:10.1007/978-3-540-74126-8_27
    title: Paul Medvedev, Konstantinos Georgiou, Gene Myers and Michael Brudno, Computability of models for sequence assembly, WABI 2007, LNCS 4645
    locator: pp. 289 to 301
  - paper: doi:10.1016/0304-3975(92)90143-4
    title: Esko Ukkonen, Approximate string-matching with q-grams and maximal matches, Theoretical Computer Science 92(1) (1992)
    locator: pp. 191 to 211 (the condition for a string to be fixed by its q-grams)
  - paper: doi:10.1186/1471-2105-14-S5-S18
    title: Guy Bresler, Ma'ayan Bresler and David Tse, Optimal assembly for high throughput shotgun sequencing, BMC Bioinformatics 14(Suppl 5) (2013)
    locator: Article S18 (interleaved and triple repeats, the critical read length)
  - paper: doi:10.1089/cmb.2016.0141
    title: Alexandru I. Tomescu and Paul Medvedev, Safe and complete contig assembly through omnitigs, Journal of Computational Biology 24(6) (2017)
    locator: pp. 590 to 602
  - paper: doi:10.1038/nrg3367
    title: Niranjan Nagarajan and Mihai Pop, Sequence assembly demystified, Nature Reviews Genetics 14(3) (2013)
    locator: pp. 157 to 167
  - book: isbn:9781107078536
    title: Veli Mäkinen, Djamal Belazzougui, Fabio Cunial and Alexandru I. Tomescu, Genome-Scale Algorithm Design, Cambridge University Press (2015)
    locator: Chapter 13, Fragment assembly
---

The genome assembly problem asks for the sequence of a genome, given only the reads of a [shotgun sequencing](/shotgun-sequencing/) experiment: many short substrings from unknown positions and strands, with some errors. The first formal model, the [shortest common superstring](/shortest-common-superstring/), is NP-hard and also gives the wrong answer when the genome has [repeats](/genome-repeat/), because the shortest answer collapses the copies of a repeat into one. Later models count all genomes that agree with the reads and show that the reads often do not fix one genome. So practical assemblers output [contigs](/contig/): the pieces that all consistent genomes share.

## In plain words

Someone copies a long book many times, cuts every copy into small random strips, and gives you the strips in a pile. Your task is to rebuild the book. Strips that share text at their ends were probably neighbors, so you chain them by their overlaps.

This works until the book repeats itself. If the same long paragraph occurs in three chapters, a strip from inside that paragraph fits in all three places. The strips no longer tell you which chapter follows which. Asking for the shortest book that holds all the strips does not help: it keeps only one copy of the repeated paragraph and loses the text between the copies. The honest answer gives the stretches that are certain and marks the places where the strips leave a choice.

## Definition

Let $\Sigma = \{A, C, G, T\}$. For a string $x$, let $\overline{x}$ be its reverse complement.

**Input.** A multiset of reads $R = \{r_1, \ldots, r_N\}$ over $\Sigma$. Each read is a copy of a substring of an unknown genome $S$ or of $\overline{S}$, possibly with a few errors.

**Output.** A string $S'$ such that every read occurs in $S'$ or in $\overline{S'}$, up to the errors, and such that $S'$ is the genome $S$.

The last condition cannot be checked from the input. The reads do not fix $S$ in general: many strings contain all the reads. So every formal version adds an objective or changes the output. The three main versions follow, for error-free reads.

**Shortest superstring version.** Find a shortest string that contains every read as a substring. This is the [shortest common superstring](/shortest-common-superstring/) problem. It is NP-hard, and the shortest string is often not the genome.

**Graph-walk version.** Build a graph from the reads, either the [overlap graph](/overlap-graph/) or [string graph](/string-graph/) of reads, or the [de Bruijn graph](/de-bruijn-graph/) of their [k-mers](/kmer/). A genome that is consistent with the reads spells a walk in the graph that uses each read (or each k-mer) at least once. Nagarajan and Pop define the *Assembly Problem* as the search for a shortest such walk in a string graph, with a minimum overlap $k$ between reads.

**Safe output version.** Output the set of strings that occur in *every* genome consistent with the reads, as long as possible. These are the contigs that are safe to report. Unitigs are safe. Tomescu and Medvedev show that, in their model of a genome as a closed walk that covers the graph, the maximal safe walks are the *omnitigs*, which can be longer than unitigs.

## Variants

- **Single or double strand.** Real reads come from both strands. The graphs then need both orientations of each read, as in a bidirected graph.
- **With errors.** Reads have substitutions, and for some machines insertions and deletions. The assembler first runs [read error correction](/read-error-correction/), then aligns overlaps with errors and computes a [consensus](/consensus-sequence-calling/).
- **With pairs.** [Paired-end reads](/paired-end-reads/) give two reads at a known distance. They help to order contigs into [scaffolds](/scaffolding/) and to resolve repeats.
- **With a reference.** [Reference-guided assembly](/reference-guided-assembly/) uses the genome of a related organism as a guide.
- **With mixed reads.** [Hybrid assembly](/hybrid-assembly/) combines accurate short reads and long reads with more errors.
- **Diploid and mixed samples.** A human genome has two copies of each chromosome that differ at some sites. A metagenome mixes the genomes of many species at different coverage.

## Examples

**A tandem repeat breaks the shortest superstring.** Let $U = \texttt{ACGTTGCA}$ and let the genome be $S = \texttt{CATG}\,UUU\,\texttt{GTCA}$, of length 32. Its 16 distinct substrings of length 6 are the reads. All 16 also occur in $\texttt{CATG}\,UU\,\texttt{GTCA}$, of length 24. So the shortest superstring has length at most 24 and is not $S$. It keeps fewer copies of the repeat than the genome has.

**A triple repeat makes two genomes look the same.** Let $X = \texttt{GATTACA}$ (7 bases) and compare

- $S_1 = \texttt{TC}\,X\,\texttt{CC}\,X\,\texttt{TGT}\,X\,\texttt{GG}$,
- $S_2 = \texttt{TC}\,X\,\texttt{TGT}\,X\,\texttt{CC}\,X\,\texttt{GG}$.

Both have length 30. The stretches CC and TGT between the copies of $X$ swap places. For every $k$ from 3 to 8, $S_1$ and $S_2$ have the same multiset of k-mers, so reads of length 8 or less cannot tell them apart. For $k \ge 9$ the multisets differ. The 9-mer $\texttt{C}\,X\,\texttt{C} = \texttt{CGATTACAC}$, which holds a whole copy of $X$ and one base on each side, occurs in $S_1$ but not in $S_2$.

**Interleaved repeats.** Let $X = \texttt{ACGTA}$ and $Y = \texttt{TTGAC}$. The genomes $\texttt{C}X\texttt{G}Y\texttt{CA}X\texttt{TT}Y\texttt{G}$ and $\texttt{C}X\texttt{TT}Y\texttt{CA}X\texttt{G}Y\texttt{G}$ have the same k-mers for $k \le 6$ and differ for $k \ge 7$. Each repeat has only two copies, but the copies alternate, $X \ldots Y \ldots X \ldots Y$, and the stretches between them can swap.

The two examples show the general rule. If a genome has a triple repeat, or an interleaved pair of repeats, of length at least $L - 1$, reads of length $L$ cannot fix the genome. This is *Ukkonen's condition*.

## Known algorithms

- **Greedy merging.** Merge the two reads with the largest overlap, and repeat. See the [greedy shortest common superstring](/greedy-shortest-common-superstring/) algorithm. Early assemblers used it.
- **[Overlap-layout-consensus](/overlap-layout-consensus/).** Find all pairwise [overlaps](/overlap-detection/), find a layout as a path in the [overlap graph](/overlap-graph/) or [string graph](/string-graph/), then call the consensus. Used for long reads.
- **[de Bruijn assembly](/de-bruijn-assembly/).** Break the reads into k-mers, build the de Bruijn graph, simplify it ([tips](/tip-removal/), [bubbles](/bubble-popping/)), and output its [unitigs](/unitig/) as contigs. Used for short reads. The [Eulerian superpath problem](/eulerian-superpath-problem/) adds the constraint that each read must be a subpath.
- **Scaffolding.** Order and orient the contigs with read pairs, then fill the gaps; see [scaffolding](/scaffolding/) and [gap filling](/gap-filling/).

The usual output is a set of contigs and scaffolds, not one string. The quality is measured by the contig length statistics such as [N50](/n50/), and by the errors against a known genome; see [assembly quality assessment](/assembly-quality-assessment/).

## Bounds

**Hardness of the shortest versions.**

- Shortest common superstring is NP-hard; see [its hardness proof](/shortest-common-superstring-np-hard/).
- The Assembly Problem of Nagarajan and Pop is NP-hard, by a reduction from shortest superstring (their Theorem 1). It stays NP-hard when all repeats are short (Corollary 2), when the read length $r$ and the minimum overlap $k$ satisfy $r - k \ge 4$ (Theorem 7), and on a binary alphabet when $r \ge 2k + 4$ (Theorem 6).
- Medvedev, Georgiou, Myers and Brudno show NP-hardness for both the string graph model and the de Bruijn graph model, when each read must be used in full.

**Easy cases.**

- When the graph is a de Bruijn graph and the only constraint is that the walk uses every k-mer, a shortest walk is a [Chinese postman](/chinese-postman-problem/) tour, which takes polynomial time. Medvedev and colleagues give a polynomial algorithm by bidirected flow for the shortest double-stranded string that contains all k-mers.
- Nagarajan and Pop show that the Assembly Problem is polynomial when all repeats are long enough, at least $2 r_{\max} - k - 1$ where $r_{\max}$ is the longest read length (Theorem 2). It is also polynomial, with a unique answer, when all repeats are shorter than the shortest read and every repeat copy is spanned by a read (Theorem 4).

**Why the shortest answer is wrong.** Nagarajan and Pop prove that a shortest superstring cannot contain a repeat of length $2 r_{\max} - 1$ or more (Theorem 5). A real genome with such a repeat is then never the shortest answer: the shortest answer collapses the repeat. Hardness is not the main obstacle. The objective itself is wrong.

**How many answers there are.** Counting the Chinese postman tours, and so the shortest reconstructions, is #P-complete (Nagarajan and Pop, Theorem 3). For the de Bruijn graph in which each k-mer is an edge used once, the number of reconstructions is the number of Eulerian circuits, which the BEST theorem gives in polynomial time. Kingsford, Schatz and Pop computed this number for 668 chromosomes and plasmids of 375 prokaryotes. The genome is fixed by its k-mers only when the Eulerian circuit is unique, and for short read lengths many genomes are not. Most genes can still be rebuilt from reads of 25 bases, because the ambiguity sits in repeats such as mobile elements. Genome size alone is a poor measure of how hard the assembly is.

**When the reads fix the genome.** Ukkonen's condition is necessary: with a triple repeat or an interleaved repeat of length at least $L - 1$, the reads cannot fix the genome. Bresler, Bresler and Tse define the critical read length $L_{\text{crit}} = \max(\ell_{\text{interleaved}}, \ell_{\text{triple}}) + 1$ from the longest such repeats. The coverage must also be high enough that the reads overlap everywhere, which the [Lander-Waterman model](/lander-waterman-model/) quantifies. They give an algorithm whose needs come close to these two lower bounds on the genomes that they study.

## Reductions

- **From shortest superstring.** Shortest common superstring reduces to the Assembly Problem, which proves its NP-hardness.
- **To Hamiltonian paths.** A shortest superstring is a maximum-weight [Hamiltonian path](/hamiltonian-path/) in the overlap graph.
- **To Eulerian paths.** If the reads are replaced by their k-mers, a genome is an [Eulerian path](/eulerian-path/) in the de Bruijn graph, or a Chinese postman tour when k-mers may be used more than once. Nagarajan and Pop show the de Bruijn Superpath Problem, which keeps the reads as paths, equivalent to the Assembly Problem.
- **Sequencing by hybridization.** When the data is the set of k-mers of the genome, the problem is [sequencing by hybridization](/sequencing-by-hybridization/), which Pevzner solved with Eulerian paths.

## Applications

- New reference genomes of species that have none.
- Bacterial genomes in clinical and food safety work, where a strain must be compared with known strains.
- Metagenomics: the genomes of microbes that cannot be grown in the lab.
- Structural variants: regions of an individual genome that differ too much from the reference to be found by [read mapping](/read-mapping/).
- The assembly of transcripts from RNA reads, with the same graph methods.

## References
