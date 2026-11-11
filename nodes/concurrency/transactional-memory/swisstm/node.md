---
tag: DS6V72
kind: algorithm
slug: swisstm
name: SwissTM
area: concurrency/transactional-memory
level: research
summary: Word-based STM of Dragojević, Guerraoui and Kapałka (PLDI 2009). Eager write-write and lazy read-write conflict detection, a global clock, and a two-phase contention manager.
complexity:
  vars: {r: the number of words a transaction reads, w: the number of words it writes, e: the number of snapshot extensions, m: the number of data words, n: the number of processes}
  steps: {read: O(r), write: O(1), commit: O(r + w), total: O(r + w + e·r)}
  space: {shared: O(m + n), extra: Θ(r + w)}
properties: {deterministic: true, opaque: true, blocking: true, obstruction_free: false, deadlock_free: true}
history:
  year: 2009
  people: [Aleksandar Dragojević, Rachid Guerraoui, Michał Kapałka]
  note: Dragojević, Guerraoui and Kapałka presented SwissTM in the paper "Stretching transactional memory" at PLDI 2009, as an STM that works well for both short and long transactions.
prereqs: [tinystm, lazy-conflict-detection]
see_also: [opacity, eager-conflict-detection, contention-management, greedy-contention-manager, tl2, norec, transaction-conflict, stamp-benchmark-suite]
sources:
  - paper: doi:10.1145/1542476.1542494
    title: "Aleksandar Dragojević, Rachid Guerraoui and Michał Kapałka, Stretching transactional memory, PLDI 2009, pages 155-165"
    locator: the description of SwissTM (the two locks per memory stripe, the commit counter, the read, write, validate and commit procedures) and the section on the two-phase contention manager
  - paper: doi:10.1145/1345206.1345241
    title: "Pascal Felber, Christof Fetzer and Torvald Riegel, Dynamic performance tuning of word-based software transactional memory, PPoPP 2008, pages 237-246"
    locator: the description of TinySTM, the encounter-time design that SwissTM changes
  - paper: doi:10.1007/11864219_20
    title: "Torvald Riegel, Pascal Felber and Christof Fetzer, A lazy snapshot algorithm with eager validation, DISC 2006, LNCS 4167, pages 284-298"
    locator: the snapshot extension that SwissTM uses for its reads
  - paper: doi:10.1145/1073814.1073863
    title: "Rachid Guerraoui, Maurice Herlihy and Bastian Pochon, Toward a theory of transactional contention managers, PODC 2005, pages 258-264"
    locator: the Greedy contention manager, which the second phase of SwissTM uses
  - book: isbn:9781608452354
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Morgan and Claypool, 2010
    locator: Chapter 4 (Software transactional memory), the sections on lock-based STM with a global clock
---

SwissTM is a word-based [software transactional memory](/software-transactional-memory/) of Aleksandar Dragojević, Rachid Guerraoui and Michał Kapałka (PLDI 2009). It starts from the design of [TinySTM](/tinystm/): a [global version clock](/global-version-clock/), invisible reads with snapshot extension, and a redo log. It changes two things. First, it splits each lock into a write lock and a read lock, so that it finds write-write conflicts at the first write ([eager conflict detection](/eager-conflict-detection/)) but read-write conflicts only when the writer commits ([lazy conflict detection](/lazy-conflict-detection/)). Second, it uses a two-phase [contention manager](/contention-management/): a short transaction gives way on a conflict, and a long one takes a timestamp and uses the rules of the [Greedy contention manager](/greedy-contention-manager/). The aim is an STM that works well for both short and long transactions. SwissTM is [opaque](/opacity/), which means that every transaction, even one that later aborts, sees a state that some serial run of the committed transactions could produce.

## In plain words

Each word has two locks. A writer takes the write lock of a word at its first write and keeps the new value in a private log. Other writers see the write lock at once. Readers look only at the read lock, which holds the version of the word and is locked only while a committer copies its log to memory. So a reader and a writer of the same word run side by side, and the reader notices the writer only if the writer commits first.

When two writers want the same word, a contention manager decides. A transaction with few writes is cheap to restart, so it gives way. A transaction with many writes gets a timestamp from a shared counter; the older one wins, aborts the loser, and waits for the lock.

