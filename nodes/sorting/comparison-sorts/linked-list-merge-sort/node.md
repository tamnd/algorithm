---
tag: NEN2CA
kind: algorithm
slug: linked-list-merge-sort
name: Linked-list merge sort
aliases:
- Linked-list sort
- list merge sort
area: sorting/comparison-sorts
level: core
summary: Mergesort on a linked list that splits and merges nodes by relinking them, needing no auxiliary array.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of nodes}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(1)}
properties: {stable: true, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [merge-sort, singly-linked-list]
see_also: [natural-merge-sort, timsort, doubly-linked-list, heapsort, stable-sort, in-place-merge-sort]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.4, Sorting by merging (Algorithm L, list merge sort, which merges runs by changing link fields)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.2, Mergesort (bottom-up mergesort, and the exercise on sorting a linked list with a natural mergesort)
---

Linked-list merge sort is [merge sort](/merge-sort/) on a [singly linked list](/singly-linked-list/). The merge of two sorted lists needs no buffer on a list: it relinks the nodes, taking the smaller head each time. This page uses the bottom-up form. Pass 1 merges neighbouring single nodes into sorted runs of 2, pass 2 merges these into runs of 4, and so on, until one pass makes a single merge. It makes at most $n \lceil \lg n \rceil$ comparisons, uses $O(1)$ extra space, and is stable. It is the standard way to sort a linked list, where [quicksort](/quicksort/) and [heapsort](/heapsort/) are awkward because they need random access.

## In plain words

Think of a chain of paper clips, each with a number. You may unhook and rehook clips, but you cannot jump to the middle of the chain; you must walk along it.

First walk the chain and fix each pair of neighbours: hook the smaller one first. Now the chain is made of sorted pieces of 2. Walk it again and join each two neighbouring pieces into one sorted piece of 4. To join two sorted pieces, look at the first clip of each, take the smaller one, and hook it to the end of the new piece. Then walk again for pieces of 8, and so on. When a walk joins only one pair, the whole chain is one sorted piece.

## The problem

The input is a singly linked list of $n$ nodes, each with a key from a total order and a pointer to the next node. The output is the same nodes, relinked so that the keys are in non-decreasing order, and the head of the new list. This is the [sorting problem](/sorting-problem/) on a list. The keys are not copied.

## The algorithm

A dummy node $D$ stands before the head, so the first node of the output needs no special case. A *run* is a block of $w$ consecutive nodes, or fewer at the end of the list.

```pseudo id=main
LIST-MERGE-SORT(head)                       ▷ head ≠ nil
L1  w ← 1
L2  loop
L3      tail ← D, p ← head, merges ← 0
L4      while p ≠ nil do                    ▷ merge the run at p with the run after it
L5          merges ← merges + 1
L6          q ← p, a ← 0; while a < w and q ≠ nil do q ← q.next, a ← a + 1
L7          b ← w                           ▷ the left run has a nodes, the right run at q has at most b
L8          while a > 0 or (b > 0 and q ≠ nil) do
L9              if a = 0 or (b > 0 and q ≠ nil and q.key < p.key) then e ← q, q ← q.next, b ← b − 1
L10             else e ← p, p ← p.next, a ← a − 1
L11             tail.next ← e, tail ← e
L12         p ← q                           ▷ the start of the next pair of runs
L13     tail.next ← nil
L14     if merges ≤ 1 then return D.next
L15     head ← D.next, w ← 2w
```

Line L6 walks $w$ nodes from $p$ to find the start $q$ of the right run, and counts the length $a$ of the left run. Lines L8 to L11 merge the two runs. Line L9 takes the right node only when its key is strictly smaller, so on equal keys the left node goes first, which makes the sort stable. After the merge, $q$ points to the first node after the right run, so line L12 goes on from there. Each node is appended to the output exactly once in a pass, by line L11. Line L13 ends the list. A pass with one merge has merged two runs that together are the whole list, so line L14 returns.

## Example

Sort the list $5 \to 1 \to 4 \to 2 \to 8 \to 0 \to 3$.

| pass | $w$ | the runs merged | the list after the pass | comparisons |
|---|---|---|---|---|
| 1 | 1 | (5, 1), (4, 2), (8, 0), (3) | 1 5 2 4 0 8 3 | 3 |
| 2 | 2 | (1 5, 2 4), (0 8, 3) | 1 2 4 5 0 3 8 | 5 |
| 3 | 4 | (1 2 4 5, 0 3 8) | 0 1 2 3 4 5 8 | 6 |

In pass 1, the last run $(3)$ has no right partner, so line L8 copies it with no comparison. In pass 3, the merge compares $0 < 1$, then 3 with 1, 2 and 4, then 8 with 4 and 5, and then appends 8 alone. Pass 3 makes one merge, so the sort stops. The run makes 14 comparisons. The bound is $n \lceil \lg n \rceil = 7 \cdot 3 = 21$.

## Correctness

Each pass keeps this [loop invariant](/loop-invariant/):

> At the start of a pass with width $w$, the list holds all the input nodes, and each block of $w$ consecutive nodes from the head, the last block possibly shorter, is sorted, and keeps equal keys in their input order.

It holds for $w = 1$, since a block of one node is sorted. A pass merges the blocks in pairs from the left. A merge of two sorted runs gives a sorted run of their nodes, and taking the left node on a tie keeps equal keys in order. So after the pass each block of $2w$ nodes is sorted, and the invariant holds for $2w$. A pass with $m$ merges has $n > 2w(m-1)$, so the number of merges is $\lceil n / 2w \rceil$. It is at most 1 when $2w \ge n$, and then the single merged block is the whole list, which is sorted. Since $w$ doubles in each pass, this happens after $\lceil \lg n \rceil$ passes for $n \ge 2$. The full proof is below.

## Complexity

- **Passes.** $\lceil \lg n \rceil$ for $n \ge 2$, and 1 for $n = 1$. Each pass walks the list twice: once in line L6 to find the right runs and once in the merges. So each pass takes $\Theta(n)$ time, and the total is $\Theta(n \log n)$ on every input, even a sorted one.
- **Comparisons.** A merge of runs with $a$ and $b$ nodes makes at most $a + b - 1$ comparisons, and at least $\min(a, b)$. So a pass makes fewer than $n$, and the sort makes at most $n \lceil \lg n \rceil$. On a sorted list each merge stops comparing when the left run is used up, so each pass makes about $n/2$ comparisons, and the sort about $\frac{1}{2} n \lg n$. In the worst case it makes the same count as array merge sort on a power of two, $n \lg n - n + 1$.
- **Space.** $\Theta(1)$ extra: a few pointers and counters, and one dummy node. There is no recursion and no buffer.

## Properties

- **Stable.** Line L9 takes the right node only when its key is strictly smaller.
- **In place on the list.** It changes only the next pointers, and needs $O(1)$ extra space. The array form of merge sort needs a buffer of $n/2$ to $n$ items.
- **Not adaptive.** It makes $\lceil \lg n \rceil$ passes on every input. The natural form, below, adapts to runs.
- **Only sequential access.** It reads each list from the front, so it also works on data that can only be scanned, such as tapes or streams with two outputs, which is the origin of merge sorting.

## Variants and improvements

- **Top-down form.** Split the list into halves with a slow pointer and a fast pointer, as in [Floyd's cycle detection](/floyd-cycle-detection/), sort each half recursively, and merge. It needs a recursion stack of depth $\lceil \lg n \rceil$, and walks the list once more at each level to find the middle.
- **[Natural merge sort](/natural-merge-sort/).** Start from the maximal ascending runs of the input instead of single nodes. A sorted list is then one run, and the sort takes $\Theta(n)$ time. Knuth's Algorithm L can start this way, and Sedgewick and Wayne set it as an exercise.
- **Merging with a table of lists.** Keep an array of $\lg n$ sorted lists, where slot $k$ holds a list of $2^k$ nodes or is empty, and add the nodes one at a time like adding 1 to a binary counter. This makes one scan of the input, and is how some libraries sort lists.
- **[Doubly linked lists](/doubly-linked-list/).** Sort with the next pointers only, and then set the previous pointers in one walk.
- **[Timsort](/timsort/).** For arrays, a run-based merge sort with a buffer gives the adaptivity of the natural form and better cache use.

## When to use it

Use it to sort a linked list, for example the list sort of a standard library or the chains of a hash table. It is stable, needs no extra memory, and makes few comparisons. For data in an array, an array sort is faster, because a walk of a linked list misses the cache at many nodes. If the list is long and the time matters, copying the keys into an array, sorting it, and relinking can be faster than any list sort.

## Pitfalls

- **Losing the end of the list.** If a pass does not set $tail.next \leftarrow nil$ in line L13, the last node may still point into the old list, and the next pass walks a cycle.
- **Counting the right run wrongly.** The right run has at most $w$ nodes, and may be shorter at the end of the list. The test $q \ne nil$ in lines L8 and L9 handles this.
- **Taking the right node on ties.** With $q.key \le p.key$ in line L9, the sort is still correct but not stable.
- **Recursion on a long list.** A top-down form that splits off one node at a time, or a recursive merge that calls itself for each node, has a recursion depth of $\Theta(n)$ and overflows the stack on long lists. The merge must be a loop.

## Implementations

## History

Merge sorting started with data on tapes and other sequential stores, where it was the only efficient method. John von Neumann described merging for the EDVAC in 1945. Knuth gives the list merge sort as Algorithm L in Section 5.2.4, where the links of the records replace the moves of the records.

## References
