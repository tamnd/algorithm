---
tag: 6XE08Y
kind: problem
slug: horn-sat
name: Horn-SAT
aliases:
- Horn formula satisfiability
- HORNSAT
area: logic-and-constraints/sat-solving
level: core
summary: SAT where each clause has at most one positive literal. Solvable in linear time by forward chaining, and a satisfiable instance has a least model.
prereqs: [sat, conjunctive-normal-form, horn-clause]
see_also: [horn-sat-forward-chaining, 2-sat, xor-sat, unit-propagation, datalog, logic-programming, schaefer-dichotomy-theorem, model-counting]
sources:
  - paper: doi:10.1016/0743-1066(84)90014-1
    title: William F. Dowling and Jean H. Gallier, Linear-time algorithms for testing the satisfiability of propositional Horn formulae, Journal of Logic Programming 1(3), 267 to 284 (1984)
    locator: the whole paper
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity (1994)
    locator: Chapter 4, Section 4.2 (HORNSAT in polynomial time), and Chapter 8 (P-completeness)
  - paper: doi:10.1137/0208032
    title: Leslie G. Valiant, The complexity of enumeration and reliability problems, SIAM Journal on Computing 8(3), 410 to 421 (1979)
    locator: "the #P-completeness of counting the models of monotone 2-CNF formulas"
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2 (2022)
    locator: Section 7.2.2.2, Satisfiability (Horn clauses)
---

Horn-SAT is the [satisfiability problem](/sat/) for CNF formulas where each clause has at most one positive literal, the [Horn clauses](/horn-clause/). It is solvable in time linear in the size of the formula by [forward chaining](/horn-sat-forward-chaining/) (Dowling and Gallier 1984). A satisfiable Horn formula has a least model, the intersection of all its models, and this model is the meaning of a [Datalog](/datalog/) program or a [logic program](/logic-programming/) without negation. This page covers the problem; the algorithm has its own page.

## In plain words

A Horn rule has the form "if these facts all hold, then that fact holds", or "these facts never all hold together". A rule with no "if" part is a plain fact. The question is whether all the rules can hold at once.

The answer is easy to find. Start from the plain facts, and apply the rules forward as long as some rule gives a new fact. If a rule of the "never together" kind fires, the rules contradict each other. Otherwise, the facts you found, and nothing else, make all the rules hold. You only add facts that the rules force, so this answer also makes as few facts true as possible. With rules that may end in "this or that", the problem becomes as hard as general satisfiability.

## Definition

We use the notation of the area: $n$ variables, $m$ clauses, and $|F|$ literal occurrences.

**Horn clause.** A clause with at most one positive literal. As an implication, $(\neg x_1 \vee \cdots \vee \neg x_k \vee x_h)$ is the rule $x_1 \wedge \cdots \wedge x_k \Rightarrow x_h$, and $(\neg x_1 \vee \cdots \vee \neg x_k)$ is the goal clause $x_1 \wedge \cdots \wedge x_k \Rightarrow \bot$. With $k = 0$ the first form is a fact $x_h$, and the second is the empty clause.

**Input.** A formula $F = C_1 \wedge \cdots \wedge C_m$ over $x_1, \ldots, x_n$ where each $C_j$ is a Horn clause.

**Output.** The decision version asks whether some $x \in \{0,1\}^n$ makes each clause true. The search version also asks for a model. The usual algorithms return the *least model*: the model $x^*$ with $x^* \le x$ for each model $x$, where $\le$ is the order of each coordinate.

**Least model theorem.** If a Horn formula has a model, then the intersection of all its models is a model, so the least model exists. The proof on the page of [forward chaining](/horn-sat-forward-chaining/) builds it: the algorithm returns a model in which each true variable is true in each model.

## Variants

