---
tag: 3D757V
kind: data-structure
slug: combining-funnel
name: Combining funnel
aliases:
- combining funnels
area: data-structures/concurrent-structures
level: research
summary: Layered funnel that combines colliding operations before reaching a shared structure.
prereqs: [combining-tree, fetch-and-add, compare-and-swap]
see_also: [diffracting-tree, elimination-backoff-stack, flat-combining, counting-network, exponential-backoff, sloppy-counter, treiber-stack, linearizability]
sources:
  - paper: doi:10.1006/jpdc.2000.1621
    title: Nir Shavit and Asaph Zemach, Combining funnels, a dynamic approach to software combining, Journal of Parallel and Distributed Computing 60(11), 2000
    locator: pages 1355 to 1387, the layers and the collision protocol, the distribution of results, elimination for stacks, and the adaptive width of the layers
  - book: isbn:9780123973375
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, revised reprint
    locator: Chapter 12, Section 12.3 (Software Combining), the static combining tree that the funnel replaces; Chapter 11, the elimination array
---

A combining funnel puts a few layers of small arrays in front of a shared object, such as a [fetch-and-add](/fetch-and-add/) counter. A thread on its way to the object passes through the layers. On each layer it writes its id into a random cell and reads who was there before. If that thread is still on the same layer, the two *collide*: one captures the other, takes over its operation, and goes on alone with the sum of both. So operations combine in pairs, then in fours, and the object sees one combined operation instead of many. The results then flow back along the same captures. Shavit and Zemach introduced combining funnels in 1998 and published the journal version in 2000. Unlike a [combining tree](/combining-tree/), a funnel has no fixed pairing of threads, so a thread that comes alone passes quickly, and the layers can grow and shrink with the load.

## In plain words

Many people want to drop money into one box. Instead of queueing at the box, they first walk through a few rooms. In each room, a person writes their name on a random spot of a board and looks at the name that was there before. If that person is still in the room, one of them hands their money to the other and waits.

The one with the money goes on. At the end, one person drops a large sum into the box at once. Then each person learns what the box held at the moment their own money went in.

## The abstract type

The funnel implements a counter with fetch-and-add:

- fetch-and-add$(x)$ adds $x$ to the counter and returns the value it had just before.

Each call is [linearizable](/linearizability/) with respect to this sequential counter. All calls that were combined into one fetch-and-add take effect at that one step, one after another, in the order in which their ranges were given out. The same funnel can sit in front of other objects whose operations can be combined or eliminated, for example a stack (see Variants).

## Representation

- $F.layer[0..D-1]$: $D$ arrays of cells, of widths $w_0 \ge w_1 \ge \ldots$, usually halving. Each cell holds a thread id or NIL and is changed by atomic swap.
- $F.counter$: the shared counter, changed by fetch-and-add.
- For each thread $me$, a record with:
  - $loc$: the layer the thread is on, or SELF while it is busy capturing, or CAPTURED once another thread has taken over its operation. Changed by compare-and-swap (CAS).
  - $sum$: its own amount plus the sums of the threads it has captured.
  - $kids$: the captured threads, each with the offset of its share.
  - $result$: written by the capturer when the result is known.

A thread may capture another only if both are on the same layer $d$, which means each has already combined about the same number of calls. That keeps the trees of captures balanced.

## Operations

```pseudo id=main
FETCH-AND-ADD(F, x)                       ▷ run by thread me
L1  me.sum ← x; me.kids ← empty; me.result ← NONE; me.loc ← 0
L2  for d ← 0 to D − 1
L3      q ← SWAP(F.layer[d][a random cell], me)
L4      if q ≠ NIL and q ≠ me then
L5          if not CAS(me.loc, d, SELF) then go to L11          ▷ someone captured me
L6          if CAS(q.loc, d, CAPTURED) then append (q, me.sum) to me.kids; me.sum ← me.sum + q.sum
L7          me.loc ← d
L8      stay on the layer for a few steps
L9      if not CAS(me.loc, d, d + 1) then go to L11
L10 v ← FETCH-AND-ADD(F.counter, me.sum); go to L12
L11 wait until me.result ≠ NONE; v ← me.result
L12 for each (q, base) in me.kids: q.result ← v + base
L13 return v
```

