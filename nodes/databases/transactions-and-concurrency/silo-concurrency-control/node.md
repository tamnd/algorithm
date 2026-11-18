---
tag: 023YX3
kind: algorithm
slug: silo-concurrency-control
name: Silo epoch-based OCC
aliases:
- Silo
- Silo commit protocol
area: databases/transactions-and-concurrency
level: research
summary: "An optimistic commit protocol for multicore in-memory databases: lock the write set, read a global epoch, validate the read set by TIDs, then install. Reads never write shared memory."
solves: [concurrency-control]
model: word-ram
complexity:
  vars: {r: the size of the read set, w: the size of the write set}
  time: {worst: O(r + w log w)}
  space: {extra: O(r + w)}
properties: {deterministic: true}
history:
  year: 2013
  people: [Stephen Tu, Wenting Zheng, Eddie Kohler, Barbara Liskov, Samuel Madden]
  note: "SOSP 2013. Silo reached almost 700,000 TPC-C transactions per second on a 32-core machine."
prereqs: [optimistic-concurrency-control, conflict-serializability]
see_also: [tl2, software-transactional-memory, transaction-validation, read-set-and-write-set, global-version-clock, epoch-based-reclamation, strict-two-phase-locking, b-plus-tree]
sources:
  - paper: doi:10.1145/2517349.2522713
    title: "Stephen Tu, Wenting Zheng, Eddie Kohler, Barbara Liskov and Samuel Madden, Speedy transactions in multicore in-memory databases, Proceedings of the 24th ACM SOSP, 2013, pages 18 to 32"
    locator: "Section 4.1 (epochs, updated every 40 ms), Section 4.2 (TIDs and the rule for choosing one), Section 4.4 and Figure 2 (the commit protocol and its serializability argument), Section 5.1 (the machine) and Figures 5 and 6 (TPC-C throughput)"
  - paper: doi:10.1145/319566.319567
    title: "H. T. Kung and John T. Robinson, On optimistic methods for concurrency control, ACM Transactions on Database Systems 6(2), 1981, pages 213 to 226"
    locator: "the read, validation and write phases that Silo refines, chapter level only"
  - paper: "Yandong Mao, Eddie Kohler and Robert Morris, Cache craftiness for fast multicore key-value storage, Proceedings of EuroSys 2012"
    locator: "the Masstree index that Silo builds on, chapter level only"
  - paper: doi:10.1145/2882903.2882935
    title: "Xiangyao Yu, Andrew Pavlo, Daniel Sanchez and Srinivas Devadas, TicToc, time traveling optimistic concurrency control, Proceedings of ACM SIGMOD 2016, pages 1629 to 1642"
    locator: "a later OCC protocol that computes commit timestamps from data, chapter level only"
  - paper: "Wenting Zheng, Stephen Tu, Eddie Kohler and Barbara Liskov, Fast databases with fast durability and recovery through multicore parallelism, Proceedings of USENIX OSDI 2014, pages 465 to 477"
    locator: "SiloR, the logging, checkpoint and recovery design built on Silo, chapter level only"
---

*Silo* is an in-memory database for multicore machines by Tu, Zheng, Kohler, Liskov and Madden (2013), and its commit protocol is a form of [optimistic concurrency control](/optimistic-concurrency-control/). A transaction runs without locks and records the version (the *TID*) of each record it reads. At commit it locks the records it writes, reads a global *epoch* number, and then [validates](/transaction-validation/) that every record it read still has the same TID and is not locked by another transaction. If so, it picks a TID in the current epoch and installs its writes. There is no shared counter: TIDs are chosen by each worker from the TIDs it saw, and the only shared word, the epoch, changes every 40 ms. Reads never write shared memory. The design is close to [TL2](/tl2/) and other [software transactional memory](/software-transactional-memory/) systems, which also validate a read set against version numbers; Silo replaces the [global version clock](/global-version-clock/) of TL2 by the epoch and by local TID choice. The result is [conflict serializable](/conflict-serializability/). The code on this page is a toy, single-threaded model of the protocol and not Silo itself.

## In plain words

Many cores run transactions at the same time on data in memory. A shared counter for transaction numbers would make every core write the same memory word, and that alone limits speed. Silo avoids it. Each record carries a version stamp. A transaction remembers the stamps of what it read and keeps its writes private. To commit, it locks what it will write, looks once at a slowly moving clock (the epoch), and then checks that nothing it read has changed or is locked by someone else. If the check passes, it makes a new stamp a little larger than every stamp it saw, writes it with the new values, and unlocks. If the check fails, it aborts and runs again. The epoch groups transactions into time slices, which logging, recovery and memory cleanup use.

## The problem

Give serializable transactions on a database in main memory, on a machine with tens of cores, so that throughput grows with the number of cores. The obstacles are writes to shared memory: a central lock manager, a central counter for transaction numbers, or reader counts on records all move cache lines between cores. Silo wants a protocol in which a read-only access to a record does not write anything shared, and in which the only global state is written rarely.

## The algorithm

