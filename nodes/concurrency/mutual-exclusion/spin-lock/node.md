---
tag: S4E1T8
kind: algorithm
slug: spin-lock
name: Spin lock
aliases: [busy-waiting lock, test-and-test-and-set lock]
area: concurrency/mutual-exclusion
level: intro
summary: A lock whose waiters busy-wait on shared memory. The main form reads the lock word until it is free, then tries test-and-set, and backs off for a random time if it fails.
solves: [mutual-exclusion-problem]
complexity:
  space: {shared: Θ(1)}
  steps: {solo: Θ(1)}
  rmr: {cc: ∞, dsm: ∞}
properties: {deterministic: false, deadlock_free: true, starvation_free: false, fcfs: false, local_spinning: false}
history:
  year: 1990
  people: [Larry Rudolph, Zary Segall, Thomas E. Anderson, Gary Graunke, Shreekant Thakkar, John M. Mellor-Crummey, Michael L. Scott]
  note: Rudolph and Segall proposed test-and-test-and-set in 1984. Anderson (1990) measured the spin lock family and added exponential backoff and the array lock. Mellor-Crummey and Scott (1991) gave the MCS queue lock.
prereqs: [test-and-set, mutex]
see_also: [ticket-lock, anderson-lock, mcs-lock, clh-lock, cohort-lock, exponential-backoff, ski-rental-problem, rmr-complexity]
sources:
  - paper: doi:10.1109/71.80120
    title: Thomas E. Anderson, The performance of spin lock alternatives for shared-memory multiprocessors, IEEE Transactions on Parallel and Distributed Systems 1(1), 1990, pages 6-16
    locator: spin on test-and-set, spin on read (test-and-test-and-set), delay after a failed test-and-set with exponential backoff, and the array-based queue lock
  - paper: doi:10.1145/103727.103729
    title: John M. Mellor-Crummey and Michael L. Scott, Algorithms for scalable synchronization on shared-memory multiprocessors, ACM Transactions on Computer Systems 9(1), 1991, pages 21-65
    locator: Section 2, the simple test-and-set lock with backoff, the ticket lock, Anderson's lock and the MCS lock, with the empirical comparison
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 7, Spin Locks and Contention (TAS, TTAS, the BackoffLock, the queue locks)
  - paper: "Anna R. Karlin, Kai Li, Mark S. Manasse and Susan Owicki, Empirical studies of competitive spinning for a shared-memory multiprocessor, Proceedings of the 13th ACM Symposium on Operating Systems Principles (SOSP), 1991"
    locator: the spin then block rule, its competitive ratio of 2, and the randomized and adaptive variants
  - paper: "Larry Rudolph and Zary Segall, Dynamic decentralized cache schemes for MIMD parallel processors, Proceedings of the 11th International Symposium on Computer Architecture (ISCA), 1984"
    locator: the test-and-test-and-set idea, which reads the lock word in the cache before it tries test-and-set
---

A spin lock is a [mutex](/mutex/) in which a waiting process busy-waits: it keeps reading shared memory until the lock is free, instead of asking the operating system to put it to sleep. The family runs from the plain [test-and-set](/test-and-set/) lock, through test-and-test-and-set with exponential backoff, to the [ticket lock](/ticket-lock/) and the queue locks of [Anderson](/anderson-lock/), [Mellor-Crummey and Scott](/mcs-lock/) and [Craig, Landin and Hagersten](/clh-lock/). This page gives test-and-test-and-set with exponential backoff (TTAS-BO) as the main algorithm, and the rule of spinning for a while before blocking, which is 2-competitive.

## In plain words

A spin lock is a door with a sign that says "busy" or "free". A person who wants to go in keeps looking at the sign. When the sign says "free", the person grabs the door handle and turns the sign to "busy" in one move. If somebody else was faster, the person steps back for a short random time before looking again, and waits a bit longer after each miss.

Looking at the sign is cheap, because each person sees a copy of it on their own desk. Grabbing the handle is expensive, because everybody's copy must be updated. So people look a lot and grab rarely.

Spinning is good when the wait is short. If the wait may be long, it is better to look for a while and then go to sleep.

## The problem

The [mutual exclusion problem](/mutual-exclusion-problem/) for $n$ processes: each process repeats a remainder section, an entry section, a critical section and an exit section, and at most one process may be in its critical section at a time. The model is $n$ asynchronous processes on a sequentially consistent shared memory. The objects are atomic registers (consensus number 1) and one [test-and-set](/test-and-set/) bit (consensus number 2). The cost measure is the number of remote memory references (RMRs) in the cache coherent (CC) and distributed shared memory (DSM) models; see [RMR complexity](/rmr-complexity/). We write $k$ for the number of processes that contend at the same time.

