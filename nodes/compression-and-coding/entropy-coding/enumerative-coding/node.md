---
tag: HHYSRG
kind: algorithm
slug: enumerative-coding
name: Enumerative coding
aliases:
- combinatorial coding
- Cover enumerative coding
area: compression-and-coding/entropy-coding
level: advanced
summary: Codes a binary sequence as its weight k and its lexicographic rank among the C(n, k) sequences of that weight, which is within lg(n+1) + 2 bits of n h(k/n).
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the length of the sequence, k: the number of ones}
  time: {worst: O(n^2), average: O(n^2), best: Θ(n)}
  space: {extra: O(n)}
properties: {deterministic: true, online: false, recursive: false, comparison: false}
history:
  year: 1966
  people: [Thomas J. Lynch, Lee D. Davisson, Thomas M. Cover]
  note: Lynch coded binary blocks by weight and index in 1966, with comments by Davisson; Cover gave the general formula for any set of sequences in 1973.
prereqs: [combinatorial-ranking-and-unranking, binomial-coefficient]
see_also: [combinatorial-number-system, binomial-coefficient-bounds, lexicographic-combinations, rrr-bitvector, arithmetic-coding, adaptive-modeling, big-integer, golomb-coding]
sources:
  - paper: doi:10.1109/TIT.1973.1054929
    title: Thomas M. Cover, Enumerative source encoding, IEEE Transactions on Information Theory 19(1), 73-77, 1973
    locator: the rank formula as a sum of counts over prefixes, for any set of sequences
  - paper: doi:10.1109/PROC.1966.5167
    title: Thomas J. Lynch, Sequence time coding for data compression, Proceedings of the IEEE 54(10), 1490-1491, 1966
    locator: coding a binary block by its weight and its index among the blocks of that weight
  - paper: doi:10.1109/PROC.1966.5344
    title: "Lee D. Davisson, Comments on 'Sequence time coding for data compression', Proceedings of the IEEE 54(12), 2010, 1966"
    locator: the comments on the code of Lynch
  - paper: doi:10.1109/TIT.1972.1054832
    title: J. Pieter M. Schalkwijk, An algorithm for source coding, IEEE Transactions on Information Theory 18(3), 395-399, 1972
    locator: the computation of the index of a binary sequence through Pascal's triangle
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, 2nd edition, Wiley, 2006
    locator: the chapter on the method of types, with the bounds on the size of a type class
---

Enumerative coding codes a binary sequence of length $n$ by two numbers: its weight $k$, the number of ones, and its rank among all $\binom{n}{k}$ sequences of that weight in lexicographic order. The weight takes $\lceil \lg(n + 1) \rceil$ bits and the rank $\lceil \lg \binom{n}{k} \rceil$ bits. Since $\lg \binom{n}{k} \le n\,h(k/n)$, where $h$ is the [binary entropy function](/binary-entropy-function/), the code is at most $\lg(n + 1) + 2$ bits longer than the empirical [entropy](/shannon-entropy/) of the sequence, for every sequence and with no model of the source. The rank is a sum of binomial coefficients, given by Cover's formula, and it is an instance of [combinatorial ranking](/combinatorial-ranking-and-unranking/). The same idea codes any set of sequences that one can count.

## In plain words

Suppose a block of 16 bits has exactly two ones. There are only 120 such blocks, so once the reader knows "two ones", a number from 0 to 119 is enough to say which block it is. The code sends the count of ones, then that number.

To find the number, list all the blocks with two ones in dictionary order and count how many come before this one. There is a short way to do this count without making the list: at each 1 in the block, add the number of blocks that agree up to that place but have a 0 there. The decoder runs the same count backwards. The fewer ones the block has, the fewer such blocks there are, and the shorter the number gets.

## The problem

The input is a binary sequence $x_1 \ldots x_n$; $n$ is known to the decoder. The output is a bit string from which the decoder gets the sequence back. The goal is a length close to $n\,h(k/n)$, the length that an ideal code would give the sequence if it knew the fraction of ones in advance.

## The algorithm

The rank of $x$ is the number of sequences of the same weight that come before it in lexicographic order, with 0 before 1. Cover's formula gives it as

