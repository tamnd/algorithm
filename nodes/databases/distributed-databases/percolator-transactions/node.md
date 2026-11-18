---
tag: FVBYZN
kind: algorithm
slug: percolator-transactions
name: Percolator transaction protocol
aliases:
- Percolator
area: databases/distributed-databases
level: research
summary: "Snapshot isolation over a key-value store that has only single-row transactions, using a timestamp oracle, a primary lock per transaction and lazy cleanup by readers."
solves: [concurrency-control]
model: asynchronous-model
complexity:
  vars: {r: the number of items that a transaction reads, w: the number of items that it writes}
  messages: {best: "2 r + 4 w + 4"}
  space: {extra: "O(w)"}
properties: {deterministic: true, recursive: false}
history:
  year: 2010
  people: [Daniel Peng, Frank Dabek]
  note: "Peng and Dabek described Percolator at OSDI 2010. Google built it to update its web search index incrementally in place of a chain of MapReduce jobs."
prereqs: [snapshot-isolation, two-phase-commit]
see_also: [multiversion-concurrency-control, write-skew, serializable-snapshot-isolation, clock-si, calvin-deterministic-transactions, ramp-transactions, truetime, crash-failure]
sources:
  - paper: url:https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Peng.pdf
    title: "Daniel Peng and Frank Dabek, Large-scale incremental processing using distributed transactions and notifications, OSDI 2010, pages 251 to 264"
    locator: "Section 2.2 (transactions, the lock, data and write columns, cleanup, and the pseudocode in Figure 6), Section 2.3 (the timestamp oracle and the proof that Get sees all earlier commits), Sections 3.2 and 3.3 (overhead against Bigtable and the TPC-E-like benchmark)"
---

Percolator is the transaction protocol that Google built on top of Bigtable, a key-value store that can change only one row atomically. It gives multi-row transactions with [snapshot isolation](/snapshot-isolation/). A central timestamp oracle gives each transaction a start timestamp and a commit timestamp. A writer first locks every cell it writes and stores the new data, and then commits with a form of [two-phase commit](/two-phase-commit/) in which the client is the coordinator and one of its locks, the *primary*, holds the decision. There is no lock server and no recovery process. If a client crashes, the next reader that finds one of its locks looks at the primary and either finishes the commit or erases the transaction.

## In plain words

Each cell keeps its old versions, labelled by time. A transaction reads the versions committed before it started, so it sees a fixed photograph of the table.

To write, a transaction puts a "locked by me" note next to the new value of every cell it changes. One note is the main note, and the others say "ask the main note". The transaction then gets a commit time and replaces the main note by a record "my value is valid from this time". That one change commits the transaction. Then it replaces the other notes in the same way.

A reader that finds a note waits. If the writer seems dead, the reader looks at the main note. If it has become a commit record, the reader finishes the job. If it is still a note, the reader erases it, and the writer can never commit.

## The problem

A table is split over many servers. Each cell $x$ has many versions, each with a timestamp, and the store can read and change the cells of one row in one atomic step (a row transaction). Clients run transactions that read some cells and then write some cells. The model is the [asynchronous model](/asynchronous-model/) for safety, and clients can fail by stopping ([crash failure](/crash-failure/)).

The protocol must give snapshot isolation:

1. Each transaction reads the last committed version of each item as of its start timestamp.
2. If two transactions write the same item, one of them commits before the other starts (first committer wins).
3. All writes of a transaction become visible together or not at all.

There is no separate transaction manager that could recover the work of a crashed client. The data in the table must be enough to finish or erase every transaction.

## The algorithm

Each cell $x$ has three columns, each indexed by timestamp. $\mathrm{data}[x][s]$ is the value written by the transaction with start timestamp $s$. $\mathrm{lock}[x][s]$ is a lock of that transaction, and it holds the name of the primary cell. $\mathrm{write}[x][c] = s$ is a write record: the transaction with start timestamp $s$ committed with commit timestamp $c$, and its value is $\mathrm{data}[x][s]$. The timestamp oracle hands out strictly increasing timestamps. Each step on one cell (GET, PREWRITE, and each commit and cleanup step) is one row transaction.

```pseudo id=main
PERCOLATOR
▷ client: transaction T
L1  T.start ← a timestamp from the oracle
L2  for each item x that T reads: v[x] ← GET(T, x)
L3  compute the writes W from v; primary ← the first item of W; the other items of W are secondaries
L4  for each x in W, primary first: if not PREWRITE(T, x, primary) then erase the locks of T and abort
L5  T.commit ← a timestamp from the oracle
L6  on the primary, in one row transaction: if lock[primary][T.start] is gone then abort; write[primary][T.commit] ← T.start; erase the lock   ▷ the commit point
L7  for each secondary x: write[x][T.commit] ← T.start; erase lock[x][T.start]
▷ GET(T, x), one row transaction
L8  if x has a lock with a timestamp s ≤ T.start: if its owner seems dead then CLEANUP(x, s); wait and go back to L8
L9  c ← the largest write timestamp of x with c ≤ T.start; return data[x][write[x][c]]
▷ PREWRITE(T, x, p), one row transaction
L10 if x has a write record with timestamp ≥ T.start, or a lock with any timestamp, then return false
L11 data[x][T.start] ← W[x]; lock[x][T.start] ← p; return true
▷ CLEANUP(x, s)
L12 if the primary of s has a write record that points to s then roll forward: write the same record on x and erase lock[x][s]; else erase the lock and data of s at the primary, then at x
```

