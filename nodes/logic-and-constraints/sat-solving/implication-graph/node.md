---
tag: 2V1W4P
kind: data-structure
slug: implication-graph
name: Implication graph
aliases:
- conflict graph
- implication DAG
area: logic-and-constraints/sat-solving
level: core
summary: Directed acyclic graph of the assignments of a SAT search. Each forced literal has edges from the literals that forced it. CDCL reads its conflict clauses and UIPs from it.
model: word-ram
prereqs: [unit-propagation, directed-acyclic-graph]
see_also: [first-uip, clause-learning, cdcl, non-chronological-backtracking, two-sat-algorithm, 2-sat, dominator-tree, strongly-connected-components]
sources:
  - paper: "João P. Marques-Silva and Karem A. Sakallah, GRASP, a new search algorithm for satisfiability, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD), 1996"
    locator: pages 220 to 227 (the implication graph, conflict analysis and unique implication points)
  - paper: doi:10.1109/12.769433
    title: João P. Marques-Silva and Karem A. Sakallah, GRASP, a search algorithm for propositional satisfiability, IEEE Transactions on Computers 48(5), 1999
    locator: pages 506 to 521 (the implication graph, conflict-induced clauses and UIPs)
  - paper: "Lintao Zhang, Conor F. Madigan, Matthew W. Moskewicz and Sharad Malik, Efficient conflict driven learning in a Boolean satisfiability solver, Proceedings of ICCAD 2001, pages 279 to 285"
    locator: cuts of the implication graph as learning schemes, and the comparison that favours the first UIP
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 4, Conflict-Driven Clause Learning SAT Solvers, by Marques-Silva, Lynce and Malik, the sections on implication graphs and conflict analysis
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, An Algorithmic Point of View, second edition, 2016
    locator: Chapter 2, Section 2.2 (the implication graph, conflict clauses and UIPs)
  - paper: doi:10.1016/0020-0190(79)90002-4
    title: Bengt Aspvall, Michael F. Plass and Robert Endre Tarjan, A linear-time algorithm for testing the truth of certain quantified Boolean formulas, Information Processing Letters 8(3), 1979
    locator: pages 121 to 123 (the implication graph of a 2-CNF formula and the strongly connected component test)
---

An implication graph is a [directed acyclic graph](/directed-acyclic-graph/) that records why each literal of a SAT search is true: its nodes are the true literals, and a literal forced by [unit propagation](/unit-propagation/) has an edge from each literal that made its reason clause unit. A conflict adds a special node $\kappa$ with an edge from the negation of each literal of the false clause. [CDCL](/cdcl/) reads its [learned clauses](/clause-learning/) from cuts of this graph, and the best cut sits at the [first unique implication point](/first-uip/). For [2-SAT](/2-sat/) the same name means a different, static graph on all literals, see the variants.

## In plain words

A solver guesses some values and then works out the values that the guesses force. The implication graph is the record of this work. Each true value is a box. A guess has no arrows into it. A forced value has an arrow from each value that forced it.

When a clause turns false, the solver adds a box for the conflict, with arrows from the values that made the clause false. Then it walks the arrows back from the conflict. Any set of boxes that cuts every path from the guesses to the conflict is a reason for the conflict, and the solver learns a clause that rules out that set of values. The best cut often goes through one box that every path from the last guess must pass. Such a box is a unique implication point.

## The abstract type

The graph is built over the variables $x_1, \ldots, x_n$ of a CNF formula $F$, alongside a search that keeps a trail of assigned literals and a current decision level $d$. The operations are:

- `decide(ℓ)`: open level $d + 1$ with the free literal $\ell$ as its decision.
- `imply(ℓ, C)`: add the free literal $\ell$, forced by the clause $C$ whose other literals are all false.
- `conflict(C)`: add the conflict node $\kappa$ for a clause $C$ whose literals are all false.
- `backjump(b)`: remove $\kappa$ and every node of a level above $b$.
- `uips()`: list the unique implication points of the conflict level, the one nearest to $\kappa$ first.
- `first-uip-clause()`: the clause of the first UIP cut and the level to jump back to.

