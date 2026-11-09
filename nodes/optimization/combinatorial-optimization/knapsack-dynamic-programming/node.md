---
tag: 2ST7VJ
kind: algorithm
slug: knapsack-dynamic-programming
name: Dynamic programming for knapsack
aliases:
- pseudo-polynomial knapsack DP
- Bellman recursion for knapsack
- 0-1 knapsack DP
area: optimization/combinatorial-optimization
level: core
summary: Fill a table over items and capacities in O(nW) time.
solves: [knapsack-problem]
model: word-ram
complexity:
  vars: {n: the number of items, W: the capacity}
  time: {worst: Θ(n W), average: Θ(n W), best: Θ(n W)}
  space: {extra: Θ(n W)}
properties: {deterministic: true, recursive: false, exact: true}
prereqs: [knapsack-problem, optimal-substructure, tabulation]
see_also: [knapsack-problem, greedy-fractional-knapsack, knapsack-fptas, profit-indexed-dynamic-programming, knapsack-branch-and-bound, unbounded-knapsack, subset-sum-problem, pseudo-polynomial-time]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Section 6.4, Subset Sums and Knapsacks, Adding a Variable
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms, McGraw-Hill, 2008
    locator: Section 6.4, Knapsack
  - book: isbn:9783540402862
    title: Hans Kellerer, Ulrich Pferschy and David Pisinger, Knapsack Problems, Springer, 2004
    locator: the chapter on basic algorithmic concepts (the dynamic programming recursion by capacities and by profits, and the storage reduction)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 15.2, Elements of the greedy strategy (the 0-1 knapsack problem), and Chapter 14, Dynamic Programming
  - paper: doi:10.1287/opre.5.2.266
    title: George B. Dantzig, Discrete-variable extremum problems, Operations Research 5(2), 266 to 288, 1957
    locator: the knapsack problem and its linear relaxation
  - paper: doi:10.1145/321906.321909
    title: Oscar H. Ibarra and Chul E. Kim, Fast approximation algorithms for the knapsack and sum of subset problems, Journal of the ACM 22(4), 463 to 468, 1975
    locator: the approximation scheme built on a dynamic program over scaled values
---

Dynamic programming solves the 0-1 [knapsack problem](/knapsack-problem/) exactly by filling a table $V[i][c]$, the best value that items $1$ to $i$ can reach with capacity $c$. Each entry is the better of two choices for item $i$, leave it or take it, so the table has $(n+1)(W+1)$ entries and takes $\Theta(nW)$ time. This is [pseudo-polynomial](/pseudo-polynomial-time/): polynomial in the value of $W$, but exponential in its number of digits, which matches the [weak NP-hardness](/weak-np-hardness/) of the problem.

## In plain words

Think about the last item. The best packing either leaves it out, or puts it in. If it is left out, the answer is the best packing of the other items in the same bag. If it is put in, the answer is its value plus the best packing of the other items in a bag that is smaller by its weight.

So the best answer for all items and the full bag depends only on best answers for fewer items and smaller bags. Write these smaller answers in a table, one row for each number of items and one column for each bag size, and fill it row by row. At the end, walk back through the table to see which items were taken.

## The problem

The input is $n$ items with weights $w_1, \ldots, w_n \in \mathbb{Z}_{\ge 0}$ and values $v_1, \ldots, v_n \in \mathbb{Z}_{\ge 0}$, and a capacity $W \in \mathbb{Z}_{\ge 0}$. The output is the largest $\sum_{i \in S} v_i$ over all $S \subseteq \{1, \ldots, n\}$ with $\sum_{i \in S} w_i \le W$, and one set $S$ that reaches it. This is the [knapsack problem](/knapsack-problem/). The weights and the capacity must be integers, because they index the table.

## The algorithm

Let $V[i][c]$ be the largest value of a set $S \subseteq \{1, \ldots, i\}$ with $w(S) \le c$. Then $V[0][c] = 0$, and for $i \ge 1$

$$ V[i][c] = \begin{cases} V[i-1][c] & \text{if } w_i > c, \\ \max\bigl(V[i-1][c],\ V[i-1][c - w_i] + v_i\bigr) & \text{if } w_i \le c. \end{cases} $$

