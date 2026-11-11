---
tag: V63Y97
kind: definition
slug: obstruction-freedom
name: Obstruction-freedom
aliases:
- obstruction-free progress
- obstruction-free
- solo termination
area: concurrency/lock-free-structures
level: advanced
summary: A progress condition. An operation completes if, from some point on, it runs alone for long enough. Weaker than lock-freedom, since two processes can stop each other for ever.
prereqs: [lock-freedom]
see_also: [lock-freedom, wait-freedom, livelock, non-blocking-algorithm, consensus-number, helping, deadlock-freedom, compare-and-swap]
sources:
  - paper: doi:10.1109/ICDCS.2003.1203503
    title: Maurice Herlihy, Victor Luchangco and Mark Moir, Obstruction-free synchronization, double-ended queues as an example, ICDCS 2003
    locator: the definition of obstruction-freedom, the array-based deque and its figure of code, and the part on contention managers
  - paper: doi:10.1007/978-3-642-25873-2_22
    title: Maurice Herlihy and Nir Shavit, On the nature of progress, OPODIS 2011, LNCS 7109
    locator: pages 313 to 328 (obstruction-freedom as a dependent non-blocking condition; clash-freedom)
  - paper: doi:10.1007/11561927_11
    title: Hagit Attiya, Rachid Guerraoui and Petr Kouznetsov, Computing with reads and writes in the absence of step contention, DISC 2005, LNCS 3724
    locator: pages 122 to 136 (obstruction-free implementations of any object from registers)
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: Chapter 3, the section on progress conditions (obstruction-freedom and dependent progress conditions)
  - paper: doi:10.1145/1073814.1073861
    title: William N. Scherer III and Michael L. Scott, Advanced contention management for dynamic software transactional memory, PODC 2005
    locator: contention managers for obstruction-free transactional memory
---

Obstruction-freedom is the weakest of the three common non-blocking progress conditions: an operation must complete if, from some point on, it runs alone for long enough. Herlihy, Luchangco and Moir defined it in 2003. It allows a livelock, where two processes keep stopping each other's operations, but it does not allow a process that has stopped to block the others. So a crash never blocks the system, and the job of avoiding livelock goes to a separate *contention manager*.

## Definition

**Notation and model.** $n$ is the number of processes, $p$ and $q$ are processes, $i$ and $k$ are indices. Processes are asynchronous and can crash between steps. Memory is sequentially consistent. A *solo run* of $p$ from a state is a run in which only $p$ takes steps.

**Definition.** An implementation is **obstruction-free** if, from every reachable state, every solo run of a process $p$ completes the pending operation of $p$ in a finite number of steps.

The other processes may be stopped in the middle of an operation, in any state. They count only as part of the starting state; they take no steps in the solo run. An implementation has a **solo bound** $B$ if every such solo run completes within $B$ steps of $p$.

Equivalently: in every run, an operation of $p$ completes if $p$ eventually takes steps alone, for long enough. This is the form in which Herlihy, Luchangco and Moir gave it: a thread that eventually runs in isolation completes its operation in a finite number of steps.

**What it allows.** Two operations that run at the same time can make each other retry for ever. That is a [livelock](/livelock/): both processes take steps, and no operation completes. Lock-freedom forbids it.

**What it forbids.** A process cannot wait for another process. A lock is not obstruction-free: if the holder stops, the others spin alone for ever. So obstruction-freedom is still non-blocking: a crashed process never stops the rest.

**Place in the hierarchy.** Wait-free implies lock-free, and lock-free implies obstruction-free. Proof of the second step: suppose a solo run of $p$ never completes the pending operation of $p$. Then the run is infinite, and only $p$ takes steps, so only $p$ can complete operations in it. The pending operation of $p$ comes before any later operation of $p$, so no operation completes at all. That breaks lock-freedom. In the table of Herlihy and Shavit (2011), obstruction-freedom is the *dependent* non-blocking condition with maximal progress: it guarantees progress only under a condition on the scheduler (isolation). Its minimal counterpart is *clash-freedom*.

**Contention managers.** The designer splits the job in two. The algorithm only needs to be correct (linearizable) and obstruction-free. A contention manager decides, on each retry, whether to back off, wait, or abort the other process, so that in practice one operation runs alone long enough. Randomized exponential backoff is the simplest manager. Scherer and Scott (2005) compared many managers (for example Karma and Polka) for obstruction-free transactional memory. The manager can change performance, but it cannot break correctness, since the algorithm is correct under every schedule.

**Power.** Obstruction-freedom is outside the [consensus hierarchy](/consensus-number/). Herlihy's bounds are about wait-free (and so lock-free) objects. With only read/write registers, obstruction-free consensus exists for any $n$, and Attiya, Guerraoui and Kouznetsov (2005) showed that any object has an obstruction-free implementation from registers. So the step from obstruction-free to lock-free needs stronger primitives, or a scheduler with some timing guarantees.

