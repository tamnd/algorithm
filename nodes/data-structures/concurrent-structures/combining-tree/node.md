---
tag: 9G1178
kind: data-structure
slug: combining-tree
name: Combining tree
aliases:
- software combining tree
area: data-structures/concurrent-structures
level: advanced
summary: Tree of nodes where pairs of threads combine their increments before ascending, spreading contention.
prereqs: [complete-binary-tree, monitor, linearizability]
see_also: [combining-funnel, counting-network, diffracting-tree, sloppy-counter, fetch-and-add, flat-combining, linearization-point, quiescent-consistency]
sources:
  - book: isbn:9780123973375
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, revised reprint
    locator: Chapter 12, Section 12.3 (Software Combining), pages 281 onward, with the Node class and the four phases precombining, combining, operation and distribution
  - paper: doi:10.1109/TC.1987.1676921
    title: Pen-Chung Yew, Nian-Feng Tzeng and Duncan H. Lawrie, Distributing hot-spot addressing in large-scale multiprocessors, IEEE Transactions on Computers C-36(4), 1987
    locator: pages 388 to 395, the software combining tree for a hot spot
  - paper: doi:10.1145/70082.68188
    title: James R. Goodman, Mary K. Vernon and Philip J. Woest, Efficient synchronization primitives for large-scale cache-coherent multiprocessors, ASPLOS 1989
    locator: pages 64 to 75, combining of fetch-and-op requests in a tree
  - paper: doi:10.1109/TC.1983.1676201
    title: Allan Gottlieb, Ralph Grishman, Clyde P. Kruskal, Kevin P. McAuliffe, Larry Rudolph and Marc Snir, The NYU Ultracomputer, designing an MIMD shared memory parallel computer, IEEE Transactions on Computers C-32(2), 1983
    locator: pages 175 to 189, hardware combining of fetch-and-add in the network
---

A combining tree is a shared counter built as a complete binary tree with one leaf for each pair of threads. A thread that calls getAndIncrement() climbs from its leaf toward the root. When two threads meet at a node, one of them waits there, and the other takes the increments of both on up, so that one step at the root can add a whole batch of increments. On the way down, the climber hands each waiting thread its share of the range of values. With $p$ threads a call takes $O(\log p)$ steps, but no more than two threads ever contend for one node. The counter is [linearizable](/linearizability/) and blocking. The idea comes from the hardware combining of the NYU Ultracomputer; Yew, Tzeng and Lawrie, and Goodman, Vernon and Woest made it a software structure, and this page follows the version of Herlihy and Shavit.

## In plain words

Think of a large office where each person must get a ticket number from one machine in the lobby. If everyone walks to the lobby, there is a long line. Instead, people pair up on each floor. One of each pair waits, and the other goes down with a note that says "two tickets". On the next floor down, two such people meet, one waits, and the other goes on with "four tickets". At the lobby, one person takes a whole block of numbers at once. Then each person walks back up and hands the waiting partner the second half of the block.

A combining tree does this for a counter. Only two threads ever meet at one place, so no place gets crowded. The cost is that each call walks up and down the tree, and some threads must wait for a partner.

## The abstract type

The tree implements a shared counter with one operation, getAndIncrement(), which returns the current value $v$ and changes it to $v + 1$. Equivalently it is [fetch-and-add](/fetch-and-add/) with argument 1; the tree works for any associative operation in the same way. The concurrent object is linearizable with respect to the sequential counter: if a call returns before another starts, it gets the smaller value. This is stronger than the [quiescent consistency](/quiescent-consistency/) of a [counting network](/counting-network/).

## Representation

For $w$ threads, $w$ a power of 2, the tree has $w - 1$ nodes in a [complete binary tree](/complete-binary-tree/): the root, internal nodes, and $w/2$ leaves. Threads $2i$ and $2i + 1$ start at leaf $i$. Each node $n$ has:

- $n.status$: one of IDLE, FIRST, SECOND, RESULT, and ROOT for the root.
- $n.locked$: a flag that keeps a third thread out while two threads work at the node.
- $n.first$, $n.second$: the batch sizes that the two threads bring.
- $n.result$: the counter value, at the root; elsewhere, the first value of the passive thread's share.
- A [monitor](/monitor/): each node procedure below runs with the node's lock held, and "wait until" releases the lock while it waits.

At a node, the first thread to arrive is the *active* thread, which goes on up. The second is the *passive* thread, which stops at the node and waits for its result.

