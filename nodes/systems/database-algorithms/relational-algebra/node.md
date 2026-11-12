---
tag: NEME20
kind: definition
slug: relational-algebra
name: Relational algebra
aliases:
- relational operators
- Codd's relational algebra
area: systems/database-algorithms
level: intro
summary: "The query language of six operators on relations: selection, projection, renaming, union, difference and product. Join, intersection and division are derived from them."
prereqs: [relational-model]
see_also: [relational-join, predicate-pushdown, query-optimization, semijoin, datalog, query-containment-problem, join-ordering]
sources:
  - paper: "E. F. Codd, Relational completeness of data base sublanguages, in R. Rustin (ed.), Data Base Systems, Courant Computer Science Symposia 6, Prentice-Hall (1972), 65 to 98"
    locator: the definition of the algebra and of the calculus, and the reduction algorithm from the calculus to the algebra
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Section 4.4 (the SPJR algebra and conjunctive queries), Section 5.1 (the relational algebras), Sections 5.3 and 5.4 (the calculus, domain independence and the equivalence theorem)
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson (2008)
    locator: Section 2.4 (an algebraic query language) and Chapter 16 (algebraic laws for improving query plans)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: Chapter 4 (relational algebra and calculus)
  - paper: doi:10.1145/362384.362685
    title: E. F. Codd, A relational model of data for large shared data banks, Communications of the ACM 13(6), 377 to 387 (1970)
    locator: Section 2.1 (permutation, projection, join, composition and restriction)
---

The relational algebra is a set of operators that take [relations](/relational-model/) as input and return a relation. The six basic operators are selection, projection, renaming, union, difference and Cartesian product, and the natural [join](/relational-join/), intersection and division are derived from them. Codd defined the algebra in 1972 and proved that it can express each query of the relational calculus, so it is the reference for the expressive power of a query language. Database systems translate SQL into a tree of these operators and then rewrite the tree with algebraic laws.

## Definition

We use the named perspective of the [relational model](/relational-model/). A relation $r$ over a finite attribute set $U$ is a finite set of tuples, and each tuple is a function from $U$ to values. For $X \subseteq U$, $t[X]$ is the restriction of $t$ to $X$. Let $r$ be over $U$ and $s$ be over $V$.

A *selection condition* $\theta$ over $U$ is built from atoms $A = B$, $A = c$, $A < B$ and $A < c$, with $A, B \in U$ and $c$ a constant, by $\wedge$, $\vee$ and $\neg$.

The six basic operators are:

| operator | condition | schema of the result | value |
| --- | --- | --- | --- |
| selection $\sigma_\theta(r)$ | $\theta$ over $U$ | $U$ | $\{ t \in r : t \text{ satisfies } \theta \}$ |
| projection $\pi_X(r)$ | $X \subseteq U$ | $X$ | $\{ t[X] : t \in r \}$ |
| renaming $\rho_f(r)$ | $f : U \to W$ a bijection | $W$ | $\{ t \circ f^{-1} : t \in r \}$ |
| union $r \cup s$ | $U = V$ | $U$ | the set union |
| difference $r - s$ | $U = V$ | $U$ | the set difference |
| product $r \times s$ | $U \cap V = \emptyset$ | $U \cup V$ | $\{ t : t[U] \in r,\ t[V] \in s \}$ |

An *expression* is a term built from relation names and constant relations with these operators. On a database instance, each relation name denotes its relation, and the expression denotes the relation that the operators compute. Each operator returns a relation, so the operators compose without limit. This is the *closure* property of the algebra.

### Derived operators

- **Natural join.** $r \bowtie s = \{ t \text{ over } U \cup V : t[U] \in r,\ t[V] \in s \}$. Let $C = U \cap V = \{A_1, \ldots, A_k\}$, and let $f$ rename each $A_i$ in $V$ to a new name $A_i'$. Then $r \bowtie s = \rho_g\big(\pi_{U \cup f(V) - \{A'_1, \ldots, A'_k\}}(\sigma_{A_1 = A_1' \wedge \cdots \wedge A_k = A_k'}(r \times \rho_f(s)))\big)$, with $g$ the identity. If $C = \emptyset$, the join is the product. If $U = V$, the join is the intersection.
- **Theta join.** $r \bowtie_\theta s = \sigma_\theta(r \times s)$ for disjoint schemas.
- **Intersection.** $r \cap s = r - (r - s)$.
- **Division.** For $V \subseteq U$ and $X = U - V$, $r \div s = \{ x : x \times s \subseteq r \}$, the $X$-values that occur in $r$ with every tuple of $s$. It equals $\pi_X(r) - \pi_X\big((\pi_X(r) \times s) - r\big)$.
- **Semijoin.** $r \ltimes s = \pi_U(r \bowtie s)$, the tuples of $r$ that join with some tuple of $s$. See [semijoin](/semijoin/).

