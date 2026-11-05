---
tag: BSBQWW
kind: data-structure
slug: fm-index
name: FM-index
aliases:
- Ferragina-Manzini index
area: strings/suffix-structures
level: advanced
summary: A compressed full-text index built from the Burrows-Wheeler transform, with backward search.
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, σ: the alphabet size, s: the sampling step of the suffix array, k: the number of occurrences}
  time: {worst: O((m + k s) log σ)}
  space: {extra: O(n log σ / log n + n / s)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [burrows-wheeler-transform, suffix-array, wavelet-tree]
see_also: [compressed-suffix-array, r-index, full-text-index, burrows-wheeler-transform, wavelet-tree, rank-select-problem, compressed-suffix-tree, inverse-burrows-wheeler-transform]
sources:
  - paper: doi:10.1109/SFCS.2000.892127
    title: Paolo Ferragina and Giovanni Manzini, Opportunistic data structures with applications, 41st IEEE Symposium on Foundations of Computer Science (FOCS), 2000
    locator: pages 390 to 398, the first description of backward search on the BWT and of the sampled locate
  - paper: doi:10.1145/1082036.1082039
    title: Paolo Ferragina and Giovanni Manzini, Indexing compressed text, Journal of the ACM 52(4), 2005
    locator: pages 552 to 581, the counting, locating and extracting procedures and the space bound in terms of the empirical entropy
  - paper: doi:10.1145/1216370.1216372
    title: Gonzalo Navarro and Veli Mäkinen, Compressed full-text indexes, ACM Computing Surveys 39(1), 2007
    locator: the sections on the backward search, the FM-index family and the wavelet tree representation of the BWT
---

The FM-index of a text $T$ of length $n$ is a [full-text index](/full-text-index/) made of the [Burrows-Wheeler transform](/burrows-wheeler-transform/) of $T$, a small table of symbol counts, a [rank](/rank-select-problem/) structure on the transform and a sample of the [suffix array](/suffix-array/). It counts the occurrences of a pattern of length $m$ with $m$ steps of *backward search*, each two rank queries, and reports each occurrence by walking the LF mapping to a sampled position. Its size is close to the size of the compressed text, so it replaces the suffix array where memory is tight, as in DNA read aligners.

## In plain words

Sort all endings of a text, and for each one write down the letter just before it. This column, the Burrows-Wheeler transform, often has long runs of one letter, so it compresses well.

To find a word, read it from its last letter to its first. First take all sorted endings that start with the last letter: they form one block of rows. Then ask which of these rows have the second-to-last letter just before them. Simple counts in the column tell you where the new block starts and ends. Each letter of the word shrinks the block, and the size of the last block is the number of times the word occurs.

To find where each match is, keep the text position only for some rows, and step back through the text from a match until you reach one of these rows.

## The abstract type

The structure is static. It is built once from a text $T$ and supports:

- `count(P)`: the number of occurrences of $P$ in $T$;
- `locate(P)`: the start positions of the occurrences of a nonempty $P$;
- `extract(l, r)`: the substring $T[l \ldots r-1]$, so that the text itself need not be kept.

Because `extract` gives back any part of $T$, the index can replace the text: it is a *self-index*.

## Representation

The text $T = T[0 \ldots n-1]$ is over a general ordered alphabet of $\sigma$ symbols, coded $1, \ldots, \sigma$ in their order. A sentinel $\$$, the code 0, is appended: it occurs once and is smaller than every symbol. Let $T' = T\$$, of length $n + 1$. Positions and rows are 0-based. Let $SA$ be the suffix array of $T'$, so that $SA[0] = n$ is the suffix $\$$.

- $L$, the BWT: $L[i] = T'[SA[i] - 1]$, and $L[i] = \$$ when $SA[i] = 0$. The first column $F[i] = T'[SA[i]]$ is the sorted text and is not stored.
- $C[c]$, for each symbol $c$: the number of symbols of $T'$ smaller than $c$. The rows whose suffixes start with $c$ are $C[c]$ to $C[c+1] - 1$.
- A rank structure: $\mathrm{rank}_c(L, i)$ is the number of rows $r < i$ with $L[r] = c$. The implementation stores the counts of all symbols at every $b$-th row and scans at most $b - 1$ symbols; a [wavelet tree](/wavelet-tree/) answers it in $O(\log \sigma)$ time for any alphabet.
- A sample of $SA$: the value $SA[i]$ for each row with $SA[i] \bmod s = 0$, and for the extraction the row of each position $p \bmod s = 0$ and of $p = n$.

**The LF mapping.** $\mathrm{LF}(i) = C[L[i]] + \mathrm{rank}_{L[i]}(L, i)$ is the row of the suffix that starts one position before the suffix of row $i$: if $SA[i] = p > 0$, then $SA[\mathrm{LF}(i)] = p - 1$. The $j$-th occurrence of a symbol $c$ in $L$ and the $j$-th occurrence of $c$ in $F$ are the same position of the text.

## Operations

```pseudo id=main
FM-LOCATE(P)                             ▷ rows of T$ are 0 .. n; P is nonempty
L1  sp ← 0; ep ← n + 1                    ▷ the rows [sp, ep) whose suffixes start with the part of P read so far
L2  for j ← m − 1 down to 0 do
L3      c ← P[j]; if c is not in the alphabet then return the empty list
L4      sp ← C[c] + rank_c(L, sp); ep ← C[c] + rank_c(L, ep)
L5      if sp ≥ ep then return the empty list
L6  for each row i in [sp, ep) do
L7      t ← 0
L8      while SA[i] is not sampled do i ← LF(i); t ← t + 1
L9      report SA[i] + t
L10 return the reported positions in increasing order
```

**Count.** Lines L1 to L5 alone are `count`: the answer is $ep - sp$. For the empty pattern the range is all $n + 1$ rows, which counts the empty string at every position including $n$.

**Locate.** Lines L6 to L9 walk from each row of the range to the left in the text with LF until they reach a sampled row. Each step moves one position to the left, so at most $s - 1$ steps are needed, since position 0 is sampled.

**Extract.** To get $T[l \ldots r-1]$, start at the row of the smallest sampled position $p \ge r$ (or $p = n$), and repeat $p - l$ times: output $L[i] = T[p-1]$, set $i \leftarrow \mathrm{LF}(i)$ and $p \leftarrow p - 1$. Keep the symbols of positions $l$ to $r - 1$ and reverse them.

## Example

The text is $T = \texttt{banana}$, so $T' = \texttt{banana\$}$ and $n = 6$. The sampling step is $s = 2$.

| row $i$ | $SA[i]$ | suffix | $L[i]$ | sampled |
|---|---|---|---|---|
| 0 | 6 | \$ | a | yes |
| 1 | 5 | a\$ | n | |
| 2 | 3 | ana\$ | n | |
| 3 | 1 | anana\$ | b | |
| 4 | 0 | banana\$ | \$ | yes |
| 5 | 4 | na\$ | a | yes |
| 6 | 2 | nana\$ | a | yes |

So $L = \texttt{annb\$aa}$, and $C[\$] = 0$, $C[\texttt{a}] = 1$, $C[\texttt{b}] = 4$, $C[\texttt{n}] = 5$, with $7$ symbols in all.

**Backward search for `ana`.** Start with $[0, 7)$.

| symbol | $\mathrm{rank}_c(L, sp)$, $\mathrm{rank}_c(L, ep)$ | new range | rows |
|---|---|---|---|
| a | 0, 3 | $[1 + 0, 1 + 3) = [1, 4)$ | a\$, ana\$, anana\$ |
| n | 0, 2 | $[5 + 0, 5 + 2) = [5, 7)$ | na\$, nana\$ |
| a | 1, 3 | $[1 + 1, 1 + 3) = [2, 4)$ | ana\$, anana\$ |

So `ana` occurs $4 - 2 = 2$ times. To locate them: row 2 is not sampled, and $\mathrm{LF}(2) = C[\texttt{n}] + \mathrm{rank}_\texttt{n}(L, 2) = 5 + 1 = 6$, with $SA[6] = 2$, so the occurrence is at $2 + 1 = 3$. Row 3 goes to $\mathrm{LF}(3) = C[\texttt{b}] + 0 = 4$, with $SA[4] = 0$, so the occurrence is at $0 + 1 = 1$. The answer is $[1, 3]$.

For `nab`, the range after `b` is $[4, 5)$, and after `a` it is $[1 + 1, 1 + 1)$, which is empty, so `nab` does not occur.

## Correctness

The full proof is in the proof file of this page. It rests on two lemmas.

1. **LF.** For a symbol $c$, the rows $i$ with $L[i] = c$, in increasing order, are the suffixes $cX$ of $T'$ in the order of $X$, which is their order as suffixes $cX$. So the $j$-th of them goes to row $C[c] + j$, and that is $\mathrm{LF}(i)$.
2. **Backward search.** If $[sp, ep)$ is the range of rows whose suffixes start with $Q$, then the rows whose suffixes start with $cQ$ are exactly $\mathrm{LF}(i)$ for the rows $i \in [sp, ep)$ with $L[i] = c$. By the first lemma, these form the range from $C[c] + \mathrm{rank}_c(L, sp)$ to $C[c] + \mathrm{rank}_c(L, ep)$. By induction over the symbols of $P$ from the last one, line L5 or the end of the loop gives the range of $P$.

Locate is correct because each LF step lowers the text position by one, and extract is correct because $L[i] = T'[SA[i] - 1]$.

## Complexity

| operation | time with checkpoints every $b$ rows | time with a wavelet tree |
|---|---|---|
| build | $O(n \log n)$ in the implementation; $O(n)$ with a linear suffix sort for an integer alphabet | the same plus $O(n \log \sigma)$ |
| `count(P)` | $O(m b)$ | $O(m \log \sigma)$ |
| `locate(P)` | the count plus $O(k s b)$ | the count plus $O(k s \log \sigma)$ |
| `extract(l, r)` | $O((r - l + s) b)$ | $O((r - l + s) \log \sigma)$ |

**Space.** $L$ takes $n \lceil \log_2 (\sigma + 1) \rceil$ binary digits, and less when it is compressed. The checkpoints take $(n / b)\,\sigma$ counters. The samples take about $2n/s$ words. Ferragina and Manzini showed that with a compressed $L$ the space is bounded by a constant times $n H_k(T)$ plus lower-order terms, where $H_k$ is the $k$-th order empirical [entropy](/shannon-entropy/) of the text; with a wavelet tree on a compressed $L$ it is $n H_k(T) + o(n \log \sigma)$ for small $k$. A plain suffix array takes $n$ words of $\log_2 n$ binary digits, often four or eight times the text.

The parameter $s$ trades space for locate time, and $b$ trades space for rank time.

## Variants

- **Wavelet tree FM-index.** The BWT in a [wavelet tree](/wavelet-tree/) of compressed [bit vectors](/bit-vector/) gives $O(\log \sigma)$ rank for any alphabet and entropy-bounded space; a [wavelet matrix](/wavelet-matrix/) does the same for large alphabets.
- **Run-length FM-index and the r-index.** For repetitive text, $L$ has few runs $r$. The run-length FM-index stores $L$ in $O(r)$ words, and the [r-index](/r-index/) also locates in $O(r)$ words, without the $n/s$ samples.
- **Bidirectional FM-index.** Indexes of $T$ and of its reverse, kept in step, extend a match to the left or to the right; read aligners use it for search with mismatches.
- **Compressed suffix arrays.** The [compressed suffix array](/compressed-suffix-array/) of Grossi and Vitter and of Sadakane uses the $\Psi$ function, the inverse of LF, in place of the BWT. The [compressed suffix tree](/compressed-suffix-tree/) adds an LCP array and the tree shape to an FM-index or a CSA.
- **Document indexes.** For a collection of documents joined by separators, an FM-index with extra structures answers [document listing](/document-listing/).

## When to use it

Use the FM-index to search a large, fixed text when a suffix array or suffix tree does not fit in memory: genomes and read alignment, large logs, versioned documents. Counting is fast and needs only the BWT and $C$. Locating many occurrences is slower than with a plain suffix array, by a factor near $s$. For text that changes often, or when memory is not a concern, a plain [suffix array](/suffix-array/) is simpler and faster. For highly repetitive collections, use the [r-index](/r-index/).

## Pitfalls

- **The sentinel.** Without a unique smallest end symbol, the rotations and the suffixes sort differently and the LF lemma fails. If the text can contain the code 0, shift the codes first.
- **Half-open ranges.** $\mathrm{rank}_c(L, i)$ counts the rows strictly before $i$. Mixing it with an inclusive count shifts $sp$ or $ep$ by one.
- **Symbols not in the text.** A pattern symbol with no code must give an empty range at once; $C[c]$ is not defined for it.
- **Sampling position 0.** If no sampled row reaches position 0, the LF walk from the row of the suffix at 0 goes to the row of $\$$ and on, and the count of steps is wrong. Sample by text position, not by row, so that the walk is at most $s - 1$ steps.
- **Large alphabets.** Checkpoints with one counter per symbol take $n\sigma/b$ counters; for bytes or words use a wavelet tree.

## Implementations

The Python class builds the suffix array by prefix doubling with library sorts, then $L$, $C$, the rank checkpoints and the two samples. The tests compare `count` and `locate` with a direct scan, `extract` with slicing and the BWT with sorting all rotations, on random strings over alphabets of size 1, 2 and 4 and on $\texttt{a}^n$ and $(\texttt{ab})^n$.

## History

Burrows and Wheeler introduced their transform for compression in 1994. In 2000, Paolo Ferragina and Giovanni Manzini showed at FOCS that the transform plus small extra structures is a full-text index, with backward search for counting and sampled positions for locating, in space bounded by the entropy of the text; they called such structures opportunistic. The name FM-index comes from their initials, and the journal version, "Indexing compressed text", appeared in the Journal of the ACM in 2005. Later work replaced the rank structure by wavelet trees and run-length codes, and the read aligners Bowtie and BWA made the FM-index a standard tool in genomics.

## References
