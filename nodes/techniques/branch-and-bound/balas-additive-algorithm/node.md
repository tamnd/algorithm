---
tag: MXCW04
kind: algorithm
slug: balas-additive-algorithm
name: Balas additive algorithm
aliases:
- Balas implicit enumeration
- additive algorithm for 0-1 programming
area: techniques/branch-and-bound
level: advanced
summary: Implicit enumeration for 0-1 integer programs using additive bounds and dominance tests, without LP.
solves: [binary-integer-programming]
model: word-ram
complexity:
  vars: {n: the number of variables, m: the number of constraints}
  time: {worst: O(2^n m n)}
  space: {extra: O(n (n + m))}
properties: {deterministic: true, recursive: false}
prereqs: [binary-integer-programming, depth-first-branch-and-bound, fathoming-rule]
see_also: [land-doig-algorithm, depth-first-branch-and-bound, fathoming-rule, branching-rule, incumbent-solution, set-cover, knapsack-branch-and-bound, generic-backtracking-algorithm]
sources:
  - paper: doi:10.1287/opre.13.4.517
    title: Egon Balas, An additive algorithm for solving linear programs with zero-one variables, Operations Research 13(4), 1965
    locator: pp. 517 to 546
  - paper: doi:10.1137/1009031
    title: A. M. Geoffrion, Integer programming by implicit enumeration and Balas' method, SIAM Review 9(2), 1967
    locator: pp. 178 to 190
  - paper: doi:10.1287/opre.16.4.741
    title: Fred Glover, Surrogate constraints, Operations Research 16(4), 1968
    locator: pp. 741 to 749
---

The Balas additive algorithm solves 0-1 linear programs by a depth-first search over partial assignments of the variables. It needs no linear program: at each node it checks whether setting all free variables to 0 is feasible, and it uses simple tests on the constraint rows to show that no completion can be feasible or better than the [incumbent](/incumbent-solution/). The tests use only additions, subtractions and comparisons, which gives the method its name. Balas published it in 1965, and Geoffrion (1967) recast it as *implicit enumeration*: every 0-1 vector is examined, most of them only implicitly.

## In plain words

You must choose some items from a list, each with a cost, so that a set of rules holds, and you want the cheapest choice. Costs are never negative, so choosing nothing is the cheapest choice of all, if it obeys the rules.

The search decides items one at a time. After each decision it asks: if I choose nothing more, do the rules hold? If yes, that is the best way to finish this branch. If no, it looks at the broken rules. If even the most helpful remaining items cannot repair a broken rule, or each helpful item is too expensive, the branch is dropped. Otherwise it picks the item that repairs the most, tries "choose it" first and "do not choose it" second.

## The problem

Minimize $c^\top x$ subject to $A x \le b$ and $x \in \{0, 1\}^n$, where $A$ is an $m \times n$ matrix and $c \ge 0$. Every 0-1 linear program can be put in this form: an equation is two inequalities, a row with $\ge$ is multiplied by $-1$, and a variable with $c_j < 0$ is replaced by $x'_j = 1 - x_j$. Balas states the problem with slack variables, as $A x + y = b$ with $y \ge 0$.

## The algorithm

A node is a tuple $(O, v, s, F)$: the set $O$ of variables fixed to 1, their cost $v = \sum_{j \in O} c_j$, the slacks $s = b - \sum_{j \in O} A_j$, where $A_j$ is column $j$ of $A$, and the set $F$ of free variables. The other variables are fixed to 0. The *zero completion* of the node sets every free variable to 0; it is feasible exactly when $s \ge 0$, and it is the cheapest completion because $c \ge 0$.

```pseudo id=main
BALAS(c, A, b)
L1  z ← ∞; best ← NIL; PUSH(Q, (∅, 0, b, {1, …, n}))
L2  while Q is not empty do
L3      (O, v, s, F) ← POP(Q)
L4      if s ≥ 0 then                                  ▷ the zero completion is feasible
L5          if v < z then z ← v; best ← O
L6          continue
L7      T ← {j ∈ F : v + c_j < z and a_ij < 0 for some i with s_i < 0}   ▷ helpful variables
L8      if T = ∅ or s_i − Σ_{j ∈ T} min(0, a_ij) < 0 for some i with s_i < 0 then continue
L9      choose j ∈ T that maximizes Σ_i min(0, s_i − a_ij)
L10     PUSH(Q, (O, v, s, F ∖ {j}))                     ▷ x_j = 0, taken second
L11     PUSH(Q, (O ∪ {j}, v + c_j, s − A_j, F ∖ {j}))    ▷ x_j = 1, taken first
L12 return (z, best)
```

Line L7 keeps the free variables that can still help. A variable is useless at this node if setting it to 1 makes the cost at least $z$, or if it does not lower the left side of any violated row. Line L8 fathoms the node when no helpful variable is left, or when a violated row stays violated even if every helpful variable with a negative coefficient in it is set to 1. Line L9 is Balas's choice: the sum is the total violation that is left after $x_j$ is set to 1, and the variable with the least total violation is taken. Ties go to the smallest index.

## Example

Minimize $3 x_1 + 5 x_2 + 2 x_3 + 6 x_4 + 3 x_5$ subject to

$$\begin{aligned} -5 x_1 + x_2 + x_3 - 4 x_4 - 4 x_5 &\le -1, \\ -3 x_1 + 2 x_3 + 4 x_4 + 2 x_5 &\le -1, \\ x_1 - 2 x_2 - 2 x_3 + 5 x_5 &\le 0, \end{aligned}$$

with $x \in \{0, 1\}^5$.

