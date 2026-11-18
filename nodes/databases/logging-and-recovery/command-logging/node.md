---
tag: DQZNNJ
kind: technique
slug: command-logging
name: Command logging
aliases:
- stored procedure logging
area: databases/logging-and-recovery
level: advanced
summary: Log only the transaction requests of a deterministic in-memory database and recover by replaying them from a checkpoint.
prereqs: [logical-logging, group-commit, checkpointing]
see_also: [physiological-logging, write-ahead-logging, calvin-deterministic-transactions, state-machine-replication, crash-recovery, write-behind-logging, point-in-time-recovery, replicated-log]
sources:
  - paper: doi:10.1109/ICDE.2014.6816685
    title: Nirmesh Malviya, Ariel Weisberg, Samuel Madden and Michael Stonebraker, Rethinking main memory OLTP recovery, Proceedings of the 30th IEEE International Conference on Data Engineering (ICDE), 2014, pages 604 to 615
    locator: the command log record format, synchronous logging with group commit, the transaction-consistent snapshots, recovery by replay, and the measurements against ARIES-style logging in VoltDB with TPC-C and Voter, paper level
  - paper: doi:10.1145/128765.128770
    title: C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh and Peter Schwarz, ARIES, a transaction recovery method supporting fine-granularity locking and partial rollbacks using write-ahead logging, ACM Transactions on Database Systems 17(1), 1992, pages 94 to 162
    locator: physiological log records and redo with the page_LSN, the baseline that command logging replaces, paper level
---

Command logging, or stored procedure logging, is a recovery technique for in-memory databases in which every transaction is a call of a stored procedure. The log holds one small record per transaction: its id, the name of the procedure and the parameters, and no data at all. Recovery loads the newest snapshot of the database and runs the logged procedures again, in the same order. This works only if the execution is *deterministic*: the same procedure with the same parameters on the same state must make the same changes. Malviya, Weisberg, Madden and Stonebraker (ICDE 2014) built it in VoltDB and measured it against [physiological logging](/physiological-logging/), the record format of ARIES. It is the far end of [logical logging](/logical-logging/): the logged operation is the whole transaction.

## In plain words

A cook keeps a notebook. One way is to write down, after each step, how much of each thing is in each pot. That takes many lines per dish.

Another way is to write only the order: "dish 41, soup, for 3 people". If the cook always follows the recipe in the same way, the order is enough. After a fire, the cook takes the last photo of the kitchen and cooks every order written after the photo again, in the same order. The kitchen ends up the same.

This only works if the recipe never says "add a pinch, as you like". Every choice must come from the order itself. A random choice is fine only if it is made with a fixed rule, for example from the order number.

Short notes make cooking fast. The price is that recovery must cook every dish again.

## When it applies

- The whole database is in main memory, and the disk holds only the log and snapshots.
- Every transaction is a stored procedure, or another request that the system can run again from its text and its parameters.
- Execution is deterministic: transactions run in one fixed serial order, for example one at a time per partition as in VoltDB, or in an order that a sequencer fixes before execution as in [Calvin](/calvin-deterministic-transactions/). Calls to the clock or to a random source must take their values from the log record, for example from a seed equal to the transaction id.
- Fast normal processing matters more than fast recovery, or recovery is rare because replicas take over after a failure.

## The template

The log is an append-only file of command records. A snapshot is *transaction consistent*: it holds the effects of exactly the transactions up to one point in the serial order, and it stores that point.

```pseudo id=main
EXECUTE(proc, params)                                  ▷ normal work, one transaction at a time
L1  t ← the next transaction id; append ⟨t, proc, params⟩ to the log tail
L2  run proc(params) on the database in memory, with a random source seeded by t
L3  at the next group commit: write the log tail to stable storage, then report its transactions to the clients

CHECKPOINT()
L4  between two transactions: mark a snapshot of the database with the LSN of the last logged transaction
L5  write the snapshot to disk while transactions go on (copy on write); when it is complete, it becomes the newest checkpoint

RECOVER()
L6  load the newest complete snapshot, with its LSN c, and rebuild the indexes in memory
L7  for each command record r in the stable log after c, in log order do
L8      run r.proc(r.params) with the random source seeded by r.t
```

A transaction that the procedure itself aborts writes the same record. Its replay aborts again, at the same point, because the state is the same. A transaction whose record is in the tail at a crash was never reported, and it is lost with the tail: the state after recovery is that of a serial run of exactly the stable commands. The snapshot in line L5 must hold only the effects of stable commands; the code forces the tail before it records a snapshot.

**Why it works.** By determinism and induction over the log, the state after the replay of the first $i$ records is the state that normal work had after transaction $i$. The snapshot is the state after transaction $c$, so lines L7 and L8 give the state after the last stable record. Every reported transaction is stable, by line L3. Recovery writes nothing to disk, so a crash during recovery only makes it start again. The tests check this by a crash after every prefix of a random workload with group commits and checkpoints.

