---
tag: 5ZHQ6D
kind: algorithm
slug: chronological-backtracking
name: Chronological backtracking
aliases:
- naive backtracking
- naive backtracking for CSP
- simple backtracking
- standard backtracking search
area: techniques/backtracking
level: intro
summary: Undoes the most recent assignment on failure, the baseline against which smarter backtracking is compared.
solves: [constraint-satisfaction-problem]
model: word-ram
complexity:
  vars: {m: the number of variables, d: the size of the largest domain}
  time: {worst: O(m d^m), best: O(m^2)}
  space: {extra: O(m)}
properties: {deterministic: true, recursive: true}
prereqs: [constraint-satisfaction-problem, generic-backtracking-algorithm]
see_also: [conflict-directed-backjumping, graph-based-backjumping, non-chronological-backtracking, forward-checking, variable-ordering-heuristics, dynamic-backtracking, dpll]
sources:
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 6, Constraint Satisfaction Problems (backtracking search and intelligent backtracking)
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing
    locator: Chapter 5 (backtracking and look-ahead) and Chapter 6 (look-back, backjumping)
  - paper: doi:10.1111/j.1467-8640.1993.tb00310.x
    title: Patrick Prosser, Hybrid algorithms for the constraint satisfaction problem, Computational Intelligence 9(3), 1993
    locator: pp. 268 to 299
  - paper: doi:10.1145/321296.321300
    title: Solomon W. Golomb and Leonard D. Baumert, Backtrack programming, Journal of the ACM 12(4), 1965
    locator: pp. 516 to 524
  - paper: doi:10.1090/psapm/010/0121306
    title: R. J. Walker, An enumerative technique for a class of combinatorial problems, Combinatorial Analysis, Proceedings of Symposia in Applied Mathematics 10, AMS, 1960
    locator: pp. 91 to 94
---

Chronological backtracking is the plain backtracking search for a [constraint satisfaction problem](/constraint-satisfaction-problem/): it assigns the variables in a fixed order, checks each new value against the values already assigned, and when a variable has no value left it goes back to the variable assigned just before it. The word *chronological* says that the search always undoes the most recent decision, whatever caused the failure. It is the [generic backtracking algorithm](/generic-backtracking-algorithm/) applied to a CSP, and it is the baseline for [backjumping](/conflict-directed-backjumping/), [forward checking](/forward-checking/) and the other improvements. It is sound and complete, and it can repeat the same failure an exponential number of times, which is called thrashing.

## In plain words

You fill in a form where some answers must agree with others. You answer the questions in order. For each question, you try the possible answers one at a time and keep the first one that agrees with all your earlier answers. If no answer fits, you go back to the question just before and change its answer.

This rule is simple and never misses a solution. Its weakness is that the question just before may have nothing to do with the problem. If question 9 fails because of question 1, the search changes questions 8, 7, 6 and so on in every possible way before it comes back to question 1, and question 9 fails again each time.

## The problem

A constraint satisfaction problem has variables $X_1, \ldots, X_m$, a finite ordered domain $D_i$ for each $X_i$, and a set of constraints. Each constraint names some variables and the combinations of their values that it allows. A *partial assignment* gives values to some variables. It is *consistent* when it violates no constraint whose variables all have values. A *solution* is a consistent assignment of all $m$ variables. The task is to find one solution or to report that there is none. The page uses binary constraints, between two variables, in the code; the method is the same for constraints of any arity.

## The algorithm

The variables are assigned in the order $X_1, X_2, \ldots, X_m$. The call BT$(a, 1)$ with the empty assignment $a$ returns a solution or *failure*.

```pseudo id=main
BT(a, i)                         ▷ a assigns X_1 .. X_{i−1} and is consistent
L1  if i > m then return a
L2  for each v in D_i, in order do
L3      if a ∪ {X_i = v} violates no constraint then   ▷ check only the constraints on X_i and earlier variables
L4          a[X_i] ← v
L5          r ← BT(a, i + 1)
L6          if r ≠ failure then return r
L7          remove X_i from a
L8  return failure                ▷ the caller changes X_{i−1}, the most recent assignment
```

Line L3 is the consistency check. Since $a$ is already consistent, only the constraints between $X_i$ and the variables $X_1, \ldots, X_{i-1}$ need a check. Line L8 is the chronological step: the failure of $X_i$ always returns control to the loop of $X_{i-1}$, which tries its next value. To list all solutions instead of one, output $a$ at line L1 and do not return at line L6.

## Example

Take four variables with $D_1 = D_4 = \{1, 2\}$ and $D_2 = D_3 = \{1, 2, 3\}$, and two constraints: $X_2 \ne X_3$ and $X_4 < X_1$. The variables $X_2$ and $X_3$ have no constraint with $X_1$ or $X_4$.

| $X_1$ | $X_2$ | $X_3$ | $X_4$ tried | result |
|---|---|---|---|---|
| 1 | 1 | 1 rejected, 2 | 1, 2 rejected | back to $X_3$ |
| 1 | 1 | 3 | 1, 2 rejected | back to $X_3$, then $X_2$ |
| 1 | 2 | 1 | 1, 2 rejected | back to $X_3$ |
| 1 | 2 | 2 rejected, 3 | 1, 2 rejected | back to $X_3$, then $X_2$ |
| 1 | 3 | 1 | 1, 2 rejected | back to $X_3$ |
| 1 | 3 | 2 | 1, 2 rejected | 3 rejected, back to $X_2$, then $X_1$ |
| 2 | 1 | 1 rejected, 2 | 1 | solution $(2, 1, 2, 1)$ |

