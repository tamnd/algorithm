---
tag: 611KPX
kind: problem
slug: dining-philosophers-problem
name: Dining philosophers problem
aliases:
- dining philosophers
- five dining philosophers
area: concurrency/mutual-exclusion
level: intro
summary: Philosophers at a round table share one fork between each pair and need both of theirs to eat. Find a protocol with no deadlock and no starvation. No deterministic symmetric one exists.
history:
  year: 1971
  people: [Edsger W. Dijkstra, Daniel Lehmann, Michael O. Rabin]
  note: Dijkstra published the problem and a semaphore solution in 1971; it is said to go back to an exam problem he set in 1965. Lehmann and Rabin gave a randomized symmetric solution in 1981.
prereqs: [deadlock, lock-ordering]
see_also: [chandy-misra-algorithm, lock-ordering, deadlock, starvation, livelock, randomized-algorithm, symmetry-reduction, mutual-exclusion-problem]
sources:
  - paper: doi:10.1007/BF00289519
    title: Edsger W. Dijkstra, Hierarchical ordering of sequential processes, Acta Informatica 1(2), 1971, pages 115 to 138
    locator: the section on the five dining philosophers, with the states thinking, hungry and eating, and one private semaphore per philosopher
  - paper: "Daniel Lehmann and Michael O. Rabin, On the advantages of free choice: a symmetric and fully distributed solution to the dining philosophers problem, Proceedings of the 8th ACM Symposium on Principles of Programming Languages (POPL), 1981, pages 133 to 138"
    locator: the impossibility of a deterministic symmetric solution, the free philosophers algorithm, and the courteous philosophers algorithm
  - paper: "Nancy Lynch, Isaac Saias and Roberto Segala, Proving time bounds for randomized distributed algorithms, Proceedings of the 13th ACM Symposium on Principles of Distributed Computing (PODC), 1994"
    locator: the formal proof of a time bound for the progress of the Lehmann and Rabin free philosophers algorithm
  - url: "https://greenteapress.com/wp/semaphores/"
    title: Allen B. Downey, The Little Book of Semaphores, version 2.2
    locator: Chapter 4, the section Dining philosophers (the footman with n minus 1 seats, and the left-handed philosopher)
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition (2015)
    locator: Chapter 2, the section on classical IPC problems, the dining philosophers problem
---

In the dining philosophers problem, $n$ philosophers sit at a round table. Between each pair of neighbours lies one fork, so there are $n$ forks. A philosopher thinks for a while, gets hungry, and must then hold both of its forks, the left and the right one, to eat; after eating it puts both down. The task is a protocol for picking up and putting down forks such that two neighbours never eat at the same time, the table never [deadlocks](/deadlock/), and, better, no philosopher [starves](/starvation/). Dijkstra published it in 1971 as a model of processes that each need two of a ring of shared resources.

## In plain words

Five people sit around a round table. There is one fork between each pair of neighbours, so five forks in all, and each person needs the fork on the left and the fork on the right to eat.

If everybody picks up the left fork at the same moment, everybody waits for the right fork for ever. Nobody can eat.

The fixes are simple once you see the problem. Number the forks and always pick up the lower number first. Or let one person be left-handed. Or have a waiter who lets only four people sit at once. Each fix breaks the circle of waiting.

There is one surprise. If all the people follow exactly the same rule and nothing tells them apart, no fix without coin tosses can work.

## Definition

The model has $n \ge 2$ asynchronous processes $p_0, \ldots, p_{n-1}$ in a ring, in a sequentially consistent memory. Fork $i$ is shared by $p_i$ (for whom it is the left fork) and $p_{i-1}$ (for whom it is the right one), indices mod $n$. A fork is a [mutex](/mutex/) with lock, unlock and trylock; some solutions add [semaphores](/semaphore/), and the randomized one adds a fair coin. A philosopher eats for a finite time and does not crash while it holds a fork; it may stop for ever while thinking.

| Symbol | Meaning |
|---|---|
| $n$ | the number of philosophers, which is also the number of forks (the shared objects, $m = n$) |
| $p, q$ or $p_i$ | philosopher names; $i, j$ are indices mod $n$ |
| $k$ | the contention: the number of hungry philosophers |

A solution gives each philosopher an entry protocol (from hungry to eating) and an exit protocol (from eating to thinking), with these properties.

- **Exclusion** (safety): two neighbours never eat at the same time. With forks this is mutual exclusion on each fork.
- **[Deadlock freedom](/deadlock-freedom/)** (progress): if some philosopher is hungry, then some philosopher eventually eats.
- **[Starvation freedom](/starvation-freedom/)** (lockout freedom): every hungry philosopher eventually eats.

Two more properties matter for the impossibility result. A solution is **symmetric** if all philosophers run the same program, start in the same state, and all forks start in the same state; a philosopher has no name, it only knows its left and right fork. It is **fully distributed** if there is no central process (no waiter) and no shared object other than the forks.

## Variants

