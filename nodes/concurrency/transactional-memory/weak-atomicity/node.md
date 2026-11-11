---
tag: NZDH5H
kind: definition
slug: weak-atomicity
name: Weak atomicity
aliases:
- weak isolation
area: concurrency/transactional-memory
level: advanced
summary: A TM is weakly atomic if transactions are atomic only with respect to other transactions; a plain load or store can see or change the inside of a running transaction.
prereqs: [transaction, race-condition, serializability]
see_also: [strong-atomicity, privatization-safety, opacity, lazy-versioning, eager-versioning, hardware-transactional-memory, read-barrier, write-barrier]
sources:
  - paper: doi:10.1109/L-CA.2006.18
    title: "Colin Blundell, E Christopher Lewis and Milo M. K. Martin, Subtleties of transactional memory atomicity semantics, IEEE Computer Architecture Letters 5(2), 2006"
    locator: the names strong atomicity and weak atomicity, and the examples where the choice changes the behavior of a program
  - paper: doi:10.1145/1250734.1250744
    title: "Tatiana Shpeisman, Vijay Menon, Ali-Reza Adl-Tabatabai, Steven Balensiefer, Dan Grossman, Richard L. Hudson, Katherine F. Moore and Bratin Saha, Enforcing isolation and ordering in STM, PLDI 2007, pp. 78 to 88"
    locator: the list of anomalies of weakly atomic STMs (non-repeatable read, intermediate lost update, intermediate dirty read, speculative lost update, speculative dirty read, granular lost update)
  - paper: doi:10.1145/1378533.1378588
    title: "Vijay Menon, Steven Balensiefer, Tatiana Shpeisman, Ali-Reza Adl-Tabatabai, Richard L. Hudson, Bratin Saha and Adam Welc, Practical weak-atomicity semantics for Java STM, SPAA 2008, pp. 314 to 325"
    locator: single global lock atomicity and the weaker semantics proposed for Java STM
  - book: doi:10.1007/978-3-031-01728-5
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Synthesis Lectures on Computer Architecture, 2010
    locator: Chapter 2 (Basic transactions, the section on weak and strong isolation)
---

**Weak atomicity** (also called weak isolation) is the guarantee that a transaction is atomic and isolated only with respect to other transactions. A load or store outside any transaction is not checked, so it can see the partial state of a running transaction, and a running transaction can see or lose a plain store. The names weak atomicity and [strong atomicity](/strong-atomicity/) come from Blundell, Lewis and Martin (2006). Most software TMs are weakly atomic because checking every plain access costs too much; their users must keep shared data that transactions use away from plain code, or follow rules such as [privatization safety](/privatization-safety/).

## Definition

**Model.** Processes run on a shared memory of words. A process runs *transactions* (each a sequence of reads and writes that ends in a commit or an abort) and *plain accesses* (single reads and writes outside any transaction). An execution is a sequence of these events. Two events *conflict* if they access the same word and at least one of them writes. A plain access and a transaction are *concurrent* if the access happens after the transaction begins and before it commits or aborts (including the write-back or rollback that the TM does after the commit or abort).

**Weak atomicity.** A TM is *weakly atomic* if, for every execution, the transactional events alone satisfy the TM's correctness condition (for example [serializability](/serializability/) of committed transactions, or [opacity](/opacity/)), and the TM gives no guarantee about a plain access that conflicts with a concurrent transaction.

More precisely, remove all plain accesses from the execution; the transactions that remain must look as if they ran one at a time. A plain access is guaranteed to read the latest committed value only if no transaction that conflicts with it is concurrent with it. In the other case the value it reads, and the effect it has on the transaction, depend on the TM.

**Race freedom.** A program is *transactionally race free* if, in every execution under a serial semantics, no plain access conflicts with a concurrent transaction. The useful contract of a weakly atomic TM is: a program that is race free in this sense behaves as if every transaction ran alone. For programs with races, a weakly atomic TM can show the anomalies below. Menon et al. make this contract exact with *single global lock atomicity* (SGLA): a program must behave as if every atomic block took one global lock. The idioms of privatization and publication are race free under SGLA, so an SGLA TM must handle them, and many weakly atomic STMs need extra work to do so.

**Notation for the anomalies.** In each case below, $X$ starts at 0, process $p$ runs one transaction and process $q$ makes one plain access. The names are those of Shpeisman et al. (2007).

## Examples and non-examples

