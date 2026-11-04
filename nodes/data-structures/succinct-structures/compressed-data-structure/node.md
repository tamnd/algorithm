---
tag: BNCX01
kind: concept
slug: compressed-data-structure
name: Compressed data structure
aliases:
- entropy-compressed data structure
area: data-structures/succinct-structures
level: advanced
summary: A structure whose space adapts to the compressibility of the input, such as its empirical entropy, rather than to its raw size.
prereqs: [succinct-data-structures, shannon-entropy]
see_also: [rrr-bitvector, sd-array, wavelet-tree, fm-index, compressed-suffix-array, compressed-indexing, r-index, grammar-based-compression]
sources:
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 2, Sections 2.1 (Worst-Case Entropy) and 2.3 (Empirical Entropy), and Chapter 4, Section 4.1.1 (Zero-Order Compression)
  - paper: doi:10.1145/1216370.1216372
    title: Gonzalo Navarro and Veli Mäkinen, Compressed full-text indexes, ACM Computing Surveys 39(1), Article 2, 2007
    locator: Section 2 (the empirical entropies H0 and Hk of a text) and the classification of self-indexes by their space in terms of nHk
  - paper: doi:10.1145/1290672.1290680
    title: Rajeev Raman, Venkatesh Raman and S. Srinivasa Rao, Succinct indexable dictionaries with applications to encoding k-ary trees, prefix sums and multisets, ACM Transactions on Algorithms 3(4), Article 43, 2007
    locator: the bit vector in lg C(n, m) + o(n) bits, the first compressed structure for rank and select
---

A compressed data structure answers queries about an object in space bounded by a measure of how compressible that particular object is, such as its empirical entropy $n H_k$, plus a lower-order term, instead of in space bounded by the size of the whole class of objects. A [succinct data structure](/succinct-data-structures/) uses about $\lg N$ bits for a class of $N$ objects, the same for every member; a compressed one uses less for the members that are easy to compress, and about the same for the others. The [RRR bit vector](/rrr-bitvector/), the [wavelet tree](/wavelet-tree/) on compressed bit vectors and the [FM-index](/fm-index/) are the standard examples.

## In plain words

A succinct structure takes about as many bits as the number of possible inputs requires, and that is a fixed amount for all inputs of the same size. But most real inputs are far from random. A long text in English repeats words, a row of bits may be almost all 0s, and a collection of genomes repeats the same genome with small changes.

A compressed structure takes advantage of this. Its size goes down when the input has patterns that a compressor would find, and it can still answer questions without being unpacked first. The measure of size is usually the entropy of the input, which is the length that a good compressor would reach, or the number of pieces in which the input can be described.

## The idea

**Empirical entropy of order zero.** For a string $T$ of length $n$ in which symbol $c$ occurs $n_c$ times,

$$H_0(T) = \sum_{c} \frac{n_c}{n} \lg \frac{n}{n_c},$$

the [Shannon entropy](/shannon-entropy/) of the symbol frequencies of $T$. No code that encodes each symbol by a fixed codeword can use fewer than $n H_0(T)$ bits for $T$. For a bit vector with $m$ ones, $n H_0 = n \cdot H(m/n)$ with $H$ the [binary entropy function](/binary-entropy-function/), and $\lg \binom{n}{m} = n H_0 - O(\lg n)$.

**Empirical entropy of order $k$.** For each string $s$ of length $k$, let $T_s$ be the string of the symbols that follow the occurrences of $s$ in $T$. Then

$$n H_k(T) = \sum_{|s| = k} |T_s| \, H_0(T_s).$$

This is the space of a code that may choose the codeword of each symbol by the $k$ symbols before it. It satisfies $H_k \le H_{k-1} \le \cdots \le H_0 \le \lg \sigma$ for an alphabet of $\sigma$ symbols.

