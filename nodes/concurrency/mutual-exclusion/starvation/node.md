---
tag: 3775ED
kind: concept
slug: starvation
name: Starvation
aliases: [indefinite postponement, lockout]
area: concurrency/mutual-exclusion
level: intro
summary: A process waits forever for a resource or the processor while other processes keep getting it. The system as a whole still makes progress.
history:
  year: 1971
  people: [P. J. Courtois, F. Heymans, D. L. Parnas, Edsger W. Dijkstra]
  note: Courtois, Heymans and Parnas (1971) showed that writers can starve under reader preference. Dijkstra used starvation of a philosopher as the central risk in the dining philosophers problem.
prereqs: [critical-section]
see_also: [starvation-freedom, deadlock-freedom, livelock, aging, priority-scheduling, readers-writers-problem, ticket-lock, fairness]
sources:
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 5, CPU Scheduling, Section 5.3.4, Priority Scheduling (indefinite blocking or starvation, and aging)
  - paper: doi:10.1145/362759.362813
    title: P. J. Courtois, F. Heymans and D. L. Parnas, Concurrent control with "readers" and "writers", Communications of the ACM 14(10), 1971, pages 667-668
    locator: Problem 1 and Problem 2, where writers or readers may wait indefinitely
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 10, Section 10.2, the lockout-freedom condition
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 2, Section 2.2, starvation-freedom; Chapter 8, Section 8.3, readers-writers locks
---

Starvation is a state in which a process waits forever for something it needs, such as a lock, a resource or the processor, while other processes keep getting it. Unlike in a [deadlock](/deadlock/), the system as a whole keeps working; only the starved process makes no progress. Algorithms that rule out starvation are called [starvation free](/starvation-freedom/).

## In plain words

Imagine a shop with one counter and a crowd of customers, but no line. Whoever pushes hardest is served next. The shop is always busy, so it is not stuck. But a small customer at the back may never reach the counter. That customer is starved.

Starvation happens when a rule picks the next winner and the rule can keep passing over the same one. The usual cures are to serve customers in the order they arrive, or to make a customer more important the longer the customer waits.

## The idea

**Definition.** Fix a fair run of a concurrent system, in which every process that is not idle takes infinitely many steps. A process *starves* in the run if, from some time on, it waits for an event (entry to its critical section, a grant of a resource, a turn on the processor) that never comes, although other processes get that event infinitely often. If no process can get the event, the state is a deadlock or a [livelock](/livelock/) instead. So starvation is a failure of the individual progress property ([starvation freedom](/starvation-freedom/)) while the global one ([deadlock freedom](/deadlock-freedom/)) still holds.

**Causes.**

- **Races with no order.** A lock that gives the lock to whichever waiter wins a race, such as the [test-and-set](/test-and-set/) lock or a [spin lock](/spin-lock/), lets one process win every time. Fairness of the scheduler does not help: each process takes steps, but the unlucky one always tries at the wrong moment.
- **Priority.** A scheduler that always runs the ready process with the highest priority starves a low priority process if higher priority work keeps arriving. This is the classic case in [priority scheduling](/priority-scheduling/). Shortest job first starves long jobs in the same way.
- **Preference policies.** A [readers-writer lock](/readers-writer-lock/) with reader preference lets new readers in while a reader is inside. With a steady stream of overlapping readers, a waiting writer never enters. With writer preference, a steady stream of writers starves the readers. Courtois, Heymans and Parnas (1971) pointed this out for both of their solutions.
- **Weak wake-up.** A [semaphore](/semaphore/) or a [condition variable](/condition-variable/) that may wake any waiter, not the one that waited longest, can pass over the same waiter forever when three or more processes compete.
- **Unlucky resource patterns.** In the [dining philosophers problem](/dining-philosophers-problem/), a philosopher can starve if its two neighbors eat in turns, so that one of its forks is always in use.

**Remedies.**

- **Fair queues.** Serve waiters in the order of their arrival. The [ticket lock](/ticket-lock/), the [MCS lock](/mcs-lock/), the [CLH lock](/clh-lock/) and the [bakery algorithm](/lamport-bakery-algorithm/) do this for locks, a strong semaphore does it for P, and [round-robin](/round-robin/) and [first-come, first-served](/fcfs-scheduling/) scheduling do it for the processor. A first-in first-out order also gives a bound on the waiting time.
- **Aging.** Raise the priority of a process as it waits, so that every waiting process eventually has the highest priority. See [aging](/aging/). The [multilevel feedback queue](/multilevel-feedback-queue/) uses a periodic priority boost for the same purpose.
- **Bounded bypass.** Limit how often others may pass a waiter. Peterson's algorithm lets the other process enter at most once; a [cohort lock](/cohort-lock/) bounds the number of local passes before the lock goes to another node.
- **Phase-fair or task-fair policies.** For readers-writer locks, alternate between a phase of readers and one writer, or queue readers and writers in one line.
- **Randomization.** [Lottery scheduling](/lottery-scheduling/) gives each process a chance in every round, so a process with at least one ticket waits only a finite time with probability 1. Its expected wait is finite, but it has no fixed bound.

**Cost.** Fair orders cost something. A queue lock hands the lock to a waiter that may be descheduled or far away, while an unfair lock lets a running process take it again at once. Many practical locks, such as the default Java `ReentrantLock` and most mutexes in operating systems, are unfair for this reason, and accept the small risk of starvation for higher throughput.

## Examples

**A test-and-set lock.** Two processes share a test-and-set lock. Process 1 leaves its critical section, comes back at once and wins the test-and-set before process 0 tries again. If the schedule repeats this pattern, process 0 takes infinitely many steps but never enters. The [test-and-set](/test-and-set/) page shows the cycle that the explorer finds.

**Reader preference.** Readers $r_1$ and $r_2$ and a writer $w$ share a reader-preference lock. $r_1$ enters. $w$ arrives and waits. $r_2$ enters while $r_1$ is inside, then $r_1$ leaves and comes back while $r_2$ is inside, and so on. The reader count never falls to 0, so $w$ waits forever. The test file of the [readers-writer lock](/readers-writer-lock/) page finds this cycle.

**Priority scheduling.** Process $L$ has priority 1. A new process of priority 5 arrives every 10 ms and needs 10 ms of processor time. The processor is never free for $L$. With aging that adds 1 to the priority of a waiting process every second, $L$ reaches priority 5 after 4 seconds and then runs before the newer arrivals of the same priority, if ties go to the process that waited longer.

**Starvation and priority inversion.** In [priority inversion](/priority-inversion/), a high priority process waits for a lock held by a low priority process that is starved by medium priority work. The high priority process is then starved too. The [priority inheritance protocol](/priority-inheritance-protocol/) is the usual fix.

## Where it is used

- As the property to rule out in lock design: [starvation freedom](/starvation-freedom/) and its stronger form, a bound on bypasses.
- In the design of schedulers, where aging and fair shares are used against it.
- In readers-writer locks and the [readers-writers problem](/readers-writers-problem/), where the choice of policy decides which side can starve.
- In the analysis of the [dining philosophers problem](/dining-philosophers-problem/) and other resource allocation problems.

## References
