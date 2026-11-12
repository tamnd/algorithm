---
tag: SA5P36
kind: definition
slug: third-normal-form
name: Third normal form (3NF)
aliases:
- 3NF
- third normal form
area: systems/database-algorithms
level: intro
summary: "A schema is in 3NF if, for each nontrivial FD X → A that holds, X is a superkey or A is in some key. Each schema has a lossless, dependency-preserving 3NF split."
prereqs: [normalization, dependency-implication-problem]
see_also: [third-normal-form-synthesis, boyce-codd-normal-form, minimal-cover-problem, bcnf-decomposition, dependency-preserving-decomposition, lossless-join-decomposition, first-normal-form]
sources:
  - paper: "E. F. Codd, Further normalization of the data base relational model, in R. Rustin (ed.), Data Base Systems, Courant Computer Science Symposia 6, Prentice-Hall (1972), 33 to 64"
    locator: the definitions of second and third normal form, with transitive dependence on a key
  - paper: doi:10.1145/319732.319749
    title: Carlo Zaniolo, A new normal form for the design of relational database schemata, ACM Transactions on Database Systems 7(3), 489 to 499 (1982)
    locator: the formulation of 3NF with superkeys and prime attributes, and elementary key normal form
  - paper: "Jieh Hsiang Jou and Patrick C. Fischer, The complexity of recognizing 3NF relation schemes, Information Processing Letters 14(4), 187 to 190 (1982)"
    locator: testing whether a schema is in 3NF is NP-complete
  - paper: doi:10.1016/0022-0000(78)90009-0
    title: Cláudio L. Lucchesi and Sylvia L. Osborn, Candidate keys for relations, Journal of Computer and System Sciences 17(2), 270 to 279 (1978)
    locator: the prime attribute problem is NP-complete; the algorithm that lists all keys
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Section 11.2 (normal forms, 3NF and BCNF)
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Section 7.6 (normal forms for relation schemes, 2NF, 3NF and BCNF) and Section 7.8 (dependency-preserving 3NF decompositions)
---

A relation schema is in third normal form (3NF) if each nontrivial [functional dependency](/functional-dependency/) $X \to A$ that holds in it has a superkey $X$ on the left or a prime attribute $A$ on the right. Codd defined 3NF in 1971 and 1972 as the absence of transitive dependencies of non-prime attributes on keys, and Zaniolo (1982) gave the form with superkeys and prime attributes that is used today. 3NF allows a little more redundancy than [Boyce-Codd normal form](/boyce-codd-normal-form/), and in exchange each schema has a 3NF decomposition that is lossless and preserves all dependencies. Testing 3NF is [NP-complete](/np-complete/), because it asks which attributes are in some key.

## Definition

Let $R(U)$ be a relation schema in [first normal form](/first-normal-form/), with a set $F$ of FDs. A *key* is a minimal set $K$ with $K^+ = U$, and an attribute is *prime* if it is in some key.

**Definition (Zaniolo 1982).** $R$ is in *3NF* if, for each FD $X \to A$ in $F^+$ with $A \notin X$ and $A$ a single attribute,

$$X \text{ is a superkey of } R \quad\text{or}\quad A \text{ is prime}.$$

**Definition (Codd 1972).** $R$ is in 3NF if it is in second normal form and no non-prime attribute is *transitively dependent* on a key: there are no $K$, $Y$ and $A$ with $K$ a key, $K \to Y$, $Y \not\to K$, $Y \to A$, $A \notin Y$ and $A$ non-prime. *Second normal form* (2NF) asks that no non-prime attribute depends on a proper subset of a key. For a 1NF schema, the two definitions of 3NF are equivalent.

**It is enough to check $F$.** Write each FD of $F$ with one attribute on the right side. Then $R$ is in 3NF if and only if each $X \to A$ in $F$ with $A \notin X$ has $X$ a superkey or $A$ prime.

*Proof.* The FDs of $F$ are in $F^+$, so one direction is clear. For the other, let $Y \to A$ be in $F^+$ with $A \notin Y$ and $Y$ not a superkey, so $Y^+ \ne U$. Compute $Y^+$ by firing FDs of $F$. Since $A \in Y^+ - Y$, some FD $X \to A$ of $F$ fired, with $X \subseteq Y^+$. Then $X^+ \subseteq Y^+ \ne U$, so $X$ is not a superkey. By the assumption on $F$, $A$ is prime. $\square$

**Testing.** The lemma gives this test:

