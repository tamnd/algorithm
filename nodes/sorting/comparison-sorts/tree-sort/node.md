---
tag: P5E3N3
kind: algorithm
slug: tree-sort
name: Tree sort
aliases:
- binary tree sort
area: sorting/comparison-sorts
level: intro
summary: Insert all keys into a binary search tree, then read them in order; Theta(n log n) average.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n²), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {stable: true, in_place: false, adaptive: false, online: true, deterministic: true, comparison: true, recursive: false}
prereqs: [binary-search-tree, inorder-traversal]
see_also: [binary-search-tree, inorder-traversal, quicksort, random-binary-search-tree, red-black-tree, avl-tree, splay-tree, treap]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.2, Binary tree searching (Algorithm T, tree insertion, the mean number of comparisons for random insertions, and its link with quicksort)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 12, Binary search trees (Section 12.3 on insertion, and Exercise 12.3-3 on sorting by insertions and an inorder walk)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.2, Binary search trees (Proposition C, about 2 ln N compares for a search hit in a tree built from random keys, and the link with quicksort)
---

Tree sort inserts the items one by one into a [binary search tree](/binary-search-tree/) and then reads them back with an [inorder traversal](/inorder-traversal/), which visits the keys in sorted order. With a plain, unbalanced tree, it makes exactly the same comparisons as [quicksort](/quicksort/) with the first item as the pivot: on average $2(n+1)H_n - 4n \approx 1.39\, n \lg n$, and $n(n-1)/2$ on a sorted input, so the time is $\Theta(n \log n)$ on average and $\Theta(n^2)$ in the worst case. With a balanced tree, such as a [red-black tree](/red-black-tree/) or an [AVL tree](/avl-tree/), the worst case is $O(n \log n)$. It needs $\Theta(n)$ extra space for the nodes. If equal keys go to the right, it is stable.

## In plain words

You build a family tree of numbers. The first number is the top. Each new number starts at the top and walks down: if it is smaller than the number it meets, it goes left, otherwise it goes right. When it finds an empty place, it stays there. So for each number in the tree, all smaller numbers are on its left side, and all the others are on its right side.

To read the numbers in order, you visit the left side of the top, then the top, then the right side, and you do the same inside each side. This gives the numbers from smallest to largest.

If the numbers come in random order, the tree is bushy and the walks are short. If they come already sorted, each new number goes right, the tree is one long line, and the walks are long.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array, with its items in non-decreasing order. This is the [sorting problem](/sorting-problem/). The algorithm builds a tree of $n$ nodes and then writes the items back into $A$.

## The algorithm

```pseudo id=main
TREE-SORT(A)                               ▷ n is the length of A
L1  T ← an empty binary search tree
L2  for i ← 0 to n − 1 do
L3      INSERT(T, A[i])                    ▷ go left if A[i] < key, else right
L4  i ← 0
L5  for each node v of T, in inorder do
L6      A[i] ← v.key;  i ← i + 1
```

INSERT starts at the root and moves to the left child when the new item is less than the key of the node, and to the right child otherwise, until it reaches an empty place, where it puts a new node. Each step of the walk is one comparison. Line L5 visits the nodes in inorder: the left subtree, the node, the right subtree. Both the walk of INSERT and the inorder traversal can be loops, with an explicit stack for the traversal, so a tall tree does not overflow the call stack.

## Example

Sort $A = [5, 3, 8, 1, 4, 7, 9, 2, 6]$. The inserts build this tree, with each item placed under the node shown:

| item | path from the root | comparisons | placed as |
|---|---|---|---|
| 5 | | 0 | the root |
| 3 | 5 | 1 | left child of 5 |
| 8 | 5 | 1 | right child of 5 |
| 1 | 5, 3 | 2 | left child of 3 |
| 4 | 5, 3 | 2 | right child of 3 |
| 7 | 5, 8 | 2 | left child of 8 |
| 9 | 5, 8 | 2 | right child of 8 |
| 2 | 5, 3, 1 | 3 | right child of 1 |
| 6 | 5, 8, 7 | 3 | left child of 7 |

The inserts make 16 comparisons, and the tree has height 3. The inorder traversal visits 1, 2, 3, 4, 5, 6, 7, 8, 9. Quicksort with the first item as the pivot and a partition that keeps the input order of each part compares 5 with each other item, then 3 with 1, 4 and 2, then 8 with 7, 9 and 6, then 1 with 2, and 7 with 6: also 16 comparisons, the same pairs.

## Correctness

The insert keeps the binary search tree property: for each node $v$, the keys in the left subtree of $v$ are less than $v.key$, and the keys in the right subtree are at least $v.key$. A new item goes left at $v$ exactly when it is less than $v.key$, so it lands in the correct subtree of each node on its path. An inorder traversal of a tree with this property visits the keys in non-decreasing order: by induction on the tree, it lists the left subtree in order, all of whose keys are less than the root, then the root, then the right subtree in order, all of whose keys are at least the root. The tree holds each item once, so lines L5 and L6 write a sorted permutation of the input into $A$. The full proof is below.

