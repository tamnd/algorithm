---
tag: TSEGXF
kind: abstract-type
slug: condition-variable
name: Condition variable
aliases:
- condvar
- condition
- condition queue
area: concurrency/mutual-exclusion
level: core
summary: A queue of threads that wait, under a mutex, for a predicate on shared state. wait releases the mutex and blocks in one step; signal wakes one waiter and broadcast wakes all.
history:
  year: 1974
  people: [C. A. R. Hoare, Per Brinch Hansen, Butler W. Lampson, David D. Redell, Andrew D. Birrell]
  note: Hoare (1974) defined conditions with wait and signal inside monitors. Lampson and Redell (1980) made signal a hint (Mesa semantics). Birrell (2003, printed 2004) told how hard they are to build from semaphores.
prereqs: [mutex]
see_also: [monitor, mutex, semaphore, bounded-buffer-problem, sleeping-barber-problem, readers-writers-problem, race-condition, deadlock]
sources:
  - paper: doi:10.1145/355620.361161
    title: C. A. R. Hoare, Monitors, an operating system structuring concept, Communications of the ACM 17(10), 1974, pages 549-557
    locator: the definition of condition variables with wait and signal, where signal passes control to the waiting program at once, and the implementation of monitors and conditions with semaphores
  - paper: doi:10.1145/358818.358824
    title: Butler W. Lampson and David D. Redell, Experience with processes and monitors in Mesa, Communications of the ACM 23(2), 1980, pages 105-117
    locator: the section on condition variables, where NOTIFY is a hint, WAIT must be in a loop that tests the condition again, and BROADCAST and timeouts are added
  - paper: doi:10.1007/0-387-21821-1_5
    title: Andrew D. Birrell, Implementing condition variables with semaphores, in Computer Systems, Theory, Technology, and Applications, a tribute to Roger Needham, Springer, 2004, pages 29-37
    locator: the three versions built at DEC SRC with a semaphore s, then a lock x and a count waiters, then a handshake semaphore h, the bugs of the first two, and the version with an explicit queue of per thread semaphores
  - url: "https://pubs.opengroup.org/onlinepubs/9699919799/functions/pthread_cond_wait.html"
    title: The Open Group Base Specifications Issue 7 (POSIX.1-2008), pthread_cond_wait and pthread_cond_timedwait
    locator: the rule that the mutex is released and the thread blocks atomically, and the note that spurious wakeups may occur, so that the predicate must be tested again in a loop
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 8, Monitors and Blocking Synchronization, Section 8.2, Monitor Locks and Conditions, with the lost-wakeup problem
---

A condition variable is a queue of threads that wait for a predicate on shared state to become true. It is always used with a [mutex](/mutex/) that protects that state. A thread that holds the mutex and finds the predicate false calls *wait*, which releases the mutex and puts the thread to sleep in one atomic step. A thread that makes the predicate true calls *signal*, to wake one waiter, or *broadcast*, to wake all of them. Unlike a [semaphore](/semaphore/), a condition variable has no memory: a signal when nobody waits does nothing. Condition variables are the waiting part of a [monitor](/monitor/), and they are the form of waiting in POSIX threads, Java and most thread libraries.

## In plain words

Think of a waiting room next to an office. Only one person can be in the office at a time, and the office key is the mutex. You go in and find that the thing you need is not ready yet. You do not stay in the office, because then nobody else could get in to make it ready. You hand back the key and sit in the waiting room. When someone in the office makes a change, they call into the waiting room: "one of you, come and look", or "all of you, come and look". The ones called queue for the key again.

When you get back into the office, you must look again. Someone else may have come in first and taken the thing. That is why every wait sits inside a loop.

## Operations

The model has $n$ asynchronous processes (threads) in a [sequentially consistent](/sequential-consistency/) memory. A process may crash between steps; a process that crashes while it holds the mutex blocks all the others, as with any lock. The primitives are a mutex with lock and unlock, and for the implementations below, counting and binary semaphores with P and V.

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $p, q$ | process names; $i, j$ index processes |
| $c$ | a condition variable; in code, its mutex is called mutex |
| $w$ | the number of processes that wait on $c$ |
| $k$ | the contention: the number of processes that want the mutex at once |
| $m$ | the number of shared objects, when used as a count |
| $B$ | the predicate on shared state that a waiter waits for |

A condition variable $c$ is bound to a mutex. Every operation is called by a process that holds that mutex. (POSIX lets a thread signal without the mutex; the changes to the shared state must still be made under it.)

- **wait(c).** Precondition: the caller holds the mutex. Atomically, the caller joins the queue of $c$ and releases the mutex. It then blocks until it is woken, and takes the mutex again before wait returns. When wait returns, the caller holds the mutex, but it knows nothing about $B$.
- **signal(c).** If the queue of $c$ is not empty, wake at least one waiter. Otherwise do nothing. Lampson and Redell call it NOTIFY, Java calls it notify, and POSIX calls it pthread_cond_signal.
- **broadcast(c).** Wake every process that is in the queue of $c$ when broadcast is called. Mesa calls it BROADCAST, Java notifyAll, POSIX pthread_cond_broadcast.

