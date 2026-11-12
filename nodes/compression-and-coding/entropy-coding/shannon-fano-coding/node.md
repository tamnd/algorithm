---
tag: M37AW1
kind: algorithm
slug: shannon-fano-coding
name: Shannon-Fano coding
aliases:
- Shannon-Fano
- Fano coding
area: compression-and-coding/entropy-coding
level: intro
summary: Two early prefix codes. Fano splits the sorted symbols into halves of near-equal weight; Shannon gives lengths ceil(log2 1/p). Both are near-optimal but not always optimal.
solves: [optimal-prefix-code]
model: word-ram
complexity:
  vars: {n: the number of symbols}
  time: {worst: Θ(n log n), average: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true, online: false, comparison: true}
history:
  year: 1948
  people: [Claude E. Shannon, Robert M. Fano]
  note: Shannon gave the cumulative-probability code in 1948 and Fano the top-down splitting method in an MIT technical report in 1949.
prereqs: [prefix-code, shannon-entropy]
see_also: [huffman-coding, shannon-fano-elias-coding, optimal-prefix-code, source-coding-theorem, kraft-inequality, arithmetic-coding]
sources:
  - paper: doi:10.1002/j.1538-7305.1948.tb01338.x
    title: Claude E. Shannon, A mathematical theory of communication, Bell System Technical Journal 27(3), 1948
    locator: Part I, Section 9, The fundamental theorem for a noiseless channel (the code from the cumulative probabilities)
  - paper: "Robert M. Fano, The transmission of information, Technical Report No. 65, Research Laboratory of Electronics, MIT, 1949"
    locator: the splitting method
  - paper: doi:10.1145/3342555
    title: Alistair Moffat, Huffman coding, ACM Computing Surveys 52(4), 2019
    locator: Section 1.2, Fano's challenge
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition
    locator: Sections 5.4 (the Shannon code lengths) and 5.9 (Shannon-Fano-Elias coding)
  - paper: doi:10.1109/isit.2015.7282755
    title: Stanislav Krajči, Chin-Fu Liu, Ladislav Mikeš and Stefan M. Moser, Performance analysis of Fano coding, IEEE International Symposium on Information Theory, 2015
    locator: pages 1746 to 1750
---

Shannon-Fano coding is the name of two early ways to build a [prefix code](/prefix-code/) from symbol probabilities, which are often mixed up. *Fano's method* (1949) sorts the symbols by probability and splits the list into two parts of nearly equal probability, gives the bit 0 to one part and 1 to the other, and repeats inside each part. *Shannon's method* (1948) gives a symbol of probability $p$ a codeword of $\lceil \log_2 (1/p) \rceil$ bits, read from the binary expansion of the sum of the probabilities before it. Both are within about one bit of the [entropy](/shannon-entropy/), and Shannon's form proves $L < H + 1$, but neither is always optimal. [Huffman coding](/huffman-coding/) (1952) replaced them.

## In plain words

Fano's idea is a game of twenty questions. Put the symbols in order, most common first. Cut the list in two so that both halves are about equally likely. The first bit says which half the symbol is in. Then cut that half in two the same way, and so on, until each part has one symbol. Common symbols are found after few cuts, so they get short codewords.

Shannon's idea fixes the length first. A symbol that occurs once in eight times gets three bits, once in five times also gets three bits, rounding up. To pick the bits, line the symbols up from common to rare and stack their chances one after another on a ruler from zero to one. A symbol's codeword is where its piece starts, written in binary, cut to its length.

## The problem

The input is $n$ symbols with weights $w_1, \ldots, w_n > 0$, the probabilities $p_i$ of a memoryless source or counts of a known message. Here $n$ is the alphabet size, written $\sigma$ in the notation of this area. The output is a prefix code. The aim is a small expected length $L = \sum_i p_i l_i$, the goal of the [optimal prefix code problem](/optimal-prefix-code/); neither method always reaches the optimum.

## The algorithm

**Fano's method.** The symbols are sorted by non-increasing weight. The first call is FANO with the whole list and the empty prefix.

```pseudo id=main
FANO(s[1 .. m], c)                         ▷ s sorted by non-increasing weight; c is the prefix so far
L1  if m = 1 then the codeword of s[1] is c; return
L2  T ← w(s[1]) + … + w(s[m])
L3  k ← the index 1 ≤ k < m that minimizes |2 · (w(s[1]) + … + w(s[k])) − T|, the smallest one on a tie
L4  FANO(s[1 .. k], c·0)
L5  FANO(s[k + 1 .. m], c·1)
```

With one symbol in total, give it the codeword 0 so that each symbol costs one bit.

**Shannon's method.** The probabilities are sorted, $p_1 \ge p_2 \ge \cdots \ge p_n$, and $P_i = p_1 + \cdots + p_{i-1}$ is the probability before symbol $i$.

```pseudo id=shannon
SHANNON(p[1 .. n])                         ▷ p sorted non-increasing, sum 1
S1  P ← 0
S2  for i ← 1 to n do
S3      l ← ⌈log2(1 / p[i])⌉
S4      codeword(i) ← the first l bits after the binary point of P
S5      P ← P + p[i]
```

The lengths of Shannon's code satisfy $2^{-l_i} \le p_i$, so the gap $P_{i+1} - P_i = p_i$ is at least the width $2^{-l_i}$ of the interval of numbers that start with the codeword. That is why no codeword is a prefix of another.

## Example

Take five symbols A to E with counts 15, 7, 6, 6, 5 in a message of 39 symbols.

