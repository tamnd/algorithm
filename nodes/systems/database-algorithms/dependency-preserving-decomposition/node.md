---
tag: HRYHGM
kind: definition
slug: dependency-preserving-decomposition
name: Dependency-preserving decomposition
aliases:
- dependency preservation
- FD-preserving decomposition
area: systems/database-algorithms
level: core
summary: "A decomposition preserves the dependencies F when the dependencies that hold inside the parts imply all of F. A polynomial test computes closures without building the projections."
prereqs: [functional-dependency, attribute-closure-algorithm, armstrongs-axioms]
see_also: [lossless-join-decomposition, bcnf-decomposition, third-normal-form-synthesis, boyce-codd-normal-form, minimal-cover-problem, dependency-implication-problem, normalization]
sources:
  - paper: doi:10.1137/0210048
    title: Catriel Beeri and Peter Honeyman, Preserving functional dependencies, SIAM Journal on Computing 10(3), 647 to 656 (1981)
    locator: the polynomial-time test of dependency preservation
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Chapter 7 (design theory for relational databases), decompositions that preserve dependencies, with the closure test that does not build the projections
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson (2009)
    locator: Section 3.4 (dependency preservation) and Section 3.2 (projecting functional dependencies)
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 11 (design and dependencies)
---

A decomposition of a relation schema is dependency preserving when the [functional dependencies](/functional-dependency/) that hold inside the single parts together imply all the given dependencies. Then each part can check its own dependencies on an update, and no join is needed to find a violation. Dependency preservation and the [lossless join](/lossless-join-decomposition/) are independent goals of schema design: [BCNF decomposition](/bcnf-decomposition/) always gives a lossless join but can lose dependencies, while [3NF synthesis](/third-normal-form-synthesis/) gives both. A polynomial test (Beeri and Honeyman 1981) avoids the projected dependency sets, which can be exponentially large.

## Definition

Let $R$ be a finite set of attributes, $F$ a set of functional dependencies over $R$, and $\rho = (R_1, \ldots, R_k)$ subsets of $R$ with union $R$. $X^+$ is the closure of $X$ under $F$. The *projection* of $F$ onto $R_i$ is

$$\pi_{R_i}(F) = \{\, X \to Y \;:\; X \cup Y \subseteq R_i,\ F \models X \to Y \,\}.$$

**Definition.** $\rho$ *preserves* $F$ when $G = \pi_{R_1}(F) \cup \cdots \cup \pi_{R_k}(F)$ implies every dependency of $F$:

$$\forall (X \to Y) \in F:\quad G \models X \to Y .$$

Since each dependency of $G$ follows from $F$, this is the same as $G^+ = F^+$.

**Why it matters.** Let $r_1, \ldots, r_k$ be relations over the parts, each satisfying its own $\pi_{R_i}(F)$, and let $r = r_1 \bowtie \cdots \bowtie r_k$. The projection of $r$ on $R_i$ is a subset of $r_i$, so $r$ satisfies $G$. If $\rho$ preserves $F$, then $r$ satisfies $F$. So local checks on the parts are enough. If $\rho$ does not preserve $F$, the parts can each be legal while the join violates $F$.

### The polynomial test

Do not build $G$. For each $X \to Y$ in $F$, compute the closure of $X$ under $G$ with this loop, and check $Y \subseteq Z$:

$$Z \leftarrow X; \quad \text{repeat } Z \leftarrow Z \cup \big( (Z \cap R_i)^+ \cap R_i \big) \text{ for } i = 1, \ldots, k, \text{ until } Z \text{ does not change}.$$

**Claim.** The loop ends with $Z = X^+_G$, the closure of $X$ under $G$.

*Proof.* ($Z \subseteq X^+_G$.) At the start $Z = X$. Assume $Z \subseteq X^+_G$, and let $A \in (Z \cap R_i)^+ \cap R_i$. Then $(Z \cap R_i) \to A$ is a dependency of $F^+$ inside $R_i$, so it is in $\pi_{R_i}(F) \subseteq G$. Its left side is in $X^+_G$, so $A \in X^+_G$. ($Z \supseteq X^+_G$.) At the end $Z$ is closed under $G$: let $V \to W$ be in $\pi_{R_i}(F)$ with $V \subseteq Z$. Then $V \subseteq Z \cap R_i$, so $W \subseteq (Z \cap R_i)^+ \cap R_i \subseteq Z$, because $Z$ is stable. A set that contains $X$ and is closed under $G$ contains $X^+_G$. $\square$

