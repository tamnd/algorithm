---
tag: W6NDNV
kind: definition
slug: boyce-codd-normal-form
name: Boyce-Codd normal form (BCNF)
aliases:
- BCNF
- Boyce-Codd normal form
area: systems/database-algorithms
level: intro
summary: "A schema is in BCNF when the left side of every nontrivial functional dependency that holds is a superkey. Testing a schema against its own FDs is polynomial; testing a projection is coNP-complete."
prereqs: [functional-dependency, attribute-closure-algorithm]
see_also: [bcnf-decomposition, third-normal-form, normalization, dependency-preserving-decomposition, lossless-join-decomposition, third-normal-form-synthesis, first-normal-form]
sources:
  - paper: "E. F. Codd, Recent investigations in relational data base systems, Information Processing 74 (Proceedings of the IFIP Congress 1974), North-Holland, pages 1017 to 1021"
    locator: the definition of the normal form now called BCNF
  - paper: doi:10.1145/320064.320066
    title: Catriel Beeri and Philip A. Bernstein, Computational problems related to the design of normal form relational schemas, ACM Transactions on Database Systems 4(1), 30 to 59 (1979)
    locator: the NP-completeness of deciding whether a subschema violates BCNF
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 11 (design and dependencies), the definition of BCNF and its relation to 3NF
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Chapter 7 (design theory for relational databases), the normal forms for relation schemes
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson (2009)
    locator: Section 3.3 (Boyce-Codd normal form and decomposition into BCNF)
---

A relation schema $R$ with a set $F$ of [functional dependencies](/functional-dependency/) is in Boyce-Codd normal form (BCNF) when, for every nontrivial dependency $X \to Y$ that holds, the left side $X$ is a superkey of $R$. A schema in BCNF stores no fact twice because of a functional dependency. Codd stated the form in 1974, and it is the strictest normal form that is defined by functional dependencies alone. To test a schema against its own set $F$ takes polynomial time with the [attribute closure algorithm](/attribute-closure-algorithm/), but to test a projection of $R$ is coNP-complete.

## Definition

Let $R$ be a finite set of attributes and $F$ a set of functional dependencies over $R$. Write $F \models X \to Y$ when every relation over $R$ that satisfies $F$ also satisfies $X \to Y$, and write $X^+$ for the closure of $X$ under $F$, the set of all attributes $A$ with $F \models X \to A$.

- $X \to Y$ is *trivial* when $Y \subseteq X$.
- $X$ is a *superkey* of $R$ when $X \to R$ holds, that is, when $R \subseteq X^+$.

**Definition.** $(R, F)$ is in BCNF if and only if

$$\forall X \subseteq R,\ \forall A \in R \setminus X:\quad F \models X \to A \;\Longrightarrow\; R \subseteq X^+ .$$

In words: if $X$ fixes any attribute outside $X$, then $X$ fixes all attributes.

**Subschemas.** For $S \subseteq R$, the *projection* of $F$ onto $S$ is $\pi_S(F) = \{X \to A : X \cup \{A\} \subseteq S,\ F \models X \to A\}$. The subschema $S$ is in BCNF when $(S, \pi_S(F))$ is in BCNF, that is, when every $X \subseteq S$ with $(X^+ \cap S) \setminus X \ne \emptyset$ has $S \subseteq X^+$. This is the case that arises after a [decomposition](/bcnf-decomposition/).

### Testing BCNF

**The full schema needs only the dependencies of $F$.** $(R, F)$ is in BCNF if and only if each $X \to Y$ in $F$ with $Y \not\subseteq X$ has $R \subseteq X^+$.

*Proof.* The direction "only if" holds because each dependency of $F$ holds. For "if", assume that each nontrivial dependency of $F$ has a superkey on its left side, and let $X \to A$ hold with $A \notin X$. The attribute closure algorithm builds $X^+$ from $X$. Since $A \in X^+ \setminus X$, it applies at least one dependency. The first one it applies is some $L \to M$ in $F$ with $L \subseteq X$ and $M \not\subseteq X$, so $M \not\subseteq L$ and $L \to M$ is nontrivial. By the assumption $R \subseteq L^+$, and $L^+ \subseteq X^+$ because $L \subseteq X$. So $X$ is a superkey. $\square$

So the test costs $|F|$ closure computations, which is polynomial. With the linear-time closure algorithm it is $O(|F| \cdot \|F\|)$, where $\|F\|$ is the total length of $F$.

**A subschema is hard.** The result above uses the dependencies of $F$ itself. For a subschema $S$, the projection $\pi_S(F)$ can be exponentially larger than $F$, and the dependencies of $F$ that lie inside $S$ do not tell the answer. Beeri and Bernstein proved that to decide whether a subschema violates BCNF is NP-complete. So to decide that a subschema is in BCNF is coNP-complete. The direct test tries every $X \subseteq S$, which costs $2^{|S|}$ closures.

