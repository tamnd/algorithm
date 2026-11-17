---
tag: 6KKBA9
kind: algorithm
slug: pseudoalignment
name: Pseudoalignment
aliases:
- kallisto pseudoalignment
- read equivalence classes
area: biology/transcriptomics
level: advanced
summary: 'Find the set of transcripts compatible with a read by intersecting the colors of its k-mers in a transcriptome de Bruijn graph, skipping along contigs, with no base-level alignment.'
solves: [transcript-abundance-estimation]
model: word-ram
complexity:
  vars: {L: the read length, k: the k-mer length, m: the number of transcripts, n: the total length of the transcripts}
  time: {worst: O(L·(k+m))}
  space: {extra: O(n·(k+m))}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2016
  people: [Nicolas L. Bray, Harold Pimentel, Páll Melsted, Lior Pachter]
  note: kallisto replaced alignment by the set of transcripts whose k-mers a read holds, found in a colored de Bruijn graph of the transcriptome with skips along contigs, and ran the EM on the counts of these sets.
prereqs: [transcript-abundance-estimation, kmer, de-bruijn-graph]
see_also: [em-isoform-quantification, selective-alignment, kmer-index, unitig, hash-table, read-mapping, single-cell-rna-sequencing, bootstrap-method]
sources:
  - paper: doi:10.1038/nbt.3519
    title: Nicolas L. Bray, Harold Pimentel, Páll Melsted and Lior Pachter, Near-optimal probabilistic RNA-seq quantification, Nature Biotechnology 34(5) (2016)
    locator: pp. 525 to 527 and Online Methods (the transcriptome de Bruijn graph, k-compatibility classes, skipping along contigs, and the EM on equivalence classes)
  - paper: doi:10.1038/ng.1028
    title: Zamin Iqbal, Mario Caccamo, Isaac Turner, Paul Flicek and Gil McVean, De novo assembly and genotyping of variants using colored de Bruijn graphs, Nature Genetics 44(2) (2012)
    locator: pp. 226 to 232 (the colored de Bruijn graph)
  - paper: doi:10.1038/nbt.2862
    title: Rob Patro, Stephen M. Mount and Carl Kingsford, Sailfish enables alignment-free isoform quantification from RNA-seq reads using lightweight algorithms, Nature Biotechnology 32(5) (2014)
    locator: pp. 462 to 464 (quantification from k-mer counts without alignment)
  - paper: doi:10.1038/nmeth.4197
    title: Rob Patro, Geet Duggal, Michael I. Love, Rafael A. Irizarry and Carl Kingsford, Salmon provides fast and bias-aware quantification of transcript expression, Nature Methods 14(4) (2017)
    locator: pp. 417 to 419 (equivalence classes in a lightweight mapping method)
  - paper: doi:10.1186/s13059-020-02151-8
    title: Avi Srivastava, Laraib Malik, Hirak Sarkar, Mohsen Zakeri, Fatemeh Almodaresi, Charlotte Soneson, Michael I. Love, Carl Kingsford and Rob Patro, Alignment and mapping methodology influence transcript abundance estimation, Genome Biology 21 (2020)
    locator: Article 239 (where reads mapped without alignment go wrong)
---

Pseudoalignment finds, for each read, the set of transcripts that the read is compatible with, and nothing more: not the position, not the alignment. In kallisto, introduced by Bray, Pimentel, Melsted and Pachter (2016), the compatible set is the intersection of the colors of the read [k-mers](/kmer/), where the color of a k-mer is the set of transcripts that hold it. The k-mers are the nodes of a [de Bruijn graph](/de-bruijn-graph/) of the transcriptome, and the graph is cut into contigs whose k-mers all have one color, so after one lookup the algorithm can jump to the end of a contig and check only one k-mer there. Reads with the same set form an equivalence class, and the class counts are all that the [EM](/em-isoform-quantification/) of abundance estimation needs. On reads whose k-mers are all in the index, the skips give exactly the intersection of all the colors; on other reads they give a superset of it.

## In plain words

Make a list of every short word of a fixed length that occurs in any transcript, and write next to each word the transcripts that contain it. To place a read, cut it into words and look each one up. A transcript that the read came from must contain all of the words, so keep only the transcripts that are on every list.

Looking up every word is slow. But many words follow each other in long chains, and inside a chain the lists are all the same. So after one word, jump to the end of its chain, check that the read still agrees there, and skip the words in between.

The answer is a set of transcripts, not a place. Reads with the same answer are counted together.

## The problem

The input is a set of $m$ transcripts, a k-mer length $k$, and reads. Let $K$ be the set of k-mers of the transcripts and of their reverse complements, so that reads from both strands are found. The color $\mathrm{col}(x)$ of $x \in K$ is the set of transcripts that hold $x$ on either strand. For a read $R$ of length $L$, the task is the set

