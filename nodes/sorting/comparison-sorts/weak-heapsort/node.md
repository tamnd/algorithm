---
tag: KTRHK1
kind: algorithm
slug: weak-heapsort
name: Weak heapsort
aliases:
- Dutton's weak heapsort
area: sorting/comparison-sorts
level: research
summary: Heapsort variant using weak heaps, needing at most n log n + 0.1n comparisons.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 1993
  people: [Ronald D. Dutton]
  note: Dutton introduced the weak heap and weak heapsort in BIT in 1993; Edelkamp and Wegener gave the exact worst case and studied the average in 2000.
prereqs: [weak-heap, heapsort]
see_also: [weak-heap, heapsort, binary-heap, sift-down, smoothsort, tournament-sort, ford-johnson-algorithm, comparison-sort-lower-bound]
sources:
  - paper: Ronald D. Dutton, Weak-heap sort, BIT 33(3), 1993
    locator: the definition of the weak heap with reverse bits, the algorithm, and the bound of n⌈lg n⌉ − 2^⌈lg n⌉ + n − 1 comparisons
  - paper: Stefan Edelkamp and Ingo Wegener, On the performance of weak-heapsort, STACS 2000, Lecture Notes in Computer Science 1770
    locator: the exact worst case, the inputs that reach it, and the average number of comparisons
  - paper: "Stefan Edelkamp, Amr Elmasry and Jyrki Katajainen, The weak-heap data structure: variants and applications, Journal of Discrete Algorithms 16, 2012"
    locator: the survey of weak heaps, the operations join and the distinguished ancestor, and weak heapsort
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3, Sorting by selection (heapsort and its number of comparisons, for comparison)
---

Weak heapsort is a variant of [heapsort](/heapsort/) by Ronald Dutton (1993) that uses a [weak heap](/weak-heap/) instead of a [binary heap](/binary-heap/). A weak heap only asks each node to be at least the items of its *right* subtree, and one extra bit per node says which child counts as right. This weaker order is cheap to build and cheap to repair: one comparison per level, never two. So weak heapsort makes at most $n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + n - \lceil \lg n \rceil$ comparisons, which is less than $n \lg n + 0.087n$, close to the lower bound of $\lg n! \approx n \lg n - 1.44n$. Standard heapsort makes about $2 n \lg n$. The cost is $n$ extra bits, and the sort is not stable.

## In plain words

In a normal heap, each parent must be at least both of its children. To repair it, you compare a parent with two children at each level.

A weak heap asks less. Each parent only needs to be at least everything below its right child. The left side can be in any order. Each node also has a switch that can swap the roles of its two sides at no cost. Two weak heaps join with one comparison: the larger top wins, and if the order was wrong, the switch flips.

The sort builds a weak heap, so the largest item is at the top. It moves that item to the end and repairs the heap along one path, with one comparison per step, until all items are in place. Because it saves a comparison at each step, it makes about half as many comparisons as heapsort.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array, with its items in non-decreasing order. This is the [sorting problem](/sorting-problem/). Weak heapsort works on the array, with an array $r$ of $n$ bits as extra memory.

## The algorithm

**The weak heap.** Node $i$ has the two children $2i + r[i]$ (the left child) and $2i + 1 - r[i]$ (the right child). The root 0 has only the right child 1, since $r[0] = 0$ and its left child would be itself. Flipping $r[i]$ swaps the two subtrees of $i$ without moving any item. The *distinguished ancestor* $d(j)$ of a node $j \ge 1$ is found by climbing from $j$ while the node is a left child, then taking one more step up: so $j$ is in the right subtree of $d(j)$. The array is a weak heap when $A[d(j)] \ge A[j]$ for each $j \ge 1$. Then each node is at least all items of its right subtree, and the root is the largest item.

**Join.** JOIN$(i, j)$, for $i = d(j)$, makes one comparison: if $A[i] < A[j]$, it swaps $A[i]$ and $A[j]$ and flips $r[j]$. After it, $A[i]$ is the larger of the two items.

```pseudo id=main
WEAK-HEAPSORT(A)                           ▷ n is the length of A
L1  r[0 .. n − 1] ← 0
L2  for j ← n − 1 down to 1 do             ▷ build the weak heap, bottom up
L3      JOIN(d(j), j)
L4  for m ← n − 1 down to 2 do             ▷ the heap is A[0 .. m]
L5      swap A[0] and A[m]                 ▷ the largest item goes to its place
L6      x ← 1;  while 2x + r[x] < m do x ← 2x + r[x]    ▷ the left spine of node 1
L7      while x > 0 do
L8          JOIN(0, x);  x ← ⌊x / 2⌋
L9  if n ≥ 2 then swap A[0] and A[1]
```

