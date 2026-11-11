---
tag: 39HPVB
kind: concept
slug: rmr-complexity
name: Remote memory references complexity
aliases: [RMR complexity, remote memory references]
area: concurrency/mutual-exclusion
level: research
summary: The cost of a lock as the number of remote memory references per passage, in the cache coherent (CC) or the distributed shared memory (DSM) model. Local spinning is free.
history:
  year: 1991
  people: [John M. Mellor-Crummey, Michael L. Scott, James H. Anderson, Jae-Heon Yang, Hagit Attiya, Danny Hendler, Philipp Woelfel]
  note: Mellor-Crummey and Scott (1991) made local spinning the design goal. Yang and Anderson (1995) gave O(log n) RMRs with reads and writes, and Attiya, Hendler and Woelfel (2008) proved it optimal.
prereqs: [mutual-exclusion-problem, spin-lock]
see_also: [mcs-lock, clh-lock, anderson-lock, ticket-lock, tournament-lock, mutual-exclusion-lower-bounds, peterson-algorithm, cohort-lock]
sources:
  - paper: doi:10.1007/BF01784242
    title: Jae-Heon Yang and James H. Anderson, A fast, scalable mutual exclusion algorithm, Distributed Computing 9(1), 1995, pages 51-60
    locator: the arbitration tree of two-process local-spin locks with O(log n) remote references per passage, using reads and writes only
  - paper: doi:10.1145/1374376.1374410
    title: Hagit Attiya, Danny Hendler and Philipp Woelfel, Tight RMR lower bounds for mutual exclusion and other problems, Proceedings of the 40th ACM Symposium on Theory of Computing (STOC), 2008, pages 217-226
    locator: the Omega(log n) lower bound for deadlock-free mutual exclusion with reads, writes and conditional primitives, in the CC and DSM models
  - paper: doi:10.1145/103727.103729
    title: John M. Mellor-Crummey and Michael L. Scott, Algorithms for scalable synchronization on shared-memory multiprocessors, ACM Transactions on Computer Systems 9(1), 1991, pages 21-65
    locator: local spinning as the goal, and the MCS lock with O(1) remote references
  - paper: doi:10.1007/s00446-003-0088-6
    title: James H. Anderson, Yong-Jik Kim and Ted Herman, Shared-memory mutual exclusion, major research trends since 1986, Distributed Computing 16(2-3), 2003, pages 75-110
    locator: the CC and DSM models, the definition of remote memory references, and the survey of local-spin, adaptive and lower bound results
  - paper: "Yong-Jik Kim and James H. Anderson, Adaptive mutual exclusion with local spinning, Distributed Computing 19(3), 2007"
    locator: an algorithm with reads and writes whose RMR cost is O(min(k, log n)) for point contention k
  - paper: "Prasad Jayanti, Adaptive and efficient abortable mutual exclusion, Proceedings of the 22nd ACM Symposium on Principles of Distributed Computing (PODC), 2003"
    locator: an abortable lock with O(min(k, log n)) remote references, using LL/SC
---

Remote memory references (RMR) complexity measures a lock by the number of *remote* memory accesses that a process makes in one passage: one trip through the entry section, the critical section and the exit section. An access is remote if it must cross the interconnect of the machine; an access that a process can serve from its own cache or its own memory module is local and costs nothing. Busy waiting on a local location is therefore free. Two models make "remote" precise: the cache coherent (CC) model and the distributed shared memory (DSM) model. Most modern results on [mutual exclusion](/mutual-exclusion-problem/) are stated in RMRs.

## In plain words

Imagine that every worker sits in an office, and the shared data sits in other offices down the hall. Looking at a paper on your own desk is free. Walking down the hall to look at a paper costs one trip.

A worker who waits for a lock may look at a paper a million times. If the paper is on the worker's desk, all that looking costs nothing. What matters is how many trips the worker must make. A good lock lets each waiter watch a paper on its own desk, and makes only a few trips for each entry.

There are two kinds of offices. In one kind, a worker may copy any paper to the desk and is told when the original changes. In the other kind, papers never move, so a waiter must watch a paper that lives in its own office.

## The idea

**Model.** There are $n$ asynchronous processes on a sequentially consistent shared memory. A process takes steps on shared objects: reads, writes and read-modify-write operations such as [test-and-set](/test-and-set/), swap, [fetch-and-add](/fetch-and-add/) and [compare-and-swap](/compare-and-swap/). A *passage* is the sequence of steps from the start of an entry section to the end of the next exit section. The RMR complexity of a lock is the largest number of remote steps in one passage, over all runs; it may be unbounded.

**The CC model.** Each process has a cache. A read is local if the location is in the cache of the reader and no other process has written it since the reader last accessed it; otherwise it is remote, and it brings a copy into the cache. A write or a read-modify-write step counts as remote; it removes the copies in the other caches. (Some papers count a write as local when the writer already holds the only copy; the bounds below do not depend on this choice up to a constant.) So a process that spins on a location that nobody writes makes one RMR, and then one more each time another process writes it.

**The DSM model.** There are no caches. Each location lives in the memory module of one process, chosen when the algorithm is written. An access to a location in the module of the caller is local, and every other access is remote. So a process can spin locally only on a location in its own module.

