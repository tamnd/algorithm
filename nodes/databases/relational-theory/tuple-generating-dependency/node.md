---
tag: 6AV13D
kind: definition
slug: tuple-generating-dependency
name: Tuple-generating dependency
aliases:
- TGD
- embedded implicational dependency
area: databases/relational-theory
level: advanced
summary: A first-order constraint that whenever some tuples are present, tuples with possibly new values must be present too.
prereqs: [conjunctive-query, multivalued-dependency, inclusion-dependency]
see_also: [equality-generating-dependency, chase-algorithm, join-dependency, weak-acyclicity, schema-mapping, data-exchange-problem, datalog, dependency-implication-problem]
sources:
  - paper: doi:10.1145/1634.1636
    title: Catriel Beeri and Moshe Y. Vardi, A proof procedure for data dependencies, Journal of the ACM 31(4), 718 to 741 (1984)
    locator: tuple-generating and equality-generating dependencies, and the chase as a proof procedure for their implication
  - paper: doi:10.1145/322344.322347
    title: Ronald Fagin, Horn clauses and database dependencies, Journal of the ACM 29(4), 952 to 985 (1982)
    locator: embedded implicational dependencies as Horn sentences, which cover tuple-generating and equality-generating dependencies
  - paper: doi:10.1145/800076.802488
    title: Ashok K. Chandra, Harry R. Lewis and Johann A. Makowsky, Embedded implicational dependencies and their inference problem, Proceedings of the 13th Annual ACM Symposium on Theory of Computing (STOC), 342 to 354 (1981)
    locator: the undecidability of implication for embedded implicational dependencies
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 10 (a larger perspective), tuple-generating and equality-generating dependencies and the chase
---

A tuple-generating dependency (TGD) says that whenever some pattern of tuples occurs in a database, another pattern of tuples occurs too, possibly with values that are not in the first pattern. Both patterns are conjunctions of relational atoms, as in a [conjunctive query](/conjunctive-query/). TGDs cover [multivalued dependencies](/multivalued-dependency/), [join dependencies](/join-dependency/) and [inclusion dependencies](/inclusion-dependency/) in one form. Together with [equality-generating dependencies](/equality-generating-dependency/) they make up the embedded implicational dependencies of Fagin (1982), and Beeri and Vardi (1984) gave the [chase](/chase-algorithm/) as a general proof procedure for them. Today TGDs are also the language of [schema mappings](/schema-mapping/) in [data exchange](/data-exchange-problem/) and of rules with existential variables in ontologies.

## Definition

We use set semantics: a relation is a set of tuples. A *conjunction of atoms* is a formula $A_1 \wedge \cdots \wedge A_m$ where each $A_i$ is a relational atom $R(t_1, \ldots, t_r)$ over variables and constants.

**Definition (Beeri and Vardi 1984).** A *tuple-generating dependency* is a first-order sentence

$$\forall \bar x \, \big( \varphi(\bar x) \rightarrow \exists \bar y \; \psi(\bar x, \bar y) \big),$$

where $\varphi$, the *body*, and $\psi$, the *head*, are conjunctions of atoms, $\varphi$ is not empty, and the variables of $\bar y$ do not occur in $\varphi$. In ASCII it is written `phi(x) -> exists y psi(x, y)`. A database $D$ *satisfies* the TGD if every valuation $v$ of $\bar x$ with $v(\varphi) \subseteq D$ extends to a valuation $v'$ of $\bar x \bar y$ with $v'(\psi) \subseteq D$.

- The TGD is *full* if $\bar y$ is empty: no new values are needed.
- It is *embedded* if $\bar y$ is not empty.
- The variables of $\bar x$ that occur in $\psi$ are the *frontier*. Let $\bar f$ be the frontier. Then $D$ satisfies the TGD if and only if $Q_\varphi(D) \subseteq Q_\psi(D)$ for the two conjunctive queries $Q_\varphi(\bar f) \mathbin{:\!-} \varphi$ and $Q_\psi(\bar f) \mathbin{:\!-} \psi$.

A TGD with several atoms in the head that share existential variables, such as $R(x) \rightarrow \exists y \, (S(x, y) \wedge T(y))$, can not be split into TGDs with one atom each, because $y$ must be the same value in both atoms.

