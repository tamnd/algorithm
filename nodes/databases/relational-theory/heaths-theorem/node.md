---
tag: CHJRS4
kind: theorem
slug: heaths-theorem
name: "Heath's theorem"
aliases:
- lossless decomposition by a functional dependency
area: databases/relational-theory
level: core
summary: "If X -> Y holds in a relation over the attributes XYZ, the relation is the join of its projections on XY and XZ. Fagin showed that the exact condition is the MVD X ->> Y."
prereqs: [functional-dependency, relational-algebra]
see_also: [lossless-join-decomposition, multivalued-dependency, lossless-join-test, bcnf-decomposition, fourth-normal-form, join-dependency, normalization, boyce-codd-normal-form]
sources:
  - paper: doi:10.1145/1734714.1734717
    title: Ian J. Heath, Unacceptable file operations in a relational data base, Proceedings of the 1971 ACM SIGFIDET Workshop on Data Description, Access and Control, 19 to 33 (1971)
    locator: a relation that satisfies a functional dependency is the join of two of its projections
  - paper: doi:10.1145/320557.320571
    title: Ronald Fagin, Multivalued dependencies and a new normal form for relational databases, ACM Transactions on Database Systems 2(3), 262 to 278 (1977)
    locator: the definition of multivalued dependencies and the theorem that a relation is the join of its projections on XY and XZ exactly when X ->> Y holds
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 8 (functional and join dependency), multivalued dependencies and lossless joins
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Chapter 7 (design theory for relational databases), lossless-join decompositions and multivalued dependencies
---

Heath's theorem says that a [functional dependency](/functional-dependency/) $X \to Y$ lets you split a relation into its projections on $XY$ and on $X$ with the other attributes, and get it back with a natural join. Fagin (1977) found the exact condition for this, the [multivalued dependency](/multivalued-dependency/) $X \twoheadrightarrow Y$. Both are statements about one relation. The [lossless join](/lossless-join-decomposition/) page is about a schema and a set of FDs, and proves that a split in two parts is lossless under FDs exactly when the common attributes fix one part. The [tableau test](/lossless-join-test/) handles any number of parts.

## Statement

Let $U$ be a finite set of attributes, let $X, Y \subseteq U$, and let $Z = U - XY$, where $XY$ means $X \cup Y$. We use set semantics: a relation $r$ over $U$ is a finite set of tuples, and projection and join remove duplicates. Write $J(r) = \pi_{XY}(r) \bowtie \pi_{XZ}(r)$.

**Theorem (Heath 1971).** If $r$ satisfies $X \to Y$, then $r = J(r)$.

**Theorem (Fagin 1977).** $r = J(r)$ if and only if $r$ satisfies $X \twoheadrightarrow Y$, that is: for any two tuples $u, v \in r$ with $u[X] = v[X]$, there is a tuple $w \in r$ with $w[XY] = u[XY]$ and $w[Z] = v[Z]$.

## In plain words

Suppose each value in some columns fixes the value in some other columns, for example each department has one manager. Then you can cut the table into two narrower tables that share the deciding columns: one with the deciding columns and the fixed columns, one with the deciding columns and everything else. Joining the two narrow tables on the shared columns gives back exactly the rows you started with, no more and no fewer.

Fagin found the precise rule. The split works exactly when, for each value of the shared columns, the two halves combine freely: every left half that goes with that value pairs with every right half that goes with it. A fixed value is one special case of free combination, because there is only one left half to pair.

## Proof

**Lemma.** $r \subseteq J(r)$. A tuple $t$ over $U$ is in $J(r)$ if and only if there are $u, v \in r$ with $u[XY] = t[XY]$ and $v[XZ] = t[XZ]$.

*Proof.* The natural join of $\pi_{XY}(r)$ and $\pi_{XZ}(r)$ is joined on the common attributes $XY \cap XZ = X$, since $Y \cap Z = \emptyset$. A tuple $t$ over $XY \cup XZ = U$ is in it exactly when $t[XY] \in \pi_{XY}(r)$ and $t[XZ] \in \pi_{XZ}(r)$, which is the condition with $u$ and $v$. For $t \in r$, take $u = v = t$. $\square$

**Proof of Heath's theorem.** By the lemma it is enough to show $J(r) \subseteq r$. Let $t \in J(r)$, with $u, v \in r$ as in the lemma. Then $u[X] = t[X] = v[X]$. Since $r$ satisfies $X \to Y$, $v[Y] = u[Y] = t[Y]$. So $v$ agrees with $t$ on $X$, on $Y$ and on $Z$, that is on $U$, and $t = v \in r$. $\square$

