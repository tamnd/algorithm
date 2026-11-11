---
tag: 0R8C9C
kind: algorithm
slug: gilbert-moore-code
name: Gilbert-Moore code
aliases:
- Gilbert-Moore coding
- Gilbert-Moore alphabetic code
area: compression-and-coding/entropy-coding
level: advanced
summary: An alphabetic prefix code from 1959. Each symbol gets the first ceil(log2 1/p) + 1 bits of the midpoint of its cumulative interval, so the codewords keep the symbol order and L < H + 2.
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the number of symbols, B: the total number of bits in the codewords}
  time: {worst: Θ(n + B), average: Θ(n + B)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, comparison: false}
history:
  year: 1959
  people: [Edgar N. Gilbert, Edward F. Moore]
  note: Gilbert and Moore studied alphabetic codes in the Bell System Technical Journal in 1959, with this code, its bound H + 2 and an O(n^3) program for the optimal alphabetic code.
prereqs: [shannon-fano-elias-coding]
see_also: [optimal-alphabetic-code, hu-tucker-algorithm, garsia-wachs-algorithm, optimal-binary-search-tree, huffman-coding, arithmetic-coding, interval-dp]
sources:
  - paper: doi:10.1002/j.1538-7305.1959.tb01583.x
    title: Edgar N. Gilbert and Edward F. Moore, Variable-length binary encodings, Bell System Technical Journal 38(4), 1959
    locator: pages 933 to 967 (alphabetic codes, the code from the midpoints, and the dynamic program)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition
    locator: Section 5.9, Shannon-Fano-Elias coding (the same construction)
  - paper: doi:10.1007/bf00264289
    title: Donald E. Knuth, Optimum binary search trees, Acta Informatica 1(1), 1971
    locator: pages 14 to 25 (the O(n^2) form of the interval program)
---

The Gilbert-Moore code is an *alphabetic* [prefix code](/prefix-code/): when the symbols are listed in a fixed order, such as the alphabet, their codewords are in the same lexicographic order. Gilbert and Moore (1959) built it from cumulative probabilities. Symbol $i$, with probability $p_i$, owns the interval from $P_i = p_1 + \cdots + p_{i-1}$ to $P_i + p_i$, and its codeword is the first $\lceil \log_2 (1/p_i) \rceil + 1$ bits of the midpoint $P_i + p_i/2$. The mean length is less than $H + 2$, against $H + 1$ for a [Huffman code](/huffman-coding/), which ignores the order. The construction is the same as [Shannon-Fano-Elias coding](/shannon-fano-elias-coding/); this page treats it as an alphabetic code, which is how Gilbert and Moore used it. In the same paper they gave an $O(n^3)$ dynamic program for the [optimal alphabetic code](/optimal-alphabetic-code/).

## In plain words

Sometimes the codewords must sort the same way as the things they stand for, so that a list of codewords can be sorted, or searched, without first decoding it. A Huffman code does not do this: it puts the common symbols near the top of the tree wherever they are in the alphabet.

Gilbert and Moore's idea keeps the order for free. Lay out the symbols along a ruler from zero to one, in alphabetical order, each one taking a piece as long as its chance. Name each symbol by the middle of its piece, written in binary, and keep just enough digits to stay inside the piece. Pieces further to the right give larger numbers, so the names come out in alphabetical order, and no name can start another.

## The algorithm

The input is $n$ symbols in their fixed order with positive counts $w_1, \ldots, w_n$ and total $T$, so $p_i = w_i / T$. Here $n$ is the alphabet size, written $\sigma$ in the notation of this area. All steps use integers.

```pseudo id=main
GILBERT-MOORE(w[1 .. n])                   ▷ counts in the order of the symbols; T = w[1] + … + w[n]
L1  W ← 0                                   ▷ the sum of the counts before symbol i
L2  for i ← 1 to n do
L3      M ← (2W + w[i]) / (2T)              ▷ the midpoint of [W / T, (W + w[i]) / T)
L4      l ← ⌈log2(T / w[i])⌉ + 1
L5      codeword(i) ← ⌊2^l · M⌋ written with l bits
L6      W ← W + w[i]
```

Line L3 takes the middle of the symbol's interval, as a fraction of two integers. Line L4 chooses the length so that $2^{-l} \le p_i / 2$; it is one bit more than the length $\lceil \log_2 (1/p_i) \rceil$ of [Shannon's code](/shannon-fano-coding/). Line L5 truncates the midpoint to $l$ bits with one integer division. All numbers that start with these bits lie inside the symbol's interval, so codewords of different symbols never start one another, and they are ordered as the intervals are.

**The optimal alphabetic code.** The code above is not optimal. Gilbert and Moore also gave an exact method: $c(i, j)$, the least cost of an alphabetic tree for the symbols $i$ to $j$, is the sum of their counts plus the least $c(i, k) + c(k + 1, j)$ over the splits $i \le k < j$. This [interval program](/interval-dp/) takes $O(n^3)$ time; Knuth's speedup for [optimal binary search trees](/optimal-binary-search-tree/) brings it to $O(n^2)$, and the [Hu-Tucker](/hu-tucker-algorithm/) and [Garsia-Wachs](/garsia-wachs-algorithm/) algorithms to $O(n \log n)$.

## Example

Five symbols in the order A, B, C, D, E with counts 4, 1, 6, 2, 3, total 16.

