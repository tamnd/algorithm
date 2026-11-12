---
tag: ZF3N9M
kind: theorem
slug: chandra-merlin-theorem
name: Chandra-Merlin theorem
aliases:
- homomorphism theorem for conjunctive queries
- containment mapping theorem
area: systems/database-algorithms
level: advanced
summary: "A conjunctive query Q1 is contained in Q2 if and only if there is a homomorphism from Q2 to Q1, if and only if the head of Q1 is an answer of Q2 on the canonical database of Q1."
prereqs: [relational-algebra, query-containment-problem]
see_also: [query-containment-problem, chase-algorithm, constraint-satisfaction-problem, csp-dichotomy-theorem, three-coloring, query-optimization, yannakakis-algorithm, treewidth]
sources:
  - paper: doi:10.1145/800105.803397
    title: Ashok K. Chandra and Philip M. Merlin, Optimal implementation of conjunctive queries in relational data bases, Proceedings of the 9th Annual ACM Symposium on Theory of Computing (STOC), 77 to 90 (1977)
    locator: the homomorphism criterion for containment and equivalence, the NP-completeness results, and the minimization of conjunctive queries
  - paper: doi:10.1145/322217.322221
    title: Yehoshua Sagiv and Mihalis Yannakakis, Equivalences among relational expressions with the union and difference operators, Journal of the ACM 27(4), 633 to 655 (1980)
    locator: the extension of the criterion to unions of conjunctive queries
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 4 (conjunctive queries) and Chapter 6 (static analysis and optimization), the homomorphism theorem and query minimization
---

The Chandra-Merlin theorem characterizes containment of conjunctive queries. A conjunctive query $Q_1$ is contained in a conjunctive query $Q_2$, that is, $Q_1(D) \subseteq Q_2(D)$ for every database $D$, if and only if there is a homomorphism from $Q_2$ to $Q_1$, and if and only if $Q_2$ returns the head of $Q_1$ on the canonical database of $Q_1$. Chandra and Merlin proved it in 1977. It turns a question about infinitely many databases into a finite search, so [query containment](/query-containment-problem/) and equivalence of conjunctive queries are decidable and [NP-complete](/np-complete/). It also gives the minimization of a conjunctive query to its core.

## Statement

A *conjunctive query* (CQ) is a rule

$$Q(\bar x) \;\leftarrow\; R_1(\bar u_1), \ldots, R_m(\bar u_m),$$

where each $\bar u_i$ is a tuple of variables and constants, and each variable of the *head* $\bar x$ occurs in the *body*. A *valuation* $v$ maps variables to values and is the identity on constants. On a database $D$,

$$Q(D) = \{\, v(\bar x) \;:\; v(\bar u_i) \in R_i^D \text{ for } i = 1, \ldots, m \,\}.$$

In [relational algebra](/relational-algebra/) these are the queries built from selection with equalities, projection and join. $Q_1 \subseteq Q_2$ means $Q_1(D) \subseteq Q_2(D)$ for every database $D$.

A *homomorphism* from $Q_2$ to $Q_1$ is a map $h$ from the variables of $Q_2$ to the variables and constants of $Q_1$, the identity on constants, such that $h(\bar x_2) = \bar x_1$ and $h$ maps each atom of the body of $Q_2$ to an atom of the body of $Q_1$. The *canonical database* $D_Q$ of $Q$ has one fact for each atom of the body, with each variable read as a new constant of its own.

**Theorem (Chandra and Merlin 1977).** For CQs $Q_1$ and $Q_2$ with heads of the same arity, the following are equivalent:

1. $Q_1 \subseteq Q_2$;
2. there is a homomorphism from $Q_2$ to $Q_1$;
3. $\bar x_1 \in Q_2(D_{Q_1})$.

## In plain words

A conjunctive query asks for all ways to fill in a pattern of facts, such as "x has a parent y who is a parent of z". One query is contained in another when it never gives an answer that the other one misses, on any database at all.

