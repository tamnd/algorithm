---
tag: D6MZ35
kind: definition
slug: log-sequence-number
name: Log sequence number
aliases:
- LSN
- pageLSN
area: databases/logging-and-recovery
level: core
summary: A monotone address of a log record; each page stores the LSN of its last update so recovery knows which updates it already holds.
prereqs: [write-ahead-logging]
see_also: [aries-recovery, compensation-log-record, fuzzy-checkpoint, checkpointing, physiological-logging, logical-logging, lamport-clocks, replicated-log]
sources:
  - paper: doi:10.1145/128765.128770
    title: C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh and Peter Schwarz, ARIES, a transaction recovery method supporting fine-granularity locking and partial rollbacks using write-ahead logging, ACM Transactions on Database Systems 17(1), 1992, pages 94 to 162
    locator: Section 4.1, Log Records (LSN, PrevLSN, UndoNxtLSN), Section 4.2, Page Structure (page_LSN), Section 4.4, Dirty_Pages Table (RecLSN), Section 6.2, Redo Pass (the page_LSN test), and Section 10.4 (several LSNs in one page)
  - url: https://www.postgresql.org/docs/current/datatype-pg-lsn.html
    title: PostgreSQL documentation, pg_lsn type
    locator: the definition of pg_lsn as a pointer to a location in the WAL, a 64-bit byte position printed as two hexadecimal numbers
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill, 2003
    locator: Chapter 18, Crash Recovery (the log, LSNs, pageLSN and flushedLSN)
  - book: isbn:9781558601901
    title: Jim Gray and Andreas Reuter, Transaction Processing, Concepts and Techniques, Morgan Kaufmann, 1993
    locator: Chapter 9, Log Manager, chapter level only
---

A *log sequence number* (LSN) is a number that names a record of the [write-ahead log](/write-ahead-logging/) and grows with the record's position, so that comparing two LSNs tells which record was written first. Its main use is the *pageLSN*: each page carries the LSN of the last logged change applied to it, and recovery compares that number with the LSN of a record to decide whether the page already holds the change. For a reader who knows algorithms, an LSN is a version stamp drawn from one global counter, the end of the log; unlike a [Lamport clock](/lamport-clocks/) it needs no message exchange, because a single log orders all records. The [ARIES](/aries-recovery/) and [fuzzy checkpoint](/fuzzy-checkpoint/) pages use the LSN fields defined here; this page defines them and the tests built on them.

## Definition

**LSN.** Let the log be the sequence of records $r_1, r_2, \ldots$ in the order they were appended. An LSN assignment is a function $\text{lsn}$ with $\text{lsn}(r_i) < \text{lsn}(r_j)$ whenever $i < j$, and every LSN is positive. On this site $\text{lsn}(r_i) = i$, so the first record has LSN 1. Real systems often use the byte offset of the record in an ever-growing log address space: ARIES defines the LSN as the address of the first byte of the record, a monotonically increasing value, and PostgreSQL stores an LSN as a 64-bit byte position in the WAL stream, printed as two hexadecimal numbers such as `16/B374D848`. Gaps between LSNs carry no meaning; only the order does.

**Fields that hold LSNs.** The recovery literature names several:

| name | where | value |
|---|---|---|
| pageLSN | in each page | the LSN of the last update or CLR applied to the page; 0 if the page was never updated |
| flushedLSN | in memory, log manager | the largest LSN of a record on stable storage |
| prevLSN | in each log record | the LSN of the previous record of the same transaction; 0 for its first record |
| lastLSN | transaction table | the LSN of the newest record of the transaction |
| recLSN | dirty page table | the LSN of the first record that changed the page since it was last written |
| undoNextLSN | in each CLR | the prevLSN of the update that the CLR undid: the next record to undo |
| master record | fixed place on disk | the LSN of the last BEGIN_CHECKPOINT record whose end record is stable |

ARIES sets the recLSN, when a clean page is first changed, to the current end-of-log LSN, which is at most the LSN of the change; any value at most that LSN and larger than the last write of the page is correct.

