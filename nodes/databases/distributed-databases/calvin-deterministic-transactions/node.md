---
tag: AX20CH
kind: algorithm
slug: calvin-deterministic-transactions
name: Calvin deterministic transaction protocol
aliases:
- Calvin
- deterministic database
area: databases/distributed-databases
level: research
summary: "Agree on a global order of transaction inputs first, then execute them deterministically at every replica, so no two-phase commit is needed."
solves: [concurrency-control]
model: asynchronous-model
complexity:
  vars: {p: the number of partitions that one transaction touches}
  messages: {worst: "p(p - 1)"}
  space: {extra: "O(p)"}
properties: {deterministic: true, recursive: false}
history:
  year: 2012
  people: [Alexander Thomson, Thaddeus Diamond, Shu-Chun Weng, Kun Ren, Philip Shao, Daniel J. Abadi]
  note: "Thomson, Diamond, Weng, Ren, Shao and Abadi presented Calvin at SIGMOD 2012. It builds on the deterministic database design of Thomson and Abadi at VLDB 2010."
prereqs: [conservative-two-phase-locking, state-machine-replication]
see_also: [two-phase-commit, paxos, total-order-broadcast, one-copy-serializability, shared-nothing-architecture, deadlock-prevention, percolator-transactions, ramp-transactions]
sources:
  - paper: doi:10.1145/2213836.2213838
    title: "Alexander Thomson, Thaddeus Diamond, Shu-Chun Weng, Kun Ren, Philip Shao and Daniel J. Abadi, Calvin, fast distributed transactions for partitioned database systems, SIGMOD 2012, pages 1 to 12"
    locator: "Section 2 (deterministic database systems), Section 3.1 (sequencer, 10 ms epochs and replication), Section 3.2 (the deterministic lock manager and the five phases of execution), Section 3.2.1 (OLLP), Section 5 (checkpointing) and Section 6.1 (TPC-C)"
---

Calvin is a transaction layer for a partitioned and replicated database. It first puts the inputs of all transactions in one global order and replicates this order, and only then executes the transactions. Every replica executes them so that the result is the same as running them one at a time in that order. Execution is deterministic, so two replicas that get the same input reach the same state without talking to each other. A node failure therefore does not force a transaction to abort, and Calvin needs no [two-phase commit](/two-phase-commit/) at the end of a distributed transaction. The cost is that each transaction must declare its read and write sets before it runs.

## In plain words

Several kitchens cook the same menu for the same list of orders. Each morning a clerk writes all the orders of the last few minutes in one numbered list and gives a copy to every kitchen. Each kitchen cooks the orders strictly in list order wherever two orders need the same pan, and in parallel where they do not. Since every kitchen follows the same list and the same recipes, all kitchens produce the same dishes. If one kitchen burns down, the others still have everything, and a new kitchen can catch up by cooking the list again from the start.

The kitchens never need to agree on anything at the end of a dish. All the agreement happened once, when the clerk wrote the list.

## The problem

A database is split into partitions on a cluster of [shared-nothing](/shared-nothing-architecture/) nodes, and each partition is replicated. Transactions can touch several partitions. The system must give [serializability](/serializability/) at each replica, keep the replicas consistent with each other ([one-copy serializability](/one-copy-serializability/)), and scale with the number of nodes.

The usual design runs [two-phase locking](/two-phase-locking/) and then [two-phase commit](/two-phase-commit/). A distributed transaction then holds its locks during several network round trips of the commit protocol, and this time, the *contention footprint*, limits the throughput on hot items. Two-phase commit exists because a node may fail or the transaction logic may decide to abort, and the nodes must agree on the outcome.

The model of the page is the [asynchronous model](/asynchronous-model/) inside a replica: messages take any time and are not lost while the replica is up. Nodes fail by stopping ([crash failure](/crash-failure/)). Agreement on the input is done by a consensus protocol such as [Paxos](/paxos/), which is outside the scope of the page.

## The algorithm

Calvin has three layers on every node: a sequencer, a scheduler with a lock manager and worker threads, and a storage engine with a simple read and write interface.

