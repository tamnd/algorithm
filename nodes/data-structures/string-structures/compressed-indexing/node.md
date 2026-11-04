---
tag: KGGFKJ
kind: concept
slug: compressed-indexing
name: Compressed full-text indexing
aliases:
- compressed text indexing
area: data-structures/string-structures
level: research
summary: Indexing a text in space close to its compressed size while keeping fast substring queries.
prereqs: [full-text-index, suffix-array, burrows-wheeler-transform]
see_also: [fm-index, compressed-suffix-array, compressed-suffix-tree, lz-index, r-index, wavelet-tree, succinct-data-structures, suffix-array]
sources:
  - paper: Gonzalo Navarro and Veli Mäkinen, Compressed full-text indexes, ACM Computing Surveys 39(1), 2007, doi:10.1145/1216370.1216372
    locator: article 2, the survey of self-indexes, the empirical entropy H_k, the operations count, locate and extract, backward search, and the families based on compressed suffix arrays, the FM-index and Lempel-Ziv parsing
  - paper: Paolo Ferragina and Giovanni Manzini, Opportunistic data structures with applications, 41st Annual Symposium on Foundations of Computer Science (FOCS 2000), doi:10.1109/SFCS.2000.892127
    locator: pages 390 to 398, the FM-index, backward search on the Burrows-Wheeler transform, and space bounded by the k-th order entropy of the text
  - paper: Roberto Grossi and Jeffrey Scott Vitter, Compressed suffix arrays and suffix trees with applications to text indexing and string matching, SIAM Journal on Computing 35(2), 2005, doi:10.1137/S0097539702402354
    locator: pages 378 to 407, the compressed suffix array with the function Ψ, in space proportional to the text in bits
  - paper: Travis Gagie, Gonzalo Navarro and Nicola Prezza, Fully functional suffix trees and optimal text searching in BWT-runs bounded space, Journal of the ACM 67(1), 2020, doi:10.1145/3375890
    locator: article 2, the r-index, which locates occurrences in space proportional to the number r of runs of the Burrows-Wheeler transform
---

Compressed full-text indexing is the design of indexes that answer substring queries on a text while taking space close to the size of the compressed text, rather than the $\Theta(n \log n)$ bits of a [suffix tree](/suffix-tree/) or a [suffix array](/suffix-array/). Most such indexes are *self-indexes*: they replace the text, since any part of it can be extracted from the index. The three main families are the [compressed suffix array](/compressed-suffix-array/), the [FM-index](/fm-index/) on the Burrows-Wheeler transform, and indexes on a Lempel-Ziv parsing such as the [LZ-index](/lz-index/). This page explains the idea common to them; each structure has its own page.

## In plain words

A suffix array of a text of $n$ letters is a list of $n$ numbers, each $\log_2 n$ bits. For a genome of three billion letters that is many times the size of the genome itself, which needs only two bits per letter, and even less if it is compressed.

Compressed indexes store the same information in a form that exploits the regularities of the text. The idea is that the sorted order of the suffixes is itself very regular when the text is: neighboring suffixes in sorted order tend to come from neighboring places. So the index can be compressed about as well as the text, and the text can be thrown away, because the index can rebuild any part of it.

## The idea

**The measure of compressibility.** For a text $T$ over an alphabet of size $\sigma$, the zero-order empirical entropy $H_0(T)$ is the entropy of the symbol frequencies, and the $k$-th order empirical entropy $H_k(T)$ is the average entropy of the symbol that follows each context of $k$ symbols. $n H_k(T)$ is a lower bound for the output of compressors that code each symbol by its preceding $k$ symbols, and $H_k(T) \le H_0(T) \le \log_2 \sigma$. A compressed index aims at $n H_k(T) + o(n \log \sigma)$ bits, or a small constant times $n H_k(T)$.

**The operations.** A self-index supports three queries, for a pattern $P$ of length $m$:

- *count*: the number of occurrences of $P$;
- *locate*: the positions of the occurrences;
- *extract*: the substring $T[i \ldots j]$, which replaces access to the text.

