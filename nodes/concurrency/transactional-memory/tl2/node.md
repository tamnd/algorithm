---
tag: V7T1AZ
kind: algorithm
slug: tl2
name: TL2
aliases:
- Transactional Locking II
area: concurrency/transactional-memory
level: advanced
summary: Word-based STM of Dice, Shalev and Shavit (2006). A global version clock, versioned write locks taken at commit, a redo log and a check after each read make it opaque.
complexity:
  vars: {r: the number of words a transaction reads, w: the number of words it writes, m: the number of data words}
  steps: {read: Θ(1), write: Θ(1), commit: Θ(r + w)}
  space: {shared: O(m), extra: Θ(r + w)}
properties: {deterministic: true, opaque: true, blocking: true, obstruction_free: false, privatization_safe: false}
history:
  year: 2006
  people: [Dave Dice, Ori Shalev, Nir Shavit]
  note: Dice, Shalev and Shavit presented TL2 at DISC 2006. It added a global version clock to the earlier Transactional Locking (TL) design of Dice and Shavit.
prereqs: [global-version-clock, commit-time-locking, lazy-versioning, compare-and-swap, fetch-and-add]
see_also: [opacity, tinystm, swisstm, norec, transaction-validation, zombie-transactions, privatization-safety, contention-management]
sources:
  - paper: doi:10.1007/11864219_14
    title: "Dave Dice, Ori Shalev and Nir Shavit, Transactional Locking II, DISC 2006, LNCS 4167, pages 194-208"
    locator: Section 2.1 (the global version clock, the versioned write locks, the read and commit steps, the rv + 1 = wv case, read-only transactions) and Section 2.2 (low-level details)
  - paper: doi:10.1145/1345206.1345233
    title: "Rachid Guerraoui and Michał Kapałka, On the correctness of transactional memory, PPoPP 2008"
    locator: the definition of opacity, which the correctness proof uses
  - book: isbn:9781608452354
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Morgan and Claypool, 2010
    locator: Chapter 4 (Software transactional memory), the section on lock-based STM systems with a global clock
  - paper: "Yossi Lev, Victor Luchangco, Virendra J. Marathe, Mark Moir, Dan Nussbaum and Marek Olszewski, Anatomy of a scalable software transactional memory, TRANSACT 2009"
    locator: the discussion of the global clock schemes GV4, GV5 and GV6 of the TL2 code release
---

TL2 (Transactional Locking II) is a word-based [software transactional memory](/software-transactional-memory/) that Dave Dice, Ori Shalev and Nir Shavit presented at DISC 2006. It combines four parts: a [global version clock](/global-version-clock/); one versioned write lock per memory stripe, taken only at commit ([commit-time locking](/commit-time-locking/)); a private redo log for the writes ([lazy versioning](/lazy-versioning/)); and invisible reads that are checked against the clock after each load. The check after each read makes TL2 [opaque](/opacity/). Opacity means that all transactions, also the ones that abort, read values that agree with one serial order that respects real time. So a TL2 transaction never runs on an inconsistent state and cannot become a [zombie](/zombie-transactions/). A read costs a constant number of steps, and the commit checks each read once, so TL2 avoids the quadratic cost of incremental [validation](/transaction-validation/).

## In plain words

Each shared word has a small lock with a version number, and there is one shared clock. A transaction first notes the clock. When it reads a word, it checks that the lock of the word is free and that its version is not newer than the noted clock. A newer version means that someone changed the word after the transaction started, so the transaction gives up and starts again. Writes go into a private list and do not touch memory. At the end, the transaction locks the words it wants to write, moves the clock forward by one, checks that the words it read are still not newer than its start, copies its writes to memory, and frees the locks with the new clock value as their version. A transaction that only reads needs no locks and no final check.

## The problem

Give $n$ processes [transactions](/transaction/) on a memory of $m$ words: begin, read$(a)$, write$(a, v)$ and commit, where any operation can abort the transaction. The safety condition is [opacity](/opacity/) (Guerraoui and Kapałka 2008): each history, with its aborted and live transactions, is equivalent to one legal serial history that respects real-time order. A [transaction conflict](/transaction-conflict/) may abort a transaction, but the STM must not deadlock. TL2 does not promise that a given transaction ever commits, and it is a blocking design: a process that stops while it holds a lock blocks the transactions that need that stripe.

