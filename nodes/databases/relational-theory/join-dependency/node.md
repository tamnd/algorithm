---
tag: 0MG279
kind: definition
slug: join-dependency
name: Join dependency
aliases:
- JD
area: databases/relational-theory
level: advanced
summary: A constraint that a relation equals the natural join of its projections on given sets of attributes; an MVD is the case of two sets.
prereqs: [multivalued-dependency, relational-algebra]
see_also: [fifth-normal-form, chase-algorithm, lossless-join-test, acyclic-hypergraph, tuple-generating-dependency, heaths-theorem, entity-relationship-model, normalization]
sources:
  - paper: doi:10.1145/582095.582120
    title: Ronald Fagin, Normal forms and relational database operators, Proceedings of the 1979 ACM SIGMOD International Conference on Management of Data, 153 to 160 (1979)
    locator: join dependencies and project-join normal form
  - paper: doi:10.1145/320083.320091
    title: Alfred V. Aho, Catriel Beeri and Jeffrey D. Ullman, The theory of joins in relational databases, ACM Transactions on Database Systems 4(3), 297 to 314 (1979)
    locator: lossless joins of several projections and the tableau test
  - paper: doi:10.1145/320107.320115
    title: David Maier, Alberto O. Mendelzon and Yehoshua Sagiv, Testing implications of data dependencies, ACM Transactions on Database Systems 4(4), 455 to 469 (1979)
    locator: the chase decides implication of functional and join dependencies
  - paper: "Catriel Beeri, Ronald Fagin, David Maier and Mihalis Yannakakis, On the desirability of acyclic database schemes, Journal of the ACM 30(3) (1983)"
    locator: a join dependency with an acyclic hypergraph is equivalent to a set of multivalued dependencies
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 8 (functional and join dependency), join dependencies and the chase
---

A join dependency says that a relation is the natural join of its projections on some given sets of attributes, so it can be stored as those projections and rebuilt without loss. A [multivalued dependency](/multivalued-dependency/) is the case of two sets, and join dependencies with three or more sets express constraints that no MVD or FD can. The [normalization](/normalization/) page mentions them only as the basis of 5NF, and [BCNF](/boyce-codd-normal-form/) does not see them at all. This page defines join dependencies, shows when they are trivial and how they relate to MVDs, and gives the standard example.

## Definition

Let $U$ be a finite set of attributes and let $X_1, \ldots, X_k \subseteq U$ with $X_1 \cup \cdots \cup X_k = U$. We use set semantics.

**Definition.** A relation $r$ over $U$ *satisfies* the **join dependency** (JD) $\bowtie[X_1, \ldots, X_k]$ if
$$r = \pi_{X_1}(r) \bowtie \pi_{X_2}(r) \bowtie \cdots \bowtie \pi_{X_k}(r).$$

Each tuple of $r$ is in the join of its own projections, so the condition is that the join adds no tuple. In tuple form: for any $t_1, \ldots, t_k \in r$ and any tuple $t$ over $U$ with $t[X_i] = t_i[X_i]$ for each $i$, also $t \in r$. So a JD is a full [tuple-generating dependency](/tuple-generating-dependency/). The sets $X_i$ are the *components*, and they form a [hypergraph](/hypergraph/) on $U$.

**Trivial JDs.** $\bowtie[X_1, \ldots, X_k]$ holds in every relation over $U$ if and only if some $X_i = U$.

*Proof.* If $X_i = U$, each tuple $t$ of the join has $t = t[X_i] \in \pi_U(r) = r$. If no $X_i$ is $U$, let $r$ have the $k$ tuples $t_i$ with the value $0$ on $X_i$ and the value $i$ elsewhere. Each $t_i$ is $0$ on $X_i$, so the all-$0$ tuple is in the join. It is not in $r$, since each $t_i$ has a value $i \ne 0$ outside $X_i$. $\square$

**Two components are an MVD.** With $k = 2$, the JD $\bowtie[X_1, X_2]$ is the MVD $X_1 \cap X_2 \twoheadrightarrow X_1$, by Fagin's theorem (see [Heath's theorem](/heaths-theorem/)). Conversely, $X \twoheadrightarrow Y$ is the JD $\bowtie[XY, X(U - XY)]$.

