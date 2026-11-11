---
tag: PKTMQN
kind: algorithm
slug: tinystm
name: TinySTM
aliases:
- lazy snapshot algorithm
area: concurrency/transactional-memory
level: advanced
summary: Word-based STM of Felber, Fetzer and Riegel (2008). Write locks taken at the first write, a global clock, and snapshot extension (LSA), in write-back or write-through mode.
complexity:
  vars: {r: the number of words a transaction reads, w: the number of words it writes, e: the number of snapshot extensions, m: the number of data words}
  steps: {read: O(r), write: O(r), commit: O(r + w), total: O(r + w + e·r)}
  space: {shared: O(m), extra: Θ(r + w)}
properties: {deterministic: true, opaque: true, blocking: true, obstruction_free: false}
history:
  year: 2008
  people: [Pascal Felber, Christof Fetzer, Torvald Riegel]
  note: Felber, Fetzer and Riegel presented TinySTM at PPoPP 2008. It builds on the lazy snapshot algorithm (LSA) of Riegel, Felber and Fetzer, DISC 2006.
prereqs: [tl2, encounter-time-locking, eager-versioning, lazy-versioning]
see_also: [opacity, global-version-clock, swisstm, norec, undo-log, redo-log, contention-management, lock-striping]
sources:
  - paper: doi:10.1145/1345206.1345241
    title: "Pascal Felber, Christof Fetzer and Torvald Riegel, Dynamic performance tuning of word-based software transactional memory, PPoPP 2008, pages 237-246"
    locator: the description of TinySTM (encounter-time locking, write-back and write-through, the lock array and clock) and the sections on hierarchical locking and dynamic tuning
  - paper: doi:10.1007/11864219_20
    title: "Torvald Riegel, Pascal Felber and Christof Fetzer, A lazy snapshot algorithm with eager validation, DISC 2006, LNCS 4167, pages 284-298"
    locator: the lazy snapshot algorithm (LSA) and its snapshot extension
  - paper: doi:10.1007/11864219_14
    title: "Dave Dice, Ori Shalev and Nir Shavit, Transactional Locking II, DISC 2006, LNCS 4167, pages 194-208"
    locator: Section 2.1, the commit-time locking design that TinySTM is compared with
  - book: isbn:9781608452354
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Morgan and Claypool, 2010
    locator: Chapter 4 (Software transactional memory), the sections on lock-based STM with a global clock
---

TinySTM is a word-based [software transactional memory](/software-transactional-memory/) of Pascal Felber, Christof Fetzer and Torvald Riegel (PPoPP 2008). Like [TL2](/tl2/), it keeps a [global version clock](/global-version-clock/) and an array of versioned locks, one per stripe of memory, and its reads are invisible and checked after each load. It differs from TL2 in two ways. First, it takes the write lock of a word at the first write to it ([encounter-time locking](/encounter-time-locking/)), so write-write conflicts show up at once. Second, when a read finds a word newer than its snapshot, it does not abort at once: it reads the clock again, validates its read set, and extends the snapshot if nothing it read has changed. This extension is the lazy snapshot algorithm (LSA) of Riegel, Felber and Fetzer (DISC 2006); the aliases "LSA" and "lazy snapshot algorithm" name that part. TinySTM runs in write-back mode (a redo log, [lazy versioning](/lazy-versioning/)) or in write-through mode (in-place writes with an undo log, [eager versioning](/eager-versioning/)), and it is [opaque](/opacity/) in both.

## In plain words

Each word has a lock with a version, and there is one shared clock. A transaction notes the clock when it starts. When it first writes a word, it locks the word at once; if another transaction holds the lock, there is a conflict and one of them gives up. When it reads a word, it checks that the word is not locked by someone else and not newer than its noted clock. If the word is newer, the transaction does not give up yet: it reads the clock again and checks that everything it has read so far is still unchanged. If so, it moves its noted clock forward and goes on. At commit, it moves the clock forward, checks its reads once more if needed, and frees its locks with the new clock value as the version.

