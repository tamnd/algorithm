---
tag: TNQ9RS
kind: algorithm
slug: priority-ceiling-protocol
name: Priority ceiling protocol
aliases:
- PCP
- immediate priority ceiling
area: systems/scheduling
level: advanced
summary: "Each semaphore gets a ceiling, the top priority of its users. A lock is granted only above all ceilings held by others: no deadlock, and blocking by at most one critical section."
solves: [real-time-scheduling]
model: word-ram
complexity:
  vars: {j: the number of jobs, s: the number of semaphores, a: the number of actions and time units in the run}
  time: {worst: O(a j^2 (j + s))}
  space: {extra: O(j + s)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1990
  people: [Lui Sha, Ragunathan Rajkumar, John P. Lehoczky]
  note: Sha, Rajkumar and Lehoczky defined the priority ceiling protocol in a 1987 report and in IEEE Transactions on Computers in 1990; Baker's stack resource policy of 1991 gave the immediate form for stacks and EDF.
prereqs: [priority-inheritance-protocol, deadlock]
see_also: [priority-inheritance-protocol, priority-inversion, response-time-analysis, fixed-priority-scheduling, deadlock-prevention, lock-ordering, coffman-conditions, earliest-deadline-first]
sources:
  - paper: doi:10.1109/12.57058
    title: "Lui Sha, Ragunathan Rajkumar and John P. Lehoczky, Priority inheritance protocols: an approach to real-time synchronization, IEEE Transactions on Computers 39(9) (1990), 1175-1185"
    locator: the priority ceiling protocol, its freedom from deadlock and its bound of one critical section
  - paper: doi:10.1007/BF00365393
    title: "Theodore P. Baker, Stack-based scheduling of realtime processes, Real-Time Systems 3(1) (1991), 67-99"
    locator: the stack resource policy and its preemption ceilings
  - book: isbn:9781461406754
    title: "Giorgio C. Buttazzo, Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, third edition, Springer, 2011"
    locator: Chapter 7 (resource access protocols), the priority ceiling protocol and the stack resource policy
  - book: isbn:9780130996510
    title: Jane W. S. Liu, Real-Time Systems, Prentice Hall, 2000
    locator: Chapter 8 (resources and resource access control)
---

The priority ceiling protocol is a lock rule for [fixed-priority scheduling](/fixed-priority-scheduling/) that bounds [priority inversion](/priority-inversion/) and prevents [deadlock](/deadlock/). Each semaphore gets a *ceiling*, the highest priority of any task that uses it, and a job may lock a free semaphore only if its priority is above the ceilings of all semaphores that other jobs hold. Holders also inherit priorities, as in the [priority inheritance protocol](/priority-inheritance-protocol/). Sha, Rajkumar and Lehoczky proved in 1990 that a job is then blocked by at most one critical section of one lower job, and that no deadlock can occur.

## In plain words

Each room in an office has a sign with the rank of the most senior person who ever uses it. Before you enter any room, you look at the signs of all rooms that other people are using at the moment. You may enter only if you outrank every one of those signs.

This rule can stop you even when your room is empty. The reason is that someone inside another room might later need your room, and the two of you could then wait for each other forever. The rule stops that before it starts. The price is a short wait. The gain is that a senior person waits for at most one junior person, and only once.

## The problem

One processor runs jobs of [periodic](/periodic-task-model/) or [sporadic](/sporadic-task-model/) tasks under preemptive fixed priorities. Jobs lock and unlock binary [semaphores](/semaphore/) in properly nested [critical sections](/critical-section/), and the set of semaphores that each task uses is known before the system runs. Jobs do not suspend themselves. The goal is a lock rule with no deadlock and a small bound on the blocking time $B_i$ of each task. The bound goes into the sufficient [response-time test](/response-time-analysis/) $R_i = C_i + B_i + \sum_{j \in hp(i)} \lceil R_i / T_j \rceil C_j \le D_i$.

## The algorithm

The ceiling $c(S)$ is the highest base priority of a job that uses $S$. For a job $x$, $\Pi(x)$ is the highest ceiling of a semaphore held by a job other than $x$. The simulation works in time units. A job that asked for a lock and was refused is *blocked* until the condition of line L3 is false.

```pseudo id=main
PRIORITY-CEILING(jobs)                      ▷ ceilings c(S) computed in advance
L1  t ← 0
L2  while some job is not finished do
L3      for each pending job x that asked for S: if S is held or p*(x) ≤ Π(x) then blocker(x) ← the holder of the held semaphore of highest ceiling
L4      p*(x) ← p(x) for all x; repeat p*(blocker(x)) ← max(p*(blocker(x)), p*(x)) until no change; repeat L3 and L4 until p* is stable
L5      R ← the pending jobs with no blocker; j ← the job of R with the largest p*, a lock holder first on a tie
L6      if R is empty then
L7          if some job is pending then stop: deadlock
L8          idle for one unit; t ← t + 1; go to L2
L9      if the next action of j is LOCK(S) then
L10         if S is free and p*(j) > Π(j) then j holds S else j asks again later
L11     else if the next action of j is UNLOCK(S) then free S
L12     else run j for one unit; t ← t + 1
```

Line L10 is the ceiling test. It is strict, and $\Pi(j)$ leaves out the semaphores that $j$ holds itself, so a job can nest its own locks. A refusal at line L10 with a free $S$ is *ceiling blocking*: the protocol refuses a lock that is free because another job holds a semaphore that a job of higher priority may need.

## Example

The two cases below are also tests of the implementation. The ceilings are $c(A) = c(B) = 2$ in the first case and $c(A) = c(B) = 3$ in the second.

**Opposite lock order.** $J_1$ (priority 1, released at 0) locks $A$, runs 1 unit, locks $B$, runs 1 unit, then frees $B$ and $A$. $J_2$ (priority 2, released at 1) locks $B$ then $A$ in the same way.

| slot | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| priority inheritance | $J_1$ takes $A$ | $J_2$ takes $B$ | deadlock | |
| priority ceiling | $J_1$ takes $A$ | $J_1$ takes $B$ | $J_2$ | $J_2$ |

At time 1, $J_2$ asks for the free $B$, but $p(J_2) = 2 \le \Pi(J_2) = c(A) = 2$, so line L10 refuses it. $J_1$ inherits priority 2, takes $B$, ends its work and frees both locks. $J_2$ is blocked for 1 unit, and no deadlock occurs.

**Chained blocking.** $J_3$ (priority 1, released at 0) holds $A$ for 2 units. $J_2$ (priority 2, released at 1) holds $B$ for 2 units. $J_1$ (priority 3, released at 2) holds $A$ for 1 unit, then $B$ for 1 unit.

| slot | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| priority inheritance | $J_3$ | $J_2$ | $J_3$ | $J_1$ | $J_2$ | $J_1$ |
| priority ceiling | $J_3$ | $J_3$ | $J_1$ | $J_1$ | $J_2$ | $J_2$ |

Under inheritance, $J_1$ is blocked twice, by $J_3$ and then by $J_2$. Under the ceiling rule, $J_2$ is refused $B$ at time 1 because $c(A) = 3 \ge 2$, so it never starts its critical section. $J_1$ is not blocked at all, and $J_2$ is blocked for 1 unit by $J_3$.

## Correctness

Order the jobs that hold locks by the time each took its outermost lock: $K_1, \ldots, K_r$. The proof keeps three facts true. Each $K_k$ has a base priority above every ceiling of the locks of the earlier holders, every blocked job holds no lock and is blocked by $K_r$, and $K_r$ is ready. The first fact holds because line L10 grants a first lock only above all held ceilings. It follows that only $K_r$ runs among the holders, and that $K_r$ is never refused, so there is always a ready job and no deadlock. For blocking, a lower job $L$ can run while $J$ is pending only if it held, at the release of $J$, a lock of ceiling at least $p(J)$. Two such lower jobs would break the first fact, so only one lower job blocks $J$, inside one outermost critical section. The full proof is in the proofs folder.

## Complexity

- **Per decision.** Line L3 takes $O(j s)$ time, line L4 takes $O(j^2)$, and the two lines repeat at most $j + 2$ times. So one decision takes $O(j^2 (j + s))$ time, and a run of $a$ decisions takes $O(a j^2 (j + s))$. The extra space is $O(j + s)$.
- **In a kernel.** By the invariant, locks are taken and freed in last-in, first-out order over the whole system. So the kernel keeps a stack of the running maximum of ceilings, and $\Pi$ costs $O(1)$ per lock and unlock.
- **Blocking term.** $B_i$ is the longest outermost critical section of a lower task that locks a semaphore with ceiling at least the priority of $\tau_i$. This is one section, not a sum.

## Properties

- **No deadlock.** No cycle of waits can form, whatever order the jobs lock in.
- **One blocking section.** A job is blocked by at most one outermost critical section of one lower job, so there is no chained blocking.
- **Ceiling blocking.** A job can be refused a free lock, as $J_2$ is at time 1 in both examples.
- **Static knowledge.** The ceilings need the full list of the users of each semaphore. A task added later with a higher priority changes the ceilings.
- **No self-suspension.** A job that suspends inside a critical section breaks the bound, because the proof needs the top holder to be ready.

## Variants and improvements

- **Immediate ceiling.** When a job locks $S$, it runs at once at priority $\max(p, c(S))$, and it is not preempted by any job that could need $S$. A lock is then always free when asked for, a job blocks at most once and only before it starts, and the bound on $B_i$ is the same. This is the "highest locker" protocol, `PTHREAD_PRIO_PROTECT` in POSIX and `Ceiling_Locking` in Ada. It causes fewer context switches than the original, at the cost of more blocking in some runs.
- **Stack resource policy.** Baker gave each job a preemption level and each resource a ceiling, and let a job start only when its preemption level is above the system ceiling. This works with EDF as well as with fixed priorities, and all jobs can share one run-time stack.
- **Dynamic and multiprocessor forms.** The dynamic priority ceiling protocol uses deadlines for EDF. Multiprocessor protocols, for global and for partitioned scheduling, extend the ceiling idea to locks shared across processors.

## When to use it

Use it in a hard real-time system in which every task and every lock is known before the system runs, and you need a blocking bound of one critical section and freedom from deadlock without a global lock order. In practice the immediate form is more common, because it is simpler to build: raise the priority on lock and restore it on unlock. If the users of a lock are not known, use the [priority inheritance protocol](/priority-inheritance-protocol/).

## Pitfalls

- **A test with $\ge$.** Line L10 needs $p^*(j) > \Pi(j)$. With $\ge$, $J_2$ in the first example takes $B$ at time 1, and the two jobs deadlock.
- **Counting the own locks.** If $\Pi(j)$ in line L10 includes the semaphores that $j$ holds, the top holder is refused its own nested lock and the system stops.
- **Ceilings that are too low.** A ceiling must cover every task that may use the semaphore. One missing user makes the proof false.
- **Ties in the immediate form.** A job at the ceiling priority and a newly released job with the same base priority tie. Line L5 must keep the holder on the processor, or the new job runs and finds the lock taken.
- **Suspension in a critical section.** Waiting for input while a lock is held lets other jobs run and breaks the bound of one section.

## Implementations

## History

Sha, Rajkumar and Lehoczky described the priority ceiling protocol, with the basic inheritance protocol, in a Carnegie Mellon report in 1987, and published it in IEEE Transactions on Computers in 1990. Baker's stack resource policy of 1991 gave a form that suits EDF and a shared stack. The immediate ceiling form became the standard choice in POSIX, in Ada and in the OSEK and AUTOSAR operating systems for cars.

## References