**The two levels.** Following Navarro and Mäkinen, a structure for strings over $\sigma$ symbols is *compressed* if it uses $n H_k(T) + o(n \lg \sigma)$ bits, often for all $k \le \alpha \log_\sigma n$ with a constant $0 < \alpha < 1$, and *zero-order compressed* if it uses $n H_0(T) + o(n \lg \sigma)$ bits. For a bit vector, $\lg \binom{n}{m} + o(n)$ bits is zero-order compressed. The lower-order term is $o$ of the size of the plain object, not of the entropy, which is why a compressed structure can be larger than the entropy by a large factor when the object is very compressible.

**Beyond entropy.** For highly repetitive data, such as versions of a document, $n H_k$ stays close to the entropy of one copy times the number of copies, and so it does not capture the repetition. Measures such as the number $z$ of [Lempel-Ziv](/lz77/) phrases, the size $g$ of a [grammar](/grammar-based-compression/), or the number $r$ of runs in the [Burrows-Wheeler transform](/burrows-wheeler-transform/) do. Structures in $O(z)$, $O(g)$ or $O(r)$ words of space, such as the [r-index](/r-index/), are compressed in this stronger sense.

## Examples

**A sparse bit vector.** Take $n = 2^{20}$ bits with $m = 2^{16}$ ones. A succinct [rank/select dictionary](/rank-select-dictionary/) uses $n + o(n) = 1{,}048{,}576$ bits plus its index. Here $H_0 = H(1/16) \approx 0.337$, so $n H_0 \approx 353{,}674$ bits and $\lg \binom{n}{m} \approx 353{,}665$ bits. The [RRR bit vector](/rrr-bitvector/) stores it in about $353{,}665$ bits plus $O(n \lg \lg n / \lg n)$, and the [SD-array](/sd-array/) in $m(\lfloor \lg 16 \rfloor + 2) = 393{,}216$ bits plus a small index.

**A short text.** For $T = $ abracadabra, $n = 11$, with $a$ five times, $b$ and $r$ twice, and $c$ and $d$ once. Then $n H_0(T) \approx 22.4$ bits, while a fixed code of $\lceil \lg 5 \rceil = 3$ bits per symbol uses 33. For $k = 1$, the strings of followers are $T_a = $ bcdb, $T_b = $ rr, $T_r = $ aa, $T_c = $ a and $T_d = $ a. Only $T_a$ has positive entropy, $4 \cdot 1.5 = 6$ bits, so $n H_1(T) = 6$ bits: after a $b$ comes an $r$, and after $r$, $c$ or $d$ comes an $a$.

**Sequences and text indexes.** A [wavelet tree](/wavelet-tree/) whose bit vectors are RRR vectors stores a [static sequence](/static-sequence/) in $n H_0 + o(n \lg \sigma)$ bits with access, rank and select in $O(\lg \sigma)$ time. Applied to the Burrows-Wheeler transform of $T$ with one tree for each context block, it gives the [FM-index](/fm-index/) in $n H_k(T) + o(n \lg \sigma)$ bits, a [compressed suffix array](/compressed-suffix-array/) that also replaces the text.

**A non-example.** A plain [bit vector](/bit-vector/) with a rank and select index uses $n + o(n)$ bits whatever its content; it is succinct for the class of all bit vectors of length $n$ but not compressed.

## Where it is used

- Compressed bit vectors: the [RRR bit vector](/rrr-bitvector/), the [SD-array](/sd-array/) and [Elias-Fano](/elias-fano-encoding/), and the [fully indexable dictionary](/fully-indexable-dictionary/).
- Sequences over larger alphabets: the [wavelet tree](/wavelet-tree/) and the [wavelet matrix](/wavelet-matrix/) with compressed bit vectors or Huffman shape.
- Text indexes: the [FM-index](/fm-index/), the [compressed suffix array](/compressed-suffix-array/), the [compressed suffix tree](/compressed-suffix-tree/), and [compressed indexing](/compressed-indexing/) in general.
- Repetitive collections: the [r-index](/r-index/) and grammar-based indexes for genomes and versioned documents.
- Posting lists of [inverted indexes](/inverted-index/), stored with Elias-Fano and its partitioned variants.

## References
