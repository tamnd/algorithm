---
tag: R0G4WY
kind: technique
slug: trimming-technique
name: Trimming technique
aliases:
- list trimming
- trimming
- trimming the state space
- state space trimming
area: approximation/approximation-schemes
level: core
summary: Remove from a sorted list of partial solutions any values that lie within a factor (1+δ) of a kept value, bounding the list length.
prereqs: [approximation-ratio, tabulation, optimal-substructure]
see_also: [subset-sum-fptas, knapsack-fptas, rounding-and-scaling, profit-indexed-dynamic-programming, fptas, approximate-pareto-set, makespan-minimization, no-fptas-for-strongly-np-hard-problems]
sources:
  - book: isbn:9780262033848
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, third edition, MIT Press, 2009
    locator: Section 35.5 (The subset-sum problem), the procedure TRIM and Theorem 35.8
  - paper: doi:10.1145/321906.321909
    title: Oscar H. Ibarra and Chul E. Kim, Fast approximation algorithms for the knapsack and sum of subset problems, Journal of the ACM 22(4), 1975
    locator: pages 463 to 468
  - title: Gerhard J. Woeginger, When does a dynamic programming formulation guarantee the existence of a fully polynomial time approximation scheme (FPTAS)?, INFORMS Journal on Computing 12(1), 2000
    locator: the framework of DP-benevolent problems and the trimming of the state space
  - title: Sartaj K. Sahni, Algorithms for scheduling independent tasks, Journal of the ACM 23(1), 1976
    locator: the approximation schemes for scheduling on a fixed number of machines
  - book: isbn:9783540402862
    title: Hans Kellerer, Ulrich Pferschy and David Pisinger, Knapsack Problems, Springer, 2004
    locator: the chapters on approximation schemes for the subset sum and knapsack problems
---

Trimming is a way to turn an exact dynamic program over a list of partial solutions into an approximation scheme. The exact list can grow to an exponential length. After each stage, the list is sorted by the objective value, and a value is removed when a kept value is smaller by at most a factor $1 + \delta$. Each removed value then has a stand-in that is almost as good. The kept values grow by more than a factor $1 + \delta$ from one to the next, so a list of values in $[1, U]$ has at most $\log_{1 + \delta} U + 2$ entries. With $\delta = \varepsilon / (2n)$ over $n$ stages, the total loss is a factor of at most $1 + \varepsilon$, and the method gives an [FPTAS](/fptas/). The standard example is the [subset sum FPTAS](/subset-sum-fptas/).

## In plain words

Many exact methods keep a list of all partial results and extend each one at every step. The list can double at each step. Trimming keeps the list short by throwing away results that are nearly the same as a result that is kept.

Sort the list, keep the first value, and go up the list. Keep a value only if it is larger than the last kept value by more than a small factor, such as 1 percent. Each value that you throw away has a kept value that is at most 1 percent smaller. The kept values grow by 1 percent each time, so only a few hundred of them fit below a large bound. The small losses add up over the steps, so the factor must be smaller when there are more steps.

## When it applies

Look for these signals:

- An exact algorithm works in $n$ stages and keeps a list of states. Each state is a partial solution, described by a value of the objective and maybe some resource (weight, load, time).
- The final answer is the best state in the last list, and the list can grow to an exponential or pseudo-polynomial length.
- The objective values are positive numbers in a range $[\ell, U]$ with $\log(U / \ell)$ polynomial in the input size (or zero, which is kept as a special case).
- **The loss does not grow when a state is extended.** If $z \ge y / c$ for some $c \ge 1$, then each extension of $y$ has a matching extension of $z$ with value at least $1/c$ of it, and with the same or a better resource. An extension that adds a non-negative amount has this property: $z + x \ge (y + x) / c$.
- Among states with almost the same value, one state can be kept for all of them: the one with the best resource.

The method fails when an extension can subtract, for example an objective of the form $|t - \text{sum}|$, because then a small relative error in $z$ can become a large relative error later.

## The template

The template is for a maximization problem. The holes are the extension step, the resource that decides which state of a group is kept, and the feasibility test.

```pseudo id=main
TRIMMED-DP(n stages, δ)                                 ▷ δ = ε/(2n) for a (1 + ε) bound
L1  L ← ⟨the initial state⟩
L2  for i ← 1 to n do
L3      L ← all extensions of the states of L by stage i      ▷ hole: the extension step
L4      remove from L the states that are infeasible           ▷ hole: the feasibility test
L5      sort L by value; among equal values keep the best resource
L6      K ← ⟨the first state of L⟩; last ← its value
L7      for each next state s of L, in order of value do
L8          if value(s) > last · (1 + δ) then append s to K; last ← value(s)
L9          else if s has a better resource than the last state of K then replace the last state of K by s   ▷ hole: the resource
L10     L ← K
L11 return the state of L with the largest value
```

