---
tag: 9E7PE4
kind: algorithm
slug: clock-si
name: Clock-SI
aliases:
- clock-based snapshot isolation
area: databases/distributed-databases
level: research
summary: "Snapshot isolation for partitioned data that takes snapshot and commit timestamps from loosely synchronized local clocks, with no central timestamp server."
solves: [concurrency-control]
model: asynchronous-model
complexity:
  vars: {r: the number of items read on other partitions, p: the number of partitions written}
  messages: {best: "2 r", worst: "2 r + 3 p"}
  space: {extra: "O(p)"}
properties: {deterministic: true, recursive: false}
history:
  year: 2013
  people: [Jiaqing Du, Sameh Elnikety, Willy Zwaenepoel]
  note: "Du, Elnikety and Zwaenepoel presented Clock-SI at SRDS 2013. It removes the central timestamp authority that earlier partitioned SI systems such as Percolator used."
prereqs: [snapshot-isolation, two-phase-commit, clock-synchronization]
see_also: [percolator-transactions, multiversion-concurrency-control, write-skew, ntp, truetime, hybrid-logical-clocks, session-guarantees, sharding]
sources:
  - paper: doi:10.1109/SRDS.2013.26
    title: "Jiaqing Du, Sameh Elnikety and Willy Zwaenepoel, Clock-SI, snapshot isolation for partitioned data stores using loosely synchronized clocks, SRDS 2013, pages 173 to 184"
    locator: "Section II (the model, the definition of SI and the two examples of unavailable snapshots), Section III with Algorithms 1 and 2 (read and commit protocols, older snapshots, the correctness argument), Section V (evaluation)"
---

Clock-SI implements [snapshot isolation](/snapshot-isolation/) for a data store that is split into partitions, with no central timestamp server. A transaction takes its snapshot timestamp from the clock of the partition where it starts, and an update transaction takes its commit timestamp from the clocks of the partitions it writes. The clocks are kept close by a protocol such as [NTP](/ntp/), but they are never exact. Clock-SI stays correct for any clock skew because a partition delays a read in two cases: when its own clock has not yet reached the snapshot timestamp, and when a transaction that may commit before the snapshot is still committing. The skew changes only how long reads wait.

## In plain words

Each partition keeps old versions of each item, labelled with the time of their commit. A transaction reads the clock of the partition where it starts and then reads the version of each item that was committed before that time.

Two things can go wrong. The clock of another partition may be behind, so a transaction there could still commit "before" our time after we have read. And a transaction may have got its commit time but not yet finished its commit. In both cases our reader waits a little: until the slow clock passes our time, or until the commit is finished. After that, nothing can appear below our time, so what we read is a fixed photograph.

## The problem

Data is split into partitions, and each partition is on one server with its own clock. Clocks move forward but can differ from each other by an unknown amount. Clients start transactions at some partition, called the *originating partition*, which runs the reads and writes and talks to other partitions when it needs their items.

The system must give snapshot isolation, as in Section II-B of the paper:

1. Each transaction reads a consistent snapshot: all writes of transactions committed before its snapshot timestamp, and no other writes.
2. Committed update transactions are in a total order given by their commit timestamps.
3. Of two concurrent transactions that write the same item, at most one commits.

Earlier systems, such as [Percolator](/percolator-transactions/), get both timestamps from a central server. That server is a single point of failure, it adds a round trip at the start and one at the commit, and it can limit throughput. Clock-SI wants the same isolation with timestamps from local clocks. The model is the [asynchronous model](/asynchronous-model/) for safety: no bound on message delay or clock skew is needed for correctness.

## The algorithm

Each partition keeps a list of versions for each item, and for each transaction that is committing or prepared there, the keys it writes and its commit or prepare timestamp. Writes are buffered at the originating partition until the commit.

