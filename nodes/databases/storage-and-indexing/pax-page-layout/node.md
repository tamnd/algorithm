---
tag: 2CYGS7
kind: data-structure
slug: pax-page-layout
name: PAX page layout
aliases:
- partition attributes across
- PAX
area: databases/storage-and-indexing
level: advanced
summary: "Keep the records of a page in that page, as NSM does, but store their values by attribute in one minipage each, so that a scan of one attribute uses whole cache lines."
model: external-memory-model
complexity:
  vars: {N: the number of records, c: the number of records that fit in one page, k: the number of attributes, L: the size of a cache line in bytes}
  io: {worst: "⌈N/c⌉", average: "⌈N/c⌉"}
  space: {extra: "O(k⌈N/c⌉ + N)"}
prereqs: [n-ary-storage-model, decomposition-storage-model]
see_also: [n-ary-storage-model, decomposition-storage-model, slotted-page, late-materialization, zone-map, vectorized-query-execution, dictionary-encoding, vertical-fragmentation]
sources:
  - paper: "Anastassia Ailamaki, David J. DeWitt, Mark D. Hill and Marios Skounakis, Weaving relations for cache performance, Proceedings of the 27th International Conference on Very Large Data Bases (VLDB), 2001, 169 to 180"
    title: Weaving relations for cache performance
    locator: the abstract, the section on the design of PAX (page layout, F-minipages and V-minipages), the section on its implementation in Shore, and the evaluation
  - paper: "George P. Copeland and Setrag N. Khoshafian, A decomposition storage model, Proceedings of the 1985 ACM SIGMOD International Conference on Management of Data, 1985, 268 to 279"
    title: A decomposition storage model
    locator: the decomposed layout that PAX applies inside one page
  - paper: "Daniel Abadi, Peter Boncz, Stavros Harizopoulos, Stratos Idreos and Samuel Madden, The design and implementation of modern column-oriented database systems, Foundations and Trends in Databases 5(3), 2013, 197 to 280"
    title: The design and implementation of modern column-oriented database systems
    locator: the discussion of hybrid row and column layouts
---

PAX (partition attributes across) is a page layout. A page holds the same records as an [NSM](/n-ary-storage-model/) page would, but inside the page the values are grouped by attribute: one *minipage* holds the first attribute of every record of the page, the next minipage the second attribute, and so on. The I/O is the I/O of NSM, since a record is still in one page and a scan still reads every page. The cache behavior is that of the [decomposition storage model](/decomposition-storage-model/), since a scan of one attribute reads one contiguous minipage per page and every cache line it loads is full of useful values. Putting a record together needs only the $k$ minipages of one page, not $k$ files as in DSM.

## In plain words

Think of a folder that holds the forms of 60 people. NSM keeps each form whole. PAX cuts the forms apart inside the folder: one sheet with the 60 names, one sheet with the 60 ages, one with the 60 cities. The folder still holds exactly the same 60 people.

To add up the ages, you still open every folder, as before. But in each folder you read one short sheet with only ages on it, and your eyes do not pass over names and cities.

To see everything about person 12, you open one folder and read line 12 of each sheet. That is more work than one form, but much less than opening a separate folder for each sheet, as a column store must.

## The abstract type

A PAX file has the abstract type of an NSM file: a table of records over a schema of $k$ attributes, with record ids (page, slot).

- `insert(t)`: store $t$ and return its record id.
- `get(rid)`: return all $k$ values of the record.
- `attr(rid, j)`: return value $j$ of the record.
- `delete(rid)`: remove the record.
- `scan(J)`: return the attributes in the set $J$ of all records.

## Representation

A page of $p$ bytes has room for $c$ records, fixed when the page is formatted. It holds:

| part | contents |
|---|---|
| header | $n$ (records on the page), $c$, the start of each of the $k$ minipages, and one presence bit per record |
| F-minipage, for a fixed-width attribute | $c$ values of the attribute; the value of record $s$ is at $start_j + ws$ for width $w$ |
| V-minipage, for a variable-width attribute | $c$ ends of 2 bytes, then the values one after another; end $s$ is where the value of record $s$ ends |

In the sample code the fixed-width attributes are 8-byte ints, the variable-width attributes are texts, minipages start at multiples of 8, and the minipage of a text attribute is sized for an expected length $avg_j$ of its values. The capacity $c$ is the largest number for which the header and $c$ records of the expected size fit in the page.

The design of Ailamaki et al. (2001) has the same parts. Their header holds the number of attributes, the attribute sizes, the offsets of the minipages, the number of records and the free space. Their F-minipages end with a bit vector of presence bits, for null values, and their V-minipages hold the offsets of the ends of the values. The sample code keeps a single presence bit per record in the header and uses it for deletes; it has no nulls.

## Operations

```pseudo id=main
FORMAT(P)
L1  c ← the largest count for which the header and c records of the expected size fit in p bytes
L2  give minipage j the bytes for c values of attribute j, one minipage after another

INSERT(P, t)
L3  if n = c then fail: page full
L4  if the value of some text attribute j is longer than the free part of minipage j then fail: page full
L5  for j ← 0 to k - 1 do
L6      if attribute j has fixed width w then write t[j] at start_j + w n
L7      else write t[j] after the value of record n - 1 in minipage j, and store its end as end n
L8  set presence bit n; n ← n + 1; return n - 1

ATTR(P, s, j)
L9  if attribute j has fixed width w then return bytes [start_j + w s, start_j + w s + w)
L10 a ← end s - 1 of minipage j, or 0 if s = 0; b ← end s
L11 return the bytes from a to b of the values of minipage j

SCAN(P, J)
L12 for s ← 0 to n - 1 do
L13     if presence bit s is set then output ATTR(P, s, j) for each j in J
```

