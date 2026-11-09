---
tag: ZP1QQ8
kind: algorithm
slug: ac-4
name: AC-4 algorithm
aliases:
- support-counting arc consistency
- AC4
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: Enforces arc consistency in optimal O(ed^2) time by maintaining support counters and lists of supported values.
model: word-ram
complexity:
  vars: {n: the number of variables, e: the number of binary constraints, d: the largest domain size}
  time: {worst: O(e d^2)}
  space: {extra: O(e d^2)}
properties: {deterministic: true, exact: true, in_place: true, online: false, recursive: false}
history:
  year: 1986
  people: [Roger Mohr, Thomas C. Henderson]
  note: Mohr and Henderson gave AC-4 and its O(ed^2) bound in 1986, and showed that this bound is optimal.
prereqs: [arc-consistency, ac-3]
see_also: [ac-3, constraint-propagation, maintaining-arc-consistency, path-consistency, pc-2, singleton-arc-consistency]
sources:
  - paper: doi:10.1016/0004-3702(86)90083-4
    title: Roger Mohr and Thomas C. Henderson, Arc and path consistency revisited, Artificial Intelligence 28(2), 1986
    locator: pages 225 to 233 (the algorithm AC-4, its O(ed^2) bound and its optimality, and the path consistency algorithm PC-3)
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 3, Consistency-enforcing algorithms (AC-4 and its complexity)
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 3, Constraint propagation, by Christian Bessière (fine-grained algorithms AC-4, AC-6 and AC-7, and their space)
  - paper: "Christian Bessière, Arc-consistency and arc-consistency again, Artificial Intelligence 65(1), 1994, pages 179 to 190"
    locator: the algorithm AC-6, with O(ed^2) time and O(ed) space
  - paper: "Richard J. Wallace, Why AC-3 is almost always better than AC-4 for establishing arc consistency in CSPs, Proceedings of IJCAI 1993"
    locator: the measured comparison of AC-3 and AC-4 on random and structured problems
---

AC-4 is an algorithm that enforces [arc consistency](/arc-consistency/) on a binary [constraint satisfaction problem](/constraint-satisfaction-problem/) by counting supports. For each value and each arc it stores how many values of the other variable support it, and for each value the list of values it supports. A deletion then costs only the work of decreasing the counters that it touches, so AC-4 runs in $O(e d^2)$ time in the worst case, which Mohr and Henderson (1986) showed is optimal. It computes the same closure as [AC-3](/ac-3/), but it needs $O(e d^2)$ space.

## In plain words

AC-3 looks for a partner of a value again and again, each time a neighbour loses a value. AC-4 does the search for partners only once, at the start. For each value and each constraint it writes down how many partners the value has, and it keeps, for each value, a list of the values that use it as a partner.

When a value is deleted, AC-4 walks its list and takes one away from the partner count of each value on the list. A count that reaches zero means that a value lost its last partner on that constraint, so that value is deleted too and goes on a to-do list. Each value is deleted at most once, and each entry of each list is used at most once. This is why the total work is no more than the work of the set-up step.

## The problem

The input is a binary CSP: variables $x_1, \ldots, x_n$, finite domains $D_1, \ldots, D_n$ with $|D_i| \le d$, and $e$ binary constraints. A constraint on $x_i$ and $x_j$ is a relation $R_{ij}$, and $R_{ji}$ is its converse; each constraint gives the two arcs $(i, j)$ and $(j, i)$. The output is the arc consistency closure $D^\ast$, the largest arc consistent subdomains, and a flag that is false when $D^\ast$ has an empty domain. The page [arc consistency](/arc-consistency/) proves that $D^\ast$ is unique.

Notation: $n$ variables, $d$ the largest domain size, $e$ binary constraints (the area writes $m$ for the number of constraints, and $m = e$ here). The cost is counted in constraint checks, the tests "is $(a, b) \in R_{ij}$?", and in the word-RAM with constant-time access to the counters and lists.

## The algorithm

For each arc $(i, j)$ and value $a \in D_i$, the counter $N[i, j, a]$ is the number of supports of $a$ on $(i, j)$. For each value $b \in D_j$, the list $S[j, b]$ holds the pairs $(i, a)$ such that $b$ supports $a$. $D^0$ is the input domains.

```pseudo id=main
AC-4(D, C)                                   ▷ binary CSP; D is changed in place
L1  L ← an empty list of deleted pairs (variable, value)
L2  for each arc (i, j) do
L3      for each a ∈ D⁰_i do
L4          for each b ∈ D⁰_j do                       ▷ one check each
L5              if (a, b) ∈ R_ij then N[i, j, a] ← N[i, j, a] + 1; append (i, a) to S[j, b]
L6          if N[i, j, a] = 0 and a ∈ D_i then delete a from D_i; append (i, a) to L
L7  while L ≠ ∅ do
L8      remove a pair (j, b) from L
L9      for each (i, a) ∈ S[j, b] with a ∈ D_i do
L10         N[i, j, a] ← N[i, j, a] − 1
L11         if N[i, j, a] = 0 then delete a from D_i; append (i, a) to L
L12 return true if no D_i is empty, else false
```

