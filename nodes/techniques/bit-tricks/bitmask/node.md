---
tag: B2G33W
kind: concept
slug: bitmask
name: Bitmask
aliases:
- bit mask
- bit set encoding
area: techniques/bit-tricks
level: intro
summary: An integer whose bits encode membership of elements in a small set.
prereqs: [bitwise-operations]
see_also: [bit-set, bitmask-dp, submask-enumeration, power-set-enumeration, gospers-hack, sum-over-subsets, bitboard, population-count]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley (2011)
    locator: Section 7.1.3 (Bitwise tricks and techniques), the part on bitwise operations as operations on sets
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley (2013)
    locator: Chapter 2 (Basics), Section 2-1 (Manipulating Rightmost Bits)
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer (2011)
    locator: Chapter 1 (Bit wizardry), Section 1.2 (Operations on individual bits) and the section Words as bitsets
  - book: isbn:9780131103627
    title: Brian W. Kernighan and Dennis M. Ritchie, The C Programming Language, second edition, Prentice Hall (1988)
    locator: Section 2.9 (Bitwise Operators)
  - url: https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf
    title: ISO/IEC 9899:2011 committee draft N1570 (the C11 standard)
    locator: Section 6.5.7 (Bitwise shift operators), paragraphs 3 and 4
---

A bitmask is an integer used as a set: for a universe $\{0, 1, \dots, n - 1\}$ with $n \le w$, the set $S$ is stored as the word $\sum_{i \in S} 2^i$, so that bit $i$ is 1 exactly when $i \in S$. [Bitwise operations](/bitwise-operations/) then act as set operations: AND is intersection, OR is union, XOR is symmetric difference and NOT is complement, each in one step on the [word RAM](/word-ram/). The numbers $0, 1, \dots, 2^n - 1$ are exactly the subsets of the universe, which makes bitmasks the natural index of [bitmask dynamic programming](/bitmask-dp/) over subsets. For universes larger than a word the same idea uses an array of words, the [bit set](/bit-set/).

## In plain words

Give each element of a small set a number from 0 to $n - 1$. To describe a group of elements, write a row of $n$ switches and turn on the switches of the elements in the group. Read as a binary number, this row of switches is an ordinary integer.

Now the questions about groups become fast operations on numbers. "Which elements are in both groups?" is one AND. "Put the two groups together" is one OR. "Is element 3 in the group?" looks at one bit. And counting through all numbers from 0 up to $2^n - 1$ visits every possible group once.

## The idea

Fix $n \le w$ and the universe $U = \{0, \dots, n - 1\}$. The encoding $\mathrm{mask}(S) = \sum_{i \in S} 2^i$ is a bijection between the subsets of $U$ and the integers in $[0, 2^n)$. Under it, set operations become word operations, with the full set $\mathrm{mask}(U) = 2^n - 1$:

| set operation | bitmask expression |
|---|---|
| $\emptyset$, $U$ | $0$, $2^n - 1$ |
| $\{i\}$ | $1 \ll i$ |
| $i \in S$ | $(S \gg i) \wedge 1 = 1$, or $S \wedge (1 \ll i) \ne 0$ |
| $S \cup \{i\}$, $S \setminus \{i\}$ | $S \vee (1 \ll i)$, $S \wedge \overline{(1 \ll i)}$ |
| $S \cap T$, $S \cup T$ | $S \wedge T$, $S \vee T$ |
| $S \setminus T$, $S \mathbin{\triangle} T$ | $S \wedge \overline{T}$, $S \oplus T$ |
| $U \setminus S$ | $S \oplus (2^n - 1)$ |
| $S \subseteq T$ | $S \wedge \overline{T} = 0$, or $S \wedge T = S$ |
| $\lvert S \rvert$ | [population count](/population-count/) of $S$ |
| $\min S$ | [trailing-zero count](/trailing-zero-count/), or $S \wedge (-S)$ as the set $\{\min S\}$ |
| $\max S$ | [floor of log2](/floor-log2/) of $S$ |
| $S \setminus \{\min S\}$ | $S \wedge (S - 1)$ |

The complement must be taken relative to $U$: plain $\overline{S}$ also sets the $w - n$ bits above the universe.

**Order.** If $S \subseteq T$ then $\mathrm{mask}(S) \le \mathrm{mask}(T)$, because $T$ has every 1-bit of $S$. So increasing integer order is a linear extension of inclusion: a loop over the masks from $0$ to $2^n - 1$ visits each set after all of its subsets. This is the property that a [bitmask DP](/bitmask-dp/) needs when the value of a set depends on the values of its proper subsets.

