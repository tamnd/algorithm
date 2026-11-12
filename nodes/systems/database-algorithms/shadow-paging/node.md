---
tag: 951MHG
kind: technique
slug: shadow-paging
name: Shadow paging
aliases:
- shadow page technique
- shadow page table recovery
area: systems/database-algorithms
level: core
summary: "Recovery without an undo or redo log for page contents: a transaction writes changed pages to new places, and commits by an atomic switch of the root page table pointer."
prereqs: [crash-recovery]
see_also: [path-copying, steal-and-force-policies, write-ahead-logging, aries-recovery, checkpointing, log-structured-merge-tree]
sources:
  - paper: doi:10.1145/320521.320540
    title: Raymond A. Lorie, Physical integrity in a large segmented database, ACM Transactions on Database Systems 2(1), 1977, pages 91 to 104
    locator: the description of the shadow mechanism (current and backup page tables, page allocation maps, and the atomic switch at a save point)
  - paper: doi:10.1145/356842.356847
    title: Jim Gray, Paul McJones, Mike Blasgen, Bruce Lindsay, Raymond Lorie, Tom Price, Franco Putzolu and Irving Traiger, The recovery manager of the System R database manager, ACM Computing Surveys 13(2), 1981, pages 223 to 242
    locator: the sections on the shadow mechanism of System R and the evaluation of its costs (page table I/O, loss of clustering, checkpoint cost) against logging
  - paper: doi:10.1145/289.291
    title: Theo Haerder and Andreas Reuter, Principles of transaction-oriented database recovery, ACM Computing Surveys 15(4), 1983, pages 287 to 317
    locator: the classification of propagation strategies, where shadow pages give ATOMIC propagation
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 6, the section on shadowing (the no-undo/no-redo algorithm with shadow copies and a directory switch), chapter level only
---

*Shadow paging* solves the [crash recovery problem](/crash-recovery/) by never writing over the committed version of a page. The database is a set of pages reached through a *page table*, and one fixed disk block, the *root*, names the current page table. A transaction writes each page that it changes to a free place on the disk and changes its own copy of the page table. The old pages and the old table stay on the disk as the *shadow*. To commit, the transaction writes its new table and then writes the root to point at it. A one-block write is atomic, so after a crash the root names either the old table or the new one, and the disk shows either none or all of the transaction. Recovery needs no undo or redo log for page contents. The cost is that pages move on every update, the old copies become garbage, and running several transactions at once is hard. The method is from Lorie (1977), and System R used it.

## In plain words

Think of a book with a table of contents. To change some pages, you do not erase them. You write new versions of those pages on blank sheets, and you make a new table of contents that points to the new sheets and to the old sheets that did not change.

Until you finish, the old table of contents is still the official one, and it points only to old sheets. To finish, you change one note on the front cover: "the official table of contents is now the new one". That one change is the moment of commit.

If the power fails before the note changes, the old book is complete. If it fails after, the new book is complete. Sheets that no table points to are thrown away.

## When it applies

- The storage writes one block atomically, so the root can be switched in one write.
- One transaction at a time changes the database, or changes are grouped into whole-database versions (a save point), so one root switch commits all changes that are ready.
- Pages can be stored anywhere, because the page table translates logical page numbers into disk places.
- The data is read more than it is updated, or its layout on disk does not matter much (for example on flash, or with large pages).

## The template

```pseudo id=main
BEGIN()
L1  T.table ← a copy of the page table named by the root; T.new ← ∅
WRITE(T, p, v)
L2  s ← a free slot: not the root's table, not in the root's table, not in T.new
L3  write v into slot s                                  ▷ the shadow slot T.table[p] is not touched
L4  if T.table[p] ∈ T.new then free T.table[p]           ▷ a second write of p in T
L5  T.table[p] ← s; add s to T.new
COMMIT(T)
L6  t ← a free slot; write T.table into slot t
L7  wait until every write of lines L3 and L6 is on the disk
L8  write t into the root                                ▷ one atomic block write: the commit point
L9  free the old table slot and the old slots of the pages that T changed
ABORT(T)
L10 free every slot in T.new; drop T.table
RESTART()
L11 free ← all slots, less the root's table slot and the slots in the root's table
```

**Why it is atomic.** No line before L8 writes a slot that the root's table uses: line L2 picks only free slots. So until line L8, everything reachable from the root is the state before $T$. Line L8 is one atomic write, and after it everything reachable from the root is the state after $T$, because line L7 made all the new slots durable first. A crash leaves one of the two states, and restart (line L11) only rebuilds the free list.

**What is not needed.** There is no undo, because uncommitted changes are never reachable from the root; and no redo, because the commit point is after all the changed pages are on disk. In the terms of [steal and force](/steal-and-force-policies/), shadow paging is the force policy with ATOMIC propagation, which is the one way to need neither undo nor redo.

