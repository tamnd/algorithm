---
tag: 0N945P
kind: problem
slug: binate-covering-problem
name: Binate covering problem
aliases:
- minimum cost satisfiability of a product of sums
- binate covering
area: cad/logic-synthesis
level: advanced
summary: Find a least cost assignment that satisfies a product of sums in which variables appear in both phases, the core of exact FSM and technology mapping problems.
prereqs: [set-cover, conjunctive-normal-form, np-hard]
see_also: [petricks-method, hitting-set, weighted-max-sat, pseudo-boolean-sat, binary-integer-programming, incompletely-specified-fsm-minimization, technology-mapping, depth-first-branch-and-bound]
sources:
  - paper: doi:10.1109/43.644030
    title: Tiziano Villa, Timothy Kam, Robert K. Brayton and Alberto L. Sangiovanni-Vincentelli, Explicit and implicit algorithms for binate covering problems, IEEE Transactions on Computer-Aided Design 16(7), 677 to 691, 1997
    locator: the definition of binate covering as a table, the reduction rules, the lower bounds for branch and bound, and the measured runs of explicit and implicit solvers
  - paper: "Olivier Coudert, On solving covering problems, Proceedings of the 33rd Design Automation Conference (DAC), 1996"
    title: On solving covering problems
    locator: lower bounds and pruning for unate and binate covering by branch and bound (general locator)
  - paper: "A. Grasselli and F. Luccio, A method for minimizing the number of internal states in incompletely specified sequential networks, IEEE Transactions on Electronic Computers EC-14(3), 350 to 359, 1965"
    title: A method for minimizing the number of internal states in incompletely specified sequential networks
    locator: state minimization as a covering problem with closure conditions, solved by a cost-minimal satisfying assignment
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: "R. M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, 1972"
    locator: the NP-completeness of set covering and of satisfiability
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: the sections on covering problems (general locator), and their use in Chapters 7, 9 and 10
---

The binate covering problem asks for a 0-1 assignment of least cost that satisfies a Boolean formula in [conjunctive normal form](/conjunctive-normal-form/), a product of sums. Each variable has a nonnegative cost, paid when the variable is 1. If every variable appears only as a positive literal, the formula is unate, and the problem is weighted [set cover](/set-cover/), the unate covering problem of two-level minimization. If some variables also appear negated, the formula is binate, and a choice can force or forbid other choices. That is the form of exact state minimization, of DAG covering in technology mapping, and of many other selection problems in logic synthesis. It contains both set cover and satisfiability, so it is [NP-hard](/np-hard/), and even finding any feasible solution is NP-complete.

## In plain words

You have a list of items to buy, each with a price. You also have a list of rules. Each rule names some items and says "buy at least one of these", or "if you buy this one, you must also buy one of those", or "do not buy both of these". You want to follow all the rules and pay as little as possible. If all rules are of the first kind, the problem is the classic covering problem, and buying everything always works. With rules of the other kinds, buying more can break a rule, and it may be hard even to find a choice that follows all of them.

## Definition

**Input.** Boolean variables $x_1, \dots, x_n$ with costs $c_i \ge 0$, and a formula $F = C_1 \wedge \cdots \wedge C_m$, where each clause $C_j$ is an OR of literals $x_i$ or $\bar{x}_i$.

**Feasible solutions.** Assignments $x \in \{0,1\}^n$ with $F(x) = 1$.

**Objective.** Minimize $\sum_i c_i x_i$.

**Decision version.** Given $F$, the costs and $k$, is there a satisfying $x$ with $\sum_i c_i x_i \le k$?

**Table form.** In logic synthesis the input is a covering table with one row per clause and one column per variable. The entry is 1 if $x_i$ is in $C_j$, 0 if $\bar{x}_i$ is in $C_j$, and blank otherwise. A set of columns (the variables set to 1) is a solution when every row has a 1 in a chosen column or a 0 in a column that is not chosen. The table is unate when it has no 0 entry.

## Variants

- **Unate covering.** No negative literal. This is weighted set cover, or [hitting set](/hitting-set/), with the clauses as the elements to cover. Setting all variables to 1 is always feasible when no clause is empty.
- **Covering with closure.** Clauses of the form "at least one of these" plus implications $x_a \Rightarrow (x_b \vee x_c \vee \cdots)$, written $(\bar{x}_a \vee x_b \vee x_c \vee \cdots)$. This is the form that comes from [incompletely specified FSM minimization](/incompletely-specified-fsm-minimization/).
- **Unit costs.** All $c_i = 1$, so the goal is the fewest variables set to 1. The general case keeps its hardness.
- **Negative costs.** A variable with $c_i < 0$ can be replaced by its complement $y_i = \bar{x}_i$ with cost $-c_i$ and a constant offset, so nonnegative costs lose no generality.
- **Multiple-valued variables.** Each variable takes one of several values, as in some encoding problems. A one-hot set of binary variables with "exactly one" clauses gives the binary form.

## Examples

**From state minimization.** Let $p$, $q$ and $r$ stand for three compatible sets of states of the machine on the [ISFSM minimization](/incompletely-specified-fsm-minimization/) page, each of cost 1. The clauses are $(p)$, $(p \vee q)$, $(q \vee r)$, $(r)$ for covering, and $(\bar{p} \vee r)$, $(\bar{r} \vee q)$, $(\bar{q} \vee p)$, $(\bar{q} \vee r)$ for closure.

