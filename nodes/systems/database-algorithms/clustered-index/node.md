---
tag: KP39G2
kind: concept
slug: clustered-index
name: Clustered index
aliases:
- clustering index
area: systems/database-algorithms
level: intro
summary: "An index whose key order is the same as the physical order of the rows. A range query reads only the pages of the matching rows, not one page per row."
prereqs: [b-plus-tree, external-memory-model]
see_also: [covering-index, zone-map, bulk-loading-b-tree, index-selection, index-nested-loop-join, selectivity, bitmap-index, b-tree]
sources:
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: Chapter 8, Section 8.2 (8.2.1 clustered indexes, 8.2.2 primary and secondary indexes), Section 8.4 (the cost model and the comparison of file organizations, including 8.4.4 clustered files and 8.4.5 a heap file with an unclustered tree index) and Section 8.5.2 (clustered index organization)
  - paper: doi:10.1145/359461.359475
    title: "S. Bing Yao, Approximating block accesses in database organizations, Communications of the ACM 20(4) (1977)"
    locator: the expected number of blocks that hold k records chosen at random
---

An index is *clustered* when the order of the data records in the file is the same as, or close to, the order of the entries of the index. A range query through a clustered index finds the first match with one search of the index and then reads the matching records as consecutive pages, so it costs the index search plus the pages that hold the matches. Through an *unclustered* index the matching records lie on scattered pages, and the query costs about one page read per matching record. A file can be in only one order, so a table has at most one clustered index.

## In plain words

A library sorts its shelves by subject. The subject catalog is "clustered": all books about birds stand together, so you walk to the bird shelf and take them all from two or three shelves.

The author catalog is "unclustered". Books by authors whose names start with B are spread all over the building. The catalog lists each of them, but you must walk to a different shelf for almost every book. For one book, both catalogs are equally good. For many books, the catalog that matches the order of the shelves wins by far. The shelves can be in only one order, so only one catalog can be clustered.

## The idea

**Data entries.** Ramakrishnan and Gehrke describe three choices for what an index stores in its leaves: (1) the data record itself, (2) a pair of a key and the record id $\langle k, \mathit{rid} \rangle$, or (3) a key with a list of record ids. With choice (1) the index *is* the file, kept in key order, so it is clustered by definition; this is an index-organized table. With choices (2) and (3), the index is clustered only if the file happens to be sorted, or nearly sorted, on the same key.

**Cost of a range query.** Take a file of $n$ records, $p$ per page, a B+ tree index on key $A$ of height $h$, and a query $lo \le A \le hi$ that matches $k$ records. The index part costs $h - 1$ internal nodes plus the leaves with the $k$ entries. Then each match is fetched by its record id, with one buffer frame for data pages:

```pseudo id=main
RANGE-THROUGH-INDEX(lo, hi)
L1  read the internal nodes on the path from the root to the leaf of lo
L2  read the leaves from that leaf on while they hold keys ≤ hi
L3  for each matching entry (k, rid), in key order do
L4      if page(rid) is not the page in the buffer frame then
L5          read page(rid) into the frame          ▷ one I/O
L6      output the record rid
L7  ▷ variant: collect the rids, sort them by page, read each distinct page once
```

- **Clustered.** The matches are consecutive in the file, so line L5 runs once per page that holds a match: $\lceil k / p \rceil$ or $\lceil k / p \rceil + 1$ pages. The total is about $h + k/p$ I/Os.
- **Unclustered.** Consecutive matches are on unrelated pages, so line L5 runs for almost every match. The total is about $h + k$ I/Os, which is $p$ times more for the data part. When $k$ is more than about $n/p$, that is more than a full scan of the file, which costs $n/p$ I/Os.
- **Sorted record ids.** Line L7 reads each distinct page once. For $k$ matches placed at random over the $m = n/p$ pages, the expected number of distinct pages is Yao's formula
$$m \left(1 - \binom{n - p}{k} \Big/ \binom{n}{k}\right),$$
since a given page holds none of the $k$ matches with probability $\binom{n-p}{k} / \binom{n}{k}$, the chance that all $k$ come from the other $n - p$ records. Sorting helps, but the cost is still far above $k/p$ unless the matches cover most pages anyway.

**Why only one.** The file has one physical order. Any second index on another key sees the records in an order that is unrelated to its own, so it is unclustered. To get a second "clustered" access path, the system keeps a second copy of the data in another order, or uses a [covering index](/covering-index/) that holds the needed columns in its own leaves.

**Keeping it clustered.** Inserts into a sorted heap file break the order unless the file leaves free space on its pages, and overflow pages break it in time. A B+ tree that stores the records in its leaves (choice 1) stays clustered under updates, at the cost of page splits and of record ids that change when a record moves; secondary indexes then often store the primary key instead of a physical record id.

**Primary is not the same as clustered.** In the terms of Ramakrishnan and Gehrke, a *primary index* is an index on a search key that contains the primary key, and a *secondary index* is any other. Whether an index is primary says nothing about the order of the file. Several systems cluster the table on its primary key by default, which is why the two words are often used for the same thing; other books use "primary index" for an index on the sort key of a sorted file.

## Examples

**The page simulator.** A table has $n = 1000$ records with keys $0$ to $999$, $p = 10$ per page, so 100 data pages. The B+ tree index has 50 entries per leaf and fanout 50, so 20 leaves and a root; its height is 2. The query is $200 \le A \le 299$, so $k = 100$ matches, all in leaves 4 and 5, and the index part costs $1 + 2 = 3$ I/Os in every layout.

| layout of the file | data I/Os, key order | data I/Os, sorted rids | total, key order |
|---|---|---|---|
| clustered: key $k$ on page $\lfloor k/10 \rfloor$ | 10 | 10 | 13 |
| striped: key $k$ on page $k \bmod 100$ | 100 | 100 | 103 |
| random order (`random.Random(7)`) | 98 | 65 | 101 |
| full scan, no index | | | 100 |

The clustered index reads exactly the 10 pages that hold the matches. The striped layout is the worst case for an unclustered index: every match is on a new page. The random file is close to it; sorting the record ids reduces the cost to 65 distinct pages, and Yao's formula gives $100(1 - \binom{990}{100} / \binom{1000}{100}) \approx 65.31$. At 10% selectivity the unclustered index already costs more than a full scan. For the whole table ($k = 1000$), the clustered index costs $21 + 100 = 121$ I/Os and the unclustered one $21 + 1000 = 1021$, against 100 for the scan.

**Equality on a key.** For $k = 1$ match, both cost $h + 1$ I/Os. A clustered index matters for ranges and for equality on keys that are not unique.

**A join.** An [index nested loop join](/index-nested-loop-join/) probes the index of the inner table once per outer row. If the outer rows come in key order and the inner index is clustered, consecutive probes land on the same or the next page, and the buffer turns many probes into one I/O.

## Where it is used

- Tables organized as a B+ tree on the primary key, as in InnoDB in MySQL and in SQL Server tables with a clustered index; Oracle calls them index-organized tables.
- Heap files sorted once on a key, as with PostgreSQL's `CLUSTER` command, which sorts the table once but does not keep the order under later updates.
- Physical design: choosing which index to cluster is part of [index selection](/index-selection/), and Ramakrishnan and Gehrke treat it as a main decision of physical tuning (Section 8.5.2), since range queries and grouping gain the most from it.
- A [zone map](/zone-map/) skips blocks only when the file is clustered on the column, and a [bulk load](/bulk-loading-b-tree/) of a B+ tree creates a clustered layout of its leaves by sorting.

## References