### Sizes

For relations of $N$ and $M$ tuples: $|\sigma_\theta(r)| \le N$, $|\pi_X(r)| \le N$, $|r \cup s| \le N + M$, $|r - s| \le N$, $|r \times s| = NM$ and $|r \bowtie s| \le NM$. The bound for the join is tight: if all tuples of both relations have the same value on $U \cap V$, the join has $NM$ tuples.

### Monotonicity

An operator is *monotone* if $r \subseteq r'$ and $s \subseteq s'$ give $\mathrm{op}(r, s) \subseteq \mathrm{op}(r', s')$. Selection, projection, renaming, union and product are monotone. Selection is monotone even with $\neg$ in the condition, because it keeps or drops each tuple on its own. A composition of monotone operators is monotone. Difference is not monotone: $\{t\} - \emptyset = \{t\}$, but $\{t\} - \{t\} = \emptyset$. So no expression without difference is equal to $r - s$ on all instances, and difference is necessary.

### Algebraic laws

These equations hold for all relations with the stated schemas. A query optimizer uses them to rewrite a plan into a cheaper equivalent plan.

1. $\sigma_{\theta_1}(\sigma_{\theta_2}(r)) = \sigma_{\theta_1 \wedge \theta_2}(r) = \sigma_{\theta_2}(\sigma_{\theta_1}(r))$.
2. $\pi_X(\pi_Y(r)) = \pi_X(r)$ for $X \subseteq Y \subseteq U$. With $X = Y$, projection is idempotent.
3. $\sigma_\theta(r \bowtie s) = \sigma_\theta(r) \bowtie s$ if $\theta$ uses only attributes of $U$. This is [predicate pushdown](/predicate-pushdown/).
4. $r \bowtie s = s \bowtie r$ and $(r \bowtie s) \bowtie q = r \bowtie (s \bowtie q)$. So the join order is free, which [join ordering](/join-ordering/) uses.
5. $\sigma_\theta(r \cup r') = \sigma_\theta(r) \cup \sigma_\theta(r')$ and $\sigma_\theta(r - r') = \sigma_\theta(r) - \sigma_\theta(r')$.
6. $\pi_X(r \cup r') = \pi_X(r) \cup \pi_X(r')$.
7. $\pi_X(r) - \pi_X(r') \subseteq \pi_X(r - r')$. The inclusion can be strict (see the non-example below).

*Proof of law 3.* Let $t$ be over $U \cup V$. Then $t \in \sigma_\theta(r \bowtie s)$ if and only if $t[U] \in r$, $t[V] \in s$ and $t$ satisfies $\theta$. Since $\theta$ uses only attributes of $U$, $t$ satisfies $\theta$ if and only if $t[U]$ does. So the condition is $t[U] \in \sigma_\theta(r)$ and $t[V] \in s$, which defines $\sigma_\theta(r) \bowtie s$. $\square$

## Examples and non-examples

**A database.** Take $\mathrm{Emp}(\mathit{Name}, \mathit{Dept}, \mathit{Salary})$ and $\mathrm{Dept}(\mathit{Dept}, \mathit{Building})$:

| Name | Dept | Salary |
| --- | --- | --- |
| Ann | R&D | 70 |
| Bob | R&D | 50 |
| Cid | Sales | 60 |
| Dee | HR | 40 |

| Dept | Building |
| --- | --- |
| R&D | B1 |
| Sales | B2 |
| Ops | B2 |

