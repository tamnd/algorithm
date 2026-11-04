---
tag: XE00JC
kind: problem
slug: bounded-knapsack
name: Bounded knapsack
aliases:
- Bounded (multiple) knapsack
area: techniques/dynamic-programming
level: core
summary: Knapsack variant where each item type has a limited number of copies, solved by binary splitting or monotone queue dynamic programming.
prereqs: [knapsack-problem, knapsack-dynamic-programming, monotonic-deque]
see_also: [unbounded-knapsack, multiple-knapsack-problem, sliding-window-maximum, rolling-array-space-reduction, pseudo-polynomial-time, weak-np-hardness, coin-change-problem, rod-cutting-problem]
sources:
  - book: isbn:9783540402862
    title: Hans Kellerer, Ulrich Pferschy and David Pisinger, Knapsack Problems, Springer, 2004
    locator: Chapter 7, The Bounded Knapsack Problem, pp. 185 to 209 (Section 7.1 with the transformation of the bounded problem into a 0/1 knapsack, and Section 7.2 dynamic programming)
  - book: isbn:9780471924203
    title: Silvano Martello and Paolo Toth, Knapsack Problems, Algorithms and Computer Implementations, Wiley, 1990
    locator: Chapter 3 (the bounded knapsack problem)
  - paper: doi:10.1007/s006070050042
    title: Ulrich Pferschy, Dynamic programming revisited, improving knapsack algorithms, Computing 63(4), 1999
    locator: pp. 419 to 430 (the bounded knapsack problem in O(nc) time and O(n + c) space)
  - paper: doi:10.1145/3293465
    title: Marek Cygan, Marcin Mucha, Karol Węgrzycki and Michał Włodarczyk, On problems equivalent to (min,+)-convolution, ACM Transactions on Algorithms 15(1), 2019
    locator: Article 14, the main equivalence theorem (0/1 Knapsack in time O((n + t)^(2 − ε)))
---

The bounded knapsack problem gives $n$ item types, each with a weight, a value and a number of available copies, and a capacity $W$, and asks for the largest total value of a selection that fits, with type $i$ used at most $c_i$ times. It lies between the 0/1 [knapsack problem](/knapsack-problem/), where each $c_i = 1$, and the [unbounded knapsack](/unbounded-knapsack/), where no limit applies. The plain dynamic program takes $O(W \sum_i c_i)$ time, binary splitting of the copies takes $O(W \sum_i \log c_i)$, and a [monotonic deque](/monotonic-deque/) over residue classes takes $O(nW)$, the same as the 0/1 case.

## In plain words

A shop has several kinds of goods, but only a few of each kind in stock. A buyer with a bag of fixed capacity wants the most value that fits.

The simple idea treats every copy as a separate item and runs the usual knapsack table. This is slow when a kind has many copies. A better idea packs the copies of a kind into bundles of 1, 2, 4, 8 and so on, plus one bundle for the rest. Any number of copies, from none to all, is a choice of some of these bundles, and there are only a few bundles. The best method looks at the capacities that differ by the weight of one item and finds the best choice for each of them with a sliding window, so each kind costs the same as a single item.

## Definition

**Input.** Item types $1, \ldots, n$ with integer weights $w_i \ge 1$, values $v_i \ge 0$ and bounds $c_i \ge 0$, and an integer capacity $W \ge 0$.

**Feasible solutions.** Integer vectors $x$ with $0 \le x_i \le c_i$ for each $i$ and $\sum_i w_i x_i \le W$.

**Output.** A feasible $x$ that maximizes $\sum_i v_i x_i$.

**Recurrence.** Let $K_j(t)$ be the best value with types $1, \ldots, j$ and capacity $t$. Then $K_0(t) = 0$ for all $t \ge 0$, and for $j \ge 1$,

$$ K_j(t) = \max_{0 \le k \le \min(c_j,\ \lfloor t / w_j \rfloor)} \bigl( K_{j-1}(t - k w_j) + k v_j \bigr). $$

