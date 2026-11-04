---
tag: XFPAYN
kind: algorithm
slug: mo-algorithm-with-updates
name: Mo's algorithm with updates
aliases:
- time-dimension Mo's algorithm
- Mo with modifications
area: data-structures/range-query-structures
level: advanced
summary: Adds time as a third sorting dimension so offline queries with point updates run in O(n^(5/3)).
solves: [range-distinct-count-query]
model: word-ram
complexity:
  vars: {n: the length of the array, q: the number of queries, m: the number of point updates; the bound is for q and m of order n and the block size n^(2/3)}
  time: {worst: O(n^(5/3) + q log q)}
  space: {extra: O(n + q + m)}
properties: {deterministic: true, online: false, recursive: false}
prereqs: [mo-algorithm, square-root-decomposition, offline-query-processing]
see_also: [range-distinct-count-query, range-mode-query, hilbert-curve, offline-deletion, rollback-technique, persistent-segment-tree, sliding-window]
sources:
  - url: https://oi-wiki.org/misc/modifiable-mo-algo/
    title: OI Wiki, 带修改莫队 (Mo's algorithm with modifications)
    locator: the sections 特点 (the time dimension and the sort by the block of l, the block of r and the time), 最优块长以及时间复杂度分析 (the block length (n^2 t / m)^(1/3) and the bound O(n^(2/3) m^(2/3) t^(1/3))) and 过程 (applying and undoing a modification)
  - url: https://codeforces.com/blog/entry/72690
    title: Codeforces blog, Mo's Algorithm (with update and without update, now you can understand both)
    locator: the part with updates (queries as triples with a time, blocks of size n^(2/3), and the count of the moves of the time pointer)
  - url: https://codeforces.com/blog/entry/44711
    title: Codeforces blog, Update query on Mo's Algorithm, and its comments
    locator: the comments that set the block size to n^(2/3) for a total of O(n^(5/3))
---

Mo's algorithm with updates answers offline range queries on an array that also receives point updates, by giving each query a third coordinate: its *time*, the number of updates before it. It keeps a window $[L, R)$ and a time $T$, and moves all three by single steps, where a step in time applies or undoes one update. The queries are sorted by the block of $l$, then the block of $r$, then $t$, with blocks of size $B \approx n^{2/3}$, which makes the total number of steps $O(n^{5/3})$ when the numbers of queries and updates are of order $n$. It extends [Mo's algorithm](/mo-algorithm/) to queries such as the [number of distinct values](/range-distinct-count-query/) of a range under updates, which have no easy online solution.

## In plain words

Plain Mo's algorithm walks a frame along a shelf and answers questions in a clever order. Now the shelf also changes: from time to time one item is replaced. Each question is about the shelf as it was at the moment it was asked.

So the frame gets a third handle: a clock. Turning the clock forward by one replays the next change, and turning it back undoes it. If the changed item is inside the frame, the count is fixed by taking the old item out and putting the new one in. The questions are put in an order where the two edges and the clock all stay close from one question to the next, so the total work stays small.

## The problem

**Input.** An array $A[0 \ldots n-1]$ and a sequence of operations, known in advance, of two kinds:

- $\textsc{update}(p, x)$: set $A[p] \leftarrow x$;
- $\textsc{query}(l, r)$ with $0 \le l \le r \le n$: a value $f(A[l \ldots r-1])$ of the current array.

**Tools.** As in Mo's algorithm, a state for the window with ADD$(x)$, REMOVE$(x)$ and ANSWER, each in $O(1)$ time, where $x$ is a value, so that the state after any sequence of ADD and REMOVE calls depends only on the multiset of values in the window.

**Output.** The answer of each query, in the input order.

## The algorithm

Number the updates $1, \ldots, m$, and give each query the time $t$ equal to the number of updates before it. So a query is a triple $(l, r, t)$ on the array after the first $t$ updates. The update $j$ is stored as a pair $U[j] = (p, x)$, and *applying* it swaps $A[p]$ with $x$: afterwards $A[p]$ is the new value and $U[j]$ holds the old one, so applying it a second time undoes it.

