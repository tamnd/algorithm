---
tag: 48Q02J
kind: technique
slug: interval-dp
name: Interval dynamic programming
aliases:
- range DP
- DP over intervals
area: techniques/dynamic-programming
level: core
summary: DP over contiguous intervals, combining the solutions of two sub-intervals split at an inner point.
prereqs: [optimal-substructure, overlapping-subproblems, tabulation]
see_also: [matrix-chain-multiplication, optimal-binary-search-tree, optimal-polygon-triangulation, longest-palindromic-subsequence, knuth-optimization, memoization, traceback]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.2 (matrix-chain multiplication), Section 14.3 (elements of dynamic programming) and Section 14.5 (optimal binary search trees)
  - paper: doi:10.1007/BF00264289
    title: Donald E. Knuth, Optimum binary search trees, Acta Informatica 1(1), 14-25, 1971
    locator: the interval recurrence for optimum binary search trees
  - paper: doi:10.1137/0211028
    title: T. C. Hu and M. T. Shing, Computation of matrix chain products, part I, SIAM Journal on Computing 11(2), 362-373, 1982
    locator: the link between matrix-chain orders and polygon partitions
---

Interval dynamic programming solves a problem on a sequence $x_1, \ldots, x_n$ by computing the answer for every contiguous interval $x_i, \ldots, x_j$, from the shortest intervals to the longest. The answer for an interval is built from the answers for shorter intervals inside it, most often from two sub-intervals $[i, k]$ and $[k+1, j]$ at a split point $k$. There are $\Theta(n^2)$ intervals, and with a split point the typical cost is $\Theta(n^3)$ time and $\Theta(n^2)$ space. [Matrix-chain multiplication](/matrix-chain-multiplication/), [optimal binary search trees](/optimal-binary-search-tree/) and [polygon triangulation](/optimal-polygon-triangulation/) are the standard examples.

## In plain words

Some problems ask how to group or split a row of things, where the order of the row must not change. For example: in which order to multiply a chain of matrices, or how to build a search tree on sorted keys.

The idea is to solve the problem for every stretch of neighbors in the row. A stretch of one or two items is easy. For a longer stretch, try every place where its last step can split it into a left part and a right part. Both parts are shorter stretches, so their best answers are already known. Add the cost of the last step and keep the best split. When the full row is done, the table also tells you where to split, so you can rebuild the best grouping.

## When it applies

- The input is a sequence, and the order of the elements must be kept. A solution of the whole is a tree of nested intervals: one step at the top joins or splits two (or a few) adjacent pieces.
- An optimal solution for an interval contains optimal solutions for the sub-intervals it uses. This is [optimal substructure](/optimal-substructure/), usually shown by a [cut-and-paste argument](/cut-and-paste-argument/).
- The cost of the top step depends only on the interval and the split, and not on how the parts were solved inside. For matrix chains it is $p_{i-1} p_k p_j$, which depends on the dimensions only.
- The same sub-interval occurs in many different splits, so the problems [overlap](/overlapping-subproblems/), and a plain recursion takes exponential time.

Typical words in a problem: parenthesize, merge adjacent, split a string, triangulate a polygon, remove from the ends, palindrome.

## The template

Let $c(i, j)$ be the best value for the interval $[i, j]$. The holes are the base value, the cost of the top step, and the set of splits.

```pseudo id=main
INTERVAL-DP(n)
L1  for i ← 1 to n do c[i, i] ← base(i)                         ▷ hole: the base case
L2  for len ← 2 to n do                                         ▷ shorter intervals first
L3      for i ← 1 to n − len + 1 do
L4          j ← i + len − 1
L5          c[i, j] ← +∞
L6          for k ← i to j − 1 do                               ▷ hole: the set of splits
L7              q ← c[i, k] + c[k+1, j] + cost(i, k, j)         ▷ hole: the cost of the top step
L8              if q < c[i, j] then c[i, j] ← q, s[i, j] ← k
L9  return c[1, n], s
```

**Why the order of line L2 is right.** The value $c[i, j]$ reads $c[i, k]$ and $c[k+1, j]$, both of which have length less than $len$. All intervals of a smaller length are complete when the loop of line L2 reaches $len$. Any order that finishes an interval after all intervals inside it also works: for example $i$ from $n$ down to 1 and $j$ from $i$ up to $n$. A [memoized](/memoization/) recursion finds such an order by itself.

**Why line L8 gives the optimum.** By optimal substructure, an optimal solution of $[i, j]$ splits at some $k$ and uses optimal solutions of $[i, k]$ and $[k+1, j]$, so its value is one of the $q$ of line L7. Each $q$ is the value of some valid solution, so none is below the optimum. So the minimum of the $q$ is the optimum. The table $s$ records the split, and a [traceback](/traceback/) from $s[1, n]$ rebuilds the solution in $O(n)$ time.

**Cost.** Lines L6 to L8 run $\sum_{len=2}^{n} (n - len + 1)(len - 1) = (n^3 - n)/6$ times, so the time is $\Theta(n^3)$ when the cost of line L7 takes $O(1)$ time. The tables use $\Theta(n^2)$ space.

## Classic examples

### Matrix-chain multiplication

Multiply $A_1 A_2 \cdots A_n$, where $A_i$ has $p_{i-1}$ rows and $p_i$ columns, with the fewest scalar multiplications. The last product joins $A_i \cdots A_k$ and $A_{k+1} \cdots A_j$, at a cost of $p_{i-1} p_k p_j$. So $c(i, i) = 0$ and the cost of line L7 is $p_{i-1} p_k p_j$. This is CLRS Section 14.2.

