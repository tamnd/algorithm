---
tag: KAC40H
kind: technique
slug: deadlock-prevention
name: Deadlock prevention
aliases:
- deadlock prevention
- Havender's methods
area: concurrency/mutual-exclusion
level: core
summary: Design the system so that one of the four Coffman conditions can never hold, for example by taking all locks at once, by giving locks back, or by a global lock order.
history:
  year: 1968
  people: [J. W. Havender]
  note: Havender described, for OS/360, the three classic ways to deny a deadlock condition. Coffman, Elphick and Shoshani (1971) put them in terms of their four conditions.
prereqs: [coffman-conditions]
see_also: [lock-ordering, banker-algorithm, deadlock-detection, coffman-conditions, mutual-exclusion-deadlock-handling, livelock, wait-die-and-wound-wait, two-phase-locking]
sources:
  - paper: "J. W. Havender, Avoiding deadlock in multitasking systems, IBM Systems Journal 7(2), 1968, pages 74 to 84"
    locator: the rules on requesting all resources together, on releasing and requesting again, and on ordered classes of resources
  - paper: doi:10.1145/356586.356588
    title: E. G. Coffman, M. J. Elphick and A. Shoshani, System deadlocks, ACM Computing Surveys 3(2), 1971, pages 67 to 78
    locator: the four necessary conditions, and the section on prevention
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition (2018)
    locator: Chapter 8, Deadlocks, the section on deadlock prevention (mutual exclusion, hold and wait, no preemption, circular wait)
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition (2015)
    locator: Chapter 6, Deadlocks, the section on deadlock prevention, with its summary table of the four approaches
---

Deadlock prevention is the design technique that makes a [deadlock](/deadlock/) impossible by construction: the system is built so that one of the four [Coffman conditions](/coffman-conditions/) can never hold. Since every deadlock needs all four, breaking one is enough, and no run-time check of the global state is needed. Havender (1968) described the three classic rules: take all resources at once, give resources back when a request fails, and take resources in a fixed order. Each rule has a price in concurrency, in knowledge needed in advance, or in wasted work.

## In plain words

A deadlock needs four things at the same time. Only one program can use a thing at a time. A program keeps what it has while it waits for more. Nobody can take a thing away from a program. And the programs wait for each other in a circle.

Take away any one of the four, and the deadlock cannot happen. You can make a program ask for everything it needs in one go, so it never waits while it holds something. You can make it give back what it holds when it cannot get the next thing. Or you can number all the things and make every program take them in increasing number, so a circle cannot form.

Each of these rules costs something. Programs wait longer, hold things they do not use yet, or redo work.

## When it applies

The setting is that of the Coffman conditions: asynchronous processes that acquire and release reusable resources, such as [mutexes](/mutex/), devices or records, through a lock manager or a lock library whose operations are atomic in a sequentially consistent memory. A blocked process takes no step. The four conditions are:

| condition | meaning | prevention |
|---|---|---|
| mutual exclusion | a unit is held by at most one process | make the resource sharable |
| hold and wait | a process holds units while it waits for more | ask for everything at once |
| no preemption | a unit leaves its holder only when the holder releases it | take units back, or release on failure |
| circular wait | a cycle of processes, each waiting for the next | a global order on the resources |

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $p, q$ | process names; $i, j$ are indices |
| $m$ | the number of resources (shared objects) |
| $k$ | the number of resources one process needs at once |

The technique applies when the code that acquires resources can be changed to follow a rule, and the rule's cost is acceptable. It gives [deadlock freedom](/deadlock-freedom/) as a safety property of every run. It does not by itself give [starvation freedom](/starvation-freedom/), and the second rule can trade deadlock for [livelock](/livelock/).