A node $u$ of the conflict level $d$ is a *unique implication point* (UIP) when every path from the decision $\delta_d$ of level $d$ to $\kappa$ passes through $u$. In graph words, the UIPs are the [dominators](/dominator-tree/) of $\kappa$ in the subgraph of level $d$ with root $\delta_d$, so they form a chain, and $\delta_d$ is always one of them.

## Representation

Each node $v$ has a trail position $\mathrm{pos}(v)$, a level $\mathrm{lev}(v)$ and a list $\mathrm{pred}(v)$ of its predecessors. The array `lim` holds, for each level $i \ge 1$, the trail position where level $i$ starts. The conflict node is the list $\mathrm{pred}(\kappa)$, or nothing.

**Invariant (G).** (a) Every edge $w \to v$ between literal nodes has $\mathrm{pos}(w) < \mathrm{pos}(v)$ and $\mathrm{lev}(w) \le \mathrm{lev}(v)$. (b) Levels do not decrease along the trail, and the first node of each level $i \ge 1$ is its decision, which has no in-edges. (c) No variable has two nodes.

By (a), the trail followed by $\kappa$ is a [topological order](/topological-sort/), so the graph has no cycle. A solver does not store the edges. It stores, for each variable, a pointer to its reason clause, as MiniSat does, and reads the edges from the clause when it needs them. The predecessors of a node are then the negations of the other literals of its reason.

## Operations

```pseudo id=main
DECIDE(G, ℓ)                                  ▷ ℓ is free and κ does not exist
L1  append |trail| to lim                       ▷ level d + 1 starts here
L2  append ℓ to the trail with level d + 1 and pred(ℓ) ← ∅

IMPLY(G, ℓ, C)                                ▷ ℓ ∈ C, every other literal of C is false
L3  P ← {¬q : q ∈ C, q ≠ ℓ}
L4  pred(ℓ) ← P                                 ▷ one edge w → ℓ for each w ∈ P
L5  append ℓ to the trail with level d

CONFLICT(G, C)                                ▷ every literal of C is false
L6  pred(κ) ← {¬q : q ∈ C}

BACKJUMP(G, b)                                ▷ 0 ≤ b ≤ d
L7  remove κ; remove every node of level above b; shorten lim to b entries

UIPS(G)                                       ▷ κ exists; d ← max level in pred(κ) ≥ 1
L8  S ← {w ∈ pred(κ) : lev(w) = d}; c ← |S|; U ← empty list
L9  for each node v of level d, from the last to the first on the trail do
L10     if v ∈ S then
L11         if c = 1 then append v to U
L12         c ← c − 1
L13         for each w ∈ pred(v) with lev(w) = d and w ∉ S do add w to S; c ← c + 1
L14 return U
```

**Decide** (lines L1 and L2) opens a new level. The decision is a source of the graph.

**Imply** (lines L3 to L5) adds a forced literal. Its in-edges come from the negations of the other literals of the reason, since those literals are false and so their negations are nodes.

**Conflict** (line L6) adds $\kappa$ in the same way, with the false clause as its reason.

**Backjump** (line L7) cuts the trail at the start of level $b + 1$. Every edge goes forward on the trail, so the rest of the graph keeps all its edges.

**Uips** (lines L8 to L14) walks the conflict level backwards from the end of the trail. The set $S$ holds the nodes of level $d$ known to reach $\kappa$, and $c$ counts those not yet visited. When the walk visits a node $v$ of $S$ and $c = 1$, every path from $\delta_d$ to $\kappa$ goes through $v$, so $v$ is a UIP. Then $v$ is replaced in $S$ by its level-$d$ predecessors.

**First-uip-clause** runs the same walk and stops at the first UIP $u$. It also collects the nodes of levels 1 to $d - 1$ with an edge into a visited node of $S$ or into $\kappa$. The clause is $\neg u$ together with the negations of those nodes, and the backjump level $b$ is the largest of their levels, or 0. Nodes of level 0 are left out, because they hold in every model. This clause is exactly the one that [clause learning](/clause-learning/) gets by resolution, see the [first UIP](/first-uip/) page.

## Example

This is the run on the [CDCL](/cdcl/) page. The formula has the clauses