| symbol | count | interval | midpoint | in binary | $l$ | Gilbert-Moore | optimal alphabetic | Huffman length |
|---|---|---|---|---|---|---|---|---|
| A | 4 | [0, 4/16) | 2/16 | 0.00100 | 3 | 001 | 00 | 2 |
| B | 1 | [4/16, 5/16) | 9/32 | 0.01001 | 5 | 01001 | 01 | 3 |
| C | 6 | [5/16, 11/16) | 16/32 | 0.10000 | 3 | 100 | 10 | 2 |
| D | 2 | [11/16, 13/16) | 24/32 | 0.11000 | 4 | 1100 | 110 | 3 |
| E | 3 | [13/16, 1) | 29/32 | 0.11101 | 4 | 1110 | 111 | 2 |

The Gilbert-Moore code costs $12 + 5 + 18 + 8 + 12 = 55$ bits for the 16 symbols, 3.44 bits per symbol. The dynamic program finds the best alphabetic code, with lengths 2, 2, 2, 3, 3 and cost 37. A Huffman code, free to ignore the order, costs 35, and $16 H \approx 33.7$. The words of both alphabetic codes increase from A to E.

## Correctness

Symbol $i$ owns $I_i = [P_i, P_i + p_i)$, and the intervals are disjoint and in the order of the symbols. The numbers that start with the codeword $c_i$ fill an interval $J_i$ of width $2^{-l_i} \le p_i/2$ that starts at the truncated midpoint, and this places $J_i$ inside $I_i$. If $c_i$ were a prefix of $c_j$, then $J_j$ would lie in $J_i$ and $I_i$ would meet $I_j$. For $i < j$, all of $J_i$ is left of all of $J_j$, so $c_i$ comes first in lexicographic order. Summing $l_i < \log_2 (1/p_i) + 2$ with weights $p_i$ gives $L < H + 2$. For the dynamic program, the root of an alphabetic tree splits the symbols into a left run and a right run, each subtree is again alphabetic, and each leaf is one level deeper in the whole tree. The full proofs are in proofs/correctness.md.

## Complexity

- **The code.** One pass with $O(1)$ integer operations per symbol plus the output bits: $\Theta(n + B)$ time, where $B$ is the total length of the codewords, and $O(1)$ extra space. There is no sort, which would break the order anyway.
- **The dynamic program.** $O(n^3)$ time and $O(n^2)$ space. Knuth's monotone split rule gives $O(n^2)$ time; see [optimal alphabetic code](/optimal-alphabetic-code/).

## Properties

- **Alphabetic.** The codewords increase with the symbol order, so comparing codewords as bit strings compares the symbols.
- **Bounds.** $H + 1 \le L < H + 2$. Since this code is alphabetic, the optimal alphabetic code also has $L < H + 2$, and no prefix code has $L < H$.
- **Not full.** The Kraft sum is at most $\frac12$, so the code is never optimal, even among alphabetic codes; the dynamic program can always improve it.
- **Exact in integers.** With integer counts, each codeword needs one integer division.
- **The price of order.** The best alphabetic code can be much worse than a Huffman code on the same weights: for counts 1, 10, 1 in that order, it costs 23 bits against 14, because the heavy middle symbol can not get a 1-bit word without one of its neighbours.

## Variants and improvements

- **[Shannon-Fano-Elias coding](/shannon-fano-elias-coding/).** The same construction, used to explain and prove [arithmetic coding](/arithmetic-coding/); the order is only a side effect there.
- **Optimal alphabetic codes.** Gilbert and Moore's $O(n^3)$ program, Knuth's $O(n^2)$ form, and the $O(n \log n)$ algorithms of [Hu and Tucker](/hu-tucker-algorithm/) and [Garsia and Wachs](/garsia-wachs-algorithm/).
- **[Optimal binary search trees](/optimal-binary-search-tree/).** The same interval program, with weights also on the inner nodes for successful searches. An alphabetic code has weights only on the leaves.
- **Better simple bounds.** Shorter codes that keep the order can be built by choosing each split point of the interval more carefully; later work tightened the $H + 2$ bound for optimal alphabetic codes.

## When to use it

Use the Gilbert-Moore code when the order of the codewords must match the order of the symbols and a quick, provable bound is enough: for example, keys in a sorted index that are compared in compressed form. When the best alphabetic code is needed, use the [Hu-Tucker](/hu-tucker-algorithm/) or [Garsia-Wachs](/garsia-wachs-algorithm/) algorithm. When the order does not matter, a Huffman code is shorter.

## Pitfalls

- **Sorting the symbols.** Sorting by probability, as in Shannon's code, destroys the alphabetic property, which is the point of the code.
- **Dropping the extra bit.** Without it, the truncated start of one interval can be a prefix of the next codeword when a large probability follows a small one.
- **Floating point.** Compute the midpoint bits with integers, as in line L5; rounding errors can break the prefix property.
- **Mixing up the two problems.** The interval program for alphabetic codes puts weight only on the leaves. The optimal binary search tree problem also has weights on the inner keys; the two share the recurrence shape but not the costs.

## Implementations

## History

Gilbert and Moore (1959), at Bell Labs, studied variable-length binary encodings, among them codes whose words keep the order of the symbols. They gave the midpoint code with its bound $H + 2$ and a dynamic program of $O(n^3)$ steps for the best such code. Knuth (1971) showed that the split points of such interval programs are monotone, which gives $O(n^2)$ time. Hu and Tucker (1971) found an $O(n \log n)$ algorithm, and Garsia and Wachs (1977) a simpler one. The same midpoint construction is known in information theory as Shannon-Fano-Elias coding.

## References