**Why RMRs.** Plain step counts do not work for locks. A waiting process takes steps until the holder leaves, and the holder may stay in its critical section for any number of steps, so every lock has unbounded step complexity. RMRs measure what actually limits performance: traffic on the bus or the network, which also slows the holder. Anderson (1990) and Mellor-Crummey and Scott (1991) found by measurement that locks whose waiters spin on locations that nobody else spins on scale, and locks whose waiters all spin on one word do not. A lock with a bounded RMR cost per passage is said to use *local spinning*. In the DSM model, local spinning requires each waiter to spin on a location in its own module, which is a stronger demand than in the CC model.

**Upper bounds.**

- With swap (fetch-and-store) and compare-and-swap, the [MCS lock](/mcs-lock/) makes $O(1)$ RMRs per passage in both models.
- With swap alone, the [CLH lock](/clh-lock/) makes $O(1)$ RMRs in the CC model. With fetch-and-add, [Anderson's lock](/anderson-lock/) makes $O(1)$ in the CC model if its array is padded. Neither spins locally in the DSM model.
- With reads and writes only, Yang and Anderson (1995) give a lock with $O(\log n)$ RMRs per passage in both models. It is an arbitration tree, like the [tournament lock](/tournament-lock/), in which each node is a two-process lock where each process spins only on a location in its own module, and a process announces its arrival to the other side in a variable that the other side then reads once.

**Lower bounds.**

- Attiya, Hendler and Woelfel (2008) proved that every deadlock-free mutual exclusion algorithm for $n$ processes that uses reads, writes and *conditional* primitives has a passage with $\Omega(\log n)$ RMRs, in both the CC and the DSM model. A conditional primitive changes the value of an object only if the value equals a given one; compare-and-swap and load-linked/store-conditional are of this kind. So the algorithm of Yang and Anderson is optimal, and compare-and-swap does not help on its own.
- Earlier, Anderson and Kim (2002) proved $\Omega(\log n / \log \log n)$ for reads and writes, and Fan and Lynch (2006) proved that $n$ processes that each enter once make $\Omega(n \log n)$ RMRs in all in the CC model.
- The bound does not hold for fetch-and-store or fetch-and-add, which are not conditional: the MCS, CLH and Anderson locks beat it. RMR complexity thus separates primitives in a way that [consensus numbers](/consensus-number/) do not: compare-and-swap has consensus number $\infty$, and swap and fetch-and-add have 2.

**Adaptive and abortable locks.** An *adaptive* lock has an RMR cost that depends on the contention $k$, not on $n$. Kim and Anderson (2007) give a lock with reads and writes and $O(\min(k, \log n))$ RMRs. An *abortable* lock lets a waiter give up; Jayanti (2003) gives one with $O(\min(k, \log n))$ RMRs from LL/SC, and Scott and Scherer (2001) gave queue locks with time-out.

## Examples

The costs of the locks of this area, per passage, with $n$ processes. "Unbounded" means that a waiter can make any number of RMRs while one other process stays in its critical section.

| lock | primitives | CC model | DSM model |
|---|---|---|---|
| [test-and-set](/test-and-set/) lock, [TTAS with backoff](/spin-lock/) | test-and-set | unbounded | unbounded |
| [ticket lock](/ticket-lock/) | fetch-and-add | $O(n)$; exactly $n + 2$ at worst | unbounded |
| [Anderson's lock](/anderson-lock/), padded | fetch-and-add | $O(1)$; at most 6 | unbounded |
| [Anderson's lock](/anderson-lock/), one cache line | fetch-and-add | $O(n)$ | unbounded |
| [MCS lock](/mcs-lock/) | swap, compare-and-swap | $O(1)$; at most 8 | $O(1)$; at most 4 |
| [CLH lock](/clh-lock/) | swap | $O(1)$; at most 5 | unbounded |
| [Peterson's algorithm](/peterson-algorithm/), two processes | reads and writes | $O(1)$ | unbounded |
| [tournament lock](/tournament-lock/) of Peterson locks | reads and writes | $O(\log n)$ | unbounded |
| Yang and Anderson (1995) | reads and writes | $O(\log n)$ | $O(\log n)$ |
| [cohort lock](/cohort-lock/) C-BO-MCS | test-and-set, swap, compare-and-swap | unbounded | unbounded |

The exact numbers are the maxima that the test files of the lock pages measure with an exhaustive explorer, or prove on those pages. For example, the ticket lock costs $n + 2$ for the last of $n$ processes in line: one fetch-and-add, one read miss for the first read and for each of the $n - 1$ handovers ahead, and one write.

**A concrete count.** In the CC model, a waiter of the test-and-set lock that applies test-and-set in a loop makes one RMR per attempt, because each test-and-set is a write. A waiter of the test-and-test-and-set lock reads the lock word from its cache, and misses only when the word changes. The test file of the [spin lock](/spin-lock/) page measures 199 RMRs against 1 over 200 steps of a waiter while the lock is held.

## Where it is used

- The design of scalable spin locks: queue locks, NUMA locks such as the [cohort lock](/cohort-lock/), and readers-writer locks with local spinning.
- Lower bounds for mutual exclusion and related problems, such as [mutual exclusion lower bounds](/mutual-exclusion-lower-bounds/), and for the implementation of objects such as counters and [compare-and-swap](/compare-and-swap/) from weaker primitives.
- Barriers and other blocking synchronization, where the same models give the cost of [barrier synchronization](/barrier-synchronization/).
- The comparison of primitives: some primitives allow $O(1)$ RMR locks and some do not, which is a different ranking from the consensus hierarchy.

## References