$$C_1 = \{x_1, x_2\},\ C_2 = \{x_1, x_3, x_7\},\ C_3 = \{\neg x_2, \neg x_3, x_4\},\ C_4 = \{\neg x_4, x_5, x_8\},\ C_5 = \{\neg x_4, x_6, x_9\},\ C_6 = \{\neg x_5, \neg x_6\}.$$

The decisions $\neg x_7$, $\neg x_8$, $\neg x_9$ and $\neg x_1$ open levels 1 to 4. Unit propagation then calls IMPLY five times, and $C_6$ becomes false.

| trail position | node | level | reason | predecessors |
|---|---|---|---|---|
| 1 | $\neg x_7$ | 1 | decision | none |
| 2 | $\neg x_8$ | 2 | decision | none |
| 3 | $\neg x_9$ | 3 | decision | none |
| 4 | $\neg x_1$ | 4 | decision | none |
| 5 | $x_2$ | 4 | $C_1$ | $\neg x_1$ |
| 6 | $x_3$ | 4 | $C_2$ | $\neg x_1, \neg x_7$ |
| 7 | $x_4$ | 4 | $C_3$ | $x_2, x_3$ |
| 8 | $x_5$ | 4 | $C_4$ | $x_4, \neg x_8$ |
| 9 | $x_6$ | 4 | $C_5$ | $x_4, \neg x_9$ |
| | $\kappa$ | 4 | $C_6$ | $x_5, x_6$ |

UIPS starts with $S = \{x_5, x_6\}$ and $c = 2$. The walk over level 4 goes as follows.

| visited node | in $S$ | $c$ at the visit | recorded | level-4 nodes added to $S$ | $c$ after |
|---|---|---|---|---|---|
| $x_6$ | yes | 2 | no | $x_4$ | 2 |
| $x_5$ | yes | 2 | no | none | 1 |
| $x_4$ | yes | 1 | yes | $x_2, x_3$ | 2 |
| $x_3$ | yes | 2 | no | $\neg x_1$ | 2 |
| $x_2$ | yes | 2 | no | none | 1 |
| $\neg x_1$ | yes | 1 | yes | none | 0 |

The UIPs are $x_4$ and $\neg x_1$. Every path from $\neg x_1$ to $\kappa$ passes through $x_4$, but $x_2$ is not a UIP, because the path through $x_3$ avoids it. The first UIP cut puts $x_5$, $x_6$ and $\kappa$ on the conflict side. The edges that cross it come from $x_4$, $\neg x_8$ and $\neg x_9$, so the first UIP clause is $\{\neg x_4, x_8, x_9\}$ with $b = 3$. The cut at the decision $\neg x_1$ gives the clause $\{x_1, x_7, x_8, x_9\}$, which is longer. After BACKJUMP(3), IMPLY adds $\neg x_4$ at level 3 with the learned clause as its reason, so its predecessors are $\neg x_8$ and $\neg x_9$.

## Correctness

Each operation keeps the invariant (G): DECIDE and IMPLY append a node whose predecessors are already on the trail at levels not above the current one, CONFLICT adds edges into $\kappa$ only, and BACKJUMP removes a suffix of the trail. If the search decides only after propagation is complete, every node of a level $i \ge 1$ has a predecessor of level $i$ or is $\delta_i$, so it is reachable from $\delta_i$ inside level $i$. Under this condition, the walk of UIPS keeps two facts: a node visited later than $t$ is in $S$ exactly when it reaches $\kappa$, and $c$ is the number of nodes of $S$ at or before $t$. A node $u$ is then a UIP exactly when it is the only one of $S$ at or before its own position, which is the test $c = 1$. The other direction uses a path from $\delta_d$ to a second node of $S$, joined to a path from that node to $\kappa$ that skips over $u$. The first UIP clause has exactly one literal of level $d$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $s$ be the number of nodes of level $d$ and $e$ the number of their in-edges. With arrays indexed by variable, as solvers use, each step below is $O(1)$ worst case; the Python code uses dictionaries, which give the same bounds in expectation.

