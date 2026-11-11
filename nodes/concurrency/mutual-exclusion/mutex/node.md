---
tag: CKW457
kind: abstract-type
slug: mutex
name: Mutex
aliases: [mutual exclusion lock, lock]
area: concurrency/mutual-exclusion
level: intro
summary: A lock object with lock, unlock and trylock. At most one process holds it at a time, and only the holder may unlock it.
history:
  year: 1965
  people: [Edsger W. Dijkstra, Hubertus Franke, Rusty Russell, Matthew Kirkwood, Ulrich Drepper]
  note: Dijkstra posed mutual exclusion in 1965. Linux futexes (Franke, Russell and Kirkwood 2002) let a mutex lock and unlock without a system call when there is no contention. Drepper described the three-state futex mutex in 2004.
prereqs: [mutual-exclusion-problem]
see_also: [spin-lock, semaphore, reentrant-lock, readers-writer-lock, condition-variable, monitor, test-and-set, ticket-lock]
sources:
  - url: "https://www.akkadia.org/drepper/futex.pdf"
    title: Ulrich Drepper, Futexes Are Tricky, Red Hat, version 1.6, November 2011 (first draft 2003; mutex3 added in 2004)
    locator: the sections Mutex, Take 1, Mutex, Take 2 and Mutex, Take 3, with the table of atomic operations and system calls
  - paper: "Hubertus Franke, Rusty Russell and Matthew Kirkwood, Fuss, futexes and furwocks: fast userlevel locking in Linux, Proceedings of the Ottawa Linux Symposium, 2002"
    locator: the futex design (a user space word with kernel wait queues)
  - url: "https://man7.org/linux/man-pages/man2/futex.2.html"
    title: futex(2), Linux manual page
    locator: FUTEX_WAIT and FUTEX_WAKE
  - url: "https://pubs.opengroup.org/onlinepubs/9699919799/functions/pthread_mutex_lock.html"
    title: The Open Group Base Specifications Issue 7 (POSIX.1-2008), pthread_mutex_lock, pthread_mutex_trylock, pthread_mutex_unlock
    locator: the mutex types NORMAL, ERRORCHECK, RECURSIVE and DEFAULT, and the errors EBUSY, EDEADLK and EPERM
  - url: "https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf"
    title: ISO/IEC 9899:201x (C11) committee draft N1570
    locator: Section 7.26.4, Mutex functions (mtx_lock synchronizes with prior mtx_unlock)
  - paper: "Anna R. Karlin, Kai Li, Mark S. Manasse and Susan Owicki, Empirical studies of competitive spinning for a shared-memory multiprocessor, SOSP 1991"
    locator: spinning for about the cost of a block before blocking, and its competitive ratio
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 2, Mutual Exclusion, and Chapter 7, Spin Locks and Contention
---

A mutex is a shared object that solves the [mutual exclusion problem](/mutual-exclusion-problem/) as a library type: `lock` waits until the caller holds the mutex, `unlock` gives it back, and `trylock` takes it only if it is free. At most one process holds a mutex at a time, and only the holder may release it. A waiting process either spins on shared memory or sleeps in the operating system; most real mutexes, such as the futex-based mutex of Linux, do both, and take no system call at all when there is no contention.

## In plain words

A mutex is the key to a room that only one person may use. To enter, you take the key from its hook. If the hook is empty, you wait. When you leave, you hang the key back. Only the person who took the key may hang it back.

There are two ways to wait. You can stand at the hook and look at it again and again, which is quick when the wait is short but wastes your time when it is long. Or you can sit down and ask to be called when the key is back, which saves effort but costs time to get up again. Good mutexes look a few times and then sit down.

## Operations

**Model and notation.** There are $n$ processes (threads) $p, q, \ldots$ that run asynchronously and share memory. The mutex is one shared object $M$ with a state that is either *free* or *held by* $p$. Processes call its operations in their entry and exit sections:

