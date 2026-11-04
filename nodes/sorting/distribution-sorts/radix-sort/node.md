---
tag: HB6K6X
kind: algorithm
slug: radix-sort
name: Radix sort (LSD)
aliases:
- LSD radix sort
- Least-significant-digit radix sort
- Digital sort
area: sorting/distribution-sorts
level: intro
summary: Sorts keys digit by digit from least to most significant using a stable sort on each digit.
solves: [integer-sorting, string-sorting]
model: word-ram
complexity:
  vars: {n: the number of items, d: the number of digits of the largest key, b: the base}
  time: {worst: Θ(d(n + b)), average: Θ(d(n + b)), best: Θ(d(n + b))}
  space: {extra: Θ(n + b)}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: false}
history:
  year: 1954
  people: [Harold H. Seward]
  note: Punched-card sorters used the least significant digit first order long before computers. Knuth credits Seward (1954) with radix sorting by distribution counting on a computer.
prereqs: [counting-sort, stable-sort, positional-number-system]
see_also: [msd-radix-sort, radix-sort-time-bound, counting-sort, bucket-sort, integer-sorting, string-sorting, parallel-radix-sort, radix]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 8, Section 8.3, Radix sort (Lemmas 8.3 and 8.4)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Chapter 5, Section 5.1, String Sorts, subsection LSD string sort
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.5, Sorting by Distribution
---

LSD radix sort sorts integer keys one digit at a time, from the least significant digit to the most significant, with a [stable sort](/stable-sort/) on each digit. With $d$ digits in base $b$ and [counting sort](/counting-sort/) as the digit sort, it takes $\Theta(d(n + b))$ time, which is linear in $n$ when $d$ is a constant and $b = O(n)$. It does not compare keys, so the $\Omega(n \log n)$ [comparison lower bound](/comparison-sort-lower-bound/) does not limit it. It also sorts strings of equal length, one character at a time from the last position to the first.

## In plain words

Write each number with the same count of digits, and sort the numbers by their last digit only. Then sort them by the digit before the last, and so on, up to the first digit. Each of these sorts must be stable: when two numbers have the same digit in the current position, the sort keeps them in the order that they already have.

After the sort on the last digit, the numbers are in order of their last digit. After the sort on the next digit, they are in order of their last two digits, because a tie on the new digit keeps the order from the earlier pass. After the last pass they are in order of all their digits, so they are sorted. Each pass is a counting sort over ten possible digits, so it looks at each number one time.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with keys that are integers in $\{0, \ldots, b^d - 1\}$ for a base $b \ge 2$. In base $b$, each key $x$ has the digits $x_t = \lfloor x / b^t \rfloor \bmod b$ for $t = 0, \ldots, d-1$, and $x = \sum_t x_t b^t$ (see [positional number system](/positional-number-system/)). The output is the items in non-decreasing order of key. This is the [integer sorting](/integer-sorting/) problem. Fixed-length strings over an alphabet of size $b$ are the same problem, with the last character as digit 0.

## The algorithm

```pseudo id=main
RADIX-SORT(A, n, b)                        ▷ keys are integers ≥ 0, base b ≥ 2
L1  m ← the largest key in A, or 0 if n = 0
L2  p ← 1                                  ▷ p = b^t at the start of pass t
L3  repeat
L4      A ← COUNTING-SORT(A, n, b, x ↦ ⌊key(x) / p⌋ mod b)    ▷ a stable sort on digit t
L5      p ← p · b
L6  until p > m
L7  return A
```

Line L1 finds the largest key $m$, so the loop runs for exactly $d = \max(1, \lfloor \log_b m \rfloor + 1)$ passes: the number of base-$b$ digits of $m$. Line L4 is one stable [counting sort](/counting-sort/) with $b$ buckets on digit $t$. Line L5 moves to the next digit. The loop stops when $b^{t+1} > m$, that is, when no key has a nonzero digit at a higher position.

## Example

Sort $A = [329, 457, 657, 839, 436, 720, 355]$ in base $b = 10$. The largest key is 839, so there are $d = 3$ passes.

| pass | sort on | the array after the pass |
|---|---|---|
| start | | 329, 457, 657, 839, 436, 720, 355 |
| $t = 0$ | ones digit | 720, 355, 436, 457, 657, 329, 839 |
| $t = 1$ | tens digit | 720, 329, 436, 839, 355, 457, 657 |
| $t = 2$ | hundreds digit | 329, 355, 436, 457, 657, 720, 839 |

In pass $t = 1$, the keys 720 and 329 both have tens digit 2. 720 comes first because its ones digit 0 is smaller, and pass 0 has already put it in front. In pass $t = 2$, 329 and 355 both have hundreds digit 3, and 329 comes first because of its tens digit, from pass 1. In the same way 457 stays in front of 657 in pass 1, because both have ones digit 7 and 457 came first in the input. Each tie on the current digit is broken by the order of the earlier passes.

**Choosing the digit size.** For $n = 10^6$ keys of 64 bits and digits of $r$ bits ($b = 2^r$), the number of passes is $\lceil 64/r \rceil$ and the work is about $\lceil 64/r \rceil (n + 2^r)$ steps:

| $r$ | passes | $\lceil 64/r \rceil (n + 2^r)$ |
|---|---|---|
| 8 | 8 | 8 002 048 |
| 11 | 6 | 6 012 288 |
| 16 | 4 | 4 262 144 |
| 19 | 4 | 6 097 152 |
| 22 | 3 | 15 582 912 |

