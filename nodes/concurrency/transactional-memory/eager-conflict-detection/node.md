---
tag: XAJX4E
kind: concept
slug: eager-conflict-detection
name: Eager conflict detection
aliases:
- early conflict detection
- pessimistic conflict detection
area: concurrency/transactional-memory
level: advanced
summary: Detecting a conflict at the access that causes it, so a doomed transaction stops early. It wastes less work per abort but can abort transactions that could both have committed.
prereqs: [transaction-conflict, software-transactional-memory]
see_also: [lazy-conflict-detection, encounter-time-locking, eager-versioning, contention-management, swisstm, tinystm, dstm, transaction-abort]
sources:
  - paper: doi:10.1007/11864219_13
    title: "Michael F. Spear, Virendra J. Marathe, William N. Scherer III and Michael L. Scott, Conflict detection and validation strategies for software transactional memory, DISC 2006, LNCS 4167, pages 179-193"
    locator: the comparison of eager, lazy and mixed acquisition, and of visible and invisible reads
  - book: isbn:9781608452354
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Morgan and Claypool, 2010
    locator: Chapter 2 (conflict detection, eager and lazy) and Chapter 4 (Software transactional memory)
  - paper: doi:10.1145/872035.872048
    title: "Maurice Herlihy, Victor Luchangco, Mark Moir and William N. Scherer III, Software transactional memory for dynamic-sized data structures, PODC 2003, pages 92-101"
    locator: an STM that acquires an object for writing when it opens it, and calls the contention manager at that moment
  - paper: doi:10.1145/1542476.1542494
    title: "Aleksandar Dragojević, Rachid Guerraoui and Michał Kapałka, Stretching transactional memory, PLDI 2009, pages 155-165"
    locator: eager detection of write-write conflicts with lazy detection of read-write conflicts
---

**Eager conflict detection** finds a [transaction conflict](/transaction-conflict/) at the moment of the access that creates it: when a transaction writes a word that another live transaction has read or written, or reads a word that another live transaction has written. The STM then resolves the conflict at once, by making one of the two transactions wait or [abort](/transaction-abort/). It is one end of the conflict detection axis of [software transactional memory](/software-transactional-memory/); the other end is [lazy conflict detection](/lazy-conflict-detection/), which finds conflicts only at commit. Eager detection stops a doomed transaction early and so wastes less work per abort. Its cost is that it may abort a transaction that would have committed, because the conflict would have resolved itself. Spear, Marathe, Scherer and Scott (DISC 2006) compared the choices and found that neither wins on all workloads; a *mixed* policy, eager for write-write conflicts and lazy for read-write conflicts, did well, and [SwissTM](/swisstm/) later built on it.

## In plain words

Two transactions want the same data and at least one wants to change it. With eager detection, the system notices this the moment the second one touches the data, and it decides then and there which one goes on. The other one stops at once, which saves the work it would have done. But sometimes the system is too quick: if the first transaction had simply finished first, both could have succeeded, and the stop was not needed.

## The idea

**Notation and model.** $n$ is the number of processes, $r$ and $w$ the numbers of words a transaction reads and writes. The STM has per-word or per-stripe metadata, updated with [compare-and-swap](/compare-and-swap/), on a [sequentially consistent](/sequential-consistency/) memory.

### What it takes to detect a conflict at the access

A conflict involves two accesses. For the second access to see the first, the first must leave a trace in shared metadata:

| Conflict, in access order | Trace left by the first access | Eager detection possible |
|---|---|---|
| write, then write (WW) | the first writer holds a write lock | yes, at the second write |
| write, then read (WR) | the writer holds a write lock | yes, at the read |
| read, then write (RW) | nothing, if reads are invisible | only with *visible reads* |

So eager detection of write conflicts comes almost for free with [encounter-time locking](/encounter-time-locking/): the write lock taken at the first write is the trace. Eager detection of read-write conflicts needs *visible reads*: each reader registers itself, for example in a reader list or a reader counter of the word, so that a later writer can find it. That costs a shared write per read and much cache traffic, so most STMs keep reads invisible. With invisible reads, the reader finds an RW conflict later, when it [validates](/transaction-validation/): at its next read in an STM with a [global version clock](/global-version-clock/), or at its commit.

