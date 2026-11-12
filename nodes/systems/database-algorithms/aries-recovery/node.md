---
tag: YSPCY5
kind: algorithm
slug: aries-recovery
name: ARIES recovery
aliases:
- Algorithm for Recovery and Isolation Exploiting Semantics
- ARIES
- ARIES restart recovery
area: systems/database-algorithms
level: advanced
summary: "Write-ahead-log recovery in three passes: analysis rebuilds the transaction and dirty page tables, redo repeats history, undo rolls back losers and logs compensation records."
solves: [crash-recovery]
model: word-ram
complexity:
  vars: {n: the log records from the redo point to the end, u: the update records of the losers, m: the number of losers, d: the dirty pages}
  time: {worst: O(n + u log m)}
  space: {extra: O(m + d)}
properties: {deterministic: true}
history:
  year: 1992
  people: [C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh, Peter Schwarz]
  note: Published in ACM TODS in 1992 by a team at IBM.
prereqs: [write-ahead-logging, checkpointing, steal-and-force-policies]
see_also: [crash-recovery, shadow-paging, group-commit, strict-two-phase-locking, two-phase-commit, undo-log]
sources:
  - paper: doi:10.1145/128765.128770
    title: C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh and Peter Schwarz, ARIES, a transaction recovery method supporting fine-granularity locking and partial rollbacks using write-ahead logging, ACM Transactions on Database Systems 17(1), 1992, pages 94 to 162
    locator: the sections on the data structures (log records, page_LSN, transaction table, dirty_pages table), normal processing (rollback and CLRs, checkpoints) and restart processing (analysis, redo and undo passes)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill, 2003
    locator: Chapter 18, Crash Recovery (introduction to ARIES, the log, checkpointing, and the analysis, redo and undo phases)
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: Chapter 13, Page-Model Crash Recovery Algorithms (the redo-history algorithm family to which ARIES belongs), chapter level only
  - book: isbn:9781558601901
    title: Jim Gray and Andreas Reuter, Transaction Processing, Concepts and Techniques, Morgan Kaufmann, 1993
    locator: Chapters 10 and 11 (transaction manager concepts and structure, restart), chapter level only
---

ARIES is the recovery method of Mohan, Haderle, Lindsay, Pirahesh and Schwarz (1992) that solves the [crash recovery problem](/crash-recovery/) for a buffer manager with the steal and no-force policies and with record-level locking. It is [write-ahead logging](/write-ahead-logging/) plus three ideas: each page carries the LSN of its last change, so redo is exact; restart *repeats history*, redoing every logged change, of winners and losers alike, before it undoes anything; and every undo step is logged as a *compensation log record* (CLR) that points past the change it undid, so that an undo is never undone and repeated crashes during recovery add a bounded amount of log. Restart reads the log three times: analysis, redo and undo.

## In plain words

The database keeps a journal of every change, and each page remembers the number of the last journal entry it holds. Now and then it writes a checkpoint: a list of the running transactions and of the pages in memory that differ from the disk. No page is written for the checkpoint.

After a crash, the first pass starts at the last checkpoint and reads forward, to learn which transactions were still running and which pages might be out of date. The second pass replays every change from the oldest out-of-date page onwards, but only on a page that does not already hold it. Now memory looks as it did at the crash. The third pass walks the unfinished transactions backwards and takes back their changes. For each change it takes back, it writes a note "undone, continue from there", so a later crash never undoes a change twice.

## The problem

The model is the one of the [crash recovery problem](/crash-recovery/), refined as follows. Pages hold several records, and locks are on records, so two running transactions can change the same page; the history is strict at the level of records. The buffer pool may write any page at any time (steal) and does not write pages at commit (no-force), but it obeys the WAL rule: before it writes a page it flushes the log up to the page's pageLSN. A commit forces the log up to the commit record.

Normal processing keeps two tables in memory:

- the *transaction table* (ATT): for each active transaction its status, its *lastLSN* (its newest log record) and its *undoNext* (the next record to undo);
- the *dirty page table* (DPT): for each page in the buffer that differs from the disk, its *recLSN*, the LSN of the first record that made it dirty since it was last written.

