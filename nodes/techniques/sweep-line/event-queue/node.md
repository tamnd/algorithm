---
tag: 324RJK
kind: data-structure
slug: event-queue
name: Event queue
aliases:
- event schedule
- event-point schedule
area: techniques/sweep-line
level: intro
summary: Priority queue that yields the next event point in sweep order.
implements: [priority-queue]
prereqs: [priority-queue, binary-heap, event-point]
see_also: [sweep-line-technique, sweep-status-structure, bentley-ottmann-algorithm, balanced-binary-search-tree, collision-prediction-and-resolution, event-driven-simulation, indexed-priority-queue, degeneracy-in-sweeps]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Chapter 2, Section 2.1 (the event queue Q of the plane sweep for segment intersection)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 33.2 (the sorted array of endpoints of ANY-SEGMENTS-INTERSECT) and Chapter 6 (priority queues)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 6.1, Event-driven simulation (the priority queue of collision events and the test of invalid events)
  - paper: doi:10.1109/SFCS.1976.16
    title: Michael Ian Shamos and Dan Hoey, Geometric intersection problems, 17th Annual Symposium on Foundations of Computer Science, 1976
    locator: pp. 208 to 215
  - paper: doi:10.1109/TC.1979.1675432
    title: Jon L. Bentley and Thomas A. Ottmann, Algorithms for reporting and counting geometric intersections, IEEE Transactions on Computers C-28(9), 1979
    locator: pp. 643 to 647
---

The event queue of a [sweep](/sweep-line-technique/) is the [priority queue](/priority-queue/) of the [event points](/event-point/) that the sweep line has not reached yet, ordered by the sweep order. It returns the next event point with all the work attached to it, and it accepts new event points that the sweep finds while it runs. An insert of a point that is already in the queue does not create a second event: the two are merged into one event point. With $m$ points in the queue each operation costs $O(\log m)$, so the [Bentley-Ottmann algorithm](/bentley-ottmann-algorithm/), which handles $O(n + k)$ event points, spends $O((n + k) \log n)$ time in its queue.

## In plain words

A sweep moves a line across the plane and stops only at special places, the events. The event queue is the to-do list of these stops, kept in the order in which the line reaches them. The sweep takes the first stop from the list, does the work for it, and may then add new stops further ahead.

Two pieces of work can belong to the same place, for example a segment that ends where another one starts. The queue keeps one stop for that place and attaches both pieces of work to it. The same stop can also be found twice during the sweep; the queue then does not add a copy.

When all the stops are known before the sweep starts, a sorted list is enough. When the sweep finds new stops on the way, a heap or a balanced search tree is needed.

## The abstract type

The event queue is a [priority queue](/priority-queue/) whose keys are event points and whose order is the sweep order. For a vertical line that moves from left to right, a point is a pair $(x, y)$ and the order is lexicographic:

$$ (x_1, y_1) < (x_2, y_2) \iff x_1 < x_2 \text{ or } (x_1 = x_2 \text{ and } y_1 < y_2). $$

Points with the same $x$ are handled from bottom to top. This is the order of a line that is turned by a very small angle, so that it meets no two points at the same time. De Berg et al. sweep a horizontal line from top to bottom and order the points by decreasing $y$, then by increasing $x$. That is the same order after a rotation of the plane by a quarter turn.

The queue $Q$ holds a set of distinct points, and each point $p$ has a list $A(p)$ of payloads, for example the segments whose left endpoint is $p$. The operations are:

- INSERT$(Q, p, a)$: if $p \in Q$, append the payload $a$ to $A(p)$; else add $p$ with $A(p) = [a]$. The payload may be NIL; then INSERT only makes sure that $p$ is in $Q$.
- POP-MIN$(Q)$: remove the smallest point $p$ of $Q$ and return $(p, A(p))$. The precondition is $Q \ne \emptyset$.
- CONTAINS$(Q, p)$: return whether $p \in Q$.
- IS-EMPTY$(Q)$: return whether $Q = \emptyset$.

