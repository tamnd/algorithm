---
tag: 17CGZ9
kind: problem
slug: consistent-query-answering
name: Consistent query answering
aliases:
- CQA
- consistent answers over repairs
area: databases/data-integration-and-cleaning
level: advanced
summary: "Return the answers to a query that hold in every repair of an inconsistent database, without choosing one repair."
prereqs: [database-repair, conjunctive-query, functional-dependency, co-np]
see_also: [database-repair, denial-constraint, certain-answers, data-and-combined-complexity, candidate-key, sat, answering-queries-using-views, holoclean]
sources:
  - paper: doi:10.1145/303976.303983
    title: "Marcelo Arenas, Leopoldo Bertossi and Jan Chomicki, Consistent query answers in inconsistent databases, PODS 1999"
    locator: "pages 68-79, the definition of repairs and consistent answers, and the rewriting by residues"
  - paper: doi:10.1016/j.jcss.2006.10.013
    title: "Ariel Fuxman and Renée J. Miller, First-order query rewriting for inconsistent databases, Journal of Computer and System Sciences 73(4), 2007"
    locator: "pages 610-635, the class of queries with a first-order rewriting under primary keys, and a coNP-complete query"
  - paper: doi:10.1016/j.ipl.2010.07.021
    title: "Jef Wijsen, A remark on the complexity of consistent conjunctive query answering under primary key violations, Information Processing Letters 110(21), 2010"
    locator: "pages 950-955, a query in polynomial time without a first-order rewriting"
  - paper: doi:10.1145/3068334
    title: "Paraschos Koutris and Jef Wijsen, Consistent query answering for self-join-free conjunctive queries under primary key constraints, ACM TODS 42(2), 2017"
    locator: "the attack graph and the dichotomy between polynomial time and coNP-completeness"
  - paper: doi:10.1007/s00224-020-09985-6
    title: "Paraschos Koutris and Jef Wijsen, Consistent query answering for primary keys in Datalog, Theory of Computing Systems 65(1), 2021"
    locator: "the polynomial cases expressed in symmetric stratified Datalog and placed in logspace"
  - paper: doi:10.1016/j.ic.2004.04.007
    title: "Jan Chomicki and Jerzy Marcinkowski, Minimal-change integrity maintenance using tuple deletions, Information and Computation 197(1-2), 2005"
    locator: "pages 90-121, the conflict hypergraph and the complexity of consistent answers under denial constraints"
  - book: isbn:9783031007552
    title: "Leopoldo Bertossi, Database Repairing and Consistent Query Answering, Morgan and Claypool, 2011"
    locator: "the chapters on consistent query answering and its complexity"
---

Consistent query answering asks which answers of a query are true in every repair of a database that violates its constraints. It differs from [database repair](/database-repair/): that problem builds one consistent database and runs queries on it, while consistent query answering keeps the data as it is and returns only what no choice of repair can change. The definition follows Arenas, Bertossi and Chomicki. Most of the theory is for primary keys, where a repair keeps exactly one fact of each group of facts with the same key.

## In plain words

Two sources disagree about the department of Ann. One says sales and the other says HR, and the database cannot tell which is right. You can still answer questions. "Is Bob in HR?" gets yes if all sources agree on Bob. "Does Ann work somewhere?" gets yes, because she does in every reading. "Is Ann in HR?" gets no clear answer, so it is left out.

The answers you return are the safe ones: true whatever way the conflicts are settled. The hard part is that the number of ways to settle the conflicts grows very fast, so you cannot try them one by one. For some questions a clever rewrite of the question gives the safe answers directly. For others, no fast method is known.

## Definition

**Repairs.** Let $D$ be a finite database and $\Sigma$ a set of constraints, for example primary keys, functional dependencies or [denial constraints](/denial-constraint/). Set semantics holds. A *subset repair* of $D$ is a subset $D' \subseteq D$ that satisfies $\Sigma$ and is maximal under inclusion among such subsets. Denial constraints, and so primary keys and functional dependencies, are kept when facts are deleted, so at least one subset repair exists.

