---
tag: YE46T5
kind: technique
slug: pessimistic-cardinality-estimation
name: Pessimistic cardinality estimation
aliases:
- bound sketch
- upper-bound cardinality estimation
area: databases/query-planning
level: research
summary: "Use a guaranteed upper bound on the size of a join, computed from sizes and maximum degrees of the relations, in place of an estimate. The bound never underestimates, but it can be loose."
prereqs: [cardinality-estimation, agm-bound]
see_also: [attribute-value-independence, estimation-error-propagation, join-size-estimation-problem, count-min-sketch, generic-join, hash-partitioning, join-ordering, learned-cardinality-estimation]
sources:
  - paper: doi:10.1145/3299869.3319894
    title: "Walter Cai, Magdalena Balazinska and Dan Suciu, Pessimistic cardinality estimation: tighter upper bounds for intermediate join cardinalities, Proceedings of ACM SIGMOD 2019, 18 to 35"
    locator: the bound sketch (hash partitioning of the join values with degree statistics per bucket) and its use in place of the estimates of PostgreSQL
  - paper: doi:10.1137/110859440
    title: Albert Atserias, Martin Grohe and Daniel Marx, Size bounds and query plans for relational joins, SIAM Journal on Computing 42(4) (2013), 1737 to 1767
    locator: the bound on the size of a join from the sizes of the relations and a fractional edge cover of the query hypergraph
  - paper: doi:10.14778/2850583.2850594
    title: Viktor Leis, Andrey Gubichev, Atanas Mirchev, Peter Boncz, Alfons Kemper and Thomas Neumann, How good are query optimizers, really?, Proceedings of the VLDB Endowment 9(3) (2015), 204 to 215
    locator: Section 3 (the underestimates of the usual estimators on the Join Order Benchmark, which motivate bounds)
---

Pessimistic cardinality estimation replaces the estimate of the size of a join by an upper bound that holds for every database with the same statistics. Classic estimators assume [independence](/attribute-value-independence/) and uniformity, and on real data they mostly underestimate, which leads the optimizer to plans that are fast only for small results. An upper bound can be loose, but it cannot be too small. Walter Cai, Magdalena Balazinska and Dan Suciu proposed the bound sketch in 2019: it splits the join values into buckets by hashing and adds up a bound for each bucket, which makes the bound much tighter. This page gives the template, the simple degree bounds with their proofs, and the bucket method. The general problem is on the [cardinality estimation](/cardinality-estimation/) page, and the bound from the sizes of the relations alone is the [AGM bound](/agm-bound/).

## In plain words

An optimizer must guess how many rows a join gives. Usual guesses assume that columns are unrelated and values are spread evenly, and on real data they are often far too small. A plan made for a small result can then run for hours.

A pessimistic estimate asks a different question: what is the largest result that is possible, given what we know about the tables? For example, if every customer has at most 50 orders, then a join of 1000 customers with their orders has at most 50,000 rows. That number is never too small.

To make the bound tighter, split the join values into groups and find the largest group size inside each group. Many small bounds added together are much closer to the truth than one big bound.

## When it applies

- **Equality joins with statistics on degrees.** The method needs, for each relation and join attribute, the size of the relation and the maximum degree: the largest number of tuples with the same value of the attribute. Both are cheap to keep.
- **Underestimates are expensive.** It is useful when the cost of a plan grows much faster when the result is larger than planned than when it is smaller, which is common for nested loop joins and for joins that spill to disk.
- **Many joins.** Errors of estimates grow with the number of joins (see [estimation error propagation](/estimation-error-propagation/)). The bound has the same kind of growth, but only upward, so a plan chosen on bounds is safe against the worst case.
- **It does not apply** when a good estimate, not a safe one, is needed, for example for memory grants of small queries, or for predicates the statistics do not describe, such as LIKE.

## The template