The set-up (lines L2 to L6) counts on the input domains $D^0$, even after some values are deleted, so that each counter and each list is complete. The test $a \in D_i$ of line L6 makes sure that each value enters $L$ at most once. Line L9 skips values that are already deleted, because their counters no longer matter.

## Example

Take $X, Y, Z \in \{1, 2, 3\}$ with $X < Y$ and $Y < Z$, the same input as on the [AC-3](/ac-3/) page. The set-up handles the arcs $(X, Y)$, $(Y, X)$, $(Y, Z)$, $(Z, Y)$ in this order and makes $4 \times 9 = 36$ checks. The counters are:

| arc | value 1 | value 2 | value 3 |
|---|---|---|---|
| $N[X, Y, \cdot]$ | 2 | 1 | 0 |
| $N[Y, X, \cdot]$ | 0 | 1 | 2 |
| $N[Y, Z, \cdot]$ | 2 | 1 | 0 |
| $N[Z, Y, \cdot]$ | 0 | 1 | 2 |

The zero counters delete $X = 3$, $Y = 1$, $Y = 3$ and $Z = 1$, and $L$ holds these four pairs. The loop then runs:

| removed from $L$ | its list $S$ (live values only) | counter changes | new deletions |
|---|---|---|---|
| $(X, 3)$ | empty | none | none |
| $(Y, 1)$ | $(Z, 2), (Z, 3)$ | $N[Z, Y, 2]$: 1 to 0, $N[Z, Y, 3]$: 2 to 1 | $Z = 2$ |
| $(Y, 3)$ | $(X, 1), (X, 2)$ | $N[X, Y, 1]$: 2 to 1, $N[X, Y, 2]$: 1 to 0 | $X = 2$ |
| $(Z, 1)$ | empty | none | none |
| $(Z, 2)$ | $(Y, 1)$ is deleted, so nothing | none | none |
| $(X, 2)$ | $(Y, 3)$ is deleted, so nothing | none | none |

The result is $D_X = \{1\}$, $D_Y = \{2\}$, $D_Z = \{3\}$, the same closure that AC-3 finds, after 36 checks and 4 counter decrements. AC-3 needs only 23 checks here. AC-4 pays for its set-up on every input, and wins only when the propagation is long.

## Correctness

AC-4 returns the arc consistency closure $D^\ast$, and true exactly when $D^\ast$ has no empty domain. The proof uses one invariant: after the set-up and at each test of line L7, for each arc $(i, j)$ and each $a \in D_i$, the counter $N[i, j, a]$ equals the number of $b$ with $(a, b) \in R_{ij}$ such that $b \in D_j$ or $(j, b)$ is still in $L$, and this number is positive. Processing $(j, b)$ removes it from $L$ and lowers by one the counter of each live value that it supported, so the invariant stays true. When $L$ is empty, each counter counts supports in $D_j$ and is positive, so the domains are arc consistent. A value of $D^\ast$ always keeps a support in $D^\ast \subseteq D$, so its counter never reaches zero and it is never deleted. The full proof is below.

## Complexity

**Set-up.** Lines L2 to L6 make $|D^0_i| \cdot |D^0_j| \le d^2$ checks for each of the $2e$ arcs, so $2 e d^2$ checks in total. Each allowed pair of each arc adds one entry to one list, so the lists hold at most $2 e d^2$ entries.

**Propagation.** A value is deleted at most once, at line L6 or line L11, because both lines first test that it is in $D_i$. So each pair $(j, b)$ is removed from $L$ at most once, and the loop of line L9 reads each list at most once. The total work of lines L7 to L11 is at most the total length of the lists, $2 e d^2$, plus $O(nd)$ for the pairs of $L$.

So AC-4 takes $O(e d^2)$ time in the worst case, with no constraint checks after the set-up. The counters take $2ed$ words and the lists $O(e d^2)$ words, so the extra space is $O(e d^2)$. The set-up always makes all its checks, so the time is $\Theta(e d^2)$ on every input whose domains have size $d$, also when nothing is deleted.

**Optimality.** No algorithm can do better in the worst case, up to the constant factor.

