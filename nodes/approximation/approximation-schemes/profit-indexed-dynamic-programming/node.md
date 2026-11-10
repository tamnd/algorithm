---
tag: Z5HN7N
kind: technique
slug: profit-indexed-dynamic-programming
name: Profit-indexed dynamic programming
aliases:
- DP by profit
- value-indexed dynamic programming
- dynamic programming by profits
- min-weight-for-each-profit table
area: approximation/approximation-schemes
level: core
summary: A dynamic program indexed by the objective value that stores the least weight reaching each value. Its size depends on the profits, not the capacity, so it is the base of the knapsack FPTAS.
prereqs: [knapsack-dynamic-programming, optimal-substructure, tabulation]
see_also: [knapsack-fptas, rounding-and-scaling, trimming-technique, constrained-shortest-path, bounded-knapsack, unbounded-knapsack, approximate-pareto-set, pseudo-polynomial-time]
sources:
  - book: isbn:9783540402862
    title: Hans Kellerer, Ulrich Pferschy and David Pisinger, Knapsack Problems, Springer, 2004
    locator: the chapter on basic algorithmic concepts (dynamic programming by profits) and the chapter on approximation algorithms for the knapsack problem
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms, Springer, 2001
    locator: Chapter 8, Section 8.2 (the pseudo-polynomial algorithm by profit and the FPTAS built on it)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 3, Section 3.1 (the dynamic program over profits for knapsack)
  - paper: doi:10.1145/321906.321909
    title: Oscar H. Ibarra and Chul E. Kim, Fast approximation algorithms for the knapsack and sum of subset problems, Journal of the ACM 22(4), 1975
    locator: pages 463 to 468
  - paper: doi:10.1287/moor.17.1.36
    title: Refael Hassin, Approximation schemes for the restricted shortest path problem, Mathematics of Operations Research 17(1), 1992
    locator: pages 36 to 42
---

Profit-indexed dynamic programming is a [dynamic program](/tabulation/) whose table has one column for each value of the objective, and stores in each column the least amount of a resource that reaches that value exactly. For the [0/1 knapsack problem](/knapsack-problem/), $A[j][q]$ is the least weight of a subset of the first $j$ items with profit exactly $q$, and the answer is the largest $q$ with $A[n][q] \le W$. The table has $n \sum_j p_j$ entries, which does not depend on the capacity. When the profits are first scaled down, this table becomes polynomial in size, and it is the exact core of the [knapsack FPTAS](/knapsack-fptas/).

## In plain words

The usual table for the knapsack problem asks: for each possible load, what is the best profit? Its size grows with the capacity of the knapsack. This page turns the question around. For each possible profit, what is the least weight that earns exactly that profit?

The new table has one column for each total profit. Its size grows with the sum of the profits, not with the capacity. To read the answer, find the largest profit whose least weight still fits. When the profits are small numbers and the capacity is huge, this table is much smaller. The approximation schemes for knapsack make the profits small on purpose, and then use this table.

## When it applies

Look for these signals in a problem:

- The solution is built by a sequence of choices, one for each item or stage, and the objective is a sum of integer values of the choices.
- There is one resource (weight, cost, time, length) whose sum must stay within a budget, and a smaller use of the resource is always better.
- The objective values are small integers, or they can be made small by [rounding and scaling](/rounding-and-scaling/), while the resource values and the budget are large.
- The exact table indexed by the resource would have too many columns, because the budget is a large number.

The method needs a monotone resource: a partial solution that reaches value $q$ with less resource is at least as good as one that reaches $q$ with more. With two or more resources there is no single least value to store, and the table must hold sets of non-dominated vectors instead.

## The template

The template is for a maximization problem with values $v_j \ge 0$ (integers), resource uses $c_j \ge 0$ and a budget $B$. The holes are the bound $V$, the way a choice adds to the resource (the operation $\oplus$, usually $+$), and the test against the budget.

```pseudo id=main
PROFIT-INDEXED-DP(v[1 .. n], c[1 .. n], B)
L1  V ← an upper bound on the value of each feasible solution    ▷ hole: Σ v_j, or 2·(a lower bound on OPT)
L2  A[0] ← 0; A[q] ← ∞ for 1 ≤ q ≤ V
L3  for j ← 1 to n do
L4      for q ← V down to v_j do                                ▷ down: each item is used at most once
L5          A[q] ← min(A[q], A[q − v_j] ⊕ c_j)                   ▷ hole: how the choice adds to the resource
L6  return max { q : A[q] ≤ B }                                  ▷ hole: the budget test
```

After the iteration $j$ of line L3, the entry $A[q]$ is the least resource of a subset of the first $j$ items with value exactly $q$, or $\infty$ if no subset has value $q$. The proof is by induction on $j$: a subset of the first $j$ items with value $q$ either avoids item $j$, and is counted in the old $A[q]$, or holds item $j$, and is a subset of the first $j - 1$ items with value $q - v_j$ plus item $j$. Line L4 runs $q$ downwards, so the entry $A[q - v_j]$ that line L5 reads is still the value from the iteration $j - 1$. Line L6 is then the largest value that fits in the budget.

The time is $O(nV)$ and the space is $O(V)$ for the value. To recover the solution, keep one bit for each pair $(j, q)$ that records whether line L5 took item $j$, which is $O(nV)$ bits, and walk back from the answer. With $V = \sum_j v_j \le n \cdot v_{\max}$, the time is $O(n^2 v_{\max})$. This is [pseudo-polynomial](/pseudo-polynomial-time/) in the values, and it does not depend on the budget at all.

