---
tag: Y272XW
kind: concept
slug: deadlock
name: Deadlock
aliases:
- Deadlock problem
- deadlock handling
- deadly embrace
area: concurrency/mutual-exclusion
level: intro
summary: A state in which each process of a set waits for an event that only another process of the same set can cause, so none of them can ever proceed.
history:
  year: 1965
  people: [Edsger W. Dijkstra, Edward G. Coffman, Richard C. Holt]
  note: Dijkstra described the deadly embrace and the banker's algorithm in 1965. Coffman, Elphick and Shoshani gave the four conditions in 1971, and Holt gave the graph model in 1972.
prereqs: [critical-section, directed-graph]
see_also: [coffman-conditions, deadlock-prevention, banker-algorithm, deadlock-detection, wait-for-graph, livelock, starvation, dining-philosophers-problem]
sources:
  - url: "https://www.cs.utexas.edu/~EWD/transcriptions/EWD01xx/EWD123.html"
    title: Edsger W. Dijkstra, Cooperating sequential processes, EWD 123, Technological University Eindhoven, 1965
    locator: Section 6, The problem of the deadly embrace
  - paper: doi:10.1145/356586.356588
    title: E. G. Coffman, M. J. Elphick and A. Shoshani, System deadlocks, ACM Computing Surveys 3(2), 1971, pages 67 to 78
    locator: the four necessary conditions and the survey of prevention, avoidance and detection
  - paper: doi:10.1145/356603.356607
    title: Richard C. Holt, Some deadlock properties of computer systems, ACM Computing Surveys 4(3), 1972, pages 179 to 196
    locator: the definition of a deadlocked process and the general resource graph
  - paper: doi:10.1145/357360.357365
    title: K. Mani Chandy, Jayadev Misra and Laura M. Haas, Distributed deadlock detection, ACM Transactions on Computer Systems 1(2), 1983, pages 144 to 156
    locator: the resource model and the communication model of deadlock
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition (2015)
    locator: Chapter 6, Deadlocks (including the ostrich algorithm)
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition (2018)
    locator: Chapter 8, Deadlocks
---

A deadlock is a state of a concurrent system in which each process of a nonempty set is blocked, and each one waits for an event that only another process of the same set can cause. No process of the set can ever proceed, whatever the scheduler does. The classic case has two processes and two [mutexes](/mutex/): each process holds one mutex and waits for the other. Dijkstra called it the "deadly embrace" in 1965.

## In plain words

Two cars meet on a one-lane bridge. Each driver waits for the other to back up, and neither does. Traffic stops forever.

In a program the cars are threads and the bridge is a set of locks. One thread holds lock A and asks for lock B. Another thread holds lock B and asks for lock A. Each one waits for the other to let go first, and a waiting thread never lets go of what it holds. A deadlock does not go away by itself, and it can be rare: the two threads must take their first locks at nearly the same moment. A program can pass every test and still deadlock once a month in production. There are four ways to deal with it: make it impossible by design, refuse requests that could lead to it, find it and break it, or ignore it and restart.

## The idea

**Model.** There are $n$ asynchronous processes $p, q, \ldots$. Each process takes steps at its own speed, and memory is sequentially consistent. A process can *block* on a synchronization step: a lock of a held [mutex](/mutex/), a P on a [semaphore](/semaphore/) whose value is 0, a wait on a [condition variable](/condition-variable/), or a receive on an empty channel. A blocked process takes no steps until another process changes the state that blocks it. This page assumes that no process crashes. A process that stops forever while it holds a lock also makes the others wait forever, but that is a crash failure, not a deadlock.

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $p, q$ | process names; $i, j$ are indices |
| $m$ | the number of resources (shared objects) |
| $D$ | a set of processes |
| $S, T$ | states of the system |

**Definition.** A process $p$ is *deadlocked* in a state $S$ if $p$ is blocked in $S$ and in every state $T$ that the system can reach from $S$. A set $D$ of processes is deadlocked in $S$ if each process of $D$ is blocked in $S$ and each event that can unblock a process of $D$ is a step of a process of $D$. Then no process of $D$ can ever move, because each step that could free one of them belongs to a process that is itself blocked. Holt (1972) uses the first form: deadlock is a property of all the futures of a state, not only of the present state. A system is in a *total* deadlock when no process at all can take a step and some process has not finished. This is the form that a runtime can see directly: the Go runtime stops a program with the message "all goroutines are asleep - deadlock!" in this case.

**What deadlock is not.** In a [livelock](/livelock/) the processes keep taking steps, for example each one takes a lock, sees a conflict, releases the lock and retries, but none of them makes progress. In [starvation](/starvation/) one process waits forever while the others keep making progress. Deadlock is the case in which the waiting processes take no steps at all. [Deadlock freedom](/deadlock-freedom/) for a lock is a progress property: if some process tries to enter, some process eventually enters.

**Resource deadlock and communication deadlock.** Chandy, Misra and Haas (1983) separate two models.

