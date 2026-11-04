---
tag: FAY1AX
kind: algorithm
slug: cycle-sort
name: Cycle sort
area: sorting/comparison-sorts
level: advanced
summary: In-place sort that writes each element to its final position exactly once, minimizing the number of writes.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n²), average: Θ(n²), best: Θ(n²)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 1990
  people: [Bruce K. Haddon]
  note: Haddon described the method in The Computer Journal, starting from the decomposition of a permutation into disjoint cycles.
prereqs: [permutation-cycles, selection-sort, in-place-algorithm]
see_also: [permutation-cycle-decomposition, cycle-leader-permutation, in-place-permutation, selection-sort, index-sort, counting-sort, comparison-cost-model]
sources:
  - paper: "Bruce K. Haddon, Cycle-sort: a linear sorting method, The Computer Journal 33(4), 1990"
    locator: pp. 365 to 367 (the cycle-following sort with the least number of writes, and its linear-time form for keys that give their own positions)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.3.3, Applications to permutations (the cycle form of a permutation)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2 introduction (rearranging records in place by following the cycles of a permutation) and Section 5.2.3 (straight selection and its number of moves)
---

Cycle sort sorts an array in place with the least possible number of writes to the array. For each position $s$ from the left, it takes the item $x$ there, finds the final place of $x$ by counting the items to its right that are smaller, puts $x$ there, and continues with the item it displaced, until an item lands back at $s$. This follows one cycle of the permutation that sorts the array. Each write puts an item in its final place, so a position whose item is already correct is never written, and each other position is written exactly once. The price is $\Theta(n^2)$ comparisons on every input, so the method is useful only when writes are much more expensive than comparisons, as on flash memory or EEPROM.

## In plain words

Look at the first card. Count how many of the cards to its right are smaller. If 3 cards are smaller, this card belongs in place 3, so put it there, and pick up the card that was in place 3.

Do the same with the card in your hand: count, put it in its place, and pick up the card that was there. Sooner or later the card in your hand belongs in the first place. Put it there. Now the first place is correct, and so is each place you visited.

Move to the next place and do the same. A card that is already in its correct place is never moved. Each other card is moved once, straight to where it belongs. The counting is the slow part: each count looks at all the cards to the right.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order, which the algorithm can only compare with $<$. The output is the same array with its items in non-decreasing order. This is the [sorting problem](/sorting-problem/). Besides the comparisons, the cost that matters here is the number of **writes** to the array. The held item $x$ is in a register and is not part of the array.

## The algorithm

```pseudo id=main
CYCLE-SORT(A)
L1  writes ← 0
L2  for s ← 0 to n − 2 do
L3      x ← A[s]
L4      p ← POSITION(A, s, x)
L5      if p = s then continue with the next s     ▷ x is in its place
L6      loop
L7          while x = A[p] do p ← p + 1             ▷ skip equal items in their places
L8          exchange x and A[p]                     ▷ one write to the array
L9          writes ← writes + 1
L10         if p = s then exit the loop             ▷ the cycle is closed
L11         p ← POSITION(A, s, x)
L12 return writes

POSITION(A, s, x)
L13 p ← s
L14 for i ← s + 1 to n − 1 do
L15     if A[i] < x then p ← p + 1
L16 return p
```

The positions $0, \ldots, s-1$ hold the $s$ smallest items in their final places, so the final place of $x$ is $s$ plus the number of items in $A[s+1 \ldots n-1]$ that are smaller than $x$. While a cycle is open, $A[s]$ still holds a stale copy of the first item, and POSITION does not look at it. The test $x = A[p]$ of line L7 is done with two comparisons: $x = y$ when neither $x < y$ nor $y < x$. It moves $x$ past copies of itself that are already in their places, so equal keys do not cause an endless loop.

## Example

Sort $A = [3, 0, 4, 1, 2]$. The permutation that sorts it has the cycles $(0\ 3\ 1)$ and $(2\ 4)$.

| $s$ | held item $x$ | items to the right of $s$ smaller than $x$ | write at | array after the write | new held item |
|---|---|---|---|---|---|
| 0 | 3 | 0, 1, 2 | 3 | 3 0 4 **3** 2 | 1 |
| 0 | 1 | 0 | 1 | 3 **1** 4 3 2 | 0 |
| 0 | 0 | none | 0 | **0** 1 4 3 2 | 3 (stale copy, dropped) |
| 1 | 1 | none | (stays) | 0 1 4 3 2 | |
| 2 | 4 | 3, 2 | 4 | 0 1 4 3 **4** | 2 |
| 2 | 2 | none | 2 | 0 1 **2** 3 4 | 4 (stale copy, dropped) |
| 3 | 3 | none | (stays) | 0 1 2 3 4 | |

There are 5 writes, one for each item that was out of place, and 28 comparisons. [Selection sort](/selection-sort/) on the same array makes 3 exchanges, which are 6 writes, and 10 comparisons.

With equal keys, $A = [2, 4, 1, 2, 0, 4]$ gives one cycle at $s = 0$ with 4 writes: 2 goes to position 2, 1 to position 1, 4 to position 4, and 0 to position 0. Positions 3 and 5 already hold their final values 2 and 4, and they are never written.

## Correctness

