---
tag: JGNYFQ
kind: model
slug: relational-model
name: Relational data model
aliases:
- relational model
- relational model of data
area: systems/database-algorithms
level: intro
summary: "Codd's model of data: a database is a finite set of relations, each a finite set of tuples over named attributes, with keys and other integrity constraints."
see_also: [relational-algebra, functional-dependency, first-normal-form, normalization, relational-join, datalog, query-containment-problem, agm-bound]
sources:
  - paper: doi:10.1145/362384.362685
    title: E. F. Codd, A relational model of data for large shared data banks, Communications of the ACM 13(6), 377 to 387 (1970)
    locator: Section 1.2 (data dependencies in present systems), Section 1.3 (a relational view of data, primary and foreign keys), Section 1.4 (normal form), Section 2.1 (operations on relations)
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 3, Sections 3.1 to 3.4 (the structure of the model, named and unnamed perspectives); Section 6.3 (static analysis of the relational calculus); Section 17.1 (complexity of first-order queries); Chapter 20 (complex values)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: Chapter 3 (the relational model, integrity constraints, keys and foreign keys)
  - paper: "E. F. Codd, Relational completeness of data base sublanguages, in R. Rustin (ed.), Data Base Systems, Courant Computer Science Symposia 6, Prentice-Hall (1972), 65 to 98"
    locator: the relational algebra, the relational calculus and the reduction of the calculus to the algebra
  - paper: "Moshe Y. Vardi, The complexity of relational query languages, Proceedings of the 14th ACM Symposium on Theory of Computing (STOC 1982)"
    locator: the data complexity and the expression complexity of first-order queries
  - paper: "Alfred V. Aho and Jeffrey D. Ullman, Universality of data retrieval languages, Proceedings of the 6th ACM Symposium on Principles of Programming Languages (POPL 1979)"
    locator: transitive closure is not expressible in the relational algebra
---

The relational data model, introduced by E. F. Codd in 1970, describes a database as a finite set of *relations*. Each relation is a finite set of tuples, and each tuple gives one value to each attribute of the relation's schema. Users state what data they want with set operations on relations, such as the [relational algebra](/relational-algebra/), and not by following pointers. Keys, [functional dependencies](/functional-dependency/) and foreign keys restrict which sets of tuples are legal.

## The machine

**Domains and attributes.** Fix a set $\mathbf{dom}$ of values (numbers, strings and so on). An *attribute* is a name, and it may carry a domain $\mathrm{dom}(A) \subseteq \mathbf{dom}$.

**Schemas.** A *relation schema* is a name $R$ with a finite set $U$ of attributes, written $R(U)$. A *database schema* is a finite set of relation schemas with distinct names.

**Tuples and relations.** A *tuple* over $U$ is a function $t : U \to \mathbf{dom}$ with $t(A) \in \mathrm{dom}(A)$. For $X \subseteq U$, $t[X]$ is the restriction of $t$ to $X$. A *relation* (or instance) over $U$ is a finite set of tuples over $U$. A *database instance* gives one relation to each relation schema.

This is the *named perspective* of Abiteboul, Hull and Vianu. Codd's 1970 paper used the *unnamed perspective*: a relation of degree $n$ is a subset of $D_1 \times \cdots \times D_n$, and a column is known by its position. The two perspectives are equivalent: fix an order of the attributes, and each named tuple becomes a sequence.

Three properties follow from "a relation is a set of functions":

- The tuples have no order, and a relation holds no tuple twice.
- The attributes have no order. Only their names identify them.
- Each tuple has exactly one value for each attribute. This is [first normal form](/first-normal-form/).

**Keys.** A set $K \subseteq U$ is a *superkey* of an instance $r$ if no two distinct tuples of $r$ agree on $K$. This is the [functional dependency](/functional-dependency/) $K \to U$. A *candidate key* is a superkey with no proper subset that is a superkey. A schema has at least one candidate key, because $U$ itself is a superkey of every instance. The designer picks one candidate key as the *primary key*. A *foreign key* of $R$ is a list of attributes whose values must occur as primary key values of a relation $S$. Codd introduced primary and foreign keys in Section 1.3 of the 1970 paper.

**Constraints.** A schema can carry *integrity constraints*: domain constraints, keys, functional dependencies, foreign keys (inclusion dependencies) and others. An instance is *legal* if it satisfies all of them. Constraints are statements about every legal instance. One instance can satisfy a dependency by chance, so an instance cannot prove that a constraint holds.

