---
tag: XC1TS5
kind: algorithm
slug: hyaline
name: Hyaline
aliases: [Hyaline reclamation, Hyaline-1, Hyaline-1S]
area: concurrency/memory-reclamation
level: research
summary: Retired nodes go in batches into the lists of the threads that are inside an operation. Each thread releases its list when it leaves, and the last release frees the batch.
solves: [safe-memory-reclamation]
complexity:
  vars: {n: the number of processes, B: the number of nodes born at or before the era of a stopped process}
  space: {slots: Θ(n), garbage_held_by_a_stopped_process_1S: O(n B)}
  steps: {enter: O(1), leave_per_batch: O(1), retire_per_node: O(1)}
properties: {robust: false, robust_1S: true, bounded_garbage_1S: true, per_node_cost: false, snapshot_free: true}
history:
  year: 2019
  people: [Ruslan Nikolaev, Binoy Ravindran]
  note: Nikolaev and Ravindran presented Hyaline as a brief announcement at PODC 2019, and the full family, with Hyaline-1, Hyaline-S and Hyaline-1S, at PLDI 2021.
prereqs: [safe-memory-reclamation, reference-counting]
see_also: [epoch-based-reclamation, hazard-eras, interval-based-reclamation, lock-free-reference-counting, hazard-pointers, debra]
sources:
  - paper: doi:10.1145/3453483.3454090
    title: Ruslan Nikolaev and Binoy Ravindran, Snapshot-free, transparent, and robust memory reclamation for lock-free data structures, PLDI 2021
    locator: Section 4.1 with Figure 7 (Hyaline) and Figure 8 (Hyaline-1 with swap and an insert counter), Section 4.2 with Figure 9 (Hyaline-S and Hyaline-1S, birth eras, deref and the skip of slots with old access eras)
  - paper: doi:10.1145/3293611.3331575
    title: Ruslan Nikolaev and Binoy Ravindran, Brief announcement, Hyaline, fast and transparent lock-free memory reclamation, PODC 2019
    locator: the first account of the batch reference counts and the per-slot retirement lists
  - paper: doi:10.1145/3178487.3178488
    title: Haosen Wen, Joseph Izraelevitz, Wentao Cai, H. Alan Beadle and Michael L. Scott, Interval-based memory reclamation, PPoPP 2018, pages 1-13
    locator: the birth epochs and the wrapped pointer read that Hyaline-S takes over
---

Hyaline is a family of [safe memory reclamation](/safe-memory-reclamation/) methods by Ruslan Nikolaev and Binoy Ravindran that uses [reference counting](/reference-counting/) only at reclamation time. A thread marks the start and the end of each operation in its own slot. A thread that retires nodes collects them in a batch, and then puts the batch into the list of every slot whose thread is inside an operation, and counts how many it reached. When a thread leaves, it takes its list and subtracts one from the count of each batch in it. The thread that brings a count to zero frees the batch. No thread ever scans the slots of the others to decide whether a node is free. This page implements Hyaline-1, with one slot per thread, and its robust form Hyaline-1S, which adds birth eras so that a stopped thread holds back only old batches. The general Hyaline, with shared slots and a double-width head, is described but not implemented.

## In plain words

An office throws away old papers in bundles. When a worker sits down at a desk, they put up a flag.

To throw away a bundle, you put one copy of a note "bundle 7 is out" on every desk with a flag up, and you write on the bundle how many notes you put out.

When a worker stands up, they take down the flag, pick up the notes on their desk, and cross one off each bundle. The worker who crosses off the last note throws the bundle away.

A worker who sat down after the bundle was ready needs no note: they cannot reach the old papers. In the robust version, a note goes only to workers who have looked at something as new as the oldest paper in the bundle, so a worker who fell asleep early does not hold up new bundles.

## The problem

[Safe memory reclamation](/safe-memory-reclamation/) for lock-free structures such as the [Treiber stack](/treiber-stack/) and the [Michael and Scott queue](/michael-scott-queue/). [Epoch-based reclamation](/epoch-based-reclamation/) is fast, but a reclaiming thread must check all threads, and one stopped thread stops all reclamation. [Hazard pointers](/hazard-pointers/) are robust but cost a write per node and a scan of all slots. Hyaline wants the cost of epochs, with the work of freeing spread over the threads that leave, and in the -1S form the robustness of [hazard eras](/hazard-eras/).

