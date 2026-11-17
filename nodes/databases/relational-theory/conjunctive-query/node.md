---
tag: PG1J3V
kind: definition
slug: conjunctive-query
name: Conjunctive query
aliases:
- select-project-join query
- SPJ query
area: databases/relational-theory
level: core
summary: A query built from relational atoms with conjunction and existential quantification; it is the select-project-join part of SQL.
prereqs: [relational-model, relational-algebra]
see_also: [chandra-merlin-theorem, conjunctive-query-minimization, sagiv-yannakakis-theorem, query-containment-problem, acyclic-hypergraph, yannakakis-algorithm, data-and-combined-complexity, datalog]
sources:
  - paper: doi:10.1145/800105.803397
    title: Ashok K. Chandra and Philip M. Merlin, Optimal implementation of conjunctive queries in relational data bases, Proceedings of the 9th Annual ACM Symposium on Theory of Computing (STOC), 77 to 90 (1977)
    locator: the definition of conjunctive queries, their equivalence with select, project and join expressions, and the NP-completeness of evaluation, containment and equivalence
  - paper: doi:10.1145/800070.802186
    title: Moshe Y. Vardi, The complexity of relational query languages, Proceedings of the 14th Annual ACM Symposium on Theory of Computing (STOC), 137 to 146 (1982)
    locator: the separation of data complexity and combined complexity of query languages
  - paper: doi:10.1006/jcss.2000.1713
    title: Phokion G. Kolaitis and Moshe Y. Vardi, Conjunctive-query containment and constraint satisfaction, Journal of Computer and System Sciences 61(2), 302 to 332 (2000)
    locator: conjunctive query evaluation and containment as constraint satisfaction
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 4 (conjunctive queries), the rule-based, tableau, calculus and algebra forms and their equivalence
---

A conjunctive query asks for the ways to fill a pattern of facts with values from a database. It is a rule $Q(\bar x) \mathbin{:\!-} R_1(\bar u_1), \ldots, R_m(\bar u_m)$: the body lists the atoms that must hold, and the head lists the variables to return. In logic it is a first-order formula with only $\exists$ and $\wedge$. In [relational algebra](/relational-algebra/) it is an expression with selections on equalities, projections and joins, which is why it is also called a select-project-join (SPJ) query. Most queries that databases run are conjunctive queries or unions of them, and their theory is the best understood part of query languages: containment is decidable by the [Chandra-Merlin theorem](/chandra-merlin-theorem/), and each query has a unique smallest equivalent form.

## Definition

A *schema* is a finite set of relation names, each with an arity. A *term* is a variable or a constant. An *atom* is $R(t_1, \ldots, t_r)$ where $R$ has arity $r$ and the $t_i$ are terms. We use set semantics: a database $D$ gives each relation name $R$ a finite set $R^D$ of tuples of constants, and a query returns a set of tuples.

**Definition (Chandra and Merlin 1977).** A *conjunctive query* (CQ) over a schema is a rule

$$Q(\bar x) \mathbin{:\!-} R_1(\bar u_1), \ldots, R_m(\bar u_m)$$

with $m \ge 1$, where the *body* $R_1(\bar u_1), \ldots, R_m(\bar u_m)$ is a list of atoms, the *head* $\bar x$ is a tuple of terms, and each variable of $\bar x$ occurs in the body. This last condition is *safety*. The variables of the body that are not in the head are the *existential* variables.

A *valuation* is a map $v$ from the variables to constants, extended to be the identity on constants. The answer of $Q$ on $D$ is

$$Q(D) = \{\, v(\bar x) \;:\; v \text{ is a valuation with } v(\bar u_i) \in R_i^D \text{ for } i = 1, \ldots, m \,\}.$$

$Q$ is *Boolean* if its head is empty. Its answer is then the empty tuple (true) or nothing (false). $Q$ is *full* if it has no existential variables.

**Equivalent forms.** The following describe the same class of queries:

1. **Rules.** The rule form above.
2. **Logic.** First-order formulas $\varphi(\bar x) = \exists \bar y \, (A_1 \wedge \cdots \wedge A_m)$ where the $A_i$ are relational atoms or equalities. An equality $x = y$ is removed by replacing $y$ by $x$ everywhere, and an equality $x = c$ by replacing $x$ by $c$.
3. **Algebra.** [Relational algebra](/relational-algebra/) expressions built from the relations with selection $\sigma_{A = B}$ and $\sigma_{A = c}$, projection, renaming and join (or product). These are the SPJ expressions.
4. **Tableaux.** A table with one row per atom and a summary row for the head, as Aho, Sagiv and Ullman use for [minimization](/conjunctive-query-minimization/).
5. **SQL.** `SELECT DISTINCT` queries whose `WHERE` clause is a conjunction of equalities between columns and constants. `DISTINCT` gives set semantics. Without it, SQL uses bag semantics, and the theory on this page changes.

**Canonical database.** The *canonical database* $D_Q$ of $Q$ has one fact $R_i(\bar u_i)$ for each atom of the body, with each variable read as a new constant of its own. The identity valuation shows that $\bar x \in Q(D_Q)$. This database is the key to the [Chandra-Merlin theorem](/chandra-merlin-theorem/).

