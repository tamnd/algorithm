---
tag: SZVHAQ
kind: technique
slug: rounding-and-scaling
name: Rounding and scaling
aliases:
- rounding technique
- scaling technique
- scaling and rounding
- rounding the input
area: approximation/approximation-schemes
level: core
summary: Scale the numeric input values down and round them so that a dynamic program over the rounded values runs in polynomial time.
prereqs: [approximation-ratio, pseudo-polynomial-time, profit-indexed-dynamic-programming]
see_also: [knapsack-fptas, trimming-technique, fptas, ptas, no-fptas-for-strongly-np-hard-problems, dual-approximation, hochbaum-shmoys-makespan-ptas, chekuri-khanna-ptas]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 3 (Rounding data and dynamic programming), Sections 3.1 to 3.3
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms, Springer, 2001
    locator: Chapter 8 (Knapsack), Section 8.2, and Chapter 9 (Bin packing)
  - paper: doi:10.1145/321906.321909
    title: Oscar H. Ibarra and Chul E. Kim, Fast approximation algorithms for the knapsack and sum of subset problems, Journal of the ACM 22(4), 1975
    locator: pages 463 to 468
  - paper: doi:10.1145/322077.322090
    title: Michael R. Garey and David S. Johnson, "Strong" NP-completeness results, motivation, examples, and implications, Journal of the ACM 25(3), 1978
    locator: pages 499 to 508 (the link between pseudo-polynomial algorithms and FPTAS)
---

Rounding and scaling is the most common way to build an approximation scheme from an exact algorithm whose time depends on the size of the numbers. Divide each number of the objective by a scale $K$ and round. The rounded numbers are small integers, so a [pseudo-polynomial](/pseudo-polynomial-time/) exact algorithm runs on them in polynomial time. Each rounded number is off by less than $K$ after the scaling back, so a solution that uses at most $n$ numbers is off by less than $nK$. With $K = \varepsilon \cdot \mathrm{LB} / n$, where $\mathrm{LB}$ is a lower bound on the optimum, the loss is at most $\varepsilon \cdot \mathrm{OPT}$. The standard example is the [knapsack FPTAS](/knapsack-fptas/). Other forms round to powers of $1 + \varepsilon$, or round sizes into a few classes, and they give many PTAS and APTAS results.

## In plain words

Some exact methods are fast when the numbers in the input are small, and slow when they are large. Rounding makes the numbers small on purpose. Divide all of them by the same amount and drop the fractions. The exact method is now fast, and it finds the best answer for the rounded numbers.

That answer may not be the best for the true numbers, because the rounding changed each number a little. The trick is to choose the divisor so that the total change is small next to the value of the best answer. If each number changes by less than $K$, and an answer uses $n$ numbers, the total change is less than $nK$. So pick $K$ as a small part of the optimum, divided by $n$. You do not know the optimum, but a simple lower bound on it is enough.

## When it applies

Look for these signals:

- There is an exact algorithm whose time is polynomial in $n$ and in the largest number $a_{\max}$ of the objective, for example a [profit-indexed dynamic program](/profit-indexed-dynamic-programming/).
- The objective of a solution is a sum of at most $n$ numbers of the input, so the rounding errors add up to at most $n$ times the error of one number.
- There is a lower bound $\mathrm{LB} \le \mathrm{OPT}$, computable in polynomial time, with $\mathrm{OPT} \le c \cdot \mathrm{LB}$ for a constant or polynomial $c$. For knapsack, the largest profit of an item that fits gives $c = n$, and the greedy 1/2-approximation gives $c = 2$.
- Only the objective is rounded. The constraints keep their true numbers, so each solution of the rounded instance is feasible for the true instance.

If the constraints must also be rounded, as in bin packing and scheduling, the method still works, but the solution is feasible only for a relaxed instance, and an extra step must repair it. This is the [dual approximation](/dual-approximation/) form.

## The template

The template is for a maximization problem whose objective is $a(T) = \sum_{j \in T} a_j$ with $|T| \le n$. The holes are the lower bound, the direction of the rounding and the exact algorithm.

```pseudo id=main
ROUND-AND-SOLVE(instance I with objective numbers a_1 .. a_n, ε)
L1  LB ← a lower bound with LB ≤ OPT ≤ c · LB        ▷ hole: a simple approximation
L2  K ← ε · LB / n                                   ▷ n numbers add their errors
L3  if K ≤ 1 then return EXACT(I)                    ▷ the numbers are already small
L4  for j ← 1 to n do a'_j ← ⌊a_j / K⌋               ▷ hole: down for max; a cap for min
L5  S ← EXACT(I with a'_j in place of a_j)           ▷ hole: pseudo-polynomial, time poly(n, max a')
L6  return S
```

