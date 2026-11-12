---
tag: BA8X6D
kind: concept
slug: paired-end-reads
name: Paired-end and mate-pair reads
aliases:
- mate pairs
area: biology/genome-assembly
level: core
summary: Two reads from the two ends of one DNA fragment of roughly known length. The pair links regions that are far apart, which orders contigs and spans repeats.
prereqs: [shotgun-sequencing, sequencing-coverage]
see_also: [scaffolding, scaffold, gap-filling, repeat-resolution, genome-repeat, read-mapping, central-limit-theorem, hybrid-assembly]
sources:
  - paper: doi:10.1016/s1046-2023(05)80162-8
    title: Al Edwards and C. Thomas Caskey, Closure strategies for random DNA sequencing, Methods 3(1) (1991)
    locator: pp. 41 to 47 (sequencing both ends of each clone)
  - paper: doi:10.1016/0888-7543(95)80219-c
    title: Jared C. Roach, Cecilie Boysen, Kai Wang and Leroy Hood, Pairwise end sequencing, a unified approach to genomic mapping and sequencing, Genomics 26(2) (1995)
    locator: pp. 345 to 353
  - paper: doi:10.1101/gr.7.5.401
    title: James L. Weber and Eugene W. Myers, Human whole-genome shotgun sequencing, Genome Research 7(5) (1997)
    locator: pp. 401 to 409 (end sequences of clones of several sizes to order the contigs)
  - book: isbn:9780990374602
    title: Phillip Compeau and Pavel Pevzner, Bioinformatics Algorithms, An Active Learning Approach, Volume I, second edition
    locator: Chapter 3 (read-pairs and the paired de Bruijn graph)
  - paper: doi:10.1038/nrg3367
    title: Niranjan Nagarajan and Mihai Pop, Sequence assembly demystified, Nature Reviews Genetics 14(3) (2013)
    locator: pp. 157 to 167 (mate pairs and scaffolding)
---

A read pair is two reads taken from the two ends of one DNA fragment. The length of the fragment, the *insert size*, is not measured for each pair, but it follows a known distribution, often close to normal with mean $\mu$ and standard deviation $\sigma$. So the two reads of a pair lie on opposite strands at a distance of about $\mu$. *Paired-end* reads come from short fragments of a few hundred bases. *Mate pairs* come from long fragments of thousands of bases, through a different library protocol. Assemblers use the pairs to order and orient [contigs](/contig/) into [scaffolds](/scaffold/), to estimate the gaps between them, and to span [repeats](/genome-repeat/) that are longer than one read.

## In plain words

You tear a long book into pieces, but instead of reading a whole piece, you read only its first line and its last line. You also know that each piece has about the same number of lines, say twenty. Now two lines that came from one piece tell you something no single line can: these two passages sit about twenty lines apart in the book.

That helps in two ways. If you have rebuilt two chapters but do not know their order, a piece whose first line is at the end of one chapter and whose last line is at the start of the other tells you that the chapters are neighbors, and roughly how big the hole between them is. And if a paragraph repeats in several places, a piece that starts before the paragraph and ends after it shows which text surrounds that copy.

## The idea

### The library and the geometry of a pair

The DNA is broken into fragments, and the fragments are selected by length. The machine reads $L_r$ bases from each end of each fragment. Each end is read from its own 5' end, so the two reads come from opposite strands. Take a fragment that covers $S[p \ldots p + I - 1]$ of the genome $S$. Then one read is $S[p \ldots p + L_r - 1]$, from the forward strand at the left end. The other read is the reverse complement of $S[p + I - L_r \ldots p + I - 1]$, from the reverse strand at the right end. Which of the two is called read 1 depends on the strand of the fragment. Mapped to the genome, the two reads point toward each other. This is the "forward-reverse" or inward orientation of paired-end reads.

### Insert size distribution

The insert size $I$ varies from fragment to fragment. It is estimated after the fact: map the pairs to a reference or to long contigs, keep the pairs whose reads map uniquely and close together, and take the mean $\mu$ and standard deviation $\sigma$ of the distances. A pair whose distance or orientation disagrees with this distribution is *discordant*. Discordant pairs point to a misassembly, a structural variant, or a chimeric fragment.

### Paired-end and mate-pair libraries

- **Paired-end.** Short fragments, a few hundred bases, read from both ends. The two reads face inward. With short inserts, the two reads of a pair can even overlap and be merged into one longer read.
- **Mate-pair.** Long fragments, thousands of bases. The fragment is closed into a circle with a marked junction, the circle is broken again, and the short piece around the junction is read from both ends. The two reads then come from the two ends of the long fragment, and they face outward when mapped (the "reverse-forward" orientation). Some pairs miss the junction and come out as short-insert pairs instead, so the assembler must filter them.
- **Clone ends.** In the Sanger era the inserts were plasmids of a few kilobases, fosmids of about 40 kilobases and bacterial artificial chromosomes of over 100 kilobases, each read from both ends. Edwards and Caskey, and Roach and colleagues, proposed this pairwise end sequencing, and Weber and Myers built their plan for the human genome on it.

