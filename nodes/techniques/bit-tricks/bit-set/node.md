---
tag: C0Q5CB
kind: data-structure
slug: bit-set
name: Bit vector
aliases:
- bit array
- bitmap
- bitset
area: techniques/bit-tricks
level: intro
summary: A fixed-size array of bits giving constant-time membership, insertion and deletion over a small universe.
prereqs: [bitmask, bitwise-operations, dictionary-problem]
see_also: [bit-vector, population-count, trailing-zero-count, roaring-bitmap, rank-select-dictionary, bloom-filter, sieve-of-eratosthenes, bitset-adjacency-matrix]
sources:
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition, Addison-Wesley (2000)
    locator: Column 1 (Cracking the Oyster), the bitmap sort of telephone numbers
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.1 (Direct-address tables)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley (2011)
    locator: Section 7.1.3 (Bitwise tricks and techniques), the part on bitwise operations as operations on sets
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer (2011)
    locator: Chapter 1 (Bit wizardry), the section Words as bitsets
  - url: https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf
    title: ISO/IEC 9899:2011 committee draft N1570 (the C11 standard)
    locator: Section 6.5.7 (Bitwise shift operators), paragraph 3
---

A bit vector stores a subset $S$ of a universe $\{0, 1, \dots, n - 1\}$ as an array of $n$ bits, one per possible element, packed into $\lceil n / w \rceil$ machine words of $w$ bits. Element $i$ lives in bit $i \bmod w$ of word $\lfloor i / w \rfloor$. Insertion, deletion and membership each touch one word and take $\Theta(1)$ time on the [word RAM](/word-ram/); union, intersection, complement and counting work on whole words and take $\Theta(n / w)$ time, which is $w$ times faster than one bit at a time. The space is $n$ bits whatever the size of $S$, so the structure pays off when the universe is small or the set is dense. It is the multi-word form of the [bitmask](/bitmask/) and a [direct-address table](/direct-address-table/) whose entries are single bits.

## In plain words

Suppose you must remember which of the numbers from 0 to 999 999 you have seen. You can keep a row of a million switches, one for each number, all off at the start. To record a number, turn its switch on. To ask about a number, look at its switch. No search is needed, because the number itself tells you where its switch is.

A computer packs 64 such switches into one word. So the million switches take about 15 600 words, and many questions about whole sets, such as "which numbers are in both sets", are answered 64 switches at a time.

## The abstract type

A bit vector implements the [dictionary problem](/dictionary-problem/) for keys from a fixed universe $\{0, \dots, n - 1\}$ without associated values, that is, a dynamic set with these operations:

- `new(n)`: the empty set over the universe $\{0, \dots, n - 1\}$;
- `insert(S, i)`, `delete(S, i)`, `contains(S, i)` for $0 \le i < n$;
- `count(S)`: the number of members $\lvert S \rvert$;
- `next(S, i)`: the least member $\ge i$, or NIL; this gives ordered iteration;
- `complement(S)`, `union(S, T)`, `intersection(S, T)`, `difference(S, T)` for two sets over the same universe.

## Representation

Fix the word size $w$; often $w$ is a power of two, so that $\lfloor i / w \rfloor$ is $i \gg \lg w$ and $i \bmod w$ is $i \wedge (w - 1)$. Let $m = \lceil n / w \rceil$. The fields are the universe size $n$ and an array $B[0..m-1]$ of unsigned $w$-bit words.

**Invariant.** (I1) For every $i$ with $0 \le i < n$: $i \in S$ exactly when bit $i \bmod w$ of $B[\lfloor i / w \rfloor]$ is 1. (I2) Every bit of $B[m - 1]$ at a position $t$ with $(m - 1) w + t \ge n$ is 0; these are the padding bits of the last word.

Part (I2) is what lets `count`, `next` and comparisons of whole words ignore the boundary.

## Operations

The main operations each touch one word.

```pseudo id=main
NEW(n)
L1  B ← array of ⌈n / w⌉ words, all 0
INSERT(B, i)                              ▷ 0 ≤ i < n
L2  B[⌊i / w⌋] ← B[⌊i / w⌋] ∨ (1 ≪ (i mod w))
DELETE(B, i)                              ▷ 0 ≤ i < n
L3  B[⌊i / w⌋] ← B[⌊i / w⌋] ∧ ¬(1 ≪ (i mod w))
CONTAINS(B, i)                            ▷ 0 ≤ i < n
L4  return ((B[⌊i / w⌋] ≫ (i mod w)) ∧ 1) = 1
```

Line L1 allocates the words and clears them, which costs $\Theta(n / w)$. Lines L2 to L4 compute the word index and the bit position, build the one-bit mask $1 \ll (i \bmod w)$, and set, clear or test that bit with OR, AND with the complement, or a shift and AND. Each costs $\Theta(1)$.

