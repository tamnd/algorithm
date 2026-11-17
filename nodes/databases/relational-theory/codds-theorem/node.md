---
tag: TP5RJX
kind: theorem
slug: codds-theorem
name: "Codd's theorem"
aliases:
- equivalence of relational algebra and calculus
area: databases/relational-theory
level: core
summary: "Relational algebra and the domain-independent (or safe-range) relational calculus express exactly the same queries, under set semantics, and each translates into the other."
prereqs: [relational-algebra, relational-calculus, domain-independent-query]
see_also: [relational-model, data-and-combined-complexity, query-containment-problem, datalog, conjunctive-query, transitive-closure, query-optimization, sql-null-semantics]
sources:
  - paper: "E. F. Codd, Relational completeness of data base sublanguages, in R. Rustin (ed.), Data Base Systems, Courant Computer Science Symposia 6, Prentice-Hall (1972), 65 to 98"
    locator: the relational algebra, the tuple calculus with range-coupled quantifiers, the reduction algorithm from the calculus to the algebra, and the definition of relational completeness
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Section 5.1 (the relational algebras), Section 5.3 (the calculus and domain independence), Section 5.4 (safe-range formulas and the equivalence of the algebra, the domain-independent calculus, the safe-range calculus and the active domain calculus)
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Chapter 3 (the relational algebra, the domain and tuple calculus, safe formulas and the equivalence proofs)
  - paper: doi:10.1145/567752.567763
    title: Alfred V. Aho and Jeffrey D. Ullman, The universality of data retrieval languages, Conference Record of the 6th ACM Symposium on Principles of Programming Languages (POPL), 110 to 120 (1979)
    locator: the transitive closure is not expressible in relational algebra, a limit of relational completeness
  - paper: doi:10.1145/362384.362685
    title: E. F. Codd, A relational model of data for large shared data banks, Communications of the ACM 13(6), 377 to 387 (1970)
    locator: the relational model and its first operators
  - paper: doi:10.1145/321510.321524
    title: Robert A. Di Paola, The recursive unsolvability of the decision problem for the class of definite formulas, Journal of the ACM 16(2), 324 to 327 (1969)
    locator: definite (domain-independent) formulas are undecidable
---

Codd's theorem says that [relational algebra](/relational-algebra/) and the [relational calculus](/relational-calculus/), restricted to [domain-independent queries](/domain-independent-query/), express exactly the same queries. Each algebra expression translates into a calculus formula with the same answer on every database, and each domain-independent formula translates into an algebra expression. Codd proved a form of it in 1972 for his own tuple calculus, and called a language *relationally complete* when it expresses all these queries. This page proves the form of Abiteboul, Hull and Vianu (AHV), which also brings in the safe-range formulas and the active domain semantics.

## Statement

Fix a database schema, a countably infinite set of constants **dom**, and set semantics. The *relational algebra* has the relation names, the constant relations $\{\langle A : c \rangle\}$, and the operators $\sigma_{A = c}$, $\sigma_{A = B}$, $\pi_X$, $\rho_{A \to B}$, $\cup$, $-$ (set difference) and $\bowtie$ (natural join, which is the product $\times$ when the attribute sets are disjoint). The calculus is the domain calculus with the three readings of the [relational calculus](/relational-calculus/) page. Two queries are *equivalent* when they have the same answer on every instance (for calculus queries, under the stated reading). A tuple of a calculus query is read as a tuple over attributes named by its free variables.

**Theorem (Codd 1972; AHV, Section 5.4).** The following four classes of queries are the same:

1. the queries of the relational algebra;
2. the domain-independent queries of the calculus;
3. the safe-range queries of the calculus;
4. the queries of the calculus under active domain semantics.

The translations are effective: there are algorithms that map a query of each class to an equivalent query of each other class.

## In plain words

There are two ways to write a database query. One is a recipe: take this table, keep these rows, join with that table, remove these columns. The other is a description: give me every student such that there is a course the student takes and no required course the student skips. The theorem says that the two ways are equally strong. Every recipe can be written as a description, and every sensible description can be turned into a recipe.

"Sensible" matters. A description such as "every value that is not a student" has an answer that depends on the set of all possible values, not on the data. Such descriptions are excluded. The ones that remain can be checked by a simple syntax rule, and a database system can turn each of them into a plan that it runs.

## Proof

Write $\mathrm{adom} = \mathrm{adom}(Q, I)$ for the constants of the instance $I$ and of the query $Q$. The proof shows (1) to (3), (3) to (2), (2) to (4) and (4) to (1).

