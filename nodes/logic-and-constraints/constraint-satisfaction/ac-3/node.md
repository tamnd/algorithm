---
tag: QXMHYC
kind: algorithm
slug: ac-3
name: AC-3 algorithm
aliases:
- arc revision algorithm AC-3
- AC3
area: logic-and-constraints/constraint-satisfaction
level: core
summary: Enforces arc consistency by repeatedly revising arcs whose domains have changed, in O(ed^3) time.
model: word-ram
complexity:
  vars: {n: the number of variables, e: the number of binary constraints, d: the largest domain size}
  time: {worst: O(e d^3)}
  space: {extra: O(e + n d)}
properties: {deterministic: true, exact: true, in_place: true, online: false, recursive: false}
history:
  year: 1977
  people: [Alan K. Mackworth]
  note: Mackworth defined AC-1, AC-2 and AC-3 in Consistency in networks of relations. Mackworth and Freuder proved the O(ed^3) bound in 1985.
prereqs: [arc-consistency, constraint-satisfaction-problem]
see_also: [ac-4, constraint-propagation, maintaining-arc-consistency, forward-checking, pc-2, singleton-arc-consistency, node-consistency, tree-structured-csp]
sources:
  - paper: doi:10.1016/0004-3702(77)90007-8
    title: Alan K. Mackworth, Consistency in networks of relations, Artificial Intelligence 8(1), 1977
    locator: pages 99 to 118 (node, arc and path consistency, and the algorithms AC-1, AC-2 and AC-3)
  - paper: doi:10.1016/0004-3702(85)90041-4
    title: Alan K. Mackworth and Eugene C. Freuder, The complexity of some polynomial network consistency algorithms for constraint satisfaction problems, Artificial Intelligence 25(1), 1985
    locator: pages 65 to 74 (the O(ed^3) bound for AC-3, and the bounds for AC-1 and path consistency)
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 3, Consistency-enforcing algorithms (REVISE, AC-1, AC-3 and AC-4, with their complexity)
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 3, Constraint propagation, by Christian Bessière (arc consistency algorithms AC-3, AC-4, AC-6 and AC2001)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, 2020
    locator: Chapter 6, Section 6.2 (constraint propagation and the AC-3 algorithm)
  - paper: "Christian Bessière, Jean-Charles Régin, Roland H. C. Yap and Yuanlin Zhang, An optimal coarse-grained arc consistency algorithm, Artificial Intelligence 165(2), 2005"
    locator: the algorithm AC2001/3.1, which keeps the AC-3 queue of arcs and runs in O(ed^2) time
---

AC-3 is an algorithm that enforces [arc consistency](/arc-consistency/) on a binary [constraint satisfaction problem](/constraint-satisfaction-problem/). It keeps a queue of arcs, removes each value that has no support on an arc, and puts back on the queue only the arcs that a removal can affect. It runs in $O(e d^3)$ time in the worst case and returns the unique arc consistency closure of the domains, or reports that a domain became empty. Mackworth gave it in 1977, and it is the propagation step inside [maintaining arc consistency](/maintaining-arc-consistency/) search.

## In plain words

Each variable has a list of possible values. Each constraint says which pairs of values two variables may take together. A value is useless if, for some constraint, no value of the other variable goes with it. AC-3 deletes useless values.

It keeps a to-do list of "variable, other variable" pairs. It takes a pair from the list and deletes each value of the first variable that has no partner among the values of the second. If it deleted something, the neighbours of the first variable may have lost their only partner, so their pairs go back on the list. When the list is empty, every remaining value has a partner on every constraint. If a list of values becomes empty, the problem has no solution.

AC-3 does not solve the problem. It only makes the lists shorter, and a search then works on the shorter lists.

## The problem

The input is a binary CSP: variables $x_1, \ldots, x_n$, finite domains $D_1, \ldots, D_n$ with $|D_i| \le d$, and $e$ binary constraints. Each constraint on $x_i$ and $x_j$ is a relation $R_{ij} \subseteq D_i \times D_j$, and $R_{ji} = \{(b, a) : (a, b) \in R_{ij}\}$ is the same constraint read the other way. The [constraint graph](/constraint-graph/) has an edge $\{i, j\}$ for each constraint, so it has $e$ edges, and each edge gives two directed *arcs* $(i, j)$ and $(j, i)$. If two constraints have the same two variables, we intersect them first, so each arc has one relation.

A value $a \in D_i$ is *supported* on the arc $(i, j)$ if some $b \in D_j$ has $(a, b) \in R_{ij}$. The domains are arc consistent if every value of every domain is supported on every arc that leaves its variable. The output is the *arc consistency closure*: the largest domains $D'_i \subseteq D_i$ that are arc consistent. The page [arc consistency](/arc-consistency/) defines the property and proves that this closure is unique. AC-3 is one way to compute it; [AC-4](/ac-4/) is another.

