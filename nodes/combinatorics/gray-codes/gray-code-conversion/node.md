---
tag: 2PRMNN
kind: problem
slug: gray-code-conversion
name: Gray code conversion
aliases:
- binary-Gray conversion
- Gray code ranking and unranking
area: combinatorics/gray-codes
level: intro
summary: Convert a binary number to its Gray code and back.
prereqs: [binary-reflected-gray-code, bitwise-operations]
see_also: [binary-to-gray-conversion, gray-to-binary-conversion, ranking-unranking, gray-code-generation, bit-parity, prefix-sums, k-ary-gray-code, gray-code]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1 (g(k) = k XOR floor(k/2), its inverse, and the reflected mixed-radix code with its conversion rules)
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer, 2011
    locator: Chapter 1, the section on the Gray code and parity
  - paper: doi:10.1137/S0036144595295272
    title: Carla Savage, A survey of combinatorial Gray codes, SIAM Review 39(4), 605 to 629, 1997
    locator: Section 2 (the binary reflected Gray code and its rank)
---

Gray code conversion is the pair of maps between a number $b$ and the string at position $b$ in the [binary reflected Gray code](/binary-reflected-gray-code/): the unrank map $b \mapsto g(b) = b \oplus \lfloor b/2 \rfloor$ and its inverse, the rank map. The forward map costs one shift and one exclusive or. The inverse is a prefix exclusive or, which costs $\Theta(n)$ bit operations on an $n$-bit code, or $\Theta(\log w)$ word operations on a $w$-bit word. Together they make the reflected code a listing with exact [ranking and unranking](/ranking-unranking/) in constant or near constant time.

## In plain words

A Gray code is a list of all bit patterns of a fixed length, in an order where neighbors differ in one bit. Conversion answers two questions about the standard such list. Which pattern is at a given position? At which position is a given pattern?

The first question has a one-line answer: compare the number with itself shifted one place, and mark where they differ. The second question undoes this. Read the pattern from the left and keep a running bit that flips at each 1. Both answers are exact, so a program can jump to any place in the list without listing the patterns before it.

## Definition

Let $n \ge 0$ be the number of bits and $\Gamma_n$ the reflected Gray code, the list of all $N = 2^n$ strings of $\{0,1\}^n$ defined by $\Gamma_0 = \varepsilon$ and $\Gamma_{n+1} = 0\Gamma_n,\ 1\Gamma_n^R$. A string $a_{n-1} \ldots a_0$ stands for the integer $\sum_j a_j 2^j$.

- **To Gray (unrank).** Input: an integer $b$ with $0 \le b < 2^n$. Output: the entry $\Gamma_n[b]$.
- **To binary (rank).** Input: a string $a \in \{0,1\}^n$. Output: the unique $b$ with $\Gamma_n[b] = a$.

The answers are $\Gamma_n[b] = b \oplus \lfloor b/2 \rfloor$, bit by bit $a_j = b_j \oplus b_{j+1}$, and $b_j = a_j \oplus a_{j+1} \oplus \cdots \oplus a_{n-1}$. The proofs are on the pages of the two algorithms.

## Variants

- **Successor.** Given $a = \Gamma_n[b]$, find $\Gamma_n[b+1]$ without computing $b$. If $a$ has an even number of ones, flip bit 0. Otherwise flip the bit to the left of the lowest 1. The input $a = 10 \ldots 0$, the last entry, has no successor.
- **Base $k$ and mixed radix.** For the reflected code over digits $0$ to $k - 1$, digit $j$ of the code is $b_j$ when the higher part $\lfloor b / k^{j+1} \rfloor$ is even, and $k - 1 - b_j$ when it is odd. See [k-ary Gray code](/k-ary-gray-code/).
- **Other Gray codes.** For a [balanced Gray code](/balanced-gray-code/) or a code found by search, no short formula is known in general. Conversion then needs a table of $2^n$ entries or the recursive construction of the code.
- **Combinations.** The rank of a $k$-subset in the [revolving door order](/revolving-door-ordering/), which is the reflected code restricted to strings with $k$ ones, is an alternating sum of binomial coefficients.