For $p = (5, 4, 6, 2, 7)$ the tables are:

| $c[i, j]$ | $j = 1$ | $j = 2$ | $j = 3$ | $j = 4$ |
|---|---|---|---|---|
| $i = 1$ | 0 | 120 | 88 | 158 |
| $i = 2$ | | 0 | 48 | 104 |
| $i = 3$ | | | 0 | 84 |
| $i = 4$ | | | | 0 |

| $s[i, j]$ | $j = 2$ | $j = 3$ | $j = 4$ |
|---|---|---|---|
| $i = 1$ | 1 | 1 | 3 |
| $i = 2$ | | 2 | 3 |
| $i = 3$ | | | 3 |

For example, $c[1, 3] = \min(0 + 48 + 5 \cdot 4 \cdot 2, \; 120 + 0 + 5 \cdot 6 \cdot 2) = \min(88, 180) = 88$. The traceback gives $s[1, 4] = 3$, then $s[1, 3] = 1$, so the best order is $((A_1 (A_2 A_3)) A_4)$, with $48 + 40 + 70 = 158$ multiplications. The order $((A_1 A_2) A_3) A_4$ costs $120 + 60 + 70 = 250$.

### Other members of the family

- **[Optimal binary search trees](/optimal-binary-search-tree/).** The root $k$ of the keys $i, \ldots, j$ splits them into $[i, k-1]$ and $[k+1, j]$, and the cost of the top step is the total probability of the interval. CLRS Section 14.5. The split is a key, not a gap, so the two parts do not touch.
- **[Optimal polygon triangulation](/optimal-polygon-triangulation/).** The triangle on the side $v_{i-1} v_j$ has a third vertex $v_k$ with $i \le k < j$, which splits the polygon into two smaller polygons. Hu and Shing showed that matrix-chain orders correspond to triangulations of a polygon with $n + 1$ vertices.
- **[Longest palindromic subsequence](/longest-palindromic-subsequence/).** Here $c(i, j)$ uses only $c(i+1, j-1)$, $c(i+1, j)$ and $c(i, j-1)$, with no split loop, so the time is $\Theta(n^2)$.
- **Merging adjacent piles.** The cost of the top step is the total weight of the interval. With [Knuth's optimization](/knuth-optimization/) the time drops to $O(n^2)$.
- **Games on the ends of a row.** Two players take an element from either end of a row. The best score difference of the player to move on $[i, j]$ depends on $[i+1, j]$ and $[i, j-1]$.

## Variations

- **Splits that keep the split element.** In OBST and in polygon triangulation, the parts are $[i, k-1]$ and $[k+1, j]$ (or share the vertex $k$). Only the index bounds of line L6 and the base cases change.
- **Removal problems.** Some problems, such as removing all elements of a row where removing one joins its neighbors, define $c(i, j)$ by the element removed last. The element $k$ removed last splits $[i, j]$ into $[i, k-1]$ and $[k+1, j]$, which do not interact.
- **Extra state.** When the cost depends on what lies next to the interval, add the state to the table: $c(i, j, x)$. The time grows by the size of the new dimension.
- **Circular sequences.** For a cycle, double the sequence to $x_1, \ldots, x_n, x_1, \ldots, x_n$, run the method on length $2n$, and take the best interval of length $n$.
- **Faster methods.** When the cost of the top step depends only on $(i, j)$ and satisfies the quadrangle inequality of the [Monge property](/monge-property/), [Knuth's optimization](/knuth-optimization/) gives $O(n^2)$. Matrix chains have a special $O(n \log n)$ algorithm by Hu and Shing.

## Pitfalls

- **Wrong order of the loops.** A loop with $i$ from 1 to $n$ outside and $j$ from $i$ to $n$ inside reads $c[k+1, j]$ before it is computed. Loop by length, or loop $i$ downward.
- **Greedy splits.** Choosing the split with the cheapest top step does not give the optimum. For $p = (1, 1, 2, 3)$, the cheapest top step is $k = 1$ with $1 \cdot 1 \cdot 3 = 3$, which gives $A_1 (A_2 A_3)$ at a total of $6 + 3 = 9$. The split $k = 2$ has a top step of 6 but gives $(A_1 A_2) A_3$ at a total of $2 + 6 = 8$. Only the full minimum of line L8 is safe.
- **A cost that depends on the inside of the parts.** If the cost of the top step depends on how a part was solved, the interval is not a complete state. Add the missing information to the state.
- **Memory.** The table has $n^2$ entries, which for $n = 10^5$ is too much. Interval DP is usually for $n$ up to a few thousand, or a few hundred for $\Theta(n^3)$ time.

## Exercises

1. Show that the number of executions of line L7 is $(n^3 - n)/6$.
2. Give the recurrence for the longest palindromic subsequence of a string, and fill the table for "character".
   <details><summary>Hint</summary>If $x_i = x_j$, use $2 + c(i+1, j-1)$; otherwise use $\max(c(i+1, j), c(i, j-1))$. The answer for "character" is 5, for example "carac".</details>
3. Write the interval recurrence for a game in which two players take turns removing a coin from either end of a row, each wants the largest total, and both play optimally.
4. Find an input with four matrices on which the greedy rule of the pitfalls fails, and check it with the table.

## References
