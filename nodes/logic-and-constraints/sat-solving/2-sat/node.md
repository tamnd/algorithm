---
tag: K8YWXT
kind: problem
slug: 2-sat
name: 2-SAT
aliases:
- 2SAT
- Krom formulas
- 2-satisfiability
area: logic-and-constraints/sat-solving
level: intro
summary: SAT where each clause has at most two literals. It is solvable in linear time with the implication graph, while its counting and maximization versions are hard.
prereqs: [sat, conjunctive-normal-form, literal, clause]
see_also: [two-sat-algorithm, implication-graph, strongly-connected-components, 3-sat, horn-sat, xor-sat, max-2-sat, schaefer-dichotomy-theorem]
sources:
  - paper: doi:10.1016/0020-0190(79)90002-4
    title: Bengt Aspvall, Michael F. Plass and Robert E. Tarjan, A linear-time algorithm for testing the truth of certain quantified Boolean formulas, Information Processing Letters 8(3), 121 to 123 (1979)
    locator: the whole paper
  - paper: "Shimon Even, Alon Itai and Adi Shamir, On the complexity of timetable and multicommodity flow problems, SIAM Journal on Computing 5(4), 691 to 703 (1976)"
    locator: the section on 2-SAT and limited backtracking
  - paper: doi:10.1137/0208032
    title: Leslie G. Valiant, The complexity of enumeration and reliability problems, SIAM Journal on Computing 8(3), 410 to 421 (1979)
    locator: "the #P-completeness of counting the models of monotone 2-CNF formulas"
  - paper: "Christos H. Papadimitriou, On selecting a satisfying truth assignment, Proceedings of the 32nd IEEE Symposium on Foundations of Computer Science (FOCS 1991), 163 to 169"
    locator: the random walk algorithm for 2-SAT and its expected number of flips
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2 (2022)
    locator: Section 7.2.2.2, Satisfiability (2SAT and the implication digraph)
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity (1994)
    locator: Chapter 9, Section 9.2 (2SAT and its place in NL)
---

2-SAT is the [satisfiability problem](/sat/) for formulas in [conjunctive normal form](/conjunctive-normal-form/) where each [clause](/clause/) has at most two [literals](/literal/). Unlike [3-SAT](/3-sat/), which is NP-complete, 2-SAT is solvable in $\Theta(n + m)$ time by the [2-SAT algorithm](/two-sat-algorithm/) of Aspvall, Plass and Tarjan, which works on the [implication graph](/implication-graph/). The counting version and the maximization version, [MAX-2-SAT](/max-2-sat/), are hard. This page covers the problem; the algorithm has its own page.

## In plain words

You have a list of yes-or-no choices, and a list of rules. Each rule names at most two choices and says that at least one of them must go a certain way, for example "Ann gets the morning shift, or Bob gets the evening shift". The question is whether some way of making all the choices obeys every rule, and if so, which way.

Rules with two parts are easy to reason about. Each rule says "if this one goes wrong, then that one must go right". These "if, then" steps form chains. A contradiction exists only when a chain leads from a choice to its opposite and back. A fast search for such chains solves the problem in time that grows in proportion to the size of the rule list. With three parts in a rule, no fast method is known.

## Definition

We use the notation of the area: $n$ is the number of variables, $m$ the number of clauses, and a literal is $x_v$ or $\neg x_v$.

**Input.** A formula $F = C_1 \wedge \cdots \wedge C_m$ over the variables $x_1, \ldots, x_n$, where each clause $C_j$ is a set of at most two literals. Such a formula is a *2-CNF formula*, also called a *Krom formula*.

**Output.** The decision version asks whether there is an assignment $x \in \{0,1\}^n$ that makes each clause true:

$$\exists x \in \{0,1\}^n \ \forall j \in \{1, \ldots, m\} \ \exists \ell \in C_j : \ell \text{ is true under } x.$$

The search version also asks for such an $x$, a *model*, when one exists.

## Variants

