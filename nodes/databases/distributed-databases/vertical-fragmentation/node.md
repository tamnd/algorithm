---
tag: XEF5EY
kind: definition
slug: vertical-fragmentation
name: Vertical fragmentation
aliases:
- vertical partitioning
area: databases/distributed-databases
level: core
summary: Split a relation into projections that each keep the key, grouping attributes that queries use together.
prereqs: [relational-algebra, candidate-key]
see_also: [horizontal-fragmentation, bond-energy-algorithm, lossless-join-decomposition, decomposition-storage-model, pax-page-layout, data-allocation-problem, functional-dependency, n-ary-storage-model]
sources:
  - paper: doi:10.1145/1994.2209
    title: Shamkant Navathe, Stefano Ceri, Gio Wiederhold and Jinglie Dou, Vertical partitioning algorithms for database design, ACM Transactions on Database Systems 9(4), 1984, pages 680 to 710
    locator: the attribute usage and attribute affinity matrices, the clustering of the affinity matrix by the bond energy algorithm, and the split of the clustered attributes into fragments
  - book: isbn:9783030262525
    title: M. Tamer Özsu and Patrick Valduriez, Principles of Distributed Database Systems, fourth edition, Springer, 2020
    locator: Chapter 2, Distributed and Parallel Database Design, the section on vertical fragmentation and the rules of completeness, reconstruction and disjointness
---

A vertical fragmentation splits a relation into fragments that each hold some of its columns and all of its rows. Each fragment is a projection $\pi_{K \cup G}(R)$ that keeps a key $K$ of $R$, so that a join of the fragments on $K$ gives $R$ back. The groups $G$ of other attributes are chosen so that each query of the workload reads few fragments: attributes that the same queries use go into the same fragment. In a distributed database the fragments can then live at the sites that use them, and in one database they can be stored apart, so that a scan reads only the columns it needs.

## Definition

Let $R$ be a relation over the attributes $U$ with a [candidate key](/candidate-key/) $K$. A *vertical fragmentation* of $R$ is a list of fragments $R_i = \pi_{K \cup G_i}(R)$, where $G_1, \dots, G_n$ are sets of attributes outside $K$. It is *correct* if it meets three rules.

- **Completeness.** Every attribute of $U$ is in some fragment: $K \cup G_1 \cup \dots \cup G_n = U$.
- **Reconstruction.** $R = R_1 \bowtie \dots \bowtie R_n$, the natural join on $K$.
- **Disjointness.** The groups $G_i$ are pairwise disjoint. Only the key is repeated in every fragment.

When $K$ is a key, completeness gives reconstruction: a row of $R$ is the join of its own pieces, and two pieces with the same key value come from the same row. This is the special case of a [lossless-join decomposition](/lossless-join-decomposition/) in which the shared attributes are a key of every fragment. Disjointness is not needed for reconstruction; it keeps each value in one place, so that an update of a non-key attribute changes one fragment.

```pseudo id=main
FRAGMENT(R, K, G_1..G_n)
L1  for i ← 1 to n
L2      R_i ← π_{K ∪ G_i}(R)
RECONSTRUCT(R_1..R_n, K)
L3  T ← R_1; for i ← 2 to n
L4      T ← T ⋈ R_i on K                  ▷ a NULL in K matches nothing
L5  return T, with the columns in the order of R
```

**Choosing the groups.** Navathe, Ceri, Wiederhold and Dou (1984) start from the queries of the workload. The *attribute usage matrix* says which attributes each query uses. The *attribute affinity* of two attributes $A_i$ and $A_j$ is the total frequency of the queries that use both. The [bond energy algorithm](/bond-energy-algorithm/) permutes the affinity matrix so that attributes with high affinity are next to each other, and a split step then cuts the ordered attributes into groups that separate the queries well. The [proof page](proofs/correctness.md) shows that the fragments of lines L1 and L2 join back to $R$ when $K$ is a key.

## Examples and non-examples

**A vertical fragmentation.** The relation $EMP(eno, name, salary, dept)$ has the key $eno$ and four rows: $(1, Ann, 5000, RD)$, $(2, Bo, 4000, Sales)$, $(3, Cy, NULL, RD)$ and $(4, Di, 4000, NULL)$. A directory application reads $name$ and $dept$, and a payroll application reads $salary$. The fragments are

- $EMP_1 = \pi_{eno, name, dept}(EMP)$, at the site of the directory,
- $EMP_2 = \pi_{eno, salary}(EMP)$, at the site of the payroll.

The join of $EMP_1$ and $EMP_2$ on $eno$ gives the four rows of $EMP$ back. The NULLs in $salary$ and $dept$ do no harm, because the join compares only $eno$.

**A non-example: fragments without the key.** Take $\pi_{name, dept}(EMP)$ and $\pi_{dept, salary}(EMP)$ for the two employees of RD, Ann with 5000 and Cy with NULL. The fragments share only $dept$, which is not a key. The join on $dept$ has four rows: each RD name gets each RD salary, so two of the rows were never in $EMP$.

**A non-example: a bag without a key.** The bag $R(A, B, C) = \{(0, 0, 0), (0, 1, 1)\}$ split into $\pi_{A, B}$ and $\pi_{A, C}$ joins back to four rows, since $A$ is not a key. The usual fix is a *tuple identifier*: give each row, and each copy of a duplicate row, its own id, and keep the id in every fragment.

**A non-example: a NULL in the key.** A row with a NULL in $K$ is lost by the join, because a NULL matches nothing. A key used for fragmentation must be NOT NULL.

**A non-example: a projection that drops an attribute.** $\pi_{eno, name}(EMP)$ and $\pi_{eno, salary}(EMP)$ alone are not complete, because $dept$ is in no fragment, and no join can bring it back.

## Related definitions

- **Horizontal fragmentation.** A [horizontal fragmentation](/horizontal-fragmentation/) splits the rows and keeps all the columns; it is put back by a union, not a join. A *hybrid* fragmentation applies one kind of split to the fragments of the other.
- **Column stores.** The [decomposition storage model](/decomposition-storage-model/) is the extreme case: each fragment holds the key, or a row position, and one attribute. The [n-ary storage model](/n-ary-storage-model/) is the other extreme, one fragment with all attributes, and [PAX](/pax-page-layout/) keeps the rows of a page together but stores each column of the page apart.
- **Lossless joins and dependencies.** The test that a decomposition joins back without loss uses the [functional dependencies](/functional-dependency/) of the schema; the condition that the common attributes are a key is the simplest case of the test on [lossless-join decomposition](/lossless-join-decomposition/).
- **Allocation.** Where to store each fragment and its copies is the [data allocation problem](/data-allocation-problem/).

## References