Line L10 is the write-write conflict check. A write record after the start of $T$ means that a concurrent transaction has already committed $x$. A lock means that another transaction is in the middle of a commit. In both cases $T$ aborts at once, so writers never wait for each other.

Line L8 is the reason that the oracle makes reads correct. A writer locks all its cells before it asks for its commit timestamp, so if its commit timestamp is below the start timestamp of a reader, its locks or its write records are already in place when the reader looks.

The decision of a transaction is in one cell. Line L6 checks that the primary lock is still there and replaces it by the write record in the same row transaction. A cleanup at line L12 erases the primary lock first. So a writer and a cleanup cannot both succeed: either the record is there and every later cleanup rolls forward, or the lock is gone and line L6 fails for ever.

## Example

The test file builds this case. Items $a = 0$ and $b = 10$ were written by a loader with timestamps 1 and 2. Transaction $T_1$ writes $a = 5$ and $b = 6$, so $a$ is its primary. It crashes right after its commit point. Then $T_2$ reads $a$ and $b$.

| step | line | what happens |
|---|---|---|
| 1 | L1 | $T_1.\mathrm{start} = 3$ |
| 2 | L11 | $\mathrm{data}[a][3] = 5$, $\mathrm{lock}[a][3] = a$ |
| 3 | L11 | $\mathrm{data}[b][3] = 6$, $\mathrm{lock}[b][3] = a$ |
| 4 | L5 | $T_1.\mathrm{commit} = 4$ |
| 5 | L6 | $\mathrm{write}[a][4] = 3$, the lock on $a$ is erased; $T_1$ is committed, then its client crashes |
| 6 | L1 | $T_2.\mathrm{start} = 5$ |
| 7 | L9 | $a$ has no lock; its largest write timestamp up to 5 is 4, so $T_2$ reads $\mathrm{data}[a][3] = 5$ |
| 8 | L8 | $b$ has the lock $\mathrm{lock}[b][3]$, and its owner is dead |
| 9 | L12 | the primary $a$ has the record $4 \to 3$, so $T_2$ writes $\mathrm{write}[b][4] = 3$ and erases the lock |
| 10 | L9 | $T_2$ reads $\mathrm{data}[b][3] = 6$ |

$T_2$ sees both writes of $T_1$. If $T_1$ crashes one step earlier, after step 4, the primary still has its lock. Then at step 7 $T_2$ finds the lock on $a$, rolls it back, and reads $a = 0$; on $b$ it rolls back again and reads $b = 10$. Neither write of $T_1$ is ever visible, and $T_1$ can no longer commit.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It is a theorem in the model of the page, and it extends the argument of Section 2.3 of the paper. The main steps are these.

1. Every write record belongs to a committed transaction, because the record of a secondary is written only after the record of the primary.
2. The commit point is final. Line L6 and the roll back of line L12 both work on the primary lock in one row transaction, so exactly one of them succeeds.
3. Snapshot reads: a writer with commit timestamp $c$ below the start timestamp $s$ of a reader locked its cells before it got $c$, and the reader got $s$ after $c$. So the reader sees the lock and waits, or sees the write record.
4. First committer wins: of two overlapping writers of $x$, the one that runs line L10 second sees the lock or the newer write record of the other and aborts.
5. All or nothing: a reader that meets a lock of a dead client rolls it forward if the primary committed and back if not, so no transaction is ever half visible.

Cleanup is safe even when the owner is alive, because of step 2. The owner then fails at line L6 and aborts. So the test of liveness (a token in the Chubby lock service and a wall time in the lock, in the paper) affects only performance, not correctness.

The tests compare each run with a brute force oracle that knows only the committed writers and their timestamps. It checks that every read returns the value of the committed writer with the largest commit timestamp below the start of the reader, that no two committed writers of the same item overlap, and that after a final read of every item no lock is left, every committed writer has its record on each of its items, and no data of an uncommitted writer is left. Each run has 3 to 5 transactions over 4 items, and the scheduler interleaves the row transactions with a seeded generator. Over 300 runs with no crash, 362 of 1186 transactions aborted at line L10 and 569 writers committed. Over 300 runs with one client crash, half of them at the commit point, readers rolled 36 locks forward and 23 back. In 200 runs where a reader also cleans up live clients with probability 0.3, 46 live writers lost their primary lock and aborted at line L6. All runs passed the oracle (a measurement of this simulation). The same tests fail when line L8, the check of line L6 or the write check of line L10 is removed.