The merge rule is the difference from a plain priority queue. A plain priority queue keeps two inserts of the same key as two entries and returns them one after the other. The sweep needs one event for each point, because all the segments through a point must be handled together.

## Representation

**Balanced search tree.** De Berg et al. store $Q$ in a [balanced binary search tree](/balanced-binary-search-tree/) keyed by the event order, with $A(p)$ stored at the node of $p$ (Section 2.1). A search for $p$ finds an existing event, so the merge and CONTAINS cost $O(\log m)$, and the leftmost node is the minimum. They state that they do not use a heap because they must test whether an event is already present.

**Heap and index.** The implementation of this page uses a [binary heap](/binary-heap/) of the distinct points, and a [hash table](/hash-table/) `index` from each point in the queue to its list $A(p)$. The representation invariant is:

1. the points in the heap are distinct, and they are exactly the keys of `index`;
2. the heap has the heap order: each point is not smaller than its parent;
3. `index`$[p]$ is the list of the non-NIL payloads inserted with $p$ since $p$ last entered the queue, in the order of the inserts.

The index answers "is $p$ present" in $O(1)$ expected time. A heap alone cannot do that without a scan of all its entries.

## Operations

```pseudo id=main
INSERT(Q, p, a)                          ▷ a may be NIL
L1  if p ∈ Q.index then                  ▷ p is already an event
L2      if a ≠ NIL then append a to Q.index[p]
L3  else Q.index[p] ← [a], or [] if a = NIL
L4      HEAP-INSERT(Q.heap, p)           ▷ the heap holds each point once

POP-MIN(Q)                               ▷ precondition: Q is not empty
L5  p ← HEAP-EXTRACT-MIN(Q.heap)
L6  A ← Q.index[p], and delete the key p from Q.index
L7  return (p, A)

CONTAINS(Q, p)
L8  return p ∈ Q.index

IS-EMPTY(Q)
L9  return Q.heap is empty
```

**INSERT.** Line L1 looks up $p$ in the index. If $p$ is present, line L2 adds the payload to the existing event and the heap does not change. Otherwise lines L3 and L4 create the event and push the point on the heap. The cost is $O(1)$ expected for the index and $O(\log m)$ for the push.

**POP-MIN.** Line L5 removes the smallest point from the heap in $O(\log m)$ time. Line L6 takes its payload list and removes the key from the index, so a later insert of the same point creates a new event. This can happen in a [simulation](/event-driven-simulation/), where a time can be scheduled again after it was handled. In a geometric sweep it does not happen, because each new event lies after the current one.

**CONTAINS and IS-EMPTY.** Line L8 is one lookup in the index, $O(1)$ expected. Line L9 tests the size of the heap, $O(1)$.

With the search tree of de Berg et al., INSERT is one search followed by an insert or an append, POP-MIN deletes the leftmost node, and each costs $O(\log m)$ in the worst case.

## Example

Take three segments: $a$ from $(0, 0)$ to $(10, 10)$, $b$ from $(0, 10)$ to $(10, 0)$, and $c$ from $(1, 5)$ to $(3, 5)$. The payload of an event is the list of segments that start there, as in de Berg et al.; right endpoints and intersections are inserted with a NIL payload, because the [status structure](/sweep-status-structure/) finds the segments through them. The sweep first inserts the six endpoints. Then it pops events and inserts the intersections that it finds between new neighbors.

