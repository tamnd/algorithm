---
tag: M1834Y
kind: theorem
slug: dalvi-suciu-dichotomy
name: Dalvi-Suciu dichotomy theorem
aliases:
- dichotomy for queries on probabilistic databases
area: databases/relational-theory
level: research
summary: "Each union of conjunctive queries on a tuple-independent database can be evaluated in polynomial time by lifted rules or is #P-hard."
prereqs: [probabilistic-database, model-counting]
see_also: [data-and-combined-complexity, provenance-semirings, d-dnnf, dnf-counting, karp-luby-algorithm, inclusion-exclusion-principle, csp-dichotomy-theorem, conjunctive-query]
sources:
  - paper: "Nilesh Dalvi and Dan Suciu, Efficient query evaluation on probabilistic databases, Proceedings of the 30th International Conference on Very Large Data Bases (VLDB), 864 to 875 (2004)"
    locator: safe plans, the #P-hardness of the query R(x), S(x,y), T(y), and the dichotomy for conjunctive queries without self-joins
  - paper: doi:10.1007/s00778-006-0004-3
    title: Nilesh Dalvi and Dan Suciu, Efficient query evaluation on probabilistic databases, The VLDB Journal 16(4), 523 to 544 (2007)
    locator: journal version of the VLDB 2004 paper, with the dichotomy for conjunctive queries without self-joins
  - paper: "Nilesh Dalvi and Dan Suciu, The dichotomy of conjunctive queries on probabilistic structures, Proceedings of the 26th ACM Symposium on Principles of Database Systems (PODS), 293 to 302 (2007)"
    locator: the dichotomy extended to conjunctive queries with self-joins
  - paper: doi:10.1145/2395116.2395119
    title: Nilesh Dalvi and Dan Suciu, The dichotomy of probabilistic inference for unions of conjunctive queries, Journal of the ACM 59(6), article 30 (2012)
    locator: the lifted inference rules for unions of conjunctive queries and the proof that every query they reject is #P-hard
  - paper: doi:10.1137/0212053
    title: J. Scott Provan and Michael O. Ball, The complexity of counting cuts and of computing the probability that a graph is connected, SIAM Journal on Computing 12(4), 777 to 788 (1983)
    locator: counting the satisfying assignments of a positive partitioned 2-DNF formula is #P-complete
  - paper: doi:10.1137/0208032
    title: Leslie G. Valiant, The complexity of enumeration and reliability problems, SIAM Journal on Computing 8(3), 410 to 421 (1979)
    locator: the class #P and #P-completeness of counting problems
  - book: isbn:9781608456802
    title: Dan Suciu, Dan Olteanu, Christopher Re and Christoph Koch, Probabilistic Databases, Synthesis Lectures on Data Management, Morgan and Claypool (2011)
    locator: Chapter 3 (the query evaluation problem, hierarchical queries and the hardness of H0) and Chapter 4 (extensional evaluation, the lifted rules and the dichotomy for unions of conjunctive queries)
---

The Dalvi-Suciu dichotomy theorem says that, on a [probabilistic database](/probabilistic-database/) with independent tuples, the probability of each fixed union of conjunctive queries is either computable in polynomial time or #P-hard, with nothing in between. The polynomial queries are those that a small set of lifted inference rules can evaluate, and for conjunctive queries without self-joins they are exactly the *hierarchical* queries. The theorem is about data complexity: the query is fixed and the database, with its probabilities, is the input. Dalvi and Suciu proved the case without self-joins in 2004 and the general case for unions of conjunctive queries in 2012.

## Statement

**Setting.** A tuple-independent database (TID) is a set of tuples, each present independently with a given probability $p(t)$; see [probabilistic database](/probabilistic-database/). For a Boolean query $Q$, $P(Q)$ is the probability that $Q$ is true in a random world. The probabilities are rational numbers given in binary. $\#\mathrm{P}$ is Valiant's class of counting problems; a function is #P-hard if every function in #P reduces to it in polynomial time with oracle calls. Queries with free variables reduce to the Boolean case by substituting each candidate answer.

A *conjunctive query* (CQ) here is a Boolean formula $\exists \bar{x}\, (g_1 \land \cdots \land g_m)$ whose atoms $g_i$ use variables and constants. It is *self-join-free* if no relation name occurs in two atoms. For a variable $x$, let $\mathrm{at}(x)$ be the set of atoms that contain $x$. The query is *hierarchical* if for every two variables $x$ and $y$,

