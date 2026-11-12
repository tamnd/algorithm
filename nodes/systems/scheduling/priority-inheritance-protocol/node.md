---
tag: 1XKZ0H
kind: algorithm
slug: priority-inheritance-protocol
name: Priority inheritance protocol
aliases:
- priority inheritance
area: systems/scheduling
level: advanced
summary: "A job that holds a lock runs at the highest priority of the jobs it blocks. This bounds priority inversion to at most min(n, m) critical sections."
solves: [real-time-scheduling]
model: word-ram
complexity:
  vars: {j: the number of jobs, a: the number of actions and time units in the run}
  time: {worst: O(a j^2)}
  space: {extra: O(j)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1990
  people: [Lui Sha, Ragunathan Rajkumar, John P. Lehoczky]
  note: Sha, Rajkumar and Lehoczky defined the basic priority inheritance protocol and the priority ceiling protocol in a 1987 report and in IEEE Transactions on Computers in 1990.
prereqs: [priority-inversion, semaphore]
see_also: [priority-ceiling-protocol, priority-inversion, response-time-analysis, fixed-priority-scheduling, deadlock, lock-ordering, wait-for-graph, mutex]
sources:
  - paper: doi:10.1109/12.57058
    title: "Lui Sha, Ragunathan Rajkumar and John P. Lehoczky, Priority inheritance protocols: an approach to real-time synchronization, IEEE Transactions on Computers 39(9) (1990), 1175-1185"
    locator: the basic priority inheritance protocol, its properties and its blocking bound
  - book: isbn:9781461406754
    title: "Giorgio C. Buttazzo, Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, third edition, Springer, 2011"
    locator: Chapter 7 (resource access protocols), the priority inheritance protocol
  - book: isbn:9780130996510
    title: Jane W. S. Liu, Real-Time Systems, Prentice Hall, 2000
    locator: Chapter 8 (resources and resource access control)
  - url: https://catless.ncl.ac.uk/Risks/19.49.html
    title: "Mike Jones, What really happened on Mars?, The RISKS Digest 19(49), 9 December 1997"
    locator: the Mars Pathfinder fault and the fix that turned on priority inheritance
---

The priority inheritance protocol is a lock rule for [fixed-priority scheduling](/fixed-priority-scheduling/) that stops unbounded [priority inversion](/priority-inversion/). When a job waits for a lock, the job that holds the lock runs at the priority of the waiting job, so a job of medium priority cannot preempt it. Sha, Rajkumar and Lehoczky proved in 1990 that a job is then blocked during at most $\min(n, m)$ critical sections, for $n$ jobs of lower priority and $m$ semaphores. It needs no knowledge of which job uses which lock, but it does not prevent deadlock.

## In plain words

A junior clerk holds the key to the printer room, and the boss waits at the door. While the boss waits, the clerk gets the boss's rank. Nobody of middle rank can call the clerk away, because the clerk now outranks them. When the clerk gives back the key, the clerk gets the old rank back, and the boss goes in.

If the clerk in turn waits for a key held by a second clerk, the second clerk also gets the boss's rank. The boss still has to wait for each clerk who holds a key on the path, but only for the time the key is held.

## The problem

One processor runs jobs under preemptive fixed priorities. Each job has a release time, a base priority and a list of actions: run for some time, lock a binary [semaphore](/semaphore/), unlock it. Critical sections are properly nested. The task model behind the jobs is the [periodic](/periodic-task-model/) or [sporadic](/sporadic-task-model/) model. The goal is a dispatch rule under which the time that a job waits for jobs of lower priority, its blocking time $B_i$, has a bound in terms of critical sections. With such a bound, the sufficient [response-time test](/response-time-analysis/) $R_i = C_i + B_i + \sum_{j \in hp(i)} \lceil R_i / T_j \rceil C_j \le D_i$ applies.

## The algorithm

The simulation below works in time units. Each job $x$ has a base priority $p(x)$ and a current priority $p^*(x)$. A job is *pending* from its release until it ends. A pending job that asked for a lock held by another job *waits* for the holder.

```pseudo id=main
PRIORITY-INHERITANCE(jobs)
L1  t ← 0
L2  while some job is not finished do
L3      for each pending job x that waits for a semaphore S do blocker(x) ← the holder of S
L4      p*(x) ← p(x) for all x; repeat p*(blocker(x)) ← max(p*(blocker(x)), p*(x)) until no change
L5      R ← the pending jobs with no blocker; j ← the job of R with the largest p*
L6      if R is empty then
L7          if some job is pending then stop: deadlock
L8          idle for one unit; t ← t + 1; go to L2
L9      if the next action of j is LOCK(S) then
L10         if S is free then j holds S else j waits for S
L11     else if the next action of j is UNLOCK(S) then free S
L12     else run j for one unit; t ← t + 1
```

Line L4 is the inheritance. It is transitive: if $x$ waits for $y$ and $y$ waits for $z$, then $z$ gets the priority of $x$. Because the loop starts from the base priorities in each step, a job falls back to the correct priority as soon as a waiter leaves: after an unlock, it keeps the highest priority of the jobs that still wait for its other locks. In a kernel, the same effect comes from a priority update along the chain of holders at each block and each unlock.

## Example

The job $J_3$ (priority 1, released at 0) locks $A$ for 3 units. The job $J_2$ (priority 2, released at 1) locks $B$, runs 1 unit, then locks $A$ for 1 unit. At time 3, $J_1$ (priority 4) asks for $B$, and $J_m$ (priority 3, 5 units) uses no lock.

| slot | runs | current priorities | what happens |
|---|---|---|---|
| 0 | $J_3$ | $J_3$: 1 | $J_3$ locks $A$ |
| 1 | $J_2$ | $J_2$: 2 | $J_2$ preempts $J_3$ and locks $B$ |
| 2 | $J_3$ | $J_3$: 2 | $J_2$ waits for $A$, so $J_3$ inherits 2 |
| 3 | $J_3$ | $J_2$: 4, $J_3$: 4 | $J_1$ waits for $B$; $J_2$ and, through it, $J_3$ inherit 4, so $J_m$ cannot run |
| 4 | $J_2$ | $J_2$: 4 | $J_3$ frees $A$; $J_2$ takes it, runs, then frees $A$ and $B$ |
| 5 | $J_1$ | $J_1$: 4 | $J_1$ takes $B$ and ends |
| 6 to 10 | $J_m$ | $J_m$: 3 | |

$J_1$ is blocked in slots 3 and 4, once by a critical section of $J_3$ and once by one of $J_2$. Without the transitive step, $J_3$ would keep priority 2 at time 3, and $J_m$ would run for 5 units while $J_1$ waits.

## Correctness

The claim is about a run with no deadlock. Lemma: if a job $L$ of lower base priority runs while $J$ is pending, then $L$ is inside an outermost critical section that it entered before $J$ was released. The reason: the chain of waits from $J$ ends at a ready job whose current priority is at least $p(J)$, so $L$ must have inherited a priority, so it holds a lock. If it had opened that lock after $r_J$, it would have run at its base priority while $J$ was pending, which line L5 does not allow. At the release of $J$ each lower job is in at most one outermost critical section, and two of them cannot start with the same semaphore. So $J$ is blocked during at most $\min(n, m)$ critical sections. The full proof is in the proofs folder.

## Complexity

- **Per decision.** Line L3 takes $O(j)$ time with a map from semaphores to holders. The loop of line L4 makes at most $j$ rounds over at most $j$ waiting jobs, so $O(j^2)$. Each lock, unlock or time unit is one decision, so a run of $a$ decisions takes $O(a j^2)$ time and $O(j)$ extra space.
- **In a kernel.** Inheritance costs one walk along the chain of holders at each block and each unlock, plus a priority-queue update for each job on the chain. The chain has at most $\min(n, m)$ links by the theorem.
- **Blocking.** $B_i$ is at most the sum, over the lower tasks, of the longest outermost critical section of each, and at most the sum over the $m$ semaphores of the longest critical section that a lower task holds on each.

## Properties

- **No knowledge in advance.** The protocol needs no list of the locks that each task uses. This is why kernels can offer it as a mutex option.
- **Bounded blocking.** A job is blocked by at most $\min(n, m)$ critical sections, and jobs of medium priority that use no lock do not add to the blocking.
- **Chained blocking.** A job can be blocked once by each of several lower jobs, as $J_1$ in the example.
- **No deadlock prevention.** Two jobs that lock $A$ and $B$ in opposite orders can still deadlock. Line L7 reports it.
- **Push-through blocking.** A job of medium priority can be blocked by a low job that inherited a high priority, even if the medium job uses no lock.

## Variants and improvements

- **[Priority ceiling protocol](/priority-ceiling-protocol/).** It adds a lock rule based on ceilings. A job is then blocked by at most one critical section, and deadlock is not possible.
- **Immediate ceiling.** A job takes the ceiling of a lock as soon as it locks it. This is `PTHREAD_PRIO_PROTECT` in POSIX.
- **Kernel mutexes.** POSIX gives priority inheritance as `PTHREAD_PRIO_INHERIT`, and Linux uses it in its real-time mutexes and priority-inheritance futexes.
- **Other schedulers.** Under EDF the same idea passes deadlines instead of priorities. For reservation servers such as the [constant bandwidth server](/constant-bandwidth-server/), bandwidth inheritance lets the holder use the budget of the waiting server.

## When to use it

Use priority inheritance when tasks share locks and you cannot list in advance which task uses which lock, for example in a general-purpose kernel or a library. Add a global order of locks, as in [lock ordering](/lock-ordering/), to prevent deadlock. If the locks of each task are known and you need a bound of one critical section, use the [priority ceiling protocol](/priority-ceiling-protocol/) instead.

## Pitfalls

- **Inheritance that is not transitive.** If line L4 makes only one round, the holder at the end of a chain keeps a low priority, and a medium job can run for an unbounded time, as $J_m$ would in the example.
- **Reset to the base priority on unlock.** A job that frees one lock but still holds another must keep the priority of the jobs that wait for the other lock. Line L4 recomputes $p^*$ from the base priorities in each step, which does this right; code that sets $p^* = p$ at each unlock does not.
- **A wait queue in arrival order.** When line L11 frees a semaphore, the waiter of highest priority must get it next. A first-in, first-out queue lets a low waiter take it first, which is a new inversion.
- **Expecting freedom from deadlock.** Line L10 grants any free lock, so lock cycles are possible. Use a lock order, or the ceiling protocol.
- **Forgetting the option.** On Mars Pathfinder in 1997, the mutex that caused the resets had priority inheritance as an option, and it was off.

## Implementations

## History

Lampson and Redell described in 1980 how locks in the Mesa system interact with priorities. Sha, Rajkumar and Lehoczky defined the basic priority inheritance protocol and the priority ceiling protocol in a Carnegie Mellon report in 1987, and published them in IEEE Transactions on Computers in 1990, with the bound of $\min(n, m)$ critical sections. In 1997 the Mars Pathfinder lander reset itself several times because of a priority inversion. The fix turned on the inheritance option of a VxWorks mutex, and the case made the protocol widely known.

## References