Each log record of a transaction holds *prevLSN*, the LSN of its previous record. An update record holds the page, the record key and the before and after images. A CLR holds the page, the key, the value it writes, and *undoNextLSN*, the prevLSN of the update it undid. A transaction ends with an end record, after a commit or after its rollback. A *fuzzy checkpoint* writes a begin_checkpoint record, then an end_checkpoint record with copies of the ATT and the DPT, forces the log, and then writes the LSN of the begin record to a *master record* at a known place on disk. No data page is written by a checkpoint.

The output is the state of the [crash recovery problem](/crash-recovery/): every record holds the last surviving write of a committed transaction (a write that a partial rollback removed does not count). The method must stay correct when it crashes during its own run.

## The algorithm

```pseudo id=main
RESTART()
L1  start ← the LSN in the master record (or the first LSN of the log)        ▷ analysis
L2  for each log record r with r.lsn ≥ start, in LSN order do
L3      if r is an update or a CLR then ATT[r.T].lastLSN ← r.lsn; ATT[r.T].undoNext ← r.lsn for an update, r.undoNextLSN for a CLR
L4          if r.page ∉ DPT then DPT[r.page] ← r.lsn                              ▷ its recLSN
L5      else if r is commit then mark r.T committed; else if r is end then remove r.T from the ATT
L6      else if r is end_checkpoint then replace the ATT and the DPT by the copies in r
L7  for each committed T in the ATT do write ⟨end, T⟩ and remove T
L8  redoLSN ← the smallest recLSN in the DPT                                      ▷ redo
L9  for each update or CLR r with r.lsn ≥ redoLSN, in LSN order do
L10     if r.page ∈ DPT and r.lsn ≥ DPT[r.page].recLSN then
L11         if pageLSN(r.page) < r.lsn then                                       ▷ fetch the page
L12             apply r to the page; pageLSN(r.page) ← r.lsn
L13 while the ATT is not empty do                                                 ▷ undo
L14     T ← the transaction in the ATT with the largest undoNext
L15     UNDO-STEP(T)
L16 force the log
L17 take a checkpoint

UNDO-STEP(T)                                                                     ▷ also used by rollback in normal work
L18 r ← the record ATT[T].undoNext; if r is an update then
L19     c ← APPEND(⟨CLR, T, prevLSN = ATT[T].lastLSN, r.page, r.key, value = r.before, undoNextLSN = r.prevLSN⟩)
L20     write r.before into the page; pageLSN ← c.lsn; ATT[T].lastLSN ← c.lsn; ATT[T].undoNext ← r.prevLSN
L21 else if r is a CLR then ATT[T].undoNext ← r.undoNextLSN       ▷ else (an abort record) undoNext ← r.prevLSN
L22 if ATT[T].undoNext = 0 then write ⟨end, T⟩ and remove T from the ATT
```

**Analysis (lines L1 to L7).** It starts at the begin_checkpoint record named by the master record, so it reads only the log since the last complete checkpoint. At the end_checkpoint record it takes the copied tables. In this version the tables are copied at the moment the end record is written, so they are exact there; a system that gathers the tables while transactions run merges them with what the scan has seen instead. An abort record leaves the transaction in the ATT: it becomes a loser whose rollback recovery must finish. Transactions that committed get their end record. The rest are the *losers*.

**Redo (lines L8 to L12).** Redo starts at the smallest recLSN, which can be older than the checkpoint, and applies each update and each CLR, of losers too, that the page does not already hold. Line L10 skips, without a page read, records on pages that were written to disk after the record. Line L11 is the pageLSN test, which makes redo exact even for operations that cannot be applied twice. After redo, the buffer pool holds the pages as they were at the crash, up to the end of the stable log. This is *repeating history*. Writes to disk during redo remove pages from the live DPT, so the decisions of line L10 use the DPT as analysis left it.

