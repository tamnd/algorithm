---
tag: GA0P2G
kind: data-structure
slug: spraylist
name: SprayList
area: data-structures/concurrent-structures
level: research
summary: Relaxed concurrent priority queue on a skip list whose delete-min sprays to random nearby elements to reduce contention.
prereqs: [relaxed-priority-queue, lock-free-skip-list, compare-and-swap]
see_also: [multiqueue, skip-list, fine-grained-concurrent-heap, delta-stepping, lock-freedom, linearizability, priority-queue]
sources:
  - paper: doi:10.1145/2688500.2688523
    title: Dan Alistarh, Justin Kopinsky, Jerry Li and Nir Shavit, The SprayList, a scalable relaxed priority queue, PPoPP 2015
    locator: pages 11 to 20, the spray walk and its parameters, the bound on the rank of the item returned, and the experiments
  - book: isbn:9780123973375
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, revised reprint
    locator: Chapter 14 (Skiplists and Balanced Search), the lock-free skip list; Chapter 15 (Priority Queues), the skip-list-based priority queue
  - paper: doi:10.1145/2755573.2755616
    title: Hamza Rihani, Peter Sanders and Roman Dementiev, MultiQueues, simple relaxed concurrent priority queues, SPAA 2015
    locator: pages 80 to 82, the comparison with the SprayList
---

The SprayList is a [relaxed priority queue](/relaxed-priority-queue/) built on a [lock-free skip list](/lock-free-skip-list/). An exact skip-list priority queue makes every delete-min fight for the first node of the list. In the SprayList, delete-min instead makes a short random walk, a *spray*, from the head: it starts a few levels up, moves forward a random number of nodes on each level, goes down, and lands on a node near the front. It claims that node with one [compare-and-swap](/compare-and-swap/). Different threads land on different nodes, so they rarely collide, and the node they take is with high probability among the first $O(p \log^3 p)$ items for $p$ threads. Alistarh, Kopinsky, Li and Shavit introduced it in 2015.

## In plain words

Picture a long line of people sorted by their ticket numbers, with some of them holding up signs so that you can skip ahead. In an exact queue every clerk calls the person at the very front, and all clerks shout at once for the same person.

In a SprayList each clerk closes their eyes, jumps a few signs ahead, then a few people ahead, and calls whoever they land on. That person is not the very first, but is near the front. Two clerks rarely land on the same person, so they rarely have to wait for each other.

## The abstract type

The SprayList implements a relaxed priority queue over a multiset $Q$:

- insert$(x)$ adds $x$ to $Q$.
- delete-min() removes and returns some item of $Q$, or returns EMPTY if $Q$ is empty.

Each operation is [linearizable](/linearizability/) with respect to this nondeterministic specification. The quality of the item returned is a separate, probabilistic guarantee: with the parameters of the paper, its rank is $O(p \log^3 p)$ with high probability, independent of the size of $Q$.

## Representation

- A lock-free skip list in the style of Herlihy and Shavit, ordered by key. Each node has a key, a height, and on each of its levels a next reference with a mark bit, read and changed together by compare-and-swap. A marked reference means that the node is being unlinked on that level.
- Each node has a flag *claimed*, set by compare-and-swap. A node is in $Q$ when it is linked on level 0 and not claimed.
- Two counters, $started$ and $linked$, count the inserts that have begun and those that have linked their node on level 0. They let delete-min decide EMPTY safely.
- The spray parameters: a starting level $H$, a largest jump $L$ and a descent $D$. The paper takes $H$ about $\log p$, $L$ polylogarithmic in $p$, and $D$ about $\log \log p$; the Python module uses $H = \lceil \log_2 p \rceil$, $L = H^3$ and $D = \lceil \log_2 H \rceil$.

Equal items are stored as distinct keys, each with a unique serial number.

## Operations