- **Any number $n$.** The problem makes sense for $n \ge 2$; at most $\lfloor n/2 \rfloor$ philosophers can eat at once.
- **Any conflict graph.** Replace the ring by any graph: a philosopher needs the forks on all its edges. This is the general form solved by the [Chandy and Misra algorithm](/chandy-misra-algorithm/).
- **Drinking philosophers.** Each philosopher needs only some of its resources (bottles) for each session; also from Chandy and Misra.
- **Message passing.** The forks are tokens passed in messages, not shared variables; again Chandy and Misra.
- **Randomized.** Philosophers may toss coins; the progress property must then hold with probability 1.

## Examples

**The naive protocol deadlocks.** Each philosopher takes its left fork, then its right fork. If all $n$ take the left fork before any takes a right one, each holds one fork and waits for a fork held by its right neighbour: a cycle of waits round the whole table. The simulator of the implementation finds this state at $n = 3$ by a search over all interleavings: it is the schedule in which $p_0$, $p_1$, $p_2$ think and then each take their left fork.

**The solutions.** The implementation has each of the following, and checks them in two ways: over all interleavings at $n = 3$ with two meals each (no deadlock, neighbours never eat together, and every run ends with all meals eaten), and over 30 seeded random schedules at $n = 5$ with three meals each.

| solution | which condition it breaks | exhaustive at $n = 3$ | seeded at $n = 5$ |
|---|---|---|---|
| naive: left, then right | none | deadlocks | not run |
| resource order: lower numbered fork first | circular wait | no deadlock | all meals eaten |
| asymmetric: odd philosophers right fork first | circular wait | no deadlock | all meals eaten |
| waiter with $n - 1$ seats | circular wait (at most $n - 1$ in the ring) | no deadlock | all meals eaten |
| Dijkstra 1971: states and private semaphores | hold and wait | no deadlock | all meals eaten |

With $n$ seats instead of $n - 1$ the waiter is no help, and the search finds the deadlock again.

**Dijkstra's solution can starve.** Philosophers $p_0$ and $p_2$ are not neighbours. If their meals overlap, so that one of them always eats, then $p_1$, which sits between them, is never let in. The test builds this schedule at $n = 5$: $p_0$ and $p_2$ eat nine times each while $p_1$ stays hungry.

**Symmetry defeats determinism.** The "polite" protocol (take the left fork, try the right one, and if it is busy put the left one down and start again) cannot deadlock, since nobody waits while it holds a fork, but under the lock step schedule $p_0, p_1, \ldots, p_{n-1}, p_0, \ldots$ nobody ever eats: after each round all philosophers are in the same state, all forks are taken or all are free, and this goes on for ever. That is a [livelock](/livelock/), and the test shows it at $n = 5$. With Lehmann and Rabin's coin tosses, the same schedule ends with every meal eaten in each of 20 seeded runs.

## Known algorithms

- **Resource order** (a [lock ordering](/lock-ordering/)). Number the forks $0, \ldots, n-1$ and take the lower numbered fork first. Then $p_{n-1}$, whose forks are $n-1$ and $0$, takes fork $0$ first, unlike all the others. By the lock ordering theorem the wait-for graph has no cycle. With starvation free forks (for example FIFO locks) it is also starvation free. Its weak point is concurrency: a chain of waits can run almost all the way round the table, so one slow eater can hold up many others.
- **The asymmetric solution.** Make at least one philosopher take its right fork first; alternating the direction (even philosophers left first, odd ones right first) gives short chains of waits. Any assignment in which not all philosophers start on the same side breaks the cycle. Downey calls the one exception the left-handed philosopher.
- **A waiter, or $n - 1$ seats.** A counting semaphore with value $n - 1$ admits at most $n - 1$ philosophers to the table, and the seated ones take left, then right. In that protocol a philosopher waits only for its right neighbour (who holds the right fork as its left one), so a cycle of waits must go round the whole table and contain all $n$ philosophers. With at most $n - 1$ at the table, it cannot form. Downey calls this the footman.
- **Dijkstra's solution** (1971). Each philosopher has a state (thinking, hungry or eating) and a private semaphore, and one mutex protects all the states. A hungry philosopher sets its state and runs a test: if neither neighbour is eating, it moves to eating and signals its own semaphore. On leaving, a philosopher runs the test for both neighbours. A philosopher takes both "forks" at once or none, so there is no hold and wait. It is deadlock free but not starvation free, as the example shows.
- **Lehmann and Rabin's free philosophers** (1981). A hungry philosopher tosses a fair coin to choose its first fork, waits until that fork is free and takes it, then takes the other fork if it is free; if it is not, it puts the first fork down and starts again with a new coin toss. The program is symmetric and fully distributed. Lehmann and Rabin claim that, for every fair schedule, with probability 1, if some philosopher is hungry then some philosopher eventually eats: deadlock freedom with probability 1. It is not lockout free. Their courteous philosophers algorithm adds a little shared state per fork (who used it last, and which neighbours are hungry), and they claim lockout freedom with probability 1 for it.
- **Chandy and Misra** (1984). Forks are passed in messages and are clean or dirty; a philosopher must give up a dirty fork when asked. This works on any conflict graph and is starvation free. See the [Chandy and Misra algorithm](/chandy-misra-algorithm/).

