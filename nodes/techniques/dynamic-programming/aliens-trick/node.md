---
tag: J6F5JB
kind: technique
slug: aliens-trick
name: Aliens trick
aliases:
- Alien's DP
- Lagrangian penalty binary search
- Lagrangian relaxation for DP
- Lagrangian relaxation of DP
- WQS binary search
area: techniques/dynamic-programming
level: research
summary: Remove a count constraint with a penalty term and binary search on the penalty, relying on concavity.
prereqs: [lagrangian-relaxation, convex-function, binary-search, monge-property]
see_also: [lagrangian-relaxation, lagrangian-duality, divide-and-conquer-optimization, convex-hull-trick, monge-property, parametric-search, knuth-optimization]
sources:
  - paper: doi:10.1007/BF02574380
    title: Alok Aggarwal, Baruch Schieber and Takeshi Tokuyama, Finding a minimum-weight k-link path in graphs with the concave Monge property and applications, Discrete and Computational Geometry 12(3), 263-280, 1994
    locator: the convexity of the k-link path weight in k for Monge weights, and the parametric search over the penalty
  - paper: doi:10.1016/0166-218X(95)00103-X
    title: Rainer E. Burkard, Bettina Klinz and Rüdiger Rudolf, Perspectives of Monge properties in optimization, Discrete Applied Mathematics 70(2), 95-161, 1996
    locator: the section on shortest paths with a fixed number of edges in Monge graphs
---

The Aliens trick solves an optimization problem with the constraint "use exactly $k$ parts" (or $k$ items, or $k$ edges) by removing the constraint and charging a penalty $\lambda$ for each part instead. For a fixed $\lambda$, the unconstrained problem is often much faster to solve, and it reports how many parts its optimum uses. If the best value $F(k)$ is a convex function of $k$, then for every $k$ there is a penalty at which $k$ parts are optimal, and a [binary search](/binary-search/) on $\lambda$ finds it. The cost drops from about $k$ times the cost of one layer to $O(\log R)$ times the cost of the unconstrained problem, where $R$ is the range of the penalty. Aggarwal, Schieber and Tokuyama used this idea in 1994 for minimum weight paths with $k$ edges in Monge graphs; it is the [Lagrangian relaxation](/lagrangian-relaxation/) of the count constraint.

## In plain words

Say you must cut a list into exactly $k$ groups as cheaply as possible. Keeping track of the number of groups makes the work $k$ times larger.

Drop the rule. Instead, charge a fee for every group. With no fee, the cheapest plan uses many small groups. With a huge fee, it uses one group. As the fee goes up, the number of groups goes down. Search for the fee at which the cheapest plan uses exactly $k$ groups. Then take its cost and subtract the fees you charged. This gives the right answer when each extra group saves less than the one before it.

## When it applies

- The problem has a count constraint: exactly $k$ parts, $k$ edges, $k$ chosen items, $k$ facilities.
- Let $F(t)$ be the best value with exactly $t$ parts. $F$ must be **convex** in $t$ for a minimum (concave for a maximum): $F(t-1) - F(t) \ge F(t) - F(t+1)$. Each extra part helps at most as much as the previous one.
- The penalized problem $g(\lambda) = \min_t \bigl( F(t) + \lambda t \bigr)$ can be solved fast without the count in the state, and its solver can report the number of parts of an optimum, with a fixed rule for ties.
- Convexity often comes from the [Monge property](/monge-property/): for partitions of a sequence with a cost $w$ that satisfies the quadrangle inequality, $F$ is convex. This is a theorem of Aggarwal, Schieber and Tokuyama.

## The template

Let $SOLVE(\lambda)$ return the pair $(g(\lambda), c(\lambda))$, where $c(\lambda)$ is the smallest number of parts among the optimal solutions of the penalized problem. The holes are the penalized solver and the range of $\lambda$. The version below is for integer values of $F$.

```pseudo id=main
ALIENS(k)
L1  lo ← −M, hi ← M                        ▷ hole: M bounds every |F(t) − F(t+1)|
L2  while lo < hi do
L3      mid ← ⌊(lo + hi) / 2⌋
L4      (v, c) ← SOLVE(mid)                 ▷ hole: the penalized problem, ties to fewer parts
L5      if c ≤ k then hi ← mid else lo ← mid + 1
L6  (v, c) ← SOLVE(lo)
L7  return v − lo · k
```

**Why it is correct.** Let $F$ be convex on $t = 1, \ldots, n$, and let $1 \le k \le n$. Define $\lambda^* = F(k) - F(k+1)$ if $k < n$, and $\lambda^* = -M$ if $k = n$.

1. *A count $t$ is optimal for $\lambda$ exactly when $F(t) - F(t+1) \le \lambda \le F(t-1) - F(t)$*, with the missing bound dropped at the ends. The function $t \mapsto F(t) + \lambda t$ is convex, so a local minimum is a global one, and the two inequalities say that $t$ is no worse than $t - 1$ and $t + 1$.
2. *At $\lambda = \lambda^*$, $k$ is optimal and $c(\lambda^*) \le k$.* The upper bound $\lambda^* \le F(k-1) - F(k)$ holds by convexity, and the lower bound holds with equality.
3. *For $\lambda < \lambda^*$, $c(\lambda) > k$.* Then $F(k+1) + \lambda(k+1) < F(k) + \lambda k$, so $k+1$ is strictly better than $k$, and by convexity strictly better than every $t \le k$. So all optimal counts exceed $k$.
4. $c(\lambda)$ does not increase with $\lambda$, by a standard exchange of the two optimality inequalities. So the predicate $c(\lambda) \le k$ is monotone, and the binary search of lines L2 to L5 returns the smallest $\lambda$ with $c(\lambda) \le k$, which is $\lambda^*$ by steps 2 and 3.
5. At $\lambda^*$, $k$ is optimal, so $g(\lambda^*) = F(k) + \lambda^* k$, and line L7 returns $F(k)$.

