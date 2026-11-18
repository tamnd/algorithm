---
tag: HJWXRS
kind: data-structure
slug: n-ary-storage-model
name: N-ary storage model
aliases:
- NSM
- row-oriented storage
- row store
area: databases/storage-and-indexing
level: core
summary: "Store each record contiguously in a slotted page, so that a whole row costs one page read. A scan of one column still reads every byte of every row."
model: external-memory-model
complexity:
  vars: {N: the number of records, m: the number of records that fit in one page, k: the number of attributes}
  io: {worst: "⌈N/m⌉", average: "⌈N/m⌉"}
  space: {extra: "O(N + k)"}
prereqs: [slotted-page, relational-model]
see_also: [decomposition-storage-model, pax-page-layout, slotted-page, heap-file, buffer-pool, vertical-fragmentation, late-materialization, vectorized-query-execution]
sources:
  - paper: "George P. Copeland and Setrag N. Khoshafian, A decomposition storage model, Proceedings of the 1985 ACM SIGMOD International Conference on Management of Data, 1985, 268 to 279"
    title: A decomposition storage model
    locator: the comparison of the decomposed layout with the usual layout of whole records
  - paper: "Anastassia Ailamaki, David J. DeWitt, Mark D. Hill and Marios Skounakis, Weaving relations for cache performance, Proceedings of the 27th International Conference on Very Large Data Bases (VLDB), 2001, 169 to 180"
    title: Weaving relations for cache performance
    locator: the section on NSM, its page layout and its cache behavior when a query reads one attribute
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: "Chapter 9 (storing data: disks and files), the sections on record formats and page formats"
  - paper: "Daniel Abadi, Peter Boncz, Stavros Harizopoulos, Stratos Idreos and Samuel Madden, The design and implementation of modern column-oriented database systems, Foundations and Trends in Databases 5(3), 2013, 197 to 280"
    title: The design and implementation of modern column-oriented database systems
    locator: the introduction, the comparison of row stores and column stores
---

The N-ary storage model (NSM) stores a table as whole records. All $k$ attribute values of a record lie next to each other in one [slotted page](/slotted-page/), and the pages of the table form a [heap file](/heap-file/). It is the layout of most row stores. The [decomposition storage model](/decomposition-storage-model/) is the opposite choice: it stores each attribute in its own file, so a scan of one attribute reads only that attribute, but a whole record must be put together from $k$ files. The [PAX layout](/pax-page-layout/) is in between: it keeps the records of a page in that page, as NSM does, but groups their values by attribute inside the page.

## In plain words

Think of a table as a pile of forms, one form per person, with the name, the age and the city on each form. NSM keeps each form whole and puts the forms in folders.

If you want everything about one person, you open one folder and take out one form. This is fast.

If you want only the ages of everybody, you must still take out every form and look at one line on each. You carry the names and cities around for nothing. A column store would keep a separate sheet with only the ages on it.

## The abstract type

An NSM file is a table of records over a schema of $k$ attributes, with record ids.

- `insert(t)`: store the record $t$ and return its record id (page, slot).
- `get(rid)`: return all $k$ values of the record.
- `attr(rid, j)`: return value $j$ of the record.
- `delete(rid)`: remove the record.
- `scan(J)`: return the values of the attributes in the set $J$ for every record.

## Representation

A page is a slotted page: a header $(n, e)$ with the number of slots and the start of the record area, then $n$ slots of 4 bytes, each with the offset and the length of one record, then free space, and the records at the end of the page. A deleted record has the slot $(0, 0)$.

A record is a *fixed part* followed by a *text part*. The fixed part has one field per attribute, in schema order. In the sample code, an int field holds the value in 8 bytes. A text field holds, in 2 bytes, the offset inside the record where the text of that attribute ends. The text part holds the bytes of the text values in schema order.

Let $f_j$ be the offset of field $j$ inside the fixed part and $F$ the size of the fixed part. These numbers depend only on the schema. A text value $j$ starts where the text value before it ends, or at $F$ if it is the first text value. So any attribute is found in a constant number of steps from the start of its record, and no field of another attribute is read on the way.

## Operations

```pseudo id=main
ENCODE(t)
L1  fixed ← empty; text ← empty
L2  for j ← 0 to k - 1 do
L3      if attribute j is an int then append t[j] to fixed (8 bytes)
L4      else append t[j] to text; append F + |text| to fixed (2 bytes)
L5  return fixed followed by text

INSERT(P, t)
L6  r ← ENCODE(t)
L7  if |r| + 4 > e - 4 - 4n then fail: page full
L8  e ← e - |r|; copy r to bytes [e, e + |r|)
L9  slot[n] ← (e, |r|); n ← n + 1
L10 return n - 1

ATTR(P, s, j)
L11 (o, ℓ) ← slot[s]
L12 if attribute j is an int then return bytes [o + f_j, o + f_j + 8)
L13 a ← F if j is the first text attribute, else the end stored in the field of the text attribute before j
L14 b ← the end stored at o + f_j
L15 return bytes [o + a, o + b)

SCAN(R, J)
L16 for each page P of R do
L17     for s ← 0 to n - 1 do
L18         if slot s is live then output ATTR(P, s, j) for each j in J
```

The file inserts into its last page and starts a new page when the last page is full. `get` is ATTR for every $j$. `delete` frees the slot; the bytes of the record stay as a hole until the page is compacted, as described on the slotted page.

## Example

Take a page of 64 bytes and the schema (id int, name text, age int). The fixed part has $f = (0, 8, 10)$ and $F = 18$.

