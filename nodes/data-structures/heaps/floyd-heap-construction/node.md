---
tag: ADHNWH
kind: algorithm
slug: floyd-heap-construction
name: Floyd's heap construction
aliases:
- bottom-up heap construction
- build-heap
- linear-time heapify
area: data-structures/heaps
level: intro
summary: Sifts down every internal node from the last to the first, building a heap in O(n) time.
solves: [heap-construction]
model: comparison-model
complexity:
  vars: {n: the number of keys}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 1964
  people: [Robert W. Floyd]
  note: Floyd published the method in Algorithm 245, Treesort 3, in the Communications of the ACM in 1964.
prereqs: [binary-heap, sift-down, heap-property, loop-invariant]
see_also: [heap-construction, heap-construction-by-insertion, heapsort, binary-heap, d-ary-heap, legendre-formula]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 6.3 (Building a heap), BUILD-MAX-HEAP, its loop invariant and the O(n) bound
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3 (Sorting by selection), Algorithm H, the heap creation phase, and the history of heapsort
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.4, Heapsort, the heap construction by sink
  - paper: "Robert W. Floyd, Algorithm 245: Treesort 3, Communications of the ACM 7(12), 1964"
    locator: page 701
  - paper: "Marek A. Suchenek, Elementary yet precise worst-case analysis of Floyd's heap-construction program, Fundamenta Informaticae 120(1), 2012"
    locator: the main theorem, the worst-case number of comparisons 2n − 2s(n) − e(n)
---

Floyd's heap construction turns an array of $n$ keys into a [binary heap](/binary-heap/) in place, by a [sift-down](/sift-down/) of each internal node, from the last one back to the root. It solves the [heap construction](/heap-construction/) problem in $\Theta(n)$ time, with at most $n - s_2(n)$ swaps and at most $2(n - s_2(n))$ comparisons, where $s_2(n)$ is the number of 1 bits of $n$. Building the same heap by $n$ inserts costs $\Theta(n \log n)$ in the worst case, so this method is the standard first phase of [heapsort](/heapsort/) and the `heapify` of most libraries. Floyd published it in 1964.

## In plain words

Picture the heap as a family tree drawn in rows, with each parent required to be at least as large as its children. The bottom half of the tree is the leaves: a leaf alone is already a correct little heap.

Now go back over the parents, starting with the last parent and moving towards the top. Each parent has two little heaps under it. If it is smaller than a child, swap it with its larger child, and keep going down until it is at least as large as the children under it. After this, the parent and everything under it form a correct heap.

Most parents are near the bottom, and they can only move down a short way. Only a few parents are near the top, where the moves are long. So the total work is a small multiple of the number of items.

## The problem

The input is an array $A[1 \ldots n]$ of keys with a [total order](/total-order/). The output is a permutation of the same keys in $A$ that has the max-heap property $A[\lfloor i/2 \rfloor] \ge A[i]$ for $2 \le i \le n$. This is the max-heap version of [heap construction](/heap-construction/); for a min-heap, reverse each comparison of lines L5 and L6.

## The algorithm

```pseudo id=main
BUILD-MAX-HEAP(A, n)
L1  for i ← ⌊n/2⌋ downto 1 do
L2      MAX-HEAPIFY(A, n, i)

MAX-HEAPIFY(A, n, i)                    ▷ the subtrees of 2i and 2i + 1 are max-heaps
L3  while true do
L4      l ← 2i; r ← 2i + 1; m ← i
L5      if l ≤ n and A[l] > A[m] then m ← l
L6      if r ≤ n and A[r] > A[m] then m ← r
L7      if m = i then return
L8      swap A[i] and A[m]
L9      i ← m
```

The nodes $\lfloor n/2 \rfloor + 1$ to $n$ have no children, since $2i > n$ for them, so they are heaps of one node and line L1 skips them. MAX-HEAPIFY is the [sift-down](/sift-down/) of CLRS, written as a loop. Lines L5 and L6 find the largest of $A[i]$ and its children, with one comparison for each child that exists. If $A[i]$ is the largest, the subtree of $i$ is a heap and line L7 returns. Else line L8 swaps $A[i]$ with its larger child, and the loop goes on at the child, which is now the only place where the order can be wrong.

