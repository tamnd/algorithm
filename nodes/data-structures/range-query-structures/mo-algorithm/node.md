---
tag: S9FYEP
kind: algorithm
slug: mo-algorithm
name: Mo's algorithm
aliases:
- Mo's algorithm for offline range queries
- square-root ordering of queries
area: data-structures/range-query-structures
level: advanced
summary: Sorts offline queries by blocks and moves a window across the array in O(n sqrt q) total.
solves: [range-distinct-count-query]
model: word-ram
complexity:
  vars: {n: the length of the array, q: the number of queries}
  time: {worst: O(n √q + q log q)}
  space: {extra: O(n + q)}
properties: {deterministic: true, online: false, recursive: false}
prereqs: [square-root-decomposition, offline-query-processing, two-pointers]
see_also: [mo-algorithm-with-updates, range-distinct-count-query, range-mode-query, hilbert-curve, sliding-window, offline-algorithm, persistent-segment-tree]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook (free PDF edition)
    locator: Chapter 27, Square root algorithms, Section 27.3 Mo's algorithm
  - url: https://cp-algorithms.com/data_structures/sqrt_decomposition.html
    title: cp-algorithms, Sqrt Decomposition
    locator: the section Mo's algorithm, with its subsections Implementation, Complexity and Tips for improving runtime
  - url: https://codeforces.com/blog/entry/20032
    title: Codeforces blog, On "Mo's algorithm" (2015), and its comments
    locator: the comments on the origin of the name, with the 2009 China training camp problem
  - url: https://arxiv.org/abs/1908.11819
    title: "Lech Duraj, Krzysztof Kleiner, Adam Polak and Virginia Vassilevska Williams, Equivalences between triangle and range query problems (SODA 2020)"
    locator: the introduction and the appendix on Mo's algorithm
---

Mo's algorithm answers $q$ offline queries about ranges $[l, r)$ of an array of $n$ items by sorting the queries into a good order and moving one window $[L, R)$ from each query to the next, one item at a time. It sorts the queries by the block $\lfloor l / B \rfloor$ of the left end and then by $r$, so that with $B \approx n / \sqrt q$ the two ends of the window move $O(n \sqrt q)$ steps in total. If the answer of the window can be kept under adding and removing one item in $O(1)$ time, all queries take $O(n \sqrt q + q \log q)$ time. This handles queries that do not split into two halves, such as the [number of distinct values](/range-distinct-count-query/) or the [mode](/range-mode-query/) of a range, where a [segment tree](/segment-tree/) does not help directly.

## In plain words

You have a long shelf of items and a list of questions, each about one stretch of the shelf, like "how many different colours are there from item 10 to item 40?". You know all questions before you start. You keep a frame over the shelf and a count of what is inside the frame. You can move either edge of the frame by one item and update the count.

If you take the questions in the given order, the frame may jump from one end of the shelf to the other each time. Mo's idea is to answer them in a better order. Cut the shelf into blocks. Group the questions by the block where they start, and in each group take them by where they end. Then the right edge mostly walks forward, and the left edge only shakes inside one block.

## The problem

The input is an array $A[0 \ldots n-1]$ and a list of $q$ queries $(l_j, r_j)$ with $0 \le l_j \le r_j \le n$. Each query asks for $f(A[l_j \ldots r_j - 1])$ for a fixed function $f$ of a multiset (or of a window). All queries are known before the first answer is needed, which is the [offline](/offline-query-processing/) setting. The method needs a state $S$ of the current window with three operations, the holes of the algorithm:

- ADD$(i)$: add $A[i]$ to the window, where $i$ is next to one end of the window;
- REMOVE$(i)$: remove $A[i]$, where $i$ is an end of the window;
- ANSWER$()$: return $f$ of the window.

For the [range distinct count](/range-distinct-count-query/), $S$ is an array $cnt$ of counts per value and a number $d$ of values with a positive count. ADD$(i)$ increases $cnt[A[i]]$ and increases $d$ when the count becomes 1; REMOVE$(i)$ is the reverse; ANSWER returns $d$.

## The algorithm

