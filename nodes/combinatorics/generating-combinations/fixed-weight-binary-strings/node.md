---
tag: HN5MBB
kind: problem
slug: fixed-weight-binary-strings
name: Enumerating fixed-weight binary strings
aliases:
- bit strings with k ones
- fixed Hamming weight enumeration
- (s,t)-combinations
- constant-weight binary strings
area: combinatorics/generating-combinations
level: intro
summary: List all n-bit strings with exactly k ones; equivalent to enumerating k-subsets.
complexity:
  vars: {n: the length of each string, k: the number of ones, N: the number of strings}
  time: {worst: Ω(N)}
prereqs: [k-subset-enumeration]
see_also: [k-subset-enumeration, next-same-popcount, gospers-hack, cool-lex-order, hamming-weight, multiset-permutations, colexicographic-order, chase-sequence]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.3, Generating all combinations ((s,t)-combinations in bit string form, Chase's sequence)
  - paper: doi:10.1016/j.disc.2007.11.048
    title: Frank Ruskey and Aaron Williams, The coolest way to generate combinations, Discrete Mathematics 309(17), 2009, 5305-5320
    locator: Sections 1 and 2 (cool-lex order on binary strings with s zeros and t ones)
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley, 2012
    locator: Section 2-1, Manipulating Rightmost Bits (next higher number with the same number of 1-bits)
---

The fixed-weight binary string problem asks for a list of all binary strings of length $n$ that have exactly $k$ ones, each exactly once. There are $C(n, k)$ such strings, and each one is the characteristic vector of a [k-subset](/k-subset-enumeration/) of $[n]$, so the two problems are the same. The bit string view is the natural one for machine words: when $n$ fits in a word, [Gosper's hack](/gospers-hack/) gives the next string in $O(1)$ word operations.

## In plain words

Take a row of $n$ light switches. You must turn on exactly $k$ of them. You want to see every possible pattern of on and off switches, once each.

Each pattern is a choice of $k$ switches, so this is the same task as choosing a team of $k$ players. The difference is the way you write it down. Here each choice is a row of zeros and ones, and a computer can store such a row in one number. Then the next pattern comes from a few fast operations on that number.

## Definition

Let $0 \le k \le n$. A binary string $b = b_1 b_2 \cdots b_n$ has *weight* $|b| = b_1 + \cdots + b_n$, the [Hamming weight](/hamming-weight/). Let $B(n, k) = \{b \in \{0, 1\}^n : |b| = k\}$. Knuth calls these strings $(s, t)$-combinations, with $s = n - k$ zeros and $t = k$ ones.

**Input.** The integers $n$ and $k$.

**Output.** A sequence of the $N = C(n, k)$ strings of $B(n, k)$, each exactly once.

**Bijection.** The string $b$ corresponds to the set $S = \{j : b_j = 1\}$. So each listing of $B(n, k)$ is a listing of the $k$-subsets of $[n]$, and the converse is also true.

**Word form.** When $n \le w$ for the word size $w$, the string is the integer $x = \sum_j b_j 2^{j-1}$, with $b_1$ as the lowest bit. Then the operations of the [word RAM](/word-ram/) act on the whole string at once.

## Variants

- **Increasing integers.** List the integers in $[0, 2^n)$ with $k$ one bits in increasing order. This is [colexicographic order](/colexicographic-order/) of the sets. Each step is the [next same popcount](/next-same-popcount/) problem.
- **Decreasing strings.** List the strings $b_1 \cdots b_n$ as words in decreasing order. This is lexicographic order of the sets, see [lexicographic combinations](/lexicographic-combinations/).
- **Two bit changes.** Neighbors differ in exactly two bits. This is the [revolving door](/revolving-door-ordering/) order and other [combination Gray codes](/combination-gray-code-generation/).
- **Adjacent or near changes.** Neighbors differ by moving one $1$ to a near position. [Chase's sequence](/chase-sequence/) is near-perfect: each step moves one $1$ by one or two positions, over $0$s.
- **Prefix shifts.** Each step moves one bit of a prefix to the front. This is [cool-lex order](/cool-lex-order/).
- **Multiset permutations.** A string in $B(n, k)$ is a permutation of the multiset $\{0^{n-k}, 1^k\}$. So generators for [multiset permutations](/multiset-permutations/) also solve this problem.

## Examples

**$n = 5$, $k = 2$, in four orders.** Each column has the $C(5, 2) = 10$ strings.

| step | increasing integers ($b_5 \cdots b_1$) | decreasing words ($b_1 \cdots b_5$) | revolving door ($b_5 \cdots b_1$) | cool-lex ($b_1 \cdots b_5$) |
| --- | --- | --- | --- | --- |
| 0 | $00011$ | $11000$ | $00011$ | $11000$ |
| 1 | $00101$ | $10100$ | $00110$ | $01100$ |
| 2 | $00110$ | $10010$ | $00101$ | $10100$ |
| 3 | $01001$ | $10001$ | $01100$ | $01010$ |
| 4 | $01010$ | $01100$ | $01010$ | $00110$ |
| 5 | $01100$ | $01010$ | $01001$ | $10010$ |
| 6 | $10001$ | $01001$ | $11000$ | $01001$ |
| 7 | $10010$ | $00110$ | $10100$ | $00101$ |
| 8 | $10100$ | $00101$ | $10010$ | $00011$ |
| 9 | $11000$ | $00011$ | $10001$ | $10001$ |

The first column is what Gosper's hack produces from $x = 3$. In the revolving door column each step changes exactly two bits. In the cool-lex column each step moves the last bit of a prefix to the front of that prefix.

**Gosper's step.** From $x = 01100_2 = 12$: the lowest one bit is $c = 4$, $r = x + c = 16 = 10000_2$, and the bits that changed are $r \oplus x = 11100_2$. Shift this right by $2$ and divide by $c$ to get $00001_2$. The result is $r \vee 1 = 10001_2 = 17$, the next integer with two one bits.

## Known algorithms

| algorithm | order | time for each string | page |
| --- | --- | --- | --- |
| Gosper's hack | increasing integers | $O(1)$ word operations | [Gosper's hack](/gospers-hack/) |
| lexicographic successor on positions | decreasing words | $O(1)$ amortized when $k \le n/2$ | [lexicographic combinations](/lexicographic-combinations/) |
| cool-lex | prefix shifts | $O(1)$ worst case | [cool-lex order](/cool-lex-order/) |
| revolving door with Payne's jump | revolving door | $O(1)$ worst case | [Ehrlich's loopless combination generation](/ehrlich-loopless-combinations/) |
| Chase's Algorithm C | Chase's sequence | $O(1)$ amortized | [Chase's sequence](/chase-sequence/) |
| filter a binary counter | increasing integers | $O(2^n / N)$ amortized, often poor | [power set enumeration](/power-set-enumeration/) |

## Bounds

- **Lower bound.** Each algorithm takes $\Omega(N)$ time, because there are $N$ outputs.
- **Bit changes.** Two different strings of the same weight differ in at least two bits. So a list changes at least $2(N - 1)$ bits in total. The revolving door order meets this bound.
- **Upper bound.** Cool-lex order and the loopless revolving door take $O(1)$ time in the worst case between visits, after $O(n)$ initialization. Gosper's hack takes $O(1)$ word operations for each string when $n \le w$, and it needs a division or a count of trailing zeros.

## Reductions

- **To and from k-subsets.** The map $b \mapsto \{j : b_j = 1\}$ is a bijection between $B(n, k)$ and the [k-subsets](/k-subset-enumeration/) of $[n]$. It maps lexicographic, colexicographic and Gray code orders to the orders of the same names on sets.
- **Complement.** Flipping all bits maps $B(n, k)$ to $B(n, n - k)$.
- **Reversal.** Reading a string right to left maps the colexicographic order of one family to the reverse lexicographic order of the other.
- **Lattice paths.** A string in $B(n, k)$ is a monotone lattice path with $k$ up steps and $n - k$ right steps. See [counting lattice paths](/counting-lattice-paths/).

## Applications

- **Bitmask loops by popcount.** A [bitmask DP](/bitmask-dp/) such as the [Held-Karp algorithm](/held-karp-algorithm/) processes subsets in layers of the same size. Gosper's hack lists each layer.
- **Constant-weight codes.** Codes in which each codeword has the same weight are subsets of $B(n, k)$. Their enumeration and indexing use the [combinatorial number system](/combinatorial-number-system/) and [enumerative coding](/enumerative-coding/).
- **Succinct data structures.** The [RRR bit vector](/rrr-bitvector/) stores each block of bits as its weight and its index in $B(n, k)$.

## References
