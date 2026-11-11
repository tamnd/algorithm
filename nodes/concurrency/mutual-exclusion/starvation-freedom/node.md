---
tag: 7XB2EJ
kind: definition
slug: starvation-freedom
name: Starvation freedom
aliases: [lockout freedom]
area: concurrency/mutual-exclusion
level: core
summary: "A progress property of a lock: in every fair run, every process that tries to enter its critical section eventually enters. It implies deadlock freedom."
history:
  year: 1966
  people: [Donald E. Knuth, Nancy A. Lynch, Leslie Lamport, Maurice Herlihy, Nir Shavit]
  note: Knuth (1966) gave the first n-process solution in which no process can wait forever. Lynch (1996) calls the property lockout freedom, and Herlihy and Shavit (2008) call it starvation freedom.
prereqs: [deadlock-freedom, starvation]
see_also: [deadlock-freedom, starvation, wait-freedom, ticket-lock, lamport-bakery-algorithm, peterson-algorithm, filter-lock, test-and-set]
sources:
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 10, Mutual Exclusion, Section 10.2, the lockout-freedom condition and the bounded bypass condition
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 2, Section 2.2 (starvation-freedom) and Section 2.5, Fairness (doorway, waiting section and r-bounded waiting)
  - paper: "Donald E. Knuth, Additional comments on a problem in concurrent programming control, Communications of the ACM 9(5), 1966, pages 321-322"
    locator: the remark that Dijkstra's 1965 solution lets a process wait forever, and a solution that prevents it
  - paper: doi:10.1145/361082.361093
    title: Leslie Lamport, A new solution of Dijkstra's concurrent programming problem, Communications of the ACM 17(8), 1974, pages 453-455
    locator: the doorway and the first-come, first-served property of the bakery algorithm
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 6, Synchronization Tools, Section 6.2, The Critical-Section Problem (the bounded waiting requirement)
---

Starvation freedom is the progress property of a lock or a solution of the [mutual exclusion problem](/mutual-exclusion-problem/) that protects each process: every process that tries to enter its critical section eventually enters, as long as no process stops inside the lock. It is stronger than [deadlock freedom](/deadlock-freedom/), which only asks that *some* process enters, and it is the property that rules out [starvation](/starvation/).

## Definition

**Model.** There are $n$ asynchronous processes on a sequentially consistent shared memory. Each process repeats four sections: the *remainder section*, the *entry section*, the *critical section* and the *exit section*. A lock supplies the entry and exit sections. Each critical section ends after a finite number of steps of its process, and no process stops in its entry, critical or exit section. A run is *fair* if every process that is not in its remainder section takes infinitely many steps.

**Definition.** An algorithm is *starvation free* if, in every fair run:

1. every process that is in its exit section leaves it after a finite number of its own steps; and
2. every process that is in its entry section at some time $t$ enters its critical section at a time later than $t$.

Lynch calls this *lockout freedom*. Herlihy and Shavit call it *starvation freedom*.

**Bounded bypass.** Split the entry section into a *doorway*, which is a prefix that each process finishes in a bounded number of its own steps, and a *waiting section*. An algorithm has *$b$-bounded bypass* if, whenever process $p$ finishes its doorway at time $t$, every other process enters its critical section at most $b$ times after $t$ and before $p$ enters. With $b = 0$ this is the *first-come, first-served* order of the [bakery algorithm](/lamport-bakery-algorithm/) and the [ticket lock](/ticket-lock/). Herlihy and Shavit call the same condition *$r$-bounded waiting*. Lynch states a variant with no doorway, in which the count starts when $p$ enters its entry section.

**A note on the name "bounded waiting".** Operating systems texts such as Silberschatz, Galvin and Gagne list *bounded waiting* as a requirement for critical section solutions: a bound on the number of times other processes may enter after a process has asked to enter. That is bounded bypass, which is strictly stronger than starvation freedom, as the filter lock example below shows. So "bounded waiting" is not a synonym of starvation freedom, although some sources use it loosely in that sense.

## Examples and non-examples

- **Starvation free with 0-bounded bypass.** The [ticket lock](/ticket-lock/): the doorway is the fetch-and-add that takes a ticket, and processes enter in ticket order. The [MCS lock](/mcs-lock/) and the [CLH lock](/clh-lock/) also serve in the order of their doorway (a swap on the tail), and so does the [bakery algorithm](/lamport-bakery-algorithm/).
- **Starvation free with 1-bounded bypass.** [Peterson's algorithm](/peterson-algorithm/) for two processes. After process $p$ writes its flag and the victim variable, the other process can enter at most once before $p$ does.
- **Starvation free with no bound on bypass.** The [filter lock](/filter-lock/) for 3 processes. Let process $A$ finish its first write and then take steps very slowly. Processes $B$ and $C$ can take turns: each time one of them arrives at level 1 it writes itself as victim of level 1, which frees the other, and the freed one climbs and enters. $A$ is also freed, but it takes a step only rarely, so $B$ and $C$ can enter any number of times before $A$ does. $A$ still enters in every fair run, since the filter lock is starvation free.
- **Deadlock free but not starvation free.** The [test-and-set](/test-and-set/) lock and every lock where waiters race for one word. With two processes there is a fair run in which process 1 always takes the lock again before process 0 applies test-and-set to a free lock, so process 0 waits forever while process 1 enters infinitely often. This run separates the two properties.
- **Not even deadlock free.** A lock with flags only, where each process raises its flag and waits while the other flag is up. Both can wait forever.

**Proposition 1 (starvation freedom implies deadlock freedom).** Every starvation-free algorithm is deadlock free.

*Proof.* Condition 1 is the same in both definitions. If some process $p$ is in its entry section at time $t$ of a fair run, then by starvation freedom $p$ itself enters after $t$, so some process enters after $t$. $\square$

The converse fails: the test-and-set lock above is deadlock free and not starvation free.

**Proposition 2 (bounded bypass gives starvation freedom).** A deadlock-free algorithm with $b$-bounded bypass is starvation free.

*Proof.* Take a fair run and a process $p$ in its entry section. The doorway takes a bounded number of steps of $p$, and $p$ takes infinitely many steps, so $p$ finishes its doorway at some time $t$. Assume that $p$ never enters. Then $p$ is in its entry section at every time after $t$, so by deadlock freedom some process enters after each time $t' \ge t$, and there are infinitely many entries after $t$. All of them are by the $n - 1$ other processes, and by bounded bypass these processes enter at most $(n - 1) b$ times after $t$ before $p$ enters. This is a contradiction, so $p$ enters. $\square$

The converse of Proposition 2 fails too: the filter lock is starvation free with no bound on bypass.

## Related definitions

- **[Deadlock freedom](/deadlock-freedom/).** Some process enters if some process tries. Weaker.
- **[Starvation](/starvation/).** The failure that starvation freedom rules out.
- **Bounded bypass and first-come, first-served.** Defined above; stronger than starvation freedom.
- **[Wait freedom](/wait-freedom/).** The non-blocking analog: every process finishes its operation in a finite number of its own steps, even if other processes stop. No lock is wait free.
- **[Fairness](/fairness/).** The assumption on the scheduler under which these properties are stated; starvation freedom of a lock is a guarantee under a fair scheduler, not a property of the scheduler.

## References
