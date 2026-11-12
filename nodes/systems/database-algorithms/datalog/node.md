---
tag: QGDDAD
kind: model
slug: datalog
name: Datalog
aliases:
- recursive Horn-clause queries
- function-free Horn logic programs
area: systems/database-algorithms
level: advanced
summary: "A query language of function-free Horn rules over relations. Its meaning is the least fixed point of the rules, which adds recursion to the select-project-join-union queries."
prereqs: [relational-algebra, horn-clause]
see_also: [datalog-evaluation, semi-naive-evaluation, magic-sets, logic-programming, horn-sat-forward-chaining, knaster-tarski-theorem, transitive-closure, query-containment-problem]
sources:
  - paper: doi:10.1145/321978.321991
    title: Maarten H. van Emden and Robert A. Kowalski, The semantics of predicate logic as a programming language, Journal of the ACM 23(4), 733 to 742 (1976)
    locator: the least Herbrand model of a set of Horn clauses equals the least fixed point of the immediate consequence operator
  - paper: doi:10.1145/502807.502810
    title: Evgeny Dantsin, Thomas Eiter, Georg Gottlob and Andrei Voronkov, Complexity and expressive power of logic programming, ACM Computing Surveys 33(3), 374 to 425 (2001)
    locator: the data complexity (P-complete) and the combined and program complexity (EXPTIME-complete) of Datalog, and of its extensions with negation
  - paper: "Krzysztof R. Apt, Howard A. Blair and Adrian Walker, Towards a theory of declarative knowledge, in Jack Minker (ed.), Foundations of Deductive Databases and Logic Programming, Morgan Kaufmann (1988), pages 89 to 148"
    locator: stratified programs with negation and their standard model, which does not depend on the stratification
  - paper: doi:10.1109/69.43410
    title: Stefano Ceri, Georg Gottlob and Letizia Tanca, What you always wanted to know about Datalog (and never dared to ask), IEEE Transactions on Knowledge and Data Engineering 1(1), 146 to 166 (1989)
    locator: survey of the syntax, the semantics and the evaluation of Datalog
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 12 (Datalog, its model-theoretic, fixpoint and proof-theoretic semantics) and Chapter 15 (negation in Datalog)
---

Datalog is a query language for relational databases in which a query is a finite set of rules. Each rule says that a fact holds when some other facts hold, as a [Horn clause](/horn-clause/) without function symbols. Rules can be recursive, so Datalog expresses queries such as the [transitive closure](/transitive-closure/) of a graph, which [relational algebra](/relational-algebra/) cannot express. The meaning of a program is its least model, which equals the least fixed point of its immediate consequence operator (van Emden and Kowalski 1976). Every program stops on every finite database. With the program fixed, a query takes polynomial time, and the problem is P-complete. With the program as part of the input, it is EXPTIME-complete. Datalog is the core of deductive databases and of many program analysis and network tools, and SQL has a form of it as recursive queries.

## The machine

**Syntax.** Fix a set of predicate names, each with an arity, split into *extensional* (EDB) predicates, which are the stored relations, and *intensional* (IDB) predicates, which the program defines. A *term* is a variable or a constant. An *atom* is $p(t_1, \ldots, t_k)$ with $p$ of arity $k$. A *rule* is

$$H \leftarrow B_1, \ldots, B_m,$$

where the *head* $H$ is an atom with an IDB predicate and the *body* $B_1, \ldots, B_m$ is a list of atoms. A rule must be *safe*: each variable of the head occurs in the body. A *program* $P$ is a finite set of rules. A *database* $D$ is a finite set of ground EDB facts. There are no function symbols, so the only values are the constants of $D$ and of $P$, a finite set $\mathit{adom}$.

**Example.** With the EDB predicate $\mathit{edge}$, this program computes the pairs of nodes joined by a path:

$$\begin{aligned}
\mathit{path}(x, y) &\leftarrow \mathit{edge}(x, y),\\
\mathit{path}(x, y) &\leftarrow \mathit{edge}(x, z), \mathit{path}(z, y).
\end{aligned}$$

**Semantics.** Let $I$ be a set of ground facts over $\mathit{adom}$. The *immediate consequence operator* is

$$T_P(I) = D \cup \{\, \theta(H) \;:\; (H \leftarrow B_1, \ldots, B_m) \in P,\ \theta \text{ maps the variables to } \mathit{adom},\ \theta(B_i) \in I \text{ for all } i \,\}.$$

$T_P$ is monotone: $I \subseteq J$ implies $T_P(I) \subseteq T_P(J)$. The sets of facts over $\mathit{adom}$ form a finite complete lattice, so by the [Knaster-Tarski theorem](/knaster-tarski-theorem/) $T_P$ has a least [fixed point](/fixed-point/), and the chain $\emptyset \subseteq T_P(\emptyset) \subseteq T_P^2(\emptyset) \subseteq \cdots$ reaches it after at most $N$ steps, where $N$ is the number of possible IDB facts. Three definitions of the meaning $P(D)$ agree:

- *model-theoretic:* the least set of facts that contains $D$ and satisfies each rule, read as a first-order sentence with its variables universally quantified;
- *fixed-point:* the least fixed point of $T_P$;
- *proof-theoretic:* the set of facts that have a finite derivation tree, whose leaves are facts of $D$ and whose inner nodes are rule applications.

The equality of the first two is the theorem of van Emden and Kowalski. A query is the program together with one IDB predicate whose facts are the answer.