1. Choose statistics that describe every database the optimizer may see: here, the sizes $|R|$ and the maximum degrees $\deg_R(a) = \max_v |\sigma_{a = v}(R)|$.
2. Prove an inequality $|Q(D)| \le B(\text{statistics of } D)$ for every database $D$.
3. Use $B$ wherever the optimizer would use an estimate.
4. Make $B$ tighter by splitting the data into parts and adding the bounds of the parts.

**Two relations.** For $R \bowtie_{R.a = S.a} S$,

$$|R \bowtie S| \le \min\big(|R| \cdot \deg_S(a),\ |S| \cdot \deg_R(a)\big).$$

*Proof.* Each tuple of $R$ joins with the tuples of $S$ with the same value of $a$, and there are at most $\deg_S(a)$ of them. So the join has at most $|R| \deg_S(a)$ tuples, and by the same argument from the side of $S$, at most $|S| \deg_R(a)$. $\square$

This bound is the best possible from these four numbers, up to rounding. If $|R| \deg_S \le |S| \deg_R$, put the tuples of $R$ in groups of $\deg_R$ tuples with the same value, and give each of these $|R|/\deg_R$ values $\deg_S$ tuples in $S$. This uses $|R| \deg_S / \deg_R \le |S|$ tuples of $S$, and every tuple of $R$ joins with $\deg_S$ tuples, so the join has exactly $|R| \deg_S$ tuples.

**Chains and trees of joins.** For a query whose join graph is a tree, pick a root relation $R_1$ and give each other relation $R_i$ its parent $R_{p(i)}$, joined on attribute $a_i$. Then

$$|Q| \le |R_1| \prod_{i \ge 2} \deg_{R_i}(a_i).$$

*Proof.* By induction over the relations in an order where each parent comes before its children: each partial result tuple extends in at most $\deg_{R_i}(a_i)$ ways when $R_i$ is added. $\square$

The best bound is the minimum over all roots. In a cyclic query, drop edges to get a spanning tree; the bound for the tree is also a bound for the query, because dropping join conditions can only add tuples. For a cyclic query, the [AGM bound](/agm-bound/) from the sizes alone can be tighter, for example $\sqrt{|R| |S| |T|}$ for a triangle, and the degree-aware bounds in the line of work of Cai et al. combine both kinds of statistics.

**Buckets (the bound sketch).** Choose a hash function $h$ from join values to $k$ buckets, and let $R^j$ and $S^j$ be the tuples whose join value hashes to bucket $j$. Tuples in different buckets do not join, so

$$|R \bowtie S| = \sum_{j=1}^{k} |R^j \bowtie S^j| \le \sum_{j=1}^{k} \min\big(|R^j| \deg_{S^j}(a),\ |S^j| \deg_{R^j}(a)\big).$$

*This is never looser than the bound with one bucket.* A sum of minimums is at most the minimum of the sums, and $\deg_{S^j} \le \deg_S$ and $\deg_{R^j} \le \deg_R$, so the right side is at most $\min(\sum_j |R^j| \deg_S, \sum_j |S^j| \deg_R) = \min(|R| \deg_S, |S| \deg_R)$. If each bucket holds a single join value $v$, then $|R^j| = \deg_{R^j} = f_R(v)$, the minimum is $f_R(v) f_S(v)$, and the bound is the exact join size. So $k$ trades the space of the statistics for the tightness of the bound. For a query with several join attributes, each attribute is hashed, and the sum runs over the combinations of buckets.

## Classic examples

**A bound against an estimate.** Let $R$ have 1000 tuples on attribute $b$: 100 with $b = 1$ and one each with $b = 2, \ldots, 901$. Let $S$ have 1001 tuples: one with $b = 1$, 50 each with $b = 2, \ldots, 11$, and one each with $b = 1000, \ldots, 1499$. The true join size is $100 \cdot 1 + 10 \cdot 50 = 600$. The classic estimate $|R| |S| / \max(V(R, b), V(S, b)) = 1000 \cdot 1001 / 901 \approx 1111$, where $V$ is the number of distinct values. The degree bound is $\min(1000 \cdot 50,\ 1001 \cdot 100) = 50{,}000$.