Counting adds the [population counts](/population-count/) of the words.

```pseudo id=count
COUNT(B)
C1  c ← 0
C2  for j ← 0 to m − 1
C3      c ← c + POPCOUNT(B[j])
C4  return c
```

With a constant-time popcount, the cost is $\Theta(m) = \Theta(n / w)$. Without (I2), padding bits would be counted too.

Finding the next member skips empty words and then uses a [trailing-zero count](/trailing-zero-count/).

```pseudo id=next
NEXT(B, i)                                ▷ least member ≥ i, or NIL
N1  j ← ⌊i / w⌋
N2  if j ≥ m then return NIL
N3  x ← B[j] ∧ ¬((1 ≪ (i mod w)) − 1)      ▷ drop the bits below i
N4  while x = 0
N5      j ← j + 1
N6      if j = m then return NIL
N7      x ← B[j]
N8  return j · w + CTZ(x)
```

Line N3 keeps the bits of word $j$ at positions $\ge i \bmod w$. The loop of lines N4 to N7 runs at most $m - 1$ times, so the cost is $O(n / w)$ in the worst case and $O(1 + g / w)$ when the next member is $g$ positions away. Iterating over all members by repeated calls, or by clearing the [lowest set bit](/lowest-set-bit/) of each word, costs $O(n / w + \lvert S \rvert)$.

The set operations work word by word; complement must restore (I2).

```pseudo id=complement
COMPLEMENT(B)
K1  for j ← 0 to m − 1
K2      B[j] ← ¬B[j]
K3  if n mod w ≠ 0 then B[m − 1] ← B[m − 1] ∧ ((1 ≪ (n mod w)) − 1)
UNION(A, B)                               ▷ both over the same n
K4  for j ← 0 to m − 1
K5      A[j] ← A[j] ∨ B[j]
```

Intersection and difference are the same loop with $A[j] \wedge B[j]$ and $A[j] \wedge \neg B[j]$; they cannot set a padding bit, and neither can union. Each of these costs $\Theta(n / w)$.

## Example

Take $n = 10$ and, to keep the words short, $w = 4$, so $m = 3$ words. Element $i$ is bit $i \bmod 4$ of word $\lfloor i / 4 \rfloor$, and word 2 has two padding bits. Words are written with bit 3 on the left.

| operation | $B[0]$ | $B[1]$ | $B[2]$ | result | set |
|---|---|---|---|---|---|
| new(10) | 0000 | 0000 | 0000 | | $\emptyset$ |
| insert 1 | 0010 | 0000 | 0000 | | $\{1\}$ |
| insert 6 | 0010 | 0100 | 0000 | | $\{1, 6\}$ |
| insert 9 | 0010 | 0100 | 0010 | | $\{1, 6, 9\}$ |
| contains 6 | | | | true | |
| delete 1 | 0000 | 0100 | 0010 | | $\{6, 9\}$ |
| contains 1 | | | | false | |
| insert 4 | 0000 | 0101 | 0010 | | $\{4, 6, 9\}$ |
| count | | | | 3 | |
| next(5) | | | | 6 | |
| next(7) | | | | 9 | |
| complement | 1111 | 1010 | 0001 | | $\{0, 1, 2, 3, 5, 7, 8\}$ |

For next(7), line N3 masks word 1 to $0101 \wedge 1000 = 0000$, the loop moves to word 2, $x = 0010$, and line N8 returns $2 \cdot 4 + 1 = 9$. For complement, line K2 turns $B[2] = 0010$ into $1101$, and line K3 clears the padding bits 2 and 3, which leaves $0001$, the set $\{8\}$ within word 2. Without line K3, the count after the complement would be 9 instead of 7.

## Correctness

Each operation keeps (I1) and (I2) and returns the value the abstract type asks for. NEW makes every bit 0, so (I1) holds for $S = \emptyset$ and (I2) holds. INSERT and DELETE change exactly the bit of $i$, which lies in the universe, so (I1) holds for $S \cup \{i\}$ or $S \setminus \{i\}$ and the padding bits are not touched. CONTAINS reads the bit that (I1) ties to $i$. COUNT returns the number of 1-bits, which by (I1) and (I2) is $\lvert S \rvert$. NEXT returns the position of the lowest 1-bit at or after position $i$, which by (I1) and (I2) is the least member $\ge i$. COMPLEMENT inverts every bit and then clears the padding again. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | notes |
|---|---|---|
| new | $\Theta(n / w)$ | clearing the array |
| insert, delete, contains | $\Theta(1)$ | one word, one mask |
| count | $\Theta(n / w)$ | one popcount per word; $O(1)$ if a counter is kept up to date by insert and delete |
| next | $O(n / w)$ worst case | $O(1 + g / w)$ for a gap of $g$ |
| iterate all members | $O(n / w + \lvert S \rvert)$ | |
| union, intersection, difference, complement | $\Theta(n / w)$ | one operation per word |
| space | $\lceil n / w \rceil$ words | $n$ bits plus at most $w - 1$ padding bits |

