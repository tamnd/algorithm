---
tag: VQ6BRS
kind: concept
slug: critical-section
name: Critical section
aliases: [critical region]
area: concurrency/mutual-exclusion
level: intro
summary: A part of a program that accesses shared state and must not run in two processes at the same time. An entry section and an exit section guard it.
history:
  year: 1965
  people: [Edsger W. Dijkstra]
  note: Dijkstra named the critical section and stated the problem of guarding it in 1965. Brinch Hansen and Hoare proposed the critical region as a language statement in 1972.
prereqs: [race-condition]
see_also: [mutual-exclusion-problem, mutex, spin-lock, semaphore, monitor, condition-variable, deadlock, lock-ordering]
sources:
  - paper: doi:10.1145/365559.365617
    title: Edsger W. Dijkstra, Solution of a problem in concurrent programming control, Communications of the ACM 8(9), 1965, page 569
    locator: the statement of the problem with the critical section of each of N computers
  - paper: doi:10.1145/5383.5384
    title: Leslie Lamport, The mutual exclusion problem, Part I, A theory of interprocess communication, Journal of the ACM 33(2), 1986
    locator: the model of the noncritical section, trying statement, critical section and exit statement
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 10, Mutual Exclusion (the remainder, trying, critical and exit regions)
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition
    locator: Chapter 6, Synchronization Tools (the critical-section problem)
  - paper: "Per Brinch Hansen, Structured multiprogramming, Communications of the ACM 15(7), 1972"
    locator: the shared variable and the region statement (critical regions and conditional critical regions)
  - paper: "C. A. R. Hoare, Towards a theory of parallel programming, in Operating Systems Techniques, Academic Press, 1972"
    locator: the critical region and the conditional critical region (with when)
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 2, Mutual Exclusion
---

A critical section is a part of the code of a process that accesses shared state and must not run at the same time as a conflicting critical section of another process. Each process puts an *entry section* before it and an *exit section* after it, and the two together make sure that at most one process is inside at any time. The term comes from Dijkstra (1965), and Lynch calls the same part of the code the *critical region*. A critical section removes a [race condition](/race-condition/) by turning a sequence of steps into a unit that no other process can split.

## In plain words

Some work must be done by one person at a time. Two people must not edit the same line of a shared ledger at once, and two cars must not be in a one-lane bridge from both ends. The part of the work that needs the room alone is the critical section.

A program puts a guard at the door. Before the critical section, a process asks to enter and waits if someone is inside. After it, the process tells the guard that it left. The guard is a lock. Everything else the process does, it does outside, at the same time as the others. A good critical section is short, so that the others do not wait long.

## The idea

**Model and notation.** There are $n$ processes $p, q, \ldots$ (indices $i, j$) that run asynchronously and share memory. The code of each process is a loop with four parts, as in Dijkstra (1965), Lamport (1986) and Lynch (1996, Chapter 10):

```pseudo
loop forever
    remainder section      ▷ private work; the process may stay here forever
    entry section          ▷ also called the trying section: acquire the right to enter
    critical section       ▷ access the shared state
    exit section           ▷ give the right back
```

The *remainder section* (Lamport says noncritical section) holds all code that does not touch the guarded state. The process may stay in it forever, and it may also stop there. The *entry section* and the *exit section* are the lock: the code that the [mutual exclusion problem](/mutual-exclusion-problem/) asks us to design. The *critical section* is the code they protect. The problem assumes that a process that enters the critical section leaves it after a finite number of its own steps, and that no process stops inside the entry, critical or exit section.

In real code, the entry section is a call such as `lock()` on a [mutex](/mutex/), and the exit section is `unlock()`. This C program uses POSIX threads; each comment names the section:

```c
#include <pthread.h>

static pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;
static long total = 0;                 /* shared state, guarded by m */

void *worker(void *arg) {
    for (long k = 0; k < 1000000; k++) {
        long x = compute(arg, k);      /* remainder section: private work */
        pthread_mutex_lock(&m);        /* entry section */
        total += x;                    /* critical section: short, no blocking */
        pthread_mutex_unlock(&m);      /* exit section */
    }
    return NULL;
}
```

