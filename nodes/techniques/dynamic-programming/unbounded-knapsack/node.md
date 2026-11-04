---
tag: Q2KGB0
kind: problem
slug: unbounded-knapsack
name: Unbounded knapsack problem
aliases:
- unlimited knapsack
area: techniques/dynamic-programming
level: intro
summary: Knapsack variant where each item type may be taken any number of times.
prereqs: [knapsack-problem, optimal-substructure, tabulation]
see_also: [knapsack-dynamic-programming, bounded-knapsack, rod-cutting-problem, coin-change-problem, rolling-array-space-reduction, pseudo-polynomial-time, weak-np-hardness, min-plus-convolution]
sources:
  - book: isbn:9783540402862
    title: Hans Kellerer, Ulrich Pferschy and David Pisinger, Knapsack Problems, Springer, 2004
    locator: Chapter 8, The Unbounded Knapsack Problem, pp. 211 to 234 (Section 8.2 periodicity and dominance, Section 8.3 dynamic programming, Section 8.5 approximation)
  - book: isbn:9780073523408
    title: Dasgupta, Papadimitriou and Vazirani, Algorithms
    locator: Section 6.4, Knapsack (knapsack with repetition and without repetition)
  - paper: doi:10.1145/3293465
    title: Marek Cygan, Marcin Mucha, Karol Węgrzycki and Michał Włodarczyk, On problems equivalent to (min,+)-convolution, ACM Transactions on Algorithms 15(1), 2019
    locator: Article 14, the main equivalence theorem (Unbounded Knapsack in time O((n + t)^(2 − ε)))
---

The unbounded knapsack problem gives $n$ item types, each with a weight and a value, and a capacity $W$, and asks for the largest total value of a multiset of items whose total weight is at most $W$, where each type may be taken any number of times. It differs from the 0/1 [knapsack problem](/knapsack-problem/) only in that limit. A dynamic program over the capacities $0, \ldots, W$ solves it in $O(nW)$ time and $O(W)$ space, which is [pseudo-polynomial](/pseudo-polynomial-time/). [Rod cutting](/rod-cutting-problem/) and the [coin change problem](/coin-change-problem/) are special cases.

## In plain words

A thief has a bag that holds a fixed weight. A shop has several kinds of goods, and the shelves never run out: each kind can be taken as often as the thief likes. Each kind has a weight and a value. The thief wants the most value that still fits in the bag.

Think of the last item that goes into the bag. Whatever kind it is, the rest of the bag is a smaller bag, and the rest should be packed in the best way. So the best value for each bag size comes from the best values of smaller bag sizes. A table over all bag sizes, from empty upward, fills in each entry by trying each kind as the last item.

## Definition

**Input.** Item types $1, \ldots, n$ with integer weights $w_i \ge 1$ and values $v_i \ge 0$, and an integer capacity $W \ge 0$.

**Feasible solutions.** Vectors $x \in \mathbb{Z}_{\ge 0}^{n}$ with $\sum_i w_i x_i \le W$. The number $x_i$ is the number of copies of type $i$.

**Output.** A feasible $x$ that maximizes $\sum_i v_i x_i$, and the maximum value $K(W)$.

**Recurrence.** $K(c)$ is the best value for capacity $c$. Then $K(0) = 0$, and for $c \ge 1$,

$$ K(c) = \max\Bigl( 0,\ \max_{i : w_i \le c} \bigl( K(c - w_i) + v_i \bigr) \Bigr). $$

The term $0$ is the empty bag. To prove the recurrence, take an optimal multiset for $c$. If it is empty, its value is $0$ and every term on the right is at most $0$, since each term is the value of a feasible multiset. Otherwise remove one copy of some type $i$ in it. The rest fits in $c - w_i$, and if a better multiset existed for $c - w_i$, adding the copy back would beat the optimum for $c$. So $K(c) = K(c - w_i) + v_i$ for this $i$. Each other term is the value of a feasible multiset for $c$ and is at most $K(c)$.