### What a pair tells an assembler

Let read 1 map to contig $A$ and read 2 map to contig $B$, both uniquely.

- **Order and orientation.** The strand of each read on its contig fixes how $A$ and $B$ face each other. If read 1 is forward on $A$ and read 2 is reverse on $B$, then $B$ follows $A$ in the same orientation. If read 2 is forward on $B$, then $B$ follows $A$ reverse-complemented.
- **Gap size.** Let $A$ have length $a$, let read 1 start at position $x$ of $A$, and let read 2 end at position $y$ of $B$ (0-based). The insert covers $a - x$ bases of $A$, the gap of length $g$, and $y + 1$ bases of $B$. So

$$I = (a - x) + g + (y + 1), \qquad \hat g = \mu - (a - x) - (y + 1).$$

With $n$ independent pairs between the same two contigs, the average of their estimates has standard deviation $\sigma / \sqrt{n}$, and by the [central limit theorem](/central-limit-theorem/) it is close to normal. A negative $\hat g$ suggests that the contigs overlap.

- **Repeat spanning.** A pair spans a repeat of length $R$ when read 1 lies fully before it and read 2 fully after it. For a fixed insert $I$, the fragment start must lie in a window of $I - 2L_r - R + 1$ positions. With $P$ pairs on a genome of length $G$, the expected number of spanning pairs is $P (I - 2 L_r - R + 1)/G$ when this is positive, and zero when the repeat is longer than $I - 2L_r$.

These links form the input of [scaffolding](/scaffolding/), [gap filling](/gap-filling/) and [repeat resolution](/repeat-resolution/). In a de Bruijn assembler, a *paired de Bruijn graph* uses pairs of k-mers at distance $\mu$ as its edges.

### Physical coverage

With $P$ pairs of insert size $I$, the physical coverage is $PI/G$, the mean number of fragments that span a point of the genome. It counts the unread middle of each fragment, so it is larger than the sequence coverage $2PL_r/G$ when $I > 2L_r$. See [sequencing coverage](/sequencing-coverage/).

## Examples

**One gap estimate.** Contig $A$ has length $a = 3000$. Read 1 starts at position $x = 2800$ of $A$, forward. Read 2 maps reverse to contig $B$ and ends at position $y = 149$ of $B$. The library has $\mu = 500$. The pair covers $3000 - 2800 = 200$ bases of $A$ and $150$ bases of $B$, so $\hat g = 500 - 200 - 150 = 150$ bases. If $\sigma = 50$ and 25 pairs link $A$ and $B$ in the same way, the mean estimate has standard deviation $50 / \sqrt{25} = 10$ bases.

**How long a repeat a short insert can span.** Take a bacterial genome with $G = 5 \times 10^6$, $P = 500{,}000$ pairs, $L_r = 150$ and $I = 500$. The expected number of pairs that span a repeat of length $R$:

| $R$ | window $I - 2L_r - R + 1$ | expected spanning pairs | probability of none |
|---|---|---|---|
| 0 | 201 | 20.1 | $1.9 \times 10^{-9}$ |
| 100 | 101 | 10.1 | $4.1 \times 10^{-5}$ |
| 150 | 51 | 5.1 | 0.006 |
| 200 | 1 | 0.1 | 0.90 |

Here the probability of none is the Poisson value $e^{-\lambda}$. A repeat of 200 bases is almost never spanned, and longer repeats never are: these pairs cannot place the copies of a 5-kilobase rRNA operon. A mate-pair library with inserts of several kilobases can.

**Orientation.** Let read 2 be $\texttt{CCATGA}$, from an inward library, and let read 1 map forward near the end of contig $A$. In the genome, the region after $A$ holds $\overline{\texttt{CCATGA}} = \texttt{TCATGG}$. If contig $B$ contains TCATGG near its start, $B$ follows $A$ as it is. If $B$ contains CCATGA near its end instead, the assembler has built $B$ on the other strand, and the next piece of the genome is $\overline{B}$.

## Where it is used

- [Scaffolding](/scaffolding/): order and orient contigs and estimate gap sizes.
- [Repeat resolution](/repeat-resolution/): pairs that span a repeat copy choose the right way out of a collapsed repeat in the assembly graph.
- [Read mapping](/read-mapping/): if one read of a pair maps uniquely, its mate is searched only near the expected distance, which places reads that fall in repeats.
- Structural variant detection: pairs that map too far apart, too close, or in the wrong orientation mark deletions, insertions, inversions and translocations.
- Assembly validation: regions where many pairs are discordant are candidate misjoins.
- [Hybrid assembly](/hybrid-assembly/), where long reads now do much of the work that mate pairs used to do.

## References