Notation: $n$ is the number of variables, $d$ the largest domain size, and $e$ the number of binary constraints (the area uses $m$ for the number of constraints, and $m = e$ here). The cost is counted in *constraint checks*, the tests "is $(a, b) \in R_{ij}$?", and in the word-RAM with a constant-time membership test.

## The algorithm

```pseudo id=main
AC-3(D, C)                                  ▷ binary CSP; D is changed in place
L1  if some D_i = ∅ then return false
L2  Q ← the 2e arcs (i, j) and (j, i) of the constraints
L3  while Q ≠ ∅ do
L4      remove an arc (i, j) from Q
L5      if REVISE(i, j) then
L6          if D_i = ∅ then return false
L7          for each neighbour k of i with k ≠ j do
L8              add (k, i) to Q, unless it is already in Q
L9  return true

REVISE(i, j)                                ▷ delete the values of D_i with no support in D_j
L10 G ← ∅
L11 for each a ∈ D_i do
L12     if no b ∈ D_j has (a, b) ∈ R_ij then
L13         G ← G ∪ {a}
L14 D_i ← D_i \ G; return G ≠ ∅
```

REVISE$(i, j)$ makes the arc $(i, j)$ consistent. It changes only $D_i$. A deletion from $D_i$ can remove the only support of a value $c \in D_k$ on the arc $(k, i)$, so lines L7 and L8 put these arcs back. The arc $(j, i)$ is not put back: a value $a$ that REVISE$(i, j)$ deletes has no partner in $D_j$, so it was the support of no value of $D_j$. The queue holds each arc at most once, so it is a set with a first-in, first-out order.

## Example

Take three variables $X, Y, Z$ with domains $\{1, 2, 3\}$ and the constraints $X < Y$ and $Y < Z$. The queue starts as $(X, Y), (Y, X), (Y, Z), (Z, Y)$, and REVISE tests the values in increasing order.

| step | arc | deleted | $D_X$ | $D_Y$ | $D_Z$ | queue after the step | checks |
|---|---|---|---|---|---|---|---|
| 1 | $(X, Y)$ | 3 from $X$ | {1, 2} | {1, 2, 3} | {1, 2, 3} | $(Y, X), (Y, Z), (Z, Y)$ | 8 |
| 2 | $(Y, X)$ | 1 from $Y$ | {1, 2} | {2, 3} | {1, 2, 3} | $(Y, Z), (Z, Y)$ | 4 |
| 3 | $(Y, Z)$ | 3 from $Y$ | {1, 2} | {2} | {1, 2, 3} | $(Z, Y), (X, Y)$ | 6 |
| 4 | $(Z, Y)$ | 1 and 2 from $Z$ | {1, 2} | {2} | {3} | $(X, Y)$ | 3 |
| 5 | $(X, Y)$ | 2 from $X$ | {1} | {2} | {3} | empty | 2 |

In step 2 the arc $(Z, Y)$ is already in the queue, so it is not added again. In step 3 the deletion from $D_Y$ puts $(X, Y)$ back, and step 5 then deletes 2 from $X$. The run takes 5 revisions and 23 checks, and the closure $X = 1, Y = 2, Z = 3$ is the only solution. On the same input, AC-4 makes 36 checks, because its set-up step tests all 9 pairs on each of the 4 arcs.

Arc consistency does not decide a CSP. Three variables with domains $\{1, 2\}$ and the constraints $X \ne Y$, $Y \ne Z$, $X \ne Z$ are already arc consistent, so AC-3 deletes nothing and returns true. The problem has no solution, because it asks for a proper 2-colouring of a triangle.

## Correctness

AC-3 returns true exactly when the arc consistency closure of the input has no empty domain, and then the domains it leaves are that closure. The proof has three parts. First, REVISE never deletes a value of the closure, because a value of the closure has a support inside the closure. Second, an arc that is not in the queue is consistent: REVISE$(i, j)$ makes $(i, j)$ consistent, and a deletion from $D_i$ can break only the arcs $(k, i)$, which line L8 puts back, or $(j, i)$, which the argument above shows is safe. So when the queue is empty the domains are arc consistent, and they contain the closure, so they are the closure. Third, the loop stops because each revision either deletes a value or makes the queue shorter. The full proof is below.

Since the closure is unique, the order in which line L4 takes arcs from the queue does not change the result. It changes only the number of checks.

## Complexity

**Revisions.** The queue starts with $2e$ arcs. An arc $(k, i)$ enters the queue again only at line L8, after a revision has deleted a value of $D_i$. The domain $D_i$ loses values at most $d$ times, and each time line L8 adds at most $\deg(i) - 1$ arcs. So the number of arcs added after the start is at most $\sum_i d \deg(i) = 2 e d$. Each arc is removed from the queue once for each time it was added, so there are at most $2e + 2ed = 2e(d+1)$ revisions.

**Checks.** REVISE$(i, j)$ tests at most $|D_i| \cdot |D_j| \le d^2$ pairs. So AC-3 makes at most $2e(d+1)d^2 = O(e d^3)$ checks in the worst case, and with a constant-time membership test the time is $O(e d^3)$ too. This is the bound of Mackworth and Freuder (1985).

