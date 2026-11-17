---
tag: CYWMQ4
kind: definition
slug: domain-independent-query
name: Domain-independent query
aliases:
- safe query
- safe-range query
area: databases/relational-theory
level: advanced
summary: "A calculus query whose answer depends only on the database and not on the domain of values. The property is undecidable; the safe-range queries are a decidable subclass with the same power."
prereqs: [relational-calculus]
see_also: [codds-theorem, relational-algebra, data-and-combined-complexity, conjunctive-query, datalog, undecidability, church-theorem, query-containment-problem]
sources:
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Section 5.3 (domain independence and the active domain semantics), Section 5.4 (safe-range normal form, the range restriction rules and safe-range queries), Chapter 6 (undecidability results for the calculus)
  - paper: doi:10.1145/321510.321524
    title: Robert A. Di Paola, The recursive unsolvability of the decision problem for the class of definite formulas, Journal of the ACM 16(2), 324 to 327 (1969)
    locator: there is no algorithm that decides whether a first-order formula is definite (domain independent)
  - paper: "E. F. Codd, Relational completeness of data base sublanguages, in R. Rustin (ed.), Data Base Systems, Courant Computer Science Symposia 6, Prentice-Hall (1972), 65 to 98"
    locator: the range-coupled tuple calculus, whose queries are domain independent by construction
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Chapter 3 (the relational calculus, domain independence and a syntactic class of safe formulas)
---

