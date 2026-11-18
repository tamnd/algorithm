---
tag: 80XPYE
kind: technique
slug: write-behind-logging
name: Write-behind logging
aliases:
- WBL
area: databases/logging-and-recovery
level: research
summary: A protocol for non-volatile memory that writes data first and logs only commit timestamp ranges, so recovery needs no redo.
prereqs: [write-ahead-logging, multiversion-concurrency-control, group-commit]
see_also: [steal-and-force-policies, crash-recovery, aries-recovery, shadow-paging, command-logging, instant-restart, checkpointing, snapshot-isolation]
sources:
  - paper: doi:10.14778/3025111.3025116
    title: Joy Arulraj, Matthew Perron and Andrew Pavlo, Write-behind logging, Proceedings of the VLDB Endowment 10(4), 2016, pages 337 to 348
    locator: Section 4 (the write-behind logging protocol, the dirty tuple table, the commit timestamp gaps and recovery), Section 6 (the NVM platform) and Section 7 (the evaluation in Peloton against write-ahead logging)
  - paper: doi:10.1145/128765.128770
    title: C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh and Peter Schwarz, ARIES, a transaction recovery method supporting fine-granularity locking and partial rollbacks using write-ahead logging, ACM Transactions on Database Systems 17(1), 1992, pages 94 to 162
    locator: the redo and undo passes of write-ahead logging, the baseline that write-behind logging replaces, paper level
---

Write-behind logging (WBL) is a logging protocol for a database system that keeps its data in byte-addressable non-volatile memory (NVM). It turns the order of [write-ahead logging](/write-ahead-logging/) around: a transaction's changes reach durable storage *before* its log record, and the log record holds no data, only a range of commit timestamps. With [multiversion concurrency control](/multiversion-concurrency-control/), every version of a tuple carries the timestamp of the transaction that wrote it. After a crash, the versions whose timestamps fall in the range that was open at the crash are simply not visible. Recovery has no redo and no undo pass, and it reads only the end of the log. Arulraj, Perron and Pavlo proposed it in 2016.

## In plain words

Picture a bank where every change to an account is a new card in a drawer, with a stamp number on it. The newest card of an account holds its balance. The drawer does not lose cards when the power fails.

Work goes in batches. The clerk files the new cards of a batch at once. When the whole batch is filed, he writes one line in a book: "everything up to 150 is done, and the next batch gets stamps up to 249".

After a power cut, he reads only the last line of the book. Cards with stamps after the last "done" number and below the promised limit belong to a batch that never finished. He ignores them when he reads a balance and throws them out later. Nothing needs to be copied or repaired before work starts again.

## When it applies

- The database keeps its tuples in NVM with fast persistent writes, for example on a memory bus, and the system can flush CPU cache lines to it.
- The system uses multiversion concurrency control, so a version is visible or not according to its timestamp, and the old version of a tuple stays in place while the new one is uncommitted. The paper also describes a variant for a single-version system.
- Commits are grouped. A group commit can then persist many changes and write one small log record.
- It does not apply to disks and flash. Writing every changed tuple at commit is a force policy, and on SSDs and hard disks this random writing costs more than a sequential log. The paper measures WBL as slower than WAL on those devices.

## The template

The system assigns increasing commit timestamps. The *dirty tuple table* (DTT), in volatile memory, lists the versions that each transaction of the open group has created or changed. A log record has two timestamps, $c_p$ and $c_d$, and the list of the *gaps* that still hold versions. Every timestamp up to $c_p$ belongs to a transaction whose fate is decided and whose changes are persistent. No transaction gets a timestamp of $c_d$ or more before the next group commit.

```pseudo id=main
COMMIT-GROUP()
L1  for each transaction of the group: persist every version that the DTT lists for it (flush its cache lines to NVM)
L2  c_p ← the largest timestamp given out; c_d ← c_p + G        ▷ the next group gets timestamps below c_d
L3  persist the log record ⟨c_p, c_d, the gaps that still hold versions⟩
L4  report the transactions of the group

RECOVER()
L5  read the last log record ⟨c_p, c_d, gaps⟩
L6  add the gap (c_p, c_d) to gaps; persist the record ⟨c_d, c_d + G, gaps⟩; open the database    ▷ no redo, no undo

VISIBLE(v)                                                      ▷ on every read
L7  v is visible if no gap (a, b) has a < v.ts < b, and v is the newest such version of its key

GC-STEP()                                                       ▷ in the background
L8  remove a version whose timestamp lies in a gap
```

Uncommitted versions may reach NVM at any time, as a cache line is evicted; this is a steal policy. An aborted transaction's versions are removed from the DTT and from NVM, which MVCC does anyway. A gap is dropped from the next log record when garbage collection has removed all its versions.

