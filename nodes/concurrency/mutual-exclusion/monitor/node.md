---
tag: 7D5E07
kind: abstract-type
slug: monitor
name: Monitor
aliases:
- Hoare monitor
- Mesa monitor
- monitor object
area: concurrency/mutual-exclusion
level: core
summary: Shared data with procedures that run under mutual exclusion, and condition variables for waiting. Hoare's signal hands the monitor to the waiter; Mesa's signal is only a hint.
history:
  year: 1974
  people: [Per Brinch Hansen, C. A. R. Hoare, Butler W. Lampson, David D. Redell]
  note: Brinch Hansen (1973) and Hoare (1974) proposed monitors, and Hoare gave proof rules and an implementation with semaphores. Lampson and Redell (1980) described Mesa semantics, which Java and POSIX follow.
prereqs: [condition-variable]
see_also: [condition-variable, mutex, semaphore, bounded-buffer-problem, readers-writers-problem, critical-section, reentrant-lock, deadlock]
sources:
  - paper: doi:10.1145/355620.361161
    title: C. A. R. Hoare, Monitors, an operating system structuring concept, Communications of the ACM 17(10), 1974, pages 549-557
    locator: the definition of monitors and conditions, the single resource monitor, the proof rules for wait and signal with the monitor invariant, the implementation with the semaphores mutex, urgent and condsem, and the examples (bounded buffer, readers and writers)
  - paper: doi:10.1145/155360.155361
    title: Per Brinch Hansen, Monitors and Concurrent Pascal, a personal history, History of Programming Languages II (HOPL-II), 1993
    locator: the account of how the monitor concept grew from 1971 to 1974, the shared classes of his 1973 book Operating System Principles, and monitors in Concurrent Pascal
  - paper: doi:10.1145/358818.358824
    title: Butler W. Lampson and David D. Redell, Experience with processes and monitors in Mesa, Communications of the ACM 23(2), 1980, pages 105-117
    locator: the sections on monitors and on condition variables, where NOTIFY is a hint and WAIT is in a loop, and the reasons for this choice over Hoare's signal
  - url: "https://docs.oracle.com/javase/specs/jls/se21/html/jls-17.html"
    title: James Gosling and others, The Java Language Specification, Java SE 21 Edition, Chapter 17, Threads and Locks
    locator: Section 17.1, Synchronization (every object has a monitor, which a thread may lock more than once), and Section 17.2, Wait Sets and Notification (wait, notify, notifyAll, and spurious wakeups)
---

A monitor is a module of shared data together with the procedures that act on it, in which at most one process at a time runs a procedure. Processes outside the monitor can reach the data only through its procedures, so the data is never seen in the middle of a change. Inside a procedure, a process that must wait for the data to reach some state waits on a [condition variable](/condition-variable/), which releases the monitor while it waits. Per Brinch Hansen and C. A. R. Hoare proposed monitors in 1973 and 1974 as a structured replacement for scattered [semaphore](/semaphore/) operations. Hoare's version hands the monitor straight to the woken process; the Mesa version of Lampson and Redell only gives it a hint, and that is the version in Java and POSIX threads.

## In plain words

A monitor is a room with a lock on the door, and all the shared things are inside. Only one person may be in the room at a time. Everything you can do with the shared things is a procedure that you carry out inside the room.

Sometimes you go in and cannot finish yet: the box you want to take from is empty. Then you step into a side room and let the next person in. When someone fills the box, they call you.

There are two rules for that call. In Hoare's rule, the caller steps out and you go in at once, so the box is still full. In the Mesa rule, you only join the line for the door, and someone may empty the box before you get in. Under the Mesa rule you must look again.

## Operations

The model has $n$ asynchronous processes in a [sequentially consistent](/sequential-consistency/) memory. A process may crash between steps; a process that crashes inside the monitor blocks every other process that calls it, as with any lock. The primitives are those of the monitor below. Hoare's implementation uses counting semaphores with P and V, and the Mesa form uses a [mutex](/mutex/) and condition variables.

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $p, q$ | process names; $i, j$ index processes |
| $c$ | a condition variable of the monitor |
| $B$ | the predicate that a waiter on $c$ waits for |
| $I$ | the monitor invariant |
| $k$ | the contention: the number of processes that call the monitor at once |
| $m$ | the number of shared objects: the monitor's variables and conditions |

A monitor has

- **shared variables**, which only its procedures may read or write, with an initial value;
- **procedures**, which processes call; a call *enters* the monitor, and the return *exits* it. At most one process is *active* in the monitor at a time: inside a procedure, and not waiting;
- **condition variables**, each with wait and signal (and in Mesa, broadcast).

