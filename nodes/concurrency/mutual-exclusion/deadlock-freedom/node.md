---
tag: GPMYXM
kind: definition
slug: deadlock-freedom
name: Deadlock freedom
aliases: [deadlock-free progress]
area: concurrency/mutual-exclusion
level: core
summary: "A progress property of a lock: in every fair run, if some process is trying to enter, then some process (maybe another) enters its critical section."
history:
  year: 1965
  people: [Edsger W. Dijkstra, Nancy A. Lynch, Maurice Herlihy, Nir Shavit]
  note: Dijkstra (1965) required that the processes must not block each other forever by mutual politeness. Lynch (1996) and Herlihy and Shavit (2008) state it as the progress condition above.
prereqs: [mutual-exclusion-problem]
see_also: [starvation-freedom, livelock, deadlock, lock-freedom, wait-freedom, test-and-set, spin-lock, mutual-exclusion-problem]
sources:
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 10, Mutual Exclusion, Section 10.2, the progress condition and the lockout-freedom condition
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 2, Mutual Exclusion, Section 2.2, Critical Sections (deadlock-freedom and starvation-freedom)
  - paper: doi:10.1145/365559.365617
    title: Edsger W. Dijkstra, Solution of a problem in concurrent programming control, Communications of the ACM 8(9), 1965, page 569
    locator: the requirement that "after you" blocking must not be possible
  - paper: doi:10.1145/5383.5384
    title: Leslie Lamport, The mutual exclusion problem, Part I, A theory of interprocess communication, Journal of the ACM 33(2), 1986
    locator: the formal model of the trying, critical and exit statements behind the progress properties of Part II
---

Deadlock freedom is the basic progress property of a lock or a solution of the [mutual exclusion problem](/mutual-exclusion-problem/). It says that the processes as a group cannot get stuck: whenever some process tries to enter its critical section, some process enters, though not necessarily the one that tried. It is weaker than [starvation freedom](/starvation-freedom/), which demands that each trying process enters.

## Definition

**Model.** There are $n$ asynchronous processes $p, q, \ldots$ on a sequentially consistent shared memory. Each process repeats four sections: the *remainder section*, the *entry section* (also called the trying section), the *critical section* and the *exit section*. A lock or algorithm supplies the entry and exit sections. We assume that each critical section ends after a finite number of steps of its process, and that no process stops in its entry, critical or exit section. A run is *fair* if every process that is not in its remainder section takes infinitely many steps; a process may stay in its remainder section forever.

**Definition.** An algorithm is *deadlock free* if, in every fair run:

1. every exit section ends after a finite number of steps of its process; and
2. if some process is in its entry section at some time $t$, then some process enters its critical section at a time later than $t$.

Lynch calls the second condition *progress*. The first condition is often stated separately, or it holds because the exit section has no loop.

**Equivalent form.** Given condition 1, condition 2 says that there is no fair run with a time after which some process is in its entry section, no process is in its critical section, and no process ever enters again.

**Relation to non-blocking progress.** Deadlock freedom is the blocking analog of [lock freedom](/lock-freedom/): both require that some process makes progress. The difference is that deadlock freedom assumes that no process stops while it holds the lock, and lock freedom does not.

## Examples and non-examples

- **The test-and-set lock is deadlock free.** If the lock is free and some processes keep trying, the next test-and-set returns false and its caller enters. See [test-and-set](/test-and-set/) and the proof on the [spin lock](/spin-lock/) page.
- **Peterson's algorithm, the bakery algorithm and the queue locks** ([ticket](/ticket-lock/), [MCS](/mcs-lock/), [CLH](/clh-lock/)) are deadlock free, and in fact starvation free.
- **Non-example: flags only.** Process $i$ does `flag[i] ← true`, then waits while `flag[j] = true`. If both processes raise their flags before either reads, both wait forever. This is a deadlock: no process is in its critical section and both are stuck in their entry sections.
- **Non-example: polite retreat.** Process $i$ raises its flag; if the other flag is up, it lowers its own flag and tries again. Both processes can repeat this in lock step forever. They take steps, but nobody enters. This is a [livelock](/livelock/), and it also breaks deadlock freedom, because the definition counts entries, not steps.
- **Non-example: strict alternation.** Process $i$ waits while `turn ≠ i`, enters, and writes `turn ← j` in its exit section. If process $j$ stays in its remainder section forever, process $i$ can enter once and then waits forever. The run is fair, since a process in its remainder section need not take steps, so the algorithm is not deadlock free.
- **Deadlock free but not starvation free.** The test-and-set lock: a fair run in which one process always wins the lock again while the other keeps trying. The run is shown on the [test-and-set](/test-and-set/) page and checked by its test file.

## Related definitions

- **[Starvation freedom](/starvation-freedom/).** Every process in its entry section eventually enters. Starvation freedom implies deadlock freedom: if process $p$ is in its entry section at time $t$, then $p$ itself enters after $t$. The converse fails, as the test-and-set lock shows.
- **Bounded bypass.** After a process finishes a wait-free prefix of its entry section (the doorway), every other process enters at most $b$ times before it does. Deadlock freedom with bounded bypass implies starvation freedom; see [starvation freedom](/starvation-freedom/).
- **[Deadlock](/deadlock/).** In resource allocation, a set of processes that each wait for a resource held by another process of the set. A lock that is not deadlock free has a run that ends in such a state, or in a [livelock](/livelock/).
- **[Wait freedom](/wait-freedom/) and [lock freedom](/lock-freedom/).** The non-blocking counterparts of starvation freedom and deadlock freedom. No lock is wait free or lock free, since a process that stops in its critical section blocks all others.
- **[Obstruction freedom](/obstruction-freedom/).** A process that runs alone finishes. It is weaker than lock freedom and has no blocking counterpart in this list.

## References
