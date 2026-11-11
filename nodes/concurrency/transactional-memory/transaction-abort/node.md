---
tag: CJ9VDQ
kind: concept
slug: transaction-abort
name: Transaction abort
aliases:
- transaction rollback
area: concurrency/transactional-memory
level: intro
summary: Discarding a transaction's tentative effects after a conflict or an explicit request, then retrying or giving up. Its causes, how an STM undoes the work, the retry policy and the wasted work.
prereqs: [transaction-conflict]
see_also: [contention-management, undo-log, redo-log, retry-and-orelse, transaction-irrevocability, zombie-transactions, livelock, best-effort-htm]
sources:
  - book: isbn:9781608452354
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Morgan and Claypool, 2010
    locator: Chapter 2 (aborts, conflict detection and contention management) and Chapter 4 (Software transactional memory)
  - paper: doi:10.1145/872035.872048
    title: "Maurice Herlihy, Victor Luchangco, Mark Moir and William N. Scherer III, Software transactional memory for dynamic-sized data structures, PODC 2003, pages 92-101"
    locator: aborting another transaction with one CAS on its status word, and the contention manager that decides when to do so
  - paper: doi:10.1007/11864219_14
    title: "Dave Dice, Ori Shalev and Nir Shavit, Transactional Locking II, DISC 2006, LNCS 4167, pages 194-208"
    locator: Section 2.1 (the cases in which a TL2 transaction aborts, and the retry of the transaction)
  - paper: doi:10.1145/1065944.1065952
    title: Tim Harris, Simon Marlow, Simon Peyton Jones and Maurice Herlihy, Composable memory transactions, PPoPP 2005
    locator: retry, which aborts the transaction on purpose and blocks it until a word it read changes
---

A transaction **aborts** when it ends without effect: the transactional memory throws away its tentative writes, releases what it holds, and reports that the transaction did not happen. In most systems the code of the transaction then runs again from the start, so for the programmer an abort is invisible except for the time it costs. Aborts are the price of optimism. A TM lets transactions run in parallel and aborts one of them when they turn out to [conflict](/transaction-conflict/), instead of making them wait for a lock in advance. This page lists the causes of aborts, shows what an STM does to undo a transaction, discusses when and how to retry, and measures the work that aborts waste.

## In plain words

A transaction is a try. If it meets another transaction on the same data and the system cannot keep both, one of them is cancelled. Cancelling means that no other thread ever sees any of its writes: either the writes were kept aside and are now dropped, or they were written in place and the old values are now put back. Then the cancelled transaction starts again. If two transactions keep cancelling each other, neither makes progress, so the system needs a rule for who goes first and how long to wait before the next try.

## The idea

**Notation and model.** $n$ is the number of processes. A transaction reads $r$ words and writes $w$ words. An *attempt* is one run of the transaction's code from begin to commit or abort. The STMs on this site are word-based, on a [sequentially consistent](/sequential-consistency/) memory with [compare-and-swap](/compare-and-swap/).

### The causes of an abort

1. **A conflict.** Another transaction wrote a word that this one read, or holds the lock of a word that this one wants. In [TL2](/tl2/) a read aborts when the lock of the word is held or its version is newer than the start time; the commit aborts when a write lock cannot be taken or a read fails [validation](/transaction-validation/). With [eager conflict detection](/eager-conflict-detection/) the abort comes at the access, with [lazy detection](/lazy-conflict-detection/) at commit.
2. **A decision of the contention manager.** When two transactions conflict, a [contention manager](/contention-management/) decides whether to wait, to abort itself, or to abort the other one. In [DSTM](/dstm/), a transaction aborts another by one CAS of the other's status word from ACTIVE to ABORTED.
3. **An explicit request.** The program asks to abort, for example Haskell's `retry` ([retry and orElse](/retry-and-orelse/)), which aborts the attempt and blocks until a word in its read set changes.
4. **A false conflict.** Two transactions that touch different words of one lock stripe look as if they conflict ([transaction conflict](/transaction-conflict/)).
5. **Limits of the system.** A [best-effort hardware TM](/best-effort-htm/) aborts when the read or write set does not fit in the cache, on an interrupt, or on some instructions. An STM with a bounded number of versions aborts a reader whose snapshot is gone ([multi-version STM](/multi-version-stm/)).
6. **Inconsistent state.** A transaction that detects that it has read an inconsistent state must abort at once, before the state does damage ([zombie transactions](/zombie-transactions/)).

