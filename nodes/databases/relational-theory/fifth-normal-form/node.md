---
tag: PD85QQ
kind: definition
slug: fifth-normal-form
name: Fifth normal form (5NF)
aliases:
- 5NF
- project-join normal form
area: databases/relational-theory
level: advanced
summary: A schema in which every nontrivial join dependency is implied by the candidate keys, so no lossless split into projections removes redundancy.
prereqs: [join-dependency, fourth-normal-form, candidate-key]
see_also: [normalization, multivalued-dependency, chase-algorithm, boyce-codd-normal-form, third-normal-form, second-normal-form, lossless-join-test, first-normal-form]
sources:
  - paper: doi:10.1145/582095.582120
    title: Ronald Fagin, Normal forms and relational database operators, Proceedings of the 1979 ACM SIGMOD International Conference on Management of Data, 153 to 160 (1979)
    locator: project-join normal form, defined by the implication of all dependencies by the key dependencies
  - paper: doi:10.1145/132271.132274
    title: C. J. Date and Ronald Fagin, Simple conditions for guaranteeing higher normal forms in relational databases, ACM Transactions on Database Systems 17(3), 465 to 476 (1992)
    locator: a 3NF schema in which every key has one attribute is in project-join normal form
  - paper: doi:10.1145/320107.320115
    title: David Maier, Alberto O. Mendelzon and Yehoshua Sagiv, Testing implications of data dependencies, ACM Transactions on Database Systems 4(4), 455 to 469 (1979)
    locator: the chase for functional and join dependencies, used here for the test of a JD against the keys
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 11 (design and dependencies), normal forms for join dependencies
---

Fifth normal form, or project-join normal form, is the normal form of Fagin (1979) for schemas with [join dependencies](/join-dependency/). It asks that every join dependency that holds follows from the candidate keys alone, so a split into projections is lossless only for a reason that also makes it useless. The [normalization](/normalization/) page places 5NF at the top of the chain of normal forms, and the [BCNF](/boyce-codd-normal-form/) page treats the FD case. This page gives the exact definition, a test of a JD against the keys, the proof that 5NF implies 4NF, and one schema for each gap in the chain from 1NF to 5NF.

## Definition

Let $U$ be a finite set of attributes and $D$ a finite set of FDs and JDs over $U$, where an MVD $X \twoheadrightarrow Y$ counts as the JD $\bowtie[XY, X(U - XY)]$. We use set semantics. Let $K_1, \ldots, K_p$ be the [candidate keys](/candidate-key/) of $(U, D)$, and let $\mathrm{Keys}(D) = \{K_1 \to U, \ldots, K_p \to U\}$, the *key dependencies*.

