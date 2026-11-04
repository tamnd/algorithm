---
tag: 5B1WV2
kind: data-structure
slug: fine-grained-concurrent-heap
name: Fine-grained concurrent heap
aliases:
- Hunt et al. concurrent heap
area: data-structures/concurrent-structures
level: research
summary: Binary heap with per-node locks and bit-reversed insertion order, letting inserts and deletes proceed in parallel.
prereqs: [binary-heap, priority-queue, lock-coupling]
see_also: [multiqueue, spraylist, relaxed-priority-queue, bit-reversal, quiescent-consistency, deadlock, linearizability, mutex]
sources:
  - paper: doi:10.1016/S0020-0190(96)00148-2
    title: Galen C. Hunt, Maged M. Michael, Srinivasan Parthasarathy and Michael L. Scott, An efficient algorithm for concurrent priority queue heaps, Information Processing Letters 60(3), 1996
    locator: pages 151 to 157, the slot tags, the bit-reversed order of the bottom slots, insert with its moves up and delete-min with its moves down
  - book: isbn:9780123973375
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, revised reprint
    locator: Chapter 15 (Priority Queues), the fine-grained heap, with the same tags and the owner check of insert
---

The fine-grained concurrent heap is an array [binary heap](/binary-heap/) with one lock on each slot and one lock on the size, so that many inserts and delete-mins can work on the heap at the same time. Hunt, Michael, Parthasarathy and Scott gave it in 1996. A call holds the size lock only for a moment, to pick its bottom slot, and then holds at most two slot locks at a time while it moves an item up or down. Two ideas make this work. First, each slot has a *tag* that says whether the slot is empty, holds an item in its place, or holds an item that an insert is still moving up. Second, the bottom slots are used in bit-reversed order, so that successive inserts start in different subtrees and do not meet on their way to the root.

## In plain words

Think of a pyramid of boxes, each with its own key. The smallest number must be at the top, and each box must be no larger than the boxes under it.

To add a number, a worker puts it in a free box at the bottom and carries it up, one level at a time, as long as it is smaller than the box above. To take the smallest number, a worker takes the top box, puts the last bottom number there, and carries that number down.

Each worker only opens two boxes at a time, so many workers can carry numbers at once. A label on each box tells the others whether its number is still on the move.

## The abstract type

The heap holds a multiset $Q$ of items:

- insert$(x)$ adds $x$ to $Q$.
- delete-min() removes and returns a smallest item of $Q$, or returns EMPTY if $Q$ is empty.

Run alone, each call does exactly this. Under concurrency the guarantee is weaker than [linearizability](/linearizability/). No item is lost or duplicated; whenever no call is running, the array is a valid heap of exactly the items of $Q$; and a call that overlaps no other call returns the true minimum. But two overlapping delete-mins can return a pair of items that no sequential order explains (see Example), so the heap is not linearizable as an exact [priority queue](/priority-queue/), and it is not even [quiescently consistent](/quiescent-consistency/).

## Representation

- $H.slot[1..N]$: an array heap, slot $i$ with children $2i$ and $2i + 1$. Each slot has a lock, a priority $pri$ and a tag.
- The tag is EMPTY for an unused slot, AVAILABLE for an item that is in its place, and the id of an inserting thread for an item that this insert is still moving up.
- $H.size$ and its own lock. The items fill the slots $rev(1), \ldots, rev(size)$.
- $rev(n)$ keeps the top bit of $n$ and reverses the bits below it, so the slots of each level are used in [bit-reversal](/bit-reversal/) order: 1; 2, 3; 4, 6, 5, 7; 8, 12, 10, 14, 9, 13, 11, 15; and so on. Two inserts in a row start in different halves of the tree, so their paths to the root share only the top slots.

The heap order holds between two slots when both are AVAILABLE. An item tagged with an owner may be smaller than its parent until its insert moves it.

## Operations

```pseudo id=main
INSERT(H, x, me)
L1  LOCK(H.size); if H.size = N then fail; H.size ← H.size + 1; i ← rev(H.size)
L2  LOCK(slot[i]); UNLOCK(H.size)
L3  slot[i].pri ← x; slot[i].tag ← me; UNLOCK(slot[i])
L4  while i > 1
L5      p ← i div 2; LOCK(slot[p]); LOCK(slot[i])
L6      if slot[p].tag = AVAILABLE and slot[i].tag = me then
L7          if slot[i].pri < slot[p].pri then swap slot[i] and slot[p]; i ← p
L8          else slot[i].tag ← AVAILABLE; i ← 0            ▷ in place
L9      else if slot[i].tag ≠ me then i ← p                ▷ a delete-min moved the item up, or took it
L10     UNLOCK(the child slot of this round); UNLOCK(slot[p])
L11     if i did not change then wait and retry            ▷ the parent's item belongs to another insert
L12 if i = 1 then LOCK(slot[1]); if slot[1].tag = me then slot[1].tag ← AVAILABLE; UNLOCK(slot[1])

DELETE-MIN(H)
L13 LOCK(H.size); if H.size = 0 then UNLOCK(H.size); return EMPTY
L14 b ← rev(H.size); H.size ← H.size − 1; LOCK(slot[b]); UNLOCK(H.size)
L15 x ← slot[b].pri; slot[b].tag ← EMPTY; UNLOCK(slot[b]); if b = 1 then return x
L16 LOCK(slot[1]); if slot[1].tag = EMPTY then UNLOCK(slot[1]); return x
L17 swap x and slot[1].pri; slot[1].tag ← AVAILABLE; i ← 1
L18 while 2i ≤ N: LOCK(slot[2i]); LOCK(slot[2i + 1])
L19     if slot[2i].tag = EMPTY then unlock both children; exit the loop; c ← the child with the smaller pri that is not EMPTY; unlock the other child
L20     if slot[c].pri < slot[i].pri then swap slot[c] and slot[i]; UNLOCK(slot[i]); i ← c else UNLOCK(slot[c]); exit the loop
L21 UNLOCK(slot[i]); return x
```