**Collisions.** A thread first locks its own record (line L5): it changes its $loc$ from $d$ to SELF. If this fails, the thread has been captured and only waits. Then it tries to capture $q$ (line L6), which succeeds only if $q$ is on the same layer and not busy. The captured thread can no longer change its sum, so the capturer may read it. Line L7 unlocks the record again.

**Leaving a layer.** Line L9 moves the thread to the next layer with one CAS. If it fails, someone captured the thread in the meantime. A thread that leaves the last layer uncaptured is the root of a tree of captures, and its $sum$ is the sum of all calls in the tree.

**Distribution.** The root applies its sum with a single fetch-and-add (line L10). Its own call gets $v$, and each captured thread $q$ gets $v$ plus the offset recorded at capture time, which is the sum of the capturer's call and of all threads it had captured before $q$. Each captured thread passes the results on to its own kids in the same way (line L12).

**Waiting on a layer.** Line L8 keeps a thread on a layer for a short time so that later threads can find it. Without load a thread finds NIL or stale ids and passes all layers in $O(D)$ steps.

## Example

Four threads $A$, $B$, $C$, $D$ each add 1 to a counter that holds 0. The funnel has layer 0 of width 2 and layer 1 of width 1.

| step | thread | what it does | effect |
|---|---|---|---|
| 1 | $A$ | L3 on layer 0, cell 0 | cell 0 holds $A$ |
| 2 | $B$ | L3 on layer 0, cell 0: gets $A$; L5, L6 | $B$ captures $A$ at offset 1; $B.sum = 2$ |
| 3 | $C$ | L3 on layer 0, cell 1 | cell 1 holds $C$ |
| 4 | $D$ | L3 on layer 0, cell 1: gets $C$; L5, L6 | $D$ captures $C$ at offset 1; $D.sum = 2$ |
| 5 | $B$ | L9, then L3 on layer 1 | the cell of layer 1 holds $B$ |
| 6 | $D$ | L9, then L3 on layer 1: gets $B$; L5, L6 | $D$ captures $B$ at offset 2; $D.sum = 4$ |
| 7 | $D$ | L10: fetch-and-add 4 | counter 0 to 4; $v = 0$ |
| 8 | $D$ | L12: $C$ gets $0 + 1$, $B$ gets $0 + 2$; returns 0 | |
| 9 | $C$, $B$ | L11; $B$ at L12: $A$ gets $2 + 1$ | $C$ returns 1, $B$ returns 2, $A$ returns 3 |

The counter saw one fetch-and-add instead of four. The four calls are linearized at step 7 in the order $D$, $C$, $B$, $A$, which gives exactly the results 0, 1, 2, 3.

## Correctness

The proof is in [the correctness proof](proofs/correctness.md). The key facts:

- *Captures are exclusive.* A thread is captured at most once per call, since only one CAS can change its $loc$ from $d$ to CAPTURED, and a thread whose $loc$ is SELF or CAPTURED cannot capture or be captured. So the captures of a moment form a forest, and a captured thread's sum never changes again.
- *Sums.* By induction on the captures, the sum of a thread is its own amount plus the amounts of all calls in its subtree, and the offsets give these calls disjoint, consecutive ranges inside $[0, sum)$.
- *Linearizability.* The root of each tree applies its sum in one fetch-and-add at line L10. All calls in the tree are pending at that moment, since a captured call only returns after it gets its result, which is computed from $v$. Linearize them at that step, in the order of their offsets. The call at offset $b$ then sees the counter at $v + b$, which is what line L12 gives it. Every call is in exactly one tree, and so is linearized exactly once.
- *Progress.* The funnel is blocking: a captured call waits for its capturer. But no thread ever waits for a thread that it captured, a root never waits at all, and each layer is passed in a bounded number of steps, so every call finishes in a bounded number of its own steps once its capturers have run. In a run where every thread keeps taking steps, every call finishes. A thread that stops while it holds captured calls blocks them for ever, as in a combining tree.

