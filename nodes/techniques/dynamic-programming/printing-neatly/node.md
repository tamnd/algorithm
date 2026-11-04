---
tag: R1T36V
kind: problem
slug: printing-neatly
name: Printing neatly (optimal line breaking)
aliases:
- Printing neatly
area: techniques/dynamic-programming
level: core
summary: Breaking a paragraph of words into lines to minimize the total penalty from extra spaces, solved by dynamic programming.
prereqs: [optimal-substructure, tabulation, traceback]
see_also: [optimal-text-wrapping, knuth-plass-line-breaking, text-segmentation, greedy-algorithm, dp-on-dag, monge-property, segmented-least-squares]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 14, end-of-chapter problems, Printing neatly
---

Printing neatly is the line breaking problem as CLRS states it in the problems of its dynamic programming chapter. A paragraph of $n$ words with lengths $l_1, \ldots, l_n$ is printed in a monospaced font on lines of at most $M$ characters, with one space between words on a line. A line that holds words $i$ through $j$ has $M - j + i - \sum_{k=i}^{j} l_k$ extra spaces at its end, which must be nonnegative. The goal is to minimize the sum of the **cubes** of the extra spaces over all lines except the last. A dynamic program over the suffixes of the paragraph solves it in $O(n^2)$ time, or $O(nM)$, while the greedy rule that fills each line as far as it can is not optimal. This page is about that one instance. The general problem with any line cost is [optimal text wrapping](/optimal-text-wrapping/), and the method that TeX uses, with stretchable spaces and hyphens, is the [Knuth-Plass algorithm](/knuth-plass-line-breaking/).

## In plain words

You type a paragraph on a screen where every letter has the same width, and each line holds at most $M$ letters. You may only break lines between words. A line that ends far from the right edge looks bad, and the cost grows fast with the gap: a gap of 4 costs 64, but two gaps of 2 cost only 16. The last line is free, because it is normal for it to be short.

Filling each line as much as possible is the obvious plan, but it can leave one very bad line later. Instead, find the best way to print the words from $i$ to the end, for every $i$, starting at the last word. For each $i$, try every possible first line, add its cost to the stored best cost of the rest, and keep the smallest.

## Definition

**Input.** Word lengths $l_1, \ldots, l_n \ge 1$ and a line width $M$ with $M \ge l_k$ for all $k$.

**Lines.** For $i \le j$, let $e(i, j) = M - (j - i) - \sum_{k=i}^{j} l_k$, the extra spaces of a line with words $i$ to $j$. The line fits if $e(i, j) \ge 0$.

**Cost of a line.**

$$\text{lc}(i, j) = \begin{cases} \infty & \text{if } e(i, j) < 0, \\ 0 & \text{if } j = n \text{ and } e(i, j) \ge 0, \\ e(i, j)^3 & \text{otherwise.} \end{cases}$$

**Output.** Break points $0 = b_0 < b_1 < \cdots < b_t = n$ that minimize $\sum_{s=1}^{t} \text{lc}(b_{s-1} + 1, b_s)$, where line $s$ holds words $b_{s-1} + 1$ to $b_s$.

## Variants

- **Other powers.** The square of the extra spaces gives the "minimum raggedness" form; any convex function of the extra spaces works the same way. See [optimal text wrapping](/optimal-text-wrapping/).
- **Count the last line.** Charging the last line too favors a long last line; the dynamic program only changes in its base case.
- **Fewest lines.** With cost 1 per line, the greedy rule is optimal; see [optimal text wrapping](/optimal-text-wrapping/).
- **Proportional fonts and stretchable spaces.** Real typesetting measures widths in points and lets spaces stretch and shrink, which is the setting of the [Knuth-Plass algorithm](/knuth-plass-line-breaking/).

## Examples

**A short case.** Words `aaa bb cc ddddd` with $M = 6$. The greedy rule puts `aaa bb` on the first line (0 extra spaces), then `cc` alone, since `cc ddddd` needs 8 characters, and then `ddddd`. Its cost is $0^3 + 4^3 = 64$. The layout `aaa` / `bb cc` / `ddddd` costs $3^3 + 1^3 = 28$, which is optimal.

