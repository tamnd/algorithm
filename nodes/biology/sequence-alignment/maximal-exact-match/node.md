---
tag: 30ANMZ
kind: concept
slug: maximal-exact-match
name: Maximal exact match
aliases:
- MEM
area: biology/sequence-alignment
level: core
summary: An exact common substring of two sequences that cannot be extended left or right. MUMs and SMEMs are restricted kinds of MEMs used as alignment seeds.
prereqs: [longest-common-substring, suffix-array]
see_also: [matching-statistics, maximal-repeats, generalized-suffix-tree, mummer, bwa, seed-and-extend, colinear-chaining, kmer-index]
sources:
  - paper: doi:10.1093/nar/27.11.2369
    title: Arthur L. Delcher, Simon Kasif, Robert D. Fleischmann, Jeremy Peterson, Owen White and Steven L. Salzberg, Alignment of whole genomes, Nucleic Acids Research 27(11), 1999
    locator: pages 2369 to 2376, Maximal unique matching subsequence decomposition (the definition of a MUM and how a suffix tree finds all MUMs)
  - paper: doi:10.1093/bioinformatics/bts280
    title: Heng Li, Exploring single-sample SNP and INDEL calling with whole-genome de novo assembly, Bioinformatics 28(14), 2012
    locator: pages 1838 to 1844, the FMD-index and the algorithm that finds the super-maximal exact matches of a query
  - paper: arxiv:1303.3997
    title: Heng Li, Aligning sequence reads, clone sequences and assembly contigs with BWA-MEM, 2013
    locator: Section 2 (SMEMs as seeds, reseeding and chaining)
  - paper: doi:10.1371/journal.pcbi.1005944
    title: Guillaume Marçais, Arthur L. Delcher, Adam M. Phillippy, Rachel Coston, Steven L. Salzberg and Aleksey Zimin, MUMmer4, a fast and versatile genome alignment system, PLoS Computational Biology 14(1), 2018
    locator: e1005944, the suffix array that replaces the suffix tree for finding MUMs and MEMs
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences
    locator: Chapter 7, first applications of suffix trees (common substrings, maximal pairs and matching statistics)
---

A maximal exact match (MEM) of two sequences $A$ and $B$ is a pair of positions where $A$ and $B$ agree on a run of letters that cannot be made longer on either side. MEMs are the seeds of many aligners: a long MEM is strong evidence that the two regions are related, and it can be found exactly and fast with a [suffix array](/suffix-array/), a suffix tree or an [FM-index](/fm-index/). Two restricted kinds matter in practice and must be kept apart. A *maximal unique match* (MUM), from [MUMmer](/mummer/), is a MEM whose string occurs exactly once in each sequence. A *super-maximal exact match* (SMEM), from [BWA](/bwa/)-MEM, is a MEM that no other match contains on the query.

## In plain words

Put two DNA sequences side by side and look for places where they agree letter for letter. Take one such place and grow it to the left and to the right, letter by letter, until the next letters differ or a sequence ends. What you get is a maximal exact match: a shared piece that is as long as it can be at that place.

The same short piece can appear many times, so two sequences can share a very large number of these matches. Most of them are short and happen by chance. Tools keep only the long ones. Some tools keep only the pieces that appear once in each sequence, because those point to one clear place. Others keep, for each part of the read, only the longest shared piece that covers it.

## The idea

**The model.** Let $A$ and $B$ be strings over an alphabet $\Sigma$ (for DNA, $\{A, C, G, T\}$), of lengths $n$ and $m$. Positions start at 0.

**Definition (MEM).** A triple $(i, j, \ell)$ with $\ell \ge 1$ is a *maximal exact match* of $A$ and $B$ when

1. $A[i \ldots i+\ell-1] = B[j \ldots j+\ell-1]$ (an exact match),
2. $i = 0$ or $j = 0$ or $A[i-1] \ne B[j-1]$ (it cannot be extended to the left), and
3. $i + \ell = n$ or $j + \ell = m$ or $A[i+\ell] \ne B[j+\ell]$ (it cannot be extended to the right).

