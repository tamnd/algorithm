---
tag: BRK0H7
kind: algorithm
slug: next-balanced-bracket-sequence
name: Lexicographically next balanced bracket sequence
aliases:
- Next Dyck word
- Lexicographic successor of a balanced bracket sequence
area: combinatorics/generating-partitions-and-trees
level: core
summary: Algorithm that produces the next balanced bracket sequence of the same length in lexicographic order by changing a suffix.
solves: [balanced-parentheses-generation]
model: word-ram
complexity:
  vars: {n: the number of bracket pairs}
  time: {worst: Θ(n), best: Θ(1), amortized: Θ(1)}
  space: {extra: Θ(1)}
properties: {in_place: true, deterministic: true, recursive: false}
history:
  year: 1977
  people: [Frank Ruskey, T. C. Hu]
  note: Ruskey and Hu published a lexicographic generation of binary trees in 1977.
prereqs: [dyck-word, lexicographic-order, lexicographic-successor]
see_also: [balanced-parentheses-generation, balanced-bracket-sequence-ranking, kth-balanced-bracket-sequence, next-permutation, zaks-tree-generation, constant-amortized-time-generation, ballot-number, binary-tree-generation]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.6, Generating all trees (Algorithm P, nested parentheses in lexicographic order)
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Section 4.6.1, Binary Trees, Ordered Trees (Algorithm 4.16 and Theorem 4.1), and the bibliographic remarks of Chapter 4
  - url: https://cp-algorithms.com/combinatorics/bracket_sequences.html
    title: cp-algorithms, Balanced bracket sequences
    locator: the section Finding the next balanced sequence
---

The next balanced bracket sequence algorithm takes a [Dyck word](/dyck-word/) of length $2n$ and returns the next Dyck word of the same length in [lexicographic order](/lexicographic-order/) with $\texttt{(} < \texttt{)}$, or reports that the word is the last one. It scans from the right for the last opening bracket that may turn into a closing bracket, turns it, and writes the least possible completion after it. One call takes $\Theta(n)$ time in the worst case, and the average over all $C_n$ words is less than $8 + 2n/C_n$ cells, so repeated calls [generate all balanced sequences](/balanced-parentheses-generation/) in constant amortized time.

## In plain words

The words are in dictionary order, with the opening bracket before the closing bracket. To get the next word, keep the longest possible start and make the first change as far to the right as you can.

The only useful change is to put a closing bracket where the word has an opening bracket. That is allowed only if some bracket is still open at that point, or the word would close more than it opened. So walk from the right end to the left, and keep a count of how many brackets are open at each point. Stop at the first opening bracket that has an open bracket before it. Turn it into a closing bracket. Then fill the rest with the smallest correct ending: all the remaining opening brackets first, then all the closing brackets.

## The problem

The input is a balanced word $s[1 \ldots m]$ with $m = 2n$, that is, a word in the set $D_n$ of Dyck words of semilength $n$. The output is the least word of $D_n$ that is greater than $s$ in lexicographic order with $\texttt{(} < \texttt{)}$, written over $s$, or the answer "none" when $s$ is the greatest word $(\texttt{()})^n$. The list starts at $\texttt{(}^n\texttt{)}^n$, so the loop "start there, call until false" lists $D_n$. This solves [generating balanced parentheses](/balanced-parentheses-generation/).

## The algorithm

The counter $d$ holds, at index $i$, the number of closing minus opening brackets in $s[i \ldots m]$. Since the whole word is balanced, after line L4 this is the height $h_{i-1}$ of the prefix $s[1 \ldots i-1]$, the number of brackets that are open just before position $i$.

```pseudo id=main
NEXT-BALANCED(s)                 ▷ s[1 .. m] is balanced, m = 2n
L1  d ← 0
L2  for i ← m downto 1 do
L3      if s[i] = ')' then d ← d + 1
L4      else d ← d − 1           ▷ d = height before position i
L5          if d > 0 then
L6              s[i] ← ')'
L7              p ← (m − i − d + 1) / 2      ▷ opening brackets after i
L8              s[i+1 .. i+p] ← '('
L9              s[i+p+1 .. m] ← ')'
L10             return true
L11 return false                 ▷ s = ()()...(), the last word
```

After line L6 the height is $d - 1$, and $m - i$ cells remain. A completion from height $d - 1$ in $m - i$ cells needs $p$ opening and $p + d - 1$ closing brackets, so $2p + d - 1 = m - i$, which is line L7. The value is an integer because $m - i - d + 1$ is even.

## Example

Take $n = 5$ and $s$ = `(()(()))()`, the word of rank 17 among the $C_5 = 42$ words. The table shows the scan. The value of $d$ is the value after line L3 or L4.

| $i$ | $s[i]$ | $d$ | action |
|---|---|---|---|
| 10 | `)` | 1 | go on |
| 9 | `(` | 0 | no open bracket before it, go on |
| 8 | `)` | 1 | go on |
| 7 | `)` | 2 | go on |
| 6 | `)` | 3 | go on |
| 5 | `(` | 2 | $d > 0$, stop |

Line L6 turns $s[5]$ into `)`, so the prefix is `(()()` at height 1. Line L7 gives $p = (10 - 5 - 2 + 1)/2 = 2$. Lines L8 and L9 write `((` in positions 6 and 7 and `)))` in positions 8 to 10. The result is `(()()(()))`, the word of rank 18.

## Correctness