```pseudo id=main
KNAPSACK-DP(w[1 .. n], v[1 .. n], W)
L1  for c ← 0 to W do V[0][c] ← 0
L2  for i ← 1 to n do
L3      for c ← 0 to W do
L4          V[i][c] ← V[i − 1][c]                       ▷ leave item i
L5          if w[i] ≤ c and V[i − 1][c − w[i]] + v[i] > V[i][c] then
L6              V[i][c] ← V[i − 1][c − w[i]] + v[i]     ▷ take item i
L7  S ← ∅, c ← W
L8  for i ← n downto 1 do
L9      if V[i][c] ≠ V[i − 1][c] then                    ▷ item i was taken
L10         S ← S ∪ {i}, c ← c − w[i]
L11 return V[n][W], S
```

Lines L1 to L6 fill the table row by row. Row $i$ reads only row $i - 1$. Lines L7 to L11 trace the choices back from the corner $(n, W)$. If $V[i][c] = V[i-1][c]$, some best set for $(i, c)$ leaves item $i$ out, so the traceback leaves it out. Otherwise every best set for $(i, c)$ takes item $i$, and the rest of the set is a best set for $(i - 1, c - w_i)$.

## Example

Take $W = 10$ and the items $w = (5, 4, 6, 3)$, $v = (10, 40, 30, 50)$. The table, with one row for each $i$ and one column for each capacity $c$:

| $i$ \ $c$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 ($w = 5$, $v = 10$) | 0 | 0 | 0 | 0 | 0 | 10 | 10 | 10 | 10 | 10 | 10 |
| 2 ($w = 4$, $v = 40$) | 0 | 0 | 0 | 0 | 40 | 40 | 40 | 40 | 40 | 50 | 50 |
| 3 ($w = 6$, $v = 30$) | 0 | 0 | 0 | 0 | 40 | 40 | 40 | 40 | 40 | 50 | 70 |
| 4 ($w = 3$, $v = 50$) | 0 | 0 | 0 | 50 | 50 | 50 | 50 | 90 | 90 | 90 | 90 |

Two entries in detail. $V[3][10] = \max(V[2][10], V[2][4] + 30) = \max(50, 70) = 70$: items 2 and 3. $V[4][7] = \max(V[3][7], V[3][4] + 50) = \max(40, 90) = 90$.

The traceback starts at $(4, 10)$:

| $i$ | $c$ | $V[i][c]$ | $V[i-1][c]$ | decision | new $c$ |
| --- | --- | --- | --- | --- | --- |
| 4 | 10 | 90 | 70 | take item 4 | 7 |
| 3 | 7 | 40 | 40 | leave item 3 | 7 |
| 2 | 7 | 40 | 10 | take item 2 | 3 |
| 1 | 3 | 0 | 0 | leave item 1 | 3 |

The answer is $S = \{2, 4\}$ with weight 7 and value 90, which is the optimum of all 16 subsets.

## Correctness

The table entries satisfy the recurrence by [optimal substructure](/optimal-substructure/): a best set for $(i, c)$ either does not contain item $i$, and is then a feasible set for $(i - 1, c)$, or contains it, and then removing item $i$ leaves a feasible set for $(i - 1, c - w_i)$. Conversely, each of the two options in the maximum is the value of a feasible set for $(i, c)$. By induction on $i$, lines L1 to L6 compute $V[i][c]$ for every $i$ and $c$. The traceback keeps the invariant that the set chosen so far, together with any best set for $(i, c)$, is a best set for $(n, W)$. The full proof is in the proof file below.

## Complexity

- **Time.** Lines L4 to L6 cost $O(1)$ in the [word RAM](/word-ram/), and they run $n(W+1)$ times. Line L1 costs $\Theta(W)$ and the traceback $\Theta(n)$. The total is $\Theta(nW + n + W)$, which is $\Theta(nW)$ when $n, W \ge 1$. It is the same on every input of the same $n$ and $W$, so the best, average and worst cases agree.
- **Space.** The full table has $(n+1)(W+1)$ entries, so $\Theta(nW)$. The traceback needs the full table.
- **Value only.** Row $i$ needs only row $i - 1$. With one row and the inner loop over $c$ from $W$ down to $w_i$, the entry $V[c - w_i]$ still holds the old row when it is read. This takes $\Theta(W)$ space.
- **Pseudo-polynomial.** The input has length $\Theta(n \log W)$ when all numbers have about $\log W$ bits, and $nW$ is exponential in $\log W$. For $W = 2^{60}$ the table is not practical. This is not a weakness of this algorithm only: the problem is NP-hard, and a running time polynomial in $n$ and $\log W$ would give P = NP.

