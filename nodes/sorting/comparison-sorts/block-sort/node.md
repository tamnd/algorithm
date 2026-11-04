---
tag: 0XYD20
kind: algorithm
slug: block-sort
name: Block sort
aliases:
- WikiSort
- GrailSort
- in-place stable merge via block rotation
area: sorting/comparison-sorts
level: research
summary: Stable in-place sort that merges by rotating blocks, achieving O(n log n) comparisons with O(1) extra memory.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: O(n log² n), average: Θ(n log n), best: Θ(n), comparisons: O(n log n)}
  space: {extra: O(1)}
properties: {stable: true, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 1969
  people: [M. A. Kronrod, Luis Trabb Pardo, Bing-Chao Huang, Michael A. Langston, Pok-Son Kim, Arne Kutzner]
  note: Kronrod merged in place in linear time with blocks of about √n items and an internal buffer; Pardo made the method stable in 1977; Huang and Langston and later Kim and Kutzner made it practical, and WikiSort and GrailSort are programs built on these ideas.
prereqs: [in-place-merge-sort, merge-sort, stable-sort, vector-rotation, selection-sort, binary-search]
see_also: [in-place-merge-sort, timsort, heapsort, in-place-algorithm, merging-sorted-sequences, merging-lower-bound, java-system-sort, smoothsort]
sources:
  - paper: "M. A. Kronrod, Optimal ordering algorithm without operational field, Soviet Mathematics Doklady 10, 1969"
    locator: pp. 744 to 746 (merging in linear time with O(1) extra space, using √n blocks and an internal buffer)
  - paper: "Luis Trabb Pardo, Stable sorting and merging with optimal space and time bounds, SIAM Journal on Computing 6(2), 1977"
    locator: pp. 351 to 372 (the first stable merge in linear time and constant extra space)
  - paper: "Bing-Chao Huang and Michael A. Langston, Fast stable merging and sorting in constant extra space, The Computer Journal 35(6), 1992"
    locator: pp. 643 to 650 (a practical stable block merge with an internal buffer of distinct keys)
  - paper: "Pok-Son Kim and Arne Kutzner, Ratio based stable in-place merging, TAMC 2008, LNCS 4978"
    locator: pp. 246 to 257 (the block merge on which WikiSort is based)
---

Block sort is a stable merge sort that needs only $O(1)$ extra words. Its merge borrows space from the input: it takes about $3\sqrt{m}$ items with distinct keys from the left run, of length $m$, and uses them as an internal buffer. It cuts the rest of both runs into blocks of about $\sqrt{m}$ items, puts the blocks in order of their first items, and then merges neighbouring blocks with the buffer as swap space. At the end it sorts the buffer and puts its items back. When the buffer can be found, each merge takes $O(m)$ time, so the sort takes $O(n \log n)$ time, like merge sort with a second array. WikiSort and GrailSort are well-known programs of this kind. The version on this page falls back to the simpler [in-place merge](/in-place-merge-sort/) by rotations when a run has too few distinct keys.

## In plain words

Merging two sorted rows usually needs an empty row to write into. Block sort makes its own empty space. It takes a few dozen items with different values out of the first row and parks them at the front. Their order no longer matters while they are parked, so they can serve as scratch space.

Then it cuts both rows into short blocks of equal length and puts the blocks in order of their first items. After that, each item is already close to its final place. A short merge between neighbouring blocks, using the scratch space to swap items in and out, finishes the job.

At the end it sorts the parked items, which is cheap because there are few of them, and slides each one back into its place. Nothing is copied to a second array, and equal items keep their order.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order, which the algorithm can only compare with $<$. The output is the same array in non-decreasing order, with items of equal keys in their input order. This is the [sorting problem](/sorting-problem/) with [stability](/stable-sort/). The algorithm may use only $O(1)$ extra words: a fixed number of indices and one held item, and no recursion that grows with $n$. Items may only be exchanged in the array.

## The algorithm

```pseudo id=main
BLOCK-SORT(A)
L1  sort each run A[16i … 16i + 15] by insertion sort
L2  for w ← 16, 32, 64, … while w < n do
L3      for each pair of neighbouring runs A[lo … mid−1], A[mid … hi−1] with mid = lo + w
L4          if A[mid] < A[mid − 1] then BLOCK-MERGE(A, lo, mid, hi)

BLOCK-MERGE(A, lo, mid, hi)                     ▷ m = mid − lo ≥ hi − mid
L5  if m < 64 then merge by rotations, as in in-place merge sort; return
L6  s ← ⌈√m⌉; k ← 3s
L7  move the first copy of each of the k smallest distinct values of A[lo … mid−1] to A[lo … lo+k−1]
L8  if fewer than k exist then merge the rest by rotations, put the buffer back (line L17's second step); return
L9  tags T ← A[lo … lo+2s−1]; swap buffer S ← A[lo+2s … lo+3s−1]
L10 cut the rest of the left run into a short run R of fewer than s items, then A-blocks of s items;
    cut the right run into B-blocks of s items, then a short tail W
L11 selection-sort the A-blocks and B-blocks by (first item, tag), exchanging the tags with the blocks
L12 rotate W to just before the trailing A-blocks whose first item is greater than W's first item
L13 F ← R, marked as from A; S lies just before F
L14 for each block Z in order: if Z comes from the same run as F then move F before S, and F ← Z
L15     else merge F and Z into the space that starts at S, until one of them is used up; F ← the rest of the other
L16 move F before S; rotate S to just after T
L17 insertion-sort the k buffer items; then, from the smallest, put each one before the first item that is not smaller
```

**The buffer.** The left run is sorted, so its distinct values can be found in one scan. Line L7 rolls a growing block of the first copies to the right through the run with rotations, and then rotates it to the front. Each buffer item is the first copy of its value in the left run, so in the output it belongs before every other item with the same key. Line L17 puts it there with LOWER-BOUND, which keeps the sort stable.

**Tags.** The block sort of line L11 must know, for two blocks with equal first items, which came first. The tags tell this. Tag $j$ starts beside block $j$, in the original order with all A-blocks first, and moves with its block. The tags have distinct values, so comparing tags is a strict tie-break, and the value $\tau$ of the first B-block's tag tells the origin of a block: it is an A-block exactly when its tag is less than $\tau$. The algorithm holds $\tau$ in one variable.

**The local merge.** The swap space $S$ of $s$ items sits just before $F$. Line L15 writes the smaller head of $F$ or $Z$ to the first item of $S$ by an exchange, and moves on. The items of $S$ move to the right, mixed but intact, into the places that the merge frees. Ties go to the item from the left run. When $F$ is used up, $S$ is again one block, followed by the rest of $Z$. When $Z$ is used up first, the rest of $F$ is moved to the right end by exchanges, past the pieces of $S$. $Z$ has at most $s$ items, so the output never overtakes the unread items.

## Example

To show the block phase on a small case, ignore the cut-off $m < 64$ of line L5. Merge the left run $[0, 1, \ldots, 17, 20, 22, 24, 26, 28, 30, 41, 43, 45, 47, 49, 51]$, with $m = 30$, and the right run $[5, 10, 15, 19, 21, 23, 25, 27, 29, 31, 33, 35, 36, 37, 38, 39, 39, 40, 40, 40, 42, 44]$ of 22 items.

**Buffer.** $s = \lceil \sqrt{30} \rceil = 6$ and $k = 18$. The 18 smallest distinct values of the left run are $0, \ldots, 17$, already at the front. The tags are $0, \ldots, 11$ and the swap space is $12, \ldots, 17$.

**Blocks.** The rest of the left run has 12 items, so $R$ is empty, and there are two A-blocks, $A_1 = [20, 22, 24, 26, 28, 30]$ and $A_2 = [41, 43, \ldots, 51]$. The right run gives $B_1 = [5, \ldots, 23]$, $B_2 = [25, \ldots, 35]$, $B_3 = [36, 37, 38, 39, 39, 40]$ and the tail $W = [40, 40, 42, 44]$. By first items 5, 20, 25, 36, 41 the order is $B_1, A_1, B_2, B_3, A_2$. The first item of $W$ is 40, less than 41, so $W$ goes before $A_2$.

**Local merges.**

| $F$, from | next block $Z$ | action | items now final | new $F$, from |
|---|---|---|---|---|
| empty, A | $B_1$ | merge: $F$ is used up at once | none | $B_1$, B |
| $B_1$, B | $A_1 = [20, \ldots, 30]$ | merge until $B_1$ is used up | 5 10 15 19 20 21 22 23 | $[24, 26, 28, 30]$, A |
| $[24, 26, 28, 30]$, A | $B_2 = [25, \ldots, 35]$ | merge until $F$ is used up | 24 25 26 27 28 29 30 | $[31, 33, 35]$, B |
| $[31, 33, 35]$, B | $B_3$ | same run: $F$ is final | 31 33 35 | $B_3$, B |
| $B_3$, B | $W$ | same run: $F$ is final | 36 37 38 39 39 40 | $W$, B |
| $W = [40, 40, 42, 44]$, B | $A_2 = [41, \ldots, 51]$ | merge until $W$ is used up | 40 40 41 42 43 44 | $[45, \ldots, 51]$, A |

After line L16 the last $F$ is final too. Line L17 sorts the 18 buffer items and moves them back. Each of $0, \ldots, 17$ goes before the first item that is not smaller, and the result is the stable merge of the two runs. No local merge handled more than 12 items.

## Correctness

Three facts carry the proof. First, after line L11 the blocks of each run appear in their original order, because ties are broken by the tags, and every block comes no earlier than any block with a smaller first item. Second, each step of lines L14 and L15 makes final only items that are no larger than any item still to come: an item from one run is bounded by the next unread item of its own run, and the order of the first items bounds the other run. Third, each buffer item is the first copy of its value in the left run, so placing it before every equal item restores the stable order. The full proof is below.

## Complexity

Let a buffered merge have runs of lengths $m \ge m'$ and $N = m + m'$.

**One merge is $O(N)$.** Line L7 rolls a block of at most $k$ items through the run. Each rotation costs the size of the block plus the gap it crosses, so the total is $O(m + k^2) = O(m)$. There are $t \le N/s \le 2s$ blocks, so the selection sort of line L11 makes $O(t^2) = O(m)$ comparisons and $t$ exchanges of blocks, which move $O(ts) = O(N)$ items. Line L12 is one rotation. In lines L13 to L15, $F$ always has at most $s$ items and $Z$ at most $s$, and each step costs $O(|F| + |Z|)$, which sums to $O(N)$. The last line sorts $k = 3s$ items by insertion in $O(s^2) = O(m)$, and puts them back with $k$ rotations whose cost sums to $O(N + k^2)$.

**The sort.** Lines L1 to L4 make $\lceil \lg(n/16) \rceil$ levels, each with merges of total size at most $n$. When every merge finds its buffer, the time is $O(n \log n)$. A merge that falls back to rotations at line L8 costs $O(N \log N)$ moves, so the worst case of this version is $O(n \log^2 n)$, on inputs with fewer than about $3\sqrt{m}$ distinct keys. The comparisons stay $O(n \log n)$ in all cases. A sorted input costs $n - 1$ comparisons when $n$ is a multiple of 16: 15 in each run of line L1, and one test of line L4 for each pair of runs.

Measured on random keys, with $n = 2^{18}$, the cost per item of one level of buffered merges is close to constant:

| run length $m$ | comparisons per item | array writes per item |
|---|---|---|
| 64 | 3.81 | 7.88 |
| 1,024 | 3.64 | 8.44 |
| 16,384 | 3.48 | 8.53 |
| 131,072 | 3.41 | 8.60 |

Each exchange counts as two writes. For the whole sort:

| input, $n$ | comparisons | array writes |
|---|---|---|
| random, $2^{10}$ | 22,510 | 46,231 |
| random, $2^{14}$ | 594,243 | 1,309,396 |
| random, $2^{16}$ | 2,830,088 | 6,359,286 |
| sorted, $2^{14}$ | 16,383 | 15,360 |
| reversed, $2^{14}$ | 540,633 | 1,327,158 |
| 10 distinct values, $2^{14}$ | 262,628 | 1,413,299 |

So block sort makes about 3.5 comparisons and 8.5 writes per item and level, where merge sort with a buffer makes at most 1 comparison and 1 write. The rotation merge of [in-place merge sort](/in-place-merge-sort/) makes 1,342,230 writes at $n = 2^{14}$, about the same, but its writes per level grow like $\log n$, while those of block sort do not.

**Space.** A fixed number of indices, the value $\tau$, and no recursion except in the fall-back, whose depth is $O(\log n)$. The production versions avoid this recursion too.

## Properties

- **Stable.** Ties are broken toward the left run in every local merge, the blocks of each run keep their order, and buffer items go back before their equals.
- **In place.** It uses $O(1)$ extra words, with the buffer taken from the input. See [in-place algorithm](/in-place-algorithm/).
- **Linear merges.** With a buffer, each merge of $N$ items takes $O(N)$ time, which matches merge sort with a second array up to a constant factor.
- **Adaptive only to sorted runs.** Line L4 skips merges of runs that are already in order, so a sorted input takes linear time. Other kinds of presortedness do not help.

## Variants and improvements

- **WikiSort.** McFadden's WikiSort follows Kim and Kutzner. It extracts two buffers once per level of the bottom-up sort, not once per merge, moves the A-blocks through the B-blocks by rolling them instead of a full selection sort, and has a separate path with no buffer for runs with few distinct keys. It reaches $O(n \log n)$ time in the worst case. It can also use a small fixed cache, for example 512 items, to speed up the merges.
- **GrailSort.** Astrelin's GrailSort collects about $2\sqrt{n}$ distinct keys once for the whole sort, uses them as tags and swap space for every level, and has special code when there are fewer. It reaches $O(n \log n)$ worst-case time and is stable.
- **Few distinct keys.** When a run has fewer distinct keys than the buffer needs, the production versions do not fall back to the rotation merge of this page. They use the keys they found as tags only, or merge with a smaller buffer, and keep $O(n \log n)$ time.
- **Theory.** Kronrod's merge (1969) is linear and in place but not stable. Pardo (1977) gave the first stable merge in linear time and constant space. Later work, such as Symvonis (1995) and Kim and Kutzner (2008), reduced the number of comparisons and moves to within constant factors of the optimum for runs of unequal lengths.

## When to use it

Use it when the sort must be stable, the array is large, and there is no memory for a buffer of $n$ items or even $\sqrt{n}$ items: embedded systems, kernels, or sorts of huge arrays close to the memory limit. If a buffer of $n/2$ items is available, ordinary merge sort or [Timsort](/timsort/) is simpler and faster. If stability is not needed, [heapsort](/heapsort/) or an introsort is simpler and faster.

## Pitfalls

- **Buffer items that are not distinct.** If two buffer items have equal keys, the local merges mix them, and the tags may compare as equal, so the original order is lost. Line L7 must take only the first copy of each value.
- **Putting the buffer back with the wrong search.** A buffer item is the first copy of its key in the left run, so it must go before every equal item, with LOWER-BOUND. Using UPPER-BOUND puts it after the other copies and breaks stability.
- **Comparing by the first item only.** Selection sort of the blocks by their first items alone is not stable on ties. An A-block and a B-block with equal first items must keep the A-block first, which the tags ensure.
- **Forgetting the tail.** The short tail $W$ of the right run must take its place among the blocks, as in line L12. Leaving it at the end lets an A-block be declared final although $W$ holds a smaller item.
- **A local merge that overruns.** The output overtakes the unread items if $Z$ has more items than the swap space. Every block, including $W$, must have at most $s$ items.

## Implementations

## History

Kronrod (1969) showed how to merge two sorted runs in linear time with constant extra space. He cut the input into blocks of about $\sqrt{n}$ items, used one block as an internal buffer, and sorted the blocks by their first items. The merge was not stable. Pardo (1977) made the method stable and used it for a stable sort in $O(n \log n)$ time and constant extra space, which showed that stable, in-place and optimal time can be had together. These methods were complex. Huang and Langston (1988 and 1992) gave simpler and faster versions, with a buffer of distinct keys. Symvonis (1995) and Kim and Kutzner (2004 and 2008) reduced the constants and handled runs of very different lengths. WikiSort (Mike McFadden, 2014) and GrailSort (Andrey Astrelin, 2013) are public programs built on these ideas, and they are the usual reference implementations of block merge sort.

## References
