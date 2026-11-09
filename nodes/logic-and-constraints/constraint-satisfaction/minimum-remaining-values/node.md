---
tag: BBYD6D
kind: concept
slug: minimum-remaining-values
name: Minimum remaining values heuristic
aliases:
- MRV
- fail-first
- fail-first heuristic
- most constrained variable
- smallest domain first
- dom
area: logic-and-constraints/constraint-satisfaction
level: core
summary: A dynamic variable ordering for backtracking search on a CSP. It assigns next the unassigned variable with the fewest values left in its current domain, a form of the fail-first principle.
prereqs: [constraint-satisfaction-problem, forward-checking, variable-ordering-heuristics]
see_also: [degree-heuristic, least-constraining-value, maintaining-arc-consistency, chronological-backtracking, graph-coloring, n-queens-problem, branching-rule, search-tree-pruning]
sources:
  - paper: doi:10.1016/0004-3702(80)90051-X
    title: Robert M. Haralick and Gordon L. Elliott, Increasing tree search efficiency for constraint satisfaction problems, Artificial Intelligence 14(3), 1980
    locator: pages 263 to 313 (the fail-first principle, the smallest-domain ordering with forward checking, and its analysis and experiments)
  - paper: doi:10.1145/361219.361224
    title: James R. Bitner and Edward M. Reingold, Backtrack programming techniques, Communications of the ACM 18(11), 1975
    locator: pages 651 to 656 (search rearrangement, choosing next the variable with the fewest remaining choices)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, 4th edition, Pearson, 2020
    locator: Chapter 6, Constraint satisfaction problems, variable and value ordering (minimum remaining values, the degree heuristic as a tie-breaker)
  - paper: "Barbara M. Smith and Stuart A. Grant, Trying harder to fail first, Proceedings of ECAI-98, 1998, pages 249 to 253"
    locator: experiments showing that a heuristic that fails sooner does not always give a smaller search tree
  - paper: "Frédéric Boussemart, Fred Hemery, Christophe Lecoutre and Lakhdar Sais, Boosting systematic search by weighting constraints, Proceedings of ECAI 2004, pages 146 to 150"
    locator: the dom/wdeg heuristic, which divides the domain size by a weighted degree learned from failures
---

The minimum remaining values heuristic (MRV) is a rule for choosing the next variable in a backtracking search for a [CSP](/constraint-satisfaction-problem/): choose the unassigned variable whose current domain has the fewest values. The current domain is what remains after the search's own filtering, such as [forward checking](/forward-checking/) or [arc consistency](/maintaining-arc-consistency/). Haralick and Elliott (1980) named the idea behind it the *fail-first principle*: "to succeed, try first where you are most likely to fail". A variable with one value left is forced, and a variable with no value left shows a dead end at once. MRV is a heuristic. It never changes the set of solutions, only the size of the search tree, and the gains reported for it are measurements.

## In plain words

When you fill in a puzzle, start with the square that has the fewest possible entries left. If a square has only one possible entry, write it now. If a square has none, you have already made a mistake, and it is better to find out now than after ten more steps.

MRV does exactly this at every step of the search. After each choice, it looks at how many values each open variable still has, and it picks the one with the fewest. Because it decides again at every step, the order changes as the search goes on.

## The idea

**The rule.** At a node of the search with the set $U$ of unassigned variables and current domains $D'(x)$, MRV selects

$$x^* = \arg\min_{x \in U} |D'(x)| .$$

Ties are broken by a second rule, most often the [degree heuristic](/degree-heuristic/) (the most constraints with unassigned variables), and then by a fixed order. With plain backtracking and no filtering, $D'(x)$ is the set of values consistent with the current assignment, which the search must compute. With forward checking or MAC the filtered domains are already there, so MRV costs only $O(n)$ for each choice, or less with a priority queue.

**Why it helps.** Two effects work together.

- *Forced moves first.* A variable with $|D'(x)| = 1$ has no real choice, so assigning it first adds no branching and spreads its effect to the other domains early. A variable with $|D'(x)| = 0$ is a dead end that MRV finds at once.
- *Small branching near the root.* The number of nodes of a tree is roughly the product of the branching factors along the paths. Putting small domains near the root keeps this product small when the search must explore the whole tree, as on unsatisfiable problems.

Haralick and Elliott gave a probabilistic argument for fail-first. Smith and Grant (1998) tested it: they built heuristics that fail even sooner than MRV and found that they do not always give smaller trees. So MRV works well in practice, but the reason "it fails first" is only part of the story.

**What it does not change.** MRV is a variable order, so it keeps the search sound and complete. It can change the first solution found, and the number of nodes, but not the set of solutions.

**Variants.**

- **dom/deg.** Divide the domain size by the degree of the variable, and choose the smallest ratio (Bessière and Régin, 1996).
- **dom/wdeg.** Give each constraint a weight that grows by 1 each time it causes a dead end, and divide the domain size by the total weight of the constraints on the variable (Boussemart, Hemery, Lecoutre and Sais, 2004). This learns from the search where the hard part of the problem is.
- **DSATUR.** In [graph coloring](/graph-coloring/), Brélaz's [DSATUR](/dsatur/) rule chooses the vertex whose neighbours already use the most different colors. This is MRV for coloring, with ties broken by degree.

## Examples

**4-queens with forward checking.** After $x_1 = 1$, forward checking leaves $x_2 \in \{3, 4\}$, $x_3 \in \{2, 4\}$ and $x_4 \in \{2, 3\}$. All three have 2 values, so MRV breaks the tie by index and picks $x_2$. After $x_2 = 3$, forward checking empties the domain of $x_3$ at once, and the search backs up. The trace on the [forward checking](/forward-checking/) page shows the rest.

**Measured on n-queens.** These counts are from a forward checking search written for this page, counting value assignments until the first solution. "Static" assigns $x_1, x_2, \ldots$ in order, and values are tried in increasing order.

| $n$ | static order | MRV | MRV with [least constraining value](/least-constraining-value/) |
|---|---|---|---|
| 8 | 88 | 75 | 39 |
| 12 | 193 | 153 | 32 |
| 16 | 7560 | 44 | 332 |
| 20 | 145151 | 145 | 31 |
| 25 | 32840 | 275 | 25 |
| 30 | more than 300000 | 147 | 68 |

The static order is very sensitive to $n$, while MRV stays small. The numbers are for one value order and one tie-breaking rule. They are not a bound, and other orders give other numbers.

**Measured on random CSPs.** For 60 random binary CSPs with 20 variables, 8 values, constraint density 0.3 and tightness 0.38 (seed 1980), forward checking needed on average 30540 assignments with the static order and 49 with MRV. At tightness 0.45, near the hardest region, where 46 of the 60 instances had a solution, MRV needed 285 on average, and MRV with the degree heuristic as a tie-breaker needed 122.

## Where it is used

- In almost every CP solver as the default or a basic variable order, often as dom/wdeg or a related rule.
- In textbook backtracking with forward checking, such as the solvers of Russell and Norvig.
- In graph coloring as DSATUR, and in Sudoku and similar puzzles, where it amounts to "fill the cell with the fewest candidates".
- In SAT, the unit rule of [DPLL](/dpll/) is the extreme case: a clause with one free literal is a variable with one value left, and it is assigned before any decision.

## References
