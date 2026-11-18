---
tag: MZEXV9
kind: problem
slug: media-recovery
name: Media recovery
aliases:
- archive recovery
- recovery from disk failure
area: databases/logging-and-recovery
level: core
summary: Restore a database after the loss of stable storage from an archive copy and the log written since that copy was taken.
prereqs: [crash-recovery, write-ahead-logging]
see_also: [point-in-time-recovery, aries-recovery, instant-restart, differential-file, fuzzy-checkpoint, checkpointing, log-sequence-number, shadow-paging]
sources:
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 6, Centralized Recovery, Section 6.8 (media failures, the archive database and the archive log, and fuzzy copies of the archive)
  - paper: doi:10.1145/289.291
    title: Theo Haerder and Andreas Reuter, Principles of transaction-oriented database recovery, ACM Computing Surveys 15(4), 1983, pages 287 to 317
    locator: the failure types, with media failure, and the archive copy and the archive log, paper level
  - paper: doi:10.1145/128765.128770
    title: C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh and Peter Schwarz, ARIES, a transaction recovery method supporting fine-granularity locking and partial rollbacks using write-ahead logging, ACM Transactions on Database Systems 17(1), 1992, pages 94 to 162
    locator: the section on media recovery (fuzzy image copies and redo from the log), paper level
  - book: isbn:9781558601901
    title: Jim Gray and Andreas Reuter, Transaction Processing, Concepts and Techniques, Morgan Kaufmann, 1993
    locator: the treatment of archive copies and recovery from media failure, book level only
  - book: isbn:9781627058728
    title: Goetz Graefe, Wey Guy and Caetano Sauer, Instant Recovery with Write-Ahead Logging, second edition, Morgan and Claypool, 2016
    locator: the chapter Instant Restore after a Media Failure, chapter level only
---

The media recovery problem, also called archive recovery or recovery from disk failure, asks how a database system can rebuild its data after the device that holds it is lost, so that the rebuilt data holds the effects of exactly the committed transactions. A [crash](/crash-recovery/) loses only main memory and keeps the disk; a media failure loses the disk too. The standard solution keeps an *archive copy* of the database on another device, taken from time to time, and keeps the log since that copy on a device that does not fail at the same time. Recovery restores the copy and redoes the archive log over it, then undoes the transactions that did not commit.

## In plain words

You keep a ledger on a desk, and every change also goes into a journal that you keep in another room. Once a week you photocopy the whole ledger and put the copy in a safe.

One night the desk burns, and the ledger with it. The journal and the copy are safe. You take the copy out of the safe and replay, in order, every change in the journal written after the day of the copy. Then you cross out the changes of any deal that was not closed. The ledger is now as it was before the fire, with every closed deal in it.

If the copy is a week old, you replay a week of journal. More frequent copies make the replay shorter but cost more work while the shop is open.

## Definition

**Storage model.** The database is a set of pages, each with a pageLSN, as in the model of the [crash recovery problem](/crash-recovery/) and of [write-ahead logging](/write-ahead-logging/). There are three kinds of storage:

- the *online database* on a disk, which a media failure destroys;
- the *log*, with every update record, kept on a device that fails independently of the online database; the part of the log that is kept for media recovery is the *archive log*;
- the *archive*, which holds one or more *archive copies* of the database (a dump, a backup), each with a *start LSN* $s$: every page in the copy holds the effects of all records on that page with an LSN below $s$.

**Copies.** A *consistent copy* is taken while no transaction updates the database and after the buffer is written out, so it holds the effects of exactly the transactions that committed before $s$. A *fuzzy copy* is taken while transactions run, from the disk, one page at a time. Each page in it holds the effects of all records on that page up to its pageLSN, which can be after $s$. Pages that are dirty in the buffer when the copy begins can miss older records, so $s$ is the smallest recLSN of those pages, as for a [fuzzy checkpoint](/fuzzy-checkpoint/), or the end of the log if no page is dirty.

**Failure.** A media failure destroys the online database, and also main memory if it comes with a crash. The log and the archive survive.

**The problem.** Let $C$ be the set of transactions whose commit record is in the stable log at the failure. Given an archive copy with start LSN $s$ and the log from $s$ to its end, build an online database in which every item has the value of its last write by a member of $C$, or its initial value. As for crash recovery, the procedure must be restartable after a crash during its own run.

## Variants

