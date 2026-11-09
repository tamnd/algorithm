---
tag: X51QNF
kind: concept
slug: least-constraining-value
name: Least constraining value heuristic
aliases:
- LCV
- value ordering heuristic
- succeed-first
- min-conflicts value ordering
area: logic-and-constraints/constraint-satisfaction
level: core
summary: A value ordering for CSP search. It tries first the value of the chosen variable that removes the fewest values from the domains of its unassigned neighbours.
prereqs: [constraint-satisfaction-problem, forward-checking, minimum-remaining-values]
see_also: [minimum-remaining-values, degree-heuristic, maintaining-arc-consistency, min-conflicts, variable-ordering-heuristics, n-queens-problem, graph-coloring, chronological-backtracking]
sources:
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, 4th edition, Pearson, 2020
    locator: Chapter 6, Constraint satisfaction problems, variable and value ordering (the least constraining value, and why value order matters only for the first solution)
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 5, General search strategies, look-ahead (value ordering by look-ahead)
  - paper: "Pieter A. Geelen, Dual viewpoint heuristics for binary constraint satisfaction problems, Proceedings of ECAI-92, 1992, pages 31 to 35"
    locator: the promise of a value, the product of the remaining domain sizes of the other variables
  - paper: "Daniel Frost and Rina Dechter, Look-ahead value ordering for constraint satisfaction problems, Proceedings of IJCAI-95, 1995, pages 572 to 578"
    locator: experiments with value orderings that count or weigh the values a choice removes
---

The least constraining value heuristic (LCV) orders the values of a variable in a backtracking search for a [CSP](/constraint-satisfaction-problem/). After the variable $x$ is chosen, for example by [minimum remaining values](/minimum-remaining-values/), LCV tries first the value that removes the fewest values from the current domains of the unassigned neighbours of $x$. A variable order follows the *fail-first* idea, but a value order follows the opposite, *succeed-first* idea: try first the value most likely to lead to a solution. LCV can only help a search that stops at the first solution. When the search must explore the whole tree, because the problem has no solution or all solutions are wanted, the order of the values does not change the size of the tree. It is a heuristic, and its gains are measurements.

## In plain words

You have chosen which question to answer next. Now pick the answer that leaves the most options open for the other questions. If one answer would rule out five options for the neighbours and another only one, try the second first.

This makes sense only when you want one solution. If you must try every answer anyway, for example to prove that there is no solution, the order in which you try them does not matter, because you try them all.

## The idea

**The rule.** Let $x$ be the chosen variable, $U$ the set of other unassigned variables and $D'(y)$ the current domains. For a value $a \in D'(x)$, let

$$\operatorname{removed}(a) = \sum_{y \in U} \bigl|\{ b \in D'(y) : \text{the assignment } x = a \text{ rules out } y = b \}\bigr| ,$$

where "rules out" means that a constraint on $x$ and $y$ (and on assigned variables only) is violated by $x = a, y = b$. LCV tries the values of $x$ in increasing order of $\operatorname{removed}(a)$, with ties broken by a fixed order. For binary constraints this is the number of values that [forward checking](/forward-checking/) would remove after $x = a$.

**Variants of the score.**

- *Promise* (Geelen, 1992): order by the product $\prod_{y \in U} |D'(y) \setminus \text{removed by } a|$, largest first. This counts the number of combinations that are left, and it gives value 0 to a choice that empties a domain.
- *Smallest minimum domain*: prefer the value whose worst neighbour domain is largest, which avoids values that leave some neighbour with one value.
- *Look-ahead with stronger filtering*: compute the score after [arc consistency](/maintaining-arc-consistency/) instead of forward checking, which costs more but sees further (Frost and Dechter, 1995).

**Why value order matters only for the first solution.** With chronological backtracking and no learning, the subtree below $x = a$ depends only on the assignment made so far, not on which sibling values were tried before. If the search explores all values of $x$, it explores the same set of subtrees in any order, so the tree has the same size. This holds when the problem has no solution and when all solutions are counted. When the search stops at the first solution, only the values before the first good value are explored, and a good order makes this prefix short. So LCV is useless for proving that a problem has no solution, and on problems near the threshold, where many instances have no solution, its gain is small.

**Cost.** Computing $\operatorname{removed}(a)$ for all values of $x$ takes $O(d \cdot \sum_{y} d)$ constraint checks for binary constraints with domains of size $d$, at every node. With forward checking, much of this work is the same as the filtering that follows the choice, so the cost can be shared.

**Relation to min-conflicts.** The [min-conflicts](/min-conflicts/) local search uses a similar value rule on a full assignment: it gives a variable the value with the fewest violated constraints. LCV counts values removed from domains in a partial assignment, so the two are related but not the same.

## Examples

**The map of Australia.** Color with red, green and blue. After WA is red and NT is green, the variable Q is next, with the domain $\{\text{red}, \text{blue}\}$, and SA has only $\{\text{blue}\}$ left. The value $Q = \text{red}$ removes red from the domain of NSW, which is 1 value. The value $Q = \text{blue}$ removes blue from SA and from NSW, which is 2 values, and it empties the domain of SA. LCV tries red first, and the search goes on without a dead end.

**Measured on n-queens.** These counts are from a forward checking search written for this page, counting value assignments until the first solution, with MRV as the variable order.

| $n$ | MRV, values in increasing order | MRV with LCV |
|---|---|---|
| 8 | 75 | 39 |
| 12 | 153 | 32 |
| 16 | 44 | 332 |
| 20 | 145 | 31 |
| 25 | 275 | 25 |
| 30 | 147 | 68 |

LCV helped for five of the six sizes, and for $n = 16$ it made the search more than 7 times larger. A value order is a guess about where the solutions are, and a guess can be wrong.

**Measured on random CSPs.** For 60 random binary CSPs with 20 variables, 8 values and constraint density 0.3 (seed 1980), the mean number of assignments was:

| tightness | solvable | MRV | MRV with LCV |
|---|---|---|---|
| 0.38 | 60 of 60 | 49.1 | 25.3 |
| 0.45 | 46 of 60 | 284.7 | 259.1 |

At tightness 0.38 every instance had a solution and LCV halved the mean. At 0.45 the 14 instances with no solution took the same number of assignments with and without LCV, as the argument above says, and the mean gain was small. The counts do not include the extra constraint checks that LCV makes.

## Where it is used

- In textbook CSP solvers together with MRV and the [degree heuristic](/degree-heuristic/), for example in Russell and Norvig.
- In CP solvers as a value selection option, often in the cheaper forms "smallest value", "middle value" or a value chosen by a problem-specific rule, since the full count is costly.
- In scheduling and timetabling, where the value that leaves the most room for the other tasks is a natural first choice.
- In [graph coloring](/graph-coloring/), where the least constraining color is the color used least among the uncolored neighbours' options.

## References
