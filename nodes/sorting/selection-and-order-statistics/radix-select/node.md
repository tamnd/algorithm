---
tag: ZPSQHH
kind: algorithm
slug: radix-select
name: Radix select
aliases:
- bucket select
- digit-wise selection
area: sorting/selection-and-order-statistics
level: advanced
summary: Find the element of a given rank by examining keys digit by digit and narrowing the candidate buckets.
solves: [selection-problem]
model: word-ram
complexity:
  vars: {n: the number of keys, w: the number of bits of a key, r: the number of bits of a digit}
  time: {worst: O((n + 2^r) w / r), best: O(n + 2^r)}
  space: {extra: O(n + 2^r)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: false}
history:
  year: 2000
  people: [Hosam M. Mahmoud, Philippe Flajolet, Philippe Jacquet, Mireille Régnier]
  note: Selection by digits is a folklore variant of MSD radix sort; Mahmoud, Flajolet, Jacquet and Régnier analyzed bucket selection, its form with general buckets, in 2000.
prereqs: [selection-problem, msd-radix-sort]
see_also: [msd-radix-sort, counting-sort, quickselect, bucket-sort, american-flag-sort, word-ram, trie, top-k-selection]
sources:
  - paper: "Hosam M. Mahmoud, Philippe Flajolet, Philippe Jacquet and Mireille Régnier, Analytic variations on bucket selection and sorting, Acta Informatica 36(9-10) (2000)"
    locator: pages 735 to 760 (bucket selection and its average cost)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2 (radix exchange sorting) and Section 5.2.5, Sorting by distribution (MSD radix sorting)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 5.1, String sorts (MSD string sort and key-indexed counting)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 8, Sections 8.2 and 8.3 (counting sort and radix sort)
---

Radix select finds the item of rank $k$ among $n$ integer keys without comparing keys with each other. It looks at the most significant digit of each key, counts how many keys fall in each digit value, and keeps only the bucket that must contain rank $k$; then it repeats on the next digit inside that bucket. It is the selection form of [MSD radix sort](/msd-radix-sort/), in which only one bucket is followed at each level instead of all of them. With $w$-bit keys and digits of $r$ bits it takes $O((n + 2^r) w / r)$ time in the worst case, and on keys spread evenly it touches each key about once.

## In plain words

You want the person with the 500th smallest phone number in a city. Sort the cards into ten piles by the first digit and count each pile. If the piles for the first digits 0 to 3 hold 420 cards and the pile for 4 holds 200, the answer is in pile 4, and it is the 80th smallest card in that pile.

Throw away all other piles and repeat with the second digit, inside pile 4. Each round keeps one pile, which is usually a small part of the cards, and you never compare two phone numbers. When the digits run out, or one card is left, that card is the answer.

## The problem

Given $n \ge 1$ keys that are integers in $[0, 2^w)$ and a rank $k$ with $1 \le k \le n$, return the $k$-th smallest key: the [selection problem](/selection-problem/) on a [word RAM](/word-ram/), where a key can be split into digits in constant time. Other keys, such as signed integers, floating-point numbers and fixed-length strings, can be mapped to such integers by a map that keeps the order.

## The algorithm

A key has $d = \lceil w / r \rceil$ digits of $r$ bits. Digit $j$ of $x$, counted from $0$ at the least significant end, is $\operatorname{dig}_j(x) = \lfloor x / 2^{rj} \rfloor \bmod 2^r$.

```pseudo id=main
RADIX-SELECT(A[1 .. n], k)                 ▷ keys in [0, 2^w), 1 ≤ k ≤ n
L1  S ← A; d ← ⌈w / r⌉
L2  for j ← d − 1 downto 0 do              ▷ from the most significant digit
L3      if |S| = 1 then return S[1]
L4      C[0 .. 2^r − 1] ← 0
L5      for each x in S do C[dig_j(x)] ← C[dig_j(x)] + 1
L6      b ← 0
L7      while k > C[b] do k ← k − C[b]; b ← b + 1
L8      S ← the keys x of S with dig_j(x) = b
L9  return S[1]                            ▷ all keys of S are equal
```

Lines L4 and L5 are the counting pass of [counting sort](/counting-sort/). Line L7 walks through the buckets in order and subtracts the sizes of the buckets below the one that holds rank $k$, so after it the answer is the key of rank $k$ inside bucket $b$. Line L8 keeps that bucket. After the last digit, all keys left agree on every digit, so they are equal.

## Example

For $A = [31, 41, 59, 26, 53, 58, 97, 93, 23, 84]$ and $k = 5$, with $w = 7$ and $r = 4$, so $d = 2$ digits, the high digit of $x$ is $\lfloor x / 16 \rfloor$:

| key | 31 | 41 | 59 | 26 | 53 | 58 | 97 | 93 | 23 | 84 |
|---|---|---|---|---|---|---|---|---|---|---|
| high digit | 1 | 2 | 3 | 1 | 3 | 3 | 6 | 5 | 1 | 5 |

