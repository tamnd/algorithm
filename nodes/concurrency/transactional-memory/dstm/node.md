---
tag: 4KD1YP
kind: algorithm
slug: dstm
name: DSTM
aliases:
- Dynamic Software Transactional Memory
area: concurrency/transactional-memory
level: research
summary: Object-based, obstruction-free STM of Herlihy, Luchangco, Moir and Scherer (PODC 2003). Locators, commit by one CAS on a status word, and a pluggable contention manager.
complexity:
  vars: {r: the number of objects a transaction opens for reading, w: the number of objects it opens for writing, b: the number of back-off steps of the contention manager}
  steps: {open: O(r + b), commit: O(r), total: O((r + w)·r + b)}
  space: {per_object: Θ(1), extra: Θ(r + w)}
properties: {deterministic: true, opaque: true, blocking: false, obstruction_free: true, lock_free: false}
history:
  year: 2003
  people: [Maurice Herlihy, Victor Luchangco, Mark Moir, William N. Scherer III]
  note: Herlihy, Luchangco, Moir and Scherer presented DSTM at PODC 2003. It was the first STM for dynamic data structures and the first obstruction-free one.
prereqs: [software-transactional-memory, obstruction-freedom, compare-and-swap]
see_also: [opacity, contention-management, polite-contention-manager, karma-contention-manager, transaction-validation, shavit-touitou-stm, tl2, zombie-transactions]
sources:
  - paper: doi:10.1145/872035.872048
    title: "Maurice Herlihy, Victor Luchangco, Mark Moir and William N. Scherer III, Software transactional memory for dynamic-sized data structures, PODC 2003, pages 92-101"
    locator: the sections on the TMObject and Locator, opening an object, the status CAS, read-only access and validation, early release, and the contention manager interface (Figure 6) with the Aggressive and Polite managers
  - paper: doi:10.1007/11864219_13
    title: "Michael F. Spear, Virendra J. Marathe, William N. Scherer III and Michael L. Scott, Conflict detection and validation strategies for software transactional memory, DISC 2006, LNCS 4167, pages 179-193"
    locator: the quadratic cost of incremental validation with invisible reads
  - paper: doi:10.1145/1345206.1345233
    title: "Rachid Guerraoui and Michał Kapałka, On the correctness of transactional memory, PPoPP 2008"
    locator: the definition of opacity
  - book: isbn:9781608452354
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Morgan and Claypool, 2010
    locator: Chapter 4 (Software transactional memory), the section on nonblocking STM systems
---

DSTM (Dynamic Software Transactional Memory) is the object-based, [obstruction-free](/obstruction-freedom/) [software transactional memory](/software-transactional-memory/) of Maurice Herlihy, Victor Luchangco, Mark Moir and William N. Scherer III (PODC 2003). Unlike the [Shavit and Touitou STM](/shavit-touitou-stm/), it does not need to know the data set of a transaction in advance, so a transaction can follow pointers in a list or a tree. Each object points to a *locator* that names the last transaction to open it for writing, the old version and the new version. A transaction commits with one CAS on its own status word, which makes all its new versions current at once. Reads are invisible and are validated at every open, so DSTM is [opaque](/opacity/): every transaction, even one that later aborts, sees a state that some serial run of the committed transactions could produce. Conflicts go to a [contention manager](/contention-management/), a separate module with a fixed interface.

## In plain words

Each shared object has a small record, the locator, that says who wrote it last and keeps two copies: the value before that writer and the value the writer wants. If the writer committed, the new copy is the real value; if it aborted or is still running, the old copy is. A transaction that wants to write an object makes a new locator that names itself, with the real value as its old copy, and swaps it in with a CAS. To commit, it changes its own status from ACTIVE to COMMITTED with one CAS, and at that moment every object it wrote shows its new copy. If an object belongs to another running transaction, the contention manager decides whether to wait or to abort that transaction.

## The problem