Strictly, then, few STMs are fully eager. The usual "eager" STM is eager for WW and WR conflicts and lazy for RW conflicts in which the reader came first.

### What happens at a detected conflict

When a transaction finds that another live transaction owns the word, it asks its [contention manager](/contention-management/). The choices are: abort itself, wait a little and look again, or abort the owner. In [DSTM](/dstm/) the attacker can abort the owner with one CAS of the owner's status. In [TinySTM](/tinystm/) the default is that the transaction that finds the lock aborts itself. In [SwissTM](/swisstm/), short transactions abort themselves and long ones use a Greedy rule.

### The trade

- **Less waste per abort.** A doomed transaction stops at its conflicting access, not at its commit.
- **More aborts.** The transaction that holds the word may abort later for another reason, or the conflict may not break serializability at all (two blind writes, or a reader that could commit first). Eager detection treats every such conflict as fatal.
- **Risk of livelock.** Two transactions that keep aborting each other at their first access make no progress, so a contention manager with back-off or priorities is essential.
- **Fits eager versioning.** With [eager versioning](/eager-versioning/), WW and WR conflicts must be detected eagerly, since memory holds uncommitted values under the lock.

## Examples

The runs below come from the simulations of the [TL2](/tl2/), [TinySTM](/tinystm/) and [SwissTM](/swisstm/) pages, with each transaction allowed one attempt.

**A write-write conflict that did not matter.** Memory has $x = 0$ and words $a_0, \dots, a_4$. $T_1$ writes $x \leftarrow 1$ (a blind write) and then reads $a_0, \dots, a_4$. Right after $T_1$'s write, $T_2$ runs alone: it writes $x \leftarrow 2$ and commits, or in a second run it reads $x$ and writes $x \leftarrow x + 10$.

| STM | Detection of WW | $T_2$ | $T_1$ | Final $x$ |
|---|---|---|---|---|
| TL2 | lazy (locks at commit) | commits | commits | 1 |
| TinySTM | eager (lock at write) | aborts at its first access | commits | 1 |
| SwissTM | eager (lock at write) | aborts at its write | commits | 1 |

The serial order "$T_2$ then $T_1$" explains the TL2 run, and the checker confirms it is opaque. The eager STMs abort $T_2$ although both could commit. In the TinySTM run $T_2$ takes 2 steps before it aborts at the blind write and 4 steps in the read-modify-write case; under retries it would abort again and again until $T_1$ ends. The tests `test_encounter_time_locking_finds_a_write_write_conflict_at_the_write` (TinySTM) and `test_eager_write_write_detection` (SwissTM) show the same detection.

**A doomed reader, found late in both.** $T_1$ reads $x$, then reads $a_0, \dots, a_4$, then writes $y$. After $T_1$'s read of $x$, $T_2$ writes $x \leftarrow 7$ and commits. Reads are invisible in all three STMs, so $T_2$ does not see $T_1$, and $T_1$ does not learn of the conflict until its commit validation. It takes 20 more steps in TL2 and TinySTM (31 in SwissTM) and then aborts. A visible-read STM would have let $T_2$ see $T_1$ and decide at $T_2$'s write.

## Where it is used

- [DSTM](/dstm/) (2003), which acquires an object for writing when it opens it.
- [TinySTM](/tinystm/) (2008) and the McRT STM (2006), with encounter-time write locks.
- [SwissTM](/swisstm/) (2009): eager for write-write, lazy for read-write conflicts.
- Most hardware TMs detect conflicts eagerly through the cache coherence protocol: a remote request for a line in the read or write set of a transaction aborts it at once ([hardware transactional memory](/hardware-transactional-memory/), [Intel TSX](/intel-tsx/)).
- In databases, [two-phase locking](/two-phase-locking/) is the pessimistic analogue: a conflict blocks the requester at the access.

## References