| step | record bytes | $n$ | $e$ | slots | free bytes |
|---|---|---|---|---|---|
| start | | 0 | 64 | | 60 |
| insert (962, Jane, 30) | 22 at offset 42 | 1 | 42 | 0: (42, 22) | 34 |
| insert (7658, John, 45) | 22 at offset 20 | 2 | 20 | 0: (42, 22), 1: (20, 22) | 8 |

The first record holds 962 at bytes 42 to 49, the end 22 at bytes 50 and 51, the age 30 at bytes 52 to 59, and "Jane" at bytes 60 to 63. The end 22 is relative to the record: $F$ plus the 4 bytes of "Jane". A third record of 22 bytes needs 26 bytes with its slot, and only 8 are free, so the insert fails and the file starts a new page.

To read the age of record (page, 1), ATTR reads slot 1 at bytes 8 to 11, which gives $o = 20$, and then the 8 bytes at $20 + 10 = 30$. It reads no other byte of the page. A scan of all the ages reads the slots and one 8-byte field of each record, but the cache brings in whole cache lines, and these lines hold the ids and names too.

## Correctness

The invariant of the page is the one of the slotted page: the header, the slots and the records do not overlap, and the bytes of a live slot are the encoding of the record stored with it. Line L7 keeps it, since it allows a record only if the record and its new slot fit in the gap between the slots and the records.

The encoding is decodable because the field offsets $f_j$ are the same for every record and each text field stores where its text ends. The texts are stored in schema order, so the text of attribute $j$ is between the end of the text attribute before it, or $F$, and its own end, which is what lines L13 to L15 read. A scan visits each page and each slot once, and skips the free slots, so it returns every live record once, in record id order. The proof is in the proof file.

## Complexity

The page I/O is counted in the [external memory model](/external-memory-model/), with one page per block. In the external memory model, the memory holds M/B blocks; this is the number of buffer pages B of this page. Every operation here needs only one buffer page. The costs do not count the output, and they do not separate sequential and random I/O; a scan reads the pages in file order, which is sequential when the file is contiguous on disk.

| operation | page reads | CPU work |
|---|---|---|
| `insert` | 1 (plus a write) | $O(k + r)$ for a record of $r$ bytes |
| `get` | 1 | $O(k + r)$ |
| `attr` | 1 | $O(1)$ plus the length of the value |
| `scan(J)` | $\lceil N/m \rceil$ | $O(N \cdot \lvert J \rvert)$ plus the bytes returned |

When every record has $s$ bytes, a page holds $m = \lfloor (p - 4)/(s + 4) \rfloor$ records, so the scan reads $\lceil N/m \rceil$ pages *whatever $J$ is*. A scan of one attribute costs as much I/O as a scan of all $k$.

The same waste happens between memory and the CPU cache. Take ints only, $s = 8k$, and a cache line of $L$ bytes that divides $s$ and the page size. A scan of one attribute of a page with $c$ records reads $c + \lceil (4 + 4c)/L \rceil$ cache lines, one line per record plus the slots, while the full scan reads $cs/L + \lceil (4 + 4c)/L \rceil$. A dense array of the one attribute would take only $8c/L$ lines. With $p = 4096$, $k = 8$ and $L = 32$, a page holds 60 records, and the scan of one attribute reads 68 lines against 128 for all attributes and 15 for a dense array.

The space overhead is 4 bytes of slot per record and 2 bytes per text field, plus the header of each page.

## Variants

- **Null bitmap.** Most systems start a record with a bitmap of one bit per attribute that says whether the value is null, and leave out the fields of null values. PostgreSQL does this in its tuple header.
- **Records from the start of the page.** The records can also grow from the start of the page and the slots from the end. The choice does not change the costs.
- **Offsets for all fields.** Instead of the end of each text value, a record can store the start of every field. This costs more bytes but removes the dependency on the text attribute before.
- **Vertical partitions.** A table can be split into groups of attributes that queries read together, each stored in NSM. This is [vertical fragmentation](/vertical-fragmentation/), and DSM is the extreme with one attribute per group.

## When to use it

Use NSM when queries read or change whole records, or many attributes of few records: online transaction processing, inserts of single rows, and lookups by key through an index. A record is one page read, and an insert writes one page. Use a column layout, [DSM](/decomposition-storage-model/) or [PAX](/pax-page-layout/), when most queries scan a few attributes of many records.

## Pitfalls

- **Wide records and narrow scans.** A query that sums one int of a table with 50 attributes reads all 50 from disk and brings them through the cache. Adding an index on that attribute or a column copy helps; a faster disk does not change the ratio.
- **The field offsets depend on the text before.** If a record stores only lengths, as in a simple length-prefixed format, finding attribute $j$ needs a walk over all the text values before it. Store ends or offsets, as here.
- **Alignment.** Values that are not aligned to their size can cross a cache line or need slower loads on some CPUs. Systems often pad the fixed part, which costs space.
- **Records that grow.** An update that makes a record longer may not fit in its page; the slotted page then needs a forwarding address.

## Implementations

## History

Copeland and Khoshafian (1985) proposed the decomposition storage model as the alternative to the usual layout of whole records. Ailamaki, DeWitt, Hill and Skounakis (2001) call the usual layout the N-ary storage model, "a.k.a., slotted pages", measure its cache behavior, and propose PAX. Row stores such as PostgreSQL, MySQL with InnoDB and SQLite keep whole rows in their pages, in heap pages or in the leaves of B+ trees. Abadi, Boncz, Harizopoulos, Idreos and Madden (2013) survey the column stores that replaced NSM for analytic workloads.

## References
