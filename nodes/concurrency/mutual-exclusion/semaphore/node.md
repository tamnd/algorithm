---
tag: AHWX4C
kind: abstract-type
slug: semaphore
name: Semaphore
aliases: [counting semaphore, binary semaphore]
area: concurrency/mutual-exclusion
level: intro
summary: A shared counter with two atomic operations, P (wait until positive, then decrement) and V (increment). Dijkstra introduced it in 1965.
history:
  year: 1965
  people: [Edsger W. Dijkstra, Joseph M. Morris]
  note: Dijkstra introduced semaphores with the operations P and V in EWD 123 (1965). Morris (1979) gave a starvation-free mutual exclusion algorithm from three weak semaphores.
prereqs: [mutual-exclusion-problem]
see_also: [mutex, condition-variable, monitor, bounded-buffer-problem, readers-writers-problem, sleeping-barber-problem, dining-philosophers-problem, starvation-freedom]
sources:
  - url: "https://www.cs.utexas.edu/~EWD/transcriptions/EWD01xx/EWD123.html"
    title: Edsger W. Dijkstra, Cooperating sequential processes, EWD 123, Technological University Eindhoven, 1965
    locator: the binary semaphore with the operations P and V, the general semaphore, and the producer and consumer example
  - paper: "Joseph M. Morris, A starvation-free solution to the mutual exclusion problem, Information Processing Letters 8(2), 1979, pages 76-80"
    locator: the algorithm with three weak semaphores and two counters, and its proof of freedom from starvation
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 6, Synchronization Tools, Section 6.6, Semaphores (counting and binary semaphores, and the implementation with a list of waiting processes)
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 8, Monitors and Blocking Synchronization, Section 8.5, the semaphore built from a lock and a condition
  - url: "https://greenteapress.com/wp/semaphores/"
    title: Allen B. Downey, The Little Book of Semaphores, second edition, version 2.2.1, Green Tea Press, 2016
    locator: Section 4.3, No-starve mutex (Morris's algorithm with weak semaphores)
  - url: "https://pubs.opengroup.org/onlinepubs/9699919799/functions/sem_wait.html"
    title: The Open Group Base Specifications Issue 7 (POSIX.1-2008), sem_wait and sem_trywait
    locator: the decrement that blocks while the value is zero, and sem_post
---

A semaphore is a shared object that holds a nonnegative integer and has two atomic operations. $P(s)$ waits until the value of $s$ is positive and then decreases it by 1. $V(s)$ increases the value by 1, which may let a waiting process continue. Dijkstra introduced semaphores in 1965 as the first general tool for synchronization between processes. A semaphore that starts at 1 and is used in pairs of P and V is a mutual exclusion lock, a semaphore that starts at $k$ admits $k$ processes at a time, and a semaphore that starts at 0 lets one process wait for a signal from another.

## In plain words

A semaphore is a bowl of tokens. To go on, a process takes a token from the bowl. If the bowl is empty, the process waits next to it. When a process is done, it puts a token back, and a waiting process may then take it.

With one token, the bowl works as a lock: only the holder of the token may go on. With five tokens, five processes may go on at the same time. With no token at the start, a process can wait until another process puts in a token, which works as a signal.

Unlike a lock, the bowl does not remember who took a token. Any process may put one in. So a process that takes the only token and then asks for another one waits forever.

## Operations

**Model.** There are $n$ asynchronous processes that share memory. A semaphore $s$ has a value $val(s) \ge 0$, set when it is created, and a set of blocked processes, which is empty at the start.

| operation | effect | waits |
|---|---|---|
| $P(s)$ | if $val(s) > 0$, then $val(s) \leftarrow val(s) - 1$ and return; else join the blocked processes of $s$ and return when a $V$ wakes the caller | yes, while $val(s) = 0$ |
| $V(s)$ | if some process is blocked on $s$, wake one of them; else $val(s) \leftarrow val(s) + 1$ | no |
| $\mathit{tryP}(s)$ | if $val(s) > 0$, decrement it and return true; else return false | no |

Each operation is atomic: the test and the change of the value happen in one step, and so do the wake and the change of the blocked set. Dijkstra took the letters from Dutch words; V is usually read as *verhogen* (to increase) and P as *prolaag*, a word that he made from *probeer te verlagen* (to try to decrease). Other names are wait and signal, down and up, acquire and release, and `sem_wait` and `sem_post` in POSIX.

**The wake-up as a handoff.** In the table, a $V$ that finds a blocked process gives the token straight to that process and does not increase the value. So a process that calls $V$ and then $P$ at once cannot take the token back from a process that was blocked at the time of the $V$. Some texts define $V$ to always increase the value and let the woken process test it again; then a newcomer can take the token first. Other texts let the value go below 0, so that $-val(s)$ counts the blocked processes. The three forms give the same safety, but different fairness.

**Counting and binary.** A *counting* (or general) semaphore can hold any value $\ge 0$. A *binary* semaphore holds only 0 or 1, and a $V$ on a binary semaphore with value 1 has no effect (or is an error). A counting semaphore can be built from two binary semaphores and a counter.

**Strong and weak.** A *strong* semaphore wakes the processes in the order in which they blocked, first in, first out. A *weak* semaphore may wake any blocked process. With a strong semaphore, the plain lock

```pseudo
P(mutex)
critical section
V(mutex)
```

is [starvation free](/starvation-freedom/): if process $q$ blocks with $k$ processes ahead of it, each later $V$ wakes the first blocked process, so $q$ is woken by the $(k + 1)$st $V$, and each holder calls $V$ after a finite critical section. With a weak semaphore, the lock is starvation free for two processes, since there is only one blocked process to wake, but not for three: the $V$ calls can keep waking the other two processes in turn. The test file finds both facts with the explorer.

**Typical uses.**

- *Mutual exclusion.* `mutex` starts at 1; each process calls $P(mutex)$ before its critical section and $V(mutex)$ after it.
- *Admission of $k$ processes.* A semaphore that starts at $k$ guards a pool of $k$ identical resources.
- *Signals.* `ready` starts at 0. Process $A$ calls $V(ready)$ when an event has happened, and $B$ calls $P(ready)$ to wait for it. If the $V$ comes first, the token waits in the semaphore, so no signal is lost.
- *The bounded buffer.* Dijkstra's producer and consumer use `empty`, which starts at the buffer size $N$, `full`, which starts at 0, and a binary `mutex`. See the [bounded buffer problem](/bounded-buffer-problem/). The [readers-writers problem](/readers-writers-problem/), the [dining philosophers problem](/dining-philosophers-problem/) and the [sleeping barber problem](/sleeping-barber-problem/) were posed and solved with semaphores.

## Laws

1. *The semaphore invariant.* Let $s_0$ be the initial value, $\#V$ the number of completed $V$ calls and $\#P$ the number of $P$ calls that have returned. Then at every time $val(s) = s_0 + \#V - \#P$, so $\#P \le s_0 + \#V$. A $V$ that wakes a process adds 1 to both $\#V$ and $\#P$, and leaves the value as it is.
2. *No needless wait.* If $val(s) > 0$, no process is blocked on $s$, and a $P$ returns at once.
3. *No lost wakeup.* If a process is blocked on $s$ when a $V(s)$ happens, then some blocked process returns from its $P$. A strong semaphore wakes the one that blocked first.
4. *No owner.* Any process may call $V(s)$, also one that never called $P(s)$. This is what makes a semaphore useful for signals, and what separates a binary semaphore from a [mutex](/mutex/), which only its holder may release.
5. *Not reentrant.* A process that has taken the last token and calls $P(s)$ again blocks, and only another process can wake it. The semaphore does not know which process holds a token, so it cannot tell a nested $P$ from a $P$ by another process. The test file shows that the single process gets stuck. A [reentrant lock](/reentrant-lock/) records an owner and a count to allow nesting.
6. *Admission.* By law 1, at most $s_0$ processes are between a returned $P$ and the matching $V$ at any time, if each process calls $V$ only after its own $P$. The test file checks this for $s_0 = 1$ and $s_0 = 2$ with three processes, and checks that $s_0 = 2$ really lets two processes in at once.

## Implementations

| implementation | waiting | wake order | notes |
|---|---|---|---|
| kernel semaphore with a queue of blocked processes | sleep | FIFO (strong) | Dijkstra's form; the kernel makes P and V atomic |
| kernel semaphore with a set of blocked processes | sleep | any (weak) | cheaper; can starve a process when three or more compete |
| mutex and [condition variable](/condition-variable/) | sleep | any, and a newcomer may take the token first | the usual library form, shown below |
| spinning on a counter with [compare-and-swap](/compare-and-swap/) | spin | none | $P$ retries a compare-and-swap from $v$ to $v - 1$ while it reads $v > 0$ |
| POSIX `sem_t` in glibc on Linux | futex sleep | not specified | an atomic fast path in user space, so no system call when there is no contention |
| Java `java.util.concurrent.Semaphore` | park | FIFO if created fair, else any | `acquire`, `release` and `tryAcquire` |

**From a mutex and a condition variable.** The value is an integer `count`, guarded by the mutex `m`, and the condition variable `c` holds the waiters:

```pseudo
P()
    lock(m)
    while count = 0 do
        wait(c, m)          ▷ releases m while it sleeps, and takes m again
    count ← count - 1
    unlock(m)

V()
    lock(m)
    count ← count + 1
    signal(c)
    unlock(m)
```

The test is in a loop because a woken waiter must take `m` again, and another process may take the token first. So this semaphore is weak, and it is not even a handoff semaphore. The test file checks it with three processes for $k = 1$ and $k = 2$: no more than $k$ processes are inside, and no run gets stuck.

**Morris's algorithm.** Morris (1979) showed that weak semaphores suffice for a starvation-free lock, even for any number of processes, as long as $V$ hands the token to a blocked process as in the table above. The algorithm uses the counters $room_1$ and $room_2$ (both 0), a binary semaphore `mutex` = 1 for $room_1$, and two weak semaphores, the doors $t_1 = 1$ and $t_2 = 0$:

```pseudo
P(mutex); room1 ← room1 + 1; V(mutex)
P(t1)
    room2 ← room2 + 1
    P(mutex); room1 ← room1 - 1
    if room1 = 0 then V(mutex); V(t2)    ▷ the last one closes door 1 and opens door 2
    else V(mutex); V(t1)
P(t2)
    room2 ← room2 - 1
    critical section
    if room2 = 0 then V(t1)              ▷ the last one opens door 1 again
    else V(t2)
```

Processes collect in room 1 and go through door 1 one at a time into room 2. When room 1 is empty, door 1 stays shut and door 2 opens, and all processes in room 2 pass through the critical section one at a time. The last of them opens door 1 again. A process that arrives while door 2 is open waits in room 1, so the group in room 2 is fixed, and each of its members enters before the door opens again. The test file checks mutual exclusion, absence of stuck states and absence of starvation for three processes that run forever. A conjecture attributed to Dijkstra said that weak semaphores could not do this; Morris's algorithm answered it.

## Lower bounds

- *No wait freedom.* A $P$ on a semaphore with value 0 must wait until some other process calls $V$. If that process stops, the caller waits forever, so no implementation is wait free.
- *Register lower bounds carry over.* A binary semaphore that starts at 1 gives a deadlock-free mutex for $n$ processes. So any implementation of a semaphore from atomic reads and writes needs at least $n$ shared registers, by the bound of Burns and Lynch for mutual exclusion. See [mutual exclusion lower bounds](/mutual-exclusion-lower-bounds/).
- *Weak semaphores and fairness.* The plain lock $P(mutex)$, $V(mutex)$ on a weak semaphore is not starvation free for three processes, as the test file shows. Fairness then needs more structure, such as the three semaphores and two counters of Morris's algorithm.

## References
