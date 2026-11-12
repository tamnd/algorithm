---
tag: PCCASC
kind: problem
slug: datalog-evaluation
name: Datalog evaluation problem
aliases:
- recursive query evaluation
- Datalog query evaluation
area: systems/database-algorithms
level: advanced
summary: "Given a Datalog program and a database, compute the least fixed point of the rules, or the facts of it that a query asks for. P-complete in the data and EXPTIME-complete in the program."
prereqs: [datalog]
see_also: [semi-naive-evaluation, magic-sets, dred-algorithm, horn-sat-forward-chaining, sld-resolution, transitive-closure, circuit-value-problem, generic-join]
sources:
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 12 (Datalog) and Chapter 13 (evaluation of Datalog), bottom-up and top-down evaluation, the semi-naive method and magic sets
  - paper: doi:10.1145/502807.502810
    title: Evgeny Dantsin, Thomas Eiter, Georg Gottlob and Andrei Voronkov, Complexity and expressive power of logic programming, ACM Computing Surveys 33(3), 374 to 425 (2001)
    locator: data complexity P-complete and program and combined complexity EXPTIME-complete for Datalog, and linear time for ground programs
  - paper: doi:10.1145/227595.227597
    title: Weidong Chen and David S. Warren, Tabled evaluation with delaying for general logic programs, Journal of the ACM 43(1), 20 to 74 (1996)
    locator: SLG resolution, top-down evaluation with tables that stops on all function-free programs
  - paper: doi:10.1109/69.43410
    title: Stefano Ceri, Georg Gottlob and Letizia Tanca, What you always wanted to know about Datalog (and never dared to ask), IEEE Transactions on Knowledge and Data Engineering 1(1), 146 to 166 (1989)
    locator: survey of bottom-up and top-down evaluation methods and their optimizations
---

The Datalog evaluation problem asks for the result of a [Datalog](/datalog/) program on a database: the least fixed point of its rules, or the part of it that a query asks for. The simplest method, naive evaluation, applies all rules to all known facts until nothing new appears. It is forward chaining, a relation at a time. Better methods avoid repeated work ([semi-naive evaluation](/semi-naive-evaluation/)), restrict the work to the facts that a query needs ([magic sets](/magic-sets/)), or work top down from the query with tables of answers (SLG resolution). For a fixed program the problem takes polynomial time in the size of the database and is P-complete. With the program as part of the input it is EXPTIME-complete.

## In plain words

A Datalog program is a list of rules such as "if x is a parent of y, and y is an ancestor of z, then x is an ancestor of z", together with a table of stored facts. Evaluating it means finding every fact that the rules make true. You can start from the stored facts and apply the rules again and again until nothing new appears. Or you can start from a question, such as "who are the ancestors of Ann?", and only look for the facts that help answer it.

The work always ends, because the rules cannot invent new names, so there are only finitely many possible facts. The hard part is to avoid doing the same work many times and to avoid computing facts that nobody asked for.

## Definition

**Input.** A Datalog program $P$, a finite set $D$ of EDB facts, and possibly a query atom $q(\bar t)$, whose terms are constants and variables.

**Output.** The least model $P(D)$, which is the least fixed point of the immediate consequence operator $T_P$ that contains $D$. With a query atom, the output is the set of facts of $P(D)$ that match $q(\bar t)$.

**Decision version.** Given $P$, $D$ and a ground fact $f$, is $f \in P(D)$?

The least fixed point exists and is reached after finitely many applications of $T_P$, because $T_P$ is monotone and the number of possible facts is finite: with $n$ constants and IDB predicates of arity at most $a$, there are at most $p \cdot n^a$ IDB facts for $p$ IDB predicates.

## Variants

- **Data complexity.** The program is fixed and only $D$ is the input. This is the usual view for a database query.
- **Combined complexity.** Both $P$ and $D$ are the input. The arities and the number of variables in a rule now matter.
- **Query with bound arguments.** The query atom has constants, as in $\mathit{path}(1, y)$. Only the facts on which the answer depends need to be computed.
- **Stratified negation.** Negated atoms on predicates of lower strata. Evaluate stratum by stratum, each as a least fixed point.
- **Incremental evaluation.** After a change of $D$, update $P(D)$ instead of computing it again; see the [DRed algorithm](/dred-algorithm/).
- **Ground programs.** If $P$ has no variables, it is a propositional Horn formula, and the problem is [Horn-SAT](/horn-sat/).

## Examples

**Transitive closure.** With $\mathit{path}(x, y) \leftarrow \mathit{edge}(x, y)$ and $\mathit{path}(x, y) \leftarrow \mathit{edge}(x, z), \mathit{path}(z, y)$, the least model holds all pairs joined by a path. On a chain $1 \to 2 \to \cdots \to n$ it has $n(n-1)/2$ $\mathit{path}$ facts, and naive evaluation needs $n$ rounds.

**A query that needs little.** For the query $\mathit{path}(n - 1, y)$ on the same chain, only one answer, $\mathit{path}(n - 1, n)$, exists. Bottom-up evaluation still derives all $n(n-1)/2$ facts. A top-down or magic-sets evaluation derives only the facts about nodes reachable from $n - 1$.

