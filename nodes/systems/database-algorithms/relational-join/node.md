---
tag: 00W70A
kind: problem
slug: relational-join
name: Relational join problem
aliases:
- join problem
- theta-join
- two-way join problem
area: systems/database-algorithms
level: intro
summary: "Given relations R and S and a join condition, output every pair of tuples, one from each relation, that satisfies the condition, combined into one tuple."
model: external-memory-model
complexity:
  vars: {M: the number of pages of R, N: the number of pages of S, B: the number of buffer pages, T: the number of output tuples}
  io: {worst: "Ω(M + N)"}
prereqs: [relational-algebra, relational-model]
see_also: [semijoin, multiway-join, join-ordering, join-size-estimation-problem, reduce-side-join, spatial-join, set-similarity-join, sliding-window-join]
sources:
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill, 2003
    locator: Chapter 4 (the join operators of relational algebra), and Chapter 14, Section 14.4, The Join Operation, Sections 14.4.1 to 14.4.4
  - paper: doi:10.1145/152610.152611
    title: Goetz Graefe, Query evaluation techniques for large databases, ACM Computing Surveys 25(2), 1993, pages 73 to 169
    locator: the sections on binary matching operations (nested loops, merge and hash join)
  - paper: doi:10.1145/362384.362685
    title: Edgar F. Codd, A relational model of data for large shared data banks, Communications of the ACM 13(6), 1970, pages 377 to 387
    locator: Section 2.1, Operations on relations (the join)
---

The relational join problem asks for all pairs of tuples, one from a relation $R$ and one from a relation $S$, that satisfy a join condition, each pair combined into one output tuple. It is the operator of [relational algebra](/relational-algebra/) that query plans spend most of their time on. In a database the inputs are on disk, so the cost is counted in page reads and writes, and the classic solutions are the [nested-loop join](/nested-loop-join/), the [sort-merge join](/sort-merge-join/) and the [hash join](/hash-join/) families.

## In plain words

You have two lists on paper. One lists orders, with a customer number on each line. The other lists customers, with a number and a name on each line. You want a third list where each order also shows the name of its customer. To make it, you must find, for each order, the customer lines with the same number, and write one combined line for each match.

A join does this for any two tables and any rule that says which lines go together. If one order line matches two customer lines, you write two output lines. If an order has no match, it does not appear.

The question is how to find the matches without comparing every line of one list with every line of the other, when the lists are too large to keep in memory.

## Definition

A relation is a finite multiset of tuples over a schema, as in the [relational model](/relational-model/). Let $R$ have schema $(A_1, \ldots, A_a)$ and $S$ have schema $(B_1, \ldots, B_b)$, and let $\theta(r, s)$ be a predicate on a pair of tuples. The **theta-join** is

$$R \bowtie_\theta S = \{\!\{\, r \cdot s : r \in R,\ s \in S,\ \theta(r, s) \,\}\!\},$$

where $r \cdot s$ is the concatenation of the two tuples and the multiset keeps one copy for each pair $(r, s)$. So the multiplicity of a tuple $t$ in the output is the number of pairs $(r, s)$ with $r \cdot s = t$ and $\theta(r, s)$ true. In set semantics, the duplicates collapse.

- An **equi-join** has a condition $r.A_{i_1} = s.B_{j_1} \wedge \cdots \wedge r.A_{i_c} = s.B_{j_c}$. The attributes are the *join key*.
- A **natural join** $R \bowtie S$ is the equi-join on all attributes with the same name, with one copy of each such attribute in the output.

**Cost model.** $R$ has $M$ pages with $p_R$ tuples per page and $S$ has $N$ pages with $p_S$ tuples per page. Memory holds $B$ pages. The cost of an algorithm is the number of page reads and page writes, without the writes of the output, because every algorithm writes the same output. These are the conventions of Ramakrishnan and Gehrke, Section 14.4. The page [external memory model](/external-memory-model/) counts the same transfers but writes $N$ for the items, $M$ for the memory and $B$ for the block size, so the letters do not mean the same thing there.

## Variants

- **Equi-join and natural join.** The most common case, and the only case where hashing and sorting on the key apply.
- **Theta-join with a general condition.** Conditions such as $r.a < s.b$ or a band $|r.a - s.b| \le 5$. Sort-merge join can do inequality and band conditions. A general predicate needs a nested-loop join (Ramakrishnan and Gehrke, Section 14.4.4).
- **Outer joins.** A left outer join also outputs each $r$ with no match, padded with nulls. The algorithms below extend to it with one flag per tuple.
- **Semijoin and antijoin.** The [semijoin](/semijoin/) $R \ltimes S$ keeps the tuples of $R$ that have a match, and the antijoin keeps those with no match. Neither builds pairs.
- **Many relations.** The [multiway join problem](/multiway-join/) joins three or more relations, where the order of the binary joins matters, see [join ordering](/join-ordering/).
- **Other areas.** A [spatial join](/spatial-join/) pairs objects whose shapes overlap, a [set similarity join](/set-similarity-join/) pairs sets whose similarity passes a threshold, and a [sliding-window join](/sliding-window-join/) joins two streams over recent tuples. Each has its own index structures, and none of them is an equality test on a key. The [reduce-side join](/reduce-side-join/) and the [map-side join](/map-side-join/) solve the equi-join on a cluster, where the cost is the data shuffled over the network, not page I/Os.

