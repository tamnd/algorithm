---
tag: X1WTJN
kind: definition
slug: multivalued-dependency
name: Multivalued dependency
aliases:
- MVD
area: databases/relational-theory
level: core
summary: "X ->> Y holds when, for each value of X, the Y values and the values of the other attributes combine freely as a cross product."
prereqs: [functional-dependency, relational-algebra]
see_also: [fourth-normal-form, heaths-theorem, join-dependency, tuple-generating-dependency, chase-algorithm, armstrongs-axioms, lossless-join-decomposition, normalization]
sources:
  - paper: doi:10.1145/320557.320571
    title: Ronald Fagin, Multivalued dependencies and a new normal form for relational databases, ACM Transactions on Database Systems 2(3), 262 to 278 (1977)
    locator: the definition of multivalued dependencies, the lossless split into XY and XZ, and fourth normal form
  - paper: doi:10.1145/509404.509414
    title: Catriel Beeri, Ronald Fagin and John H. Howard, A complete axiomatization for functional and multivalued dependencies in database relations, Proceedings of the 1977 ACM SIGMOD International Conference on Management of Data, 47 to 61 (1977)
    locator: the inference rules for FDs and MVDs together and their completeness
  - paper: doi:10.1145/320613.320614
    title: Catriel Beeri, On the membership problem for functional and multivalued dependencies in relational databases, ACM Transactions on Database Systems 5(3), 241 to 259 (1980)
    locator: the dependency basis and a polynomial-time test for implication of FDs and MVDs
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 8 (functional and join dependency), multivalued dependencies, their inference rules and the chase
---

A multivalued dependency $X \twoheadrightarrow Y$ says that, within each group of tuples with the same $X$ value, the $Y$ values are independent of the values of the remaining attributes. It is the exact condition under which a relation splits without loss into two projections that share $X$, by [Heath's theorem](/heaths-theorem/) in Fagin's form. The [normalization](/normalization/) page uses MVDs only as the reason for 4NF, and [BCNF](/boyce-codd-normal-form/) sees only [functional dependencies](/functional-dependency/). This page defines MVDs, gives their equivalent forms and the rules for reasoning with them, and shows how they differ from FDs.

## Definition

Let $U$ be a finite set of attributes, let $X, Y \subseteq U$, and let $Z = U - XY$, where $XY$ means $X \cup Y$. We use set semantics: a relation over $U$ is a finite set of tuples.

**Definition (Fagin 1977).** A relation $r$ over $U$ *satisfies* the multivalued dependency $X \twoheadrightarrow Y$ if for any two tuples $u, v \in r$ with $u[X] = v[X]$, there is a tuple $w \in r$ with
$$w[XY] = u[XY] \quad\text{and}\quad w[Z] = v[Z].$$
Applied to the pair $(v, u)$ as well, the rule asks for both "swaps" of the $Y$ part and the $Z$ part of two tuples that agree on $X$.

**Equivalent forms.** For a relation $r$ over $U$, the following are equivalent:

1. $r$ satisfies $X \twoheadrightarrow Y$.
2. $r = \pi_{XY}(r) \bowtie \pi_{XZ}(r)$. This is Fagin's theorem, proved on the [Heath's theorem](/heaths-theorem/) page.
3. For each value $x$ of $X$ in $r$, with $r_x = \{t \in r : t[X] = x\}$, the set of pairs $\{(t[Y - X], t[Z]) : t \in r_x\}$ equals $\pi_{Y - X}(r_x) \times \pi_Z(r_x)$. The $Y$ values and the $Z$ values that occur with $x$ combine as a full cross product.

Form 2 says that an MVD is the [join dependency](/join-dependency/) $\bowtie[XY, XZ]$ with two components. Form 3 gives the name: $X$ determines a *set* of $Y$ values, not one value, and that set does not depend on the rest of the tuple.

**Trivial MVDs.** $X \twoheadrightarrow Y$ is *trivial* if $Y \subseteq X$ or $XY = U$. A trivial MVD holds in every relation over $U$: for $Y \subseteq X$ take $w = v$, and for $XY = U$ take $w = u$. Every other MVD fails in some relation with two tuples.

**Dependence on the whole schema.** Whether $X \twoheadrightarrow Y$ holds depends on $Z$, so on all of $U$, while an FD $X \to Y$ involves only the attributes in $XY$. If $r$ satisfies $X \twoheadrightarrow Y$ and $X \subseteq V \subseteq U$, then $\pi_V(r)$ satisfies $X \twoheadrightarrow Y \cap V$: restrict $u$, $v$ and $w$ to $V$. The other way fails: on $V = XY$ the MVD $X \twoheadrightarrow Y$ is trivial, so it holds in $\pi_{XY}(r)$ for every $r$, also when it fails in $r$. An MVD that is required only on a projection, $\pi_{XYW}(r) \models X \twoheadrightarrow Y$, is called an *embedded* MVD, and it is a different and harder kind of constraint.