### Model and notation

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $p, q$ | process names |
| $m$ | the number of data words |
| $r, w$ | the number of words that one transaction reads and writes |
| GV | the global version clock, one shared word |
| lock$(a)$ | the versioned write lock of the stripe of word $a$: a pair (version, owner) |
| $rv$, $wv$ | the read version (GV at begin) and the write version (GV after the commit increment) of a transaction |

The processes are asynchronous and may crash between any two steps. They share words with atomic read, write, [compare-and-swap](/compare-and-swap/) (CAS) and [fetch-and-add](/fetch-and-add/) (FAA). CAS has [consensus number](/consensus-number/) $\infty$ and FAA has consensus number 2. The memory is [sequentially consistent](/sequential-consistency/). The paper maps each word to a lock with a hash of its address into a table of $2^{20}$ entries (the per-stripe mode) or puts the lock inside each object (the per-object mode). Several words can share a lock, which is [lock striping](/lock-striping/).

## The algorithm

```pseudo id=main
BEGIN()
L1  rv ← GV
L2  R ← ∅; W ← empty redo log

READ(a)
L3  if a ∈ W then return W[a]          ▷ read after write
L4  l1 ← lock(a)
L5  v ← a
L6  l2 ← lock(a)
L7  if l1 is owned or l1 ≠ l2 or l1.version > rv then ABORT
L8  R ← R ∪ {a}; return v

WRITE(a, v)
L9  W[a] ← v

COMMIT()
L10 if W = ∅ then return COMMITTED     ▷ read-only: nothing to check
L11 for each stripe s of W: if not CAS(lock(s), (ver, FREE), (ver, me)) then ABORT
L12 wv ← FAA(GV, 1) + 1
L13 if wv ≠ rv + 1 then
L14     for each a ∈ R: if lock(a) is owned by another or lock(a).version > rv then ABORT
L15 for each (a, v) ∈ W: a ← v
L16 for each stripe s of W: lock(s) ← (wv, FREE)
L17 return COMMITTED

ABORT
L18 set each lock taken at L11 back to (its old version, FREE); drop R and W; retry
```

**Reads (L3 to L8).** A transaction first looks in its own write set, so it reads its own writes. Otherwise it samples the lock, loads the word, and samples the lock again. If the lock was free, did not change, and has a version not newer than $rv$, then the loaded value was the current value of the word at the first sample, and no transaction that committed after the begin has written it. This post-validation is what gives opacity. TL2 reads are invisible: a reader writes no shared word, so readers do not slow each other down. In the paper, a read-only transaction does not even keep the read set $R$, since it never validates at commit.

**Commit (L10 to L17).** The order of the steps matters. The transaction locks its write set first (L11), then takes its write version from the clock (L12), then validates its read set (L14), then writes back (L15) and releases each lock with version $wv$ (L16). Because the locks are held before $wv$ is drawn, any reader whose $rv \ge wv$ either finds the lock owned or finds the new version. The paper acquires the locks "in any convenient order using bounded spinning" and aborts when the bound runs out; the code on this page aborts at once on an owned lock. Both choices avoid [deadlock](/deadlock/), because no transaction waits forever for a lock.

**The skip at L13.** If $wv = rv + 1$, then no other transaction took a write version between the begin and the commit of this one, so no transaction committed in that window and validation is not needed.

**Abort (L18).** An aborting transaction has written no data word, because every abort happens before L15. So it can put back the old version of each lock it holds. Compare [TinySTM](/tinystm/) in write-through mode, where this is wrong.

## Example

Two accounts start with $a_0 = a_1 = 10$. Process $q$ runs an audit $T_2$ that returns $a_0 + a_1$. Process $p$ runs $T_1$, a transfer of 3 from $a_0$ to $a_1$. The run below is the one in `test_worked_example`.

