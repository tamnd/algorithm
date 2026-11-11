---
tag: 09YRQ0
kind: abstract-type
slug: reentrant-lock
name: Reentrant lock
aliases: [recursive mutex]
area: concurrency/mutual-exclusion
level: core
summary: A mutex that records its owner and a hold count, so the owner may lock it again without deadlock. It is free again after as many unlocks as locks.
history:
  year: 2004
  people: [Doug Lea, David R. Butenhof]
  note: Java monitors were reentrant from the start, and Java 5 (2004) added ReentrantLock from the JSR 166 work led by Doug Lea. POSIX has the recursive mutex type, which Butenhof (1997) advised against.
prereqs: [mutex]
see_also: [mutex, semaphore, monitor, condition-variable, readers-writer-lock, deadlock, lock-ordering, spin-lock]
sources:
  - url: "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/ReentrantLock.html"
    title: Oracle, Java SE 21 API, class java.util.concurrent.locks.ReentrantLock
    locator: the class description (owner, hold count, fairness, the limit of 2147483647 recursive locks) and the methods getHoldCount, isHeldByCurrentThread and newCondition
  - url: "https://pubs.opengroup.org/onlinepubs/9699919799/functions/pthread_mutex_lock.html"
    title: The Open Group Base Specifications Issue 7 (POSIX.1-2008), pthread_mutex_lock, pthread_mutex_trylock, pthread_mutex_unlock
    locator: the type PTHREAD_MUTEX_RECURSIVE, its lock count, and the error for an unlock by a thread that is not the owner
  - book: isbn:9780201633924
    title: David R. Butenhof, Programming with POSIX Threads, Addison-Wesley, 1997
    locator: Chapter 5, Advanced threaded programming, the mutex attributes and the remarks on recursive mutexes
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 8, Monitors and Blocking Synchronization, Section 8.4, a reentrant lock built from a lock and a condition
  - url: "https://en.cppreference.com/w/cpp/thread/recursive_mutex"
    title: cppreference.com, std::recursive_mutex (C++11)
    locator: the description of ownership levels and the unspecified maximum number of levels
  - url: "https://docs.python.org/3/library/threading.html#rlock-objects"
    title: Python documentation, threading, RLock objects
    locator: the owning thread and the recursion level
---

A reentrant lock, also called a recursive mutex, is a [mutex](/mutex/) that its owner may lock again while it already holds it. The lock records which thread owns it and how many times that thread has locked it, the *hold count*. A `lock` by the owner only increases the count, and an `unlock` decreases it; the lock is free again when the count falls to 0. With a plain mutex, a second `lock` by the owner waits for itself forever, or is an error.

## In plain words

Think of a room key with a tally sheet. When you take the key, your name goes on the sheet with one mark. If you need the key again while you still have it, for example because one job inside the room calls another job that also asks for the key, you just add a mark. Each time you finish a job, you erase one mark. When the last mark is gone, the key goes back on its hook for others.

Only the person whose name is on the sheet may add or erase marks. Others still wait for the key, as with an ordinary lock.

## Operations

**Model.** There are $n$ threads that share memory. A reentrant lock $R$ has a state $(owner, count)$, where $owner$ is a thread or $\bot$ and $count \ge 0$, with $owner = \bot$ exactly when $count = 0$. At the start the state is $(\bot, 0)$.

| operation by thread $t$ | effect | waits |
|---|---|---|
| `lock(R)` | if $owner = t$, then $count \leftarrow count + 1$; else wait until $owner = \bot$, then $(owner, count) \leftarrow (t, 1)$ | only while another thread owns $R$ |
| `unlock(R)` | if $owner \ne t$, error; else $count \leftarrow count - 1$, and if $count = 0$ then $owner \leftarrow \bot$ | no |
| `trylock(R)` | as `lock`, but return false at once instead of waiting | no |
| `holdCount(R)` | return $count$ if $owner = t$, else 0 | no |

**Java.** `java.util.concurrent.locks.ReentrantLock` has `lock`, `unlock`, `tryLock`, `getHoldCount` and `isHeldByCurrentThread`. An `unlock` by a thread that does not hold the lock throws `IllegalMonitorStateException`. The constructor `ReentrantLock(true)` gives a fair lock that favors the thread that waited longest, and the default is unfair. The documentation sets a limit of 2147483647 recursive locks by one thread. Java's built-in monitors (`synchronized`) are reentrant too.

**POSIX.** A mutex created with the type `PTHREAD_MUTEX_RECURSIVE` keeps a lock count. A relock by the owner succeeds, the mutex is released after as many unlocks as locks, and an unlock by a thread that is not the owner returns an error. The types `PTHREAD_MUTEX_NORMAL` and `PTHREAD_MUTEX_ERRORCHECK` deadlock on a relock or return `EDEADLK`. C++ has `std::recursive_mutex`, Python has `threading.RLock`, and a Windows critical section is reentrant.

