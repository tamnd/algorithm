---
tag: FD99F0
kind: technique
slug: constraint-propagation
name: Constraint propagation
aliases:
- domain filtering
- inference in CSP
- propagation to a fixpoint
area: logic-and-constraints/constraint-satisfaction
level: core
summary: Repeatedly prunes domains using local consistency rules until a fixpoint, shrinking the search space before or during search.
prereqs: [constraint-satisfaction-problem, arc-consistency]
see_also: [ac-3, ac-4, maintaining-arc-consistency, forward-checking, unit-propagation, bounds-consistency, global-constraint, fixed-point]
sources:
  - paper: "Krzysztof R. Apt, The essence of constraint propagation, Theoretical Computer Science 221(1-2), 1999, pages 179 to 210"
    locator: the generic chaotic iteration algorithm, and the theorem that monotone and inflationary functions reach the same least common fixpoint in any fair order (stated there on the reverse order of domains)
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 3, Constraint propagation, by Christian Bessière (local consistencies, propagators, the fixpoint and the propagation engine)
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 3, Consistency-enforcing algorithms, and Chapter 4, Directional consistency
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, 2020
    locator: Chapter 6, Section 6.2, Constraint propagation, inference in CSPs
  - paper: doi:10.1016/0004-3702(77)90007-8
    title: Alan K. Mackworth, Consistency in networks of relations, Artificial Intelligence 8(1), 1977
    locator: pages 99 to 118 (node, arc and path consistency as propagation)
---

Constraint propagation is the technique of shrinking the domains of a [constraint satisfaction problem](/constraint-satisfaction-problem/) by local rules, each of which deletes values that cannot be part of a solution, and of running the rules again until none of them changes anything. The point where it stops is a [fixed point](/fixed-point/) of all the rules, and for monotone rules it does not depend on the order in which they run. [Arc consistency](/arc-consistency/) is the main case, computed by [AC-3](/ac-3/) or [AC-4](/ac-4/); [unit propagation](/unit-propagation/) in SAT solvers and bounds propagation on numbers are others.

## In plain words

Each unknown has a list of values that are still possible. Each rule looks at a few unknowns and deletes values that it can prove are impossible: if the sum must be ten and one unknown is at most five, the other must be at least five. A deletion can make another rule able to delete more, so a to-do list keeps the rules that must run again.

The process stops when no rule can delete anything, or when some list becomes empty, which proves that there is no solution. Propagation is not a full solver. It is fast and it cuts down the search, so solvers run it before the search and again after each guess.

## When it applies

Use propagation when:

- the problem is a CSP with finite domains, or with intervals of numbers, and each constraint has a cheap rule that deletes unsupported values;
- a search will follow, and fewer values mean fewer branches;
- you want to detect some unsolvable instances early, without a complete search.

A rule here is a *propagator*: a function $f$ that maps domains $D = (D_1, \ldots, D_n)$ to smaller or equal domains. The fixpoint theory below needs three properties of each propagator.

- **Contracting.** $f(D) \subseteq D$, that is $f(D)_i \subseteq D_i$ for each $i$.
- **Monotone.** $D \subseteq D'$ implies $f(D) \subseteq f(D')$.
- **Correct.** If $s$ is a solution with $s_i \in D_i$ for each $i$, then $s_i \in f(D)_i$ for each $i$.

Each propagator belongs to one constraint, and it reads and changes only the domains of the variables of that constraint.

Notation: $n$ variables, $m$ constraints ($e$ when they are binary), $d$ the largest domain size, $r$ the largest arity.

## The template

```pseudo
PROPAGATE(D, F)                    ▷ F is a finite set of propagators
1  Q ← F
2  while Q ≠ ∅ do
3      remove a propagator f from Q
4      D' ← f(D)
5      if some D'_i = ∅ then return fail
6      if D' ≠ D then
7          add to Q each g ∈ F that reads a variable i with D'_i ≠ D_i
8          D ← D'
9  return D
```

Line 7 must also add $f$ itself when $f$ is not idempotent, that is when $f(f(D))$ can differ from $f(D)$.

**Theorem (a unique result).** Let every propagator in $F$ be contracting and monotone, and let $D^0$ be the input domains. Then there is a largest $G \subseteq D^0$ with $f(G) = G$ for all $f \in F$. PROPAGATE stops, and it returns $G$, or fail exactly when $G$ has an empty domain. If every propagator is also correct, $G$ contains every solution.

*Proof.* If $f(A) = A$ and $f(B) = B$, then by monotonicity $f(A \cup B) \supseteq f(A) \cup f(B) = A \cup B$, and by contraction $f(A \cup B) \subseteq A \cup B$. So the union of common fixpoints is a common fixpoint. The all-empty domains are a common fixpoint, and there are finitely many subdomains of $D^0$, so the union $G$ of all common fixpoints inside $D^0$ is the largest one. While the loop runs, $G \subseteq D$: this holds at the start, and if $G \subseteq D$ then $G = f(G) \subseteq f(D)$. Each change at line 8 deletes at least one value, so there are at most $\sum_i |D^0_i|$ changes; between two changes each iteration takes one propagator from $Q$ and adds none, so the loop stops. When it stops with $Q = \emptyset$, every propagator has run on the current $D$ since the last change that could affect it, so $f(D) = D$ for all $f$ (this uses line 7 and the note on idempotence). Then $D \subseteq G$ by maximality, and $D = G$. If line 5 returns fail, some $D'_i$ is empty, and $G \subseteq D'$ (by the same argument as for $D$), so $G_i$ is empty. Correct propagators keep each solution $s$ inside $D$ at every step, so $s$ lies in $G$. $\square$

