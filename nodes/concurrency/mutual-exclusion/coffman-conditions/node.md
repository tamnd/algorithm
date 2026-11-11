---
tag: 90K4PA
kind: definition
slug: coffman-conditions
name: Coffman conditions
aliases:
- necessary conditions for deadlock
- four conditions for deadlock
area: concurrency/mutual-exclusion
level: core
summary: Mutual exclusion, hold and wait, no preemption and circular wait. All four are necessary for a resource deadlock. They are sufficient only when each resource has one unit.
history:
  year: 1971
  people: [Edward G. Coffman, Michael J. Elphick, Arie Shoshani]
  note: Coffman, Elphick and Shoshani listed the four conditions in their 1971 survey "System deadlocks". Havender had already prevented deadlock in 1968 by breaking single conditions.
prereqs: [deadlock, resource-allocation-graph]
see_also: [deadlock-prevention, lock-ordering, wait-for-graph, deadlock-detection, banker-algorithm, readers-writer-lock]
sources:
  - paper: doi:10.1145/356586.356588
    title: E. G. Coffman, M. J. Elphick and A. Shoshani, System deadlocks, ACM Computing Surveys 3(2), 1971, pages 67 to 78
    locator: the four necessary conditions for deadlock
  - paper: doi:10.1145/356603.356607
    title: Richard C. Holt, Some deadlock properties of computer systems, ACM Computing Surveys 4(3), 1972, pages 179 to 196
    locator: graph reduction, and the cycle condition for single unit and for several unit resources
  - paper: "J. W. Havender, Avoiding deadlock in multitasking systems, IBM Systems Journal 7(2), 1968, pages 74 to 84"
    locator: allocation of all resources at once, release on refusal, and ordered allocation
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition (2018)
    locator: Chapter 8, Deadlocks, the necessary conditions and the resource-allocation graph with a cycle and no deadlock
---

The Coffman conditions are four properties of a system of processes and resources: mutual exclusion, hold and wait, no preemption, and circular wait. Coffman, Elphick and Shoshani (1971) showed that all four must hold for a [deadlock](/deadlock/) to occur, so a design that rules out one of them is free of deadlock. The four together are also sufficient when each resource has a single unit. With several units of a resource, all four can hold, with a cycle in the [resource allocation graph](/resource-allocation-graph/), and still no process is deadlocked.

## Definition

**Model.** There are $n$ asynchronous processes and $m$ resource types; type $r$ has $t(r) \ge 1$ units. Resources are reusable: a unit goes back to the pool when its holder releases it. A process asks for units with a blocking request, such as a lock on a [mutex](/mutex/) or a P on a [semaphore](/semaphore/), and it waits until all the units it asked for are free (an AND request). A process that waits takes no step, so it releases nothing. A process that gets all it asks for eventually releases all its units, for example when it finishes. No process asks for more units of a type than the type has.

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $p, q$ | process names; $i, j$ are indices |
| $m$ | the number of resource types |
| $t(r)$ | the number of units of type $r$ |

**The four conditions.** In the words of the survey, a deadlock needs:

1. **Mutual exclusion.** Each unit is used by at most one process at a time. A process that asks for a unit in use must wait.
2. **Hold and wait.** A process holds the units it already has while it waits for more. (The survey calls this the "wait for" condition.)
3. **No preemption.** A unit is released only by the process that holds it, when that process chooses to. The system cannot take it away.
4. **Circular wait.** There is a cycle of processes $p_0, p_1, \ldots, p_{k-1}$ in which each $p_i$ waits for a unit that $p_{i+1}$ holds (indices modulo $k$). In graph terms, the [wait-for graph](/wait-for-graph/) has a cycle.

The first three conditions are properties of the rules of the system. The fourth is a property of one state.

**Theorem 1 (the conditions are necessary).** If a state of the model has a deadlocked process, then all four conditions hold.

*Proof.* Use Holt's reduction: start with the free units, and repeatedly remove a process whose requests all fit in the free units, adding its held units to the pool. Let $L$ be the set of processes that remain. The page on [deadlock detection](/deadlock-detection/) proves that $L$ does not depend on the order of removal and that $L$ is exactly the set of deadlocked processes, so $L \ne \emptyset$. We check each condition.

- Mutual exclusion. A process of $L$ is blocked, so some request of it does not fit in the free units. If resources could be shared without limit, no request would ever block, and $L$ would be empty.
- Circular wait. Let $\mathit{work}^*[r]$ be the pool when the reduction stops; it is $t(r)$ minus the units held by processes of $L$. Take $p \in L$. Some type $r$ has $\mathit{req}[p][r] > \mathit{work}^*[r]$, so the processes of $L$ hold more than $t(r) - \mathit{req}[p][r] \ge \mathit{held}[p][r]$ units of $r$. Hence some $q \in L$ with $q \ne p$ holds a unit of $r$, and $p$ waits for $q$. Every process of the finite set $L$ waits for another process of $L$, so following these edges from any process repeats a process after at most $|L|$ steps, which closes a cycle.
- Hold and wait. Each process $q$ on that cycle has an incoming edge, so it holds a unit, and an outgoing edge, so it waits for another.
- No preemption. Suppose the system could take units from blocked processes. Consider the future in which every process outside $L$ finishes and releases its units, so that the pool is $\mathit{work}^*$, and then the system takes all units held by the processes of $L$. The pool becomes $\mathit{work}^* + \sum_{q \in L} \mathit{held}[q] = t$. Each request is at most $t(r)$, so the system can now serve the processes of $L$ one at a time. So no process of $L$ is blocked in every future, which contradicts the deadlock. $\square$