**Queries and updates.** A *query* maps each database instance to a relation. The relational algebra, the relational calculus (first-order logic over the relations) and [Datalog](/datalog/) are query languages. An update inserts, deletes or changes tuples, and the result must still be legal.

**Example.** The schema $\mathrm{Teaches}(\mathit{Course}, \mathit{Teacher}, \mathit{Room})$ with the key $\{\mathit{Course}\}$ has the instance

| Course | Teacher | Room |
| --- | --- | --- |
| CS101 | Smith | R1 |
| MA201 | Jones | R2 |
| PH110 | Smith | R2 |

The instance satisfies the key: the three courses are distinct. The tuple $(\text{CS101}, \text{Jones}, \text{R3})$ cannot be added, because it agrees with the first tuple on the key and differs on $\mathit{Teacher}$. The set $\{\mathit{Teacher}\}$ is not a superkey of this instance, because Smith occurs twice. The set $\{\mathit{Teacher}, \mathit{Room}\}$ is a superkey of this instance, but it is not a key of the schema unless the designer declares it.

## What it counts

The model fixes the data, not the cost. Each kind of algorithm on this site uses its own measure, and each page says which one it uses.

- **Query evaluation in a database system.** Relations are stored in pages of $B$ bytes on disk. A relation of $N$ tuples fills about $N / (\text{tuples per page})$ pages. The cost of a plan is the number of page reads and writes, with $M$ pages of buffer memory. The [join](/relational-join/) pages and the query optimization pages use this measure.
- **In-memory algorithms.** The cost is the number of tuples read, compared or hashed, as a function of the relation sizes $N$ and $M$ in tuples and of the output size.
- **Query languages.** *Data complexity* fixes the query and measures the time or space as a function of the size of the database. *Combined complexity* lets the query vary too. Vardi (1982) introduced these measures.
- **Schema design.** The input is the attribute set $U$ and a set $F$ of dependencies. The size is $|U|$ plus $\|F\|$, the number of attribute occurrences in $F$. The pages on [attribute closure](/attribute-closure-algorithm/), [keys](/dependency-implication-problem/) and [normal forms](/normalization/) use this measure.

## Relation to other models

- **Hierarchical and network models.** IMS stored records in trees, and CODASYL systems stored them in graphs of owner and member records. A program followed the links one record at a time. Codd's paper argued that such programs depend on the order of records, on indexes and on access paths (Section 1.2), and that these dependencies break programs when the storage changes. Relations hide all three, so programs depend only on the data.
- **SQL.** SQL tables are *bags*: a table can hold the same row twice unless a key or DISTINCT forbids it. SQL also has NULL with a three-valued logic, and ordered output. The theory of this site is for sets without NULL, unless a page says otherwise.
- **First-order logic.** A database instance is a finite relational structure, and a relational calculus query is a first-order formula evaluated in it. This connects databases to finite model theory.
- **Nested relations and complex values.** These models allow a value to be a set or a tuple, so they drop first normal form. Abiteboul, Hull and Vianu treat them in Chapter 20.
- **Datalog.** [Datalog](/datalog/) adds recursion. It can express the [transitive closure](/transitive-closure/) of a relation, which the relational algebra cannot.

## Known results in the model

- **Codd's theorem.** The relational algebra and the domain-independent (safe) relational calculus express the same queries (Codd 1972). See [relational algebra](/relational-algebra/).
- **Evaluation.** For a fixed relational algebra query, evaluation takes time polynomial in the size of the database, and in fact logarithmic space. When the query is part of the input, evaluation is PSPACE-complete (Vardi 1982; Abiteboul, Hull and Vianu, Section 17.1).
- **Limits of expressive power.** The transitive closure of a binary relation is not expressible in the relational algebra (Aho and Ullman 1979).
- **Static analysis.** Satisfiability and equivalence of relational calculus queries are undecidable (Abiteboul, Hull and Vianu, Section 6.3). For conjunctive queries, containment is NP-complete: see the [query containment problem](/query-containment-problem/) and the [Chandra-Merlin theorem](/chandra-merlin-theorem/).
- **Dependencies.** Implication of functional dependencies takes linear time with the [attribute closure algorithm](/attribute-closure-algorithm/), and [Armstrong's axioms](/armstrongs-axioms/) are sound and complete for it. Finding a key of at most $k$ attributes is NP-complete (see the [dependency implication problem](/dependency-implication-problem/)).
- **Joins.** The output of a natural join of several relations can be much larger than each input. The [AGM bound](/agm-bound/) gives the tight worst-case size, and the [Yannakakis algorithm](/yannakakis-algorithm/) evaluates a full acyclic join in time linear in the size of the input plus the size of the output.

## References
