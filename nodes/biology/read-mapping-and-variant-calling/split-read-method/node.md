---
tag: TDWFBV
kind: algorithm
slug: split-read-method
name: Split-read method
aliases:
- split-read SV detection
area: biology/read-mapping-and-variant-calling
level: advanced
summary: Find breakpoints at base resolution by aligning the two parts of a read to different places, as one anchored mate and one split mate.
solves: [structural-variant-detection]
model: word-ram
complexity:
  vars: {W: the length of the search window, L: the length of the read}
  time: {worst: O(W L), best: O(W)}
  space: {extra: O(W)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2009
  people: [Kai Ye, Marcel H. Schulz, Quan Long, Rolf Apweiler, Zemin Ning]
  note: Pindel used the mapped mate of a pair as an anchor and found the two parts of the unmapped mate by pattern growth, which gave deletions and short insertions to the base from short reads. DELLY (2012) used split reads to refine the breakpoints of read-pair clusters.
prereqs: [structural-variant-detection, paired-end-read-mapping]
see_also: [discordant-read-pair-method, read-depth-copy-number-analysis, variant-normalization, maximal-exact-match, seed-and-extend, smith-waterman, haplotype-based-variant-calling, variant-call-format]
sources:
  - paper: doi:10.1093/bioinformatics/btp394
    title: Kai Ye, Marcel H. Schulz, Quan Long, Rolf Apweiler and Zemin Ning, Pindel, a pattern growth approach to detect break points of large deletions and medium sized insertions from paired-end short reads, Bioinformatics 25(21), 2009
    locator: the sections on the anchor points, the pattern growth of the two ends of the unmapped read and the calls of deletions and insertions
  - paper: doi:10.1093/bioinformatics/bts378
    title: Tobias Rausch, Thomas Zichner, Andreas Schlattl and others, DELLY, structural variant discovery by integrated paired-end and split-read analysis, Bioinformatics 28(18), 2012
    locator: the sections on the split-read refinement of the breakpoints of paired-end clusters
  - paper: doi:10.1038/nrg2958
    title: Can Alkan, Bradley P. Coe and Evan E. Eichler, Genome structural variation discovery and genotyping, Nature Reviews Genetics 12(5), 2011
    locator: the section on split-read methods and their place among the other signals
---

The split-read method finds the exact breakpoint of a deletion or an insertion from a read that crosses it. Such a read does not align to the reference as one piece: its first part matches on one side of the breakpoint and its second part on the other side. In a paired library, the mate of that read maps normally and is the *anchor*, so the search for the two parts is limited to a short window next to it. The method finds the longest prefix and the longest suffix of the read that match in the window, and the gap or the overlap between them gives the type, the place and the size of the event, to the base. This page follows Pindel (Ye et al., 2009), with exact matches.

## In plain words

When a piece of DNA is missing in a sample, a read that crosses the missing piece is the two sides joined together. Its start matches one place on the reference and its end matches a place a little further on.

So take a read that does not match anywhere as a whole, and look near its mate, which did match. Find how much of the start of the read matches there, then how much of its end matches after that. If the two parts are farther apart on the reference than in the read, bases were lost, and the distance tells how many. If they overlap, bases were added, and the read shows which ones.

## The problem

The input is a reference $\mathit{ref}$, a read $r$ of length $L$ turned to the forward strand of the reference, and a window $[lo, hi)$ where the read must lie. The window comes from the anchor: it starts at the anchor and is about two insert sizes long. The output is one event that explains the read as two exact parts, each of at least $m$ bases, or nothing:

- a **deletion** of $D$ bases: $r = \mathit{ref}[p{:}p + i] + \mathit{ref}[p + i + D{:}e]$, or
- an **insertion** of $\iota$ bases: $r = \mathit{ref}[p{:}p + i] + w + \mathit{ref}[p + i{:}e]$ with $|w| = \iota$.

The read must not occur in the window as a whole, and each part must occur only once, so that the place is not in doubt. See [structural variant detection](/structural-variant-detection/) for the problem and the other signals.

## The algorithm

Pattern growth keeps the list of places where the current prefix occurs and adds one base at a time until the list is empty. The suffix grows in the same way from the right end, only at or after the start $p$ of the prefix.

```pseudo id=main
SPLIT-READ(ref, r, lo, hi, m, ι_max)
L1  P ← the positions x in [lo, hi) with ref[x] = r[0]; a ← 1
L2  while a < L and some x in P has ref[x + a] = r[a] do keep those x in P; a ← a + 1
L3  if a = L or a < m or |P| ≠ 1 then return none, else p ← the one x in P
L4  grow the suffix r[L - b..L) in [p, hi) the same way; Q ← the end positions of its matches
L5  if b < m or |Q| ≠ 1 then return none, else e ← the one end in Q
L6  D ← e - p - L
L7  first ← max(L - max(-D, 0) - b, 1); last ← min(a, L - max(-D, 0) - 1)
L8  if D > 0 then return DEL at p + first of D bases
L9  else return INS before p + first of -D bases, the bases r[first..first - D)
```

Line L6 is the key step. The prefix starts at $p$ and the suffix ends at $e$, so the read covers $e - p$ bases of the reference. If $e - p > L$, the reference has $D$ more bases than the read, which is a deletion. If $e - p < L$, the read has $-D$ bases that are not in the reference, which is an insertion. $D = 0$ is no event, and an insertion longer than $\iota_{\max}$ is rejected.

The parts can overlap on the read when the bases next to the breakpoint repeat, an effect called *microhomology*. Then the split point $i$ can be any value in the range of line L7, and every one gives the same event. The code takes the leftmost one, which is the left-aligned form of [variant normalization](/variant-normalization/). A range that leaves a part shorter than $m$ is rejected.

## Example

The reference has 40 bases and the read 20:

$$\mathit{ref} = \texttt{CAGAACCTGCTGTGACATAAACTAGCTGATATGTGTTCCC}, \qquad r = \texttt{ACCTGCTGTGACTAGCTGAT}.$$

The prefix grows to $a = 12$ bases, $\texttt{ACCTGCTGTGAC}$, which occurs once, at $p = 4$. The suffix grows to $b = 10$ bases, $\texttt{ACTAGCTGAT}$, which occurs once in $[4, 40)$ and ends at $e = 30$. The read covers $e - p = 26$ bases of the reference, so $D = 26 - 20 = 6$: a deletion of 6 bases.

The two parts overlap by two bases, $\texttt{AC}$, so the split point can be 10, 11 or 12. At $i = 10$ the read is $\mathit{ref}[4{:}14] + \mathit{ref}[20{:}30]$ and the deleted bases are $\mathit{ref}[14{:}20] = \texttt{ACATAA}$. At $i = 12$ the deleted bases are $\mathit{ref}[16{:}22] = \texttt{ATAAAC}$, the same event shifted by the repeat. The call is the leftmost form, a deletion of 6 bases at position 14.

On a simulated reference of 6000 bases, with a deletion of 40 bases at 2000 and an insertion of $\texttt{GATTACA}$ before 4000, 1500 pairs with reads of 60 bases and an insert size of $300 \pm 20$ were made from the sample. The mates that did not map as a whole near their anchor gave 31 reads to split. Nine of them gave no call, because one part was too short or occurred twice. The deletion got 14 reads and the insertion 8, each at its true normalized place, and no read gave another event.

## Correctness

Pattern growth keeps the invariant that $P$ is the list of all places where $r[0{:}a]$ occurs in the window, so it returns the longest prefix that occurs and all its places; the same holds for the suffix. For any $i$ in the range of line L7, $r[0{:}i]$ is a prefix of the first part and $r[i + \iota{:}L]$ is a suffix of the second part, so the read is exactly the reference with the stated deletion or insertion, by the arithmetic of line L6. Conversely, every split with $i \le a$ and the suffix inside the second part is in that range, and they all give the same event up to a shift in a repeat. The proofs are in proofs/correctness.md, and the tests check the calls against a search over every split of every read in small random cases.

These are theorems for the model of two exact parts. As a detector of structural variants the method is a heuristic: a part can match by chance, a read with a sequencing error in the wrong place gives no call, and an event that is not a deletion or a short insertion is outside the model.

## Complexity

- **Time.** Line L1 scans the window in $O(W)$ for $W = hi - lo$. Each step of line L2 filters the list $P$, so the growth costs $O(W + a |P_1|)$, where $P_1$ is the first list; in the worst case, as for a read of one repeated base, this is $O(W L)$. In random sequence, the list shrinks by a factor of about 4 at each step, and the cost is close to $O(W)$.
- **Space.** $O(W)$ for the lists.
- **For a sample.** Only reads whose mate maps and that do not map as a whole are split, so the work grows with the number of such reads times the window length.

## Properties

- **Base resolution.** The call gives the exact breakpoint and, for an insertion, the inserted bases.
- **Exact matching.** The two parts must match without errors in this version. Pindel and later tools allow a few mismatches.
- **Short events only for insertions.** Both parts and the insertion must fit in one read, so an insertion can have at most $L - 2m$ bases.
- **Unique parts.** A part that occurs twice in the window gives no call, so repeats near the breakpoint hide the event.
- **Normalized output.** The leftmost split point gives the same call for every read of one event, so the reads can be counted together.

## Variants and improvements

- **Mismatches.** Allow a few mismatches in each part, at the cost of more candidate places.
- **Other types.** With the second part searched on the other strand, or before the first part, the same method finds inversions and tandem duplications. With a window on another chromosome, it finds translocations.
- **Large insertions.** Pindel joins the two ends of a long insertion from two groups of reads, one for each breakpoint.
- **Split alignments from the mapper.** Mappers such as [BWA](/bwa/) and [minimap2](/minimap2/) report a read that aligns in two pieces as a primary and a supplementary alignment. Many callers start from these and skip the search.
- **Refinement of other signals.** DELLY finds a cluster with [discordant pairs](/discordant-read-pair-method/) first and then uses split reads near it to find the breakpoint to the base.
- **Long reads.** With long reads, one read often crosses a whole event, and the split alignment shows larger and more complex events.

## When to use it

Use it to find the exact breakpoints of deletions and of insertions shorter than a read, or to refine the place of events found by read pairs or [read depth](/read-depth-copy-number-analysis/). It fills a gap in size between the small indels that a normal alignment finds and the large events that read pairs find. It is weak in repeats, for long insertions with short reads, and in regions where the mates do not map.

## Pitfalls

- **Repeats at the breakpoint.** A part that occurs twice gives no call, and a part of 10 or 15 bases can match by chance in a long window. Set the minimum length of a part with the window length in mind.
- **Microhomology.** Without normalization, reads of one event give calls at different places in the repeat and look like several events.
- **Sequencing errors.** An error near the breakpoint shortens one part and can move or lose the call.
- **The strand of the read.** The unmapped mate must be turned to the strand of the reference before the search; with the forward-reverse layout of most libraries, that is its reverse complement.
- **A wrong window.** A wrong insert size, or an anchor in a repeat, puts the window in the wrong place.

## Implementations

## History

Ye, Schulz, Long, Apweiler and Ning (2009) introduced Pindel. It took the read pairs in which one mate mapped and the other did not, and searched for the two ends of the unmapped read near the anchor by pattern growth, which found deletions and medium sized insertions to the base from short Illumina reads. DELLY (Rausch et al., 2012) combined read pairs with split reads to refine the breakpoints. Later callers use the split alignments that the mappers report, and long reads made split alignments the main signal for many classes of events.

## References
