---
tag: Z4745G
kind: problem
slug: constraint-satisfaction-problem
name: Constraint satisfaction problem
aliases:
- CSP
area: logic-and-constraints/constraint-satisfaction
level: intro
summary: Assign values from finite domains to variables so that every constraint over subsets of variables is satisfied.
prereqs: [np-complete, graph-coloring]
see_also: [constraint-graph, arc-consistency, constraint-propagation, chronological-backtracking, maintaining-arc-consistency, csp-dichotomy-theorem, counting-csp, constraint-programming]
sources:
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, 2020
    locator: Chapter 6, Constraint Satisfaction Problems (the definition, the map colouring example, propagation, backtracking search, local search and the structure of problems)
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapters 1 and 2 (constraint networks, their graphs and their solutions), and Chapter 5 (backtracking search)
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 3 (constraint propagation), Chapter 4 (backtracking search algorithms, by Peter van Beek), Chapter 7 (tractable structures, by Rina Dechter) and Chapter 8 (the complexity of constraint languages, by David Cohen and Peter Jeavons)
  - paper: doi:10.1016/0004-3702(77)90007-8
    title: Alan K. Mackworth, Consistency in networks of relations, Artificial Intelligence 8(1), 1977
    locator: pages 99 to 118 (networks of relations and their consistency)
  - paper: doi:10.1137/S0097539794266766
    title: Tomás Feder and Moshe Y. Vardi, The computational structure of monotone monadic SNP and constraint satisfaction, a study through Datalog and group theory, SIAM Journal on Computing 28(1), 1998
    locator: pages 57 to 104 (CSP as the homomorphism problem for a fixed template, and the dichotomy conjecture)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, 1979
    locator: Appendix, problems GT4 (graph K-colorability), LO1 (satisfiability) and LO2 (3-satisfiability)
---

A constraint satisfaction problem (CSP) asks for an assignment of values to variables, each value taken from the finite domain of its variable, such that every constraint holds; a constraint lists the allowed tuples of values for a few of the variables. The decision version is [NP-complete](/np-complete/), and it contains [graph colouring](/graph-coloring/) and [SAT](/sat/) as special cases. Solvers combine [backtracking search](/chronological-backtracking/) with [constraint propagation](/constraint-propagation/), and the problem becomes polynomial when the [constraint graph](/constraint-graph/) has small treewidth or when the constraint relations have a special algebraic form ([CSP dichotomy theorem](/csp-dichotomy-theorem/)).

## In plain words

You have a set of unknowns. Each unknown can take one value from its own short list. A set of rules says which combinations are allowed: "these two must differ", "this one is less than that one", "these three add up to ten". You must choose one value for each unknown so that all rules hold at once.

Colouring a map so that neighbours differ is a constraint problem, and so is a sudoku, a school timetable or the placement of queens on a chess board. Trying every combination works, but the number of combinations grows very fast. Practical solvers guess one value at a time, delete the values that the rules now forbid, and go back when a list becomes empty.

## Definition

An *instance* is a triple $P = (X, D, C)$:

- $X = \{x_1, \ldots, x_n\}$ is a finite set of variables;
- $D = (D_1, \ldots, D_n)$ gives a finite domain $D_i$ for each $x_i$, with $d = \max_i |D_i|$;
- $C$ is a finite set of $m$ constraints. A constraint is a pair $(S, R)$: its *scope* $S = (x_{i_1}, \ldots, x_{i_r})$ is a tuple of $r$ distinct variables, $r$ is its *arity*, and its *relation* is $R \subseteq D_{i_1} \times \cdots \times D_{i_r}$.

An *assignment* gives each variable $x_i$ a value $s_i \in D_i$. It *satisfies* the constraint $(S, R)$ if $(s_{i_1}, \ldots, s_{i_r}) \in R$. A *solution* is an assignment that satisfies every constraint. A *partial assignment* gives values to some variables only, and it is *consistent* if it satisfies every constraint whose scope it covers.

The problem has four standard forms:

- **Decision.** Does $P$ have a solution?
- **Search.** Find a solution, or report that there is none.
- **Counting.** How many solutions does $P$ have? See [counting CSP](/counting-csp/).
- **Optimization.** Find an assignment that satisfies as many constraints as possible, or that minimizes a cost. See [maximum CSP](/maximum-csp/) and [soft constraints](/soft-constraints/).

A CSP is *binary* if every constraint has arity at most 2. For a binary CSP we write $e$ for the number of binary constraints, so $m = e$ when there are no unary constraints, and $R_{ij}$ for the relation on $x_i$ and $x_j$. The input size is $\sum_i |D_i| + \sum_{(S, R) \in C} r |R|$ when the relations are given as tables. In this area $n$ is the number of variables, $m$ the number of constraints, $e$ the number of binary constraints, $d$ the largest domain size, $r$ the largest arity and $w$ a width.