```pseudo id=main
CALVIN
▷ sequencer at partition p, for each epoch e (10 ms in Calvin)
L1  collect the transaction requests that clients send to p during epoch e into batch(e, p)
L2  replicate batch(e, p) (Paxos or a master replica), then send it to the scheduler of every partition in each replica
▷ scheduler at partition q, its lock thread
L3  wait until batch(e, p) has arrived from every sequencer p; the order of epoch e is batch(e, 1), batch(e, 2), ...
L4  for each transaction T in this global order: request all locks of T on the items of q, at once
L5  grant the locks on each item strictly in the order of the requests
▷ scheduler at partition q, a worker for T, when T holds all its locks at q
L6  read the items of the read set of T that are stored at q
L7  send these values to every active participant of T (a partition with an item of the write set of T)
L8  if q is not an active participant then release the locks of T at q and stop
L9  wait until the values from every partition of the read set of T have arrived
L10 run the logic of T on these values; every active participant computes the same writes or the same abort
L11 apply the writes to the items stored at q and release the locks of T at q
```

Lines L4 and L5 are a form of [conservative two-phase locking](/conservative-two-phase-locking/) with one extra rule: the locks are requested in the global order by one thread, and granted in request order. This makes the order of conflicting transactions equal to the global order at every partition and every replica. It also prevents deadlock, because a transaction waits only for transactions that come before it in the global order.

There is no commit protocol. A transaction that aborts because of its own logic, for example because a stock level would fall below zero, aborts at every active participant, because each of them runs the same logic on the same values. A transaction does not abort because a node fails: another replica has done the same work and has the same state.

**Dependent transactions and OLLP.** A transaction whose read or write set depends on data, such as an update through a secondary index, cannot declare its sets in advance. Calvin uses *optimistic lock location prediction* (OLLP). The client first runs a cheap reconnaissance query, with no locks and no replication, which reads the index and predicts the sets. It then sends the real transaction with these sets. At execution the transaction checks the index values again, and if they changed it restarts in the same deterministic way at every replica, and the client sends it again.

**The code on this page is a toy.** It runs all nodes in one thread, delivers messages in an order chosen by a seeded random generator, and gives the agreed input log to every replica in place of Paxos. It has no storage engine, no disk, no checkpoints and no worker threads. It keeps exactly the parts that make the protocol correct: epochs, the global order, the lock manager, the phases of lines L6 to L11, deterministic aborts, OLLP restarts and replay after a crash.

## Example

Item $a$ is on partition $P_0$ and item $b$ on $P_1$, with $a = 30$ and $b = 0$. In epoch 0, sequencer 0 gets $T_1$: "if $a \ge 10$, move 10 from $a$ to $b$, else abort", and sequencer 1 gets $T_2$: "set $a$ to $b$". The global order is $T_1, T_2$.

| step | where | what happens |
|---|---|---|
| 1 | L4 at $P_0$ | queue of $a$: $T_1$ (X), $T_2$ (X) |
| 2 | L4 at $P_1$ | queue of $b$: $T_1$ (X), $T_2$ (S) |
| 3 | L6, L7 | $T_1$ holds its locks at both partitions; $P_0$ sends $a = 30$ to $P_1$ and $P_1$ sends $b = 0$ to $P_0$ |
| 4 | L10, L11 | both partitions compute $a = 20$, $b = 10$, apply their own write and release |
| 5 | L6 to L8 at $P_1$ | $T_2$ gets its S lock on $b$, reads $b = 10$, sends it to $P_0$, and releases, since $P_1$ is not an active participant of $T_2$ |
| 6 | L9 to L11 at $P_0$ | $T_2$ gets its X lock on $a$ after $T_1$, waits for $b$, sets $a = 10$ |

The result $a = 10$, $b = 10$ is the result of $T_1$ and then $T_2$, and it is the same in every replica whatever the message delays. $T_1$ sends 2 messages and $T_2$ sends 1, and nobody sends a commit message. If $T_2$ had been first in the log, every replica would compute $a = 0$ and then abort $T_1$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It is a theorem in the model of the page, given that every replica gets the same input log.

