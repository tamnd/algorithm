---
tag: B5EH8D
kind: technique
slug: tabulation
name: Tabulation (bottom-up dynamic programming)
aliases:
- bottom-up dynamic programming
area: techniques/dynamic-programming
level: intro
summary: Fill a table of subproblem values in dependency order instead of recursing.
prereqs: [optimal-substructure, overlapping-subproblems, topological-sort]
see_also: [memoization, subproblem-graph, rolling-array-space-reduction, traceback, dag-dynamic-programming, lcs-dynamic-programming, knapsack-dynamic-programming, rod-cutting-problem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.1 (BOTTOM-UP-CUT-ROD and the bottom-up method), Section 14.2 (MATRIX-CHAIN-ORDER) and Section 14.4 (LCS-LENGTH)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 6.2, Principles of dynamic programming (memoization or iteration over subproblems)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 6, Sections 6.1 to 6.5
---

Tabulation is the technique of computing the values of a recurrence by filling a table in a fixed order, where each entry is computed after all the entries that it depends on. It is the bottom-up form of dynamic programming: there is no recursion, only loops over the subproblems in a [topological order](/topological-sort/) of the [subproblem graph](/subproblem-graph/), reversed so that dependencies come first. It does the same work as [memoization](/memoization/) up to a constant factor when all subproblems are needed, it uses no call stack, and its fixed order allows [rolling-array space reduction](/rolling-array-space-reduction/).

## In plain words

Some problems are solved from the answers of smaller versions of the same problem. Memoization starts from the big question and asks smaller ones as needed. Tabulation goes the other way. It first answers all the smallest questions and writes them in a table. Then it answers the next size, reading the answers it needs from the table. It goes on, size by size, until it reaches the question you asked.

The only thing you must get right, apart from the rule itself, is the order. When you fill a cell, every cell it reads must already be filled. For many problems the order is plain: by increasing length, by increasing amount, or row by row.

## When it applies

Look for these signals.

- You have a recurrence that is correct, by [optimal substructure](/optimal-substructure/) or by a counting argument, and it has [overlapping subproblems](/overlapping-subproblems/).
- The subproblems can be indexed by a few integers in known ranges, so that an array holds them all.
- You can name an order in which each subproblem comes after all of its subproblems. For integer indices this is often "increasing in each index" or "increasing in the length of a range".
- Most of the subproblems in the table are needed for the answer. If only a few are reachable from the goal, memoization does less work.

## The template

The holes are SUBPROBLEMS, ORDER, BASE, BASE-VALUE, CHOICES, SUB, COMBINE and GOAL. ORDER must list each subproblem after every SUB$(x, c)$ with $c \in$ CHOICES$(x)$.

```pseudo id=main
BOTTOM-UP(input)
L1  T ← a new table indexed by SUBPROBLEMS
L2  for each x in ORDER do                 ▷ every SUB(x, c) comes before x
L3      if BASE(x) then
L4          T[x] ← BASE-VALUE(x)
L5      else
L6          T[x] ← COMBINE over c ∈ CHOICES(x) of (c, T[SUB(x, c)])
L7  return T[GOAL]
```

Line L6 is the recurrence with each recursive call replaced by a read of the table. To get an optimal solution and not only its value, store the best choice of L6 in a second table, then follow the choices from GOAL. That is [traceback](/traceback/).

**Correctness.** Let $f$ be the function that the recurrence defines. The [loop invariant](/loop-invariant/) of line L2 is: for each subproblem $y$ that comes before the current $x$ in ORDER, $T[y] = f(y)$. It holds before the first pass, since no subproblem comes before the first. In a pass on $x$, either L4 sets $T[x] = f(x)$, or L6 reads only entries $T[\mathrm{SUB}(x, c)]$ that come before $x$, which equal $f$ by the invariant, so L6 sets $T[x] = f(x)$ by the recurrence. When the loop ends, every subproblem has been processed, so $T[\mathrm{GOAL}] = f(\mathrm{GOAL})$.

**Cost.** Each subproblem is processed once, so the time is $\sum_{x} O(1 + |\mathrm{CHOICES}(x)|)$ times the cost of one choice, summed over all subproblems in the table. This is the number of vertices plus edges of the subproblem graph. The space is the size of the table. Unlike memoization, the sum is over all subproblems, even those that the goal does not need.

### Walk-through: longest common subsequence

For strings $X = x_1 \cdots x_m$ and $Y = y_1 \cdots y_n$, let $c[i, j]$ be the length of a [longest common subsequence](/longest-common-subsequence/) of $x_1 \cdots x_i$ and $y_1 \cdots y_j$. Then $c[i, 0] = c[0, j] = 0$, and for $i, j \ge 1$,

$$ c[i, j] = \begin{cases} c[i-1, j-1] + 1 & \text{if } x_i = y_j, \\ \max(c[i-1, j],\ c[i, j-1]) & \text{otherwise.} \end{cases} $$

Each entry reads the entry to its left, above it, and above-left. So row by row, left to right in each row, is a valid ORDER. This is LCS-LENGTH of CLRS Section 14.4. For $X = \mathrm{ABCBDAB}$ and $Y = \mathrm{BDCABA}$, the table is:

| | | B | D | C | A | B | A |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A | 0 | 0 | 0 | 0 | 1 | 1 | 1 |
| B | 0 | 1 | 1 | 1 | 1 | 2 | 2 |
| C | 0 | 1 | 1 | 2 | 2 | 2 | 2 |
| B | 0 | 1 | 1 | 2 | 2 | 3 | 3 |
| D | 0 | 1 | 2 | 2 | 2 | 3 | 3 |
| A | 0 | 1 | 2 | 2 | 3 | 3 | 4 |
| B | 0 | 1 | 2 | 2 | 3 | 4 | 4 |

The answer is the last entry, $c[7, 6] = 4$; BCBA is one longest common subsequence. The table has $8 \cdot 7 = 56$ entries, each computed in $O(1)$ time, so the time is $\Theta(mn)$. Column by column is also a valid order, and so is anti-diagonal by anti-diagonal. Bottom to top is not.

## Classic examples

- **[Fibonacci numbers](/fibonacci-numbers/).** Fill $F(0), F(1), \ldots, F(n)$ in increasing order. The time is $\Theta(n)$ additions, and two variables are enough in place of the table.
- **[Rod cutting](/rod-cutting-problem/).** BOTTOM-UP-CUT-ROD of CLRS Section 14.1 fills $r_0, \ldots, r_n$ in increasing order of length, in $\Theta(n^2)$ time. With the CLRS prices, $r_0, \ldots, r_{10}$ is $0, 1, 5, 8, 10, 13, 17, 18, 22, 25, 30$.
- **[0/1 knapsack](/knapsack-dynamic-programming/).** Fill the table of (first $i$ items, capacity $w$) row by row, in $O(nW)$ time. This is a [pseudo-polynomial](/pseudo-polynomial-time/) bound.
- **[Matrix-chain multiplication](/matrix-chain-multiplication/).** MATRIX-CHAIN-ORDER of CLRS Section 14.2 fills $m[i, j]$ in order of increasing chain length $j - i + 1$, because the range $[i, j]$ depends on shorter ranges. Row by row would read entries that are not yet filled. This order is the pattern of [interval DP](/interval-dp/).
- **[Floyd-Warshall](/floyd-warshall/).** The table $d^{(k)}[i, j]$ is filled in order of increasing $k$, the largest allowed intermediate vertex, and the $k$ index is then dropped by an in-place update.
- **[Bellman-Ford](/bellman-ford/).** Read as tabulation, it fills "the shortest walk from $s$ to $v$ with at most $k$ edges" for $k = 0, 1, \ldots, n - 1$.

## Variations

- **Pull and push.** The template is the pull form: each entry reads the entries it depends on. In the push form, after $T[x]$ is final, the loop adds its contribution to each entry that depends on $x$. Both visit each edge of the subproblem graph once. The push form is natural when the successors are easier to list than the predecessors, as in many [DP on DAGs](/dp-on-dag/).
- **Rolling arrays.** When row $i$ reads only rows $i - 1, \ldots, i - k$, keep only $k + 1$ rows. See [rolling-array space reduction](/rolling-array-space-reduction/). In the 0/1 knapsack, one row suffices if each row is filled from high capacity to low.
- **Orders by length or by diagonal.** [Interval DP](/interval-dp/) fills by increasing length of the range. A table where each cell reads its left, top and top-left neighbors can be filled by anti-diagonals. The cells of one anti-diagonal do not depend on each other, so they can be filled in parallel.
- **Sparse tables.** When only some states can occur, keep a dictionary of the reachable states of the current layer, and build the next layer from it. This is tabulation over a layered set of states, and it is close to memoization in the work it does.
- **Speed-ups of the COMBINE step.** When the minimum in L6 has structure, the same table can be filled faster: [Knuth's optimization](/knuth-optimization/), the [divide-and-conquer optimization](/divide-and-conquer-optimization/) and the [convex hull trick](/convex-hull-trick/) are examples.

## Pitfalls

- **The wrong order.** Filling an interval DP row by row, or a 2D table from the wrong corner, reads entries that still hold their initial value. The program runs and returns a wrong number. Before you write the loops, list the entries that L6 reads and check that each comes earlier.
- **The wrong initial value.** For a minimum, unset entries and unreachable states must be $+\infty$, not 0. With 0, the minimum picks up states that do not exist. For a maximum, use $-\infty$. For a count, unreachable states are 0 and the base case is 1.
- **The direction of a one-row loop.** With one row for a knapsack, filling capacities from low to high lets an item be used again in the same row. That is right for the [unbounded knapsack](/unbounded-knapsack/) and wrong for the 0/1 knapsack.
- **Off-by-one sizes.** A table for prefixes of lengths $0, \ldots, m$ has $m + 1$ rows. The base row for the empty prefix is part of the table.
- **Work on states that are never used.** Tabulation computes every entry. When the reachable states are a small part of the table, for example when the capacity is huge but the weights are all multiples of a large number, memoization or a sparse layer is faster.
- **Overflow in counting tables.** A table of counts, such as the number of paths, grows quickly. Use big integers, or count modulo a number if the task asks for it.
- **A rolled table cannot be traced back.** After [rolling-array space reduction](/rolling-array-space-reduction/), the choices of early rows are gone. Keep the full table, or keep the choices, or use [Hirschberg's method](/hirschberg-algorithm/).

## Exercises

1. Write the recurrence for the number of ways to climb $n$ stairs with steps of 1, 2 or 3, and fill the table for $n = 10$. Then rewrite it with three variables.
2. In the LCS table of the walk-through, give an order of the cells that is not row by row, not column by column and not by anti-diagonals, and that is still valid. Prove that it is valid.
3. For [matrix-chain multiplication](/matrix-chain-multiplication/), show that filling $m[i, j]$ for $i$ from $n$ down to 1, and for each $i$, $j$ from $i$ up to $n$, is a valid order. Compare it with the order by chain length.
4. Convert the memoized solution of a problem of your choice into a bottom-up one. Give a problem where the bottom-up version computes at least 10 times as many entries as the memoized version needs.
   <details><summary>Hint</summary>Try the minimum number of coins for an amount $A$ with coin values that are all multiples of 100, and $A$ a multiple of 100.</details>
5. Explain why tabulation in a fixed order cannot compute shortest paths in a graph with cycles by the recurrence $d(v) = \min_{(u, v)} (d(u) + w(u, v))$, and how [Bellman-Ford](/bellman-ford/) changes the subproblems to get an acyclic order.

## References
