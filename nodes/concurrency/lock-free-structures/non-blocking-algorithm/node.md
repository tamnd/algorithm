---
tag: VNK7PG
kind: definition
slug: non-blocking-algorithm
name: Non-blocking algorithm
aliases:
- nonblocking progress
- non-blocking synchronization
area: concurrency/lock-free-structures
level: intro
summary: A concurrent algorithm in which the delay or crash of one process cannot stop all others for ever. Wait-free, lock-free and obstruction-free are its three standard levels.
prereqs: [race-condition]
see_also: [lock-freedom, wait-freedom, obstruction-freedom, deadlock-freedom, starvation-freedom, linearizability, consensus-number, helping]
sources:
  - paper: doi:10.1007/978-3-642-25873-2_22
    title: Maurice Herlihy and Nir Shavit, On the nature of progress, OPODIS 2011, LNCS 7109
    locator: pages 313 to 328 (minimal and maximal progress, dependent and independent conditions, clash-freedom, and the periodic table of progress conditions)
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: Chapter 3, the section on progress conditions (wait-free, lock-free, and the dependent conditions deadlock-free, starvation-free and obstruction-free)
  - paper: doi:10.1145/114005.102808
    title: Maurice Herlihy, Wait-free synchronization, ACM Transactions on Programming Languages and Systems 13(1), 1991
    locator: pages 124 to 149 (the definition of wait-free implementations)
  - paper: doi:10.1145/161468.161469
    title: Maurice Herlihy, A methodology for implementing highly concurrent data objects, ACM Transactions on Programming Languages and Systems 15(5), 1993
    locator: pages 745 to 770 (non-blocking used in the sense that is now called lock-free)
  - paper: doi:10.1109/ICDCS.2003.1203503
    title: Maurice Herlihy, Victor Luchangco and Mark Moir, Obstruction-free synchronization, Double-ended queues as an example, ICDCS 2003
    locator: pages 522 to 529 (obstruction-freedom, and non-blocking as the name for the whole family)
---

A non-blocking algorithm is a concurrent algorithm in which the delay or the crash of one process cannot stop the others from making progress for ever. A lock is the opposite: if a process stops while it holds a lock, every process that needs the lock waits for ever. "Non-blocking" is now the name of a family of three progress conditions, from strong to weak: [wait-freedom](/wait-freedom/), [lock-freedom](/lock-freedom/) and [obstruction-freedom](/obstruction-freedom/). Older papers, for example Herlihy (1993), use "non-blocking" to mean lock-free only, so check which meaning a source uses.

## Definition

**Notation and model.** $n$ is the number of processes, $p$ and $q$ are processes, $i$ and $j$ are indices, $k$ is the number of processes that compete at the same time, and $m$ is the number of shared words. Processes are asynchronous: each takes steps at its own speed, and a process can crash between any two steps. Memory is sequentially consistent unless a page says otherwise. The primitives (read, write, [compare-and-swap](/compare-and-swap/) and others) are atomic steps.

A progress condition is a property of the infinite runs of an implementation of a shared object, in which processes call operations of the object again and again. Let $R$ be an infinite run. A process is *correct* in $R$ if it takes infinitely many steps, and *crashed* otherwise. The conditions below differ in two ways (Herlihy and Shavit 2011):

- **Minimal or maximal.** Minimal progress: some operation completes, again and again. Maximal progress: each operation of each correct process completes.
- **Independent or dependent.** An independent condition holds in every run, whatever the scheduler does. A dependent condition holds only in runs that the scheduler makes nice: either *fair* runs, in which no process crashes or stays suspended (each process that has started an operation takes infinitely many steps), or *isolating* runs, in which a process eventually runs alone for long enough.

The conditions are these.

| Condition | Holds in | Guarantee |
|---|---|---|
| [Wait-free](/wait-freedom/) | every run | each operation completes in a finite number of its own steps |
| [Lock-free](/lock-freedom/) | every run | in each infinite run, infinitely many operations complete |
| [Obstruction-free](/obstruction-freedom/) | isolating runs | a process that runs alone completes its operation in a finite number of steps |
| Clash-free | isolating runs | in each run where processes eventually run alone, some operation completes |
| [Starvation-free](/starvation-freedom/) | fair runs | each operation completes |
| [Deadlock-free](/deadlock-freedom/) | fair runs | some operation completes |

An implementation is **non-blocking** if it meets at least obstruction-freedom, so if no condition on fairness is needed. An implementation that uses locks is **blocking**: the best it can give is starvation-freedom, and only in fair runs, because a process that crashes while it holds a lock stops the others.

Herlihy and Shavit put these six conditions into a table, their "periodic table of progress conditions":

