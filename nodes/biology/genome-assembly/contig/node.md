---
tag: ZMCD8S
kind: definition
slug: contig
name: Contig
aliases:
- contiguous sequence
area: biology/genome-assembly
level: intro
summary: A gap-free sequence that an assembler builds from overlapping reads. In graph terms it is a walk that every possible genome contains; unitigs and omnitigs are such walks.
prereqs: [shotgun-sequencing]
see_also: [unitig, scaffold, de-bruijn-assembly, overlap-layout-consensus, n50, lander-waterman-model, genome-repeat, assembly-quality-assessment]
sources:
  - paper: doi:10.1093/nar/8.16.3673
    title: Rodger Staden, A new computer method for the storage and manipulation of DNA gel reading data, Nucleic Acids Research 8(16) (1980)
    locator: pp. 3673 to 3694 (the first use of the word contig for a set of overlapping gel readings)
  - paper: doi:10.1016/0888-7543(88)90007-9
    title: Eric S. Lander and Michael S. Waterman, Genomic mapping by fingerprinting random clones, a mathematical analysis, Genomics 2(3) (1988)
    locator: pp. 231 to 239 (the expected number of islands)
  - paper: doi:10.1089/cmb.2016.0141
    title: Alexandru I. Tomescu and Paul Medvedev, Safe and complete contig assembly through omnitigs, Journal of Computational Biology 24(6) (2017)
    locator: pp. 590 to 602 (Definition 5 of an omnitig, Theorem 1 that safe strings are the omnitig strings, Theorem 2 the polynomial algorithm)
  - paper: doi:10.1145/3341731
    title: Massimo Cairo, Paul Medvedev, Nidia Obscura Acosta, Romeo Rizzi and Alexandru I. Tomescu, An optimal O(nm) algorithm for enumerating all walks common to all closed edge-covering walks of a graph, ACM Transactions on Algorithms 15(4) (2019)
    locator: the O(nm) algorithm and the matching lower bound on the output size
  - paper: doi:10.1007/BF01188580
    title: John D. Kececioglu and Eugene W. Myers, Combinatorial algorithms for DNA sequence assembly, Algorithmica 13(1-2) (1995)
    locator: pp. 7 to 51
---

A contig is a sequence without gaps that an assembler builds from reads that overlap one another. The word is short for "contiguous", and it names both the string and the set of reads placed along it. An assembler usually outputs many contigs, because it stops a contig where the coverage ends or where a [repeat](/genome-repeat/) leaves more than one way to go on. In the graph model of assembly, a contig is *safe* if every genome that fits the data contains it; [unitigs](/unitig/) are safe, and omnitigs are the longest safe walks.

## Definition

**Practical definition.** Let $R$ be a set of reads from a genome $S$. A **contig** is a string $s$ together with a *layout*: a set of reads of $R$ and, for each one, an offset and an orientation in $s$, such that the reads cover each position of $s$ and consecutive reads overlap. The letters of $s$ are the [consensus](/consensus-sequence-calling/) of the reads at each position. A contig has no unknown letters. When contigs are ordered and joined with gaps of estimated length, the result is a [scaffold](/scaffold/).

**Graph definition.** Let $H$ be an assembly graph, for example the edge-centric [de Bruijn graph](/de-bruijn-graph/) of the reads or the [string graph](/string-graph/). A contig is the string *spelled* by a walk $w$ of $H$, written $\mathrm{spell}(w)$. For a de Bruijn graph of order $k$, this is the first $k$-mer of $w$ followed by the last letter of each later $k$-mer.

**Safe contigs.** The definition of Tomescu and Medvedev (2017) needs a model of which walks are possible genomes. In their edge-centric model, a *genomic reconstruction* is a closed walk of $H$ that uses each edge at least once. This expresses a circular genome, no errors and no coverage gaps. A string $s$ is **safe** if it is a substring of $\mathrm{spell}(w)$ for every genomic reconstruction $w$. An algorithm that outputs only safe strings never makes a misassembly in the model.

**Omnitigs.** A walk $v_0, e_0, v_1, e_1, \ldots, v_t, e_t, v_{t+1}$ of $H$ is an **omnitig** if, for all $1 \le i \le j \le t$, there is no path of length at least 1 from $v_j$ to $v_i$ whose first edge is not $e_j$ and whose last edge is not $e_{i-1}$. Such a path would let a genome leave the walk at $v_j$ and come back at $v_i$ without the part between them. Theorem 1 of Tomescu and Medvedev says that a string is safe if and only if it is spelled by an omnitig. Their Theorem 2 gives a polynomial-time algorithm that outputs all maximal omnitigs. Cairo, Medvedev, Acosta, Rizzi and Tomescu (2019) give an $O(nm)$ algorithm for a graph with $n$ vertices and $m$ edges. The title of their paper calls it optimal: the maximal omnitigs of some graphs have a total length of order $nm$, so writing them out takes that long.