1. Every scheduler sees the transactions in the same global order (line L3).
2. At each item the lock queue follows the global order, and a lock is granted only when all earlier conflicting locks are released (lines L4 and L5).
3. By induction on the global order, every transaction finishes: it waits only for earlier transactions, so there is no deadlock.
4. By the same induction, each read sees the value written by the last earlier writer of the item. So every transaction reads the serial values, decides the same way as in the serial execution, and writes the same values. The final state equals the state after a serial execution in log order.
5. Replicas apply the same log, so they reach the same state. A replica rebuilt by replaying the log reaches it too.

The tests check this against a brute force oracle that runs the transactions one at a time in log order. In 300 random runs with 3 to 6 transactions over 6 items on 3 partitions and 2 replicas, every replica has the oracle's final state and every transaction read the oracle's values; 88 of the 1342 transactions aborted by their logic. With a lock manager that grants every request, 273 of the 300 runs differ from the oracle, so the test is sensitive to the lock order. In 150 runs where one replica crashes, the other replica finishes without waiting, and the crashed replica, which was behind in 142 runs, reaches the same state after it replays the log.

## Complexity

For a transaction that touches $p$ partitions, phase 3 sends one message from each partition with reads to each other active participant, at most $p(p - 1)$ messages per replica, and there is no commit round (a theorem, in the proof). Each sequencer also sends one batch message per epoch to each scheduler. The latency of a transaction includes the wait for the end of its epoch and the replication of the batch.

The lock manager holds the locks of a transaction from line L4 until the transaction finishes at that partition, but a transaction holds no lock while the batch is replicated, so slow replication across data centers adds latency but not contention.

Thomson et al. measured Calvin on Amazon EC2 High-CPU Extra-Large instances (7 GB of memory, 8 virtual cores) with a TPC-C workload of New Order transactions only, 10 warehouses per partition and about 10% of transactions on two partitions. Calvin ran about 5000 transactions per second per node on clusters of more than 10 nodes, and nearly half a million transactions per second on 100 nodes (a measurement, 2012, Section 6.1). They also report that the throughput did not change when they replicated the input with Paxos across three data centers, while the latency grew (Section 3.1.1).

## Properties

- Serializable, and equivalent to the serial order of the log, at every replica (a theorem).
- Deterministic: the state of a replica depends only on the input log.
- No two-phase commit, no deadlock, and no abort because of a node failure.
- Logging is logical: only the input is logged, and recovery replays it from a checkpoint.
- Read and write sets must be known before execution; dependent transactions need OLLP.
- A slow node delays every later transaction that conflicts with its transactions, because nobody can skip ahead in the global order.

## Variants and improvements

- Replication of the input: asynchronous, with a master replica that forwards batches, or synchronous with Paxos among the replicas of a partition. The Calvin implementation used ZooKeeper for this.
- Disk-based storage: when a sequencer gets a transaction that may wait for the disk, it delays the transaction before it enters the scheduling layer and asks the storage to bring the records into memory, so that the transaction does not hold locks during a disk read (Section 4).
- Checkpointing: a naive mode that freezes one replica, an asynchronous variant of the Zig-Zag algorithm of Cao et al., and a snapshot mode when the storage keeps multiple versions (Section 5).

## When to use it

Calvin fits workloads with many short distributed transactions on hot items, where the time locks are held during two-phase commit limits throughput, and where read and write sets are known or cheap to predict. It fits less well when transactions are interactive, when the read set depends on many reads, or when latency must be below the epoch length plus the time to replicate a batch.

## Pitfalls

- The transaction logic must be deterministic. A call to a clock, a random number generator or an external service gives different results at different replicas.
- The order of epochs is the commit order, so a client sees a delay of at least one epoch (10 ms in Calvin) plus replication.
- An OLLP prediction that is often wrong causes repeated restarts. Calvin expects this to be rare because indexes on fields that change often are rare.
- Every replica must apply exactly the same log. A replica that misses or reorders one batch diverges silently.

## Implementations

## History

Thomson and Abadi argued in 2010 that a database that executes a given input in a fixed order can replace two-phase commit with replication of the input. Their earlier prototype used a single sequencer, which limited throughput and was a single point of failure. Calvin, presented at SIGMOD 2012 by Thomson, Diamond, Weng, Ren, Shao and Abadi, distributed the sequencer over all nodes with 10 ms epochs, added OLLP, disk support and checkpointing, and ran on a cluster of 100 commodity machines.

## References
