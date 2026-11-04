---
tag: M9ATZ3
kind: concept
slug: succinct-data-structures
name: Succinct data structures
aliases:
- succinct representation
- succinct space
area: data-structures/succinct-structures
level: advanced
summary: Representations that use the information-theoretic minimum space plus o(n) overhead while still supporting fast queries.
prereqs: [information-theoretic-bound, asymptotic-notation, word-ram]
see_also: [compressed-data-structure, rank-select-problem, rank-select-dictionary, bit-vector, ordinal-tree, louds-tree, balanced-parentheses-representation, patrascu-succinct-lower-bound]
sources:
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 1, Section 1.1 (Why Compact Data Structures?), and Chapter 2, Section 2.1 (Worst-Case Entropy)
  - paper: doi:10.1109/SFCS.1989.63533
    title: Guy Jacobson, Space-efficient static trees and graphs, 30th Annual Symposium on Foundations of Computer Science (FOCS 1989), 549-554
    locator: the representation of n-node trees in 2n + o(n) bits with constant-time navigation
  - paper: doi:10.1137/S0097539799364092
    title: J. Ian Munro and Venkatesh Raman, Succinct representation of balanced parentheses and static trees, SIAM Journal on Computing 31(3), 2001, 762-776
    locator: Section 1 (the information-theoretic lower bound for trees and the goal of 2n + o(n) bits)
  - paper: doi:10.1145/1290672.1290680
    title: Rajeev Raman, Venkatesh Raman and S. Srinivasa Rao, Succinct indexable dictionaries with applications to encoding k-ary trees, prefix sums and multisets, ACM Transactions on Algorithms 3(4), Article 43, 2007
    locator: Section 1 (the space bound lg C(n, m) + o(n) for sets and its use for k-ary trees)
---

A succinct data structure stores an object from a class of $N$ possible objects in $\lg N + o(\lg N)$ bits, which is the [information-theoretic minimum](/information-theoretic-bound/) plus a lower-order term, and still answers the queries of the class fast, often in $O(1)$ time on the [word RAM](/word-ram/). The classic examples are a [bit vector](/bit-vector/) with [rank and select](/rank-select-problem/) in $n + o(n)$ bits, and a tree of $n$ nodes with full navigation in $2n + o(n)$ bits, where a pointer-based tree uses $\Theta(n \lg n)$ bits. Guy Jacobson started the field in 1989. Succinct structures are the base of compressed text indexes and of large in-memory graphs and trees.

## In plain words

Suppose a kind of object can take a certain number of different forms, for example all the trees with a thousand nodes. Any way to write such an object down must use at least enough bits to tell all the forms apart. That number of bits is the floor that no format can beat.

A normal data structure uses much more, because it stores pointers and counters. A succinct data structure uses almost exactly the floor, with only a small extra part that grows more slowly than the object. The surprise is that it can still answer questions about the object quickly, without unpacking it. The small extra part holds a few counts and tables, cut so that each question touches only a few machine words.

## The idea

**The minimum.** Let $\mathcal{U}_n$ be a finite class of objects of size $n$, for example the bit vectors of length $n$ with $m$ ones, or the ordered trees with $n$ nodes. A representation that can tell all objects of $\mathcal{U}_n$ apart needs at least

$$Z = \lceil \lg |\mathcal{U}_n| \rceil$$

bits for some object, because $b$ bits have only $2^b$ values. Navarro calls $Z$ the *worst-case entropy* of the class.

**The three levels.** A representation of $\mathcal{U}_n$ that supports a given set of queries is

- **implicit** if it uses $Z + O(1)$ bits;
- **succinct** if it uses $Z + o(Z)$ bits;
- **compact** if it uses $O(Z)$ bits.

The extra $o(Z)$ bits are the *redundancy*. A pointer-based tree is not even compact: it uses $\Theta(n \lg n)$ bits, while $Z = 2n - \Theta(\lg n)$ for trees. A structure whose space adapts to the content of the object, and not only to the class, is a [compressed data structure](/compressed-data-structure/).

**Why $o(Z)$ is enough for fast queries.** On the word RAM with $w = \Theta(\lg n)$, the standard plan has three parts:

1. Store the object as a short bit string, such as a bit vector or a sequence of [balanced parentheses](/balanced-parentheses-representation/).
2. Cut the string into *superblocks* of $\Theta(\lg^2 n)$ bits and *blocks* of $\Theta(\lg n)$ bits. Store an answer of $O(\lg n)$ bits for each superblock and an answer of $O(\lg \lg n)$ bits relative to its superblock for each block. This takes $O(n / \lg n)$ and $O(n \lg \lg n / \lg n)$ bits, both $o(n)$.
3. Answer a query inside a block of $\frac12 \lg n$ bits from a table that lists the answer for each possible block. There are only $2^{\frac12 \lg n} = \sqrt{n}$ blocks, so the table has $O(\sqrt{n} \lg n \lg \lg n)$ bits, also $o(n)$. This is the [method of Four Russians](/four-russians-method/) at the level of bits.

