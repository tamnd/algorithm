---
tag: WX5SGY
kind: algorithm
slug: smoothsort
name: Smoothsort
aliases:
- Dijkstra's smoothsort
- smooth sort
area: sorting/comparison-sorts
level: research
summary: In-place heap-based sort using Leonardo heaps; O(n) on sorted input and O(n log n) worst case.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: O(n log n), average: Θ(n log n), best: Θ(n)}
  space: {extra: O(1)}
properties: {stable: false, in_place: true, adaptive: true, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 1981
  people: [Edsger W. Dijkstra]
  note: Dijkstra described smoothsort in the note EWD796a in 1981, published in Science of Computer Programming in 1982.
prereqs: [heapsort, binary-heap]
see_also: [heapsort, binary-heap, sift-down, adaptive-sorting, timsort, insertion-sort, weak-heapsort, presortedness]
sources:
  - paper: "Edsger W. Dijkstra, Smoothsort, an alternative for sorting in situ, Science of Computer Programming 1(3), 1982 (also the note EWD796a, 1981)"
    locator: the whole paper, with the Leonardo numbers, the stretches, the operations sift and trinkle, and the claim of linear time on sorted input
  - paper: "Stefan Hertel, Smoothsort's behavior on presorted sequences, Information Processing Letters 16(4), 1983"
    locator: the analysis of the number of comparisons on presorted input
  - paper: "Coenraad Bron and Wim H. Hesselink, Smoothsort revisited, Information Processing Letters 39(5), 1991"
    locator: the derivation of smoothsort from its invariants
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3, Sorting by selection (heapsort, and the remarks on heaps that adapt to the order of the input)
---

Smoothsort is an in-place sort by Edsger Dijkstra (1981) that works like [heapsort](/heapsort/) but adapts to the order of the input. Instead of one [binary heap](/binary-heap/), it keeps the prefix of the array as a forest of *Leonardo heaps*: max-heaps whose sizes are Leonardo numbers $1, 1, 3, 5, 9, 15, 25, \ldots$, laid out from left to right with their roots in ascending order. The largest item of the prefix is then the root of the last heap, at the right end, which is where it must go. Building the forest and taking it apart cost $O(n \log n)$ comparisons in the worst case and $O(n)$ on a sorted input, with a smooth change between the two. It uses $O(1)$ extra space and is not stable.

## In plain words

Heapsort first builds a heap, a tree in which each parent is at least its children, and then takes the largest item off again and again. It always does the same amount of work, even on a list that is already sorted.

Smoothsort uses a row of several heaps instead of one. The sizes of the heaps follow a special list of numbers, so that two neighbouring heaps and one new item can always join into a bigger heap. The heaps are kept so that their tops, read from left to right, go up. Then the largest item of all is the top of the last heap, at the right end of the row. That is already its place in the sorted list.

On a sorted list, each new item is larger than everything before it, so it can stay where it is, and almost no work is needed.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array, with its items in non-decreasing order. This is the [sorting problem](/sorting-problem/). Smoothsort works in place, with a small description of the forest as its only extra memory.

## The algorithm

The Leonardo numbers are $L(0) = L(1) = 1$ and $L(k) = L(k-1) + L(k-2) + 1$. A *Leonardo tree* of order $k$ is a single node for $k \le 1$; for $k \ge 2$ it is a root with a left subtree of order $k - 1$ and a right subtree of order $k - 2$. It has $L(k)$ nodes, and it is stored in a segment of the array in post-order: the left subtree, then the right subtree, then the root at the right end. So the root of a tree of order $k \ge 2$ at index $r$ has its right child at $r - 1$ and its left child at $r - 1 - L(k-2)$. A *Leonardo heap* is such a tree in max-heap order.

```pseudo id=main
SMOOTHSORT(A)                              ▷ the forest is a list of (root, order), left to right
L1  F ← an empty forest
L2  for i ← 0 to n − 1 do                  ▷ build: add A[i] to the forest
L3      if the last two trees of F have orders k + 1 and k then replace them by one tree of order k + 2, with root i
L4      else if the last tree has order 1 then append a tree of order 0 at i, else append a tree of order 1 at i
L5      RECTIFY(F, the last tree)
L6  for i ← n − 1 down to 1 do             ▷ take apart: A[i] is the largest item left
L7      remove the last tree from F;  let k be its order
L8      if k ≥ 2 then
L9          append its two subtrees to F, and RECTIFY each of them, the left one first

RECTIFY(F, j)                              ▷ trees before j are heaps with ascending roots
    while j is not the first tree, and the root of tree j − 1 is greater than the root of tree j and its children:
        swap the two roots;  j ← j − 1
    SIFT-DOWN the root of tree j
```

**The two invariants.** After each step of the build, and of the taking apart, (a) each tree of the forest is a Leonardo heap, and (b) the roots of the trees are in non-decreasing order from left to right. So the largest item of the forest is the root of the last tree, at the right end of the prefix.

**Adding an item.** Line L3 joins two neighbouring trees of orders $k + 1$ and $k$ with the new item as root, which gives a tree of order $k + 2$ in the right layout. Otherwise the new item is a tree of one node. RECTIFY then moves the new root to the left past larger roots, as in an insertion sort of the roots, and sifts it down into the tree where it stops. The test also looks at the children of the current root, because the root of a new tree may be smaller than its children; then the larger root must not move into this tree.

**Removing the largest item.** The root of the last tree is at index $i$, its final place. If the tree has order $k \ge 2$, removing its root leaves its two subtrees as two trees of the forest. They are heaps, but their roots may break the order (b), so each is rectified.

**The shape of the forest.** The rule of lines L3 and L4 keeps the orders of the trees strictly decreasing from left to right, except that the last two may be 1 and 0. Each $n$ is a sum of such Leonardo numbers, and $L(k) = 2F_{k+1} - 1$, where $F_k$ is the $k$-th Fibonacci number, so the forest has $O(\log n)$ trees. Dijkstra stores it as a bit vector of the orders that are present, which fits in a few machine words, so the extra space is $O(1)$ words.

## Example

Sort $A = [7, 2, 9, 4, 1, 8, 3, 6]$. Each tree is written as (root index, order).

| $i$ | the array after the step | the forest |
|---|---|---|
| 0 | 7 2 9 4 1 8 3 6 | (0, 1) |
| 1 | 2 7 9 4 1 8 3 6 | (0, 1), (1, 0): 7 and 2 swap, so the roots ascend |
| 2 | 2 7 9 4 1 8 3 6 | (2, 2): the root 9 is at least its children 2 and 7 |
| 3 | 2 4 7 9 1 8 3 6 | (2, 2), (3, 1): 4 swaps with 9, then sifts down past 7 |
| 4 | 2 4 7 1 9 8 3 6 | (4, 3): 1 joins the trees as the root, and 9 rises to replace it |
| 5 | 2 4 7 1 8 9 3 6 | (4, 3), (5, 1): 8 and 9 swap |
| 6 | 2 3 4 1 7 8 9 6 | (4, 3), (5, 1), (6, 0) |
| 7 | 2 3 4 1 7 8 6 9 | (4, 3), (7, 2) |

After the build, the largest item 9 is at index 7. The taking apart then removes the root at index 7 and splits its tree of order 2 into trees at indices 5 and 6, rectifies them, and so on. At the end the array is $1, 2, 3, 4, 6, 7, 8, 9$. The build makes 22 comparisons and the whole sort 33.

## Correctness

The proof uses the two invariants (a) and (b) above. Line L3 joins two heaps under a new root, so after it all trees are heaps except perhaps the new one at its root. RECTIFY restores both invariants: each swap moves a root that is larger than the current root and its children into the current tree, which keeps that tree a heap below its root, and keeps the order of the roots to its left; at the end the sift-down makes the last touched tree a heap. In the taking apart, the largest item of the prefix $A[0 \ldots i]$ is the root of the last tree, by (b), and it is at index $i$, so it is in its final place. Its subtrees are heaps, and rectifying them restores (b). The full proof is below.

## Complexity

**The worst case.** The forest has $O(\log n)$ trees and each tree has height $O(\log n)$. RECTIFY moves a root past at most $O(\log n)$ trees, and then sifts down through $O(\log n)$ levels, with $O(1)$ comparisons per step. It runs $n$ times in the build and at most $2n$ times in the taking apart. So the time is $O(n \log n)$.

**Sorted input.** Each new item is at least all items before it. In RECTIFY, the root of the previous tree is not greater than the new root, so no root moves, and the sift-down stops at once, because the new root is at least its children. In the taking apart, the subtrees of a removed root are heaps with roots in order, so each rectify is again $O(1)$. So the time is $O(n)$. For sorted input of $10^5$ items, the implementation makes 599,819 comparisons, about $6n$.

**Measured counts.** For the implementation on this page, which rectifies after each step:

| input | $n = 1000$ | $n = 10^5$ |
|---|---|---|
| sorted | 5,893 | 599,819 |
| sorted, then 10 swaps of neighbours | 5,925 | 599,845 |
| reversed | 26,933 | 4,084,823 |
| random | 28,749 | 5,096,785 |

On random input this is about $3 n \lg n$, more than the about $2 n \lg n$ of heapsort. Dijkstra's version saves some of this: in the build, it only sifts down a new tree that will later be joined into a larger one, and rectifies only the trees that stay.

**Adaptivity.** Hertel (1983) studied smoothsort on presorted input. The time is linear on sorted input and close to it on input with few local changes, but smoothsort does not reach the best bound for some measures of [presortedness](/presortedness/), for which adaptive merge sorts such as [Timsort](/timsort/) do better.

| claim | model and case | bound |
|---|---|---|
| time | comparison model, worst | $O(n \log n)$ |
| time | sorted input | $\Theta(n)$ |
| time | random permutation | $\Theta(n \log n)$ |
| extra space | | $O(1)$ words, with the forest as a bit vector |

## Properties

- **Not stable.** The sift-down and the swaps of roots move items over long distances.
- **In place.** The forest is described by a few words; all items stay in the array.
- **Adaptive.** Linear time on sorted input, and a smooth change to $O(n \log n)$ as the disorder grows, which is the meaning of the name.
- **Complex.** It needs the Leonardo numbers, the layout of the trees and two kinds of repair, and it is much harder to write correctly than heapsort.

## Variants and improvements

- **Dijkstra's original.** It keeps the orders in a bit vector and two Leonardo numbers in variables, and it uses the operations "sift" and "trinkle" for the two kinds of repair. It also avoids the rectify for trees that will be joined later.
- **Poplar sort.** Bron and Hesselink and others studied related forests of perfect binary trees ("poplars"), which are simpler but not linear on sorted input.
- **[Heapsort](/heapsort/).** The same method with one heap, simpler and with fewer comparisons on random input, but $\Theta(n \log n)$ on every input.
- **[Weak heapsort](/weak-heapsort/).** A heapsort variant that aims at few comparisons rather than at adaptivity.

## When to use it

Smoothsort is mostly of interest as a design: it shows that an in-place sort with $O(1)$ extra space can be both $O(n \log n)$ in the worst case and linear on sorted input. In practice, use [Timsort](/timsort/) or a natural merge sort when adaptivity matters and memory is available, and [heapsort](/heapsort/) or introsort when an in-place worst-case bound matters. Smoothsort fits small systems where memory is very tight and the input is often nearly sorted.

## Pitfalls

- **The rectify test.** Compare the previous root with the larger of the current root and its children, not with the root alone. A new root can be smaller than its children before the sift-down, and moving a root that is smaller than those children into the tree breaks the heap order.
- **The layout of a tree.** The left subtree has order $k - 1$ and starts the segment; the right subtree has order $k - 2$ and ends just before the root. Swapping the two gives wrong child indices.
- **The order of the two rectifies.** After a root is removed, rectify the left subtree first, then the right one, so that each rectify sees a valid forest to its left.
- **Joining the right trees.** Only the last two trees, of orders $k + 1$ and $k$, may be joined. The rule for orders 1 and 0 at the end is easy to get wrong; test all small sizes.

## Implementations

## History

Dijkstra wrote smoothsort in 1981, in the note EWD796a, as an answer to the question whether an in-place sort could be $O(n \log n)$ in the worst case and still be fast on input that is almost sorted. The paper appeared in Science of Computer Programming in 1982. Hertel analysed its behaviour on presorted input in 1983, and Bron and Hesselink gave a new derivation in 1991. It is rarely used in libraries, but it remains a classic example of a careful design driven by invariants.

## References