- **Whole device and part of a device.** The loss of a whole disk needs all pages of it. A single bad page needs only that page, from its last copy and its own log records; this is single-page repair.
- **Consistent and fuzzy copies.** A consistent copy needs a quiet database while it is taken. A fuzzy copy does not, but needs the redo from $s$ to bring every page to a common point and undo of the losers.
- **Full, incremental and differential copies.** An incremental copy holds only the pages changed since the previous copy. A [differential file](/differential-file/) keeps the main data read-only, so its copy stays valid until the next reorganization.
- **Loss of the log.** If the log is lost too, the committed transactions after the newest copy are lost. The log is kept on a separate device, often written twice.
- **Recovery to an earlier point.** [Point-in-time recovery](/point-in-time-recovery/) solves the same problem with the log cut at an earlier LSN, to remove the effect of a user error.
- **Restore on demand.** Instant restore, in the book of Graefe, Guy and Sauer, opens the database before the restore ends and restores each part of the device when a transaction first needs it, as [instant restart](/instant-restart/) does for a crash.

## Examples

Two pages: P1 holds $x$ and P2 holds $y$. The log, with a fuzzy copy taken during it:

| LSN | record | note |
|---|---|---|
| 1 | update T1, P1, $x$: 1 to 2 | |
| 2 | commit T1 | P1 is written to disk: $x = 2$, pageLSN 1 |
| 3 | begin copy | no page is dirty, so the start LSN is $s = 3$ |
| | | the copy reads P2: $y = 5$, pageLSN 0 |
| 4 | update T2, P2, $y$: 5 to 6 | |
| 5 | commit T2 | |
| 6 | update T3, P1, $x$: 2 to 3 | P1 is written to disk (a steal) |
| | | the copy reads P1: $x = 3$, pageLSN 6 |
| 7 | end copy | |
| 8 | update T4, P2, $y$: 6 to 7 | then the disk fails |

The copy holds $x = 3$ and $y = 5$. It is neither the state before nor the state after any transaction: P2 is older than the copy's end, and P1 holds an uncommitted change of T3.

Recovery restores the copy and redoes from LSN 3. Record 4 applies to P2 (pageLSN 0 < 4), so $y = 6$. Record 6 is skipped, because P1 already has pageLSN 6. Record 8 applies, so $y = 7$. The losers are T3 and T4, which have no commit record, and undo sets $x = 2$ and $y = 6$. The result holds the committed T1 and T2 only.

Redo from LSN 7, the end of the copy, would skip record 4 and give $y = 5$: the committed change of T2 would be lost. With a fuzzy copy, redo must start at the start LSN, not at the end. If P1 had still been dirty in the buffer at LSN 3, with $x = 2$ only in memory, the start LSN would be 1, the recLSN of P1.

## Known algorithms

- **Restore and redo.** Restore the newest archive copy, redo the log from its start LSN with the pageLSN test, then undo the losers with [compensation records](/compensation-log-record/), as in [ARIES](/aries-recovery/). This is the textbook method of Bernstein, Hadzilacos and Goodman and of Haerder and Reuter.
- **Fuzzy copies with LSNs.** ARIES takes image copies while transactions run, and the pageLSN of each copied page tells redo which records to skip. A copy is like a [fuzzy checkpoint](/fuzzy-checkpoint/) of the whole database.
- **Restore with a log archive sorted by page.** Instant restore keeps the archive log ordered by page, so the records of one part of the device are read together, and it restores parts on demand.
- **Mirrored or replicated storage.** Two copies on separate devices avoid the restore, but a mirror also copies a wrong write or a user error at once, so it does not replace the archive.

## Bounds

The costs are counted in log records read and in pages read and written.

- **Log records read.** All records from the start LSN $s$ of the copy to the end of the log. A [checkpoint](/checkpointing/) does not bound this number, since it bounds only the redo over the online database. The time between copies bounds it.
- **Pages read and written.** Every page of the lost device is read from the archive and written once to the new device. Redo reads and writes each page that the log after $s$ changed, once if the records of each page are applied together.
- **Log volume per update.** Each update record must stay in the archive log until the next copy is complete: its after image for redo, and its before image as long as its transaction may be a loser. A system can drop the before images of committed transactions from the archive log.
- **Copy cost.** A full copy reads every page. An incremental copy reads only the changed pages, but recovery then reads several copies.

A simple lower bound holds: with only the copy and the log, recovery must read every lost page from the copy, and for each page the last committed record on it after $s$. The general methods read all records after $s$.

## Reductions

- Media recovery reduces to [crash recovery](/crash-recovery/): restore the copy as the disk state, and run redo from the start LSN of the copy instead of the redo point of the last checkpoint. A consistent copy taken at $s$ is a disk state after a checkpoint at $s$ with an empty buffer.
- Point-in-time recovery reduces to media recovery with the log cut at the target LSN.
- Single-page repair reduces to media recovery of one page.

## Applications

Every database system that promises durability beyond the loss of a disk keeps archive copies and an archive log. PostgreSQL keeps base backups with an archive of its write-ahead log, and other systems have their own backup tools with the same plan. File systems and storage arrays use mirrors and snapshots, which protect against a failed device but not against a wrong write that the mirror copies.

## References