> **Theorem (Mohr and Henderson 1986).** Let an algorithm learn the relations only by constraint checks. For all $e, d \ge 1$, there are binary CSPs with $e$ constraints and domains of size $d$ on which the algorithm makes at least $e d^2$ checks before it can tell whether the arc consistency closure has an empty domain.
>
> *Proof.* Use $2e$ variables and $e$ constraints on disjoint pairs $(x_{2k-1}, x_{2k})$. For one constraint alone, the closure has no empty domain if the relation has at least one pair (the closure is then the set of first values and the set of second values of its pairs), and it is empty if the relation is empty. An adversary answers each check on constraint $k$ with "no", except that it answers "yes" to the last unchecked pair of constraint $k$. Suppose the algorithm stops while some constraint $k$ has an unchecked pair $p$. All answers on $k$ were "no". Each other constraint has either received a "yes", or it also has an unchecked pair, which the adversary can allow. So the answers fit an input where $R_k = \{p\}$ and every constraint is non-empty, which has a non-empty closure, and also an input where $R_k = \emptyset$, whose closure is empty. The algorithm gives the same answer on both, so it is wrong on one. So it must check all $d^2$ pairs of each of the $e$ constraints. $\square$

AC-3 has the bound $O(e d^3)$, which is a factor $d$ above this lower bound (see [AC-3](/ac-3/)).

## Properties

- **Exact and order independent.** The order in which $L$ gives out its pairs does not change the result, because the result is the unique closure.
- **Fine grained.** The propagation works on single deleted values, not on arcs.
- **Optimal time, large space.** $O(e d^2)$ time is optimal, but the lists also take $O(e d^2)$ space, and the set-up costs $\Theta(e d^2)$ even when nothing is deleted.
- **Costly to undo.** Inside a backtracking search, the counters must be restored when the search goes back. This makes AC-4 heavier than AC-3 as the propagator of [maintaining arc consistency](/maintaining-arc-consistency/).

## Variants and improvements

- **AC-6.** Bessière (1994) keeps only one current support for each value and arc, and the list of values that currently rely on each value. When a support is deleted, AC-6 looks for the next support after it in a fixed order of $D_j$. Time $O(e d^2)$, space $O(e d)$, and no full set-up.
- **AC-7.** AC-7 also uses the fact that $(a, b) \in R_{ij}$ exactly when $(b, a) \in R_{ji}$, so it never checks a pair twice in the two directions.
- **AC2001 (AC-3.1).** It keeps the queue of arcs of AC-3 and stores the last support found for each value and arc. Time $O(e d^2)$, space $O(e d)$, and it is easy to restore during search.
- **GAC-4.** The same counters on tuples give generalized arc consistency for non-binary constraints. The set-up enumerates all allowed tuples, so it is practical only for constraints given as small tables.
- **PC-3 and PC-4.** Mohr and Henderson applied counters to path consistency as well (PC-3). The corrected form PC-4 runs in $O(n^3 d^3)$ time. See [path consistency](/path-consistency/) and [PC-2](/pc-2/).

## When to use it

Use AC-4 when the propagation is expected to be long, for example when one deletion starts long chains of deletions, and when $e d^2$ words of memory are affordable. In most solvers AC-3 or AC2001 is the better choice: Wallace (1993) measured AC-3 faster than AC-4 on most random and structured problems, because AC-3 often finds a support after a few checks while AC-4 always pays the full set-up. AC-4 is still the standard example of an optimal arc consistency algorithm, and its counting idea is used in many filtering algorithms for [global constraints](/global-constraint/).

## Pitfalls

- **Counting on the shrinking domains.** If the set-up counts only on the current $D_j$ while it deletes values, some lists miss entries, and later deletions do not lower all the counters they should. Count on $D^0$, as lines L3 and L4 do, or handle the deletions with care.
- **Deleting a value twice.** Without the test $a \in D_i$, a value can enter $L$ twice and lower the counters of its supported values twice.
- **Lowering counters of deleted values.** Line L9 skips them. Lowering them does no harm to the result, but it can push a counter to zero again and delete a value a second time.
- **Forgetting that the set-up is the cost.** AC-4 is optimal in the worst case, not on each input. On an input where AC-3 finds supports at once, AC-4 can be slower by a factor of $d$.
- **Memory.** With $d = 1000$ and $e = 10^4$ the lists can reach $2 \cdot 10^{10}$ entries. Use AC-6 or AC2001 for large domains.

## Implementations

## History

Mohr and Henderson (1986) gave AC-4 in Arc and path consistency revisited, and showed that its $O(e d^2)$ time is optimal; until then the best bound was the $O(e d^3)$ of AC-3 (Mackworth and Freuder 1985). The same paper gave PC-3 for path consistency. Bessière (1994) reduced the space to $O(e d)$ with AC-6. Wallace (1993) measured that AC-3 is usually faster in practice. AC2001 later joined the simple queue of AC-3 with the optimal time of AC-4.

## References
