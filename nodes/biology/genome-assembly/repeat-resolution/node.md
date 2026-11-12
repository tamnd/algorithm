---
tag: PDH55W
kind: problem
slug: repeat-resolution
name: Repeat resolution
aliases:
- repeat disambiguation
- repeat untangling
area: biology/genome-assembly
level: advanced
summary: Decide how the copies of a repeat that the assembly graph merged connect to the sequence around them, using read paths, read pairs and coverage, and know when no data can decide.
prereqs: [genome-repeat, paired-end-reads, de-bruijn-assembly]
see_also: [eulerian-superpath-problem, unitig, contig, scaffolding, hybrid-assembly, sequencing-by-hybridization, sequencing-coverage, kmer-spectrum]
sources:
  - paper: doi:10.1016/0304-3975(92)90143-4
    title: Esko Ukkonen, Approximate string-matching with q-grams and maximal matches, Theoretical Computer Science 92(1) (1992)
    locator: pp. 191 to 211 (the condition on interleaved and triple repeats under which two strings have the same q-grams)
  - paper: doi:10.1186/1471-2105-14-S5-S18
    title: Guy Bresler, Ma'ayan Bresler and David Tse, Optimal assembly for high throughput shotgun sequencing, BMC Bioinformatics 14(Suppl 5) S18 (2013)
    locator: definitions of repeats, interleaved and triple repeats and bridging; Theorem 1 (lower bound), Theorems 3 to 6 (sufficient conditions for DEBRUIJN, SIMPLEBRIDGING and MULTIBRIDGING)
  - paper: doi:10.1073/pnas.171285098
    title: Pavel A. Pevzner, Haixu Tang and Michael S. Waterman, An Eulerian path approach to DNA fragment assembly, PNAS 98(17) (2001)
    locator: pp. 9748 to 9753, sections Eulerian Superpaths and EULER with Clone-End Data (tangles, read-paths, mate-reads)
---

Repeat resolution is the part of genome assembly that decides how the copies of a [repeat](/genome-repeat/) connect to the rest of the genome. A [de Bruijn graph](/de-bruijn-graph/) merges all copies of a repeat longer than $k$ into one path, so the graph shows which sequences enter the repeat and which leave it, but not which entrance goes with which exit. Three kinds of data can decide: reads that span a repeat copy (read paths), [read pairs](/paired-end-reads/) whose two ends lie on the two sides, and coverage, which estimates how many copies a repeat has. A result of Ukkonen and its form for shotgun reads by Bresler, Bresler and Tse say exactly when the data cannot decide: if a pair of interleaved repeats or a triple repeat has no copy spanned by a read, another genome explains the reads equally well.

## In plain words

Suppose the genome contains the same stretch $X$ twice. The assembly graph has one copy of $X$, with two roads in and two roads out. To write the genome you must pair each road in with a road out. A read that runs from a road in, across all of $X$, to a road out shows one pairing. A read pair with one end on each side shows the same thing over a longer distance. The amount of coverage on $X$ shows how many times you must go through it.

Some repeats cannot be resolved by any method. If two repeats alternate, or one repeat occurs three times, and no read crosses any copy, you can swap two parts of the genome and get a different genome that gives exactly the same reads.

## Definition

The genome $S$ is a string. A **repeat** of length $\ell$ is a string $X$ with $|X| = \ell$ that occurs at two positions $t_1 < t_2$ of $S$ and is maximal: the letters before the two copies differ, and the letters after them differ. A **triple repeat** occurs at three positions, and neither all three letters before nor all three letters after are equal. Two repeats, one at $t_1 < t_3$ and one at $t_2 < t_4$, are **interleaved** if $t_1 < t_2 < t_3 < t_4$ or $t_2 < t_1 < t_4 < t_3$. A read **bridges** a copy of a repeat if it covers at least one letter on each side of the copy.

In the assembly graph $G$, a repeat longer than $k$ becomes a path that many genome positions share. At its first vertex several edges enter, and at its last vertex several edges leave. The genome is a walk through $G$ that goes through the repeat path once for each copy.

**Repeat resolution.** Given $G$ and the data, find for each repeat its number of copies and the pairing of entrances to exits that the genome uses, or decide that the data do not determine them. A resolution replaces the shared repeat path by one copy per occurrence, each joined to one entrance and one exit. The [Eulerian superpath problem](/eulerian-superpath-problem/) is the exact form of this problem with read-paths as the data.

## Variants

