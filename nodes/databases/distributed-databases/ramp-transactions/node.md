---
tag: 1YZCSM
kind: algorithm
slug: ramp-transactions
name: RAMP transactions
aliases:
- read atomic multi-partition transactions
- read atomic isolation
area: databases/distributed-databases
level: research
summary: "Read atomic transactions over partitioned data: a reader sees all or none of the writes of each transaction, never waits for other clients, and needs at most two round trips."
solves: [concurrency-control]
model: asynchronous-model
complexity:
  vars: {k: the number of items that one transaction reads or writes}
  messages: {best: "2k", worst: "4k"}
  space: {extra: "O(k)"}
properties: {deterministic: true, recursive: false}
history:
  year: 2014
  people: [Peter Bailis, Alan Fekete, Ali Ghodsi, Joseph M. Hellerstein, Ion Stoica]
  note: "Bailis, Fekete, Ghodsi, Hellerstein and Stoica defined read atomic isolation and gave the RAMP-Fast, RAMP-Small and RAMP-Hybrid algorithms at SIGMOD 2014."
prereqs: [isolation-levels, multiversion-concurrency-control]
see_also: [highly-available-transactions, invariant-confluence, snapshot-isolation, two-phase-commit, percolator-transactions, clock-si, sharding, bloom-filter]
sources:
  - paper: doi:10.1145/2588555.2588562
    title: "Peter Bailis, Alan Fekete, Ali Ghodsi, Joseph M. Hellerstein and Ion Stoica, Scalable atomic visibility with RAMP transactions, SIGMOD 2014, pages 27 to 38"
    locator: "Section 3.1 (fractured reads and read atomic isolation), Section 3.3 (synchronization and partition independence), Algorithms 1 to 3 and Table 1 in Section 4, Section 5.4 (scale out), and the Appendix (Claims 1 to 6 and Invariant 1)"
---

RAMP transactions (read atomic multi-partition transactions) let a client write several items on different partitions so that other clients see either all of the new versions or none of them. This property is *read atomic isolation*. A writer first places its new versions on the partitions and only then marks them as committed. A reader first reads the last committed version of each item, and each version carries metadata about the other items that its transaction wrote. If the metadata shows that the reader got a version of one item but an older version of a sibling item, the reader fetches the missing version in a second round. No client ever waits for another client, and a crashed writer does not block anybody.

## In plain words

Two users become friends. The application stores the friendship twice, once in the list of each user, and the two lists are on different servers. Another user must never see that Sam is a friend of Mary while Mary is not yet a friend of Sam.

With RAMP, the writer first puts the two new list entries on their servers, marked as not yet visible. When both servers have them, it tells both servers to make them visible. A reader may arrive when one server has made its entry visible and the other has not. The visible entry says "I was written together with an entry of the other list, at time 1", so the reader asks the other server for that exact entry. The server has it already, because the writer put it there before it made anything visible, so the server answers at once.

## The problem

A database is split into partitions, and each item has one copy on one partition. Clients run two kinds of transactions: a write transaction PUT_ALL$(W)$ that writes a set $W$ of items, and a read transaction GET_ALL$(I)$ that reads a set $I$ of items. The model is the [asynchronous model](/asynchronous-model/): messages take any time and are not lost, and a client can fail by stopping ([crash failure](/crash-failure/)).

A read transaction has a *fractured read* if a transaction $T$ wrote versions of $x$ and $y$, and the reader got the version of $x$ from $T$ but a version of $y$ older than the version from $T$. A system gives *read atomic isolation* (RA) if no transaction has a fractured read and no transaction reads data that is not committed, aborted or intermediate.

The system must give RA with two scalability conditions. *Synchronization independence*: a transaction of one client never waits for a transaction of another client, so each client can always finish. *Partition independence*: a transaction contacts only the partitions of its own items.

RA is weaker than [snapshot isolation](/snapshot-isolation/) and [serializability](/serializability/). Two transactions can write the same item at the same time, and nothing stops another writer between a read of an item and a write of it. RA is the right level for writes that must be seen together, such as both halves of a two-way relation, an item and its entry in a secondary index, or a base table and a materialized view.

## The algorithm

Each write transaction gets a unique timestamp, made from a client id and a sequence number of the client; no central server is needed. Each partition keeps all the versions it has received, and for each item the timestamp $\mathrm{lastCommit}[x]$ of the newest committed version. This is a small form of [multiversion concurrency control](/multiversion-concurrency-control/). RAMP-Fast (RAMP-F) stores with each version the set of the other items of its transaction.