Here $r = 16$ is best. The count is only a model: in practice the count array must also fit in the cache, which favours digits of 8 to 11 bits.

## Correctness

The proof is by induction on the passes, with this claim: after pass $t$, the items are sorted by the value of their lowest $t + 1$ digits, $\mathrm{key} \bmod b^{t+1}$. Pass $t$ sorts by digit $t$. Two items with different digit $t$ are put in the right order by this pass. Two items with the same digit $t$ keep the order from the earlier passes, because the digit sort is stable, and by the induction hypothesis that order is by the lower $t$ digits. When the loop ends, $b^d > m$, so $\mathrm{key} \bmod b^d = \mathrm{key}$ for each item, and the array is sorted. The result is also stable. The full proof is below, and the [radix sort time bound](/radix-sort-time-bound/) page states the result as a theorem.

## Complexity

Each pass is one counting sort with $b$ buckets, which takes $\Theta(n + b)$ time. There are $d$ passes, and line L1 takes $\Theta(n)$ time. So the time is $\Theta(d(n + b))$ in each case, in the [word RAM](/word-ram/) where a digit extraction costs $O(1)$.

- **Keys of $w$ bits with digits of $r$ bits.** Then $b = 2^r$ and $d = \lceil w / r \rceil$, so the time is $\Theta((w/r)(n + 2^r))$ (CLRS Lemma 8.4). For $w \le \lfloor \lg n \rfloor$ the best choice is $r = w$, one pass, $\Theta(n)$ time. For $w > \lfloor \lg n \rfloor$, the choice $r = \lfloor \lg n \rfloor$ gives $\Theta(w n / \log n)$ time. So keys in $\{0, \ldots, n^c - 1\}$ for a constant $c$ sort in $\Theta(c n) = \Theta(n)$ time.
- **The extra space** is $\Theta(n)$ for the output array of the counting sort and $\Theta(b)$ for the counts. The same two arrays are used in each pass.
- **Strings of length $W$** over an alphabet of size $R$ take $\Theta(W(n + R))$ time.

The bound is linear in $n$ only for a fixed key width. With 64-bit keys and $n = 1000$, the best digit size is $r = 8$, and the model count $8 \cdot (1000 + 256) = 10048$ is about the same as $n \lg n \approx 9966$ comparisons of a comparison sort.

## Properties

- **Stable**, if the digit sort is stable. The proof uses stability in each pass.
- **Not in place.** The counting sort writes to a second array of $n$ items.
- **Not adaptive.** It does all $d$ passes on each input, even a sorted one.
- **Not a comparison sort.** It reads digits of keys and uses them as indices.
- **Oblivious order of work.** Each pass reads the whole array. There is no recursion and no branch that depends on the data, which suits vector units and GPUs.

## Variants and improvements

- **[MSD radix sort](/msd-radix-sort/).** Start from the most significant digit, split into buckets, and sort each bucket on the next digit. It can stop early on a bucket of one item, so it handles strings of different lengths, but it is recursive and has more overhead on small buckets.
- **One counting pass for all digits.** The counts of all $d$ digits can be computed in one read of the input before the first pass. This saves $d - 1$ reads.
- **Signed integers and floats.** Flip the sign bit of a two's complement integer before the sort. For IEEE 754 floats, flip the sign bit of a positive number and all bits of a negative number. Then the unsigned order of the bit patterns is the numeric order.
- **List radix sort.** Knuth's Section 5.2.5 links the items into $b$ queues in each pass instead of counting. This needs a link field per item but no second array.
- **Parallel radix sort.** Each processor counts digits of its own block, and a prefix sum over all count arrays gives each processor its write positions; see [parallel radix sort](/parallel-radix-sort/).

## When to use it

Use LSD radix sort for many integer or fixed-length keys, for example 32-bit or 64-bit integers, IP addresses, or fixed-length codes, when $n$ is large enough that $d$ passes cost less than $\lg n$ comparisons per item. For strings of different lengths use [MSD radix sort](/msd-radix-sort/) or [three-way radix quicksort](/three-way-radix-quicksort/). For keys with a known uniform distribution, [bucket sort](/bucket-sort/) is an alternative. For a few items, or for keys with an expensive digit extraction, a comparison sort is faster.

## Pitfalls

- **An unstable digit sort.** If line L4 uses a sort that is not stable, for example a counting sort with a forward pass over end positions, or a quicksort, the later passes destroy the order of the earlier ones. The result is then sorted only by the most significant digit.
- **The wrong digit order.** Starting from the most significant digit with the same loop gives an array sorted by the least significant digit. The LSD loop must go from digit 0 upwards. Starting at the top needs the recursive MSD method.
- **Too few passes.** Computing $d$ from the first key or from a fixed width that is too small leaves the high digits unsorted. Line L1 uses the largest key.
- **Negative keys.** The expression $\lfloor x/p \rfloor \bmod b$ puts negative keys in the wrong place, since they have no valid base-$b$ digits. Shift the keys by the minimum, or flip the sign bit as in the variants.

## Implementations

## History

Card sorters for punched cards sort a deck on one column at a time, and operators sorted a multi-column key by running the deck through the machine from the last column to the first. This is LSD radix sort, used long before electronic computers. Knuth (Section 5.2.5) gives the history and credits H. H. Seward (1954) with the computer form that uses distribution counting instead of separate piles.

## References