This plan gives [Jacobson's rank structure](/jacobson-rank/), the [rank/select dictionary](/rank-select-dictionary/) and the [range min-max tree](/range-min-max-tree/). Then a tree, a set or a sequence is stored as one or more bit strings, and each query becomes $O(1)$ rank, select or parenthesis queries.

**The limits.** The redundancy cannot go to zero for free. For rank on a bit vector, Pătraşcu showed $n + n / (\lg n / t)^t + \tilde{O}(n^{3/4})$ bits with $O(t)$ time, and Pătraşcu and Viola proved that $n + n / w^{O(t)}$ bits are necessary in the [cell-probe model](/cell-probe-model/). See [Pătraşcu's lower bounds](/patrascu-succinct-lower-bound/).

## Examples

**Bit vectors with $m$ ones.** The class has $\binom{n}{m}$ members, so $Z = \lceil \lg \binom{n}{m} \rceil$. For $n = 2^{20}$ and $m = 2^{16}$, $\lg \binom{n}{m} \approx 353{,}665$ bits, about a third of the $n = 1{,}048{,}576$ bits of the plain vector. The [RRR bit vector](/rrr-bitvector/) uses $\lg \binom{n}{m} + o(n)$ bits with $O(1)$ rank and select. The plain [bit vector](/bit-vector/) with an index of $o(n)$ bits is succinct for the class of all $2^n$ vectors, but not for the class with $m$ fixed when $m$ is far from $n/2$.

**Ordered trees.** The number of ordered trees with $n$ nodes is the [Catalan number](/catalan-numbers/) $C_{n-1} = \frac{1}{n}\binom{2n-2}{n-1}$: 1, 1, 2, 5, 14, 42 for $n = 1$ to 6. So $Z = 2n - \Theta(\lg n)$. For $n = 10^6 + 1$ nodes, $\lg C_{10^6} \approx 1{,}999{,}969.3$ bits. A node with a first-child pointer and a next-sibling pointer of 64 bits each uses $128 \cdot (10^6 + 1)$ bits, about 64 times more. [LOUDS](/louds-tree/), [BP](/balanced-parentheses-representation/) and [DFUDS](/dfuds/) use $2n + o(n)$ bits with navigation in $O(1)$ time.

**Sets of integers.** A set of $m$ integers from $\{0, \ldots, u-1\}$ is one of $\binom{u}{m}$ sets. For $u = 2^{32}$ and $m = 10^6$, $\lg \binom{u}{m} \approx 13{,}510{,}947$ bits, about 13.5 bits for each element, while a sorted array of 32-bit integers uses 32 bits for each. [Elias-Fano](/elias-fano-encoding/) with $\lfloor \lg(u/m) \rfloor = 12$ low bits for each element stores this set in $12m + m + 2^{20} = 14{,}048{,}576$ bits, about 14.05 bits for each element, and finds the $j$-th element in $O(1)$ time.

**Permutations.** There are $n!$ permutations of $n$ items, and $\lg n! = n \lg n - n \lg e + O(\lg n)$ by [Stirling's approximation](/stirling-approximation/). The plain array is close to this, but it gives only $\pi(i)$. The [succinct permutation](/succinct-permutation/) adds $\varepsilon n \lg n$ bits to also give $\pi^{-1}(i)$ in $O(1/\varepsilon)$ time.

**A non-example.** A [suffix array](/suffix-array/) of a text of length $n$ over $\sigma$ symbols stores $n$ integers of $\lceil \lg n \rceil$ bits. The class of texts has $\sigma^n$ members, so $Z = \lceil n \lg \sigma \rceil$, and for a fixed alphabet the suffix array uses a factor $\Theta(\lg n)$ more. It is not compact. The [FM-index](/fm-index/) answers the same pattern queries in about $n \lg \sigma + o(n \lg \sigma)$ bits.

## Where it is used

- Bit vectors with [rank and select](/rank-select-problem/) are the base layer: [rank/select dictionary](/rank-select-dictionary/), [RRR](/rrr-bitvector/), [SD-array](/sd-array/), [dynamic bit vector](/dynamic-bit-vector/).
- Trees: the [ordinal tree](/ordinal-tree/) type, with [LOUDS](/louds-tree/), [BP](/balanced-parentheses-representation/), [DFUDS](/dfuds/) and the [range min-max tree](/range-min-max-tree/), and the [LOUDS trie](/louds-trie/) for string dictionaries.
- Sequences: the [wavelet tree](/wavelet-tree/) and the [wavelet matrix](/wavelet-matrix/) for [static sequences](/static-sequence/) over larger alphabets.
- Text indexes: the [FM-index](/fm-index/), the [compressed suffix array](/compressed-suffix-array/) and [compressed indexing](/compressed-indexing/) in general.
- Graphs: [succinct graph representations](/succinct-graph-representation/) of large web and social graphs.
- Range queries: a range minimum query structure in $2n + o(n)$ bits stores a [Cartesian tree](/cartesian-tree/) shape in place of the array.

## References
