---
tag: 6F6TAM
kind: algorithm
slug: burrows-wheeler-transform
name: Burrows-Wheeler transform
aliases:
- BWT
- block-sorting transform
area: compression-and-coding/transforms-for-compression
level: core
summary: Sort all rotations of a string and output the last symbol of each. The output is invertible and puts symbols with the same context together, so it has long runs.
model: word-ram
complexity:
  vars: {n: the length of the text over an integer alphabet of size at most n}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true, online: false, comparison: false}
history:
  year: 1994
  people: [Michael Burrows, David Wheeler]
  note: Burrows and Wheeler described the transform in SRC Research Report 124 of Digital Equipment Corporation in 1994. Wheeler had found the transform in 1983.
prereqs: [suffix-array, sentinel-character, lossless-compression]
see_also: [inverse-burrows-wheeler-transform, bijective-burrows-wheeler-transform, move-to-front-transform, run-length-encoding, sa-is, fm-index, r-index, context-modeling]
sources:
  - paper: "Michael Burrows and David J. Wheeler, A block-sorting lossless data compression algorithm, SRC Research Report 124, Digital Equipment Corporation, Palo Alto, California, 1994"
    title: Burrows and Wheeler 1994
    locator: Section 2 (the transform by a sort of the rotations, the index of the original row, and the reverse transform) and Section 3 (why the output compresses well, with a move-to-front coder)
  - paper: doi:10.1145/382780.382782
    title: Giovanni Manzini, An analysis of the Burrows-Wheeler transform, Journal of the ACM 48(3), 2001
    locator: pages 407 to 430 (bounds on the output of BWT plus move-to-front plus an order-0 coder in terms of the k-th order empirical entropy, for every input string)
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 2 (empirical entropy H_k) and Chapter 11 (the BWT, its relation to the suffix array, and the FM-index)
  - url: https://sourceware.org/bzip2/manual/manual.html
    title: Julian Seward, bzip2 and libbzip2, the manual of version 1.0.8
    locator: Section 2, How to use bzip2 (block sizes of 100k to 900k bytes, set by the flags -1 to -9)
---

The Burrows-Wheeler transform (BWT) is a reversible permutation of a string: it sorts all rotations of the string and outputs the last symbol of each rotation in sorted order. Symbols that are followed by the same text end up next to each other, so the output has long runs of equal symbols, which a [move-to-front](/move-to-front-transform/) step and an entropy coder then compress well. With a [suffix array](/suffix-array/) built in linear time, the transform takes $\Theta(n)$ time, and the [inverse transform](/inverse-burrows-wheeler-transform/) also takes $\Theta(n)$ time. It is the core of the bzip2 compressor and of the [FM-index](/fm-index/).

## In plain words

Write the text in a circle and read it from each start position. This gives as many strings as the text has symbols. Sort these strings like words in a dictionary and write them in a column, one under the other. Now read the last symbol of each line, from top to bottom. That column is the output.

Lines that start with the same letters are next to each other after the sort. The last symbol of a line is the symbol just before those letters in the text. In English, the letters before "he " are nearly always "t" or "s", so the output gets long groups of the same letter. The output has the same symbols as the input, only in a different order. A short extra mark lets the receiver undo the shuffle.

## The problem

**Notation.** The text is $T = T[0 \ldots n-1]$ over an ordered alphabet $\Sigma$ of size $\sigma$. We append a sentinel $\$$, a symbol that is not in $\Sigma$ and is smaller than each symbol of $\Sigma$ (see [sentinel character](/sentinel-character/)). Let $T' = T\$$, of length $N = n + 1$. For $0 \le i < N$, the rotation $T'_i = T'[i \ldots N-1]\, T'[0 \ldots i-1]$. The suffix array $SA$ of $T'$ lists the start positions of the suffixes of $T'$ in increasing order.

**The convention of this page.** The BWT of $T$ is the string $L[0 \ldots n]$ of length $n + 1$ with

