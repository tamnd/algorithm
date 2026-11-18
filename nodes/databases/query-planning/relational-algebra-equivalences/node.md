---
tag: 00WBVB
kind: theorem
slug: relational-algebra-equivalences
name: Equivalence rules of relational algebra
aliases:
- algebraic laws of query rewriting
area: databases/query-planning
level: core
summary: "Laws such as join commutativity, associativity and the pushing of selections and projections, which let an optimizer rewrite a plan. Some hold for sets only, others for sets and bags."
prereqs: [relational-algebra]
see_also: [predicate-pushdown, semijoin, provenance-semirings, sql-null-semantics, join-ordering, query-optimization, eager-aggregation, subquery-unnesting]
sources:
  - book: isbn:9780131873254
    title: "Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems: The Complete Book, second edition, Pearson Prentice Hall (2009)"
    locator: "Section 16.2, Algebraic laws for improving query plans (commutative and associative laws, laws involving selection, pushing selections, laws involving projection, laws about joins and products, laws involving duplicate elimination)"
  - paper: doi:10.1145/1265530.1265535
    title: "Todd J. Green, Grigoris Karvounarakis and Val Tannen, Provenance semirings, Proceedings of the 26th ACM Symposium on Principles of Database Systems (PODS), 31 to 40 (2007)"
    locator: "K-relations, with the Boolean semiring for sets and the natural numbers for bags, and the commutation of positive queries with semiring homomorphisms"
  - paper: doi:10.1145/362384.362685
    title: "Edgar F. Codd, A relational model of data for large shared data banks, Communications of the ACM 13(6), 377 to 387 (1970)"
    locator: the operations on relations
---

The equivalence rules of relational algebra are equations between two algebra expressions that hold on every database. An optimizer uses them to rewrite a [query plan](/query-plan/) into a cheaper plan with the same result: it moves selections and projections down, reorders joins and turns subqueries into joins. This page states the laws as one theorem. For each law it says whether it holds under set semantics, under bag semantics (the semantics of SQL) or under both, and it gives the side conditions, and the proof section proves each law. [Predicate pushdown](/predicate-pushdown/) is the rewrite strategy that applies the selection laws of this page to a plan; that page describes the strategy, and this page holds the laws and their proofs.

## Statement

**Relations.** A relation $R$ over a finite set $A$ of attributes is a function from tuples over $A$ to the natural numbers: $R(t)$ is the number of copies of $t$ in $R$. Under *bag semantics* any number is allowed. Under *set semantics* every value is 0 or 1. Write $[P]$ for 1 if the statement $P$ is true and 0 if it is false, and $\delta(R)(t) = \min(1, R(t))$ for duplicate elimination. Below, $R$, $S$ and $T$ are relations over $A$, $B$ and $C$, and $J = A \cap B$. A condition $\theta$ is TRUE or FALSE on each tuple, except in law 3, which treats the value UNKNOWN of SQL.

**Operators under bag semantics.** For tuples $t$, $u$ and $w$ over the right attributes:

- $\sigma_\theta(R)(t) = R(t) \cdot [\theta(t)]$, and $\pi_D(R)(u) = \sum_{t : t[D] = u} R(t)$ for $D \subseteq A$.
- $(R \bowtie S)(w) = R(w[A]) \cdot S(w[B])$ for $w$ over $A \cup B$. The product $R \times S$ is the case $J = \emptyset$, and $R \bowtie_\theta S = \sigma_\theta(R \times S)$.
- For $R$ and $S$ over the same attributes: $(R \cup S)(t) = R(t) + S(t)$, which is UNION ALL; $(R \cap S)(t) = \min(R(t), S(t))$; and $(R - S)(t) = \max(0, R(t) - S(t))$, the *monus*, which is EXCEPT ALL.
- $(R \ltimes S)(t) = R(t) \cdot [\text{some } s \text{ with } S(s) > 0 \text{ has } s[J] = t[J]]$, the [semijoin](/semijoin/).

**Operators under set semantics.** They are the same functions on relations with values 0 and 1, except that union and projection apply $\delta$ to the result: $R \cup S = \delta(R + S)$ and $\pi_D(R) = \delta$ of the sum above. On values 0 and 1 the monus is the set difference.

Two expressions are *equivalent* under a semantics if they have the same attributes and give the same relation on every database of that semantics. Attributes have names, so the order of the columns does not matter.

**Theorem.** The following equivalences hold under the semantics and the side conditions given.