There are infinitely many databases, so this looks hard to check. The theorem says that one database is enough: the first query itself, read as a small database. If the second query finds the answer that the first query trivially finds there, then it finds it everywhere. That test is the same as finding a way to rename the variables of the second query so that each of its facts becomes a fact of the first query.

Note the direction: the smaller query receives the map. A query with more conditions has fewer answers.

## Proof

Write $Q_1(\bar x_1) \leftarrow B_1$ and $Q_2(\bar x_2) \leftarrow B_2$, where $B_1$ and $B_2$ are the bodies.

*(2) implies (1).* Let $h$ be a homomorphism from $Q_2$ to $Q_1$, and let $t \in Q_1(D)$ for a database $D$. Then there is a valuation $v$ with $v(B_1) \subseteq D$ and $v(\bar x_1) = t$. The map $v \circ h$ is a valuation for $Q_2$. For each atom $R(\bar u)$ of $B_2$, $h(R(\bar u))$ is an atom of $B_1$, so $v(h(\bar u)) \in R^D$. And $v(h(\bar x_2)) = v(\bar x_1) = t$. So $t \in Q_2(D)$.

*(1) implies (3).* The identity valuation $\iota$, which maps each variable of $Q_1$ to the constant of the same name, maps $B_1$ into $D_{Q_1}$ by the definition of $D_{Q_1}$. So $\bar x_1 = \iota(\bar x_1) \in Q_1(D_{Q_1})$. By (1), $\bar x_1 \in Q_2(D_{Q_1})$.

*(3) implies (2).* By (3) there is a valuation $g$ with $g(B_2) \subseteq D_{Q_1}$ and $g(\bar x_2) = \bar x_1$. The values of $D_{Q_1}$ are the variables and constants of $Q_1$, so $g$ maps the variables of $Q_2$ to the terms of $Q_1$, and it is the identity on constants. Each atom of $B_2$ goes to a fact of $D_{Q_1}$, which is an atom of $B_1$. So $g$ is a homomorphism from $Q_2$ to $Q_1$. $\blacksquare$

The proof uses that the variables of $Q_1$ become new constants in $D_{Q_1}$, different from each other and from the constants of the queries. If a variable were read as an existing constant, the homomorphism found in step (3) could map a constant of $Q_2$ to a variable of $Q_1$.

## Consequences

