---
tag: A543GS
kind: definition
slug: dense-and-sparse-index
name: Dense and sparse indexes
aliases:
- dense index
- sparse index
area: databases/storage-and-indexing
level: intro
summary: "A dense index has an entry for every search key value of the file. A sparse index has one entry per block, and it works only on a file sorted on the key."
prereqs: [external-memory-model, binary-search]
see_also: [clustered-index, b-plus-tree, zone-map, covering-index, heap-file, bulk-loading-b-tree, partial-index, inverted-index]
sources:
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson Prentice Hall (2009)
    locator: "Section 14.1, Index-Structure Basics: 14.1.1 sequential files, 14.1.2 dense indexes, 14.1.3 sparse indexes, 14.1.4 multiple levels of index, 14.1.5 secondary indexes"
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: Chapter 8, Overview of Storage and Indexing (data entries, clustered and unclustered indexes), chapter level only
  - paper: doi:10.1561/1900000028
    title: "Goetz Graefe, Modern B-tree techniques, Foundations and Trends in Databases 3(4) (2011)"
    locator: pp. 203 to 402, the sections on the basic B-tree structure, where the upper levels of a B+ tree are a sparse index over the leaves (section level only)
---

An index on a file is *dense* if it has an entry for every search key value that occurs in the file, and *sparse* if it has one entry for each block of the file. A sparse index is much smaller, but it can find a record only when the file is sorted on the search key, so a file has at most one useful sparse index. The words describe how many entries an index has; whether the order of the file follows the key is the separate idea of a [clustered index](/clustered-index/).

## Definition

**Setting.** A data file holds $n$ records in $N$ blocks (pages), and each record has a value of a search key $K$. An *index entry* is a pair $(k, p)$ of a key value $k$ and a pointer $p$, to a record or to a block. An index file keeps its entries sorted on $k$, so a lookup can do a [binary search](/binary-search/) over the index blocks. Costs on this page are in the page I/O model: one block read is one I/O, and the index and data blocks are not in memory unless the text says so. In the [external memory model](/external-memory-model/), the memory holds M/B blocks; this page uses only block reads, so it needs no buffer size.

**Dense index.** An index is dense if, for every value $k$ of $K$ that occurs in the file, the index has an entry with key $k$. If $K$ is a key of the file (no two records have the same value), a dense index has $n$ entries, one per record. If values repeat, there are two forms: one entry for each record, or one entry for each distinct value that points to the first record with that value, which then needs a file sorted on $K$. A dense index can answer "is there a record with $K = k$?" without a read of the data file.

**Sparse index.** Let the file be sorted on $K$, and let $f_j$ be the key of the first record in block $j$, for $j = 0, \ldots, N - 1$. The sparse index has the $N$ entries $(f_j, j)$. To find the records with $K = k$:

1. Find the largest $j$ with $f_j < k$. If there is none, let $j = 0$.
2. Read block $j$ and the blocks after it, in order, until a record with key greater than $k$ appears or the file ends. Return the records with key $k$.

If $K$ has no duplicates, the search can start at the largest $j$ with $f_j \le k$, and it reads exactly one data block. With duplicates, the strict test $f_j < k$ is needed, because the records with key $k$ can begin at the end of block $j - 1$ when $f_j = k$.

**Why a sparse index needs a sorted file.** Step 2 is correct because every record in blocks $0, \ldots, j - 1$ has a key at most $f_j < k$ and every record from block $j + 1$ onward has a key at least $f_{j+1}$. If the file is not sorted on $K$, a record with key $k$ can be in any block, and the entry of a block says nothing about the keys of the records in it. So a sparse index can exist on at most one key order of a file, and every other index on the file (a *secondary index*) must be dense.

**Sizes.** If an index block holds $f$ entries, a dense index on a key has $\lceil n / f \rceil$ blocks and a sparse index has $\lceil N / f \rceil$ blocks. A binary search over $b$ sorted blocks reads at most $\lfloor \log_2 b \rfloor + 1$ of them.

**Multiple levels.** An index file is itself sorted on $k$, so a sparse index on the index is always possible. Repeat this until the top level fits in one block. The result is a static tree of sparse indexes. A [B+ tree](/b-plus-tree/) is the dynamic form: its leaves are a dense index (or hold the records), and its upper levels are a sparse index over the leaves.

## Examples and non-examples

**A small file.** Take 12 records with keys $10, 20, \ldots, 120$, three records per block, sorted on the key. The file has $N = 4$ blocks: $[10, 20, 30]$, $[40, 50, 60]$, $[70, 80, 90]$ and $[100, 110, 120]$.

- The dense index has 12 entries $(10, r_0), (20, r_1), \ldots, (120, r_{11})$.
- The sparse index has 4 entries $(10, 0), (40, 1), (70, 2), (100, 3)$.
- A lookup of 80 in the sparse index finds the largest first key at most 80, which is 70, reads block 2 and finds the record. A lookup of 85 also reads block 2 and finds nothing. The dense index answers 85 with no data read, because 85 is not among its keys.

**Duplicates.** Keys $10, 20, 20, 20, 20, 30$ in blocks of three give the blocks $[10, 20, 20]$ and $[20, 20, 30]$, with first keys $f_0 = 10$ and $f_1 = 20$. A search for 20 that starts at the largest $f_j \le 20$ reads only block 1 and misses two records. The rule "largest $f_j < 20$" starts at block 0 and finds all four.

**Sizes with real numbers.** A file of $n = 1\,000\,000$ records with 10 records per block has $N = 100\,000$ blocks. With $f = 256$ entries per index block (an 8-byte key and an 8-byte pointer in a 4096-byte block), the dense index has $\lceil 10^6 / 256 \rceil = 3907$ blocks and the sparse index has $\lceil 10^5 / 256 \rceil = 391$ blocks. A binary search reads at most 12 index blocks of the dense index and at most 9 of the sparse one, plus one data block. A second level of sparse index has 16 blocks over the dense index and 2 blocks over the sparse index. If that level stays in memory, a lookup costs 2 block reads in both cases. The sparse index is about 10 times smaller, which is the number of records per block.

**Non-examples.**

- A one-entry-per-block index on a [heap file](/heap-file/) in insertion order is not a sparse index. It cannot locate a key, because the blocks are not sorted on it.
- A [zone map](/zone-map/) keeps the minimum and the maximum of a column for each block of an unsorted file. It looks like a sparse index, but it only tells which blocks *cannot* hold the value. On unsorted data many zones can overlap a value, and the scan must read them all.
- A secondary index on a second column of a sorted file cannot be sparse. It must be dense, often with a list of record pointers for each value.

## Related definitions

- [Clustered index](/clustered-index/): the order of the file follows the index key. A sparse index is always clustered. A clustered index can be dense or sparse, and an unclustered index is always dense.
- [Covering index](/covering-index/): a dense index whose entries hold every column a query needs, so the query never reads the file.
- [B+ tree](/b-plus-tree/) and [bulk loading](/bulk-loading-b-tree/): the dynamic and the built-from-sorted-data forms of a multilevel index.
- [Partial index](/partial-index/): an index with entries only for the records that satisfy a predicate. It is dense on that subset and has no entries for the rest.
- [Inverted index](/inverted-index/): a dense index from each term to the list of documents that contain it.

## References