**A sentence.** The 12 words of "Dynamic programming finds the best way to break a paragraph into lines" with $M = 19$:

| optimal, cost 375 | extra | greedy, cost 855 | extra |
|---|---|---|---|
| `Dynamic programming` | 0 | `Dynamic programming` | 0 |
| `finds the best` | 5 | `finds the best way` | 1 |
| `way to break a` | 5 | `to break a` | 9 |
| `paragraph into` | 5 | `paragraph into` | 5 |
| `lines` | free | `lines` | free |

The optimum is $0 + 125 + 125 + 125 = 375$. The greedy layout costs $0 + 1 + 729 + 125 = 855$: its second line is very full, which leaves a gap of 9 on the third. Both use 5 lines.

The table $c[i]$ of the algorithm below, the least cost of words $i$ to 12, with the last word of the best first line:

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| word | Dynamic | programming | finds | the | best | way | to | break | a | paragraph | into | lines |
| $c[i]$ | 375 | 80 | 375 | 72 | 35 | 250 | 854 | 8 | 27 | 125 | 0 | 0 |
| line ends at | 2 | 3 | 5 | 7 | 8 | 9 | 9 | 10 | 11 | 11 | 12 | 12 |

For example, $c[3] = \min(e^3 + c[j + 1])$ over the lines that start at `finds`: ending at word 3 gives $14^3 + 72 = 2816$, at word 4 gives $10^3 + 35 = 1035$, at word 5 gives $5^3 + 250 = 375$, and at word 6 gives $1 + 854 = 855$, which is the greedy choice. A search over all $2^{11}$ sets of break points confirms 375.

## Known algorithms

**Dynamic program over suffixes.** Let $c[i]$ be the least cost to print words $i, \ldots, n$, with $c[n + 1] = 0$. The first line of an optimal layout of words $i, \ldots, n$ holds words $i$ to $j$ for some $j$, and the rest is a layout of words $j + 1, \ldots, n$, which must itself be optimal or the whole could be improved (the [cut-and-paste argument](/cut-and-paste-argument/)). So

$$c[i] = \min_{i \le j \le n,\; e(i, j) \ge 0} \bigl( \text{lc}(i, j) + c[j + 1] \bigr),$$

and the answer is $c[1]$. Fill $c$ for $i = n$ down to 1, and store the best $j$ for each $i$; following these from $i = 1$ gives the lines (see [traceback](/traceback/)).

**Cost.** For each $i$, increase $j$ and update $e(i, j)$ by subtracting $l_j + 1$; stop as soon as it is negative. Each line holds at most $\lceil M/2 \rceil$ words, since each word takes at least one character and one space, so the inner loop runs at most $\min(n, \lceil M / 2 \rceil)$ times. The time is $O(n \min(n, M))$ and the space is $O(n)$. CLRS asks for this algorithm and its time and space.

**Faster.** The cost $\text{lc}$ satisfies the [quadrangle inequality](/monge-property/), so the recurrence is a concave least weight subsequence problem and can be solved in $O(n)$ time with matrix searching. The proof and the methods are on [optimal text wrapping](/optimal-text-wrapping/).

## Bounds

- $O(n \min(n, M))$ time and $O(n)$ space by the dynamic program.
- $O(n)$ time by the methods for concave least weight subsequence problems.
- $\Omega(n)$, since every word length must be read.

## Reductions

- **To a shortest path.** Make vertices $1, \ldots, n + 1$ and an edge $i \to j + 1$ of weight $\text{lc}(i, j)$ for each line that fits. A layout is a path from 1 to $n + 1$, and the dynamic program is a shortest path in this [DAG](/dp-on-dag/).
- **A special case of the least weight subsequence problem**, the general form treated on [optimal text wrapping](/optimal-text-wrapping/).
- **Same shape as other cut problems.** [Text segmentation](/text-segmentation/) and [segmented least squares](/segmented-least-squares/) also cut a sequence into consecutive pieces with a cost per piece.

## Applications

- **Text in monospaced output**, such as terminal programs and plain text email, where a short program can wrap paragraphs better than the greedy rule.
- **Teaching.** It is a standard exercise in choosing the subproblem (the suffixes), in handling the special last line, and in seeing why greedy fails for a convex cost.

## References
