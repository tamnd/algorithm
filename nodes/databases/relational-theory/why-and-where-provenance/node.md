---
tag: XWZGP9
kind: definition
slug: why-and-where-provenance
name: Why-provenance and where-provenance
aliases:
- why-provenance
- where-provenance
- witness basis
area: databases/relational-theory
level: advanced
summary: "The sets of input tuples that witness an output tuple, and the input locations from which each output value was copied."
prereqs: [relational-algebra]
see_also: [provenance-semirings, probabilistic-database, conjunctive-query, relational-calculus, incremental-view-maintenance, materialized-view, datalog, sql-null-semantics]
sources:
  - paper: doi:10.1007/3-540-44503-X_20
    title: Peter Buneman, Sanjeev Khanna and Wang-Chiew Tan, Why and where, a characterization of data provenance, Proceedings of the 8th International Conference on Database Theory (ICDT), LNCS 1973, 316 to 330 (2001)
    locator: the definitions of witnesses, the witness basis and the minimal witness basis (why-provenance) and of where-provenance; the minimal witness basis is invariant under query equivalence and where-provenance is not
  - paper: doi:10.1145/357775.357777
    title: Yingwei Cui, Jennifer Widom and Janet L. Wiener, Tracing the lineage of view data in a warehousing environment, ACM Transactions on Database Systems 25(2), 179 to 227 (2000)
    locator: the lineage of a view tuple, the source tuples that contribute to it, for select-project-join views with aggregation and set operations
  - paper: doi:10.1145/1265530.1265535
    title: Todd J. Green, Grigoris Karvounarakis and Val Tannen, Provenance semirings, Proceedings of the 26th ACM Symposium on Principles of Database Systems (PODS), 31 to 40 (2007)
    locator: why-provenance, lineage and the minimal witness basis as semirings of annotations, and their relation to provenance polynomials
  - paper: doi:10.1561/1900000006
    title: James Cheney, Laura Chiticariu and Wang-Chiew Tan, Provenance in databases, why, how, and where, Foundations and Trends in Databases 1(4), 379 to 474 (2009)
    locator: survey of lineage, why-provenance, how-provenance and where-provenance, with their definitions for the positive relational algebra
---

Why-provenance and where-provenance are two ways to explain an answer of a query by the input data. The why-provenance of an output tuple is a set of *witnesses*: sets of input tuples that are enough to produce it, one for each way the query derives it. The where-provenance of a value in an output tuple is the set of input *locations*, a relation, a tuple and an attribute, from which the query copied that value. Buneman, Khanna and Tan defined both in 2001, and showed that the minimal witnesses depend only on the meaning of the query, while where-provenance depends on how the query is written.

## Definition

The setting is the positive relational algebra (selection, projection, natural join, union and renaming) under set semantics, as on the [relational algebra](/relational-algebra/) page. Each input tuple has an identifier, written $r_1, r_2, \ldots$, so that a set of tuples is a set of identifiers. $I$ is the input instance and $Q$ a query; all queries here are monotone, so $J \subseteq I$ implies $Q(J) \subseteq Q(I)$.

**Witnesses.** For $t \in Q(I)$, a *witness* for $t$ is a set $J \subseteq I$ with $t \in Q(J)$. The set of all witnesses is upward closed: a superset of a witness, inside $I$, is a witness. A witness is *minimal* if no proper subset is a witness.

**Witness basis (why-provenance).** The witness basis $\mathrm{Why}(Q, I, t)$ is a set of witnesses defined by induction on the expression $Q$, one witness for each derivation of $t$:

- $\mathrm{Why}(R, I, t) = \{\{t\}\}$ for $t \in I(R)$;
- $\mathrm{Why}(\sigma_{\theta}(E), I, t) = \mathrm{Why}(E, I, t)$;
- $\mathrm{Why}(\pi_{X}(E), I, t) = \bigcup \{\, \mathrm{Why}(E, I, s) \mid s \in E(I),\ s[X] = t \,\}$;
- $\mathrm{Why}(E_1 \bowtie E_2, I, t) = \{\, J_1 \cup J_2 \mid J_i \in \mathrm{Why}(E_i, I, t_i) \,\}$, where $t_1$ and $t_2$ are the two parts of $t$;
- $\mathrm{Why}(E_1 \cup E_2, I, t) = \mathrm{Why}(E_1, I, t) \cup \mathrm{Why}(E_2, I, t)$, where a part is empty when $t$ is not in that side.

Each member of the witness basis is a witness, by induction on $Q$. The *minimal witness basis* $\mathrm{MWhy}(Q, I, t)$ is the set of minimal members of $\mathrm{Why}(Q, I, t)$.

**Where-provenance.** A *location* is a triple $(R, s, A)$: relation $R$, tuple $s \in I(R)$ and attribute $A$. For an output tuple $t$ and an attribute $A$ of $Q$, the where-provenance $\mathrm{Where}(Q, I, t, A)$ is a set of locations, by induction:

- $\mathrm{Where}(R, I, t, A) = \{(R, t, A)\}$;
- selection keeps the where-provenance of its input;
- projection takes the union over the input tuples $s$ with $s[X] = t$;
- a natural join copies the value of a join attribute from both sides, so for a shared attribute $A$ it takes the union of the two sides, and for any other attribute it takes the side that has $A$;
- union takes the union of the two sides;
- a value that the query writes as a constant, such as $5$ in $\{(x, 5) \mid R(x, 5)\}$, has empty where-provenance.

The why-provenance is about tuples, and the where-provenance is about single values in them.

**Two facts** (Buneman, Khanna and Tan 2001).

