---
tag: 0PQJ7X
kind: algorithm
slug: heap-construction-by-insertion
name: Heap construction by insertion
aliases:
- Building a heap using insertion
area: data-structures/heaps
level: core
summary: Building a heap by inserting elements one at a time, which takes O(n log n) time in the worst case, slower than bottom-up construction.
solves: [heap-construction]
model: comparison-model
complexity:
  vars: {n: the number of keys}
  time: {worst: Θ(n log n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: true, adaptive: true, online: true, deterministic: true, comparison: true, recursive: false}
history:
  year: 1964
  people: [J. W. J. Williams]
  note: Williams built the heap of heapsort by inserting the keys one by one in Algorithm 232, in the Communications of the ACM in 1964.
prereqs: [binary-heap, sift-up, heap-property, heap-construction]
see_also: [floyd-heap-construction, heap-construction, heap-increase-key, heapsort, binary-heap, sift-up, d-ary-heap, heap-extract-max]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 6, Problem 6-1 (Building a heap using insertion)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3 (Sorting by selection), the history of heapsort and the insertion method of Williams
  - paper: "J. W. J. Williams, Algorithm 232: Heapsort, Communications of the ACM 7(6), 1964"
    locator: pages 347 to 348
  - paper: "Ryan Hayward and Colin McDiarmid, Average case analysis of heap building by repeated insertion, Journal of Algorithms 12(1), 1991"
    locator: the main result, the linear average number of comparisons
---

Heap construction by insertion builds a [binary heap](/binary-heap/) from $n$ keys by inserting them one at a time: for $j = 2, \ldots, n$, it treats $A[1 \ldots j - 1]$ as a heap and moves $A[j]$ up with [sift-up](/sift-up/) until the [heap property](/heap-property/) holds. It is the method of Williams (1964). It works in place and online, so the keys can arrive one by one. Its worst case is $\Theta(n \log n)$, when each new key is larger than all earlier ones and climbs to the root, which is worse than the $\Theta(n)$ of [Floyd's heap construction](/floyd-heap-construction/). On a random order it takes $\Theta(n)$ expected time. CLRS states it as Problem 6-1.

## In plain words

Start with the first number as a heap of one. Take the next number and put it at the end. If it is larger than the number above it, swap them, and go on until the number above is larger or you reach the top. Then the heap is one item larger. Do this for each number in turn.

Each number can climb all the way to the top, which is about $\lg n$ steps. If the numbers come in increasing order, each new number is the largest so far, and each one climbs to the top, so the total work grows like $n \lg n$. In a random order, most new numbers stop after one or two steps.

## The problem

The [heap construction](/heap-construction/) problem: given $A[1 \ldots n]$, permute it so that $A[\lfloor i/2 \rfloor] \ge A[i]$ for each $2 \le i \le n$ (a max-heap). The online version asks that $A[1 \ldots j]$ is a max-heap after the $j$-th key is added.

## The algorithm

```pseudo id=main
BUILD-BY-INSERTION(A, n)                   ▷ makes A[1 .. n] a max-heap
L1  for j ← 2 to n do                      ▷ A[1 .. j − 1] is a max-heap
L2      i ← j
L3      while i > 1 and A[⌊i/2⌋] < A[i] do
L4          swap A[i] and A[⌊i/2⌋]
L5          i ← ⌊i/2⌋
```

Lines L2 to L5 are the insert of a binary max-heap: the key $A[j]$ is the new last cell, and sift-up moves it up while it is larger than its parent. CLRS writes it as a loop of MAX-HEAP-INSERT calls.

## Example

Take $A = [4, 1, 3, 2, 16, 9, 10, 14, 8, 7]$, the input that CLRS uses for BUILD-MAX-HEAP.

| $j$ | new key | what happens | comparisons | swaps | array |
|---|---|---|---|---|---|
| 2 | 1 | parent 4, stop | 1 | 0 | [4, 1, 3, 2, 16, 9, 10, 14, 8, 7] |
| 3 | 3 | parent 4, stop | 1 | 0 | same |
| 4 | 2 | swap with 1, then parent 4 | 2 | 1 | [4, 2, 3, 1, 16, 9, 10, 14, 8, 7] |
| 5 | 16 | swap with 2, then with 4 at the root | 2 | 2 | [16, 4, 3, 1, 2, 9, 10, 14, 8, 7] |
| 6 | 9 | swap with 3, then parent 16 | 2 | 1 | [16, 4, 9, 1, 2, 3, 10, 14, 8, 7] |
| 7 | 10 | swap with 9, then parent 16 | 2 | 1 | [16, 4, 10, 1, 2, 3, 9, 14, 8, 7] |
| 8 | 14 | swap with 1, with 4, then parent 16 | 3 | 2 | [16, 14, 10, 4, 2, 3, 9, 1, 8, 7] |
| 9 | 8 | swap with 4, then parent 14 | 2 | 1 | [16, 14, 10, 8, 2, 3, 9, 1, 4, 7] |
| 10 | 7 | swap with 2, then parent 14 | 2 | 1 | [16, 14, 10, 8, 7, 3, 9, 1, 4, 2] |

The result is a valid max-heap after 17 comparisons and 9 swaps. Floyd's method gives the different max-heap $[16, 14, 10, 8, 7, 9, 3, 2, 4, 1]$ on the same input, with 14 comparisons and 7 swaps.

## Correctness

The loop of line L1 keeps the invariant that $A[1 \ldots j - 1]$ is a max-heap. Adding the cell $j$ adds one edge, from $\lfloor j/2 \rfloor$ to $j$, and the new node has no children. So the only edge that may fail is the one into the current $i$, and the parent of $i$ is at least each child of $i$. Each swap moves the possible failure one level up and keeps this condition, and the loop of line L3 stops at the root or when the edge holds. Then $A[1 \ldots j]$ is a max-heap. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The insert of the key $j$ makes at most $\lfloor \lg j \rfloor$ swaps, one per level of the tree $A[1 \ldots j]$, and as many comparisons plus one if it stops below the root.

**Worst case.** If $A$ is in increasing order, each new key is larger than each earlier key, so it climbs to the root with exactly $\lfloor \lg j \rfloor$ comparisons and swaps. The total is

$$\sum_{j=1}^{n} \lfloor \lg j \rfloor = (n + 1)\lfloor \lg n \rfloor - 2^{\lfloor \lg n \rfloor + 1} + 2,$$

which is $n \lg n - O(n)$. For $n = 10$ this is 19. No input does more swaps, so the worst case is $\Theta(n \log n)$ time. The sum follows by counting: the $2^t$ values $j$ from $2^t$ to $2^{t+1} - 1$ each give $t$.

**Best case.** If $A$ is already a max-heap, for example in decreasing order, each insert does one comparison and no swap, so $n - 1$ comparisons and $\Theta(n)$ time.

**Average case.** For a random order of $n$ distinct keys, Hayward and McDiarmid (1991) showed that the expected number of comparisons is $\Theta(n)$; its constant is about 2.28 comparisons per key, with about 1.28 swaps per key. The reason is that a new key at the bottom level is likely to be smaller than its parent, which is the largest key of its subtree. Floyd's method is linear in the worst case as well, with fewer than $2n$ comparisons.

**Space.** $\Theta(1)$ extra cells.

## Properties

- In place and online: after the $j$-th key, the prefix $A[1 \ldots j]$ is a heap.
- Adaptive: input that is close to a heap, for example decreasing input, costs $O(n)$.
- Comparison-based and not stable.
- On the same input, it can give a different heap from Floyd's method; both are correct.

## Variants and improvements

- **Min-heap.** Reverse the comparison in line L3.
- **Hole method.** Keep the new key in a variable and move each smaller parent down into the hole, then write the key once. This uses one write per level in place of a swap.
- **Binary search on the path.** The keys on the path from the new leaf to the root are sorted, so a binary search finds the place with about $\lg \lg j$ comparisons per insert, which gives $O(n \log \log n)$ comparisons in the worst case. The moves still cost $O(n \log n)$.
- **Floyd's method.** When all keys are known at the start, [Floyd's heap construction](/floyd-heap-construction/) builds the heap in $\Theta(n)$ worst-case time.
- **Other heaps.** In a [binomial heap](/binomial-heap/) or a [Fibonacci heap](/fibonacci-heap/), $n$ inserts take $O(n)$ time in the worst case or amortized.

## When to use it

Use it when the keys arrive one at a time and the heap must be valid after each arrival, as in a priority queue that is filled while it is used, or when the code already has an insert and the inputs are not adversarial. When all keys are known at the start, use Floyd's method, which is never worse and is linear in the worst case.

## Pitfalls

- **Assuming $O(n)$.** The average is linear, but sorted or nearly sorted input in the wrong direction costs $\Theta(n \log n)$, and such input is common in practice.
- **Starting at $j = 1$.** A single key is a heap; starting at $j = 1$ does no harm, but a sift-up from index 1 must not read its parent.
- **The 0-based parent.** With $A[0 \ldots n - 1]$, the parent of $i$ is $\lfloor (i - 1)/2 \rfloor$.
- **Comparing with the wrong order.** For a max-heap the test is $A[\text{parent}] < A[i]$. With the test reversed, the result is a min-heap, which the rest of the code may not expect.

## Implementations

The Python function `heap_construction_by_insertion(a)` works on a 0-based list in place. The helper `sift_up(a, j)` is the body of the loop, lines L2 to L5, so it can also be used to add one key to an existing max-heap. Keys need only the operation "<".

## History

Williams introduced heapsort in 1964 in Algorithm 232 of the Communications of the ACM, and his heap was built by inserting the keys one by one. In the same year Floyd gave the bottom-up method, Treesort 3, which builds the heap in linear time. Hayward and McDiarmid analysed the average case of the insertion method in 1991.

## References
