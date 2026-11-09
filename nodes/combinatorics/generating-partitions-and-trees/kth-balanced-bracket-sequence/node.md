---
tag: 4XTB6R
kind: algorithm
slug: kth-balanced-bracket-sequence
name: k-th balanced bracket sequence
aliases:
- Unranking balanced bracket sequences
- Unrank a Dyck word
area: combinatorics/generating-partitions-and-trees
level: core
summary: Algorithm that builds the balanced bracket sequence at a given lexicographic position using dynamic programming counts of completions.
solves: [balanced-parentheses-generation]
model: word-ram
complexity:
  vars: {n: the number of bracket pairs}
  time: {worst: Θ(n^2), best: Θ(n^2)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [dyck-word, lexicographic-order, ranking-unranking]
see_also: [balanced-bracket-sequence-ranking, next-balanced-bracket-sequence, balanced-parentheses-generation, permutation-unranking, combinatorial-number-system, ballot-number, catalan-numbers, combinatorial-ranking-and-unranking]
sources:
  - url: https://cp-algorithms.com/combinatorics/bracket_sequences.html
    title: cp-algorithms, Balanced bracket sequences
    locator: the section Finding the k-th sequence (the table d and the choice at each position)
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Section 4.6.1, Binary Trees, Ordered Trees (ranking and unranking with O(n) arithmetic operations through a lattice walk, Figure 4.7)
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration and Search, CRC Press, 1999
    locator: Chapter 3, the section on Catalan families (ranking and unranking)
---

The $k$-th balanced bracket sequence algorithm builds the [Dyck word](/dyck-word/) of length $2n$ at 0-based position $k$ in the [lexicographic order](/lexicographic-order/) of all $C_n$ Dyck words, with $\texttt{(} < \texttt{)}$. It writes the word from left to right. At each position it counts the balanced words that put an opening bracket there, and it takes the opening bracket if $k$ is below that count, else it subtracts the count and takes the closing bracket. The counts come from a table of [ballot numbers](/ballot-number/) built once by dynamic programming. It is the inverse of [ranking](/balanced-bracket-sequence-ranking/).

## In plain words

Picture the full dictionary of correct bracket strings of one length, numbered from 0. You want the string with a given number, without making the dictionary.

The first character splits the dictionary into two blocks: the strings that start with an opening bracket, then the strings that start with a closing bracket. If you know the size of the first block, you know which block holds your number. If the number is in the second block, subtract the size of the first block. Then do the same for the second character inside the chosen block, and so on. The size of each block depends only on how many cells are left and how many brackets are open, so a small table gives it in one step.

## The problem

The input is $n \ge 0$ and an integer $k$ with $0 \le k < C_n$, where $C_n = \frac{1}{n+1}\binom{2n}{n}$ is the [Catalan number](/catalan-numbers/). The output is the word $s \in D_n$ that has exactly $k$ smaller words in $D_n$, the set of balanced words of semilength $n$ in lexicographic order with $\texttt{(} < \texttt{)}$.

## The algorithm

Let $d[i][j]$ be the number of ways to finish from height $j$ with $i$ cells: words of length $i$ whose height, starting at $j$, never goes below 0 and ends at 0. By the first letter,

$$d[0][0] = 1, \quad d[0][j] = 0 \ (j \ge 1), \qquad d[i][j] = d[i-1][j+1] + [\,j \ge 1\,]\, d[i-1][j-1] \ (i \ge 1),$$

and $d[2n][0] = C_n$.

```pseudo id=main
UNRANK(n, k)                     ▷ returns s[1 .. m], m = 2n
L1  d ← the table above, for 0 ≤ i ≤ m and 0 ≤ j ≤ m + 1
L2  if not 0 ≤ k < d[m][0] then error "k out of range"
L3  h ← 0
L4  for i ← 1 to m do
L5      c ← d[m − i][h + 1]          ▷ words with the prefix and '(' at i
L6      if k < c then
L7          s[i] ← '(', h ← h + 1
L8      else k ← k − c
L9          s[i] ← ')', h ← h − 1
L10 return s
```

At position $i$ the prefix $s[1 \ldots i-1]$ has height $h$. An opening bracket at $i$ gives height $h + 1$ with $m - i$ cells left, so line L5 counts the words of the first block. When $h + 1 > m - i$, the count is 0, and line L9 writes the forced closing bracket.

## Example

Find the word of rank $k = 7$ for $n = 4$. The table $d$ for $m = 8$ is on the [ranking page](/balanced-bracket-sequence-ranking/); its row 8 is $14, 0, 28, 0, 20, 0, 7, 0, 1$.

| $i$ | $h$ before | $c = d[8-i][h+1]$ | $k$ before | choice | $k$ after |
|---|---|---|---|---|---|
| 1 | 0 | $d[7][1] = 14$ | 7 | `(` | 7 |
| 2 | 1 | $d[6][2] = 9$ | 7 | `(` | 7 |
| 3 | 2 | $d[5][3] = 4$ | 7 | `)` | 3 |
| 4 | 1 | $d[4][2] = 3$ | 3 | `)` | 0 |
| 5 | 0 | $d[3][1] = 2$ | 0 | `(` | 0 |
| 6 | 1 | $d[2][2] = 1$ | 0 | `(` | 0 |
| 7 | 2 | $d[1][3] = 0$ | 0 | `)` | 0 |
| 8 | 1 | $d[0][2] = 0$ | 0 | `)` | 0 |

The result is `(())(())`. In the full list of 14 words it comes after `(((())))`, `((()()))`, `((())())`, `((()))()`, `(()(()))`, `(()()())` and `(()())()`, which are 7 words. At $i = 3$ the algorithm skips the 4 words that start with `(((`, and at $i = 4$ the 3 words that start with `(()(`.

## Correctness

Let $W(x)$ be the set of balanced words with prefix $x$, in lexicographic order. The list of $W(x)$ is the list of $W(x\texttt{(})$ followed by the list of $W(x\texttt{)})$, and $|W(x\texttt{(})|$ is the table entry of line L5. The loop keeps the invariant that the wanted word is at position $k$ of $W(s[1 \ldots i-1])$, with $0 \le k < |W(s[1 \ldots i-1])|$. Each step keeps it by choosing the block that holds position $k$. After $2n$ steps the set holds one word, which is the output. The full proof is below.

## Complexity

- **The table.** $(m + 1)(m + 2) = \Theta(n^2)$ entries, one addition each, in $\Theta(n^2)$ space. It depends only on $n$, so many calls can share it.
- **The loop.** $2n$ steps, each with one comparison and at most one subtraction, so $\Theta(n)$ arithmetic operations given the table.
- **Size of the numbers.** The entries read in line L5 have $i + j \le m$, so they are at most $C_n < 4^n$, and $k < C_n$. For $n \le 35$ they fit in a signed 64-bit integer. For larger $n$ each operation is on $O(n)$ bits, so the loop costs $O(n^2)$ bit operations.
- **Without a table.** The closed form $d[i][j] = \binom{i}{u} - \binom{i}{u-1}$ with $u = (i - j)/2$ can be updated in $O(1)$ multiplications and divisions per step, which gives $O(n)$ arithmetic operations and $O(1)$ stored numbers.

## Properties

- **Inverse of ranking.** UNRANK$(n, \mathrm{rank}(s)) = s$ for each $s \in D_n$, and $\mathrm{rank}(\mathrm{UNRANK}(n, k)) = k$ for each $0 \le k < C_n$.
- **Greedy with counts.** Each choice is final; the algorithm never backtracks.
- **Order preserving.** If $k < k'$, then UNRANK$(n, k)$ is lexicographically smaller than UNRANK$(n, k')$.

## Variants and improvements

- **Uniform random word.** Draw $k$ uniformly from $[0, C_n)$ and unrank it. This gives a uniform random Dyck word, and so a uniform random binary tree with $n$ nodes or ordered tree with $n + 1$ nodes.
- **Listing a range.** Unrank the first word of the range, then call the [successor rule](/next-balanced-bracket-sequence/) for the rest. This costs one unrank plus $O(1)$ amortized per word.
- **Restricted words.** For words with depth at most $b$, use the same recurrence with $d[i][j] = 0$ for $j > b$. For several kinds of brackets, multiply the counts by powers of the number of kinds.
- **Other Catalan objects.** Composing with the bijections of the [Dyck word](/dyck-word/) page unranks binary trees and ordered trees.

## When to use it

Use it to jump to a given position of the list, to split the list of all words into equal parts for parallel work, or to draw a uniform random word. To list all words, the successor rule is faster.

## Pitfalls

- **Out of range input.** For $k \ge C_n$ the loop still returns a string, but not a balanced one. Check $k < d[m][0]$ first.
- **Wrong block order.** With $\texttt{(} < \texttt{)}$ the block of $\texttt{(}$ comes first. If the opposite order is used, the test of line L6 must count the words with $\texttt{)}$ first.
- **Overflow.** In fixed-width integers, $C_n$ overflows a signed 64-bit integer at $n = 36$, and the full table has larger entries for $i + j > m$ that the loop never uses.
- **Rebuilding the table on each call.** Many calls with the same $n$ should share one table, or the $\Theta(n^2)$ table dominates the cost.

## Implementations

## History

The cp-algorithms article gives this table method for the $k$-th balanced sequence. Ruskey's book presents the same counts as edge labels of a lattice walk in the treatment of binary trees and ordered trees.

## References
