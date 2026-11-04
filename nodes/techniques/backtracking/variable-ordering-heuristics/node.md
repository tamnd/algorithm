---
tag: Q454F0
kind: concept
slug: variable-ordering-heuristics
name: Variable ordering heuristics
aliases:
- static and dynamic variable ordering
area: techniques/backtracking
level: core
summary: Rules that choose which variable to assign next, since the order strongly affects the size of the search tree.
prereqs: [constraint-satisfaction-problem, chronological-backtracking, state-space-tree]
see_also: [minimum-remaining-values, degree-heuristic, forward-checking, graph-coloring, branching-rule, search-tree-pruning]
sources:
  - paper: doi:10.1016/0004-3702(80)90051-X
    title: Robert M. Haralick and Gordon L. Elliott, Increasing tree search efficiency for constraint satisfaction problems, Artificial Intelligence 14(3), 1980
    locator: pp. 263 to 313
  - paper: doi:10.1145/361219.361224
    title: James R. Bitner and Edward M. Reingold, Backtrack programming techniques, Communications of the ACM 18(11), 1975
    locator: pp. 651 to 656
  - paper: doi:10.1145/359094.359101
    title: Daniel Brelaz, New methods to color the vertices of a graph, Communications of the ACM 22(4), 1979
    locator: pp. 251 to 256
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 6 (variable and value ordering in backtracking search)
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing
    locator: Chapter 5 (variable ordering heuristics in look-ahead search)
---

Variable ordering heuristics are the rules that choose which variable a backtracking search assigns next. The set of solutions of a [constraint satisfaction problem](/constraint-satisfaction-problem/) does not depend on the order, but the [state space tree](/state-space-tree/) that the search walks does, and its size can change by orders of magnitude. A *static* order is fixed before the search; a *dynamic* order is chosen again at each node from the current state. The best known rule is the dynamic [minimum remaining values](/minimum-remaining-values/) rule, also called fail-first, often with the [degree heuristic](/degree-heuristic/) to break ties.

## In plain words

When you solve a puzzle by trial and error, you choose which blank to fill next. If one blank has only one possible answer left, it is wise to fill it now. If you leave it for later, you may make many other guesses first, and then find that this blank has no answer, and you must undo all those guesses.

A variable ordering heuristic is a rule for this choice. A common rule says: fill next the blank with the fewest possible answers left. It does not change which final answers exist. It changes how much work the search does to find them, and the change can be huge.

## The idea

Consider a backtracking search on variables $X_1, \ldots, X_m$ with finite domains. At a node with the partial assignment $a$ on the set $Y$ of assigned variables, a **variable ordering** picks a variable $X \notin Y$; the children of the node are the extensions $a \cup \{X = v\}$ for the values $v$ that are left. A **value ordering** fixes the order of these children.

- A **static order** is one permutation $\pi$ of the variables, used at each node: the variable at depth $k$ is $X_{\pi(k)}$.
- A **dynamic order** may pick a different variable at different nodes of the same depth. It uses the state of the node, usually the current domains after [forward checking](/forward-checking/) or [arc consistency](/arc-consistency/).

Each order gives a valid search: each solution is a full assignment, and each ordering reaches it along one path. The order changes the tree, so it changes the cost.

**Why order matters.** A failure is cheap when it happens near the root and expensive when it happens deep in the tree, because everything between the cause and the discovery is searched again and again, a pattern called thrashing. A good order places the variables that are likely to fail, or that constrain many others, early.

**The main rules.**

