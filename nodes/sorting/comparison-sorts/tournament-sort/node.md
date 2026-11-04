---
tag: 15RWNV
kind: algorithm
slug: tournament-sort
name: Tournament sort
aliases:
- tree selection sort
area: sorting/comparison-sorts
level: advanced
summary: Selection sort using a tournament tree of comparisons to find each successive minimum.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [tournament-tree, selection-sort]
see_also: [tournament-tree, selection-sort, heapsort, replacement-selection, k-way-merge, binary-heap, selection-problem, weak-heapsort]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3, Sorting by selection (tree selection, the tournament with n - 1 comparisons for the first winner and the replay of one path for each next winner, and the step to heapsort)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection (the tournament finds the second smallest with n + ceil(lg n) - 2 comparisons, and the matching lower bound)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.4.1, Multiway merging and replacement selection (the tree of losers, and replacement selection with runs of mean length 2P)
---

Tournament sort is a [selection sort](/selection-sort/) that keeps the results of its comparisons in a [tournament tree](/tournament-tree/). The items play a knockout tournament: in each match the smaller item wins, and the winner of the final is the minimum, found with $n - 1$ comparisons. After the winner is output, its leaf is emptied and only the matches on its path to the root are played again, with at most $\lceil \lg n \rceil$ comparisons, to find the next minimum. So the sort makes at most $n - 1 + (n - 1)\lceil \lg n \rceil$ comparisons and takes $\Theta(n \log n)$ time. It is stable when ties go to the left, and it needs $\Theta(n)$ extra space for the tree. Knuth calls it tree selection; it led to [heapsort](/heapsort/), which keeps the same idea in place.

## In plain words

Imagine a sports cup for numbers. The numbers play in pairs, and the smaller one wins and goes on to the next round. The winner of the final is the smallest number, and it takes one match for each number that drops out.

Now take the champion out. To find the second smallest, you do not need to play the whole cup again. Only the matches that the champion played are open now, because in the other matches the winner is still in the cup. So you replay only these few matches, one per round, and the new champion is the second smallest number.

You repeat this until all numbers are out. Each new champion costs one match per round, and the number of rounds grows only slowly with the number of players.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array, with its items in non-decreasing order. This is the [sorting problem](/sorting-problem/). The algorithm uses a tree of $2m$ slots, where $m$ is the least power of 2 at least $n$, and an output array of $n$ items.

## The algorithm

```pseudo id=main
TOURNAMENT-SORT(A)                         ▷ T[v] holds the index of an item, or empty
L1  m ← the least power of 2 with m ≥ n;  T[m + i] ← i for i < n, and empty for the other leaves
L2  for v ← m − 1 down to 1 do T[v] ← WINNER(T[2v], T[2v + 1])
L3  for t ← 0 to n − 1 do
L4      w ← T[1];  B[t] ← A[w]             ▷ the root holds the least item left
L5      v ← m + w;  T[v] ← empty
L6      while v > 1 do
L7          v ← ⌊v / 2⌋;  T[v] ← WINNER(T[2v], T[2v + 1])
L8  copy B into A

WINNER(i, j)
    if i is empty then return j;  if j is empty then return i
    if A[j] < A[i] then return j else return i
```

The tree is stored as in a [binary heap](/binary-heap/): node $v$ has children $2v$ and $2v + 1$, and the leaves are $T[m \ldots 2m - 1]$. Each internal node holds the index of the winner of its subtree. WINNER makes a comparison only when both slots are full, and on a tie it keeps the left one, which has the smaller index. Line L2 plays the first tournament. Lines L5 to L7 empty the leaf of the winner and replay the matches on its path.

## Example

Sort $A = [5, 1, 4, 2, 8, 3, 7, 6]$, so $m = 8$. Line L2 plays 4 matches in the first round (winners 1, 2, 3, 6), 2 in the second (1, 3) and 1 in the final (1): 7 comparisons.

| output | the leaf emptied | the replayed matches | comparisons |
|---|---|---|---|
| 1 | $A[1]$ | 5 against nobody, 5 against 2, 2 against 3 | 2 |
| 2 | $A[3]$ | 4 against nobody, 5 against 4, 4 against 3 | 2 |
| 3 | $A[5]$ | 8 against nobody, 8 against 6, 4 against 6 | 2 |
| 4 | $A[2]$ | empty pair, 5 against nobody, 5 against 6 | 1 |
| 5 | $A[0]$ | empty pair, empty pair, nobody against 6 | 0 |
| 6 | $A[7]$ | 7 against nobody, 8 against 7, nobody against 7 | 1 |
| 7 | $A[6]$ | empty pair, 8 against nobody, nobody against 8 | 0 |
| 8 | $A[4]$ | all empty | 0 |

The sort makes $7 + 8 = 15$ comparisons. The least worst-case number for 8 items is 16, and $\lg 8! \approx 15.3$. A match against an empty slot costs no comparison, so the count is often well below the bound $7 + 7 \cdot 3 = 28$.