The answer of line L7 is right even though the solver's own optimum may use fewer than $k$ parts: at $\lambda^*$ several counts tie, and the value $g$ is the same for all of them.

**Cost.** The loop runs $\lceil \lg(2M + 1) \rceil$ times, so the time is $O(\log M)$ times the time of one call of $SOLVE$. If $SOLVE$ takes $O(n)$ or $O(n \log n)$, the whole method takes $O(n \log M)$ or $O(n \log n \log M)$, independent of $k$.

## Classic examples

### Cutting an array into exactly $k$ parts

Cut $a = (4, 1, 3, 2, 5, 1, 2)$ into exactly $k = 3$ parts, with a part of sum $s$ costing $s^2$. The best values for each count are

| $t$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| $F(t)$ | 324 | 164 | 114 | 84 | 70 | 64 | 60 |
| $F(t) - F(t+1)$ | 160 | 50 | 30 | 14 | 6 | 4 | |

The differences decrease, so $F$ is convex, as the quadrangle inequality of $(S_j - S_i)^2$ promises. The penalized problem $E(j) = \min_{i < j} \bigl( E(i) + (S_j - S_i)^2 + \lambda \bigr)$ has no count in its state; its values, with ties broken toward fewer parts, are:

| $\lambda$ | 0 | 10 | 20 | 30 | 40 | 50 | 200 |
|---|---|---|---|---|---|---|---|
| $g(\lambda)$ | 60 | 120 | 164 | 204 | 234 | 264 | 524 |
| $c(\lambda)$ | 7 | 5 | 4 | 3 | 3 | 2 | 1 |

The smallest $\lambda$ with $c(\lambda) \le 3$ is $\lambda^* = 30 = F(3) - F(4)$. At $\lambda = 30$ the counts 3 and 4 tie ($114 + 90 = 84 + 120 = 204$), and the answer is $204 - 30 \cdot 3 = 114$, which matches $F(3)$. On 500 random arrays and values of $k$, the method agrees with the full $O(k n^2)$ DP.

The penalized problem here has the form of the [convex hull trick](/convex-hull-trick/), so each call takes $O(n)$ time, and the method takes $O(n \log M)$ instead of the $O(k n \log n)$ of the [divide and conquer optimization](/divide-and-conquer-optimization/).

### Other uses

- **Minimum weight paths with $k$ edges in Monge graphs.** The original setting of Aggarwal, Schieber and Tokuyama, who give applications in computational geometry and in coding.
- **Choosing exactly $k$ items** under a structure where the best value is concave in $k$, for example the most total weight of $k$ disjoint subarrays.
- **Trees.** The best total of exactly $k$ vertex-disjoint paths in a tree, when the penalized tree DP is linear.

## Variations

- **Real penalties.** When $F$ takes real values, search $\lambda$ over the reals to a tolerance, or search over the finite set of candidate slopes. The answer must still be read with the formula of line L7 at a $\lambda$ where $k$ is optimal.
- **Ties toward more parts.** If the solver breaks ties toward the largest count, search for the largest $\lambda$ with $c(\lambda) \ge k$ instead. The two rules must not be mixed.
- **Recovering a solution with exactly $k$ parts.** The solver at $\lambda^*$ may return a solution with fewer parts. A solution with exactly $k$ parts is among the optimal ones at $\lambda^*$, but finding it needs extra work beyond the value of line L7.
- **Several constraints.** With two count constraints, the method needs a two-dimensional search on two penalties, and the convexity conditions are harder to check.
- **The general view.** This is [Lagrangian duality](/lagrangian-duality/) for one constraint. Convexity of $F$ means there is no duality gap, so the dual optimum equals the primal optimum.

## Pitfalls

- **Assuming convexity.** If $F$ is not convex, some counts are never optimal for any $\lambda$, and line L7 returns a lower bound, not $F(k)$. Prove convexity first, or check it by brute force on small inputs.
- **Inconsistent tie-breaking.** The proof needs $c(\lambda)$ to be the smallest optimal count. A solver that breaks ties in an arbitrary way can make the predicate of line L5 non-monotone, and the search can stop at a wrong $\lambda$.
- **Reading the count of the solver.** Never use $v - \lambda c$ with the solver's own count $c$; use $v - \lambda k$.
- **The range of $\lambda$.** It must include every difference $F(t) - F(t+1)$, which may be negative when more parts cost more. A range that starts at 0 fails in that case.
- **Fractional slopes.** If $F$ has integer values, all slopes are integers and an integer search is exact. If not, an integer search can miss $\lambda^*$.

## Exercises

1. Show that $c(\lambda)$ is nonincreasing in $\lambda$, using only the definition of an optimal count.
2. For the example, compute $g(30)$ by hand from the optimal partitions with 3 and with 4 parts.
3. Choose exactly $k$ nonoverlapping subarrays of an array with the largest total sum. Show that the best value is concave in $k$ and solve it with the Aliens trick in $O(n \log M)$ time.
   <details><summary>Hint</summary>Concavity follows because the problem is a min-cost flow problem in which each extra unit of flow uses a path of no smaller cost.</details>
4. Give a small example in which $F$ is not convex and the method returns a wrong value.

## References
