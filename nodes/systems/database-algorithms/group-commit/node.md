---
tag: D9GM98
kind: technique
slug: group-commit
name: Group commit
aliases:
- batched log flush at commit
- group commit of log records
area: systems/database-algorithms
level: advanced
summary: "Make one log write durable for the commit records of many transactions, so the commit rate is no longer bounded by one log device write per transaction."
prereqs: [write-ahead-logging]
see_also: [checkpointing, crash-recovery, steal-and-force-policies, aries-recovery, replicated-log, two-phase-commit]
sources:
  - paper: doi:10.1145/602259.602261
    title: David J. DeWitt, Randy H. Katz, Frank Olken, Leonard D. Shapiro, Michael R. Stonebraker and David Wood, Implementation techniques for main memory database systems, Proceedings of ACM SIGMOD 1984, pages 1 to 8
    locator: the section on recovery for main memory databases, where commit records of several transactions share one log write; the attribution of group commit to this section is not checked against the text
  - paper: "Dieter Gawlick and David Kinkade, Varieties of concurrency control in IMS/VS Fast Path, IEEE Database Engineering Bulletin 8(2), June 1985, pages 3 to 10"
    locator: the description of Fast Path commit processing and its log; whether the paper names group commit is not checked
  - book: isbn:9781558601901
    title: Jim Gray and Andreas Reuter, Transaction Processing, Concepts and Techniques, Morgan Kaufmann, 1993
    locator: Chapter 9, Log Manager (log writes at commit and group commit), chapter level only
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: the chapters on crash recovery (logging during normal operation), chapter level only
---

*Group commit* is a way to make the commit rule of [write-ahead logging](/write-ahead-logging/) cheap. The rule says that a transaction's commit can be reported only after its commit record is on stable storage, so each commit waits for a log write. If each transaction did its own write, a log device that takes $D$ seconds per write could commit at most $1/D$ transactions per second, whatever the number of processors. With group commit, the commit records that arrive while one log write is in progress wait in memory and go to the disk together in the next write. One write makes many commits durable, and each commit is still acknowledged only after its record is durable.

## In plain words

When a transaction ends, the system must write a line to its journal on disk before it says "done". A disk write takes time, for example a few milliseconds, and a disk does one write at a time.

If every transaction made its own write, the system could finish only a few hundred transactions per second, however fast the rest of it is.

Group commit works like a bus. While one write is going to disk, new transactions that want to finish put their lines in a queue in memory. When the write ends, all the queued lines go to disk in the next write. Each transaction waits at most about two writes, but one write now finishes many transactions. No transaction is told "done" before its own line is on disk.

## When it applies

- Commits must be durable, so the log is forced at commit ([no-force](/steal-and-force-policies/) data pages, a forced log), and the log write is the bottleneck: a disk or an SSD with a high fixed cost per write, or a replicated log where each write is a network round trip.
- Many transactions commit at the same time, so a batch has more than one record.
- The application accepts a small extra wait for each commit in exchange for more commits per second.

## The template

```pseudo id=main
COMMIT(T)                                                     ▷ runs in the thread of T
L1  append ⟨commit, T⟩ to the log tail in memory; lsn(T) ← its LSN
L2  add T to the list of waiting transactions
L3  sleep until the log writer reports durableLSN ≥ lsn(T)
L4  acknowledge the commit of T to the client; release the locks of T
LOG-WRITER()                                                  ▷ one thread
L5  loop
L6      wait until the device is idle, the tail is not empty, and (the tail has k records or its oldest record has waited τ)
L7      end ← the last LSN in the tail; write the whole tail to the log device
L8      when the write completes: durableLSN ← end
L9      wake every waiting T with lsn(T) ≤ durableLSN
```

With $k = 1$ and $\tau = 0$ the writer starts a write as soon as the device is free, and the batch is whatever arrived during the previous write. This is the policy that adapts to the load by itself: under light load each write holds one record and there is no extra wait, and under heavy load each write holds all the records of one write time.

**Safety.** A transaction is acknowledged only at line L4, after line L3 has seen durableLSN at least its LSN, and durableLSN is set only at line L8, after the write that contains the record has completed. So a crash at any time loses no acknowledged commit. The log is written in LSN order, so a durable record also has all earlier records durable, which the WAL rule needs.