## Complexity

A transaction that runs alone and reads $r$ items and writes $w \ge 1$ items makes $r + 2w + 2$ requests: two to the oracle, $r$ reads, $w$ prewrites and $w$ commits, so $2r + 4w + 4$ messages with the replies (a theorem, Theorem 4 of the proof). The prewrites of the secondaries can go in parallel after the primary, and so can the commits of the secondaries, so the latency is a few round trips, not $w$ of them. Each prewrite is a read and a write on the cell, so a one-cell write costs a check for locks, a write of the lock and a second write to erase it, beyond the write of the data. Peng and Dabek measured about four times the cost of a raw Bigtable write for a transaction that writes one cell (a measurement, 2010, Section 3.2).

The extra space is one lock per written cell while the transaction runs, $O(w)$, and the old versions of each cell until they are garbage collected. Under contention the cost has no bound: a writer that meets a lock aborts, and a reader that meets a lock waits.

Peng and Dabek ran the system on servers in a Google data center, x86 machines with Linux and commodity SATA drives. Moving the indexing system from MapReduce to Percolator cut the average processing latency of a document by a factor of 100. The oracle served about 2 million timestamps per second from one machine, with batching of requests (Section 2.3). On a benchmark based on TPC-E, Percolator ran 11,200 transactions per second on 15,000 cores, with an average latency of 2 to 5 seconds, and it scaled almost linearly from 11 to 15,000 cores. The fastest commercial TPC-E system then ran 3,183 tpsE on one machine with 64 Nehalem cores, and the authors estimate that Percolator used about 30 times more CPU per transaction (all measurements, 2010, Section 3).

## Properties

- Snapshot isolation (a theorem): reads see the committed state at the start timestamp, and concurrent writers of one item cannot both commit.
- Reads take no locks. A reader waits only when it meets a lock of a writer that is in the middle of its commit.
- No central lock manager and no recovery process. The state of every transaction is in the table, and readers clean up lazily.
- A single commit point, the primary lock, which holds the decision for all cells of the transaction.
- A central timestamp oracle that every transaction calls twice. It is a single point of failure and a limit on throughput.
- Not serializable: write skew is possible.

## Variants and improvements

- Batching at the oracle: each worker keeps only one request to the oracle open, and the oracle allocates ranges of timestamps on stable storage, so it can restart without going back in time (Section 2.3).
- [Clock-SI](/clock-si/) removes the oracle and takes snapshot timestamps from the loosely synchronized clocks of the partitions.
- Notifications and observers: Percolator runs user code when an observed column changes, each run in its own transaction, and at most one observer transaction commits for each change of the column (Section 2.4). This is the part of Percolator that drives incremental processing.
- To get serializability on top of the same storage, a system can add the read checks of [serializable snapshot isolation](/serializable-snapshot-isolation/) or use locks on reads. [Calvin](/calvin-deterministic-transactions/) and systems with [TrueTime](/truetime/) take other routes.

## When to use it

Use Percolator when the storage already gives atomic single-row changes and multi-version cells, and you need multi-row transactions with snapshot isolation without a separate transaction manager. It suits workloads that tolerate latency of seconds and have few conflicts, such as incremental processing of a large data set, which was its purpose. It is a poor fit for interactive OLTP with tight latency targets or hot items: conflicting writers abort and retry, and readers can wait behind slow writers.

## Pitfalls

- The code on this page is a toy. One process runs all clients, the table is a dict, each method stands for a row transaction, and there is no network, no Chubby, no time-outs and no garbage collection.
- Snapshot isolation is not serializable. The [write skew](/write-skew/) test in the test file commits two transactions that each keep $x + y \ge 1$ but together set $x = y = 0$.
- The primary must be locked first and committed first. If a secondary could commit before the primary, a cleanup could roll the primary back after part of the transaction was visible.
- The oracle must never go back in time, also after a restart. If it gives out a timestamp twice or out of order, the argument of Section 2.3 fails and a reader can miss a committed write.
- A reader must not ignore a lock with a timestamp below its start, even if the owner seems slow. The tests fail if line L8 is removed.
- Locks of a dead client stay until a reader or writer finds them, and writers abort at line L10 when they meet such a lock. A writer that never reads the cell keeps aborting until some reader cleans it up.
- A cleanup that rolls back a live client costs that client its transaction. The liveness check matters for performance.

## Implementations

## History

Google built its web search index with a series of 100 MapReduce jobs over the whole repository, so a new document had to wait for a full pass. To add new documents with low latency, Daniel Peng and Frank Dabek designed Percolator, which adds multi-row transactions and notifications to Bigtable, and presented it at OSDI 2010. With Caffeine, the indexing system built on it, the average age of a document in a search result dropped by nearly 50 percent (Section 1). The design uses the definition of snapshot isolation of Berenson et al. (SIGMOD 1995) and runs two-phase commit on the client, with the decision stored in the data itself.

## References