$$L[i] = T'[SA[i] - 1] \text{ if } SA[i] > 0, \qquad L[i] = \$ \text{ if } SA[i] = 0.$$

Equivalently, $L$ is the last column of the matrix whose rows are the $N$ rotations of $T'$ in sorted order. The first column of that matrix is $F$, the symbols of $T'$ in sorted order.

**The convention of the 1994 report.** Burrows and Wheeler used no sentinel. They sort the $n$ rotations of $T$ itself, output the last column $L_{\mathrm{rot}}$ of length $n$, and output the index $I$ of a row that equals $T$. When $T$ is periodic, several rows are equal; they have the same last symbol, and any of them works as $I$.

**The two give the same information.** The sentinel form is the rotation form applied to $T'$, in which the index of the row $T'$ is redundant: it is the one row whose last symbol is $\$$. Remove the $\$$ from $L$ and keep its position; this gives $n$ symbols and one index, the same size as the pair $(L_{\mathrm{rot}}, I)$. Each form determines $T$ (by the [inverse transform](/inverse-burrows-wheeler-transform/)), so each can be computed from the other. The two strings are in general different: for $T = \texttt{banana}$, $L = \texttt{annb\$aa}$, while $(L_{\mathrm{rot}}, I) = (\texttt{nnbaaa}, 3)$.

The model is the worst case: no probability model of the text. Costs are in operations of the [word RAM](/word-ram/) with integer symbols.

## The algorithm

```pseudo id=main
BWT(T[0 .. n − 1])
L1  T′ ← T · $                         ▷ $ is unique and smaller than each symbol
L2  SA ← SUFFIX-ARRAY(T′)              ▷ n + 1 entries; SA[0] = n
L3  for i ← 0 to n do
L4      if SA[i] = 0 then L[i] ← $
L5      else L[i] ← T′[SA[i] − 1]
L6  return L
```

Line L2 builds the suffix array of $T'$, for example with [SA-IS](/sa-is/) or the [DC3 algorithm](/dc3-skew-algorithm/) in $O(n)$ time; see [suffix array construction](/suffix-array-construction/). Because $\$$ is unique and smallest, the order of the suffixes of $T'$ is the same as the order of the rotations of $T'$, so no rotation needs to be built. Lines L3 to L5 read, for each row, the symbol just before the start of its rotation. The row of the suffix that starts at 0 is the row of $T'$ itself, and its last symbol is $\$$.

The direct method follows the definition: build the $N$ rotations, sort them, and take the last symbols. It is correct but slow, and it is the oracle of the tests.

```pseudo id=rotations
BWT-BY-ROTATIONS(T[0 .. n − 1])
R1  T′ ← T · $, N ← n + 1
R2  sort the indices 0, 1, ..., N − 1 by the rotation T′[i .. N − 1] T′[0 .. i − 1]
R3  for each index i in sorted order, output T′[(i − 1) mod N]
```

The 1994 convention without a sentinel can also use a suffix array: sort the suffixes of $TT$ and keep those that start before position $n$. The first $n$ symbols of the suffix at $i < n$ are the rotation at $i$, so the order is correct up to ties between equal rotations, and equal rotations have equal last symbols.

## Example

The BWT of $T = \texttt{banana}$, with $T' = \texttt{banana\$}$ and $N = 7$:

| row $i$ | $SA[i]$ | sorted rotation | $F[i]$ | $L[i]$ |
|---|---|---|---|---|
| 0 | 6 | `$banana` | `$` | `a` |
| 1 | 5 | `a$banan` | `a` | `n` |
| 2 | 3 | `ana$ban` | `a` | `n` |
| 3 | 1 | `anana$b` | `a` | `b` |
| 4 | 0 | `banana$` | `b` | `$` |
| 5 | 4 | `na$bana` | `n` | `a` |
| 6 | 2 | `nana$ba` | `n` | `a` |

So $L = \texttt{annb\$aa}$. The three rows that start with `a` have the last symbols `n`, `n`, `b`. These are exactly the symbols before the three `a` in `banana`. In the same way, both rows that start with `n` end in `a`.