**Proof of Fagin's theorem.** *If.* Let $r$ satisfy $X \twoheadrightarrow Y$ and let $t \in J(r)$, with $u, v$ as in the lemma. Then $u[X] = t[X] = v[X]$, so there is $w \in r$ with $w[XY] = u[XY] = t[XY]$ and $w[Z] = v[Z] = t[Z]$. So $w = t$, and $t \in r$. With the lemma, $r = J(r)$.

*Only if.* Let $r = J(r)$, and let $u, v \in r$ with $u[X] = v[X]$. Define $t$ over $U$ by $t[XY] = u[XY]$ and $t[Z] = v[Z]$. This is well defined, because $XY$ and $Z$ are disjoint and cover $U$. Then $t[X] = u[X] = v[X]$, so $t[XZ] = v[XZ]$. By the lemma, $t \in J(r) = r$, and $w = t$ is the tuple that $X \twoheadrightarrow Y$ asks for. $\square$

Heath's theorem also follows from Fagin's: if $X \to Y$ holds and $u[X] = v[X]$, then $w = v$ works, since $v[Y] = u[Y]$.

## Consequences

- **Every FD is an MVD.** If $r$ satisfies $X \to Y$, then by Heath $r = J(r)$, and by Fagin $r$ satisfies $X \twoheadrightarrow Y$. This is the *replication* rule of the axioms for FDs and MVDs.
- **Complementation.** $J(r)$ does not change when $Y$ and $Z$ swap roles, so $X \twoheadrightarrow Y$ holds exactly when $X \twoheadrightarrow Z$ holds. In particular $X \to Z$ is also enough for the split.
- **BCNF decomposition is lossless.** Each step of [BCNF decomposition](/bcnf-decomposition/) splits a schema on a violating FD $X \to A$ into $XA$ and $X(U - A)$. Heath's theorem shows that each step loses nothing, and a lossless split of a part of a lossless split is still lossless.
- **4NF decomposition is lossless.** The [4NF](/fourth-normal-form/) decomposition splits on a violating MVD $X \twoheadrightarrow Y$ into $XY$ and $XZ$. Fagin's theorem is exactly what makes this step lossless.
- **Splits for 2NF and 3NF.** $\mathrm{Emp}(E, D, N)$ with $E \to D$ and $D \to N$ splits on $D \to N$ into $DN$ and $ED$ with no loss, which removes the transitive dependency.
- **The schema version.** Under a set $F$ of FDs only, the split into $XY$ and $XZ$ is lossless for every relation that satisfies $F$ exactly when $F \models X \to Y$ or $F \models X \to Z$. The *if* part is Heath's theorem. The *only if* part needs a two-tuple counterexample and is proved on the [lossless join](/lossless-join-decomposition/) page.

## Tightness

- **The converse of Heath's theorem is false.** Over $U = ABC$ take $X = A$, $Y = B$ and
  $$r = \{(x, y_1, z_1),\ (x, y_1, z_2),\ (x, y_2, z_1),\ (x, y_2, z_2)\}.$$
  Then $\pi_{AB}(r) \bowtie \pi_{AC}(r) = r$, but neither $A \to B$ nor $A \to C$ holds. The MVD $A \twoheadrightarrow B$ holds, as Fagin's theorem says it must.
- **Bag semantics breaks the theorem.** Take the bag $r = \{(x, y, z_1), (x, y, z_2)\}$ over $ABC$, where $A \to B$ holds. As bags, $\pi_{AB}(r)$ holds $(x, y)$ twice, and the bag join with $\pi_{AC}(r)$ gives each of the two tuples twice, four tuples in all. In SQL, the projections must use DISTINCT, or a key must be kept in each part.
- **The common attributes must be the left side.** With $r = \{(x_1, y, z_1), (x_2, y, z_2)\}$ over $ABC$, the FD $A \to B$ holds, but the split into $AB$ and $BC$ joins on $B$ and gives four tuples, two of them spurious. The theorem needs the part that holds $Y$ and the part that holds $Z$ to share exactly $X$.
- **Three or more parts.** The theorem is about two parts. A relation over $SPJ$ can be the join of its projections on $SP$, $PJ$ and $JS$ and satisfy no nontrivial MVD at all, so no split in two parts explains it. The right condition is a [join dependency](/join-dependency/), and under FDs the [tableau test](/lossless-join-test/) decides it.

## History

Heath (1971) proved the FD case in a paper on file operations that are not acceptable in a relational database, at a time when Codd's normal forms were new. Fagin (1977) introduced multivalued dependencies and fourth normal form, and proved that the MVD is the exact condition for a lossless split in two parts. Aho, Beeri and Ullman (1979) and Maier, Mendelzon and Sagiv (1979) then treated splits into many parts with tableaux and the chase.

## References