## Complexity

**Comparisons.** The insert of an item makes one comparison for each node on its path, so the total number of comparisons is the internal path length of the final tree: the sum of the depths of the nodes. The traversal makes no comparisons.

**The link with quicksort.** The root is $A[0]$, and every other item is compared with it, as with the pivot of quicksort that takes the first item. The items less than $A[0]$ go to the left subtree in their input order, and they form the same subproblem as the left part of a stable partition. So tree sort compares the same pairs as this quicksort, and the counts are equal. Knuth (Section 6.2.2) and Sedgewick and Wayne (Section 3.2) note this link.

**The average.** For a random permutation of distinct keys, the mean number of comparisons is that of quicksort:

$$2(n+1)H_n - 4n \approx 2n \ln n \approx 1.386\, n \lg n,$$

where $H_n$ is the $n$-th [harmonic number](/harmonic-series/). For $n = 1000$ the mean is about 10,986, and five random inputs gave 10,990 on average. The height of a random binary search tree is $O(\log n)$ with high probability (CLRS, Section 12.4); for $n = 100{,}000$ a random input gave height 37.

**The worst case.** A sorted or reversed input makes the tree a path, and the $i$-th insert makes $i$ comparisons, $n(n-1)/2$ in total. So the time is $\Theta(n^2)$.

**Balanced trees.** A [red-black tree](/red-black-tree/) or an [AVL tree](/avl-tree/) has height $O(\log n)$ after each insert, so tree sort with one takes $O(n \log n)$ time in the worst case.

**Space.** Each item gets a node with two links, so the extra space is $\Theta(n)$, plus the stack of the traversal, which is as deep as the tree.

| claim | model and case | bound |
|---|---|---|
| time | comparison model, average over random permutations | $\Theta(n \log n)$, with about $1.386\, n \lg n$ comparisons |
| time | comparison model, worst (sorted input) | $\Theta(n^2)$, with $n(n-1)/2$ comparisons |
| time | with a balanced tree, worst | $O(n \log n)$ |
| extra space | | $\Theta(n)$ |

## Properties

- **Stable.** An item equal to a key goes right, so it is visited after the earlier equal items. Equal items come out in input order.
- **Not in place.** The tree needs $\Theta(n)$ extra nodes.
- **Online.** The items can be inserted as they arrive, and the sorted order can be read at any time.
- **Not adaptive.** A sorted input is the worst case of the plain tree. A [splay tree](/splay-tree/) makes the method adaptive to some kinds of presorted input.
- **Not oblivious.** The comparisons depend on the data, as in quicksort.

## Variants and improvements

- **A balanced tree.** Use a [red-black tree](/red-black-tree/), an [AVL tree](/avl-tree/) or a [treap](/treap/) to get $O(n \log n)$ time in the worst case, or in expectation for the treap.
- **A random order.** Shuffle the input first. Then the tree is a [random binary search tree](/random-binary-search-tree/), and the expected time is $O(n \log n)$ on each input, as with [randomized quicksort](/randomized-quicksort/).
- **Splay sort.** Insert into a [splay tree](/splay-tree/). The time is $O(n \log n)$ in the worst case, and much less on input that is close to sorted.
- **Counts for equal keys.** Store each distinct key once with a count or a list of its items. This makes inputs with many equal keys cheap.
- **A sorted container.** In many programs the tree is kept anyway, as a sorted map or set, and the sort is a side effect: the keys are in order at any time.

## When to use it

Use tree sort when the items arrive one at a time and the order must be available at each moment, or when a balanced tree such as a sorted map already holds the data. For a one-time sort of an array, [merge sort](/merge-sort/), [quicksort](/quicksort/) or [heapsort](/heapsort/) are faster: they use less memory and have better locality than a tree of separate nodes.

## Pitfalls

- **Sorted input.** With a plain tree, sorted or nearly sorted input gives a path and quadratic time. Use a balanced tree or shuffle the input.
- **Deep recursion.** A recursive insert or traversal on a path of $n$ nodes uses $n$ stack frames, which overflows for large $n$. Use loops, as in the implementation.
- **Dropping duplicates.** A tree used as a set ignores an item whose key is already present. A sort must keep each item, so equal keys must go to one side.
- **Equal keys on the wrong side.** If equal keys go left, the sort is still correct but no longer stable.

## Implementations

## History

Sorting by insertion into a binary tree goes back to the first studies of binary search trees in the late 1950s and early 1960s. Knuth treats tree insertion in Section 6.2.2 and shows that the cost of building a random tree is the same as the cost of quicksort, because the two methods compare the same pairs. CLRS gives the method as an exercise in its chapter on binary search trees.

## References