Give $n$ processes [transactions](/transaction/) on a set of shared objects: begin, open an object for reading or for writing, and commit, where any operation may abort. The set of objects that a transaction opens is not known in advance; it depends on the values it reads. The safety condition is [opacity](/opacity/). The progress condition is obstruction-freedom: a transaction that runs alone for long enough commits, even if other processes have stopped in the middle of their transactions.

### Model and notation

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $o$ | a transactional object (a TMObject) |
| start$(o)$ | the word of $o$ that points to its current locator |
| locator | an immutable record (owner, old, new); old and new are versions of the object |
| status$(T)$ | the status word of transaction $T$: ACTIVE, COMMITTED or ABORTED |
| $cv(o)$ | the current version of $o$: new if the owner committed, old otherwise |
| R | the read table of a transaction: pairs (object, version) |
| $r, w$ | the number of objects that one transaction opens for reading and for writing |

The processes are asynchronous and may stop at any time. They share words with atomic read, write and [compare-and-swap](/compare-and-swap/) (CAS), under [sequential consistency](/sequential-consistency/). In the paper the new version is a private copy of the object, reachable from the locator; the transaction changes the copy in place. The code on this page keeps the value of the copy inside the locator.

## The algorithm

```pseudo id=main
BEGIN()
L1  status(me) ← ACTIVE; R ← ∅

CURRENT(o)                                  ▷ the version of o that is committed now
L2  loc ← start(o)
L3  if loc.owner ≠ me and status(loc.owner) = ACTIVE then ask the contention manager: back off, or CAS(status(loc.owner), ACTIVE, ABORTED); go to L2
L4  if status(loc.owner) = COMMITTED then return (loc, loc.new) else return (loc, loc.old)

OPEN-READ(o)
L5  (loc, cur) ← CURRENT(o); R ← R ∪ {(o, cur)}; if not VALIDATE() then ABORT; return cur

OPEN-WRITE(o)
L6  if I own o then return my copy
L7  (loc, cur) ← CURRENT(o); new ← (me, cur, a copy of cur)
L8  if not CAS(start(o), loc, new) then go to L7
L9  if (o, v) ∈ R and v ≠ cur then ABORT; if not VALIDATE() then ABORT; return my copy

VALIDATE()
L10 if status(me) ≠ ACTIVE then return false
L11 for each (o, v) in R: if CURRENT(o) ≠ v or another ACTIVE transaction owns o then return false; return true

COMMIT()
L12 if not VALIDATE() then ABORT
L13 if CAS(status(me), ACTIVE, COMMITTED) then return COMMITTED else ABORT

ABORT
L14 status(me) ← ABORTED

RELEASE(o)                                  ▷ early release
L15 R ← R ∖ {(o, ·)}
```

**Locators and the status CAS (L7, L8, L13).** A locator never changes after it is made. To write $o$, a transaction makes a new locator whose old version is the current version of $o$ and whose new version is a private copy, and installs it with one CAS on start$(o)$. While the owner is ACTIVE, every other transaction sees the old version, so nothing becomes visible. The CAS at L13 flips the status to COMMITTED, and at that instant every object whose locator names the transaction has the new version as its current version. A transaction that opens $w$ objects for writing does $w + 1$ CAS steps when there is no conflict.

**Conflicts and the contention manager (L3).** An open that finds an object owned by another ACTIVE transaction does not wait for it. It asks the contention manager, which either tells it to back off and look again, or tells it to abort the owner with a CAS of the owner's status from ACTIVE to ABORTED. After that, the old version of the object is current, and the open goes on. In the paper, the contention manager is an object with a fixed interface: the STM tells it when a transaction begins, commits, aborts or opens an object, and asks it what to do on a conflict. The paper gives two managers. *Aggressive* always aborts the owner. *Polite* backs off exponentially a few times before it aborts the owner. Later work gave many more, such as [Karma](/karma-contention-manager/) and [Polka](/polka-contention-manager/).

**Invisible reads and validation (L5, L10, L11).** An open for reading does not change the object. It records the version in the read table and validates the whole table: the own status must still be ACTIVE, and each object read must still have the same current version. This check after every open is what keeps a transaction from acting on an inconsistent state, a [zombie](/zombie-transactions/). It costs $O(r)$ steps per open, and so $O(r^2)$ for a transaction that reads $r$ objects; see [transaction validation](/transaction-validation/).

