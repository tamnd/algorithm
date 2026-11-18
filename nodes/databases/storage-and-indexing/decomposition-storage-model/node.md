---
tag: Y6XVQQ
kind: data-structure
slug: decomposition-storage-model
name: Decomposition storage model
aliases:
- DSM
- column-oriented storage
- column store
area: databases/storage-and-indexing
level: core
summary: "Store each attribute of a table in its own file of values, in record order, so that a scan reads only the columns it needs. A whole record costs one page per column."
model: external-memory-model
complexity:
  vars: {N: the number of records, m: the number of values in one page, k: the number of attributes, a: the number of attributes that a scan reads}
  io: {worst: "a⌈N/m⌉", average: "a⌈N/m⌉"}
  space: {extra: "O(k⌈N/m⌉)"}
prereqs: [n-ary-storage-model]
see_also: [n-ary-storage-model, pax-page-layout, late-materialization, dictionary-encoding, vertical-fragmentation, vectorized-query-execution, zone-map, run-length-encoding]
sources:
  - paper: "George P. Copeland and Setrag N. Khoshafian, A decomposition storage model, Proceedings of the 1985 ACM SIGMOD International Conference on Management of Data, 1985, 268 to 279"
    title: A decomposition storage model
    locator: the definition of the decomposed layout as binary relations of a surrogate and one attribute, and its comparison with n-ary storage
  - paper: "Anastassia Ailamaki, David J. DeWitt, Mark D. Hill and Marios Skounakis, Weaving relations for cache performance, Proceedings of the 27th International Conference on Very Large Data Bases (VLDB), 2001, 169 to 180"
    title: Weaving relations for cache performance
    locator: the section on DSM and the measurements of record reconstruction
  - paper: "Daniel Abadi, Peter Boncz, Stavros Harizopoulos, Stratos Idreos and Samuel Madden, The design and implementation of modern column-oriented database systems, Foundations and Trends in Databases 5(3), 2013, 197 to 280"
    title: The design and implementation of modern column-oriented database systems
    locator: the history of column stores and the chapters on column storage and tuple reconstruction
---

The decomposition storage model (DSM) stores a table of $k$ attributes as $k$ separate files, one per attribute. Record $i$ is the $i$-th value of every file. A query that reads $a$ of the $k$ attributes reads only those $a$ files, and the values it reads lie next to each other, which suits the disk and the CPU cache. The price is that a whole record is spread over $k$ pages. The [N-ary storage model](/n-ary-storage-model/) makes the opposite choice: whole records in one page, cheap to fetch, but a scan of one attribute reads them all. The [PAX layout](/pax-page-layout/) keeps whole records in one page, as NSM does, and groups their values by attribute inside the page, so it has the cache behavior of DSM and the I/O of NSM.

## In plain words

Think of a table of people with a name, an age and a city. A column store writes all the names on one sheet, all the ages on a second sheet and all the cities on a third, in the same order of people.

To add up all the ages, you read only the age sheet. You never touch the names or the cities.

To see everything about person number 12, you look at line 12 of each of the three sheets. That is three sheets to open instead of one, and you must keep the order of the people the same on every sheet.

## The abstract type

A DSM table is a sequence of records over a schema of $k$ attributes. Positions $0, 1, \ldots, N - 1$ act as record ids.

- `append(t)`: add record $t$ at position $N$ and return $N$.
- `fetch(i, J)`: return the attributes in the set $J$ of the record at position $i$.
- `scan(J)`: return the attributes $J$ of all records, in position order.

Deletes and updates in place are possible but costly; see the pitfalls.

## Representation

Column $j$ is a list of pages. A page has a header $(n, e)$, with the number of entries and the start of the text area, then $n$ entries of the same size, and, for a text column, the texts at the end of the page. In the sample code an entry of an int column is the 8-byte value, and an entry of a text column is the offset and the length of its text, 2 bytes each.