- $\mathrm{Emp} \bowtie \mathrm{Dept}$ has 3 tuples: (Ann, R&D, 70, B1), (Bob, R&D, 50, B1) and (Cid, Sales, 60, B2). Dee has no department tuple, and Ops has no employee, so they do not occur.
- $\pi_{\mathit{Name}}(\sigma_{\mathit{Salary} > 55}(\mathrm{Emp} \bowtie \mathrm{Dept})) = \{\text{Ann}, \text{Cid}\}$. By law 3, the selection can run before the join, on 4 tuples instead of 3 joined tuples. On large relations this order reads much less data.
- $\pi_{\mathit{Dept}}(\mathrm{Dept}) - \pi_{\mathit{Dept}}(\mathrm{Emp}) = \{\text{Ops}\}$: the departments with no employee. This query needs difference, because it is not monotone: a new employee in Ops removes Ops from the answer.
- $\mathrm{Emp} \times \rho_{\mathit{Dept} \to \mathit{D2}}(\mathrm{Dept})$ has $4 \cdot 3 = 12$ tuples. The renaming is necessary, because the two schemas share $\mathit{Dept}$.

**Division.** Let $\mathrm{Takes}(S, C)$ hold (ann, db), (ann, os), (bob, db), (cid, os), (cid, db), (cid, ai), and let $\mathrm{Req}(C)$ hold db and os. Then $\mathrm{Takes} \div \mathrm{Req} = \{\text{ann}, \text{cid}\}$: the students who take every required course. Bob takes only db. If $\mathrm{Req}$ is empty, every student in $\mathrm{Takes}$ is in the answer.

**Non-example: projection and difference.** Let $r = \{(A{=}1, B{=}1)\}$ and $s = \{(A{=}1, B{=}2)\}$. Then $\pi_A(r - s) = \{1\}$, but $\pi_A(r) - \pi_A(s) = \emptyset$. So projection does not distribute over difference, and an optimizer must not push a projection through a difference.

**Non-example: union of different schemas.** $\mathrm{Emp} \cup \mathrm{Dept}$ is not defined, because the schemas differ. Union and difference need equal schemas; product needs disjoint schemas.

**Non-example: transitive closure.** For a binary relation $E(\mathit{From}, \mathit{To})$, no expression of the algebra computes the set of pairs joined by a path of any length (Aho and Ullman 1979). Each expression has a fixed number of joins, so it follows paths of bounded length only. [Datalog](/datalog/) adds recursion for this, and [transitive closure](/transitive-closure/) covers the graph algorithms.

**Non-example: SQL bags.** In SQL, `SELECT Dept FROM Emp` returns R&D twice. The projection $\pi_{\mathit{Dept}}(\mathrm{Emp})$ returns it once. SQL's semantics is a *bag* algebra, and the laws above change in it: for example, $r \cup r = r$ holds for sets and fails for bags.

## Related definitions

- **Relational calculus and Codd's theorem.** The domain relational calculus writes a query as $\{ (x_1, \ldots, x_k) \mid \varphi \}$ with $\varphi$ a first-order formula over the relations. A query is *domain independent* if its answer does not depend on the domain of values, only on the database. *Codd's theorem*: the relational algebra and the domain-independent relational calculus express exactly the same queries. Codd (1972) gave a reduction from his calculus to the algebra. Domain independence is undecidable, so practical languages use a syntactic restriction, the safe-range formulas, which keeps the same expressive power (Abiteboul, Hull and Vianu, Section 5.4). A language that can express all these queries is called *relationally complete*.
- **Conjunctive queries.** The fragment of selection with equality atoms joined by $\wedge$, projection, natural join and renaming (the SPJR algebra) expresses exactly the conjunctive queries. Their containment is NP-complete: see the [query containment problem](/query-containment-problem/) and the [Chandra-Merlin theorem](/chandra-merlin-theorem/).
- **Join.** The [relational join](/relational-join/) pages cover the algorithms that compute $r \bowtie s$, from [nested-loop join](/nested-loop-join/) to [hash join](/hash-join/).
- **Query optimization.** [Query optimization](/query-optimization/) searches the space of expressions equal to a given one, with the laws above, and picks the cheapest under a [cost model](/cost-model/).
- **Datalog.** [Datalog](/datalog/) is the language of recursive rules. Its nonrecursive part with negation expresses the same queries as the algebra.

## References
