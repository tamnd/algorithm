---
tag: XFJR29
kind: concept
slug: physiological-logging
name: Physiological logging
aliases:
- physical-to-a-page logical-within-a-page logging
area: databases/logging-and-recovery
level: core
summary: Log records that name a page physically but describe the change inside the page logically, which keeps records small and redo per page.
prereqs: [write-ahead-logging, log-sequence-number]
see_also: [logical-logging, aries-recovery, slotted-page, b-plus-tree, compensation-log-record, crash-recovery, buffer-pool]
sources:
  - book: isbn:9781558601901
    title: Jim Gray and Andreas Reuter, Transaction Processing, Concepts and Techniques, Morgan Kaufmann, 1993
    locator: Chapter 10, physical, logical and physiological logging, chapter level only
  - url: https://www.postgresql.org/docs/current/runtime-config-wal.html
    title: PostgreSQL documentation, Write Ahead Log settings
    locator: the parameter full_page_writes (torn pages, and why row-level change data cannot restore them)
  - url: https://dev.mysql.com/doc/refman/8.0/en/innodb-doublewrite-buffer.html
    title: MySQL 8.0 Reference Manual, Doublewrite Buffer
    locator: the first paragraph (a good copy of a page that was half written at a crash)
---

*Physiological logging* is a way to write the redo records of a [write-ahead log](/write-ahead-logging/): each record names one page physically, by its page id, and describes the change inside that page logically, as an operation such as "insert this row in slot 5". It is the middle point between *physical logging*, which records the bytes that changed at given offsets, and [logical logging](/logical-logging/), which records an operation on a table or an index and names no page at all. A physiological record is small like a logical one, and like a physical one it can be redone by reading one page only, with the [pageLSN](/log-sequence-number/) test; the price is that the record is not idempotent and needs a page that is internally consistent before it is applied.

## In plain words

A database keeps a diary of its changes so that it can repeat them after a crash. One way is to write down exactly which bytes changed and to what. That is safe but long. Another way is to write down only the action, such as "add this customer". That is short, but to repeat it the system may have to search many pages. Physiological logging does both halves: it says which page to open, and then says what to do inside that page. The system opens one page, checks a number stored on the page that says how far the page already got, and does the action only if the page did not get that far. This needs the page on disk to be complete, not half old and half new, so systems take extra care when they write pages.

## The idea

Take a change made by one operation. It can be logged in three ways.

| kind | the record holds | to redo it |
|---|---|---|
| physical | page id, offset, old bytes, new bytes, for each changed byte range | copy the new bytes in; the page can be in any state |
| physiological | page id, and an operation with its arguments that changes only that page | read the page, run the operation on it |
| logical | an operation on a table or an index, with its arguments | run the operation through the normal access paths, which find the pages |

Physical redo is idempotent: copying the same bytes twice gives the same page. Physiological redo is not, since inserting a row in a slot twice makes two rows. So the system stores in each page the LSN of the last record applied to it and redoes a record only if the page's LSN is smaller. With that test, each missing record is applied exactly once.

The test is sound only if every page on disk is a state that some prefix of its log records produced. A page that the disk wrote only in part, a *torn page*, is not such a state, and running an operation on it can give garbage. Physical records do not need this, since they overwrite the bytes they describe. Systems that use physiological records therefore protect page writes. PostgreSQL, with the setting `full_page_writes` (on by default), writes the whole page to the WAL at its first change after each checkpoint, and its documentation says that the row-level change data normally stored in the WAL is not enough to restore a torn page. InnoDB writes each page first to a doublewrite buffer and then to its place, so that recovery can find a good copy of a page that was half written.

A record that names one page also makes the order of redo simple. Two records on different pages do not depend on each other, so redo can apply records per page in LSN order, and even run pages in parallel. A logical record, by contrast, depends on the whole structure it goes through, so the database must be in a state where the structure is consistent before logical redo can start.

Undo can use a different kind of record than redo. After the row's page has changed for other reasons, for example because a [B+ tree](/b-plus-tree/) split moved the row, a physiological undo of the insert on the original page is wrong. Many systems therefore use physiological redo and logical undo: redo puts the pages back as they were, and undo then deletes the row wherever it now is, writing a [compensation log record](/compensation-log-record/) for the page that it really changed.

## Examples

**An insert in a slotted page.** Inserting a 100-byte row in a [slotted page](/slotted-page/) writes the row bytes, a new slot entry and the free-space pointer in the header. A physical record holds three byte ranges with old and new values. A physiological record holds the page id, "insert at slot 5" and the 100 row bytes. Redo of it reads the page and repeats the insert, which also sets the slot entry and the header.

**Compaction.** Deleting a row and then compacting an 8 KB page can move several kilobytes of rows to close the gap. Physical logging records every moved byte range, old and new, which can be as large as the page. A physiological record says "delete slot 3 of page 17" and lets redo compact again, because compaction is a function of the page alone.

**A B+ tree split.** A split of leaf $P$ into $P$ and a new page $P'$, with a separator key added to the parent $Q$, is logged as three physiological records: "format $P'$ with these keys", "remove the keys above $k$ from $P$" and "insert separator $k$ with pointer $P'$ in $Q$". Each record can be redone with its one page. A single logical record "insert key $x$ in index $I$" would make redo search the tree, and the tree might be half split on disk.

**A torn page.** A page of 8 KB is written to a disk with 4 KB atomic writes, and the power fails after the first half. The page now has the new header and slot array and the old rows. Its pageLSN, in the header, says it holds all changes, so redo skips every record for it, and the page stays wrong. A full page image in the log, or a good copy in a doublewrite area, is the fix.

## Where it is used

- Redo logs of relational systems that use a buffer of fixed-size pages. The PostgreSQL WAL holds row-level change records per page, together with the full page images above.
- [ARIES recovery](/aries-recovery/), whose redo pass reads each page and applies a record only after the pageLSN test, which is what physiological records need.
- Index structures such as the [B+ tree](/b-plus-tree/), where structure changes touch several pages and each page gets its own record.
- [Crash recovery](/crash-recovery/) designs that redo pages in parallel, since records for different pages are independent.

## References