```pseudo id=main
CLOCK-SI
▷ originating partition o of transaction T
L1  T.snapshot ← clock(o) − Δ
▷ partition q serves a read of item k by T
L2  if T came from another partition and T.snapshot ≥ clock(q): wait until clock(q) > T.snapshot
L3  if a transaction that writes k is committing or prepared at q with a timestamp < T.snapshot: wait until it is committed or aborted
L4  return the latest committed version of k with a timestamp < T.snapshot
▷ commit of T
L5  if T wrote nothing: commit at once
L6  if T writes one partition q: at q (after the wait of L2), certify; state committing; T.commit ← clock(q); log; install
L7  else send PREPARE to each partition q that T writes; q first waits as in L2
L8  at q, certify: no other transaction is committing or prepared on the keys, and no version of them is newer than T.snapshot; if so, state prepared, prepare timestamp ← clock(q); reply with it, else reply no
L9  if every partition replied with a timestamp: T.commit ← the largest prepare timestamp; log the decision; send COMMIT(T.commit)
L10 at q on COMMIT: install the writes of T as versions with timestamp T.commit
L11 else: send ABORT to every partition that T writes
```

Line L2 handles a clock that is behind. If the clock of $q$ has not reached the snapshot, another transaction could still commit at $q$ with a timestamp below the snapshot, and the reader would miss it. After the wait, every later commit at $q$ gets a larger timestamp. The same wait is applied to PREPARE and to a remote local commit, so a commit timestamp is always above the snapshot of its own transaction.

Line L3 handles a commit in progress. A transaction that has a commit or prepare timestamp below the snapshot may still commit, and its versions must be in the snapshot, so the reader waits for the outcome.

Line L9 takes the largest prepare timestamp. A participant that does not delay a reader (because its prepare timestamp is above the snapshot) must also not see the transaction committed below the snapshot, so the commit timestamp must be at least every prepare timestamp. The proof gives a counterexample for the smallest one.

$\Delta \ge 0$ lets a transaction read a slightly older snapshot. With a large enough $\Delta$ the waits of lines L2 and L3 almost never happen, at the cost of staler data and a few more aborts.

## Example

The test file builds this case. Partition $P_0$ has a clock 5 ticks ahead of $P_1$. A clock reading at partition $p$ is $1000 \cdot (\text{tick} + \text{skew}) + p$, and two readings at one partition differ by at least 10.

| tick | line | what happens |
|---|---|---|
| 0 | L1 | $T_1$ starts at $P_0$; $T_1.\mathrm{snapshot} = 5000$; it reads $b_0$, which is on $P_1$ |
| 1 or 2 | L2 | the read reaches $P_1$, whose clock is 1001 or 2001, below 5000, so it waits |
| 3 | L1, L6 | $T_2$ starts at $P_1$ with snapshot 3001, writes $b_0 = 200$ and gets the commit timestamp 3011 |
| 5 | L6 | the commit record of $T_2$ is on disk, and its version of $b_0$ at 3011 is installed |
| 5 | L2, L4 | the clock of $P_1$ is 5001; the read goes on and returns $b_0 = 200$ from the version at 3011 |

$T_2$ committed with a timestamp below the snapshot of $T_1$, so snapshot isolation requires $T_1$ to see it. Without the wait of line L2, the read would run at tick 1 or 2 and return the old value 20, and the snapshot of $T_1$ would miss a write that comes before it in the commit order. The test checks both runs.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It is a theorem in the model of the page and does not assume any bound on the clock skew; the paper makes the same point in Section III-D. The main steps are these.

1. After a partition serves a request of $T$ (after the wait of line L2), every later reading of its clock is above $T.\mathrm{snapshot}$.
2. A committed writer $W$ of $k$ with commit timestamp below $T.\mathrm{snapshot}$ was certified at the partition of $k$ before $T$ read there; otherwise its timestamp there would be above the snapshot by step 1. So when $T$ reads, $W$ is pending, and line L3 waits, or it is installed.
3. So line L4 sees exactly the committed writers below the snapshot.
4. Certification at line L8 is atomic at each partition, and it rejects a writer when an overlapping writer of the same item is pending or installed with a newer timestamp. So two concurrent writers of one item cannot both commit.

The tests compare each run with a brute force oracle that knows only the committed writers and their timestamps. It checks every returned read against the committed writer with the largest commit timestamp below the snapshot, checks that overlapping committed writers never share an item, and checks the final versions and that nothing is left pending. Each run has 3 to 6 transactions over 6 items on 3 partitions, clock skews of up to 3 ticks each way and messages of 1 or 2 ticks, all from a seeded generator. Over 300 runs, 561 writers committed and 350 transactions aborted; reads waited 416 times for a clock and 72 times for a pending commit. In 200 more runs a coordinator crashes, before the votes arrive or after it logged the commit, and votes sent to it while it is down are lost. All runs pass. With line L2 removed, 30 of the 300 runs break snapshot isolation; with line L3 removed, 53; with the smallest prepare timestamp at line L9, 44 (measurements of this simulation).

