---
tag: 9VV51Q
kind: technique
slug: point-in-time-recovery
name: Point-in-time recovery
aliases:
- PITR
- log replay to a timestamp
area: databases/logging-and-recovery
level: core
summary: Restore a backup and replay the archived log up to a chosen time, which undoes the effect of a later user error.
prereqs: [media-recovery, write-ahead-logging]
see_also: [crash-recovery, aries-recovery, fuzzy-checkpoint, log-sequence-number, compensation-log-record, differential-file, checkpointing, savepoint]
sources:
  - url: https://www.postgresql.org/docs/current/continuous-archiving.html
    title: PostgreSQL documentation, Continuous Archiving and Point-in-Time Recovery (PITR)
    locator: Section 25.3.5, Recovering Using a Continuous Archive Backup (the recovery target, and the note that the stop point must be after the end of the base backup), and Section 25.3.6, Timelines
  - url: https://www.postgresql.org/docs/current/runtime-config-wal.html
    title: PostgreSQL documentation, Write Ahead Log settings
    locator: Section 19.5.6, Recovery Target (recovery_target_time, recovery_target_xid, recovery_target_lsn and recovery_target_inclusive)
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 6, Centralized Recovery, Section 6.8 (the archive database and the archive log)
  - paper: doi:10.1145/128765.128770
    title: C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh and Peter Schwarz, ARIES, a transaction recovery method supporting fine-granularity locking and partial rollbacks using write-ahead logging, ACM Transactions on Database Systems 17(1), 1992, pages 94 to 162
    locator: the section on media recovery (fuzzy image copies and redo from the log), paper level
---

Point-in-time recovery (PITR), or log replay to a timestamp, rebuilds a database as it was at a chosen moment in the past. It restores an archive copy taken before that moment, replays the archived log from the copy up to the target, and rolls back the transactions that had not committed at the target. Committed work after the target is not undone: it is simply never replayed. It uses the same parts as [media recovery](/media-recovery/), with the log cut at an earlier point, and its main use is to remove the effect of a user error, such as a wrong DELETE, that the database has already committed and that every replica has already copied.

## In plain words

Someone deleted a table at 14:05, and the database committed it, as it should. A crash recovery does not help, because the delete is committed work.

So you take the last full copy of the database from before 14:05, for example the one from the night before. You replay the journal of changes over it, in order, and you stop just before 14:05. Work that was half done at that moment is cancelled, as after a crash. Work after 14:05 is never replayed.

The result is the database as it was at 14:04. Everything after that is gone, the good changes with the bad one. You can then copy the lost table back into the live database, or use the restored copy as the new database.

## When it applies

- The system keeps archive copies and keeps every log record since the oldest copy that it may need, as for [media recovery](/media-recovery/).
- Each commit record holds a time, or the operator knows a log position (an LSN), a transaction or a named restore point to stop at.
- The target is after the end of some archive copy. A copy taken while transactions run (a fuzzy copy) is consistent only together with the log up to its end, so it cannot give a state from before its end.
- The loss of all committed work after the target is acceptable, or the result is used only to copy data back.

## The template

The log is the one of [write-ahead logging](/write-ahead-logging/): update records with before and after images, compensation records (CLRs) for undo, and pages with a pageLSN. A commit record holds its time. An archive copy has a *start LSN*, the smallest recLSN of the pages that were dirty in the buffer when the copy began, and an *end LSN*, the LSN of the record that ends the copy.

```pseudo id=main
RECOVER-TO(t)
L1  stop ← the LSN just before the first commit record with a time after t, or the end of the log
L2  restore, on a new device, the newest archive copy whose end LSN is at most stop
L3  cut the log at stop: the records after stop are not used
L4  for each update or CLR r from the start LSN of the copy up to stop, in LSN order do
L5      if pageLSN(r.page) < r.lsn then apply r.after to the page; pageLSN(r.page) ← r.lsn
L6  losers ← the transactions in the log up to stop with no commit record and no end record
L7  for each loser, undo its updates newest first with CLRs, written to the new branch of the log
L8  append ⟨end, T⟩ for each loser; open the database on the new branch
```

**What happens to transactions open at the target.** A transaction that began before the target and committed after it has no commit record in the log up to stop. Line L6 makes it a loser, and line L7 rolls back the part of it that is before the target, even though it committed later. A transaction that began after the target has no records up to stop and does not appear. So the result holds exactly the transactions with a commit record at or before the target, as if the system had crashed at that moment.

**The new branch.** After line L8 the database writes new records after the CLRs and end records of line L7. These records must not mix with the old records after stop, which are still in the archive and describe a different history. PostgreSQL gives each such branch a new *timeline* ID and keeps a history file that says where it branched off.