| law | equivalence | side condition | holds under |
|---|---|---|---|
| 1 | $\sigma_{\theta_1 \wedge \theta_2}(R) = \sigma_{\theta_1}(\sigma_{\theta_2}(R)) = \sigma_{\theta_2}(\sigma_{\theta_1}(R))$ | none | both |
| 2 | $\sigma_{\theta_1 \vee \theta_2}(R) = \sigma_{\theta_1}(R) \cup \sigma_{\theta_2}(R)$ | none | sets only |
| 3 | $\sigma_{\neg\theta}(R) = R - \sigma_\theta(R)$ | $\theta$ is never UNKNOWN on a tuple of $R$ | both |
| 4 | $\sigma_\theta(R \times S) = R \bowtie_\theta S$ | $J = \emptyset$ | both |
| 5 | $\sigma_\theta(R \bowtie S) = \sigma_\theta(R) \bowtie S$, and the same for $\bowtie_\varphi$ and $\times$ | $\theta$ reads only attributes in $A$ | both |
| 6 | $\sigma_\theta(R \circ S) = \sigma_\theta(R) \circ \sigma_\theta(S)$ for $\circ$ in $\cup, \cap, -$, and $\sigma_\theta(R - S) = \sigma_\theta(R) - S$ | $A = B$ | both |
| 7 | $\pi_D(\pi_E(R)) = \pi_D(R)$ | $D \subseteq E \subseteq A$ | both |
| 8 | $\pi_D(\sigma_\theta(R)) = \sigma_\theta(\pi_D(R))$ | $\theta$ reads only attributes in $D$ | both |
| 9 | $\pi_L(R \bowtie S) = \pi_L(\pi_{L_R}(R) \bowtie \pi_{L_S}(S))$ | $L \subseteq A \cup B$, $L_R = (L \cap A) \cup J$, $L_S = (L \cap B) \cup J$ | both |
| 10 | $\pi_D(R \cup S) = \pi_D(R) \cup \pi_D(S)$ | $A = B$ | both |
| 11 | $\pi_D(R - S) = \pi_D(R) - \pi_D(S)$ | $A = B$, and no two different tuples with a positive value in $R$ or in $S$ agree on $D$ | both |
| 12 | $R \bowtie S = S \bowtie R$, and the same for $\times$, $\cup$ and $\cap$ | none | both |
| 13 | $(R \bowtie S) \bowtie T = R \bowtie (S \bowtie T)$, and the same for $\times$, $\cup$ and $\cap$ | none | both |
| 14 | $(R \bowtie_{\theta_1} S) \bowtie_{\theta_2} T = R \bowtie_{\theta_1} (S \bowtie_{\theta_2} T)$ | $A$, $B$, $C$ pairwise disjoint, $\theta_1$ reads only $A \cup B$, $\theta_2$ reads only $B \cup C$ | both |
| 15 | $R \bowtie (S \cup T) = (R \bowtie S) \cup (R \bowtie T)$ | $B = C$ | both |
| 16 | $R \bowtie (S - T) = (R \bowtie S) - (R \bowtie T)$ | $B = C$ | both |
| 17 | $R \cup R = R$ | none | sets only |
| 18 | $R \cap (S \cup T) = (R \cap S) \cup (R \cap T)$ | $A = B = C$ | sets only |
| 19 | $(R \cup S) - T = (R - T) \cup (S - T)$ | $A = B = C$ | sets only |
| 20 | $R \ltimes S = \pi_A(R \bowtie S)$ | none | sets only |
| 21 | $R \ltimes S = R \bowtie \delta(\pi_J(S))$ | none | both |

"Sets only" means that the law holds under set semantics and fails under bag semantics. Law 11 fails under both semantics without its side condition. Moreover (law 22, transfer): if two expressions use only $\sigma$, $\pi$, $\times$, $\bowtie$, $\cup$ and $\cap$, and they are equivalent under bag semantics, then they are equivalent under set semantics.

## In plain words

A database can compute the same answer in many ways. The laws on this page say which changes to a query never change the answer, on any data. Two kinds matter most. A filter can move down, closer to the tables, so that the later steps see fewer rows. And the joins can be done in any order. An optimizer applies the laws again and again to find a cheaper form of the same query.

SQL tables can hold the same row twice. Some laws that are true for sets of rows are then false. For example, if you put a list of rows together with itself and keep the copies, every row is there twice, so the result is not the list you started with. So each law here says if it is true for sets, for tables with copies, or for both.

## Proof

