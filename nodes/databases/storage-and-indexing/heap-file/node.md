---
tag: FWEZG7
kind: data-structure
slug: heap-file
name: Heap file
aliases:
- unordered file
- heap-organized table
area: databases/storage-and-indexing
level: intro
summary: "An unordered file of records in pages, with a page directory or two linked lists to find free space. It is the default storage of a table."
model: external-memory-model
complexity:
  vars: {N: the number of data pages, D: the number of entries in one directory page, F: the number of pages on the free list}
  io: {worst: "N + ⌈N/D⌉", average: "N + ⌈N/D⌉"}
  space: {extra: "⌈N/D⌉"}
prereqs: [slotted-page]
see_also: [slotted-page, buffer-pool, b-plus-tree, clustered-index, zone-map, n-ary-storage-model, free-list, log-structured-merge-tree]
sources:
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: "Chapter 8 (overview of storage and indexing), the cost comparison of file organizations; Chapter 9 (storing data: disks and files), files of records and the two implementations of heap files"
  - book: isbn:9781558601901
    title: Jim Gray and Andreas Reuter, Transaction Processing, Concepts and Techniques, Morgan Kaufmann (1993)
    locator: the chapters on file and buffer management and on the tuple-oriented file system, the entry-sequenced file and free space administration
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson (2009)
    locator: the chapter on data storage, the representation of records and of blocks
  - url: https://www.postgresql.org/docs/current/storage-fsm.html
    title: "PostgreSQL documentation, Free space map"
    locator: the free space map of a relation, a separate fork with the free space of each heap page
---

A heap file stores the records of a table in pages, in no particular order. A record goes into any page that has room, and a record id (page id, slot) names it for as long as it exists. The only extra structure is the one that finds a page with free space: a *page directory*, with one entry (page id, free bytes) per page, or two *linked lists* of pages, one of the pages with free space and one of the full pages. Inside each page the records are kept in a [slotted page](/slotted-page/); the slotted page is about the layout of one page, and the heap file is about how a table is spread over many pages. A heap file supports a full scan and an access by record id; any search on a value needs a scan or an index such as a [B+ tree](/b-plus-tree/).

## In plain words

A heap file is a stack of pages with records in them, in the order they happened to arrive. Nothing keeps them sorted. To find a record by its address, "page 12, slot 3", you go straight to page 12. To find a record by a value, you read every page, unless an index tells you where to look.

When you add a record, you need a page with enough room. One way is to keep a short list of all pages with the free room on each, and look it up. The other way is to keep the pages that still have room in a chain, and walk the chain until one is big enough.

## The abstract type

A heap file is a bag of records with ids.

- `insert(H, r)`: store record $r$ in some page and return its record id.
- `get(H, rid)`: the record with id $rid$.
- `delete(H, rid)`: remove the record.
- `scan(H)`: every record with its id, each once, in some order.

The file gives no order, and an insert may go to any page with room. Updates are a delete and an insert in the worst case, or an update in place inside the slotted page; a record that grows out of its page keeps its id through a forwarding address, as on the slotted page.

## Representation

The data pages have ids $0, 1, \ldots, N - 1$. A record of $\ell$ bytes costs $\ell + 4$ bytes of its page: the bytes and a slot entry.

**Page directory.** A chain of directory pages, each with up to $D$ entries (page id, free bytes). The entries are in page id order, so the entry of page $q$ is entry $q \bmod D$ of directory page $\lfloor q / D \rfloor$. The first directory page is at a known place, often the header page of the file, so an empty file still has one directory page. The invariant is that the entry of every page holds its exact free space, and every data page has one entry.

**Linked lists.** A header page holds the heads of two doubly linked lists. Each data page holds a pointer to the page before it and to the page after it on its list. A page is on the *full list* if its free space is below a limit $m$, and on the *free list* otherwise. The invariant is that every data page is on exactly one list, the one its free space calls for.

The directory costs $\lceil N / D \rceil$ extra pages; with entries of 8 bytes in 4 KB pages, $D$ is about 500, so a directory page covers 2 MB of data. The lists cost two pointers in each data page and one header page.

## Operations