```pseudo id=main
MO(A, n, Q, B)                             ▷ Q[0 .. q − 1] holds (l, r); B ≥ 1 is the block size
L1  sort the indices j of Q by the key (⌊l_j / B⌋, r_j)
L2  L ← 0, R ← 0, S ← the state of the empty window
L3  for each j in sorted order do
L4      while L > l_j do L ← L − 1, ADD(L)          ▷ grow to the left
L5      while R < r_j do ADD(R), R ← R + 1          ▷ grow to the right
L6      while L < l_j do REMOVE(L), L ← L + 1       ▷ shrink from the left
L7      while R > r_j do R ← R − 1, REMOVE(R)       ▷ shrink from the right
L8      ans[j] ← ANSWER()
L9  return ans
```

The window is the half-open range $[L, R)$. The two growing loops come first. Then the window always holds at least one of the old and the new range, and it never becomes a range with $L > R$: when line L6 runs, $R \ge r_j \ge l_j$, and when line L7 runs, $R > r_j \ge l_j = L$. So REMOVE is called only for items that are in the window. The block size $B = \max(1, \lceil n / \sqrt q \rceil)$ gives the bound of the front matter. The common choice $B \approx \sqrt n$ gives $O((n + q) \sqrt n)$, which is the same when $q = \Theta(n)$.

## Example

Count the distinct values of $A = [1, 2, 1, 3, 2, 2, 4, 1]$ ($n = 8$) for the queries $Q_0 = [0, 4)$, $Q_1 = [2, 7)$, $Q_2 = [1, 3)$, $Q_3 = [5, 8)$ and $Q_4 = [3, 6)$, with $B = 3$. The keys are $(0, 4)$, $(0, 7)$, $(0, 3)$, $(1, 8)$ and $(1, 6)$, so the order is $Q_2, Q_0, Q_1, Q_4, Q_3$.

| query | key | window before | moves | window after | distinct values |
|---|---|---|---|---|---|
| $Q_2 = [1, 3)$ | $(0, 3)$ | $[0, 0)$ | add 0, 1, 2; remove 0 | $[1, 3)$ | 2 (values 2, 1) |
| $Q_0 = [0, 4)$ | $(0, 4)$ | $[1, 3)$ | add 0, 3 | $[0, 4)$ | 3 |
| $Q_1 = [2, 7)$ | $(0, 7)$ | $[0, 4)$ | add 4, 5, 6; remove 0, 1 | $[2, 7)$ | 4 |
| $Q_4 = [3, 6)$ | $(1, 6)$ | $[2, 7)$ | remove 2, 6 | $[3, 6)$ | 2 (values 3, 2) |
| $Q_3 = [5, 8)$ | $(1, 8)$ | $[3, 6)$ | add 6, 7; remove 3, 4 | $[5, 8)$ | 3 |

The answers in input order are $3, 4, 2, 3, 2$, after 17 calls of ADD and REMOVE in total.

## Correctness

The invariant of the loop of line L3 is: before each round, $S$ is the state of the window $[L, R)$ and $0 \le L \le R \le n$. Each of the lines L4 to L7 moves one end by one step and calls ADD or REMOVE on exactly the item that enters or leaves, so the invariant holds after each step, and the four loops stop with $[L, R) = [l_j, r_j)$. So line L8 returns $f(A[l_j \ldots r_j - 1])$. The order of line L1 changes only the cost, not the answers. The [full proof](proofs/correctness.md) also shows that the window stays a valid range, and proves the bound on the number of moves.

## Complexity

Let $k = \lceil n / B \rceil$ be the number of blocks. Count the steps of the two ends separately.