So a system in which one of the four conditions can never hold has no deadlock. This is the basis of [deadlock prevention](/deadlock-prevention/).

**Theorem 2 (sufficient for single units).** If every type has one unit, and the state has a cycle $p_0 \to p_1 \to \cdots \to p_{k-1} \to p_0$ in which each $p_i$ is blocked on a type that $p_{i+1}$ holds, then every $p_i$ is deadlocked.

*Proof.* The single unit of the type that $p_i$ waits for is held by $p_{i+1}$, which is blocked and therefore releases nothing, and no process can take the unit away. By induction on the number of steps, in every reachable state each $p_i$ still holds its unit and still waits: a step is a step of a process off the cycle, and it can neither release a unit of $p_{i+1}$ nor give $p_i$ a unit that is held. $\square$

**Theorem 3 (not sufficient for several units).** There is a state with two units of each of two types in which all four conditions hold, with a cycle in the wait-for graph, and no process is deadlocked. The example follows.

## Examples and non-examples

**Two locks, one unit each.** Process $p$ holds lock $A$ and waits for $B$; process $q$ holds $B$ and waits for $A$. Each lock is exclusive, each process holds one lock while it waits for the other, a lock is released only by its owner, and $p \to q \to p$ is a cycle. By Theorem 2 this is a deadlock.

**A cycle that is not a deadlock.** Types $R_1$ and $R_2$ have two units each. Process $p_1$ takes one $R_1$ and then asks for one $R_2$. Process $p_2$ takes one $R_2$ and then asks for one $R_1$. Process $p_3$ takes one $R_1$, and $p_4$ takes one $R_2$; neither asks for more. After the four first steps the state is:

| process | holds | waits for | waits for the holders |
|---|---|---|---|
| $p_1$ | one $R_1$ | one $R_2$ | $p_2, p_4$ |
| $p_2$ | one $R_2$ | one $R_1$ | $p_1, p_3$ |
| $p_3$ | one $R_1$ | nothing | |
| $p_4$ | one $R_2$ | nothing | |

No unit is free, and $p_1 \to p_2 \to p_1$ is a cycle. All four conditions hold. But $p_3$ and $p_4$ are not blocked: when $p_3$ releases its $R_1$, $p_2$ gets it, finishes, and releases its $R_2$, and then $p_1$ goes on. Over all interleavings of the four processes, no reachable state is a deadlock, although some reachable states have the cycle. With one unit of each type and only $p_1$ and $p_2$, the same programs deadlock on the schedule in which each takes its first unit before the other asks for its second.

**An upgrade on a shared lock.** A [readers-writer lock](/readers-writer-lock/) lets many readers in at once, so mutual exclusion fails between readers and two readers never deadlock on it. But if two readers each hold a read lock and each asks to upgrade to a write lock, each waits for the other to leave: the write mode is exclusive, each holds and waits, and the cycle is closed. Many readers-writer locks therefore refuse upgrades or allow only one upgrader at a time.

**Non-examples by design.**

- A process that asks for all its locks in one atomic step, and holds nothing while it waits, breaks hold and wait.
- A database that aborts a transaction and takes back its locks, as in [wait-die and wound-wait](/wait-die-and-wound-wait/), breaks no preemption.
- Programs that take locks only in one global order cannot form a cycle; see [lock ordering](/lock-ordering/).
- A [livelock](/livelock/) needs none of the four conditions: the processes are not blocked at all.

**Outside the model.** In a communication deadlock, processes wait for messages, not for resources that someone holds. "Hold and wait" and "no preemption" have no meaning there, and a cycle of waiting processes is not enough for a deadlock when a process can accept a message from any of several senders.

## Related definitions

- [Deadlock](/deadlock/): the state that the conditions describe.
- [Resource allocation graph](/resource-allocation-graph/) and [wait-for graph](/wait-for-graph/): the graphs in which circular wait is a cycle.
- [Deadlock prevention](/deadlock-prevention/): designs that make one condition impossible, with Havender's three methods (1968).
- [Banker's algorithm](/banker-algorithm/): avoidance, which allows all four conditions but refuses requests that lead to unsafe states.
- [Deadlock detection](/deadlock-detection/): the exact test with several units, by graph reduction.
- [Starvation](/starvation/) and [deadlock freedom](/deadlock-freedom/): progress properties that are not about resources held in a cycle.

## References