**Strict validation (L11).** The code on this page also fails a validation when another ACTIVE transaction has an object of the read table open for writing. If validation checks only that each read version is still current, then two transactions $T$ (reads $x$, writes $y$) and $U$ (reads $y$, writes $x$) can both pass the validation at L12 before either CAS at L13, and both commit: write skew, which no serial order explains. The test `test_version_only_validation_allows_write_skew` shows this run. We could not confirm from the text of the paper how DSTM closes this window, so the page states the stricter check that the proof needs.

**Early release (L15).** A transaction may remove an object from its read table before it commits. Then a later change to the object no longer aborts it. A search in a sorted linked list can release each node once it has passed it, so that writers behind it do not abort it. Early release gives up the guarantee for the released objects: the programmer must know that a change to them does not matter.

## Example

**A polite reader aborts a stalled writer.** Words $x = y = 0$. Process $p$ runs $x \leftarrow 1; y \leftarrow 1$, and process $q$ runs a transaction that reads $x$ and $y$. Both use the Polite manager with 3 rounds of back-off. The run is the one in `test_worked_example_polite_reader_aborts_a_writer`.

| Step | Process | Lines | Effect | start$(x)$ | status$(p)$ |
|---|---|---|---|---|---|
| 1 | $p$ | L1, L7, L8 | installs $(p, x{=}0, x{=}1)$ | owner $p$ | ACTIVE |
| 2 | $p$ | L9, L10 | validates (empty read table) | owner $p$ | ACTIVE |
| 3 | $q$ | L2, L3 | $x$ is owned by ACTIVE $p$: backs off 1, 2, then 4 steps | owner $p$ | ACTIVE |
| 4 | $q$ | L3 | after the last round, CAS status$(p)$ to ABORTED | owner $p$ | ABORTED |
| 5 | $q$ | L2, L4, L5 | current version of $x$ is the old one: $x = 0$; validates | owner $p$ | ABORTED |
| 6 | $q$ | L5, L12, L13 | reads $y = 0$; commits with $(0, 0)$ | owner $p$ | ABORTED |
| 7 | $p$ | L7 to L10 | opens $y$, then the validation sees its own ABORTED status | owner $p$ | ABORTED |
| 8 | $p$ | L14, L1 to L13 | retries and commits $x = y = 1$ | owner $p$ (new attempt) | COMMITTED |

The reader $q$ did not wait for $p$ to finish. If $p$ had stopped for ever after step 2, $q$ would still have committed, which is the point of obstruction-freedom. The test `test_obstruction_freedom_a_solo_run_finishes` stops a transfer after each possible number of steps and checks that a second transfer, running alone, commits.

**Livelock.** With the Aggressive manager, two transactions that write $x$ and $y$ in opposite orders can abort each other for ever. In a lockstep schedule, each one installs its first locator, then at its second open aborts the other, then finds itself aborted at its next validation, and both retry in the same rhythm. The test `test_aggressive_managers_can_livelock` runs 600 steps of this schedule with no commit. Obstruction-freedom does not rule this out; it promises progress only to a transaction that runs alone. See [livelock](/livelock/).

## Correctness

The full proof is in [the correctness proof](proofs/correctness). The current version of an object changes only when the owner of its locator commits, by the CAS on its status, and version identities never repeat. A committed transaction owns each object it writes from its CAS at L8 to its CAS at L13; in that interval no open of the object by another transaction returns, and every strict validation that checks it fails. Each transaction is placed in the serial order at the start of its last successful validation. Each read then returns the value of the last committed writer before that point. A read whose validation fails returns no value. Real-time order holds, since the point of a transaction lies between its begin and its end.

Obstruction-freedom: in a solo run, an open kills any ACTIVE owner after a bounded back-off, the install CAS cannot fail, and the validations can fail only for objects that other transactions opened before the solo run began. So the solo transaction commits after at most one abort.

## Complexity