**Enumerations.**

- All subsets of $U$: the loop `for S in 0 .. 2^n - 1`; see [power-set enumeration](/power-set-enumeration/).
- All submasks of a mask $m$, in decreasing order: start with $s = m$, and step $s \gets (s - 1) \wedge m$ until after $s = 0$; see [submask enumeration](/submask-enumeration/). Over all $m$, the total number of pairs $s \subseteq m$ is $\sum_m 2^{\lvert m \rvert} = 3^n$.
- All $k$-subsets in increasing order: [Gosper's hack](/gospers-hack/) maps a mask to the next larger mask with the same [population count](/population-count/).
- All members of $S$: repeat $b \gets S \wedge (-S)$, use $b$, $S \gets S \oplus b$, until $S = 0$; see [lowest set bit](/lowest-set-bit/).

**Size limits.** A mask of $n$ elements needs $n$ bits, so one machine word holds up to 64 elements. Algorithms that loop over all masks take at least $2^n$ steps, which limits them to about $n \le 25$ in practice; a table indexed by masks needs $2^n$ entries. In Python, integers have no fixed width, so a mask can have any number of bits, but the operations then cost time linear in the number of words.

**C rules.** The expression `1 << i` has type `int`; for $i \ge 31$ on a 32-bit `int` it overflows or shifts by the width, which is undefined (C11 Section 6.5.7, paragraphs 3 and 4). Write `1u << i` for $i < 32$ and `1ull << i` for $i < 64$, and never shift by $i \ge$ the width of the type.

## Examples

**Encoding.** With $n = 8$, $A = \{1, 3, 4\}$ is $00011010_2 = 26$, and $B = \{3, 5\}$ is $00101000_2 = 40$.

| expression | binary | value | set |
|---|---|---|---|
| $A \wedge B$ | 00001000 | 8 | $\{3\}$ |
| $A \vee B$ | 00111010 | 58 | $\{1, 3, 4, 5\}$ |
| $A \oplus B$ | 00110010 | 50 | $\{1, 4, 5\}$ |
| $A \wedge \overline{B}$ | 00010010 | 18 | $\{1, 4\}$ |
| $A \wedge (-A)$ | 00000010 | 2 | $\{1\}$, the minimum |
| $\nu(A)$ | | 3 | $\lvert A \rvert$ |

**Submasks.** The submasks of $m = 1011_2 = 11$, in the order of $s \gets (s - 1) \wedge m$, are 11, 10, 9, 8, 3, 2, 1, 0, that is, all $2^3 = 8$ subsets of $\{0, 1, 3\}$. For $n = 4$, the sum of $2^{\lvert m \rvert}$ over the 16 masks is $81 = 3^4$.

**A subset DP.** In the [Held-Karp algorithm](/held-karp-algorithm/) for the [traveling salesman problem](/traveling-salesman-problem/), $D[S][j]$ is the length of the shortest path that starts at city 0, visits exactly the cities of the mask $S$, and ends at $j \in S$. The recurrence reads $D[S \wedge \overline{(1 \ll j)}][i]$, a smaller mask, so a loop over $S$ in increasing order computes the table in $O(2^n n^2)$ time.

**Flags.** A program that stores options as named bits, such as `READ = 1`, `WRITE = 2` and `EXEC = 4`, tests `flags & WRITE` and combines `READ | WRITE`. This is a bitmask over a universe of three elements.

## Where it is used

- [Bitmask DP](/bitmask-dp/) and the [Held-Karp algorithm](/held-karp-algorithm/): tables indexed by subsets.
- [Submask enumeration](/submask-enumeration/) and [sum over subsets](/sum-over-subsets/): loops over submasks and transforms over the subset lattice.
- [Power-set enumeration](/power-set-enumeration/) and [Gosper's hack](/gospers-hack/): listing all subsets or all $k$-subsets.
- [Bitboards](/bitboard/): a 64-square board as one 64-bit mask per piece type.
- [Bitset adjacency matrices](/bitset-adjacency-matrix/): the neighbourhood of a vertex as a mask, so that common neighbours are one AND; used in searches for a [maximum clique](/maximum-clique/).
- [Bit sets](/bit-set/): the same encoding over arrays of words for universes larger than $w$.

## References