**Same generation.** With $\mathit{sg}(x, y) \leftarrow \mathit{flat}(x, y)$ and $\mathit{sg}(x, y) \leftarrow \mathit{up}(x, u), \mathit{sg}(u, v), \mathit{down}(v, y)$, two nodes are in the same generation when they are connected by a path that goes up some steps, across one flat edge, and down the same number of steps. This is the classic test case for recursive query methods.

**Left recursion.** With the rule $\mathit{path}(x, y) \leftarrow \mathit{path}(x, z), \mathit{edge}(z, y)$ and a cycle in $\mathit{edge}$, plain Prolog-style [SLD resolution](/sld-resolution/) loops forever on $\mathit{path}(1, y)$, although the least model is finite. Bottom-up methods and tabling stop.

## Known algorithms

- **Naive evaluation.** $M \leftarrow D$; repeat $M \leftarrow M \cup T_P(M)$ until $M$ does not change. Each round evaluates each rule as a join of its body relations followed by a projection on the head. It is [forward chaining](/horn-sat-forward-chaining/) done with relational operators, and it repeats every derivation in every later round.
- **Semi-naive evaluation.** In each round, use only rule instances with at least one fact that is new from the last round. Same result, and with the refined form each derivation is done once. See [semi-naive evaluation](/semi-naive-evaluation/).
- **Magic sets.** For a query with bound arguments, rewrite the program so that bottom-up evaluation only derives facts that are relevant to the query, then evaluate it semi-naively. See [magic sets](/magic-sets/).
- **Top-down evaluation with tabling.** Start from the query, as in SLD resolution, but keep a table of the calls made and the answers found for each call. A call that is already in the table is not evaluated again; it consumes the answers of the table as they appear. With no function symbols there are finitely many calls and answers, so the method stops. SLG resolution (Chen and Warren 1996) is this method for general logic programs, and it is the basis of XSB. Earlier methods of this kind are query-subquery evaluation (Vieille 1986) and OLDT resolution (Tamaki and Sato 1986). Magic sets and tabling find essentially the same set of relevant facts.
- **Grounding and Horn-SAT.** Replace the program by all its ground instances over the constants and compute the least model of the propositional Horn formula in linear time in its size (Dowling and Gallier 1984). The grounding has up to $r n^v$ clauses for $r$ rules with $v$ variables, so this is practical only for small $v$.
- **Join algorithms.** Inside each round, a rule body is a conjunctive query, and its join can use any join method, including worst-case optimal joins such as [generic join](/generic-join/).

## Bounds

- **Data complexity: P-complete.** For a fixed program, the number of rounds and the number of rule instances are polynomial in the size of $D$. P-hardness holds already for a fixed program that evaluates monotone circuits; see the [circuit value problem](/circuit-value-problem/).
- **Combined and program complexity: EXPTIME-complete.** The number of facts $p \cdot n^a$ is exponential in the arity $a$. Conversely, a program with predicates of large arity over the constants 0 and 1 can simulate an exponential-time machine.
- **Bounded arity.** If the arities and the number of variables per rule are bounded, the number of rule instances is polynomial in the input, and evaluation is in polynomial time.
- **Ground programs.** Linear time in the size of the program, by forward chaining with counters.
- **Nonrecursive programs.** Evaluating a single conjunctive query rule is already NP-complete in combined complexity, by the [Chandra-Merlin theorem](/chandra-merlin-theorem/); with a fixed query it is in polynomial time and highly parallel.

## Reductions

- **From the monotone circuit value problem.** Put the gates and wires of a monotone circuit in EDB relations; four fixed rules derive the gates whose value is true. So a polynomial-time problem that is P-hard reduces to Datalog evaluation with a fixed program.
- **To Horn-SAT.** Ground the program over the constants; the least model of the ground program is the least model of $P$ on $D$.
- **Linear programs to reachability.** In a linear program each rule body has at most one IDB atom. Make a graph whose nodes are the possible IDB facts, with an edge from $g$ to $h$ for each ground rule instance with IDB body fact $g$, head $h$ and true EDB atoms. The least model is the set of facts reachable from the heads of the exit instances, so evaluation is [transitive closure](/transitive-closure/) on a larger graph.
- **Conjunctive query evaluation.** A nonrecursive rule is a conjunctive query, and its evaluation is a [constraint satisfaction problem](/constraint-satisfaction-problem/).

## Applications

- **Deductive databases and recursive SQL.** Recursive views, bill-of-materials queries and graph reachability in SQL (WITH RECURSIVE) are evaluated by semi-naive iteration.
- **Program analysis.** Points-to analysis, call-graph construction and taint analysis are written as Datalog programs and run on engines such as Soufflé and the Doop framework.
- **Networking and distributed systems.** Declarative networking writes routing protocols as Datalog rules evaluated in a distributed way.
- **Knowledge graphs and ontologies.** Rule-based reasoning over RDF data, such as the OWL 2 RL profile, is Datalog evaluation.
- **Security policies.** Access control languages based on Datalog decide whether a request follows from the policy facts.

## References
