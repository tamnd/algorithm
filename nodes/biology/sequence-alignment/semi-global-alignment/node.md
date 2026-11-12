---
tag: 1TYCNQ
kind: problem
slug: semi-global-alignment
name: Semi-global alignment
aliases:
- overlap alignment
- fitting alignment
- free-end-gap alignment
- end-space free alignment
area: biology/sequence-alignment
level: core
summary: Global alignment of two sequences in which the gaps at chosen ends cost nothing; overlap and fitting alignment are the main cases.
prereqs: [global-alignment]
see_also: [semi-global-dp, global-alignment, local-alignment, overlap-detection, read-mapping, approximate-string-matching, sellers-algorithm, overlap-graph]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 11, the section on end-space free alignment
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.3, Overlap matches
  - book: isbn:9780262101066
    title: Neil C. Jones and Pavel A. Pevzner, An Introduction to Bioinformatics Algorithms, MIT Press, 2004
    locator: Chapter 6, the sections on global and local alignment and their variations
  - paper: "Peter H. Sellers, The theory and computation of evolutionary distances: pattern recognition, Journal of Algorithms 1(4), 1980, 359-373"
    locator: the computation of the substrings of a text that are closest to a pattern
---

Semi-global alignment is the form of [pairwise sequence alignment](/pairwise-sequence-alignment/) that aligns all of both sequences, as [global alignment](/global-alignment/) does, but does not charge for the gaps at some of the four ends. Which ends are free depends on the question. In *overlap* alignment, a suffix of one sequence lines up with a prefix of the other, as two reads that overlap in a genome assembly. In *fitting* alignment, one sequence must fit completely inside the other, as a short read inside a reference. The [semi-global DP](/semi-global-dp/) solves every case in $O(mn)$ time for lengths $m$ and $n$, by a change of the first row, the first column and the end cell of the Needleman-Wunsch table.

## In plain words

Sometimes two sequences are related, but they do not cover the same stretch. Two pieces of DNA read from a genome may overlap only at their ends: the end of the first is the start of the second. A short piece may come from the middle of a long one. If you align such sequences end to end, the parts that stick out are scored as long gaps, and the true match looks bad.

Semi-global alignment fixes this. You say in advance which ends may stick out for free. The parts that stick out cost nothing; everything else is scored as in a normal alignment. Unlike local alignment, you may not drop bad letters in the middle or at the ends that you did not declare free.

## Definition

**Model.** The alphabet $\Sigma$ is DNA, RNA or the 20 amino acids. The input is $x = x_1 \cdots x_m$, $y = y_1 \cdots y_n$, a substitution score $s : \Sigma \times \Sigma \to \mathbb{Z}$, a linear gap penalty $d \ge 0$ per gap symbol, and four flags $P_x, S_x, P_y, S_y$ that say which end gaps are free. The costs are in the [word RAM](/word-ram/) model.

Let $A$ be an alignment of $x$ and $y$ (see [alignment score](/alignment-score/)). A gap column $(x_k, -)$ is *leading* if it comes before every column that holds a letter of $y$, and *trailing* if it comes after every such column. The same words apply to a gap column $(-, y_l)$ and the letters of $x$. The semi-global score of $A$ is

$$S_F(A) = \sum_{\text{pair columns } (a, b)} s(a, b) \; - \; d \cdot (\text{number of charged gap columns}),$$

where a gap column $(x_k, -)$ is free if it is leading and $P_x$ holds, or trailing and $S_x$ holds; a gap column $(-, y_l)$ is free if it is leading and $P_y$ holds, or trailing and $S_y$ holds; and every other gap column is charged.

**Output.** An alignment $A$ of $x$ and $y$ with the largest $S_F(A)$, and its score.

**The named cases.**

| name | free ends | equivalent statement |
|---|---|---|
| global | none | [global alignment](/global-alignment/) of $x$ and $y$ |
| overlap, $x$ then $y$ | $P_x$, $S_y$ | the best global alignment of a suffix of $x$ with a prefix of $y$ |
| overlap, $y$ then $x$ | $P_y$, $S_x$ | the best global alignment of a suffix of $y$ with a prefix of $x$ |
| fitting $y$ into $x$ | $P_x$, $S_x$ | the best global alignment of $y$ with a substring of $x$ |
| fitting $x$ into $y$ | $P_y$, $S_y$ | the best global alignment of $x$ with a substring of $y$ |
| all ends free | all four | the best of the two overlap and the two fitting cases |

The third column holds because a free leading gap of $x$ is the same as dropping a prefix of $x$ before the global alignment, and a free trailing gap the same as dropping a suffix. Leading gaps of $x$ and leading gaps of $y$ cannot both occur in one alignment: if a gap column $(x_k, -)$ comes before all letters of $y$, then $x_1$ comes before all of them too, and no gap column $(-, y_l)$ can come before $x_1$.

## Variants