$$\operatorname{rank}(x) = \sum_{i : x_i = 1} \binom{n - i}{j_i},$$

where $j_i$ is the number of ones at positions $i$ to $n$. The term for position $i$ counts the sequences that agree with $x$ before position $i$ and have a 0 there.

```pseudo id=main
ENUM-RANK(x_1 … x_n)
L1  k ← the number of ones in x; j ← k; r ← 0
L2  for i ← 1 to n do
L3      if x_i = 1 then
L4          r ← r + C(n − i, j)
L5          j ← j − 1
L6  return (k, r)

ENUM-UNRANK(n, k, r)
L7  j ← k
L8  for i ← 1 to n do
L9      c ← C(n − i, j)
L10     if r ≥ c then x_i ← 1, r ← r − c, j ← j − 1
L11     else x_i ← 0
L12 return x

ENUM-ENCODE(x): (k, r) ← ENUM-RANK(x)
L13 write k in ⌈lg(n + 1)⌉ bits, then r in ⌈lg C(n, k)⌉ bits
ENUM-DECODE(code, n)
L14 read k from the first ⌈lg(n + 1)⌉ bits and r from the next ⌈lg C(n, k)⌉ bits; return ENUM-UNRANK(n, k, r)
```

Here $\binom{m}{j} = 0$ when $j > m$. In line L10, the sequences that start with the output so far list first those with a 0 next, $\binom{n-i}{j}$ of them, and then those with a 1, so the test picks the right branch.

## Example

Take $n = 16$ and $x = 0001000000100000$, with ones at positions 4 and 11, so $k = 2$.

- At position 4 there are $j = 2$ ones left, and the term is $\binom{12}{2} = 66$.
- At position 11 there is $j = 1$ one left, and the term is $\binom{5}{1} = 5$.

So $\operatorname{rank}(x) = 71$. The weight 2 takes $\lceil \lg 17 \rceil = 5$ bits, `00010`, and the rank takes $\lceil \lg 120 \rceil = 7$ bits, `1000111`. The code has 12 bits in place of 16, against $\lg 17 + \lg 120 = 11.0$ bits before rounding and $16\,h(1/8) = 8.7$ bits for an ideal code that knew the fraction of ones.

To decode, UNRANK starts with $r = 71$ and $j = 2$. At positions 1, 2 and 3, the counts $\binom{15}{2} = 105$, $\binom{14}{2} = 91$ and $\binom{13}{2} = 78$ exceed 71, so the bits are 0. At position 4, $\binom{12}{2} = 66 \le 71$, so the bit is 1, $r = 5$ and $j = 1$. The counts $\binom{11}{1}$ to $\binom{6}{1}$ exceed 5, then at position 11 $\binom{5}{1} = 5 \le 5$ gives a 1 and $r = 0$, and the rest are 0.

For $n = 4$ and $k = 2$ the six sequences `0011`, `0101`, `0110`, `1001`, `1010`, `1100` get the ranks 0 to 5, in this order.

## Correctness

