---
tag: NS3N1K
kind: concept
slug: arc-consistency
name: Arc consistency
aliases:
- 2-consistency
- generalized arc consistency
- GAC
- domain consistency
- hyper-arc consistency
area: logic-and-constraints/constraint-satisfaction
level: core
summary: Each value in a variable's domain must have a supporting value in every neighboring domain under each binary constraint.
prereqs: [constraint-satisfaction-problem, constraint-graph, node-consistency]
see_also: [ac-3, ac-4, constraint-propagation, path-consistency, singleton-arc-consistency, bounds-consistency, maintaining-arc-consistency, freuder-theorem]
sources:
  - paper: doi:10.1016/0004-3702(77)90007-8
    title: Alan K. Mackworth, Consistency in networks of relations, Artificial Intelligence 8(1), 1977
    locator: pages 99 to 118 (the definitions of node, arc and path consistency)
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 3, Consistency-enforcing algorithms (arc consistency, generalized arc consistency and the closure)
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 3, Constraint propagation, by Christian Bessière (arc consistency, generalized arc consistency and the fixpoint view)
  - paper: "Krzysztof R. Apt, The essence of constraint propagation, Theoretical Computer Science 221(1-2), 1999, pages 179 to 210"
    locator: chaotic iteration of monotone and inflationary functions, and the uniqueness of the common fixpoint
  - paper: "Kostas Stergiou and Toby Walsh, Encodings of non-binary constraint satisfaction problems, Proceedings of AAAI 1999"
    locator: the result that arc consistency on the hidden variable encoding equals generalized arc consistency on the original problem
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, 2020
    locator: Chapter 6, Section 6.2 (node, arc, path and k-consistency)
---

Arc consistency is a property of the domains of a [constraint satisfaction problem](/constraint-satisfaction-problem/): every value of every variable has, for each constraint on that variable, a value of the other variable that the constraint allows with it. For constraints of any arity the same idea is called generalized arc consistency (GAC). Each CSP has a unique largest arc consistent set of subdomains, its arc consistency closure, and it contains every solution. The algorithms [AC-3](/ac-3/) and [AC-4](/ac-4/) compute this closure, and [constraint propagation](/constraint-propagation/) is the general technique of which it is the most used case.

## In plain words

Each variable has a list of possible values. Each constraint links two variables and says which pairs of values may go together. A value is arc consistent if, for each constraint on its variable, at least one value of the other variable goes with it. If a value has no partner on some constraint, no solution can use it, so we can delete it.

A problem is arc consistent when no value can be deleted in this way. Deleting one value can take away the only partner of another value, so the deletions must be repeated until nothing changes. The result does not depend on the order of the deletions. Arc consistency is a cheap test. It finds many dead values, but a problem can be arc consistent and still have no solution.

## The idea

**Notation.** A binary CSP has variables $x_1, \ldots, x_n$, finite domains $D_1, \ldots, D_n$ with $|D_i| \le d$, and $e$ binary constraints. A constraint on $x_i$ and $x_j$ is a relation $R_{ij} \subseteq D_i \times D_j$, and $R_{ji}$ is its converse. Each edge $\{i, j\}$ of the [constraint graph](/constraint-graph/) gives the two arcs $(i, j)$ and $(j, i)$. In this area $m$ is the number of constraints, so $m = e$ for a binary CSP.

**Definition.** Let $D'_i \subseteq D_i$ for each $i$. A value $a \in D'_i$ is *supported* on the arc $(i, j)$ if some $b \in D'_j$ has $(a, b) \in R_{ij}$; such a $b$ is a *support* of $a$. The arc $(i, j)$ is *arc consistent* if every value of $D'_i$ is supported on it. The domains $D'$ are arc consistent if every arc is.

**Generalized arc consistency.** Let $C$ be a constraint with scope $(x_{i_1}, \ldots, x_{i_r})$ and relation $R \subseteq D_{i_1} \times \cdots \times D_{i_r}$. A value $a \in D'_{i_k}$ is supported on $C$ if some tuple $t \in R \cap (D'_{i_1} \times \cdots \times D'_{i_r})$ has $t_k = a$. The domains are generalized arc consistent if every value of each variable is supported on every constraint that contains it. For $r = 2$ this is arc consistency. Unary constraints are handled by [node consistency](/node-consistency/), and arc consistency on node consistent domains is the same as 2-consistency in the sense of [k-consistency](/k-consistency/).

**The closure is unique.** Write $D' \subseteq D$ when $D'_i \subseteq D_i$ for each $i$.

> **Proposition.** For each CSP with domains $D$ there is exactly one largest arc consistent $D^\ast \subseteq D$. Every solution $s$ has $s_i \in D^\ast_i$ for each $i$.
>
> *Proof.* Let $D'$ and $D''$ be arc consistent subdomains of $D$, and let $a \in D'_i \cup D''_i$. If $a \in D'_i$, then $a$ has a support $b \in D'_j \subseteq D'_j \cup D''_j$ on each arc $(i, j)$; the case $a \in D''_i$ is the same. So the union $D' \cup D''$ is arc consistent. The all-empty domains are arc consistent, and there are finitely many subdomains, so the union $D^\ast$ of all arc consistent subdomains is arc consistent and contains each of them. Two largest ones would contain each other, so $D^\ast$ is unique. For a solution $s$, the domains $\{s_1\}, \ldots, \{s_n\}$ are arc consistent, since $(s_i, s_j) \in R_{ij}$ on each arc, so $s_i \in D^\ast_i$. $\square$

The same proof works for generalized arc consistency, with tuples in place of pairs. $D^\ast$ is the *arc consistency closure*. To *enforce* arc consistency is to compute it. It can have empty domains; then the CSP has no solution.

