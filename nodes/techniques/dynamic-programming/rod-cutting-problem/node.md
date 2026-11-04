---
tag: C4MGZ0
kind: problem
slug: rod-cutting-problem
name: Rod cutting
aliases:
- cut rod
area: techniques/dynamic-programming
level: intro
summary: Cut a rod of length n into pieces to maximise the total price of the pieces.
prereqs: [optimal-substructure, overlapping-subproblems, recursion]
see_also: [unbounded-knapsack, coin-change-problem, memoization, tabulation, traceback, subproblem-graph, knapsack-problem, min-plus-convolution]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.1 (rod cutting), including the price table, CUT-ROD, MEMOIZED-CUT-ROD, BOTTOM-UP-CUT-ROD and EXTENDED-BOTTOM-UP-CUT-ROD, and Exercises 14.1-2 and 14.1-3
  - book: isbn:9780073523408
    title: Dasgupta, Papadimitriou and Vazirani, Algorithms
    locator: Section 6.4 (knapsack with repetition, the same recurrence)
  - paper: doi:10.1145/3293465
    title: Marek Cygan, Marcin Mucha, Karol Węgrzycki and Michał Włodarczyk, On problems equivalent to (min,+)-convolution, ACM Transactions on Algorithms 15(1), 2019
    locator: Article 14 (Unbounded Knapsack is subquadratically equivalent to (min,+)-convolution)
---

Rod cutting asks how to cut a rod of integer length $n$ into pieces of integer lengths so that the sum of the prices of the pieces is as large as possible, given a price $p_i$ for a piece of each length $i$. It is the first example of dynamic programming in CLRS, Section 14.1. A plain recursion takes $\Theta(2^n)$ time because it solves the same [subproblems](/overlapping-subproblems/) again and again, while [memoization](/memoization/) or [tabulation](/tabulation/) takes $\Theta(n^2)$. The problem is the [unbounded knapsack](/unbounded-knapsack/) problem in which the weight of an item is its length.

## In plain words

A company buys long steel rods and sells short pieces. Each length has a fixed price, and a long piece is not always worth more than the short pieces it could be cut into. The question is where to cut a rod so that the pieces sell for the most money.

Look at the first piece that you cut from the left end. It has some length. The rest of the rod is a shorter rod, and you should cut it in the best way too. So the best answer for the whole rod is the best, over all lengths of the first piece, of that piece's price plus the best answer for the rest. A table of the best answers for all shorter rods, filled from the shortest up, gives each answer with a few lookups.

## Definition

**Input.** An integer $n \ge 0$ and prices $p_1, \ldots, p_n \ge 0$, where $p_i$ is the price of a piece of length $i$.

**Feasible solutions.** A decomposition of $n$ into an ordered list of positive integers $i_1 + i_2 + \cdots + i_k = n$, with $k \ge 1$ when $n \ge 1$. The list $(n)$ means no cut. The value is $p_{i_1} + \cdots + p_{i_k}$. Since the value does not depend on the order, it is enough to consider multisets of lengths.

**Output.** The largest value $r_n$ and a decomposition that reaches it. With $r_0 = 0$, the values satisfy, for $n \ge 1$,

$$ r_n = \max_{1 \le i \le n} \bigl( p_i + r_{n - i} \bigr). $$

Here $i$ is the length of the first piece and $r_{n-i}$ is the best value of the rest.

**Why the recurrence holds.** Take an optimal decomposition of $n$ and let $i$ be the length of its first piece. The other pieces form a decomposition of $n - i$. If some decomposition of $n - i$ had a larger value, putting the piece $i$ in front of it would give a better decomposition of $n$, which is not possible. So the rest is optimal for $n - i$ ([optimal substructure](/optimal-substructure/), proved by a [cut-and-paste argument](/cut-and-paste-argument/)), and $r_n = p_i + r_{n-i}$ for this $i$. For every other $i$, the piece $i$ plus an optimal decomposition of $n - i$ is feasible, so $r_n \ge p_i + r_{n-i}$. The two facts give the recurrence.

## Variants

- **A cost per cut.** Each cut costs a fixed $c$. The recurrence becomes $r_n = \max\bigl(p_n,\ \max_{1 \le i < n} (p_i + r_{n-i} - c)\bigr)$ (CLRS Exercise 14.1-3).
- **A limit on each length.** At most $\ell_i$ pieces of length $i$ may be sold. This is a [bounded knapsack](/bounded-knapsack/).
- **Only some lengths have a price.** Set $p_i = 0$ for the other lengths. A piece with no price is then the same as waste, so the model covers this case.
- **Minimum cost with an exact length.** Give each length a cost and ask for the cheapest way to make exactly $n$. The recurrence is the same with $\min$ and with $\infty$ for lengths that are not available, as in the [coin change problem](/coin-change-problem/).
- **Cutting with a cost that depends on the position.** If each cut at position $x$ costs an amount that depends on the length of the piece being cut, the problem becomes an [interval DP](/interval-dp/), as in the stick-cutting problem.
- **Two dimensions.** Cutting a sheet into rectangles by guillotine cuts has a similar recurrence over the sizes of rectangles.