- **Affine gaps.** The same flags work with the [Gotoh algorithm](/gotoh-algorithm/); a free end gap then costs neither the opening nor the extension.
- **Unit costs.** Fitting a pattern into a text with unit costs is [approximate string matching](/approximate-string-matching/), and [Sellers' algorithm](/sellers-algorithm/) is the fitting table for it. With a bound $k$ on the cost, it is the [k-differences problem](/k-differences-problem/).
- **Local at one end.** Some read mappers align a read globally at one end and locally at the other, so that the read may be clipped at one end only. This mixes semi-global and [local alignment](/local-alignment/): the free end may drop letters of the read itself, not only gaps against the reference.
- **Banded.** If the position of the overlap or of the fit is roughly known, a [banded alignment](/banded-alignment/) restricts the table to a band.

## Examples

All examples use the toy DNA scheme: $s(a, a) = +2$, $s(a, b) = -1$ for $a \ne b$, $d = 2$.

**Overlap.** $x = $ TTCAGTAC and $y = $ AGTACGGA share AGTAC, at the end of $x$ and the start of $y$. The overlap alignment ($P_x$ and $S_y$) is

```
T T C A G T A C - - -
- - - A G T A C G G A
```

with the score $5 \cdot 2 = 10$: the three leading gap columns under TTC are free by $P_x$, and the three trailing gap columns over GGA are free by $S_y$. The global alignment of the same pair scores $-2$, because it charges these 6 end gaps.

**Fitting.** $x = $ CAGGTACT and $y = $ TAGTAC. Fitting $y$ into $x$ ($P_x$ and $S_x$) gives

```
C A G G T A C T
T A - G T A C -
```

with the score $-1 + 2 - 2 + 2 + 2 + 2 + 2 = 7$; the last column is free by $S_x$. The global alignment scores 5, because the last gap is charged. The [local alignment](/local-alignment/) scores 8 with GTAC alone, because it may drop the mismatch (C, T) and the letters TA of $y$; fitting must keep all of $y$.

**All the cases for one pair.** For $x = $ TTCAGTAC and $y = $ AGTACGGA:

| form | score |
|---|---|
| global | $-2$ |
| overlap, $x$ then $y$ | 10 |
| overlap, $y$ then $x$ | 4 |
| fitting $y$ into $x$ | 4 |
| fitting $x$ into $y$ | 4 |
| all ends free | 10 |
| local, for comparison | 10 |

Only the overlap in the right order finds the shared AGTAC without a penalty. The overlap in the other order, $y$ then $x$, asks whether the end of AGTACGGA matches the start of TTCAGTAC, which is not the case here.

## Known algorithms

| algorithm | gaps | time (worst case) | space |
|---|---|---|---|
| [Semi-global DP](/semi-global-dp/) | linear | $\Theta(mn)$ | $\Theta(mn)$, or $\Theta(\min(m, n))$ for the score |
| Semi-global flags on the [Gotoh algorithm](/gotoh-algorithm/) | affine | $\Theta(mn)$ | $\Theta(mn)$ |
| [Sellers' algorithm](/sellers-algorithm/) | unit costs, fitting a pattern into a text | $\Theta(mn)$ | $\Theta(m)$ for a pattern of length $m$ |
| [Banded alignment](/banded-alignment/) with free ends | linear or affine | $O(k \max(m, n))$ for a band of width $k$ | |
| [Myers bit-parallel algorithm](/myers-bit-parallel-algorithm/) | unit costs, fitting | $O(\lceil m / w \rceil n)$ for a machine word of $w$ bits | |

To get the alignment in linear space, find the end cell with a score-only pass, find the start cell with a second pass over the reversed sequences, and align the part between them with [Hirschberg's algorithm](/hirschberg-algorithm/).

## Bounds

- **Upper.** $O(mn)$ time for every choice of flags, with linear or affine gaps.
- **Lower, conditional.** Global alignment reduces to every form of semi-global alignment (see below), so the bounds of [global alignment](/global-alignment/) carry over: under the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/), no $O(n^{2 - \varepsilon})$ algorithm exists for a constant $\varepsilon > 0$.
- **Lower, trivial.** $\Omega(m + n)$ to read the input.

## Reductions

- **To global alignment.** Each named case is a maximum of global problems over prefixes, suffixes or substrings, as in the table of the definition. For fitting $y$ into $x$ this takes one global problem for each of the $O(m^2)$ substrings of $x$. The [semi-global DP](/semi-global-dp/) avoids this factor with a border of zeros and a maximum over the last row or column.
- **From global alignment.** Add two new letters $\#$ and $\$$, and set $s(\#, \#) = s(\$, \$) = C$ for a $C$ larger than the largest possible change of score, $(m + n)(\max |s| + d)$, and score them $-C$ against every other letter. Align $\#x\$$ with $\#y\$$ with any flags. An optimal alignment pairs $\#$ with $\#$ and $\$$ with $\$$, so no gap column is leading or trailing, and the score is $2C$ plus the global score of $x$ and $y$.
- **To a longest path.** In the [alignment graph](/alignment-graph/), the free leading gaps are edges of weight 0 on the left or top border, and the free trailing gaps are edges of weight 0 from the last column or row to a sink.

## Applications

- **Genome assembly.** [Overlap detection](/overlap-detection/) aligns a suffix of one read with a prefix of another; the overlaps are the edges of the [overlap graph](/overlap-graph/).
- **Read mapping.** A read must align over its full length to a part of the reference: fitting the read into the reference, usually inside a band around a seed hit ([read mapping](/read-mapping/)).
- **Adapter and primer trimming.** An adapter at the end of a read is found by an overlap alignment of the read with the adapter sequence.
- **Pattern search.** Fitting a short sequence, such as a primer or a motif, into a long one finds where it occurs with a few differences ([approximate string matching](/approximate-string-matching/)).

## References