- **By data.** Read paths from long reads ([hybrid assembly](/hybrid-assembly/)), paired ends or mate pairs with a known insert size, coverage, or several of these together.
- **Spectrum only.** The data are the counts of all $q$-mers of $S$, as in [sequencing by hybridization](/sequencing-by-hybridization/). Ukkonen's condition then decides alone.
- **Full or partial.** Resolve all repeats and output one genome, or resolve the bridged repeats and output contigs that stop at the others.
- **Haplotypes.** In a diploid genome, two copies that differ only at a few sites act as near-repeats, and the same tools separate the haplotypes.

## Examples

**Two interleaved repeats.** Take $X = \mathtt{TTAC}$, $Y = \mathtt{AGGT}$, and

$$S = \mathtt{GA}\,X\,\mathtt{CG}\,Y\,\mathtt{TC}\,X\,\mathtt{AC}\,Y\,\mathtt{GC} = \mathtt{GATTACCGAGGTTCTTACACAGGTGC},$$

$$S' = \mathtt{GA}\,X\,\mathtt{AC}\,Y\,\mathtt{TC}\,X\,\mathtt{CG}\,Y\,\mathtt{GC} = \mathtt{GATTACACAGGTTCTTACCGAGGTGC}.$$

The copies of $X$ and $Y$ alternate, and $S'$ swaps the pieces $\mathtt{CG}$ and $\mathtt{AC}$ between them. Both strings have length 26. They have the same multiset of substrings of each length $q \le 5$, and different ones for $q = 6$. So the set of all reads of length 5 is the same for both genomes, and reads of length 6 tell them apart: a read of length 6 that covers $X$ with one letter on each side bridges that copy.

**A triple repeat.** With $X = \mathtt{TTAC}$,

$$T = \mathtt{GA}\,X\,\mathtt{CG}\,X\,\mathtt{AT}\,X\,\mathtt{GC}, \qquad T' = \mathtt{GA}\,X\,\mathtt{AT}\,X\,\mathtt{CG}\,X\,\mathtt{GC},$$

that is $\mathtt{GATTACCGTTACATTTACGC}$ and $\mathtt{GATTACATTTACCGTTACGC}$. Again the $q$-mer multisets agree for $q \le 5$ and differ for $q = 6$.

**A repeat that is not a problem.** If $S = A\,X\,B\,X\,C$ with only one repeat with two copies, the walk enters $X$ from $A$, must leave to $B$ (leaving to $C$ ends the walk with $B$ unused), comes back from $B$ and leaves to $C$. The graph has one Eulerian path, so a single repeat with two copies needs no data to resolve in a linear genome.

**Coverage gives the copy number.** Suppose the unique unitigs around a repeat have a mean $k$-mer count near 20 and the repeat unitig has a mean count of 61. The best guess is 3 copies. The guess is uncertain when coverage is uneven or the repeat is short, because the mean over few $k$-mers varies more.

**How often a copy is bridged.** With $N$ reads of length $L$ that start at uniform positions in a genome of length $G$, a copy of length $\ell$ is bridged if a read starts in one of the $L - \ell - 1$ positions before it. The probability that no read does is close to $e^{-N(L - \ell - 1)/G}$. For coverage $NL/G = 30$ and $L = 100$:

| repeat length $\ell$ | $N(L - \ell - 1)/G$ | probability that one copy is unbridged |
|---|---|---|
| 80 | 5.7 | 0.0033 |
| 95 | 1.2 | 0.30 |
| 99 or more | 0 | 1 |

## Known algorithms

- **Read threading.** Map each read to its path in the graph. If the read paths that enter a repeat from one edge all leave on the same edge, split the repeat vertex or edge and join that pair. EULER does this with its x,y-detachments. Bresler, Bresler and Tse's SIMPLEBRIDGING duplicates the nodes of bridged repeats with two copies, and MULTIBRIDGING resolves a repeat node when the reads bridge enough of its copies.
- **Read pairs.** If one read of a pair maps to an entrance edge and the other to an exit edge, and the distance through the repeat matches the insert size, the pair supports that pairing. EULER-DB turns such a pair into a mate-read, an artificial long read, when exactly one path between the two reads has a length that matches the clone length.
- **Coverage.** Estimate the copy number of each unitig from its mean count divided by the count of unique unitigs, and use it as the multiplicity of the edge.
- **Larger $k$.** A repeat shorter than $k - 1$ does not merge in the graph. IDBA builds a series of graphs with growing $k$. MULTIBRIDGING has the same effect locally, without a global change of $k$.
- **Stop at the repeat.** If no method decides, output the unique parts as [contigs](/contig/) and leave the repeat for [scaffolding](/scaffolding/) or for a later step with longer reads.