**Non-repeatable read (NR).** $p$ runs `atomic { a ← X; b ← X }` and $q$ runs `X ← 1`. A weakly atomic TM can commit $p$ with $a = 0$ and $b = 1$: the plain store does not change the version of $X$, so a version check at the second read does not see it. No serial order gives $a \ne b$.

**Intermediate lost update (ILU).** $p$ runs `atomic { X ← X + 1 }` and $q$ runs `X ← 10`. The serial results are 10 and 11.

| step | $p$ (transaction, redo log) | $q$ (plain) | $X$ |
|---|---|---|---|
| 1 | read $X = 0$, buffer $X \leftarrow 1$ | | 0 |
| 2 | | $X \leftarrow 10$ | 10 |
| 3 | lock, validate (the version of $X$ did not change), write back $X \leftarrow 1$ | | 1 |

The plain store is lost. An eager TM loses it in the same way, with the write in place at step 3.

**Intermediate dirty read (IDR).** $p$ runs `atomic { X ← 1; X ← 2 }` and $q$ reads $X$. An eager TM writes in place, so $q$ can read 1, a value that no committed state ever had. A TM with a redo log writes only the final value 2, so it does not have this anomaly.

**Speculative lost update and speculative dirty read (SLU, SDR).** These are the eager cases where the transaction later aborts: the rollback from the undo log overwrites a plain store made in the meantime (SLU), or a plain load reads a value that the aborted transaction wrote (SDR). The doomed-transaction run on the [privatization safety](/privatization-safety/) page is a lost update of this kind.

**Granular lost update (GLU).** Words 0 and 1 are in the same block (one ownership record, one cache line or one object). $p$ runs `atomic { word0 ← 1 }` and $q$ runs `word1 ← 5`, so there is no race at the level of words. A TM that buffers or logs whole blocks reads the block at the first transactional write and writes the whole block back at commit, so it can restore word 1 to 0. The anomaly disappears if the TM logs single words, or with strong atomicity.

**Non-example: race-free programs.** If every word that a transaction touches is touched outside transactions only when no transaction that uses it can run, a weakly atomic TM gives serial behavior. In each anomaly above, the plain access is concurrent with a conflicting transaction, so each program has a race.

**Non-example: hardware TM.** On most hardware TMs a plain store to a cache line in the read or write set of a running transaction causes a coherence conflict and aborts the transaction (see [best-effort HTM](/best-effort-htm/)). The anomalies above do not occur, so these hardware TMs are strongly atomic for plain accesses.

**Checked on a model.** The implementation for this page builds the NR, ILU, GLU and IDR programs on a small TL2-like STM (redo log, block versions) and on an eager STM (in-place writes, undo log), and runs all interleavings of the two processes. With weak atomicity, NR and ILU appear on both STMs, GLU on the redo-log STM with two words per block, and IDR on the eager STM. With strong atomicity, where each plain access waits for the block lock and a plain store bumps the block version, no interleaving shows an anomaly.

## Related definitions

- **[Strong atomicity](/strong-atomicity/).** Every plain access acts as a transaction of one access, so the anomalies cannot occur. It costs a [read barrier](/read-barrier/) or [write barrier](/write-barrier/) on plain accesses, or hardware support.
- **Single global lock atomicity (SGLA).** Between weak and strong: race-free programs under the global lock semantics behave correctly, including the privatization and publication idioms; racy programs get no guarantee. Menon et al. also study weaker variants that are cheaper to implement in a Java STM.
- **[Privatization safety](/privatization-safety/).** The property that the race-free privatization idiom works on a given weakly atomic TM. Delayed write-back and doomed transactions break it, even though the program has no race.
- **[Opacity](/opacity/)** and serializability speak only about transactional events, so they are silent about plain accesses. A TM can be opaque and weakly atomic.
- **Data races in memory models.** The contract "race-free programs behave as if serial" is the transactional form of the data-race-free guarantee of a language memory model; see [race condition](/race-condition/) for the general notion.
- **Locks versus transactions.** Blundell, Lewis and Martin also point out that a program that works with locks does not always work when each critical section becomes an atomic block. For example, a critical section that waits for a flag that another thread sets can wait forever as a transaction, because a transaction does not see a new value in the middle of its run. Under strong atomicity this is true even when the other thread sets the flag outside any transaction, so strong atomicity is not simply "weak atomicity with fewer surprises".

## References
