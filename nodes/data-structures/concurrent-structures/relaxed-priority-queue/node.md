---
tag: V0W0KM
kind: concept
slug: relaxed-priority-queue
name: Relaxed priority queue
aliases:
- relaxed concurrent priority queue
area: data-structures/concurrent-structures
level: advanced
summary: Priority queue whose delete-min may return an element close to the minimum, trading order for scalability.
prereqs: [priority-queue, linearizability]
see_also: [multiqueue, spraylist, fine-grained-concurrent-heap, lock-free-skip-list, power-of-two-choices, delta-stepping, quiescent-consistency]
sources:
  - paper: doi:10.1145/2429069.2429109
    title: Thomas A. Henzinger, Christoph M. Kirsch, Hannes Payer, Ali Sezgin and Ana Sokolova, Quantitative relaxation of concurrent data structures, POPL 2013
    locator: the framework of relaxed sequential specifications with a cost function, and the k-out-of-order relaxations
  - paper: doi:10.1145/2755573.2755616
    title: Hamza Rihani, Peter Sanders and Roman Dementiev, MultiQueues, simple relaxed concurrent priority queues, SPAA 2015
    locator: pages 80 to 82, the MultiQueue and its measured rank error
  - paper: doi:10.1145/2688500.2688523
    title: Dan Alistarh, Justin Kopinsky, Jerry Li and Nir Shavit, The SprayList, a scalable relaxed priority queue, PPoPP 2015
    locator: pages 11 to 20, the spray operation and its rank bound
  - paper: doi:10.1145/3087801.3087810
    title: Dan Alistarh, Justin Kopinsky, Jerry Li and Giorgi Nadiradze, The power of choice in priority scheduling, PODC 2017
    locator: pages 283 to 292, the rank bounds of the two-choice process
  - paper: doi:10.1145/2688500.2688547
    title: Martin Wimmer, Jakob Gruber, Jesper Larsson Träff and Philippas Tsigas, The lock-free k-LSM relaxed priority queue, PPoPP 2015
    locator: pages 277 to 278, the k-LSM with its bound of k on the rank error
---

A relaxed priority queue is a concurrent [priority queue](/priority-queue/) whose delete-min may return an item that is close to the minimum instead of the minimum itself. An exact concurrent priority queue is a bottleneck by its specification: each delete-min must take the one smallest item, so all threads compete for the same place in the structure. If delete-min may return any of the $k$ smallest items, or an item of small expected rank, the threads can work on different parts of the structure. The [MultiQueue](/multiqueue/), the [SprayList](/spraylist/) and the k-LSM are the main designs. They are used where an approximate order is enough, such as parallel shortest paths and schedulers.

## In plain words

In a hospital the most urgent patient should be treated first. If there is only one list of patients and many doctors, every doctor goes to the top of the same list at the same time, and they get in each other's way.

Now give up a little order. Split the patients over several lists. A free doctor looks at the top of two lists chosen at random, and takes the more urgent of the two. The patient taken is not always the most urgent of all, but almost always one of the most urgent few. The doctors now rarely wait for each other.

A relaxed priority queue makes this trade. It promises an item near the front, not the front, and in return many threads can remove items at the same time.

## The idea

**Why an exact queue does not scale.** In any [linearizable](/linearizability/) priority queue, two delete-min calls in sequence must return the smallest and then the second smallest item. Whatever the data structure, they touch the same few items, and so the same few cache lines. In a heap the root is the hot spot, in a [lock-free skip list](/lock-free-skip-list/) the first nodes of the bottom list are. The throughput of delete-min is then bounded by the rate at which one cache line can move between cores, whatever the number of threads.

**Measures of relaxation.** Let delete-min return item $x$ while the queue holds the items $Q$.

- The *rank* of $x$ is $1 + |\{ y \in Q : y < x \}|$. An exact queue always returns rank 1, and the *rank error* is the rank minus 1.
- A queue is *$k$-relaxed* if each delete-min returns an item of rank at most $k$. The k-LSM gives this guarantee for every call, with $k$ a parameter.
- A probabilistic guarantee bounds the expected rank, or the rank with high probability. The MultiQueue and the SprayList give guarantees of this kind.
- The *delay* of an item is the number of delete-min calls that return a larger item while it is in the queue. A bound on the delay says that no item is skipped for ever.