## The algorithm

The lock is one word $L$, false when the lock is free. $MIN$ and $MAX$ are the smallest and the largest backoff limits.

```pseudo id=main
LOCK()                                 ▷ test-and-test-and-set with backoff
L1  delay ← MIN
L2  loop
L3      while L = true do nothing      ▷ spin on the cached copy
L4      if TAS(L) = false then return  ▷ the lock is ours
L5      wait for a random time in [0, delay)
L6      delay ← min(2 · delay, MAX)
UNLOCK()
L7  L ← false
```

The plain TAS lock is L4 alone in a loop: `while TAS(L) = true do nothing`. The TTAS lock is L2 to L4 without L5 and L6. L3 is the "test" before the "test-and-set": a read hits in the cache while the lock stays held, and only a release makes it miss. L4 is the only atomic step. L5 and L6 are the backoff: after a failed TAS, the process knows that others contend, so it waits for a random time before it reads again, and it doubles the limit up to $MAX$.

**Spin then block.** When the holder may be descheduled, a waiter should not spin forever. Let $C$ be the cost of blocking (the context switches of a sleep and a wake up), and let spinning cost 1 per unit of time. The rule: spin for at most $C$ time units; if the lock is still held, block. The function `spin_then_block` in the implementation gives the cost of this rule.

## Example

Two processes run TTAS-BO with $MIN = 1$, from the free state. This is the kind of run that the test file explores.

| step | process | line | action | $L$ after |
|---|---|---|---|---|
| 1 | 0 | L3 | reads false (a cache miss) | false |
| 2 | 1 | L3 | reads false (a cache miss) | false |
| 3 | 0 | L4 | TAS returns false, enters | true |
| 4 | 1 | L4 | TAS returns true (a miss: the line moves) | true |
| 5 | 1 | L5 | coin in $[0, 1)$ is 0, no wait | true |
| 6 | 1 | L6 | $delay \leftarrow 2$ | true |
| 7 to 20 | 1 | L3 | reads true from its cache, no traffic | true |
| 21 | 0 | L7 | leaves: $L \leftarrow$ false (invalidates the copy of 1) | false |
| 22 | 1 | L3 | reads false (a miss) | false |
| 23 | 1 | L4 | TAS returns false, enters | true |

While process 0 is inside, process 1 makes no remote references. With the plain TAS lock, each of the steps 7 to 20 would be a TAS, so each would be a remote reference. The test file measures this: over 200 steps of a waiter while the lock is held, a TAS waiter makes 199 RMRs in the CC model, and a TTAS waiter makes 1.

## Correctness

The full proof is in proofs/correctness.md. It shows four facts.

- **Mutual exclusion.** A process enters only when its TAS at L4 returns false. After such a TAS, $L$ is true until the holder writes false at L7, so no other TAS returns false in between.
- **Deadlock freedom.** If no process enters from some time on, the last holder has left, $L$ stays false, and the next process to reach L3 passes it and wins its TAS at L4. Backoff waits are finite because $delay \le MAX$.
- **No starvation freedom.** The run on the [test-and-set](/test-and-set/) page also works here: the holder can leave and take the lock again before the waiter's next TAS, forever. The test file finds such a cycle for two processes.
- **Spin then block is 2-competitive.** For every wait time $w$, the cost of the rule is at most $2 \min(w, C)$, which is twice the cost of an offline waiter that knows $w$. No deterministic rule has a ratio below 2.

The test file checks mutual exclusion over all interleavings for two processes with two passages each and for three processes, checks deadlock freedom and finds the starvation cycle when two processes run forever, and runs random schedules for up to 4 processes.

## Complexity

| measure | TAS | TTAS | TTAS-BO |
|---|---|---|---|
| shared words | 1 | 1 | 1 |
| steps without contention | 2 | 3 | 3 |
| CC RMRs while the lock is held | one per step | one per release | one per release |
| CC traffic for one release with $k$ waiters | $\Theta(k)$ per step | $\Theta(k)$ misses and up to $k$ TAS | fewer TAS, spread out in time |
| RMRs per passage, CC and DSM | unbounded | unbounded | unbounded |

