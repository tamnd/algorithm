---
tag: JZA43S
kind: algorithm
slug: in-place-merge-sort
name: In-place merge sort
aliases:
- in-place stable merge sort
area: sorting/comparison-sorts
level: advanced
summary: Merge sort using O(1) extra space via in-place merging, at a cost in running time.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: O(n log² n), average: Θ(n log² n), best: Θ(n log n), comparisons: O(n log n)}
  space: {extra: O(log n)}
properties: {stable: true, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: true}
history:
  year: 1981
  people: [Krzysztof Dudziński, Andrzej Dydek]
  note: Dudziński and Dydek gave the stable merge without a buffer that splits one run at its middle, cuts the other by binary search and rotates the middle blocks; Kim and Kutzner gave the symmetric form SymMerge in 2004.
prereqs: [merge-sort, binary-search, vector-rotation, in-place-algorithm]
see_also: [block-sort, stable-sort, merging-sorted-sequences, merging-lower-bound, insertion-sort, heapsort, timsort, java-system-sort]
sources:
  - paper: "Krzysztof Dudziński and Andrzej Dydek, On a stable minimum storage merging algorithm, Information Processing Letters 12(1), 1981"
    locator: pp. 5 to 8 (the recursive merge by binary search and rotation)
  - paper: "Pok-Son Kim and Arne Kutzner, Stable minimum storage merging by symmetric comparisons, ESA 2004, LNCS 3221"
    locator: pp. 714 to 723 (SymMerge, and the comparison bound O(m log(n/m + 1)) for merging runs of lengths m ≤ n)
  - paper: "Jyrki Katajainen, Tomi Pasanen and Jukka Teuhola, Practical in-place mergesort, Nordic Journal of Computing 3(1), 1996"
    locator: pp. 27 to 40 (an unstable in-place merge sort with n lg n + O(n) comparisons that uses part of the array as the buffer)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.4, Sorting by merging (merging with little extra memory, in the exercises)
---

In-place merge sort is [merge sort](/merge-sort/) with a merge that needs no second array. The version on this page merges two sorted runs like this: it takes the middle item of the longer run, finds by [binary search](/binary-search/) where that item belongs in the other run, swaps the two blocks between the cut points with a [rotation](/vector-rotation/), and then merges the two smaller pairs of runs that result. The sort stays stable and makes $O(n \log n)$ comparisons, but the rotations move items $O(n \log^2 n)$ times, so it is slower than merge sort with a buffer by a factor of $\log n$. It is the fall-back that C++ `std::stable_sort` uses when it cannot get memory, and Go's `sort.Stable` uses the symmetric form of the same merge.

## In plain words

You have two sorted piles laid out side by side on a narrow shelf, with no room for a third pile. Take the middle book of the longer pile. Find where it would go in the other pile.

Now the books split into four blocks. Swap the two blocks in the middle, keeping the order inside each block. After the swap, every book on the left of the chosen book is no larger than every book on its right. So the shelf now holds two smaller merge jobs, one on each side, and you do each in the same way.

To sort, split the shelf in half, sort each half the same way, and merge the halves with this method. Swapping blocks moves many books, so the method is slower than merging into a second shelf. But it needs no second shelf, and equal books keep their order.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order, which the algorithm can only compare with $<$. The output is the same array in non-decreasing order, and items with equal keys keep their input order. This is the [sorting problem](/sorting-problem/) with the extra demand of [stability](/stable-sort/). The algorithm may use only $O(\log n)$ extra words: a few indices for each level of recursion, and no buffer that grows with $n$.

## The algorithm

```pseudo id=main
IN-PLACE-MERGE-SORT(A, lo, hi)                       ▷ sorts A[lo … hi−1]
L1  if hi − lo < 2 then return
L2  mid ← ⌊(lo + hi)/2⌋
L3  IN-PLACE-MERGE-SORT(A, lo, mid)
L4  IN-PLACE-MERGE-SORT(A, mid, hi)
L5  MERGE-IN-PLACE(A, lo, mid, hi)

MERGE-IN-PLACE(A, lo, mid, hi)        ▷ merges sorted A[lo … mid−1] and A[mid … hi−1]
L6  if lo = mid or mid = hi then return
L7  if hi − lo = 2 then exchange A[lo] and A[mid] if A[mid] < A[lo]; return
L8  if mid − lo ≥ hi − mid then
L9      cut1 ← lo + ⌊(mid − lo)/2⌋;  cut2 ← LOWER-BOUND(A, mid, hi, A[cut1])
L10 else
L11     cut2 ← mid + ⌊(hi − mid)/2⌋;  cut1 ← UPPER-BOUND(A, lo, mid, A[cut2])
L12 ROTATE(A, cut1, mid, cut2)
L13 newmid ← cut1 + (cut2 − mid)
L14 MERGE-IN-PLACE(A, lo, cut1, newmid)
L15 MERGE-IN-PLACE(A, newmid, cut2, hi)

ROTATE(A, i, m, j)                    ▷ A[i … m−1], A[m … j−1] become A[m … j−1], A[i … m−1]
L16 if i < m < j then reverse A[i … m−1]; reverse A[m … j−1]; reverse A[i … j−1]

LOWER-BOUND(A, lo, hi, x)             ▷ the first i in [lo, hi] with not A[i] < x
L17 while lo < hi: m ← ⌊(lo + hi)/2⌋; if A[m] < x then lo ← m + 1 else hi ← m
L18 return lo

UPPER-BOUND(A, lo, hi, x)             ▷ the first i in [lo, hi] with x < A[i]
L19 while lo < hi: m ← ⌊(lo + hi)/2⌋; if x < A[m] then hi ← m else lo ← m + 1
L20 return lo
```