| step of FANO | list | total | split | difference |
|---|---|---|---|---|
| 1 | A15 B7 C6 D6 E5 | 39 | A B / C D E | 22 against 17 |
| 2 | A15 B7 | 22 | A / B | 15 against 7 |
| 3 | C6 D6 E5 | 17 | C / D E | 6 against 11 |
| 4 | D6 E5 | 11 | D / E | 6 against 5 |

The split A / B C D E has a difference of 24 against 15, which is worse, so step 1 takes A B / C D E.

| symbol | A | B | C | D | E | total bits |
|---|---|---|---|---|---|---|
| count | 15 | 7 | 6 | 6 | 5 | |
| Fano | 00 | 01 | 10 | 110 | 111 | 89 |
| Shannon | 00 | 011 | 100 | 101 | 110 | 102 |
| Huffman | 0 | 100 | 101 | 110 | 111 | 87 |

Fano's code costs 89 bits and Huffman's 87, so Fano's code is not optimal here: putting A alone gives it a 1-bit codeword, which is worth more than the balance of the first split. For Shannon's code, $\lceil \log_2 (39/15) \rceil = 2$ and the other lengths are 3. The starting points are $P = 0, 15/39, 22/39, 28/39, 34/39$, which begin $0.00\ldots, 0.0110\ldots, 0.1001\ldots, 0.1011\ldots, 0.1101\ldots$ in binary, giving the codewords in the table. Shannon's code wastes room: the words 010 and 111 are unused, and the Kraft sum is $3/4$. The entropy is $H \approx 2.186$ bits per symbol, against $89/39 \approx 2.282$ for Fano and $102/39 \approx 2.615$ for Shannon.

## Correctness

Fano's calls form a binary tree with the symbols at the leaves, so the code is prefix-free, and since each split has two non-empty parts the tree is full. For Shannon's code, take $i < j$ in sorted order: then $P_j - P_i \ge p_i \ge 2^{-l_i}$, so $P_j$ is not in the interval of width $2^{-l_i}$ that starts at $P_i$, and the codeword of $i$ is not a prefix of that of $j$. Summing $\log_2 (1/p_i) \le l_i < \log_2 (1/p_i) + 1$ with weights $p_i$ gives $H \le L < H + 1$ for Shannon's code. The weights 15, 7, 6, 6, 5 show that Fano's code is not always optimal. The full proofs are in proofs/correctness.md.

## Complexity

- **Fano's method.** Sorting costs $O(n \log n)$. With prefix sums of the sorted weights, the best split of a sublist is where the prefix sum crosses half of its total, which a binary search finds in $O(\log n)$ time. There are $n - 1$ splits, so the total is $\Theta(n \log n)$. The implementation below scans each sublist instead, which costs $O(n)$ per split and $O(n^2)$ in the worst case.
- **Shannon's method.** Sorting costs $O(n \log n)$, and the codewords take $O(\sum_i l_i)$ bit operations.
- **Space.** $\Theta(n)$ words besides the codewords.

## Properties

- **Prefix-free.** Both methods give prefix codes.
- **Fano's code is full.** Its tree has two children at each inner node, so the Kraft sum is 1 and no codeword is wasted.
- **Shannon's code wastes room.** Its Kraft sum is often below 1. It is optimal only when all $p_i$ are powers of $\frac12$, because a code with Kraft sum below 1 can always be shortened; in that case both methods give an optimal code.
- **Bounds.** Shannon's code has $H \le L < H + 1$. Fano's code stayed below $H + 1$ in all tests below; Krajči, Liu, Mikeš and Moser (2015) analyze its gap from $H$.
- **Not optimal.** Both can be worse than a Huffman code. In random tests with 2 to 12 symbols, Fano's code cost more than Huffman's in about one case in six.
- **Order of codewords.** Both codes assign codewords that increase in the sorted order of the symbols, so on the sorted list they are alphabetic codes.

## Variants and improvements

- **Huffman coding.** Huffman (1952) builds the tree bottom-up and is always optimal; it replaced both methods.
- **[Shannon-Fano-Elias coding](/shannon-fano-elias-coding/).** Shannon's construction without the sort: use the midpoint $P_i + p_i/2$ and one more bit. It keeps the symbol order and leads to [arithmetic coding](/arithmetic-coding/).
- **Other split rules.** Splitting so that the larger part comes first, or choosing the split by a look-ahead, gives other codes; none is optimal in general.
- **$D$-ary codes.** Fano's method splits into $D$ parts of nearly equal weight.

## When to use it

Use these methods to teach prefix codes and the bound $L < H + 1$, or when a code must be built top-down. For real compression, use [Huffman coding](/huffman-coding/): it is as simple, as fast, and always optimal. The ZIP format's old "implode" method is one of few formats that used a code called Shannon-Fano.

## Pitfalls

- **Two different methods.** The name Shannon-Fano means Fano's split in most textbooks and Shannon's cumulative code in others. Say which one.
- **Unsorted input.** Both methods assume the sorted order. Without the sort, Shannon's codewords can be prefixes of each other; that is why Shannon-Fano-Elias coding adds a bit.
- **Tie rules.** A split with equal differences in both directions must be broken the same way by encoder and decoder, or the code must be sent.
- **Floating-point sums.** The bits of $P_i$ in Shannon's method must be exact. Rounding errors in the cumulative sums can give two codewords the same prefix. Use exact fractions or integer counts.

## Implementations

## History

Shannon (1948) described the cumulative-probability code in Section 9 of A mathematical theory of communication, to prove the noiseless coding theorem. Fano (1949) gave the splitting method in an MIT report. Both are top-down, and neither is optimal. Fano posed the problem of an optimal code to the students of his class, and David Huffman, then a student, solved it with the bottom-up method published in 1952 (Moffat 2019, Section 1.2).

## References