## Operations

```pseudo id=main
GET-AND-INCREMENT(T, id)
L1  leaf ← T.leaf[⌊id/2⌋]; node ← leaf
L2  while PRECOMBINE(node) do node ← node.parent     ▷ phase 1: find the stop node
L3  stop ← node; node ← leaf; combined ← 1; S ← empty stack
L4  while node ≠ stop do                              ▷ phase 2: collect increments
L5      combined ← COMBINE(node, combined); push node on S; node ← node.parent
L6  prior ← OP(stop, combined)                        ▷ phase 3
L7  while S is not empty do DISTRIBUTE(pop S, prior)  ▷ phase 4: hand out values
L8  return prior

PRECOMBINE(n)
L9  wait until not n.locked
L10 if n.status = IDLE then n.status ← FIRST; return true      ▷ active: go on up
L11 if n.status = FIRST then n.locked ← true; n.status ← SECOND; return false   ▷ passive
L12 return false                                                ▷ the root

COMBINE(n, c)
L13 wait until not n.locked                ▷ wait for the passive thread to deposit
L14 n.locked ← true; n.first ← c
L15 if n.status = FIRST then return c else return c + n.second

OP(n, c)
L16 if n.status = ROOT then prior ← n.result; n.result ← prior + c; return prior
L17 n.second ← c; n.locked ← false         ▷ passive: deposit and let the active thread combine
L18 wait until n.status = RESULT
L19 n.locked ← false; n.status ← IDLE; return n.result

DISTRIBUTE(n, prior)
L20 if n.status = FIRST then n.status ← IDLE; n.locked ← false    ▷ nobody joined
L21 else n.result ← prior + n.first; n.status ← RESULT            ▷ the passive share
```

**Precombining.** A thread climbs while it is the first to mark the nodes on its path (line L10). It stops at the first node where another thread was first (line L11), or at the root. At that node it becomes passive and locks the node, so that the active thread there waits for its increments.

**Combining.** The thread climbs again from its leaf to its stop node, and at each node adds the batch that the passive thread there deposited (line L15). Line L14 locks the node, so no new thread can start at it until this round is over.

**Operation.** At the root, the thread adds its whole batch in one step and gets the old value (line L16). At another stop node, it deposits its batch for the active thread (line L17) and waits for its value (line L18).

**Distribution.** On the way down, at each node where a passive thread waits, the thread gives it the start of its share: the active thread's own subtree takes the first $n.first$ values from prior, so the passive share starts at $prior + n.first$ (line L21).

## Example

Width 4: a root and two leaves. Threads $A$ (id 0) and $B$ (id 1) share leaf 0; thread $C$ (id 2) uses leaf 1. The counter is 0.

| step | thread | what it does | leaf 0 | leaf 1 | root result |
|---|---|---|---|---|---|
| 1 | $A$ | L10 at leaf 0: FIRST; L12 at the root: stop | FIRST | IDLE | 0 |
| 2 | $B$ | L11 at leaf 0: SECOND, locked; stop is leaf 0 | SECOND, locked | IDLE | 0 |
| 3 | $C$ | L10 at leaf 1, L12 at the root: stop | SECOND, locked | FIRST | 0 |
| 4 | $B$ | L17: second = 1, unlocks; then waits at L18 | SECOND | FIRST | 0 |
| 5 | $A$ | L13 to L15 at leaf 0: first = 1, carries 2 | SECOND, locked | FIRST | 0 |
| 6 | $C$ | L13 to L15 at leaf 1: carries 1 | SECOND, locked | FIRST, locked | 0 |
| 7 | $C$ | L16 at the root: prior = 0 | SECOND, locked | FIRST, locked | 1 |
| 8 | $C$ | L20 at leaf 1; returns 0 | SECOND, locked | IDLE | 1 |
| 9 | $A$ | L16 at the root: prior = 1 | SECOND, locked | IDLE | 3 |
| 10 | $A$ | L21 at leaf 0: result = 1 + 1 = 2; returns 1 | RESULT, locked | IDLE | 3 |
| 11 | $B$ | L18, L19: returns 2 | IDLE | IDLE | 3 |

The root was touched only twice for three increments. The linearization puts $C \to 0$ at step 7, then $A \to 1$ and $B \to 2$ at step 9, in the order of their values. Both $A$ and $B$ were pending at step 9, so this order respects real time.

## Correctness

