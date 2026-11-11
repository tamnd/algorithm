---
tag: FY15RG
kind: data-structure
slug: herlihy-wing-queue
name: Herlihy-Wing queue
aliases:
- Herlihy-Wing linearizable queue
area: concurrency/lock-free-structures
level: advanced
summary: Array queue with fetch-and-add on back and swap on slots. Linearizable, but an enqueue has no fixed linearization point. Enqueue is wait-free; dequeue waits on an empty queue.
implements: [queue]
complexity:
  vars: {n: the number of processes, r: the number of enqueues that have started}
  space: {extra: Θ(r)}
properties: {persistent: false, concurrent: true, external: false}
prereqs: [queue, fetch-and-add, linearizability, linearization-point]
see_also: [michael-scott-queue, read-modify-write, kogan-petrank-queue, lcrq, wait-freedom, lock-freedom, consensus-number, concurrent-queue]
sources:
  - paper: doi:10.1145/78969.78972
    title: "Maurice P. Herlihy and Jeannette M. Wing, Linearizability: a correctness condition for concurrent objects, ACM TOPLAS 12(3), 1990, pp. 463-492"
    locator: Section 4 (the queue implementation with INC, STORE and SWAP and the discussion that its enqueue has no single linearization point)
  - paper: "Thomas A. Henzinger, Ali Sezgin and Viktor Vafeiadis, Aspect-oriented linearizability proofs, CONCUR 2013, LNCS 8052"
    locator: the characterization of linearizable queue histories by forbidden patterns and its use on the Herlihy-Wing queue
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, 2020
    locator: Chapter 3 (Concurrent objects), the discussion of linearization points; Chapter 10 for total and partial queue methods
---

The Herlihy-Wing queue is a concurrent [queue](/queue/) on an array, given by Maurice Herlihy and Jeannette Wing in their 1990 paper on [linearizability](/linearizability/). An enqueue takes a fresh slot with one [fetch-and-add](/fetch-and-add/) on a counter `back` and then writes its item into the slot. A dequeue reads `back` and scans the slots from the start, emptying each one with an atomic swap until it gets an item. The queue is linearizable, but it is the standard example of an object whose operations have no fixed [linearization point](/linearization-point/): which enqueue counts as first can depend on what happens after both enqueues have taken their steps. An enqueue is [wait-free](/wait-freedom/), and a dequeue waits for as long as the queue is empty, so the queue as a whole is not [lock-free](/lock-freedom/).

## In plain words

Picture a long row of numbered boxes and a ticket machine. Someone who wants to add an item takes the next ticket, walks to the box with that number, and puts the item in. Someone who wants to take an item looks at the last ticket number given out, and opens the boxes from the first one up to that number, until one has an item; they take it out. If all the boxes are empty, they start again from the first box.

The tickets give the order of the boxes, but not the order of the items: a person with ticket 1 may still be on the way while the item of ticket 2 is already in its box and is taken first.

## The abstract type

The object is a FIFO queue with enq$(x)$ and deq(). Here deq is a *partial* operation: on an empty queue it does not return EMPTY, it waits until an item comes. Items are taken to be distinct, which the proof uses. The safety condition is [linearizability](/linearizability/) with respect to the sequential queue in which deq on an empty queue is not enabled.

## Representation

### Model and notation

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $p, q$ | process names |
| $i, j$ | slot indices |
| $r$ | the value of `back`: the number of enqueues that have taken a slot |

The processes are asynchronous and may crash between steps. The queue uses atomic read and write, [fetch-and-add](/fetch-and-add/) (consensus number 2) and swap (consensus number 2), and no CAS. The memory is sequentially consistent. The array is infinite in the paper; a real version needs a bound or a way to recycle slots.

### Fields

- `items`$[0, 1, 2, \ldots]$: the slots, each NONE at the start.
- `back`: the index of the next free slot, 0 at the start.