**(1) to (3): algebra to safe-range calculus.** For an expression $E$ with attributes $A_1, \ldots, A_k$, use one variable $x_A$ per attribute and build $\varphi_E$ with $\mathrm{free}(\varphi_E) = \{x_{A_1}, \ldots, x_{A_k}\}$:

- $R$: $R(x_{A_1}, \ldots, x_{A_k})$; $\{\langle A : c \rangle\}$: $x_A = c$;
- $\sigma_{A = c}(E)$: $\varphi_E \land x_A = c$; $\sigma_{A = B}(E)$: $\varphi_E \land x_A = x_B$;
- $\pi_X(E)$: $\exists \bar y\, \varphi_E$, where $\bar y$ are the variables of the attributes not in $X$; $\rho_{A \to B}(E)$: $\varphi_E$ with $x_A$ renamed to $x_B$;
- $E_1 \cup E_2$: $\varphi_{E_1} \lor \varphi_{E_2}$; $E_1 - E_2$: $\varphi_{E_1} \land \neg \varphi_{E_2}$; $E_1 \bowtie E_2$: $\varphi_{E_1} \land \varphi_{E_2}$, where shared attributes share a variable.

*Same answer.* By induction on $E$: for every $\mathbf{d} \supseteq \mathrm{adom}$ and every valuation $\nu$ into $\mathbf{d}$, $I \models_{\mathbf{d}} \varphi_E[\nu]$ if and only if the tuple $\nu(x_{A_1}), \ldots, \nu(x_{A_k})$ is in $E(I)$. The atom, constant, selection, renaming, union, difference and join cases follow from the definitions of the operators and of the connectives. For $\pi_X(E)$: a tuple $t$ over $X$ is in $\pi_X(E)(I)$ if and only if some tuple $s \in E(I)$ extends $t$. Every value of $s$ is in $\mathrm{adom} \subseteq \mathbf{d}$, so the witness for $\exists \bar y$ exists in $\mathbf{d}$, and by the induction hypothesis the two conditions agree. So $\varphi_E$ gives $E(I)$ on every domain, and the query is domain independent.

*Safe-range.* By induction, $\mathrm{rr}(\mathrm{SRNF}(\varphi_E)) = \mathrm{free}(\varphi_E)$, with the rules of [domain-independent query](/domain-independent-query/). An atom restricts its variables, $x_A = c$ restricts $x_A$, and $\varphi_E \land x_A = x_B$ adds both variables because $x_A$ is already restricted. In $\exists \bar y\, \varphi_E$ each $y$ is restricted in $\varphi_E$, so the rule for $\exists$ succeeds. In a union both sides have the same free variables, all restricted, so the intersection keeps them all. For $\varphi_{E_1} \land \neg \varphi_{E_2}$, the SRNF only moves the negation in front of atoms and of $\exists$ subformulas of $\varphi_{E_2}$, which already pass the rule for $\exists$; so no $\bot$ appears, and the conjunction keeps $\mathrm{rr}(\varphi_{E_1})$, which is all the free variables. A join is a union of the two restricted sets.

**(3) to (2): safe-range queries are domain independent.** Let $\varphi$ be in SRNF with $\mathrm{rr}(\varphi) = \mathrm{free}(\varphi)$. Two claims hold for each subformula $\psi$ and each pair $\mathbf{d}, \mathbf{d}' \supseteq \mathrm{adom}$.

*Claim A.* If $\nu$ maps $\mathrm{free}(\psi)$ into $\mathbf{d}$ and $I \models_{\mathbf{d}} \psi[\nu]$, then $\nu(x) \in \mathrm{adom}$ for each $x \in \mathrm{rr}(\psi)$. Induction: an atom of $I$ holds only on values of $I$; $x = c$ forces $\nu(x) = c \in \mathrm{adom}$; in $\psi \land x = y$ the equality copies a value in $\mathrm{adom}$ from one variable to the other; a conjunction is true only if each conjunct is; a disjunction is true only if one side is, and $\mathrm{rr}$ keeps only the variables that both sides restrict; $\mathrm{rr}(\neg \psi) = \emptyset$ claims nothing; for $\exists x\, \psi$, take the witness value $a$ and apply the hypothesis to $\nu$ extended by $x \mapsto a$.