**A fixpoint view.** Let $F(D')$ delete from $D'$ each value that is not supported on some arc. $F$ is monotone ($D' \subseteq D''$ gives $F(D') \subseteq F(D'')$) and $F(D') \subseteq D'$. The arc consistent subdomains are the fixpoints of $F$, and $D^\ast$ is the greatest one. By the [Knaster-Tarski theorem](/knaster-tarski-theorem/) a greatest fixpoint exists, and iterating $F$ from $D$ reaches it in at most $nd$ rounds, because each round that changes something deletes a value. Each REVISE of AC-3 applies one part of $F$. Apt (1999) showed that any fair order of such monotone deletion steps reaches the same fixpoint, which is why AC-3 can take its arcs in any order.

**What arc consistency gives and what it does not.**

- *Sound.* It never deletes a value of a solution (the proposition).
- *Not complete.* An arc consistent CSP with no empty domain can have no solution. The 2-colouring of a triangle below is an example.
- *Complete on trees.* If the constraint graph is a tree and the domains are arc consistent and not empty, a solution exists and a search finds it without backtracking. This is [Freuder's theorem](/freuder-theorem/), and the [tree-structured CSP algorithm](/tree-structured-csp/) uses it.
- *Complete for some languages.* For Horn clauses, GAC is [unit propagation](/unit-propagation/), and it decides [Horn-SAT](/horn-sat/).

**How the pages relate.** This page defines the property and its closure. [AC-3](/ac-3/) computes the closure with a queue of arcs in $O(e d^3)$ time. [AC-4](/ac-4/) computes the same closure with support counters in $O(e d^2)$ time, which is optimal. [Constraint propagation](/constraint-propagation/) is the general method of deleting values by local rules until a fixpoint, with arc consistency as its main case. [Forward checking](/forward-checking/) applies only a part of it during search, and [maintaining arc consistency](/maintaining-arc-consistency/) applies all of it at each search node.

## Examples

**A chain.** Take $X, Y, Z \in \{1, 2, 3\}$ with $X < Y$ and $Y < Z$. The value $X = 3$ has no support on $(X, Y)$, $Y = 1$ none on $(Y, X)$, $Y = 3$ none on $(Y, Z)$, and $Z = 1$ none on $(Z, Y)$. After these deletions $Y = 2$ is the only value of $Y$, so $Z = 2$ and $X = 2$ lose their support. The closure is $D_X = \{1\}$, $D_Y = \{2\}$, $D_Z = \{3\}$. The [AC-3](/ac-3/) page traces this run.

**Arc consistent, with no solution.** Take $X, Y, Z \in \{1, 2\}$ with $X \ne Y$, $Y \ne Z$ and $X \ne Z$. Each value of each variable has a support on each arc: 1 is supported by 2, and 2 by 1. So the domains are arc consistent, but no assignment satisfies all three constraints. [Path consistency](/path-consistency/) finds the conflict, because no pair for $(X, Z)$ extends to $Y$.

**GAC is stronger than arc consistency on a binary encoding.** Take the [all-different constraint](/all-different-constraint/) on $X, Y \in \{1, 2\}$ and $Z \in \{1, 2, 3\}$. Written as the three constraints $X \ne Y$, $X \ne Z$, $Y \ne Z$, the domains are arc consistent. As one ternary constraint, the only allowed tuples are $(1, 2, 3)$ and $(2, 1, 3)$, so GAC deletes 1 and 2 from $Z$.

**A non-example of the closure.** Deleting $Y = 2$ from the chain gives smaller domains, but then $X$ and $Z$ lose all support, and the closure becomes empty. Arc consistency asks for the largest consistent subdomains, not any consistent ones: the all-empty domains are arc consistent but say nothing.

**Equations.** Take $x, y \in \{0, \ldots, 9\}$ with $y = x^2$. The supported values are $x \in \{0, 1, 2, 3\}$ and $y \in \{0, 1, 4, 9\}$. Bounds consistency would keep $y \in [0, 9]$, the full interval, because it tests only the ends of the interval. See [bounds consistency](/bounds-consistency/).

## Where it is used

- **Search with propagation.** Constraint solvers run arc consistency or GAC at each node of a backtracking search, as in [maintaining arc consistency](/maintaining-arc-consistency/), and use the closure to choose the next variable (for example by [minimum remaining values](/minimum-remaining-values/)).
- **Global constraints.** A solver gives each [global constraint](/global-constraint/) its own GAC algorithm, such as [Régin's filtering](/regin-all-different-filtering/) for all-different, which runs in polynomial time where the generic method would need time exponential in the arity.
- **SAT solving.** On clauses, GAC is [unit propagation](/unit-propagation/), the inference step of DPLL and CDCL solvers for [SAT](/sat/).
- **Tree-shaped problems.** On a constraint tree, directional arc consistency and one forward pass solve the problem in $O(n d^2)$ time ([tree-structured CSP algorithm](/tree-structured-csp/)), and [cutset conditioning](/cutset-conditioning/) extends this to graphs with a small cycle cutset.
- **Non-binary encodings.** On the hidden variable encoding of a non-binary CSP, arc consistency equals GAC on the original problem (Stergiou and Walsh 1999). See [dual encoding](/dual-graph-transformation/).
- **Stronger consistencies.** [Singleton arc consistency](/singleton-arc-consistency/) runs arc consistency as a test for each value, and [path consistency](/path-consistency/) and [k-consistency](/k-consistency/) extend the idea to pairs and larger sets of variables.
- **Scene labelling.** The first use was the labelling of line drawings by Waltz filtering, which Mackworth (1977) recast as arc consistency.

## References
