---
tag: 61TNHC
kind: definition
slug: functional-dependency
name: Functional dependency
aliases:
- FD
- functional dependencies
area: systems/database-algorithms
level: intro
summary: "A constraint X → Y on a relation: any two tuples that agree on the attributes X must also agree on the attributes Y. Keys are the special case Y = all attributes."
prereqs: [relational-model]
see_also: [armstrongs-axioms, attribute-closure-problem, dependency-implication-problem, normalization, third-normal-form, boyce-codd-normal-form, chase-algorithm, hash-table]
sources:
  - paper: "E. F. Codd, Further normalization of the data base relational model, in R. Rustin (ed.), Data Base Systems, Courant Computer Science Symposia 6, Prentice-Hall (1972), 33 to 64"
    locator: the definition of functional dependence and its use for the second and third normal forms
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Section 8.1 (motivation) and Section 8.2 (functional and key dependencies)
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Section 7.1 (what constitutes a bad database design) and Section 7.2 (functional dependencies)
  - paper: "W. W. Armstrong, Dependency structures of data base relationships, Information Processing 74 (Proceedings of the IFIP Congress 1974), North-Holland, 580 to 583"
    locator: the inference rules for functional dependencies and the relations that satisfy exactly a given set of them
  - paper: doi:10.1093/comjnl/42.2.100
    title: Yka Huhtala, Juha Kärkkäinen, Pasi Porkka and Hannu Toivonen, TANE, An efficient algorithm for discovering functional and approximate dependencies, The Computer Journal 42(2), 100 to 111 (1999)
    locator: the discovery of all minimal functional dependencies that hold in a given relation
---

A functional dependency $X \to Y$ on a relation states that the values of the attributes $X$ fix the values of the attributes $Y$. Any two tuples that agree on $X$ must agree on $Y$. Keys are functional dependencies, and the theory of [normal forms](/normalization/) is built on them. One instance can be checked in linear expected time with a [hash table](/hash-table/) keyed on the $X$-values.

## Definition

Let $U$ be a finite set of attributes and $X, Y \subseteq U$. A *functional dependency* (FD) over $U$ is an expression $X \to Y$. A relation $r$ over $U$ *satisfies* $X \to Y$, written $r \models X \to Y$, if

$$\text{for all } t, u \in r:\quad t[X] = u[X] \implies t[Y] = u[Y].$$

Equivalently, the projection $\pi_{XY}(r)$ is the graph of a function from $X$-values to $Y$-values. Here $XY$ is short for $X \cup Y$, and a single attribute $A$ stands for $\{A\}$.

For a set $F$ of FDs, $r \models F$ if $r$ satisfies each FD of $F$. $F$ *implies* $X \to Y$, written $F \models X \to Y$, if each relation over $U$ that satisfies $F$ also satisfies $X \to Y$.

Some terms:

- $X \to Y$ is *trivial* if $Y \subseteq X$. Each relation satisfies it.
- $X$ is a *superkey* of $r$ if $r \models X \to U$. A *key* is a superkey with no proper subset that is a superkey.
- $X \to Y$ holds if and only if $X \to A$ holds for each $A \in Y$. So it is enough to study FDs with one attribute on the right side.
- $\emptyset \to Y$ says that $Y$ has one value in the whole relation.

**A dependency is a constraint, not a fact about one instance.** A designer declares $F$ as a rule about all legal instances. A given instance can satisfy an FD by chance. So an instance can refute an FD, but it cannot prove that the FD is part of the schema.

### Checking an instance

To test $r \models X \to Y$, read the tuples once. Keep a hash table from each $X$-value to the first $Y$-value seen with it. For each tuple $t$, look up $t[X]$. If it is absent, store $t[Y]$. If it is present with a different $Y$-value, the stored tuple and $t$ are a violating pair. If the scan ends with no conflict, the FD holds. With $n$ tuples, this takes $O(n(|X| + |Y|))$ expected time. The pairwise test from the definition takes $O(n^2(|X| + |Y|))$ time. Sorting $r$ on $X$ gives a deterministic $O(n \log n)$ test: the tuples with equal $X$-values become adjacent.

A database system checks a declared key in the same way, with an index on the key. Each insert looks up its key value before it adds the tuple.

## Examples and non-examples