Each record has a *TID word*: the TID of the transaction that last wrote it, plus status bits, one of which is the lock bit. In Silo a TID is a 64-bit integer whose high bits hold the epoch in which the writer committed. A global epoch number $E$ is advanced by one designated thread, every 40 ms in the paper. Each worker $w$ keeps $last[w]$, the TID it chose last. $R(T)$ maps each record read to the TID seen at the read, and $W(T)$ maps each record written to its new value.

```pseudo id=main
READ(T, x)
L1  if x ∈ W(T) then return W(T)[x]
L2  read x.value and x.tid as one consistent pair; add (x, x.tid) to R(T); return x.value
WRITE(T, x, v)
L3  W(T)[x] ← v                                              ▷ private until Phase 3
COMMIT(T) on worker w
L4  for x in W(T), in one fixed global order do lock(x)      ▷ Phase 1
L5  e ← E                                                    ▷ the serialization point
L6  for (x, t) in R(T) do                                    ▷ Phase 2
L7      if x.tid ≠ t or (x is locked and x ∉ W(T)) then unlock W(T); abort T
L8  tid ← the smallest TID in epoch e that is larger than every TID in R(T), every x.tid for x ∈ W(T), and last[w]
L9  last[w] ← tid
L10 for x in W(T) do x.value ← W(T)[x]; x.tid ← tid; unlock(x)      ▷ Phase 3
ADVANCE-EPOCH()                                              ▷ one thread, every 40 ms
L11 E ← E + 1
```

**Phase 1** (line L4) locks the write set. The global order, the record addresses in Silo, prevents deadlock. **The serialization point** is line L5: Silo uses memory fences so that this read of $E$ comes after all the locks and before all the checks. **Phase 2** (lines L6 and L7) aborts if a record read has a new TID or is locked by another transaction; a record locked by another may be about to change. In Silo the check also tests a *latest-version* bit for records that were replaced, and checks the version numbers of index nodes to catch phantoms in range scans. **The TID** of line L8 is larger than every TID the transaction saw. So the TIDs of one record grow, the TIDs of one worker grow, and a transaction that reads or overwrites the data of another gets a larger TID. TIDs do not follow anti-dependencies: if $T_1$ reads $x$ and $T_2$ later overwrites it, either TID may be larger. **Phase 3** (line L10) writes each record and releases its lock in one store, since the lock bit is in the TID word.

**Epochs.** TIDs of different epochs agree with the serial order, and committed transactions of an earlier epoch never depend on transactions of a later one. Silo uses this for durability: it logs by epoch and tells clients that a transaction is durable once its whole epoch is on disk. Epochs also drive the reclamation of old records, as in [epoch-based reclamation](/epoch-based-reclamation/), and the snapshots for read-only transactions.

## Example

Records $x$ and $y$ start at 0 with TID $(0, 0)$; a TID is written (epoch, sequence). $T_1$ on worker 1 runs $y \leftarrow x + 1$ and $T_2$ on worker 2 runs $x \leftarrow y + 1$. This is Figure 3 of the paper: in a serializable run both cannot read 0.

| step | action | line | $E$ | $x$ (value, TID, lock) | $y$ (value, TID, lock) |
|---|---|---|---|---|---|
| 1 | $T_1$ reads $x = 0$; $R(T_1) = \{x \mapsto (0,0)\}$ | L2 | 1 | 0, (0,0), free | 0, (0,0), free |
| 2 | $T_2$ reads $y = 0$; $R(T_2) = \{y \mapsto (0,0)\}$ | L2 | 1 | 0, (0,0), free | 0, (0,0), free |
| 3 | $T_1$ buffers $y = 1$, locks $y$ | L3, L4 | 1 | 0, (0,0), free | 0, (0,0), $T_1$ |
| 4 | $T_1$ reads $e = 1$ | L5 | 1 | | |
| 5 | $T_1$ checks $x$: same TID, not locked | L7 | 1 | | |
| 6 | $T_1$ picks $(1, 0)$ and installs $y$ | L8, L10 | 1 | 0, (0,0), free | 1, (1,0), free |
| 7 | the epoch advances | L11 | 2 | | |
| 8 | $T_2$ buffers $x = 1$, locks $x$, reads $e = 2$ | L3 to L5 | 2 | 0, (0,0), $T_2$ | 1, (1,0), free |
| 9 | $T_2$ checks $y$: TID $(1,0) \ne (0,0)$, abort, unlock $x$ | L7 | 2 | 0, (0,0), free | |
| 10 | $T_2$ runs again: reads $y = 1$ with TID $(1,0)$, buffers $x = 2$ | L2, L3 | 2 | | |
| 11 | locks $x$, reads $e = 2$, checks $y$, picks $(2, 0)$, installs | L4 to L10 | 2 | 2, (2,0), free | 1, (1,0), free |

