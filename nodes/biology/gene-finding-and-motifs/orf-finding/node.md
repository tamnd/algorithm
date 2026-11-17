---
tag: 1C4YKG
kind: algorithm
slug: orf-finding
name: Open reading frame finding
aliases:
- six-frame ORF scan
area: biology/gene-finding-and-motifs
level: intro
summary: Scan the three frames of each strand once, codon by codon, and report every open reading frame that reaches a length cutoff. It takes O(G) time for a sequence of length G.
model: word-ram
complexity:
  vars: {G: the length of the DNA sequence, R: the number of ORFs reported}
  time: {worst: Θ(G + R log R), average: Θ(G + R log R), best: Θ(G)}
  space: {extra: Θ(G + R)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
prereqs: [open-reading-frame]
see_also: [gene-prediction, codon-adaptation-index, periodic-markov-chain-gene-model, interpolated-markov-model, generalized-hmm-gene-finder, genome-annotation, kmer, sliding-window]
sources:
  - book: isbn:9780262101066
    title: Neil C. Jones and Pavel A. Pevzner, An Introduction to Bioinformatics Algorithms, MIT Press, 2004
    locator: Chapter 6, the sections on gene prediction (open reading frames and statistical approaches)
  - url: https://emboss.sourceforge.net/apps/cvs/emboss/apps/getorf.html
    title: EMBOSS getorf manual (Peter Rice, Ian Longden and Alan Bleasby, EMBOSS, Trends in Genetics 16(6), 2000)
    locator: the -find option (regions between STOP codons, or between START and STOP codons), -minsize, -circular and -reverse
  - url: https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi
    title: NCBI, The Genetic Codes
    locator: table 1 (the standard code) and table 11 (bacterial starts GTG and TTG)
  - paper: doi:10.1093/nar/26.2.544
    title: Steven L. Salzberg, Arthur L. Delcher, Simon Kasif and Owen White, Microbial gene identification using interpolated Markov models, Nucleic Acids Research 26(2), 1998
    locator: pp. 544 to 548, the use of long ORFs that do not overlap other long ORFs as the training set of Glimmer
---

ORF finding lists the [open reading frames](/open-reading-frame/) of a DNA sequence. It reads the sequence in each of the three frames of each strand, one codon at a time, and keeps one number per frame: where the current ORF began. When it meets a stop codon, the run from that position to the stop is an ORF, and it is reported if it reaches a length cutoff. The scan reads each codon of the six frames once, so it takes $O(G)$ time for a sequence of $G$ bases. It is the first step of most bacterial gene finders: the ORFs are the candidates, and a codon model such as a [three-periodic Markov chain](/periodic-markov-chain-gene-model/) or an [interpolated Markov model](/interpolated-markov-model/) then decides which of them are genes.

## In plain words

A gene of a bacterium is read three letters at a time, from a start word (usually ATG) to one of three stop words (TAA, TAG or TGA). We do not know where the reading begins, so there are three ways to cut the sequence into words of three letters, and three more on the other strand. For each of the six ways, walk along the words. Remember the first start word you see. When a stop word comes, the stretch from the remembered start to the stop is a candidate gene; write it down if it is long enough, and forget the start. Long stretches without a stop are rare by chance, so the long candidates are worth a closer look.

## The problem

**Input.** A DNA sequence $s$ of length $G$ over $\{A, C, G, T\}$, a minimum length $\ell$ in sense codons, a set $\mathrm{START}$ of start codons (by default $\{\mathrm{ATG}\}$), the stop codons $\mathrm{STOP} = \{\mathrm{TAA}, \mathrm{TAG}, \mathrm{TGA}\}$ of the standard code, and one of the two definitions of an ORF.

**Output.** Every ORF of $s$ in the six frames with at least $\ell$ sense codons, each as a strand, a frame, an interval of $s$ and a number of codons. With the *start-stop* definition, an ORF runs from a start codon to the next in-frame stop codon, and for each stop codon only the longest ORF is kept, the one from the first start codon after the previous stop. With the *stop-stop* definition, an ORF runs from right after a stop codon (or from the first codon of the frame) to the next stop codon. The [definition page](/open-reading-frame/) gives both in full. A run of codons with no stop codon before the end of the sequence is not reported.

The page and the code use 0-based, half-open intervals $[a, b)$ in the pseudocode, as Python does, and 1-based positions in the text. An ORF on the minus strand is given by its interval on $s$; its bases are $\mathrm{rc}(s[a, b))$.

## The algorithm

For each frame, the scan keeps the position `open` where the current ORF began, or *none* if no ORF is open. In start-stop mode, `open` is set at the first start codon after a stop. In stop-stop mode, `open` is set right after each stop, and at the first codon of the frame.

```pseudo id=main
FIND-ORFS(s, ℓ, START, mode)
L1  for each strand (t, sign) in ((s, +), (rc(s), -)) do
L2      for each offset f in 0, 1, 2 do    ▷ open ← none in start-stop mode, f in stop-stop mode
L3          for i ← f, f + 3, f + 6, ... while i + 3 ≤ G do
L4              if c = t[i, i + 3) is in STOP then
L5                  if open ≠ none and (i - open) / 3 ≥ ℓ then
L6                      add the ORF [open, i + 3) with (i - open) / 3 sense codons
L7                  open ← none in start-stop mode, i + 3 in stop-stop mode
L8              else if open = none and c is in START then
L9                  open ← i
L10         map each ORF [a, b) of the minus strand to the interval [G - b, G - a) of s
L11 return the ORFs, sorted by start, end, strand and frame
```

Line L8 sets `open` only when no ORF is open, so a second ATG inside an open ORF does not move its start; this keeps the longest ORF for each stop. Line L10 converts coordinates: base $p$ of $\mathrm{rc}(s)$ (from 0) is the complement of base $G - 1 - p$ of $s$, so the interval $[a, b)$ of $\mathrm{rc}(s)$ covers $[G - b, G - a)$ of $s$. The test for STOP and START is a look-up of one codon among 64, which takes constant time.

## Example

Take the 30 bases $s = \mathrm{GATGAAAATGTTTTGACTAGGGCATCCATG}$, with $\ell = 0$ and the start-stop definition. The reverse complement is $\mathrm{CATGGATGCCCTAGTCAAAACATTTTCATC}$. The translations of the six frames, with $*$ for a stop, are:

| frame | offset $f$ | translation |
|---|---|---|
| $+1$ | 0 | D E N V L T R A S M |
| $+2$ | 1 | M K M F * L G H P |
| $+3$ | 2 | * K C F D * G I H |
| $-1$ | 0 | H G C P S Q N I F I |
| $-2$ | 1 | M D A L V K T F S |
| $-3$ | 2 | W M P * S K H F H |

The scan of frame $+2$ (offset 1) goes as follows; the positions $i$ are from 0.

| $i$ | codon | line | action | open |
|---|---|---|---|---|
| 1 | ATG | L8, L9 | a start, no ORF open | 1 |
| 4 | AAA | | sense codon | 1 |
| 7 | ATG | L8 | a start, but an ORF is open: no change | 1 |
| 10 | TTT | | sense codon | 1 |
| 13 | TGA | L4 to L7 | a stop: report $[1, 16)$ with $(13 - 1)/3 = 4$ codons | none |
| 16, 19, 22, 25 | CTA, GGG, CAT, CCA | | no start | none |

Then $i = 28$ fails the test $i + 3 \le 30$, and the frame ends. Frames $+1$ and $-1$ have no stop codon. Frame $+3$ has stops but no ATG. Frame $-2$ has a start but no stop. In frame $-3$, ATG at offsets 5 to 7 of $\mathrm{rc}(s)$ is followed by CCC and the stop TAG at 11 to 13, which gives the interval $[5, 14)$ of $\mathrm{rc}(s)$ with 2 codons. Line L10 maps it to $[30 - 14, 30 - 5) = [16, 25)$ of $s$. So the output is:

| strand | frame | interval of $s$ (from 0) | bases 1-based | codons | peptide |
|---|---|---|---|---|---|
| + | $+2$ | $[1, 16)$ | 2 to 16 | 4 | MKMF |
| - | $-3$ | $[16, 25)$ | 17 to 25 | 2 | MP |

With $\ell = 3$ only the first remains. In stop-stop mode the output has four ORFs: $[1, 16)$ in frame $+2$ (it starts at the first codon of the frame), the empty run $[2, 5)$ that ends at the TGA at the start of frame $+3$, the run $[5, 20)$ with the 4 codons KCFD in frame $+3$, and $[16, 28)$ with the 3 codons WMP in frame $-3$. The test file checks all these values.

## Correctness

Fix one frame of one strand, with codons $c_0, c_1, \ldots$ at positions $f, f + 3, \ldots$. In start-stop mode, the invariant at the top of line L4 for codon $c_j$ is: `open` is the position of the first start codon after the last stop codon before $c_j$ (after the beginning of the frame if there is none), or none if there is no such start codon. In stop-stop mode, `open` is the position right after the last stop codon before $c_j$, or $f$. Lines L7 and L9 keep the invariant, and no other line changes `open`. When $c_j$ is a stop, every ORF that ends at $c_j$ begins after the previous stop, so by the invariant the run $[\mathit{open}, i + 3)$ is the longest start-stop ORF ending at $c_j$, or the stop-stop ORF ending at $c_j$. Every ORF ends at a stop codon, and each stop codon is visited once, so line L6 reports each ORF of the frame with at least $\ell$ codons exactly once. A run with no stop after it is never reported. Line L10 is correct by the identity $\mathrm{rc}(s)_p = \overline{s_{G - 1 - p}}$. The full proof is in the proofs folder.

## Complexity

- **Time.** Line L1 builds $\mathrm{rc}(s)$ in $\Theta(G)$ time. For each strand, the three frames together read $\lfloor G/3 \rfloor + \lfloor (G-1)/3 \rfloor + \lfloor (G-2)/3 \rfloor \le G$ codons, and each codon costs $O(1)$ on a word RAM: it is a 6-bit number, and the start and stop tests are table look-ups. So the scan costs $\Theta(G)$ in every case. With $R$ ORFs reported, the sort of line L11 adds $O(R \log R)$. The sort can be dropped: a merge of the six lists, each already sorted, costs $O(R \log 6) = O(R)$, and many uses need no order.
- **Number of ORFs.** Each stop codon ends at most one reported ORF, and each strand has at most $G$ codon positions over its three frames, so $R \le 2G$. In random DNA with uniform bases, a codon is a stop with probability $3/64$ and the chance of at least 100 sense codons before a stop is $(61/64)^{100} \approx 0.0082$, so a cutoff of 100 codons keeps about 771 ORFs per megabase over the six frames.
- **Space.** $\Theta(G)$ for $\mathrm{rc}(s)$ and $\Theta(R)$ for the output. A scan of the minus strand that reads $s$ backward and complements each codon on the fly needs no copy, and then the extra space is $O(1)$ beyond the output.

## Properties

- **Exact and deterministic.** It returns exactly the ORFs of the definition; there is no scoring and no randomness.
- **One pass per frame, online in each frame.** Each frame is read left to right with one variable of state, so a stream of bases can be scanned as it arrives, for the plus strand. The minus strand needs the stop codons to its right, so it waits for the end of a run or reads the sequence backward.
- **Independent frames.** The six scans share nothing, so they run in parallel.
- **Nested ORFs.** For each stop codon, start-stop mode gives the longest ORF. The other start-stop ORFs that end at the same stop begin at the later in-frame start codons inside it; listing them all costs $O(G)$ more, one per start codon.
- **Code dependent.** STOP and START come from the genetic code. Table 11 adds GTG, TTG and other starts for bacteria, and table 2 (vertebrate mitochondria) has the stops TAA, TAG, AGA and AGG.

## Variants and improvements

- **Alternative start codons.** For bacteria, pass START $= \{\mathrm{ATG}, \mathrm{GTG}, \mathrm{TTG}\}$. The ORF is then longer or equal, and the true start is decided later from a ribosome binding site or a start model.
- **Circular genomes.** A bacterial chromosome or a plasmid is circular. An ORF can cross the origin. Scan the sequence $s s$, written twice, and keep each ORF that starts in the first copy and is not longer than $G$. EMBOSS getorf has a `-circular` option for this.
- **Partial ORFs.** On contigs and reads, the ends of the sequence cut genes. A tool for these reports the open run at each end as a partial ORF.
- **Six-frame translation.** Translate all six frames and split at the stops. This is the same scan with the protein written out, and it is how a protein database is searched with DNA.
- **Training sets for gene models.** Glimmer takes the long ORFs that do not overlap other long ORFs as its first training set for the [interpolated Markov model](/interpolated-markov-model/). Later gene finders score every start-stop ORF with a codon model and choose the start codon and the set of genes by dynamic programming.
- **Coding statistics in the scan.** A score that is a sum over the codons, such as the log-likelihood ratio of a [codon model](/periodic-markov-chain-gene-model/) or the log of the [codon adaptation index](/codon-adaptation-index/), can be added up during the scan with a prefix sum per frame. Then the score of any ORF is one subtraction.

## When to use it

Use it as the first step of gene finding in bacteria, archaea and viruses, where most genes are one uninterrupted ORF; to translate a sequence before a protein search; to check a cloned or synthetic gene for an intact reading frame; and to list candidates for small proteins. Do not use the ORF list alone as a gene list. A cutoff of 100 codons is a rule of thumb: it misses short genes, and in GC-rich genomes it keeps many chance ORFs, often on the strand opposite a real gene. For eukaryotic genes with introns, use [gene prediction](/gene-prediction/) with a [GHMM](/generalized-hmm-gene-finder/), or align a protein or a transcript to the genome with [spliced alignment](/spliced-alignment-problem/).

## Pitfalls

- **Coordinates of the minus strand.** The frame number of a minus strand ORF depends on whether the offset is counted on $\mathrm{rc}(s)$ or from the start of $s$. An ORF at offset $f$ of $\mathrm{rc}(s)$ has its codon boundaries at offset $(G - f) \bmod 3$ of $s$, and the two numbers agree only when $G \equiv 2f \pmod 3$. Say which. The code counts it on $\mathrm{rc}(s)$.
- **Off by one at the stop.** Say whether the stop codon is part of the ORF interval and whether it counts in the length. Here the interval holds the stop, and the length counts sense codons only.
- **Moving the start.** Line L8 must not move `open` when an ORF is already open, or the scan reports the shortest ORF for each stop instead of the longest.
- **Runs to the end.** A run with no stop codon is not an ORF. Reporting it as one makes the last ORF of each frame wrong.
- **Lower case and N.** Upper-case the sequence first, and decide what a codon with N means; here it is neither a start nor a stop, which can join two ORFs across an unknown stop.
- **The wrong genetic code.** A mitochondrial sequence scanned with table 1 breaks its genes at each TGA, which codes for tryptophan there.

## Implementations

## History

Programs that search the six frames of a sequence for long stretches without stop codons are a standard part of sequence analysis toolkits such as EMBOSS, whose getorf program (Rice, Longden and Bleasby 2000) reports both the regions between stop codons and the regions from a start codon to a stop codon. Glimmer (Salzberg, Delcher, Kasif and White 1998) used the long ORFs of a new genome to train its interpolated Markov model, and later bacterial gene finders score every ORF with codon statistics. The textbook treatment of ORFs as the first step of gene prediction is in Chapter 6 of Jones and Pevzner (2004).

## References