## Examples

Take $R(\textit{order}, \textit{cust}) = \{(1, 2), (2, 2), (3, 3), (4, 1)\}$ and $S(\textit{cust}, \textit{name}) = \{(2, x), (3, y), (2, z)\}$, with the condition $R.\textit{cust} = S.\textit{cust}$.

| $r$ | matching $s$ | output tuples |
|---|---|---|
| $(1, 2)$ | $(2, x)$, $(2, z)$ | $(1, 2, 2, x)$, $(1, 2, 2, z)$ |
| $(2, 2)$ | $(2, x)$, $(2, z)$ | $(2, 2, 2, x)$, $(2, 2, 2, z)$ |
| $(3, 3)$ | $(3, y)$ | $(3, 3, 3, y)$ |
| $(4, 1)$ | none | none |

The output has 5 tuples. The key value 2 appears two times on each side, so it gives $2 \cdot 2 = 4$ tuples.

With the condition $R.\textit{order} < S.\textit{cust}$ instead, the pairs are those with $\textit{order} \in \{1, 2\}$ and $\textit{cust} \in \{2, 3\}$ larger than it: order 1 matches all 3 tuples of $S$, and order 2 matches $(3, y)$. So the output has 4 tuples.

The output can be as large as $|R| \cdot |S|$. If all keys are equal, each pair matches.

## Known algorithms

The costs are in page I/Os with the cost model above, from Ramakrishnan and Gehrke, Sections 14.4.1 to 14.4.3.

- [Nested-loop join](/nested-loop-join/): any condition, $M + p_R M N$ tuple at a time, $M + MN$ page at a time.
- [Block nested-loop join](/block-nested-loop-join/): any condition, $M + \lceil M/(B-2) \rceil N$.
- [Index nested-loop join](/index-nested-loop-join/): a condition that an index on $S$ can answer, $M + p_R M$ times the cost of one probe.
- [Sort-merge join](/sort-merge-join/): equality, inequality and band conditions, about $3(M + N)$ when $B$ is larger than about $\sqrt{\max(M, N)}$.
- [Hash join](/hash-join/): equality, $M + N$ when the smaller input fits in $B - 2$ pages.
- [Grace hash join](/grace-hash-join/): equality, $3(M + N)$ when $B > \sqrt{f M}$ for a fudge factor $f$.
- [Hybrid hash join](/hybrid-hash-join/): equality, between $M + N$ and $3(M + N)$.
- [Bloom join](/bloom-join/): equality across two sites, with a filter that reduces the tuples that are sent.
- [Join index](/join-index/): a stored list of matching tuple pairs, so the join reads only the pairs and the pages they name.

## Bounds

- **Lower bound.** Each algorithm must read each page of each input in the worst case, because a tuple that it does not read could match. So the cost is $\Omega(M + N)$ page reads. It must also produce $T$ output tuples, which costs $\Omega(T)$ work in memory, and $T$ can be $|R| \cdot |S|$.
- **Equi-join, upper bound.** Grace and hybrid hash join, and sort-merge join with enough memory, read and write each input page a constant number of times, so they cost $O(M + N)$ I/Os when $B$ is about $\sqrt{M}$ or more, plus the output. With little memory, both sorting and partitioning take $O(\log_B M)$ passes, and the cost is $O((M + N)\log_B (M + N))$, the cost of [external merge sort](/external-merge-sort/).
- **General condition.** Without structure in $\theta$, an algorithm must test each pair, so block nested-loop join, with about $MN/B$ I/Os, is the method.
- **Many relations.** For three or more relations, the [AGM bound](/agm-bound/) gives the largest possible output, and [generic join](/generic-join/) meets it. See the [multiway join problem](/multiway-join/).

## Reductions

- A natural join reduces to an equi-join and a projection, and a theta-join reduces to a Cartesian product and a selection: $R \bowtie_\theta S = \sigma_\theta(R \times S)$. This is the definition in [relational algebra](/relational-algebra/), not a good algorithm, because the product has $|R| \cdot |S|$ tuples.
- An equi-join reduces to sorting: sort both inputs on the key, then merge. This is [sort-merge join](/sort-merge-join/), and it inherits the cost of [external merge sort](/external-merge-sort/).
- An equi-join reduces to partitioning by a [hash function](/hash-function/): tuples with equal keys go to the same partition, so the join of the inputs is the union of the joins of the partition pairs. This is [Grace hash join](/grace-hash-join/), and the same idea is the [reduce-side join](/reduce-side-join/) on a cluster.
- Element distinctness reduces to a self equi-join: a list of keys has a repeated key exactly when its join with itself on the key has more tuples than the list.

## Applications

- Every query that combines facts from two tables, for example the orders of each customer or the courses of each student, needs a join.
- [Query optimization](/query-optimization/) chooses a join algorithm and an order for each join, with a [cost model](/cost-model/) and estimates of the output size from [cardinality estimation](/cardinality-estimation/).
- Distributed databases send a [semijoin](/semijoin/) or a [Bloom join](/bloom-join/) filter before the join to reduce network traffic.

## References