A TTAS waiter makes one CC miss for each write to $L$ while it waits. Other processes may enter and leave any number of times before it wins, so no lock of this family has a bound on the RMRs of one passage. The test file finds the maximum passage cost infinite for all three locks. In the DSM model $L$ lives in one memory module, so every read of L3 is remote for all but one process.

After a release with $k$ waiters, each TTAS waiter misses on its read of L3 and then tries TAS. The first TAS wins, and the other $k - 1$ each take the line away from the others. This burst is what backoff spreads out. For the spin then block rule, the space is one word and the time is in units of spinning; the ratio is 2.

## Properties

- Needs one test-and-set (or swap, or compare-and-swap) per attempt, and plain reads and writes.
- Deadlock free, not starvation free, not FCFS: the last process to read false wins, and backoff favors processes with a short current delay, so newcomers often beat old waiters.
- Randomized, because of the backoff in L5. Without L5 and L6 it is deterministic.
- Spins on a word that every waiter shares; there is no local spinning in the RMR sense.
- Unlock is one plain write, so any process may unlock: the lock does not record an owner.

## Variants and improvements

- **TAS lock.** Only L4 in a loop. Simplest, and worst under contention, because every attempt is a write that moves the cache line.
- **TTAS lock** (Rudolph and Segall 1984). Adds L3. Waiters spin in their caches, but each release still sends all of them to TAS at once.
- **TTAS with exponential backoff** (Anderson 1990). This page. The limit doubles, as in [exponential backoff](/exponential-backoff/) for Ethernet. The constants $MIN$ and $MAX$ must be tuned to the machine.
- **Ticket lock.** A [fetch-and-add](/fetch-and-add/) counter gives FIFO order; backoff can be proportional to the distance to the front. See [ticket lock](/ticket-lock/).
- **Queue locks.** Each waiter spins on its own word: [Anderson's array lock](/anderson-lock/) (and Graunke and Thakkar 1990), the [MCS lock](/mcs-lock/) and the [CLH lock](/clh-lock/). They are FIFO and make $O(1)$ RMRs per passage in the CC model.
- **Hierarchical and NUMA locks.** The [cohort lock](/cohort-lock/) keeps the lock inside one NUMA node for a few passages.
- **Spin then block.** Spin for about the cost $C$ of blocking, then block. This is the [ski rental problem](/ski-rental-problem/) in a new form. A randomized threshold gives the expected ratio $e/(e - 1) \approx 1.58$ (Karlin, Manasse, McGeoch and Owicki). Most production mutexes, for example the adaptive mutexes of Solaris and glibc, spin briefly before they sleep.

## When to use it

Use a spin lock when critical sections are short (a few hundred instructions), the holder is not descheduled while it holds the lock, and contention is low: for example inside an operating system kernel with preemption off, or for a lock that guards a few words. Use TTAS-BO or a ticket lock for low contention. Use a queue lock when many processors contend. Use a blocking [mutex](/mutex/), or spin then block, in user code where threads may outnumber processors.

## Pitfalls

**Spinning with TAS.** The wrong line is `while TAS(L) = true do nothing`: every attempt writes the cache line and slows the holder too. The right line is L3 before L4: `while L = true do nothing`, then one TAS.

**Backoff on the wrong branch.** The wrong code backs off after L3 sees the lock held. That only delays the waiter. The right place is after a failed TAS at L4, which is the evidence of contention.

**No memory order.** On weak memory models the release must be a release store and the successful TAS an acquire operation. A plain store at L7 may let writes of the critical section become visible after the lock looks free. In C11 write `atomic_store_explicit(&L, false, memory_order_release)` at L7, not `L = false` on a plain variable.

**Preemption of the holder.** If the holder is descheduled, every waiter spins for its whole time slice. Use spin then block, or turn off preemption while holding a kernel spin lock.

**Priority inversion.** A low priority holder and a high priority spinner on one processor can spin forever. See [priority inversion](/priority-inversion/).

## Implementations

## History

Test-and-set instructions appeared in the 1960s, and the plain TAS lock with them. Rudolph and Segall (1984) suggested reading the lock word in the cache before the TAS. Anderson (1990) showed by measurement that TAS and TTAS both slow down badly with many processors, and proposed exponential backoff and an array-based queue lock; Graunke and Thakkar (1990) proposed a similar queue lock. Mellor-Crummey and Scott (1991) compared the family and gave the MCS lock. Ousterhout (1982) proposed waiting by spinning first and then blocking, and Karlin, Li, Manasse and Owicki (1991) studied the competitive analysis of this rule.

## References