The counts are $C[1] = 3$, $C[2] = 1$, $C[3] = 3$, $C[5] = 2$, $C[6] = 1$. Line L7 skips bucket $1$ ($k$ becomes $2$) and bucket $2$ ($k$ becomes $1$), and stops at bucket $3$, so $S = [59, 53, 58]$ with $k = 1$. Their low digits are $11$, $5$ and $10$, so bucket $5$ is the first that is not empty, and $S = [53]$. The answer is $53$, the fifth smallest.

## Correctness

At the start of the pass for digit $j$ the loop keeps this [invariant](/loop-invariant/): all keys of $S$ have the same digits above position $j$, $1 \le k \le |S|$, and the key of rank $k$ of $S$ is the answer. It holds at the start, with no digits above position $d - 1$ inside $[0, 2^w)$. Two keys with the same higher digits compare as their digit $j$ does whenever those differ, so the buckets $0, 1, \ldots$ of line L5 come in increasing order of keys: each key of a lower bucket is less than each key of a higher one. So if the buckets below $b$ hold $c$ keys in total and $c < k \le c + C[b]$, the key of rank $k$ of $S$ is the key of rank $k - c$ of bucket $b$, which is what lines L7 and L8 keep. After the last pass the keys of $S$ agree on all digits, so they are equal, and each of them is the answer. The full proof is in the proof file below.

## Complexity

- **Worst case, $O((n + 2^r) w / r)$.** Each of the $d = \lceil w / r \rceil$ passes reads at most $n$ keys and clears and scans $2^r$ counters. This happens when many keys share their high digits, for example when $n$ keys agree on all digits but the last.
- **Keys spread evenly, $O(n + 2^r w / r)$.** If the keys are uniform random $w$-bit integers, each bucket holds about a $2^{-r}$ fraction of the keys, so the passes read about $n + n/2^r + n/2^{2r} + \cdots$ keys. For $10^6$ random 32-bit keys and $r = 8$, the median was found after reading $1.004n$ keys: the buckets kept $3929$, then $19$, then $1$ key.
- **Choice of $r$.** A larger $r$ means fewer passes but $2^r$ counters per pass. With $r$ near $\lg n$, the first pass costs $O(n)$ and leaves about one key per bucket on spread-out data; $r = 8$ or $r = 11$ are common in practice.
- **Space.** The counters take $2^r$ words, and the list version keeps a copy of the current bucket, at most $n$ keys. An in-place version moves the kept bucket to the front of the array, as in [American flag sort](/american-flag-sort/).

## Properties

- **Not comparison based.** It reads digits of keys, so the $\Omega(n)$ comparison lower bound is not the relevant limit, and its cost does not depend on the order of the input.
- **Deterministic.** There are no random choices; the cost depends only on the multiset of keys.
- **Not in place** in the form above.
- **Not stable.** It returns a key value; the position of equal keys is not kept.

## Variants and improvements

- **Signed and floating-point keys.** Flip the sign bit of two's-complement integers. For IEEE floating-point numbers, flip all bits of negative numbers and only the sign bit of the others; the resulting unsigned integers are in the same order as the numbers.
- **Bucket select.** Split by value ranges instead of bits, as in [bucket sort](/bucket-sort/): $m$ buckets of equal width between the minimum and the maximum. This is the method analyzed by Mahmoud, Flajolet, Jacquet and Régnier.
- **The $k$ smallest.** Keep all buckets below $b$ as part of the answer at each level; the result is the [top-k](/top-k-selection/) set without any comparison. GPU libraries use this form to find the top $k$ entries of large arrays, since each pass is a parallel histogram.
- **Switch to quickselect.** When the current bucket is small, sorting it or a few steps of [quickselect](/quickselect/) can be faster than more counting passes.
- **Strings.** For variable-length strings the digits are characters, as in MSD string sort, and the method follows one branch of the implicit [trie](/trie/).

## When to use it

Use it for large arrays of integers or floating-point numbers, when comparisons are not cheaper than digit extraction and the cost should not depend on the order of the input, and on parallel hardware where a histogram is cheap. For general keys with only a comparison, or for small arrays, [quickselect](/quickselect/) is simpler. When many keys share long prefixes, the extra passes make it slower than quickselect.

## Pitfalls

- **Negative keys taken as unsigned.** Without the sign-bit flip, negative numbers sort after the positive ones.
- **Forgetting to update $k$.** The rank must be taken relative to the kept bucket: subtract the sizes of all lower buckets.
- **Many equal keys.** If all keys are equal, every pass keeps all of them; the method is still correct, but it pays the full $d$ passes.
- **Too large a digit.** With $r = 16$ on a list of a thousand keys, clearing $65536$ counters per pass costs far more than reading the keys.

## Implementations

## History

Selecting by digits is a folklore adaptation of MSD radix sorting, which goes back to the punched-card sorters of the early twentieth century; Knuth describes the sorting forms in Sections 5.2.2 and 5.2.5. Mahmoud, Flajolet, Jacquet and Régnier gave an analysis of bucket selection, the form with value buckets, in Acta Informatica in 2000. Parallel radix selection has since become a standard way to find the top $k$ entries on graphics processors.

## References