Languages with scoped resources run the exit section on every path out of the critical section, including an exception. In Python, `with lock:` runs `lock.acquire()` as the entry section and `lock.release()` as the exit section. In C++, `std::lock_guard` releases the mutex in its destructor.

**What a correct critical section needs.** A critical section is correct when every access to the shared state is inside a critical section of the same lock. A lock guards *data*, not code: two different functions that touch `total` must use the same mutex `m`, and a read outside the lock is still a [race condition](/race-condition/) and a data race.

**Rules of use.**

1. *Keep it short.* While one process is inside, all others that want to enter wait. If each process spends a fraction $s$ of its time inside the critical section, the lock is busy all the time once $n \cdot s \ge 1$, and more processes do not give more throughput. For example, if the critical section takes 1 microsecond and the remainder takes 9 microseconds, 10 processes keep the lock busy, and the system cannot pass $10^6$ entries per second however many processes it has. Compute outside, then enter only to publish the result, as `compute` does above.
2. *Do not block inside.* Do not do input or output, sleep, wait for another process, or allocate memory that may wait, while holding the lock. A process that blocks inside holds up every process that waits at the door. On a uniprocessor kernel that uses a [spin lock](/spin-lock/), a process that sleeps while holding the lock can make the machine hang.
3. *Leave on every path.* An early return or an exception that skips the exit section leaves the lock held forever. Use scoped release.
4. *Take a second lock only in a fixed global order.* Two processes that each hold one lock and wait for the other's lock are in a [deadlock](/deadlock/). [Lock ordering](/lock-ordering/) prevents it.
5. *Do not call unknown code inside.* A callback may block, take other locks, or try to take the same lock again, which deadlocks a lock that is not [reentrant](/reentrant-lock/).
6. *To wait for a condition inside, use a [condition variable](/condition-variable/).* It releases the lock while the process waits, so the rule against blocking still holds.

**Critical regions as a language construct.** Brinch Hansen (1972) and Hoare (1972) proposed a statement `region v do S` for a shared variable `v`: the compiler checks that `v` is used only inside such regions and generates the entry and exit sections. The conditional form `region v when B do S` waits until `B` holds. These ideas led to the [monitor](/monitor/).

## Examples

**A counter.** The program above adds to `total` inside a critical section. Without the lock, the update `total += x` is a read and a write, and two processes can lose an update, as the trace on the [race condition](/race-condition/) page shows. With the lock, the read and the write of one process are never separated by a step of another process on `total`. The tests on the race condition page check this for three processes over every interleaving: the final value is 3 in each one.

**A linked list.** To insert a node after node $a$, a process reads `a.next`, sets the new node's `next` to it, and writes `a.next`. If two processes insert after the same node at the same time, one node is lost, as with the counter. A critical section around the three steps makes the insert a unit. Finer locking, such as [lock coupling](/lock-coupling/), uses one lock per node and keeps each critical section small.

**Disabling interrupts.** On a uniprocessor kernel, the only way another flow of control can run in the middle of a critical section is an interrupt. So the entry section can be "disable interrupts" and the exit section "enable interrupts". This does not work on a multiprocessor, where another processor runs at the same time, so kernels use spin locks there.

**A bad critical section.** A process takes the lock, reads a file, updates a shared table, and releases the lock. The file read may take milliseconds, and every other process waits that long. The fix is to read the file in the remainder section and take the lock only for the table update.

## Where it is used

Every lock-based concurrent program uses critical sections: operating system kernels (run queues, file tables, the page allocator), databases (short *latches* on pages, as opposed to long transaction *locks*), language runtimes (the heap and the class loader), and lock-based data structures. The [mutual exclusion problem](/mutual-exclusion-problem/) asks for the entry and exit sections, and the algorithms of this area give them: [Peterson's algorithm](/peterson-algorithm/) and the [bakery algorithm](/lamport-bakery-algorithm/) with plain reads and writes, the [test-and-set](/test-and-set/) and [ticket](/ticket-lock/) locks with atomic instructions, and the [mutex](/mutex/) of an operating system, which puts a waiting process to sleep.

The length of the critical section also decides the choice of lock. For a section of a few instructions, a [spin lock](/spin-lock/) is best, because putting a process to sleep costs more than the wait. For a long section, a blocking mutex is better, because a spinning process burns a processor while it waits.

## References