| buckets $k$ (with $h(v) = v \bmod k$) | 1 | 2 | 4 | 16 | 64 | 256 | 2048 |
|---|---|---|---|---|---|---|---|
| bound | 50,000 | 28,000 | 17,025 | 1125 | 1106 | 1101 | 600 |

With 16 buckets the bound is already within a factor 2 of the truth, and with 2048 buckets every value has its own bucket and the bound is exact. The classic estimate is close here, but nothing stops it from being 100 times too small on other data with the same statistics; the bound has no such case.

**Foreign keys.** If $S.a$ is a key, $\deg_S(a) = 1$, and the bound gives $|R \bowtie S| \le |R|$, the familiar rule for a join along a foreign key. A chain of such joins from a fact table has a bound equal to the size of the fact table, and it is exact when every foreign key has a match.

**Measured use.** Cai, Balazinska and Suciu replaced the estimates of PostgreSQL by bound sketches and report, on the Join Order Benchmark, that the plans were often faster and seldom slower. This is a measurement of their system, not a theorem.

## Variations

- **Degree sequences.** Keep the sorted list of the degrees of all values, or a compressed form of it, in place of the maximum alone. This gives tighter bounds at more cost; later systems such as SafeBound keep compressed degree sequences.
- **Entropy bounds.** The sizes and degrees can be written as constraints on the entropies of the attributes of a random result tuple, and an [entropy](/shannon-entropy/) inequality then bounds the size of the result. The AGM bound is the case with sizes only. The degree bounds above are special cases.
- **Bounds with predicates.** For a selection on a relation, use the statistics of the selected part, for example from a sample, or bound the selected part by the whole relation, which is safe but loose.
- **Using bounds in the plan search.** A bound for each subplan fits into [join ordering](/join-ordering/) in the same place as an estimate. Because the bounds are often loose by a similar factor for the competing subplans, the order of the plans by cost is often better than the bounds themselves.

## Pitfalls

- **Reading the bound as an estimate.** The bound is only an upper limit. Memory grants and cost numbers based on it can be far too high.
- **Stale statistics.** The guarantee holds only for the data the statistics describe. After updates, the maximum degree can grow, and the bound is no longer safe.
- **Too few buckets.** One heavy value can dominate a bucket. With few buckets, a single heavy value makes the bound for all values in its bucket large.
- **Cross products from dropped edges.** In a cyclic query, a spanning tree with a bad root can give a bound much larger than the AGM bound. Take the minimum of several bounds.
- **Hash collisions across attributes.** With several join attributes, the number of bucket combinations is $k^m$ for $m$ attributes, which limits $k$.

## Exercises

1. Show that the bucket bound with $k$ buckets is at most the bound with any coarser split, in which each part is a union of buckets. (Use the same two facts as the proof above.)
2. For the chain $R(a, b) \bowtie S(b, c) \bowtie T(c, d)$ with $|R| = 10^4$, $|S| = 10^5$, $|T| = 10^3$, $\deg_S(b) = 20$, $\deg_T(c) = 5$, $\deg_S(c) = 100$ and $\deg_R(b) = 3$, compute the bound with root $R$ and the bound with root $T$. (Answer: $10^4 \cdot 20 \cdot 5 = 10^6$; with root $T$, $10^3 \cdot 100 \cdot 3 = 3 \cdot 10^5$, which is tighter.)
3. Give two relations with the same sizes and maximum degrees for which the classic estimate is too small by a factor of at least 100.
4. For the triangle query $R(a, b) \bowtie S(b, c) \bowtie T(c, a)$ with $|R| = |S| = |T| = N$ and all degrees equal to $N$, compare the tree bound with the AGM bound $N^{3/2}$.

## References
