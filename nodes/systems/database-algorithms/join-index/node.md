---
tag: 8DK147
kind: data-structure
slug: join-index
name: Join index
aliases:
- Valduriez join index
- join index of tuple identifiers
area: systems/database-algorithms
level: advanced
summary: "A stored binary relation of pairs of tuple identifiers (rid of r, rid of s) for the tuples of R and S that join. The join is read from it instead of recomputed, at a cost in updates."
model: external-memory-model
complexity:
  vars: {P: the number of pairs in the index, q: the number of pairs per page, M: the number of pages of R, N: the number of pages of S, d: the number of pairs of the tuple that is inserted or deleted}
  time: {join: O(P log P), insert: O(d) expected, delete: O(d) expected}
  space: {extra: Θ(P)}
  io:
    worst: "⌈P/q⌉ + M + N"
properties: {persistent: false, concurrent: false, external: true}
prereqs: [relational-join, b-plus-tree]
see_also: [index-nested-loop-join, semijoin, materialized-view, bitmap-index, clustered-index, covering-index, hash-join, b-tree]
sources:
  - paper: doi:10.1145/22952.22955
    title: Patrick Valduriez, Join indices, ACM Transactions on Database Systems 12(2), 1987, pages 218 to 246
    locator: the definition of the join index as a binary relation of surrogates, its storage as two copies clustered on each surrogate, the join algorithm that sorts the partial result on the surrogates of S, and the cost of maintenance under updates
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill, 2003
    locator: Chapter 25, Data Warehousing and Decision Support, the part on indexing for decision support (join indexes and bitmapped join indexes); Section 14.4 for the cost conventions
  - paper: doi:10.1145/152610.152611
    title: Goetz Graefe, Query evaluation techniques for large databases, ACM Computing Surveys 25(2), 1993, pages 73 to 169
    locator: the section on join algorithms, the part on join indices and on fetching tuples by sorted record identifiers
---

A join index stores the result of a join in its smallest form: the set of pairs $(i, j)$ of tuple identifiers such that the tuple of $R$ with identifier $i$ joins with the tuple of $S$ with identifier $j$. It holds no attribute values. To answer the join, a system reads the pairs and fetches the tuples they name, so it does not need to compare join keys at all. Valduriez (1987) defined it and kept it in two copies, one ordered on the identifiers of $R$ and one on those of $S$, each in a [B+ tree](/b-plus-tree/). The price is maintenance: each insertion or deletion in $R$ or $S$ must add or remove the pairs of the changed tuple.

## In plain words

Two filing cabinets hold customer cards and order slips, and every card and slip has a number stamped on it. Instead of matching them by customer name each time, you keep a thin notebook. Each line of the notebook has two numbers: the number of a card and the number of a slip that belongs to it.

To list all customers with their orders, you go down the notebook, pull each card and each slip it names, and put them side by side. You never compare names. When a new slip arrives, you look up its customer and add a line. When a card is thrown away, you strike out its lines. The notebook is small, but it must be kept up to date.

## The abstract type

Let $R$ and $S$ be relations whose tuples have *record identifiers* (rids): $R[i]$ is the tuple of $R$ with rid $i$, and the rid gives the page of the tuple. For a join condition $\theta$, here $r.a = s.b$, the join index is
$$J = \{\, (i, j) \mid \theta(R[i], S[j]) \,\}.$$
The operations are:

- `insert-R(r)` and `insert-S(s)`: add a tuple, give it a new rid, and add its pairs to $J$.
- `delete-R(i)` and `delete-S(j)`: remove a tuple and all its pairs.
- `join()`: return the multiset $R \bowtie S$, built from $J$.
- `matches-of-R(i)`: the rids of $S$ that join with $R[i]$, which also answers the [semijoin](/semijoin/) test for one tuple.

An update of the join attribute of a tuple is a delete followed by an insert.

## Representation

