---
tag: 4NBAVM
kind: algorithm
slug: norec
name: NOrec
aliases:
- NOrec STM
- no ownership records
area: concurrency/transactional-memory
level: advanced
summary: STM of Dalessandro, Spear and Scott (2010) with no ownership records. One global sequence lock, value-based validation and serialized write-back give opacity and privatization safety.
complexity:
  vars: {r: the number of words a transaction reads, w: the number of words it writes, c: the number of writers that commit while the transaction runs}
  steps: {read: O(r), commit: Θ(r + w), total: O(r + w + c·r)}
  space: {shared: Θ(1), extra: Θ(r + w)}
properties: {deterministic: true, opaque: true, blocking: true, livelock_free: true, privatization_safe: true}
history:
  year: 2010
  people: [Luke Dalessandro, Michael F. Spear, Michael L. Scott]
  note: Dalessandro, Spear and Scott presented NOrec at PPoPP 2010. Dice and Shavit had found an equivalent algorithm earlier but did not publish it as a paper.
prereqs: [transaction-validation, lazy-versioning, lazy-conflict-detection, compare-and-swap]
see_also: [opacity, privatization-safety, tl2, global-version-clock, zombie-transactions, hybrid-transactional-memory]
sources:
  - paper: doi:10.1145/1693453.1693464
    title: "Luke Dalessandro, Michael F. Spear and Michael L. Scott, NOrec: streamlining STM by abolishing ownership records, PPoPP 2010"
    locator: the listings of the algorithm (Validate, TXBegin, TXRead, TXWrite, TXCommit) and the discussion of privatization, publication and livelock freedom
  - paper: doi:10.1007/11864219_13
    title: "Michael F. Spear, Virendra J. Marathe, William N. Scherer III and Michael L. Scott, Conflict detection and validation strategies for software transactional memory, DISC 2006, LNCS 4167, pages 179-193"
    locator: Section 3, the global commit counter heuristic (validate only when some writer has committed)
  - paper: doi:10.1145/1345206.1345233
    title: "Rachid Guerraoui and Michał Kapałka, On the correctness of transactional memory, PPoPP 2008"
    locator: the definition of opacity, which the correctness proof uses
  - book: isbn:9781608452354
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Morgan and Claypool, 2010
    locator: Chapter 4 (Software transactional memory), the sections on value-based validation and on privatization
---

NOrec ("no ownership records") is a word-based [software transactional memory](/software-transactional-memory/) of Luke Dalessandro, Michael Spear and Michael Scott (PPoPP 2010). It keeps no lock or version per word. Its only shared metadata is one global sequence lock: a counter that is odd while a writer copies its writes to memory and even otherwise. A transaction logs the values that it reads and keeps its writes in a redo log ([lazy versioning](/lazy-versioning/)). It validates by value: it checks that each logged word still holds the logged value, and it does so only when the sequence lock shows that some writer has committed. Writers commit one at a time. The result is [opaque](/opacity/) (all transactions, aborted ones included, read values of one serial order that respects real time), livelock-free, and [privatization safe](/privatization-safety/), with very low cost per read.

## In plain words

There is one shared counter. It is odd while some transaction is writing its results to memory, and even otherwise. A transaction notes the counter when it starts. Each time it reads a word, it also writes down the value it saw. If the counter is still the noted value, nothing has changed and the read is good. If the counter has moved on, some writer finished in the meantime, so the transaction checks its notes: does every word it read still hold the value it saw? If yes, it notes the new counter and goes on. If no, it starts again. To commit, a writer moves the counter from the noted even value to odd, which only one writer can do at a time, copies its writes to memory, and makes the counter even again.

## The problem

Give $n$ processes [transactions](/transaction/) on a memory of words: begin, read$(a)$, write$(a, v)$ and commit, where reads and commits may abort. The safety condition is [opacity](/opacity/). The design goal of NOrec is to remove the per-word metadata (ownership records, or orecs) of designs such as [TL2](/tl2/): no lock table, no false conflicts from hashing, and a small fixed cost per read. The price is that all writers commit one at a time.

### Model and notation

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $p, q$ | process names |
| GL | the global sequence lock, one shared word |
| snapshot | the even value of GL that the transaction last checked against |
| reads | the read log: a list of (address, value) pairs |
| writes | the redo log: a map from address to value |
| $r, w$ | the number of words that one transaction reads and writes |
| $c$ | the number of writers that commit while one transaction runs |

The processes are asynchronous and may crash. They share words with atomic read, write and [compare-and-swap](/compare-and-swap/) (consensus number $\infty$). The memory is [sequentially consistent](/sequential-consistency/). "Await GL is even" is a spin loop that reads GL until it is even.

