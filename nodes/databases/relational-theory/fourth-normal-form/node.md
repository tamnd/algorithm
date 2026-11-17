---
tag: 9VM6F5
kind: definition
slug: fourth-normal-form
name: Fourth normal form (4NF)
aliases:
- 4NF
area: databases/relational-theory
level: core
summary: A schema in which every nontrivial multivalued dependency has a superkey on its left side, which removes redundancy from independent facts.
prereqs: [multivalued-dependency, boyce-codd-normal-form, heaths-theorem]
see_also: [fifth-normal-form, normalization, bcnf-decomposition, join-dependency, lossless-join-decomposition, candidate-key, chase-algorithm, third-normal-form]
sources:
  - paper: doi:10.1145/320557.320571
    title: Ronald Fagin, Multivalued dependencies and a new normal form for relational databases, ACM Transactions on Database Systems 2(3), 262 to 278 (1977)
    locator: the definition of fourth normal form, the proof that it implies BCNF, and the decomposition into 4NF
  - paper: doi:10.1145/132271.132274
    title: C. J. Date and Ronald Fagin, Simple conditions for guaranteeing higher normal forms in relational databases, ACM Transactions on Database Systems 17(3), 465 to 476 (1992)
    locator: a BCNF schema with at least one key of one attribute is in 4NF
  - paper: doi:10.1145/320613.320614
    title: Catriel Beeri, On the membership problem for functional and multivalued dependencies in relational databases, ACM Transactions on Database Systems 5(3), 241 to 259 (1980)
    locator: the polynomial test for implication of FDs and MVDs, which finds the superkeys under a set of FDs and MVDs
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 11 (design and dependencies), fourth normal form
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Chapter 7 (design theory for relational databases), multivalued dependencies and fourth normal form
---

Fourth normal form is the normal form of Fagin (1977) for schemas with [multivalued dependencies](/multivalued-dependency/) as well as functional ones. It asks what [BCNF](/boyce-codd-normal-form/) asks of FDs, a superkey on the left side, of every nontrivial MVD. The [normalization](/normalization/) page places it in the chain of normal forms, and the BCNF page treats the FD case. This page proves that 4NF implies BCNF, that it is enough to check the given dependencies, and that 4NF and BCNF agree when there are no MVDs.

## Definition

Let $U$ be a finite set of attributes and $D$ a finite set of FDs and MVDs over $U$. We use set semantics. A set $X \subseteq U$ is a *superkey* if $D \models X \to U$. An MVD $X \twoheadrightarrow Y$ is *trivial* if $Y \subseteq X$ or $XY = U$, and then it holds in every relation over $U$.

**Definition (Fagin 1977).** $(U, D)$ is in **fourth normal form** if for each nontrivial MVD $X \twoheadrightarrow Y$ with $D \models X \twoheadrightarrow Y$, the set $X$ is a superkey.

Each FD $X \to Y$ gives the MVD $X \twoheadrightarrow Y$ by replication, so the FDs of $D$ are covered too. With MVDs present, $D$ can imply FDs that no rule for FDs alone gives, through the *coalescence* rule, so superkeys must be found with an implication test for FDs and MVDs together, such as Beeri's dependency basis or the [chase](/chase-algorithm/), not with the attribute closure under the FDs of $D$ only.

**4NF implies BCNF.** Let $(U, D)$ be in 4NF, and let $D \models X \to A$ with $A \notin X$. If $XA = U$, then $X \to U$ follows and $X$ is a superkey. Otherwise $X \twoheadrightarrow A$ is a nontrivial MVD that $D$ implies, by replication, so $X$ is a superkey by 4NF. So each nontrivial implied FD has a superkey on its left side, which is BCNF. $\square$

**It is enough to check $D$.** $(U, D)$ is in 4NF if and only if the left side of each nontrivial MVD of $D$ and of each nontrivial FD of $D$ is a superkey.