## Complexity

Let $r$ be the number of items that a transaction reads on other partitions and $p$ the number of partitions it writes. The reads take $2r$ messages. A commit on one partition takes 2 messages if it is not the origin, and two-phase commit takes 3 messages per participant other than the origin (a theorem, Theorem 4 of the proof). A central timestamp server would add one round trip for a read-only transaction and two for an update transaction; Clock-SI saves these.

The cost is waiting. A wait at line L2 lasts at most the clock skew minus the one-way message delay, and a wait at line L3 at most the time to write a commit record plus, for a distributed commit, a round trip (Section III-A of the paper). These bounds hold only when skew and delays are bounded, so they are a property of the deployment, not a theorem in the asynchronous model. In the simulation, $\Delta = 6$ ticks cut the number of waits over 200 runs from 333 to 10.

Du, Elnikety and Zwaenepoel built a partitioned in-memory key-value store in C++ and compared Clock-SI with SI that uses a timestamp server. In a LAN of servers with two Intel Xeon processors each, Linux 3.2.0, Gigabit Ethernet and a SATA disk for the log, short read-only transactions on YCSB had about 50% lower latency on one partition, and throughput improved by up to 50%. On Amazon EC2 with partitions in US West, US East and Europe and the timestamp server in US West, clients in Europe saw about 160 ms less latency per transaction (measurements, 2013, Section V).

## Properties

- Snapshot isolation for any clock skew (a theorem); the skew affects only the waits.
- No central timestamp server, so no single point of failure for timestamps and no extra round trips.
- Read-only transactions never abort and take no locks, but they can wait.
- The commit order can differ from real time for independent transactions on different partitions whose commit timestamps are closer than the clock precision (Section III-D). Clock-SI does not give [external consistency](/external-consistency/).
- Not serializable: [write skew](/write-skew/) is possible, as with any snapshot isolation.
- Distributed commits use two-phase commit and keep its blocking when a coordinator fails.

## Variants and improvements

- Older snapshots: choose $\Delta$ per transaction. $\Delta = 0$ gives the freshest data; the paper suggests the larger of the commit time plus a round trip and the clock skew minus the one-way delay, to make waits rare (Section III-C).
- Session consistency: a client keeps the last snapshot or commit timestamp it saw and sends it with the next transaction; the originating partition waits until its clock passes this value (Section III-E).
- In line L3 the paper does not wait for a prepared transaction whose commit timestamp, once known, is above the snapshot; the reader can ask the coordinator for it. The toy waits for every prepared writer with a prepare timestamp below the snapshot, which is simpler and still correct.
- Systems with tight clock bounds, such as [TrueTime](/truetime/), make a commit wait out the uncertainty and get external consistency; [hybrid logical clocks](/hybrid-logical-clocks/) mix physical time with a logical counter.

## When to use it

Use Clock-SI when data is partitioned, snapshot isolation is enough, and a central timestamp server would be a bottleneck or a long way off, as in a store spread over several data centers. It helps most for short transactions, where the round trips to a timestamp server are a large part of the latency. Do not use it if transactions must see each other in real-time order across partitions, or if write skew is not acceptable.

## Pitfalls

- The code on this page is a toy. One process simulates the partitions in ticks, clocks are tick counts plus a fixed skew, and the log is a delay; there is no disk, no network and no clock synchronization protocol.
- Every request that reaches a partition from another partition must wait for the clock, not only reads. If PREPARE does not wait, a prepare timestamp can be below the snapshot of its own transaction.
- The commit timestamp must be the largest prepare timestamp. The tests break with the smallest.
- A participant must make a prepared write visible as "pending" to readers, or line L3 cannot see it. The paper does this with a version that no reader may read until the commit finishes.
- Large clock skew does not break correctness, but reads at a partition with a slow clock wait longer.
- A clock that goes back, for example after a bad NTP step, breaks the proof. The model assumes clocks only move forward.

## Implementations

## History

Earlier partitioned SI systems got timestamps from a central authority. Du, Elnikety and Zwaenepoel built on work that orders events with physical clocks and showed at SRDS 2013 how to read a consistent snapshot from loosely synchronized clocks, with an analytical model of the waits and aborts that older snapshots cause, checked against their prototype.

## References