The index $k$ is the number of copies of type $j$. An optimal solution for $(j, t)$ uses some $k$ copies of type $j$, and its other items form a solution for $(j - 1, t - k w_j)$, which must be optimal or the whole could be improved. Each $k$ in the range gives a feasible solution. So the maximum is right.

## Variants

- **0/1 knapsack.** All $c_i = 1$.
- **Unbounded knapsack.** All $c_i \ge \lfloor W / w_i \rfloor$, so the limit never binds.
- **Bounded change making.** Minimize the number of coins with at most $c_i$ coins of value $d_i$ and an exact sum.
- **Bounded subset sum.** All $v_i = w_i$. Ask whether the weight $W$ can be reached exactly.
- **Multiple knapsacks.** Several bags instead of one; see the [multiple knapsack problem](/multiple-knapsack-problem/). It is a different problem despite the alias "multiple" used for the bounded one.
- **Counting form.** Count the vectors $x$ with $\sum_i w_i x_i = W$. The monotone deque does not apply, but a sliding window sum does.

## Examples

Take $W = 10$ and the types $(w, v, c) = (2, 3, 3)$, $(3, 5, 2)$, $(5, 9, 1)$.

| capacity $t$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $K_1(t)$ | 0 | 0 | 3 | 3 | 6 | 6 | 9 | 9 | 9 | 9 | 9 |
| $K_2(t)$ | 0 | 0 | 3 | 5 | 6 | 8 | 10 | 11 | 13 | 14 | 16 |
| $K_3(t)$ | 0 | 0 | 3 | 5 | 6 | 9 | 10 | 12 | 14 | 15 | 17 |

The optimum is $17$ with one copy of each type: weight $2 + 3 + 5 = 10$, value $3 + 5 + 9 = 17$. Without the limits the best is $18$, two copies of $(5, 9)$. The row $K_1$ stops growing at $t = 6$ because only three copies of $(2, 3)$ exist.

**Binary splitting.** The bound $c = 13$ splits into bundles of $1, 2, 4, 6$ copies. The bound $c = 100$ splits into $1, 2, 4, 8, 16, 32, 37$. The bound $c = 5$ splits into $1, 2, 2$.

