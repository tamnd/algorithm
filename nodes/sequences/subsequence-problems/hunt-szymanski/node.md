---
tag: EEQDBV
kind: algorithm
slug: hunt-szymanski
name: Hunt-Szymanski algorithm
aliases:
- Hunt-Szymanski LCS
area: sequences/subsequence-problems
level: core
summary: Computes LCS in O((r + n) log n) time, where r is the number of matching index pairs, which is fast when matches are sparse.
solves: [longest-common-subsequence]
model: word-ram
complexity:
  vars: {m: the length of X, n: the length of Y, r: the number of matching index pairs}
  time: {worst: O((r + m + n) log n)}
  space: {extra: O(r + m + n)}
properties: {stable: false, in_place: false, adaptive: true, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [lcs-dynamic-programming, longest-increasing-subsequence, binary-search]
see_also: [longest-common-subsequence, patience-sorting, hirschberg-lcs, myers-diff, bit-parallel-lcs, shortest-edit-script, colinear-chaining, fenwick-tree]
sources:
  - paper: doi:10.1145/359581.359603
    title: James W. Hunt and Thomas G. Szymanski, A fast algorithm for computing longest common subsequences, Communications of the ACM 20(5), 1977, 350-353
    locator: the threshold array, the match lists in decreasing order, the binary search, the links for recovery, and the O((r + n) log n) bound
  - paper: "J. W. Hunt and M. D. McIlroy, An algorithm for differential file comparison, Computing Science Technical Report 41, Bell Laboratories, 1976"
    locator: the use of the threshold method in the Unix diff program, with lines hashed to numbers
  - paper: "Alberto Apostolico and Concettina Guerra, The longest common subsequence problem revisited, Algorithmica 2, 1987, 315-336"
    locator: the improvements of the match-list method, with time bounds in terms of the number of dominant matches
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences
    locator: Chapter 12, the reduction of LCS to the longest increasing subsequence of the list of matches
---

The Hunt-Szymanski algorithm computes a [longest common subsequence](/longest-common-subsequence/) of $X$ (length $m$) and $Y$ (length $n$) by looking only at the $r$ index pairs $(i, j)$ with $x_i = y_j$, not at all $mn$ cells of the [LCS table](/lcs-dynamic-programming/). It keeps, for each length $k$, the smallest $Y$ position at which a common subsequence of length $k$ can end, and updates these thresholds with [binary search](/binary-search/), in $O((r + m + n) \log n)$ time. When most pairs of lines differ, as in two versions of a source file, $r$ is close to $n$ and the method is much faster than the table; the first Unix diff used it. In the worst case $r = mn$, and it is slower than the table by a factor $\log n$.

## In plain words

Put the two sequences on the two sides of a grid, and mark the cells where the two items are equal. A common subsequence is a chain of marked cells that goes down and to the right at each step. You want the longest such chain.

Go down the rows. For each length of chain, remember the leftmost column where a chain of that length can end so far. These columns go up as the length goes up, so for a new marked cell a binary search finds which length it can extend. Handle the marked cells of a row from right to left, so that two cells of the same row never join the same chain.

## The problem

The input is two sequences $X = \langle x_1, \ldots, x_m \rangle$ and $Y = \langle y_1, \ldots, y_n \rangle$ whose items can be sorted or hashed, so that the positions of each item in $Y$ can be listed. The output is one common subsequence of maximum length. This is the [longest common subsequence](/longest-common-subsequence/) problem; the method suits inputs with few *matches*, the pairs $(i, j)$ with $x_i = y_j$.

## The algorithm

For $0 \le i \le m$ and $k \ge 0$, let the *threshold* $T_i[k]$ be the smallest $j$ such that $X[1 \ldots i]$ and $Y[1 \ldots j]$ have a common subsequence of length $k$, or $\infty$ if there is none. Then $T_i[0] = 0$, and $T_i[1] < T_i[2] < \cdots$ while the values are finite. The algorithm keeps one array $T$ and turns $T_{i-1}$ into $T_i$ with the matches of row $i$.

```pseudo id=main
HUNT-SZYMANSKI(X[1 .. m], Y[1 .. n])
L1  for each item c of X: MATCHLIST[c] ← the positions j with Y[j] = c, in decreasing order
L2  T[0] ← 0; T[1 .. min(m, n)] ← ∞; link[0] ← nil
L3  for i ← 1 to m do
L4      for each j in MATCHLIST[X[i]] do                    ▷ in decreasing order
L5          k ← the smallest index with T[k] ≥ j             ▷ binary search; T[k − 1] < j
L6          if j < T[k] then
L7              T[k] ← j; link[k] ← (i, j, link[k − 1])
L8  ℓ ← the largest k with T[k] < ∞; p ← link[ℓ]
L9  while p ≠ nil do put X[p.i] at the front of Z; p ← p.next
L10 return Z
```

Line L5 finds the length $k$ that the match $(i, j)$ can reach: the longest chain that ends left of column $j$ has length $k - 1$, because $T[k - 1] < j$. If $j$ is a better end for length $k$ than the current one, line L7 records it, with a link to the chain of length $k - 1$ that it extends. The decreasing order of line L4 is the key detail. A match $(i, j)$ may only extend a chain that ends in an earlier row. After $(i, j)$ updates $T[k]$, the next match $(i, j')$ of the same row has $j' < j$, so its search stops at an index at most $k$ and never sees the new value $j$ as a predecessor.

The method is the [patience sorting](/patience-sorting/) solution of the [longest increasing subsequence](/longest-increasing-subsequence/) problem, applied to the column numbers of all matches, listed row by row with the columns of each row in decreasing order. A strictly increasing subsequence of this list takes at most one match per row, so it is a chain of matches, that is, a common subsequence.

## Example

Take $X = \text{ABCBDAB}$ and $Y = \text{BDCABA}$. The positions of A in $Y$ are 4 and 6, of B are 1 and 5, of C is 3 and of D is 2. There are $r = 12$ matches. The array $T[1 \ldots]$ after each row:

| $i$ | $x_i$ | match list | $T[1 \ldots]$ after the row | change |
| --- | --- | --- | --- | --- |
| 1 | A | 6, 4 | 4 | 6 starts length 1, then 4 replaces it |
| 2 | B | 5, 1 | 1, 5 | 5 extends length 1 (end 4); 1 replaces $T[1]$ |
| 3 | C | 3 | 1, 3 | 3 replaces $T[2] = 5$ |
| 4 | B | 5, 1 | 1, 3, 5 | 5 extends length 2; 1 equals $T[1]$, no change |
| 5 | D | 2 | 1, 2, 5 | 2 replaces $T[2] = 3$ |
| 6 | A | 6, 4 | 1, 2, 4, 6 | 6 extends length 3; 4 replaces $T[3] = 5$ |
| 7 | B | 5, 1 | 1, 2, 4, 5 | 5 replaces $T[4] = 6$; 1 equals $T[1]$ |

The final array has 4 finite entries, so $\mathrm{lcs}(X, Y) = 4$. The link of $T[4]$ is the match $(7, 5)$, which links to $(6, 4)$, then $(5, 2)$, then $(2, 1)$. These are the items B, A, D, B read backward, so the output is BDAB. In row 1, the order 6 then 4 matters: in increasing order, 4 would set $T[1] = 4$ and then 6 would extend it to $T[2] = 6$, a chain of two A matches in the same row, which is wrong.

## Correctness

The invariant is that after row $i$, $T[k] = T_i[k]$ for each $k$, and $\mathrm{link}[k]$ is a chain of $k$ matches in rows $1, \ldots, i$ with strictly increasing rows and columns that ends in column $T[k]$. It holds for $i = 0$. For row $i$, a common subsequence of length $k$ of $X[1 \ldots i]$ and $Y[1 \ldots j]$ either does not use row $i$, or ends with a match $(i, j')$, $j' \le j$, after a chain of length $k - 1$ that ends left of $j'$ in earlier rows. So $T_i[k] = \min(T_{i-1}[k], \min\{ j' : (i, j') \text{ is a match and } T_{i-1}[k-1] < j' \})$. The decreasing order of line L4 makes each search of line L5 see only values of $T_{i-1}$ at the indices below the index it finds, which gives exactly this minimum. At the end, $T[\ell]$ is the last finite entry, so $\ell = \mathrm{lcs}(X, Y)$, and $\mathrm{link}[\ell]$ is a chain of $\ell$ matches, which spells a common subsequence. The full proof is in the proof file.

## Complexity

- **Time.** Line L1 sorts the positions of $Y$ by item, in $O(n \log n)$ time, or $O(n)$ expected time with hashing. The loop of lines L3 to L7 visits each of the $r$ matches once, with one binary search in an array of at most $\min(m, n) + 1$ entries, so $O(r \log n)$, plus $O(m)$ for the rows. The traceback takes $O(\ell)$. The total is $O((r + m + n) \log n)$; Hunt and Szymanski state it as $O((r + n) \log n)$.
- **Space.** $O(n)$ for the match lists, $O(\min(m, n))$ for $T$, and one link node for each update of line L7, at most $r$. So $O(r + m + n)$. To keep the space small, keep only the links that are still reachable, or recover the LCS with [Hirschberg's](/hirschberg-lcs/) divide and conquer.
- **Range of $r$.** $r$ can be anywhere from 0 to $mn$. For random strings over an alphabet of size $\sigma$, the expected value is $mn / \sigma$. For two versions of a file of distinct lines, $r$ is about $n$, and the time is $O(n \log n)$. For $X = Y = \text{a}^n$, $r = n^2$ and the time is $\Theta(n^2 \log n)$.

## Properties

- **Output sensitive in the matches.** The work depends on $r$, not on $mn$.
- **Needs an order or a hash.** The items must be grouped by value for line L1. An equality test alone is not enough; this is why the $\Omega(mn)$ lower bound for equality tests does not apply.
- **One pass over $X$.** $X$ is read once, from left to right, so the length can be computed with $X$ read as a stream if $Y$ is indexed in advance.
- **Same answer as a leftmost chain.** Each threshold is the leftmost possible end, so the chain found ends as far left in $Y$ as possible for its length.

## Variants and improvements

- **LIS view.** Write the columns of all matches row by row, decreasing within a row, and run any [LIS](/longest-increasing-subsequence/) algorithm with strict increase. This is the form in Gusfield's book.
- **Dominant matches.** Many matches can never be the end of a best chain for their length. Apostolico and Guerra, among others, give methods whose time depends on the number of dominant matches instead of $r$.
- **Faster search structures.** The binary search can be replaced by a van Emde Boas tree over the column numbers, which gives $O(r \log \log n)$ for the main loop.
- **Weighted matches.** If matches have weights, a chain of maximum weight is found with a [Fenwick tree](/fenwick-tree/) over the columns, as in [colinear chaining](/colinear-chaining/) of seeds in sequence alignment.
- **Unix diff.** Hunt and McIlroy hash each line to a number, so the items of $X$ and $Y$ are the lines of two files, and then run this method on the line numbers.

## When to use it

Use it when the number of matching pairs is small compared with $mn$: long sequences over a large alphabet, such as files compared line by line, or token streams. When the alphabet is small, as for DNA, $r$ is close to $mn$ and the [table](/lcs-dynamic-programming/) or the [bit-parallel method](/bit-parallel-lcs/) is better. When the two inputs are similar, so that the edit distance $D$ is small, [Myers' algorithm](/myers-diff/) is better, since a long common run of equal lines does not raise its cost.

## Pitfalls

- **Increasing order in a row.** Processing the matches of a row in increasing order lets one item of $X$ match two positions of $Y$, and the result can be too long, as the example shows.
- **Non-strict search.** Line L5 must find the first entry *at least* $j$, and line L6 must test strict less. With the first entry *greater than* $j$, a chain could use column $j$ twice.
- **Repeated lines.** Files with many equal lines, such as blank lines or a closing brace, make $r$ large.
- **Link memory.** Storing a link for each update keeps up to $r$ nodes alive, which can be large when $r$ is near $mn$.

## Implementations

## History

Hunt and Szymanski published the method in Communications of the ACM in 1977. Hunt and McIlroy describe in their 1976 Bell Labs report how the Unix diff program uses it, with the lines of the files hashed to numbers. Apostolico and Guerra (1987) revisited the problem and refined the bounds in terms of dominant matches.

## References