**Why it works.** Take a crash at any point. Every transaction that was reported belongs to a group whose log record was persisted, and line L1 persisted its versions before line L3. So every reported change is in NVM, with a timestamp at or below the $c_p$ of the last record, which is not in a gap. Every transaction whose group was not reported has a timestamp above that $c_p$ and below $c_d$, by the promise of line L2, so all its versions that reached NVM lie in the new gap of line L6 and are not visible. Older gaps stay in the record until they are empty. So the visible state is the newest version per key among the reported transactions. A crash during recovery only repeats line L6. The tests check this by a crash after every prefix of a random workload, new work after the restart and a second crash.

**Cost.** For one restart:

- *Log records read and written.* The last record is read, and one record is written. This does not depend on the length of the log or on the work since a checkpoint.
- *Pages read and written.* None during recovery. Garbage collection later removes the versions in the gaps.
- *Log volume per update.* None. Each group commit writes one record of two timestamps and its gap list. The data is written once, to its place in NVM, instead of once to the log and once to the database.
- *Checkpoints.* WBL needs no checkpoints of the kind that WAL uses to bound redo, since there is no redo. The work at a commit grows with the changes of the group, because they are all persisted at that moment.

**Measurements** (Arulraj, Perron and Pavlo, PVLDB 2016; the Peloton system and the YCSB benchmark, on the Intel persistent memory emulation platform (PMEP) with NVM latency set to 4 times that of DRAM, two Intel Xeon E5-4620 processors and 128 GB of memory): compared with write-ahead logging on the same emulated NVM, WBL gave about 1.3 times the throughput, recovered more than 100 times faster, and needed about 1.5 times less storage. On SSD and HDD, WBL was slower than WAL. These are measurements on an emulator in 2016, not on the NVM devices that came later.

**Example.** The code uses $G = 100$ and starts with the record ⟨0, 100, none⟩. T1 gets timestamp 1 and writes a = 11. Its group commits: the version is persisted and the record ⟨1, 101, none⟩ is written. T2 gets timestamp 2 and writes b = 22, and the cache evicts the version to NVM, but the system crashes before the next group commit. NVM now holds versions (a, 1) and (b, 2). Recovery reads ⟨1, 101, none⟩ and writes ⟨101, 201, (1, 101)⟩. The version (b, 2) lies in the gap, so b reads as 20, and a reads as 11. The next transaction gets timestamp 102. Garbage collection later removes (b, 2); after that, the next group commit drops the empty gap from its record.

## Classic examples

- **Peloton.** The paper implements WBL in the Peloton in-memory database with multiversion concurrency control on NVM, and compares it with a WAL implementation in the same system.
- **Replication.** Section 5 of the paper discusses WBL in a system with replicas. The log holds no data, so the changes that a replica needs must come from another source than the log.
- **Steal and force on NVM.** WBL is the force side of the [steal and force](/steal-and-force-policies/) trade-off, made cheap by fast persistent writes, together with steal made safe by versions and timestamps instead of before images.
- **Related ideas.** [Shadow paging](/shadow-paging/) also writes new data before the commit and needs no redo, but it switches a root pointer at commit. [Instant restart](/instant-restart/) keeps WAL and makes the system available before redo and undo end.

## Variations

- **Single-version storage.** Without multiversion tuples, an uncommitted change in place hides the old value, so the system must keep the old value somewhere until the commit. The paper describes a variant of WBL for such systems.
- **Size of the group.** A larger $G$ allows longer groups between log records; a crash then leaves a wider gap, which costs nothing at recovery but more work for garbage collection.
- **Gaps in the index.** Indexes in NVM must also ignore entries of versions in a gap, or remove them in the background.

## Pitfalls

- **Writing the log record before the data.** If line L3 runs before line L1 ends, a crash can lose the data of a reported transaction, and nothing in the log can redo it.
- **Breaking the promise of $c_d$.** If a transaction of the open group gets a timestamp of $c_d$ or more, its versions fall outside the gap after a crash and become visible although it never committed. A group must commit before the timestamps run out.
- **Dropping a gap too early.** If a gap leaves the log record while versions in it remain in NVM, those uncommitted versions become visible.
- **Volatile CPU caches.** A store to NVM is persistent only after its cache line is flushed and the flush is ordered. Line L1 needs the flush and a fence, not only the store.
- **Using it on block devices.** On disks and SSDs the forced random writes at each commit cost more than WAL.

## Exercises

1. In the example, T2 commits at once but its group never commits. Show that the client was never told of the commit, and that the result is correct.
2. A system crashes twice, once during the group after ⟨1, 101⟩ and once during the group after ⟨101, 201⟩. Give the gap list after the second recovery, and the versions that garbage collection removes.
3. Change line L2 to $c_d \leftarrow c_p$ and give a crash that makes an uncommitted version visible.
4. Compare the bytes written per update by WBL and by WAL with before and after images, for tuples of 100 bytes and an update of one field of 8 bytes.

## References
