---
tag: QSDF24
kind: concept
slug: genome-repeat
name: Genome repeat
aliases:
- repeated sequence
area: biology/genome-assembly
level: intro
summary: A sequence that occurs more than once in a genome. A repeat longer than the reads, with no read or pair to span it, makes the assembly ambiguous.
prereqs: [shotgun-sequencing, kmer]
see_also: [genome-assembly-problem, repeat-resolution, paired-end-reads, kmer-spectrum, de-bruijn-graph, maximal-repetition, sequencing-coverage, scaffolding]
sources:
  - paper: doi:10.1038/nrg3117
    title: Todd J. Treangen and Steven L. Salzberg, Repetitive DNA and next-generation sequencing, computational challenges and solutions, Nature Reviews Genetics 13(1) (2012)
    locator: pp. 36 to 46 (the classes of repeats and their effect on assembly and alignment)
  - paper: doi:10.1038/nrg3367
    title: Niranjan Nagarajan and Mihai Pop, Sequence assembly demystified, Nature Reviews Genetics 14(3) (2013)
    locator: pp. 157 to 167 (repeats and the assembly graph)
  - paper: doi:10.1186/1471-2105-11-21
    title: Carl Kingsford, Michael C. Schatz and Mihai Pop, Assembly complexity of prokaryotic genomes using short reads, BMC Bioinformatics 11 (2010)
    locator: Article 21 (the repeats that block reconstruction in 375 prokaryotes)
  - paper: doi:10.1186/1471-2105-14-S5-S18
    title: Guy Bresler, Ma'ayan Bresler and David Tse, Optimal assembly for high throughput shotgun sequencing, BMC Bioinformatics 14(Suppl 5) (2013)
    locator: Article S18 (interleaved and triple repeats and the critical read length)
  - paper: doi:10.1016/0304-3975(92)90143-4
    title: Esko Ukkonen, Approximate string-matching with q-grams and maximal matches, Theoretical Computer Science 92(1) (1992)
    locator: pp. 191 to 211
---

A genome repeat is a stretch of DNA that occurs two or more times in a genome, exactly or with a few differences. Repeats are the main reason that [genome assembly](/genome-assembly-problem/) is hard. A read that lies inside a repeat fits every copy, so when no read or read pair spans a repeat, the reads do not tell how the regions around the copies are joined. More reads do not help: the fix is longer reads, [paired reads](/paired-end-reads/) with a longer span, or other data.

## In plain words

A street has many houses that look the same. You get photos of small parts of the street, each a few meters wide, and you must draw the whole street from them. A photo of one plain door does not tell you which of the identical houses it shows. If a photo is wide enough to show the plain house *and* the two different houses beside it, you know where it goes. If every photo is narrower than the plain houses, you can draw the parts between them, but not their order.

DNA has many such repeated passages. Some are short words repeated side by side many times. Some are long pieces that copy themselves to new places. A repeat is a problem only when it is longer than what one read, or one pair of reads, can span.

## The idea

### What counts as a repeat

Let $S$ be a genome of length $G$. A string $X$ is a **repeat** of $S$ if it occurs at two or more positions of $S$, or of $S$ and its reverse complement $\overline{S}$. The copies can be:

- **Direct**, on the same strand, or **inverted**, one copy on each strand.
- **Exact**, or **approximate**, with a few substitutions or indels between copies. Old repeats differ more than young ones, because the copies mutate independently.
- **Tandem**, side by side ($XXX\ldots$), or **interspersed**, far apart.

For assembly, the length that matters is the length of the longest exact (or nearly exact) part, because that is the part that reads cannot place.

A random string has short repeats by chance. A string of length $G$ over four letters has about $\binom{G}{2} / 4^{\ell} \approx G^2 / (2 \cdot 4^{\ell})$ pairs of equal $\ell$-mers. This number falls below 1 at $\ell \approx 2 \log_4 G - 0.5$: about 22 for $G = 5 \times 10^6$, and about 31 for $G = 3.1 \times 10^9$. Real genomes have repeats of thousands of bases. These are not chance: they come from biology.

### Classes of repeats

Treangen and Salzberg sort the repeats that matter for sequencing into a few classes.

- **Tandem repeats.** A short unit repeated side by side. Microsatellites have units of a few bases, minisatellites longer units, and satellites at centromeres span long regions. The number of copies often differs between individuals.
- **Transposable elements.** Pieces of DNA that copy or move themselves to new places in the genome. They include short interspersed elements (SINEs, such as Alu in primates, about 300 bases), long interspersed elements (LINEs, such as L1), retrotransposons with long terminal repeats, and DNA transposons. A young family has many nearly identical copies.
- **Segmental duplications.** Large blocks of the genome that were copied to another place, with high identity between the copies.
- **Multi-copy genes.** Genes present in several copies, such as the ribosomal RNA operons of bacteria, several kilobases long.

About half of the human genome is repetitive. Bacteria have fewer repeats, but the rRNA operons and insertion sequences are often longer than short reads.

### Why repeats make assembly ambiguous