### A worked table

Take the knapsack items with profits $3, 4, 5, 6$ and weights $2, 3, 4, 5$, so $V = 18$. The finite entries $(q, A[q])$ after each item are:

| after item | finite entries $(q, A[q])$ |
|---|---|
| 1 | (0, 0), (3, 2) |
| 2 | (0, 0), (3, 2), (4, 3), (7, 5) |
| 3 | (0, 0), (3, 2), (4, 3), (5, 4), (7, 5), (8, 6), (9, 7), (12, 9) |
| 4 | (0, 0), (3, 2), (4, 3), (5, 4), (6, 5), (7, 5), (8, 6), (9, 7), (10, 8), (11, 9), (12, 9), (13, 10), (14, 11), (15, 12), (18, 14) |

For $W = 5$ the answer is $q = 7$ (items 1 and 2). The same last row answers every capacity: $W = 9$ gives 12 and $W = 10$ gives 13. Only the entries with $A[q] < A[q']$ for all $q' > q$ matter. Here $(6, 5)$ and $(11, 9)$ drop out, because $(7, 5)$ and $(12, 9)$ give more profit for the same weight. The other 13 entries are the Pareto front of profit against weight.

## Classic examples

- **Exact knapsack by value.** The [knapsack dynamic program](/knapsack-dynamic-programming/) has a form indexed by value, in $O(n \sum_j p_j)$ time. It is better than the capacity form when $\sum_j p_j < W$.
- **The knapsack FPTAS.** The [Ibarra and Kim scheme](/knapsack-fptas/) rounds the profits down to multiples of $K = \varepsilon P / n$, so that $V \le n \lfloor n / \varepsilon \rfloor$, and then runs this template. The time is $O(n^3 / \varepsilon)$.
- **Bounded and unbounded knapsack.** For the [unbounded knapsack](/unbounded-knapsack/), run line L4 upwards, so that item $j$ can be used again. The [bounded knapsack](/bounded-knapsack/) splits each item into copies of sizes $1, 2, 4, \ldots$ and uses the 0/1 template.
- **Restricted shortest path.** In the [constrained shortest path](/constrained-shortest-path/) problem, each edge has a cost and a delay, and the task is a cheapest path with delay at most $D$. The table $A[v][q]$ is the least delay of a path to $v$ with cost exactly $q$. Hassin (1992) scales the costs and gets an FPTAS from it.
- **Approximate Pareto sets.** The last row of the table, cut to its non-dominated entries, is the exact Pareto front of profit against weight. With scaled profits it is an [approximate Pareto set](/approximate-pareto-set/), as in [multi-objective knapsack](/multi-objective-knapsack/).

## Variations

- **Covering form.** For the minimum knapsack problem (least weight with profit at least $D$), index the columns by $\min(q, D)$, so that all profits of $D$ or more share one column. The answer is $A[D]$, and the table has $D + 1$ columns.
- **Bound from a lower bound.** If an algorithm gives $L \le \mathrm{OPT} \le 2L$, set $V = 2L$ in line L1. For knapsack, the greedy 1/2-approximation gives such an $L$, and this saves a factor of $n$ in the FPTAS.
- **Lists instead of arrays.** Store only the non-dominated pairs (value, resource) in a sorted list. The list can be much shorter than $V + 1$, and the [trimming technique](/trimming-technique/) shortens it more, at a controlled loss.
- **More constraints.** A cardinality bound $|S| \le k$ adds an index: $A[j][t][q]$ for $t \le k$ items. Each extra index multiplies the table size by its range.

## Pitfalls

- **Line L4 in the wrong direction.** With $q$ running upwards, line L5 can read an entry that already holds item $j$, so an item is used twice. That is the unbounded knapsack, not the 0/1 knapsack.
- **Returning A[V] or the last finite column.** The answer is the largest $q$ with $A[q] \le B$, not the largest $q$ with $A[q] < \infty$. The largest finite column usually needs more than the budget.
- **Large values without scaling.** The table has $V + 1$ columns. With profits of 30 decimal digits, $V$ is astronomically large, and the method is useless until the profits are scaled.
- **The sentinel.** If $\infty$ is a large integer, then $\infty + c_j$ can overflow in a fixed-width integer type. Test for $\infty$ before the addition, or use a sentinel larger than the sum of all resource values.
- **Scaling the resource.** The template is exact in the resource. If the resource is rounded instead of the value, a solution that breaks the budget can look feasible.

## Exercises

1. Write the covering form: the least weight of a set of items with profit at least $D$. Show that it runs in $O(nD)$ time. *Hint:* in line L5 read the column $\max(0, q - v_j)$ and let $q$ run from $D$ down to $0$, with column $D$ standing for "at least $D$".
2. Show that the last row of the table determines $\mathrm{OPT}(W)$ for every capacity $W$ at once, and give a method with $O(V)$ preprocessing that answers each capacity query in $O(\log V)$ time. *Hint:* the minimum of $A[q..V]$ is non-decreasing in $q$; precompute suffix minima and use binary search.
3. Give an instance with $n$ items where the profit-indexed table has $\Theta(n \cdot 2^n)$ entries but the capacity-indexed table has only $O(n^2)$ entries. *Hint:* profits $2^j$ and weights 1, with $W = n$.
4. Adapt the template to the restricted shortest path problem on a directed acyclic graph, with the table indexed by vertex and cost, and bound its time by $O(m C)$, where $m$ is the number of edges and $C$ is a bound on the cost of a path.

## References