Under set semantics, the operators $\sigma$, $\times$, $\bowtie$, $\cap$, $-$ and $\ltimes$ are the bag operators restricted to relations with values 0 and 1, and they give such relations again. So a proof of a law in these operators under bag semantics is also a proof under set semantics. For the laws with $\cup$ or $\pi$ and no difference, law 22 gives the set case from the bag case. The other set cases are proved directly. Below, $t$ is a tuple over $A$, $x$ a tuple over $A$, $y$ a tuple over $B$, and $w$ a tuple over all attributes of the expression.

**Law 22.** First, $\delta$ commutes with each positive operator, in the sense $\delta(\mathrm{op}_{\text{bag}}(R, S)) = \mathrm{op}_{\text{set}}(\delta R, \delta S)$. For selection, $[R(t)[\theta(t)] > 0] = [R(t) > 0][\theta(t)]$. For join and product, $[R(x) S(y) > 0] = [R(x) > 0] \cdot [S(y) > 0]$. For union, $[R(t) + S(t) > 0] = \max([R(t) > 0], [S(t) > 0])$, which is the set union of $\delta R$ and $\delta S$. For projection, a sum of natural numbers is positive exactly when one of its terms is positive, so $\delta(\pi_D(R)) = \delta(\pi_D(\delta R))$, the set projection of $\delta R$. For intersection, $[\min(R(t), S(t)) > 0] = \min([R(t) > 0], [S(t) > 0])$. By induction on the expression, $\delta(E_{\text{bag}}(D)) = E_{\text{set}}(\delta D)$ for every positive expression $E$ and every database $D$. If $D$ is a set database, then $\delta D = D$, so $E_{1,\text{set}}(D) = \delta(E_{1,\text{bag}}(D)) = \delta(E_{2,\text{bag}}(D)) = E_{2,\text{set}}(D)$. Difference does not commute with $\delta$: for $R = \{t, t\}$ and $S = \{t\}$, $\delta(R - S) = \{t\}$ but $\delta R - \delta S = \emptyset$. So the law needs the restriction to positive expressions.

**Law 1.** $[\theta_1(t) \wedge \theta_2(t)] = [\theta_1(t)] \cdot [\theta_2(t)]$, and multiplication is commutative. In SQL a conjunction is TRUE exactly when both parts are TRUE, and selection keeps a tuple exactly when its condition is TRUE, so the law also holds with UNKNOWN.

**Law 2.** Under sets, $R(t) \in \{0, 1\}$ and $[\theta_1 \vee \theta_2] = \max([\theta_1], [\theta_2])$, so the left side is $R(t) \max([\theta_1(t)], [\theta_2(t)])$, which is $\delta(R(t)[\theta_1(t)] + R(t)[\theta_2(t)])$, the right side. Under bags, take $R = \{t\}$ with $\theta_1(t)$ and $\theta_2(t)$ both true: the left side holds $t$ once and the right side twice.

**Law 3.** $\max(0, R(t) - R(t)[\theta(t)]) = R(t)(1 - [\theta(t)]) = R(t)[\neg\theta(t)]$, because $\theta(t)$ is TRUE or FALSE. If $\theta(t)$ is UNKNOWN, then $\neg\theta(t)$ is UNKNOWN too, so $t$ is in neither $\sigma_\theta(R)$ nor $\sigma_{\neg\theta}(R)$, and the right side keeps $t$ while the left side drops it.

**Law 4.** This is the definition of $\bowtie_\theta$.

**Law 5.** The left side at $w$ is $R(w[A]) S(w[B]) [\theta(w)]$. Because $\theta$ reads only attributes in $A$, $\theta(w) = \theta(w[A])$, so this equals $R(w[A])[\theta(w[A])] \cdot S(w[B])$, the right side. A join condition $\varphi$ adds the same factor $[\varphi(w)]$ to both sides.

**Law 6.** $[\theta](R + S) = [\theta]R + [\theta]S$ and $[\theta] \min(R, S) = \min([\theta]R, [\theta]S)$. Because $[\theta]$ is 0 or 1, $[\theta] \max(0, R - S) = \max(0, [\theta]R - [\theta]S)$, and this also equals $\max(0, [\theta]R - S)$: if $[\theta] = 1$ the two are the same, and if $[\theta] = 0$ both are 0. The case of $\cup$ under sets follows by law 22, and the other cases are among the operators that sets and bags share.

**Law 7.** $\pi_D(\pi_E(R))(u) = \sum_{v : v[D] = u} \sum_{t : t[E] = v} R(t) = \sum_{t : t[D] = u} R(t)$, because $D \subseteq E$ gives $t[D] = (t[E])[D]$, so each $t$ is counted once. Law 22 gives the set case.