In a [de Bruijn graph](/de-bruijn-graph/) of [k-mers](/kmer/), all copies of a repeat longer than $k$ collapse into one path. The path has several edges in, from the regions before the copies, and several edges out, to the regions after them. A walk through the graph must choose which way out to take after each way in. The reads give the answer only if some read covers the repeat and one base on each side: then the read *bridges* the repeat and links one way in to one way out.

Not every unbridged repeat is ambiguous. With two copies of $X$ in the order $A\,X\,B\,X\,C$, the walk from $A$ must go through $X$ to $B$ first: if it went to $C$, it could not come back to use $B$. Ambiguity needs a choice that keeps the walk valid. There are two basic patterns:

- **A triple repeat**, $A\,X\,B\,X\,C\,X\,D$: the walk can visit $B$ and $C$ in either order.
- **Interleaved repeats**, $A\,X\,B\,Y\,C\,X\,D\,Y\,E$: the stretches $B$ and $D$ can swap.

Ukkonen's condition states that if a genome has a triple repeat, or an interleaved pair of repeats, of length at least $L - 1$, reads of length $L$ cannot fix the genome. Bresler, Bresler and Tse take the longest such repeats to define the critical read length of a genome. In 375 prokaryotes, Kingsford, Schatz and Pop found that most genes can be rebuilt from short reads even when the whole genome cannot, and that the genes that cannot are mostly in mobile elements.

### What a repeat does to an assembly

- **A break.** The assembler stops the [contig](/contig/) at the start of the repeat, because the way out is not known. The repeat copy becomes a separate contig.
- **A collapse.** All copies of the repeat become one contig. Its read depth is about $m$ times the usual [coverage](/sequencing-coverage/) for $m$ copies, which is how assemblers spot it. The number of copies of a tandem repeat is often wrong.
- **A misjoin.** The assembler guesses a way out and joins two regions that are not neighbors in the genome. This is the worst result, because the contig looks fine.

### What resolves a repeat

- **Longer reads.** A read longer than the repeat, with unique bases on both sides, bridges it.
- **Paired reads.** A [read pair](/paired-end-reads/) with one read in the unique region before a repeat and the other read after it links the two sides, if the insert is longer than the repeat.
- **Depth.** The depth of a collapsed contig estimates the copy number.
- **Graph methods.** [Repeat resolution](/repeat-resolution/) in the assembly graph uses read paths and pairs to split the collapsed path into its copies.

## Examples

**A two-copy repeat that is not ambiguous.** Let $X = \texttt{GATTACA}$ and $S = \texttt{TC}\,X\,\texttt{CC}\,X\,\texttt{GG}$. The 4-mers of $S$ fix it: $S$ is the only string with the same multiset of 4-mers. A walk must pass $X$, then CC, then $X$ again, then GG. There is no second way through, although the repeat is longer than the 4-mers.

**A triple repeat that is.** With a third copy, $S_1 = \texttt{TC}\,X\,\texttt{CC}\,X\,\texttt{TGT}\,X\,\texttt{GG}$ and $S_2 = \texttt{TC}\,X\,\texttt{TGT}\,X\,\texttt{CC}\,X\,\texttt{GG}$ have the same multiset of k-mers for every $k$ from 3 to 8 and differ for $k \ge 9$. Here $|X| = 7$, so the condition "repeat length at least $L - 1$" holds exactly for $L \le 8$.

**Interleaved repeats.** With $X = \texttt{ACGTA}$ and $Y = \texttt{TTGAC}$, the genomes $\texttt{C}X\texttt{G}Y\texttt{CA}X\texttt{TT}Y\texttt{G}$ and $\texttt{C}X\texttt{TT}Y\texttt{CA}X\texttt{G}Y\texttt{G}$ have the same k-mers for $k \le 6$ and differ for $k \ge 7$. Each repeat has length 5, and $5 \ge L - 1$ exactly for $L \le 6$.

**A tandem repeat.** In $\texttt{CATG}\,UUU\,\texttt{GTCA}$ with $U = \texttt{ACGTTGCA}$, every read of length 6 also occurs in $\texttt{CATG}\,UU\,\texttt{GTCA}$. Reads of length 6 cannot tell three copies of $U$ from two. A shortest superstring keeps too few copies.

**Repeats in the k-mer spectrum.** A k-mer in a repeat with $m$ copies occurs about $m$ times as often as a k-mer from a unique region. In the [k-mer spectrum](/kmer-spectrum/) of a genome with repeats, extra peaks appear at $2c_k$, $3c_k$ and so on, where $c_k$ is the k-mer coverage.

## Where it is used

- Choosing the read length and insert sizes of a sequencing project. The longest repeats that must be spanned set the needs.
- [Genome assembly](/genome-assembly-problem/): every assembler has a step that finds repeat regions and either breaks contigs there or resolves them.
- [Read mapping](/read-mapping/): a read from a repeat maps to several places equally well, and the mapper reports a low mapping quality.
- Repeat masking before gene annotation and before [k-mer](/kmer/) based seeding, so that seeds in repeats do not flood the search.
- Assembly quality: collapsed repeats and misjoins at repeats are the main errors that [assembly quality assessment](/assembly-quality-assessment/) looks for.

## References