$$\mathrm{at}(x) \subseteq \mathrm{at}(y), \quad \mathrm{at}(y) \subseteq \mathrm{at}(x), \quad \text{or} \quad \mathrm{at}(x) \cap \mathrm{at}(y) = \emptyset.$$

**Theorem 1** (Dalvi and Suciu 2004, 2007). Let $Q$ be a self-join-free Boolean CQ. If $Q$ is hierarchical, then $P(Q)$ is computable in time polynomial in the size of the TID. If $Q$ is not hierarchical, then computing $P(Q)$ on TIDs is #P-hard.

**Theorem 2** (Dalvi and Suciu 2012). For every Boolean union of conjunctive queries (UCQ) $Q$, one of the two holds: the lifted inference rules (independent join, independent union, independent project and inclusion-exclusion with cancellation) compute $P(Q)$, in time polynomial in the size of the TID; or computing $P(Q)$ on TIDs is #P-hard.

Both theorems are in data complexity. The polynomial in Theorem 1 has a degree that grows with the number of variables of $Q$.

## In plain words

Some database tuples are uncertain, and each one is there or not by its own coin flip. You ask a question that joins several tables, and you want the chance that the answer is yes. For some questions you can split the work: the parts use different tuples, so their chances multiply, and you can go value by value. For other questions the parts always share tuples, and no such split exists.

The theorem says there is no middle ground. Either the splitting rules work, and the chance is easy to compute even on a huge database, or the problem is as hard as counting the solutions of a hard puzzle. For queries that use each table once, you can see which case holds by looking at how the variables share tables: if every two variables either nest or stay apart, the query is easy.

## Proof

The proof is for Theorem 1. Theorem 2 needs a long proof of hardness for the queries that the rules reject, given in Dalvi and Suciu (2012); its polynomial half is the same kind of argument as below, with two more rules. Fix a self-join-free Boolean CQ $Q$ with $k$ variables, and let $n$ be the number of constants in the TID.

**Polynomial time for hierarchical queries.** Two atoms are *connected* if they share a variable, and the components of $Q$ are the classes of the transitive closure of this relation. The algorithm uses three rules. Each subquery they produce is again self-join-free and hierarchical: it has a subset of the atoms, or the same atoms with one variable replaced by a constant, and in both cases the sets $\mathrm{at}(y)$ of the remaining variables only lose the same atoms, which keeps every inclusion and every empty intersection.