**Space.** The queue holds at most $2e$ arcs, a flag for each arc records whether it is in the queue, and the domains take $O(nd)$ space. The extra space is $O(e + nd)$, besides the relations of the input.

The $d^3$ comes from REVISE starting its search for a support from the first value of $D_j$ each time. AC-4 and AC2001 avoid this and run in $O(e d^2)$ time, which is optimal (see [AC-4](/ac-4/)).

## Properties

- **Exact.** It computes the arc consistency closure, not an approximation of it.
- **Order independent.** Any order of the queue gives the same domains.
- **Coarse grained.** The queue holds arcs, not single deleted values. This makes AC-3 simple and its memory small.
- **Incremental.** If AC-3 has run and some values are then deleted (for example by a search decision), it is enough to start with the queue of the arcs $(k, i)$ whose $D_i$ changed. This is how [maintaining arc consistency](/maintaining-arc-consistency/) uses it.
- **Not complete.** An arc consistent CSP can have no solution, as the triangle above shows.

## Variants and improvements

- **AC-1.** Revise all $2e$ arcs, and repeat until a full pass deletes nothing. Each pass makes at most $2ed^2$ checks and at most $nd$ passes delete something, so AC-1 costs $O(n e d^3)$.
- **AC-4.** Count the supports of each value on each arc, and keep lists of the values each value supports. Time $O(e d^2)$, which is optimal, but space $O(e d^2)$ too. See [AC-4](/ac-4/).
- **AC-6 and AC2001.** AC-6 (Bessière 1994) keeps one current support for each value. AC2001, also called AC-3.1, keeps the AC-3 queue of arcs and remembers for each value and arc the last support found, so that REVISE never tests a pair twice. Both run in $O(e d^2)$ time; AC2001 needs $O(e d)$ extra space.
- **Generalized arc consistency (GAC-3).** For a constraint of arity $r$, the queue holds pairs (variable, constraint), and REVISE looks for a supporting tuple. With $m$ constraints of arity at most $r$ there are at most $mr + mr(r-1)d$ revisions, and each tests at most $d^r$ tuples, so GAC-3 makes $O(m r^2 d^{r+1})$ tuple checks.
- **Bounds consistency.** For numeric domains and arithmetic constraints, REVISE can change only the ends of each interval. See [bounds consistency](/bounds-consistency/).
- **Stronger filtering.** [Path consistency](/path-consistency/) (computed by [PC-2](/pc-2/)) and [singleton arc consistency](/singleton-arc-consistency/) delete more values, at a higher cost.

## When to use it

Use AC-3 before a search and at each node of a search, as in [maintaining arc consistency](/maintaining-arc-consistency/). It is short, it needs little memory, and its queue makes it fast when only a few domains change. For a tree-shaped constraint graph, one pass of directional arc consistency is enough to solve the problem without backtracking (see [tree-structured CSP algorithm](/tree-structured-csp/)). For large domains, use AC2001 or AC-6, which keep the queue but drop the $d^3$ term. For constraints that are not binary, use the GAC form, or a filtering algorithm made for the constraint, such as [Régin's filtering](/regin-all-different-filtering/) for [all-different](/all-different-constraint/).

## Pitfalls

- **Adding the arc the wrong way round.** A deletion from $D_i$ requires the arcs $(k, i)$, which point into $i$, to be revised again. Re-adding $(i, k)$ is wrong: those arcs cannot lose consistency when $D_i$ shrinks.
- **Taking a value as consistent because it was once.** A value supported at one time can lose its support later. The queue is what records this, so an arc must go back in the queue after each deletion from its target.
- **Reading true as "has a solution".** True means only that the closure has no empty domain. The triangle with two colours is arc consistent and has no solution.
- **Using the domains after a false answer.** When line L6 returns false, the other domains are not the closure. Use them only to conclude that there is no solution.
- **Two constraints on the same pair.** Revising each one separately is still correct, but the bound counts edges of the graph. Intersect them first.
- **Deleting while iterating.** REVISE collects the deleted values in $G$ and removes them after the loop. Removing from $D_i$ while the loop of line L11 runs over it breaks the iteration in many languages.

## Implementations

## History

Waltz used a filtering procedure of this kind to label line drawings, and Mackworth (1977) placed it in a general setting. Mackworth named node, arc and path consistency and gave the algorithms AC-1, AC-2 and AC-3. Mackworth and Freuder (1985) proved that AC-3 runs in $O(e d^3)$ time and AC-1 in $O(n e d^3)$. Mohr and Henderson (1986) gave AC-4, with $O(e d^2)$ time. Later algorithms, AC-6 (Bessière 1994) and AC2001 (Bessière, Régin, Yap and Zhang, 2005), reach the same optimal time with less space, and AC2001 keeps the simple queue of AC-3.

## References
