---
tag: HDPVHM
kind: technique
slug: transaction-validation
name: Transaction validation
aliases:
- read validation
- commit-time validation
- read-set validation
area: concurrency/transactional-memory
level: advanced
summary: Checking that the values a transaction has read are still current. Checking the whole read set after each read costs r(r+1)/2 checks; a global clock or commit counter cuts most of them.
prereqs: [read-set-and-write-set, transaction-conflict]
see_also: [global-version-clock, opacity, zombie-transactions, tl2, norec, dstm, lazy-conflict-detection, multi-version-stm]
sources:
  - paper: doi:10.1007/11864219_13
    title: "Michael F. Spear, Virendra J. Marathe, William N. Scherer III and Michael L. Scott, Conflict detection and validation strategies for software transactional memory, DISC 2006, LNCS 4167, pages 179-193"
    locator: the quadratic cost of incremental validation with invisible reads, and the global commit counter heuristic that skips a validation when no transaction has committed
  - paper: doi:10.1145/872035.872048
    title: "Maurice Herlihy, Victor Luchangco, Mark Moir and William N. Scherer III, Software transactional memory for dynamic-sized data structures, PODC 2003, pages 92-101"
    locator: the validation of all opened objects at each open, which keeps a DSTM transaction consistent
  - paper: doi:10.1007/11864219_14
    title: "Dave Dice, Ori Shalev and Nir Shavit, Transactional Locking II, DISC 2006, LNCS 4167, pages 194-208"
    locator: Section 2.1 (the check of each read against the start time rv, and the validation of the read set at commit)
  - paper: doi:10.1007/11864219_20
    title: "Torvald Riegel, Pascal Felber and Christof Fetzer, A lazy snapshot algorithm with eager validation, DISC 2006, LNCS 4167, pages 284-298"
    locator: validity ranges from a global time base, and the extension of a snapshot by validation
  - paper: doi:10.1145/1345206.1345233
    title: "Rachid Guerraoui and Michał Kapałka, On the correctness of transactional memory, PPoPP 2008, pages 175-184"
    locator: Section 6 (a lower bound of Ω(k) steps for progressive, single-version, opaque TMs with invisible reads, where k is the number of objects)
  - url: https://arxiv.org/abs/1502.04908
    title: Petr Kuznetsov and Srivatsan Ravi, Progressive transactional memory in time and space, 2015
    locator: the step lower bound quadratic in the size of the read set for progressive opaque TMs with invisible reads
  - paper: doi:10.1145/1693453.1693464
    title: Luke Dalessandro, Michael F. Spear and Michael L. Scott, NOrec, streamlining STM by abolishing ownership records, PPoPP 2010
    locator: value-based validation, done only when the global sequence lock has changed
---

**Transaction validation** is the check that every value a transaction has read so far is still the current value in memory, or at least that all its reads still fit one consistent state. An STM with *invisible reads* needs it: a reader writes no shared metadata, so a writer cannot tell the reader that it has changed a word the reader used. The reader must find out for itself, by looking again at its [read set](/read-set-and-write-set/). Validation at commit makes the committed transactions [serializable](/serializability/). Validation during the run is what makes an STM [opaque](/opacity/) (every transaction, also one that will abort, sees a consistent state) and keeps it from running [zombie transactions](/zombie-transactions/). The simple way, *incremental validation*, checks the whole read set after each read, which costs $1 + 2 + \dots + r$ checks for $r$ reads: quadratic. Spear, Marathe, Scherer and Scott (DISC 2006) measured this cost and proposed a global commit counter to skip most scans. A [global version clock](/global-version-clock/), as in [TL2](/tl2/) and LSA, removes the scans altogether: each read is checked once, in $O(1)$.

## In plain words

A transaction keeps a list of what it has read. Before it trusts a new value, it goes back over the list and checks that nothing on it has changed. If something changed, its picture of memory is mixed up and it must start again. Doing this after every read means that the tenth read checks nine old ones, the hundredth checks ninety nine, and so on, so long transactions spend most of their time checking. Two tricks help. One: keep a shared count of commits, and skip the check when the count has not moved. Two: stamp every write with the time of a global clock, and reject any value stamped later than the transaction's start; then one look at each value is enough.

## When it applies

- The STM uses **invisible reads**: readers leave no trace that writers can see. With visible reads, a writer finds the readers and aborts them or waits, and readers need not validate.
- The STM keeps **one version** of each word. A [multi-version STM](/multi-version-stm/) can give a reader an old version that fits its snapshot instead.
- Each word has **metadata** that changes whenever the word does: a version number in an ownership record, or the value itself (value-based validation).
- The safety goal decides **when** to validate: at commit only for serializability of the committed transactions, and also during the run for opacity.

## The template