**Why reentrancy is wanted.** A class whose public methods take the lock, and that call each other, would deadlock on a plain mutex. Callbacks into the same object and recursive algorithms over a locked structure have the same issue. A reentrant lock makes such code work without changes.

**Butenhof's warning, an opinion.** Butenhof, who took part in the design of POSIX threads, argues that recursive mutexes are a poor tool. His reasoning: the point of a lock is that the code between `lock` and `unlock` may assume the invariants of the data it guards, and a nested `lock` gives no such point, because the outer caller may be in the middle of an update with the invariants broken. He advises to split each operation into a public function that takes the lock and an internal function that assumes it is held, and to call the internal ones from inside. Many programmers agree, and many libraries still use reentrant locks; this is a matter of design taste, not of correctness.

**Condition waits.** A wait on a [condition variable](/condition-variable/) must release the lock so that other threads can change the condition. With a reentrant lock held $c$ times this needs care:

- In Java, `Condition.await` on a condition from `ReentrantLock.newCondition` releases the lock completely, whatever the hold count, and restores the same hold count before it returns. The same holds for `Object.wait` inside nested `synchronized` blocks.
- POSIX gives `pthread_cond_wait` no way to release all levels of a recursive mutex. In common implementations it acts like one `unlock`, so a caller that holds the mutex more than once keeps it, no other thread can take it to change the condition, and the wait can last forever. This is one of Butenhof's arguments against the type.

Either way, the code that waits must not assume that its own outer callers have restored the invariants, since other threads run while it waits.

## Laws

1. *Mutual exclusion between threads.* At every time at most one thread is the owner, and only the owner is between a `lock` and its matching `unlock`.
2. *Reentry.* A `lock` by the owner returns at once and adds 1 to the count.
3. *Balance.* If thread $t$ owns $R$ with count $c$, then $R$ becomes free after exactly $c$ more unlocks by $t$, and no other thread can own $R$ before that.
4. *Ownership.* An `unlock` by a thread that is not the owner is an error, not a release. Ownership cannot be passed to another thread, so a reentrant lock cannot be used for signals between threads, unlike a [semaphore](/semaphore/).
5. *Progress.* The lock gives the same progress between threads as the mutex it is built on: deadlock freedom, and starvation freedom if that mutex has it.
6. *Deadlock is still possible.* Reentrancy removes only the deadlock of a thread with itself. Two threads that take two reentrant locks in opposite orders can still deadlock; see [lock ordering](/lock-ordering/).

## Implementations

| implementation | owner and count | waiting | fair |
|---|---|---|---|
| wrapper around any mutex (below) | two fields next to the mutex | as the mutex | as the mutex |
| Java `ReentrantLock` | `AbstractQueuedSynchronizer` state as the count, plus an owner thread field | park in a queue | optional |
| Java `synchronized` | the object header or a monitor record | park | no |
| POSIX `PTHREAD_MUTEX_RECURSIVE` | fields of `pthread_mutex_t` | futex sleep on Linux | no |
| C++ `std::recursive_mutex` | implementation defined, unspecified maximum count | implementation defined | no |
| Python `threading.RLock` | owner and count | blocks on an inner lock | no |

**A wrapper around a mutex.** Let $M$ be any mutex, and let $owner$ (an atomic word, $\bot$ at the start) and $count$ be two extra fields. Thread $t$ runs:

```pseudo
LOCK()
    if owner = t then
        count ← count + 1
        return
    lock(M)
    owner ← t
    count ← 1

UNLOCK()
    if owner ≠ t then error
    count ← count - 1
    if count = 0 then
        owner ← ⊥
        unlock(M)
```

The test $owner = t$ reads the word without holding $M$. It is still safe: only thread $t$ writes the value $t$ to $owner$, it does so while it holds $M$, and it writes $\bot$ before it releases $M$. So a thread $t$ that reads $owner = t$ holds $M$, and a thread that does not hold $M$ reads some other value, even while other threads change the word. The word must be read and written atomically, so that no thread sees a torn value. $count$ is touched only by the owner, so it needs no atomicity. Herlihy and Shavit build the same lock from a lock and a condition, with the waiting done by the condition.

## Lower bounds

A reentrant lock gives a mutex (use it without nesting), and the wrapper above builds a reentrant lock from any mutex with $O(1)$ extra steps and no extra waiting. So the lower bounds of a [mutex](/mutex/) carry over in both directions: with reads and writes only, $n$ threads need at least $n$ shared registers (Burns and Lynch), and with reads, writes and compare-and-swap some passage makes $\Omega(\log n)$ remote memory references (see [RMR complexity](/rmr-complexity/)). Like every lock, a reentrant lock is not wait free: a thread that stops while it owns the lock blocks every other thread forever.

## References
