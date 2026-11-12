---
tag: 281T73
kind: concept
slug: covering-index
name: Covering index
aliases:
- index-only plan
- index-only scan
area: systems/database-algorithms
level: intro
summary: "An index that holds every column a query needs, so the query is answered from the index alone with no reads of the table. Extra columns can ride in the leaves only."
prereqs: [clustered-index, b-plus-tree]
see_also: [bitmap-index, index-selection, materialized-view, index-nested-loop-join, selectivity, cost-model, zone-map, join-index]
sources:
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: Chapter 8, Section 8.5 (indexes and performance tuning, with composite search keys in 8.5.3 and index-only evaluation)
  - paper: doi:10.1561/1900000028
    title: "Goetz Graefe, Modern B-tree techniques, Foundations and Trends in Databases 3(4) (2011)"
    locator: the parts on secondary indexes that cover a query and on index-only retrieval
  - url: https://www.postgresql.org/docs/current/indexes-index-only-scans.html
    title: PostgreSQL documentation, Index-only scans and covering indexes
    locator: the INCLUDE clause, and the visibility map check that an index-only scan needs
---

An index *covers* a query when every column that the query reads, in its predicates, its output, its grouping and its ordering, is stored in the index. The query plan then reads only the index, an *index-only plan*, and never fetches a record from the table. For a range query through an [unclustered index](/clustered-index/), this removes the fetch of one table page per match, which is most of the cost. A covering index is a second, narrow, sorted copy of some columns of the table, and it gives a second access path that behaves like a clustered one for the queries it covers.

## In plain words

A library catalog card lists the title, the author and the year of a book. If you only want to know which books by an author came out after 1990, the cards are enough: you read the cards for that author and never walk to a shelf.

If you also want the number of pages, and the card does not show it, you must walk to the shelf for every book. A covering index is a catalog whose cards hold everything that a common question needs. The cards are small and sorted, so reading many of them is fast. The cost is that every card is bigger, and every change to a book must also change its card.

## The idea

**When an index covers a query.** Let the index store, in each leaf entry, the columns $C_I$, and let the query $Q$ use the columns $C_Q$. The index covers $Q$ when $C_Q \subseteq C_I$. An index on $(a, b)$ covers `SELECT b FROM T WHERE a BETWEEN 10 AND 20`, and also `SELECT a, COUNT(*) FROM T GROUP BY a`, since the leaves hold $a$ in sorted order. It does not cover `SELECT c FROM T WHERE a = 5`.

**Key columns and included columns.** In a composite index, the key columns define the order of the entries, and a search can use them as a prefix: an index on $(a, b)$ helps a predicate on $a$, or on $a$ and $b$, but not a predicate on $b$ alone. Columns that a query only reads, and does not search or sort on, need not be part of the key. Several systems let you declare them as *included* columns. They are stored as a payload in the leaf entries only, not in the internal nodes and not in the separator keys. So they do not lower the fanout of the internal nodes, they do not count for the uniqueness of a unique index, and the order of the entries does not depend on them.

**Cost.** For a range query with $k$ matches, through a B+ tree of height $h$ with $e$ entries per leaf, on a table of $n$ records with $p$ per page:

- an index-only plan reads $h - 1$ internal nodes and about $k/e$ leaves;
- a plan through the same index that fetches the records reads also about one table page per match, about $k$ pages, or the number of distinct pages when it sorts the record ids first;
- a full scan of the table reads $n/p$ pages.

Index entries are narrower than records, so $e > p$, and even a full scan of a covering index is cheaper than a full scan of the table.

**What it costs to keep.** Every insert, delete and update of a covered column changes the index. Wide included columns make the index larger, and the gain is lost when the index is close to the size of the table. Choosing covering indexes for a workload under a space budget is an instance of [index selection](/index-selection/), close to choosing [materialized views](/materialized-view/).

**Visibility.** In a system with multiversion concurrency control, a record version may be invisible to a transaction even though its index entry is there. If the index does not store visibility information, an index-only plan must still check it. PostgreSQL keeps a visibility map of table pages whose records are all visible to everyone; an index-only scan fetches the table page only for entries on pages that are not marked. On a table with many recent updates, an "index-only" scan can fetch most table pages anyway.

**Implicit coverage.** When a table is clustered on its primary key and secondary indexes store the primary key instead of a physical record id, as in InnoDB, every secondary index holds the primary key columns too. A secondary index on $a$ then covers queries that read only $a$ and the primary key.

## Examples

**A range query.** A table has $n = 1{,}000{,}000$ records, 40 per page, so 25,000 pages, in an order unrelated to column $a$. An index on $(a, b)$ has 200 entries per leaf, so 5,000 leaves, with 25 internal nodes and a root: height 3. The query reads $b$ for the 10,000 records with $a$ in a range, 1% of the table.

| plan | I/Os |
|---|---|
| index-only, on $(a, b)$ | 2 internal nodes + 50 leaves = 52 |
| index on $a$ only, fetch each record in key order | 52 + about 10,000 |
| index on $a$ only, sort record ids, fetch each distinct page once | 52 + about 8,276 |
| full scan of the table | 25,000 |

The value 8,276 is Yao's estimate $25{,}000\,(1 - \binom{990{,}000}{40} / \binom{1{,}000{,}000}{40})$ of the number of distinct pages that hold 10,000 records chosen at random (see the [clustered index](/clustered-index/) page). The covering index makes the query about 160 times cheaper than the best plan that fetches records.

**A grouping query.** `SELECT a, COUNT(*) FROM T GROUP BY a` reads the 5,000 leaves of an index on $a$ in order, and counts runs of equal keys, with no sort and no hash table. A scan of the table would read 25,000 pages and then group.

**Included columns.** Suppose $a$ is 8 bytes and $b$ is a 200-byte string. An index with key $(a, b)$ puts the 200-byte values in its separators, so an internal node holds far fewer entries. An index with key $a$ and $b$ as an included column has internal nodes with 8-byte separators, and the same leaves. Both cover the query; the second has a higher fanout and may have one level less.

**A join.** An [index nested loop join](/index-nested-loop-join/) that needs only the join key and a few columns of the inner table can probe a covering index of the inner table and never touch its records.

## Where it is used

- Most relational systems choose an index-only plan automatically when an index covers the query. SQL Server and PostgreSQL (from version 11) have an `INCLUDE` clause for included columns; other systems get the same effect with a wider composite key.
- Physical design tools propose covering indexes for frequent queries, as part of [index selection](/index-selection/).
- A [join index](/join-index/) or a [bitmap index](/bitmap-index/) can answer some queries without reading the table as well, for counts and for predicates on the indexed columns.
- Ramakrishnan and Gehrke discuss index-only evaluation as a reason to add columns to a composite search key during physical tuning.

## References