**Run on the example.** Let $D = \{\mathit{edge}(1, 2), \mathit{edge}(2, 3), \mathit{edge}(3, 4)\}$. The first stage adds $\mathit{path}(1, 2)$, $\mathit{path}(2, 3)$ and $\mathit{path}(3, 4)$ by the first rule. The second stage adds $\mathit{path}(1, 3)$ and $\mathit{path}(2, 4)$ by the second rule. The third stage adds $\mathit{path}(1, 4)$. The fourth stage adds nothing, so the least fixed point has six $\mathit{path}$ facts.

**Negation.** Plain Datalog has no negation. *Stratified* Datalog allows negated body atoms $\neg q(\bar t)$ when the program splits into strata such that a predicate that is negated is fully defined in a lower stratum. For example, $\mathit{unreach}(x, y) \leftarrow \mathit{node}(x), \mathit{node}(y), \neg\,\mathit{path}(x, y)$ uses $\mathit{path}$ from a lower stratum. The strata are computed bottom up, each as a least fixed point with the lower strata fixed. The result, the *perfect model*, does not depend on the choice of the stratification (Apt, Blair and Walker 1988). A rule such as $\mathit{win}(x) \leftarrow \mathit{move}(x, y), \neg\,\mathit{win}(y)$ has recursion through negation and is not stratified. Such programs need the well-founded or the stable model semantics.

## What it counts

- **Data complexity.** The program is fixed and the database $D$ of size $n$ is the input. The number of possible IDB facts is $O(n^a)$, where $a$ is the largest arity, so the least fixed point is reached in polynomial time. This is the main measure for database queries.
- **Combined and program complexity.** The program is part of the input. The number of possible facts and the number of stages can be exponential in the arities, and evaluation is EXPTIME-complete.
- **Stages.** The number of applications of $T_P$ before the fixed point. For the path program on a path of $n$ nodes, $n - 1$ stages add facts, and one more stage finds nothing new. A program is *bounded* when this number has a bound that does not depend on $D$; then it is equivalent to a nonrecursive program.
- **Derivations.** Practical cost measures count the facts derived and the rule instances fired. [Semi-naive evaluation](/semi-naive-evaluation/) reduces the second number, and [magic sets](/magic-sets/) reduce the first one for queries with constants.

## Relation to other models

- **Relational algebra.** A nonrecursive Datalog program is equivalent to a union of conjunctive queries, that is, to a positive relational algebra expression with selection, projection, join and union. Recursion adds power: transitive closure is not expressible in relational algebra (Aho and Ullman 1979). Relational algebra has difference, which Datalog without negation does not have, so the two languages are incomparable.
- **Logic programming.** A Datalog program is a [logic program](/logic-programming/) without function symbols. Prolog evaluates it top-down by [SLD resolution](/sld-resolution/), which can loop on left-recursive rules such as $\mathit{path}(x, y) \leftarrow \mathit{path}(x, z), \mathit{edge}(z, y)$. Datalog uses set semantics and a bottom-up or tabled evaluation, which always stops.
- **Propositional Horn logic.** Replace each rule by all its ground instances over $\mathit{adom}$. The result is a propositional Horn formula, and the least model is computed by [forward chaining](/horn-sat-forward-chaining/) as in [Horn-SAT](/horn-sat/). Naive Datalog evaluation is forward chaining, done a relation at a time.
- **Fixed-point logic.** Datalog is the existential, negation-free part of least fixed-point logic. Its queries are monotone and preserved under homomorphisms, so it cannot express "the graph has no path from $a$ to $b$" or "the number of nodes is even".
- **SQL.** The recursive common table expressions of SQL (WITH RECURSIVE) express linear Datalog rules, such as the path program above.

## Known results in the model

- **Least model equals least fixed point** (van Emden and Kowalski 1976), equal also to the set of facts with a derivation tree.
- **Data complexity is P-complete.** Evaluation is in polynomial time for a fixed program. It is P-hard by a reduction from the monotone [circuit value problem](/circuit-value-problem/): with EDB relations for the inputs that are true and for the AND and OR gates, the fixed rules $\mathit{true}(g) \leftarrow \mathit{input}(g)$, $\mathit{true}(g) \leftarrow \mathit{and}(g, a, b), \mathit{true}(a), \mathit{true}(b)$, $\mathit{true}(g) \leftarrow \mathit{or}(g, a, b), \mathit{true}(a)$ and $\mathit{true}(g) \leftarrow \mathit{or}(g, a, b), \mathit{true}(b)$ derive exactly the gates whose value is true. See Dantsin, Eiter, Gottlob and Voronkov (2001).
- **Combined complexity is EXPTIME-complete.** The program can encode the run of an exponential-time machine, because a predicate of arity $k$ over two constants has $2^k$ facts.
- **Capturing polynomial time.** On databases that also store a successor relation of a linear order of the domain, with its first and last elements, Datalog with negation of EDB atoms, and also stratified Datalog, express exactly the queries computable in polynomial time.
- **Static analysis is undecidable.** Containment and equivalence of Datalog programs (Shmueli 1993) and boundedness (Gaifman, Mairson, Sagiv and Vardi 1987) are undecidable. Containment of a union of conjunctive queries in a Datalog program is decidable; see the [query containment problem](/query-containment-problem/).
- **Evaluation methods.** Naive and semi-naive bottom-up iteration, the magic sets rewriting for queries with bound arguments, and top-down evaluation with tabling all compute the least model or the part of it that a query needs; see [Datalog evaluation](/datalog-evaluation/). The [DRed algorithm](/dred-algorithm/) maintains the least model when the database changes.

## References