**The chase step.** If $v(\varphi) \subseteq D$ and no extension $v'$ maps $\psi$ into $D$, the [chase](/chase-algorithm/) adds the facts $v'(\psi)$, where $v'$ sends each variable of $\bar y$ to a new labeled null. For full TGDs the chase adds only tuples over the values already in $D$, so it stops. For embedded TGDs it may run forever.

## Examples and non-examples

Let $R$ have the attributes $A$, $B$ and $C$.

- **Multivalued dependency.** $A \twoheadrightarrow B$ on $R(A, B, C)$ is the full TGD
  $$\forall a, b, c, b', c' \, \big( R(a, b, c) \wedge R(a, b', c') \rightarrow R(a, b, c') \big).$$
- **Join dependency.** $\bowtie[AB, BC, CA]$ on $R(A, B, C)$ is the full TGD $R(a, b, c') \wedge R(a', b, c) \wedge R(a, b', c) \rightarrow R(a, b, c)$. Each body atom agrees with the head on one component of the join.
- **Inclusion dependency.** For $R(A, B)$ and $S(C, D)$, the IND $R[A] \subseteq S[D]$ is the embedded TGD $R(x, y) \rightarrow \exists z \; S(z, x)$.
- **Transitivity.** $E(x, y) \wedge E(y, z) \rightarrow E(x, z)$ is a full TGD. It is also a [Datalog](/datalog/) rule: a full TGD with one head atom is a Datalog rule, read as a constraint.
- **Source-to-target mapping.** $\mathit{Flight}(x, y) \rightarrow \exists z \, (\mathit{Leg}(x, z) \wedge \mathit{Leg}(z, y))$ says that each flight of the source is two legs in the target, through some stop $z$. TGDs of this form, with the body over the source and the head over the target, are *source-to-target TGDs*.
- **Non-example: functional dependency.** $A \to B$ asks for equal values, not for tuples: $R(a, b, c) \wedge R(a, b', c') \rightarrow b = b'$. It is an [equality-generating dependency](/equality-generating-dependency/). No set of TGDs without constants is equivalent to it: the relation of all 8 tuples over $\{0, 1\}$ satisfies every such TGD, because any head atom can be matched there, but it violates $A \to B$.
- **Non-example: disjunction.** $R(x) \rightarrow S(x) \vee T(x)$ is not a TGD. It is a *disjunctive* TGD, and the chase must branch.
- **Non-example: negation.** $R(x) \wedge \neg S(x) \rightarrow T(x)$ is not a TGD, because the body is not a conjunction of atoms.

## Related definitions

- **Equality-generating dependency.** The other half of the embedded implicational dependencies: the head is an equality $x_i = x_j$. See [equality-generating dependency](/equality-generating-dependency/).
- **Embedded implicational dependency.** Fagin (1982) defined the class of sentences $\forall \bar x \, (\varphi \rightarrow \exists \bar y \, \psi)$ where $\psi$ is a conjunction of atoms or of equalities. It contains both TGDs and EGDs. The name is sometimes used for TGDs alone, but it is the larger class.
- **Implication.** Implication of embedded implicational dependencies is undecidable (Chandra, Lewis and Makowsky 1981). For full TGDs and EGDs the chase stops, so implication is decidable. For embedded TGDs, when the chase of the body of the goal stops, its result decides implication; when the chase does not stop, a finite part of it can still prove that the goal holds. See the [dependency implication problem](/dependency-implication-problem/).
- **Weak acyclicity.** A set of TGDs is weakly acyclic if its dependency graph has no cycle through an edge that creates a new value. Then every chase stops after polynomially many steps in the size of the database. See [weak acyclicity](/weak-acyclicity/).
- **Schema mapping and data exchange.** A [schema mapping](/schema-mapping/) is a set of source-to-target TGDs, often with target TGDs and EGDs. The chase builds a [universal solution](/universal-solution/), and queries are answered by their [certain answers](/certain-answers/).
- **Datalog.** A [Datalog](/datalog/) program is a set of full TGDs with one head atom, read as rules that compute the smallest database that satisfies them.

## References