| | Non-blocking, independent | Non-blocking, dependent | Blocking, dependent |
|---|---|---|---|
| Maximal progress (each process) | wait-free | obstruction-free | starvation-free |
| Minimal progress (some process) | lock-free | clash-free | deadlock-free |

Clash-freedom fills the empty cell. It is weaker than obstruction-freedom and is mostly of theoretical interest.

### The inclusions

Wait-free implies lock-free, and lock-free implies obstruction-free. Each inclusion is strict.

*Wait-free implies lock-free.* In an infinite run, some process $p$ takes infinitely many steps. Under wait-freedom, each operation of $p$ ends after a finite number of steps of $p$, so $p$ completes infinitely many operations.

*Lock-free implies obstruction-free.* Take a run in which, from some point on, process $p$ is the only one that takes steps. If $p$ never completes its operation, the run is infinite, and the only process that takes steps after that point never completes anything. Only finitely many operations completed before that point, so the run has only finitely many completions, which breaks lock-freedom.

*The inclusions are strict.* The [Treiber stack](/treiber-stack/) is lock-free but not wait-free: a process can fail its CAS for ever while the others push and pop. The [lock-freedom](/lock-freedom/) page runs this schedule in the explorer. The double-ended queue of Herlihy, Luchangco and Moir (2003) is obstruction-free but not lock-free: a left push and a right push on an empty deque can make each other fail for ever, and no operation completes. The [obstruction-freedom](/obstruction-freedom/) page runs that schedule.

*Blocking conditions are not comparable in the same way.* A lock-free implementation is also deadlock-free (it gives minimal progress in every run, and so in fair runs). A deadlock-free lock does not give obstruction-freedom: if the lock holder stops, a process that runs alone still waits for ever.

### Why the conditions matter

Herlihy (1991) showed that the strength of the primitives limits which non-blocking objects you can build. A wait-free or lock-free implementation of consensus for $n$ processes needs primitives of [consensus number](/consensus-number/) at least $n$, so atomic read/write registers are not enough for two processes, and compare-and-swap is enough for any $n$. Obstruction-freedom escapes this limit: with only reads and writes you can build an obstruction-free implementation of any object (Attiya, Guerraoui and Kouznetsov 2005, cited on the [obstruction-freedom](/obstruction-freedom/) page).

The practical gains of a non-blocking algorithm are the same as its definition: no deadlock, no priority inversion and no convoys behind a preempted lock holder, and safety when a thread is killed or is interrupted by a signal handler that uses the same object. The costs are a harder design, retries under contention, the [ABA problem](/aba-problem/), and the need for safe memory reclamation, such as [hazard pointers](/hazard-pointers/), because a node can be read by a slow process after another process removed it.

## Examples and non-examples

- **Wait-free:** an atomic counter built from one [fetch-and-add](/fetch-and-add/) instruction. Each increment is one step. The [Afek et al. atomic snapshot](/afek-atomic-snapshot/) is wait-free with $O(n^2)$ steps per operation, using only registers.
- **Lock-free, not wait-free:** the [Treiber stack](/treiber-stack/) and the [Michael and Scott queue](/michael-scott-queue/). A CAS fails only because another operation succeeded, so the system as a whole progresses, but one process can starve.
- **Obstruction-free, not lock-free:** the Herlihy, Luchangco and Moir deque, and most software transactional memory with a contention manager that does not guarantee more.
- **Blocking:** a stack protected by a [spin lock](/spin-lock/) or a [mutex](/mutex/). It is deadlock-free (and starvation-free with a fair lock such as a [ticket lock](/ticket-lock/)) in fair runs, but a crash of the lock holder blocks everyone.
- **Not a progress condition:** [linearizability](/linearizability/) is a safety condition. It has a "non-blocking property" of its own, which says that the condition never forces a pending total operation to wait. That property is about the correctness condition, not about an algorithm, and a lock-based object can be linearizable and blocking.
- **Not the same as non-blocking I/O:** a system call that returns at once instead of waiting is a different use of the word.

## Related definitions

- [Lock-freedom](/lock-freedom/) and [wait-freedom](/wait-freedom/) are the independent members of the family. Lock-freedom is about the system (some operation completes) and wait-freedom is about each operation.
- [Obstruction-freedom](/obstruction-freedom/) is the weakest member. It is dependent: it needs a contention manager or backoff to make progress in practice.
- [Deadlock-freedom](/deadlock-freedom/) and [starvation-freedom](/starvation-freedom/) are the blocking conditions of [mutual exclusion](/mutual-exclusion-problem/). They are the counterparts of lock-freedom and wait-freedom under a fair scheduler. A [livelock](/livelock/) is a run with steps but no progress, which obstruction-freedom allows and lock-freedom forbids.
- [Helping](/helping/) is the main technique that turns lock-free designs into wait-free ones.
- [Consensus number](/consensus-number/) measures which primitives can give wait-free or lock-free implementations.

## References