**Large page tables.** A page table for a large database does not fit in one block. It is then itself a tree of table pages, and a commit copies only the table pages on the paths from the root to the changed leaves, as in [path copying](/path-copying/) of persistent trees. A copy-on-write B-tree takes this one step further and lets the index itself be the page table.

## Classic examples

**A hand example.** Six pages in slots 1 to 6 hold 0, and slot 0 holds the page table $(1, 2, 3, 4, 5, 6)$; the root is 0. A transaction writes page 2 with 7, then page 2 again with 8, then page 4 with 9.

| step | disk write | T.table | free (lowest) | root |
|---|---|---|---|---|
| write p2 = 7 | slot 7 $\leftarrow$ 7 | $(1, 2, 7, 4, 5, 6)$ | 8, 9, ... | 0 |
| write p2 = 8 | slot 8 $\leftarrow$ 8, slot 7 freed | $(1, 2, 8, 4, 5, 6)$ | 7, 9, ... | 0 |
| write p4 = 9 | slot 7 $\leftarrow$ 9 | $(1, 2, 8, 4, 7, 6)$ | 9, ... | 0 |
| commit, table | slot 9 $\leftarrow (1, 2, 8, 4, 7, 6)$ | | 10, ... | 0 |
| commit, root | root $\leftarrow$ 9 | | 0, 3, 5, 10, ... | 9 |

A crash at any row before the last leaves the root at 0, and the database is all zeros. After the last row, pages 2 and 4 hold 8 and 9. Slots 0, 3 and 5 are now garbage and become free.

**System R.** System R used shadows for its files (segments) together with a log. The shadow mechanism gave a consistent state of the files at each checkpoint, so recovery could start from a state where no action was half done, and the log was used to undo and redo transactions from there. Gray and others (1981) report that the page table writes and lost clustering of shadow pages were a large cost, and they judge that a log with update in place would have done the same work more cheaply.

**Copy-on-write storage.** LMDB keeps a B+tree whose pages are never overwritten. A write transaction copies the pages on the path to each change, and commit writes one of two meta pages, which act as the root. File systems such as WAFL, ZFS and btrfs use the same idea for whole file system trees, and keep old roots as snapshots.

## Variations

- **Save points of the whole database.** Lorie's design switches the root at a save point for all changes made so far, rather than per transaction. The system then needs a log to undo or redo individual transactions between save points.
- **Two roots.** Some systems keep two root blocks with a version number and a checksum, and write them in turn. Restart takes the valid root with the higher version. This avoids depending on the atomicity of one sector write.
- **Copy-on-write B-trees.** The index is the page table. Each update copies a path, and old roots can be kept as read-only versions, which gives snapshots and multiversion reads for free.
- **Log-structured storage.** A [log-structured merge tree](/log-structured-merge-tree/) also never overwrites data in place, but it batches changes into new sorted files and merges them later. Its durability comes from a [write-ahead log](/write-ahead-logging/), not from a root switch at each commit.
- **Shadow paging in memory.** [Path copying](/path-copying/) in persistent data structures is the same copy-on-write idea for in-memory trees, with no crash and no disk.

## Pitfalls

- **Writing over a shadow page.** If line L3 writes into the slot the root's table uses, a crash before line L8 leaves part of the transaction on the disk, with no log to undo it. The test of the implementation shows such a crash.
- **Switching the root too early.** Line L8 must wait for line L7. If the root is written while new pages are still in a write cache, a crash can leave a root that points to pages that were never written.
- **Scattered data.** Pages move to wherever a free slot is, so pages that were next to each other on disk are no longer, and range scans become random reads. This was a main cost reported for System R.
- **Garbage.** Every update leaves an old slot behind, and an abort leaves new slots behind. The free list must be rebuilt from the root at restart (line L11), or slots leak.
- **Concurrency.** Two transactions that change different records on the same page each make a private copy of the page, and one root switch cannot commit one copy without the other. Shadow paging therefore needs page-level locks, one writer at a time, or a log for record-level changes, which removes its main advantage.
- **The page table cost.** Each commit writes table pages as well as data pages, at least one per changed path, and the table must be read to find any page.

## Exercises

1. In the hand example, the system crashes after the row "commit, table". Which slots does restart mark as free?
2. Two transactions run at the same time and change different pages. Describe a way to commit both with one root switch, and say what happens if one of them aborts.
3. A page table has 1024 entries per block and the database has $2^{30}$ pages. How many blocks does one commit write if a transaction changes one page? If it changes 1000 random pages?
4. Show that shadow paging with save points of the whole database and no log cannot provide record-level locking. Give a schedule.
5. Compare the I/O of one commit with shadow paging and with [write-ahead logging](/write-ahead-logging/) under no-force, for a transaction that changes 10 records on 10 pages.

## References
