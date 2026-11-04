---
tag: H7Z6GX
kind: problem
slug: fractional-knapsack
name: Fractional knapsack
aliases:
- Fractional knapsack problem
- continuous knapsack problem
- fractional knapsack problem
area: techniques/greedy
level: intro
summary: Fill a capacity with divisible items to maximize value; taking items by value-to-weight ratio is optimal.
prereqs: [greedy-algorithm, knapsack-problem]
see_also: [greedy-fractional-knapsack, knapsack-dynamic-programming, exchange-argument, greedy-choice-property, lp-relaxation, knapsack-branch-and-bound, linear-programming-problem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 15.2, Elements of the greedy strategy (the 0-1 knapsack problem and the fractional knapsack problem)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, sixth edition
    locator: Chapter 17, The Knapsack Problem (fractional knapsack and the weighted median problem)
  - book: isbn:9780929306414
    title: Ellis Horowitz, Sartaj Sahni and Sanguthevar Rajasekaran, Computer Algorithms, second edition
    locator: Chapter 4, The Greedy Method (the knapsack problem)
---

The fractional knapsack problem asks how to fill a knapsack of capacity $W$ with parts of $n$ items, each with a value and a weight, so that the total value is as large as possible, when any fraction of an item may be taken. Taking the items in order of value per unit of weight, and a fraction of the first item that does not fit, is optimal. This [greedy algorithm](/greedy-algorithm/) runs in $O(n \log n)$ time, and a weighted median gives $O(n)$ time. It is the [linear programming relaxation](/lp-relaxation/) of the [0-1 knapsack problem](/knapsack-problem/), where the same greedy rule fails.

## In plain words

A thief has a bag that can carry a fixed weight. In the shop there is gold dust, silver dust and some spices, each in a limited amount, and each has a price per gram. Because the goods are powders, the thief can take any amount of each, up to what the shop has.

The best plan is to take the goods with the highest price per gram first. Take all of the best one, then all of the next one, and so on. When the next one does not fit in full, take as much of it as fits, and stop.

If the goods are solid objects that must be taken whole or left, the same plan can be bad. A light but cheap object can use up space that a heavy, valuable object needed. That is the harder 0-1 knapsack problem.

## Definition

**Input.** A capacity $W \ge 0$ and $n$ items. Item $i$ has a value $v_i \ge 0$ and a weight $w_i > 0$.

**Output.** Fractions $x_1, \ldots, x_n$ that solve the [linear program](/linear-programming-problem/)
$$ \text{maximize } \sum_{i=1}^{n} v_i x_i \quad \text{subject to} \quad \sum_{i=1}^{n} w_i x_i \le W, \qquad 0 \le x_i \le 1 \ (1 \le i \le n). $$

The *ratio* of item $i$ is $\rho_i = v_i / w_i$, its value per unit of weight.

**The greedy solution.** Order the items so that $\rho_1 \ge \rho_2 \ge \cdots \ge \rho_n$. If $\sum_i w_i \le W$, take all items: $g_i = 1$ for all $i$. Else let $k$ be the least index with $w_1 + \cdots + w_k > W$, and set
$$ g_i = 1 \ (i < k), \qquad g_k = \frac{W - (w_1 + \cdots + w_{k-1})}{w_k}, \qquad g_i = 0 \ (i > k). $$
Then $0 \le g_k < 1$ and $\sum_i w_i g_i = W$.

**Theorem.** The greedy solution $g$ is optimal.

*Proof.* If $\sum_i w_i \le W$, then $g_i = 1$ is the largest value of each $x_i$, and $v_i \ge 0$, so no feasible $x$ has a larger value. Otherwise let $r = \rho_k \ge 0$ and let $x$ be any feasible solution. For $i < k$, $x_i - g_i = x_i - 1 \le 0$ and $\rho_i \ge r$, so $\rho_i w_i (x_i - g_i) \le r\, w_i (x_i - g_i)$. For $i > k$, $x_i - g_i = x_i \ge 0$ and $\rho_i \le r$, so the same inequality holds. For $i = k$ it is an equality. Summing over $i$, and using $v_i = \rho_i w_i$,
$$ \sum_i v_i x_i - \sum_i v_i g_i \le r \Bigl(\sum_i w_i x_i - \sum_i w_i g_i\Bigr) \le r\,(W - W) = 0. $$
So $\sum_i v_i x_i \le \sum_i v_i g_i$. $\square$

The proof is an [exchange argument](/exchange-argument/) in compact form: moving weight from a higher-ratio item to a lower-ratio item never gains value. It holds for every order of items with equal ratios. The number $r$ is the optimal dual variable of the capacity constraint.

## Variants

- **0-1 knapsack.** Each $x_i$ must be 0 or 1. This is the [knapsack problem](/knapsack-problem/), which is NP-hard. The greedy rule by ratio can be far from optimal there, but the fractional optimum is an upper bound on the 0-1 optimum, which [branch and bound](/knapsack-branch-and-bound/) uses.
- **Bounded amounts.** Item $i$ is available in an amount $u_i$ instead of 1. Scale: replace $w_i$ by $u_i w_i$ and $v_i$ by $u_i v_i$, and the problem is the same.
- **Unbounded items.** If any amount of each item may be taken, the optimum takes $W / w_i$ units of an item of the largest ratio.
- **Several constraints.** With two or more capacity constraints, the problem is a general linear program, and the ratio rule no longer applies.
- **Minimization form.** Cover a demand $D$ at the least cost, with costs $c_i$ and amounts $w_i$: take the items in increasing order of $c_i / w_i$. The same proof applies with the inequalities reversed.

## Examples

**The CLRS instance.** Capacity $W = 50$ and three items with $(v_i, w_i) = (60, 10), (100, 20), (120, 30)$, so the ratios are 6, 5 and 4. The greedy solution takes items 1 and 2 in full (weight 30) and $20/30 = 2/3$ of item 3, for a value of $60 + 100 + 80 = 240$. For the 0-1 version, the optimum is 220 with items 2 and 3, and the ratio rule, which takes items 1 and 2 and then cannot fit item 3, reaches only 160.

**A larger instance.** Capacity $W = 60$ and five items:

| item | $v_i$ | $w_i$ | ratio $\rho_i$ | greedy order | fraction taken | value taken |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 30 | 5 | 6 | 1st | 1 | 30 |
| 2 | 40 | 10 | 4 | 2nd | 1 | 40 |
| 3 | 45 | 15 | 3 | 5th | 0 | 0 |
| 4 | 77 | 22 | 3.5 | 4th | $10/11$ | 70 |
| 5 | 90 | 25 | 3.6 | 3rd | 1 | 90 |

After items 1, 2 and 5 the remaining capacity is $60 - 40 = 20$, so the greedy solution takes $20/22 = 10/11$ of item 4. The optimum is 230, with dual value $r = 3.5$. In the 0-1 version, the ratio rule takes items 1, 2, 5 and then item 3 (weight 15 fits in 20), for 205; the 0-1 optimum is 207, with items 2, 4 and 5 and weight 57.

**Equal ratios.** If all ratios are equal to $\rho$, every solution that fills the knapsack is optimal, with value $\rho \min(W, \sum_i w_i)$.

## Known algorithms

- **[Greedy by ratio](/greedy-fractional-knapsack/).** Sort by ratio, then take items until the capacity is reached. $O(n \log n)$ time for the sort and $O(n)$ for the scan.
- **Weighted median, linear time.** The greedy solution only needs the *critical item* $k$ and the set of items with a larger ratio. Find it as a weighted median of the ratios: pick the median ratio with a linear-time [selection](/median-of-medians/) algorithm, split the items into those with a larger, equal and smaller ratio, compare the weight of the first group with $W$, and recurse into one side. Each round halves the number of items and costs linear time, so the total is $O(n)$. Korte and Vygen give this algorithm in Chapter 17.
- **[Linear programming](/linear-programming-problem/).** A general LP solver also solves the problem, but much more slowly than the ratio rule.

## Bounds

- **Upper bound.** $O(n)$ time in the worst case with the weighted median method, $O(n \log n)$ with sorting.
- **Lower bound.** $\Omega(n)$ time, because each item can change the answer and must be read.
- **Structure of the optimum.** Some optimal solution has at most one fractional $x_i$: the greedy solution. If all ratios are distinct, the greedy solution is the unique optimum when $\sum_i w_i > W$ and $\rho_k > 0$.

## Reductions

- **Relaxation of 0-1 knapsack.** Replacing $x_i \in \{0, 1\}$ by $0 \le x_i \le 1$ gives this problem. Its optimum $z_{LP}$ bounds the 0-1 optimum $z$ from above, and $z_{LP} \le z + \max_i v_i$ when every item fits alone ($w_i \le W$), because the greedy integer part plus the critical item is worth at least $z_{LP}$. This gives the 2-approximation for 0-1 knapsack that takes the better of the greedy integer part and the most valuable item.
- **To linear programming.** The problem is a linear program with one constraint and box bounds, and the ratio rule is the simplex method run by hand on this special form.

## Applications

- **Bounds in branch and bound.** The fractional optimum is the standard upper bound for 0-1 knapsack in [knapsack branch and bound](/knapsack-branch-and-bound/).
- **Divisible resources.** Loading a bulk carrier, blending, buying a budget of divisible goods, or allocating a bandwidth among streams with linear values.
- **Teaching.** CLRS uses the pair of fractional and 0-1 knapsack to show that a greedy algorithm that works for one problem can fail for a close relative.

## References