A sequence $y$ of the same weight comes before $x$ exactly when, at the first place $i$ where they differ, $y$ has a 0 and $x$ a 1. For a fixed $i$, the number of such $y$ is the number of ways to place the $j_i$ ones that are left in the $n - i$ places after $i$, which is $\binom{n-i}{j_i}$. Summing over $i$ counts every smaller sequence once, so the rank is the position of $x$ in the sorted list, and the ranks are exactly $0$ to $\binom{n}{k} - 1$. UNRANK walks down the same choices: at each place, the sequences with a 0 next come first, and there are $\binom{n-i}{j}$ of them. The length bound follows from $\frac{1}{n+1} 2^{n h(k/n)} \le \binom{n}{k} \le 2^{n h(k/n)}$, which holds because $\binom{n}{k} p^k (1-p)^{n-k}$ with $p = k/n$ is the largest of the $n + 1$ terms of a binomial distribution that sum to 1. The full proof is in [the correctness proof](#proof-correctness).

## Complexity

Model: [word RAM](/word-ram/) with words of $w \ge \lg n$ bits.

- **Time.** RANK and UNRANK each make $n$ steps, and each step adds or compares numbers of up to $n$ bits, stored as [big integers](/big-integer/). With a table of Pascal's triangle, this is $O(n^2 / w)$ word operations, which the front matter states as $O(n^2)$. Without a table, the next binomial follows from the last one by one multiplication and one division by small numbers, at the same cost. For blocks of at most $w$ bits, as in succinct data structures, each step costs $O(1)$.
- **Space.** The rank has at most $n$ bits. A full table of $\binom{m}{j}$ for $m \le n$ and $j \le k$ needs $O(n k)$ numbers of up to $n$ bits.
- **Length.** At most $n\,h(k/n) + \lg(n + 1) + 2$ bits for every sequence. On a sequence of 4000 bits with 10% ones, the code is within $\lg 4001 + 2$ bits of $n\,h(k/n)$, as the tests check.

## Properties

- **Optimal for the type.** Every sequence with the same $n$ and $k$ gets a rank of the same length, $\lceil \lg \binom{n}{k} \rceil$ bits, which is the least possible for a fixed-length code of that set.
- **Universal for memoryless sources.** For any memoryless binary source, the expected length per bit tends to the entropy of the source, with an excess of $O(\lg n / n)$.
- **Same length as adaptive arithmetic coding.** The Laplace estimator of [adaptive modeling](/adaptive-modeling/) gives every sequence with $k$ ones the probability $1 / ((n + 1)\binom{n}{k})$, so an ideal [arithmetic coder](/arithmetic-coding/) with that model spends the same $\lg(n + 1) + \lg \binom{n}{k}$ bits.
- **Not online.** The encoder must know $k$, and so see the whole block, before it can write the rank.

## Variants and improvements

- **Larger alphabets.** A sequence over $m$ symbols is coded by its *type*, the count of each symbol, and its rank among the $\binom{n}{n_1, \ldots, n_m}$ sequences of that type, through the same formula with multinomial coefficients. The type costs at most $(m - 1) \lg(n + 1)$ bits.
- **Cover's general form.** For any set $S$ of sequences and a function $N(u)$ that counts the elements of $S$ that start with $u$, the rank of $x$ in $S$ is $\sum_i \sum_{c < x_i} N(x_1 \ldots x_{i-1} c)$. With the right counting function, this covers sequences with a fixed count of each pair of adjacent symbols and sequences with constraints on runs.
- **Blocks.** Coding fixed blocks of $b$ bits one at a time keeps the numbers small but adds the cost of the weight for each block. The [RRR bit vector](/rrr-bitvector/) stores a bit vector as such blocks, each as its class (the weight) and its offset (the rank), and supports rank and select queries on the result.
- **Arithmetic coding.** An arithmetic coder can be seen as an enumerative code with counts rounded to a fixed precision, which removes the need for large integers and works online.

## When to use it

Use enumerative coding when the data come in blocks of known length whose weight varies, and when the reader needs to decode a block without the blocks before it, as in succinct bit vectors and in some index structures. Use it also to code a combinatorial object, such as a subset or a permutation of a multiset, in the least number of bits. For long streams, adaptive arithmetic coding gives the same length with small numbers and online operation.

## Pitfalls

- **Large numbers.** The rank of an $n$-bit block can have $n$ bits. Fixed-width integers overflow for $n$ above about 64; use big integers or short blocks.
- **The order of the terms.** The term at position $i$ uses the number of ones from $i$ to the end, including the one at $i$, and $n - i$ places after it. Off-by-one errors here give a map that is not a bijection, which the test by enumeration finds at once.
- **The cost of the weight.** For short blocks, the $\lceil \lg(n + 1) \rceil$ bits of the weight can cost more than the rank saves. Code the weights with an entropy coder when they are skewed.

## Implementations

## History

Lynch described the code in 1966, as a way to code binary blocks by the number of ones and the index of the block among those with that number, and Davisson commented on it in the same year. Schalkwijk (1972) computed the index with Pascal's triangle. Cover's 1973 paper *Enumerative source encoding* gave the general formula for the index of a sequence in any set whose prefixes can be counted. Enumerative codes later became a standard part of succinct data structures, where short blocks are stored by class and offset.

## References