## The problem

Give $n$ processes [transactions](/transaction/) on a memory of $m$ words: begin, read$(a)$, write$(a, v)$ and commit, where any operation may abort. The safety condition is [opacity](/opacity/). The goals of SwissTM are good throughput on mixed workloads, with both short transactions and long ones that read and write much data, few wasted aborts of long transactions, and no starvation of long transactions by short ones.

### Model and notation

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $m$ | the number of data words |
| $r, w$ | the number of words that one transaction reads and writes |
| $e$ | the number of snapshot extensions of one transaction |
| CLOCK | the commit counter, one shared word |
| GREEDY | the counter that hands out greedy timestamps |
| wl$(a)$ | the write lock of word $a$: the owner, or FREE |
| rl$(a)$ | the read lock of word $a$: a version, or LOCKED |
| status | one word per process: the attempt, its state (active, committing, aborted) and its greedy timestamp $c$ |
| $vt$ | the valid timestamp: the clock value up to which the reads are known to be consistent |
| $ts$ | the commit timestamp that a committer draws from CLOCK |
| $c$ | the greedy timestamp; $\infty$ while the transaction is timid |

The processes are asynchronous. They share words with atomic read, write, [compare-and-swap](/compare-and-swap/) (CAS) and [fetch-and-add](/fetch-and-add/) (FAA), under [sequential consistency](/sequential-consistency/). The paper maps groups of neighbouring words to one pair of locks in a table; the code on this page gives each word its own pair.

## The algorithm

```pseudo id=main
BEGIN()
L1  status ← (active, c = ∞); vt ← CLOCK; R ← ∅; W ← ∅

READ(a)
L2  if my status is not active then ABORT
L3  if a ∈ W then return W[a]
L4  wait until rl(a) ≠ LOCKED; v1 ← rl(a); v ← a; v2 ← rl(a)
L5  if v1 ≠ v2 then go to L4
L6  R[a] ← v1
L7  if v1 > vt and not EXTEND() then ABORT
L8  return v

WRITE(a, v)
L9  if my status is not active then ABORT
L10 if a ∈ W then W[a] ← v; return
L11 o ← wl(a); if o = FREE then (if CAS(wl(a), FREE, me) then go to L13 else go to L11)
L12 s ← status of o; if s.state = active then (if c ≥ s.c then ABORT; if not CAS(status of o, s, aborted) then go to L11); wait until wl(a) ≠ o; go to L11
L13 W[a] ← v; if |W| = the greedy threshold then c ← FAA(GREEDY, 1) + 1 and CAS my status to (active, c), or ABORT if the CAS fails

EXTEND()
L14 now ← CLOCK; if rl(b) ≠ ver for some (b, ver) in R then return false; vt ← now; return true

COMMIT()
L15 if W = ∅ then return COMMITTED          ▷ read-only
L16 if not CAS(my status, active, committing) then ABORT
L17 for each a in W: saved[a] ← rl(a); rl(a) ← LOCKED
L18 ts ← FAA(CLOCK, 1) + 1
L19 if ts > vt + 1 and EXTEND's check fails then ABORT
L20 for each (a, v) in W: a ← v
L21 for each a in W: rl(a) ← ts; wl(a) ← FREE; return COMMITTED

ABORT
L22 restore rl(a) ← saved[a] for each saved a; wl(a) ← FREE for each a in W; my status ← aborted
```

**Two locks per word (L4, L11, L17).** The write lock says who will write the word; the read lock says which version of the word is in memory. A writer takes only the write lock while it runs, so readers are not stopped. At commit it sets the read locks of its words to LOCKED (L17), and only then can a reader be stopped, for the few steps of the write-back. In the check at L19, a word that the committer has itself locked is compared against the version saved at L17.

**Eager write-write detection (L11, L12).** A second writer of a word sees the write lock at its own first write, not at commit. Long transactions thus find write-write conflicts before they do more work. Because the first writer's value is only in its redo log ([lazy versioning](/lazy-versioning/)), the conflict does not stop any reader.

**Lazy read-write detection (L4 to L7, L19).** Reads are invisible. A reader that meets a version newer than $vt$ extends its snapshot as in [TinySTM](/tinystm/), and a committer validates its read set after it draws $ts$. So a read-write conflict shows up only when the writer has committed. A reader that commits first is simply placed before the writer in the serial order.