```pseudo id=main
DIR-INSERT(H, r)                           ▷ page directory form
L1  for each directory page j, in order do
L2      read directory page j
L3      for each entry (q, f) of page j do
L4          if f ≥ |r| + 4 then
L5              read page q; put r in q at slot s
L6              write page q
L7              f ← the free space of q; write directory page j
L8              return (q, s)
L9  q ← a new page id; put r in a new page q at slot s
L10 write page q
L11 if the last directory page has D entries then
L12     add a new directory page and link the old last page to it
L13 append (q, the free space of q) to the last directory page; write it
L14 return (q, s)

DIR-SCAN(H)
L15 for each directory page j, in order do
L16     read directory page j
L17     for each entry (q, f) of page j do
L18         read page q
L19         for each live slot s of q do
L20             output ((q, s), the record of slot s)

GET(H, (q, s))
L21 read page q; return the record of slot s

LIST-INSERT(H, r)                          ▷ linked list form, limit m
L22 read the header page; q ← the head of the free list
L23 while q ≠ nil do
L24     read page q
L25     if |r| + 4 ≤ free(q) then
L26         put r in q at slot s; write page q
L27         if free(q) < m then
L28             unlink q from the free list; push q on the full list
L29         return (q, s)
L30     q ← next(q)
L31 q ← a new page id; put r in a new page q at slot s
L32 push q on the free list, or on the full list if free(q) < m
L33 return (q, s)
```

A delete reads the page of the record, frees the slot and writes the page. With a directory, it also reads and writes the directory page of that page, to update its free space. With the lists, a page that was full and now has $m$ or more free bytes moves back to the free list. A move between lists changes the pointers of the page, its old neighbors, the old head of the other list, and the header.

A scan of the list form reads the header page and walks the full list and then the free list. It visits each data page once, because each page is on exactly one list.

## Example

Take pages of 100 bytes and a directory with $D = 2$ entries per page. Insert records of 56, 46, 36, 26 and 26 bytes; they cost 60, 50, 40, 30 and 30 bytes of a page.

| step | goes to | directory after the step | reads | writes |
|---|---|---|---|---|
| insert 56 | new page 0, slot 0 | (0, 40) | 1 | 2 |
| insert 46 | new page 1, slot 0 | (0, 40) (1, 50) | 1 | 2 |
| insert 36 | page 0, slot 1 | (0, 0) (1, 50) | 2 | 2 |
| insert 26 | page 1, slot 1 | (0, 0) (1, 20) | 2 | 2 |
| insert 26 | new page 2, slot 0 | (0, 0) (1, 20) / (2, 70) | 1 | 3 |
| delete (1, 0) | | (0, 0) (1, 70) / (2, 70) | 2 | 2 |
| insert 30 | page 1, slot 0 | (0, 0) (1, 36) / (2, 70) | 2 | 2 |

The slash separates the two directory pages. The fifth insert finds no page with 30 free bytes, makes page 2, and needs a second directory page, so it writes the new data page and both directory pages. The last insert reuses slot 0 of page 1, so the new record has the id of the deleted one; an index must not still hold that id (see the pitfalls). A scan now reads 2 directory pages and 3 data pages.

With linked lists and $m = 20$, the same five inserts end with pages 0 and 1 on the full list (free space 10 each) and page 2 on the free list. Here the third insert goes to page 1, the head of the free list, and not to page 0, so the record ids differ from the directory form. After the delete of (1, 0), page 1 has 60 free bytes and moves back to the head of the free list. A scan reads the header and 3 data pages.

## Correctness

Each record is in exactly one slot of one page, and its id is the place of that slot, which does not change while the record exists. So `get` finds it with one read and `scan` returns it once, provided that the scan visits each data page once. With a directory, the scan visits the pages of the entries, and each data page has exactly one entry. With the lists, the scan visits the pages of the two lists, and each data page is on exactly one list.

DIR-INSERT keeps the directory exact: line L7 writes the new free space of the page that took the record, and line L13 adds the entry of a new page. It puts a record in an existing page only if the entry shows enough free space, and since the entry is exact, the record fits. LIST-INSERT does the same with the free space stored in the page itself, and lines L27 and L28 keep each page on the list that its free space calls for. The full proof is below.

## Complexity