- **The right end.** Inside one block of left ends, the queries are sorted by $r$, so $R$ only grows: at most $n$ steps per block. Going from the last query of one block to the first query of the next can move $R$ by up to $n$. So $R$ moves at most $2 n k$ steps.
- **The left end.** Between two queries in the same block, $|l_j - l_{j'}| < B$, so these moves add up to less than $q B$. Going from block $b$ to a later block $b'$ moves $L$ forward by less than $(b' - b + 1) B$, and these jumps add up to less than $2 k B \le 2n + 2B$. So $L$ moves at most $q B + 4n$ steps for $B \le n$.

The total is at most $2 n \lceil n / B \rceil + q B + 4n$ calls of ADD and REMOVE. With $B = \lceil n / \sqrt q \rceil$ this is $O(n \sqrt q)$ for $q \le n^2$. The sort takes $O(q \log q)$, or $O(q + n)$ with a bucket sort on the keys. The extra space is $O(q)$ for the order and the answers, plus the state, which is $O(n)$ for the distinct count after [coordinate compression](/coordinate-compression/) of the values. The [complexity proof](proofs/complexity.md) gives the bound in full.

For $n = q = 10^5$, the bound $2 n \lceil n / B \rceil + q B + 4n$ with $B = 317$ is about $9.5 \cdot 10^7$ steps, against up to $10^{10}$ for the naive method that recomputes each query.

## Properties

- **Offline.** All queries must be known before the first answer. With updates mixed in, see [Mo's algorithm with updates](/mo-algorithm-with-updates/).
- **Any window function.** The method uses no algebra of $f$: no associativity, inverse or idempotence. It needs only ADD and REMOVE.
- **Deterministic.** The order and the cost depend only on the queries.
- **Cost depends on the holes.** If ADD and REMOVE take $O(t)$ time, the total is $O(t \cdot n \sqrt q)$. For the mode with a count of counts it is $O(1)$; for a sum of pairwise products it may be more.

## Variants and improvements

- **Odd-even order.** Sort by $r$ ascending in even blocks and descending in odd blocks. The right end then does not jump back after each block, which removes about half of its moves in practice.
- **Hilbert order.** Sort the queries by the position of the point $(l, r)$ on a [Hilbert curve](/hilbert-curve/) over a grid of side a power of two that is at least $n$. Neighbouring queries on the curve are near in both coordinates, and the total movement is $O(n \sqrt q)$ as well, often faster in practice.
- **Add-only Mo (Mo with rollback).** When REMOVE is hard, as for the maximum of a window, take the queries of each block in order of $r$, keep a window that starts at the end of the block and only grows to the right, and for each query add the few items left of the block end, read the answer, and undo these additions from a stack. The cost stays $O(n \sqrt q)$ undo steps.
- **Mo on trees.** Answer path queries on a tree by Mo's algorithm over the Euler tour of the tree, where an item that appears twice in the window counts as absent. See the [Euler tour technique](/euler-tour-technique/).
- **With updates.** Add time as a third coordinate, see [Mo's algorithm with updates](/mo-algorithm-with-updates/), with $O(n^{5/3})$ total moves when $q$ and the number of updates are $\Theta(n)$.

## When to use it

Use Mo's algorithm for offline range queries whose answer is easy to update when one item enters or leaves the window, but hard to combine from two halves: distinct counts, modes, counts of pairs of equal items, sums of squares of counts. For queries with a [monoid](/monoid/) structure, such as sums or minima, a [segment tree](/segment-tree/) or a [sparse table](/sparse-table/) is faster and online. For the distinct count, an offline sweep with a [Fenwick tree](/fenwick-tree/) gives $O((n + q) \log n)$, which is better than $O(n \sqrt q)$; Mo's algorithm is simpler and also extends to the mode and to related queries. If the queries must be answered online, use a [persistent segment tree](/persistent-segment-tree/) or a precomputed square-root table.

## Pitfalls

- **Shrinking first.** If lines L6 and L7 come before lines L4 and L5, the window can pass through $L > R$, and REMOVE is called on an item that is not in the window. A count can then become $-1$, and a distinct counter that tests "the count became 0" gives a wrong value.
- **The wrong key.** Sorting by $(l, r)$ instead of $(\lfloor l / B \rfloor, r)$ lets $R$ jump by up to $n$ at each query, and the cost becomes $\Theta(n q)$.
- **A block size of 0.** With $B = \lfloor n / \sqrt q \rfloor$ and $q > n^2$, or with $\lfloor \sqrt n \rfloor$ for $n = 0$, the division by $B$ in line L1 fails. Use $B = \max(1, \ldots)$.
- **Answers in sorted order.** Line L8 must store the answer at the original index $j$, not at the position in the sorted order.
- **Large values.** An array $cnt$ indexed by the values needs [coordinate compression](/coordinate-compression/) when the values are large. A hash map works but makes each step slower.

## Implementations

## History

The technique is folklore of competitive programming and has almost no presence in the research literature, as Duraj, Kleiner, Polak and Vassilevska Williams remark. In a Codeforces discussion of 2015, the name is traced to Mo Tao (莫涛), who used it with his teammates for a problem of the 2009 China national training camp. Laaksonen's handbook and cp-algorithms describe it as a square-root method for offline queries.

## References