The file inserts into its last page and formats a new page when the last page refuses a record. `get` is ATTR for every $j$: Ailamaki et al. call this the *mini-join* of the minipages. `delete` clears the presence bit; the values stay until the page is rebuilt.

## Example

Take a page of 128 bytes, the schema (ssn int, name text, age int), and an expected name length of 4 bytes, so a record is expected to take $8 + (2 + 4) + 8 = 22$ bytes. The header takes $4 + 2 \cdot 3 + 1 = 11$ bytes. With $c = 5$ the minipages start at 16, 56 and 88, and the last one ends at exactly 128, so $c = 5$ is the capacity. Insert (962, Jane, 30) and (7658, John, 45), as in the figure of the PAX paper.

| bytes | contents |
|---|---|
| 0 to 9 | $n = 2$, $c = 5$, starts 16, 56, 88 |
| 10 | presence bits 00000011 |
| 16 to 31 | 962, 7658 |
| 56 to 59 | ends 4, 8 |
| 66 to 73 | "JaneJohn" |
| 88 to 103 | 30, 45 |

A scan of the ages reads the header and bytes 88 to 103, which are next to each other. The texts of the names minipage start at $56 + 2 \cdot 5 = 66$ and end at 88, so they have 22 bytes, of which 8 are used. A record with a name of 15 bytes is refused, even though only 2 of the 5 places are used, and goes to a new page. A name of 14 bytes fits.

## Correctness

The minipages are placed one after another after the header and the last one ends inside the page, so they do not overlap. A value of an F-minipage is at a position fixed by its slot, and the test $n < c$ at line L3 keeps it inside its minipage. In a V-minipage, each value is written right after the previous one and its end is stored, so the value of slot $s$ is the bytes between end $s - 1$ and end $s$, and line L4 keeps the last end inside the minipage. The presence bits tell SCAN which slots are live. So ATTR returns the value that was inserted, and SCAN returns each live record once. The proof file has the details and the cache line count.

## Complexity

The page I/O is counted in the [external memory model](/external-memory-model/), with one page per block. In the external memory model, the memory holds M/B blocks; this is the number of buffer pages B of this page. Every operation needs one buffer page. The costs do not count the output and do not separate sequential and random I/O; a scan reads the pages in file order. The I/O is the I/O of NSM: `get`, `attr`, `insert` and `delete` read one page, and `scan(J)` reads all $\lceil N/c \rceil$ pages whatever $J$ is.

The gain is between memory and the CPU cache. A scan of one int attribute of a page with $n$ records reads the header and the $8n$ bytes of one minipage, so it touches about $\lceil H/L \rceil + 8n/L$ cache lines for a header of $H$ bytes, where NSM touches one line per record. With $p = 4096$, $k = 8$ int attributes and $L = 32$:

| layout | records per page | lines read per page, one attribute | lines per record |
|---|---|---|---|
| NSM | 60 | 68 | 1.13 |
| PAX | 63 | 17 | 0.27 |
| DSM, one column | 511 | 128 | 0.25 |

PAX holds a few more records per page than this NSM, since it needs no slot per record, only one presence bit. The CPU work of a scan is $O(n \lvert J \rvert)$ per page, and `get` reads $k$ minipages, $O(k)$ plus the length of the values.

## Variants

- **Minipage boundaries.** The sample code fixes the size of each V-minipage when it formats the page and starts a new page when one minipage fills. A system can instead move the minipage boundaries inside the page when the other minipages have room, at the cost of moving their values.
- **Nulls.** Per-minipage presence bits, as in the paper, mark null values of fixed-width attributes without a separate null bitmap per record.
- **Row groups.** Parquet and ORC split a file into groups of rows and store each group by column. This is the PAX idea at the scale of megabytes: a group holds whole records, and inside it each column is contiguous, with a [zone map](/zone-map/) per column chunk.
- **Compression per minipage.** Since a minipage holds values of one attribute, it can be compressed with [dictionary encoding](/dictionary-encoding/) or [frame of reference encoding](/frame-of-reference-encoding/) independently of the others.

## When to use it

Use PAX when a system stores records in pages, as a row store does, but many queries scan a few attributes of many records in memory. It changes only the layout inside the page, so the buffer pool, the record ids and the recovery code stay the same as for NSM. When the data is on disk and the scans read few attributes, a column layout such as [DSM](/decomposition-storage-model/) saves I/O as well, which PAX cannot do.

## Pitfalls

- **No I/O saving.** PAX reads every page of the table for a scan of one attribute. It speeds up the work after the page is in memory, not the reads.
- **Variable-width values.** The expected sizes of the V-minipages decide the capacity. A bad guess leaves most of a page empty when one text attribute fills first.
- **Updates that grow a value.** A longer value in the middle of a V-minipage shifts the values after it and changes their ends.
- **Record access touches $k$ places.** `get` reads one value from each minipage, so it touches up to $k$ cache lines, where NSM touches $\lceil s/L \rceil$ for a record of $s$ bytes.

## Implementations

## History

Ailamaki, DeWitt, Hill and Skounakis (2001) proposed PAX and built it in the Shore storage manager. They report that it saves at least 75% of the stall time due to data cache accesses compared with NSM, that it runs range selections and updates on memory-resident relations 17 to 25% faster, and that it runs TPC-H queries that do I/O 11 to 48% faster, with no storage penalty and the same I/O as NSM. They compared it with NSM, which they describe as "a.k.a., slotted pages", and with DSM, stored as one file of (id, value) pairs per attribute, which needed costly record reconstruction for queries on many attributes. The row groups of Parquet and ORC follow the same idea at a larger scale.

## References