## The algorithm

```pseudo id=main
BEGIN()
L1  snapshot ← await GL is even; reads ← empty list; writes ← empty map

READ(a)
L2  if a ∈ writes then return writes[a]   ▷ read after write
L3  v ← a
L4  while snapshot ≠ GL do                 ▷ a writer has committed since snapshot
L5      snapshot ← VALIDATE()
L6      v ← a
L7  append (a, v) to reads; return v

WRITE(a, v)
L8  writes[a] ← v

VALIDATE()
L9  loop
L10     t ← await GL is even
L11     for each (a, v) in reads: if a ≠ v then ABORT
L12     if GL = t then return t

COMMIT()
L13 if writes is empty then return COMMITTED      ▷ read-only
L14 while not CAS(GL, snapshot, snapshot + 1) do snapshot ← VALIDATE()
L15 for each (a, v) in writes: a ← v
L16 GL ← snapshot + 2; return COMMITTED
```

On ABORT, the transaction drops its logs and starts again at L1.

**Reads (L2 to L7).** The load at L3 comes before the check of GL at L4. If GL still equals the snapshot, then no writer has started a write-back since the snapshot was taken, so the loaded value belongs to the same consistent state as all earlier reads. This is the "post-read validation" that gives opacity. When the check fails, the transaction validates and loads the word again.

**Validation (L9 to L12).** It waits until no write-back is in progress (L10), compares each logged value with memory (L11), and accepts only if GL did not change during the comparison (L12). So all the compared values come from one moment, and the new snapshot is the time of that moment. This is value-based validation: a word that changed and then changed back passes, which is correct, because the transaction sees the same values that it would see if it had run at the new snapshot. The check at L4 is the global commit counter heuristic of Spear et al. (2006): a transaction validates only when some writer has committed.

**Commit (L13 to L16).** A read-only transaction commits at once, since its reads are already consistent at its snapshot. A writer moves GL from its snapshot to an odd value with one CAS. This succeeds only if no writer committed since the snapshot, so the reads are still valid at the moment of the CAS. If the CAS fails, the writer validates again and retries. The odd value excludes every other committer and every reader that needs a new snapshot until the write-back ends at L16.

## Example

Three accounts start with $a_0 = a_1 = a_2 = 10$. Process $q$ runs an audit that returns $a_0 + a_1$. The runs below are the ones in `test_worked_example`.

**A writer that touches another word.** Process $p$ commits a transaction that sets $a_2 = 15$ while the audit runs.

| Step | Process | Lines | Effect | GL | reads of the audit |
|---|---|---|---|---|---|
| 1 | $q$ | L1 | snapshot $= 0$ | 0 | empty |
| 2 | $q$ | L3, L4, L7 | $a_0 = 10$; GL $= 0$ = snapshot | 0 | $(a_0, 10)$ |
| 3 | $p$ | L1, L8, L13, L14 | CAS(GL, 0, 1) succeeds | 1 | $(a_0, 10)$ |
| 4 | $p$ | L15, L16 | $a_2 \leftarrow 15$; GL $\leftarrow 2$ | 2 | $(a_0, 10)$ |
| 5 | $q$ | L3, L4 | $a_1 = 10$; GL $= 2 \ne 0$ | 2 | $(a_0, 10)$ |
| 6 | $q$ | L5, L9 to L12 | $a_0$ is still 10; GL stayed 2: snapshot $= 2$ | 2 | $(a_0, 10)$ |
| 7 | $q$ | L6, L4, L7, L13 | $a_1 = 10$ again; commit with sum 20 | 2 | $(a_0, 10), (a_1, 10)$ |

The audit paid one validation and did not abort. With per-word locks and lock striping, the write of $a_2$ could even have aborted the audit if $a_2$ shared a lock with $a_1$. NOrec has no false conflicts of this kind.

**A writer that changes a logged word.** If $p$ instead moves 3 from $a_0$ to $a_1$ at step 3, the validation at step 6 finds $a_0 = 7 \ne 10$ and the audit aborts. The retry reads $7 + 13 = 20$. Without the check at L4, the audit would read $a_1 = 13$ next to the old $a_0 = 10$ and commit the sum 23. The test `test_without_the_check_after_each_read...` shows this run.

## Correctness