```pseudo id=main
DELETE-MIN(S)
L1  x ← S.head; h ← H
L2  loop
L3      j ← a random number in 0..L
L4      move x forward j nodes on level h, or to the last node of the level
L5      if h = 0 then exit the loop else h ← max(0, h − D)
L6  walk level 0 from x to the first node that is not claimed, and try CAS(node.claimed, false, true); on failure walk on
L7  if a node was claimed then REMOVE(S, node); return its item
L8  l ← S.linked; s ← S.started                      ▷ the spray fell off the end
L9  x ← the first node of level 0
L10 walk level 0 from x as in line L6; if a node is claimed, REMOVE(S, node) and return its item
L11 if l = s and S.started = s then return EMPTY
L12 go to line L1

INSERT(S, x)
L13 FETCH-AND-ADD(S.started, 1)
L14 FIND the place of x; link a new node of random height on level 0 by CAS; retry on failure
L15 FETCH-AND-ADD(S.linked, 1)
L16 link the node on each level above, by CAS, finding new neighbours after each failure

REMOVE(S, node)
L17 mark the next reference of node on each level, from the top down
L18 FIND(node.key), which unlinks every marked node that it passes
```

**The spray.** Lines L1 to L5 are the random walk. On each visited level the walk moves forward a uniform random number of nodes, then goes down $D$ levels, and it always ends on level 0. Since a node on level $h$ stands for about $2^h$ nodes of level 0, jumps on high levels cover large distances and jumps on low levels spread the landing points.

**Claiming.** The compare-and-swap on the claimed flag at line L6 is the logical deletion: exactly one thread can claim each node. A thread that lands on a claimed node just walks on. The thread that claimed a node then unlinks it with the usual removal of the lock-free skip list (lines L17 and L18).

**Empty.** If the spray reaches the end of the list without a claim, delete-min scans level 0 from the head. It returns EMPTY only if it found nothing, no insert was between lines L13 and L15 when it read the counters, and no insert started during the scan. Otherwise it sprays again.

**Insert.** Insert is the lock-free skip list insert: it links the node on level 0, which puts the item in $Q$, and then on the higher levels. A node whose removal starts while it is still being linked is left alone on the higher levels; the next FIND that passes it unlinks it.

## Example

Eight items with these heights: 40 reaches level 2; 20, 40 and 60 reach level 1; all reach level 0. With $p = 4$ threads the spray starts on level 2 and goes down one level at a time.

| call | jumps on levels 2, 1, 0 | path | lands on | returns | rank |
|---|---|---|---|---|---|
| delete-min | 1, 0, 1 | head, 40, 40, 50 | 50 | 50 | 5 |
| delete-min | 1, 0, 1 | head, 40, 40, then the node after 40 | 60 (50 is gone) | 60 | 5 |
| delete-min | 0, 0, 0 | head | the first node, 10 | 10 | 1 |

Now two threads $A$ and $B$ spray at the same time, with no jumps, on the list 1, 2, 3. $A$ lands on 1 and claims it. Before $A$ has unlinked node 1, $B$ also lands on node 1, sees that it is claimed, walks on, and claims 2. They paid one extra read for the collision and never waited for each other.

## Correctness

Insert takes effect when its node is linked on level 0 (line L14), and a delete-min that returns an item takes effect at its successful claim (line L6 or line L10). The claimed node is linked on level 0 at that moment: a node is unlinked only after it was claimed, so it was in $Q$, and no other call can claim it again. An EMPTY result takes effect at the last read of $started$ in line L11. The counters show that no node was linked on level 0 between the first read of $started$ and the last one; the scan in this interval visits every node that is not claimed, because level 0 stays sorted and a node is unlinked only after it was claimed; so at the end every node of level 0 is claimed, and $Q$ is empty. The skip list operations keep each level sorted, as in the proof of the lock-free skip list. Progress: each CAS that fails was beaten by a successful CAS of another call, and a spray that ends in EMPTY retries only while an insert is in progress, so the SprayList is lock-free. The rank bound is the theorem of Alistarh, Kopinsky, Li and Shavit and is not part of this proof. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| quantity | value |
|---|---|
| insert | $O(\log n)$ expected steps without contention, as in a skip list |
| delete-min, spray | $O(L \cdot H / D)$ steps for the walk, plus the removal, $O(\log n)$ expected |
| rank of the item returned, with high probability | $O(p \log^3 p)$, with the parameters of the paper |
| space | $O(n)$ expected, plus claimed nodes that are not yet unlinked |