$$\mathrm{Naive}(R) = \bigcap_{i \,:\, R[i..i+k-1] \in K} \mathrm{col}(R[i..i+k-1]),$$

the transcripts that hold every k-mer of the read that is in the index, or the empty set if no k-mer of the read is in the index. Kallisto calls it the k-compatibility class of the read. The reads are then grouped by this set into equivalence classes with counts, which is the input of [abundance estimation](/transcript-abundance-estimation/).

The index joins the k-mers into contigs. There is an edge from $x$ to $y$ when the last $k - 1$ letters of $x$ are the first $k - 1$ letters of $y$. A contig $c = (c_1, \ldots, c_{|c|})$ is a maximal run in which each $c_j$ has exactly one successor in $K$, which is $c_{j+1}$, $c_{j+1}$ has exactly one predecessor, and both have the same color. Contigs are the [unitigs](/unitig/) of the graph, cut further where the color changes. Each k-mer is stored in a [hash table](/hash-table/) with its contig and its position in the contig.

## The algorithm

Positions are 1-based in the text and 0-based in the code.

```pseudo id=main
PSEUDOALIGN(read R of length L, an index of k-mers with contig, position and color)
L1  E ← undefined
L2  i ← 1
L3  while i ≤ L - k + 1 do
L4      x ← R[i .. i + k - 1]
L5      if x is in the index then
L6          (c, p) ← the contig and position of x; E ← col(c) if E is undefined, else E ∩ col(c)
L7          d ← min(|c| - p, L - k + 1 - i)
L8          if d > 0 and R[i + d .. i + d + k - 1] = c_{p+d} then i ← i + d + 1 else i ← i + 1
L9      else i ← i + 1
L10 return E, or the empty set if E is undefined
```

Lines L4 to L6 look up one k-mer and intersect its color. Line L7 computes how far the read can still follow the contig: to the end of the contig or to the end of the read, whichever comes first. Line L8 checks the k-mer at that distance. Inside a contig every k-mer has only one successor, so a read whose k-mers are all in the index must follow the contig, and the check passes. Then all the k-mers in between have the color already intersected, and the loop skips them. If the check fails, the read has left the contig or has an error, and the loop goes on one k-mer at a time. Line L9 steps over a k-mer that is not in the index, for example one that holds a sequencing error.

The code builds the contigs from a dictionary of k-mers. It leaves out what kallisto does for speed and space: canonical k-mers that store both strands once, a compact store of contigs and color classes, read pairs, and the EM, which is on the [EM page](/em-isoform-quantification/).

## Example

The transcripts are $t_1 = X E Y$ and $t_2 = X Y$, with $X = \texttt{CAGAACC}$, $E = \texttt{TGCTGT}$ and $Y = \texttt{GACATAA}$, and $k = 5$. All 5-mers are distinct, so $K$ has 20 k-mers on each strand. The index has 8 contigs, 4 on each strand. The forward ones are:

| contig | k-mers | color |
|---|---|---|
| CAGAACC | 3 | $\{t_1, t_2\}$ |
| AACCTGCTGTGACA | 10 | $\{t_1\}$ |
| AACCGACA | 4 | $\{t_2\}$ |
| GACATAA | 3 | $\{t_1, t_2\}$ |

The contig CAGAACC ends where $X$ ends, because GAACC has two successors, AACCT into $E$ and AACCG into $Y$. The second contig is the end of $X$, all of $E$ and the start of $Y$, which only $t_1$ has. The third is the junction of $X$ and $Y$, which only $t_2$ has.

The read $R = \texttt{AGAACCTGCTGTGACATA}$ is $t_1$ without its first and last two bases. It has $L = 18$ and 14 k-mers.

| $i$ | k-mer | contig, $p$ | $d$ | checked k-mer | E after line L6 | next $i$ |
|---|---|---|---|---|---|---|
| 1 | AGAAC | CAGAACC, 2 | $\min(1, 13) = 1$ | GAACC at 2, equal to $c_3$ | $\{t_1, t_2\}$ | 3 |
| 3 | AACCT | AACCTGCTGTGACA, 1 | $\min(9, 11) = 9$ | TGACA at 12, equal to $c_{10}$ | $\{t_1\}$ | 13 |
| 13 | GACAT | GACATAA, 1 | $\min(2, 1) = 1$ | ACATA at 14, equal to $c_2$ | $\{t_1\}$ | 15, stop |

Three lookups and three checks replace 14 lookups, and the result is $\{t_1\}$. The read $t_2$ itself, of 14 bases, is looked up at positions 1, 4 and 8 and gives $\{t_2\}$. The read $X$ alone gives $\{t_1, t_2\}$, and a read of only T bases gives the empty set. The reverse complement of each read gives the same set, through the contigs of the other strand. The test file checks all of these, with the 0-based positions 0, 2 and 12 for the first read.

## Correctness