**Lemma (the rounding loss).** For each solution $T$, $K \, a'(T) \le a(T) < K \, a'(T) + |T| K$.

*Proof.* For each $j$, $a_j / K - 1 < \lfloor a_j / K \rfloor \le a_j / K$. Multiply by $K$ and add over $T$. $\square$

**Theorem.** The set $S$ of line L5 has $a(S) \ge (1 - \varepsilon) \cdot \mathrm{OPT}$.

*Proof.* Let $O$ be an optimal solution. Line L5 is exact on the rounded numbers, so $a'(S) \ge a'(O)$. By the lemma,

$$
a(S) \ge K a'(S) \ge K a'(O) > a(O) - nK = \mathrm{OPT} - \varepsilon \, \mathrm{LB} \ge (1 - \varepsilon) \, \mathrm{OPT}. \qquad \square
$$

**Time.** A solution worth more than $\mathrm{OPT} \le c \cdot \mathrm{LB}$ does not exist, so each useful rounded value is at most $c \cdot \mathrm{LB} / K = c n / \varepsilon$. A number $a_j > c \cdot \mathrm{LB}$ is in no feasible solution when the numbers are non-negative, and it can be dropped. So the exact algorithm runs with $a'_{\max} \le cn / \varepsilon$, which is polynomial in $n$ and $1 / \varepsilon$ when $c$ is polynomial. For the knapsack FPTAS with $c = n$, the table has $O(n^2 / \varepsilon)$ columns and the time is $O(n^3 / \varepsilon)$.

For a minimization problem the same lemma gives $a(S) < K a'(S) + nK \le K a'(O) + nK \le \mathrm{OPT} + \varepsilon \, \mathrm{LB} \le (1 + \varepsilon) \, \mathrm{OPT}$. Here the cap matters: the numbers above $c \cdot \mathrm{LB}$ cannot be dropped if every solution must use some of them, so replace them by the value $\lfloor c \cdot \mathrm{LB} / K \rfloor + 1$, which is still too large for any solution of cost at most $c \cdot \mathrm{LB}$.

### A worked rounding

Take the knapsack items of the [knapsack FPTAS](/knapsack-fptas/) page: profits $56, 22, 12, 45, 58, 53$, weights $2, 7, 3, 8, 9, 6$, capacity 15, with $\mathrm{LB} = P = 58$ and $n = 6$. The exact profit-indexed table has $\sum_j p_j + 1 = 247$ columns, and the optimum is 131.

| $\varepsilon$ | $K = \varepsilon P / n$ | rounded profits | columns $Q + 1$ | profit found |
|---|---|---|---|---|
| 1 | 9.67 | 5, 2, 1, 4, 6, 5 | 24 | 126 |
| 1/2 | 4.83 | 11, 4, 2, 9, 12, 10 | 49 | 126 |
| 1/4 | 2.42 | 23, 9, 4, 18, 24, 21 | 100 | 131 |
| 1/10 | 0.97 | 57, 22, 12, 46, 60, 54 | 252 | 131 |

A smaller $\varepsilon$ gives a larger table and a better answer. For $\varepsilon = 1/10$ the scale $K$ is below 1, so the "rounded" profits are larger than the true ones and the table is larger than the exact table. Line L3 runs the exact algorithm in that case.

## Classic examples

