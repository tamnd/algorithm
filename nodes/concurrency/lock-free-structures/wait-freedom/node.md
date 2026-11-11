---
tag: Y8SZMW
kind: definition
slug: wait-freedom
name: Wait-freedom
aliases:
- wait-free progress
- wait-free
area: concurrency/lock-free-structures
level: core
summary: A progress condition. Each operation completes in a finite number of its own steps, whatever the other processes do. Bounded wait-freedom also fixes a bound on that number.
prereqs: [lock-freedom]
see_also: [lock-freedom, obstruction-freedom, helping, universal-construction, consensus-number, afek-atomic-snapshot, kogan-petrank-queue, starvation-freedom]
sources:
  - paper: doi:10.1145/114005.102808
    title: Maurice Herlihy, Wait-free synchronization, ACM Transactions on Programming Languages and Systems 13(1), 1991
    locator: pages 124 to 149 (the definition of wait-freedom, the consensus hierarchy and the universal construction)
  - paper: doi:10.1145/62546.62593
    title: Maurice Herlihy, Impossibility and universality results for wait-free synchronization, PODC 1988
    locator: pages 276 to 290 (the conference version of the results above)
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: Chapter 3, the section on progress conditions (wait-free, bounded wait-free and population-oblivious)
  - paper: doi:10.1145/2145816.2145835
    title: Alex Kogan and Erez Petrank, A methodology for creating fast wait-free data structures, PPoPP 2012
    locator: the fast-path-slow-path method
  - paper: doi:10.1007/978-3-642-25873-2_22
    title: Maurice Herlihy and Nir Shavit, On the nature of progress, OPODIS 2011, LNCS 7109
    locator: pages 313 to 328 (wait-freedom as the independent condition with maximal progress)
---

Wait-freedom is the strongest common progress condition for a concurrent object: every operation of a process that does not crash completes in a finite number of that process's own steps, whatever the other processes do. Other processes can be fast, slow, stopped or crashed; none of this can stop the operation. [Lock-freedom](/lock-freedom/) promises only that some operation completes; wait-freedom promises it for each operation. The price is usually [helping](/helping/), and that costs time and space.

## Definition

**Notation and model.** $n$ is the number of processes, $p$ and $q$ are processes, $i$ and $j$ are indices, and $k$ is the contention. Processes are asynchronous and can crash between steps. Memory is sequentially consistent. A *run* is a sequence of steps, where each process calls operations of the object one after the other.

**Definition (wait-free).** An implementation is **wait-free** if, in every run, every operation invoked by a process $p$ that takes infinitely many steps completes. Equivalently: if $p$ keeps taking steps, then each operation of $p$ completes after a finite number of steps of $p$.

The count is of the steps of $p$ only. The steps of other processes do not count, and there can be any number of them between two steps of $p$.

**Definition (bounded wait-free).** An implementation is **bounded wait-free** if there is a number $B$, which can depend on $n$, such that every operation completes within $B$ of its own steps in every run. It is **population-oblivious** if $B$ does not depend on $n$.

The two definitions are not the same, and papers do not always use the same names. Herlihy (1991) writes "a finite number of steps"; The Art of Multiprocessor Programming calls the condition with a fixed bound "bounded wait-free". Some papers use "wait-free" for the bounded form. The difference is real:

- **Finite but not bounded.** Take an append-only log where each operation adds a record and then reads all records added before it. Each operation finishes, because only finitely many records exist when it starts, but the number of steps grows with the length of the run. No single $B$ works for all runs. The implementation is wait-free but not bounded wait-free.
- **Bounded.** The [Afek et al. snapshot](/afek-atomic-snapshot/) takes $O(n^2)$ steps per operation, so it is bounded but not population-oblivious. The wait-free [universal construction](/universal-construction/) takes $O(n)$ consensus steps per operation; in the textbook form, which rebuilds the state by replaying the log, the replay grows with the run, so it is a case of the "finite but not bounded" kind unless the state is saved in the cells.
- **Population-oblivious.** A [fetch-and-add](/fetch-and-add/) counter takes one step per operation, for any $n$.

Bounded wait-freedom is a statement about steps, not about the size of memory. A *bounded space* implementation uses a fixed number of registers of bounded size. The two are independent. Herlihy's universal construction, for example, uses unbounded sequence numbers and a list of cells that grows without bound, and some algorithms need extra work to make the space bounded.

**Wait-freedom is per operation.** Lock-freedom is a property of the object as a whole; wait-freedom is a property of each operation. A wait-free implementation is lock-free: in an infinite run some process takes infinitely many steps, and each of its operations completes, so infinitely many operations complete. The other way fails, as the CAS retry loop shows below.

**The cost.** Wait-freedom usually costs more than lock-freedom:

