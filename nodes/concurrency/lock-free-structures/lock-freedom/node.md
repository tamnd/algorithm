---
tag: NXBV97
kind: definition
slug: lock-freedom
name: Lock-freedom
aliases:
- lock-free progress
- lock-free
area: concurrency/lock-free-structures
level: core
summary: A progress condition. In every infinite run, infinitely many operations complete, whatever the scheduler does. The system always progresses, but one process can starve.
prereqs: [non-blocking-algorithm, compare-and-swap]
see_also: [wait-freedom, obstruction-freedom, non-blocking-algorithm, deadlock-freedom, treiber-stack, michael-scott-queue, helping, livelock]
sources:
  - paper: doi:10.1145/161468.161469
    title: Maurice Herlihy, A methodology for implementing highly concurrent data objects, ACM Transactions on Programming Languages and Systems 15(5), 1993
    locator: pages 745 to 770 (the condition, under the name non-blocking, and lock-free objects built with load-linked/store-conditional)
  - paper: doi:10.1007/978-3-642-25873-2_22
    title: Maurice Herlihy and Nir Shavit, On the nature of progress, OPODIS 2011, LNCS 7109
    locator: pages 313 to 328 (lock-freedom as the independent condition with minimal progress)
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: Chapter 3, the section on progress conditions; Chapter 11 (the lock-free stack)
  - paper: doi:10.1145/2591796.2591836
    title: Dan Alistarh, Keren Censor-Hillel and Nir Shavit, Are lock-free concurrent algorithms practically wait-free?, STOC 2014
    locator: pages 714 to 723 (under a stochastic scheduler, a lock-free algorithm is wait-free with probability 1)
  - paper: doi:10.1145/114005.102808
    title: Maurice Herlihy, Wait-free synchronization, ACM Transactions on Programming Languages and Systems 13(1), 1991
    locator: pages 124 to 149 (the consensus hierarchy, which also bounds lock-free implementations of one-shot objects)
---

Lock-freedom is a progress condition for a concurrent object: in every infinite run, infinitely many operations complete. The scheduler can do anything, and processes can crash, but the object as a whole keeps making progress. It is a guarantee about the system, not about one operation: a single process can retry for ever while the others complete operations. Lock-freedom sits between [wait-freedom](/wait-freedom/), which also promises that each operation completes, and [obstruction-freedom](/obstruction-freedom/), which only promises progress to a process that runs alone.

## Definition

**Notation and model.** $n$ is the number of processes, $p$ and $q$ are processes, and $k$ is the contention. Processes are asynchronous and can crash between steps. Memory is sequentially consistent. The primitives are atomic steps; most lock-free code uses [compare-and-swap](/compare-and-swap/) or [LL/SC](/load-linked-store-conditional/).

A *run* is a finite or infinite sequence of steps of an implementation, where each process calls operations of the object one after the other.

**Definition.** An implementation is **lock-free** if every infinite run has infinitely many completed operations.

Equivalent form: from every reachable state in which some operation is pending, every infinite continuation of the run completes an operation. A crashed process takes only finitely many steps, so it cannot keep a run infinite on its own, and the steps of crashed processes do not help or hurt.

An implementation is **bounded lock-free** with bound $B$ if every $B$ consecutive steps of a run contain the completion of an operation. The bound counts the steps of all processes. It is a bound for the system, not for an operation: lock-freedom gives no bound on the number of steps of a single operation, and no bound in which a given process completes anything.

Three consequences of the definition:

1. **Per object, not per operation.** The condition talks about the completions of all processes together. "Process $p$ will finish" does not follow, even if $p$ runs in every round. If every process must finish, you need [wait-freedom](/wait-freedom/).
2. **Finite workloads finish.** If each process calls only finitely many operations, every operation of a correct process completes: an infinite run would contain infinitely many steps but only finitely many completions. In particular, a lock-free implementation of a one-shot object such as consensus, where each process calls one operation, is in effect wait-free, and Herlihy's [consensus number](/consensus-number/) bounds apply to it. For example, no lock-free consensus for two processes exists with only read/write registers.
3. **Composition.** A system of several lock-free objects is lock-free: an infinite run takes infinitely many steps in some object, and that object then completes infinitely many operations.

**The CAS retry loop.** Most lock-free operations have this shape: read the shared state, compute a new state, and try to install it with one CAS; on failure, start again. The proof of lock-freedom is always the same. A CAS fails only if the word changed since the read, and only a successful CAS of another operation changes it. So every failure is paid for by a success.