For $T = \texttt{abracadabra}$, $SA = [11, 10, 7, 0, 3, 5, 8, 1, 4, 6, 9, 2]$ and $L = \texttt{ard\$rcaaaabb}$. The rows that start with `b` (`bra$abracada` and `bracadabra$a`) both end in `a`, and the rows that start with `r` both end in `b`: in the text, each `b` comes after an `a`, and each `r` after a `b`. Without a sentinel, the sorted rotations of `abracadabra` give $(L_{\mathrm{rot}}, I) = (\texttt{rdarcaaaabb}, 2)$.

The effect grows with the length. The text that repeats `the cat sat on the mat and the cat ate the rat ` 20 times has 940 symbols and 940 runs (no two equal neighbours). Its BWT, with a sentinel below the space character, has 941 symbols and only 29 runs.

## Correctness

Two facts make the algorithm correct. First, because $\$$ is unique and smallest, two rotations of $T'$ compare in the same way as the two suffixes that start at the same positions; so row $i$ of the sorted rotations is the rotation that starts at $SA[i]$, and its last symbol is $T'[SA[i] - 1]$, or $\$$ when $SA[i] = 0$. Second, the output is a permutation of $T'$, because $SA$ is a permutation and $i \mapsto i - 1 \bmod N$ is a bijection. The [inverse transform](/inverse-burrows-wheeler-transform/) shows that $L$ determines $T$. The proofs are below, together with the context lemma of the next sections.

## Complexity

- **Time.** Line L2 takes $O(n)$ time with SA-IS or DC3 when the alphabet is the integers $0$ to $n$ (any alphabet can be ranked to such integers by one sort). Lines L3 to L5 take $\Theta(n)$. So the transform takes $\Theta(n)$ time in the worst case.
- **The direct method.** Sorting $N$ rotations takes $O(N \log N)$ comparisons, and one comparison reads up to $N$ symbols, so the cost is $O(n^2 \log n)$. Long runs make it slow: on $T = a^n$, the comparison of the rotations at $i$ and $j$ reads $n - \max(i, j) + 1$ symbols before it meets the $\$$.
- **Space.** The suffix array takes $n + 1$ words, and $L$ takes $n + 1$ symbols. Compressors cut the input into blocks to bound this memory: bzip2 uses blocks of 100k to 900k bytes, set by its flags -1 to -9.

## Properties

- **A permutation, not a compressor.** $L$ has the same symbols as $T\$$. The gain comes from the stages after it.
- **Context grouping.** For a word $w$ over $\Sigma$ of length $k$, the rows that start with $w$ form one block of consecutive rows, and the symbols of $L$ in this block are exactly the symbols that come just before the occurrences of $w$ in $T\$$ read as a circle (proof below).
- **Empirical entropy.** Let $T_w$ be the string of the symbols just before the occurrences of $w$ in $T$. Define $n H_k(T) = \sum_{w \in \Sigma^k} |T_w|\, H_0(T_w)$, where $H_0$ is the zero-order [empirical entropy](/shannon-entropy/). By the context lemma, the block of $w$ in $L$ is a permutation of $T_w$, with at most one extra $\$$, and only the at most $k$ rows whose first $k$ symbols hold $\$$ are outside all blocks. So a coder that codes each block with its own zero-order model reaches about $n H_k(T)$ bits, plus lower-order terms for the models of the blocks. The same $L$ serves each $k$; only the cut into blocks depends on $k$. Many texts define $H_k$ with the symbols just *after* each context; for that version, apply the BWT to the reversed text.
- **Bounds for the full pipeline.** Manzini proved that BWT followed by move-to-front and a zero-order coder outputs at most a constant times $n H_k(T)$ bits plus lower-order terms, for every $k \ge 0$ and every input string, and a sharper bound when run-length coding of zeros is added. The exact constants are in his paper; this page does not repeat them.
- **Runs.** The number of runs $r$ of $L$ is small for repetitive texts. The [r-index](/r-index/) is a full-text index in $O(r)$ words.
- **Search.** $L$ together with rank queries on it (for example with a [wavelet tree](/wavelet-tree/)) supports backward search for a pattern. This is the [FM-index](/fm-index/), a main example of [compressed indexing](/compressed-indexing/).