## The problem

Give $n$ processes [transactions](/transaction/) on a memory of $m$ words: begin, read$(a)$, write$(a, v)$ and commit, where any operation may abort. The safety condition is [opacity](/opacity/). The design goals of TinySTM are a small, fast word-based STM for C and C++, fewer wasted aborts than TL2 for long readers, early detection of write-write conflicts, and a few parameters that can be tuned to the workload.

### Model and notation

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $p, q$ | process names |
| $m$ | the number of data words |
| $r, w$ | the number of words that one transaction reads and writes |
| $e$ | the number of snapshot extensions of one transaction |
| CLOCK | the global clock, one shared word |
| lock$(a)$ | the versioned lock of the stripe of word $a$: a pair (version, owner) |
| $ub$ | the upper bound of the snapshot: the clock value up to which the reads are known to be consistent |
| $wv$ | the write version that a committer draws from the clock |

The processes are asynchronous and may crash. They share words with atomic read, write, [compare-and-swap](/compare-and-swap/) (CAS) and [fetch-and-add](/fetch-and-add/) (FAA), under [sequential consistency](/sequential-consistency/). Words map to locks by a hash of the address, which is [lock striping](/lock-striping/).

## The algorithm

```pseudo id=main
BEGIN()
L1  ub ← CLOCK; R ← ∅; W ← ∅; undo ← ∅; held ← ∅

READ(a)
L2  if I own lock(a) then return W[a] if a ∈ W (write-back), else the word a
L3  l1 ← lock(a); v ← a; l2 ← lock(a)
L4  if l1 is owned or l1 ≠ l2 then ABORT
L5  if l1.version > ub then
L6      if not EXTEND() then ABORT
L7      go to L3
L8  R[stripe of a] ← l1.version; return v

WRITE(a, v)
L9  if I do not own lock(a) then l ← lock(a); if l is owned then ABORT
L10     if not CAS(lock(a), l, (l.version, me)) then ABORT; held ← held ∪ {(stripe, l.version)}; if l.version > ub and not EXTEND() then ABORT
L11 write-back: W[a] ← v.  write-through: append (a, old value of a) to undo; a ← v

EXTEND()
L12 now ← CLOCK
L13 for each (s, ver) in R: unless lock(s) = (ver, FREE) or I took s at version ver, return false
L14 ub ← now; return true

COMMIT()
L15 if held = ∅ then return COMMITTED          ▷ read-only
L16 wv ← FAA(CLOCK, 1) + 1
L17 if ub ≠ wv − 1 and the check of L13 fails then ABORT
L18 write-back: for each (a, v) in W: a ← v
L19 for each held stripe s: lock(s) ← (wv, FREE); return COMMITTED

ABORT
L20 write-back: release each held lock with its old version. write-through: undo in reverse order, nv ← FAA(CLOCK, 1) + 1, release each held lock with (nv, FREE)
```

**Encounter-time locks (L9, L10).** The first write to a stripe takes its lock with a CAS that keeps the version. A transaction that finds the lock owned by another aborts (the default policy of the paper is to abort the transaction that finds the conflict; other [contention managers](/contention-management/) can wait or back off). A transaction that takes a lock whose version is newer than $ub$ must extend first, because later reads of that stripe come straight from memory.

**Reads and the snapshot extension (L3 to L8, L12 to L14).** A read samples the lock, loads the word, and samples the lock again, as in TL2. Unlike TL2, the read set keeps the version seen for each stripe. When the version is newer than $ub$, the transaction reads the clock, checks that every stripe it has read still has the same version and is not locked by someone else, and then moves $ub$ to the new clock value. If any stripe changed, the snapshot cannot be extended and the transaction aborts. Read-only transactions that run next to writers on other data therefore commit, where TL2 would abort them.

**Commit (L15 to L19).** A read-only transaction commits with no further step. An update transaction draws $wv$ from the clock, validates its read set unless no other commit happened since $ub$ ($ub = wv - 1$), writes back its redo log in write-back mode, and releases its locks with version $wv$.

