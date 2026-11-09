---
tag: DZ23JN
kind: concept
slug: degree-heuristic
name: Degree heuristic
aliases:
- most constraining variable
- maximum degree ordering
- deg
area: logic-and-constraints/constraint-satisfaction
level: core
summary: A variable ordering for CSP search that picks the unassigned variable in the most constraints with other unassigned variables. It is mostly used to break ties of the MRV heuristic.
prereqs: [constraint-satisfaction-problem, constraint-graph, variable-ordering-heuristics]
see_also: [minimum-remaining-values, least-constraining-value, forward-checking, dsatur, graph-coloring, freuder-theorem, n-queens-problem, chronological-backtracking]
sources:
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, 4th edition, Pearson, 2020
    locator: Chapter 6, Constraint satisfaction problems, variable and value ordering (the degree heuristic as a tie-breaker for minimum remaining values, the map of Australia)
  - paper: doi:10.1145/359094.359101
    title: Daniel Brélaz, New methods to color the vertices of a graph, Communications of the ACM 22(4), 1979
    locator: pages 251 to 256 (the DSATUR rule, with ties of the saturation degree broken by the degree in the uncolored subgraph)
  - paper: doi:10.1145/322290.322292
    title: Eugene C. Freuder, A sufficient condition for backtrack-free search, Journal of the ACM 29(1), 1982
    locator: pages 24 to 32 (the width of an ordering and the minimum width ordering)
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 5, General search strategies, look-ahead (static and dynamic variable orderings, including maximum degree and minimum width)
---

The degree heuristic is a rule for choosing the next variable in a backtracking search for a [CSP](/constraint-satisfaction-problem/): choose the unassigned variable that is involved in the largest number of constraints with other unassigned variables. It looks only at the structure of the problem, the [constraint graph](/constraint-graph/), and not at the current domains. Alone it is a weak rule. Its main use is to break ties of the [minimum remaining values](/minimum-remaining-values/) heuristic (MRV), which looks only at the domains. The idea is that a variable with many open constraints will remove many values when it is assigned, so it is best to decide it early, while the search tree is still small. It is a heuristic, and its gains are measurements, not guarantees.

## In plain words

Look at the map of who constrains whom. Pick the open variable with the most links to other open variables. Choosing it first fixes a lot of the problem at once, so later choices have fewer options and fewer chances to go wrong.

The rule does not look at how many values each variable still has. So it can pick a variable with many choices while another variable has only one choice left. That is why it is mostly used as the second rule, after MRV: among the variables with the fewest values left, pick the one with the most open links.

## The idea

**The rule.** At a search node with the set $U$ of unassigned variables, the dynamic degree of $x \in U$ is

$$\deg_U(x) = \bigl|\{ c \in C : x \in \operatorname{scope}(c) \text{ and } \operatorname{scope}(c) \cap (U \setminus \{x\}) \neq \emptyset \}\bigr| ,$$

the number of constraints on $x$ that also involve another unassigned variable. The degree heuristic selects $x^* = \arg\max_{x \in U} \deg_U(x)$. Constraints whose other variables are all assigned do not count, since after propagation they only restrict the domain of $x$, which MRV already measures.

**As a tie-breaker for MRV.** The usual combined rule is: among the variables with the smallest current domain, choose the one with the largest $\deg_U$, and break any remaining tie by a fixed order. In symbols, minimize the pair $(|D'(x)|, -\deg_U(x))$ in lexicographic order.

**Static form.** Without the restriction to $U$, the degree is fixed, and sorting the variables by decreasing degree once gives a static order, the *maximum degree ordering*. A related static order is Freuder's *minimum width ordering* (1982), which is found by repeatedly removing a vertex of minimum degree and placing it last. On a tree it has width 1, and with arc consistency the search is then backtrack free, see [Freuder's theorem](/freuder-theorem/).

**When it gives no information.** If the constraint graph is complete, as in [n-queens](/n-queens-problem/), every unassigned variable has the same dynamic degree, $|U| - 1$. Then the degree rule is just the fixed order, and MRV with the degree tie-breaker is just MRV. In general the rule helps most on sparse graphs with very different degrees.

**Relation to DSATUR.** In Brélaz's [DSATUR](/dsatur/) rule for [graph coloring](/graph-coloring/), the first criterion is the number of colors used by the neighbours, which is MRV for coloring, and the tie-breaker is the degree in the uncolored subgraph, which is exactly $\deg_U$.

## Examples

**The map of Australia.** Color the seven regions with red, green and blue so that neighbours differ. The constraint graph has the edges WA to NT, WA to SA, NT to SA, NT to Q, SA to Q, SA to NSW, SA to V, Q to NSW and NSW to V, and T has no neighbours.

At the start the degrees are SA 5, NT 3, Q 3, NSW 3, WA 2, V 2 and T 0, so the degree heuristic picks SA, while MRV sees a tie of all seven, since every domain has 3 values. Say SA is red. The open degrees are now NT 2, Q 2, NSW 2, WA 1, V 1, T 0. Pure degree picks NT (first in the tie) and gives it green. Now NSW has open degree 2 and Q has 1, so pure degree picks NSW next, although the domain of Q is already down to $\{\text{blue}\}$. If NSW gets blue, Q has no color left, and the search must back up. MRV with the degree tie-breaker picks Q at that point instead, since its domain has 1 value, and it never meets this dead end.

**Measured on random CSPs.** These counts are from a forward checking search written for this page, counting value assignments until the first solution, with values tried in increasing order. The test set was 60 random binary CSPs with 20 variables, 8 values and constraint density 0.3 (seed 1980).

| tightness | solvable | degree alone | MRV | MRV with degree tie-break |
|---|---|---|---|---|
| 0.38 | 60 of 60 | 426.2 | 49.1 | 38.5 |
| 0.45 | 46 of 60 | 1414.3 | 284.7 | 122.3 |

Degree alone was much worse than MRV, and as a tie-breaker it helped, by more at the harder tightness. On n-queens from 8 to 30, the counts with degree alone were equal to those of the fixed order, and the counts of MRV with the degree tie-breaker were equal to those of MRV, as the argument above predicts. These are measurements on one generator and one implementation, not bounds.

## Where it is used

- As the standard tie-breaker for MRV in textbook CSP solvers, such as the one of Russell and Norvig.
- In DSATUR for graph coloring, and in other greedy coloring rules such as Welsh and Powell's largest degree first.
- As a static order for problems with a sparse constraint graph, and as a first step before search, as in the dom/deg rule of CP solvers, which divides the domain size by the degree.
- In the choice of an elimination order for [bucket elimination](/bucket-elimination/) and for [tree decompositions](/treewidth/), where minimum degree is a common greedy rule.

## References