**Notation and model.** $n$ is the number of processes. A transaction reads $r$ words and writes $w$ words. Each word $a$ has a versioned lock $\ell(a)$ holding (version, owner), with owner free or a transaction. The STM uses atomic read, write, [compare-and-swap](/compare-and-swap/) (consensus number $\infty$) and [fetch-and-add](/fetch-and-add/) (consensus number 2), on a [sequentially consistent](/sequential-consistency/) memory. Writes go to a [redo log](/redo-log/) and the write locks are taken at commit ([commit-time locking](/commit-time-locking/)). Every committed write of a word gives its lock a higher version. A *check* is one look at the lock of one read-set entry.

The template has four policies in one place: *incremental* (scan at every read), *counter* (scan only when a global commit counter $C$ has moved), *clock* (TL2: compare each version with the start time $rv$ of a global clock $G$), and *commit* (scan only at commit, not opaque).

```pseudo id=main
READ(T, a)
L1  if a ∈ WS(T) then return WS(T)[a]                 ▷ read after write
L2  (v1, o1) ← ℓ(a); x ← M[a]; (v2, o2) ← ℓ(a)      ▷ a consistent single read
L3  if o1 ≠ free or (v1, o1) ≠ (v2, o2) then ABORT
L4  if policy = clock and v1 > rv then ABORT         ▷ one O(1) check, no scan
L5  append (a, v1) to RS(T)
L6  if policy = incremental then VALIDATE(T, earlier entries of RS(T))
L7  if policy = counter then c ← C; if c ≠ last then VALIDATE(T, all of RS(T)); last ← c
    return x

VALIDATE(T, E)
L8  for each (b, v) in E: if ℓ(b) is owned by another, or its version ≠ v (clock: > rv), then ABORT

COMMIT(T)                                             ▷ read-only: skip, except under policy commit
L9  lock each word of WS(T) with CAS, or ABORT
L10 if policy = clock then wv ← FAA(G, 1) + 1; if policy = counter then FAA(C, 1)
L11 VALIDATE(T, all of RS(T))
L12 write back WS(T); release each lock with a higher version (clock: wv)
```

At the begin, the clock policy reads $rv \leftarrow G$ and the counter policy reads $last \leftarrow C$.

### Why a validated transaction sees a consistent state

Take the incremental policy, and let $t$ be the time of the second lock read at L2 of the newest read. Each earlier entry $(b, v)$ was read before $t$ and checked at L8 after $t$, and the check found version $v$ and no owner. Versions only grow, and a committer holds the lock while it writes $b$, so $b$ held the value read during the whole time from its read to its check, which contains $t$. The newest word held its value at $t$ by L3. So every value the transaction has read was in memory together at time $t$: it is the state after the transactions that committed before $t$, and the transaction can be placed right after them. This holds after every read, so even a transaction that later aborts has only seen consistent states. The same argument works for the counter policy, with $t$ the time of the read of $C$ that found a change, provided that a writer increments $C$ while it holds its locks and before it writes back.

The commit policy has no such point: between two reads, a writer can commit and change the first word, and the transaction goes on with a mixed state until its commit. Its commit still validates under the write locks, so the committed transactions are serializable, but the run is not opaque.

### The cost of incremental validation

**Claim.** A transaction that reads $r$ distinct words and writes at least one does exactly $r(r+1)/2$ checks under the incremental policy when it commits.

**Proof.** The $i$-th read appends the $i$-th entry and then checks the $i - 1$ earlier entries (L6). Over the $r$ reads this is $\sum_{i=1}^{r} (i - 1) = r(r-1)/2$ checks. The commit checks all $r$ entries (L11). The total is $r(r-1)/2 + r = r(r+1)/2$. $\square$

Each check is one shared read of a lock, so the shared steps of the transaction also grow as $\Theta(r^2)$. A read-only transaction skips the commit scan, since its last read already validated everything, and does $r(r-1)/2$ checks. The [DSTM](/dstm/) test `test_validation_checks_grow_quadratically` counts the same $r(r+1)/2$ for DSTM, which validates every opened object at each open and at commit.

This is not only a weakness of one design. Guerraoui and Kapałka (PPoPP 2008) prove that a *progressive* STM (one that aborts a transaction only on a real conflict) that keeps a single version, uses invisible reads and is opaque must in the worst case spend $\Omega(k)$ steps on a read, where $k$ is the number of objects. Kuznetsov and Ravi (2015) give a lower bound quadratic in the size of the read set for progressive opaque STMs with invisible reads, under their assumptions on disjoint-access parallelism. So an STM that wants constant-time reads must give up one of the conditions.

### How a global clock avoids it

The clock policy gives up progressiveness. At begin, the transaction reads $rv$ from a [global version clock](/global-version-clock/). A committer takes a new time $wv$ from the clock and stamps its locks with it. A read accepts a word only if its version is at most $rv$ (L4). All accepted values were written by transactions that committed before the clock passed $rv$, and none was overwritten before the read, so the values form the state at time $rv$, and no scan is needed. Each read costs one check, and the commit checks each entry once: $r$ checks in all, $O(r)$ instead of $\Theta(r^2)$. The price is that the clock policy aborts a reader that meets any word written after its start, even when nothing it read has changed: a conflict that progressiveness would forbid. [TinySTM](/tinystm/) and LSA soften this by *extending* the snapshot: on meeting a newer version, they validate the read set once and, if it passes, move $rv$ forward.

