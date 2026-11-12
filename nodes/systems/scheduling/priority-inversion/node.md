---
tag: 3BZX31
kind: concept
slug: priority-inversion
name: Priority inversion
aliases:
- unbounded priority inversion
area: systems/scheduling
level: core
summary: "A high-priority job waits while a lower-priority job runs, often because the lower job holds a lock it needs. Without a protocol the wait has no bound."
prereqs: [fixed-priority-scheduling, mutex, critical-section]
see_also: [priority-inheritance-protocol, priority-ceiling-protocol, response-time-analysis, deadlock, starvation, spin-lock, semaphore, non-blocking-algorithm]
sources:
  - paper: doi:10.1109/12.57058
    title: "Lui Sha, Ragunathan Rajkumar and John P. Lehoczky, Priority inheritance protocols: an approach to real-time synchronization, IEEE Transactions on Computers 39(9) (1990), 1175-1185"
    locator: the introduction (the uncontrolled priority inversion problem) and the blocking bounds of the basic inheritance and the ceiling protocols
  - paper: doi:10.1145/358818.358824
    title: "Butler W. Lampson and David D. Redell, Experience with processes and monitors in Mesa, Communications of the ACM 23(2) (1980), 105-117"
    locator: the discussion of priorities and monitor locks
  - url: https://catless.ncl.ac.uk/Risks/19.49.html
    title: "Mike Jones, What really happened on Mars?, The RISKS Digest 19(49), 9 December 1997, with the reply of Glenn Reeves"
    locator: the account of the Mars Pathfinder resets
  - book: isbn:9781461406754
    title: "Giorgio C. Buttazzo, Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, third edition, Springer, 2011"
    locator: Chapter 7 (resource access protocols)
---

Priority inversion is a state in which a job of high priority waits while a job of lower priority runs. Under [fixed-priority scheduling](/fixed-priority-scheduling/) it comes mostly from shared resources: the high job needs a [mutex](/mutex/) that a low job holds, so it must wait until the low job leaves its [critical section](/critical-section/). This wait is necessary and short, but if jobs of medium priority preempt the low job, the wait grows with all of their work and has no bound. Protocols such as [priority inheritance](/priority-inheritance-protocol/) and the [priority ceiling protocol](/priority-ceiling-protocol/) put a bound on it, so that [response-time analysis](/response-time-analysis/) can count it.

## In plain words

Three people share one printer room, and the boss always goes first. A junior clerk goes in and locks the door to print a long report. Then the boss arrives with one page and must wait at the door. That wait is fair: the clerk will finish soon.

Now a middle manager comes and calls the clerk away for an hour of other work. The clerk still has the key. The boss waits for the full hour, behind a person with less rank who does not even use the printer. The order of rank is now upside down, and nobody can say how long the boss will wait.

The usual fix is simple: while the clerk holds the key that the boss needs, the clerk gets the boss's rank. The middle manager can then not call the clerk away.

## The idea

**The model.** One processor runs jobs of [periodic](/periodic-task-model/) or [sporadic](/sporadic-task-model/) tasks under preemptive fixed priorities: at each time the ready job of highest priority runs. Jobs share resources, and each resource is guarded by a binary [semaphore](/semaphore/) or a mutex. A job uses a resource only inside a critical section that starts with a lock and ends with an unlock. A job that asks for a lock that another job holds is blocked until the holder unlocks.

**Blocking and interference.** For a job $J$ of priority $p$, a time unit is *interference* when a job of higher priority runs. It is *blocking* when a job of lower priority runs while $J$ is released and not finished. Priority inversion is the set of blocking units. The worst total blocking of a job of task $\tau_i$ is written $B_i$.

**Bounded and unbounded inversion.** Let $J_H$, $J_M$ and $J_L$ have high, medium and low priority, and let $J_H$ and $J_L$ share a semaphore $S$.

1. $J_L$ locks $S$.
2. $J_H$ is released, preempts $J_L$, and asks for $S$. It is blocked. This *direct blocking* lasts at most the rest of the critical section of $J_L$.
3. $J_M$ is released. It does not need $S$, and its priority is higher than that of $J_L$, so it preempts $J_L$. $J_H$ now waits for all the work of $J_M$, and for any other medium job that comes.