- **Knapsack.** The [knapsack FPTAS](/knapsack-fptas/) of Ibarra and Kim rounds the profits down with $K = \varepsilon P / n$ and runs the [profit-indexed dynamic program](/profit-indexed-dynamic-programming/). The same method gives an FPTAS for [subset sum](/subset-sum-fptas/), [bounded](/bounded-knapsack/) and [unbounded knapsack](/unbounded-knapsack/).
- **Restricted shortest path.** For the [constrained shortest path](/constrained-shortest-path/) problem, round the costs and run a dynamic program indexed by cost that stores the least delay. Hassin (1992) gave an FPTAS of this kind.
- **Scheduling with rounded sizes.** The [Hochbaum and Shmoys PTAS](/hochbaum-shmoys-makespan-ptas/) for makespan guesses a target $T$, rounds the large job sizes down to multiples of $\varepsilon^2 T$, and solves the rounded instance exactly by a dynamic program over machine configurations. This is the [dual approximation](/dual-approximation/) form: the constraint, not only the objective, is rounded.
- **Bin packing.** The [bin packing APTAS](/bin-packing-aptas/) of [Fernandez de la Vega and Lueker](/fernandez-de-la-vega-lueker-aptas/) rounds the large item sizes up into $O(1/\varepsilon^2)$ groups (linear grouping), so only a constant number of sizes remain.
- **Rounding to powers.** The [Chekuri and Khanna PTAS](/chekuri-khanna-ptas/) for multiple knapsack rounds each profit down to a power of $1 + \varepsilon$. This loses a factor $1 + \varepsilon$, not an additive term, and leaves only $O(\log_{1 + \varepsilon}(n/\varepsilon))$ distinct profits after the small ones are dropped.
- **Geometric rounding.** The [Arora PTAS for Euclidean TSP](/arora-euclidean-tsp-ptas/) first moves each point to the nearest point of a grid of spacing about $\varepsilon L / n$, where $L$ is the side of the bounding box.

## Variations

- **Additive rounding.** Round to multiples of $K$, as in the template. The error of one number is less than $K$, and the errors add. This is right when the objective is a sum of at most $n$ numbers.
- **Geometric rounding.** Round each number down to a power of $1 + \varepsilon$. The relative error of each number is less than $1 + \varepsilon$, so the error of a sum is also less than $1 + \varepsilon$. The number of distinct values is $\log_{1 + \varepsilon}(a_{\max} / a_{\min}) + 1$, which is small when the ratio $a_{\max}/a_{\min}$ is bounded, for example after the small numbers are dropped.
- **Large and small items.** Round only the large numbers, and treat the small ones by a greedy rule at the end. A small number is at most $\varepsilon \cdot \mathrm{LB}$, so a greedy step loses at most one small number, or a fraction $\varepsilon$ of the optimum.
- **Grouping.** Sort the sizes and round each group of $g$ consecutive sizes up to the largest size of the group. This leaves $n / g$ distinct sizes, and the loss is bounded by a shift argument, not by a bound on each number.
- **Randomized rounding.** When the rounding is of a fractional solution of a linear program, not of the input numbers, the technique is a different one: see [randomized rounding](/randomized-rounding/).

## Pitfalls

- **Rounding the constraints by mistake.** If the weights of a knapsack are rounded down, a set can fit the rounded capacity and not the true one. Round only the objective, or prove a repair step.
- **A bad lower bound.** The bound $\varepsilon \, \mathrm{LB} \le \varepsilon \, \mathrm{OPT}$ needs $\mathrm{LB} \le \mathrm{OPT}$. For knapsack, the largest profit over all items is not a lower bound when that item does not fit; use the largest profit of an item that fits alone.
- **The wrong number of terms.** The divisor in $K = \varepsilon \, \mathrm{LB} / n$ is the largest number of terms in a solution. If a solution can use an item many times, as in unbounded knapsack, the count of terms is not $n$, and $K$ must use a bound on the count.
- **K below 1.** For a small $\varepsilon$ and small numbers, $K < 1$, and the rounded numbers are larger than the true ones. Run the exact algorithm with the true numbers in that case.
- **Reporting the rounded value.** The value $K a'(S)$ is only a lower bound on $a(S)$. Compute the value of $S$ with the true numbers.
- **Strongly NP-hard problems.** If the problem is [strongly NP-hard](/strong-np-hardness/), no pseudo-polynomial algorithm exists unless P = NP, so this method cannot give an FPTAS. The [Garey and Johnson theorem](/no-fptas-for-strongly-np-hard-problems/) makes this exact.

## Exercises

1. Apply the template to the minimum knapsack problem: choose items of least total weight whose profits sum to at least $D$. Here the weights are the objective. Give the lower bound you use and the time of the scheme.
2. Show that the template with $\mathrm{LB} = P$ (the largest profit of an item that fits) and the profit-indexed table gives time $O(n^3 / \varepsilon)$, and with the greedy bound $L \le \mathrm{OPT} \le 2L$ gives $O(n^2 / \varepsilon)$.
3. Prove that rounding each profit down to a power of $1 + \varepsilon$ loses at most a factor $1 + \varepsilon$ in the value of each solution. After the profits below $\varepsilon P / n$ are removed, how many distinct rounded profits remain?
4. Use the template to give an FPTAS for makespan minimization on 2 identical machines. *Hint:* the exact algorithm is subset sum on the job sizes with target $\lfloor \sum_j p_j / 2 \rfloor$.

## References