Henzinger, Kirsch, Payer, Sezgin and Sokolova made this precise as a *quantitative relaxation*: the sequential specification is extended to all sequences of operations, each with a cost, and a relaxed object may produce sequences of cost at most $k$. The concurrent object then stays linearizable, but with respect to the relaxed sequential object. So a relaxed queue is not a weaker consistency condition, like [quiescent consistency](/quiescent-consistency/); it is a strong condition with a weaker specification.

**How designs get the relaxation.**

- *Many queues and random choice.* The [MultiQueue](/multiqueue/) keeps $c \cdot p$ sequential queues with a lock each, for $p$ threads. Insert puts the item in one random queue. Delete-min reads the minimum of two random queues and removes the smaller one. By the [power of two choices](/power-of-two-choices/), the queues stay balanced: for $n$ queues the expected rank is $O(n)$ and the largest rank over a long run is $O(n \log n)$, as Alistarh, Kopinsky, Li and Nadiradze proved.
- *Random walks over a skip list.* The [SprayList](/spraylist/) is a lock-free skip list in which delete-min does a short random walk from the head, the *spray*, and removes the node where the walk lands. The walk lands among the first $O(p \log^3 p)$ items with high probability, and the landing points of different threads rarely meet.
- *Local buffers.* The k-LSM keeps a small [log-structured](/log-structured-merge-tree/) part for each thread and a shared part, and a thread may take its local minimum if fewer than $k$ items could be smaller. This gives a deterministic bound of $k$.
- *Exact structures as a baseline.* A heap with fine-grained locks, like the [fine-grained concurrent heap](/fine-grained-concurrent-heap/), or a skip-list queue in the style of Lotan and Shavit, returns rank 1 but stays a bottleneck at the front.

**The price.** An algorithm that uses the queue must tolerate the rank error. A label-correcting shortest path algorithm, such as [Bellman-Ford](/bellman-ford/) or [delta-stepping](/delta-stepping/), stays correct when it takes vertices out of order, but may relax an edge more than once. So the relaxation trades contention for extra work, and the right amount of relaxation is the point where the saved waiting is larger than the wasted work.

## Examples

**A MultiQueue with four queues.** The queues hold these items, with the minimum first.

| queue | items |
|---|---|
| 0 | 1, 9, 12 |
| 1 | 4, 5 |
| 2 | 2, 11 |
| 3 | 7, 8, 10 |

The global order is 1, 2, 4, 5, 7, 8, 9, 10, 11, 12. A thread picks queues 1 and 3 at random. Their minima are 4 and 7, so it removes 4. The true minimum is 1, and 4 has rank 3: the rank error is 2. A second thread picks queues 0 and 2 at the same time, takes the lock of queue 0, and removes 1, with rank 1 among the items still there. The two threads never touched the same queue. An exact queue would have returned 1 and then 2, and both calls would have touched the same root.

**A bound that cannot be met cheaply.** A $k$-relaxed queue with $k = 1$ is an exact queue, so all of the cost of the exact case is back. For $k \ge p$ each of $p$ threads can be given its own item among the $k$ smallest, which is the reason that many designs choose the relaxation proportional to the number of threads.

**Not a relaxation.** A queue that returns an item of rank at most $k$ only in quiescent states, and any item otherwise, is not $k$-relaxed. A relaxation bounds every delete-min.

## Where it is used

- **Parallel shortest paths.** [Delta-stepping](/delta-stepping/) and label-correcting variants of [Dijkstra's algorithm](/dijkstra/) for [single-source shortest paths](/single-source-shortest-paths/) take vertices from a relaxed queue; the MultiQueue and the SprayList papers both measure this use.
- **Task schedulers with priorities.** Graph analytics systems schedule tasks by an approximate priority, and many-core runtimes use per-core queues with stealing, close to [work stealing](/work-stealing/) with priorities.
- **Discrete event simulation and branch and bound.** Events or subproblems may be handled slightly out of order if the algorithm can roll back or bound the waste.
- **Search with heuristics.** Parallel [A* search](/a-star-search/) may expand nodes in an approximate order and then needs more expansions to prove optimality.

## References
