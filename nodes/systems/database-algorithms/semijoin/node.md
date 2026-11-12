---
tag: XWTK09
kind: concept
slug: semijoin
name: Semijoin
aliases:
- semi-join
- left semi join
area: systems/database-algorithms
level: intro
summary: "The tuples of R that have at least one matching tuple in S, written R ⋉ S. Semijoins shrink relations before a join and fully reduce the relations of a tree query."
prereqs: [relational-join, relational-algebra]
see_also: [yannakakis-algorithm, bloom-join, acyclic-join-evaluation, hypergraph, multiway-join, hash-join, magic-sets, reduce-side-join]
sources:
  - paper: doi:10.1145/322234.322238
    title: Philip A. Bernstein and Dah-Ming W. Chiu, Using semi-joins to solve relational queries, Journal of the ACM 28(1), 1981, pages 25 to 40
    locator: the definition of the semijoin, semijoin programs, full reducers, and the results on tree queries and cyclic queries
  - paper: doi:10.1145/319628.319650
    title: Philip A. Bernstein, Nathan Goodman, Eugene Wong, Christopher L. Reeve and James B. Rothnie, Query processing in a system for distributed databases (SDD-1), ACM Transactions on Database Systems 6(4), 1981, pages 602 to 625
    locator: the reduction phase of query processing in SDD-1 (semijoins chosen by a cost and benefit estimate before the data is moved to one site)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill, 2003
    locator: Chapter 22, Parallel and Distributed Databases, the part on distributed query processing (joins across sites with semijoins and Bloomjoins)
---

The semijoin of a relation $R$ with a relation $S$, written $R \ltimes S$, is the set of tuples of $R$ that join with at least one tuple of $S$. It is the join followed by a projection back onto the attributes of $R$: $R \ltimes S = \pi_{\mathrm{attrs}(R)}(R \bowtie S)$. It never adds a tuple to $R$ and never adds an attribute, so it is a filter on $R$. The join $R \bowtie S$ is unchanged if $R$ is first replaced by $R \ltimes S$. This makes the semijoin the basic tool for removing *dangling tuples*, the tuples that cannot take part in the result, before an expensive join or before data is sent over a network. Bernstein and Chiu (1981) studied programs of semijoins and showed which queries they can fully reduce.

## In plain words

You have a list of employees, each with a department number, and a list of departments, each with a city. You want only the employees whose department is in the department list. You do not want the city, and you do not want an employee twice if the department has two cities.

So you go through the employees and, for each one, you check whether the department number appears at least once in the department list. If it does, you keep the employee as is. If not, you drop the employee. The result is a shorter list of employees with the same columns. That is the semijoin.

## The idea

**Definition.** Let $R$ and $S$ be relations and let $\theta$ be a join condition, by default equality on the common attributes. Then
$$R \ltimes_\theta S = \{\, r \in R \mid \text{there is an } s \in S \text{ with } \theta(r, s) \,\}.$$
For the natural join this is $\pi_{\mathrm{attrs}(R)}(R \bowtie S)$ under set semantics. The operator is not symmetric: $R \ltimes S$ is a part of $R$ and $S \ltimes R$ is a part of $S$. The *antijoin* $R \mathbin{\triangleright} S = R \setminus (R \ltimes S)$ is the complement: the tuples of $R$ with no match in $S$.

**Bags.** Under bag semantics, the semijoin keeps each tuple of $R$ with its own multiplicity in $R$, once if it has any match. This is *not* the bag projection of the join, which repeats a tuple of $R$ once for each of its matches. Systems that offer a semijoin operator, often called a *left semi join*, use the first meaning, because it is what an `EXISTS` or `IN` subquery needs.

**Three facts.** Let $J$ be the common attributes of $R$ and $S$ and let the join be the natural join.

1. *Only the join columns of $S$ matter:* $R \ltimes S = R \ltimes \pi_J(S)$. A tuple $r$ has a match in $S$ exactly when its value $r[J]$ is in $\pi_J(S)$.
2. *The reducer identity:* $R \bowtie S = (R \ltimes S) \bowtie S$. A tuple of $R$ that is not in $R \ltimes S$ has no partner in $S$, so it gives no tuple of the join, and every tuple of $R \ltimes S$ keeps all its partners.
3. *Idempotence:* $(R \ltimes S) \ltimes S = R \ltimes S$, because every tuple left after the first step has a match.

Fact 1 is why a semijoin is cheap to send over a network: one ships the set $\pi_J(S)$ of join values, not $S$. Fact 2 is why a semijoin is safe: it can only remove tuples that do not matter. A [Bloom join](/bloom-join/) replaces $\pi_J(S)$ by a [Bloom filter](/bloom-filter/) of it, which is smaller but lets some extra tuples through. By Fact 2 those extra tuples are harmless, because the final join removes them.

**Semijoin programs and full reducers.** For a query that joins relations $R_1, \dots, R_n$, a *semijoin program* is a sequence of steps $R_i := R_i \ltimes R_j$. By Fact 2, no step changes the result of the query. A program is a *full reducer* if, after it runs, every remaining tuple of every $R_i$ takes part in at least one tuple of the result. Bernstein and Chiu (1981) showed that tree queries, whose relations can be arranged as a tree with each join attribute on a connected set of nodes, always have a full reducer, and that cyclic queries need not have one. For a tree, two passes are enough: one from the leaves to the root, then one from the root to the leaves, with $2(n - 1)$ semijoins. These are the queries with an acyclic [hypergraph](/hypergraph/), and this reduction is the first half of the [Yannakakis algorithm](/yannakakis-algorithm/).

