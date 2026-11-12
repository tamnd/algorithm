---
tag: W54Y5D
kind: concept
slug: normalization
name: Database normalization
aliases:
- normal forms theory
- schema normalization
- relational normalization
area: systems/database-algorithms
level: intro
summary: "The theory of splitting relation schemas into smaller ones to remove redundancy and update anomalies, with normal forms 1NF, 2NF, 3NF, BCNF and 4NF as goals."
prereqs: [functional-dependency, first-normal-form]
see_also: [third-normal-form, boyce-codd-normal-form, third-normal-form-synthesis, bcnf-decomposition, lossless-join-decomposition, dependency-preserving-decomposition, chase-algorithm, minimal-cover-problem]
sources:
  - paper: "E. F. Codd, Further normalization of the data base relational model, in R. Rustin (ed.), Data Base Systems, Courant Computer Science Symposia 6, Prentice-Hall (1972), 33 to 64"
    locator: the update anomalies, and the second and third normal forms
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Section 11.2 (normal forms) and Section 11.3 (the universal relation assumption)
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Section 7.1 (bad designs and anomalies), Sections 7.4 and 7.5 (lossless and dependency-preserving decompositions), Sections 7.6 to 7.8 (normal forms and decomposition algorithms), Sections 7.9 and 7.10 (multivalued dependencies and fourth normal form)
  - paper: "Ronald Fagin, Multivalued dependencies and a new normal form for relational databases, ACM Transactions on Database Systems 2(3), 262 to 278 (1977)"
    locator: multivalued dependencies and fourth normal form
  - paper: "E. F. Codd, Recent investigations in relational data base systems, Information Processing 74 (Proceedings of the IFIP Congress 1974), North-Holland, 1017 to 1021"
    locator: the normal form now called Boyce-Codd normal form
  - paper: doi:10.1145/320493.320489
    title: Philip A. Bernstein, Synthesizing third normal form relations from functional dependencies, ACM Transactions on Database Systems 1(4), 277 to 298 (1976)
    locator: the synthesis approach to 3NF design
  - paper: "William Kent, A simple guide to five normal forms in relational database theory, Communications of the ACM 26(2), 120 to 125 (1983)"
    locator: an informal account of the normal forms from first to fifth
---

Database normalization is the theory of how to split a relation schema into smaller schemas so that each fact is stored once. A schema that stores a fact many times has *update anomalies*: an update can change one copy and miss the others, and some facts cannot be stored without others. Codd defined the first three normal forms between 1970 and 1972, and later work added Boyce-Codd, fourth and fifth normal forms. Each normal form is a condition on the [dependencies](/functional-dependency/) of a schema, and the algorithms of this area test the conditions and build decompositions that meet them.

## In plain words

A table that mixes two kinds of facts repeats one of them. If a table lists each item a supplier sells with the supplier's address, the address appears once per item. To change the address, you must change many rows. If the supplier sells nothing yet, you cannot store the address at all. If you delete the last item, you lose the address. The cure is to split the table: one table for suppliers and addresses, one for supplier, item and price. Normal forms say when a table needs no more splitting. The split must lose no information, and it should keep each rule checkable inside one table.

## The idea

**Anomalies come from dependencies with small left sides.** Let a schema $R(U)$ have a set $F$ of FDs. If $X \to A$ holds and $X$ is not a superkey, then two tuples can agree on $X$, and then they repeat the same $A$-value. The fact "$X$ determines this $A$" is stored once per tuple with that $X$-value. Normal forms forbid such FDs, with different exceptions.

**The normal forms.** Let $R$ be a schema with its FDs, and call an attribute *prime* if it is in some key.

| form | condition | source |
| --- | --- | --- |
| 1NF | each value is atomic; see [first normal form](/first-normal-form/) | Codd 1970 |
| 2NF | 1NF, and no non-prime attribute depends on a proper subset of a key | Codd 1972 |
| 3NF | for each nontrivial $X \to A$, $X$ is a superkey or $A$ is prime; see [third normal form](/third-normal-form/) | Codd 1972 |
| BCNF | for each nontrivial $X \to A$, $X$ is a superkey; see [Boyce-Codd normal form](/boyce-codd-normal-form/) | Codd 1974 |
| 4NF | for each nontrivial multivalued dependency $X \twoheadrightarrow Y$, $X$ is a superkey | Fagin 1977 |
| 5NF | each join dependency is implied by the keys | Fagin 1979 |

Each form implies the one above it: $\text{5NF} \Rightarrow \text{4NF} \Rightarrow \text{BCNF} \Rightarrow \text{3NF} \Rightarrow \text{2NF} \Rightarrow \text{1NF}$. Zaniolo's elementary key normal form (1982) lies between 3NF and BCNF.

**Decomposition.** A decomposition replaces $R(U)$ by schemas $R_1(U_1), \ldots, R_k(U_k)$ with $U_1 \cup \cdots \cup U_k = U$. An instance $r$ is stored as its projections $\pi_{U_i}(r)$. Two properties matter:

- **Lossless join.** For each legal $r$, the [natural join](/relational-join/) of the projections is $r$ again. Otherwise the join gives extra tuples, and the split loses the information of which tuples were real. A split into two schemas is lossless if and only if $U_1 \cap U_2 \to U_1$ or $U_1 \cap U_2 \to U_2$ is implied. In general, the [chase](/chase-algorithm/) decides it. See [lossless-join decomposition](/lossless-join-decomposition/).
- **Dependency preservation.** The FDs that hold inside the $U_i$ imply all of $F$. Then a system can check each update on one small relation. Otherwise, some FD can be checked only after a join. See [dependency-preserving decomposition](/dependency-preserving-decomposition/).

**The trade-off between 3NF and BCNF.** Every schema has a lossless decomposition into BCNF, built by splitting on a violating FD again and again: the [BCNF decomposition](/bcnf-decomposition/) algorithm. But some schemas have no BCNF decomposition that preserves the dependencies. Every schema has a decomposition into 3NF that is both lossless and dependency preserving, built by [3NF synthesis](/third-normal-form-synthesis/) from a [minimal cover](/minimal-cover-problem/). So the designer chooses between less redundancy (BCNF) and checkable constraints (3NF).

**Two ways to design.** *Decomposition* starts from one universal schema and splits it on violations. *Synthesis* starts from the FDs and builds one schema per group of FDs. Both assume that all attributes have global meanings across the schema, the *universal relation assumption* (Abiteboul, Hull and Vianu, Section 11.3).

**Costs of the tests.** Testing BCNF for a schema with its own FDs takes polynomial time: check that each left side of $F$ is a superkey. Testing 3NF is NP-complete, because it asks whether attributes are prime (Jou and Fischer 1982). Testing whether a subschema of a decomposition is in BCNF under the projected FDs is harder than testing the whole schema, because the projected FDs can be exponentially many (Beeri and Bernstein 1979).

## Examples

**Supplier and items.** Let $\mathrm{Supply}(S, \mathit{Addr}, I, P)$ hold supplier, address, item and price, with $F = \{S \to \mathit{Addr},\ SI \to P\}$. The only key is $SI$.

- $S \to \mathit{Addr}$ violates 2NF: $\mathit{Addr}$ is not prime and depends on $S$, a proper subset of the key.
- The address of a supplier with 100 items is stored 100 times.
- Split into $R_1(S, \mathit{Addr})$ and $R_2(S, I, P)$. The common attribute $S$ is a key of $R_1$, so the split is lossless. Each FD lies inside one schema, so it is dependency preserving. Both schemas are in BCNF.

**A transitive dependency.** $\mathrm{Emp}(E, D, N)$ with employee, department and department name, and $F = \{E \to D,\ D \to N\}$. The key is $E$. $D \to N$ violates 3NF: $D$ is not a superkey and $N$ is not prime. The schema is in 2NF, because the key has one attribute. Split into $(E, D)$ and $(D, N)$.

**3NF but not BCNF.** $\mathrm{Addr}(C, S, Z)$ with city, street and zip, and $F = \{CS \to Z,\ Z \to C\}$. The keys are $CS$ and $SZ$, so all attributes are prime and the schema is in 3NF. $Z \to C$ violates BCNF, because $Z$ is not a superkey. A split on $Z \to C$ gives $(Z, C)$ and $(Z, S)$. It is lossless, but $CS \to Z$ does not hold inside either schema, so it is not dependency preserving. No BCNF decomposition can preserve $CS \to Z$: that needs a schema with $C$, $S$ and $Z$, which is the whole schema, and it is not in BCNF. In the split, two tuples (Z1, Main St) and (Z2, Main St) in $(Z, S)$, with Z1 and Z2 both in the same city, satisfy each part but break $CS \to Z$ after the join.

**A multivalued fact.** $\mathrm{CTB}(C, T, B)$ lists for each course all pairs of its teachers and its books. No nontrivial FD holds, so the schema is in BCNF, but each teacher of a course is stored once per book. The multivalued dependency $C \twoheadrightarrow T$ violates 4NF. Split into $(C, T)$ and $(C, B)$.

## Where it is used

- **Database design.** Normalization is the standard method to design an OLTP schema from an entity-relationship model. Textbooks and design tools apply 3NF or BCNF as the target.
- **Constraint enforcement.** In a normalized schema, most FDs become key constraints, which a database system checks with an index on each insert.
- **Denormalization.** Analytical schemas, such as the star schemas of data warehouses, are deliberately not normalized. They store repeated values to avoid joins at query time, and they are loaded in bulk, so update anomalies matter less.
- **Data cleaning.** Discovered FDs in a dataset point to the columns that could be split out, and violations of declared FDs point to errors.
- **Theory.** The normal forms motivated the theory of dependencies: [Armstrong's axioms](/armstrongs-axioms/), the [implication problem](/dependency-implication-problem/), the chase and the study of acyclic schemas.

## References
