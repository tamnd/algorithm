---
tag: XH9D31
kind: definition
slug: horizontal-fragmentation
name: Horizontal fragmentation
aliases:
- primary horizontal fragmentation
- derived horizontal fragmentation
area: databases/distributed-databases
level: core
summary: Split a relation into subsets of rows defined by selection predicates or by a join with another fragmented relation.
prereqs: [relational-algebra]
see_also: [vertical-fragmentation, hash-partitioning, range-partitioning, sharding, data-allocation-problem, schism-partitioning, semijoin, distributed-query-processing]
sources:
  - paper: doi:10.1145/582353.582376
    title: Stefano Ceri, Mauro Negri and Giuseppe Pelagatti, Horizontal data partitioning in database design, Proceedings of the 1982 ACM SIGMOD International Conference on Management of Data, 1982, starting at page 128
    locator: horizontal fragments defined by minterm predicates over the simple predicates that the applications use, and derived fragments that follow the fragments of another relation
  - book: isbn:9783030262525
    title: M. Tamer Özsu and Patrick Valduriez, Principles of Distributed Database Systems, fourth edition, Springer, 2020
    locator: Chapter 2, Distributed and Parallel Database Design, the sections on fragmentation (the rules of completeness, reconstruction and disjointness, and primary and derived horizontal fragmentation)
---

A horizontal fragmentation splits a relation into fragments that each hold some of its rows and all of its columns. In a *primary* fragmentation each fragment is a selection $\sigma_{m}(R)$ by a predicate $m$ on $R$; in a *derived* fragmentation each fragment of a relation $S$ is a [semijoin](/semijoin/) $S \ltimes R_m$ with a fragment of another relation $R$. The fragments can then be stored at different sites, so that each site holds the rows that its users need. A fragmentation is correct when it is complete, can be put back together, and puts each row in one fragment.

## Definition

Let $R$ be a relation, a bag of rows. A *horizontal fragmentation* of $R$ is a list of fragments $R_1, \dots, R_n$ with $R_i = \sigma_{q_i}(R)$ for some predicates $q_i$. It is *correct* if it meets three rules.

- **Completeness.** Every row of $R$ is in at least one fragment.
- **Reconstruction.** $R$ is the bag union of the fragments, $R = R_1 \cup \dots \cup R_n$ (UNION ALL in SQL), with the right count for every row.
- **Disjointness.** No row is in two fragments.

For bags, completeness and disjointness together give reconstruction. If the fragments are complete but not disjoint, a set union still gives $R$ back, but a bag union counts a row twice.

**Minterm fragments.** Let $p_1, \dots, p_k$ be simple predicates, each a comparison of one attribute with a constant. A *minterm* chooses, for each $p_i$, either "$p_i$ is true" or "$p_i$ is not true". The *primary horizontal fragmentation* by $p_1, \dots, p_k$ has one fragment $\sigma_m(R)$ for each minterm $m$ that some row satisfies. With "not true" read as "FALSE or UNKNOWN", each row satisfies exactly one minterm, so the minterm fragments are always correct, also when the data has NULLs.

**Derived fragments.** Let $S$ be a relation that refers to $R$ by the attributes $J$, for example by a foreign key. The *derived horizontal fragmentation* of $S$ by a fragmentation $R_1, \dots, R_n$ of $R$ has the fragments $S_i = S \ltimes R_i$. It puts a row of $S$ in the same fragment as the row of $R$ that it refers to, so a join of $S$ with $R$ on $J$ can run fragment by fragment, $S_i \bowtie R_i$, at one site each.

```pseudo id=main
PRIMARY(R, p_1..p_k)
L1  for each minterm m over p_1..p_k        ▷ each p_i taken as "is true" or "is not true"
L2      R_m ← σ_m(R)
L3      keep R_m if it is not empty
DERIVED(S, R_1..R_n)
L4  for each fragment R_i of the owner R
L5      S_i ← S ⋉ R_i                       ▷ on the common attributes; NULL matches nothing
RECONSTRUCT(fragments)
L6  return the bag union of the fragments
```