Count shared memory steps. An open with no conflict takes 1 or 2 steps to find the current version, a CAS for a write, and a validation of $1 + 2r$ steps at most. A transaction that opens $r$ objects for reading checks $1 + 2 + \dots + r = r(r + 1)/2$ entries at its opens and $r$ more at commit; the test `test_validation_checks_grow_quadratically` counts them. A transaction that opens $w$ objects for writing does $w + 1$ CAS steps. With back-off, each conflict adds the back-off steps $b$.

Space: one start word and one locator per object, plus up to two versions while a writer is active. Each transaction keeps $\Theta(r + w)$ private words. Old locators and versions become garbage; the Java version of the paper relies on the garbage collector, and a C++ version needs a [memory reclamation](/epoch-based-reclamation/) scheme.

## Properties

- **Opaque**, by the proof, with strict validation.
- **Obstruction-free**, not lock-free: two transactions can abort each other for ever, and progress under contention depends on the contention manager.
- **Dynamic**: the objects a transaction touches need not be known in advance.
- **Commit is one CAS**: no write-back step, and no window in which a commit is half done.
- **Invisible reads** with incremental validation, $O(r^2)$ per transaction.
- **Extra indirection**: each access goes through start$(o)$ and a locator to reach the data.

## Variants and improvements

- **Contention managers.** Scherer and Scott studied many managers for DSTM, among them Karma, Polka and Greedy; see [contention management](/contention-management/) and [the Polite manager](/polite-contention-manager/).
- **Visible readers.** A transaction can register as a reader of the object, so that a writer sees it and must ask the contention manager before it overrides it. This replaces the $O(r^2)$ validation by extra writes to shared memory on every read.
- **Global commit counter.** A transaction can skip validation when no transaction has committed since its last one; see [transaction validation](/transaction-validation/).
- **ASTM, RSTM and DSTM2.** Later object-based STMs removed the extra indirection of the locator, made the acquire time of an object adaptive, or turned the design into a framework.
- **Lock-based STMs.** [TL2](/tl2/) and later word-based STMs gave up obstruction-freedom for fewer steps per access.

## When to use it

DSTM fits object-based STM where a transaction must not depend on the progress of other threads, for example when threads can be preempted or stopped in the middle of a transaction. It is the model to study for nonblocking STM and contention management. In practice, lock-based STMs such as TL2 are faster, because they avoid the indirection and the CAS per opened object, and most STM systems today are blocking.

## Pitfalls

- **Validating only the committed version.** This lets two transactions that read what the other writes both commit, as the write-skew test shows. The validation must fail when another ACTIVE transaction owns an object of the read table, or the commit must close the window between the validation and the CAS in another way.
- **Skipping validation at each open.** A transaction that validates only at commit can see $x = 0$ and $y = 1$ when every commit keeps $x = y$, and act on it as a zombie. The test `test_without_validation_at_each_open_a_zombie_sees_x_ne_y` shows the run.
- **A contention manager that waits for ever.** If the manager waits for an owner instead of aborting it after a bound, a stopped owner blocks everyone, and DSTM is no longer obstruction-free.
- **Aggressive managers.** They can livelock; a Polite or Karma manager makes this less likely but cannot rule it out.
- **Releasing too early.** Early release drops the check for an object. If the rest of the transaction depends on the released value, the result may not be serializable.

## Implementations

The code on this page keeps the new value inside the locator instead of in a separate copy, so a second write to the same object replaces the locator by one with the same identity and the new value. It uses the strict validation described above.

## History

Herlihy, Luchangco and Moir defined obstruction-freedom in 2003, and in the same year Herlihy, Luchangco, Moir and Scherer presented DSTM at PODC. Earlier STMs, such as the Shavit and Touitou STM of 1995, needed the data set of a transaction in advance; DSTM was the first to allow dynamic data structures. The paper also introduced the separation of the STM from its contention manager. Scherer and Scott then studied contention managers for DSTM, and Marathe, Scherer and Scott built ASTM and RSTM on its ideas. Herlihy, Luchangco and Moir later turned it into the DSTM2 framework.

## References