Every call that does its own step at the root (line L16) carries a *batch*: itself and, recursively, the batches of the passive threads at the nodes where it combined. A batch of size $c$ gets the $c$ consecutive values from prior. Linearize all calls of a batch at the root step of that batch, in the order of their values. The proof shows three facts. First, the values of a batch are distributed without overlap, because at each node the active subtree gets the first $n.first$ values and the passive one the next $n.second$, and $n.first + n.second$ is exactly what was carried up. Second, each call of a batch is pending at its root step: it has deposited its increment before, and it gets its value only after. Third, the lock flags give each node to at most one pair of threads per round. From these, each history is linearizable. The waits only ever point down the tree, for a deposit, or up the tree, for a result, so they cannot form a cycle, and the tree is [deadlock-free](/deadlock-freedom/). It is not lock-free: a passive thread waits for its partner. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| quantity | value |
|---|---|
| steps of one call | $O(\log w)$ node procedures, plus waits |
| threads that contend for one node | at most 2 in a round, plus late arrivals that wait at line L9 |
| root steps for $m$ concurrent calls | as few as 1 for a full batch of $w$, at worst $m$ |
| space | $w - 1$ nodes |

Without concurrency, each call pays $2 \log_2 w$ node visits where a plain [fetch-and-add](/fetch-and-add/) pays one, so the tree is slower at low load. Under heavy load, all $w$ threads can be served by one root step, and the throughput grows with $w$ while the latency is $O(\log w)$. Herlihy and Shavit note that the gain depends on threads arriving together; a thread that arrives a moment late at a node finds its partner gone and climbs alone. Real implementations make a thread wait a short time at a node to give a partner the chance to come.

## Variants

- **[Combining funnels](/combining-funnel/).** Shavit and Zemach replace the fixed tree by layers of random collision arrays, so threads combine with whoever comes, and the depth adapts to the load.
- **[Diffracting trees](/diffracting-tree/) and [counting networks](/counting-network/).** Spread the calls over many counters instead of combining them, with no waiting for a partner; the price is that the counter is only quiescently consistent.
- **[Flat combining](/flat-combining/).** One thread at a time takes a lock and applies the requests that the other threads have posted in a list, a combining tree of height 1.
- **Hardware combining.** The NYU Ultracomputer combined fetch-and-add requests inside the switches of its network, which is the origin of the software version.
- **Other operations.** Any associative operation with an identity combines in the same way: fetch-and-add of any amount, fetch-and-max, and the arrival count of a tree barrier.

## When to use it

Use a combining tree when many threads update one counter or one accumulator at the same moments, the hardware has no fast [fetch-and-add](/fetch-and-add/), and the threads can wait a little for a partner: barriers, global sums in a parallel loop, ticket counters on large machines. Use a plain atomic counter when contention is low, a [sloppy counter](/sloppy-counter/) when reads can be approximate, and a lock-free design when threads can be delayed for a long time, since a delayed active thread delays all threads that wait for it.

## Pitfalls

- **Testing the status without the lock.** The procedures must run under the node monitor. A status change and the test of the flag of line L9 must be one atomic block, or two threads both become active at a node.
- **Dropping the lock flag.** Without line L14, a third thread could start a new round at a node while the old round is still being distributed, and overwrite $n.first$.
- **Swapping the shares.** The active thread's own subtree takes the first values, so the passive share starts at $prior + n.first$, not at $prior + n.second$.
- **More than two threads per leaf.** The protocol assumes that at most two threads start at a leaf. Thread ids must be distinct among concurrent callers.
- **Expecting progress from every thread.** A passive thread cannot finish until its active partner has been to the root and back. A preempted active thread blocks a whole subtree.

## Implementations

The Python class follows the pseudocode. Each node has a lock that serves as its monitor, and each node procedure is a generator step that holds the lock; a wait releases the lock and yields. The tests replay the example step by step, show that a late thread waits at a locked node, check sequential use against an ordinary counter, and check random interleavings of three threads with a linearizability search. The plain method also runs under real threads.

## History

Gottlieb and others built hardware combining of fetch-and-add into the network of the NYU Ultracomputer in 1983. Yew, Tzeng and Lawrie proposed software combining trees in 1987 to spread a hot spot over many memory modules, and Goodman, Vernon and Woest studied combining for cache-coherent machines in 1989. Herlihy and Shavit give the protocol with four phases in their textbook, and Shavit and Zemach generalized it into combining funnels.

## References