The two binary searches differ on purpose. When the cut item comes from the left run (line L9), the items of the right run that are equal to it must stay after it, so the search stops before them. When the cut item comes from the right run (line L11), the items of the left run that are equal to it must stay before it, so the search goes past them. This is what keeps the merge stable. The call is `IN-PLACE-MERGE-SORT(A, 0, n)`.

## Example

Merge the runs $[1, 4, 6, 8]$ and $[2, 3, 5, 7]$, which fill $A[0 \ldots 7]$.

| call (lo, mid, hi) | runs | cut item | cuts | after the rotation | comparisons |
|---|---|---|---|---|---|
| (0, 4, 8) | 1 4 6 8, 2 3 5 7 | 6, from the left | cut1 = 2, cut2 = 7 | 1 4 **2 3 5** **6 8** 7 | 2 |
| (0, 2, 5) | 1 4, 2 3 5 | 3, from the right | cut1 = 1, cut2 = 4 | 1 **2 3** **4** 5 | 2 |
| (0, 1, 2) | 1, 2 | two items | | 1 2 | 1 |
| (2, 3, 4) | 4, 3 | two items | | 3 4 | 1 |
| (2, 4, 5) | 3 4, 5 | 5, from the right | cut1 = 4, cut2 = 5 | no change | 1 |
| (5, 7, 8) | 6 8, 7 | 8, from the left | cut1 = 6, cut2 = 8 | 6 **7** **8** | 1 |
| (5, 6, 7) | 6, 7 | two items | | 6 7 | 1 |

In the first call, the cut item 6 belongs after 2, 3 and 5 of the right run, so the blocks $[6, 8]$ and $[2, 3, 5]$ change places. Then $[1, 4]$ with $[2, 3, 5]$ on the left, and $[6, 8]$ with $[7]$ on the right, are two independent merges. The result is $[1, 2, \ldots, 8]$ after 9 comparisons. A merge into a buffer makes 7 comparisons on this input. Calls with an empty run return at once and are not shown.

## Correctness

The key fact is about one call of MERGE-IN-PLACE with cut item $x$. After the rotation, each item in $A[lo \ldots newmid-1]$ is at most $x$ and each item in $A[newmid \ldots hi-1]$ is at least $x$. Both parts are made of a piece of the left run followed by a piece of the right run, each still sorted, so the two recursive calls get valid inputs. An equal pair of items that ends up split between the two parts is always a left-run item before a right-run item, so stability holds. Each recursive call is on fewer items, so the recursion ends. By induction the merge is correct and stable, and by induction on the length of the range, so is the sort. The full proof is below.

## Complexity

Let a merge have runs of lengths $m \le k$ and total $N = m + k$.

**Depth of the merge recursion.** If the cut item is the middle of the longer run, each of the two sub-merges gets at most half of the longer run plus all of the shorter one, which is at most about $3N/4$ items. So the depth is at most $\log_{4/3} N$, and the stack holds $O(\log N)$ frames.

**Moves.** At one depth of the merge recursion the calls work on disjoint parts of the array, and a rotation of $L$ items makes at most $L$ exchanges. So each depth costs at most $N$ exchanges, and a merge costs $O(N \log N)$. The sort has $\lg n$ levels of merges, each with total size $n$, so it makes $O(n \log^2 n)$ moves and takes $O(n \log^2 n)$ time. Dudziński and Dydek give the sharper bound $O(N \log m)$ for the moves of a merge.

**Comparisons.** A merge makes $O(m \log(k/m + 1))$ comparisons. This is optimal up to a constant factor, by the [merging lower bound](/merging-lower-bound/) $\lg \binom{N}{m}$. In the sort, $m$ and $k$ differ by at most 1, so each merge costs $O(N)$ comparisons and the sort costs $O(n \log n)$. Measured on random keys:

| $n$ | comparisons | per $n \lg n$ | array writes | per $n \lg^2 n$ |
|---|---|---|---|---|
| 1,024 | 12,234 | 1.20 | 39,608 | 0.39 |
| 4,096 | 60,905 | 1.24 | 237,732 | 0.40 |
| 16,384 | 291,474 | 1.27 | 1,342,230 | 0.42 |
| 65,536 | 1,353,256 | 1.29 | 7,162,940 | 0.43 |