Lines L2 and L3 build the weak heap with $n - 1$ comparisons. Each step of line L4 removes the root to index $m$, which leaves the heap $A[0 \ldots m-1]$ with a wrong root. The new root must be compared with the nodes $d(x) = 0$, which are the nodes on the *left spine* of node 1: node 1, its left child, the left child of that, and so on. Line L6 walks down this spine to its last node, and lines L7 and L8 join each spine node with the root from the bottom up, one comparison each. The last swap at line L9 places the two remaining items, which the heap property already orders.

## Example

Sort $A = [5, 1, 4, 2, 8, 3, 7, 6]$.

**The build.** For $j = 7, 6, \ldots, 1$, the joins compare $A[d(j)]$ with $A[j]$. Three of them swap: $j = 7$ with $d = 3$ (items 2 and 6), $j = 6$ with $d = 1$ (items 1 and 7), and $j = 4$ with $d = 0$ (items 5 and 8). Each swap flips $r[j]$. After 7 comparisons the array is $[8, 7, 4, 6, 5, 3, 1, 2]$ with $r[4] = r[6] = r[7] = 1$.

**The sort.** Each row swaps the root into index $m$ and joins the root with the spine of node 1, from the bottom up.

| $m$ | the spine | the array after the joins | comparisons so far |
|---|---|---|---|
| 7 | 4, 2, 1 | 7 5 4 6 2 3 1 \| 8 | 10 |
| 6 | 3, 1 | 6 5 4 1 2 3 \| 7 8 | 12 |
| 5 | 3, 1 | 5 3 4 1 2 \| 6 7 8 | 14 |
| 4 | 2, 1 | 4 3 2 1 \| 5 6 7 8 | 16 |
| 3 | 2, 1 | 3 2 1 \| 4 5 6 7 8 | 18 |
| 2 | 1 | 2 1 \| 3 4 5 6 7 8 | 19 |

Line L9 swaps the last two items, and the result is $1, 2, \ldots, 8$ after 19 comparisons. For $m = 7$ the spine starts at node 1 and goes to its left child 2 (as $r[1] = 0$) and then to $2 \cdot 2 + r[2] = 4$; the next step, $2 \cdot 4 + r[4] = 9$, is outside the heap. The lower bound for 8 items is $\lceil \lg 8! \rceil = 16$ comparisons.

## Correctness

The proof uses this invariant for the build: after the step for $j$, each node $s \ge j$ satisfies $A[d(s)] \ge$ each item of the subtree of $s$. A step JOIN$(d(j), j)$ keeps it: before the step, the items of the right subtree of $j$ are at most $A[j]$, and the items of its left subtree are at most $A[d(j)]$, by the invariant for the children of $j$. The join puts the larger of $A[d(j)]$ and $A[j]$ at $d(j)$, and if it swaps, flipping $r[j]$ makes the old left subtree, whose items are at most the item that moves down, the new right subtree. After the build, $j = 1$ gives a weak heap, and $A[0]$ is the largest item. In the sort, removing the root breaks the invariant only for the nodes $s$ with $d(s) = 0$, the left spine of node 1, and lines L7 and L8 repair them from the bottom up by the same join step. So each step of line L4 moves the largest item of $A[0 \ldots m]$ to index $m$. The full proof is below.

## Complexity

**Comparisons.** The build makes $n - 1$ comparisons. When the heap is $A[0 \ldots m-1]$ after line L5, the spine nodes $1 = s_1, s_2, \ldots, s_t$ satisfy $s_i \ge 2^{i-1}$ and $s_t \le m - 1$, so the spine has $t \le \lceil \lg m \rceil$ nodes, one comparison each. With $\sum_{m=1}^{n} \lceil \lg m \rceil = n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + 1$, the total is at most

$$(n - 1) + \sum_{m=2}^{n-1} \lceil \lg m \rceil = n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + n - \lceil \lg n \rceil.$$

This is within Dutton's bound $n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + n - 1$. Writing $n = 2^{\lceil \lg n \rceil} x$ with $1/2 < x \le 1$, the bound minus $n \lg n$ is $n(1 - \lg x - 1/x)$, which is largest at $x = \ln 2$, where it is about $0.0861 n$. So weak heapsort makes fewer than $n \lg n + 0.087 n$ comparisons. An exhaustive test of all permutations of up to 8 items shows that the implementation on this page reaches the bound above exactly; Edelkamp and Wegener (2000) show that the worst case is reached for all $n$.

