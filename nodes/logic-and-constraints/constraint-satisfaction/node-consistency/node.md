---
tag: 9MKW92
kind: concept
slug: node-consistency
name: Node consistency
aliases:
- 1-consistency
area: logic-and-constraints/constraint-satisfaction
level: core
summary: Every value in a variable's domain satisfies all unary constraints on that variable.
prereqs: [constraint-satisfaction-problem]
see_also: [arc-consistency, k-consistency, constraint-propagation, path-consistency, unit-propagation, forward-checking]
sources:
  - paper: doi:10.1016/0004-3702(77)90007-8
    title: Alan K. Mackworth, Consistency in networks of relations, Artificial Intelligence 8(1), 1977
    locator: pages 99 to 118 (node consistency as the first level, before arc and path consistency)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, 2020
    locator: Chapter 6, Section 6.2 (node consistency, with the unary constraint on South Australia in map colouring)
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 3, Consistency-enforcing algorithms (unary constraints and the levels of local consistency)
  - paper: "Eugene C. Freuder, Synthesizing constraint expressions, Communications of the ACM 21(11), 1978, pages 958 to 966"
    locator: the definition of k-consistency, of which node consistency is the case k = 1
---

Node consistency is the simplest local consistency of a [constraint satisfaction problem](/constraint-satisfaction-problem/): a variable is node consistent if every value in its domain satisfies every unary constraint on that variable. It is the case $k = 1$ of [k-consistency](/k-consistency/). A single pass that filters each domain by its unary constraints enforces it, with no propagation between variables, and [arc consistency](/arc-consistency/) and the stronger levels assume it has been done.

## In plain words

Some rules talk about one unknown only: "this value must be even", "this region may not be green". Node consistency means that the list of possible values of each unknown already obeys all such one-unknown rules.

To get there, go through each list once and cross out each value that breaks one of its own rules. Crossing out a value of one unknown cannot break a one-unknown rule of another, so one pass is enough. After that, the one-unknown rules can be thrown away: the lists say everything they said.

## The idea

**Definition.** Let $P$ be a CSP with variables $x_1, \ldots, x_n$ and domains $D_1, \ldots, D_n$. A unary constraint on $x_i$ is a set $U \subseteq D_i$ of allowed values. The variable $x_i$ is *node consistent* if $D_i \subseteq U$ for each unary constraint $U$ on $x_i$, and $P$ is node consistent if every variable is.

**Enforcing it.** Replace each $D_i$ by $D_i \cap \bigcap_U U$, over the unary constraints $U$ on $x_i$. Then drop the unary constraints. With $u$ unary constraints in total and domains of size at most $d$, this takes $O(u d)$ membership tests, and $O(nd)$ when each variable has at most one unary constraint. The result is the largest node consistent subdomains, and it keeps every solution, because a solution satisfies each unary constraint.

**Why one pass is enough.** The filter for $x_i$ reads and changes only $D_i$. So filtering $x_j$ cannot undo the node consistency of $x_i$, and the filters of different variables commute. In the language of [constraint propagation](/constraint-propagation/), each unary filter is idempotent and the filters have disjoint inputs, so their fixpoint is reached after one run of each. Arc consistency differs: a binary constraint links two domains, and a deletion in one can force a deletion in the other.

**Place in the hierarchy.** In the terms of [k-consistency](/k-consistency/), a consistent assignment of zero variables extends to any one variable when each domain has a value that satisfies its unary constraints. So "1-consistent" also asks that no domain be empty after the filter; node consistency is the filter itself. Strong $k$-consistency for any $k \ge 1$ includes it.

Notation: $n$ variables, $m$ constraints, $d$ the largest domain size, $k$ the consistency level.

## Examples

**Map colouring.** In the Australia problem with colours red, green and blue, add the unary constraint "SA is not green". Node consistency deletes green from $D_{SA}$, leaving $\{\text{red}, \text{blue}\}$. The other domains do not change, even though SA has five neighbours. Arc consistency would then do nothing more either, since each colour of a neighbour still has a support.

**A search decision.** In a backtracking search, the decision $x_3 = 5$ is the unary constraint $\{5\}$ on $x_3$. Node consistency makes $D_3 = \{5\}$, and [forward checking](/forward-checking/) or [arc consistency](/arc-consistency/) then carries the effect to the neighbours of $x_3$.

**Unit clauses.** In a CNF formula, a unit clause $x$ or $\neg x$ is a unary constraint. Node consistency fixes the variable; deleting the other literal from the clauses that contain it is then the work of [unit propagation](/unit-propagation/).

**An empty domain.** $x \in \{1, 2, 3\}$ with the unary constraints "$x$ is even" and "$x > 2$" gives $D_x = \emptyset$, so the CSP has no solution. Node consistency finds this without looking at any other variable.

**A non-example.** $x, y \in \{1, 2\}$ with $x < y$. Each variable is node consistent, as there is no unary constraint, but the value $x = 2$ has no partner. Removing it is a matter of arc consistency, not node consistency.

## Where it is used

- **Preprocessing.** Solvers fold unary constraints into the domains before anything else. Many textbooks then define a CSP with binary constraints only, which is possible because of this step.
- **The base of the hierarchy.** [Arc consistency](/arc-consistency/), [path consistency](/path-consistency/) and [k-consistency](/k-consistency/) are defined for node consistent domains, and strong $k$-consistency includes node consistency.
- **Search.** Each decision $x_i = a$ and each refutation $x_i \ne a$ is a unary constraint that the solver applies by node consistency before it propagates.
- **Bucket elimination.** When the constraints in the bucket of a variable mention only one other variable, eliminating the first variable gives a unary constraint on the other, which acts as a filter of its domain ([bucket elimination](/bucket-elimination/)).

## References
