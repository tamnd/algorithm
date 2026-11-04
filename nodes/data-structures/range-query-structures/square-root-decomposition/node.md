---
tag: GE30M9
kind: technique
slug: square-root-decomposition
name: Square-root decomposition
aliases:
- sqrt decomposition
- block decomposition
area: data-structures/range-query-structures
level: intro
summary: Split the array into blocks of size about sqrt(n) and precompute block aggregates.
prereqs: [range-query-problem, array, asymptotic-notation]
see_also: [mo-algorithm, sqrt-tree, segment-tree, range-mode-query, range-update-range-query, fenwick-tree, mo-algorithm-with-updates, chtholly-tree]
sources:
  - url: https://cp-algorithms.com/data_structures/sqrt_decomposition.html
    title: cp-algorithms, Sqrt Decomposition
    locator: sections Basic idea, Other problems, Mo's algorithm
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 27 (Square root algorithms)
  - paper: "Timothy M. Chan, Stephane Durocher, Kasper Green Larsen, Jason Morrison and Bryan T. Wilkinson, Linear-Space Data Structures for Range Mode Query in Arrays, Theory of Computing Systems 55(4) (2014)"
    locator: the block decomposition with a table of the modes of block spans
---

Square-root decomposition is a technique for range queries and updates on an array of $n$ items: cut the array into blocks of about $\sqrt n$ items, and keep a summary of each block. A query then reads at most two partial blocks item by item and takes the summaries of the at most $\sqrt n$ full blocks between them, so it costs $O(\sqrt n)$ steps; an update changes one item and one summary. It is slower than a [segment tree](/segment-tree/) for the usual [range queries](/range-query-problem/), but it is simple, and it also works for queries that do not split into two halves, such as the [range mode](/range-mode-query/), and for the reordering of offline queries in [Mo's algorithm](/mo-algorithm/).

## In plain words

Think of a book with many pages, and you often need the number of words between two pages. Counting all the pages each time is slow. Instead, put a bookmark every few pages and write on each one how many words the pages up to the next bookmark hold.

To answer a question, count the words of the loose pages at the two ends, one page at a time, and add the numbers written on the bookmarks in between. If the bookmarks are too close, you have many of them to add. If they are too far apart, the loose pages at the ends are many. The best spacing is the square root of the number of pages, because then both kinds of work are equal and small.

When a page changes, fix that page and the number on its one bookmark.

## When it applies

- **A summary of a block is easy to build and to combine.** Sums, minimums, counts, sorted copies of a block, or a table of counts of each value in a block.
- **The query or the update has no tree-friendly form.** The answer for a range does not follow from the answers for two halves (the mode, the number of distinct values), or an update does not compose well with the stored summaries. A block can still be rebuilt from its items.
- **The time limit allows about $n \sqrt n$ steps.** For $n$ and the number of operations near $10^5$, $\sqrt n$ is about 316, and $10^5 \cdot 316 \approx 3 \cdot 10^7$ steps is fast.
- **A simple, safe solution is wanted.** The code has no recursion and few cases.

## The template

```pseudo id=main
BUILD(A[0 .. n − 1])
L1  b ← max(1, ⌊√n⌋)                                       ▷ hole: the block size
L2  for j ← 0 to ⌈n/b⌉ − 1 do B[j] ← SUMMARY(j)            ▷ hole: the summary of A[jb .. min(n, (j+1)b) − 1]

QUERY(l, r)                                                ▷ 0 ≤ l ≤ r < n
L3  res ← e; i ← l
L4  while i ≤ r and i mod b ≠ 0 do res ← res ⊕ A[i]; i ← i + 1      ▷ left partial block
L5  while i + b − 1 ≤ r do res ← res ⊕ B[i / b]; i ← i + b          ▷ full blocks
L6  while i ≤ r do res ← res ⊕ A[i]; i ← i + 1                      ▷ right partial block
L7  return res

UPDATE(i, x)
L8  A[i] ← x
L9  B[⌊i/b⌋] ← SUMMARY(⌊i/b⌋)                              ▷ hole: or a faster repair of one summary
```

The holes are the block size $b$, the summary of a block with its combine $\oplus$ and identity $e$, and the repair of a summary after an update. Block $j$ holds the indices $jb$ to $\min(n, (j+1)b) - 1$, so the last block may be shorter.

**Why it is correct.** The query keeps the invariant $res = A[l] \oplus \cdots \oplus A[i - 1]$, with $res = e$ when $i = l$. Line L4 adds single items until $i$ is the start of a block or passes $r$. Line L5 runs only while $i$ is the start of a block, since $i$ is a multiple of $b$ after line L4 when $i \le r$ and stays one after each step, and the block $[i, i + b - 1]$ lies inside $[l, r]$; by the invariant of $B$ it adds the product of exactly that block. Line L6 adds the rest one by one. Each step raises $i$ by at least 1, so the loops end, and at the end $i = r + 1$, so $res$ is the product of $A[l \ldots r]$. The update keeps $B[j]$ equal to the summary of block $j$, because only the block of $i$ holds the changed item.

**Cost.** Line L4 and line L6 each run at most $b - 1$ times, and line L5 runs at most $\lfloor (r - l + 1)/b \rfloor \le n / b$ times. So a query does at most $2(b - 1) + n/b$ applications of $\oplus$. The function $2b + n/b$ is smallest at $b = \sqrt{n/2}$, where it is $2\sqrt{2n}$; with $b = \lfloor \sqrt n \rfloor$ the bound is about $3 \sqrt n$. The build costs $O(n)$ when SUMMARY costs time linear in the block. An update that rebuilds the summary costs $O(b) = O(\sqrt n)$, and one that repairs it in $O(1)$, as $B[j] \leftarrow B[j] - \mathit{old} + x$ for a sum, costs $O(1)$.

### A worked run

Let $A = [5, 2, 8, 1, 9, 3, 7, 4, 6]$, $n = 9$, $\oplus = +$. Then $b = 3$ and the block sums are $B = [15, 13, 17]$.

| step | operation | work | result |
|---|---|---|---|
| 1 | QUERY$(1, 7)$ | line L4 adds $A[1], A[2] = 2, 8$; line L5 adds $B[1] = 13$; line L6 adds $A[6], A[7] = 7, 4$ | $10 + 13 + 11 = 34$ |
| 2 | UPDATE$(4, 0)$ | $A[4] = 0$; block 1 is $1, 0, 3$ | $B = [15, 4, 17]$ |
| 3 | QUERY$(1, 7)$ | the same parts, with $B[1] = 4$ | $10 + 4 + 11 = 25$ |
| 4 | QUERY$(3, 8)$ | line L4 adds nothing; line L5 adds $B[1] = 4$ and $B[2] = 17$ | 21 |

## Classic examples

- **Range sum or minimum with point updates.** The template with $B[j]$ the sum or the minimum of block $j$. It gives $O(\sqrt n)$ per operation, against $O(\log n)$ for a [segment tree](/segment-tree/) or a [Fenwick tree](/fenwick-tree/).
- **Range add and range sum.** Keep, besides the sum, a pending add $tag[j]$ for each block. An add on a full block changes only $tag[j]$ and the block sum; an add on a partial block changes the items. Both operations cost $O(\sqrt n)$; see [range update range query](/range-update-range-query/).
- **Count the items at most $x$ in a range.** Keep a sorted copy of each block. A query searches each full block by [binary search](/binary-search/) and scans the partial blocks, in $O(\sqrt n \log n)$ time; an update re-sorts one block by one insertion step in $O(\sqrt n)$.
- **[Range mode](/range-mode-query/).** Precompute the mode of each span of whole blocks, a table of $(n/b)^2$ entries. The mode of a query is the mode of its full blocks or a value of the two partial blocks, so $O(b)$ candidates must be counted. Chan and coauthors count each candidate in $O(1)$ with position lists, which gives $O(\sqrt n)$ per query in $O(n)$ space.
- **[Mo's algorithm](/mo-algorithm/).** Square-root decomposition of the queries, not of the array: sort offline queries by the block of their left end and then by their right end, and move a window from one query to the next. The window moves $O((n + q)\sqrt n)$ steps in total for $q$ queries with blocks of size $\sqrt n$, and $O(n \sqrt q)$ steps with blocks of size $n / \sqrt q$. This answers the [range distinct count](/range-distinct-count-query/) and similar queries.
- **[Sqrt tree](/sqrt-tree/).** Apply the decomposition again inside each block, and store the products between blocks. With $O(\log \log n)$ levels the query takes $O(1)$ time.

## Variations

- **Other block sizes.** When a partial block costs $c_1$ per item and a full block costs $c_2$, the bound $2 c_1 b + c_2 n / b$ is smallest at $b = \sqrt{c_2 n / (2 c_1)}$. For the sorted blocks above, $c_2 = \log b$, so slightly larger blocks are better.
- **Decomposition of the operations.** Keep a list of the recent updates and apply them to each query by hand. After every $\sqrt q$ updates, rebuild a static structure from scratch. This turns a static structure into a dynamic one.
- **Decomposition by size.** Split the objects into "heavy" ones, of size at least $\sqrt m$, of which there are at most $\sqrt m$, and "light" ones, and handle each kind by its own method. This is the usual way to count triangles or to answer pair queries in graphs with $m$ edges.
- **Several levels.** Blocks of blocks give $O(n^{1/k})$-style trade-offs and, in the limit, a [segment tree](/segment-tree/) or the [sqrt tree](/sqrt-tree/).

## Pitfalls

- **A float square root.** `int(sqrt(n))` can be one too small or one too large when $n$ is beyond the exact range of a double; use an integer square root. The exact value does not matter for the bound, but $b = 0$ for $n = 0$ breaks the division in line L2, which is why line L1 takes $\max(1, \cdot)$.
- **The short last block.** Block $\lceil n/b \rceil - 1$ may hold fewer than $b$ items. A loop that assumes $b$ items in each block reads past the end of the array.
- **Forgotten tags on partial blocks.** With pending range updates, an operation that touches some items of a block must first apply the tag of that block to its items, or clear the tag into them. Otherwise the items and the summary disagree.
- **Line L5 starting inside a block.** If line L4 is skipped and the full-block loop starts at $l$ when $l$ is not a multiple of $b$, it adds a block that begins before $l$.
- **A block size fixed for the wrong cost.** Taking $b = \sqrt n$ when the two parts of a query have very different costs can make the program several times slower than the balanced choice.

## Exercises

1. Show that the query of the template does at most $2\sqrt{2n} - 2$ applications of $\oplus$ when $b = \sqrt{n/2}$ is an integer. For $n$ a multiple of $b$, find a query that needs $2(b - 1) + n/b - 2$ of them.
2. Write range add and range minimum with block tags, and prove that each operation costs $O(\sqrt n)$.
3. With $q$ queries "count the items at most $x$ in $A[l \ldots r]$" and $u$ point updates, choose the block size that minimizes the total time, and state the result.
4. In the variant that rebuilds a static structure after every $k$ updates, a rebuild costs $\Theta(n)$ and each query also scans the at most $k$ pending updates in $O(1)$ time each. Show that $q$ operations take $O(qk + qn/k)$ time, and that $k = \lceil \sqrt n \rceil$ gives $O(q \sqrt n)$.

## References
