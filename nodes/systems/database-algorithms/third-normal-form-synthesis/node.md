---
tag: NWV2WW
kind: algorithm
slug: third-normal-form-synthesis
name: 3NF synthesis
aliases:
- Bernstein synthesis
- 3NF synthesis algorithm
- third normal form synthesis
area: systems/database-algorithms
level: core
summary: "Builds a 3NF decomposition that is lossless and dependency preserving: one schema per left side of a minimal cover, plus a key schema if needed, minus subsumed schemas."
model: word-ram
complexity:
  vars: {n: the number of attributes, m: the total number of attribute occurrences in F}
  time: {worst: O(n (n + m)²)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1976
  people: [Philip A. Bernstein, Joachim Biskup, Umeshwar Dayal]
  note: Bernstein gave the synthesis of 3NF schemas from a minimal cover in 1976. Biskup, Dayal and Bernstein added the key schema in 1979, which makes the result lossless.
prereqs: [third-normal-form, minimal-cover-problem]
see_also: [bcnf-decomposition, lossless-join-decomposition, dependency-preserving-decomposition, chase-algorithm, attribute-closure-algorithm, normalization, boyce-codd-normal-form]
sources:
  - paper: doi:10.1145/320493.320489
    title: Philip A. Bernstein, Synthesizing third normal form relations from functional dependencies, ACM Transactions on Database Systems 1(4), 277 to 298 (1976)
    locator: the synthesis algorithm from a minimal cover, with the grouping of FDs by left side
  - paper: "Joachim Biskup, Umeshwar Dayal and Philip A. Bernstein, Synthesizing independent database schemas, Proceedings of the ACM SIGMOD Conference (1979), 143 to 151"
    locator: the added key schema, and the result that a dependency-preserving decomposition is lossless if and only if some schema holds a key
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Section 7.8 (dependency-preserving 3NF decompositions, with the key added for a lossless join); Section 7.4 (the tableau test for lossless joins)
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Section 11.2 (normal forms and the 3NF synthesis algorithm); Section 8.4 (the chase)
  - paper: doi:10.1145/319732.319749
    title: Carlo Zaniolo, A new normal form for the design of relational database schemata, ACM Transactions on Database Systems 7(3), 489 to 499 (1982)
    locator: the synthesized schemas are in elementary key normal form
  - paper: doi:10.1145/320064.320066
    title: Catriel Beeri and Philip A. Bernstein, Computational problems related to the design of normal form relational schemas, ACM Transactions on Database Systems 4(1), 30 to 59 (1979)
    locator: the linear closure algorithm and the minimal cover used by synthesis
---

3NF synthesis builds a database schema from a set $F$ of [functional dependencies](/functional-dependency/). It computes a [minimal cover](/minimal-cover-problem/) of $F$, makes one relation schema for each left side, adds one schema for a key if no schema holds a key, and removes each schema that is part of another. The result is in [third normal form](/third-normal-form/), it preserves all dependencies, and its natural join is lossless. Bernstein gave the synthesis in 1976, and Biskup, Dayal and Bernstein added the key step in 1979.

## In plain words

Start from the rules "these columns fix that column". First clean the rules: one column on each right side, no extra columns on the left, and no rule that the others give. Then make one table for each different left side, with the left-side columns and all the columns it fixes. Each rule now lives inside one table, so a system can check it there. If no table holds a key of the whole data, add a table with just a key. This table is what lets the tables join back to the original data with no false rows. Last, drop a table if all its columns are in another table.

## The problem

The input is a finite attribute set $U$ and a set $F$ of FDs over $U$. The output is a list of attribute sets $R_1, \ldots, R_s$ with $R_1 \cup \cdots \cup R_s = U$, such that:

1. each $R_i$, with the FDs of $F^+$ that hold inside it, is in [3NF](/third-normal-form/);
2. the decomposition is *dependency preserving*: the FDs of $F^+$ that hold inside the $R_i$ imply $F$ (see [dependency-preserving decomposition](/dependency-preserving-decomposition/));
3. the decomposition is *lossless*: for each relation $r$ over $U$ that satisfies $F$, $r = \pi_{R_1}(r) \bowtie \cdots \bowtie \pi_{R_s}(r)$ (see [lossless-join decomposition](/lossless-join-decomposition/)).

Such a decomposition exists for each $F$. For [BCNF](/boyce-codd-normal-form/), conditions 2 and 3 together can be impossible.

## The algorithm

```pseudo id=main
3NF-SYNTHESIS(U, F)
L1  G ← a minimal cover of F
L2  for each distinct left side X of G do
L3      R_X ← X ∪ {A : X → A is in G}
L4  S ← the list of all R_X
L5  if no schema T in S has T⁺ = U under G then
L6      K ← a key of U under G; append K to S
L7  remove from S each schema that is a subset of another schema in S, and keep one copy of equal schemas
L8  return S
```

Line L1 uses the three-step algorithm of the [minimal cover problem](/minimal-cover-problem/): split right sides, remove extraneous left-side attributes, then remove redundant FDs. Line L5 makes one [attribute closure](/attribute-closure-algorithm/) per schema. Line L6 finds a key by starting with $U$ and removing each attribute whose removal keeps a superkey. If $G$ is empty, the loop makes no schema, and line L6 adds the key $U$.

## Example

**Ullman's course schema.** $U = CTHRSG$ (course, teacher, hour, room, student, grade) with

$$F = \{ C \to T,\ HR \to C,\ HT \to R,\ CS \to G,\ HS \to R \}.$$

- L1: $F$ is already a minimal cover, so $G = F$.
- L2 to L4: each FD has its own left side, so there are five schemas: $CT$, $CHR$, $HRT$, $CGS$ and $HRS$.
- L5: $HRS^+ = U$, since $HS$ is a key. No key schema is added.
- L7: no schema is a subset of another.

The result is $\{CT, CHR, HRT, CGS, HRS\}$. Each schema is in 3NF. For example, $CHR$ has the keys $HR$ and $CH$, since $CH^+ = CTHR$, so each of its attributes is prime. The original schema had four 3NF violations.

**A key schema is needed.** $U = ABCD$ with $F = \{A \to B, C \to D\}$. Lines L2 to L4 give $AB$ and $CD$. Neither holds the key $AC$ of $U$, so line L6 adds $AC$. The result is $\{AB, CD, AC\}$. Without $AC$ the decomposition is lossy: the relation $\{(1,1,1,1), (2,2,2,2)\}$ over $ABCD$ satisfies $F$, but the join of its projections on $AB$ and $CD$ has four tuples, including $(1,1,2,2)$.

**One schema.** $U = CSZ$ with $F = \{CS \to Z, Z \to C\}$. The schemas are $CSZ$ and $CZ$. $CSZ$ holds a key, and $CZ \subseteq CSZ$ is removed in line L7. The result is the original schema, which is already in 3NF. [BCNF decomposition](/bcnf-decomposition/) would split it and lose $CS \to Z$.

## Correctness

Let $G$ be the minimal cover from line L1. The proof has three parts.

- **3NF.** In $R_X$, the left side $X$ is a key of $R_X$, because $G$ has no extraneous attribute. Let $Y \to B$ be a nontrivial FD that holds in $R_X$, with $Y$ not a superkey of $R_X$. If $B \in X$, then $B$ is prime in $R_X$. If $B \notin X$, then $X \to B$ is in $G$, and since $Y$ does not determine $X$, the FD $X \to B$ never fires in the computation of $Y^+$. Then $X \to B$ follows from the rest of $G$, so it is redundant, which contradicts minimality. A key schema has no nontrivial FD inside it, because a key is minimal.
- **Dependency preservation.** Each FD $X \to A$ of $G$ lies inside $R_X$, or inside the schema that subsumed $R_X$ in line L7. $G$ is equivalent to $F$.
- **Lossless join.** Some schema holds a key $K$ of $U$. Run the [chase](/chase-algorithm/) on the tableau with one row per schema. Follow the order in which the closure algorithm adds attributes to $K^+$: each step uses an FD $X \to A$ of $G$ whose schema row is distinguished on $X$ and $A$, so the key row becomes distinguished on $A$. At the end the key row is all distinguished, which means the join is lossless.

The full proof is below. The implementation checks all three properties on 150 random inputs: 3NF by brute force over the projected FDs, preservation with closures, and losslessness both by the chase and on random relations that satisfy $F$.

## Complexity

Let $n = |U|$ and $m = \|F\|$.

- L1: the minimal cover takes $O(m)$ closures of $O(n + m)$ each, so $O(m(n + m))$.
- L2 to L4: grouping by left side takes $O(m)$ with hashing, and gives at most $|G| \le m$ schemas.
- L5: one closure per schema, $O(m(n + m))$.
- L6: $n$ closures, $O(n(n + m))$.
- L7: compare all pairs of schemas, $O(m^2 n)$, or $O(m^2 n / w)$ with bit sets in words of $w$ bits.

The total is $O(n (n + m)^2)$, polynomial in the input. The algorithm never lists all keys, so it avoids the NP-complete prime attribute test that a 3NF check would need.

## Properties

- **Deterministic.** The result depends on the order of the FDs and attributes, because the minimal cover and the key are not unique. Each result has the three properties.
- **Not unique.** Different minimal covers give different schemas. For $F = \{A \to BC, B \to AC, C \to AB\}$, the covers $\{A \to B, B \to C, C \to A\}$ and $\{A \to C, B \to C, C \to A, C \to B\}$ give $\{AB, BC, AC\}$ and $\{AC, BC, ABC\}$ before line L7; after line L7 the second is the single schema $ABC$.
- **Elementary key normal form.** The schemas are also in Zaniolo's elementary key normal form, which lies between 3NF and BCNF (Zaniolo 1982).
- **Often BCNF.** In many practical schemas, each synthesized schema is in BCNF too. A schema $R_X$ fails BCNF only when some FD inside it has a non-superkey left side and a right side in $X$, as $Z \to C$ in $CSZ$.

## Variants and improvements

- **Merging equivalent keys.** Bernstein's 1976 algorithm also merged the groups of left sides that determine each other ($X^+ = Y^+$) into one schema, and removed transitive dependencies between them. This gives fewer schemas.
- **Without the key schema.** The 1976 algorithm did not add a key, so it could be lossy, as in the $\{A \to B, C \to D\}$ example. Biskup, Dayal and Bernstein (1979) showed that a dependency-preserving decomposition into schemas of this form is lossless if and only if some schema holds a key of $U$.
- **BCNF decomposition.** The other classic approach splits $U$ on violating FDs until each part is in BCNF. It is always lossless, but it can lose dependencies, and testing a subschema needs the projected FDs. See [BCNF decomposition](/bcnf-decomposition/).
- **3NF then BCNF.** Some design tools synthesize 3NF first, and then split the few schemas that are not in BCNF, if the designer accepts the lost dependencies.

## When to use it

Use 3NF synthesis when the FDs are known and each of them must be checkable on one relation, for example as a key or a unique index. It runs in polynomial time even for schemas with many keys. Use BCNF decomposition instead when less redundancy matters more than local checks, or when the synthesized schemas are already in BCNF, which is common.

## Pitfalls

- **Skipping the key schema.** Without lines L5 and L6, the result can be lossy, as in the $\{A \to B, C \to D\}$ example.
- **A cover that is not minimal.** With a redundant FD, a schema can fail 3NF. For $F = \{A \to B, B \to C, A \to C\}$, grouping without the cover gives $ABC$ and $BC$. Then $ABC$ holds $B \to C$ with $B$ not a superkey and $C$ not prime, so it is not in 3NF. The minimal cover $\{A \to B, B \to C\}$ gives $AB$ and $BC$.
- **Wrong step order in the cover.** The minimal cover must left-reduce before it removes redundant FDs. Otherwise a redundant FD can remain, with the problem above. See the [minimal cover problem](/minimal-cover-problem/) for an example.
- **Testing the result by keys of $U$.** The 3NF test of each $R_i$ uses the FDs that hold inside $R_i$ and the keys of $R_i$, not the keys of $U$.

## Implementations

## History

Codd defined 3NF in 1971 and 1972 and designed schemas by decomposition. Bernstein's 1976 paper in ACM Transactions on Database Systems took the opposite approach: synthesize the schemas from the FDs, with one relation per group of FDs that share a left side. It used the minimal cover, which Beeri and Bernstein (1979) then computed with the linear closure algorithm. Biskup, Dayal and Bernstein (1979) added the key schema and proved that it makes the synthesis lossless. Zaniolo (1982) showed that the result also meets his elementary key normal form. The algorithm with the key step is the version in Ullman's 1988 textbook and in most courses.

## References