**Why it works.** The log up to stop is a prefix of the log, and a crash at stop would have left exactly this prefix as the stable log, with some disk state. Lines L2 to L5 build, from the copy, the state that holds every record on each page up to stop, by the pageLSN argument of [crash recovery](/crash-recovery/) and [ARIES](/aries-recovery/): each page in the copy holds all records on it below the start LSN and up to its own pageLSN, and lines L4 and L5 add the rest. The copy ended at or before stop, so no page in it holds a record after stop. Lines L6 to L8 are then the undo of a crash recovery at stop. The tests check this by a media failure after every prefix of a random workload, and recovery to every target time.

**Cost.** Line L2 reads every page of the copy and writes it to the new device. Lines L4 and L5 read the log records from the start LSN of the copy to stop, and write each page that they change once at the end. Line L7 reads the records of the losers and writes one CLR per loser update. The log volume per update in normal work is that of write-ahead logging, but every record must be kept in the archive for as long as a target before it may be asked for. A [checkpoint](/checkpointing/) does not shorten the replay: the time since the newest copy that ended before the target bounds it, so more frequent copies make it shorter.

**Example.** Items a = 10 and c = 30, a copy that ends before T1 starts, and commit times 1, 2 and 3.

| LSN | record |
|---|---|
| 1, 2 | begin copy, end copy |
| 3, 4 | begin T1, update T1 a: 10 to 11 |
| 5, 6 | commit T1 (time 1), end T1 |
| 7, 8 | begin T2, update T2 c: 30 to 31 |
| 9, 10 | commit T2 (time 2), end T2 |
| 11, 12 | begin T3, update T3 a: 11 to 99 (the user error) |
| 13, 14 | commit T3 (time 3), end T3 |

RECOVER-TO(2) finds the first commit after time 2 at LSN 13, so stop = 12. It restores the copy and replays records 4, 8 and 12. T3 has no commit record up to 12, so it is a loser, and a CLR sets a back to 11. The result is a = 11, c = 31: T1 and T2 are in, the error is out. RECOVER-TO(1) stops at 8, rolls back the open T2 with a CLR, and gives a = 11, c = 30.

## Classic examples

- **PostgreSQL.** A base backup and an archive of the write-ahead log. The recovery target is a time, a transaction ID, an LSN or a named restore point. The setting recovery_target_inclusive says whether a transaction that commits exactly at the target is included. Each completed archive recovery starts a new timeline.
- **Database systems with log backups.** Systems with full backups and log backups restore a full backup, then the log backups in order, and stop at a time or at a marked transaction.
- **ARIES image copies.** The fuzzy image copies of ARIES and redo from the log give the media recovery on which point-in-time recovery builds.
- **Recovery of a [differential file](/differential-file/).** The read-only main file and a dump of the differential file give a point to restore to; the logged changes since then are redone up to the target.

## Variations

- **Target by transaction.** Stop just after the commit of a named transaction. Transaction IDs are given at the start of a transaction, but transactions commit in another order, so the target is a position in the commit order, not an ID range.
- **Inclusive or exclusive target.** Include or exclude a transaction whose commit time is exactly the target.
- **Named restore points.** The system writes a record with a name into the log, for example before a risky change, so that the operator can later stop exactly there.
- **Delayed replica.** A replica that applies the log a fixed time late keeps a state from the past at all times, so that recovery from a user error needs no restore.
- **Table-level recovery.** Recover the whole database to a side copy, then copy only the lost rows or tables back into the live database. The live database keeps its later work.
- **Flashback by undo.** A system that keeps old versions of rows can read or rebuild a past state without a restore, as long as the old versions are still kept. This replaces replay by undo and is limited by how long the old versions stay.

## Pitfalls

- **A copy that ended after the target.** A fuzzy copy can hold committed changes after the target, and recovery never undoes committed work. Use only a copy whose end is at or before the target. The tests check that such a copy is refused.
- **Redo from the end of the copy, or from the begin record only.** Redo must start at the start LSN, the smallest recLSN of the pages dirty in the buffer when the copy began. A later start loses committed changes that were only in the buffer.
- **Forgetting the open transactions.** Stopping replay at the target without the undo of lines L6 to L8 leaves changes of transactions that had not committed at the target, some of which may never have committed at all.
- **Mixing timelines.** After a recovery to the past, the old log after the target is still in the archive. A later recovery must not replay it on top of the new branch.
- **A gap in the archive.** If one log segment between the copy and the target is missing, replay must stop at the gap. The result is then older than the target.
- **Clock targets.** A target time is compared with commit times in the log, which come from the clock of the server. A user who gives the time from another clock can stop on the wrong side of the error.

## Exercises

1. In the example, a fuzzy copy reads page a after LSN 12 and ends at LSN 15. Show that RECOVER-TO(2) with this copy gives a = 99, and that no undo with the log alone can repair it.
2. Change line L1 to stop at the first commit after t instead of just before it. Which transaction is then wrong, and how?
3. A transaction T starts at time 1, writes x, and commits at time 5. Give the value of x after RECOVER-TO(t) for t = 0, 3 and 5, and the log records that line L7 writes in each case.
4. Show that recovery to a target and then a second recovery of the new branch to a later target never replays a record of the old branch after the first target.

## References