## Variants

- **0/1 knapsack.** Each type at most once. The table needs the items as a second index; see [knapsack dynamic programming](/knapsack-dynamic-programming/).
- **Bounded knapsack.** Type $i$ at most $c_i$ times; see [bounded knapsack](/bounded-knapsack/).
- **Exact fill.** The weight must equal $W$. Start with $K(0) = 0$ and $K(c) = -\infty$ for $c > 0$, and drop the term $0$. Change making is this form with value $-1$ per coin.
- **Minimization form.** Each type has a cost, and the total weight must be at least $W$, at least cost. This is the covering form, used for buying packs of a product.
- **Fractional form.** Copies may be taken in any real amount. Then the type with the best ratio $v_i / w_i$ alone is optimal, as in the [fractional knapsack](/fractional-knapsack/).
- **Decision form.** Given a target $V$, decide whether some feasible $x$ has value at least $V$.

## Examples

Take the instance of DPV Section 6.4: capacity $W = 10$ and the four types $(w, v) = (6, 30), (3, 14), (4, 16), (2, 9)$.

| capacity $c$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| unbounded $K(c)$ | 0 | 0 | 9 | 14 | 18 | 23 | 30 | 32 | 39 | 44 | 48 |
| 0/1 knapsack | 0 | 0 | 9 | 14 | 16 | 23 | 30 | 30 | 39 | 44 | 46 |

With repetition the best for $W = 10$ is $48$: one copy of $(6, 30)$ and two of $(2, 9)$. Without repetition it is $46$: $(6, 30)$ and $(4, 16)$. The two rows first differ at $c = 4$, where two copies of $(2, 9)$ give $18$.

**The order of the loops.** With a one-dimensional array $K[0 \ldots W]$, both problems use the update $K[c] \leftarrow \max(K[c], K[c - w] + v)$ for each item and each $c \ge w$. The only difference is the direction of the loop over $c$.

```text
for each item (w, v):                      for each item (w, v):
    for c = w, w+1, ..., W:                    for c = W, W-1, ..., w:
        K[c] = max(K[c], K[c-w] + v)               K[c] = max(K[c], K[c-w] + v)
       unbounded: c goes up                       0/1: c goes down
```

When $c$ goes up, $K[c - w]$ has already been updated for this item, so it may already contain copies of the item, and the update adds one more. When $c$ goes down, $K[c - w]$ still holds the value without the item, so the item is used at most once. On the instance above, the upward loop gives the first row of the table and the downward loop gives the second.

**Periodicity.** In this instance the type $(6, 30)$ has the best ratio, $5$. For every $c \ge 8$, $K(c) = K(c - 6) + 30$, while $K(7) = 32 > K(1) + 30$. So for large capacities the table repeats with period 6, as the lemma in the Bounds section predicts.

## Known algorithms

- **Table over capacities.** Fill $K(0), \ldots, K(W)$ with the recurrence: $O(nW)$ time, $O(W)$ space. Store the maximizing type for each $c$ and follow it back to list the items; on the instance above this gives types $(6, 30)$, $(2, 9)$, $(2, 9)$.
- **One array, items outer.** The upward loop shown above gives the same values in the same time and space. It is the knapsack form of [rolling-array space reduction](/rolling-array-space-reduction/): the table over items and capacities shrinks to one row.
- **Dominance and periodicity.** Remove each type $j$ that is dominated by another type $i$ with $w_i \le w_j$ and $v_i \ge v_j$, or by a multiple of $i$. Stop the table once it becomes periodic. Both ideas are in Kellerer, Pferschy and Pisinger, Section 8.2.
- **Approximation.** The problem has an [FPTAS](/fptas/), by scaling the values as for the 0/1 knapsack (Kellerer, Pferschy and Pisinger, Section 8.5).

## Bounds

**Complexity.** The decision form is NP-complete, and the problem is [weakly NP-hard](/weak-np-hardness/): it is NP-hard when the numbers are in binary, and the $O(nW)$ table is polynomial in the value of $W$.

