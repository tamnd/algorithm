---
tag: VSSWCG
kind: algorithm
slug: dinkelbach-algorithm
name: Dinkelbach's algorithm
aliases:
- Dinkelbach's method
- Dinkelbach transform iteration
area: searching/search-on-answers
level: advanced
summary: Solve a fractional optimization problem by iterating a parametric linear objective until the ratio stops decreasing.
solves: [minimum-ratio-problem]
model: query-model
complexity:
  vars: {U: "a bound on |N| and D for integer data", T: the time of one call of the parametric problem}
  time: {worst: O(T log U), best: O(T)}
  space: {extra: Θ(1)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 1967
  people: [Werner Dinkelbach]
  note: Dinkelbach published the method for nonlinear fractional programs in Management Science in 1967.
prereqs: [fractional-programming, minimum-ratio-problem, newton-raphson-method]
see_also: [fractional-programming, minimum-ratio-problem, parametric-search, binary-search-on-real-numbers, minimum-mean-cycle-problem, maximum-density-segment, lagrangian-relaxation]
sources:
  - paper: doi:10.1287/mnsc.13.7.492
    title: "Werner Dinkelbach, On nonlinear fractional programming, Management Science 13(7) (1967), 492-498"
  - paper: doi:10.1287/mnsc.22.8.868
    title: "Siegfried Schaible, Fractional Programming. II, On Dinkelbach's Algorithm, Management Science 22(8) (1976), 868-873"
    note: superlinear convergence of the iteration
  - paper: doi:10.1109/SFCS.1992.267785
    title: "Tomasz Radzik, Newton's method for fractional combinatorial optimization, Proceedings of the 33rd IEEE Symposium on Foundations of Computer Science (1992), 659-669"
    note: a strongly polynomial bound on the number of iterations for linear ratios over subsets
---

Dinkelbach's algorithm minimizes a ratio $N(x)/D(x)$, with $D > 0$, by solving a sequence of problems with the linear objective $N(x) - \lambda D(x)$: it sets $\lambda$ to the ratio of the current solution, finds the solution that minimizes $N - \lambda D$, and repeats until the minimum is $0$. Each step is a Newton step for the root of the concave decreasing function $F(\lambda) = \min_x (N(x) - \lambda D(x))$, so the ratios decrease strictly and, on a finite set, reach the optimum after finitely many steps. For integer data bounded by $U$ it needs $O(\log U)$ steps, Radzik showed a strongly polynomial number of steps for linear ratio problems, and in practice it takes far fewer steps than a [binary search on real numbers](/binary-search-on-real-numbers/). It is the standard method of [fractional programming](/fractional-programming/).

## In plain words

You want the choice with the lowest cost per hour. Start with any choice, and compute its cost per hour; call that the price. Now charge every choice that price for each of its hours, and look for the choice that does best under the charge. If even the best one only breaks even, no choice beats the price, so your current choice is the best. Otherwise the best one under the charge has a lower cost per hour than the price. Make it your current choice, compute its cost per hour as the new price, and repeat.

Each round the price goes down, and no choice is used twice, so the rounds end. In practice only a handful of rounds are needed.

## The problem

The input is a set $X$ of feasible solutions, given implicitly, two functions $N, D : X \to \mathbb{R}$ with $D(x) > 0$ for all $x \in X$, and an oracle MIN-PARAM$(\lambda)$ that returns a solution minimizing $N(x) - \lambda D(x)$ over $X$. The output is a solution $x^*$ that minimizes $N(x)/D(x)$, and the optimal ratio $\lambda^*$. The cost is counted in calls of the oracle, as in the [query model](/query-model/). The main case is the [minimum ratio problem](/minimum-ratio-problem/), where $X$ is a family of subsets and $N$, $D$ are sums of weights, and the oracle is an ordinary combinatorial algorithm with the weights $c_e - \lambda t_e$.

The method rests on Dinkelbach's lemma, proved on the page [fractional programming](/fractional-programming/): with $F(\lambda) = \min_{x} (N(x) - \lambda D(x))$, $F(\lambda) \ge 0$ exactly when $\lambda \le \lambda^*$, and $F(\lambda^*) = 0$. The function $F$ is concave and strictly decreasing.

## The algorithm

```pseudo id=main
DINKELBACH(MIN-PARAM, N, D, x0)            ▷ x0 is any feasible solution
L1  x ← x0
L2  loop
L3      λ ← N(x) / D(x)                    ▷ the ratio of the current solution
L4      y ← MIN-PARAM(λ)                   ▷ y minimizes N − λD; F(λ) = N(y) − λD(y)
L5      if N(y) − λ·D(y) ≥ 0 then return (x, λ)   ▷ F(λ) = 0, so λ = λ*
L6      x ← y                              ▷ F(λ) < 0, so N(y)/D(y) < λ
```

**Why it is Newton's method.** At $\lambda_k$ the minimizer $y$ gives the affine function $\ell(\lambda) = N(y) - \lambda D(y)$, which touches $F$ at $\lambda_k$ and lies above it elsewhere, because $F$ is the minimum of such functions. Its root is $\lambda = N(y)/D(y)$, the next value of line L3. So each step replaces $F$ by its tangent line and jumps to the root of the tangent.

## Example

Choose $k = 2$ of the five items $A = (8, 1)$, $B = (4, 2)$, $C = (9, 4)$, $D = (2, 2)$, $E = (9, 5)$, given as (cost, time), to minimize total cost over total time. The oracle sorts the items by $c_i - \lambda t_i$ and takes the two smallest. Start with $\{A, B\}$.

| round | x | λ = N(x)/D(x) | the two smallest $c_i - \lambda t_i$ | y | F(λ) |
|---|---|---|---|---|---|
| 0 | {A, B} | 12/3 = 4 | E: −11, C: −7 | {C, E} | −18 |
| 1 | {C, E} | 18/9 = 2 | D: −2, E: −1 | {D, E} | −3 |
| 2 | {D, E} | 11/7 ≈ 1.571 | D: −8/7, B: 6/7 | {B, D} | −2/7 |
| 3 | {B, D} | 6/4 = 1.5 | D: −1, B: 1 | {B, D} | 0 |

It returns $\{B, D\}$ with ratio $3/2$ after 4 calls of the oracle. The 10 pairs have ratios between $1.5$ and $4$, and $\{B, D\}$ is the best. The denominators of the solutions found from round 1 on are $9, 7, 4$, non-increasing, and $|F|$ drops from $18$ to $3$ to $2/7$ to $0$.

## Correctness

In each round $F(\lambda) \le N(x) - \lambda D(x) = 0$, since the current $x$ is a candidate. If line L5 finds $F(\lambda) \ge 0$, then $F(\lambda) = 0$, so $\lambda \le \lambda^*$ by the lemma, and $\lambda \ge \lambda^*$ because $\lambda$ is the ratio of a feasible $x$; so $x$ is optimal. Otherwise $N(y) - \lambda D(y) < 0$ gives $N(y)/D(y) < \lambda$: the ratio strictly decreases, no solution repeats, and on a finite $X$ the loop ends after at most $|X|$ rounds. The full proof, with the bound for integer data, is below.

## Complexity

- **Finite termination.** At most $|X|$ rounds, because the ratios strictly decrease.
- **Monotone denominators.** From round 1 on, $D(x_k)$ does not increase. *Proof.* If $y$ minimizes $N - \mu D$ and $z$ minimizes $N - \nu D$ with $\mu < \nu$, adding the two minimality inequalities gives $(\nu - \mu)D(y) \le (\nu - \mu)D(z)$; the parameters $\lambda_k$ decrease.
- **Halving.** With $F_k = F(\lambda_k)$ and $D_k = D(x_k)$, each round $k \ge 1$ satisfies $|F_k|/|F_{k-1}| + D_{k+1}/D_k \le 1$, so either $|F|$ or $D$ at least halves.
- **Integer data.** If $|N| \le U$ and $1 \le D \le U$ are integers, then $1/U \le |F_k| \le 2U^2$ while the algorithm runs, so $|F|$ halves at most $1 + 3\lg U$ times and $D$ at most $\lg U$ times: at most $4\lg U + 3$ rounds, that is $O(T \log U)$ time for an oracle of time $T$.
- **Strongly polynomial bound.** For linear ratios over any family of subsets of an $m$-element ground set, Radzik proved a number of rounds bounded by a polynomial in $m$ alone.
- **Local speed.** Schaible showed that the convergence is superlinear, and often locally quadratic, as expected of Newton's method.

## Properties

- **Exact.** On a finite set it returns the exact optimum, with no tolerance, if the arithmetic is exact. The implementation uses rational numbers.
- **Needs an exact minimizer.** Line L4 must return a true minimizer of $N - \lambda D$; the halving bound uses this. With a solution that is only better than $x$, the ratio still decreases, but the speed of Newton's method is lost.
- **Any sign of the weights.** The parametric weights $c_e - \lambda t_e$ can be negative, so the oracle must handle weights of any sign.
- **Anytime.** Each $\lambda_k$ is the ratio of a feasible solution, so stopping early gives a feasible solution and an upper bound on $\lambda^*$.

## Variants and improvements

- **Bisection instead of Newton.** Search $\lambda$ by the sign of $F$ on an interval: each step halves the interval, and for integer data an interval of width below $1/T^2$, with $T$ the largest denominator, identifies $\lambda^*$. It needs only the sign of $F$, not a minimizer, but uses more calls than Newton in practice.
- **Maximization.** Maximize $N/D$ by minimizing $-N/D$, or by the same loop with "max" and the opposite stopping test.
- **Generalized fractional programs.** For $\min_x \max_i N_i(x)/D_i(x)$, the same iteration with $F(\lambda) = \min_x \max_i (N_i(x) - \lambda D_i(x))$ converges, with a slower rate in general.
- **Continuous problems.** For $N$ convex and $D$ concave and positive on a convex set, each parametric problem is convex, and the loop solves a sequence of convex programs; this is common in the design of energy-efficient communication systems.
- **Parametric search.** For a combinatorial oracle with comparisons that are linear in $\lambda$, [parametric search](/parametric-search/) gives strongly polynomial bounds with a different method, by simulating the oracle at $\lambda^*$.

## When to use it

Use Dinkelbach's algorithm for a ratio objective when the problem with a linear objective $N - \lambda D$ is easy and its solver accepts weights of any sign: ratio spanning trees, ratio assignment, the densest subgraph with a minimum cut, ratio problems over matroids, or continuous ratios of convex over concave functions. It usually needs fewer oracle calls than a bisection, and returns the exact optimum. If the oracle can only decide the sign of $F$, use bisection. For the minimum mean cycle, Karp's direct algorithm is simpler.

## Pitfalls

- **A non-optimal oracle.** A heuristic in line L4 can stop at $F(\lambda) \ge 0$ for its own solution while a better one exists; the result is then not optimal.
- **A floating-point stopping test.** With floating point, $N(y) - \lambda D(y)$ near the optimum is a small number of either sign, and "$\ge 0$" can fail forever. Use exact rationals for integer data, or stop when $\lambda$ does not decrease by more than a tolerance.
- **A zero denominator.** The lemma needs $D > 0$ on all of $X$; an empty set, a cycle of total time $0$, or a segment of length $0$ breaks it. Exclude them from $X$ or add a small positive time.
- **Ratio paths.** For $s$-$t$ paths with parametric weights, the oracle would need a shortest simple path in a graph with negative cycles, which is NP-hard. The method is then not efficient, though it remains correct with an exact oracle.

## Implementations

## History

Werner Dinkelbach introduced the method for nonlinear fractional programs in 1967, building on the parametric view of linear fractional programs. Siegfried Schaible analysed its convergence in 1976 and showed it to be superlinear. In combinatorial optimization the method is also called the Newton method for fractional problems, and Tomasz Radzik proved in 1992 that the number of its iterations is strongly polynomial for linear ratios over subsets.

## References