**Page invariant.** If changes to a page are applied in LSN order and each one sets the pageLSN to its own LSN, then a page version with pageLSN $n$ holds exactly the effects of the logged changes on that page with LSN at most $n$. This invariant is what makes the three tests below sound.

**Tests.**

- *Redo test.* During redo, apply record $r$ to its page $P$ if and only if $\text{pageLSN}(P) < \text{lsn}(r)$, and then set $\text{pageLSN}(P) \leftarrow \text{lsn}(r)$. Because of the invariant, redo applies each missing change exactly once, even if the change is not idempotent.
- *WAL test.* The buffer manager may write page $P$ to disk only if $\text{pageLSN}(P) \le \text{flushedLSN}$; otherwise it first flushes the log up to $\text{pageLSN}(P)$.
- *Commit test.* A commit is reported only when $\text{flushedLSN} \ge$ the LSN of the commit record.

## Examples and non-examples

**A redo decision.** Pages $P$ (records $a = 10$, $b = 20$) and $Q$ ($c = 30$), both with pageLSN 0. The log:

| LSN | record | prevLSN |
|---|---|---|
| 1 | $T_1$ updates $P.a$: 10 to 11 | 0 |
| 2 | $T_2$ updates $Q.c$: 30 to 31 | 0 |
| 3 | $T_1$ updates $P.b$: 20 to 21 | 1 |
| 4 | commit $T_1$ | 3 |
| 5 | $T_2$ updates $P.a$: 11 to 12 | 2 |

The commit forces the log, so flushedLSN is 4. The buffer manager writes $P$ after LSN 3: its pageLSN is 3 and $3 \le 4$, so the WAL test passes. After LSN 5 the pageLSN of $P$ is 5, so the buffer manager may not write $P$ again until it flushes the log to 5. The system crashes; the stable log holds LSNs 1 to 4, and the disk holds $P$ with pageLSN 3 and $Q$ with pageLSN 0. Redo reads LSN 1: $3 \ge 1$, skip. LSN 2: $0 < 2$, apply, $c = 31$, pageLSN$(Q) = 2$. LSN 3: $3 \ge 3$, skip. The update of LSN 5 was never on disk and its record is lost, which is consistent: the page never held it. The prevLSN column chains $T_1$ as $3 \to 1 \to 0$ and $T_2$ as $5 \to 2 \to 0$.

**Byte offsets.** If three records of 40, 64 and 40 bytes start at byte 1000 of the log, their LSNs are 1000, 1040 and 1104. The tests above work the same way, since they only compare LSNs.

**Non-example: a wall-clock time.** A time stamp can go backwards when the clock is set, and two records can get the same value. Neither the redo test nor the WAL test is sound then.

**Non-example: a version counter per page.** A counter that each change of a page increments is monotone for that page, but it cannot be compared with flushedLSN, so it does not give the WAL test, and it cannot be compared with a record's position in the log without a lookup.

**Non-example: a transaction id.** Transaction ids order transactions by their start, not records by their position. Two records of one transaction share it.

**Several LSNs in one page.** ARIES Section 10.4 discusses pages whose parts carry LSNs of their own, as DB2 did for minipages, and ARIES keeps one LSN per page. With one LSN per page, the redo test is on the whole page, which is why records must be applied per page in LSN order.

## Related definitions

- [Write-ahead logging](/write-ahead-logging/) is the technique whose rules the WAL test and the commit test state.
- A [compensation log record](/compensation-log-record/) carries undoNextLSN, an LSN that skips records already undone.
- [Checkpointing](/checkpointing/) and the [fuzzy checkpoint](/fuzzy-checkpoint/) store recLSNs and lastLSNs, and the master record stores the LSN of a checkpoint.
- [ARIES recovery](/aries-recovery/) uses every field in the table.
- [Logical logging](/logical-logging/) and [physiological logging](/physiological-logging/) need the redo test, because their records are not idempotent.
- The index of an entry in a [replicated log](/replicated-log/) plays a similar part in distributed systems: it orders entries and lets a replica say how far it has applied the log.
- A [Lamport clock](/lamport-clocks/) also gives monotone numbers, across processes that exchange messages, and its numbers respect the happened-before order; an LSN is simply the position in one log.

## References