| operation | time |
|---|---|
| decide | $O(1)$ |
| imply with a reason of $k$ literals | $O(k)$ |
| conflict on a clause of $k$ literals | $O(k)$ |
| backjump | $O(r + e_r)$, for $r$ removed nodes with $e_r$ in-edges |
| uips | $O(s + e)$ |
| first-uip-clause | $O(s + e)$ |
| space | $O(n)$ nodes; edges are read from the reason clauses |

The bound for UIPS holds because each node of level $d$ is visited once and enters $S$ at most once. A general dominator algorithm such as [Lengauer and Tarjan's](/lengauer-tarjan-algorithm/) is not needed: the trail is already a topological order, and the walk finds all dominators of $\kappa$ in one pass.

## Variants

- **The 2-SAT implication graph.** For a [2-CNF](/2-sat/) formula, the graph has a node for each of the $2n$ literals and, for each clause $\{a, b\}$, the edges $\neg a \to b$ and $\neg b \to a$. It is static and can have cycles. Aspvall, Plass and Tarjan showed that the formula is unsatisfiable exactly when some $x$ and $\neg x$ lie in the same [strongly connected component](/strongly-connected-components/), which gives the linear-time [2-SAT algorithm](/two-sat-algorithm/). The binary clauses of a general formula form the same kind of graph, and [failed literal probing](/failed-literal-probing/) and equivalent literal substitution in preprocessors work on it.
- **Implicit graph.** Solvers store one reason pointer for each variable and no edge lists. A binary reason can be stored inline as the other literal, which saves a memory access.
- **Other cuts.** Any set of nodes that separates the decisions from $\kappa$ gives a valid clause. GRASP learned at all UIPs; the decision cut and the "all UIP" scheme are compared on the [clause learning](/clause-learning/) page.
- **Chronological backtracking.** When a solver backtracks only one level after some conflicts, a clause can be false with its highest level below the current level. The conflict level $d$ is then the largest level in $\mathrm{pred}(\kappa)$, not the current level, which is why line L8 takes the maximum.

## When to use it

Use the implication graph in any search for SAT that learns from conflicts: in [CDCL](/cdcl/), in [DPLL(T)](/dpll-t/), where theory propagations add nodes with reasons from the theory, and in [nogood learning](/nogood-learning/) for constraint solvers. In practice it stays implicit in the trail and the reason pointers, and it is materialized only in conflict analysis. Use the 2-SAT variant for 2-CNF formulas and binary clause reasoning.

## Pitfalls

- **Deciding before propagation is complete.** If a clause that was unit at a lower level is used as a reason at level $d$, its node is not reachable from $\delta_d$, and the count in UIPS can stop at a wrong node. Complete the propagation before each decision, or give the late node the lower level.
- **Using the current level as the conflict level.** After a chronological backtrack, the false clause can have no literal of the current level. Take the maximum level of its literals.
- **Counting a node twice.** A node can be a predecessor of several nodes. Line L13 adds it to $S$ only once; without the test $w \notin S$, the counter $c$ never reaches 1 at the right place.
- **A conflict at level 0.** There is no decision to cut from, and UIPS has no meaning. A conflict at level 0 means that $F$ is unsatisfiable.
- **Level-0 nodes in the learned clause.** Their negations are false in every model, so they only make the clause longer. Leave them out, as first-uip-clause does.
- **Deleting a reason clause.** A clause that is the reason of a node on the trail holds the in-edges of that node. A [clause database reduction](/clause-database-reduction/) must keep it, or conflict analysis reads edges that no longer exist.

## Implementations

The Python class keeps the trail, the array `lim`, and dictionaries for the levels, the positions and the predecessor lists, with literals as signed integers. `uips` follows the main block line by line, `first_uip_clause` runs the same walk and also collects the lower-level predecessors, and `check_invariant` tests (G).

## History

Marques-Silva and Sakallah introduced the implication graph for conflict analysis in GRASP, first at ICCAD 1996 and then in the IEEE Transactions on Computers in 1999. They defined unique implication points and learned clauses from cuts of the graph. Zhang, Madigan, Moskewicz and Malik compared several cuts in 2001 and found that learning only at the first UIP worked best on their benchmarks; this is the scheme of Chaff, MiniSat and the solvers after them. The 2-SAT implication graph is older: Aspvall, Plass and Tarjan used it in 1979 for a linear-time test of 2-CNF formulas.

## References
