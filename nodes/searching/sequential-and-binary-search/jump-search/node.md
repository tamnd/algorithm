---
tag: FX08EH
kind: algorithm
slug: jump-search
name: Jump search
aliases:
- block search
area: searching/sequential-and-binary-search
level: intro
summary: Jump ahead by blocks of size about sqrt(n) to find the block that could hold the key, then scan that block linearly.
solves: [search-in-sorted-array]
model: comparison-model
complexity:
  vars: {n: the number of items in the array}
  time: {worst: Θ(√n), average: Θ(√n), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, comparison: true, recursive: false, in_place: true}
prereqs: [linear-search, binary-search]
see_also: [linear-search, binary-search, exponential-search, sentinel-search, search-in-sorted-array, lower-bound-query]
sources:
  - paper: doi:10.1145/359619.359623
    title: Ben Shneiderman, Jump searching, a fast sequential search technique, Communications of the ACM 21(10) (1978)
    locator: pp. 831 to 834 (the jump size square root of n, multi-level and variable jumps)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.1 (sequential search in an ordered table) and Section 6.2.1 (searching an ordered table)
---

Jump search finds a key $x$ in a sorted array by testing every $m$-th item until it passes $x$, and then scanning the one block of $m$ items that can hold $x$. With the block size $m = \lfloor \sqrt{n} \rfloor$ it makes at most about $2\sqrt{n}$ comparisons, so its time is $\Theta(\sqrt{n})$ in the worst case. That is far more than the $\lg n$ of [binary search](/binary-search/), but jump search moves only forward and reads the items in long forward runs, which is cheap on a tape, a linked file with skip pointers, or any medium where a step back costs much more than a step ahead. It returns the first occurrence of $x$.

## In plain words

You look for a page in a thick binder with sorted pages, and you can only flip forward. You flip ten pages at a time and read only the last page of each jump. When that page is past what you want, you know the page you want is among the last ten you flipped. You go back to the start of that group once and read those pages one by one.

If the jumps are too short, you make many jumps. If they are too long, the final group is long to read. The best jump length is about the square root of the number of pages: for ten thousand pages, jumps of one hundred, and about two hundred looks in the worst case.

## The problem

The input is an array $A[0 \ldots n-1]$, $n \ge 0$, sorted so that $A[0] \le \cdots \le A[n-1]$, and a key $x$. The output is the smallest index $i$ with $A[i] = x$, or NIL when $x$ is not in $A$. This is [search in a sorted array](/search-in-sorted-array/), with the first occurrence as the answer. The algorithm uses only comparisons of $x$ with items.

## The algorithm

The algorithm keeps a block $[lo, hi)$ of the array. All items before $lo$ are less than $x$.

```pseudo id=main
JUMP-SEARCH(A, x)
L1  m ← max(1, ⌊√n⌋)                  ▷ the block size
L2  lo ← 0, hi ← min(m, n)             ▷ the first block is A[0 .. hi − 1]
L3  while hi < n and A[hi − 1] < x do  ▷ the whole block is less than x
L4      lo ← hi, hi ← min(hi + m, n)   ▷ jump to the next block
L5  i ← lo
L6  while i < hi and A[i] < x do       ▷ scan the block for the first A[i] ≥ x
L7      i ← i + 1
L8  if i < n and A[i] = x then return i
L9  return NIL
```

Lines L3 and L4 are the jumps. The test reads the last item of the current block. When it is less than $x$, the whole block is less than $x$, because the array is sorted, so the search moves on. The loop stops at the last block, or at the first block whose last item is at least $x$. Lines L5 to L7 are a [linear search](/linear-search/) in that block for the first item that is not less than $x$. This index is the [lower bound](/lower-bound-query/) of $x$. Line L8 tests whether it holds $x$.

The test of line L3 does not look at the last block, because $hi = n$ there; the scan of line L6 covers it.

## Example

The array has $n = 16$ items, so $m = 4$:

| index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $A$ | 3 | 8 | 11 | 15 | 19 | 23 | 27 | 31 | 35 | 40 | 44 | 50 | 57 | 62 | 68 | 71 |

Search for $x = 57$:

| step | line | $lo$ | $hi$ | test | result |
|---|---|---|---|---|---|
| 1 | L3 | 0 | 4 | $A[3] = 15 < 57$ | jump |
| 2 | L3 | 4 | 8 | $A[7] = 31 < 57$ | jump |
| 3 | L3 | 8 | 12 | $A[11] = 50 < 57$ | jump |
| 4 | L3 | 12 | 16 | $hi = n$ | stop jumping |
| 5 | L6 | 12 | 16 | $A[12] = 57 < 57$ is false | stop, $i = 12$ |
| 6 | L8 | | | $A[12] = 57$ | return 12 |

That is 5 comparisons of items: 3 jumps, 1 in the scan and the final equality test. A search for $x = 20$ makes one jump ($A[3] = 15 < 20$), stops at $A[7] = 31$, scans $A[4] = 19$ and $A[5] = 23$, and finds $A[5] \ne 20$: 5 comparisons and the answer NIL. A search for $x = 80$ makes 3 jumps and scans all of the last block: 7 comparisons, then $i = 16 = n$ and the answer NIL.

## Correctness