**Undo (lines L13 to L22).** All losers are rolled back in one backward sweep: line L14 always takes the largest LSN still to undo, so the log is read backwards once. UNDO-STEP undoes one update and writes a CLR whose undoNextLSN is the update's prevLSN. If the chain reaches a CLR (left by a rollback before the crash, or by an earlier, interrupted recovery), line L21 jumps to its undoNextLSN, past everything that CLR's rollback already undid. A CLR is redone in the redo pass but never undone. The same UNDO-STEP serves an abort in normal processing and a partial rollback to a savepoint (which stops at the savepoint's LSN and writes no end record).

## Example

Pages $P$ (keys $a = 10$, $b = 20$), $Q$ ($c = 30$, $d = 40$) and $R$ ($e = 50$), all with pageLSN 0. The run before the crash:

| LSN | record | prevLSN | note |
|---|---|---|---|
| 1 | update $T_1$, $P.a$: 10 to 11 | 0 | |
| 2 | update $T_2$, $P.b$: 20 to 21 | 0 | same page as LSN 1 |
| 3 | begin_checkpoint | | |
| 4 | end_checkpoint, ATT $= \{T_1: (1, 1), T_2: (2, 2)\}$, DPT $= \{P: 1\}$ | | master record $\leftarrow 3$ |
| 5 | update $T_1$, $Q.c$: 30 to 31 | 1 | |
| 6 | commit $T_2$ | 2 | log forced to 6 |
| 7 | end $T_2$ | 6 | still in the log tail |

The ATT entries show (lastLSN, undoNext). Then the buffer writes page $P$ (WAL: the log is already forced past LSN 2), so the disk holds $P = \{a = 11, b = 21\}$ with pageLSN 2, and $Q$ still holds $c = 30$. Then the system crashes, and record 7 is lost.

| pass | step | ATT | DPT | effect |
|---|---|---|---|---|
| analysis | read LSN 3, 4 | $T_1: (1, 1)$, $T_2: (2, 2)$ | $P: 1$ | tables from the checkpoint |
| analysis | read LSN 5 | $T_1: (5, 5)$, $T_2$ | $P: 1$, $Q: 5$ | |
| analysis | read LSN 6 | $T_1$, $T_2$ committed | same | |
| analysis | line L7 | $T_1: (5, 5)$ | same | LSN 7: end $T_2$ |
| redo | LSN 1, 2 | | | skipped: pageLSN$(P) = 2$ |
| redo | LSN 5 | | | $c = 31$, pageLSN$(Q) = 5$ |
| undo | undoNext 5 | $T_1: (8, 1)$ | | LSN 8: CLR $Q.c = 30$, undoNextLSN 1 |
| undo | undoNext 1 | $T_1: (9, 0)$ | | LSN 9: CLR $P.a = 10$, undoNextLSN 0 |
| undo | line L22 | empty | | LSN 10: end $T_1$ |

The final state is $a = 10$, $b = 21$, $c = 30$, $d = 40$, $e = 50$. Page $P$ held a change of the loser $T_1$ and a change of the winner $T_2$; ARIES undoes the first and keeps the second, which a page-level undo could not do. If the system crashes again after LSN 8 reaches the disk, the next analysis sets $T_1$'s undoNext to 1 from that CLR, and the next undo starts at LSN 1 and does not touch $Q.c$ again.

## Correctness

**Theorem.** Assume strict record-level locking, the WAL rule on every page write, a forced commit record, and a master record written only after its end_checkpoint is on disk. After a crash at any point, also during RESTART, any number of times, a RESTART that runs to the end leaves every record with the last surviving write of a transaction whose commit record is in the stable log. Moreover, the stable log never holds two CLRs for the same update.

The proof rests on three invariants. *Page invariant:* a page version with pageLSN $n$ holds exactly the effect of all update and CLR records on that page with LSN at most $n$, applied in LSN order. *Dirty page invariant:* if a page in the buffer holds a record that its disk version does not, the page is in the DPT with a recLSN at most that record's LSN. *Chain invariant:* following undoNext from a transaction's entry (an update leads to its prevLSN, a CLR to its undoNextLSN) visits exactly the updates of the transaction that no CLR has undone, newest first. From these: analysis rebuilds a DPT that covers every logged change missing from the disk, so redo brings each page to its state at the end of the stable log; undo then removes the uncompensated updates of each loser, newest first, and strictness makes each before image the right value to restore. A CLR in the stable log removes its update from every later chain, so no update is undone twice. The full proof is in the correctness proof below.

## Complexity

The cost is counted in log records and page operations, for one restart, in the worst case.

- **Analysis** reads the log from the begin_checkpoint to the end: at most $n$ records, $O(1)$ work each with hash tables.
- **Redo** reads from redoLSN to the end, also at most $n$ records if $n$ is counted from $\min(\text{redoLSN}, \text{start})$. It reads each page in the DPT at most once, $O(d)$ page reads, and line L10 avoids page reads for pages written after their records.
- **Undo** does one step for each update of a loser that is not yet undone, $u$ steps, plus one jump for each CLR met on a chain. With the undoNext values in a max-heap, line L14 costs $O(\log m)$, so undo takes $O(u \log m)$ time and writes at most $u$ CLRs and $m$ end records. The implementation below scans the ATT instead, $O(m)$ per step.
- **Space** is $O(m + d)$ for the two tables.

Over repeated crashes during recovery the log grows by at most one CLR for each update of a loser in total, plus the end records, because of the last claim of the theorem.

## Properties

- **Steal and no-force.** Both are allowed, so the buffer manager can write any page at any time and commit costs one log force.
- **Record-level locking.** Pages are shared between transactions, and the pageLSN with repeating history keeps a winner's change on a page that a loser also changed.
- **Restartable.** A crash in any pass is followed by a normal restart; work done by CLRs that reached the disk is not redone or undone again.
- **Partial rollback.** Savepoints use the same UNDO-STEP and CLRs.
- **Fuzzy checkpoints.** Checkpoints write no pages and do not stop transactions.
- **Logical undo.** Because undo runs after history is repeated, an undo can act on a different page than the original change (for example after a B-tree split), as long as it is logged as a CLR.

## Variants and improvements

- **Selective redo.** Earlier methods redo only winners. With record-level locking this is wrong: a page can hold a loser's change below the pageLSN of a winner's change, and the pageLSN no longer says which changes are on the page. ARIES chose repeating history for this reason.
- **Nested top actions.** A structure change, such as a page split, that must survive the rollback of its transaction is logged and then closed by a dummy CLR whose undoNextLSN points before it, so the undo pass jumps over it.
- **Index variants.** Later papers by Mohan and others adapt the method to B-tree indexes with key-level locking.
- **Parallel and on-demand restart.** Redo can run in parallel per page, and the system can accept new transactions before undo ends, with the losers' locks held, because analysis knows which records the losers locked.
- **Recovery work bounds.** Writing out old dirty pages in the background raises the smallest recLSN and so shortens redo; see [checkpointing](/checkpointing/).

## When to use it

Use ARIES, or a design close to it, when pages are updated in place, the buffer manager must be free to write any page, commits must cost only a sequential log write, and locking is finer than a page. That is the case of a general-purpose disk-based relational system. [Shadow paging](/shadow-paging/) avoids the log for page contents but scatters data and handles concurrent transactions poorly. A main-memory system that never writes uncommitted data needs only redo, and a plain redo log with periodic snapshots is simpler. [Write-ahead logging](/write-ahead-logging/) with page-level locking and physical images can use a simpler redo-then-undo recovery without CLRs, at the cost of logging the end of recovery carefully.

## Pitfalls

- **Undoing a CLR.** If line L21 treated a CLR like an update and undid it, a crash during recovery would make the next restart undo the undo. Follow the CLR's undoNextLSN instead.
- **Redo from the checkpoint.** Starting redo at the begin_checkpoint record in line L8 misses changes made before the checkpoint to pages that were still dirty at it. Start at the smallest recLSN of the DPT.
- **Redo only the winners.** Skipping losers' records in line L9 breaks the pageLSN reasoning when pages are shared. Repeat all of history, then undo.
- **The live DPT in line L10.** If the buffer writes a page during redo and the redo test reads the live table, the page has left the table and its later records are skipped. Decide with the table that analysis built, and add pages to the live table as redo dirties them.
- **The comparison in line L11.** The test is pageLSN $<$ LSN. With $\le$ a record already on the page is applied a second time.
- **The master record too early.** Writing the master record before the end_checkpoint record is on disk can make analysis start at a checkpoint that has no tables.

## Implementations

## History

Mohan, Haderle, Lindsay, Pirahesh and Schwarz described ARIES in ACM Transactions on Database Systems in 1992, from work at IBM. The paper reviews the recovery methods of earlier systems, among them the shadow pages and log of System R, and explains why their combinations of selective redo, page locking and undo without compensation records fail with finer locking. The three-pass structure, repeating history and CLRs with undoNextLSN became the standard textbook account of recovery; Ramakrishnan and Gehrke present it as the recovery method of their Chapter 18.

## References