The table keeps, for each column, the list $first_j$ of the positions of the first value of each page. Entry $x$ of page $q$ of column $j$ is attribute $j$ of record $first_j(q) + x$. When all values of a column have the same width, page $q$ starts at position $qm$ and this list is not needed.

Copeland and Khoshafian store each column as a binary relation of pairs (surrogate, value), so each entry also holds the record id. Modern column stores leave the id out and use the position, a *virtual id*. The sample code does both: with ids on, an entry takes 16 bytes instead of 8, and a page holds half as many values.

## Operations

```pseudo id=main
APPEND(R, t)
L1  i ← N; N ← N + 1
L2  for j ← 0 to k - 1 do
L3      P ← the last page of column j
L4      if there is no P, or the entry and the text of t[j] do not fit in P then
L5          P ← a new page of column j; append i to first_j
L6      write the entry of t[j] (with id i, if ids are stored) as entry n of P; n ← n + 1
L7  return i

FETCH(R, i, J)
L8  for each j in J do
L9      q ← the largest page number with first_j(q) ≤ i      ▷ binary search
L10     v_j ← entry i - first_j(q) of page q of column j
L11 return (v_j for each j in J)

SCAN(R, J)
L12 for each j in J, put a cursor before the first page of column j
L13 for i ← 0 to N - 1 do
L14     for each j in J: v_j ← the next entry of cursor j, moving to the next page of column j when a page ends
L15     output (v_j for each j in J)
```

SCAN reads the columns in step, all at the same position. A real system reads a block of values of one column at a time, as in [vectorized execution](/vectorized-query-execution/), and often delays putting the values of a row together; this is [late materialization](/late-materialization/).

## Example

Take pages of 64 bytes, the schema (id int, name text, age int), and the records (962, Jane, 30) and (7658, John, 45).

| column | header $(n, e)$ | entries | text area |
|---|---|---|---|
| id | (2, 64) | 962 at bytes 4 to 11, 7658 at bytes 12 to 19 | none |
| name | (2, 56) | (60, 4) at bytes 4 to 7, (56, 4) at bytes 8 to 11 | "JohnJane" at bytes 56 to 63 |
| age | (2, 64) | 30 at bytes 4 to 11, 45 at bytes 12 to 19 | none |

A scan of the ages reads one page and, in it, the header and bytes 4 to 19. The id and name pages are not read. To fetch record 1, the table reads entry 1 of each column: three pages, one per attribute. An int page holds $\lfloor 60/8 \rfloor = 7$ values, so the third record still goes to the same pages, and the eighth starts a new page of each int column.

## Correctness

The invariant is that, for each column, the pages cover the positions $0$ to $N - 1$ in order without gaps: $first_j(0) = 0$, each page starts where the one before it ends, and entry $x$ of page $q$ is attribute $j$ of record $first_j(q) + x$. APPEND keeps it, because the new value goes to the last page at the position where that page ends, or to a new page whose first position is $N$. Line L4 lets a value into a page only if its entry stays below the text area and its text stays above the entries, so no bytes of two values overlap.

FETCH is correct because the binary search at line L9 finds the one page whose range of positions holds $i$. SCAN is correct because each cursor moves to the next page exactly when it has used all the entries of its page, so it is always at position $i$. The proof file has the details.

## Complexity

The page I/O is counted in the [external memory model](/external-memory-model/), with one page per block. In the external memory model, the memory holds M/B blocks; this is the number of buffer pages B of this page. A scan of $a$ columns needs $a$ buffer pages, one per cursor. The costs do not count the output. They do not separate sequential and random I/O, but this matters here: each column is read in order, and a scan of $a$ columns switches between $a$ files, which a system reads in large blocks to keep the access sequential.

| operation | page reads | CPU work |
|---|---|---|
| `append` | $k$ (plus $k$ writes) | $O(k)$ plus the length of the texts |
| `fetch(i, J)` | $\lvert J \rvert$ | $O(\lvert J \rvert \log(N/m))$ for the binary searches |
| `scan(J)` | $a \lceil N/m \rceil$ for $a = \lvert J \rvert$ columns | $O(N a)$ |

