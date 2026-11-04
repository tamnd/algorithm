---
tag: 8TNZV0
kind: algorithm
slug: heap-delete
name: Heap delete
aliases:
- HEAP-DELETE
area: data-structures/heaps
level: intro
summary: A heap operation that removes an arbitrary element by replacing it with the last element and then restoring the heap property.
model: comparison-model
complexity:
  vars: {n: the number of keys in the heap}
  time: {worst: Θ(log n), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {in_place: true, deterministic: true, comparison: true, recursive: false}
prereqs: [binary-heap, heap-property, sift-up, sift-down]
see_also: [heap-extract-max, heap-increase-key, decrease-key, indexed-priority-queue, lazy-deletion, priority-queue, binary-heap, sift-down]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 6.5 (Priority queues), the exercise on MAX-HEAP-DELETE and the procedures MAX-HEAPIFY and MAX-HEAP-INCREASE-KEY that it uses
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 6.5, the exercise on HEAP-DELETE(A, i)
  - book: isbn:9783540779773
    title: Kurt Mehlhorn and Peter Sanders, Algorithms and Data Structures, The Basic Toolbox
    locator: Section 6.2 (Addressable priority queues), remove in a binary heap
---

Heap delete removes the key at any index $i$ of a binary max-heap in an array. It moves the last key into the cell $i$, shrinks the heap by one, and then moves the new key either up, if it is larger than its parent, or down, if it is smaller than a child. It runs in $O(\log n)$ time and $O(1)$ extra space. It is the delete operation of an [indexed priority queue](/indexed-priority-queue/), where the caller removes an item by its name, and [heap extract-max](/heap-extract-max/) is the case $i = 1$. The common bug is to sift down only: the last key can be larger than the parent of $i$, and then it must go up.

## In plain words

You want to take out one number from the middle of the heap. The heap must stay a full tree with no gaps, and the only cell you can drop without a gap is the last one. So move the last number into the place of the one you remove.

The moved number came from another branch of the tree, so it may be too large or too small for its new place. If it is larger than the number above it, move it up, swapping with the number above. Else move it down, swapping with the larger number below, as long as one is larger. Only one of the two moves can be needed.

## The problem

Input: a max-heap $A[1 \ldots n]$, so $A[\lfloor j/2 \rfloor] \ge A[j]$ for each $2 \le j \le n$, and an index $1 \le i \le n$. Output: the key $A[i]$, and a max-heap $A[1 \ldots n - 1]$ whose multiset of keys is the old one with one copy of that key removed. An index out of range is an error.

## The algorithm

```pseudo id=main
HEAP-DELETE(A, i)                          ▷ A[1 .. A.heap-size] is a max-heap
L1  if i < 1 or i > A.heap-size then error "index out of range"
L2  x ← A[i]
L3  A[i] ← A[A.heap-size]
L4  A.heap-size ← A.heap-size − 1
L5  if i ≤ A.heap-size then                ▷ else the removed cell was the last one
L6      if i > 1 and A[⌊i/2⌋] < A[i] then SIFT-UP(A, i)
L7      else MAX-HEAPIFY(A, i)
L8  return x

SIFT-UP(A, i)
L9  while i > 1 and A[⌊i/2⌋] < A[i] do
L10     swap A[i] and A[⌊i/2⌋]
L11     i ← ⌊i/2⌋

MAX-HEAPIFY(A, i)
L12 while true do
L13     l ← 2i, r ← 2i + 1, m ← i
L14     if l ≤ A.heap-size and A[l] > A[m] then m ← l
L15     if r ≤ A.heap-size and A[r] > A[m] then m ← r
L16     if m = i then return
L17     swap A[i] and A[m], i ← m
```

Lines L2 to L4 save the key, fill the hole with the last key $y$, and drop the last cell. If $i$ was the last cell, nothing else is needed. Else the edges between other cells are unchanged, and only the edges at $i$ can fail. Line L6 tests the edge to the parent. If it fails, $y$ is larger than the parent of $i$, and so larger than each child of $i$, which were at most that parent; then SIFT-UP alone repairs the heap. Else $y$ fits under its parent, and MAX-HEAPIFY repairs the edges to the children.

**By increase and extract.** The same result comes from HEAP-INCREASE-KEY$(A, i, +\infty)$ followed by [HEAP-EXTRACT-MAX](/heap-extract-max/). That needs a key $+\infty$ and does two passes, so the direct method above is shorter.

## Example

**A key that goes down.** Take $A = [16, 14, 10, 8, 7, 9, 3, 2, 4, 1]$ and delete $i = 2$, the key 14.

| step | what happens | array |
|---|---|---|
| L2 to L4 | $x = 14$; the last key 1 goes to cell 2 | [16, 1, 10, 8, 7, 9, 3, 2, 4] |
| L6 | the parent 16 is not smaller than 1, so sift down | |
| L12 to L17, $i = 2$ | children 8 and 7; swap with 8 | [16, 8, 10, 1, 7, 9, 3, 2, 4] |
| $i = 4$ | children 2 and 4; swap with 4 | [16, 8, 10, 4, 7, 9, 3, 2, 1] |

**A key that goes up.** Take $A = [100, 50, 90, 40, 45, 80, 85]$ and delete $i = 4$, the key 40. The last key 85 comes from the right subtree of the root.

| step | what happens | array |
|---|---|---|
| L2 to L4 | $x = 40$; 85 goes to cell 4 | [100, 50, 90, 85, 45, 80] |
| L6 | the parent $A[2] = 50 < 85$, so sift up | |
| L9 to L11, $i = 4$ | swap with 50 | [100, 85, 90, 50, 45, 80] |
| $i = 2$ | the parent 100 is not smaller, stop | [100, 85, 90, 50, 45, 80] |

A sift-down alone would leave $[100, 50, 90, 85, 45, 80]$, where 85 sits under 50, which is not a max-heap.

## Correctness

After line L4, every edge holds except perhaps the edges with an end at $i$. If the edge from the parent of $i$ fails, then $y$ is larger than the parent, and the children of $i$ were at most the parent, so the edges out of $i$ hold, and the sift-up lemma applies. If the edge to the parent holds, the parent is at least $y$, and it was at least each child of $i$, so the sift-down lemma applies. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Lines L1 to L6 cost $O(1)$. SIFT-UP from $i$ does at most $\lfloor \lg i \rfloor$ swaps, and MAX-HEAPIFY from $i$ does at most $\lfloor \lg((n - 1)/i) \rfloor$ swaps with 2 comparisons each. Only one of them runs. So the cost is $O(\log n)$.

**Worst case.** Deleting the root of the heap $[n, n - 1, \ldots, 1]$ moves the key 1 to the root, and it goes down to a leaf, so $\Theta(\log n)$. Deleting a leaf near the start of the bottom level, when the last key is larger than all keys on the path to the root, sends the key up to the root, also $\Theta(\log n)$.

**Best case.** Deleting the last cell, $i = n$, costs $\Theta(1)$.

**Space.** $\Theta(1)$ extra cells.

## Properties

- In place, with $O(1)$ extra space.
- Comparison-based.
- It changes the cells on one path through $i$: the path from $i$ up to the root, or a path from $i$ down to a leaf.
- It needs the index of the key. Finding the index of a key by search costs $\Theta(n)$, because the heap order does not guide a search.

## Variants and improvements

- **Min-heap.** Reverse each comparison: sift up if the moved key is smaller than its parent, else sift down.
- **With a position map.** In an [indexed priority queue](/indexed-priority-queue/), the caller gives an item name, a map gives its index, and each swap and the move of line L3 update the map.
- **Lazy deletion.** Mark the item as deleted and skip it when it reaches the root. This avoids the index, but the heap keeps dead entries, see [lazy deletion](/lazy-deletion/).
- **Other heaps.** In a [binomial heap](/binomial-heap/) or a [Fibonacci heap](/fibonacci-heap/), delete is DECREASE-KEY to $-\infty$ followed by EXTRACT-MIN.

## When to use it

Use it when items must leave a priority queue before they reach the top: a cancelled timer in an event queue, a job that is withdrawn from a scheduler, or a vertex that is removed from a search frontier. The caller must know the index, so it is used with a position map or with handles.

## Pitfalls

- **Sift-down only.** The moved key comes from the last cell, which can be in another subtree and larger than the parent of $i$. The second example shows a heap that breaks if line L6 is left out.
- **Deleting the last cell.** When $i = n$, the cell $i$ is gone after line L4, so line L5 must skip the repair. Else the code reads a cell beyond the heap.
- **Using the old size.** MAX-HEAPIFY must use the new size; the old last cell still holds a copy of $y$.
- **Stale handles.** The key that moved from the last cell has a new index, and so do the keys that the sift moved. A position map must record all of them.

## Implementations

The Python function `heap_delete(a, i)` works on a 0-based list, so the parent of $i$ is $\lfloor (i - 1)/2 \rfloor$. It pops the last element, and if $i$ is still inside the list it writes that element to $a[i]$ and sifts it up or down. Keys need only the operation "<".

## History

Heap delete at an index is a textbook operation; CLRS gives it as an exercise in Section 6.5. It goes back to the array heap of Williams (1964), whose insert and delete-max are the two moves that it combines.

## References
