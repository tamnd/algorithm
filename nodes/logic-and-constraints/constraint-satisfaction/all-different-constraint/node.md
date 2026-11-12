---
tag: W319XS
kind: definition
slug: all-different-constraint
name: All-different constraint
aliases:
- alldifferent constraint
- alldiff
- distinct constraint
area: logic-and-constraints/constraint-satisfaction
level: core
summary: Global constraint requiring that the variables in a set take pairwise distinct values. It is the same relation as a clique of binary not-equal constraints, but it allows much stronger propagation.
prereqs: [constraint-satisfaction-problem, global-constraint, arc-consistency]
see_also: [regin-all-different-filtering, bounds-consistency, hall-theorem, bipartite-matching, sudoku, graph-coloring, permanent-computation, constraint-programming]
sources:
  - paper: "Willem-Jan van Hoeve, The alldifferent constraint, a survey, 2001, arXiv:cs/0105015"
    locator: the definition, the binary decomposition, and the comparison of arc consistency on the decomposition, bounds consistency, range consistency and generalized arc consistency
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 6, Global constraints, by Willem-Jan van Hoeve and Irit Katriel (the alldifferent constraint and its propagators)
  - paper: "Jean-Charles Régin, A filtering algorithm for constraints of difference in CSPs, Proceedings of AAAI-94, 1994, pages 362 to 367"
    locator: constraints of difference, the value graph and generalized arc consistency by matching
  - paper: "Jean-François Puget, A fast algorithm for the bound consistency of alldiff constraints, Proceedings of AAAI-98, 1998, pages 359 to 366"
    locator: bounds consistency for alldifferent in O(n log n) time with Hall intervals
  - paper: "Philip Hall, On representatives of subsets, Journal of the London Mathematical Society 10, 1935, pages 26 to 30"
    locator: the marriage theorem (a system of distinct representatives exists if and only if Hall's condition holds)
  - paper: "Leslie G. Valiant, The complexity of computing the permanent, Theoretical Computer Science 8(2), 1979, pages 189 to 201"
    locator: "the permanent of a 0/1 matrix is #P-complete"
---

The all-different constraint on variables $x_1, \ldots, x_n$ says that no two of them take the same value. As a relation it is the same as the conjunction of the $n(n-1)/2$ binary constraints $x_i \ne x_j$, but as a [global constraint](/global-constraint/) it can be propagated much more strongly: [Régin's filter](/regin-all-different-filtering/) removes every value that is in no solution, while [arc consistency](/arc-consistency/) on the binary constraints only removes the value of a variable whose domain is a single value. The constraint is a model of a [bipartite matching](/bipartite-matching/) that covers all variables, and it occurs in [Sudoku](/sudoku/), timetabling, [graph coloring](/graph-coloring/) cliques and permutation problems.

## Definition

Let $x_1, \ldots, x_n$ be variables with finite domains $D(x_1), \ldots, D(x_n)$. The constraint all-different$(x_1, \ldots, x_n)$ is the relation

$$\text{AllDiff} = \{(a_1, \ldots, a_n) \in D(x_1) \times \cdots \times D(x_n) : a_i \ne a_j \text{ for all } 1 \le i < j \le n\}.$$

A *solution* of the constraint is a tuple in this relation. Notation: $n$ is the number of variables of the constraint and $d = \max_i |D(x_i)|$, as on the other pages of this area.

**Value graph.** The value graph is the bipartite graph with the variables on one side, the values $\bigcup_i D(x_i)$ on the other, and an edge $\{x_i, a\}$ for each $a \in D(x_i)$. A tuple is a solution if and only if its $n$ edges form a matching. So the constraint has a solution if and only if the value graph has a matching that covers every variable. By [Hall's theorem](/hall-theorem/) this holds if and only if

$$\Bigl|\bigcup_{x \in S} D(x)\Bigr| \ge |S| \quad \text{for every set } S \subseteq \{x_1, \ldots, x_n\}.$$

A set $S$ with $|\bigcup_{x \in S} D(x)| = |S|$ is a *Hall set*. Its variables use up all of its values, so no variable outside $S$ can take one of them.

**Decompositions.** A *decomposition* of a constraint is a set of smaller constraints, possibly on new variables, with the same solutions on the original variables. The standard one is the *binary decomposition* $C_{\ne} = \{x_i \ne x_j : 1 \le i < j \le n\}$. Others:

- With $n = |\bigcup_i D(x_i)|$ (a permutation), the binary decomposition plus a redundant constraint, such as $\sum_i x_i = \sum_{a} a$, or one counting constraint per value: each value is taken exactly once.
- A Boolean encoding: a 0/1 variable $b_{i,a}$ for "$x_i = a$", with exactly one true $b_{i,a}$ for each $i$ and at most one true $b_{i,a}$ for each $a$. This is how a [SAT](/sat/) solver sees the constraint.

All decompositions have the same solutions. They differ in how much a propagator on the parts can remove before search.

**Levels of propagation.** For one all-different constraint, four levels are standard. *Generalized arc consistency* (GAC) keeps a value if and only if it is in a solution. *Range consistency* asks the same, but the other variables may take any value inside the interval between their bounds. *Bounds consistency* asks it only for the smallest and largest value of each domain, with the other domains replaced by their intervals. *Arc consistency on $C_{\ne}$* checks each pair on its own.

**Fact (what the decomposition sees).** On $x_i \ne x_j$, a value $a \in D(x_i)$ has a support if and only if $D(x_j) \ne \{a\}$ and $D(x_j) \ne \emptyset$. So arc consistency on $C_{\ne}$ removes $a$ from $D(x_i)$ exactly when some other domain is $\{a\}$, and it repeats this until nothing changes. It never uses a Hall set of size 2 or more.

## Examples and non-examples

**A Hall set.** Take $D(x_1) = D(x_2) = \{1, 2\}$ and $D(x_3) = \{1, 2, 3\}$. The set $S = \{x_1, x_2\}$ is a Hall set, so $x_3 = 3$ in every solution. GAC, range consistency and bounds consistency all reduce $D(x_3)$ to $\{3\}$. Arc consistency on $C_{\ne}$ removes nothing, because no domain is a single value. The constraint has 2 solutions, $(1, 2, 3)$ and $(2, 1, 3)$.

**Pigeonhole.** Take $D(x_1) = D(x_2) = D(x_3) = \{1, 2\}$. Hall's condition fails for $S = \{x_1, x_2, x_3\}$ (three variables, two values), so there is no solution, and GAC detects this. Each binary constraint $x_i \ne x_j$ is arc consistent, since $1$ has the support $2$ and $2$ has the support $1$. A search on the decomposition must try the assignments to find out. With $n$ variables and $n - 1$ values, [chronological backtracking](/chronological-backtracking/) on $C_{\ne}$ visits a number of nodes that grows exponentially with $n$, while GAC fails at once.

**A hole in a domain.** Take $D(x_1) = \{2\}$ and $D(x_2) = \{1, 2, 3\}$. Arc consistency on $C_{\ne}$ and GAC remove 2 from $D(x_2)$. Bounds consistency does not: the bounds 1 and 3 of $D(x_2)$ each have the support $x_1 = 2$, and bounds consistency does not look inside the interval. With the Hall set example above, this shows that bounds consistency and arc consistency on $C_{\ne}$ are incomparable, and GAC is at least as strong as each.

**Larger example.** With $D(x_1) = D(x_2) = \{1, 2\}$, $D(x_3) = \{1, 2, 3, 4\}$, $D(x_4) = \{2, 3, 4\}$ and $D(x_5) = \{3, 5, 6\}$, GAC gives $D(x_3) = D(x_4) = \{3, 4\}$ and $D(x_5) = \{5, 6\}$. The Hall sets are $\{x_1, x_2\}$ with values $\{1, 2\}$, and then $\{x_3, x_4\}$ with values $\{3, 4\}$. The [Régin page](/regin-all-different-filtering/) traces this example through the matching.

**Sudoku.** Each row, column and box of a Sudoku grid is one all-different constraint on 9 cells with values 1 to 9, so a puzzle has 27 such constraints. A puzzle-solving rule such as "naked pair" (two cells of a row with the same two candidates) is a Hall set of size 2. GAC on one of the 27 constraints applies every rule of this kind, of any size, inside that row, column or box.

**Non-example: all-equal or not-all-equal.** The constraint "not all of $x_1, \ldots, x_n$ are equal" is weaker. For $n = 3$ and domains $\{1, 2\}$ it has 6 solutions, while all-different has none.

**Non-example: a global cardinality constraint.** "Each value is used at most twice" is a *global cardinality constraint*. All-different is the special case where each value is used at most once.

**Counting solutions.** The number of solutions is the number of matchings of the value graph that cover all variables. When the domains use exactly $n$ values, this is the permanent of the 0/1 matrix $A_{ia} = [a \in D(x_i)]$, and computing it is #P-complete (Valiant 1979). See [permanent computation](/permanent-computation/). Deciding whether a solution exists is a matching problem and takes polynomial time.

## Related definitions

- [Régin's all-different filtering](/regin-all-different-filtering/) is the algorithm that reaches GAC for this constraint in $O(n^{3/2} d)$ time with a maximum matching. This page is about the constraint and its decompositions; that page is about the filter and its proof.
- [Global constraint](/global-constraint/): all-different is the standard example of a constraint whose own propagator is stronger than any propagation on its binary decomposition.
- [Bounds consistency](/bounds-consistency/): Puget (1998) gives bounds consistency for all-different in $O(n \log n)$ time.
- [Arc consistency](/arc-consistency/) and [constraint propagation](/constraint-propagation/): the general propagation framework in which these levels sit.
- [Hall's theorem](/hall-theorem/) and [bipartite matching](/bipartite-matching/): the combinatorics behind the constraint.
- [Symmetry breaking](/symmetry-breaking/): permutation problems with an all-different constraint often have value symmetries.

## References