The order of the loop of line L1 is the point of the method. When node $i$ is processed, each node with a larger index is already the root of a heap, so the two subtrees of $i$ are heaps, and that is the condition of MAX-HEAPIFY.

## Example

Build a max-heap from $A = [4, 1, 3, 2, 16, 9, 10, 14, 8, 7]$, the input of CLRS Section 6.3. Here $n = 10$, so line L1 runs for $i = 5, 4, 3, 2, 1$. The columns "cmp" and "swaps" count the key comparisons of lines L5 and L6 and the swaps of line L8.

| $i$ | what MAX-HEAPIFY does | array after the step | cmp | swaps |
|---|---|---|---|---|
| 5 | 16 is larger than its child 7 | [4, 1, 3, 2, 16, 9, 10, 14, 8, 7] | 1 | 0 |
| 4 | 2 swaps with 14 | [4, 1, 3, 14, 16, 9, 10, 2, 8, 7] | 2 | 1 |
| 3 | 3 swaps with 10 | [4, 1, 10, 14, 16, 9, 3, 2, 8, 7] | 2 | 1 |
| 2 | 1 swaps with 16, then with 7 | [4, 16, 10, 14, 7, 9, 3, 2, 8, 1] | 3 | 2 |
| 1 | 4 swaps with 16, with 14, then with 8 | [16, 14, 10, 8, 7, 9, 3, 2, 4, 1] | 6 | 3 |

The total is 14 comparisons and 7 swaps. The bound of the complexity section gives at most $n - s_2(n) = 10 - 2 = 8$ swaps and $2 \cdot 8 = 16$ comparisons, and the exact worst case over all inputs of size 10 is $2n - 2s_2(n) - e_2(n) = 15$ comparisons. Inserting the same keys one by one in a heap gives a different max-heap, $[16, 14, 10, 8, 7, 3, 9, 1, 4, 2]$, with 17 comparisons and 9 swaps.

## Correctness

The loop of line L1 keeps this [loop invariant](/loop-invariant/): before the iteration for $i$, each node $j$ with $i + 1 \le j \le n$ is the root of a max-heap. At the start, $i = \lfloor n/2 \rfloor$ and each $j > \lfloor n/2 \rfloor$ is a leaf. In the iteration for $i$, both children of $i$ have larger indices, so their subtrees are heaps, and MAX-HEAPIFY makes the subtree of $i$ a heap; it changes only cells of that subtree, so each other subtree of an index above $i$ stays a heap. At the end $i = 0$, and node 1 is the root of a max-heap, which is the whole array. MAX-HEAPIFY only swaps, so the keys are permuted. The full proof, with the invariant of MAX-HEAPIFY itself, is in [the correctness proof](proofs/correctness.md).

## Complexity

**The work at one node.** Let the height of node $i$ be $h(i)$, the largest $h$ with $2^h i \le n$. MAX-HEAPIFY at $i$ moves down one level per swap, so it does at most $h(i)$ swaps. Each iteration of its loop does at most 2 comparisons, and the last iteration does none when $i$ has become a leaf. So it does at most $2 h(i)$ comparisons: if it stops at a leaf, there were $h(i)$ iterations with comparisons; if it stops earlier, there were at most $h(i)$ iterations in total.

**The sum of the heights.** Node $i$ has $h(i) \ge h$ exactly when $i \le \lfloor n/2^h \rfloor$. So

$$\sum_{i=1}^{n} h(i) = \sum_{h \ge 1} \#\{i : h(i) \ge h\} = \sum_{h \ge 1} \left\lfloor \frac{n}{2^h} \right\rfloor = n - s_2(n).$$