**Law 8.** If $t[D] = u$, then $\theta(t) = \theta(u)$, because $\theta$ reads only attributes in $D$. So $\sum_{t : t[D] = u} R(t)[\theta(t)] = [\theta(u)] \sum_{t : t[D] = u} R(t)$. Law 22 gives the set case.

**Law 9.** Write $R' = \pi_{L_R}(R)$ and $S' = \pi_{L_S}(S)$, and let $z$ be a tuple over $L_R \cup L_S$. Then $(R' \bowtie S')(z) = \sum_{x, y} R(x) S(y)$ over the $x$ with $x[L_R] = z[L_R]$ and the $y$ with $y[L_S] = z[L_S]$. Each such pair agrees on $J$, because $J \subseteq L_R \cap L_S$ and both agree with $z$ there, so it forms one tuple $w$ over $A \cup B$ with $w[L_R \cup L_S] = z$. Each such $w$ comes from exactly one pair, $x = w[A]$ and $y = w[B]$. So $R' \bowtie S' = \pi_{L_R \cup L_S}(R \bowtie S)$. Since $L \subseteq L_R \cup L_S$, law 7 gives $\pi_L(R' \bowtie S') = \pi_L(R \bowtie S)$. Law 22 gives the set case.

**Law 10.** A sum over the $t$ with $t[D] = u$ of $R(t) + S(t)$ splits into two sums. Law 22 gives the set case.

**Law 11.** By the side condition, for each tuple $u$ over $D$ at most one tuple $t$ with $t[D] = u$ has a positive value in $R$ or in $S$. If there is none, both sides are 0 at $u$. Otherwise both sides are $\max(0, R(t) - S(t))$. The same computation with values 0 and 1 is the set case. Without the condition the law fails under both semantics: for $R = \{(1, 2)\}$ and $S = \{(1, 3)\}$ over $(a, b)$ and $D = \{a\}$, $\pi_a(R - S) = \{(1)\}$, but $\pi_a(R) - \pi_a(S) = \emptyset$.

**Laws 12 and 13.** The two sides of each law are the products $R(w[A]) S(w[B])$ and $R(w[A]) S(w[B]) T(w[C])$, the sums or the minimums of the same numbers, grouped or ordered in another way. Multiplication, addition and the minimum are commutative and associative. Law 22 gives the case of $\cup$ under sets.

**Law 14.** By law 4 and law 5 (with $\theta_1$ on the left input $R \times S$), the left side is $\sigma_{\theta_2}(\sigma_{\theta_1}(R \times S) \times T) = \sigma_{\theta_2}(\sigma_{\theta_1}(R \times S \times T))$. By law 5 and law 12 (with $\theta_2$ on the right input $S \times T$), the right side is $\sigma_{\theta_1}(\sigma_{\theta_2}(R \times S \times T))$. Law 1 makes the two equal. The side conditions are what makes $\theta_1$ readable on $R \times S$ and $\theta_2$ readable on $S \times T$.

**Law 15.** $R(x)(S(y) + T(y)) = R(x)S(y) + R(x)T(y)$. Law 22 gives the set case.

**Law 16.** Because $R(x) \ge 0$, $R(x) \max(0, S(y) - T(y)) = \max(0, R(x)S(y) - R(x)T(y))$.

**Law 17.** Under sets, $\delta(R + R) = R$ when the values of $R$ are 0 and 1. Under bags, $(R \cup R)(t) = 2R(t)$, which differs from $R(t)$ when $R(t) > 0$.

**Law 18.** Under sets, the law is the distributive law of AND over OR at each tuple. Under bags, take $R = S = T = \{t\}$: the left side is $\min(1, 2) = 1$ copy and the right side is $1 + 1 = 2$ copies.

**Law 19.** Under sets, $(r \vee s) \wedge \neg u = (r \wedge \neg u) \vee (s \wedge \neg u)$ at each tuple. Under bags, take $R = S = T = \{t\}$: the left side is $\max(0, 2 - 1) = 1$ copy and the right side is $0 + 0 = 0$ copies.

**Law 20.** Under bags, $\pi_A(R \bowtie S)(t) = R(t) \cdot \sum_{y : y[J] = t[J]} S(y)$, so each copy of $t$ is repeated once for each match. Under sets this value is positive exactly when $R(t) = 1$ and some match exists, which is $(R \ltimes S)(t)$. For bags, take $R = \{(1)\}$ over $a$ and $S = \{(1, 5), (1, 6)\}$ over $(a, c)$: $\pi_a(R \bowtie S)$ holds $(1)$ twice, and $R \ltimes S$ holds it once.