**Fine-grained equivalence.** Cygan, Mucha, Węgrzycki and Włodarczyk prove that the unbounded knapsack with $n$ items and capacity $t$ has an algorithm with time $O((n + t)^{2 - \varepsilon})$ for some $\varepsilon > 0$ if and only if [(min,+)-convolution](/min-plus-convolution/) of two sequences of length $N$ has an algorithm with time $O(N^{2 - \varepsilon'})$. No such algorithm is known.

**Periodicity lemma.** Let type $1$ have the best ratio, $v_1 / w_1 \ge v_i / w_i$ for all $i$, with $v_1 > 0$, and let $w_{\max}$ be the largest weight. Then $K(c) = K(c - w_1) + v_1$ for every $c \ge (w_1 - 1) w_{\max} + w_1$.

*Proof.* Among the optimal solutions for $c$, take one with the most copies of type $1$. Suppose it holds at least $w_1$ items of other types. List $w_1$ of them and form the $w_1$ prefix sums of their weights. Either some prefix sum is $\equiv 0 \pmod{w_1}$, or two of them are equal modulo $w_1$ by the pigeonhole principle, since there are only $w_1 - 1$ nonzero residues. In both cases some nonempty set $S$ of these items has total weight $q w_1$ for an integer $q \ge 1$. Its value is at most $(v_1 / w_1) \cdot q w_1 = q v_1$. Replace $S$ by $q$ copies of type $1$: the weight is the same, the value does not drop, and the count of type $1$ grows. This contradicts the choice. So the solution has at most $w_1 - 1$ items of other types, of total weight at most $(w_1 - 1) w_{\max}$. If it had no copy of type $1$, its weight would be at most $(w_1 - 1) w_{\max} \le c - w_1$, and adding one copy of type 1 would raise the value by $v_1 > 0$, a contradiction. So it has a copy of type 1. Removing it leaves a feasible solution for $c - w_1$, so $K(c - w_1) \ge K(c) - v_1$. Adding a copy of type 1 to an optimal solution for $c - w_1$ gives $K(c) \ge K(c - w_1) + v_1$. ∎

So for a very large $W$, the table needs to run only up to about $w_1 w_{\max}$, and the answer for $W$ follows by adding copies of type $1$.

## Reductions

- **From rod cutting.** A piece of length $i$ with price $p_i$ is a type of weight $i$ and value $p_i$, with capacity $n$.
- **From change making.** A coin $d$ is a type of weight $d$ and value $-1$, with an exact fill.
- **To the 0/1 knapsack.** Replace type $i$ by $\lfloor \log_2 (W / w_i) \rfloor + 1$ items that stand for $1, 2, 4, \ldots$ copies. Every count up to $\lfloor W / w_i \rfloor$ is a sum of distinct powers of two; the same idea for a finite bound is proved on the [bounded knapsack](/bounded-knapsack/) page. Cygan et al. show that a $T(n, t)$ algorithm for the 0/1 knapsack gives an $O(T(n, t) \log t)$ algorithm for the unbounded one.
- **To a longest path in a DAG.** Vertices $0, \ldots, W$, an edge $c \to c + w_i$ of weight $v_i$ for each $c$ and $i$, and edges $c \to c + 1$ of weight $0$. Then $K(W)$ is the heaviest path from $0$ to $W$; see [dynamic programming on DAGs](/dag-dynamic-programming/).

## Applications

- **Cutting stock.** Choosing the pattern of pieces to cut from one stock length, with unlimited demand, is an unbounded knapsack. The column generation method for the cutting-stock problem solves one such knapsack in each round to find a new cutting pattern.
- **Purchasing.** Buying packs of fixed sizes and prices to reach a total quantity at least cost is the minimization form.
- **Resource allocation.** Repeated tasks with a fixed resource use and a fixed profit, under one budget.
- **Integer programming.** It is the knapsack problem with one constraint and general integer variables, a building block of cutting planes and relaxations.

## References