The model: $n$ asynchronous processes on a sequentially consistent shared memory with reads, writes, swap, fetch-and-add and [compare-and-swap](/compare-and-swap/). Process $q$ has a head word $H[q] = (HRef, HPtr)$ that fits in one machine word because $HRef$ is one bit. A batch has $n + 1$ nodes: one counter node $ref$ with the field $NRef$, and $n$ list nodes, one per slot. Each list node has a link $blink$ and a pointer $bref$ to the counter node. In Hyaline-1S, a global era grows once every $F$ allocations of a process, each node has a birth era, and each slot has an access era $A[q]$.

## The algorithm

```pseudo id=main
ENTER()
L1  H[me] ← (1, nil)
PROTECT(src)                         ▷ Hyaline-1S only; Hyaline-1 reads src once
L2  p ← src; e ← era
L3  if e = A[me] then return p
L4  A[me] ← e; goto L2
LEAVE()
L5  (_, p) ← SWAP(H[me], (0, nil))
L6  while p ≠ nil: next ← p.blink; ref ← p.bref
L7      if FAA(ref.NRef, −1) = 1 then free every node of the batch of ref; p ← next
RETIRE_BATCH(β)                      ▷ β has n + 1 nodes; ref.NRef ← 0; I ← 0
L8  for each slot q, with its own list node y of β:
L9      read h ← H[q]; if h.HRef = 0 then go to the next slot
L10     if Hyaline-1S and A[q] < min birth era in β then go to the next slot
L11     y.blink ← h.HPtr; if CAS(H[q], h, (1, y)) then I ← I + 1 else go back to L9
L12 if FAA(ref.NRef, I) = −I then free every node of β
```

A batch is put only into slots whose thread is inside an operation, because only those threads can still hold a node of it: a thread that enters later cannot reach nodes that were unlinked before. The count $I$ is added at the end, after all inserts. Until then the count is zero or negative, so a thread that leaves early cannot free the batch by mistake.

Hyaline-1S adds the check at L10. A thread that is inside an operation but whose access era is older than every node of the batch has not read any node of the batch, and cannot read one later, because PROTECT would first raise its era. So the batch can skip its slot. A stopped thread keeps its old era for good, and so it holds back only batches that contain a node born at or before that era.

## Example

A stack $top \to A \to B \to C \to D$, two processes, so a batch has three nodes. Process $p$ pops once and process $q$ pops three times. This is Hyaline-1.

| step | process | line | action | state after |
|---|---|---|---|---|
| 1 | $p$ | L1 | enters | $H[p] = (1, nil)$ |
| 2 | $p$ | pop | reads $top = A$ | |
| 3 | $q$ | three pops | unlinks $A$, $B$ and $C$; the batch $\{A, B, C\}$ is full, $A$ is the counter node | $top = D$ |
| 4 | $q$ | L8 to L11 | slot $p$ is active: CAS puts $B$ in front | $H[p] = (1, B)$, $I = 1$ |
| 5 | $q$ | L8 to L11 | slot $q$ is active (in its third pop): CAS puts $C$ in front | $H[q] = (1, C)$, $I = 2$ |
| 6 | $q$ | L12 | adds 2 | $A.NRef = 2$ |
| 7 | $q$ | L5 to L7 | leaves, takes $C$, subtracts 1 | $A.NRef = 1$ |
| 8 | $p$ | pop | reads $A.next$ safely; its CAS fails; it pops $D$ | |
| 9 | $p$ | L5 to L7 | leaves, takes $B$, subtracts 1: the count is 0, frees $A$, $B$, $C$ | |

With an immediate free, $A$ is freed at step 3, and the read at step 8 is a use after free. The test finds this run.

## Correctness

The full proof is in proofs/correctness.md. It assumes that a process uses a node only inside an operation and only if the node was reachable at the read that returned it (the stack reads from the root, and the dequeue checks the head again), retires each node once after its unlink, and does not link a retired node again.

- **Key fact.** Each insert into a slot is matched by exactly one decrement, by the owner of the slot after it leaves. The count is added after all inserts, so it reaches zero once, after every slot that got the batch has left.
- **Safety.** A thread that may use a node of a batch is inside an operation when the batch is inserted, so its slot is active and gets a list node. In Hyaline-1S, its access era is at least the birth era of that node, so L10 does not skip it.
- **Bound (Hyaline-1S).** A stopped process with access era $a$ holds back at most one batch per node born at or before $a$.