**The monotone deque, one residue class.** Add type $(3, 5, 2)$ to the row $K_1$. The capacities $1, 4, 7, 10$ form the class of residue 1 modulo 3. Write $t = 1 + 3k$ and $g(k) = K_1(1 + 3k) - 5k$. Then $g = 0, 1, -1, -6$ for $k = 0, 1, 2, 3$. The new value is $K_2(1 + 3k) = 5k + \max\{ g(k') : k - 2 \le k' \le k \}$, a maximum over a window of 3 consecutive entries. This gives $0$, $5 + 1 = 6$, $10 + 1 = 11$ and $15 + 1 = 16$, as in the row $K_2$.

## Known algorithms

- **Copy expansion.** Replace type $i$ by $c_i$ separate 0/1 items and run the [0/1 knapsack table](/knapsack-dynamic-programming/). Time $O(W \sum_i c_i)$, space $O(W)$. Evaluating the recurrence directly over all $k$ costs the same.
- **Binary splitting.** Replace type $i$ by $O(\log c_i)$ bundles, each a 0/1 item with weight $q w_i$ and value $q v_i$ for a bundle of $q$ copies. Time $O(W \sum_i \log (c_i + 1))$. The bundles and the proof are below. Kellerer, Pferschy and Pisinger describe this transformation of the bounded problem into a 0/1 knapsack in Section 7.1.
- **Monotone deque over residue classes.** For type $j$ and each residue $r \in \{0, \ldots, w_j - 1\}$, walk $t = r, r + w_j, r + 2w_j, \ldots \le W$. With $t = r + k w_j$ and $g(k) = K_{j-1}(r + k w_j) - k v_j$, the recurrence becomes $K_j(r + k w_j) = k v_j + \max_{k - c_j \le k' \le k,\ k' \ge 0} g(k')$. This is a [sliding window maximum](/sliding-window-maximum/) with window $c_j + 1$. A deque that keeps indices with decreasing $g$ gives each maximum in amortized $O(1)$ time, because each index enters and leaves the deque at most once. Each capacity is in exactly one class, so type $j$ costs $O(W)$, and the total is $O(nW)$ time with two rows of $O(W)$ space.
- **Pferschy's algorithm.** Pferschy shows that the bounded knapsack problem is solved in $O(nW)$ time and $O(n + W)$ space, so the solution vector, not only the value, comes at the cost of the 0/1 case.
- **Branch and bound and approximation.** Kellerer, Pferschy and Pisinger, Sections 7.3 and 7.4, give exact branch-and-bound methods and approximation algorithms.

## Bounds

**Binary splitting is exact.** For $c \ge 0$, let $t$ be the largest integer with $2^t - 1 \le c$, and let $R = c - (2^t - 1)$. The bundles are $1, 2, 4, \ldots, 2^{t-1}$ and, if $R > 0$, one more bundle $R$. Then:

1. *Every count $m \in \{0, \ldots, c\}$ is the sum of some of the bundles.* The sums of subsets of $\{1, 2, \ldots, 2^{t-1}\}$ are exactly $0, \ldots, 2^t - 1$, by binary notation. This covers $m \le 2^t - 1$. By the choice of $t$, $2^{t+1} - 1 > c$, so $R < 2^t$. For $2^t \le m \le c$, let $m' = m - R$. Then $m' \le c - R = 2^t - 1$ and $m' \ge 2^t - R > 0$. So $m'$ is the sum of some powers of two, and $m = m' + R$ adds the bundle $R$.
2. *No sum of bundles exceeds $c$.* The sum of all bundles is $2^t - 1 + R = c$.

So the 0/1 choices over the bundles of type $i$ give exactly the counts $0, \ldots, c_i$ of the bounded problem, with the same weights and values, and the two problems have the same optimum. The number of bundles is $t + [R > 0] \le \lfloor \log_2 (c + 1) \rfloor + 1$.

**Upper bound.** $O(nW)$ time by the deque method, $O(n + W)$ space with Pferschy's method, in the word RAM. This matches the bound of the 0/1 knapsack table.

**Hardness.** The problem contains the 0/1 knapsack, so it is NP-hard when the numbers are in binary. The $O(nW)$ table makes it [weakly NP-hard](/weak-np-hardness/), and the running time is [pseudo-polynomial](/pseudo-polynomial-time/). Cygan, Mucha, Węgrzycki and Włodarczyk (2019) show that an $O((n + W)^{2 - \varepsilon})$ algorithm for the 0/1 knapsack would give a subquadratic algorithm for (min,+)-convolution. Since the bounded problem includes the 0/1 problem, the same conditional bound applies to it.

## Reductions

- **To the 0/1 knapsack.** By binary splitting, with $\sum_i O(\log c_i)$ items. This is a polynomial reduction, since $\log c_i$ is at most the length of $c_i$ in binary.
- **From the 0/1 knapsack.** Set all $c_i = 1$.
- **From the unbounded knapsack.** Set $c_i = \lfloor W / w_i \rfloor$.
- **To a longest path.** The table is a longest path in the layered [DAG](/directed-acyclic-graph/) of states $(j, t)$, with an edge from $(j - 1, t - k w_j)$ to $(j, t)$ of weight $k v_j$ for $0 \le k \le c_j$.

## Applications

- **Stock with limited supply.** Loading goods of a few kinds, each with a known number of units, into one container or one budget.
- **Bounded change making.** A cash drawer with a known number of each coin.
- **Production planning.** Several products with a demand cap each, a profit per unit and a shared machine time.
- **Subroutine of larger solvers.** Column generation methods for cutting and packing with limited demand can call a bounded knapsack to find each new pattern.

## References
