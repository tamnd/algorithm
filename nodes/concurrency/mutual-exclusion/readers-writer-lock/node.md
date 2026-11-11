---
tag: ZZ28W3
kind: abstract-type
slug: readers-writer-lock
name: Readers-writer lock
aliases: [rwlock, shared-exclusive lock]
area: concurrency/mutual-exclusion
level: core
summary: A lock with a shared mode for readers and an exclusive mode for writers. Its policy (reader preference, writer preference, or fair) decides who can starve.
history:
  year: 1971
  people: [P. J. Courtois, F. Heymans, D. L. Parnas, John M. Mellor-Crummey, Michael L. Scott, Björn B. Brandenburg, James H. Anderson]
  note: Courtois, Heymans and Parnas (1971) gave reader and writer preference with semaphores. Mellor-Crummey and Scott (1991) gave local-spin queue versions, and Brandenburg and Anderson (2009) defined phase-fair locks.
prereqs: [mutex]
see_also: [readers-writers-problem, mutex, semaphore, starvation, ticket-lock, mcs-lock, read-copy-update, reentrant-lock]
sources:
  - paper: doi:10.1145/362759.362813
    title: P. J. Courtois, F. Heymans and D. L. Parnas, Concurrent control with "readers" and "writers", Communications of the ACM 14(10), 1971, pages 667-668
    locator: Problem 1 (readers have priority) and Problem 2 (writers have priority), with semaphores
  - paper: "John M. Mellor-Crummey and Michael L. Scott, Scalable reader-writer synchronization for shared-memory multiprocessors, Proceedings of the 3rd ACM SIGPLAN Symposium on Principles and Practice of Parallel Programming (PPoPP), 1991, pages 106-113"
    locator: the fair, reader preference and writer preference reader-writer locks built on a queue with local spinning
  - paper: "Björn B. Brandenburg and James H. Anderson, Reader-writer synchronization for shared-memory multiprocessor real-time systems, Proceedings of the 21st Euromicro Conference on Real-Time Systems (ECRTS), 2009"
    locator: task-fair and phase-fair reader-writer locks, and the bound on the blocking of readers under phase fairness
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 8, Monitors and Blocking Synchronization, Section 8.3, Readers-Writers Locks (the simple and the fair readers-writers lock)
  - url: "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/ReentrantReadWriteLock.html"
    title: Oracle, Java SE 21 API, class java.util.concurrent.locks.ReentrantReadWriteLock
    locator: the fair and nonfair modes, and the remarks that downgrading is allowed and upgrading is not
  - url: "https://pubs.opengroup.org/onlinepubs/9699919799/functions/pthread_rwlock_rdlock.html"
    title: The Open Group Base Specifications Issue 7 (POSIX.1-2008), pthread_rwlock_rdlock and pthread_rwlock_tryrdlock
    locator: the rule that it is implementation defined whether a reader gets the lock while writers are blocked
---

A readers-writer lock is a lock with two modes. Any number of *readers* may hold it at the same time in *shared* mode, and one *writer* may hold it alone in *exclusive* mode. It is the library form of a solution to the [readers-writers problem](/readers-writers-problem/), which states the requirements; this page is about the lock type, its policies and its implementations. Since readers do not change the data, letting them in together is safe, and it can give much more parallelism than a [mutex](/mutex/) when reads are common. The price is a *policy* question: when readers are inside and a writer waits, may a new reader enter? Each answer lets some process [starve](/starvation/).

## In plain words

Think of a notice board in a hall. Many people may read it at the same time, because reading does not change it. But when someone wants to change the board, nobody else may stand at it, so that no reader sees a half-written notice.

The hard part is the line. If readers keep coming, and each new reader may join those already reading, a person who wants to write may wait forever. If writers always go first, readers may wait forever. A fair rule takes people in the order they came, and lets readers who stand next to each other in the line go in together.

## Operations

**Model.** There are $n$ processes that share memory. The lock $L$ has a state: the set of readers that hold it, and the writer that holds it, if any. At the start nobody holds it.