**Lock order.** Every call takes the size lock first, and slot locks from the root downward: a parent before its child, a node before its children. Insert releases the lock of its slot at line L3 before it locks the parent at line L5, so it never holds a child while it waits for a parent. Delete-min holds the size lock only while it locks the bottom slot.

**Insert follows its item.** A delete-min that moves down past the item of an insert can swap the item one level up. So at line L9 the insert sees that its slot no longer holds its own tag, and moves to the parent. Items with an owner tag only move up, so the item is at this slot or above it, and the insert finds it again on the way to the root. If a delete-min took the item as its bottom item and put it at the root, the tag is overwritten with AVAILABLE, and the insert climbs to the root, where line L12 finds no own tag and does nothing. The climb must go on even when the parent is EMPTY (see Pitfalls).

**Waiting.** If the parent holds an item that another insert is still moving up, the parent's tag is a thread id and line L6 fails. The insert releases both locks and retries (line L11), and in the meantime the other insert moves its item up or marks it AVAILABLE.

**Delete-min.** Delete-min empties the bottom slot first, under its lock, and only then locks the root. So no insert or delete-min can see the bottom item in two places. Line L16 handles the case where the root is EMPTY: then the heap had only this one item, or the root was itself the bottom slot of another delete-min, and the bottom item is the answer.

## Example

Insert 2, 5, 4, 8, 9, 6 one by one. They go to slots 1, 2, 3, 4, 6, 5, in bit-reversed order, and the moves up give

| slot | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| pri | 2 | 5 | 4 | 8 | 6 | 9 |

(the 6 in slot 5 is under 5, and the 9 in slot 6 is under 4). Now insert 1 with id 7: it goes to $rev(7) = 7$, under slot 3. Line L7 swaps it with 4 into slot 3, then with 2 into slot 1, and line L12 marks it AVAILABLE. Delete-min then takes the bottom slot $rev(7) = 7$, which now holds 4, swaps 4 into the root and gets 1 back. It moves 4 down: the children are 5 and 2, so 4 and 2 swap; in slot 3 the only child left is 9, which is larger, so it stops. The heap is again 2, 5, 4, 8, 6, 9.

**Two overlapping deletes.** Let the heap hold 0 in slot 1, 1 in slot 2 and 13 in slot 3, with size 3. Delete-min $A$ takes 13 from slot $rev(3) = 3$, locks the root, swaps 13 into it and gets 0, and still holds the root lock. Delete-min $B$ now takes 1 from slot $rev(2) = 2$ and waits for the root. $A$ finds no children with items, releases the root and returns 0. $B$ locks the root, swaps 1 into it and returns 13. The heap is left with 1. Both calls ran at the same time, but no order of two exact delete-mins on $\{0, 1, 13\}$ returns 0 and 13: the second one must return 1. The tests replay this schedule. The cause is general: a delete-min chooses its bottom item $b$ before it sees the root, and if another call has changed the root in between, the item it returns can be larger than $b$, which it has just put back.

## Correctness

Four properties hold, and the full proof is in [the correctness proof](proofs/correctness.md).

- *Mutual exclusion.* Each field of a slot is read and written only by the holder of its lock, and the size only by the holder of the size lock.
- *Conservation.* Each item inserted is, at every moment, in exactly one slot, or in the hands of exactly one call: the insert before line L3, or a delete-min between lines L15 and L17, and after it returns. So no item is lost or duplicated, and each item that a delete-min returns was inserted and is returned once.
- *Quiescent heap.* When no call is running, the used slots are exactly $rev(1), \ldots, rev(size)$, all AVAILABLE, and each is at least its parent. The heap order can only be broken between a slot that a call is about to fix and its neighbours, and each call fixes its slot before it ends.
- *Isolated calls.* A call that overlaps no other call starts on a valid heap and runs as a sequential heap operation, so it returns the true minimum.

