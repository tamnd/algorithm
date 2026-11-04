---
tag: B8EJVN
kind: algorithm
slug: skyline-sweep
name: Skyline sweep
aliases:
- skyline algorithm
area: techniques/sweep-line
level: core
summary: Sweep over building edges with a max-heap of active heights to output the skyline.
solves: [skyline-problem]
model: comparison-model
complexity:
  vars: {n: the number of buildings}
  time: {worst: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [skyline-problem, sweep-line-technique, binary-heap, priority-queue]
see_also: [event-queue, sweep-status-structure, sweep-invariant, degeneracy-in-sweeps, lazy-deletion, rectangle-union-sweep, sliding-window-maximum-deque, merge-sort]
sources:
  - book: isbn:9780201120370
    title: Udi Manber, Introduction to Algorithms, A Creative Approach, Addison-Wesley, 1989
    locator: Chapter 5, Section 5.6, A divide-and-conquer algorithm, the skyline problem (the problem and the merge of two skylines)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 2, Section 2.1 (the plane sweep paradigm, with an event queue and a status structure)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 6, Section 6.5 (max-priority queues on a binary heap)
---

The skyline sweep solves the [skyline problem](/skyline-problem/) with a [sweep line](/sweep-line-technique/) that moves from left to right over the left and right ends of the buildings, and a max-[priority queue](/priority-queue/) of the heights of the buildings that the line crosses. At each event coordinate it reads the largest active height and outputs a key point when that height changes. With a [binary heap](/binary-heap/) and [lazy deletion](/lazy-deletion/) it takes $\Theta(n \log n)$ time and $\Theta(n)$ extra space for $n$ buildings, which is optimal in the worst case in the [algebraic computation tree](/algebraic-computation-tree/) model. That model includes every algorithm of the [comparison model](/comparison-model/).

## In plain words

Picture the buildings drawn on a long strip of paper, and a vertical ruler that slides from the left edge to the right edge. The outline can change only where a building starts or ends, so the ruler stops only there. At each stop you keep a pile of the buildings that the ruler touches now, with the tallest on top. A building that starts goes on the pile. A building that ended is thrown away, but only when it comes to the top: until then it does no harm, because a taller building that is still standing hides it. After you handle every building that starts or ends at a stop, the top of the pile is the height of the outline there. You write down a point each time this height is different from the last height you wrote.

## The problem

The input is a list of $n$ buildings $(L_i, R_i, H_i)$ with $L_i < R_i$ and $H_i > 0$. Let $f(x) = \max\{H_i : L_i \le x < R_i\}$, with $f(x) = 0$ when no building covers $x$. The output is the shortest list of key points $(x_1, h_1), \ldots, (x_m, h_m)$ with $x_1 < \cdots < x_m$ such that $f(x) = h_j$ on $[x_j, x_{j+1})$, $f(x) = 0$ for $x < x_1$ and for $x \ge x_m$, and $h_j \ne h_{j+1}$. The [skyline problem](/skyline-problem/) page gives the variants and the bounds.

## The algorithm

The [event points](/event-point/) are the distinct values among all $L_i$ and $R_i$. The [status structure](/sweep-status-structure/) is a max-heap $Q$ of pairs $(H_i, R_i)$, ordered by $H_i$.

```pseudo id=main
SKYLINE-SWEEP(B[1 .. n])                    ▷ B[i] = (L_i, R_i, H_i)
L1  X ← the distinct values of {L_i} ∪ {R_i}, in increasing order
L2  sort B by L; i ← 1
L3  Q ← an empty max-heap of pairs (H, R) keyed by H; out ← empty list; prev ← 0
L4  for each x in X, in increasing order do
L5      while i ≤ n and B[i].L = x do
L6          INSERT(Q, (B[i].H, B[i].R)); i ← i + 1
L7      while Q is not empty and R of MAX(Q) ≤ x do
L8          EXTRACT-MAX(Q)                      ▷ lazy deletion of an expired building
L9      h ← H of MAX(Q) if Q is not empty, else 0
L10     if h ≠ prev then
L11         append (x, h) to out; prev ← h
L12 return out
```

Lines L5 and L6 add every building that starts at $x$. Lines L7 and L8 remove expired entries, but only from the top of the heap. An entry with $R \le x$ that is not on top stays in the heap. It is harmless: the top entry is valid and at least as tall, so the expired entry cannot be the answer. It is removed later, at the first event where it reaches the top. Line L9 reads the height of the outline only after all the events at $x$ are handled, and lines L10 and L11 output a point only when the height changes.

## Example

Run SKYLINE-SWEEP on the buildings $(2, 9, 10)$, $(3, 7, 15)$, $(5, 12, 12)$, $(15, 20, 10)$ and $(19, 24, 8)$. The event coordinates are $X = [2, 3, 5, 7, 9, 12, 15, 19, 20, 24]$. A heap entry is written as $H{:}R$, and the heap column lists the entries after line L8, from the tallest.

| $x$ | inserted (L6) | extracted (L8) | heap after L8 | $h$ | output |
|---|---|---|---|---|---|
| 2 | 10:9 | | 10:9 | 10 | $(2, 10)$ |
| 3 | 15:7 | | 15:7, 10:9 | 15 | $(3, 15)$ |
| 5 | 12:12 | | 15:7, 12:12, 10:9 | 15 | |
| 7 | | 15:7 | 12:12, 10:9 | 12 | $(7, 12)$ |
| 9 | | | 12:12, 10:9 | 12 | |
| 12 | | 12:12, 10:9 | empty | 0 | $(12, 0)$ |
| 15 | 10:20 | | 10:20 | 10 | $(15, 10)$ |
| 19 | 8:24 | | 10:20, 8:24 | 10 | |
| 20 | | 10:20 | 8:24 | 8 | $(20, 8)$ |
| 24 | | 8:24 | empty | 0 | $(24, 0)$ |

The output is $[(2, 10), (3, 15), (7, 12), (12, 0), (15, 10), (20, 8), (24, 0)]$. At $x = 9$ the building $(2, 9, 10)$ ends, but its entry 10:9 is under 12:12, so the lazy deletion keeps it. At $x = 12$ the entry 12:12 leaves the top, and 10:9 comes to the top with $9 \le 12$, so it leaves too.

## Correctness

The [sweep invariant](/sweep-invariant/) is: after line L8 at the event $x$, the heap holds every building $i$ with $L_i \le x < R_i$, each entry in the heap has $L \le x$, and the top entry, if there is one, has $R > x$. Then the top is an active building that is at least as tall as each active building, so line L9 sets $h = f(x)$. Between two consecutive events no building starts or ends, so $f$ is constant on $[x, x')$. Line L10 outputs exactly the events where $f$ changes, which gives the shortest list. The full proof is below.

## Complexity

- **Sorting.** Lines L1 and L2 sort $2n$ and $n$ values: $O(n \log n)$ comparisons and time.
- **Heap operations.** Line L6 runs exactly $n$ times in total, once per building. Each run of line L8 removes an entry that line L6 inserted, so line L8 runs at most $n$ times in total over the whole sweep. The heap never holds more than $n$ entries, so each INSERT and EXTRACT-MAX costs $O(\log n)$. Lines L9 to L11 cost $O(1)$ for each of the at most $2n$ events. The total is $O(n \log n)$ in the worst case.
- **Lower bound.** Each algorithm in the [algebraic computation tree](/algebraic-computation-tree/) model, and so each comparison-based algorithm, needs $\Omega(n \log n)$ time in the worst case, by the reduction from [element distinctness](/element-distinctness/) on the [skyline problem](/skyline-problem/) page. So the worst-case time is $\Theta(n \log n)$.
- **Space.** $X$, the sorted copy of $B$ and the heap use $\Theta(n)$ extra space. The output has at most $2n$ points, one for each event coordinate.

## Properties

- **Output in order.** The key points come out sorted by $x$, so a caller can stream them.
- **Comparison-based.** The algorithm only compares coordinates and heights. It works for integers, for exact rationals and for floating-point values without any arithmetic on them.
- **Not online.** It needs all the buildings before it starts, because it sorts the events first.
- **Deterministic.** Ties in the heap between equal heights do not change $h$, so the output does not depend on how the heap breaks ties.

## Variants and improvements

- **Balanced tree or multiset instead of a heap.** Keep a [balanced binary search tree](/balanced-binary-search-tree/) of the active heights with counts, insert $H_i$ at $L_i$ and delete one copy of $H_i$ at $R_i$. This is eager deletion with the same $O(n \log n)$ bound, and it also supports a query of the current maximum in $O(\log n)$.
- **Indexed heap.** An [indexed priority queue](/indexed-priority-queue/) deletes the building at $R_i$ by its index, so the heap holds only active buildings.
- **Divide and conquer.** Split the buildings into two halves, compute both skylines, and merge them in linear time with a walk like the merge of [merge sort](/merge-sort/). This takes $O(n \log n)$ time and needs no heap. The [skyline problem](/skyline-problem/) page describes the merge.
- **Sorted and non-nested input.** If the buildings are sorted by $L$ and the order by $R$ is the same, the active buildings form a first-in first-out queue. A [monotonic deque](/monotonic-deque/) of heights then gives the maximum in $O(1)$ amortized time per event, and the whole sweep takes $O(n)$ time after the sort, as in the [sliding window maximum](/sliding-window-maximum-deque/).
- **Area under the skyline.** Add $h \cdot (x' - x)$ between consecutive events to get the area of the union of the buildings, a special case of the [area of a union of rectangles](/area-of-union-of-rectangles/).

## When to use it

Use the heap sweep when the input is a plain list of buildings and you need the skyline once: it is short, it uses only a library heap, and it is optimal. Use the divide-and-conquer merge when you already have skylines to combine, for example two skylines from two parts of a city, because one merge costs $O(m_1 + m_2)$ for skylines with $m_1$ and $m_2$ points. For rectangles that do not stand on a common baseline, use the [rectangle union sweep](/rectangle-union-sweep/) with a [segment tree](/segment-tree/) instead.

## Pitfalls

- **Reading the height after each event, not after each coordinate.** If the code handles one event at a time and checks the height after each one, a building that ends at $x$ and another that starts at $x$ give two points at $x$. For $(0, 2, 5)$ and $(2, 4, 3)$, handling the end first outputs $(2, 0)$ and then $(2, 3)$, a piece of zero width. Lines L5 to L8 handle every event at $x$ before line L9 reads the height.
- **Adjacent buildings of the same height.** For $(0, 2, 5)$ and $(2, 4, 5)$ the correct output is $[(0, 5), (4, 0)]$. Code that outputs a point at every event where a building ends or starts outputs $(2, 5)$ as well. Line L10 compares with the last output height, not with the event type.
- **A wrong test for expiry.** The test in line L7 must be $R \le x$, because a building covers $[L, R)$. With $R < x$, a building that ends at $x$ still counts at $x$, and the drop to the next height is reported one event late.
- **Equal heights.** Two buildings of the same height can both be in the heap. Line L10 compares heights, so a change of the top building with no change of height outputs nothing, which is right.
- **Assuming the heap holds only active buildings.** With lazy deletion the heap size is not the number of active buildings, and an entry below the top can be expired. Only the top is guaranteed valid after line L8.

## Implementations

## History

Manber presents the skyline problem in Section 5.6 of his 1989 book as an example of divide and conquer, and solves it by merging two skylines. The heap sweep on this page applies the general plane sweep method, with an event queue and a status structure, which de Berg et al. describe in Section 2.1.

## References