**Invariant.** Each slot is written at most once by an enqueue, after that enqueue took the slot by fetch-and-add, and emptied at most once by a swap that returns its item. So each item is taken at most once.

## Operations

```pseudo id=main
ENQ(x)
L1  i ← FAA(back, 1)              ▷ take a fresh slot
L2  items[i] ← x                  ▷ store the item

DEQ()
L3  loop
L4      r ← back
L5      for i ← 0 to r − 1
L6          x ← SWAP(items[i], NONE)
L7          if x ≠ NONE then return x
```

**Enqueue.** L1 gives each enqueue its own slot, in the order of the fetch-and-add steps. L2 stores the item. Between L1 and L2 the slot is reserved but still empty.

**Dequeue.** L4 reads how many slots are taken. L5 to L7 go through them in index order and swap NONE into each one. A swap returns the old content, so if two dequeues swap the same slot, only one gets the item. If the whole scan returns nothing, the dequeue starts a new scan.

**No fixed linearization point.** Fix the prefix: $p$ runs L1 of enq($x$) and gets slot 0; $q$ runs enq($y$) to the end and gets slot 1. A dequeuer $d$ then calls deq twice. Two ways to go on:

- **Run 1.** $d$ reads `back` $= 2$, finds slot 0 empty, and takes $y$ from slot 1. Then $p$ stores $x$, and the second deq takes $x$. The deqs return $y$, then $x$, so enq($y$) must come before enq($x$).
- **Run 2.** $p$ stores $x$ first. Then $d$ takes $x$ from slot 0 and then $y$ from slot 1. So enq($x$) must come before enq($y$).

Both runs share the prefix, and in it enq($y$) has completed, so its point is in the prefix. Suppose each enqueue had a fixed point at one of its own steps. In Run 2, enq($x$) must come before enq($y$), so its point must come before the point of enq($y$), that is inside the prefix; the only step of $x$ in the prefix is its FAA. Then in Run 1, enq($x$) also has its point at its FAA, which comes before both steps of $y$, so enq($x$) comes first; but Run 1 needs enq($y$) first. So neither the FAA nor the store can be the point. The order of the two enqueues is fixed only later, by the dequeues. The proofs of the paper handle this with a set of possible linearizations, not with one point.

**Progress.** The two operations have different guarantees:

- An enqueue is wait-free: it takes exactly 2 steps.
- A dequeue on an empty queue spins for ever. A run in which one process calls deq on an empty queue and nobody enqueues has infinitely many steps and no completed operation, so the queue is not lock-free. This is the meaning of a partial operation, not a bug.
- A dequeue is not blocked by a stalled enqueuer: if $p$ stops between L1 and L2, its slot stays empty, and dequeues skip it and take later items.
- If from some time on there is always an item that is stored and not yet taken, then among the dequeues that keep running, some dequeue completes: a scan that starts after the item is stored either finds it, or finds that another dequeue took an item. But one dequeue can starve: others can take each new item just before its scan reaches the slot.

### Memory reclamation

There are no nodes and nothing to free. The cost is the array itself: slots are never reused, and a scan always starts at slot 0, so the queue needs space for each enqueue ever done, and the scan gets longer over time. This is why the queue is a teaching example and not a practical design. Practical queues that take slots with fetch-and-add, such as [LCRQ](/lcrq/), reuse a ring of slots and solve the problems that this brings.

## Example

The prefix and Run 1 from above, step by step. Slots hold NONE at the start.

| step | process | line | action | slots 0, 1 after it | result |
|---|---|---|---|---|---|
| 1 | $p$ | L1 | FAA(`back`, 1) | NONE, NONE | slot 0 |
| 2 | $q$ | L1 | FAA(`back`, 1) | NONE, NONE | slot 1 |
| 3 | $q$ | L2 | items[1] $\leftarrow y$ | NONE, $y$ | enq($y$) returns |
| 4 | $d$ | L4 | read `back` | | 2 |
| 5 | $d$ | L6 | SWAP(items[0], NONE) | NONE, $y$ | NONE |
| 6 | $d$ | L6 | SWAP(items[1], NONE) | NONE, NONE | deq returns $y$ |
| 7 | $p$ | L2 | items[0] $\leftarrow x$ | $x$, NONE | enq($x$) returns |
| 8 | $d$ | L4, L6 | read `back`, SWAP(items[0], NONE) | NONE, NONE | deq returns $x$ |