A query of the [relational calculus](/relational-calculus/) is domain independent when its answer on a database is the same for every domain of values that contains the constants of the database and of the query. Such a query asks only about the data: it cannot return a value that is in neither, and its answer does not grow when the domain grows. The property is undecidable (Di Paola 1969), so database theory uses the safe-range formulas of Abiteboul, Hull and Vianu, a syntactic class that one checks by a pass over the formula and that expresses the same queries. By [Codd's theorem](/codds-theorem/), these are the queries of [relational algebra](/relational-algebra/).

## Definition

The notation follows the [relational calculus](/relational-calculus/) page, under set semantics. A query is $Q = \{(x_1, \ldots, x_k) \mid \varphi\}$ over a schema, $I$ is an instance, and $Q_{\mathbf{d}}(I)$ is the answer when the variables range over a set $\mathbf{d}$ with $\mathrm{adom}(Q, I) \subseteq \mathbf{d}$.

**Domain independence (semantic).** $Q$ is *domain independent* if for every instance $I$ and every two sets $\mathbf{d}, \mathbf{d}'$ with $\mathrm{adom}(Q, I) \subseteq \mathbf{d}, \mathbf{d}' \subseteq \mathbf{dom}$,

$$Q_{\mathbf{d}}(I) = Q_{\mathbf{d}'}(I).$$

Then $Q(I)$ denotes this common answer. It is a subset of $\mathrm{adom}(Q, I)^k$, since the answer for $\mathbf{d} = \mathrm{adom}(Q, I)$ is. Codd's range-coupled calculus and Di Paola's "definite formulas" are earlier names for the same idea.

**Safe-range (syntactic).** First put $\varphi$ in *safe-range normal form* (SRNF): rename bound variables so that no variable is bound twice or both bound and free; replace $\forall x\, \psi$ by $\neg \exists x\, \neg \psi$ and $\psi \rightarrow \chi$ by $\neg \psi \lor \chi$; push each negation down with De Morgan's laws and $\neg\neg\psi = \psi$, until it stands in front of an atom or of an $\exists$; flatten nested $\land$ and $\lor$. Then compute the set $\mathrm{rr}(\varphi)$ of *range-restricted* variables, or the failure value $\bot$, by these rules (any rule that meets $\bot$ in a part returns $\bot$):

- $\mathrm{rr}(R(e_1, \ldots, e_k))$ is the set of variables among $e_1, \ldots, e_k$;
- $\mathrm{rr}(x = c) = \{x\}$ for a constant $c$, and $\mathrm{rr}(x = y) = \emptyset$ for variables;
- $\mathrm{rr}(\psi \land x = y)$ is $\mathrm{rr}(\psi) \cup \{x, y\}$ if $x$ or $y$ is in $\mathrm{rr}(\psi)$, and $\mathrm{rr}(\psi)$ if not; for other conjunctions, $\mathrm{rr}(\psi \land \chi) = \mathrm{rr}(\psi) \cup \mathrm{rr}(\chi)$;
- $\mathrm{rr}(\psi \lor \chi) = \mathrm{rr}(\psi) \cap \mathrm{rr}(\chi)$;
- $\mathrm{rr}(\neg \psi) = \emptyset$;
- $\mathrm{rr}(\exists x\, \psi) = \mathrm{rr}(\psi) \setminus \{x\}$ if $x \in \mathrm{rr}(\psi)$, and $\bot$ if not.

$Q$ is *safe-range* if $\mathrm{rr}(\mathrm{SRNF}(\varphi)) = \mathrm{free}(\varphi)$. This is the definition of AHV, Section 5.4. A variable is range restricted when every way to make the formula true binds it to a value of an atom or a constant: that is why a disjunction keeps only the variables that both sides restrict, and a negation restricts none.

**The two facts.** Every safe-range query is domain independent, by induction on the SRNF: a subformula with $\mathrm{rr} = X$ is false under every valuation that maps a variable of $X$ outside the active domain, and each quantifier ranges only over values that some atom supplies. Conversely, every domain-independent query is equivalent to a safe-range query, because it equals an algebra expression, and each algebra expression translates into a safe-range formula. Both facts are parts of the proof of [Codd's theorem](/codds-theorem/).

**Undecidability.** No algorithm decides whether a calculus query is domain independent. Here is a reduction from the finite satisfiability of first-order sentences, which is undecidable by Trakhtenbrot's theorem (AHV, Chapter 6). Let $\psi$ be a sentence over a schema with a relation of arity at least 2, and add a unary relation name $D$. Let $\psi^{D}$ be $\psi$ with each quantifier restricted to $D$: $\exists x\, \chi$ becomes $\exists x\, (D(x) \land \chi)$ and $\forall x\, \chi$ becomes $\forall x\, (D(x) \rightarrow \chi)$. Let

$$Q_\psi = \{\, (z) \mid \exists y\, D(y) \land \psi^{D} \,\}.$$

The sentence $\exists y\, D(y) \land \psi^{D}$ does not depend on the domain, because all its quantifiers range over $D$. If $\psi$ has no finite model, it is false in every instance, and $Q_\psi$ returns $\emptyset$ on every domain, so $Q_\psi$ is domain independent. If $\psi$ has a finite model $A$, let $I$ hold the relations of $A$ and $I(D) = $ the universe of $A$. Then the sentence is true in $I$, and $Q_{\mathbf{d}}(I) = \mathbf{d}$ for every $\mathbf{d}$, so $Q_\psi$ is not domain independent. So $Q_\psi$ is domain independent if and only if $\psi$ has no finite model. In contrast, the test "is $Q$ safe-range" is one pass over the SRNF, with set operations on the free variables, so it takes polynomial time in the size of the formula.

## Examples and non-examples

Use the schema $\mathrm{Takes}(\mathit{student}, \mathit{course})$, $\mathrm{Course}(\mathit{course})$ of the [relational calculus](/relational-calculus/) page, and its instance with five constants.

- **Safe-range.** $\{(s) \mid \mathrm{Takes}(s, \mathit{db})\}$: the atom gives $\mathrm{rr} = \{s\}$, which equals the free variables.
- **Safe-range with a universal quantifier.** $\{(s) \mid \exists c\, \mathrm{Takes}(s, c) \land \forall c\, (\mathrm{Course}(c) \rightarrow \mathrm{Takes}(s, c))\}$. After renaming the second $c$ to $c'$, the SRNF is $\exists c\, \mathrm{Takes}(s, c) \land \neg \exists c'\, (\mathrm{Course}(c') \land \neg \mathrm{Takes}(s, c'))$. Inside, $\mathrm{rr}(\mathrm{Course}(c') \land \neg \mathrm{Takes}(s, c')) = \{c'\}$, so the inner $\exists c'$ gives $\emptyset$ and the negation gives $\emptyset$. The first conjunct gives $\{s\}$. The union is $\{s\}$, the free variables. The query is safe-range, and its answer is $\{\mathit{ann}\}$ on every domain.
- **Not safe-range and not domain independent.** $\{(s) \mid \neg \mathrm{Takes}(s, \mathit{db})\}$ has $\mathrm{rr} = \emptyset \neq \{s\}$. $\{(x, y) \mid \mathrm{Takes}(x, \mathit{db}) \lor \mathrm{Course}(y)\}$ has $\mathrm{rr} = \{x\} \cap \{y\} = \emptyset$. $\{(s) \mid \forall c\, \mathrm{Takes}(s, c)\}$ has SRNF $\neg \exists c\, \neg \mathrm{Takes}(s, c)$, and the rule for $\exists c$ fails, since $c \notin \mathrm{rr}(\neg \mathrm{Takes}(s, c)) = \emptyset$. The relational calculus page shows that each of the three answers changes with the domain.
- **Domain independent but not safe-range.** $\{(x) \mid R(x) \lor (x = x \land \neg (x = x))\}$. The second disjunct is false for every value, so the query is equivalent to $\{(x) \mid R(x)\}$ and is domain independent. But $\mathrm{rr}(x = x \land \neg(x = x)) = \emptyset$, so $\mathrm{rr}$ of the disjunction is $\{x\} \cap \emptyset = \emptyset$, and the query is not safe-range. Safe-range is a sufficient condition, not a necessary one; it only promises that an equivalent safe-range query exists.
- **Active domain semantics.** Any query, safe or not, has a domain-independent version: relativize every free and bound variable to the formula $\mathrm{adom}(x)$, the disjunction of $\exists \ldots R(\ldots, x, \ldots)$ over each relation and position and of $x = c$ over each constant of $Q$. On the instance above, $\{(s) \mid \mathrm{adom}(s) \land \neg \mathrm{Takes}(s, \mathit{db})\}$ returns $\{\mathit{cal}, \mathit{db}, \mathit{os}\}$ on every domain. This is how a system can evaluate any formula, but the answer is often not the intended one.

## Related definitions

- **Relational calculus and algebra.** The definitions of the semantics are on [relational calculus](/relational-calculus/), and the equivalence with the algebra is [Codd's theorem](/codds-theorem/).
- **Other syntactic classes.** Ullman's safe formulas (Ullman 1988, Chapter 3) are another syntactic class of domain-independent formulas, with other rules for the same aim. The book shows that they also express every query of the algebra.
- **Range restriction in rules.** A [conjunctive query](/conjunctive-query/) and a [Datalog](/datalog/) rule must have each head variable in a positive body atom. That is the same condition for the positive fragment, and it makes each rule domain independent.
- **Other words "safe".** In probabilistic databases, a "safe plan" is a plan that computes the right probabilities by independence rules (see [probabilistic database](/probabilistic-database/)). That notion has nothing to do with domain independence.
- **Decision problems.** Domain independence is undecidable for the same reason that satisfiability and [containment](/query-containment-problem/) of calculus queries are undecidable: all three encode finite satisfiability, see [Church's theorem](/church-theorem/) for the unrestricted case and [undecidability](/undecidability/) for the general idea.

## References