## Examples

**One semijoin.** Let $R(\mathit{id}, \mathit{dept}) = \{(1, 10), (2, 20), (3, 10), (4, 30)\}$ and $S(\mathit{dept}, \mathit{city}) = \{(10, \text{Paris}), (10, \text{Lyon}), (20, \text{Rome})\}$. The join $R \bowtie S$ has 5 tuples: employees 1 and 3 appear twice each, because department 10 has two cities. The semijoin is $R \ltimes S = \{(1, 10), (2, 20), (3, 10)\}$, three tuples, each once. The bag projection of the join onto $(\mathit{id}, \mathit{dept})$ would have 5 tuples, which is the wrong answer for "employees with a department". The antijoin is $R \mathbin{\triangleright} S = \{(4, 30)\}$, and $S \ltimes R = S$, because every department of $S$ has an employee.

**A semijoin across two sites.** Let $R$ be at site 1, with 10,000 tuples of 100 bytes, or 1,000,000 bytes, and let $S$ be at site 2, with 500 tuples of 200 bytes, or 100,000 bytes, and 500 distinct join values of 4 bytes each. Suppose 400 tuples of $R$ have a match, and the result is wanted at site 2.

| plan | bytes sent |
|---|---|
| send $R$ to site 2 | 1,000,000 |
| send $S$ to site 1, join, send the result to site 2 | 100,000 plus the result |
| send $\pi_J(S)$ to site 1, send $R \ltimes S$ to site 2, join there | $2000 + 40{,}000 = 42{,}000$ |

The semijoin plan sends the least data here. It pays when the join values are small and the semijoin removes most of $R$. If almost every tuple of $R$ matches, it sends $\pi_J(S)$ for nothing.

**A full reducer on a chain.** Let $R(A, B) = \{(1, 1), (2, 2), (3, 3)\}$, $S(B, C) = \{(1, 5), (2, 6), (4, 7)\}$ and $T(C, D) = \{(5, 8), (7, 9)\}$. The join $R \bowtie S \bowtie T$ is $\{(1, 1, 5, 8)\}$. The tree is the path $T, S, R$, and we take $R$ as the root. The pass toward the root runs $S := S \ltimes T$ and then $R := R \ltimes S$. The pass back runs $S := S \ltimes R$ and then $T := T \ltimes S$.

| step | result |
|---|---|
| $S := S \ltimes T$ | $\{(1, 5), (4, 7)\}$ |
| $R := R \ltimes S$ | $\{(1, 1)\}$ |
| $S := S \ltimes R$ | $\{(1, 5)\}$ |
| $T := T \ltimes S$ | $\{(5, 8)\}$ |

After four semijoins, $2(n - 1)$ for $n = 3$, each relation holds exactly the tuples that appear in the result.

**A cycle that semijoins cannot reduce.** Let $R(A, B) = \{(1, 1), (2, 2)\}$, $S(B, C) = \{(1, 1), (2, 2)\}$ and $T(C, A) = \{(1, 2), (2, 1)\}$. Every tuple of each relation has a match in each of the other two: for example $(1, 1) \in R$ meets $(1, 1) \in S$ on $B$ and $(2, 1) \in T$ on $A$. So every semijoin leaves its relation unchanged, and no semijoin program removes anything. But the join $R \bowtie S \bowtie T$ is empty: following $A = 1$ through $R$ and $S$ gives $C = 1$, and $T$ maps $C = 1$ to $A = 2$, not 1. A script checked both claims. The tests are local, two relations at a time, and a cycle can hide a contradiction that no pair shows.

## Where it is used

- **Distributed query processing.** SDD-1 (Bernstein, Goodman, Wong, Reeve and Rothnie, 1981) ran a reduction phase of semijoins, chosen by estimated cost and benefit, before it moved the reduced relations to one site. Ramakrishnan and Gehrke, Chapter 22, present semijoins and Bloomjoins for joins across sites.
- **Acyclic joins.** The [Yannakakis algorithm](/yannakakis-algorithm/) runs a full reducer and then joins along the tree, in time linear in the input plus the output. See [acyclic join evaluation](/acyclic-join-evaluation/).
- **Subqueries.** `EXISTS` and `IN` subqueries are semijoins, and `NOT EXISTS` and `NOT IN` (without nulls) are antijoins. Optimizers turn them into semijoin operators, usually a [hash join](/hash-join/) that stops at the first match of each probe, or emits each build tuple once.
- **Bloom filters in joins.** The [Bloom join](/bloom-join/) and the bit-vector filters of hash joins are approximate semijoins.
- **Magic sets.** The [magic sets](/magic-sets/) rewriting passes bindings sideways in a query, which is a semijoin with the set of bindings.
- **Clusters.** In a [reduce-side join](/reduce-side-join/), a first job can compute the join keys of one input and filter the other input with them, to shuffle less data.
- **Multiway joins.** On the page [multiway join](/multiway-join/), semijoins remove dangling tuples before the intermediate results of a binary plan can grow.

## References