**Consistent answers.** For a query $Q$, a tuple $\bar a$ is a *consistent answer* if $\bar a \in Q(D')$ for every subset repair $D'$ of $D$. For a Boolean query $q$, the decision problem $\text{CERTAINTY}(q)$ asks, given $D$, whether $q$ is true in every repair. The query and the constraints are fixed, so the complexity is data complexity unless stated.

**Primary keys.** A schema with primary keys is written $R(\underline{x}; y)$, with the key before the semicolon. A *block* is a maximal set of facts of one relation that agree on the key. Under primary keys, the subset repairs are exactly the sets that keep one fact from each block, so a database with blocks of sizes $b_1, \ldots, b_s$ has $b_1 \cdots b_s$ repairs. Queries are conjunctive queries in AHV notation $q() \text{ :- } R_1(\bar u_1), \ldots, R_m(\bar u_m)$. The query is *self-join-free* if no relation name occurs twice.

## Variants

- **Constraints.** Primary keys, functional dependencies, denial constraints, or constraints with insertions such as inclusion dependencies. With inclusion dependencies a repair may also add facts, and repairs are defined by a minimal symmetric difference.
- **Repair semantics.** Subset repairs, repairs with the largest number of facts, repairs by updates of values, or repairs with priorities among facts. Each gives a different set of consistent answers.
- **Queries.** Self-join-free conjunctive queries, queries with self-joins, unions, aggregates, or first-order queries. For an aggregate, the usual answer is the range of values over all repairs.
- **Counting.** Count the repairs in which the query is true, instead of asking if it is true in all of them.

## Examples

Let $\text{Emp}(\underline{name}; dept)$ hold (ann, sales), (ann, hr) and (bob, hr). The block of ann has two facts, so there are two repairs: {(ann, sales), (bob, hr)} and {(ann, hr), (bob, hr)}.

| query | answers in repair 1 | answers in repair 2 | consistent answers |
|---|---|---|---|
| $Q(x) \text{ :- } \text{Emp}(x, \text{hr})$ | bob | ann, bob | bob |
| $Q(x) \text{ :- } \text{Emp}(x, y)$ | ann, bob | ann, bob | ann, bob |
| $Q(y) \text{ :- } \text{Emp}(\text{ann}, y)$ | sales | hr | none |

Three Boolean queries over $R(\underline{x}; y)$ and $S(\underline{y}; z)$ or $S(\underline{z}; y)$ show the three cases of the theory.

- **First-order.** $q_0() \text{ :- } R(x, y), S(y, z)$ with $S$ keyed on $y$. It is true in every repair if and only if $\exists x\, [\exists y\, R(x, y) \wedge \forall y\, (R(x, y) \to \exists z\, S(y, z))]$ holds in $D$. Each repair keeps one fact of the block of such an $x$, and the block of $S$ for its $y$ is not empty, so the repair keeps an $S$ fact that joins. If no such $x$ exists, a repair that picks a bad $y$ in every block of $R$ makes $q_0$ false. So $\text{CERTAINTY}(q_0)$ is a first-order query, and SQL can compute it.
- **Polynomial but not first-order.** $q_1() \text{ :- } R(x, y), S(y, x)$ with $S$ keyed on $y$. Wijsen proved that $\text{CERTAINTY}(q_1)$ is in polynomial time but has no first-order rewriting.
- **coNP-complete.** $q_2() \text{ :- } R(x, y), S(z, y)$ with $S$ keyed on $z$, so the join is on two attributes outside the keys. $\text{CERTAINTY}(q_2)$ is coNP-complete (Fuxman and Miller). The reduction is below.

## Known algorithms

- **Brute force.** Enumerate the repairs and evaluate the query in each one. Correct for every query, but the number of repairs can be exponential in $|D|$.
- **First-order rewriting.** For the queries where it exists, compute a first-order query $\varphi$ with $\varphi(D)$ equal to the consistent answers, and run it as SQL. Arenas, Bertossi and Chomicki gave a rewriting by residues for some classes of constraints and queries. Fuxman and Miller gave a rewriting for a class of self-join-free conjunctive queries under primary keys, which contains $q_0$.
- **The attack graph.** Koutris and Wijsen define, for a self-join-free conjunctive query, a graph on its atoms. It decides which case holds and, in the polynomial cases, guides the algorithm.
- **The conflict hypergraph.** Under denial constraints, the facts are the vertices and each minimal set of facts that violates a constraint is a hyperedge. The repairs are the maximal independent sets. Chomicki and Marcinkowski use it to answer queries without quantifiers in polynomial time.
- **Solvers.** For the coNP-complete cases, encode "some repair makes the query false" as a [SAT](/sat/) instance, an integer program or an answer set program, and give it to a solver.

## Bounds

All bounds are theorems in data complexity unless stated.

- **Upper bound.** Under denial constraints, $\text{CERTAINTY}(q)$ is in [coNP](/co-np/) for every first-order $q$. A certificate for "no" is a repair $D'$ with $q$ false. Checking that $D'$ is consistent takes polynomial time for fixed constraints. Checking that it is maximal needs only single facts: $D'$ is maximal if and only if $D' \cup \{f\}$ violates $\Sigma$ for each $f \in D \setminus D'$, since a consistent $D' \cup S$ would make $D' \cup \{f\}$ consistent for each $f \in S$.
- **Hardness.** $\text{CERTAINTY}(q_2)$ is coNP-complete (Fuxman and Miller).
- **Trichotomy for primary keys.** For each self-join-free conjunctive query $q$ under primary keys, $\text{CERTAINTY}(q)$ is in FO if the attack graph of $q$ is acyclic, coNP-complete if it has a strong cycle, and in P but not in FO otherwise (Koutris and Wijsen, TODS 2017). The case can be decided from $q$.
- **Logspace.** The polynomial cases of the trichotomy can be expressed in symmetric stratified Datalog and so are in logspace (Koutris and Wijsen, 2021).
- **Queries without quantifiers.** Under denial constraints, the consistent answers to quantifier-free queries can be found in polynomial time (Chomicki and Marcinkowski).
- **Combined complexity.** If the query is part of the input, the problem is at least as hard as evaluating a Boolean conjunctive query, which is NP-complete: with $\Sigma$ empty the database is its own only repair.

## Reductions

- **From SAT to the complement of $\text{CERTAINTY}(q_2)$.** Take a formula in conjunctive normal form. For each clause $C$, put $R(C, \ell)$ for each literal $\ell$ of $C$, so the block of $C$ holds its literals. For each variable $v$, put $S(v, v)$ and $S(v, \neg v)$, a block of two facts. A repair picks one literal per clause from $R$ and one literal per variable from $S$, and $q_2$ is false in it if and only if no literal is picked by both. Read the $S$ pick $v$ as "$v$ is false" and $\neg v$ as "$v$ is true". Then the $S$ picks are the false literals of an assignment, and $q_2$ fails if and only if each clause picks a true literal. So the formula is satisfiable if and only if some repair makes $q_2$ false. This gives the coNP-hardness.
- **To SAT.** In the other direction, "some repair makes $q$ false" is in NP and so reduces to SAT, which is how solvers are used.
- **From certain answers.** The consistent answers are the [certain answers](/certain-answers/) over the set of possible worlds given by the repairs. Data exchange and [answering queries using views](/answering-queries-using-views/) use the same idea with other sets of worlds.

## Applications

- **Data integration.** Sources that agree on the schema can disagree on the values for one key. Consistent answers report only what holds whatever source is right.
- **Querying dirty data without cleaning it.** When no repair can be chosen with confidence, consistent answers give a safe subset of the answers. A probabilistic method such as [HoloClean](/holoclean/) chooses values instead.
- **Data quality checks.** The difference between the plain answers and the consistent answers shows which answers depend on the conflicts.

## References