- **Helping.** If $p$ is slow, $q$ must not wait for $p$, but $q$ also must not undo $p$'s work for ever. So $q$ finishes $p$'s operation for it. That needs an announce array, a scan of $n$ entries, and a check on every step, as in the [universal construction](/universal-construction/). Censor-Hillel, Petrank and Timnat (2015) proved that, for queues, stacks and snapshots built from reads, writes and CAS, wait-freedom needs some form of help; see [helping](/helping/).
- **Time.** The universal construction is $O(n)$ per operation, and the Afek snapshot is $O(n^2)$; the lock-free double collect is cheaper when there is no contention.
- **Power.** Wait-freedom is the condition under which Herlihy's [consensus numbers](/consensus-number/) are defined. Registers alone cannot give wait-free consensus for 2 processes, and so cannot give wait-free queues, stacks or test-and-set. With CAS, every object has a wait-free implementation.

**The fast path and the slow path.** Kogan and Petrank (2012) gave a method to reduce the cost. An operation first runs a lock-free fast path, the plain CAS loop. If it fails a fixed number of times, it moves to a wait-free slow path: it announces itself in a shared array, and the other processes help it before they start their own operations. Under low contention the cost is close to the lock-free version; under an adversarial schedule each operation still has a bounded number of steps. They applied it to the [Kogan and Petrank queue](/kogan-petrank-queue/), which they had published in 2011 as a wait-free queue. Later work by Timnat and Petrank (2014) made the method automatic for a class of lock-free data structures.

## Examples and non-examples

**Wait-free: a counter from single-writer registers.** Process $i$ owns register $c_i$. To increment, $p_i$ reads $c_i$ and writes $c_i + 1$ (2 steps). To read, a process reads $c_0, \dots, c_{n-1}$ once and returns the sum ($n$ steps). Each operation has a fixed number of steps, so the counter is bounded wait-free.

It is also linearizable. Let $C(t)$ be the true count at time $t$, the sum of all registers. A read sees each $c_i$ at some time inside its interval; each $c_i$ only grows, so the sum it returns is at least $C$ at the start and at most $C$ at the end. $C$ grows by 1 at each increment, so it takes every value between the two, and the read can be linearized at a time where $C$ equals the returned sum. An increment is linearized at its write. An exhaustive check with the interleaving explorer and the linearizability checker from [linearizability](/linearizability/) agrees: all 70 histories of 2 increments and 2 reads, all 120 histories of 2 increments and 1 read in 3 processes, and all 5190 histories of 3 processes running (increment, read), (increment, read) and (read) are linearizable.

**Lock-free, not wait-free: the CAS retry loop.** An increment that reads $x$ and tries CAS($x$, $v$, $v + 1$) can fail each time another process succeeds first. The [lock-freedom](/lock-freedom/) page gives a fair schedule of 1000 rounds in which one process takes 2000 steps and completes nothing. The loop is lock-free and not wait-free.

**Wait-free: a single fetch-and-add.** On hardware with an atomic add, the counter is one [fetch-and-add](/fetch-and-add/) per increment. The step count is 1 for every $n$, so it is population-oblivious. On hardware where the add is built from an LL/SC loop, the instruction itself is only lock-free at the level of the hardware; the guarantee then rests on the forward progress rules of the processor.

**Wait-free with helping.** The [Afek et al. snapshot](/afek-atomic-snapshot/), the wait-free [universal construction](/universal-construction/) and the [Kogan and Petrank queue](/kogan-petrank-queue/).

**Not wait-free: any lock.** A process that waits for a lock waits for the holder; if the holder crashes, the process waits for ever. A [starvation-free](/starvation-freedom/) lock promises progress for each process, but only in runs where no process stops inside the critical section.

**One-shot objects.** If each process calls only one operation, a lock-free implementation is wait-free: a run can be infinite only if some process takes infinitely many steps, and then infinitely many operations would have to complete, which is impossible with finitely many operations. So the bounds on consensus hold for lock-free consensus too.

## Related definitions

- [Lock-freedom](/lock-freedom/): some operation completes in every infinite run. Weaker; implied by wait-freedom.
- [Obstruction-freedom](/obstruction-freedom/): an operation completes if it runs alone long enough. Weaker still.
- [Starvation-freedom](/starvation-freedom/): the blocking condition with maximal progress. Each operation completes, but only in runs where no process stops in the middle.
- [Helping](/helping/): the usual technique to turn a lock-free design into a wait-free one.
- [Consensus number](/consensus-number/): the measure of a primitive's power, defined by wait-free implementations.
- *Wait-free for some operations*: some designs make only some operations wait-free, for example wait-free reads and lock-free writes. Such an object is wait-free only for those operations, and the page or paper must say which.

## References