**Lemma (Treiber push).** Let $n$ processes each run a sequence of Treiber pushes: read `top`, then CAS(`top`, read value, new node), and repeat on failure. In every run, at most $2n - 1$ steps in a row pass without a completed push.

*Proof.* Consider a stretch of steps with no successful CAS. A CAS in the stretch fails, so `top` changed after the read of that process; no success happened in the stretch, so that read was before the stretch. Hence each process makes at most one failed CAS in the stretch, whose read lies before the stretch. After its failure, its next steps are a read and then a CAS. The read sees the current `top`, and the CAS would succeed because no success happens in the stretch. So each process takes at most 2 steps in the stretch (a failed CAS and a read). The process $q$ that made the last success before the stretch has no stale read, so it takes at most 1 step (a read). That is at most $2(n - 1) + 1 = 2n - 1$ steps. $\square$

So the Treiber push is bounded lock-free with $B = 2n$. It is not wait-free, as the first example shows.

## Examples and non-examples

The numbers come from the tests in the implementation folder, which run the interleaving explorer.

**Lock-free, and a process starves.** Two processes push for ever. The schedule repeats four steps: $p_0$ reads `top`; $p_1$ reads `top`; $p_1$'s CAS succeeds; $p_0$'s CAS fails. After 1000 rounds, each process has taken 2000 steps, $p_1$ has completed 1000 pushes, and $p_0$ none. This schedule is fair: both processes take steps all the time. So lock-freedom does not imply starvation-freedom, even under a fair scheduler.

**The bound is tight.** The explorer computes the longest stretch with no completed push over all runs. With 2 processes and 3 pushes each it is 3, and with 3 processes and 2 pushes each it is 5, both equal to $2n - 1$. With 3 processes and 1 push each it is 4, because a process that has finished takes no more steps. With finite workloads, every run ends: the explorer visits all 78 states for 2 processes with 2 pushes each and all 3014 states for 3 processes with 2 pushes each, and finds no run longer than the depth bound.

**Blocking: a stack with a spin lock.** The same push under a [test-and-set](/test-and-set/) lock. Process $p_0$ takes the lock and then stops. Process $p_1$, running alone, comes back to the same state after one step (a failed test-and-set), so it spins for ever, and no operation completes. The implementation is [deadlock-free](/deadlock-freedom/) only under the assumption that the lock holder keeps running.

**Other lock-free objects.** The [Treiber stack](/treiber-stack/), the [Michael and Scott queue](/michael-scott-queue/), the [Harris linked list](/harris-linked-list/), [split-ordered lists](/split-ordered-list/) and the [elimination backoff stack](/elimination-backoff-stack/) are lock-free and not wait-free.

**Not lock-free, though it uses no locks.** Code without any mutex can still block. A thread that spins until another thread sets a flag (a hand-made lock, or the retry loop of a reader of a sequence lock while a writer is stopped in the middle) makes no progress when the other thread stops. "Lock-free" is a property of the runs, not of the instructions used.

**Not lock-free: obstruction-free only.** The deque of Herlihy, Luchangco and Moir can livelock: two operations at the two ends can make each other retry for ever with no completion. See [obstruction-freedom](/obstruction-freedom/).

## Related definitions

- [Wait-freedom](/wait-freedom/) is the stronger condition: each operation completes in a finite number of its own steps. A lock-free design becomes wait-free with [helping](/helping/), at a cost.
- [Obstruction-freedom](/obstruction-freedom/) is the weaker condition: an operation completes if it runs alone long enough. Lock-freedom implies it. The difference is a [livelock](/livelock/), which lock-freedom forbids and obstruction-freedom allows.
- [Deadlock-freedom](/deadlock-freedom/) is the blocking counterpart: minimal progress, but only in fair runs where no process stops while it holds a lock. Lock-freedom gives minimal progress in every run.
- [Non-blocking algorithm](/non-blocking-algorithm/) is the family of all three non-blocking conditions. Older papers, such as Herlihy (1993), use "non-blocking" to mean exactly lock-free.
- In practice, the starvation of the first example needs a very unlucky schedule. Alistarh, Censor-Hillel and Shavit (2014) showed that under a stochastic scheduler, a lock-free algorithm is wait-free with probability 1, and they bounded the expected latency for a class of algorithms. Under an adversarial scheduler, the starvation is real.
- Lock-freedom of an object also needs lock-free memory management. Freeing nodes with an epoch scheme can block when one thread stops; [hazard pointers](/hazard-pointers/) do not.

## References
