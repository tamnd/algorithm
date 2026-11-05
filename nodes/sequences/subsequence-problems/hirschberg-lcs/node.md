---
tag: S3GJKS
kind: algorithm
slug: hirschberg-lcs
name: Hirschberg's algorithm
aliases:
- Hirschberg linear-space LCS
area: sequences/subsequence-problems
level: core
summary: Recovers an LCS in O(nm) time and O(n + m) space by divide and conquer on the middle row.
solves: [longest-common-subsequence]
model: word-ram
complexity:
  vars: {m: the length of X, n: the length of Y}
  time: {worst: Θ(m n), average: Θ(m n), best: Θ(m n)}
  space: {extra: Θ(m + n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: true}
prereqs: [lcs-dynamic-programming, divide-and-conquer-paradigm, rolling-array-space-reduction]
see_also: [longest-common-subsequence, lcs-optimal-substructure, myers-diff, needleman-wunsch, global-alignment, edit-distance, bit-parallel-lcs, hunt-szymanski]
sources:
  - paper: doi:10.1145/360825.360861
    title: D. S. Hirschberg, A linear space algorithm for computing maximal common subsequences, Communications of the ACM 18(6), 1975, 341-343
    locator: the procedures for the last row of the LCS table in linear space and the divide and conquer on the middle row of the first string
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 6.7, Sequence alignment in linear space via divide and conquer (the split through the middle column and the time bound by recurrence)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences
    locator: Chapter 12, the section on computing alignments in only linear space
  - paper: "Eugene W. Myers and Webb Miller, Optimal alignments in linear space, Computer Applications in the Biosciences 4(1), 1988, 11-17"
    locator: the extension of the linear-space method to alignment with affine gap costs
---

Hirschberg's algorithm finds a [longest common subsequence](/longest-common-subsequence/) of two sequences $X$ and $Y$ of lengths $m$ and $n$ in $\Theta(mn)$ time and only $\Theta(m + n)$ space. The [LCS table](/lcs-dynamic-programming/) needs $\Theta(mn)$ space for its traceback; Hirschberg instead computes one row of the table from the top and one from the bottom, finds where an optimal path crosses the middle row of $X$, and solves the two halves recursively. The halves together have half the area of the full table, so the total work is less than about twice that of the plain table. Hirschberg published it in 1975, and it is the standard way to get alignments of long sequences in small memory.

## In plain words

The usual way to find a longest common part of two words fills a big grid and then walks back through it. For long words the grid does not fit in memory. You can fill the grid row by row and keep only the last row, but then you know only the length of the answer, not the answer.

Hirschberg's idea is to cut the first word in the middle. A best answer uses some of the second word for the first half and the rest for the second half. One pass from the top and one pass from the bottom, each keeping only one row, tell you where to cut the second word. Then solve the two smaller pairs in the same way and join the two answers.

## The problem

The input is two sequences $X = \langle x_1, \ldots, x_m \rangle$ and $Y = \langle y_1, \ldots, y_n \rangle$ over a set with an equality test. The output is one common subsequence of maximum length. This is the [longest common subsequence](/longest-common-subsequence/) problem, with the extra goal of space linear in the input.

## The algorithm

Write $\mathrm{lcs}(U, V)$ for the LCS length, $U^R$ for the reverse of $U$, and $Y[a \ldots b]$ for the factor $y_a \cdots y_b$ (empty if $a > b$). LCS-ROW is the [LCS table](/lcs-dynamic-programming/) fill with a [rolling array](/rolling-array-space-reduction/): it keeps one row $R$ and the old value of the cell up and to the left in a variable.

```pseudo id=main
HIRSCHBERG(X[1 .. m], Y[1 .. n])
L1  if m = 0 or n = 0 then return the empty sequence
L2  if m = 1 then return ⟨x_1⟩ if x_1 occurs in Y, else the empty sequence
L3  h ← ⌊m / 2⌋
L4  F ← LCS-ROW(X[1 .. h], Y)                        ▷ F[j] = lcs(X[1 .. h], Y[1 .. j])
L5  B ← LCS-ROW(X[h + 1 .. m]^R, Y^R)                ▷ B[j] = lcs(X[h + 1 .. m], Y[n − j + 1 .. n])
L6  k ← the largest j in 0 .. n that maximizes F[j] + B[n − j]
L7  return HIRSCHBERG(X[1 .. h], Y[1 .. k]) followed by HIRSCHBERG(X[h + 1 .. m], Y[k + 1 .. n])

LCS-ROW(X[1 .. m], Y[1 .. n])                        ▷ returns R[0 .. n] with R[j] = lcs(X, Y[1 .. j])
L8  R[0 .. n] ← 0
L9  for i ← 1 to m do
L10     diag ← 0                                 ▷ old R[j − 1], the cell up and to the left
L11     for j ← 1 to n do
L12         up ← R[j]
L13         if X[i] = Y[j] then R[j] ← diag + 1 else R[j] ← max(up, R[j − 1])
L14         diag ← up
L15 return R
```

Line L5 runs the same fill on the reversed sequences. Since a sequence $Z$ is a subsequence of $U$ exactly when $Z^R$ is a subsequence of $U^R$, the value $B[n - j]$ is the LCS length of the bottom half $X[h+1 \ldots m]$ and the suffix $Y[j+1 \ldots n]$. Line L6 picks the column where an optimal path crosses from the top half to the bottom half. The two recursive calls of line L7 get disjoint parts of $X$ and of $Y$, and their outputs are concatenated. Any tie rule in line L6 is correct; the largest index is the rule of the implementation.

## Example

Take $X = \text{ABCBDAB}$ and $Y = \text{BDCABA}$, the example of the [LCS table](/lcs-dynamic-programming/) page, with $\mathrm{lcs}(X, Y) = 4$. Here $m = 7$, so $h = 3$, the top half is ABC and the bottom half is BDAB.

| $j$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $Y[1 \ldots j]$ | | B | BD | BDC | BDCA | BDCAB | BDCABA |
| $F[j]$ = lcs(ABC, $Y[1 \ldots j]$) | 0 | 1 | 1 | 2 | 2 | 2 | 2 |
| $B[6 - j]$ = lcs(BDAB, $Y[j+1 \ldots 6]$) | 4 | 3 | 2 | 2 | 2 | 1 | 0 |
| $F[j] + B[6 - j]$ | 4 | 4 | 3 | 4 | 4 | 3 | 2 |

The maximum 4 is the LCS length, as it must be. The largest maximizing column is $k = 4$, so the calls are on (ABC, BDCA) and (BDAB, BA). The recursion tree, with the split $k$ of each call:

| call | $h$ | $k$ | result |
| --- | --- | --- | --- |
| (ABCBDAB, BDCABA) | 3 | 4 | BC followed by BA = BCBA |
| (ABC, BDCA) | 1 | 0 | (A, empty) and (BC, BDCA) |
| (BC, BDCA) | 1 | 2 | B from (B, BD) and C from (C, CA) |
| (BDAB, BA) | 2 | 1 | (BD, B) and (AB, A) |
| (BD, B) | 1 | 1 | B from (B, B), and (D, empty) |
| (AB, A) | 1 | 1 | A from (A, A), and (B, empty) |

The output is BCBA, an LCS of length 4. The calls fill 74 cells in total, against $mn = 42$ cells for one fill of the full table.

## Correctness

The method rests on one split lemma: for each $0 \le h \le m$,

$$\mathrm{lcs}(X, Y) = \max_{0 \le j \le n} \big( \mathrm{lcs}(X[1 \ldots h], Y[1 \ldots j]) + \mathrm{lcs}(X[h+1 \ldots m], Y[j+1 \ldots n]) \big).$$

The right side is at most the left side, because two common subsequences of the two parts, joined, are a common subsequence of $X$ and $Y$. For the other direction, take an LCS with a matching of index pairs, and let $j$ be the largest $Y$ index that is matched with an $X$ index at most $h$ (or $j = 0$). The pairs with $X$ index at most $h$ lie in the top-left block, and the others have $Y$ index above $j$, so they lie in the bottom-right block. LCS-ROW returns the last row of the [LCS table](/lcs-dynamic-programming/) by the same induction as the full fill, so $F$ and $B$ hold the two terms. Then induction on $m$ shows that HIRSCHBERG returns a common subsequence of length $\mathrm{lcs}(X, Y)$: the calls of line L7 return LCSs of the two blocks, and their lengths add up to $F[k] + B[n - k] = \mathrm{lcs}(X, Y)$. The full proof is in the proof file.

## Complexity

- **Time.** A call with $m \ge 2$ fills $h n + (m - h) n = mn$ cells in lines L4 and L5. Its two children have $\lceil m/2 \rceil$ or fewer rows each and their columns add up to $n$, so by induction the total number of cells is at most $n (m + \lceil m/2 \rceil + \lceil m/4 \rceil + \cdots) < n (2m + \log_2 m)$. Lines L1, L2 and L6 cost $O(n' + 1)$ in a call with $n'$ columns. The calls of one level of the recursion have disjoint columns, there are $\lceil \log_2 m \rceil + 1$ levels and fewer than $2m$ calls, so this adds $O(m + n \log m)$, which is $O(mn)$. The total is $\Theta(mn)$: at least the $mn$ cells of the top call and less than about $2mn$ cells in all. Kleinberg and Tardos give the same bound with the recurrence $T(m, n) \le cmn + T(m/2, k) + T(m/2, n - k)$.
- **Space.** LCS-ROW keeps one row of $n + 1$ numbers, and the rows of a call are freed before its children run. The recursion has depth $\lceil \log_2 m \rceil$, and each frame keeps $O(1)$ indices if the subsequences are passed as index ranges. With the output, the space is $\Theta(m + n)$.
- **Shorter side.** Swap the inputs so that the row has length $\min(m, n)$ and the recursion halves the longer sequence. The work space for the rows is then $\Theta(\min(m, n))$.

## Properties

- **Equality only.** Like the table, it needs only equality tests on the items.
- **Deterministic and oblivious in the first level.** The top call always fills exactly $mn$ cells; the deeper calls depend on the splits.
- **Not adaptive.** Equal inputs still cost $\Theta(mn)$ time.
- **Same answer set.** The output is an LCS, but often a different one from the traceback of the full table. On the example both give BCBA.
- **Parallel halves.** The two passes of lines L4 and L5 are independent, and so are the two calls of line L7.

## Variants and improvements

- **Alignment and edit distance.** The split lemma holds for each score that adds up along a path of the grid, so the same method gives linear-space [global alignment](/global-alignment/) for [Needleman-Wunsch](/needleman-wunsch/) scores and a linear-space [edit distance](/edit-distance/) script. Myers and Miller extended it to affine gap costs.
- **With Myers' algorithm.** Myers' $O((n + m) D)$ difference algorithm uses the same idea with a "middle snake" to find a shortest edit script in linear space; see [Myers' diff algorithm](/myers-diff/).
- **Faster rows.** LCS-ROW can be replaced by any method that returns the last row, for example the [bit-parallel](/bit-parallel-lcs/) row, to get $O(mn / w)$ word operations for the lengths.

## When to use it

Use it when you need an LCS or an alignment itself, not only its length, and the full table does not fit in memory: for example two sequences of $10^5$ items, whose table has $10^{10}$ cells. If the table fits, the plain [LCS table](/lcs-dynamic-programming/) is simpler and about twice as fast. If the inputs are long but similar, [Myers' algorithm](/myers-diff/) in linear space is faster.

## Pitfalls

- **Copies of the inputs.** Passing slices copies $X$ and $Y$ at each level, which costs $O((m + n) \log m)$ space in the worst case. Pass index ranges to keep the space linear. The Python implementation uses slices for clarity.
- **Wrong reverse row.** $B$ must be the LCS of the bottom half with each *suffix* of $Y$, so both $X[h+1 \ldots m]$ and $Y$ must be reversed. Reversing only one gives wrong values.
- **The index shift.** $F[j]$ is paired with $B[n - j]$, not with $B[j]$.
- **Base case.** With $m = 1$, line L4 gets an empty top half; without the base case of line L2, the recursion on $(X, Y)$ with $h = 0$ does not terminate.

## Implementations

## History

Hirschberg published the linear-space method in Communications of the ACM in 1975, for maximal common subsequences. The same divide and conquer applies to sequence alignment; Myers and Miller (1988) gave it for affine gap costs, and textbooks such as Kleinberg and Tardos and Gusfield present it for alignment.

## References
