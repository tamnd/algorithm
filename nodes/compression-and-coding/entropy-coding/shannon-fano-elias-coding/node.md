---
tag: C2GA8M
kind: algorithm
slug: shannon-fano-elias-coding
name: Shannon-Fano-Elias coding
aliases:
- SFE coding
area: compression-and-coding/entropy-coding
level: advanced
summary: Codes each symbol by the first ceil(log2 1/p) + 1 bits of the midpoint of its interval of cumulative probability. No sort is needed, L < H + 2, and it leads to arithmetic coding.
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the number of symbols, B: the total number of bits in the codewords}
  time: {worst: Θ(n + B), average: Θ(n + B)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, comparison: false}
history:
  year: 1959
  people: [Edgar N. Gilbert, Edward F. Moore, Peter Elias, Claude E. Shannon]
  note: The midpoint rule with one extra bit was published by Gilbert and Moore in 1959; the idea of coding whole sequences this way is credited to Elias, who did not publish it.
prereqs: [prefix-code, shannon-entropy]
see_also: [arithmetic-coding, shannon-fano-coding, gilbert-moore-code, huffman-coding, range-coding, source-coding-theorem, optimal-alphabetic-code]
sources:
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition
    locator: Section 5.9, Shannon-Fano-Elias coding
  - paper: doi:10.1002/j.1538-7305.1959.tb01583.x
    title: Edgar N. Gilbert and Edward F. Moore, Variable-length binary encodings, Bell System Technical Journal 38(4), 1959
    locator: pages 933 to 967 (the order-preserving code from the midpoints)
  - paper: doi:10.1002/j.1538-7305.1948.tb01338.x
    title: Claude E. Shannon, A mathematical theory of communication, Bell System Technical Journal 27(3), 1948
    locator: Part I, Section 9 (the code from the cumulative probabilities)
---