**The two-phase contention manager (L12, L13).** A transaction starts *timid* ($c = \infty$). On a write-write conflict with an active owner, a timid transaction aborts itself. After its write set reaches a threshold (10 writes in the paper), it takes a timestamp $c$ from GREEDY and becomes *greedy*. On a conflict, a greedy transaction with a smaller timestamp than the owner (an older one) aborts the owner with a CAS on the owner's status word and waits for the lock; otherwise it aborts itself. An aborted owner sees its status at its next operation or at the CAS of L16 and releases its locks. If the owner is already committing or aborted, the waiter just waits. Short transactions thus pay nothing for timestamps, and long transactions cannot be starved by short ones.

## Example

**The greedy phase.** Let the threshold be 1, so a transaction becomes greedy at its first write. Words $x = y = 0$. Process $p$ runs $x \leftarrow 1; y \leftarrow 1$, and process $q$ runs $y \leftarrow 2; x \leftarrow 2$. The run is the one in `test_worked_example_greedy_phase`.

| Step | Process | Lines | Effect | wl$(x)$ | wl$(y)$ | status of $p$ | status of $q$ |
|---|---|---|---|---|---|---|---|
| 1 | $q$ | L1, L9, L11, L13 | locks $y$; becomes greedy with $c = 1$ | free | $q$ | idle | active, 1 |
| 2 | $p$ | L1, L9, L11, L13 | locks $x$; becomes greedy with $c = 2$ | $p$ | $q$ | active, 2 | active, 1 |
| 3 | $q$ | L9, L11, L12 | $x$ is owned by $p$; $1 < 2$, so $q$ aborts $p$ by CAS and waits | $p$ | $q$ | aborted, 2 | active, 1 |
| 4 | $p$ | L9, L22 | the write of $y$ sees the abort; $p$ frees $x$ | free | $q$ | aborted, 2 | active, 1 |
| 5 | $q$ | L11, L13 | takes $x$ | $q$ | $q$ | aborted, 2 | active, 1 |
| 6 | $q$ | L15 to L21 | $ts = 1 = vt + 1$: no validation; $x = y = 2$; frees both | free | free | aborted, 2 | committed |
| 7 | $p$ | L1 to L21 | the retry commits $x = y = 1$ with $ts = 2$ | free | free | committed | committed |

Without a contention manager that lets one side win, the two transactions could each abort on the other's lock and restart in step, which is [livelock](/livelock/). Here $q$ is older and wins, and the run has one abort.

**Lazy read-write detection.** With $x = 0$, a writer $p$ takes wl$(x)$ for $x \leftarrow 1$ and stops before its commit. A reader $q$ reads $x$: rl$(x)$ holds version 0, so it reads 0 and commits. Then $p$ commits $x = 1$. No one aborts, and the serial order is $q$ then $p$. Under [encounter-time locking](/encounter-time-locking/) with one lock per word, as in TinySTM, $q$ would see an owned lock and abort. The run is the one in `test_lazy_read_write_detection`.

## Correctness

The full proof is in [the correctness proof](proofs/correctness). Opacity has the same shape as the proof for TinySTM. Only the owner of the write lock writes the read lock and the data word, and it writes the data word only while the read lock is LOCKED. Each release of a read lock sets either the saved version (after an abort, with no data written) or the new $ts$, which is larger than every earlier version. So a reader whose two samples of the read lock are equal has read a committed value with that version. The serial order puts each committed update transaction at its $ts$ and every other transaction just after the commits with $ts \le vt$, with its final $vt$. The contention manager plays no part in safety: the kill only changes a status word and never takes a lock from its owner.

The second theorem is that the contention manager cannot deadlock. A transaction waits for another only when it is greedy and older than the owner it has aborted, or when the owner is already committing or aborted. Greedy timestamps never change, so the waits-for graph has no cycle, and the last transaction on a chain of waits releases its locks in a bounded number of its own steps. The proof also shows why the kill CAS must expect the full status word, timestamp included.

## Complexity