- **Two copies of $J$.** $J_R$ holds the pairs ordered by $i$, and $J_S$ holds the same pairs ordered by $j$. Valduriez stores each in a B+ tree on its first rid, so that the pairs of one tuple are found by one search and lie together. A page holds $q$ pairs. The B+ tree is only the container: it indexes keys of one relation, while the join index stores the result of a join between two. A [B-tree](/b-tree/) would also do, but the B+ tree keeps all pairs in linked leaves, so line L5 reads them in order with one scan.
- **Value indexes.** An insertion of $r$ must find the tuples of $S$ with $s.b = r.a$. The structure keeps an index $V_S$ from each value of $b$ to the rids of $S$ that hold it, and an index $V_R$ for $R$. In a system these are ordinary indexes on the join attributes.
- **Stable rids.** A rid names a tuple for as long as it exists and is not used again after a delete. In the implementation the rid $i$ lies on page $\lfloor i / t \rfloor$ of its heap file, for $t$ tuples per page.

**Invariant.** $J_R$ and $J_S$ hold exactly the set $J$ for the current $R$ and $S$, and each tuple with no pairs has no entry in them.

## Operations

```pseudo id=main
INSERT-R(r)                                  ▷ INSERT-S is the same with R and S swapped
L1  i ← a new rid; store r in R at i; add i to V_R[r.a]
L2  for each j in V_S[r.a] do add (i, j) to J_R and to J_S

DELETE-R(i)                                  ▷ DELETE-S is the same with R and S swapped
L3  r ← R[i]; remove i from R and from V_R[r.a]
L4  for each j with (i, j) in J_R do remove (i, j) from J_R and from J_S

JOIN()
L5  P ← the pairs of J_R in order of i       ▷ ⌈|P|/q⌉ page reads
L6  for each (i, j) in P do read the page of R[i] if it differs from the last one, and append (j, R[i]) to L
L7  sort L on j
L8  for each (j, r) in L do read the page of S[j] if it differs from the last one, and append r · S[j] to out
L9  return out
```

Lines L1 and L2 add the pairs of a new tuple with one lookup in $V_S$. Lines L3 and L4 remove the pairs of a tuple with one search in $J_R$, and each pair removed from $J_R$ is also removed from $J_S$. Lines L5 to L8 are Valduriez's join algorithm: reading the pairs in order of $i$ fetches each page of $R$ that holds a matching tuple once, and sorting the partial result $L$ on $j$ fetches each page of $S$ that holds a matching tuple once.

## Example

Let $R$ have the keys $[10, 20, 10, 30]$ with rids 0 to 3, and $S$ have the keys $[20, 10, 40]$ with rids 0 to 2. There are $t = 2$ tuples per page, so $R$ has pages $\{0, 1\}$ and $\{2, 3\}$ and $S$ has pages $\{0, 1\}$ and $\{2\}$, and a page holds $q = 4$ pairs. The tuples of $R$ are inserted first, so their insertions add no pairs.

| operation | pairs added or removed | $J$ after it |
|---|---|---|
| insert $(20)$ into $S$, rid 0 | $V_R[20] = \{1\}$: add $(1, 0)$ | $\{(1, 0)\}$ |
| insert $(10)$ into $S$, rid 1 | $V_R[10] = \{0, 2\}$: add $(0, 1)$, $(2, 1)$ | $\{(0, 1), (1, 0), (2, 1)\}$ |
| insert $(40)$ into $S$, rid 2 | $V_R[40]$ is empty | unchanged |

JOIN reads the 3 pairs from 1 page. In the order $(0, 1), (1, 0), (2, 1)$, it reads page 0 of $R$ for rids 0 and 1 and page 1 for rid 2: 2 reads. After the sort on $j$, the partial result is $(0, R[1]), (1, R[0]), (1, R[2])$, and all three rids of $S$ are on page 0: 1 read. The output has 3 tuples, and the cost is $1 + 2 + 1 = 4$ I/Os.

Then delete rid 1 from $S$: line L4 for $S$ removes $(0, 1)$ and $(2, 1)$, and $J = \{(1, 0)\}$. Then insert $(40)$ into $R$: it gets the new rid 4, because rids are not used again, and $V_S[40] = \{2\}$ gives the pair $(4, 2)$. Now $J = \{(1, 0), (4, 2)\}$. The tests check every step.

## Correctness

The invariant holds after each operation. An insertion of $r$ with rid $i$ adds the pairs $(i, j)$ for the rids $j$ in $V_S[r.a]$, which are exactly the tuples of $S$ that join with $r$; no old pair changes, because the other tuples did not change. A deletion of $i$ removes exactly the pairs with first rid $i$, from both copies. So $J_R$ is always the set of matching pairs. JOIN emits $R[i] \cdot S[j]$ once for each pair, which is one copy for each matching pair of tuples, and the order of the pairs does not change the multiset. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