Take the relation $\mathrm{Sched}(\mathit{Course}, \mathit{Teacher}, \mathit{Hour}, \mathit{Room})$:

| row | Course | Teacher | Hour | Room |
| --- | --- | --- | --- | --- |
| 0 | CS101 | Smith | Mon9 | R1 |
| 1 | CS101 | Smith | Wed9 | R1 |
| 2 | MA201 | Jones | Mon9 | R2 |
| 3 | MA201 | Jones | Tue11 | R1 |
| 4 | PH110 | Smith | Tue11 | R2 |

- $\mathit{Course} \to \mathit{Teacher}$ holds. The hash table maps CS101 to Smith, MA201 to Jones and PH110 to Smith, and no lookup finds a conflict.
- $\mathit{Teacher} \to \mathit{Course}$ fails. Rows 0 and 4 agree on Smith and differ on the course. The scan finds this pair at row 4.
- $\mathit{Course} \to \mathit{Room}$ fails at rows 2 and 3: MA201 meets in R2 and in R1.
- $\mathit{Hour} \to \mathit{Room}$ fails at rows 0 and 2.
- $\mathit{Hour}\,\mathit{Room} \to \mathit{Course}$ holds: no room has two courses at the same hour. This is the kind of rule a school wants as a constraint.
- $\mathit{Course}\,\mathit{Room} \to \mathit{Room}$ is trivial, and holds in every relation.

Of the 32 FDs $X \to A$ with $A \notin X$ over these four attributes, 12 hold in this instance. Only one of them, $\mathit{Course} \to \mathit{Teacher}$, has a left side with fewer than two attributes. Some of the 12, such as $\mathit{Teacher}\,\mathit{Room} \to \mathit{Course}$, hold only by chance: the next term can give Smith a second course in R1.

**Non-example: a value that is not unique.** If two employees can have the same name, $\mathit{Name} \to \mathit{Salary}$ is not a constraint, even if the current instance satisfies it.

**Non-example: a multivalued fact.** In $\mathrm{CTB}(\mathit{Course}, \mathit{Teacher}, \mathit{Book})$, where each course has a set of teachers and a set of books and all pairs occur, neither $\mathit{Course} \to \mathit{Teacher}$ nor $\mathit{Course} \to \mathit{Book}$ holds. The constraint is a *multivalued dependency* $\mathit{Course} \twoheadrightarrow \mathit{Teacher}$, which is the basis of fourth normal form (see [normalization](/normalization/)).

## Related definitions

- **Implication and closure.** $F^+$ is the set of FDs that $F$ implies. For $X \subseteq U$, the *closure* $X^+$ is the largest $Y$ with $F \models X \to Y$. Then $F \models X \to Y$ if and only if $Y \subseteq X^+$. See the [attribute closure problem](/attribute-closure-problem/), the [attribute closure algorithm](/attribute-closure-algorithm/) and the [dependency implication problem](/dependency-implication-problem/).
- **Armstrong's axioms.** Reflexivity, augmentation and transitivity derive exactly the implied FDs. See [Armstrong's axioms](/armstrongs-axioms/).
- **Covers.** Two sets of FDs are *equivalent* if they imply the same FDs. A [minimal cover](/minimal-cover-problem/) is an equivalent set with no redundant FD and no redundant attribute.
- **Normal forms.** [Third normal form](/third-normal-form/) and [Boyce-Codd normal form](/boyce-codd-normal-form/) are conditions on the FDs that hold in a schema. They limit the redundancy that an FD with a small left side causes.
- **Horn clauses.** Read each attribute as a propositional variable. Then $A_1 \cdots A_k \to B$ is the [Horn clause](/horn-clause/) $A_1 \wedge \cdots \wedge A_k \Rightarrow B$, and implication of FDs is implication of these clauses (Sagiv, Delobel, Parker and Fagin 1981).
- **Other dependencies.** Multivalued dependencies, join dependencies and inclusion dependencies (foreign keys) are more general. The [chase](/chase-algorithm/) reasons with all of them.
- **Discovery.** Data profiling tools list the minimal FDs that hold in a given instance. The search space has $|U| \cdot 2^{|U| - 1}$ candidates, and TANE (Huhtala and others 1999) searches it level by level with partitions of the tuples.

## References