- In the *resource model* (also called the AND model) a blocked process needs all the resources that it asked for, and each resource is held by some process. Draw an edge $p \to q$ when $p$ waits for a resource that $q$ holds. This is the [wait-for graph](/wait-for-graph/). When each resource has one unit, a cycle in this graph is a deadlock and each deadlock contains a cycle.
- In the *communication model* (also called the OR model) a blocked process waits for a message from any one process of a set, its *dependent set*. A cycle is not enough here: a process on a cycle can still get a message from a process off the cycle that is not blocked. A set $D$ is deadlocked when all its processes are blocked, the dependent set of each one is inside $D$, and no message is in transit between them.

With resources of several units, a cycle in the [resource allocation graph](/resource-allocation-graph/) does not imply a deadlock either. The page on [the Coffman conditions](/coffman-conditions/) gives a two-unit example in which a cycle is present and all processes still finish.

**The four strategies.** Coffman, Elphick and Shoshani (1971) sort the ways to handle deadlock into prevention, avoidance and detection. Tanenbaum adds a fourth, to ignore the problem.

| strategy | idea | cost | pages |
|---|---|---|---|
| prevention | design the system so that one of the four [Coffman conditions](/coffman-conditions/) cannot hold | lower use of resources, or a fixed order on all locks | [deadlock prevention](/deadlock-prevention/), [lock ordering](/lock-ordering/) |
| avoidance | know the maximum claim of each process, and grant a request only if the new state is safe | the claims must be known in advance; a check at each request | [banker's algorithm](/banker-algorithm/), claim edges in the [resource allocation graph](/resource-allocation-graph/) |
| detection and recovery | grant requests freely, look for a deadlock from time to time, and abort or roll back a victim | the work of the victim is lost; the check costs time | [deadlock detection](/deadlock-detection/), [wait-for graph](/wait-for-graph/) |
| ignore it | do nothing, and restart the system or the program when it hangs | a hang when it happens | Tanenbaum calls this the ostrich algorithm |

For locks inside one program the usual tools are lock hierarchies, trylock with back off, timeouts and lock order checkers. In databases the usual tools are detection on the wait-for graph and the timestamp schemes [wait-die and wound-wait](/wait-die-and-wound-wait/). The page on [deadlock handling for mutual exclusion](/mutual-exclusion-deadlock-handling/) covers both.

## Examples

**Two locks in opposite order.** Process $p$ runs `lock A; lock B; unlock B; unlock A`, and process $q$ runs `lock B; lock A; unlock A; unlock B`.

| step | process | action | owner of A | owner of B | state |
|---|---|---|---|---|---|
| 1 | $p$ | lock A | $p$ | none | |
| 2 | $q$ | lock B | $p$ | $q$ | |
| 3 | $p$ | lock B | $p$ | $q$ | $p$ blocks |
| 4 | $q$ | lock A | $p$ | $q$ | $q$ blocks: deadlock |

After step 2 the deadlock is certain: each process will ask for the lock that the other holds. The schedules that start with "$p$, $q$" and "$q$, $p$" lead to the same deadlocked state, and every other schedule finishes. If both processes take A first, no schedule deadlocks. This is the idea of [lock ordering](/lock-ordering/).

**Dining philosophers.** Five philosophers sit at a round table with one fork between each pair of neighbours. Each one picks up the left fork, then the right fork. If all five pick up their left forks at the same time, each one waits for its right neighbour forever. This is a cycle of length 5 in the wait-for graph. See the [dining philosophers problem](/dining-philosophers-problem/).

**A communication deadlock.** Process $p$ waits for a message from $q$ and then sends one to $q$. Process $q$ does the same with the roles exchanged. No lock and no resource is involved: both processes block on an empty channel. The fix is to let one of them send first.

**Semaphores.** In the [bounded buffer problem](/bounded-buffer-problem/) a producer that does P on the buffer mutex before P on the count of empty slots deadlocks when the buffer is full: the producer holds the mutex and waits for a slot, and the consumer waits for the mutex to free a slot.

**One process alone.** A process that locks a mutex that it already holds blocks forever if the mutex is not reentrant. Here the set $D$ has one process. A [reentrant lock](/reentrant-lock/) counts the nested locks of its owner instead.

**A non-example.** Two processes each hold one unit of a resource with two units, and a third process holds nothing and waits for one unit. The third process is blocked, but the first two can release their units, so it is not deadlocked.

## Where it is used

Operating systems allocate devices, memory and locks to processes, and the textbook treatment of deadlock comes from this setting (Silberschatz, Galvin and Gagne, Chapter 8; Tanenbaum and Bos, Chapter 6). Most general purpose kernels do not run the banker's algorithm, because processes do not declare their maximum claims. They prevent deadlock on their own locks by a fixed order, and the Linux kernel checks that order at run time with its lock validator.

Database systems let transactions lock rows and tables in any order, so they detect deadlock instead. A lock manager keeps a wait-for graph, finds a cycle, and aborts one transaction of the cycle so that the others can go on. Some systems use timeouts, or the timestamp rules of [wait-die and wound-wait](/wait-die-and-wound-wait/), instead of a graph.

In distributed systems no process sees the whole wait-for graph. Chandy, Misra and Haas (1983) find a cycle by sending probe messages along its edges. This is also close to [termination detection](/termination-detection/), which asks whether all processes are idle and no message is in transit.

[Model checkers](/deadlock-freedom-checking/) search all the reachable states of a model of a program for a state with no enabled step. The tests of this page do the same on a small scale: each process is a generator that yields at each step on a lock or a channel, and the search visits each reachable state once.

## References