The paper models the skip list as an ideal one, in which the nodes of level $h$ are spaced about $2^h$ apart, and shows that the landing points of a spray are spread almost uniformly over a prefix of length about $p \log^3 p$, so that no node of this prefix is much more likely to be hit than the others. So $p$ concurrent sprays seldom collide, while the items returned stay near the front. In the Python module, with 4 threads and 3000 items, the mean rank is about 40.

The paper reports that the SprayList scales much better than exact skip-list priority queues at high thread counts. Rihani, Sanders and Dementiev report that the [MultiQueue](/multiqueue/) is faster still on their machines.

## Variants

- **Exact skip-list queues.** With $L = 0$ every spray lands on the head, and the structure is the lock-free skip-list priority queue of Herlihy and Shavit, after Lotan and Shavit: exact items, but all threads compete for the front.
- **Few threads.** For small $p$, contention is low and sprays are not needed; an implementation can switch to exact deletes.
- **Cleaning.** Claimed nodes at the front slow down later walks. Implementations unlink them in batches, so that walks do not pay for each claimed node.
- **[MultiQueue](/multiqueue/).** A relaxed queue from many sequential heaps with locks; simpler and, in published experiments, faster.
- **k-LSM.** A relaxed queue with a deterministic bound on the rank error of every call.

## When to use it

Use a SprayList as a shared work list for algorithms that tolerate items out of order, such as parallel shortest paths in the style of [delta-stepping](/delta-stepping/), branch and bound, or priority schedulers, when a lock-free structure is wanted. When locks are acceptable, a MultiQueue is simpler and usually faster. When the order of items matters for correctness, use an exact priority queue.

## Pitfalls

- **Taking the spray for an exact queue.** The item returned can be far from the minimum, up to the polylogarithmic bound, and the bound is probabilistic.
- **Returning EMPTY because the spray fell off.** A spray can pass the end of a list that is not empty. Check from the head, and only return EMPTY when no insert can have been missed.
- **Wrong parameters.** A jump that is too short makes threads collide at the front; one that is too long makes the rank error large. The parameters depend on the number of threads $p$, which must be known or estimated.
- **A spray over a degenerate list.** The analysis assumes the skip list has its usual random heights. Few items, or a bad random source, change the distribution of landing points.
- **Claimed nodes that pile up.** If claimed nodes are not unlinked, every spray walks over them; unlink them promptly or in batches.

## Implementations

The Python module models every reference of the skip list as a word with a mark bit and compare-and-swap, simulated with a lock, and the claimed flags and counters as atomic words. Each access is one step of a generator. The tests replay the example with scripted random choices, show a collision on a claimed node, check that $L = 0$ gives an exact queue, compare random sequential runs with a multiset, measure the mean rank, check random interleavings of three threads against the relaxed specification with a linearizability search, and run the plain methods under real threads.

## History

Pugh introduced skip lists in 1990. Lotan and Shavit built a concurrent priority queue on a skip list in 2000, and Herlihy and Shavit's textbook gives a lock-free version. Exact queues of this kind stop scaling because all delete-mins meet at the first node. Alistarh, Kopinsky, Li and Shavit replaced the walk to the first node by a random spray in 2015 and proved the rank bound. The MultiQueue appeared the same year, and Alistarh, Kopinsky, Li and Nadiradze analysed it in 2017.

## References