### How an STM undoes an attempt

The work to undo depends on the [versioning](/software-transactional-memory/) policy.

| Policy | Memory at abort | Abort cost | Commit cost |
|---|---|---|---|
| lazy versioning ([redo log](/redo-log/)) | never changed | drop the log: no shared step | write back $w$ words |
| eager versioning ([undo log](/undo-log/)) | holds the new values | write back $w$ old values | drop the log |

In both cases the attempt also releases its locks or ownership records. A lock released after an in-place write that someone may have seen must get a new version, so that a reader who saw the undone value fails its validation; the [TinySTM](/tinystm/) test `test_write_through_abort_must_release_with_a_new_version` shows the run that goes wrong otherwise. Private state (the read and write sets, allocations made inside the attempt) is freed. Memory that the attempt freed is not really freed until commit, since an abort must be able to bring it back. Effects outside the memory, such as I/O, cannot be undone at all, which is why most TMs forbid them inside transactions or make the transaction [irrevocable](/transaction-irrevocability/).

### Retry

The simplest policy is to retry at once. Under contention this can [livelock](/livelock/): two transactions keep aborting each other and neither commits. The usual answers are:

- **Back-off.** Wait a random time before the next attempt, longer after each abort ([exponential back-off](/exponential-backoff/)).
- **Priorities.** Give an old or long transaction priority, so that it eventually wins: the [Greedy](/greedy-contention-manager/), [Karma](/karma-contention-manager/) and [Polka](/polka-contention-manager/) managers do this.
- **Fall back to a lock.** After $k$ aborts, run the transaction under a global lock or as an irrevocable transaction. Hardware TMs need this path, since a transaction that does not fit in the cache never commits in hardware.

### Waste

Each aborted attempt wastes the steps it took. With lazy detection a doomed transaction runs to its commit before it learns its fate; with eager detection it may stop earlier, but it may also abort for a conflict that would have gone away. A common measure is the *abort rate*, the number of aborts per commit, and the *wasted work*, the fraction of all steps spent in attempts that aborted.

## Examples

**Two increments.** $T$ and $U$ both run $x \leftarrow x + 1$ with $x = 0$, and both read $x = 0$. Under TL2, the first to commit takes the lock of $x$, writes $x = 1$ and releases it with a new version. The second then fails validation at its commit: the version of $x$ is newer than its start time. It aborts and retries, reads $x = 1$, and commits $x = 2$. The aborted attempt cost it about as many steps as the attempt that committed.

**Measured waste.** Four processes each run one transfer of 1 between two accounts, two in each direction, under a seeded random schedule; each process retries until it commits. Over 200 seeds (800 commits in all):

| STM | Steps of one transfer alone | Aborts per commit | Fraction of steps wasted |
|---|---|---|---|
| [TL2](/tl2/) | 16 | 3.67 | 0.57 |
| [TinySTM](/tinystm/), write-back | 16 | 3.65 | 0.57 |
| [NOrec](/norec/) | 9 | 0.87 | 0.49 |

The wasted fraction is $1 - 800 \cdot s / S$, where $s$ is the solo cost and $S$ the total number of steps. All four transactions touch the same two words, so this is close to the worst case. The table comes from the simulations on the STM pages; a random schedule is not a real machine, but it shows the effect: under high contention, more than half the work is thrown away. NOrec aborts less here because it validates by value and waits for a running commit instead of aborting.

**Explicit abort.** A transaction pops from an empty queue and calls `retry`. The attempt aborts, and the thread sleeps until another transaction writes a word that the attempt read, here the queue's head. Then the attempt runs again.

## Where it is used

- Every TM aborts: STMs in research and in Haskell and Clojure, hardware TMs such as [Intel TSX](/intel-tsx/), and [hybrid TMs](/hybrid-transactional-memory/).
- Database systems abort transactions for the same reasons: deadlock victims in [two-phase locking](/two-phase-locking/), failed validation in [optimistic concurrency control](/optimistic-concurrency-control/), and user aborts. A database abort undoes changes with an undo log, as in eager versioning, and must also be durable.
- [Transactional lock elision](/transactional-lock-elision/) treats an abort as a signal to take the real lock.

## References