1. *Ground atom.* If $Q$ is one atom without variables, it is one tuple $t$, and $P(Q) = p(t)$, or $0$ if $t$ is not in the TID.
2. *Independent join.* If $Q$ has two or more components, $Q = Q_1 \land Q_2$ where $Q_1$ and $Q_2$ share no variable. They also share no relation name, because $Q$ is self-join-free, so the events $Q_1$ and $Q_2$ depend on disjoint sets of tuples and are independent: $P(Q) = P(Q_1) \cdot P(Q_2)$.
3. *Independent project.* If $Q$ has one component and at least one variable, it has a *root variable*, one that occurs in every atom. To see this, take $x$ with $\mathrm{at}(x)$ maximal under inclusion. If an atom $g$ is not in $\mathrm{at}(x)$, follow a chain of shared variables from an atom in $\mathrm{at}(x)$ to $g$; some variable $y$ on the chain occurs both in an atom of $\mathrm{at}(x)$ and in an atom outside it. Then $\mathrm{at}(x) \cap \mathrm{at}(y) \neq \emptyset$ and $\mathrm{at}(y) \not\subseteq \mathrm{at}(x)$, so the hierarchical condition gives $\mathrm{at}(x) \subsetneq \mathrm{at}(y)$, against the choice of $x$. So $x$ is a root. Write $Q = \exists x\, Q'(x)$. For two constants $a \neq b$, every atom of $Q'(a)$ has $a$ in the positions of $x$, and the atom of the same relation in $Q'(b)$ has $b$ there, so $Q'(a)$ and $Q'(b)$ depend on disjoint sets of tuples and are independent. A value outside the active domain makes $Q'$ false. Hence
$$P(Q) = 1 - \prod_{a} \big(1 - P(Q'(a))\big),$$
over the $n$ constants $a$ of the TID, and each $Q'(a)$ has $k - 1$ variables.

The rules apply until every subquery is a ground atom. Each application of rule 3 creates at most $n$ subqueries and removes one variable, and rule 2 splits the atoms, so the recursion has at most $m \cdot n^{k}$ leaves for $m$ atoms, and each step costs polynomial time in the size of the TID. For a fixed $Q$, the total time is polynomial.

**#P-hardness of $H_0$.** Let $H_0 = \exists x\, \exists y\, (R(x) \land S(x, y) \land T(y))$. A *positive partitioned 2-DNF* is a formula $\Phi = \bigvee_{(i, j) \in E} X_i Y_j$ over two disjoint sets of variables $X_1, \ldots, X_{m}$ and $Y_1, \ldots, Y_{l}$. Counting its satisfying assignments, #PP2DNF, is #P-complete (Provan and Ball 1983). Given $\Phi$, build the TID with tuples $R(i)$ for $i \leq m$ and $T(j)$ for $j \leq l$, each with probability $1/2$, and $S(i, j)$ for $(i, j) \in E$ with probability 1. A world chooses which $R(i)$ and $T(j)$ are present, that is, an assignment of the $X_i$ and $Y_j$, each with probability $2^{-(m + l)}$. $H_0$ is true in the world exactly when some $(i, j) \in E$ has $R(i)$ and $T(j)$ present, that is, when the assignment satisfies $\Phi$. So

$$\#\Phi = 2^{m + l} \cdot P(H_0),$$

and a polynomial algorithm for $P(H_0)$ would count the satisfying assignments of $\Phi$. So $P(H_0)$ is #P-hard.

**#P-hardness of every non-hierarchical query.** If $Q$ is not hierarchical, there are variables $x$, $y$ and atoms $g_1 \in \mathrm{at}(x) \setminus \mathrm{at}(y)$, $g_2 \in \mathrm{at}(x) \cap \mathrm{at}(y)$ and $g_3 \in \mathrm{at}(y) \setminus \mathrm{at}(x)$. Reduce $H_0$ to $Q$. Take an $H_0$ instance of the form above, with constants $A$ for $x$ and $B$ for $y$, chosen disjoint, and a new constant $c$. For a constant $a \in A$ and $b \in B$, let $\nu_{a, b}$ map $x$ to $a$, $y$ to $b$ and every other variable to $c$. Build a TID for $Q$, relation by relation; since $Q$ is self-join-free, each atom has its own relation.

- For $g_1$: the tuple $\nu_{a, b}(g_1)$, which depends only on $a$, for each $a \in A$, with probability $p(R(a))$.
- For $g_3$: the tuple $\nu_{a, b}(g_3)$, which depends only on $b$, for each $b \in B$, with probability $p(T(b))$.
- For every other atom $g$: the tuples $\nu_{a, b}(g)$ for all $(a, b)$ with $S(a, b)$ in the instance, with probability 1.

The new database has polynomial size. A valuation that makes $Q$ true must map every variable other than $x, y$ to $c$, the only value in their positions, $x$ into $A$ (by $g_1$) and $y$ into $B$ (by $g_3$), and $(x, y)$ to a pair in $S$ (by $g_2$). The only uncertain tuples are those of $g_1$ and $g_3$, one per $R(a)$ and per $T(b)$. So a world of the new database satisfies $Q$ exactly when the matching world of the $H_0$ instance satisfies $H_0$, and the probabilities are equal. Hence $P(Q)$ is #P-hard. $\square$

**A worked case.** For $\Phi = X_1 Y_1 \lor X_1 Y_2 \lor X_2 Y_2$, the TID has $R(1), R(2), T(1), T(2)$ with probability $1/2$ and $S = \{(1, 1), (1, 2), (2, 2)\}$. Of the 16 assignments, 8 satisfy $\Phi$: with $X_1$ true, 3 of the 4 choices of $(Y_1, Y_2)$ for each value of $X_2$; with only $X_2$ true, the 2 choices with $Y_2$ true. So $P(H_0) = 8/16 = 1/2$. On the other side, $Q = \exists x\, \exists y\, (R(x) \land S(x, y))$ is hierarchical, with $\mathrm{at}(y) \subseteq \mathrm{at}(x)$, and $x$ is a root; the [probabilistic database](/probabilistic-database/) page evaluates it by rules 2 and 3 to 0.448.

## Consequences

- **A syntactic test.** For self-join-free CQs, the line between easy and hard is decided by looking at the query: compute $\mathrm{at}(x)$ for each variable and check the condition, in time polynomial in the query. For UCQs, whether the rules succeed is also decidable, by running them on the query.
- **Safe plans.** The rules of the proof translate into a query plan whose operators compute probabilities by independence: a join of independent inputs multiplies, and a projection on a root variable combines by $1 - \prod (1 - p)$. Such plans, the *safe plans* of Dalvi and Suciu (2004), run in a relational engine with modified operators. For self-join-free CQs, a safe plan exists exactly for the hierarchical queries.
- **Read-once lineage.** For a hierarchical self-join-free CQ, the rules split the lineage formula into conjunctions and disjunctions of parts on disjoint variables, so the lineage is a read-once formula, and its probability follows from the formula in linear time. For $H_0$ on the instance of the proof, the lineage is the formula $\Phi$ itself, and $X_1 Y_1 \lor X_1 Y_2 \lor X_2 Y_2$ is not read-once.
- **Where to spend effort.** A system can test the query first and use the lifted rules for the safe ones. For the others it uses intensional methods, such as compilation of the lineage into a [d-DNNF](/d-dnnf/) or exact [model counting](/model-counting/), or approximation by the [Karp-Luby estimator](/karp-luby-algorithm/), which gives an FPRAS for every UCQ because the lineage is a polynomial-size DNF.
- **A counting analogue of the CSP dichotomy.** Like the [CSP dichotomy theorem](/csp-dichotomy-theorem/) for decision problems, the theorem says that a natural class of problems has no intermediate cases, here for exact probability computation.

## Tightness

- **Self-joins.** Without the self-join-free condition, hierarchical is not enough. Let $A = \exists x\, \exists y\, (R(x) \land S(x, y))$ and $B = \exists u\, \exists v\, (S(u, v) \land T(v))$. The union $H_1 = A \lor B$ is #P-hard (Dalvi and Suciu 2012), while $A$ and $B$ are hierarchical and easy. The conjunction $A \land B$ is a CQ with a self-join on $S$ in which every variable meets the hierarchical condition. By [inclusion-exclusion](/inclusion-exclusion-principle/), $P(A \land B) = P(A) + P(B) - P(A \lor B)$, so $A \land B$ is #P-hard too. Theorem 2 covers such queries with its full set of rules.
- **Inclusion-exclusion with cancellation.** Some UCQs are in polynomial time only because, in the inclusion-exclusion expansion, the #P-hard terms cancel each other. Dalvi and Suciu (2012) show that such queries have no safe plan built from the first three rules, so the fourth rule is needed for the dichotomy.
- **Data complexity only.** In combined complexity the question changes: deciding whether $P(Q) > 0$, with $Q$ part of the input and all probabilities 1, is CQ evaluation, which is NP-complete (see [data and combined complexity](/data-and-combined-complexity/)). The polynomial bound of Theorem 1 has degree up to the number of variables.
- **Probabilities 1/2 and 1 suffice.** The hardness proof uses only these two values, so the hard queries stay hard when some relations are deterministic, as $S$ is in the reduction.
- **Exact computation only.** The theorem is about exact probabilities. For every UCQ, an approximation within a factor $1 \pm \varepsilon$ is possible in randomized polynomial time.
- **Beyond UCQs.** Queries with negation or with aggregates are outside both theorems, as are databases whose tuples are correlated.

## History

Dalvi and Suciu (VLDB 2004, journal version in the VLDB Journal 2007) defined the possible worlds semantics for independent tuples, gave safe plans, proved that $H_0$ is #P-hard by the reduction from Provan and Ball's counting problem, and proved the dichotomy for self-join-free CQs: a query with a safe plan is in polynomial time, and every other query is #P-hard. The statement with the hierarchical condition is the form used in the later papers and in the textbook. In PODS 2007 (pages 293 to 302) they extended the dichotomy to CQs with self-joins. Their paper in the Journal of the ACM in 2012 proved the dichotomy for all UCQs, with the lifted inference rules and the inclusion-exclusion rule with cancellation. The textbook of Suciu, Olteanu, Re and Koch (2011) presents both results and the lifted rules.

## References