**Latency.** Under the policy $k = 1$, $\tau = 0$, a record that arrives while a write is in progress waits for the end of that write (less than $D$) and then for its own write ($D$). So the commit latency is at most $2D$, against $D$ for a lone transaction.

**Throughput.** A write holds all the records that arrived during the previous write. If commits arrive at rate $\lambda$, a write holds about $\lambda D$ records, and the device keeps up with any $\lambda$ as long as the write time does not grow much with the size of the batch. Without group commit the device saturates at $\lambda = 1/D$ and the queue grows without bound.

**Locks.** Line L4 releases the locks only after the log write. Some systems release them at line L1, when the commit record is in the tail (early lock release). This is safe for the commit order, because a transaction that reads the released data commits after $T$ in the log, so it cannot become durable before $T$; but its result must not be shown to a client before $T$ is durable.

## Classic examples

**A hand example.** The device takes $D = 10$ time units per write. Commits arrive at times 0, 1, 2, 3 and 12, from $T_1$ to $T_5$.

| write | start | end | records | acknowledged |
|---|---|---|---|---|
| 1 | 0 | 10 | $T_1$ | $T_1$ at 10 |
| 2 | 10 | 20 | $T_2$, $T_3$, $T_4$ | at 20 |
| 3 | 20 | 30 | $T_5$ | at 30 |

The latencies are 10, 19, 18, 17 and 18, and three writes do five commits. With one write per commit, the five writes end at 10, 20, 30, 40 and 50, and the latencies are 10, 19, 28, 37 and 38.

**Under load.** One commit every 2 units and $D = 10$: group commit does about one write per 10 units with 5 records each, and no latency exceeds 20. With one write per commit, the device can do only one commit per 10 units, and after 1000 commits the last one waits more than 7000 units.

**Waiting for a batch.** With $k = 3$ and $\tau = 8$, commits at times 0 and 1 wait until time 8 (the timeout of the first record), and a write with two records runs from 8 to 13. A commit at 30 waits until 38. Here the policy adds latency at light load and gains nothing, which is why most systems use $k = 1$ or a very small $\tau$.

## Variations

- **Timer-based group commit.** The writer waits a fixed time, or until a batch size is reached, before it writes. This can give larger batches with a slow device, at the price of latency at light load. Helland and others studied the choice of the timer for high-volume systems in 1987.
- **Leader and followers.** No separate writer thread: the first transaction that finds the device free becomes the leader, writes the tail for all waiting transactions, and wakes them. MySQL's InnoDB and binary log use a staged form of this.
- **Pipelined log writes.** With a device that accepts several writes at once, the writer can start the next write before the previous one ends, as long as durableLSN only advances over a prefix of completed writes.
- **Asynchronous commit.** Some systems can acknowledge before the write, for example PostgreSQL with synchronous_commit set to off. This gives up durability for the last moments before a crash and is not group commit.
- **Replicated logs.** A [replicated log](/replicated-log/) batches entries in one consensus round in the same way, and the participants of [two-phase commit](/two-phase-commit/) can group their prepare and commit records.

## Pitfalls

- **Acknowledging at the start of the write.** If the client is told "done" when the write starts (line L7) rather than when it ends (line L8), a crash during the write loses a commit that the client was told about.
- **Waking on the wrong LSN.** A transaction must wait for durableLSN $\ge$ its own LSN, not for the next write to end: a record that arrives during a write is not in that write.
- **A long timeout.** A large $\tau$ or $k$ adds its full value to the latency of every commit when the load is light, and the throughput gain is zero there.
- **Reading released data.** With early lock release, a read-only transaction that read data of a not-yet-durable commit can report it to a client. It must wait for that LSN to become durable before it answers.
- **A device that lies.** A disk write cache that reports completion before the data is on the medium breaks line L8. The log device must honour a flush, or have a write cache with battery or capacitor backup.

## Exercises

1. In the hand example, add a commit at time 21. Which write holds it, and what is its latency?
2. Prove that under the policy $k = 1$, $\tau = 0$ no commit waits longer than $2D$ if the write time is $D$ for any batch size.
3. A write of $b$ records takes $D_0 + b c$. Find the largest commit rate that group commit can sustain.
4. Give a schedule with early lock release where a client sees a value that is lost after a crash, if the reader does not wait for durability.
5. With a replicated log of three nodes and a round trip of $R$, what is the analogue of $D$, and what limits the batch size?

## References
