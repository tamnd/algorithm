---
tag: 346K9S
kind: algorithm
slug: forward-checking
name: Forward checking
aliases:
- FC
- forward checking search
area: logic-and-constraints/constraint-satisfaction
level: core
summary: Backtracking search for a binary CSP that, after each assignment, removes the conflicting values from the domains of the unassigned neighbours and backtracks when a domain becomes empty.
solves: [constraint-satisfaction-problem]
model: word-ram
complexity:
  vars: {n: the number of variables, d: the largest domain size}
  time: {worst: O(n d^(n+1))}
  space: {extra: O(n d)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 1980
  people: [Robert M. Haralick, Gordon L. Elliott]
  note: Haralick and Elliott named and studied forward checking in 1980 and compared it with backtracking and with look-ahead methods that do more propagation. They found forward checking the best of the methods they tested on n-queens and random problems.
prereqs: [constraint-satisfaction-problem, chronological-backtracking, arc-consistency]
see_also: [maintaining-arc-consistency, conflict-directed-backjumping, minimum-remaining-values, generic-backtracking-algorithm, constraint-propagation, n-queens-problem, search-tree-pruning]
sources:
  - paper: doi:10.1016/0004-3702(80)90051-X
    title: Robert M. Haralick and Gordon L. Elliott, Increasing tree search efficiency for constraint satisfaction problems, Artificial Intelligence 14(3), 1980
    locator: pages 263 to 313 (forward checking, the comparison with backtracking and full look-ahead, and the fail-first principle)
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 5, General search strategies, look-ahead (forward checking and its relation to arc consistency)
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 4, Backtracking search algorithms, by Peter van Beek (forward checking and the hierarchy of look-ahead methods)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, 4th edition, Pearson, 2020
    locator: Chapter 6, Constraint satisfaction problems, interleaving search and inference
---

Forward checking is [chronological backtracking](/chronological-backtracking/) with one cheap step of [constraint propagation](/constraint-propagation/) after each assignment. When the search gives a value $a$ to a variable $x_i$, it looks at every unassigned variable $x_j$ that shares a constraint with $x_i$ and deletes from the current domain of $x_j$ the values that are not compatible with $x_i = a$. If some domain becomes empty, the value $a$ cannot be part of a solution and the search tries the next value at once. The deleted values come back when the search undoes the assignment. Forward checking is sound and complete, it never visits more nodes than plain backtracking with the same order, and it is the weakest of the standard look-ahead methods. [Maintaining arc consistency](/maintaining-arc-consistency/) does more work per node to prune more.

## In plain words

Plain backtracking places one variable at a time and only checks a new value against the values already placed. It finds out that a later variable has no possible value only when it reaches that variable.

Forward checking looks ahead by one step. Each time it places a value, it crosses out, in the lists of the variables still to place, every value that now clashes. If some list becomes empty, the current choice is hopeless, and the search changes it at once instead of going deeper. When the search goes back, it puts the crossed-out values back.

The lists of the variables still to place only ever hold values that agree with everything placed so far. So the search never needs to check a new value against the past.

## The problem

The input is a binary [constraint satisfaction problem](/constraint-satisfaction-problem/): variables $x_1, \ldots, x_n$, finite domains $D(x_1), \ldots, D(x_n)$, and binary constraints $C_{ij} \subseteq D(x_i) \times D(x_j)$. Two constraints on the same pair are replaced by their intersection. An assignment $\sigma$ to some of the variables is *consistent* if it satisfies every constraint whose two variables it assigns. The output is a solution, that is, a consistent assignment to all $n$ variables, or "failure" if there is none. In the all-solutions version the output is every solution.

Notation: $n$ is the number of variables, $d = \max_i |D(x_i)|$, and the variables are taken in the static order $x_1, \ldots, x_n$. A dynamic order such as [minimum remaining values](/minimum-remaining-values/) changes only which variable comes next.

## The algorithm

The algorithm keeps a *current domain* $CD[j] \subseteq D(x_j)$ for each variable, and for each level $i$ a list $pruned[i]$ of the pairs $(j, b)$ that the assignment at level $i$ removed.

```pseudo id=main
FORWARD-CHECKING(x_1, ..., x_n, D, C)
L1  CD[j] ← D(x_j) for each j; i ← 1; the untried values of x_1 are CD[1]
L2  while i ≥ 1 do
L3      put back the values in pruned[i]; pruned[i] ← empty
L4      if no untried value of x_i is left then
L5          i ← i − 1                                  ▷ backtrack
L6      else
L7          a ← the next untried value of x_i; σ(x_i) ← a
L8          for each j > i with a constraint C_ij, and each b ∈ CD[j] with (a, b) ∉ C_ij do
L9              remove b from CD[j] and add (j, b) to pruned[i]
L10         if no CD[j] with j > i is empty then
L11             if i = n then return σ                 ▷ all solutions: record σ and go on
L12             i ← i + 1; the untried values of x_i are CD[i]
L13 return failure
```

Line L3 undoes the work of the previous value at level $i$, or the work of level $i$ when the search comes back from level $i + 1$. Line L8 may stop as soon as one future domain is empty. Line L12 fixes the untried values of the new level to its current domain, which only holds values that agree with $x_1, \ldots, x_i$. The implementation tries the values of each level in the order of the input domain.

## Example

Take the 4-queens problem: $x_i \in \{1, 2, 3, 4\}$ is the row of the queen in column $i$, and two queens must not share a row or a diagonal, so $C_{ij}$ allows $(a, b)$ when $a \ne b$ and $|a - b| \ne j - i$. Forward checking finds the first solution after 8 assignments:

| node | assignment | current domains of the future variables after L8 | result |
|---|---|---|---|
| 1 | $x_1 = 1$ | $x_2 \{3, 4\}$, $x_3 \{2, 4\}$, $x_4 \{2, 3\}$ | go deeper |
| 2 | $x_2 = 3$ | $x_3 \{\}$ | wipe-out, next value |
| 3 | $x_2 = 4$ | $x_3 \{2\}$, $x_4 \{3\}$ | go deeper |
| 4 | $x_3 = 2$ | $x_4 \{\}$ | wipe-out, back to $x_1$ |
| 5 | $x_1 = 2$ | $x_2 \{4\}$, $x_3 \{1, 3\}$, $x_4 \{1, 3, 4\}$ | go deeper |
| 6 | $x_2 = 4$ | $x_3 \{1\}$, $x_4 \{1, 3\}$ | go deeper |
| 7 | $x_3 = 1$ | $x_4 \{3\}$ | go deeper |
| 8 | $x_4 = 3$ | none | solution $(2, 4, 1, 3)$ |

At node 1, the queen at row 1 of column 1 crosses out row 1 everywhere and one square on each diagonal. At node 4 the search returns to $x_1$ without trying $x_3 = 4$, because $x_3$ had only the value 2 left. Chronological backtracking with the same order needs 26 assignments to reach the same solution.

The implementation gives these counts of assignments with the same static order (the all-solutions columns go through the whole tree):

| $n$ | backtracking, first solution | forward checking, first solution | backtracking, all solutions | forward checking, all solutions |
|---|---|---|---|---|
| 4 | 26 | 8 | 60 | 16 |
| 6 | 171 | 27 | 894 | 130 |
| 8 | 876 | 88 | 15720 | 1724 |

## Correctness

The proof rests on one invariant. Before line L4 runs at level $i$, every value left in $CD[j]$, $j \ge i$, agrees with every constraint between $x_j$ and the assigned variables $x_1, \ldots, x_{i-1}$, and $CD[j]$ holds exactly those values of $D(x_j)$. Line L8 removes only values that conflict with the new assignment, and line L3 puts back exactly what the level removed.

- **Soundness.** At line L11, $x_n$ got a value from $CD[n]$, which agrees with $x_1, \ldots, x_{n-1}$ by the invariant. Each earlier variable also got a value that agreed with the variables before it. So every constraint is satisfied, and $\sigma$ is a solution.
- **Completeness.** A value $b$ is removed from $CD[j]$ only if $(\sigma(x_i), b) \notin C_{ij}$, so no solution that extends the current $\sigma$ gives $b$ to $x_j$. A wipe-out at line L10 then means that the current $\sigma$ extends to no solution. So the search drops only subtrees with no solution, and it tries every value of each level that is not removed. In the all-solutions mode it reports each solution exactly once.
- **Never more nodes than backtracking.** The tree of forward checking is a subtree of the backtracking tree with the same order: each node of forward checking is a consistent partial assignment, and each such node is also a node of backtracking, whose parent is consistent too.

The full proof is below.

## Complexity

- **Time.** The search tree has at most $d + d^2 + \cdots + d^n = O(d^n)$ nodes. At each node, line L8 checks at most $d$ values for each of at most $n - 1$ future variables, and line L3 puts back at most as many. So the worst case is $O(n d^{n+1})$ constraint checks, in the word-RAM with $O(1)$ membership tests in a constraint. The problem is [NP-complete](/np-complete/), so an exponential worst case is expected.
- **Space.** The current domains take $O(n d)$ words. A value of $x_j$ is removed at most once along the current branch, so all the lists $pruned[i]$ together hold at most $n d$ pairs. The extra space is $O(n d)$, besides the input.
- **Per node.** Forward checking does $O(n d)$ work at each node. [Maintaining arc consistency](/maintaining-arc-consistency/) does up to $O(e d^3)$ with AC-3 for $e$ constraints, and prunes more.

## Properties

- **Sound and complete.** It returns a solution exactly when one exists, and in the all-solutions mode it returns each solution once.
- **Never worse than backtracking in nodes.** With the same variable and value order, its tree is a subtree of the backtracking tree. In constraint checks it can do more work, because it checks each future value at once instead of when the search reaches it.
- **Same first solution as backtracking.** With the same order, both meet the solutions in the same order, so they return the same first solution. The tests check this.
- **Deterministic, not recursive.** The implementation keeps its levels in arrays and uses no recursion.

## Variants and improvements

- **Dynamic variable order.** Forward checking keeps the current domains up to date, so choosing the variable with the smallest current domain next costs nothing extra. This is the [minimum remaining values](/minimum-remaining-values/) rule, which Haralick and Elliott proposed with forward checking. See also [variable ordering heuristics](/variable-ordering-heuristics/).
- **Stronger look-ahead.** *Partial look-ahead* and *full look-ahead* also check pairs of future variables. [Maintaining arc consistency](/maintaining-arc-consistency/) makes the whole future arc consistent after each assignment.
- **Non-binary constraints.** nFC0 to nFC5 (Bessière, Meseguer, Freuder and Larrosa, 2002) are generalizations that differ in which constraints with two or more unassigned variables they also check.
- **Backjumping.** FC-CBJ adds [conflict-directed backjumping](/conflict-directed-backjumping/): each removal at line L9 records that $x_i$ is in the conflict set of $x_j$. Prosser (1993) gave this combination.
- **Branch and bound.** For [Max-CSP](/maximum-csp/), partial forward checking counts conflicts with the past in place of removing values, to get a lower bound.

## When to use it

Use forward checking when constraint checks are cheap and the problem is loose or of moderate size, or as the inner loop of a simple solver. It is a good default for puzzles such as [n-queens](/n-queens-problem/) and [graph coloring](/graph-coloring/). On hard problems near the phase transition, the extra pruning of [maintaining arc consistency](/maintaining-arc-consistency/) usually pays for its cost. For [Sudoku](/sudoku/) and other problems with [all-different constraints](/all-different-constraint/), a solver should also use a global propagator.

## Pitfalls

- **Restoring in the wrong place.** The values that the assignment $x_i = a$ removed must come back before the next value of $x_i$ is tried, not only when the search leaves level $i$. Line L3 does both, because it runs at every entry to level $i$.
- **Fixing the untried values too early.** The untried values of $x_{i+1}$ must be read from $CD[i+1]$ after line L8 for $x_i$. A copy taken earlier holds values that conflict with $x_i$.
- **Checking only one direction.** A constraint given as $C_{ji}$ with $j > i$ also restricts $x_j$ when $x_i$ is assigned. The implementation stores each constraint in both directions.
- **Expecting fewer constraint checks.** Fewer nodes do not always mean less time. On easy problems backtracking can use fewer checks, because forward checking checks future values that the search never reaches.

## Implementations

## History

Haralick and Elliott (1980) gave forward checking its name and compared it, on n-queens and random problems, with backtracking and with partial and full look-ahead, which they also defined. In their measurements, forward checking was the most efficient of the methods they tested. The same paper proposed the fail-first principle, which led to the [minimum remaining values](/minimum-remaining-values/) rule. Later work on random problems (Sabin and Freuder, 1994, and Bessière and Régin, 1996) showed that [maintaining arc consistency](/maintaining-arc-consistency/) often does better on hard instances.

## References