The operations on a condition $c$ inside the monitor:

- **c.wait.** The caller leaves the monitor and blocks on $c$, in one atomic step. When it is woken and gets the monitor back, it goes on after the wait.
- **c.signal.** If a process waits on $c$, wake one. Under *Hoare semantics* (signal and urgent wait), the woken process runs in the monitor at once, and the signaller waits in an *urgent* queue, which has priority over new entries, until the woken process exits or waits. Under *Mesa semantics* (signal and continue), the woken process only becomes ready to enter, and the signaller goes on.
- **c.broadcast** (Mesa only). Wake all processes that wait on $c$.

Hoare's single resource monitor shows the form.

```text
monitor resource
  busy := false
  nonbusy : condition

  procedure acquire()
    if busy then nonbusy.wait      { Hoare semantics; use while under Mesa }
    busy := true

  procedure release()
    busy := false
    nonbusy.signal
```

A third form, *signal and exit*, makes signal the last action of the procedure, so that the signaller leaves and the waiter runs; Concurrent Pascal's continue works in this way.

**In Java.** Every object is a monitor. A synchronized method or block locks the object's monitor on entry and unlocks it on exit, and the lock is reentrant: the thread that holds it may lock it again. wait, notify and notifyAll act on the object's single wait set, must be called while the thread holds the monitor, and follow Mesa semantics: notify moves one arbitrary thread from the wait set, and that thread must lock the monitor again before wait returns. The language specification also allows spurious wakeups, so every wait goes in a while loop. The class java.util.concurrent.locks.ReentrantLock with its Condition objects gives a lock several condition variables.

## Laws

**The monitor invariant.** Hoare's proof method attaches an invariant $I$ to the monitor's variables. $I$ must hold after initialization, and each procedure may assume $I$ when it enters and must make $I$ true again before it exits. Since only one process is active at a time, the reasoning inside a procedure is sequential, apart from waits and signals.

**Hoare's rules for wait and signal.** With $B$ the predicate associated with condition $c$:

$$\{I\}\ c.\mathrm{wait}\ \{I \land B\} \qquad \{I \land B\}\ c.\mathrm{signal}\ \{I\}$$

A waiter gives up the monitor, so it must leave $I$ true; it gets the monitor back directly from a signaller that made $B$ true, so it may assume $B$. A signaller hands the monitor over, so it must establish $I$ and $B$; it gets the monitor back when the waiter exits or waits, so it may assume only $I$. These rules are sound only for Hoare semantics.

**The Mesa rules.** Under Mesa semantics, other processes may run between the signal and the waiter's return, so the rules are

$$\{I\}\ c.\mathrm{wait}\ \{I\} \qquad \{P\}\ c.\mathrm{signal}\ \{P\}$$

for any $P$. A waiter knows only $I$ when wait returns, so it tests $B$ again: $\{I\}\ \mathbf{while}\ \lnot B\ \mathbf{do}\ c.\mathrm{wait}\ \{I \land B\}$. A signal is a hint: it changes nothing in the monitor's state, and signalling too often is safe. Neither set of rules implies the other. A Hoare proof may use $B$ after a wait, which Mesa does not give; a Mesa proof may signal with $I$ false, or use after a signal facts that, under Hoare semantics, the waiter may have changed. A program whose waits are in while loops, and whose signals come with $I$ true as the last action of a procedure, is correct under both.

**Where Hoare and Mesa differ.** In the resource monitor with if, let $q$ wait for nonbusy. Process $p$ releases the resource and signals. Under Mesa semantics, a third process $r$ enters before $q$ runs again, finds busy false, and takes the resource. Then $q$ returns from wait, does not test again, and takes the resource too: two processes hold it. Under Hoare semantics $q$ runs right after the signal, so $r$ cannot come in between. With while, the Mesa version is correct: $q$ sees busy true and waits again.

**Nested monitor calls.** If a procedure of monitor $A$ calls a procedure of monitor $B$ that waits, the wait releases $B$ but not $A$. A process that would signal must first enter $A$, and it cannot, so the system can [deadlock](/deadlock/). The usual rules are to release $A$ before the call, or not to wait inside a nested call.

## Implementations

**Hoare's implementation with semaphores.** For the monitor, a semaphore mutex (start 1), a semaphore urgent (start 0) on which signallers wait, and a count urgentcount; for each condition, a semaphore condsem (start 0) and a count condcount.

