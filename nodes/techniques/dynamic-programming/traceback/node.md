---
tag: XFJT3K
kind: technique
slug: traceback
name: Traceback
aliases:
- Solution reconstruction by traceback
- alignment reconstruction
- backtrace
- parent pointers
- traceback
area: techniques/dynamic-programming
level: intro
summary: Recover the optimal alignment by following stored predecessor pointers through the DP table.
prereqs: [tabulation, optimal-substructure]
see_also: [rod-cutting-problem, lcs-dynamic-programming, matrix-chain-multiplication, needleman-wunsch, hirschberg-algorithm, rolling-array-space-reduction, dag-dynamic-programming, edit-distance]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.1 (EXTENDED-BOTTOM-UP-CUT-ROD and PRINT-CUT-ROD-SOLUTION), Section 14.2 (PRINT-OPTIMAL-PARENS) and Section 14.4 (PRINT-LCS)
  - book: isbn:9780321295354
    title: Kleinberg and Tardos, Algorithm Design
    locator: Section 6.1 (computing a solution in addition to its value), Section 6.6 (sequence alignment) and Section 6.7 (sequence alignment in linear space)
  - paper: doi:10.1145/360825.360861
    title: Daniel S. Hirschberg, A linear space algorithm for computing maximal common subsequences, Communications of the ACM 18(6), 1975
    locator: pp. 341 to 343
---