| operation | precondition | effect | waits |
|---|---|---|---|
| `lock(M)` by $p$ | $p$ does not hold $M$ | when $M$ is free, $M$ becomes held by $p$ | yes, while $M$ is held |
| `unlock(M)` by $p$ | $p$ holds $M$ | $M$ becomes free | no |
| `trylock(M)` by $p$ | $p$ does not hold $M$ | if $M$ is free, it becomes held by $p$ and the call returns true; otherwise it returns false | no |

POSIX names them `pthread_mutex_lock`, `pthread_mutex_unlock` and `pthread_mutex_trylock`, C11 names them `mtx_lock`, `mtx_unlock` and `mtx_trylock`, and Java has `lock`, `unlock` and `tryLock` on `java.util.concurrent.locks.Lock`. Some mutexes also offer a timed lock that gives up after a deadline.

**Ownership.** A mutex has an owner, which is what separates it from a binary [semaphore](/semaphore/), which any process can signal. POSIX leaves the behavior undefined if a process unlocks a default mutex that it does not hold, and the error-checking type returns `EPERM`. A second `lock` by the owner deadlocks a normal mutex, returns `EDEADLK` for an error-checking mutex, and succeeds for a recursive mutex, which keeps a count (see [reentrant lock](/reentrant-lock/)).

**Blocking versus spinning.** A *spin lock* waits by reading shared memory in a loop until the mutex is free (see [spin lock](/spin-lock/) and [test-and-set](/test-and-set/)). It reacts fast, but it uses a processor for the whole wait, and if the holder is not running (it was preempted), the spinner wastes its whole time slice. A *blocking* mutex puts the waiter to sleep in the kernel and wakes it at unlock. Sleeping and waking cost two system calls and two context switches, which is much longer than a short critical section. So many mutexes are *adaptive*: they spin for a bounded time, then block. Karlin, Li, Manasse and Owicki (1991) study this choice; if a process spins for as long as a block costs and then blocks, it pays at most twice the cost of the best choice made with knowledge of the wait.

**Futexes.** Linux provides the futex, a "fast user space mutex" (Franke, Russell and Kirkwood 2002). It is an aligned integer in user memory plus two system calls. `futex_wait(a, v)` checks, atomically with respect to `futex_wake`, that the word at `a` still holds `v`, and then sleeps; if the word holds another value it returns at once. `futex_wake(a, k)` wakes at most `k` sleepers on `a`. The word holds the state of the mutex, and atomic instructions on it decide the uncontended cases in user space, so a system call is needed only when a thread must sleep or must wake a sleeper.

**Drepper's three-state mutex.** Drepper ("Futexes Are Tricky", Mutex, Take 3) gives this mutex. The word `val` is 0 (free), 1 (held, no waiter) or 2 (held, waiters possible):

```pseudo
LOCK()
    c ← CAS(val, 0, 1)                 ▷ returns the old value
    if c ≠ 0 then
        if c ≠ 2 then c ← XCHG(val, 2)
        while c ≠ 0 do
            FUTEX-WAIT(val, 2)          ▷ sleeps only if val is still 2
            c ← XCHG(val, 2)

UNLOCK()
    if ATOMIC-DEC(val) ≠ 1 then         ▷ the old value was 2: someone may sleep
        val ← 0
        FUTEX-WAKE(val, 1)
```

Without contention, `lock` is one compare-and-swap that changes 0 to 1, and `unlock` is one atomic decrement that changes 1 to 0: two atomic instructions and no system call. The test file counts exactly that. A waiter always writes 2 before it sleeps, and it sleeps only while the word is still 2, so the next unlock sees the old value 2 and calls `futex_wake`. That is the reason that no wakeup is lost. A thread that wakes up writes 2 again, because it cannot know whether others still sleep; this can cost one needless `futex_wake` later, but it is never wrong.

## Laws