**Prevention is not avoidance.** Prevention restricts how processes may ask, and it needs no information about the future. Avoidance, as in the [banker's algorithm](/banker-algorithm/), lets processes ask in any way but decides at each request, from declared maximum claims, whether granting it keeps a safe state. Detection, the third approach, lets deadlocks happen and then breaks them; see [deadlock detection](/deadlock-detection/). This page covers prevention only.

## The template

```pseudo id=template
ACQUIRE-ONE-SHOT(S)              ▷ denies hold and wait
1  wait until every lock in S is free, holding nothing
2  take all locks of S in one atomic step

ACQUIRE-OR-RELEASE(S)            ▷ denies no preemption, by giving back
3  loop
4      lock the first lock of S
5      if trylock succeeds on every other lock of S then return
6      release every lock of S that this process holds
7      back off for a random time

ACQUIRE-ORDERED(S)               ▷ denies circular wait
8  for each lock ℓ of S in increasing rank do
9      lock ℓ
```

Pick the condition to break by asking what the program can afford.

- **Deny hold and wait** (lines 1 and 2). A process never waits while it holds something, so no process holds a unit that a waiting process needs while itself waiting; the wait-for graph has an edge only out of a process that holds nothing, so it has no cycle. Variant: release everything before each new request. Cost: the process must know its whole set $S$ before it starts, it holds units it does not need yet, and a process that needs many popular resources can wait for ever while smaller requests overtake it.
- **Deny no preemption** (lines 3 to 7). A process that cannot get a unit gives back what it holds, so it never waits while holding. The forced form takes units away from a waiting process, which works only for resources whose state can be saved and restored, such as the CPU or memory pages, or for transactions that can be rolled back. Cost: wasted work, and without the random back-off a symmetric schedule repeats for ever.
- **Deny circular wait** (lines 8 and 9). Give every resource a rank and acquire in increasing rank. Along any chain of waits the ranks rise, so the chain cannot close. The proof and the practical forms (lock levels, address order) are on the [lock ordering](/lock-ordering/) page. Cost: all code must agree on one order, and a process that discovers late that it needs a lower ranked lock must release and start again.
- **Deny mutual exclusion.** Make the resource sharable: read-only data needs no lock, a printer can be driven by one spooler process that takes jobs from a queue, and a data structure can be made [lock-free](/lock-freedom/). Cost: possible only for some resources; most locks exist because the data cannot be shared.

## Classic examples

**Three processes, three locks.** Process $p$ needs locks $a$ and $b$, $q$ needs $b$ and $c$, and $s$ needs $c$ and $a$, each taking the first before the second. If each takes its first lock, the wait-for graph has the cycle $p \to q \to s \to p$. The implementation runs this workload in a simulator that tries every interleaving:

| version | condition broken | deadlocks over all interleavings | other behavior |
|---|---|---|---|
| naive | none | yes | |
| one shot | hold and wait | none | no blocked process ever holds a lock |
| release and retry | no preemption | none | a lock step schedule repeats for ever (livelock) |
| ordered by rank | circular wait | none | the wait-for graph is acyclic in every state |

The livelock of the third version is real: if the three processes run in lock step, each takes its first lock, each fails on its second, and each gives its first back, and the state after every round is the state before it. Seeded random schedules finish, which is what a random back-off buys.

**The dining philosophers.** The same three rules give three of the classic solutions of the [dining philosophers problem](/dining-philosophers-problem/): pick up both forks at once, put the left fork down when the right one is busy, or number the forks and pick up the lower number first.

**Databases.** Conservative two-phase locking takes all locks of a transaction before it starts, which denies hold and wait. [Wait-die and wound-wait](/wait-die-and-wound-wait/) abort a transaction instead of letting certain waits happen, which is a form of preemption decided by timestamps. Ordinary [two-phase locking](/two-phase-locking/) prevents nothing, and database systems use detection on the [wait-for graph](/wait-for-graph/) instead.

**Operating systems.** Ordered acquisition is the standard rule inside kernels; Linux documents lock nesting orders and checks them with its lock validator. Spooling denies mutual exclusion for printers. Swapping a process out preempts its memory.

## Variations

- **Partial orders.** Only locks that may be held together need an order, so a partial order, or a hierarchy of levels, is enough.
- **Order by address or identifier.** For dynamic sets of objects, such as two bank accounts in a transfer, order by a unique key known at run time.
- **Two phase with trylock.** For locks that cannot be ordered, take the first, try the others, and on failure release all and retry. This is the second rule, used inside the ordered scheme.
- **Timeouts.** A lock request with a time limit turns a potential deadlock into a failure that the caller handles, usually by releasing and retrying. It is a weak form of preemption.
- **Mixed strategies.** Different classes of resources can use different methods, for example a rank order between the classes, preemption inside the class of memory, and one shot allocation inside the class of devices. Since every cycle must then either cross classes against the order or stay inside one class, where its method breaks it, no cycle can form.

## Pitfalls

- Breaking a condition for most locks is not enough. One lock acquired outside the order, or one callback that takes a lock while holding another, can close a cycle.
- The release-and-retry rule without random back-off can livelock, and with it, a process can still starve.
- Preemption of a resource with state (a half written record, a device in mid operation) corrupts the state unless the work can be rolled back.
- Asking for everything at once can make a process wait for ever behind a stream of smaller requests, unless the lock manager is fair.
- Prevention covers resources. Processes that wait for messages from each other can still deadlock (a communication deadlock); a lock order does not help there.
- Do not confuse prevention with avoidance: a prevented system needs no maximum claims, and an avoiding system does not restrict the order of requests.

## Exercises

1. Show that the one shot rule prevents deadlock even if the lock manager grants waiting requests in any order.
2. In the release-and-retry version with two processes and two locks, give a schedule that repeats for ever. What does a random back-off change?
3. A function takes lock $a$, then calls a library that takes lock $b$. Another thread takes $b$, then calls back into code that takes $a$. Which rule is broken, and how would you fix it without changing the library?
4. Why does ordering by rank not prevent a deadlock between two processes that each wait to receive a message from the other?

## References