The costs count page reads and writes in the [external memory model](/external-memory-model/), with one page per block. In the external memory model, the memory holds M/B blocks; this is the number of buffer pages B of this page. Each operation here needs only two or three buffer pages, and the costs assume that no page is in the [buffer pool](/buffer-pool/) when the operation starts. The costs do not count the output of a scan. They do not separate sequential and random I/O, but a scan of a directory file can read the data pages in page id order, which is sequential when the pages are contiguous on disk, while the list form reads them in list order.

| operation | page directory | linked lists |
|---|---|---|
| `scan` | $N + \lceil N/D \rceil$ reads | $N + 1$ reads |
| `get` | 1 read | 1 read |
| `insert` into page $q$ | $\lfloor q/D \rfloor + 2$ reads, 2 writes | $k + 1$ reads and 1 write, if $q$ is the $k$-th page of the free list and stays on it |
| `insert` into a new page | $\lceil N/D \rceil$ reads, 2 or 3 writes | at most $F + 2$ reads and 3 writes |
| `delete` | 2 reads, 2 writes | 1 read and 1 write, or at most 5 of each when the page changes lists |

The search for free space is the weak point of both forms. The directory scans $\lceil N/D \rceil$ pages in the worst case, which is small, since one directory page covers $D$ data pages. The free list can hold $F$ pages that each have a little free space but not enough for a large record, and an insert may read all of them. This is why systems prefer a directory or a separate free space map.

Ramakrishnan and Gehrke compare a heap file with sorted and hashed files in a simpler model, where the file has $N$ pages and inserts go to the last page. A scan costs $N$ page reads, a search for one record with a given key costs $N/2$ reads on average, a search for a range costs $N$ reads, and an insert costs 2: read the last page and write it back. A sorted file finds one record in about $\log_2 N$ reads, but an insert must move half of the file on average.

## Variants

- **Free space map.** PostgreSQL keeps the free space of each heap page in a separate file (a fork of the relation), organized as a small tree of pages, so that a search for a page with $x$ free bytes reads a few pages and not the whole directory. This is a directory with an index on its free space values.
- **Coarse free space classes.** Some systems store only a few bits per page, a class of the free space (for example less than 25%, 25% to 50%, and so on), so that a directory page covers many more data pages.
- **Append only.** A heap file that never reuses space puts every insert in the last page: one read and one write, and the scan reads the records in insert order. Deleted space comes back only when the file is rewritten. A [log-structured merge tree](/log-structured-merge-tree/) builds on files of this kind.
- **Clustered and sorted files.** A file kept in the order of a key is a sorted file or a [clustered index](/clustered-index/). It answers range queries on that key with a short scan, and pays for it on insert.
- **Zone maps.** A heap file in insert order often has values that are nearly sorted, such as dates. A [zone map](/zone-map/) with the minimum and maximum of each page or block lets a scan skip pages without an index.

## When to use it

Use a heap file as the base storage of a table when most access is by full scan or through secondary indexes that store record ids, and when inserts are frequent. It is the default table organization of most relational systems. Use the page directory when records vary in size, since a list walk can read many pages that are almost full. Use an append only heap for logs and other data that is written once. Use a sorted file or a clustered index when range queries on one key dominate.

## Pitfalls

- **Slot reuse under an index.** When a slot is reused, an old index entry with that record id points to a different record. Delete the index entries of a record before its slot can be reused.
- **A stale directory.** The directory entry must change with the page. If the system crashes between the two writes, the entry can be wrong; recovery must log both changes, or treat the free space values as hints and check the page before it uses it.
- **Long free lists.** A free list with many pages that each have a few free bytes makes inserts slow. Raise the limit $m$, or use a directory.
- **Directory contention.** Every insert reads and writes the directory, and every insert to the same page latches it. Concurrent inserts can spread over several insert points, or choose pages at random among those with room.
- **Search by value.** A heap file has no order. A search on a value scans the whole file unless an index exists. A query plan that forgets this costs $N$ reads per lookup.

## Implementations

## History

The heap file, also called the entry-sequenced file, is the simplest file organization of relational systems, and Gray and Reuter (1993) treat it together with the free space administration of the tuple-oriented file system. Ramakrishnan and Gehrke give the two implementations of a heap file, with a page directory and with two linked lists, and the cost comparison of heap, sorted and hashed files that most database courses use. Oracle calls the default table a heap-organized table, in contrast with its index-organized table, and PostgreSQL names its table files heap files and keeps their free space in a free space map.

## References
