---
tag: 4GYGY9
kind: algorithm
slug: heap-extract-max
name: Heap extract-max
aliases:
- HEAP-EXTRACT-MAX
area: data-structures/heaps
level: intro
summary: A priority queue operation that removes and returns the largest element of a max-heap, then restores the heap property.
model: comparison-model
complexity:
  vars: {n: the number of keys in the heap}
  time: {worst: Θ(log n), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {in_place: true, deterministic: true, comparison: true, recursive: false}
history:
  year: 1964
  people: [J. W. J. Williams]
  note: Williams gave the removal of the largest key from an array heap in Algorithm 232, Heapsort, in the Communications of the ACM in 1964.
prereqs: [binary-heap, heap-property, sift-down]
see_also: [heap-increase-key, heap-delete, heapsort, priority-queue, floyd-heap-construction, sift-down, d-ary-heap, binary-heap]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 6.2 (Maintaining the heap property), MAX-HEAPIFY, and Section 6.5 (Priority queues), MAX-HEAP-EXTRACT-MAX
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.4 (Priority queues), delMax and sink in Algorithm 2.6
  - paper: "J. W. J. Williams, Algorithm 232: Heapsort, Communications of the ACM 7(6), 1964"
    locator: pages 347 to 348
---

Heap extract-max removes and returns the largest key of a binary max-heap stored in an array. It saves the root, moves the last key into the root, shrinks the heap by one cell, and sifts the new root down with MAX-HEAPIFY until the [heap property](/heap-property/) holds again. It runs in $O(\log n)$ time with at most $2\lfloor \lg(n - 1) \rfloor$ comparisons and $O(1)$ extra space. It is the delete-max of a max-[priority queue](/priority-queue/) and the step that [heapsort](/heapsort/) repeats $n - 1$ times. CLRS calls it HEAP-EXTRACT-MAX in the third edition and MAX-HEAP-EXTRACT-MAX in the fourth.

## In plain words

The largest number is at the top of the heap, so you take it from there. Now the top is empty. The only cell you can remove without a gap is the last one, so you move the last number to the top.

That number is usually small, so it is in the wrong place. Compare it with its two children. If a child is larger, swap it with the larger child. Repeat one level lower, until the number is at least as large as its children or it reaches the bottom. Each step goes down one level, and the heap has only about $\lg n$ levels.

## The problem

Input: an array $A[1 \ldots n]$ with $n = A.\mathit{heap\text{-}size} \ge 1$ that is a max-heap, so $A[\lfloor j/2 \rfloor] \ge A[j]$ for each $2 \le j \le n$. Output: a largest key of $A$, and the array $A[1 \ldots n - 1]$, which is a max-heap whose keys are the old keys with one copy of that largest key removed. An empty heap is an error.

## The algorithm

```pseudo id=main
HEAP-EXTRACT-MAX(A)                        ▷ A[1 .. A.heap-size] is a max-heap
L1  if A.heap-size < 1 then error "heap underflow"
L2  max ← A[1]
L3  A[1] ← A[A.heap-size]
L4  A.heap-size ← A.heap-size − 1
L5  MAX-HEAPIFY(A, 1)
L6  return max

MAX-HEAPIFY(A, i)                          ▷ sift A[i] down
L7  while true do
L8      l ← 2i, r ← 2i + 1, m ← i
L9      if l ≤ A.heap-size and A[l] > A[m] then m ← l
L10     if r ≤ A.heap-size and A[r] > A[m] then m ← r
L11     if m = i then return
L12     swap A[i] and A[m], i ← m
```

Line L2 saves the root, which is a largest key by the global form of the heap property. Lines L3 and L4 fill the hole with the last key and drop the last cell, so the array is again a [complete binary tree](/complete-binary-tree/). Only the root can now be too small for its place. MAX-HEAPIFY (lines L7 to L12) is the [sift-down](/sift-down/) for a max-heap: it finds the largest of the key and its children, and if that is a child, it swaps the two and goes on from the child.

## Example

Take the max-heap $A = [16, 14, 10, 8, 7, 9, 3, 2, 4, 1]$ of CLRS Chapter 6, with $n = 10$.

| step | what happens | array |
|---|---|---|
| L2 | max ← 16 | [16, 14, 10, 8, 7, 9, 3, 2, 4, 1] |
| L3, L4 | the last key 1 goes to the root, size 9 | [1, 14, 10, 8, 7, 9, 3, 2, 4] |
| L7 to L12, $i = 1$ | children 14 and 10; swap with 14 | [14, 1, 10, 8, 7, 9, 3, 2, 4] |
| $i = 2$ | children 8 and 7; swap with 8 | [14, 8, 10, 1, 7, 9, 3, 2, 4] |
| $i = 4$ | children 2 and 4; swap with 4 | [14, 8, 10, 4, 7, 9, 3, 2, 1] |
| $i = 9$ | no children, return | [14, 8, 10, 4, 7, 9, 3, 2, 1] |

The call returns 16 after 6 comparisons and 3 swaps. A second call returns 14 and leaves $[10, 8, 9, 4, 7, 1, 3, 2]$.

## Correctness

After line L4, each edge of the heap holds except perhaps the two edges out of the root: the edges between other cells are old edges between unchanged keys, and the root has no parent. MAX-HEAPIFY keeps the invariant that the only edges that may fail are the edges out of the current $i$, and that the parent of $i$, if any, is at least each child of $i$. When it stops, all edges hold. The keys were only moved, so the heap holds the old keys minus the returned one. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $n \ge 2$ be the size before the call, so the heap after line L4 has $n - 1$ cells and height $\lfloor \lg(n - 1) \rfloor$. Each iteration of MAX-HEAPIFY either stops or moves $i$ one level down, so there are at most $\lfloor \lg(n - 1) \rfloor$ swaps. An iteration does at most 2 comparisons of keys, and the last iteration does none if $i$ is a leaf. So the number of comparisons is at most $2\lfloor \lg(n - 1) \rfloor$, and the time is $O(\log n)$.

**Worst case.** On the heap $[n, n - 1, \ldots, 1]$, which is sorted in decreasing order and so a max-heap, the last key is 1, the smallest. It goes down to a leaf, so the call does $\lfloor \lg(n - 1) \rfloor$ or $\lfloor \lg(n - 1) \rfloor - 1$ swaps. So the worst case is $\Theta(\log n)$.

**Best case.** If all keys are equal, line L11 stops at once, after at most 2 comparisons. So the best case is $\Theta(1)$.

**Space.** The loop uses three indices, so the extra space is $\Theta(1)$.

In heapsort, the key that moves to the root comes from the bottom level, and it tends to sink back to near the bottom. That is why the bottom-up variant below saves comparisons.

## Properties

- In place: it uses $O(1)$ cells besides the array.
- Comparison-based: it uses only the order of keys.
- Not stable: two equal keys may change their relative order.
- Iterative: the loop of line L7 replaces the recursion of the CLRS version.

## Variants and improvements

- **Min-heap.** HEAP-EXTRACT-MIN is the same with each comparison reversed, see [binary heap](/binary-heap/).
- **Bottom-up sift-down.** Go down the path of larger children to a leaf with one comparison per level, then go back up from the leaf to the place of the moved key. This uses about $\lg n$ comparisons in place of about $2 \lg n$ when the key belongs near the bottom, as in heapsort.
- **Hole method.** Keep the moved key in a variable and move the children up into the hole, then write the key once at the end. This halves the writes.
- **[d-ary heap](/d-ary-heap/).** The sift-down compares $d$ children per level, so it costs $O(d \log_d n)$.
- **Delete of any index.** [Heap delete](/heap-delete/) removes $A[i]$ for any $i$; it may need a sift-up as well.
- **Heapsort.** Build with [Floyd's method](/floyd-heap-construction/), then call extract-max $n - 1$ times and put each result at the end of the array.

## When to use it

Use it whenever a max-priority queue in an array must return and remove its largest key: in [heapsort](/heapsort/), in schedulers that run the job of highest priority, and in the selection of the $k$ largest keys. For a min-queue, use the min version.

## Pitfalls

- **Forgetting the right-child bound.** The test $r \le A.\mathit{heap\text{-}size}$ in line L10 must use the new size. After line L4, the cell $n$ still holds the old last key, which now also sits at the root; comparing with it reads a stale key.
- **Comparing with $A[i]$ in line L10.** The second test must compare $A[r]$ with $A[m]$, the larger of $A[i]$ and $A[l]$; else the smaller child may move up and break the edge to the other child.
- **Underflow.** Line L1 must catch the empty heap. With $n = 1$, line L3 copies the root onto itself and the heap becomes empty, which is correct.
- **Recursion in MAX-HEAPIFY.** The recursive form of CLRS is a tail call; in a language without tail calls, the loop form avoids a stack of depth $\lg n$.

## Implementations

The Python function works on a 0-based list, so the children of $i$ are $2i + 1$ and $2i + 2$. It pops the last element first and writes it to the root only if the list is not empty, which covers the case $n = 1$ without the self-copy of line L3. Keys need only the operation "<".

## History

Williams described the array heap and the removal of its top key in 1964, as part of heapsort, in Algorithm 232 of the Communications of the ACM. The form with MAX-HEAPIFY and the name HEAP-EXTRACT-MAX are the ones of CLRS, Chapter 6.

## References