## Examples and non-examples

**Non-example: street, city, zip.** Let $R = \{\mathit{street}, \mathit{city}, \mathit{zip}\}$ with

$$F = \{\ \mathit{street}\,\mathit{city} \to \mathit{zip},\quad \mathit{zip} \to \mathit{city}\ \}.$$

The keys are $\{\mathit{street}, \mathit{city}\}$ and $\{\mathit{street}, \mathit{zip}\}$. The dependency $\mathit{zip} \to \mathit{city}$ is nontrivial, and $\mathit{zip}^+ = \{\mathit{zip}, \mathit{city}\}$ does not contain $\mathit{street}$. So $R$ is not in BCNF. The city of a zip code is stored again in each row with that zip code. $R$ is in [third normal form](/third-normal-form/), because $\mathit{city}$ is part of a key.

This schema has no decomposition into BCNF that preserves the dependencies. *Proof.* A [dependency-preserving decomposition](/dependency-preserving-decomposition/) must have a component that contains all three attributes. If not, each component has at most two attributes. Over $F$, the only nontrivial dependency between two single attributes is $\mathit{zip} \to \mathit{city}$: the closures are $\mathit{street}^+ = \{\mathit{street}\}$, $\mathit{city}^+ = \{\mathit{city}\}$ and $\mathit{zip}^+ = \{\mathit{zip}, \mathit{city}\}$. So the union of the projections is equivalent to $\{\mathit{zip} \to \mathit{city}\}$, and the closure of $\{\mathit{street}, \mathit{city}\}$ under it is $\{\mathit{street}, \mathit{city}\}$, which misses $\mathit{zip}$. So the decomposition does not imply $\mathit{street}\,\mathit{city} \to \mathit{zip}$. A component with all three attributes is $R$ itself, which is not in BCNF. $\square$ The BCNF decomposition $\{\mathit{zip}, \mathit{city}\}$, $\{\mathit{street}, \mathit{zip}\}$ is [lossless](/lossless-join-decomposition/), but a database can then hold two rows with the same street and city and different zip codes, and no single relation shows the violation.

**Non-example: a transitive dependency.** $R = ABC$ with $F = \{A \to B,\ B \to C\}$. Here $B \to C$ holds and $B^+ = BC$, so $R$ is not in BCNF. This schema is not in 3NF either.

**Example: two keys.** $R = ABC$ with $F = \{A \to BC,\ BC \to A\}$. Both left sides are keys, so $R$ is in BCNF.

**Example: two attributes.** A schema $\{A, B\}$ is in BCNF unless exactly one of its attributes is constant. A nontrivial dependency inside it has the form $B \to A$, $A \to B$ or $\emptyset \to A$ (or $\emptyset \to B$). For $B \to A$, the closure of $B$ holds $A$ and $B$, so $B$ is a superkey. For $\emptyset \to A$, the empty set is a superkey only if $\emptyset \to B$ also holds. So the only violation is a dependency $\emptyset \to A$ (the attribute $A$ has one value in every relation) without $\emptyset \to B$.

**The projection pitfall.** $R = ABCD$ with $F = \{A \to B,\ B \to C\}$, and the subschema $S = ACD$. No dependency of $F$ lies inside $S$, so a check of $F$ alone finds nothing. But $A \to C$ holds, and $A^+ \cap S = AC$, which misses $D$. So $S$ is not in BCNF.

## Related definitions

- **Third normal form.** [3NF](/third-normal-form/) allows a violation $X \to A$ when $A$ is a prime attribute (a member of some key). So BCNF implies 3NF, and the street, city, zip schema shows that the converse fails. Every schema has a lossless, dependency-preserving 3NF decomposition by [3NF synthesis](/third-normal-form-synthesis/), but not always a BCNF one.
- **BCNF decomposition.** The [BCNF decomposition algorithm](/bcnf-decomposition/) splits a schema on a violation until each part is in BCNF. The result is always lossless, but it can lose dependencies, as above. Tsou and Fischer showed that to decide whether a dependency-preserving BCNF decomposition exists is NP-hard.
- **Lossless join and dependency preservation.** These are the two goals of a decomposition. See [lossless-join decomposition](/lossless-join-decomposition/) and [dependency-preserving decomposition](/dependency-preserving-decomposition/).
- **Fourth normal form.** 4NF replaces functional dependencies by multivalued dependencies in the same condition. A schema in 4NF is in BCNF.
- **Normalization.** The general theory of normal forms is on the page [normalization](/normalization/), and the most basic form is [first normal form](/first-normal-form/).

## References
