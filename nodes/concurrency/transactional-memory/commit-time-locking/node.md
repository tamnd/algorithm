---
tag: CJ1W44
kind: concept
slug: commit-time-locking
name: Commit-time locking
aliases:
- lazy locking
- lazy acquire
area: concurrency/transactional-memory
level: advanced
summary: An STM takes the write locks only at the start of commit, so locks are held for a short time. Write conflicts are found late; every read must look in the redo log.
prereqs: [lazy-conflict-detection]
see_also: [encounter-time-locking, lazy-versioning, tl2, norec, transaction-conflict, transaction-validation, deadlock, lock-ordering]
sources:
  - paper: doi:10.1007/11864219_14
    title: "Dave Dice, Ori Shalev and Nir Shavit, Transactional Locking II, DISC 2006, LNCS 4167, pages 194-208"
    locator: Section 2.1 (the commit, which locks the write set, takes a write version, validates the read set, writes back and releases)
  - paper: "Dave Dice and Nir Shavit, What really makes transactions faster?, TRANSACT 2006"
    locator: the first Transactional Locking (TL) algorithm and its encounter-time and commit-time locking modes
  - paper: doi:10.1145/1693453.1693464
    title: Luke Dalessandro, Michael F. Spear and Michael L. Scott, NOrec, streamlining STM by abolishing ownership records, PPoPP 2010
    locator: a single global sequence lock, taken only at commit
  - book: isbn:9781608452354
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Morgan and Claypool, 2010
    locator: Chapter 4 (Software transactional memory), the sections on lock-based STM with versioned locks
---

**Commit-time locking** (CTL) is the rule that a lock-based [software transactional memory](/software-transactional-memory/) takes the write locks of a transaction only when the transaction commits. Until then its writes sit in a private [redo log](/redo-log/) and it holds no lock. At commit, it locks every word (or stripe) of its write set, validates its reads, writes back the log, and releases the locks with a new version. [TL2](/tl2/) is the best known STM that works this way, and [NOrec](/norec/) is the extreme case, with one global lock taken only at commit. The counterpart is [encounter-time locking](/encounter-time-locking/) (ETL), which takes each lock at the first write. CTL is a choice about *when locks are held*. It implies that write-write conflicts are found at commit, but it does not by itself say when read-write conflicts are found: TL2 uses CTL and still checks each read as it happens. CTL needs [lazy versioning](/lazy-versioning/), since memory must not change before the locks are held.

## In plain words

The transaction keeps its changes on a private list and touches no lock while it works. Only at the very end does it lock the words it wants to change, check that what it read is still current, copy its changes in, and unlock. The locks are held only for those few steps, so other transactions are rarely in the way. The price is that a clash between two writers is found only at the end, after both have done all their work.

## The idea

**Notation and model.** $n$ is the number of processes, $r$ and $w$ the numbers of words a transaction reads and writes. Each word maps to a versioned lock, as in TL2, and the STM uses atomic read, write, [compare-and-swap](/compare-and-swap/) (consensus number $\infty$) and [fetch-and-add](/fetch-and-add/) (consensus number 2), on a [sequentially consistent](/sequential-consistency/) memory.

A write of $T$ only adds to the redo log. A read of $T$ first looks in the redo log (read after write), and otherwise reads the word with the STM's checks: in TL2, the lock must be free and its version at most $T$'s start time $rv$, before and after the load.

The commit of $T$, as in TL2:

1. For each stripe of the write set, CAS its lock from free to owned by $T$. If one CAS fails, release what was taken and abort.
2. Get a write version $wv$ from the [global version clock](/global-version-clock/) by fetch-and-add.
3. [Validate](/transaction-validation/) the read set: each lock must be free (or owned by $T$) with a version at most $rv$.
4. Write back the redo log.
5. Release each lock with version $wv$.

### Locking time and detection time

CTL decides when write locks are held; it does not decide when every kind of conflict is detected.

| Kind of conflict | Under CTL |
|---|---|
| write, then write | found at the commit of the second one to commit, when its CAS fails or its validation fails; two blind writes are not a conflict for the result at all |
| write, then read | the reader cannot see the writer before the writer commits; it reads the committed value, which is correct |
| read, then write | found by the reader's validation; in TL2 at the reader's next read (if the version is newer than $rv$) or at its commit |

So TL2, a CTL STM, is lazy for write-write conflicts but checks reads eagerly enough to be [opaque](/opacity/). An STM can also combine early detection of write conflicts with late locking of reads: [SwissTM](/swisstm/) takes write locks at encounter time and read-visible locks at commit.

### Why CTL

- Locks are held for a few steps, so readers rarely see a locked word and abort.
- Two transactions that both write a word blindly can both commit, one after the other.
- No deadlock can arise from lock order, because the commit takes the locks with a CAS and aborts on failure instead of waiting. If an STM wants to wait at commit, it can sort the write set and lock in address order ([lock ordering](/lock-ordering/)).
- A transaction that aborts before commit has never touched shared memory or locks.

### Why not

- A write-write conflict is found only after both transactions have done all their work.
- Every read must look in the redo log, since there is no owned lock that marks the word as written.
- A long transaction can be overtaken again and again by short transactions that commit first.

## Examples

**Lock hold time.** A transaction reads $a_0$, writes $a_0 \leftarrow a_0 - 1$, and reads $k$ more words. In a solo run of the simulations, the shared steps between the CAS that takes the lock of $a_0$ and the write that releases it are 3 for TL2, whatever $k$ is, against $3 + 3k$ for TinySTM's encounter-time locking (3, 9 and 18 for $k = 0, 2, 5$). See [encounter-time locking](/encounter-time-locking/) for the table.

**Two writers, both commit.** $T_1$ writes $x \leftarrow 1$ and then reads five words; meanwhile $T_2$ reads $x$, writes $x \leftarrow x + 10$ and commits. Under TL2, $T_1$ held no lock when $T_2$ committed, so $T_2$ commits with $x = 10$, and $T_1$, which never read $x$, then commits $x = 1$. The order "$T_2$ then $T_1$" explains the run. Under TinySTM's ETL, $T_2$ finds $T_1$'s lock and aborts.

**A lost update without the locks.** The commit locks matter. The TL2 test `test_without_write_locks_an_update_is_lost` removes them: two transactions both read $x = 0$ and write $x \leftarrow x + 1$. $T_1$ takes $wv = 1$; $T_2$ takes $wv = 2$, validates ($x$ is unchanged) and writes $x = 1$; $T_1$ has $wv = rv + 1$, so TL2 lets it skip validation, and it writes $x = 1$ again. Both commit and one increment is lost. With the locks, $T_1$ holds the lock of $x$ from the start of its commit, so $T_2$'s CAS on that lock fails and $T_2$ aborts.

## Where it is used

- [TL2](/tl2/) (2006), per stripe or per object.
- [NOrec](/norec/) (2010), with one global sequence lock that a writer takes at commit; read-only transactions take no lock at all.
- The first Transactional Locking algorithm (Dice and Shavit, TRANSACT 2006), in its commit-time mode.
- [SwissTM](/swisstm/) takes its read-visible locks at commit.
- In databases, [optimistic concurrency control](/optimistic-concurrency-control/) has the same shape: a private read phase, then a short critical section for validation and write.

## References
