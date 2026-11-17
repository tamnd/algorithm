---
tag: EYRQEM
kind: definition
slug: relational-calculus
name: Relational calculus
aliases:
- tuple relational calculus
- domain relational calculus
area: databases/relational-theory
level: core
summary: "First-order logic over relation names, in tuple or domain form, used as the declarative query language of the relational model. Its answers depend on the domain unless the query is domain independent."
prereqs: [relational-model, relational-algebra]
see_also: [codds-theorem, domain-independent-query, data-and-combined-complexity, conjunctive-query, datalog, sql-null-semantics, query-containment-problem, transitive-closure]
sources:
  - paper: "E. F. Codd, Relational completeness of data base sublanguages, in R. Rustin (ed.), Data Base Systems, Courant Computer Science Symposia 6, Prentice-Hall (1972), 65 to 98"
    locator: the tuple calculus with range-coupled quantifiers (Codd's calculus), and the definition of relational completeness
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Section 5.3 (the relational calculus, the natural and active domain semantics, and domain independence) and Section 5.4 (safe-range formulas)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: Chapter 4 (relational algebra and calculus), the sections on the tuple and the domain relational calculus
  - paper: doi:10.1145/567752.567763
    title: Alfred V. Aho and Jeffrey D. Ullman, The universality of data retrieval languages, Conference Record of the 6th ACM Symposium on Principles of Programming Languages (POPL), 110 to 120 (1979)
    locator: the transitive closure of a binary relation is not expressible in relational algebra, so not in the domain-independent calculus
---

The relational calculus is first-order logic used as a query language: a query is a formula over the relation names of a schema, and its answer is the set of tuples of values that make the formula true in the database. Codd proposed it in 1972, in a tuple form whose variables range over whole tuples, as the declarative standard for [relational algebra](/relational-algebra/); the domain form, whose variables range over single values, has the same power. A formula can mention values that are not in the database, for example with a negation, so the definition must say over which domain the variables range. The queries whose answer does not depend on that choice are the [domain-independent queries](/domain-independent-query/), and [Codd's theorem](/codds-theorem/) says that they are exactly the queries of relational algebra.

## Definition

The notation is that of Abiteboul, Hull and Vianu (AHV), named perspective, under set semantics. A schema is a finite set of relation names $R, S, \ldots$, each with a finite set of attributes $\mathrm{att}(R)$ of size $\mathrm{arity}(R)$. **dom** is a fixed countably infinite set of constants. An instance $I$ gives each $R$ a finite relation $I(R)$. The active domain $\mathrm{adom}(I)$ is the set of constants that occur in $I$, and $\mathrm{adom}(Q, I)$ adds the constants that occur in the query $Q$.

**Domain calculus.** Terms are variables $x, y, \ldots$ and constants. Formulas are built by these rules:

- $R(e_1, \ldots, e_k)$ for a relation name $R$ of arity $k$ and terms $e_i$ is an atom; $e = e'$ is an atom;
- if $\varphi$ and $\psi$ are formulas, then $\varphi \land \psi$, $\varphi \lor \psi$, $\neg \varphi$ and $\varphi \rightarrow \psi$ are formulas;
- if $\varphi$ is a formula and $x$ a variable, then $\exists x\, \varphi$ and $\forall x\, \varphi$ are formulas.

The free variables $\mathrm{free}(\varphi)$ are defined as usual. A *query* is an expression

$$Q = \{\, (x_1, \ldots, x_k) \mid \varphi \,\},$$

where $x_1, \ldots, x_k$ are distinct variables and $\mathrm{free}(\varphi) = \{x_1, \ldots, x_k\}$. A query with $k = 0$ is Boolean: its answer is $\{()\}$ (true) or $\emptyset$ (false).

**Semantics relative to a domain.** Let $\mathbf{d}$ be a set of constants with $\mathrm{adom}(Q, I) \subseteq \mathbf{d} \subseteq \mathbf{dom}$. A valuation $\nu$ maps variables to $\mathbf{d}$ and is the identity on constants. Truth $I \models_{\mathbf{d}} \varphi[\nu]$ is defined by induction: $R(e_1, \ldots, e_k)$ holds when $(\nu(e_1), \ldots, \nu(e_k)) \in I(R)$, $e = e'$ holds when $\nu(e) = \nu(e')$, the connectives have their Boolean meaning, and $\exists x\, \varphi$ (or $\forall x\, \varphi$) holds when $\varphi$ holds for some (or every) value of $x$ in $\mathbf{d}$. The answer is

$$Q_{\mathbf{d}}(I) = \{\, (\nu(x_1), \ldots, \nu(x_k)) \mid \nu : \mathrm{free}(\varphi) \to \mathbf{d},\ I \models_{\mathbf{d}} \varphi[\nu] \,\}.$$

Three readings of a query are in use, and they are not the same:

- *natural semantics*: $\mathbf{d} = \mathbf{dom}$. The answer can be infinite.
- *active domain semantics*: $\mathbf{d} = \mathrm{adom}(Q, I)$. The answer is always finite, and it can be computed by brute force over the finite domain.
- *domain independent* queries: $Q_{\mathbf{d}}(I) = Q_{\mathbf{d}'}(I)$ for every instance $I$ and all $\mathbf{d}, \mathbf{d}'$ that contain $\mathrm{adom}(Q, I)$. For such a query the two semantics above agree, and one writes $Q(I)$. See [domain-independent query](/domain-independent-query/) for this class and its decidable subclass, the safe-range queries.

**Tuple calculus.** A tuple variable $t$ has a sort, a set of attributes. Atoms are $R(t)$ with $\mathrm{sort}(t) = \mathrm{att}(R)$, and $t.A = s.B$ or $t.A = c$ for attributes in the sorts and a constant $c$. Connectives and quantifiers are as above, with quantifiers over tuples of the given sort. A query is $\{\, t : X \mid \varphi \,\}$, where $t$ is the only free variable and $X$ is its sort. A tuple variable of sort $\{A_1, \ldots, A_k\}$ is the same as $k$ domain variables, one per attribute, so each tuple calculus query translates into a domain calculus query with the same answer under each of the three readings, and back. The two forms differ only in notation.

Codd's own calculus of 1972 is a tuple calculus in which every tuple variable is bound to a relation by a range term, such as "$t$ in $R$". That restriction makes every query of his calculus domain independent. The free form above is the one of the textbooks, and AHV use it.

## Examples and non-examples

Take the schema $\mathrm{Takes}(\mathit{student}, \mathit{course})$ and $\mathrm{Course}(\mathit{course})$ and the instance

$$I(\mathrm{Takes}) = \{(\mathit{ann}, \mathit{db}), (\mathit{ann}, \mathit{os}), (\mathit{bob}, \mathit{db}), (\mathit{cal}, \mathit{os})\}, \qquad I(\mathrm{Course}) = \{\mathit{db}, \mathit{os}\}.$$

So $\mathrm{adom}(I) = \{\mathit{ann}, \mathit{bob}, \mathit{cal}, \mathit{db}, \mathit{os}\}$, five constants.

- **A selection.** $\{(s) \mid \mathrm{Takes}(s, \mathit{db})\}$ returns $\{\mathit{ann}, \mathit{bob}\}$ on every domain. In algebra it is $\pi_{\mathit{student}}(\sigma_{\mathit{course} = \mathit{db}}(\mathrm{Takes}))$.
- **The same query in tuple form.** $\{\, t : \{\mathit{student}\} \mid \exists u\, (\mathrm{Takes}(u) \land u.\mathit{course} = \mathit{db} \land t.\mathit{student} = u.\mathit{student}) \,\}$.
- **A universal query.** The students who take every course:

$$\{\, (s) \mid \exists c\, \mathrm{Takes}(s, c) \land \forall c\, (\mathrm{Course}(c) \rightarrow \mathrm{Takes}(s, c)) \,\}.$$

The answer is $\{\mathit{ann}\}$: bob misses os and cal misses db. The first conjunct ties $s$ to the database, and the implication restricts the universal quantifier to the courses, so the answer is the same on every domain. In algebra it is the division $\mathrm{Takes} \div \mathrm{Course}$, which is $\pi_{\mathit{student}}(\mathrm{Takes}) - \pi_{\mathit{student}}((\pi_{\mathit{student}}(\mathrm{Takes}) \times \mathrm{Course}) - \mathrm{Takes})$, where $-$ is set difference. That expression also gives $\{\mathit{ann}\}$.

- **Non-example: an unrestricted negation.** $\{(s) \mid \neg \mathrm{Takes}(s, \mathit{db})\}$. Under natural semantics the answer is infinite: every constant of **dom** except ann and bob. Under active domain semantics it is $\{\mathit{cal}, \mathit{db}, \mathit{os}\}$, which contains the two course names, because nothing in the formula says that $s$ is a student. The query is not domain independent. The intended query is $\{(s) \mid \exists c\, \mathrm{Takes}(s, c) \land \neg \mathrm{Takes}(s, \mathit{db})\}$, with answer $\{\mathit{cal}\}$ on every domain.
- **Non-example: a disjunction with different free variables.** $\{(x, y) \mid \mathrm{Takes}(x, \mathit{db}) \lor \mathrm{Course}(y)\}$. For a domain $\mathbf{d}$ of size $n$ that contains the five constants, the answer has $2n + 2n - 4 = 4n - 4$ pairs: 16 pairs for $n = 5$ and 20 pairs for $n = 6$. The answer grows with the domain.
- **Non-example: a bare universal quantifier.** $\{(s) \mid \forall c\, \mathrm{Takes}(s, c)\}$. On the instance $J$ with $J(\mathrm{Takes}) = \{(a, a)\}$, the active domain is $\{a\}$ and the answer is $\{a\}$. Add one more constant $b$ to the domain and the answer is empty, since $(a, b) \notin J(\mathrm{Takes})$.

## Related definitions

- **Relational algebra.** [Relational algebra](/relational-algebra/) is the procedural language of the model. By [Codd's theorem](/codds-theorem/), the algebra, the domain-independent calculus, the safe-range calculus and the calculus under active domain semantics express the same queries.
- **Domain independence and safety.** Domain independence is a semantic property, and it is undecidable. The safe-range formulas are a syntactic class with the same power. See [domain-independent query](/domain-independent-query/).
- **Fragments.** The formulas with only $\exists$ and $\land$ over atoms are the [conjunctive queries](/conjunctive-query/), the select-project-join queries of the algebra. Adding $\lor$ gives the positive existential queries, which are the unions of conjunctive queries. Containment is decidable for these fragments and undecidable for the full calculus (see [query containment](/query-containment-problem/)).
- **Recursion.** The calculus cannot express the [transitive closure](/transitive-closure/) of a binary relation (Aho and Ullman 1979). [Datalog](/datalog/) adds recursion to the positive fragment.
- **Complexity.** A fixed calculus query is evaluated in polynomial time in the size of the instance, and the problem is much harder when the query is part of the input. See [data complexity and combined complexity](/data-and-combined-complexity/).
- **SQL.** The WHERE clause of SQL with EXISTS and NOT EXISTS is a tuple calculus over bags. With nulls, SQL uses a three-valued logic instead of the two-valued logic above; see [three-valued logic of SQL nulls](/sql-null-semantics/).

## References