Shannon-Fano-Elias coding gives each symbol a codeword taken from the binary expansion of a point in its own share of the interval $[0, 1)$. The symbols, in any fixed order, divide $[0, 1)$ into consecutive intervals, one of width $p$ for a symbol of probability $p$. The codeword is the first $\lceil \log_2 (1/p) \rceil + 1$ bits of the midpoint of that interval. Unlike [Shannon's code](/shannon-fano-coding/), no sorting is needed: the extra bit keeps the codeword inside the symbol's interval, so the code is a [prefix code](/prefix-code/) for any order. The expected length is less than $H + 2$, one bit worse than a [Huffman code](/huffman-coding/). Applied to whole blocks of symbols, the same rule is the exact form of [arithmetic coding](/arithmetic-coding/).

## In plain words

Lay a ruler from zero to one and give each symbol a piece whose length is its chance of occurring. Common symbols get long pieces and rare symbols get short ones. Now name each symbol by a point in the middle of its piece, written as a binary fraction.

You do not need all the digits of that point. You need just enough of them that every number which starts with those digits still lies inside the piece. For a long piece, a few digits are enough. For a short piece, you need more. One digit more than the plain count for that chance always does the job, because the middle is at least half a piece away from both ends.

Since the pieces do not overlap, no name can be the start of another name.

## The algorithm

The input is $n$ symbols with probabilities $p_1, \ldots, p_n > 0$ that sum to 1, in any order that the encoder and decoder agree on. Here $n$ is the alphabet size, written $\sigma$ in the notation of this area. $F$ is the sum of the probabilities of the symbols before the current one.

```pseudo id=main
SFE(p[1 .. n])
L1  F ← 0
L2  for i ← 1 to n do
L3      M ← F + p[i] / 2                 ▷ the midpoint of the interval [F, F + p[i])
L4      l ← ⌈log2(1 / p[i])⌉ + 1
L5      codeword(i) ← the first l bits after the binary point of M
L6      F ← F + p[i]
```

Line L3 takes the middle of symbol $i$'s interval. Line L4 sets the length so that $2^{-l} \le p_i / 2$: dropping the bits after position $l$ moves the point down by less than $2^{-l}$, so the truncated point stays above $F$, and all numbers that start with the codeword stay below $F + p_i$. Line L5 writes out the bits. Line L6 moves to the next interval. To decode, read bits until they form a codeword; the table of codewords is prefix-free.

**Blocks.** For a block $x_1 \cdots x_k$ from a memoryless source, start with the interval $[0, 1)$ and, for each symbol, shrink it to the part that symbol owns: the new start is the old start plus the old width times $F(x_j)$, and the new width is the old width times $p(x_j)$. Then apply lines L3 to L5 to the final interval. The decoder takes the number $0.c$ given by the codeword and finds, step by step, which symbol's part of the current interval contains it. This is arithmetic coding with exact arithmetic.

## Example

Four symbols, in the order A, B, C, D, with probabilities 0.3, 0.1, 0.4, 0.2.

| symbol | $p$ | $F$ | midpoint | in binary | $l$ | codeword |
|---|---|---|---|---|---|---|
| A | 0.3 | 0 | 0.15 | 0.001001… | 3 | 001 |
| B | 0.1 | 0.3 | 0.35 | 0.010110… | 5 | 01011 |
| C | 0.4 | 0.4 | 0.6 | 0.100110… | 3 | 100 |
| D | 0.2 | 0.8 | 0.9 | 0.111001… | 4 | 1110 |

The codewords are prefix-free and in the order of the symbols. The mean length is $0.9 + 0.5 + 1.2 + 0.8 = 3.4$ bits. The entropy is $H \approx 1.846$, so $L = 3.4 < H + 2 \approx 3.846$. A Huffman code gives C, A, D, B the lengths 1, 2, 3, 3, a mean of 1.9 bits. The single-symbol code is wasteful; its use is with blocks. For the source with probabilities 0.7, 0.2, 0.1, the mean length per symbol of the block code falls below $H + 2/k$ for blocks of $k$ symbols, so it tends to $H \approx 1.157$ as $k$ grows.

## Correctness

Symbol $i$ owns the interval $I_i = [F_i, F_i + p_i)$, and these intervals are disjoint. The numbers whose binary expansion starts with the codeword $c_i$ form an interval $J_i$ of width $2^{-l_i}$, starting at the truncated midpoint. Since $2^{-l_i} \le p_i/2$, the interval $J_i$ lies inside $I_i$. If $c_i$ were a prefix of $c_j$, then $J_j$ would lie inside $J_i$, so $I_i$ and $I_j$ would meet, which is false. The same containment shows that the codewords keep the order of the symbols. Summing $\log_2 (1/p_i) + 1 \le l_i < \log_2 (1/p_i) + 2$ with weights $p_i$ gives $H + 1 \le L < H + 2$. The full proofs are in proofs/correctness.md.

## Complexity

- **Time.** One pass over the symbols with $O(1)$ arithmetic operations each, plus one step for each output bit: $\Theta(n + B)$, where $B = \sum_i l_i$. There is no sort, unlike Shannon's and Fano's methods.
- **Space.** $O(1)$ beyond the input and output; the running sum $F$ is the only state.
- **Precision.** The bits of $F$ and of the midpoint must be exact. With counts $w_i$ and total $T$, the computation can be done in integers: the first $l$ bits of $(2F + p)/2$ are $\lfloor 2^l (2 W + w_i) / (2T) \rfloor$, where $W$ is the sum of the counts before $i$.
- **Blocks.** Exact interval arithmetic on blocks of $k$ symbols needs numbers with about $k$ times as many bits as one probability. Arithmetic coding avoids this by keeping a fixed number of bits and sending the leading bits as soon as they are settled.

## Properties

- **Prefix-free for any order.** The proof does not depend on how the symbols are arranged.
- **Order-preserving.** The codewords increase in the order of the symbols, so the code is an alphabetic code. This is the [Gilbert-Moore code](/gilbert-moore-code/).
- **Length.** $H + 1 \le L < H + 2$. The extra bit is the price of not sorting; on single symbols it makes the code worse than Shannon's and Huffman's.
- **Not full.** The Kraft sum is at most $\frac12$, since each $2^{-l_i} \le p_i / 2$. So half of the code space is never used. A decoder can use this to detect some errors, but it is waste.
- **Local.** Each codeword depends only on the symbol's probability and on the sum before it, so the codeword of one symbol can be computed without building the others.
- **Rate on blocks.** On blocks of $k$ symbols the mean rate is less than $H + 2/k$ bits per symbol, which tends to the entropy.

## Variants and improvements

- **[Shannon's code](/shannon-fano-coding/).** Sort the symbols by non-increasing probability and use the first $\lceil \log_2 (1/p) \rceil$ bits of the start $F$ instead of the midpoint. This saves the extra bit but needs the sort.
- **[Gilbert-Moore code](/gilbert-moore-code/).** The same construction, studied as an alphabetic code; Gilbert and Moore also give a dynamic program for the [optimal alphabetic code](/optimal-alphabetic-code/).
- **[Arithmetic coding](/arithmetic-coding/).** The block form with finite precision: the interval is kept in fixed-width integers, settled leading bits are sent at once, and the end needs only about 2 bits in total, not 2 bits per symbol.
- **[Range coding](/range-coding/).** The same with bytes as output digits.
- **Adaptive models.** The probabilities used for each symbol of the block may change from step to step, as long as the decoder can compute them too; the interval argument still holds.

## When to use it

Use Shannon-Fano-Elias coding to explain why arithmetic coding works and to prove the $H + 2$ bound with a short argument. As a code for single symbols it is never the best choice: a Huffman code has mean length below $H + 1$, and this code at least $H + 1$. Its one practical merit on single symbols is that the codewords keep the symbol order without any search, which matters for alphabetic codes.

## Pitfalls

- **Floating point.** Rounding errors in $F$ can change a bit of the codeword and break the prefix property. Use integer counts or exact fractions.
- **Truncation, not rounding.** Rounding the midpoint up to $l$ bits can move the codeword out of the interval. The proof needs truncation.
- **Agreeing on the order.** The order is free, but the encoder and decoder must use the same one, and the same probabilities.
- **Not optimal.** Do not compare it with Huffman coding on single symbols and conclude that interval coding is weak; the gain comes only with blocks.
- **Blocks need an end.** A block code needs the decoder to know $k$, or an end-of-message symbol, because short blocks are also valid inputs.

## Implementations

## History

Shannon (1948) built a code from the cumulative probabilities of sorted symbols to prove the noiseless coding theorem. Gilbert and Moore (1959) used the midpoint of each interval and one more bit, which removes the need to sort and keeps the order of the symbols, and so gives an alphabetic code within 2 bits of the entropy. Peter Elias saw that the same interval idea can code a whole sequence at once by nesting intervals; he did not publish it, and it reached print through textbooks of the 1960s. This is the root of arithmetic coding, which Rissanen and Pasco made practical with finite precision in 1976. The name Shannon-Fano-Elias coding is used by Cover and Thomas.

## References
