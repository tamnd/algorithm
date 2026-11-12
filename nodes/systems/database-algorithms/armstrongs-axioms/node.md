---
tag: X72AKB
kind: theorem
slug: armstrongs-axioms
name: Armstrong's axioms
aliases:
- Armstrong axioms
- Armstrong's inference rules
area: systems/database-algorithms
level: core
summary: "Reflexivity, augmentation and transitivity derive exactly the functional dependencies that a set of FDs implies: the rules are sound and complete (Armstrong 1974)."
prereqs: [functional-dependency]
see_also: [attribute-closure-problem, attribute-closure-algorithm, dependency-implication-problem, minimal-cover-problem, horn-clause, horn-sat, chase-algorithm]
sources:
  - paper: "W. W. Armstrong, Dependency structures of data base relationships, Information Processing 74 (Proceedings of the IFIP Congress 1974), North-Holland, 580 to 583"
    locator: the axioms for functional dependencies, their completeness, and the relation that satisfies exactly the implied dependencies
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Section 8.2 (functional and key dependencies, the inference rules and their completeness); Section 9.3 (inclusion dependencies with fd's have no finite axiomatization)
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Section 7.3 (reasoning about functional dependencies, Armstrong's axioms and their completeness)
  - paper: doi:10.1145/320064.320066
    title: Catriel Beeri and Philip A. Bernstein, Computational problems related to the design of normal form relational schemas, ACM Transactions on Database Systems 4(1), 30 to 59 (1979)
    locator: the derivation of implied dependencies and the linear membership algorithm
  - paper: "Catriel Beeri, Ronald Fagin and John H. Howard, A complete axiomatization for functional and multivalued dependencies in database relations, Proceedings of the ACM SIGMOD Conference (1977), 47 to 61"
    locator: the extension of the rules to multivalued dependencies
  - paper: "Catriel Beeri, Martin Dowd, Ronald Fagin and Richard Statman, On the structure of Armstrong relations for functional dependencies, Journal of the ACM 31(1), 30 to 46 (1984)"
    locator: the size of the smallest Armstrong relation
  - paper: "Yehoshua Sagiv, Claude Delobel, D. Scott Parker and Ronald Fagin, An equivalence between relational database dependencies and a fragment of propositional logic, Journal of the ACM 28(3), 435 to 453 (1981)"
    locator: functional dependencies as propositional Horn clauses
---

Armstrong's axioms are three inference rules for [functional dependencies](/functional-dependency/): reflexivity, augmentation and transitivity. W. W. Armstrong proved in 1974 that they are sound and complete. Each FD that they derive from a set $F$ holds in every relation that satisfies $F$, and each such FD has a derivation. The completeness proof needs only relations of two tuples, and it shows that implication of FDs reduces to the computation of one [attribute closure](/attribute-closure-problem/).

## Statement

Fix a finite attribute set $U$, and let $X, Y, Z, W \subseteq U$. The rules are:

| rule | premises | conclusion |
| --- | --- | --- |
| reflexivity | none, if $Y \subseteq X$ | $X \to Y$ |
| augmentation | $X \to Y$ | $XZ \to YZ$ |
| transitivity | $X \to Y$ and $Y \to Z$ | $X \to Z$ |

Here $XZ$ is short for $X \cup Z$. A *derivation* of $X \to Y$ from $F$ is a finite list of FDs. Each FD in the list is in $F$, or it follows from earlier FDs of the list by one rule, and the last FD is $X \to Y$. Write $F \vdash X \to Y$ if a derivation exists, and $F \models X \to Y$ if each relation over $U$ that satisfies $F$ satisfies $X \to Y$.

Let $X^+_F = \{ A \in U : F \vdash X \to A \}$.

**Theorem (Armstrong 1974).** For each set $F$ of FDs over $U$ and all $X, Y \subseteq U$:

$$F \vdash X \to Y \iff F \models X \to Y \iff Y \subseteq X^+_F.$$

**Corollary (two tuples suffice).** $F \models X \to Y$ if and only if each relation of at most two tuples that satisfies $F$ satisfies $X \to Y$.

**Derived rules.** These follow from the three rules, so they are sound:

| rule | premises | conclusion |
| --- | --- | --- |
| union | $X \to Y$ and $X \to Z$ | $X \to YZ$ |
| decomposition | $X \to YZ$ | $X \to Y$ |
| pseudotransitivity | $X \to Y$ and $WY \to Z$ | $WX \to Z$ |

## In plain words

Three rules let you reason about "these columns fix those columns". A set of columns fixes each part of itself. If some columns fix others, adding the same extra columns to both sides keeps this true. And if the first set fixes the second and the second fixes a third, the first fixes the third. The theorem says that these three rules are enough. Each consequence of a list of such facts can be found with them, and nothing false can. To show that a fact does not follow, two rows are enough: make them equal on exactly the columns that the given set fixes, and different on all other columns.

## Proof

**Derived rules.** *Union:* augment $X \to Y$ with $X$ to get $X \to XY$. Augment $X \to Z$ with $Y$ to get $XY \to YZ$. Transitivity gives $X \to YZ$. *Decomposition:* reflexivity gives $YZ \to Y$, and transitivity with $X \to YZ$ gives $X \to Y$. *Pseudotransitivity:* augment $X \to Y$ with $W$ to get $WX \to WY$, and use transitivity with $WY \to Z$.

**Soundness.** Each rule preserves truth in every relation $r$. *Reflexivity:* if $Y \subseteq X$ and $t[X] = u[X]$, then $t[Y] = u[Y]$. *Augmentation:* let $r \models X \to Y$ and $t[XZ] = u[XZ]$. Then $t[X] = u[X]$, so $t[Y] = u[Y]$. Also $t[Z] = u[Z]$, so $t[YZ] = u[YZ]$. *Transitivity:* if $t[X] = u[X]$, then $t[Y] = u[Y]$, so $t[Z] = u[Z]$. By induction on the length of a derivation, each derived FD holds in each relation that satisfies $F$. So $F \vdash X \to Y$ gives $F \models X \to Y$.

**From derivations to closures.** If $Y \subseteq X^+_F$, then $F \vdash X \to A$ for each $A \in Y$, and the union rule gives $F \vdash X \to Y$ (for $Y = \emptyset$, use reflexivity). Conversely, if $F \vdash X \to Y$, decomposition gives $F \vdash X \to A$ for each $A \in Y$, so $Y \subseteq X^+_F$. Thus $F \vdash X \to Y$ if and only if $Y \subseteq X^+_F$.

**Completeness.** Suppose $F \nvdash X \to Y$. Then $Y \not\subseteq X^+_F$. Write $C = X^+_F$, and build a relation $r = \{t, u\}$ over $U$ with $t(A) = 0$ for each $A$, $u(A) = 0$ for $A \in C$ and $u(A) = 1$ for $A \notin C$. The two tuples agree exactly on $C$.

*Claim: $r \models F$.* Let $V \to W$ be in $F$. A pair of equal tuples satisfies each FD, so only the pair $t, u$ matters. If $V \not\subseteq C$, then $t[V] \ne u[V]$ and the FD holds. If $V \subseteq C$, then $F \vdash X \to V$ by the union rule, and transitivity with $V \to W$ gives $F \vdash X \to W$. So $W \subseteq C$, and $t[W] = u[W]$.

*Claim: $r \not\models X \to Y$.* Reflexivity gives $X \subseteq C$, so $t[X] = u[X]$. Some $A \in Y$ is not in $C$, so $t(A) \ne u(A)$.

So $F \not\models X \to Y$. With soundness, $F \vdash X \to Y$ if and only if $F \models X \to Y$. $\square$

**Why two tuples suffice.** The corollary follows from the proof: the countermodel has two tuples. There is also a direct reason. If some relation $r$ satisfies $F$ and violates $X \to Y$, then some pair $t, u \in r$ violates it. The relation $\{t, u\}$ is a subset of $r$, and an FD that holds in $r$ holds in each subset of $r$, so $\{t, u\}$ still satisfies $F$. A two-tuple relation satisfies $V \to W$ if and only if $V \not\subseteq S$ or $W \subseteq S$, where $S$ is the *agree set* of its two tuples. So whether it satisfies an FD depends only on $S$, and the $2^{|U|}$ agree sets are all the cases. The completeness proof picks the one agree set $S = X^+_F$ that is enough for every $X \to Y$ with the same left side.

**A test.** The implementation computes, for $|U| = 3$ and $|U| = 4$ and random sets $F$, two sets of pairs $(X, Y)$. The first set is the fixpoint of the three rules applied to all FDs over $U$. The second set is the semantic one: all $(X, Y)$ that hold in each of the $2^{|U|}$ two-tuple relations that satisfy $F$. The two sets are equal in all cases, and both are equal to $\{(X, Y) : Y \subseteq X^+\}$. It also builds an explicit derivation of each implied FD and checks it step by step. For $F = \{A \to B, B \to C\}$ over $ABC$, all three sets have 43 FDs, counting trivial ones and those with an empty side.

## Consequences

- **Membership in linear time.** To decide $F \models X \to Y$, compute $X^+$ and test $Y \subseteq X^+$. The [attribute closure algorithm](/attribute-closure-algorithm/) computes $X^+$ in time linear in the size of $F$ (Beeri and Bernstein 1979). There is no need to list $F^+$, which can have $2^{|U|}$ FDs or more. See the [dependency implication problem](/dependency-implication-problem/).
- **Finite and unrestricted implication agree.** The countermodel is finite. So, for FDs, implication over all relations and over finite relations is the same. This is not true for FDs with inclusion dependencies.
- **Horn logic.** Read $A_1 \cdots A_k \to B$ as the [Horn clause](/horn-clause/) $A_1 \wedge \cdots \wedge A_k \Rightarrow B$. A two-tuple relation with agree set $S$ is the truth assignment "true on $S$". Under this map, an FD holds in the relation if and only if the clause is true under the assignment. So $F \models X \to Y$ if and only if the clauses of $F$ with the facts $X$ imply each $B \in Y$, and the closure algorithm is unit propagation for [Horn-SAT](/horn-sat/) (Sagiv, Delobel, Parker and Fagin 1981).
- **Armstrong relations.** For each $F$ there is a single relation that satisfies exactly the FDs in $F^+$ and no other. Take, for each closed set $S = S^+$ other than $U$, a pair of tuples with agree set $S$, with fresh values for each pair. Such a relation is an *Armstrong relation*. The smallest one can need a number of tuples exponential in $|U|$ (Beeri, Dowd, Fagin and Statman 1984). Designers use small Armstrong relations as sample data to check that they declared the right FDs.
- **Covers and normal forms.** Equivalence of FD sets, [minimal covers](/minimal-cover-problem/), keys and the tests for [third normal form](/third-normal-form/) all use the closure from this theorem.

## Tightness

**Each rule is necessary.** Remove one rule and the other two are not complete:

- Without reflexivity, $\emptyset \vdash A \to A$ fails: augmentation and transitivity need a premise, and $F = \emptyset$ gives none.
- Without augmentation, $\{A \to B\} \vdash AC \to BC$ fails. Each FD $V \to W$ that reflexivity and transitivity derive from $A \to B$ has $W \subseteq V$ or $W \subseteq AB$. The given FD and the trivial FDs have this property, and transitivity keeps it: from $X \to Y$ and $Y \to Z$, either $Z \subseteq AB$, or $Z \subseteq Y$ and then $Z \subseteq X$ or $Z \subseteq AB$. But $BC \not\subseteq AC$ and $BC \not\subseteq AB$.
- Without transitivity, $\{A \to B, B \to C\} \vdash A \to C$ fails. Each FD $V \to W$ that reflexivity and augmentation derive has $W \subseteq V$, or $A \in V$ and $W \subseteq VB$, or $B \in V$ and $W \subseteq VC$. Augmentation by $Z$ keeps this property. But $A \to C$ has none of the three forms.

The implementation confirms all three cases by computing the fixpoint of the remaining two rules.

**The rules do not extend to other dependencies.**

- For multivalued dependencies with FDs, a larger finite set of rules is sound and complete (Beeri, Fagin and Howard 1977).
- For FDs with inclusion dependencies, no finite set of rules of this kind is complete (Abiteboul, Hull and Vianu, Section 9.3), and implication is undecidable (Chandra and Vardi 1985; Mitchell 1983).
- Join dependencies have no complete finite set of rules of this kind either.

**Two tuples are needed.** One-tuple relations satisfy every FD, so they cannot refute any implication. Two tuples is the smallest number that works.

## History

Armstrong presented the rules and the completeness proof at the IFIP Congress of 1974. He also proved that each set of FDs has a relation that satisfies exactly its consequences, now called an Armstrong relation. Codd had used functional dependence in 1971 and 1972 to define the second and third normal forms, but without a formal system for deriving new dependencies. Beeri, Fagin and Howard (1977) extended the rules to multivalued dependencies. Beeri and Bernstein (1979) turned the closure into a linear-time algorithm and used it for normal form design. Sagiv, Delobel, Parker and Fagin (1981) proved that FD implication is equivalent to implication in a fragment of propositional logic. Textbooks often give union, decomposition and pseudotransitivity as further axioms, but they are derived rules.

## References