There are $2^k$ minterms, but no more fragments than distinct rows survive line L3, and many minterms are empty because they are contradictory, such as $A < 5$ together with $A > 10$. The [proof page](proofs/correctness.md) shows that the minterm fragments are complete and disjoint, and that the derived fragments are complete when every row of $S$ refers to a row of $R$ and disjoint when $J$ is a key of $R$.

## Examples and non-examples

**A primary fragmentation.** The relation $ACCOUNT(id, branch, balance)$ has five rows: $(1, Paris, 500)$, $(2, Paris, 2500)$, $(3, Lyon, 800)$, $(4, Lyon, NULL)$ and $(5, Nice, 1200)$. The simple predicates are $p_1$: $branch = Paris$ and $p_2$: $balance < 1000$.

| minterm | rows |
|---|---|
| $p_1$ true, $p_2$ true | 1 |
| $p_1$ true, $p_2$ not true | 2 |
| $p_1$ not true, $p_2$ true | 3 |
| $p_1$ not true, $p_2$ not true | 4, 5 |

Row 4 has a NULL balance, so $p_2$ is UNKNOWN on it, which is "not true". The four fragments are complete and disjoint, and their bag union is $ACCOUNT$.

**A non-example: NOT in place of "not true".** If the last fragment is written as $\sigma_{\lnot p_1 \land \lnot p_2}(ACCOUNT)$ in SQL, then on row 4 the predicate $\lnot p_2$ is UNKNOWN, and the selection drops the row. Row 4 is in no fragment, so this fragmentation is not complete. The fix is to write the negative literal as $p_2$ IS NOT TRUE, or to declare the attribute NOT NULL.

**A derived fragmentation.** The relation $TXN(tid, id, amount)$ refers to $ACCOUNT$ by $id$, with the rows 10 and 11 for account 1, row 12 for account 3, row 13 for account 4 and row 14 for account 5. The derived fragments are $\{10, 11\}$, $\{\}$, $\{12\}$ and $\{13, 14\}$: each transaction goes to the fragment of its account. Since $id$ is a key of $ACCOUNT$ and every transaction refers to an existing account, the fragments are complete and disjoint.

**A non-example: a derived fragmentation on a non-key.** If the owner has two rows with the same value of $J$ in two different fragments, a member row with that value is in both derived fragments, and disjointness fails. If a member row has a NULL in $J$, or a value that is not in the owner, it is in no fragment, and completeness fails. The tests of the implementation check these cases.

**A non-example: a fragmentation that keeps only some columns.** Splitting $ACCOUNT$ into $\pi_{id, branch}$ and $\pi_{id, balance}$ is a [vertical fragmentation](/vertical-fragmentation/), not a horizontal one: each fragment has all the rows and some of the columns.

## Related definitions

- **Hash partitioning.** [Hash partitioning](/hash-partitioning/) puts a row in the fragment that a hash function of a key chooses. It is a horizontal fragmentation whose predicates are $h(K) \bmod n = i$, but they come from the hash function, not from the workload, so a query with a range predicate must read every fragment.
- **Range partitioning.** [Range partitioning](/range-partitioning/) uses predicates of the form $c_{i-1} \le K < c_i$ on one attribute. It is the special case of a primary fragmentation with simple predicates on one attribute only, and a range query reads only the fragments that meet its range.
- **Sharding.** [Sharding](/sharding/) is the systems name for a horizontal fragmentation together with its placement: each fragment, a shard, lives on one server, and a router maps a key to its shard. The fragmentation is the logical split; sharding adds the servers, the routing and the moving of shards.
- **Hybrid fragmentation.** A vertical fragmentation of a horizontal fragment, or the other way around. Reconstruction then uses both joins and unions.
- **Allocation.** Where to store each fragment and its copies is the [data allocation problem](/data-allocation-problem/). [Schism](/schism-partitioning/) chooses a fragmentation and an allocation together from a trace of transactions.
- **Localization.** In [distributed query processing](/distributed-query-processing/), a query on $R$ is rewritten on the fragments, and the fragments whose predicates contradict the query are dropped.

## References