This is the chaotic iteration theorem of Apt (1999), written for domains that shrink. It is why the order of the queue in [AC-3](/ac-3/) does not change its result, and why each consistency below has a unique *closure*.

**The cost.** The loop runs a propagator at most $(1 + \text{number of changes}) \cdot |F|$ times in the crude count, and at most $|F| + \sum_i \deg(i) \cdot d$ times when a change of $D_i$ re-queues only the $\deg(i)$ propagators that read $x_i$. A fast propagator, an incremental one that works on the change and not on the whole domain, and a good queue order make the difference in practice.

## Classic examples

- **Arc consistency.** For each arc $(i, j)$ of a binary constraint, the propagator deletes the values of $D_i$ that have no support in $D_j$. The fixpoint is the arc consistency closure. [AC-3](/ac-3/) is the template with arcs as propagators, in $O(e d^3)$ time; [AC-4](/ac-4/) uses support counters and runs in the optimal $O(e d^2)$ time.
- **Unit propagation.** On a clause, generalized arc consistency deletes a value only when all other literals of the clause are false, which is [unit propagation](/unit-propagation/). It runs in time linear in the formula size with counters, and with two watched literals in [SAT](/sat/) solvers.
- **Bounds propagation.** For $x + y = 10$ with $x \in [0, 8]$ and $y \in [0, 5]$, the rule $x \ge 10 - \max y$ gives $x \in [5, 8]$, and $y \ge 10 - \max x$ gives $y \in [2, 5]$. Running the rules again changes nothing. See [bounds consistency](/bounds-consistency/) and [interval constraint propagation](/interval-constraint-propagation/).
- **All-different.** The binary form $x_i \ne x_j$ deletes a value only when another variable is fixed to it. [Régin's filtering](/regin-all-different-filtering/) for the [all-different constraint](/all-different-constraint/) achieves GAC with matchings, and finds, for example, that 3 variables with domain $\{1, 2\}$ cannot all differ.
- **Path consistency.** The propagator for a triple $(i, k, j)$ deletes pairs from $R_{ij}$ that have no extension to $x_k$. [PC-2](/pc-2/) runs it to the fixpoint. On the [simple temporal problem](/simple-temporal-problem/), path consistency is the Floyd-Warshall algorithm and decides the problem.
- **Forward checking.** After each assignment in a search, delete the values of the unassigned neighbours that conflict with it. This is one round of arc consistency on the arcs into the new variable, not a fixpoint. See [forward checking](/forward-checking/).

## Variations

- **Propagation during search.** [Maintaining arc consistency](/maintaining-arc-consistency/) runs propagation after each decision of a backtracking search, and undoes it on backtrack.
- **Stronger consistencies.** [Path consistency](/path-consistency/), [k-consistency](/k-consistency/) and [singleton arc consistency](/singleton-arc-consistency/) delete more, at a higher cost. Each strong enough consistency is a complete solver on some class: arc consistency on trees ([Freuder's theorem](/freuder-theorem/)), strong path consistency on binary Boolean constraints.
- **Weaker consistencies.** [Node consistency](/node-consistency/) uses unary constraints only. Bounds consistency checks only the ends of each interval.
- **Directional propagation.** Enforce consistency along one order of the variables only. Directional arc consistency solves trees ([tree-structured CSP algorithm](/tree-structured-csp/)), and adaptive consistency along an order is [bucket elimination](/bucket-elimination/).
- **Propagation for global constraints.** Each [global constraint](/global-constraint/) has its own filtering algorithm, often based on matchings, flows or dynamic programming.
- **Event-based engines.** Real solvers wake a propagator only on the events it cares about, such as "a bound changed" or "the variable is fixed", and run cheap propagators before costly ones.

## Pitfalls

- **Taking the fixpoint as a solution.** A CSP can be at the fixpoint, with no empty domain, and have no solution. The 2-colouring of a triangle is arc consistent.
- **A non-monotone rule.** If a rule is not monotone, the result can depend on the order, and the theorem above does not hold. A rule that reads the size of a domain, for example "if $|D_y| \ge 2$ then delete 1 from $D_x$", is not monotone.
- **A rule that is not idempotent.** If $f(f(D)) \ne f(D)$ is possible, $f$ must re-queue itself after a change, or the result is not a fixpoint of $f$.
- **An incorrect rule.** A rule that deletes a value of some solution makes the solver miss solutions. Test each propagator against brute force on small domains.
- **Slow convergence on intervals.** On real intervals, a rule pair such as $x = y$ and $x = y/2 + 1$ can shrink the bounds by small steps for a long time. Interval solvers stop when the change is below a threshold.
- **Forgetting to undo.** Inside a search, the domains must be restored on backtrack, by a trail of changes or by copying.

## Exercises

1. Prove that the union of two common fixpoints of contracting and monotone propagators is a common fixpoint. Give two non-monotone propagators on two variables for which the two orders of running them give different fixpoints.
2. Show that generalized arc consistency on a clause $\ell_1 \vee \cdots \vee \ell_r$ deletes a value exactly when unit propagation assigns the variable.
3. Take $n + 1$ variables with domain $\{1, \ldots, n\}$ and the constraint $\ne$ on each pair. Show that for $n \ge 2$ the problem is arc consistent and has no solution, and that GAC on one all-different constraint detects this.
4. For $x + y = 10$, $x - y = 2$, $x, y \in [0, 10]$, run bounds propagation by hand to its fixpoint. Is the fixpoint the single solution?
5. Show that with the re-queue rule of line 7 restricted to the $\deg(i)$ propagators that read $x_i$, the number of propagator runs is at most $|F| + d \sum_i \deg(i)$.

## References
