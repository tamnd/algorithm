---
tag: BG75MM
kind: problem
slug: query-containment-problem
name: Query containment problem
aliases:
- containment of queries
- conjunctive query containment
area: systems/database-algorithms
level: advanced
summary: "Decide whether one query returns a subset of the answers of another query on every database. NP-complete for conjunctive queries and undecidable for the full relational calculus."
prereqs: [relational-model, relational-algebra]
see_also: [chandra-merlin-theorem, chase-algorithm, datalog, constraint-satisfaction-problem, treewidth, yannakakis-algorithm, query-optimization, polynomial-hierarchy]
sources:
  - paper: doi:10.1145/800105.803397
    title: Ashok K. Chandra and Philip M. Merlin, Optimal implementation of conjunctive queries in relational data bases, Proceedings of the 9th Annual ACM Symposium on Theory of Computing (STOC), 77 to 90 (1977)
    locator: containment and equivalence of conjunctive queries are NP-complete
  - paper: doi:10.1145/322217.322221
    title: Yehoshua Sagiv and Mihalis Yannakakis, Equivalences among relational expressions with the union and difference operators, Journal of the ACM 27(4), 633 to 655 (1980)
    locator: containment of unions of conjunctive queries, and the Pi-2-p-completeness of equivalence for select, project, join and union expressions
  - paper: doi:10.1006/jcss.2000.1713
    title: Phokion G. Kolaitis and Moshe Y. Vardi, Conjunctive-query containment and constraint satisfaction, Journal of Computer and System Sciences 61(2), 302 to 332 (2000)
    locator: conjunctive query containment and constraint satisfaction are the same problem, and tractable classes from bounded treewidth
  - paper: doi:10.1016/S0304-3975(99)00220-0
    title: Chandra Chekuri and Anand Rajaraman, Conjunctive query containment revisited, Theoretical Computer Science 239(2), 211 to 229 (2000)
    locator: polynomial-time containment and minimization for acyclic queries and for queries of bounded query width
  - paper: doi:10.1016/0743-1066(93)90040-N
    title: Oded Shmueli, Equivalence of DATALOG queries is undecidable, Journal of Logic Programming 15(3), 231 to 241 (1993)
    locator: containment and equivalence of Datalog programs are undecidable
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 6 (static analysis and optimization), containment of conjunctive queries and the undecidability of containment for the relational calculus
---

The query containment problem asks, for two queries $Q_1$ and $Q_2$ over the same schema, whether $Q_1(D) \subseteq Q_2(D)$ for every database $D$. Query equivalence is containment in both directions, so an optimizer that wants to replace a query by a cheaper equivalent one must solve this problem. Its difficulty depends on the query language. For conjunctive queries it is [NP-complete](/np-complete/), by the [Chandra-Merlin theorem](/chandra-merlin-theorem/). For unions of conjunctive queries it stays NP-complete. With comparisons it rises to $\Pi_2^p$. For the full relational calculus, and for [Datalog](/datalog/), it is [undecidable](/undecidability/).

## In plain words

Two people write a database question in two different ways. Do the two questions give the same answers? A first step is to ask whether one question always gives a part of the answers of the other, whatever data is stored. If yes in both directions, the questions are equal, and a database system can run whichever is faster.

The words "whatever data is stored" make this hard: there are infinitely many possible databases. For the simplest common form of question, a search for a pattern of facts, one small database built from the question itself is enough to decide. That makes the test finite, but still as hard as coloring a map with three colors. For questions that can say "not" and "for all", no program can decide it at all.

## Definition

Fix a database schema and a query language $\mathcal L$. A query $Q$ of arity $k$ maps each finite database $D$ to a finite set $Q(D)$ of $k$-tuples.

**Input.** Queries $Q_1, Q_2 \in \mathcal L$ of the same arity.

**Question.** Is $Q_1 \subseteq Q_2$, that is, $Q_1(D) \subseteq Q_2(D)$ for every finite database $D$?