**Cost.** For one restart:

- *Log records read.* The command records after the snapshot. The snapshot interval bounds them: a checkpoint is the only thing that shortens the replay.
- *Pages read and written.* The whole snapshot is read once. Replay writes nothing to disk; the next checkpoint writes a new snapshot.
- *Work.* Each replayed transaction runs again in full, reads included, so replay costs about as much as the original work. Physiological redo instead applies only the changes, and can run in parallel per page.
- *Log volume per update.* One record per transaction, whatever the number of updates in it. Malviya et al. report command records of 50 to 170 bytes.

**Measurements** (Malviya, Weisberg, Madden and Stonebraker, ICDE 2014; VoltDB with command logging and with an ARIES-style physiological log; a two-socket Intel Xeon machine at 2.4 GHz with 8 cores and 24 GB of memory; group commit every 5 ms):

- On TPC-C, throughput with command logging was about 1.5 times that with physiological logging. With 50 percent distributed transactions the gain was still about 1.4 times.
- Physiological logging wrote about 10 times as many log bytes on TPC-C.
- Recovery was slower with command logging: replay of the physiological log was about 1.5 times faster on TPC-C and about 5 times faster on the Voter benchmark.

These numbers hold for that system, workload and machine. They are not a guarantee for other systems.

**Example.** Accounts a, b, c and d hold 100 each. The log holds three records: 1001 transfer(a, b, 500), 1002 transfer(a, b, 60), 1003 transfer(a, b, 60). The first aborts, since a has only 100. The second moves 60. The third aborts, since a has only 40. The newest snapshot has LSN 0. After a crash, recovery loads it and runs the three records again; the same two aborts happen, and the state is a = 40, b = 160. A physiological log would hold the before and after values of a and b for record 1002, and nothing for the aborts.

## Classic examples

- **VoltDB** logs the stored procedure calls of each transaction with group commit and takes asynchronous transaction-consistent snapshots, as described by Malviya et al. It runs the transactions of a partition one at a time, so each partition is deterministic, and a coordinator logs the distributed transactions.
- **Calvin** fixes the order of the transaction inputs before it runs them, and replicates and logs only the inputs. See [Calvin](/calvin-deterministic-transactions/).
- **State machine replication.** A [replicated log](/replicated-log/) of commands that every replica applies in the same order is the same idea used for replication instead of recovery; see [state machine replication](/state-machine-replication/).
- **Statement-based replication** in some SQL systems ships the SQL text of each statement to replicas. It has the same need for determinism, and it fails on statements whose effect depends on the clock or on an order of rows that is not fixed.

## Variations

- **Command logging with physical logging for some transactions.** Log the changes of a transaction that is not deterministic, or that is very long, and the command for the others.
- **Parallel replay.** Replay can run the commands of different partitions in parallel, as long as each partition keeps its order and distributed transactions are synchronized across the partitions they touch.
- **Replicas instead of recovery.** With a replica that runs the same commands, a failure is handled by failover, and the slow replay is needed only when all replicas fail.
- **Asynchronous command logging.** Report a transaction before its record is stable. This is faster but loses reported transactions in a crash.

## Pitfalls

- **Hidden non-determinism.** A call to the clock, to a random source that is not seeded from the log, to an outside service, or a loop over a hash table whose order is not fixed makes the replay differ. The tests show a procedure that reads a clock and gets another value in the replay.
- **A snapshot that is not transaction consistent.** A fuzzy snapshot of the kind that physiological redo accepts is wrong here: replaying a whole transaction on a state that already holds half of it applies the first half twice.
- **A snapshot ahead of the stable log.** If the snapshot holds the effect of a command that the crash then loses from the tail, the next transaction after recovery gets the same LSN with other contents.
- **Long replay.** Replay time grows with the time since the last snapshot and with the cost of the transactions, reads included. Take snapshots often enough for the recovery time that the system must meet.
- **A changed procedure.** If the code of a stored procedure changes between the run and the replay, the replay runs the new code. The log or the snapshot must name the version of each procedure.

## Exercises

1. A procedure reads all rows of a table and updates the first one in the order of a hash table. Give two runs with the same log and different results, and two ways to make the procedure deterministic.
2. In the example, the snapshot is taken after record 1002 but before it is stable, and the tail is lost. Describe the state after recovery and the next LSN.
3. A transaction updates 1,000 rows of 100 bytes each. Compare the log volume of command logging and of physiological logging with before and after images.
4. Prove that replaying the stable log from a transaction-consistent snapshot gives the state after the last stable command, and show where the proof uses determinism.

## References