The standard pattern is

```text
lock(mutex)
while not B:
    wait(c)
... B holds here, and the mutex is held ...
unlock(mutex)
```

and on the other side

```text
lock(mutex)
change the shared state so that B may now hold
signal(c)  or  broadcast(c)
unlock(mutex)
```

**Mesa and Hoare semantics.** In Hoare's original definition, signal hands the mutex straight to one waiter, which runs at once, and the signaller waits until the mutex is free again. The waiter then knows that $B$ holds, since no other process ran in between. In Mesa semantics, which Lampson and Redell introduced and which POSIX and Java follow, signal only moves a waiter from the queue of $c$ to the queue of the mutex. The signaller goes on. Other processes may take the mutex first and make $B$ false again. So a woken waiter must test $B$ again, and signal is only a hint. The [monitor](/monitor/) page compares the two in detail.

## Laws

- **Atomic release.** In wait, the step that releases the mutex and the step that joins the queue are one atomic step. If they were two steps, a signal could come between them and find nobody to wake. This is the *lost wakeup*: the waiter then sleeps although $B$ holds. The same [race condition](/race-condition/) is the problem in the [sleeping barber](/sleeping-barber-problem/) with plain sleep and wakeup.
- **No memory.** A signal or a broadcast when no process waits has no effect. A process that calls wait later is not woken by it. So a process must test $B$ before it waits, and must never wait for a signal without a predicate.
- **Wait in a loop.** Under Mesa semantics, $B$ can be false when wait returns: another process may have run between the signal and the waiter's return and made $B$ false. POSIX and Java also allow *spurious wakeups*, a return with no signal at all. So the test of $B$ is a while loop, not an if. With while, a waiter is also correct under Hoare semantics, where the extra test is merely redundant.
- **No wakeup from the past.** A wait returns only after a signal or broadcast that was called after the wait began (apart from spurious wakeups where they are allowed). Birrell states it for broadcast: it wakes exactly the threads that called wait before it.
- **Signal versus broadcast.** If waiters on one condition variable wait for different predicates, signal can wake a process whose predicate is still false, while the process that could go on stays asleep. Use broadcast, or one condition variable per predicate.
- **Signal under the mutex.** If the process that makes $B$ true does not hold the mutex, the change can come between a waiter's test of $B$ and its wait, and the wakeup is lost. The rule is to change the state under the mutex; whether the signal itself is inside the critical section is then a question of speed only.

## Implementations

**In the kernel or the thread library.** The usual implementation keeps a queue of waiting threads per condition variable. Wait puts the thread on the queue and releases the mutex while it holds the lock that protects the queue, so the two steps are atomic. Signal moves the first thread from that queue to the ready queue, or straight to the queue of the mutex. Each operation costs $O(1)$ outside the scheduler, and broadcast costs $O(w)$. Birrell reports that, after the attempts below, his group at DEC SRC gave up and put condition variables in the kernel.

**From semaphores (Birrell).** At DEC SRC in 1984, Birrell and his colleagues tried to build Mesa condition variables from semaphores, and found that it is much harder than it looks. The mutex is a semaphore with count 1. Each version below is modelled in the implementation, and the tests find each bug with a search over all interleavings.

*Version 1.* One binary semaphore $s$, which starts at 0.

```text
wait:    release(mutex); P(s); acquire(mutex)
signal:  V(s)
```

The race between release(mutex) and P(s), which Saltzer called the wake-up waiting race, is handled: a V that comes in between leaves $s$ at 1, and the P goes through. But a signal when no thread waits also leaves $s$ at 1, so the next wait returns at once. This breaks the law of no memory. The test finds this with a setter that signals before any process waits, and a late process that waits afterwards and returns with no signal.

*Version 2.* Add a lock $x$ and a count of waiters, so that a signal with no waiter does nothing.

```text
wait:       P(x); waiters := waiters + 1; V(x)
            release(mutex); P(s); acquire(mutex)
signal:     P(x); if waiters > 0 then waiters := waiters - 1; V(s) end; V(x)
broadcast:  P(x); while waiters > 0 do waiters := waiters - 1; V(s) end; V(x)
```

It has two bugs, both at the point between release(mutex) and P(s). First, $s$ is still binary. If several waiters are at that point when broadcast does its V operations, the count of $s$ stops at 1, and all waiters but one stay blocked. The test finds this with two waiters and one broadcast. Second, with a counting $s$, a process that calls wait after the broadcast can do its P(s) first and take a V that was meant for an older waiter. The newcomer returns although no signal came after its wait began, and the older waiter stays blocked for ever. The test finds this for broadcast and for signal: a waiter $p$ is between release(mutex) and P(s), the setter wakes it, and a late process $q$ waits and takes the V.