```pseudo id=main
MO-WITH-UPDATES(A, ops, B)
L1  split ops into queries (l, r, t) and updates U[1..m] = (p, x)
L2  sort the queries by (⌊l / B⌋, ⌊r / B⌋, t)
L3  L ← 0, R ← 0, T ← 0                    ▷ empty window on the original array
L4  for each query (l, r, t) in sorted order do
L5      while T < t do T ← T + 1, APPLY(T)
L6      while T > t do APPLY(T), T ← T − 1
L7      move L to l and R to r with ADD and REMOVE, as in Mo's algorithm
L8      record ANSWER() for this query
L9  return the answers in the input order

APPLY(j)                                   ▷ apply or undo the update j
L10 (p, x) ← U[j]
L11 if L ≤ p < R then REMOVE(A[p])
L12 swap A[p] and x, U[j] ← (p, x)
L13 if L ≤ p < R then ADD(A[p])
```

The block size $B = \lceil n^{2/3} \rceil$ is the usual choice. For other ratios of $q$ and $m$, OI Wiki gives the block size $(n^2 m / q)^{1/3}$, up to a constant.

## Example

Take $A = [1, 2, 1, 3, 2]$ and the operations

$\textsc{query}(0, 3)$, $\textsc{update}(1, 1)$, $\textsc{query}(0, 3)$, $\textsc{query}(1, 5)$, $\textsc{update}(3, 2)$, $\textsc{query}(1, 5)$,

where each query asks for the number of distinct values. The queries are $(0, 3, 0)$, $(0, 3, 1)$, $(1, 5, 1)$ and $(1, 5, 2)$, with $U[1] = (1, 1)$ and $U[2] = (3, 2)$. With $B = \lceil 5^{2/3} \rceil = 3$, every query has the key $(0, 1, t)$, so the sorted order is the input order.

| query | time moves | window moves | window values | answer |
|---|---|---|---|---|
| $(0, 3, 0)$ | none | ADD at 0, 1, 2 | $1, 2, 1$ | 2 |
| $(0, 3, 1)$ | APPLY(1): $p = 1$ is inside, REMOVE(2), $A[1] \leftarrow 1$, ADD(1) | none | $1, 1, 1$ | 1 |
| $(1, 5, 1)$ | none | ADD at 3, 4, REMOVE at 0 | $1, 1, 3, 2$ | 3 |
| $(1, 5, 2)$ | APPLY(2): $p = 3$ is inside, REMOVE(3), $A[3] \leftarrow 2$, ADD(2) | none | $1, 1, 2, 2$ | 2 |

The answers $2, 1, 3, 2$ match the queries asked on the array of their time. After the run, $U[1] = (1, 2)$ and $U[2] = (3, 3)$ hold the old values, ready to undo.

## Correctness

The algorithm keeps the invariant: $A$ is the original array after the updates $1, \ldots, T$, and the window state holds the multiset $\{A[k] : L \le k < R\}$. APPLY$(j)$ with $T = j - 1$ before it turns the array into the array after update $j$, because the swap writes the new value; with $T = j$ before it, it writes back the old value that the earlier swap stored in $U[j]$. In both cases, if $p$ is in the window, the old value leaves the state and the new one enters it, so the multiset stays right; if not, the window does not change. Lines L5 and L6 therefore bring the array to time $t$ with a correct state, and line L7 brings the window to $[l, r)$ by the argument of Mo's algorithm. So line L8 reads $f$ of the window of the query on the array of its time. The [proof](proofs/correctness.md) gives the details, and the [complexity proof](proofs/complexity.md) counts the moves.

## Complexity

Let $k = \lceil n / B \rceil$ be the number of blocks, and call a *group* the queries with the same pair of blocks $(\lfloor l / B \rfloor, \lfloor r / B \rfloor)$; there are at most $k^2$ groups, and they are consecutive in the sorted order.