**Write-through and the abort version (L11, L20).** In write-through mode, a write goes to memory at once, and the old value goes to an undo log. A reader cannot use the new value, since the lock is owned. On abort, the undo log restores the old values in reverse order. The locks must then be released with a new version drawn from the clock, not with their old version. Otherwise a reader that sampled the lock before the in-place write and again after the undo sees two equal samples and keeps the dirty value it loaded in between.

## Example

**Snapshot extension.** Two accounts start with $a_0 = a_1 = 10$. Process $q$ runs an audit that returns $a_0 + a_1$. Process $p$ runs a transaction that sets $a_1 = 15$. The run is the one in `test_worked_example_snapshot_extension`.

| Step | Process | Lines | Effect | CLOCK | lock$(a_0)$ | lock$(a_1)$ | $ub$ of $q$ |
|---|---|---|---|---|---|---|---|
| 1 | $q$ | L1 | $ub = 0$ | 0 | (0, free) | (0, free) | 0 |
| 2 | $q$ | L3 to L8 | reads $a_0 = 10$, version 0; R = $\{a_0 \mapsto 0\}$ | 0 | (0, free) | (0, free) | 0 |
| 3 | $p$ | L1, L9, L10 | locks $a_1$ at its write | 0 | (0, free) | (0, $p$) | 0 |
| 4 | $p$ | L16 | $wv = 1 = ub + 1$: no validation | 1 | (0, free) | (0, $p$) | 0 |
| 5 | $p$ | L18, L19 | $a_1 \leftarrow 15$; release with version 1 | 1 | (0, free) | (1, free) | 0 |
| 6 | $q$ | L3 to L5 | reads $a_1$: version $1 > ub = 0$ | 1 | (0, free) | (1, free) | 0 |
| 7 | $q$ | L12 to L14 | now $= 1$; $a_0$ still has version 0: $ub = 1$ | 1 | (0, free) | (1, free) | 1 |
| 8 | $q$ | L7, L3 to L8 | reads $a_1 = 15$ again; commits with sum 25 | 1 | (0, free) | (1, free) | 1 |

The audit commits with no abort; its serial position is after $p$. With the TL2 rule (abort when the version is newer than $ub$), the same run has one abort; the test checks both counts.

**Write-through abort.** With $x = 0$, a reader samples lock$(x) = (0, \text{free})$. A write-through transaction locks $x$, writes $x = 99$ in place, and then aborts. The reader loads $x = 99$ between these steps. The undo puts $x = 0$ back. If the lock is released as (0, free), the reader's second sample equals the first, and the reader commits the value 99, which no committed transaction wrote. With the release at a new version (1, free), the second sample differs, the reader aborts, and its retry reads 0. The test `test_write_through_abort_must_release_with_a_new_version` runs both versions and also finds the bad run by exhaustive search.

## Correctness

The full proof is in [the correctness proof](proofs/correctness). It has the same shape as the proof for TL2. The serial order puts each committed update transaction at its $wv$ and each other transaction just after the commits with $wv \le ub$, using its final $ub$. The main invariant is that, between operations, everything a transaction has read agrees with the state after all commits with $wv \le ub$. A read keeps it by the two lock samples; an extension keeps it because the validation shows that no stripe in the read set was written by a commit with a version in the gap; and a lock taken at a version newer than $ub$ forces an extension. The write-through case needs one extra fact: each release of a lock either keeps the data and the version unchanged (a write-back abort), or writes a version drawn from the clock while the lock was held, so it is larger than every earlier version of that lock.

Progress: no transaction waits for a lock in the default policy, so there is no [deadlock](/deadlock/), but there can be [livelock](/livelock/). A transaction that stops while it owns locks blocks the readers and writers of those stripes, so TinySTM is not [obstruction-free](/obstruction-freedom/).

## Complexity