Each exchange counts as two writes. Merge sort with a buffer makes about $n \lg n - 1.25n$ comparisons, which is 208,896 for $n = 16{,}384$, and $n \lg n = 229{,}376$ writes into the buffer. On the same $n$, a sorted input costs 89,868 comparisons and no writes, because every cut falls at an end of a run and every rotation is empty. A reversed input costs 81,677 comparisons and 950,286 writes.

**Space.** $O(\log n)$ words for the two recursions together, and nothing else.

## Properties

- **Stable.** Equal items keep their input order, by the choice of LOWER-BOUND and UPPER-BOUND in lines L9 and L11.
- **In place.** It uses $O(\log n)$ words of stack and no buffer. A bottom-up form of the sort removes the outer recursion, but the merge still needs its stack, or an explicit one of the same size. See [in-place algorithm](/in-place-algorithm/).
- **Few comparisons.** It makes $O(n \log n)$ comparisons, like merge sort, so it suits items with an expensive comparison and a cheap move.
- **Not adaptive in its writes.** It makes no writes on a sorted input, but the comparisons stay $\Theta(n \log n)$. A check before each merge, given below, makes the sorted case linear.

## Variants and improvements

- **Skip merges that are not needed.** Before line L8, return if not $A[mid] < A[mid-1]$. Then the runs are already in order, and a sorted input costs $n - 1$ comparisons.
- **SymMerge.** Kim and Kutzner choose the cuts symmetrically around the middle of the whole range, with one binary search that compares items from both runs. It has the same bounds and fewer special cases. Go's `sort.Stable` sorts blocks of 20 items with [insertion sort](/insertion-sort/) and then merges them with SymMerge, and its documentation states $O(n \log n)$ comparisons and $O(n \log^2 n)$ swaps.
- **Insertion merge.** The simplest in-place merge moves each item of the right run into the left run one place at a time, as [insertion sort](/insertion-sort/) does. It is stable, but it takes $\Theta(N^2)$ time in the worst case.
- **Unstable, $O(n \log n)$ time.** Katajainen, Pasanen and Teuhola use one part of the array as the buffer for merging the other part, by exchanges instead of copies, and get an unstable in-place merge sort with $n \lg n + O(n)$ comparisons and $O(n \log n)$ moves.
- **Stable, $O(n \log n)$ time.** Merges that split the runs into blocks of about $\sqrt{N}$ items and use some of them as an internal buffer, after Kronrod, are stable, in place and linear. Sorts built on them, such as WikiSort and GrailSort, are on the [block sort](/block-sort/) page.
- **With a small buffer.** When some memory is available, merge into it directly, and fall back to rotations only for the parts that do not fit. C++ `std::stable_sort` and `std::inplace_merge` work this way.

## When to use it

Use it when the sort must be stable, no buffer of size $\Theta(n)$ can be allocated, and $n$ is moderate: embedded code, a library fall-back when memory allocation fails, or a generic sort that only has a swap operation on the data, as in Go. If stability is not needed, [heapsort](/heapsort/) or an introsort is faster and truly in place. If a buffer is available, merge sort or [Timsort](/timsort/) is faster by a factor of about $\log n$ in moves. For large $n$ with no buffer and a need for stability, use a [block sort](/block-sort/).

## Pitfalls

- **The same search on both sides.** Using LOWER-BOUND in both lines L9 and L11, or UPPER-BOUND in both, breaks stability on equal keys, although the output is still sorted.
- **No base case for two items.** Without line L7, a call with one item in each run that are already in order gets cut1 = lo and cut2 = mid, the rotation is empty, and the second recursive call is the same call again, forever.
- **Rotating with a temporary copy.** Rotating by copying the shorter block to a temporary array brings back the buffer that the method is meant to avoid. Use three reversals or the juggling rotation of [vector rotation](/vector-rotation/).
- **Counting the stack as $O(1)$.** The merge recursion has depth $\Theta(\log n)$. That is usually accepted as in place, but it is not $O(1)$ extra space.

## Implementations

## History

Merging in place is an old problem. Kronrod showed in 1969 that two sorted runs can be merged in linear time with $O(1)$ extra space, with a method that splits the input into blocks of about $\sqrt{n}$ items, but the method was not stable and was hard to use. Dudziński and Dydek (1981) gave the simple stable merge on this page, by binary search and rotation, with $O(m \log(n/m + 1))$ comparisons. Kim and Kutzner (2004) gave SymMerge, a symmetric form of the same idea. Katajainen, Pasanen and Teuhola (1996) gave a practical in-place merge sort that is not stable. Library sorts adopted the rotation merge as the stable fall-back with no memory, as in libstdc++, and as the main method in Go's `sort.Stable`.

## References