**Definition (Fagin 1979; Date's form).** $(U, D)$ is in **fifth normal form** if every JD that $D$ implies is implied by $\mathrm{Keys}(D)$.

Fagin asked the same of the FDs that $D$ implies. This adds nothing: the proof below that 5NF implies 4NF shows that each nontrivial implied FD then has a superkey on its left side, and so follows from a key dependency.

**Testing a JD against the keys.** Let $\sigma = \bowtie[X_1, \ldots, X_k]$. Repeat: if two components $X_i$ and $X_j$ have $K_l \subseteq X_i \cap X_j$ for some key $K_l$, replace them by $X_i \cup X_j$. Then $\mathrm{Keys}(D) \models \sigma$ if and only if this ends with a component equal to $U$.

*Proof.* Run the [chase](/chase-algorithm/) of the tableau for $\sigma$ with the FDs $K_l \to U$: row $i$ has $0$ on $X_i$ and the symbol $i$ elsewhere. We claim that at each time the rows fall into *classes*, where all rows of a class are equal, have $0$ on the union $C$ of their components and a symbol of their own elsewhere. This holds at the start. Two rows of different classes $C$ and $C'$ agree exactly on $C \cap C'$, where both hold $0$. So $K_l \to U$ applies to them exactly when $K_l \subseteq C \cap C'$, and then it makes all their symbols equal, which merges the two classes into one class with union $C \cup C'$. So the chase performs exactly the merges of the test. It ends with an all-$0$ row exactly when some class has $C = U$, and by the chase theorem this is exactly when $\mathrm{Keys}(D) \models \sigma$. $\square$

The test is polynomial once the keys are known. Finding all keys can take exponential time, since there can be exponentially many.

**It is enough to check $D$.** If each FD of $D$ has a superkey on its left side and each JD of $D$ passes the test above, then $(U, D)$ is in 5NF. *Proof.* $\mathrm{Keys}(D)$ implies each member of $D$: an FD $X \to Y$ with $X \supseteq K_l$ follows from $K_l \to U$. Also $D$ implies $\mathrm{Keys}(D)$. So the two sets imply the same JDs. $\square$ Superkeys under $D$ must be found with an implication test for FDs and JDs, such as the chase.

**5NF implies 4NF.** Let $(U, D)$ be in 5NF and let $D \models X \twoheadrightarrow Y$ be nontrivial, with $Z = U - XY$. This MVD is the JD $\bowtie[XY, XZ]$, so $\mathrm{Keys}(D)$ implies it. $\mathrm{Keys}(D)$ holds FDs only, so by Fagin's theorem and the binary test of the [lossless join](/lossless-join-decomposition/) page, $\mathrm{Keys}(D) \models X \to Y$ or $\mathrm{Keys}(D) \models X \to Z$. Both are nontrivial FDs. Every FD of $\mathrm{Keys}(D)$ has a key on its left side, so $(U, \mathrm{Keys}(D))$ is in BCNF, and the left side $X$ of a nontrivial FD that it implies is a superkey. So $(U, D)$ is in [4NF](/fourth-normal-form/). $\square$

**A sufficient condition (Date and Fagin 1992).** If $(U, D)$ is in 3NF and every candidate key has a single attribute, then it is in 5NF.

## Examples and non-examples

**The strict chain.** Each normal form implies the one before it, $\text{5NF} \Rightarrow \text{4NF} \Rightarrow \text{BCNF} \Rightarrow \text{3NF} \Rightarrow \text{2NF} \Rightarrow \text{1NF}$, and each step is strict:

| in | not in | schema | dependencies | the violation |
|---|---|---|---|---|
| 1NF | 2NF | $\mathrm{Grade}(S, C, G, N)$ | $SC \to G$, $S \to N$ | $N$ depends on the part $S$ of the key $SC$ |
| 2NF | 3NF | $\mathrm{Emp}(E, D, N)$ | $E \to D$, $D \to N$ | $D$ is not a superkey and $N$ is not prime |
| 3NF | BCNF | $\mathrm{Addr}(C, S, Z)$ | $CS \to Z$, $Z \to C$ | $Z$ is not a superkey, but $C$ is prime |
| BCNF | 4NF | $\mathrm{CTB}(C, T, B)$ | $C \twoheadrightarrow T$ | $C$ is not a superkey |
| 4NF | 5NF | $\mathrm{SPJ}(S, P, J)$ | $\bowtie[SP, PJ, JS]$ | the JD does not follow from the key $SPJ$ |

The pages of [2NF](/second-normal-form/), [3NF](/third-normal-form/) and [4NF](/fourth-normal-form/) explain the first four rows. For the last one: the JD implies no FD, because the chase with JDs never makes two symbols equal, so the only key is $SPJ$. The JD implies no nontrivial MVD either, as the [join dependency](/join-dependency/) page shows with the chase, so $\mathrm{SPJ}$ is in 4NF. In the test against the key $SPJ$, no two components contain the key in their intersection, so no merge happens, no component becomes $U$, and the JD is not implied by the keys. The 5NF split is into $SP$, $PJ$ and $JS$, and each part, with two attributes and no dependency, is in 5NF.

- **A JD that the key implies.** $\mathrm{Emp}(E, N, S, D)$ with employee, name, salary and department, and $F = \{E \to NSD\}$. The JD $\bowtie[EN, ES, ED]$ holds, and the test merges $EN$ and $ES$ on the key $E$, then $ENS$ and $ED$, which gives $U$. So the JD follows from the key. The schema is in 5NF, and indeed by Date and Fagin, since it is in 3NF with a single-attribute key. Splitting it into three parts would be lossless but would remove no redundancy.
- **No dependencies.** With $D = \emptyset$, the only key is $U$, every implied JD is trivial, and the schema is in 5NF.

## Related definitions

- **Join dependency.** The [JD](/join-dependency/) page defines join dependencies, their trivial cases and their relation to MVDs.
- **4NF and BCNF.** [4NF](/fourth-normal-form/) is 5NF restricted to JDs with two components, and [BCNF](/boyce-codd-normal-form/) is the case of FDs. With FDs only, BCNF, 4NF and 5NF agree, because every JD that FDs imply is then implied by the keys.
- **Implication of JDs.** Deciding whether $D$ implies a JD uses the [chase](/chase-algorithm/). With JDs in $D$ the chase can be expensive, which makes 5NF hard to test in general. The test against the keys above is the easy part.
- **Lossless decompositions.** The split of a schema that violates 5NF uses the components of the violating JD, and it is lossless because the JD holds. The [tableau test](/lossless-join-test/) checks lossless joins under FDs.

## References