## Complexity

| quantity | value |
|---|---|
| steps of a call that combines nothing | $O(D)$, plus the waits of line L8 |
| fetch-and-adds on the counter for $m$ concurrent calls | between about $m / 2^D$ and $m$ |
| depth of a tree of captures | at most $D$ |
| space | the cells of the layers, plus one record per thread |

With layers of widths about $p, p/2, \ldots, 1$ for $p$ threads, the number of calls that reach the counter at the same time falls by about half per layer when the load is high. Shavit and Zemach make the widths and the waiting time adapt to the observed collision rate: under low load a thread uses narrow layers, or skips the funnel, and pays almost nothing. Their experiments show funnels to scale better than combining trees for counters, and their elimination funnel to be among the fastest stacks of the time.

## Variants

- **Elimination.** For a stack, a push and a pop that collide can cancel each other: the pop takes the pushed value, and neither touches the stack. Two pushes, or two pops, combine as above. The [elimination back-off stack](/elimination-backoff-stack/) of Hendler, Shavit and Yerushalmi uses one such layer in front of a [Treiber stack](/treiber-stack/).
- **Adaptive funnels.** Each thread picks how wide a part of each layer to use and how long to wait, from its own recent collisions, so the funnel thins out when contention drops.
- **[Combining trees](/combining-tree/).** The static ancestor: the pairing of threads is fixed by the leaves, so a lone thread must still climb the whole tree.
- **[Diffracting trees](/diffracting-tree/).** A related idea from Shavit and Zemach: colliding tokens in a prism are sent in opposite directions, which gives a counting network rather than a combined operation.
- **[Flat combining](/flat-combining/).** One thread takes a lock and performs all pending calls from a public list; simpler, with less parallelism at the object.

## When to use it

Use a combining funnel in front of a hot spot whose operations can be combined, such as a shared counter, a fetch-and-add on an index, or a stack or pool with elimination, on a machine with many threads and bursts of contention. When contention is low, a single atomic operation with [exponential back-off](/exponential-backoff/) is cheaper. When exact values are not needed, a [sloppy counter](/sloppy-counter/) avoids the shared word almost always.

## Pitfalls

- **Capturing a thread on another layer.** Without the check that both are on the same layer, trees become unbalanced and deep, and the waits grow. The CAS of line L6 tests the layer.
- **Reading a sum before the capture.** A thread may still be capturing others while its id is in a cell. Read its sum only after the CAS to CAPTURED, which freezes it, and lock your own record first, as in line L5.
- **Stale ids.** A cell can hold the id of a thread that has finished or started a new call. The CAS on $loc$ with the layer number makes such a capture fail, or capture the new call, which is also correct.
- **Waiting too long.** The wait of line L8 helps collisions under load and costs latency without load. Tune or adapt it.
- **A stopped thread.** A thread that stops after it captured others blocks them. The funnel is not lock-free.

## Implementations

The Python module models every cell, every $loc$ field, every result field and the counter as a shared word whose swap, CAS and fetch-and-add are simulated with a lock, and makes every access one step of a generator. The cell chosen on each layer comes from a seeded random generator or from a script. The tests replay the example step by step, check that a funnel with no layers is a plain counter, check stale ids, compare a long sequential run with a running total, check random interleavings of three threads with a linearizability search, and count that many of them combined calls, and run the plain method under real threads, checking that the 800 results are exactly $0, \ldots, 799$.

## History

Hardware combining of fetch-and-add in the network of the NYU Ultracomputer dates from 1983. Yew, Tzeng and Lawrie, and Goodman, Vernon and Woest, moved combining into software trees in 1987 and 1989. Shavit and Zemach presented combining funnels at PODC 1998, with the journal version in 2000, after their diffracting trees of 1996. The elimination idea of the funnel led to the elimination back-off stack of Hendler, Shavit and Yerushalmi in 2004.

## References