## Examples

For $n = 4$:

| $b$ | binary | $\Gamma_4[b]$ | | $b$ | binary | $\Gamma_4[b]$ |
|---|---|---|---|---|---|---|
| 0 | 0000 | 0000 | | 8 | 1000 | 1100 |
| 1 | 0001 | 0001 | | 9 | 1001 | 1101 |
| 2 | 0010 | 0011 | | 10 | 1010 | 1111 |
| 3 | 0011 | 0010 | | 11 | 1011 | 1110 |
| 4 | 0100 | 0110 | | 12 | 1100 | 1010 |
| 5 | 0101 | 0111 | | 13 | 1101 | 1011 |
| 6 | 0110 | 0101 | | 14 | 1110 | 1001 |
| 7 | 0111 | 0100 | | 15 | 1111 | 1000 |

So $g(13) = 1011$, and the rank of $1011$ is $13$: from the top, the running bits are $1$, $1 \oplus 0 = 1$, $1 \oplus 1 = 0$, $0 \oplus 1 = 1$, which read $1101$.

## Known algorithms

| task | algorithm | time |
|---|---|---|
| to Gray, one word | [binary to Gray conversion](/binary-to-gray-conversion/), $b \oplus (b \gg 1)$ | $O(1)$ |
| to Gray, $n$-bit array | the same rule bit by bit | $\Theta(n)$ |
| to binary, one word | [Gray to binary conversion](/gray-to-binary-conversion/), shifts by $1, 2, 4, \ldots$ | $\Theta(\log w)$ |
| to binary, any length | Gray to binary conversion, running exclusive or from the top bit | $\Theta(n)$ |
| successor | the parity rule above | $O(1)$ amortized with a stored parity |

All times are on the [word RAM](/word-ram/) with $w$-bit words, $n \le w$ for the one-word rows.

## Bounds

- **To Gray** is optimal: each output bit depends only on two input bits, so a word computes in $O(1)$ time and an $n$-bit array in $\Theta(n)$, the size of the output.
- **To binary** on an $n$-bit array needs $\Omega(n)$ time: the output bit $b_0$ is the [parity](/bit-parity/) of all $n$ input bits, and changing any one input bit changes it, so an algorithm that skips an input bit fails on some input. The running exclusive or meets this bound.
- **To binary on a word** takes $\lceil \lg w \rceil$ rounds with the doubling method. A machine with a population count instruction finds any single bit $b_j$, the parity of $\lfloor a/2^j \rfloor$, in $O(1)$ time.

## Reductions

- **Rank is a prefix scan.** The rank is the [prefix sum](/prefix-sums/) modulo 2 of the bits, taken from the top bit down. Any parallel prefix method gives a parallel rank, with depth $O(\log n)$.
- **Rank needs parity.** Parity reduces to rank: the parity of $a$ is the lowest bit of its rank.
- **Generation from unrank.** Calling to Gray for $b = 0, 1, \ldots, 2^n - 1$ lists $\Gamma_n$ in $\Theta(N)$ word operations, so [Gray code generation](/gray-code-generation/) reduces to unranking.

## Applications

- **Encoders.** A rotary encoder with a Gray coded disc reports a code; the controller converts it to a position with the rank map.
- **Embedding a ring in a hypercube.** In a network whose nodes are the $n$-bit strings and whose links join strings at Hamming distance 1, node $g(i)$ and node $g(i+1)$ are linked. So the map $i \mapsto g(i)$ places a ring of $2^n$ processes on the network with each ring link on one network link.
- **Random access to a listing.** Unranking lets several workers split the list $\Gamma_n$ into blocks and start each block at its own position, for example to search all subsets of a set in parallel.
- **Genetic algorithms.** Some programs encode numbers in Gray code, so that numbers next to each other differ in one bit and a one-bit mutation can move to a neighbor value.

## References