| Step | Process | Lines | Effect | GV | lock$(a_0)$ | lock$(a_1)$ | $a_0$ | $a_1$ |
|---|---|---|---|---|---|---|---|---|
| 1 | $q$ | L1 | $T_2$: $rv = 0$ | 0 | (0, free) | (0, free) | 10 | 10 |
| 2 | $q$ | L4 to L8 | $T_2$ reads $a_0 = 10$; the lock is free at version $0 \le rv$ | 0 | (0, free) | (0, free) | 10 | 10 |
| 3 | $p$ | L1 to L9 | $T_1$: $rv = 0$, reads 10 and 10, buffers $a_0 = 7$, $a_1 = 13$ | 0 | (0, free) | (0, free) | 10 | 10 |
| 4 | $p$ | L11 | $T_1$ locks both stripes | 0 | (0, $T_1$) | (0, $T_1$) | 10 | 10 |
| 5 | $p$ | L12, L13 | $wv = 1 = rv + 1$: skip validation | 1 | (0, $T_1$) | (0, $T_1$) | 10 | 10 |
| 6 | $p$ | L15, L16 | write back, release with version 1 | 1 | (1, free) | (1, free) | 7 | 13 |
| 7 | $q$ | L4 to L7 | $T_2$ reads $a_1$: version $1 > rv = 0$, so ABORT | 1 | (1, free) | (1, free) | 7 | 13 |
| 8 | $q$ | L1 to L10 | retry with $rv = 1$: reads 7 and 13, commits with sum 20 | 1 | (1, free) | (1, free) | 7 | 13 |

The aborted first attempt of $T_2$ saw only $a_0 = 10$, which agrees with the serial order ($T_2$ attempt 1, $T_1$, $T_2$ attempt 2). Without the check at L7, step 7 would return $a_1 = 13$, and the audit would commit the sum 23, which no serial order gives. The test `test_without_post_validation...` finds this run by exhaustive search.

## Correctness

The full proof is in [the correctness proof](proofs/correctness). It orders each committed update transaction by its $wv$ and puts every other transaction just after the update transactions with $wv \le rv$. Four facts carry it. The clock never decreases, and FAA gives each committer a distinct $wv$. The version of each lock only grows, because a committer that takes a lock at version $v_0$ draws its $wv > v_0$ after it holds the lock. A read that passes L7 returns the value of the state after all committed transactions with $wv \le rv$ (the lock samples rule out a write in between, and a writer with a larger $wv$ either holds the lock or has raised the version). Commit validation at L14 shows that no transaction with $wv$ strictly between $rv$ and the own $wv$ wrote a word of $R$, so the reads also hold in the state just before the own $wv$. Real-time order holds because a transaction that begins after another one completes reads a clock value at least as large as the write version of the first.

Progress: no transaction waits for a lock, so TL2 cannot deadlock. It can [livelock](/livelock/): two transactions can keep making each other abort. A crashed lock owner makes every later access to its stripes abort, so TL2 is not [obstruction-free](/obstruction-freedom/).

## Complexity

Count shared memory steps. A read takes 3 steps (two lock samples and the load), plus a look-up in the private write set. A write takes no shared step. A read-only transaction commits with no further step, so it costs $3r$ steps in total. An update commit takes 2 steps per lock (read and CAS), 1 FAA, at most $r$ lock reads for validation, $w$ data writes and one release per lock: $\Theta(r + w)$ steps. So a transaction that does not abort costs $\Theta(r + w)$ steps. A design that validates its whole read set at each read pays $1 + 2 + \dots + r = r(r+1)/2$ checks instead; see [transaction validation](/transaction-validation/).

Space: one clock word and one lock word per stripe, so $O(m)$ shared words in the per-object mode and a fixed table in the per-stripe mode. Each transaction keeps $\Theta(r + w)$ private words.

The cost that the step count hides is the clock. Every update transaction does an FAA on GV, so the cache line of GV moves between cores at each commit. The TL2 code release has clock variants for this, named GV4, GV5 and GV6 in its release notes and discussed by Lev et al. (2009); see [global version clock](/global-version-clock/).

## Properties

