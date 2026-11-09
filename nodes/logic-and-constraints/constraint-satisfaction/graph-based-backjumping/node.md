---
tag: F25KS3
kind: algorithm
slug: graph-based-backjumping
name: Graph-based backjumping
aliases:
- GBJ
- Dechter's backjumping
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: Backtracking that, at a dead end, jumps back to the latest earlier neighbour of the failed variable in the constraint graph and passes its other earlier neighbours on to the target.
solves: [constraint-satisfaction-problem]
model: word-ram
complexity:
  vars: {n: the number of variables, d: the largest domain size}
  time: {worst: O(n d^n)}
  space: {extra: O(n^2 + n d)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 1990
  people: [Rina Dechter]
  note: Dechter (1990) gave graph-based backjumping together with learning and cutset decomposition. It uses only the constraint graph to decide where to jump, so it needs no bookkeeping during the checks.
prereqs: [chronological-backtracking, constraint-graph, constraint-satisfaction-problem]
see_also: [conflict-directed-backjumping, dynamic-backtracking, nogood-learning, cutset-conditioning, tree-structured-csp, depth-first-search, treewidth]
sources:
  - paper: doi:10.1016/0004-3702(90)90046-3
    title: Rina Dechter, Enhancement schemes for constraint processing, backjumping, learning, and cutset decomposition, Artificial Intelligence 41(3), 1990
    locator: pages 273 to 312 (graph-based backjumping, the parent sets and their merge at internal dead ends)
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 6, General search strategies, look-back (Gaschnig's backjumping, graph-based backjumping with induced ancestors, and its use with a depth-first search ordering)
  - paper: doi:10.1111/j.1467-8640.1993.tb00310.x
    title: Patrick Prosser, Hybrid algorithms for the constraint satisfaction problem, Computational Intelligence 9(3), 1993
    locator: pages 268 to 299 (conflict-directed backjumping, which replaces the graph by recorded conflicts)
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 4, Backtracking search algorithms, by Peter van Beek (graph-based backjumping and its relation to conflict-directed backjumping)
---

Graph-based backjumping (GBJ) is [chronological backtracking](/chronological-backtracking/) that, at a dead end, jumps back to the latest variable that shares a constraint with the failed variable. A variable that has no constraint with $x_i$ cannot be the reason that every value of $x_i$ fails, so changing it is wasted work. GBJ reads the reasons from the [constraint graph](/constraint-graph/) alone: the *jump set* of $x_i$ starts as its earlier neighbours, and at a dead end it is merged into the jump set of the target. Dechter gave GBJ in 1990. It needs no bookkeeping during the constraint checks, but it can jump less far than [conflict-directed backjumping](/conflict-directed-backjumping/), which records which earlier variables really failed. [Dynamic backtracking](/dynamic-backtracking/) is a third method in this family. It keeps the variables it jumps over.

## In plain words

When a variable has no value left, plain backtracking changes the last choice, even if that choice has no link to the stuck variable. GBJ looks at the map of constraints. Only the earlier variables joined to the stuck variable by a constraint can be the cause, so the search goes back directly to the latest of them.

If that variable also runs out of values later, its failure may come from its own neighbours or from the neighbours of the variable that sent the search back to it. So it inherits that list before the search goes on. The lists come from the map, so the search does not need to note which check failed.

## The problem

The input is a binary [constraint satisfaction problem](/constraint-satisfaction-problem/) with variables $x_1, \ldots, x_n$ in a fixed order, finite domains, and binary constraints. Its [constraint graph](/constraint-graph/) has an edge $\{x_j, x_i\}$ for each constraint. Write $P(i) = \{j < i : \{x_j, x_i\} \text{ is an edge}\}$ for the earlier neighbours (the *parents*) of $x_i$. The output is a solution, every solution in the all-solutions version, or "failure".

Notation: $n$ variables, $d$ the largest domain size.

## The algorithm

$CD[i]$ holds the untried values of $x_i$, and $J[i]$ is its jump set.

```pseudo id=main
GBJ(x_1, ..., x_n, D, C)
L1  i ← 1; CD[1] ← D(x_1); J[1] ← ∅
L2  while true do
L3      if CD[i] is empty then                         ▷ dead end at x_i
L4          if J[i] = ∅ then return failure
L5          h ← the largest index in J[i]
L6          J[h] ← J[h] ∪ J[i] \ {h}
L7          i ← h                                      ▷ jump back to x_h
L8      else
L9          take a value a out of CD[i]; σ(x_i) ← a
L10         if a is consistent with σ(x_1), ..., σ(x_{i−1}) then
L11             if i = n then return σ                 ▷ all solutions: record σ, J[n] ← {1, ..., n − 1}
L12             i ← i + 1; CD[i] ← D(x_i); J[i] ← P(i)
```

The loop is the same as in [conflict-directed backjumping](/conflict-directed-backjumping/), with one change. CBJ starts each conflict set empty and adds, at each failed check, the first earlier variable that conflicts. GBJ starts each jump set with all the parents and adds nothing during the checks. A failed check of $x_i$ is always with a parent, so the jump set of GBJ contains every variable that CBJ could record.

The merge at line L6 handles *internal dead ends*. If the search jumps from $x_i$ to $x_h$, and $x_h$ then runs out of values, the cause may be a parent of $x_h$ or one of the other parents of $x_i$. Dechter calls the merged set the *induced ancestors* of $x_h$. A jump set is reset only when the search comes down to the variable again at line L12.

## Example

Take four variables with domains $\{1, 2\}$. The value $x_1 = 1$ rules out every value of $x_4$, and $x_3 \ne x_4$. The variable $x_2$ is in no constraint. The parents are $P(2) = P(3) = \emptyset$ and $P(4) = \{1, 3\}$.

| node | assignment | check at L10 | jump sets | next |
|---|---|---|---|---|
| 1 to 3 | $x_1 = 1$, $x_2 = 1$, $x_3 = 1$ | consistent | $J[4] = \{1, 3\}$ on entry | go to $x_4$ |
| 4, 5 | $x_4 = 1$, $x_4 = 2$ | both fail with $x_1$ | | dead end, jump to $x_3$, $J[3] = \{1\}$ |
| 6 | $x_3 = 2$ | consistent | $J[4] = \{1, 3\}$ on entry | go to $x_4$ |
| 7, 8 | $x_4 = 1$, $x_4 = 2$ | both fail with $x_1$ | | dead end, jump to $x_3$, $J[3] = \{1\}$ |
| | | | | dead end at $x_3$, jump to $x_1$, skipping $x_2$ |
| 9 to 13 | $x_1 = 2$, $x_2 = 1$, $x_3 = 1$, $x_4 = 1$, $x_4 = 2$ | $x_4 = 1$ fails with $x_3$ | | solution $(2, 1, 1, 2)$ |

GBJ needs 13 nodes. Chronological backtracking needs 20: it also tries $x_2 = 2$ with both values of $x_3$. [Conflict-directed backjumping](/conflict-directed-backjumping/) needs 10: it records that only $x_1$ failed the values of $x_4$, so its first jump goes straight to $x_1$.

A second example from the tests shows the jump over a long stretch. With six variables and domains $\{0, 1, 2\}$, let $x_1 = 0$ rule out every value of $x_6$, let $x_2, x_3, x_4, x_5$ form a chain of $\ne$ constraints, and let $x_6$ have no other neighbour. At the first dead end of $x_6$, $J[6] = \{1\}$, so GBJ jumps straight to $x_1$. It finds the first solution after 18 nodes. Chronological backtracking tries every consistent assignment to $x_2, \ldots, x_5$ under $x_1 = 0$ before it changes $x_1$, which takes more than 100 nodes.

If the constraint graph is complete, as in n-queens, every earlier variable is a parent, every jump goes back one level, and GBJ is chronological backtracking. The tests check this.

## Correctness

The proof is the same as for [conflict-directed backjumping](/conflict-directed-backjumping/). The invariant is: for each refuted value $v$ of $x_k$, no solution agrees with $\sigma$ on the variables of $J[k]$ and gives $v$ to $x_k$. It holds for the values that fail a check at line L10, because the failed check is with a parent of $x_k$, and $P(k) \subseteq J[k]$. It is kept at a jump by the merge at line L6. So at a dead end, the assignment to $J[i]$ is a nogood, and the skipped part of the tree has no solution.

**Theorem.** GBJ is sound and complete: it returns a solution if and only if one exists, and it never skips a solution. With the same order, its nodes are a subset of the nodes of chronological backtracking, met in the same order, so both return the same first solution. In the all-solutions mode it returns every solution once. The full proof is below.

## Complexity

- **Time.** GBJ visits no node that chronological backtracking would not visit, so it visits $O(d^n)$ nodes, with at most $n - 1$ checks each. The worst case is $O(n d^n)$ in the word-RAM.
- **Structure.** The jumps depend on the order. With an order in which every variable comes after its parent in a [depth-first search](/depth-first-search/) tree of the constraint graph, each jump set stays on the path to the root, and the search below a variable splits into independent parts. Dechter's book shows that the time is then exponential only in the depth of this tree, not in $n$. This links GBJ to [treewidth](/treewidth/) and to [cutset conditioning](/cutset-conditioning/).
- **Space.** The jump sets take $O(n^2)$ and the untried values $O(n d)$, so the extra space is $O(n^2 + n d)$.

## Properties

- **Sound and complete, never skips a solution.**
- **No bookkeeping in the checks.** The sets come from the graph. Each check is a plain test, as in backtracking.
- **CBJ jumps at least as far from a leaf dead end.** A failed check of $x_i$ is always with a parent of $x_i$, so the conflict set that CBJ records at a variable reached from above is a subset of $P(i)$, and its latest element is not later than the latest parent. In the examples on this page, CBJ also visits fewer nodes in total.
- **Same as backtracking on dense graphs.** On a complete constraint graph, GBJ never jumps more than one level.
- **Deterministic, not recursive.**

## Variants and improvements

- **Gaschnig's backjumping.** Gaschnig (1979) jumps from a dead end at a leaf to the latest variable that conflicts with some value, and backtracks one level at other dead ends.
- **Conflict-directed backjumping.** Records the first conflicting variable of each failed value. See [conflict-directed backjumping](/conflict-directed-backjumping/).
- **Learning.** Dechter's 1990 paper also stores the nogood found at a dead end as a new constraint. This is graph-based [nogood learning](/nogood-learning/).
- **Pseudo-tree search.** With a depth-first search order of the constraint graph, the subproblems below a variable can be solved separately. AND/OR search builds on this idea.

## When to use it

Use GBJ when the constraint graph is sparse and the checks are cheap, so that recording conflicts in each check would cost more than it gains. It also suits constraints that are hard to explain, because GBJ needs no reason for a failure, only the scope of the constraint. On dense graphs it gains nothing over backtracking. When the reasons are cheap to record, [CBJ](/conflict-directed-backjumping/) jumps farther.

## Pitfalls

- **Jumping to the latest parent at an internal dead end.** At a dead end of $x_h$ reached by a jump, the target must be the latest variable of the merged set $J[h]$, not of $P(h)$. The parents of the variable that jumped to $x_h$ may be the real cause.
- **Not resetting the jump set.** $J[i]$ is reset to $P(i)$ only when the search comes down to $x_i$ at line L12. A jump to $x_i$ keeps the merged set.
- **All solutions.** After a solution, set $J[n]$ to all earlier variables. The parents of $x_n$ are not a reason to skip the other solutions.

## Implementations

## History

Gaschnig (1979) introduced backjumping. Dechter (1990) gave the graph-based version in a paper that also introduced learning of nogoods during search and cutset decomposition, and she showed how the depth of a depth-first search ordering bounds the search. Prosser (1993) then replaced the graph by recorded conflicts in [conflict-directed backjumping](/conflict-directed-backjumping/). Ginsberg (1993) gave [dynamic backtracking](/dynamic-backtracking/), which jumps without erasing the work in between.

## References