A linearization is enq($y$), deq() $= y$, enq($x$), deq() $= x$. The enqueue of $x$ took its slot first, but it takes effect after the first dequeue.

## Correctness

The proof is a sketch. Use the view of Henzinger, Sezgin and Vafeiadis: a history of a queue with distinct items is linearizable if and only if no dequeue returns an item that was never enqueued, no item is returned twice, and the order rule holds (if enq($a$) completes before enq($b$) starts, then $b$ is not dequeued before $a$). For the partial dequeue there is no empty case to check. The first two rules follow from the invariant: a swap returns only what an enqueue stored, and each slot is emptied once. For the order rule, let enq($a$) complete before enq($b$) starts. Then $a$ got a smaller slot $i < j$ and was stored before $b$ took slot $j$. A dequeue that takes $b$ read `back` $> j$, so after the FAA of $b$, and so after $a$ was stored; its scan visits slot $i$ before slot $j$ and finds it empty, so $a$ had already been taken by an earlier swap. So $a$ is dequeued, by a swap before the swap that took $b$. The paper gives its own proof, with a set of possible values of the abstract queue in place of a single one.

## Complexity

| operation | steps |
|---|---|
| enqueue | 2, always |
| one scan of a dequeue | $1 + r$, where $r$ is the value of `back` it read |
| dequeue | unbounded: it waits on an empty queue and can starve on a non-empty one |

The space is one slot for each enqueue ever started, $\Theta(r)$. These bounds follow from the code and are shown here.

## Variants

- **[Michael-Scott queue](/michael-scott-queue/).** A lock-free queue on a linked list with CAS, with fixed linearization points and total operations (deq returns EMPTY).
- **Total dequeue.** Return EMPTY when a scan finds nothing. This is not the queue of the paper, and the argument above does not cover it: a scan that finds nothing does not show that the queue was empty at any one moment, because items can be stored in slots behind the scan while other items are taken ahead of it. A total version needs its own proof.
- **Ring buffers with fetch-and-add.** CRQ and [LCRQ](/lcrq/) take slots with fetch-and-add on a ring and fix the problems of empty slots with extra state per slot.
- **[Kogan-Petrank queue](/kogan-petrank-queue/).** A queue in which both operations are wait-free, built with helping.

## When to use it

Use it as a model and a test case, not in production. It is the shortest example of a linearizable object whose proof needs a future-dependent linearization, and it is a standard benchmark for proof methods and checkers. For a real queue, use the [Michael-Scott queue](/michael-scott-queue/) or a ring queue built on fetch-and-add.

## Pitfalls

- **Looking for the linearization point in the code.** Neither the FAA nor the store of an enqueue works for all runs, as the example shows. A proof must look at the whole history.
- **Making dequeue total in a naive way.** An empty scan does not show an empty queue, so returning EMPTY after one empty scan needs a new proof.
- **Calling it lock-free.** A dequeue on an empty queue spins with no bound; only the enqueue is wait-free.
- **Running out of slots.** With a finite array, `back` passes its end. Slots must be recycled, and that is where real ring queues become hard.

## Implementations

## History

Herlihy and Wing (1990) used the queue to show that linearizability is a property of whole histories, and that a correct object need not have a fixed step at which each operation takes effect. The example became a standard test for verification methods: Henzinger, Sezgin and Vafeiadis (2013) proved it by forbidden patterns, and later work on prophecy variables and on the checking of linearizability uses it too.

## References