A MEM is a property of a pair of positions, not of a string. The same string can be the string of several MEMs, and a MEM can be a substring of a longer MEM at other positions. In the dot plot of $A$ against $B$, each diagonal run of matching letters is one MEM.

**How many there are.** Each pair $(i, j)$ is the start of at most one MEM, so there are at most $nm$ of them. In random sequences this bound is close: a pair $(i, j)$ with $i, j \ge 1$ starts a MEM exactly when $A[i] = B[j]$ and $A[i-1] \ne B[j-1]$. For uniform random DNA this has probability $\frac14 \cdot \frac34 = \frac{3}{16}$, so two random DNA strings have about $3nm/16$ MEMs. Almost all of them are short. Tools therefore ask only for MEMs of length at least a minimum $L$. In random DNA a given pair of positions starts a match of length $L$ with probability $4^{-L}$, so the number of chance MEMs of length at least $L$ is about $nm \cdot 4^{-L}$, and $L$ is chosen to make this small.

**Definition (MUM).** Delcher et al. (1999) define a *maximal unique match* as a string that occurs exactly once in $A$ and exactly once in $B$, and that is not contained in any longer string with this property.

**Claim.** Let $u$ occur exactly once in $A$, at $i$, and exactly once in $B$, at $j$. Then $u$ is a MUM exactly when $(i, j, |u|)$ is a MEM. So the MUMs are the MEMs whose string is unique in both sequences.

*Proof.* Suppose $(i, j, |u|)$ is not a MEM, for example $A[i+\ell] = B[j+\ell]$ with $\ell = |u|$. Let $v = u\,A[i+\ell]$. Each occurrence of $v$ starts with an occurrence of $u$, so $v$ occurs in $A$ only at $i$ and in $B$ only at $j$. Then $v$ is a longer string, unique in both, that contains $u$, so $u$ is not a MUM. Extension to the left is the same. Conversely, suppose $(i, j, |u|)$ is a MEM and $v = xuy$ is longer and unique in both, with $|x| + |y| \ge 1$. The occurrence of $v$ in $A$ holds an occurrence of $u$, at offset $|x|$; since $u$ is unique in $A$, $v$ starts at $i - |x|$. In the same way $v$ starts at $j - |x|$ in $B$. Then the match $(i, j, |u|)$ extends to $(i - |x|, j - |x|, |v|)$, which contradicts maximality. $\square$

**At most $\min(n, m)$ MUMs.** Two MUMs cannot start at the same position $i$ of $A$. If $(i, j, \ell)$ and $(i, j', \ell')$ are MUMs with $\ell \le \ell'$, then $A[i \ldots i+\ell-1]$ occurs in $B$ at $j$ and at $j'$, so $j = j'$ by uniqueness. Two MEMs that start at the same pair of positions are equal. The same holds for the positions of $B$. So MUMs are few, which made them a good base for aligning whole genomes in MUMmer; the price is that a region repeated in one genome holds no MUM.

**Definition (SMEM).** For read mapping the question is asked from the query side. Let $Q$ be a query and $R$ a reference. Li (2012) calls an interval $[a, b)$ of $Q$ a *super-maximal exact match* when $Q[a \ldots b-1]$ occurs in $R$ and no other interval $[a', b') \supsetneq [a, b)$ of $Q$ has $Q[a' \ldots b'-1]$ occurring in $R$. An SMEM keeps all its occurrences in $R$, so it is not unique, and a MEM whose query interval lies inside a longer match is not an SMEM. Different SMEMs have different start points and different end points, so a query has at most $|Q|$ of them.

