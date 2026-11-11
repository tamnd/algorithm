---
tag: Y4RNV8
kind: algorithm
slug: package-merge
name: Package-merge algorithm
aliases:
- Larmore-Hirschberg algorithm
- package-merge
area: compression-and-coding/entropy-coding
level: advanced
summary: Computes an optimal prefix code with no codeword longer than L bits in O(nL) time, by pairing the cheapest items into packages and merging them with the symbols, level by level.
solves: [length-limited-prefix-code]
model: word-ram
complexity:
  vars: {n: the number of symbols, L: the length limit}
  time: {worst: Θ(n L), average: Θ(n L)}
  space: {extra: Θ(n L)}
properties: {deterministic: true, recursive: false, online: false, comparison: true}
history:
  year: 1990
  people: [Lawrence L. Larmore, Daniel S. Hirschberg]
  note: Larmore and Hirschberg published package-merge in the Journal of the ACM in 1990, with a reduction to the coin collector's problem and a version in linear space.
prereqs: [length-limited-prefix-code, huffman-coding]
see_also: [canonical-huffman-code, optimal-prefix-code, deflate, jpeg-compression, kraft-inequality, greedy-algorithm, exchange-argument]
sources:
  - paper: doi:10.1145/79147.79150
    title: Lawrence L. Larmore and Daniel S. Hirschberg, A fast algorithm for optimal length-limited Huffman codes, Journal of the ACM 37(3), 1990
    locator: pages 464 to 473 (the coin collector's problem, package-merge, and the O(n) space version)
  - paper: doi:10.1145/3342555
    title: Alistair Moffat, Huffman coding, ACM Computing Surveys 52(4), 2019
    locator: Section 4.1, Length-limited codes (Algorithm 3 and Figure 6)
  - paper: doi:10.1093/comjnl/38.5.339
    title: Andrew Turpin and Alistair Moffat, Practical length-limited coding for large alphabets, The Computer Journal 38(5), 1995
    locator: pages 339 to 347 (reverse package-merge)
---

Package-merge computes an optimal [length-limited prefix code](/length-limited-prefix-code/): a code of least weighted length in which no codeword is longer than $L$ bits. Larmore and Hirschberg (1990) found it by a reduction to a coin problem: each symbol has one coin for each depth, and a code is a set of coins of a fixed total value. Coins of the smallest value can only be used in pairs, so the algorithm pairs the cheapest ones into packages, merges the packages with the next coins, and repeats. It runs in $O(nL)$ time, and with $L$ larger than any Huffman length it gives a Huffman code.

## In plain words

Think of each symbol as owning a row of coins: a half, a quarter, an eighth, and so on, down to the smallest size allowed by the limit. Each coin costs as much as the symbol's weight. If you buy coins worth exactly one less than the number of symbols, the number of coins each symbol sold you is a valid codeword length, and the price you paid is the cost of the code.

So the task is to buy that amount as cheaply as possible. The smallest coins are only useful in pairs, because the rest are bigger. So pair them, cheapest with next cheapest, and treat each pair as one coin of the next size. Mix these pairs in with the real coins of that size, and do the same again. At the top, take the cheapest half-coins you need.

## The algorithm

The weights are sorted, $w_1 \le w_2 \le \cdots \le w_n$, and $n \le 2^L$. The list $Q_k$ holds items of face value $2^{-(L - k + 1)}$: so $Q_1$ holds the coins of the deepest level $L$, and $Q_L$ holds the items of face value $\frac12$. An item is a *leaf*, that is a coin of one symbol, or a *package* of two items of the list before it.

```pseudo id=main
PACKAGE-MERGE(w[1 .. n], L)                ▷ w sorted non-decreasing, 2 ≤ n ≤ 2^L
L1  Q_1 ← the leaves w[1], …, w[n]
L2  for k ← 2 to L do
L3      P ← the packages (Q_{k−1}[1], Q_{k−1}[2]), (Q_{k−1}[3], Q_{k−1}[4]), …, each of weight the sum of its two items; drop a last odd item
L4      Q_k ← MERGE(w[1 .. n], P) by weight, a leaf before a package of equal weight
L5  r ← 2n − 2                             ▷ take the first r items of Q_L
L6  for k ← L downto 1 do
L7      c ← the number of leaves among the first r items of Q_k
L8      for j ← 1 to c do l[j] ← l[j] + 1   ▷ the leaves are the c lightest symbols
L9      r ← 2 · (r − c)                     ▷ the packages are the first r − c, made of the first 2(r − c) items of Q_{k−1}
L10 return l[1 .. n]
```

Lines L1 to L4 are the *package* and *merge* phases. Line L5 chooses the $2n - 2$ cheapest items of face value $\frac12$, which have total face value $n - 1$. Lines L6 to L9 expand the chosen packages level by level: each time a symbol's leaf is chosen at some level, its codeword gets one bit longer. Only the order of leaves and packages in each list is needed for the expansion, not the packages themselves, which is why each level costs $O(n)$.

The lengths can then be turned into codewords with a [canonical code](/canonical-huffman-code/).

## Example

Take the weights of Moffat (2019, Figure 6), sorted: $w = (1, 1, 1, 2, 2, 2, 3, 6, 17, 20)$, with $n = 10$ and $L = 5$. A trailing P marks a package. The bold part of each list is the prefix that the expansion takes.

| list | items in order of weight | $r$ | leaves $c$ in the prefix |
|---|---|---|---|
| $Q_5$ | **1 1 1 2 2 2 2P 3 3P 4P 5P 6 7P 11P 17 18P 20 37P** 59P | 18 | 10 |
| $Q_4$ | **1 1 1 2 2 2 2P 3 3P 4P 5P 6 7P 11P 17 20** 22P 37P | 16 | 10 |
| $Q_3$ | **1 1 1 2 2 2 2P 3 3P 4P 5P 6** 7P 15P 17 20 37P | 12 | 8 |
| $Q_2$ | **1 1 1 2 2 2 2P 3** 3P 4P 6 9P 17 20 37P | 8 | 7 |
| $Q_1$ | **1 1** 1 2 2 2 3 6 17 20 | 2 | 2 |

In $Q_5$ the 18 cheapest items contain 8 packages, so the expansion takes 16 items of $Q_4$, and so on down. A symbol's length is the number of lists in which its leaf is in the prefix. The two symbols of weight 1 that come first are in all five prefixes and get length 5; the third symbol of weight 1, the three of weight 2 and the one of weight 3 are in the prefixes of $Q_5$ to $Q_2$ and get length 4; weight 6 gets length 3; weights 17 and 20 get length 2.

| weight | 20 | 17 | 6 | 3 | 2 | 2 | 2 | 1 | 1 | 1 |
|---|---|---|---|---|---|---|---|---|---|---|
| length, $L = 5$ | 2 | 2 | 3 | 4 | 4 | 4 | 4 | 4 | 5 | 5 |
| Huffman length | 1 | 2 | 4 | 5 | 5 | 5 | 5 | 5 | 6 | 6 |

The cost is 142 bits, against 140 for the Huffman code, whose longest codeword has 6 bits. With $L = 4$ the result is $(2, 2, 4, 4, 4, 4, 4, 4, 4, 4)$ with cost 146, and $L = 3$ is impossible because $2^3 < 10$. These are the values of Moffat's Figure 6.

## Correctness

Two facts give the proof. First, codes and coin sets match: each symbol $i$ has a coin of face value $2^{-d}$ and cost $w_i$ for each depth $d \le L$; for a set of coins with total face value $n - 1$, the numbers of coins $l_i$ of the symbols satisfy the Kraft inequality, and the cost of the set is $\sum_i w_i l_i$; conversely each code with Kraft sum 1 gives such a set. Second, a greedy lemma: since the target $n - 1$ is a multiple of each larger face value, an optimal set uses an even number of the smallest items, and by an [exchange argument](/exchange-argument/) these are the cheapest ones, so they can be replaced by packages of consecutive pairs without changing the optimum. Applying the lemma $L - 1$ times leaves items of face value $\frac12$, where the best choice is the $2n - 2$ cheapest. The expansion of lines L6 to L9 counts the leaves correctly because leaves and packages appear in each list in the order in which they were made. The full proof is in proofs/correctness.md.

## Complexity

- **Time.** The list $Q_k$ has fewer than $2n$ items, so each package and merge pass takes $O(n)$ time, and so does each step of the expansion. The total is $\Theta(nL)$ after an $O(n \log n)$ sort. Since $L \ge \lceil \log_2 n \rceil$ for a code to exist, and $L \le n - 1$ is enough for a Huffman code, this lies between $O(n \log n)$ and $O(n^2)$.
- **Space.** The implementation keeps one flag for each item of each list, $\Theta(nL)$ bits. Larmore and Hirschberg (1990) also give a version in $O(n)$ space, at a constant factor more time.
- **The number of levels.** Only levels where the code can change matter. Turpin and Moffat (1995) work with the complement of the solution and need $O(n(L - \log_2 n + 1))$ time, which is linear when $L$ is close to $\log_2 n$.

## Properties

- **Exact.** The result is an optimal length-limited code, unlike the heuristics of zlib and JPEG.
- **Monotone.** A heavier symbol never gets a longer codeword: the leaves in each prefix are the lightest symbols.
- **Huffman as a special case.** For $L \ge n - 1$ the limit does not bind and the result has the cost of a Huffman code.
- **Full code.** The chosen coins have total face value $n - 1$, so the lengths satisfy the Kraft inequality with equality.
- **Deterministic ties.** With a fixed rule for equal weights (here, a leaf before a package), encoder and decoder do not need to agree on anything but the lengths, which are sent anyway.

## Variants and improvements

- **Linear space.** Larmore and Hirschberg (1990) give a recursive version that needs $O(n)$ space.
- **$O(L^2)$ space.** Katajainen, Moffat and Turpin (1995) compute the lengths in $O(nL)$ time with $O(L^2)$ extra space, following the chains of packages lazily (see Moffat 2019, Section 4.1).
- **Reverse package-merge.** Turpin and Moffat (1995) compute the complement of the solution, in $O(n(L - \log_2 n + 1))$ time.
- **From a Huffman code.** Liddell and Moffat start from a Huffman code and change only what the limit forces, in $O(n(L_{\text{Huff}} - L + 1))$ time (Moffat 2019, Section 4.1).
- **Coin collector's problem.** The same method solves the general problem of paying a target sum with coins whose face values are powers of 2, at least cost.

## When to use it

Use package-merge when a format limits the codeword length and an exact optimum is wanted, for example in an encoder that tunes DEFLATE or JPEG tables for size, as zopfli does for DEFLATE. When speed matters more than the last fraction of a percent, the repair heuristics of zlib and JPEG are simpler and usually lose very little (see [length-limited prefix code](/length-limited-prefix-code/)). If the Huffman code already respects the limit, compute only the Huffman code.

## Pitfalls

- **Infeasible limits.** If $2^L < n$ no code exists; check before running, or the expansion asks for more items than the lists have.
- **Unsorted weights.** The expansion assumes that the leaves in each list come in the order of the symbols. Sort the weights first and map the lengths back to the symbols.
- **Zero weights.** A symbol of weight 0 still gets a codeword. Drop unused symbols before the call, as DEFLATE does by giving them length 0.
- **Odd lists.** The last item of an odd list has no partner and must be dropped in line L3, not paired with a leaf of the next level.
- **Counting the wrong packages.** The expansion relies on the packages in each list being in the order in which they were made. Merging with an unstable rule that reorders equal packages breaks the count of line L9.

## Implementations

## History

Hu and Tan (1972) and Van Voorhis (1974) gave the first exact algorithms for length-limited codes, which were slower. Larmore and Hirschberg (1990) published package-merge in the Journal of the ACM, with its reduction to the coin collector's problem, the $O(nL)$ time bound and a linear-space version. Katajainen, Moffat and Turpin, and Turpin and Moffat, gave faster and smaller versions in 1995.

## References