For an int column, a page of $p$ bytes holds $m = \lfloor (p - 4)/8 \rfloor$ values, or $\lfloor (p - 4)/16 \rfloor$ with ids. For $k$ int attributes in NSM, a page holds $\lfloor (p - 4)/(8k + 4) \rfloor$ records, and every scan reads all pages. So a scan of $a$ attributes in DSM reads about $a/k$ of the pages that NSM reads, a little less because DSM needs no slots. With $p = 4096$ and $k = 8$, NSM holds 60 records per page and DSM 511 values per page, and a scan of one attribute of $10^6$ records reads 16,667 pages in NSM and 1,957 in DSM.

In the cache, a page of $c$ int values costs $\lceil (4 + 8c)/L \rceil$ lines of $L$ bytes: no byte of another attribute comes into the cache. With ids, every line holds half as many values.

## Variants

- **Virtual ids or stored ids.** Storing the id with each value, as in the binary relations of Copeland and Khoshafian, doubles the size of an int column. With dense positions the id is implicit. MonetDB stores columns as binary association tables whose head is a dense sequence of ids, which is not stored.
- **A second copy sorted by value.** A copy of a column as (value, id) pairs sorted by value works as an index: a range predicate becomes a search, and the ids it returns select the other attributes.
- **Sorted projections.** C-Store and Vertica store groups of columns, each group sorted on some of its attributes, so that the sorted columns compress well and range predicates on them read a contiguous range.
- **Compression.** Values of one column have one type and often few distinct values, so a column compresses far better than a row. See [dictionary encoding](/dictionary-encoding/), [run-length encoding](/run-length-encoding/) and [frame of reference encoding](/frame-of-reference-encoding/).
- **Row groups.** Parquet and ORC files split a table into groups of rows and store each group by column, with a [zone map](/zone-map/) per column chunk. Inside one group this is DSM, and at the scale of files it is close to [PAX](/pax-page-layout/).

## When to use it

Use DSM for analytic workloads: queries that scan a few attributes of many records, aggregate them and return a small result. Use it when the data is loaded in bulk and changed rarely. Do not use it for workloads that insert, update or fetch single whole records, where each record costs $k$ page writes or reads; use [NSM](/n-ary-storage-model/) there.

## Pitfalls

- **Tuple reconstruction.** A query that needs many attributes of the qualifying records must join the columns by position. With random positions, each value is a random page read. Delay reconstruction until after the selective operators, and fetch the positions in sorted order.
- **Single-row writes.** An insert writes one page per column, and an update in place of a compressed column may need to rewrite a block. Systems buffer new rows in a row store and merge them into the columns in batches, as in the write store of C-Store.
- **Deletes.** Removing a value from the middle of a column shifts the positions of all later values, which breaks the alignment of the columns. Mark deleted positions in a bitmap and remove them only when the columns are rewritten together.
- **Alignment of columns.** Every column must have the same number of values in the same order. A crash in the middle of APPEND can leave the columns of different lengths, so the append must be atomic, for instance under [write-ahead logging](/write-ahead-logging/).
- **Variable-width values.** Without a fixed width, position $i$ is no longer at a known offset. Keep a list of first positions per page, or store fixed-width codes from a dictionary.

## Implementations

## History

Copeland and Khoshafian (1985) proposed the decomposition storage model and compared it, along several dimensions, with the n-ary storage models that systems used. Ailamaki, DeWitt, Hill and Skounakis (2001) measured DSM against NSM and PAX in the Shore storage manager, storing DSM as $k$ files of (id, value) pairs, and found that record reconstruction made DSM slow for queries on many attributes. MonetDB, from the 1990s, built its query processing on columns. C-Store and the column stores of the 2000s, surveyed by Abadi, Boncz, Harizopoulos, Idreos and Madden (2013), added compression, sorted projections and late materialization, and made column storage the standard layout for analytic databases.

## References