**Hypergraph.** The [hypergraph](/hypergraph/) of $Q$ has the variables as vertices and one edge per atom, the set of variables of that atom. Its structure decides how hard $Q$ is to evaluate: see [acyclic hypergraph](/acyclic-hypergraph/), [hypertree width](/hypertree-width/) and [fractional hypertree width](/fractional-hypertree-width/).

**Basic facts.** Let $k$ be the number of atoms of $Q$ and $n$ the number of tuples of $D$.

- *Monotone (theorem).* If $D \subseteq D'$ relation by relation, then $Q(D) \subseteq Q(D')$.
- *Preserved by homomorphisms (theorem).* If $h$ is a map of constants with $h(D) \subseteq D'$ that fixes the constants of $Q$, then $h(Q(D)) \subseteq Q(D')$. Compose each valuation with $h$.
- *Data complexity (theorem).* For a fixed $Q$, the naive method tries all $n^k$ choices of one tuple per atom, so $Q(D)$ takes polynomial time in $n$. Since $Q$ is a fixed first-order formula, the problem is in the circuit class $\mathrm{AC}^0$. See [data and combined complexity](/data-and-combined-complexity/).
- *Combined complexity (theorem).* When $Q$ is part of the input, deciding whether a Boolean CQ is true on $D$ is [NP-complete](/np-complete/) (Chandra and Merlin 1977). It is the same problem as the [constraint satisfaction problem](/constraint-satisfaction-problem/) with $D$ as the template (Kolaitis and Vardi). For [acyclic](/acyclic-hypergraph/) queries the [Yannakakis algorithm](/yannakakis-algorithm/) takes polynomial time even in combined complexity.

## Examples and non-examples

Let $E$ be a binary relation, the edges of a directed graph.

- **Paths of length two.** $Q(x, z) \mathbin{:\!-} E(x, y), E(y, z)$. In algebra, $\pi_{1, 4}(\sigma_{2 = 3}(E \times E))$. In SQL, `SELECT DISTINCT a.src, b.dst FROM E a, E b WHERE a.dst = b.src`. The variable $y$ is existential.
- **Triangles.** The Boolean query $Q() \mathbin{:\!-} E(x, y), E(y, z), E(z, x)$ is true if and only if the graph has a directed cycle of length 3, or a loop, since $x$, $y$ and $z$ need not be different. Its hypergraph is a triangle, so it is not acyclic.
- **Constants.** $Q(x) \mathbin{:\!-} \mathit{Emp}(x, d), \mathit{Dept}(d, \text{'Sales'})$ returns the employees of the sales department.
- **Repeated variables.** $Q(x) \mathbin{:\!-} E(x, x)$ returns the nodes with a loop. A repeated variable is an equality selection.
- **Non-example: union.** $R(x) \vee S(x)$ is not a CQ. If a CQ $Q$ were equivalent to it, then by the [Sagiv-Yannakakis theorem](/sagiv-yannakakis-theorem/) $Q$ would be contained in $R(x)$ alone or in $S(x)$ alone. Say it is $R(x)$. On the database $\{S(a)\}$, the union returns $a$ and $Q$ returns nothing. Unions of CQs (UCQs) are the next larger class.
- **Non-example: negation.** $Q(x) \mathbin{:\!-} R(x), \neg S(x)$ is not monotone: adding $S(a)$ to $\{R(a)\}$ removes the answer $a$. So no CQ expresses it.
- **Non-example: inequality.** $Q() \mathbin{:\!-} E(x, y), x \neq y$ is true on $\{E(a, b)\}$. The map $a, b \mapsto c$ sends this database to $\{E(c, c)\}$, where $Q$ is false. CQs are preserved by such maps, so no CQ expresses $Q$.
- **Non-example: counting.** "Nodes with at least as many out-edges as in-edges" is not monotone, and no CQ expresses it. Aggregates such as `COUNT` are outside the class.

## Related definitions

- **Union of conjunctive queries (UCQ).** A finite union of CQs with heads of the same arity. UCQs are the positive existential queries: $\exists$, $\wedge$ and $\vee$, without negation. Containment is decided member by member, by the [Sagiv-Yannakakis theorem](/sagiv-yannakakis-theorem/).
- **Containment and equivalence.** $Q_1 \subseteq Q_2$ holds if and only if there is a homomorphism from $Q_2$ to $Q_1$. See the [Chandra-Merlin theorem](/chandra-merlin-theorem/) and the [query containment problem](/query-containment-problem/).
- **Minimal query and core.** Each CQ has an equivalent CQ with the fewest atoms, unique up to renaming. See [conjunctive query minimization](/conjunctive-query-minimization/).
- **CQ with comparisons.** Atoms $x < y$, $x \le y$ or $x \ne y$ in the body. Containment becomes $\Pi_2^p$-complete.
- **Datalog rule.** A [Datalog](/datalog/) rule has the same form as a CQ, and a non-recursive Datalog program is a UCQ.
- **Acyclic CQ.** A CQ whose hypergraph is [alpha-acyclic](/acyclic-hypergraph/). The [GYO reduction](/gyo-reduction/) tests this.
- **Dependencies.** The two sides of a [tuple-generating dependency](/tuple-generating-dependency/) are conjunctions of atoms, so a TGD says that on the database each answer of one CQ is also an answer of another CQ.
- **Bag semantics.** If answers are counted with multiplicity, as in SQL without `DISTINCT`, CQ equivalence becomes isomorphism of queries, and containment is much harder.

## References