| operation | effect | waits |
|---|---|---|
| `read_lock(L)` | the caller joins the readers | while a writer holds $L$, and maybe longer, by policy |
| `read_unlock(L)` | the caller leaves the readers | no |
| `write_lock(L)` | the caller becomes the writer | while a writer or any reader holds $L$, and maybe longer, by policy |
| `write_unlock(L)` | the writer leaves | no |
| `try_read_lock`, `try_write_lock` | as above, but return false instead of waiting | no |
| `downgrade(L)` (some locks) | the writer becomes a reader, with no gap | no |

POSIX names them `pthread_rwlock_rdlock`, `pthread_rwlock_wrlock` and `pthread_rwlock_unlock`, and Java has `readLock()` and `writeLock()` on `ReentrantReadWriteLock`.

**Policies.** The safety rule is the same for all locks. They differ in the order of entry:

| policy | rule while readers are inside and a writer waits | who can starve |
|---|---|---|
| reader preference | a new reader enters | writers |
| writer preference | a new reader waits; waiting writers go before waiting readers | readers |
| task fair | all requests are served in arrival order; neighboring readers share | nobody |
| phase fair | reader phases and writer phases alternate; at the end of a writer phase, all waiting readers enter together | nobody |

Courtois, Heymans and Parnas (1971) gave the first two with semaphores. Mellor-Crummey and Scott (1991) gave fair, reader preference and writer preference locks with local spinning, built on the queue of the [MCS lock](/mcs-lock/). Brandenburg and Anderson (2009) compared these policies for real-time systems and defined *phase fair* locks. In a task-fair lock, a reader can wait behind a long line of writers. In a phase-fair lock a reader waits for at most one writer phase and one reader phase, whatever the number of writers, and writers among themselves are served in order.

**Reader preference with a counter and a mutex.** The first solution of Courtois, Heymans and Parnas uses a counter $rc$, a binary semaphore `mutex` that guards it, and a binary semaphore `wrt` that the writers and the group of readers share:

```pseudo
READ-LOCK()
    P(mutex)
    rc ← rc + 1
    if rc = 1 then P(wrt)       ▷ the first reader locks out the writers
    V(mutex)

READ-UNLOCK()
    P(mutex)
    rc ← rc - 1
    if rc = 0 then V(wrt)       ▷ the last reader lets the writers in
    V(mutex)

WRITE-LOCK()      P(wrt)
WRITE-UNLOCK()    V(wrt)
```

*Why a writer is alone.* The semaphore `wrt` has one token. A writer inside holds it. A reader inside has raised $rc$ and released `mutex`; the first reader of the current group took the token before it released `mutex`, and the token goes back only when $rc$ falls to 0, which needs every reader inside to leave. So when a reader is inside, the reader group holds the token, and no writer can hold it. The test file checks this for every policy, with two readers and one writer and with one reader and two writers, and also checks that two readers really share the lock.

*Why the writer can starve.* While $rc > 0$, new readers enter without touching `wrt`. If two readers take turns so that one of them is always inside, $rc$ never falls to 0, and a waiting writer never gets `wrt`. The explorer finds this cycle for two readers and one writer. With a weak `wrt`, the first reader can also lose to the writer forever.

**Writer preference.** A monitor keeps the counts $readers$, $writer$ (0 or 1) and $waiting$ (the number of writers that wait). A reader enters when $writer = 0$ and $waiting = 0$. A writer adds 1 to $waiting$, and enters when $writer = 0$ and $readers = 0$. With two writers that take turns, $waiting$ is never 0, and the explorer finds that a reader starves.

**A task-fair lock from a ticket lock.** The lock in the Python file uses the [ticket lock](/ticket-lock/) for the line, and a counter $readers$ for the readers inside:

```pseudo
READ-LOCK()
    t ← FETCH-AND-ADD(next, 1)
    wait until serving = t
    FETCH-AND-ADD(readers, 1)
    serving ← t + 1             ▷ the next in line may be a reader too

READ-UNLOCK()     FETCH-AND-ADD(readers, -1)

WRITE-LOCK()
    t ← FETCH-AND-ADD(next, 1)
    wait until serving = t
    wait until readers = 0

WRITE-UNLOCK()    serving ← t + 1
```

A reader adds itself to $readers$ before it passes the turn on, so a writer that has its turn and then reads $readers = 0$ knows that every earlier reader has left, and no later process can pass, because $serving$ stays at the ticket of the writer. Requests are served in ticket order, so nobody starves, and the explorer confirms this for two readers and a writer and for a reader and two writers. This is a centralized lock: every waiter spins on $serving$. It is not the queue-based reader-writer lock of Mellor-Crummey and Scott (1991), which keeps the same fair policy but lets each waiter spin on its own queue node.

**Upgrade.** Some programs want to read, decide, and then write, without letting another writer in between. An `upgrade` operation would turn a reader into the writer when it is the only reader. Two readers that both call `upgrade` deadlock: each waits for the other to leave the reader set, and neither does. The test file shows that the explorer gets stuck in this way. Locks deal with it in one of three ways: they offer no upgrade (Java `ReentrantReadWriteLock` allows a downgrade from write to read, but not an upgrade); they let an upgrade fail, so that the caller must release, take the write lock, and check its data again; or they add a third *upgradable* mode that only one process may hold at a time, which shares with readers and excludes other upgraders.

## Laws

1. *Writer exclusion.* While a writer holds $L$, no other process holds it in either mode.
2. *Reader sharing.* A lock may let readers share. A lock that never lets two readers in at once satisfies law 1, but it is a mutex in disguise; a useful lock lets a reader in whenever only readers hold the lock and no writer waits.
3. *Memory order.* `write_unlock` is a release and every later `read_lock` or `write_lock` is an acquire, so a reader sees every write of the last writer before it. Two readers need no ordering between them.
4. *Policy decides starvation.* Reader preference can starve writers, writer preference can starve readers, and task-fair and phase-fair locks are starvation free if each critical section is finite.
5. *No upgrade without care.* Two readers that wait to become writers deadlock.
6. *Not wait free.* As with any lock, a holder that stops blocks the processes of the other mode.

## Implementations

| implementation | policy | waiting | notes |
|---|---|---|---|
| Courtois, Heymans and Parnas, Problem 1 | reader preference | semaphores | above; writers can starve |
| Courtois, Heymans and Parnas, Problem 2 | writer preference | semaphores | readers can starve |
| ticket lock and reader counter | task fair | spin on one word | in the Python file |
| Mellor-Crummey and Scott (1991) | fair, reader or writer preference | local spinning on a queue | each waiter spins on its own queue node |
| Brandenburg and Anderson (2009) | phase fair | spin | readers wait for at most one writer phase |
| Java `ReentrantReadWriteLock` | fair or nonfair | park | reentrant; downgrade allowed |
| POSIX `pthread_rwlock_t` | implementation defined | sleep | glibc prefers readers by default |
| [read-copy-update](/read-copy-update/) | readers never wait | none for readers | not a lock: readers see old versions while a writer works |

**The cost of the reader counter.** In every lock above, `read_lock` writes a shared counter or a queue node. On a cache-coherent machine this write moves the cache line, so readers on many cores slow each other down even though they never conflict. Locks for read-mostly data spread the reader count over per-core counters, at the price of a writer that must check all of them, or avoid shared writes by readers altogether, as read-copy-update does.

## Lower bounds

- A readers-writer lock in which every process is a writer is a mutex, so the lower bounds of the [mutex](/mutex/) hold: with reads and writes only, $n$ processes need at least $n$ shared registers, and with reads, writes and compare-and-swap some passage makes $\Omega(\log n)$ remote memory references (see [RMR complexity](/rmr-complexity/)).
- No lock is wait free: a writer that stops while it holds the lock blocks all readers.

## References