## Correctness

The key invariant is: each internal node $v$ holds the index of the least item, with ties broken by the smaller index, among the items that are still in the leaves of its subtree, or empty if there are none. Line L2 makes it true from the bottom up, because WINNER returns the better of the two children. When a leaf is emptied, only the nodes on its path have a changed subtree, and line L7 recomputes them from the bottom up, so the invariant holds again. So the root always holds the least remaining item, by key and then by index, and the output $B$ is the input in sorted order with equal items in input order. The full proof is below.

## Complexity

**Comparisons.** The first tournament makes exactly $n - 1$ comparisons, because each comparison knocks out one item and $n - 1$ items must be knocked out. Each replay passes $\lg m = \lceil \lg n \rceil$ levels and makes at most one comparison per level. So the total is at most $(n - 1) + (n - 1) \lceil \lg n \rceil$; the last replay finds an empty tree. Matches against empty slots are free, so the true count is lower and depends on the input.

| input | $n$ | comparisons | $\lg n!$ | $n \lg n$ |
|---|---|---|---|---|
| random | 1024 | 8,971 | 8,769 | 10,240 |
| sorted | 1024 | 5,120 | 8,769 | 10,240 |
| random | $10^5$ | 1,566,566 | 1,516,704 | 1,660,964 |
| sorted | $10^5$ | 877,968 | 1,516,704 | 1,660,964 |

On random input the count is close to $\lg n!$, the lower bound for any comparison sort. On sorted input it is lower, because the items leave the tree from left to right, and many matches are against empty halves.

**Time.** Each comparison comes with $O(1)$ other work, and each replay visits $\lceil \lg n \rceil$ nodes, so the time is $\Theta(n \log n)$ in every case.

**Space.** The tree has $2m < 4n$ slots of indices, and the output needs $n$ items. So the extra space is $\Theta(n)$.

| claim | model and case | bound |
|---|---|---|
| time | comparison model, worst, average and best | $\Theta(n \log n)$ |
| comparisons | worst | at most $(n - 1)(1 + \lceil \lg n \rceil)$ |
| extra space | | $\Theta(n)$ |

## Properties

- **Stable.** WINNER keeps the left item on a tie, so each root is the least item with the smallest index, and equal items leave in input order.
- **Not in place.** The tree and the output take $\Theta(n)$ extra space.
- **Not adaptive.** The time is $\Theta(n \log n)$ on each input, although sorted input saves comparisons.
- **Lazy.** The first $k$ items of the output cost $O(n + k \log n)$ time, so the method also finds the $k$ least items, in order, fast.

## Variants and improvements

- **[Heapsort](/heapsort/).** A heap stores each item once, in the array itself, instead of a winner in each node. This makes the sort in place, at the cost of about twice as many comparisons per step. Knuth presents heapsort as the step after tree selection.
- **The tree of losers.** Store at each node the loser of its match, and the overall winner apart. A replay then compares the new item with the losers on its path, without a look at the siblings. This form is used in [k-way merging](/k-way-merge/), where the leaves are the heads of the input runs.
- **[Replacement selection](/replacement-selection/).** In external sorting, replace the winner by the next item of the input instead of an empty slot. Items that are smaller than the last output wait for the next run. With $P$ leaves, the runs have mean length $2P$ on random input (Knuth, Section 5.4.1).
- **The second smallest.** The second smallest item is one of the items that lost to the winner, so it is found with $\lceil \lg n \rceil - 1$ more comparisons, $n + \lceil \lg n \rceil - 2$ in total. Knuth (Section 5.3.3) shows that this is optimal.

## When to use it

Use tournament sort, or its tree of losers, when the items come from several sorted sources, as in a k-way merge or in external sorting, or when only the first $k$ items of the sorted order are needed. For a full sort of an array in memory, [heapsort](/heapsort/) gives the same bound in place, and [merge sort](/merge-sort/) is faster in practice.

## Pitfalls

- **Ties.** WINNER must keep the left item on a tie. A test with $\le$ the other way gives a correct sort that is not stable.
- **Sizes that are not powers of 2.** Pad the leaves with empty slots, and make WINNER treat empty slots as losers without a comparison. A sentinel value such as $+\infty$ works for numbers, but not for general items.
- **Output in place.** The algorithm reads $A$ through the indices in the tree, so it must not write the output into $A$ before the end. Use the separate array $B$.
- **Space.** The tree needs about $2n$ to $4n$ indices. For large arrays of small items, this costs more memory than the data.

## Implementations

## History

Tree selection is the knockout tournament of sports, applied to sorting. Knuth's Section 5.2.3 describes it as the natural improvement of straight selection: keep the results of the matches, so that each later minimum costs about $\lg n$ comparisons instead of $n$. The same section then shows how Williams's heapsort of 1964 keeps the gain without the extra space. Tournament trees remain the standard structure for multiway merging in external sorting.

## References