| operation | page I/O | work in memory |
|---|---|---|
| join | $\lceil P/q \rceil$ + pages of $R$ touched + pages of $S$ touched $\le \lceil P/q \rceil + M + N$ | $O(P \log P)$ for the sort |
| insert or delete of one tuple | one search of $V$ or of $J_R$, then $d$ pair updates in each copy | $O(d)$ expected with hash tables |
| matches of one tuple | one search of $J_R$ | $O(d)$ |
| space | $\lceil P/q \rceil$ pages per copy | $\Theta(P)$ pairs |

- **The join.** Each page of pairs is read once, each page of $R$ with a matching tuple is read once because the pairs are in order of $i$, and each page of $S$ with a matching tuple is read once because $L$ is sorted on $j$. The bound assumes that $L$ fits in memory for the sort; otherwise an [external merge sort](/external-merge-sort/) of $L$ adds its passes. The page counts are exact in the implementation, and the tests check them against $\lceil P/q \rceil$ plus the number of distinct pages.
- **When it pays.** A hash join costs about $3(M + N)$ for large inputs. If the matching tuples lie on few pages, a join index does much better. For example, with $M = N = 1000$, $P = 2000$ pairs, $q = 500$ and matching tuples on 100 pages of $R$ and 300 pages of $S$, the join costs $4 + 100 + 300 = 404$ I/Os, against $6000$ for a Grace hash join.
- **The worst case.** If every key is the same, $P = |R| \cdot |S|$. The index is then as large as the output, and fetching the tuples is no better than a nested-loop join.
- **Maintenance.** Each insertion or deletion of a tuple with $d$ partners costs $d$ updates in each of the two copies, plus the search in the value index. This cost is why a join index suits relations that change rarely.

## Variants

- **One copy only.** Keep only $J_R$ if the join is always driven from $R$, for example after a selection on $R$. Then deletions in $S$ need a scan or a search by $j$, so one copy suits relations where $S$ rarely changes.
- **Selections.** With a selection on $R$ that keeps a few rids, look up only their pairs in $J_R$. The cost is then proportional to the selected tuples and their partners, not to the size of $R$.
- **Bitmap join index.** For a star schema, store for each value of a dimension attribute a bitmap over the rows of the fact table that join with it. This combines the join index with a [bitmap index](/bitmap-index/), and decision support systems use it for selective star joins.
- **Materialized join.** A [materialized view](/materialized-view/) stores the joined tuples themselves, not their rids. It avoids the fetches of lines L6 and L8 but is much larger, and an update to any attribute must change it.
- **Several relations.** A join index can store tuples of rids for a path of joins, which helps a query that always follows the same path.

## When to use it

Use a join index when the same join, often with selections, is run many times, the relations change rarely, and the matching tuples are a small part of the relations. Decision support and data warehouses fit this. When the relations change often, or each join reads most of both relations, an ordinary [hash join](/hash-join/) or [sort-merge join](/sort-merge-join/) needs no maintenance and costs about the same. When only one side needs fast access by key, an index on the join attribute and an [index nested-loop join](/index-nested-loop-join/) are simpler.

## Pitfalls

- **Unstable rids.** A rid must not change while the tuple lives. A system that moves tuples, for example to reorganize a file, must update every pair that names them, or use a logical identifier.
- **Reusing a rid.** If a deleted rid is given to a new tuple before its pairs are removed, the old pairs point at the wrong tuple. The implementation never reuses a rid.
- **Fetching in pair order only.** Reading $S[j]$ in the order of $J_R$ reads a page of $S$ once per pair in the worst case. Line L7 must sort on $j$ first.
- **Forgetting one copy.** Line L4 must remove each pair from both copies. Otherwise $J_S$ keeps pairs of a deleted tuple, and a later join from $S$ fetches a tuple that does not exist.

## Implementations

## History

Valduriez (1987) introduced the join index as a binary relation of tuple surrogates, gave the join algorithm that fetches $R$ in surrogate order and $S$ after a sort, and compared its cost, including the cost of maintenance, with join methods that use no precomputed data. The comparison favors the join index when the join is selective and updates are rare. Bitmapped join indexes, for star joins in data warehouses, followed in the 1990s. Ramakrishnan and Gehrke, Chapter 25, present join indexes among the index structures for decision support.

## References