For the subset sum problem, the state is only its sum, the resource is not needed, and line L9 never fires. For knapsack, the state is a pair (profit, weight), and line L9 keeps the lightest pair of each group.

Line L8 opens a new group when a value is more than the factor $1 + \delta$ above the value $\mathit{last}$ that opened the current group. Line L9 does not change $\mathit{last}$. So each group holds the states with values in $[o, (1 + \delta) o]$, where $o$ is the value that opened it, and the kept state of the group is the one with the best resource.

**Lemma 1 (one trim).** After lines L6 to L9, each state $s$ of the sorted list has a kept state $z$ with $\mathrm{value}(z) \ge \mathrm{value}(s) / (1 + \delta)$ and a resource at least as good as that of $s$.

*Proof.* Let $o$ be the value that opened the group of $s$, so $o \le \mathrm{value}(s) \le (1 + \delta) o$. The kept state $z$ of the group has the best resource in the group, and its value is at least $o \ge \mathrm{value}(s) / (1 + \delta)$. $\square$

**Lemma 2 (length).** If the positive values lie in $[\ell, U]$, then the kept list has at most $\log_{1 + \delta}(U / \ell) + 2$ states.

*Proof.* The values that open the groups grow by more than the factor $1 + \delta$, so $k$ positive group values satisfy $U \ge \ell (1 + \delta)^{k-1}$. One more state can have value 0. $\square$

**Lemma 3 (n stages).** If the extensions keep the loss as in the last signal above, then after stage $i$ each feasible partial solution $y$ has a kept state $z$ with $\mathrm{value}(z) \ge \mathrm{value}(y) / (1 + \delta)^i$. For $\delta = \varepsilon / (2n)$ and $0 < \varepsilon \le 1$, $(1 + \delta)^n \le e^{\varepsilon / 2} \le 1 + \varepsilon$.

*Proof.* By induction on $i$: the stand-in of the parent of $y$ has an extension within the factor $(1 + \delta)^{i-1}$ of $y$, and with a resource at least as good, so it is feasible, and the trim loses one more factor $1 + \delta$. For the last claim, $1 + u \le e^u$, and $e^u \le 1 + u + u^2$ for $0 \le u \le 1$. With $u = \varepsilon / 2$, $1 + \varepsilon / 2 + \varepsilon^2 / 4 < 1 + \varepsilon$. $\square$

With $U / \ell \le 2^{\mathrm{poly}}$ and $\delta = \varepsilon / (2n)$, Lemma 2 gives lists of length $O(n \log(U/\ell) / \varepsilon)$, because $\ln(1 + \delta) \ge \delta / (1 + \delta)$. The whole run is then polynomial in the input size and in $1 / \varepsilon$.

### A worked trim

Take the sorted list $\langle 10, 11, 12, 15, 20, 21, 22, 23, 29 \rangle$ and $\delta = 1/10$. The value 10 is kept. The value 11 is not above $1.1 \cdot 10 = 11$, so it is removed. The value 12 is kept. Then 15 (above 13.2) and 20 (above 16.5) are kept. The values 21 and 22 are not above $1.1 \cdot 20 = 22$, so they are removed. The value 23 is kept, and 29 (above 25.3) is kept. The result is $\langle 10, 12, 15, 20, 23, 29 \rangle$. Each removed value has a kept value at most 10 percent below it: 11 has 10, and 21 and 22 have 20.

## Classic examples