*Claim B.* If $\nu$ maps $\mathrm{free}(\psi)$ into $\mathbf{d} \cap \mathbf{d}'$, then $I \models_{\mathbf{d}} \psi[\nu]$ if and only if $I \models_{\mathbf{d}'} \psi[\nu]$. Induction: atoms and equalities do not look at the domain, and the connectives keep the property. For $\exists x\, \psi$, suppose it is true in $\mathbf{d}$ with witness $a \in \mathbf{d}$. The rule for $\exists$ succeeded, so $x \in \mathrm{rr}(\psi)$, and Claim A gives $a \in \mathrm{adom} \subseteq \mathbf{d}'$. The extended valuation maps into $\mathbf{d} \cap \mathbf{d}'$, so by the hypothesis $\psi$ is true in $\mathbf{d}'$ and $a$ is a witness there. The other direction is the same.

Now let $t \in Q_{\mathbf{d}}(I)$, given by $\nu$. All free variables are in $\mathrm{rr}(\varphi)$, so by Claim A, $\nu$ maps into $\mathrm{adom} \subseteq \mathbf{d} \cap \mathbf{d}'$, and by Claim B, $t \in Q_{\mathbf{d}'}(I)$. By symmetry $Q_{\mathbf{d}}(I) = Q_{\mathbf{d}'}(I)$.

**(2) to (4).** A domain-independent $Q$ has $Q(I) = Q_{\mathrm{adom}}(I)$, which is the active domain answer of the same formula.

**(4) to (1): active domain calculus to algebra.** First an expression for the active domain, with one attribute $D$:

$$\mathrm{ADOM} = \bigcup_{R} \bigcup_{A \in \mathrm{att}(R)} \rho_{A \to D}(\pi_A(R)) \;\cup\; \bigcup_{c \in Q} \{\langle D : c \rangle\}.$$

$\mathrm{ADOM}(I) = \mathrm{adom}$. Write $\mathrm{ADOM}_x$ for $\rho_{D \to x}(\mathrm{ADOM})$. Replace $\forall x\, \psi$ by $\neg \exists x\, \neg \psi$ and $\psi \rightarrow \chi$ by $\neg \psi \lor \chi$. For each subformula $\psi$ with free variables $Y$, build $E_\psi$ with one attribute per variable of $Y$, such that

$$E_\psi(I) = \{\, \nu \mid \nu : Y \to \mathrm{adom},\ I \models_{\mathrm{adom}} \psi[\nu] \,\}.$$

- $R(e_1, \ldots, e_k)$: apply $\sigma_{A_i = c}$ to each position $i$ that holds a constant $c$ and $\sigma_{A_i = A_j}$ to each two positions with the same variable, then project on one position per variable and rename it to the variable.
- $x = c$: $\{\langle x : c \rangle\}$. $x = y$: $\sigma_{x = y}(\mathrm{ADOM}_x \times \mathrm{ADOM}_y)$. $x = x$: $\mathrm{ADOM}_x$.
- $\psi \land \chi$: $E_\psi \bowtie E_\chi$.
- $\psi \lor \chi$: extend each side to the variables $Y_\psi \cup Y_\chi$ by a product with $\mathrm{ADOM}_y$ for each missing $y$, then take the union.
- $\neg \psi$: $(\mathrm{ADOM}_{y_1} \times \cdots \times \mathrm{ADOM}_{y_m}) - E_\psi$ for $Y = \{y_1, \ldots, y_m\}$, with $\{()\}$ for $m = 0$.
- $\exists x\, \psi$: $\pi_{Y \setminus \{x\}}(E_\psi)$ if $x$ is free in $\psi$, and $E_\psi \times \pi_{\emptyset}(\mathrm{ADOM}_x)$ if not; the factor is $\{()\}$ if the active domain is not empty and $\emptyset$ if it is, as the semantics of $\exists$ requires.

Each case follows from the definition of truth with the variables ranging over $\mathrm{adom}$: the join matches valuations on the shared variables, the padding and the complement are taken inside $\mathrm{adom}$, and the projection is the existential quantifier over $\mathrm{adom}$. For the query $\{(x_1, \ldots, x_k) \mid \varphi\}$, the expression $E_\varphi$ gives the active domain answer. So each class is contained in the next one around the cycle, and the four classes are equal. Each step is an algorithm on the syntax.

## Consequences

- **An example of both directions.** Take $\mathrm{Takes}(\mathit{student}, \mathit{course})$ with the tuples $(\mathit{ann}, \mathit{db})$, $(\mathit{ann}, \mathit{os})$, $(\mathit{bob}, \mathit{db})$, $(\mathit{cal}, \mathit{os})$. The safe-range query $\{(s) \mid \exists c\, \mathrm{Takes}(s, c) \land \neg \mathrm{Takes}(s, \mathit{db})\}$ has the algebra form $\rho_{\mathit{student} \to s}(\pi_{\mathit{student}}(\mathrm{Takes}) - \pi_{\mathit{student}}(\sigma_{\mathit{course} = \mathit{db}}(\mathrm{Takes})))$, and both give $\{\mathit{cal}\}$. The formula $\neg \mathrm{Takes}(s, \mathit{db})$ alone is not domain independent. Step (4) to (1) turns it into $\mathrm{ADOM}_s - \rho_{\mathit{student} \to s}(\pi_{\mathit{student}}(\sigma_{\mathit{course} = \mathit{db}}(\mathrm{Takes})))$, whose answer is $\{\mathit{cal}, \mathit{db}, \mathit{os}\}$: the active domain answer, which includes the two course names.
- **Relational completeness.** Codd used the theorem as a yardstick: a query language is relationally complete if it expresses every algebra query. The SELECT FROM WHERE core of SQL with NOT EXISTS, UNION and EXCEPT is relationally complete under set semantics.
- **Compilation of declarative queries.** A system can accept a declarative query, check that it is safe-range, and translate it into an algebra plan. The plan is then rewritten by algebraic laws during [query optimization](/query-optimization/).
- **Transfer of results.** Results proved for one language hold for the other. The calculus is first-order logic, so the undecidability of finite satisfiability (Trakhtenbrot) makes equivalence and [containment](/query-containment-problem/) of algebra expressions undecidable. Logical bounds on expressive power apply to the algebra too: the [transitive closure](/transitive-closure/) of a binary relation is not expressible (Aho and Ullman 1979), which is why [Datalog](/datalog/) adds recursion. The data complexity bounds of first-order logic also hold for the algebra; see [data complexity and combined complexity](/data-and-combined-complexity/).
- **Sizes of the translations.** Step (1) to (3) gives a formula with one connective or quantifier per operator. Step (4) to (1) gives one operator per connective, plus copies of $\mathrm{ADOM}$, whose size is linear in the schema and the number of constants; so the output size is polynomial in the input.
- **Fragments.** The same construction, restricted, gives smaller equivalences: the SPJR algebra (selection, projection, join, renaming) and the calculus with only $\exists$ and $\land$ over atoms both express the [conjunctive queries](/conjunctive-query/), and adding union on one side and $\lor$ on the other gives the unions of conjunctive queries.

## Tightness

- **Domain-dependent queries have no algebra form.** Under natural semantics, $\{(s) \mid \neg \mathrm{Takes}(s, \mathit{db})\}$ has an infinite answer, while an algebra expression always has a finite answer made of active domain values. So the restriction to domain-independent queries in (2) cannot be dropped. Under active domain semantics the formula has an algebra form, but with another meaning.
- **Set semantics.** The theorem is about sets. Under bag semantics the algebra keeps multiplicities: $\pi_A(R)$ can hold one value twice, and a calculus whose answers are sets cannot express that answer. SQL works on bags, and its relation to the calculus needs a separate treatment.
- **Nulls.** The theorem assumes two-valued logic and no nulls. SQL with nulls uses a three-valued logic, so a translation between SQL and a calculus query must handle UNKNOWN; see [three-valued logic of SQL nulls](/sql-null-semantics/).
- **Aggregates, order and recursion.** Counting, sums, comparisons with a built-in order and recursion are outside both languages. An equivalence for an extended language must be proved again for that extension.
- **Codd's calculus.** Codd's 1972 calculus binds each tuple variable to a relation, and his proof is a reduction algorithm for that syntax. It is not the textbook domain calculus, and his notion of completeness was relative to his calculus. The modern form above is the one of AHV and of Ullman.

## History

Codd introduced the relational model in 1970 and defined the relational algebra and a tuple calculus in the 1972 paper "Relational completeness of data base sublanguages". There he gave an algorithm that reduces each calculus query to an algebra expression, and he defined relational completeness. Later textbooks, among them Ullman (1988) and Abiteboul, Hull and Vianu (1995), restated the result for the domain calculus with domain independence, safe formulas and the active domain semantics, and gave the four-way equivalence proved above. Di Paola had shown in 1969 that definite formulas, the same idea as domain independence, are undecidable, which is why a syntactic class such as the safe-range formulas is needed.

## References