| row | $p$ | $q$ | $r$ |
|---|---|---|---|
| 1 | 1 | | |
| 2 | 1 | 1 | |
| 3 | | 1 | 1 |
| 4 | | | 1 |
| 5 | 0 | | 1 |
| 6 | | 1 | 0 |
| 7 | 1 | 0 | |
| 8 | | 0 | 1 |

The unate rows 1 to 4 alone have the minimum $\{p, r\}$ of cost 2. It breaks row 6: $r$ is chosen and $q$ is not. The only assignment of cost at most 2 that meets rows 1 and 4 is $\{p, r\}$, so the binate minimum is $\{p, q, r\}$, of cost 3. This shows the effect of the 0 entries: the minimum of the unate part is only a lower bound.

**From SAT.** Any CNF formula with all costs 0 is a binate covering instance whose minimum is 0 when the formula is satisfiable and that has no solution otherwise.

## Known algorithms

- **Branch and bound on the table.** The exact method of Grasselli and Luccio (1965), refined by many later tools. It applies reduction rules, picks a column, and branches on $x_i = 1$ and $x_i = 0$, as in [depth-first branch and bound](/depth-first-branch-and-bound/). The rules are: a row with one literal fixes its variable (an essential column); a row whose literal set contains another row's literal set can be removed (row dominance); and a column $x_k$ can be set to 0 when another column $x_j$ has $c_j \le c_k$, a 1 in every row where $x_k$ has a 1, and no 0 in a row where $x_k$ has no 0 (column dominance, where the condition on the 0 entries is the extra check of the binate case). The lower bound is often a [maximal independent set](/maximal-independent-set/) of unate rows with no common column, since each such row needs its own column.
- **Implicit branch and bound.** Villa, Kam, Brayton and Sangiovanni-Vincentelli (1997) store the rows and columns as BDDs and apply the reductions to whole sets at once, for tables with very many rows.
- **Shortest path in a BDD.** Build the [binary decision diagram](/binary-decision-diagram/) of $F$. Each path to the 1 leaf is a set of satisfying assignments, and with edge weights $c_i$ on the 1 branches and 0 on the 0 branches, a shortest path to the 1 leaf gives the minimum. This takes time linear in the BDD size, which can be exponential in $n$.
- **0-1 integer programming.** Each clause becomes $\sum_{x_i \in C} x_i + \sum_{\bar{x}_i \in C} (1 - x_i) \ge 1$, and a [0-1 integer programming](/binary-integer-programming/) solver works on it. The [LP relaxation](/lp-relaxation/) gives a lower bound for branch and bound.
- **Pseudo-Boolean and MaxSAT solvers.** The same model for a [pseudo-Boolean](/pseudo-boolean-sat/) solver, or for [weighted MaxSAT](/weighted-max-sat/), with the clauses of $F$ as hard clauses and one soft unit clause $(\bar{x}_i)$ of weight $c_i$ for each variable.
- **Unate case.** [Petrick's method](/petricks-method/), branch and bound, and the greedy set cover algorithm. The greedy method does not apply to the binate case, where it can fail to find a feasible solution at all.

## Bounds

**Upper bounds (proved).**

- Enumeration of all $2^n$ assignments solves every instance in $O(2^n (n + |F|))$ time, where $|F|$ is the total length of the clauses.
- The decision version is in NP: a satisfying assignment of cost at most $k$ is a certificate.
- The unate case has a polynomial-time approximation within a factor $H(m) \le 1 + \ln m$ by greedy set cover, where $m$ is the number of rows.

**Lower bounds (proved, as hardness).**

- The decision version is NP-complete. It contains set cover (Karp 1972) as the unate case, and SAT as the case with all costs 0.
- Deciding whether a feasible solution exists is NP-complete, since that is SAT. So unless P = NP, no polynomial-time algorithm returns a feasible solution whenever one exists, and in particular no polynomial-time algorithm approximates the binate problem within any factor. The unate case keeps the hardness of approximation of set cover.

**Measured.** Villa, Kam, Brayton and Sangiovanni-Vincentelli (1997) ran their explicit and implicit solvers on covering tables from FSM minimization and other synthesis problems. They compare the two solvers on these tables, and the implicit solver finishes on some tables that are too large for the explicit one. This is a measurement on their benchmarks, not a proved bound.

## Reductions

- **From SAT.** Give all variables cost 0. The instance has a solution exactly when the formula is satisfiable.
- **From set cover.** A set cover instance with elements $e_j$ and sets $S_i$ of cost $c_i$ is the unate instance with one clause $\bigvee_{i : e_j \in S_i} x_i$ per element.
- **To 0-1 integer programming.** One linear inequality per clause, as above, with the same objective.
- **To weighted MaxSAT.** Hard clauses $F$ and soft clauses $(\bar{x}_i)$ of weight $c_i$. A maximum weight of satisfied soft clauses is a minimum cost of the variables set to 1.
- **To shortest paths.** For an ordered BDD of $F$, the minimum is a [shortest path](/shortest-path/) from the root to the 1 leaf, with the edge weights above.

## Applications

- **ISFSM minimization.** The choice of a closed cover by compatibles of an [incompletely specified FSM](/incompletely-specified-fsm-minimization/) is a binate covering problem, as in the example.
- **Technology mapping.** Covering a subject DAG by library patterns, where choosing a match forces matches at its inputs, is binate covering. See [technology mapping](/technology-mapping/).
- **LUT mapping for area.** Choosing cuts so that every output and every leaf of a chosen cut is the root of a chosen cut is binate covering, as noted on the [LUT mapping](/lut-mapping/) page.
- **Two-level minimization.** The prime selection step of [two-level minimization](/two-level-logic-minimization/) is the unate case.

## References