- **Containment and equivalence are NP-complete.** By (2), containment is in NP: guess $h$ and check it. It is NP-hard by a [reduction](/polynomial-time-reduction/) from [3-coloring](/three-coloring/). For a graph $G$, let $Q_G$ be the Boolean CQ with an atom $E(u, v)$ and an atom $E(v, u)$ for each edge $\{u, v\}$. Then $Q_{K_3} \subseteq Q_G$ if and only if there is a homomorphism from $G$ to the triangle, that is, $G$ is 3-colorable. Equivalence is NP-complete too, and so is the evaluation of a CQ on a database when the query is part of the input. All three are forms of the [constraint satisfaction problem](/constraint-satisfaction-problem/).
- **An example.** Let $Q_1(x) \leftarrow E(x, y), E(y, y)$ and $Q_2(x) \leftarrow E(x, u), E(u, v)$. The map $x \mapsto x$, $u \mapsto y$, $v \mapsto y$ sends $E(x, u)$ to $E(x, y)$ and $E(u, v)$ to $E(y, y)$, so $Q_1 \subseteq Q_2$: a node with an edge to a node with a loop has a path of length 2. No homomorphism goes the other way, since $E(y, y)$ would need a loop in $B_2$, so $Q_2 \not\subseteq Q_1$. In form (3): $D_{Q_1} = \{E(x, y), E(y, y)\}$ and $Q_2(D_{Q_1}) = \{x, y\}$, which contains $x$.
- **Minimization.** A CQ $Q$ is equivalent to a CQ whose body is a subset of its own body: if $Q'$ is equivalent to $Q$ with fewer atoms, then a homomorphism from $Q$ to $Q'$ followed by one from $Q'$ to $Q$ maps $Q$ into a subquery of itself with at most as many atoms as $Q'$, and that subquery is equivalent to $Q$. So one finds a minimal equivalent CQ by deleting atoms from the body, one at a time, as long as the query stays equivalent. The test for one deletion is the theorem: the identity shows $Q \subseteq Q - a$, and $Q - a \subseteq Q$ needs a homomorphism from $Q$ to $Q - a$. In the example $Q(x) \leftarrow E(x, y), E(x, z), E(z, w)$, the atom $E(x, y)$ goes, by $y \mapsto z$, and the result $Q(x) \leftarrow E(x, z), E(z, w)$ is minimal.
- **The core is unique.** Any two minimal equivalent CQs are the same up to a renaming of variables. Let $Q$ and $Q'$ be minimal and equivalent, with homomorphisms $h: Q \to Q'$ and $g: Q' \to Q$. Then $f = g \circ h$ maps $Q$ to a subquery $f(Q)$ that is equivalent to $Q$ (by $f$ and by the inclusion), so by minimality $f$ is a bijection on the atoms of $Q$. Every variable occurs in an atom, so $f$ is also onto the variables of $Q$, hence a bijection on them. So $h$ is one to one on the atoms and on the variables of $Q$, and $|Q| \le |Q'|$. The same argument for $h \circ g$ gives $|Q'| \le |Q|$. So $h$ maps the atoms of $Q$ onto the atoms of $Q'$, hence onto the variables of $Q'$, and $h$ is an isomorphism. This minimal query is the *core* of $Q$, as in the core of a graph.
- **Query optimization.** Fewer atoms means fewer joins, which was the aim of Chandra and Merlin. The test is also the basic step when one decides whether a query can be answered from stored views.
- **Tractable cases.** The search for $h$ is a CSP whose constraint graph is the query $Q_2$. When $Q_2$ is acyclic, the search is a semijoin program of the [Yannakakis algorithm](/yannakakis-algorithm/) and takes polynomial time. More generally it is polynomial when $Q_2$ has bounded [treewidth](/treewidth/).

## Tightness

- **Inequalities and comparisons.** Add the comparisons $\ne$ or $<$ to the bodies, and condition (2) is sufficient but not necessary. Let $Q_1() \leftarrow R(x, y), R(y, x)$ and $Q_2() \leftarrow R(u, v), u \le v$. Then $Q_1 \subseteq Q_2$, since one of $a \le b$ and $b \le a$ holds for each pair. But neither map, $u, v \mapsto x, y$ or $u, v \mapsto y, x$, carries the comparison $u \le v$ into a fact that $Q_1$ implies. Containment with comparisons needs a case split over the orders of the variables, and it is $\Pi_2^p$-complete.
- **Negation.** For CQs with negated atoms the criterion fails too, and the test must consider many databases, not one.
- **Unions.** For unions of CQs the theorem extends: $Q_1 \cup \cdots \cup Q_k \subseteq P_1 \cup \cdots \cup P_l$ if and only if each $Q_i$ is contained in some $P_j$ (Sagiv and Yannakakis 1980). The proof is the same: take the canonical database of $Q_i$.
- **Bag semantics.** If answers are counted with their multiplicities, as in SQL without DISTINCT, a homomorphism is not enough, and the decidability of containment of CQs under bag semantics has been open for a long time.
- **Full relational calculus.** For queries with all of first-order logic, containment is undecidable. See the [query containment problem](/query-containment-problem/).

## History

Ashok Chandra and Philip Merlin proved the theorem at STOC 1977, in a paper on the optimal implementation of conjunctive queries. They showed that containment, equivalence and evaluation of conjunctive queries are NP-complete and that each query has a unique minimal equivalent query. Aho, Sagiv and Ullman gave the same idea in the language of tableaux in 1979, with a polynomial-time minimization for a subclass. Sagiv and Yannakakis extended it to unions in 1980. The link to the constraint satisfaction problem, made explicit by Kolaitis and Vardi in 1998, explains which classes of queries are tractable.

## References
