---
tag: DCKXBX
kind: definition
slug: inclusion-dependency
name: Inclusion dependency
aliases:
- IND
- referential integrity constraint
area: databases/relational-theory
level: core
summary: A constraint that the projection of one relation on some attributes is a subset of the projection of another, as a foreign key states.
prereqs: [relational-model, functional-dependency]
see_also: [tuple-generating-dependency, equality-generating-dependency, chase-algorithm, dependency-implication-problem, candidate-key, weak-acyclicity, pspace, undecidability]
sources:
  - paper: doi:10.1016/0022-0000(84)90075-8
    title: Marco A. Casanova, Ronald Fagin and Christos H. Papadimitriou, Inclusion dependencies and their interaction with functional dependencies, Journal of Computer and System Sciences 28(1), 29 to 59 (1984)
    locator: the definition of inclusion dependencies, the complete set of three inference rules, the PSPACE-completeness of implication, and the interaction with functional dependencies
  - paper: doi:10.1016/s0019-9958(83)80002-3
    title: John C. Mitchell, The implication problem for functional and inclusion dependencies, Information and Control 56(3), 154 to 173 (1983)
    locator: implication of functional and inclusion dependencies together
  - paper: doi:10.1137/0214049
    title: Ashok K. Chandra and Moshe Y. Vardi, The implication problem for functional and inclusion dependencies is undecidable, SIAM Journal on Computing 14(3), 671 to 677 (1985)
    locator: the undecidability of implication for functional and inclusion dependencies together
  - paper: doi:10.1016/0022-0000(84)90081-3
    title: David S. Johnson and Anthony Klug, Testing containment of conjunctive queries under functional and inclusion dependencies, Journal of Computer and System Sciences 28(1), 167 to 189 (1984)
    locator: containment of conjunctive queries under inclusion dependencies, by the chase
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 9 (inclusion dependency), the inference rules, finite and unrestricted implication, and the chase for inclusion dependencies
---

An inclusion dependency (IND) says that each combination of values that occurs in some columns of one relation also occurs in some columns of another relation, or of the same relation. A foreign key is the common case: each customer number in the orders table must be the number of a customer in the customers table. Casanova, Fagin and Papadimitriou (1984) studied INDs as a class of dependencies. For INDs alone, implication has a short complete set of rules and is [PSPACE](/pspace/)-complete. Together with [functional dependencies](/functional-dependency/), implication becomes [undecidable](/undecidability/), and a dependency can follow on all finite databases without following on all databases.

## Definition

We use set semantics: a relation is a finite set of tuples. For a tuple $t$ and a list $X = A_1 \ldots A_n$ of attributes, $t[X]$ is the tuple $(t[A_1], \ldots, t[A_n])$.

**Definition (Casanova, Fagin and Papadimitriou 1984).** Let $R$ and $S$ be relation names, which may be equal. Let $X = A_1 \ldots A_n$ be a list of distinct attributes of $R$ and $Y = B_1 \ldots B_n$ a list of distinct attributes of $S$, of the same length $n$. The *inclusion dependency* $R[X] \subseteq S[Y]$ holds in a database $D$ if

$$\pi_X(R^D) \subseteq \pi_Y(S^D),$$

with the columns matched in order: for each $t \in R^D$ there is $s \in S^D$ with $t[A_i] = s[B_i]$ for $i = 1, \ldots, n$. The number $n$ is the *width* of the IND, and the IND is *unary* if $n = 1$. It is *trivial* if $R = S$ and $X = Y$.

**As a first-order sentence.** With one variable per attribute, $R[X] \subseteq S[Y]$ is the [tuple-generating dependency](/tuple-generating-dependency/)

$$\forall \bar x \, \big( R(\bar x) \rightarrow \exists \bar z \; S(\bar w) \big),$$

where $\bar w$ has the variable of $A_i$ at the place of $B_i$, and a new variable of $\bar z$ at each other place. It has one atom on each side, and the variables of $\bar z$ are existential when $S$ has attributes outside $Y$.

**Key-based INDs and foreign keys.** If $Y$ is a key of $S$ (see [candidate key](/candidate-key/)), the IND is *key-based*. A foreign key in SQL, `FOREIGN KEY (X) REFERENCES S (Y)`, is a key-based IND, and *referential integrity* is the property that all foreign keys hold. So a referential integrity constraint is a special case of an IND, not every IND.

**Inference rules (Casanova, Fagin and Papadimitriou 1984).** The following three rules are sound and complete for implication of INDs by INDs.