The wait in step 2 is bounded by the length of one critical section. The wait in step 3 is not: its length depends on jobs that have no relation to $S$. This is *unbounded priority inversion*.

**What bounds it.** Each method below is a change to the lock rules or to the priorities, and each gives a bound on $B_i$.

| method | worst blocking of a job | other effects |
|---|---|---|
| no protocol | no bound in terms of critical sections | none |
| non-preemptive critical sections | one critical section of any lower job | blocks jobs that share nothing |
| [priority inheritance](/priority-inheritance-protocol/) | at most $\min(n, m)$ critical sections, for $n$ lower jobs and $m$ semaphores | chained blocking, no deadlock prevention |
| [priority ceiling](/priority-ceiling-protocol/) and its immediate form | at most one critical section | no deadlock, needs the ceilings in advance |

**How it enters the test.** For sporadic tasks with constrained deadlines, the response time $R_i$ is the least fixed point of

$$R_i = C_i + B_i + \sum_{j \in hp(i)} \left\lceil \frac{R_i}{T_j} \right\rceil C_j,$$

where $hp(i)$ is the set of tasks with higher priority. The task set is accepted if $R_i \le D_i$ for each $i$. With a blocking term, this [response-time test](/response-time-analysis/) is sufficient, not exact: $B_i$ is a worst case that a real run may not reach.

**Other sources.** A semaphore whose waiting queue is first in, first out, and not ordered by priority, also inverts priorities. A non-preemptive section in a driver or in the kernel does the same. On one processor, a high job that spins on a [spin lock](/spin-lock/) held by a preempted low job never lets the low job run, so the system stops. Priority inversion is not [deadlock](/deadlock/): the high job waits, but the chain of waits ends at a job that can run. It is also not [starvation](/starvation/), which is an unbounded wait for a turn in a fair system.

## Examples

**A trace.** The low job $L$ (priority 1, released at 0) locks $S$, runs 3 units, unlocks $S$, then runs 1 unit. The high job $H$ (priority 3, released at 1) locks $S$, runs 1 unit and unlocks. The medium job $M$ (priority 2, released at 2) runs $m$ units and uses no lock. For $m = 4$:

| slot | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| no protocol | L | L | M | M | M | M | L | H | L |
| priority inheritance | L | L | L | H | M | M | M | M | L |

With no protocol, $H$ is blocked from time 1 to time 7 and finishes at 8. For each $m$ it is blocked for $m + 2$ units, so the wait grows with $M$. With priority inheritance, $L$ runs at priority 3 while $H$ waits for $S$, so $M$ cannot preempt it. $H$ is blocked for 2 units and finishes at 4, for each $m$.

**Mars Pathfinder, 1997.** The lander used the VxWorks real-time kernel with preemptive priority scheduling. A high-priority task managed an information bus. A low-priority task that collected weather data published its results through a mutex that guarded the bus. A medium-priority communications task ran for a long time. When it preempted the weather task while that task held the mutex, the bus task waited too long. A watchdog saw that the bus task had not run and reset the system. The engineers found the cause in a trace on a copy of the system on Earth. The mutex had a parameter that turned on priority inheritance, and it was off. They turned it on by an upload that changed a global variable.

## Where it is used

- **Real-time kernels.** POSIX threads give the mutex protocols `PTHREAD_PRIO_INHERIT` and `PTHREAD_PRIO_PROTECT`. The first is priority inheritance and the second is the immediate ceiling form. Linux uses inheritance in its real-time mutexes and in priority-inheritance futexes. The Ada real-time annex has the `Ceiling_Locking` policy.
- **Analysis.** Each schedulability test for fixed priorities with shared resources has a blocking term $B_i$. Its value comes from the protocol, and the table above gives the usual bounds.
- **Design.** Short critical sections, [lock-free structures](/non-blocking-algorithm/) and message passing reduce or remove blocking. A design that has no shared lock between tasks of very different priority has no priority inversion from locks.

## References