| step | operation | result | queue after the step |
|---|---|---|---|
| 0 | insert the 6 endpoints | | (0,0)[a] (0,10)[b] (1,5)[c] (3,5)[] (10,0)[] (10,10)[] |
| 1 | POP-MIN | (0,0), [a] | (0,10)[b] (1,5)[c] (3,5)[] (10,0)[] (10,10)[] |
| 2 | POP-MIN | (0,10), [b] | (1,5)[c] (3,5)[] (10,0)[] (10,10)[] |
| 3 | INSERT((5,5), NIL) | $a$ and $b$ are neighbors and cross at (5,5) | (1,5)[c] (3,5)[] (5,5)[] (10,0)[] (10,10)[] |
| 4 | POP-MIN | (1,5), [c] | (3,5)[] (5,5)[] (10,0)[] (10,10)[] |
| 5 | POP-MIN | (3,5), [] | (5,5)[] (10,0)[] (10,10)[] |
| 6 | INSERT((5,5), NIL) | $c$ is gone, $a$ and $b$ are neighbors again; (5,5) is present, nothing is added | (5,5)[] (10,0)[] (10,10)[] |
| 7 | POP-MIN | (5,5), [] | (10,0)[] (10,10)[] |
| 8 | POP-MIN | (10,0), [] | (10,10)[] |
| 9 | POP-MIN | (10,10), [] | empty |

Step 6 shows why the merge is needed. A plain heap would hold (5,5) twice, and the sweep would swap $a$ and $b$ twice, which puts them back in the wrong order. Step 8 shows the lexicographic order: (10,0) comes before (10,10) because the two points have the same $x$. There are 7 events, which is $2n + k$ for $n = 3$ segments and $k = 1$ intersection.

## Correctness

Each operation keeps the representation invariant, and under the invariant each operation returns the result that the abstract type asks for. INSERT keeps the heap free of duplicates because it pushes $p$ only when $p$ is not a key of the index, and it adds the key and the heap entry together. POP-MIN removes the heap minimum and its key together. By the heap order, the root is the smallest point present, so POP-MIN returns the smallest event point with the payloads of all the inserts of that point. The full proof is below.

## Complexity

Let $m$ be the number of distinct points in the queue. The heap holds exactly $m$ entries, one for each point, so its height is $\lfloor \lg m \rfloor$.

| operation | heap and hash index | balanced search tree | sorted array (static) |
|---|---|---|---|
| INSERT, new point | $O(\log m)$, plus $O(1)$ expected for the index | $O(\log m)$ worst case | not supported |
| INSERT, present point | $O(1)$ expected | $O(\log m)$ worst case | not supported |
| POP-MIN | $O(\log m)$, plus $O(1)$ expected | $O(\log m)$ worst case | $O(1)$ |
| CONTAINS | $O(1)$ expected | $O(\log m)$ worst case | $O(\log m)$ by [binary search](/binary-search/) |
| IS-EMPTY | $O(1)$ | $O(1)$ | $O(1)$ |
| space | $O(m + \text{payloads})$ | $O(m + \text{payloads})$ | $O(m + \text{payloads})$ |

**Bentley-Ottmann.** For $n$ segments with $k$ intersection points, the event points are the at most $2n$ endpoints and the $k$ intersection points, so there are at most $2n + k$ pops. Each event makes $O(1)$ inserts of intersection points, one for each new pair of neighbors, so there are $O(n + k)$ inserts. For segments of which no two overlap, each intersection point is a crossing of at least one pair, so $k \le n(n-1)/2$, and the queue never holds more than $2n + n(n-1)/2$ points, and $\log m = O(\log n)$. The total time in the queue is $O((n + k) \log n)$. De Berg et al. also keep the space at $O(n)$: an intersection event is deleted from the queue when its two segments stop being neighbors, so the queue holds only intersections of current neighbors (Section 2.1 and its exercises).

**Lower bound.** In the [comparison model](/comparison-model/), $m$ inserts of distinct points followed by $m$ pops sort the points. Sorting needs $\Omega(m \log m)$ comparisons in the worst case ([comparison sort lower bound](/comparison-sort-lower-bound/)), so no comparison-based event queue does both operations in $o(\log m)$ amortized time.

## Variants