**How the suffix order is compressed.** The suffix array $SA$ itself looks random, but two functions derived from it are compressible. The function $\Psi(r) = SA^{-1}[SA[r] + 1]$, the rank of the suffix that follows the $r$-th suffix in text order, is increasing on each range of suffixes that start with the same symbol, so it can be stored with gap encoding; this is the basis of the compressed suffix array of Grossi and Vitter. Its inverse, the LF mapping, is computed from the Burrows-Wheeler transform $L$ with rank queries, $LF(r) = C[L[r]] + rank_{L[r]}(L, r)$, where $C[c]$ counts the symbols smaller than $c$; this is the basis of the FM-index of Ferragina and Manzini. Storing $L$ with a compressed [wavelet tree](/wavelet-tree/) or similar structure reaches $n H_k(T) + o(n \log \sigma)$ bits.

**Backward search.** With the LF mapping, counting needs no access to $SA$. The suffixes that start with a string $cX$ are those whose next suffix starts with $X$ and whose first symbol is $c$, so their range is computed from the range of $X$ by two rank queries. Reading $P$ from right to left gives the range of $P$ in $m$ steps of $O(1)$ rank queries each.

**Sampling.** To locate an occurrence, the index keeps $SA[r]$ only for the suffixes whose position is a multiple of a parameter $s$. From any other row, it applies $LF$ or $\Psi$ until it reaches a sampled row, at most $s - 1$ steps, and adds the number of steps. This costs $O((n / s) \log n)$ bits and $O(s)$ steps per occurrence, the basic time and space trade-off of compressed indexes. Extraction uses the same samples, in the other direction.

**Repetitive texts.** Collections of similar documents, such as many genomes of one species, have small $H_k$ per symbol but are far more compressible than $H_k$ shows, because long parts repeat. Indexes based on the number $r$ of runs in the Burrows-Wheeler transform, such as the [r-index](/r-index/), or on [LZ77](/lz77/) and grammar compression, take space proportional to these repetitions instead.

## Examples

**Backward search on banana.** For $T = $ banana\$, the sorted rotations are \$banana, a\$banan, ana\$ban, anana\$b, banana\$, na\$bana and nana\$ba, so the Burrows-Wheeler transform is $L = $ annb\$aa, and $C[\$] = 0$, $C[a] = 1$, $C[b] = 4$, $C[n] = 5$. Counting ana proceeds from the last symbol:

| step | symbol | range of rows |
|---|---|---|
| 1 | a | $[C[a], C[b]) = [1, 4)$ |
| 2 | n | $[5 + rank_n(L, 1), 5 + rank_n(L, 4)) = [5, 7)$ |
| 3 | a | $[1 + rank_a(L, 5), 1 + rank_a(L, 7)) = [2, 4)$ |

The final range has 2 rows, ana\$ban and anana\$b, so ana occurs twice, at positions 3 and 1. The index never read the text or the suffix array.

**The three families.** The compressed suffix array stores $\Psi$ in compressed form and searches by binary search over the suffixes, using $\Psi$ to read their symbols. The FM-index stores the Burrows-Wheeler transform with rank support and counts by backward search. The LZ-index stores the tries of the LZ78 phrases and finds occurrences by how they cross phrase boundaries; it locates quickly but cannot count without listing.

**Compressed suffix trees.** Adding a compressed LCP array and a succinct tree to a compressed suffix array gives a [compressed suffix tree](/compressed-suffix-tree/), which supports the navigation of a suffix tree in compressed space at the cost of slower operations.

## Where it is used

- **Bioinformatics.** Read aligners map short DNA reads to a reference genome with an FM-index of the genome, which fits in memory where a suffix tree would not.
- **Collections of genomes and versioned documents.** Run-length and Lempel-Ziv based indexes store many similar sequences in space close to their differences.
- **Search in large text collections.** Self-indexes support substring search where an [inverted index](/inverted-index/) of words does not apply, for example in East Asian languages without word separators, in source code, or in DNA and protein sequences.
- **Succinct data structure libraries.** The same building blocks, rank and select on bit vectors and wavelet trees, are used for compressed indexes and for other [succinct data structures](/succinct-data-structures/).

## References