- **Search.** Output a model. The [2-SAT algorithm](/two-sat-algorithm/) gives one at no extra cost.
- **Forced literals.** Find the literals that are true in each model, the [backbone](/backbone/). In a satisfiable 2-CNF formula, $\ell$ is false in each model exactly when the implication graph has a path from $\ell$ to $\neg\ell$, so the backbone also takes polynomial time.
- **Counting (#2-SAT).** Count the models. This is [#P-complete](/model-counting/), even for monotone formulas, where no literal is negated (Valiant 1979).
- **Maximization.** Satisfy as many clauses as possible. This is [MAX-2-SAT](/max-2-sat/), which is NP-hard.
- **Fewest true variables.** Find a model with the fewest true variables. This is NP-hard: for a graph, the monotone formula with the clause $(x_u \vee x_v)$ for each edge has as models exactly the [vertex covers](/vertex-cover/).
- **Quantified 2-CNF.** Each variable is under $\exists$ or $\forall$. The general [QBF](/qbf/) problem is PSPACE-complete, but with a 2-CNF matrix it takes linear time (Aspvall, Plass and Tarjan 1979).

## Examples

**A satisfiable formula with one model.** The formula

$$F = (x_1 \vee x_2) \wedge (\neg x_1 \vee x_3) \wedge (\neg x_2 \vee x_3) \wedge (\neg x_3 \vee x_4) \wedge (\neg x_4 \vee \neg x_1)$$

has exactly one model of the 16 assignments: $x = (0, 1, 1, 1)$. The chain $x_1 \Rightarrow x_3 \Rightarrow x_4 \Rightarrow \neg x_1$ shows that $x_1$ must be false, and then the clause $(x_1 \vee x_2)$ forces $x_2$, which forces $x_3$ and $x_4$. The [2-SAT algorithm](/two-sat-algorithm/) page traces the run on this formula.

**An unsatisfiable formula.** Add the clause $(x_1 \vee \neg x_2)$ to $F$. Now $x_1 = 0$ forces $x_2 = 0$, and the clause $(x_1 \vee x_2)$ is false. No assignment satisfies all six clauses.

**Two-coloring a cycle.** Color each vertex of a graph with color 0 or 1 so that each edge has two colors. For an edge $\{u, w\}$, add the clauses $(x_u \vee x_w)$ and $(\neg x_u \vee \neg x_w)$. A 4-cycle gives 8 clauses with 2 models, the two proper colorings. A triangle gives 6 clauses with no model, because an odd cycle has no 2-coloring.

**A non-example.** The clause $(x_1 \vee x_2 \vee x_3)$ has three literals, so a formula with it is not in 2-CNF. It cannot be written as a 2-CNF formula over the same variables. Such a formula would need a clause that is false at $(0,0,0)$. That clause has only positive literals, at most two of them, so it misses some $x_i$. Then it is also false at the assignment where only $x_i$ is 1, which is a model of $(x_1 \vee x_2 \vee x_3)$.

## Known algorithms

| algorithm | bound | case |
|---|---|---|
| [2-SAT algorithm](/two-sat-algorithm/) (Aspvall, Plass and Tarjan 1979) | $\Theta(n + m)$ | worst case, deterministic |
| Limited backtracking with [unit propagation](/unit-propagation/) (Even, Itai and Shamir 1976) | $O(n (n + m))$ for a simple version | worst case, deterministic |
| Resolution closure | $O(n^3)$ resolvents for a simple version | worst case, deterministic |
| Random walk (Papadimitriou 1991) | at most $n^2$ flips in expectation | expected, on satisfiable inputs only |

The resolution closure works because the resolvent of two clauses of size at most 2 has size at most 2. There are at most $(2n)^2 + 2n + 1$ such clauses, so the closure under [resolution](/robinson-resolution/) is reached after a polynomial number of steps, and it holds the empty clause exactly when $F$ is unsatisfiable. The random walk is analyzed on the page on [Schöning's algorithm](/schoning-algorithm/); it cannot prove that a formula is unsatisfiable.

## Bounds

- **Upper bound.** $O(n + m)$ time on the [word RAM](/word-ram/), by the [2-SAT algorithm](/two-sat-algorithm/).
- **Lower bound.** Take the inputs where each clause is $(x_1)$, except one clause, which is $(x_1)$ or $(\neg x_1)$. An algorithm that does not read that clause gives the same answer on both inputs, but one is satisfiable and the other is not. So a correct algorithm reads all $m$ clauses in the worst case, and the search version also writes $n$ values. So $\Omega(n + m)$ time is needed, and the linear bound is tight.
- **Space.** 2-SAT is complete for nondeterministic logarithmic space ([NL](/nondeterministic-logspace/)) under logspace reductions. The unsatisfiability test is a reachability question on the implication graph.

## Reductions

- **To strongly connected components.** The [2-SAT algorithm](/two-sat-algorithm/) reduces 2-SAT to the [strongly connected components](/strongly-connected-components/) of a graph with $2n$ vertices and $2m$ arcs, in linear time.
- **From 2-coloring.** A graph is bipartite if and only if the formula of the 2-coloring example is satisfiable. The reduction takes linear time.
- **Place in Schaefer's theorem.** 2-CNF formulas are the bijunctive case of [Schaefer's dichotomy theorem](/schaefer-dichotomy-theorem/). The other tractable cases include [Horn-SAT](/horn-sat/) and [XOR-SAT](/xor-sat/), and all other Boolean constraint languages give NP-complete problems.
- **The boundary at three.** Each CNF formula reduces to [3-SAT](/3-sat/) in polynomial time, and 3-SAT is NP-complete. A polynomial-time reduction from 3-SAT to 2-SAT would give P = NP, so none is known.

## Applications

- **Two-choice constraints.** Scheduling with two options for each task, the placement of map labels in one of two positions, and the orientation of items that can face one of two ways, where each conflict forbids one pair of options.
- **Inside SAT solvers.** The binary clauses of a general CNF formula form an implication graph. Solvers use it for [equivalent literal substitution](/equivalent-literal-substitution/) and [failed literal probing](/failed-literal-probing/).
- **Teaching.** It is the standard example of a special case of SAT that is in P, and of an application of strongly connected components.

## References