The jump loop keeps this invariant: $0 \le lo \le hi \le n$, $hi - lo \le m$, and $A[j] < x$ for each $j < lo$. A jump runs only when $A[hi - 1] < x$, so all of $A[lo \ldots hi-1]$ is less than $x$ and the new $lo = hi$ keeps it. When the loop stops, either $hi = n$, or $A[hi - 1] \ge x$; in both cases the lower bound $\ell$ of $x$ lies in $[lo, hi]$. The scan then stops at $i = \ell$. Since the copies of $x$ start at $\ell$, line L8 returns the first occurrence when $x$ is present and NIL otherwise. Each jump increases $hi$ by $m \ge 1$ until $hi = n$, and each scan step increases $i$, so both loops stop. The full proof is below.

## Complexity

Count the comparisons of items. Let $m = \max(1, \lfloor \sqrt{n} \rfloor)$ and let $b = \lceil n/m \rceil$ be the number of blocks.

- **Jumps.** Line L3 compares only while $hi < n$, which holds in at most $b - 1$ blocks. So the jumps make at most $b - 1$ comparisons.
- **Scan.** The block has at most $m$ items, so line L6 makes at most $m$ comparisons.
- **Final test.** Line L8 makes at most one.

So the total is at most $b - 1 + m + 1 = \lceil n/m \rceil + m$. For a perfect square $n = m^2$ this is $2m = 2\sqrt{n}$, and the key $x = A[n-1]$ (with distinct items) reaches it: $m - 1$ jumps, $m$ scan steps and one equality test. The table gives the worst case of the pseudocode over all keys, on the array $[0, 2, 4, \ldots, 2n-2]$:

| $n$ | 16 | 100 | 1000 |
|---|---|---|---|
| $m$ | 4 | 10 | 31 |
| worst case, comparisons | 8 | 20 | 64 |
| bound $\lceil n/m \rceil + m$ | 8 | 20 | 64 |

- **Worst case.** For $n \ge 4$, since $m > \sqrt{n} - 1$, $\lceil n/m \rceil + m < n/(\sqrt{n} - 1) + 1 + \sqrt{n}$, which is $2\sqrt{n} + O(1)$, so the time is $\Theta(\sqrt{n})$. The choice $m \approx \sqrt{n}$ is optimal for this scheme: the cost $n/m + m$ is smallest when $m = \sqrt{n}$, by the inequality $n/m + m \ge 2\sqrt{n}$.
- **Average case.** For a key at a uniform random index, the jumps cost about half of the $\sqrt{n}$ blocks and the scan about half a block, so about $\sqrt{n}$ comparisons: $\Theta(\sqrt{n})$.
- **Best case.** A key at most $A[m-1]$ costs one jump test and a few scan steps; a key at index 0 costs 3 comparisons. That is $\Theta(1)$.
- **Space.** Four indices: $\Theta(1)$.

## Properties

- **Forward only, with one step back.** The jumps move forward, and the scan goes back once, at most $m$ items, to the start of the block.
- **First occurrence.** The scan stops at the lower bound, so the result is the smallest index of $x$.
- **Comparison-based.** It uses only $<$ and $=$ on items.
- **In place.** It does not change the array.

## Variants and improvements

- **Jump, then binary search.** Search the final block with [binary search](/binary-search/) instead of a scan. The cost is then about $n/m + \lg m$, and the best $m$ is larger. With $m = n/\lg n$ the total is $O(\log n)$, but then the method is close to a binary search with a bad first step.
- **Multi-level jumps.** Jump by $n^{2/3}$, then by $n^{1/3}$ inside the block, then scan. With $k$ levels the cost is about $k\, n^{1/k}$. Shneiderman studies these variants.
- **Variable jumps.** If the key is more likely to be near the start, use shorter jumps there.
- **[Exponential search](/exponential-search/).** Jump by $1, 2, 4, 8, \ldots$, which doubles each time. The jumps then cost $O(\log i)$ for a key at index $i$, and the block is searched by binary search.
- **Unsorted version.** Without order the jumps give no information, and the method falls back to a [linear search](/linear-search/).

## When to use it

Use jump search when the data is sorted, a step back is much more costly than a step forward, and random access is not available or not cheap: a sorted file on a tape, a sorted linked list with a pointer every $m$ nodes, or a compressed sorted list where only every $m$-th item is stored in full. When the array is in memory and random access costs the same everywhere, [binary search](/binary-search/) is better: 20 comparisons for a million items against 2000.

## Pitfalls

- **Block size 0.** For $n < 1$ the value $\lfloor \sqrt{n} \rfloor$ is 0, and a loop that adds $m = 0$ never ends. Line L1 takes $\max(1, \cdot)$.
- **Reading past the end.** A jump that sets $hi \gets hi + m$ without the minimum of line L4 can test $A[hi - 1]$ beyond the array. Line L3 also tests $hi < n$ before it reads $A[hi - 1]$.
- **Testing the first item of the next block.** A version that jumps while $A[hi] \le x$ moves past a block that starts with $x$ when there are copies before it, and then misses the first occurrence. Test the last item of the current block with $<$, as in line L3.
- **Using a floating-point square root.** For large $n$, a float square root can round so that $m^2 > n$. Use an integer square root, such as `math.isqrt` in Python.
- **Final test on $A[n]$.** The scan can end with $i = n$. Line L8 tests $i < n$ before it reads $A[i]$.

## Implementations

## History

Shneiderman described jump search, with the optimal jump size $\sqrt{n}$ and its multi-level and variable-size variants, in Communications of the ACM in 1978, for sequential files where binary search is not possible.

## References