The test file checks every interleaving of a stack run and a queue run for both versions, seeded random runs, two broken versions (a leave that subtracts before it reads the link, and Hyaline-1S without the re-read in PROTECT), an immediate free, and the garbage under a stall.

## Complexity

| measure | value |
|---|---|
| shared space | one head word per process, one access era per process in -1S |
| ENTER | 1 write |
| LEAVE | 1 swap, plus 3 steps per batch in the list |
| RETIRE | $O(n)$ steps per batch of $n + 1$ nodes, so $O(1)$ per node |
| PROTECT in -1S | 2 reads when the era did not move |
| garbage held by a stopped process | Hyaline-1: no bound; -1S: at most $(n + 1) B$ nodes |

**Garbage under a stall.** The test runs three processes on a structure with four nodes, with process 0 stopped inside its first pop and the others doing 50 or 400 operations. Hyaline-1 keeps all of them: the peak is at least 50 or 400. Hyaline-1S with $F = 2$ stays between 7 and 17 in all runs. The test checks the bound $n^2 + (n + 1)(B + 2(n - 1)) = 53$, in which $B = 4 + n(F - 1) = 7$ is the number of nodes born in era 1. The first two parts are proved; the allowance of $2(n - 1)$ batches in the slots of the running processes is for this workload only.

## Properties

- Snapshot free: no thread reads all slots to decide whether a node can be freed. The work of freeing is done by the last thread to leave, so it is spread over the threads.
- Hyaline-1 is not robust. Hyaline-1S is robust: a stopped thread holds back only batches with an old node.
- ENTER and LEAVE are wait free. RETIRE is lock free.
- Transparent in the full Hyaline: threads can share slots and come and go, because nothing is tied to a thread identity. Hyaline-1 gives this up for single-width atomics.
- Each node carries two extra words while it is retired, and a birth era in -1S.

## Variants and improvements

- **Hyaline.** The general version: $k$ slots shared by any number of threads, $HRef$ counts the threads in a slot, the head needs a double-width CAS or LL/SC, and an insert adjusts the count of the batch that it puts in front of.
- **Hyaline-S.** The robust form of the general version. Threads share access eras per slot, and an acknowledgment counter per slot lets entering threads move away from slots held by stopped threads. The number of slots can grow.
- **[Interval-based reclamation](/interval-based-reclamation/) and [hazard eras](/hazard-eras/).** The source of the birth eras and the wrapped pointer read. They decide by scanning reservations; Hyaline decides by counting.
- **Crystalline.** A later wait-free method by the same authors (2021) builds on Hyaline.

## When to use it

Use Hyaline when the number of threads is large or changes, as in thread pools with many short-lived threads, or under oversubscription, where scanning all threads is slow. Use Hyaline-1S when a thread can stall inside an operation and the garbage must stay bounded. Hyaline needs a batch of more nodes than there are slots before it reclaims anything, so with many slots and few retires memory is freed late.

## Pitfalls

**Subtracting before reading the link.** The wrong code at L6 and L7 does the decrement first and then reads $p.blink$. If that decrement is not the last one, another thread can free the batch before the read, and the read of $p.blink$ is a use after free. The right code reads $next$ and $ref$ at L6 and decrements at L7.

**Adding the count before the inserts.** If the count $I$ were added before all inserts, or as each insert happens, a thread could leave and bring the count to zero while a later slot still has to get its node. The right code adds the total once, at L12.

**Skipping the re-read in Hyaline-1S.** Writing the era once after the pointer read, without the loop at L2 to L4, lets a thread use a node born after the era in its slot. A batch then skips the slot at L10 and is freed under the thread. The test finds this.

**Batches that are too small.** A batch needs a list node for every slot, so it needs at least $n + 1$ nodes. Fewer nodes leave some active slot without a node, and the batch would be freed while that thread may still use it.

## Implementations

## History

Ruslan Nikolaev and Binoy Ravindran presented Hyaline as a brief announcement at PODC 2019, and the full paper, with Hyaline, Hyaline-1, Hyaline-S and Hyaline-1S and the adaptive growth of slots, at PLDI 2021. The name means glass-like: the method is meant to be transparent to the data structure and to the threads. The robust forms take the birth eras of [hazard eras](/hazard-eras/) (Ramalhete and Correia, 2017) and [interval-based reclamation](/interval-based-reclamation/) (Wen and others, 2018), but use them only to detect stalled threads, not to define when a node can be freed.

## References