The example above shows that the heap is not linearizable. A second schedule shows that it is not [quiescently consistent](/quiescent-consistency/) either. Start with 2 at the root and 5 in slot 2. Delete-min $D_1$ takes 5 from slot 2 and holds it. $D_2$ takes 2 from the root, the last slot, and returns 2. $D_3$ sees size 0 and returns EMPTY. An insert of 9 puts 9 at the root. $D_1$ swaps 5 into the root and returns 9. All four calls overlap $D_1$, so quiescent consistency would allow any order of them, but in every order 5 is in $Q$ from the start to the end, so no exact delete-min could return EMPTY or 9. The cause is the same: the size counts only the items in slots, not the item that a delete-min holds. The schedules are those of the pseudocode on this page and of the Python module; they use only steps that the algorithm allows, and the tests replay both.

Progress: the heap is deadlock-free. Locks are always taken in the fixed order (size lock, then slots from the root down), and no call holds a slot lock while it waits for the size lock or for a slot above, so no cycle of lock waits exists. An insert that retries at line L11 because its parent is tagged waits for the insert that owns the parent's item. That owner's item is nearer the root, and the owner nearest the root of such a chain is not blocked by a tag, so it moves its item up or marks it AVAILABLE.

## Complexity

| quantity | value |
|---|---|
| insert, alone | $O(\log n)$ lock pairs, $O(1)$ time holding the size lock |
| delete-min, alone | $O(\log n)$ lock pairs, $O(1)$ time holding the size lock |
| locks held by one call at a time | at most 2 slot locks, or the size lock and 1 slot lock |
| space | $N$ slots, each with a lock, a tag and a priority |

The size lock is held for a constant time, so it is a short serial section. All delete-mins still pass through the root, so the root lock is the point of contention, and throughput does not grow beyond a few threads. Hunt et al. measured that their heap was faster than a heap with one lock and than earlier concurrent heaps, mainly for workloads with many inserts. Under contention, an insert may retry many times while a parent stays tagged.

## Variants

- **One big lock.** A sequential heap with one lock is linearizable and simpler; it is slower only when many calls overlap.
- **Rao and Kumar, and Ayani.** Earlier concurrent heaps moved items top-down on insert as well, so every call started at the root. Hunt et al. avoid this with the bottom-up insert and the tags.
- **The textbook heap.** Herlihy and Shavit present the same algorithm with an owner field for each slot and a status that is EMPTY, AVAILABLE or BUSY. Their insert climbs to the root whenever it does not own the child, as on this page.
- **[MultiQueue](/multiqueue/) and [SprayList](/spraylist/).** [Relaxed priority queues](/relaxed-priority-queue/) give up exact minima on purpose and in return scale to many threads, with a clear, linearizable relaxed specification.
- **Skip-list queues.** The lock-free skip-list priority queue of Herlihy and Shavit, after Lotan and Shavit, is linearizable in its exact form, at the cost of contention at the first node.

## When to use it

Use it when a bounded priority queue with array storage is shared by a few threads, when inserts are frequent, and when the program only needs exact results from calls that do not overlap, for example for an event list in which each event is handled after all earlier calls have ended. When an exact linearizable queue is needed, use a heap with one lock or a skip-list queue. When many threads delete at once, use a relaxed queue.

## Pitfalls

- **Taking it for linearizable.** Overlapping delete-mins can return items out of order, as in the example. Do not use it where a later call must see the result of an earlier one.
- **Locking upward.** An insert that held its slot while it waited for the parent could deadlock with a delete-min that holds the parent and waits for the child. Release the slot before locking the parent.
- **Losing the item.** An insert must follow its tag, not its slot number: a delete-min can move the item up, or take it away.
- **Stopping at an EMPTY parent.** Some versions of the code end the climb when the parent slot is EMPTY, on the idea that the item was then taken away. That is not safe: deletes can first move the item up past the parent, and later empty the parent and the slot of the insert as bottom slots. The insert then stops with its tag still on the item, and every later insert that reaches that slot waits for ever. The tests replay such a schedule. Climb to the root instead, as Herlihy and Shavit do.
- **Tags that are not unique.** The tag must name one running insert. Reusing the id of a thread for two inserts at the same time breaks the owner checks.
- **A fixed capacity.** The array has $N$ slots. Growing it needs a lock on the whole heap.

## Implementations

The Python module keeps each slot as a lock, a tag and a priority, and models each lock attempt and each change of a slot as one step of a generator; a call that waits yields "spin". The tests check the bit-reversed order, replay the example step by step, replay the schedule of the two overlapping delete-mins and the schedule with a wrong EMPTY and show with a linearizability search that they have no legal order, replay a schedule in which deletes empty the path below a paused insert, compare random sequential runs with a multiset, and run random interleavings of several threads, checking that the final heap is valid, that no item is lost or duplicated, and that calls that overlap no other call are exact. A last test runs the plain methods under real threads.

## History

Biswas and Browne in 1987, Rao and Kumar in 1988 and Ayani in 1990 gave concurrent heaps in which every insert went from the root down, so all calls met at the root. Hunt, Michael, Parthasarathy and Scott published the bottom-up insert with tags and the bit-reversed order of the bottom slots in 1996. Herlihy and Shavit's textbook made it the standard example of a fine-grained heap. Later work on concurrent priority queues turned to skip lists and to relaxed queues.

## References