```pseudo id=main
RAMP-FAST
▷ client: PUT_ALL(W), W is a set of (item, value)
L1  ts ← a new unique timestamp (sequence number, client id)
L2  for each (x, v) in W, in parallel: send PREPARE(x, v, ts, md = the other items of W) to the partition of x
L3  wait until every partition has answered PREPARED
L4  for each x in W, in parallel: send COMMIT(x, ts) to the partition of x
▷ client: GET_ALL(I), I is a set of items
L5  for each x in I, in parallel: ret[x] ← GET(x, none) from the partition of x
L6  for each y in I: v_latest[y] ← the largest ret[x].ts over the x in I with y in ret[x].md (⊥ if none)
L7  for each x in I with v_latest[x] > ret[x].ts, in parallel: ret[x] ← GET(x, v_latest[x])
L8  return the values of ret
▷ partition
L9  on PREPARE(x, v, ts, md): add the version (x, v, ts, md) to versions; answer PREPARED
L10 on COMMIT(x, ts): lastCommit[x] ← max(lastCommit[x], ts); answer COMMITTED
L11 on GET(x, ts_req): if ts_req is none, answer the version of x with timestamp lastCommit[x], else the version of x with timestamp ts_req
```

The key fact is that a partition makes a version visible (line L10) only after every partition of the transaction has the version (lines L3 and L9). So when a reader learns about a sibling version from metadata, the version is already on its partition, and the GET of line L7 returns it at once. The reader never asks for a version that is not there and never waits.

**RAMP-Small (RAMP-S)** stores no item sets, only the timestamp. The reader always does two rounds. In the first round it gets the timestamp $\mathrm{lastCommit}[x]$ of each item. In the second round it sends the whole set $S$ of these timestamps to each partition, and the partition returns the version of $x$ with the largest timestamp in $S$ that it has for $x$. Writes are the same as in RAMP-F.

**RAMP-Hybrid (RAMP-H)** stores a [Bloom filter](/bloom-filter/) of the items of the transaction in place of the set. A reader asks in the second round for each item that the filter of a newer version may contain. A false positive asks for a version that does not exist, and the partition answers "none". With no false positives RAMP-H reads act like RAMP-F reads; with all false positives they act like RAMP-S reads.

## Example

The test file builds this case. Items $x$ and $y$ are on partitions $P_0$ and $P_1$. Transaction $T_1$ with timestamp 1 writes $x = 11$ and $y = 12$. Both PREPARE messages have arrived (line L9), so both partitions have the versions. The COMMIT has reached $P_0$, so $\mathrm{lastCommit}[x] = 1$, but it has not reached $P_1$, where $\mathrm{lastCommit}[y] = \bot$. Then a client reads $x$ and $y$.

| step | line | what happens |
|---|---|---|
| 1 | L5 | $P_0$ returns $x = 11$, timestamp 1, metadata $\{y\}$; $P_1$ returns $y = 0$, timestamp $\bot$, no metadata |
| 2 | L6 | $v_{\mathrm{latest}}[y] = 1$, from the metadata of $x$; $v_{\mathrm{latest}}[x] = \bot$ |
| 3 | L7 | $1 > \bot$, so the reader sends GET$(y, 1)$ to $P_1$ |
| 4 | L11 | $P_1$ has the prepared version of $y$ with timestamp 1 and returns $y = 12$ |
| 5 | L8 | the reader returns $x = 11$, $y = 12$ |

The read takes 2 round trips and 6 messages, and $\mathrm{lastCommit}[y]$ at $P_1$ is still $\bot$ at the end. A reader that stops after one round returns $x = 11$, $y = 0$, which is a fractured read. RAMP-S also returns $x = 11$, $y = 12$: the set $S$ is $\{1, \bot\}$, and $P_1$ has a version of $y$ at timestamp 1.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It follows the Appendix of Bailis et al. (2014) and is a theorem in the model of the page. The main steps are these.

1. If a partition ever sets $\mathrm{lastCommit}[x] = t$, then every version of the transaction with timestamp $t$ is on its partition. This holds because COMMIT is sent only after all PREPARED answers.
2. For RAMP-F, let the read return the timestamp $f[x] = \max(\mathrm{ret}[x].ts, v_{\mathrm{latest}}[x])$ for each $x$. If $T$ wrote $x$ at $f[x] = t$ and also wrote $y \in I$, then $t$ came from a first round version of some item of $T$, whose metadata names $y$ (or which is $y$ itself), so $f[y] \ge t$. That is exactly the absence of fractured reads.
3. Every timestamp returned is a value of $\mathrm{lastCommit}$ or a sibling of one, so the transaction is committed. A writer that crashed before line L3 is never visible.
4. For RAMP-S, the set $S$ contains $t$, and by step 1 the partition of $y$ has a version at $t$, so it returns a timestamp of at least $t$ for $y$.
5. Each GET finds its version at once by step 1, so no partition and no client waits for another client.

The tests check read atomicity in a simulation where messages arrive in a random order from a seeded generator. Each run has 2 to 4 write transactions of 2 or 3 items and 2 to 4 read transactions of 2 to 4 items, over 4 items on 3 partitions, and in half of the tests one writer crashes at a random step. Over 200 seeds per test (608 reads), RAMP-F and RAMP-S give no fractured read and no read of an uncommitted version, and every reader finishes in at most 2 rounds. The one round reader of the same runs has a fractured read in 90 of 200 runs without crashes and 77 of 200 with crashes (a measurement of this simulation).