- **Entailment.** Does $F$ imply $x_v$? This holds exactly when $F \wedge (\neg x_v)$ has no model. That formula is again Horn, so entailment is also linear. When $F$ is satisfiable, $F$ implies $x_v$ exactly when $x_v$ is true in the least model.
- **Dual Horn.** Each clause has at most one negative literal. Flip the sign of each variable to get a Horn formula; its least model gives the greatest model of the original.
- **Renamable Horn.** Some set of sign flips makes the formula Horn. Finding the set is a [2-SAT](/2-sat/) question.
- **Counting.** Counting the models of a Horn formula is [#P-complete](/model-counting/). *Proof.* Counting the models of a monotone 2-CNF formula, with clauses $(x_u \vee x_w)$, is #P-complete (Valiant 1979). Replace each $x_v$ by $\neg y_v$. Each clause becomes $(\neg y_u \vee \neg y_w)$, which is Horn, and the map $y = \neg x$ is a bijection of the models. So the count is the same.
- **Maximization.** Satisfying the most clauses of a Horn formula is NP-hard. *Proof.* Reduce from [independent set](/independent-set/) in a graph with $n$ vertices. Take the fact $(x_v)$ for each vertex, and $n + 1$ copies of the goal clause $(\neg x_u \vee \neg x_w)$ for each edge. Breaking one edge clause loses $n + 1$ clauses, more than all facts together, so an optimal assignment satisfies all edge clauses. Its true variables then form an independent set, and the number of true facts is its size. So the optimum is the edge count times $n + 1$ plus the size of a largest independent set.

## Examples

**A satisfiable formula.** The seven clauses

$$x_1,\quad x_1 \Rightarrow x_2,\quad x_1 \wedge x_2 \Rightarrow x_3,\quad x_3 \wedge x_4 \Rightarrow x_5,\quad x_2 \wedge x_5 \Rightarrow \bot,\quad x_4 \Rightarrow x_1,\quad x_3 \Rightarrow x_6$$

have exactly one model of the 64 assignments: $x_1 = x_2 = x_3 = x_6 = 1$ and $x_4 = x_5 = 0$. Forward chaining derives $x_1$, $x_2$, $x_3$ and $x_6$ in four steps. The [forward chaining](/horn-sat-forward-chaining/) page shows the run with the counters.

**An unsatisfiable formula.** Add the fact $x_4$. Then $x_3 \wedge x_4$ gives $x_5$, and $x_2 \wedge x_5 \Rightarrow \bot$ fires.

**Intersection, not union.** The formula $(\neg x_1 \vee \neg x_2)$ has the models $00$, $01$ and $10$. The intersection of any two of them is a model, as the theorem says. The union of $01$ and $10$ is $11$, which is not a model. So Horn formulas have a least model but no greatest model in general.

**A non-example.** $(x_1 \vee x_2)$ has two positive literals, so it is not Horn. Its models $01$ and $10$ have the intersection $00$, which is not a model. So no Horn formula over $x_1, x_2$ has the same models.

## Known algorithms

| algorithm | bound | notes |
|---|---|---|
| [Forward chaining](/horn-sat-forward-chaining/) (Dowling and Gallier 1984) | $\Theta(n + m + \lvert F \rvert)$ worst case | returns the least model |
| Naive fixed point: rescan all clauses until no change | $O(n \cdot \lvert F \rvert)$ worst case | at most $n$ rounds, since each round sets a new variable or stops |
| [Unit propagation](/unit-propagation/), as in [DPLL](/dpll/) | linear with counters or watched literals | complete for Horn formulas: no decision is needed |
| [SLD resolution](/sld-resolution/) (backward chaining) | can loop on a cyclic rule such as $x_1 \Rightarrow x_1$ without tabling | answers one query, as in Prolog |

## Bounds

- **Upper bound.** $O(n + m + |F|)$ time on the [word RAM](/word-ram/), by forward chaining.
- **Lower bound.** $\Omega(m + |F|)$ in the worst case, and $\Omega(n)$ to write a model. Take $m - 1$ copies of $(x_1)$ and one clause that is $(x_1)$ or $(\neg x_1)$: an algorithm that does not read the last clause gives the same answer on two inputs with different answers. For literals, take the facts $x_1, \ldots, x_k$ and the goal clause $(\neg x_1 \vee \cdots \vee \neg x_k)$, which is false. Changing one literal $\neg x_j$ of it to $x_j$ gives a Horn clause that is true, so each literal must be read.
- **Parallel complexity.** Horn-SAT is complete for P under logspace reductions. So it is unlikely to have a fast parallel algorithm: one in NC would give P = NC.
- **Where it sits.** Horn formulas are one of the tractable cases of [Schaefer's dichotomy theorem](/schaefer-dichotomy-theorem/). Their models are closed under coordinatewise AND, and this property defines the case.

## Reductions

- **Datalog.** A Datalog program without negation, after grounding, is a Horn formula, and its least model is the set of derived facts. Grounding can make the formula exponentially larger than the program.
- **Reachability in AND-OR graphs.** Each rule is an AND node with arcs from its body variables to its head. A variable is in the least model exactly when it is reachable in this graph, where an AND node needs all its predecessors.
- **2-SAT and XOR-SAT.** A 2-CNF formula need not be Horn, and a Horn formula need not be 2-CNF. [2-SAT](/2-sat/), Horn-SAT and [XOR-SAT](/xor-sat/) are three different tractable classes, with three different algorithms.

## Applications

- **Logic programming and deductive databases.** The least model is the meaning of a definite logic program and of a Datalog program.
- **Rule-based systems.** Expert systems, build systems that derive which targets are out of date, and access control rules all derive facts by forward chaining.
- **Program analysis.** Many analyses solve a set of Horn constraints over a finite set of facts.
- **Inside SAT solvers.** The Horn part of a formula is decided by [unit propagation](/unit-propagation/) alone, with no search.

## References