These bounds hold on the word RAM with $w \ge \lg n$ and constant-time popcount and trailing-zero count. Without these instructions, count and next cost $O(\lg w)$ per word by the [SWAR popcount](/swar-popcount/) and a binary search on the bits.

## Variants

- **Fixed size in a language library.** C++ has `std::bitset<N>` with the size fixed at compile time; Java has `java.util.BitSet`, which grows as needed and has `nextSetBit`. Python has no built-in bit vector, but one `int` used as a [bitmask](/bitmask/) does the same job.
- **Counted bit vector.** Keep $\lvert S \rvert$ in a field and update it in INSERT and DELETE, after a CONTAINS test, so that count is $O(1)$.
- **Rank and select.** A [rank-select dictionary](/rank-select-dictionary/) adds small tables of prefix counts, which answer "how many members are below $i$" and "which is the $k$-th member" in $O(1)$ time with $o(n)$ extra bits; this is the base of [succinct data structures](/succinct-data-structures/).
- **Compressed bitmaps.** For large sparse universes, a [Roaring bitmap](/roaring-bitmap/) splits the universe into chunks of $2^{16}$ and stores each chunk as a sorted array, a bit vector or runs, depending on its density.
- **Hierarchical bit vectors.** A second-level bit vector with one bit per nonempty word lets NEXT skip $w$ empty words at a time; repeating the idea gives $O(\log_w n)$ for NEXT.
- **Probabilistic sets.** A [Bloom filter](/bloom-filter/) uses a bit vector indexed by several hash values to store a set from a huge universe in few bits, at the cost of false positives.
- **Bit-packed tables.** A [bitmap index](/bitmap-index/) keeps one bit vector per value of a database column, and an [adjacency matrix with bitset rows](/bitset-adjacency-matrix/) keeps one per vertex.

## When to use it

Use a bit vector when the keys are integers in a known range $[0, n)$ and $n$ is not much larger than the number of keys times $w$; then it uses less memory than a [hash table](/hash-table/) or a sorted array and has no hashing and no collisions. Use it when the program combines whole sets, because one word operation handles $w$ elements; the [sieve of Eratosthenes](/sieve-of-eratosthenes/), set operations in graph searches, and the bitmap sort of Bentley's Column 1 are examples. Avoid it when the universe is huge and the set is sparse: the space and the cost of new, count and the set operations grow with $n$, not with $\lvert S \rvert$. Then use a hash set, a sorted array or a compressed bitmap.

## Pitfalls

- **Wrong mask type.** In C, writing line L2 as `B[i / 64] |= 1 << (i % 64)` builds the mask as an `int`; for $i \bmod 64 \ge 31$ the shift overflows or is by at least the width, which is undefined behaviour (C11 Section 6.5.7, paragraph 3). Use `1ull << (i % 64)` with `uint64_t` words.
- **Padding bits after complement.** Inverting the words without line K3 sets the padding bits, and later COUNT and NEXT report members $\ge n$. Mask the last word after every operation that can set padding bits.
- **Rounding the array size down.** Allocating $\lfloor n / w \rfloor$ words in line L1 instead of $\lceil n / w \rceil$ loses the last $n \bmod w$ elements and writes past the end of the array. Use $\lfloor (n + w - 1) / w \rfloor$.
- **Missing range check.** Lines L2 to L4 assume $0 \le i < n$. An index $i \ge n$ in the last word silently sets a padding bit, and a larger one writes outside the array; check the range or document the precondition.
- **Shift of the wrong width in NEXT.** Line N3 computes $1 \ll (i \bmod w)$, which is always less than $w$; computing $1 \ll i$ instead shifts by more than the width for $i \ge w$.
- **`std::vector<bool>` is not a container of `bool`.** The C++ specialization packs bits and returns proxy objects, so `bool* p = &v[0]` does not compile and concurrent writes to different elements of the same word are a data race.

## Implementations

## History

Bit vectors are as old as binary computers: a word was used as a set of flags from the start. Bentley's Programming Pearls, Column 1, made the bitmap a textbook example with the problem of sorting up to ten million distinct seven-digit telephone numbers in about a megabyte of memory, by setting one bit per possible number and reading the bits in order. CLRS treats the direct-address table, of which a bit vector is the case with one-bit entries, in Section 11.1, and Knuth's Section 7.1.3 treats words as sets with the bitwise operations as set operations.

## References