*Proof.* *Only if:* each member of $D$ is implied by $D$, and a nontrivial FD $X \to Y$ with $XY \ne U$ gives a nontrivial MVD; if $XY = U$, then $X$ is a superkey anyway. *If:* let $K$ be the set of FDs $X \to U$, one for each left side $X$ of a nontrivial member of $D$. Each of these $X$ is a superkey, so $D \models K$. Each nontrivial member of $D$ follows from its FD $X \to U$, and the trivial ones follow from nothing, so $K \models D$. So $D$ and $K$ imply the same dependencies. Now let $D \models V \twoheadrightarrow W$ be nontrivial, with $Z = U - VW$. Then $K \models V \twoheadrightarrow W$. By Fagin's theorem (see [Heath's theorem](/heaths-theorem/)), this means that the split into $VW$ and $VZ$ is lossless for each relation that satisfies $K$. $K$ holds FDs only, so by the test of the [lossless join](/lossless-join-decomposition/) page, $K \models V \to W$ or $K \models V \to Z$. Both FDs are nontrivial, because $W - V$ and $Z$ are not empty. Every FD of $K$ has a superkey on its left side, so $(U, K)$ is in BCNF, and by the BCNF page, the left side of each nontrivial FD that $K$ implies is a superkey. So $V$ is a superkey. $\square$

**With FDs only, 4NF and BCNF agree.** If $D$ is a set of FDs, then $(U, D)$ is in 4NF exactly when it is in BCNF. One direction is the proposition above. For the other, BCNF means that each nontrivial FD of $D$ has a superkey on its left side, which is the condition of the previous proposition.

**4NF decomposition.** If a schema violates 4NF with $X \twoheadrightarrow Y$, split it into $XY$ and $X(U - XY)$. Fagin's theorem shows that the split is lossless. Repeat on the parts with the MVDs that hold on them. The process stops, since the parts get smaller, and it ends with a lossless 4NF decomposition. Like [BCNF decomposition](/bcnf-decomposition/), it may not preserve the dependencies.

**A sufficient condition (Date and Fagin 1992).** If a schema with FDs and MVDs is in BCNF and has at least one candidate key with a single attribute, then it is in 4NF.

## Examples and non-examples

- **BCNF, not 4NF.** $\mathrm{CTB}(C, T, B)$ with course, teacher and book, and $D = \{C \twoheadrightarrow T\}$: the teachers and the books of a course are independent. No nontrivial FD follows, so the only key is $CTB$ and the schema is in BCNF. $C \twoheadrightarrow T$ is nontrivial and $C$ is not a superkey, so it is not in 4NF. A relation over it stores each teacher of a course once for each book of the course.
- **The 4NF split.** Splitting $\mathrm{CTB}$ on $C \twoheadrightarrow T$ gives $\mathrm{CT}(C, T)$ and $\mathrm{CB}(C, B)$. On each part, $C \twoheadrightarrow T$ and $C \twoheadrightarrow B$ become trivial, and both parts are in 4NF. A course with $p$ teachers and $q$ books needs $p + q$ tuples instead of $pq$.
- **An MVD with a key on the left.** $\mathrm{Emp}(E, N, S)$ with employee, name and salary, and $D = \{E \to NS\}$. $E$ is a key, so every MVD with $E$ on the left is allowed. The schema is in BCNF and has a key with one attribute, so it is in 4NF by the result of Date and Fagin.
- **Not BCNF, so not 4NF.** $\mathrm{Emp}(E, D, N)$ with $F = \{E \to D,\ D \to N\}$ violates BCNF with $D \to N$, and $D \twoheadrightarrow N$ violates 4NF.
- **No dependencies.** With $D = \emptyset$, only trivial MVDs hold and the schema is in 4NF.

## Related definitions

- **BCNF.** [BCNF](/boyce-codd-normal-form/) is the same condition for FDs. 4NF implies BCNF, and the two agree when $D$ has no MVDs.
- **Fifth normal form.** [5NF](/fifth-normal-form/) extends the condition to [join dependencies](/join-dependency/) and implies 4NF. A schema can be in 4NF and not in 5NF.
- **Multivalued dependency.** The [MVD](/multivalued-dependency/) page gives the definition, its forms and the inference rules used above.
- **Lossless split.** [Heath's theorem](/heaths-theorem/), in Fagin's form, is the reason the 4NF split loses nothing.

## References