The last step is [Legendre's formula](/legendre-formula/): if $n = \sum_j b_j 2^j$ in binary, then $\lfloor n/2^h \rfloor = \sum_{j \ge h} b_j 2^{j-h}$, and summing over $h \ge 1$ gives $\sum_j b_j (2^j - 1) = n - s_2(n)$.

**The result.** BUILD-MAX-HEAP does at most $n - s_2(n) < n$ swaps and at most $2(n - s_2(n)) < 2n$ comparisons. Each iteration costs $O(1)$ plus $O(1)$ per swap, so the time is $O(n)$. Line L1 runs $\lfloor n/2 \rfloor$ times on each input, so the time is also $\Omega(n)$, and it is $\Theta(n)$ in the best, the average and the worst case. The extra space is $\Theta(1)$, since MAX-HEAPIFY is a loop, not a recursion.

**The exact worst case.** Suchenek (2012) proved that the largest number of comparisons over all inputs of size $n$ is $2n - 2s_2(n) - e_2(n)$, where $e_2(n)$ is the exponent of 2 in $n$. For $n = 1$ to $8$ this is $0, 1, 2, 4, 6, 7, 8, 11$.

**Why it beats $n$ inserts.** The method sends each key down, and most nodes are near the bottom, where a move down is short. A build by [insertion](/heap-construction-by-insertion/) sends each key up, and most nodes are near the bottom, where a move up is long: an increasing input makes each new key climb to the root, for $\sum_{i=1}^{n} \lfloor \lg i \rfloor = \Theta(n \log n)$ swaps. The proof of the bounds is in [the complexity proof](proofs/complexity.md).

## Properties

- **In place.** It uses the input array and $O(1)$ extra cells.
- **Not stable.** Swaps move equal keys past each other; a heap has no stable order anyway.
- **Not online.** It needs all keys at the start. For keys that arrive one at a time, insert each one.
- **Deterministic and comparison-based.** It uses only comparisons of keys, so its bounds hold in the [comparison model](/comparison-model/).

## Variants and improvements

- **Recursive MAX-HEAPIFY.** CLRS writes MAX-HEAPIFY with a tail call. The loop of lines L3 to L9 is the same and needs no stack.
- **Min-heap.** Reverse the comparisons in lines L5 and L6.
- **$d$-ary heaps.** Sift down with $d$ children. The same sum argument gives $O(n)$ time for each fixed $d$, see [d-ary heap](/d-ary-heap/).
- **Bottom-up sift-down.** Walk the path of larger children to a leaf with one comparison per level, then climb back to the place of the key. This lowers the comparison count, and it is the idea of bottom-up heapsort.
- **Better constants.** Gonnet and Munro (1986) build a heap with about $1.625n$ comparisons in the worst case, see [heap construction](/heap-construction/).
- **Cache-friendly order.** Processing the subtrees in depth-first order instead of index order does the same sift-downs, by the same invariant, with better locality for large arrays.

## When to use it

Use it whenever all keys are known at the start: for [heapsort](/heapsort/), to start a priority queue with many items, to meld two binary heaps (join the arrays, then build), or for [top-k selection](/top-k-selection/) in $O(n + k \log n)$ time. Use [repeated insertion](/heap-construction-by-insertion/) only when the keys arrive one at a time and the heap must be valid after each one. When a sorted output is needed anyway, sort.

## Pitfalls

- **Wrong loop order.** A loop for $i \leftarrow 1$ to $\lfloor n/2 \rfloor$ calls MAX-HEAPIFY on a node whose subtrees are not heaps yet, and the result is not a heap. For $A = [1, 2, 3, 4]$ it gives $[3, 4, 1, 2]$, where $3 < 4$ breaks the order at the root. Line L1 must count down.
- **Starting at $n$.** A loop from $n$ down to 1 is correct but does useless calls on the leaves. Start at $\lfloor n/2 \rfloor$, the last node with a child.
- **Off-by-one in 0-based code.** With $A[0 \ldots n-1]$, the children of $i$ are $2i + 1$ and $2i + 2$, and the loop runs from $\lfloor n/2 \rfloor - 1$ down to 0. Using $n/2$ as the first index reads beyond a leaf; using $2i$ and $2i + 1$ makes node 0 its own child.
- **Comparing the right child with $A[i]$.** Line L6 must compare $A[r]$ with $A[m]$, the larger of $A[i]$ and $A[l]$. Comparing with $A[i]$ can swap with the smaller child and leave the larger child below a smaller parent.

## Implementations

The Python function works on a 0-based list in place and builds a max-heap. A `key` function is not needed: the keys must support `<`.

## History

Robert W. Floyd published the method in 1964 as Algorithm 245, Treesort 3, in the Communications of the ACM. It improved the heapsort of Williams, Algorithm 232 of the same year, which built the heap by repeated insertion. Knuth gives this history in Section 5.2.3 of Volume 3. The exact worst-case count of comparisons, $2n - 2s_2(n) - e_2(n)$, is due to Suchenek (2012).

## References