## Variants and improvements

- **The bzip2 pipeline.** bzip2 runs, on each block: a run-length step on runs of 4 or more equal bytes (see [run-length encoding](/run-length-encoding/)), the BWT, [move-to-front](/move-to-front-transform/), a run-length code of the runs of zeros that move-to-front makes (with two symbols, RUNA and RUNB), and [Huffman coding](/huffman-coding/) with several code tables.
- **Other second stages.** Move-to-front can be replaced by other recency transforms, such as inversion frequencies or distance coding (see [locality recoding](/locality-recoding/)), or by direct [context modeling](/context-modeling/) of $L$.
- **The bijective BWT.** Sort the rotations of the Lyndon factors in the omega order. This needs no sentinel and no index, and each string of length $n$ is the image of exactly one string. See [bijective Burrows-Wheeler transform](/bijective-burrows-wheeler-transform/).
- **Sort only the first $k$ symbols.** The sort transform of Schindler sorts the rotations by their first $k$ symbols only, with the position as the tie-break. It is faster to compute, but its inverse is more complex.
- **Reversed text.** Apply the BWT to the reverse of $T$ to group symbols by the context that comes before them, as a [prediction by partial matching](/prediction-by-partial-matching/) model does.
- **Data structure view.** The sorted rotations are the [circular suffix array](/circular-suffix-array/). The BWT can also be built from a [suffix tree](/suffix-tree/) or in compressed space.

## When to use it

Use the BWT for lossless compression of text and of other data with strong contexts, such as DNA, source code and logs, when the whole block can be in memory and the coder can work on blocks. It compresses text better than an [LZ77](/lz77/) coder with a small window, but it is slower and it cannot stream: it needs the whole block before it outputs the first symbol. Use it as the base of an index when you need pattern search in a compressed text. For data with no contexts, such as random bytes or already compressed data, it gives no gain.

## Pitfalls

- **A sentinel that is not the smallest symbol.** Line L1 needs a $\$$ that is smaller than each symbol. In ASCII, the space (32) is smaller than the dollar sign (36), so a text with spaces and the character `$` as the sentinel gives a wrong suffix order. Use a code below all symbols, for example $-1$ on integer codes.
- **A sentinel that occurs in the text.** If $\$$ is also a symbol of $T$, the order of rotations and the order of suffixes differ, and lines L4 and L5 output a wrong string. Check that the sentinel is unique, or use the byte form with an explicit index.
- **Forgetting the index.** In the 1994 convention, $L_{\mathrm{rot}}$ alone does not determine $T$: all rotations of $T$ have the same $L_{\mathrm{rot}}$. Store $I$ with the block.
- **The naive sort on repetitive data.** Sorting rotations with a general comparison sort is quadratic or worse on inputs such as long runs of one byte. Use a suffix array algorithm, or a run-length step before the BWT, as bzip2 does.
- **Expecting compression from the BWT alone.** The output has one more symbol than the input. Without the later stages, nothing is saved.
- **Using a compressor as a test oracle.** The bz2 module of Python uses the BWT inside, but it does not expose the transform, so it cannot check a BWT implementation. Compare with a direct sort of the rotations instead.

## Implementations

## History

David Wheeler found the transform in 1983 and did not publish it. Michael Burrows and David Wheeler described it, with a move-to-front coder after it, in SRC Research Report 124 of Digital Equipment Corporation in 1994. Julian Seward released bzip2, a compressor based on the transform, in 1996. Ferragina and Manzini showed in 2000 that the output also supports pattern search, which led to the FM-index. Manzini gave the first worst-case analysis of the compression in terms of $H_k$ in 2001.

## References