### The deque of Herlihy, Luchangco and Moir

The 2003 paper gave a double-ended queue as the example. It needs only single-word CAS, and it is simpler than the lock-free deques of that time. The deque lives in an array $A[0..m+1]$ of pairs (value, counter). A value is LN (left null), RN (right null) or data, and the array always has the form LN+ data* RN+. Every CAS adds 1 to the counter of the cell it writes, which defeats the [ABA problem](/aba-problem/). An *oracle* gives a guess at the edge; the operation checks the guess, so a wrong guess only costs a retry.

```text
rightpush(v):
  loop
    k := oracle(right)            // a guess at the leftmost RN
    prev := A[k-1]; cur := A[k]
    if prev.val != RN and cur.val = RN then
      if k = m+1 then return "full"
      if CAS(A[k-1], prev, (prev.val, prev.ctr+1)) then
        if CAS(A[k], cur, (v, cur.ctr+1)) then return "ok"

rightpop():
  loop
    k := oracle(right)
    cur := A[k-1]; next := A[k]
    if cur.val != RN and next.val = RN then
      if cur.val = LN and A[k-1] = cur then return "empty"
      if CAS(A[k], next, (RN, next.ctr+1)) then
        if CAS(A[k-1], cur, (RN, cur.ctr+1)) then return cur.val
```

The left operations are the mirror image, with LN in place of RN and $k+1$ in place of $k-1$.

The first CAS of each operation writes the same value back with a new counter. It changes nothing in the deque, but it makes the second CAS of any other operation that read the old cell fail. So two operations that touch the same pair of cells cannot both succeed.

**Why it is obstruction-free.** Let $p$ run alone from any state. Its current attempt can fail, because it may hold old values. Its next attempt starts with fresh reads, and no other process takes steps, so the check passes and both CAS steps succeed (or the operation returns "full" or "empty"). So $p$ finishes within the rest of one attempt plus one full attempt: at most about $2(m + 6)$ steps with a scan oracle.

**Why it is not lock-free.** On an empty deque, let $p$ run rightpush and $q$ run leftpush at the same boundary. Both read the two boundary cells. $p$ bumps the counter of the LN cell, $q$ bumps the counter of the RN cell, and then both second CAS steps fail, because each one wrote the cell that the other wanted. They start again, and the same four steps repeat for ever.

## Examples and non-examples

The numbers come from the tests in the implementation folder, which run the interleaving explorer and the linearizability checker from [linearizability](/linearizability/) on the deque with a scan oracle.

**Obstruction-free, not lock-free: the deque.** The livelock schedule above, run for 1000 rounds on an array LN LN RN RN, gives 6000 steps to each process, no completed operation, and an empty deque. The counters of the two boundary cells are both 1000.

**The solo bound, measured.** From every state reached in at most 24 steps, for 7 workloads of two operations (pushes and pops at both ends, on an empty deque and on deques with one or two items, array LN LN LN, items, RN RN RN), each process running alone finished in at most 11 steps. For two processes with two operations each it was at most 17 steps, for both operations.

**Linearizable on small cases.** Every history of every run of at most 24 steps of these 8 workloads, with pending operations included, is linearizable for the sequential deque. This is a check of small cases, not a proof; the paper gives the proof.

**Lock-free, so also obstruction-free.** The [Treiber stack](/treiber-stack/) and the [Michael and Scott queue](/michael-scott-queue/).

**Not obstruction-free: any lock.** A [test-and-set](/test-and-set/) lock whose holder stops makes every other process spin alone for ever. The lock is [deadlock-free](/deadlock-freedom/), a blocking condition.

**Obstruction-free from registers: consensus.** Obstruction-free consensus for any number of processes can be built from read/write registers alone, for example with the general construction of Attiya, Guerraoui and Kouznetsov. No wait-free or lock-free one exists, because registers have [consensus number 1](/registers-have-consensus-number-one/). So this is a task where the gap between obstruction-freedom and lock-freedom is a gap in power, not only in performance.

## Related definitions

- [Lock-freedom](/lock-freedom/): in every infinite run, infinitely many operations complete. It forbids livelock.
- [Wait-freedom](/wait-freedom/): every operation completes in a finite number of its own steps.
- [Livelock](/livelock/): the failure that obstruction-freedom allows and lock-freedom forbids.
- *Clash-freedom*: the minimal-progress counterpart of obstruction-freedom in the table of Herlihy and Shavit.
- [Non-blocking algorithm](/non-blocking-algorithm/): the family of all three conditions.
- *Practically wait-free*: Fich, Luchangco, Moir and Shavit (DISC 2005) showed how to turn an obstruction-free algorithm into one that is wait-free in a partially synchronous model, where step times have an unknown bound.

## References