**Cost.** Each round that changes $Z$ adds at least one attribute, so there are at most $n = |R|$ rounds that change $Z$, plus one that does not. Each round does $k$ closures under $F$, each $O(m)$ with the linear-time closure algorithm, where $m$ is the size of $F$. So one dependency costs $O(nkm)$, and the full test costs $O(|F|\, n k m)$, which is polynomial.

**The brute force is exponential.** To build $\pi_{R_i}(F)$, one takes each $X \subseteq R_i$ and adds $X \to (X^+ \cap R_i) \setminus X$. This costs $2^{|R_i|}$ closures, and no method can avoid a large output in general: for $F = \{A_j \to C_j,\ B_j \to C_j : 1 \le j \le n\} \cup \{C_1 \cdots C_n \to D\}$, the projection onto $\{A_1, B_1, \ldots, A_n, B_n, D\}$ has $2^n$ dependencies with minimal left sides for $D$, one for each choice of $A_j$ or $B_j$ for each $j$ (2, 4, 8 and 16 for $n = 1$ to 4). No other nontrivial dependency holds among these attributes, so every set of dependencies equivalent to the projection must have a dependency with each of these $2^n$ left sides.

## Examples and non-examples

**Example: a dependency that lies in no part.** $R = ABC$, $F = \{A \to B,\ B \to C,\ C \to A\}$, $\rho = (AB, BC)$. The dependency $C \to A$ is inside no part. But $\pi_{AB}(F) \ni B \to A$ and $\pi_{BC}(F) \ni C \to B$. The loop for $C \to A$ runs: $Z = C$; part $AB$ adds nothing; part $BC$ gives $(C)^+ \cap BC = BC$, so $Z = BC$; part $AB$ gives $(B)^+ \cap AB = AB$, so $Z = ABC$. So $A \in Z$, and $\rho$ preserves $F$. A test that only looks for each dependency of $F$ inside some part gives the wrong answer here.

**Non-example: street, city, zip.** $F = \{\mathit{street}\,\mathit{city} \to \mathit{zip},\ \mathit{zip} \to \mathit{city}\}$ and the [BCNF](/boyce-codd-normal-form/) decomposition $(\{\mathit{zip}, \mathit{city}\}, \{\mathit{street}, \mathit{zip}\})$. For $\mathit{street}\,\mathit{city} \to \mathit{zip}$: $Z = \{\mathit{street}, \mathit{city}\}$; part $\{\mathit{zip}, \mathit{city}\}$ gives $\mathit{city}^+ = \{\mathit{city}\}$; part $\{\mathit{street}, \mathit{zip}\}$ gives $\mathit{street}^+ = \{\mathit{street}\}$. $Z$ does not change and misses $\mathit{zip}$. So the dependency is lost: the two parts can hold $(\mathit{z1}, \mathit{c})$, $(\mathit{z2}, \mathit{c})$ and $(\mathit{s}, \mathit{z1})$, $(\mathit{s}, \mathit{z2})$, each legal, while their join has two zip codes for street $\mathit{s}$ in city $\mathit{c}$.

**Non-example from BCNF decomposition.** $R = ABCDE$, $F = \{A \to B,\ B \to C,\ CD \to E\}$ and $\rho = (AB, BC, ADE)$. For $CD \to E$, the loop stays at $Z = CD$, so $CD \to E$ is lost. The decomposition $(CDE, AD, AB, BC)$ of the same schema preserves $F$, since each dependency lies in one part.

**Preserving but lossy.** $R = ABCD$, $F = \{A \to B,\ C \to D\}$, $\rho = (AB, CD)$. Each dependency lies in a part, so $\rho$ preserves $F$. But the parts share no attribute, so the join is a cross product and $\rho$ is lossy.

## Related definitions

- **Lossless-join decomposition.** The other goal of a decomposition; see [lossless-join decomposition](/lossless-join-decomposition/). The two are independent, as the examples show.
- **BCNF and 3NF.** A [BCNF](/boyce-codd-normal-form/) decomposition that is lossless and dependency preserving may not exist, and deciding whether one exists is NP-hard (Tsou and Fischer 1982). A [3NF](/third-normal-form/) decomposition with both properties always exists and [3NF synthesis](/third-normal-form-synthesis/) finds one from a [minimal cover](/minimal-cover-problem/).
- **Implication.** The test is an instance of the [dependency implication problem](/dependency-implication-problem/) for the set $G$, solved without writing $G$ down. The basic rules of implication are [Armstrong's axioms](/armstrongs-axioms/).
- **Normalization.** The design process that uses these notions is [normalization](/normalization/).

## References