**Unitigs are omnitigs.** In a unitig each inner vertex $v_i$ has in-degree 1 and out-degree 1. A path from $v_j$ that does not start with $e_j$ cannot exist, because $e_j$ is the only edge out of $v_j$. So the omnitig condition holds. The converse fails, as the second example below shows.

**Coverage gaps.** Even without repeats, contigs end where no read covers the genome. In the model of [Lander and Waterman](/lander-waterman-model/) (1988), $N$ reads of length $L$ start at random on a genome of length $G$, the coverage is $c = NL/G$, and two reads join if they overlap by a fraction at least $1 - \sigma$ of $L$. The expected number of islands, the groups of joined reads, is $N e^{-c\sigma}$.

## Examples and non-examples

**Coverage gaps.** A bacterial genome with $G = 5{,}000{,}000$ is read with $L = 100$ at coverage $c = 8$, so $N = 400{,}000$. With $\sigma = 1$, the expected number of islands is $400{,}000 \cdot e^{-8} \approx 134$. At $c = 15$, $N = 750{,}000$ and the expected number is $750{,}000 \cdot e^{-15} \approx 0.23$. So at high coverage, the repeats and not the gaps end the contigs.

**An omnitig longer than every unitig.** Take the circular genome $S = x R y R$ with $x = \mathtt{CATTG}$, $R = \mathtt{GTACG}$, $y = \mathtt{TCCA}$, so $S = \mathtt{CATTGGTACGTCCAGTACG}$ and $|S| = 19$, and let $k = 4$. The 19 circular 4-mers hold 17 distinct ones. In the de Bruijn graph, the vertex $\mathtt{GTA}$ has in-degree 2 and out-degree 1, and $\mathtt{ACG}$ has in-degree 1 and out-degree 2. The unitigs are

| unitig | edges | from | to |
|---|---|---|---|
| ACGCATTGGTA | 8 | ACG | GTA |
| ACGTCCAGTA | 7 | ACG | GTA |
| GTACG | 2 | GTA | ACG |

A walk that enters $\mathtt{GTA}$ has one way out, and the only way into $\mathtt{ACG}$ comes from $\mathtt{GTA}$. So each genomic reconstruction that uses the first unitig reads $\mathtt{GTACG}$ before it and after it, and the string $R x R = \mathtt{GTACGCATTGGTACG}$ is safe. It has 15 letters, and the longest unitig has 11. The omnitig condition goes further here. After each copy of $R$ a circular walk takes $x$ or $y$, and a closed walk that uses both must pass from $x$ to $y$ at least once. So $R x R y R$, 24 letters long, is also safe.

**Non-example: a walk across a choice.** In the de Bruijn graph of the triple repeat $\mathtt{CCGTAAGTATTGTAG}$ with $k = 4$, the walk that spells $\mathtt{CCGTAAGTA}$ is not safe: the genome $\mathtt{CCGTATTGTAAGTAG}$ has the same 4-mers and does not contain it. In the omnitig condition, the path $\mathtt{GTA} \to \mathtt{TAT} \to \cdots \to \mathtt{TGTA}$ leaves the walk at $\mathtt{GTA}$ with an edge other than $\mathtt{GTAA}$.

**Non-example: a scaffold.** The string $\mathtt{ACGTT}\,\mathtt{NNNNNNNNNN}\,\mathtt{GGATC}$, with ten unknown letters, is not a contig. It is a scaffold with two contigs.

**A contig with an error.** Real assemblers also remove [tips](/tip-removal/) and [bubbles](/bubble-popping/) and follow read pairs, so their contigs are longer than the safe walks, and some are wrong. A contig that joins two parts of the genome that are not adjacent is a *misassembly*. [Assembly quality assessment](/assembly-quality-assessment/) counts them against a reference.

## Related definitions

- **[Unitig](/unitig/).** The contig of a maximal path whose inner vertices have one edge in and one edge out. It is the simplest safe contig.
- **[Scaffold](/scaffold/).** Contigs in a fixed order and orientation, with gaps of estimated length between them.
- **[N50](/n50/).** The length $\ell$ such that the contigs of length at least $\ell$ hold half of the assembly. It is the usual summary of contig length.
- **Island.** In the [Lander and Waterman model](/lander-waterman-model/), a maximal group of reads joined by overlaps. Without repeats and errors, an island is a contig.
- **[Genome repeat](/genome-repeat/).** A repeat longer than the reads, or longer than $k - 1$ in a de Bruijn graph, makes a branch, so contigs end there.
- **[Read error correction](/read-error-correction/).** Fewer errors make fewer false branches, and the contigs get longer.

## References