## Properties

- **Exact.** It returns an optimal value and an optimal set, not an approximation.
- **Oblivious work.** The number of steps depends only on $n$ and $W$, not on the values.
- **All capacities at once.** Row $n$ gives the optimal value for every capacity $c \le W$, so one run answers all smaller capacities.
- **Integer weights.** The weights index the table. Values may be any numbers that can be added and compared.

## Variants and improvements

- **DP over values.** Let $M[i][p]$ be the least weight of a set of items from $1..i$ with value exactly $p$. Then $f^* = \max \{ p : M[n][p] \le W \}$, in $O(nV)$ time with $V = \sum_i v_i$. With scaled values this is the [profit-indexed dynamic program](/profit-indexed-dynamic-programming/) of the [knapsack FPTAS](/knapsack-fptas/). On the example, the largest $p$ with $M[4][p] \le 10$ is 90.
- **Sparse lists.** Keep, for each $i$, only the Pareto-optimal pairs (weight, value): no other pair has less weight and more value. The lists are often much shorter than $W$, and merging two lists is linear. The meet-in-the-middle algorithm of Horowitz and Sahni builds such lists for two halves of the items.
- **Unbounded knapsack.** With unlimited copies of each item, the one-row loop runs over $c$ from low to high: then $V[c - w_i]$ may already include item $i$. See [unbounded knapsack](/unbounded-knapsack/).
- **Solution in small space.** Split the items into two halves, and run the one-row DP forward on the first half and backward on the second. The best split $c_1 + c_2 = W$ gives the capacity for each half, and recursion on the halves finds the set. This gives the set in $O(nW)$ time and $O(n + W)$ space, in the same way as Hirschberg's method for [the longest common subsequence](/lcs-dynamic-programming/).
- **Bounded and multiple-choice knapsack.** The same recursion with more choices per row. See [bounded knapsack](/bounded-knapsack/).

## When to use it

Use the capacity DP when $W$ is small, up to about $10^7$ in practice, or when you need the answer for all capacities at once. Use the value DP when the values are small and the weights are large. When both are large, use [branch and bound](/knapsack-branch-and-bound/) with the fractional bound, or the [FPTAS](/knapsack-fptas/) when a $(1 - \varepsilon)$ guarantee is enough. The [ratio greedy](/greedy-fractional-knapsack/) is exact only for the fractional problem.

## Pitfalls

- **Low to high in the one-row form.** If line L3 runs $c$ from 0 up to $W$ in the one-row version, $V[c - w_i]$ may already contain item $i$, and the item is used twice. That solves the unbounded problem, not the 0-1 problem. In the one-row form, run $c$ from $W$ down to $w_i$.
- **A missing bound check.** Line L5 tests $w_i \le c$ before it reads $V[i-1][c - w_i]$. Without the test, a negative index reads a wrong entry (in Python, an entry from the end of the row).
- **Traceback with one row.** The one-row version keeps no history, so lines L7 to L10 cannot run on it. Keep the full table, or keep one bit per entry that says whether item $i$ was taken.
- **Calling it polynomial.** $\Theta(nW)$ is not polynomial in the input length. Scaling the weights down to make $W$ small changes the problem unless the weights share a common factor.
- **Real weights.** The table needs integer weights. Rounding real weights down can make an infeasible set look feasible.

## Implementations

## History

Dantzig (1957) studied the knapsack problem and solved its linear relaxation by the ratio order. The recursion over items and capacities is the standard example of Bellman's dynamic programming, and Kellerer, Pferschy and Pisinger call it the Bellman recursion. The value-indexed recursion is the base of the approximation scheme of Ibarra and Kim (1975).

## References