1. *Reflexivity.* $R[X] \subseteq R[X]$.
2. *Projection and permutation.* From $R[A_1 \ldots A_n] \subseteq S[B_1 \ldots B_n]$ infer $R[A_{i_1} \ldots A_{i_k}] \subseteq S[B_{i_1} \ldots B_{i_k}]$ for any list $i_1, \ldots, i_k$ of distinct indices.
3. *Transitivity.* From $R[X] \subseteq S[Y]$ and $S[Y] \subseteq T[Z]$ infer $R[X] \subseteq T[Z]$.

Deciding whether a set of INDs implies an IND is PSPACE-complete. For INDs alone, implication on finite databases and implication on all databases are the same. A set of unary INDs is a directed graph on the pairs $(R, A)$, and a unary IND follows from it exactly when there is a path, so this case takes linear time.

## Examples and non-examples

- **Foreign key.** In a schema with $\mathit{Orders}(\mathit{oid}, \mathit{cust}, \mathit{date})$ and $\mathit{Customers}(\mathit{id}, \mathit{name})$, the IND $\mathit{Orders}[\mathit{cust}] \subseteq \mathit{Customers}[\mathit{id}]$ says that each order belongs to a known customer. It is key-based, since $\mathit{id}$ is a key.
- **One relation.** In $\mathit{Emp}(\mathit{name}, \mathit{manager})$, the IND $\mathit{Emp}[\mathit{manager}] \subseteq \mathit{Emp}[\mathit{name}]$ says that each manager is an employee.
- **Order of the columns.** $R[AB] \subseteq S[CD]$ and $R[AB] \subseteq S[DC]$ are different INDs. For $R = \{(1, 2)\}$ and $S = \{(1, 2)\}$ the first holds and the second fails.
- **Non-example: a wide IND from narrow ones.** $R[AB] \subseteq S[CD]$ implies $R[A] \subseteq S[C]$ and $R[B] \subseteq S[D]$, by rule 2. The converse fails: $R = \{(1, 2)\}$ and $S = \{(1, 3), (4, 2)\}$ satisfy both unary INDs, but $(1, 2)$ is not in $\pi_{CD}(S)$.
- **Finite and unrestricted implication differ with FDs.** Let $R$ have attributes $A$ and $B$, and let $\Sigma = \{A \to B,\ R[A] \subseteq R[B]\}$. On a finite relation, the FD makes $\pi_B(R)$ the image of a function on $\pi_A(R)$, so $|\pi_B(R)| \le |\pi_A(R)|$, and the IND gives $\pi_A(R) \subseteq \pi_B(R)$. So the two sets are equal, and $\Sigma$ implies $R[B] \subseteq R[A]$ on finite databases. The infinite relation $\{ (i + 1, i) : i \ge 0 \}$ satisfies $\Sigma$, but $0$ is in $\pi_B$ and not in $\pi_A$. So $\Sigma$ does not imply $R[B] \subseteq R[A]$ on all databases.
- **A chase that does not stop.** Repair $R = \{(a, b)\}$ for $R[B] \subseteq R[A]$ with the [chase](/chase-algorithm/): add $(b, z_1)$ with a new value $z_1$, then $(z_1, z_2)$, and so on. Each new tuple needs another one, so the chase never ends. A cyclic set of INDs can cause this, and [weak acyclicity](/weak-acyclicity/) rules it out.

## Related definitions

- **Functional dependencies together with INDs.** Implication of FDs and INDs together is undecidable, as Mitchell (1983) and Chandra and Vardi (1985) showed independently. The example above shows that finite implication is a different problem for this class. Keys with key-based INDs, the common case in practice, are easier: Johnson and Klug decided containment of conjunctive queries under them.
- **Query containment.** Johnson and Klug (1984) decided containment of [conjunctive queries](/conjunctive-query/) under INDs with the chase, and showed that it is PSPACE-complete. This is the basis of query optimization that uses foreign keys, such as removing a join with a table that only checks a foreign key.
- **Tuple-generating dependency.** Each IND is a TGD with one atom on each side. TGDs also cover [multivalued dependencies](/multivalued-dependency/) and [join dependencies](/join-dependency/).
- **Equality-generating dependency.** FDs and keys are [EGDs](/equality-generating-dependency/). A schema with keys and foreign keys has EGDs and INDs, and the [chase](/chase-algorithm/) applies both.
- **Implication problem.** The [dependency implication problem](/dependency-implication-problem/) asks the general question for all these classes.

## References
