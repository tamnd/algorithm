---
tag: 7XCRR6
kind: algorithm
slug: conflict-directed-backjumping
name: Conflict-directed backjumping
aliases:
- CBJ
- backjumping
- BT-CBJ
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: Backtracking that records, for each variable, the earlier variables that made its values fail, and at a dead end jumps back to the latest of them, merging the sets so that no solution is skipped.
solves: [constraint-satisfaction-problem]
model: word-ram
complexity:
  vars: {n: the number of variables, d: the largest domain size}
  time: {worst: O(n d^n)}
  space: {extra: O(n^2 + n d)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 1993
  people: [Patrick Prosser]
  note: Gaschnig (1979) gave backjumping, which jumps back only from a dead end at the deepest level. Dechter (1990) gave graph-based backjumping. Prosser (1993) gave conflict-directed backjumping, which keeps a conflict set for every variable and jumps from every dead end, and combined it with forward checking and other methods. Kondrak and van Beek (1997) proved it correct.
prereqs: [chronological-backtracking, constraint-satisfaction-problem]
see_also: [graph-based-backjumping, dynamic-backtracking, nogood-learning, forward-checking, maintaining-arc-consistency, non-chronological-backtracking, cdcl, first-uip]
sources:
  - paper: doi:10.1111/j.1467-8640.1993.tb00310.x
    title: Patrick Prosser, Hybrid algorithms for the constraint satisfaction problem, Computational Intelligence 9(3), 1993
    locator: pages 268 to 299 (the conflict sets, BT-CBJ and the hybrids FC-CBJ and others, with experiments on the zebra problem and random problems)
  - paper: doi:10.1016/S0004-3702(96)00027-6
    title: Grzegorz Kondrak and Peter van Beek, A theoretical evaluation of selected backtracking algorithms, Artificial Intelligence 89, 1997
    locator: pages 365 to 387 (the proof that backjumping and conflict-directed backjumping are correct, and the partial order of BT, BJ, CBJ and FC by nodes visited)
  - paper: doi:10.1016/0004-3702(90)90046-3
    title: Rina Dechter, Enhancement schemes for constraint processing, backjumping, learning, and cutset decomposition, Artificial Intelligence 41(3), 1990
    locator: pages 273 to 312 (graph-based backjumping and learning)
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 4, Backtracking search algorithms, by Peter van Beek (backjumping, conflict-directed backjumping and the conflict sets)
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 6, General search strategies, look-back (Gaschnig's backjumping, graph-based backjumping and conflict-directed backjumping)
---

Conflict-directed backjumping (CBJ) is [chronological backtracking](/chronological-backtracking/) that can go back more than one level. For each variable $x_i$ it keeps a *conflict set* $CS[i]$: the earlier variables that ruled out some value of $x_i$. When every value of $x_i$ has failed, the current values of the variables in $CS[i]$ are already enough to make $x_i$ fail, so the search jumps straight back to the latest of them, $x_h$, and changes it. The variables between $x_h$ and $x_i$ are skipped. To stay correct when $x_h$ fails later as well, the conflict set of $x_i$ is merged into the conflict set of $x_h$. Prosser gave CBJ in 1993, and it is the constraint version of the *non-chronological backtracking* of [CDCL](/cdcl/) SAT solvers. This page is about CBJ. [Graph-based backjumping](/graph-based-backjumping/) jumps by the constraint graph alone, and [dynamic backtracking](/dynamic-backtracking/) jumps without erasing the work in between.

## In plain words

Plain backtracking always undoes the last choice. Often that choice has nothing to do with the failure. If the last variable cannot take any value because of a choice made much earlier, then trying new values for the variables in between is wasted work.

CBJ keeps a note for each variable: "which earlier choices blocked my values?" When a value fails a check, the search writes down the first earlier variable it clashed with. When a variable runs out of values, the search goes back directly to the latest variable in its note, and it hands over the rest of the note to that variable. That way, if the target also runs out of values, it still knows every earlier choice that took part in the failure.

## The problem

The input is a binary [constraint satisfaction problem](/constraint-satisfaction-problem/): variables $x_1, \ldots, x_n$ in a fixed order, finite domains $D(x_i)$, and binary constraints $C_{ji}$. The output is a solution, or every solution in the all-solutions version, or "failure". A *nogood* is a partial assignment that is part of no solution.

Notation: $n$ variables, $d$ the largest domain size.

## The algorithm

$CD[i]$ holds the values of $x_i$ not yet tried since the search last came down to $x_i$ from $x_{i-1}$, and $CS[i] \subseteq \{1, \ldots, i - 1\}$ is the conflict set of $x_i$.

```pseudo id=main
CBJ(x_1, ..., x_n, D, C)
L1  i ← 1; CD[1] ← D(x_1); CS[1] ← ∅
L2  while true do
L3      if CD[i] is empty then                         ▷ dead end at x_i
L4          if CS[i] = ∅ then return failure
L5          h ← the largest index in CS[i]
L6          CS[h] ← CS[h] ∪ CS[i] \ {h}
L7          i ← h                                      ▷ jump back to x_h
L8      else
L9          take a value a out of CD[i]; σ(x_i) ← a
L10         h ← the smallest j < i such that σ(x_j) and a violate C_ji, or none
L11         if h = none then
L12             if i = n then return σ                 ▷ all solutions: record σ, CS[n] ← {1, ..., n − 1}
L13             i ← i + 1; CD[i] ← D(x_i); CS[i] ← ∅
L14         else CS[i] ← CS[i] ∪ {h}
```

Line L10 checks the new value against $x_1, x_2, \ldots$ in this order and stops at the first conflict, so $h$ is the earliest variable that rules out $a$. Taking the earliest one makes the conflict set point as far back as possible. Line L7 jumps to $x_h$ but keeps $CD[h]$, so $x_h$ goes on with its next untried value. The levels between $h$ and $i$ are reset when the search comes down to them again at line L13.

Line L6 is the step that makes CBJ different from Gaschnig's backjumping. When $x_h$ runs out of values later, the reason is the union of its own conflicts and the conflicts that made $x_i$ fail, so both must be in $CS[h]$.

In the all-solutions mode, a solution says nothing about which earlier variable is to blame, so the solution sets $CS[n]$ to all earlier variables and the next dead end at $x_n$ goes back one level.

## Example

Take four variables with domains $\{1, 2\}$. The value $x_1 = 1$ rules out every value of $x_4$ ($C_{14}$ allows only the pairs with $x_1 = 2$), $x_3 \ne x_4$, and $x_2$ is in no constraint. CBJ finds the solution $(2, 1, 1, 2)$:

| node | assignment | check at L10 | conflict sets after the step | next |
|---|---|---|---|---|
| 1 | $x_1 = 1$ | consistent | | go to $x_2$ |
| 2 | $x_2 = 1$ | consistent | | go to $x_3$ |
| 3 | $x_3 = 1$ | consistent | | go to $x_4$ |
| 4 | $x_4 = 1$ | fails with $x_1$ | $CS[4] = \{1\}$ | next value |
| 5 | $x_4 = 2$ | fails with $x_1$ | $CS[4] = \{1\}$ | dead end, jump to $x_1$ |
| 6 | $x_1 = 2$ | consistent | | go to $x_2$ |
| 7 to 9 | $x_2 = 1$, $x_3 = 1$, $x_4 = 1$ | the last fails with $x_3$ | $CS[4] = \{3\}$ | next value |
| 10 | $x_4 = 2$ | consistent | | solution |

At node 5, the jump skips the untried values $x_3 = 2$ and $x_2 = 2$. Chronological backtracking tries all four combinations of $x_2$ and $x_3$ under $x_1 = 1$ and needs 20 nodes. [Graph-based backjumping](/graph-based-backjumping/) needs 13: its first jump goes to $x_3$, the latest neighbour of $x_4$, because it does not know that only $x_1$ was to blame.

On n-queens with the same static order, the implementation gives these counts of nodes to the first solution:

| $n$ | backtracking | CBJ |
|---|---|---|
| 6 | 171 | 161 |
| 8 | 876 | 765 |
| 10 | 975 | 881 |
| 12 | 3066 | 2586 |

On n-queens every pair of variables is constrained, so the jumps are short. CBJ gains much more on problems with structure, where a failure is often caused far back.

## Correctness

The proof uses one invariant. Call a value $v$ of $x_i$ *refuted* if it was taken out of $CD[i]$ since the search last came down to $x_i$.

**Invariant.** For each level $k \le i$ and each refuted value $v$ of $x_k$, no solution agrees with $\sigma$ on the variables of $CS[k]$ and gives $v$ to $x_k$. (In the all-solutions mode: no solution that is not yet recorded.)

- A value refuted at line L14 conflicts with $x_h$, so no solution agrees with $\sigma$ on $x_h$ and gives it $v$. Adding $h$ to $CS[i]$ keeps the statement true for the other refuted values, because agreeing on a larger set is a stronger condition.
- At a dead end, every value of $x_i$ is refuted, so no solution agrees with $\sigma$ on $CS[i]$ at all: the assignment to $CS[i]$ is a nogood. Then the current value of $x_h$, $h = \max CS[i]$, together with the assignment to $CS[i] \setminus \{h\}$, is a nogood. After line L6, $CS[h]$ contains $CS[i] \setminus \{h\}$, so the invariant holds for this value of $x_h$, and it still holds for the earlier refuted values of $x_h$. Every index in the new $CS[h]$ is smaller than $h$.
- If $CS[i] = \emptyset$ at a dead end, the empty assignment is a nogood, so there is no solution, and line L4 is right.

**Theorem.** CBJ is sound and complete: it returns a solution if and only if one exists, it never skips a solution, and in the all-solutions mode it returns every solution exactly once. With the same order, its nodes are a subset of the nodes of chronological backtracking, and both find the solutions in the same order.

The skipped part of the tree is the subtree below the current value of $x_h$ where the variables between $x_h$ and $x_i$ take other values. In that subtree, the variables of $CS[i]$ keep their current values, so it contains no solution. The full proof is below.

## Complexity

- **Time.** CBJ never visits a node that chronological backtracking with the same order would not visit, so it visits at most $d + d^2 + \cdots + d^n = O(d^n)$ nodes. Each node does at most $n - 1$ constraint checks at line L10 and $O(n)$ work on the conflict sets. The worst case is $O(n d^n)$ in the word-RAM. The problem is [NP-complete](/np-complete/), and on problems where no jump skips anything, CBJ is just backtracking.
- **Space.** The conflict sets take $O(n^2)$ bits or words, and the untried values $O(n d)$. The extra space is $O(n^2 + n d)$.

## Properties

- **Sound and complete, never skips a solution.** The tests compare the solutions and their order with chronological backtracking and with brute force.
- **Never more nodes than backtracking** with the same order.
- **Forgets.** The nogood found at a dead end is used for one jump and then dropped. The same failure can be found again in another branch. [Nogood learning](/nogood-learning/) keeps it.
- **Erases.** The jump erases the values of the variables between $x_h$ and $x_i$, even if they had nothing to do with the failure. [Dynamic backtracking](/dynamic-backtracking/) keeps them.
- **Deterministic, not recursive.**

## Variants and improvements

- **Gaschnig's backjumping (BJ).** Jumps back only from a dead end at a leaf, that is, after the last variable reached failed for every value, and jumps to the latest variable that conflicts with some value. At other dead ends it backtracks one level. CBJ jumps from every dead end.
- **Graph-based backjumping (GBJ).** Uses the earlier neighbours in the constraint graph in place of the recorded conflicts. It needs no checks to build its sets but can jump less far. See [graph-based backjumping](/graph-based-backjumping/).
- **FC-CBJ and MAC-CBJ.** With [forward checking](/forward-checking/), when $x_i = a$ removes values of a future $x_j$, $i$ is added to a set of $x_j$. At a wipe-out of $x_j$, the conflict set of $x_i$ gets the variables that removed values of $x_j$. Prosser (1993) gave FC-CBJ. With [MAC](/maintaining-arc-consistency/), the reasons for all removals must be tracked.
- **Learning.** Recording the conflict set at each dead end as a new constraint gives [nogood learning](/nogood-learning/). The [first-UIP](/first-uip/) rule of [CDCL](/cdcl/) solvers is a way to choose which nogood to learn and where to jump.
- **Dynamic backtracking.** Keeps the jump but does not erase the variables in between. See [dynamic backtracking](/dynamic-backtracking/).

## When to use it

Use CBJ with a static or weak variable order, on problems where a failure is often caused far back, such as structured scheduling or configuration problems. With a good dynamic order such as dom/deg and strong propagation such as [MAC](/maintaining-arc-consistency/), the order already moves the variables in conflict close together, and the gain of the jumps is often small. For SAT and for CSPs with many related failures, learning the nogoods, as in [CDCL](/cdcl/), gains more than jumping alone.

## Pitfalls

- **Not merging at line L6.** If $x_h$ fails later and its conflict set lacks the reasons of $x_i$, the next jump can go too far and skip solutions. This is the error that Gaschnig's backjumping avoids by jumping only from leaves.
- **Recording the latest conflict, not the first.** Line L10 must check $x_1, x_2, \ldots$ in this order and record the first conflict. Recording any conflicting variable is still correct, but the earliest gives the longest jumps.
- **Clearing conflict sets at the wrong time.** $CS[i]$ is cleared when the search comes down to $x_i$ (line L13), not when it jumps back to $x_i$. A jump to $x_h$ must keep $CS[h]$ and the untried values of $x_h$.
- **All solutions.** After a solution, jumping by the conflict set of $x_n$ skips other solutions. Set $CS[n]$ to all earlier variables.

## Implementations

## History

Gaschnig (1979) described backjumping, which jumps back from a dead end at the deepest level reached. Dechter (1990) described [graph-based backjumping](/graph-based-backjumping/), which uses the constraint graph and jumps from every dead end. Prosser (1993) gave conflict-directed backjumping, which keeps a conflict set per variable, merges the sets at each jump, and can be combined with backmarking and forward checking. He compared the hybrids on the zebra problem and random problems. Kondrak and van Beek (1997) proved that backjumping and CBJ are correct and ordered BT, BJ, CBJ and FC by the number of nodes they visit. The same idea appeared in SAT solvers as non-chronological backtracking in GRASP (Marques-Silva and Sakallah, 1996), where it is combined with clause learning. See [non-chronological backtracking](/non-chronological-backtracking/).

## References