Traceback is the step of a dynamic program that recovers an optimal solution, not only its value: it starts at the final state and follows, one step at a time, the choice that gave each state its optimal value, back to a base case. The choices are either stored during the fill, as a table of predecessor or parent pointers, or recomputed from the table of values. For sequence alignment, the path that the traceback follows through the table is the optimal alignment itself. It costs time proportional to the length of the solution, but it needs the table, so a program that keeps only a few rows must use another method, such as [Hirschberg's algorithm](/hirschberg-algorithm/).

## In plain words

A table-filling program tells you the best score, for example the most money for a rod or the fewest edits between two words. Usually you also want the cuts or the edits themselves.

When the program fills a cell, it picks the best of a few options. Write down which option won, in a second table. At the end, start at the cell of the full answer. Read which option won there, and step to the cell that option came from. Do it again until you reach the start. The options you read, in reverse, are the best solution.

If you did not keep the second table, you can still do this. At each cell, try the options again and pick one that gives the stored score.

## When it applies

Look for these signals.

- A [tabulated](/tabulation/) or [memoized](/memoization/) dynamic program computes an optimal value, and the problem asks for an optimal object: a set of items, a path, a tree, an alignment.
- The value of each state is the best over a few choices, and each choice leads to one or more smaller states.
- The table of values, or a table of choices, is still in memory when the fill ends.

## The template

The holes are the states, the choices at a state, the function NEXT that gives the smaller states of a choice, the function COMBINE that gives the value of a choice, and the function EMIT that writes the part of the solution that a choice adds.

```pseudo id=main
FILL-WITH-CHOICES()
L1  for each state v in evaluation order do
L2      if v is a base state then val[v] ← base(v), continue
L3      val[v] ← best over choices c at v of COMBINE(c, val[NEXT(v, c)])
L4      choice[v] ← a choice c at which line L3 attains the best

TRACEBACK(v)
L5  while v is not a base state do
L6      c ← choice[v]                 ▷ or recompute: a c with COMBINE(c, val[NEXT(v, c)]) = val[v]
L7      EMIT(c)
L8      v ← NEXT(v, c)
```

Line L4 stores the winner of the comparison of line L3, so it costs only $O(1)$ extra time per state, and one extra table of the same size as $val$. TRACEBACK then follows a single path from the final state to a base state. It does $O(1)$ work per step with the stored choices, or $O(d)$ work per step when it recomputes them among $d$ choices. In both cases the cost is small next to the fill.

**Why it is correct.** Let $v_0$ be the final state and $v_{t+1} = \mathrm{NEXT}(v_t, c_t)$ where $c_t$ is the choice at $v_t$. By line L3 or L6, each $c_t$ attains $val[v_t]$. By induction from the base state backward, the choices $c_t, c_{t+1}, \ldots$ form an optimal solution of $v_t$: the base state is solved by its base value, and if the choices from $v_{t+1}$ on give the value $val[v_{t+1}]$, then adding $c_t$ gives $\mathrm{COMBINE}(c_t, val[v_{t+1}]) = val[v_t]$. For $t = 0$ this is an optimal solution of the whole problem. The loop stops because each step moves to a state that comes earlier in the evaluation order.

**The order of the output.** The traceback finds the last decision first. Either collect the emitted parts and reverse them at the end, or write the traceback as a recursion that calls itself first and emits after, which is what PRINT-LCS in CLRS Section 14.4 does.

**Trees.** When a choice leads to two smaller states, as a split in an [interval DP](/interval-dp/), the traceback is a recursion on both states. Its output is a tree, such as a parenthesization or a binary search tree.

## Classic examples

### Rod cutting

EXTENDED-BOTTOM-UP-CUT-ROD in CLRS Section 14.1 stores, for each length $j$, the size $s[j]$ of the first piece of an optimal cut. With the prices $p = (1, 5, 8, 9, 10, 17, 17, 20, 24, 30)$, the values and choices for $j = 0, \ldots, 10$ are:

| $j$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $r[j]$ | 0 | 1 | 5 | 8 | 10 | 13 | 17 | 18 | 22 | 25 | 30 |
| $s[j]$ | | 1 | 2 | 3 | 2 | 2 | 6 | 1 | 2 | 3 | 10 |

For $n = 7$ the traceback reads $s[7] = 1$, moves to $7 - 1 = 6$, reads $s[6] = 6$, and moves to 0. The cut is a piece of length 1 and a piece of length 6, for $1 + 17 = 18$. The table $s$ takes the first maximum in the order $i = 1, 2, \ldots$. Another tie rule can give the cut $2 + 2 + 3$, which also has revenue $5 + 5 + 8 = 18$. See the [rod cutting problem](/rod-cutting-problem/).

### Longest common subsequence

For $X = \mathrm{ABCBDAB}$ and $Y = \mathrm{BDCABA}$, the example of CLRS Section 14.4, the LCS length is 4. The traceback starts at the cell $(7, 6)$. When $x_i = y_j$ it emits the letter and moves to $(i-1, j-1)$. Otherwise it moves to the neighbor $(i-1, j)$ or $(i, j-1)$ with the larger value. When the two neighbors are equal, the rule "go up" gives BCBA and the rule "go left" gives BDAB. The strings have three different LCSs in all: BCAB, BCBA and BDAB. CLRS stores arrows in a table $b$, and its Exercise 14.4-2 asks for the traceback from the table $c$ alone, which is the recompute form. See [LCS by dynamic programming](/lcs-dynamic-programming/).

### Matrix-chain multiplication

MATRIX-CHAIN-ORDER in CLRS Section 14.2 stores in $s[i, j]$ the split point $k$ of an optimal product of $A_i \cdots A_j$. PRINT-OPTIMAL-PARENS prints "(", recurses on $(i, s[i,j])$ and on $(s[i,j] + 1, j)$, and prints ")". For the dimensions $30, 35, 15, 5, 10, 20, 25$, the least cost is 15125 scalar multiplications, $s[1, 6] = 3$, and the traceback prints $((A_1(A_2A_3))((A_4A_5)A_6))$. This is the tree form. See [matrix-chain multiplication](/matrix-chain-multiplication/).

### Sequence alignment

In [edit distance](/edit-distance/) and in [global alignment](/global-alignment/) by [Needleman-Wunsch](/needleman-wunsch/), the cell $(i, j)$ came from $(i-1, j-1)$ (a match or a substitution, written as two letters in one column), from $(i-1, j)$ (a gap in the second string) or from $(i, j-1)$ (a gap in the first). The traceback path from $(m, n)$ to $(0, 0)$ is the alignment, column by column from the right. For SNOWY and SUNNY the distance is 3. A traceback that prefers the diagonal gives the alignment of SNOWY over SUNNY with three substitutions. A traceback that prefers gaps can give

```
S - N O W Y
S U N N - Y
```

which also costs 3: one insertion, one substitution and one deletion. In [local alignment](/smith-waterman/) the traceback starts at the cell of the largest value and stops at the first cell of value 0, not at $(0, 0)$.

## Variations

- **Stored choices or recomputed choices.** Storing costs one more table and saves the work of trying the choices again. Recomputing uses no extra table, but it needs the values of all neighbor states, and with floating-point scores an exact equality test can fail.
- **Pointers in memoized code.** A top-down program stores the choice next to the memoized value. Every state on the optimal path has been computed, because the value of the final state used it.
- **All optimal solutions.** Keep every choice that attains the best, not only one. The kept choices form a DAG of optimal choices, and each path in it is an optimal solution. Counting these paths is a [path count on a DAG](/dp-on-dag/). Listing them can take exponential time, because the number of optimal solutions can be exponential.
- **Linear space.** When the table is too large to keep, [Hirschberg's algorithm](/hirschberg-algorithm/) (Hirschberg 1975, and Kleinberg and Tardos Section 6.7) finds the middle cell of an optimal path with two linear-space passes, one forward and one backward, and then recurses on the two halves. It finds an optimal alignment in $O(mn)$ time and $O(m + n)$ space. See also [Hirschberg for LCS](/hirschberg-lcs/).
- **Traceback for k best solutions.** Keep the $k$ best values per state, with their choices, and trace each of them. The fill then costs about $k$ times more.

## Pitfalls

- **A choice table that does not match the values.** Lines L3 and L4 must come from the same comparison. A common bug computes the value with `max(...)` and then sets the choice in a separate loop with a strict test against a stale best. The choice can then stay at its initial value, which is not a valid choice. Set the value and the choice in the same branch.
- **Ties and tests.** Different tie rules give different optimal solutions, as the LCS and the rod examples show. A test must check that the output is valid and has the optimal value, not that it equals one fixed answer.
- **The table is gone.** A [rolling array](/rolling-array-space-reduction/) keeps only the last rows. After the fill, the traceback has nothing to read. Keep the choices in a separate full table (they often fit in fewer bits than the values), or use Hirschberg's method.
- **Deep recursion.** A recursive traceback for two strings of length $10^5$ has depth up to $2 \cdot 10^5$, which overflows the default stack of many languages. Use a loop and a list, then reverse the list.
- **Off by one between the table and the input.** The table has a row and a column for the empty prefix, so the cell $(i, j)$ talks about the letters $x[i-1]$ and $y[j-1]$ in a zero-based string. Emitting $x[i]$ is a common bug.
- **Forgetting the start rule.** In local alignment and in problems whose answer is the best over many final states, the traceback must start at the state that holds the best value, not at the last cell.

## Exercises

1. For the rod prices above, change the tie rule of line L4 to the last maximum in the order $i = 1, 2, \ldots$. Give the cut for $n = 7$ and for $n = 10$.
2. Write the traceback of LCS without the arrow table, using only the table of lengths. Prove that it takes $O(m + n)$ time.
3. Prove that every optimal parenthesization appears as the output of PRINT-OPTIMAL-PARENS for some choice of $s$ among the optimal split points.
4. For the knapsack table $K[i][c]$, write a traceback that returns the chosen items. Explain why it needs the full table and not only the last row.
5. Give a family of string pairs whose number of different optimal alignments grows exponentially with the length.
   <details><summary>Hint</summary>Align $\mathrm{A}^n$ with $\mathrm{B}^n$ under unit costs for gaps and a substitution cost of 2.</details>
6. Write a traceback that counts the optimal alignments of two strings instead of listing them, in $O(mn)$ time.

## References
