---
tag: 5HMHYS
kind: algorithm
slug: umi-deduplication
name: UMI deduplication
aliases:
- directional UMI network
- UMI collapsing
area: biology/transcriptomics
level: core
summary: Count molecules, not reads, by grouping reads by cell and locus and merging UMIs one substitution apart when the count of one is at least about twice the other.
model: word-ram
complexity:
  vars: {n: the number of reads, m: the number of distinct UMIs over all bundles, l: the UMI length}
  time: {worst: O(n + m^2 l)}
  space: {extra: O(m l)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2017
  people: [Tom Smith, Andreas Heger, Ian Sudbery]
  note: Kivioja et al. (2012) and Islam et al. (2014) counted molecules by their UMIs. Smith, Heger and Sudbery (2017) added the directional network in UMI-tools to merge UMIs with sequencing and PCR errors.
prereqs: [hamming-distance, breadth-first-search]
see_also: [single-cell-rna-sequencing, duplicate-read-marking, connected-components, hamming-distance, breadth-first-search, hash-table, read-mapping, pseudoalignment]
sources:
  - paper: doi:10.1101/gr.209601.116
    title: Tom Smith, Andreas Heger and Ian Sudbery, UMI-tools, modeling sequencing errors in Unique Molecular Identifiers to improve quantification accuracy, Genome Research 27(3) (2017), 491-499
    locator: the unique, cluster, adjacency and directional methods, and the directional edge rule n(a) >= 2 n(b) - 1 at Hamming distance 1
  - paper: doi:10.1038/nmeth.1778
    title: Teemu Kivioja et al., Counting absolute numbers of molecules using unique molecular identifiers, Nature Methods 9(1) (2012), 72-74
    locator: the use of random molecular labels to count molecules after PCR
  - paper: doi:10.1038/nmeth.2772
    title: Saiful Islam et al., Quantitative single-cell RNA-seq with unique molecular identifiers, Nature Methods 11(2) (2014), 163-166
    locator: UMIs in single-cell RNA-seq
---

UMI deduplication counts the molecules behind a set of sequencing reads. Before PCR, each cDNA molecule gets a short random tag, the unique molecular identifier (UMI). All PCR copies of a molecule then carry the same UMI and map to the same place, so the number of distinct UMIs at a locus estimates the number of molecules, not the number of copies. Errors in PCR and in sequencing change some UMIs, and each changed UMI looks like a new molecule. The directional method of UMI-tools (Smith, Heger and Sudbery 2017) joins a UMI to a neighbor that differs at one position when the neighbor has at least about twice as many reads, and it counts the groups that this makes. It is the default of UMI-tools and the method behind the cell by gene count matrices of [single-cell RNA-seq](/single-cell-rna-sequencing/). It differs from [duplicate read marking](/duplicate-read-marking/), which has no UMIs and can use only the mapping position of each read.

## In plain words

Each molecule gets a random name before it is copied many times. To count the molecules, count the names. The problem is that some copies get a misspelled name, and a misspelled name looks like a new molecule. A misspelling usually changes one letter, and it is usually rare: the true name has many reads, and the misspelled one has few. So link two names that differ in one letter when one of them has at least about twice as many reads. Start from the most common name, follow the links to the rarer names, and call everything you reach one molecule. Then take the most common name that is left and do the same. Two names that differ in one letter but have similar counts stay apart, because they are probably two real molecules.

## The problem

**Input.** Reads $(c, x, u)$, each with a cell barcode $c$, a locus $x$ and a UMI $u$, a string of length $l$. For bulk data the locus is a mapping position and strand; for droplet single-cell data it is the gene that the read maps to. The reads with the same $(c, x)$ form a bundle, and $n(u)$ is the number of reads with UMI $u$ in the bundle.

**Output.** For each bundle, an estimate of the number of distinct molecules, and a partition of its UMIs into groups, one group for each molecule, with the UMI that stands for it.

**Model.** Every molecule has its own UMI. A read shows the UMI of its molecule, or a copy with one or more substitutions. The task has no exact solution: two real molecules can have UMIs one letter apart, and an error can turn one UMI into another real one. The directional method is a heuristic for this model.

## The algorithm

```pseudo id=main
DIRECTIONAL-DEDUP(reads)                    ▷ reads: (cell, locus, UMI) triples
L1  n[b][u] ← the number of reads of bundle b = (cell, locus) with UMI u
L2  for each bundle b do
L3      U ← the UMIs of b by decreasing n[b][u], ties by the UMI string
L4      for each pair u, v of U with hamming(u, v) = 1 do
L5          add the arc u → v if n[b][u] ≥ 2 n[b][v] - 1
L6      T ← ∅                                ▷ the UMIs taken by earlier groups
L7      for each u in U, in order do
L8          if u ∈ T then skip u
L9          R ← the UMIs reached from u by breadth-first search along the arcs
L10         make R \ T a group with representative u; T ← T ∪ R
L11     molecules[b] ← the number of groups of b
L12 return molecules
```

Line L1 groups the reads into bundles. Lines L4 and L5 build the directed graph. The rule $n(u) \ge 2n(v) - 1$ says that $u$ has at least about twice the reads of $v$. For $n(v) = 1$ it allows $n(u) = 1$, so two single reads one letter apart join in both directions. Lines L7 to L10 take the UMIs from the most common down. Each UMI that no earlier group holds starts a [breadth-first search](/breadth-first-search/), and the UMIs it reaches that are still free form one group. Line L11 counts the groups.

UMI-tools has three other methods on the same graph of [Hamming distance](/hamming-distance/) 1. "Unique" counts each distinct UMI as a molecule. "Cluster" counts the [connected components](/connected-components/) of the undirected graph. "Adjacency" takes each component and removes, from the most common UMI down, the UMI and its direct neighbors, until the component is covered. The directional method lies between "cluster", which merges too much when UMIs are dense, and "unique", which keeps every error. The code has "unique", "cluster" and "directional".

## Example

One bundle has six UMIs of length 4.

| UMI | reads | arcs out (line L5) |
|---|---|---|
| ACGT | 50 | ACGA, ACGC, TCGT |
| ACGA | 20 | ACGC |
| TCGA | 18 | TCGT |
| GGGG | 5 | none |
| ACGC | 2 | none |
| TCGT | 1 | none |

ACGT and ACGA differ at the last position, and $50 \ge 2 \cdot 20 - 1 = 39$, so there is an arc ACGT → ACGA. ACGA and TCGA also differ at one position, but $20 < 2 \cdot 18 - 1$ and $18 < 2 \cdot 20 - 1$, so there is no arc in either direction. TCGT is one letter from both ACGT and TCGA, and both point to it.

The visit order is ACGT, ACGA, TCGA, GGGG, ACGC, TCGT. The search from ACGT reaches ACGA, ACGC and TCGT, which form the first group. ACGA is now taken. TCGA starts a search that reaches TCGT, but TCGT is taken, so the second group is TCGA alone. GGGG is the third group, and the last two UMIs are taken. The bundle has 3 molecules, with representatives ACGT, TCGA and GGGG.

The other methods give other counts. "Unique" gives 6. "Cluster" gives 2, because ACGA, TCGA and TCGT link ACGT and TCGA into one component, even though their counts of 50 and 18 suggest two molecules.

## Correctness

The [proof](proofs/correctness.md) shows four facts. Counts never increase along an arc, and they stay equal only between two UMIs with one read each. The groups partition the UMIs of the bundle, and the UMI that starts a group has the highest count in it. The number of groups is at least the number of connected components and at most the number of distinct UMIs. Last, under a model of errors the method is exact: if the true UMIs differ pairwise in at least 4 positions, each other UMI is one substitution from a true UMI, and each true UMI has at least $2n - 1$ reads for each of its error UMIs with $n$ reads, then each group is one true UMI with its errors. A read with two errors is two positions from its UMI and is always counted as an extra molecule. On real data the count is an estimate, and the error rate it reaches is a measurement.

## Complexity

On a [word RAM](/word-ram/), line L1 takes $O(n)$ expected time with a [hash table](/hash-table/). For a bundle with $m_b$ distinct UMIs, comparing all pairs at line L4 takes $\Theta(m_b^2 l)$ time. This is what UMI-tools does, and over all bundles it is at most $O(m^2 l)$. In place of the pairs, one can look up the $3l$ substitution variants of each UMI in a hash table, in $O(m_b l^2)$ expected time; the code has both. Each search at line L9 takes time linear in the part of the graph it reaches, and in the worst case the searches together take $O(m_b^2 l)$. The extra space is $O(m l)$ for the counts and the arcs, since a UMI has at most $3l$ neighbors over the alphabet ACGT.

## Properties

- **Deterministic.** With the tie rule of line L3, the groups depend only on the counts.
- **Between two simple methods.** The count is never below the number of components and never above the number of distinct UMIs.
- **The representative is the most common UMI** of its group.
- **One step at a time.** An arc joins UMIs one substitution apart, and a path can join UMIs several substitutions apart, but only along falling counts.
- **Local to a bundle.** Bundles are independent, so they can run in parallel.

## Variants and improvements

- **Threshold.** UMI-tools has an edit distance threshold, 1 by default. A larger threshold joins reads with two errors and also joins more real molecules.
- **Adjacency method.** Removes the most common UMI and its direct neighbors at each step. It does not follow paths of falling counts.
- **Cell barcode correction.** The same idea, a graph of one-letter differences weighted by counts, also corrects errors in cell barcodes. Tools such as UMI-tools whitelist and the 10x Genomics pipeline use a known list of barcodes for this.
- **Gene as locus.** For droplet data the bundle is (cell, gene) after the reads are assigned to genes, so reads of one molecule at different positions count once.
- **Insertions and deletions.** The Hamming distance sees only substitutions. An edit distance version finds UMIs with an indel, at a higher cost.

## When to use it

Use it on any data with UMIs: droplet and plate single-cell RNA-seq, and UMI-tagged bulk or targeted sequencing. It is the default of UMI-tools, and pipelines for droplet data apply methods of the same kind. Without UMIs, use [duplicate read marking](/duplicate-read-marking/) by position, which cannot tell true duplicates from two molecules that start at the same place. When the number of molecules per bundle is close to the number of possible UMIs, $4^l$, no method can separate the molecules well, and a longer UMI is the fix.

## Pitfalls

- **Short UMIs saturate.** With many molecules and short UMIs, real UMIs are often one letter apart, and they are then merged when their counts differ by a factor of two or more. With 6-base UMIs and 150 molecules in one bundle this already costs about one molecule in ten.
- **Errors with two substitutions** stay separate and inflate the count.
- **Different UMI lengths** in one bundle give no Hamming distance; trim or split them first.
- **Bundles must be right.** Reads of one molecule that map to two positions, or to two genes, are counted twice. Reads of two molecules in one bundle with equal UMIs are counted once.
- **Counts of 1.** Two UMIs with one read each and one letter apart join in both directions, so the result for them depends on the tie rule.

## Implementations

## History

Kivioja et al. (2012) showed that random molecular labels attached before PCR let one count molecules in place of reads. Islam et al. (2014) used UMIs in single-cell RNA-seq, and droplet methods such as Drop-seq (Macosko et al. 2015) put a cell barcode and a UMI on every bead. Early tools counted distinct UMIs. Smith, Heger and Sudbery (2017) showed that errors in UMIs inflate these counts and proposed the network methods of UMI-tools, with the directional method as the default.

## References