With $X_1 = 1$, no value of $X_4$ satisfies $X_4 < X_1$. Chronological backtracking does not know this. It tries all 6 pairs of different values of $X_2$ and $X_3$, and each time $X_4$ fails for the same reason. The search makes 14 assignments and 24 constraint checks. [Conflict-directed backjumping](/conflict-directed-backjumping/) records that the failure of $X_4$ involves only $X_1$, and jumps from $X_4$ straight back to $X_1$. On this instance it makes 7 assignments and 7 checks.

## Correctness

BT is the [generic backtracking algorithm](/generic-backtracking-algorithm/) with $D_{i}$ as the candidates and consistency as the test. Consistency is prefix-closed: if an assignment of $X_1, \ldots, X_i$ violates no constraint, then its restriction to $X_1, \ldots, X_{i-1}$ violates none, because each constraint checked on the shorter assignment is also checked on the longer one. So the search visits exactly the consistent assignments of $X_1, \ldots, X_k$, for each $k$, in lexicographic order, and returns the first consistent full assignment in that order. It returns failure if and only if no solution exists. The full proof is below.

## Complexity

A node of the search is a consistent assignment of $X_1, \ldots, X_{k}$. There are at most $d^{k}$ of them for each $k$. The node for $X_1, \ldots, X_{k-1}$ tries at most $d$ values for $X_k$ and checks each against at most $k - 1$ earlier variables. So the number of binary constraint checks is at most

$$\sum_{k=1}^{m} d^{k} (k-1) \le (m-1) \frac{d}{d-1} d^{m} \le 2 (m-1) d^m \quad (d \ge 2),$$

which is $O(m d^m)$. If one check costs $O(1)$, this is the time.

- **Worst case.** $O(m d^m)$. The bound is reached up to the factor $m$: on the instance with $D_i = \{1, \ldots, d\}$ for each $i$, $D_1 = D_m = \{1, 2\}$, and the one constraint $X_m < X_1$, the search with $X_1 = 1$ tries all $d^{m-2}$ assignments of $X_2, \ldots, X_{m-1}$ before it changes $X_1$. The problem is [NP-complete](/np-complete/), so no method is polynomial in the worst case unless P = NP. The point of the example is that this instance is easy for backjumping.
- **Best case.** When the first value of each variable is consistent, the search makes $m$ assignments and checks each binary constraint once, so it does at most $m(m-1)/2$ checks.
- **Space.** The recursion has depth $m$, and the assignment has $m$ entries, so the extra space is $O(m)$.

## Properties

- **Sound.** Each returned assignment is a solution: line L3 checks each constraint at the moment its last variable gets a value.
- **Complete.** If a solution exists, BT returns one. It returns the lexicographically first solution under the variable order and the value orders.
- **Memoryless.** It keeps no record of why a branch failed. This is what causes thrashing, and what backjumping and the learning of nogoods add.
- **Static order.** The order of the variables is fixed before the search. Dynamic orders are covered under [variable ordering heuristics](/variable-ordering-heuristics/).

## Variants and improvements

- **Backjumping.** On a failure, return to the most recent variable that is involved in the failure, not to the most recent variable. [Graph-based backjumping](/graph-based-backjumping/) uses the constraint graph; [conflict-directed backjumping](/conflict-directed-backjumping/) (Prosser 1993) keeps a conflict set for each variable. See also [non-chronological backtracking](/non-chronological-backtracking/) in SAT solvers.
- **Look-ahead.** Remove the values of future variables that conflict with the new assignment, as in [forward checking](/forward-checking/) and [maintaining arc consistency](/maintaining-arc-consistency/). A domain that becomes empty shows the failure early.
- **Ordering.** Choose the next variable by the [minimum remaining values](/minimum-remaining-values/) rule or the [degree heuristic](/degree-heuristic/). The tree changes, the solutions do not.
- **Dynamic backtracking.** [Dynamic backtracking](/dynamic-backtracking/) undoes a variable in the middle of the assignment and keeps the later ones.
- **All solutions.** Output at line L1 and continue. The proof below covers this version.

## When to use it

Use chronological backtracking for small problems, for problems whose constraints are mostly between variables close in the order, and as a correct reference against which to test a faster solver. For larger CSPs, add forward checking and a dynamic variable order first: they cost little and often reduce the tree by orders of magnitude. For SAT, use [DPLL](/dpll/) with unit propagation and conflict learning.

## Pitfalls

- **Checking against all variables.** Line L3 must check only constraints whose variables all have values. A check of a constraint with an unassigned variable either fails wrongly or reads a stale value.
- **A stale value after undo.** If line L7 is missing and the code tests "has $X_j$ a value?" by a field that is not reset, later checks read the old value. Remove the assignment, or keep the assignment as a stack whose length is $i - 1$.
- **Thrashing taken as hardness.** A long run of chronological backtracking does not show that an instance is hard. The example above has a failure that one backjump removes.
- **Order of returns.** With "return on first solution" at line L6, the result depends on the value orders. Tests that compare with another solver must compare the set of solutions, or only the existence of one.

## Implementations

## History

Backtracking for combinatorial search was described by Walker in 1960 and by Golomb and Baumert in 1965. In the constraint satisfaction literature the plain method is called *chronological backtracking*, in contrast with backjumping, which may return to an earlier variable. Prosser's 1993 paper compares chronological backtracking with backjumping, conflict-directed backjumping and forward checking in one framework, and Chapters 5 and 6 of Dechter's book give the modern account.

## References