Count shared memory steps. A read takes 1 status read and 3 lock and word reads when nothing changes, plus, for each extension, 1 clock read and at most $r$ lock reads. A write takes 1 status read and, at the first write of a word, 2 steps (a read and a CAS) when there is no conflict; the greedy switch adds 2 steps once. A commit takes 1 CAS, 2 steps per written word to lock, 1 FAA, at most $r$ lock reads, $w$ stores and $2w$ releases: $O(r + w)$. A transaction that does not abort and extends $e$ times costs $O(r + w + e \cdot r)$ steps; in the worst case this is $\Theta(r^2)$, as for incremental [validation](/transaction-validation/).

Space: the clock, the greedy counter, one status word per process, and two lock words per word (per stripe in the paper): $O(m + n)$. Each transaction keeps $\Theta(r + w)$ private words.

## Properties

- **Opaque**, by the proof.
- **Mixed conflict detection**: write-write conflicts at the first write, read-write conflicts at the writer's commit.
- **Invisible reads** with a [global version clock](/global-version-clock/) and snapshot extension.
- **Blocking but deadlock-free**: a transaction can wait for a lock, but the waits-for graph has no cycle. A transaction that stops while it holds write locks blocks the other writers of those words, so SwissTM is not [obstruction-free](/obstruction-freedom/).
- **Long transactions are protected**: once greedy, the transaction with the smallest timestamp is never aborted by a write-write conflict, so it can only abort by a failed validation.
- **Not privatization safe** in the basic form, like TL2 and TinySTM; see [privatization safety](/privatization-safety/).

## Variants and improvements

- **TinySTM** detects all conflicts at encounter time, with one lock per stripe, and aborts the transaction that finds the lock owned; see [TinySTM](/tinystm/).
- **TL2** detects all conflicts at commit, takes its locks at commit, and aborts instead of extending; see [TL2](/tl2/).
- **Other contention managers.** The second phase is Greedy. The first phase is a form of the timid policy. Other managers, such as Karma or Polka, can replace either phase; see [contention management](/contention-management/).
- **Lock granularity.** The paper maps several neighbouring words to one pair of locks and studies the effect of that choice on performance. Larger groups mean fewer locks to check and more [false conflicts](/transaction-conflict/).

## When to use it

SwissTM fits word-based STM for workloads that mix short transactions with long ones, such as large object graphs where a long traversal reads much and writes little. Lazy read-write detection lets long readers run beside writers, and the greedy phase stops short transactions from starving long ones. For workloads of only short transactions, a simpler design such as [NOrec](/norec/) or TinySTM may be as fast. Like TL2 and TinySTM, SwissTM has a shared clock that every update transaction increments.

## Pitfalls

- **Killing on a stale timestamp.** If the contention manager reads the owner's timestamp and then aborts the owner with a CAS that does not check the timestamp, two transactions can each see the other as timid, each abort the other, and each wait for the other's lock for ever. The tests found this run in an early version of the code on this page. The fix is to keep the timestamp in the status word and let the kill CAS expect the full word.
- **Committing after being killed.** The commit must change the status from active to committing with a CAS (L16). A plain check followed by a write lets a killed transaction commit while its killer waits.
- **Reading the write lock in a read.** A reader that aborts on an owned write lock gets encounter-time read-write detection back, and with it the aborts that SwissTM was built to avoid.
- **Checking the own locked words.** At L19 the committer has set its own read locks to LOCKED. Its validation must compare those words against the saved versions, or it fails on its own locks.
- **Greedy too early.** If every transaction becomes greedy at once, each pays for an FAA on the shared counter. The threshold keeps that cost to long transactions.

## Implementations

The code on this page simplifies the paper in three ways. It gives each word its own pair of locks instead of a hashed table. It does not wait or back off after an abort. And a transaction that meets a committing or aborted owner waits for the lock, whatever its phase.

## History

Dragojević, Guerraoui and Kapałka presented SwissTM at PLDI 2009 under the title "Stretching transactional memory". They built it after a study of earlier STMs on workloads with large transactions, where designs tuned for short transactions did badly. They kept the global clock and snapshot extension of TL2, LSA and TinySTM, and added the mix of eager and lazy conflict detection and the two-phase contention manager. The Greedy contention manager that its second phase uses comes from Guerraoui, Herlihy and Pochon (PODC 2005).

## References
