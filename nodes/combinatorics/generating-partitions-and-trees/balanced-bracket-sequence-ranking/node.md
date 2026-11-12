---
tag: 6BDKZQ
kind: algorithm
slug: balanced-bracket-sequence-ranking
name: Ranking balanced bracket sequences
aliases:
- Number of the balanced bracket sequence
- Rank of a Dyck word
area: combinatorics/generating-partitions-and-trees
level: core
summary: Algorithm that computes the lexicographic index of a given balanced bracket sequence among all balanced sequences of its length.
solves: [balanced-parentheses-generation]
model: word-ram
complexity:
  vars: {n: the number of bracket pairs}
  time: {worst: Θ(n^2), best: Θ(n^2)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [dyck-word, lexicographic-order, ranking-unranking]
see_also: [kth-balanced-bracket-sequence, next-balanced-bracket-sequence, balanced-parentheses-generation, permutation-ranking, combinatorial-number-system, ballot-theorem, counting-balanced-bracket-sequences, combinatorial-ranking-and-unranking]
sources:
  - url: https://cp-algorithms.com/combinatorics/bracket_sequences.html
    title: cp-algorithms, Balanced bracket sequences
    locator: the section Sequence index (the table d of completions and the sum over the closing brackets)
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Section 4.6.1, Binary Trees, Ordered Trees (ranking as a sum of edge labels of a lattice walk, Figure 4.7)
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration and Search, CRC Press, 1999
    locator: Chapter 3, the section on Catalan families (ranking and unranking)
---

Ranking a balanced bracket sequence computes the 0-based position of a [Dyck word](/dyck-word/) $s$ of length $2n$ in the [lexicographic order](/lexicographic-order/) of all $C_n$ Dyck words of that length, with $\texttt{(} < \texttt{)}$. It reads $s$ once from left to right, and at each closing bracket it adds the number of balanced words that have the same prefix but an opening bracket there. These numbers come from a table of [ballot numbers](/ballot-theorem/) of size $\Theta(n^2)$, built once. The inverse map is [unranking](/kth-balanced-bracket-sequence/), and the pair is an instance of [ranking and unranking](/ranking-unranking/).

## In plain words

Write down all correct bracket strings of one length in dictionary order, with the opening bracket first, and number them from 0. The rank of a string is its number in this list. You want it without writing the list.

Read the string from the left. Each time you see a closing bracket, every correct string that has the same start but an opening bracket here comes earlier in the list. Count those strings and add the count. The count depends only on how many cells are left and how many brackets are open, so a small table, filled in once, gives each count in one step. The sum of all the counts is the rank.

## The problem

The input is a word $s[1 \ldots m]$ with $m = 2n$ in the set $D_n$ of balanced words of semilength $n$. The output is $\mathrm{rank}(s) = \#\{v \in D_n : v < s\}$, an integer in $[0, C_n)$, where $C_n = \frac{1}{n+1}\binom{2n}{n}$ is the [Catalan number](/catalan-numbers/) and $<$ is lexicographic order with $\texttt{(} < \texttt{)}$.

## The algorithm

Let $d[i][j]$ be the number of ways to finish from height $j$ with $i$ cells: the number of words $y$ of length $i$ such that the height, starting at $j$ and moving by $+1$ for $\texttt{(}$ and $-1$ for $\texttt{)}$, never goes below 0 and ends at 0. The table follows from the first letter of $y$:

$$d[0][0] = 1, \quad d[0][j] = 0 \ (j \ge 1), \qquad d[i][j] = d[i-1][j+1] + [\,j \ge 1\,]\, d[i-1][j-1] \ (i \ge 1).$$

It has the closed form $d[i][j] = \binom{i}{u} - \binom{i}{u-1}$ with $u = (i - j)/2$ when $i - j$ is even and $0 \le j \le i$, and $d[i][j] = 0$ otherwise, by the [reflection principle](/reflection-principle/). In particular $d[2n][0] = C_n$.

```pseudo id=main
RANK(s)                          ▷ s[1 .. m] is balanced, m = 2n
L1  d ← the table above, for 0 ≤ i ≤ m and 0 ≤ j ≤ m + 1
L2  r ← 0, h ← 0
L3  for i ← 1 to m do
L4      if s[i] = '(' then h ← h + 1
L5      else r ← r + d[m − i][h + 1]      ▷ same prefix, '(' at position i
L6           h ← h − 1
L7  return r
```

The variable $h$ is the height of the prefix $s[1 \ldots i-1]$. A word with this prefix and $\texttt{(}$ at position $i$ is at height $h + 1$ with $m - i$ cells left, so line L5 adds the number of ways to finish from there.

## Example

The table $d[i][j]$ for $m = 8$ (rows $i = 0$ to 8, columns $j = 0$ to 8; the empty cells are 0):

| $i$ | $j{=}0$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | | | | | | | | |
| 1 | | 1 | | | | | | | |
| 2 | 1 | | 1 | | | | | | |
| 3 | | 2 | | 1 | | | | | |
| 4 | 2 | | 3 | | 1 | | | | |
| 5 | | 5 | | 4 | | 1 | | | |
| 6 | 5 | | 9 | | 5 | | 1 | | |
| 7 | | 14 | | 14 | | 6 | | 1 | |
| 8 | 14 | | 28 | | 20 | | 7 | | 1 |

Rank $s$ = `()(())()`, with $n = 4$. The column "added" is $d[8 - i][h + 1]$ at a closing bracket, with $h$ the height before position $i$.

| $i$ | $s[i]$ | $h$ before | added | $r$ |
|---|---|---|---|---|
| 1 | `(` | 0 | 0 | 0 |
| 2 | `)` | 1 | $d[6][2] = 9$ | 9 |
| 3 | `(` | 0 | 0 | 9 |
| 4 | `(` | 1 | 0 | 9 |
| 5 | `)` | 2 | $d[3][3] = 1$ | 10 |
| 6 | `)` | 1 | $d[2][2] = 1$ | 11 |
| 7 | `(` | 0 | 0 | 11 |
| 8 | `)` | 1 | $d[0][2] = 0$ | 11 |

The rank is 11. The 9 words added at $i = 2$ are the 9 words that start with `((`, ranks 0 to 8. The word at $i = 5$ is `()((()))` and the word at $i = 6$ is `()(()())`.

## Correctness

A word $v < s$ differs first from $s$ at some index $i$, and there $v_i = \texttt{(}$ and $s_i = \texttt{)}$. So the words below $s$ split into disjoint groups, one for each closing bracket of $s$, and the group of index $i$ has exactly $d[m-i][h_{i-1} + 1]$ words. Line L5 adds the size of each group once. The table entries count the ways to finish by induction on $i$, splitting by the first letter. Since lexicographic order is total, the rank is a bijection from $D_n$ onto $\{0, \ldots, C_n - 1\}$. The full proof is below.

## Complexity

- **The table.** It has $(m + 1)(m + 2) = \Theta(n^2)$ entries, each one addition, so it takes $\Theta(n^2)$ additions and $\Theta(n^2)$ space. It depends only on $n$, so many calls can share it.
- **The scan.** Given the table, lines L2 to L7 take $\Theta(n)$ additions.
- **Size of the numbers.** Line L5 only reads entries $d[i][j]$ with $i + j \le m$. Each of these counts words with a fixed prefix, so it is at most $C_n < 4^n$, and $r < C_n$. Each such number has at most $2n$ bits, and for $n \le 35$ it fits in a signed 64-bit integer. For larger $n$ the additions are on big integers of $O(n)$ bits, so the scan costs $O(n^2)$ bit operations.
- **Without a table.** Compute $d[m-i][h+1]$ from the closed form. When $i$ grows by 1 and $h$ changes by 1, the two binomial coefficients change by $O(1)$ multiplications and divisions by small integers, so the rank takes $O(n)$ arithmetic operations and $O(1)$ stored numbers.

## Properties

- **Order preserving.** For $s, t \in D_n$, $s < t$ if and only if $\mathrm{rank}(s) < \mathrm{rank}(t)$.
- **First and last.** $\mathrm{rank}(\texttt{(}^n\texttt{)}^n) = 0$, since no closing bracket has a smaller choice that adds anything, and $\mathrm{rank}((\texttt{()})^n) = C_n - 1$.
- **One pass.** The input is read once, from left to right, so the rank of a stream can be computed with $O(n)$ arithmetic operations and the table.

## Variants and improvements

- **Unranking.** The inverse map: go from left to right and choose $\texttt{(}$ when $k$ is less than the number of ways to finish after it. See [k-th balanced bracket sequence](/kth-balanced-bracket-sequence/).
- **Several kinds of brackets.** With $t$ kinds, a word with $p$ open pairs and $i$ cells left has $d[i][p] \cdot t^{(i-p)/2}$ completions, since each pair still to open picks its kind. The same scan works with the order on all $2t$ symbols.
- **Other orders.** Ranking in the order of a Gray code, or of the Zaks sequence, uses the same idea of counting the words that branch off earlier, with other tables. See [Zaks' algorithm](/zaks-tree-generation/).
- **Trees.** Through the bijections of the [Dyck word](/dyck-word/) page, the same rank numbers binary trees with $n$ nodes and ordered trees with $n + 1$ nodes.

## When to use it

Use ranking to store a tree shape or a bracket word as one integer of about $2n$ bits, to index an array by tree shapes, or to split a listing of all words into equal parts for parallel work. To list all words in order, the [successor rule](/next-balanced-bracket-sequence/) is faster and needs no table.

## Pitfalls

- **Index of the table.** At position $i$ (1-based) the number of cells left after it is $m - i$, and the height after a hypothetical $\texttt{(}$ is $h + 1$. Using $h$ instead of $h + 1$ counts the wrong group.
- **Column $j = m + 1$.** The recurrence reads $d[i-1][j+1]$, so the table needs one column past $m$, or a bound check.
- **Overflow.** In a fixed-width language, $C_n$ overflows a signed 64-bit integer at $n = 36$. The full table holds even larger entries, for $i + j > m$, which RANK never uses; build only the entries with $i + j \le m$, or use big integers.
- **The other letter order.** With $\texttt{)} < \texttt{(}$ the ranks are $C_n - 1 - \mathrm{rank}(s)$. Mixing the two conventions gives reversed lists.

## Implementations

## History

Ruskey's book presents the rank as the sum of edge labels of a lattice walk, with the same counts as the table here. The table form with a sum over the closing brackets is the one in the cp-algorithms article.

## References