```text
entry:      P(mutex)
exit:       if urgentcount > 0 then V(urgent) else V(mutex)
c.wait:     condcount := condcount + 1
            if urgentcount > 0 then V(urgent) else V(mutex)
            P(condsem)
            condcount := condcount - 1
c.signal:   urgentcount := urgentcount + 1
            if condcount > 0 then V(condsem); P(urgent) end
            urgentcount := urgentcount - 1
```

The monitor is passed from process to process without being released: a waiter does V(urgent) or V(mutex) for the next process, a signaller does V(condsem) for the waiter and then waits on urgent, and an exit lets a waiting signaller in before any new caller. All counts are changed only by the process that is active in the monitor, so they need no other protection. Each operation costs $O(1)$ semaphore operations.

**The Mesa implementation.** A monitor is a [mutex](/mutex/) taken at entry and released at exit, and each condition is a [condition variable](/condition-variable/) with Mesa semantics on that mutex. Java's synchronized and wait and notify, and POSIX mutexes with pthread_cond_t, are this form.

**A semaphore from a monitor.** A monitor with a count and one condition gives a semaphore: P is "while count = 0 do positive.wait; count := count - 1", and V is "count := count + 1; positive.signal". With Hoare's implementation in the other direction, monitors and semaphores can each be built from the other, so they solve the same synchronization problems.

**In the tests.** The implementation runs three monitors: procsim's Mesa conditions, procsim's Hoare conditions, and Hoare's semaphore implementation above. Each runs the resource monitor (three processes once each, and two processes twice each) and a bounded buffer monitor with conditions nonfull and nonempty (one producer and two consumers, and two of each), with if and with while. The models check the proof rules as they run: $I$ at each wait, signal and exit, and, under Hoare semantics, $B$ at each signal and when each wait returns. The search over all interleavings finds:

- under Hoare semantics, in both implementations, with if or with while, no broken rule, no two processes active in the monitor, and no [deadlock](/deadlock/);
- under Mesa semantics with while, the same; but there are runs in which a woken process finds $B$ false and waits again;
- under Mesa semantics with if, the run described under Laws, in which a third process takes the resource between the signal and the waiter's return, and the buffer runs in which a consumer takes from an empty buffer;
- in a broken version of Hoare's implementation, in which exit and wait always do V(mutex) and ignore urgent, a deadlock: a signaller waits on urgent for ever.

Seeded random runs with four processes and three rounds each on the resource, and two producers and three consumers on a buffer of two slots, end with no error in each correct form.

## Lower bounds

**One process at a time.** A monitor allows one active process, so $k$ processes that call it at once take at least $k$ times the length of the longest procedure, even when their calls touch different data. This is the cost of the coarse grain, and the reason for finer locks such as the [readers-writer lock](/readers-writer-lock/).

**The cost of Hoare's signal.** Under Hoare semantics, a signal that finds a waiter costs two process switches inside the monitor: from the signaller to the waiter, and back when the waiter leaves. Lampson and Redell chose Mesa semantics so that a signal costs no switch at all; the price is the while loop and a second test of $B$.

**No guarantee of progress.** A monitor gives mutual exclusion, but no freedom from deadlock or [starvation](/starvation/) in general: a process can wait on a condition that no one will signal, and under Mesa semantics a woken process can be overtaken again and again by new callers. Under Hoare semantics a signalled process cannot be overtaken, since it gets the monitor directly from the signaller, and with FIFO condition queues the waiters on one condition are served in order.

### History

Brinch Hansen describes the shared class, a shared data structure with its operations under mutual exclusion, in his 1973 book Operating System Principles, and Hoare published the monitor with conditions, proof rules, an implementation with semaphores and a set of examples in 1974. Brinch Hansen built monitors into Concurrent Pascal in 1975. Lampson and Redell reported on monitors in the Mesa language and the Pilot operating system in 1980, where NOTIFY became a hint, and that choice passed to Modula-3, POSIX threads and Java.

### Exercises

1. Prove the resource monitor correct with Hoare's rules, with $I$: busy is true exactly when one process holds the resource.
2. In Hoare's implementation, why does exit test urgentcount before mutex? Give a schedule that goes wrong if it does not.
3. Write a bounded buffer monitor with one condition and broadcast, and show that it is correct under Mesa semantics.
4. Build a semaphore as a monitor, and prove with Hoare's rules that P never makes the count negative.
5. In Java, why does notify with a single wait set lead to a deadlock in a bounded buffer with several producers and consumers, while notifyAll does not?

## References
