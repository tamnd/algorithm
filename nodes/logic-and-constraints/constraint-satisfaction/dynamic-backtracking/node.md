---
tag: KDGJJC
kind: algorithm
slug: dynamic-backtracking
name: Dynamic backtracking
aliases:
- Ginsberg's dynamic backtracking
- DBT
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: Backtracking that, at a dead end, unassigns only the latest variable to blame and keeps all other assignments, with stored explanations for eliminated values. Complete, in polynomial space.
solves: [constraint-satisfaction-problem]
model: word-ram
complexity:
  vars: {n: the number of variables, d: the largest domain size}
  time: {worst: O(n^2 d (n d + 1)^(n+1))}
  space: {extra: O(n^2 d)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 1993
  people: [Matthew L. Ginsberg]
  note: Ginsberg (1993) gave dynamic backtracking in the first volume of the Journal of Artificial Intelligence Research. It keeps the jump of backjumping but not the erasure of the work in between, and it keeps only the explanations that are still valid, so its space stays polynomial.
prereqs: [conflict-directed-backjumping, chronological-backtracking, constraint-satisfaction-problem]
see_also: [graph-based-backjumping, nogood-learning, min-conflicts, cdcl, non-chronological-backtracking, local-search]
sources:
  - paper: doi:10.1613/jair.1
    title: Matthew L. Ginsberg, Dynamic backtracking, Journal of Artificial Intelligence Research 1, 1993
    locator: pages 25 to 46 (eliminating explanations, the algorithm, and the theorem that it is complete and uses polynomial space)
  - paper: doi:10.1111/j.1467-8640.1993.tb00310.x
    title: Patrick Prosser, Hybrid algorithms for the constraint satisfaction problem, Computational Intelligence 9(3), 1993
    locator: pages 268 to 299 (conflict-directed backjumping, the method that dynamic backtracking changes)
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 4, Backtracking search algorithms, by Peter van Beek (dynamic backtracking and partial-order backtracking)
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 6, General search strategies, look-back (nogoods, learning and the methods that keep their valid nogoods)
---

Dynamic backtracking (DBT) is a search method for [constraint satisfaction problems](/constraint-satisfaction-problem/) that jumps back like [conflict-directed backjumping](/conflict-directed-backjumping/) but does not erase the work in between. For each value it rules out, it stores an *explanation*: the set of assigned variables whose current values rule it out. At a dead end it takes the union of the explanations, unassigns only the variable of the union that was assigned last, and keeps every other assignment, including the ones made after that variable. Explanations that mention the unassigned variable are deleted, so at most one explanation is stored for each value, and the space stays polynomial. Ginsberg proved in 1993 that the method is complete. Of the three related pages, [graph-based backjumping](/graph-based-backjumping/) jumps by the constraint graph, [CBJ](/conflict-directed-backjumping/) jumps by recorded conflicts and erases everything after the target, and DBT keeps what does not depend on the target.

## In plain words

Backjumping goes back to the real cause of a failure, but on its way back it throws away every choice made after the cause, even the ones that had nothing to do with it. Those choices must then be made again.

Dynamic backtracking keeps a note for each value it has crossed out: which current choices are to blame. At a dead end, it collects the notes of the stuck variable, finds the most recent choice among the blamed ones, and undoes only that one choice. The other choices stay. Notes that blamed the undone choice are no longer true, so they are thrown away. The old value of the undone variable gets a new note, so it is not tried again while the other blamed choices stay as they are.

## The problem

The input is a binary [constraint satisfaction problem](/constraint-satisfaction-problem/): variables $x_1, \ldots, x_n$, finite domains $D(x_i)$ and binary constraints. The output is a solution, or every solution in the all-solutions version, or "failure".

An *elimination* is a pair $(x, b)$, a value $b$ of $x$, with an *explanation* $E(x, b)$, a set of assigned variables. It is *valid* if no solution agrees with the current assignment $\sigma$ on $E(x, b)$ and gives $b$ to $x$. In other words, the current values of $E(x, b)$ together with $x = b$ form a nogood.

Notation: $n$ variables, $d$ the largest domain size. $P$ is the list of assigned variables in the order they were assigned.

## The algorithm

```pseudo id=main
DYNAMIC-BACKTRACKING(x_1, ..., x_n, D, C)
L1  P ← empty list; no value is eliminated
L2  while some variable is unassigned do
L3      x ← the unassigned variable with the smallest index
L4      for each value b of x that is not eliminated: if b conflicts with σ(y) for some y in P, eliminate (x, b) with E(x, b) ← {y}
L5      if some value of x is not eliminated then
L6          σ(x) ← the first such value; append x to P
L7      else                                           ▷ dead end at x
L8          U ← the union of E(x, b) over all values b of x
L9          if U = ∅ then return failure
L10         y ← the variable of U that comes last in P
L11         unassign y and remove it from P; every other variable keeps its value
L12         delete every elimination whose explanation contains y
L13         eliminate (y, old value of y) with E ← U \ {y}
L14 return σ                                          ▷ all solutions: record σ, then run L10 to L13 with U = P
```

Line L4 builds explanations of size one from the constraint checks. Line L13 builds a larger explanation from a dead end: the values of $U$ rule out every value of $x$, so the values of $U \setminus \{y\}$ rule out the current value of $y$. After line L11, the variable $x$ is still unassigned and $y$ is unassigned too. The next iteration takes the unassigned variable with the smallest index, which may be $y$ or $x$. The variables assigned after $y$ keep their values, which is the difference from backjumping.

## Example

Take four variables with domains $\{1, 2\}$. The value $x_1 = 1$ rules out every value of $x_4$, $x_3 \ne x_4$, and $x_2$ is in no constraint. This is the example of the [CBJ](/conflict-directed-backjumping/) and [GBJ](/graph-based-backjumping/) pages.

| step | action | $P$ | eliminations |
|---|---|---|---|
| 1 to 3 | $x_1 = 1$, $x_2 = 1$, $x_3 = 1$ | $x_1, x_2, x_3$ | none |
| 4 | L4 for $x_4$: both values conflict with $x_1$ | $x_1, x_2, x_3$ | $(x_4, 1)$: $\{x_1\}$; $(x_4, 2)$: $\{x_1\}$ |
| 5 | dead end, $U = \{x_1\}$, $y = x_1$: unassign $x_1$, keep $x_2$ and $x_3$ | $x_2, x_3$ | $(x_4, \cdot)$ deleted; $(x_1, 1)$: $\emptyset$ |
| 6 | L4 for $x_1$: value 1 is eliminated, value 2 has no conflict; $x_1 = 2$ | $x_2, x_3, x_1$ | $(x_1, 1)$: $\emptyset$ |
| 7 | L4 for $x_4$: value 1 conflicts with $x_3$; $x_4 = 2$ | $x_2, x_3, x_1, x_4$ | $(x_4, 1)$: $\{x_3\}$ |

DBT finds $(2, 1, 1, 2)$ after 5 assignments. [CBJ](/conflict-directed-backjumping/) needs 10: its jump to $x_1$ erases $x_2 = 1$ and $x_3 = 1$, and it makes them again. The explanation $\emptyset$ for $(x_1, 1)$ says that $x_1 = 1$ is in no solution at all.

On n-queens with the static order, the implementation needs 37, 59, 110 and 601 assignments to find a first solution for $n = 6, 8, 10, 12$, against 171, 876, 975 and 3066 for chronological backtracking. Each assignment of DBT costs more, because line L4 checks against all of $P$ and line L12 scans the stored eliminations. DBT can also find a different first solution: for $n = 6$ it finds $(4, 1, 5, 2, 6, 3)$, while backtracking finds $(2, 4, 6, 1, 3, 5)$.

## Correctness

**Invariant.** Every stored elimination is valid, every variable in an explanation is assigned, and the assigned variables are consistent with each other.

- Line L4 stores $\{y\}$ only for a value that conflicts with $\sigma(y)$, so it is valid.
- At a dead end, every value of $x$ is eliminated, and each explanation is a subset of $U$. So no solution agrees with $\sigma$ on $U$, and no solution agrees with $\sigma$ on $U \setminus \{y\}$ and gives the old value to $y$. That is line L13. The variables of $U \setminus \{y\}$ stay assigned, with the same values.
- Line L12 deletes every explanation that mentions $y$, because $y$ is about to change. The other explanations keep their variables and values, so they stay valid.
- Line L6 picks a value that conflicts with no variable of $P$, so the assigned variables stay consistent.

So line L14 returns a solution, and line L9 returns failure only if the empty assignment is a nogood, that is, only if there is no solution.

**Termination.** Give each elimination an *anchor*: the position in $P$ of the latest variable of its explanation, or position 0 for an empty explanation. Let $c_k$ be the number of eliminations anchored at position $k$, and compare the vectors $(c_0, c_1, \ldots, c_{|P|})$ in lexicographic order, where a proper prefix is smaller. Each step makes the vector strictly larger. Line L4 adds eliminations, line L6 adds a position at the end, and a dead end deletes only eliminations anchored at the position $p$ of $y$ or later, while it adds one elimination anchored before $p$. Each $c_k$ is at most $n d$ and the vector has at most $n + 1$ entries, so the steps cannot go on forever.

**Theorem (Ginsberg 1993).** Dynamic backtracking is sound and complete: it returns a solution if and only if one exists, and in the all-solutions mode it returns every solution (the tests check that none is repeated). It stores at most one explanation for each value, so it uses $O(n^2 d)$ space. The full proof is below.

## Complexity

- **Space.** At most one elimination is stored for each pair $(x, b)$, since line L4 skips eliminated values and line L13 eliminates the current value of $y$, which was not eliminated. So there are at most $n d$ eliminations, each with at most $n$ variables, and the space is $O(n^2 d)$. Unlimited [nogood learning](/nogood-learning/) can need exponential space.
- **Time.** The termination proof bounds the number of steps by the number of vectors, at most $(n + 2)(n d + 1)^{n+1}$. One step costs $O(n d)$ in the word-RAM: line L4 checks at most $d$ values against at most $n$ variables, and line L12 scans at most $n d$ eliminations with a constant-time membership test. The bound $O(n^2 d (n d + 1)^{n+1})$ is crude. The problem is [NP-complete](/np-complete/), and no backtracking method avoids an exponential worst case.
- **Compared with backtracking.** DBT does not visit a subset of the backtracking tree. It can visit assignments that backtracking never reaches, because it changes an early variable and keeps later ones.

## Properties

- **Sound, complete, polynomial space.** These are the properties that Ginsberg proved.
- **Keeps unrelated work.** A dead end changes one variable. In problems made of nearly independent parts, the work on one part is not lost when another part fails.
- **Not a tree search.** The set of assigned variables is not always a prefix of the order. This is why the termination proof needs a measure other than the depth-first order.
- **Deterministic, not recursive.**

## Variants and improvements

- **Partial-order backtracking.** Ginsberg and McAllester (1994) relaxed the order in which the culprit is chosen, which gives more freedom and allows moves like those of [local search](/local-search/) with the same guarantee of completeness.
- **With look-ahead.** Combining DBT with [forward checking](/forward-checking/) or [MAC](/maintaining-arc-consistency/) needs explanations for every value that propagation removes. Several later papers did this. With strong propagation and a dynamic variable order, the gain of DBT can be lost, because a variable that is kept may no longer be a good choice.
- **Learning more.** Keeping the explanations that line L12 deletes, in a bounded store, gives [nogood learning](/nogood-learning/). [CDCL](/cdcl/) SAT solvers keep learned clauses but erase assignments, the opposite choice from DBT.

## When to use it

Use DBT when the problem has parts that interact weakly, so that backjumping would throw away much unrelated work, and when the variable order is static or changes little. Ginsberg reported large gains on crossword puzzle generation. With a strong dynamic variable order and [MAC](/maintaining-arc-consistency/), the advantage is often small, and the cost per step is higher than for [CBJ](/conflict-directed-backjumping/).

## Pitfalls

- **Keeping invalid explanations.** When $y$ is unassigned, every explanation that contains $y$ must go. A stale explanation can rule out a value that is in a solution, and the search can then miss solutions or report failure wrongly.
- **Choosing the wrong culprit.** Line L10 must take the variable of $U$ that was assigned last, not the one with the largest index. The termination proof uses the order of $P$.
- **Forgetting the old value.** Without line L13, the search can give $y$ its old value again and loop.
- **Expecting a subset of the backtracking tree.** DBT is complete, but it may assign values that backtracking would skip. Compare it with backtracking by the solutions found, not by the nodes visited.

## Implementations

## History

Ginsberg (1993) gave dynamic backtracking in the first volume of the Journal of Artificial Intelligence Research. He used the term *eliminating explanation* and proved that the method is complete and uses polynomial space. He showed it on crossword puzzles, where backjumping erased much useful work. Ginsberg and McAllester (1994) generalized it to partial-order backtracking. Later work combined it with propagation and studied when it helps.

## References