The full proof is in [the correctness proof](proofs/correctness). Writers that pass L14 are totally ordered by their CAS, and the $k$-th one moves GL from $2k - 2$ to $2k - 1$ and then to $2k$. Data words change only while GL is odd, so whenever GL equals $2k$ the memory is exactly the state $S_k$ after the first $k$ writers. A transaction keeps the invariant that its read log agrees with $S_{s/2}$ for its current snapshot $s$: a read keeps it because GL did not move between the snapshot and the check at L4, and a validation re-establishes it at a new even value because GL did not move during the comparison. A writer's CAS succeeds only on its own snapshot, so its reads agree with the state just before its write-back. The serial order puts the writers in CAS order and every other transaction just after the writer that its last snapshot names. The same proof shows that a transaction aborts, or its CAS fails, only when some other writer committed after its snapshot, so NOrec is livelock-free.

## Complexity

Count shared memory steps. A read takes 2 steps (the load and the check of GL) when no writer committed since the snapshot. Each validation takes $r + 2$ steps for $r$ logged reads. A transaction validates at most once per writer that commits during its run, so a transaction that does not abort takes $O(r + w + c\,r)$ steps, where $c$ is the number of such writers. In the worst case $c$ grows with $r$, and the cost is $\Theta(r^2)$, the same as incremental [validation](/transaction-validation/); in the common case of few writers, it is close to $\Theta(r + w)$. Commit takes one CAS, $w$ writes and one release, plus the validations caused by failed CAS steps.

Space: one shared word in total. Each transaction keeps $\Theta(r + w)$ private words. There is no lock table, so there are no false conflicts from hashing and no cache misses on metadata.

The weak points are the serial write-back, which limits throughput when many transactions write, and the fact that every commit makes every running transaction validate, even when their data are disjoint.

## Properties

- **Opaque**: every read is consistent with the current snapshot, so a transaction never becomes a [zombie](/zombie-transactions/), and NOrec needs no sandboxing.
- **Livelock-free**: a transaction aborts only when another writer has committed.
- **Privatization safe**: write-backs are serialized, and a transaction that commits after another one sees GL even only after the earlier write-back has ended. So code that privatizes data in one transaction and then accesses it outside transactions cannot see a write-back that is still in progress. The paper also argues publication safety, from value-based validation.
- **Blocking**: a writer that stops during its write-back leaves GL odd, and every other transaction waits at L1 or L10.
- **No per-word metadata**: no false conflicts, but also no parallel write-back.

## Variants and improvements

- **Transactional Mutex Locks (TML)** use one sequence lock in the same way but let only one writer run at a time, and that writer updates memory in place.
- **Hybrid NOrec** runs transactions in [best-effort hardware TM](/best-effort-htm/) and falls back to NOrec, using the global sequence lock to coordinate the two; see [hybrid transactional memory](/hybrid-transactional-memory/).
- **Orec-based designs.** [TL2](/tl2/), [TinySTM](/tinystm/) and [SwissTM](/swisstm/) keep one lock per stripe so that disjoint writers can commit in parallel, at the cost of a lock table and possible false conflicts.
- **The broken variant on this page.** `NOrec(check_reads=False)` skips the check at L4. It validates only when a writer commits, so its read-only transactions can commit inconsistent results. It shows why the check after each read is needed.

## When to use it

NOrec fits workloads with few writers, many readers and short transactions, and machines with a modest number of cores. It is a good default fallback path for hybrid TM, and a good choice when the STM must be privatization safe without extra fences. It does not fit workloads in which many transactions write disjoint data at the same time, since their write-backs are serialized.

## Pitfalls

- **Loading after the check.** The order is load, then check GL. A check before the load cannot rule out a write-back that starts between the two.
- **Validating during a write-back.** Validation must wait for an even GL (L10) and confirm that GL did not change (L12). Otherwise it can compare against a half-written state.
- **Retrying the commit CAS without validation.** A failed CAS at L14 means that another writer committed. The transaction must validate before it tries again with the new snapshot.
- **No check after each read.** A design that validates only at commit is not opaque; see `NOrec(check_reads=False)` and [zombie transactions](/zombie-transactions/).
- **Assuming that a changed and restored value is a conflict.** It is not one for NOrec. The test `test_a_change_and_a_change_back_passes_value_validation` shows a reader that sees $x = 0$ before and after two writers change $x$ to 1 and back, and the history is opaque.
- **A long write-back.** All other transactions wait while a large writer copies its log. Keep update transactions small.

## Implementations

## History

Spear, Marathe, Scherer and Scott (2006) studied when an STM must validate, and proposed a global commit counter that lets a transaction skip validation when no writer has committed. JudoSTM (Olszewski, Cutler and Steffan, 2007) already used value-based validation. Dalessandro, Spear and Scott combined these ideas in NOrec and presented it at PPoPP 2010. The paper notes that Dice and Shavit had found an equivalent algorithm earlier but had not published it. NOrec later became the software path of Hybrid NOrec and a common baseline in STM studies.

## References