1. **Root.** $s = (-1, -1, 0)$, so rows 1 and 2 are violated. The helpful variables are $x_1$, $x_4$ and $x_5$. The test of line L8 passes: row 1 can reach $-1 + 5 + 4 + 4 = 12$ and row 2 can reach $-1 + 3 = 2$. The measures are $-1$ for $x_1$ (slacks $(4, 2, -1)$), $-5$ for $x_4$ and $-8$ for $x_5$, so the search branches on $x_1$.
2. **$x_1 = 1$.** $v = 3$, $s = (4, 2, -1)$, and row 3 is violated. The helpful variables are $x_2$ and $x_3$, both with measure 0; the tie goes to $x_2$.
3. **$x_1 = x_2 = 1$.** $v = 8$, $s = (3, 2, 1) \ge 0$. The zero completion is feasible: $z = 8$.
4. **$x_1 = 1, x_2 = 0$.** Row 3 is still violated. Only $x_3$ is helpful, since $3 + 2 < 8$. Branch on $x_3$.
5. **$x_1 = x_3 = 1$.** $v = 5$, $s = (3, 0, 1) \ge 0$: $z = 5$.
6. **$x_1 = 1, x_2 = x_3 = 0$.** Row 3 is violated, and $x_4$ and $x_5$ have no negative coefficient in it. No helpful variable: fathomed.
7. **$x_1 = 0$.** $s = (-1, -1, 0)$. With $z = 5$, the variables $x_2$ and $x_4$ cost too much, and $x_3$ does not help rows 1 or 2. Only $x_5$ is helpful, and its coefficient in row 2 is $+2$, so row 2 stays at $-1 < 0$: fathomed.

The optimum is $x = (1, 0, 1, 0, 0)$ with cost 5, after 7 nodes out of the 63 nodes of the full tree on 5 variables.

## Correctness

Every node stands for the 0-1 vectors that agree with its fixed variables. The two children of line L10 and line L11 split these vectors by the value of $x_j$, so they cover the parent. At line L4, the zero completion costs $v$ and every other completion costs at least $v$, as $c \ge 0$, so the node needs no further search. At line L8, let $x$ be a feasible completion with cost below $z$. Every free variable that $x$ sets to 1 has $v + c_j < z$. For a violated row $i$, the left side must drop by at least $-s_i$, and only variables with $a_{ij} < 0$ lower it; these are helpful, so they are in $T$, and their total effect is at most $-\sum_{j \in T} \min(0, a_{ij})$. If this is less than $-s_i$, or if $T$ is empty, no such $x$ exists. The search is finite because each branch removes one variable from $F$. So the search ends with an optimal vector, or with $z = \infty$ when there is none. The [proof](proofs/correctness.md) gives the details.

## Complexity

The tree has at most $2^{n+1} - 1$ nodes, and each node costs $O(m n)$ for lines L7 to L11, so the time is $O(2^n m n)$. The stack of a depth-first search with two children per node holds at most $n + 1$ nodes, each with $O(n + m)$ numbers, so the extra space is $O(n (n + m))$.

The tests are weak on some easy problems. For $2 x_1 + \cdots + 2 x_n = n$ with $n$ odd, written as two inequalities and with all costs 1, there is no solution, but the search makes 11, 39, 139, 503, 1847 and 6863 nodes for $n = 3, 5, \ldots, 13$: the tests look at one row at a time, and each row alone can still be repaired.

## Properties

- **Exact.** It returns an optimal 0-1 vector, or reports that there is none.
- **No linear programs.** All tests are sums and comparisons over the rows, so a node costs $O(m n)$ and there are no rounding errors with integer data.
- **Depth-first.** The memory is linear in the size of the problem, and the first feasible vector is found early.
- **Monotone cost.** Costs only grow along a path, so a variable that is too expensive at a node stays too expensive below it.

## Variants and improvements

- **Bookkeeping.** Geoffrion (1967) presented the method as implicit enumeration, with a short list of the fixed variables as the only record of the search, which is enough to make sure that no part of the tree is searched twice.
- **Surrogate constraints.** A nonnegative combination of the rows is again a valid row. Glover (1968) proposed such surrogate constraints, which give stronger infeasibility tests than single rows, such as for the parity example above.
- **LP bounds.** With an LP relaxation at each node, the search becomes LP-based branch and bound, as in the [Land-Doig algorithm](/land-doig-algorithm/); a node costs more, but the tree is often much smaller.
- **Ordering.** The variables can be sorted by cost first, so that cheap variables are tried first and $z$ falls quickly.

## When to use it

Use it for small or sparse 0-1 programs, such as [set cover](/set-cover/) instances, when an LP solver is not available or when exact integer arithmetic matters. It is also a clear example of [depth-first branch and bound](/depth-first-branch-and-bound/) with cheap [fathoming rules](/fathoming-rule/). For large programs, LP-based branch and bound with cuts is much stronger.

## Pitfalls

- **Negative costs.** The zero completion is the cheapest completion only when $c \ge 0$. Complement the variables with $c_j < 0$ first.
- **Restricting the free set too far.** A variable that is not helpful at a node can become helpful below it, when another row becomes violated. Only the test at line L8 may use $T$; the children keep all of $F$ except $j$.
- **Equality rows.** An equation written as two inequalities makes one of them violated after almost every step, and the single-row tests become weak, as in the parity example.

## Implementations

## History

Balas (1965) gave the additive algorithm for linear programs with zero-one variables, with a search over partial assignments and tests that use only additions and subtractions. Geoffrion (1967) described it in the general setting of implicit enumeration. Glover (1968) introduced surrogate constraints, which were used to strengthen such tests.

## References
