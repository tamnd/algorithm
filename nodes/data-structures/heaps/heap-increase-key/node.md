---
tag: ZN9K6H
kind: algorithm
slug: heap-increase-key
name: Heap increase-key
aliases:
- HEAP-INCREASE-KEY
area: data-structures/heaps
level: intro
summary: A max-heap operation that raises the key of an element and moves it up toward the root until the heap property holds.
model: comparison-model
complexity:
  vars: {n: the number of keys in the heap, i: the index of the changed key}
  time: {worst: Θ(log n), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {in_place: true, deterministic: true, comparison: true, recursive: false}
history:
  year: 1964
  people: [J. W. J. Williams]
  note: Williams moved a new key up from the bottom of an array heap in Algorithm 232 (1964); the increase-key form is the one that textbooks such as CLRS give.
prereqs: [binary-heap, heap-property, sift-up]
see_also: [decrease-key, heap-extract-max, heap-delete, sift-up, indexed-priority-queue, priority-queue, heapsort, binary-heap]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 6.5 (Priority queues), MAX-HEAP-INCREASE-KEY, its loop invariant, and MAX-HEAP-INSERT
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 6.5 (Priority queues), HEAP-INCREASE-KEY and Figure 6.5
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.4 (Priority queues), swim
---

Heap increase-key raises the key at index $i$ of a binary max-heap in an array to a new key $k \ge A[i]$, and then moves it up: while the key is larger than the key of its parent, it swaps the two. It runs in $O(\log n)$ time, with at most $\lfloor \lg i \rfloor$ swaps and comparisons of the parent and the child. It is the max-heap form of [decrease-key](/decrease-key/), and the [sift-up](/sift-up/) that it does also gives the insert of a max-priority queue: append a key smaller than all others and increase it. CLRS calls it HEAP-INCREASE-KEY in the third edition and MAX-HEAP-INCREASE-KEY in the fourth.

## In plain words

In a max-heap, each number is at least as large as the numbers below it. If you make one number larger, the numbers below it are still fine. The only rule that can break is with the number directly above it.

So compare the new number with the one above. If the new number is larger, swap them. Do the same at the new place. Stop when the number above is at least as large, or when you reach the top. Each swap goes up one level, so there are at most about $\lg n$ swaps.

## The problem

Input: a max-heap $A[1 \ldots n]$, so $A[\lfloor j/2 \rfloor] \ge A[j]$ for each $2 \le j \le n$, an index $1 \le i \le n$, and a key $k \ge A[i]$. Output: a max-heap on the same cells whose multiset of keys is the old one with one copy of $A[i]$ replaced by $k$. A key $k < A[i]$ is an error.

## The algorithm

```pseudo id=main
HEAP-INCREASE-KEY(A, i, k)                 ▷ A[1 .. n] is a max-heap, 1 ≤ i ≤ n
L1  if k < A[i] then error "new key is smaller than the current key"
L2  A[i] ← k
L3  while i > 1 and A[⌊i/2⌋] < A[i] do
L4      swap A[i] and A[⌊i/2⌋]
L5      i ← ⌊i/2⌋
```

Line L1 checks the direction. Line L2 writes the key. A larger key at $i$ keeps the edges from $i$ to its children, so only the edge to the parent can fail. Lines L3 to L5 move the key up while that edge fails.

**Insert by increase.** MAX-HEAP-INSERT$(A, k)$ appends a key $-\infty$ at the new cell $n + 1$ and calls HEAP-INCREASE-KEY$(A, n + 1, k)$. The Python code appends $k$ itself and calls the same loop, which is the same since the loop only compares.

## Example

Take the max-heap $A = [16, 14, 10, 8, 7, 9, 3, 2, 4, 1]$ and raise $A[9] = 4$ to 15, as in Figure 6.5 of the third edition of CLRS.

| step | what happens | array |
|---|---|---|
| L2 | $A[9] \leftarrow 15$ | [16, 14, 10, 8, 7, 9, 3, 2, 15, 1] |
| L3 to L5, $i = 9$ | the parent $A[4] = 8 < 15$, swap | [16, 14, 10, 15, 7, 9, 3, 2, 8, 1] |
| $i = 4$ | the parent $A[2] = 14 < 15$, swap | [16, 15, 10, 14, 7, 9, 3, 2, 8, 1] |
| $i = 2$ | the parent $A[1] = 16 \ge 15$, stop | [16, 15, 10, 14, 7, 9, 3, 2, 8, 1] |

The call does 3 comparisons in line L3 and 2 swaps.

## Correctness

The loop keeps the invariant of CLRS: each edge of the heap holds except perhaps the edge from $A[\lfloor i/2 \rfloor]$ to $A[i]$, and if $A[i]$ has a parent, that parent is at least each child of $i$. A swap moves the one possible failure one level up, and the loop stops at the root or when the edge holds. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Each iteration of lines L3 to L5 costs $O(1)$ and halves $i$, so there are at most $\lfloor \lg i \rfloor \le \lfloor \lg n \rfloor$ iterations, with one comparison each, plus one last comparison when the loop stops at an index $i > 1$.

**Worst case.** Raise a leaf at the bottom level to a key larger than the root: the key goes up to the root, with $\lfloor \lg n \rfloor$ swaps. So the worst case is $\Theta(\log n)$.

**Best case.** If $k$ is at most the key of the parent, or $i = 1$, the loop does not run. So the best case is $\Theta(1)$.

**Space.** $\Theta(1)$ extra cells.

**Insert.** MAX-HEAP-INSERT costs the same, $O(\log n)$. Building a heap by $n$ inserts is [heap construction by insertion](/heap-construction-by-insertion/), which is $\Theta(n \log n)$ in the worst case.

## Properties

- In place, with $O(1)$ extra space.
- Comparison-based.
- It changes only the cells on the path from $i$ to the root.
- Not stable: equal keys may change their order.

## Variants and improvements

- **Min-heap.** The same loop with the comparison reversed is the decrease-key of a binary min-heap, see [binary heap](/binary-heap/).
- **Hole method.** Keep $k$ in a variable, move each smaller parent down into the hole, and write $k$ once at the end. This uses one write per level in place of the three of a swap. CLRS gives it as an exercise.
- **Binary search on the path.** The keys on the path from $i$ to the root are in non-decreasing order upward, so a binary search finds the place of $k$ with about $\lg \lg n$ comparisons. The moves still cost $O(\log n)$.
- **Change-key.** A key that may go up or down needs a sift-up when it grows and a sift-down when it shrinks.
- **Handles.** With a position map, the caller names the item instead of the index, see [indexed priority queue](/indexed-priority-queue/). The map must be updated at each swap.

## When to use it

Use it in a max-priority queue whose items gain priority while they wait, for example a scheduler that raises the priority of old jobs, and as the insert of an array max-heap. For shortest paths and spanning trees, the same operation in a min-heap is the decrease-key of [Dijkstra's algorithm](/dijkstra/) and [Prim's algorithm](/prim/).

## Pitfalls

- **A smaller key.** If $k < A[i]$, the loop does nothing, but the edges from $i$ to its children may now fail. Line L1 must reject it, or the code must call a sift-down.
- **Off-by-one in the parent.** With a 0-based array, the parent of $i$ is $\lfloor (i - 1)/2 \rfloor$. The 1-based formula $\lfloor i/2 \rfloor$ makes 0 the parent of 1 and 1 the parent of 2 and 3, which is wrong.
- **The loop bound.** The test $i > 1$ (or $i > 0$ when 0-based) must come first, so that the code never reads the parent of the root.
- **Stale indices.** After the call, the item that was at $i$ is at a new index. A caller that keeps indices must update them at each swap.

## Implementations

The Python function `heap_increase_key(a, i, key)` works on a 0-based list and checks the index and the direction. `max_heap_insert(a, key)` appends the key and calls it. Keys need only the operation "<".

## History

Williams used the upward move to insert a key into an array heap in 1964, in Algorithm 232, Heapsort. The name HEAP-INCREASE-KEY and its use as a priority-queue operation come from textbooks, in particular CLRS, Section 6.5.

## References