**The homomorphism form.** Feder and Vardi (1998) wrote a CSP as a question about relational structures. For a finite set $\Gamma$ of relations on one domain $A$, the *constraint language*, the problem CSP($\Gamma$) takes instances whose relations all belong to $\Gamma$. Equivalently, an instance is a structure $\mathbf{I}$ with the same signature as the template $\mathbf{A} = (A; \Gamma)$, and a solution is a homomorphism from $\mathbf{I}$ to $\mathbf{A}$. Graph $k$-colouring is CSP($K_k$), the homomorphism problem to the complete graph on $k$ vertices.

## Variants

- **Binary and non-binary CSPs.** Each non-binary CSP can be turned into a binary one by the [dual encoding or the hidden variable encoding](/dual-graph-transformation/).
- **Boolean CSP.** All domains are $\{0, 1\}$. This is [Boolean constraint satisfaction](/boolean-constraint-satisfaction/), also called generalized satisfiability, and it contains [SAT](/sat/), [2-SAT](/2-sat/), [Horn-SAT](/horn-sat/) and [XOR-SAT](/xor-sat/).
- **Fixed constraint language.** CSP($\Gamma$) for a fixed finite $\Gamma$. Each such problem is in P or NP-complete ([Schaefer's theorem](/schaefer-dichotomy-theorem/) for two values, the [CSP dichotomy theorem](/csp-dichotomy-theorem/) in general).
- **Restricted structure.** The constraint graph is a tree, has small treewidth or a small cycle cutset. See [tree-structured CSP algorithm](/tree-structured-csp/), [cutset conditioning](/cutset-conditioning/) and [bucket elimination](/bucket-elimination/).
- **Infinite domains.** Variables range over integers or reals, and constraints are equations or inequalities: [numeric constraint satisfaction](/numeric-constraint-satisfaction/), [interval constraint propagation](/interval-constraint-propagation/) and the [simple temporal problem](/simple-temporal-problem/).
- **Counting and optimization.** [Counting CSP](/counting-csp/), [maximum CSP](/maximum-csp/) and [soft constraints](/soft-constraints/).
- **Global constraints.** Constraints such as [all-different](/all-different-constraint/) have unbounded arity and are given by a rule, not a table. See [global constraint](/global-constraint/) and [constraint programming](/constraint-programming/).

## Examples

**Map colouring.** Colour the 7 regions of Australia, WA, NT, SA, Q, NSW, V and T, with 3 colours so that neighbours differ. There are 7 variables with domain $\{0, 1, 2\}$ and 9 binary constraints $\ne$: WA-NT, WA-SA, NT-SA, NT-Q, SA-Q, SA-NSW, SA-V, Q-NSW and NSW-V. Tasmania has no constraint. The instance has 18 solutions: SA takes one of 3 colours, then WA, NT, Q, NSW and V alternate between the other 2 colours along a path in 2 ways, and T takes any of 3 colours, so $3 \cdot 2 \cdot 3 = 18$.

**Sudoku.** 81 variables with domain $\{1, \ldots, 9\}$, some fixed by the clues. Each row, column and box is an [all-different constraint](/all-different-constraint/), 27 in total. As a binary CSP, each cell differs from its 20 peers, which gives $81 \cdot 20 / 2 = 810$ binary constraints. See [sudoku](/sudoku/).

**Eight queens.** 8 variables, one per column, with domain $\{1, \ldots, 8\}$ for the row. For each pair of columns $i < j$, the constraint is $q_i \ne q_j$ and $|q_i - q_j| \ne j - i$. There are 28 binary constraints and 92 solutions. See [n-queens problem](/n-queens-problem/).

**SAT.** A CNF formula with $n$ variables is a CSP with domains $\{0, 1\}$ and one constraint for each clause, whose relation holds all $2^r - 1$ assignments that satisfy the clause.

**A non-example.** A system of linear equations over the reals is not a CSP in the sense of this page, because the domains are infinite. Over a finite field it is one, and it is solved by [Gaussian elimination](/gaussian-elimination/) in polynomial time.

## Known algorithms

- **Generate and test.** Try all $\prod_i |D_i| \le d^n$ assignments. Time $O(d^n m r)$.
- **Backtracking search.** Assign variables one at a time and go back when a constraint fails ([chronological backtracking](/chronological-backtracking/)). Variable and value order heuristics help: [minimum remaining values](/minimum-remaining-values/), the [degree heuristic](/degree-heuristic/) and [least constraining value](/least-constraining-value/). Smarter backtracking: [conflict-directed backjumping](/conflict-directed-backjumping/), [graph-based backjumping](/graph-based-backjumping/), [dynamic backtracking](/dynamic-backtracking/) and [nogood learning](/nogood-learning/).
- **Search with propagation.** [Forward checking](/forward-checking/) and [maintaining arc consistency](/maintaining-arc-consistency/) delete values at each search node. The propagation uses [AC-3](/ac-3/), [AC-4](/ac-4/) or the filtering of [global constraints](/global-constraint/).
- **Local search.** [Min-conflicts](/min-conflicts/) starts from a full assignment and changes one variable at a time. It does not prove that there is no solution.
- **Structure-based algorithms.** A tree-shaped constraint graph is solved in $O(n d^2)$ time ([tree-structured CSP algorithm](/tree-structured-csp/)). A cycle cutset of size $c$ gives $O(d^c (n - c) d^2)$ time ([cutset conditioning](/cutset-conditioning/)). [Bucket elimination](/bucket-elimination/) along an order of induced width $w$ takes time and space exponential only in $w$, and the same bound holds for dynamic programming on a [tree decomposition](/tree-decomposition/) of width $w$.
- **Tractable languages.** Horn, dual Horn, bijunctive and affine Boolean constraints are solved by [forward chaining](/horn-sat-forward-chaining/), the [2-SAT algorithm](/two-sat-algorithm/) and [Gaussian elimination over GF(2)](/xor-gaussian-elimination/). For larger domains, the polynomial cases are those of the [CSP dichotomy theorem](/csp-dichotomy-theorem/).

## Bounds

- **NP-complete.** The decision problem is in NP: a solution is a certificate that can be checked with $m$ table lookups. It is NP-hard even for binary constraints with $d = 3$, because graph 3-colouring is such a CSP, and for Boolean domains with arity 3, because [3-SAT](/3-sat/) is such a CSP (Garey and Johnson, problems GT4 and LO2).
- **Polynomial special cases.** Binary Boolean CSPs are 2-SAT, which is solvable in linear time. A CSP whose constraint graph is a tree is solvable in $O(n d^2)$ time, by [Freuder's theorem](/freuder-theorem/). A CSP whose primal graph has an elimination order of induced width $w$ is solvable in $O((m + n)(w + 1) d^{w+1})$ time.
- **Dichotomy for languages.** For each finite constraint language $\Gamma$, CSP($\Gamma$) is either in P or NP-complete. Schaefer (1978) proved this for Boolean domains, and Bulatov (2017) and Zhuk (2017, journal version 2020) proved it in general.
- **Exponential time.** No algorithm is known that solves 3-SAT, a CSP with $d = 2$ and arity 3, in time $2^{o(n)}$, and the exponential time hypothesis says that none exists. Under the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/), Boolean CSPs of large arity need time $2^{(1 - \varepsilon) n}$ for each fixed $\varepsilon > 0$.

## Reductions

- **SAT to CSP.** Each clause becomes a constraint, as in the examples. So CSP is NP-hard.
- **CSP to SAT.** The *direct encoding* has a Boolean variable $p_{i,a}$ for each $x_i$ and $a \in D_i$, a clause $\bigvee_a p_{i,a}$ for each variable, clauses $\neg p_{i,a} \vee \neg p_{i,b}$ for $a \ne b$, and for each binary constraint and each forbidden pair $(a, b)$ the clause $\neg p_{i,a} \vee \neg p_{j,b}$. Its models match the solutions one to one. The size is $O(n d^2 + e d^2)$.
- **Graph colouring.** A graph is $k$-colourable exactly when the binary CSP with domain $\{1, \ldots, k\}$ and a constraint $\ne$ on each edge has a solution ([k-coloring](/k-coloring/)).
- **Non-binary to binary.** The [dual encoding](/dual-graph-transformation/) has one variable for each constraint, whose values are the allowed tuples, and binary constraints that make shared variables agree. It preserves the number of solutions when each variable is in some constraint.
- **Databases.** The set of solutions is the natural [join](/relational-join/) of the constraint relations, so deciding a CSP is the same as deciding whether a join is non-empty. This is why acyclic CSPs, like [acyclic joins](/acyclic-join-evaluation/), are solvable in polynomial time.

## Applications

- Scheduling and timetabling, with resources, time windows and precedence constraints.
- Product configuration, where each component must fit the others.
- Planning and verification, by bounded encodings into constraints.
- Frequency assignment and register allocation, both close to graph colouring.
- Puzzles such as [sudoku](/sudoku/), crosswords and the [n-queens problem](/n-queens-problem/), which are standard test problems.
- Temporal reasoning with [Allen's interval algebra](/allens-interval-algebra/) and the [simple temporal problem](/simple-temporal-problem/).

## References