The result $x = 2, y = 1$ is the serial order $T_1, T_2$. If instead $T_2$ had locked $x$ before $T_1$ checked $x$ in step 5, $T_1$ would find $x$ locked and abort. In the toy test of this case, $T_2$ then commits, and the history is $r_1(x)\, r_2(y)\, a_1\, w_2(x)\, c_2$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It is for the toy model, in which every step is atomic. Order the committed transactions by the time of line L5. For two conflicting operations, the one that comes first belongs to the transaction with the earlier serialization point. A write-write or write-read pair is ordered by the lock of the writer, which is held from before its serialization point until after its install. A read-write pair is ordered by Phase 2: if the writer had its serialization point first, it held the lock before the reader validated, so the reader saw either the lock or a new TID and aborted. So the committed projection is conflict equivalent to the serial order of the serialization points. The paper argues the same result by a reduction to [strict two-phase locking](/strict-two-phase-locking/): whenever validation succeeds, strict 2PL could have held a read lock on each record from the read to the commit. The proof also shows the TID rules: TIDs grow along every write-read and write-write dependency, along each worker and along each record, and epochs never go back along the serial order.

## Complexity

A commit sorts and locks the write set, checks each entry of the read set once, and installs each write once: $O(r + w \log w)$ steps, plus the time spent waiting for locks that others hold. Waiting is short, because a lock is held only during the commit of a transaction, never during its execution. The read set and the write set take $O(r + w)$ space. No step writes a shared word except the locks and installs of the records in $W(T)$, and the epoch update of one thread every 40 ms.

**Measurements.** These are results of the paper, not properties of the algorithm. On a machine with four 8-core Intel Xeon E7-4830 processors at 2.1 GHz (32 cores) and 256 GB of DRAM, running 64-bit Linux 3.2.0, Silo reached almost 700,000 transactions per second on the standard TPC-C mix on 32 cores, about 22,000 per core (SOSP 2013). The paper reports near-linear scaling with the number of cores on this benchmark.

## Properties

- **Serializable.** Committed transactions are equivalent to their order of serialization points.
- **Invisible reads.** A read changes nothing in shared memory, so readers of a hot record do not slow each other down.
- **No global counter.** The TID comes from local information; the epoch is the only global word, and it is written rarely.
- **Deadlock-free.** Locks are taken only at commit and in one global order.
- **Not opaque.** A running transaction can read an inconsistent state, because nothing is checked until commit. A transaction that will abort can see values that no serial run produces. Unlike [TL2](/tl2/), Silo does not check reads against a start time.
- **Aborts under contention.** A transaction aborts whenever a record it read was overwritten before its validation, even if a serial order exists.

## Variants and improvements

- **Snapshot transactions.** Silo keeps old versions for a while and lets read-only transactions read a consistent snapshot of a recent epoch, so they never abort.
- **Range scans.** The index (a variant of Masstree, a [B+ tree](/b-plus-tree/) and trie for multicore machines) gives each leaf a version number; the transaction validates the versions of the leaves it scanned, which detects inserts into a scanned range, the [phantom problem](/phantom-problem/).
- **Durability.** SiloR (Zheng, Tu, Kohler and Liskov, OSDI 2014) adds parallel logging, checkpoints and recovery around the epochs.
- **TicToc.** Yu, Pavlo, Sanchez and Devadas (2016) compute a commit timestamp for each transaction from the read and write timestamps of the records it touched, which commits some schedules that Silo aborts.
- **Transactional memory.** [TL2](/tl2/) uses a global version clock and validates at every read; [NOrec](/norec/) uses one global sequence lock and value-based validation. Silo is closer to TL2 with the clock replaced by the epoch.

## When to use it

Use a Silo-style protocol in a main-memory store on a multicore machine when transactions are short, mostly touch disjoint data, and are known in full when they start, such as stored procedures. It is a poor fit under high contention on a few hot records, where OCC aborts and retries waste work, and for long transactions that read much data, which are likely to fail validation; there, locking or a snapshot read for the long reader is better.

## Pitfalls

- **Reading the epoch too early.** Line L5 must come after line L4. If a transaction reads $E$ before it holds its locks, a later epoch can contain a transaction that it depends on, and the epoch order no longer agrees with the serial order. Silo puts memory fences around line L5; without them a compiler or CPU can move the read.
- **Not checking the lock bit.** Line L7 must abort on a record locked by another transaction even when its TID is unchanged. A version of line L7 that tests only $x.tid \ne t$ lets $T_1$ and $T_2$ of the example both commit with the values $x = 1, y = 1$, which no serial order gives.
- **Locks in arbitrary order.** Line L4 must take the locks in one global order. Taking them in program order can deadlock two committing transactions that write the same two records.
- **A TID that ignores the write set.** Line L8 must exceed $x.tid$ for each $x \in W(T)$, not only the TIDs in $R(T)$. A blind write can otherwise get a TID smaller than the version it overwrites, and the TIDs of the record stop growing.

## Implementations

## History

Kung and Robinson introduced optimistic concurrency control in 1981. Work on software transactional memory in the 2000s, in particular TL2 (2006), made validation of a read set by version numbers fast. Stephen Tu, Wenting Zheng, Eddie Kohler, Barbara Liskov and Samuel Madden presented Silo at SOSP 2013; it took its index from Masstree (Mao, Kohler and Morris, 2012) and replaced the central transaction counter by epochs and local TIDs. SiloR added fast durability and recovery in 2014, and later in-memory OCC protocols such as TicToc (2016) were measured against Silo.

## References