Let $M_s$ be the multiset of the items that belong in positions $s, \ldots, n-1$ of the sorted output. During the work for $s$, the items of $A[s+1 \ldots n-1]$ together with the held item $x$ are exactly $M_s$, while $A[s]$ is a hole that holds a stale copy. Each item of $M_s$ that is smaller than $x$ is in $A[s+1 \ldots n-1]$, so POSITION returns the first place of the block of $x$ in the sorted order of $M_s$. That block has one more place than there are copies of $x$ in the array, so line L7 stops at a place of the block that does not yet hold $x$, and the write of line L8 makes that place final without moving a final item. A place in $A[s+1 \ldots n-1]$ can become final only $n - 1 - s$ times, so the cycle closes, and it closes with the smallest item of $M_s$ at place $s$. By induction on $s$, the array is sorted at the end. The full proof is below.

## Complexity

**Writes.** Each write puts an item at a place where the sorted output has that item, and it never writes a place that already holds its final item. So the number of writes is exactly the number of places $i$ where $A[i]$ differs from the $i$-th item of the sorted output. For $n$ distinct keys this is $n$ minus the number of fixed points of the sorting permutation. No algorithm can do with fewer, because each such place must be written at least once. On a uniformly random permutation the expected number of fixed points is 1, so the expected number of writes is $n - 1$. Selection sort writes up to $2(n-1)$ times, and insertion sort $\Theta(n^2)$ times on average.

**Comparisons.** Each call of POSITION for start $s$ makes $n - 1 - s$ comparisons. Each start calls it once at line L4, and once more for each write of its cycle except the last. Line L7 adds 1 or 2 comparisons for each item it tests. So the count is at least $\sum_{s=0}^{n-2} (n - 1 - s) = n(n-1)/2$ on every input, and for distinct keys at most about $3n^2/2$, which is reached when one cycle of length $n$ starts at $s = 0$. With $n = 1000$:

| input | writes | comparisons |
|---|---|---|
| sorted | 0 | 499,500 |
| uniform random permutation | 998 | 1,492,097 |
| $1, 2, \ldots, 999, 0$ (one cycle of length $n$) | 1,000 | 1,498,502 |
| random keys from $\{0, \ldots, 9\}$ | 905 | 1,379,413 |

**Time and space.** $\Theta(n^2)$ time in every case, and $\Theta(1)$ extra space: the held item and a few indices.

## Properties

- **Least number of writes.** Among all sorts that work in the array, it writes the fewest times, on every input.
- **In place.** It uses $O(1)$ extra words. See [in-place algorithm](/in-place-algorithm/).
- **Not stable.** The array $[1_a, 1_b, 0]$ becomes $[0, 1_b, 1_a]$: $1_a$ skips past $1_b$ in line L7.
- **Not adaptive.** It makes at least $n(n-1)/2$ comparisons even on a sorted array.
- **Comparison-based and deterministic.** It looks at the keys only through $<$.

## Variants and improvements

- **Keys that give their positions.** If the array holds a permutation of $0, \ldots, n-1$, the final place of $x$ is $x$ itself, and no counting is needed. Following the cycles then sorts in $O(n)$ time with the same least number of writes. This is the linear form in Haddon's paper, and it is the core of [in-place permutation](/in-place-permutation/) and of [cycle leader](/cycle-leader-permutation/) algorithms.
- **Small key ranges.** With keys from a small range, a table of counts as in [counting sort](/counting-sort/) gives the first place of each key's block in $O(n + k)$ time. Following the cycles with a pointer for each key then gives an in-place, write-optimal sort in $O(n + k)$ time, at the cost of $O(k)$ extra words.
- **Sort indices first.** Sort an array of indices with a fast comparison sort, as in [index sort](/index-sort/), then apply the permutation to the records by its cycles. This uses $O(n \log n)$ comparisons and $n + O(n)$ extra words, and it moves each record at most once plus once per cycle.

## When to use it

Use it when each write to the array is very expensive compared with a comparison and memory for a second array is not available: for example, small arrays on EEPROM or flash memory with a limited number of write cycles. For a large $n$ the $\Theta(n^2)$ comparisons make it too slow, and an index sort followed by a cycle-following permutation is better. When writes are cheap, use [insertion sort](/insertion-sort/) for small arrays and an $O(n \log n)$ sort for large ones.

## Pitfalls

- **Forgetting the equal-key skip.** Without line L7, an item whose final block already holds a copy of it is written over that copy, and the copy is then placed again at the same spot, forever. On $[1, 1, 0]$ the loop never ends.
- **Counting over the wrong range.** POSITION must count only $A[s+1 \ldots n-1]$. Counting from $0$ adds the $s$ final items, and counting $A[s]$ counts the stale copy.
- **Counting writes wrong.** The first item of a cycle is taken into the register and is not written back at $s$. A version that writes $x$ back to $A[s]$ before the cycle starts does one extra write per cycle and loses the optimal count.
- **Running the outer loop to $n - 1$.** When $s = n - 1$ is reached, the last item is already in place, so the loop stops at $n - 2$. Going on is harmless, but it is one more useless POSITION call.

## Implementations

## History

Haddon (1990) described cycle sort in The Computer Journal. He started from the fact that each permutation is a product of disjoint cycles, which Knuth covers in Section 1.3.3 of Volume 1, and from the classic way to apply a permutation in place by following its cycles. His title calls the method linear because, when the keys give their own final positions, it sorts in linear time. For general keys, a count of the smaller items replaces the position, and the time becomes quadratic, while the number of writes stays the least possible.

## References