$Q_1 \equiv Q_2$ (equivalence) means $Q_1 \subseteq Q_2$ and $Q_2 \subseteq Q_1$. For a Boolean query (arity 0), $Q(D)$ is either the empty set (false) or the set with the empty tuple (true), so containment means that $Q_1$ implies $Q_2$.

A *conjunctive query* (CQ) is a rule $Q(\bar x) \leftarrow R_1(\bar u_1), \ldots, R_m(\bar u_m)$, the select-project-join queries of [relational algebra](/relational-algebra/). A *union of conjunctive queries* (UCQ) is a finite union of CQs with the same arity.

## Variants

- **Conjunctive queries.** By the Chandra-Merlin theorem, $Q_1 \subseteq Q_2$ if and only if there is a homomorphism from $Q_2$ to $Q_1$, which maps the head to the head and each atom to an atom.
- **Unions of conjunctive queries.** $\bigcup_i Q_i \subseteq \bigcup_j P_j$ if and only if each $Q_i$ is contained in some $P_j$ (Sagiv and Yannakakis 1980). If the union is written inside joins, as in select, project, join and union expressions, the expansion into a UCQ can be exponential, and equivalence is $\Pi_2^p$-complete.
- **Conjunctive queries with comparisons.** With atoms $x < y$, $x \le y$ or $x \ne y$, a homomorphism is sufficient but not necessary, and the test must consider every order of the variables of $Q_1$. Containment is $\Pi_2^p$-complete.
- **Containment under dependencies.** The question is asked only over databases that satisfy a set $\Sigma$ of dependencies. First apply the [chase](/chase-algorithm/) with $\Sigma$ to $Q_1$, then look for a homomorphism from $Q_2$ to the result. This decides the question when the chase stops, for example with functional dependencies and full dependencies.
- **Datalog.** Containment of a CQ or UCQ in a Datalog program is decidable: evaluate the program on the canonical database of each CQ, as in the Chandra-Merlin theorem. Containment of a Datalog program in a UCQ is decidable but harder, and containment of one Datalog program in another is undecidable (Shmueli 1993).
- **Bag semantics.** If answers are counted with their multiplicities, the homomorphism test is no longer correct, and decidability for CQs has been open for a long time.
- **Relational calculus and relational algebra.** With negation or difference, the problem is undecidable.

## Examples

**A contained query.** Let $E$ be the edges of a graph.

$$Q_1(x) \leftarrow E(x, y), E(y, y), \qquad Q_2(x) \leftarrow E(x, u), E(u, v).$$

$Q_1$ asks for nodes with an edge to a node with a loop, and $Q_2$ for nodes at the start of a path of length 2. The map $u \mapsto y$, $v \mapsto y$ is a homomorphism from $Q_2$ to $Q_1$, so $Q_1 \subseteq Q_2$. The converse fails on the database $\{E(1, 2), E(2, 3)\}$, where $Q_2$ returns $1$ and $Q_1$ returns nothing.

**Redundant atoms.** $Q(x) \leftarrow E(x, y), E(x, z), E(z, w)$ is equivalent to $Q'(x) \leftarrow E(x, z), E(z, w)$: the identity maps $Q'$ into $Q$, and $y \mapsto z$ maps $Q$ into $Q'$. An optimizer can drop the join with $E(x, y)$.

**Triangles and colorings.** The Boolean query "the graph has a triangle" is contained in the Boolean query "the graph has a path of length 2", and not the other way.

**A comparison case.** $Q_1() \leftarrow R(x, y), R(y, x)$ is contained in $Q_2() \leftarrow R(u, v), u \le v$, because for a pair $a, b$ either $a \le b$ or $b \le a$. No single homomorphism shows it; the proof needs both orders.

**An undecidable case.** Let $\varphi$ be a first-order sentence and $Q_\varphi$ the Boolean query "$\varphi$ holds". Then $Q_\varphi \subseteq \text{false}$ holds if and only if $\varphi$ has no finite model.