**SMEMs from matching statistics.** Let $\mathit{ms}[a]$ be the length of the longest prefix of $Q[a \ldots]$ that occurs in $R$; these are the [matching statistics](/matching-statistics/) of $Q$ against $R$. Then $\mathit{ms}[a+1] \ge \mathit{ms}[a] - 1$, so the end point $e(a) = a + \mathit{ms}[a]$ never decreases. Each SMEM $[a, b)$ satisfies $b = e(a)$, since $Q[a \ldots b-1]$ occurs in $R$ and is not extendable to the right. So the SMEMs are the intervals $[a, e(a))$ with $\mathit{ms}[a] > 0$ that no interval $[a', e(a'))$ with $a' < a$ contains, that is, those with $a = 0$ or $e(a) > e(a-1)$.

## Examples

Take $A = \texttt{GATTACAGATTACC}$ and $B = \texttt{CATTACAGGATTAC}$, both of length 14. The MEMs of length at least 3 are:

| MEM $(i, j, \ell)$ | string | occurrences in $A$ | occurrences in $B$ | kind |
|---|---|---|---|---|
| $(1, 1, 7)$ | ATTACAG | 1 | 1 | MEM, MUM, SMEM |
| $(0, 8, 6)$ | GATTAC | 2 | 1 | MEM, SMEM |
| $(7, 8, 6)$ | GATTAC | 2 | 1 | MEM, SMEM |
| $(8, 1, 5)$ | ATTAC | 2 | 2 | MEM only |

The match $(8, 1, 5)$ stops on the left because $A[7] = \texttt{G}$ and $B[0] = \texttt{C}$, and on the right because $A[13] = \texttt{C}$ and $B[6] = \texttt{A}$. It is a MEM, but its string ATTAC also occurs inside the longer match ATTACAG, so it is not a MUM. GATTAC occurs twice in $A$, so its two MEMs are not MUMs either; this is the repeat problem of MUMs.

Now treat $B$ as the query and $A$ as the reference. The matching statistics of $B$ are $2, 7, 6, 5, 4, 3, 2, 1, 6, 5, 4, 3, 2, 1$, and the end points $e(a)$ are $2, 8, 8, 8, 8, 8, 8, 8, 14, 14, \ldots$. They grow at $a = 0$, $1$ and $8$, so the SMEMs are $[0, 2)$ = CA, $[1, 8)$ = ATTACAG with one hit in $A$, and $[8, 14)$ = GATTAC with two hits in $A$. The MEM ATTAC at query interval $[1, 6)$ is inside $[1, 8)$ and is not an SMEM. With a minimum length of 3, CA is dropped.

## Where it is used

- **Whole-genome alignment.** [MUMmer](/mummer/) finds all MUMs of two genomes above a minimum length, keeps a [colinear chain](/colinear-chaining/) of them, and aligns the gaps between them; later versions can also use all MEMs. The 1999 paper builds a suffix tree of both genomes; MUMmer4 uses a suffix array. See [whole-genome alignment](/whole-genome-alignment/).
- **Read mapping.** [BWA](/bwa/)-MEM finds the SMEMs of each read with an FM-index of the genome and its reverse complement, uses them as seeds, and chains and extends them. See [read mapping](/read-mapping/).
- **Finding them.** All MEMs of length at least $L$ come from a [generalized suffix tree](/generalized-suffix-tree/) of $A$ and $B$, or from a suffix array with an [LCP array](/lcp-array/), in time linear in $n + m$ plus the number reported. The method is the same as for [maximal repeats](/maximal-repeats/) and maximal pairs, restricted to pairs that take one position from each sequence. Matching statistics give the SMEMs in $O(m)$ steps of a suffix tree or an FM-index.
- **Seeds in general.** A MEM is a variable-length seed. Unlike a fixed-length seed from a [k-mer index](/kmer-index/), it grows to the full length of the exact match, so one MEM replaces many overlapping k-mer hits on the same diagonal. See [seed-and-extend](/seed-and-extend/).

## References