- **Time pointer.** Inside a group, $t$ is non-decreasing, so $T$ moves at most $m$ steps per group, plus at most $m$ steps on entering it: at most $2 m k^2$ steps.
- **Left end.** Between two queries with the same left block, $l$ moves less than $B$. The left block is non-decreasing along the order, so the moves between different left blocks sum to $O(n)$: in total $O(q B + n)$.
- **Right end.** Inside a group it moves less than $B$ per query. For a fixed left block the right block is non-decreasing, so the moves between groups with that left block sum to $O(n)$, and over the $k$ left blocks to $O(n k)$.

In total, $O(q B + n^2 / B + m n^2 / B^2)$ steps, each $O(1)$, plus $O(q \log q)$ for the sort. With $q, m = \Theta(n)$ and $B = n^{2/3}$ this is $O(n^{5/3})$. In general, the block $B = (n^2 m / q)^{1/3}$ balances the first and third terms and gives $O(n^{2/3} m^{1/3} q^{2/3})$, as stated on OI Wiki. The space is $O(n + q + m)$ for the array, the updates and the answers, plus the window state.

## Properties

- **Offline.** All operations must be known before the first answer.
- **Deterministic.** The order depends only on the queries.
- **Undo by swap.** The update list is its own undo log, so no extra memory is used for history.
- **Value-based state.** The window state only sees values; an update outside the window costs one array write.

## Variants and improvements

- **Order inside a group.** Sorting $t$ up and down in alternate groups, like the odd-even trick of plain Mo, removes the reset of $T$ at the start of each group and helps in practice.
- **Space-filling curves.** Ordering the triples along a three-dimensional curve such as the Peano or [Hilbert curve](/hilbert-curve/) also gives $O(n^{5/3})$ and is often faster.
- **On trees.** The same time dimension works with Mo's algorithm on paths of a tree, through an Euler tour.
- **Without updates.** With $m = 0$ the time pointer never moves and the method is plain Mo's algorithm, but the block size should then be $n / \sqrt q$, not $n^{2/3}$.
- **Rollback instead of remove.** If REMOVE is hard but ADD can be undone, combine the time dimension with Mo's algorithm with [rollback](/rollback-technique/).

## When to use it

Use it when the queries are offline, there are point updates between them, and the answer of a window is easy to keep under adding and removing one value, but hard to combine from two halves: the number of distinct values, the number of values that occur exactly $k$ times, or the mode of a range. For queries that combine from halves, such as sums or minima, a [segment tree](/segment-tree/) is faster and online. For $n = 10^5$, $n^{5/3}$ is about $2 \cdot 10^8$ cheap steps, which is near the limit of what runs in a few seconds.

## Pitfalls

- **The block size of plain Mo.** With $B = \sqrt n$ the time pointer moves up to $m$ steps for each of the $n$ groups, which gives $\Theta(n^2)$ for $m = \Theta(n)$.
- **Sorting by the right end, not its block.** Sorting the second key by $r$ instead of $\lfloor r / B \rfloor$ leaves $t$ in random order, and the time pointer moves $\Theta(m)$ per query.
- **Updates outside the window.** APPLY must still write the array when $p$ is outside $[L, R)$, or later window moves read stale values.
- **Undo order.** Undoing must go from $T$ down to $t + 1$, the reverse of the order in which the updates were applied, since two updates of the same position do not commute.
- **Updates that do not change the value.** These are harmless with the swap form, but code that stores only the new value must also keep the old one to undo.

## Implementations

## History

The time dimension appears in Chinese competitive programming, where OI Wiki presents it as 带修改莫队 with the problem 数颜色 (count colours under updates) of the Chinese national training team as its example. In English the method spread through Codeforces blogs and through problems such as SPOJ ADAUNIQ, with the block size $n^{2/3}$ and the bound $O(n^{5/3})$ stated in the comments of a 2016 blog on update queries.

## References
