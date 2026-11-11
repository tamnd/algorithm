---
tag: RHBQNE
kind: algorithm
slug: clh-lock
name: CLH lock
aliases: [Craig-Landin-Hagersten lock]
area: concurrency/mutual-exclusion
level: advanced
summary: A FIFO queue lock with an implicit list. A process swaps its node into the tail and spins on its predecessor's node; on release it clears its own node and takes the predecessor's.
solves: [mutual-exclusion-problem]
complexity:
  vars: {n: the number of processes}
  space: {shared: Θ(n)}
  steps: {solo: Θ(1)}
  rmr: {cc: O(1), dsm: ∞}
properties: {deterministic: true, deadlock_free: true, starvation_free: true, fcfs: true, local_spinning: true}
history:
  year: 1993
  people: [Travis S. Craig, Peter S. Magnusson, Anders Landin, Erik Hagersten]
  note: Craig described the lock in a 1993 technical report of the University of Washington. Magnusson, Landin and Hagersten found it independently and published it at IPPS in 1994.
prereqs: [mcs-lock]
see_also: [mcs-lock, anderson-lock, ticket-lock, spin-lock, cohort-lock, rmr-complexity, read-modify-write]
sources:
  - paper: "Travis S. Craig, Building FIFO and priority-queuing spin locks from atomic swap, Technical Report TR 93-02-02, Department of Computer Science and Engineering, University of Washington, February 1993"
    locator: the FIFO queue lock built from swap, in which each process spins on the element of its predecessor and inherits it on release
  - paper: "Peter S. Magnusson, Anders Landin and Erik Hagersten, Queue locks on cache coherent multiprocessors, Proceedings of the 8th International Parallel Processing Symposium (IPPS), 1994, pages 165-171"
    locator: the LH lock and the M lock, with the cache coherent analysis
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 7, Spin Locks and Contention, Section 7.5.2, the CLH queue lock (recycling of the predecessor's node)
  - paper: doi:10.1145/103727.103729
    title: John M. Mellor-Crummey and Michael L. Scott, Algorithms for scalable synchronization on shared-memory multiprocessors, ACM Transactions on Computer Systems 9(1), 1991, pages 21-65
    locator: Section 2.4, the MCS lock, for the comparison of the two list-based locks
---

The CLH lock is a queue lock in which each waiting process spins on the node of the process ahead of it. A shared pointer $tail$ points to the node of the last process. A process sets the flag $locked$ in its own node to true, swaps its node into $tail$, and spins until the flag of the node it got back is false. To release, it writes false to its own node, which is what its successor watches. It then takes the predecessor's node as its own for the next passage. The queue is implicit: no node points to the next one. In the cache coherent (CC) model a passage makes $O(1)$ remote memory references, but in the distributed shared memory (DSM) model it does not, because a process spins on a node that another process brought.

## In plain words

Each person carries a lamp. When you arrive you switch your lamp on, put it on the counter, and take the lamp that the last person left there. That lamp belongs to the person just ahead of you. You watch it. When that person is done, they switch their lamp off, and you go in.

When you are done, you switch your own lamp off, so the person behind you can go. You keep the lamp you were watching and use it next time.

Nobody needs to know who is behind them, and leaving takes one move. But the lamp you watch was carried in by someone else, so on a machine where each lamp sits in one fixed place, it may sit far away from you.

## The problem

The [mutual exclusion problem](/mutual-exclusion-problem/) for $n$ processes with first come, first served order and local spinning. The model is $n$ asynchronous processes on a sequentially consistent shared memory, with atomic registers (consensus number 1) and one swap object, fetch-and-store (consensus number 2). No compare-and-swap is needed. The costs are counted in the CC and DSM models of [RMR complexity](/rmr-complexity/).

## The algorithm

There are $n + 1$ nodes with one flag $locked$ each. At the start process $p$ owns node $p$ as $my$, and $tail$ points to an extra node whose flag is false.

```pseudo id=main
LOCK()                                   ▷ my is the node that the caller owns now
L1  my.locked ← true
L2  pred ← FETCH-AND-STORE(tail, my)      ▷ the doorway
L3  while pred.locked do nothing          ▷ spin on the predecessor's node
UNLOCK()
L4  my.locked ← false                     ▷ the successor watches this flag
L5  my ← pred                             ▷ recycle: the predecessor's node is now ours
```

L1 must come before L2: once the node is in $tail$, a successor may read it. L3 reads the predecessor's node; in the CC model it stays in the cache until the predecessor writes L4. L5 is local. After L4 the old node of the caller belongs to the successor, who still reads it, so the caller may not use it again. The node of the predecessor, on the other hand, is no longer read by anyone, because the predecessor has left and the caller has stopped spinning.

**How it differs from the MCS lock.**

| | [MCS lock](/mcs-lock/) | CLH lock |
|---|---|---|
| the list | explicit: $pred.next \leftarrow I$ | implicit: only the swap links the nodes |
| a waiter spins on | its own node | the predecessor's node |
| release | read $next$, maybe CAS, maybe wait for the link, write | one write |
| primitives | swap and compare-and-swap | swap only |
| node after release | the caller keeps its own node | the caller takes the predecessor's node |
| local spinning | CC and DSM | CC only |
| RMRs per passage | at most 8 in CC, at most 4 in DSM | at most 5 in CC, unbounded in DSM |
| space for $n$ processes and one lock | $n$ nodes | $n + 1$ nodes |

## Example

Three processes with nodes 0, 1 and 2, and the extra node 3, which holds false.

| step | process | line | action | $tail$ | flags of nodes 0 1 2 3 |
|---|---|---|---|---|---|
| start | | | | 3 | F F F F |
| 1 | 0 | L1, L2 | sets node 0, swap returns 3 | 0 | T F F F |
| 2 | 0 | L3 | node 3 is false, enters | 0 | T F F F |
| 3 | 1 | L1, L2 | sets node 1, swap returns 0 | 1 | T T F F |
| 4 | 1 | L3 | node 0 is true, spins | 1 | T T F F |
| 5 | 2 | L1, L2 | sets node 2, swap returns 1 | 2 | T T T F |
| 6 | 2 | L3 | node 1 is true, spins | 2 | T T T F |
| 7 | 0 | L4, L5 | clears node 0, takes node 3 | 2 | F T T F |
| 8 | 1 | L3 | node 0 is false, enters | 2 | F T T F |
| 9 | 1 | L4, L5 | clears node 1, takes node 0 | 2 | F F T F |
| 10 | 2 | L3 | node 1 is false, enters | 2 | F F T F |
| 11 | 2 | L4, L5 | clears node 2, takes node 1 | 2 | F F F F |

At the end process 0 owns node 3, process 1 owns node 0 and process 2 owns node 1, and $tail$ points to node 2, which is the free node now. The test file runs this schedule and checks that $tail$ ends at node 2.

## Correctness

The full proof is in proofs/correctness.md. It uses the queue $Q$ of processes from their L2 step to their L4 step, in the order of their L2 steps.

- **Nodes.** The $n$ nodes owned as $my$ are distinct, and the one other node is the *gate*. If $Q$ is empty, $tail$ points to the gate. Otherwise the first process of $Q$ (the head) has the gate as $pred$, and each other process has the node of the process before it.
- **Flags.** The gate holds false. The node of a process in $Q$ holds true until its L4.
- **Mutual exclusion and FIFO.** Only the head can read false at L3, so the processes enter one at a time in the order of $Q$.
- **Starvation freedom.** The head leaves after a finite critical section, and its L4 makes the next process the head.
- **Remote references.** At most 5 per passage in the CC model.

The test file checks mutual exclusion and FIFO order over all interleavings for two processes with two passages each and for three processes, checks starvation freedom for two processes that run forever, measures the maximum CC cost of a passage (5), and finds that the DSM cost of a passage is unbounded.

## Complexity

| measure | value |
|---|---|
| shared space | $n + 1$ nodes of one flag for $n$ processes, plus the pointer $tail$ |
| steps without contention | 4: L1, L2, one read at L3, L4 |
| RMRs per passage, CC model | at most 5 |
| RMRs per passage, DSM model | unbounded |
| bypass after the doorway | 0 |

**CC count.** L1, L2 and L4 are one RMR each. While a process waits, the predecessor's node is written only once, by the predecessor's L4: its L1 came before its L2, which came before the L2 of the waiter. So the reads of L3 miss at most twice, at the first read and after that write. The total is at most 5.

**Why not DSM.** In the DSM model each node lives in one memory module. Nodes move between processes at L5, so the predecessor's node is in general in another module, and every read of L3 is remote. Magnusson, Landin and Hagersten's M lock and other variants reduce this, but the basic lock has no bound in DSM.

**Space.** For $L$ locks and $n$ processes, the lock needs $L + n$ nodes in all if each process keeps one spare node, while the MCS lock needs one node per process for each lock it holds or waits for.

## Properties

- Uses one swap per passage, plus reads and writes. No compare-and-swap.
- Deadlock free, starvation free and FCFS, with bypass 0 after a doorway of one swap.
- The exit section is one write: it is wait free.
- Local spinning in the CC model, not in the DSM model.
- Each process must keep $pred$ from L2 to L5, and the node it owns changes with each passage.

## Variants and improvements

- **MCS lock.** Spins on the caller's own node, which gives local spinning in DSM too, at the cost of a release that may need CAS and a wait. See [MCS lock](/mcs-lock/).
- **Craig's priority queue lock.** Craig's report also builds a lock that serves waiters by priority on top of the same queue.
- **Timeout.** Scott and Scherer (2001) gave a CLH-try lock in which a waiter marks its node as abandoned, and its successor skips it.
- **Hierarchical CLH.** Luchangco, Nussbaum and Shavit (2006) gave the HCLH lock, which splices local queues of one NUMA node into a global queue. See also the [cohort lock](/cohort-lock/).
- **Java.** The wait queue of `AbstractQueuedSynchronizer` in `java.util.concurrent`, which is under `ReentrantLock` and others, is a variant of the CLH queue with explicit links added for blocking.

## When to use it

Use the CLH lock on a cache coherent machine when you want a FIFO lock with local spinning and the simplest possible release, or when only swap is available. It is a good default queue lock for one socket. On machines without coherent caches, or when spinning must be on local memory across NUMA nodes, use the [MCS lock](/mcs-lock/) or a [cohort lock](/cohort-lock/).

## Pitfalls

**Reusing the own node.** The wrong code keeps $my$ after UNLOCK and does `my.locked ← true` in the next LOCK. The successor may still be spinning on that node; it then sees true again and may wait forever, or the queue gets a cycle. The right line is L5: `my ← pred`.

**Swapping before setting the flag.** The wrong order is L2 and then `my.locked ← true`. A successor that swaps in between reads the old value of the node, which may be false, and enters while the caller is inside. The right order is L1 then L2.

**Losing pred.** The value of $pred$ must survive from L2 to L5, for example in a per-thread variable. A lock that frees the predecessor's node at once breaks the next passage.

**DSM machines.** Spinning on a node in another module is as bad as spinning on a shared word. Do not use plain CLH where the cost of a remote read does not go away with caching.

## Implementations

## History

Craig (1993) built FIFO and priority queue spin locks from atomic swap in a technical report at the University of Washington. Magnusson, Landin and Hagersten (1994), at the Swedish Institute of Computer Science, found the same queue lock independently and published it at IPPS, with variants for cache coherent multiprocessors. The name CLH comes from the initials of Craig, Landin and Hagersten. Doug Lea's `AbstractQueuedSynchronizer` in Java 5 (2004) built the blocking locks of Java on a variant of the CLH queue.

## References
