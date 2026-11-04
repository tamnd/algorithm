---
tag: F8X8XG
kind: problem
slug: next-same-popcount
name: Next number with same popcount
aliases:
- next higher number with same number of set bits
- next bitmask combination
area: techniques/bit-tricks
level: core
summary: Finding the next larger integer that has the same number of 1-bits as x.
model: word-ram
complexity:
  vars: {w: the word size in bits}
  time: {worst: O(1)}
prereqs: [population-count, bitmask, lowest-set-bit]
see_also: [gospers-hack, colexicographic-order, k-subset-enumeration, combinatorial-ranking-and-unranking, submask-enumeration]
sources:
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition
    locator: Section 2-1, Manipulating Rightmost Bits, subsection A Novel Application
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.3, Generating all combinations (colexicographic order and the combinatorial number system)
  - url: "https://dspace.mit.edu/handle/1721.1/6086"
    title: Michael Beeler, R. William Gosper and Richard Schroeppel, HAKMEM, MIT Artificial Intelligence Laboratory, AI Memo 239, February 1972
    locator: Item 175
---

The next-same-popcount problem asks, for a positive integer $x$, for the least integer $y > x$ that has the same number of 1-bits as $x$, that is, the same [population count](/population-count/). When $x$ is a [bitmask](/bitmask/) of a $k$-element set, $y$ is the next $k$-element set in [colexicographic order](/colexicographic-order/), so repeated answers list all subsets of a given size. On the [word RAM](/word-ram/) with division or a trailing-zero count, [Gosper's hack](/gospers-hack/) solves it in $O(1)$ time with no loop.

## In plain words

You have a number written in binary, for example a number with three 1-bits. You want the next larger number that also has exactly three 1-bits. Counting upward one number at a time and checking each one works, but it can take a long time.

The answer has a simple shape. Find the lowest group of 1-bits that stand side by side. Move the top bit of the group up by one place, and push the rest of the group down to the bottom. If the 1-bits stand for the items you picked from a list, this step gives the next way to pick the same number of items. So the problem is how to list all ways to choose a fixed number of items.

## Definition

**Input.** An integer $x$ with $0 < x < 2^w$, given as a $w$-bit word. Let $\operatorname{pop}(v)$ be the number of ones in the binary form of $v \ge 0$, and let $k = \operatorname{pop}(x)$.

**Output.** The integer
$$ \operatorname{next}(x) = \min \{\, y \in \mathbb{Z} : y > x,\ \operatorname{pop}(y) = k \,\}, $$
together with a flag that says whether $\operatorname{next}(x) < 2^w$. The minimum always exists: with $h = \lfloor \lg x \rfloor$, the integer $x + 2^h$ moves the top one of $x$ up one place, so it is larger than $x$ and has $k$ ones. The answer is a $w$-bit word if and only if $x$ is not the largest $w$-bit word with $k$ ones, which is $(2^k - 1) \cdot 2^{w-k}$.

**Closed form.** Write $x = a \cdot 2^{t+m+1} + (2^m - 1) \cdot 2^t$, where $t$ is the number of trailing zeros of $x$ and $m \ge 1$ is the length of its lowest block of ones. Then
$$ \operatorname{next}(x) = a \cdot 2^{t+m+1} + 2^{t+m} + 2^{m-1} - 1 . $$
The proof is on the page of [Gosper's hack](/gospers-hack/).

## Variants

- **Previous number.** Find the greatest $y < x$ with $\operatorname{pop}(y) = k$. In $w$ bits, complementing maps the words with $k$ ones to the words with $w - k$ ones and reverses the order, so $\operatorname{prev}(x) = \lnot \operatorname{next}(\lnot x)$ when $\lnot x$ is not the last word with $w - k$ ones.
- **Enumeration.** List all $\binom{n}{k}$ masks of the $k$-subsets of $\{0, \ldots, n - 1\}$ in increasing order. Start at $2^k - 1$ and apply $\operatorname{next}$ until the value reaches $2^n$. This is [k-subset enumeration](/k-subset-enumeration/) in colexicographic order.
- **Ranking and unranking.** The position of a set $\{c_1 < c_2 < \cdots < c_k\}$ in this list, counted from 0, is $\sum_{i=1}^{k} \binom{c_i}{i}$, the combinatorial number system. So the $r$-th mask can be found directly, without $r$ steps of $\operatorname{next}$. See [combinatorial ranking and unranking](/combinatorial-ranking-and-unranking/).
- **Several words.** For $n > w$ the mask spans several words. The same closed form applies, but the carry and the shift of the low block cross word borders.

## Examples

| $x$ | binary | $\operatorname{next}(x)$ | binary |
| --- | --- | --- | --- |
| 1 | 1 | 2 | 10 |
| 3 | 11 | 5 | 101 |
| 6 | 110 | 9 | 1001 |
| 7 | 111 | 11 | 1011 |
| 12 | 1100 | 17 | 10001 |
| 14 | 1110 | 19 | 10011 |
| 22 | 10110 | 25 | 11001 |
| 92 | 1011100 | 99 | 1100011 |

For $x = 92$ the lowest block is 111 at bits 2 to 4, so $t = 2$, $m = 3$ and $a = 1$, and the closed form gives $1 \cdot 2^6 + 2^5 + 2^2 - 1 = 64 + 32 + 3 = 99$. In colexicographic order the set $\{2, 3, 4, 6\}$ of 92 has rank $\binom{2}{1} + \binom{3}{2} + \binom{4}{3} + \binom{6}{4} = 2 + 3 + 4 + 15 = 24$, and the set $\{0, 1, 5, 6\}$ of 99 has rank 25.

A non-example: in 8 bits, $x = 11100000_2 = 224$ has no answer, because 224 is the largest 8-bit word with three ones. The true answer $352 = 101100000_2$ needs 9 bits.

## Known algorithms

- [Gosper's hack](/gospers-hack/): $O(1)$ word operations, one of them a division by a power of two; or a trailing-zero count instead of the division.
- Scan: test $x + 1, x + 2, \ldots$ with a [population count](/population-count/) each. By the closed form, the gap $\operatorname{next}(x) - x$ is $2^t + 2^{m-1} - 1$. Inside $w$ bits it reaches $2^{w-2}$, for example at $x = 2^{w-2}$, so the scan takes time exponential in $w$ in the worst case.
- Bit-by-bit: scan the bits from the bottom for the first 1 with a 0 above it, then rebuild the low part. This takes $O(w)$ time, or $O(\log w)$ with a [trailing zero count](/trailing-zero-count/) found by binary search.

## Bounds

- **Upper bound.** $O(1)$ time on the [word RAM](/word-ram/) with addition, Boolean operations, shifts and either a division or a trailing-zero count, by [Gosper's hack](/gospers-hack/). A trailing-zero count itself takes $O(1)$ time with one multiplication by the [de Bruijn bit scan](/de-bruijn-bit-scan/).
- **Without multiplication and division.** With only addition, subtraction, Boolean operations and shifts, the trailing-zero count takes $O(\log w)$ steps by binary search on the position, so the problem takes $O(\log w)$ time by this route.
- **Lower bound.** Each algorithm reads the input word, so $\Omega(1)$ time is needed, and the $O(1)$ bound is tight on the word RAM.
- **Enumeration.** Listing all $k$-subsets of an $n$-set takes $\Theta(\binom{n}{k})$ time for $n < w$, which is optimal, since the output has $\binom{n}{k}$ words.

## Reductions

- **To the lowest set bit.** The closed form needs $2^t$, the [lowest set bit](/lowest-set-bit/), and the shift by $t + 2$. Given $2^t = x \mathbin{\&} (-x)$ and a way to shift by $t$, the rest is a constant number of word operations.
- **From k-subset listing.** Listing the $k$-subsets of $\{0, \ldots, n-1\}$ in colexicographic order reduces to $\binom{n}{k} - 1$ calls of $\operatorname{next}$.
- **Rank and unrank.** The combinatorial number system gives the rank of a mask in $O(k)$ arithmetic operations on binomial coefficients, so the $r$-th answer can be found without the $r$ calls.

## Applications

- **Layered [bitmask DP](/bitmask-dp/).** Some dynamic programs over subsets fill the table by the size of the set, all sets of size $k$ before those of size $k + 1$. A loop of $\operatorname{next}$ visits exactly the sets of one size.
- **Brute force over choices.** Testing all ways to choose $k$ items from $n < w$, for example $k$ columns of a matrix or $k$ vertices of a small graph, with no array of indices.
- **Fixed-weight codes.** The words of a constant-weight binary code of length $n$ and weight $k$ are the $k$-subsets, listed in order.

## References