**Merging components weakens a JD.** If $r$ satisfies $\bowtie[X_1, X_2, X_3, \ldots, X_k]$, it satisfies $\bowtie[X_1 \cup X_2, X_3, \ldots, X_k]$. *Proof.* A tuple $t$ of the second join has $t[X_1 X_2] \in \pi_{X_1 X_2}(r)$, so $t[X_1] \in \pi_{X_1}(r)$ and $t[X_2] \in \pi_{X_2}(r)$, and $t$ is in the first join, which is $r$. $\square$ So a JD implies each MVD $X_1 \cap (X_2 \cup \cdots \cup X_k) \twoheadrightarrow X_1$ that comes from a split of its components into two groups. A component contained in another one can be dropped without changing the JD.

**Implication.** A set $D$ of FDs and JDs *implies* a JD $\sigma$ if every relation that satisfies $D$ satisfies $\sigma$. The [chase](/chase-algorithm/) decides this (Maier, Mendelzon and Sagiv 1979), with a start tableau of one row per component of $\sigma$. With FDs only in $D$, this is the [tableau test](/lossless-join-test/) for a lossless join, which runs in polynomial time. With JDs in $D$, the tableau can grow, and the chase page gives what is known about the cost.

## Examples and non-examples

- **A three-way rule.** $\mathrm{SPJ}(S, P, J)$ with supplier, part and project, and the rule: if supplier $s$ supplies part $p$, part $p$ is used in project $j$, and $s$ supplies project $j$, then $s$ supplies $p$ to $j$. This is the JD $\bowtie[SP, PJ, JS]$. The relation
  $$r = \{(s_1, p_1, j_2),\ (s_1, p_2, j_1),\ (s_2, p_1, j_1),\ (s_1, p_1, j_1)\}$$
  satisfies it. The first three tuples give $s_1 p_1$, $p_1 j_1$ and $j_1 s_1$, and the fourth tuple is the one the rule asks for.
- **Non-example: one tuple missing.** Remove $(s_1, p_1, j_1)$. The projections on $SP$, $PJ$ and $JS$ still contain $s_1 p_1$, $p_1 j_1$ and $j_1 s_1$, so the join of the three projections has the spurious tuple $(s_1, p_1, j_1)$, and the JD fails.
- **A JD that is not an MVD.** $\bowtie[SP, PJ, JS]$ implies no nontrivial MVD over $SPJ$. The chase of each of the twelve nontrivial MVDs over three attributes, $\emptyset \twoheadrightarrow S$ to $J \twoheadrightarrow P$, with this JD, ends without an all-$0$ row. Each split of its components into two groups gives a component equal to $SPJ$, a trivial JD, which agrees with the merging rule. So no lossless split into two projections explains $r$, but the split into three does.
- **MVDs as JDs.** In $\mathrm{CTB}(C, T, B)$, the MVD $C \twoheadrightarrow T$ is the JD $\bowtie[CT, CB]$.
- **Trivial JDs.** $\bowtie[AB, ABC]$ over $ABC$ holds in every relation, because one component is all of $U$.

## Related definitions

- **Fifth normal form.** A schema is in [5NF](/fifth-normal-form/) when each JD that holds is implied by the candidate keys. $\mathrm{SPJ}$ with its JD is in 4NF and not in 5NF.
- **Acyclic JDs.** If the hypergraph of the components is [acyclic](/acyclic-hypergraph/), the JD is equivalent to a set of MVDs (Beeri, Fagin, Maier and Yannakakis 1983). The hypergraph of $\bowtie[SP, PJ, JS]$ is a triangle, which is cyclic, and indeed no set of MVDs is equivalent to it.
- **Lossless decomposition.** A decomposition $(R_1, \ldots, R_k)$ of $U$ is lossless under $D$ exactly when $D$ implies $\bowtie[R_1, \ldots, R_k]$. See the [lossless join](/lossless-join-decomposition/) page.
- **Embedded JDs.** If $X_1 \cup \cdots \cup X_k$ is a proper subset of $U$, the JD is required only of the projection on that union. Such embedded dependencies behave differently, and the chase need not stop for them.
- **Ternary relationships.** A relationship set of degree three in the [ER model](/entity-relationship-model/) is in general not the join of its binary projections. When it is, the JD lets the designer replace it by binary relationships.

## References
