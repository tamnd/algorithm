---
tag: 8MCYKZ
kind: definition
slug: second-normal-form
name: Second normal form (2NF)
aliases:
- 2NF
area: databases/relational-theory
level: intro
summary: A relation in first normal form in which no non-prime attribute depends on a proper subset of a candidate key.
prereqs: [candidate-key, first-normal-form, functional-dependency]
see_also: [third-normal-form, normalization, boyce-codd-normal-form, heaths-theorem, prime-attribute-np-completeness, attribute-closure-algorithm, lossless-join-decomposition]
sources:
  - paper: "E. F. Codd, Further normalization of the data base relational model, in R. Rustin (ed.), Data Base Systems, Courant Computer Science Symposia 6, Prentice-Hall (1972), 33 to 64"
    locator: full functional dependence on a key and the definitions of second and third normal form
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Section 7.6 (normal forms for relation schemes, 2NF, 3NF and BCNF)
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 11 (design and dependencies), normal forms based on functional dependencies
---

Second normal form is the first of Codd's normal forms that uses [functional dependencies](/functional-dependency/). It forbids a non-prime attribute that depends on only a part of a [candidate key](/candidate-key/). The [normalization](/normalization/) page compares all the normal forms, and the [third normal form](/third-normal-form/) page treats the stronger condition that is used in practice. This page gives the exact definition of 2NF, a test for it, and the examples that separate it from 1NF and 3NF.

## Definition

Let $U$ be a finite set of attributes and $F$ a finite set of FDs over $U$. Keys, prime attributes and closures $X^+$ are taken with respect to $F$, as on the [candidate key](/candidate-key/) page.

- An attribute $A$ is **fully dependent** on a set $X$ if $F \models X \to A$ and $F \not\models X' \to A$ for each proper subset $X' \subsetneq X$. If $F \models X \to A$ but $A$ is not fully dependent on $X$, the dependence is **partial**.
- **Definition (Codd 1972).** A schema $(U, F)$ in [first normal form](/first-normal-form/) is in **second normal form** if each non-prime attribute is fully dependent on each candidate key. Equivalently, there is no candidate key $K$, proper subset $X \subsetneq K$ and non-prime attribute $A$ with $F \models X \to A$.

**A test.** The schema is in 2NF if and only if, for each candidate key $K$ and each $B \in K$, the closure $(K - \{B\})^+$ contains no non-prime attribute. *Proof.* If $X \subsetneq K$ and $F \models X \to A$ with $A$ non-prime, pick $B \in K - X$. Then $X \subseteq K - \{B\}$, so $A \in X^+ \subseteq (K - \{B\})^+$. The other direction is the case $X = K - \{B\}$. $\square$ The test needs all keys, so it can take time exponential in $|U|$ when there are many keys, and finding the prime attributes is NP-hard in general (see [the prime attribute problem](/prime-attribute-np-completeness/)).

**3NF implies 2NF.** Use Zaniolo's form of 3NF: for each FD $X \to A$ implied by $F$ with $A \notin X$, either $X$ is a superkey or $A$ is prime. Suppose $(U, F)$ is not in 2NF, with a key $K$, a set $X \subsetneq K$ and a non-prime $A$ with $F \models X \to A$. Then $A \notin X$, because $X \subseteq K$ and $A$ is in no key. $X$ is not a superkey, because it is a proper subset of the key $K$. So $X \to A$ violates 3NF. $\square$

**Edge cases.** If every key has one attribute, the only proper subset of a key is $\emptyset$, so the schema is in 2NF unless $F \models \emptyset \to A$ for a non-prime $A$. If every attribute is prime, the schema is in 2NF, since there is no non-prime attribute to test.

## Examples and non-examples

- **Not in 2NF: a partial dependency.** $\mathrm{Grade}(S, C, G, N)$ with student, course, grade and student name, and $F = \{SC \to G,\ S \to N\}$. The only key is $SC$, and $N$ is non-prime. $S \to N$ makes $N$ depend on part of the key, so the schema is in 1NF and not in 2NF. A student's name is stored once for each course the student takes. Splitting on $S \to N$ into $SN$ and $SCG$ is lossless by [Heath's theorem](/heaths-theorem/), and both parts are in 2NF.
- **In 2NF, not in 3NF.** $\mathrm{Emp}(E, D, N)$ with employee, department and department name, and $F = \{E \to D,\ D \to N\}$. The only key is $E$, a single attribute, so the schema is in 2NF. $D \to N$ is a transitive dependency on the key, so it is not in 3NF.
- **Not in 2NF, although the primary key has one attribute.** $\mathrm{Section}(C, T, S, D)$ with course, teacher, section and department, and $F = \{S \to CT,\ CT \to S,\ C \to D\}$: each section has one course and one teacher, each course and teacher pair has one section, and each course belongs to one department. The keys are $S$ and $CT$, since $S^+ = CT^+ = CTSD$ while $C^+ = CD$ and $T^+ = T$. So $D$ is the only non-prime attribute. $C \to D$ makes $D$ depend on the part $C$ of the key $CT$, so the schema is not in 2NF. A check that looks only at the primary key $S$ finds nothing to test and misses this.
- **All attributes prime.** $\mathrm{Addr}(C, S, Z)$ with $F = \{CS \to Z,\ Z \to C\}$ has the keys $CS$ and $SZ$. Every attribute is prime, so it is in 2NF, and in fact in 3NF, but not in BCNF.
- **No FDs.** If $F = \emptyset$, the only key is $U$ and every attribute is prime, so the schema is in 2NF, and also in BCNF.

## Related definitions

- **First normal form.** 2NF assumes [1NF](/first-normal-form/), atomic values in each column. Each 2NF schema is in 1NF by definition, and $\mathrm{Grade}$ shows that the converse is false.
- **Third normal form.** [3NF](/third-normal-form/) also forbids a non-prime attribute that depends on a key through a non-key set, as in $\mathrm{Emp}$. It implies 2NF, as shown above, and has a lossless, dependency-preserving synthesis algorithm, which makes 2NF of mostly historical interest.
- **BCNF.** [BCNF](/boyce-codd-normal-form/) drops the exception for prime attributes. It implies 3NF and so 2NF.
- **Partial dependency.** The FD $X \to A$ with $X$ a proper subset of a key and $A$ non-prime is the pattern that 2NF forbids. Splitting it off into $XA$ is always lossless, by Heath's theorem, and keeps the FD.

## References