1. Compute all keys of $R$: by brute force over the subsets of $U$, or with the Lucchesi and Osborn algorithm from the [dependency implication problem](/dependency-implication-problem/). Let $P$ be their union, the prime attributes.
2. For each $X \to A$ in $F$ with $A \notin X$: compute $X^+$. If $X^+ \ne U$ and $A \notin P$, report the violation $(X, A)$.

Step 2 takes polynomial time. Step 1 can take exponential time, because a schema can have $2^{|U|/2}$ keys. This cannot be avoided in general: **testing 3NF is NP-complete** (Jou and Fischer 1982). It is in NP: for each FD $X \to A$ of $F$ with $X$ not a superkey, a certificate gives a key that holds $A$, and each key is checked with $|K| + 1$ closures. NP-hardness comes from the NP-completeness of the prime attribute problem (Lucchesi and Osborn 1978). For comparison, BCNF needs only the superkey test, so it takes polynomial time for a schema with its own FDs.

## Examples and non-examples

**Non-example: a transitive dependency.** $\mathrm{Emp}(E, D, N)$ with $F = \{E \to D, D \to N\}$. The only key is $E$, so $D$ and $N$ are not prime. $D \to N$ violates 3NF: $D^+ = DN$, so $D$ is not a superkey. In Codd's terms, $N$ depends on the key $E$ through $D$. The update anomaly: a department name is stored once per employee.

**Non-example: a partial dependency.** $\mathrm{Grade}(S, C, G, N)$ with student, course, grade and student name, and $F = \{SC \to G, S \to N\}$. The key is $SC$. $S \to N$ violates 3NF, and also 2NF, because $S$ is a proper subset of the key.

**Non-example: Ullman's course schema.** $U = CTHRSG$ with $F = \{C \to T, HR \to C, HT \to R, CS \to G, HS \to R\}$. The only key is $HS$, so the prime attributes are $H$ and $S$. The violations are $C \to T$, $HR \to C$, $HT \to R$ and $CS \to G$. Only $HS \to R$ is allowed, since $HS$ is the key. [3NF synthesis](/third-normal-form-synthesis/) splits this schema into five 3NF schemas.

**Example: in 3NF, not in BCNF.** $\mathrm{Addr}(C, S, Z)$ with city, street and zip, and $F = \{CS \to Z, Z \to C\}$. The keys are $CS$ and $SZ$, so all three attributes are prime. $CS \to Z$ has a superkey on the left, and $Z \to C$ has a prime attribute on the right, so the schema is in 3NF. It is not in BCNF, because $Z$ is not a superkey. The redundancy that 3NF allows is visible here: the city of a zip code is stored once per street in it. Splitting it out would lose the dependency $CS \to Z$.

**Example: a key only.** A schema whose FDs all have a superkey on the left is in BCNF, so it is in 3NF. A schema with $F = \emptyset$ is in 3NF: its only key is $U$.

**Frequency.** On 400 random schemas over 5 attributes, each with up to 5 FDs, the implementation found 283 not in 3NF, 5 in 3NF but not in BCNF, and 112 in BCNF. It compared the lemma-based test with a check of all implied FDs $X \to A$ on all 400.

## Related definitions

- **Boyce-Codd normal form.** Drop the exception for prime attributes: for each nontrivial $X \to A$, $X$ is a superkey. BCNF implies 3NF. See [Boyce-Codd normal form](/boyce-codd-normal-form/) and [BCNF decomposition](/bcnf-decomposition/).
- **Elementary key normal form.** Zaniolo (1982) defined EKNF, between 3NF and BCNF. A key $K$ is *elementary* if some attribute $A$ has $K \to A$ with no proper subset of $K$ determining $A$. EKNF allows a non-superkey $X$ in $X \to A$ only when $A$ is in an elementary key. Zaniolo showed that Bernstein's synthesis yields schemas in EKNF.
- **Second normal form.** 3NF implies 2NF. The schema $\mathrm{Emp}$ above is in 2NF and not in 3NF.
- **Synthesis.** Each schema has a decomposition into 3NF schemas that is lossless and dependency preserving. [3NF synthesis](/third-normal-form-synthesis/) builds it from a [minimal cover](/minimal-cover-problem/) in polynomial time, without computing all keys. See also [lossless-join decomposition](/lossless-join-decomposition/) and [dependency-preserving decomposition](/dependency-preserving-decomposition/).
- **3NF of a subschema.** For a schema $R_i$ inside a decomposition, the FDs are the projection of $F^+$ onto $U_i$, which can need exponentially many FDs to write down. Then even step 2 of the test is costly.

## References