## Classic examples

**Counts for one transaction.** A transaction reads $r$ words and writes one, alone. The test `test_incremental_validation_counts_r_r_plus_1_over_2` checks, for $r = 1, \dots, 10$:

| $r$ | incremental | counter | clock | commit |
|---|---|---|---|---|
| 1 | 1 | 1 | 1 | 1 |
| 4 | 10 | 4 | 4 | 4 |
| 8 | 36 | 8 | 8 | 8 |
| 10 | 55 | 10 | 10 | 10 |

The shared steps are $3r + r(r-1)/2 + 4 + r$ for the incremental policy and $3r + r + 6$ for the clock policy (the test `test_shared_steps_of_a_solo_run`): for $r = 8$, 64 against 38.

**The counter skips work.** An audit reads $a_0, a_1$; then a transfer between $a_2$ and $a_3$ commits; then the audit reads $a_2$ and $a_3$. Under the counter policy, the audit scans nothing for its first two reads, scans 3 entries after its read of $a_2$ (the counter has moved), and nothing after $a_3$. The incremental policy would have done $0 + 1 + 2 + 3 = 6$ checks. The test `test_counter_heuristic_scans_only_after_a_commit` runs this.

**Commit-only validation lets a zombie run.** With $a_0 = a_1 = 10$, an audit reads $a_0 = 10$; a transfer of 3 commits; the audit reads $a_1 = 13$ and has seen a total of 23. Its commit validation fails and it aborts, so the committed results are right, but for a while it ran on a state that never existed. The exhaustive search of `test_commit_only_validation_is_serializable_but_not_opaque` finds such a run, and checks that the committed transactions are strictly serializable in every interleaving. In the seeded bank runs of `test_bank_random_schedules`, audits that see a sum other than 30 occur only under the commit policy.

**Opacity of the other policies.** Exhaustive search over all interleavings of a transfer and an audit (each with up to two attempts), and of two writers and a two-word reader, finds only opaque histories for the incremental, counter and clock policies. Seeded random runs of transfers, audits and sorted-list operations keep the bank total and the list order.

## Variations

- **Value-based validation.** [NOrec](/norec/) records (address, value) pairs and validates by reading each address again and comparing values. It needs no per-word metadata, and it validates only when a global sequence lock has changed, which plays the role of the commit counter.
- **Validation at open.** Object-based STMs such as [DSTM](/dstm/) validate all opened objects each time a new object is opened.
- **Snapshot extension.** LSA and TinySTM keep a validity range $[lb, ub]$ and extend $ub$ by a validation when a read meets a newer version; most reads need no scan.
- **Visible reads.** Readers register in the metadata, and writers abort or wait for them; no validation is needed, but every read writes shared memory.
- **Sandboxing.** Validate only at commit and at a few dangerous points (before a store through a computed pointer, in loops, on a fault), as in the sandboxing of Dalessandro and Scott (2012); see [zombie transactions](/zombie-transactions/).
- **Multiple versions.** A reader that finds a newer version can use an older one instead of aborting ([multi-version STM](/multi-version-stm/)).

## Pitfalls

- **Validating only at commit.** The committed transactions are serializable, but a live transaction can see an inconsistent state, loop or fault. This is the zombie problem.
- **Forgetting the newest read in a lazy scan.** In the counter policy, when the counter has moved, the scan must include the entry just added. The first version of the code on this page scanned only the earlier entries and recorded the new counter value; the exhaustive test found a reader that read the old $x$, missed the commit that changed it, and then read the new $y$. The test keeps this variant as `check_new=False`.
- **The commit counter must move before write-back.** A writer that increments the counter after it writes back lets a reader see the new values while the counter still says that nothing changed.
- **ABA on values.** Value-based validation accepts a word that changed and changed back. This is safe for the reader, since the value is the same, but it means that a version check and a value check are not interchangeable in proofs.
- **Validation is not atomic.** The scan reads the locks one by one. The argument above works because each check confirms the word was unchanged from its read up to the check; a scan that only compares values without the lock can accept a state in the middle of another transaction's write-back.
- **Quadratic cost hidden in a library.** Incremental validation looks cheap for short transactions and makes long ones, such as a walk down a list of a thousand nodes, about 500 times slower.

## Exercises

1. Show that the incremental policy does exactly $r(r-1)/2$ checks for a read-only transaction of $r$ distinct reads, and find the count when the transaction reads the same word twice.
2. Under the counter policy, give a schedule with $k$ concurrent writers that makes a reader of $r$ words do $\Theta(r^2)$ checks, so that the heuristic does not improve the worst case.
3. Explain why the clock policy aborts a reader that the incremental policy would let commit, using one writer to a word the reader never reads.

## References