1. **Minimum remaining values (MRV), or fail-first.** Pick the unassigned variable with the fewest values left in its current domain. A variable with one value is forced; a variable with zero values shows a dead end at once. Haralick and Elliott (1980) studied this rule under the name *fail first*, as part of their analysis of look-ahead for CSPs, and Bitner and Reingold (1975) used a dynamic choice of the next variable with the fewest choices left, which they called search rearrangement. See [minimum remaining values](/minimum-remaining-values/).
2. **Degree.** Pick the variable that has constraints with the most unassigned variables. It is used as a static order, and as a tie-breaker for MRV. See [degree heuristic](/degree-heuristic/).
3. **Saturation degree for coloring.** Brelaz's [DSATUR](/dsatur/) rule for [graph coloring](/graph-coloring/) picks the uncolored vertex whose neighbors already use the most distinct colors, with ties broken by the degree. Under the usual coloring CSP, the saturation degree of a vertex is $k$ minus the size of its remaining domain when $k$ colors are allowed, so DSATUR is MRV with the degree as a tie-breaker.
4. **Static orders from the structure.** Order the variables by decreasing degree in the [constraint graph](/constraint-graph/), or so that each variable has many constraints with earlier ones (a small width). A good static order costs nothing at run time.

**Value ordering is a different question.** Once the variable is chosen, the order of its values matters only when one solution is wanted. A common rule is *[least constraining value](/least-constraining-value/)*: try first the value that removes the fewest values from the domains of the neighbors. Fail-first for variables and succeed-first for values work together: the variable choice makes failures happen early, and the value choice makes the first branch likely to contain a solution. When all solutions are wanted, or when the instance has no solution, the value order does not change the number of nodes.

## Examples

### A forced variable

Take four variables with $D_1 = D_2 = \{1, \ldots, 9\}$, $D_3 = D_4 = \{5\}$, and the one constraint $X_3 \ne X_4$. The instance has no solution, and the cause involves only $X_3$ and $X_4$.

- Static order $X_1, X_2, X_3, X_4$ with forward checking: each of the $9 \cdot 9 = 81$ assignments of $X_1, X_2$ is tried, and under each one the value 5 for $X_3$ empties $D_4$. The search tries $9 + 81 + 81 = 171$ values.
- MRV with forward checking: $X_3$ and $X_4$ have one value each, so MRV picks $X_3$ first. The value 5 empties $D_4$, and the search stops after 1 value.

### Queens with forward checking

The table counts the values tried for a variable, including those that forward checking rejects at once, in a search for the first solution of $n$ queens. Each row is a variable whose value is a column. "Static" assigns the rows from top to bottom; "MRV" assigns the row with the fewest columns left, with ties broken by the lowest row. Both use forward checking and try the columns from left to right.

| $n$ | static order | MRV |
|---|---|---|
| 8 | 88 | 75 |
| 12 | 193 | 153 |
| 16 | 7560 | 44 |
| 20 | 145151 | 145 |

For $n = 20$ the dynamic order saves a factor of about 1000. For all 92 solutions of 8 queens, the counts are 1724 for the static order and 1360 for MRV: the saving is smaller, but each solution is found either way.

### Coloring

Color with three colors the graph made of a path $p_1, \ldots, p_{10}$, a complete graph on the four vertices $q_1, \ldots, q_4$, and the edge $p_{10} q_1$. The complete graph on four vertices needs four colors, so there is no solution. Plain backtracking without look-ahead, with the colors tried in a fixed order:

| order | values tried |
|---|---|
| static: $p_1, \ldots, p_{10}, q_1, \ldots, q_4$ | 55290 |
| [DSATUR](/dsatur/) (saturation, then degree among uncolored vertices) | 48 |

The static order colors the path in each of its $3 \cdot 2^9 = 1536$ ways and fails on the four vertices each time. DSATUR starts at $q_1$, which has the largest degree, stays inside the complete graph because its vertices have the highest saturation, and finds the failure there.

## Where it is used

Each CSP solver uses a dynamic variable order, and MRV with a degree tie-breaker is the textbook default for [backtracking search](/chronological-backtracking/) with [forward checking](/forward-checking/) or [maintaining arc consistency](/maintaining-arc-consistency/). Puzzle solvers for [sudoku](/sudoku/) fill the cell with the fewest candidates first, and [dancing links](/dancing-links/) for [exact cover](/exact-cover/) picks the column with the fewest rows, which is the same rule. SAT solvers such as [DPLL](/dpll/) choose the next variable by a branching heuristic, and integer programming chooses the variable to branch on by a [branching rule](/branching-rule/) such as [strong branching](/strong-branching/). Graph coloring by DSATUR is both an exact backtracking order and a greedy heuristic.

## References