1. *Mutual exclusion.* In every history, between a `lock` (or a successful `trylock`) of $p$ and the next `unlock` of $p$, no other `lock` or `trylock` succeeds.
2. *Ownership.* Only the holder calls `unlock`. A call by another process is an error, not a release.
3. *Trylock does not wait.* `trylock` returns in a bounded number of the caller's steps. It returns false only if the mutex was held, and POSIX then reports `EBUSY`.
4. *Progress.* A correct mutex is at least deadlock free: if the mutex is free and some processes call `lock`, one of them returns. POSIX does not require starvation freedom, and the futex mutex above does not give it: a thread that returns from `futex_wait` can lose the race to a newcomer each time. The test file finds such a run for two threads. A fair mutex, such as a [ticket lock](/ticket-lock/), gives each waiter its turn in FCFS order, at a cost in throughput.
5. *Memory ordering.* `unlock` is a release and `lock` is an acquire: in C11, a call to `mtx_lock` synchronizes with prior calls to `mtx_unlock` on the same mutex (N1570, Section 7.26.4). So every write that one holder made in its critical section is visible to the next holder. This is the property that makes data guarded by a mutex free of data races (see [race condition](/race-condition/)).
6. *No wait freedom.* A process that holds the mutex and stops forever blocks every process that calls `lock`. No implementation can avoid this, because the specification of `lock` makes the caller wait while the mutex is held.

The `MutexSpec` class in the Python file is the sequential specification of laws 1 to 3: a test runs it and checks the errors for relock and for unlock by a non-owner.

## Implementations

| implementation | primitive | uncontended cost | waiting | fair |
|---|---|---|---|---|
| [Peterson](/peterson-algorithm/), [bakery](/lamport-bakery-algorithm/) | reads and writes | $O(1)$ or $O(n)$ steps | spin | yes |
| [test-and-set](/test-and-set/) lock | test-and-set | 1 atomic, 1 write | spin | no |
| [ticket lock](/ticket-lock/) | fetch-and-add | 1 atomic, 1 read, 1 write | spin | FCFS |
| [Anderson](/anderson-lock/), [MCS](/mcs-lock/), [CLH](/clh-lock/) | fetch-and-add or swap, CAS | a few atomics | local spin | FCFS |
| Drepper's mutex3 | CAS, swap, decrement, futex | 2 atomics, 0 system calls | sleep | no |
| Drepper's Take 1 | increment, futex | 1 atomic, 1 write, 1 system call | sleep | no |

**Drepper's Take 1.** The first attempt in Drepper's paper keeps a counter: `lock` increments it and sleeps with `futex_wait(val, c + 1)` unless the old value was 0, and `unlock` writes 0 and always calls `futex_wake`. The explorer finds it safe for two threads, but every unlock makes a system call, even with no waiter, and Drepper points out two more bugs: the waiters change the word all the time, so a `futex_wait` can fail again and again (a livelock), and the counter can overflow.

**A broken variant.** Suppose that a waiter does not write 2 and sleeps on the value 1: `c ← CAS(val, 0, 1)`, and while `c ≠ 0`, `FUTEX-WAIT(val, 1)` and try again. Then `unlock` always sees the old value 1 and never calls `futex_wake`. The test file finds the lost wakeup in 7 steps: thread 0 takes the mutex, thread 1 fails its compare-and-swap and sleeps on the value 1, and thread 0 unlocks and leaves. The mutex is free and thread 1 sleeps forever. The checker finds 4 such states out of 61 for two threads.

**Mutexes in practice.** POSIX threads on Linux (glibc) build `pthread_mutex_t` on futexes, with a word that tells whether there may be waiters, in the same way as mutex3. Java's `ReentrantLock` keeps a queue of parked threads and offers a fair and an unfair mode. Many kernels and runtimes spin for a short time before they block.

## Lower bounds

- With atomic reads and writes only, a deadlock-free mutex for $n$ processes needs at least $n$ shared registers (Burns and Lynch 1993). See [mutual exclusion lower bounds](/mutual-exclusion-lower-bounds/).
- With reads, writes and compare-and-swap, some passage makes $\Omega(\log n)$ remote memory references in the worst case (Attiya, Hendler and Woelfel 2008), in the CC and the DSM models. With fetch-and-add or swap, the queue locks make $O(1)$ RMRs per passage. The page [RMR complexity](/rmr-complexity/) explains the models.
- No mutex is wait free, by law 6. A process that holds a mutex and is preempted makes every other caller wait, which is the problem that the [non-blocking](/non-blocking-algorithm/) objects avoid.

## References