## Examples

The price table of CLRS Section 14.1:

| length $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| price $p_i$ | 1 | 5 | 8 | 9 | 10 | 17 | 17 | 20 | 24 | 30 |
| best $r_i$ | 1 | 5 | 8 | 10 | 13 | 17 | 18 | 22 | 25 | 30 |
| first piece $s_i$ | 1 | 2 | 3 | 2 | 2 | 6 | 1 | 2 | 3 | 10 |
| pieces | 1 | 2 | 3 | 2+2 | 2+3 | 6 | 1+6 | 2+6 | 3+6 | 10 |

For $n = 4$ there are $2^{3} = 8$ ways to cut. The best is $2 + 2$ with value $5 + 5 = 10$, more than $p_4 = 9$ for no cut. The entry $r_7 = 18$ is reached as $p_1 + r_6 = 1 + 17$; it is also reached by $2 + 2 + 3$, with $5 + 5 + 8 = 18$. The row $s_i$ stores the first piece of one optimal choice, and a [traceback](/traceback/) reads the pieces: for $n = 9$, $s_9 = 3$, then $s_6 = 6$, so the pieces are $3$ and $6$.

**The density greedy fails.** Cut first the piece with the highest price per unit length that fits, then repeat (CLRS Exercise 14.1-2). For $n = 4$ the densities are $1, 2.5, 2.67, 2.25$, so greedy cuts 3 first and then 1, for $8 + 1 = 9$, while $r_4 = 10$.

**The cost of the plain recursion.** The recursion that tries each first piece and recurses on the rest, with no table, makes $2^n$ calls for a rod of length $n$: 16 calls for $n = 4$ and 1024 calls for $n = 10$.

## Known algorithms

- **Plain recursion (CUT-ROD).** Let $T(n)$ be the number of calls. Then $T(0) = 1$ and $T(n) = 1 + \sum_{j=0}^{n-1} T(j)$. By induction $T(n) = 2^n$: if $T(j) = 2^j$ for $j < n$, then $T(n) = 1 + (2^n - 1) = 2^n$. The time is $\Theta(2^n)$.
- **Memoized recursion.** Store $r_j$ the first time it is computed. Each $r_j$ is then computed once, with a loop of $j$ terms, so the time is $\sum_{j=1}^{n} \Theta(j) = \Theta(n^2)$.
- **Bottom-up table.** Compute $r_1, r_2, \ldots, r_n$ in this order. Two nested loops, $\Theta(n^2)$ time and $\Theta(n)$ space. Storing the maximizing $i$ as $s_j$ lets a traceback print the pieces in $O(n)$ more time.
- **As an unbounded knapsack.** Item $i$ has weight $i$ and value $p_i$, and the capacity is $n$. The knapsack table computes the same values, in $O(n \cdot m)$ time when only $m$ lengths have a positive price.

## Bounds

**Upper bound.** $\Theta(n^2)$ time with the table, in the word RAM with prices that fit in a word. The [subproblem graph](/subproblem-graph/) has $n + 1$ vertices and $n(n+1)/2$ edges, one for each pair $j > j - i \ge 0$, and the table does constant work per edge.

**Subquadratic algorithms.** Rod cutting is an unbounded knapsack in which the item lengths are $1, \ldots, n$ and the capacity is $n$. Cygan, Mucha, Węgrzycki and Włodarczyk show that an $O((n + t)^{2 - \varepsilon})$ algorithm for the unbounded knapsack with $n$ items and capacity $t$ exists if and only if one exists for (min,+)-convolution, which is conjectured not to exist. Their hard instances are not the special case of rod cutting, so this does not prove that rod cutting needs quadratic time.

**Lower bound.** Each algorithm must read the $n$ prices, so $\Omega(n)$ time is needed.

## Reductions

- **To the unbounded knapsack.** As above, with weight equal to length. With nonnegative prices, an unused part of the capacity can be sold as one more piece without loss of value, so the knapsack with capacity $n$ and the exact cut of length $n$ have the same optimum.
- **To a longest path in a DAG.** Make a vertex for each length $0, \ldots, n$ and an edge $j \to j - i$ of weight $p_i$. Then $r_n$ is the weight of a heaviest path from $n$ to $0$ in this [directed acyclic graph](/directed-acyclic-graph/), solved by [dynamic programming on a DAG](/dag-dynamic-programming/).
- **To the coin change problem.** With a value of $-1$ per piece and the goal of an exact length, the same table gives the fewest pieces, which is the [coin change problem](/coin-change-problem/).

## Applications

- **Stock cutting.** Cutting pipe, timber, cable or steel into lengths with market prices. Industrial versions add the limits on demand and many rods, and become cutting-stock problems.
- **Selling divisible goods.** Any good that can be split into integer units, with a price per bundle size, has the same model: data plans, bundles of shares, time slots.
- **Teaching.** CLRS uses rod cutting to show the gap between the exponential recursion and the quadratic table, and to introduce memoization, the bottom-up method, subproblem graphs and the reconstruction of a solution.

## References
