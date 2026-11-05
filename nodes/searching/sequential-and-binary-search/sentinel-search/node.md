---
tag: ZX47TN
kind: technique
slug: sentinel-search
name: Sentinel linear search
aliases:
- sentinel technique
area: searching/sequential-and-binary-search
level: intro
summary: Place the key at the end of the array so the loop needs one comparison per step instead of two.
prereqs: [linear-search, loop-invariant]
see_also: [linear-search, sentinel-node, sentinel-character, insertion-sort, merge-sort, search-in-unordered-array, sequential-search-symbol-table]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.1, Algorithm Q (quick sequential search) and Algorithm T (sequential search in an ordered table)
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 9, Code tuning (sequential search with a sentinel and loop unrolling)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.2, Linked lists (sentinels)
---

Sentinel search is the technique of placing a copy of the key, the *sentinel*, just past the end of the data, so that a search loop is sure to find the key and needs no separate test for the end. In [linear search](/linear-search/) it removes one of the two tests of each pass: the loop "while $A[i] \ne x$" stops at the latest at the sentinel, and one test after the loop tells a real match from the sentinel. The number of key tests stays $n$ in the worst case, but the end tests drop from $n + 1$ to one. The same idea, a value that stops a loop by itself, appears in [insertion sort](/insertion-sort/), in merging, in [linked lists](/sentinel-node/) and in [strings](/sentinel-character/).

## In plain words

You walk along a row of boxes to find a red ball. At each box you ask two questions: am I past the last box, and is this the red ball? The first question is there only to stop you from walking off the end.

Now put a red ball of your own in an extra box at the end of the row. You are now sure to find a red ball, so you only need to ask one question at each box. When you stop, you look once at where you are. If you stopped at the extra box, the only red ball was yours, and the row has none. If you stopped earlier, you found a real one.

## When it applies

- A loop tests two conditions in each pass, one of which is "the end is not reached", and the other is a test on the data.
- There is a value that makes the data test true, and it can be written at the place where the end test would fail.
- There is a free cell after the data, or the last cell can be saved and restored, and no other code reads the data during the search.
- The loop is hot: it runs many times, so one test less in each pass matters.

## The template

```pseudo id=main
SENTINEL-SEARCH(A, x)               ▷ A[0 .. n − 1] holds the items; A[n] is a free cell
L1  A[n] ← x                         ▷ the sentinel: the loop must stop at index n or before
L2  i ← 0
L3  while A[i] ≠ x do                ▷ one test in each pass, no test of i
L4      i ← i + 1
L5  if i < n then return i           ▷ a real match
L6  return NIL                       ▷ only the sentinel matched
```

The holes are the stop test of line L3 (here $A[i] \ne x$) and the sentinel value of line L1 (here $x$), which must make the stop test true. For a search in a sorted table that stops at the first $A[i] \ge x$, the sentinel is $+\infty$ or any value $\ge x$.

**Why it is correct.** Before each test of line L3, $0 \le i \le n$ and $A[j] \ne x$ for each $j < i$. A pass runs only when $A[i] \ne x$, so it keeps this statement for $i + 1$, and $i + 1 \le n$ because $A[n] = x$ stops the loop at $i = n$ at the latest. So the loop stops after at most $n + 1$ tests, with $A[i] = x$. If $i < n$, then $i$ is the first index of $x$ in the real data. If $i = n$, no index $j < n$ holds $x$, so NIL is correct.

**Cost.** Let the first copy of $x$ be at index $k$, or $k = n$ when $x$ is absent. The plain linear search makes $k + 1$ end tests and $\min(k + 1, n)$ key tests. The sentinel search makes $k + 1$ key tests and one index test at line L5. In the worst case that is $2n + 1$ tests against $n + 2$.

**A trace.** For $A = [7, 3, 9, 3, 1, 8]$ and $x = 5$, line L1 writes $A[6] = 5$. The loop tests $A[0], \ldots, A[6]$, which are 7 tests, and stops at $i = 6 = n$. Line L5 finds $i \not< n$, so the result is NIL. The plain loop makes 6 key tests and 7 end tests, 13 in all, against 8 here.

## Classic examples

- **[Linear search](/linear-search/).** The template above. Knuth gives it as Algorithm Q, the "quick sequential search", next to the plain Algorithm S.
- **Search in an ordered table.** To stop at the first $A[i] \ge x$, put $A[n] = +\infty$. Knuth's Algorithm T does this.
- **[Insertion sort](/insertion-sort/).** The inner loop moves the new item left while the item before it is larger. With $A[-1] = -\infty$, or with the smallest item first moved to $A[0]$, the loop needs no test $j \ge 0$.
- **Merging.** Put $+\infty$ at the end of each of two sorted runs. The merge loop then runs exactly $n$ times and never tests whether a run is empty. Some editions of CLRS write MERGE for [merge sort](/merge-sort/) this way.
- **[Sentinel nodes](/sentinel-node/) in linked lists.** A dummy node in a circular list makes insertion and deletion at the ends the same as in the middle, with no test for an empty list.
- **[Sentinel characters](/sentinel-character/) in strings.** A unique end character, such as the 0 byte of C strings or the $ of a suffix array, stops scans and comparisons without a length test.

## Variations

- **Overwrite the last item.** When there is no free cell, save $t = A[n-1]$, put $x$ in $A[n-1]$, search, then restore $A[n-1] = t$. The search found a real match if it stopped before $n - 1$, or if $t = x$.
- **Search from the right.** Put the sentinel in $A[-1]$ and scan down. This finds the last occurrence.
- **Unrolled loop.** With the end test gone, the loop body can be repeated several times per pass, which removes more branches. Bentley shows this step on the sequential search in Column 9.
- **Two-sided sentinels.** A sort or a merge that can run off either end gets a sentinel at both ends.

## Pitfalls

- **No room for the sentinel.** Writing $A[n]$ in a language without bounds checks, when the array has exactly $n$ cells, writes over other memory. Allocate $n + 1$ cells, or use the variation that overwrites the last item.
- **Forgetting the final test.** Without line L5, a search for an absent key returns $n$, the index of the sentinel, as if it were a match.
- **Not restoring the data.** The variation that overwrites $A[n-1]$ must restore it on every path, including the path that returns early. Otherwise the array is changed.
- **Shared or read-only data.** The sentinel writes to the array. If another thread reads it at the same time, or the array is constant memory, the technique is not safe.
- **A wrong sentinel value.** In the ordered version, the sentinel must make the stop test true for every key. A sentinel of $+\infty$ that is not larger than all keys, for example a "maximum integer" that is also a real key, gives wrong results at the boundary.

## Exercises

1. Write the sentinel version of the search for the first $A[i] \ge x$ in a sorted array, and count its tests for an absent key larger than all items.
2. Write insertion sort with a sentinel at $A[0]$ by first moving the minimum to the front, and show that the inner loop needs no index test.
3. In the variation that overwrites $A[n-1]$, show that the answer is correct when the only copy of $x$ is the old $A[n-1]$.

## References