- **Static queue.** When all the events are known before the sweep, sort them into an array and read it from left to right. Merging equal points means grouping each run of equal keys after the sort. The [rectangle union sweep](/rectangle-union-sweep/), the [skyline sweep](/skyline-sweep/) and the [closest pair sweep](/closest-pair-sweep-line/) work this way, and so does ANY-SEGMENTS-INTERSECT of CLRS (Section 33.2), which only detects whether some pair intersects, so it needs no intersection events. Its sort puts left endpoints before right endpoints at equal $x$, and lower $y$ first among each group.
- **Dynamic queue.** When the sweep creates events, the queue must accept inserts while it runs. [Bentley-Ottmann](/bentley-ottmann-algorithm/) inserts intersection points, and [Fortune's algorithm](/fortunes-algorithm/) inserts circle events (de Berg et al., Chapter 7).
- **Lazy deletion of invalid events.** Some events stop being valid before the sweep reaches them: in Fortune's algorithm a circle event is a false alarm when its arc disappears first, and in a [collision simulation](/collision-prediction-and-resolution/) a predicted collision does not happen when one of the two particles hits something else first. One option is to delete the event at once, which needs a pointer to it in the queue, as with an [indexed priority queue](/indexed-priority-queue/). The other is to leave it in the queue and discard it when it is popped. Sedgewick and Wayne (Section 6.1) store in each collision event the collision counts of its particles at the time of the prediction. A particle's count goes up at each of its collisions, so a popped event whose counts differ from the current ones is stale and is skipped. The queue then holds more entries than there are valid events, which costs space and makes $m$ larger.
- **Ties and degeneracies.** The order of events at the same point, or at the same $x$, is part of the algorithm. Each sweep must fix it; see [degeneracy in sweeps](/degeneracy-in-sweeps/).
- **Other priority queues.** Any [priority queue](/priority-queue/) works if the merge rule is added. A [calendar queue](/calendar-queue/) is common in discrete event simulation, where the keys are times.

## When to use it

Use a sorted array when the sweep never creates events: it is simple, fast and uses no pointers. Use a heap with a hash index when events are created on the way and keys can be hashed, for example integer or rational coordinates. Use a balanced search tree when the points cannot be hashed in a way that agrees with equality, or when you need worst-case bounds and the deletion of an arbitrary event, as in the $O(n)$-space version of Bentley-Ottmann. Use lazy deletion when many events become invalid and a delete by handle is not available.

## Pitfalls

- **Duplicate events.** A heap without the index of lines L1 to L4 keeps two copies of a point that is found twice, as in step 6 of the example. The sweep then handles the point twice. In Bentley-Ottmann a second swap of the same two segments breaks the order of the status structure.
- **Points that are equal but not identical.** With floating-point coordinates, an intersection computed from two different pairs of segments can differ in the last bit, so the merge does not happen. Use exact coordinates (integers or rationals) for the keys, or snap them to a grid.
- **The wrong order of ties.** Ordering by $x$ only leaves the order of points with equal $x$ undefined. The sweep then depends on the heap's internal order. Use the full lexicographic order of the abstract type.
- **Stale events.** A sweep that deletes nothing must check each popped event against the current state before it acts on it. A collision that is predicted for two particles and processed after one of them changed its course moves the particles in a wrong way.
- **A key that is popped and inserted again.** After POP-MIN the point is no longer in the queue. A geometric sweep must insert only points after the current event, because a point at or before it is never popped in the right order.

## Implementations

## History

Shamos and Hoey (1976) used a plane sweep with a static queue of endpoints to detect whether any two of $n$ segments intersect, in $O(n \log n)$ time. Bentley and Ottmann's algorithm reports the $k$ intersections of $n$ segments in $O((n + k) \log n)$ time with an event queue that receives the intersection points during the sweep. De Berg et al. present the method with a balanced search tree as the event queue and explain why they do not use a heap.

## References