The scan finds the largest index $i$ with $s[i] = \texttt{(}$ and $h_{i-1} \ge 1$. A larger balanced word must differ first from $s$ at such an index, where it has a closing bracket. The first difference at the largest such index gives the smallest larger words, and among them the least is the one with the least completion $\texttt{(}^p\texttt{)}^{p+d-1}$. If no such index exists, every opening bracket stands at height 0, so $s = (\texttt{()})^n$ is the last word. The full proof is below.

## Complexity

Let $\mathrm{cost}(s)$ be the number of cells that the call reads, $m - i + 1$ when it stops at $i$ and $m$ for the last word. Lines L6 to L9 write $m - i + 1$ cells, so the time is $\Theta(\mathrm{cost}(s))$, and the extra space is $\Theta(1)$.

- **Worst case $\Theta(n)$.** The word $\texttt{(())}(\texttt{()})^{n-2}$ stops at $i = 2$ and rewrites $2n - 1$ cells. The last word reads all $2n$ cells.
- **Best case $\Theta(1)$.** A word that ends in `())` stops at $i = m - 2$.
- **Amortized $\Theta(1)$.** Let $s \ne (\texttt{()})^n$ stop at $i$ with $d = h \ge 1$. Every opening bracket after $i$ stands at height 0, so $s$ ends with $\texttt{(}\,\texttt{)}^{h+1}(\texttt{()})^j$ for some $j \ge 0$, and $\mathrm{cost}(s) = h + 2 + 2j$. The next word ends with $\texttt{(}^{j+1}\texttt{)}^{j+h}$, so its final run of closing brackets has length $t = j + h$, and $\mathrm{cost}(s) \le 2t + 2$. The map from a word to the next word is one to one, so $\sum_s \mathrm{cost}(s) \le 2n + \sum_{v \in D_n} (2t(v) + 2)$.

Now count the final runs. A word $v$ has $t(v) \ge k$ when it is a prefix of length $2n - k$ that ends at height $k$, followed by $\texttt{)}^k$. Cut a nonnegative path of length $2n$ that ends at height 2 at its last up step: it is a nonnegative path of length $2n - k$ that ends at height $k$, then one up step, then $k - 1$ down steps, for a unique $k \ge 1$. So $\sum_v t(v) = \sum_{k \ge 1} \#\{v : t(v) \ge k\}$ equals the number of nonnegative paths of length $2n$ that end at height 2. By the [reflection principle](/reflection-principle/) this is the [ballot number](/ballot-number/) $\binom{2n}{n-1} - \binom{2n}{n-2} = \frac{3n}{n+2} C_n$. Hence

$$\sum_{s \in D_n} \mathrm{cost}(s) \le \Big(\frac{6n}{n+2} + 2\Big) C_n + 2n < 8 C_n + 2n.$$

So the full listing takes $\Theta(C_n)$ time, and the amortized cost per word is $O(1)$. The exact totals, for comparison:

| $n$ | $C_n$ | total cells read | average per word |
|---|---|---|---|
| 4 | 14 | 63 | 4.50 |
| 6 | 132 | 624 | 4.73 |
| 8 | 1430 | 6916 | 4.84 |
| 10 | 16796 | 82498 | 4.91 |
| 12 | 208012 | 1033410 | 4.97 |

## Properties

- **In place.** The call changes only the suffix $s[i \ldots m]$ and uses two counters.
- **No arithmetic on large numbers.** Unlike [unranking](/kth-balanced-bracket-sequence/), it needs no counts, so it works for any $n$ that fits in memory.
- **Not a Gray code.** One step can rewrite $2n - 1$ cells, so the algorithm is CAT but not loopless.
- **Same tree as backtracking.** The cells read in one step are the new nodes on the path to the next leaf of the pruned backtracking search with $\texttt{(}$ tried first.

## Variants and improvements

- **Previous word.** Swap the roles: scan from the right for the last closing bracket that may turn into an opening one, and write the greatest completion $\texttt{)}^h(\texttt{()})^a$.
- **The opposite letter order.** With $\texttt{)} < \texttt{(}$, as in Ruskey's bit strings with 1 for $\texttt{(}$ and 0 for $\texttt{)}$ ordered by $0 < 1$, the list is reversed. Ruskey's Algorithm 4.16 is the successor rule for that order.
- **Positions of the opening brackets.** Store the word as the increasing positions of its $n$ opening brackets. The successor then moves one position up by one and resets the positions after it. This is [Zaks' algorithm](/zaks-tree-generation/).
- **Direct access.** To jump to a given position in the list, use [unranking](/kth-balanced-bracket-sequence/); to find the position of a word, use [ranking](/balanced-bracket-sequence-ranking/).

## When to use it

Use it to list all balanced words of a fixed length one by one, with no recursion and $O(1)$ extra memory, for example to test code on every tree shape. Use it to resume a listing from any given word. If you need the word at a given position, unrank instead.

## Pitfalls

- **Missing the height test.** Turning an opening bracket at height 0 into a closing one gives a negative prefix. Line L5 must test $d > 0$ after the decrement of line L4.
- **The wrong fill.** The completion must use all the remaining opening brackets first. Filling with `()()` pairs gives the greatest completion, the result of the previous-word rule.
- **Off by one in line L7.** In 0-based code with indices $0$ to $m - 1$, the number of cells after $i$ is $m - 1 - i$, not $m - i$.
- **Copying each word.** Writing each word out costs $2n$ per word and hides the $O(1)$ amortized cost of the step.

## Implementations

## History

Ruskey and Hu published an algorithm that generates binary trees in lexicographic order in 1977, and Ruskey's 1978 thesis continued this work. Ruskey's book gives the successor rule for well-formed parentheses as Algorithm 4.16 and proves that it runs in constant amortized time, through the average level $\frac{3n}{n+2}$ of the leftmost leaf of a binary tree. Knuth gives the lexicographic generation of nested parentheses as Algorithm P in Section 7.2.1.6.

## References