Count shared memory steps. A read takes 3 steps plus, for each extension, 1 clock read and at most $r$ lock reads. A write takes 2 steps (read and CAS) at the first write to a stripe and none later; write-through adds one load and one store. A commit takes 1 FAA, at most $r$ lock reads, $w$ stores in write-back mode, and one release per lock: $O(r + w)$. A transaction that does not abort and extends $e$ times costs $O(r + w + e \cdot r)$ steps. Without extensions this is the $\Theta(r + w)$ of TL2; in the worst case each read extends, and the cost grows to $\Theta(r^2)$, the cost of incremental [validation](/transaction-validation/).

Space: one clock word and one lock word per stripe. The paper uses a fixed array of locks, with the number of locks as a parameter. Each transaction keeps $\Theta(r + w)$ private words.

## Properties

- **Opaque** in both modes, by the proof.
- **Encounter-time locking**: write-write conflicts are found at the write, before more work is wasted. Read-write conflicts are found at a read (an owned lock or a newer version that cannot be extended) or at commit.
- **Write-back or write-through**: write-back makes aborts cheap and commits more expensive; write-through makes commits cheap and aborts more expensive, and it lets a transaction read its own writes from memory with no lookup.
- **Blocking**: deadlock-free under abort-on-conflict, not obstruction-free, and it can livelock.
- **Not privatization safe** in the basic form, like TL2; see [privatization safety](/privatization-safety/).

## Variants and improvements

- **Tuning.** The paper tunes three parameters at run time: the number of locks in the array, the number of low address bits that are ignored when a word is mapped to a lock (so that neighboring words share a lock), and the size of a second array of counters for hierarchical locking, which lets a validation skip whole groups of locks that did not change. A tuning loop tries a configuration, measures throughput, and moves to a better one. The code on this page fixes the map from words to locks and does not model these parameters.
- **SwissTM** keeps encounter-time detection only for write-write conflicts and detects read-write conflicts at commit, with a two-phase contention manager; see [SwissTM](/swisstm/).
- **Commit-time locking.** TL2 takes its locks at commit and aborts instead of extending; see [commit-time locking](/commit-time-locking/).
- **Multi-version LSA.** The original LSA paper also keeps old versions so that a read-only transaction can read an older version instead of aborting; see [multi-version STM](/multi-version-stm/).

## When to use it

TinySTM fits word-based STM in C or C++ with transactions of medium length, where early detection of write conflicts and snapshot extension save work. Write-back mode is the safer default when aborts are frequent; write-through mode pays off when aborts are rare and transactions often read their own writes. Like TL2, it relies on a shared clock that every update transaction increments, which becomes a bottleneck at high commit rates.

## Pitfalls

- **Releasing a write-through abort with the old version.** This brings back the ABA problem on the lock word, and a reader can commit a value that was never committed. The test shows the run.
- **Reading a newly locked stripe without an extension.** If a transaction takes a lock whose version is newer than $ub$ and then reads other words of that stripe from memory, it can mix two snapshots. The code extends at L10 for this reason.
- **Validating only versions, not owners.** A stripe that another transaction owns has an unchanged version but may hold dirty data in write-through mode. VALIDATE must fail on an owned lock (unless the owner is the transaction itself).
- **Too few locks.** With a small lock array, unrelated words share locks, and false conflicts abort transactions; see [transaction conflict](/transaction-conflict/).
- **Holding locks for a long time.** Encounter-time locks are held from the first write until commit, so a long transaction blocks others longer than under commit-time locking.

## Implementations

## History

Riegel, Felber and Fetzer presented the lazy snapshot algorithm at DISC 2006, in the same volume as TL2. LSA introduced the idea of extending the validity range of a snapshot with a global time base instead of aborting. Felber, Fetzer and Riegel built TinySTM on LSA with encounter-time locking and presented it at PPoPP 2008, together with the dynamic tuning of the lock array. TinySTM became a common baseline in STM research and was later extended with other contention managers and with support for hybrid TM.

## References