## Known algorithms

- **Homomorphism search.** For CQs, search for a homomorphism from $Q_2$ to $Q_1$ by backtracking, atom by atom. This is the same as evaluating $Q_2$ on the canonical database of $Q_1$, so any CQ evaluation method works, including the methods of the [constraint satisfaction problem](/constraint-satisfaction-problem/). The time is exponential in the size of $Q_2$ in the worst case and polynomial in the size of $Q_1$ for a fixed $Q_2$.
- **Acyclic and bounded-treewidth queries.** If $Q_2$ is acyclic, the [Yannakakis algorithm](/yannakakis-algorithm/) evaluates it on the canonical database of $Q_1$ in polynomial time. If the query graph of $Q_2$ has [treewidth](/treewidth/) at most $k$, dynamic programming over a tree decomposition decides containment in polynomial time for fixed $k$ (Kolaitis and Vardi 2000). Chekuri and Rajaraman (2000) gave the same for queries of bounded query width, a measure of cyclicity under which the acyclic queries have width 1.
- **UCQs.** Test each pair $Q_i$, $P_j$ with the CQ test.
- **Comparisons.** Try each linear order of the variables of $Q_1$ that is consistent with its comparisons, and test containment in each case.
- **Chase.** Under dependencies, chase $Q_1$ first.

## Bounds

| query language | complexity of containment |
|---|---|
| CQ, with $Q_2$ of bounded treewidth | in [P](/p/) |
| CQ | NP-complete |
| UCQ | NP-complete |
| CQ with comparisons $<, \le, \ne$ | $\Pi_2^p$-complete |
| select, project, join and union expressions (equivalence) | $\Pi_2^p$-complete |
| UCQ in Datalog | [EXPTIME](/exptime/)-complete |
| Datalog in Datalog | undecidable |
| relational calculus, relational algebra | undecidable |

The NP lower bound holds already for Boolean CQs over one binary relation. The [polynomial hierarchy](/polynomial-hierarchy/) class $\Pi_2^p$ is the class of problems of the form "for all $y$ there is $z$" with polynomial checks.

## Reductions

- **From 3-coloring.** A graph $G$ is 3-colorable if and only if the Boolean CQ of the triangle is contained in the Boolean CQ of $G$, both written with the edges in both directions. This shows NP-hardness for CQs.
- **To and from constraint satisfaction.** $Q_1 \subseteq Q_2$ for CQs if and only if the structure of $Q_2$ maps homomorphically to the structure of $Q_1$. This is the constraint satisfaction problem, so the [CSP dichotomy](/csp-dichotomy-theorem/) and the tractable classes of CSPs transfer to containment (Kolaitis and Vardi 2000).
- **From finite satisfiability.** By Trakhtenbrot's theorem, it is undecidable whether a first-order sentence has a finite model. The example above reduces this question to containment, so containment for the relational calculus is undecidable. A counterexample to containment is a finite database, which can be found by enumeration, so the problem is co-recursively enumerable.
- **Equivalence and containment.** Equivalence is two containment tests. For CQs, containment also reduces to equivalence: $Q_1 \subseteq Q_2$ if and only if $Q_1 \equiv Q_1 \wedge Q_2$, the CQ with both bodies and the heads made equal.

## Applications

- **Query optimization.** Removing redundant joins from a CQ uses one containment test for each atom. The result is the core of the query, which is unique.
- **Answering queries using views.** In data integration and in query caching, a query must be rewritten in terms of stored views, and each candidate rewriting is checked by containment.
- **Static analysis.** Containment shows that a query returns nothing on some branch, that an integrity constraint makes a query redundant, or that one access policy is stricter than another.
- **Recursive queries.** For [Datalog](/datalog/), tests for containment in a UCQ decide whether a recursive program is equivalent to a nonrecursive one.

## References