*Version 3.* Add a handshake semaphore $h$, which starts at 0, and let $s$ count.

```text
wait:       P(x); waiters := waiters + 1; V(x)
            release(mutex); P(s); V(h); acquire(mutex)
signal:     P(x)
            if waiters > 0 then waiters := waiters - 1; V(s); P(h) end
            V(x)
broadcast:  P(x)
            for i := 1 to waiters do V(s) end
            while waiters > 0 do waiters := waiters - 1; P(h) end
            V(x)
```

The signaller holds $x$ until each woken thread has done its P(s) and its V(h). A newcomer cannot even count itself as a waiter while $x$ is held, so it cannot take a V meant for another thread. Birrell believed this version to be correct, and the search over all interleavings agrees for the scenarios tested. It costs two extra context switches per signal, since the signaller must wait for the handshake.

*An explicit queue.* Each thread has its own binary semaphore, which starts at 0, and the condition variable is a queue of threads under a lock $x$. Wait puts the caller on the queue under $x$, releases $x$ and the mutex, and does P on its own semaphore; signal takes the first thread off the queue under $x$ and does V on its semaphore; broadcast does that for every thread on the queue. Since each V is addressed to one thread, nobody can take another's wakeup. This is Birrell's recommendation: do the queuing yourself, or get a primitive that releases the mutex and blocks in one step.

| implementation | signal with no waiter | broadcast | newcomer steals a wakeup | status |
|---|---|---|---|---|
| version 1 | remembered | none | yes | wrong |
| version 2, binary $s$ | ignored | strands waiters | yes | wrong |
| version 2, counting $s$ | ignored | correct alone | yes | wrong |
| version 3, handshake | ignored | correct | no | correct, slow |
| explicit queue | ignored | correct | no | correct |
| kernel queue | ignored | correct | no | correct |

**In the tests.** The implementation runs each version in two scenarios: processes that wait for a flag that one setter raises, and a [bounded buffer](/bounded-buffer-problem/) with producers and consumers. The search over all interleavings checks the law of no wakeup from the past, the buffer bounds, and the absence of [deadlock](/deadlock/). It also shows three bugs of use, with correct condition variables: a consumer that tests "not empty" with if takes from an empty buffer under Mesa semantics; a waiter that waits without a predicate misses a signal that came first; and a bounded buffer with one condition variable and signal deadlocks, because a consumer's signal wakes the other consumer and not the producer. With while, two condition variables, or broadcast, the same searches find no error. Seeded random runs with two producers, three consumers and two slots end with every item consumed for each correct implementation.

**In languages.** POSIX threads have pthread_cond_wait, pthread_cond_signal and pthread_cond_broadcast. Java has wait, notify and notifyAll on every object, used inside synchronized, and the Condition objects of java.util.concurrent.locks, which give a lock several conditions. Both use Mesa semantics and allow spurious wakeups.

## Lower bounds

**Broadcast costs $\Omega(w)$.** A broadcast that wakes $w$ waiters must change the state of each of them, and each of them must then take the mutex again, one at a time. So a broadcast costs at least $w$ steps, and the waiters run through the mutex in series. When only one of them can go on, the rest test $B$, find it false and wait again; this is why one condition variable per predicate, with signal, is cheaper than one shared condition variable with broadcast.

**A wakeup must be addressed.** The two bugs of Birrell's version 2 have one cause. A V on a shared semaphore is not addressed to a thread, so any thread that does P on that semaphore can take it, including one that began to wait after the signal. A correct implementation must either name the thread it wakes (a queue with one semaphore per thread, or a kernel queue) or stop new threads from doing P until the woken ones have done theirs (the handshake of version 3, which costs two extra context switches per signal). This is an argument from the cases tested, not a proof that no cheaper construction exists.

**Signal cannot replace broadcast in general.** With one condition variable and waiters for different predicates, a signal may wake a process whose predicate is false. If that process waits again, the wakeup is used up, and the system can deadlock with a process asleep whose predicate holds. The bounded buffer with one condition variable shows this with one producer and two consumers on one slot.

### Exercises

1. Show that if wait released the mutex in one step and joined the queue in a later step, a waiter could sleep for ever with $B$ true.
2. In Birrell's version 1, give a schedule with one waiter and two signals that leaves $s$ at 1 after the waiter returns. Which later wait is wrong?
3. In version 3, why must broadcast do all its V(s) operations before its first P(h)?
4. Give a schedule of the bounded buffer with one condition variable and signal in which a producer's signal wakes the other producer, with two producers and one consumer.
5. Change the if in the Mesa consumer to while, and show that the count of the buffer can no longer go below 0.

## References