**Measured counts.**

| input | $n = 1000$ | $n = 10^5$ |
|---|---|---|
| sorted | 8,977 | 1,568,929 |
| reversed | 9,496 | 1,612,121 |
| random | 9,484 | 1,617,756 |
| the worst-case bound | 9,975 | 1,668,927 |
| $\lg n!$ | 8,529 | 1,516,704 |

On random input the mean is close to $n \lg n - 0.46 n$ (mean of 50 runs: 9,505 for $n = 1000$ and 9,763 for $n = 1024$). This is about 1.0 comparisons per item above the lower bound $\lg n!$. Standard heapsort makes about $2 n \lg n$ comparisons, and bottom-up heapsort about $n \lg n + O(n)$ on average but $1.5 n \lg n$ in the worst case.

**Time and space.** Each comparison comes with $O(1)$ other work, and the climbs to the distinguished ancestors in the build take $O(n)$ steps in total, since a node is passed only by the climbs from the nodes on the left spine below it, at most its height many, and the heights of the nodes of a complete binary tree add up to $O(n)$. So the time is $\Theta(n \log n)$. The extra space is the $n$ bits of $r$, plus $O(1)$ words.

| claim | model and case | bound |
|---|---|---|
| comparisons | comparison model, worst | $n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + n - \lceil \lg n \rceil < n \lg n + 0.087 n$ |
| time | worst, average and best | $\Theta(n \log n)$ |
| extra space | | $\Theta(n)$: $n$ bits and $O(1)$ words |

## Properties

- **Not stable.** The joins swap items over long distances.
- **Almost in place.** Besides the array, it needs the $n$ reverse bits. With a word of $w$ bits, this is $n / w$ words, but it is not $O(1)$.
- **Not adaptive.** Each phase of line L4 does a full walk down the spine, whatever the order. On sorted input it saves only about 3 percent of the comparisons.
- **Few comparisons.** Among heap-based sorts it makes the fewest comparisons in the worst case. It is close to the [merge insertion algorithm of Ford and Johnson](/ford-johnson-algorithm/), which makes the fewest known in the worst case for small $n$ but is hard to use for large $n$.

## Variants and improvements

- **[Heapsort](/heapsort/).** The binary heap needs two comparisons per level to sift down, so about $2 n \lg n$ in all. Bottom-up heapsort first walks down the path of larger children with one comparison per level and then climbs up, which brings the average close to $n \lg n$ but not the worst case.
- **Relaxed weak heapsort.** Edelkamp and Stiegeler (2002) keep an index array of $n$ words and reach at most $n \lg n - 0.9 n$ comparisons.
- **Weak heaps as priority queues.** The same structure gives a [priority queue](/priority-queue/) with $O(\log n)$ insert and delete-min and few comparisons; see [weak heap](/weak-heap/).
- **[Tournament sort](/tournament-sort/).** Also close to $n \lg n$ comparisons, but it needs $\Theta(n)$ extra words.

## When to use it

Use weak heapsort when comparisons are much more costly than moves, for example for long strings or for keys that are compared by a slow function, and when the worst case matters and memory is limited. With cheap comparisons, a quicksort or introsort is faster in practice, because weak heapsort jumps around the array and has poor cache behaviour. When stability or adaptivity matter, use a merge sort such as [Timsort](/timsort/).

## Pitfalls

- **The distinguished ancestor.** Climb while $j$ is a *left* child, which is the test $(j \bmod 2) = r[\lfloor j/2 \rfloor]$, and then take the parent. Using the plain parent instead gives a binary-heap order that the joins do not maintain.
- **Flip the bit of $j$, not of $i$.** A join that swaps must flip $r[j]$, so that the old left subtree of $j$, whose items are at most the new $A[j]$, becomes its right subtree.
- **The order of the repair.** In the sort phase the joins must go from the bottom of the spine up to node 1. From the top down, the root does not see the items deep in the spine.
- **The end of the spine.** The walk of line L6 must stop at the last node below $m$, the current size of the heap; a test against $n$ reads items that are already sorted.

## Implementations

## History

Dutton introduced weak heaps and weak heapsort in 1993, in BIT, with the bound of $n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + n - 1$ comparisons. Edelkamp and Wegener analysed it again in 2000: they gave the exact worst case and the inputs that reach it, and they studied the average number of comparisons. Edelkamp, Elmasry and Katajainen surveyed weak heaps and their uses in priority queues and sorting in 2012.

## References
