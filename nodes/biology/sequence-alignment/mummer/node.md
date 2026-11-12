---
tag: VB8A1D
kind: algorithm
slug: mummer
name: MUMmer
aliases:
- maximal unique match alignment
area: biology/sequence-alignment
level: advanced
summary: Delcher and colleagues' 1999 whole-genome aligner. It finds the maximal unique matches of two genomes with a suffix tree, chains them by a longest increasing subsequence, and aligns the gaps.
solves: [whole-genome-alignment]
model: word-ram
complexity:
  vars: {n: the total length of the two genomes, u: the number of MUMs, g: the total size of the dynamic programming tables for the gaps}
  time: {worst: O(n + u log u + g)}
  space: {extra: O(n + g)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1999
  people: [Arthur L. Delcher, Simon Kasif, Robert D. Fleischmann, Jeremy Peterson, Owen White, Steven L. Salzberg]
  note: An early aligner of whole bacterial genomes; MUMmer2 (2002), MUMmer3 (2004) and MUMmer4 (2018) followed.
prereqs: [maximal-exact-match, suffix-tree, longest-increasing-subsequence]
see_also: [whole-genome-alignment, colinear-chaining, suffix-array, lcp-array, seed-chaining, blat, smith-waterman, minimap2]
sources:
  - paper: doi:10.1093/nar/27.11.2369
    title: Arthur L. Delcher, Simon Kasif, Robert D. Fleischmann, Jeremy Peterson, Owen White and Steven L. Salzberg, Alignment of whole genomes, Nucleic Acids Research 27(11), 1999
    locator: pages 2369 to 2376, the definition of a MUM, the suffix tree step, the longest increasing subsequence step and the four classes of gaps
  - paper: doi:10.1093/nar/30.11.2478
    title: Arthur L. Delcher, Adam Phillippy, Jane Carlton and Steven L. Salzberg, Fast algorithms for large-scale genome alignment and comparison, Nucleic Acids Research 30(11), 2002
    locator: pages 2478 to 2483, MUMmer2 with a suffix tree of one genome only, and PROmer
  - paper: doi:10.1186/gb-2004-5-2-r12
    title: Stefan Kurtz, Adam Phillippy, Arthur L. Delcher, Michael Smoot, Martin Shumway, Corina Antonescu and Steven L. Salzberg, Versatile and open software for comparing large genomes, Genome Biology 5(2), 2004
    locator: article R12, MUMmer3, its options for unique and non-unique matches, and NUCmer
  - paper: doi:10.1371/journal.pcbi.1005944
    title: Guillaume Marçais, Arthur L. Delcher, Adam M. Phillippy, Rachel Coston, Steven L. Salzberg and Aleksey Zimin, MUMmer4, a fast and versatile genome alignment system, PLOS Computational Biology 14(1), 2018
    locator: article e1005944, the suffix array index and the multithreaded matching
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 7, the applications of suffix trees to common substrings and maximal repeats
---

MUMmer, by Arthur Delcher, Steven Salzberg and colleagues (1999), was an early program built to align two complete bacterial genomes. Dynamic programming over two genomes of millions of bases each needs a table of $10^{12}$ cells, so MUMmer uses exact matches as anchors. It finds the *maximal unique matches* (MUMs) of the two genomes with a [suffix tree](/suffix-tree/): the [maximal exact matches](/maximal-exact-match/) whose string occurs exactly once in each genome. A MUM of good length is very likely to come from the same place in both genomes. MUMmer then keeps the largest set of MUMs in the same order in both genomes, found as a [longest increasing subsequence](/longest-increasing-subsequence/), and aligns the short gaps between them with dynamic programming. The later versions add protein-level matching, non-unique matches and faster indexes, and the package is still in wide use.

## In plain words

Two strains of a bacterium have almost the same genome. Look for long pieces of text that appear once in the first genome and once in the second. Such a piece almost surely marks the same place in both, so it can serve as an anchor.

Most anchors appear in the same order in both genomes. A few are out of order, because of repeats or because a part of a genome was moved. MUMmer keeps the largest set of anchors that are in order in both genomes. Between two neighbouring anchors there is a short gap: one changed base, an extra piece, or a region of many changes. These gaps are small, so MUMmer aligns them letter by letter.

## The problem

**Input.** Two genomes $A$ and $B$, with total length $n$, and a minimum match length $\ell$.

**Output.** An alignment of $A$ with $B$ that consists of a chain of exact matches in the same order in both genomes, with the gaps between them aligned, and the list of gaps with their types.

This is a heuristic for [whole-genome alignment](/whole-genome-alignment/) of two closely related genomes with few rearrangements.

## The algorithm

**1. MUMs.** A MUM of $A$ and $B$ is a string $u$ that occurs exactly once in $A$, at $i$, and once in $B$, at $j$, and that is maximal: the letters before $A[i]$ and $B[j]$ differ, and so do the letters after. MUMmer 1 builds a suffix tree of $A\#B$. A MUM is then a leaf pair: an internal node with exactly two leaf children, one from each genome, whose two suffixes have different letters before them. This page uses the equivalent test on the [suffix array](/suffix-array/) and [LCP array](/lcp-array/) of $S = A\#B\$$: two adjacent suffixes from different genomes whose common prefix is longer than the common prefixes with their outer neighbours.

**2. Chain.** Sort the MUMs by position in $A$, and find the heaviest subsequence whose positions in $B$ also increase, where a MUM weighs its length. This is a weighted longest increasing subsequence. MUMs off the chain come from repeats, inversions and moved segments. This is a simple case of [colinear chaining](/colinear-chaining/), with points instead of fragments.

**3. Gaps.** The gap between two consecutive MUMs of the chain falls into one of four classes in the 1999 paper:

- *SNP*: exactly one base in each genome, a single substitution;
- *insertion*: a gap in one genome only, an inserted or deleted segment;
- *highly polymorphic region*: a gap in both genomes, aligned with dynamic programming;
- *repeat*: the two MUMs overlap in one genome, as with a tandem repeat of different copy numbers. The overlap is trimmed from one of them.

```pseudo id=main
MUMMER(A, B, ℓ)
L1  SA ← suffix array of S = A # B $
L2  LCP ← LCP array of S and SA
L3  for r ← 1 to |S| − 1 do
L4      if SA[r − 1] and SA[r] are in different genomes and LCP[r] ≥ ℓ then
L5          if LCP[r − 1] < LCP[r] and LCP[r + 1] < LCP[r] then
L6              if the letters before the two suffixes differ, or one is at the start then
L7                  add (i, j, LCP[r]) to the MUMs M
L8  sort M by the start in A
L9  for each MUM x in this order do
L10     best ← the largest f(y) over the MUMs y before x with start in B below that of x
L11     f(x) ← best + length(x)
L12     store f(x) at the rank of the start of x in B
L13 C ← the chain that ends at the MUM with the largest f, by back pointers
L14 for each pair of consecutive MUMs of C, and the two ends do
L15     if they overlap, trim the start of the second one; the gap is a repeat
L16     align the gap strings with dynamic programming and classify the gap
L17     move on to the end of the second MUM
```

Line L10 is a prefix maximum query on a [Fenwick tree](/fenwick-tree/) over the ranks of the starts in $B$. In this page's implementation the gaps are aligned with unit-cost edit distance; MUMmer 1 used a variant of [Smith-Waterman](/smith-waterman/).

## Example

Let $\ell = 3$ and

$A = \texttt{GATTACAGGCTTACGATCCA}$ (20 bases),

$B = \texttt{GATTACATGCTTACGTTCCATT}$ (22 bases).

The pairs have 7 maximal exact matches of length 3 or more, and 3 of them are MUMs:

| start in $A$ | start in $B$ | match | MUM? |
|---|---|---|---|
| 0 | 0 | GATTACA | yes |
| 8 | 8 | GCTTACG | yes |
| 16 | 16 | TCCA | yes |
| 2 | 10 | TTAC | no, TTAC occurs twice in each genome |
| 10 | 2 | TTAC | no |
| 1 | 19 | ATT | no, ATT occurs twice in $B$ |
| 14 | 0 | GAT | no, GAT occurs twice in $A$ |

The three MUMs are in the same order in both genomes, so the chain holds all of them, with weight $7 + 7 + 4 = 18$. The gaps are:

| between | $A$ gap | $B$ gap | class | cost |
|---|---|---|---|---|
| GATTACA and GCTTACG | G (position 7) | T (position 7) | SNP | 1 |
| GCTTACG and TCCA | A (position 15) | T (position 15) | SNP | 1 |
| TCCA and the end | empty | TT | insertion | 2 |

The alignment costs 4, which here equals the edit distance of $A$ and $B$.

## Correctness

The MUM test is exact. A MUM string occurs exactly twice in $S$, so its two suffixes are adjacent in the suffix array, and their common prefix is longer than the common prefixes with the neighbours; conversely, two adjacent suffixes from different genomes with this property share a string that occurs once in each genome. The separators $\#$ and $\$$ stop every common prefix at the end of a genome, which gives right-maximality, and line L6 checks left-maximality. The chain step is the standard dynamic program for a weighted increasing subsequence; it is exact because MUMs have distinct starts in each genome. The proofs file gives the details, and the tests compare MUMs with a naive scan and chains with brute force over all subsets.

The whole method is a heuristic. A short or diverged homologous region may have no MUM; a repeat may have a unique piece that matches the wrong copy; and the chain fixes the anchors, so the final alignment can cost more than an optimal one.

## Complexity

| step | time | space |
|---|---|---|
| suffix tree or suffix array with LCP | $O(n)$ | $O(n)$ |
| MUMs | $O(n)$ | $O(u)$ |
| chain | $O(u \log u)$ | $O(u)$ |
| gaps | the sum of the products of the gap lengths, $g$ | $O(g)$, or linear with [Hirschberg's](/hirschberg-algorithm/) method |

With few differences the gaps are short, and the linear-time index dominates. In practice the memory of the suffix tree, many bytes per base, was the limit, and the later versions reduced it (see below).

## Properties

- **Anchored on uniqueness.** A MUM marks the same locus in both genomes with high probability, because its string occurs once in each.
- **Collinear.** The chain keeps one order. Inversions and translocations break the alignment into pieces, and MUMs on the reverse strand need a second run against the reverse complement.
- **Tuned for close genomes.** With many differences, MUMs become short and few, and the gaps large.

## Variants and improvements

- **MUMmer2 (2002).** Builds the suffix tree of one genome only and streams the other genome through it, which lowers memory. PROmer finds matches in the six-frame translations, for more distant genomes.
- **MUMmer3 (2004).** Rewritten by Kurtz and colleagues with a smaller suffix tree. It can also report matches that are unique in only the reference, or all maximal matches; NUCmer clusters them into alignments of draft assemblies.
- **MUMmer4 (2018).** Replaces the suffix tree with a suffix array, runs on several threads and handles larger genomes.
- **[Colinear chaining](/colinear-chaining/).** The general form of step 2, with fragments that span intervals in both genomes and with gap costs ([seed chaining](/seed-chaining/)).
- **[Minimap2](/minimap2/).** Uses minimizer anchors and chaining with gap costs, and replaces MUMmer for many genome-to-genome comparisons.

## When to use it

Use MUMmer (in practice NUCmer and the dot plots of the package) to compare two assemblies of the same species, a draft against a finished genome, or two close strains. Use it to find SNPs, indels and large rearrangements. For distant genomes or many genomes, use a whole-genome aligner with gapped seeds and multiple alignment, such as those on the [whole-genome alignment](/whole-genome-alignment/) page.

## Pitfalls

- **MUM versus MEM.** A MUM must be unique in both genomes; a [maximal exact match](/maximal-exact-match/) need not be. Using all MEMs gives many anchors in repeats.
- **Reverse strand.** MUMs between $A$ and the reverse complement of $B$ need a separate search; one run sees only one strand.
- **A short minimum length.** Short MUMs are often chance matches and pull the chain into wrong places.
- **Reading the chain as the whole story.** MUMs off the chain are not noise by default; they show repeats and rearrangements.

## Implementations

## History

Delcher and colleagues at The Institute for Genomic Research wrote MUMmer in 1999 to compare closely related bacterial genomes, building on the suffix tree methods for repeats and maximal matches in Gusfield's book. MUMmer2 (2002) lowered memory and added protein matching, MUMmer3 (2004) became an open-source package with NUCmer and PROmer, and MUMmer4 (2018) moved to a suffix array. The idea of MUMs as anchors also shaped later whole-genome aligners such as Mauve, which uses multiple MUMs.

## References