**Law 21.** Since $J \subseteq A$, the join has the attributes $A$, and $(R \bowtie \delta(\pi_J(S)))(t) = R(t) \cdot [\pi_J(S)(t[J]) > 0]$. The sum $\pi_J(S)(t[J])$ is positive exactly when some $s$ with $S(s) > 0$ has $s[J] = t[J]$, so this is $(R \ltimes S)(t)$. With values 0 and 1 it is the set case. $\square$

## Consequences

- **Predicate pushdown.** Laws 1, 5, 6 and 8 move a selection below joins, unions and projections, and law 4 turns a selection over a product into a join. They hold under both semantics, so they are safe for SQL. [Predicate pushdown](/predicate-pushdown/) applies them to plans, also through outer joins on the preserved side, which needs rules that are not on this page.
- **Join reordering.** By laws 12 and 13, all join trees over the same relations give the same result, under bags too. This is why the [join ordering](/join-ordering/) problem can choose the tree by cost alone. Law 14 says that a theta-join condition must move with the relations it reads.
- **Narrow rows.** Law 9 lets a plan drop the columns that no later operator reads, as soon as each relation is read, if it keeps the join columns.
- **OR under bags.** Law 2 fails under bags, but $\sigma_{\theta_1 \vee \theta_2}(R) = \sigma_{\theta_1}(R) \cup \sigma_{\neg\theta_1 \wedge \theta_2}(R)$ holds under both semantics for conditions that are TRUE or FALSE, because $[\theta_1 \vee \theta_2] = [\theta_1] + [\neg\theta_1 \wedge \theta_2]$. In SQL, write the second condition with $\theta_1$ IS NOT TRUE in place of NOT $\theta_1$.
- **Semijoins.** Law 21 is the rewrite of EXISTS into a join with the distinct join values of the inner table, as in [subquery unnesting](/subquery-unnesting/). Law 20 is right only after duplicate elimination, so a plan for SQL must use law 21.
- **Example.** Take $R(a, b) = \{(1, 10), (1, 10), (2, 20)\}$ and $S(b, c) = \{(10, x), (20, y), (20, z)\}$ as bags. Then $R \bowtie S$ holds $(1, 10, x)$ twice, $(2, 20, y)$ and $(2, 20, z)$. Selecting $a = 1$ gives $(1, 10, x)$ twice, and so does $\sigma_{a=1}(R) \bowtie S$, as law 5 says. $R \ltimes S$ is $R$ itself. $\pi_{a,b}(R \bowtie S)$ holds $(1, 10)$ twice and $(2, 20)$ twice, which is not $R$, as law 20 says. $\delta(\pi_b(S)) = \{(10), (20)\}$ and $R \bowtie \delta(\pi_b(S)) = R$, as law 21 says.

## Tightness

- **Sets and bags.** Laws 2, 17, 18, 19 and 20 hold under sets and fail under bags, by the examples in the proof. So law 22 has no converse: a law that holds under sets need not hold under bags. Law 22 also fails for expressions with difference, by the example in its proof.
- **Side conditions.** Law 11 fails without its condition under both semantics. Law 3 fails when the condition can be UNKNOWN: for $R = \{(\mathrm{NULL})\}$ over $a$ and $\theta$ equal to $a = 1$, $\sigma_{\neg\theta}(R) = \emptyset$, but $R - \sigma_\theta(R) = R$. In laws 5, 8 and 14 the side condition is what makes the right side defined.
- **Outer joins.** Joins and outer joins do not reassociate freely. For $R(a) = \{(1)\}$, $S(a, b) = \emptyset$ and $T(b) = \{(5)\}$, $R$ LEFT JOIN $(S \bowtie T)$ is $\{(1, \mathrm{NULL})\}$. But $R$ LEFT JOIN $S$ is $\{(1, \mathrm{NULL})\}$, and its join with $T$ is empty, because NULL = 5 is not TRUE.
- **Aggregation.** No law on this page moves a grouping. That needs its own conditions, given on [eager aggregation](/eager-aggregation/).

## History

Codd (1970) defined the operations of the relational model on sets of tuples. Textbooks list the algebraic laws that optimizers use; Garcia-Molina, Ullman and Widom give them in Section 16.2 of their book, with the laws for selections, projections, joins and products and for duplicate elimination. Green, Karvounarakis and Tannen (2007) put sets and bags in one model, relations annotated by a commutative semiring, with the Boolean semiring for sets and the natural numbers for bags, and showed that positive queries commute with semiring homomorphisms. Law 22 is the case of the homomorphism from the natural numbers to the Boolean values.

## References