## Examples and non-examples

- **Independent facts.** $\mathrm{CTB}(C, T, B)$ lists, for each course, its teachers and its textbooks, which are chosen independently. The relation
  $$\{(\mathit{db}, \mathit{Smith}, \mathit{Ullman}),\ (\mathit{db}, \mathit{Smith}, \mathit{Date}),\ (\mathit{db}, \mathit{Jones}, \mathit{Ullman}),\ (\mathit{db}, \mathit{Jones}, \mathit{Date})\}$$
  satisfies $C \twoheadrightarrow T$ and, by complementation, $C \twoheadrightarrow B$. No nontrivial FD holds. Each teacher is stored once for each book, which is the redundancy that [4NF](/fourth-normal-form/) removes.
- **Non-example: one tuple missing.** Remove $(\mathit{db}, \mathit{Jones}, \mathit{Date})$. Then $u = (\mathit{db}, \mathit{Jones}, \mathit{Ullman})$ and $v = (\mathit{db}, \mathit{Smith}, \mathit{Date})$ agree on $C$, but no tuple has Jones with Date, so $C \twoheadrightarrow T$ fails, and so does $C \twoheadrightarrow B$.
- **Every FD is an MVD.** If $r$ satisfies $X \to Y$ and $u[X] = v[X]$, then $w = v$ has $w[Y] = u[Y]$, so $r$ satisfies $X \twoheadrightarrow Y$. The converse fails, as $\mathrm{CTB}$ shows.
- **A larger right side does not give a smaller one.** Over $U = ABCD$, the relation
  $$\{(a, b_1, c_1, d_1),\ (a, b_2, c_2, d_2),\ (a, b_1, c_1, d_2),\ (a, b_2, c_2, d_1)\}$$
  satisfies $A \twoheadrightarrow BC$ and $A \twoheadrightarrow D$, but not $A \twoheadrightarrow B$ and not $A \twoheadrightarrow C$: the first two tuples would need $(a, b_1, c_2, d_2)$. For FDs, $A \to BC$ implies $A \to B$. For MVDs this *decomposition* rule fails. Its projection on $ABD$ does satisfy $A \twoheadrightarrow B$, as the rule for projections says.
- **Trivial cases.** $AB \twoheadrightarrow A$ and $A \twoheadrightarrow BCD$ over $ABCD$ hold in every relation.

## Related definitions

- **Inference rules (Beeri, Fagin and Howard 1977).** With $Z = U - XY$, the rules below, together with [Armstrong's axioms](/armstrongs-axioms/) for FDs, are sound and complete for implication of FDs and MVDs together:
  - *complementation:* from $X \twoheadrightarrow Y$ infer $X \twoheadrightarrow U - XY$;
  - *reflexivity:* if $Y \subseteq X$, infer $X \twoheadrightarrow Y$;
  - *augmentation:* from $X \twoheadrightarrow Y$ and $V \subseteq W$ infer $XW \twoheadrightarrow YV$;
  - *transitivity:* from $X \twoheadrightarrow Y$ and $Y \twoheadrightarrow W$ infer $X \twoheadrightarrow W - Y$;
  - *replication:* from $X \to Y$ infer $X \twoheadrightarrow Y$;
  - *coalescence:* from $X \twoheadrightarrow Y$, $W \to V$, $V \subseteq Y$ and $W \cap Y = \emptyset$ infer $X \to V$.

  From these follow the *union*, *intersection* and *difference* rules: from $X \twoheadrightarrow Y$ and $X \twoheadrightarrow W$ infer $X \twoheadrightarrow YW$, $X \twoheadrightarrow Y \cap W$ and $X \twoheadrightarrow Y - W$.
- **Dependency basis (Beeri 1980).** For a set $D$ of FDs and MVDs and a set $X$, the sets $Y$ with $D \models X \twoheadrightarrow Y$ are closed under union, intersection and difference, so the sets $Y - X$ among them are the unions of the blocks of one partition of $U - X$. This partition is the *dependency basis* of $X$. Beeri computes it in polynomial time, which decides implication of an MVD or an FD by $D$. The [chase](/chase-algorithm/) decides the same question with a tableau.
- **Join dependency.** An MVD is the two-component case of a [join dependency](/join-dependency/). Some relations are the join of three projections but satisfy no nontrivial MVD.
- **Tuple-generating dependency.** An MVD asks for a tuple $w$ built from $u$ and $v$, so it is a full [tuple-generating dependency](/tuple-generating-dependency/). An FD asks for equal values, so it is an [equality-generating dependency](/equality-generating-dependency/).
- **Fourth normal form.** A schema is in [4NF](/fourth-normal-form/) if the left side of each nontrivial MVD that holds is a superkey.

## References
