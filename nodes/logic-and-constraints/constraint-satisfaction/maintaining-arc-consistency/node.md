---
tag: 178PFC
kind: algorithm
slug: maintaining-arc-consistency
name: Maintaining arc consistency
aliases:
- MAC
- MAC search
- full look-ahead with arc consistency
area: logic-and-constraints/constraint-satisfaction
level: core
summary: Backtracking search for a binary CSP that makes the unassigned variables arc consistent after each assignment, and backtracks when a domain becomes empty.
solves: [constraint-satisfaction-problem]
model: word-ram
complexity:
  vars: {n: the number of variables, d: the largest domain size, e: the number of binary constraints}
  time: {worst: O(e d^(n+3))}
  space: {extra: O(e + n d)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 1994
  people: [Daniel Sabin, Eugene C. Freuder]
  note: Look-ahead with full arc consistency is older (Gaschnig 1974, Haralick and Elliott 1980). Sabin and Freuder (1994) named MAC and showed on random problems that it often beats forward checking on hard instances. Bessière and Régin (1996) gave further measurements.
prereqs: [forward-checking, arc-consistency, ac-3]
see_also: [constraint-propagation, chronological-backtracking, conflict-directed-backjumping, regin-all-different-filtering, minimum-remaining-values, singleton-arc-consistency, ac-4, global-constraint]
sources:
  - paper: "Daniel Sabin and Eugene C. Freuder, Contradicting conventional wisdom in constraint satisfaction, Principles and Practice of Constraint Programming (PPCP 94), Lecture Notes in Computer Science 874, Springer, 1994, pages 10 to 20"
    locator: the MAC algorithm and the comparison with forward checking on random binary CSPs
  - paper: "Christian Bessière and Jean-Charles Régin, MAC and combined heuristics, two reasons to forsake FC (and CBJ?) on hard problems, Principles and Practice of Constraint Programming (CP 96), Lecture Notes in Computer Science 1118, Springer, 1996, pages 61 to 75"
    locator: MAC with the dom/deg variable order, measured against FC and FC-CBJ on random problems
  - paper: doi:10.1016/0004-3702(80)90051-X
    title: Robert M. Haralick and Gordon L. Elliott, Increasing tree search efficiency for constraint satisfaction problems, Artificial Intelligence 14(3), 1980
    locator: pages 263 to 313 (full look-ahead, partial look-ahead and forward checking)
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 4, Backtracking search algorithms, by Peter van Beek (look-ahead with arc consistency and the comparison of FC and MAC)
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 5, General search strategies, look-ahead (full and partial look-ahead and MAC)
---

Maintaining arc consistency (MAC) is backtracking search in which, after each assignment $x_i = a$, the solver runs an arc consistency algorithm such as [AC-3](/ac-3/) on the variables that are not yet assigned. Every value that has no support in the domain of some neighbour is removed, the removals spread, and the search backtracks if some domain becomes empty. The removed values come back when the search undoes the assignment. MAC is sound and complete. With the same order its search tree is part of the tree of [forward checking](/forward-checking/), which in turn is part of the tree of [chronological backtracking](/chronological-backtracking/). It is the default search of most finite-domain constraint solvers, where arc consistency is replaced by the propagators of the [global constraints](/global-constraint/).

## In plain words

[Forward checking](/forward-checking/) crosses out, after each choice, the values of the later variables that clash with that choice. MAC goes further. When a value of a later variable is crossed out, other later values may lose their last partner, so MAC crosses those out too, and it repeats until every remaining value of every later variable has a partner in each neighbour. If some list becomes empty, the choice is hopeless.

Each step costs more than in forward checking, but the search sees dead ends earlier and visits fewer choices. When it backtracks, it puts back all the values that the undone choice crossed out.

## The problem

The input is a binary [constraint satisfaction problem](/constraint-satisfaction-problem/): variables $x_1, \ldots, x_n$, finite domains $D(x_j)$, and binary constraints $C_{jk}$, with two constraints on the same pair intersected. A value $b$ of $x_j$ has a *support* on the arc $(x_j, x_k)$ if some $c$ in the current domain of $x_k$ has $(b, c) \in C_{jk}$. A set of current domains is [arc consistent](/arc-consistency/) if every value has a support on every arc. The output is a solution, or every solution in the all-solutions version, or "failure".

Notation: $n$ variables, $d$ the largest domain size, $e$ the number of binary constraints, and the static variable order $x_1, \ldots, x_n$.

## The algorithm

The current domains $CD[j]$ and the lists $pruned[i]$ play the same role as in [forward checking](/forward-checking/). The difference is lines L9 to L12, which run AC-3 on the future variables in place of one round of checks.

```pseudo id=main
MAC(x_1, ..., x_n, D, C)
L1  CD[j] ← D(x_j) for each j; run AC-3 on all arcs; if a CD[j] is empty then return failure
L2  i ← 1; the untried values of x_1 are CD[1]
L3  while i ≥ 1 do
L4      put back the values in pruned[i]; pruned[i] ← empty
L5      if no untried value of x_i is left then
L6          i ← i − 1                                  ▷ backtrack
L7      else
L8          a ← the next untried value of x_i; σ(x_i) ← a; CD[i] ← {a}, recording the removed values in pruned[i]
L9          Q ← the arcs (x_j, x_i) with j > i and a constraint C_ji
L10         while Q is not empty do
L11             take (x_j, x_k) from Q; remove from CD[j] each b with no support in CD[k], recording (j, b) in pruned[i]
L12             if CD[j] is empty then stop the loop; else if CD[j] changed then add to Q each arc (x_l, x_j) with l > i, l ≠ k
L13         if no CD[j] is empty then
L14             if i = n then return σ                 ▷ all solutions: record σ and go on
L15             i ← i + 1; the untried values of x_i are CD[i]
L16 return failure
```

Line L1 removes the values that are in no solution for a reason that arc consistency can see. These removals are kept for the whole search. Lines L9 to L12 are AC-3 restricted to the future variables. Arcs to assigned variables need no revision: an assigned variable has the single value $\sigma(x_k)$, and line L11 already removed every future value that conflicts with it. The first round of revisions, on the arcs $(x_j, x_i)$, is exactly the work of forward checking at line L8 of that page.

## Example

Take the 4-queens problem with $x_i \in \{1, 2, 3, 4\}$ the row of the queen in column $i$. Line L1 removes nothing: each value of each variable has a support in every other column. MAC then finds the first solution after 5 assignments.

| node | assignment | arc consistency on the future variables | result |
|---|---|---|---|
| 1 | $x_1 = 1$ | forward step: $x_2 \{3, 4\}$, $x_3 \{2, 4\}$, $x_4 \{2, 3\}$; then $x_2 = 3$ has no support in $x_3$, so $x_2 \{4\}$; then $x_3 \{2\}$; then $x_4 = 2$ and $x_4 = 3$ have no support in $x_3$ | wipe-out of $x_4$ |
| 2 | $x_1 = 2$ | forward step: $x_2 \{4\}$, $x_3 \{1, 3\}$, $x_4 \{1, 3, 4\}$; then $x_3 \{1\}$; then $x_4 \{3\}$ | all domains are single values |
| 3 | $x_2 = 4$ | nothing more to remove | go deeper |
| 4 | $x_3 = 1$ | nothing more to remove | go deeper |
| 5 | $x_4 = 3$ | none | solution $(2, 4, 1, 3)$ |

At node 1, forward checking would go on to try $x_2 = 4$ and $x_3 = 2$ before it finds the dead end (see the [forward checking](/forward-checking/) page, nodes 1 to 4). MAC finds it at once.

The implementation gives these counts of assignments, with the same static order for both methods:

| $n$ | forward checking, first solution | MAC, first solution | forward checking, all solutions | MAC, all solutions |
|---|---|---|---|---|
| 4 | 8 | 5 | 16 | 10 |
| 6 | 27 | 11 | 130 | 44 |
| 8 | 88 | 20 | 1724 | 768 |

The counts of nodes do not show the cost per node, which is higher for MAC.

A small case where arc consistency is not enough: three variables with domains $\{0, 1\}$ and $x_1 \ne x_2$, $x_1 \ne x_3$, $x_2 \ne x_3$. All arcs are consistent, so line L1 removes nothing. The assignment $x_1 = 0$ forces $x_2 = x_3 = 1$, which wipes out, and the same happens for $x_1 = 1$. MAC proves there is no solution after 2 nodes. A [global constraint](/global-constraint/) such as [all-different](/all-different-constraint/) with [Régin's filter](/regin-all-different-filtering/) would fail with no node at all.

## Correctness

Arc consistency removes a value $b$ of $x_j$ only if no value of a neighbour $x_k$ supports it, and then no solution that extends the current assignment gives $b$ to $x_j$. So MAC never removes a value that is in a solution below the current node, and it never cuts off a solution. The values it takes are always compatible with the assigned variables, so each complete assignment it reaches is a solution.

**Theorem.** MAC is sound and complete: it returns a solution if and only if one exists, and in the all-solutions mode it returns every solution exactly once. With the same variable and value order, every node of MAC is a node of forward checking, so MAC never visits more nodes than forward checking.

The second part holds because, at each node, the current domains of MAC are subsets of those of forward checking: both start from the same domains, both remove the values that conflict with the new assignment, and MAC removes more. The full proof is below.

## Complexity

- **Per node.** AC-3 on the future variables makes $O(e d^3)$ constraint checks in the worst case, and AC-2001 or [AC-4](/ac-4/) make $O(e d^2)$. This is more than the $O(n d)$ of forward checking. In practice the propagation after one assignment is incremental and much cheaper than the bound.
- **Whole search.** The tree has at most $d + d^2 + \cdots + d^n$ nodes, so the worst case is $O(e d^{n+3})$ checks with AC-3, in the word-RAM with constant-time membership tests. The problem is [NP-complete](/np-complete/).
- **Space.** The current domains take $O(n d)$ words, the lists $pruned[i]$ hold at most $n d$ pairs in total along one branch, and the queue holds at most $2e$ arcs. The extra space is $O(e + n d)$.

## Properties

- **Sound and complete**, as above.
- **Never more nodes than forward checking** with the same order. The tests compare both node counts on random problems.
- **Same first solution as backtracking.** All three methods visit the solutions in the same order when the order is the same, and the tests check this.
- **Not stronger than the propagation it uses.** MAC detects failure at a node only when arc consistency does. Stronger local consistencies, such as [singleton arc consistency](/singleton-arc-consistency/) or [path consistency](/path-consistency/), can prune more at a higher cost.
- **Deterministic, not recursive.** The implementation uses arrays for the levels.

## Variants and improvements

- **Other AC algorithms.** Any arc consistency algorithm can run at lines L9 to L12. AC-2001/3.1 keeps the last support of each value, which is cheap to restore on backtracking. [AC-4](/ac-4/) has the optimal worst case but a high cost to set up.
- **Binary branching.** Many solvers branch on $x_i = a$ versus $x_i \ne a$ and propagate after both. The second branch removes $a$ and runs arc consistency again, which can prune more than trying the next value directly.
- **Dynamic variable order.** MAC with the dom/deg order (current domain size divided by degree) is the combination that Bessière and Régin (1996) measured. See [minimum remaining values](/minimum-remaining-values/).
- **Global constraints.** A solver replaces AC-3 on binary constraints by a propagator for each constraint, such as [Régin's filter](/regin-all-different-filtering/) for all-different. The search loop stays the same. This is [constraint programming](/constraint-programming/).
- **Backjumping.** MAC-CBJ adds [conflict-directed backjumping](/conflict-directed-backjumping/). The conflict sets must record the reasons for every removal, so the bookkeeping is heavier than for FC-CBJ. The title of Bessière and Régin (1996) asks whether, with MAC and a good variable order, the jumps of CBJ are still worth their cost.

## When to use it

Use MAC for hard problems, and for problems with tight constraints, where pruning more per node saves many nodes. This is the usual case in scheduling and timetabling, and near the phase transition of random CSPs. On loose or easy problems, [forward checking](/forward-checking/) can be faster, because MAC propagates through constraints that never fail. For problems with structure, combine MAC with [global constraints](/global-constraint/) and a dynamic variable order.

## Pitfalls

- **Undoing only part of the propagation.** Every value removed at lines L8 and L11 must be recorded at the current level, including the values removed from variables far from $x_i$. If one is missed, a later branch loses a value and the search can miss solutions.
- **Revising arcs to assigned variables.** It does no harm, but it costs time. Arcs from assigned variables must not be revised, because the domain of an assigned variable is its value.
- **Restoring the initial removals.** The removals of line L1 are not recorded in any $pruned[i]$, and they must stay removed: those values are in no solution.
- **Comparing by nodes only.** MAC has fewer nodes than forward checking, but each node costs more. Measure time or constraint checks.

## Implementations

## History

Gaschnig (1974) and Haralick and Elliott (1980) described look-ahead schemes that check the future variables after each assignment. Haralick and Elliott's *full look-ahead* is close to MAC, but in their experiments it did not pay for its cost, and forward checking became the usual choice. Sabin and Freuder (1994) named MAC and showed, on random binary CSPs, that it often beats forward checking on hard instances, which went against the common view of that time. Bessière and Régin (1996) gave measurements of MAC with the dom/deg order against forward checking and FC-CBJ. Today, MAC with global constraint propagators is the search in most constraint programming solvers.

## References