## Complexity

Let $k$ be the number of items of a transaction, each on a different partition. In round trips and messages (a theorem, part 3 of the proof):

| | write | read, best | read, worst | metadata per version |
|---|---|---|---|---|
| RAMP-F | 2 round trips, $4k$ messages | 1, $2k$ | 2, $4k$ | the other $k - 1$ items |
| RAMP-S | 2, $4k$ | 2, $4k$ | 2, $4k$ | none |
| RAMP-H | 2, $4k$ | 1, $2k$ | 2, $4k$ | a Bloom filter |

The paper sends one COMMIT per partition, not per item, so a write touches each partition twice. A RAMP-F read needs the second round only when it overlaps a write that has committed at some of its partitions and not yet at others. In the test runs, 128 of 608 RAMP-F reads needed a second round, and 105 of 608 in the runs with crashes; all 608 RAMP-S reads took two rounds (a measurement of this simulation, not of a real system). A RAMP-S second round GET carries the set $S$, so its size grows with $k$.

Partitions keep old versions until no reader can ask for them, so the space is more than one version per item while writes are in progress. The metadata of RAMP-F is $O(k)$ items per version.

Bailis et al. measured RAMP on Amazon EC2 cr1.8xlarge instances with YCSB, 95% reads and transactions of 4 operations. The RAMP algorithms had a throughput typically within 8% of a baseline with no concurrency control and never more than 48% below it, and RAMP-F reached slightly under 7.1 million operations per second (1.79 million transactions per second) on 100 servers (a measurement, 2014, Sections 5.2 and 5.4).

## Properties

- RA isolation: no fractured reads, and no reads of data that is not committed (a theorem).
- Synchronization independence: no client waits for another client, and a slow or crashed writer does not block readers or other writers.
- Partition independence: a transaction contacts only the partitions of its items, and partitions never talk to each other.
- No central timestamp server: a timestamp only names a version and orders the versions of one item.
- Concurrent writers to the same item are not stopped. The version with the larger timestamp wins at each partition (line L10), as in [last writer wins](/last-writer-wins/).

## Variants and improvements

- RAMP-S and RAMP-H trade metadata size for read round trips, as in the table above.
- Faster commit detection: if a partition returns a version whose timestamp is above $\mathrm{lastCommit}$, the transaction has committed at some partition, so this partition can mark the version as committed (Section 4.7 of the paper).
- Cooperative termination: a client that crashes after some COMMIT messages leaves versions committed at some partitions and not at others. A partition that times out asks the other partitions of the transaction, and commits if one of them has committed (Section 4.6). This always finishes the transaction except when every partition has prepared and none has committed.
- Garbage collection: a partition can remove an overwritten version when no reader will ask for it again. The simple rule is to limit the time a read can take and remove versions after a fixed window, 5 seconds in the experiments of the paper; a slower read is restarted (Sections 4.5 and 5.1).
- Read-write transactions: a transaction that declares its read set first runs GET_ALL, buffers its writes and sends them with one PUT_ALL at the end. This is still RA, but it can lose concurrent updates (Section 4.5).
- Replication: each partition can be replicated with any protocol that keeps operations on one item [linearizable](/linearizability/) (Section 3.3).

## When to use it

Use RAMP when writes to several partitions must become visible together and transactions do not need to stop concurrent updates of the same item. Typical cases are both directions of a relation, a row and its secondary index entries, and materialized views. Do not use RAMP when a transaction must check a condition and then write, such as "withdraw only if the balance stays positive"; RA allows two withdrawals to run at the same time. Such cases need [serializability](/serializability/) or a check that the invariant survives merges ([invariant confluence](/invariant-confluence/)).

## Pitfalls

- RA is not snapshot isolation. It does not order transactions against each other, and a read-write transaction built from GET_ALL and PUT_ALL can lose an update.
- The timestamps must be unique across clients. Two writers with the same timestamp would mix their versions, and RAMP-H would return wrong versions for false positives.
- If the commit of a crashed client is not finished by a termination protocol, its versions stay visible at some partitions and invisible at others. Readers stay correct, because they fetch the missing siblings, but they pay the second round forever.
- The proofs need every version that a reader can learn about to stay on its partition until the reader asks. Garbage collection that is too fast breaks this.
- A one round reader that just reads the last committed versions is not RA. The example above shows the fractured read.

## Implementations

## History

Bailis, Fekete, Ghodsi, Hellerstein and Stoica introduced RA isolation and RAMP transactions at SIGMOD 2014. They wanted multi-partition updates for systems such as Facebook TAO, LinkedIn Espresso and Yahoo PNUTS, which often gave up transactions across partitions because locking and two-phase commit block under failures and contention. The paper compares RA with the isolation levels of Adya: it is stronger than read committed and weaker than snapshot isolation. RA allows concurrent updates and so stays within what [highly available transactions](/highly-available-transactions/) can give, which the same group studied in earlier work.

## References