[The proof](proofs/correctness.md) first shows that the contigs split $K$, with one color per contig. The key lemma: if $R[i..]$ equals $c_p$ and the next $d$ read k-mers are all in $K$, they are $c_{p+1}, \ldots, c_{p+d}$, because each of these nodes has only one successor in $K$. From this, three theorems follow. The result always contains $\mathrm{Naive}(R)$, because it intersects the colors of a subset of the same k-mers. If every k-mer of the read is in $K$, the result equals $\mathrm{Naive}(R)$, and for an error-free read the source transcript is in it. And in that case the number of lookups is the number of contig visits of the read.

## Complexity

The word RAM, with read length $L$, k-mer length $k$, $m$ transcripts of total length $n$.

- **Index.** $O(n)$ k-mers, each hashed in $O(k)$, with a color of up to $m$ ids. The contigs cost $O(k)$ per k-mer for the four successor and predecessor lookups. That is $O(n (k + m))$ time and space.
- **One read.** At most $L - k + 1$ rounds, each with a lookup and a check of $O(k)$ and an intersection of $O(m)$, so $O(L (k + m))$ in the worst case. When every k-mer is in the index, the rounds are as many as the contig visits, which is often 1 to 3 for a short read.

Kallisto reported the quantification of 30 million reads in a few minutes on one ordinary computer, which is a measurement.

## Properties

- **Not an alignment.** It gives no position, strand or CIGAR. It cannot be used for variant calling or as a SAM file.
- **Exact or a superset.** The result equals the k-mer intersection when every read k-mer is indexed, and is a superset of it otherwise, both theorems. The k-mer intersection is itself only an approximation of the set of transcripts that hold the read.
- **Deterministic and online.** Each read is handled on its own, so reads can be streamed and the work runs in parallel.
- **Robust to errors in a crude way.** A k-mer with an error is usually not in $K$ and is just skipped, so a read with a few errors still gets a set.

## Variants and improvements

- **Canonical k-mers.** Kallisto stores each k-mer and its reverse complement once, as the smaller of the two, and keeps the strand in the contig.
- **Read pairs.** The set of a pair is the intersection of the sets of its two reads.
- **Quasi-mapping and selective alignment.** RapMap and Salmon find the transcripts and the positions of exact matches in an index, and [selective alignment](/selective-alignment/) adds a score to every candidate, which removes many of the false hits that a pure k-mer intersection allows.
- **Single cells.** In [single-cell RNA-seq](/single-cell-rna-sequencing/), pseudoalignment of each read with its barcode and molecule identifier gives counts per cell.
- **Uncertainty.** Kallisto runs the EM again on bootstrap samples of the class counts to estimate the variance; see [bootstrap](/bootstrap-method/).

## When to use it

Use it to quantify the expression of known transcripts, quickly and with little memory, when the transcriptome is good and the sample is not too far from it. It is the method of choice for large studies and for single-cell data. Do not use it when positions or alignments are needed, when new transcripts or junctions are expected, or when the sample has many reads from outside the transcriptome, such as intron reads; there, [selective alignment](/selective-alignment/) with decoys, or [spliced alignment](/spliced-read-alignment/) to the genome, does better. Srivastava and colleagues (2020) measured cases where mapping without alignment scores gave worse abundance estimates than alignment.

## Pitfalls

- **Order is not checked.** A transcript that holds all the read k-mers in another order, or on mixed strands, is in the set. For small $k$ this happens often; kallisto uses $k = 31$.
- **Reads from outside the index.** A read from an intron or from an unannotated gene may share a few k-mers with a transcript and get that transcript as its set. The other k-mers are not in $K$ and are skipped without notice.
- **Skipping over an error.** If a read leaves a contig because of an error and comes back to it at the checked position, the k-mers with the error are skipped. If such a k-mer happens to be in $K$ with another color, the naive set would have been smaller. This is why the result is only a superset in general.
- **An empty intersection.** Two read k-mers with disjoint colors, from an error or from a read across an unannotated junction, give the empty set, and the read is not counted. Many such reads are a sign that the index lacks transcripts of the sample.
- **Contigs must end where colors change.** A unitig whose k-mers have different colors cannot be skipped as a whole. Forgetting to cut there makes the skip wrong.

## Implementations

## History

Iqbal, Caccamo, Turner, Flicek and McVean (2012) introduced the colored de Bruijn graph, which labels each k-mer with the samples that contain it, for variant calling. Patro, Mount and Kingsford (2014) quantified transcripts from k-mer counts in Sailfish, without alignment. Bray, Pimentel, Melsted and Pachter (2016) defined pseudoalignment in kallisto: the colored de Bruijn graph of the transcriptome, the intersection of k-compatibility classes, the skip to the end of a contig, and the EM on equivalence classes. Srivastava, Sarkar, Gupta and Patro (2016) gave quasi-mapping in RapMap, and later work in Salmon moved to [selective alignment](/selective-alignment/).

## References