**A caveat on the randomized proofs.** Lehmann and Rabin's proofs are informal, and probabilistic arguments about adversary schedulers are easy to get wrong. Lynch, Saias and Segala (1994) gave a careful proof of a time bound for the progress of the free philosophers algorithm, and later work, for example by Duflot, Fribourg and Picaronny (2004), studied which fairness assumptions on the scheduler the free philosophers need. Use the claims above in the exact form stated: with probability 1, against a fair scheduler.

## Bounds

**Theorem (Lehmann and Rabin).** For $n \ge 2$ there is no deterministic, symmetric, fully distributed protocol that has exclusion and deadlock freedom.

In the model, one step of a philosopher changes its local state and accesses at most one fork, its left or its right one, as one atomic operation. A philosopher that waits for a fork tests it again at each step, so every philosopher can always take a step.

*Proof.* Take any such protocol, let every philosopher be hungry, and use the lock step schedule that runs $p_0, p_1, \ldots, p_{n-1}$ for one step each, over and over. Call a state symmetric if all philosophers are in the same local state and all forks are in the same state. The start is symmetric. Suppose a round starts in a symmetric state. All philosophers are in the same local state, so the deterministic program makes each of them take the same kind of step: all access their left fork, or all access their right fork, or none accesses a fork. In the first case $p_i$ accesses fork $i$, and in the second fork $i + 1$; either way each fork is accessed by exactly one philosopher in the round. So each philosopher sees the same local state and the same fork state as every other, gets the same result, and leaves its fork in the same new state. The round ends in a symmetric state. By induction every round ends in a symmetric state. If some philosopher eats at the end of a round, all of them eat, including two neighbours, which breaks exclusion. So with exclusion nobody ever eats, although all are hungry and all keep taking steps: deadlock freedom fails. $\square$

The proof shows why every deterministic solution above breaks symmetry: a fork order, a left-handed philosopher, a waiter (a central process), or Dijkstra's shared state array (one shared object for all). Randomization breaks it with coin tosses, and Chandy and Misra break it with an initial placement of forks that makes the precedence graph acyclic. The simulator test of the polite protocol illustrates the theorem for one protocol; no test can prove it for all protocols.

Other bounds:

- At most $\lfloor n/2 \rfloor$ philosophers eat at the same time, since eaters form an independent set in the ring.
- With the resource order, a chain of waits can have $n - 2$ edges: $p_0$ waits for $p_1$, which waits for $p_2$, and so on up to $p_{n-2}$, which eats.
- With alternating directions and even $n$, a chain of waits has at most two edges. The fork that a philosopher takes second is also the second fork of the neighbour who shares it, so whoever holds a second fork holds both and eats; and whoever holds a first fork either eats or waits for a second fork.

## Reductions

- The problem is a set of [mutual exclusion problems](/mutual-exclusion-problem/), one per fork, where each process needs two at once. Any solution must stop the four [Coffman conditions](/coffman-conditions/) from holding together, and each solution above names the condition it breaks.
- The resource order solution is [lock ordering](/lock-ordering/) applied to forks; the waiter is a counting [semaphore](/semaphore/) that limits the number of competitors; Dijkstra's solution is a small [monitor](/monitor/) with a private condition per philosopher.
- In the general form, philosophers are the vertices of a conflict graph and forks are its edges, and a solution orients the edges: the Chandy and Misra algorithm keeps the orientation acyclic, as in an acyclic orientation from a [graph coloring](/graph-coloring/).

## Applications

- **Teaching.** The problem is the standard first example of deadlock, of livelock (the polite protocol), and of starvation (Dijkstra's solution).
- **Model checking.** It is a standard benchmark for [deadlock freedom checking](/deadlock-freedom-checking/), and, because the ring is symmetric, for [symmetry reduction](/symmetry-reduction/).
- **Resource allocation.** Any system in which processes need several of a set of shared resources, such as database transactions locking rows or threads locking two accounts, has the same deadlock, and the same fixes apply.

### History

Dijkstra published the problem, with five philosophers and his solution with states and private semaphores, in "Hierarchical ordering of sequential processes" (Acta Informatica, 1971). Accounts of the problem say that he first set it in 1965 as an examination problem, as five computers that compete for shared tape drives, and that the story of philosophers and forks was given to it soon after; these accounts are second hand, so treat the date and the details with care. Lehmann and Rabin proved in 1981 that no deterministic symmetric solution exists and gave the randomized free and courteous philosophers. Chandy and Misra generalized the problem in 1984 to any conflict graph and to drinking philosophers.

### Exercises

1. Prove that the asymmetric protocol is deadlock free as soon as at least one philosopher takes its right fork first and at least one takes its left fork first.
2. Show that the waiter with $n - 1$ seats is deadlock free, and give a schedule with $n$ seats that deadlocks.
3. Give a schedule for the resource order protocol, at $n = 5$, in which four philosophers wait in one chain.
4. Under Dijkstra's solution, show that a philosopher can starve at $n = 4$. Can it starve at $n = 3$?
5. Why does the lock step argument fail for a protocol in which each philosopher reads its own name?

## References