## Bounds

**Theorem (swap).** Let $q \ge 2$, and let $X$ and $Y$ be strings of length at least $q - 1$. Then the strings $S = A X B Y C X D Y E$ and $S' = A X D Y C X B Y E$ have the same multiset of substrings of length $q$, and so do $T = A X B X C X D$ and $T' = A X C X B X D$.

*Proof.* For strings $\alpha$ and $\beta$ such that the last $q - 1$ letters of $\alpha$ equal the first $q - 1$ letters of $\beta$, let $\alpha \odot \beta$ be $\alpha$ followed by $\beta$ without its first $q - 1$ letters. A window of length $q$ in $\alpha \odot \beta$ cannot contain both the letter before the overlap and the letter after it, so it lies inside $\alpha$ or inside $\beta$. So the $q$-mer multiset of $\alpha \odot \beta$ is the sum of those of $\alpha$ and $\beta$. Let $x$ and $y$ be the first $q - 1$ letters of $X$ and of $Y$. Then

$$S = Ax \odot XBy \odot YCx \odot XDy \odot YE, \qquad S' = Ax \odot XDy \odot YCx \odot XBy \odot YE,$$

and each $\odot$ is defined because each middle piece starts with $x$ or $y$ and the piece before it ends with the same string. The two products use the same five pieces, so they have the same $q$-mer multiset. In the same way $T = Ax \odot XBx \odot XCx \odot XD$ and $T' = Ax \odot XCx \odot XBx \odot XD$. $\square$

The two strings can be different, as in the examples above. So reads of length $L$ cannot separate $S$ and $S'$ when both repeats have length at least $L - 1$, at any coverage. This is Ukkonen's condition: interleaved repeats or a triple repeat of length at least $L - 1$ make reconstruction from the $L$-mers impossible. Bresler, Bresler and Tse write the resulting bound as $L > L_{crit} = \max(\ell_{interleaved}, \ell_{triple}) + 1$, where $\ell_{interleaved}$ is the length of the shorter repeat in the longest interleaved pair and $\ell_{triple}$ is the length of the longest triple repeat.

**Lower bound with bridging.** Bresler, Bresler and Tse prove that if all copies of a pair of interleaved repeats, or of a triple repeat, are unbridged, there is another sequence of the same length under which the reads have the same likelihood (Theorem 1). So when this event occurs, any method is wrong with probability at least $1/2$. With the bridging probability above, this gives a lower bound on the number of reads.

**Upper bounds.** In the same paper, if there are no interleaved or triple repeats of length at least $K$, the condensed $K$-mer graph of the $(K+1)$-mers has a unique Eulerian cycle, which spells $S$ (Theorem 3). MULTIBRIDGING reconstructs $S$ if all interleaved repeats are bridged, all copies of each triple repeat are bridged, and the reads cover $S$ (Theorem 6). The necessary condition asks for one bridged copy of a triple repeat, and the sufficient condition asks for all of them, so a gap remains for triple repeats.

**Copy number from coverage.** Coverage alone does not give the order: in the examples above, both genomes have the same copy numbers. It only fixes $\mu$, and with $\mu$ fixed the read-path problem is still NP-hard in general, by the hardness of the [Eulerian superpath problem](/eulerian-superpath-problem/) with multiplicities.

## Reductions

- **To the [Eulerian superpath problem](/eulerian-superpath-problem/).** Read paths and mate-reads become the path system, coverage gives the multiplicities, and a solution is a full resolution.
- **To [scaffolding](/scaffolding/).** Repeats that stay unresolved become gaps between contigs, and read pairs that jump over them order the contigs.
- **From the $q$-mer spectrum.** The spectrum form is the reconstruction question of [sequencing by hybridization](/sequencing-by-hybridization/). The swap theorem shows the ambiguity in both settings.

## Applications

Repeat resolution decides how long the contigs of a short-read assembly can get, because contigs end at the repeats that stay unresolved. The *N. meningitidis* genome has 126 long nearly perfect repeats. With clone-end pairs, EULER-DB reduced its contigs from 149 to 91 and left 5 unresolved tangles, each longer than the clone inserts. [Hybrid assembly](/hybrid-assembly/) uses long reads to bridge repeats that short reads cannot. Bresler, Bresler and Tse use the bounds to compare assemblers with the best possible coverage for given read lengths and repeat statistics.

## References
