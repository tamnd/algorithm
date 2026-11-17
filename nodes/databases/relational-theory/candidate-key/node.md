---
tag: BYCHZG
kind: definition
slug: candidate-key
name: Candidate key
aliases:
- superkey
- minimal key
area: databases/relational-theory
level: intro
summary: A set of attributes that functionally determines every attribute of a relation and has no proper subset that does.
prereqs: [functional-dependency, attribute-closure-algorithm]
see_also: [prime-attribute-np-completeness, dependency-implication-problem, second-normal-form, third-normal-form, boyce-codd-normal-form, inclusion-dependency, entity-relationship-model, relational-model]
sources:
  - paper: doi:10.1145/362384.362685
    title: E. F. Codd, A relational model of data for large shared data banks, Communications of the ACM 13(6), 377 to 387 (1970)
    locator: primary keys of relations
  - paper: "E. F. Codd, Further normalization of the data base relational model, in R. Rustin (ed.), Data Base Systems, Courant Computer Science Symposia 6, Prentice-Hall (1972), 33 to 64"
    locator: candidate keys and prime attributes, used to define second and third normal form
  - paper: doi:10.1016/0022-0000(78)90009-0
    title: Cláudio L. Lucchesi and Sylvia L. Osborn, Candidate keys for relations, Journal of Computer and System Sciences 17(2), 270 to 279 (1978)
    locator: finding one key, listing all keys, and the hardness of the prime attribute and bounded key problems
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Chapter 7 (design theory for relational databases), keys of a relation scheme
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 8 (functional and join dependency) and Chapter 11 (design and dependencies), keys and superkeys
---

A candidate key of a schema is a set of attributes that determines all the other attributes under the [functional dependencies](/functional-dependency/) of the schema, and that is minimal with this property. This page defines keys, superkeys, prime attributes and primary keys, and gives their basic properties. The [attribute closure algorithm](/attribute-closure-algorithm/) tests whether a set is a superkey, the [dependency implication problem](/dependency-implication-problem/) page finds one key and lists all keys, and the [prime attribute](/prime-attribute-np-completeness/) page proves that asking whether an attribute is in some key is NP-complete.

## Definition

Let $U$ be a finite set of attributes and $F$ a finite set of FDs over $U$. For $X \subseteq U$, let $X^+$ be the closure of $X$ under $F$, the set of attributes $B$ with $F \models X \to B$.

- A **superkey** is a set $X \subseteq U$ with $X^+ = U$, that is $F \models X \to U$. In a relation that satisfies $F$, under set semantics, two distinct tuples never agree on a superkey.
- A **candidate key**, or simply a *key*, is a superkey $K$ such that no proper subset of $K$ is a superkey.
- A **prime attribute** is an attribute that belongs to at least one candidate key. The others are **non-prime**.
- A **primary key** is one candidate key that the designer chooses as the main identifier of the tuples. The other candidate keys are *alternate keys*.

Superkeys are closed upward: if $X$ is a superkey and $X \subseteq Y \subseteq U$, then $Y$ is a superkey. So a superkey $K$ is a candidate key exactly when $K - \{B\}$ is not a superkey for each $B \in K$. This gives a test with $|K|$ closures.

**Every schema has a key.** $U$ is a superkey. Go through the attributes of $U$ in any order, and drop each attribute whose removal leaves a superkey. The result $K$ is a superkey. For each $B \in K$, the set from which $B$ was not dropped contains $K$, and removing $B$ from it gave no superkey, so by upward closure $K - \{B\}$ is not a superkey either. So $K$ is a candidate key, found with $|U|$ closures.

**Keys form an antichain.** No candidate key contains another, by minimality. By Sperner's theorem on antichains of subsets, a schema with $a$ attributes has at most $\binom{a}{\lfloor a/2 \rfloor}$ candidate keys, and this bound is reached. With $F = \{X \to U : |X| = \lfloor a/2 \rfloor\}$, each set of $\lfloor a/2 \rfloor$ attributes is a key and no smaller set is a superkey. For $a = 4$ this gives the six keys $AB$, $AC$, $AD$, $BC$, $BD$, $CD$, and for $a = 6$ it gives 20 keys.

**Keys of a schema, not of an instance.** A key is a property of $(U, F)$. One relation can happen to have distinct values in some column without that column being a key, and adding a tuple can then make two tuples agree on it. In SQL, the PRIMARY KEY and UNIQUE constraints declare keys so that the system rejects such tuples.

## Examples and non-examples

- **One key.** $\mathrm{Emp}(E, D, N)$ with employee, department and department name, and $F = \{E \to D,\ D \to N\}$. Here $E^+ = EDN$, so $E$ is a key. $D^+ = DN$, so $D$ is not a superkey. $EN$ is a superkey but not a candidate key, because $E$ alone is one.
- **Two keys of the same size.** $\mathrm{Addr}(C, S, Z)$ with city, street and zip, and $F = \{CS \to Z,\ Z \to C\}$. The keys are $CS$ and $SZ$, so every attribute is prime.
- **Minimal is not minimum.** $U = ABCD$ and $F = \{A \to BCD,\ BC \to A\}$. The keys are $A$ and $BC$. Both are minimal under set inclusion, but they have different sizes. The key with the fewest attributes is a different question, and deciding whether a key of at most $k$ attributes exists is NP-complete.
- **A key with two attributes.** $\mathrm{Grade}(S, C, G, N)$ with student, course, grade and student name, and $F = \{SC \to G,\ S \to N\}$. The only key is $SC$. $S$ is not a key, because $S^+ = SN$.
- **No FDs.** If $F = \emptyset$, then $X^+ = X$ for each $X$, and the only key is $U$. Every attribute is prime.
- **The empty key.** If $F \models \emptyset \to U$, then $\emptyset$ is the only key, and every relation that satisfies $F$ has at most one tuple.
- **Non-example: unique by chance.** In a relation over $\mathrm{Emp}$ in which no two employees share a department, the column $D$ has distinct values, but $D$ is not a key of the schema, because $F$ does not imply $D \to E$.

## Related definitions

- **Superkey.** Every candidate key is a superkey, but a superkey need not be minimal. Some texts use the word loosely for a key. Here a superkey is any set with $X^+ = U$, minimal or not.
- **Prime attribute problem.** Whether a given attribute is prime is NP-complete, and there can be exponentially many keys. See [the prime attribute problem](/prime-attribute-np-completeness/).
- **Normal forms.** [Second normal form](/second-normal-form/) forbids a non-prime attribute that depends on part of a key. [Third normal form](/third-normal-form/) and [BCNF](/boyce-codd-normal-form/) ask that the left side of each nontrivial FD is a superkey, with an exception for prime attributes in 3NF.
- **Foreign keys.** A foreign key is a set of attributes whose values must appear as values of a key of another relation. In dependency theory it is an [inclusion dependency](/inclusion-dependency/) whose right side is a key.
- **Keys in the ER model.** An entity set of the [entity-relationship model](/entity-relationship-model/) has a key, and a weak entity set has a partial key that becomes a key only together with the key of its owner.

## References