1. *The minimal witness basis is the set of minimal witnesses.* Every witness contains a member of the witness basis: if $t \in Q(J)$, some derivation of $t$ uses only tuples of $J$, and the member of $\mathrm{Why}(Q, I, t)$ that it gives is a subset of $J$. So the minimal members of $\mathrm{Why}$ are exactly the minimal witnesses, and equivalent queries have the same minimal witness basis, since they have the same witnesses.
2. *Where-provenance is not invariant.* Two equivalent queries can give different where-provenance, as the second example below shows.

From fact 1 and monotonicity: for every set $D \subseteq I$ of deleted tuples, $t \in Q(I \setminus D)$ if and only if some minimal witness of $t$ is disjoint from $D$. So the minimal witness basis answers every question of the form "does $t$ survive the deletion of $D$?".

## Examples and non-examples

Take $R(\mathit{emp}, \mathit{dept})$ with $r_1 = (\mathit{ann}, \mathit{db})$, $r_2 = (\mathit{bob}, \mathit{db})$, $r_3 = (\mathit{cal}, \mathit{os})$, and $S(\mathit{dept}, \mathit{floor})$ with $s_1 = (\mathit{db}, 2)$, $s_2 = (\mathit{os}, 3)$, $s_3 = (\mathit{db}, 4)$. Let $Q = \pi_{\mathit{floor}}(R \bowtie S)$, the floors on which someone works. Then $Q(I) = \{(2), (3), (4)\}$.

- **Why-provenance.** The output $(2)$ has two derivations, through $r_1 \bowtie s_1$ and $r_2 \bowtie s_1$, so $\mathrm{Why}(Q, I, (2)) = \{\{r_1, s_1\}, \{r_2, s_1\}\}$; both are minimal. Similarly $\mathrm{Why}(Q, I, (4)) = \{\{r_1, s_3\}, \{r_2, s_3\}\}$ and $\mathrm{Why}(Q, I, (3)) = \{\{r_3, s_2\}\}$. Check by deletion: removing $r_1$ keeps all three answers, since $\{r_2, s_1\}$ and $\{r_2, s_3\}$ survive. Removing $s_1$ removes $(2)$ only, since $s_1$ is in both witnesses of $(2)$. Removing $r_1$ and $r_2$ leaves only $(3)$.
- **Where-provenance.** $\mathrm{Where}(Q, I, (2), \mathit{floor}) = \{(S, s_1, \mathit{floor})\}$: the value 2 was copied from $s_1$ only, although $r_1$ and $r_2$ are needed to produce it. For $Q' = \pi_{\mathit{dept}}(R \bowtie S)$, the value $\mathit{db}$ comes from both sides of the join, and $\mathrm{Where}(Q', I, (\mathit{db}), \mathit{dept})$ is the four locations $(R, r_1, \mathit{dept})$, $(R, r_2, \mathit{dept})$, $(S, s_1, \mathit{dept})$, $(S, s_3, \mathit{dept})$.
- **Equivalent queries, same minimal witnesses.** Let $Q_1 = R$ and $Q_2 = R \cup \pi_{\mathit{emp}, \mathit{dept}}(R \bowtie S)$. They are equivalent under set semantics, since the second part is contained in $R$. For the output $r_1$, $\mathrm{Why}(Q_1) = \{\{r_1\}\}$, while $\mathrm{Why}(Q_2) = \{\{r_1\}, \{r_1, s_1\}, \{r_1, s_3\}\}$. The witness bases differ, but the minimal witness basis is $\{\{r_1\}\}$ for both.
- **Non-example: where-provenance of equivalent queries.** On a relation $T(A, B)$ with the tuple $u = (a, 5)$, the queries $\sigma_{B = 5}(T)$ and $\{(x, 5) \mid T(x, 5)\}$ are equivalent. For the output $(a, 5)$ and attribute $B$, the first gives $\{(T, u, B)\}$, because selection copies the value, and the second gives $\emptyset$, because the value is a constant of the query.
- **Non-example: queries with difference.** For $Q = R - S$, the output depends on the absence of tuples, so a set of present tuples is not enough to explain it, and the witness definitions above do not apply. Removing a tuple can add an output. Provenance for queries with negation needs other models.

## Related definitions

- **Lineage.** Cui, Widom and Wiener (2000) defined the *lineage* of a view tuple as the source tuples that contribute to it, for select-project-join views with aggregation and set operations. For a positive query, the lineage of $t$ is the union of the members of its witness basis: $\{r_1, r_2, s_1\}$ for the output $(2)$ above. Lineage loses the information of which tuples work together.
- **Provenance semirings.** Green, Karvounarakis and Tannen (2007) showed that lineage, why-provenance and the minimal witness basis are each the annotations of a commutative semiring, and that each is a homomorphic image of the provenance polynomials $\mathbb{N}[X]$; see [provenance semirings](/provenance-semirings/). For the example, the provenance polynomial of $(2)$ is $r_1 s_1 + r_2 s_1$; forgetting the coefficients and exponents gives the why-provenance. Where-provenance is about locations, not about tuples, and is not a semiring annotation of this kind.
- **Probabilistic databases.** The probability of an output tuple on a [probabilistic database](/probabilistic-database/) with independent tuples is the probability that some minimal witness is fully present, so it depends only on the minimal witness basis and the tuple probabilities.
- **Deletion propagation and view maintenance.** The deletion criterion above is the basis of propagating deletions to a [materialized view](/materialized-view/); [incremental view maintenance](/incremental-view-maintenance/) keeps the counts of derivations for the same purpose.
- **Recursive queries.** For [Datalog](/datalog/), a tuple can have infinitely many derivations, but it has only finitely many witnesses, since each is a subset of the finite instance. The minimal witnesses are defined as before and still answer the deletion question.

## References