- **Opaque**, by the proof above. Committed transactions are strictly serializable.
- **Invisible reads**: a reader does not write shared memory.
- **Commit-time locking with lazy versioning**: writes go to a redo log, and locks are taken only at commit. Write-write and read-write conflicts are found at commit, or at a read of a word that a later transaction changed. See [encounter-time locking](/encounter-time-locking/) for the other choice.
- **Blocking**: deadlock-free, but not obstruction-free. It can livelock.
- **Not privatization safe** in the basic form: a committed transaction can still be writing back when another thread accesses the same data outside a transaction. See [privatization safety](/privatization-safety/).
- **False conflicts** can come from lock striping: two different words that hash to the same lock conflict.

## Variants and improvements

- **Per-object and per-stripe locks.** The paper gives both modes. Per-object locks give no false conflicts but need a lock field in each object. Per-stripe locks work for any memory, at the cost of false conflicts.
- **Clock variants.** GV4 lets a committer whose CAS on the clock fails use the value that the winner wrote. GV5 does not increment the clock at commit and lets lock versions run ahead of it, at the cost of extra aborts. GV6 uses GV4 with a small probability and GV5 otherwise. These names come from the TL2 code release and the account of Lev et al. (2009), not from the DISC paper.
- **Snapshot extension.** When a read finds a version newer than $rv$, TL2 aborts. [TinySTM](/tinystm/) and [SwissTM](/swisstm/) instead read the clock again, validate the read set, and move $rv$ forward if the validation succeeds. This idea is the lazy snapshot algorithm of Riegel, Felber and Fetzer (2006).
- **No ownership records.** [NOrec](/norec/) keeps the global clock idea but drops the lock table: one global sequence lock, value-based validation and serialized write-back.
- **Encounter-time locking.** Taking the write locks at the first write, as TinySTM does, finds write-write conflicts early. See [encounter-time locking](/encounter-time-locking/) and [commit-time locking](/commit-time-locking/).

## When to use it

TL2 fits word-based STM in C or C++ where a transaction may follow pointers into memory that another transaction frees or changes, so that opacity is needed. It fits short transactions that mostly read, because reads are invisible and cheap and a read-only transaction commits with no extra work. It scales worse when many short update transactions commit at a high rate, because they all increment one clock. For long transactions that read many words, the abort when a read finds a newer version wastes work; the snapshot extension of TinySTM helps there.

## Pitfalls

- **No check after the read.** Without L7, a transaction can read one word from before a commit and another from after it. A read-only transaction then commits an inconsistent result. The test with `post_validate=False` shows the audit sum 23.
- **Sampling the lock only once.** The lock must be read before and after the load, or the load can see a write-back in progress. On hardware with weak memory order (ARM, POWER), the two lock loads and the data load need acquire order or fences; on x86 (TSO), loads are not reordered with other loads.
- **No write locks.** If two committers do not lock their write sets, both can pass validation on the same word, and one update is lost. The test with `write_locks=False` shows two committed increments that leave $x = 1$.
- **Wrong commit order.** Drawing $wv$ before the locks are held breaks the argument: a reader with $rv \ge wv$ could then read the old value while the lock is still free.
- **False conflicts.** With lock striping, a writer of $y$ can abort a reader of $x$ when both words share one lock. The test `test_lock_striping_gives_a_false_conflict` shows one abort with one stripe and none with one lock per word.
- **A crashed or descheduled committer.** A process that stops while it holds locks blocks those stripes. The test `test_a_crashed_committer_blocks_others` shows three aborts and no commit for the other process.
- **Forgetting the write set at a read.** A transaction must read its own buffered writes (L3); otherwise it reads the old value from memory.

## Implementations

## History

Dice and Shavit had earlier described Transactional Locking (TL), a lock-based STM that checked reads only by validation of the read set. TL2, presented by Dice, Shalev and Shavit at DISC 2006, added the global version clock, which lets each read be checked against the start of the transaction in constant time. The paper discusses "zombie" transactions that loop or access illegal memory, and argues that a consistent snapshot at every read is needed in unmanaged languages. Riegel, Felber and Fetzer published the lazy snapshot algorithm at the same conference, and TinySTM (2008) combined its snapshot extension with encounter-time locking. Guerraoui and Kapałka (2008) later defined opacity, the condition that TL2 satisfies.

## References