- **Subset sum.** The [subset sum FPTAS](/subset-sum-fptas/) (APPROX-SUBSET-SUM of Cormen et al.) trims the sorted list of reachable sums with $\delta = \varepsilon / (2n)$. The lists have $O(n \log t / \varepsilon)$ entries, and the time is $O(n^2 \log t / \varepsilon)$.
- **0/1 knapsack.** The states are pairs (profit, weight). Sort by profit and keep the lightest pair in each group. The invariant is: for each feasible set with profit $p$ and weight $w$ there is a kept pair with profit at least $p / (1 + \delta)^i$ and weight at most $w$. This gives an FPTAS with lists of $O(n \log(n P) / \varepsilon)$ pairs. The [knapsack FPTAS](/knapsack-fptas/) by scaling is the other standard route.
- **Scheduling on a fixed number of machines.** For [makespan minimization](/makespan-minimization/) on $m$ identical machines, with $m$ fixed, the state is the vector of the $m$ loads. Trim each coordinate on a geometric grid with ratio $1 + \delta$, and keep one state for each cell of the grid. There are $O((n \log(\sum p_j) / \varepsilon)^m)$ cells, which is polynomial for fixed $m$. Sahni (1976) gave schemes of this kind. For $m$ in the input the problem is [strongly NP-hard](/strong-np-hardness/), and [no FPTAS exists](/no-fptas-for-strongly-np-hard-problems/) unless P = NP.
- **Approximate Pareto sets.** For two or more objectives, a geometric grid in each objective keeps one point for each cell, and the result is an [approximate Pareto set](/approximate-pareto-set/) of polynomial size.

## Variations

- **The grid form.** In place of a comparison with the last kept value, put each value $v > 0$ in the cell $\lfloor \log_{1 + \delta} v \rfloor$ and keep one state for each cell. The two values in a cell differ by less than the factor $1 + \delta$, and the number of cells is the same as in Lemma 2. This form is easier to use in several dimensions, because it needs no sorting.
- **The (1 − ε) form.** With $\delta = \varepsilon / n$, the loss after $n$ stages is $(1 + \delta)^{-n} \ge (1 - \delta)^n \ge 1 - n\delta = 1 - \varepsilon$, by Bernoulli's inequality. This gives $\mathrm{ALG} \ge (1 - \varepsilon) \mathrm{OPT}$ with lists half as long as with $\delta = \varepsilon / (2n)$.
- **Minimization.** For a minimization problem, keep the smallest value of each group. The stand-in $z$ of $y$ has $y \le z \le (1 + \delta) y$, and the bound becomes $\mathrm{ALG} \le (1 + \delta)^n \mathrm{OPT} \le (1 + \varepsilon) \mathrm{OPT}$.
- **Trimming in the resource.** If the resource is a number that can be large, it can also be trimmed, but only when a small loss in the resource is allowed, as in a problem with a soft budget. If the budget is hard, trim only the objective.
- **A general theorem.** Woeginger (2000) gave syntactic conditions on a dynamic program (the problem is DP-benevolent) under which trimming the state space always gives an FPTAS. Many scheduling and knapsack problems meet these conditions.

## Pitfalls

- **Comparing with the previous entry.** The test of line L8 is against the last kept value, not against the value just before $s$ in the list. With the previous value, a long run of close values can all be removed, and the loss is much larger than $1 + \delta$.
- **δ that does not depend on n.** The losses multiply over the stages. A fixed $\delta = \varepsilon$ gives only the bound $(1 + \varepsilon)^n$.
- **Trimming the constraint.** If two states with close values but very different weights are merged, and the heavier one is kept, a later item may not fit. Keep the state with the best resource (line L9), or the invariant fails.
- **A zero or negative value.** The geometric grid has no cell for 0, and the ratio $z / y$ means nothing for negative values. Keep 0 as its own state, and use trimming only for objectives that are positive.
- **Subtraction in the objective.** If an extension can lower the value, a stand-in that is a little lower can later be much lower in relative terms. Trimming does not apply to such objectives without extra work.
- **Large U.** The length bound has $\log(U / \ell)$. If the values can be as large as $2^{2^n}$, the lists are not polynomial.

## Exercises

1. Show that the TRIM of the subset sum page runs in linear time, and that the output list depends only on the set of values, not on the order in which they were generated. *Hint:* the input is sorted, and TRIM is a single pass.
2. Write the knapsack form of the template with states (profit, weight). Prove the invariant of the classic example, and bound the list length by $\log_{1 + \delta}(nP) + 2$, where $P$ is the largest profit.
3. Give an instance of subset sum on which the trimmed algorithm with $\delta = \varepsilon / (2n)$ and $\varepsilon = 1$ returns less than the optimum. *Hint:* the example on the [subset sum FPTAS](/subset-sum-fptas/) page has 5 numbers.
4. Show that trimming cannot give an FPTAS for minimizing $|t - \sum_{i \in S} x_i|$ over subsets $S$ unless P = NP. *Hint:* an FPTAS with any ratio would decide whether the optimum is 0.
5. Design a trimmed dynamic program for scheduling $n$ jobs on two identical machines to minimize the makespan, and bound its time by $O(n^3 \log^2(\sum_j p_j) / \varepsilon^2)$ or better.

## References
